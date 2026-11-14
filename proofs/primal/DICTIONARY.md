# Primal-dual dictionary

LIT for source names; PROVED-HERE for the identifications used in this note. Sources: OpenAI, Sections 2 through 7; Li, Definitions 5 and 6, Lemmas 7 and 8, Claims 25 and 31, Appendix C; A constructive proof, Sections 1, 4, 5 and 7. A dash means that this table assigns no exact named counterpart. Lean names are under OAI.Barnette, with the Network and ColoredDual prefixes as specified in STATUS.md. Similar purpose does not mean identical definitions.

| Object in G | Main paper, in T | OpenAI | Li | Constructive paper | Lean declaration |
| --- | --- | --- | --- | --- | --- |
| Black / white vertex | Black / white triangle | Black / white face | B / W | Black / white face | ColoredDual |
| Face; edge as face link | Vertex; edge | Vertex; edge | Face-vertex; dual edge | Vertex; edge | Duality |
| Root vertex b0, its three faces | Outer black triangle t0, its corners | t0, R | b0 and its face neighbours | Outer centre, roots | State root |
| Incidences A to X | State: a corner in each black triangle | State | Perfect matching of H | Perfect matching of B | TriangleSystem.State |
| Two disjoint states | Pair (r,s), different in every triangle | Pair (r,s) | Ordered 2-factor (M1,M2) | Matching pair | TriangleSystem.Pair |
| Edge not on s(b), as face link | Opposite side, in Q_s | Q_s | Cycle-breaking test | Opposite-edge graph | oppositeGraph |
| Directed marked face links; undirected D | D(r,s); its cover | D(r,s); group | Cycles of M1 union M2 | D-cycles | StateCycle |
| Bond; root-free shore | Cycle; disk away from t0 | Disk identity | Claim 25 | Disk identity | circuit_cut; state_disk_count |
| White vertices on cut side | White triangles inside disk | Positive circulation | White-vertex marks | Positive cycle slope | whiteCharge_cut_integral |
| Forest Q_s with a partner | Good state; good pair | Forest pair | Cycle-breaking 2-factor | Tree matching; unique mate | forest_pair_of_disk_circulation |
| Compatible perfect matching P | Selection P, one side of every face | One selected edge per face | Matching P | Recovery, Section 7 | selected_forest |
| Hamiltonian cycle G-P | Acyclic selection; two induced trees | Tree partition | Connected complement | Two induced trees | connected_complement_matching |
| Nontrivial three-edge cut; cap | Separating triangle; capped piece | Gluing | Appendix C | Recursive gluing | cap_duality; cap_glue_connected |

The second column uses the names of the project's main paper, paper/main/barnette.pdf: state, pair, opposite sides Q_s, cover (the undirected D), good state, good pair (a pair whose second state is good), selection. In this note the edges of D are marked, and selected refers only to the matching P.

PROVED-HERE. With aligned corner signs and weights, the real local sign is i^n times Lean's complex phase. The apparently circuit-dependent ratio in the referee report simplifies to this constant. See STATUS.md. The tree recovered in this note lies in G; the white-face tree of the source papers is a different auxiliary tree.

Naming warning. Li's H is the incidence graph of the row "Incidences A to X"; the constructive paper calls the same graph B. OpenAI and the constructive paper use H for the spoke graph, and this note uses B for the black vertices of G. See research/2026-11-14_opus_cross-audit/CONSISTENCY.md.
