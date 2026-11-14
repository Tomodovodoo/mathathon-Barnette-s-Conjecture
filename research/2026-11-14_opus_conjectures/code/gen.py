"""Random Eulerian triangulations, written in bar.c -t text format (ccw rotations, 0-based).

Models
  ins    : octahedron + random degree-4 insertions (vertex split), vertex chosen uniformly
  skew   : as ins, vertex chosen with probability proportional to deg^3 (hubs)
  mcmc   : grow to V by ins, then many insert/delete steps (delete = inverse merge at a
           degree-4 vertex, only when the result stays simple); a walk that mixes better
  glue   : glue random pieces (each made by ins) along faces; many separating triangles
  prism  : glue hexagonal bipyramids (V=8, dual of the hexagonal prism) along faces
Usage: python gen.py model V count seed [mcmc_steps]
"""
import random, sys


def octahedron():
    # vertices 0..5: 0 top, 5 bottom, 1..4 equator ccw seen from top
    rot = {0: [1, 2, 3, 4], 5: [4, 3, 2, 1]}
    for i in range(1, 5):
        nx, pv = i % 4 + 1, (i - 2) % 4 + 1
        rot[i] = [0, pv, 5, nx]
    return rot


def check(rot):
    # each consecutive pair (a,b) in rot[v] must form a face (v,a,b): b follows... verify triangles
    for v, ns in rot.items():
        d = len(ns)
        assert d % 2 == 0 and d >= 4, (v, ns)
        assert len(set(ns)) == d
        for k in range(d):
            a, b = ns[k], ns[(k + 1) % d]
            # face (v, a, b) ccw: at a, v must follow b  (face (a, b, v))
            ra = rot[a]; i = ra.index(b)
            assert ra[(i + 1) % len(ra)] == v, ("bad face", v, a, b)


def split(rot, v, i, k, newid):
    """split v at neighbours w_i and w_{i+k} (k even, 2<=k<=d-2) inserting degree-4 vertex x"""
    ns = rot[v]; d = len(ns)
    w = [ns[(i + m) % d] for m in range(d)]   # w[0]=w_i ... w[k]=w_j
    v1, v2, x = v, newid, newid + 1
    arc1 = w[0:k + 1]
    arc2 = w[k:] + [w[0]]
    old = {u: list(rot[u]) for u in w}
    rot[v1] = arc1 + [x]
    rot[v2] = arc2 + [x]
    rot[x] = [w[0], v1, w[k], v2]
    inside = set(w[1:k])
    for u in w:
        r = old[u]; p = r.index(v)
        if u == w[0]:
            rep = [v1, x, v2]
        elif u == w[k]:
            rep = [v2, x, v1]
        elif u in inside:
            rep = [v1]
        else:
            rep = [v2]
        rot[u] = r[:p] + rep + r[p + 1:]


def random_split(rot, rng, weight=None):
    vs = list(rot)
    if weight:
        ws = [len(rot[u]) ** weight for u in vs]
        v = rng.choices(vs, ws)[0]
    else:
        v = rng.choice(vs)
    d = len(rot[v])
    i = rng.randrange(d)
    k = rng.choice(range(2, d - 1, 2))
    split(rot, v, i, k, max(rot) + 1)


def collapse(r, first, mid, last, new):
    k = r.index(first)
    r = r[k:] + r[:k]
    assert r[1] == mid and r[2] == last, (r, first, mid, last)
    return [new] + r[3:]


def try_delete(rot, x, rng):
    """merge two opposite neighbours of a degree-4 vertex x (inverse of split); True if done"""
    p = rot[x]
    if len(p) != 4:
        return False
    off = rng.randrange(2)
    a, v1, b, v2 = p[off], p[off + 1], p[(off + 2) % 4], p[(off + 3) % 4]
    if v2 in rot[v1]:
        return False
    if (set(rot[v1]) & set(rot[v2])) - {a, b, x}:
        return False
    if len(rot[a]) < 6 or len(rot[b]) < 6:
        return False
    l1 = rot[v1]; i = l1.index(a); l1 = l1[i:] + l1[:i]
    l2 = rot[v2]; j = l2.index(b); l2 = l2[j:] + l2[:j]
    assert l1[-1] == x and l2[-1] == x, (l1, l2, x)
    v = v1
    newl = l1[:-1] + l2[1:-2]
    rot[a] = collapse(rot[a], v1, x, v2, v)
    rot[b] = collapse(rot[b], v2, x, v1, v)
    for u in set(newl) - {a, b}:
        rot[u] = [v if y == v2 else y for y in rot[u]]
    del rot[x]; del rot[v2]
    rot[v] = newl
    return True


def relabel(rot):
    idx = {v: i for i, v in enumerate(sorted(rot))}
    return {idx[v]: [idx[w] for w in ns] for v, ns in rot.items()}


def glue(r1, r2, f1, f2):
    """glue r2 into r1: remove face f1=(a,b,c) of r1 (ccw) and f2=(p,q,s) of r2 (ccw), identify a-p, b-s... orientation reversing"""
    off = max(r1) + 1
    r2 = {v + off: [w + off for w in ns] for v, ns in r2.items()}
    a, b, c = f1
    p, q, s = [v + off for v in f2]
    # identify a<->p, b<->s, c<->q (reverse orientation so the faces glue)
    ident = {p: a, s: b, q: c}
    rot = {v: list(ns) for v, ns in r1.items()}
    for v, ns in r2.items():
        if v in ident:
            continue
        rot[v] = [ident.get(w, w) for w in ns]
    for old, new in ident.items():
        # at new (in r1): face (new, x, y) of f1 is consecutive; insert r2's neighbours there
        l2 = [ident.get(w, w) for w in r2[old]]
        l1 = rot[new]
        # f1 = (a,b,c) ccw: at a, the face (a,b,c) means b then c consecutive in rot[a]
        nxt = {a: (b, c), b: (c, a), c: (a, b)}[new]
        i = l1.index(nxt[0]); assert l1[(i + 1) % len(l1)] == nxt[1]
        # in r2, face (p,q,s) ccw: at the old vertex, its two face-neighbours are consecutive
        u1, u2 = nxt[1], nxt[0]  # in r2 coordinates (after ident) the order is reversed
        j = l2.index(u1)
        assert l2[(j + 1) % len(l2)] == u2, ("glue orientation", l2, u1, u2)
        # l2 rotated to start after u2 and end before u1: the interior part
        l2r = l2[(j + 2) % len(l2):] + l2[:(j + 2) % len(l2)]
        inner = l2r[:-2]
        # new list: l1 up to nxt[0], then inner (reversed?), then nxt[1]...
        rot[new] = l1[:i + 1] + inner + l1[i + 1:]
    return rot


def faces(rot):
    out = []
    for v, ns in rot.items():
        for k in range(len(ns)):
            a, b = ns[k], ns[(k + 1) % len(ns)]
            if v < a and v < b:
                out.append((v, a, b))
    return out


def face_classes(rot):
    """2-colour faces; class 0 contains the anchor face (0,1,2) of the base"""
    fs = faces(rot)
    key = {}
    for f in fs:
        for i in range(3):
            key[(f[i], f[(i + 1) % 3])] = f
    col = {}
    anchor = [f for f in fs if set(f) == {0, 1, 2}][0]
    col[anchor] = 0; st = [anchor]
    while st:
        f = st.pop()
        for i in range(3):
            g = key[(f[(i + 1) % 3], f[i])]
            if g not in col:
                col[g] = 1 - col[f]; st.append(g)
    return col


def make(model, V, rng, steps=0):
    rot = octahedron()
    if model in ('ins', 'skew', 'mcmc'):
        while len(rot) < V:
            random_split(rot, rng, weight=3 if model == 'skew' else None)
        if model == 'mcmc':
            for _ in range(steps):
                if rng.random() < 0.5 and len(rot) > V - 6:
                    cand = [u for u in rot if len(rot[u]) == 4]
                    if cand:
                        try_delete(rot, rng.choice(cand), rng)
                else:
                    if len(rot) < V + 6:
                        random_split(rot, rng)
            while len(rot) < V:
                random_split(rot, rng)
            while len(rot) > V:
                cand = [u for u in rot if len(rot[u]) == 4]
                rng.shuffle(cand)
                for u in cand:
                    if try_delete(rot, u, rng):
                        break
        return relabel(rot)
    if model in ('glue', 'prism'):
        rot = relabel(octahedron()) if model == 'glue' else hexbip()
        while len(rot) < V:
            if model == 'prism':
                piece = hexbip()
            else:
                pv = rng.choice([6, 8, 10, 12, 14])
                piece = octahedron()
                while len(piece) < pv:
                    random_split(piece, rng)
                piece = relabel(piece)
            if len(rot) + len(piece) - 3 > V + 4:
                break
            col = face_classes(rot)
            f1 = rng.choice([f for f in col if col[f] == 1]); f2 = rng.choice(faces(piece))
            rot = relabel(glue(rot, piece, f1, f2))
        while len(rot) < V:
            random_split(rot, rng)
        return rot
    raise ValueError(model)


def hexbip():
    # hexagonal bipyramid: apexes 0 (top), 7 (bottom), equator 1..6 ccw from top
    rot = {0: [1, 2, 3, 4, 5, 6], 7: [6, 5, 4, 3, 2, 1]}
    for i in range(1, 7):
        nx, pv = i % 6 + 1, (i - 2) % 6 + 1
        rot[i] = [0, pv, 7, nx]
    return rot


def line(rot):
    parts = [str(len(rot))]
    for v in range(len(rot)):
        parts.append(str(len(rot[v]))); parts += [str(w) for w in rot[v]]
    return ' '.join(parts)


if __name__ == '__main__':
    model, V, count, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    steps = int(sys.argv[5]) if len(sys.argv) > 5 else 20 * V
    rng = random.Random(seed)
    for _ in range(count):
        rot = make(model, V, rng, steps)
        check(rot)
        print(line(rot))
