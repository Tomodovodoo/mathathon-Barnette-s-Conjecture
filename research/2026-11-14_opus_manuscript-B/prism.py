"""Hexagonal prism: compare good states with Hamiltonian cycles avoiding e0*.
Run: python research/2026-11-14_opus_manuscript-B/prism.py
T = hexagonal bipyramid (apexes N=6, S=7, equator 0..5)."""
import itertools as it
N, S = 6, 7
F = [(i, (i + 1) % 6, N) for i in range(6)] + [((i + 1) % 6, i, S) for i in range(6)]
left = {}
for k, f in enumerate(F):
    for a, b in zip(f, f[1:] + f[:1]):
        assert (a, b) not in left
        left[a, b] = k
E = sorted({tuple(sorted(x)) for x in left})
col = {}
for k in range(6):
    col[k] = k % 2          # north faces alternate
    col[6 + k] = 1 - k % 2  # south face below north face k has the opposite colour
for (a, b), k in left.items():
    assert col[k] != col[left[b, a]]
t0 = 0
black = [k for k in col if col[k] == col[t0]]
roots = list(F[t0])
A = [t for t in black if t != t0]
X = [v for v in range(8) if v not in roots]
n = len(A)
states = [dict(zip(A, c)) for c in it.product(*[[v for v in F[t] if v not in roots] for t in A]) if len(set(c)) == n]
pairs = [(r, s) for r in states for s in states if all(r[t] != s[t] for t in A)]


def comps(V, edges):
    p = {v: v for v in V}
    def f(x):
        while p[x] != x:
            x = p[x]
        return x
    cyc = False
    for a, b in edges:
        ra, rb = f(a), f(b)
        if ra == rb:
            cyc = True
        p[ra] = rb
    g = {}
    for v in V:
        g.setdefault(f(v), []).append(v)
    return cyc, list(g.values())


good = []
for s in states:
    Q = [tuple(v for v in F[t] if v != s[t]) for t in A]
    cyc, cs = comps(range(8), Q)
    if not cyc and all(sum(1 for v in c if v in roots) == 1 for c in cs):
        good.append(s)
e0 = (0, 1)
G = {k: set() for k in range(len(F))}
for a, b in E:
    G[left[a, b]].add(left[b, a]); G[left[b, a]].add(left[a, b])
avoid = frozenset((left[0, 1], left[1, 0]))
found = set()
def dfs(path, used):
    v = path[-1]
    if len(path) == len(F):
        if path[0] in G[v] and frozenset((v, path[0])) != avoid:
            c = path + [path[0]]
            found.add(frozenset(frozenset(x) for x in zip(c, c[1:])))
        return
    for w in G[v]:
        if w not in used and frozenset((v, w)) != avoid:
            used.add(w); path.append(w); dfs(path, used); path.pop(); used.discard(w)
dfs([t0], {t0})
print('n =', n, 'states', len(states), 'pairs', len(pairs), 'good states', len(good), 'Hamiltonian cycles avoiding e0*', len(found))

# the state assigned to each avoiding cycle (Lemma 3.1 of the draft) and whether it has a partner
e0 = (0, 1)
a, b = e0
for cyc in found:
    Pstar = {frozenset(x) for x in [tuple(sorted(e)) for e in E]}
    # edges of T crossed by the cycle
    crossed = set()
    for gedge in cyc:
        i, k = tuple(gedge)
        (e,) = [tuple(sorted(x)) for x in left if left[x] == i and left[(x[1], x[0])] == k]
        crossed.add(e)
    P = [e for e in E if e not in crossed]
    P0 = [e for e in P if e != tuple(sorted(e0))]
    # orient P0 towards the roots
    adj = {v: [] for v in range(8)}
    for x, y in P0:
        adj[x].append(y); adj[y].append(x)
    parent = {}
    for rt in roots:
        parent[rt] = None
        st = [rt]
        while st:
            v = st.pop()
            for w in adj[v]:
                if w not in parent:
                    parent[w] = v; st.append(w)
    s = {}
    for t in A:
        (e,) = [e for e in P0 if set(e) <= set(F[t])]
        tail = e[0] if parent.get(e[0]) == e[1] else e[1]
        s[t] = tail
    has_partner = any(all(r[t] != s[t] for t in A) for r in states)
    print('cycle state', [s[t] for t in A], 'good' if s in good else 'not good', 'partner' if has_partner else 'no partner')
