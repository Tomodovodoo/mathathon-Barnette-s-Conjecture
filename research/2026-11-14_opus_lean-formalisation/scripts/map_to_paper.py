"""Assign every Lean declaration to a statement of the OpenAI paper, then total the effort.

Usage (from the repository root):
    python -I research/2026-11-14_opus_lean-formalisation/scripts/map_to_paper.py \
        research/2026-11-14_opus_lean-formalisation/graph/lean-decls.json \
        papers/text/OpenAI-Barnette.txt \
        research/2026-11-14_opus_lean-formalisation/graph

The assignment is by hand-written rules (file, then a regex on the declaration name,
first match wins).  I wrote the rules after reading every statement; they are an
editorial judgement, recorded here so that anyone can change a rule and rerun.
Output: graph/lean-to-paper.json, graph/lean-to-paper-full.md, graph/effort.json,
graph/effort.md, graph/effort.png (if matplotlib is available).
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Tags: (section key, label).  Section keys group tags for the effort table.
T = {
    "stmt": ("1", "Thm 1.1: statement and definitions"),
    "emb": ("E", "no counterpart: drawing in R^2 -> algebraic dual (grid minor)"),
    "dual": ("D", "no counterpart: algebraic duality, rank and Euler"),
    "jordan": ("D", "no counterpart: cycle of T = bond of G (algebraic Jordan curve)"),
    "minor": ("D", "no counterpart: duality survives deletion/contraction"),
    "graph": ("D", "no counterpart: generic graph and cycle bookkeeping"),
    "thm11": ("7", "Sec 7, proof of Thm 1.1: G has no 1-,2-cuts, T simple triangulation, 2-factor -> cycle"),
    "l21": ("2", "Lemma 2.1 (complement of a forest is connected)"),
    "states": ("2", "Sec 2: states, pairs, (2.1) counts"),
    "p31flow": ("3", "Prop 3.1: degree-2 subgraph -> two matchings (Hall, replaces max-flow)"),
    "p31dens": ("3", "Prop 3.1: density inequality (3.1)-(3.4)"),
    "p31face": ("3", "Prop 3.1: triangular regions of T[U] are faces (uses no separating triangle)"),
    "diskeul": ("4", "Lemma 4.1: Euler count (4.1) for the disk"),
    "disktop": ("4", "Lemma 4.1: the inside of a cycle is a disk (no pinch vertex)"),
    "l41": ("4", "Lemma 4.1 (disk identity), state count (4.2)"),
    "orient": ("4", "Sec 4: delta = black-face-on-left, from orientations of the black triangles"),
    "l52": ("5", "Lemma 5.2 (fixed-s cancellation, Q_s-cycle reversal)"),
    "l53": ("5", "Lemma 5.3 / (5.3): positive weights (replaced by a white-charge flow on G)"),
    "group": ("5", "Sec 5.3: regrouping pairs by D (orientations of cycles)"),
    "nonvan": ("5", "Sec 5.3: nonvanishing (5.4)-(5.5), polynomial version"),
    "p51": ("5", "Prop 5.1 (some pair has Q_s a forest)"),
    "l61": ("6", "Lemma 6.1 (one root per component of Q_s)"),
    "tree": ("6", "Sec 6.1: tree on the white faces, one selected edge per face"),
    "l62": ("6", "Lemma 6.2 (P is a forest)"),
    "ham": ("6", "Sec 6.2: complement of P is one cycle (replaces the induced-tree labelling)"),
    "irr": ("6", "Thm 2.2 without separating triangles (assembly)"),
    "glue": ("7", "Sec 7: cut at a separating triangle, cap, glue, induction"),
}

RULES = {
    "Model": [(r".", "stmt")],
    "Network": [(r"cubic_bipartite_order", "thm11"), (r"boundary_cover_of_threeConnected", "thm11"), (r".", "dual")],
    "CutSpaces": [(r"region_card_le_cut|cut_card_three|gradient_small_support|simple_dual", "thm11"),
                  (r"flow_no_leaf|Triangle$|triangle_of_flow", "thm11"), (r".", "graph")],
    "FlowCircuits": [(r"FlowCircuit$|circuit_two_levels|circuit_cut|dual_conserved|gradient_of_dual|flowSupport_eq|cycle_support_minimal|flowCircuit_of_cycle", "jordan"),
                     (r"gradient_indicator_support|cubic_face_triangles", "thm11"), (r".", "graph")],
    "Bonds": [(r"faces_vertex_deleted_connected|Triangle\.", "disktop"), (r".", "jordan")],
    "Quotients": [(r".", "minor")],
    "DiskRegions": [(r".", "diskeul")],
    "StateDisk": [(r"Duality\.symm|vertex_flow_circuit|cut_restrict_conserved|no_split|mixed_corner_on_boundary", "disktop"),
                  (r".", "l41")],
    "Circulation": [(r"proportional|Triangle\.coordinates|Triangle\.reverse|arcSign_opposite|oriented_face", "orient"),
                    (r".", "l53")],
    "TriangleSystem": [(r"oriented_cycleFlow|cycle_integral|oriented_integral|potential|side", "l53"),
                       (r"blackGradient_face|index_delta|indexDelta", "orient"),
                       (r"oppositeGraph|thirdIndex|other_corners", "l52"), (r".", "states")],
    "ColoredDual": [(r"cycle_disk", "l41"), (r"weights", "l53"), (r"StateCycle", "nonvan"), (r".", "states")],
    "CycleReversal": [(r"cycleCoordinates_of_not_acyclic", "graph"), (r".", "l52")],
    "PairPhases": [(r"disk_count_identity", "l41"), (r"^phase|phase_add|phase_sub", "l52"),
                   (r"rawIndexSum|Partners|faceSet|cyclicDelta|reverse_|fixed_second", "l52"),
                   (r".", "group")],
    "PairPolynomials": [(r"secondFiberEquiv|sum_second_states|forest_pair_of_disk", "p51"),
                        (r"orient_left|orient_right|orient_delta|orient_rawIndex|orient_phase|cycleFaces|cycleDelta|GroupIndex|groupIndex|sum_groups", "group"),
                        (r".", "nonvan")],
    "Forest": [(r"opposite", "l52"), (r"forest_pair$", "p51"),
               (r"connected_of_kernel|Components|componentMap|descends", "graph"), (r".", "nonvan")],
    "Contraction": [(r"region_cut_subset|rim_cut_count|cut_le_rim|rim_of_shore_univ|rim_ge_three|rim_three|singleton_region_star|star_subset_eq|complement_singleton_root|TrivialThreeCuts", "p31face"),
                    (r"ThreeEdgeConnected", "thm11"), (r".", "p31dens")],
    "MinorDuality": [(r".", "p31dens")],
    "BMatching": [(r"exists_value", "states"), (r"nonroots_card|corner_filter_card|state_capacity|pair_nonempty", "p31dens"),
                  (r".", "p31flow")],
    "Matching": [(r"not_acyclic|acyclic_conserved_zero|Simple\.restrict|extend_restriction|conserved_supported_acyclic|complement_connected", "l21"),
                 (r"addSink|augQ|rootStart|QNet|q_graph|pair_val_ne", "l61"), (r".", "tree")],
    "ForestMatching": [(r"matching_cut_balance|reverseCycle|directed_cycle|matchingEdge|selectNet|selected_forest", "l62"),
                       (r"recover_connected_complement", "ham"), (r".", "tree")],
    "ThreeCuts": [(r"irreducible_matching", "irr"),
                  (r"gradient_small_support_edge|simple_dual_edge|cubic_face_triangles_edge|make_coloredDual|simple_of_cubic_stars", "thm11"),
                  (r"ThreeEdgeConnected\.connected|threeCut_bond", "graph"),
                  (r"boundary_range_restrict|exists_independent_restriction|duality_of_first_exact", "minor"),
                  (r".", "glue")],
    "CappedDuality": [(r"push_pull|pull_push|split_support|push_boundary_on_internal|Duality\.minor", "minor"),
                      (r"SimpleCycle", "thm11"), (r".", "glue")],
    "Gluing": [(r"restrict_star_image|matching_complement_two", "thm11"), (r"connected_complement_matching", "glue"), (r".", "glue")],
    "Traces": [(r".", "emb")], "SquareGrid": [(r".", "emb")], "Corridors": [(r".", "emb")],
    "MinorModel": [(r".", "emb")], "BranchPartition": [(r".", "emb")],
    "Rectangle": [(r".", "emb")], "ExactDual": [(r"Realizes|minor_quotient|graphMinor|connectedFibers_of_partition|exists_dart", "emb"), (r".", "emb")],
    "Main": [(r".", "thm11")],
}

SECTION_NAMES = {
    "1": "Sec 1 (statement)", "2": "Sec 2 (plane trees, states)", "3": "Sec 3 (Prop 3.1)",
    "4": "Sec 4 (disk identity)", "5": "Sec 5 (cancellation)", "6": "Sec 6 (two induced trees)",
    "7": "Sec 7 (separating triangles, Thm 1.1)", "D": "no counterpart: algebraic duality layer",
    "E": "no counterpart: embedding -> dual",
}

# Paper text line ranges per section (papers/text/OpenAI-Barnette.txt, pdftotext -layout),
# found with grep for the section headers.  Section 1 includes 1.1.
PAPER_RANGES = {"1": (13, 94), "2": (95, 129), "3": (130, 208), "4": (209, 243),
                "5": (244, 378), "6": (379, 448), "7": (449, 510)}


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    paper = Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
    out = Path(sys.argv[3])
    rows = []
    for n in data["nodes"]:
        short = n["name"].replace("OAI.Barnette.", "")
        tag = None
        for rx, t in RULES[n["module"]]:
            if re.search(rx, short):
                tag = t
                break
        n["paper_tag"] = tag
        n["paper_label"] = T[tag][1]
        n["paper_section"] = T[tag][0]
        rows.append(n)
    json.dump({"tags": T, "nodes": [{k: n[k] for k in ("name", "module", "start_line", "lines", "kind",
                                                     "paper_tag", "paper_label", "paper_section",
                                                     "reachable_from_main")} for n in rows]},
              open(out / "lean-to-paper.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # full table
    lines = ["# Every Lean declaration with its paper counterpart (generated)", "",
             "Generated by `scripts/map_to_paper.py` from `graph/lean-decls.json`. `lines` counts non-blank,",
             "non-comment lines of the declaration including its proof. `reach` = reachable from `OAI.Barnette.main`",
             "in the approximate dependency graph.", "",
             "| file:line | declaration | kind | lines | reach | paper counterpart |", "| --- | --- | --- | --- | --- | --- |"]
    for n in rows:
        short = n["name"].replace("OAI.Barnette.", "")
        lines.append(f"| {n['module']}:{n['start_line']} | `{short}` | {n['kind']} | {n['lines']} | "
                     f"{'y' if n['reachable_from_main'] else 'n'} | {n['paper_label']} |")
    (out / "lean-to-paper-full.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # effort
    tag_lines, sec_lines = {}, {}
    for n in rows:
        tag_lines[n["paper_tag"]] = tag_lines.get(n["paper_tag"], 0) + n["lines"]
        sec_lines[n["paper_section"]] = sec_lines.get(n["paper_section"], 0) + n["lines"]
    total = sum(sec_lines.values())
    paper_lines = {k: sum(1 for l in paper[a - 1:b] if l.strip()) for k, (a, b) in PAPER_RANGES.items()}
    ptotal = sum(paper_lines.values())
    eff = {"lean_lines_by_tag": tag_lines, "lean_lines_by_section": sec_lines,
           "lean_total": total, "paper_lines_by_section": paper_lines, "paper_total": ptotal}
    json.dump(eff, open(out / "effort.json", "w", encoding="utf-8"), indent=1)
    md = ["# Effort distribution (generated)", "",
          f"Lean: {total} counted lines in declarations (raw file total {sum(data['file_lines'].values())}).",
          f"Paper: {ptotal} non-blank text lines in Sections 1-7 of `papers/text/OpenAI-Barnette.txt`.", "",
          "| paper section | paper lines | paper % | Lean lines | Lean % | ratio Lean%/paper% |",
          "| --- | --- | --- | --- | --- | --- |"]
    for k in ["1", "2", "3", "4", "5", "6", "7", "D", "E"]:
        pl = paper_lines.get(k, 0)
        ll = sec_lines.get(k, 0)
        ratio = f"{(ll / total) / (pl / ptotal):.2f}" if pl else "n/a"
        md.append(f"| {SECTION_NAMES[k]} | {pl} | {100 * pl / ptotal:.0f} | {ll} | {100 * ll / total:.0f} | {ratio} |")
    md += ["", "| paper statement (tag) | Lean lines |", "| --- | --- |"]
    for t, (s, lab) in T.items():
        md.append(f"| {lab} | {tag_lines.get(t, 0)} |")
    (out / "effort.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        keys = ["1", "2", "3", "4", "5", "6", "7", "D", "E"]
        labels = [SECTION_NAMES[k].replace(" (", "\n(") for k in keys]
        pp = [100 * paper_lines.get(k, 0) / ptotal for k in keys]
        lp = [100 * sec_lines.get(k, 0) / total for k in keys]
        fig, ax = plt.subplots(figsize=(10, 4.2))
        x = range(len(keys))
        ax.bar([i - 0.2 for i in x], pp, width=0.4, label="paper (% of text lines)", color="#4C78A8")
        ax.bar([i + 0.2 for i in x], lp, width=0.4, label="Lean (% of proof lines)", color="#F58518")
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_ylabel("% of total")
        ax.legend(frameon=False)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_title("Where the words go: paper vs Lean formalisation", fontsize=10)
        fig.tight_layout()
        fig.savefig(out / "effort.png", dpi=150)
    except ImportError:
        print("matplotlib not available, no effort.png")


if __name__ == "__main__":
    main()
