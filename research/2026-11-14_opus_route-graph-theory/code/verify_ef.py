"""Independent check of a saved 2-factor without tree pair; also tests whether the lattice
min / max (face flips) of that instance contain a tree pair.
Usage: python verify_ef.py data/ef_fail_40_40.json"""
import sys, json, collections
from tri import Tri
from states import Rooted
from alpha import pairs_of_factor, flip_to_extreme
from exp_alpha import tutte_positions

d = json.load(open(sys.argv[1]))
T = Tri({int(k): v for k, v in d["rot"].items()}); T.check(); assert T.is_eulerian()
R = Rooted(T, tuple(d["t0"]))
print("V =", len(T.V), "n =", R.n, "separating triangles:", len(T.separating_triangles()),
      "black-inner:", len(R.black_inner_sep_triangles()))
fs = {frozenset(t): t for t in R.A}
u = {fs[frozenset(t)]: v for t, v in d["u"]}
cnt = collections.Counter()
for t in R.A:
    assert u[t] in t
    for w in t:
        if w != u[t]:
            cnt[w] += 1
assert all(cnt[x] == 2 for x in R.X) and all(cnt[r] == 0 for r in R.R), "not a 2-factor of B"
prs = list(pairs_of_factor(R, u))
print("cycles in the 2-factor:", (len(prs)).bit_length() - 1, "ordered pairs:", len(prs),
      "tree pairs among them:", sum(R.is_tree_matching(s) for r, s in prs))
P = tutte_positions(R)
for sense, name in ((+1, "min"), (-1, "max")):
    ue = flip_to_extreme(R, u, sense, P)
    pe = list(pairs_of_factor(R, ue))
    print(name, "2-factor: same as failing one?", ue == u, " tree pairs:", sum(R.is_tree_matching(s) for r, s in pe), "of", len(pe))
