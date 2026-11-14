"""T-side packing (PROOFS Theorem 2.7): for a deleted-corner map u, the edges of T other than
those of t0 and the edges opposite u(t) split into two spanning trees of T/R (roots merged).
Checks every pair support and RANDOM random maps on every rooting of plantri orders VMIN..VMAX.
Usage: python tside.py VMIN VMAX RANDOM SEED   (writes data/tside_V<a>-<b>.json)"""
import json, sys, random
from pathlib import Path
from tp import Tri, Rooted, plantri, two_tree_partition

OUT = Path(__file__).resolve().parents[1] / 'data'


def tside_edges(inst, u):
    F = inst.tri.faces
    lab = {}
    for v in range(inst.tri.V):
        lab[v] = 0 if v in inst.R else 1 + inst.X.index(v)
    es = []
    for t, d in zip(inst.A, u):
        a, b, c = F[t]
        for x, y in ((a, b), (b, c), (c, a)):
            if d not in (x, y):
                continue  # this is the edge opposite d: excluded
            es.append((lab[x], lab[y]))
    return es


def main():
    a, b, nr, seed = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    summ = {}
    for V in range(a, b + 1):
        S = summ.setdefault(V, {'supports': 0, 'support_fail': 0, 'random_with_pair': 0, 'random_fail_with_pair': 0,
                                'random_no_pair': 0, 'random_fail_no_pair': 0})
        for rot in plantri(V):
            tri = Tri(rot)
            for f in range(len(tri.faces)):
                inst = Rooted(tri, f)
                us = inst.two_factors()
                m = inst.n + 1
                for u in us:
                    S['supports'] += 1
                    S['support_fail'] += two_tree_partition(m, tside_edges(inst, u)) is None
                key = 'with_pair' if us else 'no_pair'
                for _ in range(nr):
                    u = [rng.choice(list(tri.faces[t])) for t in inst.A]
                    S['random_' + key] += 1
                    S['random_fail_' + key] += two_tree_partition(m, tside_edges(inst, u)) is None
        print(V, S, flush=True)
    (OUT / f'tside_V{a}-{b}.json').write_text(json.dumps({'command': 'python code/tside.py ' + ' '.join(sys.argv[1:]),
                                                         'summary': summ}, indent=1))


if __name__ == '__main__':
    main()
