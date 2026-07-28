# shared-files

🧩 **Skills 同步中心 — 16 个 Agent Skills，换电脑换平台一键拉齐**

个人的 Agent Skills 集中管理仓库。无论在哪个 Agent 平台、哪台电脑上工作，一行命令就能把所有 Skills 同步到本地。收录原创 Skills 和社区精选，覆盖产品管理、金融分析、思维学习、开发运维等场景。

---

## 这是什么？

一个 **Skills 同步中心**。当你需要在多个 Agent 平台（QoderWork、QoderCLI 等）和不同电脑间切换时，不用再逐个手动搭建 Skills——克隆这个仓库，一行命令全部就位。

> 一句话：**一次整理，到处可用。**

| | 说明 |
|---|---|
| 适用平台 | QoderWork / QoderCLI / 任何支持 SKILL.md 的 Agent |
| 技能数量 | **17 个**（10 原创 + 7 社区精选），覆盖产品、分析、学习、开发场景 |
| 使用方式 | 克隆后一行命令同步到本地 skills 目录 |

---

## ⚡ 一键同步

### 全量同步（推荐，换电脑时用）

```bash
# macOS / Linux
git clone https://github.com/sliec/shared-files.git
cp -r shared-files/skills/* ~/.qoderwork/skills/

# Windows PowerShell
git clone https://github.com/sliec/shared-files.git
Copy-Item -Recurse -Force shared-files\skills\* "$env:USERPROFILE\.qoderwork\skills\"
```

### 按需下载单个 Skill

```bash
# macOS / Linux（以 claude-code-style-html 为例）
mkdir -p ~/.qoderwork/skills/claude-code-style-html
curl -o ~/.qoderwork/skills/claude-code-style-html/SKILL.md \
  https://raw.githubusercontent.com/sliec/shared-files/main/skills/claude-code-style-html/SKILL.md

# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.qoderwork\skills\claude-code-style-html"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sliec/shared-files/main/skills/claude-code-style-html/SKILL.md" `
  -OutFile "$env:USERPROFILE\.qoderwork\skills\claude-code-style-html\SKILL.md"
```

---

## 🧰 17 个 Skills 全览

### 产品管理

| 技能 | 来源 | 干什么 | 触发词 |
|---|---|---|---|
| [`prd-doc-writer`](skills/prd-doc-writer/) | [云舒](https://github.com/yunshu0909/yunshu_skillshub) | PRD 产品需求文档撰写，含标准模板和 Mermaid 流程图 | "写PRD"、"产品需求文档" |
| [`prd-test-writer`](skills/prd-test-writer/) | [云舒](https://github.com/yunshu0909/yunshu_skillshub) | PRD 测试用例生成 + 对抗性评审，输出 HTML 评审报告 | "PRD测试"、"测试用例"、"PRD评审" |
| [`prd-auto-test-loop`](skills/prd-auto-test-loop/) | [云舒](https://github.com/yunshu0909/yunshu_skillshub) | PRD 自动化测试闭环 | "自动化测试"、"测试闭环" |

### 开发与设计

| 技能 | 来源 | 干什么 | 触发词 |
|---|---|---|---|
| [`claude-code-style-html`](skills/claude-code-style-html/) | 原创 | 生成暖色纸质风格的自包含 HTML 页面，含 18 种组件 + 设计系统 | "做HTML"、"生成页面"、"写个页面" |
| [`git-push`](skills/git-push/) | [云舒](https://github.com/yunshu0909/yunshu_skillshub) | Git 推送助手 | "git push"、"推送代码" |
| [`github-repo-search`](skills/github-repo-search/) | [云舒](https://github.com/yunshu0909/yunshu_skillshub) | GitHub 仓库搜索 | "搜GitHub"、"找仓库" |

### 思维与学习

| 技能 | 来源 | 干什么 | 触发词 |
|---|---|---|---|
| [`problem-goal-defined`](skills/problem-goal-defined/) | 原创 | 将模糊问题精确定义为结构化议题，将宏观目标拆解为可执行路线图 | "帮我定义问题"、"目标拆解"、"根因分析" |
| [`topic-question-generator`](skills/topic-question-generator/) | 原创 | 课题研究的问题引擎——系统性生成循序渐进的探究问题清单 | "帮我分析这个课题"、"帮我提一些问题" |
| [`multi-perspective-analysis`](skills/multi-perspective-analysis/) | [云舒](https://github.com/yunshu0909/yunshu_skillshub) | 多视角分析：内置 10 位大佬思维模型（张小龙/张一鸣/任正非/Munger/Musk/Bezos 等） | "多视角分析"、"换个角度想" |
| [`readable-output`](skills/readable-output/) | [云舒](https://github.com/yunshu0909/yunshu_skillshub) | 可读性输出优化，让 Agent 产出更易读 | "优化输出"、"可读性" |

### 金融分析

| 技能 | 来源 | 干什么 | 触发词 |
|---|---|---|---|
| [`equity-fund-attribution`](skills/equity-fund-attribution/) | 原创 | 权益类基金业绩归因全流程：净值法、持仓法、风险归因 | "基金归因"、"业绩归因"、"Brinson" |
| [`fof-performance-attribution`](skills/fof-performance-attribution/) | 原创 | FOF 基金业绩归因与绩效分析，含 Python CLI 工具 | "FOF归因"、"选基能力"、"FOF分析" |

### 存储清理

| 技能 | 来源 | 干什么 | 触发词 |
|---|---|---|---|
| [`storage-analyzer`](skills/storage-analyzer/) | [卡兹克](https://github.com/KKKKhazix/khazix-skills) | macOS/Windows 存储分析：三级分类 + 交互式 HTML 报告 + 本地服务一键清理 | "存储分析"、"磁盘满了"、"清理空间" |
| [`c-drive-cleanup`](skills/c-drive-cleanup/) | 原创 | Windows C 盘空间扫描与智能清理（轻量版） | "C盘清理"、"空间不足" |

### 深度研究与 Agent 协作

| 技能 | 来源 | 干什么 | 触发词 |
|---|---|---|---|
| [`hv-analysis`](skills/hv-analysis/) | [卡兹克](https://github.com/KKKKhazix/khazix-skills) | 横纵分析法深度研究：纵轴发展历程 + 横轴竞品对比 → PDF 报告 | "横纵分析"、"深度研究"、"帮我分析" |
| [`leader`](skills/leader/) | [卡兹克](https://github.com/KKKKhazix/khazix-skills) | 把一句话想法拆成 AI Agent 能独立跑完的目标任务书 | "帮我给 agent 写个目标"、"写个任务书" |

---

## 📖 各 Skill 详解

### prd-doc-writer — PRD 产品需求文档撰写

**作者**：[云舒](https://github.com/yunshu0909/yunshu_skillshub) | 文件：`SKILL.md` + `assets/` + `references/`

按产品经理标准体例撰写 PRD，包含需求背景、用户故事、功能规格、交互设计、验收标准。支持 Mermaid 流程图、UI 线框图示例。

---

### prd-test-writer — PRD 测试用例生成与评审

**作者**：[云舒](https://github.com/yunshu0909/yunshu_skillshub) | 文件：`SKILL.md` + `assets/` + `references/` + `samples/`

从 PRD 自动生成测试用例，并进行对抗性评审。输出包含 HTML 格式的评审报告和测试用例模板。

---

### prd-auto-test-loop — PRD 自动化测试闭环

**作者**：[云舒](https://github.com/yunshu0909/yunshu_skillshub) | 文件：`SKILL.md` + `agents/`

PRD → 测试用例 → 自动化执行 → 结果反馈的完整闭环。

---

### multi-perspective-analysis — 多视角分析

**作者**：[云舒](https://github.com/yunshu0909/yunshu_skillshub) | 文件：`SKILL.md` + 11 份参考文档

内置 10 位业界领袖的思维模型作为分析视角：

| 视角 | 思维模型 |
|---|---|
| Dan Sullivan | 10 倍增长思维 |
| Elon Musk | 第一性原理 |
| 张小龙 | 产品直觉 |
| MrBeast | 创作者增长 |
| Charlie Munger | 多元思维模型 |
| Peter Thiel | 从 0 到 1 |
| Steve Jobs | 产品愿景 |
| Jeff Bezos | 客户至上 |
| 张一鸣 | 算法思维 |
| 任正非 | 战略生存 |

---

### readable-output — 可读性输出优化

**作者**：[云舒](https://github.com/yunshu0909/yunshu_skillshub) | 文件：`SKILL.md`

优化 Agent 输出的可读性：结构化、分层、重点突出，让长内容更易阅读和理解。

---

### claude-code-style-html — 暖色纸质风格 HTML 生成

**原创** | 版本 2.0.0 | 文件：`SKILL.md` + `template.html`

完整的 HTML 页面设计系统：暖米白底 + 陶土橙点睛、衬线标题 + 无衬线正文、18 种组件、自检清单。

---

### problem-goal-defined — 问题定义与目标拆解

**原创** | 版本 1.0.0 | 文件：`SKILL.md` + 2 份参考文档

问题定义（5 步）：5W2H → 5 Whys → 边界分析 → 问题重构 → 假设检验。目标拆解（8 步）：SMART → 逆向推导 → WBS → 优先级 → 依赖 → 里程碑 → 风险预案。

---

### storage-analyzer — 全平台存储分析

**作者**：[卡兹克](https://github.com/KKKKhazix/khazix-skills) | 文件：`SKILL.md` + `assets/` + `references/` + `scripts/`

macOS / Windows 双平台只读存储分析：🟢可自动清理 / 🟡需判断 / 🔴谨慎清理 三级分类，生成交互式 HTML 报告 + 本地服务一键清理。

---

### hv-analysis — 横纵分析法深度研究

**作者**：[卡兹克](https://github.com/KKKKhazix/khazix-skills) | 文件：`SKILL.md` + `references/` + `scripts/`

纵轴追踪发展历程，横轴竞品对比，交叉产出洞察，输出 PDF 报告。

---

### leader — Agent 目标任务书生成器

**作者**：[卡兹克](https://github.com/KKKKhazix/khazix-skills) | 文件：`SKILL.md` + `references/`

领导出想法 → 管理者调研写书 → 执行者拿书独立跑完。含实测数字、白名单地界、防作弊验收。

---

## 🗂️ 项目结构

```
shared-files/
├── README.md
├── LICENSE
├── skills/
│   ├── ATTRIBUTION.md
│   ├── claude-code-style-html/         # [原创] 暖色 HTML 设计系统
│   ├── problem-goal-defined/           # [原创] 问题定义与目标拆解
│   ├── topic-question-generator/       # [原创] 课题研究问题引擎
│   ├── c-drive-cleanup/                # [原创] Windows C 盘清理
│   ├── equity-fund-attribution/        # [原创] 权益基金业绩归因
│   ├── fof-performance-attribution/    # [原创] FOF 业绩归因
│   ├── fixed-income-fund-attribution/  # [原创] 固收基金业绩归因
│   ├── prd-doc-writer/                 # [云舒] PRD 撰写
│   ├── prd-test-writer/                # [云舒] PRD 测试用例
│   ├── prd-auto-test-loop/             # [云舒] PRD 自动化测试
│   ├── multi-perspective-analysis/     # [云舒] 多视角分析
│   ├── readable-output/                # [云舒] 可读性输出
│   ├── git-push/                       # [云舒] Git 推送
│   ├── github-repo-search/             # [云舒] GitHub 搜索
│   ├── storage-analyzer/               # [卡兹克] 全平台存储分析
│   ├── hv-analysis/                    # [卡兹克] 横纵深度研究
│   └── leader/                         # [卡兹克] Agent 任务书
```

---

## 🤝 贡献与来源

本仓库收录了三类 Skills：

- **原创**：个人工作中沉淀的 Skills
- **社区精选**：来自优秀开源作者的 Skills（已标注来源和 License）
- 欢迎 Fork 并提交 PR 分享你的 Skills

提交新 Skill 时请确保：`SKILL.md` 包含完整的 frontmatter（name / description / version），不含个人信息（API Key、本地路径等），描述清晰说明"什么时候触发"和"做什么"。

社区贡献归属详见 [ATTRIBUTION.md](skills/ATTRIBUTION.md)。

---

## 📜 License

[MIT License](./LICENSE)

---

<p align="center">
  Made with 🤖 for QoderWork<br>
  <sub>一次整理，到处可用</sub>
</p>
