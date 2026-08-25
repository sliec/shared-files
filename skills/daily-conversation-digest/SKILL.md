---
name: daily-conversation-digest
description: 整理当日所有 QoderWork 对话，提取用户提问和 AI 回复，连同产出文件一起打包成可读的 Markdown 日报。适用于"每日对话整理"、"今日对话摘要"、"daily digest"、"导出今天聊了什么"等场景。可配合定时任务每日自动运行。
version: 1.0.0
---

# 每日对话整理 (Daily Conversation Digest)

## 触发词
每日对话整理、今日对话摘要、daily digest、导出今天聊了什么、整理今天的对话

## 工作流程

### 1. 确定日期
运行 `date` 获取当前日期，用于筛选当天的 JSONL 文件和命名输出。

### 2. 运行提取脚本
执行以下 Python 脚本，传入日期参数（格式 YYYY-MM-DD），脚本会：
- 统计窗口为前一日 23:00 ~ 当日 23:00（覆盖完整工作日）
- 扫描 `~/.qoderwork/projects/` 下窗口内修改过的 `.jsonl` 文件
- 按 sessionId 去重（同一会话可能出现在多个项目目录下）
- 提取用户提问（排除 system-reminder 注入内容）和 AI 文字回复
- 列出每个会话 outputs 目录下的产出文件
- 输出一份 Markdown 日报

```bash
python ~/.qoderwork/skills/daily-conversation-digest/extract.py --date YYYY-MM-DD --output "输出路径.md"
```

### 3. 输出格式
生成的 Markdown 文件结构如下：

```
# QoderWork 对话日报 - 2026-08-06

## 概览
- 总会话数：X
- 总提问数：X
- 产出文件数：X

---

## 会话 1：{session标题或ID}
时间范围：HH:MM - HH:MM

### 对话记录

**Q1** (HH:MM)
{用户提问内容，超过500字截断并标注}

**A1** (HH:MM)
{AI回复内容，超过1000字截断并标注}

**Q2** (HH:MM)
...

### 产出文件
- 文件名1 (大小)
- 文件名2 (大小)

---
```

### 4. 保存位置
- 默认保存到 `~/.qoderwork/workspace/{当前会话ID}/outputs/对话日报_YYYY-MM-DD.md`
- 如果用户指定了其他路径，按用户要求保存

### 5. 注意事项
- 用户提问中的 `<system-reminder>` 标签内容必须过滤，只保留用户实际输入的文字
- AI 回复中的 thinking 内容不提取，只提取 type="text" 的 content
- 超长内容做截断处理，标注"（已截断，共 X 字）"
- 如果某天没有对话，输出"今日无对话记录"
- 产出文件路径在 workspace 的 outputs 子目录下，按实际存在的情况列出

## 定时任务配置建议
建议设置为每天 23:00 或 23:30 运行：
```
schedule: { kind: "cron", expr: "0 23 * * *", tz: "Asia/Shanghai" }
payload.message: "执行每日对话整理：运行 daily-conversation-digest skill，把今天所有对话整理成日报，保存到 outputs 目录。"
```
