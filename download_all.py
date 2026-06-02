#!/usr/bin/env python3
"""
从 bestexamhelp.com 批量下载 9708 Economics Paper 3 (A2 MCQ) 的
题目(qp) 和 答案(ms)。文件保存到脚本所在目录。
"""

import urllib.request
import os
import time

BASE = "https://bestexamhelp.com/exam/cambridge-international-a-level/economics-9708"

# (年份目录, 文件名)  —— qp=题目, ms=答案
# 注意: m25 = 2025年3月卷, s25/s24 = May/June, w24/w25 = Oct/Nov
codes = [
    ("2025", "9708_m25_32"),
    ("2024", "9708_s24_31"), ("2024", "9708_s24_32"), ("2024", "9708_s24_33"),
    ("2025", "9708_s25_31"), ("2025", "9708_s25_32"),
    ("2025", "9708_s25_33"), ("2025", "9708_s25_34"),
    ("2024", "9708_w24_31"), ("2024", "9708_w24_32"), ("2024", "9708_w24_33"),
    ("2025", "9708_w25_31"), ("2025", "9708_w25_32"),
    ("2025", "9708_w25_33"), ("2025", "9708_w25_34"),
]

save_dir = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
headers = {"User-Agent": UA, "Accept": "application/pdf,*/*",
           "Referer": "https://bestexamhelp.com/"}


def fetch(url, save_path, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if len(data) < 5000 or not data[:5] == b"%PDF-":
                raise ValueError(f"不是有效PDF (size={len(data)})")
            with open(save_path, "wb") as f:
                f.write(data)
            return len(data)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(1.5)
    return 0


success, failed = [], []
for year, code in codes:
    for kind in ("qp", "ms"):
        fname = f"{code[:9]}_{kind}{code[9:]}.pdf"  # 9708_s25_qp_31.pdf
        # code 形如 9708_s25_31 -> 拆成 9708_s25_ + qp/ms + _31
        prefix, num = code.rsplit("_", 1)
        fname = f"{prefix}_{kind}_{num}.pdf"
        url = f"{BASE}/{year}/{fname}"
        save_path = os.path.join(save_dir, fname)
        try:
            sz = fetch(url, save_path)
            print(f"✅ {fname} ({sz//1024} KB)")
            success.append(fname)
        except Exception as e:
            print(f"❌ {fname} — {e}")
            failed.append((fname, url))
        time.sleep(0.4)

print(f"\n完成：{len(success)} 成功，{len(failed)} 失败")
for fname, url in failed:
    print(f"  失败 {fname}\n        {url}")
