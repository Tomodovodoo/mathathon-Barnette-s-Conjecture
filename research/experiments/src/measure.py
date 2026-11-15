"""What is measured on a graph and on an instance.

An instance is a triangulation T with a face t0, that is, a cubic graph G with
a vertex t0.  The states, the good states, the pairs, the search and the walk
depend only on t0; the side e0 of t0 enters only when the cycle is built, and
the three sides give three Hamiltonian cycles, each avoiding the dual of one
side.  Faces in the same orbit of the automorphism group give isomorphic
instances, so one face per orbit is measured.
"""
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT.parents[1] / 'workings'))

import fb                                                     # noqa: E402
import graphs                                                 # noqa: E402
import symmetry                                               # noqa: E402
from barnette import is_hamiltonian_cycle                     # noqa: E402

GRAPH_DTYPE = np.dtype([
    ('gid', 'i8'), ('V', 'i4'), ('N', 'i4'), ('aut', 'i4'), ('aut_op', 'i4'), ('type', 'U8'),
    ('degs', 'U160'), ('maxdeg', 'i4'), ('n4', 'i4'), ('nsep', 'i4'), ('sep_diameter', 'i4'),
    ('max_piece_n', 'i4'), ('min_piece_n', 'i4'), ('face_orbits', 'i4'), ('dart_orbits', 'i4'),
    ('hc_status', 'i1'), ('hc_total', 'i8'), ('source', 'U24'), ('params', 'U48')])

INST_DTYPE = np.dtype([
    ('gid', 'i8'), ('t0', 'i4'), ('orbit', 'i4'), ('rd0', 'i4'), ('rd1', 'i4'), ('rd2', 'i4'),
    ('n', 'i4'), ('log10_states', 'f8'), ('states', 'i8'), ('good', 'i8'), ('good_status', 'i1'),
    ('good_nodes', 'i8'), ('has_pair', 'i1'),
    ('pairs', 'i8'), ('pairs_status', 'i1'), ('two_factors', 'i8'), ('m', 'i4'),
    ('two_factors_m', 'i8'), ('max_cycles', 'i4'),
    ('cuts', 'i4'), ('pieces', 'i4'), ('max_piece', 'i4'),
    ('nodes', 'i8'), ('cands', 'i8'), ('st_search', 'i1'), ('t_search', 'f4'),
    ('nodes_bfs', 'i8'), ('st_bfs', 'i1'), ('nodes_rand', 'i8'), ('st_rand', 'i1'),
    ('moves', 'i8'), ('rounds', 'i4'), ('st_walk', 'i1'), ('t_walk', 'f4'),
    ('moves_mirror', 'i8'), ('st_walk_mirror', 'i1'), ('moves_rand', 'i8'), ('st_walk_rand', 'i1'),
    ('h0', 'i8'), ('h1', 'i8'), ('h2', 'i8'),
    ('sis_mean', 'f8'), ('sis_se', 'f8'), ('sis_n', 'i4'), ('uni_good', 'i4'), ('uni_n', 'i4'),
    ('uni_excess', 'f8'),
    ('cycles_ok', 'i1'), ('cycles_bad', 'i1'), ('error', 'i2')])

# Status codes of a run: 0 finished, 1 the budget ran out (censored), -1 not
# run, other negative values are errors of the algorithm.


class Config:
    """Budgets and limits of a run."""
    good_budget = 2 * 10**7          # nodes for counting the good states
    search_budget = 2 * 10**7        # nodes for the search for the first good state
    move_budget = 10**6              # moves of the exchange walk
    enumerate_max_states = 200_000   # enumerate all states up to this number (check of det)
    pairs_max_states = 3000          # enumerate the pairs up to this number of states
    pairs_budget = 5 * 10**6
    hc_max_faces = 44                # count the Hamiltonian cycles of G up to this N
    hc_budget = 5 * 10**7
    max_instances = None             # faces t0 per graph (None: one per orbit)
    symmetry_max_vertices = 700      # above this the automorphism group is not computed
    large_n = 10**9                  # from this n on the next two budgets apply
    good_budget_large = 10**6
    search_budget_large = 2 * 10**6
    orders = True                    # also search in breadth-first and random order, and walk in random order
    mirror = True                    # also walk in the mirror image
    sis = 0                          # importance-sampling draws when the count is censored
    sis_max_n = 600
    uniform = 0                      # uniform draws (0: none)
    reference_check = True           # test every cycle with the reference is_hamiltonian_cycle

    def __init__(self, **kw):
        for k, v in kw.items():
            if not hasattr(Config, k):
                raise AttributeError(k)
            setattr(self, k, v)


def log10_states(F, t0):
    """log10 of the number of states |det K| from a sparse LU factorisation."""
    from scipy.sparse import csc_matrix
    from scipy.sparse.linalg import splu
    F = np.asarray(F)
    nf = len(F)
    black = two_colouring(F, t0)
    A = [f for f in range(nf) if black[f] and f != t0]
    roots = set(F[t0].tolist())
    xi = {}
    for v in sorted(set(F.ravel().tolist())):
        if v not in roots:
            xi[v] = len(xi)
    rows, cols = [], []
    for i, f in enumerate(A):
        for v in F[f].tolist():
            if v in xi:
                rows.append(i)
                cols.append(xi[v])
    n = len(A)
    K = csc_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    try:
        lu = splu(K)
    except RuntimeError:
        return float('-inf')
    d = np.abs(lu.U.diagonal())
    if np.any(d < 1e-9):
        return float('-inf')
    return float(np.sum(np.log10(d)))


def two_colouring(F, t0):
    """Boolean array: the faces with the colour of t0."""
    F = np.asarray(F)
    left = {}
    for f, (a, b, c) in enumerate(F.tolist()):
        left[a, b] = f
        left[b, c] = f
        left[c, a] = f
    black = np.zeros(len(F), dtype=bool)
    seen = {t0}
    black[t0] = True
    stack = [t0]
    while stack:
        f = stack.pop()
        a, b, c = F[f].tolist()
        for d in ((b, a), (c, b), (a, c)):
            g = left[d]
            if g not in seen:
                seen.add(g)
                black[g] = not black[f]
                stack.append(g)
    return black


def bfs_order(F, t0):
    """F with its faces in breadth-first order from t0 (which comes first)."""
    F = np.asarray(F)
    left = {}
    for f, (a, b, c) in enumerate(F.tolist()):
        left[a, b] = f
        left[b, c] = f
        left[c, a] = f
    order, seen = [t0], {t0}
    for f in order:
        a, b, c = F[f].tolist()
        for d in ((b, a), (c, b), (a, c)):
            g = left[d]
            if g not in seen:
                seen.add(g)
                order.append(g)
    return np.ascontiguousarray(F[order]), 0, order


def random_order(F, t0, rng):
    """F with its faces in random order and every triple rotated at random."""
    F = np.asarray(F)
    perm = rng.permutation(len(F))
    G = F[perm]
    shift = rng.integers(0, 3, size=len(F))
    G = np.stack([G[np.arange(len(F)), (shift + j) % 3] for j in range(3)], axis=1)
    return np.ascontiguousarray(G.astype(np.int32)), int(np.nonzero(perm == t0)[0][0]), perm.tolist()


def dual_graph(F):
    import networkx as nx
    left = {}
    for f, (a, b, c) in enumerate(np.asarray(F).tolist()):
        left[a, b] = f
        left[b, c] = f
        left[c, a] = f
    return nx.Graph((f, left[w, v]) for (v, w), f in left.items()), left


def describe_graph(F, gid, source, params, cfg):
    """The row of the graph table, the orbit representatives of the faces with
    the sizes of their orbits, and the counts of Hamiltonian cycles.  For a
    graph with more than cfg.symmetry_max_vertices faces the group is not
    computed (aut = 0) and every face counts as its own orbit."""
    F = np.ascontiguousarray(F, dtype=np.int32)
    row = np.zeros(1, dtype=GRAPH_DTYPE)[0]
    if int(F.max()) + 1 <= cfg.symmetry_max_vertices:
        c = symmetry.describe(F)
    else:
        c = {'order': 0, 'order_op': 0, 'type': '', 'face_orbit': np.arange(len(F)),
             'dart_orbit': np.arange(3 * len(F))}
    deg = np.bincount(F.ravel())
    sizes, counts = np.unique(deg, return_counts=True)
    sep = fb.sep_structure(F)
    row['gid'], row['V'], row['N'] = gid, int(F.max()) + 1, len(F)
    row['aut'], row['aut_op'], row['type'] = c['order'], c['order_op'], c['type']
    row['degs'] = ' '.join(f'{s}^{k}' for s, k in zip(sizes.tolist(), counts.tolist()))
    row['maxdeg'], row['n4'] = int(deg.max()), int(np.sum(deg == 4))
    row['nsep'], row['sep_diameter'] = sep['nsep'], sep['sep_diameter']
    row['max_piece_n'], row['min_piece_n'] = sep['max_piece_n'], sep['min_piece_n']
    reps, orbit_sizes = np.unique(c['face_orbit'], return_counts=True)
    row['face_orbits'] = len(reps)
    row['dart_orbits'] = len(np.unique(c['dart_orbit']))
    row['source'], row['params'] = source, params
    avoid = None
    row['hc_status'], row['hc_total'] = -1, -1
    if len(F) <= cfg.hc_max_faces:
        status, total, avoid = fb.hamiltonian_cycles(F, cfg.hc_budget)
        row['hc_status'], row['hc_total'] = status, total if status == 0 else -1
        if status != 0:
            avoid = None
    return row, reps, orbit_sizes, avoid, deg


def measure_instance(F, t0, gid, orbit, deg, avoid, G, left, cfg, rng):
    """One row of the instance table."""
    F = np.ascontiguousarray(F, dtype=np.int32)
    nf = len(F)
    n = nf // 2 - 1
    r = np.zeros(1, dtype=INST_DTYPE)[0]
    r['gid'], r['t0'], r['orbit'], r['n'] = gid, t0, orbit, n
    r['rd0'], r['rd1'], r['rd2'] = sorted(int(deg[v]) for v in F[t0])
    for name in ('states', 'good', 'pairs', 'two_factors', 'm', 'two_factors_m', 'max_cycles',
                 'nodes_bfs', 'nodes_rand', 'moves_mirror', 'moves_rand', 'h0', 'h1', 'h2'):
        r[name] = -1
    for name in ('good_status', 'pairs_status', 'st_bfs', 'st_rand', 'st_walk_mirror', 'st_walk_rand'):
        r[name] = -1
    r['sis_mean'] = r['sis_se'] = r['uni_excess'] = np.nan

    # the number of states
    if n <= 79:
        M = fb.states_det(F, t0)
        r['states'] = M
        r['log10_states'] = np.log10(M) if M else -np.inf
    else:
        M = None
        r['log10_states'] = log10_states(F, t0)
    has_states = np.isfinite(r['log10_states'])

    # the good states, by the pruned search
    large = n >= cfg.large_n
    search_budget = cfg.search_budget_large if large else cfg.search_budget
    e = fb.enumerate_states(F, t0, 1, cfg.good_budget_large if large else cfg.good_budget)
    r['good_status'] = 1 if e['status'] == 2 else 0
    r['good'] = e['good'] if e['status'] != 2 else -1
    r['good_nodes'] = e['nodes']
    if M is not None and M <= cfg.enumerate_max_states:
        e0 = fb.enumerate_states(F, t0, 0)
        if e0['states'] != M or (r['good'] >= 0 and e0['good'] != r['good']):
            r['error'] |= 1                         # enumeration against determinant
    pair = fb.first_pair(F, t0)
    r['has_pair'] = pair is not None
    if (pair is None) != (r['good'] == 0) and r['good'] >= 0:
        r['error'] |= 2                             # a pair without good state, or the converse
    if M is not None and M <= cfg.pairs_max_states:
        p = fb.pairs(F, t0, cfg.pairs_budget)
        r['pairs_status'] = 1 if p['status'] == 2 else 0
        if p['status'] != 2:
            r['pairs'], r['two_factors'], r['m'] = p['pairs'], p['two_factors'], p['m']
            r['two_factors_m'], r['max_cycles'] = p['two_factors_m'], p['max_cycles']
            if r['good'] >= 0 and p['pairs_good'] != r['good']:
                r['error'] |= 4                     # good states against pairs with good second state

    # the algorithm with the search, and with the walk
    ok = bad = 0

    def verify(sol, Fx, tx, back=None):
        # Fx: the triangulation as passed to the solver; back[i]: the face of F
        # that is the face i of Fx.  Every cycle is tested in C on Fx and with
        # the reference is_hamiltonian_cycle on the dual graph G of F.
        nonlocal ok, bad
        for k in range(3):
            cyc = sol['cycles'][k]
            good = cyc is not None and fb.check_cycle(Fx, cyc, tx, k)
            if good and cfg.reference_check:
                a, b = int(Fx[tx][k]), int(Fx[tx][(k + 1) % 3])
                other = left[b, a] if left[a, b] == t0 else left[a, b]
                if back is not None:
                    cyc = [back[f] for f in cyc]
                good = is_hamiltonian_cycle(G, cyc, avoid=(t0, other))
            ok += good
            bad += not good

    start = time.perf_counter()
    sol = fb.solve(F, t0, 0, search_budget, cfg.move_budget)
    r['t_search'] = time.perf_counter() - start
    r['st_search'], r['nodes'], r['cands'] = sol['status'], sol['nodes'], sol['cands']
    r['cuts'], r['pieces'], r['max_piece'] = sol['cuts'], sol['pieces'], sol['max_piece_n']
    if sol['status'] == 0:
        verify(sol, F, t0)
    elif sol['status'] < 0:
        r['error'] |= 8
    start = time.perf_counter()
    sol = fb.solve(F, t0, 1, cfg.search_budget, cfg.move_budget)
    r['t_walk'] = time.perf_counter() - start
    r['st_walk'], r['moves'], r['rounds'] = sol['status'], sol['moves'], sol['rounds']
    if sol['status'] == 0:
        verify(sol, F, t0)
    elif sol['status'] < 0:
        r['error'] |= 16
    if cfg.mirror:
        Fm = graphs.mirror(F)
        sol = fb.solve(Fm, t0, 1, cfg.search_budget, cfg.move_budget)
        r['st_walk_mirror'], r['moves_mirror'] = sol['status'], sol['moves']
        if sol['status'] == 0:
            verify(sol, Fm, t0)
        elif sol['status'] < 0:
            r['error'] |= 16
    if cfg.orders:
        Fb, tb, back = bfs_order(F, t0)
        sol = fb.solve(Fb, tb, 0, search_budget, cfg.move_budget)
        r['st_bfs'], r['nodes_bfs'] = sol['status'], sol['nodes']
        if sol['status'] == 0:
            verify(sol, Fb, tb, back)
        elif sol['status'] < 0:
            r['error'] |= 8
        Fr, tr, back = random_order(F, t0, rng)
        sol = fb.solve(Fr, tr, 0, search_budget, cfg.move_budget)
        r['st_rand'], r['nodes_rand'] = sol['status'], sol['nodes']
        if sol['status'] == 0:
            verify(sol, Fr, tr, back)
        elif sol['status'] < 0:
            r['error'] |= 8
        sol = fb.solve(Fr, tr, 1, cfg.search_budget, cfg.move_budget)
        r['st_walk_rand'], r['moves_rand'] = sol['status'], sol['moves']
        if sol['status'] == 0:
            verify(sol, Fr, tr, back)
        elif sol['status'] < 0:
            r['error'] |= 16
    r['cycles_ok'], r['cycles_bad'] = ok, bad
    if bad:
        r['error'] |= 32

    if avoid is not None:
        r['h0'], r['h1'], r['h2'] = (int(x) for x in avoid[t0])
        if r['good'] >= 0 and r['good'] > min(avoid[t0]):
            r['error'] |= 64                        # more good states than cycles avoiding e

    # random states
    want_sis = cfg.sis if (r['good_status'] == 1 and has_states and n <= cfg.sis_max_n) else 0
    want_uni = cfg.uniform if (has_states and n <= cfg.sis_max_n) else 0
    if want_sis or want_uni:
        s = fb.sample(F, t0, want_uni, want_sis, seed=int(rng.integers(1, 2**62)))
        if s is not None:
            if want_sis:
                r['sis_mean'], r['sis_n'] = s['sis_mean'], want_sis
                r['sis_se'] = np.sqrt(max(s['sis_meansq'] - s['sis_mean'] ** 2, 0) / want_sis)
            if want_uni:
                r['uni_good'], r['uni_n'] = int(s['uniform_good']), want_uni
                r['uni_excess'] = s['uniform_excess'] / want_uni
            if s['max_dev'] > 1e-6:
                r['error'] |= 128                   # the conditional probabilities do not add up
    return r


def measure_graph(F, gid, source, params, cfg, seed, t0=None):
    """All rows for one graph: (graph row, array of instance rows).  If t0 is
    given, only this face is taken."""
    F = np.ascontiguousarray(F, dtype=np.int32)
    rng = np.random.default_rng([seed, gid & 0x7fffffff, gid >> 31])
    grow, reps, orbit_sizes, avoid, deg = describe_graph(F, gid, source, params, cfg)
    if t0 is not None:
        reps, orbit_sizes = np.array([t0]), np.array([1])
    elif cfg.max_instances is not None and len(reps) > cfg.max_instances:
        pick = np.sort(rng.choice(len(reps), size=cfg.max_instances, replace=False))
        reps, orbit_sizes = reps[pick], orbit_sizes[pick]
    G, left = dual_graph(F)
    rows = np.zeros(len(reps), dtype=INST_DTYPE)
    for i, (t0, orbit) in enumerate(zip(reps.tolist(), orbit_sizes.tolist())):
        rows[i] = measure_instance(F, t0, gid, orbit, deg, avoid, G, left, cfg, rng)
    return grow, rows
