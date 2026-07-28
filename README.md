# shared-files

> **Agent Skills 工具箱 — 20 个技能，一行命令全平台同步**

换电脑、换平台，不用重新搭环境。克隆这个仓库，一行命令把所有 Skills 拉到本地。覆盖产品管理、金融分析、数据统计、思维学习、开发运维、系统设计 6 大场景。

| 快速信息 | |
|---|---|
| 技能总数 | **20 个**（8 原创 + 12 社区精选） |
| 覆盖场景 | 产品 · 金融 · 数据 · 思维 · 开发 · 设计 |
| 适用平台 | QoderWork / QoderCLI / 任何支持 SKILL.md 的 Agent |
| 安装时间 | < 30 秒 |

---

## 场景速选：你现在想做什么？

```
你想做什么？
│
├─ 写产品文档 ──────→ prd-doc-writer / prd-test-writer / prd-auto-test-loop
├─ 分析基金业绩 ────→ equity-fund-attribution / fof-performance-attribution / fixed-income-fund-attribution
├─ 做问卷/统计分析 ──→ statistical-analysis
├─ 画技术架构图 ────→ fireworks-tech-graph
├─ 拆解模糊问题 ────→ problem-goal-defined / topic-question-generator
├─ 多角度分析问题 ──→ multi-perspective-analysis / hv-analysis
├─ 给 Agent 派任务 ──→ leader
├─ 清理磁盘空间 ────→ storage-analyzer / c-drive-cleanup
└─ 生成漂亮网页 ────→ claude-code-style-html
```

---

## 安装：两种方式

### 方式一：全量同步（推荐，新电脑首选）

```bash
# macOS / Linux
git clone https://github.com/sliec/shared-files.git && cp -r shared-files/skills/* ~/.qoderwork/skills/

# Windows PowerShell
git clone https://github.com/sliec/shared-files.git
Copy-Item -Recurse -Force shared-files\skills\* "$env:USERPROFILE\.qoderwork\skills\"
```

同步完成，重新打开 Agent 对话即可使用所有技能。

### 方式二：按需单个安装

```bash
# macOS / Linux（替换技能名即可）
SKILL=claude-code-style-html
mkdir -p ~/.qoderwork/skills/$SKILL
curl -o ~/.qoderwork/skills/$SKILL/SKILL.md \
  https://raw.githubusercontent.com/sliec/shared-files/main/skills/$SKILL/SKILL.md

# Windows PowerShell
$skill = "claude-code-style-html"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.qoderwork\skills\$skill"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sliec/shared-files/main/skills/$skill/SKILL.md" `
  -OutFile "$env:USERPROFILE\.qoderwork\skills\$skill\SKILL.md"
```

---

## 20 个技能一览表

> 触发词就是你对 Agent 说的话，说完 Agent 会自动调用对应技能。

### 产品管理

| 技能 | 一句话说明 | 产出物 | 触发词 |
|---|---|---|---|
| **prd-doc-writer** | 按产品经理标准写 PRD，含需求背景、用户故事、功能规格、验收标准 | PRD 文档 + Mermaid 流程图 | "写PRD"、"产品需求文档" |
| **prd-test-writer** | 从 PRD 生成测试用例 + 对抗性评审报告 | HTML 评审报告 | "PRD测试"、"测试用例" |
| **prd-auto-test-loop** | PRD → 测试用例 → 自动执行 → 结果反馈的闭环 | 测试报告 + 修复建议 | "自动化测试"、"测试闭环" |

### 金融分析

| 技能 | 一句话说明 | 产出物 | 触发词 |
|---|---|---|---|
| **equity-fund-attribution** | 权益类基金业绩归因：净值法（T-M/H-M/Carhart）+ 持仓法（Brinson）+ 风险归因 | 归因报告 + 量化数据 | "基金归因"、"业绩归因"、"Brinson" |
| **fof-performance-attribution** | FOF 基金业绩归因：选基能力 + 择时能力 + 多因子回归 | 归因报告 + Python 计算 | "FOF归因"、"选基能力"、"FOF分析" |
| **fixed-income-fund-attribution** | 固收基金归因：财报法 + 净值法（Campisi五因子）+ 持仓法（四效应模型） | 归因报告 + 绩效指标 | "固收归因"、"债券基金"、"Campisi" |

### 数据分析

| 技能 | 一句话说明 | 产出物 | 触发词 |
|---|---|---|---|
| **statistical-analysis** | 统计顾问：先诊断数据再选方法，输出 APA 标准三件套 | 表格 + 图表 + 结果段落 | "统计分析"、"分析我的数据"、"问卷分析" |

### 思维与学习

| 技能 | 一句话说明 | 产出物 | 触发词 |
|---|---|---|---|
| **problem-goal-defined** | 把模糊问题变结构化：5W2H → 5Whys → WBS → SMART 拆解 | 问题定义书 + 行动路线图 | "帮我定义问题"、"目标拆解"、"根因分析" |
| **topic-question-generator** | 课题研究的问题引擎：系统性生成循序渐进的探究问题清单 | 问题清单 + 学习路线 | "帮我分析这个课题"、"帮我提问题" |
| **multi-perspective-analysis** | 10 位大佬视角分析问题（张小龙/Munger/Musk/Bezos 等） | 多视角分析报告 | "多视角分析"、"换个角度想" |
| **readable-output** | 优化 Agent 输出的可读性：结构化、分层、重点突出 | 优化后的输出文本 | "优化输出"、"可读性" |
| **hv-analysis** | 横纵分析法：纵轴发展历程 + 横轴竞品对比，交叉产出洞察 | PDF 深度研究报告 | "横纵分析"、"深度研究" |
| **leader** | 把一句话想法拆成 Agent 能独立跑完的任务书 | 目标任务书 | "帮我给 agent 写个目标" |

### 开发运维

| 技能 | 一句话说明 | 产出物 | 触发词 |
|---|---|---|---|
| **git-push** | Git 推送助手，规范 commit 流程 | 推送确认 | "git push"、"推送代码" |
| **github-repo-search** | GitHub 仓库智能搜索 | 仓库列表 + 推荐 | "搜GitHub"、"找仓库" |

### 系统设计

| 技能 | 一句话说明 | 产出物 | 触发词 |
|---|---|---|---|
| **fireworks-tech-graph** | 12 种视觉风格画 14 种图表类型（架构/流程/时序/C4/云部署等） | SVG / PNG / GIF / HTML | "画架构图"、"画流程图"、"技术图表" |
| **claude-code-style-html** | 暖色纸质风格 HTML 生成：18 种组件 + 完整设计系统 | 自包含 HTML 页面 | "做HTML"、"生成页面"、"写个页面" |

### 存储管理

| 技能 | 一句话说明 | 产出物 | 触发词 |
|---|---|---|---|
| **storage-analyzer** | macOS/Windows 双平台只读存储分析，三级分类 + 交互式报告 | HTML 报告 + 清理建议 | "存储分析"、"磁盘满了" |
| **c-drive-cleanup** | Windows C 盘轻量扫描与清理（仅 Windows） | 清理建议 | "C盘清理"、"空间不足" |

---

## 重点技能详解

### 金融分析三件套

这三个技能覆盖主流基金类型的业绩归因，组合使用效果最佳：

| 场景 | 用什么 |
|---|---|
| 股票型 / 混合型 / 指数增强基金 | `equity-fund-attribution` |
| FOF（基金中基金）| `fof-performance-attribution` |
| 纯债 / "固收+" / 债券型基金 | `fixed-income-fund-attribution` |

**equity-fund-attribution** 支持：Brinson 行业配置/选股归因、CT&CS 风格归因、Fama-French 三/四/五因子、Carhart 模型、T-M/H-M 择时选股检验、x-sigma-rho 风险分解。输出包含归因表格、贡献度图表和基金经理能力六模块评估。

**fof-performance-attribution** 支持：底层基金穿透分析、选基 Alpha 归因、择时能力 T-M/H-M 检验、多因子风格回归。附带 Python CLI 工具可直接计算。

**fixed-income-fund-attribution** 支持：Campisi 五因子净值回归（久期/利率曲线/信用利差/违约/可转债）、Campisi 四效应持仓归因（收入/国债/利差/择券）、Brinson 行业归因。绩效指标覆盖夏普/卡玛/信息比率/索提诺。

---

### statistical-analysis — 统计分析顾问

来源：[TerryFYL](https://github.com/TerryFYL/claude-statistical-analysis-skill)

核心理念是"先诊断数据，再选方法"——不直接跑统计，先看数据长什么样。

**工作流程**：数据画像（样本量/变量类型/缺失/分布）→ 前提假设检验（正态性/方差齐性）→ 智能方法选择 → 执行分析 → APA 三件套（表格 + 图表 + 结果段落）

**支持方法**：

| 级别 | 方法 |
|---|---|
| 基础 | 描述统计、t检验、卡方检验、相关、信效度（Cronbach's alpha） |
| 进阶 | 回归、ANOVA、调节/中介效应、ROC/AUC、生存分析 |
| 高阶 | SEM/CFA、HLM、IRT、元分析、倾向得分匹配 |
| 规划 | 样本量计算 / Power Analysis |

特别适合问卷调查分析，内置信效度分析和缺失数据处理。

---

### fireworks-tech-graph — 技术架构图绘制

来源：[yizhiyanhua-ai](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)

12 种视觉风格 × 14 种图表类型，几乎覆盖所有技术配图需求。

**视觉风格**：Flat Icon / Dark Terminal / Blueprint / Notion Clean / Glassmorphism / Claude Official / OpenAI Official / Dark Luxury / C4 Review Canvas / Cloud Fabric / Event Transit / Ops Pulse

**图表类型**：系统架构图、流程图、时序图、部署图、网络拓扑、数据流图、C4 模型、云架构、事件流、可观测性、Agent/记忆系统、UML、ER 图、时间线

---

### multi-perspective-analysis — 10 位大佬视角

来源：[云舒](https://github.com/yunshu0909/yunshu_skillshub)

同一个问题，切换 10 种思维模型来看：

| 视角 | 核心思维 | 适合分析 |
|---|---|---|
| 张小龙 | 产品直觉 | 产品设计、用户体验 |
| 张一鸣 | 算法思维 | 推荐系统、增长策略 |
| 任正非 | 战略生存 | 企业战略、组织管理 |
| Charlie Munger | 多元思维模型 | 投资决策、认知偏差 |
| Elon Musk | 第一性原理 | 技术创新、成本控制 |
| Jeff Bezos | 客户至上 | 商业模式、运营效率 |
| Steve Jobs | 产品愿景 | 品牌定位、产品打磨 |
| Peter Thiel | 从 0 到 1 | 创业方向、垄断策略 |
| Dan Sullivan | 10 倍增长 | 个人成长、目标设定 |
| MrBeast | 创作者增长 | 内容策略、流量运营 |

---

### problem-goal-defined — 问题定义与目标拆解

原创技能，分两步走：

**第一步 · 定义问题（5 步）**：5W2H 全面扫描 → 5 Whys 找根因 → 边界分析划清范围 → 问题重构 → 假设检验

**第二步 · 拆解目标（8 步）**：SMART 定义 → 逆向推导 → WBS 分解 → 优先级排序 → 依赖关系 → 里程碑 → 风险预案 → OKR 对齐

---

### claude-code-style-html — 暖色纸质风格 HTML

原创技能，完整的 HTML 页面设计系统：暖米白底 + 陶土橙点睛、衬线标题 + 无衬线正文、18 种预设组件、响应式布局、内置自检清单。适合生成报告页面、文档页面、数据展示页。

---

### leader — Agent 目标任务书

来源：[卡兹克](https://github.com/KKKKhazix/khazix-skills)

把领导一句话的想法，拆成 AI Agent 能独立跑完的任务书。含三层角色：领导出想法 → 管理者调研写书 → 执行者拿书独立跑。含实测数字、白名单边界、防作弊验收机制。

---

## 对比：相似技能怎么选？

| 你可能在纠结 | 用这个 | 为什么 |
|---|---|---|
| 分析股票基金 vs 债券基金 vs FOF | 看清基金类型再选 | equity / fixed-income / fof 三选一 |
| storage-analyzer vs c-drive-cleanup | Windows 用户日常用 `c-drive-cleanup`；深度分析用 `storage-analyzer` | 前者轻量快速，后者报告详细 |
| problem-goal-defined vs topic-question-generator | 业务问题用前者，学术课题用后者 | 前者偏 OKR/WBS，后者偏探究问题链 |
| multi-perspective-analysis vs hv-analysis | 快速多视角用前者，深度研究报告用后者 | 前者出分析报告，后者出 PDF 报告 |
| prd-doc-writer vs prd-test-writer | 先写 PRD 用前者，PRD 写完要测用后者 | 可配合 prd-auto-test-loop 形成闭环 |

---

## 项目结构

```
shared-files/
├── README.md                          # 你正在看的文件
├── LICENSE
└── skills/
    ├── ATTRIBUTION.md                 # 社区贡献归属
    │
    │  ── 金融分析 ──
    ├── equity-fund-attribution/       # [原创] 权益基金业绩归因
    ├── fof-performance-attribution/   # [原创] FOF 业绩归因
    ├── fixed-income-fund-attribution/ # [原创] 固收基金业绩归因
    │
    │  ── 数据分析 ──
    ├── statistical-analysis/          # [TerryFYL] 统计分析顾问
    │
    │  ── 产品管理 ──
    ├── prd-doc-writer/                # [云舒] PRD 撰写
    ├── prd-test-writer/               # [云舒] PRD 测试用例
    ├── prd-auto-test-loop/            # [云舒] PRD 自动化测试
    │
    │  ── 思维与学习 ──
    ├── problem-goal-defined/          # [原创] 问题定义与目标拆解
    ├── topic-question-generator/      # [原创] 课题研究问题引擎
    ├── multi-perspective-analysis/    # [云舒] 多视角分析
    ├── readable-output/               # [云舒] 可读性输出
    ├── hv-analysis/                   # [卡兹克] 横纵深度研究
    ├── leader/                        # [卡兹克] Agent 任务书
    │
    │  ── 开发运维 ──
    ├── git-push/                      # [云舒] Git 推送助手
    ├── github-repo-search/            # [云舒] GitHub 搜索
    │
    │  ── 系统设计 ──
    ├── fireworks-tech-graph/          # [yizhiyanhua-ai] 技术架构图绘制
    ├── claude-code-style-html/        # [原创] 暖色 HTML 设计系统
    │
    │  ── 存储管理 ──
    ├── storage-analyzer/              # [卡兹克] 全平台存储分析
    └── c-drive-cleanup/               # [原创] Windows C 盘清理
```

---

## 贡献

本仓库收录三类 Skills：个人原创、社区精选（已标注来源和 License）。

**提交新 Skill 的要求**：
- `SKILL.md` 含完整 frontmatter（name / description / version）
- 不含个人信息（API Key、本地路径等）
- description 清晰说明"什么时候触发"和"做什么"

社区贡献归属详见 [ATTRIBUTION.md](skills/ATTRIBUTION.md)。

---

## License

[MIT License](./LICENSE)

---

<p align="center">
  Made with 🤖 for QoderWork<br>
  <sub>一次整理，到处可用</sub>
</p>
