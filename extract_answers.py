#!/usr/bin/env python3
"""
从所有 mark scheme (ms) PDF 中提取每题正确答案 (ABCD)。
输出 answers.json: { "9708_s24_31": {"1":"B","2":"C",...}, ... }
答案表行格式: "<题号> <字母> 1"
"""
import os, re, json, glob
from pypdf import PdfReader

DIR = os.path.dirname(os.path.abspath(__file__))
out = {}

# 行匹配: 题号(1-30) 空格 答案字母(A-D) 空格 分值(通常1)
row_re = re.compile(r'^\s*(\d{1,2})\s+([A-D])\s+\d\s*$')

for ms_path in sorted(glob.glob(os.path.join(DIR, "9708_*_ms_*.pdf"))):
    fname = os.path.basename(ms_path)
    # 9708_s24_ms_31.pdf -> key 9708_s24_31
    m = re.match(r'(9708)_([a-z]\d{2})_ms_(\d{2})\.pdf', fname)
    if not m:
        print(f"⚠️  跳过命名异常: {fname}")
        continue
    key = f"{m.group(1)}_{m.group(2)}_{m.group(3)}"

    reader = PdfReader(ms_path)
    text = "\n".join(p.extract_text() or "" for p in reader.pages)

    ans = {}
    for line in text.splitlines():
        rm = row_re.match(line)
        if rm:
            q = int(rm.group(1))
            if 1 <= q <= 30:
                ans[str(q)] = rm.group(2)

    out[key] = ans
    status = "✅" if len(ans) == 30 else f"⚠️ 只有{len(ans)}题"
    print(f"{status} {key}: {len(ans)} 个答案")

with open(os.path.join(DIR, "answers.json"), "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

total = sum(len(v) for v in out.values())
print(f"\n共 {len(out)} 份卷子, {total} 个答案 -> answers.json")
# 报告不完整的卷子
bad = {k: len(v) for k, v in out.items() if len(v) != 30}
if bad:
    print("⚠️ 不足30题的卷子:", bad)
