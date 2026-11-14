"""Small checks: spanning trees of the spoke graph H (UST probabilities), bridges of H,
separating triangles in tubes, M >= 2m and H_avoid >= M on the census."""
import sys, itertools
from fractions import Fraction
from core import *

def spoke_graph(inst):
    h = nx.Graph()
    for t in inst.black:
        for v in inst.faces[t]:
            h.add_edge(('t', t), ('v', v))
    return h

def tau(h):
    nodes = list(h.nodes()); idx = {x: i for i, x in enumerate(nodes)}; n = len(nodes) - 1
    Mx = [[Fraction(0)] * n for _ in range(n)]
    for a, b in h.edges():
        i, j = idx[a], idx[b]
        if i < n: Mx[i][i] += 1
        if j < n: Mx[j][j] += 1
        if i < n and j < n: Mx[i][j] -= 1; Mx[j][i] -= 1
    det = Fraction(1)
    for k in range(n):
        p = next(i for i in range(k, n) if Mx[i][k] != 0)
        if p != k: Mx[k], Mx[p] = Mx[p], Mx[k]; det = -det
        det *= Mx[k][k]
        for i in range(k + 1, n):
            f = Mx[i][k] / Mx[k][k]
            if f:
                for j in range(k, n): Mx[i][j] -= f * Mx[k][j]
    return int(det)

for name, inst in (('cube', Inst(bipyramid(4), (4, 0, 1))), ('hexagonal prism', Inst(bipyramid(6), (6, 0, 1)))):
    h = spoke_graph(inst)
    M = sum(1 for _ in inst.good_states())
    print(name, 'tau(H) =', tau(h), 'M =', M, 'uniform UST success = M/tau =', Fraction(M, tau(h)), 'bridges of H:', len(list(nx.bridges(h))))
# no bridge in H on the census, hence E deg_T(t0) < 3 for every positive weighting
nb = 0; cnt = 0
for V in range(6, 15):
    for g in plantri_eulerian(V):
        inst = Inst(g, 0); cnt += 1
        nb += len(list(nx.bridges(spoke_graph(inst))))
print('plantri V<=14:', cnt, 'graphs, total bridges of H:', nb)
# tubes: every 3-cycle is a face
for p in (4, 6, 8):
    for L in range(0, 7):
        g = tube(p, L)
        tri = sum(nx.triangles(g).values()) // 3
        assert tri == 2 * len(g) - 4, (p, L, tri)
print('tubes p=4,6,8, L<=6: number of 3-cycles equals number of faces (no separating triangle)')
# H_avoid(e0) >= M and 3M <= H on every root and every root edge, V<=14
viol = 0; roots = 0; eq = []
for V in range(6, 15):
    for gi, g in enumerate(plantri_eulerian(V)):
        faces = oriented_faces(g)
        H, use = hamilton(Inst(g, 0, faces=faces))
        for fi in range(len(faces)):
            inst = Inst(g, fi, faces=faces); roots += 1
            M = sum(1 for _ in inst.good_states())
            f = faces[fi]
            for e in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                if H - use.get(frozenset(e), 0) < M: viol += 1
            if 3 * M > H: viol += 1
            if 3 * M == H: eq.append((V, gi))
print('V<=14, roots', roots, 'violations of H_avoid(e0) >= M or 3M <= H:', viol, 'graphs with 3M = H:', sorted(set(eq)))
