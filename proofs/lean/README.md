# Lean: the paper's devices on top of OpenAI's formal proof

This folder holds Lean 4 sources that machine-check parts of `paper/main/barnette.tex` (version 2, commit `e97b061`; statement numbers are unchanged from version 1) inside the model of OpenAI's formal proof. `opus_lean-devices` wrote and built them. A different model rebuilt them from a fresh clone and audited them theorem by theorem in `research/2026-11-14_astra_lean-check`. Where the two reports differ, this README follows the checker.

What is machine-checked, stated exactly:
- In the Lean's algebraic-dual model, the sign of a pair as a product of local signs, its change under both reversals and its closed formula (Lemma 4.4). Here "counterclockwise" means `δ`-sum `-3`, which the paper uses as its characterisation. The Lean has no drawing to compare with.
- `ε = i^n · phase` for every pair of the concrete system, so OpenAI's phase and the paper's real sign differ by the constant `i^n`.
- Lemma 4.5, first sentence, with the real sign. Of its second sentence only the case where no pair has acyclic `Q_s` is checked: then the signed total is zero. That case is the one the existence proof uses. The identity with a sum over good states and their unique partners is **not** checked.
- Lemma 4.7, for any commutative ring. Proposition 4.8 by `ε · ω^m` and finite differences, with the Lean's flow weights as `ω`, **not** the paper's heights along face paths. The conclusion is a pair whose `Q_s` is acyclic, which is the Lean's stand-in for "a good state".
- OpenAI's main theorem `OAI.Barnette.main`, with its statement unchanged, rebuilds through this route. The rebuilt proof no longer reaches the six named phase and polynomial lemmas (`phase`, `Pair.term`, `forest_pair_of_disk_circulation`, `total_sum_ne_zero`, `common_phase_sum_ne_zero`, `fixed_second_state_cancels`). It still reaches 276 general Mathlib `Polynomial` declarations through the unchanged exact-dual construction, so "no polynomial" is true only of those six lemmas.
- In plain Mathlib: the component count of Lemma 3.7 for one connected graph (without the lemma's first sentence, and not applied to `Q_s`), and "a forest has at most one perfect matching".

Every one of the 29 headline theorems, and the rebuilt `main`, depends only on `propext`, `Classical.choice` and `Quot.sound`. No `sorry`, `admit`, `native_decide`, `axiom` or `set_option` occurs in these files (checker's source scan, 29 files).

Where the build lives: the Lake project was built at `E:\lbb` on the machine where it was made, and the checker's fresh clone was `E:\lb2` (since deleted). Neither is in the repository. To reproduce from a clone of this repository, follow "How to build" below. It takes about 10 minutes plus the Mathlib cache download.

## Upstream and toolchain

- OpenAI's development: `https://github.com/openai/math`, commit `4eaee87548250b2682affda7d05d947c05554bae`, directory `lean/OAI/Combinatorics/Hamiltonian/` (31 files).
- Lean `v4.34.1` (`lean-toolchain`), Lake `5.0.0-src+5045d00`, Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` (`lake-manifest.json` pins all dependencies).
- Built on 14 November 2026 in the Lake project `E:\lbb`. The project needs a short path on Windows because of the 260-character limit. Call `lake` through elan (`~/.elan/bin/lake`), since another `lake` on the Git Bash PATH runs Lean 4.28.

## How to build

1. Make an empty directory at a short path, for example `E:\lbb`, and copy `lakefile.toml`, `lake-manifest.json` and `lean-toolchain` from this folder into it.
2. Copy OpenAI's 31 files from `lean/OAI/Combinatorics/Hamiltonian/` at the commit above to `OAI/Combinatorics/Hamiltonian/` in the project. `ComparatorChallenges/BarnetteHamiltonian.lean` is optional because no target here imports it.
3. Copy `Devices/` from this folder to `Devices/` in the project.
4. Copy `paper-route/make_paper_route.py` to the project root and run `python -I make_paper_route.py`. It writes `PaperRoute/`, which holds copies of OpenAI's files `Forest.lean` through `Main.lean` (17 files, the tail of the linear import chain). Their imports point to `PaperRoute.*`, and the script makes exactly one change: in `Forest.lean` the call `Pair.forest_pair_of_disk_circulation hex` becomes `Pair.forest_pair_of_disk_circulation_real hex`, and the file also imports `Devices.RealSign`. This folder does not contain the copies, because they are OpenAI's code.
5. Run, in the project root:

```
lake exe cache get                      # Mathlib oleans
lake build                              # OpenAI's 31 files (default target OAI)
lake build Devices PaperRoute           # our files, then main rebuilt through our lemma
lake env lean Devices/Axioms.lean       # #print axioms for every result below
lake env lean Devices/PaperRouteCheck.lean     # rebuilt main: statement, axioms, what it reaches
lake env lean Devices/OriginalRouteCheck.lean  # the same check on OpenAI's main (control)
```

The logs of these runs are in `research/2026-11-14_opus_lean-devices/build-logs/`. `PaperRoute` takes about 3 minutes, and each `Devices` file about 10 to 15 seconds.

## Files

| file | lines | content |
| --- | --- | --- |
| `Devices/FiniteDifference.lean` | 94 | Lemma 4.7, from `research/2026-11-14_opus_blueprint/lean/` (unchanged; namespace `Blueprint`) |
| `Devices/LocalSign.lean` | 350 | Lemma 4.4, Lemma 4.5 with `ε`, the relation `ε = i^n · phase` |
| `Devices/RealSign.lean` | 277 | Lemma 4.5 summed, Lemma 4.6 (additivity), Proposition 4.8 by `ε · ω^m` |
| `Devices/Concrete.lean` | 87 | the above for the Lean's concrete system, with no hypotheses left |
| `Devices/Outdegree.lean` | 108 | Lemma 3.7, component count (Mathlib only) |
| `Devices/TreeMatching.lean` | 44 | an acyclic graph has at most one perfect matching (Mathlib only) |
| `Devices/Axioms.lean` | 40 | `#print axioms` for every theorem below |
| `Devices/PaperRouteCheck.lean`, `OriginalRouteCheck.lean` | 44, 39 | a `#reaches` command (transitive constant closure) and the checks on `main` |
| `paper-route/make_paper_route.py` | | generates `PaperRoute/` (step 4) |
| `TODO-statements.lean.txt` | | targets that are **not** checked; not compiled. T5 as first written was false and is replaced |

## Dictionary

| paper | Lean (`OAI.Barnette.TriangleSystem`) |
| --- | --- |
| black face `t ∈ A`, its corners | `t : A`, `T.vertex t : Fin 3 → V` |
| state `s`, pair `(r,s)` | `s : T.State X`, `P : T.Pair X` with `P.left = r`, `P.right = s` |
| `δ(r(t), s(t))` | `indexDelta (r.val t) (s.val t)` (cyclic order of `Fin 3` in each triangle) |
| `ε(r,s) = ∏ δ(r(t),s(t))` | `paperSign r s`, `P.sign` (new) |
| reversal of a cycle of `Q_s` (4.3(1)) | `C.reverse r hrs`, `C : T.OppositeCycle s` |
| reversal of cycles of `D(r,s)` (4.3(2)) | `P.orient b`, `b : CycleClass P.next → Bool` |
| cycles of `D(r,s)`; their `δ`-sums | `CycleClass P.next`; `P.cycleDelta c` |
| counterclockwise cycle of `D` | `P.cycleDelta c = -3` (paper: a counterclockwise cycle of chosen sides has `δ`-sum `-3`) |
| `ω(s)`, with step `L(C)` | `weight w s = Σ_t w t (s t)`; `P.step w c = -P.cycleSlope w c` |
| `Σ = Σ ε(r,s) ω(s)^m` | `realSum w m` (new) |
| OpenAI's `i^J`, `J = (1/3) Σ δ` | `phase (rawIndexSum r s)` |

The Lean does not fix how the cyclic order of `Fin 3` sits on the sphere. So "counterclockwise" in the theorems below means `δ`-sum `-3`, which is how the paper characterises it.

## Theorems and their paper counterparts

Abstract results (any `TriangleSystem`, under the disk-identity hypotheses that the Lean itself uses):

| Lean name | paper | statement |
| --- | --- | --- |
| `OppositeCycle.paperSign_reverse` | Lemma 4.4, first reversal | `ε(r̃, s) = -ε(r, s)` if the cycle of `Q_s` has `δ`-sum `±3` |
| `Pair.sign_orient` | Lemma 4.4, second reversal | reversing the cycles of `D` picked by `b` multiplies `ε` by `(-1)^#b` |
| `Pair.sign_reverse_one` | Lemma 4.4, second reversal | reversing one cycle of `D` negates `ε` |
| `Pair.sign_formula` | Lemma 4.4, formula | `n ≡ c (mod 2)` and `ε = (-1)^((n+c)/2 + c⁺)` |
| `OppositeCycle.paperSign_partners_sum` | Lemma 4.5, first sentence | `Σ_r ε(r, s) • x = 0` over the partners of `s` when `Q_s` has a cycle |
| `Pair.sum_sign_eq_zero_of_no_good` | Lemma 4.5, second sentence, **only** the case used | if no pair has acyclic `Q_s`, then `Σ ε(r,s) F(s) = 0` for every `F` |
| `Pair.weight_orient` | Lemma 4.6, additivity | `ω(s') = ω(s) + Σ_{reversed} L(C)` |
| `Blueprint.finite_difference(_fin)` | Lemma 4.7 | as printed |
| `Pair.group_sum`, `group_sum_lt`, `group_sum_card` | proof of Prop. 4.8 | class sum is `ε · F`; `0` if `c > m`; `(-1)^((n+m)/2+m) m! ∏ |L(C_i)|` if `c = m` |
| `Pair.realSum_ne_zero` | Prop. 4.8, `Σ ≠ 0` | with `m = minCycles` |
| `Pair.forest_pair_of_disk_circulation_real` | Prop. 4.8 | a pair gives a good state; same hypotheses and conclusion as OpenAI's `forest_pair_of_disk_circulation` |
| `Pair.I_zpow_rawIndexSum` | | `i^(Σ δ) = i^n ε`, for any pair |
| `Pair.phase_eq_paperSign`, `paperSign_eq_I_pow_mul_phase`, `sign_eq_I_pow_mul_phase` | Remark 4.10 (`i^J = i^{-n} ε`) | `phase = i^(-n) ε` and `ε = i^n · phase`, given `3 ∣ Σ δ`, which `three_dvd_rawIndexSum` derives from the disk identity on `D` |

The sign `(-1)^((n+m)/2+m)` equals the paper's `(-1)^((n-m)/2)`, because the two exponents differ by `2m`.

Concrete results (`OAI.Barnette.Network.ColoredDual`, the triangle system `M.system root` of the formal proof; the Lean's `opposite_disk` and `paired_sign` discharge the hypotheses):

| Lean name | paper |
| --- | --- |
| `sign_reverse_opposite`, `sign_orient_concrete`, `sign_formula_concrete` | Lemma 4.4, unconditional |
| `sign_eq_I_pow_mul_phase_concrete` | Remark 4.10: `ε(P) = i^n · phase(P)` for every pair |
| `realSum_ne_zero_concrete` | Prop. 4.8, `Σ ε ω^m ≠ 0`, with the Lean's flow weights as `ω` |
| `forest_pair_real` | Prop. 4.8, word for word the statement of OpenAI's `ColoredDual.forest_pair` (an `example` in the file checks the types agree) |

Main theorem through the paper's route (`PaperRoute/`, generated):

| check | output (`build-logs/paper-route-check.out`) |
| --- | --- |
| `#check (OAI.Barnette.main : OAI.Barnette.MainStatement)` | passes; `MainStatement` comes from OpenAI's unchanged `Model.lean` |
| `#print axioms OAI.Barnette.main` | `[propext, Classical.choice, Quot.sound]` |
| reached from `main` | `forest_pair_of_disk_circulation_real`, `realSum_ne_zero`, `paperSign_reverse`, `sign_orient`, `Blueprint.finite_difference` |
| **not** reached from `main` | `phase`, `Pair.term`, `forest_pair_of_disk_circulation`, `total_sum_ne_zero`, `common_phase_sum_ne_zero`, `fixed_second_state_cancels` (general Mathlib `Polynomial` declarations are still reached; see below) |

Control (`build-logs/original-route-check.out`): on OpenAI's own `main`, all six of the last row are reached. So the `#reaches` command does detect them.

Mathlib-only results:

| Lean name | paper |
| --- | --- |
| `Devices.OutOrientation.card_edgeSet_add_sinks`, `component_count` | Lemma 3.7: for a connected graph (a component) with every edge directed and outdegree at most one, `|E| + γ = q`, `γ ≤ 1`, a tree if `γ = 1`, and if `γ = 0` not acyclic and a tree after deleting any non-bridge edge (exactly one cycle) |
| `Devices.IsAcyclic.perfectMatching_unique` | a forest has at most one perfect matching |

## `#print axioms`

All 29 theorems in `Devices/Axioms.lean`, and the rebuilt `main`, print

```
depends on axioms: [propext, Classical.choice, Quot.sound]
```

The full output is in `research/2026-11-14_opus_lean-devices/build-logs/axioms.out`.

## Independently rebuilt and checked

`research/2026-11-14_astra_lean-check` (a different model, no access to the author's build outputs) did the following. Full commands, timings and outputs are in its `BUILD-LOG.md`.

| check | command (cwd `E:\lb2`, a fresh clone) | result |
| --- | --- | --- |
| clone | `git clone --no-checkout https://github.com/openai/math.git E:\lb2`; `git checkout --detach 4eaee87548250b2682affda7d05d947c05554bae` | only `.lake/packages` copied from `E:\lbb`; no OAI, Devices or PaperRoute build output reused; the 9 dependency repositories match `lake-manifest.json` |
| inputs | `inputs-sha256.json` | the 19 submitted files hashed; they still match the files in this folder (rechecked by `opus_lean-integration`) |
| upstream | `C:\Users\Tom\.elan\bin\lake.exe build` | 8,955 jobs, exit 0 (first run interrupted at 438 s by design, resumed 259 s) |
| this folder | `python -I make_paper_route.py`; `lake.exe build Devices PaperRoute` | 8,963 jobs, exit 0, 206 s; generated `Main.lean` changes only its import, `Forest.lean` one call and one import |
| axioms | `lake.exe env lean Devices/Axioms.lean` | all 29 and the rebuilt `main`: `[propext, Classical.choice, Quot.sound]` (`AXIOMS.txt`) |
| statements | `lake.exe env lean Statements.lean`, `Definitions.lean` | elaborated types of all 29 match the README; `OAI.Barnette.main : OAI.Barnette.MainStatement` from the unchanged `Model.lean` |
| nonvacuity | `lake.exe env lean Nonvacuity.lean` | a three-face triangle system with a pair, and both sign values occur |
| dependencies | `IndependentWalker.lean`, `OriginalCheck.lean`, `ReplacementCheck.lean` (the checker's own walker, not `#reaches`) | original `main` reaches 36,722 constants and all six phase/polynomial lemmas; rebuilt `main` 36,345 and none of them, but 276 Mathlib `Polynomial` declarations (`REACHABILITY.md`, `PathCheck.lean` gives a path to `Polynomial.eval₂_add`) |
| sign | `python -I numerical.py`; `SIGN-CHECK.md` | `ε / phase = i^n` proved by hand; all 174,763 admissible sign words up to length 18 and all 136 pairs in every face rooting of two triangulations pass |
| faithfulness | `FAITHFULNESS.md` | 29 verdicts: faithful or stronger for all except `sum_sign_eq_zero_of_no_good` (weaker), `weight_orient`, `realSum_ne_zero`, `realSum_ne_zero_concrete` (different: flow weights, nonzero only) and `component_count` (weaker) |
| TODO | `COUNTEREXAMPLE.md` | T5 false (hexagonal prism); see `TODO-statements.lean.txt` |

The checker found no failure in any compiled theorem. Its corrections concern this README's wording, now fixed: Lemma 4.5 in full, "no polynomial", and the direction of the positive step (positive when reversing a clockwise cycle).

## What is machine-checked now, and what is not

Checked, in the formal model, and independently rebuilt:
- Lemma 4.4 (both reversals and the closed formula), with "counterclockwise" read as `δ`-sum `-3`.
- Lemma 4.5, first sentence; the second sentence in the case no pair has acyclic `Q_s`.
- Lemma 4.7; Proposition 4.8 by the paper's method, with flow weights.
- `ε = i^n · phase` (the phase sentence of Remark 4.10).
- That this route replaces OpenAI's phase-and-polynomial nonvanishing argument in the proof of the unchanged main theorem.
- Lemma 3.7's count and its tree and one-cycle conclusions, for one connected graph.
- Uniqueness of a perfect matching in a forest.

Not checked:
- Lemma 4.6 for the paper's **heights along face paths**. Additivity is checked for any weight that is a sum of local terms, and the step `L(C) > 0` holds for the Lean's flow weights when a **clockwise** cycle is reversed (`paired_sign`). The bridge "the heights are the weights of one flow, up to a constant per face" is T2.
- Lemma 4.5's identity with the sum over good states and their unique partners (T10), partner uniqueness (T8), and "acyclic `Q_s` with a partner means one root per component" (T7).
- `minCycles` is the minimum over one representative per class. Equality with the minimum over all pairs is T1. It does not affect the conclusion.
- Lemma 3.7's first sentence (T4), and Lemma 3.7 applied to `Q_s` (T3).
- Which Hamiltonian cycles arise (T5, corrected), the explicit `P_s` (T9), Lemma 2.2 and Prop. 2.6(2) (T6), the paper's gluing (T12).
- The paper's own objects: the drawing, faces, the Jordan curve theorem, the prescribed avoided edge in the drawn theorem (T11). Everything here lives in the Lean's algebraic-dual model.
