"""Numerical check of two devices of the Lean proof on real Eulerian triangulations.

Usage (from the repository root):
    python research/2026-11-14_opus_lean-formalisation/scripts/check_lean_devices.py VMAX [SEED]

Uses the triangulation generator and rooted-state code of the route-combinatorics agent
(research/2026-11-14_fable_route-combinatorics/lab/tri.py and rooted.py), read only.

For every Eulerian triangulation class with 6 <= V <= VMAX and every choice of outer face t0:

W (white-charge weights, Lean ColoredDual.weights / StateCycle.signed):
   take a flow F on G = T* (F(e) = flow from the black face of e to its white face) with
   net inflow 1 at every white face, net outflow #white at t0 and conservation at the other
   black faces.  We use a spanning-tree solution plus random integer circulations around
   vertices of T (so the check does not depend on the particular solution).  Weights:
   a(t, v) = potential of F around the black triangle t.  Checks, for every D-cycle C of
   every pair, oriented as given (tail -> head):
     W1  slope(C) = sum a(t,head) - a(t,tail) equals +-(number of white faces inside C);
     W2  sign coupling: sign(slope) * (delta-sum / 3) is the same for all cycles (counted
         in the output; one value only means the coupling holds with a fixed convention);
     W3  the paper's spoke weights (rooted.py, Lemma 5.3) give the same slope up to one
         global sign (counted in the output).
P (polynomial Z, Lean Pair.term / total_sum_ne_zero):
   Z(X) = sum over pairs of i^J * prod_t (1 + a(t, s(t)) X) in Z[i][X].
     P1  for every s with cyclic Q_s, the partner sum of i^J is 0;
     P2  if a pair exists, Z != 0, its lowest degree is c_min (fewest D-cycles) and the
         lowest coefficient equals (-i)^c_min * sum over D-groups with c_min cycles of the
         product of the counterclockwise slopes L+(C) - L-(C), which all have one sign.
D (disk identity on G, LESSONS-FOR-EXPOSITION.md section 2, Lean state_disk_count):
   for every D-cycle C (an r-directed state cycle), with A = faces inside C (t0 not in A):
     D0  the cut of A in G (edges of T with one face in A) is exactly the edge set of C,
         and G[A], G[V - A] are connected (bond);
     D1  3|A| + h = 2|E_A|;  D2  3|A_b| + h = |E_A| + l;  D3  |A| + |U| = |E_A| + 1;
     D4  |A_b| + h = |U| + l;  D5 every vertex of T on a face in A and a face outside lies on C;
     hence h = 2l + 3.
Output: one line per V with counts, then a summary.  Any failure raises AssertionError.
"""
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
LAB = HERE.parents[2] / "2026-11-14_fable_route-combinatorics" / "lab"
sys.path.insert(0, str(LAB))
from tri import enumerate_classes, from_code  # noqa: E402
from rooted import Rooted  # noqa: E402


def white_charge_flow(R, rng):
    T = R.T
    fc = T.fcol
    black = R.bc
    # dual graph: faces adjacent across undirected edges
    edge_faces = {}
    for (a, b), f in T.de.items():
        key = frozenset((a, b))
        edge_faces.setdefault(key, []).append(f)
    adj = defaultdict(list)
    for key, (f, g) in edge_faces.items():
        adj[f].append((g, key))
        adj[g].append((f, key))
    nwhite = sum(1 for f in range(T.F) if fc[f] != black)
    demand = {f: (1 if fc[f] != black else 0) for f in range(T.F)}
    # BFS tree from t0
    parent = {R.t0: None}
    order = [R.t0]
    for x in order:
        for (y, key) in adj[x]:
            if y not in parent:
                parent[y] = (x, key)
                order.append(y)
    F = defaultdict(int)
    sub = dict(demand)
    for x in reversed(order[1:]):
        p, key = parent[x]
        need = sub[x]
        # flow p -> x of size `need`; F measured black -> white
        F[key] += need if fc[x] != black else -need
        sub[p] += sub[x]
    assert sub[R.t0] == nwhite
    # random circulations around vertices of T
    for z in range(T.V):
        c = rng.randint(-3, 3)
        if c == 0:
            continue
        nb = T.nbrs(z)
        d = len(nb)
        for k in range(d):
            u = nb[k]
            # face on the left of z -> u is de[(z,u)], it precedes the face de[(u,z)]?  Walk
            # around z: consecutive faces share the edge (z, u).  Orient the circulation from
            # the face containing directed edge (u, z) to the face containing (z, u).
            f_from = T.de[(u, z)]
            key = frozenset((z, u))
            F[key] += c if fc[f_from] == black else -c
    # check conservation
    out = defaultdict(int)
    for key, (f, g) in edge_faces.items():
        b, w = (f, g) if fc[f] == black else (g, f)
        out[b] += F[key]
        out[w] -= F[key]
    for f in range(T.F):
        if fc[f] != black:
            assert out[f] == -1
        elif f == R.t0:
            assert out[f] == nwhite
        else:
            assert out[f] == 0
    return F


def potentials(R, F):
    T = R.T
    a = {}
    for f in R.A:
        x, y, z = T.faces[f]
        a[(f, x)] = 0
        a[(f, y)] = F[frozenset((x, y))]
        a[(f, z)] = F[frozenset((x, y))] + F[frozenset((y, z))]
        assert a[(f, z)] + F[frozenset((z, x))] == 0
    return a


def edge_faces_of(T):
    ef = {}
    for (a, b), f in T.de.items():
        ef.setdefault(frozenset((a, b)), []).append(f)
    return ef


def connected_faces(T, ef, S):
    S = set(S)
    if not S:
        return True
    adj = defaultdict(list)
    for key, (f, g) in ef.items():
        if f in S and g in S:
            adj[f].append(g)
            adj[g].append(f)
    start = next(iter(S))
    seen = {start}
    todo = [start]
    while todo:
        x = todo.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen == S


def disk_check(R, cyc, inside, ef, stats):
    T = R.T
    A = set(inside)
    assert R.t0 not in A
    h = len(cyc)
    cyc_edges = {frozenset((t, hd)) for (_, t, hd) in cyc}
    cut = {key for key, (f, g) in ef.items() if (f in A) != (g in A)}
    assert cut == cyc_edges, "D0 cut"
    assert connected_faces(T, ef, A) and connected_faces(T, ef, set(range(T.F)) - A), "D0 bond"
    EA = {key for key, (f, g) in ef.items() if f in A or g in A}
    Ab = {f for f in A if T.fcol[f] == R.bc}
    U = {v for f in A for v in T.faces[f]}
    l = sum(1 for key in cyc_edges if any(T.fcol[f] == R.bc and f in A for f in ef[key]))
    assert 3 * len(A) + h == 2 * len(EA), "D1"
    assert 3 * len(Ab) + h == len(EA) + l, "D2"
    assert len(A) + len(U) == len(EA) + 1, "D3"
    assert len(Ab) + h == len(U) + l, "D4"
    outside = {v for f in range(T.F) if f not in A for v in T.faces[f]}
    cverts = {t for (_, t, _) in cyc}
    assert (U & outside) == cverts, "D5"
    assert h == 2 * l + 3
    stats["disk checks"] += 1


def check(R, rng, stats):
    F = white_charge_flow(R, rng)
    a = potentials(R, F)
    spoke = R.weights()[0]
    ef = edge_faces_of(R.T)
    # polynomial as dict degree -> (re, im)
    Z = defaultdict(lambda: [0, 0])
    groups = {}
    any_pair = False
    for s in R.states():
        rs = R.partners(s)
        if not rs:
            continue
        any_pair = True
        valid, forced, qcycles = R.Q_structure(s)
        tot = [0, 0]
        for r in rs:
            j3 = R.J3(r, s)
            assert j3 % 3 == 0
            ph = [(1, 0), (0, 1), (-1, 0), (0, -1)][(j3 // 3) % 4]
            tot[0] += ph[0]
            tot[1] += ph[1]
            # D-cycle checks
            cyc_list = R.D_cycles(r, s)
            for cyc in cyc_list:
                verts = [t for (_, t, _) in cyc]
                ccw, inside = R.is_ccw(verts)
                dsum = sum(R.delta(t, h) for (_, t, h) in cyc)
                slope = sum(a[(R.A[i], h)] - a[(R.A[i], t)] for (i, t, h) in cyc)
                if not ccw:
                    inside = R.is_ccw(list(reversed(verts)))[1]
                nwin = sum(1 for f in inside if R.T.fcol[f] != R.bc)
                disk_check(R, cyc, inside, ef, stats)
                assert abs(slope) == nwin and nwin > 0, ("W1", slope, nwin)
                assert dsum in (-3, 3)
                stats["W2 sign(slope)*delta/3 = " + str((1 if slope > 0 else -1) * dsum // 3)] += 1
                assert (dsum == -3) == ccw
                sp = sum(spoke.get((R.A[i], h), 0) - spoke.get((R.A[i], t), 0) for (i, t, h) in cyc)
                assert sp in (slope, -slope), ("W3", sp, slope)
                stats["W3 spoke slope / flow slope = " + str(sp // slope)] += 1
                stats["cycles"] += 1
            # polynomial term
            poly = [1]
            for f, v in zip(R.A, s):
                c = a[(f, v)]
                poly = [(poly[k] if k < len(poly) else 0) + (c * poly[k - 1] if k >= 1 else 0)
                        for k in range(len(poly) + 1)]
            for k, cf in enumerate(poly):
                Z[k][0] += ph[0] * cf
                Z[k][1] += ph[1] * cf
            # group by D (undirected edge set)
            key = frozenset(frozenset((x, y)) for x, y in zip(r, s))
            if key not in groups:
                prod = 1
                signs = set()
                for cyc in cyc_list:
                    verts = [t for (_, t, _) in cyc]
                    ccw, _ = R.is_ccw(verts)
                    slope = sum(a[(R.A[i], h)] - a[(R.A[i], t)] for (i, t, h) in cyc)
                    ccw_slope = slope if ccw else -slope
                    signs.add(ccw_slope > 0)
                    prod *= ccw_slope
                stats["ccw slope positive: " + str(sorted(signs))] += 1
                groups[key] = (len(cyc_list), prod)
        if qcycles:
            assert tot == [0, 0], ("P1", tot)
            stats["cyclic_s"] += 1
        stats["pairs"] += len(rs)
    if not any_pair:
        stats["no_pair"] += 1
        return
    degs = [k for k in sorted(Z) if Z[k] != [0, 0]]
    assert degs, "P2: Z = 0"
    cmin = min(c for c, _ in groups.values())
    assert degs[0] == cmin, ("P2 degree", degs[0], cmin)
    total = sum(p for c, p in groups.values() if c == cmin)
    # all groups of degree c_min have products of the same sign (ccw slopes share one sign)
    assert len({p > 0 for c, p in groups.values() if c == cmin}) == 1
    ph = [(1, 0), (0, -1), (-1, 0), (0, 1)][cmin % 4]   # (-i)^cmin
    assert Z[cmin] == [ph[0] * total, ph[1] * total], ("P2 coeff", Z[cmin], cmin, total)
    stats["rooted_with_pair"] += 1


def main():
    vmax = int(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    classes = enumerate_classes(vmax)
    grand = defaultdict(int)
    for v in range(6, vmax + 1):
        stats = defaultdict(int)
        for code in classes[v]:
            T = from_code(code)
            stats["classes"] += 1
            for t0 in range(T.F):
                R = Rooted(T, t0)
                stats["rooted"] += 1
                check(R, rng, stats)
        print(v, dict(stats), flush=True)
        for k, x in stats.items():
            grand[k] += x
    print("all checks passed;", dict(grand))


if __name__ == "__main__":
    main()
