# Blueprint of the Barnette proofs

Summary.
1. The route to Theorem 1.1 in `paper/main/barnette.tex` has 34 nodes: 26 numbered statements (two of them split into their parts, giving 28 nodes) and six load-bearing claims made in running text. For 29 of them the Lean proof at `openai/math@4eaee875` contains a declaration with the same content. Four are exact; 25 match only after a translation (triangulation to algebraic dual, sign to phase, heights to flow) that is itself not machine-checked.
2. Five statements on the route have no machine-checked counterpart: Lemma 2.2 (faces bounded by cycles give a connected graph), Proposition 2.6(2) (two induced trees), the component count in Lemma 3.7, Lemma 4.4 (the sign as a product of local signs) and Lemma 4.7 (finite differences). I proved Lemma 4.7 in Lean here; it compiles against Mathlib (`research/2026-11-14_opus_blueprint/lean/FiniteDifference.lean`).
3. Matching statements does not mean matching routes. Most of the paper's proofs differ from the Lean's: the sign, the weights, the nonvanishing argument, the explicit rooting of the tree and the gluing all use other devices. Measured in proof words, 90% of the route's proof text sits in statements with a formal counterpart, but only ten proofs follow the Lean argument.
4. The logical skeleton is a 10-step chain from the definition of a state through the cancellation and the sign to Theorem 6.2. Nothing is used before it is proved. Four items are never used for Theorem 1.1: Lemma 3.1, Remark 4.10 and the two proved remarks of Section 7.
5. The primal note matches the Lean most closely: 6 of its 17 statements have exact counterparts. The involution note is a different proof of Proposition 5.1 (OpenAI) and only its theorem and disk lemma have counterparts.

Files: `blueprint.json` (nodes and edges), `blueprint.dot` and `blueprint.{pdf,svg,png}` (dependency graph of the merged paper), `columns.dot` and `columns.{pdf,svg,png}` (five-column correspondence chart), `FORMALISATION.md` (what it would take to check the merged route), `README.md` (how to rebuild). The extraction scripts are in `research/2026-11-14_opus_blueprint/scripts/`.

## Sources and versions

| column | source | version |
| --- | --- | --- |
| merged paper | `paper/main/barnette.tex` | commit `b0fc398` (last change `3d3dea1`), the text refereed FOLLOWS in `research/2026-11-14_sol_referee-main/` |
| primal note | `proofs/primal/primal.tex` | commit `b0fc398` (last change `048615a`); refereed FOLLOWS in `research/2026-11-14_fable_referee-primal/` before the revision; Remarks 14 and 15 were added after that referee |
| involution note | `proofs/involutions/involutions.tex` | commit `b0fc398` (last change `8397461`); refereed FOLLOWS in `research/2026-11-14_opus_referee-involutions/` (commit `45c4cea`) |
| OpenAI paper | `papers/OpenAI-Barnette.pdf` (text dump `papers/text/OpenAI-Barnette.txt`) | 24 September 2026 |
| Lean | `github.com/openai/math`, `lean/OAI/Combinatorics/Hamiltonian/` | commit `4eaee87548250b2682affda7d05d947c05554bae`, re-cloned into `research/2026-11-14_opus_blueprint/upstream/` (not committed); every cited header is in `research/2026-11-14_opus_blueprint/data/lean-sigs.json` |

While I worked, other agents were editing `paper/main/barnette.tex` and `proofs/involutions/involutions.tex` in the working tree (uncommitted). I extracted both versions. The working-tree paper has the same 31 numbered statements with the same numbers and labels. The changes are renamed symbols and lemma statements made self-contained (Lemmas 3.7 and 3.8); one text paragraph (the one on `D(r,s)`) was reworded. None of this changes the graph. The working-tree involution note adds one statement (`path-crossings`, a variant with paths in place of rays), which is off the proof route. Rerun `extract_tex.py --worktree` to compare again.

## How to read the status

Every statement of the merged paper gets one status. The vocabulary is the one the brief asks for.

| status | meaning | colour |
| --- | --- | --- |
| machine-checked counterpart, exact | a Lean declaration states the same proposition, up to notation | dark green |
| machine-checked counterpart in different form | a Lean declaration states an equivalent or stronger proposition once a stated translation is applied; the translation is not machine-checked | light green |
| refereed by a second model only | no Lean declaration states it or anything equivalent; the nearest one is weaker or uses another device | orange |
| unrefereed | not read by an independent referee | red |

The relation column says how the Lean statement compares: `exact`, `primal-form` (same content stated on the cubic graph `G` or the algebraic dual), `different-form` (same content with another device), `stronger`, `weaker`, `none`. "Weaker but covered" means the Lean proves less than the paper states, but proves the part the route uses. The `bridge` and `gap` fields of `blueprint.json` say exactly what is missing in each case.

"Machine-checked" here is a claim about statements. The previous Lean analysis built the development and printed its axioms (`research/2026-11-14_opus_lean-formalisation/build/`, COMPUTED there). I did not rebuild it. I did compile my own file `lean/FiniteDifference.lean`.

## The honest answer: how much of the exposition is formally verified

On the route to Theorem 1.1 (34 nodes):

| status | count | statements |
| --- | --- | --- |
| exact | 4 | Def. 3.2 state, Def. 4.1 pair, Lemma 4.3 two reversals, the max-flow paragraph of Section 5 (as `BMatching.two_matchings`) |
| different form | 25 | everything else not listed below |
| no counterpart | 5 | Lemma 2.2, Prop. 2.6(2), Lemma 3.7 (component count), Lemma 4.4, Lemma 4.7 (now proved in Lean here) |

Off the route: Lemma 3.1, Remark 4.10 and the two proved remarks of Section 7 have no counterpart. Remark "the polynomial behind the count" is a generalisation of `Pair.group_sum_product`.

Three caveats make "25 in different form" weaker than it sounds.

**The translations are informal.** Five translations carry all 25. None of them is a Lean declaration.
- (B1) *Triangulation to algebraic dual.* The faces of `T` are the vertices of `G`. The inside of a cycle of `T` is the root-free shore of a bond of `G` (`Duality.circuit_cut`). "Counterclockwise" is the sign `c` in `cycleFlow = c * gradient(1_A)`. Used by Lemmas 2.1, 2.5, 3.8, the text on the inside of `Z`, Proposition 5.2 and Lemma 6.1.
- (B2) *Sign to phase.* The paper's `eps(r,s) = prod delta(r(t),s(t))` equals `i^n * phase(rawIndexSum r s)` (primal STATUS.md, PROVED-HERE there). Lemma 4.5 is checked only with the phase. This translation is exactly the missing Lemma 4.4.
- (B3) *Heights to flow.* Summing unit path flows from each white face to `t0` gives a flow with boundary `whiteCharge`. The heights `kappa` are then the potentials `ColoredDual.weights` up to one constant per black triangle, and those constants cancel on every cycle. Used by Lemma 4.6.
- (B4) *Good state to "second state of a pair with acyclic Q_s".* The Lean never names good states. Used by Definition 3.4, Lemmas 3.5 and 4.2, Proposition 4.8.
- (B5) *Drawing to algebraic dual.* Theorem 1.1 with the prescribed edge is proved in Lean only for graphs with an algebraic dual (`Duality.connected_complement_matching`). Combining it with `PlaneEmbedding.exists_exact_dual` would take a few lines, but nobody has written them (DIFFERENCES.md item 27 of the earlier analysis).

**Routes differ.** The Lean proof follows the paper's argument for ten statements on the route: Def. 2.4, Prop. 2.6(1), Lemma 3.8, Prop. 3.9, Defs. 3.2 and 4.1, Lemma 4.3, Lemma 4.5, the capacity condition (5.1) and Prop. 5.2 (the density argument; per component in the paper, global in Lean). Everywhere else the conclusion is checked and the paper's proof is not. The sharpest case is Theorem 6.2. Its statement is checked, but its proof glues acyclic selections through Prop. 2.6(2), which is not formalised; the Lean glues perfect matchings with connected complements (`cap_glue_connected`) and never needs the two-tree structure.

**Weaker but covered.** Five Lean counterparts prove less than the paper states: Lemma 2.5(2) (no spanning-tree sentence), Lemma 3.5 (one direction), Lemma 3.6 (Hall gives some matching inside `Y_s`, not the paper's `P_s`), Lemma 4.2 (no uniqueness of the partner) and Lemma 4.6 (only the sum over white faces, not the jump at each face). In each case the route uses only the part that is checked.

Measured in proof words (`proof_words` in `blueprint.json`): the route has 5,626 words of proof, and 5,040 of them (90%) prove statements with a counterpart. The five uncovered statements have 586 words of proof. Lemma 4.7 accounts for 101 of those words and is now checked here.

## Correspondence table

One row per statement of the merged paper, in reading order. "text" rows are claims made in running text that later proofs use. Lean entries give the short name and `file:line` at `4eaee875`; full names and headers are in `blueprint.json` and `research/2026-11-14_opus_blueprint/data/lean-sigs.json`.

| merged paper | statement | OpenAI | primal note | involution note | Lean (file:line) | relation | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Thm 1.1 `thm:main` | Hamiltonian cycle avoiding e | Thm 1.1 + Cor 7.1 | Theorem T | - | `main` (Main:47), `connected_complement_matching` (Gluing:294), `exists_exact_dual` (ExactDual:116) | primal-form | checked, other form |
| Lemma 2.1 `lem:dual` | the dual is a coloured triangulation | proof of Thm 1.1 (Sec 7, paragraphs 1-2) | Lemma 1; last paragraph of proof of Thm T | - | `cut_card_three` (CutSpaces:51), `simple_dual_edge` (ThreeCuts:37), `cubic_face_triangles_edge` (ThreeCuts:82), `make_coloredDual` (ThreeCuts:101), `black_dual_card` (MinorDuality:179) | primal-form | checked, other form |
|  text `txt:two-faces` | two faces share <= 1 side | tacit | Lemma 1 (two faces share at most one edge) | - | `TriangleSystem` (TriangleSystem:9), `system` (ColoredDual:29) | primal-form | checked, other form |
| Lemma 2.2 `lem:connected` | faces bounded by cycles => connected | none (tacit) | none (map rules in Sec 2) | - | `region_connected` (DiskRegions:74), `connected_shore` (Bonds:163) | none | refereed only |
| Eq. (2.3) `eq:counts` | k black, k white, 3k edges, k+2 vertices | (2.1) | Lemma 1 (counts) | Sec 1 | `cubic_cards` (Matching:477), `black_dual_card` (MinorDuality:179), `euler` (Network:192), `nonroots_card` (BMatching:341) | primal-form | checked, other form |
| Def. 2.4 `def:selection` | selection | "one selected edge at each black and white triangle" (Sec 6.1) | perfect matching P of G | - | `connected_complement_matching` (Gluing:294) | primal-form | checked, other form |
| Lemma 2.5(1) `lem:duality.1` | cycle in N => dual disconnected | Sec 6.2 (Jordan curve labelling) | circuit-cut fact; Lemma 2(a) | background | `circuit_cut` (FlowCircuits:71), `bond_of_circuit` (Bonds:109) | primal-form | checked, other form |
| Lemma 2.5(2) `lem:duality.2` | N acyclic => dual connected | Lemma 2.1 | circuit-cut fact (converse direction) | - | `complement_connected` (Matching:79), `conserved_supported_acyclic` (Matching:68) | weaker | checked, other form |
| Prop. 2.6(1) `prop:target.1` | acyclic selection => HC | proof of Thm 1.1, last paragraph | Lemma 12, second paragraph | - | `hamiltonian` (Main:13), `complement_connected` (Matching:79), `matching_complement_two` (Gluing:26), `cycle_at_of_connected_two` (CappedDuality:187) | primal-form | checked, other form |
| Prop. 2.6(2) `prop:target.2` | two induced trees | Thm 2.2 (two induced trees) | Remark 15 (part) | - | none | none | refereed only |
| Lemma 3.1 `lem:selections-give-states` (off route) | HC => state | none | Remark 15 (stronger: also uniqueness) | - | none | none | refereed only |
| Def. 3.2 `def:state` | state | Sec 2 (state) | Sec 3 (state) | Sec 1 (state) | `State` (TriangleSystem:19), `State` (ColoredDual:46) | exact | checked, exact |
| Def. 3.4 `def:good` | good state | Prop 5.1 + Lemma 6.1 (no name) | "circuit-free Q_s" with partner; Remark 14 | Theorem 1 (forest Q_s) | `oppositeGraph` (TriangleSystem:105), `augQ` (Matching:276) | different-form | checked, other form |
| Lemma 3.5 `lem:good` | good <=> S_s spanning tree | Sec 6.1 ("the remainder is a spanning tree of H") | Lemma 9, first paragraph; Remark 14 | - | `removed_acyclic` (Matching:330), `augQ_acyclic` (Matching:281) | weaker | checked, other form |
| Lemma 3.6 `lem:Y` | tree Y_s and selection P_s | Sec 6.1 (tree on white faces, rooted at y0) | Lemmas 9 and 10 | - | `remainder_connected` (Matching:342), `remainder_independent` (Matching:487), `remainder_black_degree` (Matching:444), `tree_matching` (ForestMatching:51), `recovery_matching` (ForestMatching:226) | weaker | checked, other form |
| Lemma 3.7 `lem:outdegree` | outdegree <= 1 | inline in Lemma 5.2, 6.1, 6.2 | inline (Sec 3, Lemma 9) | inline (Lemma 4) | `tail_orientation` (FlowCircuits:255), `addSink_acyclic` (Matching:114) | weaker | refereed only |
|  text `txt:inside` | inside of a cycle (R_Z) | Sec 4, one sentence ("its bounded disk contains no root") | Lemma 2 (cut side, no-pinch) | background | `circuit_cut` (FlowCircuits:71), `connected_shore` (Bonds:163), `region_connected` (DiskRegions:74), `region_euler` (DiskRegions:252), `mixed_corner_on_boundary` (StateDisk:129) | different-form | checked, other form |
| Lemma 3.8 `lem:disk` | disk identity | Lemma 4.1 | Lemma 5 | Lemma 2 | `state_disk_delta` (StateDisk:442), `cycle_disk` (ColoredDual:83), `state_disk_count` (StateDisk:260), `disk_boundary_imbalance` (StateDisk:428), `white_positive_of_boundary` (Circulation:227) | primal-form | checked, other form |
| Prop. 3.9 `prop:recover` | P_s acyclic | Lemma 6.2 and end of Sec 6.2 | Lemmas 11 and 12 | - | `selected_forest` (ForestMatching:338), `selectNet_forest` (ForestMatching:307), `matching_cut_balance` (ForestMatching:176), `recover_connected_complement` (ForestMatching:375) | stronger | checked, other form |
| Def. 4.1 `def:pair` | pair | Sec 2 (pair) | Sec 3 (pair) | Sec 1 (pair) | `Partner` (TriangleSystem:82), `Pair` (PairPhases:189) | exact | checked, exact |
| Lemma 4.2 `lem:partner` | partner orients Q_s | Lemma 5.2 proof (outdegree) and Lemma 6.1 | Sec 3; Lemma 9; Remark 14 (uniqueness) | Lemma 4 proof | `partner_orientation` (CycleReversal:106), `augQ_acyclic` (Matching:281) | weaker | checked, other form |
|  text `txt:D` | D(r,s) = disjoint cycles | Sec 5 (D is a union of vertex-disjoint cycles) | Lemma 8, first paragraph | Sec 2 (D_p) | `next` (PairPhases:204), `CycleClass` (PairPhases:115), `pairedCycle` (Forest:100) | different-form | checked, other form |
| Lemma 4.3 `lem:reversals` | two reversals | Lemma 5.2 proof (1); Sec 5.3 grouping (2) | Lemma 7 proof (1); Lemma 8 (2) | Lemma 4 (1); Lemma 5 case 1 (2) | `reverse` (CycleReversal:171), `reversal_involutive` (CycleReversal:238), `reversal_ne` (CycleReversal:243), `orient` (PairPhases:286), `groupEquiv` (PairPhases:359) | exact | checked, exact |
|  text `txt:delta` | delta, delta-sum = -/+3 | Sec 4 (delta) | Sec 2 (delta), Lemma 3 | Sec 2 (delta) | `indexDelta` (TriangleSystem:96), `index_delta` (TriangleSystem:291), `blackDelta` (StateDisk:385), `cycle_disk` (ColoredDual:83) | different-form | checked, other form |
| Lemma 4.4 `lem:sign` | sign = product of local signs | (5.1): phase i^J | Lemmas 7-8 (same real sign) | Definition 3 (sign with floor(J/2)) | `phase` (PairPhases:9), `rawIndexSum` (PairPhases:30), `reverse_phase` (PairPhases:81), `phase_add_six` (PairPhases:11), `group_sum_product` (PairPolynomials:238) | none | refereed only |
| Lemma 4.5 `lem:cancel` | cancellation | Lemma 5.2 | Lemma 7 | Lemma 4 | `fixed_second_state_cancels` (PairPhases:91), `opposite_disk` (Forest:200) | different-form | checked, other form |
|  text `txt:heights` | heights along face paths | Lemma 5.3 (spoke circulations, different weights) | Lemma 6 (integer path flow and local potentials) | rays rho_w and crossings (Sec 1) | `whiteCharge` (Circulation:183), `boundary_of_sum_zero` (Circulation:154), `weights` (ColoredDual:102) | different-form | checked, other form |
| Lemma 4.6 `lem:height` | height jump = white faces inside | Lemma 5.3 and (5.3) | Lemma 6 | crossing pairing (Lemmas 5-6) | `whiteCharge_cut_integral` (Circulation:208), `signed` (ColoredDual:183), `paired_sign` (Forest:156), `white_positive_of_boundary` (Circulation:227) | weaker | checked, other form |
| Lemma 4.7 `lem:difference` | finite difference [Lean: here] | Taylor coefficient of the product (5.4)-(5.5) | Lemma 8 (product of linear polynomials) | Sec 7 (moment comparison, off-route) | `cycle_factor_witness` (PairPolynomials:288), `common_phase_sum_ne_zero` (PairPolynomials:12) | none | refereed only |
| Prop. 4.8 `prop:good` | a pair gives a good state | Prop 5.1 | Lemma 8 | Theorem 1 | `forest_pair` (Forest:234), `forest_pair_of_disk_circulation` (PairPolynomials:423), `total_sum_ne_zero` (PairPolynomials:348) | primal-form | checked, other form |
| Remark 4.10 `rem:other-sums` (off route) | other sums | (5.2) | (6.1) | Sec 7 | `term` (PairPolynomials:224) | none | refereed only |
|  text `txt:flow` | capacity => pair (max-flow) | Prop 3.1, first paragraph | Lemma 4, first paragraph | - | `two_matchings` (BMatching:286) | exact | checked, exact |
| Eq. (5.1) `eq:hall` | capacity condition | (3.1) | (3.1) | - | `state_capacity` (BMatching:378) | primal-form | checked, other form |
| Prop. 5.2 `prop:pair` | no separating triangle => pair | Prop 3.1 | Lemma 4 (different proof: minimal deficit) | hypothesis | `pair_nonempty` (BMatching:403), `state_capacity` (BMatching:378), `capacity_full` (MinorDuality:220), `induced_density` (MinorDuality:87), `region_density` (MinorDuality:55), `region_balance_rim` (Contraction:223), `rim_defect` (Contraction:273), `rim_three_cut` (Contraction:346), `complement_singleton_root` (Contraction:407), `induced_euler_bound` (Contraction:121) | primal-form | checked, other form |
| Lemma 6.1 `lem:cap` | caps | proof of Thm 2.2 (cap colouring) | Lemma 13, first part | - | `threeCut_black_card` (ThreeCuts:367), `cap_coloring` (ThreeCuts:381), `cap_simple` (ThreeCuts:352), `cap_cubic` (ThreeCuts:360), `cap_threeConnected` (ThreeCuts:230), `cap_duality` (CappedDuality:148) | primal-form | checked, other form |
| Thm 6.2 `thm:T` | acyclic selection containing e0 | Thm 2.2 | Theorem T (first sentence) | - | `connected_complement_matching` (Gluing:294), `irreducible_matching` (ThreeCuts:109), `cap_matching_boundary` (Gluing:51), `cap_glue_matching` (Gluing:94), `cap_glue_connected` (Gluing:167) | primal-form | checked, other form |
| Remark Sec 7 `rem:which` (off route) | which HCs arise | none | Remarks 14-15 | - | none | none | refereed only |
| Remark Sec 7 `rem:poly` (off route) | polynomial F(w) | (5.4) | (6.3) | - | `group_sum_product` (PairPolynomials:238) | weaker | refereed only |

The primal and involution notes, with the Lean declarations and the merged-paper statement each one corresponds to:

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
| involutions 3 objects | none | none | refereed only | txt:heights |
| involutions 4 one | `reversal_involutive`, `reverse_phase` | weaker | refereed only | lem:cancel |
| involutions 5 two | none | none | refereed only | prop:good |
| involutions 6 fixed | `common_phase_sum_ne_zero` | none | refereed only | prop:good |
| involutions 7 walk | none | none | refereed only |  |

## Statements with no machine-checked counterpart

For each one: the nearest formal lemma and how far away it is.

**Lemma 2.2 (faces bounded by cycles give a connected graph).** Used three times: for Euler's formula on `T` (2.3), for the inside of a cycle `R_Z` before Lemma 3.8, and for the pieces in Lemma 6.1. The Lean has no plane graphs, so nothing can state it. The nearest lemmas are `region_connected` (DiskRegions:74, the region network of a connected shore is connected) and `Bond.connected_shore` (Bonds:163). Those state connectivity of an algebraic object built from a vertex set of `G`, not of a plane graph, so the distance is a change of objects, not a missing step. Connectivity of `T` is a field of `Duality`, and connectivity of the pieces comes from `Duality.minor`. This Mathlib has no Jordan curve theorem (COMPUTED: `grep -ri "jordan curve"` over Mathlib d13f23b7 finds nothing), so a literal formalisation of the lemma's proof would need one first.

**Proposition 2.6(2) (an acyclic selection is a forest with two components, and an edge is selected exactly when its ends lie in one component).** This is OpenAI's Theorem 2.2 in the form of two induced trees. The Lean never states it (earlier analysis, DIFFERENCES.md items 22 and 28). The merged paper uses it twice: in the gluing step of Theorem 6.2 and for Lemma 3.1. Nearest: `Duality.circuit_cut` (a cycle in `P` would be a cut) and `cap_matching_boundary` (exactly one edge of a 3-cut lies in a perfect matching). Distance: a counting argument on `D` restricted to `P`, perhaps 150 to 250 Lean lines (FORMALISATION.md, step 5). Alternatively the paper could glue matchings as the Lean does, and this statement would leave the route.

**Lemma 3.7 (outdegree at most one).** The first sentence (every cycle is directed) is `CycleCoordinates.tail_orientation` (FlowCircuits:255), which is exact for one cycle. The component count (`q - gamma` edges, so at most one sink, a tree if exactly one) is not formalised. The Lean avoids it with `addSink_acyclic` (Matching:114): add two root sides pointing into the third root and conclude acyclicity. The paper uses the count in Lemma 4.2 (each tree of `Q_s` has one root) and in Proposition 3.9 (each component of `P_0` has one root). Close: 30 to 60 lines on top of Mathlib's `SimpleGraph.IsTree.card_edgeFinset`.

**Lemma 4.4 (the sign as a product of local signs).** The Lean has no real sign. It uses `phase (rawIndexSum r s) = I ^ (sum delta div 3)` (PairPhases:9 and :30) and proves the two facts it needs: a `Q_s` reversal negates the phase (`reverse_phase`, PairPhases:81), and the phase factorises over the cycles of `D` (`group_sum_product`, PairPolynomials:238). The distance is the identity `eps = i^n * phase` (bridge B2), which needs `3 | sum delta` from the disk identity on every `D`-cycle. The pieces exist (`paired_sign` gives every `D`-cycle delta-sum `-3` or `3`). Estimate 60 to 120 lines. The paper's own proof, which counts the factors `-1` on each cycle, is just as short to formalise directly.

**Lemma 4.7 (finite differences).** The Lean never forms `omega^m`. It writes each class of pairs as a product of polynomials `X * q_C` with `q_C(0) > 0` (`cycle_factor_witness`, PairPolynomials:288) and reads off the lowest coefficient (`common_phase_sum_ne_zero`, :12). Mathlib has the one-step versions (`fwdDiff_iter_pow_eq_zero_of_lt`, `fwdDiff_iter_eq_factorial` in `Algebra/Group/ForwardDiff.lean`), with a single common step. The paper needs `c` different steps. **Proved in Lean here**: `Blueprint.finite_difference` (any finite index set, any commutative ring) and `Blueprint.finite_difference_fin` (the paper's form over `Fin c`), 90 lines, `research/2026-11-14_opus_blueprint/lean/FiniteDifference.lean`. It compiled with Lean v4.34.1 and Mathlib `d13f23b7`, and `#print axioms` gives `[propext, Classical.choice, Quot.sound]` (COMPUTED, output in `FiniteDifference.out`). It is a standalone file and is not connected to the OpenAI development.

Off the route:
- **Lemma 3.1** (a Hamiltonian cycle avoiding `e` gives a state): no counterpart; the Lean never goes back from a cycle to a state. Primal Remark 15 proves a stronger statement (also uniqueness), unrefereed.
- **Remark 4.10** (other sums): no counterpart. The merged-paper referee noted that `sum eps z^omega` is a Laurent polynomial, not an integer polynomial, since `omega` can be negative (Table 4.2 has `omega = -4`).
- **Section 7, "which Hamiltonian cycles arise"** and **"the polynomial behind the count"**: no counterpart for the first. `Pair.group_sum_product` is the second after substituting `w_(t,v) = 1 + a(t,v) X`, with the phase in place of the sign.

## The logical skeleton

The skeleton is everything Theorem 1.1 depends on: 34 of the 38 non-example nodes, all except Lemma 3.1 and the three remarks. Drawn with the transitive reduction, the uses graph of the merged paper is `blueprint.pdf`.

The longest chain of uses, from a definition to the theorem, has ten steps:

`Def. 3.2 state` -> `Def. 4.1 pair` -> `Lemma 4.2 partner orients Q_s` -> `text: D(r,s) is a union of cycles` -> `Lemma 4.3 two reversals` -> `Lemma 4.4 sign` -> `Lemma 4.5 cancellation` -> `Prop. 4.8 a pair gives a good state` -> `Thm 6.2` -> `Thm 1.1`.

The chain runs through the uncovered Lemma 4.4. Following the Lean's route instead, the same depth is reached through `reverse_phase` and the chain is checked.

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

None in the refereed version. Every cited label is proved earlier in the text, apart from Theorem 1.1, which is stated in the introduction and proved at the end, as intended. Lemma 3.1 comes before Definition 3.2 but does not use it: it proves the two properties that the definition then names.

Uses that the proofs make without a reference (all listed in `implicit_uses`):
- Prop. 3.9 uses the disk identity by name, without `\ref`.
- The heights paragraph says "such a path exists because `G` is connected". For an arbitrary coloured triangulation this is Lemma 2.5(2) with `N` empty; the paper does not say so.
- Lemma 3.6 and Prop. 5.2 use "two faces share at most one side" from the text after Lemma 2.1.
- The paragraph on the inside of `Z` says the outside of `Z` is "an open disk", which is the Schoenflies theorem. Only the Jordan curve theorem is needed: the outside is a connected open set with boundary `Z`.

## Five-column chart

`columns.pdf` has one row per waypoint, 18 in all, from the statement through the disk identity and the cancellation to the gluing. Each row shows the OpenAI section, the merged-paper statements, the primal lemmas, the involution lemmas and the Lean declarations, with the same colours. Two rows show the routes splitting. In "nonvanishing" the merged paper has Lemma 4.7 and Prop. 4.8, the primal note its Lemma 8, the involution note the fixed points of its second involution, and the Lean `total_sum_ne_zero`: four different arguments for the same conclusion. The last row, "construct a forest pair", has an entry only in the involution note (Lemma 7, the alternating path).
