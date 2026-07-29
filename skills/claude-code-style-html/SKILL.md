---
name: claude-code-style-html
description: Generate self-contained HTML pages in the Claude Code warm paper aesthetic. Use when the user asks to create HTML, build a web page, make a report page, or produce any standalone .html artifact. Triggers on requests involving HTML generation, web page creation, or when the user says "做HTML"、"生成页面"、"做个网页".
version: 1.0.0
---

# Claude Code Style HTML

## 一、设计哲学（最重要，先理解再动手）

Claude 风格的核心不是花哨效果，而是**克制、温暖、有文档质感**的审美。三个关键词：

- **克制（Restraint）**：少即是多。不堆叠效果、不滥用颜色、不强调一切。
- **温暖（Warmth）**：用暖色调（米白、陶土橙），避免冰冷的纯白和科技蓝。给人"纸张"和"手账"的亲切感。
- **可读（Readability）**：充足留白、清晰层级、舒服的行高。页面是给人"认真读"的。

**反例（要避免）**：荧光色、渐变满屏、阴影很重、动效浮夸、信息密度爆炸、纯黑纯白对比。

## 二、配色系统（Color Tokens）

### 浅色主题（默认，首选）

```css
:root {
  /* —— 背景层 —— */
  --bg-primary:    #F7F4EE;  /* 主背景：暖米白，纸感 */
  --bg-secondary:  #FCFAF6;  /* 卡片/内容区背景 */
  --bg-tertiary:   #F0ECE3;  /* 次级区块、hover 底色 */
  --bg-code:       #F4F0E8;  /* 代码块浅色背景 */

  /* —— 主色（Anthropic 陶土橙）—— */
  --accent:        #D97757;  /* 主强调色：陶土橙/赭石色 */
  --accent-hover:  #C56646;  /* 主色 hover 加深 */
  --accent-soft:   #F5E6DF;  /* 主色的浅色调，用于背景高亮 */

  /* —— 文字层 —— */
  --text-primary:   #1F1E1C;  /* 正文主色：近黑暖调 */
  --text-secondary: #5C5A54;  /* 次要文字：暖灰 */
  --text-tertiary:  #8A8780;  /* 辅助文字/占位 */
  --text-on-accent: #FFFFFF;  /* 主色按钮上的文字 */

  /* —— 边框/分割线 —— */
  --border:        #E5E0D6;  /* 标准边框：浅暖灰 */
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

- 背景永远用暖米白，绝不用纯白 #FFFFFF 当大面积底色
- 陶土橙 --accent 是点睛色，只用在关键处：主按钮、激活态、链接、强调标签
- 正文用 --text-primary（近黑暖调），绝不用纯黑 #000
- 语义色（红绿黄）只在表达状态时用，平时不用

## 三、字体排版（Typography）

```css
:root {
  --font-serif: "Georgia", "Times New Roman", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "宋体", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "SF Mono", "JetBrains Mono", "Fira Code", "Cascadia Code", "Consolas", "Menlo", "Monaco", monospace;

  --text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem;
  --text-lg: 1.125rem; --text-xl: 1.375rem; --text-2xl: 1.75rem;
  --text-3xl: 2.25rem; --text-4xl: 3rem;

  --leading-tight: 1.25; --leading-normal: 1.6; --leading-relaxed: 1.75;
  --weight-normal: 400; --weight-medium: 500; --weight-semibold: 600; --weight-bold: 700;
  --tracking-tight: -0.02em; --tracking-normal: 0; --tracking-wide: 0.05em;
}
```

### 排版速查

| Element | Font | Size | Weight | Notes |
|---------|------|------|--------|-------|
| Page title (h1) | serif | 2.25rem | 700 | tracking-tight |
| Section heading (h2) | sans | 1.75rem | 600 | uppercase, tracking-wide, muted |
| Sub-heading (h3) | sans | 1.375rem | 600 | normal case |
| Body text (p) | serif | 1rem~1.125rem | 400 | leading-relaxed (1.75) |
| UI labels/tags | sans | 0.75rem~0.875rem | 500 | |
| Code inline | mono | 0.9em | 400 | bg --bg-code |
| Code blocks | mono | 0.875rem | 400 | bg --code-dark-bg |

## 四、间距系统（Spacing）

```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem; --space-5: 1.5rem; --space-6: 2rem;
  --space-8: 3rem; --space-10: 4rem; --space-12: 6rem;
}
```

- 宁可多留白，不要挤
- 卡片内边距至少 --space-5（24px）
- 区块之间间隔 --space-8（48px）以上

## 五、圆角与边框

```css
:root {
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px;
  --radius-xl: 16px; --radius-full: 9999px;
}
```

- 圆角适中，卡片用 8–12px
- 边框 1px solid var(--border)，很淡
- 优先用淡边框 + 极轻阴影区分层级

## 六、组件规范

### 按钮
- **主按钮**（陶土橙，一个区域只有一个）：bg accent, color on-accent, radius-md, hover accent-hover
- **次要按钮**（描边）：transparent bg, border-strong, hover border-color accent
- **幽灵按钮**：transparent, no border, hover color accent + bg tertiary

### 卡片
bg-secondary, border, radius-lg, padding space-5, shadow-sm, hover shadow-md

### 标签/徽章
inline-flex, font-sans, text-xs, weight-medium, padding 2px space-2, radius-full, bg-tertiary
语义变体：safe(success), warn(warning), danger(danger), info(info), accent

### 输入框
bg-secondary, border-strong, radius-md, focus border-color accent + box-shadow accent-soft

### 表格
collapse, text-sm; th: weight-semibold, color secondary, border-bottom 2px strong; td: border-bottom 1px; tr:hover bg-tertiary

### 代码块
行内：bg-code, radius-sm, color accent-hover, mono 0.9em
深色块：bg code-dark-bg, color code-dark-text, radius-md, mono text-sm

### 导航胶囊
flex, gap space-2; links: bg-secondary, border, radius-full, hover accent-soft

### 时间线
left border via ::before, items with accent dot, time in mono text-xs

### 标签页
tabs: border-bottom 1.5px; tab: text-sm, color secondary, active: color accent + border-bottom accent

## 七、动效原则

- 所有交互加 0.15–0.25s 过渡，ease-out 曲线
- 绝不用弹跳、旋转、闪烁
- 尊重 `prefers-reduced-motion`

## 八、布局原则

- 长文阅读页：max-width 680px，居中
- 普通页面/仪表盘：max-width 1100–1200px
- 侧栏+内容：grid, 260px + 1fr
- CSS Grid / Flexbox，不用浮动
- 移动端响应式：侧栏可收起，单列堆叠

## 九、自检清单

1. 背景用暖米白，没用纯白 #FFFFFF
2. 正文用近黑暖调 #1F1E1C，没用纯黑 #000
3. 陶土橙只用在关键强调处
4. 大标题衬线体，正文/UI无衬线体，代码等宽体
5. 行高 1.6，正文宽度不超过 ~680px
6. 留白充足，区块间距 >= 48px
7. 圆角 8–12px，边框淡，阴影极轻
8. 一个区域只有一个主按钮
9. 所有交互有 0.15–0.25s 过渡
10. 没有荧光色、重渐变、夸张动效
11. 语义化标签，有 focus 状态
12. 加了 prefers-reduced-motion
13. 单文件自包含 .html（样式内联 style）

## 十、反面模式（Anti-Patterns）

- NO pure blue (#2563eb, #0066cc) — use ochre/sienna
- NO pure white (#ffffff) background — use cream #F7F4EE
- NO pure black (#000000) text — use warm dark #1F1E1C
- NO cold gray borders (#e5e7eb) — use warm gray #E5E0D6
- NO external CDN dependencies — everything inline
- NO heavy box-shadows — subtle warm shadows only
- NO system-ui as primary font for headings — use serif
- NO linear easing — use ease-out curves
- NO fluorescent / neon colors — muted warm palette only
- NO excessive accent color usage — less is more

## 十一、工作流

1. 所有 CSS 放在 `<style>` 中，不引入外部样式表
2. 所有 JS 放在 `<script>` 中，不用 CDN
3. 用语义化 HTML：section, article, nav, header, footer
4. 复制 :root 变量到每个页面
5. 添加 @media 响应式断点
6. 添加 prefers-reduced-motion
7. 逐项对照自检清单

## Verification

生成页面后，逐项核对自检清单全部 13 条。确保是单个自包含 .html 文件。
