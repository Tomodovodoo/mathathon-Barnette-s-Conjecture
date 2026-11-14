/-
Lemma 4.4 of paper/main/barnette.tex (the sign of a pair), in the model of
github.com/openai/math, commit 4eaee875 (`OAI.Barnette.TriangleSystem`).

Dictionary (paper -> Lean):
* black face `t ∈ A`, its corners          -> `t : A`, `T.vertex t : Fin 3 → V`
* state `s`, pair `(r, s)`                  -> `s : T.State X`, `P : T.Pair X` (`P.left = r`, `P.right = s`)
* local sign `δ(r(t), s(t))`                -> `indexDelta (r.val t) (s.val t)` (cyclic order of `Fin 3`)
* `ε(r, s) = ∏_t δ(r(t), s(t))`             -> `paperSign r s` (defined here)
* reversal of a cycle `K` of `Q_s` (4.3(1)) -> `C.reverse r hrs`, `C : T.OppositeCycle s`
* reversal of cycles of `D(r, s)` (4.3(2))  -> `P.orient b`, `b : CycleClass P.next → Bool`
* cycles of `D(r, s)`                        -> `CycleClass P.next` (cycles of the permutation `r⁻¹ ∘ s`)
* `δ`-sum along a cycle of `D`               -> `P.cycleDelta c`
* the disk identity on a cycle (`δ`-sum ±3) -> the hypotheses `hdisk` (the Lean proves them for its
                                               concrete system in `Forest.lean`, `opposite_disk`, `paired_sign`)
* OpenAI's phase `i^J`, `J = (1/3) Σ δ`      -> `phase (rawIndexSum r s)`
-/
import OAI.Combinatorics.Hamiltonian.PairPolynomials

namespace OAI.Barnette

open Finset

/-! ### Products of signs -/

/-- A product of `±1` is `(-1)^k` with `k` the number of `-1` factors, and the sum of the same
factors is the number of factors minus `2k`. -/
theorem prod_sum_of_signs {ι : Type*} (S : Finset ι) (f : ι → ℤ)
    (hf : ∀ i ∈ S, f i = 1 ∨ f i = -1) :
    ∏ i ∈ S, f i = (-1) ^ (S.filter (fun i => f i = -1)).card ∧
      (S.card : ℤ) = ∑ i ∈ S, f i + 2 * (S.filter (fun i => f i = -1)).card := by
  classical
  induction S using Finset.induction_on with
  | empty => simp
  | @insert j S hj ih =>
    obtain ⟨h1, h2⟩ := ih (fun i hi => hf i (mem_insert_of_mem hi))
    rw [prod_insert hj, sum_insert hj, card_insert_of_notMem hj, filter_insert]
    rcases hf j (mem_insert_self j S) with h | h
    · have hne : ¬ f j = -1 := by omega
      simp only [h1, h, one_mul]
      refine ⟨rfl, ?_⟩
      push_cast
      linarith
    · simp only [h, ite_true]
      have hjf : j ∉ S.filter (fun i => f i = -1) := fun hm => hj (mem_filter.mp hm).1
      rw [card_insert_of_notMem hjf, h1, pow_succ]
      refine ⟨by ring, ?_⟩
      push_cast
      linarith

/-- A sum of `±1` terms has the parity of the number of terms. If the sum is `±3`, the number of
terms is odd. -/
theorem card_odd_of_sum_signs {ι : Type*} (S : Finset ι) (f : ι → ℤ)
    (hf : ∀ i ∈ S, f i = 1 ∨ f i = -1) (h3 : ∑ i ∈ S, f i = 3 ∨ ∑ i ∈ S, f i = -3) :
    Odd S.card := by
  have h := (prod_sum_of_signs S f hf).2
  rw [Nat.odd_iff]
  rcases h3 with h3 | h3 <;> rw [h3] at h <;> omega

/-- Changing the sign of every factor of a `±1` product with factor sum `±3` changes the sign of the
product (the step "the cycle has odd length by the disk identity" in the proof of Lemma 4.4). -/
theorem prod_neg_of_sum_three {ι : Type*} (S : Finset ι) (f : ι → ℤ)
    (hf : ∀ i ∈ S, f i = 1 ∨ f i = -1) (h3 : ∑ i ∈ S, f i = 3 ∨ ∑ i ∈ S, f i = -3) :
    ∏ i ∈ S, -f i = -∏ i ∈ S, f i := by
  rw [prod_neg, (card_odd_of_sum_signs S f hf h3).neg_one_pow, neg_one_mul]

namespace TriangleSystem

variable {A V : Type*} {T : TriangleSystem A V} {X : Set V}

/-! ### Local signs in a black triangle -/

/-- `δ(v, w) = ±1` for distinct corners. -/
theorem indexDelta_sign : ∀ i j : Fin 3, i ≠ j → indexDelta i j = 1 ∨ indexDelta i j = -1 := by
  decide

/-- Proof of Lemma 4.4, first line: in a black triangle with corners `r, s, u`,
`δ(u, s) = -δ(r, s)`. -/
theorem indexDelta_third_left : ∀ i j : Fin 3, i ≠ j →
    indexDelta (thirdIndex i j) j = -indexDelta i j := by decide

/-- The same triangle: `δ(r, u) = -δ(r, s)`. -/
theorem indexDelta_to_third : ∀ i j : Fin 3, i ≠ j →
    indexDelta i (thirdIndex i j) = -indexDelta i j := by decide

theorem State.val_ne_of_partner {r s : T.State X} (hrs : T.Partner r s) (t : A) :
    r.val t ≠ s.val t := fun h => hrs t ((State.value_eq_iff r s t).mpr h)

/-! ### The sign of a pair -/

/-- The sign of a pair, paper §4 "A sign": `ε(r, s) = ∏_{t ∈ A} δ(r(t), s(t))`. -/
def paperSign [Fintype A] (r s : T.State X) : ℤ := ∏ t, indexDelta (r.val t) (s.val t)

theorem paperSign_sign [Fintype A] {r s : T.State X} (hrs : T.Partner r s) :
    paperSign r s = 1 ∨ paperSign r s = -1 := by
  classical
  rw [paperSign, (prod_sum_of_signs univ _ (fun t _ =>
    indexDelta_sign _ _ (State.val_ne_of_partner hrs t))).1]
  exact neg_one_pow_eq_or ℤ _

/-- `ε = (-1)^N` and `n = Σ_t δ + 2N`, where `N` counts the faces with `δ = -1` and `n = |A|`. -/
theorem paperSign_count [Fintype A] {r s : T.State X} (hrs : T.Partner r s) :
    paperSign r s = (-1) ^ (univ.filter (fun t => indexDelta (r.val t) (s.val t) = -1)).card ∧
      (Fintype.card A : ℤ) = rawIndexSum r s +
        2 * (univ.filter (fun t => indexDelta (r.val t) (s.val t) = -1)).card := by
  classical
  have h := prod_sum_of_signs (univ : Finset A) (fun t => indexDelta (r.val t) (s.val t))
    (fun t _ => indexDelta_sign _ _ (State.val_ne_of_partner hrs t))
  exact ⟨h.1, by rw [← card_univ, h.2, rawIndexSum]⟩

/-! ### Lemma 4.4, first reversal: a cycle of `Q_s` -/

namespace OppositeCycle

variable {s : T.State X} (C : T.OppositeCycle s)

/-- The `δ`-sum of the Lean's opposite cycle is minus the sum of the `δ(r(t), s(t))` over its faces. -/
theorem cyclicDelta_eq_neg (r : T.State X) (hrs : T.Partner r s) :
    C.cyclicDelta r = -∑ i, indexDelta (r.val (C.face i)) (s.val (C.face i)) := by
  rw [cyclicDelta, ← sum_neg_distrib]
  exact sum_congr rfl fun i _ =>
    indexDelta_to_third _ _ (State.val_ne_of_partner hrs _)

/-- **Lemma 4.4 (first reversal).** Reversing a cycle `K` of `Q_s` (Lemma 4.3(1)) changes the sign
`ε`, provided the cycle has `δ`-sum `±3` (the disk identity, which the Lean proves for its concrete
system as `ColoredDual.opposite_disk`). -/
theorem paperSign_reverse [Fintype A] (r : T.State X) (hrs : T.Partner r s)
    (hdisk : C.cyclicDelta r = 3 ∨ C.cyclicDelta r = -3) :
    paperSign (C.reverse r hrs) s = -paperSign r s := by
  classical
  -- the new factors: `-δ` on the faces of `K`, unchanged elsewhere
  have hfac : ∀ t, indexDelta ((C.reverse r hrs).val t) (s.val t) =
      (if t ∈ C.faceSet then (-1 : ℤ) else 1) * indexDelta (r.val t) (s.val t) := by
    intro t
    rw [reverse_val, changedCorners]
    by_cases ht : t ∈ Set.range C.face
    · rw [ite_eq_left ht, ite_eq_left ((C.mem_faceSet t).mpr ht), indexDelta_third_left _ _
        (State.val_ne_of_partner hrs t)]
      ring
    · rw [ite_eq_right ht, ite_eq_right (fun h => ht ((C.mem_faceSet t).mp h)), one_mul]
  -- the cycle has an odd number of faces
  have hodd : Odd C.faceSet.card := by
    rw [faceSet, card_image_of_injective _ C.face.injective]
    apply card_odd_of_sum_signs univ (fun i => indexDelta (r.val (C.face i)) (s.val (C.face i)))
      (fun i _ => indexDelta_sign _ _ (State.val_ne_of_partner hrs _))
    rw [C.cyclicDelta_eq_neg r hrs] at hdisk
    rcases hdisk with h | h
    · right; linarith
    · left; linarith
  rw [paperSign, paperSign, prod_congr rfl (fun t _ => hfac t), prod_mul_distrib, prod_ite_mem,
    univ_inter, prod_const, hodd.neg_one_pow, neg_one_mul]

/-- The cancellation of Lemma 4.5 with the real sign: for a state `s` whose `Q_s` has a cycle
(with `δ`-sum `±3` for every partner), `Σ_r ε(r, s) = 0` over the partners `r` of `s`. -/
theorem paperSign_partners_sum [Fintype A] {M : Type*} [AddCommGroup M]
    (hdisk : ∀ r : T.Partners s, C.cyclicDelta r.val = 3 ∨ C.cyclicDelta r.val = -3)
    (weight : M) : (∑ r : T.Partners s, paperSign r.val s • weight) = 0 := by
  classical
  apply Finset.sum_ninvolution C.reversal
  · intro r
    change paperSign r.val s • weight + paperSign (C.reverse r.val r.property) s • weight = 0
    rw [C.paperSign_reverse r.val r.property (hdisk r), neg_smul, add_neg_cancel]
  · intro r _
    exact C.reversal_ne r
  · intro r
    exact Finset.mem_univ _
  · intro r
    exact C.reversal_involutive r

end OppositeCycle

/-! ### Lemma 4.4, second reversal: cycles of `D(r, s)` -/

namespace Pair

variable [Fintype A]

/-- The sign of a pair, as a function of the pair. -/
def sign (P : T.Pair X) : ℤ := paperSign P.left P.right

theorem sign_eq_prod_cycles (P : T.Pair X) :
    P.sign = ∏ c, ∏ t ∈ P.cycleFaces c, indexDelta (P.left.val t) (P.right.val t) := by
  classical
  rw [sign, paperSign, ← Finset.prod_fiberwise Finset.univ (classOf P.next)]
  rfl

/-- On one cycle of `D(r, s)` the factors `δ(r(t), s(t))` multiply to `-1` after reversing
when the cycle has `δ`-sum `±3`. -/
theorem cycle_prod_reverse (P : T.Pair X) (c : CycleClass P.next)
    (hdisk : P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    ∏ t ∈ P.cycleFaces c, -indexDelta (P.left.val t) (P.right.val t) =
      -∏ t ∈ P.cycleFaces c, indexDelta (P.left.val t) (P.right.val t) :=
  prod_neg_of_sum_three _ _ (fun t _ => indexDelta_sign _ _ (State.val_ne_of_partner P.partner t))
    hdisk

/-- **Lemma 4.4 (second reversal), several cycles at once.** Reversing the cycles of `D(r, s)`
selected by `b` (Lemma 4.3(2)) multiplies `ε` by `(-1)^(number of reversed cycles)`, provided every
cycle of `D(r, s)` has `δ`-sum `±3` (the disk identity; the Lean proves it for its concrete system
as `ColoredDual.paired_sign`). -/
theorem sign_orient (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (b : CycleClass P.next → Bool) :
    (P.orient b).val.sign = (-1) ^ (univ.filter (fun c => b c = true)).card * P.sign := by
  classical
  have hcls : ∀ c, ∏ t ∈ P.cycleFaces c, indexDelta ((P.orient b).val.left.val t)
      ((P.orient b).val.right.val t) =
      (if b c = true then (-1 : ℤ) else 1) *
        ∏ t ∈ P.cycleFaces c, indexDelta (P.left.val t) (P.right.val t) := by
    intro c
    have hcongr : ∀ t ∈ P.cycleFaces c, indexDelta ((P.orient b).val.left.val t)
        ((P.orient b).val.right.val t) =
        if b c then -indexDelta (P.left.val t) (P.right.val t)
          else indexDelta (P.left.val t) (P.right.val t) := by
      intro t ht
      rw [orient_left_val, orient_right_val, (P.mem_cycleFaces c t).mp ht]
      cases b c
      · rfl
      · exact indexDelta_antisymm _ _
    rw [prod_congr rfl hcongr]
    cases hb : b c
    · simp
    · simp only [ite_true]
      rw [P.cycle_prod_reverse c (hdisk c), neg_one_mul]
  rw [sign, paperSign, ← Finset.prod_fiberwise Finset.univ (classOf P.next), sign_eq_prod_cycles]
  calc _ = ∏ c, (if b c = true then (-1 : ℤ) else 1) *
        ∏ t ∈ P.cycleFaces c, indexDelta (P.left.val t) (P.right.val t) := by
        apply prod_congr rfl
        intro c _
        exact hcls c
    _ = _ := by rw [prod_mul_distrib, prod_ite, prod_const, prod_const_one, mul_one]

/-- **Lemma 4.4 (second reversal).** Reversing one cycle `c` of `D(r, s)` changes the sign. -/
theorem sign_reverse_one (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (c : CycleClass P.next) (b : CycleClass P.next → Bool) (hb : ∀ c', b c' = true ↔ c' = c) :
    (P.orient b).val.sign = -P.sign := by
  classical
  rw [P.sign_orient hdisk]
  have : (univ.filter (fun c' => b c' = true)) = {c} := by
    ext c'; simp [hb]
  rw [this, card_singleton, pow_one, neg_one_mul]

/-- The `δ`-sums of the cycles of `D(r, s)` add up to the Lean's `rawIndexSum`. -/
theorem rawIndexSum_eq_sum_cycleDelta (P : T.Pair X) :
    rawIndexSum P.left P.right = ∑ c, P.cycleDelta c := by
  classical
  rw [rawIndexSum, ← Finset.sum_fiberwise Finset.univ (classOf P.next)]
  rfl

/-- The number of cycles of `D(r, s)` that run counterclockwise (`δ`-sum `-3`). -/
noncomputable def ccwCount (P : T.Pair X) : ℕ :=
  by classical exact (univ.filter (fun c => P.cycleDelta c = -3)).card

theorem sum_cycleDelta (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    ∑ c, P.cycleDelta c = 3 * Fintype.card (CycleClass P.next) - 6 * P.ccwCount := by
  classical
  have h : ∀ c, P.cycleDelta c = if P.cycleDelta c = -3 then -3 else 3 := by
    intro c
    rcases hdisk c with h | h <;> simp [h]
  rw [sum_congr rfl (fun c _ => h c), sum_ite, sum_const, sum_const, ccwCount, nsmul_eq_mul,
    nsmul_eq_mul]
  have hc := card_filter_add_card_filter_not (s := (univ : Finset (CycleClass P.next)))
    (fun c => P.cycleDelta c = -3)
  rw [card_univ] at hc
  have hc' : ((univ.filter (fun c => P.cycleDelta c = -3)).card : ℤ) +
      (univ.filter (fun c => ¬P.cycleDelta c = -3)).card = Fintype.card (CycleClass P.next) := by
    exact_mod_cast hc
  linarith

/-- **Lemma 4.4 (formula).** If `D(r, s)` has `c` cycles, of which `c⁺` run counterclockwise, then
`n ≡ c (mod 2)` and `ε(r, s) = (-1)^((n + c)/2) (-1)^(c⁺)`, where `n = |A|`. -/
theorem sign_formula (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    Even (Fintype.card A + Fintype.card (CycleClass P.next)) ∧
      P.sign = (-1) ^ ((Fintype.card A + Fintype.card (CycleClass P.next)) / 2 + P.ccwCount) := by
  classical
  obtain ⟨hs, hn⟩ := paperSign_count P.partner
  rw [P.rawIndexSum_eq_sum_cycleDelta, P.sum_cycleDelta hdisk] at hn
  set N := (univ.filter (fun t => indexDelta (P.left.val t) (P.right.val t) = -1)).card
  set n := Fintype.card A
  set c := Fintype.card (CycleClass P.next)
  have hle : P.ccwCount ≤ c := by
    rw [ccwCount]; exact (card_filter_le _ _).trans (by rw [card_univ])
  refine ⟨by rw [Nat.even_iff]; omega, ?_⟩
  rw [sign, hs, neg_one_pow_eq_pow_mod_two, neg_one_pow_eq_pow_mod_two (n := (n + c) / 2 + _)]
  congr 1
  omega

/-! ### The real sign and OpenAI's phase -/

/-- `i^(Σ_t δ(r(t), s(t))) = i^n ε(r, s)` for every pair; no disk identity needed. -/
theorem I_zpow_rawIndexSum {r s : T.State X} (hrs : T.Partner r s) :
    Complex.I ^ rawIndexSum r s = Complex.I ^ Fintype.card A * (paperSign r s : ℂ) := by
  classical
  obtain ⟨hs, hn⟩ := paperSign_count hrs
  set N := (univ.filter (fun t => indexDelta (r.val t) (s.val t) = -1)).card
  have hraw : rawIndexSum r s = (Fintype.card A : ℤ) + 2 * (-(N : ℤ)) := by omega
  rw [hraw, zpow_add₀ Complex.I_ne_zero, zpow_natCast, zpow_mul,
    show Complex.I ^ (2 : ℤ) = -1 by norm_num, hs]
  push_cast
  rw [zpow_neg, zpow_natCast, ← inv_pow, inv_neg, inv_one]

/-- **The phase of OpenAI's Lean proof is the real sign times the constant `i^(-n)`**
(paper, Remark 4.10: "`i^J = i^{-n} ε`"). The hypothesis `3 ∣ Σ δ` holds for every pair of the
concrete system by the disk identity (see `three_dvd_rawIndexSum`). -/
theorem phase_eq_paperSign {r s : T.State X} (hrs : T.Partner r s)
    (h3 : (3 : ℤ) ∣ rawIndexSum r s) :
    phase (rawIndexSum r s) = Complex.I ^ (-(Fintype.card A : ℤ)) * (paperSign r s : ℂ) := by
  obtain ⟨J, hJ⟩ := h3
  have hI := I_zpow_rawIndexSum hrs
  rw [hJ] at hI ⊢
  have hph : phase (3 * J) = Complex.I ^ J := by
    unfold phase; congr 1; omega
  rw [hph]
  -- `i^(3J) * i^J = 1`
  have h4 : Complex.I ^ (3 * J) * Complex.I ^ J = 1 := by
    rw [← zpow_add₀ Complex.I_ne_zero, show 3 * J + J = 4 * J by ring, zpow_mul]
    norm_num
  have hε : (paperSign r s : ℂ) * (paperSign r s : ℂ) = 1 := by
    rcases paperSign_sign hrs with h | h <;> rw [h] <;> norm_num
  rw [zpow_neg, zpow_natCast]
  rw [hI] at h4
  have hIn : Complex.I ^ Fintype.card A ≠ 0 := pow_ne_zero _ Complex.I_ne_zero
  field_simp
  calc Complex.I ^ J * Complex.I ^ Fintype.card A
      = Complex.I ^ J * Complex.I ^ Fintype.card A * ((paperSign r s : ℂ) * paperSign r s) := by
        rw [hε, mul_one]
    _ = (Complex.I ^ Fintype.card A * paperSign r s * Complex.I ^ J) * paperSign r s := by ring
    _ = paperSign r s := by rw [h4, one_mul]

/-- Equivalently `ε(r, s) = i^n · phase`: the ratio `ε / phase` is the constant `i^n`. -/
theorem paperSign_eq_I_pow_mul_phase {r s : T.State X} (hrs : T.Partner r s)
    (h3 : (3 : ℤ) ∣ rawIndexSum r s) :
    (paperSign r s : ℂ) = Complex.I ^ Fintype.card A * phase (rawIndexSum r s) := by
  rw [phase_eq_paperSign hrs h3, ← mul_assoc, zpow_neg, zpow_natCast,
    mul_inv_cancel₀ (pow_ne_zero _ Complex.I_ne_zero), one_mul]

/-- The disk identity on the cycles of `D(r, s)` gives `3 ∣ Σ_t δ(r(t), s(t))`. -/
theorem three_dvd_rawIndexSum (P : T.Pair X)
    (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    (3 : ℤ) ∣ rawIndexSum P.left P.right := by
  rw [P.rawIndexSum_eq_sum_cycleDelta, P.sum_cycleDelta hdisk]
  exact ⟨Fintype.card (CycleClass P.next) - 2 * P.ccwCount, by ring⟩

/-- For a pair whose `D`-cycles satisfy the disk identity: `ε = i^n · phase`. -/
theorem sign_eq_I_pow_mul_phase (P : T.Pair X)
    (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    (P.sign : ℂ) = Complex.I ^ Fintype.card A * phase (rawIndexSum P.left P.right) :=
  paperSign_eq_I_pow_mul_phase P.partner (P.three_dvd_rawIndexSum hdisk)

end Pair
end TriangleSystem
end OAI.Barnette
