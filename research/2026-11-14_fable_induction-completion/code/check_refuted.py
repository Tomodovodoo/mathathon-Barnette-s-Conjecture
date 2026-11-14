"""Confirms the stated counterexamples of route-induction/data/failed_inductions.json
with this folder's own code. The author's root index t0 refers to his face order, which
I do not reproduce; for each (V, gid, x, merge) I search all roots and print the roots
at which the claimed failure occurs. usage: python check_refuted.py"""
import itertools, json, gzip
import et
from census import pattern_leaves


def setups(blacks, whites, t0):
    for (x, a, v1, b, v2) in et.degree4_setups(blacks, whites, t0):
        yield (x, a, v1, b, v2)
        yield (x, v1, a, v2, b)


def data(nv, gid, x=None, merge=None):
    rot = et.plantri(nv)[gid]
    for blacks, ri, whites in et.rooted_instances(rot):
        t0 = blacks[ri]
        tm = et.tree_matchings(blacks, ri, nv)
        for (xx, A_, V1, B_, V2) in setups(blacks, whites, t0):
            if x is not None and xx != x:
                continue
            if merge is not None and {V1, V2} != set(merge):
                continue
            nb = (A_, V1, B_, V2)
            outer, leaves = pattern_leaves(blacks, ri, nv, xx, nb, want_assign=True)
            res = et.contract(blacks, ri, xx, V1, V2)
            yield dict(blacks=blacks, ri=ri, whites=whites, t0=t0, tm=tm, x=xx, nb=nb,
                       outer=outer, leaves=leaves, res=res)


def classes(d):
    A_, V1, B_, V2 = d["nb"]
    lifts = fails = Bcnt = tmc = C = lc_ok = 0
    outer = d["outer"]
    for (m, c, assign) in d["leaves"]:
        ca, cv1, cb, cv2 = c
        is_tm = (m in (V2, B_) and ca != cv1) or (m in (V1, A_) and cb != cv2)
        if m in (V1, V2):
            if cv1 != cv2:
                tmc += 1
                lifts += is_tm
                fails += not is_tm
                if m == V2:
                    g = next(f for f in outer if A_ in f and V2 in f)
                    lc_ok += assign[outer.index(g)] not in (A_, V2)
                else:
                    g = next(f for f in outer if B_ in f and V1 in f)
                    lc_ok += assign[outer.index(g)] not in (B_, V1)
            elif is_tm:
                Bcnt += 1
        elif is_tm:
            C += 1
    return dict(TMc=tmc, lifts=lifts, fails=fails, B=Bcnt, C=C, LC=lc_ok)


def cmin(blacks, ri, nv):
    t0 = blacks[ri]
    A = [f for i, f in enumerate(blacks) if i != ri]
    states = []
    et.enum(A, t0, [], nv, lambda assign, find: states.append(tuple(assign)), acyclic=False)
    best = None
    for r in states:
        for s in states:
            if any(p == q for p, q in zip(r, s)):
                continue
            nxt = dict(zip(r, s))
            seen = set(); c = 0
            for v in nxt:
                if v not in seen:
                    c += 1
                    while v not in seen:
                        seen.add(v); v = nxt[v]
            best = c if best is None else min(best, c)
    return best


print("R1 V=6 x=3 merge {5,0}:", [(d["t0"], classes(d), et.is_simple(d["res"][0])) for d in data(6, 0, 3, (5, 0))][:2])
print("R1/R2 V=11 gid 1 x=5 merge {6,4}:")
for d in data(11, 1, 5, (6, 4)):
    cb, cri = d["res"]
    k = classes(d)
    if k["B"] > 0 and k["TMc"] == 0:
        print("   root", d["t0"], "TM(T)", d["tm"], "M-type TMs not projecting to TMs", k["B"],
              "simple", et.is_simple(cb), "pair(T/M)", et.has_pair_flow(cb, cri), "pair(T)", et.has_pair_flow(d["blacks"], d["ri"]))
print("R3/R4/R7 V=8 x=4 merge {5,0}:")
for d in data(8, 0, 4, (5, 0)):
    k = classes(d)
    if k["fails"]:
        print("   root", d["t0"], "TM(T)", d["tm"], k, "rootnbrs", [v for v in d["nb"] if v in d["t0"]])
print("R3 root-free V=10 gid 1 x=8 merge {9,7}:")
for d in data(10, 1, 8, (9, 7)):
    k = classes(d)
    if k["fails"] and not any(v in d["t0"] for v in d["nb"]):
        print("   root", d["t0"], "TM(T)", d["tm"], k)
print("R5 V=10 gid 1 x=9 merge {2,8}:")
for d in data(10, 1, 9, (2, 8)):
    k = classes(d)
    if k["TMc"] and k["LC"] == 0:
        print("   root", d["t0"], k)
print("R6 membership in my exception list:")
rows = [json.loads(l) for l in open("../data/exceptions_6_13.jsonl")]
rows += [json.loads(l) for l in gzip.open("../data/exceptions_14_17.jsonl.gz", "rt")]
print("   V=13 gid 7 x=10 merge {8,4}:", [(r["t0"], r["rootnbrs"]) for r in rows if r["V"] == 13 and r["gid"] == 7 and r["x"] == 10 and {r["v1"], r["v2"]} == {8, 4}])
print("   V=14 gid 12 x=2 merge {9,0}:", [(r["t0"], r["rootnbrs"]) for r in rows if r["V"] == 14 and r["gid"] == 12 and r["x"] == 2 and {r["v1"], r["v2"]} == {9, 0}])
print("   smallest V with an exception:", min(r["V"] for r in rows), " smallest root-free:", min(r["V"] for r in rows if not r["rootnbrs"]))
print("R9 V=14 gid 7 x=12 merge {10,6}: (cmin T, cmin T/M) over roots with both pairs:")
seen = set()
for d in data(14, 7, 12, (10, 6)):
    cb, cri = d["res"]
    if et.is_simple(cb) and et.has_pair_flow(cb, cri):
        seen.add((cmin(d["blacks"], d["ri"], 14), cmin(cb, cri, 14)))
print("   ", sorted(seen))
print("R10 V=6: TM(T), TM(T/M)+TM(T/N):", {(d["tm"], classes(d)["TMc"]) for d in data(6, 0, 3)})
print("R10 strict V=13 gid 7 x=10:")
agg = {}
for d in data(13, 7, 10):
    agg.setdefault(d["t0"], [d["tm"]]).append(classes(d)["TMc"])
print("   roots with TM(T) < TM(T/M)+TM(T/N):", [(t, v) for t, v in agg.items() if v[0] < sum(v[1:])])
print("R11 V=8: face (3,6,5), corner 3:")
rot = et.plantri(8)[0]
for blacks, ri, whites in et.rooted_instances(rot):
    fs = [f for f in blacks if set(f) == {3, 6, 5}]
    if fs and blacks[ri] != fs[0] and 3 not in blacks[ri]:
        tms = et.tree_matchings(blacks, ri, 8, collect=True)
        print("   root", blacks[ri], "TMs", len(tms), "with s(t)=3:", sum(1 for s in tms if s[fs[0]] == 3))
print("R12 V=9: roots with a pair but no contraction keeping a pair:")
rot = et.plantri(9)[0]
for blacks, ri, whites in et.rooted_instances(rot):
    if not et.has_pair_flow(blacks, ri):
        continue
    good = False
    for (x, A_, V1, B_, V2) in setups(blacks, whites, blacks[ri]):
        res = et.contract(blacks, ri, x, V1, V2)
        if res and et.is_simple(res[0]) and et.has_pair_flow(*res):
            good = True
    if not good:
        print("   root", blacks[ri])
