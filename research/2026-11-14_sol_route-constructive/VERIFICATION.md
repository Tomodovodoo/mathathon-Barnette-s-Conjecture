# Verification ledger

COMPUTED. The commands in DATA.md produced the checked ranges below. No discrepancy with a checked mathematical statement of the three supplied papers was found. These finite tests do not certify their general proofs.

## Scope

COMPUTED. `data/verification.json` records 77 rooted runs. These include all 55 unrooted Eulerian plane triangulations output by the downloaded plantri 4.5 at orders 6 through 14, one embedding-dependent root per graph, four named primal graphs, four built-in generator outputs, and all 14 roots of a connected sum of two octahedra. Some runs repeat isomorphism classes. This is not exhaustive over roots, vertex labels, or prescribed edges on every graph. The largest named primal has 48 vertices.

COMPUTED. Across these runs the checker enumerated 1,040 states and 254 disjoint ordered pairs, including repetitions between runs. It checked 1,466 directed disk cycles, 744 tree-state recoveries, 504 directed exchange adjacencies, 254 marked constructors, 3,234 single-token involution checks, 1,253 Li single-mark objects, 10,248 Li multiple-mark objects, 231 recursive prescriptions, 81,936 subset identities and 248,626 connected induced-subgraph density bounds. `data/supplemental.json` adds 7,819 face-region checks and 49 exact undirected-cycle group checks.

## OpenAI paper

LIT. References below are to `papers/OpenAI-Barnette.pdf`, “Paired states and Hamiltonian cycles in cubic bipartite planar graphs,” supplied September 2026 preprint. Several requested numbers are equations rather than lemmas. There is no separately numbered Lemma 4.2 or Lemmas 5.4 and 5.5 in that paper.

| Obligation | Status and executable check | Limits |
| --- | --- | --- |
| Lemma 2.1 | COMPUTED. `tests/test_proof.py::test_all_cube_incidence_forests_dual_connected` enumerates all 4,096 spoke subsets of the cube incidence graph, retaining forests, and checks connected complementary duals and tree complements. | Exhaustive only on cube H. Recoveries exercise it on larger H. |
| Equation 2.1 | COMPUTED. Construction has triangular faces, bipartite dual and matching-size counts; states, H and recovery sizes agree in all 77 runs. | Definitions are shared across several checks. |
| Proposition 3.1 | COMPUTED. Every separator-free test instance has a disjoint pair; integral flow also returns a pair. | Root 0 except the explicit rerooted glued case. |
| Equation 3.1 | COMPUTED. Every subset of X for n <= 12; only nested prefix subsets for n = 23 in the 48-vertex named graph. | Larger-range subset check is sampled. |
| Equation 3.2 | COMPUTED. Exact equality of the Hall slack and density slack for the same subsets. | No rounding. |
| Equation 3.3 | COMPUTED. `supplemental.py` cuts the full dual along each connected induced K, counts face regions, boundary multiplicities and signed balances. All connected induced K with at least four vertices for all plantri graphs of order <= 10. | 7,819 regions. Bridges count twice, as required. |
| Equation 3.4 | COMPUTED. Every connected induced subset with at least four vertices in separator-free tested T of order <= 14. | Not run at order 26. |
| Lemma 4.1 | COMPUTED. `verify.py` floods the dual outside each cycle, counts I, B, W, h and l, checks all disk equalities, root avoidance and oriented delta-sum minus or plus three. | All outgoing choices for all states only when n <= 6. Otherwise pair D cycles. |
| Equations 4.1 and 4.2 | COMPUTED. Same disk counters check B+W=2I+h-2, 3(B-W)=2l-h and B=I+l individually. | Orientation is checked independently by which directed edge-side lies in the flooded bounded disk. |
| Equation 5.1 | COMPUTED. J integrality and parity, odd D cycles, and sign reversal on every exchange edge. | All 254 pairs. |
| Proposition 5.1 | COMPUTED. Every rooted run with a pair has a tree state; every exchange component has tree pairs. | Components built explicitly, so small instances only. |
| Equation 5.2 | COMPUTED. Exact integer coefficient dictionary with epsilon sign, related to the exponential sum by Z_OpenAI(x)=i^(-n) Z_integer(exp(x)). | The exponential sum is not literally an ordinary polynomial in x. |
| Lemma 5.2 | COMPUTED. Every cyclic second state has zero signed mate sum. Q reversals are valid, reversible and sign reversing. | Includes actual cyclic second states at 20 primal vertices. |
| Lemma 5.3 | COMPUTED. Integer dual routing constructs spoke weights and checks every face circulation exactly; all tested D cycles have positive counterclockwise gaps, and every weight lies in [0,6n]. | Does not enumerate every simple spoke cycle. The route-to-face circulation proof is LIT, not exhaustively verified here. |
| Equation 5.3 | COMPUTED. Strict L+ > L- for every D cycle in the 254 pairs. | Includes cycles adjacent to separators. |
| Equations 5.4 and 5.5 | COMPUTED. `supplemental.py` multiplies orientation factors and compares exact coefficient dictionaries with the pair sum for all 49 groups in plantri orders <=14; it checks the exact first coefficient, not just its sign. | Converted from complex phases to the equivalent integer epsilon convention. |
| Lemma 6.1 | COMPUTED. Every forest second state with a mate has exactly three components, each with one root. | Also checks the stronger mate-count characterization. |
| Lemma 6.2 | COMPUTED. Every selected P is a two-component forest; every face has one selected side; both components induce trees. | Every tree state, all three edges of its chosen outer face. |
| Theorem 2.2 | COMPUTED. Direct recoveries and recursive separator gluing preserve the prescribed same-class edge and induced-tree partition. | 231 recursive prescriptions, including obstructed roots. |
| Corollary 7.1 | COMPUTED. Independent checker tests cycle coverage, input adjacency and forbidden-edge avoidance. Unit tests additionally prescribe every edge of all four named input graphs. | The public API returns original input labels. |

## Li

LIT. `papers/A-Note-On-Barnette.pdf`, Zhentao Li, “A Note On Barnette,” supplied exposition. Its reduced H is our B. Its full face-black incidence graph is our H. Black primal vertices correspond to black triangles, face vertices to vertices of T, and white primal vertices to white triangles.

COMPUTED. The Key Lemma 7 is checked by existence of cycle-breaking pairs on all separator-free tested inputs. The condition that the reduced graph minus the second matching is acyclic is checked by the mate count and the full incidence-tree test. Lemma 8, Corollary 27 and the final cycle construction are tested through the equivalent dual objects.

COMPUTED. `li.py` solves the exact rational barycentric embedding of T inside its root triangle. Black and white face centers provide the incidence drawing and half-ray origins. A rational affine shear avoids all ray-vertex coincidences. Definitions 22 and 23 are implemented literally for the single-mark case. The checker tests involutivity, validity, sign reversal off fixed points, nonempty fixed sets and a common fixed-point sign on every enumerated object when c_min=1.

COMPUTED. `LiMultiObjects` implements Appendix B when c_min>1 and n<=11. It uses sets of distinct intersections, as Definition 14 specifies, stored canonically as sorted tuples. It checks 10,248 complete objects. These runs include c_min=2 and c_min=3. No failing involution or sign check was found.

LIT. Li's Appendix B leaves some bookkeeping in prose. The implementation chooses the first cycle under the same face-set ordering throughout. It does not claim equivalence with an ordered-token convention allowing repetitions. The constructive paper uses that different convention explicitly.

## Constructive paper

LIT. `papers/barnette_trees.pdf`, “A constructive proof of Barnette's conjecture,” dated 18 October 2026.

COMPUTED. Theorem 1.2 is checked in all rooted runs: tree-state existence, pair existence and absence of a black-inner-boundary separator agree. A state has exactly 2^k mates precisely when Q has rooted tree components and k rootless unicyclic components. Tree states have one mate.

COMPUTED. Theorem 5.2 is checked component by component. Tree pairs have equal positive counts of both signs, and the component polynomial has a nonzero first coefficient at its minimum cycle count. Theorem 5.3 is implemented with ordered tokens and explicit caps. Single-token involutions are exhaustively checked; constructors from every pair terminate. Additional benchmark starts exercise nonfixed moves. Two additional benchmark starts exercise a restart from four D cycles to two.

COMPUTED. Lemma 6.1, the same permutation sign claim, is tested on every enumerated state by inversion parity and exact determinant equality. The Hadamard bound is checked as M^2 <= 3^n, with exact integers. Proposition 6.2's constructor succeeds; runtime measurements cannot verify its asymptotic worst-case claim.

## Discrepancies and limits

COMPUTED. No checked paper statement failed. Acyclicity of Q alone is not treated as a tree certificate without the root condition. A state without a mate is never used as a paired forest state.

REFUTED. The naive claim that the signed sum equals the ordinary determinant obtained by setting all face variables to one fails already on the hexagonal prism. See ALGORITHMS.md for the exact polynomial witness. This is a failed route explored here, not a claim made by any supplied paper.

COMPUTED. The marked-walk counter `moves` excludes initialization and records alternating alpha/beta moves only. The benchmark also records initial `normalization_reversals`. A zero-move run may therefore change its input pair before testing beta.

COMPUTED. The JSON exports now use a representative pair whose second state is the selected tree matching, so D, Q, J and the final certificate refer to the same pair. Face-index labels of the reconstructed primal and original input labels are both available.
