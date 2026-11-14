"""Lengths of the marked (Garsia-Milne) walk of barnette_trees Theorem 5.3, from every pair.

Uses the reference lab read-only (algorithms.marked_walk). For every plantri triangulation with
V vertices, every face as root, every ordered pair as the starting pair, record the number of
involution moves, the normalisation reversals and the restarts, and compare with the distance
to the nearest tree pair in the exchange graph (BFS).
Usage: python gm_lengths.py V [max_instances]   -> one JSON line on stdout
"""
import sys, json, time
from pathlib import Path
from collections import deque
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'workings/barnette_lab'))
from barnette_lab.core import Instance, plantri_graphs
from barnette_lab.algorithms import marked_walk

V = int(sys.argv[1])
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
P = ROOT / 'workings/barnette_lab/vendor/plantri.exe'
t_start = time.time()
tot = dict(V=V, rooted=0, pairs=0, nontree_starts=0, gm_max_moves=0, gm_sum_moves=0, gm_max_total=0,
           gm_restarts=0, gm_timeouts=0, bfs_max=0, bfs_sum=0, hist={})
worst = None
done = 0
for t in plantri_graphs(V, P):
    probe = Instance(t)
    for f in range(len(probe.faces)):
        b = Instance(t, f)
        if b.flow_pair() is None:
            continue
        pairs = b.pairs()
        if not pairs:
            continue
        tot['rooted'] += 1; tot['pairs'] += len(pairs)
        tree = {p for p in pairs if not b.qcycles(p[1])}
        # BFS distance to a tree pair
        dist = {p: 0 for p in tree}; q = deque(tree)
        while q:
            p = q.popleft()
            for nb in b.neighbors(p):
                if nb not in dist:
                    dist[nb] = dist[p] + 1; q.append(nb)
        for p in pairs:
            if p in tree:
                continue
            tot['nontree_starts'] += 1
            tot['bfs_max'] = max(tot['bfs_max'], dist[p]); tot['bfs_sum'] += dist[p]
            try:
                _, info = marked_walk(b, p, cap=200000)
            except TimeoutError:
                tot['gm_timeouts'] += 1
                continue
            m = info['moves']; total = m + info['normalization_reversals']
            tot['gm_sum_moves'] += m; tot['gm_restarts'] += len(info['restarts'])
            tot['hist'][m] = tot['hist'].get(m, 0) + 1
            if m > tot['gm_max_moves']:
                tot['gm_max_moves'] = m
                worst = dict(graph=sorted(map(list, t.edges())), outer=f, r=list(p[0]), s=list(p[1]), info=info)
            tot['gm_max_total'] = max(tot['gm_max_total'], total)
        done += 1
        if done >= limit:
            break
    if done >= limit:
        break
tot['hist'] = {str(k): v for k, v in sorted(tot['hist'].items())}
tot['worst'] = worst
tot['seconds'] = round(time.time() - t_start, 1)
print(json.dumps(tot))
