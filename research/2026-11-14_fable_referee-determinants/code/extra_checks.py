"""Three further checks.

1. Replay astra's 18 stored rows (edges and root triangle read as data) with my code.
2. The gauge identity: sol's number-field matrix is -i times a diagonal conjugate of
   astra's real matrix, D = diag(omega^c(u)) for the vertex three-colouring c.
3. Parity audit: which uses of the disk identity need the value 3 and which only "odd".

Run from the repository root:
    python -B research/2026-11-14_fable_referee-determinants/code/extra_checks.py
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from etri import Tri, det_int, octahedron, bipyramid, tetrakis_hexahedron, disdyakis_dodecahedron, glue
from referee import audit
from compare_lab import Z12, Q, QINV, I

out = {}

# ---------------------------------------------------------------- 1. astra's stored examples
rows = json.loads((ROOT / 'research/2026-11-14_astra_route-dimers/data.json').read_text())
lin = {r['name']: r for r in json.loads((ROOT / 'research/2026-11-14_astra_route-dimers/linear_weights.json').read_text())}
rep = []
for r in rows:
    mine = audit(r['name'], [tuple(e) for e in r['edges']], r['root_face'], heavy=False)
    same = {
        'states': mine['states'] == r['states'],
        'pairs': mine['pairs'] == r['pairs'],
        'trees': mine['tree_matchings'] == r['trees'],
        'cmin': mine['cmin'] == r['cmin'],
        'white_tau': mine['white_tau_full'] == r['white_tau'],
        'restricted_white_tau': mine['white_tau_B'] == r['restricted_white_tau'],
        'lowest coefficient': (mine.get('lowest_coefficient', 0)) == r['leading'],
        'norm': mine['norm'] == lin[r['name']]['norm'],
        'my own checks': mine['all_ok'],
    }
    rep.append({'name': r['name'], 'agree': same, 'pairs': r['pairs'], 'cyclic_states_with_mates': mine['states_with_cyclic_Q_and_mates'],
                'two_matroid_false_positives': mine.get('two_matroid_false_positives'),
                'white_trees_one_spoke_per_face': mine.get('white_trees_one_spoke_per_face')})
    print(r['name'], 'n', mine['n'], 'states', mine['states'], 'pairs', mine['pairs'], 'trees', mine['tree_matchings'], 'tau', mine['white_tau_full'], mine['white_tau_B'],
          'face-transversal white trees', mine.get('white_trees_one_spoke_per_face'), 'ALL AGREE' if all(same.values()) else same)
out['astra_rows'] = rep
print('astra rows with no pair at all:', sum(1 for r in rows if r['pairs'] == 0), 'of', len(rows))
print('astra rows where a cyclic Q_s with mates occurs:', sum(1 for r in rep if r['cyclic_states_with_mates']))
print('astra polarization rows (mixed_q2 present):', sum('mixed_q2' in r for r in rows), ', of which no pair:', sum('mixed_q2' in r and r['pairs'] == 0 for r in rows))

# ---------------------------------------------------------------- 2. gauge identity
rng = random.Random(7)
OMEGA = Q * Q * Q * Q  # exp(2 pi i / 3)
OM = [Z12.of(1), OMEGA, OMEGA * OMEGA]
assert OM[2] * OMEGA == 1
lib = [('octahedron', octahedron(), (0, 1, 2)), ('hexagonal_bipyramid', bipyramid(6), (0, 1, 6)),
       ('tetrakis_hexahedron', tetrakis_hexahedron(), (0, 1, 8)), ('disdyakis_dodecahedron', disdyakis_dodecahedron(), (0, 8, 20)),
       ('double_octahedron', glue(octahedron(), (0, 1, 2), octahedron(), (0, 1, 2)), (0, 1, 3))]
lib += [(r['name'], [tuple(e) for e in r['edges']], r['root_face']) for r in rows]
gauge_ok = True
for name, edges, root in lib:
    for mirror in (False, True):
        b = Tri(edges, root, mirror)
        # three-colouring with c(v) - c(u) = delta(u, v) mod 3
        c = {b.V[0]: 0}
        stack = [b.V[0]]
        adj = {}
        for u, v in b.edges:
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in c:
                    c[v] = (c[u] + b.delta(u, v)) % 3
                    stack.append(v)
        col_ok = all((c[v] - c[u] - b.delta(u, v)) % 3 == 0 for (u, v) in b.left)
        # entrywise: q^delta(u,v) == -i * delta(u,v) * omega^(c(v)-c(u))
        ent_ok = True
        for (u, v) in b.left:
            lhs = Q if b.delta(u, v) == 1 else QINV
            rhs = (-I) * b.delta(u, v) * OM[c[v]] * OM[(-c[u]) % 3]
            ent_ok &= lhs == rhs
        gauge_ok &= col_ok and ent_ok
out['gauge identity holds on every directed edge'] = [gauge_ok, len(lib) * 2]
print('gauge identity q^delta = -i * delta * omega^(c(v)-c(u)) on', len(lib) * 2, 'oriented instances:', gauge_ok)

# ---------------------------------------------------------------- 3. raw determinant and skew symmetry
for name, edges, root in lib[:3]:
    b = Tri(edges, root)
    one = {(t, v): 1 for t in b.A for v in b.faces[t]}
    vals = []
    for _ in range(5):
        w = {(t, v): rng.randint(2, 30) for t in b.A for v in b.faces[t]}
        vals.append((b.raw_det(w), b.F_by_pairs(w)))
    print(name, 'n', b.n, 'raw det at w=1:', b.raw_det(one), 'F(1):', b.F_by_pairs(one), '| (raw det, F) at random w:', vals)
    out[f'raw_vs_F_{name}'] = {'at_one': [b.raw_det(one), b.F_by_pairs(one)], 'random': vals}

# ---------------------------------------------------------------- 4. parity audit of Q-cycle and D-cycle reversal
par_ok, n_q, n_d = True, 0, 0
for name, edges, root in lib:
    b = Tri(edges, root)
    if len(b.states()) > 60:
        continue
    for r, s in b.pairs():
        # D reversal: swapping r and s on one cycle multiplies eps by (-1)^length
        for cyc in b.dcycles(r, s):
            faces = {t for t, _, _ in cyc}
            r2 = tuple(sv if t in faces else rv for t, rv, sv in zip(b.A, r, s))
            s2 = tuple(rv if t in faces else sv for t, rv, sv in zip(b.A, r, s))
            par_ok &= b.eps(r2, s2) == b.eps(r, s) * (-1) ** len(cyc) == -b.eps(r, s)
            n_d += 1
        # Q reversal on each directed cycle of r(t) -> u(t)
        third = {rv: (t, next(x for x in b.faces[t] if x not in (rv, sv))) for t, rv, sv in zip(b.A, r, s)}
        seen = set()
        for start in r:
            path, v = [], start
            while v in third and v not in seen:
                seen.add(v)
                path.append(v)
                v = third[v][1]
            if v in path:
                cyc = path[path.index(v):]
                faces = {third[x][0] for x in cyc}
                r2 = tuple(third[rv][1] if t in faces else rv for t, rv in zip(b.A, r))
                assert sorted(r2) == sorted(r) and all(x != y for x, y in zip(r2, s))
                par_ok &= b.eps(r2, s) == b.eps(r, s) * (-1) ** len(cyc) == -b.eps(r, s)
                n_q += 1
out['reversal multiplies eps by (-1)^length, and length is odd'] = [par_ok, {'D cycles': n_d, 'Q cycles': n_q}]
print('reversal multiplies eps by (-1)^length with odd length:', par_ok, 'D cycles', n_d, 'Q cycles', n_q)
(HERE / 'extra_checks.json').write_text(json.dumps(out, indent=1))
