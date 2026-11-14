"""Independent check (pure Python + networkx, no code shared with bar.c) of the distance from the
two extremes of the alpha-orientation lattice of 2-factors to the nearest element carrying a
tree pair.

Input: a line in bar.c -T format (V, deg + ccw neighbours per vertex, then the 3 roots).
Method:
  * faces by the left-face rule, 2-colouring, root face t0 coloured black;
  * a 2-factor of B by networkx max flow;
  * lattice of 2-factors = integer potentials phi on H_0 faces (white faces, the three at t0
    merged into 'O', phi(O)=0) with phi(R)-phi(L) in {-1,0} for every spoke (L,R w.r.t. the
    reference orientation);  extremes by networkx shortest paths (Bellman-Ford);
  * up-covers of phi: for each face a, the least solution >= phi with phi(a)+1, obtained by
    relaxing lower bounds to a fixpoint; covers are the inclusion-minimal ones;
  * tree pair test: try all 2^c orientations of the D-cycles, Q_s forest via networkx.
Usage: python verify_near.py file line_index maxdist
"""
import sys, itertools
import networkx as nx


def parse(line):
    a = list(map(int, line.split()))
    V = a[0]; p = 1; rot = {}
    for v in range(V):
        d = a[p]; rot[v] = a[p + 1:p + 1 + d]; p += 1 + d
    return rot, set(a[p:p + 3])


def build(rot, roots):
    pos = {v: {w: i for i, w in enumerate(ns)} for v, ns in rot.items()}
    face_of = {}
    faces = []
    for v in rot:
        for w in rot[v]:
            if (v, w) in face_of:
                continue
            f = []; d = (v, w)
            while d not in face_of:
                face_of[d] = len(faces); f.append(d[0])
                a, b = d
                c = rot[b][pos[b][a] - 1]
                d = (b, c)
            assert len(f) == 3
            faces.append(tuple(f))
    t0 = [i for i, f in enumerate(faces) if set(f) == roots][0]
    col = {t0: 0}; st = [t0]
    while st:
        f = st.pop(); a, b, c = faces[f]
        for x, y in ((a, b), (b, c), (c, a)):
            g = face_of[(y, x)]
            if g not in col:
                col[g] = 1 - col[f]; st.append(g)
            else:
                assert col[g] != col[f]
    return faces, face_of, t0, col


def main():
    lines = [l for l in open(sys.argv[1]) if l.strip()]
    rot, roots = parse(lines[int(sys.argv[2])])
    maxd = int(sys.argv[3])
    faces, face_of, t0, col = build(rot, roots)
    A = [i for i in range(len(faces)) if col[i] == 0 and i != t0]
    X = [v for v in rot if v not in roots]
    white = [i for i in range(len(faces)) if col[i] == 1]
    outer = {face_of[(b, a)] for a, b in zip(faces[t0], faces[t0][1:] + faces[t0][:1])}
    node = {w: ('O' if w in outer else w) for w in white}
    # spoke (t, i): corner faces[t][i]; side_plus = white across edge (c_i, c_{i+1}); side_minus = across (c_{i+2}, c_i)
    sp = {}
    for t in A:
        f = faces[t]
        for i in range(3):
            a, b, c = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            sp[(t, i)] = (node[face_of[(b, a)]], node[face_of[(a, c)]])
    # 2-factor by max flow: deleted corner u(t); faces with a root corner are forced
    G = nx.DiGraph()
    forced = {}
    for t in A:
        rc = [i for i in range(3) if faces[t][i] in roots]
        if rc:
            forced[t] = rc[0]; continue
        G.add_edge('s', ('t', t), capacity=1)
        for i in range(3):
            G.add_edge(('t', t), ('x', faces[t][i]), capacity=1)
    for x in X:
        G.add_edge(('x', x), 'z', capacity=len(rot[x]) // 2 - 2)
    val, flow = nx.maximum_flow(G, 's', 'z')
    free = [t for t in A if t not in forced]
    assert val == len(free), "no pair"
    u0 = dict(forced)
    for t in free:
        u0[t] = [i for i in range(3) if flow[('t', t)][('x', faces[t][i])] == 1][0]
    # constraints: for spoke (t,i) reference direction t->corner unless u0[t]==i (corner->t)
    cons = []
    for (t, i), (Lp, Rm) in sp.items():
        L, R = (Lp, Rm) if u0[t] != i else (Rm, Lp)
        if L != R:
            cons.append((L, R, t, i))
    nodes = sorted({x for c in cons for x in c[:2]}, key=str)
    D = nx.DiGraph()
    for L, R, t, i in cons:   # phi(R) <= phi(L) ; phi(L) <= phi(R) + 1
        for (a, b, w) in ((L, R, 0), (R, L, 1)):
            if D.has_edge(a, b):
                D[a][b]['weight'] = min(D[a][b]['weight'], w)
            else:
                D.add_edge(a, b, weight=w)
    hi = nx.single_source_bellman_ford_path_length(D, 'O')
    lo = {k: -v for k, v in nx.single_source_bellman_ford_path_length(D.reverse(), 'O').items()}

    def feasible(phi):
        return all(phi[R] - phi[L] in (-1, 0) for L, R, t, i in cons) and phi['O'] == 0

    assert feasible(hi) and feasible(lo)

    def u_of(phi):
        u = {}
        for t in A:
            got = []
            for i in range(3):
                Lp, Rm = sp[(t, i)]
                L, R = (Lp, Rm) if u0[t] != i else (Rm, Lp)
                rev = (L != R) and (phi[R] - phi[L] == -1)
                into = (u0[t] == i) != rev
                if into:
                    got.append(i)
            assert len(got) == 1
            u[t] = got[0]
        return u

    def tree_pair(u):
        adj = {x: [] for x in X}
        for t in A:
            f = faces[t]; a, b = f[(u[t] + 1) % 3], f[(u[t] + 2) % 3]
            adj[a].append((b, t)); adj[b].append((a, t))
        seen = set(); cycles = []
        for x0 in X:
            if x0 in seen:
                continue
            cyc = []; x = x0; prev = None
            while True:
                seen.add(x)
                y, t = [e for e in adj[x] if e[1] != prev][0] if prev is not None else adj[x][0]
                cyc.append((x, y, t)); prev = t; x = y
                if x == x0:
                    break
            cycles.append(cyc)
        for mask in itertools.product((0, 1), repeat=len(cycles)):
            Q = nx.Graph(); Q.add_nodes_from(rot)
            for bit, cyc in zip(mask, cycles):
                for x, y, t in cyc:
                    tail = x if bit == 0 else y
                    Q.add_edge(tail, faces[t][u[t]])
            if Q.number_of_edges() == len(A) and nx.is_forest(Q):
                return True, len(cycles)
        return False, len(cycles)

    def covers(phi, d):
        cands = []
        for a in nodes:
            if a == 'O':
                continue
            q = dict(phi); q[a] += d
            changed = True; ok = True
            while changed and ok:
                changed = False
                for L, R, t, i in cons:
                    if d > 0:
                        if q[R] < q[L] - 1: q[R] = q[L] - 1; changed = True
                        if q[L] < q[R]: q[L] = q[R]; changed = True
                    else:
                        if q[R] > q[L]: q[R] = q[L]; changed = True
                        if q[L] > q[R] + 1: q[L] = q[R] + 1; changed = True
                if q['O'] != 0: ok = False
            if ok:
                assert feasible(q)
                cands.append(q)
        def le(p, q): return all(p[k] <= q[k] for k in nodes)
        uniq = []
        for q in cands:
            if q not in uniq: uniq.append(q)
        if d > 0:
            return [q for q in uniq if not any(r != q and le(r, q) for r in uniq)]
        return [q for q in uniq if not any(r != q and le(q, r) for r in uniq)]

    print(f"V={len(rot)} n={len(A)} faces of H_0={len(nodes)} extremes equal={lo == hi}")
    front = {0: [lo], 1: [hi]}
    for d in range(maxd + 1):
        res = []
        for side in (0, 1):
            for phi in front[side]:
                res.append((side, tree_pair(u_of(phi))))
        print(f"distance {d}: elements {len(res)}; carrying a tree pair: {sum(r[1][0] for r in res)}; D-cycle counts {sorted(r[1][1] for r in res)[:12]}")
        if any(r[1][0] for r in res):
            print("nearest tree-pair element at distance", d); return
        for side in (0, 1):
            nxt = []
            for phi in front[side]:
                for q in covers(phi, +1 if side == 0 else -1):
                    if q not in nxt: nxt.append(q)
            front[side] = nxt


main()
