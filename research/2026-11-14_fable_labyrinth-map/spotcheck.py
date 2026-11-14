#!/usr/bin/env python3
"""Spot check of the numbers that HOW-IT-WORKS.md and the route map lean on.

Written from the definitions in research/BRIEF.md. It imports nothing from any other agent.

Claims tested, on the even bipyramids with rim m = 4 (octahedron, dual of the cube),
m = 6 (dual of the hexagonal prism) and m = 8, rooted at the black face (N, 0, 1):
  1. |A| = |X| = n.
  2. number of states, pairs, tree matchings (state s with H - s a spanning tree).
  3. a state is a tree matching iff it has exactly one partner; partner counts are 0 or 2^k.
  4. for a pair, Q_s forest  <=>  tree matching; for a single state this can fail (prism).
  5. the real sign prod delta(r(t), s(t)) flips under reversal of any D-cycle, all D-cycles are odd,
     and the unweighted signed sum over pairs is 0, so tree matchings have balanced signs.
  6. every D-cycle has delta-sum +3 or -3 (disk identity, in the form used for the sign).
  7. (rim 4, 6, 8) every Hamiltonian cycle of G avoiding e0* gives a state by the backward reading of
     HOW-IT-WORKS Section 2, and each such state is a tree matching or has no partner.
     Expected for the prism: 4 avoiding cycles, 2 tree matchings, 2 without partner.
     Found in addition (not predicted): the map from cycles to states is not injective. On the prism,
     for the middle edge of t0, the two cycles without partner give the same state. A state fixes the
     tail of the selected edge in each black face, not the edge, unless H - s is a tree.
Expected from the agents' reports: octahedron 2 states, 2 pairs, 2 tree matchings;
prism dual 3 states, 2 pairs, 2 tree matchings, all three Q_s acyclic.

Command:  python -B research/2026-11-14_fable_labyrinth-map/spotcheck.py
Output :  research/2026-11-14_fable_labyrinth-map/spotcheck.json
"""
import itertools
import json
from pathlib import Path


def bipyramid(m):
    """Counterclockwise faces (seen from outside) of the bipyramid over an m-cycle, m even. Black faces first."""
    N, S = "N", "S"
    black, white = [], []
    for i in range(m):
        j = (i + 1) % m
        (black if i % 2 == 0 else white).append((N, i, j))
        (white if i % 2 == 0 else black).append((S, j, i))
    return black, white


def acyclic(n_vertices, edges):
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True


def components(vertices, edges):
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        parent[find(a)] = find(b)
    comp = {}
    for v in vertices:
        comp.setdefault(find(v), []).append(v)
    return list(comp.values())


def analyse(m):
    black, white = bipyramid(m)
    t0 = black[0]
    roots = set(t0)
    A = black[1:]
    V = {v for f in black + white for v in f}
    X = sorted(V - roots, key=str)
    n = len(A)
    assert n == len(X), "count |A| = |X|"
    # every edge lies in exactly one black face
    owner = {}
    for f in black:
        for k in range(3):
            e = frozenset((f[k], f[(k + 1) % 3]))
            assert e not in owner
            owner[e] = f

    def delta(t, u, v):
        """+1 if u -> v is counterclockwise around the black face t."""
        k = t.index(u)
        return 1 if t[(k + 1) % 3] == v else -1

    choices = [[v for v in t if v not in roots] for t in A]
    states = [s for s in itertools.product(*choices) if len(set(s)) == n]

    def Q(s):
        return [tuple(v for v in t if v != s[i]) for i, t in enumerate(A)]

    def is_tree_matching(s):
        # H - s: spokes (t, v) for all black t and corners v, minus (t, s(t)). Spanning tree iff connected and acyclic.
        spokes = [(("c", t), v) for t in black for v in t]
        removed = {(("c", t), s[i]) for i, t in enumerate(A)}
        kept = [e for e in spokes if e not in removed]
        verts = [("c", t) for t in black] + sorted(V, key=str)
        return len(kept) == len(verts) - 1 and acyclic(len(verts), kept)

    pairs = [(r, s) for r in states for s in states if all(a != b for a, b in zip(r, s))]
    partners = {s: [r for r in states if all(a != b for a, b in zip(r, s))] for s in states}
    tm = [s for s in states if is_tree_matching(s)]

    def sign(r, s):
        out = 1
        for i, t in enumerate(A):
            out *= delta(t, r[i], s[i])
        return out

    def d_cycles(r, s):
        nxt = {r[i]: (s[i], i) for i in range(n)}
        seen, cycles = set(), []
        for v in X:
            if v in seen:
                continue
            cyc, w = [], v
            while w not in seen:
                seen.add(w)
                w2, i = nxt[w]
                cyc.append(i)
                w = w2
            cycles.append(cyc)
        return cycles

    checks = {"tm_iff_one_partner": True, "partners_power_of_two": True, "pair_forest_iff_tm": True,
              "d_cycles_odd": True, "delta_sum_pm3": True, "d_reversal_flips_sign": True}
    for s in states:
        k = len(partners[s])
        checks["tm_iff_one_partner"] &= ((s in tm) == (k == 1))
        checks["partners_power_of_two"] &= (k == 0 or (k & (k - 1)) == 0)
        if k:
            checks["pair_forest_iff_tm"] &= (acyclic(len(V), Q(s)) == (s in tm))
    for r, s in pairs:
        for cyc in d_cycles(r, s):
            checks["d_cycles_odd"] &= (len(cyc) % 2 == 1)
            checks["delta_sum_pm3"] &= (abs(sum(delta(A[i], r[i], s[i]) for i in cyc)) == 3)
            r2, s2 = list(r), list(s)
            for i in cyc:
                r2[i], s2[i] = s[i], r[i]
            assert (tuple(r2), tuple(s2)) in set(pairs)
            checks["d_reversal_flips_sign"] &= (sign(tuple(r2), tuple(s2)) == -sign(r, s))
    forest_states_not_tm = [s for s in states if acyclic(len(V), Q(s)) and s not in tm]
    bad_components = None
    if forest_states_not_tm:
        s = forest_states_not_tm[0]
        bad_components = [sorted(map(str, c)) for c in components(sorted(V, key=str), Q(s))]
    tm_signs = [sign(partners[s][0], s) for s in tm]
    return {
        "rim": m, "vertices_of_T": len(V), "n": n, "states": len(states), "pairs": len(pairs), "tree_matchings": len(tm),
        "partner_counts": sorted(len(partners[s]) for s in states),
        "signed_sum_over_pairs": sum(sign(r, s) for r, s in pairs),
        "tree_matching_signs": sorted(tm_signs),
        "states_with_Q_forest": sum(1 for s in states if acyclic(len(V), Q(s))),
        "forest_states_that_are_not_tree_matchings": len(forest_states_not_tm),
        "components_of_Q_for_one_such_state": bad_components,
        "checks": checks,
    }


def cycles_to_states(m):
    """Section 2 of HOW-IT-WORKS, run on the bipyramid of rim m. For every Hamiltonian cycle of G = T* avoiding e0*:
    P = edges of T not crossed; P - e0 must be three trees, one per root; orienting them to the roots must give a state;
    that state must be a tree matching or have no partner (route-combinatorics Proposition 7)."""
    black, white = bipyramid(m)
    faces = black + white
    t0 = black[0]
    roots = set(t0)
    A = black[1:]
    V = sorted({v for f in faces for v in f}, key=str)
    X = [v for v in V if v not in roots]
    edge_faces = {}
    for f in faces:
        for k in range(3):
            edge_faces.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(f)
    adj = {f: [] for f in faces}                      # the cubic graph G on the faces of T
    for e, (f, g) in edge_faces.items():
        adj[f].append((g, e))
        adj[g].append((f, e))
    choices = [[v for v in t if v not in roots] for t in A]
    states = [st for st in itertools.product(*choices) if len(set(st)) == len(A)]

    def n_partners(st):
        return sum(1 for r in states if all(x != y for x, y in zip(r, st)))

    def tree_matching(st):
        spokes = [(("c", t), v) for t in black for v in t]
        removed = {(("c", t), st[i]) for i, t in enumerate(A)}
        kept = [e for e in spokes if e not in removed]
        return len(kept) == len(black) + len(V) - 1 and acyclic(0, kept)

    ham = set()
    start = faces[0]

    def dfs(path, used_edges, seen):
        f = path[-1]
        for g, e in adj[f]:
            if g == start and len(path) == len(faces):
                ham.add(frozenset(used_edges | {e}))
            elif g not in seen:
                dfs(path + [g], used_edges | {e}, seen | {g})
    dfs([start], frozenset(), {start})
    rows = []
    for e0 in [frozenset((t0[k], t0[(k + 1) % 3])) for k in range(3)]:
        tally = {"avoiding_cycles": 0, "give_a_state": 0, "tree_matchings": 0, "no_partner": 0, "other": 0, "distinct_states": set()}
        for crossed in ham:
            if e0 in crossed:
                continue
            tally["avoiding_cycles"] += 1
            P = [e for e in edge_faces if e not in crossed]
            assert all(sum(1 for k in range(3) if frozenset((f[k], f[(k + 1) % 3])) in P) == 1 for f in faces)
            rest = [tuple(e) for e in P if e != e0]
            assert acyclic(0, rest)
            comps = components(V, rest)
            assert len(comps) == 3 and all(len(roots & set(c)) == 1 for c in comps)
            # orient towards the roots: breadth-first from each root
            nbr = {v: [] for v in V}
            for x, y in rest:
                nbr[x].append(y)
                nbr[y].append(x)
            parent, stack = {}, list(roots)
            seen = set(roots)
            while stack:
                x = stack.pop()
                for y in nbr[x]:
                    if y not in seen:
                        seen.add(y)
                        parent[y] = x
                        stack.append(y)
            st = []
            for t in A:
                sel = [e for e in (frozenset((t[k], t[(k + 1) % 3])) for k in range(3)) if e in P]
                assert len(sel) == 1
                x, y = tuple(sel[0])
                st.append(x if parent.get(x) == y else y)
                assert parent.get(st[-1]) in (x, y)
            st = tuple(st)
            assert st in states
            tally["give_a_state"] += 1
            tally["distinct_states"].add(st)
            k = n_partners(st)
            if tree_matching(st):
                tally["tree_matchings"] += 1
            elif k == 0:
                tally["no_partner"] += 1
            else:
                tally["other"] += 1
        tally["distinct_states"] = len(tally["distinct_states"])
        rows.append(tally)
    return {"rim": m, "hamiltonian_cycles_of_G": len(ham), "per_edge_of_t0": rows}


if __name__ == "__main__":
    hc = [cycles_to_states(m) for m in (4, 6, 8)]
    for h in hc:
        print(h)
        for row in h["per_edge_of_t0"]:
            assert row["give_a_state"] == row["avoiding_cycles"] and row["other"] == 0
            # the cycles that are tree matchings have distinct states; unpartnered states can repeat
            assert row["distinct_states"] >= row["tree_matchings"] + (1 if row["no_partner"] else 0)
    out = [analyse(m) for m in (4, 6, 8, 10)]
    out.append({"cycles_to_states": hc})
    Path(__file__).with_name("spotcheck.json").write_text(json.dumps(out, indent=1))
    for o in out[:4]:
        print({k: v for k, v in o.items() if k not in ("checks", "components_of_Q_for_one_such_state")})
        print("   checks:", o["checks"])
        if o["components_of_Q_for_one_such_state"]:
            print("   a forest state that is not a tree matching has Q-components", o["components_of_Q_for_one_such_state"])
    assert out[0]["states"] == 2 and out[0]["pairs"] == 2 and out[0]["tree_matchings"] == 2
    assert out[1]["states"] == 3 and out[1]["pairs"] == 2 and out[1]["tree_matchings"] == 2
    assert out[1]["states_with_Q_forest"] == 3
    assert all(all(o["checks"].values()) for o in out[:4])
    assert all(o["signed_sum_over_pairs"] == 0 and sum(o["tree_matching_signs"]) == 0 for o in out[:4])
    print("all expected values confirmed")
