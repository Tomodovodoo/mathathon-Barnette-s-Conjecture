"""Stage 1 (constructed families and random graphs).

  python src/run_large.py families [workers]
  python src/run_large.py random [workers]
  python src/run_large.py deep [workers]

families  the constructed families of families.py; up to six faces t0 per
          graph (one per orbit, chosen at random), the stored t0 for the trap
          chains.
random    the two random ensembles at the sizes of SIZES; RANDOM_T0 faces t0
          per graph.
deep      exact numbers of good states for a subsample of the random graphs
          with 82 and 102 vertices, with a larger budget.

Results go to raw/large/, one file per block of graphs; blocks that are
already there are skipped.
"""
import pickle
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import families                                               # noqa: E402
import fb                                                     # noqa: E402
import measure                                                # noqa: E402

SEED = 20261115
RAW = ROOT / 'raw' / 'large'

# number of vertices V of T: (graphs per ensemble, independent chains)
SIZES = {20: (300, 12), 22: (300, 12), 26: (300, 12), 30: (300, 12), 34: (300, 12), 40: (300, 12),
         46: (300, 12), 52: (300, 12), 60: (300, 12), 70: (200, 10), 82: (200, 10), 102: (200, 10),
         127: (200, 10), 152: (200, 10), 202: (100, 10), 252: (100, 10), 302: (100, 10),
         402: (50, 10), 502: (50, 10), 752: (24, 8), 1002: (24, 8)}
RANDOM_T0 = 4


def config(nfaces, source):
    cfg = measure.Config(
        good_budget=3 * 10**7, search_budget=5 * 10**6, move_budget=10**7,
        large_n=81, good_budget_large=10**6, search_budget_large=2 * 10**6,
        max_instances=RANDOM_T0 if source.startswith('random') else 6,
        uniform=1000, sis_max_n=200)
    if nfaces > 600:
        cfg.max_instances = min(cfg.max_instances, 3)
    return cfg


def block(task):
    name, items = task
    out = RAW / f'{name}.npz'
    if out.exists():
        return name, 0, 0, 0.0
    start = time.time()
    grows, irows = [], []
    for gid, source, params, F, t0 in items:
        g, r = measure.measure_graph(F, gid, source, params, config(len(F), source), SEED, t0)
        grows.append(g)
        irows.append(r)
    RAW.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix('.part.npz')
    np.savez_compressed(tmp, graphs=np.array(grows, dtype=measure.GRAPH_DTYPE), inst=np.concatenate(irows))
    tmp.replace(out)
    return name, len(grows), sum(map(len, irows)), time.time() - start


def sample(task):
    kind, V, count, chains = task
    out = RAW / 'graphs' / f'random{3 + kind}_V{V}.pkl'
    if not out.exists():
        res = families.random_graphs(kind, V, count, chains, SEED + 1000 * V + kind)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(pickle.dumps(res))
    return task


def run(tasks, workers):
    start = time.time()
    ng = ni = 0
    tasks.sort(key=lambda t: -sum(len(item[3]) ** 2 for item in t[1]))
    with Pool(workers) as pool:
        for k, (name, g, i, sec) in enumerate(pool.imap_unordered(block, tasks), 1):
            ng += g
            ni += i
            if k % 20 == 0 or k == len(tasks):
                print(f'{k}/{len(tasks)} blocks, {ng} graphs, {ni} instances, {time.time() - start:.0f} s',
                      flush=True)


def blocks(prefix, items, size):
    """Blocks of about `size` faces in total."""
    out, cur, tot = [], [], 0
    for item in items:
        cur.append(item)
        tot += len(item[3])
        if tot >= size:
            out.append((f'{prefix}_{len(out):04d}', cur))
            cur, tot = [], 0
    if cur:
        out.append((f'{prefix}_{len(out):04d}', cur))
    return out


def main():
    what = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    if what == 'families':
        cache = RAW / 'graphs' / 'families.pkl'
        if not cache.exists():
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(pickle.dumps(families.families()))
        fam = pickle.loads(cache.read_bytes())
        items = [(10**12 + i, source, params, F, t0) for i, (source, params, F, t0) in enumerate(fam)]
        run(blocks('families', items, 1500), workers)
    elif what == 'random':
        tasks = [(kind, V, count, chains) for V, (count, chains) in SIZES.items() for kind in (0, 1)]
        tasks.sort(key=lambda t: -t[1])
        with Pool(workers) as pool:
            for task in pool.imap_unordered(sample, tasks):
                print('sampled', task, flush=True)
        todo = []
        for kind, V, count, chains in tasks:
            res = pickle.loads((RAW / 'graphs' / f'random{3 + kind}_V{V}.pkl').read_bytes())
            items = [((2 + kind) * 10**12 + V * 10**6 + chain * 10**3 + idx, f'random{3 + kind}',
                      f'V={V} chain={chain} sample={idx}', F, None) for chain, idx, F in res]
            todo += blocks(f'random{3 + kind}_V{V}', items, 1500)
        run(todo, workers)
    elif what == 'deep':
        todo = []
        for kind in (0, 1):
            for V in (82, 102):
                res = pickle.loads((RAW / 'graphs' / f'random{3 + kind}_V{V}.pkl').read_bytes())
                todo += [(kind, V, chain, idx, F) for chain, idx, F in res if idx < 3]
        with Pool(workers) as pool:
            rows = pool.map(deep, todo, chunksize=1)
        np.save(RAW / 'deep.npy', np.array(rows, dtype=[('gid', 'i8'), ('t0', 'i4'), ('n', 'i4'),
                ('log10_states', 'f8'), ('good', 'i8'), ('status', 'i1'), ('nodes', 'i8'), ('seconds', 'f4')]))
        print(len(rows), 'instances;', sum(r[5] != 0 for r in rows), 'censored')


def deep(task):
    kind, V, chain, idx, F = task
    gid = (2 + kind) * 10**12 + V * 10**6 + chain * 10**3 + idx
    rng = np.random.default_rng([SEED, gid & 0x7fffffff, gid >> 31])
    t0 = int(rng.integers(len(F)))
    start = time.time()
    e = fb.enumerate_states(F, t0, 1, 3 * 10**9)
    return (gid, t0, len(F) // 2 - 1, measure.log10_states(F, t0), e['good'] if e['status'] != 2 else -1,
            1 if e['status'] == 2 else 0, e['nodes'], time.time() - start)


if __name__ == '__main__':
    main()
