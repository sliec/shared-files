#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Conversation Digest - 每日对话提取脚本
从 QoderWork 的 JSONL 日志中提取当天的问答记录，生成 Markdown 日报。
"""

import json
import os
import sys
import argparse
import glob
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import OrderedDict


def get_projects_dir():
    """获取 QoderWork projects 目录"""
    home = Path.home()
    return home / ".qoderwork" / "projects"


def find_jsonl_files(start_dt: datetime, end_dt: datetime):
    """查找在时间窗口内修改过的所有 JSONL 文件"""
    projects_dir = get_projects_dir()
    if not projects_dir.exists():
        return []

    results = []
    for root, dirs, files in os.walk(projects_dir):
        for f in files:
            if f.endswith(".jsonl"):
                fp = os.path.join(root, f)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(fp))
                    if start_dt <= mtime <= end_dt:
                        results.append(fp)
                except Exception:
                    pass
    return results


def deduplicate_by_session(jsonl_files):
    """按 sessionId 去重，保留第一个出现的文件"""
    seen_sessions = {}
    for fp in jsonl_files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    sid = obj.get("sessionId")
                    if sid and sid not in seen_sessions:
                        # 从目录名推断 workspace 路径
                        dir_name = os.path.basename(os.path.dirname(fp))
                        seen_sessions[sid] = {
                            "jsonl_path": fp,
                            "dir_name": dir_name,
                        }
                    break  # 只读第一行获取 sessionId
        except Exception:
            pass
    return seen_sessions


def extract_user_text(content_list):
    """从 user message 的 content 中提取实际提问（排除 system-reminder）"""
    texts = []
    for item in content_list:
        if not isinstance(item, dict):
            continue
        if item.get("type") != "text":
            continue
        text = item.get("text", "")
        # 过滤 system-reminder 注入
        if text.strip().startswith("<system-reminder>"):
            # 尝试提取 system-reminder 之后的用户实际输入
            # system-reminder 可能只占部分，后面跟着用户文字
            end_tag = "</system-reminder>"
            if end_tag in text:
                after = text.split(end_tag)[-1].strip()
                if after:
                    texts.append(after)
            # 如果整个都是 system-reminder，跳过
            continue
        if text.strip():
            texts.append(text.strip())
    return "\n".join(texts)


def extract_assistant_text(content_list):
    """从 assistant message 的 content 中提取文字回复（排除 thinking）"""
    texts = []
    for item in content_list:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "text":
            text = item.get("text", "").strip()
            if text:
                texts.append(text)
    return "\n".join(texts)


def truncate(text: str, max_len: int, label: str = "") -> str:
    """截断过长文本"""
    if len(text) <= max_len:
        return text
    return text[:max_len] + f"\n\n（已截断，共 {len(text)} 字）"


def parse_session(jsonl_path: str, start_dt: datetime, end_dt: datetime):
    """解析单个 JSONL 文件，提取时间窗口内的问答对"""
    conversations = []
    session_info = {
        "start_time": None,
        "end_time": None,
        "title": None,
    }

    with open(jsonl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_user_msg = None
    current_user_time = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg_type = obj.get("type")
        timestamp = obj.get("timestamp")

        # 解析时间戳
        ts = None
        if timestamp:
            if isinstance(timestamp, (int, float)):
                ts = datetime.fromtimestamp(timestamp / 1000)
            else:
                try:
                    ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    # 去掉时区信息，统一为本地时间比较
                    ts = ts.replace(tzinfo=None)
                except Exception:
                    ts = None

        # 检查是否在时间窗口内
        in_window = ts and (start_dt <= ts <= end_dt)

        # 记录时间范围（仅记录窗口内的）
        if ts and in_window:
            if session_info["start_time"] is None:
                session_info["start_time"] = ts
            session_info["end_time"] = ts

        if msg_type == "user" and in_window:
            content = obj.get("message", {}).get("content", [])
            user_text = extract_user_text(content)
            if user_text:
                current_user_msg = user_text
                current_user_time = ts.strftime("%H:%M") if ts else "??:??"

        elif msg_type == "assistant":
            content = obj.get("message", {}).get("content", [])
            asst_text = extract_assistant_text(content)
            if asst_text and current_user_msg:
                conversations.append({
                    "question": current_user_msg,
                    "answer": asst_text,
                    "q_time": current_user_time,
                    "a_time": ts.strftime("%H:%M") if ts else "??:??",
                })
                current_user_msg = None
                current_user_time = None
            elif asst_text and not current_user_msg and in_window:
                # AI 主动回复（如定时任务触发），也记录
                conversations.append({
                    "question": "（系统/定时触发）",
                    "answer": asst_text,
                    "q_time": "??:??",
                    "a_time": ts.strftime("%H:%M") if ts else "??:??",
                })

    return session_info, conversations


def list_output_files(session_dir_name: str, start_dt: datetime, end_dt: datetime):
    """列出会话的 outputs 目录下在时间窗口内修改的文件"""
    workspace_base = Path.home() / ".qoderwork" / "workspace" / session_dir_name / "outputs"
    files = []
    if workspace_base.exists():
        for f in os.listdir(workspace_base):
            fp = workspace_base / f
            if fp.is_file():
                try:
                    size = fp.stat().st_size
                    mtime = datetime.fromtimestamp(fp.stat().st_mtime)
                    if start_dt <= mtime <= end_dt:
                        size_str = format_size(size)
                        files.append({"name": f, "size": size_str})
                except Exception:
                    pass
    return files


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def get_session_title(session_id: str, dir_name: str):
    """尝试从数据库获取会话标题，否则用目录名"""
    # 从目录名提取 workspace ID（兼容不同用户名）
    import re
    match = re.search(r'workspace-(\w+)$', dir_name)
    if match:
        chat_id = match.group(1)
    elif dir_name.startswith("-sessions-"):
        chat_id = dir_name
    else:
        chat_id = dir_name

    # 尝试从数据库查标题
    try:
        import sqlite3
        db_path = Path.home() / "AppData" / "Roaming" / "QoderWork" / "data" / "agents.db"
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM chats WHERE id = ?", (chat_id,))
            row = cursor.fetchone()
            conn.close()
            if row and row[0]:
                return row[0]
    except Exception:
        pass

    return f"会话 {session_id[:8]}..."


def generate_markdown(target_date: date, start_dt: datetime, end_dt: datetime, sessions_data: list) -> str:
    """生成 Markdown 日报"""
    total_sessions = len(sessions_data)
    total_questions = sum(len(s["conversations"]) for s in sessions_data)
    total_files = sum(len(s["output_files"]) for s in sessions_data)

    lines = []
    lines.append(f"# QoderWork 对话日报 - {target_date.strftime('%Y-%m-%d')}\n")
    lines.append(f"> 统计窗口：{start_dt.strftime('%Y-%m-%d %H:%M')} ~ {end_dt.strftime('%Y-%m-%d %H:%M')}\n")
    lines.append("## 概览\n")
    lines.append(f"- 总会话数：**{total_sessions}**")
    lines.append(f"- 总提问数：**{total_questions}**")
    lines.append(f"- 产出文件数：**{total_files}**")
    lines.append("")

    if total_sessions == 0:
        lines.append("*今日无对话记录。*\n")
        return "\n".join(lines)

    for idx, session in enumerate(sessions_data, 1):
        info = session["session_info"]
        convs = session["conversations"]
        files = session["output_files"]
        title = session["title"]

        lines.append("---\n")
        lines.append(f"## 会话 {idx}：{title}\n")

        start = info["start_time"]
        end = info["end_time"]
        if start and end:
            lines.append(f"时间范围：{start.strftime('%H:%M')} - {end.strftime('%H:%M')}")
        lines.append("")

        if not convs:
            lines.append("*（该会话无有效问答记录）*\n")
            continue

        lines.append("### 对话记录\n")
        for q_idx, conv in enumerate(convs, 1):
            lines.append(f"**Q{q_idx}** ({conv['q_time']})")
            lines.append(truncate(conv["question"], 500, "提问"))
            lines.append("")
            lines.append(f"**A{q_idx}** ({conv['a_time']})")
            lines.append(truncate(conv["answer"], 1000, "回复"))
            lines.append("")

        if files:
            lines.append("### 产出文件\n")
            for f in files:
                lines.append(f"- {f['name']} ({f['size']})")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="每日对话提取工具")
    parser.add_argument("--date", type=str, default=None, help="目标日期 YYYY-MM-DD，默认今天")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    args = parser.parse_args()

    # 确定日期
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        target_date = date.today()

    # 时间窗口：前一日 23:00 ~ 当日 23:00
    yesterday = target_date - timedelta(days=1)
    start_dt = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 0, 0)
    end_dt = datetime(target_date.year, target_date.month, target_date.day, 23, 0, 0)

    print(f"[INFO] 提取日期: {target_date}")
    print(f"[INFO] 时间窗口: {start_dt} ~ {end_dt}")

    # 查找 JSONL 文件
    jsonl_files = find_jsonl_files(start_dt, end_dt)
    print(f"[INFO] 找到 {len(jsonl_files)} 个 JSONL 文件")

    if not jsonl_files:
        print("[INFO] 今日无对话记录")
        if args.output:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(f"# QoderWork 对话日报 - {target_date.strftime('%Y-%m-%d')}\n\n")
                f.write(f"> 统计窗口：{start_dt.strftime('%Y-%m-%d %H:%M')} ~ {end_dt.strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write("*今日无对话记录。*\n")
        return

    # 去重
    sessions = deduplicate_by_session(jsonl_files)
    print(f"[INFO] 去重后 {len(sessions)} 个会话")

    # 解析每个会话
    sessions_data = []
    for sid, info in sessions.items():
        print(f"[INFO] 解析会话: {sid[:8]}... ({info['dir_name']})")
        session_info, conversations = parse_session(info["jsonl_path"], start_dt, end_dt)
        output_files = list_output_files(info["dir_name"], start_dt, end_dt)
        title = get_session_title(sid, info["dir_name"])

        # 跳过没有问答也没有文件的空会话
        if not conversations and not output_files:
            continue

        sessions_data.append({
            "session_id": sid,
            "session_info": session_info,
            "conversations": conversations,
            "output_files": output_files,
            "title": title,
        })

    # 按开始时间排序
    sessions_data.sort(key=lambda s: s["session_info"]["start_time"] or datetime.min)

    # 生成 Markdown
    markdown = generate_markdown(target_date, start_dt, end_dt, sessions_data)

    # 输出
    if args.output:
        output_path = args.output
    else:
        output_path = f"对话日报_{target_date.strftime('%Y-%m-%d')}.md"

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"[OK] 日报已保存: {output_path}")

    # 统计
    total_q = sum(len(s["conversations"]) for s in sessions_data)
    total_f = sum(len(s["output_files"]) for s in sessions_data)
    print(f"[STATS] {len(sessions_data)} 个会话, {total_q} 组问答, {total_f} 个产出文件")


if __name__ == "__main__":
    main()
