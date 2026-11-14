"""Classifies the rotation exceptions written by census.py.
usage: python residual.py OUT.json FILE [FILE ...]   (jsonl or jsonl.gz)"""
import sys, json, gzip, collections


def rows_of(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as f:
        for line in f:
            yield json.loads(line)


out = sys.argv[1]
per_v = collections.defaultdict(collections.Counter)
by_x = collections.defaultdict(collections.Counter)
viol = collections.Counter()
for path in sys.argv[2:]:
    for r in rows_of(path):
        V = r["V"]
        x, a, v1, b, v2, c = r["x"], r["a"], r["v1"], r["b"], r["v2"], r["c"]
        outer = [tuple(f) for f in r["outer"]]
        assign = r["assign"]
        t0 = r["t0"]
        deg = collections.Counter()
        for f in r["blacks"]:
            for v in f:
                deg[v] += 2
        gp = next(f for f in outer if b in f and v1 in f)
        (cp,) = [v for v in gp if v not in (b, v1)]
        sgp = assign[outer.index(gp)]
        g = next(f for f in outer if a in f and v2 in f)
        C = per_v[V]
        C["exceptions"] += 1
        C["class A: g' takes b"] += sgp == b
        C["class B: g' takes v1"] += sgp == v1
        C["g' takes c' (never, by pattern P_1)"] += sgp == cp
        C["g takes a (always, local condition)"] += assign[outer.index(g)] == a
        C["root neighbours of x: %d" % len(r["rootnbrs"])] += 1
        C["c = b"] += c == b
        C["c' = a"] += cp == a
        C["c = c' (would make T/M non-simple)"] += c == cp
        C["deg profile (a,v1,b,v2) = %s" % (tuple(deg[u] for u in (a, v1, b, v2)),)] += 0
        C["min degree among a,b,v1,v2 = %d" % min(deg[u] for u in (a, v1, b, v2))] += 1
        C["v1 is a root"] += v1 in t0
        C["a is a root"] += a in t0
        C["b is a root"] += b in t0
        # floating component: which of K1, K2 holds the roots
        par = {}
        def find(u):
            while par.get(u, u) != u:
                u = par[u]
            return u
        for f, u in zip(outer, assign):
            p, q = [w for w in f if w != u]
            par[find(p)] = find(q)
        par[find(t0[0])] = find(t0[1]); par[find(t0[1])] = find(t0[2])
        if not (find(a) == find(v1) and find(b) == find(v2) and find(a) != find(b)):
            viol["not pattern P_1"] += 1
        C["roots on the K1 side (with a, v1)"] += find(t0[0]) == find(a)
        C["roots on the K2 side (with b, v2)"] += find(t0[0]) == find(b)
        by_x[(V, r["gid"], tuple(t0), x)][frozenset((v1, v2))] += 1
unbalanced = sum(1 for k, cnt in by_x.items() if len(set(cnt.values())) != 1 or len(cnt) != 2)
res = dict(per_V={V: {k: v for k, v in sorted(C.items()) if v} for V, C in sorted(per_v.items())},
           vertex_root_pairs_with_exceptions=len(by_x),
           pairs_where_the_two_merges_have_different_exception_counts=unbalanced,
           violations=dict(viol))
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
