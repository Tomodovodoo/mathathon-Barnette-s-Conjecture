"""Experiments on Step R and Step X. Own implementation (etri.py, rainbow.py).

Usage (from the repository root):
    python research/2026-11-14_fable_referee-topology/code/exp_rainbow.py rado 12
        Rado condition by brute force over all vertex sets J, against the triangle criterion
        and the exact formula of RAINBOW.md Theorem R.
    python .../exp_rainbow.py exist 16
        point-rainbow tree (matroid intersection) vs pair (flow) vs black-inner triangle,
        and the face-rainbow tree, on every rooted instance.
    python .../exp_rainbow.py traps VMIN VMAX [all|two]
        every point-rainbow tree of every rooted instance; move graph; plateau components.
    python .../exp_rainbow.py sample V NTRI SEED [c4]
        plantri triangulations with V vertices (every NTRI-th), random and adversarial starts.
    python .../exp_rainbow.py random V COUNT SEED [GLUE]
        random large triangulations.
    python .../exp_rainbow.py saved
        the saved V = 40, 50, 80 instances of the graph-theory run.
"""
import json
import random
import sys
import time
from collections import Counter, deque
from pathlib import Path

import etri
from rainbow import RB, climb, descend, random_walk

DATA = Path(__file__).resolve().parents[1] / 'data'


def save(name, obj):
    DATA.mkdir(exist_ok=True)
    obj = {'command': 'python research/2026-11-14_fable_referee-topology/code/exp_rainbow.py ' + ' '.join(sys.argv[1:]),
           'result': obj}
    (DATA / f'{name}.json').write_text(json.dumps(obj, indent=1))
    txt = json.dumps(obj['result'], indent=1)
    print(txt[:4000])


# ------------------------------------------------------------------ Rado condition
def exp_rado(vmax):
    cnt = Counter()
    worst = []
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        cnt['instances'] += 1
        X = I.X
        nb = [set(r) for r in I.tri.rot]
        wf = [[f for f in I.Wh if v in I.faces[f]] for v in range(I.nv)]
        bi = len(I.black_inner_triangles()) > 0
        viol = False
        mindef = None
        for mask in range(1, 1 << len(X)):
            J = [X[i] for i in range(len(X)) if (mask >> i) & 1]
            Js = set(J)
            # connected?
            st = [J[0]]
            seen = {J[0]}
            while st:
                a = st.pop()
                for b in nb[a]:
                    if b in Js and b not in seen:
                        seen.add(b)
                        st.append(b)
            if len(seen) != len(J):
                continue
            w = len({f for v in J for f in wf[v]})
            slack = w - len(J) - 1
            cnt['connected_sets'] += 1
            # exact formula: slack = (c - 1) + (3d - sigma - 12) / 6 for the face of T[U] containing J
            U = [v for v in range(I.nv) if v not in Js]
            Us = set(U)
            # components of T[U]
            comp = {}
            c = 0
            for u in U:
                if u in comp:
                    continue
                c += 1
                comp[u] = c
                st = [u]
                while st:
                    a = st.pop()
                    for b in nb[a]:
                        if b in Us and b not in comp:
                            comp[b] = c
                            st.append(b)
            # boundary sides of the region containing J: darts (u, v) in T[U] whose left face has a corner in J
            d = 0
            sig = 0
            for u in U:
                for v in I.tri.rot[u]:
                    if v in Us:
                        f = I.face_of[(u, v)]
                        if any(z in Js for z in I.faces[f]):
                            d += 1
                            sig += 1 if I.black[f] else -1
            pred6 = 6 * (c - 1) + (3 * d - sig - 12)
            cnt['formula_ok'] += (6 * slack == pred6)
            if slack < 0:
                viol = True
                cnt['violating_sets'] += 1
                cnt['violations_are_d3_sigma3_c1'] += (d == 3 and sig == 3 and c == 1)
            if mindef is None or slack < mindef:
                mindef = slack
        cnt['criterion_agrees'] += (viol == bi)
        cnt['with_black_inner'] += bi
        cnt['min_slack_%d' % mindef] += 1
    save('rado_%d' % vmax, {'vmax': vmax, 'counts': dict(cnt)})


# ------------------------------------------------------------------ existence
def exp_exist(vmax):
    cnt = Counter()
    per_v = {}
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        rb = RB(I)
        cnt['instances'] += 1
        pair = I.has_pair_flow()
        bi = len(I.black_inner_triangles()) > 0
        sig = rb.point_rainbow_tree()
        if sig is not None:
            assert rb.is_tree(sig)
        fr = rb.face_rainbow_tree()
        cnt['pair'] += pair
        cnt['point_rainbow'] += (sig is not None)
        cnt['face_rainbow'] += fr
        cnt['pair_iff_point_rainbow'] += (pair == (sig is not None))
        cnt['pair_iff_no_black_inner'] += (pair == (not bi))
        d = per_v.setdefault(V, Counter())
        d['instances'] += 1
        d['pair'] += pair
    save('exist_%d' % vmax, {'vmax': vmax, 'counts': dict(cnt), 'per_V': {k: dict(v) for k, v in per_v.items()}})


# ------------------------------------------------------------------ exhaustive trap search
def analyse(I, rb, trees):
    X = rb.X
    n = len(X)
    index = {s: i for i, s in enumerate(trees)}
    N = len(trees)
    # neighbours: group by the tuple with one coordinate removed
    nbr = [[None] * n for _ in range(N)]
    bad_unique = 0
    for j in range(n):
        groups = {}
        for i, s in enumerate(trees):
            groups.setdefault(s[:j] + s[j + 1:], []).append(i)
        for g in groups.values():
            if len(g) != 2:
                bad_unique += 1
                continue
            nbr[g[0]][j] = g[1]
            nbr[g[1]][j] = g[0]
    Aidx = {t: i for i, t in enumerate(I.A)}
    exc = []
    for s in trees:
        c = [0] * n
        for t in s:
            c[Aidx[t]] += 1
        exc.append(sum(abs(v - 1) for v in c))
    # connectivity of the full move graph
    seen = [False] * N
    seen[0] = True
    st = [0]
    while st:
        a = st.pop()
        for b in nbr[a]:
            if b is not None and not seen[b]:
                seen[b] = True
                st.append(b)
    connected = all(seen)
    # plateau components
    par = list(range(N))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    has_desc = [False] * N
    for i in range(N):
        for b in nbr[i]:
            if b is None:
                continue
            if exc[b] == exc[i]:
                par[find(i)] = find(b)
            elif exc[b] < exc[i]:
                has_desc[i] = True
    comp_desc = {}
    comp_size = Counter()
    for i in range(N):
        r = find(i)
        comp_desc[r] = comp_desc.get(r, False) or has_desc[i]
        comp_size[r] += 1
    traps = [r for r in comp_desc if exc[r] > 0 and not comp_desc[r]]
    # depth: plateau distance to a point with a decreasing move
    maxdepth = 0
    dist = [None] * N
    dq = deque()
    for i in range(N):
        if has_desc[i] or exc[i] == 0:
            dist[i] = 0
            dq.append(i)
    while dq:
        a = dq.popleft()
        for b in nbr[a]:
            if b is not None and dist[b] is None and exc[b] == exc[a]:
                dist[b] = dist[a] + 1
                dq.append(b)
    maxdepth = max((d for d in dist if d is not None), default=0)
    return {'N': N, 'bad_unique': bad_unique, 'connected': connected, 'max_excess': max(exc), 'tree_matchings': exc.count(0),
            'no_immediate_descent': sum(1 for i in range(N) if exc[i] > 0 and not has_desc[i]),
            'traps': [(trees[r], exc[r], comp_size[r]) for r in traps], 'maxdepth': maxdepth}


def exp_traps(vmin, vmax, roots):
    cnt = Counter()
    hist_depth = Counter()
    trap_examples = []
    t0 = time.time()
    rsel = 'all' if roots == 'all' else (lambda tri: [0, next(f for f in range(len(tri.faces)) if tri.col[f] != tri.col[0])])
    for V, idx, f0, I in etri.all_rooted(vmin, vmax, rsel):
        rb = RB(I)
        trees = rb.all_trees()
        cnt['instances'] += 1
        if not trees:
            cnt['no_rainbow_tree'] += 1
            assert len(I.black_inner_triangles()) > 0
            continue
        res = analyse(I, rb, trees)
        cnt['with_rainbow_tree'] += 1
        cnt['rainbow_trees'] += res['N']
        cnt['tree_matchings'] += res['tree_matchings']
        cnt['unique_move_violations'] += res['bad_unique']
        cnt['move_graph_connected'] += res['connected']
        cnt['instances_with_trap'] += (len(res['traps']) > 0)
        cnt['trap_components'] += len(res['traps'])
        cnt['plateau_points_without_immediate_descent'] += res['no_immediate_descent']
        cnt['max_excess_max'] = max(cnt['max_excess_max'], res['max_excess'])
        hist_depth[res['maxdepth']] += 1
        cnt['largest_N'] = max(cnt['largest_N'], res['N'])
        if res['traps'] and len(trap_examples) < 20:
            tr, e, sz = res['traps'][0]
            trap_examples.append({'V': V, 'plantri_index': idx, 'outer_face_vertices': list(I.R), 'rot': I.tri.rot,
                                  'X': rb.X, 'sigma_faces': [list(I.faces[t]) for t in tr], 'excess': e, 'plateau_size': sz,
                                  'n_traps': len(res['traps']), 'N': res['N'], 'sep_triangles': len(I.tri.separating_triangles())})
        if time.time() - t0 > 540:
            cnt['TIMED_OUT'] = 1
            break
    save('traps_%d_%d_%s' % (vmin, vmax, roots), {'range': [vmin, vmax], 'roots': roots, 'counts': dict(cnt),
                                               'maxdepth_histogram': dict(hist_depth), 'trap_examples': trap_examples,
                                               'seconds': round(time.time() - t0, 1)})


# ------------------------------------------------------------------ sampling at larger sizes
def trial(I, rng, starts=3, cap=20000):
    rb = RB(I)
    sig = rb.point_rainbow_tree(rng)
    if sig is None:
        return None
    out = []
    for k in range(starts):
        s = random_walk(rb, sig, 4 * rb.n, rng)
        if k > 0:
            s = climb(rb, s, rng, 30 * rb.n)
        res = descend(rb, s, cap)
        res['kind'] = 'random' if k == 0 else 'climbed'
        if res['ok']:
            st = tuple(res['sigma'][x] for x in rb.X)
            # sigma is a bijection X -> A: turn it into a state and test it with the independent predicate
            inv = {t: x for x, t in res['sigma'].items()}
            state = tuple(inv[t] for t in I.A)
            assert I.is_tree_matching(state)
        out.append(res)
    return out


def summarise(cnt, hist, fails, I, tag, results):
    for res in results:
        cnt['starts'] += 1
        cnt['reached'] += res['ok']
        cnt['max_start_excess'] = max(cnt['max_start_excess'], res['start_excess'])
        if res['ok']:
            cnt['max_plateau'] = max(cnt['max_plateau'], res['max_plateau'])
            cnt['max_depth'] = max(cnt['max_depth'], res['max_depth'])
            cnt['max_steps'] = max(cnt['max_steps'], res['steps'])
            hist[min(res['max_depth'], 10)] += 1
        else:
            cnt['stuck_' + res['stuck']] += 1
            if len(fails) < 20:
                fails.append({'tag': tag, 'rot': I.tri.rot, 'outer_face_vertices': list(I.R), 'excess': res['excess'],
                              'plateau': res['plateau'], 'stuck': res['stuck'],
                              'sigma': {str(x): list(I.faces[t]) for x, t in res['sigma'].items()}})


def exp_sample(V, step, seed, opts):
    rng = random.Random(seed)
    cnt = Counter()
    hist = Counter()
    fails = []
    t0 = time.time()
    rots = etri.plantri(V, '-bac4' if 'c4' in opts else '-ba')
    cnt['triangulations_total'] = len(rots)
    for idx in range(seed % step, len(rots), step):
        tri = etri.Tri(rots[idx])
        for f0 in rng.sample(range(len(tri.faces)), 2):
            I = etri.Inst(tri, f0)
            res = trial(I, rng)
            cnt['rooted'] += 1
            if res is None:
                cnt['no_rainbow_tree'] += 1
                continue
            summarise(cnt, hist, fails, I, [V, idx, f0], res)
        if time.time() - t0 > 540:
            cnt['TIMED_OUT_at_index'] = idx
            break
    save('sample_%d_%d_%d%s' % (V, step, seed, '_c4' if 'c4' in opts else ''),
         {'V': V, 'every': step, 'seed': seed, 'counts': dict(cnt), 'max_depth_histogram': dict(hist), 'failures': fails,
          'seconds': round(time.time() - t0, 1)})


def exp_random(V, count, seed, glue):
    rng = random.Random(seed)
    cnt = Counter()
    hist = Counter()
    fails = []
    t0 = time.time()
    for i in range(count):
        rot = etri.random_eulerian(V, rng, glue)
        tri = etri.Tri(rot)
        f0 = rng.randrange(len(tri.faces))
        I = etri.Inst(tri, f0)
        res = trial(I, rng, starts=3, cap=30000)
        cnt['rooted'] += 1
        if res is None:
            cnt['no_rainbow_tree'] += 1
            continue
        summarise(cnt, hist, fails, I, [V, i], res)
        if time.time() - t0 > 540:
            cnt['TIMED_OUT_at'] = i
            break
    save('random_%d_%d_%d_%s' % (V, count, seed, glue), {'V': V, 'count': count, 'seed': seed, 'glue_prob': glue, 'counts': dict(cnt),
                                                      'max_depth_histogram': dict(hist), 'failures': fails,
                                                      'seconds': round(time.time() - t0, 1)})


def exp_saved():
    base = etri.REPO / 'research' / '2026-11-14_opus_route-graph-theory' / 'code' / 'data'
    rng = random.Random(5)
    out = {}
    for name in ['deeptrap_50_1', 'strongviol_50_seed50', 'ef_fail_40_40', 'alpha_min_fail_40_41', 'alpha_min_fail_60_61',
                 'alpha_min_fail_80_83', 'alpha_max_fail_80_83', 'alpha_max_fail_100_7', 'alpha_min_fail_100_7']:
        p = base / (name + '.json')
        if not p.exists():
            out[name] = 'missing'
            continue
        rot, d = etri.load_rot_json(p)
        tri = etri.Tri(rot)
        I = etri.Inst(tri, tri.face_by_vertices(d['t0']))
        cnt = Counter()
        hist = Counter()
        fails = []
        t0 = time.time()
        for rep in range(4):
            res = trial(I, rng, starts=3, cap=30000)
            summarise(cnt, hist, fails, I, name, res)
        out[name] = {'V': tri.nv, 'counts': dict(cnt), 'failures': fails, 'seconds': round(time.time() - t0, 1)}
        print(name, out[name]['counts'], flush=True)
    save('saved_instances', out)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'rado':
        exp_rado(int(sys.argv[2]))
    elif cmd == 'exist':
        exp_exist(int(sys.argv[2]))
    elif cmd == 'traps':
        exp_traps(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else 'all')
    elif cmd == 'sample':
        exp_sample(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5:])
    elif cmd == 'random':
        exp_random(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]) if len(sys.argv) > 5 else 0.0)
    elif cmd == 'saved':
        exp_saved()
