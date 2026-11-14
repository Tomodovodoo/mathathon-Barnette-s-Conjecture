"""The surplus walk ("evict the resident") on point-rainbow trees. Own implementation.

A walk state is (sigma, t, x): a rainbow tree, a black face t of load 2, and one of the two
points assigned to t (the arrival). One step moves the OTHER point y of t (the resident) by its
unique exchange to a face t'. If t' was empty the excess drops by 2 and the walk stops. Otherwise
the new state is (sigma', t', y). The step is reversible, so the states of one excess level form
paths (both ends are excess-decreasing moves) and cycles.

Usage (from the repository root):
    python research/2026-11-14_fable_referee-topology/code/exp_walk.py exhaust VMIN VMAX [all|two]
        every rainbow tree: orbit structure of the walk, cycles, path lengths, and the involutions
        on tree matchings obtained at excess 2.
    python .../exp_walk.py sample V EVERY SEED
        plantri triangulations of order V, random and adversarial starts, walk until excess 0.
    python .../exp_walk.py random V COUNT SEED [GLUE]
        random large triangulations.
    python .../exp_walk.py saved
        the saved instances of the graph-theory run.
"""
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

import etri
from rainbow import RB, climb, random_walk

DATA = Path(__file__).resolve().parents[1] / 'data'


def save(name, obj):
    DATA.mkdir(exist_ok=True)
    obj = {'command': 'python research/2026-11-14_fable_referee-topology/code/exp_walk.py ' + ' '.join(sys.argv[1:]),
           'result': obj}
    (DATA / f'{name}.json').write_text(json.dumps(obj, indent=1))
    print(json.dumps(obj['result'], indent=1)[:5000])


def neighbours(trees, n):
    index = {s: i for i, s in enumerate(trees)}
    nbr = [[None] * n for _ in trees]
    for j in range(n):
        groups = {}
        for i, s in enumerate(trees):
            groups.setdefault(s[:j] + s[j + 1:], []).append(i)
        for g in groups.values():
            assert len(g) == 2
            nbr[g[0]][j] = g[1]
            nbr[g[1]][j] = g[0]
    return nbr


def exhaust_instance(I, rb, trees):
    X = rb.X
    n = len(X)
    N = len(trees)
    nbr = neighbours(trees, n)
    # points at each face for each tree: only faces of load 2 matter
    twos = []      # twos[i] = list of (t, ja, jb) with X[ja], X[jb] assigned to t
    exc = []
    for s in trees:
        where = {}
        for j, t in enumerate(s):
            where.setdefault(t, []).append(j)
        tw = [(t, v[0], v[1]) for t, v in where.items() if len(v) == 2]
        twos.append(tw)
        exc.append(2 * len(tw))
    res = Counter()
    # a walk state is (i, j_arrival); its face is trees[i][j_arrival]
    partner = [dict() for _ in range(N)]
    for i in range(N):
        for (t, ja, jb) in twos[i]:
            partner[i][ja] = jb
            partner[i][jb] = ja

    def step(i, ja):
        """Evict the resident. Returns ('end', tree) or ('go', i2, jb)."""
        jb = partner[i][ja]
        i2 = nbr[i][jb]
        if exc[i2] < exc[i]:
            return ('end', i2, jb)
        return ('go', i2, jb)

    seen = set()
    maxlen = 0
    lens = Counter()
    inv = {}       # (tree matching index, empty face) -> tree matching index, from excess-2 paths
    cyc_examples = []
    for i in range(N):
        for ja in partner[i]:
            if (i, ja) in seen:
                continue
            # walk backwards to the start of the orbit, or detect a cycle
            orbit = [(i, ja)]
            seen.add((i, ja))
            # forward
            cur = (i, ja)
            ends = []
            cyc = False
            while True:
                r = step(*cur)
                if r[0] == 'end':
                    ends.append((cur, r[1], r[2]))
                    break
                cur = (r[1], r[2])
                if cur in seen:
                    cyc = True
                    break
                seen.add(cur)
                orbit.append(cur)
            if not cyc:
                # backward: the reverse of a step from (i, ja) evicts the arrival itself,
                # which is the forward step of the mirrored state (i, partner)
                cur = (i, partner[i][ja])
                seen.add(cur)
                while True:
                    r = step(*cur)
                    if r[0] == 'end':
                        ends.append((cur, r[1], r[2]))
                        break
                    cur = (r[1], r[2])
                    assert cur not in seen
                    seen.add(cur)
                    orbit.append(cur)
                    # mark the mirror image too
                # mirror states of the forward part
                for (a, b) in list(orbit):
                    seen.add((a, partner[a][b]))
                res['paths'] += 1
                L = len(orbit)
                lens[min(L, 60)] += 1
                maxlen = max(maxlen, L)
                if exc[i] == 2 and len(ends) == 2:
                    (c1, m1, j1), (c2, m2, j2) = ends
                    # the empty face is the target of the final move
                    f1 = trees[m1][j1]
                    f2 = trees[m2][j2]
                    res['excess2_paths'] += 1
                    res['excess2_same_empty_face'] += (f1 == f2)
                    res['excess2_distinct_ends'] += (m1 != m2)
                    inv[(m1, f1)] = m2
                    inv[(m2, f2)] = m1
            else:
                for (a, b) in list(orbit):
                    seen.add((a, partner[a][b]))
                res['cycles'] += 1
                res['cycle_states'] += len(orbit)
                if len(cyc_examples) < 3:
                    cyc_examples.append({'excess': exc[i], 'length': len(orbit),
                                         'sigma_faces': [list(I.faces[t]) for t in trees[i]], 'X': X,
                                         'face_t': list(I.faces[trees[i][ja]]), 'arrival_point': X[ja]})
    tms = [i for i in range(N) if exc[i] == 0]
    res['tree_matchings'] = len(tms)
    res['involution_defined'] = len(inv)
    res['involution_expected'] = len(tms) * n
    res['involution_ok'] = sum(1 for (m, f), m2 in inv.items() if inv.get((m2, f)) == m and m2 != m)
    res['trees'] = N
    res['states'] = sum(len(p) for p in partner)
    # is the graph on tree matchings with edges s -- iota_t(s) connected?
    if tms:
        comp = {tms[0]}
        st = [tms[0]]
        nb = {}
        for (m, f), m2 in inv.items():
            nb.setdefault(m, []).append(m2)
        while st:
            a_ = st.pop()
            for b_ in nb.get(a_, []):
                if b_ not in comp:
                    comp.add(b_)
                    st.append(b_)
        res['iota_graph_connected'] = int(len(comp) == len(tms))
        res['instances_with_tm'] = 1
    return res, maxlen, lens, cyc_examples


def exp_exhaust(vmin, vmax, roots):
    tot = Counter()
    lens = Counter()
    maxlen_by_v = {}
    examples = []
    t0 = time.time()
    rsel = 'all' if roots == 'all' else (lambda tri: [0, next(f for f in range(len(tri.faces)) if tri.col[f] != tri.col[0])])
    for V, idx, f0, I in etri.all_rooted(vmin, vmax, rsel):
        rb = RB(I)
        trees = rb.all_trees()
        if not trees:
            continue
        res, maxlen, ln, cyc = exhaust_instance(I, rb, trees)
        tot['instances'] += 1
        for k, v in res.items():
            tot[k] += v
        tot['instances_with_cycle'] += (res['cycles'] > 0)
        lens.update(ln)
        maxlen_by_v[V] = max(maxlen_by_v.get(V, 0), maxlen)
        for c in cyc:
            if len(examples) < 10:
                c.update({'V': V, 'plantri_index': idx, 'outer_face_vertices': list(I.R), 'rot': I.tri.rot,
                          'sep_triangles': len(I.tri.separating_triangles())})
                examples.append(c)
        if time.time() - t0 > 540:
            tot['TIMED_OUT'] = 1
            break
    save('walk_exhaust_%d_%d_%s' % (vmin, vmax, roots), {'range': [vmin, vmax], 'roots': roots, 'counts': dict(tot),
                                                        'max_path_states_by_V': maxlen_by_v,
                                                        'path_length_histogram': dict(sorted(lens.items())),
                                                        'cycle_examples': examples, 'seconds': round(time.time() - t0, 1)})


# ------------------------------------------------------------------ long walks on big instances
def walk_down(rb, sigma, rng, max_steps=200000):
    """Repeat: pick a face of load 2 and an arrival point at random, walk until the excess drops.
    Returns (ok, total steps, longest single walk, start excess, sigma)."""
    sigma = dict(sigma)
    load = rb.load(sigma)
    pts = {}
    for x, t in sigma.items():
        pts.setdefault(t, []).append(x)
    total = 0
    longest = 0
    exc0 = sum(abs(v - 1) for v in load.values())
    while True:
        twos = [t for t in rb.I.A if load[t] == 2]
        if not twos:
            return True, total, longest, exc0, sigma
        t = rng.choice(twos)
        x_in = rng.choice(pts[t])
        start = (t, x_in, tuple(sorted(sigma.items())))
        steps = 0
        while True:
            y = pts[t][0] if pts[t][1] == x_in else pts[t][1]
            (t2,) = rb.move_target(sigma, y)
            sigma[y] = t2
            pts[t].remove(y)
            pts.setdefault(t2, []).append(y)
            load[t] -= 1
            load[t2] += 1
            steps += 1
            if load[t2] == 1:
                break
            t, x_in = t2, y
            if steps > max_steps:
                return False, total + steps, steps, exc0, sigma
            if steps % 64 == 0 and (t, x_in, tuple(sorted(sigma.items()))) == start:
                return False, total + steps, -steps, exc0, sigma
        total += steps
        longest = max(longest, steps)


def run_trials(I, rng, cnt, hist, fails, tag, starts=3):
    rb = RB(I)
    sig = rb.point_rainbow_tree(rng)
    if sig is None:
        cnt['no_rainbow_tree'] += 1
        return
    for k in range(starts):
        s = random_walk(rb, sig, 4 * rb.n, rng)
        if k > 0:
            s = climb(rb, s, rng, 30 * rb.n)
        ok, total, longest, exc0, out = walk_down(rb, s, rng)
        cnt['starts'] += 1
        cnt['reached'] += ok
        cnt['max_start_excess'] = max(cnt['max_start_excess'], exc0)
        cnt['max_total_steps'] = max(cnt['max_total_steps'], total)
        cnt['max_single_walk'] = max(cnt['max_single_walk'], longest)
        cnt['sum_total_steps'] += total
        hist[min(longest // max(1, rb.n), 20)] += 1
        if ok:
            inv = {t: x for x, t in out.items()}
            assert I.is_tree_matching(tuple(inv[t] for t in I.A))
        elif len(fails) < 10:
            fails.append({'tag': tag, 'rot': I.tri.rot, 'outer_face_vertices': list(I.R), 'steps': total, 'longest': longest,
                          'sigma': {str(x): list(I.faces[t]) for x, t in out.items()}})


def exp_sample(V, step, seed):
    rng = random.Random(seed)
    cnt = Counter()
    hist = Counter()
    fails = []
    t0 = time.time()
    rots = etri.plantri(V)
    cnt['triangulations_total'] = len(rots)
    for idx in range(seed % step, len(rots), step):
        tri = etri.Tri(rots[idx])
        cnt['triangulations_used'] += 1
        for f0 in rng.sample(range(len(tri.faces)), 2):
            cnt['rooted'] += 1
            run_trials(etri.Inst(tri, f0), rng, cnt, hist, fails, [V, idx, f0])
        if time.time() - t0 > 540:
            cnt['TIMED_OUT_at_index'] = idx
            break
    save('walk_sample_%d_%d_%d' % (V, step, seed), {'V': V, 'every': step, 'seed': seed, 'counts': dict(cnt),
                                                   'longest_walk_over_n_histogram': dict(sorted(hist.items())), 'failures': fails,
                                                   'seconds': round(time.time() - t0, 1)})


def exp_random(V, count, seed, glue):
    rng = random.Random(seed)
    cnt = Counter()
    hist = Counter()
    fails = []
    t0 = time.time()
    for i in range(count):
        tri = etri.Tri(etri.random_eulerian(V, rng, glue))
        cnt['rooted'] += 1
        run_trials(etri.Inst(tri, rng.randrange(len(tri.faces))), rng, cnt, hist, fails, [V, i])
        if time.time() - t0 > 540:
            cnt['TIMED_OUT_at'] = i
            break
    save('walk_random_%d_%d_%d_%s' % (V, count, seed, glue), {'V': V, 'count': count, 'seed': seed, 'glue_prob': glue,
                                                           'counts': dict(cnt), 'longest_walk_over_n_histogram': dict(sorted(hist.items())),
                                                           'failures': fails, 'seconds': round(time.time() - t0, 1)})


def exp_saved():
    base = etri.REPO / 'research' / '2026-11-14_opus_route-graph-theory' / 'code' / 'data'
    rng = random.Random(5)
    out = {}
    t00 = time.time()
    for name in ['deeptrap_50_1', 'strongviol_50_seed50', 'ef_fail_40_40', 'alpha_min_fail_40_41', 'alpha_min_fail_60_61',
                 'alpha_min_fail_80_83', 'alpha_max_fail_80_83', 'alpha_max_fail_100_7', 'alpha_min_fail_100_7',
                 'alpha_max_fail_120_123', 'alpha_min_fail_120_123']:
        p = base / (name + '.json')
        if not p.exists() or time.time() - t00 > 500:
            out[name] = 'skipped'
            continue
        rot, d = etri.load_rot_json(p)
        tri = etri.Tri(rot)
        I = etri.Inst(tri, tri.face_by_vertices(d['t0']))
        cnt = Counter()
        hist = Counter()
        fails = []
        t0 = time.time()
        for rep in range(3):
            run_trials(I, rng, cnt, hist, fails, name)
        out[name] = {'V': tri.nv, 'counts': dict(cnt), 'failures': fails, 'seconds': round(time.time() - t0, 1)}
        print(name, out[name]['counts'], flush=True)
    save('walk_saved', out)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'exhaust':
        exp_exhaust(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else 'all')
    elif cmd == 'sample':
        exp_sample(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == 'random':
        exp_random(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]) if len(sys.argv) > 5 else 0.0)
    elif cmd == 'saved':
        exp_saved()
