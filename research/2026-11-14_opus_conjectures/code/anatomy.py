"""Anatomy of a 2-factor: directed cycles of the alpha-orientation O_u and the tree-pair test.

Lemma (PROOFS.md, Lemma 2): (r, s) in the 2-factor u is a tree pair iff no directed cycle of O_u
leaves every centre t it passes towards r(t).  For each directed cycle Z of O_u and each D-cycle
C it meets, record whether Z exits the faces of C all 'forward' (towards the head of C in a
fixed reference orientation), all 'backward', or mixed.  Z forbids exactly the orientations
that agree with its exit pattern on every D-cycle it meets (and is harmless if mixed somewhere).

Also cross-checks the lemma against the direct forest test for every orientation.
Usage: python anatomy.py json_file   (output of verify_c2.py)
"""
import sys, json, itertools
import networkx as nx


def main():
    d = json.load(open(sys.argv[1]))
    A = [tuple(f) for f in d['black_faces_A']]
    roots = set(d['roots'])
    for fac in d['two_factors']:
        u = fac['u']
        um = dict(zip(A, u))
        # D cycles with a reference orientation
        adj = {}
        for t in A:
            a, b = [v for v in t if v != um[t]]
            adj.setdefault(a, []).append((b, t)); adj.setdefault(b, []).append((a, t))
        seen = set(); dcyc = []; head = {}; cyc_of = {}
        for x0 in sorted(adj):
            if x0 in seen:
                continue
            x = x0; prev = None; ci = len(dcyc); cyc = []
            while True:
                seen.add(x)
                y, t = [e for e in adj[x] if e[1] != prev][0] if prev else adj[x][0]
                head[t] = y; cyc_of[t] = ci; cyc.append(t); prev = t; x = y
                if x == x0:
                    break
            dcyc.append(cyc)
        O = nx.DiGraph()
        for t in A:
            for v in t:
                if v == um[t]:
                    O.add_edge(('v', v), ('t', t))
                else:
                    O.add_edge(('t', t), ('v', v))
        patterns = []
        for Z in nx.simple_cycles(O):
            pat = {}
            for a, b in zip(Z, Z[1:] + Z[:1]):
                if a[0] == 't':
                    t = a[1]; fw = b[1] == head[t]
                    ci = cyc_of[t]
                    pat.setdefault(ci, set()).add(fw)
            patterns.append((len(Z) // 2, pat))
        dangerous = [(L, {c: next(iter(v)) for c, v in p.items()}) for L, p in patterns if all(len(v) == 1 for v in p.values())]
        # orientation o[c] = True means reference orientation (r = tail, s = head): Z survives iff all exits are backward (towards r)
        res = []
        for o in itertools.product((True, False), repeat=len(dcyc)):
            killed_by = [L for L, p in dangerous if all((not fw) == o[c] for c, fw in p.items())]
            # direct test
            Q = nx.Graph(); Q.add_nodes_from(range(d['V']))
            for t in A:
                a, b = [v for v in t if v != um[t]]
                s_t = b if head[t] == b else a
                if not o[cyc_of[t]]:
                    s_t = a if s_t == b else b
                e = [v for v in t if v != s_t]
                Q.add_edge(*e)
            direct = Q.number_of_edges() == len(A) and nx.is_forest(Q)
            assert direct == (not killed_by), "lemma check failed"
            res.append((o, killed_by))
        tag = ('E_lo/E_hi extreme' if fac['extreme_no_plus_cycle'] or fac['extreme_no_minus_cycle'] else 'middle')
        print(f"2-factor ({tag}): D-cycles {len(dcyc)} lengths {[len(c) for c in dcyc]}; directed cycles of O_u: {len(patterns)}, "
              f"dangerous (uniform exits): {len(dangerous)}; tree pairs {sum(1 for o, k in res if not k)} of {len(res)}")
        for o, k in res:
            if k:
                print("   orientation", ''.join('+' if b else '-' for b in o), "killed by directed cycles of half-lengths", sorted(k)[:6])
    print("lemma cross-check passed on every orientation")


main()
