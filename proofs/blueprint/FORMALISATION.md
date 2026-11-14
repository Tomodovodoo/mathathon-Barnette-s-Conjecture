# Machine-checking the merged paper's route: a feasibility note

Summary.
1. Keep the Lean development's model of planarity, the algebraic dual. Formalising the paper's topological lemmas literally (Lemma 2.2, the inside of a cycle as a plane graph) would first need a Jordan curve theorem, which Mathlib `d13f23b7` does not have.
2. On top of that model, the merged paper's route differs from the Lean in six places. About 7,300 of the Lean's 8,936 lines can be reused unchanged. The routes differ only inside Circulation, PairPhases, PairPolynomials, Forest and Gluing (1,670 lines).
3. The new work is the sign as a product, heights as a path flow, nonvanishing through `omega^m`, the outdegree component count, the explicit rooting of `Y_s` and the two-tree gluing. By analogy with the existing files, that is about 900 to 1,500 new lines, replacing about 600 to 900 old ones.
4. One piece is done: Lemma 4.7 (finite differences), 90 lines, compiled (`research/2026-11-14_opus_blueprint/lean/FiniteDifference.lean`).
5. The order below lets each step compile and be checked against `main` before the next one starts.

Status of this note: a plan with estimates (HUNCH for the line counts, by analogy with the existing proof). Nothing here except Lemma 4.7 has been compiled.

## What "the merged route" means formally

The target is a Lean proof of `OAI.Barnette.MainStatement`, as `main` proves it, whose intermediate declarations state the merged paper's lemmas in the translation of BLUEPRINT.md (bridges B1 to B5). The objects stay the Lean's: `Network`, `Duality`, `ColoredDual`, `TriangleSystem`. A triangle of `T` is the star of a vertex of `G`, and the inside of a cycle is the root-free shore of a bond. This is a choice, and I recommend it for two reasons.
- No Jordan curve theorem is needed. A grep of Mathlib `d13f23b7` for "jordan curve" finds nothing (COMPUTED), so the topological route would start with a large prerequisite. The Lean's `exists_exact_dual` (1,078 lines) already turns a drawing into an algebraic dual using only compactness and grid cells.
- The paper's two topological statements then have exact algebraic stand-ins that are already proved. Lemma 2.2, as it is used, is `Duality` connectivity plus `region_connected`; the inside of `Z` is `circuit_cut` plus `Bond.connected_shore`, `region_euler` and `mixed_corner_on_boundary`. Restating Lemma 2.2 literally is out of scope for this plan.

## Files that can be reused unchanged

Line counts are raw lines at commit `4eaee875`.

| group | files | lines | role in the merged route |
| --- | --- | --- | --- |
| statement | Model | 50 | the target |
| algebraic duality | Network, CutSpaces, FlowCircuits, Bonds, Quotients | 1,441 | Lemma 2.5, the inside of a cycle |
| disk identity | DiskRegions, StateDisk | 801 | Lemma 3.8 (exact match, h = 2l + 3) |
| triangle systems, reversals | TriangleSystem, ColoredDual, CycleReversal | 778 | Defs 3.2 and 4.1, Lemmas 4.2 and 4.3 |
| a pair exists | Contraction, MinorDuality, BMatching | 1,101 | Prop. 5.2 and the max-flow paragraph (Hall in place of max-flow; keep it) |
| recovery | Matching, ForestMatching | 904 | Lemmas 3.5 and 2.5(2), Prop. 3.9 (`selected_forest` is stronger than the paper) |
| caps | ThreeCuts, CappedDuality | 717 | Lemma 6.1 |
| embedding to dual | Traces, SquareGrid, Corridors, MinorModel, BranchPartition, Rectangle, ExactDual | 1,388 | "fix an embedding" |
| top | Main | 86 | Theorem 1.1 |

Total reused unchanged: about 7,270 lines, minus `Gluing` if step 5 below replaces the gluing. `Circulation` (253 lines) stays because the heights are one of its flows. `PairPhases` (369) and `PairPolynomials` (450) can stay as they are; the new nonvanishing argument goes beside them, not in their place, until it works.

## The new pieces, in order

Each step names the statement in `paper/main/barnette.tex`, the Lean it builds on, and an estimate. Estimates are by analogy with Lean proofs of similar shape in the same development, quoted with their sizes.

**Step 1. Lemma 4.7, finite differences. Done.** `Blueprint.finite_difference` and `Blueprint.finite_difference_fin`, 90 lines, compiled with Lean v4.34.1 and Mathlib `d13f23b7` in a Lake project with only Mathlib. Axioms: `propext`, `Classical.choice`, `Quot.sound`. It is stated for any finite index set and any commutative ring. Proof: induction on the index set, using `Finset.sum_powerset_insert` and `add_pow`. The `k = 0` term cancels and the others vanish by the induction hypothesis. It took one compile.

**Step 2. Lemma 4.4, the sign as a product of local signs.** Define `eps r s := ∏ t, (indexDelta (r t) (s t) : ℤ)` on a `TriangleSystem`. Prove:
- (2a) a `Q_s` reversal negates `eps`. The pieces exist: `reverse_rawIndexSum_diff` gives the raw difference `2 * cyclicDelta`, and `cyclicDelta = ±3` (the `hdisk` hypothesis) forces an odd number of changed factors, each of which changes sign by `same_third_corners`-type facts in PairPhases. About 60 lines, comparable to `reverse_rawIndexSum_diff` (29) plus `reverse_phase` (9).
- (2b) on the group of a pair, `eps (orient P b) = const * (-1)^(number of flipped bits)`. Comparable to `group_sum_product` (26 lines) with `bits_invariant`. About 50 lines.
- (2c) optional, to link to the old development: `eps = i^n * phase (rawIndexSum)` (bridge B2), about 40 lines, using the per-cycle delta sums of `paired_sign` and the factorisation in `group_sum_product`.

**Step 3. Heights as a path flow (bridge B3, Lemma 4.6 summed).** For each white vertex `y` of `G`, take a walk from `y` to the root (`G.Connected` from `Duality`); its edge indicator, with signs, is a flow with boundary `1_y - 1_root`. Sum over `y` to get `alpha` with `N.boundary alpha = whiteCharge M.black root`. Then `ColoredDual.weights alpha` are the heights up to constants, and `whiteCharge_cut_integral` gives `omega(s') - omega(s) = #white faces inside` with no new argument. The per-white-face statement of Lemma 4.6 is not needed. About 80 to 120 lines. `boundary_of_sum_zero` (28 lines) proves existence non-constructively; this step builds a specific flow, so it is longer.

**Step 4. Proposition 4.8 by `omega^m`.** This is the main new proof. Define `Sigma := ∑ P : Pair, eps P * (omega P.right)^m` with `omega s := ∑ t, a t (s t)` and `m` the least number of `D`-cycles over all pairs (a `Nat.find`). Then:
- (4a) cancellation: pairs whose second state has a cycle in `Q_s` sum to zero. `fixed_second_state_cancels` is stated for any `C`-module and the phase. Restate it for `eps` with an integer weight, or derive it from step 2c. About 30 lines.
- (4b) on each group, `omega (orient P b) = omega_0 + ∑_{bits set} L_c` with `L_c` the slope of cycle `c`. `omega` is additive over triangles and the cycles partition the triangles, so this follows from `group_values`. About 80 lines.
- (4c) each group with `c` cycles contributes `0` if `m < c` and `(-1)^{(n-m)/2} m! ∏ L_c` if `m = c` (step 1 plus step 2b). About 60 lines.
- (4d) sum over groups: every group has `c >= m`, at least one has `c = m`, and every `L_c >= 1` (`paired_sign`, `white_positive_of_boundary`), so `Sigma ≠ 0`. `total_sum_ne_zero` (37 lines) plus `common_phase_sum_ne_zero` (38) is the analogue. About 80 lines.

Together about 250 to 350 lines, against `PairPolynomials` (450) for the Lean's version. The integer version may come out shorter because it needs no complex numbers and no polynomial coefficients.

**Step 5. The two-tree gluing (Prop. 2.6(2) and the second half of Theorem 6.2).** State, for a perfect matching `P` of `G` with `G - P` connected: in `D` restricted to `P`, an edge of `D` has both ends in one component exactly when it lies in `P`, and there are two components. Proof as in the paper, with cycles of `D` as bonds (`circuit_cut`) and a cycle meeting a cut evenly. Then rewrite the gluing step of `matching_strong` to glue acyclic selections. About 150 to 250 lines, compared with `cap_glue_connected` (48) plus `cap_matching_boundary` (12) and the bookkeeping in `matching_strong` (47). **Recommendation**: do not do this step. Change the paper instead, to glue matchings as `cap_glue_connected` does; the paper already says (Section 6, after the proof) that this is Li's form of the argument. Then Prop. 2.6(2) leaves the route.

**Step 6. Lemma 3.7, the component count.** For a directed graph on `V` with outdegree at most one, a connected component with `q` vertices and `gamma` sinks has `q - gamma` edges. Use Mathlib's `SimpleGraph.Connected.card_vert_le_card_edgeSet_add_one` and `IsTree.card_edgeFinset`. About 40 to 60 lines, comparable to `addSink_acyclic` (36). Then Lemma 4.2 (one root per tree of `Q_s`) and the last paragraph of Prop. 3.9 can be restated as in the paper. Optional: `augQ_acyclic` already does the job in the Lean.

**Step 7. The explicit selection `P_s` (Lemma 3.6).** Root the tree `Y_s` at the root vertex, and let every white vertex select its parent edge. Prove that this is a perfect matching containing `e`, as primal Lemma 10 does in five sentences. It replaces `tree_matching` (98 lines, Hall). About 100 to 150 lines, because rooted trees in Mathlib take some setup (`SimpleGraph.IsTree.existsUnique_path`). Optional: only needed if the formal proof should construct `P_s` rather than prove one exists.

## Totals

| step | statement | new lines (estimate) | needed for the merged route? |
| --- | --- | --- | --- |
| 1 | Lemma 4.7 | 90 (done) | yes |
| 2 | Lemma 4.4 | 110 to 150 | yes |
| 3 | heights, Lemma 4.6 | 80 to 120 | yes |
| 4 | Prop. 4.8 by `omega^m` | 250 to 350 | yes |
| 5 | two-tree gluing | 150 to 250 | only if the paper keeps its gluing |
| 6 | Lemma 3.7 | 40 to 60 | optional |
| 7 | explicit `P_s` | 100 to 150 | optional |

Steps 1 to 4 cover every device in which the merged paper's nonvanishing argument differs from the Lean: 530 to 710 new lines, of which 90 exist. With steps 5 to 7: 820 to 1,170. For comparison, the whole development is 8,936 raw lines (7,015 counted), and its Sections 5 and 6 (cancellation, nonvanishing, recovery) took 1,314 + 660 counted lines (earlier analysis, `graph/effort.md`).

## How to start

1. Make a Lake project with only Mathlib at a short path (Windows' 260-character limit broke the build inside the repository; `research/2026-11-14_opus_lean-formalisation/build/README.md`). The existing one at `E:\lbb` works. Call `lake` through elan (`~/.elan/bin/lake`); the `lake` earlier on the Git Bash PATH is another wrapper and fails on Mathlib's lakefile.
2. Copy the 31 files of `lean/OAI/Combinatorics/Hamiltonian/` at `4eaee875` and `research/2026-11-14_opus_blueprint/lean/FiniteDifference.lean`. Add new files after `PairPolynomials` in the import chain (`PairSigns.lean` for step 2, `Heights.lean` for step 3, `PowerSum.lean` for step 4).
3. Prove `ColoredDual.forest_pair'` with the same statement as `ColoredDual.forest_pair` (Forest:234) by the new route, switch `irreducible_matching` to it, and check that `#print axioms OAI.Barnette.main` is unchanged. This is the test that the new route closes.
4. Keep the merged paper's numbering in docstrings (`/-- Lemma 4.4 of paper/main/barnette.tex -/`), so that `blueprint.json` can be regenerated with exact declarations in place of nearest ones.
