# A2 Economics 刷题网站 (Cambridge 9708 · Paper 3)

在线刷 A2 经济选择题：单题流、选完即时判分、显示正确答案，带连击和进度记录。
题目与答案均来自官方真题 + Mark Scheme（共 15 份卷子，450 题）。

## 怎么打开

题库通过 `fetch` 加载，**必须用本地服务器打开**（直接双击 index.html 会因浏览器安全限制读不到题库）。

在 `web/` 目录下运行：

```bash
cd web
python3 -m http.server 8000
```

然后浏览器访问： http://localhost:8000

## 功能

- 🎲 **随机刷题**：从 450 题随机抽 30 题连续刷
- 🔁 **错题重练**：只刷做错过的题
- 📄 **按卷子练习**：选某一份真题（如 2025 May/June Paper 31）整卷练
- ⚡ 选完立即判分：正确选项绿色高亮，选错则同时标红你的选项
- 🔥 连击系统 + 实时进度条 + 正确率统计
- 💾 进度自动存在浏览器本地（localStorage）
- ⌨️ 键盘操作：按 A/B/C/D 选答案，回车/空格下一题
- 📱 手机端自适应

## 目录结构

```
web/
├── index.html          页面
├── style.css           样式
├── app.js              逻辑（判分、连击、存档）
├── questions.json      题库（题号/答案/题图路径，网站读这个）
└── questions/          450 张题图，按卷子分文件夹
```

## 题库是怎么生成的（在上级 Economics/ 目录）

1. `download_all.py` —— 从 bestexamhelp.com 下载 15 份题目(qp) + 15 份答案(ms) PDF
2. `extract_answers.py` —— 从 Mark Scheme 提取每题正确答案 → `answers.json`
3. `slice_questions.py` —— 把题目 PDF 按题切成单独图片 → `web/questions/`
4. `build_bank.py` —— 合并答案和题图 → `web/questions.json`

如需更换/新增题目，把新的 qp/ms PDF 放进 Economics/ 目录，依次重跑 2→3→4 即可。

## 关于「讲解」

CIE 官方 Mark Scheme 的选择题部分**只给字母答案，不含文字解析**，所以网站目前
显示「正确答案 + 来源」。若要补每题讲解，可在 `questions.json` 每题加一个
`"explain": "..."` 字段，`app.js` 已预留显示位置（fbExplain），会自动渲染。
