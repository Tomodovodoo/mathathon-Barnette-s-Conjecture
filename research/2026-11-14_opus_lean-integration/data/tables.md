| paper (v2) | statement | OpenAI | primal note | involution note | Lean upstream (file:line) | Lean added here (file:line) | status | origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Thm 1.1 `thm:main` | Hamiltonian cycle avoiding e | Thm 1.1 + Cor 7.1 | Theorem T | - | `main` (Main:47), `connected_complement_matching` (Gluing:294), `exists_exact_dual` (ExactDual:116) | - | weaker / different | both |
| Lemma 2.1 `lem:dual` | the dual is a coloured triangulation | proof of Thm 1.1 (Sec 7, paragraphs 1-2) | Lemma 1; last paragraph of proof of Thm T | - | `cut_card_three` (CutSpaces:51), `simple_dual_edge` (ThreeCuts:37), `cubic_face_triangles_edge` (ThreeCuts:82), `make_coloredDual` (ThreeCuts:101), `black_dual_card` (MinorDuality:179) | - | after translation | upstream |
| Text `txt:two-faces` | two faces share <= 1 side | tacit | Lemma 1 (two faces share at most one edge) | - | `TriangleSystem` (TriangleSystem:9), `system` (ColoredDual:29) | - | after translation | upstream |
| Lemma 2.2 `lem:connected` | faces bounded by cycles => connected | none (tacit) | none (map rules in Sec 2) | - | `region_connected` (DiskRegions:74), `connected_shore` (Bonds:163) | - | none | - |
| Eq. (2.3) `eq:counts` | k black, k white, 3k edges, k+2 vertices | (2.1) | Lemma 1 (counts) | Sec 1 | `cubic_cards` (Matching:477), `black_dual_card` (MinorDuality:179), `euler` (Network:192), `nonroots_card` (BMatching:341) | - | after translation | upstream |
| Def. 2.4 `def:selection` | selection | "one selected edge at each black and white triangle" (Sec 6.1) | perfect matching P of G | - | `connected_complement_matching` (Gluing:294) | - | after translation | upstream |
| Lemma 2.5(1) `lem:duality.1` | cycle in N => dual disconnected | Sec 6.2 (Jordan curve labelling) | circuit-cut fact; Lemma 2(a) | background | `circuit_cut` (FlowCircuits:71), `bond_of_circuit` (Bonds:109) | - | after translation | upstream |
| Lemma 2.5(2) `lem:duality.2` | N acyclic => dual connected | Lemma 2.1 | circuit-cut fact (converse direction) | - | `complement_connected` (Matching:79), `conserved_supported_acyclic` (Matching:68) | - | weaker / different | upstream |
| Prop. 2.6(1) `prop:target.1` | acyclic selection => HC | proof of Thm 1.1, last paragraph | Lemma 12, second paragraph | - | `hamiltonian` (Main:13), `complement_connected` (Matching:79), `matching_complement_two` (Gluing:26), `cycle_at_of_connected_two` (CappedDuality:187) | - | after translation | upstream |
| Prop. 2.6(2) `prop:target.2` | two induced trees | Thm 2.2 (two induced trees) | Remark 15 (part) | - | - | - | none | - |
| Lemma 3.1 `lem:selections-give-states` (off route) | HC => state | none | Remark 15 (stronger: also uniqueness) | - | - | - | none | - |
| Def. 3.2 `def:state` | state | Sec 2 (state) | Sec 3 (state) | Sec 1 (state) | `State` (TriangleSystem:19), `State` (ColoredDual:46) | - | exact | upstream |
| Def. 3.4 `def:good` | good state | Prop 5.1 + Lemma 6.1 (no name) | "circuit-free Q_s" with partner; Remark 14 | Theorem 1 (forest Q_s) | `oppositeGraph` (TriangleSystem:105), `augQ` (Matching:276) | - | weaker / different | upstream |
| Lemma 3.5 `lem:good` | good <=> S_s spanning tree | Sec 6.1 ("the remainder is a spanning tree of H") | Lemma 9, first paragraph; Remark 14 | - | `removed_acyclic` (Matching:330), `augQ_acyclic` (Matching:281) | - | weaker / different | upstream |
| Lemma 3.6 `lem:Y` | tree Y_s and selection P_s | Sec 6.1 (tree on white faces, rooted at y0) | Lemmas 9 and 10 | - | `remainder_connected` (Matching:342), `remainder_independent` (Matching:487), `remainder_black_degree` (Matching:444), `tree_matching` (ForestMatching:51), `recovery_matching` (ForestMatching:226) | `perfectMatching_unique` (TreeMatching:20) | weaker / different | both |
| Lemma 3.7 `lem:outdegree` | outdegree <= 1 | inline in Lemma 5.2, 6.1, 6.2 | inline (Sec 3, Lemma 9) | inline (Lemma 4) | `tail_orientation` (FlowCircuits:255), `addSink_acyclic` (Matching:114) | `card_edgeSet_add_sinks` (Outdegree:65), `component_count` (Outdegree:81) | weaker / different | added here |
| Text `txt:inside` | inside of a cycle (R_Z) | Sec 4, one sentence ("its bounded disk contains no root") | Lemma 2 (cut side, no-pinch) | background | `circuit_cut` (FlowCircuits:71), `connected_shore` (Bonds:163), `region_connected` (DiskRegions:74), `region_euler` (DiskRegions:252), `mixed_corner_on_boundary` (StateDisk:129) | - | after translation | upstream |
| Lemma 3.8 `lem:disk` | disk identity | Lemma 4.1 | Lemma 5 | Lemma 2 | `state_disk_delta` (StateDisk:442), `cycle_disk` (ColoredDual:83), `state_disk_count` (StateDisk:260), `disk_boundary_imbalance` (StateDisk:428), `white_positive_of_boundary` (Circulation:227) | - | after translation | upstream |
| Prop. 3.9 `prop:recover` | P_s acyclic | Lemma 6.2 and end of Sec 6.2 | Lemmas 11 and 12 | - | `selected_forest` (ForestMatching:338), `selectNet_forest` (ForestMatching:307), `matching_cut_balance` (ForestMatching:176), `recover_connected_complement` (ForestMatching:375) | - | after translation | upstream |
| Def. 4.1 `def:pair` | pair | Sec 2 (pair) | Sec 3 (pair) | Sec 1 (pair) | `Partner` (TriangleSystem:82), `Pair` (PairPhases:189) | - | exact | upstream |
| Lemma 4.2 `lem:partner` | partner orients Q_s | Lemma 5.2 proof (outdegree) and Lemma 6.1 | Sec 3; Lemma 9; Remark 14 (uniqueness) | Lemma 4 proof | `partner_orientation` (CycleReversal:106), `augQ_acyclic` (Matching:281) | - | weaker / different | upstream |
| Text `txt:D` | D(r,s) = disjoint cycles | Sec 5 (D is a union of vertex-disjoint cycles) | Lemma 8, first paragraph | Sec 2 (D_p) | `next` (PairPhases:204), `CycleClass` (PairPhases:115), `pairedCycle` (Forest:100) | - | after translation | upstream |
| Lemma 4.3 `lem:reversals` | two reversals | Lemma 5.2 proof (1); Sec 5.3 grouping (2) | Lemma 7 proof (1); Lemma 8 (2) | Lemma 4 (1); Lemma 5 case 1 (2) | `reverse` (CycleReversal:171), `reversal_involutive` (CycleReversal:238), `reversal_ne` (CycleReversal:243), `orient` (PairPhases:286), `groupEquiv` (PairPhases:359) | - | exact | upstream |
| Text `txt:delta` | delta, delta-sum = -/+3 | Sec 4 (delta) | Sec 2 (delta), Lemma 3 | Sec 2 (delta) | `indexDelta` (TriangleSystem:96), `index_delta` (TriangleSystem:291), `blackDelta` (StateDisk:385), `cycle_disk` (ColoredDual:83) | - | after translation | upstream |
| Lemma 4.4 `lem:sign` | sign = product of local signs | (5.1): phase i^J | Lemmas 7-8 (same real sign) | Definition 3 (sign with floor(J/2)) | `phase` (PairPhases:9), `rawIndexSum` (PairPhases:30), `reverse_phase` (PairPhases:81), `phase_add_six` (PairPhases:11), `group_sum_product` (PairPolynomials:238) | `paperSign_reverse` (LocalSign:127), `sign_orient` (LocalSign:200), `sign_formula` (LocalSign:270), `sign_formula_concrete` (Concrete:48) | after translation | added here |
| Lemma 4.5 `lem:cancel` | cancellation | Lemma 5.2 | Lemma 7 | Lemma 4 | `fixed_second_state_cancels` (PairPhases:91), `opposite_disk` (Forest:200) | `paperSign_partners_sum` (LocalSign:155), `sum_sign_eq_zero_of_no_good` (RealSign:47) | weaker / different | added here |
| Text `txt:heights` | heights along face paths | Lemma 5.3 (spoke circulations, different weights) | Lemma 6 (integer path flow and local potentials) | rays rho_w and crossings (Sec 1) | `whiteCharge` (Circulation:183), `boundary_of_sum_zero` (Circulation:154), `weights` (ColoredDual:102) | - | weaker / different | upstream |
| Lemma 4.6 `lem:height` | height jump = white faces inside | Lemma 5.3 and (5.3) | Lemma 6 | crossing pairing (Lemmas 5-6) | `whiteCharge_cut_integral` (Circulation:208), `signed` (ColoredDual:183), `paired_sign` (Forest:156), `white_positive_of_boundary` (Circulation:227) | `weight_orient` (RealSign:77) | weaker / different | both |
| Lemma 4.7 `lem:difference` | finite difference | Taylor coefficient of the product (5.4)-(5.5) | Lemma 8 (product of linear polynomials) | Sec 7 (moment comparison, off-route) | `cycle_factor_witness` (PairPolynomials:288), `common_phase_sum_ne_zero` (PairPolynomials:12) | `finite_difference_fin` (FiniteDifference:82), `finite_difference` (FiniteDifference:50) | exact | added here |
| Prop. 4.8 `prop:good` | a pair gives a good state | Prop 5.1 | Lemma 8 | Theorem 1 | `forest_pair` (Forest:234), `forest_pair_of_disk_circulation` (PairPolynomials:423), `total_sum_ne_zero` (PairPolynomials:348) | `forest_pair_real` (Concrete:65), `forest_pair_of_disk_circulation_real` (RealSign:262), `realSum_ne_zero` (RealSign:219) | after translation | both |
| Remark 4.10 `rem:other-sums` (off route) | other sums | (5.2) | (6.1) | Sec 7 | `term` (PairPolynomials:224) | `sign_eq_I_pow_mul_phase_concrete` (Concrete:57), `phase_eq_paperSign` (LocalSign:303) | weaker / different | added here |
| Text `txt:flow` | capacity => pair (max-flow) | Prop 3.1, first paragraph | Lemma 4, first paragraph | - | `two_matchings` (BMatching:286) | - | exact | upstream |
| Eq. (5.1) `eq:hall` | capacity condition | (3.1) | (3.1) | - | `state_capacity` (BMatching:378) | - | after translation | upstream |
| Prop. 5.2 `prop:pair` | no separating triangle => pair | Prop 3.1 | Lemma 4 (different proof: minimal deficit) | hypothesis | `pair_nonempty` (BMatching:403), `state_capacity` (BMatching:378), `capacity_full` (MinorDuality:220), `induced_density` (MinorDuality:87), `region_density` (MinorDuality:55), `region_balance_rim` (Contraction:223), `rim_defect` (Contraction:273), `rim_three_cut` (Contraction:346), `complement_singleton_root` (Contraction:407), `induced_euler_bound` (Contraction:121) | - | after translation | upstream |
| Lemma 6.1 `lem:cap` | caps | proof of Thm 2.2 (cap colouring) | Lemma 13, first part | - | `threeCut_black_card` (ThreeCuts:367), `cap_coloring` (ThreeCuts:381), `cap_simple` (ThreeCuts:352), `cap_cubic` (ThreeCuts:360), `cap_threeConnected` (ThreeCuts:230), `cap_duality` (CappedDuality:148) | - | after translation | upstream |
| Thm 6.2 `thm:T` | acyclic selection containing e0 | Thm 2.2 | Theorem T (first sentence) | - | `connected_complement_matching` (Gluing:294), `irreducible_matching` (ThreeCuts:109), `cap_matching_boundary` (Gluing:51), `cap_glue_matching` (Gluing:94), `cap_glue_connected` (Gluing:167) | - | after translation | upstream |
| Remark Sec 7 `rem:which` (off route) | which HCs arise | none | Remarks 14-15 | - | - | `perfectMatching_unique` (TreeMatching:20) | weaker / different | added here |
| Remark Sec 7 `rem:poly` (off route) | polynomial F(w) | (5.4) | (6.3) | - | `group_sum_product` (PairPolynomials:238) | - | weaker / different | upstream |

| primal / involution | Lean | status | paper node |
| --- | --- | --- | --- |
| primal T  | `connected_complement_matching`, `matching_strong`, `main` | after translation | thm:T |
| primal circuit-cut fact  | `circuit_cut`, `bond_of_circuit`, `connected_shore` | after translation | lem:duality.1 |
| primal 1 elementary setup | `cubic_cards`, `nonroots_card`, `make_coloredDual` | after translation | lem:dual |
| primal 2 face circuits and cut-side faces | `circuit_cut`, `connected_shore`, `region_euler`, `mixed_corner_on_boundary` | after translation | txt:inside |
| primal 3 orientation of a bond | `cycle_cut_scalar`, `blackDelta_cut`, `index_delta`, +`sign_formula` | after translation | txt:delta |
| primal 4 a pair exists in the irreducible case | `pair_nonempty` | exact | prop:pair |
| primal 5 the cut-side identity | `state_disk_count`, `disk_boundary_imbalance`, `state_disk_delta` | exact | lem:disk |
| primal 6 the weights | `boundary_of_sum_zero`, `whiteCharge_cut_integral`, `signed` | weaker / different | lem:height |
| primal 7 cancellation | `fixed_second_state_cancels`, +`paperSign_partners_sum` | after translation | lem:cancel |
| primal 8 nonvanishing | `total_sum_ne_zero`, `forest_pair_of_disk_circulation`, +`realSum_ne_zero`, +`forest_pair_real` | after translation | prop:good |
| primal 9 the recovery tree | `removed_acyclic`, `remainder_connected`, `remainder_black_degree`, `remainder_independent` | exact | lem:Y |
| primal 10 the selected matching | `tree_matching`, `recovery_matching` | weaker / different | lem:Y |
| primal 11 matching cut balance | `matching_cut_balance` | exact | prop:recover |
| primal 12 the complement is one cycle | `selectNet_forest`, `selected_forest`, `recover_connected_complement` | exact | prop:recover |
| primal 13 caps and gluing | `cap_simple`, `cap_cubic`, `cap_threeConnected`, `cap_coloring`, `cap_glue_matching`, `cap_glue_connected`, `cap_duality` | after translation | lem:cap |
| primal 14 the partner is unique when it exists | - | none | lem:partner |
| primal 15 compatible matchings | +`perfectMatching_unique` | weaker / different | lem:selections-give-states |
| involutions 1 Forest-pair lemma | `forest_pair`, +`forest_pair_real` | after translation | prop:good |
| involutions 2 Disk identity | `state_disk_delta` | after translation | lem:disk |
| involutions 3 objects | - | none | txt:heights |
| involutions 4 one | `reversal_involutive`, `reverse_phase`, +`paperSign_reverse` | weaker / different | lem:cancel |
| involutions 5 two | - | none | prop:good |
| involutions 6 fixed | `common_phase_sum_ne_zero` | none | prop:good |
| involutions 7 path-crossings | - | none |  |
| involutions 8 walk | - | none |  |
