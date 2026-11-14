"""Recompute the numeric claims that several project documents state about the
running example (paper/figures/running.json, t0 = face 4, e0 = 04) and the
hexagonal prism (dual: double wheel, apexes 6, 7, rim 0..5, t0 = (6,0,1)).

For a rooted Eulerian triangulation it reports: states, ordered pairs, states
with a partner, tree matchings (Q_s a forest with one root per component),
cancelling states (partner and a cycle in Q_s), covers D with their circuit
counts, m = c_min, the lowest-coefficient magnitude sum_{D: c(D)=m} prod |W cap S_C|
(white triangles inside each circuit, Lemma 8 / (6.4) of the primal note),
Hamiltonian cycles of G, and those avoiding the edge of G dual to e0.

Usage: python -I scripts/recount.py   (from this research folder)
"""
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from phase_ratio import states, two_colour, delta  # noqa: E402


def rooted_counts(faces, t0, e0):
    col = two_colour(faces)
    black = [i for i in range(len(faces)) if col[i] == col[t0]]
    A = [i for i in black if i != t0]
    R = set(faces[t0])
    X = set(v for f in faces for v in f) - R
    n = len(A)
    tris = [faces[i] for i in A]
    S = states(tris, X)
    pairs = [(r, s) for s in S for r in S if all(r[i] != s[i] for i in range(n))]
    partnered = {s for r, s in pairs}

    def q_edges(s):
        out = []
        for i, t in enumerate(tris):
            a, b = [v for v in t if v != s[i]]
            out.append((a, b))
        return out

    def components(vertices, edges):
        parent = {v: v for v in vertices}

        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        cyc = False
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                cyc = True
            else:
                parent[ra] = rb
        comps = {}
        for v in vertices:
            comps.setdefault(find(v), set()).add(v)
        return cyc, list(comps.values())

    allv = X | R
    tree_matchings = 0
    forest_states = 0
    cancelling = 0
    for s in S:
        cyc, comps = components(allv, q_edges(s))
        if not cyc:
            forest_states += 1
            if all(len(c & R) == 1 for c in comps):
                tree_matchings += 1
        if cyc and s in partnered:
            cancelling += 1

    # triangle adjacency for interiors
    edge_tris = {}
    for i, f in enumerate(faces):
        for k in range(3):
            edge_tris.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(i)

    def white_inside(cycle_vertices):
        cyc_edges = {frozenset((cycle_vertices[j], cycle_vertices[(j + 1) % len(cycle_vertices)]))
                     for j in range(len(cycle_vertices))}
        seen = {t0}
        stack = [t0]
        while stack:
            i = stack.pop()
            f = faces[i]
            for k in range(3):
                e = frozenset((f[k], f[(k + 1) % 3]))
                if e in cyc_edges:
                    continue
                for j in edge_tris[e]:
                    if j not in seen:
                        seen.add(j)
                        stack.append(j)
        return sum(1 for j in range(len(faces)) if j not in seen and col[j] != col[t0])

    covers = {}
    for r, s in pairs:
        rinv = {r[i]: i for i in range(n)}
        seen = set()
        cyc_list = []
        for f0 in sorted(X):
            if f0 in seen:
                continue
            f = f0
            cyc = []
            while f not in seen:
                seen.add(f)
                cyc.append(f)
                f = s[rinv[f]]
            cyc_list.append(tuple(cyc))
        key = frozenset(frozenset(frozenset((c[j], c[(j + 1) % len(c)])) for j in range(len(c))) for c in cyc_list)
        covers.setdefault(key, cyc_list)
    cover_sizes = sorted(len(v) for v in covers.values())
    m = min(cover_sizes) if cover_sizes else None
    low = 0
    for cl in covers.values():
        if len(cl) == m:
            prod = 1
            for c in cl:
                prod *= white_inside(list(c))
            low += prod
    return {
        "n": n, "states": len(S), "ordered_pairs": len(pairs),
        "states_with_partner": len(partnered), "forest_states": forest_states,
        "tree_matchings": tree_matchings, "cancelling_states": cancelling,
        "covers": len(covers), "cover_circuit_counts": cover_sizes, "m": m,
        "lowest_coefficient_abs": low,
    }


def primal_graph(faces):
    """Vertices = triangles; edges = shared triangle sides (labelled by the side)."""
    edge_tris = {}
    for i, f in enumerate(faces):
        for k in range(3):
            edge_tris.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(i)
    return {e: tuple(v) for e, v in edge_tris.items()}


def hamiltonian_cycles(faces):
    edges = primal_graph(faces)
    N = len(faces)
    adj = {i: [] for i in range(N)}
    for e, (a, b) in edges.items():
        adj[a].append((b, e))
        adj[b].append((a, e))
    cycles = set()
    path = [0]
    used = {0}
    eused = []

    def rec():
        v = path[-1]
        for w, e in adj[v]:
            if w == 0 and len(path) == N:
                cycles.add(frozenset(eused + [e]))
            elif w not in used:
                used.add(w)
                path.append(w)
                eused.append(e)
                rec()
                eused.pop()
                path.pop()
                used.discard(w)

    rec()
    return cycles


def main():
    out = {}
    run = json.load(open(Path(__file__).parents[3] / "paper/figures/running.json"))
    faces = run["faces"]
    t0 = run["t0"]
    e0 = frozenset(run["e0"])
    res = rooted_counts(faces, t0, e0)
    H = hamiltonian_cycles(faces)
    res["hamiltonian_cycles"] = len(H)
    res["avoiding_dual_of_e0"] = sum(1 for c in H if e0 not in c)
    out["running t0=%d e0=%s" % (t0, sorted(e0))] = res

    rim = list(range(6))
    prism = [[6, i, (i + 1) % 6] for i in rim] + [[7, (i + 1) % 6, i] for i in rim]
    t0 = 0  # (6,0,1)
    base = rooted_counts(prism, t0, None)
    H = hamiltonian_cycles(prism)
    base["hamiltonian_cycles"] = len(H)
    for side in ([0, 1], [6, 0], [6, 1]):
        base["avoiding_dual_of_e0=%s%s" % tuple(side)] = sum(1 for c in H if frozenset(side) not in c)
    out["prism t0=(6,0,1)"] = base
    # the other colour class as black: root (7,1,0)
    other = rooted_counts(prism, 6, None)
    for side in ([7, 1], [1, 0], [7, 0]):
        other["avoiding_dual_of_e0=%s%s" % tuple(side)] = sum(1 for c in H if frozenset(side) not in c)
    out["prism t0=(7,1,0), other colour class"] = other
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
