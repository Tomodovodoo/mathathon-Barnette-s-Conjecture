"""Independent computation of every number the draft-B manuscript states about
its worked example.

Run from the repository root:
    python research/2026-11-14_opus_manuscript-B/example.py > research/2026-11-14_opus_manuscript-B/example.txt

Input (read only): paper/figures/running.json (faces, t0, e0) and
paper/figures/layout-running.json (coordinates, used only for point-in-polygon
tests and for the height paths). Nothing here imports the figure code or the lab.

Conventions follow the manuscript:
  * faces are listed counterclockwise (bounded faces); t0 is the outer face;
  * a state s maps each bounded black face t to a nonroot corner, bijectively;
  * a pair (r, s) has r(t) != s(t) for all t;
  * D(r, s): directed edges r(t) -> s(t);  Q_s: side opposite s(t);
  * delta(v, w) = +1 if the black face of vw is on the left of v -> w;
  * J = (1/3) sum_t delta(r(t), s(t));  eps = (-1)^((n + J)/2);
  * heights: h_s(w) = signed crossings of a downward vertical ray from the
    centroid of white face w with the spokes c_t -> s(t), +1 when the spoke
    crosses the ray from its right to its left;  omega(s) = sum_w h_s(w).
"""
import itertools as it
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
data = json.load(open(ROOT / 'paper/figures/running.json'))
lay = json.load(open(ROOT / 'paper/figures/layout-running.json'))
F = [tuple(f) for f in data['faces']]
t0 = data['t0']
e0 = tuple(sorted(data['e0']))
xy = {int(k): tuple(v) for k, v in lay['coordinates'].items()}

V = sorted({v for f in F for v in f})
left = {}
for i, f in enumerate(F):
    for a, b in zip(f, f[1:] + f[:1]):
        assert (a, b) not in left
        left[a, b] = i
E = sorted({tuple(sorted(k)) for k in left})
assert all((b, a) in left for a, b in left)

# 2-colour the faces (dual graph is bipartite)
adjF = {i: set() for i in range(len(F))}
for a, b in E:
    adjF[left[a, b]].add(left[b, a]); adjF[left[b, a]].add(left[a, b])
col = {t0: 0}
stack = [t0]
while stack:
    x = stack.pop()
    for y in adjF[x]:
        if y not in col:
            col[y] = 1 - col[x]; stack.append(y)
        else:
            assert col[y] != col[x]
black = [i for i in range(len(F)) if col[i] == 0]
white = [i for i in range(len(F)) if col[i] == 1]
roots = list(F[t0])
# white faces sharing a side with t0 have an arc side in the layout; their vertex
# centroid is not inside them. They contain two roots, so they lie outside every
# root-free cycle, and a path from them to t0 crosses that side and no spoke.
outer_white = [w for w in white if len(set(F[w]) & set(roots)) == 2]
A = [t for t in black if t != t0]
X = [v for v in V if v not in roots]
n = len(A)
assert n == len(X)
print(f'|V(T)| = {len(V)}, faces = {len(F)} ({len(black)} black, {len(white)} white), edges = {len(E)}, n = {n}')
print('roots', roots, 'e0', e0)


def blackface(a, b):
    """the black face containing edge ab"""
    i, j = left[a, b], left[b, a]
    return i if col[i] == 0 else j


def delta(v, w):
    return 1 if col[left[v, w]] == 0 else -1


def third(t, a, b):
    (c,) = [v for v in F[t] if v not in (a, b)]
    return c


# states
cand = {t: [v for v in F[t] if v not in roots] for t in A}
states = []
for choice in it.product(*[cand[t] for t in A]):
    if len(set(choice)) == n:
        states.append(dict(zip(A, choice)))
print('states:', len(states))
key = lambda s: tuple(s[t] for t in A)
pairs = [(r, s) for r in states for s in states if all(r[t] != s[t] for t in A)]
print('ordered pairs:', len(pairs))


def cycles_of_perm(succ):
    seen, cyc = set(), []
    for v in succ:
        if v in seen:
            continue
        c = [v]
        seen.add(v)
        w = succ[v]
        while w != v:
            c.append(w); seen.add(w); w = succ[w]
        cyc.append(c)
    return cyc


def signed_area(cyc):
    a = 0.0
    for p, q in zip(cyc, cyc[1:] + cyc[:1]):
        a += xy[p][0] * xy[q][1] - xy[q][0] * xy[p][1]
    return a / 2


def centroid(i):
    f = F[i]
    return (sum(xy[v][0] for v in f) / 3, sum(xy[v][1] for v in f) / 3)


def inside(pt, cyc):
    x, y = pt
    c = False
    for p, q in zip(cyc, cyc[1:] + cyc[:1]):
        (x1, y1), (x2, y2) = xy[p], xy[q]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                c = not c
    return c


def D(r, s):
    return cycles_of_perm({r[t]: s[t] for t in A})


def J(r, s):
    tot = sum(delta(r[t], s[t]) for t in A)
    assert tot % 3 == 0
    return tot // 3


def eps(r, s):
    j = J(r, s)
    assert (n + j) % 2 == 0
    return (-1) ** ((n + j) // 2)


def Q(s):
    return [tuple(sorted(v for v in F[t] if v != s[t])) for t in A]


def find_cycle(edges):
    """return a cycle (vertex list) in an undirected simple edge list or None"""
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    parent = {}
    for start in adj:
        if start in parent:
            continue
        parent[start] = None
        stack = [(start, None)]
        while stack:
            v, p = stack.pop()
            for w in adj[v]:
                if w == p:
                    continue
                if w in parent:
                    # reconstruct
                    path_v = [v]
                    while parent[path_v[-1]] is not None:
                        path_v.append(parent[path_v[-1]])
                    path_w = [w]
                    while parent[path_w[-1]] is not None:
                        path_w.append(parent[path_w[-1]])
                    common = next(x for x in path_v if x in path_w)
                    cyc = path_v[:path_v.index(common) + 1] + list(reversed(path_w[:path_w.index(common)]))
                    return cyc
                parent[w] = v
                stack.append((w, v))
    return None


def components(vertices, edges):
    comp = {v: v for v in vertices}

    def find(x):
        while comp[x] != x:
            comp[x] = comp[comp[x]]; x = comp[x]
        return x
    for a, b in edges:
        comp[find(a)] = find(b)
    groups = {}
    for v in vertices:
        groups.setdefault(find(v), []).append(v)
    return list(groups.values())


# heights: ray from centroid of w straight down; segment c_t -> v
cent = {t: centroid(t) for t in A}


def kappa(w, t, v):
    px, py = centroid(w)
    (ax, ay), (bx, by) = cent[t], xy[v]
    if (ax - px) * (bx - px) > 0 or ax == bx:
        return 0
    # x-crossing of the vertical line x = px
    lam = (px - ax) / (bx - ax)
    yc = ay + lam * (by - ay)
    if yc >= py:
        return 0
    # ray points in -y; its left side is +x... ray direction (0,-1): left = (+1, 0)? rotate ccw: (1,0)
    # spoke direction (bx-ax): moving from x<px (right side of downward ray is -x) to x>px is right->left
    return 1 if bx > ax else -1


def h(s, w):
    if w in outer_white:
        return 0
    return sum(kappa(w, t, s[t]) for t in A)


def omega(s):
    return sum(h(s, w) for w in white)


print()
print('Faces (index: vertices, colour):')
for i, f in enumerate(F):
    print(f'  {i:2d}: {f} {"black" if col[i]==0 else "white"}{"  <- t0" if i==t0 else ""}')

print()
print('Pairs:')
mins = None
info = []
for idx, (r, s) in enumerate(pairs):
    cyc = D(r, s)
    orient = ['ccw' if signed_area(c) > 0 else 'cw' for c in cyc]
    nccw, ncw = orient.count('ccw'), orient.count('cw')
    j = J(r, s)
    assert j == ncw - nccw, (j, ncw, nccw)
    qcyc = find_cycle(Q(s))
    qcomp = components(V, Q(s))
    info.append((r, s, cyc, orient, j, qcyc))
    print(f'  #{idx}: r={key(r)} s={key(s)} J={j} eps={eps(r, s):+d} D-cycles={[(c, o) for c, o in zip(cyc, orient)]} '
          f'Q_s cycle={qcyc} omega(s)={omega(s)}')
    # disk identity checks on every D-cycle
    for c, o in zip(cyc, orient):
        hh = len(c)
        ccw = c if o == 'ccw' else list(reversed(c))
        I = [v for v in V if v not in c and inside(xy[v], ccw)]
        Bf = [t for t in A if inside(centroid(t), ccw)]
        Wf = [t for t in white if t not in outer_white and inside(centroid(t), ccw)]
        l = sum(1 for p, q in zip(ccw, ccw[1:] + ccw[:1]) if col[left[p, q]] == 0)
        assert len(Wf) == len(Bf) + 1 and hh - 2 * l == 3 and len(Bf) == len(I) + l
        print(f'      cycle {c}: h={hh} I={len(I)} B={len(Bf)} W={len(Wf)} l={l}  white inside={Wf}')

# cancellation partner
print()
print('Cancellation (fixed s, reverse the Q_s cycle):')
for (r, s, cyc, orient, j, qcyc) in info:
    if qcyc is None:
        continue
    # faces supplying qcyc edges
    qset = {tuple(sorted(e)) for e in zip(qcyc, qcyc[1:] + qcyc[:1])}
    r2 = dict(r)
    for t in A:
        e = tuple(sorted(v for v in F[t] if v != s[t]))
        if e in qset:
            r2[t] = third(t, r[t], s[t])
    assert (r2, s) in pairs
    print(f'  r={key(r)} -> r~={key(r2)} with s={key(s)}: J {J(r, s)} -> {J(r2, s)}, eps {eps(r, s):+d} -> {eps(r2, s):+d}')

# minimal cycle count and the signed sum
m = min(len(c) for (_, _, c, _, _, _) in info)
print()
print('m (fewest D-cycles) =', m)
total = sum(eps(r, s) * omega(s) ** m for r, s in pairs)
tm = [(r, s) for (r, s, cyc, o, j, q) in info if q is None]
print('forest pairs:', len(tm), 'signs', [eps(r, s) for r, s in tm])
print('sum over all pairs eps * omega(s)^m =', total)
print('sum over forest pairs eps * omega(s)^m =', sum(eps(r, s) * omega(s) ** m for r, s in tm))
# group by undirected D
groups = {}
for (r, s, cyc, o, j, q) in info:
    k = frozenset(frozenset((r[t], s[t])) for t in A)
    groups.setdefault(k, []).append((r, s, cyc))
pred = 0
for k, g in groups.items():
    c = len(g[0][2])
    Ls = []
    for cyc in g[0][2]:
        ccw = cyc if signed_area(cyc) > 0 else list(reversed(cyc))
        Ls.append(sum(1 for w in white if w not in outer_white and inside(centroid(w), ccw)))
    contrib = sum(eps(r, s) * omega(s) ** m for r, s, _ in g)
    print(f'  group with {c} cycle(s), white faces inside each = {Ls}, size {len(g)}, contribution {contrib}')
    if c == m:
        pred += (-1) ** ((n - m) // 2) * math.factorial(m) * math.prod(Ls)
print('predicted (-1)^((n-m)/2) m! sum prod L =', pred)
assert pred == total

# height change check: for every pair and every D-cycle, reversing it cw->ccw raises h(w) by [w inside]
for (r, s, cyc, o, j, q) in info:
    for c, ori in zip(cyc, o):
        if ori != 'cw':
            continue
        cs = {r[t] for t in A if r[t] in c}
        r2, s2 = dict(r), dict(s)
        for t in A:
            if r[t] in c:
                r2[t], s2[t] = s[t], r[t]
        ccw = list(reversed(c))
        for w in white:
            assert h(s2, w) - h(s, w) == (1 if (w not in outer_white and inside(centroid(w), ccw)) else 0)
print('height increments checked on every clockwise D-cycle of every pair')

# recovery from a forest pair
print()
print('Recovery:')
for (r, s, cyc, o, j, q) in info:
    if q is not None:
        continue
    a, b = e0
    (c0,) = [v for v in roots if v not in e0]
    Sedges = Q(s) + [tuple(sorted((a, c0))), tuple(sorted((b, c0)))]
    assert find_cycle(Sedges) is None and len(components(V, Sedges)) == 1
    # face tree Y: faces adjacent across edges not in S
    Sset = set(Sedges)
    Yadj = {i: [] for i in range(len(F))}
    for e in E:
        if e not in Sset:
            i, k = left[e], left[e[1], e[0]]
            Yadj[i].append((k, e)); Yadj[k].append((i, e))
    # root at t0 and orient
    parent = {t0: None}
    order = [t0]
    for x in order:
        for (y, e) in Yadj[x]:
            if y not in parent:
                parent[y] = (x, e); order.append(y)
    assert len(order) == len(F)
    for t in A:
        assert len(Yadj[t]) == 2
    assert len(Yadj[t0]) == 1
    P = set()
    for y in white:
        P.add(parent[y][1])
    # check selection
    for i in range(len(F)):
        k = sum(1 for e in P if set(e) <= set(F[i]))
        assert k == 1
    assert e0 in P
    assert find_cycle(list(P)) is None
    comps = components(V, list(P))
    # Ham cycle in G: faces adjacent across edges not in P
    Hadj = {i: [] for i in range(len(F))}
    for e in E:
        if e not in P:
            i, k = left[e], left[e[1], e[0]]
            Hadj[i].append(k); Hadj[k].append(i)
    assert all(len(Hadj[i]) == 2 for i in Hadj)
    cyc = [t0]
    prev = None
    while True:
        nxt = [y for y in Hadj[cyc[-1]] if y != prev][0] if prev is not None else Hadj[t0][0]
        if nxt == t0:
            break
        prev = cyc[-1]
        cyc.append(nxt)
    assert len(cyc) == len(F)
    print(f'  s={key(s)}: S = Q_s + root sides spanning tree; P = {sorted(P)}')
    print(f'     P components: {comps}; Hamiltonian cycle of G (faces): {cyc}')
    # induced trees
    for comp in comps:
        ind = [e for e in E if set(e) <= set(comp)]
        assert len(ind) == len(comp) - 1
print('all recovered P are acyclic selections; both classes induce trees')
