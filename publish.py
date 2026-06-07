"""
微信公众号一键发布脚本（wechat-publish skill 的发布阶段）

功能：解析 HTML → 下载 GitHub/外链图片 → 上传到公众号素材库 → 替换链接 → 推送草稿箱
第一张图片自动上传为永久素材作为封面图（thumb_media_id）

依赖：
  pip install requests beautifulsoup4 premailer

用法：
  # 通过命令行参数
  python publish.py --html article_wechat.html --title "文章标题" [--author "作者"]

  # 也可以编辑下方默认值后直接运行
  python publish.py

凭证读取顺序（前者优先）：
  1. 命令行参数 --appid / --appsecret
  2. 环境变量 WECHAT_APPID / WECHAT_APPSECRET
  3. 同目录下的 .wechat_credentials.json：{"appid": "...", "appsecret": "..."}
  4. 脚本顶部的硬编码默认值（不推荐用于生产）
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from premailer import transform

# ===== 默认值（建议改用环境变量或 .wechat_credentials.json） =====
DEFAULT_APPID = ""
DEFAULT_APPSECRET = ""
DEFAULT_HTML = "article_wechat.html"
DEFAULT_TITLE = "未命名文章"
DEFAULT_AUTHOR = ""
# ==============================================================


def load_credentials(args):
    """按优先级解析 AppID / AppSecret。"""
    appid = args.appid or os.environ.get("WECHAT_APPID") or DEFAULT_APPID
    secret = args.appsecret or os.environ.get("WECHAT_APPSECRET") or DEFAULT_APPSECRET

    cred_file = Path(args.cred_file) if args.cred_file else Path.cwd() / ".wechat_credentials.json"
    if (not appid or not secret) and cred_file.exists():
        try:
            data = json.loads(cred_file.read_text(encoding="utf-8"))
            appid = appid or data.get("appid", "")
            secret = secret or data.get("appsecret", "")
        except Exception as e:
            print(f"⚠️  读取 {cred_file} 失败：{e}")

    if not appid or not secret:
        print("❌ 缺少 AppID / AppSecret。请用以下任一方式配置：")
        print("   1) 命令行：--appid xxx --appsecret xxx")
        print("   2) 环境变量：export WECHAT_APPID=xxx WECHAT_APPSECRET=xxx")
        print("   3) 当前目录下创建 .wechat_credentials.json")
        print('      内容：{"appid": "wx...", "appsecret": "..."}')
        sys.exit(1)
    return appid, secret


def get_access_token(appid, secret):
    """获取微信 Access Token。"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {"grant_type": "client_credential", "appid": appid, "secret": secret}
    resp = requests.get(url, params=params, timeout=15).json()
    if "access_token" not in resp:
        err = resp.get("errcode")
        msg = f"获取 Token 失败：{resp}"
        if err == 40164:
            try:
                public_ip = requests.get("https://ifconfig.me", timeout=5).text.strip()
            except Exception:
                public_ip = "<查询失败，请手动 curl ifconfig.me>"
            msg += (
                f"\n\n   → 错误 40164：当前 IP 不在公众号白名单。\n"
                f"   → 当前公网 IP：{public_ip}\n"
                f"   → 解决：登录 https://mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单，添加此 IP"
            )
        elif err == 40013:
            msg += "\n\n   → 错误 40013：AppID 无效，请检查配置"
        elif err == 40001:
            msg += "\n\n   → 错误 40001：AppSecret 无效或被重置，需重新生成"
        raise RuntimeError(msg)
    print("✅ Access Token 获取成功")
    return resp["access_token"]


def upload_image(token, img_url, as_thumb=False, base_dir=None):
    """下载图片并上传到公众号素材库。

    Args:
        token: access_token
        img_url: 图片 URL 或本地路径
        as_thumb: True → 永久素材（封面图），返回 media_id
                  False → 图文消息图片（正文），返回 URL
        base_dir: 解析相对路径时使用的基准目录
    """
    try:
        if img_url.startswith("http"):
            headers = {"User-Agent": "Mozilla/5.0"}
            img_resp = requests.get(img_url, headers=headers, timeout=15)
            img_resp.raise_for_status()
            content_type = img_resp.headers.get("Content-Type", "image/png")
            img_bytes = img_resp.content
        else:
            local_path = Path(img_url)
            if not local_path.is_absolute() and base_dir:
                local_path = Path(base_dir) / img_url
            if not local_path.exists():
                print(f"  ⚠️  本地文件不存在：{local_path}")
                return None
            img_bytes = local_path.read_bytes()
            suffix = local_path.suffix.lower().lstrip(".")
            mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                        "gif": "image/gif", "webp": "image/webp"}
            content_type = mime_map.get(suffix, "image/png")
        # 兼容下方扩展名解析逻辑
        class _R:
            pass
        img_resp = _R()
        img_resp.content = img_bytes

        ext = "png"
        if "jpeg" in content_type or "jpg" in content_type:
            ext = "jpg"
        elif "gif" in content_type:
            ext = "gif"
        elif "webp" in content_type:
            ext = "webp"

        if as_thumb:
            upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        else:
            upload_url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"

        files = {"media": (f"img.{ext}", img_resp.content, content_type)}
        result = requests.post(upload_url, files=files, timeout=30).json()

        if as_thumb and "media_id" in result:
            print(f"  ✅ 封面图上传成功，media_id: {result['media_id'][:20]}...")
            return result["media_id"]
        if not as_thumb and "url" in result:
            print(f"  ✅ 上传成功：{img_url[:60]}...")
            return result["url"]
        print(f"  ⚠️  上传失败：{result}")
        return None
    except Exception as e:
        print(f"  ⚠️  处理失败：{e}")
        return None


def process_html(token, html_path):
    """读取 HTML，上传所有图片并替换链接，最后内联 CSS。"""
    html = Path(html_path).read_text(encoding="utf-8")
    base_dir = Path(html_path).resolve().parent

    img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
    img_urls = img_pattern.findall(html)

    print(f"\n📷 共发现 {len(img_urls)} 张图片，开始上传...\n")

    thumb_media_id = None
    for i, img_url in enumerate(img_urls, 1):
        print(f"[{i}/{len(img_urls)}] 处理中...")

        if i == 1:
            # 第一张图同时上传为封面 + 正文图
            print("  📌 第一张图将作为封面...")
            thumb_media_id = upload_image(token, img_url, as_thumb=True, base_dir=base_dir)
            if thumb_media_id:
                new_url = upload_image(token, img_url, as_thumb=False, base_dir=base_dir)
                if new_url:
                    html = html.replace(img_url, new_url, 1)
        else:
            new_url = upload_image(token, img_url, as_thumb=False, base_dir=base_dir)
            if new_url:
                html = html.replace(img_url, new_url, 1)

        time.sleep(0.3)  # 避免请求过快被限流

    if not thumb_media_id:
        print("\n⚠️  未获取到封面图 media_id，请确保 HTML 中有可访问的图片")

    # 内联 CSS：微信草稿接口会剥掉 <head>/<style>，必须 inline
    print("\n🎨 正在内联 CSS 样式（保留排版与字体）...")
    html = transform(
        html,
        keep_style_tags=False,
        remove_classes=False,
        strip_important=False,
        cssutils_logging_level="CRITICAL",
    )
    print("✅ CSS 内联完成")

    return html, thumb_media_id


def create_draft(token, title, author, content_html, thumb_media_id):
    """推送文章到草稿箱。"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "content": content_html,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    # ensure_ascii=False 保持中文不转义，否则草稿里会乱码
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    resp = requests.post(url, data=data, headers=headers, timeout=30).json()

    if "media_id" in resp:
        print(f"\n🎉 成功推送到草稿箱！media_id: {resp['media_id']}")
        print("👉 请前往公众号后台「草稿箱」查看并发布。")
        return resp["media_id"]

    print(f"\n❌ 推送失败：{resp}")
    err = resp.get("errcode")
    if err == 40001:
        print("   → AppID 或 AppSecret 错误，请检查配置。")
    elif err == 48001:
        print("   → 该公众号未开通「草稿箱」接口，需为已认证订阅号/服务号。")
    elif err == 45009:
        print("   → 接口调用超过限额，稍后再试。")
    return None


def parse_args():
    parser = argparse.ArgumentParser(description="微信公众号一键发布到草稿箱")
    parser.add_argument("--html", default=DEFAULT_HTML, help="HTML 文件路径")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="文章标题")
    parser.add_argument("--author", default=DEFAULT_AUTHOR, help="作者名（可空）")
    parser.add_argument("--appid", default="", help="微信公众号 AppID（覆盖环境变量）")
    parser.add_argument("--appsecret", default="", help="微信公众号 AppSecret（覆盖环境变量）")
    parser.add_argument("--cred-file", default="", help="凭证文件路径（默认 ./.wechat_credentials.json）")
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 52)
    print("  微信公众号发布脚本（wechat-publish skill）")
    print("=" * 52)

    if not Path(args.html).exists():
        print(f"❌ HTML 文件不存在：{args.html}")
        sys.exit(1)

    appid, secret = load_credentials(args)
    token = get_access_token(appid, secret)
    content_html, thumb_media_id = process_html(token, args.html)

    if not thumb_media_id:
        print("❌ 无法获取封面图，请确保 HTML 中包含图片")
        sys.exit(1)

    create_draft(token, args.title, args.author, content_html, thumb_media_id)


if __name__ == "__main__":
    main()
