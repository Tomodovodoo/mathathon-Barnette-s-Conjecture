"""Survey of all rooted Eulerian triangulations with at most VMAX vertices.

usage: python survey.py VMAX [out.json]

For every isomorphism class T and every face t0 it runs analyze() (which asserts the
proved identities) and then tests the extremal candidates and the counting
conjectures listed in ROUTES.md.  Prints one summary line per class and a tally.
"""
import sys, json, time
from collections import defaultdict
from tri import enumerate_classes, from_code
from rooted import Rooted, dual_ham_cycles
from analyze import analyze, tree_to_cycle, cycle_to_state


def survey(vmax, vmin=6):
    L = enumerate_classes(vmax)
    tally = defaultdict(int)
    examples = {}
    rows = []

    def note(name, ok, ex):
        tally[name + (':yes' if ok else ':no')] += 1
        if not ok and name not in examples:
            examples[name] = ex

    for v in range(vmin, vmax + 1):
        for ci, code in enumerate(L[v]):
            T = from_code(code)
            hams = dual_ham_cycles(T)
            nsep = len(T.separating_triangles())
            for t0 in range(T.F):
                R = Rooted(T, t0)
                res, ex = analyze(R, deep=(v <= 12))
                row = dict(V=v, cls=ci, t0=t0, sep=nsep, hams=len(hams), **res)
                tag = (v, ci, t0)
                # Hamiltonian cycles avoiding each edge of t0
                a, b, c = T.faces[t0]
                hc = []
                for e0 in ((a, b), (b, c), (c, a)):
                    fe = frozenset(e0)
                    hc.append(sum(1 for H in hams if fe not in H))
                row['hc_avoid'] = hc
                if ex is None:
                    rows.append(row)
                    tally['rooted_without_pair'] += 1
                    continue
                tally['rooted_with_pair'] += 1
                st, info, partnered, trees = ex['st'], ex['info'], ex['partnered'], ex['trees']
                om, pairs, Dinfo, mu = ex['om'], ex['pairs'], ex['Dinfo'], ex['mu']
                treeset = set(trees)
                m = res['cmin']
                # --- E1: extreme partnered states are tree matchings
                mx = max(om[s] for s in partnered)
                mn = min(om[s] for s in partnered)
                note('E1 every max-rank partnered state is a tree matching',
                     all(s in treeset for s in partnered if om[s] == mx), tag)
                note('E1b some max-rank partnered state is a tree matching',
                     any(s in treeset for s in partnered if om[s] == mx), tag)
                note('E1c every min-rank partnered state is a tree matching',
                     all(s in treeset for s in partnered if om[s] == mn), tag)
                # --- E2: all-ccw / all-cw orientation of a minimal D is a tree pair
                byD = defaultdict(list)
                for p in pairs:
                    byD[p[4]].append(p)
                okccw = okcw = okany = True
                someccw = False
                everyD = True
                for Dk, ps in byD.items():
                    hit = any(p[1] in treeset for p in ps)
                    everyD &= hit
                    if len(Dinfo[Dk]) == m:
                        for p in ps:
                            if all(p[5]):
                                okccw &= p[1] in treeset
                                someccw |= p[1] in treeset
                            if not any(p[5]):
                                okcw &= p[1] in treeset
                        okany &= hit
                note('E2 minimal D, all ccw => Q_s forest', okccw, tag)
                note('E2b some minimal D has its all-ccw pair a forest pair', someccw, tag)
                note('E2c minimal D, all cw => Q_s forest', okcw, tag)
                note('E2d every minimal D contains a forest pair', okany, tag)
                note('E3 every D contains a forest pair', everyD, tag)
                # --- E4: lattice top / bottom
                top = max(om[s] for s in st)
                tops = [s for s in st if om[s] == top]
                note('E4 top state of the lattice is unique', len(tops) == 1, tag)
                note('E4b top state has a partner', all(info[s][0] for s in tops), tag)
                # --- E5: pair maximising omega(s) - omega(r)
                best = max(om[p[1]] - om[p[0]] for p in pairs)
                note('E5 pairs maximising rank(s)-rank(r) are forest pairs',
                     all(p[1] in treeset for p in pairs if om[p[1]] - om[p[0]] == best), tag)
                note('E5b ... and their first state is a tree matching too',
                     all(p[0] in treeset for p in pairs if om[p[1]] - om[p[0]] == best), tag)
                # --- E6: sign versus parity of rank
                par = {mu[s] * (-1) ** (om[s] % 2) for s in trees}
                note('E6 sign of a tree matching is (-1)^rank up to a constant', len(par) == 1, tag)
                # --- E7: counts
                note('E7 trees >= 2^cmin', res['trees'] >= 2 ** m, tag)
                note('E7b trees == 2^cmin', res['trees'] == 2 ** m, tag)
                note('E7c cmin == 1', m == 1, tag)
                # --- E8: map to Hamiltonian cycles
                for e0, cnt in zip(((a, b), (b, c), (c, a)), hc):
                    img = set()
                    for s in trees:
                        P = tree_to_cycle(R, s, e0)
                        assert P is not None
                        alledges = {frozenset(e) for e in T.de}
                        H = frozenset(alledges - P)
                        assert H in hams and frozenset(e0) not in H
                        assert H not in img, "map tree matching -> cycle not injective"
                        img.add(H)
                        s2 = cycle_to_state(R, P, e0)
                        assert s2 == s
                    note('E8 every Hamiltonian cycle avoiding e0 comes from a tree matching',
                         len(img) == cnt, tag + (e0,))
                    # which cycles are missed, and do they give states?
                    for H in hams:
                        if frozenset(e0) in H or H in img:
                            continue
                        P = frozenset({frozenset(e) for e in T.de} - H)
                        s2 = cycle_to_state(R, P, e0)
                        note('E8b a missed cycle still gives a state', s2 is not None, tag + (e0,))
                        if s2 is not None:
                            assert s2 not in treeset
                            note('E8c ... and that state has a partner', info[s2][0], tag + (e0,))
                row['img'] = len(trees)
                rows.append(row)
    return rows, dict(tally), examples


if __name__ == '__main__':
    vmax = int(sys.argv[1])
    t = time.time()
    rows, tally, examples = survey(vmax)
    for k in sorted(tally):
        print(f"{tally[k]:7d}  {k}")
    print("first counterexamples (V, class, t0[, e0]):")
    for k, v in examples.items():
        print("   ", k, v)
    print("time", round(time.time() - t, 1))
    if len(sys.argv) > 2:
        json.dump(rows, open(sys.argv[2], 'w'))
