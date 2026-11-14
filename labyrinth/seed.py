#!/usr/bin/env python3
"""Seed the labyrinth from the route map and the agents' reports.

Writes labyrinth/knowledge.json, labyrinth/sota.json and the backfilled part of labyrinth/events.jsonl.
The route data come from digestions/route-map/routes.py, so the map and the labyrinth cannot drift apart.
Events appended later with `lab.py event` (no "backfilled" flag) are kept when this script is run again.

Command:  python -X utf8 -B labyrinth/seed.py
Then:     python -X utf8 -B labyrinth/lab.py check && python -X utf8 -B labyrinth/lab.py build

Tier policy (see labyrinth/README.md):
  T1  LIT. Classical results are published. The three 2026 papers are unrefereed preprints; the brief of this
      run files them as literature, and each such node says so in its status.
  T2  PROVED-HERE, with the review state of the agent folder it comes from. Referees are AI agents; no node is
      human-checked.
  T3  only the census cross-check, where two independent implementations agree instance by instance.
  T4  every other computation.   T5 conjectures (each with a test).   T6 hunches.
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
ROOT = LAB.parent
sys.path.insert(0, str(ROOT / "digestions" / "route-map"))
import routes as RT  # noqa: E402

DAY = "2026-11-14"
PAPER = {"O": "papers/OpenAI-Barnette.pdf", "L": "papers/A-Note-On-Barnette.pdf", "T": "papers/barnette_trees.pdf"}
PREFIX = {"LIT": "th", "PROVED-HERE": "p", "COMPUTED": "c", "CONJECTURE": "k", "HUNCH": "h", "REFUTED": "x"}


def nid(r):
    return f"{PREFIX[r['status']]}.{r['id']}"


def srcs(r):
    return [x.strip() for x in r["src"].split(",")]


def expand(where):
    out = where
    for tag, folder in RT.FOLDERS.items():
        out = out.replace(f"{tag}/", folder + "/")
    return out


def review_of(r):
    """Review state of a PROVED-HERE route: the weakest state among its source folders."""
    order = ["unreviewed", "under-review", "refereed"]
    revs = [RT.REVIEW.get(f, {"state": "unreviewed"}) for f in srcs(r) if f in RT.FOLDERS]
    worst = min(revs, key=lambda v: order.index(v["state"]))
    out = {"state": worst["state"], "date": DAY}
    by = sorted({b for v in revs for b in v.get("by", [])})
    if by:
        out["by"] = by
    verdicts = sorted({v["verdict"] for v in revs if v.get("verdict")})
    if verdicts:
        out["verdict"] = " | ".join(verdicts)
    return out


nodes = []

# ---- sources
SOURCES = [
    ("src.O", "OpenAI, Paired states and Hamiltonian cycles in cubic bipartite planar graphs (2026)",
     "papers/OpenAI-Barnette.pdf. Preprint, unrefereed. Reverse-Lamport audit: FOLLOWS (dependency-graph). A Lean formalisation exists upstream and builds locally (lean-formalisation)."),
    ("src.L", "Zhentao Li, A note on the proof of Barnette's conjecture, arXiv:2610.30490 (2026)",
     "papers/A-Note-On-Barnette.pdf. Preprint. Audit: FOLLOWS once four routine unwritten steps are supplied."),
    ("src.T", "A constructive proof of Barnette's conjecture (unsigned, dated 18 October 2026)",
     "papers/barnette_trees.pdf. No public source or author found (history-literature). Audit: FOLLOWS."),
    ("src.Lean", "The Lean formalisation in OpenAI's repository", "31 files, 8936 lines. Built locally by the lean-formalisation agent; axioms propext, Classical.choice, Quot.sound."),
    ("src.stein1971", "S. K. Stein, B-sets and planar maps, Pacific J. Math. 37 (1971)", "Hamiltonian dual iff two induced forests."),
    ("src.apsw2016", "Alt, Payne, Schmidt, Wood, Thoughts on Barnette's conjecture, Australas. J. Combin. 64 (2016)", "Two induced trees; Kelmans' equivalences; limitation theorem for colour classes."),
    ("src.kelmans", "A. K. Kelmans, 1986/1994", "Reduction to cyclically 4-edge-connected graphs. Read only through APSW and Hertel."),
    ("src.hertel2005", "A. Hertel, A survey and strengthening of Barnette's conjecture (2005)", "H-: every edge is avoided by some Hamiltonian cycle."),
    ("src.hinekalman2018", "Hine, Kalman, Clock theorems for triangulated surfaces, arXiv:1808.06091", "Trinity states, arborescence bijection, lattice of states."),
    ("src.kpw", "Kenyon, Propp, Wilson, Trees and matchings, arXiv:math/9903025", "Tree-to-matching bijection."),
    ("src.kenyon-dd", "R. Kenyon, Conformal invariance of loops in the double-dimer model, arXiv:1105.4158", "Double-dimer determinant with an SL2 connection; doubled edges are not suppressed."),
    ("src.thomason1978", "A. G. Thomason, Hamiltonian cycles and uniquely edge colourable graphs (1978)", "Parity of Hamiltonian cycles in cubic graphs, Corollary 1.5."),
    ("src.bgm2022", "Brinkmann, Goedgebeur, McKay, Math. Comp. (2022)", "Computer verification to 90 vertices."),
    ("src.schnieders2025", "Schnieders (2025)", "All faces of size at most 8; sharp for connected graphs."),
    ("src.federsubi2006", "Feder, Subi, ECCC TR06-015 (2006)", "Spanning trees of faces; parity problem."),
    ("src.bagheri2022", "Bagheri Gh., Feder, Fleischner, Subi, Fund. Inform. 188 (2022)", "Prescribed edge sets are NP-complete for Barnette graphs."),
    ("src.gsw2023", "Gorsky, Steiner, Wiederrecht, Discrete Math. 346 (2023)", "Braces and Pfaffian graphs; Theorem 4.16."),
]
for sid, title, st in SOURCES:
    nodes.append(dict(id=sid, kind="source", tier=None, status="source", title=title, statement=st, links=[], created=DAY, updated=DAY))
for tag, folder in RT.FOLDERS.items():
    rv = RT.REVIEW.get(tag, {"state": "unreviewed"})
    nodes.append(dict(id=f"src.agent.{tag}", kind="source", tier=None, status="agent folder",
                      title=folder.split("/")[-1], statement=f"Agent archive {folder}/. Review state of its proofs: {rv['state']}"
                      + (f" ({rv['verdict']})" if rv.get("verdict") else "") + ".",
                      where=[folder + "/REPORT.md"], links=[], created=DAY, updated=DAY))
SRC_NODE = {"O": "src.O", "L": "src.L", "T": "src.T", "Lean": "src.Lean"}

# ---- waypoints and steps
STEP_BY_TO = {}
for s in RT.STEPS:
    STEP_BY_TO.setdefault(s["to"], []).append(s)
for w in RT.WAYPOINTS:
    links = []
    for s in STEP_BY_TO.get(w["id"], []):
        if s["id"] in ("U", "TG"):
            continue
        links += [{"to": f"wp.{f}", "rel": "uses"} for f in s["frm"]]
    nodes.append(dict(id=f"wp.{w['id']}", kind="theorem", tier="T1",
                      status="established (LIT: waypoint of the 2026 proofs; the papers are unrefereed preprints)",
                      title=w["name"], statement=w["what"], links=links, tags=["waypoint"],
                      where=["digestions/route-map/ROUTE-MAP.md"], created=DAY, updated=DAY))
for s in RT.STEPS:
    nodes.append(dict(id=f"m.step.{s['id']}", kind="method", tier=None, status=s["verdict"],
                      title=f"Step {s['id']}: {s['title']}", statement=s["must"], note=s["freedom"], tags=["step"],
                      links=[{"to": f"wp.{f}", "rel": "uses"} for f in s["frm"]] + [{"to": f"wp.{s['to']}", "rel": "supports"}],
                      where=["digestions/route-map/ROUTE-MAP.md"], created=DAY, updated=DAY))

# ---- routes
STEP = {s["id"]: s for s in RT.STEPS}
for r in RT.ROUTES:
    st, s = r["status"], STEP[r["step"]]
    links = [{"to": f"m.step.{r['step']}", "rel": "instance-of"}]
    for f in srcs(r):
        if f in SRC_NODE:
            links.append({"to": SRC_NODE[f], "rel": "cites"})
        elif f in RT.FOLDERS:
            links.append({"to": f"src.agent.{f}", "rel": "cites"})
    n = dict(id=nid(r), title=r["label"], statement=r["text"], where=[expand(r["where"])], tags=[f"step {r['step']}"],
             created=DAY, updated=DAY)
    if st == "LIT":
        pre = all(f in ("O", "L", "T", "Lean") or f in RT.FOLDERS for f in srcs(r))
        n.update(kind="theorem", tier="T1",
                 status=("established (LIT: 2026 preprint or its formalisation, unrefereed)" if pre else "established (LIT: published)")
                 + (", partial result" if r.get("partial") else ""))
        links.append({"to": f"wp.{s['to']}", "rel": "supports"})
    elif st == "PROVED-HERE":
        rv = review_of(r)
        label = {"unreviewed": "unreviewed", "under-review": "under review",
                 "refereed": "1 independent AI referee; human check pending"}[rv["state"]]
        n.update(kind="theorem", tier="T2", status=f"established: proved here ({label})", review=rv)
        links.append({"to": f"wp.{s['to']}", "rel": "supports"})
    elif st == "COMPUTED":
        n.update(kind="evidence", tier="T4", status="computed", evidence=[expand(r["where"])])
        links.append({"to": f"wp.{s['to']}", "rel": "tests"})
    elif st == "CONJECTURE":
        n.update(kind="conjecture", tier="T5", status="open", test=r["test"])
        links.append({"to": f"wp.{s['to']}", "rel": "suggests"})
    elif st == "HUNCH":
        n.update(kind="hunch", tier="T6", status="live", vivid=r.get("vivid", ""), test=r["test"])
        links.append({"to": f"wp.{s['to']}", "rel": "suggests"})
    else:
        n.update(kind="deadend", tier=None, status="refuted", lesson=r["lesson"], note="Smallest known counterexample: " + r["cex"])
    n["links"] = links
    nodes.append(n)

IDS = {n["id"] for n in nodes}


def link(a, b, rel):
    assert a in IDS and b in IDS, (a, b)
    next(n for n in nodes if n["id"] == a)["links"].append({"to": b, "rel": rel})


# who refuted what
for a, b in [("p.U.5", "x.A.x1"), ("p.D.4", "x.N.x2"), ("p.K.2", "x.N.x12"), ("p.A.GT", "x.U.x5"), ("p.D.5", "x.U.x3"),
             ("p.C.5", "x.C.x1"), ("th.A.T", "x.R.x1"), ("p.N.H", "x.N.x7")]:
    if a in IDS and b in IDS:
        link(a, b, "refutes")
for a, b in [("p.N.lin", "th.N.O"), ("p.N.H", "th.N.O"), ("p.A.GT", "th.A.T"), ("p.K.1", "th.K.O"), ("p.F.1", "th.F.OT")]:
    link(a, b, "modifies")
for a, b in [("k.D.3", "p.D.2"), ("th.A.T", "th.A.O")]:
    link(a, b, "generalizes")

# ---- the census (the one T3 node), families, methods, doors
EXTRA = [
    dict(id="e.census16", kind="exhaustive", tier="T3",
         status="exhaustive for |V(T)| <= 16: two independent implementations agree instance by instance (no referee yet)",
         title="Census of states, pairs and tree matchings, all rooted Eulerian triangulations with at most 16 vertices",
         statement="7868 rooted triangulations (T, t0), 5088 with a pair. The multiset of (states, pairs, tree matchings) per size is the same in "
                   "the combinatorics lab (own generator) and in the algebra agent's counts (plantri 4.5 and workings/barnette_lab). "
                   "Totals: 140358 states, 24744 pairs, 24090 tree matchings. Positive tree-matching counts seen: 2, 4, 6, 8, 10, 12, 14, 16. "
                   "A third enumeration by the combinatorics referee agrees as well.",
         evidence=["labyrinth/make_frontier.py", "labyrinth/frontier_crosscheck.json",
                   "research/2026-11-14_fable_route-combinatorics/data/rows_v16.json", "research/2026-11-14_sol_route-algebra/counts.json",
                   "research/2026-11-14_astra_referee-combinatorics/code/"],
         review={"state": "unreviewed", "date": DAY},
         links=[{"to": "wp.FP", "rel": "tests"}, {"to": "k.D.3", "rel": "supports"}, {"to": "src.agent.comb", "rel": "cites"},
                {"to": "src.agent.alg", "rel": "cites"}, {"to": "src.agent.refc", "rel": "cites"}]),
    dict(id="f.octahedron", kind="family", status="named example", title="Octahedron (dual of the cube), 6 vertices",
         statement="n = 3, 2 states, 2 pairs, 2 tree matchings, cmin = 1. The smallest case; with zero weights Z = i - i = 0.",
         links=[{"to": "wp.FP", "rel": "instance-of"}]),
    dict(id="f.prism", kind="family", status="named example", title="Hexagonal prism dual (hexagonal bipyramid), 8 vertices",
         statement="3 states, 2 pairs, 2 tree matchings. The smallest example that separates: acyclic Q_s from tree matching, the raw determinant "
                   "from its squarefree coefficient, trinity arborescences from tree matchings, avoiding cycles (4) from recovered cycles (2).",
         links=[{"to": "x.R.x1", "rel": "supports"}, {"to": "x.N.x9", "rel": "supports"}, {"to": "x.U.x3", "rel": "supports"}, {"to": "x.A.x1", "rel": "supports"}]),
    dict(id="f.double-octahedron", kind="family", status="named example", title="Octahedron glued into a face of an octahedron, 9 vertices",
         statement="The smallest separating triangle. With t0 on the black side: 4 states, 4 pairs, 4 tree matchings, cmin = 2. "
                   "With t0 on the white side: 4 states, no pair.",
         links=[{"to": "th.A.T", "rel": "instance-of"}, {"to": "x.N.x7", "rel": "supports"}]),
    dict(id="f.rarity", kind="family", status="named family", title="q prism duals glued into white faces, 5q + 3 vertices",
         statement="3^q states and 2^q tree matchings: tree matchings are exponentially rare among states.",
         links=[{"to": "p.D.5", "rel": "instance-of"}]),
    dict(id="f.cls6-12", kind="family", status="named example", title="12 vertices, class 6, t0 = (2,7,3)",
         statement="9 states, 10 pairs, 8 tree matchings. Highest partnered state, all-counterclockwise minimal cover and largest rank difference "
                   "all fail here; its mirror image gives the lowest-state and clockwise failures.",
         links=[{"to": "x.N.x4", "rel": "supports"}, {"to": "x.N.x5", "rel": "supports"}, {"to": "x.N.x6", "rel": "supports"}]),
    dict(id="f.cls158-16", kind="family", status="named example", title="16 vertices, class 158, t0 = (2,7,3)",
         statement="A single 13-cycle cover whose two orientations both have a triangle in Q_s. The only failure of 'every cover has a forest "
                   "orientation' among 5088 rooted cases.", links=[{"to": "x.N.x3", "rel": "supports"}]),
    dict(id="f.split4", kind="family", status="named example", title="Octahedron with every face split in four, 18 vertices (n = 15)",
         statement="20 pairs; the 4 one-cycle pairs all have a cycle in Q_s and the 12 tree pairs all have three cycles. "
                   "The smallest example found with cyclic Q_s, three D-cycles and one exchange component.",
         links=[{"to": "x.N.x3", "rel": "supports"}]),
    dict(id="f.theta26", kind="family", status="named example", title="Theta of three cubes-minus-an-edge, 26 vertices",
         statement="2-connected, cubic, bipartite, planar, non-Hamiltonian. 8 states and no pair at every root.",
         links=[{"to": "x.S0.x2", "rel": "supports"}]),
    dict(id="f.torus3x3", kind="family", status="named example", title="3 x 3 triangular grid on the torus",
         statement="No two induced trees; the dual has 36 Hamiltonian cycles; a root-free pair exists with Q unicyclic.",
         links=[{"to": "x.S0.x3", "rel": "supports"}]),
    dict(id="m.two-evaluations", kind="method", status="the one new idea", title="A signed sum over pairs, evaluated two ways",
         statement="Fix s and cancel (support on forest pairs); fix D and factor (nonzero at lowest order). Absent from the Barnette literature before 2026.",
         links=[{"to": "wp.M", "rel": "uses"}, {"to": "wp.FP", "rel": "supports"}]),
    dict(id="m.enumeration", kind="method", status="tool", title="Exhaustive enumeration of rooted Eulerian triangulations",
         statement="Three independent generators (comb/lab/tri.py; plantri 4.5 in workings/barnette_lab; gt/code/tri.py) agree on the class counts "
                   "1, 0, 1, 1, 2, 2, 8, 8, 32, 57, 185 for 6 to 16 vertices.",
         links=[{"to": "e.census16", "rel": "supports"}]),
    dict(id="m.reverse-lamport", kind="method", status="tool", title="Reverse-Lamport audit",
         statement="Conclusion-first AND/OR obligation graphs; used on the three papers and on the weight-free proof.",
         links=[{"to": "p.G2.4", "rel": "supports"}]),
]
for e in EXTRA:
    e.setdefault("tier", None)
    e.setdefault("created", DAY)
    e.setdefault("updated", DAY)
    nodes.append(e)
IDS = {n["id"] for n in nodes}

DOORS = [
    ("q.poly-time", "Is there a polynomial-time construction of the Hamiltonian cycle?",
     "The proofs give exponential search (3^(N/4), or 2^O(n log n) for the marked walk). Sampling states is polynomial; tree matchings can be exponentially rare.",
     "First test: on the 40-vertex and 80-vertex failures of the lattice extremes (gt/code/data), check conjecture k.D.7 (min or max carries a tree pair) and "
     "count the orientations to be searched.", ["k.D.7", "h.D.8", "h.U.2h", "h.N.3"]),
    ("q.structural", "Is there an existence proof with no signed count?",
     "Every reformulation of the target is exact and none has an existence argument; every structural shortcut tested fails on long D-cycles.",
     "First test: conjecture k.U.7h (local search from a point-rainbow tree, 450 of 450 so far) at 18 vertices, recording the longest plateau; "
     "then k.N.11 on exhaustive exchange graphs at 20 to 30 vertices.", ["k.U.7h", "k.N.11", "h.U.1h", "h.N.5"]),
    ("q.canonical", "Is there a canonical forest pair?",
     "Seven extremal rules are refuted. Only 'lattice min or max' survives, on random samples.",
     "First test: exhaustive census to 24 vertices for k.D.7; apply the Hine-Kalman bijection to the 8 tree matchings of f.cls6-12 (k.D.6).", ["k.D.7", "k.D.6"]),
    ("q.tm-lower", "How many tree matchings must there be?",
     "Proved here: at least 2 cmin. Conjectured: at least 2^cmin (no exception among 5088 cases; equality in 4609).",
     "First test: extend the census to 17 and 18 vertices restricted to cmin >= 3 and look for a count below 8.", ["k.D.3", "p.D.2"]),
    ("q.det", "Is there a determinant or Pfaffian for Z without coefficient extraction?",
     "Z is the squarefree coefficient of one determinant (2^n evaluations). Raw determinants, doubled edges and scalar factorisations are refuted.",
     "First test: Grassmann-Pluecker identities for the six-value turn signature (h.N.4); the hexagonal prism polynomial is the regression test.", ["h.N.4", "h.N.1", "x.N.x9"]),
    ("q.which-hc", "Which Hamiltonian cycles come from tree matchings?",
     "Exactly those avoiding e0* whose state has a partner; equivalently partitions with acyclic white parent map. No description in G alone.",
     "First test: on the hexagonal prism compare the 2 partnered and 2 unpartnered avoiding cycles face by face (k.U.6h).", ["k.U.6h", "p.U.5"]),
    ("q.disk", "Is there a second proof of the disk identity?",
     "All papers use one double count. Parity suffices three times and the value 3 once (p.C.5). The topology agent derives the identity "
     "from the theorem of turning tangents (p.B.6); nobody has refereed that.",
     "First test: referee p.B.6 on the 9-vertex non-bijective disk (lim/examples/nonbijective_disk.json), where the angle structure must fail to be flat.",
     ["p.B.6", "h.B.3", "h.B.2", "h.B.1", "p.C.5"]),
    ("q.roots", "Can a different rooting remove the separating-triangle induction?",
     "With t0 a face the obstruction is exact. Roots of three colours not on a face are untested.",
     "First test: on the 9-vertex double octahedron with the obstructed root, enumerate all root triples and count pairs (k.A.2).", ["k.A.2", "k.G.3"]),
    ("q.li-b", "Do Li's higher-mark involutions match the polynomial coefficient?",
     "Li's Appendix B leaves three verifications to the reader; li.py was not refereed.",
     "First test: k.N.12 on an instance with cmin = 2.", ["k.N.12", "th.N.L"]),
    ("q.surface", "What is the right statement on other surfaces?",
     "States need |A| = |X|, which fails by 2g. The topology-free target is one edge per triangle with connected complementary dual.",
     "First test: on the 3 x 3 torus enumerate root-free pairs and classify Q by its cycle rank against the 36 Hamiltonian cycles.", ["x.S0.x3"]),
    ("q.formal", "What is the status of formal verification?",
     "The Lean proof builds locally with standard axioms and follows a different route in four places. Corollary 7.2 and Theorem 2.2 are not formalised.",
     "First test: state Corollary 7.1 for PlaneEmbedding in Lean (a few lines, lean/DIFFERENCES.md item 27).", ["c.G2.c", "th.G2.2"]),
    ("q.human", "Has a human checked any of the proofs written here?",
     "No. Two folders are AI-refereed (combinatorics, determinants), two are under review, the rest unreviewed.",
     "First test: a human reads refc/REWRITTEN-PROP-5-1.md and refd/SIGNIFICANCE.md Section 2, the two candidates for the main text.", ["p.N.H", "p.N.lin"]),
]
for qid, title, why, nxt, to in DOORS:
    nodes.append(dict(id=qid, kind="question", tier=None, status="open", title=title, statement=why, why=why, next=nxt,
                      links=[{"to": t, "rel": "suggests"} for t in to if t in IDS], created=DAY, updated=DAY))
IDS = {n["id"] for n in nodes}
for n in nodes:
    for l in n["links"]:
        assert l["to"] in IDS, (n["id"], l)

meta = {"title": "Barnette's conjecture: the labyrinth", "eyebrow": "mathathon, 14 November 2026",
        "subtitle": "Every waypoint of the proof, every route found or refuted, and its status. "
                    "Size |V(T)|, invariant: number of tree matchings of a rooted triangulation."}
frontier_history = [
    {"date": DAY, "size": 14, "resolved": 1.0, "why": "enumerations of route-combinatorics and route-algebra agree (55 triangulations, 1206 roots)"},
    {"date": DAY, "size": 16, "resolved": 1.0, "why": "the same agreement extended to 16 vertices (297 triangulations, 7868 roots)"},
]
(LAB / "knowledge.json").write_text(json.dumps({"schema": 1, "meta": meta, "nodes": nodes, "frontier_history": frontier_history},
                                               indent=1), encoding="ascii")

# ---------------------------------------------------------------- events (backfilled)
E = []


def ev(ts, typ, summary, nodes_=(), evidence=()):
    for i in nodes_:
        assert i in IDS, i
    E.append({"ts": ts, "type": typ, "summary": summary, "nodes": list(nodes_), "evidence": list(evidence), "backfilled": True})


ev("1971-01-01T00:00:00Z", "literature", "Stein: a cubic map is Hamiltonian iff its regions split into two classes with no region-cycle (two induced forests in the dual)", ["th.TG.1"])
ev("1986-01-01T00:00:00Z", "literature", "Kelmans: reduction to cyclically 4-edge-connected Barnette graphs with a strengthened hypothesis", ["th.G.K"])
ev("2005-04-29T00:00:00Z", "literature", "Hertel: avoiding any prescribed edge (H-) is equivalent to the conjecture", ["th.TG.2"])
ev("2022-01-01T00:00:00Z", "literature", "Brinkmann-Goedgebeur-McKay: verified to 90 vertices; Bagheri Gh. et al.: prescribed edge sets are NP-complete", ["th.TG.4", "x.G.x1"])
ev("2025-01-01T00:00:00Z", "literature", "Schnieders: all faces of size at most 8, without 3-connectivity; sharp", ["th.TG.3"])
ev("2026-10-06T00:00:00Z", "literature", "OpenAI repository public: paired states, disk identity, exponential sum, Lean files", ["th.G2.1", "th.N.O", "th.B.O", "th.G2.2"])
ev("2026-10-10T00:00:00Z", "monitor", "Third-party report (cert-machine): two Lean kernels accept the formal proof (not reproduced at that time)", ["th.G2.2"])
ev("2026-10-18T00:00:00Z", "literature", "Unsigned 'constructive proof': exact criterion, unique-partner characterisation, integer polynomial, marked walk", ["th.A.T", "th.N.T1", "th.N.T2", "th.R.1"])
ev("2026-10-21T00:00:00Z", "literature", "Zhentao Li, arXiv:2610.30490: primal exposition with two sign-reversing involutions", ["th.N.L", "th.F.L"])
ev("2026-11-14T10:03:30Z", "milestone", "Mathathon starts: research archive, agent protocol, text dumps of the three papers", [])
ev("2026-11-14T10:11:43Z", "computed", "Reference implementation workings/barnette_lab: states, pairs, recovery, gluing (route-constructive)", ["c.F.c"], ["workings/barnette_lab/"])
ev("2026-11-14T10:18:17Z", "computed", "Combinatorics lab: own generator of Eulerian triangulations, states, pairs, heights", ["m.enumeration"], ["research/2026-11-14_fable_route-combinatorics/lab/"])
ev("2026-11-14T10:20:32Z", "proved", "Z is the squarefree coefficient of one determinant; tree matchings are a coefficient of the tree-degree polynomial (machinery-literature, unreviewed)", ["p.U.1", "h.N.1"])
ev("2026-11-14T10:20:32Z", "refuted", "The local phase is not a product of a weight on r and a weight on s: no product of two dimer determinants", ["x.C.x1"])
ev("2026-11-14T10:20:42Z", "proposed", "Dimer route predictions written before the runs", ["src.agent.dim"], ["research/2026-11-14_astra_route-dimers/PREDICTIONS.md"])
ev("2026-11-14T10:23:12Z", "computed", "Node checks on 36 rooted triangulations, n from 3 to 23 (dependency-graph)", ["c.B.c", "c.K.c"], ["research/2026-11-14_fable_dependency-graph/data/check_nodes.txt"])
ev("2026-11-14T10:24:15Z", "computed", "Survey of all 7868 rooted Eulerian triangulations up to 16 vertices (route-combinatorics)", ["e.census16"], ["research/2026-11-14_fable_route-combinatorics/data/survey_v16.txt"])
ev("2026-11-14T10:24:15Z", "refuted", "Canonical choices fail: highest or lowest partnered state, one-way minimal cover, largest rank difference, forest pair inside every cover, cubes, one cycle", ["x.N.x4", "x.N.x5", "x.N.x6", "x.N.x3", "x.N.x8", "x.N.x7"], ["research/2026-11-14_fable_route-combinatorics/data/counterexamples.txt"])
ev("2026-11-14T10:24:52Z", "proved", "Real mixed determinant; linear weights 1 + xa give the same nonvanishing with degree at most n (route-dimers, under review)", ["p.N.lin", "p.K.2"])
ev("2026-11-14T10:26:08Z", "literature", "History, results table, 14 equivalent forms, what was hard (history-literature)", ["src.agent.hist", "x.TG.x2", "x.TG.x1"])
ev("2026-11-14T10:27:28Z", "refuted", "Ordinary determinant with all face variables 1 fails on the hexagonal prism; two-matroid relaxation and white-tree rejection fail", ["x.N.x9", "x.U.x1", "x.U.x2"], ["research/2026-11-14_sol_route-constructive/data/exact_determinant.json"])
ev("2026-11-14T10:27:28Z", "computed", "All checked statements of the three papers pass on 77 rooted runs (route-constructive)", ["c.A.c", "c.N.c"], ["research/2026-11-14_sol_route-constructive/VERIFICATION.md"])
ev("2026-11-14T10:28:37Z", "refuted", "Doubled edges make nonvanishing too easy; trinity arborescences are not tree matchings", ["x.N.x10", "x.U.x3"])
ev("2026-11-14T10:29:24Z", "documented", "Reverse-Lamport audits: OpenAI and trees paper FOLLOW; Li follows with four routine steps supplied (unreviewed)", ["p.G2.4", "m.reverse-lamport"], ["research/2026-11-14_fable_dependency-graph/audit-openai.md"])
ev("2026-11-14T10:33:18Z", "proved", "Weight-free proof of Proposition 5.1 by heights; cancellation as an incidence determinant; tree matchings are partnered Hamiltonian cycles; at least 2 cmin tree matchings (route-combinatorics, under review)", ["p.N.H", "p.K.1", "p.U.5", "p.D.2"])
ev("2026-11-14T10:33:18Z", "proposed", "Conjecture: at least 2^cmin tree matchings (true for all 5088 cases up to 16 vertices)", ["k.D.3"])
ev("2026-11-14T10:33:58Z", "computed", "Brute force over 140358 states: tree matching iff exactly one partner", ["c.R.c"], ["research/2026-11-14_fable_route-combinatorics/data/extra2_v16.txt"])
ev("2026-11-14T10:36:52Z", "refuted", "Hypotheses dropped one at a time: bipartite, 3-connected, sphere, bijective state, positive circulation, partner (limits)", ["x.S0.x1", "x.S0.x2", "x.S0.x3", "x.B.x1", "x.N.x1", "x.R.x1"], ["research/2026-11-14_astra_limits/HYPOTHESES.md"])
ev("2026-11-14T10:36:52Z", "proved", "Rarity family: 3^q states and 2^q tree matchings; recovery is injective with a known image (limits, unreviewed)", ["p.D.5", "p.F.3"])
ev("2026-11-14T10:38:02Z", "proved", "Dictionary between the three papers; 14 shared core nodes; J is an integer by the 3-colouring alone (dependency-graph, unreviewed)", ["p.C.1", "p.C.2", "p.A.d", "p.E2.2"])
ev("2026-11-14T10:38:02Z", "question", "Doors opened by the skeleton: roots off a face, leaf removal, cut-free root, second proofs of the disk identity", ["k.A.2", "k.F.4", "k.G.3", "h.B.1", "h.B.2", "h.B.3"])
ev("2026-11-14T10:39:06Z", "proposed", "Topology route predictions P1 to P10 written before the runs", ["k.B.5", "k.U.5h", "k.TG.h2"], ["research/2026-11-14_opus_route-topology/PREDICTIONS.md"])
ev("2026-11-14T10:47:51Z", "proved", "Quartic Berezin integral, Cauchy-Binet squared-minor formula, parity of avoiding cycles from Thomason (route-algebra, unreviewed)", ["p.K.3", "p.G2.6"])
ev("2026-11-14T10:47:51Z", "refuted", "Nullstellensatz, real stability, positive semidefinite blocks, universal residues, global sign gauge, unrooted invariants", ["x.N.x12", "x.N.x13", "x.N.x11", "x.N.x15", "x.U.x8"])
ev("2026-11-14T10:47:56Z", "computed", "The Lean proof builds locally; axioms propext, Classical.choice, Quot.sound (lean-formalisation)", ["c.G2.c"], ["research/2026-11-14_opus_lean-formalisation/build/"])
ev("2026-11-14T10:48:40Z", "refuted", "Structural shortcuts fail: LP integrality (13 vertices), single-swap descent (50), lattice extremes alone (40, 80), degree-4 induction (route-graph-theory)", ["x.U.x5", "x.N.x14", "x.U.x6"])
ev("2026-11-14T10:48:40Z", "proved", "One exact Euler identity gives the pair criterion in both directions; pairs are alpha-orientations (route-graph-theory, under review)", ["p.A.GT", "p.A.6", "p.G.5"])
ev("2026-11-14T10:48:40Z", "proposed", "Conjectures: lattice min or max carries a tree pair; a non-increasing exchange path exists", ["k.D.7", "k.N.11"])
ev("2026-11-14T10:50:25Z", "literature", "The Lean proof differs from the paper in four places: algebraic dual, H- form, polynomial instead of exp, a flow on G instead of spoke circulations", ["th.S0.4", "th.N.Lean", "th.G.Lean", "th.A.Lean"], ["research/2026-11-14_opus_lean-formalisation/DIFFERENCES.md"])
ev("2026-11-14T10:54:40Z", "reviewed", "astra referee on route-combinatorics: FOLLOWS, with corrections (first-failure sizes 14 and 13 become 12 by reflection; scope of negative conclusions); independent recount to 16 vertices", ["p.N.H", "p.K.1", "p.U.5", "p.D.2", "x.N.x4", "x.N.x5", "x.N.x8"], ["research/2026-11-14_astra_referee-combinatorics/REFEREE.md"])
ev("2026-11-14T10:54:50Z", "reviewed", "fable referee on the determinant claims of route-constructive and route-dimers: all CORRECT, two wording fixes; the two determinants coincide", ["p.N.lin", "p.K.2", "p.ST.4", "p.U.2", "x.N.x9", "x.N.x10"], ["research/2026-11-14_fable_referee-determinants/REFEREE-dimers.md"])
ev("2026-11-14T10:54:50Z", "proved", "Parity of state cycles is enough for three of the four uses of the disk identity; the value 3 is used once (referee-determinants, unreviewed)", ["p.C.5"])
ev("2026-11-14T10:54:50Z", "refuted", "Positivity of the coefficient norm or of the constrained Laplacian terms does not give existence", ["x.U.x7"])
ev("2026-11-14T10:56:00Z", "documented", "Lean report: the formal proof is simpler than the paper in five places; flow weights checked on 71224 rooted triangulations up to 18 vertices", ["c.G2.c", "th.N.Lean", "c.N.c"], ["research/2026-11-14_opus_lean-formalisation/REPORT.md"])
ev("2026-11-14T11:00:00Z", "proved", "Topology: the disk identity as the theorem of turning tangents; cancellation as a Morse matching; last step as Alexander duality; tree matchings and sutured Floer homology (route-topology, unreviewed)", ["p.B.6", "p.K.4", "p.F.6", "p.U.7"], ["research/2026-11-14_opus_route-topology/REPORT.md"])
ev("2026-11-14T11:00:00Z", "refuted", "The partner of a tree matching need not be a tree matching (6 of 442)", ["x.D.x1"])
ev("2026-11-14T11:00:00Z", "proposed", "Conjecture R6': local search from a point-rainbow tree reaches a tree matching (450 of 450 up to 16 vertices)", ["k.U.7h"])
ev("2026-11-14T10:55:00Z", "answered", "Dependency-graph conjecture A2 answered: not every avoiding Hamiltonian cycle comes from a tree matching (prism: 4 against 2); the image is characterised", ["x.A.x1", "p.U.5"])
ev("2026-11-14T10:48:00Z", "computed", "Cross-check for this map: the two independent enumerations agree on all 7868 rooted triangulations up to 16 vertices", ["e.census16"], ["labyrinth/frontier_crosscheck.json"])
ev("2026-11-14T11:05:00Z", "documented", "Route map and labyrinth seeded: 16 waypoints, 17 steps, %d routes" % len(RT.ROUTES), ["m.two-evaluations"], ["digestions/route-map/ROUTE-MAP.md"])
E.sort(key=lambda e: e["ts"])
old = []
pth = LAB / "events.jsonl"
if pth.exists():
    for line in pth.read_text(encoding="utf-8").splitlines():
        if line.strip() and not json.loads(line).get("backfilled"):
            old.append(line)
pth.write_text("\n".join([json.dumps(e) for e in E] + old) + "\n", encoding="ascii")

# ---------------------------------------------------------------- state of the art
G1, G2, G3, G4 = "The theorem and its proofs", "Structure of tree matchings", "Formulas and algorithms", "Verification"


def row(id, group, cls, result, status, kind, refs, lit, previous=()):
    return dict(id=id, group=group, cls=cls, result=result, status=status, kind=kind, refs=refs, lit=lit, updated=DAY,
                previous=[{"date": d, "was": w} for d, w in previous])


S = {"about": "Best known result for each tracked question on 2026-11-14. Edited only through labyrinth/seed.py.",
     "groups": [G1, G2, G3, G4],
     "entries": [
         row("main", G1, "Barnette's conjecture", "Every cubic bipartite 3-connected planar graph has a Hamiltonian cycle avoiding any prescribed edge.",
             "LIT: three 2026 preprints, unrefereed; Lean proof builds locally with standard axioms; three reverse-Lamport audits FOLLOW (AI, unreviewed)",
             "proved", ["th.G2.1", "c.G2.c", "p.G2.4"], ["OpenAI 2026", "Li 2026", "trees paper 2026"],
             [("2022-01-01", "verified by computer up to 90 vertices (Brinkmann-Goedgebeur-McKay)"), ("2025-01-01", "proved for faces of size at most 8 (Schnieders)")]),
         row("prop51", G1, "Shortest rigorous proof of Proposition 5.1 (a pair implies a forest pair)",
             "Two candidates of about one page: heights as test functions with no weights (comb, rewritten by its referee), and one integer polynomial "
             "F with linear weights 1 + xa, real signs and parity only (dim, refd). The Lean proof uses the second form.",
             "proved here (1 independent AI referee each; human check pending)", "proved", ["p.N.H", "p.N.lin", "th.N.Lean"], [],
             [("2026-10-06", "Taylor coefficient of an exponential sum with circulation weights (OpenAI)"),
              ("2026-10-18", "integer polynomial per exchange component; marked walk (trees paper)"),
              ("2026-10-21", "two sign-reversing involutions on marked objects (Li)")]),
         row("pair", G1, "Exact hypothesis for the first pair",
             "A pair exists iff no separating triangle has black inner boundary, iff t0 is on the black side of every separating triangle. "
             "One exact Euler identity proves both directions.",
             "LIT (trees paper Thm 1.2); short proof proved here (gt, under review); computed on all 7868 roots up to 16 vertices", "proved",
             ["th.A.T", "p.A.GT", "c.A.c"], ["trees paper 2026"], [("2026-10-06", "sufficient: no separating triangle (OpenAI Prop. 3.1)")]),
         row("disk", G1, "What the disk identity is used for",
             "Four uses in OpenAI, three in Li. In the real-sign form three uses need only that state cycles are odd; the value 3 is used once.",
             "proved here (refd, unreviewed)", "proved", ["p.C.5", "p.B.0"], [], [("2026-11-14", "four uses of the full identity (dependency-graph audit)")]),
         row("structural", G1, "Existence proof with no signed count", "None. Eight exact reformulations of the target; every relaxation and every local or extremal rule tested is refuted.",
             "open; %d dead ends recorded. Most promising: conjecture k.U.7h (local search from a point-rainbow tree)" % sum(1 for r in RT.ROUTES if r["status"] == "REFUTED"),
             "partial", ["q.structural", "k.U.7h", "x.U.x5", "x.N.x14"], []),
         row("tm-lower", G2, "Lower bound on the number of tree matchings of a rooted triangulation with a pair",
             "At least 2 cmin, and always even. Conjecture: at least 2^cmin (5088 cases, equality in 4609).",
             "2 cmin proved here (1 AI referee; human check pending); 2^cmin conjecture", "proved", ["p.D.2", "k.D.3", "e.census16"], [],
             [("2026-10-18", "at least 2: both signs occur in every exchange component (trees paper Thm 5.2)")]),
         row("rarity", G2, "Fraction of states that are tree matchings", "Can be (2/3)^q on 5q + 3 vertices: 3^q states, 2^q tree matchings.",
             "proved here (lim, under review); computed for q <= 6", "proved", ["p.D.5", "f.rarity"], []),
         row("canonical", G2, "Canonical forest pair", "None known. Highest state, lowest state, one-way minimal cover, largest rank difference, "
             "each lattice extreme alone: all refuted. 'Lattice minimum or maximum' has no joint failure in 180 random instances.",
             "conjecture", "conjecture", ["k.D.7", "x.N.x4", "x.N.x5", "x.N.x6"], []),
         row("which-hc", G2, "Which Hamiltonian cycles arise from tree matchings",
             "Exactly the cycles avoiding e0* whose state has a partner. Recovery is injective, not onto (prism: 2 of 4). 3 #TM <= #HC(G).",
             "proved here (comb: 1 AI referee; lim, gt: under review)", "proved", ["p.U.5", "p.F.3", "x.A.x1"], []),
         row("det", G3, "Determinant formula for Z",
             "Z = i^(-n) [prod y_t] det(sum_t y_t M_t) with rank-two real blocks; 2^n determinant evaluations. Found independently by four agents; "
             "the versions coincide by a gauge through the 3-colouring. No formula without coefficient extraction.",
             "proved here (1 independent AI referee; human check pending)", "proved", ["p.N.lin", "h.N.1", "x.N.x9", "h.N.4"], [],
             [("2026-10-18", "the number of states is |det K_B| (trees paper Lemma 6.1)")]),
         row("algorithm", G3, "Polynomial-time construction of the cycle",
             "None. Deterministic polynomial space and O(poly(N) 3^(N/4)) time; marked walk 2^O(n log n). Uniform sampling of states is polynomial. "
             "The abstract problem without the spoke-graph structure is NP-hard.",
             "LIT bounds (trees paper); NP-hardness proved here modulo a cited theorem (gt, under review)", "partial",
             ["th.N.T2", "p.ST.4", "x.U.x5", "h.D.8"], ["trees paper 2026"]),
         row("frontier", G4, "Verified range of the counts", "All rooted Eulerian triangulations with at most 16 vertices: states, pairs and tree matchings "
             "agree between two independent implementations (7868 roots); a third recount by a referee agrees.",
             "exhaustive (T3; no referee of the comparison itself)", "exhaustive", ["e.census16"], [],
             [("2026-11-14", "77 rooted runs, 55 triangulations up to 14 vertices (route-constructive)")]),
         row("formal", G4, "Formal verification", "The upstream Lean proof builds locally (Lean 4.34.1); axioms propext, Classical.choice, Quot.sound. "
             "It proves the conjecture as usually stated, by a route that differs from the paper in four places. Not formalised: Corollary 7.2, Theorem 2.2.",
             "computed (lean-formalisation, unreviewed)", "computed", ["c.G2.c", "th.G2.2"], [],
             [("2026-10-10", "third-party report of a kernel replay (cert-machine), not reproduced here")]),
         row("review", G4, "Review state of the proofs written in this project",
             "AI-refereed: route-combinatorics (FOLLOWS with corrections), determinant claims of route-constructive and route-dimers (CORRECT). "
             "Under review: route-graph-theory, limits. Unreviewed: dependency-graph, machinery-literature, route-algebra, route-topology, "
             "lean-formalisation, the referees' own additions. "
             "Human-checked: none.", "partial", "partial", ["q.human"], []),
         row("hypotheses", G4, "Which hypotheses are needed", "Each one, with a witness: K4 (bipartite), theta of cubes on 26 vertices (3-connected), "
             "triangular bipyramid radial graph (cubic), 3 x 3 torus (sphere).",
             "proved here and computed (lim, under review)", "proved", ["x.S0.x1", "x.S0.x2", "x.S0.x3"], []),
     ]}
for e in S["entries"]:
    for ref in e["refs"]:
        assert ref in IDS, (e["id"], ref)
(LAB / "sota.json").write_text(json.dumps(S, indent=1), encoding="ascii")
from collections import Counter
print(sorted(Counter(n["id"].split(".")[0] for n in nodes).items()))
print(len(nodes), "nodes,", len(E), "backfilled events,", len(old), "live events kept,", len(S["entries"]), "state-of-the-art rows")
