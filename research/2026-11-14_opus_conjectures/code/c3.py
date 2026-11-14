"""Test of C3 (monotone descent) on random rooted instances.

A state of the search is an ordered pair (r, s).  Moves:
  D-swap along a cycle C of D(r,s):   r <-> s on the faces supplying C;
  Q-reversal along a cycle K of Q_s:  r(t) := u(t) on the faces supplying K  (s unchanged).
k(r,s) = number of cycles of Q_s.  A move p -> q is allowed iff k(q) <= k(p).
C3 says: from every pair, k = 0 is reachable by allowed moves.  Reachability from a start is
a plain BFS (allowedness depends only on the current pair).

Start pairs: random elements of the 2-factor lattice (random walk by covers from both
extremes, computed with the relaxation code of verify_near.py) with random cycle orientations,
plus the two extremes with all orientations when c <= 6.
Usage: python c3.py instances_file first last starts_per_instance cap seed
"""
import sys, random, itertools
import networkx as nx
sys.path.insert(0, __import__('os').path.dirname(__file__))


def parse(line):
    a = list(map(int, line.split()))
    V = a[0]; p = 1; rot = {}
    for v in range(V):
        d = a[p]; rot[v] = a[p + 1:p + 1 + d]; p += 1 + d
    roots = set(a[p:p + 3]) if len(a) >= p + 3 else None
    return rot, roots


def faces_of(rot):
    pos = {v: {w: i for i, w in enumerate(ns)} for v, ns in rot.items()}
    face_of, faces = {}, []
    for v in rot:
        for w in rot[v]:
            if (v, w) in face_of:
                continue
            f = []; d = (v, w)
            while d not in face_of:
                face_of[d] = len(faces); f.append(d[0])
                a, b = d; d = (b, rot[b][pos[b][a] - 1])
            faces.append(tuple(f))
    return faces, face_of


class Inst:
    def __init__(self, rot, roots):
        self.rot = rot
        faces, face_of = faces_of(rot)
        self.faces = faces
        t0 = [i for i, f in enumerate(faces) if set(f) == roots][0]
        col = {t0: 0}; st = [t0]
        while st:
            f = st.pop(); a, b, c = faces[f]
            for x, y in ((a, b), (b, c), (c, a)):
                g = face_of[(y, x)]
                if g not in col:
                    col[g] = 1 - col[f]; st.append(g)
        self.A = [i for i in range(len(faces)) if col[i] == 0 and i != t0]
        self.roots = roots
        self.X = [v for v in rot if v not in roots]
        self.t_index = {t: k for k, t in enumerate(self.A)}

    # pairs are tuples (r, s) of tuples indexed like self.A
    def third(self, k, a, b):
        return next(v for v in self.faces[self.A[k]] if v != a and v != b)

    def dcycles(self, r, s):
        succ = {r[k]: (s[k], k) for k in range(len(self.A))}
        seen = set(); out = []
        for x in succ:
            if x in seen:
                continue
            cyc = []; y = x
            while y not in seen:
                seen.add(y); nxt, k = succ[y]; cyc.append(k); y = nxt
            out.append(cyc)
        return out

    def qcycles(self, r, s):
        # functional graph: x = r(t) -> u(t) along the Q_s edge of t
        f = {}
        for k in range(len(self.A)):
            f[r[k]] = (self.third(k, r[k], s[k]), k)
        color = {}; cycles = []
        for x0 in f:
            if x0 in color:
                continue
            path = []; x = x0
            while x in f and x not in color:
                color[x] = x0; path.append(x); x = f[x][0]
            if x in f and color.get(x) == x0:
                # cycle found starting at x
                cyc = []; y = x
                while True:
                    nxt, k = f[y]; cyc.append(k); y = nxt
                    if y == x:
                        break
                cycles.append(cyc)
        return cycles

    def k(self, r, s):
        return len(self.qcycles(r, s))

    def moves(self, r, s):
        out = []
        for cyc in self.dcycles(r, s):
            r2, s2 = list(r), list(s)
            for k in cyc:
                r2[k], s2[k] = s[k], r[k]
            out.append((tuple(r2), tuple(s2)))
        for cyc in self.qcycles(r, s):
            r2 = list(r)
            for k in cyc:
                r2[k] = self.third(k, r[k], s[k])
            out.append((tuple(r2), s))
        return out


def search(I, start, cap):
    k0 = I.k(*start)
    if k0 == 0:
        return 0, 1
    kk = {start: k0}
    frontier = [start]; seen = {start}
    while frontier:
        nxt = []
        for p in frontier:
            for q in I.moves(*p):
                if q in seen:
                    continue
                kq = I.k(*q)
                if kq > kk[p]:
                    continue
                if kq == 0:
                    return 0, len(seen)
                seen.add(q); kk[q] = kq; nxt.append(q)
                if len(seen) >= cap:
                    return None, len(seen)
        frontier = nxt
    return min(kk.values()), len(seen)


def pair_from_u(I, u, rng):
    """u: dict A-index -> deleted corner vertex; random orientation of the D-cycles"""
    adj = {x: [] for x in I.X}
    for k in range(len(I.A)):
        a, b = [v for v in I.faces[I.A[k]] if v != u[k]]
        adj[a].append((b, k)); adj[b].append((a, k))
    r, s = [None] * len(I.A), [None] * len(I.A)
    seen = set()
    for x0 in I.X:
        if x0 in seen:
            continue
        bit = rng.random() < 0.5; x = x0; prev = None
        while True:
            seen.add(x)
            y, k = [e for e in adj[x] if e[1] != prev][0] if prev is not None else adj[x][0]
            r[k], s[k] = (x, y) if bit else (y, x)
            prev = k; x = y
            if x == x0:
                break
    return tuple(r), tuple(s)


def flow_u(I):
    G = nx.DiGraph(); forced = {}
    for k, t in enumerate(I.A):
        f = I.faces[t]
        rc = [v for v in f if v in I.roots]
        if rc:
            forced[k] = rc[0]; continue
        G.add_edge('s', ('t', k), capacity=1)
        for v in f:
            G.add_edge(('t', k), ('x', v), capacity=1)
    for x in I.X:
        G.add_edge(('x', x), 'z', capacity=len(I.rot[x]) // 2 - 2)
    val, flow = nx.maximum_flow(G, 's', 'z')
    u = dict(forced)
    for k in range(len(I.A)):
        if k in u:
            continue
        got = [v for v in I.faces[I.A[k]] if flow[('t', k)].get(('x', v), 0) == 1]
        if not got:
            return None
        u[k] = got[0]
    if len(u) != len(I.A):
        return None
    return u


def random_pairs(I, rng, count, walk=60):
    """random walk on pairs by arbitrary exchange moves (D-swaps and Q-reversals),
    which moves between 2-factors; returns sampled pairs"""
    u = flow_u(I)
    if u is None:
        return []
    p = pair_from_u(I, u, rng)
    out = []
    for _ in range(count):
        for _ in range(walk):
            ms = I.moves(*p)
            if not ms:
                break
            p = rng.choice(ms)
        out.append(p)
    return out


def trap(fn, cap):
    import json
    d = json.load(open(fn))
    rot = {int(k): v for k, v in d['rot'].items()}
    I = Inst(rot, set(d['t0']))
    def m(x):
        return {tuple(sorted(t)): v for t, v in x}
    rr, ss = m(d['r']), m(d['s'])
    key = lambda t: tuple(sorted(I.faces[t]))
    p = (tuple(rr[key(t)] for t in I.A), tuple(ss[key(t)] for t in I.A))
    print("trap", fn, "k =", I.k(*p), "search ->", search(I, p, cap))


def main():
    if sys.argv[1] == 'trap':
        trap(sys.argv[2], int(sys.argv[3])); return
    fn, first, last, starts, cap, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    rng = random.Random(seed)
    lines = [l for l in open(fn) if l.strip()]
    tot = fails = capped = 0
    worst = 0
    for li in range(first, min(last, len(lines))):
        rot, roots = parse(lines[li])
        if roots is None:
            faces, _ = faces_of(rot)
            roots = set(rng.choice(faces))
        I = Inst(rot, roots)
        for p in random_pairs(I, rng, starts):
            if I.k(*p) == 0:
                continue
            res, size = search(I, p, cap)
            tot += 1
            worst = max(worst, size)
            if res is None:
                capped += 1
            elif res > 0:
                fails += 1
                print("C3FAIL line", li, "k_start", I.k(*p), "reachable", size, "min k", res, flush=True)
    print(f"C3 starts={tot} failures={fails} capped={capped} largest_search={worst}")


main()
