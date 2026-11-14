/-
Lemma 4.7 of paper/main/barnette.tex (finite differences), in Lean 4 + Mathlib.

For a finite index set `s` and reals (any commutative ring) `ω₀`, `L i`:

  ∑_{S ⊆ s} (-1)^|S| (ω₀ + ∑_{i ∈ S} L i)^m = 0                       if m < |s|,
                                              = (-1)^|s| |s|! ∏_{i ∈ s} L i  if m = |s|.

The paper indexes by x ∈ {0,1}^c; a subset S is the support of x.
Standalone file: imports Mathlib only, nothing from openai/math.
Checked with: lake env lean <this file>, in a Lake project with Mathlib d13f23b7, Lean v4.34.1.
-/
import Mathlib

open Finset

namespace Blueprint

variable {ι R : Type*} [DecidableEq ι] [CommRing R]

/-- The signed sum over subsets of `s` (the class sum of Proposition 4.8, up to the
global sign). -/
def F (L : ι → R) (s : Finset ι) (a : R) (m : ℕ) : R :=
  ∑ S ∈ s.powerset, (-1 : R) ^ S.card * (a + ∑ i ∈ S, L i) ^ m

/-- Adding one index takes a difference in the direction `L j`, expanded binomially. -/
lemma F_insert (L : ι → R) {s : Finset ι} {j : ι} (hj : j ∉ s) (a : R) (m : ℕ) :
    F L (insert j s) a m =
      F L s a m - ∑ k ∈ range (m + 1), L j ^ k * (m.choose k : R) * F L s a (m - k) := by
  unfold F
  rw [sum_powerset_insert hj, sub_eq_add_neg]
  congr 1
  have h1 : ∀ t ∈ s.powerset, (-1 : R) ^ (insert j t).card * (a + ∑ i ∈ insert j t, L i) ^ m =
      -∑ k ∈ range (m + 1), L j ^ k * (m.choose k : R) *
        ((-1 : R) ^ t.card * (a + ∑ i ∈ t, L i) ^ (m - k)) := by
    intro t ht
    have hjt : j ∉ t := fun h => hj (mem_powerset.mp ht h)
    rw [card_insert_of_notMem hjt, sum_insert hjt,
      show a + (L j + ∑ i ∈ t, L i) = L j + (a + ∑ i ∈ t, L i) by ring, add_pow, mul_sum,
      ← sum_neg_distrib]
    refine sum_congr rfl fun k _ => ?_
    ring
  rw [sum_congr rfl h1, sum_neg_distrib, sum_comm]
  congr 1
  refine sum_congr rfl fun k _ => ?_
  rw [mul_sum]

/-- Lemma 4.7: the repeated difference kills degree below `|s|` and leaves `|s|!` times
the product of the steps in degree `|s|`. -/
theorem finite_difference (L : ι → R) (s : Finset ι) :
    (∀ a m, m < s.card → F L s a m = 0) ∧
      ∀ a, F L s a s.card = (-1 : R) ^ s.card * (s.card.factorial : R) * ∏ i ∈ s, L i := by
  induction s using Finset.induction_on with
  | empty =>
    refine ⟨fun a m h => absurd h (Nat.not_lt_zero _), fun a => ?_⟩
    simp [F]
  | insert j s hj ih =>
    obtain ⟨h0, h1⟩ := ih
    -- the k = 0 term cancels F L s a m
    have step : ∀ a m, F L (insert j s) a m =
        -∑ k ∈ range m, L j ^ (k + 1) * (m.choose (k + 1) : R) * F L s a (m - (k + 1)) := by
      intro a m
      rw [F_insert L hj, sum_range_succ']
      simp
    refine ⟨fun a m hm => ?_, fun a => ?_⟩
    · rw [card_insert_of_notMem hj] at hm
      rw [step, neg_eq_zero]
      refine sum_eq_zero fun k hk => ?_
      rw [h0 a (m - (k + 1)) (by have := mem_range.mp hk; omega), mul_zero]
    · rw [step, card_insert_of_notMem hj, sum_range_succ']
      have hz : ∑ k ∈ range s.card, L j ^ (k + 1 + 1) * ((s.card + 1).choose (k + 1 + 1) : R) *
          F L s a (s.card + 1 - (k + 1 + 1)) = 0 := by
        refine sum_eq_zero fun k hk => ?_
        rw [h0 a _ (by have := mem_range.mp hk; omega), mul_zero]
      rw [hz, zero_add, show s.card + 1 - (0 + 1) = s.card by omega, h1 a, prod_insert hj,
        Nat.factorial_succ]
      simp only [zero_add, pow_one, Nat.choose_one_right]
      push_cast
      ring

/-- The statement in the form printed in the paper: indices `Fin c`. -/
theorem finite_difference_fin (c : ℕ) (ω₀ : R) (L : Fin c → R) :
    (∀ m, m < c → ∑ S ∈ (univ : Finset (Fin c)).powerset,
        (-1 : R) ^ S.card * (ω₀ + ∑ i ∈ S, L i) ^ m = 0) ∧
      ∑ S ∈ (univ : Finset (Fin c)).powerset, (-1 : R) ^ S.card * (ω₀ + ∑ i ∈ S, L i) ^ c =
        (-1 : R) ^ c * (c.factorial : R) * ∏ i, L i := by
  have h := finite_difference L (univ : Finset (Fin c))
  simp only [card_univ, Fintype.card_fin] at h
  exact ⟨fun m hm => h.1 ω₀ m hm, h.2 ω₀⟩

end Blueprint

#print axioms Blueprint.finite_difference
#print axioms Blueprint.finite_difference_fin
