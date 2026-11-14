"""Prism chain (FAMILIES section 4), root sweeps on tubes, octahedral four-subdivision."""
import json, sys
from core import *
from t_families_lib import det_states, tube_root
out = {}
# ---- chain, three gluing classes
for pole_to, nm in ((0, 'N->v4'), (1, 'N->v5'), (2, 'N->S')):
    rows = []
    for q in range(1, 6):
        g, root = prism_chain(q, pole_to)
        inst = Inst(g, root)
        r = inst.summary()
        H, use = hamilton(inst)
        f0 = inst.faces[inst.t0]
        av = sorted(H - use.get(frozenset(e), 0) for e in ((6, 0), (6, 1), (0, 1)))
        exp = [1]
        for j in range(q):                       # product of (z^(5j+2)-1)
            d = 5 * j + 2; new = [0] * (len(exp) + d)
            for i, c in enumerate(exp): new[i + d] += c; new[i] -= c
            exp = new
        if exp[-1] < 0: exp = [-c for c in exp]
        rows.append(dict(q=q, V=len(g), S=r['S'], P=r['P'], M=r['M'], cmin=r['m'], covers=r['covers'], H=H, root_avoid=av,
                         poly_is_product=(tuple(exp) == r['poly'])))
        print(nm, rows[-1]); sys.stdout.flush()
    out[nm] = rows
# ---- root sweeps
sw = {}
for p, Lmax in ((4, 5), (6, 5)):
    for L in range(1, Lmax + 1):
        g = tube(p, L); faces = oriented_faces(g); vals = set()
        for i in range(len(faces)):
            inst = Inst(g, i, faces=faces)
            vals.add(sum(1 for _ in inst.good_states()))
        sw[f'{p},{L}'] = sorted(vals); print('sweep', p, L, sorted(vals)); sys.stdout.flush()
out['sweeps'] = sw
# ---- four-subdivision of the octahedron
def subdivide(g):
    faces = oriented_faces(g); mid = {}; h = nx.Graph(); nxt = max(g.nodes()) + 1
    for a, b in g.edges():
        mid[frozenset((a, b))] = nxt; nxt += 1
    for a, b, c in faces:
        x, y, z = mid[frozenset((a, b))], mid[frozenset((b, c))], mid[frozenset((c, a))]
        for tri in ((a, x, z), (b, y, x), (c, z, y), (x, y, z)):
            h.add_edges_from(((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])))
    return h
g = subdivide(bipyramid(4)); faces = oriented_faces(g); seen = {}
for i in range(len(faces)):
    inst = Inst(g, i, faces=faces); r = inst.summary()
    key = (r['S'], r['P'], r['M'], r['m'], r['poly'])
    seen.setdefault(str(key), []).append(i)
inst = Inst(g, 0, faces=faces); H, use = hamilton(inst)
print('subdivided octahedron V', len(g), 'H', H, 'avoid values', sorted(set(H - u for u in use.values())))
for k, v in seen.items(): print(' roots', len(v), k)
out['subdiv'] = dict(H=H, classes={k: len(v) for k, v in seen.items()})
json.dump(out, open('out_chain.json', 'w'), indent=1)
