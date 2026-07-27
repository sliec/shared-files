# shared-files

🧩 **7 个 QoderWork Agent Skills，开箱即用**

一套经过实战验证的 Agent 技能包，覆盖 HTML 页面生成、问题定义与目标拆解、课题研究、基金业绩归因、C 盘清理等场景。直接复制到本地 skills 目录即可使用。

---

## 这是什么？

一组可以直接装到 QoderWork / QoderCLI 的 **Agent Skills**。装了之后，你跟 Agent 说"帮我做个网页"或者"帮我定义这个问题"，它就能按照专业流程出活儿。

> 一句话：**把好用的 Skills 开源，让每个人都能受益。**

| | 说明 |
|---|---|
| 适用平台 | QoderWork / QoderCLI / 任何支持 SKILL.md 的 Agent |
| 技能数量 | **7 个**，覆盖开发、分析、学习、运维场景 |
| 使用方式 | 下载文件放入本地 skills 目录，即刻生效 |

---

## ⚡ 快速安装

### 方式一：单文件下载（推荐）

```bash
# 下载单个 Skill（以 claude-code-style-html 为例）
mkdir -p ~/.qoderwork/skills/claude-code-style-html
curl -o ~/.qoderwork/skills/claude-code-style-html/SKILL.md \
  https://raw.githubusercontent.com/sliec/shared-files/main/skills/claude-code-style-html/SKILL.md

# 下载带附属文件的 Skill（以 problem-goal-defined 为例，含 2 个 reference 文件）
mkdir -p ~/.qoderwork/skills/problem-goal-defined
curl -o ~/.qoderwork/skills/problem-goal-defined/SKILL.md \
  https://raw.githubusercontent.com/sliec/shared-files/main/skills/problem-goal-defined/SKILL.md
curl -o ~/.qoderwork/skills/problem-goal-defined/reference-problem.md \
  https://raw.githubusercontent.com/sliec/shared-files/main/skills/problem-goal-defined/reference-problem.md
curl -o ~/.qoderwork/skills/problem-goal-defined/reference-goal.md \
  https://raw.githubusercontent.com/sliec/shared-files/main/skills/problem-goal-defined/reference-goal.md
```

### 方式二：整个仓库克隆

```bash
git clone https://github.com/sliec/shared-files.git
cp -r shared-files/skills/* ~/.qoderwork/skills/
```

### 方式三：PowerShell（Windows）

```powershell
# 以 claude-code-style-html 为例
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.qoderwork\skills\claude-code-style-html"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sliec/shared-files/main/skills/claude-code-style-html/SKILL.md" `
  -OutFile "$env:USERPROFILE\.qoderwork\skills\claude-code-style-html\SKILL.md"
```

---

## 🧰 7 个 Skills 全览

### 开发与设计

| 技能 | 版本 | 干什么 | 触发词 |
|---|---|---|---|
| [`claude-code-style-html`](skills/claude-code-style-html/) | v2.0.0 | 生成暖色纸质风格的自包含 HTML 页面，含完整设计系统（配色/字体/组件/动效） | "做HTML"、"生成页面"、"做个网页"、"写个页面" |
| [`c-drive-cleanup`](skills/c-drive-cleanup/) | v1.0.0 | Windows C 盘空间扫描与智能清理，自动识别可安全删除的缓存和临时文件 | "C盘清理"、"空间不足"、"磁盘清理" |

### 思维与学习

| 技能 | 版本 | 干什么 | 触发词 |
|---|---|---|---|
| [`problem-goal-defined`](skills/problem-goal-defined/) | v1.0.0 | 将模糊问题精确定义为结构化议题，将宏观目标拆解为可执行路线图。运用 5W2H、5Whys、WBS、OKR、SMART 等框架 | "帮我定义问题"、"目标拆解"、"根因分析"、"制定计划" |
| [`topic-question-generator`](skills/topic-question-generator/) | v5.0.0 | 课题研究的问题引擎——系统性生成循序渐进的探究问题清单，帮你想透"该问什么" | "帮我分析这个课题"、"帮我提一些问题" |

### 金融分析

| 技能 | 版本 | 干什么 | 触发词 |
|---|---|---|---|
| [`equity-fund-attribution`](skills/equity-fund-attribution/) | v1.0.0 | 权益类基金业绩归因全流程：净值法（T-M/H-M/C-L）、持仓法（Brinson/Barra）、风险归因 | "基金归因"、"业绩归因"、"Brinson" |
| [`fof-performance-attribution`](skills/fof-performance-attribution/) | v1.0.0 | FOF 基金业绩归因与绩效分析：Brinson 归因、多因子回归、择时检验，含 Python CLI 工具 | "FOF归因"、"选基能力"、"FOF分析" |

---

## 📖 各 Skill 详解

### claude-code-style-html — 暖色纸质风格 HTML 生成

**版本 2.0.0** | 文件：`SKILL.md` + `template.html`

一套完整的 HTML 页面设计系统，核心审美是**克制、温暖、有文档质感**：

- **配色**：暖米白底 `#F7F4EE` + 陶土橙点睛 `#D97757`，不用纯白纯黑
- **字体**：衬线标题 + 无衬线正文 + 等宽代码，营造书卷气
- **18 种组件**：按钮、卡片、标签、输入框、代码块、表格、引用块、导航胶囊、时间线、标签页、柱状图、TL;DR 框等
- **自检清单**：生成页面后逐项核对，确保风格一致

**适用场景**：让 Agent 生成任何 HTML 页面时，自动应用统一的高级感设计。

```
你：帮我做一个项目汇报页面
你：生成一份数据分析的 HTML 报告
你：做个网页展示我的作品集
```

---

### problem-goal-defined — 问题定义与目标拆解

**版本 1.0.0** | 文件：`SKILL.md` + `reference-problem.md` + `reference-goal.md`

覆盖从"定义问题"到"拆解目标"的完整思维链：

**问题定义（5 步）**：5W2H 澄清 → 5 Whys 追根因 → 边界分析 → 问题重构 → 假设检验

**目标拆解（8 步）**：SMART 锚定 → 逆向推导 → 拆解维度 → WBS 构建 → 优先级排序 → 依赖识别 → 里程碑 → 风险预案

**方法论来源**：管理学（5W2H/5Whys）、系统工程（边界分析）、认知心理学（框架效应/确认偏误）、设计思维（共情/HMW）、六西格玛（SIPOC/鱼骨图）、项目管理（WBS/SMART/CPM/PERT）、战略管理（OKR/BSC）、敏捷方法论

```
你：帮我定义一下"面试官标准不统一"这个问题
你：帮我拆解"提升团队交付效率"这个目标
你：分析一下这个问题出在哪
```

---

### topic-question-generator — 课题研究问题引擎

**版本 5.0.0** | 文件：`SKILL.md`

一个"问题引擎"而非"答案引擎"。面对任何课题，系统性生成循序渐进的探究问题清单：

- 7 步工作流：素材问询 → 课题分类 → 认知诊断 → 双视角生成 → 课程式编排 → 交互共创 → 结构化回答
- 8 种通用提问范式 + 领域专属问题模式
- 6 阶段渐进学习路径

```
你：帮我分析一下"大模型在金融领域的应用"这个课题
你：关于量化投资，我应该了解什么？
```

---

### equity-fund-attribution — 权益基金业绩归因

**版本 1.0.0** | 文件：`SKILL.md`

三条归因路径全覆盖：

| 路径 | 方法 |
|---|---|
| 净值法 | T-M / H-M / C-L 择时选股、Fama-French 三/四/五因子、Carhart 模型 |
| 持仓法 | Brinson 行业配置/选股、CT&CS 风格归因、Barra 多因子风险模型 |
| 风险归因 | x-sigma-rho 分解 |

基金经理能力圈六模块分析：投资方法、资产配置、风格、行业、选股、交易。

---

### fof-performance-attribution — FOF 基金业绩归因

**版本 1.0.0** | 文件：`SKILL.md` + `references/` + `scripts/`

三种工作模式：

1. **分析计算**：输入净值/持仓数据 → Brinson 归因 + 多因子回归 + T-M/H-M 择时检验
2. **报告撰写**：按券商/FOF 管理人专业体例输出归因报告
3. **投资决策**：评估基金经理选基与择时能力

附带 Python CLI 工具（`fof_attribution.py`），支持 Carino 多期链接、滚动 Alpha 等高级功能。

---

### c-drive-cleanup — Windows C 盘清理

**版本 1.0.0** | 文件：`SKILL.md`

6 步工作流：扫描目录 → 递归深入 → 定位大文件 → 生成报告 → 确认后执行 → 汇报结果

自动识别可安全清理的项目：pip/npm 缓存、浏览器缓存、VS Code 扩展缓存等。执行前必须用户确认。

---

## 🗂️ 项目结构

```
shared-files/
├── README.md
├── skills/
│   ├── claude-code-style-html/     # 暖色 HTML 设计系统
│   │   ├── SKILL.md
│   │   └── template.html
│   ├── problem-goal-defined/       # 问题定义与目标拆解
│   │   ├── SKILL.md
│   │   ├── reference-problem.md
│   │   └── reference-goal.md
│   ├── topic-question-generator/   # 课题研究问题引擎
│   │   └── SKILL.md
│   ├── c-drive-cleanup/            # Windows C 盘清理
│   │   └── SKILL.md
│   ├── equity-fund-attribution/    # 权益基金业绩归因
│   │   └── SKILL.md
│   └── fof-performance-attribution/# FOF 业绩归因
│       ├── SKILL.md
│       ├── references/
│       │   ├── methodology.md
│       │   └── report-template.md
│       └── scripts/
│           └── fof_attribution.py
```

---

## 🤝 贡献

欢迎 Fork 并提交 PR，分享你自己的 Skills。

提交新 Skill 时请确保：

- `SKILL.md` 包含完整的 frontmatter（name / description / version）
- 不包含个人信息（API Key、本地路径等）
- 描述清晰说明"什么时候触发"和"做什么"

---

## 📜 License

[MIT License](./LICENSE)

---

<p align="center">
  Made with 🤖 for QoderWork<br>
  <sub>好用的 Skills，值得被更多人使用</sub>
</p>
