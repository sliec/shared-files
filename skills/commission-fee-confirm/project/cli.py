# -*- coding: utf-8 -*-
"""命令行入口：python cli.py <余额表.xls ...> [--prev 上季佣金明细.xlsx ...] [--out 输出目录]"""
import sys
import argparse
import io

if sys.stdout and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import core


def main():
    ap = argparse.ArgumentParser(description="佣金与两费确认文件生成器")
    ap.add_argument("balance", nargs="+", help="余额表 .xls 文件（可多个）")
    ap.add_argument("--prev", nargs="*", default=[], help="上季应付佣金明细 .xlsx（可选，提供席位号）")
    ap.add_argument("--out", default=None, help="输出目录（默认桌面）")
    a = ap.parse_args()

    results, files = core.generate(a.balance, a.prev, a.out)
    for r in results:
        print(f"[{r['code']}] {r['display']}  {r['period']}")
        print(f"    托管费 {r['cust_fee']:,.2f} | 管理费 {r['mgmt_fee']:,.2f} | "
              f"佣金 {r['comm_rows']} 家券商 合计 {r['comm_total']:,.2f} (席位匹配 {r['seats_matched']})")
        print(f"    → {r['file']}")
    print(f"\n共生成 {len(files)} 个文件")


if __name__ == "__main__":
    main()
