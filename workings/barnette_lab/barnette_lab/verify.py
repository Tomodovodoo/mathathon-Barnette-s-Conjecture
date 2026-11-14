"""Run finite verification and write machine-readable evidence. No theorem is inferred."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from math import comb, prod
from pathlib import Path
import time
import networkx as nx
from .core import Instance, named_graphs, generated, edge, check_cycle, faces_of
from .algorithms import alpha, beta, marked_walk, exchange_walk, determinant_sample, separators, solve, pool
from .li import LiObjects, LiMultiObjects


def verify(b, exhaustive_disk=False):
    counts = Counter()
    ss = list(b.states())
    pairs = b.pairs(ss)
    assert abs(int(b.K.det())) == len(ss)
    assert len(ss) ** 2 <= 3 ** b.n
    def permutation_sign(s):
        return (-1) ** sum(a > z for i, a in enumerate(s) for z in s[i + 1:])
    assert len({permutation_sign(s) for s in ss}) <= 1
    counts['states'] = len(ss)
    counts['pairs'] = len(pairs)
    counts['tree_states'] = sum(b.is_tree(s) for s in ss)
    sep = separators(b)
    assert bool(pairs) == (not any(black for _, _, black in sep)) == bool(counts['tree_states'])
    counts['separators'] = len(sep)
    counts['black_separators'] = sum(z[2] for z in sep)
    # Identities 3.1--3.2, every subset, including obstructed roots.
    for bits in (product((0, 1), repeat=b.n) if b.n <= 12 else [tuple(int(v in b.X[:j]) for v in b.X) for j in range(b.n + 1)]):
        s = {v for v, bit in zip(b.X, bits) if bit}
        u = set(b.T) - s
        lhs = sum(min(2, len(set(b.faces[t]) & s)) for t in b.A) - 2 * len(s)
        density = 2 * len(u) - 4 - b.T.subgraph(u).number_of_edges() + sum(set(b.faces[t]) <= u for t in b.black)
        assert lhs == density
        if not sep:
            assert lhs >= 0
        counts['subset_checks'] += 1
    # Component bound 3.4, induced connected subsets of size >=4.
    if not sep and len(b.T) <= 14:
        for bits in product((0, 1), repeat=len(b.T)):
            u = {v for v, bit in zip(b.T, bits) if bit}
            k = b.T.subgraph(u)
            if len(u) >= 4 and nx.is_connected(k):
                black = sum(set(b.faces[t]) <= u for t in b.black)
                assert k.number_of_edges() - black <= 2 * len(u) - 4
                counts['component_density_checks'] += 1
    a = b.weights()
    assert min(a.values(), default=0) >= 0 and max(a.values(), default=0) <= 6 * b.n
    # Every directed cycle achievable by an outgoing choice of a fixed state.
    disk_states = ss if exhaustive_disk else sorted({p[0] for p in pairs})
    for r in disk_states:
        choices = [[v for v in b.faces[t] if v != r[i]] for i, t in enumerate(b.A)]
        selections = product(*choices) if exhaustive_disk else [p[1] for p in pairs if p[0] == r]
        for heads in selections:
            d = nx.DiGraph()
            d.add_edges_from((v, w, {'face': t}) for t, v, w in zip(b.A, r, heads))
            for c in nx.simple_cycles(d):
                h = len(c)
                assert not set(c) & b.R
                boundary = {edge(v, w) for v, w in zip(c, c[1:] + c[:1])}
                dual = b.G.copy()
                dual.remove_edges_from(b.dual_edges[e] for e in boundary)
                outside = nx.node_connected_component(dual, b.outer)
                inside_faces = set(b.G) - outside
                vertices = set().union(*(set(b.faces[t]) for t in inside_faces)) - set(c)
                black = len(inside_faces & set(b.black))
                white = len(inside_faces & set(b.white))
                l = sum(next(t for t in (b.sides[e], b.sides[e[::-1]]) if t in b.black) in inside_faces for e in boundary)
                assert black + white == 2 * len(vertices) + h - 2
                assert 3 * (black - white) == 2 * l - h
                assert black == len(vertices) + l
                assert sum(b.delta(v, w) for v, w in zip(c, c[1:] + c[:1])) == (-3 if b.sides[c[0], c[1]] in inside_faces else 3)
                counts['disk_cycles'] += 1
    for s in ss:
        mates = [r for r, z in pairs if z == s]
        q = b.Q(s)
        components = list(nx.connected_components(q))
        admissible = all((q.subgraph(c).number_of_edges() == len(c) - 1 and len(c & b.R) == 1) or (q.subgraph(c).number_of_edges() == len(c) and not c & b.R) for c in components)
        k = sum(q.subgraph(c).number_of_edges() == len(c) for c in components)
        assert len(mates) == (2 ** k if admissible else 0)
        assert b.is_tree(s) == (len(mates) == 1)
        if b.qcycles(s):
            assert sum(b.sign(r, s) for r in mates) == 0
        if b.is_tree(s):
            assert nx.is_forest(q) and all(len(c & b.R) == 1 for c in components)
            for e0 in combinations(b.faces[b.outer], 2):
                cert = b.recover(s, e0)
                assert len(cert['classes']) == 2
                assert all(nx.is_tree(b.T.subgraph(c)) for c in cert['classes'])
                assert check_cycle(b.G, cert['cycle'], cert['avoided_edge'])
                assert len(cert['P']) == b.n + 1
                assert all(sum(set(e) <= set(f) for e in cert['P']) == 1 for f in b.faces)
                counts['recovery_checks'] += 1
    exchange = nx.Graph()
    exchange.add_nodes_from(pairs)
    for p in pairs:
        assert b.valid(p[0]) and b.valid(p[1])
        for q in b.neighbors(p):
            assert q in exchange
            assert b.sign(*q) == -b.sign(*p)
            assert p in b.neighbors(q)
            exchange.add_edge(p, q)
            counts['exchange_checks'] += 1
        for c in b.dcycles(*p):
            assert len(c) % 2 == 1
            assert len(pool(b, p, c, True)) > len(pool(b, p, c, False))
        found, stats = marked_walk(b, p)
        assert b.is_tree(found[1])
        counts['marked_runs'] += 1
        counts['marked_moves'] += stats['moves']
    for p in pairs:
        tokens = [(t, k) for t, v in zip(b.A, p[1]) for k in range(1, a.get((t, v), 0) + 1)]
        for token in tokens:
            obj = p, (token,)
            for inv in (alpha, beta):
                image = inv(b, obj)
                assert inv(b, image) == obj
                if image != obj:
                    assert b.sign(*image[0]) == -b.sign(*p)
                counts['marked_involution_checks'] += 1
    for component in nx.connected_components(exchange):
        trees = [p for p in component if b.is_tree(p[1])]
        assert trees and sum(b.sign(*p) for p in trees) == 0
        polynomial = b.polynomial(component)
        assert polynomial and sum(polynomial.values()) == 0
        m = min(len(b.dcycles(*p)) for p in component)
        first = sum(v * comb(k, m) for k, v in polynomial.items() if k >= m)
        assert first and first * (-1) ** ((b.n - m) // 2) > 0
        for j in range(m):
            assert sum(v * comb(k, j) for k, v in polynomial.items() if k >= j) == 0
        counts['exchange_components'] += 1
    # Li c_min=1 only, exact half-rays, full object set for this case.
    if pairs and min(len(b.dcycles(*p)) for p in pairs) == 1:
        li = LiObjects(b)
        objects = list(li.objects(pairs))
        fixed_signs = set()
        fixed_count = 0
        for obj in objects:
            for involution in (li.iota1, li.iota2):
                image = involution(obj)
                assert involution(image) == obj
                if image != obj:
                    assert li.sign(image) != li.sign(obj)
            if li.iota2(obj) == obj:
                fixed_signs.add(li.sign(obj))
                fixed_count += 1
            counts['li_objects'] += 1
        assert fixed_count and len(fixed_signs) == 1
    if pairs and b.n <= 11 and min(len(b.dcycles(*p)) for p in pairs) > 1:
        li = LiMultiObjects(b)
        fixed_signs = set()
        for obj in li.objects(pairs):
            for inv in (li.iota1, li.iota2):
                image = inv(obj)
                assert inv(image) == obj
                if image != obj: assert li.sign(image) != li.sign(obj)
            if li.iota2(obj) == obj: fixed_signs.add(li.sign(obj))
            counts['li_multi_objects'] += 1
        assert len(fixed_signs) == 1
    for e0 in combinations(b.faces[b.outer], 2):
        cert = solve(b, e0)
        assert check_cycle(b.G, cert['cycle'], cert['avoided_edge'])
        assert all(nx.is_tree(b.T.subgraph(c)) for c in cert['classes'])
        counts['recursive_checks'] += 1
    counts['T_vertices'] = len(b.T)
    counts['G_vertices'] = len(b.G)
    return dict(counts)


def export(b):
    ss = list(b.states())
    s = b.enumerate_tree()
    mate = next(r for r in ss if all(x != y for x, y in zip(r, s)))
    pair = mate, s
    return {'schema': 1, 'T_edges': sorted(map(list, b.T.edges())), 'T_rotation': {str(v): list(b.embedding.neighbors_cw_order(v)) for v in b.T},
            'G_edges': sorted(map(list, b.G.edges())), 'faces': b.faces, 'black': b.black, 'white': b.white, 'outer': b.outer,
            'roots': sorted(b.R), 'A': b.A, 'X': b.X, 'states': ss, 'pair': pair,
            'D_edges': list(zip(*pair)) if pair else None, 'Q_edges': sorted(map(list, b.Q(s).edges())),
            'J': b.J(*pair) if pair else None, 'delta': [[u, v, b.delta(u, v)] for u, v in b.T.edges()],
            'H_edges': list(b.H.edges()), 'weights': [[t, v, w] for (t, v), w in sorted(b.weights().items())],
            'Z_coefficients': b.polynomial(), 'tree_matching': s, 'certificate': b.recover(s)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-dual-vertices', type=int, default=10)
    parser.add_argument('--plantri', type=Path)
    parser.add_argument('--plantri-max', type=int, default=14)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rows = []
    graphs = [(name, Instance.from_primal(g)) for name, g in named_graphs().items()]
    graphs += [(f'generated_{i}', Instance(t)) for i, t in enumerate(generated(args.max_dual_vertices))]
    if args.plantri:
        from .core import plantri_graphs
        for n in range(6, args.plantri_max + 1):
            graphs += [(f'plantri_{n}_{i}', Instance(t)) for i, t in enumerate(plantri_graphs(n, args.plantri.resolve()))]
    # Both boundary colors occur by rerooting a glued example.
    from .core import glue_triangles
    glued = glue_triangles(nx.octahedral_graph(), nx.octahedral_graph())
    graphs += [(f'glued_root_{i}', Instance(glued, i)) for i in range(14)]
    for name, b in graphs:
        start = time.perf_counter()
        row = verify(b, exhaustive_disk=b.n <= 6)
        row.update(name=name, seconds=time.perf_counter() - start, disk_mode='all outgoing choices' if b.n <= 6 else 'pair D cycles only')
        rows.append(row)
        print(name, row, flush=True)
    (args.output / 'verification.json').write_text(json.dumps(rows, indent=2))
    for name in ('cube', 'truncated_octahedron'):
        b = Instance.from_primal(named_graphs()[name])
        (args.output / f'{name}.json').write_text(json.dumps(export(b), indent=2))

if __name__ == '__main__':
    main()
