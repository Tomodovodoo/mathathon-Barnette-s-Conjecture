"""Periodic surplus walks: detection, minimal examples, and whether they are traps for Step X.

Usage (from the repository root):
    python research/2026-11-14_fable_referee-topology/code/exp_cycles.py analyse
        re-examine the failures recorded by exp_walk.py (saved and random instances): exact
        periods, which walkers are periodic, and whether general plateau moves still escape.
    python .../exp_cycles.py hunt V COUNT SEED [GLUE]
        random triangulations of order V; search for a rainbow tree all of whose surplus walks
        are periodic, then test whether its plateau component is closed (a trap for Step X).
"""
import json
import random
import sys
import time
from collections import Counter, deque
from pathlib import Path

import etri
from rainbow import RB, climb, random_walk

DATA = Path(__file__).resolve().parents[1] / 'data'


def save(name, obj):
    obj = {'command': 'python research/2026-11-14_fable_referee-topology/code/exp_cycles.py ' + ' '.join(sys.argv[1:]),
           'result': obj}
    (DATA / f'{name}.json').write_text(json.dumps(obj, indent=1))
    print(json.dumps(obj['result'], indent=1)[:6000])


def orbit(rb, sigma, t, x_in, cap=100000):
    """Follow the surplus walk from (sigma, t, x_in). Returns ('descent', steps, sigma_after) or
    ('cycle', period, None) or ('cap', cap, None). Exact: the full state is compared with the start."""
    X = rb.X
    sg = dict(sigma)
    pts = {}
    for x, f in sg.items():
        pts.setdefault(f, []).append(x)
    start = (t, x_in, tuple(sg[x] for x in X))
    steps = 0
    while steps < cap:
        y = pts[t][0] if pts[t][1] == x_in else pts[t][1]
        (t2,) = rb.move_target(sg, y)
        empty = len(pts.get(t2, [])) == 0
        sg[y] = t2
        pts[t].remove(y)
        pts.setdefault(t2, []).append(y)
        steps += 1
        if empty:
            return 'descent', steps, sg
        t, x_in = t2, y
        if t == start[0] and x_in == start[1] and tuple(sg[x] for x in X) == start[2]:
            return 'cycle', steps, None
    return 'cap', cap, None


def walkers(rb, sigma):
    pts = {}
    for x, f in sigma.items():
        pts.setdefault(f, []).append(x)
    return [(t, p[0]) for t, p in pts.items() if len(p) == 2]


def plateau_search(rb, sigma, cap=200000, tlimit=120):
    """Breadth-first search over ALL moves that keep the excess, looking for one that lowers it.
    Returns ('descent', depth, explored) / ('closed', None, explored) / ('cap', None, explored)."""
    X = rb.X
    pos = {x: j for j, x in enumerate(X)}
    key0 = tuple(sigma[x] for x in X)
    seen = {key0: 0}
    dq = deque([key0])
    t0 = time.time()
    while dq:
        key = dq.popleft()
        s = dict(zip(X, key))
        ld = rb.load(s)
        for x in X:
            t = s[x]
            if ld[t] != 2 and not any(ld.get(tt, 1) == 0 for (tt, _, _) in rb.opt[x]):
                continue
            (t2,) = rb.move_target(s, x)
            d = (abs(ld[t] - 2) - abs(ld[t] - 1)) + (abs(ld[t2]) - abs(ld[t2] - 1))
            if d < 0:
                return 'descent', seen[key] + 1, len(seen)
            if d == 0:
                j = pos[x]
                k2 = key[:j] + (t2,) + key[j + 1:]
                if k2 not in seen:
                    seen[k2] = seen[key] + 1
                    dq.append(k2)
        if len(seen) > cap or time.time() - t0 > tlimit:
            return 'cap', None, len(seen)
    return 'closed', None, len(seen)


def examine(I, sigma, out, tag):
    rb = RB(I)
    ws = walkers(rb, sigma)
    kinds = []
    for (t, x) in ws:
        k, steps, _ = orbit(rb, sigma, t, x)
        kinds.append((k, steps))
    rec = {'tag': tag, 'V': I.nv, 'excess': 2 * len(ws), 'orbits': kinds,
           'all_periodic': all(k == 'cycle' for k, _ in kinds)}
    if rec['all_periodic']:
        res = plateau_search(rb, sigma)
        rec['plateau_search'] = res
    out.append(rec)
    return rec


def exp_analyse():
    out = []
    files = sorted(DATA.glob('walk_*.json'))
    for p in files:
        d = json.load(open(p))['result']
        fl = []
        if 'failures' in d:
            fl = d['failures']
        else:
            for v in d.values():
                if isinstance(v, dict):
                    fl += v.get('failures', [])
        for f in fl:
            tri = etri.Tri(f['rot'])
            I = etri.Inst(tri, tri.face_by_vertices(f['outer_face_vertices']))
            sigma = {int(x): tri.face_by_vertices(tv) for x, tv in f['sigma'].items()}
            rec = examine(I, sigma, out, [p.name, f['tag']])
            print(rec, flush=True)
    save('cycles_analyse', out)


def reduce_to_single_walker(rb, sigma, rng, tries=40):
    """From a tree whose chosen walker is periodic, try to lower the excess with the other walkers,
    keeping note of trees where every walker is periodic."""
    cur = dict(sigma)
    while True:
        ws = walkers(rb, cur)
        if not ws:
            return 'tree_matching', cur
        rng.shuffle(ws)
        moved = False
        for (t, x) in ws:
            k, steps, after = orbit(rb, cur, t, x, cap=20000)
            if k == 'descent':
                cur = after
                moved = True
                break
        if not moved:
            return 'all_periodic', cur


def exp_hunt(V, count, seed, glue):
    rng = random.Random(seed)
    cnt = Counter()
    examples = []
    t0 = time.time()
    for i in range(count):
        tri = etri.Tri(etri.random_eulerian(V, rng, glue))
        I = etri.Inst(tri, rng.randrange(len(tri.faces)))
        rb = RB(I)
        sig = rb.point_rainbow_tree(rng)
        if sig is None:
            cnt['no_rainbow_tree'] += 1
            continue
        cnt['instances'] += 1
        for rep in range(6):
            s = climb(rb, random_walk(rb, sig, 4 * rb.n, rng), rng, 20 * rb.n)
            # classify every walker of the start and of the trees met while descending
            cur = s
            while True:
                ws = walkers(rb, cur)
                if not ws:
                    cnt['reached_tree_matching'] += 1
                    break
                res = [(orbit(rb, cur, t, x, cap=20000), t, x) for (t, x) in ws]
                cyc = [r for r in res if r[0][0] == 'cycle']
                cnt['trees_examined'] += 1
                cnt['walkers'] += len(res)
                cnt['periodic_walkers'] += len(cyc)
                if cyc:
                    cnt['trees_with_periodic_walker'] += 1
                    per = min(r[0][1] for r in cyc)
                    cnt['min_period'] = per if 'min_period' not in cnt else min(cnt['min_period'], per)
                desc = [r for r in res if r[0][0] == 'descent']
                if not desc:
                    cnt['trees_all_periodic'] += 1
                    ps = plateau_search(rb, cur, cap=100000, tlimit=60)
                    cnt['all_periodic_plateau_' + ps[0]] += 1
                    if len(examples) < 6:
                        examples.append({'V': V, 'i': i, 'rot': tri.rot, 'outer_face_vertices': list(I.R),
                                         'excess': 2 * len(ws), 'periods': [r[0][1] for r in res], 'plateau_search': ps,
                                         'sigma': {str(x): list(I.faces[t]) for x, t in cur.items()}})
                    break
                cur = rng.choice(desc)[0][2]
        if time.time() - t0 > 500:
            cnt['TIMED_OUT_at'] = i
            break
    save('cycles_hunt_%d_%d_%d_%s' % (V, count, seed, glue), {'V': V, 'count': count, 'seed': seed, 'glue_prob': glue,
                                                           'counts': dict(cnt), 'examples': examples,
                                                           'seconds': round(time.time() - t0, 1)})


if __name__ == '__main__':
    if sys.argv[1] == 'analyse':
        exp_analyse()
    else:
        exp_hunt(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]) if len(sys.argv) > 5 else 0.0)
