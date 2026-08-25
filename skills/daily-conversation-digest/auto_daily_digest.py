#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日对话日报 - 自动提取 + Git 推送
直接运行，无需 AI 参与，零积分消耗。
支持多机器各自运行，推送到同一个 GitHub 私有仓库归集。

使用方式：
  1. 克隆私有仓库到本地（首次）：
     git clone https://github.com/<你的用户名>/daily-digest.git ~/.qoderwork/daily-digest-repo
  2. 设置 Windows 计划任务每天 23:00 运行本脚本：
     schtasks /create /tn "QoderWork-DailyDigest" /tr "pythonw auto_daily_digest.py" /sc daily /st 23:00

可选：在同目录下创建 config.json 自定义路径：
  { "repo_dir": "D:/path/to/daily-digest-repo" }
"""

import os
import sys
import json
import socket
import subprocess
from datetime import datetime, date
from pathlib import Path

# ---- 路径配置 ----
SKILL_DIR = Path.home() / ".qoderwork" / "skills" / "daily-conversation-digest"
EXTRACT_SCRIPT = SKILL_DIR / "extract.py"
LOG_FILE = Path.home() / ".qoderwork" / "logs" / "daily-digest.log"
MACHINE_NAME = socket.gethostname()


def find_repo_dir() -> Path:
    """
    自动查找 daily-digest 仓库目录，优先级：
    1. config.json 中指定的路径
    2. ~/.qoderwork/daily-digest-repo（推荐标准位置）
    3. ~/.qoderwork/workspace/ 下第一个含 .git 的 daily-digest-repo 目录
    """
    # 1. 读配置文件
    config_file = SKILL_DIR / "config.json"
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            repo = cfg.get("repo_dir")
            if repo and Path(repo).exists():
                return Path(repo)
        except Exception:
            pass

    # 2. 标准位置
    standard = Path.home() / ".qoderwork" / "daily-digest-repo"
    if standard.exists() and (standard / ".git").exists():
        return standard

    # 3. 搜索 workspace 目录
    workspace_base = Path.home() / ".qoderwork" / "workspace"
    if workspace_base.exists():
        for d in workspace_base.iterdir():
            if d.is_dir() and "daily-digest" in d.name and (d / ".git").exists():
                return d

    # 4. 默认返回标准位置（即使不存在，后续会提示）
    return standard


def log(msg: str):
    """写日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{MACHINE_NAME}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    today = date.today()
    log(f"=== 开始生成日报: {today} ===")

    # 0. 定位仓库
    REPO_DIR = find_repo_dir()
    if not REPO_DIR.exists():
        log(f"仓库目录不存在: {REPO_DIR}")
        log("请先克隆私有仓库：git clone https://github.com/<用户名>/daily-digest.git " + str(REPO_DIR))
        return

    # 1. 确定输出路径
    year_month = today.strftime("%Y/%m")
    out_dir = REPO_DIR / year_month
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{today.strftime('%Y-%m-%d')}.md"

    # 2. 运行提取脚本
    if not EXTRACT_SCRIPT.exists():
        log(f"提取脚本不存在: {EXTRACT_SCRIPT}")
        return

    cmd = [
        sys.executable,
        str(EXTRACT_SCRIPT),
        "--date", today.strftime("%Y-%m-%d"),
        "--output", str(out_file),
    ]
    log(f"执行: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        log(f"提取脚本输出:\n{result.stdout}")
        if result.stderr:
            log(f"提取脚本警告:\n{result.stderr}")
        if result.returncode != 0:
            log(f"提取脚本失败，退出码: {result.returncode}")
            return
    except subprocess.TimeoutExpired:
        log("提取脚本超时（120秒）")
        return
    except Exception as e:
        log(f"执行提取脚本异常: {e}")
        return

    # 3. 检查输出文件
    if not out_file.exists() or out_file.stat().st_size == 0:
        log("未生成有效日报文件，跳过提交")
        return

    log(f"日报已生成: {out_file} ({out_file.stat().st_size} bytes)")

    # 4. Git 提交 + 推送
    os.chdir(str(REPO_DIR))

    # 先 pull --rebase 防止冲突（两台机器可能同时 push）
    env = os.environ.copy()
    env["GIT_SSL_NO_VERIFY"] = "true"
    try:
        pull_result = subprocess.run(
            ["git", "pull", "--rebase"],
            capture_output=True, text=True, encoding="utf-8",
            env=env,
            timeout=30,
        )
        if pull_result.returncode != 0:
            log(f"Git pull 失败（继续尝试）: {pull_result.stderr}")
    except Exception as e:
        log(f"Git pull 异常（继续尝试）: {e}")

    # 检查是否有变更
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, encoding="utf-8"
    )
    if not status.stdout.strip():
        log("无变更，跳过提交")
        return

    subprocess.run(["git", "add", "."], check=True)
    commit_msg = f"daily: {today} from {MACHINE_NAME}"
    subprocess.run(
        ["git", "commit", "-m", commit_msg],
        check=True,
        capture_output=True, text=True, encoding="utf-8"
    )
    log("Git commit 完成")

    # 推送
    try:
        push_result = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True, encoding="utf-8",
            env=env,
            timeout=60,
        )
        if push_result.returncode == 0:
            log("Git push 成功")
        else:
            log(f"Git push 失败: {push_result.stderr}")
    except subprocess.TimeoutExpired:
        log("Git push 超时")
    except Exception as e:
        log(f"Git push 异常: {e}")

    log(f"=== 完成 ===\n")


if __name__ == "__main__":
    main()
