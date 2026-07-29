# shared-files

> Agent Skills 同步中心 — 57 个技能，覆盖飞书生态、文档处理、金融分析、开发工具等场景

换电脑、换平台，不用重新搭环境。克隆这个仓库，一行命令把所有 Skills 拉到本地。

| 快速信息 | |
|---|---|
| 技能总数 | **57 个**（47 本地同步 + 10 仓库独有） |
| 最大分类 | 飞书生态（26个）、文档处理（4个）、开发工具（6个） |
| 适用平台 | QoderWork / QoderCLI / 任何支持 SKILL.md 的 Agent |

---

## 场景速选

```
你想做什么？
│
├─ 飞书办公 ────────→ lark-doc / lark-sheets / lark-base / lark-im / lark-mail / ...（26个）
├─ 处理文档 ────────→ docx / pdf / pptx / xlsx
├─ 分析基金业绩 ────→ equity-fund-attribution / fof-performance-attribution / fixed-income-fund-attribution
├─ 写产品文档 ──────→ prd-doc-writer / prd-test-writer / prd-auto-test-loop
├─ 画技术架构图 ────→ fireworks-tech-graph
├─ 做统计分析 ──────→ statistical-analysis
├─ 拆解模糊问题 ────→ problem-goal-defined / topic-question-generator
├─ 多角度分析 ──────→ multi-perspective-analysis / hv-analysis
├─ Git/开发 ────────→ git-push / github-repo-search / create-skill
├─ 清理磁盘 ────────→ c-drive-cleanup / storage-analyzer
└─ 生成漂亮网页 ────→ claude-code-style-html
```

---

## 安装

### 全量同步（推荐）

```bash
# macOS / Linux
git clone https://github.com/sliec/shared-files.git && cp -r shared-files/skills/* ~/.qoderwork/skills/

# Windows PowerShell
git clone https://github.com/sliec/shared-files.git
Copy-Item -Recurse -Force shared-files\skills\* "$env:USERPROFILE\.qoderwork\skills\"
```

### 按需单个安装

```bash
# 例：只安装 PDF 技能
cp -r shared-files/skills/pdf ~/.qoderwork/skills/
```

---

## 全部技能一览

### 飞书生态（26个）

| 技能 | 功能 |
|---|---|
| lark-doc | 飞书文档读写 |
| lark-sheets | 飞书电子表格 |
| lark-base | 飞书多维表格 |
| lark-im | 飞书即时消息 |
| lark-mail | 飞书邮件 |
| lark-calendar | 飞书日历 |
| lark-contact | 飞书通讯录 |
| lark-task | 飞书任务 |
| lark-okr | 飞书OKR |
| lark-drive | 飞书云文档 |
| lark-wiki | 飞书知识库 |
| lark-approval | 飞书审批 |
| lark-attendance | 飞书考勤 |
| lark-apps | 飞书应用 |
| lark-event | 飞书事件 |
| lark-markdown | 飞书Markdown |
| lark-minutes | 飞书妙记 |
| lark-slides | 飞书幻灯片 |
| lark-whiteboard | 飞书白板 |
| lark-vc | 飞书视频会议 |
| lark-vc-agent | 飞书视频会议Agent |
| lark-shared | 飞书通用配置 |
| lark-openapi-explorer | 飞书API浏览器 |
| lark-skill-maker | 飞书技能生成器 |
| lark-workflow-meeting-summary | 会议纪要工作流 |
| lark-workflow-standup-report | 站会报告工作流 |

### 文档处理（4个）

| 技能 | 功能 |
|---|---|
| docx | Word文档处理（含office schemas和脚本工具链） |
| pdf | PDF读取、生成、合并、转换 |
| pptx | PowerPoint演示文稿处理 |
| xlsx | Excel电子表格处理（含脚本工具链） |

### 金融分析（3个）

| 技能 | 功能 |
|---|---|
| equity-fund-attribution | 股票型基金业绩归因（Brinson/多因子） |
| fof-performance-attribution | FOF基金业绩归因（Brinson/T-M/H-M/风险） |
| fixed-income-fund-attribution | 固收基金业绩归因 |

### 产品管理（3个）

| 技能 | 功能 |
|---|---|
| prd-doc-writer | PRD产品需求文档撰写 |
| prd-test-writer | PRD测试用例撰写 |
| prd-auto-test-loop | PRD自动化测试循环 |

### 开发工具（6个）

| 技能 | 功能 |
|---|---|
| git-push | Git推送辅助 |
| github-repo-search | GitHub仓库搜索 |
| create-skill | 创建新Agent技能 |
| find-skills | 搜索和发现技能 |
| install-skill-dependency | 安装技能依赖 |
| plugin-creator | 插件创建器 |

### 数据与分析（3个）

| 技能 | 功能 |
|---|---|
| statistical-analysis | 统计分析（描述统计/假设检验/回归） |
| fireworks-tech-graph | 技术架构图生成（多种风格） |
| hv-analysis | 多维度分析 |

### 思维与方法（3个）

| 技能 | 功能 |
|---|---|
| problem-goal-defined | 问题目标定义与拆解 |
| topic-question-generator | 主题问题生成器 |
| multi-perspective-analysis | 多视角分析框架 |

### 系统与效率（6个）

| 技能 | 功能 |
|---|---|
| c-drive-cleanup | C盘清理 |
| storage-analyzer | 磁盘空间分析 |
| vm-error-recovery | 虚拟机错误恢复 |
| computer-use-guidance-windows | Windows桌面自动化指南 |
| qoderwork-guidance | QoderWork使用指南 |
| claude-code-style-html | 代码风格HTML生成 |

### 其他（3个）

| 技能 | 功能 |
|---|---|
| leader | Agent任务分配与协调 |
| ima-skill | IMA技能 |
| readable-output | 可读输出格式化 |

---

## 仓库结构

```
shared-files/
├── skills/              # 所有技能目录
│   ├── lark-doc/        # 飞书文档
│   │   └── SKILL.md     # 技能定义文件
│   ├── docx/            # Word处理
│   │   ├── SKILL.md
│   │   ├── scripts/     # 辅助脚本
│   │   └── reference/   # 参考文档
│   ├── fireworks-tech-graph/
│   │   ├── SKILL.md
│   │   ├── assets/      # 图片资源
│   │   ├── templates/   # 模板
│   │   └── schemas/     # 数据schema
│   └── ...              # 更多技能
├── ATTRIBUTION.md       # 来源与致谢
├── LICENSE
└── README.md
```

---

## 贡献

欢迎提交新技能或改进现有技能。每个技能需包含一个 `SKILL.md` 文件作为入口。
