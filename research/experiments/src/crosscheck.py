"""Cross-check of fastbarnette.c against workings/barnette.

  python src/crosscheck.py [max_vertices] [workers]

Every Eulerian triangulation with at most max_vertices vertices (default 14)
is taken with every face as t0, together with the examples of the reference
package, the stored instances of research/instances and some members of the
constructed families.  On each labelled instance the two implementations must
agree on: the states and their number (enumeration and determinant), the good
states, the first good state found by the search and the number of partial
choices and matching tests it takes, the pairs by number of cycles, the
existence of a pair, the corner weights, the exchange walk from a common pair
(moves and final pair), the cut along separating triangles, the three
Hamiltonian cycles, and the number of Hamiltonian cycles of G avoiding each
edge (against a direct enumeration).  The walk from the stored pairs of the
ten trap chains is compared with the numbers of moves stated in
proofs/algorithm/algorithm.md, and the logarithm of the number of states from
a sparse LU factorisation with the exact determinant.  For every triangulation
with at most 45 vertices the number of states is compared, for every face t0,
with the square root of the minor of A + D/2 (README, section on the number
of states).  The result is written to data/crosscheck.json.
"""
import json
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT.parents[1] / 'workings'))

import fb                                                     # noqa: E402
import graphs                                                 # noqa: E402
import barnette                                               # noqa: E402
ref_states = sys.modules['barnette.states']                   # the module, not the function
from barnette import (Triangulation, states, is_good, pairs, is_pair, D_cycles, first_pair,
                      exchange_walk, corner_weights, separating_triangle, pieces, selection,
                      cycle_of_selection, is_hamiltonian_cycle, edge)   # noqa: E402

WALK_CAP = 3000          # moves allowed to the reference walk


class Counting:
    """Counts the calls of the reference matching test and its successes."""

    def __init__(self):
        self.original = ref_states._completable
        self.calls = self.kept = 0

    def __call__(self, faces, options):
        self.calls += 1
        ok = self.original(faces, options)
        self.kept += ok
        return ok

    def __enter__(self):
        ref_states._completable = self
        return self

    def __exit__(self, *args):
        ref_states._completable = self.original


def ref_selection(T):
    """acyclic_selection of the reference package, with the search in place
    of the walk."""
    if first_pair(T) is not None:
        return selection(T, next(states(T, good=True))), 1
    triangle = separating_triangle(T)
    first, second = pieces(T, triangle)
    x, y, z = triangle
    P1, k1 = ref_selection(Triangulation(first, T.t0, T.e0))
    e, = P1 & {edge(x, y), edge(y, z), edge(x, z)}
    P2, k2 = ref_selection(Triangulation(second, ('cap', triangle), e))
    return P1 | P2, k1 + k2


def brute_force_cycles(G):
    """All Hamiltonian cycles of the cubic graph G, as sets of edges."""
    nodes = list(G)
    start, found = nodes[0], []
    path, on = [start], {start}

    def extend():
        v = path[-1]
        if len(path) == len(nodes):
            if G.has_edge(v, start):
                found.append(frozenset(frozenset(e) for e in zip(path, path[1:] + path[:1])))
            return
        for w in G[v]:
            if w not in on:
                path.append(w)
                on.add(w)
                extend()
                path.pop()
                on.remove(w)

    extend()
    return set(found)


def check(args):
    name, F, t0, heavy = args
    F = np.asarray(F, dtype=np.int32)
    fails, done = [], Counter()

    def expect(what, ok):
        done[what] += 1
        if not ok:
            fails.append(f'{name} t0={t0}: {what}')

    T = graphs.to_reference(F, t0, 0)
    A = T.A
    as_list = lambda s: [s[t] for t in A]

    light = len(F) > 40          # more than 22 vertices: no full enumeration
    # states, good states, determinant
    with Counting() as count:
        all_states = [] if light else [as_list(s) for s in states(T)]
    good = [s for s in all_states if is_good(T, dict(zip(A, s)))]
    if not light:
        e0 = fb.enumerate_states(F, t0, 0)
        expect('number of states', e0['states'] == len(all_states))
        expect('determinant', fb.states_det(F, t0) == len(all_states))
        expect('number of good states', e0['good'] == len(good))
        expect('nodes of the full enumeration', e0['nodes'] == count.kept - (len(all_states) > 0))
        expect('tests of the full enumeration', e0['tests'] == max(count.calls - 1, 0))
        with Counting() as count:
            ref_good = [as_list(s) for s in states(T, good=True)]
        e1 = fb.enumerate_states(F, t0, 1)
        expect('good states by the pruned search', e1['good'] == len(good) == len(ref_good))
        expect('nodes of the pruned search', e1['nodes'] == count.kept - (len(all_states) > 0))
        expect('tests of the pruned search', e1['tests'] == max(count.calls - 1, 0))

    # the first good state
    with Counting() as count:
        first = next(states(T, good=True), None)
    e2 = fb.enumerate_states(F, t0, 2)
    if first is None:
        expect('no good state', e2['state'] is None)
    else:
        expect('first good state', e2['state'] == as_list(first))
        expect('nodes to the first good state', e2['nodes'] == count.kept - 1)
        expect('tests to the first good state', e2['tests'] == count.calls - 1)

    # pairs
    if not light and (len(all_states) <= 400 or heavy):
        byc, pairs_good = Counter(), 0
        for r, s in pairs(T):
            byc[len(D_cycles(T, r, s))] += 1
            pairs_good += is_good(T, s)
        p = fb.pairs(F, t0)
        expect('pairs by number of cycles', p['by_cycles'] == dict(byc))
        expect('pairs with good second state', p['pairs_good'] == pairs_good == len(good))
        expect('existence of a pair', (sum(byc.values()) > 0) == (fb.first_pair(F, t0) is not None))
    ref_pair = first_pair(T)
    pair = fb.first_pair(F, t0)
    expect('pair by a flow', (ref_pair is None) == (pair is None))

    # weights and the exchange walk, in both mirror images
    kappa = corner_weights(T)
    expect('corner weights',
           fb.corner_weights(F, t0).tolist() == [[kappa[t, v] for v in T.faces[t]] for t in A])
    if pair is not None:
        r, s = (dict(zip(A, x)) for x in pair)
        expect('the pair is a pair', is_pair(T, r, s) and sorted(pair[0]) == sorted(pair[1]) == sorted(T.X))
        for Fm, Tm in ((F, T), (graphs.mirror(F), graphs.to_reference(graphs.mirror(F), t0, 0))):
            ref = exchange_walk(Tm, r, s, max_moves=WALK_CAP)
            mine = fb.walk(Fm, t0, pair[0], pair[1], WALK_CAP)
            if ref is None:
                expect('walk stopped at the cap', mine['status'] == 1 and mine['moves'] >= WALK_CAP)
            else:
                expect('walk: moves', mine['status'] == 0 and mine['moves'] == ref[1])
                expect('walk: final pair', mine['r'] == as_list(ref[0][0]) and mine['s'] == as_list(ref[0][1]))
                expect('walk: final state good', is_good(Tm, ref[0][1]))

    # the whole algorithm and the cycles
    G = T.primal()
    for method in (0, 1):
        sol = fb.solve(F, t0, method, move_budget=10**6)
        expect('solve: status', sol['status'] == 0)
        for k in range(3):
            f = T.faces[t0]
            avoid = (t0, T.left[f[(k + 1) % 3], f[k]])
            cyc = sol['cycles'][k]
            expect('solve: Hamiltonian cycle (reference test)',
                   cyc is not None and is_hamiltonian_cycle(G, cyc, avoid=avoid))
            expect('solve: Hamiltonian cycle (C test)', cyc is not None and fb.check_cycle(F, cyc, t0, k))
            if method == 0:
                Tk = graphs.to_reference(F, t0, k)
                P, npieces = ref_selection(Tk)
                expect('solve: same cycle as the reference', cyc == cycle_of_selection(Tk, P))
                expect('solve: number of pieces', sol['pieces'] == npieces)

    # Hamiltonian cycles of G
    if len(F) <= 26 and t0 == 0:
        cycles = brute_force_cycles(G)
        status, total, avoid = fb.hamiltonian_cycles(F)
        expect('number of Hamiltonian cycles', status == 0 and total == len(cycles))
        ok = True
        for f in range(len(F)):
            for k in range(3):
                g = T.left[int(F[f][(k + 1) % 3]), int(F[f][k])]
                ok &= avoid[f][k] == sum(frozenset((f, g)) not in c for c in cycles)
        expect('Hamiltonian cycles avoiding each edge', ok)
        expect('good states <= cycles avoiding e', all(len(good) <= avoid[t0][k] for k in range(3)))
    return fails, done


def instances(max_v):
    from barnette import examples
    out = []
    for v in range(6, max_v + 1):
        path = ROOT / 'build' / f'xcheck_{v}.pc'
        import subprocess
        subprocess.run([str(ROOT / 'build' / 'bin' / 'plantri.exe'), '-b', str(v), str(path)],
                       check=True, capture_output=True)
        for i, rot in enumerate(graphs.read_planar_code(path)):
            F = graphs.faces_of_rotation(rot)
            out += [(f'plantri-{v}-{i}', F, t0, False) for t0 in range(len(F))]
        path.unlink()
    named = {
        'cube': graphs.dual_of_cubic_graph(examples.cube()),
        'prism-6': graphs.dual_of_cubic_graph(examples.prism(6)),
        'prism-8': graphs.dual_of_cubic_graph(examples.prism(8)),
        'truncated-octahedron': graphs.dual_of_cubic_graph(examples.truncated_octahedron()),
        'nanotube-3': graphs.dual_of_cubic_graph(examples.nanotube(3)),
        'two-cubes': graphs.dual_of_cubic_graph(examples.two_cubes()),
        'bipyramid-5': graphs.bipyramid(5),
        'tube-2-3': graphs.tube(2, 3), 'tube-3-2': graphs.tube(3, 2), 'tube-4-2': graphs.tube(4, 2),
        'octahedral-2-0': graphs.octahedral(2, 0), 'octahedral-2-1': graphs.octahedral(2, 1),
        'stacked-chain-3': graphs.stacked_octahedra(3), 'stacked-all-2': graphs.stacked_octahedra(2, 'all'),
        'split-bipyramid-8': graphs.split_bipyramid(8),
        'leapfrog-bipyramid-3': graphs.leapfrog(graphs.bipyramid(3)),
    }
    for name, F in named.items():
        assert graphs.is_eulerian_triangulation(F), name
        step = max(1, len(F) // 12)
        out += [(name, F, t0, False) for t0 in range(0, len(F), step)]
    for T, name in ((examples.running_example(), 'running'), (examples.eight_vertex_example(), 'eight'),
                    (examples.trap(), 'trap')):
        F = np.array([T.faces[i] for i in range(len(T.faces))], dtype=np.int32)
        out.append((name, F, T.t0, True))
    for k in range(1, 5):
        F, t0, _ = graphs.trap_chain(k)
        out.append((f'trap-chain-{k}', F, t0, False))
    inst = ROOT.parents[0] / 'instances'
    for path in sorted(inst.glob('*.json')):
        d = json.loads(path.read_text())
        if 'faces' in d and not path.name.startswith('trap-chain'):
            out.append((path.stem, np.array(d['faces'], dtype=np.int32), d['faces'].index(d['t0']), False))
    return out


def trap_chains():
    """The numbers of moves stated in proofs/algorithm/algorithm.md for the
    walk from the stored pair of trap-chain-k, and 3 in the mirror image."""
    stated = [0, 3, 24, 113, 562, 2811, 14060, 70309, 351558, 1757807]
    found, mirrored = [], []
    for k in range(1, 11):
        F, t0, d = graphs.trap_chain(k)
        r, s = d['pair']
        found.append(fb.walk(F, t0, r, s)['moves'])
        mirrored.append(fb.walk(graphs.mirror(F), t0, r, s)['moves'])
    return stated, found, mirrored


def log_determinants():
    """The logarithm of the number of states from the sparse LU factorisation
    (measure.log10_states, used when n > 79) against the exact determinant,
    on triangulations with 20 <= n <= 79 and every fourth face as t0.
    Returns the number of instances and the largest difference of log10."""
    import families
    import measure
    tris = [graphs.octahedral(k, l) for k, l in ((2, 2), (3, 0), (3, 1), (3, 2), (4, 0))]
    tris += [graphs.tube(k, m) for k, m in ((2, 9), (3, 5), (4, 4), (5, 3), (8, 2))]
    tris += [graphs.trap_chain(k)[0] for k in (3, 4, 5, 6)]
    tris += [families.grow(steps, p, seed) for seed, (steps, p) in
             enumerate(((30, 0.0), (36, 0.0), (20, 0.3), (24, 0.5), (34, 0.1), (28, 0.2)))]
    count, worst = 0, 0.0
    for F in tris:
        n = len(F) // 2 - 1
        assert 20 <= n <= 79, n
        for t0 in range(0, len(F), 4):
            M = fb.states_det(F, t0)
            approx = measure.log10_states(F, t0)
            if M == 0:
                assert approx == float('-inf')
                continue
            count += 1
            worst = max(worst, abs(approx - np.log10(float(M))))
    return count, worst


def integer_determinant(rows):
    """Exact determinant of an integer matrix by fraction-free elimination."""
    A = [list(map(int, r)) for r in rows]
    n, prev, sign = len(A), 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if A[i][k]), None)
            if swap is None:
                return 0
            A[k], A[swap] = A[swap], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[-1][-1]


def states_by_the_signless_laplacian(todo):
    """For every triangulation of the list: the number of states is the same
    for every face t0, and its square is the determinant of A + D/2 without
    the rows and columns of two adjacent vertices (A the adjacency matrix of
    T, D the diagonal matrix of the degrees).  Returns the number of
    triangulations and the number of faces t0 compared."""
    seen, graphs_done, faces_done = set(), 0, 0
    for name, F, _, _ in todo:
        if name in seen:
            continue
        seen.add(name)
        F = np.asarray(F)
        V = int(F.max()) + 1
        if V > 45:
            continue
        Q = np.zeros((V, V), dtype=np.int64)
        for x, y, z in F.tolist():
            for p, q in ((x, y), (y, z), (z, x)):
                Q[p, q] = Q[q, p] = 2
                Q[p, p] += 1
        keep = [v for v in range(V) if v not in (int(F[0][0]), int(F[0][1]))]
        det = integer_determinant(Q[np.ix_(keep, keep)].tolist())
        for t0 in range(len(F)):
            assert det == 2 ** (V - 2) * fb.states_det(F, t0) ** 2, (name, t0)
            faces_done += 1
        graphs_done += 1
    return graphs_done, faces_done


def main():
    max_v = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    todo = instances(max_v)
    start = time.time()
    fails, done = [], Counter()
    stated, found, mirrored = trap_chains()
    done['trap chains: moves stated in algorithm.md'] = 10
    if found != stated or mirrored != [3] * 10:
        fails.append(f'trap chains: {found} and {mirrored} in the mirror image, stated {stated}')
    count, worst = log_determinants()
    done['log-determinant by sparse LU against the exact determinant'] = count
    if worst > 1e-9:
        fails.append(f'log-determinant: difference {worst}')
    ngraphs, nfaces = states_by_the_signless_laplacian(todo)
    done['number of states against the minor of A + D/2, every face as t0'] = nfaces
    with Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 20) as pool:
        for f, d in pool.imap_unordered(check, todo, chunksize=8):
            fails += f
            done.update(d)
    result = {'max_vertices_exhaustive': max_v, 'instances': len(todo),
              'checks': dict(sorted(done.items())), 'total_checks': sum(done.values()),
              'largest_difference_of_log10_states': worst,
              'failures': fails, 'seconds': round(time.time() - start, 1)}
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data' / 'crosscheck.json').write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps(result, indent=1))
    if fails:
        raise SystemExit(f'{len(fails)} FAILURES')


if __name__ == '__main__':
    main()
