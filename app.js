/* ===================== A2 Economics 刷题 ===================== */
const SAVE_KEY = "a2econ_progress_v1";

let BANK = null;          // 完整题库
let session = null;       // 当前做题会话
let store = loadStore();  // 持久化进度

/* ---------- 持久化 ---------- */
function loadStore(){
  try{ return JSON.parse(localStorage.getItem(SAVE_KEY)) || newStore(); }
  catch(e){ return newStore(); }
}
function newStore(){
  return { results:{}, /* id -> {correct:bool, picks:int} */
           bestStreak:0, totalAnswered:0, totalCorrect:0 };
}
function saveStore(){ localStorage.setItem(SAVE_KEY, JSON.stringify(store)); }

/* ---------- 启动 ---------- */
init();
async function init(){
  try{
    const res = await fetch("questions.json");
    BANK = await res.json();
  }catch(e){
    document.body.innerHTML = '<p style="padding:40px;color:#fff">题库加载失败，请用本地服务器打开（见说明）。</p>';
    return;
  }
  renderHome();
  bindGlobal();
}

/* ---------- 首页 ---------- */
function renderHome(){
  document.getElementById("stTotal").textContent = BANK.meta.totalQuestions;
  const done = Object.keys(store.results).length;
  document.getElementById("stDone").textContent = done;
  const acc = store.totalAnswered ? Math.round(store.totalCorrect/store.totalAnswered*100) : null;
  document.getElementById("stAcc").textContent = acc===null ? "—" : acc+"%";
  document.getElementById("stBestStreak").textContent = store.bestStreak;

  // 卷子网格
  const grid = document.getElementById("paperGrid");
  grid.innerHTML = "";
  BANK.papers.forEach(p=>{
    const qsInPaper = BANK.questions.filter(q=>q.paper===p.key);
    const doneN = qsInPaper.filter(q=>store.results[q.id]).length;
    const pct = Math.round(doneN/qsInPaper.length*100);
    const el = document.createElement("button");
    el.className = "paper-card";
    el.innerHTML = `
      <div class="pc-name">${p.name}</div>
      <div class="pc-meta"><span>${p.count} 题</span><span>${doneN}/${p.count}</span></div>
      <div class="pc-bar"><i style="width:${pct}%"></i></div>`;
    el.onclick = ()=> startSession(qsInPaper, p.name, false);
    grid.appendChild(el);
  });
  showScreen("home");
}

function bindGlobal(){
  document.querySelectorAll(".mode-card").forEach(b=>{
    b.onclick = ()=>{
      const m = b.dataset.mode;
      if(m==="random-all"){
        startSession(shuffle([...BANK.questions]).slice(0,30), "随机刷题", true);
      }else if(m==="wrong"){
        const wrong = BANK.questions.filter(q=>store.results[q.id] && !store.results[q.id].correct);
        if(!wrong.length){ alert("还没有错题，先去刷几道吧！"); return; }
        startSession(shuffle(wrong), "错题重练", true);
      }
    };
  });
  document.getElementById("backBtn").onclick = ()=>{ saveStore(); renderHome(); };
  document.getElementById("resetBtn").onclick = ()=>{
    if(confirm("确定清空所有进度和统计？此操作不可恢复。")){
      store = newStore(); saveStore(); renderHome();
    }
  };
  document.getElementById("nextBtn").onclick = nextQuestion;
  document.getElementById("againBtn").onclick = ()=>
    startSession(shuffle([...BANK.questions]).slice(0,30), "随机刷题", true);
  document.getElementById("homeBtn").onclick = renderHome;

  // 键盘: A/B/C/D 选项, 回车/空格下一题
  document.addEventListener("keydown", e=>{
    if(document.getElementById("quiz").classList.contains("hidden")) return;
    const k = e.key.toUpperCase();
    if(["A","B","C","D"].includes(k) && !session.answered){
      pickOption(k);
    }else if((e.key==="Enter"||e.key===" ") && session.answered){
      e.preventDefault(); nextQuestion();
    }
  });
}

/* ---------- 会话 ---------- */
function startSession(questions, name, isRandom){
  session = { list:questions, idx:0, name, isRandom,
              streak:0, bestStreak:0, correct:0, answered:false };
  showScreen("quiz");
  loadQuestion();
}

function loadQuestion(){
  session.answered = false;
  const q = session.list[session.idx];
  document.getElementById("qPaperName").textContent = q.paperName;
  document.getElementById("qNumber").textContent = "Q" + q.q;
  const img = document.getElementById("qImg");
  img.src = q.img;
  // 进度
  const total = session.list.length;
  document.getElementById("progText").textContent = `${session.idx+1} / ${total}`;
  document.getElementById("progFill").style.width = (session.idx/total*100)+"%";
  document.getElementById("streakNum").textContent = session.streak;

  // 重置选项
  document.querySelectorAll(".opt").forEach(o=>{
    o.className = "opt";
    o.disabled = false;
    o.onclick = ()=> pickOption(o.dataset.opt);
  });
  document.getElementById("feedback").classList.add("hidden");
  window.scrollTo({top:0, behavior:"smooth"});
}

function pickOption(letter){
  if(session.answered) return;
  session.answered = true;
  const q = session.list[session.idx];
  const correct = letter === q.answer;

  // 高亮
  document.querySelectorAll(".opt").forEach(o=>{
    o.disabled = true;
    if(o.dataset.opt === q.answer) o.classList.add("correct");
    if(o.dataset.opt === letter && !correct){ o.classList.add("wrong","shake"); }
  });

  // streak
  if(correct){
    session.streak++; session.correct++;
    session.bestStreak = Math.max(session.bestStreak, session.streak);
    if(session.streak>=3){
      const sb=document.getElementById("streakBox");
      sb.classList.add("hot"); setTimeout(()=>sb.classList.remove("hot"),500);
    }
  }else{
    session.streak = 0;
  }
  document.getElementById("streakNum").textContent = session.streak;

  // 全局统计 & 存档(每题只首次计入正确率)
  if(!store.results[q.id]){
    store.totalAnswered++;
    if(correct) store.totalCorrect++;
  }
  store.results[q.id] = { correct, picks:(store.results[q.id]?.picks||0)+1 };
  store.bestStreak = Math.max(store.bestStreak, session.bestStreak);
  saveStore();

  // 反馈
  const fb = document.getElementById("feedback");
  const head = document.getElementById("fbHead");
  head.textContent = correct ? streakMsg(session.streak) : "❌ 答错了";
  head.className = "fb-head " + (correct ? "ok":"no");
  document.getElementById("fbAnswer").textContent = q.answer;
  document.getElementById("fbExplain").textContent =
    `来源：${q.paperName} 第 ${q.q} 题。` +
    (correct ? "" : " 看清正确选项的逻辑，再做一次类似题巩固。");
  fb.classList.remove("hidden");
  document.getElementById("progFill").style.width = ((session.idx+1)/session.list.length*100)+"%";
}

function streakMsg(s){
  if(s>=10) return `🔥🔥 ${s} 连击！太强了！`;
  if(s>=5)  return `🔥 ${s} 连击！手感火热！`;
  if(s>=3)  return `✅ 答对！${s} 连击`;
  return "✅ 答对了！";
}

function nextQuestion(){
  session.idx++;
  if(session.idx >= session.list.length){ finishSession(); return; }
  loadQuestion();
}

function finishSession(){
  showScreen("result");
  const total = session.list.length;
  const acc = Math.round(session.correct/total*100);
  document.getElementById("resScore").textContent = `${session.correct}/${total}`;
  document.getElementById("resAcc").textContent = acc+"%";
  document.getElementById("resStreak").textContent = session.bestStreak;
  document.getElementById("resTitle").textContent =
    acc>=90 ? "🏆 出色！" : acc>=70 ? "🎉 不错！" : acc>=50 ? "💪 继续加油！" : "📚 多练练！";
}

/* ---------- 工具 ---------- */
function showScreen(id){
  ["home","quiz","result"].forEach(s=>
    document.getElementById(s).classList.toggle("hidden", s!==id));
}
function shuffle(a){
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
}
