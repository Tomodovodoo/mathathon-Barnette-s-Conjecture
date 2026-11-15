"""Stage 1 (exhaustive part): every Eulerian triangulation of each size.

  python src/run_exhaustive.py VMIN VMAX [workers]

For each number V of vertices of T (N = 2V - 4 vertices of G) plantri -b
generates all Eulerian triangulations up to isomorphism, mirror images
identified, in several parts; each part is measured by one process and stored
as raw/exh/V<V>_<res>_<mod>.npz.  Parts that are already there are skipped, so
an interrupted run resumes.  Every face of T is taken as t0, one per orbit of
the automorphism group.  For V = 23 the search is run in the stored order
only and the walk in the stored orientation only.
"""
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import graphs                                                 # noqa: E402
import measure                                                # noqa: E402

SEED = 20261115
PARTS = {18: 4, 19: 16, 20: 64, 21: 256, 22: 1024, 23: 4096, 24: 8192}


def config(v):
    # With 23 vertices only the stored order and the stored orientation are run.
    return measure.Config(hc_max_faces=44 if v <= 23 else 0, orders=v <= 22, mirror=v <= 22)


def part(task):
    v, res, mod = task
    out = ROOT / 'raw' / 'exh' / f'V{v}_{res:04d}_{mod}.npz'
    if out.exists():
        return task, 0, 0, 0.0
    start = time.time()
    tmp = ROOT / 'build' / f'tmp_{v}_{res}_{mod}.pc'
    cmd = [str(ROOT / 'build' / 'bin' / 'plantri.exe'), '-b', str(v)]
    if mod > 1:
        cmd.append(f'{res}/{mod}')
    subprocess.run(cmd + [str(tmp)], check=True, capture_output=True)
    cfg = config(v)
    grows, irows = [], []
    for idx, rot in enumerate(graphs.read_planar_code(tmp)):
        F = graphs.faces_of_rotation(rot)
        gid = v * 10**10 + res * 10**6 + idx
        g, r = measure.measure_graph(F, gid, 'exhaustive', f'plantri -b {v} #{idx} of {res}/{mod}',
                                     cfg, SEED)
        grows.append(g)
        irows.append(r)
    tmp.unlink()
    G = np.array(grows, dtype=measure.GRAPH_DTYPE)
    R = np.concatenate(irows) if irows else np.zeros(0, dtype=measure.INST_DTYPE)
    out.parent.mkdir(parents=True, exist_ok=True)
    part_file = out.with_suffix('.part.npz')
    np.savez_compressed(part_file, graphs=G, inst=R)
    part_file.replace(out)
    return task, len(G), len(R), time.time() - start


def main():
    vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    tasks = []
    for v in range(vmax, vmin - 1, -1):
        if v == 7:
            continue
        mod = PARTS.get(v, 1)
        tasks += [(v, res, mod) for res in range(mod)]
    start = time.time()
    ng = ni = 0
    with Pool(workers) as pool:
        for k, (task, g, i, sec) in enumerate(pool.imap_unordered(part, tasks), 1):
            ng += g
            ni += i
            if k % 50 == 0 or k == len(tasks):
                print(f'{k}/{len(tasks)} parts, {ng} graphs, {ni} instances, '
                      f'{time.time() - start:.0f} s', flush=True)


if __name__ == '__main__':
    main()
