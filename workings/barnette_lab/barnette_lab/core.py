"""Executable incidence-matching construction. Vertices are integers; face IDs index faces."""
from collections import Counter, deque
from itertools import combinations, product
import random
import networkx as nx
import sympy as sp


def edge(u, v):
    return tuple(sorted((u, v)))


def faces_of(embedding):
    seen, faces, sides = set(), [], {}
    for u, v in embedding.edges():
        if (u, v) not in seen:
            f = embedding.traverse_face(u, v, seen)
            i = len(faces)
            faces.append(tuple(f))
            for a, b in zip(f, f[1:] + f[:1]):
                sides[a, b] = i
    return faces, sides


def dual_graph(g):
    ok, emb = nx.check_planarity(g)
    if not ok:
        raise ValueError('Nonplanar graph')
    fs, sides = faces_of(emb)
    d = nx.Graph()
    d.add_nodes_from(range(len(fs)))
    for u, v in g.edges():
        d.add_edge(sides[u, v], sides[v, u])
    return d


class Instance:
    """Rooted, embedded Eulerian triangulation and its incidence graphs."""
    def __init__(self, triangulation, outer=0):
        self.T = triangulation.copy()
        ok, self.embedding = nx.check_planarity(self.T)
        if not ok or any(d % 2 for _, d in self.T.degree()):
            raise ValueError('Expected Eulerian plane triangulation')
        self.faces, self.sides = faces_of(self.embedding)
        if any(len(f) != 3 for f in self.faces):
            raise ValueError('Expected triangular faces')
        self.outer = outer
        self.G = nx.Graph()
        self.G.add_nodes_from(range(len(self.faces)))
        self.dual_edges = {}
        for u, v in self.T.edges():
            a, b = self.sides[u, v], self.sides[v, u]
            self.G.add_edge(a, b)
            self.dual_edges[edge(u, v)] = edge(a, b)
        colors = nx.bipartite.color(self.G)
        self.black = sorted(t for t in self.G if colors[t] == colors[outer])
        self.white = sorted(set(self.G) - set(self.black))
        self.R = set(self.faces[outer])
        self.X = sorted(set(self.T) - self.R)
        self.A = sorted(set(self.black) - {outer})
        self.n = len(self.A)
        self.H = nx.Graph()
        for t in self.black:
            self.H.add_edges_from((('t', t), ('v', v)) for v in self.faces[t])
        self.B = self.H.subgraph([('t', t) for t in self.A] + [('v', v) for v in self.X]).copy()
        self.K = sp.Matrix([[int(v in self.faces[t]) for v in self.X] for t in self.A])
        self._weights = None

    @classmethod
    def from_primal(cls, g):
        if not (nx.is_bipartite(g) and all(d == 3 for _, d in g.degree()) and nx.node_connectivity(g) == 3):
            raise ValueError('Expected simple cubic bipartite 3-connected graph')
        return cls(dual_graph(g))

    def delta(self, u, v):
        return 1 if self.sides[u, v] in self.black else -1

    def states(self):
        """Stream all perfect matchings, without materializing their search tree."""
        def rec(i, used, state):
            if i == self.n:
                yield tuple(state)
                return
            for v in sorted(set(self.faces[self.A[i]]) & set(self.X) - used):
                yield from rec(i + 1, used | {v}, state + [v])
        yield from rec(0, set(), [])

    def valid(self, s):
        return len(s) == self.n and set(s) == set(self.X) and all(v in self.faces[t] for t, v in zip(self.A, s))

    def pairs(self, states=None):
        ss = list(self.states()) if states is None else states
        return [(r, s) for r in ss for s in ss if all(a != b for a, b in zip(r, s))]

    def Q(self, s):
        q = nx.Graph()
        q.add_nodes_from(self.T)
        for t, v in zip(self.A, s):
            a, b = set(self.faces[t]) - {v}
            q.add_edge(a, b, face=t)
        return q

    def incidence_complement(self, s):
        h = self.H.copy()
        h.remove_edges_from((('t', t), ('v', v)) for t, v in zip(self.A, s))
        return h

    def is_tree(self, s):
        return nx.is_tree(self.incidence_complement(s))

    def dcycles(self, r, s):
        d = nx.DiGraph()
        d.add_edges_from((a, b, {'face': t}) for t, a, b in zip(self.A, r, s))
        cycles = []
        for vertices in nx.simple_cycles(d):
            ids = tuple(sorted(d[a][b]['face'] for a, b in zip(vertices, vertices[1:] + vertices[:1])))
            cycles.append(ids)
        return sorted(cycles)

    def qcycles(self, s):
        q = self.Q(s)
        return sorted(tuple(sorted(q[a][b]['face'] for a, b in zip(c, c[1:] + c[:1]))) for c in nx.cycle_basis(q))

    def J(self, r, s):
        j = sum(self.delta(a, b) for a, b in zip(r, s))
        assert j % 3 == 0
        return j // 3

    def sign(self, r, s):
        return (-1) ** ((self.n + self.J(r, s)) // 2)

    def reverse_d(self, pair, cycle):
        r, s = map(list, pair)
        for t in cycle:
            i = self.A.index(t)
            r[i], s[i] = s[i], r[i]
        return tuple(r), tuple(s)

    def reverse_q(self, pair, cycle):
        r, s = pair
        r = list(r)
        for t in cycle:
            i = self.A.index(t)
            r[i] = next(iter(set(self.faces[t]) - {r[i], s[i]}))
        return tuple(r), s

    def neighbors(self, p):
        return [self.reverse_d(p, c) for c in self.dcycles(*p)] + [self.reverse_q(p, c) for c in self.qcycles(p[1])]

    def flow_pair(self):
        f = nx.DiGraph()
        for v in self.X:
            f.add_edge('source', ('v', v), capacity=2)
        for t in self.A:
            f.add_edge(('t', t), 'sink', capacity=2)
            for v in set(self.faces[t]) & set(self.X):
                f.add_edge(('v', v), ('t', t), capacity=1)
        value, flow = nx.maximum_flow(f, 'source', 'sink')
        if value != 2 * self.n:
            return None
        selected = nx.Graph()
        for v in self.X:
            for w, count in flow['v', v].items():
                if count:
                    selected.add_edge(('v', v), w)
        r, s = {}, {}
        for cycle in nx.cycle_basis(selected):
            for j, a in enumerate(cycle):
                b = cycle[(j + 1) % len(cycle)]
                t, v = (a[1], b[1]) if a[0] == 't' else (b[1], a[1])
                (r if j % 2 else s)[t] = v
        return tuple(r[t] for t in self.A), tuple(s[t] for t in self.A)

    def enumerate_tree(self, stats=None):
        """Paper section 6.1, with connectivity and residual-matching prefix tests."""
        stats = stats if stats is not None else Counter()
        def rec(i, used, state, h):
            stats['prefixes'] += 1
            if i == self.n:
                return tuple(state)
            t = self.A[i]
            for v in sorted(set(self.faces[t]) & set(self.X) - used):
                stats['candidates'] += 1
                hh = h.copy()
                hh.remove_edge(('t', t), ('v', v))
                if not nx.is_connected(hh):
                    stats['disconnected'] += 1
                    continue
                rows = [('t', a) for a in self.A[i + 1:]]
                cols = [('v', x) for x in self.X if x not in used | {v}]
                residual = self.B.subgraph(rows + cols)
                if rows and len(nx.bipartite.maximum_matching(residual, top_nodes=rows)) != 2 * len(rows):
                    stats['unextendable'] += 1
                    continue
                found = rec(i + 1, used | {v}, state + [v], hh)
                if found is not None:
                    return found
            return None
        return rec(0, set(), [], self.H)

    def weights(self):
        """Integer circulation by routing unit demands through the embedded dual."""
        if self._weights is not None:
            return self._weights
        rotation = {}
        for v in self.T:
            ts = [self.sides[v, w] for w in self.embedding.neighbors_cw_order(v) if self.sides[v, w] in self.black]
            rotation['v', v] = [('t', t) for t in ts]
        for t in self.black:
            rotation['t', t] = [('v', v) for v in self.faces[t]]
        emb = nx.PlanarEmbedding()
        emb.set_data(rotation)
        emb.check_structure()
        emb.remove_node(('t', self.outer))
        emb.check_structure()
        fs, side = faces_of(emb)
        outer = next(i for i, f in enumerate(fs) if all(('v', r) in f for r in self.R))
        dual = nx.Graph()
        dual.add_nodes_from(range(len(fs)))
        for u, v in emb.to_undirected().edges():
            a, b = side[u, v], side[v, u]
            if a != b:
                dual.add_edge(a, b, spoke=(u, v))
        a = Counter()
        for i in dual:
            if i == outer:
                continue
            path = nx.shortest_path(dual, i, outer)
            for f, g in zip(path, path[1:]):
                u, v = dual[f][g]['spoke']
                if side[u, v] != f:
                    u, v = v, u
                if u[0] == 't':
                    a[u[1], v[1]] += 1
                else:
                    a[v[1], u[1]] -= 1
        for t in self.A:
            shift = min(a[t, v] for v in self.faces[t])
            for v in self.faces[t]:
                a[t, v] -= shift
        self._weights = dict(a)
        return self._weights

    def polynomial(self, pairs=None):
        """Exact integer Z(z); OpenAI Z(x) is i**(-n) Z(exp(x))."""
        a = self.weights()
        coeff = Counter()
        for r, s in self.pairs() if pairs is None else pairs:
            coeff[sum(a[t, v] for t, v in zip(self.A, s))] += self.sign(r, s)
        return {k: v for k, v in sorted(coeff.items()) if v}

    def recover(self, s, prescribed=None):
        """Tree matching -> white tree -> P -> induced trees -> primal cycle."""
        if not self.is_tree(s):
            raise ValueError('Not a tree matching')
        e0 = edge(*self.faces[self.outer][:2]) if prescribed is None else edge(*prescribed)
        y0 = next(y for y in (self.sides[e0], self.sides[e0[::-1]]) if y in self.white)
        wtree = nx.Graph()
        wtree.add_nodes_from(self.white)
        spoke_sides = {}
        for t, v in zip(self.A, s):
            sides = {}
            for u in set(self.faces[t]) - {v}:
                y = next(y for y in (self.sides[v, u], self.sides[u, v]) if y in self.white)
                sides[y] = edge(v, u)
            y, z = sides
            wtree.add_edge(y, z, face=t)
            spoke_sides[t] = sides
        assert nx.is_tree(wtree)
        p = [e0]
        for parent, child in nx.bfs_edges(wtree, y0):
            p.append(spoke_sides[wtree[parent][child]['face']][child])
        forest = nx.Graph()
        forest.add_nodes_from(self.T)
        forest.add_edges_from(p)
        classes = sorted((sorted(c) for c in nx.connected_components(forest)), key=lambda c: c[0])
        cycle_graph = self.G.copy()
        cycle_graph.remove_edges_from(self.dual_edges[e] for e in p)
        cycle = [min(cycle_graph)]
        previous, current = None, cycle[0]
        while True:
            nxt = next(v for v in sorted(cycle_graph[current]) if v != previous)
            if nxt == cycle[0]:
                break
            cycle.append(nxt)
            previous, current = current, nxt
        return {'state': list(s), 'white_tree': sorted(map(list, wtree.edges())), 'white_root': y0,
                'P': p, 'classes': classes, 'cycle': cycle, 'avoided_edge': self.dual_edges[e0]}


def check_cycle(g, cycle, forbidden):
    return len(cycle) == len(g) and len(set(cycle)) == len(g) and set(cycle) == set(g) and all(g.has_edge(u, v) and edge(u, v) != edge(*forbidden) for u, v in zip(cycle, cycle[1:] + cycle[:1]))


def truncate(g):
    """Truncate a polyhedral graph using its rotation system."""
    _, emb = nx.check_planarity(g)
    h = nx.Graph()
    for v in g:
        ns = list(emb.neighbors_cw_order(v))
        for a, b in zip(ns, ns[1:] + ns[:1]):
            h.add_edge((v, a), (v, b))
        for u in ns:
            h.add_edge((v, u), (u, v))
    return nx.convert_node_labels_to_integers(h)


def named_graphs():
    cube = nx.cubical_graph()
    cuboct = nx.line_graph(cube)
    return {'cube': cube, 'hexagonal_prism': nx.circular_ladder_graph(6),
            'truncated_octahedron': truncate(nx.octahedral_graph()),
            'truncated_cuboctahedron': truncate(cuboct)}


def glue_triangles(a, b, fa=0, fb=0):
    """Sphere connected sum along facial triangles, preserving Eulerian degrees."""
    aa, bb = Instance(a), Instance(b)
    mapping = dict(zip(bb.faces[fb], aa.faces[fa]))
    nxt = max(a) + 1
    for v in b:
        if v not in mapping:
            mapping[v] = nxt
            nxt += 1
    return nx.compose(a, nx.relabel_nodes(b, mapping))


def generated(max_vertices=12):
    """Many small duals; NOT exhaustive. Octahedral face insertions, deduplicated."""
    seeds = [nx.octahedral_graph()]
    seeds += [dual_graph(nx.circular_ladder_graph(k)) for k in range(6, 2 * max_vertices - 4, 2) if k + 2 <= max_vertices]
    bysize = {}
    queue = deque(seeds)
    while queue:
        t = queue.popleft()
        if len(t) > max_vertices:
            continue
        bucket = bysize.setdefault(len(t), [])
        if any(nx.is_isomorphic(t, u) for u in bucket):
            continue
        assert nx.node_connectivity(t) >= 3
        bucket.append(t)
        yield t
        if len(t) + 3 <= max_vertices:
            fs = Instance(t).faces
            for f in range(len(fs)):
                queue.append(glue_triangles(t, nx.octahedral_graph(), f, 0))

