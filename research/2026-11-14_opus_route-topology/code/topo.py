"""Topological experiments on the Barnette proof objects.

Uses the shared reference implementation in workings/barnette_lab (read only).
Run from the repository root:

    python research/2026-11-14_opus_route-topology/code/topo.py <experiment> [maxV]

Experiments: disk, ham, lattice, hyper, degpoly, nodal, morse, all.
Each writes research/2026-11-14_opus_route-topology/data/<experiment>.json.
"""
import json
import random
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'workings' / 'barnette_lab'))
import networkx as nx  # noqa: E402
from barnette_lab.core import Instance, plantri_graphs, named_graphs, edge  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / 'data'
PLANTRI = ROOT / 'workings' / 'barnette_lab' / 'vendor' / 'plantri.exe'


# ---------------------------------------------------------------- instances
def triangulations(max_v=14, min_v=6):
    for v in range(min_v, max_v + 1):
        try:
            yield from ((v, i, t) for i, t in enumerate(plantri_graphs(v, PLANTRI)))
        except Exception:  # plantri reports no output for impossible orders
            continue


def rooted_instances(max_v=14, all_roots_up_to=12, min_v=6):
    """Every plantri Eulerian triangulation; every black outer face up to all_roots_up_to vertices,
    otherwise the first face of each colour class."""
    for v, i, t in triangulations(max_v, min_v):
        base = Instance(t)
        faces = range(len(base.faces))
        if v > all_roots_up_to:
            faces = [0, next(f for f in faces if f not in base.black)]
        for f in faces:
            try:
                yield {'V': v, 'index': i, 'outer': f}, Instance(t, f)
            except Exception:
                continue


# ---------------------------------------------------------------- geometry helpers
def colouring(inst):
    """3-colouring c with delta(u,v) = c(v)-c(u) mod 3 (lifted to +-1); None if inconsistent."""
    start = next(iter(inst.T))
    c = {start: 0}
    queue = [start]
    while queue:
        u = queue.pop()
        for v in inst.T[u]:
            want = (c[u] + inst.delta(u, v)) % 3
            if v not in c:
                c[v] = want
                queue.append(v)
            elif c[v] != want:
                return None
    return c


def inside_faces(inst, cycle):
    """Faces of T on the bounded side of the simple cycle (vertex list), i.e. away from the outer face."""
    cut = {inst.dual_edges[edge(a, b)] for a, b in zip(cycle, cycle[1:] + cycle[:1])}
    g = inst.G.copy()
    g.remove_edges_from(cut)
    outside = nx.node_connected_component(g, inst.outer)
    return set(inst.G) - outside


def disk_data(inst, cycle):
    ins = inside_faces(inst, cycle)
    b = sum(1 for f in ins if f in inst.black)
    w = len(ins) - b
    on = set(cycle)
    interior = {v for f in ins for v in inst.faces[f]} - on
    return ins, b, w, len(interior)


def positive_side(inst, cycle, ins):
    """+1 if the bounded side is the side that inst.delta counts as 'black side' (sides[u,v])."""
    a, b = cycle[0], cycle[1]
    return 1 if inst.sides[a, b] in ins else -1


# ---------------------------------------------------------------- experiment: disk identity
def exp_disk(max_v=14, samples=40, seed=1):
    rnd = random.Random(seed)
    rec = Counter()
    bad = []
    for meta, inst in rooted_instances(max_v):
        c = colouring(inst)
        rec['instances'] += 1
        rec['colouring_consistent'] += c is not None
        states = list(inst.states())
        if not states:
            continue
        for _ in range(samples):
            r = rnd.choice(states)
            # P1: random out-edge per black face from r(t); functional graph on X
            out = {}
            for t, v in zip(inst.A, r):
                out[v] = rnd.choice([u for u in inst.faces[t] if u != v])
            seen = set()
            for x in inst.X:
                path, y = [], x
                while y in out and y not in seen and y not in path:
                    path.append(y)
                    y = out[y]
                seen.update(path)
                if y in path:
                    cyc = path[path.index(y):]
                    ins, B, W, I = disk_data(inst, cyc)
                    h = len(cyc)
                    dsum = sum(inst.delta(a, b) for a, b in zip(cyc, cyc[1:] + cyc[:1]))
                    side = positive_side(inst, cyc, ins)
                    rec['P1_cycles'] += 1
                    ok = (W == B + 1) and (B + W == 2 * I + h - 2) and (side * dsum == 3 * (B - W))
                    rec['P1_ok'] += ok
                    if c is not None:
                        wind = sum(((c[b] - c[a] + 1) % 3) - 1 for a, b in zip(cyc, cyc[1:] + cyc[:1]))
                        rec['P3_ok'] += (wind == dsum)
                    if not ok:
                        bad.append({'meta': meta, 'P': 1, 'cycle': cyc, 'B': B, 'W': W, 'I': I})
            # P2: random simple cycles avoiding roots, with a random state s
            s = rnd.choice(states)
            match = {v: t for t, v in zip(inst.A, s)}  # vertex -> its matched black face
            sub = inst.T.subgraph(inst.X)
            if sub.number_of_edges() == 0:
                continue
            for cyc in nx.cycle_basis(sub)[:5]:
                ins, B, W, I = disk_data(inst, cyc)
                h = len(cyc)
                m = sum(1 for v in cyc if match[v] in ins)
                rec['P2_cycles'] += 1
                ok = (B - W == 2 * m - h + 2)
                rec['P2_ok'] += ok
                if not ok:
                    bad.append({'meta': meta, 'P': 2, 'cycle': cyc, 'B': B, 'W': W, 'm': m})
    return {'counts': dict(rec), 'failures': bad[:20]}


# ---------------------------------------------------------------- Hamiltonian cycles of G
def ham_cycles(g):
    """All Hamiltonian cycles of a small graph, as frozensets of edges."""
    nodes = sorted(g)
    start = nodes[0]
    n = len(nodes)
    found = set()
    path = [start]
    used = {start}

    def rec():
        u = path[-1]
        if len(path) == n:
            if g.has_edge(u, start):
                es = frozenset(edge(a, b) for a, b in zip(path, path[1:] + path[:1]))
                found.add(es)
            return
        for w in g[u]:
            if w not in used:
                used.add(w)
                path.append(w)
                rec()
                path.pop()
                used.discard(w)
    rec()
    return found


def state_of_cycle(inst, cyc_edges, e0):
    """Hamiltonian cycle of G avoiding e0* -> forest P -> state s (orient P - e0 towards roots)."""
    crossed = {e for e, d in inst.dual_edges.items() if d in cyc_edges}
    P = [e for e in map(lambda e: e, inst.dual_edges) if e not in crossed]
    f = nx.Graph()
    f.add_nodes_from(inst.T)
    f.add_edges_from(e for e in P if e != e0)
    tail = {}
    for comp in nx.connected_components(f):
        roots = comp & inst.R
        if len(roots) != 1:
            return None, P
        root = next(iter(roots))
        for a, b in nx.bfs_edges(f.subgraph(comp), root):
            tail[edge(a, b)] = b  # oriented b -> a, towards root
    s = []
    for t in inst.A:
        e = next(edge(a, b) for a, b in combinations(inst.faces[t], 2) if edge(a, b) in tail)
        s.append(tail[e])
    return tuple(s), P


def exp_ham(max_v=14):
    rows = []
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        states = list(inst.states())
        trees = [s for s in states if inst.is_tree(s)]
        hc = ham_cycles(inst.G)
        e0 = edge(*inst.faces[inst.outer][:2])
        e0d = inst.dual_edges[e0]
        avoid = [c for c in hc if e0d not in c]
        thr = Counter(e for c in hc for e in c)
        images = []
        for s in trees:
            res = inst.recover(s)
            cyc = res['cycle']
            images.append(frozenset(edge(a, b) for a, b in zip(cyc, cyc[1:] + cyc[:1])))
        back = Counter()
        for c in avoid:
            s, _ = state_of_cycle(inst, c, e0)
            back['valid_state'] += s is not None and inst.valid(s)
            back['tree_state'] += s is not None and inst.is_tree(s)
        rows.append({**meta, 'n': inst.n, 'states': len(states), 'tree_matchings': len(trees),
                     'ham_total': len(hc), 'ham_avoiding_e0': len(avoid),
                     'recovery_injective': len(set(images)) == len(images),
                     'image_subset_of_avoiding': set(images) <= set(avoid),
                     'cycles_whose_state_is_tree': back['tree_state'],
                     'cycles_whose_state_is_valid': back['valid_state'],
                     'thomason_even_all_edges': all(thr[e] % 2 == 0 for e in inst.G.edges() for e in [edge(*e)]),
                     'pair_exists': inst.flow_pair() is not None})
    return rows


# ---------------------------------------------------------------- state lattice (clock moves)
def exp_lattice(max_v=14):
    rows = []
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        states = list(inst.states())
        if len(states) < 1:
            continue
        idx = {s: i for i, s in enumerate(states)}
        up = defaultdict(set)
        dg = nx.DiGraph()
        dg.add_nodes_from(range(len(states)))
        # clock move: states differing exactly on a D-cycle of length 3
        for i, r in enumerate(states):
            for j in range(i + 1, len(states)):
                s = states[j]
                diff = [k for k in range(inst.n) if r[k] != s[k]]
                if len(diff) != 3:
                    continue
                J = sum(inst.delta(r[k], s[k]) for k in diff)
                if abs(J) != 3:
                    continue
                if J > 0:
                    dg.add_edge(i, j)
                else:
                    dg.add_edge(j, i)
        und = dg.to_undirected()
        connected = nx.is_connected(und) if len(states) > 1 else True
        acyclic = nx.is_directed_acyclic_graph(dg)
        sources = [v for v in dg if dg.in_degree(v) == 0]
        sinks = [v for v in dg if dg.out_degree(v) == 0]
        trees = {idx[s] for s in states if inst.is_tree(s)}
        # height = longest path from the unique source (graded if lattice)
        height = {}
        if acyclic and len(sources) == 1:
            for v in nx.topological_sort(dg):
                height[v] = max((height[u] + 1 for u in dg.predecessors(v)), default=0)
        reach = {v: nx.descendants(dg, v) for v in dg} if len(states) <= 400 else None
        antichain = reach is not None and all(b not in reach[a] for a in trees for b in trees if a != b)
        interval = None
        if reach is not None and trees:
            lo = [a for a in trees if all(a == b or b in reach[a] for b in trees)]
            hi = [a for a in trees if all(a == b or a in reach[b] for b in trees)]
            if lo and hi:
                iv = {v for v in dg if (v == lo[0] or v in reach[lo[0]]) and (v == hi[0] or hi[0] in reach[v])}
                interval = iv == trees
            else:
                interval = False
        # J between a tree matching and its unique mate, and lattice distance
        mate_info = []
        for s in states:
            if not inst.is_tree(s):
                continue
            mates = [r for r in states if all(a != b for a, b in zip(r, s))]
            if len(mates) == 1 and height:
                mate_info.append((height[idx[s]], height[idx[mates[0]]], inst.J(mates[0], s)))
        rows.append({**meta, 'n': inst.n, 'states': len(states), 'connected': connected, 'acyclic': acyclic,
                     'sources': len(sources), 'sinks': len(sinks), 'trees': len(trees),
                     'bottom_is_tree': bool(sources) and sources[0] in trees,
                     'top_is_tree': bool(sinks) and sinks[0] in trees,
                     'tree_heights': sorted(height[v] for v in trees) if height else None,
                     'max_height': max(height.values()) if height else None,
                     'trees_antichain': antichain, 'trees_interval': interval,
                     'mate_heights_and_J': mate_info})
    return rows


# ---------------------------------------------------------------- hypertrees (Kalman) of states
def hypertree(inst, s, c, src, dst):
    """Kalman Thm 10.5 style: for each point p of colour dst, count black faces t containing p whose
    state vertex has colour src."""
    f = Counter()
    for t, v in zip(inst.A, s):
        if c[v] == src:
            p = next(u for u in inst.faces[t] if c[u] == dst)
            f[p] += 1
    pts = sorted(p for p in inst.T if c[p] == dst)
    return tuple(f[p] for p in pts)


def hull_position(points, target):
    """'vertex' if target is not a convex combination of the other points, else 'nonvertex'."""
    import numpy as np
    from scipy.optimize import linprog
    others = [p for p in points if p != target]
    if not others:
        return 'vertex'
    A = np.array(others, dtype=float).T
    A_eq = np.vstack([A, np.ones(len(others))])
    b_eq = np.append(np.array(target, dtype=float), 1.0)
    res = linprog(np.zeros(len(others)), A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
    return 'nonvertex' if res.status == 0 else 'vertex'


def exp_hyper(max_v=12):
    rows = []
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        c = colouring(inst)
        states = list(inst.states())
        if len(states) < 2:
            continue
        res = {}
        for src, dst in [(0, 1), (1, 2), (2, 0), (1, 0), (2, 1), (0, 2)]:
            vecs = [hypertree(inst, s, c, src, dst) for s in states]
            injective = len(set(vecs)) == len(vecs)
            pos = Counter()
            for s, vct in zip(states, vecs):
                pos[(inst.is_tree(s), hull_position(vecs, vct))] += 1
            res[f'{src}->{dst}'] = {'injective': injective,
                                    'tree_vertex': pos[(True, 'vertex')], 'tree_nonvertex': pos[(True, 'nonvertex')],
                                    'nontree_vertex': pos[(False, 'vertex')], 'nontree_nonvertex': pos[(False, 'nonvertex')]}
        rows.append({**meta, 'n': inst.n, 'states': len(states), 'hyper': res})
    return rows


# ---------------------------------------------------------------- two-sided degree polytope of H
def spanning_tree_degree_vectors(h, limit=300000):
    """Two-sided degree vectors of all spanning trees of a small graph (edge-subset enumeration with pruning)."""
    nodes = sorted(h, key=str)
    pos = {v: i for i, v in enumerate(nodes)}
    edges = [tuple(sorted((pos[a], pos[b]))) for a, b in h.edges()]
    n = len(nodes)
    out = set()
    count = 0

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    deg = [0] * n

    def rec(i, k):
        nonlocal count
        if k == n - 1:
            out.add(tuple(deg))
            count += 1
            return
        if count > limit or len(edges) - i < n - 1 - k:
            return
        a, b = edges[i]
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            deg[a] += 1
            deg[b] += 1
            rec(i + 1, k + 1)
            deg[a] -= 1
            deg[b] -= 1
            parent[ra] = ra
        rec(i + 1, k)

    rec(0, 0)
    return nodes, out, count <= limit


def in_hull(points, target):
    import numpy as np
    from scipy.optimize import linprog
    pts = list(points)
    A = np.array(pts, dtype=float).T
    A_eq = np.vstack([A, np.ones(len(pts))])
    b_eq = np.append(np.array(target, dtype=float), 1.0)
    res = linprog(np.zeros(len(pts)), A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
    return res.status == 0


def lattice_points_in_hull(points, bounds):
    """Enumerate integer vectors inside the box with the right sum and test hull membership (small cases)."""
    import itertools
    total = sum(next(iter(points)))
    cand = []
    ranges = [range(lo, hi + 1) for lo, hi in bounds]
    for v in itertools.product(*ranges):
        if sum(v) == total:
            cand.append(v)
    return cand


def exp_degpoly(max_v=12, saturation_cases=40):
    rows = []
    sat_checked = 0
    for meta, inst in rooted_instances(max_v, all_roots_up_to=12):
        nodes, vecs, complete = spanning_tree_degree_vectors(inst.H)
        if not complete:
            continue
        target = []
        for v in nodes:
            if v[0] == 't':
                target.append(3 if v[1] == inst.outer else 2)
            else:
                target.append(inst.H.degree(v) - (0 if v[1] in inst.R else 1))
        target = tuple(target)
        has_tree = any(inst.is_tree(s) for s in inst.states())
        row = {**meta, 'n': inst.n, 'tree_degree_vectors': len(vecs), 'tree_matching_exists': has_tree,
               'target_realised': target in vecs, 'target_in_hull': in_hull(vecs, target)}
        # one-sided realisability of the target (point side alone, black side alone)
        bl = [i for i, v in enumerate(nodes) if v[0] == 't']
        pt = [i for i, v in enumerate(nodes) if v[0] == 'v']
        row['black_side_realised'] = any(all(w[i] == target[i] for i in bl) for w in vecs)
        row['point_side_realised'] = any(all(w[i] == target[i] for i in pt) for w in vecs)
        # saturation on small H: every lattice point of the hull is realised?
        if sat_checked < saturation_cases and len(nodes) <= 12:
            bounds = [(1, inst.H.degree(v)) for v in nodes]
            cands = lattice_points_in_hull(vecs, bounds)
            missing = [v for v in cands if v not in vecs and in_hull(vecs, v)]
            row['saturation_missing'] = [list(v) for v in missing[:5]]
            row['saturation_checked'] = True
            sat_checked += 1
        rows.append(row)
    return rows


# ---------------------------------------------------------------- nodal partitions
def is_two_tree_partition(t, side):
    a = [v for v in t if side[v]]
    b = [v for v in t if not side[v]]
    if not a or not b:
        return False
    return nx.is_tree(t.subgraph(a)) and nx.is_tree(t.subgraph(b))


def exp_nodal(max_v=16):
    import numpy as np
    rec = Counter()
    examples = []
    for v, i, t in triangulations(max_v):
        nodes = sorted(t)
        L = nx.laplacian_matrix(t, nodelist=nodes).toarray().astype(float)
        w, vec = np.linalg.eigh(L)
        for k in range(1, len(nodes)):
            x = vec[:, k]
            if np.any(np.abs(x) < 1e-9):
                rec['zero_entries_skipped'] += 1
                continue
            side = {u: x[j] > 0 for j, u in enumerate(nodes)}
            ok = is_two_tree_partition(t, side)
            rec['eigenvectors'] += 1
            rec['two_tree'] += ok
            rec[f'two_tree_index_{k}'] += ok
            if ok and len(examples) < 10:
                examples.append({'V': v, 'index': i, 'eigen_index': k, 'eigenvalue': float(w[k])})
        # how many partitions are two-tree at all (small V only)
        if v <= 12:
            tot = sum(1 for mask in range(1, 2 ** (len(nodes) - 1))
                      if is_two_tree_partition(t, {u: bool(mask >> j & 1) for j, u in enumerate(nodes)}))
            rec['two_tree_partitions_total_small'] += tot
            rec['partitions_total_small'] += 2 ** (len(nodes) - 1) - 1
    return {'counts': dict(rec), 'examples': examples}


# ---------------------------------------------------------------- Morse / cube structure of the cancellation
def exp_morse(max_v=14):
    """For fixed s: mates <-> sign vectors on the cycles of Q_s; J = J_ccw + 2 * #clockwise Q-cycles."""
    rec = Counter()
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        states = list(inst.states())
        for s in states:
            mates = [r for r in states if all(a != b for a, b in zip(r, s))]
            if not mates:
                continue
            k = len(inst.qcycles(s))
            rec['states_with_mates'] += 1
            rec['mate_count_is_2^k'] += len(mates) == 2 ** k
            Js = sorted(inst.J(r, s) for r in mates)
            jmin = Js[0]
            # binomial distribution of J levels: number of mates at level jmin + 2i equals C(k, i)
            from math import comb
            levels = Counter((j - jmin) // 2 for j in Js)
            rec['levels_binomial'] += all(levels[i] == comb(k, i) for i in range(k + 1))
            rec['signed_sum_is_indicator'] += sum(inst.sign(r, s) for r in mates) == (inst.sign(mates[0], s) if k == 0 else 0)
    return dict(rec)


EXPERIMENTS = {'disk': exp_disk, 'ham': exp_ham, 'lattice': exp_lattice, 'hyper': exp_hyper,
               'degpoly': exp_degpoly, 'nodal': exp_nodal, 'morse': exp_morse}


def main():
    name = sys.argv[1]
    names = list(EXPERIMENTS) if name == 'all' else [name]
    OUT.mkdir(exist_ok=True)
    for nm in names:
        args = [int(a) for a in sys.argv[2:]]
        result = EXPERIMENTS[nm](*args)
        (OUT / f'{nm}.json').write_text(json.dumps({'command': ' '.join(['python', 'research/2026-11-14_opus_route-topology/code/topo.py'] + sys.argv[1:]),
                                                     'result': result}, indent=1, default=str))
        print(nm, 'done')



# ---------------------------------------------------------------- lattice, part 2: mate involution and area height
def heights(inst, states):
    idx = {s: i for i, s in enumerate(states)}
    dg = nx.DiGraph()
    dg.add_nodes_from(range(len(states)))
    for i, r in enumerate(states):
        for j in range(i + 1, len(states)):
            s = states[j]
            diff = [k for k in range(inst.n) if r[k] != s[k]]
            if len(diff) == 3:
                J = sum(inst.delta(r[k], s[k]) for k in diff)
                if J == 3:
                    dg.add_edge(i, j)
                elif J == -3:
                    dg.add_edge(j, i)
    h = {}
    for v in nx.topological_sort(dg):
        h[v] = max((h[u] + 1 for u in dg.predecessors(v)), default=0)
    return {s: h[idx[s]] for s in states}


def relative_cycles(inst, r, s):
    """Cycles of the relative permutation r(t) -> s(t) on faces where r and s differ."""
    nxt = {r[k]: (s[k], inst.A[k]) for k in range(inst.n) if r[k] != s[k]}
    seen, cycles = set(), []
    for v in nxt:
        if v in seen:
            continue
        cyc = [v]
        seen.add(v)
        w = nxt[v][0]
        while w != v:
            cyc.append(w)
            seen.add(w)
            w = nxt[w][0]
        cycles.append(cyc)
    return cycles


def exp_lattice2(max_v=14, pair_samples=400, seed=2):
    rnd = random.Random(seed)
    rec = Counter()
    bad = []
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        states = list(inst.states())
        h = heights(inst, states)
        trees = [s for s in states if inst.is_tree(s)]
        for s in trees:
            mates = [r for r in states if all(a != b for a, b in zip(r, s))]
            rec['tree_matchings'] += 1
            rec['mate_is_tree'] += inst.is_tree(mates[0])
        # height difference versus enclosed areas of the relative cycles
        for _ in range(min(pair_samples, len(states) ** 2)):
            r, s = rnd.choice(states), rnd.choice(states)
            if r == s:
                continue
            area = 0
            for cyc in relative_cycles(inst, r, s):
                ins, B, W, I = disk_data(inst, cyc)
                dsum = sum(inst.delta(a, b) for a, b in zip(cyc, cyc[1:] + cyc[:1]))
                rec['rel_cycles'] += 1
                rec['rel_cycle_W_eq_B_plus_1'] += W == B + 1
                area += (dsum // 3) * W  # dsum/3 = +-1 is the orientation in the delta convention
            rec['pairs'] += 1
            ok = (h[s] - h[r] == area)
            rec['height_eq_signed_white_area'] += ok
            if not ok and len(bad) < 5:
                bad.append({'meta': meta, 'dh': h[s] - h[r], 'area': area})
    return {'counts': dict(rec), 'failures': bad}


EXPERIMENTS['lattice2'] = exp_lattice2



# ---------------------------------------------------------------- root-polytope triangulations (Kalman-Murakami)
def colour_tree(inst, s, c, col):
    """Edges of colour col (both ends of the other two colours) that are NOT in Q_s."""
    q = {edge(*e) for e in inst.Q(s).edges()}
    return frozenset(edge(a, b) for a, b in inst.T.edges() if c[a] != col and c[b] != col and edge(a, b) not in q)


def exp_rootpoly(max_v=14):
    rec = Counter()
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        c = colouring(inst)
        states = list(inst.states())
        clock = set()
        for i, r in enumerate(states):
            for j in range(i + 1, len(states)):
                s = states[j]
                diff = [k for k in range(inst.n) if r[k] != s[k]]
                if len(diff) == 3 and abs(sum(inst.delta(r[k], s[k]) for k in diff)) == 3:
                    clock.add((i, j))
        for col in range(3):
            gc = nx.Graph()
            gc.add_nodes_from(v for v in inst.T if c[v] != col)
            gc.add_edges_from((a, b) for a, b in inst.T.edges() if c[a] != col and c[b] != col)
            trees = [colour_tree(inst, s, c, col) for s in states]
            rec['colour_classes'] += 1
            rec['all_spanning_trees'] += all(nx.is_tree(gc.edge_subgraph(t).copy()) and len(t) == gc.number_of_nodes() - 1 for t in trees)
            rec['injective'] += len(set(trees)) == len(trees)
            facet = {(i, j) for i in range(len(states)) for j in range(i + 1, len(states)) if len(trees[i] ^ trees[j]) == 2}
            rec['clock_subset_facet'] += clock <= facet
            rec['clock_eq_facet'] += clock == facet
            rec['facet_pairs'] += len(facet)
            rec['clock_pairs'] += len(clock)
    return dict(rec)


EXPERIMENTS['rootpoly'] = exp_rootpoly



# ---------------------------------------------------------------- split lattice2 results by separating triangles
def separating_triangles(inst):
    faces = {frozenset(f) for f in inst.faces}
    out = []
    for a, b in inst.T.edges():
        for c in set(inst.T[a]) & set(inst.T[b]):
            tri = frozenset((a, b, c))
            if c > max(a, b) and tri not in faces:
                out.append(tri)
    return out


def exp_sepcheck(max_v=14, pair_samples=200, seed=5):
    rnd = random.Random(seed)
    rec = Counter()
    fails = []
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        st = bool(separating_triangles(inst))
        states = list(inst.states())
        h = heights(inst, states)
        for s in states:
            if inst.is_tree(s):
                m = next(r for r in states if all(a != b for a, b in zip(r, s)))
                ok = inst.is_tree(m)
                rec[f'mate_tree sep={st} ok={ok}'] += 1
                if not ok and len(fails) < 6:
                    fails.append({**meta, 's': s, 'mate': m, 'Q_mate_cycles': inst.qcycles(m)})
        for _ in range(pair_samples):
            r, s = rnd.choice(states), rnd.choice(states)
            if r == s:
                continue
            area = 0
            for cyc in relative_cycles(inst, r, s):
                ins, B, W, I = disk_data(inst, cyc)
                d = sum(inst.delta(a, b) for a, b in zip(cyc, cyc[1:] + cyc[:1]))
                area += (d // 3) * W
            rec[f'height sep={st} ok={h[s] - h[r] == area}'] += 1
    return {'counts': dict(rec), 'mate_failures': fails}


EXPERIMENTS['sepcheck'] = exp_sepcheck



# ---------------------------------------------------------------- one-sided hypertree test by matroid intersection
def spanning_tree_with_caps(h, cap):
    """Max common independent set of the graphic matroid of h and the partition matroid
    'at most cap[v] chosen edges at v' (every edge of h has exactly one endpoint in cap, h bipartite).
    Returns a spanning tree meeting the caps, or None."""
    edges = [tuple(e) for e in h.edges()]
    side = [a if a in cap else b for a, b in edges]
    nodes = list(h)
    chosen = set()

    def forest_ok(sel):
        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges[i] for i in sel)
        return nx.is_forest(g)

    def load(sel):
        return Counter(side[i] for i in sel)

    while True:
        ld = load(chosen)
        outside = [i for i in range(len(edges)) if i not in chosen]
        X1 = {i for i in outside if forest_ok(chosen | {i})}
        X2 = {i for i in outside if ld[side[i]] < cap[side[i]]}
        # exchange graph
        adj = defaultdict(list)
        for y in chosen:
            for x in outside:
                if forest_ok((chosen - {y}) | {x}):
                    adj[y].append(x)      # M1 exchange: y -> x
                if side[x] == side[y] or ld[side[x]] < cap[side[x]]:
                    adj[x].append(y)      # M2 exchange: x -> y
        # BFS from X1 to X2
        prev = {x: None for x in X1}
        queue = list(X1)
        end = None
        while queue:
            u = queue.pop(0)
            if u in X2:
                end = u
                break
            for w in adj[u]:
                if w not in prev:
                    prev[w] = u
                    queue.append(w)
        if end is None:
            break
        path = []
        while end is not None:
            path.append(end)
            end = prev[end]
        chosen ^= set(path)
    if len(chosen) == len(nodes) - 1:
        return [edges[i] for i in chosen]
    return None


def exp_hyperside(max_v=14):
    rec = Counter()
    rows = []
    for meta, inst in rooted_instances(max_v, all_roots_up_to=12):
        pts = {('v', v): inst.H.degree(('v', v)) - (0 if v in inst.R else 1) for v in inst.T}
        blk = {('t', t): (3 if t == inst.outer else 2) for t in inst.black}
        g_ok = spanning_tree_with_caps(inst.H, pts) is not None
        f_ok = spanning_tree_with_caps(inst.H, blk) is not None
        tm = inst.flow_pair() is not None  # tree matching exists iff a pair exists (barnette_trees Thm 1.2)
        rec[f'tree={tm} pointside={g_ok} blackside={f_ok}'] += 1
        rows.append({**meta, 'pair': tm, 'point_side_hypertree': g_ok, 'black_side_hypertree': f_ok})
    return {'counts': dict(rec), 'rows': rows}


EXPERIMENTS['hyperside'] = exp_hyperside



# ---------------------------------------------------------------- fast rainbow-spanning-tree version of the point-side test
def white_spoke_edges(inst):
    """Dual of each spoke (t, x), x nonroot, t in A: the edge joining the two white faces of t at x."""
    out = []
    for t in inst.A:
        for x in inst.faces[t]:
            if x in inst.R:
                continue
            ys = [y for u in inst.faces[t] if u != x
                  for y in (inst.sides[x, u], inst.sides[u, x]) if y in inst.white]
            out.append((ys[0], ys[1], x, t))
    return out


def rainbow_tree(nodes, edges, colour_of):
    """Matroid intersection: graphic matroid on nodes x partition matroid 'one edge per colour'.
    edges: list of (a, b); colour_of: list of colours. Returns max common independent set size."""
    m = len(edges)
    idx = {v: i for i, v in enumerate(nodes)}
    E = [(idx[a], idx[b]) for a, b in edges]

    def is_forest(sel):
        par = list(range(len(nodes)))
        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x
        for i in sel:
            a, b = f(E[i][0]), f(E[i][1])
            if a == b:
                return False
            par[a] = b
        return True

    chosen = set()
    while True:
        used = Counter(colour_of[i] for i in chosen)
        outside = [i for i in range(m) if i not in chosen]
        X1 = {i for i in outside if is_forest(chosen | {i})}
        X2 = {i for i in outside if used[colour_of[i]] == 0}
        adj = defaultdict(list)
        for y in chosen:
            rest = chosen - {y}
            for x in outside:
                if x not in X1 and is_forest(rest | {x}):
                    adj[y].append(x)
                if colour_of[x] == colour_of[y]:
                    adj[x].append(y)
        prev = {x: None for x in X1}
        queue, end = list(X1), None
        while queue:
            u = queue.pop(0)
            if u in X2:
                end = u
                break
            for w in adj[u]:
                if w not in prev:
                    prev[w] = u
                    queue.append(w)
        if end is None:
            return chosen
        path = []
        while end is not None:
            path.append(end)
            end = prev[end]
        chosen ^= set(path)


def exp_rainbow(max_v=14, all_roots_up_to=12):
    """Point side: one spoke per nonroot point (colour = point) whose white duals form a spanning tree.
    Black side: one spoke per bounded black face (colour = face). Compare with existence of a pair."""
    rec = Counter()
    rows = []
    for meta, inst in rooted_instances(max_v, all_roots_up_to=all_roots_up_to):
        es = white_spoke_edges(inst)
        edges = [(a, b) for a, b, x, t in es]
        pt = rainbow_tree(inst.white, edges, [x for a, b, x, t in es])
        bl = rainbow_tree(inst.white, edges, [t for a, b, x, t in es])
        g_ok = len(pt) == inst.n
        f_ok = len(bl) == inst.n
        pair = inst.flow_pair() is not None
        key = f'pair={pair} point_side={g_ok} black_side={f_ok}'
        rec[key] += 1
        rows.append({**meta, 'pair': pair, 'point_side': g_ok, 'black_side': f_ok,
                     'separating_triangles': len(separating_triangles(inst))})
    return {'counts': dict(rec), 'rows': rows}


EXPERIMENTS['rainbow'] = exp_rainbow



# ---------------------------------------------------------------- exchange walk among point-rainbow trees
def exp_exchange(max_v=14, restarts=20, steps=400, seed=7):
    """Start from a point-rainbow spanning tree (one deleted spoke per nonroot point, duals a white tree).
    Same-colour single exchanges keep the point side. Minimise black excess sum_t |#deleted spokes at t - 1|
    by a randomised descent that accepts equal moves. Also: is the exchange graph connected (small V)?"""
    rnd = random.Random(seed)
    rec = Counter()
    for meta, inst in rooted_instances(max_v, all_roots_up_to=10):
        if inst.flow_pair() is None:
            continue
        es = white_spoke_edges(inst)
        bycol = defaultdict(list)
        for i, (a, b, x, t) in enumerate(es):
            bycol[x].append(i)
        start = rainbow_tree(inst.white, [(a, b) for a, b, x, t in es], [x for a, b, x, t in es])
        def is_tree(sel):
            g = nx.Graph()
            g.add_nodes_from(inst.white)
            g.add_edges_from((es[i][0], es[i][1]) for i in sel)
            return nx.is_tree(g)
        def excess(sel):
            cnt = Counter(es[i][3] for i in sel)
            return sum(abs(cnt[t] - 1) for t in inst.A)
        best = None
        for _ in range(restarts):
            cur = set(start)
            e = excess(cur)
            for _ in range(steps):
                if e == 0:
                    break
                i = rnd.choice(sorted(cur))
                j = rnd.choice(bycol[es[i][2]])
                if j == i:
                    continue
                new = (cur - {i}) | {j}
                if not is_tree(new):
                    continue
                ne = excess(new)
                if ne <= e:
                    cur, e = new, ne
            best = e if best is None else min(best, e)
            if e == 0:
                break
        rec['instances'] += 1
        rec['reached_tree_matching'] += best == 0
    return dict(rec)


EXPERIMENTS['exchange'] = exp_exchange


if __name__ == '__main__':
    main()
