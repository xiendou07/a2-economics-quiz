#!/usr/bin/env python3
"""
把每份 qp (题目) PDF 按题切成单独图片。
思路: 用 PyMuPDF 在页面上搜索每个题号(1..30)作为锚点的 y 坐标,
相邻题号之间的纵向区间 = 该题的版面, 连同图表一起裁剪并渲染成 PNG。

输出:
  web/questions/<key>/q01.png ... q30.png   (key 如 9708_s24_31)
  questions_index.json  记录每题图片路径

需要人工注意: 个别卷子若题号定位有偏差, 脚本会打印告警。
"""
import os, re, json, glob
import fitz  # PyMuPDF

DIR = os.path.dirname(os.path.abspath(__file__))
OUT_ROOT = os.path.join(DIR, "questions")
os.makedirs(OUT_ROOT, exist_ok=True)

ZOOM = 2.0  # 渲染清晰度 (2x ~ 144dpi 起步, 清晰)
# 内容区左右留白裁剪比例(去掉页边的页眉页脚噪声靠 y 切, x 用整页宽度)
index = {}

def find_question_anchors(page):
    """在一页中找到形如 行首 '<num> ' 的题号锚点, 返回 [(qnum, y_top), ...].
    注意: 个别 PDF 把 '16' 这种两位数题号拆成 '1' '6' 两个 span,
    需要把行首左侧紧邻的数字 span 合并后再判断。"""
    anchors = []
    d = page.get_text("dict")
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            spans = sorted(line.get("spans", []), key=lambda s: s["bbox"][0])
            if not spans:
                continue
            x0 = spans[0]["bbox"][0]
            y0 = spans[0]["bbox"][1]
            if x0 >= page.rect.width * 0.18:
                continue  # 不在左边距, 不是题号
            # 从最左开始, 把连续的"纯数字"span 拼起来 (处理 '1'+'6'=16)
            digits = ""
            for sp in spans:
                t = sp["text"].strip()
                if t.isdigit() and len(digits) < 2:
                    digits += t
                else:
                    break
            if re.fullmatch(r"\d{1,2}", digits):
                n = int(digits)
                if 1 <= n <= 30:
                    anchors.append((n, y0, page.number))
    return anchors


def process_pdf(qp_path):
    fname = os.path.basename(qp_path)
    m = re.match(r'(9708)_([a-z]\d{2})_qp_(\d{2})\.pdf', fname)
    if not m:
        print(f"⚠️ 跳过命名异常: {fname}")
        return
    key = f"{m.group(1)}_{m.group(2)}_{m.group(3)}"
    out_dir = os.path.join(OUT_ROOT, key)
    os.makedirs(out_dir, exist_ok=True)

    doc = fitz.open(qp_path)

    # 收集所有页的题号锚点, 仅保留"按题号严格递增"的主序列
    raw = []
    for page in doc:
        raw.extend(find_question_anchors(page))

    # 过滤: 期望题号依次 1,2,3...30。逐个挑选第一个 >= 期望值的锚点
    anchors = []
    expected = 1
    for n, y, pno in raw:
        if n == expected:
            anchors.append((n, y, pno))
            expected += 1
        if expected > 30:
            break

    if len(anchors) < 30:
        print(f"⚠️ {key}: 只定位到 {len(anchors)} 题 (期望30) — 需检查")

    mat = fitz.Matrix(ZOOM, ZOOM)
    saved = {}
    for i, (qn, y_top, pno) in enumerate(anchors):
        # 该题底边 = 下一题顶边; 若下一题在别的页或没有则到页底
        if i + 1 < len(anchors):
            nqn, ny, npno = anchors[i + 1]
        else:
            nqn, ny, npno = None, None, None

        page = doc[pno]
        page_w = page.rect.width
        page_h = page.rect.height

        top = max(y_top - 6, 0)
        if ny is not None and npno == pno:
            bottom = min(ny - 2, page_h)
        else:
            bottom = page_h - 40  # 到页底(留点页脚)

        # 防御: bottom 必须大于 top
        if bottom <= top + 20:
            bottom = page_h - 40

        clip = fitz.Rect(30, top, page_w - 30, bottom)
        pix = page.get_pixmap(matrix=mat, clip=clip)
        rel = f"questions/{key}/q{qn:02d}.png"
        pix.save(os.path.join(DIR, rel))
        saved[str(qn)] = rel

    index[key] = saved
    doc.close()
    ok = "✅" if len(saved) == 30 else f"⚠️ {len(saved)}题"
    print(f"{ok} {key}: 切出 {len(saved)} 题图片")


for qp in sorted(glob.glob(os.path.join(DIR, "9708_*_qp_*.pdf"))):
    process_pdf(qp)

with open(os.path.join(DIR, "questions_index.json"), "w") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

total = sum(len(v) for v in index.values())
print(f"\n共 {len(index)} 份卷子, {total} 张题图 -> questions_index.json")
bad = {k: len(v) for k, v in index.items() if len(v) != 30}
if bad:
    print("⚠️ 题数不足30的卷子:", bad)
