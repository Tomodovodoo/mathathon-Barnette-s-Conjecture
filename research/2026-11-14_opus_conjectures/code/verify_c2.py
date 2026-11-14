"""Independent check of a C2 counterexample, built on the reference lab (workings/barnette_lab).

Input: one line in bar.c -T text format (V, then deg and neighbours per vertex, then the 3 root
vertices).  Only the edge set is used: the embedding is recomputed by networkx inside the lab.

1. All states and pairs by brute force (lab), grouped into 2-factors (deleted-corner maps u).
2. For each 2-factor: does some ordered pair (r, s) in it have s a tree matching (lab is_tree)?
3. For each 2-factor: orient H_0 (spokes; u(t) -> t, t -> other corners), enumerate ALL directed
   simple cycles (networkx), and classify each as sense +1 or -1 by flood-filling the white
   faces on one fixed side of the cycle and asking whether the outer region lies there.
4. Report the 2-factors with no sense(+1) cycle and with no sense(-1) cycle (the two lattice
   extremes, by Felsner's characterisation) and whether they carry tree pairs.
Usage: python verify_c2.py file [line_index]
"""
import sys
from collections import defaultdict
import networkx as nx
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..', '..', 'workings', 'barnette_lab'))
from barnette_lab.core import Instance

def parse(line):
    a = list(map(int, line.split()))
    V = a[0]; p = 1; edges = []
    for v in range(V):
        d = a[p]; nb = a[p + 1:p + 1 + d]; p += 1 + d
        edges += [(v, w) for w in nb if v < w]
    return nx.Graph(edges), set(a[p:p + 3])

def main():
    lines = [l for l in open(sys.argv[1]) if l.strip()]
    idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    T, roots = parse(lines[idx])
    probe = Instance(T, 0)
    outer = [i for i, f in enumerate(probe.faces) if set(f) == roots][0]
    I = Instance(T, outer)
    ss = list(I.states())
    prs = I.pairs(ss)
    print(f"V={len(T)} n={I.n} states={len(ss)} ordered pairs={len(prs)}")
    tm = [s for s in ss if I.is_tree(s) and any(all(a != b for a, b in zip(r, s)) for r in ss)]
    print("tree matchings (with a partner):", len(tm))
    # group by 2-factor
    fac = defaultdict(list)
    for r, s in prs:
        u = tuple(next(v for v in I.faces[t] if v != a and v != b) for t, a, b in zip(I.A, r, s))
        fac[u].append((r, s))
    print("2-factors:", len(fac))
    # side structure: for black face t traversed (a,b,c), spoke t->a has white face across ab on side '+'
    side = {}
    for t in I.black:
        f = I.faces[t]
        for i in range(3):
            a, b, c = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            side[(t, a)] = (I.sides[b, a], I.sides[a, c])   # (face across ab, face across ca)
    t0 = outer
    outer_white = {w for w in I.white if any(I.sides[a, b] == t0 for a, b in
                   zip(I.faces[w], I.faces[w][1:] + I.faces[w][:1])) or
                   any(I.sides[b, a] == t0 for a, b in zip(I.faces[w], I.faces[w][1:] + I.faces[w][:1]))}
    def node(w):
        return 'O' if w in outer_white else w
    spokes = [(t, v) for t in I.A for v in I.faces[t]]
    results = {}
    for u, plist in fac.items():
        um = dict(zip(I.A, u))
        D = nx.DiGraph()
        for t, v in spokes:
            if um[t] == v: D.add_edge(('v', v), ('t', t))
            else: D.add_edge(('t', t), ('v', v))
        senses = set()
        for cyc in nx.simple_cycles(D):
            cyc_sp = set()
            plus_side = set()
            for x, y in zip(cyc, cyc[1:] + cyc[:1]):
                if x[0] == 't': t, v, fwd = x[1], y[1], True
                else: t, v, fwd = y[1], x[1], False
                cyc_sp.add((t, v))
                fa, fb = side[(t, v)]
                plus_side.add(node(fa) if fwd else node(fb))
            # flood fill over H_0 faces not crossing cycle spokes
            adj = defaultdict(set)
            for t, v in spokes:
                if (t, v) in cyc_sp: continue
                fa, fb = side[(t, v)]
                adj[node(fa)].add(node(fb)); adj[node(fb)].add(node(fa))
            seen = set(plus_side); stack = list(plus_side)
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); stack.append(y)
            senses.add(-1 if 'O' in seen else +1)
        has_tp = any(I.is_tree(s) for r, s in plist)
        ncyc = len(I.dcycles(*plist[0]))
        results[u] = (senses, has_tp, ncyc)
    no_plus = [u for u, (se, _, _) in results.items() if +1 not in se]
    no_minus = [u for u, (se, _, _) in results.items() if -1 not in se]
    print("2-factors with no sense(+1) directed cycle:", len(no_plus), [(results[u][1], results[u][2]) for u in no_plus])
    print("2-factors with no sense(-1) directed cycle:", len(no_minus), [(results[u][1], results[u][2]) for u in no_minus])
    print("all 2-factors (carries tree pair, #D-cycles):", sorted((v[1], v[2]) for v in results.values()))
    if len(sys.argv) > 3:
        import json
        out = {"format": "rotation: ccw neighbour lists (0-based) as in bar.c -T; roots = vertices of t0",
               "line": lines[idx].strip(), "V": len(T), "roots": sorted(roots),
               "edges": sorted(map(list, T.edges())),
               "black_faces_A": [list(I.faces[t]) for t in I.A],
               "two_factors": [{"u": list(u), "extreme_no_plus_cycle": u in no_plus,
                                "extreme_no_minus_cycle": u in no_minus,
                                "carries_tree_pair": results[u][1], "d_cycles": results[u][2],
                                "ordered_pairs": [[list(r), list(s), I.is_tree(s)] for r, s in fac[u]]}
                               for u in fac],
               "tree_matchings": [list(s) for s in tm]}
        json.dump(out, open(sys.argv[3], "w"), indent=1)
        print("wrote", sys.argv[3])

main()
