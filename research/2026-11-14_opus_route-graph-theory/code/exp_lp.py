"""E11: integrality of the natural LP relaxation
  P = { x on spokes of B : x is a fractional perfect matching of B,
        y = 1 - x (on all spokes of H, x = 0 at root/t0 spokes) lies in the spanning-tree
        polytope of H }.
Integer points of P are exactly the tree matchings.  We maximise random objectives by
cutting planes (subtour constraints y(E(S)) <= |S|-1 separated exactly by min cut) and
compare with the best tree matching.  LP opt > best TM  => P has a fractional vertex.
Usage: python exp_lp.py Vmax trials_per_instance [Vmin]"""
import sys, random
import numpy as np
import networkx as nx
from scipy.optimize import linprog
from tri import load
from states import Rooted

def separate(Hn, Hedges, y):
    """return a vertex set S with y(E(S)) > |S|-1 + 1e-7, or None"""
    deg = {v: 0.0 for v in Hn}
    for (u, v), w in zip(Hedges, y):
        deg[u] += w; deg[v] += w
    best = None
    for k in Hn:
        G = nx.DiGraph()
        for (u, v), w in zip(Hedges, y):
            if w > 1e-12:
                G.add_edge(u, v, capacity=w / 2); G.add_edge(v, u, capacity=w / 2)
        off = 0.0
        for v in Hn:
            c = 1 - deg[v] / 2
            if v == k:
                G.add_edge("src", v, capacity=1e9)
                off += c
                continue
            if c >= 0:
                G.add_edge(v, "snk", capacity=c)
            else:
                G.add_edge("src", v, capacity=-c)
                off += c
        G.add_node("src"); G.add_node("snk")
        val, (Sside, _) = nx.minimum_cut(G, "src", "snk")
        # min over S containing k of sum_{v in S} c(v) + y(delta S)/2 = val + off
        if val + off < 1 - 1e-7:
            S = set(Sside) - {"src"}
            return S
    return None

def lp_max(R, c):
    spokes = [(t, v) for t in R.A for v in R.corners[t]]
    m = len(spokes)
    # equality: perfect matching
    A_eq, b_eq = [], []
    for t in R.A:
        A_eq.append([1.0 if sp[0] == t else 0.0 for sp in spokes]); b_eq.append(1.0)
    for x in R.X:
        A_eq.append([1.0 if sp[1] == x else 0.0 for sp in spokes]); b_eq.append(1.0)
    # H: all spokes; x=0 on spokes not in B
    Hedges = [(("c", t), ("v", v)) for t in R.black for v in t]
    Hn = sorted({u for e in Hedges for u in e}, key=str)
    sidx = {(("c", t), ("v", v)): i for i, (t, v) in enumerate(spokes)}
    A_ub, b_ub = [], []
    for it in range(200):
        res = linprog(-c, A_ub=A_ub or None, b_ub=b_ub or None, A_eq=A_eq, b_eq=b_eq,
                      bounds=[(0, 1)] * m, method="highs")
        x = res.x
        y = [1 - x[sidx[e]] if e in sidx else 1.0 for e in Hedges]
        S = separate(Hn, Hedges, y)
        if S is None:
            return -res.fun, x
        # y(E(S)) <= |S|-1  <=>  sum_{e in E(S)} (1 - x_e) <= |S|-1
        row = [0.0] * m
        const = 0.0
        for e in Hedges:
            if e[0] in S and e[1] in S:
                if e in sidx:
                    row[sidx[e]] -= 1.0
                const += 1.0
        A_ub.append(row); b_ub.append(len(S) - 1 - const)
    raise RuntimeError("no convergence")

if __name__ == "__main__":
    Vmax, trials = int(sys.argv[1]), int(sys.argv[2])
    Vmin = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    rng = np.random.default_rng(1)
    for V in range(Vmin, Vmax + 1):
        inst = frac = 0
        ex = None
        for T in load(V):
            for f in T.faces():
                R = Rooted(T, f)
                if R.black_inner_sep_triangles():
                    continue
                inst += 1
                spokes = [(t, v) for t in R.A for v in R.corners[t]]
                TM = [s for s in R.states() if R.is_tree_matching(s)]
                tmv = [np.array([1.0 if s[t] == v else 0.0 for (t, v) in spokes]) for s in TM]
                found = False
                for _ in range(trials):
                    c = rng.normal(size=len(spokes))
                    opt, x = lp_max(R, c)
                    best = max(float(c @ v) for v in tmv)
                    if opt > best + 1e-6:
                        found = True
                        if ex is None:
                            ex = (V, T.rot, R.t0, [(sp, round(xx, 3)) for sp, xx in zip(spokes, x) if 1e-6 < xx < 1 - 1e-6])
                        break
                frac += found
        print(V, "instances", inst, "with fractional optimum found:", frac, flush=True)
        if ex and ex[0] == V:
            print("   example fractional point:", ex)
