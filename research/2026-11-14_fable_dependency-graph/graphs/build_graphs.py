"""Single source for the dependency graphs.

Run from research/2026-11-14_fable_dependency-graph/:
    python graphs/build_graphs.py
Writes graphs/{openai,li,trees,merged}.dot and renders each to .pdf and .svg
with matplotlib (Graphviz `dot` was not on PATH when this was written; the DOT
files are plain Graphviz and render with `dot -Tpdf x.dot -o x.pdf` as well).

An edge A -> B means "A is used to prove B".
Node spec: id: (label, layer, role, classification, status)
  role: core      every one of the three proofs passes through this node
        variant   one paper's way of proving a core node
        extra     proved by one paper, not needed by the others
        side      side condition or case hypothesis
        packaging presentation device, removable
"""
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))

STYLE = {  # role: (fill, edge colour, line style)
    "core": ("#dbe9f6", "#1f4e79", "solid"),
    "variant": ("#fdf3d0", "#8a6d00", "solid"),
    "extra": ("#e4f1e0", "#2f6b2f", "dashed"),
    "side": ("#f3e3ea", "#8b2252", "dotted"),
    "packaging": ("#eeeeee", "#555555", "dashed"),
}

OPENAI = {
    "nodes": {
        "HYP": ("G cubic, bipartite, planar, 3-connected", 0, "side", "hypothesis", "discharged"),
        "O1": ("O1, O2: T = G* simple triangulation, faces 2-coloured", 1, "core", "proved earlier", "discharged"),
        "E1": ("(2.1): |A| = |X| = k - 1", 2, "core", "algebraic/logical step", "discharged"),
        "L21": ("Lemma 2.1: plane-tree duality", 2, "core", "proved earlier", "discharged"),
        "P5": ("P5: triangular faces of K are faces of T [no separating triangle]", 2, "side", "side condition", "discharged"),
        "C3": ("Prop 3.1: a pair exists (flow + density bound)", 3, "core", "major claim", "discharged"),
        "C4": ("Lemma 4.1: disk identity", 3, "core", "major claim", "discharged"),
        "C53": ("Lemma 5.3: unit spoke circulations", 3, "variant", "proved earlier", "discharged"),
        "N2": ("(5.1): J integer, J = #cw - #ccw", 4, "core", "proved earlier", "discharged"),
        "C52": ("Lemma 5.2: cancellation for fixed s", 4, "core", "major claim", "discharged"),
        "N3": ("5.3: regroup pairs by undirected D", 4, "core", "algebraic/logical step", "discharged"),
        "N4c": ("N4b, N4c: spoke detour is a simple ccw cycle (slide)", 4, "packaging", "side condition", "discharged"),
        "N4": ("(5.3): L+(C) > L-(C)", 5, "core", "proved earlier", "discharged"),
        "N7": ("N6, N7: Taylor coefficient of order c_min is nonzero", 6, "variant", "algebraic/logical step", "discharged"),
        "C5": ("Prop 5.1: a pair with Q_s a forest", 7, "core", "major claim", "discharged"),
        "C61": ("Lemma 6.1: one root per component of Q_s", 8, "core", "proved earlier", "discharged"),
        "W": ("6.1: H - s spanning tree, white tree, selected set P", 9, "core", "proved earlier", "discharged"),
        "C62": ("Lemma 6.2: P is a forest (disk identity for s)", 10, "variant", "major claim", "discharged"),
        "S": ("6.2: dual cycle, two induced trees, pattern at t0", 11, "core", "proved earlier", "discharged"),
        "C1b": ("Theorem 2.2 without separating triangles", 12, "core", "major claim", "discharged"),
        "C1g": ("Section 7: gluing over a separating triangle", 12, "core", "major claim", "discharged"),
        "C1": ("Theorem 2.2", 13, "core", "major claim", "discharged"),
        "O3": ("O3: two induced trees give a Hamiltonian cycle", 13, "core", "proved earlier", "discharged"),
        "C0": ("Theorem 1.1 and Corollary 7.1", 14, "core", "root", "discharged"),
        "X72": ("Corollary 7.2 (needs [5, Thm 4.16], not opened)", 15, "extra", "named theorem", "open"),
    },
    "edges": [("HYP", "O1"), ("O1", "E1"), ("O1", "P5"), ("E1", "C3"), ("P5", "C3"), ("O1", "C4"),
              ("C4", "N2"), ("C4", "C52"), ("C4", "C62"), ("C53", "N4"), ("N4c", "N4"), ("N2", "N7"),
              ("N3", "N7"), ("N4", "N7"), ("C3", "C5"), ("C52", "C5"), ("N7", "C5"), ("C5", "C61"),
              ("C61", "W"), ("L21", "W"), ("W", "C62"), ("C62", "S"), ("L21", "S"), ("S", "C1b"),
              ("C1b", "C1"), ("C1g", "C1"), ("O1", "C1g"), ("C1", "C0"), ("O3", "C0"), ("L21", "O3"),
              ("C0", "X72")],
}

LI = {
    "nodes": {
        "HYP": ("G Barnette graph, e0 = b0 w0", 0, "side", "hypothesis", "discharged"),
        "E0": ("E0: straight-line drawing of aux(G), general position (undefined in the note)", 1, "packaging", "side condition", "discharged"),
        "Q1a": ("Q1a: |B'| = |F'| (not stated)", 1, "side", "side condition", "discharged"),
        "Q1": ("Theorem 10 (Ore): deficit condition", 2, "core", "named theorem", "discharged"),
        "Q7": ("Q2-Q7: minimal deficient S gives a non-trivial 3-edge cut [cyclic 4-edge-conn.]", 2, "variant", "hypothesis", "discharged"),
        "C6": ("Lemma 9: Li's H has a 2-factor", 3, "core", "major claim", "discharged"),
        "C25": ("Claim 25: t_out - t_in = 3 (disk identity)", 3, "core", "major claim", "discharged"),
        "C26": ("Claim 26: cw' as a sum of local turns", 4, "core", "proved earlier", "discharged"),
        "C16": ("Lemma 16: swap along a cycle of M1 u M2 flips cw", 4, "core", "algebraic/logical step", "discharged"),
        "I3": ("iota_2: pair consecutive ray crossings", 4, "variant", "algebraic/logical step", "discharged"),
        "C17": ("Lemma 17: swap along a cycle of H - M2 flips cw", 5, "core", "major claim", "discharged"),
        "I1": ("iota_1 and Lemma 34: flip the first cycle of H - M2", 6, "core", "proved earlier", "discharged"),
        "I4": ("Lemma 35: iota_2 reverses the sign", 6, "variant", "proved earlier", "discharged"),
        "I5": ("Lemma 24: fixed points of iota_2 share a sign, and exist", 6, "variant", "proved earlier", "discharged"),
        "B": ("Appendix B: c_min > 1 (sketch, three steps supplied in the audit)", 6, "variant", "major claim", "discharged"),
        "C2": ("Lemma 7 (Key Lemma): cycle-breaking 2-factor", 7, "core", "major claim", "discharged"),
        "C3": ("Lemma 8: G_FB - M2 is a spanning tree", 8, "core", "major claim", "discharged"),
        "C4": ("Corollary 27: white tree T_W = M2*", 9, "core", "named theorem", "discharged"),
        "T2": ("Claim 31: P is a perfect matching of G", 10, "core", "algebraic/logical step", "discharged"),
        "C5": ("Lemma 30: E(G) - P is one cycle (innermost cycle, no disk identity)", 11, "variant", "major claim", "discharged"),
        "C1": ("Theorem 4", 12, "core", "major claim", "discharged"),
        "A": ("Appendix C: non-trivial 3-edge cuts, contraction and gluing", 12, "core", "proved earlier", "discharged"),
        "C0": ("Theorem 3", 13, "core", "root", "discharged"),
    },
    "edges": [("HYP", "E0"), ("HYP", "Q1a"), ("HYP", "Q7"), ("Q1a", "Q1"), ("Q1", "C6"), ("Q7", "C6"),
              ("E0", "C25"), ("C25", "C26"), ("C25", "C17"), ("C26", "C17"), ("C17", "I1"), ("E0", "I3"),
              ("I3", "I4"), ("C16", "I4"), ("I3", "I5"), ("C16", "B"), ("I3", "B"), ("C6", "C2"),
              ("I1", "C2"), ("I4", "C2"), ("I5", "C2"), ("B", "C2"), ("C2", "C3"), ("C3", "C4"),
              ("C4", "T2"), ("T2", "C5"), ("C5", "C1"), ("C1", "C0"), ("A", "C0"), ("HYP", "A")],
}

TREES = {
    "nodes": {
        "HYP": ("G cubic, bipartite, planar, 3-connected, edge e", 0, "side", "hypothesis", "discharged"),
        "O1": ("T = G* simple triangulation, 2-coloured, counts (2)", 1, "core", "proved earlier", "discharged"),
        "E3": ("(3): H - s tree iff Q_s rooted forest", 2, "core", "algebraic/logical step", "discharged"),
        "C21": ("Prop 2.1: mates, 2^k, unique mate iff tree matching", 2, "extra", "proved earlier", "discharged"),
        "S6": ("S6, S7: balance-1 triangle is a face; region of t0 costs one [no black-inner triangle]", 2, "side", "hypothesis", "discharged"),
        "S3": ("S3: a black-inner triangle violates (5) by one", 2, "extra", "algebraic/logical step", "discharged"),
        "C41": ("Lemma 4.1: disk identity, odd length", 2, "core", "major claim", "discharged"),
        "F23": ("Section 3: (ii) iff (iii)", 3, "core", "major claim", "discharged"),
        "C42": ("Lemma 4.2: every exchange reverses epsilon", 3, "core", "major claim", "discharged"),
        "C51": ("Lemma 5.1: integer weights, L+ > L-", 3, "core", "proved earlier", "discharged"),
        "C61": ("Lemma 6.1: one permutation sign, M = |det K_B| <= 3^{n/2}", 3, "extra", "proved earlier", "discharged"),
        "C52": ("Theorem 5.2: a tree pair in every exchange component", 4, "core", "major claim", "discharged"),
        "C53": ("Theorem 5.3: marked walk (two involutions)", 4, "extra", "major claim", "discharged"),
        "C12": ("Theorem 1.2: incidence-tree criterion", 5, "core", "major claim", "discharged"),
        "P62": ("Prop 6.2: prefix enumeration", 6, "extra", "proved earlier", "discharged"),
        "L71": ("Lemma 7.1: white tree, P forest, two induced trees", 6, "core", "major claim", "discharged"),
        "G73": ("7.3: cut only at black-inner triangles, glue", 7, "core", "proved earlier", "discharged"),
        "TB": ("time bound O(poly(N) 3^{N/4})", 7, "extra", "algebraic/logical step", "discharged"),
        "C0": ("Theorem 1.1", 8, "core", "root", "discharged"),
        "XC": ("companion: BFS and random-walk constructors (not supplied)", 9, "extra", "missing", "open"),
    },
    "edges": [("HYP", "O1"), ("O1", "E3"), ("O1", "S6"), ("O1", "S3"), ("O1", "C41"), ("S6", "F23"),
              ("S3", "F23"), ("C41", "C42"), ("C21", "C42"), ("C41", "C61"), ("C42", "C52"),
              ("C51", "C52"), ("C21", "C52"), ("E3", "C52"), ("C42", "C53"), ("C51", "C53"),
              ("E3", "C12"), ("C21", "C12"), ("F23", "C12"), ("C52", "C12"), ("C12", "P62"),
              ("C61", "P62"), ("C41", "L71"), ("C12", "G73"), ("L71", "G73"), ("P62", "C0"),
              ("G73", "C0"), ("C61", "TB"), ("TB", "C0"), ("C53", "XC")],
}

MERGED = {
    "nodes": {
        "HYP": ("Hypotheses: G cubic, bipartite, planar, 3-connected", 0, "side", "hypothesis", "discharged"),
        "K0": ("K0 rooted Eulerian triangulation: T simple, 2-coloured, t0, e0\nO: O1,O2 | L: aux(G), b0 w0 | T: O1", 1, "core", "proved earlier", "discharged"),
        "K1": ("K1 balanced incidence graph B, |A| = |X| = n\nO: (2.1) | L: unstated (Q1a) | T: (2)", 2, "core", "algebraic/logical step", "discharged"),
        "K3": ("K3 disk identity\nO: Lemma 4.1 | L: Claim 25 | T: Lemma 4.1", 2, "core", "major claim", "discharged"),
        "K10a": ("plane-tree duality\nO: Lemma 2.1 | L: tree-cotree | T: 7.1", 2, "core", "named theorem", "discharged"),
        "V2a": ("density bound on every component of T[U]\n[no separating triangle]  O: P5-P9", 3, "variant", "side condition", "discharged"),
        "V2b": ("minimal deficient set gives a 3-edge cut\n[cyclic 4-edge-connected]  L: Q2-Q7", 3, "variant", "side condition", "discharged"),
        "V2c": ("exact: region of t0 treated apart\n[no black-inner triangle], with converse  T: S3-S9", 3, "variant", "side condition", "discharged"),
        "K2": ("K2 two disjoint states exist (a pair)\nO: Prop 3.1 | L: Lemma 9 | T: Section 3", 4, "core", "major claim", "discharged"),
        "K4": ("K4 sign of a pair; D-reversal and Q_s-reversal both flip it\nO: (5.1), Lemma 5.2 | L: Lemmas 16, 17 | T: Lemma 4.2", 4, "core", "major claim", "discharged"),
        "V5a": ("unit circulation by dual paths + slide onto spokes\nO: Lemma 5.3 | T: Lemma 5.1", 4, "variant", "proved earlier", "discharged"),
        "V5b": ("vertical rays from white vertices in a straight-line drawing\nL: Remark 19, Definition 20", 4, "variant", "proved earlier", "discharged"),
        "K5": ("K5 weights with L+(C) > L-(C) on every D-cycle", 5, "core", "proved earlier", "discharged"),
        "K6": ("K6 cancellation for fixed s (reverse a cycle of Q_s)\nO: Lemma 5.2 | L: iota_1 | T: beta", 5, "core", "major claim", "discharged"),
        "V7a": ("Taylor coefficient of order c_min of Z(x)\nO: (5.4), (5.5)", 6, "variant", "algebraic/logical step", "discharged"),
        "V7b": ("iota_2: fixed points of one sign, c_min marks\nL: Lemmas 24, 35, App. B", 6, "variant", "algebraic/logical step", "discharged"),
        "V7c": ("coefficient of (z-1)^m of Z_C(z), per component\nT: Theorem 5.2", 6, "variant", "algebraic/logical step", "discharged"),
        "V7d": ("marked walk, restart with two fewer cycles\nT: Theorem 5.3", 6, "extra", "algebraic/logical step", "discharged"),
        "K7": ("K7 the grouped count is not zero:\nsum over D with fewest cycles of prod (L+ - L-) > 0", 7, "core", "major claim", "discharged"),
        "K8": ("K8 a pair with Q_s a forest = tree matching s (H - s spanning tree)\nO: Prop 5.1, Lemma 6.1 | L: Lemmas 7, 8 | T: Thm 5.2, (3), Prop 2.1", 8, "core", "major claim", "discharged"),
        "K10": ("K10 white tree: dual of the deleted spokes\nO: 6.1 | L: Cor 27 | T: 7.1", 9, "core", "proved earlier", "discharged"),
        "K11": ("K11 selected set P: one side per face of T = perfect matching of G\nO: 6.1 | L: Claim 31 | T: 7.1", 10, "core", "algebraic/logical step", "discharged"),
        "V12a": ("P is a forest: selected-side count against the disk identity\nO: Lemma 6.2 | T: Lemma 7.1", 11, "variant", "major claim", "discharged"),
        "V12b": ("innermost root-free cycle, out-degree-one walk on a tree of faces\nL: Lemma 30", 11, "variant", "major claim", "discharged"),
        "K12": ("K12 E(G) - P is a Hamiltonian cycle avoiding e0\n(O, T: equivalently two induced trees of T)", 12, "core", "major claim", "discharged"),
        "K15": ("K15 cut along a separating triangle / 3-edge cut, prescribe the cap edge, glue\nO: Section 7 | L: App. C | T: 7.3 (black-inner only)", 12, "core", "major claim", "discharged"),
        "K16": ("Barnette's conjecture, with a prescribed avoided edge\nO: Thm 1.1, Cor 7.1 | L: Thm 3 | T: Thm 1.1", 13, "core", "root", "discharged"),
        "X1": ("T only: Prop 2.1, s is a tree matching iff it has exactly one mate", 8, "extra", "proved earlier", "discharged"),
        "X2": ("T only: Lemma 6.1, all states have one permutation sign; enumeration, 3^{n/2}", 5, "extra", "proved earlier", "discharged"),
        "X3": ("O only: Corollary 7.2 (cited theorem, open)", 14, "extra", "named theorem", "open"),
    },
    "edges": [("HYP", "K0"), ("K0", "K1"), ("K0", "K3"), ("K1", "V2a"), ("K1", "V2b"), ("K1", "V2c"),
              ("V2a", "K2"), ("V2b", "K2"), ("V2c", "K2"), ("K3", "K4"), ("K3", "X2"), ("V5a", "K5"),
              ("V5b", "K5"), ("K4", "K6"), ("K2", "V7a"), ("K2", "V7b"), ("K2", "V7c"), ("K5", "V7a"),
              ("K5", "V7b"), ("K5", "V7c"), ("K5", "V7d"), ("K4", "V7a"), ("K4", "V7b"), ("K4", "V7c"),
              ("K4", "V7d"), ("V7a", "K7"), ("V7b", "K7"), ("V7c", "K7"), ("V7d", "K7"), ("K6", "K8"),
              ("K7", "K8"), ("K8", "X1"), ("K8", "K10"), ("K10a", "K10"), ("K10", "K11"),
              ("K11", "V12a"), ("K11", "V12b"), ("K3", "V12a"), ("V12a", "K12"), ("V12b", "K12"),
              ("K12", "K16"), ("K15", "K16"), ("K0", "K15"), ("K16", "X3")],
}


def write_dot(name, g, title):
    lines = [f'digraph "{name}" {{', '  rankdir=TB;', f'  label="{title}"; labelloc=t;',
             '  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10];']
    for nid, (label, layer, role, cls, status) in g["nodes"].items():
        fill, edge, ls = STYLE[role]
        lab = label.replace('"', "'").replace("\n", "\\n")
        style = "rounded,filled" + ("" if ls == "solid" else "," + ls)
        lines.append(f'  {nid} [label="{lab}", role="{role}", classification="{cls}", status="{status}", '
                     f'layer={layer}, fillcolor="{fill}", color="{edge}", style="{style}"'
                     + (', peripheries=2' if status == "open" else "") + '];')
    layers = {}
    for nid, spec in g["nodes"].items():
        layers.setdefault(spec[1], []).append(nid)
    for layer in sorted(layers):
        lines.append("  { rank=same; " + "; ".join(layers[layer]) + "; }")
    for a, b in g["edges"]:
        lines.append(f"  {a} -> {b};")
    lines.append("}")
    with open(os.path.join(HERE, name + ".dot"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def draw(name, g, title, wrap=30, width=20):
    layers = {}
    for nid, spec in g["nodes"].items():
        layers.setdefault(spec[1], []).append(nid)
    nl = max(layers) + 1
    fig, ax = plt.subplots(figsize=(width, 1.55 * nl + 1.5))
    pos = {}

    def place():
        for layer, ids in layers.items():
            for i, nid in enumerate(ids):
                pos[nid] = ((i + 0.5) / len(ids), 1 - (layer + 0.5) / nl)

    place()
    nbrs = {nid: [] for nid in g["nodes"]}
    for a, b in g["edges"]:
        nbrs[a].append(b); nbrs[b].append(a)
    for sweep in range(6):  # barycentre ordering to reduce crossings
        order = sorted(layers) if sweep % 2 == 0 else sorted(layers, reverse=True)
        for layer in order:
            def key(nid):
                xs = [pos[m][0] for m in nbrs[nid] if g["nodes"][m][1] != layer]
                return sum(xs) / len(xs) if xs else pos[nid][0]
            layers[layer].sort(key=key)
            place()
    for a, b in g["edges"]:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        rad = 0.0 if abs(g["nodes"][a][1] - g["nodes"][b][1]) <= 1 else 0.18
        ax.add_patch(FancyArrowPatch((xa, ya - 0.012), (xb, yb + 0.012), arrowstyle="-|>",
                                     mutation_scale=11, lw=0.8, color="#444444",
                                     connectionstyle=f"arc3,rad={rad}", shrinkA=16, shrinkB=16, zorder=1))
    for nid, (label, layer, role, cls, status) in g["nodes"].items():
        fill, edge, ls = STYLE[role]
        text = "\n".join("\n".join(textwrap.wrap(part, wrap)) for part in label.split("\n"))
        if status == "open":
            text += "\n[open]"
        ax.text(*pos[nid], text, ha="center", va="center", fontsize=7.5, zorder=3,
                bbox=dict(boxstyle="round,pad=0.35", fc=fill, ec=edge, lw=1.3, ls=ls))
    handles = [plt.Rectangle((0, 0), 1, 1, fc=f, ec=e, ls=s, lw=1.3) for f, e, s in STYLE.values()]
    ax.legend(handles, ["core (all three proofs)", "variant (one paper's route)", "extra (one paper only)",
                        "side condition or hypothesis", "packaging"], loc="lower right", fontsize=8,
              frameon=False, ncol=1)
    ax.set_title(title + "   (arrow A -> B: A is used to prove B)", fontsize=11)
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02); ax.axis("off")
    for ext in ("pdf", "svg"):
        fig.savefig(os.path.join(HERE, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    for name, g, title, wrap, width in [
        ("openai", OPENAI, "OpenAI: Paired states and Hamiltonian cycles", 30, 17),
        ("li", LI, "Li: A note on the proof of Barnette's conjecture", 30, 17),
        ("trees", TREES, "A constructive proof of Barnette's conjecture", 28, 20),
        ("merged", MERGED, "Merged dependency graph of the three proofs", 44, 22),
    ]:
        for a, b in g["edges"]:
            assert a in g["nodes"] and b in g["nodes"], (name, a, b)
        write_dot(name, g, title)
        draw(name, g, title, wrap, width)
        print(name, len(g["nodes"]), "nodes", len(g["edges"]), "edges")
