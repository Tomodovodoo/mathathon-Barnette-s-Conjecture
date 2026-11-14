"""Compute every number quoted in digestions/steps/.  Output: ../data/examples.json and a text log.

Run from the repository root:
    python research/2026-11-14_fable_digestions/code/examples.py
"""
import json
import os
import sys
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from dig import Tri, summary  # noqa: E402

OUT = {}
LOG = []


def log(*a):
    line = ' '.join(str(x) for x in a)
    LOG.append(line)
    print(line)


def load(name):
    d = json.load(open(os.path.join(ROOT, 'paper', 'figures', name + '.json')))
    return Tri(d['faces'], d['t0']), d


def describe(T, name, e0=None, full=True):
    info, ss, ps, tms, covers = summary(T)
    log(f'== {name}: |V(T)|={len(T.V)} faces={len(T.faces)} n={T.n}')
    log('   t0 =', T.t0, T.faces[T.t0], 'roots', T.R, 'X', T.X)
    log('   A =', [(t, T.faces[t]) for t in T.A])
    log('   white =', [(w, T.faces[w]) for w in T.white])
    log('  ', info)
    kap = T.kappa()
    a = T.spoke_weights(kap)
    rec = {'info': info, 'faces': T.faces, 't0': T.t0, 'A': T.A, 'X': T.X, 'white': T.white, 'states': []}
    for s in ss:
        q = T.q_info(s)
        partners = T.partners(s, ss)
        h = T.heights(s, kap)
        row = {'s': s, 'partners': partners, 'q_cycles': q['cycles'], 'roots_per_component': q['roots_per_component'],
               'tree_matching': q['rooted_forest'], 'omega': sum(h.values()), 'heights': h,
               'coefficient_in_F': sum(T.eps(r, s) for r in partners)}
        rec['states'].append(row)
        if full:
            log('   state', s, 'partners', len(partners), 'Qcycles', q['cycles'], 'roots/comp', q['roots_per_component'],
                'TM' if q['rooted_forest'] else '--', 'omega', row['omega'], 'coef', row['coefficient_in_F'])
    rec['covers'] = []
    for key, plist in covers.items():
        r, s = plist[0]
        cyc = T.dcycles(r, s)
        disks = []
        for c in cyc:
            d = T.disk(c)
            if not d['ccw']:
                d = T.disk(tuple(reversed(c)))
            assert d['ccw'] and d['delta_sum'] == -3 and d['W'] == d['B'] + 1 and d['h'] - 2 * d['l'] == 3
            assert d['B'] == d['I'] + d['l']
            disks.append(d)
        prs = []
        for r, s in plist:
            flags = [T.disk(c)['ccw'] for c in T.dcycles(r, s)]
            assert T.J(r, s) == sum(1 for f in flags if not f) - sum(1 for f in flags if f)
            assert T.eps(r, s) == (-1) ** ((T.n + T.J(r, s)) // 2)
            prs.append({'r': r, 's': s, 'J': T.J(r, s), 'eps': T.eps(r, s), 'ccw_cycles': sum(flags),
                        'forest_pair': T.is_tree_matching(s), 'omega_s': sum(T.heights(s, kap).values())})
        rec['covers'].append({'cycles': disks, 'pairs': prs})
        if full:
            log('   cover with', len(cyc), 'cycles:')
            for d in disks:
                log('      ccw cycle', d['cycle'], 'h', d['h'], 'l', d['l'], 'B', d['B'], 'W', d['W'], 'I', d['I'],
                    'white inside', d['white_inside'])
            for p in prs:
                log('      pair r', p['r'], 's', p['s'], 'J', p['J'], 'eps', p['eps'], 'ccw', p['ccw_cycles'],
                    'forest' if p['forest_pair'] else 'cyclic', 'omega', p['omega_s'])
    # height lemma: reversing a clockwise cycle to counterclockwise raises h by the indicator of the inside
    for r, s in ps:
        for c in T.dcycles(r, s):
            d = T.disk(c)
            r2, s2 = T.reverse_d(r, s, c)
            h1, h2 = T.heights(s, kap), T.heights(s2, kap)
            sign = -1 if d['ccw'] else 1          # after reversal the cycle is ccw iff it was cw
            for w in h1:
                assert h2[w] - h1[w] == sign * (w in d['white_inside']), (name, c, w)
    # polynomial F(1 + x a): coefficients in x
    poly = {}
    for r, s in ps:
        p = [Fraction(T.eps(r, s))]
        for t, v in zip(T.A, s):
            av = a.get((t, v), 0)
            q = [Fraction(0)] * (len(p) + 1)
            for i, c in enumerate(p):
                q[i] += c
                q[i + 1] += c * av
            p = q
        for i, c in enumerate(p):
            poly[i] = poly.get(i, 0) + c
    rec['P_coefficients'] = {i: int(c) for i, c in sorted(poly.items()) if c}
    rec['spoke_weights'] = {f'{t},{v}': val for (t, v), val in sorted(a.items()) if val}
    log('   P(x) = F(1 + x a), nonzero coefficients by degree:', rec['P_coefficients'])
    # signed moments of omega over tree matchings
    cmin = min(info['covers_by_cycle_count']) if info['covers_by_cycle_count'] else None
    rec['cmin'] = cmin
    OUT[name] = rec
    return rec, ss, ps, tms, covers, kap


def cube_two_factors(T):
    tf = T.two_factors()
    hist = {}
    for m, c in tf:
        hist[c] = hist.get(c, 0) + 1
    log('   2-factors of G by number of cycles:', dict(sorted(hist.items())), 'total', len(tf))
    return hist, tf


def main():
    # ---- octahedron / cube -------------------------------------------------
    T, d = load('octahedron')
    rec, ss, ps, tms, covers, kap = describe(T, 'octahedron')
    hist, tf = cube_two_factors(T)
    rec['two_factors_by_cycles'] = hist
    rec['G_edges'] = T.G_edges()
    rec['two_factors'] = [{'omitted_matching': m, 'cycles': c} for m, c in tf]
    for s in tms:
        for e0 in [(a, b) for a, b in combinations(T.R, 2)]:
            out = T.recover(s, e0)
            log('   recover s', s, 'e0', e0, 'y0', out['y0'], 'tree', out['white_tree'], 'P', out['P'],
                'classes', out['classes'], 'cycle', out['cycle'])
            rec.setdefault('recover', []).append({'s': s, 'e0': e0, **out})
    # zero weights: Z(x) = sum i^J = 0
    log('   J values of the pairs:', [T.J(r, s) for r, s in ps])

    # ---- hexagonal prism dual (8 vertices): double wheel with rim 6 -----------
    faces = []
    for i in range(6):
        j = (i + 1) % 6
        faces.append((6, i, j))       # top apex 6
        faces.append((7, j, i))       # bottom apex 7
    Tp = Tri(faces, 0)
    rec, ss, ps, tms, covers, kap = describe(Tp, 'prism')
    hist, tf = cube_two_factors(Tp)
    rec['two_factors_by_cycles'] = hist
    for e0 in combinations(Tp.R, 2):
        e0d = tuple(sorted((Tp.left[e0[0], e0[1]], Tp.left[e0[1], e0[0]])))
        avoiding = [m for m, c in tf if c == 1 and e0d in m]
        rec.setdefault('avoiding', []).append({'e0': e0, 'hamiltonian_cycles_avoiding_dual_of_e0': len(avoiding),
                                               'tree_matchings': len(tms)})
        log('   e0', e0, 'Hamiltonian cycles avoiding e0*:', len(avoiding), 'tree matchings:', len(tms))

    # ---- running example (13 vertices) --------------------------------------
    T, d = load('running')
    rec, ss, ps, tms, covers, kap = describe(T, 'running')
    hist, tf = cube_two_factors(T)
    rec['two_factors_by_cycles'] = hist
    e0 = tuple(d['e0'])
    for s in tms:
        out = T.recover(s, e0)
        rec.setdefault('recover', []).append({'s': s, 'e0': e0, **out})
        log('   recover s', s, 'y0', out['y0'], 'classes', out['classes'])
        log('       P', out['P'])
        log('       cycle', out['cycle'])
    e0d = tuple(sorted((T.left[e0[0], e0[1]], T.left[e0[1], e0[0]])))
    avoiding = [m for m, c in tf if c == 1 and e0d in m]
    rec['hamiltonian_cycles'] = hist.get(1, 0)
    rec['hamiltonian_cycles_avoiding_dual_of_e0'] = len(avoiding)
    log('   Hamiltonian cycles of G:', hist.get(1, 0), ' avoiding e0*:', len(avoiding), ' tree matchings:', len(tms))
    # signed moments of the heights (Theorem B) on the running example
    ws = sorted(kap)
    eps_tm = {}
    for r, s in ps:
        if T.is_tree_matching(s):
            eps_tm[s] = T.eps(r, s)
    for j in (0, 1, 2):
        tot = sum(e * sum(T.heights(s, kap).values()) ** j for s, e in eps_tm.items())
        log(f'   sum over tree matchings of eps * omega^{j} =', tot)
        rec.setdefault('omega_moments', {})[j] = tot
    mom = {}
    for w1 in ws:
        for w2 in ws:
            mom[f'{w1},{w2}'] = sum(e * T.heights(s, kap)[w1] * T.heights(s, kap)[w2] for s, e in eps_tm.items())
    rec['height_moments_degree_2'] = {k: v for k, v in mom.items() if v}
    log('   nonzero degree-2 height moments (w1,w2 -> value):', rec['height_moments_degree_2'])

    # ---- 9 vertices: octahedron glued into a face of an octahedron -----------------
    octa = [(0, 2, 1), (0, 1, 5), (1, 2, 3), (2, 0, 4), (1, 3, 5), (2, 4, 3), (0, 5, 4), (3, 4, 5)]
    # replace the face (3,4,5) by an octahedron with new vertices 6,7,8: 6 opposite 3, 7 opposite 4, 8 opposite 5
    inner = [(3, 4, 8), (4, 5, 6), (5, 3, 7), (3, 8, 7), (4, 6, 8), (5, 7, 6), (6, 7, 8)]
    faces9 = octa[:-1] + inner
    rows = []
    for t0 in range(len(faces9)):
        T9 = Tri(faces9, t0)
        info, ss9, ps9, tms9, cov9 = summary(T9)
        ins, _ = T9.inside((3, 4, 5))
        # which side of the separating triangle is t0 on, and the colour of the faces along it on the other side
        if t0 in ins:
            ins = [f for f in range(len(faces9)) if f not in ins]
        along = [f for f in ins if len(set(faces9[f]) & {3, 4, 5}) == 2]
        black_inner = all(f in T9.black for f in along)
        rows.append({'t0': t0, 'face': faces9[t0], 'states': info['states'], 'pairs': info['pairs'],
                     'tree_matchings': info['tree_matchings'], 'covers': info['covers_by_cycle_count'],
                     'black_inner_boundary': black_inner})
        log('   9-vertex, t0 =', t0, faces9[t0], info, 'black inner boundary:', black_inner)
        assert (info['pairs'] > 0) == (not black_inner)
    OUT['double_octahedron'] = {'faces': faces9, 'separating_triangle': [3, 4, 5], 'rootings': rows}

    # ---- 12 vertices, class 6: an extremal state that is not a tree matching -----------
    f12 = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 4, 5), (1, 5, 2), (2, 5, 6), (2, 6, 7), (2, 7, 3), (3, 7, 8),
           (3, 8, 9), (3, 9, 4), (4, 9, 10), (4, 10, 5), (5, 10, 11), (5, 11, 6), (6, 11, 7), (7, 10, 8), (7, 11, 10), (8, 10, 9)]
    for orient, fs in (('as listed', f12), ('mirror', [tuple(reversed(f)) for f in f12])):
        T12 = Tri(fs, 8)
        rec, ss, ps, tms, covers, kap = describe(T12, 'v12_class6_' + orient.replace(' ', '_'), full=False)
        partnered = sorted({s for _, s in ps}, key=lambda s: sum(T12.heights(s, kap).values()))
        lo, hi = partnered[0], partnered[-1]
        om = lambda s: sum(T12.heights(s, kap).values())
        log('   ', orient, 'omega of partnered states:', [(om(s), 'TM' if T12.is_tree_matching(s) else 'cyclic') for s in partnered])
        rec['partnered_by_omega'] = [(om(s), T12.is_tree_matching(s)) for s in partnered]
        mincov = [v for v in covers.values() if len(T12.dcycles(*v[0])) == rec['cmin']]
        for v in mincov:
            for r, s in v:
                flags = [T12.disk(c)['ccw'] for c in T12.dcycles(r, s)]
                if all(flags) or not any(flags):
                    log('    minimal cover, all', 'ccw' if all(flags) else 'cw', '-> forest pair:', T12.is_tree_matching(s))
                    rec.setdefault('minimal_cover_orientations', []).append({'all_ccw': all(flags), 'forest_pair': T12.is_tree_matching(s)})

    # ---- 16 vertices, class 158: a cycle cover none of whose orientations is a forest pair ------
    f16 = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 4, 5), (1, 5, 2), (2, 5, 6), (2, 6, 7), (2, 7, 3), (3, 7, 8),
           (3, 8, 9), (3, 9, 4), (4, 9, 10), (4, 10, 5), (5, 10, 11), (5, 11, 6), (6, 11, 7), (7, 11, 12), (7, 12, 13),
           (7, 13, 14), (7, 14, 8), (8, 14, 9), (9, 13, 10), (9, 14, 13), (10, 13, 15), (10, 15, 11), (11, 15, 12), (12, 15, 13)]
    T16 = Tri(f16, 8)
    rec, ss, ps, tms, covers, kap = describe(T16, 'v16_class158', full=False)
    bad = []
    for key, plist in covers.items():
        good = [T16.is_tree_matching(s) for _, s in plist]
        cyc = T16.dcycles(*plist[0])
        log('   cover with', len(cyc), 'cycles, lengths', [len(c) for c in cyc], 'pairs', len(plist), 'forest pairs', sum(good))
        if not any(good):
            for r, s in plist:
                q = T16.Q(s)
                log('      no forest pair: s =', s, 'Q_s cycles', T16.q_info(s)['cycles'])
            bad.append({'cycles': [list(c) for c in cyc], 'pairs': [{'r': r, 's': s} for r, s in plist]})
    rec['covers_without_forest_pair'] = bad
    assert len(bad) == 1

    # ---- relaxing bijectivity: the 9-vertex witness of astra_limits -----------------------------
    dnb = json.load(open(os.path.join(ROOT, 'research', '2026-11-14_astra_limits', 'examples', 'nonbijective_disk.json')))
    for fs in (dnb['faces'], [list(reversed(f)) for f in dnb['faces']]):
        Tn = Tri(fs, dnb['outer'])
        asg = {int(k): v for k, v in dnb['assignment'].items()}
        cyc = tuple(dnb['cycle'])
        ok = all(Tn.blackface(a, b) in asg and asg[Tn.blackface(a, b)] == a for a, b in zip(cyc, cyc[1:] + cyc[:1]))
        dk = Tn.disk(cyc)
        log('   non-bijective choice: edges leave the chosen corners:', ok, 'disk', {k: dk[k] for k in ('ccw', 'h', 'l', 'B', 'W', 'I', 'delta_sum')})
        if dk['ccw']:
            OUT['nonbijective_disk'] = {'faces': fs, 'outer': dnb['outer'], 'assignment': asg, 'disk': dk, 'edges_leave_chosen_corners': ok}

    os.makedirs(os.path.join(HERE, '..', 'data'), exist_ok=True)
    with open(os.path.join(HERE, '..', 'data', 'examples.json'), 'w') as f:
        json.dump(OUT, f, indent=1, default=str)
    with open(os.path.join(HERE, '..', 'data', 'examples.log'), 'w') as f:
        f.write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
