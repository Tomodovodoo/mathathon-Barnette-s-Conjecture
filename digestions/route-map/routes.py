"""Single source of the route map.

WAYPOINTS  the mathematical waypoints (nodes of the map)
STEPS      the arguments that join them (edges of the map)
ROUTES     every known way to cross a step: published, proved in this project,
           computed, conjectured, a hunch, or refuted

build_map.py renders route-map.{pdf,svg,png,dot}, routes.json and ROUTE-MAP.md from this file.
labyrinth/seed.py turns the same data into nodes of the knowledge graph.

Status vocabulary (research/BRIEF.md):
  LIT          published or in one of the three papers (the 2026 papers are unrefereed preprints)
  PROVED-HERE  full proof written in an agent folder; review state given in `review`
  COMPUTED     script and range given in `where`
  CONJECTURE   has a stated test
  HUNCH        a direction, not a claim
  REFUTED      kept with its lesson and smallest known counterexample

Sources: O = papers/OpenAI-Barnette.pdf, L = papers/A-Note-On-Barnette.pdf (Zhentao Li),
T = papers/barnette_trees.pdf, Lean = the formal proof in OpenAI's repository as analysed in the
lean-formalisation folder, lit = older literature. Folder tags are expanded in FOLDERS.
"""

FOLDERS = {
    "dep": "research/2026-11-14_fable_dependency-graph",
    "comb": "research/2026-11-14_fable_route-combinatorics",
    "dim": "research/2026-11-14_astra_route-dimers",
    "con": "research/2026-11-14_sol_route-constructive",
    "mach": "research/2026-11-14_sol_machinery-literature",
    "hist": "research/2026-11-14_opus_history-literature",
    "alg": "research/2026-11-14_sol_route-algebra",
    "lim": "research/2026-11-14_astra_limits",
    "expo": "research/2026-11-14_astra_exposition-method",
    "topo": "research/2026-11-14_opus_route-topology",
    "gt": "research/2026-11-14_opus_route-graph-theory",
    "lean": "research/2026-11-14_opus_lean-formalisation",
    "refc": "research/2026-11-14_astra_referee-combinatorics",
    "refd": "research/2026-11-14_fable_referee-determinants",
    "map": "research/2026-11-14_fable_labyrinth-map",
}

# Review state of each folder's PROVED-HERE claims on 2026-11-14 (a referee raises this, never the tier).
REVIEW = {
    "dep": {"state": "unreviewed"},
    "comb": {"state": "under-review", "by": ["research/2026-11-14_astra_referee-combinatorics"],
             "verdict": "pending; work log says the route appears sound, normalisation and scope of the "
                        "negative conclusions need corrections", "date": "2026-11-14"},
    "dim": {"state": "under-review", "by": ["research/2026-11-14_fable_referee-determinants"],
            "verdict": "pending; referee code passes on 1246 rooted instances, no report yet", "date": "2026-11-14"},
    "con": {"state": "under-review", "by": ["research/2026-11-14_fable_referee-determinants"],
            "verdict": "pending; referee code passes on 1246 rooted instances, no report yet", "date": "2026-11-14"},
    "mach": {"state": "unreviewed"},
    "alg": {"state": "unreviewed"},
    "lim": {"state": "unreviewed"},
    "expo": {"state": "unreviewed"},
    "hist": {"state": "unreviewed"},
    "topo": {"state": "unreviewed"},
    "gt": {"state": "unreviewed"},
    "map": {"state": "unreviewed"},
}

# ------------------------------------------------------------------ waypoints
WAYPOINTS = [
    dict(id="G", name="Barnette graph G",
         what="Cubic, bipartite, 3-connected, planar. The claim is that G has a Hamiltonian cycle, "
              "and more: one that avoids any prescribed edge."),
    dict(id="T", name="Dual Eulerian triangulation (T, t0, e0)",
         what="T = G* is a simple sphere triangulation with faces coloured black and white. "
              "Root it at a black face t0 with an edge e0. Vertices of G are faces of T, faces of G are vertices of T."),
    dict(id="2T", name="Two induced trees",
         what="The goal in dual form. G has a Hamiltonian cycle avoiding e0* if and only if V(T) splits "
              "into two sets, each inducing a tree, with both ends of e0 in one of them (Stein 1971; APSW 2016)."),
    dict(id="S", name="States",
         what="A state is a bijection s from the bounded black faces A to the non-root vertices X with s(t) a corner of t. "
              "It is a perfect matching of the incidence graph B. |A| = |X| = n."),
    dict(id="P", name="A pair (r, s)",
         what="Two states that differ at every face. The partner r is the certificate that orients Q_s: "
              "the edge opposite s(t) in t is directed out of r(t)."),
    dict(id="DI", name="Disk identity",
         what="A directed cycle of state edges of length h with l black faces of its disk along it has 2l - h = -3. "
              "Equivalently its disk holds exactly one more white face than black faces."),
    dict(id="M", name="Signed measure on pairs",
         what="Every pair gets a sign (i^J in O, (-1)^cw in L, epsilon in T). Reversing a cycle of D(r, s) flips it, "
              "and reversing a cycle of Q_s flips it. The whole proof is one signed sum over pairs, weighted by a function of s."),
    dict(id="K", name="Cancellation of cyclic Q_s",
         what="Sum with s fixed. If Q_s has a cycle, reversing it changes r, keeps s and the weight, and flips the sign. "
              "So only pairs with Q_s a forest survive."),
    dict(id="N", name="Nonvanishing",
         what="Sum with the undirected cycle set D fixed. With weights whose circulation is positive on every "
              "counterclockwise spoke cycle, the lowest-order term is a positive count of the covers with fewest cycles."),
    dict(id="FP", name="Good pair / good state",
         what="A pair with Q_s a forest. Equivalently a state s with H - s a spanning tree of the spoke graph. "
              "Equivalently a state with exactly one partner."),
    dict(id="IT", name="Incidence tree H - s",
         what="Delete the n matched spokes from the spoke graph H. What is left is a spanning tree: "
              "every black centre keeps two spokes, t0 keeps three."),
    dict(id="WT", name="White-face tree",
         what="The duals of the n deleted spokes form a spanning tree on the white faces (tree-cotree duality in the plane)."),
    dict(id="SE", name="Selection P",
         what="Root the white tree at y0, the white face across e0. Each tree edge selects one side of its black face. "
              "With e0 this is one edge in every face of T, a perfect matching of G."),
    dict(id="JC", name="Jordan curve",
         what="E(G) - P is 2-regular. It is a single cycle, hence a Jordan curve on the sphere, "
              "and its two sides are the two induced trees."),
    dict(id="GL", name="Gluing",
         what="If a separating triangle blocks the state method at this root, cut along it, cap both sides, "
              "solve each with the cap edge prescribed, and glue."),
    dict(id="HC", name="Hamiltonian cycle",
         what="Every Barnette graph has a Hamiltonian cycle avoiding any prescribed edge (O Theorem 1.1, Corollary 7.1)."),
]

# ------------------------------------------------------------------ steps
# verdict: 'forced' = every published proof uses the same argument here (up to translation),
#          'free'   = the published proofs differ in substance,
#          'rigid'  = one argument and no reason seen to look for another.
STEPS = [
    dict(id="S0", frm=["G"], to="T", title="Dualise and root", verdict="forced",
         must="3-connected cubic plane graphs are the duals of simple triangulations, and bipartite means the faces of T "
              "2-colour. This is the only place 3-connectivity is used.",
         freedom="No freedom in the statement. Li keeps the primal language through the auxiliary graph aux(G); "
                 "the objects are the same."),
    dict(id="TG", frm=["T"], to="2T", title="Restate the goal", verdict="forced",
         must="A Hamiltonian cycle of G is a Jordan curve; the faces of G on each side are vertices of T inducing a tree. "
              "Known since Stein. All pre-2026 attacks tried to cross here directly.",
         freedom="This is the edge that 57 years of partial results worked on. None of them reaches all Barnette graphs."),
    dict(id="ST", frm=["T"], to="S", title="Define states and count", verdict="forced",
         must="Euler's formula gives equally many black and white faces k and k + 2 vertices, so |A| = |X| = k - 1. "
              "Without this equality there is nothing to match.",
         freedom="States are Tutte's trinity states with the colours swapped. Their number is a determinant."),
    dict(id="A", frm=["S"], to="P", title="Find two disjoint states", verdict="free",
         must="The incidence graph B must contain two edge-disjoint perfect matchings. This is where a separating "
              "triangle can obstruct, and the only place the papers use 'no separating triangle'.",
         freedom="Four published arguments (flow with a density bound; Ore deficiency with a minimal set; the exact criterion; "
                 "Hall on a gadget in the Lean proof). They prove different amounts."),
    dict(id="B", frm=["T", "S"], to="DI", title="Prove the disk identity", verdict="forced",
         must="Euler's formula on the disk, a signed count of sides, and B = I + l, which holds because a state is a bijection.",
         freedom="One double count in all three papers, on triangles (O, T) or on hexagons of the spoke graph (L). "
                 "A second derivation, as the theorem of turning tangents for an angle structure, is proved in the topology folder and unreviewed."),
    dict(id="C", frm=["P", "DI"], to="M", title="Sign the pairs", verdict="forced",
         must="Define the sign and show that both reversals flip it. The disk identity is used twice here: "
              "on the cycles of D and on the cycle of Q_s.",
         freedom="Three notations for one sign. The complex phase is packaging; a real sign is enough."),
    dict(id="K", frm=["M"], to="K", title="Cancel with s fixed", verdict="forced",
         must="The reversed cycle of Q_s must be chosen from s alone, so that the map is an involution that keeps the weight.",
         freedom="All three papers use the same involution. It is the statement that a twisted incidence determinant of Q_s "
                 "vanishes on a cycle."),
    dict(id="N", frm=["M"], to="N", title="Show the total is not zero", verdict="free",
         must="Weights that depend on s only and separate the two orientations of every D-cycle. "
              "Then group by D and find a term that cannot cancel.",
         freedom="The widest step: five published arguments, two more proved here, and a long list of refuted shortcuts. "
                 "Every route that works still minimises over the number of cycles."),
    dict(id="D", frm=["K", "N"], to="FP", title="Compare the two evaluations", verdict="forced",
         must="The same sum is supported on good pairs (by K) and is not zero (by N). So a good pair exists.",
         freedom="The comparison is one line. No canonical good pair is known: every extremal choice tried is refuted."),
    dict(id="U", frm=["S"], to="FP", title="Unsigned routes (bypass)", verdict="open",
         must="Find a good state with no signed sum: as a prescribed-degree spanning tree, a three-matroid "
              "intersection, a constrained white tree, a point of the state lattice.",
         freedom="Many exact reformulations are proved. None has an existence argument. Every relaxation tried "
                 "drops a constraint and is refuted by a small example."),
    dict(id="R", frm=["FP"], to="IT", title="One root per component", verdict="forced",
         must="The partner gives out-degree one at non-roots and zero at roots, so a tree component of Q_s has exactly one root. "
              "With the three spokes of t0 this makes H - s a spanning tree.",
         freedom="Same count in all three papers. A forest without a partner is not enough."),
    dict(id="E", frm=["IT"], to="WT", title="Tree-cotree duality", verdict="rigid",
         must="The complement of a spanning tree of a plane graph is a spanning tree of the dual.",
         freedom="Rigid as a statement. The Lean proof skips the node: it selects P inside G and never builds the white tree."),
    dict(id="E2", frm=["WT"], to="SE", title="Root at y0 and select", verdict="rigid",
         must="Orient the white tree towards y0; the edge above each white face selects one side of a black face.",
         freedom="Rigid. The three papers select the same set P."),
    dict(id="F", frm=["SE"], to="JC", title="Show P leaves one cycle", verdict="free",
         must="P has one edge in every face of T, so E(G) - P is 2-regular. It must be connected.",
         freedom="Two published arguments. O, T and the Lean proof count against the disk identity (a third use). "
                 "Li uses an innermost cycle and needs neither the disk identity nor the partner."),
    dict(id="J2", frm=["JC"], to="2T", title="Sides of the curve", verdict="forced",
         must="The two sides of the Jordan curve are the two induced trees, and e0 lies in one of them.",
         freedom="Li skips this node and glues Hamiltonian cycles directly."),
    dict(id="G", frm=["JC", "2T"], to="GL", title="Cut at separating triangles", verdict="forced",
         must="The prescribed edge is what lets two solutions agree on the cap. An unbounded prescription would be NP-hard.",
         freedom="Same induction in all three papers, known since Kelmans 1986. The trees paper cuts less often."),
    dict(id="G2", frm=["GL"], to="HC", title="Conclude", verdict="forced",
         must="Induction on the number of vertices, or a minimum counterexample.",
         freedom="None."),
]

# ------------------------------------------------------------------ routes
R = []


def route(id, step, label, status, src, where, text, **kw):
    R.append(dict(id=id, step=step, label=label, status=status, src=src, where=where, text=text, **kw))


# ---- S0 dualise
route("S0.1", "S0", "duality; 3-connectivity gives a simple T", "LIT", "O,T",
      "O proof of Thm 1.1; APSW 2016 Section 1",
      "The dual of a 3-connected cubic plane graph is a simple triangulation; G bipartite iff T Eulerian iff the faces of T "
      "2-colour iff the vertices 3-colour.", arg="duality")
route("S0.2", "S0", "stay in G with aux(G)", "LIT", "L", "L Section 2",
      "Li works in the primal graph with the face/black-vertex incidence graph. aux(G) is T with a centre in every face.",
      arg="duality")
route("S0.3", "S0", "3-connectivity enters only here", "PROVED-HERE", "dep", "dep/audit-openai.md, REPORT.md",
      "In O, 3-connectivity is used once, to exclude loops and parallel edges in the dual. Simplicity is then used in the "
      "flow bound and the gluing.")
route("S0.x1", "S0", "drop bipartite", "REFUTED", "lim", "lim/HYPOTHESES.md; examples/K4.json, Tutte46.json",
      "Without bipartiteness there is no proper face colouring of T, so states are not defined.",
      lesson="Odd degrees obstruct the algebra itself, before any question of Hamiltonicity. Best max-cut colourings of "
             "K4, BBL38 and Tutte's graph leave 2, 7 and 9 monochromatic adjacencies.",
      cex="K4 (4 vertices): the dual has all degrees odd. Tutte's 46-vertex graph is the non-Hamiltonian witness.")
route("S0.x2", "S0", "drop 3-connectivity", "REFUTED", "lim", "lim/HYPOTHESES.md; examples/theta_cube_26.json",
      "A 2-connected cubic bipartite planar graph can be non-Hamiltonian. Its dual has parallel edges.",
      lesson="The proof stops at the pair: the 26-vertex theta of three cubes-minus-an-edge has 8 states and no disjoint pair "
             "at each of its 26 roots. The disk identity itself survives in the multimap.",
      cex="theta of three copies of cube-minus-edge, 26 vertices (minimum by Asano-Saito-Exoo-Harary 1982, abstract only).")
route("S0.x3", "S0", "other surfaces", "REFUTED", "lim", "lim/HYPOTHESES.md; examples/torus_3x3.json",
      "On an orientable surface of genus g, |A| - |X| = 2g, so states with three roots do not exist for g > 0, and the "
      "two-tree target is impossible on the torus by an edge count.",
      lesson="The first obstruction is cardinality. A surface version needs a different state and a different target "
             "(one edge per triangle with connected complementary dual).",
      cex="3 x 3 periodic triangular grid on the torus: no two induced trees, yet the dual has 36 Hamiltonian cycles.")

# ---- TG the goal and the pre-2026 routes
route("TG.1", "TG", "Stein 1971; APSW Lemma 5", "LIT", "lit", "Stein, Pacific J. Math. 37 (1971), Thm 2.2; APSW 2016, Lemma 5",
      "T* is Hamiltonian iff V(T) splits into two induced forests, which for triangulations are two induced trees.",
      arg="jordan")
route("TG.2", "TG", "prescribed edge: O Theorem 2.2", "LIT", "O", "O Thm 2.2; hist/EQUIVALENTS.md 9, 14a",
      "With e0 inside one tree the cycle avoids e0*. This is the H- form of Kelmans and Hertel, equivalent to the conjecture.",
      arg="jordan")
route("TG.3", "TG", "face-size results (Goodey; Schnieders)", "LIT", "lit",
      "Goodey 1975; Feder-Subi 2006; Schnieders 2025 (hist/RESULTS-TABLE.md)",
      "Hamiltonicity when all faces have size at most 6 (Goodey), at most 8 (Schnieders, 339 million computer cases). "
      "Partial: local reductions cannot see 3-connectivity, which becomes necessary at face size 10.", partial=True)
route("TG.4", "TG", "computer search to 90 vertices", "LIT", "lit", "Brinkmann-Goedgebeur-McKay, Math. Comp. 2022",
      "All Barnette graphs up to 90 vertices are Hamiltonian.", partial=True)
route("TG.5", "TG", "trees of faces (Feder-Subi)", "LIT", "lit", "Feder-Subi 2006; Bagheri Gh. et al. 2021",
      "Contract a colour class of faces and look for a quasi spanning tree of faces. Polynomial when the remaining faces "
      "have 2 or 3 sides, NP-complete in general. The closest older relative of the incidence tree.", partial=True)
route("TG.6", "TG", "A-trails, braces, book embeddings", "LIT", "lit", "hist/EQUIVALENTS.md 6, 11, 12",
      "Equivalent formulations in other languages. None supplied an existence mechanism.", partial=True)
route("TG.x1", "TG", "trees from colour classes", "REFUTED", "lit", "APSW 2016 (limitation theorem); hist/WHAT-WAS-HARD.md 5",
      "Build a permeating subtree containing all or none of a colour class of the vertex 3-colouring.",
      lesson="APSW give Eulerian triangulations in which every permeating subtree contains at least k and misses at least k "
             "vertices of every colour class. The trees of the 2026 proofs come from a matching, not from colour classes.",
      cex="APSW 2016, family for every k (not reconstructed here).")
route("TG.x2", "TG", "Grinberg obstruction", "REFUTED", "hist", "hist/WHAT-WAS-HARD.md 2",
      "Use Grinberg's formula with a modulus to decide Hamiltonicity.",
      lesson="A Barnette graph has f_4 = 6 + sum (k/2 - 3) f_k, so at least six faces of weight 2 and the classical modulus "
             "argument cannot apply. PROVED-HERE in the history folder.",
      cex="Any Barnette graph: at least six 4-faces.")
route("TG.h1", "TG", "induced-forest completion", "HUNCH", "mach", "mach/ROUTE-IDEAS.md 18",
      "Start from a large induced forest and exchange vertices until both sides are trees.",
      vivid="Farthest from the pair machinery. The general Albertson-Berman conjecture cannot be an input: 2026 preprints report counterexamples.",
      test="Enumerate maximum induced forests on small Eulerian triangulations and look for a trapped configuration.")
route("TG.h2", "TG", "nodal domains of eigenvectors", "CONJECTURE", "topo", "topo/PREDICTIONS.md P10",
      "Sign patterns of Laplacian eigenvectors of T almost never give two induced trees (predicted below 5 per cent).",
      test="Run over the sample of the topology agent; outcome pending in topo/ROUTES.md.")

# ---- ST states
route("ST.1", "ST", "Euler count |A| = |X|", "LIT", "O,T", "O (2.1); T (2); L omits it",
      "k black faces, k white faces, k + 2 vertices, so n = k - 1 on both sides of B.", arg="euler")
route("ST.2", "ST", "states = trinity states; number = |det K_B|", "LIT", "T,lit",
      "T Lemma 6.1; Hine-Kalman 2018 Thm 4.3, Lemma 4.4 (dim/ROUTES.md)",
      "All states have one permutation sign, so their number is |det K_B|, Tutte's magic number, the number of "
      "arborescences of each of the three trinity graphs.", arg="trinity")
route("ST.3", "ST", "states form a distributive lattice", "LIT", "lit", "Hine-Kalman 2018 (clock theorem); mach/REFORMULATIONS.md 9",
      "Clock moves connect all states. The good states are a subset of this lattice with no known description.",
      arg="trinity")
route("ST.4", "ST", "uniform sampling of states", "PROVED-HERE", "con", "con/ALGORITHMS.md",
      "Because all extensions of a partial matching have one sign, residual determinants count them, and a state can be "
      "sampled uniformly in polynomial time. This does not sample good states.")

# ---- A a pair
route("A.O", "A", "max-flow + planar density bound", "LIT", "O", "O Prop. 3.1, (3.1)-(3.4)",
      "No separating triangle implies the Hall-type condition for two disjoint matchings, by bounding every component of T[U].",
      arg="flow-componentwise")
route("A.L", "A", "Ore deficiency, minimal deficient set", "LIT", "L", "L Lemma 9, Theorem 10 (Ore), Claim 12",
      "A minimal deficient set yields a non-trivial 3-edge cut. The balance |B'| = |F'| needed for Ore is not stated in the note.",
      arg="ore-minimal")
route("A.T", "A", "exact criterion: no black-inner separating triangle", "LIT", "T", "T Thm 1.2 (ii) iff (iii), Section 3",
      "A pair exists if and only if t0 lies on the black side of every separating triangle.", arg="exact")
route("A.c", "A", "criterion checked on all roots to 14 vertices", "COMPUTED", "lim,con",
      "lim/code/campaign.py 14 (1206 roots); con/VERIFICATION.md (77 runs)",
      "Pair existence agrees with absence of a black-inner separating triangle at every root tested.")
route("A.d", "A", "Li's Lemma 9 already gives the black inner boundary", "PROVED-HERE", "dep", "dep/correspondence.md 3.7",
      "For a minimal deficient set all three cut edges have their black end inside, so Li's proof gives (iii) implies (ii) of T Theorem 1.2.")
route("A.1", "A", "induction over local expansions", "HUNCH", "dep", "dep/skeleton.md A1",
      "Grow rooted Eulerian triangulations by vertex splits and show a pair survives each split.",
      vivid="Would replace the flow argument by a local rule.",
      test="For each expansion look for a local map from pairs to pairs; check on all pairs for n <= 15.")
route("A.x1", "A", "every avoiding cycle comes from a good state", "REFUTED", "dep,comb,lim",
      "posed in dep/skeleton.md A2; refuted by comb/ROUTES.md 12 (E8) and lim/examples/prism_recovery.json",
      "If every Hamiltonian cycle avoiding e0* came from a good state, known Hamiltonicity results would give pairs with no flow argument.",
      lesson="The recovery map is injective and not onto. A cycle avoiding e0* always defines a state, and that state is a tree "
             "matching or has no partner at all. Most avoiding cycles are of the second kind (ratio up to 26).",
      cex="Hexagonal prism (dual with 8 vertices): 4 cycles avoid the edge, 2 good states.")
route("A.3", "A", "matroid union", "HUNCH", "dep", "dep/skeleton.md A3",
      "Two disjoint matchings as a basis of a union of transversal matroids.",
      vivid="Expected to reduce to the same deficiency count. Recorded so nobody spends an afternoon on it.",
      test="Write the rank formula and compare with O (3.1).")
route("A.2", "A", "roots not on a common face", "CONJECTURE", "dep", "dep/skeleton.md G2",
      "For every simple 2-coloured triangulation some triple of roots of three colours, not necessarily the corners of a face, "
      "admits two disjoint states.",
      test="On the smallest black-inner example (9 vertices, lim/examples/t9_0.json, outer face 2) enumerate all root triples and count pairs.")
route("A.4", "A", "pair counts depend on the root", "COMPUTED", "lim", "lim/data/roots.json",
      "In plantri graph 12_2 one black root has 9 states, 10 pairs, 8 good states; every other black root has 9, 2, 2.")

# ---- B disk identity
route("B.O", "B", "Euler + side count + bijection, on triangles", "LIT", "O,T", "O Lemma 4.1, (4.1), (4.2); T Lemma 4.1",
      "B + W = 2I + h - 2, 3(B - W) = 2l - h and B = I + l give 2l - h = -3. T adds that the length is odd.", arg="double-count")
route("B.L", "B", "the same count on hexagons of the spoke graph", "LIT", "L", "L Claim 25",
      "t_in = |C|/4 - 3/2 for an alternating cycle of the spoke graph. Same identity with t_in = l (dep/correspondence.md 3.2).",
      arg="double-count")
route("B.0", "B", "reading: W = B + 1, degree -1 of the colouring", "PROVED-HERE", "dep,comb",
      "dep/skeleton.md B0; comb/PROOF.md Section 1",
      "With the vertex 3-colouring c, delta(v, w) = c(w) - c(v) mod 3. The identity says the disk of a directed state cycle "
      "holds one more white face than black faces; the colouring map has degree -1 on it.")
route("B.c", "B", "checked on every enumerated cycle", "COMPUTED", "con,dep,refd",
      "con/VERIFICATION.md (1466 directed cycles); dep/scripts/check_nodes.py; refd/code/results.json",
      "All disk equalities hold on every cycle enumerated, with all outgoing choices for n <= 6.")
route("B.x1", "B", "drop bijectivity", "REFUTED", "lim", "lim/examples/nonbijective_disk.json",
      "Let each black face choose a corner with no injectivity requirement.",
      lesson="With defect d = B - I - l the identity becomes 2l - h = -3 - 3d. The state condition is exactly d = 0. "
             "Every interior vertex must be covered once.",
      cex="9 vertices: a directed 4-cycle with delta-sum 0; vertex 8 is used twice, d = -1.")
route("B.1", "B", "integer lift of Kasteleyn's sign lemma", "HUNCH", "dep", "dep/skeleton.md B1",
      "The faces of the spoke graph are hexagons, 6 = 2 mod 4, which is Kasteleyn's condition. The common sign of all states "
      "uses only the parity part of the disk identity.",
      vivid="The disk identity may be a flatness condition for a Z/4 or complex signing of spokes.",
      test="Derive t_out - t_in = 3 from a flatness condition for such a signing.")
route("B.2", "B", "discrete Morse theory", "HUNCH", "dep", "dep/skeleton.md B2",
      "Read the state as a pairing of black faces with vertices in the disk and compute the degree from the unpaired cells.",
      vivid="B = I + l looks like a cancellation of cells.",
      test="Write the pairing as a discrete vector field and check that one white face is always left over.")
route("B.3", "B", "peel the disk", "HUNCH", "dep", "dep/skeleton.md B3",
      "Remove a boundary vertex with its matched black face and show 2l - h does not change.",
      vivid="An inductive proof with a picture per step.", test="Implement the peeling on enumerated cycles.")
route("B.4", "B", "Grinberg count made rigid by a matching", "HUNCH", "hist", "hist/WHAT-WAS-HARD.md 2",
      "3(B - W) = 2l - h is a Grinberg balance in the dual; the bijection adds B = I + l.",
      vivid="Places the one new lemma next to the oldest tool of the subject.",
      test="State Grinberg's formula for the dual disk and compare term by term.")
route("B.5", "B", "Gauss-Bonnet form for any cycle", "CONJECTURE", "topo", "topo/PREDICTIONS.md P2",
      "For a state s and a simple cycle C avoiding the roots, B - W = 2m - h + 2, with m the boundary vertices whose "
      "matched face lies inside.", test="Outcome pending in topo/ROUTES.md.")

# ---- C sign
route("C.O", "C", "phase i^J", "LIT", "O", "O (5.1), Lemma 5.2",
      "J = (1/3) sum of delta(r(t), s(t)) is an integer; both reversals change J by 2.", arg="sign")
route("C.L", "C", "(-1)^cw from local turns", "LIT", "L", "L Lemmas 16, 17, Claim 26",
      "cw' = #clockwise - #counterclockwise cycles. cw' = -J (dep/correspondence.md 3.1).", arg="sign")
route("C.T", "C", "epsilon = (-1)^((n+J)/2)", "LIT", "T", "T Lemma 4.2, (8)", "A real sign; moves (a) and (b) flip it.", arg="sign")
route("C.1", "C", "the three signs agree up to a constant", "PROVED-HERE", "dep", "dep/correspondence.md 3.1",
      "i^J = i^(-n) epsilon, and Z(x) = i^(-n) times the sum of T's polynomials over exchange components.")
route("C.2", "C", "J is an integer by the 3-colouring alone", "PROVED-HERE", "dep,comb", "dep/skeleton.md B0; comb/PROOF.md 1",
      "3J = sum c(s(t)) - sum c(r(t)) = 0 mod 3 because r and s are bijections. J is clockwise minus counterclockwise cycles of D, "
      "the total colour winding.")
route("C.3", "C", "the sign is a Leibniz sign", "PROVED-HERE", "comb,dim,alg", "comb/PROOF.md 4; dim/PROOF.md 2; alg/PROOF.md 1",
      "After a gauge by the 3-colouring the sign of a pair is the product of the local turns delta, the sign of a term in an "
      "incidence determinant. The real sign is prod_t delta(r(t), s(t)).")
route("C.x1", "C", "sign as a product of two dimer weights", "REFUTED", "mach,con,dim",
      "mach/REFORMULATIONS.md 3; con/ALGORITHMS.md; dim/PROOF.md 6",
      "Write the local phase as alpha(r(t)) beta(s(t)) and get Z as a product of two incidence determinants.",
      lesson="At a face with three non-root corners the two cyclic triple products of the phase have ratio -1, and any "
             "separated weight gives ratio 1. Disjointness of r and s is what stops the sum from being one determinant.",
      cex="One black triangle with three non-root corners.")
route("C.4", "C", "height-function form of J", "HUNCH", "dep", "dep/skeleton.md C2",
      "The Q_s-reversal can change the cycle structure of D completely and J still moves by exactly 2.",
      vivid="Suggests J(r, s) = g(s) - g(r) plus a term local to Q_s, like a dimer height.",
      test="Fit g on the enumerated pairs of the n = 15 and n = 23 examples.")

# ---- K cancellation
route("K.O", "K", "involution: reverse a cycle of Q_s", "LIT", "O,L,T", "O Lemma 5.2; L iota_1; T beta, Prop. 2.1",
      "Cycles of Q_s are directed by r. Reversing one chosen from s alone changes r, keeps the weight and flips the sign. "
      "T classifies all components: the number of partners is 0 or 2^q(s), q(s) the number of cycles of Q_s.", arg="involution")
route("K.1", "K", "twisted incidence determinant of Q_s", "PROVED-HERE", "dep,comb", "dep/skeleton.md C1; comb/PROOF.md Prop. 5",
      "For fixed s the partner sum is kappa det N_s, where N_s is the incidence matrix of Q_s reduced at the roots. "
      "It vanishes exactly when Q_s has a cycle. Lemma 5.2 is 'the rows of an incidence matrix around a cycle are dependent'.")
route("K.2", "K", "support of the multivariate polynomial", "PROVED-HERE", "dim,alg", "dim/PROOF.md 4; alg/PROOF.md 1",
      "With one variable per incidence, F(w) has coefficient +1 or -1 on each good state and 0 on every other state. "
      "So CT F(w)F(1/w) is the number of good states.")
route("K.3", "K", "quartic Berezin integral", "PROVED-HERE", "alg", "alg/PROOF.md 5",
      "F(w) is a two-species Grassmann integral with one quartic term per black face. It has an exact Gaussian decoupling, "
      "with no assured sign.")
route("K.c", "K", "checked on every cyclic second state", "COMPUTED", "con,dep,comb,refd",
      "con/VERIFICATION.md; dep/scripts/check_nodes.py (35 cases); comb/lab/dets.py 12; refd/code/results.json",
      "Every state with a cycle in Q_s has zero signed partner sum; the partner count is 2^q(s) or 0 on 140358 states (comb/lab/extra2.py 16).")
route("K.x1", "K", "choose the cycle using r", "REFUTED", "lim", "lim/HYPOTHESES.md (disk identity and bijectivity)",
      "Let the reversed cycle depend on the partner.",
      lesson="The reversal changes r, so a rule that reads r need not pick the same cycle on the way back. "
             "The choice must be a function of s. No smallest counterexample was searched.",
      cex="none recorded; the argument is a proof that the involution property can fail, not an instance")

# ---- N nonvanishing
route("N.O", "N", "Taylor coefficient of order m", "LIT", "O", "O Lemma 5.3, (5.3)-(5.5)",
      "Unit circulations from dual paths, a slide of edges onto spokes, Z(x) = sum over D of prod (-i e^{xL+} + i e^{xL-}); "
      "the coefficient of x^m is a nonzero multiple of a positive sum.", arg="analytic")
route("N.L", "N", "second involution on marked objects", "LIT", "L", "L Section 4, Defs 14, 20-23, Appendix B",
      "Weights are signed crossings of vertical rays. A sign-reversing involution on lists of m marks; its fixed points share a sign. "
      "For m > 1 three verifications are left to the reader (dep/audit-li.md).", arg="bijective")
route("N.T1", "N", "integer polynomial per exchange component", "LIT", "T", "T Lemma 5.1, Thm 5.2, (11)",
      "Integer weights 0 <= a <= 6n; Z_C(z) = sum eps z^omega has a nonzero coefficient of (z - 1)^m. "
      "Every exchange component contains good pairs of both signs.", arg="polynomial")
route("N.T2", "N", "marked walk (Garsia-Milne)", "LIT", "T", "T Thm 5.3",
      "Alternate the two involutions on tokens; the walk ends at a good pair or restarts with fewer D-cycles. "
      "Never computes m. 2^O(n log n) time.", arg="walk")
route("N.H", "N", "heights as test functions, no weights", "PROVED-HERE", "comb", "comb/PROOF.md Sections 2-3 (Theorem B)",
      "Test the signed measure against a product of m heights at white faces. Pairs with one D form a cube, partners of one s "
      "form a cube, and the product is a m-fold difference that survives only on covers with exactly m cycles.")
route("N.lin", "N", "linear weights 1 + x a", "PROVED-HERE", "dim", "dim/PROOF.md 7",
      "Replace e^{xa} by 1 + xa. The polynomial has degree at most n and the same leading coefficient; on the forest side it is "
      "a signed elementary symmetric moment.")
route("N.id", "N", "spoke weights are a height function", "PROVED-HERE", "comb", "comb/PROOF.md 2.3",
      "omega(s) is the volume under the height of s, and L+(C) - L-(C) is the number of white faces inside C, which is B + 1.")
route("N.c", "N", "leading coefficient checked exactly", "COMPUTED", "con,comb,dim,refd",
      "con/supplemental.py (49 groups); comb/lab/dets.py 12; dim/code/linear.py; refd/code/results.json",
      "The first nonzero coefficient equals the signed sum of products of enclosed face counts on every instance tested.")
route("N.x1", "N", "zero, vertex-only or face-only weights", "REFUTED", "lim,dim,alg",
      "lim/data/zero_weights.json; dim/PROOF.md 6; alg/PROOF.md 1",
      "Use weights alpha_t + beta_v, or none.",
      lesson="Such weights are pure gauge: every state has the same total, and the signed count is 0 = 0. "
             "What is needed is positive circulation on cycles, not positive weights.",
      cex="Cube (octahedron dual, 6 vertices): two pairs with J = +1 and -1, Z = i - i = 0.")
route("N.x2", "N", "parity or mod p count without weights", "REFUTED", "comb,dep,alg",
      "comb/ROUTES.md 8; dep/skeleton.md D3; alg/PROOF.md 2",
      "Show the number of good states is odd, or nonzero mod p.",
      lesson="The number of good states is always even (the two signs balance), and T = P - 2 N_1 mod 4 is compatible with T = 0. "
             "The weighted sum is the refinement that works; the first degree at which anything survives is m.",
      cex="Octahedron: 2 good states, signed count 0.")
route("N.x3", "N", "good pair among the fewest-cycle pairs", "REFUTED", "dep,comb",
      "dep/skeleton.md D2; comb/ROUTES.md 7 (E2d, E3)",
      "Among the pairs with the fewest D-cycles one has Q_s a forest; or every cover D has an orientation that is a good pair.",
      lesson="The leading coefficient is nonzero because of the fewest-cycle covers, but the pairs that survive cancellation can live in "
             "other covers. No proof can work inside one D. A statement that held on 1794 cases failed at the next size.",
      cex="16 vertices, class 158, t0 = (2,7,3): a single 13-cycle whose two orientations both have a triangle in Q_s; "
          "its 12 good states lie in two other covers. Also the octahedron with every face split in four (n = 15).")
route("N.x4", "N", "highest or lowest partnered state", "REFUTED", "comb", "comb/ROUTES.md 4 (E1, E1c)",
      "The top (bottom) partnered state of the lattice is a good state.",
      lesson="For an extreme s every D has all cycles one way, but reversing a cycle of Q_s changes the number of D-cycles by two "
             "and extremality does not forbid it.",
      cex="Highest: 12 vertices, class 6, t0 = (2,7,3). Lowest: 14 vertices, class 21, t0 = (4,10,5).")
route("N.x5", "N", "minimal cover, all cycles one way", "REFUTED", "comb", "comb/ROUTES.md 5 (E2, E2c)",
      "Take D with m cycles and orient all of them counterclockwise (or clockwise).",
      lesson="The leading coefficient sums over all minimal covers and prefers no orientation.",
      cex="Counterclockwise: 12 vertices, class 6, t0 = (2,7,3). Clockwise: 13 vertices, class 6, face 6.")
route("N.x6", "N", "largest rank difference", "REFUTED", "comb", "comb/ROUTES.md 6 (E5)",
      "The pair maximising omega(s) - omega(r) is a good pair.",
      lesson="Maximality forces the cycles of Q_s to be counterclockwise and nothing more.",
      cex="12 vertices, class 6, t0 = (2,7,3).")
route("N.x7", "N", "one cycle always suffices", "REFUTED", "comb", "comb/ROUTES.md 13",
      "m = 1, so a first-order argument is enough.",
      lesson="m reaches 3 without separating triangles (192 of 3374 rooted cases up to 16 vertices). "
             "The degree of the test function cannot be bounded, and Li's Appendix B is needed.",
      cex="9 vertices: octahedron with an octahedron glued into a face, m = 2.")
route("N.x8", "N", "cubes of good states; sign = parity of rank", "REFUTED", "comb", "comb/ROUTES.md 9, 10",
      "Good states split into cubes of dimension m; or eps(s) = (-1)^omega(s) up to a constant.",
      lesson="Z(q)/(q - 1)^m can have mixed signs. The count equals 2^m in 4609 of 5088 cases, which suggested more structure than there is.",
      cex="Cubes: 14 vertices, class 24, face 6, Z = -1 + 2q + q^5 - 2q^6. Sign: fails at 8 vertices.")
route("N.x9", "N", "ordinary determinant, all face variables 1", "REFUTED", "con,dim",
      "con/ALGORITHMS.md, data/exact_determinant.json; dim/IDENTITIES.md",
      "Evaluate det(sum_t M_t) with no coefficient extraction.",
      lesson="Without extraction a black face can supply two transitions and another none; the extra terms can cancel the answer. "
             "Testing only the cube or the octahedron would have hidden this.",
      cex="Hexagonal prism dual (8 vertices): squarefree coefficient 45/64 at z = 5/4, all-one evaluation 0.")
route("N.x10", "N", "allow doubled edges (standard double dimers)", "REFUTED", "dim", "dim/PROOF.md 3; dim/ROUTES.md",
      "Add a diagonal so that r and s may share edges, as in Kenyon's double-dimer determinant.",
      lesson="Nonvanishing becomes too easy: F_lambda(1) = lambda^n times the number of states, which is positive even with no pair. "
             "An SL2 connection does not kill doubled edges.",
      cex="A rooted 9-vertex gluing with 4 states, no pair, doubled value 4.")
route("N.x11", "N", "positive semidefinite blocks", "REFUTED", "alg,comb", "alg/PROOF.md 4; comb/ROUTES.md 3",
      "Find a gauge in which the local matrices M_t are positive semidefinite, then use mixed-discriminant positivity.",
      lesson="Each block is, after multiplication by i, Hermitian of trace zero and rank two, signature (1, 1, 0). "
             "No similarity or congruence changes that. The determinant explains the cancellation and does not replace the planar positivity.",
      cex="Any black face with two or three non-root corners.")
route("N.x12", "N", "Combinatorial Nullstellensatz", "REFUTED", "alg", "alg/PROOF.md 1",
      "Get a nonzero evaluation of F from the coefficient form of Alon's theorem.",
      lesson="Naming a nonzero monomial of F already names a good state. Substituting w = a_t b_v kills F.",
      cex="Any instance: F(a_t b_v) = 0.")
route("N.x13", "N", "real stability of the tree-state polynomial", "REFUTED", "alg", "alg/PROOF.md 3",
      "The unsigned generating polynomial of good states is real stable, like spanning-tree polynomials.",
      lesson="Projecting onto matchings destroys stability.", cex="Cube: abc + def vanishes at a = b = c = e^{i pi/6}, d = e = f = i.")
route("N.1", "N", "mixed determinant with positive curvature", "HUNCH", "dep,mach", "dep/skeleton.md D1; mach/ROUTE-IDEAS.md 1",
      "Z = [prod z_t] det(sum z_t M_t) is n! times a mixed discriminant of rank-two blocks. Prove it nonzero from structural hypotheses.",
      vivid="At a = 1 the matrix is the adjacency matrix of T[X] with a U(1) connection of holonomy i around black and -i around white triangles.",
      test="Compute rank(sum over S of W_t) against |S| on cases with and without pairs; look for a non-diagonal normalisation.")
route("N.2", "N", "2-adic evaluation at z = -1", "HUNCH", "dep", "dep/skeleton.md D3",
      "Choose weights with every L+ - L- odd and evaluate T's polynomial at -1.",
      vivid="A count mod powers of 2 that sees the weights.", test="Check on the examples whether such weights exist and the value is nonzero.")
route("N.3", "N", "cycle popping, random walk", "HUNCH", "dep,con", "dep/skeleton.md D4; con/ALGORITHMS.md (exchange walks)",
      "The two moves pop cycles of Q_s and of D, as in Wilson's algorithm. Show the walk hits a good pair fast.",
      vivid="All 320 random and greedy trials from ten bad starts ended within ten moves (con, COMPUTED, small sample).",
      test="Measure hitting times on exchange components of growing size; look for a potential.")
route("N.4", "N", "Pfaffian gadget for the turn tensor", "HUNCH", "mach,dim", "mach/ROUTE-IDEAS.md 6; dim/ROUTES.md",
      "Replace each black face by a planar matchgate with signature q^delta on distinct ordered corners and zero on equal corners.",
      vivid="Would remove the coefficient extraction and give a polynomial-time evaluation.",
      test="Check the Grassmann-Pluecker identities of the six-value signature with the boundary order fixed.")
route("N.5", "N", "height potential on pairs", "HUNCH", "mach", "mach/ROUTE-IDEAS.md 7",
      "A combination of the two state heights that decreases along some exchange move at every non-good pair.",
      vivid="Would turn existence into descent.", test="Search for a non-tree local minimum of each candidate on small exchange graphs.")
route("N.6", "N", "curved double-dimer connection, Lee-Yang", "HUNCH", "mach", "mach/ROUTE-IDEAS.md 15; mach/REFORMULATIONS.md 8",
      "Realise the loop factor -i e^{xL+} + i e^{xL-} as the trace of a non-flat connection.",
      vivid="Each loop factor is -2i e^{xm} sinh(x Delta/2); zeros lie on the imaginary axis loop by loop.",
      test="Solve the connection equations on two bipyramids and test trace identities on nested loops.")
route("N.7", "N", "LGV after cutting along seams", "HUNCH", "mach", "mach/ROUTE-IDEAS.md 8",
      "Cut the pair diagram into non-intersecting paths and use a Lindstrom-Gessel-Viennot determinant.",
      vivid="A fixed path matrix would make the sum a single determinant.", test="Do the cut on the cube and on the first instance with two D-cycles.")
route("N.8", "N", "abstract valuation theorem", "HUNCH", "mach", "mach/ROUTE-IDEAS.md 17",
      "Axiomatise: a finite signed cycle system, two involutions, a positive circulation.",
      vivid="Would say which planar hypotheses do the work.", test="List the axioms and find the first one that fails on a torus or a disk with four roots.")
route("N.9", "N", "a test function with one sign on all covers", "CONJECTURE", "comb", "comb/REPORT.md, open question 2",
      "There is a test function of s for which every cover contributes with the same sign, so that no minimum over the number of cycles is taken.",
      test="On the 479 cases with more than 2^m good states (comb/data/rows_v16.json), search low-degree polynomials in the heights.")
route("N.10", "N", "flux on a small set of faces", "HUNCH", "dim", "dim/ROUTES.md (economical weights)",
      "Put positive flux only on a set of faces that meets the interior of every feasible D-cycle.",
      vivid="Smaller weights, smaller degrees.", test="Compute minimum hitting sets of cycle interiors on the enumerated instances.")

# ---- D compare; canonical pair
route("D.1", "D", "two evaluations of one sum", "LIT", "O,L,T", "O Prop. 5.1; L Key Lemma 7; T Thm 5.2",
      "Supported on good pairs, and not zero.", arg="double-count")
route("D.2", "D", "at least 2m good states", "PROVED-HERE", "comb", "comb/PROOF.md Corollary 3",
      "The signed measure on good states kills all polynomials of degree below m in the rank, and the two signs are equally frequent.")
route("D.3", "D", "at least 2^m good states", "CONJECTURE", "comb", "comb/ROUTES.md 11; labyrinth/scatter.json",
      "Every rooted triangulation with a pair has at least 2^m good states. True for all 5088 cases up to 16 vertices; equality in 4609.",
      test="Find a rooted triangulation with a pair and fewer than 2^m good states; start at 17 vertices with m = 3.")
route("D.4", "D", "exactly one good state is impossible", "PROVED-HERE", "lim,alg", "lim/HYPOTHESES.md; alg/PROOF.md 2 (after T Thm 5.2)",
      "The signed unweighted sum over good states is zero, so their number is even. The cube has two.")
route("D.5", "D", "good states can be exponentially rare", "PROVED-HERE", "lim", "lim/HYPOTHESES.md (rarity); code/rarity.py q <= 6",
      "Gluing q hexagonal-prism duals into white faces gives 3^q states and 2^q good states.")
route("D.6", "D", "a canonical good pair", "CONJECTURE", "comb", "comb/REPORT.md step 3",
      "Under a bijection from states to trinity arborescences, good states have a tree description that singles one out.",
      test="Write the Hine-Kalman bijection on the 12-vertex class 6 example where every extremal rule fails, and look at the images of its 8 good states.")

# ---- U unsigned bypass
route("U.1", "U", "prescribed-degree spanning tree of H", "PROVED-HERE", "mach", "mach/REFORMULATIONS.md 1, 4",
      "[y^{d*}] det L_H(y) is the number of good states: a positive coefficient of the tree-degree polynomial. "
      "Existence would follow from a support theorem for that polynomial.")
route("U.2", "U", "label-transversal white trees", "PROVED-HERE", "dim,alg", "dim/PROOF.md 5; alg/PROOF.md 3",
      "Good states are the spanning trees of the restricted white-face graph whose edge labels use every t and every v once. "
      "A doubly squarefree coefficient of a Laplacian determinant counts them, by Cauchy-Binet with all terms nonnegative.")
route("U.3", "U", "three-matroid intersection", "PROVED-HERE", "mach", "mach/REFORMULATIONS.md 6",
      "A common independent set of size n in two partition matroids and the graphic matroid of opposite edges with the roots identified.")
route("U.4", "U", "unique partner: |det K_{B-s}| = 1", "PROVED-HERE", "mach", "mach/REFORMULATIONS.md 2 (after T Prop. 2.1)",
      "Zeroing the entries of s in K_B gives a determinant equal to the number of partners up to sign. A good state is a state where it is 1.")
route("U.5", "U", "good states = partnered Hamiltonian cycles", "PROVED-HERE", "comb,lim", "comb/PROOF.md Prop. 7; lim/HYPOTHESES.md",
      "Good states are in bijection with the Hamiltonian cycles avoiding e0* whose state has a partner. So 3 #TM <= #HC(G).")
route("U.6", "U", "rooted functional orientations; two-sided hypertrees", "PROVED-HERE", "mach", "mach/REFORMULATIONS.md 5, 7",
      "Two more exact restatements of the target, as an orientation problem and as a simultaneous hypertree realisation.")
route("U.x1", "U", "matching matroid meets graphic matroid", "REFUTED", "mach,con", "mach/REFORMULATIONS.md 6; con/data/other_candidates.json",
      "Treat the two endpoint constraints as one matroid and use Edmonds' two-matroid intersection.",
      lesson="Matchings are not a matroid (augmentation fails on K_{2,2}). With only the face partition and the white graphic matroid, "
             "the augmenting-path algorithm returns white trees that repeat vertices.",
      cex="Truncated octahedron: eleven spokes repeat non-root 3 at faces 2 and 8, and non-root 4 at faces 4 and 15.")
route("U.x2", "U", "unconstrained white spanning trees", "REFUTED", "dim,con", "dim/ROUTES.md; con/ALGORITHMS.md (wilson_candidate)",
      "Every spanning tree of the white-face graph, or of its restriction to duals of B, gives a good state.",
      lesson="Both label constraints are needed. Rejection sampling accepted 0 of 100 trees on the larger named graphs.",
      cex="Octahedron: 128 white trees, 8 after restricting to duals of B, 2 good states.")
route("U.x3", "U", "trinity arborescences = good states", "REFUTED", "dim", "dim/ROUTES.md (trees and trinity)",
      "The Hine-Kalman bijection carries all states to arborescences; perhaps every arborescence is a good state.",
      lesson="Arborescences count all states. Good states are a proper subset with no known one-colour criterion.",
      cex="Hexagonal prism dual: 3 arborescences in each colour, 2 good states.")
route("U.x4", "U", "Yutsis partition of G", "REFUTED", "mach", "mach/REFORMULATIONS.md 11",
      "Identify the two induced trees with a Yutsis decomposition of the cubic graph.",
      lesson="Different ground sets: the vertices of G against the vertices of T.", cex="definitional")
route("U.1h", "U", "support of the tree-degree polynomial", "HUNCH", "mach,topo", "mach/ROUTE-IDEAS.md 2; topo/PREDICTIONS.md P8, P9",
      "Show the target degree vector d* lies in the support of det L_H(y), from plane incidence inequalities.",
      vivid="An unsigned target: no cancellation to explain. If every lattice point of the degree polytope were realised (P9), convexity would finish.",
      test="Enumerate H-trees on the cube and the hexagonal bipyramid; compare the support with the lattice points of its convex hull.")
route("U.2h", "U", "spanning-tree parity / matroid parity", "HUNCH", "hist,mach", "hist/REPORT.md (leads); mach/ROUTE-IDEAS.md 10",
      "'Each black centre keeps exactly two of its three spokes' looks like the spanning tree parity problem that Feder and Subi solve "
      "in polynomial time for 2- and 3-sided faces.",
      vivid="If it is a matroid parity instance, Lovasz gives a polynomial algorithm, against 3^(N/4).",
      test="Design the gadget for one black centre and two adjacent centres; enumerate feasible parity solutions against partial spoke choices.")
route("U.3h", "U", "planar integrality for the three matroids", "HUNCH", "mach,gt", "mach/ROUTE-IDEAS.md 5; gt/code/exp_lp.py",
      "The natural LP with two partition constraints and graphic rank inequalities may be integral on these planar instances.",
      vivid="Would give existence by LP duality and an algorithm by rounding.",
      test="Enumerate fractional vertices for n <= 7; one fractional vertex refutes full integrality.")
route("U.4h", "U", "Bernardi process, Schnyder woods, blossom trees", "HUNCH", "mach", "mach/ROUTE-IDEAS.md 4, 11, 12, 13",
      "A canonical tree or orientation of the map might produce a good state directly.",
      vivid="Each theory uses three colours and rooted trees on triangulations, as the target does.",
      test="On the octahedron and the hexagonal bipyramid, test every facewise corner rule for bijectivity on X and for the forest condition.")
route("U.5h", "U", "good states inside the state lattice", "CONJECTURE", "topo,mach", "topo/PREDICTIONS.md P6; mach/REFORMULATIONS.md 9",
      "The good states are not an interval of the clock lattice and not always an antichain (predicted).",
      test="Outcome pending in topo/ROUTES.md.")
route("U.6h", "U", "describe partnered Hamiltonian cycles in G alone", "CONJECTURE", "comb", "comb/REPORT.md, open question 3",
      "There is a description, without states, of the Hamiltonian cycles of G avoiding e0* whose state has a partner.",
      test="For the hexagonal prism list the 2 partnered and 2 unpartnered avoiding cycles and compare their face sequences; "
           "then test any candidate rule on the 176726 unpartnered cycles of the survey.")

# ---- R one root per component
route("R.1", "R", "out-degree count", "LIT", "O,L,T", "O Lemma 6.1; L Lemma 8; T (3), Prop. 2.1, Thm 1.2",
      "A tree component with v vertices and a roots has v - a out-edges and v - 1 edges, so a = 1. "
      "T: s is a good state iff it has exactly one partner.", arg="count")
route("R.c", "R", "unique partner checked on 140358 states", "COMPUTED", "comb,con", "comb/lab/extra2.py 16; con/VERIFICATION.md",
      "Brute force over all states: good state iff exactly one partner; the partner count is 2^q(s) or 0.")
route("R.x1", "R", "a good state is enough", "REFUTED", "lim,dep", "lim/HYPOTHESES.md (forest versus rooted forest); dep/correspondence.md 3.5",
      "Call s good as soon as Q_s is acyclic, with no partner assumed.",
      lesson="Without the partner the out-degree count is unavailable: a component can hold two roots and another none. "
             "'Forest', 'cycle-breaking' and 'good state' agree for pairs and differ for single states.",
      cex="Hexagonal prism dual: all 3 states have acyclic Q_s, only 2 are good states.")

# ---- E, E2
route("E.1", "E", "tree-cotree duality", "LIT", "O,L,T", "O Lemma 2.1; L Cor. 27; T 7.1",
      "The duals of the deleted spokes form a spanning tree on the white faces.", arg="duality")
route("E.2", "E", "Temperley / Kenyon-Propp-Wilson", "HUNCH", "dep,dim", "dep/skeleton.md E2; dim/ROUTES.md",
      "Read the step as the tree-to-matching bijection of KPW.",
      vivid="KPW applied to the white graph encodes all its spanning trees and carries the label constraints along; "
            "it does not identify those dimers with B (dim).",
      test="Write the bijection for the octahedron and the n = 15 example.")
route("E2.1", "E2", "orient towards y0", "LIT", "O,L,T", "O 6.1; L Claim 31; T 7.1",
      "Each tree edge is assigned to its end farther from y0 and selects the side of its black face bordering that end.", arg="rooting")
route("E2.2", "E2", "the three papers select the same P", "PROVED-HERE", "dep", "dep/correspondence.md 3.6",
      "Li's trace of the dual tree through black vertices gives the same set of edges of G.")

# ---- F one cycle
route("F.OT", "F", "P is a forest, by the disk identity", "LIT", "O,T", "O Lemma 6.2; T Lemma 7.1",
      "A cycle in P0 would be directed, and the selected-side count gives a disk with one black face fewer than the state requires. "
      "Then duality gives the cycle and the Jordan curve the two induced trees.", arg="disk-count")
route("F.L", "F", "innermost cycle, no disk identity", "LIT", "L", "L Lemma 30",
      "If the complement had two cycles, an innermost one with no root face inside bounds a tree of faces, each with an out-step; "
      "some step is undone and two faces sit on one black vertex.", arg="innermost")
route("F.1", "F", "W - B = 1 against W - B = 3", "PROVED-HERE", "comb", "comb/PROOF.md Section 5",
      "The disk-identity argument restated as two incompatible counts of white minus black faces.")
route("F.2", "F", "forest certificate implies Hamiltonian cycle", "PROVED-HERE", "expo", "expo/DEPENDENCY-AUDIT.md",
      "Conditional conversion: a spanning forest selecting one side per face has a complementary dual that is a Hamiltonian cycle.")
route("F.3", "F", "recovery is injective, with known image", "PROVED-HERE", "lim,comb", "lim/HYPOTHESES.md; comb/PROOF.md Section 6",
      "For fixed t0 and e0 the map from good states to cycles is injective. Its image is the set of avoiding cycles whose state is a good state.")
route("F.c", "F", "recovery checked on every good state", "COMPUTED", "con,lim", "con/VERIFICATION.md (744 recoveries); lim/code/campaign.py 14 (3618 certificates)",
      "Every selected P is a two-component forest and both sides induce trees.")
route("F.4", "F", "remove a leaf of the white tree", "CONJECTURE", "dep", "dep/skeleton.md F1",
      "Removing a leaf of the white tree with the black face whose spoke it crosses leaves a rooted triangulation with a good state, "
      "and the cycle of the larger graph is a local detour.",
      test="Implement leaf removal on the trees produced by dep/scripts/check_nodes.py and check validity of the smaller object.")
route("F.5", "F", "a potential along the selected out-edges", "HUNCH", "dep", "dep/skeleton.md F2",
      "Follow selected out-edges from a vertex to a root; a quantity that decreases along the walk proves connectivity.",
      vivid="A third proof of the last step, perhaps the shortest.", test="Compute the change of white-tree depth along each selected out-edge.")

# ---- J2
route("J2.1", "J2", "Jordan curve theorem and Euler count", "LIT", "O,T,lit", "O end of 6.2; T Lemma 7.1; APSW Lemma 5",
      "Each side of the cycle induces a connected acyclic subgraph of T.", arg="jordan")
route("J2.2", "J2", "Li does not need the trees", "LIT", "L", "L Section 5", "Li goes from P to the Hamiltonian cycle and glues cycles.", arg="skip")

# ---- G gluing
route("G.O", "G", "induction with a prescribed cap edge", "LIT", "O,L", "O Section 7; L Appendix C",
      "Cut at a separating triangle, cap, solve one side, prescribe the same-label edge on the other, glue. "
      "O inducts on Theorem 2.2, L takes a minimum counterexample.", arg="glue")
route("G.T", "G", "cut only at black-inner triangles", "LIT", "T", "T 7.3", "The exact criterion says when a cut is needed.", arg="glue")
route("G.K", "G", "Kelmans' reduction (1986)", "LIT", "lit", "Kelmans 1986/1994 via APSW 2016 Thm 8; Hertel 2005",
      "The reduction to cyclically 4-edge-connected graphs with an (x+ y+) or avoided-edge hypothesis was known. O re-proves it without citing it for this step.",
      arg="glue")
route("G.1", "G", "every separating triangle has one black side", "PROVED-HERE", "dep", "dep/audit-trees.md T-F1; dep/skeleton.md G1",
      "The state method needs no cut exactly when t0 is on the black side of every separating triangle. "
      "Changing the root or swapping colours can avoid cuts, not always.")
route("G.2", "G", "the gluing needs the same-label edge", "PROVED-HERE", "lim", "lim/HYPOTHESES.md (separating triangles)",
      "Trees of the two pieces meet in one vertex or one edge; prescribing the cap edge supplies the agreement. The smallest separating example has 9 vertices.")
route("G.x1", "G", "prescribe whatever each cut needs", "REFUTED", "lit", "Bagheri Gh. et al. 2022, proof of Thm 4.6; hist/WHAT-WAS-HARD.md 6",
      "Strengthen the induction hypothesis to an arbitrary set of prescribed edges.",
      lesson="Hamiltonicity through an arbitrary prescribed edge set is NP-complete for Barnette graphs. The hypothesis must prescribe "
             "something bounded: one avoided edge.", cex="reduction from Akiyama-Nishizeki-Saito instances")
route("G.3", "G", "a cut-free root", "CONJECTURE", "dep", "dep/skeleton.md G1",
      "Count how often some root (black face on the black side of all separating triangles, or the same with colours swapped) exists.",
      test="Over generated Barnette graphs with several separating triangles, compute the fraction with a cut-free root; "
           "three triangles with alternating black sides should give the first failure.")
route("G.4", "G", "boundary transfer algebra", "HUNCH", "mach", "mach/ROUTE-IDEAS.md 14",
      "Give a separating triangle a finite boundary state space and write gluing as a contraction.",
      vivid="Dynamic programming over a decomposition; an explanation of why one prescribed edge is enough.",
      test="Enumerate boundary labelings and forest-connectivity types on both sides of one triangle and write the composition table.")
route("G2.1", "G2", "Theorem 1.1 and Corollary 7.1", "LIT", "O,L,T", "O Thm 1.1, Cor. 7.1; L Thm 3; T Thm 1.1",
      "Every Barnette graph has a Hamiltonian cycle avoiding any prescribed edge.", arg="induction")
route("G2.2", "G2", "Lean formalisation upstream", "LIT", "lit,lean,hist", "hist/REPORT.md; lean/graph/",
      "OpenAI's repository holds 31 Lean files (8936 lines, no sorry or axiom by grep). A third party reports a kernel replay. "
      "Nobody in this project has rebuilt it.", arg="formal")
route("G2.3", "G2", "consequences: P4 for Pfaffian braces", "LIT", "O", "O Cor. 7.2 via Gorsky-Steiner-Wiederrecht Thm 4.16",
      "The auditor could not open the cited theorem; the corollary is indeterminate in dep/audit-openai.md.", arg="corollary")
route("G2.4", "G2", "all three proofs close", "PROVED-HERE", "dep", "dep/REPORT.md (verdicts)",
      "Reverse-Lamport audits: O and T follow as written; L follows once four routine unwritten steps are supplied.")
route("G2.5", "G2", "ordered pairs of edges (global H+-)", "CONJECTURE", "hist", "hist/REPORT.md (still open)",
      "Some Hamiltonian cycle contains x and avoids y for any two edges. Not implied by the theorem.",
      test="lim/data/strengthenings.json searched every edge pair on the small corpus; extend the search or find a counterexample across a 3-edge cut.")
route("G2.6", "G2", "an even number of avoiding cycles", "PROVED-HERE", "alg", "alg/PROOF.md 2 (from Thomason 1978, Cor. 1.5)",
      "Every cubic bipartite graph has an even number of Hamiltonian cycles avoiding each edge.")


# ------------------------------------------------------------------ second pass
# Folded in from the reports that arrived after 10:45 UTC on 2026-11-14: the two referee reports
# (refc, refd), route-graph-theory (gt), route-algebra (alg), limits (lim) and the Lean rebuild (lean).
FOLDERS["refs"] = "research/2026-11-14_sol_referee-structure"
REVIEW["comb"] = {"state": "refereed", "by": ["research/2026-11-14_astra_referee-combinatorics"],
                  "verdict": "FOLLOWS, with corrections to domain, normalisation and the scope of the negative "
                             "conclusions (REFEREE.md); human check pending", "date": "2026-11-14"}
for _f in ("dim", "con"):
    REVIEW[_f] = {"state": "refereed", "by": ["research/2026-11-14_fable_referee-determinants"],
                  "verdict": "every refereed claim CORRECT, two wording fixes (REFEREE-constructive.md, REFEREE-dimers.md); "
                             "li.py, the marked walk, the exchange walks and the trinity cofactors were not refereed; "
                             "human check pending", "date": "2026-11-14"}
for _f in ("gt", "lim"):
    REVIEW[_f] = {"state": "under-review", "by": ["research/2026-11-14_sol_referee-structure"],
                  "verdict": "pending (audit started 10:50 UTC)", "date": "2026-11-14"}
for _f in ("refc", "refd", "lean", "refs"):
    REVIEW[_f] = {"state": "unreviewed"}


def _upd(id, **kw):
    for r in R:
        if r["id"] == id:
            for k, v in kw.items():
                r[k] = (r[k] + v[1:]) if isinstance(v, str) and v.startswith("+") else v
            return
    raise KeyError(id)


# corrections from the combinatorics referee
_upd("N.x4", cex="12 vertices, class 6, t0 = (2,7,3) for the highest state, and its mirror image for the lowest "
                 "(the referee's correction: the author's enumeration identified reflections and reported 14).",
     where="+; refc/REFEREE.md; gt/ROUTES.md O1 (extremes of the whole matching lattice fail at 10 vertices)")
_upd("N.x5", cex="12 vertices, class 6, t0 = (2,7,3) for counterclockwise, and its mirror image for clockwise "
                 "(referee's correction; the author reported 13).", where="+; refc/REFEREE.md")
_upd("N.x3", lesson="Reversals inside one fixed cover cannot be guaranteed to reach a good pair, so a proof must move "
                    "between covers. The leading coefficient is nonzero because of the fewest-cycle covers, but the surviving pairs "
                    "can live in other covers. A statement that held on 1794 cases failed at the next size. (Scope as corrected by the referee.)",
     where="+; refc/REFEREE.md; gt/ROUTES.md O3 (a 40-vertex one-cycle cover with no good pair)", src="dep,comb,gt")
_upd("N.x7", lesson="m reaches 3 without separating triangles (192 of 3374 rooted cases up to 16 vertices) and 4 with them. "
                    "A first-order argument is not enough and Li's Appendix B is needed. Unboundedness of m is not proved.")
_upd("N.x8", lesson="Z(q)/(q - 1)^m can have mixed signs, which refutes a rank-compatible signed cube decomposition. "
                    "An abstract partition into cubes of dimension m is refuted by cardinality (referee).",
     cex="Signs: 14 vertices, class 24, face 6, Z = -1 + 2q + q^5 - 2q^6. Cardinality: a 13-vertex instance with 6 good states "
         "and m = 2 (refc/code/cube_cardinality.json). Sign = parity of rank fails at 8 vertices.", src="comb,refc")
_upd("N.x2", where="+; alg/TABLES.md (residues mod 2, 3, 4, 5, 7, 11)",
     lesson="+ No modulus among 2, 3, 4, 5, 7, 11 gives a universally nonzero residue; the positive counts seen are 2, 4, 6, 8, 10, 12, 14, 16, 22.")
_upd("N.H", src="comb,refc", where="+; refc/REWRITTEN-PROP-5-1.md (self-contained rewrite by the referee)")
_upd("N.lin", src="dim,refd", where="+; refd/SIGNIFICANCE.md Section 2 (full proof with real signs and parity only)",
     text="+ The Lean proof uses the same polynomial (lean/DIFFERENCES.md item 16).")
_upd("U.5", src="comb,lim,gt", where="+; gt/PROOFS.md Thm 7.2 (explicit left inverse; image = partitions with acyclic white parent map)")
_upd("U.3", src="mach,gt", where="+; gt/PROOFS.md Section 1",
     text="+ Duality maps the triple to a triple of the same kind, so it never becomes a two-matroid problem (gt).")
_upd("A.c", src="lim,con,gt", where="+; gt (all 7868 rooted instances up to 16 vertices against max-flow)",
     label="criterion checked on all roots to 16 vertices")
_upd("TG.x2", src="hist,gt", where="+; gt/PROOFS.md (Grinberg's identity is automatic for two induced trees)")
_upd("G2.2", label="Lean formalisation (OpenAI repository)", src="lit,lean,hist",
     text="31 Lean files, 8936 lines, importing only Mathlib. The formal statement is the conjecture as usually stated "
          "(lean/DIFFERENCES.md A). Corollary 7.2 and Theorem 2.2 are not formalised.")
_upd("B.c", label="checked on every enumerated cycle", src="con,dep,refd,refc")

# the Lean proof as a fourth published route (lean/DIFFERENCES.md)
route("S0.4", "S0", "algebraic dual from grid minors (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md items 1-6",
      "The formal proof never uses faces or the Jordan curve theorem. A drawn graph is a minor of a grid, the grid has an explicit "
      "algebraic dual, and duality survives deletion and contraction.", arg="algebraic-dual")
route("A.Lean", "A", "Hall's theorem on a gadget; global density bound (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md items 9-11",
      "Max-flow is replaced by Hall's theorem on a doubled incidence graph, and the density bound is proved for all of T[U] at once from a rank inequality.",
      arg="hall-gadget")
route("C.Lean", "C", "raw index sum, phase I^(n/3) (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md item 14",
      "The formal proof never shows J is an integer. It keeps the sum of delta and needs only phase(n +- 6) = -phase(n).", arg="sign")
route("N.Lean", "N", "polynomial prod(1 + aX), weights from one flow on G (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md items 15-18",
      "Z is a polynomial, not an exponential sum, and Lemma 5.3 is replaced by a single flow on G with charge +1 at every white vertex. "
      "Proved for an abstract triangle system with two hypotheses on cycle index sums.", arg="polynomial-flow")
route("R.Lean", "R", "add a sink at the third root (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md item 20",
      "Out-degree at most one and no directed cycle make a forest; no component count.", arg="sink")
route("E.Lean", "E", "the white tree is never built (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md item 19",
      "The formal proof selects P inside G and skips the tree on the white faces.", arg="skip")
route("F.Lean", "F", "cut-balance lemma against the disk identity (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md items 21-22",
      "A directed cycle of selected edges is a state cycle; a cut all of whose edges lie in a perfect matching contradicts |cut| = 2|black cut| + 3. "
      "No induced trees, no Jordan curve.", arg="disk-count")
route("G.Lean", "G", "glue perfect matchings across the 3-cut (Lean)", "LIT", "Lean", "lean/DIFFERENCES.md items 23-25",
      "Strong induction on the H- form: a perfect matching containing e with connected complement. Splitting is contraction.", arg="glue")
route("G2.c", "G2", "the Lean proof builds here; standard axioms only", "COMPUTED", "lean", "lean/build/axioms.out (Lean 4.34.1)",
      "#print axioms gives propext, Classical.choice, Quot.sound. No sorry, admit, axiom or native_decide in the 31 files.")

# graph theory
route("A.GT", "A", "one exact Euler identity, both directions", "PROVED-HERE", "gt", "gt/PROOFS.md Lemma 2.2, Thm 2.1",
      "m - b - (2p - 4) = (1/2) sum over non-face regions of (beta - (d - 4)). Every region contributes at most 0 except a "
      "black-inner separating triangle, which contributes +1.")
route("A.6", "A", "pairs are alpha-orientations (Felsner lattice)", "PROVED-HERE", "gt", "gt/PROOFS.md Lemma 3.1",
      "Pairs up to reversing D-cycles are the alpha-orientations of H - t0 with out-degrees 2, d_x - 2, d_r - 1. They form a distributive lattice.")
route("A.5", "A", "Hall-free shelling construction", "HUNCH", "gt", "gt/ROUTES.md F2",
      "Build a pair by a canonical ordering from t0 inward, as for Schnyder woods.",
      vivid="The certificate of non-existence is always one triangle, which is how density conditions behave when a shelling exists.",
      test="Implement a shelling of the 55 triangulations up to 14 vertices and compare with the flow pairs.")
route("U.x5", "U", "LP relaxation of the three constraints is integral", "REFUTED", "gt,mach", "gt/ROUTES.md M1-M4; posed in mach/ROUTE-IDEAS.md 5",
      "Perfect matchings of B intersected with complements of spanning trees of H form an integral polytope.",
      lesson="Not matroid intersection. No constraint is redundant, good states are not the bases of a matroid, and the abstract problem "
             "(a perfect matching with spanning-tree complement in a planar bipartite graph of maximum degree 3) is NP-hard. "
             "Any min-max must use the hexagonal faces of spoke graphs.",
      cex="13 vertices: a fractional vertex, the average of two non-tree states.")
route("U.x6", "U", "induction by degree-4 expansion", "REFUTED", "gt", "gt/ROUTES.md I1; gt/PROOFS.md",
      "Lift a good state through the expansion of a degree-4 vertex.",
      lesson="States lift bijectively, but the lift of a good state is a good state only under a side condition at the split vertex that is not inherited. "
             "Contraction can create the obstruction.",
      cex="Contraction creates a black-inner triangle from 11 vertices on; 708 of 1516 good states do not lift.")
route("U.x7", "U", "positivity of the norm or of the Laplacian terms", "REFUTED", "refd,alg", "refd/REPORT.md; alg/PROOF.md 6",
      "CT F(w)F(1/w) and the constrained Laplacian coefficient are sums of nonnegative terms, so they are positive.",
      lesson="Both are positive exactly when F is not zero, and showing that is the paper's argument. The positivity in the proof sits on the D side, these on the s side.",
      cex="Obstructed roots of the double octahedron (9 vertices): 360 restricted white trees, 16 with one spoke per face, no good state.")
route("U.x8", "U", "tree count as an unrooted invariant", "REFUTED", "alg", "alg/REPORT.md; alg/invariants.json",
      "The number of good states equals a fixed evaluation of a Tutte, Penrose, Tait or flow invariant of G.",
      lesson="The count depends on the root.", cex="plantri graph 12_2: 2 or 8 good states depending on the black root, all roots with a pair.")
route("N.x14", "N", "single-swap descent on the number of Q-cycles", "REFUTED", "gt", "gt/ROUTES.md D1, D2",
      "From every pair with a cycle in Q_s some single exchange lowers the number of cycles.",
      lesson="A swap along a Hamiltonian D-cycle exchanges r and s, so it cannot lower the count both ways. Exhaustive data up to 15 vertices had made it look true.",
      cex="50 vertices, 4-connected (gt/code/data/deeptrap_50_1.json); two swaps suffice there.")
route("N.x15", "N", "a global sign gauge on incidences", "REFUTED", "alg", "alg/PROOF.md 2; alg/REPORT.md",
      "Flip signs of incidence variables so that all good states get the same coefficient sign.",
      lesson="A GF(2) inconsistency certificate: six tree states in which every incidence appears an even number of times, three with negative sign.",
      cex="A 13-vertex instance with six good states.")
route("N.11", "N", "non-increasing exchange path to a good pair", "CONJECTURE", "gt", "gt/ROUTES.md D3",
      "From every pair there is a path of exchanges along which the number of Q-cycles never increases and reaches 0. A sign-free form of T Theorem 5.2.",
      test="Search exchange graphs at 20 to 30 vertices for a pair with no non-increasing path; at 80 vertices look for pairs with no decrease within two swaps.")
route("N.12", "N", "Li's marked objects are the e_m coefficient", "CONJECTURE", "refd", "refd/REPORT.md (still open)",
      "Li's objects with m distinct marks are the elementary symmetric reading of the linear-weight coefficient.",
      test="Enumerate Li's objects on an instance with m = 2 and compare the signed count with the coefficient of x^2 in F(1 + xa) for unit marks.")
route("C.5", "C", "parity is enough three times; the value 3 once", "PROVED-HERE", "refd", "refd/SIGNIFICANCE.md",
      "In the real-sign form, reversing a Q_s-cycle or a D-cycle multiplies the sign by (-1)^length. So the cancellation, the forest lemma and the "
      "permutation sign need only that state cycles are odd. The value 3 is needed once, to align the signs of the minimal D groups.")
route("D.7", "D", "extremes of Felsner's lattice of pairs", "CONJECTURE", "gt", "gt/ROUTES.md O4-O6",
      "The face-flip minimum or the face-flip maximum of the lattice of pairs always carries a good pair. Each extreme alone fails (at 40 and at 80 vertices); "
      "they never failed together in 180 random instances.",
      test="Exhaustive census of Eulerian triangulations up to about 24 vertices, where one-cycle covers start to appear.")
route("D.8", "D", "finding a good state is in PPAD", "HUNCH", "gt", "gt/REPORT.md (leads)",
      "Each phase of the marked walk follows a path in a graph of degree at most 2 with alternating signs.",
      vivid="Would place the search problem between polynomial time and the 3^(N/4) enumeration.",
      test="Write one phase of T Theorem 5.3 as an END-OF-LINE instance with polynomial-size circuits for the two involutions.")
route("G.5", "G", "sharp primal hypothesis; gluing at black-inner cuts", "PROVED-HERE", "gt", "gt/PROOFS.md; gt/ROUTES.md G",
      "In G the obstruction is a non-trivial 3-edge cut whose black-ended side avoids b0. Li's cyclic 4-edge-connectivity is sufficient and not sharp: "
      "1714 of 4494 rooted instances with separating triangles still have pairs.")

# the LP hunch of the machinery agent was tested by the graph-theory agent and is now the dead end U.x5
R[:] = [r for r in R if r["id"] != "U.3h"]

# ------------------------------------------------------------------ third pass
# Folded in at 11:10 UTC: route-topology (topo) and the report of lean-formalisation (lean).
route("B.6", "B", "Hopf's Umlaufsatz for a flat angle structure", "PROVED-HERE", "topo", "topo/REPORT.md item 1; topo/ROUTES.md",
      "The state defines a flat signed-angle structure, and a vertex-local identity says turning equals minus colour winding. "
      "The disk identity is then the theorem of turning tangents. Orientation-free form: every chosen-edge disk has W = B + 1.")
route("K.4", "K", "cancellation as a Morse matching", "PROVED-HERE", "topo", "topo/REPORT.md item 2",
      "Pairs are combinatorial vector fields, good pairs are gradient fields, and the cancellation reverses a closed orbit. "
      "The matching is acyclic and its critical cells are the good pairs. Its Euler characteristic Z(1) is always 0, so a graded version is needed.")
route("F.6", "F", "Alexander duality: #cycles = 1 + b1(P)", "PROVED-HERE", "topo", "topo/REPORT.md item 2",
      "The complement of the 2-factor retracts onto P, so the number of cycles is one more than the first Betti number of P.")
route("U.7", "U", "sutured Floer support; point-rainbow white trees", "PROVED-HERE", "topo",
      "topo/REPORT.md item 3 (conditional on T Thm 1.2); COMPUTED on 826 instances up to 16 vertices",
      "A good state exists iff a named spin-c structure is supported in the sutured Floer homology of the special alternating link of G "
      "(Juhasz-Kalman-Rasmussen), iff the white faces have a 'point-rainbow' spanning tree.")
route("U.7h", "U", "local search from a point-rainbow tree", "CONJECTURE", "topo", "topo/REPORT.md item 4 (R6'); 450 of 450 instances up to 16 vertices",
      "Same-colour exchanges from a point-rainbow tree, never increasing the black excess, reach a good state. A proof would be a "
      "cancellation-free local-search proof of the key lemma.",
      test="Measure plateaus and step counts at 18 to 20 vertices (1543 triangulations at 18); look for a potential such as black excess plus a white-tree distance.")
route("D.x1", "D", "the partner of a good state is a good state", "REFUTED", "topo", "topo/REPORT.md item 5",
      "Swapping r and s would then be a free involution on good states and explain why their number is even.",
      lesson="The evenness is a signed cancellation, Z(1) = 0, and not a free involution. Good pairs are not symmetric in r and s.",
      cex="6 failures among 442 good states tested (topo data; smallest instance not recorded here).")
_upd("U.5h", text="Outcome (topo): the good states are neither an interval nor an antichain of the clock lattice, and the top and bottom "
                  "states are often good states. No order-theoretic pattern was found.",
     label="order-theoretic position in the state lattice", test="Decided on the topology agent's sample (166 lattices); a description of the subset is still missing.")
_upd("N.c", src="con,comb,dim,refd,lean", where="+; lean/REPORT.md item 5 (71224 rooted triangulations up to 18 vertices)")
_upd("G2.c", where="lean/REPORT.md item 1; lean/build/axioms.out (Lean 4.34.1, Mathlib d13f23b7)")
_upd("B.5", text="+ The topology agent reports the orientation-free form W = B + 1 as proved (B.6); the status of this exact formula is in topo/ROUTES.md.")

route("U.c", "U", "cycle-to-state map replayed; it is not injective", "COMPUTED", "map",
      "map/spotcheck.py (bipyramids of rim 4, 6, 8, every edge of t0)",
      "Every Hamiltonian cycle avoiding e0* gives a state, and that state is a good state or has no partner. Two cycles can give the same "
      "unpartnered state: on the hexagonal prism 4 avoiding cycles give 3 states, on the rim-8 bipyramid 6 cycles give 4 states.")

# accuracy pass against the sources (11:10 UTC)
_upd("U.x1", cex="Hexagonal prism: 4 of the 6 common bases of the two-matroid relaxation are not states (referee's correction, refd). "
                 "Larger witness: truncated octahedron, eleven spokes repeating non-roots 3 and 4 (con/data/other_candidates.json).",
     src="mach,con,refd", where="+; refd/REFEREE-constructive.md")
_upd("U.x6", cex="Contraction creates a black-inner triangle from 11 vertices on; not every good state lifts (708 of 1516 cases in gt/ROUTES.md I1).")

# ------------------------------------------------------------------ fourth pass
# Folded in at 11:15 UTC: route-categorical (cat).
FOLDERS["cat"] = "research/2026-11-14_fable_route-categorical"
REVIEW["cat"] = {"state": "unreviewed"}
# the boundary-algebra hunch of the machinery agent (G.4) was carried out by the categorical agent: see G.6 and G.x2
R[:] = [r for r in R if r["id"] != "G.4"]
route("G.6", "G", "boundary states of a cut; complete at lengths 3 and 4", "PROVED-HERE", "cat", "cat/PROOF.md Prop. 1, Theorem 3; cat/CATEGORICAL.md",
      "Cut T along a cycle, record a finite boundary state on each side, glue: the number of Hamiltonian cycles is the linear term of a "
      "Temperley-Lieb pairing of two disk vectors. O Theorem 2.2 says every piece with triangular boundary realises all 3 boundary patterns; "
      "for quadrilaterals all 6 patterns allowed by a parity rule occur (conditional on O; one sub-case by a finite computation).")
route("G.x2", "G", "a uniform boundary condition for longer cuts", "REFUTED", "cat", "cat/PROOF.md Prop. 4; cat/EXPERIMENTS.md",
      "Induct along cuts of length 5 or more with a boundary condition that every piece satisfies.",
      lesson="The realised boundary patterns depend on the piece from length 5 on. The prescribed edge is the complete boundary datum of a "
             "triangular cut, and that is why the induction stops at separating triangles.",
      cex="A piece with 9 vertices and a 5-cycle boundary (cat data); checked up to 13 vertices.")
route("A.x2", "A", "two roots instead of a root face", "REFUTED", "cat", "cat/REPORT.md (what failed); cat/CATEGORICAL.md",
      "Root at two vertices not tied to a face; every root pair then has a two-root good state, and it gives a Hamiltonian cycle.",
      lesson="Two roots move the obstruction and do not remove it, and O Lemma 6.2 needs all roots on one side of every selected cycle, "
             "which a root face guarantees. This is what the face root is for.",
      cex="Existence: plantri graph 12_6, 51 of 66 root pairs. Recovery: a two-root good state with no Hamiltonian cycle at 8 vertices.")
route("K.x2", "K", "the two cube structures form a bicomplex", "REFUTED", "cat", "cat/REPORT.md (what failed)",
      "Treat reversal of Q-cycles and reversal of D-cycles as two commuting differentials and read the proof as homology.",
      lesson="The two reversals do not commute. The homological packaging is a restatement and gives no new existence argument.",
      cex="12 of 624 pairs up to 12 vertices.")
route("U.x9", "U", "topological Hall for partial good states", "REFUTED", "cat", "cat/REPORT.md (what failed)",
      "Get a good state from connectivity of the complex of partial good states.",
      lesson="The complex is not connected enough even in the smallest case.", cex="Octahedron: a two-face subcomplex is disconnected.")
route("TG.7", "TG", "acyclic triangle factor of a second trinity K", "PROVED-HERE", "cat", "cat/PROOF.md Prop. 5",
      "Hamiltonian cycles with a root on each side are the acyclic triangle factors of a second trinity K built from T. A symmetric restatement of the goal.")
route("U.8h", "U", "every Hamiltonian cycle from a two-root good state", "CONJECTURE", "cat", "cat/REPORT.md (table); COMPUTED up to 12 vertices",
      "With two roots allowed to vary, the state method sees every Hamiltonian cycle.",
      test="Decide it at 13 to 16 vertices; if it holds, find the modified disk identity for cycles that separate the roots.")
route("D.9", "D", "contraction inequality tau(T) >= tau(T/ac)", "CONJECTURE", "cat", "cat/REPORT.md (table); 948 contractions",
      "Contracting a degree-4 vertex never increases the number of good states. An injection behind it would lift good states along vertex splits.",
      test="Look for a local rule extending a good state across a vertex split on the 948 cases (cat/code/recursion.py contract).")
_upd("D.5", src="lim,cat", where="+; cat/PROOF.md Prop. 6 (states, pairs and good states multiply under insertion into a white face)")
_upd("A.2", text="+ The categorical agent tested the two-root version: the obstruction moves and the recovery lemma fails without a root face (A.x2).")

STEP_NOTES = {
    "E": "The Lean proof skips this node: it selects P inside G without building the white tree.",
    "S0": "The Lean proof replaces the sphere embedding by an algebraic dual obtained from grid minors.",
}

ROUTES = R

STATUS_ORDER = ["LIT", "PROVED-HERE", "COMPUTED", "CONJECTURE", "HUNCH", "REFUTED"]
STATUS_NAME = {
    "LIT": "published (the 2026 papers are unrefereed preprints)",
    "PROVED-HERE": "proved in this project, unrefereed",
    "COMPUTED": "computed",
    "CONJECTURE": "conjecture with a test",
    "HUNCH": "hunch",
    "REFUTED": "refuted",
}

# ------------------------------------------------------------------ kinds of argument
# Every route except the COMPUTED checks, classified by the kind of argument it is. Used for route-kinds.png.
KINDS = [
    ("count", "Euler count, parity"),
    ("matching", "matching theory, flows"),
    ("bijective", "bijection, involution"),
    ("polynomial", "polynomial, moments"),
    ("linear", "determinant, linear algebra"),
    ("matroid", "matroid, polytope"),
    ("order", "order, extremal choice"),
    ("search", "search, walk, sampling"),
    ("topology", "topology"),
    ("induction", "induction, gluing"),
    ("duality", "planar duality"),
]
_KIND_IDS = {
    "count": "S0.x1 TG.x2 ST.1 A.GT B.O B.L B.x1 B.4 C.O C.L C.T C.Lean C.1 C.2 C.5 N.2 N.x2 D.1 D.3 D.4 R.1 R.Lean R.x1 F.OT F.Lean F.1 G2.6",
    "matching": "S0.x2 A.O A.L A.T A.Lean A.d G2.3",
    "bijective": "U.8h A.x1 K.O K.x1 N.L N.12 N.x8 D.6 D.x1 U.5 U.6h U.4h U.x3 E.2 F.3",
    "polynomial": "K.2 N.O N.T1 N.Lean N.H N.lin N.9 N.8 N.10 N.x1 N.x7 N.x12 N.x13 D.2 U.x8",
    "linear": "S0.4 TG.h2 ST.2 B.1 C.3 C.x1 K.1 K.3 N.1 N.4 N.6 N.7 N.x9 N.x10 N.x11 N.x15 U.1 U.2 U.4 U.x7",
    "matroid": "TG.5 A.3 U.3 U.6 U.1h U.2h U.x1 U.x2 U.x5",
    "order": "TG.x1 ST.3 A.6 C.4 N.id N.5 N.x3 N.x4 N.x5 N.x6 D.7 U.5h",
    "search": "TG.4 TG.h1 ST.4 N.T2 N.11 N.3 N.x14 D.8 U.7h F.5",
    "topology": "K.x2 U.x9 S0.x3 TG.1 TG.2 B.0 B.6 B.2 B.5 K.4 U.7 F.L F.6 J2.1",
    "induction": "G.6 G.x2 D.9 TG.3 A.1 A.5 B.3 D.5 U.x6 F.4 G.O G.T G.K G.Lean G.1 G.2 G.5 G.3 G.x1 G2.1 G2.2 G2.4 G2.5",
    "duality": "A.x2 TG.7 S0.1 S0.2 S0.3 TG.6 A.2 U.x4 E.1 E.Lean E2.1 E2.2 F.2 J2.2",
}
KIND_OF = {i: k for k, ids in _KIND_IDS.items() for i in ids.split()}
# Audit integration, 14 November 2026. Source reports remain immutable.
FOLDERS.update(primal='research/2026-11-14_astra_primal-proof', families='research/2026-11-14_sol_counting-families', conjectures='research/2026-11-14_opus_conjectures', older='research/2026-11-14_astra_older-approaches', drafta='paper/draft-A', draftb='paper/draft-B', reft='research/2026-11-14_fable_referee-topology')
for tag in ('primal','families','conjectures','older','drafta','draftb'):
    REVIEW[tag]={'state':'unreviewed'}
REVIEW['topo']={'state':'under-review','by':[FOLDERS['reft']], 'verdict':'Code and outputs exist; no written referee verdict available.'}
_upd('D.7', status='REFUTED', src='gt,conjectures', where='conjectures/PREDICTIONS.md items 1-2',
     text='The claim that one of the two true lattice extremes always carries a good pair is reported refuted. Independent replay is pending.',
     lesson='Single-face terminal orientations need not be lattice extremes; even the true two extremes are reported insufficient. Test distance-one and irreducible replacements.',
     cex='Reported at 18 vertices: 26 rooted instances in two triangulations. Provisional computation, no final report yet.')
_upd('U.3', text='A good state is a common basis of the stated three matroids. The natural triple is irredundant. This does not rule out a different two-matroid encoding or a min-max theorem.')
_upd('U.x5', cex='A half-integral vertex at 13 vertices; minimality not proved. A feasible completion has one tree state and one non-tree state (structure referee INTEGRATION.md).',
     lesson='The natural LP is not integral. This does not exclude all encodings of the special spoke class; the broad hardness result is under polynomial Turing reductions.')
route('G2.primal','G2','primal proof with flows and real signs','PROVED-HERE','primal','proofs/primal/PRIMAL-PROOF.md; proofs/primal/STATUS.md',
      'A full primal route using disk cut counts, linear-weight nonvanishing, recovery and 3-cut gluing. Author audit and finite checks exist; independent review pending.')
route('G2.drafta','G2','draft A: heights proof','PROVED-HERE','drafta','paper/draft-A/barnette.tex; research/2026-11-14_opus_review-draft-A/REFEREE.md',
      'Manuscript route through signed intersection heights. The draft referee reports FOLLOWS with sentence repairs; this entry does not certify that every repair is applied.')
route('G2.draftb','G2','draft B: polynomial proof','PROVED-HERE','draftb','paper/draft-B/',
      'A separate manuscript presentation of the polynomial route. No final independent referee report available at this snapshot.')
route('D.families','D','exact even-prism counts','PROVED-HERE','families','families/FAMILIES.md Section 1',
      'For a prism of order 4j: j states, two good states, m=1 and normalized polynomial z^(j-1)-1. Full proof supplied, independent review pending.',partial=True)
route('D.ext1','D','distance one from a lattice extreme','CONJECTURE','conjectures','conjectures/PREDICTIONS.md item 3',
      'Some element at rank distance at most one from a true extreme carries a good pair.',test='Enumerate true extremes and their rank-one neighbours through 24 vertices.')
route('D.ext2','D','join or meet irreducible pair cover','CONJECTURE','conjectures','conjectures/PREDICTIONS.md item 4',
      'Some join-irreducible or meet-irreducible lattice element carries a good pair.',test='Enumerate irreducibles and all cover orientations through 22 vertices.')
route('TG.older','TG','older approaches: tests in progress','HUNCH','older','older/TESTS.md',
      'Test whether contractions and Pfaffian translations supply the rooted incidence structure needed for nonvanishing.',
      vivid='A classical reduction could transport the missing root data.',test='Replay the named prism, truncated-octahedron and Pfaffian tests when the report is available.')
route('N.li-check','N','Li two-mark involutions on running example','COMPUTED','map','research/2026-11-14_astra_audit-digestions/code/verify.py; outputs/verification.json',
      '213 marked objects; iota1 fixes 141, iota2 fixes 9 of one sign; signed count -9. Closure, involutivity and sign reversal checked exhaustively on this instance.')
KIND_OF.update({'G2.primal':'polynomial','G2.drafta':'polynomial','G2.draftb':'polynomial','D.families':'count','D.ext1':'order','D.ext2':'order','TG.older':'duality','N.li-check':'bijective'})
STATUS_NAME['LIT']='source result; 2026 sources are unrefereed preprints'
# Reports arriving during the audit. Reviews apply to named claims, not whole folders.
for rid in ('B.6','F.6','K.4','U.7'):
    _upd(rid, where='+; reft/REFEREE.md', text='+ Independently AI-refereed in the topology referee report; human checking pending. Apply the referee corrections where relevant.')
_upd('B.6', label='combinatorial Gauss-Bonnet with signed angles', text='+ The proof uses Euler counting, not a smooth turning-tangents theorem. Boundary flatness and exclusion of the outer face are required.')
_upd('K.4', text='+ Correct grading: J = J_ccw - 2 times the number of clockwise Q-cycles. Pair each root with its outer-centre spoke in the Forman reading. Numerical checks of the Boolean levels only reach k <= 1.')
_upd('U.7', text='+ The referee announces a Rado/Euler proof of the point-rainbow criterion in RAINBOW.md, but that file was not yet present when integrated; that new proof was not inspected here.')
route('B.height','B','signed white area is additive','PROVED-HERE','reft','reft/REFEREE.md Section (h)',
      'The referee supplies a winding-number proof of height equals signed white area without separating triangles. This new proof has not itself had a second referee.',partial=True)
route('D.unbounded','D','unbounded m in Goodey chains','PROVED-HERE','older','older/BRIDGES.md; older/REPORT.md',
      'End-rooted chains of k octahedra have k D-components in every pair, while primal faces have size four or six. Separating triangles are allowed. Author proof, not yet independently refereed.',partial=True)
route('TG.parity','TG','BF21 parity equals black-inner obstruction','REFUTED','older','older/BRIDGES.md; older/REPORT.md',
      'Identify the even-interior condition of the older contracted graph with the black-inner separator obstruction.',
      lesson='The two conditions belong to different incidence constructions; the radial tree is not H-s.',cex='Truncated-octahedron contraction, author certificate not yet independently replayed.')
_upd('TG.older', where='older/BRIDGES.md; older/REPORT.md',text='The final report gives a radial/permeating-tree dictionary and rejects a direct identification with H-s. A direct Pfaffian transfer still lacks balanced incidence objects, disk identity and recovery.')
KIND_OF.update({'B.height':'topology','D.unbounded':'induction','TG.parity':'duality'})
for r in R:
    if r['id'] in ('B.6','F.6','K.4','U.7'):
        r['review']={'state':'refereed','by':[FOLDERS['reft']], 'date':'2026-11-14','verdict':'Named claim checked with corrections in REFEREE.md; human check pending. Newly announced RAINBOW.md proof not inspected.'}
_upd('G2.draftb', label='draft B: scalar height moments', where='paper/draft-B/barnette.tex; research/2026-11-14_opus_manuscript-B/REPORT.md', text='A manuscript route entirely in T. It uses the scalar height moment sum epsilon times omega(s)^m and an m-fold finite difference, then recovers via the tree of faces Y_s from Q_s plus two root sides. No plane spoke graph is needed. Author audit exists; final independent review pending.')
# Map refresh, 2026-11-14. Reviews attach to named claims, never promote tiers.
FOLDERS.update(rc='research/2026-11-14_sol_referee-conjectures', covers='research/2026-11-14_astra_cycle-covers', ind='research/2026-11-14_opus_route-induction', ri='research/2026-11-14_fable_induction-completion', prob='research/2026-11-14_sol_route-probabilistic', pf='research/2026-11-14_astra_route-pfaffian', main='paper/main', inv='proofs/involutions', revp='research/2026-11-14_astra_primal-revision')
for tag in ('rc','covers','ind','ri','prob','pf','main','inv','revp'):
    REVIEW[tag]={'state':'unreviewed'}
REVIEW['main']={'state':'under-review','by':['research/2026-11-14_sol_referee-main','research/2026-11-14_fable_coldread-main']}
REVIEW['inv']={'state':'under-review','by':['research/2026-11-14_opus_referee-involutions']}
def checked(rid, by, verdict):
    _upd(rid, review={'state':'refereed','by':[FOLDERS.get(by,by)],'date':'2026-11-14','verdict':verdict+' Human check pending.'})
_upd('D.7', text='C2 is false. Both true lattice extremes can have no good pair. Independent exhaustive minimum-order check finds 26 failures at V=18 and none below.', where='rc/REFEREE.md; rc/data/v18.json; rc/data/census_18.json', cex='V=18, four-element diamond lattice, 54 states, 20 pairs and 12 good states.', lesson='Exact extremes are computable by two shortest paths, but neither must succeed. Greedy facial terminals are not necessarily extremes.')
_upd('D.ext1',status='REFUTED',where='rc/REFEREE.md; rc/data/r1.json', text='R1: success within cover-distance one of an extreme.',cex='Saved V=24 witness has nearest success at distance two; glued V=33 family gives unbounded distance.',lesson='No fixed distance bound works in the general class; separating-triangle-free restriction remains a separate test.')
_upd('D.ext2',status='REFUTED',label='R2: extreme or irreducible',where='rc/LATTICE-READING.md Section 6; rc/data/R2_glued_V33.json',text='A bottom, top, join-irreducible or meet-irreducible element need not carry a good pair.',cex='V=33 rigid-face sum of two V=18 witnesses; lattice B_4, 400 pairs, 144 good pairs, all ten candidates fail. Two implementations agree. No minimum-order claim.',lesson='Success need not occur at lattice boundary elements. This witness has separating triangles and does not settle a separator-free restriction.')
_upd('D.3',where='rc/REFEREE.md; covers/CENSUS.md',text='C1: every feasible root has #TM >= 2^m. Independently replayed on all rooted Eulerian triangulations through V=22; extended evidence on 23,824,742 separator-free facial roots through V=24. Equality iff one cover is also open beyond this range.',test='Prove the two-cover exceptional-overlap exclusion, then extend the overlap calculation to several covers.')
_upd('N.11',where='rc/REFEREE.md; conjectures/REPORT.md',text='C3: from every ordered pair, D-swaps and Q-reversals that never increase the number of Q-cycles reach a good pair. Independent exhaustive reachability through V=16 and on both saved plateau traps; author reports 940 successful starts.',test='Find a potential on plateau components, or search for a closed positive-cycle component at larger orders.')
_upd('D.9',where='ri/MISSING-LEMMA.md; ri/data/census_*.json',text='Contraction inequality #TM(T) >= #TM(T/M), conjectural on the rooted degree-four merge class. Checked on 1,202,792 rooted contractions through V=18. It does not imply that any contracted good state lifts directly.',test='Prove an injection from exceptional to non-exceptional matchings; distinguish direct lift from rotation.')
_upd('U.7h',where='reft/RAINBOW.md; reft/REPORT.md',text='Conjecture X: every point-rainbow tree reaches a good state by exchanges never increasing black excess, allowing plateaus. Exhaustive through V=17; sampled to V=120. Surplus walk alone can cycle.',test='Use both kinds of plateau moves; analyze periodic witnesses at V=38 before proposing another deterministic rule.')
_upd('U.7',text='The topology dictionary was AI-refereed. New Theorem R in reft/RAINBOW.md proves the point-rainbow criterion by Rado plus Euler, independent of signed nonvanishing. That new proof is T2 unreviewed.',where='topo/REPORT.md; reft/REFEREE.md; reft/RAINBOW.md')
_upd('G.6',text='Boundary vectors glue by the Temperley-Lieb pairing. Triangular cuts realise all three patterns conditional on the supplied theorem. For quadrilateral ++-- boundaries, six patterns requires chordlessness; a chorded piece can have five (pf/REPORT.md replay).',where='cat/PROOF.md; pf/REPORT.md')
_upd('G2.primal',where='proofs/primal/STATUS.md; revp/REPORT.md; research/2026-11-14_fable_referee-primal/REFEREE.md',text='Full primal proof, independently AI-refereed before revision; missing local sign calculation and map conventions repaired. Revision disputes referee M4: its phase ratio simplifies to i^n, constant in the circuit count. Revised supplementary claims and this disagreement have author verification only.')
checked('G2.primal','research/2026-11-14_fable_referee-primal','Earlier proof FOLLOWS with repairs; subsequent revision and M4 disagreement are not independently re-refereed.')
route('G2.main','G2','merged dual exposition','PROVED-HERE','main','paper/main/; research/2026-11-14_opus_manuscript-merge/', 'Written dual route uses product of local signs, heights along face paths, and an explicit connectivity lemma inside a selected cycle. Under two AI reader reviews; no final verdict at integration.')
route('G2.inv','G2','complete marked involution exposition','PROVED-HERE','inv','proofs/involutions/; research/2026-11-14_sol_li-completion/', 'Written bijective route through marked objects and two involutions. Under independent AI referee; no final verdict at integration.')
def add(rid,step,label,status,src,where,text,kind,**kw):
    route(rid,step,label,status,src,where,text,**kw); KIND_OF[rid]=kind
add('U.directed','U','linear test of a specified pair','PROVED-HERE','conjectures','rc/LATTICE-READING.md Section 2; rc/REFEREE.md','A pair is a good pair iff its selected centre-exit digraph has no directed cycle. DFS tests a given pair in linear time. Choosing directions for all cycles of a specified factor is unresolved. Exhaustively verified through V=18.','order')
checked('U.directed','rc','Submitted criterion independently proved and checked on every pair through V=18.')
add('N.rank-dead','N','signed sum as base-lattice rank polynomial','REFUTED','rc','rc/LATTICE-READING.md; rc/data/examples.json','Read the pair sum from the ordinary rank polynomial of the factor lattice.','order',cex='Octahedron and hexagonal-prism dual have identical singleton lattice but different signed polynomials; opposite signs already lie above one ideal.',lesson='The orientation cube above each lattice element carries indispensable sign and weight data.')
add('D.unique','D','one cover gives equality in C1','PROVED-HERE','conjectures','rc/REFEREE.md','If there is one factor, Q-cycle reversal would create another factor. All its 2^c orientations are good pairs, and unique partners make their second states distinct. Thus #TM=2^m. Converse open.','bijective'); checked('D.unique','rc','Submitted proof independently closed.')
add('D.covers','D','primal meaning and unbounded m without separators','PROVED-HERE','covers','covers/PROOFS.md; covers/data/family.json','For an admissible edge deletion S, c(D)=components(G-S)-1. Explicit T_j, V=3j+2, has no separating triangle, one cover with j-2 triangles and one pentagon, m=j-1 and #TM=2^(j-1). Author proof and finite checks, unreviewed.','topology')
add('D.cover-census','D','C1 and equality census through dual order 24','COMPUTED','covers','covers/code/README.md; covers/data/census.json','23,824,742 facial roots of 4-connected Eulerian triangulations, V<=24: no C1 or equality-characterization violation. Maximum m=6 at V=23. T4 under review, not an independent certification of the inherited C engine.','order')
add('D.level-dead','D','fixed-cycle-count flip connectivity','REFUTED','covers','covers/data/levels.json; covers/PROOFS.md','Covers with the same c, including minimum-c covers, form a connected flip level.','order',cex='V=18 flip squares with labels 3,1,5,3 and 1,3,3,1; no smaller failure in the separator-free search.',lesson='Do not assume that minimizing c gives a convex or connected lattice level.')
add('D.two-covers','D','two-cover exponential bound','PROVED-HERE','covers','covers/PROOFS.md','Two covers with c1,c2 cycles and j shared component cycles have overlap a either zero or 2^j and TM=2^c1+2^c2-2a. This proves C1 for two covers. Strictness has one unexcluded planar overlap configuration. Unreviewed.','count')
add('U.induction','U','degree-four contraction and rotation','PROVED-HERE','ind','ind/PROOFS.md; ri/REFEREE.md','State splitting, exact lift criterion, local sufficient condition, rotation and partial injection are AI-refereed. One-sided existence lifting is proved in ri/RESIDUAL-CASES.md; this new extension is unreviewed. Full induction has two missing lemmas.','induction'); checked('U.induction','ri','Submitted local propositions correct; one-sided extension is new referee work, unreviewed.')
add('U.G','U','ML1: preserve a pair in some merge','CONJECTURE','ri','ri/MISSING-LEMMA.md','Every separator-free rooted T with V>6 has a non-root degree-four vertex and a simple opposite-neighbour merge with a pair. All 62,416 separator-free facial roots, 8<=V<=19, pass.','induction',test='Use short-cycle obstructions and minimal tight sets in MISSING-LEMMA.md; referee the reduction first.')
add('U.ML2','U','ML2: two-sided existence lifting','CONJECTURE','ri','ri/MISSING-LEMMA.md; ri/RESIDUAL-CASES.md','If both contractions at a non-root degree-four vertex have good states, not all matchings of either contraction are exceptional. One-sided case is proved; all tested cases through V=18 pass.','induction',test='Bound the exceptional fraction by one half, or construct a sign-free injection into non-exceptional matchings.')
add('U.lift-dead','U','some contracted good state lifts directly','REFUTED','ri','ri/data/nolift_18.jsonl; ri/REFEREE.md','If T/M has good states, at least one lifts directly to T.','induction',cex='V=18 graph 309, root (5,0,6), x=11, merge {10,2}; both matchings fail to lift, both rotate. 50 such rooted contractions.',lesson='Direct lifting is stronger than existence lifting. Rotation is essential, and counting inequality does not imply direct lift.')
add('U.rainbow','U','Rado-Euler rainbow tree and unique factor','PROVED-HERE','reft','reft/RAINBOW.md','Theorem R proves rainbow existence exactly at feasible roots. Theorem S completes each rainbow tree to a unique incidence 2-factor. Reversible surplus walks give fixed-point-free involutions on good states. New proofs T2 unreviewed.','matroid')
add('U.walk-dead','U','surplus walk always terminates','REFUTED','reft','reft/RAINBOW.md; reft/data/','The surplus walk alone reaches smaller black excess.','search',cex='Periodic walks at V=38, periods 48 and 68; minimum order unresolved in 17..38.',lesson='Conjecture X needs both plateau moves; a deterministic walk can miss the exit.')
add('U.mean-dead','U','positive full-spoke UST mean fitting','REFUTED','prob','prob/PROOFS.md Sections 1-3','Finite positive weights attain the target degrees on all of H.','probability',cex='Cube: root and outer-centre target degrees are maximal, but every spoke can be absent.',lesson='Condition to the forced-spoke face before fitting means; fractional feasibility still does not round exact joint degrees.')
add('U.support-dead','U','joint Lorentzian rounding','REFUTED','prob','prob/PROOFS.md; prob/code/campaign.py','Joint endpoint degree support inherits M-convexity from the spanning-tree polynomial.','matroid',cex='Six-cycle hand witness; cube spoke graph among 128 spanning trees.',lesson='The joint substitution is bilinear. One-sided Lorentzian closure supplies no joint-degree theorem.')
add('U.packing','U','two white trees in every pair support','CONJECTURE','prob','prob/NEXT-PREDICTION.md; prob/REPORT.md','Every selected pair support partitions into two white spanning trees. 278 nonvacuous rank tests and 27 larger packings through V=120 support it. Packing supplies fractional feasibility, not degree-preserving rounding.','probability',test='Check Nash-Williams rank inequalities by the disk count; consume the dedicated packing report when available.')
add('N.zeros-dead','N','universal analytic root locations','REFUTED','prob','prob/PROOFS.md; prob/code/secondary.py','Signed z-polynomials have unit-circle roots or linear-weight polynomials have only real roots.','probability',cex='V=12 exact factors (z-1)(z^2+3) and x(x+1)(2x+1)(2x^2+5x+4); real-rooted z already fails at V=10.',lesson='Family product factorizations do not establish a universal zero-location argument.')
add('G2.pf','G2','Pfaffian corollary through GSW 4.16','PROVED-HERE','pf','pf/GSW-CHAIN.md','Conditional on the supplied planar theorem, the opened GSW Theorems 4.4, 4.9, 4.12, 1.7 and 4.16 imply Corollary 7.2. One-step trisum gluing uses six path signatures. New inference unreviewed.','induction')
add('N.heawood','N','root-free torus nonvanishing','REFUTED','pf','pf/PROOFS.md; pf/data/results.json; pf/data/verification.json','Transfer spherical signed nonvanishing directly to Heawood on the torus.','topology',cex='Heawood: 24 states, 48 pairs, D seven-cycles, odd Q cycles; every state contribution cancels and polynomial is identically zero.',lesson='Cancellation survives while nonvanishing fails; the spherical disk value is indispensable for this route.')
add('TG.edge','TG','through an edge from avoidance','PROVED-HERE','older','older/BRIDGES.md; older/NOVELTY.md','At an endpoint of a prescribed edge e, avoid either other incident edge. Degree two then forces e. Through-edge Hamiltonicity follows from universal edge avoidance. Unreviewed conditional deduction.','duality')
add('D.tubes','D','separator-free exponential rarity','PROVED-HERE','families','families/FAMILIES.md; families/data/','Width-four nanotubes have S_L=Fib_(2L+3), #TM=2 and m=1. Stationary transfer certificates also cover width six. All-length transfer reasoning is author proved; finite arithmetic and matrices remain unreviewed.','induction')
KIND_OF.update({'G2.main':'polynomial','G2.inv':'bijective'})
KINDS.append(('probability','probability, positive measures'))
# Give lattice attempts their own column instead of hiding them under generic order.
KINDS.append(('lattice','lattice'))
for rid in ('D.7','D.ext1','D.ext2','N.rank-dead','D.level-dead','U.directed'):
    KIND_OF[rid]='lattice'
for step in STEPS:
    if step['id']=='B': step['freedom']='Euler double count in the sources; the signed-angle Gauss-Bonnet derivation is independently AI-refereed with boundary corrections. No human check.'
    if step['id']=='U': step['freedom']='Contraction induction stops at ML1 and ML2; rainbow exchange and two-tree packing remain conjectural at this snapshot. The natural two-matroid and LP shortcuts fail.'

add('D.C1-census','D','independent C1 census through V=22','COMPUTED','rc','rc/code/count.cpp; rc/data/fast_census_summary.json; rc/REFEREE.md','All 9,531,638 facial roots through V=22, 4,656,948 feasible: C1 and equality iff one factor pass. Independent Python and C++ implementations agree through V=18; author and referee totals agree through V=22.','count',tier='T3',review={'state':'refereed','by':[FOLDERS['rc']],'date':'2026-11-14','verdict':'Independent replay of submitted C1 computation; human check pending.'})

for rid in ('A.GT','G.1','G.5','U.5','F.3','D.5','U.3','U.6','U.4'):
    if any(r['id']==rid and r['status']=='PROVED-HERE' for r in R):
        checked(rid,'research/2026-11-14_sol_referee-structure','Named surrounding structural claim checked in INTEGRATION.md; use its corrected scope, not the refuted broad degree-four converse or matroid isomorphism.')
for rid in ('B.6','F.6','K.4','U.7'):
    checked(rid,'reft','Original topology claim checked with corrections; new RAINBOW.md theorems have separate unreviewed entries.')

# Retain all thirteen failed induction schemes, including unreplayed cases.
add('U.ind-R1','U','induction R1: Lift lemma, only-if half (route-graph-theory PROOFS Lemma 6.','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md',"Lift lemma, only-if half (route-graph-theory PROOFS Lemma 6.2(iii)): if the lift s of s' is a TM then s' is a TM R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.",'induction',cex="smallest={'V': 6, 'gid': 0, 't0': 0, 'x': 3, 'merge': '5->0', 'note': 'T/M has a parallel pair'}; smallest_simple={'V': 11, 'gid': 1, 't0': 0, 'x': 5, 'merge': '6->4'}; range=V<=17, 13,210 of 131,336 simple contractions",lesson="splitting v can open a cycle of tau'; s TM iff split(tau')+a v1 is a spanning tree of T-x (PROOFS Prop 2.1)")
add('U.ind-R2','U','induction R2: Degree-4 contraction preserves the existence of a pair','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','Degree-4 contraction preserves the existence of a pair R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest_simple={'V': 11, 'gid': 1, 't0': 0, 'x': 5, 'merge': '6->4'}; range=V<=17, fails in 7,510 of 131,336 simple contractions",lesson='contraction can create a black-inner separating triangle; choose the contraction (conjecture G)')
add('U.ind-R3','U','induction R3: Every TM of T/M lifts to a TM of T','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','Every TM of T/M lifts to a TM of T R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 8, 'gid': 0, 't0': 0, 'x': 4, 'merge': '5->0'}; smallest_root_free={'V': 10, 'gid': 1, 't0': 3, 'x': 8, 'merge': '9->7'}; range=V<=17, fails in 41,873 of 131,336 simple contractions",lesson='the lift condition a in K2 is global; failing TMs must be sent to N-type TMs (rotation rho)')
add('U.ind-R4','U','induction R4: Failing lifts are compensated within the same type (B >= b)','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','Failing lifts are compensated within the same type (B >= b) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 8, 'gid': 0, 't0': 0, 'x': 4, 'merge': '5->0'}; range=V<=17",lesson="compensation comes from the other contraction's type (C >= b holds)")
add('U.ind-R5','U','induction R5: Some TM of T/M satisfies the local condition LC (edge a v in','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','Some TM of T/M satisfies the local condition LC (edge a v in Q) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 10, 'gid': 1, 't0': 3, 'x': 9, 'merge': '2->8'}; range=V<=17, fails in 6,474 of 131,336 simple contractions",lesson='a one-edge local prescription is too strong as an induction hypothesis')
add('U.ind-R6','U','induction R6: rho(lift) is a TM for every failing lift','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','rho(lift) is a TM for every failing lift R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 13, 'gid': 7, 't0': '(0,4,5)', 'x': 10, 'merge': '8->4', 'note': 'x has a root neighbour'}; smallest_root_free={'V': 14, 'gid': 12, 't0': '(5,11,6)', 'x': 2, 'merge': '9->0'}; range=V<=16: 466 of 28,189 failing lifts",lesson="rotation covers 98.3%; the case b in K2' needs a second rule")
add('U.ind-R7','U','induction R7: TM(T) >= 2 TM(T/M)','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','TM(T) >= 2 TM(T/M) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 8, 'gid': 0, 't0': 0, 'x': 4, 'merge': '5->0'}; range=V<=17",lesson='contraction inequality is tight: TM(T) = TM(T/M) occurs often')
add('U.ind-R8','U','induction R8: lowest coefficient lc = sum over D with m cycles of prod','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','lowest coefficient lc = sum over D with m cycles of prod_C (white faces inside C) is monotone under contraction R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 14, 'gid': 12, 't0': 3, 'x': 2, 'merge': '3->1', 'values': 'lc 5 vs 7'}; range=V<=17, 86 failures",lesson='m can drop under expansion (1 vs 3), resetting lc; signed-polynomial data is not monotone')
add('U.ind-R9','U','induction R9: m(T) = m(T/M) (when both have pairs)','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','m(T) = m(T/M) (when both have pairs) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 14, 'gid': 7, 't0': 1, 'x': 12, 'merge': '10->6', 'values': 'm 1 vs 3'}; range=V<=17; m(T) <= m(T/M) always holds, equality fails in 358 simple contractions",lesson='expansion can merge D-cycles')
add('U.ind-R10','U','induction R10: Skein relation TM(T) = TM(T/M) + TM(T/N) (both merges define','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','Skein relation TM(T) = TM(T/M) + TM(T/N) (both merges defined) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 6, 'gid': 0, 't0': 0, 'x': 3}; smallest_strict_less={'V': 13, 'gid': 7, 't0': 3, 'x': 10}; range=V<=17: fails in 24,600 of 172,436 vertex-root pairs, in both directions; least squares over V<=16 leaves max residual 14.5",lesson='only #states satisfies the deletion-contraction identity (PROOFS Prop 1.1); TM and pairs do not, because pairs mix M- and N-types')
add('U.ind-R11','U','induction R11: Prescribed corner: for every face t in A and non-root corner','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','Prescribed corner: for every face t in A and non-root corner u, some TM has s(t)=u (HCs); same for the mate r (HCr) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 8, 'gid': 0, 't0': 0, 'face': '(3,6,5)', 'corner': 3}; range=V<=17: HCs holds in only 20 of 13,130 rooted instances with a pair (8 of them octahedron roots)",lesson='local prescriptions at a face are generally impossible; consistent with NP-completeness of prescribing edge sets')
add('U.ind-R12','U','induction R12: A good contraction (result has a pair) always exists','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','A good contraction (result has a pair) always exists R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 9, 'gid': 0, 't0': 1, 'note': 'T has a separating triangle'}; range=V<=17; no failure without separating triangles",lesson='separating triangles must be handled by gluing (multiplicativity), not contraction')
add('U.ind-R13','U','induction R13: Inverse P-operation (Batagelj) preserves pairs','REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md','Inverse P-operation (Batagelj) preserves pairs R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.','induction',cex="smallest={'V': 6, 'note': 'octahedron: every P-reduction is non-simple and loses the pair'}; range=V<=17: 15,226 of 58,593 P-reductions (rooted, avoiding t0) lose the pair",lesson="P-reduction is less useful than Q-reduction; TM(T) >= TM(T'') still holds")

add('U.loads-dead','U','rainbow loads are M-convex','REFUTED','reft','reft/RAINBOW.md; reft/data/loads_sampled_6_13.json','Rainbow load vectors satisfy simultaneous M-exchange.','matroid',cex='V=12, first instances with two factors; author search, unreviewed.',lesson='Singleton-factor tests made the exchange property vacuous; include instances with several factors.')
add('D.chain-dead','D','every maximal lattice chain hits success','REFUTED','rc','rc/REFEREE.md; rc/data/r3.json; rc/data/R2_glued_V33.json','Every maximal chain contains an element carrying a good pair.','lattice',cex='Saved V=60 chain of seven elements; V=33 gluing already refutes it. No minimum claim.',lesson='A chain can complete one coordinate block before entering the next and miss every success.')
add('D.fraction-dead','D','at least half the lattice succeeds','REFUTED','rc','rc/REFEREE.md; rc/data/r5.json; rc/data/R2_glued_V33.json','At least half the factor lattice admits a successful direction choice.','lattice',cex='Saved V=70 gives 654/1410=109/235; V=33 gluing gives 4/16. No minimum claim.',lesson='Independent witness blocks multiply the successful fraction down to 2^-q.')

# Late main-manuscript referee delivered during final integration.
_upd('G2.main',where='paper/main/barnette.tex; research/2026-11-14_sol_referee-main/REFEREE.md; research/2026-11-14_sol_referee-main/EDITS.md',text='Merged dual proof independently AI-refereed: FOLLOWS for Theorem 1.1, including the inside-cycle connectivity repair. Eight replacements proposed; application not checked here. Off-route Remark 4.10 is Laurent, not an ordinary polynomial with the chosen heights. Second cold read remains pending.')
checked('G2.main','research/2026-11-14_sol_referee-main','Main theorem route FOLLOWS. Off-route Laurent terminology and conditional-scope edits proposed; application not certified. Second cold read pending.')

_upd('TG.older',label='older radial-tree dictionary and limits')

# Consistency pass, 2026-11-14 (research/2026-11-14_opus_consistency-edits/). Names follow the main paper:
# good state (T: tree matching), good pair (inv: forest pair; T: tree pair), cover, m (was cmin), q(s) (T: k).
# Statements below were overtaken by the final referee reports and the late runs.
FOLDERS.update(pack='research/2026-11-14_opus_two-tree-packing', xa='research/2026-11-14_opus_cross-audit',
               bp='research/2026-11-14_opus_blueprint', il='research/2026-11-14_astra_induction-lemmas')
for tag in ('pack', 'xa', 'bp', 'il'):
    REVIEW[tag] = {'state': 'unreviewed'}
_upd('N.li-check', where='research/2026-11-14_astra_audit-digestions/code/verify.py; research/2026-11-14_astra_audit-digestions/outputs/verification.json; '
     'research/2026-11-14_opus_referee-involutions/DISCREPANCY-279-213.md', text='+ The involution note counts 279 objects on the same running.json with the same Tutte recipe, roots 4 and 5 '
     'sent to each other\'s anchor points (a reflection). Both counts are right: the object count depends on the drawing '
     '(69 drawings, 35 values from 103 to 363), the signed sum -9 and the nine second-fixed objects do not '
     '(research/2026-11-14_opus_referee-involutions/DISCREPANCY-279-213.md).')
_upd('G2.primal', where='proofs/primal/PRIMAL-PROOF.md; research/2026-11-14_opus_cross-audit/ADJUDICATION.md; research/2026-11-14_fable_referee-primal/REFEREE.md',
     text='Full primal proof, AI-refereed before revision, revised, and accepted in a cross-audit. The M4 question is settled: '
          'the real sign divided by the Lean phase is the constant i^n for every pair (proved and checked on 24,856 pairs).')
checked('G2.primal', 'research/2026-11-14_opus_cross-audit', 'Revised note ACCEPT; phase ratio i^n proved in ADJUDICATION.md.')
_upd('G2.main', text='+ A second version applying the eight edits is in progress. Blueprint: of 34 route statements, 4 have an exact '
     'Lean counterpart, 25 a counterpart in another form (translation not formalised), 5 none; Lemma 4.7 has a standalone Lean proof '
     '(research/2026-11-14_opus_blueprint/REPORT.md).')
checked('G2.main', 'research/2026-11-14_sol_referee-main', 'Main theorem route FOLLOWS. Eight edits proposed; a second version applying them is in progress, not certified here.')
_upd('G2.inv', where='proofs/involutions/; research/2026-11-14_opus_referee-involutions/REPORT.md; research/2026-11-14_sol_involutions-revision/REPORT.md',
     text='Written bijective route through marked objects and two involutions. Independent AI referee: FOLLOWS, one sign error off the route. '
          'The revision applied all fifteen edits and added a drawing-free mark model, which has no second referee yet.')
checked('G2.inv', 'research/2026-11-14_opus_referee-involutions', 'FOLLOWS; fifteen edits, all applied in the revision. The added drawing-free model is unreviewed.')
_upd('U.packing', status='PROVED-HERE', src='pack', where='research/2026-11-14_opus_two-tree-packing/PROOFS.md Thm 2.1; research/2026-11-14_opus_two-tree-packing/REPORT.md',
     text='For every pair, the 2n white-graph edges dual to the spokes of r and s split into two spanning trees (Nash-Williams, no signed count). '
          'It holds for every choice of one deleted corner per black face, so it never sees the states, and it does not give a good state. '
          'Author proof, unreviewed.')
add('U.packing-P2', 'U', 'P2: two face-rainbow trees in every pair support', 'CONJECTURE', 'pack',
    'research/2026-11-14_opus_two-tree-packing/PACKING.md; research/2026-11-14_opus_two-tree-packing/PROOFS.md Conj 3.4',
    'Every pair support splits into two face-rainbow trees. True on all 14,881 supports with V<=17. Doing the face and point sides at once '
    'is the key lemma and fails inside a fixed support.', 'matroid', test='Extend the support census to V=18 and look for a support with no split.')
_upd('U.G', text='+ The induction-lemmas run (where it is called G) proves it for triangulations without chordless five-cycles; unreviewed.')
_upd('U.ML2', text='+ The induction-lemmas run (where it is called X) refutes mate repair at V=16, single-cycle repair at V=17 and every '
     'fixed-cover direction repair at V=18: a repair must sometimes change the cover.')
for step in STEPS:
    if step['id'] == 'U':
        step['freedom'] = ('Contraction induction stops at ML1 and ML2; rainbow exchange X and the face-side packing P2 remain conjectural. '
                           'Two-tree packing itself is proved but does not see the states. The natural two-matroid and LP shortcuts fail.')
