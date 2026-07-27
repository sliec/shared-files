---
name: claude-code-style-html
description: Generate self-contained HTML pages in the Claude Code warm paper aesthetic. Use when the user asks to create HTML, build a web page, make a report page, or produce any standalone .html artifact. Triggers on requests involving HTML generation, web page creation, or when the user says "做HTML"、"生成页面"、"做个网页"、"写个页面"、"HTML报告"、"做个报告页"、"生成网页"、"页面设计"、"暖色调页面".
version: 2.0.0
---

# Claude Code Style HTML

## 一、设计哲学（最重要，先理解再动手）

Claude 风格的核心不是某种花哨效果，而是一种**克制、温暖、有文档质感**的审美。三个关键词：

- **克制（Restraint）**：少即是多。不堆叠效果、不滥用颜色、不强调一切（强调一切等于没强调）。
- **温暖（Warmth）**：用暖色调（米白、陶土橙），避免冰冷的纯白和科技蓝。给人"纸张"和"手账"的亲切感。
- **可读（Readability）**：充足留白、清晰层级、舒服的行高。页面是给人"认真读"的，不是"快速划过"的。

**反例（要避免）**：荧光色、渐变满屏、阴影很重、动效浮夸、信息密度爆炸、纯黑纯白对比。

## 二、使用场景

- User asks to create/generate HTML
- User asks to build a web page or report page
- User asks to make a standalone .html artifact
- Any request that involves producing an .html file output

## 三、配色系统（Color Tokens）

### 浅色主题（默认，首选）

```css
:root {
  /* —— 背景层 —— */
  --bg-primary:    #F7F4EE;  /* 主背景：暖米白，纸感 */
  --bg-secondary:  #FCFAF6;  /* 卡片/内容区背景：更亮一点的米白 */
  --bg-tertiary:   #F0ECE3;  /* 次级区块、hover 底色 */
  --bg-code:       #F4F0E8;  /* 代码块浅色背景 */

  /* —— 主色（Anthropic 陶土橙）—— */
  --accent:        #D97757;  /* 主强调色：陶土橙/赭石色 */
  --accent-hover:  #C56646;  /* 主色 hover 加深 */
  --accent-soft:   #F5E6DF;  /* 主色的浅色调，用于背景高亮 */

  /* —— 文字层 —— */
  --text-primary:   #1F1E1C;  /* 正文主色：近黑暖调，不用纯黑 #000 */
  --text-secondary: #5C5A54;  /* 次要文字：暖灰 */
  --text-tertiary:  #8A8780;  /* 辅助文字/占位：浅暖灰 */
  --text-on-accent: #FFFFFF;  /* 主色按钮上的文字 */

  /* —— 边框/分割线 —— */
  --border:        #E5E0D6;  /* 标准边框：浅暖灰，很淡 */
  --border-strong: #D6D0C4;  /* 稍重的边框 */

  /* —— 语义色（克制使用）—— */
  --success: #5B8C5A;  --success-bg: #F2F7EF;
  --warning: #C99A3F;  --warning-bg: #FBF5E8;
  --danger:  #BC4B4B;  --danger-bg:  #FDF0ED;
  --info:    #5A7D9A;  --info-bg:    #F0F3F5;

  /* —— 代码块深色背景 —— */
  --code-dark-bg:   #2C2523;
  --code-dark-text: #D8D0C8;

  /* —— 阴影（极轻）—— */
  --shadow-sm: 0 1px 2px rgba(31, 30, 28, 0.04);
  --shadow-md: 0 2px 8px rgba(31, 30, 28, 0.06);
  --shadow-lg: 0 8px 24px rgba(31, 30, 28, 0.08);

  /* —— 动效 —— */
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast:   0.15s;
  --duration-normal: 0.25s;
  --duration-slow:   0.4s;
}
```

### 深色主题（可选）

```css
:root[data-theme="dark"] {
  --bg-primary:    #1F1E1C;
  --bg-secondary:  #262521;
  --bg-tertiary:   #2F2E29;
  --bg-code:       #2A2925;

  --accent:        #E08A6A;
  --accent-hover:  #EB9B7D;
  --accent-soft:   #3A2E28;

  --text-primary:   #EDEAE3;
  --text-secondary: #B0ADA5;
  --text-tertiary:  #807D76;
  --text-on-accent: #1F1E1C;

  --border:        #3A3833;
  --border-strong: #4A4842;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);
}
```

### 配色使用原则

- 背景永远用暖米白，绝不用纯白 #FFFFFF 当大面积底色。
- 陶土橙 --accent 是点睛色，只用在关键处：主按钮、激活态、链接、强调标签。一个页面里它出现得越少越高级。
- 正文用 --text-primary（近黑暖调），绝不用纯黑 #000。
- 语义色（红绿黄）只在表达状态时用，平时不用。

## 四、字体排版（Typography）

### 字体栈

```css
:root {
  /* 衬线体：大标题，增加文档/编辑质感 */
  --font-serif: "Georgia", "Times New Roman", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "宋体", serif;

  /* 无衬线体：正文、UI、按钮 */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI",
               "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
               "Helvetica Neue", Helvetica, Arial, sans-serif;

  /* 等宽体：代码、命令、数据 */
  --font-mono: "SF Mono", "JetBrains Mono", "Fira Code", "Cascadia Code",
               "Consolas", "Menlo", "Monaco", monospace;
}
```

经典搭配：大标题用衬线体（serif），营造文档/书卷气；正文与 UI 用无衬线体（sans），干净易读；代码用等宽体（mono）。

### 字号与层级（Type Scale）

```css
:root {
  --text-xs:   0.75rem;   /* 12px - 标签、脚注 */
  --text-sm:   0.875rem;  /* 14px - 辅助文字、说明 */
  --text-base: 1rem;      /* 16px - 正文基准 */
  --text-lg:   1.125rem;  /* 18px - 大正文/小标题 */
  --text-xl:   1.375rem;  /* 22px - h3 */
  --text-2xl:  1.75rem;   /* 28px - h2 */
  --text-3xl:  2.25rem;   /* 36px - h1 */
  --text-4xl:  3rem;      /* 48px - 页面主标题 */

  --leading-tight:   1.25;
  --leading-normal:  1.6;
  --leading-relaxed: 1.75;

  --weight-normal:   400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;

  --tracking-tight:  -0.02em;
  --tracking-normal: 0;
  --tracking-wide:   0.05em;
}
```

### 排版速查表

| Element | Font | Size | Weight | Notes |
|---------|------|------|--------|-------|
| Page title (h1) | --font-serif | --text-3xl | 700 | --tracking-tight, 可用 italic accent 强调 |
| Section heading (h2) | --font-sans | --text-2xl | 600 | Uppercase, --tracking-wide, muted color |
| Sub-heading (h3) | --font-sans | --text-xl | 600 | Normal case |
| Body text (p) | --font-serif | --text-base~--text-lg | 400 | --leading-relaxed (1.75) |
| UI labels/tags | --font-sans | --text-xs~--text-sm | 500 | |
| Code inline | --font-mono | 0.9em | 400 | Background --bg-code |
| Code blocks (pre) | --font-mono | --text-sm | 400 | Background --code-dark-bg, --leading-normal |

### 排版使用原则

- 标题用衬线 + --tracking-tight，正文用无衬线 + --leading-normal（1.6）。
- 正文最大宽度控制在 65-75 字符（约 680px），太宽不好读。
- 段落之间留足空隙（margin-bottom: 1.2em）。
- 全大写的小标签用 letter-spacing: 0.05em + font-size: var(--text-xs) + color: var(--text-tertiary)。

## 五、间距系统（Spacing）

采用 4px 基准的间距尺度：

```css
:root {
  --space-1:  0.25rem;  /* 4px */
  --space-2:  0.5rem;   /* 8px */
  --space-3:  0.75rem;  /* 12px */
  --space-4:  1rem;     /* 16px */
  --space-5:  1.5rem;   /* 24px */
  --space-6:  2rem;     /* 32px */
  --space-8:  3rem;     /* 48px */
  --space-10: 4rem;     /* 64px */
  --space-12: 6rem;     /* 96px */
}
```

### 间距原则

- 宁可多留白，不要挤。Claude 风格的"高级感"很大程度来自充足的呼吸感。
- 卡片内边距至少 --space-5（24px）。
- 区块之间间隔 --space-8（48px）以上。
- 相关元素靠近，不相关元素拉开（亲密性原则）。

## 六、圆角与边框（Radius & Border）

```css
:root {
  --radius-sm:   4px;     /* 标签、小按钮 */
  --radius-md:   8px;     /* 按钮、输入框 */
  --radius-lg:   12px;    /* 卡片 */
  --radius-xl:   16px;    /* 大容器 */
  --radius-full: 9999px;  /* 圆形/胶囊 */
}
```

### 原则

- 圆角适中，不要太圆（过于活泼）也不要直角（过于硬）。卡片用 8-12px 最稳。
- 边框用 1px solid var(--border)，很淡很淡，起分隔作用而非装饰。
- 优先用「淡边框 + 极轻阴影」来区分层级，而不是用重阴影。

## 七、组件规范（Components）

### 1. 按钮（Button）

```css
/* 主按钮 — 一个区域只有一个 */
.btn-primary {
  background: var(--accent);
  color: var(--text-on-accent);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  padding: var(--space-2) var(--space-4);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--duration-fast) var(--ease-out);
}
.btn-primary:hover { background: var(--accent-hover); }

/* 次要按钮（描边） */
.btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-4);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.btn-secondary:hover {
  background: var(--bg-tertiary);
  border-color: var(--accent);
}

/* 幽灵按钮（纯文字） */
.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  border: none;
  padding: var(--space-2) var(--space-3);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.btn-ghost:hover { color: var(--accent); background: var(--bg-tertiary); }
```

### 2. 卡片（Card）

```css
.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--duration-normal) var(--ease-out),
              border-color var(--duration-normal) var(--ease-out);
}
.card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--border-strong);
}
```

### 3. 标签/徽章（Tag / Badge）

```css
.tag {
  display: inline-flex;
  align-items: center;
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}
/* 语义变体 */
.tag-safe   { background: var(--success-bg); color: var(--success); }
.tag-warn   { background: var(--warning-bg); color: var(--warning); }
.tag-danger { background: var(--danger-bg);  color: var(--danger); }
.tag-info   { background: var(--info-bg);    color: var(--info); }
.tag-accent { background: var(--accent-soft); color: var(--accent-hover); }
```

### 4. 输入框（Input）

```css
.input {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--text-primary);
  background: var(--bg-secondary);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-3);
  transition: border-color var(--duration-fast) var(--ease-out),
              box-shadow var(--duration-fast) var(--ease-out);
}
.input::placeholder { color: var(--text-tertiary); }
.input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-soft);
}
```

### 5. 代码块（Code Block）

浅色行内代码 + 深色代码块两种风格：

```css
/* 行内代码 */
code:not(pre code) {
  background: var(--bg-code);
  border-radius: var(--radius-sm);
  padding: 1px 6px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--accent-hover);
}

/* 深色代码块 */
pre {
  background: var(--code-dark-bg);
  color: var(--code-dark-text);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(40, 30, 20, 0.08);
}
```

#### 语法高亮色表（Syntax Highlighting Tokens）

| Token | Class | Color | 用途 |
|-------|-------|-------|------|
| 注释 | .comment | #7A9A6A | // ..., /* ... */ |
| 关键字 | .keyword | #D4956A | const, let, return, export |
| 字符串 | .string | #C9A87C | "text", 'text' |
| 函数名 | .fn | #E0C49A | functionName() |
| 类型 | .type | #8BB8A0 | TypeName, Interface |
| Diff 添加 | .diff-add | #7AA06A | + added line |
| Diff 删除 | .diff-del | #C07060 | - removed line |

用法示例：

```html
<span class="comment">// comment</span>
<span class="keyword">const</span>
<span class="string">"text"</span>
<span class="fn">functionName</span>
<span class="type">TypeName</span>
<span class="diff-add">+ added</span>
<span class="diff-del">- removed</span>
```

### 6. 表格（Table）

```css
table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}
th {
  text-align: left;
  font-weight: var(--weight-semibold);
  color: var(--text-secondary);
  padding: var(--space-3) var(--space-4);
  border-bottom: 2px solid var(--border-strong);
}
td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--border);
  color: var(--text-primary);
}
tr:hover td { background: var(--bg-tertiary); }
```

### 7. 引用块（Blockquote）

```css
blockquote {
  border-left: 3px solid var(--accent);
  background: var(--accent-soft);
  padding: var(--space-3) var(--space-5);
  margin: var(--space-5) 0;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  color: var(--text-secondary);
  font-style: italic;
}
```

### 8. 导航胶囊（Navigation Pills）

```css
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin: var(--space-6) 0;
}
.nav a {
  font-family: var(--font-sans);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  padding: var(--space-1) var(--space-4);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--duration-normal) var(--ease-out);
}
.nav a:hover {
  border-color: var(--accent-soft);
  color: var(--accent);
  background: var(--accent-soft);
}
```

### 9. Pro/Con 对比网格

```css
.pro-con {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin: var(--space-4) 0;
}
.pro-con > div {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
}
@media (max-width: 600px) { .pro-con { grid-template-columns: 1fr; } }
```

### 10. 推荐框（Recommendation Box）

```css
.recommendation {
  background: var(--accent-soft);
  border: 1px solid #E8D0C4;
  padding: var(--space-5);
  border-radius: var(--radius-lg);
  margin-top: var(--space-6);
}
```

### 11. 时间线（Timeline）

```css
.timeline {
  position: relative;
  margin: var(--space-5) 0;
  padding-left: 2.2rem;
}
.timeline::before {
  content: '';
  position: absolute;
  left: 7px; top: 0; bottom: 0;
  width: 1.5px;
  background: var(--border);
}
.timeline-item {
  position: relative;
  margin-bottom: var(--space-5);
}
.timeline-item::before {
  content: '';
  position: absolute;
  left: -1.85rem; top: 7px;
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--accent);
  border: 2.5px solid var(--bg-primary);
}
.timeline-item .time {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}
```

### 12. 折叠面板（Collapsible / details）

```css
details {
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-5);
  margin: var(--space-3) 0;
  background: var(--bg-secondary);
}
details summary {
  cursor: pointer;
  font-family: var(--font-sans);
  font-weight: var(--weight-semibold);
  font-size: var(--text-base);
}
details[open] summary {
  margin-bottom: var(--space-3);
  border-bottom: 1px solid var(--border);
  padding-bottom: var(--space-2);
}
```

### 13. 标签页（Tabs）

```css
.tabs {
  display: flex;
  border-bottom: 1.5px solid var(--border);
  margin-top: var(--space-5);
}
.tab {
  font-family: var(--font-sans);
  padding: var(--space-2) var(--space-5);
  cursor: pointer;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  border-bottom: 2px solid transparent;
  margin-bottom: -1.5px;
  transition: all var(--duration-normal) var(--ease-out);
}
.tab:hover { color: var(--text-primary); }
.tab.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
  font-weight: var(--weight-semibold);
}
.tab-content { display: none; padding: var(--space-5) 0; }
.tab-content.active { display: block; }
```

### 14. 指标标签（Metrics / Indicator Tags）

用于展示关键数据指标，如 KPI、统计数字等：

```css
.metrics {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}
.metric {
  background: var(--bg-tertiary);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-sm);
}
.metric strong { color: var(--text-primary); }
```

HTML 用法示例：

```html
<div class="metrics">
  <span class="metric"><strong>98.5%</strong> 可用率</span>
  <span class="metric"><strong>42ms</strong> 响应时间</span>
  <span class="metric"><strong>1.2k</strong> 请求/秒</span>
</div>
```

### 15. 柱状图（Bar Chart）

纯 CSS 实现的简洁柱状图，无需 JavaScript 库：

```css
.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: var(--space-2);
  height: 150px;
  margin: var(--space-4) 0;
}
.bar {
  flex: 1;
  background: var(--accent);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  position: relative;
  transition: opacity var(--duration-normal) var(--ease-out);
  min-width: 28px;
  opacity: 0.85;
}
.bar:hover { opacity: 1; }
.bar-label {
  position: absolute;
  bottom: -1.7rem;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  white-space: nowrap;
}
.bar-value {
  position: absolute;
  top: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}
```

HTML 用法示例：

```html
<div class="bar-chart">
  <div class="bar" style="height: 60%;">
    <span class="bar-value">60</span>
    <span class="bar-label">Q1</span>
  </div>
  <div class="bar" style="height: 85%;">
    <span class="bar-value">85</span>
    <span class="bar-label">Q2</span>
  </div>
  <div class="bar" style="height: 45%;">
    <span class="bar-value">45</span>
    <span class="bar-label">Q3</span>
  </div>
  <div class="bar" style="height: 92%;">
    <span class="bar-value">92</span>
    <span class="bar-label">Q4</span>
  </div>
</div>
```

### 16. 文件头（File Header）

用于代码块顶部的文件名/路径展示，搭配深色代码块使用：

```css
.file-header {
  font-family: var(--font-sans);
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  padding: var(--space-2) var(--space-4);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--text-sm);
}
```

HTML 用法示例（搭配代码块）：

```html
<div class="file-header">
  <span>src/utils/helpers.ts</span>
  <span style="color: var(--text-tertiary); font-size: var(--text-xs);">TypeScript</span>
</div>
<pre style="border-radius: 0 0 var(--radius-md) var(--radius-md); margin-top: 0;">
<code>// code here...</code>
</pre>
```

### 17. 注释/警告块（Comment Block）

用于页面中的提示、注意事项、警告信息：

```css
.comment-block {
  background: var(--warning-bg);
  border-left: 3px solid var(--warning);
  padding: var(--space-3) var(--space-4);
  margin: var(--space-3) 0;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  font-size: var(--text-sm);
  color: #5C4830;
}
```

语义变体（按需使用）：

```css
/* 危险变体 */
.comment-block-danger {
  background: var(--danger-bg);
  border-left: 3px solid var(--danger);
  color: #6B3030;
}
/* 信息变体 */
.comment-block-info {
  background: var(--info-bg);
  border-left: 3px solid var(--info);
  color: #3A5060;
}
/* 成功变体 */
.comment-block-success {
  background: var(--success-bg);
  border-left: 3px solid var(--success);
  color: #3A5A38;
}
```

HTML 用法示例：

```html
<div class="comment-block">
  <strong>注意：</strong>此配置项在生产环境中需要额外的安全审计。
</div>
```

### 18. TL;DR 摘要框

用于长页面顶部的快速摘要，让读者一眼抓住要点：

```css
.tldr {
  background: var(--success-bg);
  border: 1px solid #D4E4CC;
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
}
.tldr strong {
  font-family: var(--font-sans);
  color: var(--success);
}
```

HTML 用法示例：

```html
<div class="tldr">
  <strong>TL;DR</strong> — 本报告核心结论：市场增速放缓但结构性机会仍在，
  建议关注具备技术壁垒的细分龙头。
</div>
```

## 八、动效（Motion）

原则：动效是为了"顺滑"，不是为了"炫"。

- 所有交互（hover、focus、展开）加 0.15-0.25s 的过渡。
- 用 ease-out 类曲线，避免线性（linear）的机械感。
- **绝不**用弹跳、旋转、闪烁等夸张动效。
- 尊重用户偏好：

```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

## 九、布局原则（Layout）

- **长文阅读页**：内容区最大宽度 680px，居中。
- **普通页面/仪表盘**：最大宽度 1100-1200px，居中。
- **侧栏 + 内容**布局：侧栏 240-280px，内容区自适应。
- 用 CSS Grid / Flexbox，不用浮动。
- 大量留白，区块之间至少 --space-8（48px）间隔。
- 移动端响应式：侧栏可收起，内容单列堆叠。

```css
/* 单列阅读布局 */
.container { max-width: 1100px; margin: 0 auto; padding: var(--space-8) var(--space-6); }

/* 侧栏 + 内容布局 */
.layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
}
@media (max-width: 768px) {
  .layout { grid-template-columns: 1fr; }
}

/* 卡片网格 */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-4);
}
```

## 十、可访问性（Accessibility）

- 正文与背景对比度 >= 4.5:1（近黑暖调文字 + 米白底已满足）。
- 所有可交互元素有清晰的 :focus 状态（用 --accent-soft 描边）。
- 图片有 alt，图标按钮有 aria-label。
- 用语义化标签：`<header>` `<nav>` `<main>` `<section>` `<article>` `<footer>`。
- 字号最小 12px，正文 16px。

## 十一、工作流（Workflow）

1. **Start with the template**: Read template.html for the full base structure
2. **Keep all CSS in `<style>`**: No external stylesheets
3. **Keep all JS in `<script>`**: No external scripts, no CDN
4. **Use semantic HTML**: `<section>`, `<article>`, `<nav>`, `<header>`, `<footer>`
5. **Apply the design tokens**: Copy the :root variables into every page
6. **Responsive**: Add @media (max-width: 768px) and @media (max-width: 600px) breakpoints
7. **Add prefers-reduced-motion** media query
8. **Self-check** against the checklist below before delivering

## 十二、自检清单（Checklist）

生成页面后，逐项核对：

1. 背景用了暖米白，没用纯白 #FFFFFF 大面积铺底
2. 正文用近黑暖调 #1F1E1C，没用纯黑 #000
3. 陶土橙只用在关键强调处，没有滥用
4. 大标题用衬线体，正文/UI用无衬线体，代码用等宽体
5. 行高 1.6 左右，正文宽度不超过 ~680px
6. 留白充足，区块间距 >= 48px
7. 圆角 8-12px，边框很淡，阴影极轻
8. 一个区域只有一个主按钮（陶土橙）
9. 所有交互有 0.15-0.25s 过渡，曲线非线性
10. 没有荧光色、重渐变、夸张动效
11. 用了语义化标签，有 focus 状态
12. 加了 prefers-reduced-motion 处理
13. 是单个自包含 .html 文件（样式内联在 `<style>` 里）

## 十三、反面模式（Anti-Patterns）

- NO pure blue (#2563eb, #0066cc) — use ochre/sienna instead
- NO pure white (#ffffff) background — use cream #F7F4EE
- NO pure black (#000000) text — use warm dark #1F1E1C
- NO cold gray borders (#e5e7eb) — use warm gray #E5E0D6
- NO external CDN dependencies — everything inline
- NO heavy box-shadows — subtle warm shadows only
- NO system-ui as primary font for headings — use serif
- NO linear easing — use ease-out curves
- NO fluorescent / neon colors — muted warm palette only
- NO excessive accent color usage — less is more

## 十四、一句话 Prompt 模板

> "请严格遵循我提供的『Claude 风格 HTML 设计规范』生成一个单文件、自包含的 HTML 页面。要求：暖米白纸感背景、陶土橙只点睛、衬线标题+无衬线正文、充足留白、淡边框轻阴影、所有交互带缓动过渡。"

## Verification

生成页面后，逐项核对自检清单全部 13 条。确保是单个自包含 .html 文件。
