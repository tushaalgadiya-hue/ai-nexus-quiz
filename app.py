"""
AI NEXUS - Search & Agents Command Center
Interactive quiz game + Search Lab for DSC401-6 Artificial Intelligence (Units I & II)
Run with:   python -m streamlit run app.py
"""
import json
import math
import random
import re
import time
from datetime import datetime

import pandas as pd
import streamlit as st

import labs
from questions import QUESTIONS, TOPICS, TOPIC_REF, ZONES

st.set_page_config(page_title="AI NEXUS | Search & Agents Command Center", page_icon="⚡", layout="wide",
                   initial_sidebar_state="expanded")

LB_FILE = "leaderboard.json"
POINTS = {"Easy": 10, "Medium": 20, "Hard": 30}
TIME_LIMIT = {"Easy": 40, "Medium": 60, "Hard": 90}
HINT_PENALTY, RISK_LOSS = 5, 10

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=JetBrains+Mono:wght@400;600&display=swap');
:root{--cy:#00e5ff;--pk:#ff2bd6;--vi:#7c4dff;--bg:#070b18;--card:rgba(16,26,51,.68);--ok:#7ee787;--bad:#ff5c7a;--am:#ffd166;}
.stApp{background:radial-gradient(1100px 560px at 8% -8%,rgba(0,229,255,.14),transparent 60%),
 radial-gradient(900px 520px at 100% 0%,rgba(255,43,214,.11),transparent 55%),var(--bg);font-family:'Segoe UI',Roboto,Arial,sans-serif;}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
 background-image:linear-gradient(rgba(0,229,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(0,229,255,.045) 1px,transparent 1px);
 background-size:46px 46px;-webkit-mask-image:radial-gradient(ellipse at top,#000 25%,transparent 75%);mask-image:radial-gradient(ellipse at top,#000 25%,transparent 75%);}
footer,#MainMenu,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
header[data-testid="stHeader"]{background:transparent;}
section[data-testid="stSidebar"]{background:rgba(9,14,32,.96);border-right:1px solid rgba(0,229,255,.22);}
.bigscore{font:900 2.3rem Orbitron,sans-serif;color:#fff;line-height:1.1;}
.block-container{max-width:1180px;padding-top:1rem;position:relative;z-index:1;}
h1,h2,h3,h4{font-family:'Orbitron',sans-serif!important;letter-spacing:.5px;}
.hud{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 18px;margin-bottom:14px;border-radius:14px;
 background:var(--card);border:1px solid rgba(0,229,255,.28);box-shadow:0 0 28px rgba(0,229,255,.08);backdrop-filter:blur(8px);}
.brand{font-family:'Orbitron';font-weight:900;font-size:1.25rem;color:#fff;letter-spacing:2px;}
.brand span{background:linear-gradient(90deg,var(--cy),var(--pk));-webkit-background-clip:text;background-clip:text;color:transparent;}
.pips{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;flex:1;}
.pip{width:14px;height:14px;border-radius:4px;background:#16224a;border:1px solid #2a3b73;}
.pip.ok{background:var(--ok);border-color:var(--ok);box-shadow:0 0 8px var(--ok);}
.pip.bad{background:var(--bad);border-color:var(--bad);box-shadow:0 0 8px var(--bad);}
.pip.skip{background:var(--am);border-color:var(--am);}
.pip.now{background:var(--cy);border-color:var(--cy);box-shadow:0 0 10px var(--cy);animation:pulse 1.1s infinite;}
@keyframes pulse{50%{opacity:.35}}
.stat{display:inline-block;text-align:center;margin-left:16px;}
.stat small{display:block;font:600 .62rem 'JetBrains Mono',monospace;color:#7f93c9;letter-spacing:2px;}
.stat b{font-family:'Orbitron';font-size:1.15rem;color:#fff;}
.glass{background:var(--card);border:1px solid rgba(0,229,255,.25);border-radius:16px;padding:20px 24px;backdrop-filter:blur(8px);
 box-shadow:0 0 26px rgba(0,229,255,.07);}
.hero{text-align:center;padding:26px 0 8px;}
.hero h1{font-weight:900!important;font-size:3.6rem!important;margin:0;background:linear-gradient(90deg,#00e5ff,#7c4dff 55%,#ff2bd6);
 -webkit-background-clip:text;background-clip:text;color:transparent!important;filter:drop-shadow(0 0 18px rgba(124,77,255,.45));}
.hero p{font:500 .95rem 'JetBrains Mono',monospace;color:#8ea4dd;letter-spacing:3px;margin-top:.2rem;}
.zone{border-radius:16px;padding:16px 18px;min-height:132px;background:linear-gradient(160deg,rgba(16,26,51,.85),rgba(10,16,34,.85));
 border:1px solid rgba(124,77,255,.35);position:relative;overflow:hidden;}
.zone:after{content:"";position:absolute;right:-30px;top:-30px;width:110px;height:110px;border-radius:50%;
 background:radial-gradient(circle,rgba(0,229,255,.22),transparent 70%);}
.zone .zid{font:600 .72rem 'JetBrains Mono',monospace;color:var(--cy);letter-spacing:3px;}
.zone .zname{font:800 1.12rem 'Orbitron';color:#fff;margin:2px 0 4px;}
.zone .zdesc{font-size:.84rem;color:#9fb2e6;}
.zone .zn{font:600 .75rem 'JetBrains Mono',monospace;color:var(--am);margin-top:8px;}
.boss{border-color:rgba(255,43,214,.55);background:linear-gradient(160deg,rgba(60,10,50,.7),rgba(16,26,51,.85));}
.chip{display:inline-block;padding:3px 11px;border-radius:999px;font:600 .76rem 'Segoe UI',Roboto,Arial,sans-serif;margin:0 6px 6px 0;}
.c-topic{background:rgba(0,229,255,.12);color:#8be9ff;border:1px solid rgba(0,229,255,.4);}
.c-kind{background:rgba(124,77,255,.15);color:#cbb8ff;border:1px solid rgba(124,77,255,.45);}
.c-Easy{background:rgba(126,231,135,.12);color:#9af0b4;border:1px solid rgba(126,231,135,.4);}
.c-Medium{background:rgba(255,209,102,.12);color:#ffe08a;border:1px solid rgba(255,209,102,.4);}
.c-Hard{background:rgba(255,92,122,.12);color:#ff9fb1;border:1px solid rgba(255,92,122,.45);}
.c-pts{background:#1b2750;color:#fff;border:1px solid #33478c;}
.c-ref{background:transparent;color:#8ea4dd;border:1px dashed #33478c;}
.qtext{font:500 1.12rem/1.65 'Segoe UI',Roboto,Arial,sans-serif;color:#eaf2ff;}
.fbt{font:700 1.15rem 'Segoe UI',Roboto,Arial,sans-serif;margin-bottom:6px;color:#fff;}
div[role="radiogroup"] p,.stTextInput input{font-family:'Segoe UI',Roboto,Arial,sans-serif!important;font-size:1.02rem;}
.zone .zdesc,.glass p,.glass li{font-family:'Segoe UI',Roboto,Arial,sans-serif;}
.fb-ok{border-left:4px solid var(--ok);}.fb-bad{border-left:4px solid var(--bad);}.fb-mid{border-left:4px solid var(--am);}
.ring{display:flex;align-items:center;justify-content:center;}
.big{font:900 3rem 'Orbitron';background:linear-gradient(90deg,var(--cy),var(--pk));-webkit-background-clip:text;background-clip:text;color:transparent;}
.rank{font:800 1.5rem 'Orbitron';color:var(--am);text-align:center;}
div[role="radiogroup"]>label{background:rgba(10,18,40,.85);border:1px solid #24346a;border-radius:12px;padding:12px 16px;margin:6px 0;width:100%;transition:all .15s;}
div[role="radiogroup"]>label:hover{border-color:var(--cy);box-shadow:0 0 14px rgba(0,229,255,.3);transform:translateX(3px);}
div[role="radiogroup"]>label:has(input:checked){border-color:var(--pk);background:rgba(255,43,214,.10);box-shadow:0 0 16px rgba(255,43,214,.25);}
.stButton>button{border-radius:12px;border:1px solid rgba(0,229,255,.5);background:rgba(0,229,255,.08);color:#dff9ff;font-weight:600;transition:all .15s;}
.stButton>button:hover{border-color:var(--pk);box-shadow:0 0 16px rgba(255,43,214,.45);color:#fff;}
.stButton>button[kind="primary"]{background:linear-gradient(90deg,#00b8d4,#7c4dff 60%,#ff2bd6);border:none;color:#fff;font-weight:700;letter-spacing:.5px;}
button[data-baseweb="tab"]{font-family:'Orbitron',sans-serif;font-size:.82rem;letter-spacing:1px;}
[data-testid="stMetricValue"]{font-family:'Orbitron';}
.legend span{display:inline-block;margin-right:14px;font:500 .78rem 'JetBrains Mono',monospace;color:#9fb2e6;}
.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-1px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ============================================================ state
def init_state():
    d = dict(stage="home", name="", queue=[], idx=0, score=0, streak=0, best_streak=0, records=[], submitted=False,
             last=None, start_q=None, extra_time=0, power=dict(fifty=1, hint=2, skip=1, time=1), removed={},
             hint_used={}, order={}, timer_on=True, survival=False, lives=3, speed_bonuses=0, saved=False,
             mission="", quiz_start=None, queens_res=None, queens_board=None, cfg=None, my_entry=None, seen_guide=False)
    for k, v in d.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()
S = st.session_state
RESET_KEYS = ["stage", "queue", "idx", "score", "streak", "best_streak", "records", "submitted", "last", "start_q",
              "extra_time", "power", "removed", "hint_used", "order", "lives", "speed_bonuses", "saved", "mission", "quiz_start", "my_entry"]


def reset_game():
    for k in list(S.keys()):
        if k.startswith(("ans_", "m_", "risk_")):
            del S[k]
    for k in RESET_KEYS:
        if k in S:
            del S[k]
    init_state()


def norm(t):
    return re.sub(r"\s+", " ", str(t).strip().lower().replace(",", "")).rstrip(".")


# ============================================================ leaderboard
def load_lb():
    try:
        with open(LB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_lb(e):
    data = sorted(load_lb() + [e], key=lambda x: (-x["score"], x["time"]))[:50]
    try:
        with open(LB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def show_lb(limit=10, me=None):
    data = load_lb()
    if not data:
        st.info("The leaderboard is empty. Finish a game to take the #1 spot.")
        return
    top = data[:limit]
    df = pd.DataFrame(top)
    df.insert(0, "Rank", range(1, len(df) + 1))
    cols = ["Rank", "Player", "XP", "Accuracy %", "Mission", "Time (s)"]
    df = df.rename(columns={"name": "Player", "score": "XP", "pct": "Accuracy %", "mission": "Mission", "time": "Time (s)"})
    if me:
        df["You"] = ["◀ YOU" if (r["name"] == me["name"] and r["score"] == me["score"] and r["date"] == me["date"]) else "" for r in top]
        cols.append("You")
    st.dataframe(df[cols], hide_index=True, width="stretch")


# ============================================================ HUD
def hud():
    pips = lives = ""
    if S.stage == "quiz":
        for i in range(len(S.queue)):
            if i < len(S.records):
                r = S.records[i]
                cls = "skip" if r["skipped"] else ("ok" if r["correct"] else "bad")
            else:
                cls = "now" if i == S.idx else ""
            pips += f"<span class='pip {cls}'></span>"
        if S.survival:
            lives = "<div class='stat'><small>LIVES</small><b>" + "".join("❤️" if i < S.lives else "🖤" for i in range(3)) + "</b></div>"
    right = (f"<div class='stat'><small>OPERATOR</small><b>{(S.name.strip() or '-')[:14].upper()}</b></div>"
             f"<div class='stat'><small>XP</small><b>{S.score}</b></div>")
    if S.stage == "quiz":
        right += f"<div class='stat'><small>STREAK</small><b>🔥{S.streak}</b></div>" + lives
    st.markdown(f"<div class='hud'><div class='brand'>AI<span>·NEXUS</span></div><div class='pips'>{pips}</div><div>{right}</div></div>",
                unsafe_allow_html=True)


# ============================================================ sidebar (player profile)
def badges():
    ok = [r for r in S.records if r["correct"]]
    b = []
    if ok:
        b.append("🥇 First Blood")
    if S.best_streak >= 3:
        b.append("🔥 On Fire (3 in a row)")
    if S.best_streak >= 5:
        b.append("⚡ Unstoppable (5 in a row)")
    if sum(1 for r in ok if r["search"]) >= 3:
        b.append("🧭 Search Master")
    if sum(1 for r in ok if r["real"]) >= 3:
        b.append("🌍 Real-World Thinker")
    if S.speed_bonuses >= 3:
        b.append("⏱️ Speedster")
    return b


def sidebar():
    with st.sidebar:
        st.markdown("## 🏆 Player Profile")
        st.markdown(f"**{S.name.strip() or 'Type your name on the home screen'}**")
        st.caption("XP / Score")
        st.markdown(f"<div class='bigscore'>{S.score}</div>", unsafe_allow_html=True)
        if S.stage == "quiz":
            st.progress(S.idx / max(len(S.queue), 1), text=f"Question {min(S.idx + 1, len(S.queue))} of {len(S.queue)}")
            st.metric("🔥 Streak", S.streak)
        st.divider()
        st.markdown("### 🎖️ Badges")
        bl = badges()
        if bl:
            for x in bl:
                st.success(x)
        else:
            st.caption("Complete challenges to unlock badges!")
        if S.stage == "quiz":
            st.divider()
            st.markdown("### 🛟 Power-ups left")
            P = S.power
            st.write(f"✂️ 50-50: **{P['fifty']}** · 🧠 Hint: **{P['hint']}** · ⏭️ Skip: **{P['skip']}** · ⏱️ +15s: **{P['time']}**")
            st.caption(f"Hint costs {HINT_PENALTY} points. Skip gives no points but keeps your streak.")
            st.markdown("### 🎯 Mission")
            st.write(S.mission)
        st.divider()
        st.info("💡 Think before you click. The goal is not just to get the answer, but to understand WHY it is correct.")
        if S.stage != "home" and st.button("🏠 Quit to Home", key="side_quit"):
            reset_game()
            st.rerun()


# ============================================================ mission control
def start_mission(pool, n, label, survival):
    if not pool or not S.name.strip():
        return
    S.name = S.name.strip()
    S.queue = random.sample(pool, min(n, len(pool)))
    S.cfg = dict(ids=[q["id"] for q in pool], n=n, label=label, surv=survival)
    S.mission, S.survival, S.lives = label, survival, 3
    S.stage, S.idx, S.quiz_start = "quiz", 0, time.time()
    S.seen_guide = True
    st.rerun()


def play_again():
    cfg = S.cfg
    if not cfg:
        reset_game()
        st.rerun()
        return
    pool = [q for q in QUESTIONS if q["id"] in set(cfg["ids"])]
    reset_game()
    start_mission(pool, cfg["n"], cfg["label"], cfg["surv"])


def zone_pool(topics):
    return [q for q in QUESTIONS if q["topic"] in topics]


GUIDE = """
**1. Type your name** in the box at the top. You cannot start without it.

**2. Choose how to play.** Pick a difficulty (Easy, Medium, Hard or Mixed), the topics you want and how many questions. You can also tap a **zone** card, the **Boss Rush** or the **Exam simulation** to jump straight in.

**3. Answer the question.** Each question has a small "How to answer" box if you are not sure how that question type works.
- *MCQ / Scenario / Problem Solving:* choose the one best option.
- *True/False:* pick True or False.
- *Assertion-Reason:* read statement A and reason R. Decide if each is true, and if R really explains A.
- *Fill in the Blank:* type a word or a number.
- *Match the Following:* choose a match for every row (you get part marks).

**4. Press "Lock answer".** The game tells you if you were right, shows the correct answer and explains why.

**5. Power-ups (use them wisely, the numbers are limited):**
- ✂️ **50-50** removes two wrong options.
- 🧠 **Hint** gives a clue but costs 5 points.
- ⏭️ **Skip** moves on without points and keeps your streak.
- ⏱️ **+15s** adds 15 seconds to the timer.
- 🎲 **Risk x2** is a bet: double points if you are right, but you lose 10 XP if you are wrong.

**6. Points.** Easy = 10, Medium = 20, Hard = 30. You earn +5 for a fast answer and extra points for a streak of 3 or more correct answers in a row. **XP** is your total score.

**7. Special modes.** *Survival* gives you 3 lives (a wrong answer costs one). *Boss Rush* is 10 hard questions with survival on. *Exam simulation* is a mixed 20 question paper.

**8. At the end** you see your score, rank, topic-wise results, a review of your mistakes and the leaderboard. Press **Return to Home** to start again.
"""


def missions_tab(ready):
    left, right = st.columns([3, 2])
    with left:
        st.subheader("🎯 Choose your mission")
        mode = st.radio("Difficulty level", ["Easy", "Medium", "Hard", "Mixed"], index=3, horizontal=True, key="mode_sel")
        topics = st.multiselect("Topics (leave empty for all)", TOPICS, key="topic_sel")
        avail = [q for q in QUESTIONS if (mode == "Mixed" or q["difficulty"] == mode) and (not topics or q["topic"] in topics)]
        n = 1
        if len(avail) > 1:
            n = st.slider("Number of questions", 1, len(avail), min(15, len(avail)), key="n_sel")
        t1, t2 = st.columns(2)
        S.timer_on = t1.toggle("⏱️ Timer (challenge mode)", value=S.timer_on, key="timer_sel")
        surv = t2.toggle("❤️ Survival mode (3 lives)", key="surv_sel")
        st.caption(f"Time per question: Easy {TIME_LIMIT['Easy']}s, Medium {TIME_LIMIT['Medium']}s, Hard {TIME_LIMIT['Hard']}s. "
                   f"Points: Easy {POINTS['Easy']}, Medium {POINTS['Medium']}, Hard {POINTS['Hard']}.")
        if not avail:
            st.warning("No questions match this filter. Change the level or the topics.")
        if st.button("🚀 Start Mission", type="primary", disabled=not ready or not avail, key="start_main"):
            start_mission(avail, n, f"{mode} mission", surv)
    with right:
        st.subheader("🏅 Leaderboard (Top 10)")
        show_lb()
    if not ready:
        st.warning("👆 Type your name at the top to unlock the missions.")

    st.markdown("### 🛰️ Or jump straight into a zone")
    cols = st.columns(3)
    for i, (zid, name, desc, topics) in enumerate(ZONES):
        pool = zone_pool(topics)
        with cols[i % 3]:
            st.markdown(f"<div class='zone'><div class='zid'>ZONE {zid}</div><div class='zname'>{name}</div>"
                        f"<div class='zdesc'>{desc}</div><div class='zn'>{len(pool)} QUESTIONS IN POOL</div></div>", unsafe_allow_html=True)
            if st.button(f"Deploy to Zone {zid}", key=f"z{zid}", width="stretch", disabled=not ready):
                start_mission(pool, 12, f"Zone {zid} - {name.title()}", surv)
    with cols[2]:
        st.markdown("<div class='zone boss'><div class='zid' style='color:#ff2bd6'>ZONE 06</div><div class='zname'>BOSS RUSH</div>"
                    "<div class='zdesc'>10 hard questions from every topic. Survival mode is forced on.</div>"
                    "<div class='zn' style='color:#ff9fb1'>EXAM-LEVEL DIFFICULTY</div></div>", unsafe_allow_html=True)
        if st.button("⚔️ Enter the Boss Rush", key="boss", type="primary", width="stretch", disabled=not ready):
            start_mission([q for q in QUESTIONS if q["difficulty"] == "Hard"], 10, "Boss Rush", True)
    if st.button("📝 Exam simulation: 20 mixed questions from all topics", key="exam", width="stretch", disabled=not ready):
        start_mission(QUESTIONS, 20, "Exam Simulation", surv)


# ============================================================ question UI
def get_options(q):
    qid = q["id"]
    if qid not in S.order:
        o = list(q["options"])
        if q["shuffle"]:
            random.shuffle(o)
        S.order[qid] = o
    return [x for x in S.order[qid] if x not in S.removed.get(qid, [])]


def match_rights(q):
    if q["id"] not in S.order:
        r = [b for _, b in q["pairs"]]
        random.shuffle(r)
        S.order[q["id"]] = r
    return S.order[q["id"]]


def time_left(q):
    return TIME_LIMIT[q["difficulty"]] + S.extra_time - (time.time() - S.start_q)


def render_input(q):
    qid, t = q["id"], q["type"]
    if t in ("mcq", "tf", "ar"):
        return st.radio("Select your answer", get_options(q), index=None, key=f"ans_{qid}", label_visibility="collapsed")
    if t == "fib":
        return st.text_input("Your answer", key=f"ans_{qid}", placeholder="Type your answer (number or word)")
    picks = {}
    rights = match_rights(q)
    for i, (left, _) in enumerate(q["pairs"]):
        cc = st.columns([2, 3])
        cc[0].markdown(f"**{i + 1}. {left}**")
        picks[left] = cc[1].selectbox("match", rights, index=None, placeholder="Select a match...", key=f"m_{qid}_{i}",
                                      label_visibility="collapsed")
    return picks


def is_answered(q, ans):
    if q["type"] == "match":
        return all(v is not None for v in ans.values())
    if q["type"] == "fib":
        return bool(str(ans).strip())
    return ans is not None


def evaluate(q, ans, timed_out=False, skipped=False):
    base = POINTS[q["difficulty"]]
    used = time.time() - S.start_q
    risk = bool(S.get(f"risk_{q['id']}", False)) and not skipped
    frac, chosen = 0.0, "-"
    if timed_out:
        chosen = "(time up)"
    elif skipped:
        chosen = "(skipped)"
    elif q["type"] in ("mcq", "tf", "ar"):
        chosen, frac = ans, float(ans == q["answer"])
    elif q["type"] == "fib":
        chosen, frac = str(ans), float(norm(ans) in q["accept"])
    else:
        good = sum(1 for a, b in q["pairs"] if ans.get(a) == b)
        frac = good / len(q["pairs"])
        chosen = "; ".join(f"{a} -> {ans.get(a)}" for a, _ in q["pairs"])
    correct = frac == 1.0
    pts = int(round(base * frac))
    if S.hint_used.get(q["id"]) and pts > 0:
        pts = max(pts - HINT_PENALTY, 0)
    bonus = 0
    if correct:
        S.streak += 1
        S.best_streak = max(S.best_streak, S.streak)
        if S.timer_on and used <= TIME_LIMIT[q["difficulty"]] / 3:
            bonus += 5
            S.speed_bonuses += 1
        if S.streak >= 3:
            bonus += min(5 * (S.streak - 2), 15)
    elif not skipped:
        S.streak = 0
    total = pts + bonus
    if risk:
        total = total * 2 if correct else -RISK_LOSS
    new_score = max(0, S.score + total)
    delta = new_score - S.score
    S.score = new_score
    if S.survival and not skipped and frac < 0.5:
        S.lives -= 1
    S.records.append(dict(id=q["id"], topic=q["topic"], kind=q["kind"], difficulty=q["difficulty"], correct=correct,
                          earned=delta, chosen=chosen, answer=q["answer"], search=q["search"], real=q["real"],
                          skipped=skipped, timed_out=timed_out, secs=round(used, 1), risk=risk, q=q["q"].replace("\n", " ")[:110],
                          explanation=q["explanation"], ref=q["ref"]))
    S.last = dict(correct=correct, partial=0 < frac < 1, delta=delta, bonus=bonus if correct else 0, timed_out=timed_out,
                  skipped=skipped, risk=risk)
    S.submitted = True


def next_question():
    S.idx += 1
    S.submitted, S.last, S.start_q, S.extra_time = False, None, None, 0
    if S.idx >= len(S.queue) or (S.survival and S.lives <= 0):
        S.stage = "result"


def ring_svg(left, total):
    frac = max(min(left / max(total, 1), 1.0), 0.0)
    r, circ = 34, 2 * math.pi * 34
    col = "#7ee787" if frac > .5 else ("#ffd166" if frac > .2 else "#ff5c7a")
    return (f"<div class='ring'><svg width='92' height='92' viewBox='0 0 92 92'>"
            f"<circle cx='46' cy='46' r='{r}' stroke='#16224a' stroke-width='7' fill='none'/>"
            f"<circle cx='46' cy='46' r='{r}' stroke='{col}' stroke-width='7' fill='none' stroke-linecap='round' "
            f"stroke-dasharray='{circ:.1f}' stroke-dashoffset='{circ * (1 - frac):.1f}' transform='rotate(-90 46 46)' "
            f"style='filter:drop-shadow(0 0 6px {col})'/>"
            f"<text x='46' y='53' text-anchor='middle' fill='#fff' font-family='Orbitron' font-weight='700' font-size='20'>{max(int(left), 0)}</text>"
            f"</svg></div>")


@st.fragment(run_every=1)
def timer_box(q):
    left = time_left(q)
    if left <= 0 and not S.submitted:
        evaluate(q, None, timed_out=True)
        st.rerun()
    st.markdown(ring_svg(left, TIME_LIMIT[q["difficulty"]] + S.extra_time), unsafe_allow_html=True)


HOW_TO = {
    "mcq": "Read the question and choose the **one best option**, then press **Lock answer**. For Problem Solving questions, work it out on paper if needed.",
    "tf": "Decide if the statement is **True** or **False**, then press **Lock answer**.",
    "ar": "A is a statement and R is a reason. Check (1) is A true? (2) is R true? (3) if both are true, does R really explain A? Then pick the matching option.",
    "fib": "Type just the **word or number** (no units). Capital letters and commas do not matter.",
    "match": "Choose the matching item for **every row**. You get part marks for each correct pair.",
}


def quiz():
    q = S.queue[S.idx]
    if S.start_q is None:
        S.start_q = time.time()
    qid = q["id"]
    head, tmr = st.columns([5, 1])
    with head:
        st.markdown(
            f"<span class='chip c-topic'>{q['topic']}</span><span class='chip c-kind'>{q['kind']}</span>"
            f"<span class='chip c-{q['difficulty']}'>{q['difficulty'].upper()}</span>"
            f"<span class='chip c-pts'>{POINTS[q['difficulty']]} PTS</span>"
            f"<span class='chip c-ref'>{S.mission} · Q{S.idx + 1}/{len(S.queue)}</span>", unsafe_allow_html=True)
    if S.timer_on and not S.submitted:
        with tmr:
            timer_box(q)
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown(f"<div class='qtext'>{q['q'].splitlines()[0] if q['type'] != 'ar' else ''}</div>", unsafe_allow_html=True)
    body = "\n".join(q["q"].splitlines()[1:]) if q["type"] != "ar" else q["q"]
    if body.strip():
        st.markdown(body)
    if q.get("graph"):
        st.graphviz_chart(q["graph"], width="stretch")
    if S.hint_used.get(qid):
        st.info(f"🧠 Hint: {q['hint']}")
    st.markdown("</div>", unsafe_allow_html=True)
    if not S.submitted:
        with st.expander("❓ How to answer this question"):
            st.markdown(HOW_TO[q["type"]] + ("\n\nThe diagram above is part of the question. Use it." if q.get("graph") else "")
                        + "\n\nPower-ups are the buttons under the options. Hover over a button to see what it does.")

    if not S.submitted:
        ans = render_input(q)
        P = S.power
        r = st.columns([1.25, 1, 1, 1, 1, 1.2])
        if r[0].button("⚡ Lock answer", type="primary", width="stretch", help="Submit your answer"):
            if is_answered(q, ans):
                evaluate(q, ans)
                st.rerun()
            else:
                st.warning("Select or type an answer first, or use Skip.")
        can50 = q["type"] in ("mcq", "ar") and P["fifty"] > 0 and qid not in S.removed
        if r[1].button(f"✂️ 50-50 ·{P['fifty']}", disabled=not can50, width="stretch", help="Removes two wrong options (MCQ and Assertion-Reason only)"):
            wrong = [o for o in q["options"] if o != q["answer"]]
            S.removed[qid] = random.sample(wrong, 2 if len(wrong) > 2 else 1)
            P["fifty"] -= 1
            st.rerun()
        if r[2].button(f"🧠 Hint ·{P['hint']}", disabled=P["hint"] <= 0 or S.hint_used.get(qid, False), width="stretch", help="Shows a clue. Costs 5 points if you answer correctly"):
            S.hint_used[qid] = True
            P["hint"] -= 1
            st.rerun()
        if r[3].button(f"⏭️ Skip ·{P['skip']}", disabled=P["skip"] <= 0, width="stretch", help="Move on with no points. Your streak is kept"):
            P["skip"] -= 1
            evaluate(q, None, skipped=True)
            next_question()
            st.rerun()
        if r[4].button(f"⏱️ +15s ·{P['time']}", disabled=P["time"] <= 0 or not S.timer_on, width="stretch", help="Adds 15 seconds to this question"):
            P["time"] -= 1
            S.extra_time += 15
            st.rerun()
        r[5].toggle("🎲 Risk ×2", key=f"risk_{qid}", help=f"A bet: double points if you are right, lose {RISK_LOSS} XP if you are wrong.")
    else:
        L = S.last
        if L["timed_out"]:
            st.markdown("<div class='glass fb-bad'><div class='fbt'>⏰ Time's up</div>", unsafe_allow_html=True)
        elif L["correct"]:
            extra = f" (includes +{L['bonus']} bonus)" if L["bonus"] else ""
            risk = " · Risk paid off 🎲" if L["risk"] else ""
            st.markdown(f"<div class='glass fb-ok'><div class='fbt'>✅ Correct · {L['delta']:+d} XP{extra}{risk}</div>", unsafe_allow_html=True)
        elif L["partial"]:
            st.markdown(f"<div class='glass fb-mid'><div class='fbt'>🟡 Partly correct · {L['delta']:+d} XP</div>", unsafe_allow_html=True)
        else:
            risk = " · Risk lost 🎲" if L["risk"] else ""
            st.markdown(f"<div class='glass fb-bad'><div class='fbt'>❌ Incorrect · {L['delta']:+d} XP{risk}</div>", unsafe_allow_html=True)
        st.markdown(f"**Correct answer:** {q['answer']}")
        st.markdown(f"**Why:** {q['explanation']}")
        st.markdown("</div>", unsafe_allow_html=True)
        done = S.idx + 1 >= len(S.queue) or (S.survival and S.lives <= 0)
        if S.survival and S.lives <= 0:
            st.error("💀 All lives lost. Mission over.")
        if st.button("🏁 Mission report" if done else "➡️ Next question", type="primary"):
            next_question()
            st.rerun()


# ============================================================ results
def radar_svg(vals):
    cx = cy = 150
    R = 105
    n = len(vals)
    pts, labs_ = [], []
    for i, (name, v) in enumerate(vals):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        pts.append((cx + R * v / 100 * math.cos(ang), cy + R * v / 100 * math.sin(ang)))
        labs_.append((cx + (R + 24) * math.cos(ang), cy + (R + 20) * math.sin(ang), name))
    rings = "".join("<polygon points='" + " ".join(
        f"{cx + R * k / 4 * math.cos(-math.pi / 2 + 2 * math.pi * i / n):.1f},{cy + R * k / 4 * math.sin(-math.pi / 2 + 2 * math.pi * i / n):.1f}"
        for i in range(n)) + "' fill='none' stroke='#26386f' stroke-width='1'/>" for k in range(1, 5))
    axes = "".join(f"<line x1='{cx}' y1='{cy}' x2='{cx + R * math.cos(-math.pi / 2 + 2 * math.pi * i / n):.1f}' "
                   f"y2='{cy + R * math.sin(-math.pi / 2 + 2 * math.pi * i / n):.1f}' stroke='#26386f'/>" for i in range(n))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    text = "".join(f"<text x='{x:.1f}' y='{y:.1f}' fill='#cfe3ff' font-size='10' text-anchor='middle' font-family='JetBrains Mono'>{t}</text>"
                   for x, y, t in labs_)
    dots = "".join(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3.5' fill='#00e5ff'/>" for x, y in pts)
    return (f"<svg viewBox='0 0 300 300' width='100%' style='max-width:380px;display:block;margin:auto'>{rings}{axes}"
            f"<polygon points='{poly}' fill='rgba(0,229,255,.25)' stroke='#00e5ff' stroke-width='2'/>{dots}{text}</svg>")


def result():
    recs = S.records
    tot = len(recs)
    ok = sum(r["correct"] for r in recs)
    pct = round(100 * ok / tot) if tot else 0
    secs = int(time.time() - S.quiz_start) if S.quiz_start else 0
    rank = ("S-RANK · GRANDMASTER" if pct >= 90 else "A-RANK · AI ENGINEER" if pct >= 75 else
            "B-RANK · ANALYST" if pct >= 60 else "C-RANK · APPRENTICE" if pct >= 40 else "D-RANK · NOVICE")
    if not S.saved:
        S.my_entry = dict(name=S.name, score=S.score, pct=pct, mission=S.mission, time=secs, date=datetime.now().strftime("%d-%b-%Y %H:%M:%S"))
        save_lb(S.my_entry)
        S.saved = True
        if pct >= 75:
            st.balloons()
    st.markdown("<div class='hero'><p>MISSION COMPLETE</p><div class='big'>" + f"{S.score} XP</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='rank'>{rank}</div>", unsafe_allow_html=True)
    m = st.columns(5)
    m[0].metric("Correct", f"{ok}/{tot}")
    m[1].metric("Accuracy", f"{pct}%")
    m[2].metric("Best streak", S.best_streak)
    m[3].metric("Time", f"{secs}s")
    m[4].metric("Mission", S.mission)
    b1, b2, _ = st.columns([1, 1, 2])
    if b1.button("🏠 Return to Home", type="primary", key="home_top", width="stretch"):
        reset_game()
        st.rerun()
    if b2.button("🔁 Play again", key="again_top", width="stretch", help="Same settings, new random questions"):
        play_again()

    df = pd.DataFrame(recs)
    left, right = st.columns([2, 1])
    with left:
        t1, t2, t3 = st.tabs(["📊 ANALYSIS", "🔍 REVIEW", "📚 REVISION PLAN"])
        with t1:
            tdf = df.groupby("topic")["correct"].agg(["sum", "count"])
            tdf["Accuracy %"] = (100 * tdf["sum"] / tdf["count"]).round(0)
            st.write("**Topic-wise accuracy**")
            st.bar_chart(tdf["Accuracy %"])
            zone_vals = []
            for zid, name, _, topics in ZONES:
                sub = df[df["topic"].isin(topics)]
                zone_vals.append((name.title(), round(100 * sub["correct"].mean()) if len(sub) else 0))
            a, b = st.columns([1, 1])
            a.markdown(radar_svg(zone_vals), unsafe_allow_html=True)
            b.markdown("**Zone mastery** (zones not played show 0%)")
            for n_, v in zone_vals:
                b.progress(v / 100, text=f"{n_}: {v}%")
            st.write("**Accuracy by question format**")
            st.bar_chart(df.groupby("kind")["correct"].mean().mul(100).round(0).rename("Accuracy %"))
        with t2:
            wrong = [r for r in recs if not r["correct"]]
            if not wrong:
                st.success("Flawless run. Nothing to review!")
            for r in wrong:
                with st.expander(f"❌ Q{r['id']} · {r['topic']} · {r['kind']}"):
                    st.markdown(f"**Question:** {r['q']}")
                    st.markdown(f"**Your answer:** {r['chosen']}")
                    st.markdown(f"**Correct answer:** {r['answer']}")
                    st.markdown(f"**Why:** {r['explanation']}")
            show = df[["id", "topic", "kind", "difficulty", "correct", "earned", "chosen", "answer", "secs"]].copy()
            show.columns = ["Q ID", "Topic", "Format", "Level", "Correct?", "XP", "Your answer", "Right answer", "Secs"]
            st.dataframe(show, hide_index=True, width="stretch")
            st.download_button("⬇️ Download my result (CSV)", show.to_csv(index=False).encode("utf-8"),
                               file_name=f"ai_nexus_{S.name}.csv", mime="text/csv")
        with t3:
            tdf2 = df.groupby("topic")["correct"].agg(["sum", "count"])
            tdf2["acc"] = 100 * tdf2["sum"] / tdf2["count"]
            weak = tdf2[tdf2["acc"] < 60]
            if weak.empty:
                st.success("No weak topics in this mission. Try Boss Rush or another zone next.")
            for tp, row in weak.sort_values("acc").iterrows():
                st.markdown(f"**{tp}**: {int(row['sum'])}/{int(row['count'])} correct. Revise: _{TOPIC_REF[tp]}_")
    with right:
        st.markdown("### 🏆 Leaderboard")
        data = load_lb()
        mine = next((i + 1 for i, e in enumerate(data) if S.my_entry and e["name"] == S.my_entry["name"]
                     and e["score"] == S.my_entry["score"] and e["date"] == S.my_entry["date"]), None)
        if mine:
            st.success(f"{S.name}, you are ranked #{mine} of {len(data)}.")
        show_lb(10, S.my_entry)
    if st.button("🏠 Return to Home", type="primary", key="home_bottom"):
        reset_game()
        st.rerun()


# ============================================================ search lab
@st.cache_data(show_spinner=False)
def cached_maze(n, density, seed):
    return labs.make_maze(n, density, seed)


def lab_path():
    st.markdown("#### Lab 1 · Path-finding on a grid (AIMA Ch.3)")
    st.caption("Watch the algorithms explore the same maze. Move the replay slider to see the frontier and explored set grow.")
    c = st.columns(5)
    alg = c[0].selectbox("Algorithm", ["BFS", "DFS", "Iterative Deepening", "Greedy Best-First", "A*"], index=4)
    n = c[1].selectbox("Grid size", [12, 16, 20], index=1)
    dens = c[2].slider("Wall density", 0.10, 0.40, 0.25, 0.05)
    seed = c[3].number_input("Maze seed", 1, 9999, 7)
    w = c[4].slider("A* weight w", 1.0, 5.0, 1.0, 0.5, disabled=alg != "A*", help="w = 1 is optimal A*; w > 1 is faster but may lose optimality.")
    walls, start, goal = cached_maze(n, dens, int(seed))
    res = labs.run_search(alg, n, walls, start, goal, w)
    total = len(res["exp"])
    step = st.slider("Replay step (nodes expanded)", 0, total, total, key=f"step_{alg}_{n}_{dens}_{seed}_{w}")
    left, right = st.columns([3, 2])
    with left:
        st.markdown(labs.grid_html(n, set(walls), start, goal, res, step, cell=max(14, int(480 / n))), unsafe_allow_html=True)
        st.markdown("<div class='legend' style='margin-top:10px;text-align:center'>"
                    "<span><i style='background:#00e676'></i>Start</span><span><i style='background:#ff2bd6'></i>Goal</span>"
                    "<span><i style='background:hsl(210,85%,42%)'></i>Expanded</span><span><i style='background:#7c4dff'></i>Frontier</span>"
                    "<span><i style='background:#ffd166'></i>Path</span><span><i style='background:#1a2342'></i>Wall</span></div>",
                    unsafe_allow_html=True)
    with right:
        base = labs.run_search("BFS", n, walls, start, goal)
        opt = len(base["path"]) - 1
        plen = len(res["path"]) - 1 if res["path"] else None
        m = st.columns(2)
        m[0].metric("Nodes expanded", total)
        m[1].metric("Path length", plen if plen is not None else "none")
        m = st.columns(2)
        m[0].metric("Frontier now", labs.frontier_size(res, step))
        m[1].metric("Optimal?", "Yes" if plen == opt else f"No (+{plen - opt})" if plen is not None else "-")
        rows = []
        for a_ in ["BFS", "DFS", "Iterative Deepening", "Greedy Best-First", "A*"]:
            r_ = labs.run_search(a_, n, walls, start, goal, 1.0)
            pl = len(r_["path"]) - 1
            rows.append({"Algorithm": a_, "Expanded": r_["expanded"], "Path": pl, "Optimal": "✔" if pl == opt else "✘"})
        st.write("**Same maze, all algorithms**")
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        st.caption("Iterative deepening counts expansions over all its iterations (upper levels are repeated).")


def lab_queens():
    st.markdown("#### Lab 2 · 8-queens hill climbing (AIMA Sec. 4.1)")
    st.caption("Run hundreds of random starts and compare your results with the numbers printed in the textbook.")
    c = st.columns(3)
    variant = c[0].selectbox("Variant", ["Steepest-ascent", "First-choice", "Steepest-ascent + sideways moves (limit 100)", "Random-restart"])
    trials = c[1].slider("Number of experiments", 50, 1000, 300, 50)
    seed = c[2].number_input("Random seed", 1, 9999, 1, key="qseed")
    book = {"Steepest-ascent": "AIMA: solves about 14%; about 4 steps when it succeeds, 3 when stuck.",
            "First-choice": "No figure in the book; useful when each state has thousands of successors.",
            "Steepest-ascent + sideways moves (limit 100)": "AIMA: success rises from 14% to about 94%.",
            "Random-restart": "AIMA: about 7 runs (6 failures + 1 success), about 22 steps in total."}[variant]
    a, b = st.columns(2)
    if a.button("▶ Run experiment", type="primary", key="qrun"):
        with st.spinner("Climbing hills..."):
            S.queens_res = (variant, labs.queens_experiment(variant, trials, int(seed)))
    if b.button("👁 Watch one climb", key="qone"):
        rng = random.Random(int(seed) + random.randint(0, 9999))
        okc, steps, state, hist = labs.climb(rng, "steepest", 0, record=True)
        S.queens_board = (okc, steps, state, hist)
    st.info(book)
    if S.queens_res:
        v, r = S.queens_res
        st.markdown(f"**Result for:** {v}")
        mm = st.columns(3)
        if r["kind"] == "restart":
            mm[0].metric("Avg runs needed", f"{r['avg_restarts']:.1f}")
            mm[1].metric("Avg total steps", f"{r['avg_steps']:.1f}")
        else:
            mm[0].metric("Solved", f"{r['success']:.1f}%")
            mm[1].metric("Avg steps (solved)", "-" if math.isnan(r["avg_ok"]) else f"{r['avg_ok']:.1f}")
            mm[2].metric("Avg steps (stuck)", "-" if math.isnan(r["avg_bad"]) else f"{r['avg_bad']:.1f}")
    if S.queens_board:
        okc, steps, state, hist = S.queens_board
        x, y = st.columns([1, 2])
        x.markdown(labs.board_html(state), unsafe_allow_html=True)
        x.caption(f"{'Solved: h = 0' if okc else 'Stuck at a local minimum'} after {steps} steps (final h = {hist[-1]}). Red queens are under attack.")
        y.line_chart(pd.DataFrame({"h (attacking pairs)": hist}))


def lab_puzzle():
    st.markdown("#### Lab 3 · 8-puzzle heuristics (AIMA Sec. 3.6)")
    st.caption("A* with no heuristic, h1 (misplaced tiles) and h2 (Manhattan distance) on the same puzzle. Better heuristic means fewer nodes and a smaller effective branching factor b*.")
    c = st.columns(3)
    k = c[0].slider("Scramble moves", 8, 30, 20)
    seed = c[1].number_input("Puzzle seed", 1, 9999, 3, key="pseed")
    start = labs.scramble(k, int(seed))
    c[2].markdown(labs.puzzle_html(start), unsafe_allow_html=True)
    if st.button("▶ Solve with A*", type="primary", key="prun"):
        rows = []
        with st.spinner("Searching..."):
            for name, h in [("h = 0 (blind)", labs.h_zero), ("h1 = misplaced tiles", labs.h1), ("h2 = Manhattan distance", labs.h2)]:
                r = labs.astar_puzzle(start, h)
                rows.append({"Heuristic": name, "Solution depth": r["depth"] if r["solved"] else "stopped",
                             "Nodes generated": r["generated"], "Nodes expanded": r["expanded"],
                             "b*": labs.effective_b(r["generated"], r["depth"]) if r["solved"] else "-"})
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        st.success("h2 dominates h1 (h2(n) ≥ h1(n) for every n), so A* with h2 expands no more nodes than with h1.")


def lab_tab():
    st.info("🧪 **New here?** The Search Lab is not part of the quiz. It lets you watch the algorithms from your syllabus run. "
            "Pick a lab, change the settings and press the button. Nothing here changes your score.")
    t1, t2, t3 = st.tabs(["🧭 PATH-FINDER", "♛ 8-QUEENS CLIMBER", "🧩 8-PUZZLE HEURISTICS"])
    with t1:
        lab_path()
    with t2:
        lab_queens()
    with t3:
        lab_puzzle()


# ============================================================ how to play tab
def briefing_tab():
    a, b = st.columns([3, 2])
    with a:
        st.markdown("### 🎮 How to play")
        st.markdown(GUIDE)
    with b:
        st.markdown("### 📋 Quick facts")
        st.markdown(f"- **{len(QUESTIONS)} questions** across 20 topics of Units I and II\n"
                    "- Formats: MCQ, True/False, Assertion-Reason, Fill in the Blank, Match the Following, Scenario, Problem Solving\n"
                    f"- Time per question: {TIME_LIMIT['Easy']}s / {TIME_LIMIT['Medium']}s / {TIME_LIMIT['Hard']}s (Easy / Medium / Hard)\n"
                    "- The **Search Lab** tab lets you watch BFS, DFS, A*, hill climbing and more run")
        st.markdown("### 📖 Where to study each topic")
        st.dataframe(pd.DataFrame({"Topic": list(TOPIC_REF.keys()), "Where to read": list(TOPIC_REF.values()),
                                   "Questions": [sum(1 for q in QUESTIONS if q['topic'] == t) for t in TOPIC_REF]}),
                     hide_index=True, width="stretch", height=400)


# ============================================================ home & router
def home():
    st.markdown("<div class='hero'><h1>AI·NEXUS</h1><p>SEARCH · AGENTS · HEURISTICS · CSP</p></div>", unsafe_allow_html=True)
    S.name = st.text_input("👤 Your name (required to start)", value=S.name, placeholder="Type your name and start the game", max_chars=20)
    ready = bool(S.name.strip())
    with st.expander("👋 New here? Read this 1-minute guide on how to play", expanded=not S.seen_guide):
        st.markdown(GUIDE)
    tabs = st.tabs(["🎮 PLAY", "🧪 SEARCH LAB", "🏆 LEADERBOARD", "📖 HOW TO PLAY"])
    with tabs[0]:
        missions_tab(ready)
    with tabs[1]:
        lab_tab()
    with tabs[2]:
        show_lb(20)
    with tabs[3]:
        briefing_tab()


sidebar()
hud()
if S.stage == "home":
    home()
elif S.stage == "quiz":
    quiz()
else:
    result()
