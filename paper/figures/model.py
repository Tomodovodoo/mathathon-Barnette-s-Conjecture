"""Combinatorics of a rooted Eulerian triangulation, as used by the figures.

Everything a figure draws is computed here and asserted in check.py.
Notation follows research/BRIEF.md and the OpenAI paper (Sections 2 to 6).

A triangulation is a list of faces, each a triple of vertices. All faces are
listed with the same orientation, so every directed edge (u, v) lies in exactly
one face. The layout draws every bounded face counterclockwise in this order,
so "the face of (u, v)" is the face on the left of the directed edge u -> v.
"""
import itertools as it
import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).parent


def und(u, v):
    return (u, v) if u < v else (v, u)


def oriented_faces(graph):
    """Faces of a planar graph, consistently oriented."""
    ok, emb = nx.check_planarity(graph)
    assert ok
    seen, faces = set(), []
    for u, v in emb.edges():
        if (u, v) not in seen:
            faces.append(tuple(emb.traverse_face(u, v, seen)))
    return faces


def dual_of_cubic(primal):
    """Faces (as vertex triples) of the dual triangulation of a cubic plane graph.

    Dual vertices are numbered by the faces of the primal graph in the order
    networkx reports them, so the numbering is only fixed up to that order.
    Use `isomorphic_to_dual` to compare with a stored triangulation.
    """
    pf = oriented_faces(primal)
    T = nx.Graph()
    for i, j in it.combinations(range(len(pf)), 2):
        if len(set(pf[i]) & set(pf[j])) == 2:
            T.add_edge(i, j)
    return oriented_faces(T)


class Model:
    def __init__(self, faces, t0, e0=None):
        self.F = [tuple(f) for f in faces]
        self.V = sorted({v for f in self.F for v in f})
        self.left = {}
        for i, f in enumerate(self.F):
            for a, b in zip(f, f[1:] + f[:1]):
                assert (a, b) not in self.left, 'faces are not consistently oriented'
                self.left[a, b] = i
        self.E = sorted({und(a, b) for a, b in self.left})
        assert all((b, a) in self.left for a, b in self.left)
        self.T = nx.Graph(self.E)
        # Primal cubic graph G: one vertex per face, one edge per edge of T.
        self.G = nx.Graph()
        self.G.add_nodes_from(range(len(self.F)))
        self.cross = {}                      # edge of G  ->  edge of T it crosses
        self.dual = {}                       # edge of T  ->  edge of G
        for a, b in self.E:
            g = und(self.left[a, b], self.left[b, a])
            self.G.add_edge(*g)
            self.cross[g] = (a, b)
            self.dual[a, b] = g
        col = nx.bipartite.color(self.G)
        self.t0 = t0
        self.black = sorted(i for i in self.G if col[i] == col[t0])
        self.white = sorted(i for i in self.G if col[i] != col[t0])
        self.roots = list(self.F[t0])
        self.A = [t for t in self.black if t != t0]
        self.X = [v for v in self.V if v not in self.roots]
        assert len(self.A) == len(self.X)
        self.e0 = und(*e0) if e0 else und(*self.roots[:2])
        assert set(self.e0) < set(self.roots)

    # -- local structure ----------------------------------------------------
    def black_face(self, u, v):
        """The unique black face containing the edge uv."""
        a, b = self.left[u, v], self.left[v, u]
        return a if a in self.black else b

    def white_face(self, u, v):
        a, b = self.left[u, v], self.left[v, u]
        return a if a in self.white else b

    def delta(self, u, v):
        """+1 if the black face of uv is on the left of u -> v (paper, Section 4).

        The outer face t0 is drawn as the unbounded region, and it also lies on
        the left of its own boundary in the stored order, so no special case.
        """
        return 1 if self.left[u, v] in self.black else -1

    def third(self, t, a, b):
        return next(v for v in self.F[t] if v not in (a, b))

    # -- states and pairs ---------------------------------------------------
    def states(self):
        out, X = [], set(self.X)

        def rec(s, used):
            if len(s) == len(self.A):
                out.append(tuple(s))
                return
            for v in self.F[self.A[len(s)]]:
                if v in X and v not in used:
                    rec(s + [v], used | {v})
        rec([], set())
        return out

    def is_state(self, s):
        return (len(s) == len(self.A) and sorted(s) == sorted(self.X)
                and all(v in self.F[t] for t, v in zip(self.A, s)))

    def is_pair(self, r, s):
        return self.is_state(r) and self.is_state(s) and all(a != b for a, b in zip(r, s))

    def pairs(self, states=None):
        states = states or self.states()
        return [(r, s) for r in states for s in states if all(a != b for a, b in zip(r, s))]

    def Q(self, s):
        """Edges opposite s(t), one per t in A, in the order of A."""
        return [tuple(v for v in self.F[t] if v != x) for t, x in zip(self.A, s)]

    def Q_graph(self, s):
        g = nx.Graph()
        g.add_nodes_from(self.V)
        g.add_edges_from(self.Q(s))
        return g

    def Q_is_forest(self, s):
        return nx.is_forest(self.Q_graph(s))

    def Q_directed(self, r, s):
        """Q_s oriented r(t) -> u(t)."""
        return [(a, self.third(t, a, b)) for t, a, b in zip(self.A, r, s)]

    def D(self, r, s):
        return list(zip(r, s))

    def J(self, r, s):
        total = sum(self.delta(a, b) for a, b in zip(r, s))
        assert total % 3 == 0
        return total // 3

    @staticmethod
    def directed_cycles(arcs):
        return [c for c in nx.simple_cycles(nx.DiGraph(arcs))]

    def reverse_Q_cycle(self, r, s, cycle):
        """The involution of Lemma 5.2: on the triangles supplying the directed
        cycle of Q_s, replace r(t) by u(t)."""
        on = {(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1])}
        return tuple(self.third(t, a, b) if (a, self.third(t, a, b)) in on else a
                     for t, a, b in zip(self.A, r, s))

    # -- disks ----------------------------------------------------------------
    def disk(self, cycle):
        """Data of the disk bounded by a directed cycle that avoids the roots.

        Returns faces inside, interior vertices, the counts B, W, I, h, l, the
        delta-sum, and whether the cycle runs counterclockwise (disk on its left).
        """
        arcs = list(zip(cycle, cycle[1:] + cycle[:1]))
        barrier = {und(a, b) for a, b in arcs}
        g = self.G.copy()
        g.remove_edges_from(e for e, te in self.cross.items() if und(*te) in barrier)
        outside = nx.node_connected_component(g, self.t0)
        inside = sorted(set(g) - outside)
        assert inside, 'cycle does not bound a disk away from t0'
        vin = {v for f in inside for v in self.F[f]} - set(cycle)
        B = [f for f in inside if f in self.black]
        W = [f for f in inside if f in self.white]
        inner_black = [(a, b) for a, b in arcs if self.black_face(a, b) in inside]
        ccw = self.left[arcs[0]] in inside
        assert all((self.left[a] in inside) == ccw for a in arcs)
        return dict(cycle=list(cycle), faces=inside, interior=sorted(vin),
                    black=B, white=W, B=len(B), W=len(W), I=len(vin), h=len(cycle),
                    l=len(inner_black), inner_black_edges=inner_black,
                    delta_sum=sum(self.delta(a, b) for a, b in arcs), ccw=ccw)

    # -- recovery (Section 6) ---------------------------------------------------
    def spoke_graph(self):
        H = nx.Graph()
        for t in self.black:
            for v in self.F[t]:
                H.add_edge(('t', t), ('v', v))
        return H

    def recover(self, s):
        """From a state with Q_s a forest: white tree, selected edges P, the two
        induced trees and the Hamiltonian cycle of G. Asserts every claim."""
        H = self.spoke_graph()
        H.remove_edges_from((('t', t), ('v', v)) for t, v in zip(self.A, s))
        assert nx.is_tree(H), 'H - s is not a tree'
        WT = nx.Graph()
        WT.add_nodes_from(self.white)
        link = {}
        for t, x in zip(self.A, s):
            sides = [(x, v) for v in self.F[t] if v != x]
            ws = [self.white_face(*e) for e in sides]
            assert ws[0] != ws[1]
            WT.add_edge(*ws)
            link[t] = dict(corner=x, sides=sides, whites=ws)
        assert nx.is_tree(WT)
        y0 = self.white_face(*self.e0)
        depth = nx.single_source_shortest_path_length(WT, y0)
        P = [self.e0]
        chosen = {}
        for t, x in zip(self.A, s):
            ws, sides = link[t]['whites'], link[t]['sides']
            k = 0 if depth[ws[0]] > depth[ws[1]] else 1      # the endpoint farther from y0
            chosen[t] = dict(edge=und(*sides[k]), child=ws[k], parent=ws[1 - k], corner=x)
            P.append(und(*sides[k]))
        assert len(set(P)) == len(P)
        for f in self.F:
            sides = {und(a, b) for a, b in zip(f, f[1:] + f[:1])}
            assert len(sides & set(P)) == 1, 'not exactly one selected side per face'
        PF = nx.Graph()
        PF.add_nodes_from(self.V)
        PF.add_edges_from(P)
        assert nx.is_forest(PF) and nx.number_connected_components(PF) == 2
        parts = [sorted(c) for c in nx.connected_components(PF)]
        parts.sort(key=lambda c: self.e0[0] not in c)          # class of e0 first
        for c in parts:
            assert nx.is_tree(self.T.subgraph(c)), 'class does not induce a tree'
        assert set(self.e0) <= set(parts[0]) and (set(self.roots) - set(self.e0)) <= set(parts[1])
        HC = nx.Graph()
        HC.add_nodes_from(self.G)
        HC.add_edges_from(g for g, te in self.cross.items() if und(*te) not in P)
        assert nx.is_connected(HC) and all(d == 2 for _, d in HC.degree())
        order = [self.t0]
        prev = None
        while True:
            nxt = [w for w in HC[order[-1]] if w != prev]
            prev = order[-1]
            if nxt[0] == self.t0 and len(order) > 1:
                break
            order.append(nxt[0])
            if len(order) > len(self.F):
                raise AssertionError
        assert len(order) == len(self.F)
        return dict(white_tree=sorted(und(*e) for e in WT.edges()), y0=y0, depth=depth,
                    chosen=chosen, P=sorted(P), parts=parts, hamiltonian=sorted(HC.edges()),
                    cycle_order=order)

    # -- Proposition 3.1 ---------------------------------------------------------
    def incidence_graph(self):
        """The bipartite incidence graph B on A and X."""
        B = nx.Graph()
        B.add_nodes_from(('t', t) for t in self.A)
        B.add_nodes_from(('v', v) for v in self.X)
        X = set(self.X)
        for t in self.A:
            for v in self.F[t]:
                if v in X:
                    B.add_edge(('t', t), ('v', v))
        return B

    def cut_inequality(self, S):
        """Both sides of (3.1) for S a subset of X."""
        S = set(S)
        return sum(min(2, len(set(self.F[t]) & S)) for t in self.A), 2 * len(S)

    def two_factors(self, components=None):
        """2-factors of G (complements of perfect matchings); optionally only
        those with a given number of components."""
        out = []

        def rec(left, es):
            if not left:
                h = self.G.copy()
                h.remove_edges_from(es)
                if components is None or nx.number_connected_components(h) == components:
                    out.append(sorted(und(*e) for e in h.edges()))
                return
            u = min(left)
            for v in self.G[u]:
                if v in left:
                    rec(left - {u, v}, es + [(u, v)])
        rec(set(self.G), [])
        return out


def load(name):
    d = json.loads((HERE / name).read_text())
    return Model(d['faces'], d['t0'], d.get('e0'))
