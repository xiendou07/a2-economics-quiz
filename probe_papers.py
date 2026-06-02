#!/usr/bin/env python3
"""探测 bestexamhelp 上 2020-2023 各 Paper 3 (qp+ms) 是否存在。
只发 HEAD 请求, 不下载。输出存在的卷子清单。"""
import urllib.request, time

BASE = "https://bestexamhelp.com/exam/cambridge-international-a-level/economics-9708"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# 考季代码: m=Feb/March(仅印度), s=May/June, w=Oct/Nov
# Paper 3 变体: 31,32,33 (偶尔34)
years = ["2020", "2021", "2022", "2023"]
seasons = {"m": "March", "s": "MayJune", "w": "OctNov"}
variants = ["31", "32", "33", "34"]

def exists(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False

found = []
for y in years:
    ycode = y[2:]  # 2020 -> 20
    for s in seasons:
        for v in variants:
            qp = f"9708_{s}{ycode}_qp_{v}.pdf"
            url = f"{BASE}/{y}/{qp}"
            if exists(url):
                # 同时确认答案也在
                ms = f"9708_{s}{ycode}_ms_{v}.pdf"
                has_ms = exists(f"{BASE}/{y}/{ms}")
                tag = "qp+ms" if has_ms else "qp only(无答案!)"
                print(f"✅ {s}{ycode} P{v}  [{tag}]")
                found.append((y, f"9708_{s}{ycode}_{v}", has_ms))
            time.sleep(0.15)

print(f"\n找到 {len(found)} 份 Paper 3 (2020-2023)")
no_ms = [f[1] for f in found if not f[2]]
if no_ms:
    print("⚠️ 缺答案的:", no_ms)
