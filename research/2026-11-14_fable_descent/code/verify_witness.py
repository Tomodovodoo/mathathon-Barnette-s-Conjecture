"""Independent check of the k-witnesses in data/witnesses.txt with the reference lab.

Shares no code with descent.cpp / walk.cpp: faces, colours, D-cycles and Q-cycles come from
barnette_lab (networkx embedding, nx.simple_cycles, nx.cycle_basis).
For lines "W SINK pot=k ..."      : checks k >= 1 and that no exchange neighbour has smaller k.
For lines "W RHO [pot=k] ..."     : checks that the nearest pair with smaller k is at distance rho
                                    (BFS in the exchange graph), and that a non-increasing path to
                                    k = 0 exists (C3 for this start).
Other lines are skipped.
Usage: python verify_witness.py ../data/witnesses.txt > ../data/witnesses_verified.json
"""
import sys, json, re
from pathlib import Path
from collections import deque
import networkx as nx
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'workings/barnette_lab'))
from barnette_lab.core import Instance


def graph_of(text):
    text = text.strip()
    g = nx.Graph()
    if ',' in text:
        n, data = text.split()
        for v, ns in enumerate(data.split(',')):
            g.add_edges_from((v, ord(ch) - ord('a')) for ch in ns)
        return g
    a = list(map(int, text.split())); V = a[0]; p = 1
    for v in range(V):
        d = a[p]
        g.add_edges_from((v, w) for w in a[p + 1:p + 1 + d]); p += 1 + d
    return g


def check(line):
    parts = [x.strip() for x in line.split(' | ')]
    head = parts[0].split()
    kind = head[1]
    kv = dict(x.split('=', 1) for x in head[2:] if '=' in x)
    if kv.get('pot', 'k') != 'k' or kind not in ('SINK', 'RHO'):
        return None
    g = graph_of(parts[1])
    t0 = set(map(int, kv['t0'].split(',')))
    probe = Instance(g)
    outer = next(i for i, f in enumerate(probe.faces) if set(f) == t0)
    b = Instance(g, outer)
    entries = [tuple(map(int, e.split('>'))) for e in parts[-1].split()[1:]]
    assert len(entries) == b.n
    r, s = {}, {}
    for x, y in entries:
        t = next(t for t in b.A if x in b.faces[t] and y in b.faces[t])
        assert t not in r
        r[t], s[t] = x, y
    p = (tuple(r[t] for t in b.A), tuple(s[t] for t in b.A))
    assert b.valid(p[0]) and b.valid(p[1])
    kk = lambda q: len(b.qcycles(q[1]))
    k0 = kk(p)
    out = dict(kind=kind, V=len(g), t0=sorted(t0), k=k0, c=len(b.dcycles(*p)))
    # nearest smaller k
    dist = {p: 0}; q = deque([p]); rho = None
    while q and rho is None:
        a = q.popleft()
        for nb in b.neighbors(a):
            if nb not in dist:
                dist[nb] = dist[a] + 1
                if kk(nb) < k0:
                    rho = dist[nb]; break
                q.append(nb)
    out['rho_lab'] = rho
    claimed = int(kv.get('rho', kv.get('extra', 0)))
    if kind == 'SINK':
        out['ok'] = k0 >= 1 and rho is not None and rho >= 2
    else:
        out['rho_claimed'] = claimed
        out['ok'] = rho == claimed
    # C3 from this start: non-increasing path to k = 0
    seen = {p: k0}; q = deque([p]); reach = k0 == 0
    while q and not reach:
        a = q.popleft()
        for nb in b.neighbors(a):
            if nb in seen:
                continue
            kn = kk(nb)
            if kn > seen[a]:
                continue
            if kn == 0:
                reach = True; break
            seen[nb] = kn; q.append(nb)
    out['c3_from_here'] = reach
    out['c3_pairs_visited'] = len(seen)
    return out


res = []
for line in open(sys.argv[1]):
    if line.startswith('W '):
        o = check(line)
        if o is not None:
            res.append(o)
            print(json.dumps(o), file=sys.stderr)
json.dump(res, sys.stdout, indent=1)
