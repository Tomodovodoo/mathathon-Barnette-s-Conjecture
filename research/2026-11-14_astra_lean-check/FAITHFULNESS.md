# Statement faithfulness

Status: COMPUTED for compiled Lean statements; PROVED-HERE for the elementary comparisons and sign algebra. This audit compares the frozen working-tree paper in `paper-at-review.tex.txt`, not an earlier author commit. The relevant labels still resolve to Lemmas 3.7, 4.4--4.7, Proposition 4.8 and Remark 4.10, as recorded in `paper-labels.txt`.

## Definitions and scope

All generic triangle results have types A,V, a TriangleSystem T, and a set X of allowed vertices. Fintype A supplies an enumeration of faces, not a Nonempty A instance. TriangleSystem has three distinct vertices per face and forbids distinct faces sharing the same side. A State is a corner function whose selected vertices are injective and have range exactly X. Thus it is an incidence-constrained bijection A to X. Partner means different selected vertices at every face; Pair is the subtype of ordered state pairs with that property. These are upstream definitions, unchanged.

indexDelta on Fin 3 is 0 on equal indices, +1 on cyclic successors, -1 otherwise. On pairs it is ±1. paperSign is the integer product over all faces, not a new arbitrary sign. The witness Nonvacuity.lean supplies a nonempty three-face model and both sign values. numerical.py checks actual sphere triangulations and has 136 ordered pairs across all face rootings.

Pair.next is right.toEquiv followed by left.toEquiv inverse. CycleClass is the quotient of A by permutation SameCycle, not a singleton surrogate. A fixed point is impossible for a pair. cycleFaces is the fiber of this quotient map. cycleDelta sums local deltas there. Group fixes the unused third corner at each face, hence the same undirected chosen side. orient swaps left and right on whole orbits. groupEquiv is upstream's bijection between Boolean orbit choices and this fiber. GroupIndex is the range of the third-corner map; representative uses Classical.choose of a pair witnessing membership. minCycles minimises the orbit count of those representatives.

OppositeGraph has an edge between the two corners not selected by the state. OppositeCycle contains an injective genuine graph cycle of length at least three and distinct incident faces. Upstream oppositeCycle_nonempty derives one from failure of IsAcyclic. Mathlib IsAcyclic says that no closed walk is a cycle. In particular an isolated vertex does not by definition make a graph non-acyclic. The paper's good state additionally requires exactly one root in every component. Acyclicity alone is not equivalent for an arbitrary state, as the prism example confirms. Existence theorems here also retain a partner, which is essential for the B4 bridge.

weight w s is the sum of w(t,s(t)). cycleSlope is sum w(t,right(t)) minus sum w(t,left(t)) on one orbit; step is its negative. realSum is the sum over all actual pairs of the integer sign, cast to reals, times weight(right)^m. For a nonempty face set and an actual pair, there is an orbit and the strict slope premise rules out identically zero local weights. Empty A is allowed, consistently: the unique empty pair has m=0, sign=1 and weight^0=1. No false universal nonvanishing for zero weights is claimed.

Concrete results quantify finite vertex, edge and dual-vertex types and M : N.ColoredDual D. Network gives edge endpoints. Duality contains connectivity of both graphs and the two cycle-space/cut-space equalities over the reals. ColoredDual adds simplicity of both networks, cubicity, a bipartition, a triangle in D for every primal vertex, and compatible orientation. It does not contain a Hamiltonicity or good-state existence field. Black(root) is black vertices other than root. nonroots is the complement of the root triangle's corners. system uses the triangles at Black(root). weights are triangle potentials of alpha. whiteCharge has charge 1 on white vertices and balancing negative charge at root. The current proofs obtain a flow from connectivity and zero total charge, rather than assume the desired conclusion.

Finite/ Fintype and DecidableEq arguments are standard finite enumeration/equality assumptions. Classical instances supply decisions without restricting the allowed finite objects. Nonempty Pair is explicit in all nonvanishing and existence results. The concrete hypotheses are satisfiable in the intended sphere examples; the full geometry-to-algebra dictionary is accepted upstream background, not re-formalised here.

Verdicts below concern each advertised part under this dictionary. A faithful algebraic theorem is not a machine-checked theorem about the paper's unformalised sphere object. Formal headers are quoted from submitted source; imported namespaces and the common parameters above are part of each header. Independently elaborated full types are saved in statements.out.

## 1. finite_difference

Formal source: `Devices/FiniteDifference.lean`, line 50.

```lean
theorem finite_difference (L : ι → R) (s : Finset ι) :
    (∀ a m, m < s.card → F L s a m = 0) ∧
      ∀ a, F L s a s.card = (-1 : R) ^ s.card * (s.card.factorial : R) * ∏ i ∈ s, L i
```

Paper counterpart: 4.7. Verdict: **stronger**. Any finite index set and any commutative ring. Both the below-degree zero and top-degree factorial product are proved. The paper is the real specialisation; no positivity of steps is required.

## 2. finite_difference_fin

Formal source: `Devices/FiniteDifference.lean`, line 82.

```lean
theorem finite_difference_fin (c : ℕ) (ω₀ : R) (L : Fin c → R) :
    (∀ m, m < c → ∑ S ∈ (univ : Finset (Fin c)).powerset,
        (-1 : R) ^ S.card * (ω₀ + ∑ i ∈ S, L i) ^ m = 0) ∧
      ∑ S ∈ (univ : Finset (Fin c)).powerset, (-1 : R) ^ S.card * (ω₀ + ∑ i ∈ S, L i) ^ c =
        (-1 : R) ^ c * (c.factorial : R) * ∏ i, L i
```

Paper counterpart: 4.7. Verdict: **stronger**. Same two conclusions on Fin c, for any commutative ring. Subsets encode bit strings bijectively. Degenerate rings are allowed but do not weaken the real instance.

## 3. prod_sum_of_signs

Formal source: `Devices/LocalSign.lean`, line 28.

```lean
theorem prod_sum_of_signs {ι : Type*} (S : Finset ι) (f : ι → ℤ)
    (hf : ∀ i ∈ S, f i = 1 ∨ f i = -1) :
    ∏ i ∈ S, f i = (-1) ^ (S.filter (fun i => f i = -1)).card ∧
      (S.card : ℤ) = ∑ i ∈ S, f i + 2 * (S.filter (fun i => f i = -1)).card
```

Paper counterpart: proof of 4.4. Verdict: **stronger**. For any finite family of integer signs, gives both the product by negative-factor count and the sum/count identity. This is the arithmetic subclaim used in the paper, independent of geometry.

## 4. paperSign_reverse

Formal source: `Devices/LocalSign.lean`, line 127.

```lean
theorem paperSign_reverse [Fintype A] (r : T.State X) (hrs : T.Partner r s)
    (hdisk : C.cyclicDelta r = 3 ∨ C.cyclicDelta r = -3) :
    paperSign (C.reverse r hrs) s = -paperSign r s
```

Paper counterpart: 4.4 first reversal. Verdict: **faithful**. A partner r, actual opposite cycle C, and its delta sum ±3 imply sign reversal. The disk premise is explicit for arbitrary triangle systems and is discharged in the concrete theorem. Not an unconditional theorem about arbitrary systems.

## 5. paperSign_partners_sum

Formal source: `Devices/LocalSign.lean`, line 155.

```lean
theorem paperSign_partners_sum [Fintype A] {M : Type*} [AddCommGroup M]
    (hdisk : ∀ r : T.Partners s, C.cyclicDelta r.val = 3 ∨ C.cyclicDelta r.val = -3)
    (weight : M) : (∑ r : T.Partners s, paperSign r.val s • weight) = 0
```

Paper counterpart: 4.5 first sentence. Verdict: **stronger**. Cancels the partners of one state for an arbitrary additive commutative group and constant group-valued weight. Requires the disk identity for all partners on the chosen cycle. The unweighted integer sum is the instance weight=1.

## 6. sign_orient

Formal source: `Devices/LocalSign.lean`, line 200.

```lean
theorem sign_orient (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (b : CycleClass P.next → Bool) :
    (P.orient b).val.sign = (-1) ^ (univ.filter (fun c => b c = true)).card * P.sign
```

Paper counterpart: 4.4 second reversal. Verdict: **faithful**. All cycle delta sums ±3; orient swaps the two corners on exactly the selected permutation orbits. The conclusion counts selected orbits, not faces.

## 7. sign_reverse_one

Formal source: `Devices/LocalSign.lean`, line 232.

```lean
theorem sign_reverse_one (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (c : CycleClass P.next) (b : CycleClass P.next → Bool) (hb : ∀ c', b c' = true ↔ c' = c) :
    (P.orient b).val.sign = -P.sign
```

Paper counterpart: 4.4 second reversal. Verdict: **faithful**. Specialises the preceding theorem with a Boolean function true exactly on the specified orbit. Such a Boolean function exists classically on the finite quotient; the condition is not contradictory.

## 8. sign_formula

Formal source: `Devices/LocalSign.lean`, line 270.

```lean
theorem sign_formula (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    Even (Fintype.card A + Fintype.card (CycleClass P.next)) ∧
      P.sign = (-1) ^ ((Fintype.card A + Fintype.card (CycleClass P.next)) / 2 + P.ccwCount)
```

Paper counterpart: 4.4 closed formula. Verdict: **faithful**. Even(n+c) and the stated integer sign exponent; ccwCount is the count of orbits whose delta sum is -3. This equals geometric counterclockwise count only with the aligned orientation convention.

## 9. I_zpow_rawIndexSum

Formal source: `Devices/LocalSign.lean`, line 289.

```lean
theorem I_zpow_rawIndexSum {r s : T.State X} (hrs : T.Partner r s) :
    Complex.I ^ rawIndexSum r s = Complex.I ^ Fintype.card A * (paperSign r s : ℂ)
```

Paper counterpart: arithmetic behind 4.10. Verdict: **stronger**. Every partner pair gives i^(raw sum)=i^n epsilon, without divisibility or disk hypotheses. Uses integer exponent on the left and natural exponent on i^n.

## 10. phase_eq_paperSign

Formal source: `Devices/LocalSign.lean`, line 303.

```lean
theorem phase_eq_paperSign {r s : T.State X} (hrs : T.Partner r s)
    (h3 : (3 : ℤ) ∣ rawIndexSum r s) :
    phase (rawIndexSum r s) = Complex.I ^ (-(Fintype.card A : ℤ)) * (paperSign r s : ℂ)
```

Paper counterpart: 4.10 phase sentence. Verdict: **faithful**. Requires 3 divides the raw sum, avoiding the truncating integer division trap in phase. Proves phase=i^(-n)epsilon.

## 11. paperSign_eq_I_pow_mul_phase

Formal source: `Devices/LocalSign.lean`, line 329.

```lean
theorem paperSign_eq_I_pow_mul_phase {r s : T.State X} (hrs : T.Partner r s)
    (h3 : (3 : ℤ) ∣ rawIndexSum r s) :
    (paperSign r s : ℂ) = Complex.I ^ Fintype.card A * phase (rawIndexSum r s)
```

Paper counterpart: 4.10 phase sentence. Verdict: **faithful**. Equivalent rearrangement epsilon=i^n phase with exactly the same partner and divisibility hypotheses.

## 12. three_dvd_rawIndexSum

Formal source: `Devices/LocalSign.lean`, line 336.

```lean
theorem three_dvd_rawIndexSum (P : T.Pair X)
    (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    (3 : ℤ) ∣ rawIndexSum P.left P.right
```

Paper counterpart: disk input to 4.10. Verdict: **faithful**. Cycle delta sums ±3 imply divisibility of the total by 3, using the actual orbit partition of the state permutation.

## 13. sign_eq_I_pow_mul_phase

Formal source: `Devices/LocalSign.lean`, line 343.

```lean
theorem sign_eq_I_pow_mul_phase (P : T.Pair X)
    (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3) :
    (P.sign : ℂ) = Complex.I ^ Fintype.card A * phase (rawIndexSum P.left P.right)
```

Paper counterpart: 4.10 phase sentence. Verdict: **faithful**. Combines the two preceding inputs for a Pair. Does not assert a height/flow correspondence or a polynomial identity with different weights.

## 14. sum_sign_eq_zero_of_no_good

Formal source: `Devices/RealSign.lean`, line 47.

```lean
theorem sum_sign_eq_zero_of_no_good
    (hdisk : ∀ (s : T.State X) (C : T.OppositeCycle s) (r : T.Partners s),
      C.cyclicDelta r.val = 3 ∨ C.cyclicDelta r.val = -3)
    (hnone : ∀ P : T.Pair X, ¬(T.oppositeGraph P.right).IsAcyclic)
    (F : T.State X → ℝ) :
    (∑ P : T.Pair X, (P.sign : ℝ) * F P.right) = 0
```

Paper counterpart: 4.5 second sentence. Verdict: **weaker**. Proves only the no-acyclic-partner case: if every pair has cyclic Q_right, the total weighted sum is zero. The paper states the full equality to a sum over good states, with their unique partners. Neither that equality nor partner uniqueness is proved here. README table acknowledges the case used, but its later whole-lemma claim is too broad.

## 15. weight_orient

Formal source: `Devices/RealSign.lean`, line 77.

```lean
theorem weight_orient (P : T.Pair X) (w : A → Fin 3 → ℝ) (b : CycleClass P.next → Bool) :
    weight w (P.orient b).val.right =
      weight w P.right + ∑ c ∈ univ.filter (fun c => b c = true), P.step w c
```

Paper counterpart: 4.6 additivity used in 4.8. Verdict: **different**. Exact algebraic additivity for arbitrary real local weights w and step=-cycleSlope. No face paths, per-face heights, positive integer white-face count, or equality to the paper weights occurs. If original delta=-3, slope>0 and reversing gives a negative step; positive steps are from clockwise to counterclockwise, as in the current paper.

## 16. group_sum

Formal source: `Devices/RealSign.lean`, line 110.

```lean
theorem group_sum (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (w : A → Fin 3 → ℝ) (m : ℕ) :
    (∑ Q : P.Group, (Q.val.sign : ℝ) * weight w Q.val.right ^ m) =
      (P.sign : ℝ) * Blueprint.F (P.step w) univ (weight w P.right) m
```

Paper counterpart: 4.8 class calculation. Verdict: **faithful**. On Group defined by fixed third corner at each face, the weighted real-sign sum equals epsilon(P) times the finite difference at the chosen representative. Uses exact orient/groupEquiv, not a newly invented quotient.

## 17. group_sum_card

Formal source: `Devices/RealSign.lean`, line 131.

```lean
theorem group_sum_card (P : T.Pair X) (w : A → Fin 3 → ℝ)
    (hsign : ∀ c, (P.cycleDelta c = -3 ∧ 0 < P.cycleSlope w c) ∨
      (P.cycleDelta c = 3 ∧ P.cycleSlope w c < 0)) :
    (∑ Q : P.Group, (Q.val.sign : ℝ) * weight w Q.val.right ^ Fintype.card (CycleClass P.next)) =
      (-1) ^ ((Fintype.card A + Fintype.card (CycleClass P.next)) / 2 +
        Fintype.card (CycleClass P.next)) * (Fintype.card (CycleClass P.next)).factorial *
        ∏ c, |P.cycleSlope w c|
```

Paper counterpart: 4.8 minimum-size class calculation. Verdict: **faithful**. With m equal to this pair orbit count, gives the common sign times m! times the product of absolute slopes. Strict slope signs are explicit. Geometric L and its integrality are not asserted; absolute slopes play that role.

## 18. group_sum_lt

Formal source: `Devices/RealSign.lean`, line 188.

```lean
theorem group_sum_lt (P : T.Pair X) (hdisk : ∀ c, P.cycleDelta c = 3 ∨ P.cycleDelta c = -3)
    (w : A → Fin 3 → ℝ) {m : ℕ} (hm : m < Fintype.card (CycleClass P.next)) :
    (∑ Q : P.Group, (Q.val.sign : ℝ) * weight w Q.val.right ^ m) = 0
```

Paper counterpart: 4.8 larger-class calculation. Verdict: **faithful**. The class contribution vanishes for m less than its orbit count, for arbitrary local real weights. No positivity premise is needed in this case.

## 19. realSum_ne_zero

Formal source: `Devices/RealSign.lean`, line 219.

```lean
theorem realSum_ne_zero (hex : Nonempty (T.Pair X)) (w : A → Fin 3 → ℝ)
    (hsign : ∀ (P : T.Pair X) c,
      (P.cycleDelta c = -3 ∧ 0 < P.cycleSlope w c) ∨
      (P.cycleDelta c = 3 ∧ P.cycleSlope w c < 0)) :
    realSum (T
```

Paper counterpart: 4.8 nonvanishing. Verdict: **different**. Nonempty Pair and strict signed slopes imply nonzero realSum at minCycles over chosen class representatives. The formal conclusion is only nonzero, not the full equality advertised in its docstring. Equality appears inside the proof. Identification of this m with the minimum over all pairs remains T1.

## 20. forest_pair_of_disk_circulation_real

Formal source: `Devices/RealSign.lean`, line 262.

```lean
theorem forest_pair_of_disk_circulation_real (hex : Nonempty (T.Pair X))
    (hdisk : ∀ (s : T.State X) (C : T.OppositeCycle s) (r : T.Partners s),
      C.cyclicDelta r.val = 3 ∨ C.cyclicDelta r.val = -3)
    (w : A → Fin 3 → ℝ)
    (hsign : ∀ (P : T.Pair X) c,
      (P.cycleDelta c = -3 ∧ 0 < P.cycleSlope w c) ∨
      (P.cycleDelta c = 3 ∧ P.cycleSlope w c < 0)) :
    ∃ P : T.Pair X, (T.oppositeGraph P.right).IsAcyclic
```

Paper counterpart: 4.8 existence. Verdict: **faithful**. Same abstract hypotheses and conclusion as upstream: nonempty Pair, every opposite disk identity, and a local real weight with the strict cycle-sign condition imply a pair with acyclic opposite graph. Paper good state includes one root per component, so translating the conclusion still uses B4. This does not define good state to make existence automatic.

## 21. sign_reverse_opposite

Formal source: `Devices/Concrete.lean`, line 34.

```lean
theorem sign_reverse_opposite {s r : M.State root} (C : (M.system root).OppositeCycle s)
    (hrs : (M.system root).Partner r s) :
    paperSign (C.reverse r hrs) s = -paperSign r s
```

Paper counterpart: 4.4 first reversal. Verdict: **faithful**. Specialises to any ColoredDual and partner pair; obtains disk hypotheses from upstream. Unconditional means relative to this substantial structure, not for every arbitrary graph.

## 22. sign_orient_concrete

Formal source: `Devices/Concrete.lean`, line 42.

```lean
theorem sign_orient_concrete (P : (M.system root).Pair (M.nonroots root))
    (b : CycleClass P.next → Bool) :
    (P.orient b).val.sign = (-1) ^ (Finset.univ.filter (fun c => b c = true)).card * P.sign
```

Paper counterpart: 4.4 second reversal. Verdict: **faithful**. For a pair of the concrete system and arbitrary Boolean orbit selection. Finite V,E,F and ColoredDual encode the geometric/algebraic setting.

## 23. sign_formula_concrete

Formal source: `Devices/Concrete.lean`, line 48.

```lean
theorem sign_formula_concrete (P : (M.system root).Pair (M.nonroots root)) :
    Even (Fintype.card (M.Black root) + Fintype.card (CycleClass P.next)) ∧
      P.sign = (-1) ^ ((Fintype.card (M.Black root) + Fintype.card (CycleClass P.next)) / 2 +
        P.ccwCount)
```

Paper counterpart: 4.4 closed formula. Verdict: **faithful**. Counts nonroot black vertices and permutation cycles. Root need not have an explicit black proof in the binders; a pair is still required. No extra positivity or nonemptiness is hidden in the instance arguments.

## 24. sign_eq_I_pow_mul_phase_concrete

Formal source: `Devices/Concrete.lean`, line 57.

```lean
theorem sign_eq_I_pow_mul_phase_concrete (P : (M.system root).Pair (M.nonroots root)) :
    (P.sign : ℂ) = Complex.I ^ Fintype.card (M.Black root) *
      phase (rawIndexSum P.left P.right)
```

Paper counterpart: 4.10 phase sentence. Verdict: **faithful**. Every supplied pair satisfies epsilon=i^n phase, with n=card Black(root). The orientation comparison to a drawing is informal; relative to indexDelta this is exact.

## 25. forest_pair_real

Formal source: `Devices/Concrete.lean`, line 65.

```lean
theorem forest_pair_real (hex : Nonempty ((M.system root).Pair (M.nonroots root))) :
    ∃ P : (M.system root).Pair (M.nonroots root),
      ((M.system root).oppositeGraph P.right).IsAcyclic
```

Paper counterpart: 4.8 existence. Verdict: **faithful**. Nonempty concrete Pair implies existence of a pair with acyclic Q_right. Same statement as upstream forest_pair. Finite-type and ColoredDual premises remain; README wording no hypotheses left is only about disk and circulation premises.

## 26. realSum_ne_zero_concrete

Formal source: `Devices/Concrete.lean`, line 81.

```lean
theorem realSum_ne_zero_concrete (hex : Nonempty ((M.system root).Pair (M.nonroots root)))
    (α : E → ℝ) (hα : N.boundary α = whiteCharge M.black root) :
    realSum (T
```

Paper counterpart: 4.8 nonvanishing. Verdict: **different**. Requires Nonempty Pair and a supplied real edge flow alpha with boundary whiteCharge. Its weight is M.weights alpha root. Neither arbitrary zero weights nor paper face-path heights are substituted without proof.

## 27. card_edgeSet_add_sinks

Formal source: `Devices/Outdegree.lean`, line 65.

```lean
theorem card_edgeSet_add_sinks [Finite V] :
    Nat.card G.edgeSet + Nat.card {v : V // o.out v = none} = Nat.card V
```

Paper counterpart: 3.7 edge count. Verdict: **stronger**. Every finite simple graph with OutOrientation satisfies edges+sinks=vertices, without connectedness. out_adj,covers,one_way ensure exactly one chosen tail per edge.

## 28. component_count

Formal source: `Devices/Outdegree.lean`, line 81.

```lean
theorem component_count [Finite V] (hG : G.Connected) :
    Nat.card G.edgeSet + Nat.card {v : V // o.out v = none} = Nat.card V ∧
      Nat.card {v : V // o.out v = none} ≤ 1 ∧
      (Nat.card {v : V // o.out v = none} = 1 → G.IsTree) ∧
      (Nat.card {v : V // o.out v = none} = 0 →
        ¬G.IsAcyclic ∧ ∀ x y, G.Adj x y → ¬G.IsBridge s(x, y) →
          (G.deleteEdges {s(x, y)}).IsTree)
```

Paper counterpart: 3.7 component conclusions. Verdict: **weaker**. For one finite connected graph, gives the count, at most one sink, tree if one sink, and if zero sinks a cycle exists and deleting any nonbridge edge leaves a tree. This faithfully encodes the component conclusions, but omits the lemma first sentence that every cycle is directed, and does not apply the orientation to Q_s.

## 29. perfectMatching_unique

Formal source: `Devices/TreeMatching.lean`, line 20.

```lean
theorem IsAcyclic.perfectMatching_unique (hG : G.IsAcyclic) {M M' : G.Subgraph}
    (hM : M.IsPerfectMatching) (hM' : M'.IsPerfectMatching) : M = M'
```

Paper counterpart: Section 7 which cycles arise; also Section 3 prose. Verdict: **faithful**. Finite graph, acyclic, two perfect-matching subgraphs imply equality. Perfectness includes spanning, so isolated vertices do not create false witnesses. It is a uniqueness theorem, not existence and not the complete recovery/injectivity remark.

## Whole-package qualifications

The 29-entry list names headline results, not every new declaration. Auxiliary lemmas and definitions are also in the compiled files. Axiom closure of a headline result includes its used auxiliaries. No claim here says that every lemma in Mathlib has been independently audited.

The README's claim that all of Lemma 4.5 is checked is too broad: its second sentence is only proved in the no-good-pair case. Its counterclockwise-positive-L wording also needs correction: step=-slope is positive when reversing an originally clockwise cycle. The current paper states that direction correctly. The formal existence result is unaffected.

TODO T5 is false as written. It strengthens “a cycle is produced iff its recovered state is good” to “every eligible Hamiltonian cycle has a good recovered state”. The hexagonal-prism enumeration gives four eligible cycles, two with non-good recovered state. See numerical.json and REPORT.md. Consequently the all-checks condition for updating canonical statuses is not met.
