"""Probe: for failing lifts s1 in TM(T') pick other-type TMs of T and show the difference."""
import sys
from tri import *
from exp_contract import project, key
from collections import Counter
V = int(sys.argv[1]); maxshow = int(sys.argv[2])
shown = 0; hist = Counter(); match_ok = Counter()
for gid, rot in enumerate(plantri(V)):
    T = from_rotation(rot)
    cons = list(contractions(T))
    for t0 in range(len(T.F)):
        R = T.rooted(t0)
        if not R.TMs(): continue
        for c in cons:
            if t0 in c['faces'] or c['loop']: continue
            if len({c['p'], c['q'], c['o1'], c['o3']} & set(R.R)): continue
            Rn = c['T'].rooted(c['fmap'][t0]); rename = {c['q']: c['p']}
            tmsN = {key(s) for s in Rn.TMs()}
            fail, other = [], []
            for s in R.states():
                sp = project(R, Rn, s, c['fmap'], rename)
                if sp is None:
                    if R.is_TM(s): other.append(s)
                elif key(sp) in tmsN and not R.is_TM(s):
                    fail.append(s)
            if not fail: continue
            # distances
            D = [[sum(1 for t in s if s[t] != o[t]) for o in other] for s in fail]
            for row in D: hist[min(row)] += 1
            # bipartite matching using only min-distance-2..k edges
            for k in (2, 3, 4, 6, 100):
                adj = [[j for j, d in enumerate(row) if d <= k] for row in D]
                m = {}
                def aug(i, seen):
                    for j in adj[i]:
                        if j in seen: continue
                        seen.add(j)
                        if j not in m or aug(m[j], seen):
                            m[j] = i; return True
                    return False
                if all(aug(i, set()) for i in range(len(fail))): match_ok[k] += 1
            if shown < maxshow:
                shown += 1
                x = c['x']; print('V', V, 'gid', gid, 't0', T.F[t0], 'x', x, 'merge', c['q'], '->', c['p'], 'o', c['o1'], c['o3'])
                for s in fail:
                    j = min(range(len(other)), key=lambda j: D[fail.index(s)][j])
                    o = other[j]
                    print('   fail lift', {T.F[t]: s[t] for t in c['faces'] if t in s}, ' nearest other', {T.F[t]: o[t] for t in c['faces'] if t in o},
                          ' diff', [(T.F[t], s[t], o[t]) for t in s if s[t] != o[t]])
print('min distance histogram', dict(hist))
print('injection by moves of distance <= k exists, cases:', dict(match_ok))
