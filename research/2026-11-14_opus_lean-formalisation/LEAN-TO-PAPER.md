# Lean to paper: which declaration formalises which statement

Summary.
1. Every numbered statement of the OpenAI paper on the route to Theorem 1.1 has a Lean counterpart, except Theorem 2.2 in its stated form (two induced trees), which is replaced by its primal equivalent. Corollary 7.2 (Pfaffian, `P4`) is not formalised.
2. Two blocks of the Lean (about 2,050 counted lines of 7,015, 29%) correspond to single sentences of the paper: "fix a sphere embedding" / "the sphere dual" (1,078 lines), and the tacit facts about duals of plane graphs (974 lines).
3. One-sentence steps that cost the most: the inside of a cycle is a disk with connected sides (Lemma 4.1, about 500 lines including the Jordan-type facts), the proof of Theorem 1.1 ("no edge cut of size one or two", "the dual T is a simple triangulation", "the 2-factor is one cycle", about 540 lines together), and splitting along a separating triangle with the cap colouring (about 430 lines).
4. Paper devices replaced by simpler ones: the exponential sum (by a polynomial), the spoke circulations (by a flow on `G`), max-flow (by Hall), the white-face tree rooting (by Hall plus a forest count), the Jordan-curve labelling of Section 6.2 (by "complement of a dual forest is connected").
5. The complete per-declaration table (697 rows) is generated in `graph/lean-to-paper-full.md`. This file is the curated version.

Paths are relative to `lean/OAI/Combinatorics/Hamiltonian/` at commit `4eaee875`. "Lines" counts non-blank, non-comment lines of the declaration including its proof. Section totals are in the last table. "None" means the paper has no corresponding statement.

## 1. Statement and the passage from Theorem 1.1 to the dual

| Paper | Lean declaration | file:line | lines | Note |
| --- | --- | --- | --- | --- |
| Thm 1.1 (statement) | `MainStatement`, `main` | Model:42, Main:47 | 5, 36 | definitions match the conjecture; see DIFFERENCES.md, section A |
| "planar" | `PlaneEmbedding`, `Planar` | Model:10, Model:29 | 17, 2 | a crossing-free drawing in ℝ² by injective paths |
| "3-vertex-connected" | `ThreeVertexConnected` | Model:33 | 3 | at least 4 vertices, deleting at most 2 leaves a connected graph. Same as the paper's Section 1 |
| "Hamiltonian cycle" | `HasHamiltonianCycle` (Mathlib `Walk.IsHamiltonianCycle`) | Model:38 | 2 | |
| "fix a sphere embedding", "the sphere dual T = G*" | `PlaneEmbedding.exists_exact_dual` | ExactDual:116 | 6 (plus 1,072 below it) | none: the paper takes the dual for granted. The Lean proves that a drawn graph has an algebraic dual |
| | `exists_lattice_corridor_model` | Corridors:61 | 30 | thicken branch sets (vertex plus first third of each arc) and arc cores (middle third), cover by grid cells of size `ε/2` |
| | `uniform_thickening`, `cells_connected` | Traces:240, SquareGrid:169 | 16, 16 | compact disjoint sets have disjoint `ε`-neighbourhoods; cells meeting a connected compact set form a connected grid set |
| | `exists_lattice_minor_model`, `BranchPartition.extend` | MinorModel:271, BranchPartition:26 | 5, 73 | a minor model of `G` in the square grid, then grown to a partition of a box |
| | `grid_duality` | Rectangle:180 | 7 | the `(2r)×(2r)` grid and its explicit dual: inner squares plus one outer face |
| | `Duality.minor`, `Duality.graphMinor` | CappedDuality:62, ExactDual:96 | 76, 11 | deletion in the primal is contraction in the dual, so a minor of a graph with a dual has a dual (Whitney) |
| Thm 1.1 proof, "no edge cut of size one or two" | `boundary_cover_of_threeConnected`, `region_card_le_cut`, `cut_card_three` | Network:241, CutSpaces:25, CutSpaces:51 | 21, 25, 12 | same argument as the paper, but needs `|V| >= 5`, from `cubic_bipartite_order` (Network:210, 28 lines: a cubic bipartite graph has at least 6 vertices) |
| "T = G* is simple" | `Duality.simple_dual_edge` | ThreeCuts:37 | 43 | a dual loop or parallel pair would give a gradient supported on at most 2 edges (`gradient_small_support_edge`) |
| "cubicity gives each dual face a triangle" | `triangle_of_flow`, `Duality.cubic_face_triangles_edge` | CutSpaces:232, ThreeCuts:82 | 79, 9 | the gradient of `1_v` is a dual flow with support 3, and a simple flow with support 3 is a triangle |
| "the bipartition colours the faces of T" | `make_coloredDual`, `oriented_face` | ThreeCuts:101, Circulation:100 | 7, 45 | also fixes the cyclic orientation of every face of `T`, which the paper gets from the plane |
| "\|V(T)\| = 2 + \|V(G)\|/2" and (2.1) | `black_dual_card`, `cubic_cards`, `Duality.euler` | MinorDuality:179, Matching:477, Network:192 | 14, 9, 6 | Euler is a rank count: `dim ker ∂ = |E| - |V| + 1` and the duality |
| last paragraph: 2-regular and connected gives one cycle | `Duality.hamiltonian`, `matching_complement_two`, `cycle_at_of_connected_two` | Main:13, Gluing:26, CappedDuality:187 | 20, 9, 24 | in the Lean the complement of a perfect matching. The paper reaches it through induced trees |

## 2. Section 2: plane trees, states, pairs

| Paper | Lean declaration | file:line | lines | Note |
| --- | --- | --- | --- | --- |
| Lemma 2.1 (complement of a spanning forest has connected dual) | `Duality.complement_connected` | Matching:79 | 13 | algebraic: a flow of `T` supported on an acyclic set is zero (`conserved_supported_acyclic`), so every function constant on components of `G - S` is constant. Only the "more generally" half is used |
| definition of state | `TriangleSystem.State`, `ColoredDual.State` | TriangleSystem:19, ColoredDual:46 | 3, 1 | an index in `Fin 3` per black triangle, bijective onto the non-roots. Defined for an abstract triangle system |
| definition of pair | `TriangleSystem.Partner`, `TriangleSystem.Pair` | TriangleSystem:82, PairPhases:189 | 1, 1 | |
| `A`, `X`, roots | `ColoredDual.Black root`, `ColoredDual.nonroots root` | ColoredDual:27, ColoredDual:44 | 1, 1 | the root is a black vertex of `G`, not a face of `T` |
| `\|A\| = \|X\|` | `nonroots_card` | BMatching:341 | 18 | |

## 3. Section 3: Proposition 3.1 (a pair exists)

| Paper | Lean declaration | file:line | lines | Note |
| --- | --- | --- | --- | --- |
| Prop 3.1 | `ColoredDual.pair_nonempty` | BMatching:403 | 25 | hypothesis "no separating triangle" is `TrivialThreeCuts`: every 3-edge cut of `G` has a singleton side |
| degree-2 subgraph splits into two matchings; max-flow argument | `BMatching.two_matchings`, `gadget_hall`, `regular_matching` | BMatching:286, :45, :277 | 28, 92, 8 | no flows. Hall's theorem on a gadget bipartite graph gives the degree-2 subgraph, and Hall again splits a 2-regular bipartite graph |
| (3.1) | `capacity_full`, `state_capacity` | MinorDuality:220, BMatching:378 | 16, 24 | |
| (3.1) ⇔ (3.2) | `capacity_identity`, `black_edge_partition`, `three_corner_count` | MinorDuality:195, :159, :115 | 24, 19, 9 | |
| (3.2) | `induced_density` | MinorDuality:87 | 18 | proved globally, not per component |
| (3.3) `\|b'-w'\| <= d-4` | `region_balance_rim`, `rim_defect`, `region_density` | Contraction:223, :273, MinorDuality:55 | 33, 9, 31 | a "region" of `T[U]` is a connected component of `G` minus the dual edges of `T[U]`, and its "rim" is the face length `d` |
| "a triangular face of K is an actual face" | `rim_three_cut`, `rim_three_no_internal`, `complement_singleton_root` | Contraction:346, :362, :407 | 14, 15, 18 | the only use of `TrivialThreeCuts`: a region with rim 3 is a single vertex of `G` or the complement of the root |
| (3.4) via `p - m + f = 2` | `induced_euler_bound` | Contraction:121 | 10 | `\|E(T[U])\| + 2 <= \|U\| + #regions` for all of `T[U]`. The rank argument gives the inequality directly, so the case split by component size disappears |

## 4. Section 4: the disk identity

| Paper | Lean declaration | file:line | lines | Note |
| --- | --- | --- | --- | --- |
| `δ(v,w)` | `indexDelta`, `Triangle.index_delta`, `blackDelta` | TriangleSystem:96, :291, StateDisk:385 | 1, 24, 3 | `δ` is `+1` when `w` follows `v` in the stored orientation of the black triangle |
| Lemma 4.1 | `state_disk_delta`, `ColoredDual.cycle_disk` | StateDisk:442, ColoredDual:83 | 37, 18 | conclusion: there are `A` (the triangles inside, root not in `A`) and `c = ±1` with cycle flow `c·∇1_A`, and `blackDelta = -3c` |
| "its bounded disk contains no root" | `Duality.circuit_cut` | FlowCircuits:71 | 53 | none as a lemma: the inside is the shore of the cut without the root, so this holds by construction |
| (4.1) first identity, Euler for the disk | `region_euler`, `region_cycles_eq_range`, `region_connected` | DiskRegions:252, :185, :74 | 7, 54, 78 | needs both shores connected (`Bond.connected_shore`, Bonds:163, 36 lines) |
| (4.1) second identity, side counting | `cubic_region_count`, `cubic_black_region_count` | DiskRegions:290, StateDisk:239 | 14, 20 | counted on `G`: `3\|A\| + \|cut A\| = 2\|edges at A\|` |
| (4.2) `B = I + l` | `state_disk_count` | StateDisk:260 | 114 | the longest single proof in the formalisation. Written as `\|black ∩ A\| + \|cut A\| = \|U\| + \|blackCut A\|` with `U` the vertices of `T` in the closed disk |
| "every vertex in the disk is interior or on the cycle" | `mixed_corner_on_boundary`, `Duality.vertex_flow_circuit`, `faces_vertex_deleted_connected` | StateDisk:129, :19, Bonds:265 | 29, 59, 36 | none: the paper never says that a vertex touching triangles on both sides lies on `C`. The Lean proves it from the fact that the link of a vertex of `T` is a face cycle of `G` |
| "(4.1)-(4.2) imply 2l - h = -3" | `disk_boundary_imbalance` | StateDisk:428 | 13 | `omega` on the three counts. `disk_count_identity` (PairPhases:22) states the paper's exact arithmetic but is unused |

## 5. Section 5: cancellation and nonvanishing

| Paper | Lean declaration | file:line | lines | Note |
| --- | --- | --- | --- | --- |
| Prop 5.1 | `ColoredDual.forest_pair` | Forest:234 | 7 | assembled from the abstract `forest_pair_of_disk_circulation` (PairPolynomials:423, 23 lines) |
| `Q_s` | `oppositeGraph` | TriangleSystem:105 | 7 | |
| `J(r,s)` (5.1) | `rawIndexSum` | PairPhases:30 | 2 | not divided by 3. The phase is `phase n = I^(n/3)` with integer division (PairPhases:9) |
| `Z(x)` (5.2) | `Pair.term`, `stateWeight`, `linearProduct` | PairPolynomials:224, :192, :51 | 2, 2, 2 | `phase(J) · ∏_t (1 + a(t,s(t)) X)` in `ℂ[X]`. No exponential |
| Lemma 5.2 | `OppositeCycle.fixed_second_state_cancels` | PairPhases:91 | 15 | for an abstract triangle system, with "every reversible cycle has index sum ±3" as hypothesis |
| the involution `r ↦ r~` | `OppositeCycle.reverse`, `reversal_involutive`, `reversal_ne` | CycleReversal:171, :238, :243 | 20, 4, 3 | |
| "the chosen cycle must be directed" | `partner_orientation`, `tail_orientation` | CycleReversal:106, FlowCircuits:255 | 6, 21 | |
| `J(r~,s) - J(r,s) = ±2` (in units of 3: ±6) | `reverse_rawIndexSum_diff`, `reverse_phase`, `phase_add_six` | PairPhases:51, :81, :11 | 29, 9, 5 | |
| Lemma 4.1 applied to the `Q_s`-cycle | `ColoredDual.opposite_disk` | Forest:200 | 33 | |
| Lemma 5.3 (positive spoke circulations) | `whiteCharge`, `boundary_of_sum_zero`, `ColoredDual.weights` | Circulation:183, :154, ColoredDual:102 | 3, 28, 2 | replaced: a flow `α` on `G` with `∂α = 1` at white vertices and `-#white` at the root. Weights are potentials of `α` around each black triangle |
| (5.3) `L+(C) - L-(C) > 0` | `StateCycle.signed`, `whiteCharge_cut_integral`, `white_positive_of_boundary` | ColoredDual:183, Circulation:208, :227 | 21, 17, 22 | slope `= c · #(white triangles inside)`, and the disk identity forces at least one white triangle inside. No spoke curve, no isotopy |
| grouping by `D`, orientations of cycles | `Pair.groupEquiv`, `Pair.orient`, `CycleClass` | PairPhases:359, :286, :115 | 6, 3, 1 | cycles of `D` are cycles of the permutation `next = r⁻¹ ∘ s` on black triangles |
| (5.4) | `Pair.group_sum_product` | PairPolynomials:238 | 26 | |
| each factor has a simple zero; leading term (5.5) | `cycle_factor_witness`, `common_phase_sum_ne_zero` | PairPolynomials:288, :12 | 24, 38 | the lowest-degree coefficient of a sum `∑ (-i)^{c_d} X^{c_d} p_d` with `p_d(0) > 0` is nonzero |
| "this coefficient of Z is nonzero" | `Pair.total_sum_ne_zero` | PairPolynomials:348 | 37 | |

## 6. Section 6: recovering the cycle

| Paper | Lean declaration | file:line | lines | Note |
| --- | --- | --- | --- | --- |
| Thm 2.2 without separating triangles | `irreducible_matching` | ThreeCuts:109 | 10 | conclusion: for every edge `e` of `G`, a perfect matching `P ∋ e` with connected complement |
| Lemma 6.1 | `addSink_acyclic`, `ColoredDual.augQ_acyclic` | Matching:114, :281 | 36, 10 | proved by adding two root sides of `t0` to `Q_s`, with the third root as a sink. Outdegree stays at most one, so the result is acyclic. No component count |
| "the remainder is a spanning tree of H" | `removed_acyclic`, `remainder_connected`, `remainder_independent`, `remainder_black_degree` | Matching:330, :342, :487, :444 | 11, 4, 10, 32 | done in `G`: the complement in `G` of `Q_s` plus two root sides is a spanning tree of `G`, with degree 2 at black vertices and 1 at the root |
| Lemma 2.1 applied to spokes; tree on white faces | (no spoke graph) | | | the spoke graph `H` never appears |
| rooting the tree at `y0`, selecting one edge per face | `tree_matching`, `recovery_matching` | ForestMatching:51, :226 | 98, 5 | a perfect matching inside the tree by Hall's theorem and a forest edge count. Not constructive |
| Lemma 6.2 | `ColoredDual.selected_forest`, `selectNet_forest` | ForestMatching:338, :307 | 36, 30 | |
| (6.1) | `matching_cut_balance` | ForestMatching:176 | 34 | stated as: if `cut(A)` consists of matching edges then `\|cut A\| = 2 \|blackCut A\|`. Against `2\|blackCut A\| + 3` from Lemma 4.1 |
| Jordan-curve labelling, two induced trees | (none) | | | replaced by `Duality.complement_connected` (Lemma 2.1) in `recover_connected_complement` (ForestMatching:375, 17 lines) |

## 7. Section 7: separating triangles

| Paper | Lean declaration | file:line | lines | Note |
| --- | --- | --- | --- | --- |
| Proof of Thm 2.2 by induction | `matching_strong` | Gluing:244 | 47 | strong induction on `\|V(G)\|`. Statement for every edge `e` of `G` (H- form), not for a face and an edge of `T` |
| separating triangle | `nontrivial_threeCut_at` | Gluing:235 | 8 | a 3-edge cut of `G` with at least 2 vertices on each side, chosen so that the prescribed edge lies on side `A` |
| "capping each side by a triangle" | `cap`, `cap_duality`, `cap_simple`, `cap_cubic`, `cap_threeConnected` | ThreeCuts:149, CappedDuality:148, ThreeCuts:352, :360, :230 | 2, 13, 7, 6, 11 | the cap is the contraction `G / A^c`. Its dual comes from `Duality.minor` |
| "the coloring extends to each cap" | `threeCut_black_card`, `cap_coloring` | ThreeCuts:367, :381 | 9, 31 | a 3-cut of a cubic bipartite graph has all black ends on one side (counting) |
| "prescribe the same-label edge of the cap" | `cap_matching_boundary` | Gluing:51 | 12 | exactly one cut edge is in the matching of the first piece. It is prescribed for the second piece |
| "the trees glue" | `cap_glue_matching`, `cap_glue_connected` | Gluing:94, :167 | 23, 48 | gluing perfect matchings with connected complements across a 3-cut |
| Cor 7.1 | `Duality.connected_complement_matching` | Gluing:294 | 6 | proved as the induction statement, for algebraic duals. Not restated for `PlaneEmbedding` |
| Cor 7.2 (Pfaffian, `P4`) | (none) | | | not formalised. The scope note `lean/docs/180.md` covers only the Hamiltonian cycle |

## 8. Effort per section

From `graph/effort.md` (generated by `scripts/map_to_paper.py`). Paper lines are non-blank lines of the `pdftotext` dump. Section 1 is mostly history and outline, so the ratio there is meaningless.

| paper section | paper lines | paper % | Lean lines | Lean % | Lean% / paper% |
| --- | --- | --- | --- | --- | --- |
| Sec 1 (introduction) | 76 | 18 | 29 | 0 | (statement only) |
| Sec 2 (plane trees, states) | 33 | 8 | 185 | 3 | 0.33 |
| Sec 3 (Prop 3.1) | 62 | 15 | 885 | 13 | 0.84 |
| Sec 4 (disk identity) | 26 | 6 | 916 | 13 | 2.06 |
| Sec 5 (cancellation) | 105 | 26 | 1,314 | 19 | 0.73 |
| Sec 6 (two induced trees) | 58 | 14 | 660 | 9 | 0.67 |
| Sec 7 (separating triangles, Thm 1.1) | 51 | 12 | 974 | 14 | 1.12 |
| no counterpart: algebraic duality layer | 0 | 0 | 974 | 14 | |
| no counterpart: embedding to dual | 0 | 0 | 1,078 | 15 | |

Within Sec 7, 544 lines go to the proof of Theorem 1.1 (no small cuts, `T` simple, faces are triangles, the 2-factor is one cycle) and 430 to the gluing.
