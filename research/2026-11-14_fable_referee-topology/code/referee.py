"""Independent checks of claims (a)-(d), (g), (h) of research/2026-11-14_opus_route-topology.

Usage (from the repository root):
    python research/2026-11-14_fable_referee-topology/code/referee.py angles 12
    python research/2026-11-14_fable_referee-topology/code/referee.py retract 14
    python research/2026-11-14_fable_referee-topology/code/referee.py morse 12
    python research/2026-11-14_fable_referee-topology/code/referee.py mate 14
    python research/2026-11-14_fable_referee-topology/code/referee.py height 12
Each writes data/ref_<name>.json. Uses etri.py only (own implementation).
"""
import json
import random
import sys
from collections import Counter, deque
from pathlib import Path

import etri

DATA = Path(__file__).resolve().parents[1] / 'data'


def save(name, obj):
    DATA.mkdir(exist_ok=True)
    obj = {'command': 'python research/2026-11-14_fable_referee-topology/code/referee.py ' + ' '.join(sys.argv[1:]),
           'result': obj}
    (DATA / f'ref_{name}.json').write_text(json.dumps(obj, indent=1))
    print(json.dumps(obj['result'], indent=1)[:3000])


# ------------------------------------------------------------------ angle structure
def corner_angle(I, s_face_of_vertex, f, v):
    """Angle in units of pi/3 at corner v of face f, for the state given by vertex -> matched face."""
    if not I.black[f]:
        return 1
    if f == I.f0:
        return -1
    return 5 if s_face_of_vertex.get(v) == f else -1


def left_faces(I, u, v, w):
    """Faces at v on the left of the path u -> v -> w, from the outgoing edge round to the incoming one."""
    rot = I.tri.rot[v]
    pos = I.tri.pos[v]
    d = len(rot)
    out = []
    i = pos[w]
    stop = pos[u]
    while i != stop:
        out.append(I.face_of[(v, rot[i])])
        i = (i - 1) % d
    return out


def cycles_of_chosen_edges(I, r, rng):
    """One out-edge per face t from r(t); return the directed cycles of the functional graph."""
    nxt = {}
    for i, t in enumerate(I.A):
        others = [x for x in I.faces[t] if x != r[i]]
        nxt[r[i]] = rng.choice(others)
    seen = {}
    out = []
    for v0 in nxt:
        path = []
        v = v0
        while v in nxt and v not in seen:
            seen[v] = v0
            path.append(v)
            v = nxt[v]
        if v in nxt and seen.get(v) == v0 and v in path:
            out.append(path[path.index(v):])
    return out


def exp_angles(vmax):
    rng = random.Random(20261114)
    cnt = Counter()
    fails = []
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        cnt['instances'] += 1
        states = I.states()
        if not states:
            cnt['no_state'] += 1
            continue
        for _ in range(80):
            s = rng.choice(states)
            m = {s[i]: t for i, t in enumerate(I.A)}
            # Lemma 2.1: face sums and vertex sums
            for f in range(len(I.faces)):
                tot = sum(corner_angle(I, m, f, v) for v in I.faces[f])
                cnt['face_sum_checked'] += 1
                if tot != (-3 if f == f0 else 3):
                    fails.append(('face', V, idx, f0, f))
            for v in range(I.nv):
                tot = sum(corner_angle(I, m, I.face_of[(v, y)], v) for y in I.tri.rot[v])
                cnt['vertex_sum_checked'] += 1
                want = 6 if v not in I.Rset else None
                if want is not None and tot != want:
                    fails.append(('vertex', V, idx, f0, v))
                if v in I.Rset:
                    cnt['root_angle_%d' % (tot - len(I.tri.rot[v]) // 2 + len(I.tri.rot[v]) // 2)] += 0
            # chosen-edge cycles of this state
            for cyc in cycles_of_chosen_edges(I, s, rng):
                h = len(cyc)
                cnt['chosen_cycles'] += 1
                d3 = sum(I.delta(cyc[i], cyc[(i + 1) % h]) for i in range(h))
                eps_sum = 0
                ok_local = True
                for i in range(h):
                    u, v, w = cyc[i - 1], cyc[i], cyc[(i + 1) % h]
                    lf = left_faces(I, u, v, w)
                    theta = sum(corner_angle(I, m, f, v) for f in lf)
                    eps = 3 - theta
                    din, dout = I.delta(u, v), I.delta(v, w)
                    if 2 * eps != (din + dout) - 6 * dout:
                        ok_local = False
                    eps_sum += eps
                cnt['local_identity_ok'] += ok_local
                cnt['turning_equals_minus2delta'] += (eps_sum == -2 * d3)
                ins = I.inside_faces(cyc)
                insset = set(ins)
                B = sum(1 for f in ins if I.black[f])
                W = len(ins) - B
                ccw = I.face_of[(cyc[0], cyc[1])] in insset
                cnt['W_eq_B_plus_1'] += (W == B + 1)
                cnt['delta_sum_pm3'] += (d3 == (-3 if ccw else 3))
                cnt['rotation_pm1'] += (eps_sum == (6 if ccw else -6))
                cnt['ccw' if ccw else 'cw'] += 1
                # Gauss-Bonnet on the disk from actual angle sums
                onb = set(cyc)
                tot = 0
                verts = set()
                for f in ins:
                    verts.update(I.faces[f])
                for v in verts:
                    th = sum(corner_angle(I, m, f, v) for f in ins if v in I.faces[f])
                    tot += (3 - th) if v in onb else (6 - th)
                cnt['gauss_bonnet_ok'] += (tot == 6)
                if not (ok_local and eps_sum == -2 * d3 and W == B + 1 and tot == 6):
                    fails.append(('cycle', V, idx, f0, cyc))
            # general cycles: chosen-edge cycles of another state r2, measured against s (claim 2.5)
            r2 = rng.choice(states)
            for cyc in cycles_of_chosen_edges(I, r2, rng):
                h = len(cyc)
                ins = set(I.inside_faces(cyc))
                B = sum(1 for f in ins if I.black[f])
                W = len(ins) - B
                mm = sum(1 for v in cyc if m[v] in ins)
                cnt['general_cycles'] += 1
                cnt['general_formula_ok'] += (B - W == 2 * mm - h + 2)
        # links of non-root vertices as generic cycles
        s = rng.choice(states)
        m = {s[i]: t for i, t in enumerate(I.A)}
        for v in I.X:
            link = list(I.tri.rot[v])
            if any(x in I.Rset for x in link):
                continue
            ins = set(I.inside_faces(link))
            if I.face_of[(v, link[0])] not in ins:
                continue  # link bounds the other side
            B = sum(1 for f in ins if I.black[f])
            W = len(ins) - B
            mm = sum(1 for x in link if m[x] in ins)
            cnt['link_cycles'] += 1
            cnt['link_formula_ok'] += (B - W == 2 * mm - len(link) + 2)
    save('angles', {'vmax': vmax, 'counts': dict(cnt), 'failures': fails[:20]})


# ------------------------------------------------------------------ retraction lemma
def random_face_matching(I, rng):
    """Random perfect matching of the dual graph: one selected edge in every face."""
    nf = len(I.faces)
    blacks = [f for f in range(nf) if I.black[f]]
    rng.shuffle(blacks)
    mate = {}

    def nbrs(f):
        a, b, c = I.faces[f]
        L = [((a, b), I.face_of[(b, a)]), ((b, c), I.face_of[(c, b)]), ((c, a), I.face_of[(a, c)])]
        rng.shuffle(L)
        return L

    def aug(f, seen):
        for e, g in nbrs(f):
            if g in seen:
                continue
            seen.add(g)
            if g not in mate or aug(mate[g][0], seen):
                mate[g] = (f, e)
                return True
        return False

    for f in blacks:
        if not aug(f, set()):
            return None
    return [tuple(sorted(e)) for (f, e) in mate.values()]


def exp_retract(vmax):
    rng = random.Random(7)
    cnt = Counter()
    hist = Counter()
    for V, idx, f0, I in etri.all_rooted(6, vmax, roots=lambda tri: [0]):
        for _ in range(60):
            P = random_face_matching(I, rng)
            if P is None:
                cnt['no_matching'] += 1
                continue
            Pset = set(P)
            nf = len(I.faces)
            # cycles of the 2-factor: faces joined across unselected edges
            par = list(range(nf))

            def find(x):
                while par[x] != x:
                    par[x] = par[par[x]]
                    x = par[x]
                return x

            for (u, v) in I.tri.edges():
                if (u, v) not in Pset:
                    par[find(I.face_of[(u, v)])] = find(I.face_of[(v, u)])
            c = len({find(f) for f in range(nf)})
            pv = list(range(I.nv))

            def findv(x):
                while pv[x] != x:
                    pv[x] = pv[pv[x]]
                    x = pv[x]
                return x

            for (u, v) in P:
                pv[findv(u)] = findv(v)
            b0 = len({findv(v) for v in range(I.nv)})
            b1 = len(P) - I.nv + b0
            cnt['samples'] += 1
            cnt['b0_eq_c_plus_1'] += (b0 == c + 1)
            cnt['b1_eq_c_minus_1'] += (b1 == c - 1)
            hist[c] += 1
            if c == 1:
                # inducedness: every edge inside a component is selected
                ok = all(((u, v) in Pset) == (findv(u) == findv(v)) for (u, v) in I.tri.edges())
                cnt['hamiltonian_samples'] += 1
                cnt['induced_ok'] += ok
    save('retract', {'vmax': vmax, 'counts': dict(cnt), 'cycles_histogram': dict(hist)})


# ------------------------------------------------------------------ cancellation structure
def q_cycle_orientations(I, r, s):
    """Number of clockwise cycles of Q_s when oriented r(t) -> u(t)."""
    nxt = {}
    for i, t in enumerate(I.A):
        u = [x for x in I.faces[t] if x != r[i] and x != s[i]][0]
        nxt[r[i]] = u
    seen = set()
    cw = ccw = 0
    for v0 in nxt:
        if v0 in seen:
            continue
        path = []
        v = v0
        while v in nxt and v not in seen:
            seen.add(v)
            path.append(v)
            v = nxt[v]
        if v in path:
            cyc = path[path.index(v):]
            ins = set(I.inside_faces(cyc))
            if I.face_of[(cyc[0], cyc[1])] in ins:
                ccw += 1
            else:
                cw += 1
    return ccw, cw


def exp_morse(vmax):
    from math import comb
    cnt = Counter()
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        cnt['instances'] += 1
        n = I.n
        total_sign = 0
        tree_pairs = 0
        npairs = 0
        for s in I.states():
            k = I.n_unicyclic(s)
            if k is None:
                cnt['states_without_mate'] += 1
                continue
            cnt['states_with_mate'] += 1
            ms = I.mates(s)
            cnt['mates_2k'] += (len(ms) == 2 ** k)
            cnt['mates_valid'] += all(len(set(r)) == n and all(a != b for a, b in zip(r, s)) for r in ms)
            lv = Counter()
            sign_s = 0
            jc = None
            ok_plus = ok_minus = True
            for r in ms:
                J3 = I.J3(r, s)
                assert J3 % 3 == 0 and (n + J3 // 3) % 2 == 0
                J = J3 // 3
                ccw, cw = q_cycle_orientations(I, r, s)
                assert ccw + cw == k
                lv[J] += 1
                sign_s += (-1) ** ((n + J) // 2)
                if cw == 0:
                    jc = J
            for r in ms:
                J = I.J3(r, s) // 3
                ccw, cw = q_cycle_orientations(I, r, s)
                ok_plus &= (J == jc + 2 * cw)
                ok_minus &= (J == jc - 2 * cw)
            cnt['J_eq_Jccw_plus_2cw'] += ok_plus
            cnt['J_eq_Jccw_minus_2cw'] += ok_minus
            js = sorted(lv)
            cnt['levels_binomial'] += (len(js) == k + 1 and all(lv[js[i]] == comb(k, i) for i in range(k + 1))
                                       and all(js[i + 1] - js[i] == 2 for i in range(k)))
            cnt['signed_sum_indicator'] += (abs(sign_s) == (1 if k == 0 else 0))
            cnt['tree_iff_k0'] += ((k == 0) == I.is_tree_matching(s))
            total_sign += sign_s
            npairs += len(ms)
            tree_pairs += (k == 0)
        cnt['pairs'] += npairs
        cnt['Z1_zero'] += (total_sign == 0)
        cnt['tree_pairs_even'] += (tree_pairs % 2 == 0)
    save('morse', {'vmax': vmax, 'counts': dict(cnt)})


# ------------------------------------------------------------------ mates of tree matchings
def exp_mate(vmax):
    cnt = Counter()
    ex = []
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        seps = len(I.tri.separating_triangles())
        tms = [s for s in I.states() if I.is_tree_matching(s)]
        if not tms:
            continue
        cnt['instances_with_tm'] += 1
        tset = set(tms)
        bad = 0
        for s in tms:
            cnt['tree_matchings'] += 1
            (r,) = I.mates(s)
            if r not in tset:
                bad += 1
                cnt['mate_not_tm'] += 1
                cnt['mate_not_tm_nosep' if seps == 0 else 'mate_not_tm_sep'] += 1
                kr = I.n_unicyclic(r)
                cnt['mate_k=%s' % kr] += 1
                if len(ex) < 12:
                    cyc_len = None
                    ex.append({'V': V, 'plantri_index': idx, 'outer_face_vertices': list(I.R), 'sep_triangles': seps,
                               's': dict(zip(map(str, I.A), s)), 'mate': dict(zip(map(str, I.A), r)), 'k_mate': kr,
                               'rot': I.tri.rot})
        cnt['instances_with_bad'] += (bad > 0)
    save('mate', {'vmax': vmax, 'counts': dict(cnt), 'examples': ex})


# ------------------------------------------------------------------ lattice height
def rel_cycles(I, r, s):
    nxt = {r[i]: s[i] for i in range(I.n) if r[i] != s[i]}
    seen = set()
    out = []
    for v0 in nxt:
        if v0 in seen:
            continue
        cyc = []
        v = v0
        while v not in seen:
            seen.add(v)
            cyc.append(v)
            v = nxt[v]
        out.append(cyc)
    return out


def signed_white_area(I, r, s):
    tot = 0
    for cyc in rel_cycles(I, r, s):
        ins = I.inside_faces(cyc)
        W = sum(1 for f in ins if not I.black[f])
        ccw = I.face_of[(cyc[0], cyc[1])] in set(ins)
        tot += W if ccw else -W
    return tot


def exp_height(vmax):
    rng = random.Random(3)
    cnt = Counter()
    for V, idx, f0, I in etri.all_rooted(6, vmax):
        states = I.states()
        if len(states) < 2:
            continue
        seps = I.tri.separating_triangles()
        tris = [tuple(f) for f in I.faces] + [tuple(t) for t in seps]
        tris = [t for t in tris if not any(x in I.Rset for x in t)]
        index = {s: i for i, s in enumerate(states)}
        Apos = {t: i for i, t in enumerate(I.A)}
        up = [[] for _ in states]
        nmoves = 0
        for s in states:
            inv = {s[i]: i for i in range(I.n)}
            for (a, b, c) in tris:
                for (p, q, r_) in ((a, b, c), (a, c, b)):
                    # p -> q -> r_ -> p : face of p takes q, face of q takes r_, face of r_ takes p
                    ip, iq, ir = inv[p], inv[q], inv[r_]
                    if q in I.faces[I.A[ip]] and r_ in I.faces[I.A[iq]] and p in I.faces[I.A[ir]]:
                        s2 = list(s)
                        s2[ip], s2[iq], s2[ir] = q, r_, p
                        s2 = tuple(s2)
                        area = signed_white_area(I, s, s2)
                        nmoves += 1
                        if area > 0:
                            up[index[s]].append((index[s2], area))
        # sources of the 'up' digraph
        indeg = [0] * len(states)
        for i in range(len(states)):
            for j, _ in up[i]:
                indeg[j] += 1
        src = [i for i in range(len(states)) if indeg[i] == 0]
        snk = [i for i in range(len(states)) if not up[i]]
        cnt['instances'] += 1
        cnt['one_source_one_sink'] += (len(src) == 1 and len(snk) == 1)
        # height = longest = shortest directed distance from the source if graded
        dist = {src[0]: 0}
        dq = deque([src[0]])
        graded = True
        while dq:
            i = dq.popleft()
            for j, _ in up[i]:
                if j not in dist:
                    dist[j] = dist[i] + 1
                    dq.append(j)
                elif dist[j] != dist[i] + 1:
                    graded = False
        cnt['connected'] += (len(dist) == len(states))
        cnt['graded_by_moves'] += graded
        key = 'nosep' if not seps else 'sep'
        cnt['instances_' + key] += 1
        unit = all(a == 1 for i in range(len(states)) for _, a in up[i])
        cnt['all_moves_area1_' + key] += unit
        pairs = [(rng.randrange(len(states)), rng.randrange(len(states))) for _ in range(40)]
        for i, j in pairs:
            if i == j or i not in dist or j not in dist:
                continue
            area = signed_white_area(I, states[i], states[j])
            cnt['pairs_' + key] += 1
            cnt['height_eq_area_' + key] += (dist[j] - dist[i] == area)
            # additivity through a third state
            k = rng.randrange(len(states))
            cnt['additive_' + key] += (signed_white_area(I, states[i], states[k]) + signed_white_area(I, states[k], states[j]) == area)
    save('height', {'vmax': vmax, 'counts': dict(cnt)})


if __name__ == '__main__':
    name = sys.argv[1]
    vmax = int(sys.argv[2])
    {'angles': exp_angles, 'retract': exp_retract, 'morse': exp_morse, 'mate': exp_mate, 'height': exp_height}[name](vmax)
