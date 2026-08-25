---
name: wechat-article-monitor
description: Operate the local WeChat official-account article monitoring app (公众号文章监测/公众号检索). Start/stop the Flask server, check credentials, run monitoring for accounts, batch-import accounts, download articles as Markdown, and diagnose WeChat API errors (freq control, invalid session). Use when the user mentions 公众号监测, 公众号文章, wechat-article-detection, or asks to fetch/monitor/download articles from WeChat official accounts.
---

# WeChat Article Monitor (公众号文章监测助手)

Local Flask app (origin: wechat-article-detection extension by 子晓, ported to Flask + SQLite).
Project dir: `D:\python\trae\program\1 个人项目\公众号检索项目\wechat-article-detection`
URL: `http://127.0.0.1:8061`

## Quick Start

1. Check server: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8061/`
2. If not `200`, start it (see "Server Management").
3. Check credentials before monitoring (see "Credentials").
4. Call APIs per task (see "API Reference").

## Server Management

**Start** (background, from project dir):
```bash
cd "/d/python/trae/program/1 个人项目/公众号检索项目/wechat-article-detection" && /c/Python314/python.exe app.py
```

**Restart after code changes** (Python source is cached; template changes also need restart):
```bash
netstat -ano | grep ":8061" | grep LISTENING   # get PID
taskkill //F //PID <PID>                        # bash needs //PID
# then start again
```

Known trap: two processes can both LISTEN on the same port on Windows — kill ALL listeners and confirm only one remains.

## Credentials

Credentials (token + cookie) live in SQLite via `/api/storage`. They expire; WeChat rate-limits per session.

**Check status** (two-layer probe: search layer + article-list layer):
```bash
curl -s -X POST http://127.0.0.1:8061/api/check-credentials
```
Status values: `OK` (all good) / `FREQ_CONTROL` (rate-limited, NOT banned — wait 10-30 min, or re-login for a fresh session) / `SESSION_EXPIRED` (re-login needed) / `MISSING` / `NETWORK`.

**Re-login**: the human must scan a QR code. Open `http://127.0.0.1:8061` in a browser and tell the user to click 「🤖 扫码登录」and scan with WeChat. QR session lives in server memory — if the server restarted, a new scan is needed. Rate limits follow the session: a fresh login often bypasses an old session's freq control.

## API Reference

All POST endpoints take JSON. Account names are Chinese — send requests via a Python script file (bash inline `curl -d` with Chinese breaks encoding on this machine).

**Monitor one account** (returns articles or structured error with code/desc/hint):
```python
import json, urllib.request
req = urllib.request.Request('http://127.0.0.1:8061/api/monitor',
    data=json.dumps({'account': '人民日报', 'days': 7}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}, method='POST')
print(urllib.request.urlopen(req, timeout=120).read().decode('utf-8'))
```
`days`: 1/3/7/30. Error `code` values: `FREQ_CONTROL`, `SESSION_EXPIRED`, `NO_PERMISSION`, `ACCOUNT_BLOCKED`, `NETWORK`, `LOCAL`.

**Add accounts** (single or batch) — write to storage directly:
```python
import json, urllib.request
# GET /api/storage → read accounts array, append {name, catId}, POST back whole object
```
Account shape: `{"name": "人民日报", "catId": "cat_123"}` or `catId: "__uncategorized__"`.
Categories shape: `[{"id": "cat_<timestamp>", "name": "量化"}]`.

**Storage**: `GET /api/storage` returns all state; `POST /api/storage` (JSON object) upserts keys; `POST /api/storage/clear` wipes everything.

**Article download** (fetch page, extract to Markdown):
```python
req = urllib.request.Request('http://127.0.0.1:8061/api/article',
    data=json.dumps({'link': '<article url>'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}, method='POST')
```

**QR login endpoints** (normally driven by the web UI; the user must scan — do not poll aggressively): `POST /api/qr/start`, `GET /api/qr/poll?qr_id=...`.

## Diagnosis Cheat Sheet

| WeChat returns | Meaning | Action |
|---|---|---|
| `freq control` | Rate-limited (NOT banned) | Wait 10-30 min; or fresh login (new session resets it) |
| `invalid session` / `invalid csrf` | Credentials expired | Re-login via QR |
| `no permission` | Account lacks API rights | Use a different (subscription) account |
| `invalid referrer` | HTTP Referer header missing | Code bug, check requests headers |

Frequency discipline: WeChat's article-list API is strictly limited. Don't re-test repeatedly (each probe consumes quota); page interval is 1.2s, account interval 1.5s in the app; frontend auto-retries once after 65s on freq control.

## Data

SQLite at `<project>/data/app.db`, table `storage` (key-value JSON). Export/import of config available in the web UI (管理公众号 → 导出/导入配置).

## Conventions

- All code changes must be git-committed (repo: `main` branch in project dir).
- UI is SkillHub-style; keep modifications consistent with the existing design tokens.
- This machine: python is `/c/Python314/python.exe` in bash, `C:\Python314\python.exe` elsewhere; PowerShell mangles Chinese paths — prefer Python scripts for file ops on Chinese paths.
