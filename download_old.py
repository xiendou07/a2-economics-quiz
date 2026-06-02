#!/usr/bin/env python3
"""下载 2020-2023 的 Paper 3 题目(qp)+答案(ms)。
基于 probe_papers.py 探测出的存在清单(已剔除缺答案的 s21_31)。"""
import urllib.request, os, time

BASE = "https://bestexamhelp.com/exam/cambridge-international-a-level/economics-9708"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
headers = {"User-Agent": UA, "Accept": "application/pdf,*/*",
           "Referer": "https://bestexamhelp.com/"}
save_dir = os.path.dirname(os.path.abspath(__file__))

# (年份目录, 季+年, 变体) —— 来自探测结果, 全部 qp+ms 齐全
papers = [
    ("2020","m20","32"),
    ("2020","s20","31"),("2020","s20","32"),("2020","s20","33"),
    ("2020","w20","31"),("2020","w20","32"),("2020","w20","33"),
    ("2021","m21","32"),
    ("2021","s21","32"),("2021","s21","33"),   # s21_31 缺答案, 跳过
    ("2021","w21","31"),("2021","w21","32"),("2021","w21","33"),
    ("2022","m22","32"),
    ("2022","s22","31"),("2022","s22","32"),("2022","s22","33"),
    ("2022","w22","31"),("2022","w22","32"),("2022","w22","33"),
    ("2023","m23","32"),
    ("2023","s23","31"),("2023","s23","32"),("2023","s23","33"),
    ("2023","w23","31"),("2023","w23","32"),("2023","w23","33"),
]

def fetch(url, path, retries=3):
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if len(data) < 5000 or data[:5] != b"%PDF-":
                raise ValueError(f"非有效PDF(size={len(data)})")
            with open(path, "wb") as f: f.write(data)
            return len(data)
        except Exception:
            if a == retries-1: raise
            time.sleep(1.5)

ok, fail = [], []
for year, sy, v in papers:
    for kind in ("qp","ms"):
        fname = f"9708_{sy}_{kind}_{v}.pdf"
        url = f"{BASE}/{year}/{fname}"
        path = os.path.join(save_dir, fname)
        try:
            sz = fetch(url, path)
            print(f"✅ {fname} ({sz//1024} KB)"); ok.append(fname)
        except Exception as e:
            print(f"❌ {fname} — {e}"); fail.append((fname,url))
        time.sleep(0.4)

print(f"\n完成: {len(ok)} 成功, {len(fail)} 失败")
for f,u in fail: print(f"  失败 {f}\n        {u}")
