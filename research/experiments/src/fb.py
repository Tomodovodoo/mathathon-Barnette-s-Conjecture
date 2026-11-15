"""ctypes interface to fastbarnette.c.

A triangulation is a numpy int32 array F of shape (nf, 3): the faces, all
listed counterclockwise.  t0 is the index of a face.  See fastbarnette.c for
the conventions, which are those of workings/barnette.
"""
import ctypes as C
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DLL = ROOT / 'build' / 'bin' / 'fastbarnette.dll'

_lib = None
I32 = np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS')
I64 = np.ctypeslib.ndpointer(dtype=np.int64, flags='C_CONTIGUOUS')
F64 = np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS')


def lib():
    global _lib
    if _lib is None:
        if not DLL.exists():
            raise RuntimeError(f'{DLL} is missing: run  python src/build.py')
        L = C.CDLL(str(DLL))
        i, q = C.c_int, C.c_longlong
        L.bx_enumerate.argtypes = [I32, i, i, i, i, q, I64, C.c_void_p]
        L.bx_states_det.argtypes = [I32, i, i, i]
        L.bx_states_det.restype = q
        L.bx_pairs.argtypes = [I32, i, i, i, q, I64, I64]
        L.bx_first_pair.argtypes = [I32, i, i, i, I32, I32]
        L.bx_walk.argtypes = [I32, i, i, i, I32, I32, q, I64]
        L.bx_corner_weights.argtypes = [I32, i, i, i, I32]
        L.bx_check_cycle.argtypes = [I32, i, i, I32, i, i]
        L.bx_solve.argtypes = [I32, i, i, i, i, q, q, I32, I32, I64, I32, I64, i]
        L.bx_cycle_of_state.argtypes = [I32, i, i, i, i, I32, I32]
        L.bx_separating_triangles.argtypes = [I32, i, i, I32, i]
        L.bx_hamiltonian_cycles.argtypes = [I32, i, i, q, I64, I64]
        L.bx_canon.argtypes = [I32, i, i, I32, I64, I32, I32, i, I32, I32]
        L.bx_sample.argtypes = [I32, i, i, i, i, i, C.c_ulonglong, F64]
        L.bx_mcmc.argtypes = [I32, i, i, i, i, i, C.c_double, q, q, i, C.c_ulonglong, I32, I32, I64]
        L.bx_mcmc.restype = i
        L.bx_sep_structure.argtypes = [I32, i, i, I32]
        _lib = L
    return _lib


def _prep(F):
    F = np.ascontiguousarray(F, dtype=np.int32)
    return F, len(F), int(F.max()) + 1


def enumerate_states(F, t0, mode=0, budget=10**9):
    """mode 0: all states; 1: the good states; 2: stop at the first good state.

    Returns a dict with status (0 complete, 1 stopped at the first good state,
    2 budget, 3 no state), states, good, nodes, cands, tests and, for mode 2,
    the state found (list of corners in the order of A)."""
    F, nf, nv = _prep(F)
    out = np.zeros(6, dtype=np.int64)
    first = np.full(nf // 2, -1, dtype=np.int32)
    rc = lib().bx_enumerate(F, nf, nv, t0, mode, budget, out, first.ctypes.data)
    if rc:
        raise ValueError(f'bx_enumerate: error {rc}')
    res = dict(zip(('status', 'states', 'good', 'nodes', 'cands', 'tests'), map(int, out)))
    if mode == 2:
        res['state'] = first[:nf // 2 - 1].tolist() if res['status'] == 1 else None
    return res


def states_det(F, t0):
    """The number of states, |det K|, exactly; None if n > 79."""
    F, nf, nv = _prep(F)
    d = lib().bx_states_det(F, nf, nv, t0)
    if d == -2:
        raise ValueError('bx_states_det: bad input')
    return None if d == -1 else int(d)


def pairs(F, t0, budget=10**9):
    F, nf, nv = _prep(F)
    out = np.zeros(8, dtype=np.int64)
    byc = np.zeros(nf // 2 + 1, dtype=np.int64)
    rc = lib().bx_pairs(F, nf, nv, t0, budget, out, byc)
    if rc:
        raise ValueError(f'bx_pairs: error {rc}')
    res = dict(zip(('status', 'pairs', 'pairs_good', 'm', 'two_factors', 'two_factors_m',
                    'max_cycles', 'nodes'), map(int, out)))
    res['by_cycles'] = {c: int(k) for c, k in enumerate(byc) if k}
    return res


def first_pair(F, t0):
    """A pair (r, s) as two lists of corners in the order of A, or None."""
    F, nf, nv = _prep(F)
    n = nf // 2 - 1
    r = np.zeros(n + 1, dtype=np.int32)
    s = np.zeros(n + 1, dtype=np.int32)
    ok = lib().bx_first_pair(F, nf, nv, t0, r, s)
    if ok < 0:
        raise ValueError(f'bx_first_pair: error {ok}')
    return (r[:n].tolist(), s[:n].tolist()) if ok else None


def walk(F, t0, r, s, max_moves=-1):
    """Algorithm W from the pair (r, s).  Returns a dict with status (0: the
    second state is good, 1: stopped), moves, rounds, cycles_start,
    cycles_end, r, s."""
    F, nf, nv = _prep(F)
    r = np.array(list(r) + [0], dtype=np.int32)
    s = np.array(list(s) + [0], dtype=np.int32)
    out = np.zeros(5, dtype=np.int64)
    rc = lib().bx_walk(F, nf, nv, t0, r, s, max_moves, out)
    if rc:
        raise ValueError(f'bx_walk: error {rc}')
    res = dict(zip(('status', 'moves', 'rounds', 'cycles_start', 'cycles_end'), map(int, out)))
    res['r'], res['s'] = r[:-1].tolist(), s[:-1].tolist()
    return res


def corner_weights(F, t0):
    F, nf, nv = _prep(F)
    kappa = np.zeros(3 * (nf // 2), dtype=np.int32)
    rc = lib().bx_corner_weights(F, nf, nv, t0, kappa)
    if rc:
        raise ValueError(f'bx_corner_weights: error {rc}')
    return kappa[:3 * (nf // 2 - 1)].reshape(-1, 3)


def solve(F, t0, method=0, node_budget=10**9, move_budget=10**9, piece_cap=64):
    """The whole algorithm.  method 0: search, 1: exchange walk.

    Returns a dict with status (0 done, 1 budget, < 0 error), pieces, cuts,
    max_piece_n, nodes, cands, tests, moves, rounds, piece_n, piece_cost and
    cycles: for each side k of t0 the cycle avoiding its dual (list of faces),
    or None."""
    F, nf, nv = _prep(F)
    cycles = np.zeros(3 * nf, dtype=np.int32)
    ok = np.zeros(3, dtype=np.int32)
    stats = np.zeros(9, dtype=np.int64)
    pn = np.zeros(piece_cap, dtype=np.int32)
    pc = np.zeros(piece_cap, dtype=np.int64)
    rc = lib().bx_solve(F, nf, nv, t0, method, node_budget, move_budget, cycles, ok, stats,
                        pn, pc, piece_cap)
    if rc:
        raise ValueError(f'bx_solve: error {rc}')
    res = dict(zip(('status', 'pieces', 'cuts', 'max_piece_n', 'nodes', 'cands', 'tests',
                    'moves', 'rounds'), map(int, stats)))
    k = min(res['pieces'], piece_cap)
    res['piece_n'], res['piece_cost'] = pn[:k].tolist(), pc[:k].tolist()
    res['cycles'] = [cycles[j * nf:(j + 1) * nf].tolist() if ok[j] else None for j in range(3)]
    return res


def cycle_of_state(F, t0, k, s):
    F, nf, nv = _prep(F)
    cyc = np.zeros(nf, dtype=np.int32)
    s = np.array(list(s) + [0], dtype=np.int32)
    rc = lib().bx_cycle_of_state(F, nf, nv, t0, k, s, cyc)
    return cyc.tolist() if rc == 0 else None


def check_cycle(F, cycle, f0, k0):
    """Whether `cycle` is a Hamiltonian cycle of the dual that does not cross
    the side k0 of the face f0 (an independent check in C)."""
    F, nf, nv = _prep(F)
    return bool(lib().bx_check_cycle(F, nf, nv, np.ascontiguousarray(cycle, dtype=np.int32), f0, k0))


def separating_triangles(F, cap=4096):
    """(number of separating triangles, for each the number of faces on the
    side away from the face 0)."""
    F, nf, nv = _prep(F)
    sizes = np.zeros(cap, dtype=np.int32)
    k = lib().bx_separating_triangles(F, nf, nv, sizes, cap)
    if k < 0:
        raise ValueError('bx_separating_triangles: bad input')
    return k, sizes[:min(k, cap)].tolist()


def hamiltonian_cycles(F, budget=10**9):
    """(status, number of Hamiltonian cycles of the dual G, array avoid of
    shape (nf, 3): the number of them that avoid the dual of each side)."""
    F, nf, nv = _prep(F)
    out = np.zeros(3, dtype=np.int64)
    avoid = np.zeros(3 * nf, dtype=np.int64)
    rc = lib().bx_hamiltonian_cycles(F, nf, nv, budget, out, avoid)
    if rc:
        raise ValueError('bx_hamiltonian_cycles: bad input')
    return int(out[0]), int(out[1]), avoid.reshape(nf, 3)


def canon(F, cap=None):
    """Canonical form and automorphisms of the plane triangulation.

    Returns a dict: code (bytes, equal exactly for isomorphic triangulations,
    mirror images included), order, order_op (orientation-preserving), autos
    (array k x nv of vertex images), aut_info (k x 3: orientation-preserving,
    order, has a fixed vertex/edge/face), face_orbit (nf), dart_orbit (nf x 3)."""
    F, nf, nv = _prep(F)
    if cap is None:
        cap = 12 * nv
    code = np.zeros(nv + 3 * nf, dtype=np.int32)
    info = np.zeros(3, dtype=np.int64)
    autos = np.zeros(cap * nv, dtype=np.int32)
    ainfo = np.zeros(3 * cap, dtype=np.int32)
    fo = np.zeros(nf, dtype=np.int32)
    do = np.zeros(3 * nf, dtype=np.int32)
    rc = lib().bx_canon(F, nf, nv, code, info, autos, ainfo, cap, fo, do)
    if rc:
        raise ValueError(f'bx_canon: error {rc}')
    k = int(info[2])
    return dict(code=code.tobytes(), order=int(info[0]), order_op=int(info[1]),
                autos=autos[:k * nv].reshape(k, nv), aut_info=ainfo[:3 * k].reshape(k, 3),
                face_orbit=fo, dart_orbit=do.reshape(nf, 3))


def sample(F, t0, n_uniform=0, n_sis=0, seed=1):
    """Random states.  Returns a dict: logdet (natural logarithm of the number
    of states), uniform_good, uniform_excess (sum over the uniform draws of
    the number of chosen sides that close a cycle), sis_mean (an unbiased
    estimate of good/states), sis_meansq, sis_nonzero, max_dev, sis_max."""
    F, nf, nv = _prep(F)
    out = np.zeros(8, dtype=np.float64)
    rc = lib().bx_sample(F, nf, nv, t0, n_uniform, n_sis, seed, out)
    if rc == -5:
        return None
    if rc:
        raise ValueError(f'bx_sample: error {rc}')
    return dict(zip(('logdet', 'uniform_good', 'uniform_excess', 'sis_mean', 'sis_meansq',
                     'sis_nonzero', 'max_dev', 'sis_max'), map(float, out)))


def mcmc(F, target, kind, steps, thin, nsamples, seed, headroom=0, gamma=3.5):
    """See fastbarnette.c, bx_mcmc.  Returns (list of face arrays, stats)."""
    F, nf, nv = _prep(F)
    maxf = 2 * target - 4
    out = np.zeros(nsamples * 3 * maxf, dtype=np.int32)
    got = np.zeros(1, dtype=np.int32)
    stats = np.zeros(8, dtype=np.int64)
    rc = lib().bx_mcmc(F, nf, nv, target, kind, headroom, gamma, steps, thin, nsamples, seed, out, got, stats)
    if rc:
        raise ValueError(f'bx_mcmc: error {rc}')
    k = int(got[0])
    return [out[j * 3 * maxf:(j + 1) * 3 * maxf].reshape(maxf, 3).copy() for j in range(k)], stats


def sep_structure(F):
    """Separating triangles of T: a dict with their number, the diameter of
    the tree of pieces, and the largest and smallest n of a piece."""
    F, nf, nv = _prep(F)
    out = np.zeros(4, dtype=np.int32)
    if lib().bx_sep_structure(F, nf, nv, out):
        raise ValueError('bx_sep_structure: bad input')
    return dict(zip(('nsep', 'sep_diameter', 'max_piece_n', 'min_piece_n'), map(int, out)))
