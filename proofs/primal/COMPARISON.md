# Primal versus dual exposition

This is an editorial assessment of the proofs read, not a theorem about which presentation is universally shortest. Mathematical equivalences below are PROVED-HERE in PRIMAL-PROOF.md or LIT as cited. I recommend the primal route for the final proof, with one candid sentence explaining face circuits. It is better aligned with the conclusion and avoids the most cumbersome drawing argument.

## Step by step

| Step | Primal note | OpenAI dual presentation | Assessment |
| --- | --- | --- | --- |
| State the target | Find a perfect matching containing the prescribed edge, with connected complement. | Prove a prescribed partition into two induced trees, then translate it back. | Primal is shorter and tells the reader what is being built. The dual target is attractive if induced-tree partitions are themselves the topic. |
| Define a state | Match nonroot black vertices to nonroot faces. Euler gives equal part sizes. | Match bounded black triangles to nonroot vertices. | Similar length. Three corners in a triangle are easier to draw than three face sectors at a cubic vertex. Li already makes the primal formulation natural. |
| Find the first pair | Minimal deficient face set; union its boundaries in G; Euler produces a forbidden monochromatic 3-cut. | Capacity inequality becomes an induced density bound, followed by planar region counts. | Li's primal proof is more direct for this audience. Its balance condition and the nontriviality of the cut should be stated, not left implicit. Lean's global density proof is another option, not the one copied here. |
| Describe the inside | The shore of a minimal cut that excludes the root vertex. | The bounded disk of a simple cycle in the triangulation. | Primal needs no drawn separating curve, but requires a short circuit-cut lemma. The dual picture explains the geometry faster. Neither route gets separation for free. |
| Disk identity | Four counts: cubic ends, colour ends, Euler after deleting a connected shore, and the state union/intersection. | Interior vertices and black/white triangles in a disk. | The dual display is shorter. The primal display is more explicit about which assumptions do work. The no-pinch condition becomes the elementary statement that a facial boundary with vertices in both shores contains a cut edge. |
| Weights | Send one unit from the root vertex to each white vertex. Integrate locally around each black vertex. | Assign spoke circulations and show a detoured cycle is simple and preserves orientation. | Primal wins decisively. Flux through a cut replaces the detour and isotopy. This is the main lesson from Lean. |
| Cancellation | Product of local real signs; reverse an odd circuit. | Complex phase changes sign when its index changes by two. | The real sign is a modest simplification. It is the referee's refinement, not literally Lean's phase definition. |
| Nonvanishing | Products of linear factors; the least possible circuit number gives a nonzero coefficient. | Products of exponentials; the first nonzero Taylor coefficient has a common phase. | Same mathematics. The polynomial removes analysis and exposes the exact use of the number three. This works for every minimum circuit number, with no separate multi-mark appendix. |
| Recovery tree | Delete one opposite edge at each nonroot black vertex and two edges at the root. The remainder in G is a tree. | Pass to a spoke tree and its complementary white-face tree. | Primal is shorter and easier to validate. The intermediate tree is already a subgraph of the graph whose Hamiltonian cycle we want. |
| Perfect matching | Root that tree and take the parent edge of each white vertex. | Assign white-tree edges to their far endpoints and translate back. | Same construction, fewer translations in primal. Lean's Hall proof is less explicit than either; do not copy that aspect of the formalisation. |
| One cycle | A matching-only cut has balanced colours, contradicting the state cut identity. | Prove selected dual edges acyclic, then label the two sides to obtain two induced trees. | The primal argument closes the target directly. Li also stays closer to G, but his final innermost-cycle proof uses more geometric nesting than the cut-balance proof here. |
| Reducible case | Contract each connected shore of a 3-cut to one vertex, then splice two spanning paths. | Split along a separating triangle and glue two tree partitions with prescribed labels. | Primal is shorter and easier to draw. Keep the quantifier “for every prescribed edge”; an unspecified Hamiltonian cycle is not enough for this gluing step. |

## What “entirely in G and its faces” means

The note defines no second triangulated graph and never draws a spoke graph. Its data are vertices, edges, facial boundary cycles, face incidences, cuts, states, and flows of G. It does use consecutive face labels across primal edges. That relation is precisely the incidence data usually packaged as the dual graph. Calling these objects “face circuits” does not produce a new proof without planar duality. It gives a different presentation and recovery route, with the same state-cancellation mechanism.

The Lean proof is also not literally a proof with no second network. It has networks N and D with exchanged cycle and cut spaces. The earlier report's slogan that everything happens in G is useful only with this qualification. The present note proves the necessary facial interpretation rather than suppressing it.

The topology saved is specific: there is no isotopy replacing edges by two spokes, no half-ray intersection pairing, and no Jordan labelling of the final cycle. Euler, the elementary boundary-walk rules of a plane embedding, face merging on deletion, and planarity of contractions remain. The oriented face-boundary span is proved by Euler and finite-dimensional linear algebra. A topology-free theorem could instead assume this algebraic data, but that would move the obligation to verifying the hypothesis for planar graphs.

## Comparison with Li throughout

LIT. Li's Definition 5 and Lemma 9 provide the natural primal incidence relation and the minimal-deficit argument. This note adds the balance calculation and spells out why the deficient subgraph is induced after Claim 12, why it is connected, and why the resulting cut has two nontrivial shores. It does not require the stronger claim that every connected union of chosen facial cycles is 2-connected.

Li's Claim 25 is the incidence-cycle form of the same signed imbalance. The four-count version here follows the checked statements in StateDisk.lean and identifies its two planar inputs separately.

Li's Lemma 7 uses two sign-reversing involutions, fully developed for a one-cycle minimum in the body and sketched for the general case in Appendix B. The repository's dependency audit lists the missing verifications and supplies them. Our polynomial handles all circuit counts in one formula, so it neither inherits that exposition gap nor disputes the possibility of filling it.

Li's Lemma 30 selects the same kind of matching from a rooted tree, but its connectivity proof uses an innermost-cycle argument and black dual traces. The cut-balance contradiction in Lemmas 11 and 12 is the cleaner conclusion for this note. Li's Appendix C is already the right primal induction; retaining 3-edge-connectivity avoids a needless conversion back to vertex connectivity at each cap.

## Recommendation for the final paper

Use the prescribed-edge matching statement as the main induction theorem. Keep the primal incidence definition, the four displayed counts, the single flow, the real-sign linear polynomial, and the recovery tree in G. Give the circuit-cut lemma once near the start, with the allowed plane-embedding facts stated explicitly. Use the cube to show the flow and recovery, and the 20-vertex example to show an actual cancelled state.

For a figure, a dual triangle makes a local cyclic sign easier to see, but it need not enter the proof's notation. If the final paper wants a strictly primal visual language too, draw the three face sectors around one black vertex and label their cyclic transitions. Draw the cut side as a set of vertices of G, without adding a second graph. The larger example should display the cut and the flow separately; overlaying both on every face label would obscure the construction.

This is a distinct route for the collection in its objects, planar bookkeeping and final recovery. It is not an independent new proof principle. Its strongest improvements are the single-flow lemma and the direct ending, and those are already supported by the machine-checked development.
