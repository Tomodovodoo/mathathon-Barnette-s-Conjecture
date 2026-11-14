# Correspondence between the three proofs

Summary.
1. The three papers run the same engine: pairs of disjoint states, a sign that both cycle reversals flip, positive weights on spoke cycles, and a count done two ways. The translation of that engine is exact, node for node.
2. They differ in substance in four places: the hypothesis for the first pair, the final step from the white tree to the cycle, global versus per-component counting, and whether the count is turned into a walk.
3. Li's `cw'` is `-J`. Li's Claim 25 is the disk identity. Li's marks are the monomials of the Taylor coefficient of order `c_min`, for one concrete choice of weights.
4. The trees paper proves more at three nodes (exact obstruction, unique mate, determinant sign). Li's proof of Lemma 9 already contains the exact obstruction without saying so.
5. The three notions "`Q_s` is a forest", "cycle-breaking" and "tree matching" agree for a pair and differ for a single state.

Paper keys: **O** = OpenAI, **L** = Li, **T** = trees. Shared notation is that of `research/BRIEF.md`. Node ids refer to `audit-openai.md`, `audit-li.md`, `audit-trees.md`.

## 1. Objects

Li works in the primal graph `G`. The other two work in the dual `T = G*`. The bridge is `aux(G)`: it is `T` with a centre in every face joined to the corners, and `G` drawn on those centres. Its three vertex classes are black vertices of `G` (black faces of `T`), white vertices of `G` (white faces of `T`), and faces of `G` (vertices of `T`).

| Shared name | O | L | T |
| --- | --- | --- | --- |
| black face `t` of `T` | black triangle | black vertex `b` | black face, or its centre |
| white face of `T` | white triangle | white vertex `w` | white triangle `y` |
| vertex of `T` | vertex | face-vertex `f` | vertex |
| `t0`, roots `R` | outer black face, roots | `b0`, root face-vertices `F(G) ∩ N(b0)` | `t0`, `R` |
| `e0`, `y0` | edge of `t0`, white triangle across it | `e0 = b0 w0`, `w0` | `e0`, `y0` |
| `H` (all spokes) | `H` of 6.1 | `G_FB` | `H` |
| `H0 = H - t0` | `H0` of 5.2 | not named | `H0` |
| `B` (incidence graph on `A`, `X`) | "incidence graph on `A` and `X`" | `H = G_FB - N[b0]` | `B` |
| state | bijection `r: A -> X` | perfect matching of Li's `H` | perfect matching of `B` |
| pair `(r, s)` | pair | ordered 2-factor `(M1, M2)` with `M1 = r`, `M2 = s` | element of `P` |
| `D(r, s)` | edges `r(t) -> s(t)` of `T` | cycles of `H[M1 ∪ M2]`; `orient(M1, M2)` runs `s(t) -> t -> r(t)`, so it is `D` reversed and moved onto spokes | `D_{r,s}` |
| `Q_s` | edge opposite `s(t)` | Li's `H - M2` is `Q_s` with each edge subdivided and the roots removed | `Q_s` |
| the good condition | `Q_s` is a forest | cycle-breaking: Li's `H - M2` is acyclic | tree matching: `H - s` is a spanning tree |
| `H - s` | "the remainder" in 6.1 | `T_FB = G_FB - M2` | `H - s` |
| white tree | spanning tree on white triangles | `T_W = M2*` | `W_s` |
| selected set `P` | `P ⊂ E(T)`, one side per face | perfect matching `P ⊂ E(G)` (the same edges, seen in `G`) | `P` |
| `P0` moved onto spokes | not used | `trace_B(P)` with its orientation | not used |
| subdivided white tree | not used | `T_BW`, spanning tree of `G - b0` | not used |
| local turn | `δ(r(t), s(t)) = ±1` | `τ(b) ∈ {0, 1}` | `δ` |
| winding count | `J = (1/3) Σ δ` | `cw' = #cw - #ccw` | `J` |
| sign of a pair | `i^J` | `(-1)^{cw}`, `cw = ⌊cw'/2⌋ mod 2` | `ε = (-1)^{(n+J)/2}` |
| weights | real `a(t, v)`, unit circulation on each bounded face of `H0` | signed number of white-vertex rays crossing the spoke | integers `0 ≤ a ≤ 6n` |
| weight of `s` | `ω(s)` | number of available marks `(w, e2)`, counted with `dir` | `ω(s)`, tokens `W(s)` |
| the count | `Z(x) = Σ i^J e^{xω(s)}` | `|O+| - |O-|` | `Z_C(z) = Σ ε z^{ω(s)}` on one component; `Ω_m` |
| obstruction | separating triangle | non-trivial 3-edge cut | separating triangle with black inner boundary |
| cap | triangle glued on the separating cycle | the vertex `x` of `G/X` | cap |

Name clash to watch. `H` means the full spoke graph in O and T, and the reduced graph `B` in L.

## 2. Lemmas

"Exact" means the statements are the same after translation and the proofs use the same ideas. Status tags are for the translation claim.

| Node | O | L | T | Translation |
| --- | --- | --- | --- | --- |
| counts `|A| = |X|` | (2.1) | not stated, needed for Theorem 10 (`Q1a`) | (2) | exact. L omits it. `PROVED-HERE` |
| a pair exists | Prop. 3.1 (`C3`) | Lemma 9 (`C6`) | Section 3 (`F23`) | T proves more: an equivalence, under a weaker hypothesis. L's proof yields the T hypothesis (note 3.7). The proofs differ: O and T bound every `U` component by component, L takes a minimal deficient set |
| disk identity | Lemma 4.1 (`C4`) | Claim 25 (`C25`) | Lemma 4.1 (`C41`) | exact (note 3.2). T adds "odd length" |
| `J` is an integer and counts cycles | (5.1) (`N2`) | Claim 26 (`C26`) | (8) | exact, `cw' = -J` (note 3.1) |
| `D`-reversal flips the sign | inside (5.4) | Lemma 16 | Lemma 4.2, move (a) | exact |
| `Q_s`-reversal flips the sign | Lemma 5.2 (`C52`) | Lemma 17 (`C17`) | Lemma 4.2, move (b) | exact |
| cycles of `Q_s` are directed | Lemma 5.2, first paragraph (`K1`) | Section 4.6 (`I1a`) | Prop. 2.1 | T proves more: all components classified, `2^k` mates |
| cancellation for fixed `s` | Lemma 5.2 | `ι1` | `Y1`, and `β` in the walk | exact |
| positive weights | Lemma 5.3 and (5.3) (`C53`, `N4`) | half-rays, Remark 19, Definition 20 | Lemma 5.1 (`C51`) | same circulation. L's weights are one concrete choice (note 3.3). T makes them bounded integers. The slide across subdisks appears in O and T only |
| regrouping by `D` | 5.3 (`N3`) | first case of `ι2` | `Y2`, rule (1) of `α` | exact |
| the count is not zero | Taylor coefficient of order `c_min` (`N6`, `N7`) | fixed points of `ι2` share a sign and exist (`I5`, `I6`, `B`) | coefficient of `(z-1)^m` (`Y3`); parity along the walk (`M5`) | same number `Σ_D Π_C (L+ - L-)` over the groups with fewest cycles (note 3.3). Different in form: analytic, bijective, polynomial, path-following |
| forest pair gives a spanning tree of `H` | Lemma 6.1 and `W2` | Lemma 8 (`C3`) | (3) and Prop. 2.1 | exact for pairs (note 3.5) |
| white tree | 6.1 with Lemma 2.1 | Corollary 27 | 7.1 | exact |
| the selected set | 6.1 (`W3`, `W4`) | Claim 31 | 7.1 | exact, the same set `P` (note 3.6) |
| `P` gives one cycle | Lemma 6.2 (`C62`), then Lemma 2.1 | Lemma 30 (`C5`) | Lemma 7.1 (`R1c`) | differ in substance. O and T use the disk identity a second time. L does not (note 4.2) |
| two induced trees | end of 6.2 (`S`) | not needed | Lemma 7.1 | L stays in `G` and skips this node |
| gluing | Section 7 (`C1g`) | Appendix C (`A1` to `A4`) | 7.3 (`G73`) | exact between O and L (note 3.8). T cuts only at black-inner triangles |
| the dual is simple | proof of Theorem 1.1 (`O1`) | implicit in "hexagonal faces" and in the simplicity of `aux(G)` | proof of Theorem 1.1 | exact |
| edge avoidance | Corollary 7.1 | Theorem 3 | Theorem 1.1 | exact |
| no counterpart | Corollary 7.2 | none | Lemma 6.1, Prop. 6.2, Theorems 5.2, 5.3, 1.2 | |

## 3. Notes on the translations

### 3.1 `cw' = -J` and the three signs (`PROVED-HERE`)

At a black vertex `b = t`, Li sets `τ = 1` when the turn from the `M2`-edge to the `M1`-edge, through the sector without the third edge, is clockwise. With `M1 = r` and `M2 = s` this is the turn from the spoke to `s(t)` to the spoke to `r(t)`. It is clockwise exactly when going `r(t) -> s(t)` runs counterclockwise around `t`, that is when `δ(r(t), s(t)) = 1`. So `τ = (1 + δ)/2` and `Σ τ = (n + 3J)/2`. Claim 26 with `|V(H_Li)| = 2n` then reads

    cw' = n/3 - (2/3)(n + 3J)/2 = -J.

This matches the orientations: `orient(M1, M2)` traverses each triangle from `s(t)` to `r(t)`, so a clockwise cycle of Li is a counterclockwise cycle of `D`.

Signs. `J ≡ n mod 2`. Then `i^J = i^{-n} ε`, and `(-1)^{cw} = (-1)^{⌊-J/2⌋}` equals `ε` up to a factor that depends on `n` only. So the three signs agree up to a global constant, and

    Z(x) = i^{-n} Σ_C Z_C(e^x),

the sum over all components `C` of the exchange graph, with the same weights.

### 3.2 Claim 25 is the disk identity (`PROVED-HERE`)

A cycle of Li's `H` that alternates `M1` and non-`M1` edges is `v1, t1, v2, t2, ...` with `r(t_i) = v_i`. It is the spoke version of a cycle of chosen edges `r(t_i) -> v_{i+1}` in Lemma 4.1, with `|C| = 2h`. The third edge at `t_i` points inside the spoke cycle exactly when the black face `t_i` lies inside the `T`-cycle. So `t_in = l`, and `t_in = |C|/4 - 3/2` is `2l - h = -3`.

The proofs also match line by line. "`M1` matches all vertices of `H_C` to each other" is `B = I + l`. The hexagon count is the signed side count. O and T apply Euler to the triangulated disk in `T`. L applies it to the hexagon-faced disk in the spoke graph.

### 3.3 Li's marks are the leading Taylor coefficient (`PROVED-HERE`)

Give the spoke `(t, v)`, directed from `v` to `t`, the weight `a(t, v)` equal to the number of white-vertex rays it crosses left to right minus the number it crosses right to left. Then for a pair, the marks `(w, e2)` with `e2 ∈ M2`, counted with `(-1)^{dir}`, sum to `ω(s)`. With ordered lists of `c_min` marks,

    |O+| - |O-| = Σ_pairs (-1)^{cw(r,s)} ω(s)^{c_min},

which is `c_min!` times the coefficient of `x^{c_min}` in `Σ (-1)^{cw} e^{xω(s)}`. Up to the constant of 3.1 this is O's leading coefficient.

Li's weight field has circulation equal to the number of white vertices inside a spoke cycle, by Remark 19. A white vertex is a face of `G_FB`. So it is O's field of Lemma 5.3 (circulation one on each face), with the vertical ray from each white vertex used as the dual path to infinity. The fixed points of `ι2` are, for each group `D` with `c_min` cycles, one object per choice of a white vertex inside each cycle. Their number is `Σ_D Π_C (L+(C) - L-(C))`, which is formula (5.5) of O without the phase. So `ι2` is a bijective proof of (5.5) for these weights.

T's tokens `(t, j)` with `1 ≤ j ≤ a(t, s(t))` are the same marks after the weights are shifted to be nonnegative. T's `α` cancels by moving tokens between the two pools of a cycle. L's `ι2` cancels by pairing consecutive ray crossings. The surviving objects are counted by the same product.

One real difference. L needs `c_min`, the least number of cycles over all 2-factors, to define the objects. T's walk uses the cycle count `m` of the current pair and restarts with a smaller `m`, so it never needs to know `c_min`.

### 3.4 Component version (`LIT`, T Theorem 5.2)

O and L count over all pairs. T counts inside one component of the exchange graph and gets a tree pair in every component, with the two signs equally often. The extra statement is free once one notices that both regroupings move along exchange edges. `COMPUTED`: holds in every component of every test case.

### 3.5 Forest, cycle-breaking, tree matching (`PROVED-HERE`, `COMPUTED`)

For a pair `(r, s)` the three conditions are equivalent. The partner orients `Q_s` with out-degree one at nonroots and zero at roots, so cycles of `Q_s` avoid the roots and each acyclic component has one root. O proves this as Lemma 6.1, L as Lemma 8, T as (3) with Proposition 2.1.

For a state `s` with no partner assumed they differ.
- "`H - s` is a tree" (T) implies that `s` has exactly one mate. Nothing else is needed.
- "Li's `H - M2` is acyclic" does not imply that `H - s` is a tree. `Q_s` can be a forest with two roots in one component. `COMPUTED`: in the octahedron with every face split in four, 34 of the 54 states have `B - s` acyclic and `H - s` not a tree. The double wheels with rim 6, 8, 10 and 12 have such states too (1, 2, 3 and 4 of them).

So Li's Lemma 8 needs its hypothesis that `M1` exists, and Li's Lemma 30 is right to assume that `M2*` is a spanning tree and not only that `H - M2` is acyclic.

### 3.6 The selected set is the same (`PROVED-HERE`)

In O and T, the tree edge dual to the deleted spoke `(t, s(t))` is assigned to its endpoint `y` farther from `y0`, and the selected side of `t` is the one bordering `y`. In L, the dual edge of the `M2`-edge at `b` is traced as the path `w, b, w'`, the tree is oriented towards `w0`, and `P` takes the edge leaving the child. The child is `y`, and the edge of `G` from `y` to `t` is the side of `t` bordering `y`. Same set. `e0` is added in both.

### 3.7 Li's Lemma 9 already gives the black inner boundary (`PROVED-HERE`)

See `audit-li.md`, L-F2. For a minimal deficient set `S`, Claim 12 shows that all three edges of the cut `δ(G_S)` have their black end on the side of `S`, away from `b0`. In `T` this is a separating triangle whose bounded side has black faces along it. So L's proof establishes (iii) ⟹ (ii) of T's Theorem 1.2. The converse (ii) ⟹ (iii) is only in T.

Dictionary for that proof: `S ⊆ X`, `U = V(T) \ S`, `k` is the number of components of `T[U]`, `B_{S,i}` and `W_{S,i}` are the black and white faces with `i` corners in `S`, and `d(S) > 0` is the failure of (3.1).

### 3.8 Cuts, triangles, caps (`PROVED-HERE`)

A 3-edge cut of `G` with at least two vertices on each side is a bond, so its dual is a 3-cycle of `T`, and at least two faces on a side force a vertex strictly on that side. So "cyclically 4-edge-connected" is "no separating triangle". Contracting one side `X` to a vertex `x` is capping that side with a face. "All ends in `X` have one colour" (L, `A1`) is "the cap colour is forced" (O, `G2`). The edge `e'` not used at `x` by the first Hamiltonian cycle is the same-label edge of the cap, and prescribing it in the second piece is the same instruction in both papers. O inducts on Theorem 2.2. L takes a minimum counterexample. Same argument.

## 4. Where the papers differ in substance

**4.1 The hypothesis for the first pair.** O and L assume no separating triangle at all. T shows that a pair exists if and only if no separating triangle has black inner boundary, equivalently `t0` lies on the black side of every separating triangle. So T cuts less often, and T can say exactly when the state method applies to a rooted triangulation. O's and L's proofs can be upgraded with a one-line change each (O: treat the region containing `t0` separately, as T does; L: read off the colours in the last sentence of Lemma 9).

**4.2 From the white tree to the cycle.** O and T prove that `P` is a forest. A cycle in `P0` would be directed, the selected-side count gives `B - W = 2l - h`, and with Euler this says the disk has one black face fewer than the state requires. Then duality gives the Hamiltonian cycle and the Jordan curve gives the two induced trees. L never shows that `P` is a forest. L assumes the complement has two cycles, takes an innermost one with no root face inside, and finds two faces matched to one black vertex (see L-F8). L's route uses less (no disk identity, no partner) and proves less (no induced trees, which L does not need).

**4.3 Global or per component.** Only T states the count per exchange component.

**4.4 Existence or construction.** O proves existence by a Taylor coefficient. L proves existence by counting two ways. T also gives a path-following algorithm (the marked walk) and a separate enumeration with a proved `3^{n/2}` bound from the determinant.

**4.5 What depends on a drawing.** O and T are combinatorial: weights come from dual paths, orientation from the choice of `t0`. L fixes a straight-line drawing in general position and uses vertical rays. The drawing replaces Lemma 5.3 and the slide across subdisks, at the cost of an unstated general-position condition (L-F4).

**4.6 Statements with no counterpart.** T's Proposition 2.1 (mates, `2^k`), Lemma 6.1 (all states have one permutation sign, `M = |det K_B|`), and the prescribed-degree spanning tree form of the problem appear only in T. O's Corollary 7.2 appears only in O.
