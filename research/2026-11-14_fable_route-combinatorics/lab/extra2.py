"""Independent check of the partner structure.  usage: python lab/extra2.py VMAX

X4  for every state s, the set of partners computed from the cycles of Q_s
    (rooted.partners) equals the set of states disjoint from s found by brute force
    over all states.  Hence: s has exactly one partner  <=>  Q_s is a forest with one
    root per component (trees paper, Theorem 1.2, last sentence).
"""
import sys
from tri import enumerate_classes, from_code
from rooted import Rooted

vmax = int(sys.argv[1])
L = enumerate_classes(vmax)
nstates = npairs = ntree = 0
for v in range(6, vmax + 1):
    for code in L[v]:
        T = from_code(code)
        for t0 in range(T.F):
            R = Rooted(T, t0)
            st = R.states()
            for s in st:
                brute = {r for r in st if all(a != b for a, b in zip(r, s))}
                fast = set(R.partners(s))
                assert brute == fast
                valid, forced, cycles = R.Q_structure(s)
                assert (len(brute) == 1) == (valid and not cycles)
                nstates += 1
                npairs += len(brute)
                ntree += len(brute) == 1
print(f"X4 states {nstates}, pairs {npairs}, states with exactly one partner {ntree}: all consistent")
