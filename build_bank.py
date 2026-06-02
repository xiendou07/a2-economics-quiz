#!/usr/bin/env python3
"""
合并 题图索引(questions_index.json) + 答案(answers.json)
=> web/questions.json  (网站直接读取的题库)

每题结构:
{
  "id": "9708_s24_31_q1",
  "paper": "9708_s24_31",
  "paperName": "2024 May/June · Paper 31",
  "q": 1,
  "img": "questions/9708_s24_31/q01.png",
  "answer": "B"
}
"""
import os, json, re

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, "web", "questions_index.json")) as f:
    qindex = json.load(f)
with open(os.path.join(DIR, "answers.json")) as f:
    answers = json.load(f)

SERIES = {"m": "March", "s": "May/June", "w": "Oct/Nov"}

def nice_name(key):
    # 9708_s24_31 -> 2024 May/June · Paper 31
    m = re.match(r"9708_([a-z])(\d{2})_(\d{2})", key)
    s, yy, pp = m.group(1), m.group(2), m.group(3)
    return f"20{yy} {SERIES.get(s, s)} · Paper {pp}"

bank = []
missing_answer = 0
for key in sorted(qindex.keys()):
    imgs = qindex[key]
    ans = answers.get(key, {})
    for qn in range(1, 31):
        sq = str(qn)
        if sq not in imgs:
            continue
        a = ans.get(sq)
        if a is None:
            missing_answer += 1
            print(f"⚠️ 缺答案: {key} 第{qn}题")
            continue
        bank.append({
            "id": f"{key}_q{qn}",
            "paper": key,
            "paperName": nice_name(key),
            "q": qn,
            "img": imgs[sq],
            "answer": a,
        })

papers = sorted({b["paper"] for b in bank})
out = {
    "meta": {
        "subject": "Cambridge A Level Economics 9708 — Paper 3 (A2 Multiple Choice)",
        "totalQuestions": len(bank),
        "totalPapers": len(papers),
    },
    "papers": [{"key": p, "name": nice_name(p),
                "count": sum(1 for b in bank if b["paper"] == p)} for p in papers],
    "questions": bank,
}

with open(os.path.join(DIR, "web", "questions.json"), "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"✅ 题库生成: {len(bank)} 题, {len(papers)} 份卷子 -> web/questions.json")
if missing_answer:
    print(f"⚠️ 有 {missing_answer} 题缺答案")
