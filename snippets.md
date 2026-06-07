# 排版片段库

> 每一段都是可直接复制使用的 HTML。**不要改色值、不要改字号字重**。占位符用 `{{xxx}}` 标记。

---

## 1. 封面卡（开篇大标题）

整篇文章开头第一个元素，渐变深蓝底，居中布局。

```html
<section style="text-align: center; padding: 40px 20px 36px; background: linear-gradient(135deg, #2C5282 0%, #1E3A5F 100%); border-radius: 8px; margin-bottom: 28px;">
  <p style="color: rgba(255,255,255,0.6); font-size: 11px; margin: 0 0 16px 0; letter-spacing: 5px;">{{ENGLISH CAPTION 全大写}}</p>
  <h1 style="color: #FFFFFF; font-size: 26px; margin: 0; letter-spacing: 3px; font-weight: 600;">{{主标题}}</h1>
  <div style="width: 36px; height: 1px; background: rgba(255,255,255,0.5); margin: 20px auto;"></div>
  <p style="color: rgba(255,255,255,0.85); font-size: 14px; margin: 0; letter-spacing: 2px;">{{副标题}}</p>
  <p style="color: rgba(255,255,255,0.55); font-size: 12px; margin: 18px 0 0 0; letter-spacing: 1px;">{{时间副线 / 主题串}}</p>
</section>
```

**使用场景：** 整篇文章顶部，1 次。
**变体：** 如果原文没有副标题或英文 caption，可省略对应行,但建议都给齐——有完整四段（caption / title / sub / line）质感最好。

---

## 2. 大节标题胶囊（一 · / 二 · / 三 ·）

每个一级大节（一、二、三、参考资料、END 之外的章节）的开头。

```html
<section style="margin: 36px 0 22px 0;">
  <div style="display: inline-block; background: linear-gradient(90deg, #2C5282, #1E3A5F); color: white; padding: 10px 26px 10px 22px; border-radius: 0 24px 24px 0; font-size: 18px; font-weight: 600; letter-spacing: 2px;">{{一  ·  章节标题}}</div>
</section>
```

**关键：** `border-radius: 0 24px 24px 0`——左方右圆，左侧贴齐版心，营造杂志切角感。
**分隔符：** 编号和标题用全角空格 + `·` + 全角空格（`一  ·  XXX`），不要用 `、` 或 `:`。

---

## 3. 三级标题（章节内的数字小节，如 1. 2. 3.）

```html
<h3 style="color: #2C5282; font-size: 17px; font-weight: 600; padding-bottom: 8px; border-bottom: 1px solid #D5DCE5; margin: 28px 0 18px;">{{1. 标题文本}}</h3>
```

**底边框线色** `#D5DCE5` 是冷灰，不要换暖灰。

---

## 4. 四级标题（如 3.1 / 4.2）

```html
<h4 style="color: #2C5282; font-size: 15px; font-weight: 600; margin: 24px 0 14px; padding-left: 10px; border-left: 3px solid #2C5282;">{{3.1 子标题}}</h4>
```

---

## 5. 编号卡片（替代 `_1）xxx：_ 描述` 这种斜体）

**这是最重要的视觉锤**。原文里所有 `_1) 2) 3)_` 编号子项都用这个。

```html
<section style="margin: 14px 0; padding: 14px 18px; background: linear-gradient(135deg, #F5F8FB 0%, #EAF0F7 100%); border-radius: 6px;">
<p style="margin: 0;">
<span style="display:inline-block; padding: 2px 10px; background: #2C5282; color: white; font-family: Georgia, serif; font-size: 13px; font-weight: 700; border-radius: 3px; margin-right: 12px; letter-spacing: 1px; vertical-align: 2px;">{{01}}</span>
<b style="color: #2C5282; font-size: 15px;">{{标题文本}}</b>
</p>
<p style="margin: 8px 0 0 0; color: #555; font-size: 14px; line-height: 1.85;">{{描述文本}}</p>
</section>
```

**关键细节：**
- 数字徽章用 `01 / 02 / 03 / 04`（前导零），不是 `1 / 2 / 3`——Georgia 衬线字体让数字有质感
- 卡片底色是 135° 渐变（左上 `#F5F8FB` → 右下 `#EAF0F7`），不是纯色
- 标题深蓝粗体单独一行，描述次级灰色（`#555` 14px）次行

**适用：** Transformer 4 创新、BERT 创新、SFT 局限性、RLHF 关键阶段、ChatGPT 创新、DeepSeek-V3 创新、NSA 三路径、两会两条等等。

---

## 6. 子标签竖条（替代 `**a. xxx：**` 这种行内加粗）

```html
<p style="margin: 22px 0 12px 0;">
<span style="display:inline-block; width:4px; height:18px; background:#2C5282; vertical-align:middle; margin-right:10px;"></span>
<b style="color:#2C5282; font-size:15.5px; vertical-align: middle;">{{a. 子标签文本}}</b>
</p>
```

**关键：** 4px 宽、18px 高的竖条，比 `█` 之类的字符精致得多。
**适用：** GPT 家族 a-d、DeepSeek-R1 a-c、GRPO a-c 等等。

---

## 7. 定义类标签条（开篇专用）

```html
<p style="margin: 14px 0; padding: 12px 16px; background: #F5F8FB; border-left: 3px solid #2C5282; line-height: 1.9; border-radius: 2px;">
<span style="display:inline-block; padding: 2px 10px; background: #2C5282; color: white; font-size: 12px; font-weight: 600; border-radius: 3px; margin-right: 10px; letter-spacing: 1px; vertical-align: 2px;">{{定 义}}</span>
<span style="color: #333; font-size: 15px;">{{完整描述}}</span>
</p>
```

**适用：** 仅用于文章**开篇第一节**的几个核心概念定义，连用 2-3 条建立设计基调。不要全文滥用，否则失去强调感。例如 LLMs 章节里「定义 / 自回归 / 文本生成」三连。

**标签文本里加空格：** `定 义` 比 `定义` 视觉效果更舒展（letter-spacing 在中文上效果有限）。

---

## 8. Callout 引用块（关键结论句）

```html
<section style="background: #F0F4F8; border-left: 3px solid #2C5282; padding: 14px 18px; margin: 22px 0; border-radius: 2px;">
<p style="margin: 0; color: #2C5282; font-size: 14px; line-height: 1.85;">{{结论或重要提示文字}}</p>
</section>
```

**适用：** 文章里有总结意味、转折意味、或独立成段的关键单句。例如：
- "Transformer 架构的引入为构建大规模高效语言模型奠定了基础。"
- "DeepSeek-V3 的价格为每百万输出标记 2.19 美元，约为 OpenAI 类似模型成本的 1/30。"
- "「ChatGPT 时刻」：ChatGPT 的推出标志着 AI 的一个关键时刻。"
- "DeepSeek-R1 的引入，使先进 LLMs 得以「普及化」。"
- "提示语没有那么复杂，直接对推理模型讲需求即可。"

**频次：** 每个一级大节 1-3 个，不要更多。

---

## 9. 加粗行内定义（中段普通段落里的 `**X：** 描述`）

```html
<p style="color: #333; font-size: 15px; line-height: 1.9;"><b style="color: #2C5282;">{{X：}}</b>{{描述}}</p>
```

**适用：** 不需要升格为「定义标签」也不需要做成卡片的小标签。例如：
- `**Transformer 架构：**` 引出说明
- `**开放权重 LLMs：**` 引出说明
- `**AI 幻觉（Hallucination）：**` 引出说明

---

## 10. 章节小标题（不带编号的子段引导句）

```html
<p style="color: #2C5282; font-size: 15px; line-height: 1.9; margin-top: 22px;"><b>{{引导短语}}</b></p>
```

**适用：** 比如「Transformer 架构的关键创新」「BERT 的关键创新」「SFT 的局限性」「DeepSeek-V3 的关键创新」「Aha Moment（顿悟时刻）」「推理模型与非推理模型」——它们后面通常紧跟着编号卡片或图片。**注意原文里这些末尾的 `：` 在升格成蓝色粗体段后可以去掉，文末加冒号视觉上很突兀。**

---

## 11. 普通段落（最常见）

```html
<p style="color: #333; font-size: 15px; line-height: 1.9;">{{段落文本}}</p>
```

注意：**所有普通段落都要带这个完整 style**——不要省略，省略了的话微信会用默认 14px 行高 1.5 的难看样式。

---

## 12. 链接

```html
<a href="{{URL}}" style="color: #2C5282; text-decoration: none;">{{链接文本}}</a>
```

长 URL（如 Google Sheets 完整链接）加 `word-break: break-all;`。

---

## 13. 图片

阶段 1（md 阶段）保留原始 `![image](url)`。阶段 2 转 HTML 时统一改为：

```html
<img src="{{URL}}" alt="image" style="max-width: 100%; display: block; margin: 14px auto; border-radius: 4px;" />
```

**不要保留 `width="1219"` 这种固定宽度**——移动端会溢出。

---

## 14. 结尾卡

```html
<section style="text-align: center; padding: 28px 20px; background: linear-gradient(135deg, #2C5282 0%, #1E3A5F 100%); border-radius: 8px; margin: 40px 0 10px 0;">
<div style="width: 30px; height: 1px; background: rgba(255,255,255,0.5); margin: 0 auto 14px;"></div>
<p style="color: rgba(255,255,255,0.9); font-size: 12px; margin: 0; letter-spacing: 4px;">END</p>
</section>
```

**和封面卡呼应**——同色渐变，但更紧凑。

---

## 反例（不要做的）

❌ 多色（橙、绿、红、黄）——只用蓝色家族
❌ 表情符号当标题装饰（🎯 ⚙️ 🚀 💰）——克制
❌ 大量 emoji 列表（✓ ✅ 📌 🔗）——可少量用作链接前缀，不要满屏
❌ 圆角太大（>12px）——文档感会塌成卡通
❌ 给每一段都加背景或边框——失去层级
❌ 改原文文字——`propability`、`Few-short`、`Zero-short` 这些笔误都要原样保留
❌ 把章节内的图片合并到一起——一个创新点对应一两张图，紧跟其后
❌ 用 `_xxx_` 斜体做强调——全部改成卡片或竖条标题

---

## 写作时的顺序检查

每次产出 `_wechat.md` 后，过一遍：

- [ ] 封面卡是否到位？英文 caption / 主标题 / 副标题 / 时间副线四件齐全？
- [ ] 每个一级大节有渐变胶囊标题？
- [ ] 每个 `1) 2) 3)` 编号项是否都用了编号卡片？没有遗留 `_xxx_` 斜体？
- [ ] 每个 `a. b. c.` 子标签是否都用了竖条样式？
- [ ] 开篇是否用了 2-3 条定义标签条建立基调？
- [ ] 全文有 5-10 处 callout 引用块，分布在关键结论处？
- [ ] 全文有没有出现 `#2C5282` `#1E3A5F` `#F0F4F8` `#F5F8FB` `#EAF0F7` `#333` `#555` `#D5DCE5` 以外的色值？有就是错的。
- [ ] 图片是否都还在原文的位置上？
- [ ] 结尾卡有 END？
