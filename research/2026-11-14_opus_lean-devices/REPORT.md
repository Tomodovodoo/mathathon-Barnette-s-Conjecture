# Report: the paper's devices, machine-checked on OpenAI's Lean proof

**Summary.**

1. OpenAI's Lean proof still builds at `E:\lbb` (Lean `v4.34.1`, Mathlib `d13f23b7`, `openai/math` at `4eaee875`), and the blueprint's `FiniteDifference.lean` compiles there (`COMPUTED`, `build-logs/`).
2. Lemma 4.4 compiles in the Lean's model: `ε(r,s) = ∏ δ(r(t),s(t))`, both reversals negate it, and `ε = (-1)^((n+c)/2 + c⁺)` with `n ≡ c (mod 2)`. For every pair of the formal proof's concrete system, `ε = i^n · phase`. The ratio is the constant `i^n`, so the reviser was right (`COMPUTED`, machine-checked).
3. Proposition 4.8 compiles by the paper's method (real sign, `ω^m`, finite differences): `Σ ε ω^m ≠ 0` and a pair gives a good state. The hypotheses are the same as in OpenAI's phase-based lemma, and the concrete version needs none.
4. OpenAI's main theorem rebuilds with that one lemma swapped for ours. In the rebuilt proof, `phase` and the polynomial lemmas are unreachable from `main`, and the axioms are still `propext`, `Classical.choice`, `Quot.sound`.
5. Lemma 3.7 (component count, one component) and "a forest has at most one perfect matching" compile in plain Mathlib. Not checked: the paper's heights as such, Lemma 3.7's first sentence and its use for Lemma 4.2, the converse "Hamiltonian cycle ⇒ good state", Lemma 2.2, and Prop. 2.6(2).

## What I set out to do

The brief asked for four things in order:
1. Confirm the build and FiniteDifference.
2. Lemma 4.4 in the Lean's model, with its relation to the Lean's phase.
3. The paper's nonvanishing argument derived from the Lean's lemmas.
4. If time remained, a tree's perfect matching, the good-state remark, or Lemma 3.7.

The sources go in `proofs/lean/` with a README and a blueprint delta.

## What I established

All items are `COMPUTED` in the sense of the protocol: the Lean kernel checked them. The exact commands and outputs are in `build-logs/` and in `proofs/lean/README.md`.

**Build (priority 1).** `~/.elan/bin/lake build` in `E:\lbb` reports `Build completed successfully (8955 jobs)` with nothing to rebuild (`build-logs/lake-build-OAI.log`). Versions are in `build-logs/versions.txt`: Lake `5.0.0-src+5045d00`, Lean `4.34.1` (commit `5045d005`), Mathlib `d13f23b7`. `FiniteDifference.lean` compiles unchanged, in 14 s, with the three standard axioms. One trap: the `lake` on the Git Bash PATH runs Lean 4.28 and fails on Mathlib's lakefile. elan's `lake` works.

**Lemma 4.4 (priority 2), `proofs/lean/Devices/LocalSign.lean`.** The Lean's local sign is `indexDelta i j` on corner indices in `Fin 3`. I defined `paperSign r s = ∏_t indexDelta (r t) (s t)`.
- The `Q_s` reversal (`OppositeCycle.paperSign_reverse`). On the faces of the cycle every factor changes sign (`δ(u,s) = -δ(r,s)`, by `decide`). The number of faces is odd because their `δ`-sum is `±3`. The Lean's own `cyclicDelta` is minus that sum.
- The `D` reversal (`Pair.sign_orient`). Reversing the set `b` of cycles multiplies `ε` by `(-1)^|b|`, through the Lean's `orient` and `CycleClass`.
- The formula (`Pair.sign_formula`). `n = Σδ + 2N` and `Σδ = 3c - 6c⁺` give `2N = n - 3c + 6c⁺`, and `omega` finishes.
- The phase (`I_zpow_rawIndexSum`, `phase_eq_paperSign`, `sign_eq_I_pow_mul_phase`). `i^(Σδ) = i^n ε` holds for any pair. If `3 ∣ Σδ`, which the disk identity on the cycles of `D` gives, then `phase = i^(-n) ε`, that is `ε = i^n · phase`.
- Concrete (`Devices/Concrete.lean`). The Lean's `opposite_disk` and `paired_sign` discharge every hypothesis for its system `M.system root`, so all of the above holds unconditionally there. This settles the referee/reviser question of `research/2026-11-14_opus_cross-audit/ADJUDICATION.md` formally, with the Lean's corner order taken as the orientation. The Lean has no sphere orientation, so it cannot decide between `i^n` and `i^{-n}` relative to a drawing. ADJUDICATION shows the reversed convention gives `i^{-n}`. Either way the ratio is constant.

**Proposition 4.8 by the paper's devices (priority 3), `Devices/RealSign.lean`.**
- Lemma 4.5 with `ε`: `sum_sign_eq_zero_of_no_good`, using the reversal involution and Lemma 4.4.
- Lemma 4.6, additivity: `weight_orient`, which gives `ω(s') = ω(s) + Σ_{reversed} L(C)` for any `ω(s) = Σ_t w(t, s(t))`.
- The class sum: `group_sum`. Through `groupEquiv` and an equivalence between `Bool`-valued functions and finsets, it is `ε(P) · F`, with `F` the repeated difference of Lemma 4.7.
- Its two cases: `0` if `c > m` (`group_sum_lt`), and `(-1)^((n+m)/2+m) m! ∏|L(C_i)|` if `c = m` (`group_sum_card`). The second uses Lemma 4.4's formula and the sign condition. That exponent equals the paper's `(n-m)/2` mod 2.
- Totals: `realSum_ne_zero` and then `forest_pair_of_disk_circulation_real`, which has exactly the binders of OpenAI's `forest_pair_of_disk_circulation`.
- Concrete: `forest_pair_real` has the statement of OpenAI's `ColoredDual.forest_pair`, and an `example` checks the types agree. `realSum_ne_zero_concrete` uses the Lean's flow weights.

**The main theorem through the paper's route.** `proofs/lean/paper-route/make_paper_route.py` copies OpenAI's files `Forest.lean` to `Main.lean` (the tail of the import chain, 17 files) into `PaperRoute/`. It changes one line: the call in `Forest.lean` now goes to `forest_pair_of_disk_circulation_real`. `lake build PaperRoute` succeeds in about 3 minutes. In the rebuilt project, `OAI.Barnette.main : OAI.Barnette.MainStatement` checks, and its axioms are the three standard ones.

I wrote a `#reaches` command that walks the constants in the types and values of `main`. It finds `forest_pair_of_disk_circulation_real`, `realSum_ne_zero`, `paperSign_reverse`, `sign_orient` and `Blueprint.finite_difference`. It does not find `phase`, `Pair.term`, `forest_pair_of_disk_circulation`, `total_sum_ne_zero`, `common_phase_sum_ne_zero` or `fixed_second_state_cancels`. As a control, the same command run on OpenAI's original `main` finds all six (`build-logs/original-route-check.out`). So the complex phase and the polynomial `∏(1 + aX)` can be dropped from a machine-checked proof of Barnette's conjecture. They are replaced by the integer sign and a power of the weight, as in the paper. This is the strongest result here.

**Priority 4.**
- `Devices/Outdegree.lean`, Lemma 3.7 in Mathlib terms. For a connected finite simple graph with every edge directed one way and outdegree at most one: `|E| + γ = |V|`, `γ ≤ 1`, a tree if `γ = 1`. If `γ = 0` it is not acyclic, and deleting any non-bridge edge leaves a tree, which is how I state "exactly one cycle".
- `Devices/TreeMatching.lean`: an acyclic graph has at most one perfect matching. The proof uses Mathlib's `symmDiff_isCycles`: no edge of the symmetric difference is a bridge, while every edge of a forest is one.

**Size.** The new files total 866 lines: LocalSign 350, RealSign 277, Concrete 87, Outdegree 108, TreeMatching 44. The check files add 123 more. FORMALISATION.md had estimated 360 to 500 lines for steps 2 and 4, and they came to 714.

## What failed and why

- Compile errors before the files went through: 5 in LocalSign, 4 in RealSign, 4 in Outdegree, 3 in TreeMatching, over two or three rounds each. All were lemma names (`filter_card_add_filter_neg_card_eq_card` is now `card_filter_add_card_filter_not`, `Set.ncard_pos` takes a finiteness argument), rewrite motives, or a missing `classical`. None needed a change of mathematics.
- `lake build` of the `PaperRoute` library with `roots = ["PaperRoute.Main"]` did not build the imported modules. `globs = ["PaperRoute.+"]` fixed it.
- I did not try the paper's heights (T2). Defining the turn sign `κ_y` needs the cyclic order of the edges at a vertex of `G`, which the Lean only encodes through `ColoredDual.oriented`. That is a separate piece of work. So `realSum_ne_zero_concrete` has the Lean's flow weights as `ω`. The research agent showed numerically that these equal the paper's heights up to sign (`research/2026-11-14_opus_lean-formalisation`, W3), but that is `COMPUTED` on small cases, not machine-checked.

## What is still open

Precise statements are in `proofs/lean/TODO-statements.lean.txt`. That file is not compiled and contains no `sorry`.
- T1: the number of cycles is constant on a class. Then `minCycles` is the paper's `m`.
- T2: the paper's heights are the Lean's weights for one flow.
- T3: Lemma 4.2 from Lemma 3.7 applied to `Q_s`.
- T4: Lemma 3.7's first sentence (every cycle is directed).
- T5: a Hamiltonian cycle avoiding the edge comes from a good state.
- T6: Lemma 2.2 and Prop. 2.6(2). These are out of reach without a Jordan curve theorem.

## Three best next steps

1. **T2, the heights bridge.** It is the last device of Section 4 that is not checked as the paper states it. Build the path flow for each white vertex and show `M.weights α root` differs from `Σ_y κ_y` by a function of `t` only. Then `realSum_ne_zero_concrete` is literally the paper's Proposition 4.8.
2. **Offer the swap upstream as a simplification.** The rebuilt `main` shows the polynomial and complex phase are dispensable. A cleaned version would replace `PairPhases` and `PairPolynomials` by `LocalSign` and `RealSign`. That needs moving the shared definitions `Pair`, `orient`, `cycleDelta` and `cycleSlope` out of `PairPolynomials`, and gives a shorter formal Section 5.
3. **T1 and T3.** Both are short (about 50 lines each, `HUNCH`) and would let the README state the paper's `m` and Lemma 4.2 word for word.

## Leads for others

- **Paper (Section 4 and Remark 4.10).** Remark 4.10's `i^J = i^{-n} ε` is now machine-checked in the Lean's model. The remark could cite `proofs/lean/` and say that OpenAI's phase and polynomial can be removed from their formal proof without other changes.
- **Blueprint owner.** `proofs/lean/BLUEPRINT-DELTA.md` lists the node changes: `lem:sign`, `lem:cancel`, `lem:difference` and `prop:good` to checked-exact; `rem:other-sums` and `lem:outdegree` to checked-form.
- **Cross-audit.** ADJUDICATION's verdict (ratio `i^n`) is confirmed by `ColoredDual.sign_eq_I_pow_mul_phase_concrete`.

## Files

- `build-logs/versions.txt`: Lake, Lean and Mathlib versions.
- `build-logs/lake-build-OAI.log`: `lake build` of OpenAI's 31 files.
- `build-logs/lake-build-Devices-PaperRoute.log`: `lake build Devices PaperRoute`.
- `build-logs/axioms.out`: `lake env lean Devices/Axioms.lean`, 29 theorems.
- `build-logs/paper-route-check.out`, `original-route-check.out`: the checks on the rebuilt and the original `main`.
- Sources, README, delta and TODO: `proofs/lean/`.

Every command was run in `E:\lbb` with `~/.elan/bin/lake`. `E:\lbb` now also contains `Devices/`, `PaperRoute/` (generated), `make_paper_route.py`, and a `lakefile.toml` extended with the `Devices` and `PaperRoute` libraries. The original lakefile is kept as `lakefile.toml.orig`.
