"""Check Lemma B of PROOFS.md with the spoke weights of the reference lab (Instance.weights()).

For every pair (r, s) of every rooted instance with V vertices:
  (a) w_r + w_s + w_u is the same for all pairs of the instance;
  (b) a D-swap fixes w_u and changes w_s by a nonzero amount d, and w_r by -d;
  (c) a Q-reversal fixes w_s and changes w_u by a nonzero amount d, and w_r by -d;
  (d) |d| equals the number of white faces inside the reversed cycle (flood fill in the dual
      from the outer face, not crossing the cycle).
Usage: python verify_heights.py V  -> one JSON line
"""
import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'workings/barnette_lab'))
from barnette_lab.core import Instance, plantri_graphs, edge

V = int(sys.argv[1])
P = ROOT / 'workings/barnette_lab/vendor/plantri.exe'
stats = dict(V=V, rooted=0, pairs=0, d_swaps=0, q_reversals=0, failures=0, max_abs_change=0)


def white_inside(b, cyc_edges):
    blocked = {edge(*e) for e in cyc_edges}
    out = {b.outer}; st = [b.outer]
    while st:
        f = st.pop(); q = b.faces[f]
        for x, y in zip(q, q[1:] + q[:1]):
            if edge(x, y) in blocked:
                continue
            g = b.sides[y, x]
            if g not in out:
                out.add(g); st.append(g)
    return sum(1 for f in b.white if f not in out)


for t in plantri_graphs(V, P):
    probe = Instance(t)
    for f in range(len(probe.faces)):
        b = Instance(t, f)
        if b.flow_pair() is None:
            continue
        pairs = b.pairs()
        if not pairs:
            continue
        a = b.weights()
        stats['rooted'] += 1; stats['pairs'] += len(pairs)

        def heights(p):
            r, s = p
            u = [next(iter(set(b.faces[tt]) - {x, y})) for tt, x, y in zip(b.A, r, s)]
            w = lambda m: sum(a.get((tt, v), 0) for tt, v in zip(b.A, m))
            return w(r), w(s), w(u)
        total = None
        for p in pairs:
            wr, ws, wu = heights(p)
            if total is None:
                total = wr + ws + wu
            if wr + ws + wu != total:
                stats['failures'] += 1
            idx = {tt: i for i, tt in enumerate(b.A)}
            for c in b.dcycles(*p):
                q = b.reverse_d(p, c); wr2, ws2, wu2 = heights(q)
                W = white_inside(b, [(p[0][idx[tt]], p[1][idx[tt]]) for tt in c])
                d = ws2 - ws
                stats['d_swaps'] += 1; stats['max_abs_change'] = max(stats['max_abs_change'], abs(d))
                if wu2 != wu or wr2 - wr != -d or abs(d) != W or W < 1:
                    stats['failures'] += 1
            for c in b.qcycles(p[1]):
                q = b.reverse_q(p, c); wr2, ws2, wu2 = heights(q)
                W = white_inside(b, [(p[0][idx[tt]], q[0][idx[tt]]) for tt in c])
                d = wu2 - wu
                stats['q_reversals'] += 1; stats['max_abs_change'] = max(stats['max_abs_change'], abs(d))
                if ws2 != ws or wr2 - wr != -d or abs(d) != W or W < 1:
                    stats['failures'] += 1
print(json.dumps(stats))
