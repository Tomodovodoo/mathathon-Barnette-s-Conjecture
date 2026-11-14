"""Point-rainbow spanning trees, the exchange move, the black excess. Own implementation.

Objects (see RAINBOW.md for the definitions):
  white-face graph  H*: vertices = white faces, one edge per spoke (t, v) of H, joining the two
                    white faces across the sides of the black face t at the corner v.
  colour of an edge its point v (point colouring) or its black face t (face colouring).
  rainbow tree      a map sigma: X -> black faces with sigma(x) at x, such that the duals of the
                    spokes (sigma(x), x) form a spanning tree of H*.
  load              c(t) = number of x with sigma(x) = t.   excess = sum over t in A of |c(t) - 1|.
  move at x         replace sigma(x) by the unique other black face t' at x that keeps a tree.
"""
import random
from collections import deque

import etri


class RB:
    def __init__(self, I):
        self.I = I
        self.X = I.X
        self.n = I.n
        self.widx = {f: i for i, f in enumerate(I.Wh)}
        self.nw = len(I.Wh)
        # options[x] = list of (t, w1, w2)
        self.opt = {}
        for x in self.X:
            self.opt[x] = [(t, self.widx[I.spoke_dual[(t, x)][0]], self.widx[I.spoke_dual[(t, x)][1]]) for t in I.bf[x]]
        self.dual = {(t, x): (a, b) for x in self.X for (t, a, b) in self.opt[x]}
        self.Aset = set(I.A)

    # ---------------------------------------------------------------- existence by matroid intersection
    def _intersect(self, classes, rng=None):
        """classes: list of lists of (u, v, tag). Largest forest with at most one edge per class."""
        edges = []
        for c, L in enumerate(classes):
            for (u, v, tag) in L:
                edges.append((u, v, c, tag))
        order = list(range(len(edges)))
        if rng:
            rng.shuffle(order)
        cur = set()
        nw = self.nw
        while True:
            adj = [[] for _ in range(nw)]
            for e in cur:
                u, v, c, _ = edges[e]
                adj[u].append((v, e))
                adj[v].append((u, e))
            comp = [-1] * nw
            for r in range(nw):
                if comp[r] < 0:
                    comp[r] = r
                    st = [r]
                    while st:
                        a = st.pop()
                        for (b, _) in adj[a]:
                            if comp[b] < 0:
                                comp[b] = r
                                st.append(b)
            usedcol = {edges[e][2]: e for e in cur}
            out = [f for f in order if f not in cur]
            src = [f for f in out if comp[edges[f][0]] != comp[edges[f][1]]]
            snk = set(f for f in out if edges[f][2] not in usedcol)
            prev = {}
            dq = deque()
            for f in src:
                prev[('f', f)] = None
                dq.append(('f', f))
            end = None
            while dq:
                kind, a = dq.popleft()
                if kind == 'f':
                    if a in snk:
                        end = (kind, a)
                        break
                    e = usedcol[edges[a][2]]
                    if ('e', e) not in prev:
                        prev[('e', e)] = (kind, a)
                        dq.append(('e', e))
                else:
                    # side of the forest cut by removing edge a
                    u0, v0 = edges[a][0], edges[a][1]
                    side = {u0}
                    st = [u0]
                    while st:
                        p = st.pop()
                        for (q, e) in adj[p]:
                            if e != a and q not in side:
                                side.add(q)
                                st.append(q)
                    cu = comp[u0]
                    for f in out:
                        if ('f', f) in prev:
                            continue
                        fu, fv = edges[f][0], edges[f][1]
                        if comp[fu] == cu and comp[fv] == cu and ((fu in side) != (fv in side)):
                            prev[('f', f)] = (kind, a)
                            dq.append(('f', f))
            if end is None:
                return [edges[e] for e in cur]
            node = end
            while node is not None:
                kind, a = node
                if kind == 'f':
                    cur.add(a)
                else:
                    cur.discard(a)
                node = prev[node]

    def point_rainbow_tree(self, rng=None):
        """sigma (dict x -> t) or None."""
        classes = [[(a, b, (t, x)) for (t, a, b) in self.opt[x]] for x in self.X]
        res = self._intersect(classes, rng)
        if len(res) < self.n:
            return None
        return {tag[1]: tag[0] for (_, _, _, tag) in res}

    def face_rainbow_tree(self):
        """One spoke at every bounded black face (no condition on points), duals a spanning tree."""
        I = self.I
        classes = []
        for t in I.A:
            L = []
            for v in I.faces[t]:
                a, b = I.spoke_dual[(t, v)]
                L.append((self.widx[a], self.widx[b], (t, v)))
            classes.append(L)
        res = self._intersect(classes)
        return len(res) == self.n

    # ---------------------------------------------------------------- basic predicates
    def is_tree(self, sigma):
        par = list(range(self.nw))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a

        for x, t in sigma.items():
            a, b = self.dual[(t, x)]
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            par[ra] = rb
        return len(sigma) == self.n

    def load(self, sigma):
        c = {t: 0 for t in self.I.A}
        for x, t in sigma.items():
            c[t] += 1
        return c

    def excess(self, sigma):
        return sum(abs(v - 1) for v in self.load(sigma).values())

    def move_target(self, sigma, x):
        """The unique black face t' != sigma(x) at x such that sigma[x -> t'] is again a tree."""
        adj = [[] for _ in range(self.nw)]
        for y, t in sigma.items():
            if y == x:
                continue
            a, b = self.dual[(t, y)]
            adj[a].append(b)
            adj[b].append(a)
        a0, _ = self.dual[(sigma[x], x)]
        side = [False] * self.nw
        side[a0] = True
        st = [a0]
        while st:
            p = st.pop()
            for q in adj[p]:
                if not side[q]:
                    side[q] = True
                    st.append(q)
        res = [t for (t, a, b) in self.opt[x] if t != sigma[x] and side[a] != side[b]]
        return res

    def all_trees(self, limit=None):
        """All point-rainbow trees as tuples (t for x in X)."""
        X = sorted(self.X, key=lambda x: len(self.opt[x]))
        out = []
        cur = {}
        nw = self.nw

        def rec(j, par):
            if limit is not None and len(out) >= limit:
                return
            if j == len(X):
                out.append(tuple(cur[x] for x in self.X))
                return
            x = X[j]
            for (t, a, b) in self.opt[x]:
                ra, rb = a, b
                while par[ra] != ra:
                    ra = par[ra]
                while par[rb] != rb:
                    rb = par[rb]
                if ra == rb:
                    continue
                p2 = par[:]
                p2[ra] = rb
                cur[x] = t
                rec(j + 1, p2)
            cur.pop(x, None)

        rec(0, list(range(nw)))
        return out


def random_walk(rb, sigma, steps, rng):
    sigma = dict(sigma)
    for _ in range(steps):
        x = rng.choice(rb.X)
        (t,) = rb.move_target(sigma, x)
        sigma[x] = t
    return sigma


def climb(rb, sigma, rng, tries=400):
    """Random moves that never decrease the excess: an adversarial start."""
    sigma = dict(sigma)
    load = rb.load(sigma)
    for _ in range(tries):
        x = rng.choice(rb.X)
        t = sigma[x]
        (t2,) = rb.move_target(sigma, x)
        d = (abs(load[t] - 2) - abs(load[t] - 1)) + (abs(load[t2]) - abs(load[t2] - 1))
        if d >= 0:
            sigma[x] = t2
            load[t] -= 1
            load[t2] += 1
    return sigma


def descend(rb, sigma, cap=20000):
    """Search the plateau of sigma (moves of excess change 0) breadth first for a decreasing move.
    Repeats until the excess is 0. Returns a dict with the trace statistics; 'stuck' is 'closed' if a
    whole plateau component was explored without finding a decreasing move (a trap), or 'cap'."""
    X = rb.X
    sigma = dict(sigma)
    steps = 0
    max_plateau = 0
    max_depth = 0
    exc0 = rb.excess(sigma)
    while True:
        load = rb.load(sigma)
        exc = sum(abs(v - 1) for v in load.values())
        if exc == 0:
            return {'ok': True, 'steps': steps, 'max_plateau': max_plateau, 'max_depth': max_depth, 'start_excess': exc0, 'sigma': sigma}
        key0 = tuple(sigma[x] for x in X)
        seen = {key0: 0}
        dq = deque([key0])
        found = None
        while dq and found is None:
            key = dq.popleft()
            s = dict(zip(X, key))
            ld = rb.load(s)
            for x in X:
                t = s[x]
                if ld[t] != 2:
                    # moves out of a load-1 face are useful only into an empty face
                    pass
                (t2,) = rb.move_target(s, x)
                d = (abs(ld[t] - 2) - abs(ld[t] - 1)) + (abs(ld[t2]) - abs(ld[t2] - 1))
                if d < 0:
                    s[x] = t2
                    found = (s, seen[key] + 1)
                    break
                if d == 0:
                    k2 = key[:X.index(x)] + (t2,) + key[X.index(x) + 1:]
                    if k2 not in seen:
                        seen[k2] = seen[key] + 1
                        dq.append(k2)
            if len(seen) > cap:
                break
        max_plateau = max(max_plateau, len(seen))
        if found is None:
            return {'ok': False, 'stuck': 'closed' if not dq and len(seen) <= cap else 'cap', 'excess': exc, 'plateau': len(seen),
                    'steps': steps, 'start_excess': exc0, 'sigma': sigma}
        sigma, depth = found
        steps += depth
        max_depth = max(max_depth, depth)


def descend_walk(rb, sigma, rng, max_steps=4000):
    """Descent for large instances: take a decreasing move when one exists, otherwise a uniformly
    random plateau move. Never increases the excess. Returns the same record as descend()."""
    X = rb.X
    sigma = dict(sigma)
    load = rb.load(sigma)
    exc0 = exc = sum(abs(v - 1) for v in load.values())
    steps = 0
    since = 0
    max_wait = 0
    while exc > 0:
        if since > max_steps:
            return {'ok': False, 'stuck': 'cap', 'excess': exc, 'plateau': since, 'steps': steps, 'start_excess': exc0, 'sigma': sigma}
        flat = []
        done = False
        # only points in a load-2 face, or with a load-0 face among their black faces, can make a non-increasing move
        order = X[:]
        rng.shuffle(order)
        for x in order:
            t = sigma[x]
            if load[t] != 2 and not any(load.get(tt, 1) == 0 for (tt, _, _) in rb.opt[x]):
                continue
            (t2,) = rb.move_target(sigma, x)
            d = (abs(load[t] - 2) - abs(load[t] - 1)) + (abs(load[t2]) - abs(load[t2] - 1))
            if d < 0:
                sigma[x] = t2
                load[t] -= 1
                load[t2] += 1
                exc += d
                steps += 1
                max_wait = max(max_wait, since)
                since = 0
                done = True
                break
            if d == 0:
                flat.append((x, t, t2))
        if done:
            continue
        if not flat:
            return {'ok': False, 'stuck': 'closed', 'excess': exc, 'plateau': 1, 'steps': steps, 'start_excess': exc0, 'sigma': sigma}
        x, t, t2 = rng.choice(flat)
        sigma[x] = t2
        load[t] -= 1
        load[t2] += 1
        steps += 1
        since += 1
    return {'ok': True, 'steps': steps, 'max_plateau': max_wait, 'max_depth': max_wait, 'start_excess': exc0, 'sigma': sigma}
