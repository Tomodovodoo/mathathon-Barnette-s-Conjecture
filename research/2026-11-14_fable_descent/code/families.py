"""Adversarial families in the text format read by descent.exe and walk.exe.

One line per triangulation: "V d n1..nd d n1..nd ... [r0 r1 r2]" (rotation lists, optional roots).
Usage:
  python families.py tube P L            hexagonal-type tube of width P (even) and length L
                                          (construction copied from sol_counting-families/code/families.py)
  python families.py bipyramid M         double wheel on a 2M-cycle (dual of the 2M-gonal prism)
  python families.py trap FILE.json      a saved trap of the graph-theory folder (rot, t0), with roots
  python families.py glue FILE.json N    N copies of the instance in FILE.json (keys rot, t0) glued in a chain:
                                          each copy's root face is glued into a white face of the previous copy
  python families.py line "V d ..." N    same, from a text line with roots
"""
import sys, json
import networkx as nx


def rot_of(g):
    ok, emb = nx.check_planarity(g)
    assert ok
    return {v: list(emb.neighbors_cw_order(v)) for v in g}


def line_of(rot, roots=None):
    V = len(rot)
    out = [V]
    for v in range(V):
        out.append(len(rot[v])); out.extend(rot[v])
    if roots:
        out.extend(roots)
    return ' '.join(map(str, out))


def tube(p, L):
    g = nx.Graph()
    for j in range(L + 1):
        for i in range(p):
            g.add_edge(j * p + i, j * p + (i + 1) % p)
    for j in range(L):
        for i in range(p):
            g.add_edge(j * p + i, (j + 1) * p + i)
            a, b = (i, (i + 1) % p) if i % 2 == 0 else ((i + 1) % p, i)
            g.add_edge(j * p + a, (j + 1) * p + b)
    g.add_edges_from(((L + 1) * p, i) for i in range(p))
    g.add_edges_from(((L + 1) * p + 1, L * p + i) for i in range(p))
    return g


def bipyramid(m):
    g = nx.cycle_graph(2 * m)
    g.add_edges_from((2 * m, i) for i in range(2 * m))
    g.add_edges_from((2 * m + 1, i) for i in range(2 * m))
    return g


def faces_of(rot):
    pos = {v: {w: i for i, w in enumerate(ns)} for v, ns in rot.items()}
    seen, faces = set(), []
    for v in rot:
        for w in rot[v]:
            if (v, w) in seen:
                continue
            f = []; a, b = v, w
            while (a, b) not in seen:
                seen.add((a, b)); f.append(a)
                a, b = b, rot[b][pos[b][a] - 1]
            faces.append(tuple(f))
    return faces


def rot_from_faces(faces):
    """faces: consistently oriented triangles. Rebuild rotation lists."""
    nxt = {}
    for a, b, c in faces:
        for x, y, z in ((a, b, c), (b, c, a), (c, a, b)):
            nxt.setdefault(x, {})[z] = y      # around x: after neighbour z comes y
    rot = {}
    for x, m in nxt.items():
        start = next(iter(m)); order = [start]; cur = m[start]
        while cur != start:
            order.append(cur); cur = m[cur]
        assert len(order) == len(m)
        rot[x] = order
    return rot


def colour(faces, t0):
    """0 = colour of t0 (black)."""
    side = {}
    for i, f in enumerate(faces):
        for j in range(3):
            side[f[j], f[(j + 1) % 3]] = i
    col = {t0: 0}; st = [t0]
    while st:
        i = st.pop(); f = faces[i]
        for j in range(3):
            g = side[f[(j + 1) % 3], f[j]]
            if g not in col:
                col[g] = 1 - col[i]; st.append(g)
    return col


def glue_chain(rot, roots, copies):
    """Chain of copies. Copy j+1 loses its root face and is glued into a white face of copy j
    that is disjoint from copy j's roots (first such face in the face order)."""
    base_faces = faces_of(rot)
    t0 = next(i for i, f in enumerate(base_faces) if set(f) == set(roots))
    col = colour(base_faces, t0)
    wf = next(i for i, f in enumerate(base_faces) if col[i] == 1 and not set(f) & set(roots))
    V = len(rot)
    faces = list(base_faces)
    cur_w = base_faces[wf]          # the white face of the current last copy, in global labels
    n_tot = V
    for _ in range(copies - 1):
        g = base_faces[t0]
        # glue root face g (orientation reversed) onto white face cur_w
        ident = {g[0]: cur_w[0], g[1]: cur_w[2], g[2]: cur_w[1]}
        for v in range(V):
            if v not in ident:
                ident[v] = n_tot; n_tot += 1
        faces = [f for f in faces if set(f) != set(cur_w)]
        faces += [tuple(ident[v] for v in f) for i, f in enumerate(base_faces) if i != t0]
        cur_w = tuple(ident[v] for v in base_faces[wf])
    return rot_from_faces(faces), list(roots)


def parse_line(line):
    a = list(map(int, line.split())); V = a[0]; p = 1; rot = {}
    for v in range(V):
        d = a[p]; rot[v] = a[p + 1:p + 1 + d]; p += 1 + d
    return rot, a[p:p + 3]


def main():
    kind = sys.argv[1]
    if kind == 'tube':
        print(line_of(rot_of(tube(int(sys.argv[2]), int(sys.argv[3])))))
    elif kind == 'bipyramid':
        print(line_of(rot_of(bipyramid(int(sys.argv[2])))))
    elif kind == 'trap':
        d = json.load(open(sys.argv[2]))
        print(line_of({int(k): v for k, v in d['rot'].items()}, d['t0']))
    elif kind == 'glue':
        d = json.load(open(sys.argv[2]))
        rot, roots = glue_chain({int(k): v for k, v in d['rot'].items()}, d['t0'], int(sys.argv[3]))
        print(line_of(rot, roots))
    elif kind == 'line':
        rot, roots = parse_line(sys.argv[2])
        rot, roots = glue_chain(rot, roots, int(sys.argv[3]))
        print(line_of(rot, roots))


main()
