# Lean: the paper's devices on top of OpenAI's formal proof

This folder holds Lean 4 sources that machine-check parts of `paper/main/barnette.tex` (committed text, last changed in `d3b3651`) inside the model of OpenAI's formal proof. Statement numbers are those of the compiled paper (`paper/main/barnette.aux`).

The short version:
- Lemma 4.4 (the sign of a pair as a product of local signs, both reversals, the closed formula), Lemma 4.5 with the real sign, the additivity part of Lemma 4.6, Lemma 4.7 and Proposition 4.8 by `ε · ω^m` and finite differences all compile, first for an abstract triangle system and then for the Lean's concrete system.
- The relation between the real sign and OpenAI's phase compiles: `ε(r,s) = i^n · phase` for every pair of the concrete system. The ratio is the constant `i^n`.
- OpenAI's main theorem `OAI.Barnette.main` rebuilds with its phase-and-polynomial nonvanishing lemma swapped for ours. In the rebuilt proof, `phase` and the polynomial lemmas are no longer reachable from `main`.
- Lemma 3.7 (component count) and "an acyclic graph has at most one perfect matching" compile in plain Mathlib.

Every main result depends only on `propext`, `Classical.choice` and `Quot.sound`. No `sorry`, `admit`, `native_decide` or `axiom` occurs in these files.

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
| `TODO-statements.lean.txt` | | precise statements that are **not** checked; not compiled |

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
| `Pair.sum_sign_eq_zero_of_no_good` | Lemma 4.5, second sentence (the case used) | if no pair has acyclic `Q_s`, then `Σ ε(r,s) F(s) = 0` for every `F` |
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
| **not** reached from `main` | `phase`, `Pair.term`, `forest_pair_of_disk_circulation`, `total_sum_ne_zero`, `common_phase_sum_ne_zero`, `fixed_second_state_cancels` |

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

## What is machine-checked now, and what is not

Checked, in the formal model:
- Lemma 4.4 entire, Lemma 4.5 (with `ε`), Lemma 4.7, Proposition 4.8 by the paper's method, and the `ε`/phase relation of Remark 4.10.
- That the paper's nonvanishing device replaces OpenAI's in the full proof of the main theorem.
- Lemma 3.7 except its first sentence, for one component at a time.
- Uniqueness of a perfect matching in a forest.

Not checked:
- Lemma 4.6 for the paper's **heights**. The additivity is checked for any weight that is a sum of local terms, and the sign condition (`L(C) > 0` on counterclockwise cycles) is the Lean's `paired_sign` for its flow weights. The bridge "the paper's heights are the Lean's weights for one flow" is `TODO-statements` T2.
- `minCycles` is the minimum over one representative per class. Equality with the minimum over all pairs is T1. It does not affect the conclusion.
- Lemma 3.7's first sentence (every cycle is directed, T4), and Lemma 3.7 applied to `Q_s` to recover Lemma 4.2 (T3).
- The converse "a Hamiltonian cycle comes from a good state" (T5), Lemma 2.2 and Prop. 2.6(2) (T6).
- The paper's own objects (sphere, faces, Jordan curve) are not formalised. Everything here lives in the Lean's algebraic-dual model.
