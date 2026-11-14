"""Render the file-level graph and the key-theorem skeleton of the Lean proof.

Usage (from the repository root):
    python -I research/2026-11-14_opus_lean-formalisation/scripts/render_graphs.py \
        research/2026-11-14_opus_lean-formalisation/graph

Reads graph/lean-decls.json and graph/lean-to-paper.json. Writes
graph/skeleton.dot, graph/skeleton.json, graph/skeleton.png, graph/files.png.

Skeleton edges: X -> Y between key declarations when Y is reachable from X in the
declaration graph through non-key declarations only, using unambiguous edges only
except edges produced only by tokens whose last component is a common Mathlib name
(list MATHLIB_LIKE below).  A transitive reduction is then
applied so that the picture shows the direct logical steps.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

sys.stdout.reconfigure(encoding="utf-8")

# key declaration -> (short label, paper counterpart, layer for drawing)
KEY = {
    "main": ("main", "Thm 1.1", 0),
    "PlaneEmbedding.exists_exact_dual": ("exists_exact_dual", "none (sphere dual)", 1),
    "PlaneEmbedding.exists_lattice_minor_model": ("lattice minor model", "none", 2),
    "PlaneEmbedding.exists_lattice_corridor_model": ("corridor model", "none", 3),
    "RectangularDual.lattice_minor_in_rectangle": ("minor in rectangle", "none", 2),
    "RectangularDual.grid_duality": ("grid duality", "none", 2),
    "Network.Duality.graphMinor": ("duality of a minor", "none", 2),
    "Network.Duality.minor": ("Duality.minor", "none (Whitney)", 3),
    "Network.Duality.hamiltonian": ("Duality.hamiltonian", "Thm 1.1 last para", 1),
    "Network.cut_card_three": ("cuts >= 3", "Thm 1.1 proof", 1),
    "cubic_bipartite_order": ("|V| >= 6", "Thm 1.1 proof", 1),
    "Network.Duality.connected_complement_matching": ("H- form", "Thm 2.2 / Cor 7.1", 2),
    "SimpleCycle.cycle_at_of_connected_two": ("2-factor connected => cycle", "Thm 1.1 last para", 2),
    "Network.matching_strong": ("induction on |V|", "Thm 2.2 (Sec 7)", 3),
    "Network.cap_duality": ("cap has a dual", "Sec 7 capping", 4),
    "Network.cap_coloring": ("cap colouring", "Sec 7 cap colour", 4),
    "Network.cap_glue_connected": ("glue: connected", "Sec 7 gluing", 4),
    "Network.cap_glue_matching": ("glue: matching", "Sec 7 gluing", 4),
    "Network.cap_simple": ("cap simple", "Sec 7", 4),
    "Network.make_coloredDual": ("colored dual", "Thm 1.1: T simple Eulerian triang.", 4),
    "Network.Duality.simple_dual_edge": ("T simple", "Thm 1.1 proof", 5),
    "Network.Duality.cubic_face_triangles_edge": ("faces are triangles", "Thm 1.1 proof", 5),
    "Network.oriented_face": ("orient black triangles", "delta convention", 5),
    "Network.irreducible_matching": ("no sep. triangle case", "Thm 2.2, Secs 3-6", 4),
    "Network.ColoredDual.pair_nonempty": ("a pair exists", "Prop 3.1", 5),
    "BMatching.two_matchings": ("two disjoint matchings", "Prop 3.1 flow", 6),
    "Network.capacity_full": ("capacity (3.1)", "(3.1)", 6),
    "Network.induced_density": ("density (3.2)", "(3.2)-(3.4)", 7),
    "Network.induced_euler_bound": ("Euler for T[U]", "(3.4)", 8),
    "Network.region_density": ("region bound", "(3.3)", 8),
    "Network.ColoredDual.forest_pair": ("forest pair", "Prop 5.1", 5),
    "TriangleSystem.Pair.forest_pair_of_disk_circulation": ("abstract Prop 5.1", "Prop 5.1", 6),
    "TriangleSystem.OppositeCycle.fixed_second_state_cancels": ("fixed-s cancellation", "Lemma 5.2", 7),
    "TriangleSystem.OppositeCycle.reverse_phase": ("reversal flips phase", "Lemma 5.2", 8),
    "TriangleSystem.Pair.total_sum_ne_zero": ("sum nonzero", "Sec 5.3", 7),
    "TriangleSystem.Pair.group_sum_product": ("group = product", "(5.4)", 8),
    "TriangleSystem.Pair.groupEquiv": ("group = orientations", "Sec 5.3 regrouping", 9),
    "common_phase_sum_ne_zero": ("lowest coefficient", "(5.5)", 8),
    "Network.ColoredDual.opposite_disk": ("Q_s-cycle: delta = +-3", "Lemma 4.1 in 5.2", 6),
    "Network.ColoredDual.paired_sign": ("D-cycle: sign coupling", "(5.3) + Lemma 4.1", 6),
    "Network.ColoredDual.StateCycle.signed": ("delta and slope signs", "(5.3)", 7),
    "Network.boundary_of_sum_zero": ("white-charge flow", "Lemma 5.3 (replaced)", 7),
    "Network.white_positive_of_boundary": ("a white face inside", "Lemma 5.3 (replaced)", 8),
    "Network.ColoredDual.cycle_disk": ("disk of a state cycle", "Lemma 4.1", 8),
    "Network.state_disk_delta": ("disk identity", "Lemma 4.1", 9),
    "Network.state_disk_count": ("B = I + l", "(4.2)", 10),
    "Network.disk_boundary_imbalance": ("h = 2l + 3", "(4.1)+(4.2)", 10),
    "Network.region_euler": ("disk Euler", "(4.1)", 11),
    "Network.Duality.circuit_cut": ("cycle = bond", "none (Jordan)", 11),
    "Network.Bond.connected_shore": ("bond shores connected", "none (Jordan)", 11),
    "Network.mixed_corner_on_boundary": ("no pinch vertex", "none (disk)", 11),
    "Network.ColoredDual.recover_connected_complement": ("recovery", "Sec 6", 5),
    "Network.ColoredDual.recovery_matching": ("one edge per face", "Sec 6.1", 6),
    "Network.tree_matching": ("tree -> matching", "Sec 6.1 rooting", 7),
    "Network.ColoredDual.remainder_independent": ("complement is a tree", "Sec 6.1 + Lemma 2.1", 7),
    "Network.ColoredDual.removed_acyclic": ("Q_s + 2 root sides acyclic", "Lemma 6.1", 7),
    "Network.addSink_acyclic": ("outdegree <= 1 argument", "Lemma 6.1", 8),
    "Network.ColoredDual.selected_forest": ("P is a forest", "Lemma 6.2", 6),
    "Network.matching_cut_balance": ("(6.1) count", "(6.1)", 7),
    "Network.Duality.complement_connected": ("forest^c connected", "Lemma 2.1", 6),
}


def main():
    gdir = Path(sys.argv[1])
    data = json.load(open(gdir / "lean-decls.json", encoding="utf-8"))
    nodes = {n["name"].replace("OAI.Barnette.", ""): n for n in data["nodes"]}
    missing = [k for k in KEY if k not in nodes]
    if missing:
        print("missing keys:", missing)
    # Skeleton edges: all extracted edges except those produced only by tokens whose last
    # component is a common Mathlib/Lean name (Path.symm, Finset.card, ...).
    MATHLIB_LIKE = set("""symm trans ext card compl map mk val property nonempty toEquiv reverse
    support walk start finish isPath step n adjacent loopless left right next flip value range_eq point
    arc trace curve core branch cell cells lower upper extend quotient potential coordinates""".split())
    def spurious(toks):
        return all(t.split(".")[-1] in MATHLIB_LIKE for t in toks)
    G = nx.DiGraph()
    for name, n in nodes.items():
        for u in n["uses"]:
            if u in n["ambiguous_uses"] and spurious(n["tokens"][u]):
                continue
            G.add_edge(name, u.replace("OAI.Barnette.", ""))
    keys = [k for k in KEY if k in nodes]
    S = nx.DiGraph()
    S.add_nodes_from(keys)
    for k in keys:
        # BFS through non-key nodes
        seen, todo = {k}, [k]
        while todo:
            x = todo.pop()
            for y in G.successors(x) if x in G else []:
                if y in seen:
                    continue
                seen.add(y)
                if y in KEY:
                    S.add_edge(k, y)
                else:
                    todo.append(y)
    cyc = list(nx.simple_cycles(S))
    if cyc:
        print("cycles in skeleton:", cyc[:5])
    R = nx.transitive_reduction(S) if not cyc else S
    # also check: are all keys reachable from main?
    unreach = [k for k in keys if k != "main" and not nx.has_path(R, "main", k)]
    print("skeleton:", R.number_of_nodes(), "nodes", R.number_of_edges(), "edges; unreachable from main:", unreach)
    json.dump({"nodes": {k: {"label": KEY[k][0], "paper": KEY[k][1], "file": nodes[k]["module"],
                             "line": nodes[k]["start_line"], "lines": nodes[k]["lines"]} for k in keys},
               "edges": sorted(R.edges())}, open(gdir / "skeleton.json", "w", encoding="utf-8"), indent=1)
    def q(s):
        return '"' + s + '"'
    dot = ["digraph skeleton {", "  rankdir=TB; node [shape=box,fontsize=9,style=rounded];"]
    for k in keys:
        lab, pap, _ = KEY[k]
        dot.append(f"  {q(k)} [label={q(lab + '\\n[' + pap + ']\\n' + nodes[k]['module'] + ':' + str(nodes[k]['start_line']))}];")
    for a, b in sorted(R.edges()):
        dot.append(f"  {q(a)} -> {q(b)};")
    dot.append("}")
    (gdir / "skeleton.dot").write_text("\n".join(dot), encoding="utf-8")

    # draw skeleton: layer = longest path from main
    layer = {}
    for k in nx.topological_sort(R):
        preds = list(R.predecessors(k))
        layer[k] = 0 if not preds else max(layer[p] for p in preds) + 1
    by = {}
    for k, l in layer.items():
        by.setdefault(l, []).append(k)
    pos = {}
    for l, ks in by.items():
        ks.sort(key=lambda k: (nodes[k]["module"], k))
        for i, k in enumerate(ks):
            pos[k] = ((i - (len(ks) - 1) / 2) * 2.3, -l * 1.25)
    colour = {"E": "#9ecae1", "D": "#c6dbef", "3": "#fdd0a2", "4": "#fc9272", "5": "#fcbba1",
              "6": "#c7e9c0", "7": "#dadaeb", "2": "#fee391", "1": "#ffffff"}
    tagmap = {n["name"].replace("OAI.Barnette.", ""): n["paper_section"]
              for n in json.load(open(gdir / "lean-to-paper.json", encoding="utf-8"))["nodes"]}
    w = max(len(v) for v in by.values())
    fig, ax = plt.subplots(figsize=(max(14, 2.4 * w), 1.3 * (max(by) + 1) + 1))
    for a, b in R.edges():
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.annotate("", xy=(x2, y2 + 0.22), xytext=(x1, y1 - 0.22),
                    arrowprops=dict(arrowstyle="-|>", color="#888888", lw=0.6, shrinkA=0, shrinkB=0))
    for k, (x, y) in pos.items():
        lab, pap, _ = KEY[k]
        ax.text(x, y, f"{lab}\n[{pap}]\n{nodes[k]['module']} ({nodes[k]['lines']})", ha="center", va="center",
                fontsize=6.2, bbox=dict(boxstyle="round,pad=0.25", fc=colour.get(tagmap.get(k, "1"), "#fff"),
                                        ec="#555555", lw=0.5))
    ax.set_axis_off()
    ax.set_title("Skeleton of the Lean proof: key declarations, edge = uses (transitively, through non-key lemmas).\n"
                 "Colour = paper section (blue: no counterpart; yellow: Sec 2; orange: Sec 3; red: Sec 4; pink: Sec 5;"
                 " green: Sec 6; violet: Sec 7). Number in brackets after the file = lines of that declaration.",
                 fontsize=8)
    xs = [p[0] for p in pos.values()]
    ax.set_xlim(min(xs) - 1.5, max(xs) + 1.5)
    ax.set_ylim(min(p[1] for p in pos.values()) - 0.8, 0.8)
    fig.tight_layout()
    fig.savefig(gdir / "skeleton.png", dpi=160)

    # file graph
    F = nx.DiGraph()
    fl = data["file_lines"]
    for n in data["nodes"]:
        for u in n["uses"]:
            if u in n["ambiguous_uses"]:
                continue
            a, b = n["module"], nodes[u.replace("OAI.Barnette.", "")]["module"]
            if a != b:
                F.add_edge(a, b, weight=F.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
    FR = nx.transitive_reduction(F)
    groups = [["Model", "Network", "CutSpaces", "FlowCircuits", "Bonds", "Quotients"],
              ["DiskRegions", "StateDisk", "Circulation"],
              ["TriangleSystem", "ColoredDual", "CycleReversal", "PairPhases", "PairPolynomials", "Forest"],
              ["Contraction", "MinorDuality", "BMatching"],
              ["Matching", "ForestMatching"],
              ["ThreeCuts", "CappedDuality", "Gluing"],
              ["Traces", "SquareGrid", "Corridors", "MinorModel", "BranchPartition", "Rectangle", "ExactDual"],
              ["Main"]]
    names = ["duality layer", "Sec 4 disk", "Sec 5 states,\ncancellation", "Sec 3 pair", "Sec 6 recovery",
             "Sec 7 gluing", "embedding -> dual", "Thm 1.1"]
    fpos = {}
    for gi, g in enumerate(groups):
        for i, m in enumerate(g):
            fpos[m] = (gi * 2.2, -i * 1.0)
    fig, ax = plt.subplots(figsize=(17, 7.5))
    for a, b in FR.edges():
        (x1, y1), (x2, y2) = fpos[a], fpos[b]
        wgt = F[a][b]["weight"]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#999999", lw=0.4 + min(2.5, wgt / 8),
                                    connectionstyle="arc3,rad=0.12", shrinkA=14, shrinkB=14))
    for m, (x, y) in fpos.items():
        ax.text(x, y, f"{m}\n{fl[m]} lines", ha="center", va="center", fontsize=7,
                bbox=dict(boxstyle="round,pad=0.3", fc="#f4f4f4", ec="#444444", lw=0.6))
    for gi, nm in enumerate(names):
        ax.text(gi * 2.2, 0.9, nm, ha="center", fontsize=8, weight="bold")
    ax.set_xlim(-1.2, (len(groups) - 1) * 2.2 + 1.2)
    ax.set_ylim(-max(len(g) for g in groups) + 0.3, 1.3)
    ax.set_axis_off()
    ax.set_title("Lean files of the Barnette proof, grouped by paper section; arrow A -> B: A uses B "
                 "(transitive reduction; width ~ number of declaration-level uses)", fontsize=9)
    fig.tight_layout()
    fig.savefig(gdir / "files.png", dpi=150)


if __name__ == "__main__":
    main()
