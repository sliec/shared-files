# 招募说明书更新器 - 技术参考

## PDF提取代码模板

### 基础文本提取

```python
import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('fund_report.pdf') as doc:
    print(f'总页数: {len(doc.pages)}')
    for i, pg in enumerate(doc.pages):
        text = pg.extract_text() or ''
        # 搜索关键词定位关键页面
        if '基金业绩' in text or '资产组合' in text or '净值增长率' in text:
            print(f'=== PAGE {i+1} ===')
            print(text)
            print()
```

### 图表提取（累计净值走势图）

```python
import pdfplumber
from PIL import Image
import sys
sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('quarterly_report.pdf') as doc:
    # 找到包含图表的页面（搜索"自基金合同生效以来基金累计净值增长率"）
    for i, pg in enumerate(doc.pages):
        text = pg.extract_text() or ''
        if '自基金合同生效以来基金累计净值增长率' in text:
            # 提取该页所有图片的坐标
            for img in pg.images:
                print(f'Image: x0={img["x0"]}, top={img["top"]}, x1={img["x1"]}, bottom={img["bottom"]}')
            
            # 渲染整页为高分辨率图片
            im = pg.to_image(resolution=200)
            im.save(f'page_{i+1}_full.png')
            
            # 按坐标裁剪图表
            full = Image.open(f'page_{i+1}_full.png')
            scale = 200.0 / 72.0
            
            # 使用第一个图片的坐标（通常是累计净值图）
            img = pg.images[0]
            crop_left = int(img['x0'] * scale)
            crop_top = int(img['top'] * scale)
            crop_right = int(img['x1'] * scale)
            crop_bottom = int(img['bottom'] * scale)
            
            chart = full.crop((crop_left, crop_top, crop_right, crop_bottom))
            chart.save('chart.png')
            print(f'图表已保存: {chart.size}')
            break
```

### 表格提取（备选方案）

```python
import pdfplumber
import sys
sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('fund_report.pdf') as doc:
    for i, pg in enumerate(doc.pages):
        tables = pg.extract_tables()
        for tbl_idx, tbl in enumerate(tables):
            if tbl and len(tbl) > 0:
                # 检查是否包含目标数据
                first_row = ' '.join(str(x) for x in tbl[0] if x)
                if '资产组合' in first_row or '债券品种' in first_row:
                    print(f'=== PAGE {i+1} TABLE {tbl_idx+1} ===')
                    for row in tbl:
                        print(row)
                    print()
```

## 数据源定位指南

### 招募说明书PDF结构

| 章节 | 搜索关键词 | 内容 |
|------|-----------|------|
| 八（九）基金的投资组合报告 | "基金的投资组合报告" | 1-11项持仓明细 |
| 九 基金业绩 | "九 基金业绩" 或 "本报告期基金份额净值增长率" | 年度净值表+累计净值图 |

### 季报PDF结构

| 章节 | 搜索关键词 | 内容 |
|------|-----------|------|
| §3.2.1 基金净值表现 | "基金份额净值增长率及其与同期业绩比较基准收益率的比较" | 滚动区间数据（过去三个月/六个月/一年等） |
| §3.2.2 累计净值图 | "自基金合同生效以来基金累计净值增长率" | 累计净值走势图 |
| §5.1 资产组合情况 | "报告期末基金资产组合情况" | 1-11项持仓明细 |

### 年报PDF结构

| 章节 | 搜索关键词 | 内容 |
|------|-----------|------|
| 3.2.1 基金净值表现 | "基金份额净值增长率及其与同期业绩比较基准收益率的比较" | 滚动区间数据 |
| 3.2.3 每年净值增长率 | "过去五年基金每年净值增长率" | 年度柱状图（图表，需OCR） |
| 4.4.2 业绩表现 | "报告期内基金的业绩表现" | 当年全年净值增长率+基准收益率（文字） |

## 数据拼接逻辑

### 年度表拼接规则

假设上次招募说明书数据截止2025H1，最新年报是2025年，最新季报是2026Q2：

```
上次招募说明书：
2020成立年 ~ 2024全年 + 2025H1 + 累计(2020-2025H1)

↓ 替换2025H1为2025全年（来自年报）
2020成立年 ~ 2024全年 + 2025全年

↓ 新增2026H1行 + 更新累计行（来自2026Q2季报）
2020成立年 ~ 2024全年 + 2025全年 + 2026H1 + 累计(2020-2026H1)
```

### 复合验证公式

```python
# 各年净值增长率连乘应等于累计行
years = [0.0095, 0.0209, 0.0245, 0.0388, 0.0490, 0.0135, 0.0129]
product = 1.0
for r in years:
    product *= (1 + r)
print(f'连乘结果: {product:.4f}')  # 应≈1.1812（即18.12%）
```

## 常见问题处理

### Q1: MCP东财数据与招募说明书不一致

**现象**：MCP返回的2022年业绩比较基准是-0.60%，但招募说明书是0.51%

**原因**：MCP可能使用自然年度区间，而招募说明书使用基金实际运作区间

**解决**：以招募说明书原文为准，MCP数据仅作参考

### Q2: PDF下载失败

**现象**：`curl` 返回404或连接超时

**解决**：
1. 检查URL是否正确（东财PDF链接格式：`https://pdf.dfcfw.com/pdf/H2_AN{日期}_{编号}_1.pdf`）
2. 尝试从其他来源下载（如基金公司官网、巨潮资讯网）
3. 如果无法下载，使用MCP数据作为备选（但需标注数据来源）

### Q3: 图表提取坐标不对

**现象**：裁剪出的图片是空白或位置偏移

**原因**：pdfplumber的images坐标是PDF页面坐标（从顶部向下），但to_image渲染后坐标系可能不同

**解决**：
```python
# 方法1：直接使用images坐标（推荐）
scale = 200.0 / 72.0
crop_left = int(img['x0'] * scale)
crop_top = int(img['top'] * scale)
crop_right = int(img['x1'] * scale)
crop_bottom = int(img['bottom'] * scale)

# 方法2：如果方法1不对，尝试y翻转
page_height = float(pg.height)
crop_top = int((page_height - img['bottom']) * scale)
crop_bottom = int((page_height - img['top']) * scale)
```

### Q4: 年度标准差缺失

**现象**：招募说明书年度表有标准差列，但年报只有滚动区间表

**解决**：
1. 从上次招募说明书提取历史年度标准差
2. 当年标准差从最新季报的"过去六个月"或"过去一年"行获取
3. 如果都没有，使用MCP东财的"报告期净值增长率标准差"（但需标注数据来源）

### Q5: 基金类型特殊（如股票型、混合型）

**现象**：模板中的"无"项实际有数据

**解决**：
- 股票型/混合型基金：2.1、2.2、3项会有股票持仓数据，按PDF原文提取
- QDII基金：可能有港股通投资（2.2项）
- 债券型基金：通常2、3项为"无"，重点在4、5项债券持仓

## 输出文件命名规范

```
{基金简称}{基金代码}_更新招募说明书_{年份}Q{季度}.md
{基金简称}{基金代码}_更新招募说明书_{年份}Q{季度}.docx
chart_{基金代码}_cumulative_nav.png
```

示例：
```
大成惠享008628_更新招募说明书_2026Q2.md
大成惠享008628_更新招募说明书_2026Q2.docx
chart_008628_cumulative_nav.png
```
