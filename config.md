# 微信公众号 API 配置

发布脚本（`publish.py`）需要公众号的 **AppID** 和 **AppSecret** 才能调用接口。本文档说明如何获取并安全配置。

> **首次运行前先装依赖**（脚本不会自动装，缺包直接 `ModuleNotFoundError`）：
> ```bash
> pip install requests beautifulsoup4 premailer
> ```
> 详见下文「四、依赖安装」。

## 一、前置条件

公众号必须满足以下条件才能用草稿箱接口：

- **已认证的订阅号或服务号**（个人订阅号无草稿箱接口权限，会返回 `errcode: 48001`）
- 当前 IP 已加入「IP 白名单」（每天上限 50 个 IP，公众号后台可改）

## 二、获取 AppID / AppSecret

1. 登录 [公众号后台](https://mp.weixin.qq.com/)
2. 左侧菜单：**设置与开发 → 基本配置**
3. 「公众号开发信息」一栏：
   - **AppID（开发者 ID）**：直接复制
   - **AppSecret（开发者密码）**：点「重置」并保存生成的值（一旦关闭页面就看不到了）
4. 同一页面下方「IP 白名单」：把本机公网 IP 加进去
   - 查公网 IP：`curl ifconfig.me`

## 三、配置凭证（按推荐度排序）

### 方式 1：环境变量（推荐）

最适合本地长期使用，不会把凭证写进任何文件。

```bash
# 临时（仅当前 shell 有效）
export WECHAT_APPID="wxxxxxxxxxxxxxxxxx"
export WECHAT_APPSECRET="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

# 持久化（zsh）
echo 'export WECHAT_APPID="wxxxxxxxxxxxxxxxxx"' >> ~/.zshrc
echo 'export WECHAT_APPSECRET="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"' >> ~/.zshrc
source ~/.zshrc
```

### 方式 2：项目目录下的凭证文件

适合多公众号切换。在文章所在目录创建 `.wechat_credentials.json`：

```json
{
  "appid": "wxxxxxxxxxxxxxxxxx",
  "appsecret": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
}
```

**记得加进 `.gitignore`**：
```
.wechat_credentials.json
```

### 方式 3：命令行参数

适合 CI/CD 或临时切换：

```bash
python ~/.claude/skills/wechat-publish/publish.py \
  --html article_wechat.html \
  --title "文章标题" \
  --appid wxxxxxxxxxxxxxxxxx \
  --appsecret yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

### 方式 4：编辑脚本顶部默认值（不推荐）

仅用于个人快速尝试。会把凭证留在脚本里，**千万不要 commit 到 git**。

## 四、依赖安装

```bash
pip install requests beautifulsoup4 premailer
```

或用 uv：

```bash
uv pip install requests beautifulsoup4 premailer
```

## 五、验证配置

```bash
# 在 HTML 文件所在目录运行
cd ~/Desktop
python ~/.claude/skills/wechat-publish/publish.py --html article_wechat.html --title "测试文章"
```

预期输出：
```
====================================================
  微信公众号发布脚本（wechat-publish skill）
====================================================
✅ Access Token 获取成功

📷 共发现 N 张图片，开始上传...

[1/N] 处理中...
  📌 第一张图将作为封面...
  ✅ 封面图上传成功，media_id: xxx...
  ✅ 上传成功：https://...
[2/N] 处理中...
  ✅ 上传成功：https://...
...

🎨 正在内联 CSS 样式（保留排版与字体）...
✅ CSS 内联完成

🎉 成功推送到草稿箱！media_id: yyy
👉 请前往公众号后台「草稿箱」查看并发布。
```

## 六、常见错误

| errcode | 含义 | 解决 |
|---|---|---|
| `40001` | AppSecret 无效 | 重新生成并更新配置 |
| `40164` | IP 不在白名单 | 把当前公网 IP 加进基本配置里的 IP 白名单 |
| `45009` | 接口调用频率超限 | 等几分钟再试 |
| `48001` | 接口未授权 | 公众号未认证或非订阅号/服务号；个人号无此权限 |
| `41006` | 缺 media_id | 第一张图没上传成功（图片 URL 失效或下载超时） |

## 七、安全提醒

- AppSecret 相当于公众号的 API 密码——泄露后任何人都能以你的身份发文章。
- 一旦泄露立刻去后台「重置」。
- 不要把含 AppSecret 的文件 commit 到 git。建议在项目根 `.gitignore` 里加上 `.wechat_credentials.json`、`.env`。
