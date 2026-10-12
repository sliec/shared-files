# -*- coding: utf-8 -*-
"""佣金与两费确认生成器 - 本地 Web 服务（端口 5274）

用法：python app.py  →  浏览器打开 http://127.0.0.1:5274
依赖：flask pandas xlrd openpyxl（可选 pywin32 用于公式重算）
"""
import os
import json
import glob
import shutil
import zipfile
import tempfile
import urllib.request
from datetime import datetime

from flask import Flask, request, jsonify, render_template, send_file

import core

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "outputs")
CFG_PATH = os.path.join(BASE, "config.json")
os.makedirs(OUT_DIR, exist_ok=True)

DEFAULT_CFG = {
    "api_key": "",
    "base_url": "https://api.siliconflow.cn/v1",
    "output_dir": os.path.join(os.path.expanduser("~"), "Desktop"),
    "manager": "大成基金管理有限公司",
}

app = Flask(__name__)


def load_cfg():
    cfg = dict(DEFAULT_CFG)
    if os.path.exists(CFG_PATH):
        try:
            with open(CFG_PATH, encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception:
            pass
    return cfg


def save_cfg(cfg):
    with open(CFG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    balance = [f for f in request.files.getlist("balance") if f.filename]
    prev = [f for f in request.files.getlist("prev") if f.filename]
    if not balance:
        return jsonify({"ok": False, "error": "请至少上传一个余额表 .xls 文件"}), 400

    cfg = load_cfg()
    out_dir = request.form.get("out_dir") or cfg.get("output_dir") or \
        os.path.join(os.path.expanduser("~"), "Desktop")

    tmp = tempfile.mkdtemp(prefix="yjlfee_")
    saved_balance, saved_prev, log = [], [], []
    try:
        for f in balance:
            p = os.path.join(tmp, os.path.basename(f.filename))
            f.save(p)
            saved_balance.append(p)
        for f in prev:
            p = os.path.join(tmp, os.path.basename(f.filename))
            f.save(p)
            saved_prev.append(p)

        try:
            results, files = core.generate(saved_balance, saved_prev, out_dir)
        except Exception as e:
            return jsonify({"ok": False, "error": f"生成失败：{e}"}), 500

        # 同步一份到 outputs 供页面下载
        dl = []
        for src in files:
            dst = os.path.join(OUT_DIR, os.path.basename(src))
            try:
                shutil.copy2(src, dst)
                dl.append(os.path.basename(src))
            except Exception:
                dl.append(os.path.basename(src))

        log = []
        for r in results:
            if r["comm_rows"]:
                note = f"佣金 {r['comm_rows']} 家券商，合计 {r['comm_total']:,.2f}，席位带出 {r['seats_matched']}"
            else:
                note = "本季无应付佣金明细，佣金 sheet 留空占位"
            log.append({
                "code": r["code"], "display": r["display"], "period": r["period"],
                "title": r["title"], "cust_fee": r["cust_fee"], "mgmt_fee": r["mgmt_fee"],
                "comm_rows": r["comm_rows"], "comm_total": r["comm_total"],
                "seats_matched": r["seats_matched"], "note": note,
                "file": r["file"],
            })
        return jsonify({"ok": True, "results": log,
                        "out_dir": os.path.abspath(out_dir), "files": dl})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@app.route("/download/<path:fname>")
def download(fname):
    p = os.path.join(OUT_DIR, fname)
    if not os.path.isfile(p):
        return "文件不存在", 404
    return send_file(p, as_attachment=True, download_name=fname)


@app.route("/api/zip")
def api_zip():
    files = sorted(glob.glob(os.path.join(OUT_DIR, "*.xlsx")),
                   key=os.path.getmtime, reverse=True)
    if not files:
        return "无文件", 404
    zp = os.path.join(OUT_DIR, "佣金与两费确认_全部.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, os.path.basename(f))
    return send_file(zp, as_attachment=True,
                     download_name=f"佣金与两费确认_{datetime.now():%Y%m%d_%H%M}.zip")


@app.route("/api/settings", methods=["GET", "POST"])
def api_settings():
    cfg = load_cfg()
    if request.method == "POST":
        data = request.get_json(force=True)
        for k in ("api_key", "base_url", "output_dir", "manager"):
            if k in data:
                cfg[k] = str(data[k]).strip()
        save_cfg(cfg)
        return jsonify({"ok": True})
    # 返回时 key 打码
    show = dict(cfg)
    if show.get("api_key"):
        k = show["api_key"]
        show["api_key_masked"] = k[:5] + "*" * (len(k) - 9) + k[-4:] if len(k) > 12 else "***"
    show["api_key"] = ""
    return jsonify(show)


@app.route("/api/test_key", methods=["POST"])
def api_test_key():
    """测试 API key 连通性（核心生成不依赖此 key，仅用于未来 AI 辅助功能）"""
    cfg = load_cfg()
    data = request.get_json(force=True) if request.data else {}
    key = data.get("api_key") or cfg.get("api_key")
    base = data.get("base_url") or cfg.get("base_url", "").rstrip("/")
    if not key or not base:
        return jsonify({"ok": False, "error": "未配置 API key 或 base_url"})
    try:
        req = urllib.request.Request(base + "/models",
                                     headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return jsonify({"ok": resp.status == 200, "status": resp.status})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


if __name__ == "__main__":
    print("佣金与两费确认生成器  http://127.0.0.1:5274")
    app.run(host="127.0.0.1", port=5274, debug=False)
