# Reverse-Lamport audit: Zhentao Li, "A note on the proof of Barnette's conjecture" (arXiv:2610.30490v1, 21 Oct 2026)

Summary.
1. The route to Theorem 3 closes once four unwritten routine steps are supplied. I supply them below and say where the text stops. Verdict: FOLLOWS, with those steps listed.
2. Theorem 10 (Ore) is applied without the balance condition `|B'| = |F'|`. It holds by Euler, but the note never says so.
3. The case `c_min > 1` of the Key Lemma is only sketched in Appendix B. The sketch is correct. Three verifications are left to the reader.
4. The proof of Lemma 9 proves more than its statement. The 3-edge cut it finds has all three black ends on the side away from `b0`, which is the "black inner boundary" condition of the trees paper.
5. Lemma 30 does not use the disk identity. It replaces OpenAI's Lemma 6.2 by an innermost-cycle argument. This is the one place where Li's route differs in substance.

Source: `papers/A-Note-On-Barnette.pdf`, text dump `papers/text/A-Note-On-Barnette.txt`. I worked from the dump and re-derived each formula. I did not open the figures, so nothing below depends on them.

Warning on names. Li's `H` is `G_FB - N[b0]`, which is the graph called `B` in the shared notation. Li's `G_FB` is the shared `H`. In this file I write `H_Li` for Li's `H`.

## 1. Audit boundary

**Conclusion `C0`** (Theorem 3). For every Barnette graph `G` (cubic, 3-connected, bipartite, planar) and every edge `e0`, `G - e0` has a Hamiltonian cycle.

**Hypotheses.** As stated. For Theorem 4, also that `G` has no 3-edge cut with at least two vertices on each side.

**Fixed data.** Bipartition `(B, W)`, `e0 = b0 w0` with `b0` black, a straight-line embedding of `aux(G)` with `e0` on the outer face and "vertices in general position".

**Accepted primitives.** Euler's formula. Fáry's theorem (a simple planar graph has a straight-line embedding). Jordan curve theorem for polygons, including the parity of ray crossings. Tree-cotree duality for connected plane graphs. A 2-regular bipartite graph splits into two perfect matchings. For cubic graphs, vertex connectivity equals edge connectivity. Max-flow min-cut, as a substitute proof of Theorem 10.

**Not accepted by name alone.** Theorem 10, cited to Ore 1957. I could not open that paper. I treat the statement as a consequence of max-flow min-cut and check its applicability condition myself.

## 2. Obligation graph

```text
C0  Theorem 3
    <- R0, minimum counterexample over non-trivial 3-edge cuts (Appendix C)
       AND: C1, A1, A2, A3, A4

C1  Theorem 4 (cyclically 4-edge-connected case)
    <- R1  AND: E0, C2, C3, C4, C5

E0  embedding: straight-line drawing of aux(G), e0 on the outer face, general position
C2  Lemma 7 (Key Lemma): H_Li has a cycle-breaking 2-factor
    <- R2, two sign-reversing involutions on marked objects
       AND: C6, I1, I2, I3, I4, I5, I6, I7, B
C6  Lemma 9: H_Li has a 2-factor
    <- R3  AND: Q1, Q1a, Q2, Q3, Q4, Q5, Q6, Q7
Q1  Theorem 10 (Ore): deficit condition <=> 2-factor
Q1a applicability: |B'| = |F'|                                  [not stated in the note]
Q2  for a minimal S of positive deficit, G_S is connected
Q3  Claim 12: no white vertex lies on exactly one face of S
Q4  |delta(G_S)| = |B_{S,1}| = 3(|B ∩ V(G_S)| - |W ∩ V(G_S)|)
Q5  Euler on G_S: d(S) = 4 - 2k - |delta(G_S)|/3
Q6  k = 1 and |delta(G_S)| = 3
Q7  delta(G_S) is a non-trivial 3-edge cut, contradiction         [uses: cyclic 4-edge-connectivity]

I1  iota_1 is a well-defined involution whose fixed points are exactly the cycle-breaking objects
    <- AND: I1a (a cycle of H_Li - M2 alternates M1 and non-M1 edges, section 4.6), I1b (the first cycle depends on M2 only)
I2  iota_1 reverses the sign (Lemma 34)
    <- AND: C17, I2a (dir is unchanged)
C17 Lemma 17: swapping M1 along a cycle of H_Li - M2 flips cw
    <- AND: C25, C26, I2b (tau flips at exactly the black vertices of C, and the net change is +-3)
C25 Claim 25: t_out = |C|/4 + 3/2, t_in = |C|/4 - 3/2            [this is the disk identity]
    <- AND: V1 (everything inside C is in H_Li), V2 (M1 matches V(H_C) inside itself, so |V(H_C)| = 2 beta),
            V3 (|E(H_C)| = 3 beta - t_out), V4 (inner faces are hexagons), Euler
C26 Claim 26: cw' = |V(H_Li)|/6 - (2/3) sum_b tau(b)
    <- AND: C25 on every cycle of orient(M1, M2), I2c (the table for tau)
I3  iota_2 is a well-defined involution
    <- AND: I3a (crossing parity, Remark 19), I3b (the pairing p_C depends on C and w only), E0
I4  iota_2 reverses the sign (Lemma 35)
    <- AND: C16 (Lemma 16), I4a (consecutive crossings of a ray with a directed simple closed curve have opposite directions)
I5  Lemma 24: all fixed points of iota_2 have the same sign
I6  the fixed set of iota_2 is nonempty                            <- C6, a white vertex inside the cycle
I7  counting: |O+| != |O-| forces a fixed point of iota_1
B   Appendix B: the same for c_min > 1
    <- AND: B1 (definition of iota_2), B2 (involution), B3 (sign reversal), B4 (fixed points share a sign),
            B5 (fixed set nonempty)                               [B2, B3, B5 are not written]

C3  Lemma 8: G_FB - M2 is a spanning tree
    <- AND: L8a (a cycle would contain a path P in H_Li with one more black vertex than face-vertices),
            L8b (M1 matches the black vertices of P into P), L8c (edge count)
C4  Corollary 27: M2* is a spanning tree on the white vertices  <- tree-cotree, faces of G_FB = white vertices
C5  Lemma 30: E(G) - P is a Hamiltonian cycle
    <- R5, innermost cycle
       AND: T1 (the trace of T_W is a spanning tree of G - b0), T2 (Claim 31, P is a perfect matching),
            T3 (P-bar and trace_B(P) touch but do not cross), T4 (Claim 32), T5 (M2 ⊆ trace_B(P)),
            T6 (Claim 33, out-degree 1), T7 (the walk from a face inside C1 ends in a directed cycle C2 inside C1),
            T8 (C2 encloses a white vertex, contradiction)

A1  a non-trivial 3-edge cut has all its ends in X of one colour
A2  the three cut edges have distinct ends on each side; G[X] and G[V - X] are connected
A3  Claim 36: G/X and G/(V - X) are Barnette graphs, smaller than G
A4  the two Hamiltonian cycles glue (the edge e' missed at x)
```

## 3. Critical findings

**L-F1. Theorem 10 is applied without its balance condition (`Q1a`).** As stated ("`H` has a 2-factor exactly when the deficit condition holds for every `S ⊆ F'`") the theorem is false for unbalanced bipartite graphs. The flow argument gives a subgraph with degree 2 at every vertex of `F'` and degree at most 2 on `B'`. That is a 2-factor only if `|B'| = |F'|`. The note never counts the two sides. The count is easy. `|B| = N/2`, `|F(G)| = N/2 + 2`, so `|B'| = N/2 - 1 = |F'|`. Classification `side condition`, discharged here. `PROVED-HERE`. I also could not check the exact form of Ore's theorem against the 1957 paper, so I rely on the max-flow proof that the OpenAI paper gives for the same statement.

**L-F2. Lemma 9 proves more than it states.** The proof shows `W_{S,1} = ∅`, so every edge of `δ(G_S)` has its black end in `V(G_S)` and its white end outside. `b0` lies outside `V(G_S)`. In the dual, `δ(G_S)` is a separating triangle, `V(G_S)` is its bounded side, and the three faces along it on the bounded side are black. So the proof gives the following. If `H_Li` has no 2-factor, then `T` has a separating triangle with black inner boundary. Only the last sentence of the proof uses the full strength of cyclic 4-edge-connectivity. `PROVED-HERE` (by reading the proof, no new argument). This is one direction of (ii) ⟺ (iii) in the trees paper.

**L-F3. Small omissions in Lemma 9.** None breaks the proof.
- `|δ(G_S)| ≥ 1` (else `V(G_S) = V(G)`, but `b0 ∉ V(G_S)`), and `|δ(G_S)|` is a multiple of 3, so it equals 3. The note writes only `≤ 3`.
- `w0 ∉ V(G_S)`. A white neighbour of `b0` lies on two root faces and one other face. If that face were in `S` the vertex would be in `W_{S,1}`, which is empty.
- In Claim 12 the vertex listed as "black not in `G_S`" may well be in `G_S`. The claim is not used.
- "`G_S` is 2-connected" is true but not used. Connectedness is what Euler needs.
- In Claim 12 the deficit changes by `-2 + (decrease of the sum)`, and the decrease is at least 2 because the two named black vertices each lose one. Other black vertices on `f` can only add to the decrease. So `d(S - f) ≥ d(S)` as claimed.

**L-F4. "General position" is never defined (`E0`).** Definitions 13, 18 and 20 and Remark 19 need that no vertex of `aux(G)` lies on the vertical line through another vertex. Then every ray meets edges in interior points and transversally. A small rotation of any straight-line drawing achieves this. `side condition`, discharged.

**L-F5. Definition 14 is ambiguous between a set and a list of marks.** Definition 14 writes `{x1, ..., x_cmin}`. Appendix B writes an indexed list. The argument works under both readings. If every cycle of `M1 ∪ M2` carries a mark then there are exactly `c_min` cycles with exactly one mark each, and `ι2` moves a mark inside its own cycle. Under the list reading, the signed count is `c_min!` times the Taylor coefficient of order `c_min` in the OpenAI sum (see `correspondence.md`). `PROVED-HERE`.

**L-F6. Appendix B stops at a sketch (`B2`, `B3`, `B5`).** The main text proves Lemma 7 for `c_min = 1` and says the extension is "technical but straightforward". Appendix B defines the sign and `ι2`, and asserts the fixed points and their common sign. It does not write out three things.
- `B2`, `ι2` is an involution. After a move on the first qualifying cycle `C_i`, the cycles are unchanged, `w_i` is on the same side of `C_i`, and the moved mark is still not the first crossing. So the same cycle and the same pairing are selected again.
- `B3`, sign reversal. If a cycle has no mark, swapping along it changes `cw'` by `±2`, so `⌊cw'/2⌋` changes by `±1`, and no `dir` changes. Otherwise the single-cycle computation of Lemma 35 applies to `C_i`, and the other cycles keep their orientation.
- `B5`, the fixed set is nonempty. Take a 2-factor with `c_min` cycles, a white vertex inside each cycle, the first edge on its ray, and swap along a cycle when that edge lies in `M1`. The swaps are independent.

Also the text omits the sub-case "swap along `C_i` if the partner edge lies in `M1`" and one sentence starts with a misplaced "Otherwise". With these supplied the appendix is a proof. For `B4` I checked the stated sign. With `q` counterclockwise cycles, `Σ dir = q` and `cw = ⌊(c_min - 2q)/2⌋ = ⌊c_min/2⌋ - q`, so the sign is `⌊c_min/2⌋ mod 2`. `PROVED-HERE`. I record this as the place where the written argument stops. I do not count it as a failure, because the note declares the analogy and the analogy holds.

**L-F7. Lemma 8, wording.** "The part of `C` in `H` is a path" should read "each maximal part of `C` in `H` is a path". Any one of them works. "All (face) neighbours of black vertices of `P` are also on `P`" is true when read in `H_Li - M2`, which is what the previous sentence sets up, and that is all the proof needs, since `M1 ⊆ H_Li - M2`. The degenerate case of a single black vertex adjacent to two root faces cannot occur (two faces of a 3-connected planar graph that share `b` and `b0` would share an edge), and the counting argument rules it out anyway. Discharged.

**L-F8. Lemma 30 takes a different route from OpenAI's Lemma 6.2.** OpenAI proves that the selected set `P` is a forest by a count that contradicts the disk identity for the state `s`, and then gets the cycle from Lemma 2.1. Li assumes the 2-factor `E(G) - P` has two cycles, takes an innermost cycle `C1` with no root face inside, and follows out-edges of the oriented trace. The argument is correct, and it can be stated in three lines. Inside `C1` every vertex of `G` lies on `C1`, so the faces inside `C1` are the nodes of a tree (the weak dual of `C1` with its chords). Each such face `f` has an out-step: go to its `M2`-partner `b`, cross the chord of `P` at `b`. A map from the nodes of a finite tree to their neighbours has a 2-cycle. A 2-cycle crosses one chord twice, so two faces are matched by `M2` to the black end of that chord. Contradiction. `PROVED-HERE`. So this lemma uses the matching property of `M2` and planarity, and neither the disk identity nor `M1`. `COMPUTED`: the selection rule returns two induced trees for every tree matching and every root edge in all test triangulations.

**L-F9. `T1` is not written.** The sketch says the trace of `T_W` is "a spanning tree of `G`". It is a spanning tree of `G - b0`. Each black vertex other than `b0` subdivides exactly one edge of `T_W` (the dual of its `M2`-edge), and a subdivision of a tree is a tree. `side condition`, discharged here.

**L-F10. Where each hypothesis enters.**
- Cyclic 4-edge-connectivity: only `Q7`.
- 3-connectivity: `Q6` (a cut of size at most 2 is impossible), the hexagonal faces of `G_FB` and the simplicity of `aux(G)` (`V4`, `E0`), Appendix C.
- Bipartiteness: the tripartition of `aux(G)`, `|B'| = |F'|`, and the colour argument `A1`.
- `M1` is used in `I1a`, `V2`, `L8b`. It is not used in Lemma 30.
- The bijectivity of the matchings is used in `V2` (this is the "state supplies `B = I + l`" step), in `I1a`, in `L8b`, in `T2` and in `T6`.

**L-F11. Orientation conventions.** I checked the table in Claim 26 with a path heading north. For a clockwise cycle with the third edge outside, the turn from the `M2`-edge to the `M1`-edge is counterclockwise, so `τ = 0`. The other three entries follow. In Lemma 24, a clockwise cycle is crossed left to right at the first exit of an interior ray, so `cw = 0` and `dir = 0`. A counterclockwise cycle gives `cw = ⌊-1/2⌋ = 1 mod 2` and `dir = 1`. Both signs are 0. The floor in the definition of `cw` is what makes this work. Consistent. `PROVED-HERE`.

**L-F12. Appendix C.** The step "a vertex cut of size at most 2 is an edge cut of size at most 2 by taking the appropriate edges" is the standard fact that a cubic graph has equal vertex and edge connectivity. It is stated without proof or reference. I accept it as background. If `e0 ∈ δ(X)` then the edge `e'` missed at `x` is `e0` itself, and the gluing still works. The note does not separate this case, and does not need to.

## 4. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Theorem 3 | root | R0 / claim | root | C1, A1 to A4 | discharged |
| C1 | Theorem 4 | C0 | R0 / AND | major claim | E0, C2, C3, C4, C5 | discharged |
| E0 | straight-line drawing of `aux(G)`, `e0` outer, general position | C1, I3, C25 | AND | side condition | Fáry, rotation, L-F4 | discharged |
| C2 | Lemma 7, cycle-breaking 2-factor | C1 | R1 / AND | major claim | C6, I1 to I7, B | discharged |
| C6 | Lemma 9, a 2-factor of `H_Li` exists | C2, I6, B5 | R2 / AND | major claim | Q1 to Q7 | discharged |
| Q1 | Theorem 10, deficit condition gives a 2-factor | C6 | AND | named theorem | Ore 1957 not opened, max-flow proof as in OpenAI Prop. 3.1 | discharged |
| Q1a | `|B'| = |F'|` | Q1 | applicability / AND | side condition | not stated in the note, Euler, L-F1 | discharged |
| Q2 | minimal deficient `S` has `G_S` connected | C6 | AND | algebraic/logical step | deficit is additive over components | discharged |
| Q3 | Claim 12, `W_{S,1} = ∅` | Q4, Q5 | AND | algebraic/logical step | removing `f` does not lower the deficit, L-F3 | discharged |
| Q4 | `|δ(G_S)| = |B_{S,1}| = 3(|B_S| - |W_S|)` | Q5 | AND | algebraic/logical step | edge count from both colours, Q3 | discharged |
| Q5 | `d(S) = 4 - 2k - |δ(G_S)|/3` | Q6 | AND | algebraic/logical step | Euler on `G_S` | discharged |
| Q6 | `k = 1`, `|δ(G_S)| = 3` | Q7 | AND | algebraic/logical step | `d(S) ≥ 1`, 3-edge-connectivity, L-F3 | discharged |
| Q7 | non-trivial 3-edge cut, contradiction | C6 | AND | hypothesis | cyclic 4-edge-connectivity | discharged |
| I1 | `ι1` is an involution fixing exactly the cycle-breaking objects | C2 | AND | proved earlier | I1a, I1b, section 4.6 | discharged |
| I1a | cycles of `H_Li - M2` alternate `M1` and non-`M1` edges | I1 | AND | algebraic/logical step | degree count at black vertices | discharged |
| I1b | the selected cycle depends on `M2` only | I1 | AND | definition | fixed total order on cycles | discharged |
| I2 | Lemma 34, `ι1` reverses the sign | C2 | AND | proved earlier | C17, I2a | discharged |
| I2a | `dir` is unchanged by `ι1` | I2 | AND | definition | `M2` and its orientation are unchanged | discharged |
| C17 | Lemma 17, `cw` flips under a swap of `M1` along a cycle of `H_Li - M2` | I2 | AND | major claim | C25, C26, I2b | discharged |
| I2b | `τ` flips at each black vertex of `C`, net change `±3` | C17 | AND | algebraic/logical step | cyclic order of three edges, C25 on `C` | discharged |
| C25 | Claim 25, `t_out - t_in = 3` | C17, C26 | AND | major claim | V1 to V4, Euler | discharged |
| V1 | all vertices inside `C` are in `H_Li` | C25 | AND | side condition | `b0` on the outer face, root faces adjacent to `b0` | discharged |
| V2 | `|V(H_C)| = 2β` | C25 | AND | side condition | `M1` perfect, `C` alternating, planarity | discharged |
| V3 | `|E(H_C)| = 3β - t_out` | C25 | AND | algebraic/logical step | cubic, count from the black side | discharged |
| V4 | inner faces of `H_C` are hexagons | C25 | AND | side condition | one white vertex per face of `G_FB` | discharged |
| C26 | Claim 26, `cw'` as a sum of `τ` | C17 | AND | proved earlier | C25 on `D`-cycles, table I2c | discharged |
| I2c | the four-entry table for `τ` | C26 | AND | algebraic/logical step | checked, L-F11 | discharged |
| I3 | `ι2` is a well-defined involution | C2 | AND | algebraic/logical step | I3a, I3b, E0, case analysis | discharged |
| I3a | Remark 19, parity of ray crossings | I3 | AND | named theorem | Jordan curve theorem for polygons, E0 | discharged |
| I3b | the pairing depends on `C` and `w` only | I3 | AND | definition | Definition 20 | discharged |
| I4 | Lemma 35, `ι2` reverses the sign | C2 | AND | proved earlier | C16, I4a | discharged |
| C16 | Lemma 16, `cw` flips under a swap along a cycle of `M1 ∪ M2` | I4 | AND | algebraic/logical step | `cw'` changes by `±2`, floor | discharged |
| I4a | consecutive crossings of a ray have opposite directions | I4 | AND | algebraic/logical step | inside and outside alternate along the ray | discharged |
| I5 | Lemma 24, fixed points of `ι2` have one sign | C2 | AND | proved earlier | L-F11 | discharged |
| I6 | the fixed set of `ι2` is nonempty (`c_min = 1`) | C2 | AND | algebraic/logical step | C6, a face of `G_FB` inside the cycle | discharged |
| I7 | a fixed point of `ι1` exists | C2 | AND | algebraic/logical step | `|O+| - |O-|` computed twice | discharged |
| B | Appendix B, the case `c_min > 1` | C2 | AND | major claim | B1 to B5 | discharged |
| B1 | definition of the sign and of `ι2` with `c_min` marks | B | AND | definition | Appendix B, with the omitted sub-case of L-F6 | discharged |
| B2 | `ι2` is an involution | B | AND | algebraic/logical step | not written, supplied in L-F6 | discharged |
| B3 | `ι2` reverses the sign | B | AND | algebraic/logical step | not written, supplied in L-F6 | discharged |
| B4 | fixed points have sign `⌊c_min/2⌋ mod 2` | B | AND | algebraic/logical step | stated, checked in L-F6 | discharged |
| B5 | the fixed set is nonempty | B | AND | algebraic/logical step | not written, supplied in L-F6 | discharged |
| C3 | Lemma 8, `G_FB - M2` is a spanning tree | C4 | AND | major claim | L8a, L8b, L8c | discharged |
| L8a | a cycle contains a path in `H_Li` with one extra black vertex | C3 | AND | algebraic/logical step | `H_Li - M2` and the star at `b0` are acyclic, L-F7 | discharged |
| L8b | `M1` matches the black vertices of `P` into `P` | C3 | AND | side condition | `M1 ⊆ H_Li - M2`, degrees | discharged |
| L8c | `2n + 3` edges on `2n + 4` vertices | C3 | AND | algebraic/logical step | count, not written out in the note | discharged |
| C4 | Corollary 27, `M2*` is a spanning tree on white vertices | C5 | AND | named theorem | tree-cotree duality, `G_FB` connected plane graph | discharged |
| C5 | Lemma 30, `E(G) - P` is a Hamiltonian cycle | C1 | R1 / AND | major claim | T1 to T8 | discharged |
| T1 | the trace of `T_W` is a spanning tree of `G - b0` | T2 | AND | side condition | subdivision of a tree, L-F9 | discharged |
| T2 | Claim 31, `P` is a perfect matching | C5 | AND | algebraic/logical step | orientation towards `w0` | discharged |
| T3 | `P-bar` and `trace_B(P)` do not cross | T7 | AND | side condition | cyclic order around a black vertex | discharged |
| T4 | Claim 32, some cycle has no root face inside | C5 | AND | algebraic/logical step | `e0 ∈ P`, only the cycle through `b0` can enclose `f3` | discharged |
| T5 | `M2 ⊆ trace_B(P)` | T6 | AND | algebraic/logical step | the `P`-edge at `b` is half of the traced path | discharged |
| T6 | Claim 33, out-degree 1 off the root faces | T7 | AND | side condition | `M2` and `P` are perfect matchings | discharged |
| T7 | the walk ends in a directed cycle inside `C1` | C5 | AND | algebraic/logical step | T3, T4, T6, finiteness | discharged |
| T8 | that cycle encloses a white vertex, contradiction | C5 | AND | algebraic/logical step | innermost choice of `C1`, L-F8 | discharged |
| A1 | a non-trivial 3-edge cut has monochromatic ends in `X` | C0 | AND | algebraic/logical step | `3(|B ∩ X| - |W ∩ X|) = |δ_B| - |δ_W|` | discharged |
| A2 | distinct ends, both sides connected | A3 | AND | algebraic/logical step | 3-edge-connectivity | discharged |
| A3 | Claim 36, both contractions are smaller Barnette graphs | C0 | AND | proved earlier | A1, A2, cubic connectivity fact, L-F12 | discharged |
| A4 | the two cycles glue to one missing `e0` | C0 | AND | algebraic/logical step | the edge `e'` unused at `x` is prescribed in `G2` | discharged |

## 5. Verdict

**FOLLOWS**, with the following qualification stated plainly. Four steps on the route are not written in the note and I supplied them: `Q1a` (the two sides of `H_Li` have equal size), `B2`, `B3` and `B5` (the involution, sign reversal and nonempty fixed set for `c_min > 1`). Each is routine and each is proved in section 3 above. If a referee insists on the letter of the text, the Key Lemma is fully proved only for `c_min = 1`, and the remaining case is a correct sketch.

The decisive nodes are `C6` (with `Q7` the only use of cyclic 4-edge-connectivity), `C25` (the disk identity), `C17`, `I5`, `B`, and `C5`.
