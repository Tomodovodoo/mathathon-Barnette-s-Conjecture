| merged paper | statement | OpenAI | primal note | involution note | Lean (file:line) | relation | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Thm 1.1 `thm:main` |  | Thm 1.1 + Cor 7.1 | Theorem T | - | `main` (Main:47), `connected_complement_matching` (Gluing:294), `exists_exact_dual` (ExactDual:116) | primal-form | checked, other form |
| Lemma 2.1 `lem:dual` |  | proof of Thm 1.1 (Sec 7, paragraphs 1-2) | Lemma 1; last paragraph of proof of Thm T | - | `cut_card_three` (CutSpaces:51), `simple_dual_edge` (ThreeCuts:37), `cubic_face_triangles_edge` (ThreeCuts:82), `make_coloredDual` (ThreeCuts:101), `black_dual_card` (MinorDuality:179) | primal-form | checked, other form |
|  text `txt:two-faces` |  | tacit | Lemma 1 (two faces share at most one edge) | - | `TriangleSystem` (TriangleSystem:9), `system` (ColoredDual:29) | primal-form | checked, other form |
| Lemma 2.2 `lem:connected` |  | none (tacit) | none (map rules in Sec 2) | - | `region_connected` (DiskRegions:74), `connected_shore` (Bonds:163) | none | refereed only |
| Eq. (2.3) `eq:counts` |  | (2.1) | Lemma 1 (counts) | Sec 1 | `cubic_cards` (Matching:477), `black_dual_card` (MinorDuality:179), `euler` (Network:192), `nonroots_card` (BMatching:341) | primal-form | checked, other form |
| Def. 2.4 `def:selection` |  | "one selected edge at each black and white triangle" (Sec 6.1) | perfect matching P of G | - | `connected_complement_matching` (Gluing:294) | primal-form | checked, other form |
| Lemma 2.5(1) `lem:duality.1` |  | Sec 6.2 (Jordan curve labelling) | circuit-cut fact; Lemma 2(a) | background | `circuit_cut` (FlowCircuits:71), `bond_of_circuit` (Bonds:109) | primal-form | checked, other form |
| Lemma 2.5(2) `lem:duality.2` |  | Lemma 2.1 | circuit-cut fact (converse direction) | - | `complement_connected` (Matching:79), `conserved_supported_acyclic` (Matching:68) | weaker | checked, other form |
| Prop. 2.6(1) `prop:target.1` |  | proof of Thm 1.1, last paragraph | Lemma 12, second paragraph | - | `hamiltonian` (Main:13), `complement_connected` (Matching:79), `matching_complement_two` (Gluing:26), `cycle_at_of_connected_two` (CappedDuality:187) | primal-form | checked, other form |
| Prop. 2.6(2) `prop:target.2` |  | Thm 2.2 (two induced trees) | Remark 15 (part) | - | none | none | refereed only |
| Lemma 3.1 `lem:selections-give-states` (off route) |  | none | Remark 15 (stronger: also uniqueness) | - | none | none | refereed only |
| Def. 3.2 `def:state` |  | Sec 2 (state) | Sec 3 (state) | Sec 1 (state) | `State` (TriangleSystem:19), `State` (ColoredDual:46) | exact | checked, exact |
| Def. 3.4 `def:good` |  | Prop 5.1 + Lemma 6.1 (no name) | "circuit-free Q_s" with partner; Remark 14 | Theorem 1 (forest Q_s) | `oppositeGraph` (TriangleSystem:105), `augQ` (Matching:276) | different-form | checked, other form |
| Lemma 3.5 `lem:good` |  | Sec 6.1 ("the remainder is a spanning tree of H") | Lemma 9, first paragraph; Remark 14 | - | `removed_acyclic` (Matching:330), `augQ_acyclic` (Matching:281) | weaker | checked, other form |
| Lemma 3.6 `lem:Y` |  | Sec 6.1 (tree on white faces, rooted at y0) | Lemmas 9 and 10 | - | `remainder_connected` (Matching:342), `remainder_independent` (Matching:487), `remainder_black_degree` (Matching:444), `tree_matching` (ForestMatching:51), `recovery_matching` (ForestMatching:226) | weaker | checked, other form |
| Lemma 3.7 `lem:outdegree` |  | inline in Lemma 5.2, 6.1, 6.2 | inline (Sec 3, Lemma 9) | inline (Lemma 4) | `tail_orientation` (FlowCircuits:255), `addSink_acyclic` (Matching:114) | weaker | refereed only |
|  text `txt:inside` |  | Sec 4, one sentence ("its bounded disk contains no root") | Lemma 2 (cut side, no-pinch) | background | `circuit_cut` (FlowCircuits:71), `connected_shore` (Bonds:163), `region_connected` (DiskRegions:74), `region_euler` (DiskRegions:252), `mixed_corner_on_boundary` (StateDisk:129) | different-form | checked, other form |
| Lemma 3.8 `lem:disk` |  | Lemma 4.1 | Lemma 5 | Lemma 2 | `state_disk_delta` (StateDisk:442), `cycle_disk` (ColoredDual:83), `state_disk_count` (StateDisk:260), `disk_boundary_imbalance` (StateDisk:428), `white_positive_of_boundary` (Circulation:227) | primal-form | checked, other form |
| Prop. 3.9 `prop:recover` |  | Lemma 6.2 and end of Sec 6.2 | Lemmas 11 and 12 | - | `selected_forest` (ForestMatching:338), `selectNet_forest` (ForestMatching:307), `matching_cut_balance` (ForestMatching:176), `recover_connected_complement` (ForestMatching:375) | stronger | checked, other form |
| Def. 4.1 `def:pair` |  | Sec 2 (pair) | Sec 3 (pair) | Sec 1 (pair) | `Partner` (TriangleSystem:82), `Pair` (PairPhases:189) | exact | checked, exact |
| Lemma 4.2 `lem:partner` |  | Lemma 5.2 proof (outdegree) and Lemma 6.1 | Sec 3; Lemma 9; Remark 14 (uniqueness) | Lemma 4 proof | `partner_orientation` (CycleReversal:106), `augQ_acyclic` (Matching:281) | weaker | checked, other form |
|  text `txt:D` |  | Sec 5 (D is a union of vertex-disjoint cycles) | Lemma 8, first paragraph | Sec 2 (D_p) | `next` (PairPhases:204), `CycleClass` (PairPhases:115), `pairedCycle` (Forest:100) | different-form | checked, other form |
| Lemma 4.3 `lem:reversals` |  | Lemma 5.2 proof (1); Sec 5.3 grouping (2) | Lemma 7 proof (1); Lemma 8 (2) | Lemma 4 (1); Lemma 5 case 1 (2) | `reverse` (CycleReversal:171), `reversal_involutive` (CycleReversal:238), `reversal_ne` (CycleReversal:243), `orient` (PairPhases:286), `groupEquiv` (PairPhases:359) | exact | checked, exact |
|  text `txt:delta` |  | Sec 4 (delta) | Sec 2 (delta), Lemma 3 | Sec 2 (delta) | `indexDelta` (TriangleSystem:96), `index_delta` (TriangleSystem:291), `blackDelta` (StateDisk:385), `cycle_disk` (ColoredDual:83) | different-form | checked, other form |
| Lemma 4.4 `lem:sign` |  | (5.1): phase i^J | Lemmas 7-8 (same real sign) | Definition 3 (sign with floor(J/2)) | `phase` (PairPhases:9), `rawIndexSum` (PairPhases:30), `reverse_phase` (PairPhases:81), `phase_add_six` (PairPhases:11), `group_sum_product` (PairPolynomials:238) | none | refereed only |
| Lemma 4.5 `lem:cancel` |  | Lemma 5.2 | Lemma 7 | Lemma 4 | `fixed_second_state_cancels` (PairPhases:91), `opposite_disk` (Forest:200) | different-form | checked, other form |
|  text `txt:heights` |  | Lemma 5.3 (spoke circulations, different weights) | Lemma 6 (integer path flow and local potentials) | rays rho_w and crossings (Sec 1) | `whiteCharge` (Circulation:183), `boundary_of_sum_zero` (Circulation:154), `weights` (ColoredDual:102) | different-form | checked, other form |
| Lemma 4.6 `lem:height` |  | Lemma 5.3 and (5.3) | Lemma 6 | crossing pairing (Lemmas 5-6) | `whiteCharge_cut_integral` (Circulation:208), `signed` (ColoredDual:183), `paired_sign` (Forest:156), `white_positive_of_boundary` (Circulation:227) | weaker | checked, other form |
| Lemma 4.7 `lem:difference` |  | Taylor coefficient of the product (5.4)-(5.5) | Lemma 8 (product of linear polynomials) | Sec 7 (moment comparison, off-route) | `cycle_factor_witness` (PairPolynomials:288), `common_phase_sum_ne_zero` (PairPolynomials:12) | none | refereed only |
| Prop. 4.8 `prop:good` |  | Prop 5.1 | Lemma 8 | Theorem 1 | `forest_pair` (Forest:234), `forest_pair_of_disk_circulation` (PairPolynomials:423), `total_sum_ne_zero` (PairPolynomials:348) | primal-form | checked, other form |
| Remark 4.10 `rem:other-sums` (off route) |  | (5.2) | (6.1) | Sec 7 | `term` (PairPolynomials:224) | none | refereed only |
|  text `txt:flow` |  | Prop 3.1, first paragraph | Lemma 4, first paragraph | - | `two_matchings` (BMatching:286) | exact | checked, exact |
| Eq. (5.1) `eq:hall` |  | (3.1) | (3.1) | - | `state_capacity` (BMatching:378) | primal-form | checked, other form |
| Prop. 5.2 `prop:pair` |  | Prop 3.1 | Lemma 4 (different proof: minimal deficit) | hypothesis | `pair_nonempty` (BMatching:403), `state_capacity` (BMatching:378), `capacity_full` (MinorDuality:220), `induced_density` (MinorDuality:87), `region_density` (MinorDuality:55), `region_balance_rim` (Contraction:223), `rim_defect` (Contraction:273), `rim_three_cut` (Contraction:346), `complement_singleton_root` (Contraction:407), `induced_euler_bound` (Contraction:121) | primal-form | checked, other form |
| Lemma 6.1 `lem:cap` |  | proof of Thm 2.2 (cap colouring) | Lemma 13, first part | - | `threeCut_black_card` (ThreeCuts:367), `cap_coloring` (ThreeCuts:381), `cap_simple` (ThreeCuts:352), `cap_cubic` (ThreeCuts:360), `cap_threeConnected` (ThreeCuts:230), `cap_duality` (CappedDuality:148) | primal-form | checked, other form |
| Thm 6.2 `thm:T` |  | Thm 2.2 | Theorem T (first sentence) | - | `connected_complement_matching` (Gluing:294), `irreducible_matching` (ThreeCuts:109), `cap_matching_boundary` (Gluing:51), `cap_glue_matching` (Gluing:94), `cap_glue_connected` (Gluing:167) | primal-form | checked, other form |
| Remark Sec 7 `rem:which` (off route) |  | none | Remarks 14-15 | - | none | none | refereed only |
| Remark Sec 7 `rem:poly` (off route) |  | (5.4) | (6.3) | - | `group_sum_product` (PairPolynomials:238) | weaker | refereed only |

| primal / involution | Lean | relation | status | merged-paper node |
| --- | --- | --- | --- | --- |
| primal T  | `connected_complement_matching`, `matching_strong`, `main` | primal-form | checked, other form | thm:T |
| primal circuit-cut fact  | `circuit_cut`, `bond_of_circuit`, `connected_shore` | primal-form | checked, other form | lem:duality.1 |
| primal 1 elementary setup | `cubic_cards`, `nonroots_card`, `make_coloredDual` | primal-form | checked, other form | lem:dual |
| primal 2 face circuits and cut-side faces | `circuit_cut`, `connected_shore`, `region_euler`, `mixed_corner_on_boundary` | primal-form | checked, other form | txt:inside |
| primal 3 orientation of a bond | `cycle_cut_scalar`, `blackDelta_cut`, `index_delta` | different-form | checked, other form | txt:delta |
| primal 4 a pair exists in the irreducible case | `pair_nonempty` | exact | checked, exact | prop:pair |
| primal 5 the cut-side identity | `state_disk_count`, `disk_boundary_imbalance`, `state_disk_delta` | exact | checked, exact | lem:disk |
| primal 6 the weights | `boundary_of_sum_zero`, `whiteCharge_cut_integral`, `signed` | exact | checked, exact | lem:height |
| primal 7 cancellation | `fixed_second_state_cancels` | different-form | checked, other form | lem:cancel |
| primal 8 nonvanishing | `total_sum_ne_zero`, `forest_pair_of_disk_circulation` | different-form | checked, other form | prop:good |
| primal 9 the recovery tree | `removed_acyclic`, `remainder_connected`, `remainder_black_degree`, `remainder_independent` | exact | checked, exact | lem:Y |
| primal 10 the selected matching | `tree_matching`, `recovery_matching` | weaker | checked, other form | lem:Y |
| primal 11 matching cut balance | `matching_cut_balance` | exact | checked, exact | prop:recover |
| primal 12 the complement is one cycle | `selectNet_forest`, `selected_forest`, `recover_connected_complement` | exact | checked, exact | prop:recover |
| primal 13 caps and gluing | `cap_simple`, `cap_cubic`, `cap_threeConnected`, `cap_coloring`, `cap_glue_matching`, `cap_glue_connected`, `cap_duality` | primal-form | checked, other form | lem:cap |
| primal 14 the partner is unique when it exists | none | none | unrefereed | lem:partner |
| primal 15 compatible matchings | none | none | unrefereed | lem:selections-give-states |
| involutions 1 Forest-pair lemma | `forest_pair` | primal-form | checked, other form | prop:good |
| involutions 2 Disk identity | `state_disk_delta` | primal-form | checked, other form | lem:disk |
| involutions 3 objects | none | none | unrefereed | txt:heights |
| involutions 4 one | `reversal_involutive`, `reverse_phase` | weaker | unrefereed | lem:cancel |
| involutions 5 two | none | none | unrefereed | prop:good |
| involutions 6 fixed | `common_phase_sum_ne_zero` | none | unrefereed | prop:good |
| involutions 7 walk | none | none | unrefereed |  |
