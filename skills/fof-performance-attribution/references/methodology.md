# FOF业绩归因方法论详细参考

## Brinson模型

### 经典GH-Brinson模型

单期超额收益分解为三项：

**资产配置效应 (AA)**：
$$AA = \sum_{i=1}^{n} (W_{pi} - W_{bi}) \times R_{bi}$$

其中 $W_{pi}$ 为组合中第 $i$ 类资产的权重，$W_{bi}$ 为基准中第 $i$ 类资产的权重，$R_{bi}$ 为基准中第 $i$ 类资产的收益率。

含义：FOF经理超配表现优于基准平均水平的资产类别、或低配表现劣于基准的资产类别时，AA为正。

**基金选择效应 (SS)**：
$$SS = \sum_{i=1}^{n} W_{bi} \times (R_{pi} - R_{bi})$$

$R_{pi}$ 为组合中第 $i$ 类资产的实际收益率。

含义：在给定资产类别内，FOF挑选的子基金组合是否超越了该类别基准的平均表现。

**交互效应 (IA)**：
$$IA = \sum_{i=1}^{n} (W_{pi} - W_{bi}) \times (R_{pi} - R_{bi})$$

含义：配置决策与选基决策之间的协同效应——是否在"正确"的资产类别上同时展现了卓越的选基能力。

**总超额收益验证**：$R_P - R_B = AA + SS + IA$

### FOF场景的特殊适配

在FOF中，Brinson模型的层次比传统基金更丰富：

**"资产配置"的三层扩展**：
1. 大类资产层：股票型基金、债券型基金、货币型基金、商品型基金、另类策略基金之间的配置
2. 投资风格层：成长/价值/均衡、大盘/小盘/中盘之间的配置
3. 投资策略层：主动量化、主观多头、宏观对冲、CTA等策略基金之间的配置

**"证券选择"转化为"基金选择"**：FOF不直接持有股票债券，"选券"能力体现为选基能力（Fund Selection）。衡量在同一风格/类别内，FOF经理挑选的子基金是否创造了超额收益。

### 多期Brinson联结算法

经典Brinson假设单期内持仓不变，多期简单加总会产生"残差项"。解决方案：

**GRAP联结**：
$$\text{总归因}_k = \prod_{t=1}^{T}(1 + R_{pt}) / \prod_{t=1}^{T}(1 + R_{bt}) - 1$$
各归因项按比例缩放，简单但可能有残差。

**Carino联结**（推荐，无残差）：
引入平滑因子 $a_t = \frac{R_{pt} - R_{bt}}{\ln(1+R_{pt}) - \ln(1+R_{bt})}$（当 $R_{pt} \neq R_{bt}$），将各期残差重新分配到各归因项中，强制消除总残差。

$$\text{总归因}_k = \sum_{t=1}^{T} a_t \times \text{单期归因}_{k,t}$$

**Menchero联结**（无残差）：
与Carino类似，重分配逻辑不同，试图保持原始归因项的相对重要性：
$$\text{总归因}_k = \sum_{t=1}^{T} \frac{R_P - R_B}{\sum_t (R_{Pt} - R_{Bt})} \times \text{单期归因}_{k,t}$$

选择建议：Carino在业界应用最广，Menchero在保持归因项比例关系上更优。

### 案例计算

假设FOF配置如下，基准为80%权益+20%债券：

| 类别 | FOF权重 | 基准权重 | FOF收益 | 基准收益 |
|------|---------|---------|---------|---------|
| 权益 | 90% | 80% | 12% | 10% |
| 债券 | 10% | 20% | 2.5% | 2% |

FOF总收益 = 90%×12% + 10%×2.5% = 11.05%
基准总收益 = 80%×10% + 20%×2% = 8.40%
总超额 = 2.65%

AA = (90%-80%)×(10%-8.4%) + (10%-20%)×(2%-8.4%) = 0.16% + 0.64% = **0.80%**
SS = 80%×(12%-10%) + 20%×(2.5%-2%) = 1.60% + 0.10% = **1.70%**
IA = (90%-80%)×(12%-10%) + (10%-20%)×(2.5%-2%) = 0.20% - 0.05% = **0.15%**
验证：0.80 + 1.70 + 0.15 = 2.65% ✓

---

## Barra因子模型

### 在FOF归因中的角色

Barra不是替代Brinson，而是对Brinson"基金选择效应"的再分解。

### 应用流程

1. **穿透持仓**：获取FOF持有的所有子基金的底层持仓（股票和债券）
2. **构建因子暴露矩阵**：利用Barra模型（如CNE5/USE4），计算FOF在每个时点上对风格因子和行业因子的暴露度
3. **收益分解**：将超额收益分解为：
   - **因子选择收益**：主动暴露于特定因子的收益（如成长股牛市中超配成长因子）
   - **个股Alpha**：剔除所有因子影响后，子基金持有的个股贡献的超额收益

### 核心因子

| 因子 | 含义 | 高暴露意味着 |
|------|------|------------|
| Size（规模） | 大盘vs小盘 | 偏好小盘股 |
| Value（价值） | 高BP vs 低BP | 偏好低估值股票 |
| Momentum（动量） | 过去12月收益 | 偏好近期强势股 |
| Volatility（波动） | 历史波动率 | 偏好低波动或高波动 |
| Leverage（杠杆） | 财务杠杆 | 偏好高杠杆或低杠杆公司 |
| Growth（成长） | 盈利增长预期 | 偏好高成长股 |

### 局限性

- 穿透数据获取难度大，成本高
- Barra模型本身有模型风险
- 适用于权益类FOF，固收类FOF需定制因子

---

## 多因子回归模型

### CAPM模型

$$R_p - R_f = \alpha_p + \beta_p (R_m - R_f) + \epsilon$$

最基础模型。$\alpha_p$ 为风险调整后的超额收益（Jensen's Alpha），$\beta_p$ 衡量系统性风险暴露。

### Fama-French三因子模型

$$R_p - R_f = \alpha_p + \beta_1 (R_m - R_f) + \beta_2 SMB + \beta_3 HML + \epsilon$$

- SMB (Small Minus Big)：小盘股收益减大盘股收益，正暴露=偏好小盘
- HML (High Minus Low)：高BP股收益减低BP股收益，正暴露=偏好价值

### Carhart四因子模型

$$R_p - R_f = \alpha_p + \beta_1 (R_m - R_f) + \beta_2 SMB + \beta_3 HML + \beta_4 MOM + \epsilon$$

- MOM (Momentum)：过去12个月赢家组合减输家组合收益，正暴露=趋势跟随

### A股因子数据获取

- 市场因子：沪深300日收益率 - Shibor/国债利率日化
- SMB/HML：CSMAR中国三因子数据库，或自行按市值和BP排序构建
- MOM：按过去12个月收益排序，赢家组（前30%）减输家组（后30%）

### 回归执行与诊断

```python
import statsmodels.api as sm

# 准备数据
X = sm.add_constant(factors)  # 添加截距项
y = fund_excess_returns

# OLS回归
model = sm.OLS(y, X).fit()
print(model.summary())

# 关注：
# - coef[const] = Alpha（年化需 ×252 或 ×52）
# - P>|t| < 0.05 为统计显著
# - R-squared 为模型解释力
```

### 局限与警示

1. **相关性≠因果性**：因子暴露高可能是主动配置也可能是被动结果
2. **适用性**：Fama-French针对权益资产设计，固收+FOF需引入信用利差、期限利差等因子
3. **Alpha是黑箱**：残差项吸收所有未建模因素，不能简单等同于能力

---

## 择时能力模型

### T-M模型 (Treynor-Mazuy)

$$R_p - R_f = \alpha_p + b(R_m - R_f) + c(R_m - R_f)^2 + \epsilon$$

**择时判断**：c > 0 且统计显著 → 具备择时能力。
- 逻辑：市场上涨时(Rm-Rf大正数)，基金Beta增加（向上凸曲线），放大收益；市场下跌时Beta减小，控制回撤

**选股判断**：αp 为剔除择时影响后的纯选股能力

```python
excess_market = market_returns - rf
excess_market_sq = excess_market ** 2
X = sm.add_constant(pd.DataFrame({'market': excess_market, 'market_sq': excess_market_sq}))
model = sm.OLS(fund_excess, X).fit()
# model.params['market_sq'] > 0 且 p < 0.1 → 具备择时能力
```

### H-M模型 (Henriksson-Merton)

$$R_p - R_f = \alpha_p + b(R_m - R_f) + d \cdot D \cdot (R_m - R_f) + \epsilon$$

其中 $D = 1$ 当 $R_m > R_f$（牛市），否则 $D = 0$。

**择时判断**：d > 0 且统计显著 → 牛市加仓（总Beta = b+d）、熊市减仓（总Beta = b）

```python
bull_market = (excess_market > 0).astype(int)
interaction = bull_market * excess_market
X = sm.add_constant(pd.DataFrame({'market': excess_market, 'interaction': interaction}))
model = sm.OLS(fund_excess, X).fit()
# model.params['interaction'] > 0 且 p < 0.1 → 具备择时能力
```

### 跨周期分析补充

除模型外，还应分析：
- 牛市期间Alpha vs 熊市期间Alpha
- 优秀基金经理通常在**下行期择时更强**（降仓/防御配置），**上行期选基更强**（积极进攻）
- 这种非对称能力展现是成熟度的标志

---

## 风险收益指标详解

### 夏普比率 (Sharpe Ratio)

$$SR = \frac{R_p - R_f}{\sigma_p}$$

- 衡量每单位总风险的超额回报
- > 1 为良好，> 2 为优秀
- 局限：假设收益率正态分布，对非对称分布（如期权策略）不适用

### 最大回撤 (Max Drawdown)

$$MDD = \max_{t} \left( \frac{\text{peak}_t - \text{trough}_t}{\text{peak}_t} \right)$$

- 衡量从峰值到谷底的最大损失
- 投资者最直观的"痛感"指标
- FOF的核心优势之一就是通过分散降低最大回撤

### 卡玛比率 (Calmar Ratio)

$$Calmar = \frac{\text{年化收益率}}{|MDD|}$$

- 直接关联收益与最大亏损体验
- > 1 为可接受，> 2 为优秀
- 特别适合评估注重回撤控制的策略

### 索提诺比率 (Sortino Ratio)

$$Sortino = \frac{R_p - R_f}{\sigma_d}$$

$\sigma_d$ 为下行偏差（只计算收益率为负的波动）。

- 比夏普更公平：向上的波动不算"风险"
- 对非对称收益分布的基金更有参考价值

### 信息比率 (Information Ratio)

$$IR = \frac{\alpha_p}{\omega_p}$$

$\omega_p$ 为跟踪误差（超额收益的标准差）。

- 衡量Alpha的稳定性
- > 0.5 为良好，> 1 为优秀
- 适合评估相对收益型FOF

### 年化计算注意

- 日频数据年化：收益 × 252，波动 × √252
- 周频数据年化：收益 × 52，波动 × √52
- 月频数据年化：收益 × 12，波动 × √12

---

## 业绩比较基准选择（SAMURAI原则）

| 原则 | 英文 | 含义 |
|------|------|------|
| 明确性 | Specified in advance | 评估期开始前已确定 |
| 适当性 | Appropriate | 与投资策略和风格一致 |
| 可测性 | Measurable | 可及时准确获取 |
| 无偏性 | Unambiguous | 构成和计算公开透明 |
| 可投资性 | Investable | 可低成本复制 |
| 代表性 | Representative | 代表FOF专注的特定领域 |

### FOF基准构建实践

- **混合型基准**："中债新综合指数×80% + 沪深300指数×20%"——权重应反映策略说明书中的中枢配置比例
- **风格化基准**：全球科技FOF → MSCI全球科技指数
- **Brinson子基准**：权益部分用偏股混合型基金指数，债券部分用中长期纯债型基金指数
- **回归模型基准(Rm)**：A股FOF通常选沪深300或中证800

### 基准错误导致的误判

为成长型FOF选择价值型基准 → 成长牛市中出现"伪Alpha"，价值回归时显得能力拙劣。分析前务必验证基准合理性。
