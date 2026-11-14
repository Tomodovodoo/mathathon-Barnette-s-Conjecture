"""Exhaustive census: every rooting of every plantri Eulerian triangulation of order V.

For each rooted instance: enumerate all pair supports (2-factors of B), test the two-tree
packing of each, count tree states per group; then test `RANDOM` random 2-selections
(arbitrary deleted corners, not 2-factors).  Usage: python census.py VMIN VMAX [RANDOM] [SEED]
Writes data/census_V<a>-<b>.json."""
import json, sys, time, random
from pathlib import Path
from tp import Tri, Rooted, plantri, check_packing

OUT = Path(__file__).resolve().parents[1] / 'data'


def run_instance(inst, nrandom, rng):
    us = inst.two_factors()
    m = len(inst.white)
    rec = {'pairs_supports': len(us), 'pack_ok': 0, 'pack_fail': [], 'groups_with_tree': 0,
           'tree_states': 0, 'random_ok': 0, 'random_fail': []}
    for u in us:
        es = inst.support(u)
        res, data = check_packing(m, [e[2:] for e in es])
        if res == 'pack':
            rec['pack_ok'] += 1
        else:
            rec['pack_fail'].append({'u': u, 'witness': data})
        k = sum(inst.is_tree_state(s) for s in inst.states_in(u))
        rec['tree_states'] += k  # each tree state lies in exactly one group (unique mate)
        rec['groups_with_tree'] += k > 0
    F = inst.tri.faces
    for _ in range(nrandom):
        u = []
        for t in inst.A:
            roots = [v for v in F[t] if v in inst.R]
            u.append(rng.choice(list(F[t])))
        es = inst.support(u)
        res, data = check_packing(m, [e[2:] for e in es])
        if res == 'pack':
            rec['random_ok'] += 1
        else:
            rec['random_fail'].append({'u': u, 'witness': data})
    return rec


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    nrandom = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    rng = random.Random(seed)
    start = time.time()
    rows = []
    summary = {}
    for V in range(a, b + 1):
        S = summary.setdefault(V, {'triangulations': 0, 'rooted': 0, 'rooted_with_pair': 0,
                                   'pair_supports': 0, 'pack_fail': 0, 'random_tests_with_pair': 0,
                                   'random_fail_with_pair': 0, 'random_tests_no_pair': 0,
                                   'random_fail_no_pair': 0, 'groups_without_tree': 0})
        for gi, rot in enumerate(plantri(V)):
            tri = Tri(rot)
            S['triangulations'] += 1
            for f in range(len(tri.faces)):
                inst = Rooted(tri, f)
                rec = run_instance(inst, nrandom, rng)
                S['rooted'] += 1
                haspair = rec['pairs_supports'] > 0
                S['rooted_with_pair'] += haspair
                S['pair_supports'] += rec['pairs_supports']
                S['pack_fail'] += len(rec['pack_fail'])
                S['groups_without_tree'] += rec['pairs_supports'] - rec['groups_with_tree']
                key = 'with_pair' if haspair else 'no_pair'
                S['random_tests_' + key] += nrandom
                S['random_fail_' + key] += len(rec['random_fail'])
                if haspair and rec['tree_states'] == 0:
                    raise AssertionError('pair but no tree state: code error or theorem false')
                if rec['pack_fail'] or rec['random_fail'] or (haspair and rec['groups_with_tree'] < rec['pairs_supports']):
                    rows.append({'V': V, 'index': gi, 'outer': f, 'rotation': rot, **rec,
                                 'random_fail': rec['random_fail'][:2]})
        S['seconds'] = round(time.time() - start, 1)
        print(V, S, flush=True)
    name = OUT / f'census_V{a}-{b}.json'
    name.write_text(json.dumps({'command': 'python code/census.py ' + ' '.join(sys.argv[1:]),
                                'summary': summary, 'flagged': rows}, indent=1))


if __name__ == '__main__':
    main()
