"""Sanity checks for the nodes of the dependency graphs.

Run:  python scripts/check_nodes.py > data/check_nodes.txt
(from research/2026-11-14_fable_dependency-graph/)

Each check is tied to a node id used in the audits. The triangulations are
small (n <= 11), so this is evidence for the dictionary, not a proof.

Conventions. A triangulation is a list of oriented triples, all oriented
counterclockwise as seen from outside the sphere, so a face lies to the LEFT of
each of its directed sides. With the black face t0 put at infinity, a directed
cycle is counterclockwise iff t0 is not on its left side.
"""
import cmath
import itertools
import random
import sys

import numpy as np

random.seed(1)


# ----------------------------------------------------------------- examples
def double_wheel(m2):
    N, S = m2, m2 + 1
    faces, col = [], []
    for i in range(m2):
        j = (i + 1) % m2
        faces.append((N, i, j)); col.append(i % 2 == 0)
        faces.append((S, j, i)); col.append(i % 2 == 1)
    return faces, col


def barycentric(base):
    """Barycentric subdivision of an oriented triangulated sphere map."""
    vid = {}

    def v(key):
        return vid.setdefault(key, len(vid))

    faces, col = [], []
    for fi, (a, b, c) in enumerate(base):
        F = v(("f", fi))
        for (p, q) in ((a, b), (b, c), (c, a)):
            m = v(("e", frozenset((p, q))))
            faces.append((v(("v", p)), m, F)); col.append(True)
            faces.append((m, v(("v", q)), F)); col.append(False)
    return faces, col


def insert_octahedron(faces, col, fi):
    """Replace face fi by an octahedral cap. The 3-cycle becomes separating and
    the three new faces along it get the colour of the replaced face."""
    a, b, c = faces[fi]
    c0 = col[fi]
    nv = 1 + max(max(f) for f in faces)
    x, y, z = nv, nv + 1, nv + 2
    new = [((a, b, z), c0), ((b, c, x), c0), ((c, a, y), c0),
           ((a, z, y), not c0), ((b, x, z), not c0), ((c, y, x), not c0),
           ((x, y, z), c0)]
    F = [f for i, f in enumerate(faces) if i != fi] + [f for f, _ in new]
    C = [k for i, k in enumerate(col) if i != fi] + [k for _, k in new]
    return F, C


def split_vertex(faces, col, f, i, j):
    """Split vertex f along its neighbours n_i, n_j (j - i even) and insert a
    degree-4 vertex z. Dual to adding a square across a face of the cubic graph.
    Keeps all degrees even and the colouring proper."""
    nxt = {}
    cmap = {}
    for k, (a, b, c) in enumerate(faces):
        for (p, q, r) in ((a, b, c), (b, c, a), (c, a, b)):
            if p == f:
                nxt[q] = r
                cmap[q] = k
    start = min(nxt)
    link = [start]
    while nxt[link[-1]] != start:
        link.append(nxt[link[-1]])
    d = len(link)
    assert (j - i) % 2 == 0 and 0 <= i < j < d and j - i >= 2 and d - (j - i) >= 2
    nv = 1 + max(max(g) for g in faces)
    f2, z = nv, nv + 1
    ni, nj = link[i], link[j]
    F, C = [], []
    keep = {link[k] for k in range(i, j)}
    for k, g in enumerate(faces):
        if f in g:
            a, b, c = g
            while a != f:
                a, b, c = b, c, a
            if b not in keep:
                g = (f2, b, c)
        F.append(g); C.append(col[k])
    c_i = col[cmap[ni]]              # colour of (f, n_i, n_{i+1})
    c_j1 = col[cmap[link[j - 1]]]    # colour of (f, n_{j-1}, n_j)
    F += [(ni, f, z), (f2, ni, z), (f, nj, z), (nj, f2, z)]
    C += [not c_i, c_i, not c_j1, c_j1]
    return F, C


def random_eulerian(seed, steps, m2=4):
    rng = random.Random(seed)
    F, C = double_wheel(m2)
    for _ in range(steps):
        for _try in range(200):
            V = sorted({v for g in F for v in g})
            f = rng.choice(V)
            d = sum(1 for g in F if f in g)
            if d < 4:
                continue
            i = rng.randrange(d)
            span = rng.choice([x for x in range(2, d - 1, 2)])
            j = i + span
            if j >= d:
                i, j = j - d, i
                if (j - i) % 2 or j - i < 2 or d - (j - i) < 2:
                    continue
            try:
                F2, C2 = split_vertex(F, C, f, i, j)
                E = {}
                okay = True
                for g in F2:
                    for e in ((g[0], g[1]), (g[1], g[2]), (g[2], g[0])):
                        if e in E:
                            okay = False
                        E[e] = 1
                if okay:
                    F, C = F2, C2
                    break
            except AssertionError:
                continue
    return F, C


TETRA = [(0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3)]
OCTA = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
PYRAMID = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1)]  # plus the square base, see barycentric_map


# ------------------------------------------------------------ triangulation
class Tri:
    def __init__(self, faces, col, t0):
        self.faces, self.col, self.t0 = faces, col, t0
        self.V = sorted({v for f in faces for v in f})
        self.left = {}
        for i, (a, b, c) in enumerate(faces):
            for e in ((a, b), (b, c), (c, a)):
                assert e not in self.left, "not an oriented surface"
                self.left[e] = i
        for (a, b) in self.left:
            assert (b, a) in self.left
            assert col[self.left[(a, b)]] != col[self.left[(b, a)]], "colouring"
        deg = {v: 0 for v in self.V}
        for (a, b) in self.left:
            deg[a] += 1
        assert all(d % 2 == 0 and d >= 4 for d in deg.values())
        assert col[t0]
        self.R = set(faces[t0])
        self.X = [v for v in self.V if v not in self.R]
        self.A = [i for i in range(len(faces)) if col[i] and i != t0]
        self.n = len(self.A)
        self.black_of = {}
        for (a, b), i in self.left.items():
            if col[i]:
                self.black_of[frozenset((a, b))] = i
        self._cyc = {}

    def euler_ok(self):
        k = sum(self.col)
        E = len(self.left) // 2
        return (len(self.faces) == 2 * k and E == 3 * k
                and len(self.V) == k + 2 and len(self.X) == self.n == k - 1)

    def delta(self, v, w):
        return 1 if self.col[self.left[(v, w)]] else -1

    def left_side(self, cyc):
        """Faces on the left of the directed simple cycle cyc (vertex list)."""
        h = len(cyc)
        on = {frozenset((cyc[i], cyc[(i + 1) % h])) for i in range(h)}
        seen = {self.left[(cyc[0], cyc[1])]}
        stack = list(seen)
        while stack:
            f = stack.pop()
            a, b, c = self.faces[f]
            for (p, q) in ((a, b), (b, c), (c, a)):
                if frozenset((p, q)) in on:
                    continue
                g = self.left[(q, p)]
                if g not in seen:
                    seen.add(g); stack.append(g)
        return seen

    def cycle_data(self, cyc):
        """(is_ccw, delta_sum, B, W, I, l) for a directed simple cycle."""
        i = cyc.index(min(cyc))
        key = tuple(cyc[i:] + cyc[:i])
        if key in self._cyc:
            return self._cyc[key]
        h = len(cyc)
        L = self.left_side(cyc)
        ccw = self.t0 not in L
        inside = L if ccw else set(range(len(self.faces))) - L
        dsum = sum(self.delta(cyc[j], cyc[(j + 1) % h]) for j in range(h))
        B = sum(1 for f in inside if self.col[f])
        W = len(inside) - B
        vin = {v for f in inside for v in self.faces[f]} - set(cyc)
        l = 0
        for j in range(h):
            p, q = cyc[j], cyc[(j + 1) % h]
            f_in = self.left[(p, q)] if ccw else self.left[(q, p)]
            l += self.col[f_in]
        out = (ccw, dsum, B, W, len(vin), l)
        self._cyc[key] = out
        return out

    # states -------------------------------------------------------------
    def states(self):
        res, cur, used = [], {}, set()
        A = self.A

        def rec(j):
            if j == len(A):
                res.append(dict(cur)); return
            for v in self.faces[A[j]]:
                if v in self.R or v in used:
                    continue
                used.add(v); cur[A[j]] = v
                rec(j + 1)
                used.discard(v); del cur[A[j]]

        rec(0)
        return res

    def perm_sign(self, s):
        p = [self.X.index(s[t]) for t in self.A]
        sign, seen = 1, [False] * len(p)
        for i in range(len(p)):
            if not seen[i]:
                j, L = i, 0
                while not seen[j]:
                    seen[j] = True; j = p[j]; L += 1
                if L % 2 == 0:
                    sign = -sign
        return sign

    def qs_edges(self, s):
        out = {}
        for t in self.A:
            a, b = [v for v in self.faces[t] if v != s[t]]
            out[t] = (a, b)
        return out

    def qs_components(self, s):
        """List of (vertices, n_edges, n_roots) per component of Q_s."""
        par = {v: v for v in self.V}

        def find(v):
            while par[v] != v:
                par[v] = par[par[v]]; v = par[v]
            return v

        E = self.qs_edges(s)
        for a, b in E.values():
            par[find(a)] = find(b)
        comp = {}
        for v in self.V:
            comp.setdefault(find(v), [set(), 0, 0])[0].add(v)
        for a, b in E.values():
            comp[find(a)][1] += 1
        for v in self.R:
            comp[find(v)][2] += 1
        return list(comp.values())

    def is_tree_matching(self, s):
        return all(e == len(vs) - 1 and r == 1 for vs, e, r in self.qs_components(s))

    def b_minus_s_acyclic(self, s):
        """Is B - s acyclic (Li's 'H - M2 acyclic', no partner assumed)?"""
        par = {}

        def find(v):
            par.setdefault(v, v)
            while par[v] != v:
                par[v] = par[par[v]]; v = par[v]
            return v

        for t in self.A:
            for v in self.faces[t]:
                if v in self.R or v == s[t]:
                    continue
                a, b = find(("t", t)), find(("v", v))
                if a == b:
                    return False
                par[a] = b
        return True

    def d_cycles(self, r, s):
        nxt = {r[t]: s[t] for t in self.A}
        seen, cycles = set(), []
        for v in self.X:
            if v in seen:
                continue
            cyc, w = [], v
            while w not in seen:
                seen.add(w); cyc.append(w); w = nxt[w]
            cycles.append(cyc)
        return cycles

    def qs_directed_cycles(self, r, s):
        nxt = {}
        for t in self.A:
            (u,) = [v for v in self.faces[t] if v not in (r[t], s[t])]
            nxt[r[t]] = (u, t)
        cycles, done = [], set()
        for v in self.X:
            path, w = [], v
            pos = {}
            while w in nxt and w not in pos and w not in done:
                pos[w] = len(path); path.append(w); w = nxt[w][0]
            if w in pos:
                cycles.append(path[pos[w]:])
            done.update(path)
        return cycles, nxt

    def J3(self, r, s):
        return sum(self.delta(r[t], s[t]) for t in self.A)

    def sep_triangles(self):
        adj = {v: set() for v in self.V}
        for (a, b) in self.left:
            adj[a].add(b)
        out = []
        for a, b, c in itertools.combinations(self.V, 3):
            if b in adj[a] and c in adj[a] and c in adj[b]:
                if self.left[(a, b)] in (self.left.get((b, c)), ) and \
                        self.left[(a, b)] == self.left.get((c, a)):
                    continue
                if self.left[(b, a)] == self.left.get((a, c)) == self.left.get((c, b)):
                    continue
                cyc = [a, b, c]
                ccw = self.cycle_data(cyc)[0]
                if not ccw:
                    cyc = [a, c, b]
                inner = [self.col[self.left[(cyc[i], cyc[(i + 1) % 3])]] for i in range(3)]
                assert len(set(inner)) == 1, "cap colour not forced?"
                out.append((tuple(cyc), inner[0]))
        return out

    # recovery -----------------------------------------------------------
    def recover(self, s, e0):
        """OpenAI 6.1-6.2 / trees 7.1. Returns the two classes or None."""
        a0, b0 = e0
        y0 = self.left[(a0, b0)] if not self.col[self.left[(a0, b0)]] else self.left[(b0, a0)]
        adj = {}
        for t in self.A:
            v = s[t]
            a, b, c = self.faces[t]
            i = (a, b, c).index(v)
            nxt, prv = (a, b, c)[(i + 1) % 3], (a, b, c)[(i - 1) % 3]
            ya, yb = self.left[(nxt, v)], self.left[(v, prv)]
            adj.setdefault(ya, []).append((yb, t, (v, nxt), (v, prv)))
            adj.setdefault(yb, []).append((ya, t, (v, prv), (v, nxt)))
        P, seen, stack = [frozenset(e0)], {y0}, [y0]
        while stack:
            y = stack.pop()
            for (z, t, side_y, side_z) in adj.get(y, []):
                if z not in seen:
                    seen.add(z); stack.append(z)
                    P.append(frozenset(side_z))  # side bordering the child z
        whites = [i for i in range(len(self.faces)) if not self.col[i]]
        if len(seen) != len(whites) or len(P) != self.n + 1:
            return None
        par = {v: v for v in self.V}

        def find(v):
            while par[v] != v:
                par[v] = par[par[v]]; v = par[v]
            return v

        for e in P:
            a, b = tuple(e)
            if find(a) == find(b):
                return None
            par[find(a)] = find(b)
        classes = {}
        for v in self.V:
            classes.setdefault(find(v), set()).add(v)
        if len(classes) != 2:
            return None
        Pset = set(P)
        for (a, b) in self.left:
            if (find(a) == find(b)) != (frozenset((a, b)) in Pset):
                return None
        return list(classes.values())


def multilinear_det(tri, a):
    """[lambda_1...lambda_n] det(sum_t lambda_t W_t), W_t[v,w]=zeta^delta(v,w) a(t,w)."""
    zeta = cmath.exp(1j * cmath.pi / 6)
    n, X = tri.n, tri.X
    idx = {v: i for i, v in enumerate(X)}
    Ws = []
    for t in tri.A:
        W = np.zeros((n, n), dtype=complex)
        cs = [v for v in tri.faces[t] if v in idx]
        for v in cs:
            for w in cs:
                if v != w:
                    W[idx[v], idx[w]] = zeta ** tri.delta(v, w) * a[(t, w)]
        Ws.append(W)
    total = 0
    for mask in range(1, 1 << n):
        M = sum(Ws[i] for i in range(n) if mask >> i & 1)
        sign = -1 if (n - bin(mask).count("1")) % 2 else 1
        total += sign * np.linalg.det(M)
    return total


def subdivide4(faces, col):
    """Split every face into four. New vertices have degree 6."""
    nv = 1 + max(max(g) for g in faces)
    mid = {}

    def m(p, q):
        k = frozenset((p, q))
        if k not in mid:
            mid[k] = nv + len(mid)
        return mid[k]

    F, C = [], []
    for (a, b, c), k in zip(faces, col):
        ab, bc, ca = m(a, b), m(b, c), m(c, a)
        F += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        C += [k, k, k, not k]
    return F, C


def enumerate_pairs(T, cap):
    """All ordered pairs (r, s) of disjoint states, by backtracking over faces."""
    order, seen = [], set()
    queue = [T.A[0]]
    byv = {}
    for t in T.A:
        for v in T.faces[t]:
            byv.setdefault(v, []).append(t)
    while queue:
        t = queue.pop(0)
        if t in seen:
            continue
        seen.add(t); order.append(t)
        for v in T.faces[t]:
            if v not in T.R:
                queue += [u for u in byv[v] if u not in seen]
    order += [t for t in T.A if t not in seen]
    last = {}
    for j, t in enumerate(order):
        for v in T.faces[t]:
            last[v] = j
    res, r, s, ur, us = [], {}, {}, set(), set()

    def rec(j):
        if len(res) >= cap:
            return
        if j == len(order):
            res.append((dict(r), dict(s))); return
        t = order[j]
        cs = [v for v in T.faces[t] if v not in T.R]
        for x in cs:
            if x in ur:
                continue
            for y in cs:
                if y == x or y in us:
                    continue
                ur.add(x); us.add(y); r[t] = x; s[t] = y
                if all(last[v] != j or (v in ur and v in us) for v in cs):
                    rec(j + 1)
                ur.discard(x); us.discard(y); del r[t]; del s[t]

    rec(0)
    return res


def analyse(name, faces, col, t0, state_cap=200000, pair_cap=60000, det_n=15):
    T = Tri(faces, col, t0)
    n = T.n
    rep = {"name": name, "n": n, "euler": T.euler_ok()}
    seps = T.sep_triangles()
    rep["sep_black_inner"] = sum(1 for _, c in seps if c)
    rep["sep_white_inner"] = sum(1 for _, c in seps if not c)
    K = np.zeros((n, n))
    for i, t in enumerate(T.A):
        for v in T.faces[t]:
            if v not in T.R:
                K[i, T.X.index(v)] = 1
    M = abs(round(np.linalg.det(K)))
    rep["abs_det_K_B"] = M
    key = lambda st: tuple(st[t] for t in T.A)
    S = None
    if M <= state_cap:
        S = T.states()
        rep["states"] = len(S)
        rep["det_ok"] = len(S) == M          # trees Lemma 6.1
        rep["sign_const"] = len({T.perm_sign(st) for st in S}) <= 1
        tree_states = [st for st in S if T.is_tree_matching(st)]
        rep["tree_matchings"] = len(tree_states)
        rep["acyclicB_not_tree"] = sum(1 for st in S if T.b_minus_s_acyclic(st)
                                       and not T.is_tree_matching(st))
        a, b, c = T.faces[t0]
        rec_ok = True
        for st in tree_states[:400]:
            for e0 in ((a, b), (b, c), (c, a)):
                cl = T.recover(st, e0)
                rec_ok &= cl is not None and any(set(e0) <= k for k in cl)
        rep["recovery_ok"] = rec_ok           # OpenAI 6.1-6.2, trees 7.1
    pairs = enumerate_pairs(T, pair_cap)
    if len(pairs) >= pair_cap:
        rep["pairs"] = f">= {pair_cap} (capped, pair checks skipped)"
        return rep
    rep["pairs"] = len(pairs)
    rep["iff_ii_iii"] = (len(pairs) > 0) == (rep["sep_black_inner"] == 0)   # trees Thm 1.2
    tree_cache = {}

    def is_tree(st):
        k = key(st)
        if k not in tree_cache:
            tree_cache[k] = T.is_tree_matching(st)
        return tree_cache[k]

    mates = {}
    for r, st in pairs:
        mates[key(st)] = mates.get(key(st), 0) + 1
    ok = True
    for st in (S if S is not None else [p[1] for p in pairs]):
        comps = T.qs_components(st)
        good = all((e == len(vs) - 1 and q == 1) or (e == len(vs) and q == 0) for vs, e, q in comps)
        k = sum(1 for vs, e, q in comps if e == len(vs))
        ok &= mates.get(key(st), 0) == (2 ** k if good else 0)
        ok &= is_tree(st) == (mates.get(key(st), 0) == 1)
    rep["mates_2^k_and_unique_mate"] = ok    # trees Prop 2.1
    if not pairs:
        return rep
    rep["pairs_with_cyclic_Qs"] = sum(1 for r, st in pairs if not is_tree(st))
    pid = {(key(r), key(st)): k for k, (r, st) in enumerate(pairs)}
    par = list(range(len(pairs)))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x

    disk_ok = J_ok = flip_ok = True
    info = []
    for k0, (r, st) in enumerate(pairs):
        cyc = T.d_cycles(r, st)
        ncw = nccw = 0
        for Cy in cyc:
            ccw, dsum, B, W, I, l = T.cycle_data(Cy)
            h = len(Cy)
            disk_ok &= dsum == (-3 if ccw else 3) and B == I + l and 2 * l - h == -3 \
                and B + W == 2 * I + h - 2
            nccw += ccw; ncw += not ccw
        J3 = T.J3(r, st)
        J_ok &= J3 % 3 == 0 and J3 // 3 == ncw - nccw and (n + J3 // 3) % 2 == 0
        J = J3 // 3
        info.append((J, len(cyc), is_tree(st)))
        face_of = {r[t]: t for t in T.A}
        for Cy in cyc:                       # move (a)
            r2, s2 = dict(r), dict(st)
            for v in Cy:
                t = face_of[v]
                r2[t], s2[t] = st[t], r[t]
            q = pid[(key(r2), key(s2))]
            flip_ok &= abs(T.J3(r2, s2) // 3 - J) == 2
            par[find(q)] = find(k0)
        qc, nxt = T.qs_directed_cycles(r, st)
        for Cy in qc:                        # move (b)
            ccw, dsum, B, W, I, l = T.cycle_data(Cy)
            disk_ok &= dsum == (-3 if ccw else 3) and B == I + l
            r2 = dict(r)
            for v in Cy:
                u, t = nxt[v]
                r2[t] = u
            q = pid[(key(r2), key(st))]
            flip_ok &= abs(T.J3(r2, st) // 3 - J) == 2
            par[find(q)] = find(k0)
    rep["disk_identity_on_D_and_Qs_cycles"] = disk_ok   # OpenAI 4.1
    rep["J=cw-ccw_and_J=n_mod_2"] = J_ok                # OpenAI (5.1)
    rep["both_moves_change_J_by_2"] = flip_ok           # OpenAI 5.2, trees 4.2
    comps = {}
    for k in range(len(pairs)):
        comps.setdefault(find(k), []).append(k)
    rep["exchange_components"] = len(comps)
    bal = True
    forest_at_min = 0
    for members in comps.values():
        eps = [(-1) ** ((n + info[k][0]) // 2) for k in members if info[k][2]]
        bal &= len(eps) > 0 and sum(eps) == 0
        cmin = min(info[k][1] for k in members)
        forest_at_min += any(info[k][2] and info[k][1] == cmin for k in members)
    rep["trees_5.2_tree_pair_in_each_component_signs_balanced"] = bal
    rep["cmin_global"] = min(c for _, c, _ in info)
    rep["max_cycles"] = max(c for _, c, _ in info)
    rep["components_with_tree_pair_at_cmin"] = f"{forest_at_min} of {len(comps)}"
    hist = {}
    for J, c, tr in info:
        hist.setdefault(c, [0, 0])[tr] += 1
    rep["pairs_by_cycle_count_(cyclic,tree)"] = dict(sorted((c, tuple(v)) for c, v in hist.items()))
    # skeleton.md C1: twisted incidence determinant of Q_s
    zeta = cmath.exp(1j * cmath.pi / 6)
    by_s = {}
    for k0, (r, st) in enumerate(pairs):
        by_s.setdefault(key(st), []).append(k0)
    c1_ok = True
    for ks, members in by_s.items():
        st = pairs[members[0]][1]
        N = np.zeros((n, n), dtype=complex)
        for jt, t in enumerate(T.A):
            for v in T.faces[t]:
                if v not in T.R and v != st[t]:
                    N[T.X.index(v), jt] = zeta ** T.delta(v, st[t])
        kappa = T.perm_sign(pairs[members[0]][0])
        want = kappa * sum((1j) ** info[k][0] for k in members)
        c1_ok &= abs(np.linalg.det(N) - want) < 1e-6
        c1_ok &= (abs(want) < 1e-9) == (not is_tree(st))
    rep["twisted_incidence_det_N_s"] = c1_ok
    if n <= det_n:                           # skeleton.md lead L1
        a = {(t, v): random.uniform(0.5, 1.5) for t in T.A for v in T.faces[t]}
        w = [(1j) ** info[k][0] * np.prod([a[(t, pairs[k][1][t])] for t in T.A])
             for k in range(len(pairs))]
        lhs = sum(w)
        rhs = multilinear_det(T, a)
        rep["multilinear_det_identity"] = abs(lhs - rhs) < 1e-6 * max(1, abs(lhs))
        forest = sum(w[k] for k in range(len(pairs)) if info[k][2])
        rep["cancellation_leaves_tree_pairs"] = abs(lhs - forest) < 1e-6 * max(1, abs(lhs))
    return rep


def black_face(faces, col, pred=lambda f: True):
    return next(i for i, f in enumerate(faces) if col[i] and pred(f))


def main():
    cases = []
    for m2 in (4, 6, 8, 10, 12):
        F, C = double_wheel(m2)
        cases.append((f"double wheel rim {m2}", F, C, 0))
    F, C = barycentric(TETRA)
    cases.append(("barycentric K4 (dual truncated octahedron)", F, C, 0))
    # separating triangles
    F, C = double_wheel(6)
    w = next(i for i in range(len(F)) if not C[i])
    F1, C1 = insert_octahedron(F, C, w)
    cases.append(("DW6 + octahedron in a white face (white inner)", F1, C1, black_face(F1, C1, lambda f: max(f) < 8)))
    b = next(i for i in range(len(F)) if C[i] and i != 0)
    F2, C2 = insert_octahedron(F, C, b)
    cases.append(("DW6 + octahedron in a black face, t0 outside (black inner)", F2, C2,
                  black_face(F2, C2, lambda f: max(f) < 8)))
    cases.append(("same triangulation, t0 inside the cap", F2, C2, len(F2) - 1))
    F, C = double_wheel(8)
    w = next(i for i in range(len(F)) if not C[i])
    F3, C3 = insert_octahedron(F, C, w)
    cases.append(("DW8 + octahedron in a white face", F3, C3, black_face(F3, C3, lambda f: max(f) < 10)))
    w2 = [i for i in range(len(F3)) if not C3[i] and max(F3[i]) < 10][2]
    F4, C4 = insert_octahedron(F3, C3, w2)
    cases.append(("DW8 + two white octahedra", F4, C4, black_face(F4, C4, lambda f: max(f) < 10)))
    F, C = barycentric(OCTA)
    cases.append(("barycentric octahedron", F, C, 0))
    F, C = subdivide4(*double_wheel(4))
    for t0 in [i for i in range(len(F)) if C[i]][:3]:
        cases.append((f"octahedron, each face split in four, t0={t0}", F, C, t0))
    F, C = subdivide4(*double_wheel(6))
    cases.append(("DW6, each face split in four", F, C, 0))
    for seed, steps in ((1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 8), (8, 9), (9, 9), (10, 10)):
        F, C = random_eulerian(seed, steps)
        for t0 in [i for i in range(len(F)) if C[i]][:2]:
            cases.append((f"random vertex splits seed={seed} steps={steps} t0={t0}", F, C, t0))
    for name, F, C, t0 in cases:
        rep = analyse(name, F, C, t0)
        print("== " + rep.pop("name"))
        for k, v in rep.items():
            print(f"   {k:38s} {v}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
