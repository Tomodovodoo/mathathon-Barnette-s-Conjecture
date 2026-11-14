"""Shared helpers. Uses the reference lab (workings/barnette_lab) read-only.

A Tri is an unrooted Eulerian sphere triangulation with its two face classes
and its vertex 3-colouring. Roots are chosen by the experiments.
"""
import os
import sys
import subprocess
from collections import defaultdict

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
LAB = os.path.join(ROOT, 'workings', 'barnette_lab')
sys.path.insert(0, LAB)
from barnette_lab.core import Instance, faces_of  # noqa: E402

PLANTRI = os.path.join(LAB, 'vendor', 'plantri.exe')


def plantri(nv):
    """All Eulerian sphere triangulations on nv vertices (plantri -ba), one per class."""
    run = subprocess.run([PLANTRI, '-ba', str(nv)], capture_output=True, check=True, text=True, timeout=300)
    out = []
    for line in run.stdout.splitlines():
        n, data = line.split()
        g = nx.Graph()
        for v, ns in enumerate(data.split(',')):
            g.add_edges_from((v, ord(c) - ord('a')) for c in ns)
        assert len(g) == int(n)
        out.append(g)
    return out


def corpus(nmin, nmax):
    for nv in range(nmin, nmax + 1):
        if nv == 7:
            continue
        for i, g in enumerate(plantri(nv)):
            yield 'plantri_%d_%d' % (nv, i), g


class Tri:
    def __init__(self, g):
        self.g = g
        ok, emb = nx.check_planarity(g)
        assert ok
        self.emb = emb
        self.faces, self.sides = faces_of(emb)
        assert all(len(f) == 3 for f in self.faces)
        self.V = sorted(g)
        self.nf = len(self.faces)
        self.k = self.nf // 2
        # face colours: 0 = black, 1 = white; face 0 is black
        colour = {0: 0}
        stack = [0]
        while stack:
            f = stack.pop()
            a = self.faces[f]
            for u, v in zip(a, a[1:] + a[:1]):
                h = self.sides[v, u]
                if h not in colour:
                    colour[h] = 1 - colour[f]
                    stack.append(h)
                else:
                    assert colour[h] != colour[f]
        self.fcol = colour
        self.black = [f for f in range(self.nf) if colour[f] == 0]
        self.white = [f for f in range(self.nf) if colour[f] == 1]
        # vertex 3-colouring: black faces read 0,1,2 in their stored cyclic order
        col = {}
        a = self.faces[0]
        for i, v in enumerate(a):
            col[v] = i
        stack = [0]
        seen = {0}
        while stack:
            f = stack.pop()
            a = self.faces[f]
            for u, v in zip(a, a[1:] + a[:1]):
                h = self.sides[v, u]
                if h in seen:
                    continue
                seen.add(h)
                w = next(x for x in self.faces[h] if x not in (u, v))
                c = 3 - col[u] - col[v]
                assert col.setdefault(w, c) == c
                stack.append(h)
        self.col = col
        for f in range(self.nf):
            assert sorted(col[v] for v in self.faces[f]) == [0, 1, 2]
        # white face across the edge of black face t opposite its corner v
        self.edges = [tuple(sorted(e)) for e in g.edges()]
        self.eface = {}
        for (u, v), f in self.sides.items():
            self.eface[frozenset((u, v)), colour[f]] = f

    def opposite_edge(self, t, v):
        a, b = [x for x in self.faces[t] if x != v]
        return frozenset((a, b))

    def across(self, t, v):
        """Face on the other side of the edge of t opposite v."""
        e = self.opposite_edge(t, v)
        return self.eface[e, 1 - self.fcol[t]]

    def third(self, f, e):
        return next(x for x in self.faces[f] if x not in e)

    def separating_triangles(self):
        fs = {frozenset(f) for f in self.faces}
        out = []
        vs = self.V
        for i, a in enumerate(vs):
            for b in vs[i + 1:]:
                if not self.g.has_edge(a, b):
                    continue
                for c in vs:
                    if c > b and self.g.has_edge(a, c) and self.g.has_edge(b, c):
                        if frozenset((a, b, c)) not in fs:
                            out.append((a, b, c))
        return out


class UF:
    def __init__(self, items):
        self.p = {x: x for x in items}

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        return True


def hamiltonian_partitions(tri):
    """All labellings V -> {0,1} with label(V[0]) = 0 and both classes inducing trees."""
    out = []
    for lab, c0, c1, cyc in labellings_no_mono(tri, tri.V, range(tri.nf), list(tri.g.edges())):
        if c0 == 1 and c1 == 1:
            out.append(lab)
    return out


def labellings_no_mono(tri, verts, faces, edges, fixed=None):
    """Backtracking over labellings of verts with no monochromatic face among `faces`.

    Yields (labelling dict, #components of class 0, #components of class 1, total cycle rank)
    computed in the graph (verts, edges). The first vertex gets label 0 unless `fixed` is given.
    """
    verts = list(verts)
    order = []
    seen = set()
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    # BFS order so faces close early
    queue = [verts[0]]
    seen.add(verts[0])
    while queue:
        x = queue.pop(0)
        order.append(x)
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                queue.append(y)
    for v in verts:
        if v not in seen:
            order.append(v)
    pos = {v: i for i, v in enumerate(order)}
    closing = defaultdict(list)
    for f in faces:
        a = tri.faces[f]
        closing[max(a, key=lambda v: pos[v])].append(a)
    lab = {}

    def rec(i):
        if i == len(order):
            uf = UF(order)
            cyc = 0
            for u, v in edges:
                if lab[u] == lab[v] and not uf.union(u, v):
                    cyc += 1
            comps = [set(), set()]
            for v in order:
                comps[lab[v]].add(uf.find(v))
            yield dict(lab), len(comps[0]), len(comps[1]), cyc
            return
        v = order[i]
        choices = (0,) if (i == 0 and fixed is None) else (0, 1)
        if fixed is not None and v in fixed:
            choices = (fixed[v],)
        for c in choices:
            lab[v] = c
            if all(not (lab[a[0]] == lab[a[1]] == lab[a[2]]) for a in closing[v]):
                yield from rec(i + 1)
        lab.pop(v, None)

    yield from rec(0)
