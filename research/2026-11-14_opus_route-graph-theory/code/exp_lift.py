"""E15: check of Lemma L (degree-4 lift): every state s' of T' has exactly one state s of T
with pi(s) = s', and Q_s = split(Q_s') + {x c1} + {c2 v*}.  Usage: python exp_lift.py Vmax"""
import sys, collections
from tri import load
from states import Rooted
from exp_induction import contract

Vmax = int(sys.argv[1])
for V in range(8, Vmax + 1):
    c = collections.Counter()
    for T in load(V):
        for f in T.faces():
            R = Rooted(T, f)
            S = R.states()
            for x in T.V:
                if len(T.rot[x]) != 4 or x in f:
                    continue
                for i in (0, 1):
                    res = contract(T, x, i)
                    if res is None:
                        continue
                    T2, v1, v2 = res
                    ren = lambda w: v1 if w == v2 else w
                    R2 = Rooted(T2, tuple(ren(w) for w in f))
                    a, b = T.rot[x][(i + 1) % 4], T.rot[x][(i + 3) % 4]
                    bet = [t for t in R.A if x in t]
                    proj = collections.Counter()
                    qok = True
                    for s in S:
                        if any(s[t] in (a, b) for t in bet):
                            continue
                        key = frozenset((frozenset(ren(w) for w in t), ren(s[t])) for t in R.A if x not in t)
                        proj[key] += 1
                        # Q formula: Q_s minus edges at x and minus {c2,v*} equals split(Q_s')
                        Qs = {frozenset(e) for e in R.Q(s)}
                        tx = [t for t in bet if s[t] == x][0]
                        cv = frozenset(w for w in tx if w != x)       # {c2, v*}
                        to = [t for t in bet if s[t] != x][0]
                        xc = frozenset(w for w in to if w != s[to])   # {x, c1}
                        if not (cv in Qs and xc in Qs and x in xc):
                            qok = False
                        rest = {frozenset(ren(w) for w in e) for e in Qs - {cv, xc}}
                        s2 = {}
                        for t2 in R2.A:
                            s2[t2] = [vv for (kk, vv) in key if kk == frozenset(t2)][0]
                        if rest != {frozenset(e) for e in R2.Q(s2)}:
                            qok = False
                    S2 = {frozenset((frozenset(t), s2[t]) for t in R2.A) for s2 in R2.states()}
                    c['cases'] += 1
                    c['bijective'] += (set(proj) == S2 and all(v == 1 for v in proj.values()))
                    c['Q formula'] += qok
    print(V, dict(c), flush=True)
