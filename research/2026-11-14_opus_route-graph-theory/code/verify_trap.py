"""Independent check of a saved trap file: rebuild T from its rotation system, verify
(r,s) is a pair, report k(s), then for every mate r' of s and every D(r',s)-cycle report
k after the swap; then 2-step lookahead (any two consecutive D-swaps / Q-reversals).
Usage: python verify_trap.py data/deeptrap_50_1.json"""
import sys, json, itertools
from tri import Tri
from states import Rooted
from pairs import fmap, fcycles, dcycles, d_swap, q_reverse, is_pair

d = json.load(open(sys.argv[1]))
T = Tri({int(k): v for k, v in d["rot"].items()})
T.check(); assert T.is_eulerian()
R = Rooted(T, tuple(d["t0"]))
assert not R.black_inner_sep_triangles()
fs = {frozenset(t): t for t in R.A}
r = {fs[frozenset(t)]: v for t, v in d["r"]}
s = {fs[frozenset(t)]: v for t, v in d["s"]}
assert is_pair(R, r, s)
k = lambda r, s: len(fcycles(R, fmap(R, r, s)))
print("V =", len(T.V), "separating triangles:", len(T.separating_triangles()), "k(s) =", k(r, s))
qcs = fcycles(R, fmap(R, r, s))
mates = []
for mask in itertools.product((0, 1), repeat=len(qcs)):
    r2 = r
    for bb, c in zip(mask, qcs):
        if bb:
            r2, _ = q_reverse(R, r2, s, c)
    mates.append(r2)
one = []
for r2 in mates:
    ks = [k(*d_swap(R, r2, s, D)) for D in dcycles(R, r2, s)]
    one.append(ks)
    print("mate: D-cycle lengths", [len(D) for D in dcycles(R, r2, s)], "k after swap", ks)
print("single-step decrease possible:", any(min(x) < k(r, s) for x in one))
# two-step lookahead over pairs reachable by one move (D-swap with any mate)
best2 = 10**9
for r2 in mates:
    for D in dcycles(R, r2, s):
        r3, s3 = d_swap(R, r2, s, D)
        qc3 = fcycles(R, fmap(R, r3, s3))
        m3 = []
        for mask in itertools.product((0, 1), repeat=len(qc3)):
            rr = r3
            for bb, c in zip(mask, qc3):
                if bb:
                    rr, _ = q_reverse(R, rr, s3, c)
            m3.append(rr)
        for rr in m3:
            for D2 in dcycles(R, rr, s3):
                best2 = min(best2, k(*d_swap(R, rr, s3, D2)))
print("best k after two D-swaps:", best2)
