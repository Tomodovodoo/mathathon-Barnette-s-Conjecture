"""Constructive algorithms and experimental candidates. All caps are explicit."""
from collections import Counter
import random
import networkx as nx
from .core import Instance, edge


def pool(b, pair, cycle, ccw):
    r, s = pair
    j = sum(b.delta(r[b.A.index(t)], s[b.A.index(t)]) for t in cycle)
    forward = (j == -3) == ccw
    a = b.weights()
    return [(t, k) for t in cycle for k in range(1, a.get((t, (s if forward else r)[b.A.index(t)]), 0) + 1)]


def alpha(b, obj):
    """Orientation involution, constructive paper section 5.1."""
    p, tokens = obj
    cycles = b.dcycles(*p)
    for c in cycles:
        if not any(t in c for t, _ in tokens):
            return b.reverse_d(p, c), tokens
    for c in cycles:
        plus, minus = pool(b, p, c, True), pool(b, p, c, False)
        current_ccw = sum(b.delta(p[0][b.A.index(t)], p[1][b.A.index(t)]) for t in c) == -3
        source = plus if current_ccw else minus
        target = minus if current_ccw else plus
        ranks = [source.index(tok) for tok in tokens if tok[0] in c]
        if not current_ccw or all(i < len(minus) for i in ranks):
            moved = tuple(target[source.index(tok)] if tok[0] in c else tok for tok in tokens)
            return b.reverse_d(p, c), moved
    return obj


def beta(b, obj):
    p, tokens = obj
    cycles = b.qcycles(p[1])
    return (b.reverse_q(p, cycles[0]), tokens) if cycles else obj


def marked_walk(b, pair=None, cap=1000000):
    """Exact marked constructor. cap raises TimeoutError, never reports success."""
    p = pair or b.flow_pair()
    if p is None:
        raise ValueError('No disjoint pair; split first')
    moves, restarts, normalizations = 0, [], 0
    while True:
        cycles = b.dcycles(*p)
        m = len(cycles)
        for c in cycles:
            if sum(b.delta(p[0][b.A.index(t)], p[1][b.A.index(t)]) for t in c) == 3:
                p = b.reverse_d(p, c)
                normalizations += 1
        tokens = tuple(pool(b, p, c, True)[len(pool(b, p, c, False))] for c in cycles)
        obj = p, tokens
        assert alpha(b, obj) == obj
        while True:
            nxt = beta(b, obj)
            if nxt == obj:
                return obj[0], {'moves': moves, 'normalization_reversals': normalizations, 'restarts': restarts}
            obj = nxt
            moves += 1
            nxt = alpha(b, obj)
            if nxt == obj:
                p = obj[0]
                c = len(b.dcycles(*p))
                assert c <= m - 2
                restarts.append([m, c])
                break
            obj = nxt
            moves += 1
            if moves >= cap:
                raise TimeoutError(f'Marked walk cap {cap}')


def exchange_walk(b, p, seed=0, cap=10000, greedy=False):
    rng = random.Random(seed)
    for step in range(cap + 1):
        if b.is_tree(p[1]):
            return p, step
        ns = b.neighbors(p)
        if greedy:
            scores = [len(b.qcycles(q[1])) for q in ns]
            best = min(scores)
            ns = [q for q, score in zip(ns, scores) if score == best]
        p = rng.choice(ns)
    return None, cap


def determinant_sample(b, seed=0):
    """Uniform state via exact determinant extension counts. No tree conditioning."""
    rng = random.Random(seed)
    used, state = set(), []
    for i, t in enumerate(b.A):
        choices = []
        for v in sorted(set(b.faces[t]) & set(b.X) - used):
            rows = list(range(i + 1, b.n))
            cols = [j for j, x in enumerate(b.X) if x not in used | {v}]
            count = abs(int(b.K.extract(rows, cols).det()))
            if count:
                choices.append((v, count))
        pick = rng.randrange(sum(c for _, c in choices))
        for v, count in choices:
            if pick < count:
                state.append(v)
                used.add(v)
                break
            pick -= count
    return tuple(state)


def separators(b):
    """Return triangle, components and black-inner flag relative to the root face."""
    facial = {frozenset(f) for f in b.faces}
    result = []
    for u in b.T:
        for v in b.T[u]:
            if v <= u:
                continue
            for w in set(b.T[u]) & set(b.T[v]):
                if w <= v or frozenset((u, v, w)) in facial:
                    continue
                tri = {u, v, w}
                components = list(nx.connected_components(b.T.subgraph(set(b.T) - tri)))
                if len(components) != 2:
                    continue
                outside = next(c for c in components if c & b.R)
                inside = next(c for c in components if c != outside)
                flags = []
                for a, z in ((u, v), (v, w), (w, u)):
                    f = next(i for i in (b.sides[a, z], b.sides[z, a]) if set(b.faces[i]) - tri <= inside)
                    flags.append(f in b.black)
                assert len(set(flags)) == 1
                result.append((tuple(sorted(tri)), components, flags[0]))
    return result


def solve(b, prescribed=None, stats=None):
    """Recursive induced-tree construction with original T vertex labels retained."""
    stats = stats if stats is not None else Counter()
    e0 = edge(*b.faces[b.outer][:2]) if prescribed is None else edge(*prescribed)
    stats['pieces'] += 1
    pair = b.flow_pair()
    if pair is not None:
        s = pair[1]
        if not b.is_tree(s):
            s = b.enumerate_tree(stats)
        return b.recover(s, e0)
    sep = next((x for x in separators(b) if x[2]), None)
    if sep is None:
        raise AssertionError('Flow obstruction without black separator')
    tri, components, _ = sep
    tri = set(tri)
    outside = next(c for c in components if c & b.R)
    inside = next(c for c in components if c != outside)
    t1 = b.T.subgraph(outside | tri).copy()
    first = Instance(t1)
    root = next(i for i, f in enumerate(first.faces) if set(f) == set(b.faces[b.outer]))
    first = Instance(t1, root)
    a = solve(first, e0, stats)
    labels = {v: i for i, c in enumerate(a['classes']) for v in c}
    same = next(edge(u, v) for u in tri for v in tri if u < v and labels[u] == labels[v])
    t2 = b.T.subgraph(inside | tri).copy()
    second = Instance(t2)
    root = next(i for i, f in enumerate(second.faces) if set(f) == tri)
    second = Instance(t2, root)
    z = solve(second, same, stats)
    labels2 = {v: i for i, c in enumerate(z['classes']) for v in c}
    flip = labels[next(iter(tri))] ^ labels2[next(iter(tri))]
    assert all(labels[v] == labels2[v] ^ flip for v in tri)
    labels.update({v: c ^ flip for v, c in labels2.items()})
    classes = [[v for v in b.T if labels[v] == i] for i in (0, 1)]
    p = [edge(u, v) for u, v in b.T.edges() if labels[u] == labels[v]]
    cycle_g = b.G.copy()
    cycle_g.remove_edges_from(b.dual_edges[e] for e in p)
    cycle = [min(cycle_g)]
    prev, cur = None, cycle[0]
    while True:
        nxt = next(v for v in sorted(cycle_g[cur]) if v != prev)
        if nxt == cycle[0]:
            break
        cycle.append(nxt)
        prev, cur = cur, nxt
    stats['splits'] += 1
    result = {'classes': classes, 'P': p, 'cycle': cycle, 'avoided_edge': b.dual_edges[e0], 'separator': sorted(tri), 'children': [a, z]}
    if hasattr(b, 'primal_labels'):
        result['cycle_original'] = [b.primal_labels[v] for v in cycle]
        result['avoided_edge_original'] = [b.primal_labels[v] for v in b.dual_edges[e0]]
    return result

def white_ground(b):
    ground = []
    for t in b.A:
        for v in sorted(set(b.faces[t]) & set(b.X)):
            ys = []
            for u in set(b.faces[t]) - {v}:
                ys.append(next(y for y in (b.sides[v, u], b.sides[u, v]) if y in b.white))
            ground.append((t, v, *ys))
    return ground


def two_matroid_candidate(b):
    """Exact intersection of face partition and white graphic matroids.
    This deliberately omits the X partition, then reports whether it held anyway.
    """
    ground = white_ground(b)
    def face_independent(ids):
        return len({ground[i][0] for i in ids}) == len(ids)
    def forest(ids):
        uf = nx.utils.UnionFind(b.white)
        for i in ids:
            _, _, u, v = ground[i]
            if uf[u] == uf[v]: return False
            uf.union(u, v)
        return True
    selected = set()
    while True:
        outside = set(range(len(ground))) - selected
        starts = [y for y in outside if face_independent(selected | {y})]
        parent = {y: None for y in starts}
        queue = list(starts)
        endpoint = None
        for y in queue:
            if y not in selected and forest(selected | {y}):
                endpoint = y
                break
            if y in selected:
                ns = [z for z in outside if face_independent(selected - {y} | {z})]
            else:
                ns = [z for z in selected if forest(selected - {z} | {y})]
            for z in ns:
                if z not in parent:
                    parent[z] = y
                    queue.append(z)
        if endpoint is None: break
        path = []
        while endpoint is not None:
            path.append(endpoint)
            endpoint = parent[endpoint]
        selected.symmetric_difference_update(path)
        assert face_independent(selected) and forest(selected)
    spokes = [(ground[i][0], ground[i][1]) for i in sorted(selected)]
    return spokes, len(spokes) == b.n and len({v for t,v in spokes}) == b.n


def wilson_candidate(b, seed=0, cap=100000):
    """Loop-erased walk on the white multigraph, followed by state rejection."""
    rng = random.Random(seed)
    ground = white_ground(b)
    adjacency = {v: [] for v in b.white}
    for i, (_, _, u, v) in enumerate(ground):
        adjacency[u].append((v, i)); adjacency[v].append((u, i))
    tree = {b.white[0]}
    selected = []
    steps = 0
    for start in b.white:
        if start in tree: continue
        path, es = [start], []
        while path[-1] not in tree:
            steps += 1
            if steps > cap: return None
            v, i = rng.choice(adjacency[path[-1]])
            if v in path:
                j = path.index(v)
                path, es = path[:j+1], es[:j]
            else:
                path.append(v); es.append(i)
        tree.update(path)
        selected.extend(es)
    spokes = [(ground[i][0], ground[i][1]) for i in selected]
    if len({t for t,v in spokes}) != b.n or len({v for t,v in spokes}) != b.n:
        return None
    state = dict(spokes)
    s = tuple(state[t] for t in b.A)
    assert b.is_tree(s)
    return s
