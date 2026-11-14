"""E16: Felsner lattice of alpha-orientations of H0 = H - (outer centre).
A pair (r,s) up to reversing its D-cycles is a 2-factor F of B; orient spokes in F
centre->vertex and the deleted spoke (t,u(t)) vertex->centre.  Two such orientations
differ on disjoint directed cycles; we read their sense from a Tutte barycentric drawing
(t0 outer).  The minimal orientation has no ccw difference cycle against any other.
Question: does the minimal (maximal) 2-factor contain an ordered tree pair?
Usage: python exp_alpha.py Vmax"""
import sys, itertools
import numpy as np
from tri import load
from states import Rooted

def tutte_positions(R):
    T = R.T
    V = T.V
    idx = {v: i for i, v in enumerate(V)}
    pos = np.zeros((len(V), 2))
    outer = list(R.t0)
    ang = [np.pi / 2 + 2 * np.pi * k / 3 for k in range(3)]
    for k, v in enumerate(outer):
        pos[idx[v]] = [np.cos(ang[k]), np.sin(ang[k])]
    inner = [v for v in V if v not in outer]
    ii = {v: i for i, v in enumerate(inner)}
    A = np.zeros((len(inner), len(inner))); b = np.zeros((len(inner), 2))
    for v in inner:
        A[ii[v], ii[v]] = len(T.rot[v])
        for w in T.rot[v]:
            if w in ii:
                A[ii[v], ii[w]] -= 1
            else:
                b[ii[v]] += pos[idx[w]]
    sol = np.linalg.solve(A, b)
    for v in inner:
        pos[idx[v]] = sol[ii[v]]
    P = {v: pos[idx[v]] for v in V}
    for t in R.black:
        P[("c", t)] = sum(P[w] for w in t) / 3
    return P

def area(P, cyc):
    a = 0.0
    for i in range(len(cyc)):
        x1, y1 = P[cyc[i]]; x2, y2 = P[cyc[(i + 1) % len(cyc)]]
        a += x1 * y2 - x2 * y1
    return a / 2

def orientation(R, u):
    """set of directed spokes for deleted-corner map u (on A)"""
    D = set()
    for t in R.A:
        for v in t:
            D.add((v, ("c", t)) if v == u[t] else (("c", t), v))
    return D

def diff_cycles(O1, O2):
    """edges of O1 reversed in O2, as directed cycles in O1"""
    E = [e for e in O1 if (e[1], e[0]) in O2]
    succ = {}
    for a, b in E:
        succ.setdefault(a, []).append(b)
    cycles = []
    used = set()
    for a, b in E:
        if (a, b) in used:
            continue
        cyc = [a]
        cur = (a, b)
        while True:
            used.add(cur)
            nxt = cur[1]
            if nxt == a:
                break
            cyc.append(nxt)
            cand = [w for w in succ[nxt] if (nxt, w) not in used]
            cur = (nxt, cand[0])
        cycles.append(cyc)
    return cycles

if __name__ == '__main__':
    Vmax = int(sys.argv[1])
    for V in range(6, Vmax + 1):
        stat = dict(inst=0, min_has_tree_pair=0, max_has_tree_pair=0, either=0)
        for T in load(V):
            for f in T.faces():
                R = Rooted(T, f)
                if R.black_inner_sep_triangles():
                    continue
                P = tutte_positions(R)
                S = R.states()
                TMset = {frozenset(s.items()) for s in S if R.is_tree_matching(s)}
                # 2-factors via u maps of pairs
                facs = {}
                for s in S:
                    for r in R.mates(s):
                        u = {t: [w for w in t if w != r[t] and w != s[t]][0] for t in R.A}
                        key = frozenset(u.items())
                        facs.setdefault(key, []).append((r, s))
                keys = list(facs)
                O = {k: orientation(R, dict(k)) for k in keys}
                mins, maxs = [], []
                for k1 in keys:
                    cw = ccw = False
                    for k2 in keys:
                        if k1 == k2:
                            continue
                        for c in diff_cycles(O[k1], O[k2]):
                            if area(P, c) > 0:
                                ccw = True
                            else:
                                cw = True
                    if not ccw:
                        mins.append(k1)
                    if not cw:
                        maxs.append(k1)
                assert len(mins) == 1 and len(maxs) == 1, (len(mins), len(maxs))
                has = lambda k: any(frozenset(s.items()) in TMset for (r, s) in facs[k])
                stat['inst'] += 1
                a, b = has(mins[0]), has(maxs[0])
                stat['min_has_tree_pair'] += a; stat['max_has_tree_pair'] += b; stat['either'] += a or b
        print(V, stat, flush=True)
