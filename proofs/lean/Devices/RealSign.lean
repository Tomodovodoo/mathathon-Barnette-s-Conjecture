/-
Proposition 4.8 of paper/main/barnette.tex ("if T has a pair, then it has a good state"), by the
paper's devices: the real sign `ε` of Lemma 4.4, the power `ω(s)^m` of a weight that is a sum of
local terms, and the finite differences of Lemma 4.7 (`Devices.FiniteDifference`), stated and
proved in the model of github.com/openai/math, commit 4eaee875.

The weight is any `w : A → Fin 3 → ℝ`, `ω(s) = Σ_t w t (s t)`: the paper's heights
`ω(s) = Σ_y η_s(y)` are of this form (`w t v = Σ_y κ_y(t, v)`), and so are the Lean's flow weights
`ColoredDual.weights α root`. The hypotheses are exactly those of the Lean's
`Pair.forest_pair_of_disk_circulation`:
* `hdisk`: every cycle of every `Q_s` has `δ`-sum `±3` (disk identity),
* `hsign`: every cycle of every `D(r, s)` has `δ`-sum `-3` and positive slope (counterclockwise,
  paper: `L(C) ≥ 1` white faces inside) or `δ`-sum `3` and negative slope (clockwise).
-/
import Devices.LocalSign
import Devices.FiniteDifference

namespace OAI.Barnette

open Finset

/-- Functions to `Bool` are subsets. -/
def boolFunEquivFinset (ι : Type*) [Fintype ι] [DecidableEq ι] : (ι → Bool) ≃ Finset ι where
  toFun b := univ.filter (fun c => b c = true)
  invFun S := fun c => decide (c ∈ S)
  left_inv b := by funext c; simp
  right_inv S := by ext c; simp

namespace TriangleSystem

variable {A V : Type*} [Fintype A] {T : TriangleSystem A V} {X : Set V}

/-- The weight of a state, `ω(s) = Σ_t w(t, s(t))`. -/
def weight (w : A → Fin 3 → ℝ) (s : T.State X) : ℝ := ∑ t, w t (s.val t)

/-- The paper's signed sum `Σ = Σ_{(r,s)} ε(r, s) ω(s)^m` over all pairs. -/
noncomputable def realSum (w : A → Fin 3 → ℝ) (m : ℕ) : ℝ :=
  ∑ P : T.Pair X, (P.sign : ℝ) * weight w P.right ^ m

namespace Pair

/-! ### Lemma 4.5 with the real sign -/

/-- **Lemma 4.5 (cancellation).** If every cycle of every `Q_s` has `δ`-sum `±3`, the pairs whose
second state has a cycle in `Q_s` contribute nothing: if no pair has an acyclic `Q_s`, then
`Σ_{(r,s)} ε(r, s) F(s) = 0` for every function `F` of the second state. -/
theorem sum_sign_eq_zero_of_no_good
    (hdisk : ∀ (s : T.State X) (C : T.OppositeCycle s) (r : T.Partners s),
      C.cyclicDelta r.val = 3 ∨ C.cyclicDelta r.val = -3)
    (hnone : ∀ P : T.Pair X, ¬(T.oppositeGraph P.right).IsAcyclic)
    (F : T.State X → ℝ) :
    (∑ P : T.Pair X, (P.sign : ℝ) * F P.right) = 0 := by
  classical
  rw [← Fintype.sum_fiberwise right (fun P : T.Pair X => (P.sign : ℝ) * F P.right)]
  apply Finset.sum_eq_zero
  intro s _
  rw [Fintype.sum_equiv (secondFiberEquiv s) _ (fun r : T.Partners s => (paperSign r.val s : ℝ) * F s)
    (by intro P; change (paperSign P.val.left P.val.right : ℝ) * F P.val.right = _
        rw [P.property]; rfl)]
  by_cases hp : Nonempty (T.Partners s)
  · let P : T.Pair X := ⟨(hp.some.val, s), hp.some.property⟩
    obtain ⟨C⟩ := T.oppositeCycle_nonempty s (hnone P)
    have h := C.paperSign_partners_sum (hdisk s C) (F s)
    simpa only [zsmul_eq_mul] using h
  · have : IsEmpty (T.Partners s) := not_nonempty_iff.mp hp
    exact Finset.sum_eq_zero (fun r _ => isEmptyElim r)

/-! ### Lemma 4.6: the weight under reversal of cycles of `D` -/

/-- The step of cycle `c`: `L(c) = Σ_{t ∈ c} w(t, r(t)) - Σ_{t ∈ c} w(t, s(t)) = -slope(c)`.
Reversing `c` replaces `s(t)` by `r(t)` on its faces, so it adds `L(c)` to `ω(s)`. -/
noncomputable def step (P : T.Pair X) (w : A → Fin 3 → ℝ) (c : CycleClass P.next) : ℝ :=
  -P.cycleSlope w c

/-- **Lemma 4.6 (additivity).** Reversing the cycles of `D(r, s)` selected by `b` adds their steps
to the weight of the second state: `ω(s') = ω(s) + Σ_{c reversed} L(c)`. -/
theorem weight_orient (P : T.Pair X) (w : A → Fin 3 → ℝ) (b : CycleClass P.next → Bool) :
    weight w (P.orient b).val.right =
      weight w P.right + ∑ c ∈ univ.filter (fun c => b c = true), P.step w c := by
  classical
  have hcls : ∀ c, ∑ t ∈ P.cycleFaces c, w t ((P.orient b).val.right.val t) =
      ∑ t ∈ P.cycleFaces c, w t (P.right.val t) + (if b c = true then P.step w c else 0) := by
    intro c
    have hcongr : ∀ t ∈ P.cycleFaces c, w t ((P.orient b).val.right.val t) =
        if b c = true then w t (P.left.val t) else w t (P.right.val t) := by
      intro t ht
      rw [orient_right_val, (P.mem_cycleFaces c t).mp ht]
      cases b c <;> rfl
    rw [sum_congr rfl hcongr]
    cases b c
    · simp
    · simp only [ite_true, step, cycleSlope]
      ring
  rw [weight, weight, ← Finset.sum_fiberwise Finset.univ (classOf P.next),
    ← Finset.sum_fiberwise Finset.univ (classOf P.next) (fun t => w t (P.right.val t))]
  calc _ = ∑ c, (∑ t ∈ P.cycleFaces c, w t (P.right.val t) +
        (if b c = true then P.step w c else 0)) := by
        apply sum_congr rfl
        intro c _
        exact hcls c
    _ = _ := by
        rw [sum_add_distrib, ← sum_filter]
        rfl

/-! ### The class sum (proof of Proposition 4.8, first half) -/

/-- **Class sum.** The pairs with the same undirected `D` as `P` (the Lean's `P.Group`, which
`Pair.groupEquiv` identifies with the `2^c` orientations of the cycles) contribute
`ε(P) · Σ_{S} (-1)^{|S|} (ω₀ + Σ_{c ∈ S} L(c))^m`, a repeated finite difference. -/
theorem group_sum (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (w : A → Fin 3 → ℝ) (m : ℕ) :
    (∑ Q : P.Group, (Q.val.sign : ℝ) * weight w Q.val.right ^ m) =
      (P.sign : ℝ) * Blueprint.F (P.step w) univ (weight w P.right) m := by
  classical
  rw [← Fintype.sum_equiv P.groupEquiv _ (fun Q : P.Group => (Q.val.sign : ℝ) *
    weight w Q.val.right ^ m) (fun _ => rfl)]
  change ∑ b : CycleClass P.next → Bool, ((P.orient b).val.sign : ℝ) *
    weight w (P.orient b).val.right ^ m = _
  simp only [P.sign_orient hdisk, P.weight_orient w]
  rw [Blueprint.F, Finset.mul_sum, powerset_univ,
    ← Fintype.sum_equiv (boolFunEquivFinset (CycleClass P.next)) _ _ (fun _ => rfl)]
  apply sum_congr rfl
  intro b _
  simp only [boolFunEquivFinset, Equiv.coe_fn_mk]
  push_cast
  ring

/-- With `m` equal to the number `c` of cycles, the class sum is `m!` times
`(-1)^((n+m)/2 + m)` times the product of the absolute steps `|L(C_i)|`: its sign depends on `n`
and `m` only. -/
theorem group_sum_card (P : T.Pair X) (w : A → Fin 3 → ℝ)
    (hsign : ∀ c, (P.cycleDelta c = -3 ∧ 0 < P.cycleSlope w c) ∨
      (P.cycleDelta c = 3 ∧ P.cycleSlope w c < 0)) :
    (∑ Q : P.Group, (Q.val.sign : ℝ) * weight w Q.val.right ^ Fintype.card (CycleClass P.next)) =
      (-1) ^ ((Fintype.card A + Fintype.card (CycleClass P.next)) / 2 +
        Fintype.card (CycleClass P.next)) * (Fintype.card (CycleClass P.next)).factorial *
        ∏ c, |P.cycleSlope w c| := by
  classical
  have hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3 := fun c => by
    rcases hsign c with ⟨h, _⟩ | ⟨h, _⟩
    · exact Or.inr h
    · exact Or.inl h
  set m := Fintype.card (CycleClass P.next) with hm
  rw [P.group_sum hdisk w m]
  have hfd := (Blueprint.finite_difference (P.step w) (univ : Finset (CycleClass P.next))).2
    (weight w P.right)
  rw [card_univ, ← hm] at hfd
  rw [hfd]
  -- `∏ L = (-1)^m ∏ slope` and `∏ slope = (-1)^(m - c⁺) ∏ |slope|`
  have hslope : ∀ c, P.cycleSlope w c =
      (if P.cycleDelta c = -3 then (1 : ℝ) else -1) * |P.cycleSlope w c| := by
    intro c
    rcases hsign c with ⟨h, hs⟩ | ⟨h, hs⟩
    · rw [ite_eq_left h, one_mul, abs_of_pos hs]
    · rw [ite_eq_right (by rw [h]; norm_num), abs_of_neg hs]; ring
  have hstep : ∏ c, P.step w c =
      (-1) ^ m * ((-1) ^ (m - P.ccwCount) * ∏ c, |P.cycleSlope w c|) := by
    simp only [step]
    rw [prod_neg]
    rw [card_univ, ← hm]
    congr 1
    rw [prod_congr rfl (fun c _ => hslope c), prod_mul_distrib, prod_ite, prod_const_one,
      prod_const, one_mul]
    congr 2
    have hc := card_filter_add_card_filter_not (s := (univ : Finset (CycleClass P.next)))
      (fun c => P.cycleDelta c = -3)
    rw [card_univ, ← hm] at hc
    rw [ccwCount]
    omega
  obtain ⟨heven, hs⟩ := P.sign_formula hdisk
  rw [← hm] at hs heven
  rw [hstep, hs]
  have hle : P.ccwCount ≤ m := by
    rw [ccwCount, hm]; exact (card_filter_le _ _).trans (by rw [card_univ])
  push_cast
  -- collect the powers of `-1`
  have hexp : ∀ k : ℕ, ((-1 : ℝ) ^ k) = (-1) ^ (k % 2) := fun k => neg_one_pow_eq_pow_mod_two k
  have key : ((-1 : ℝ) ^ ((Fintype.card A + m) / 2 + P.ccwCount)) * ((-1) ^ m * (-1) ^ m) *
      (-1) ^ (m - P.ccwCount) = (-1) ^ ((Fintype.card A + m) / 2 + m) := by
    rw [← pow_add, ← pow_add, ← pow_add, hexp, hexp ((Fintype.card A + m) / 2 + m)]
    congr 1
    omega
  calc _ = ((-1 : ℝ) ^ ((Fintype.card A + m) / 2 + P.ccwCount) * ((-1) ^ m * (-1) ^ m) *
        (-1) ^ (m - P.ccwCount)) * (m.factorial : ℝ) * ∏ c, |P.cycleSlope w c| := by ring
    _ = _ := by rw [key]

/-- With more cycles than `m`, the class sum vanishes (Lemma 4.7, case `m < c`). -/
theorem group_sum_lt (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (w : A → Fin 3 → ℝ) {m : ℕ} (hm : m < Fintype.card (CycleClass P.next)) :
    (∑ Q : P.Group, (Q.val.sign : ℝ) * weight w Q.val.right ^ m) = 0 := by
  classical
  rw [P.group_sum hdisk w m,
    (Blueprint.finite_difference (P.step w) univ).1 (weight w P.right) m (by rwa [card_univ]),
    mul_zero]

/-! ### Proposition 4.8 -/

/-- The smallest number of cycles of `D` over the representatives of the classes (the Lean's
`GroupIndex`). -/
noncomputable def minCycles (hex : Nonempty (T.Pair X)) : ℕ :=
  have : Nonempty (@GroupIndex A V T X) := ⟨hex.some.groupIndex⟩
  (univ.image (fun d : @GroupIndex A V T X =>
    Fintype.card (CycleClass d.representative.next))).min' (by simp)

/-- The class decomposition of a sum over pairs (as the Lean's `sum_groups`, for any summand). -/
theorem sum_groups' (f : T.Pair X → ℝ) :
    (∑ P : T.Pair X, f P) =
      ∑ d : @GroupIndex A V T X, ∑ Q : d.representative.Group, f Q.val := by
  classical
  rw [← Fintype.sum_fiberwise groupIndex f]
  apply Finset.sum_congr rfl
  intro d _
  exact Fintype.sum_equiv d.fiberEquivGroup _ _ (fun _ => rfl)

/-- **Proposition 4.8, nonvanishing.** If a pair exists, and every cycle of every `D(r, s)` has
`δ`-sum `-3` with positive slope or `3` with negative slope, then with `m` the smallest number of
cycles the paper's sum `Σ_{(r,s)} ε(r, s) ω(s)^m` equals
`(-1)^((n+m)/2 + m) · m! · Σ_{classes with m cycles} ∏ |L(C_i)|` and is not zero. -/
theorem realSum_ne_zero (hex : Nonempty (T.Pair X)) (w : A → Fin 3 → ℝ)
    (hsign : ∀ (P : T.Pair X) c,
      (P.cycleDelta c = -3 ∧ 0 < P.cycleSlope w c) ∨
      (P.cycleDelta c = 3 ∧ P.cycleSlope w c < 0)) :
    realSum (T := T) (X := X) w (minCycles hex) ≠ 0 := by
  classical
  set m := minCycles hex
  have hdisk : ∀ (P : T.Pair X) c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3 := fun P c => by
    rcases hsign P c with ⟨h, _⟩ | ⟨h, _⟩
    · exact Or.inr h
    · exact Or.inl h
  have hne : (univ.image (fun d : @GroupIndex A V T X =>
      Fintype.card (CycleClass d.representative.next))).Nonempty := by
    have : Nonempty (@GroupIndex A V T X) := ⟨hex.some.groupIndex⟩
    simp
  have hmin : ∀ d : @GroupIndex A V T X, m ≤ Fintype.card (CycleClass d.representative.next) :=
    fun d => min'_le _ _ (mem_image_of_mem _ (mem_univ d))
  obtain ⟨d₀, -, hd₀⟩ := mem_image.mp (min'_mem _ hne)
  let a : @GroupIndex A V T X → ℝ := fun d => ∏ c, |d.representative.cycleSlope w c|
  have ha : ∀ d, 0 < a d := fun d => prod_pos (fun c _ => abs_pos.mpr (by
    rcases hsign d.representative c with ⟨_, h⟩ | ⟨_, h⟩
    · exact h.ne'
    · exact h.ne))
  set K : ℝ := (-1) ^ ((Fintype.card A + m) / 2 + m) * (m.factorial : ℝ)
  have hterm : ∀ d : @GroupIndex A V T X,
      (∑ Q : d.representative.Group, (Q.val.sign : ℝ) * weight w Q.val.right ^ m) =
        if Fintype.card (CycleClass d.representative.next) = m then K * a d else 0 := by
    intro d
    split_ifs with h
    · have := d.representative.group_sum_card w (hsign d.representative)
      rw [h] at this
      rw [this]
    · exact d.representative.group_sum_lt (hdisk _) w (lt_of_le_of_ne (hmin d) (Ne.symm h))
  rw [realSum, sum_groups', sum_congr rfl (fun d _ => hterm d), ← sum_filter, ← mul_sum]
  apply mul_ne_zero
  · exact mul_ne_zero (pow_ne_zero _ (by norm_num)) (by exact_mod_cast m.factorial_ne_zero)
  · apply ne_of_gt
    apply sum_pos (fun d _ => ha d)
    exact ⟨d₀, mem_filter.mpr ⟨mem_univ _, hd₀⟩⟩

/-- **Proposition 4.8.** If `T` has a pair, it has a good state, by the paper's route (real sign,
power of the weight, finite differences). Same hypotheses and conclusion as the Lean's
`Pair.forest_pair_of_disk_circulation`, which uses the phase and a polynomial instead. -/
theorem forest_pair_of_disk_circulation_real (hex : Nonempty (T.Pair X))
    (hdisk : ∀ (s : T.State X) (C : T.OppositeCycle s) (r : T.Partners s),
      C.cyclicDelta r.val = 3 ∨ C.cyclicDelta r.val = -3)
    (w : A → Fin 3 → ℝ)
    (hsign : ∀ (P : T.Pair X) c,
      (P.cycleDelta c = -3 ∧ 0 < P.cycleSlope w c) ∨
      (P.cycleDelta c = 3 ∧ P.cycleSlope w c < 0)) :
    ∃ P : T.Pair X, (T.oppositeGraph P.right).IsAcyclic := by
  by_contra hforest
  push Not at hforest
  exact realSum_ne_zero hex w hsign
    (sum_sign_eq_zero_of_no_good hdisk hforest (fun s => weight w s ^ minCycles hex))

end Pair
end TriangleSystem
end OAI.Barnette
