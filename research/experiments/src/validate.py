"""Validation of the generators, of the symmetry computation and of the samplers.

  python src/validate.py

1. plantri -b against the published numbers of Eulerian triangulations, with
   and without identification of mirror images (plantri-guide.txt), the
   second number recomputed from our automorphism groups.
2. Our own generator: closure of the octahedron under vertex splits and
   insertion of octahedra, compared with the same numbers.
3. Orders of the automorphism groups against networkx on the abstract graph.
4. The Markov chain, with the settings of families.random_graphs: frequencies
   of the isomorphism classes at small sizes against the weights 1/|Aut|
   (chi-square), for both ensembles.
5. The estimates of good/states by importance sampling, and the numbers of
   good uniform draws, against exact enumeration.
Writes data/validation.json.
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import fb                                                     # noqa: E402
import graphs                                                 # noqa: E402
import symmetry                                               # noqa: E402

# plantri-guide.txt: 3-connected (-b) and 4-connected (-bc4) Eulerian triangulations,
# isomorphism classes with mirror images identified ("all") and not identified ("O-P").
PUBLISHED = {6: (1, 1, 1), 7: (0, 0, 0), 8: (1, 1, 1), 9: (1, 1, 0), 10: (2, 2, 2), 11: (2, 2, 1),
             12: (8, 9, 5), 13: (8, 11, 3), 14: (32, 41, 18), 15: (57, 89, 19), 16: (185, 296, 79),
             17: (466, 829, 134), 18: (1543, 2772, 501), 19: (4583, 8746, 1147),
             20: (15374, 29461, 3976), 21: (50116, 98342, 11055), 22: (171168, 336881, 37231),
             23: (582603, 1156559, 114560), 24: (2024119, 4024297, 384053)}


def plantri(v, extra=''):
    path = ROOT / 'build' / f'validate_{v}{extra}.pc'
    subprocess.run([str(ROOT / 'build' / 'bin' / 'plantri.exe'), '-b' + extra, str(v), str(path)],
                   check=True, capture_output=True)
    out = [graphs.faces_of_rotation(rot) for rot in graphs.read_planar_code(path)]
    path.unlink()
    return out


def chi_square(counts, weights):
    total = sum(counts)
    wsum = sum(weights)
    return sum((c - total * w / wsum) ** 2 / (total * w / wsum) for c, w in zip(counts, weights))


def main():
    result = {}

    # 1. plantri and the groups
    rows, classes = [], {}
    for v in range(6, 21):
        tris = plantri(v) if v != 7 else []
        info = [symmetry.describe(F) for F in tris]
        codes = {c['code'] for c in info}
        chiral = sum(c['order'] == c['order_op'] for c in info)
        nosep = sum(fb.separating_triangles(F)[0] == 0 for F in tris)
        rows.append({'vertices': v, 'plantri': len(tris), 'distinct_codes': len(codes),
                     'classes_without_mirror_identification': len(tris) + chiral,
                     'without_separating_triangle': nosep, 'published': list(PUBLISHED[v]),
                     'unknown_group_types': sum(c['type'] == '?' for c in info)})
        assert (len(tris), len(tris) + chiral, nosep) == PUBLISHED[v] and len(codes) == len(tris), v
        assert all(c['type'] != '?' for c in info)
        classes[v] = {c['code']: (c['order'], fb.separating_triangles(F)[0] == 0) for c, F in zip(info, tris)}
        print(rows[-1], flush=True)
    result['plantri_counts'] = rows

    # 2. our own generator
    level = {symmetry.describe(graphs.octahedron())['code']: graphs.octahedron()}
    by_size = {6: level}
    gen_rows = []
    for v in range(6, 16):
        for F in by_size.get(v, {}).values():
            children = list(graphs.all_splits(F)) + [graphs.insert_octahedron(F, f) for f in range(len(F))]
            for child in children:
                child = graphs.relabel(child)
                assert graphs.is_eulerian_triangulation(child)
                size = int(child.max()) + 1
                if size <= 15:
                    by_size.setdefault(size, {}).setdefault(symmetry.describe(child)['code'], child)
        found = len(by_size.get(v, {}))
        gen_rows.append({'vertices': v, 'generated': found, 'published': PUBLISHED[v][0]})
        assert found == PUBLISHED[v][0] and set(by_size.get(v, {})) == set(classes[v]), v
    result['own_generator'] = gen_rows
    print('own generator', gen_rows, flush=True)

    # 3. group orders against networkx
    import networkx as nx
    from networkx.algorithms.isomorphism import GraphMatcher
    checked = 0
    for v in range(6, 14):
        for F in by_size.get(v, {}).values():
            G = nx.Graph()
            for a, b, c in F.tolist():
                G.add_edges_from([(a, b), (b, c), (c, a)])
            order = sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter())
            assert order == symmetry.describe(F)['order']
            checked += 1
    result['group_orders_checked_against_networkx'] = checked
    known = {'octahedron': (graphs.octahedron(), 'Oh'), 'bipyramid-3': (graphs.bipyramid(3), 'D6h'),
             'bipyramid-5': (graphs.bipyramid(5), 'D10h'),
             'truncated octahedron': (graphs.octahedral(1, 1), 'Oh'),
             'octahedral(2,1)': (graphs.octahedral(2, 1), 'O'),
             'great rhombicuboctahedron': (graphs.omnitruncated('cube'), 'Oh'),
             'great rhombicosidodecahedron': (graphs.omnitruncated('dodecahedron'), 'Ih'),
             'truncated octahedron as omnitruncated tetrahedron': (graphs.omnitruncated('tetrahedron'), 'Oh')}
    result['known_groups'] = {}
    for name, (F, expected) in known.items():
        got = symmetry.describe(F)['type']
        result['known_groups'][name] = got
        assert got == expected, (name, got)
    assert symmetry.describe(graphs.octahedral(1, 1))['code'] == symmetry.describe(graphs.omnitruncated('tetrahedron'))['code']
    print('groups ok', flush=True)

    # 4. the Markov chain
    mc = []
    import families
    for kind, sizes in ((0, (12, 13, 14, 15, 16, 17)), (1, (12, 13, 14, 15, 16, 17, 18))):
        for v in sizes:
            target = {code: order for code, (order, nosep) in classes[v].items() if nosep or kind == 0}
            if kind == 0:
                start, head = graphs.octahedron(), 3
            else:
                start, head = (graphs.bipyramid(2) if v % 2 == 0 else families.odd_start()), 2
            samples, stats = fb.mcmc(start, v, kind, 400_000_000, 200, 200_000, seed=1000 + 10 * v + kind,
                                     headroom=head, gamma=3.6)
            counts = Counter(symmetry.describe(F)['code'] for F in samples)
            assert set(counts) <= set(target)
            codes = sorted(target)
            chi = chi_square([counts[c] for c in codes], [1 / target[c] for c in codes])
            mc.append({'kind': kind, 'vertices': v, 'classes': len(codes), 'classes_seen': len(counts),
                       'samples': len(samples), 'thin': 200, 'chi_square': round(float(chi), 2),
                       'degrees_of_freedom': len(codes) - 1,
                       'fraction_of_steps_at_target': round(float(stats[5] / stats[0]), 3)})
            print(mc[-1], flush=True)
    result['markov_chain'] = mc

    # 5. sampling of states
    rng = np.random.default_rng(5)
    samp = []
    pool = [F for v in (16, 18, 20) for F in plantri(v)[:400:40]]
    pool += [graphs.octahedral(2, 1), graphs.tube(3, 4), graphs.octahedral(2, 2)]
    for F in pool:
        t0 = int(rng.integers(len(F)))
        e = fb.enumerate_states(F, t0, 0)
        if e['states'] == 0:
            continue
        s = fb.sample(F, t0, 20000, 20000, seed=int(rng.integers(1 << 30)))
        p = e['good'] / e['states']
        se_u = (p * (1 - p) / 20000) ** 0.5
        se_s = ((s['sis_meansq'] - s['sis_mean'] ** 2) / 20000) ** 0.5
        samp.append({'faces': len(F), 'states': e['states'], 'good': e['good'],
                     'log_states_error': abs(s['logdet'] - np.log(e['states'])),
                     'z_uniform': (s['uniform_good'] / 20000 - p) / se_u if se_u else 0.0,
                     'z_importance': (s['sis_mean'] - p) / se_s if se_s else 0.0,
                     'relative_se_importance': se_s / p if p else 0.0,
                     'relative_se_uniform': se_u / p if p else 0.0})
    zu = [r['z_uniform'] for r in samp]
    zs = [r['z_importance'] for r in samp]
    result['state_sampling'] = {
        'instances': len(samp), 'max_log_states_error': max(r['log_states_error'] for r in samp),
        'z_uniform_mean': float(np.mean(zu)), 'z_uniform_rms': float(np.sqrt(np.mean(np.square(zu)))),
        'z_importance_mean': float(np.mean(zs)), 'z_importance_rms': float(np.sqrt(np.mean(np.square(zs)))),
        'max_abs_z': float(max(map(abs, zu + zs))),
        'median_ratio_of_standard_errors_uniform_to_importance':
            float(np.median([r['relative_se_uniform'] / r['relative_se_importance']
                             for r in samp if r['relative_se_importance']]))}
    print(result['state_sampling'], flush=True)

    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data' / 'validation.json').write_text(json.dumps(result, indent=1) + '\n')


if __name__ == '__main__':
    main()
