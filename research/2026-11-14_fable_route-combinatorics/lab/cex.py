"""Prints the counterexamples quoted in ROUTES.md.  usage: python cex.py"""
from collections import defaultdict
from tri import enumerate_classes, from_code
from rooted import Rooted
from analyze import analyze

L = enumerate_classes(16)


def load(v, ci, t0):
    T = from_code(L[v][ci])
    R = Rooted(T, t0)
    res, ex = analyze(R, deep=False)
    return T, R, res, ex


def header(name, v, ci, t0, T, R, res):
    print("=" * 78)
    print(name)
    print(f"T = class {ci} with {v} vertices; faces (counterclockwise):")
    print("  ", T.faces)
    print(f"t0 = face {t0} = {T.faces[t0]}; n = {R.n}; A = {[T.faces[f] for f in R.A]}")
    print("  stats:", res)


# E1 / E2 / E5: top partnered state is not a tree matching
v, ci, t0 = 12, 6, 8
T, R, res, ex = load(v, ci, t0)
header("E1, E2, E5 refuted: the highest partnered state is not a tree matching", v, ci, t0, T, R, res)
om, partnered, info = ex['om'], ex['partnered'], ex['info']
mx = max(om[s] for s in partnered)
for s in partnered:
    if om[s] == mx:
        print("  top partnered state s =", s, "rank", om[s], "cycles of Q_s:",
              [[x for (_, x, _) in c] for c in info[s][2]])
print("  ranks and signs of the tree matchings:", sorted((om[s], ex['mu'][s]) for s in ex['trees']))

# E1c: lowest partnered state is not a tree matching
v, ci, t0 = 14, 21, 13
T, R, res, ex = load(v, ci, t0)
header("E1c, E5b refuted: the lowest partnered state is not a tree matching", v, ci, t0, T, R, res)
om, partnered, info = ex['om'], ex['partnered'], ex['info']
mn = min(om[s] for s in partnered)
for s in partnered:
    if om[s] == mn:
        print("  bottom partnered state s =", s, "rank", om[s], "cycles of Q_s:",
              [[x for (_, x, _) in c] for c in info[s][2]])
print("  ranks and signs of the tree matchings:", sorted((om[s], ex['mu'][s]) for s in ex['trees']))

# E3: a cycle cover D none of whose orientations is a forest pair
v, ci, t0 = 16, 158, 8
T, R, res, ex = load(v, ci, t0)
header("E3 refuted: a cycle cover D with no forest pair among its orientations", v, ci, t0, T, R, res)
byD = defaultdict(list)
for p in ex['pairs']:
    byD[p[4]].append(p)
treeset = set(ex['trees'])
for Dk, ps in byD.items():
    if not any(p[1] in treeset for p in ps):
        print("  D has", len(ex['Dinfo'][Dk]), "cycles (counterclockwise vertex lists):",
              [[t for (_, t, _) in c] for c in ex['Dinfo'][Dk]], "areas", ex['areas'][Dk])
        for p in ps:
            print("    orientation ccw-flags", p[5], " s =", p[1], " Q_s cycles:",
                  [[x for (_, x, _) in c] for c in ex['info'][p[1]][2]])

# Z1: quotient Z/(q-1)^m with mixed signs
v, ci, t0 = 14, 24, 6
T, R, res, ex = load(v, ci, t0)
header("Z1 refuted: Z(q)/(q-1)^cmin has coefficients of both signs", v, ci, t0, T, R, res)
print("  (rank, sign) of the tree matchings:", sorted((ex['om'][s], ex['mu'][s]) for s in ex['trees']))
