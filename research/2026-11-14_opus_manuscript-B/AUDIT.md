# Reverse-Lamport audit of draft B

Audited text: `paper/draft-B/barnette.tex` as committed with this file (16 pages). Numbers refer to the compiled PDF. Method: `skills/reverse-lamport/SKILL.md`. I audit the route the draft supplies, from Theorem 1.1 backward, and do not repair silently: every fix I made during the audit is listed under "Changes made because of this audit".

## 1. Audit boundary

**Conclusion C0 (Theorem 1.1).** For every finite simple graph `G` that is cubic, bipartite, planar and 3-connected (at least four vertices, connected after deleting any two), and every edge `e` of `G`, there is a Hamiltonian cycle of `G` not containing `e`.

**Hypotheses.** Finite, simple, cubic, bipartite, planar (a sphere embedding is fixed), 3-connected as defined.

**Accepted primitives.**
- P1 Jordan curve theorem for polygonal closed curves on the sphere; a simple closed curve in the plane has winding number 1 (counterclockwise) or 0 at points inside / outside.
- P2 Euler's formula `V - E + F = 2` for connected plane graphs; in particular for the plane graph consisting of a cycle of a triangulation and everything inside it.
- P3 Plane duality basics: the dual of an embedded graph, every dual edge crosses exactly its own primal edge once; around a vertex of a simple plane graph edges and faces alternate.
- P4 Integral max-flow min-cut (Ford and Fulkerson 1956).
- P5 Hall's theorem gives a perfect matching in a regular bipartite graph (used only in motivation, not in the proof chain).
- P6 For a closed polygonal curve `Γ` and a polygonal path `γ` from `p` to `q` in general position, the signed number of crossings equals `wind(Γ, p) - wind(Γ, q)`; winding number is invariant under homotopy in the complement of the point.
- P7 Elementary graph facts: a nonempty graph with all degrees even contains a cycle; a connected finite graph with all degrees 2 is a cycle; a connected graph with `q` vertices and `q` edges has exactly one cycle; a tree has `q - 1` edges; a cycle meets every edge cut in an even number of edges; a forest with `e` edges on `v` vertices has `v - e` components.

## 2. Obligation graph

```
C0 Thm 1.1 <- R0 (AND: L2.1, T6.2, P2.5(1), O-dual-edge)
  L2.1 (T simple coloured triangulation) <- (AND: O-cut, O-loop, O-face, O-count4, O-colour)
  T6.2 (acyclic selection containing e0, any coloured T) <- induction on |V| (AND: O-cases, Case1, Case2, O-measure)
    Case1 (no separating triangle) <- (AND: O-swap, P5.2, P4.8, P3.7)
      P5.2 (a pair exists) <- (AND: O-flow, O-translate, O-components, O-small, O-tri-faces, O-region, O-euler-K)
      P4.8 (pair => good state) <- (AND: L4.5, L4.2, L4.3, L4.4, L4.6, L4.7, O-groups, O-min)
        L4.5 (cancellation) <- (AND: L4.3(1), L4.4, O-Ks-depends-on-s)
        L4.4 (sign) <- (AND: L3.6 on D-cycles, L3.6 on Q_s-cycles, O-local-delta, O-parity)
        L4.6 (heights) <- (AND: P6, P1, O-homotopy-in-black-triangle, L3.6 for L(C) >= 1)
        L4.7 (finite difference) <- algebra
      P3.7 (good state => acyclic selection) <- (AND: L3.3, L3.4, L3.6, O-outdegree, O-face-pairing)
        L3.3 (tree of faces Y_s) <- (AND: L2.4(2), O-degrees-in-Y, O-rooting)
        L3.6 (disk identity) <- (AND: P2, O-side-count, O-state-count [bijectivity])
    Case2 (separating triangle) <- (AND: L6.1, IH on T1, IH on T2, O-glue-selection, O-glue-acyclic)
      O-glue-acyclic <- (AND: P2.5(2) in T1 and T2, O-simple-sides)
  P2.5 (acyclic selection => Hamiltonian cycle; two components, induced) <- (AND: L2.4(1), L2.4(2), P7)
  L2.4 (duality) <- (AND: P1, P3, P7, P2)
```

The motivating Lemma 3.1 (every acyclic selection containing `e0` comes from a state) is not on the route to C0. It is used in Section 7 (injectivity remark) only. The two examples (3.8, 4.9) and Remark 4.10 are not on the route.

## 3. Critical findings

The dependency audits of the published papers flagged six kinds of obligation. Here is where each is discharged in draft B.

**F1. Simplicity of the dual (O-cut, O-loop).** Lemma 2.1, first two paragraphs. The 3-connectivity hypothesis is used exactly here: an edge cut of size at most two between nonempty sides is impossible (sides have at least three vertices by cubicity and simplicity of `G`; deleting the at most two cut-ends on one side disconnects). A loop or a digon of `T` is a closed curve meeting `G` in at most two crossings with both sides nonempty. Discharged. Simplicity of `T` is then used in: faces are triangles (closed walk of length 3 is a triangle), the small-component bound and the "no chord inside a facial side" step of Proposition 5.2, Lemma 6.1 (pieces simple), and O-simple-sides in the gluing (an edge of `T2` with both ends in `{x, y, z}` is a side of `Δ`). Each place cites simplicity explicitly.

**F2. Where bijectivity of a state is used.** (a) `|A| = |X|` is needed for states to exist (counts (2.2)). (b) Lemma 3.6, count `B = I + ℓ`: injectivity (no vertex counted twice; the edge of `Z` leaving `v` is the chosen side of `r^{-1}(v)`), surjectivity (every interior vertex is hit). The draft says both. (c) Lemma 4.2: outdegree one at every nonroot uses that `r` is onto `X`; outdegree zero at roots uses that `r` maps into `X`. (d) Lemma 4.3: reversal preserves bijectivity because tails and heads of a directed cycle are the same vertex set. (e) `D(r, s)` is a cycle cover because both `r` and `s` are bijections. (f) Proposition 3.7: outdegree one at nonroots in `P0` uses that `s` is a bijection. (g) Proposition 4.8, grouping: "exactly one of the two edges at `x` reversed" would make `x` a value of `r'` or `s'` twice. All discharged.

**F3. Orientation conventions.** `δ(v, w) = +1` iff the black face of `vw` is on the left of `v → w`, equivalently `w` follows `v` counterclockwise in that black face. Disk identity: counterclockwise traversal has the inside on the left, so `Σδ = ℓ - (h - ℓ) = 2ℓ - h = -3`. `J = #cw - #ccw` follows. The local identity `δ(u,s) - δ(r,s) = 2δ(r,u)` is checked in both cyclic orders in the proof of Lemma 4.4. Heights: `κ` counts crossings from the right of `γ_w` to its left as `+1`; with a counterclockwise unit circle and `γ` from the centre outward this gives `+1 = wind(p) - wind(q)` (I checked this convention by hand). In Lemma 4.6 the spoke `c_t → s(t)` is traversed backwards in the route `s(t) → c_t → r(t)`, which gives the minus sign; the new second state on the faces of `C` is `r(t)`, the counterclockwise head. `COMPUTED`: `example.py` asserts `h_{s'}(w) - h_s(w) = [w inside C]` for every clockwise `D`-cycle of all 8 pairs of the example and every white face, with independent point-in-polygon tests, and asserts `J = #cw - #ccw` for every pair. Discharged.

**F4. Euler counts.** (2.2): `E = 3·#black = 3·#white`, `V - 3k + 2k = 2`. Lemma 3.6: `E = (3(B+W) + h)/2`, Euler gives `B + W = 2I + h - 2`; signed sides give `3(B - W) = 2ℓ - h`; algebra checked twice. Proposition 3.7: face pairing count `B - ℓ = W - (h - ℓ)`. Proposition 5.2: `2m = 3(b+w) + Σ d_F = 4f - (b+w) + Σ(d_F - 4)` and `p - m + f = 2` give `m - b ≤ 2p - 4`; checked line by line. Section 7 genus count `V = k + 2 - 2g`. `COMPUTED`: `example.py` asserts `W = B + 1`, `h - 2ℓ = 3`, `B = I + ℓ` on every `D`-cycle of every pair of the example. Discharged.

**F5. Exhaustiveness of cases.** Theorem 6.2: a coloured triangulation either has a separating triangle or not. Proposition 5.2: components with `p ≤ 3` and `p ≥ 4`; root component with `p = 3` treated separately; faces of a component split into length 3 and length at least 4 (length at least 3 because `K` is simple with `p ≥ 4`). Region bound: `d = 4`, `d = 5`, `d ≥ 6`. Lemma 4.2: components with one root or none (at most one by the edge count). Lemma 4.4: the two cyclic orders of `r, s, u`. Lemma 4.7: `c > m` and `c = m`; Proposition 4.8 uses `c ≥ m` for every group by the definition of `m`. Discharged.

**F6. The gluing.** Theorem 6.2, Case 2. Obligations: (i) pieces are coloured triangulations with fewer vertices (Lemma 6.1, cap colour forced by divisibility); (ii) `t0` is a face of `T1`; (iii) `P1` contains exactly one side `e'` of the cap; (iv) the induction hypothesis applies to `T2` with face the cap and side `e'`, which is possible because Theorem 6.2 is stated for every face and side, not for a fixed colour of `t0`; (v) `P = P1 ∪ P2` has exactly one side in every face of `T` (the only shared edges are the sides of `Δ`, and `P2` contains only `e'` among them, which is in `P1`); (vi) acyclicity: by Proposition 2.5(2) in each piece, the only `P_i`-path between two of `x, y, z` is `e'`; a cycle of `P` not inside one piece contains an edge of `P2 \ P1`, which has an end strictly inside `D2` (O-simple-sides), and following the cycle gives a `P2`-path of length at least two between two distinct vertices of `{x, y, z}`. Discharged.

**F7 (found in this audit). The disk identity's hypothesis on `Q_s`-cycles.** Lemma 3.6 asks for a choice of one side at `r(t)` in *every* face of `A`. For a `Q_s`-cycle the draft uses the `Q_s`-edges directed from `r(t)` as the choice in every face (stated before Lemma 4.3: "so are the edges of `Q_s` directed as in Lemma 4.2"). For a `D`-cycle the choice is the `D`-edge in every face. For `P0` it is the `P_s`-side directed out of `s(t)`. In each case the choice is made in all faces. Discharged.

**F8 (found in this audit). The heights need general position.** `γ_w` must avoid vertices and the points `c_t` and cross spokes transversally. The draft states this. The homotopy from `C` to `Γ` stays inside closed black triangles of `A`, which contain neither `p_w` (in an open white face) nor `q` (in the open outer face). Discharged. No simplicity of `Γ` is needed, which is why the slide argument of OpenAI 5.3 does not appear.

**F9 (found in this audit). Euler on a disk needs a connected plane graph.** Lemma 3.6 and Lemma 6.1 apply Euler to "the plane graph formed by `Z` and everything inside it". Connectivity of this graph is accepted as part of P2 (the closed disk is the union of the closed triangles inside, which are connected through shared sides). Classified as accepted primitive, not as a gap. A stricter reader could ask for one more sentence.

**F10. The motivational step in Section 4.** "With `F = 1` the answer is no" is a remark, proved in one line (reverse the `D`-cycle through a fixed vertex). Not on the route.

## 4. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Theorem 1.1 | root | R0 | root | L2.1, T6.2, P2.5(1), O-dual-edge | discharged |
| O-dual-edge | `e ∈ P*` when `e0 = e*` is in `P`, so the cycle avoids `e` | C0 | definition of `P*` | definition | Def. 2.3 | discharged |
| L2.1 | `T` is a simple coloured triangulation with ≥ 4 vertices | C0 | AND | major claim | O-cut, O-loop, O-face, O-count4, O-colour | discharged |
| O-cut | no edge cut of size ≤ 2 in `G` | L2.1 | 3-connectivity | hypothesis | proof of L2.1 ¶1 | discharged |
| O-loop | no loop or digon in `T` | L2.1 | closed curve meets `G` in ≤ 2 crossings | side condition | O-cut, P1 | discharged |
| O-face | faces of `T` are triangles | L2.1 | cubic, simple | algebraic/logical step | closed walk of length 3 in a simple graph | discharged |
| O-count4 | `|V(T)| ≥ 4` | L2.1 | Euler | algebraic/logical step | P2, `|V(G)| ≥ 4` | discharged |
| O-colour | faces properly 2-coloured | L2.1 | bipartite | hypothesis | proof of L2.1 | discharged |
| (2.2) | `#black = #white = k`, `E = 3k`, `V = k + 2` | L3.*, P5.2, P2.5 | side count + Euler | algebraic/logical step | P2 | discharged |
| L2.4(1) | a cycle `Z ⊆ S` gives a cut of `M*` crossing exactly `Z` | P2.5(2) | Jordan | named theorem | P1, P3 | discharged |
| L2.4(2) | `S` acyclic ⟹ `M* - S*` connected; spanning tree ⟹ spanning tree | P2.5(1), L3.3 | even-degree boundary | algebraic/logical step | P3, P7, P2 | discharged |
| P2.5(1) | acyclic selection ⟹ Hamiltonian cycle | C0, P3.7 | degree 2 + L2.4(2) | major claim | P7 | discharged |
| P2.5(2) | 2 components; `uv ∈ P` iff ends in one component | O-glue-acyclic | parity of cut | major claim | L2.4(1), P7 | discharged |
| T6.2 | every coloured `T`, face `t0`, side `e0`: acyclic selection ∋ `e0` | C0 | induction on `|V|` | major claim | O-cases, Case1, Case2, O-measure | discharged |
| O-cases | separating triangle or not | T6.2 | dichotomy | side condition | logic | discharged |
| O-measure | pieces have fewer vertices | T6.2 | separating | side condition | L6.1 | discharged |
| O-swap | colours may be exchanged so `t0` is black | Case1 | selections ignore colours | definition | Def. 2.3 | discharged |
| P5.2 | no separating triangle ⟹ a pair | Case1 | flow + density | major claim | O-flow … O-euler-K | discharged |
| O-flow | pair ⟸ (5.1) | P5.2 | max-flow min-cut | named theorem | P4; `|A| = |X|`; even cycles split | discharged |
| O-translate | (5.1) ⟺ (5.3) | P5.2 | shortfall `max(0, j-1)` | algebraic/logical step | (2.2), each edge one black face | discharged |
| O-components | (5.3) follows from per-component bounds | P5.2 | black faces lie in one component | algebraic/logical step | roots pairwise adjacent | discharged |
| O-small | `p ≤ 3`; root component `p = 3` | P5.2 | direct | side condition | simplicity, `|V| ≥ 4` | discharged |
| O-tri-faces | length-3 faces of `K` are faces of `T` (`p ≥ 4`) | P5.2 | no separating triangle | hypothesis | simplicity (no chord) | discharged |
| O-region | `|β(F)| ≤ d_F - 4` | P5.2 | signed sides, parity, divisibility | algebraic/logical step | cases `d = 4, 5, ≥ 6` | discharged |
| O-euler-K | `m - b ≤ 2p - 4` | P5.2 | Euler for `K` | algebraic/logical step | P2 | discharged |
| P4.8 | a pair ⟹ a good state | Case1 | `Σ ε ω^m ≠ 0` | major claim | L4.5, L4.3, L4.4, L4.6, L4.7, O-groups, O-min | discharged |
| O-min | `m ≥ 1` exists | P4.8 | finiteness, a pair exists | side condition | hypothesis of P4.8 | discharged |
| O-groups | a group is exactly the `2^c` cycle reversals | P4.8 | consecutive faces agree | side condition | bijectivity (F2g), L4.3(2) | discharged |
| L4.5 | `Σ_r ε(r,s) = 0` if `Q_s` has a cycle | P4.8 | fixed-point-free involution | major claim | L4.3(1), L4.4, O-Ks | discharged |
| O-Ks | the reversed cycle depends on `s` only | L4.5 | fixed order on cycles of `T` | side condition | proof of L4.5 | discharged |
| L4.2 | partner orients `Q_s`; components rooted trees or unicyclic rootless; good ⟺ acyclic | L4.5, P4.8 | outdegree count | major claim | bijectivity of `r`, P7 | discharged |
| L4.3 | the two reversals give pairs; (1) is an involution | L4.5, O-groups | tails = heads | major claim | L4.2 | discharged |
| L4.4 | `J = #cw - #ccw`, `n + J` even, both reversals flip `ε` | L4.5, P4.8 | local `δ` + disk identity | major claim | L3.6, O-local-delta, O-parity | discharged |
| O-local-delta | `δ(u,s) - δ(r,s) = 2δ(r,u)` | L4.4 | two cyclic orders | algebraic/logical step | proof of L4.4 | discharged |
| O-parity | number of `D`-cycles ≡ `n` mod 2 | L4.4 | odd lengths sum to `n` | algebraic/logical step | L3.6 | discharged |
| L4.6 | reversal cw→ccw raises `h_s(w)` by `[w inside C]`; `L(C) ≥ 1` | P4.8 | winding numbers | major claim | P6, P1, O-homotopy, L3.6 | discharged |
| O-homotopy | `Γ ≃ C` in plane minus `{p_w, q}` | L4.6 | each edge and its route in one closed black triangle | side condition | P6 | discharged |
| L4.7 | `m`-fold difference of a power of a linear form | P4.8 | expansion | algebraic/logical step | proof | discharged |
| P3.7 | good ⟹ `P_s` acyclic selection ∋ `e0` | Case1 | disk identity vs face pairing | major claim | L3.3, L3.4, L3.6, O-outdegree, O-face-pairing | discharged |
| L3.3 | `Y_s` tree, degrees 2 and 1; `P_s` a selection ∋ `e0`, sides at `s(t)` | P3.7 | L2.4(2) + rooting | major claim | O-degrees-in-Y | discharged |
| O-degrees-in-Y | `t ∈ A` has one side in `S_s`; `t0` has two | L3.3 | each edge one black face | algebraic/logical step | definition of `S_s` | discharged |
| L3.4 | `S_s` spanning tree ⟺ `s` good | L3.3 via P3.7 | edge count | algebraic/logical step | P7 | discharged |
| L3.6 | disk identity `W = B + 1`, `h = 2ℓ + 3` | P3.7, L4.4, L4.6 | three counts | major claim | P2, O-state-count, O-side-count | discharged |
| O-state-count | `B = I + ℓ` | L3.6 | bijection | side condition | bijectivity (F2b) | discharged |
| O-side-count | `3(B - W) = 2ℓ - h` | L3.6 | signed sides | algebraic/logical step | coloured triangulation | discharged |
| O-outdegree | outdegree 1 at `X`, 0 at roots in `P0` | P3.7 | `s` bijective | side condition | F2f | discharged |
| O-face-pairing | `B - ℓ = W - (h - ℓ)` | P3.7 | each `P`-edge pairs its two faces | algebraic/logical step | Def. 2.3 | discharged |
| Case2 | gluing | T6.2 | induction | major claim | L6.1, IH, O-glue-selection, O-glue-acyclic | discharged |
| L6.1 | cap colour forced; pieces are smaller coloured triangulations | Case2 | divisibility by 3 | algebraic/logical step | signed sides, simplicity | discharged |
| O-glue-selection | `P1 ∪ P2` has one side per face, contains `e0` | Case2 | shared edges = sides of `Δ` | algebraic/logical step | proof of T6.2 | discharged |
| O-glue-acyclic | `P1 ∪ P2` acyclic | Case2 | unique `P_i`-path between cap corners | algebraic/logical step | P2.5(2), O-simple-sides | discharged |
| O-simple-sides | an edge of `T2` with both ends in `{x,y,z}` is a side of `Δ` | O-glue-acyclic | `T` simple | side condition | L2.1 | discharged |

## 5. Changes made because of this audit

1. The definition of 3-connectivity (at least four vertices) was added before Lemma 2.1 used `|V(G)| ≥ 4`.
2. The proof that the roots are not inside a cycle of chosen sides now says why: every face of `T` is inside or outside the cycle, the outer face is outside, and the roots are on its boundary.
3. In Proposition 5.2 the step "a triangle with no vertex on one side bounds a face" now says why no edge lies on that side (it would be parallel to a side of a simple graph).
4. In Proposition 4.8 the argument that a group is exactly the `2^c` reversals had a slip: it said the vertex would be a value of `r'` twice in a case where it is `s'`. It now names both cases.
5. Theorem, lemma and equation numbers now share one counter, because "(5.1)" and "Proposition 5.1" collided.
6. The claim that the example is the smallest with both phenomena came from another agent's search that I did not repeat; I removed it.

## 6. Verdict

**FOLLOWS.** Every obligation on the route the draft supplies (C0 ← L2.1, T6.2, P2.5; T6.2 ← Case1 [P5.2, P4.8, P3.7] and Case2 [L6.1, gluing]) is discharged from the hypotheses and the accepted primitives P1–P7. The decisive nodes are L3.6 (disk identity, the only place bijectivity enters the counts), L4.4 (the sign, which needs L3.6 twice), L4.6 (heights, which needs P6 and L3.6) and O-glue-acyclic (which needs P2.5(2)). The weakest point for a strict reader is F9: Euler's formula on a triangulated disk is used without proving that the disk's graph is connected; I classify it as an accepted primitive. The audit is my own; it is not independent of the author, and the draft still needs an outside reader.
