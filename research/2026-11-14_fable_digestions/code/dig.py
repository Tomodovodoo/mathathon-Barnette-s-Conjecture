"""Small independent model of the proof objects, used to compute the examples of digestions/steps/.

Input: a list of oriented faces of a sphere triangulation (every face listed in the same
rotational sense) and the index of the outer black face t0. With t0 at infinity the bounded
faces are counterclockwise, as in paper/figures/running.json.

Conventions (those of the OpenAI paper):
  delta(v, w) = +1 if the black face of the edge vw is on the left of v -> w.
  A directed cycle avoiding the roots is counterclockwise if its inside (the side away from t0)
  is on its left.
Nothing here imports workings/barnette_lab; crosscheck.py compares the two.
"""
from collections import deque
from itertools import product


class Tri:
    def __init__(self, faces, t0):
        self.faces = [tuple(f) for f in faces]
        self.t0 = t0
        self.left = {}                      # directed edge -> face on its left
        for i, f in enumerate(self.faces):
            for a, b in zip(f, f[1:] + f[:1]):
                assert (a, b) not in self.left
                self.left[a, b] = i
        self.V = sorted({v for f in self.faces for v in f})
        self.E = sorted({tuple(sorted(e)) for e in self.left})
        assert len(self.V) - len(self.E) + len(self.faces) == 2
        # proper 2-colouring of the faces, t0 black
        col = {t0: 1}
        dq = deque([t0])
        while dq:
            f = dq.popleft()
            for a, b in zip(self.faces[f], self.faces[f][1:] + self.faces[f][:1]):
                g = self.left[b, a]
                if g not in col:
                    col[g] = 1 - col[f]
                    dq.append(g)
                assert col[g] != col[f], 'faces are not 2-colourable'
        self.black = sorted(f for f in col if col[f])
        self.white = sorted(f for f in col if not col[f])
        self.R = sorted(self.faces[t0])
        self.X = [v for v in self.V if v not in self.R]
        self.A = [t for t in self.black if t != t0]
        self.n = len(self.A)
        assert len(self.X) == self.n and len(self.white) == self.n + 1

    # ---- local data -----------------------------------------------------
    def delta(self, v, w):
        return 1 if self.left[v, w] in self.black else -1

    def blackface(self, v, w):
        f = self.left[v, w]
        return f if f in self.black else self.left[w, v]

    def whiteface(self, v, w):
        f = self.left[v, w]
        return f if f in self.white else self.left[w, v]

    # ---- states and pairs -------------------------------------------------
    def states(self):
        out = []

        def rec(i, used, st):
            if i == self.n:
                out.append(tuple(st))
                return
            for v in self.faces[self.A[i]]:
                if v in self.X and v not in used:
                    rec(i + 1, used | {v}, st + [v])
        rec(0, frozenset(), [])
        return out

    def pairs(self, states=None):
        ss = self.states() if states is None else states
        return [(r, s) for r in ss for s in ss if all(a != b for a, b in zip(r, s))]

    def third(self, r, s):
        return tuple(next(v for v in self.faces[t] if v not in (a, b)) for t, a, b in zip(self.A, r, s))

    def Q(self, s):
        """Edges opposite s(t), as {face: (a, b)}."""
        return {t: tuple(v for v in self.faces[t] if v != x) for t, x in zip(self.A, s)}

    def components(self, edges):
        parent = {v: v for v in self.V}

        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        cyc = 0
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                cyc += 1
            else:
                parent[ra] = rb
        comps = {}
        for v in self.V:
            comps.setdefault(find(v), []).append(v)
        return sorted(comps.values()), cyc

    def q_info(self, s):
        comps, cyc = self.components(self.Q(s).values())
        roots = [sum(v in self.R for v in c) for c in comps]
        return {'cycles': cyc, 'components': comps, 'roots_per_component': roots,
                'rooted_forest': cyc == 0 and all(a == 1 for a in roots)}

    def is_tree_matching(self, s):
        return self.q_info(s)['rooted_forest']

    # ---- cycles and disks ---------------------------------------------------
    def dcycles(self, r, s):
        nxt = dict(zip(r, s))
        seen, out = set(), []
        for v in self.X:
            if v in seen:
                continue
            c = [v]
            seen.add(v)
            while nxt[c[-1]] != v:
                c.append(nxt[c[-1]])
                seen.add(c[-1])
            out.append(tuple(c))
        return out

    def inside(self, cyc):
        """Faces on the side of the directed cycle away from t0, and whether it is counterclockwise."""
        cut = {frozenset(e) for e in zip(cyc, cyc[1:] + cyc[:1])}
        seen = {self.t0}
        dq = deque([self.t0])
        while dq:
            f = dq.popleft()
            for a, b in zip(self.faces[f], self.faces[f][1:] + self.faces[f][:1]):
                if frozenset((a, b)) in cut:
                    continue
                g = self.left[b, a]
                if g not in seen:
                    seen.add(g)
                    dq.append(g)
        ins = [f for f in range(len(self.faces)) if f not in seen]
        ccw = self.left[cyc[0], cyc[1]] in ins
        return ins, ccw

    def disk(self, cyc):
        ins, ccw = self.inside(cyc)
        on = set(cyc)
        inner_vertices = sorted({v for f in ins for v in self.faces[f]} - on)
        edges = list(zip(cyc, cyc[1:] + cyc[:1]))
        l = sum(self.blackface(a, b) in ins for a, b in edges)
        return {'cycle': list(cyc), 'ccw': ccw, 'h': len(cyc), 'l': l,
                'B': sum(f in self.black for f in ins), 'W': sum(f in self.white for f in ins),
                'I': len(inner_vertices), 'inner_vertices': inner_vertices,
                'white_inside': sorted(f for f in ins if f in self.white),
                'delta_sum': sum(self.delta(a, b) for a, b in edges)}

    def J(self, r, s):
        j = sum(self.delta(a, b) for a, b in zip(r, s))
        assert j % 3 == 0
        return j // 3

    def eps(self, r, s):
        """Real sign: product of delta(r(t), s(t)).  Equals (-1)^((n + J)/2), the sign of the trees paper."""
        p = 1
        for a, b in zip(r, s):
            p *= self.delta(a, b)
        return p

    def reverse_d(self, r, s, cyc):
        on = set(cyc)
        r2 = tuple(b if a in on else a for a, b in zip(r, s))
        s2 = tuple(a if a in on else b for a, b in zip(r, s))
        return r2, s2

    def partners(self, s, states=None):
        ss = self.states() if states is None else states
        return [r for r in ss if all(a != b for a, b in zip(r, s))]

    # ---- heights ------------------------------------------------------------
    def white_graph(self):
        """Edges between white faces, one per spoke (t, v) with t in A:
        (white on the left of centre -> v, white on the right, t, v)."""
        out = []
        for t in self.A:
            f = self.faces[t]
            for i, v in enumerate(f):
                a, b = f[(i + 1) % 3], f[(i + 2) % 3]      # t = (v, a, b) counterclockwise
                out.append((self.left[a, v], self.left[v, b], t, v))
        return out

    def kappa(self):
        """kappa[w][(t, v)]: signed crossings of the spoke centre(t) -> v with a fixed path from the
        inner white face w to the outside (right-to-left counted +1)."""
        outer = {self.left[b, a] for a, b in zip(self.faces[self.t0], self.faces[self.t0][1:] + self.faces[self.t0][:1])}
        adj = {}
        for yl, yr, t, v in self.white_graph():
            adj.setdefault(yl, []).append((yr, t, v, +1))   # path goes left -> right of the spoke
            adj.setdefault(yr, []).append((yl, t, v, -1))
        kap = {}
        for w in self.white:
            if w in outer:
                continue
            prev = {w: None}
            dq = deque([w])
            end = None
            while dq:
                y = dq.popleft()
                if y in outer:
                    end = y
                    break
                for z, t, v, sg in adj[y]:
                    if z not in prev:
                        prev[z] = (y, t, v, sg)
                        dq.append(z)
            k = {}
            y = end
            while prev[y] is not None:
                y0, t, v, sg = prev[y]
                k[t, v] = k.get((t, v), 0) + sg
                y = y0
            kap[w] = k
        return kap

    def heights(self, s, kap=None):
        kap = self.kappa() if kap is None else kap
        return {w: sum(k.get((t, v), 0) for t, v in zip(self.A, s)) for w, k in kap.items()}

    def spoke_weights(self, kap=None):
        """a(t, v) = sum over inner white faces of kappa: unit circulation around every bounded spoke face."""
        kap = self.kappa() if kap is None else kap
        a = {}
        for k in kap.values():
            for key, val in k.items():
                a[key] = a.get(key, 0) + val
        return a

    # ---- recovery (OpenAI Section 6) -----------------------------------------
    def recover(self, s, e0):
        assert self.is_tree_matching(s)
        e0 = tuple(e0)
        y0 = self.whiteface(*e0)
        adj = {y: [] for y in self.white}
        for t, v in zip(self.A, s):
            f = self.faces[t]
            i = f.index(v)
            a, b = f[(i + 1) % 3], f[(i + 2) % 3]
            yl, yr = self.left[a, v], self.left[v, b]
            adj[yl].append((yr, t, (v, b)))      # the side of t bordering yr is v b
            adj[yr].append((yl, t, (v, a)))      # the side of t bordering yl is v a
        parent = {y0: None}
        order = [y0]
        P = [tuple(sorted(e0))]
        tree = []
        for y in order:
            for z, t, side in adj[y]:
                if z not in parent:
                    parent[z] = y
                    order.append(z)
                    tree.append((y, z, t))
                    P.append(tuple(sorted(side)))
        assert len(order) == len(self.white), 'white graph is not connected'
        assert len(tree) == self.n
        comps, cyc = self.components(P)
        assert cyc == 0 and len(comps) == 2
        Pset = set(P)
        # dual cycle: faces are vertices of G, adjacent across unselected edges
        gadj = {f: [] for f in range(len(self.faces))}
        for a, b in self.E:
            if (a, b) not in Pset:
                gadj[self.left[a, b]].append(self.left[b, a])
                gadj[self.left[b, a]].append(self.left[a, b])
        assert all(len(v) == 2 for v in gadj.values())
        cycle, prev, cur = [0], None, 0
        while True:
            nx = next(g for g in gadj[cur] if g != prev)
            if nx == cycle[0]:
                break
            cycle.append(nx)
            prev, cur = cur, nx
        assert len(cycle) == len(self.faces) and len(set(cycle)) == len(cycle)
        return {'y0': y0, 'white_tree': tree, 'P': sorted(P), 'classes': comps, 'cycle': cycle}

    # ---- two-factors and Hamiltonian cycles of the cubic graph G = T* --------------------
    def G_edges(self):
        return sorted({tuple(sorted((self.left[a, b], self.left[b, a]))) for a, b in self.E})

    def perfect_matchings_G(self):
        ge = self.G_edges()
        nb = {}
        for a, b in ge:
            nb.setdefault(a, []).append(b)
            nb.setdefault(b, []).append(a)
        out = []

        def rec(free, m):
            if not free:
                out.append(sorted(m))
                return
            v = min(free)
            for w in nb[v]:
                if w in free:
                    rec(free - {v, w}, m + [(v, w)])
        rec(frozenset(nb), [])
        return out, ge

    def two_factors(self):
        """Each 2-factor of the cubic graph is the complement of a perfect matching.
        Returns (matching, number of cycles of the complement)."""
        pms, ge = self.perfect_matchings_G()
        res = []
        for m in pms:
            ms = set(m)
            nb = {}
            for a, b in ge:
                if (a, b) not in ms:
                    nb.setdefault(a, []).append(b)
                    nb.setdefault(b, []).append(a)
            seen, c = set(), 0
            for v in nb:
                if v in seen:
                    continue
                c += 1
                st = [v]
                while st:
                    x = st.pop()
                    if x in seen:
                        continue
                    seen.add(x)
                    st.extend(nb[x])
            res.append((m, c))
        return res


def summary(T, states=None):
    ss = T.states() if states is None else states
    ps = T.pairs(ss)
    tms = [s for s in ss if T.is_tree_matching(s)]
    covers = {}
    for r, s in ps:
        key = frozenset(frozenset(e) for e in zip(r, s))
        covers.setdefault(key, []).append((r, s))
    return {'n': T.n, 'states': len(ss), 'pairs': len(ps), 'tree_matchings': len(tms),
            'partnered_states': len({s for _, s in ps}),
            'covers_by_cycle_count': sorted(len(T.dcycles(*v[0])) for v in covers.values())}, ss, ps, tms, covers
