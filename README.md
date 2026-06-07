# wechat-publish skill

> Claude Code skill：把任意 markdown 文章一键变成「微信公众号风格的排版稿 → HTML → 草稿箱推送」全流程。

经过多轮迭代沉淀，固定使用单色蓝家族的高级感设计，移动端显示友好，文本零改动、图片位置零移动。

---

## 一、下载安装

skill 由 4 个文件组成，全部放在 `~/.claude/skills/wechat-publish/` 即可。

### 方式 A：手动复制

```bash
mkdir -p ~/.claude/skills/wechat-publish
# 把 SKILL.md / snippets.md / publish.py / config.md 复制进去
```

### 方式 B：通过 Git（如果你把 skill 放到了仓库里）

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone <你的仓库地址> wechat-publish
```

安装完应该是这样：

```
~/.claude/skills/wechat-publish/
├── SKILL.md       # 入口，定义流程和铁律
├── snippets.md    # 14 种排版片段库
├── publish.py     # 上传图片 + 推草稿脚本
├── config.md      # AppID/AppSecret 配置说明
└── README.md      # 当前文件
```

### 验证安装

打开任意 Claude Code 会话，输入：

```
/skills
```

应能看到 `wechat-publish` 出现在列表里。

---

## 二、前置依赖

### 1. Python 环境

`publish.py` 需要 Python 3.8+。

**检查是否已安装**：

```bash
python3 --version
```

如果显示版本号（如 `Python 3.11.x`），跳过本节。

**如果没装 / 报 command not found**：

| 操作系统 | 推荐安装方式 |
|---|---|
| **macOS** | 用 [Homebrew](https://brew.sh)：`brew install python@3.12` |
| **macOS（无 Homebrew）** | 去 [python.org/downloads](https://www.python.org/downloads/macos/) 下安装包 |
| **Windows** | 去 [python.org/downloads](https://www.python.org/downloads/windows/) 下安装包，**安装时勾选「Add Python to PATH」** |
| **Linux** | `sudo apt install python3 python3-pip` （Debian/Ubuntu） |

**最快的零配置方案**：装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，它会自动管理 Python：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

装完 uv 后，可以这样跑 publish.py，自动隔离依赖：

```bash
uv run --with requests --with beautifulsoup4 --with premailer \
  python ~/.claude/skills/wechat-publish/publish.py --html article_wechat.html --title "文章标题"
```

**完全不想碰 Python？** 那只能用阶段 1 / 阶段 2（产出 md 和 html）。HTML 文件用浏览器打开后，全选复制粘贴到[公众号编辑器](https://mp.weixin.qq.com)或 [mdnice](https://editor.mdnice.com/) 里手动发，也能用，只是图片要一张张手动上传——这种场景下 Claude 不需要碰 publish.py，会主动告诉你怎么手动操作。

### 2. Python 依赖包

```bash
pip install requests beautifulsoup4 premailer
```

（用 uv run 的话不用这步，依赖会自动装）

### 3. 微信公众号准入

发布到草稿箱的接口**不是所有公众号都能用**，必须满足：

- ✅ **已认证的订阅号或服务号**
- ❌ 个人订阅号没有这个接口权限（会返回 `errcode: 48001`）
- ❌ 未认证账号也不行

如果你的号不符合，那这个 skill 只能用前两个阶段（产出 md / html），最后一步需要手动复制粘贴。

---

## 三、绑定公众号 API（含 IP 白名单 ⚠️）

**这步最容易踩坑，请仔细做。**

### Step 1 — 拿到 AppID 和 AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 左下角菜单：**设置与开发 → 基本配置**
3. 找到「公众号开发信息」：
   - **AppID**：直接复制
   - **AppSecret**：点「重置」→ 扫码验证 → 保存生成的字符串
     - ⚠️ AppSecret 关闭弹窗就再也看不到了，先存好
     - ⚠️ 重置后旧的会立刻失效，所有用旧 secret 的脚本都得更新

### Step 2 — 把本机 IP 加进白名单 ⚠️

**没做这步会直接 `errcode: 40164`**。微信对接口调用方有 IP 白名单管控。

1. 查询本机的**公网 IP**（不是 192.168.x.x 那种内网 IP）：

   ```bash
   curl ifconfig.me
   # 或
   curl ip.sb
   ```

   输出类似 `123.45.67.89` 这种就是公网 IP。

2. 回到「基本配置」页面，找到「IP 白名单」一栏 → 点「查看」→ 扫码 → 「修改」

3. 把刚查到的 IP 填进去，每行一个，**保存**

4. 注意事项：
   - 白名单上限 **50 个 IP**
   - **IP 会变**：换 WiFi、出差、运营商分配的动态 IP 会变。换地方后跑脚本前先 `curl ifconfig.me` 看看变没变
   - 笔记本经常在不同地点用的话，建议加进多个常用网络的 IP
   - 如果你有固定公网 IP（自建服务器），那就方便了

### Step 3 — 配置凭证给脚本

按推荐度从高到低，选一种：

#### 推荐：环境变量

```bash
# 加进 ~/.zshrc 或 ~/.bashrc
export WECHAT_APPID="wxxxxxxxxxxxxxxxxx"
export WECHAT_APPSECRET="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

# 重载
source ~/.zshrc
```

#### 备选：当前目录凭证文件

在文章所在目录创建 `.wechat_credentials.json`：

```json
{
  "appid": "wxxxxxxxxxxxxxxxxx",
  "appsecret": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
}
```

⚠️ 加进 `.gitignore`：

```
.wechat_credentials.json
```

#### 临时：命令行参数

```bash
python ~/.claude/skills/wechat-publish/publish.py \
  --appid wxxxxx --appsecret yyyyy \
  --html article_wechat.html --title "标题"
```

更详细的说明见同目录的 [config.md](./config.md)。

---

## 四、触发使用

在 Claude Code 会话里，**自然语言**就能触发这个 skill。触发词示例：

| 你说的话 | Claude 会做什么 |
|---|---|
| 「把 article.md 转成微信公众号排版」 | 走阶段 1：产出 `article_wechat.md` |
| 「再转成 HTML」 / 「转成 html 给我」 | 走阶段 2：产出 `article_wechat.html` |
| 「推送到草稿箱」 / 「上传到公众号」 / 「发布」 | 走阶段 3：调 `publish.py` 推送 |
| 「把这篇文章发到公众号」 | 一次性走完三阶段（中间会停下让你审阅） |

### 完整示例对话

```
你：把桌面上的 article.md 排版成公众号样式

Claude：[读取 article.md，应用 snippets.md 里的片段]
       已产出 article_wechat.md。应用了：
       - 封面卡 1 处
       - 章节胶囊 3 处（一/二/三）
       - 编号卡片 28 处
       - 子标签竖条 12 处
       - callout 引用块 6 处
       预览看看？要调整哪里？

你：[审阅，可能要求改某段]

你：转成 HTML

Claude：[产出 article_wechat.html]
       已产出 article_wechat.html，浏览器打开可预览。

你：[浏览器看一眼]

你：推送到草稿箱

Claude：[确认 AppID 已配置]
       即将运行 publish.py，会上传 N 张图、推一篇草稿，确认？

你：确认

Claude：[运行脚本]
       ✅ 已推送，draft media_id: xxx
       请去公众号后台 → 草稿箱审阅发布。
```

### 不显式触发也能用

直接说「我想把这篇文章发到公众号」之类的话，Claude 会自动识别需求并调起这个 skill。

---

## 五、设计风格预览

固定的视觉锤：

- **3 色蓝家族**：`#2C5282` 主色 + `#1E3A5F` 渐变副色 + `#F0F4F8/#F5F8FB` 浅底
- **封面 / 结尾**：深蓝渐变卡 + 英文 caption + 极细分隔线
- **大节标题**：右切圆角的胶囊，左侧贴边
- **编号项**：浅渐变卡 + Georgia 衬线的 `01/02` 徽章 + 蓝色粗体标题
- **a/b/c 子标签**：4×18px 深蓝小竖条 + 蓝粗体
- **关键结论**：浅蓝底 + 左竖条 callout

完整片段库见 [snippets.md](./snippets.md)。

---

## 六、常见问题

| 问题 | 排查 |
|---|---|
| `/skills` 看不到 `wechat-publish` | 文件没放对位置，确认在 `~/.claude/skills/wechat-publish/SKILL.md` |
| `errcode: 40001` | AppSecret 错了，重新生成 |
| `errcode: 40164` | **IP 不在白名单**，跑 `curl ifconfig.me` 看现在的 IP，加进白名单 |
| `errcode: 48001` | 公众号未认证或类型不对（个人号无草稿箱接口） |
| `errcode: 45009` | 接口调用超限，等几分钟 |
| 图片在草稿里显示不出来 | GitHub 图片防盗链，本脚本会先下载再上传，正常不会有这问题；若有，检查图片 URL 是否能 `curl` 通 |
| 中文在草稿里乱码 | 脚本已用 `ensure_ascii=False`，正常不会出现；如出现，检查 Python 版本（须 3.8+） |
| 排版在 PC 端浏览器好看但手机微信里塌了 | 用 mdnice 之类的预览工具看微信视图效果，不要只看 PC 浏览器 |
| 不想用 Python | 见上文「完全不想碰 Python」一段；阶段 1/2 都能用，只是阶段 3 要手动 |

---

## 七、文件清单

| 文件 | 作用 |
|---|---|
| [SKILL.md](./SKILL.md) | skill 入口，给 Claude 读，定义流程和铁律 |
| [snippets.md](./snippets.md) | 14 种排版片段的完整 HTML，给 Claude 抄 |
| [publish.py](./publish.py) | 上传图片 + 推草稿 Python 脚本 |
| [config.md](./config.md) | API 凭证配置详细说明 |
| [README.md](./README.md) | 当前文件，给人类看 |
