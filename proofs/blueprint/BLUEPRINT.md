# Blueprint of the Barnette proofs

Summary (version 2, 14 November 2026).
1. The route to Theorem 1.1 in `paper/main/barnette.tex` (version 2, commit `e97b061`) has 34 nodes: 26 numbered statements, two of them split into parts, and six load-bearing claims in running text. Statement numbers are the same as in version 1.
2. Against the Lean, after an independent rebuild and audit (`research/2026-11-14_astra_lean-check`): **5 exact, 17 after an unformalised translation, 10 for a weaker or different form, 2 with no counterpart.** Version 1 counted 4 exact, 25 "different form" and 5 none. The checker's own advisory recount, 5 / 27 / 2, is the same count with the middle two classes merged.
3. The two with no counterpart are Lemma 2.2 (faces bounded by cycles give a connected graph) and Prop. 2.6(2) (two induced trees). Three statements left the "none" class because of Lean added in `proofs/lean/Devices` and rebuilt by the checker: Lemma 4.4 (after translation), Lemma 4.7 (exact) and Lemma 3.7 (weaker: the component count without the first sentence).
4. Of the 32 with a counterpart, 24 have only upstream counterparts (OpenAI's 31 files at `4eaee875`), 4 only project counterparts and 4 use both. The project's Lean rebuilds OpenAI's unchanged `main` through the paper's sign and finite differences. It does so with the Lean's flow weights in place of the paper's heights, and it proves Lemma 4.5 only in the case the existence proof uses.
5. Measured in proof words, the route has 5,668. Of these, 401 sit in exact statements, 3,470 in statements after translation, 1,539 in weaker ones and 258 in the two with no counterpart. Matching statements still does not mean matching proofs. Theorem 6.2's statement has a counterpart, but its gluing goes through Prop. 2.6(2), which has none.

Files: `blueprint.json` (nodes and edges, with `status`, `status_v1`, `origin`, `translation`, `weaker_how`), `blueprint.dot` and `blueprint.{pdf,svg,png}` (dependency graph coloured by status, with the origin of the Lean counterpart on a third line), `columns.dot` and `columns.{pdf,svg,png}` (five-column chart), `FORMALISATION.md` (what remains to machine-check Section 4 as written), `README.md` (how to rebuild). The version 2 scripts are in `research/2026-11-14_opus_lean-integration/scripts/`. The statement-by-statement change from version 1 is `research/2026-11-14_opus_lean-integration/STATUS-TABLE.md`.

## Sources and versions

| column | source | version |
| --- | --- | --- |
| paper | `paper/main/barnette.tex` | version 2, commit `e97b0614eb3c` (read with `git show`); `extract_tex.py --worktree` reports no number mismatch against `barnette.aux` |
| primal note | `proofs/primal/primal.tex` | same commit |
| involution note | `proofs/involutions/involutions.tex` | same commit; it now has eight statements (Lemma 7 `path-crossings` added, the alternating path is Lemma 8), both off the route |
| OpenAI paper | `papers/OpenAI-Barnette.pdf` | 24 September 2026 |
| Lean, upstream | `github.com/openai/math`, `lean/OAI/Combinatorics/Hamiltonian/` | commit `4eaee87548250b2682affda7d05d947c05554bae`; headers in `research/2026-11-14_opus_lean-integration/data/lean-sigs-upstream.json` (689 declarations, identical to version 1's extraction) |
| Lean, added here | `proofs/lean/Devices/` | the files the checker hashed and built (all 19 input hashes in `astra_lean-check/inputs-sha256.json` still match); headers in `data/lean-sigs-devices.json` (58 declarations) |
| independent check | `research/2026-11-14_astra_lean-check/` | fresh clone at `4eaee875`, Lean 4.34.1, Mathlib `d13f23b7`; `FAITHFULNESS.md` (29 verdicts), `REACHABILITY.md`, `RECOUNT.md`, `COUNTEREXAMPLE.md` |

## How to read the status

| status | meaning | colour |
| --- | --- | --- |
| exact | a Lean declaration states the same proposition, given the upstream definitions of state and pair | dark green |
| after translation | a Lean declaration states the proposition in the Lean's algebraic-dual model; the dictionary to the paper's drawing (named B1 to B5 below) is informal | light green |
| weaker or different | a Lean declaration states part of the proposition, or a different one the Lean route can use; `weaker_how` says what is missing | yellow |
| none | no Lean counterpart; the statement is refereed by a second model only | salmon |

Origin, shown on the third line of each node: `upstream` (OpenAI's files only), `added here, rebuilt` (`proofs/lean/Devices` only), `upstream + added here`. The project's files were written by `opus_lean-devices` and rebuilt from a fresh clone by a different model in `astra_lean-check`, which printed the axioms of all 29 headline theorems and of the rebuilt `main` (`propext`, `Classical.choice`, `Quot.sound`).

Where the author's Lean report and the checker disagree, the checker's verdict is used. Three cases: Lemma 4.5 (the author's README said all of it; the checker found only the no-good-pair case of the second sentence), Lemma 3.7 (the first sentence is not in `component_count`), and "no polynomial" (true only of the six named phase and polynomial lemmas; general Mathlib `Polynomial` declarations are still reached).

## The translations

None of them is a Lean declaration.
- (B1) *Drawing to algebraic dual.* The faces of `T` are the vertices of `G`. The inside of a cycle of `T` is the root-free shore of a bond of `G` (`Duality.circuit_cut`). "Counterclockwise" is the sign `c` in `cycleFlow = c * gradient(1_A)`, and on chosen sides it is "delta-sum `-3`". Carries 15 of the 17 statements after translation.
- (B2) *Sign to phase.* **Now checked**: `sign_eq_I_pow_mul_phase_concrete` proves `eps = i^n * phase` for every pair of the concrete system, and the checker confirmed it independently (`SIGN-CHECK.md`; 174,763 sign words and 136 actual pairs). B2 is no longer a translation anyone has to trust.
- (B3) *Heights to flow weights.* The paper's heights along face paths should be the potentials of one flow with boundary `whiteCharge`, up to one constant per black face. Not formalised (TODO T2). This is why Lemma 4.6 and the heights paragraph are "weaker", and why Prop. 4.8 is checked with flow weights.
- (B4) *Good state to "second state of a pair with acyclic `Q_s`".* The Lean never defines one root per component. The checker's hexagonal-prism example shows that acyclic `Q_s` alone is not enough: the partner is essential (`COUNTEREXAMPLE.md`).
- (B5) *Prescribed edge.* Theorem 1.1 with the avoided edge is proved only for graphs with an algebraic dual (`Duality.connected_complement_matching`). `OAI.Barnette.main` states Hamiltonicity without it.

## The two Lean reports compared

| claim | author (`opus_lean-devices`) | checker (`astra_lean-check`) | used here |
| --- | --- | --- | --- |
| all 29 theorems and the rebuilt `main` use only the three standard axioms | yes | confirmed from a fresh clone | yes |
| rebuilt `main` no longer reaches the six named phase and polynomial lemmas | yes | confirmed by an independent dependency walk | yes |
| "no polynomial" | stated without qualification | 276 general Mathlib `Polynomial` declarations are still reached, through the unchanged exact-dual construction | only the six named lemmas |
| Lemma 4.5 | "Lemma 4.5 with `eps`" | first sentence faithful; second sentence only when no pair has acyclic `Q_s` | weaker |
| Lemma 3.7 | "except its first sentence" | weaker; also not applied to `Q_s` | weaker |
| Prop. 4.8 | "by the paper's method" | faithful in the Lean model; flow weights, not heights; `m` is a minimum over class representatives | after translation (B3, B4) |
| TODO T5 | proposed converse | **false**; hexagonal prism, four eligible cycles, two good states | marked false in `proofs/lean/TODO-statements.lean.txt` |

## Correspondence table

`+` marks a declaration added in `proofs/lean/Devices`.

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

## Statements with no Lean counterpart

**Lemma 2.2 (faces bounded by cycles give a connected graph).** Used for Euler's formula on `T` (2.3), for the inside `R_Z` before Lemma 3.8 and for the pieces in Lemma 6.1. The Lean has no plane graphs. The nearest lemmas, `region_connected` and `Bond.connected_shore`, state connectivity of an algebraic object built from a vertex set of `G`. Connectivity of `T` is a field of `Duality`, and that of the pieces comes from `Duality.minor`. Mathlib `d13f23b7` has no Jordan curve theorem (version 1 grep; the checker did not repeat this search).

**Proposition 2.6(2) (two induced trees).** OpenAI's Theorem 2.2. Used by the gluing in Theorem 6.2 and by Lemma 3.1. The Lean glues perfect matchings with connected complement (`cap_glue_connected`) and never needs it. If the paper glued matchings too, Prop. 2.6(2) and Lemma 3.1 would leave the route and the count would become 5 / 17 / 10 / 1 on 33 nodes.

Off the route: Lemma 3.1 has no counterpart. Remark 4.10 has one for its phase sentence (`sign_eq_I_pow_mul_phase_concrete`), but its Taylor and Laurent statements are not formalised. "Which Hamiltonian cycles arise" has only `perfectMatching_unique`. The image characterisation is not stated, and the converse proposed as TODO T5 is false. "The polynomial behind the count" has the upstream `group_sum_product` after the substitution `w = 1 + aX`, with the phase.

## The logical skeleton

The skeleton is everything Theorem 1.1 depends on: 34 of the 38 non-example nodes, all except Lemma 3.1 and the three remarks. Drawn with the transitive reduction, the uses graph of the merged paper is `blueprint.pdf`.

The longest chain of uses, from a definition to the theorem, has ten steps:

`Def. 3.2 state` -> `Def. 4.1 pair` -> `Lemma 4.2 partner orients Q_s` -> `text: D(r,s) is a union of cycles` -> `Lemma 4.3 two reversals` -> `Lemma 4.4 sign` -> `Lemma 4.5 cancellation` -> `Prop. 4.8 a pair gives a good state` -> `Thm 6.2` -> `Thm 1.1`.

The chain runs through Lemma 4.4, which now has a Lean counterpart (`paperSign_reverse`, `sign_orient`, `sign_formula`, added in `proofs/lean/Devices`). Every link of the chain except Lemma 4.2 and Lemma 4.5 is exact or after translation; those two are weaker in Lean (no one-root-per-component, no partner uniqueness, and the cancellation only in the case the existence proof uses).

The shortest way from the hypotheses to the theorem is the direct reduction of Theorem 6.2: Prop. 5.2 (a pair) -> Prop. 4.8 (a good state) -> Prop. 3.9 (an acyclic selection), then Lemma 6.1 and Prop. 2.6(2) for the gluing, then Lemma 2.1 and Prop. 2.6(1) for Theorem 1.1. Everything else feeds one of these seven. In the transitive reduction:

| statement | direct uses after reduction |
| --- | --- |
| Thm 1.1 | Thm 6.2 (the proof also cites Lemma 2.1 and Prop. 2.6(1), which Thm 6.2 already uses) |
| Thm 6.2 | Prop. 5.2, Prop. 4.8, Prop. 3.9, Lemma 6.1, Prop. 2.6(2) |
| Prop. 5.2 | max-flow paragraph, (2.3), two-faces claim, Lemma 2.1 |
| Prop. 4.8 | Lemmas 4.5, 4.6, 4.7 |
| Prop. 3.9 | Lemma 3.6, Lemma 3.8, Prop. 2.6(1) |
| Lemma 3.8 | the inside of `Z`, Lemma 3.7, Def. 3.2 |

## Proved but not used for Theorem 1.1

These are candidates to cut or to mark as asides:
- Lemma 3.1 (Hamiltonian cycle gives a state). It motivates the definition of a state and feeds only the Section 7 remark. It needs Prop. 2.6(2).
- Remark 4.10 and the two proved remarks of Section 7.
- Parts of statements that the route does not use: the uniqueness of the partner in Lemma 4.2; the converse direction of Lemma 3.5; the regrouped formula in Lemma 4.5 (Prop. 4.8 only needs "pairs whose second state has a cycle cancel"); the jump at each single white face in Lemma 4.6 (only the sum is used); the spanning-tree half of Lemma 2.5(2) is used once, in Lemma 3.6.
- Prop. 2.6(2) is used on the route only by the gluing. If the paper glued matchings as the Lean does, Prop. 2.6(2) and Lemma 3.1 could both move to the remarks.

## Used before proved

None in version 2. Every cited label is proved earlier in the text, apart from Theorem 1.1, which is stated in the introduction and proved at the end, as intended. Lemma 3.1 comes before Definition 3.2 but does not use it.

Version 2 fixed three of the four implicit uses that version 1 left without a reference. Prop. 3.9 now cites the disk identity, the heights paragraph cites Lemma 2.5(2) with `N` empty, and the inside paragraph uses only the Jordan curve theorem. Lemma 3.6 and Prop. 5.2 still use "two faces share at most one side" from the text after Lemma 2.1 without a reference (listed in `implicit_uses`).

## Five-column chart

`columns.pdf` has one row per waypoint, 19 in all (version 2 adds a row for Lemma 3.7), from the statement through the disk identity and the cancellation to the gluing. Each row shows the OpenAI section, the merged-paper statements, the primal lemmas, the involution lemmas and the Lean declarations, with the same colours. Two rows show the routes splitting. In "nonvanishing" the merged paper has Lemma 4.7 and Prop. 4.8, the primal note its Lemma 8, the involution note the fixed points of its second involution, and the Lean both OpenAI's `forest_pair` and the project's `forest_pair_real`, which proves it by the paper's method. In the Lean column, blue cells marked `+` are the project's declarations and grey cells are upstream. The last row, "construct a forest pair", has an entry only in the involution note (Lemma 8, the alternating path).
