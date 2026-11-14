#!/usr/bin/env python3
"""Write labyrinth/frontier.json and labyrinth/scatter.json from the agents' count data.

Size       : v = |V(T)|, the number of vertices of the dual Eulerian triangulation
             (the Barnette graph G has 2v - 4 vertices, and n = |A| = |X| = v - 3).
Invariant  : tau = the number of tree matchings of a rooted triangulation (T, t0).
             tau > 0 exactly when the state method produces a Hamiltonian cycle directly
             at that root (trees paper, Theorem 1.2).

Claim tested by this script (the cross-check): for v <= 14 the two independent
enumerations in the repository give the same multiset of (states, pairs, tree matchings)
over all rooted triangulations. They are
  A  research/2026-11-14_fable_route-combinatorics/data/rows_v16.json
     (own generator from the octahedron, own state code, v <= 16), and
  B  research/2026-11-14_sol_route-algebra/counts.json
     (plantri 4.5 triangulations, workings/barnette_lab state code; it reached v <= 16 when this was run).

Classification of the admissible values 0 .. floor(3^(n/2)) at each size:
  realized         a rooted triangulation with that many tree matchings is in the data
  impossible       odd values (the two signs of tree matchings are equally frequent:
                   trees paper Theorem 5.2), and, at every size where A and B agree, every
                   value that they do not realise
  gap-conditional  a size where B is missing: values not realised in enumeration A
                   (hypothesis: A is complete and correct). Not used once B reached 16.
  unknown          everything else (v >= 17: only parity, obstructed roots and one family are known;
                   odd values are listed up to 401 only)

Command:  python -X utf8 -B labyrinth/make_frontier.py
Output :  labyrinth/frontier.json, labyrinth/scatter.json, labyrinth/frontier_crosscheck.json
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labyrinth"
A_PATH = ROOT / "research/2026-11-14_fable_route-combinatorics/data/rows_v16.json"
B_PATH = ROOT / "research/2026-11-14_sol_route-algebra/counts.json"
RARITY = ROOT / "research/2026-11-14_astra_limits/data/rarity.json"

rows = json.loads(A_PATH.read_text(encoding="utf-8"))
B = json.loads(B_PATH.read_text(encoding="utf-8"))

# ---- enumeration A, per size
A_multi = defaultdict(Counter)      # v -> Counter of (states, pairs, trees)
witness = defaultdict(dict)         # v -> trees -> first witness
cmin_pts = {}                       # (cmin, trees) -> (count, witness)
for r in rows:
    v = r["V"]
    A_multi[v][(r["states"], r["pairs"], r["trees"])] += 1
    witness[v].setdefault(r["trees"], f"(V, class, t0) = ({v}, {r['cls']}, {r['t0']})")
    if r["pairs"] > 0:
        key = (r["cmin"], r["trees"])
        c, w = cmin_pts.get(key, (0, f"({v}, {r['cls']}, {r['t0']})"))
        cmin_pts[key] = (c + 1, w)

# ---- enumeration B, per size (plantri graphs only, all facial roots)
B_multi = defaultdict(Counter)
for g in B["graphs"]:
    if not g["name"].startswith("plantri_"):
        continue
    for rt in g["roots"]:
        B_multi[g["vertices"]][(rt["states"], rt["pairs"], rt["trees"])] += 1

cross = {}
for v in sorted(set(A_multi) | set(B_multi)):
    a, b = A_multi.get(v, Counter()), B_multi.get(v, Counter())
    if not b:
        cross[v] = {"A_rooted": sum(a.values()), "B_rooted": 0, "agree": None}
        continue
    cross[v] = {
        "A_rooted": sum(a.values()), "B_rooted": sum(b.values()),
        "agree": a == b,
        "tree_sets_agree": {k[2] for k in a} == {k[2] for k in b},
        "only_in_A": sorted(map(list, set(a) - set(b))), "only_in_B": sorted(map(list, set(b) - set(a))),
    }
(LAB / "frontier_crosscheck.json").write_text(json.dumps(cross, indent=1))

# ---- frontier
sizes = []
for v in sorted(A_multi):
    n = v - 3
    hi = int(3 ** (n / 2))
    realized = sorted(witness[v])
    row = {"size": v, "label": f"|V(T)| = {v}", "lo": 0, "hi": hi, "step": 1,
           "realized": [[t, witness[v][t]] for t in realized],
           "bounds": {"upper": hi, "upper_kind": "3^(n/2) (trees paper, Lemma 6.1 with Hadamard)",
                      "max_seen": max(realized)},
           "intervals": []}
    validated = cross[v]["agree"] is True
    status = "impossible" if validated else "gap-conditional"
    why = ("not realised; enumerations A and B agree at this size" if validated else
           "not realised in enumeration A (no independent replay at this size)")
    # complement of the realised values, as maximal runs (a realised value is never also claimed impossible)
    rs = set(realized)
    t = 0
    while t <= hi:
        if t in rs:
            t += 1
            continue
        u = t
        while u + 1 <= hi and (u + 1) not in rs:
            u += 1
        if validated:
            row["intervals"].append({"v0": t, "v1": u, "status": "impossible", "why": why + " (odd values are also excluded by the sign balance, trees paper Thm 5.2)"})
        else:
            row["intervals"].append({"v0": t, "v1": u, "status": status, "why": why})
            for o in range(t + (1 - t % 2), u + 1, 2):
                row["intervals"].append({"v0": o, "v1": o, "status": "impossible",
                                         "why": "odd: the signs of tree matchings are balanced (trees paper Thm 5.2)"})
        t = u + 1
    row["note"] = f"{sum(A_multi[v].values())} rooted triangulations in A" + (
        f", {cross[v]['B_rooted']} in B, multisets agree" if validated else ", B does not reach this size")
    sizes.append(row)

# sizes beyond the enumeration: parity, obstructed roots and the rarity family only
rar = json.loads(RARITY.read_text(encoding="utf-8")) if RARITY.exists() else None
for v in (17, 18, 23, 28, 33):
    n = v - 3
    hi = int(3 ** (n / 2))
    row = {"size": v, "label": f"|V(T)| = {v}", "lo": 0, "hi": hi, "step": 1, "realized": [], "intervals": [],
           "bounds": {"upper": hi, "upper_kind": "3^(n/2)"}, "note": "beyond every enumeration in the repository"}
    row["realized"].append([0, "glue an octahedron into a face so that t0 is on the white side "
                               "of the separating triangle (trees paper Thm 1.2)"])
    if (v - 3) % 5 == 0:
        q = (v - 3) // 5
        row["realized"].append([2 ** q, f"q = {q} hexagonal-prism duals glued into white faces: "
                                        f"3^{q} states, 2^{q} tree matchings (astra_limits, rarity family)"])
    # odd values impossible: one interval per odd value is too many here, so use bins of width 1 up to a cap
    cap = min(hi, 401)
    for t in range(1, cap + 1, 2):
        row["intervals"].append({"v0": t, "v1": t, "status": "impossible",
                                 "why": "odd: balanced signs (trees paper Thm 5.2)"})
    sizes.append(row)

frontier = {
    "meta": {"size_name": "|V(T)|", "value_name": "tree matchings of (T, t0)", "value_scale": "log"},
    "sizes": sizes,
}
(LAB / "frontier.json").write_text(json.dumps(frontier))

# ---- scatter: tree matchings against cmin
pts = []
for (c, t), (count, w) in sorted(cmin_pts.items()):
    series = "eq" if t == 2 ** c else ("gt" if t > 2 ** c else "lt")
    pts.append({"x": c, "y": t, "series": series, "src": f"{count} rooted triangulations, first {w}"})
for c in range(1, 6):
    pts.append({"x": c, "y": 2 ** c, "series": "bound", "src": "conjectured lower bound 2^cmin"})
    pts.append({"x": c, "y": 2 * c, "series": "proved", "src": "proved lower bound 2 cmin (route-combinatorics, unreviewed)"})
scatter = {
    "title": "Tree matchings against the minimum number of D-cycles",
    "tab": "tau vs cmin",
    "subtitle": "All 5088 rooted Eulerian triangulations with a pair, |V(T)| <= 16 (enumeration A). "
                "Conjecture k.tm-2cmin says no point lies below 2^cmin.",
    "x_name": "cmin (fewest cycles of D over all pairs)", "y_name": "tree matchings", "y_scale": "log",
    "series": [{"key": "eq", "label": "tau = 2^cmin"}, {"key": "gt", "label": "tau > 2^cmin"},
               {"key": "lt", "label": "tau < 2^cmin (would refute the conjecture)"},
               {"key": "bound", "label": "2^cmin"}, {"key": "proved", "label": "2 cmin (proved here, unreviewed)"}],
    "points": pts,
}
(LAB / "scatter.json").write_text(json.dumps(scatter))

print("cross-check A vs B:")
for v, c in cross.items():
    print(f"  v={v:2d}  A={c['A_rooted']:5d}  B={c['B_rooted']:5d}  agree={c['agree']}"
          + ("" if c["agree"] in (True, None) else f"  only_in_A={c['only_in_A'][:4]} only_in_B={c['only_in_B'][:4]}"))
print("sizes:", [s["size"] for s in sizes])
print("scatter points:", len(pts), " below-bound points:", sum(1 for p in pts if p["series"] == "lt"))
