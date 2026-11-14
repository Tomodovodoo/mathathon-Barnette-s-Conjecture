# Actual Lean statement extracts

Read from openai/math commit 4eaee87548250b2682affda7d05d947c05554bae. These are declaration headers from the existing upstream clone, not transcriptions from the earlier report. File-level variables and namespaces remain in the source. Our prose replaces the second network with the face-incidence relation of G; that interpretation is proved in Lemmas 2 and 3. No fresh Lean build was run by this agent.

## BMatching.lean:403

```lean
theorem pair_nonempty (hcut : N.ThreeEdgeConnected) (htr : N.TrivialThreeCuts)
    (root : V) (hr : M.black root) : Nonempty ((M.system root).Pair (M.nonroots root))
```

## Bonds.lean:163

```lean
lemma Bond.connected_shore (h : N.graph.Connected) {A : Finset V} (hA : N.Bond A)
    (hin : A.Nonempty) (hout : ∃ v, v ∉ A) :
    (N.graph.induce {v | v ∈ A}).Connected
```

## Circulation.lean:154

```lean
lemma boundary_of_sum_zero (h : N.graph.Connected) (b : V → ℝ)
    (hb : ∑ v, b v = 0) : ∃ x, N.boundary x = b
```

## Circulation.lean:183

```lean
def whiteCharge (black : V → Prop) (root : V) : V → ℝ
```

## Circulation.lean:208

```lean
lemma whiteCharge_cut_integral (black : V → Prop) (root : V) (A : Finset V)
    (hr : root ∉ A) (α : E → ℝ) (hα : N.boundary α = whiteCharge black root)
    (c : ℝ) (x : E → ℝ)
    (hx : x = c • N.gradient (fun v => if v ∈ A then 1 else 0)) :
    ∑ e, α e * x e = c * ((A.filter fun v => ¬black v).card : ℝ)
```

## Circulation.lean:227

```lean
lemma white_positive_of_boundary (black : V → Prop)
    (hc : ∀ e, black (N.tail e) ↔ ¬black (N.head e)) (A : Finset V)
    (hcount : (N.cut A).card = 2 * (N.blackCut black A).card + 3) :
    0 < (A.filter fun v => ¬black v).card
```

## DiskRegions.lean:252

```lean
theorem region_euler (h : N.Duality D) (A : Finset V)
    (hA : (N.graph.induce {v | v ∈ A}).Connected)
    (hAc : (N.graph.induce {v | v ∉ A}).Connected)
    (sD : D.Simple) (face : ∀ v, D.Triangle (N.star v)) :
    A.card + (N.regionVertices D A).card = (N.regionEdges A).card + 1
```

## FlowCircuits.lean:71

```lean
theorem Duality.circuit_cut (h : N.Duality D) (x : E → ℝ)
    (hx : D.FlowCircuit x) (root : V) :
    ∃ (A : Finset V) (c : ℝ), A.Nonempty ∧ root ∉ A ∧ c ≠ 0 ∧
      x = c • N.gradient (fun v => if v ∈ A then 1 else 0) ∧
      N.cut A = D.flowSupport x
```

## ForestMatching.lean:51

```lean
lemma tree_matching (black : V → Prop)
    (hc : ∀ e, black (N.tail e) ↔ ¬black (N.head e))
    (H : Finset E) (hi : Function.Injective (N.restrict (Subtype.val : H → E)).boundary)
    (root : V) (_hr : black root)
    (hd : ∀ v, black v → ((N.star v).filter (fun e => e ∈ H)).card = if v = root then 1 else 2)
    (hbal : Fintype.card {v // black v} = Fintype.card {v // ¬black v}) :
    ∃ P : Finset E, P ⊆ H ∧ ∀ v, ((N.star v).filter fun e => e ∈ P).card = 1
```

## ForestMatching.lean:176

```lean
lemma matching_cut_balance (hN : N.Simple) (h3 : N.graph.IsRegularOfDegree 3)
    (black : V → Prop) (hc : ∀ e, black (N.tail e) ↔ ¬black (N.head e))
    (P : Finset E) (hd : ∀ v, ((N.star v).filter fun e => e ∈ P).card = 1)
    (A : Finset V) (hcut : N.cut A ⊆ P) :
    (N.cut A).card = 2*(N.blackCut black A).card
```

## ForestMatching.lean:226

```lean
lemma recovery_matching (P : (M.system root).Pair (M.nonroots root)) (hr : M.black root)
    (ha : ((M.system root).oppositeGraph P.right).IsAcyclic) (i : Fin 3) :
    ∃ S : Finset E, S ⊆ (M.removed P i)ᶜ ∧ ∀ v, ((N.star v).filter fun e => e ∈ S).card = 1
```

## ForestMatching.lean:307

```lean
lemma selectNet_forest (s : M.State root) (P : Finset E)
    (hd : ∀ v, ((N.star v).filter fun e => e ∈ P).card = 1)
    (hi : ∀ t : M.Black root, D.Incident (N.matchingEdge P hd t.val) (s.value t)) :
    (M.selectNet s P hd).graph.IsAcyclic
```

## ForestMatching.lean:338

```lean
lemma selected_forest (s : M.State root) (P : Finset E)
    (hd : ∀ v, ((N.star v).filter fun e => e ∈ P).card = 1) (_hr : M.black root)
    (hi : ∀ t : M.Black root, D.Incident (N.matchingEdge P hd t.val) (s.value t))
    (i : Fin 3) (he0 : N.matchingEdge P hd root = (M.face root).edge i) :
    (D.restrict (Subtype.val : P → E)).graph.IsAcyclic
```

## ForestMatching.lean:375

```lean
lemma recover_connected_complement (Q : (M.system root).Pair (M.nonroots root))
    (hr : M.black root) (ha : ((M.system root).oppositeGraph Q.right).IsAcyclic) (i : Fin 3) :
    ∃ P : Finset E, (M.face root).edge i ∈ P ∧
      (∀ v, ((N.star v).filter fun e => e ∈ P).card = 1) ∧
      (N.restrict (Subtype.val : ↥(Pᶜ) → E)).graph.Connected
```

## Gluing.lean:94

```lean
lemma cap_glue_matching (A : Finset V) (P : Finset (N.regionEdges A))
    (Q : Finset (N.regionEdges Aᶜ))
    (hP : ∀ v, (((N.cap A).star v).filter (· ∈ P)).card = 1)
    (hQ : ∀ v, (((N.cap Aᶜ).star v).filter (· ∈ Q)).card = 1)
    (hcut : ∀ e ∈ N.cut A, e ∈ P.image Subtype.val ↔ e ∈ Q.image Subtype.val) :
    ∀ v, ((N.star v).filter (· ∈ P.image Subtype.val ∪ Q.image Subtype.val)).card = 1
```

## Gluing.lean:167

```lean
lemma cap_glue_connected (hN : N.Simple) (hc : N.graph.IsRegularOfDegree 3)
    (h3 : N.ThreeEdgeConnected) (A : Finset V) (hA : (N.cut A).card = 3)
    (ha : 2 ≤ A.card) (ho : 2 ≤ Aᶜ.card)
    (P : Finset (N.regionEdges A)) (Q : Finset (N.regionEdges Aᶜ))
    (hP : ∀ v, (((N.cap A).star v).filter (· ∈ P)).card = 1)
    (hQ : ∀ v, (((N.cap Aᶜ).star v).filter (· ∈ Q)).card = 1)
    (hPc : ((N.cap A).restrict (Subtype.val : ↥Pᶜ → N.regionEdges A)).graph.Connected)
    (hQc : ((N.cap Aᶜ).restrict (Subtype.val : ↥Qᶜ → N.regionEdges Aᶜ)).graph.Connected)
    (hcut : ∀ e ∈ N.cut A, e ∈ P.image Subtype.val ↔ e ∈ Q.image Subtype.val) :
    (N.restrict (Subtype.val : ↥(P.image Subtype.val ∪ Q.image Subtype.val)ᶜ → E)).graph.Connected
```

## Gluing.lean:244

```lean
private theorem matching_strong (n : ℕ) :
    ∀ {V : Type uV} {E : Type uE} {F : Type uF} [Fintype V] [Fintype E] [Fintype F]
      (N : Network V E) (D : Network F E), Fintype.card V = n →
      N.Duality D → N.Simple → N.graph.IsRegularOfDegree 3 → N.ThreeEdgeConnected →
      ∀ (black : V → Prop), (∀ e, black (N.tail e) ↔ ¬black (N.head e)) →
      ∀ e : E, ∃ P : Finset E, e ∈ P ∧ (∀ v, ((N.star v).filter (· ∈ P)).card = 1) ∧
        (N.restrict (Subtype.val : ↥Pᶜ → E)).graph.Connected
```

## Gluing.lean:294

```lean
theorem Duality.connected_complement_matching (h : N.Duality D) (hN : N.Simple)
    (hc : N.graph.IsRegularOfDegree 3) (h3 : N.ThreeEdgeConnected)
    (black : V → Prop) (hb : ∀ e, black (N.tail e) ↔ ¬black (N.head e)) (e : E) :
    ∃ P : Finset E, e ∈ P ∧ (∀ v, ((N.star v).filter (· ∈ P)).card = 1) ∧
      (N.restrict (Subtype.val : ↥Pᶜ → E)).graph.Connected
```

## Matching.lean:330

```lean
lemma removed_acyclic (P : (M.system root).Pair (M.nonroots root))
    (ha : ((M.system root).oppositeGraph P.right).IsAcyclic) (i : Fin 3) :
    (D.restrict (Subtype.val : M.removed P i → E)).graph.IsAcyclic
```

## Matching.lean:342

```lean
lemma remainder_connected (P : (M.system root).Pair (M.nonroots root))
    (ha : ((M.system root).oppositeGraph P.right).IsAcyclic) (i : Fin 3) :
    (N.restrict (Subtype.val : ↥((M.removed P i)ᶜ) → E)).graph.Connected
```

## Matching.lean:444

```lean
lemma remainder_black_degree (P : (M.system root).Pair (M.nonroots root)) (hr : M.black root)
    (i : Fin 3) (v : V) (hv : M.black v) :
    ((N.star v).filter fun e => e ∈ (M.removed P i)ᶜ).card = if v = root then 1 else 2
```

## PairPolynomials.lean:423

```lean
theorem forest_pair_of_disk_circulation (hex : Nonempty (@Pair A V T X))
    (hdisk : ∀ (s : T.State X) (C : T.OppositeCycle s) (r : T.Partners s),
      C.cyclicDelta r.val = 3 ∨ C.cyclicDelta r.val = -3)
    (w : A → Fin 3 → ℝ)
    (hsign : ∀ (P : @Pair A V T X) c,
      (P.cycleDelta c = -3 ∧ 0 < P.cycleSlope w c) ∨
      (P.cycleDelta c = 3 ∧ P.cycleSlope w c < 0)) :
    ∃ P : @Pair A V T X, (T.oppositeGraph P.right).IsAcyclic
```

## StateDisk.lean:129

```lean
theorem mixed_corner_on_boundary (h : N.Duality D) (sD : D.Simple)
    (face : ∀ v, D.Triangle (N.star v)) (A : Finset V) {z : F}
    (hzin : z ∈ N.regionVertices D A) (hzout : z ∈ N.regionVertices D Aᶜ) :
    ∃ e ∈ N.cut A, D.Incident e z
```

## StateDisk.lean:260

```lean
theorem state_disk_count (h : N.Duality D) (sD : D.Simple)
    (face : ∀ v, D.Triangle (N.star v)) (black : V → Prop)
    (hc : ∀ e, black (N.tail e) ↔ ¬black (N.head e)) (root : V)
    (m : V → F)
    (hm_inj : Set.InjOn m {v | black v ∧ v ≠ root})
    (hm_face : ∀ v, black v → v ≠ root → m v ∈ Set.range (face v).corner)
    (hm_range : ∀ z, z ∉ Set.range (face root).corner ↔
      ∃ v, black v ∧ v ≠ root ∧ m v = z)
    (C : Barnette.CycleCoordinates D.graph)
    (hchoice : ∀ i, N.blackEndpoint black (D.cycleEdge C i) ≠ root ∧
      m (N.blackEndpoint black (D.cycleEdge C i)) = C.vertex i)
    (A : Finset V) (hroot : root ∉ A) (hcut : N.cut A = D.cycleEdges C) :
    (A.filter black).card + (N.cut A).card =
      (N.regionVertices D A).card + (N.blackCut black A).card
```

## StateDisk.lean:428

```lean
lemma disk_boundary_imbalance (h : N.Duality D) (sN : N.Simple)
    (hdeg : N.graph.IsRegularOfDegree 3) (sD : D.Simple)
    (face : ∀ v, D.Triangle (N.star v))
    (black : V → Prop) (hc : ∀ e, black (N.tail e) ↔ ¬black (N.head e))
    (A : Finset V) (hA : (N.graph.induce {v | v ∈ A}).Connected)
    (hAc : (N.graph.induce {v | v ∉ A}).Connected)
    (hm : (A.filter black).card + (N.cut A).card =
      (N.regionVertices D A).card + (N.blackCut black A).card) :
    (N.cut A).card = 2 * (N.blackCut black A).card + 3
```

## StateDisk.lean:442

```lean
theorem state_disk_delta (h : N.Duality D) (sN : N.Simple)
    (hdeg : N.graph.IsRegularOfDegree 3) (sD : D.Simple)
    (face : ∀ v, D.Triangle (N.star v)) (black : V → Prop)
    (hc : ∀ e, black (N.tail e) ↔ ¬black (N.head e)) (root : V)
    (m : V → F)
    (hm_inj : Set.InjOn m {v | black v ∧ v ≠ root})
    (hm_face : ∀ v, black v → v ≠ root → m v ∈ Set.range (face v).corner)
    (hm_range : ∀ z, z ∉ Set.range (face root).corner ↔
      ∃ v, black v ∧ v ≠ root ∧ m v = z)
    (C : Barnette.CycleCoordinates D.graph)
    (hchoice : ∀ i, N.blackEndpoint black (D.cycleEdge C i) ≠ root ∧
      m (N.blackEndpoint black (D.cycleEdge C i)) = C.vertex i) :
    ∃ (A : Finset V) (c : ℝ), A.Nonempty ∧ root ∉ A ∧ (c = 1 ∨ c = -1) ∧
      D.cycleFlow C = c • N.gradient (fun v => if v ∈ A then 1 else 0) ∧
      N.cut A = D.cycleEdges C ∧
      (N.cut A).card = 2 * (N.blackCut black A).card + 3 ∧
      N.blackDelta D black C = -3*c
```

## ThreeCuts.lean:230

```lean
lemma cap_threeConnected (hN : N.ThreeEdgeConnected) (A : Finset V) (hA : Aᶜ.Nonempty) :
    (N.cap A).ThreeEdgeConnected
```

## ThreeCuts.lean:352

```lean
lemma cap_simple (hN : N.Simple) (hc : N.graph.IsRegularOfDegree 3) (h3 : N.ThreeEdgeConnected)
    (A : Finset V) (hcut : (N.cut A).card = 3) (hA : 2 ≤ A.card) (ho : Aᶜ.Nonempty) :
    (N.cap A).Simple
```

## ThreeCuts.lean:360

```lean
lemma cap_cubic (hN : N.Simple) (hc : N.graph.IsRegularOfDegree 3) (h3 : N.ThreeEdgeConnected)
    (A : Finset V) (hcut : (N.cut A).card = 3) (hA : 2 ≤ A.card) (ho : Aᶜ.Nonempty) :
    (N.cap A).graph.IsRegularOfDegree 3
```

## ThreeCuts.lean:381

```lean
lemma cap_coloring (hN : N.Simple) (hc : N.graph.IsRegularOfDegree 3)
    (black : V → Prop) (hb : ∀ e, black (N.tail e) ↔ ¬black (N.head e))
    (A : Finset V) (hA : (N.cut A).card = 3) :
    ∀ e, N.capBlack black A ((N.cap A).tail e) ↔ ¬N.capBlack black A ((N.cap A).head e)
```
