---
name: yingmi-skill
description: 盈米且慢金融数据与财富规划能力集。当用户需要筛选基金、分析基金、诊断组合、生成市场简报、做家庭财务规划、财富目标测算、投顾内容创作、数据可视化等金融场景时使用。基于 yingmi-skill-cli MCP 工具提供 57 个原子金融能力。
version: 0.1.0
---

# 盈米且慢金融能力集（yingmi-skill）

> **注意**：本 SKILL 为网络受限环境下的临时部署。待 Gitee 可访问后，请用 `git clone https://gitee.com/yingmi-tech/yingmi-skill.git` 替换本目录以获取完整模板与引用文件。

## CLI 路径

CLI 安装于用户级 npm 目录，调用前须确保 PATH 包含：

```
C:\Users\lisong\AppData\Roaming\npm
```

在 QoderWork Bash 中使用：
```bash
export PATH="C:/Users/lisong/AppData/Roaming/npm:$PATH"
yingmi-skill-cli <command>
```

## 场景路由

根据用户意图，路由到对应的子 skill 或直接调用 MCP 工具：

| 用户意图 | 路由目标 | 说明 |
|---------|---------|------|
| 筛选/推荐基金、找基金、债基排雷 | `fund-screener` | 不知道买什么 → 选基引擎 |
| 分析某只基金、基金对比、经理画像 | `fund-analyst` | 已知基金怎么样 → 深度分析 |
| 诊断持仓组合、回测、优化建议 | `portfolio-doctor` | 已有持仓 → 组合诊断 |
| 市场早报、行情速报、热点汇总 | `market-morning-brief` | 市场发生了什么 → 信息聚合 |
| 家庭财务规划、收支梳理、资产配置 | `wealth-family-advisor` | 家庭理财 → 全面规划 |
| 财富目标测算、月投计算 | `wealth-goalcalc` | 目标数字测算 → 复利计算 |
| 目标优先级推荐、目标匹配 | `wealth-goalmatch` | 多个目标如何排序 → 智能推荐 |
| 整合型财富规划报告 | `wealth-report` | 需要完整书面报告 → 全模块输出 |
| 家庭财务健康体检 | `wealth-healthcheck` | 快速体检 → 9 项指标评级 |
| 投顾内容创作、市场解读文案 | `advisor-content-studio` | 内容生产 → 选题+写作+排版 |
| 数据可视化、图表制作 | `design-data-visualization` | 可视化需求 → 多库支持 |

## MCP 工具调用方式

### 查看工具列表
```bash
yingmi-skill-cli mcp list
```

### 查看工具 Schema
```bash
yingmi-skill-cli mcp schema <toolName>
```

### 调用工具
```bash
yingmi-skill-cli mcp call <toolName> --input '<json>'
```

## MCP 工具速查（57 个）

### 基金搜索与信息
- `SearchFunds` — 搜索/筛选基金（按名称、代码、类型、收益排序）
- `GuessFundCode` — 基金名称模糊匹配代码
- `BatchGetFundsDetail` — 批量基金详情（规模/经理/费率/持仓/交易限制）
- `GetBatchFundPerformance` — 批量基金业绩（阶段收益+业绩指标，每次≤20只）
- `GetPopularFund` — 近期热门基金
- `BatchGetFundNavHistory` — 基金净值历史
- `BatchGetFundTradeLimit` — 交易限制（申购/赎回/定投状态+起购金额）
- `BatchGetFundTradeRules` — 交易规则（费率/确认日/到账日）
- `BatchGetFundsDividendRecord` — 分红记录
- `BatchGetFundsSplitHistory` — 拆分记录

### 基金深度分析
- `GetFundDiagnosis` — 基金诊断（风险/估值/业绩/行业/配置）
- `AnalyzeFundRisk` — 风险分析（风险评分/R方/残差/标准误差）
- `getFundBenchmarkInfo` — 业绩基准信息
- `fund-equity-position` — 权益仓位偏好
- `fund-sector-preference` — 板块配置偏好
- `fund-recovery-ability` — 回撤修复能力
- `getFundIndustryAllocation` — 行业配置比例
- `getFundIndustryConcentration` — 行业持仓集中度
- `getFundIndustryPreference` — 行业偏好
- `getFundIndustryReturns` — 行业收益归因
- `getStockAllocationAndMetricsByFundCode` — 估值盈利指标（PE/PB/ROE）
- `getBondAllocationByFundCode` — 券种配置
- `getBondFundCreditRatingLevel` — 债券信用评级
- `getBondIndicator` — 债基风险（久期/杠杆/集中度）
- `getFundTurnoverRate` — 换手率
- `getQdFundAreaAllocation` — QDII 地区配置
- `getFundBrinsonIndicator` — Brinson 归因（行业配置/选股收益）
- `getFundCampisiIndicator` — Campisi 归因（收入/国债/利差效应）
- `getMarketTimingIndicator` — 权益仓位择时
- `getFundDiveCount` — 债基异动/跳水次数

### 债基专项筛选
- `filterBondFundByBondType` — 券种风格筛选
- `filterBondFundByCreditRating` — 信用评级筛选
- `filterStockFundByStockTurnover` — 股票换手率筛选
- `getBondFundWithAlertRecord` — 净值异动/跳水告警债基

### 组合诊断与回测
- `DiagnoseFundPortfolio` — 账户诊断（配置/相关性/回测三维评分）
- `AnalyzePortfolioRisk` — 组合风险评估
- `GetAssetAllocation` — 资产配置分析（雷达图）
- `GetFundsCorrelation` — 基金相关性分析
- `GetFundsBackTest` — 回测分析（年化收益/最大回撤/夏普）
- `MonteCarloSimulate` — 蒙特卡洛模拟（未来收益概率分布）
- `GetFundAssetClassAnalysis` — 穿透资产大类分布

### 策略/投顾
- `StrategySearchByKeyword` — 策略关键词搜索
- `GetStrategyDetails` — 策略详情
- `GetStrategyRiskInfo` — 策略风险
- `GetStrategyBenchmark` — 策略业绩基准
- `GetStrategyAssetClassAnalysis` — 策略资产分布
- `BatchGetStrategiesComposition` — 策略持仓
- `BatchGetPoTradeComposition` — 策略交易成分
- `BatchGetStrategyRiskInfo` — 批量策略风险
- `GetFundRelatedStrategies` — 按重仓基金查策略
- `GetCompositeModel` — 复合模型（配置方案落地）
- `GetAssetAllocationPlan` — 资产配置方案

### 财富规划
- `AnalyzeAssetLiability` — 资产负债分析
- `AnalyzeCashFlow` — 现金流分析
- `AnalyzeFamilyMembers` — 家庭结构分析
- `AnalyzeFinancialIndicators` — 财务指标分析（7 项）
- `AnalyzeIncomeExpense` — 收支分析
- `AnalyzeInvestmentPerformance` — 投资方案表现

### 市场与内容
- `GetLatestQuotations` — 市场温度计（收盘行情/温度）
- `SearchFinancialNews` — 财经资讯搜索
- `SearchHotTopic` — 热点话题榜单
- `SearchManagerViewpoint` — 基金经理观点
- `searchInvestAdvisorContent` — 投顾内容搜索
- `searchRealtimeAiAnalysis` — 实时 AI 解读

### 工具
- `GetCurrentTime` — 获取当前时间
- `GetTxnDayRange` — 交易日查询
- `RenderEchart` — ECharts 图表渲染（返回图片 URL）
- `RenderHtmlToPdf` — HTML 转 PDF（返回 URL）

## 子 Skill 描述

### fund-screener（智能选基）
筛选基金、推荐基金、债基排雷。从用户需求解析筛选条件，组合 MCP 工具执行，结果排序过滤后输出推荐。支持条件筛选、热门推荐、债基排雷、券种/评级/换手率筛选、策略关联查找。

### fund-analyst（基金分析）
单只基金深度分析、多基金对比、基金经理画像。提供基金表现、风险、持仓和交易规则的全方位解读。

### portfolio-doctor（组合诊断）
基金持仓组合诊断、优化建议和历史回测。提供组合健康度、资产配置、相关性评估、蒙特卡洛模拟等全方位分析。

### market-morning-brief（市场简报）
市场早报、行情速报、基金经理观点汇总、投顾内容速览。自动聚合行情数据、财经资讯、热点话题生成结构化简报。

### wealth-family-advisor（家庭财务规划）
家庭理财规划、收支分析、资产负债评估、现金流预测、资产配置方案。覆盖家庭全生命周期的财务规划需求。

### wealth-goalcalc（目标测算）
财富目标终值测算、达成率计算、月投缺口分析。基于复利公式的精确计算。

### wealth-goalmatch（目标推荐）
推荐财富目标优先级、评估目标合理性、给出目标金额/期限/月投建议。

### wealth-report（财富报告）
整合型财富规划书面报告，涵盖诊断、资产负债、收支、指标、目标、现金流、配置与保障建议等 9 大模块。

### wealth-healthcheck（财务体检）
家庭财务健康体检，9 项核心指标与评级，输出结构化 HTML 体检报告。

### advisor-content-studio（投顾内容创作）
投顾内容生产与市场解读，支持选题发现、素材搜集、写作与排版美化。

### design-data-visualization（数据可视化）
创建图表和数据可视化，支持 matplotlib、Plotly、D3.js、Chart.js 等多库输出。

## 合规边界

- 仅使用盈米且慢 MCP 工具返回的公开数据
- 推荐结果附带客观数据依据，**不构成投资建议**
- 不做主观预测、不承诺收益
- 末尾必须使用标准免责声明

## 免责声明（标准版本）

```
免责声明：以上分析/筛选结果基于历史数据和公开信息，仅供参考，不构成投资建议。
基金过往业绩不预示未来表现，投资有风险，入市需谨慎。数据来源：盈米且慢。
```
