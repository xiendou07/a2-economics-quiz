# A2 Economics 刷题网站 · Cambridge 9708 Paper 3

一个在线刷 A2 经济选择题的网站：单题流、选完即时判分、显示正确答案，
带连击、进度记录，让刷题进入心流状态。

题库为 Cambridge 9708 Paper 3 (A Level Multiple Choice)，共 **15 份真题、450 题**。

👉 在线访问： **https://xiendou07.github.io/a2-economics-quiz/**

## 在线托管 (GitHub Pages)

网站文件在仓库根目录，已通过 GitHub Pages 部署。如需在自己的 fork 上开启：

1. 仓库 **Settings → Pages**
2. **Source** 选 `Deploy from a branch`
3. Branch 选 `main`，目录选 `/ (root)`，保存
4. 等一两分钟，即可通过 `https://<用户名>.github.io/<仓库名>/` 访问

## 本地运行

```bash
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

（题库通过 fetch 加载，必须用本地服务器，不能直接双击 html。）

## 题库生成流程

根目录的脚本用于从真题 PDF 生成题库（原始 PDF 不入库，见 `.gitignore`）：

| 脚本 | 作用 |
|---|---|
| `download_all.py` | 下载真题(qp)与答案(ms) PDF |
| `extract_answers.py` | 从 Mark Scheme 提取每题正确答案 |
| `slice_questions.py` | 把题目 PDF 按题切成单独图片 |
| `build_bank.py` | 合并答案与题图，生成 `questions.json` |

## 版权说明

题目与答案版权归 Cambridge Assessment International Education (UCLES) 所有，
本仓库仅供个人学习练习使用。
