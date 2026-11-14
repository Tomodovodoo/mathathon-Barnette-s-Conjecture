"""Step X (no trap) on chosen triangulations, exhaustively per rooted instance.
Rainbow trees are enumerated per 2-factor as the acyclic selections (Theorem S, which
check_rainbow.py S verifies against brute force for V <= 12). Instances with one 2-factor are
recorded as covered by Proposition U and also checked when small enough.
Usage: python stepx.py V idx1,idx2,... [time_limit_s]   Output ../data/stepx_V_<tag>.json"""
import sys, json, time, itertools
from collections import Counter
from core import plantri, Tri, Rooted
import rb


def trees_by_factor(R):
    F2s = R.two_factors()
    X = R.X
    out = set()
    for u in F2s:
        fac = [[t for t in R.bat[x] if u[t] != x] for x in X]
        for bits in itertools.product((0, 1), repeat=len(X)):
            nxt = {x: u[fac[i][1 - b]] for i, (x, b) in enumerate(zip(X, bits))}
            ok = True
            for x in X:
                seen = set(); y = x
                while y in nxt and y not in seen:
                    seen.add(y); y = nxt[y]
                if y in nxt:
                    ok = False; break
            if ok:
                out.add(tuple(fac[i][b] for i, b in enumerate(bits)))
    return out, len(F2s)


def alts(R, sig):
    """alt_sigma(x) for all x at once, via parent pointers of F_sigma rooted at t0's centre."""
    adj = rb.tree_adj(R, sig)
    root = R.cidx[R.t0]
    par = {root: None}; depth = {root: 0}; st = [root]
    while st:
        a = st.pop()
        for b in adj[a]:
            if b not in par:
                par[b] = a; depth[b] = depth[a] + 1; st.append(b)
    res = {}
    for x in R.X:
        c = R.cidx[sig[x]]
        # is x an ancestor of c? walk up from c to depth(x)+1
        y = c
        while depth[y] > depth[x] + 1:
            y = par[y]
        if par[y] == x:
            res[x] = R.black[y - R.T.V]
        else:
            res[x] = R.black[par[x] - R.T.V]
    return res


def check_instance(R, trees, deadline):
    X = R.X
    ex = {}
    for k in trees:
        c = Counter(k)
        ex[k] = sum(abs(c.get(t, 0) - 1) for t in R.A)
    reach = {k for k in trees if ex[k] == 0}
    frontier = list(reach)
    maxdepth = 0
    while frontier:
        if time.time() > deadline:
            return None
        nxt = []
        for k in frontier:
            al = alts(R, dict(zip(X, k)))
            for i, x in enumerate(X):
                k2 = k[:i] + (al[x],) + k[i + 1:]
                assert k2 in ex, 'move left the set of rainbow trees'
                if k2 not in reach and ex[k2] >= ex[k]:
                    reach.add(k2); nxt.append(k2)
        frontier = nxt
    return len(reach) == len(trees), sum(1 for v in ex.values() if v == 0)


if __name__ == '__main__':
    V = int(sys.argv[1]); idxs = [int(a) for a in sys.argv[2].split(',')]
    limit = float(sys.argv[3]) if len(sys.argv) > 3 else 500
    t0 = time.time(); deadline = t0 + limit
    rots = plantri(V)
    out = Counter(); rows = []
    for idx in idxs:
        tri = Tri(rots[idx])
        done = True
        for f0 in range(len(tri.faces)):
            if time.time() > deadline:
                done = False; break
            R = Rooted(tri, f0)
            if R.has_black_inner():
                out['no_rainbow'] += 1; continue
            trees, nf = trees_by_factor(R)
            if nf == 1:
                out['one_2factor_PropU'] += 1
                assert len(trees) == 2 ** R.n
                continue
            r = check_instance(R, trees, deadline)
            if r is None:
                done = False; break
            ok, ngood = r
            out['multi_checked_ok' if ok else 'multi_TRAP'] += 1
            out['trees_enumerated'] += len(trees)
            rows.append([idx, list(tri.faces[f0]), nf, len(trees), ngood, ok])
        rows.append(['triangulation', idx, 'complete' if done else 'INCOMPLETE'])
        print(idx, done, dict(out), round(time.time() - t0), flush=True)
        if not done:
            break
    json.dump({'command': 'python stepx.py ' + ' '.join(sys.argv[1:]), 'counts': dict(out), 'rows': rows,
               'seconds': round(time.time() - t0, 1)},
              open(f'../data/stepx_{V}_{sys.argv[2].replace(",", "-")[:40]}.json', 'w'), indent=1)
