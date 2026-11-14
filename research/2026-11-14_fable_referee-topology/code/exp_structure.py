"""Structure of the rainbow-tree move graph: identities, load vectors, candidate potentials.

Usage (from the repository root):
    python research/2026-11-14_fable_referee-topology/code/exp_structure.py identity 12
        fundamental-cycle identity of RAINBOW.md Lemma X2 on every move of every rainbow tree.
    python .../exp_structure.py loads 12
        the set L of load vectors: exchange axiom towards the all-ones vector, full M-convexity.
    python .../exp_structure.py potential 12
        candidate secondary potentials for a strictly monotone descent.
    python .../exp_structure.py replicate
        the exact instance sets of the refereed report (826 and 166 rooted instances); uses
        workings/barnette_lab only to read off which face it calls 'outer'.
"""
import json
import sys
from collections import Counter, deque
from pathlib import Path

import etri
from rainbow import RB

DATA = Path(__file__).resolve().parents[1] / 'data'


def save(name, obj):
    DATA.mkdir(exist_ok=True)
    obj = {'command': 'python research/2026-11-14_fable_referee-topology/code/exp_structure.py ' + ' '.join(sys.argv[1:]),
           'result': obj}
    (DATA / f'{name}.json').write_text(json.dumps(obj, indent=1))
    print(json.dumps(obj['result'], indent=1)[:4000])


def tree_adj(I, sigma):
    """Adjacency of F = H - S. Nodes ('v', x) and ('t', t)."""
    adj = {}
    for t in range(len(I.faces)):
        if not I.black[t]:
            continue
        for v in I.faces[t]:
            if sigma.get(v) == t:
                continue
            adj.setdefault(('t', t), []).append(('v', v))
            adj.setdefault(('v', v), []).append(('t', t))
    return adj


def path(adj, a, b):
    prev = {a: None}
    dq = deque([a])
    while dq:
        p = dq.popleft()
        if p == b:
            break
        for q in adj.get(p, []):
            if q not in prev:
                prev[q] = p
                dq.append(q)
    out = [b]
    while prev[out[-1]] is not None:
        out.append(prev[out[-1]])
    return out[::-1]


def exp_identity(vmax):
    cnt = Counter()
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        rb = RB(I)
        trees = rb.all_trees()
        if not trees:
            continue
        cnt['instances'] += 1
        step = max(1, len(trees) // 60)
        for s in trees[::step]:
            sigma = dict(zip(rb.X, s))
            load = rb.load(sigma)
            adj = tree_adj(I, sigma)
            for x in rb.X:
                t = sigma[x]
                p = path(adj, ('t', t), ('v', x))
                tprime = p[-2][1]
                (t2,) = rb.move_target(sigma, x)
                cnt['moves'] += 1
                cnt['primal_dual_target_agree'] += (tprime == t2)
                cyc = [x] + [node[1] for node in p if node[0] == 'v'][:-1]
                assert len(cyc) == len(set(cyc)) and len(cyc) >= 3
                ins = set(I.inside_faces(cyc))
                B = sum(1 for f in ins if I.black[f])
                W = len(ins) - B
                surplus = sum(load[f] - 1 for f in ins if I.black[f])
                cnt['identity_ok'] += (surplus == W - B - 1 + (1 if t in ins else 0))
                # after the move the same disk has surplus changed by [t' in D] - [t in D]
                d = load[t2] - (1 if True else 0)
                kind = (load[t], load[t2])
                cnt['move_kind_%d_%d' % kind] += 1
                cnt['W-B=%d,tin=%d,t2in=%d' % (W - B, t in ins, t2 in ins)] += 1
    save('identity_%d' % vmax, {'vmax': vmax, 'counts': dict(sorted(cnt.items()))})


def exp_loads(vmax):
    cnt = Counter()
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        rb = RB(I)
        trees = rb.all_trees()
        if not trees:
            continue
        cnt['instances'] += 1
        Aidx = {t: i for i, t in enumerate(I.A)}
        n = I.n
        L = set()
        for s in trees:
            c = [0] * n
            for t in s:
                c[Aidx[t]] += 1
            L.add(tuple(c))
        cnt['load_vectors'] += len(L)
        ones = tuple([1] * n)
        assert ones in L
        # exchange towards all-ones
        ok_all = True
        for c in L:
            for i in range(n):
                if c[i] == 2:
                    good = False
                    for j in range(n):
                        if c[j] == 0:
                            c2 = list(c)
                            c2[i] -= 1
                            c2[j] += 1
                            if tuple(c2) in L:
                                good = True
                                break
                    cnt['surplus_faces'] += 1
                    cnt['surplus_face_has_exchange'] += good
                    ok_all &= good
        cnt['instances_exchange_to_ones_ok'] += ok_all
        # full M-convexity (simultaneous exchange) on small sets
        if len(L) <= 400:
            Ls = sorted(L)
            mconv = True
            for c in Ls:
                for c2 in Ls:
                    for i in range(n):
                        if c[i] > c2[i]:
                            good = False
                            for j in range(n):
                                if c[j] < c2[j]:
                                    a = list(c)
                                    a[i] -= 1
                                    a[j] += 1
                                    b = list(c2)
                                    b[i] += 1
                                    b[j] -= 1
                                    if tuple(a) in L and tuple(b) in L:
                                        good = True
                                        break
                            if not good:
                                mconv = False
                                break
                    if not mconv:
                        break
                if not mconv:
                    break
            cnt['mconvex_tested'] += 1
            cnt['mconvex'] += mconv
    save('loads_%d' % vmax, {'vmax': vmax, 'counts': dict(cnt)})


def exp_potential(vmax):
    cnt = Counter()
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        rb = RB(I)
        trees = rb.all_trees()
        if not trees:
            continue
        cnt['instances'] += 1
        X = rb.X
        index = {s: i for i, s in enumerate(trees)}
        # static distances between black centres in H
        Hadj = tree_adj(I, {})

        def bfs(adj, srcs):
            dist = {a: 0 for a in srcs}
            dq = deque(srcs)
            while dq:
                p = dq.popleft()
                for q in adj.get(p, []):
                    if q not in dist:
                        dist[q] = dist[p] + 1
                        dq.append(q)
            return dist

        def pots(s):
            sigma = dict(zip(X, s))
            load = rb.load(sigma)
            two = [('t', t) for t in I.A if load[t] == 2]
            zero = [('t', t) for t in I.A if load[t] == 0]
            exc = 2 * len(two)
            if not two:
                return (0, 0, 0, 0, 0)
            adj = tree_adj(I, sigma)
            dF = bfs(adj, zero)
            dH = bfs(Hadj, zero)
            return (exc, min(dF[a] for a in two), sum(dF[a] for a in two), min(dH[a] for a in two), sum(dH[a] for a in two))

        P = [pots(s) for s in trees]
        for i, s in enumerate(trees):
            if P[i][0] == 0:
                continue
            cnt['trees_positive_excess'] += 1
            best = [False] * 4
            for j, x in enumerate(X):
                sigma = dict(zip(X, s))
                (t2,) = rb.move_target(sigma, x)
                k = index[s[:j] + (t2,) + s[j + 1:]]
                if P[k][0] > P[i][0]:
                    continue
                for q in range(4):
                    if (P[k][0], P[k][q + 1]) < (P[i][0], P[i][q + 1]):
                        best[q] = True
            for q, nm in enumerate(['minF', 'sumF', 'minH', 'sumH']):
                cnt['strict_descent_' + nm] += best[q]
    save('potential_%d' % vmax, {'vmax': vmax, 'counts': dict(cnt)})


def exp_replicate():
    sys.path.insert(0, str(etri.REPO / 'workings' / 'barnette_lab'))
    from barnette_lab.core import Instance, plantri_graphs  # only for the face numbering
    cnt = Counter()
    for V in range(6, 17):
        rots = etri.plantri(V)
        if not rots:
            continue
        labs = list(plantri_graphs(V, etri.PLANTRI))
        assert len(labs) == len(rots)
        for idx, (rot, g) in enumerate(zip(rots, labs)):
            tri = etri.Tri(rot)
            assert sorted(map(tuple, map(sorted, g.edges()))) == sorted(tri.edges())
            base = Instance(g)
            faces = list(range(len(base.faces)))
            two = [0, next(f for f in faces if f not in base.black)]
            for name, lim, sel in (('set826', 12, None), ('set166', 10, None)):
                if name == 'set166' and V > 14:
                    continue
                fs = faces if V <= lim else two
                for f in fs:
                    I = etri.Inst(tri, tri.face_by_vertices(base.faces[f]))
                    if name == 'set826':
                        rb = RB(I)
                        pair = I.has_pair_flow()
                        pr = rb.point_rainbow_tree() is not None
                        cnt['826_instances'] += 1
                        cnt['826_pair'] += pair
                        cnt['826_point_rainbow'] += pr
                        cnt['826_agree'] += (pair == pr)
                        cnt['826_face_rainbow'] += rb.face_rainbow_tree()
                    else:
                        cnt['166_instances'] += 1
                        sts = I.states()
                        tms = [s for s in sts if I.is_tree_matching(s)]
                        tset = set(tms)
                        cnt['166_with_tm'] += bool(tms)
                        cnt['166_states_with_mate'] += sum(1 for s in sts if I.n_unicyclic(s) is not None)
                        for s in tms:
                            cnt['166_tree_matchings'] += 1
                            (r,) = I.mates(s)
                            cnt['166_mate_not_tm'] += (r not in tset)
    save('replicate', {'counts': dict(cnt)})


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'identity':
        exp_identity(int(sys.argv[2]))
    elif cmd == 'loads':
        exp_loads(int(sys.argv[2]))
    elif cmd == 'potential':
        exp_potential(int(sys.argv[2]))
    elif cmd == 'replicate':
        exp_replicate()
