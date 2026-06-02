#!/usr/bin/env python3
"""
下载 9708 Economics Mark Schemes
从 GCE Guide 批量下载，文件保存到脚本所在目录
"""

import urllib.request
import os
import time

BASE_URL = "https://papers.gceguide.com/A%20Levels/Economics%20(9708)"

# 所有需要下载的 mark schemes（qp → ms）
files = [
    ("2025", "9708_m25_ms_32.pdf"),
    ("2024", "9708_s24_ms_31.pdf"),
    ("2024", "9708_s24_ms_32.pdf"),
    ("2024", "9708_s24_ms_33.pdf"),
    ("2025", "9708_s25_ms_31.pdf"),
    ("2025", "9708_s25_ms_32.pdf"),
    ("2025", "9708_s25_ms_33.pdf"),
    ("2025", "9708_s25_ms_34.pdf"),
    ("2024", "9708_w24_ms_31.pdf"),
    ("2024", "9708_w24_ms_32.pdf"),
    ("2024", "9708_w24_ms_33.pdf"),
    ("2025", "9708_w25_ms_31.pdf"),
    ("2025", "9708_w25_ms_32.pdf"),
    ("2025", "9708_w25_ms_33.pdf"),
    ("2025", "9708_w25_ms_34.pdf"),
]

save_dir = os.path.dirname(os.path.abspath(__file__))
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

success, failed = [], []

for year, filename in files:
    url = f"{BASE_URL}/{year}/{filename}"
    save_path = os.path.join(save_dir, filename)

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 1000:
            raise ValueError("文件太小，可能不存在")
        with open(save_path, "wb") as f:
            f.write(data)
        print(f"✅ {filename} ({len(data)//1024} KB)")
        success.append(filename)
    except Exception as e:
        print(f"❌ {filename} — {e}")
        failed.append(filename)

    time.sleep(0.5)  # 避免请求过快

print(f"\n完成：{len(success)} 成功，{len(failed)} 失败")
if failed:
    print("失败的文件：")
    for f in failed:
        print(f"  {f}")
