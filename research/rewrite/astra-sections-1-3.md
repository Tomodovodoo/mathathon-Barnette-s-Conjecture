The first three sections can be reduced to about four pages. Preserve the disk count and the passage from a rooted forest to a perfect matching; most of the remaining length is elementary background or repeated examples. Line numbers below refer to paper/main/barnette.tex.

| Item | Recommendation |
|---|---|
| Abstract, 38–45 | Reduce to four sentences: theorem, dual formulation, paired-state cancellation/nonvanishing, separating-triangle induction. Delete the elementary explanation of complements of matchings and the separate corner-choice sentence. Drop “self-contained”. |
| Main theorem, 57–60 | Keep verbatim, with attribution. Delete definitions of Hamiltonicity and 3-connectivity, 51–55 and 62. |
| Plan, 67–93 | Replace by the ten-sentence overview below. The five numbered stages are useful distinctions, but too detailed before the objects exist. |
| History and sources, 102–113 | Retain a short historical paragraph and credit the 2026 proof. Cite Hertel for older results; omit the catalogue of computational thresholds and discussion of differences between expositions. |
| Example introduction, 115–120 | Cut completely, including enumeration counts. |
| Dual lemma and proof, 135–154 | Replace by two sentences invoking cycle–bond duality: 3-connectivity implies 3-edge-connectivity, hence the dual is simple; cubicity and the bipartition give triangular faces and their colouring. No numbered lemma. |
| “Coloured triangulation”, 156–159 | Use “simple Eulerian plane triangulation, with its faces properly coloured black and white”. Specify at least four vertices and a spherical embedding once. Delete the shared-side argument and discussion of needing connectivity. |
| Connectivity lemma and proof, 161–174 | Cut. Connectedness is part of the triangulation convention. A cycle bounds a triangulated disk; capped pieces are connected disk triangulations. The general lemma is true but unnecessary. |
| Counts, 176–181 | Keep one inline sentence: “Write k for the number of faces of either colour; Euler's formula gives |E(T)|=3k and |V(T)|=k+2.” Cut the example. |
| Selection definition, 183–195 | Keep as one inline definition, including P*. Delete the definition of perfect matching and the explanation of why an arbitrary edge set is introduced. “Selection” is economical if used consistently; do not introduce another synonym. |
| Duality lemma and proof, 197–220 | Replace entirely by the standard assertion that N is acyclic iff T*−N* is connected, with the complementary spanning-tree consequence. Cite cycle–bond duality. Delete the alternative proof at 220. |
| Target proposition and proof, 222–243 | Keep the Hamiltonian conclusion in the setup. Retain the induced-tree conclusion only for gluing, preferably there. Combined proof: four lines, supplied below. Delete 241–242. |
| Root and state setup, 247–252, 273–281 | Keep, in one paragraph. A state is also a perfect matching of the black-face/nonroot incidence graph; say this now, not first in the flow section. |
| Selection-to-state lemma and proof, 254–271 | Cut. It motivates the definition but proves the reverse of the implication needed. It is needed only for the later classification of which cycles arise, itself dispensable. At most say that orienting a candidate forest towards its roots suggests the definition. |
| State example and array, 299–315 | Cut both, including alpha and beta. The ten-column array teaches no general step. |
| Tree-of-faces discussion, 324–332 | Absorb the definition of Y_s into recovery. Cut perfect-matching uniqueness and leaf deletion: existence is what the theorem needs. |
| Good-state definition, 334–338 | Keep inline: Q_s is a spanning forest with three components, each containing one root. Delete the alternative terminology at 338. |
| Good-state lemma and proof, 340–348 | Absorb into recovery: adding ao and bo joins the three rooted trees. The converse is unused on the shortest route. |
| Y lemma and proof, 352–370 | Absorb into recovery; four lines suffice. Delete the separate verification for each possible side of a white face, 365–368. The black-parent/white-child edges form a perfect matching immediately. |
| Transition and chosen sides, 379–387 | One sentence defines the oriented edges under consideration. Delete 387, which explains a letter choice. |
| Outdegree lemma and proof, 389–400 | Keep as an unnumbered two-sentence observation used here and in the partner argument. The current proof is already short; remove the formal lemma wrapper. |
| Disk setup, 401–419 | Retain the definitions of h, B, W, I, ell immediately inside the lemma proof. Delete the figure-specific sentence and the entire construction of R_Z. |
| Disk lemma and proof, 421–449 | Keep as a numbered lemma. It is a proof-specific identity, not merely Euler's formula. Six to eight typeset lines suffice; replacement below. Delete 448–449. |
| Recovery proposition and proof, 451–479 | Keep, incorporating the good-state and Y lemmas. Target twelve to fifteen lines including tree construction. Replace 461–476 by the proof below. The one-versus-three explanation at 479 is useful only if the proof does not already make it explicit. |
| Recovery example, 481–486 | Cut. The six-cycle count, component vertex lists and cube computation are unnecessary. |
| Transition, 488–489 | One sentence: “It remains to construct a good state when there is no separating triangle, and then glue across separating triangles.” |

Standard references should support standard facts, not replace the new argument. Use Diestel, Graph Theory, sixth edition, Theorem 4.2.9 for Euler's formula and Proposition 4.6.1 for cycle–bond duality, whose complementary-tree consequence follows at once. The Jordan curve theorem is Theorem 4.1.1. These appear in the [author's chapter on planar graphs](https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch4.pdf). The dual description follows from these facts and the definition of a dual; there is no need for a separate theorem asserting the whole package. For the two-induced-trees formulation, cite Alt–Payne–Schmidt–Wood, Lemma 5, already cited in the paper. Do not cite a theorem about 2-connected facial boundaries as if it were the converse connectivity lemma. Simply work with triangulated disks.

Replacement proofs

Target, 230–239: “Since P* is a perfect matching, G−P* is 2-regular, and cycle–bond duality makes it connected. Thus it is Hamiltonian. The forest P has k edges and k+2 vertices, hence two components. If an omitted edge joined vertices in one component, its fundamental cycle would be crossed exactly once by the Hamiltonian cycle, contrary to cut parity.”

Outdegree, 395–397: “Every cycle has as many tails as edges, so all its vertices have their unique outgoing edge on the cycle. A component with v vertices and r sinks has v−r edges; consequently it is a tree with one sink or a unicyclic component with no sink.” Here every nonsink has outdegree one; explicitly retain the assumption of outdegree at most one.

Disk, 428–445: “The cycle avoids the roots. Let I count its strictly interior vertices. Euler's formula for its triangulated disk and signed counting of face sides give
B+W=2I+h−2,  3(B−W)=2ell−h.
The state matches the interior black faces bijectively to the interior vertices and those boundary vertices whose outgoing edge has its black face inside. Hence B=I+ell. Eliminating I gives W−B=1 and h−2ell=3.” Keep these three identities in one display; the last two conclusions can be inline. This preserves precisely the state-dependent step.

Recovery, combining 340–370 and 460–476: “Since Q_s has one root in each tree, S_s=Q_s∪{ao,bo} is a spanning tree. By plane duality Y_s=T*−S_s* is a tree. Root it at t_0. Every black vertex has exactly one child: t_0 has degree one and the other black vertices have degree two. Matching each black vertex to its child therefore matches every white vertex to its parent. The corresponding selection P_s contains e_0 and avoids Q_s.
Orient each edge of P_s−e_0 away from its selected corner. Nonroots have outdegree one and roots zero. Any cycle Z is directed. With the disk lemma's notation, the selected boundary edges match ell interior black faces and h−ell interior white faces to exterior faces; all remaining interior faces are matched internally. Thus W−B=h−2ell=3, contradicting W−B=1. Therefore P_s−e_0 is a forest with one root per component. Adding ab joins two components, so P_s is acyclic.”

Figures, notation and layout

Cut the six-panel cube figure, 95–100; the large example drawing, 122–127; cut the local triangle, 283–297, the Q comparison, 317–322, and the recovery illustration, 372–377. Their content is either elementary or duplicates the construction. Keep only fig:disk, 407–412, redrawn schematically without numbered example vertices. Caption: “The state matches interior black faces to interior vertices and to the tails of boundary edges whose black face lies inside.” This illustrates the only nonroutine counting bijection. There are no formal remarks or standalone table environments in this half; the state array is its only table.

Drop R_Z, y_0, alpha and beta; none is needed after the examples disappear. Keep I, B, W, h and ell local to the disk argument; their few uses are justified by the calculation. Keep S_s and Y_s local to recovery. Keep A, X, n, Q_s and the roots because the second half uses them repeatedly. Avoid naming “chosen sides” as another object; say “edges directed from the corners selected by a state”. Inline the counts at 178–180 and B=I+ell at 442–444, or combine the latter with the other two disk equations. The target proposition's two-item enumeration becomes one sentence. No additional case table is needed.

Introduction

Order: historical problem and proof attribution; strengthened theorem; dual reformulation; proof overview. Delete the textbook definitions, cube example, detailed historical list, enumeration claims and comparisons between accounts.

Proposed opening: “Barnette's conjecture asserts that every cubic, bipartite, 3-connected planar graph is Hamiltonian. OpenAI proved the conjecture in 2026, in the stronger form that a Hamiltonian cycle can avoid any prescribed edge. We present their proof through the dual triangulation, where the central problem is to turn local corner choices into a spanning forest.”

Proposed overview: “In the dual triangulation, the bipartition colours the triangular faces black and white. We seek an acyclic edge set containing exactly one side of every face and containing the prescribed dual edge. Its complement in the primal graph is then a Hamiltonian cycle avoiding the prescribed edge. Fixing an outer black face leaves equally many other black faces and nonroot vertices. A state matches these faces to incident nonroot vertices. When the opposite sides form three trees rooted at the outer corners, complementary-tree duality produces the required selection, and a disk count proves its acyclicity. To find such a state, consider pairs of states differing at every face. A sign-reversing involution cancels pairs whose second state has a cycle among its opposite sides. Grouping the same weighted sum by the cycles between the two states proves that it is nonzero. Finally, an integral flow supplies an initial pair in the absence of separating triangles, and induction across separating triangles completes the proof.”

No mathematical error appears in the retained arguments. Goodness depends on t_0, not on the choice of e_0; correct the wording at 457 accordingly. No-separating-triangle is not required anywhere in this half. Do not strengthen recovery by assuming it.

Proposed order and budget: introduction and theorem, 0.8 page; dual setup and target, 0.5; states, opposite sides and goodness, 0.5; outdegree observation and disk lemma with one small figure, 0.9; recovery proposition, 0.7. Total 3.4 pages, allowing up to four for comfortable spacing. Use two section headings, Introduction and States and recovery; the next section can begin with pairs.

