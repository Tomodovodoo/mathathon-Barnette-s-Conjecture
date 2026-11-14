"""Tests of predictions 2-4 (PREDICTIONS.md) on every rooting of plantri orders VMIN..VMAX.

For every pair support F (2-factor of B, deleted-corner map u):
  black   : a W-spanning tree inside F with one edge in each cherry {(t,r(t)),(t,s(t))}
  point   : a W-spanning tree inside F with one edge at each nonroot
  P2      : F splits into two black-rainbow W-trees
  P1      : F splits into two point-rainbow W-trees
  both    : F splits into two trees that are rainbow for both (= a tree pair with both states trees)
For every rooted instance: W minus the triangle of t0 is a union of three spanning trees.
Brute force over the 2^n choices.  Usage: python rainbow.py VMIN VMAX"""
import json, sys, time, itertools
from pathlib import Path
from tp import Tri, Rooted, plantri, is_spanning_tree, two_tree_partition

OUT = Path(__file__).resolve().parents[1] / 'data'


def blocks_of(inst, u):
    F = inst.tri.faces
    used = {t: [v for v in F[t] if v != d] for t, d in zip(inst.A, u)}
    cherry = [((t, used[t][0]), (t, used[t][1])) for t in inst.A]
    at = {x: [] for x in inst.X}
    for t in inst.A:
        for v in used[t]:
            at[v].append((t, v))
    point = [tuple(at[x]) for x in inst.X]
    return cherry, point


def scan(inst, blocks):
    m = len(inst.white)
    w = inst.wedge
    one = two = False
    for bits in itertools.product((0, 1), repeat=len(blocks)):
        a = [w[b[i]] for b, i in zip(blocks, bits)]
        if is_spanning_tree(m, a):
            one = True
            c = [w[b[1 - i]] for b, i in zip(blocks, bits)]
            if is_spanning_tree(m, c):
                return True, True
    return one, two


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    start = time.time()
    summary, flagged = {}, []
    for V in range(a, b + 1):
        S = summary.setdefault(V, {'rooted': 0, 'with_pair': 0, 'supports': 0, 'black_in_F': 0, 'point_in_F': 0,
                                   'P2_black_split': 0, 'P1_point_split': 0, 'both_split': 0,
                                   'three_trees_with_pair': 0, 'three_trees_no_pair_ok': 0, 'no_pair': 0})
        for gi, rot in enumerate(plantri(V)):
            tri = Tri(rot)
            for f in range(len(tri.faces)):
                inst = Rooted(tri, f)
                us = inst.two_factors()
                S['rooted'] += 1
                ends = [inst.wedge[t, v] for t in inst.A for v in tri.faces[t]]
                three = two_tree_partition(len(inst.white), ends, k=3) is not None
                if us:
                    S['with_pair'] += 1
                    S['three_trees_with_pair'] += three
                else:
                    S['no_pair'] += 1
                    S['three_trees_no_pair_ok'] += three
                if us and not three:
                    flagged.append({'V': V, 'index': gi, 'outer': f, 'what': 'three trees fail with pair'})
                for u in us:
                    S['supports'] += 1
                    cherry, point = blocks_of(inst, u)
                    b1, b2 = scan(inst, cherry)
                    p1, p2 = scan(inst, point)
                    S['black_in_F'] += b1
                    S['point_in_F'] += p1
                    S['P2_black_split'] += b2
                    S['P1_point_split'] += p2
                    both = any(inst.is_tree_state(s) and inst.is_tree_state(
                        {t: next(v for v in tri.faces[t] if v != s[t] and v != uu) for t, uu in zip(inst.A, u)})
                        for s in inst.states_in(u))
                    S['both_split'] += both
                    if not (b1 and p1 and b2 and p2):
                        flagged.append({'V': V, 'index': gi, 'outer': f, 'u': list(u), 'black': b1, 'point': p1,
                                        'P2': b2, 'P1': p2, 'both': both, 'rotation': rot})
        S['seconds'] = round(time.time() - start, 1)
        print(V, S, flush=True)
    (OUT / f'rainbow_V{a}-{b}.json').write_text(json.dumps(
        {'command': 'python code/rainbow.py ' + ' '.join(sys.argv[1:]), 'summary': summary,
         'flagged': flagged[:200], 'n_flagged': len(flagged)}, indent=1))


if __name__ == '__main__':
    main()
