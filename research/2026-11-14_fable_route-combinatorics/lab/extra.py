"""Two extra checks quoted in ROUTES.md and PROOF.md.  usage: python extra.py VMAX

X1  if (r, s) maximises omega(s) - omega(r) over all pairs, every cycle of Q_s,
    directed by r, is counterclockwise.
X2  the vertex 3-colouring satisfies delta(v, w) = +1  <=>  col(w) = col(v) + kappa,
    kappa = +1 if the black faces read 0,1,2 counterclockwise.
X3  counts for line E1 of the survey (highest partnered state).
"""
import sys
from tri import enumerate_classes, from_code
from rooted import Rooted
from analyze import analyze

vmax = int(sys.argv[1])
L = enumerate_classes(vmax)
x1 = x2 = 0
e1_every = e1_some = withpair = 0
for v in range(6, vmax + 1):
    for code in L[v]:
        T = from_code(code)
        col = T.vertex_colouring()
        for t0 in range(T.F):
            R = Rooted(T, t0)
            kappa = 1 if T.fcol[0] == R.bc else -1
            for (a, b) in T.de:
                assert (R.delta(a, b) == 1) == ((col[b] - col[a]) % 3 == kappa % 3)
            x2 += 1
            res, ex = analyze(R, deep=False)
            if ex is None:
                continue
            withpair += 1
            om, pairs, info = ex['om'], ex['pairs'], ex['info']
            best = max(om[p[1]] - om[p[0]] for p in pairs)
            for p in pairs:
                if om[p[1]] - om[p[0]] == best:
                    r, s = p[0], p[1]
                    for cyc in info[s][2]:
                        # direct the cycle by r: tail of the edge in face i is r[i]
                        i0, x, y = cyc[0]
                        verts = [a_ for (_, a_, _) in cyc] if r[i0] == x else [b_ for (_, _, b_) in reversed(cyc)]
                        assert R.is_ccw(verts)[0]
                    x1 += 1
            treeset = set(ex['trees'])
            mx = max(om[s] for s in ex['partnered'])
            tops = [s for s in ex['partnered'] if om[s] == mx]
            e1_every += all(s in treeset for s in tops)
            e1_some += any(s in treeset for s in tops)
print("X1 maximising pairs checked:", x1, "all Q_s cycles counterclockwise")
print("X2 rooted triangulations with colouring = delta:", x2)
print(f"X3 with pair {withpair}; every top partnered state is a tree matching in {e1_every}; some in {e1_some}")
