"""Adversarial and large instances, plus the exact failure rule (PREDICTIONS 5, 6).

Instances: the V=18 lattice-extreme counterexample (opus_conjectures), tubes, a subdivided
tube and prism chains (sol_counting-families constructors, read only), and random octahedral
sums glued into faces of both colours (so that black-inner separating triangles occur).
For each chosen rooting: all pair supports (up to LIMIT), RANDOM random deleted-corner maps,
and for every map the prediction of the failure rule is compared with the packing result.
Usage: python big.py [SEED]   writes data/big.json"""
import json, sys, random, time
from pathlib import Path
import networkx as nx
from tp import Tri, Rooted, two_tree_partition, ROOT


def packs(m, ends):
    return two_tree_partition(m, ends) is not None
from referee_sol import tri_from_nx

sys.path.insert(0, str(ROOT / 'research/2026-11-14_sol_counting-families/code'))
from families import tube, stack, subdivide  # noqa: E402  (read-only constructors)

OUT = Path(__file__).resolve().parents[1] / 'data'
LIMIT, RANDOM = 100, 40


def black_inner_triangles(inst):
    """List of (triangle vertex set, [the three inner black faces along it])."""
    tri = inst.tri
    faceset = {frozenset(f) for f in tri.faces}
    res = []
    seen = set()
    for a in range(tri.V):
        for b in tri.adj[a]:
            for c in tri.adj[a] & tri.adj[b]:
                key = frozenset((a, b, c))
                if len(key) < 3 or key in seen or key in faceset:
                    continue
                seen.add(key)
                cut = {(a, b), (b, a), (b, c), (c, b), (a, c), (c, a)}
                # faces reachable from t0 without crossing the triangle
                side = {inst.outer}
                stack_ = [inst.outer]
                while stack_:
                    f = stack_.pop()
                    F = tri.faces[f]
                    for i in range(3):
                        x, y = F[i], F[(i + 1) % 3]
                        if (x, y) in cut:
                            continue
                        g = tri.fid[y, x]
                        if g not in side:
                            side.add(g)
                            stack_.append(g)
                inner = []
                for x, y in ((a, b), (b, c), (c, a)):
                    f1, f2 = tri.fid[x, y], tri.fid[y, x]
                    inner.append(f1 if f1 not in side else f2)
                if all(f in inst.black for f in inner):
                    res.append((sorted(key), inner))
    return res


def predicted_fail(inst, u, bits):
    ud = dict(zip(inst.A, u))
    return any(all(ud[t] in tri for t in inner) for tri, inner in bits)


def instances(rng):
    d = json.loads((ROOT / 'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text())
    tok = list(map(int, d['line'].split()))
    V, pos, rot = tok[0], 1, []
    for v in range(V):
        k = tok[pos]
        rot.append(tok[pos + 1:pos + 1 + k])
        pos += 1 + k
    tri = Tri(rot)
    outer = next(i for i, f in enumerate(tri.faces) if set(f) == set(d['roots']))
    yield 'c2_counterexample_V18', tri, [outer]
    for p, L in ((4, 8), (4, 16), (6, 6), (8, 4), (10, 3)):
        tri, _ = tri_from_nx(tube(p, L))
        yield f'tube{p}_{L}', tri, list(range(0, len(tri.faces), max(1, len(tri.faces) // 6)))
    tri, _ = tri_from_nx(subdivide(tube(4, 2)))
    yield 'subdiv_tube4_2', tri, list(range(0, len(tri.faces), 30))
    for q in (4, 8):
        b = stack(6, q)
        tri, idx = tri_from_nx(b.T)
        rs = {idx[v] for v in b.faces[b.outer]}
        yield f'prism_chain{q}', tri, [next(i for i, f in enumerate(tri.faces) if set(f) == rs)]
    oct_ = nx.octahedral_graph()
    for rep in range(12):
        g = oct_.copy()
        for j in range(rng.randint(1, 4)):
            tri, idx = tri_from_nx(g)
            inv = {i: v for v, i in idx.items()}
            f = rng.randrange(len(tri.faces))
            a, b, c = (inv[x] for x in tri.faces[f])
            # glue a fresh octahedron into face abc: remove nothing, add the opposite triangle
            n0 = max(g) + 1
            x, y, z = n0, n0 + 1, n0 + 2
            g.add_edges_from([(x, y), (y, z), (z, x), (a, y), (a, z), (b, x), (b, z), (c, x), (c, y)])
        tri, _ = tri_from_nx(g)
        yield f'random_octsum{rep}', tri, rng.sample(range(len(tri.faces)), 8)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    rng = random.Random(seed)
    rows, start = [], time.time()
    for name, tri, outers in instances(rng):
        for outer in outers:
            inst = Rooted(tri, outer)
            bits = black_inner_triangles(inst)
            us = inst.two_factors(limit=LIMIT)
            m = len(inst.white)
            fails = sum(not packs(m, [e[2:] for e in inst.support(u)]) for u in us)
            rule_ok = rule_bad = 0
            rnd_fail = 0
            example = None
            for _ in range(RANDOM):
                u = [rng.choice(list(tri.faces[t])) for t in inst.A]
                bad = not packs(m, [e[2:] for e in inst.support(u)])
                rnd_fail += bad
                if bad == predicted_fail(inst, u, bits):
                    rule_ok += 1
                else:
                    rule_bad += 1
                    example = u
            row = {'name': name, 'V': tri.V, 'outer': outer, 'black_inner_triangles': len(bits),
                   'pair_supports_tested': len(us), 'pair_support_failures': fails,
                   'random_maps': RANDOM, 'random_failures': rnd_fail,
                   'rule_agrees': rule_ok, 'rule_disagrees': rule_bad, 'disagreement_example': example}
            rows.append(row)
            print(row, round(time.time() - start, 1), flush=True)
            (OUT / 'big.json').write_text(json.dumps({'command': 'python code/big.py ' + str(seed), 'rows': rows}, indent=1))
    (OUT / 'big.json').write_text(json.dumps({'command': 'python code/big.py ' + str(seed), 'rows': rows}, indent=1))


if __name__ == '__main__':
    main()
