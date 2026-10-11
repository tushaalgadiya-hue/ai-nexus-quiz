"""
AI NEXUS - Search Lab engines.
Lab 1: grid path-finding with BFS / DFS / Iterative Deepening / Greedy best-first / A*   (AIMA Ch.3)
Lab 2: 8-queens hill climbing variants                                                  (AIMA Ch.4 Sec.4.1)
Lab 3: 8-puzzle heuristics h1 (misplaced tiles) vs h2 (Manhattan distance)               (AIMA Ch.3 Sec.3.6)
"""
import heapq
import math
import random
from collections import deque

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


# ============================================================ Lab 1: grid path-finding
def _nbrs(cell, n, walls):
    r, c = cell
    out = []
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in walls:
            out.append((nr, nc))
    return out


def _bfs_len(walls, n, start, goal):
    q, seen = deque([(start, 0)]), {start}
    while q:
        cur, d = q.popleft()
        if cur == goal:
            return d
        for nb in _nbrs(cur, n, walls):
            if nb not in seen:
                seen.add(nb)
                q.append((nb, d + 1))
    return None


def make_maze(n, density, seed):
    """Random solvable maze. Start = top-left, goal = bottom-right."""
    start, goal = (0, 0), (n - 1, n - 1)
    s = seed
    while True:
        rng = random.Random(s)
        walls = {(r, c) for r in range(n) for c in range(n) if rng.random() < density}
        walls.discard(start)
        walls.discard(goal)
        if _bfs_len(walls, n, start, goal) is not None:
            return frozenset(walls), start, goal
        s += 1000


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _path(parent, goal):
    p, cur = [], goal
    while cur is not None:
        p.append(cur)
        cur = parent.get(cur)
    return p[::-1]


def run_search(alg, n, walls, start, goal, w=1.0):
    """Returns dict(exp=list of expanded cells in order, gen={cell: expansions done when first generated},
    path=list or None, expanded=int)"""
    walls = set(walls)
    exp, gen, parent = [], {start: 0}, {start: None}
    found = False

    if alg == "BFS":
        frontier, seen = deque([start]), {start}
        if start == goal:
            found = True
        while frontier and not found:
            cur = frontier.popleft()
            exp.append(cur)
            for nb in _nbrs(cur, n, walls):
                if nb not in seen:
                    seen.add(nb)
                    parent[nb] = cur
                    gen[nb] = len(exp)
                    if nb == goal:
                        found = True
                        break
                    frontier.append(nb)

    elif alg == "DFS":
        stack, closed = [start], set()
        while stack:
            cur = stack.pop()
            if cur in closed:
                continue
            closed.add(cur)
            exp.append(cur)
            if cur == goal:
                found = True
                break
            for nb in reversed(_nbrs(cur, n, walls)):
                if nb not in closed:
                    gen.setdefault(nb, len(exp))
                    parent[nb] = cur
                    stack.append(nb)

    elif alg == "Iterative Deepening":
        for limit in range(0, n * n):
            best, par = {}, {}
            stack = [(start, 0, None)]
            while stack:
                cur, d, pr = stack.pop()
                if best.get(cur, 10 ** 9) <= d:
                    continue
                best[cur] = d
                par[cur] = pr
                exp.append(cur)
                if cur == goal:
                    found = True
                    break
                if d < limit:
                    for nb in reversed(_nbrs(cur, n, walls)):
                        gen.setdefault(nb, len(exp))
                        stack.append((nb, d + 1, cur))
            if found:
                parent = par
                break

    elif alg in ("Greedy Best-First", "A*"):
        weight = w if alg == "A*" else 1.0
        g = {start: 0}
        heap, cnt, closed = [(manhattan(start, goal), 0, start)], 0, set()
        while heap:
            _, _, cur = heapq.heappop(heap)
            if cur in closed:
                continue
            closed.add(cur)
            exp.append(cur)
            if cur == goal:
                found = True
                break
            for nb in _nbrs(cur, n, walls):
                ng = g.get(cur, 0) + 1
                if alg == "Greedy Best-First":
                    if nb not in parent:
                        parent[nb] = cur
                        g[nb] = ng
                        gen[nb] = len(exp)
                        cnt += 1
                        heapq.heappush(heap, (manhattan(nb, goal), cnt, nb))
                elif ng < g.get(nb, 10 ** 9):
                    g[nb] = ng
                    parent[nb] = cur
                    gen.setdefault(nb, len(exp))
                    closed.discard(nb)
                    cnt += 1
                    heapq.heappush(heap, (ng + weight * manhattan(nb, goal), cnt, nb))
    else:
        raise ValueError(alg)

    exp_index = {}
    for i, c in enumerate(exp, 1):
        exp_index.setdefault(c, i)
    path = _path(parent, goal) if found else None
    return dict(exp=exp, gen=gen, exp_index=exp_index, path=path, expanded=len(exp))


def grid_html(n, walls, start, goal, res, step, show_path=True, cell=26):
    """Coloured grid at replay step `step` (number of expansions shown)."""
    total = max(len(res["exp"]), 1)
    path = set(res["path"]) if (res["path"] and show_path and step >= len(res["exp"])) else set()
    rows = []
    for r in range(n):
        cells = []
        for c in range(n):
            p = (r, c)
            ei = res["exp_index"].get(p)
            gi = res["gen"].get(p)
            if p == start:
                bg, txt = "#00e676", "S"
            elif p == goal:
                bg, txt = "#ff2bd6", "G"
            elif p in walls:
                bg, txt = "#1a2342", ""
            elif p in path:
                bg, txt = "#ffd166", ""
            elif ei is not None and ei <= step:
                hue = 195 + int(60 * ei / total)
                bg, txt = f"hsl({hue},85%,42%)", ""
            elif gi is not None and gi <= step:
                bg, txt = "#7c4dff", ""
            else:
                bg, txt = "#0c1430", ""
            cells.append(f"<div style='width:{cell}px;height:{cell}px;background:{bg};display:flex;align-items:center;"
                         f"justify-content:center;font:700 12px JetBrains Mono,monospace;color:#001;border-radius:4px'>{txt}</div>")
        rows.append("<div style='display:flex;gap:2px'>" + "".join(cells) + "</div>")
    return "<div style='display:flex;flex-direction:column;gap:2px;width:max-content;margin:auto'>" + "".join(rows) + "</div>"


def frontier_size(res, step):
    return sum(1 for c, gi in res["gen"].items()
               if gi <= step and not (c in res["exp_index"] and res["exp_index"][c] <= step))


# ============================================================ Lab 2: 8-queens hill climbing
def _conf(state, col, row):
    """Number of other queens attacking square (col,row)."""
    k = 0
    for j, rj in enumerate(state):
        if j != col and (rj == row or abs(rj - row) == abs(j - col)):
            k += 1
    return k


def queens_h(state):
    return sum(1 for i in range(8) for j in range(i + 1, 8)
               if state[i] == state[j] or abs(state[i] - state[j]) == j - i)


def climb(rng, variant="steepest", sideways=0, record=False):
    """One hill-climbing run on 8-queens. Returns (solved, steps, final_state, h_history)."""
    state = [rng.randrange(8) for _ in range(8)]
    cur = queens_h(state)
    hist = [cur]
    steps = side = 0
    while cur > 0:
        if variant == "first":
            moves = [(c, r) for c in range(8) for r in range(8) if r != state[c]]
            rng.shuffle(moves)
            chosen = None
            for c, r in moves:
                hn = cur - _conf(state, c, state[c]) + _conf(state, c, r)
                if hn < cur:
                    chosen = (c, r, hn)
                    break
            if chosen is None:
                break
            c, r, hn = chosen
            state[c], cur = r, hn
            steps += 1
        else:
            best, cands = 10 ** 9, []
            for c in range(8):
                base = _conf(state, c, state[c])
                for r in range(8):
                    if r == state[c]:
                        continue
                    hn = cur - base + _conf(state, c, r)
                    if hn < best:
                        best, cands = hn, [(c, r)]
                    elif hn == best:
                        cands.append((c, r))
            if best < cur:
                c, r = rng.choice(cands)
                state[c], cur = r, best
                steps += 1
                side = 0
            elif best == cur and side < sideways:
                c, r = rng.choice(cands)
                state[c], cur = r, best
                steps += 1
                side += 1
            else:
                break
        if record:
            hist.append(cur)
    return cur == 0, steps, state, hist


def queens_experiment(variant, trials, seed):
    rng = random.Random(seed)
    if variant == "Random-restart":
        restarts, steps = [], []
        for _ in range(trials):
            nr = ts = 0
            while True:
                nr += 1
                ok, st, _, _ = climb(rng, "steepest", 0)
                ts += st
                if ok:
                    break
            restarts.append(nr)
            steps.append(ts)
        return dict(kind="restart", avg_restarts=sum(restarts) / trials, avg_steps=sum(steps) / trials)
    mode, side = {"Steepest-ascent": ("steepest", 0), "First-choice": ("first", 0),
                  "Steepest-ascent + sideways moves (limit 100)": ("steepest", 100)}[variant]
    ok_steps, bad_steps = [], []
    for _ in range(trials):
        ok, st, _, _ = climb(rng, mode, side)
        (ok_steps if ok else bad_steps).append(st)
    return dict(kind="single", success=100 * len(ok_steps) / trials,
                avg_ok=(sum(ok_steps) / len(ok_steps)) if ok_steps else float("nan"),
                avg_bad=(sum(bad_steps) / len(bad_steps)) if bad_steps else float("nan"))


def board_html(state, cell=34):
    rows = []
    for r in range(8):
        cs = []
        for c in range(8):
            dark = (r + c) % 2 == 1
            q = state[c] == r
            bad = q and _conf(state, c, r) > 0
            col = "#ff5c7a" if bad else "#00e5ff"
            cs.append(f"<div style='width:{cell}px;height:{cell}px;background:{'#16224a' if dark else '#0d1738'};"
                      f"display:flex;align-items:center;justify-content:center;font-size:{cell - 8}px;color:{col}'>"
                      f"{'♛' if q else ''}</div>")
        rows.append("<div style='display:flex'>" + "".join(cs) + "</div>")
    return "<div style='width:max-content;margin:auto;border:1px solid #00e5ff55;border-radius:6px;overflow:hidden'>" + "".join(rows) + "</div>"


# ============================================================ Lab 3: 8-puzzle heuristics
GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)


def pz_moves(s):
    i = s.index(0)
    r, c = divmod(i, 3)
    out = []
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc
            t = list(s)
            t[i], t[j] = t[j], t[i]
            out.append(tuple(t))
    return out


def h_zero(s):
    return 0


def h1(s):
    return sum(1 for i, t in enumerate(s) if t and t != i)


def h2(s):
    return sum(abs(i // 3 - t // 3) + abs(i % 3 - t % 3) for i, t in enumerate(s) if t)


def scramble(k, seed):
    rng = random.Random(seed)
    s, prev = GOAL, None
    for _ in range(k):
        opts = [m for m in pz_moves(s) if m != prev]
        prev, s = s, rng.choice(opts)
    return s


def astar_puzzle(start, h, cap=150000):
    g = {start: 0}
    heap, cnt, closed, generated = [(h(start), 0, start)], 0, set(), 1
    while heap:
        _, _, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        if cur == GOAL:
            return dict(solved=True, depth=g[cur], generated=generated, expanded=len(closed))
        closed.add(cur)
        if len(closed) >= cap:
            return dict(solved=False, depth=None, generated=generated, expanded=len(closed))
        for nb in pz_moves(cur):
            ng = g[cur] + 1
            if ng < g.get(nb, 10 ** 9):
                g[nb] = ng
                generated += 1
                cnt += 1
                heapq.heappush(heap, (ng + h(nb), cnt, nb))
    return dict(solved=False, depth=None, generated=generated, expanded=len(closed))


def effective_b(N, d):
    """Solve N + 1 = 1 + b + b^2 + ... + b^d for b."""
    if not d or N <= d:
        return float("nan")
    lo, hi = 1.0001, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        total = sum(mid ** i for i in range(d + 1))
        if total < N + 1:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 2)


def puzzle_html(s, cell=46):
    rows = []
    for r in range(3):
        cs = []
        for c in range(3):
            t = s[r * 3 + c]
            cs.append(f"<div style='width:{cell}px;height:{cell}px;display:flex;align-items:center;justify-content:center;"
                      f"font:700 20px Orbitron,sans-serif;border-radius:8px;"
                      f"background:{'#0c1430' if t == 0 else 'linear-gradient(135deg,#00e5ff33,#7c4dff44)'};"
                      f"border:1px solid #00e5ff55;color:#e6f1ff'>{'' if t == 0 else t}</div>")
        rows.append("<div style='display:flex;gap:4px'>" + "".join(cs) + "</div>")
    return "<div style='display:flex;flex-direction:column;gap:4px;width:max-content;margin:auto'>" + "".join(rows) + "</div>"
