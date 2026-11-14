/-
The paper's devices in the concrete system of the Lean proof (github.com/openai/math, commit
4eaee875): the triangle system `M.system root` of a coloured dual `M : N.ColoredDual D` with a
root `root`, where the Lean proves the disk identity for every cycle of `Q_s` (`opposite_disk`) and
for every cycle of `D(r, s)` with its flow weights (`paired_sign`). With these, the hypotheses of
`Devices.LocalSign` and `Devices.RealSign` are discharged.
-/
import OAI.Combinatorics.Hamiltonian.Forest
import Devices.RealSign

namespace OAI.Barnette.Network.ColoredDual

open scoped Classical
open Barnette.TriangleSystem

variable {V E F : Type*} [Fintype V] [Fintype E] [Fintype F]
  {N : Network V E} {D : Network F E} (M : N.ColoredDual D) {root : V}

omit [Fintype F] in
/-- A flow with the white charge exists (as in the Lean's `forest_pair`). -/
theorem exists_white_flow : ∃ α : E → ℝ, N.boundary α = whiteCharge M.black root :=
  N.boundary_of_sum_zero M.duality.connected (whiteCharge M.black root)
    (whiteCharge_sum M.black root)

/-- The disk identity on the cycles of `D(r, s)`, for every pair of the concrete system. -/
theorem pair_cycle_disk (P : (M.system root).Pair (M.nonroots root)) (c : CycleClass P.next) :
    P.cycleDelta c = 3 ∨ P.cycleDelta c = -3 := by
  obtain ⟨α, hα⟩ := M.exists_white_flow (root := root)
  rcases M.paired_sign P c α hα with ⟨h, _⟩ | ⟨h, _⟩
  · exact Or.inr h
  · exact Or.inl h

/-- **Lemma 4.4, first reversal, concrete.** Reversing a cycle of `Q_s` changes `ε`. -/
theorem sign_reverse_opposite {s r : M.State root} (C : (M.system root).OppositeCycle s)
    (hrs : (M.system root).Partner r s) :
    paperSign (C.reverse r hrs) s = -paperSign r s := by
  obtain ⟨α, hα⟩ := M.exists_white_flow (root := root)
  exact C.paperSign_reverse r hrs (M.opposite_disk C ⟨r, hrs⟩ α hα)

/-- **Lemma 4.4, second reversal, concrete.** Reversing the cycles of `D(r, s)` selected by `b`
multiplies `ε` by `(-1)^(number of reversed cycles)`. -/
theorem sign_orient_concrete (P : (M.system root).Pair (M.nonroots root))
    (b : CycleClass P.next → Bool) :
    (P.orient b).val.sign = (-1) ^ (Finset.univ.filter (fun c => b c = true)).card * P.sign :=
  P.sign_orient (M.pair_cycle_disk P) b

/-- **Lemma 4.4, formula, concrete.** `n ≡ c (mod 2)` and `ε = (-1)^((n+c)/2 + c⁺)`. -/
theorem sign_formula_concrete (P : (M.system root).Pair (M.nonroots root)) :
    Even (Fintype.card (M.Black root) + Fintype.card (CycleClass P.next)) ∧
      P.sign = (-1) ^ ((Fintype.card (M.Black root) + Fintype.card (CycleClass P.next)) / 2 +
        P.ccwCount) :=
  P.sign_formula (M.pair_cycle_disk P)

/-- **Real sign versus phase, concrete.** For every pair of the Lean's concrete system,
`ε(r, s) = i^n · phase(Σ δ)`, with `n` the number of non-root black faces. So OpenAI's phase is the
real sign times the constant `i^(-n)`, and `Σ_P ε(P) F(P) = i^n Σ_P phase(P) F(P)` for every `F`. -/
theorem sign_eq_I_pow_mul_phase_concrete (P : (M.system root).Pair (M.nonroots root)) :
    (P.sign : ℂ) = Complex.I ^ Fintype.card (M.Black root) *
      phase (rawIndexSum P.left P.right) :=
  P.sign_eq_I_pow_mul_phase (M.pair_cycle_disk P)

/-- **Proposition 4.8, concrete, by the paper's route.** The statement of the Lean's
`ColoredDual.forest_pair`, proved with the real sign, `ω^m` and finite differences instead of the
phase and the polynomial `∏ (1 + a X)`. -/
theorem forest_pair_real (hex : Nonempty ((M.system root).Pair (M.nonroots root))) :
    ∃ P : (M.system root).Pair (M.nonroots root),
      ((M.system root).oppositeGraph P.right).IsAcyclic := by
  obtain ⟨α, hα⟩ := M.exists_white_flow (root := root)
  exact Pair.forest_pair_of_disk_circulation_real hex
    (fun _ C r => M.opposite_disk C r α hα) (M.weights α root)
    (fun P c => M.paired_sign P c α hα)

/-- The two proofs have literally the same statement: this `example` typechecks the Lean's
`forest_pair` against the type of `forest_pair_real`. -/
example : (Nonempty ((M.system root).Pair (M.nonroots root)) →
    ∃ P : (M.system root).Pair (M.nonroots root),
      ((M.system root).oppositeGraph P.right).IsAcyclic) :=
  fun hex => M.forest_pair hex

/-- **The paper's signed sum is nonzero in the concrete system** with the Lean's flow weights. -/
theorem realSum_ne_zero_concrete (hex : Nonempty ((M.system root).Pair (M.nonroots root)))
    (α : E → ℝ) (hα : N.boundary α = whiteCharge M.black root) :
    realSum (T := M.system root) (X := M.nonroots root) (M.weights α root)
      (Pair.minCycles hex) ≠ 0 :=
  Pair.realSum_ne_zero hex (M.weights α root) (fun P c => M.paired_sign P c α hα)

end OAI.Barnette.Network.ColoredDual
