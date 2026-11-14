# Referee report on draft B (mathematics)

Reviewer: Claude Fable 5.2, 2026-11-14. Object: `paper/draft-B/barnette.tex` and its PDF (16 pages) as committed at `804b7ab`. Method: `skills/reverse-lamport/SKILL.md`, from Theorem 1.1 backward. I checked every proof line by line during the cold read (`COLD-READ.md`) and again against the source. Status tags follow `research/BRIEF.md`.

Summary in five lines.
1. Every step of the draft is correct. I found no false statement on the route to Theorem 1.1.
2. One hypothesis of a named theorem is not checked: Euler's formula is applied to "Z and everything inside it" without showing that this plane graph is connected. I judge this a real, small gap. Lemma D below closes it in five lines and also supplies the unstated connectedness of a coloured triangulation and of the pieces in Section 6.
3. Two wording-level side conditions: spokes are called "segments" (needs straight faces or the word "arcs"), and the claim that changing the paths shifts heights by a constant is unproved and unused.
4. The parts the author calls its own are sound: the face tree `Y_s` by duality, the winding-number proof of Lemma 4.6, the finite difference Lemma 4.7, Proposition 4.8.
5. The worked example is confirmed by an independent computation with `workings/barnette_lab`: 12 states, 8 pairs, 6 good states, `Σ = 18`, 6 Hamiltonian cycles avoiding the edge. One remark in Section 7 (hexagonal prism) holds only for one of the three sides of `t0`.

## 1. Audit boundary

**Conclusion C0 (Theorem 1.1).** For every finite simple graph `G` that is cubic, bipartite, planar and 3-connected (at least four vertices, connected after deleting any two), and every edge `e` of `G`, some Hamiltonian cycle of `G` does not contain `e`.

**Hypotheses.** As stated. A sphere embedding of `G` is fixed.

**Accepted primitives.**
- P1. Jordan curve theorem for polygonal closed curves on the sphere, in the form: the complement has two components, each an open disk, and every point of the curve is in the closure of both.
- P2. Euler's formula `V − E + F = 2` for a **connected** plane graph. I do not accept "Euler for a triangulated disk" as a primitive; connectedness has to be checked where the formula is used. This is the one place where my boundary is stricter than the author's (`AUDIT.md` P2).
- P3. Plane duality basics: the dual exists, each dual edge crosses its own edge once and nothing else, edges and face corners alternate around a vertex, a face of the dual contains one vertex and its boundary walk has length the degree of that vertex.
- P4. Integral max-flow min-cut (Ford and Fulkerson 1956). `LIT`.
- P5. For a closed polygonal curve `Γ` and a polygonal path from `p` to `q` in general position, the signed crossing number equals `wind(Γ, p) − wind(Γ, q)`; the winding number around a point is invariant under homotopy of `Γ` in the complement of that point; a counterclockwise simple closed curve has winding number 1 inside and 0 outside.
- P6. Elementary finite graph theory: a nonempty edge set with all degrees even contains a cycle; a connected graph with all degrees two is a cycle; trees have `q − 1` edges; a connected graph with `q` vertices and `q` edges has one cycle; a cycle meets an edge cut in an even number of edges; a forest with `e` edges on `v` vertices has `v − e` components.

Not accepted without proof: the disk identity, the existence of a good state, and anything about states.

**Text in scope.** Sections 2 to 6 and the proof of Theorem 1.1. Lemma 3.1, the examples, Remark 4.10 and Section 7 are not on the route; I audited them for truth separately (section 4 below).

## 2. Obligation graph

All groups are AND groups. The draft supplies one route to each claim.

```text
C0  Theorem 1.1
 <- R0: L2.1, T6.2, P2.5(1), O-avoid
L2.1  T is a coloured triangulation
 <- O-cut, O-simple, O-tri, O-four, O-colour
T6.2  every coloured T, face t0, side e0: acyclic selection containing e0
 <- induction on |V|: O-dichotomy, CaseA, CaseB
CaseA (no separating triangle)
 <- O-swap, P5.2, P4.8, P3.7
CaseB (separating triangle)
 <- L6.1, O-smaller, O-conn-piece, IH(T1), IH(T2), O-union-selection, O-union-acyclic
O-union-acyclic <- P2.5(2) in T1 and T2, O-side-simple
P2.5  acyclic selection: (1) Hamiltonian cycle, (2) two components, edge in P iff ends together
 <- L2.4(1), L2.4(2), (2.2), O-conn-T
L2.4  duality lemma for a connected simple plane graph M
 <- P1, P3, P6, P2
P3.7  good state => P_s acyclic selection containing e0
 <- L3.4, L3.3, L3.6, O-outdeg, O-directed, O-match-count, O-roots-split
L3.3  S_s spanning tree => Y_s tree with degrees 2 and 1; P_s is a selection
 <- L2.4(2), O-conn-T, O-deg-Y, O-rooting, O-white-once
L3.4  S_s spanning tree <=> s good   <- edge count, P6
L3.6  disk identity
 <- O-noroot, O-euler-disk, O-disk-connected, O-disk-faces, O-sides, O-state-count
P4.8  a pair => a good state
 <- L4.5, L4.4, L4.6, L4.7, O-group, O-min, O-additive
L4.5  cancellation for fixed s   <- L4.3(1), L4.4, O-Ks, L4.2
L4.2  partner orients Q_s; good <=> acyclic   <- bijectivity of r, P6
L4.3  both reversals give pairs   <- L4.2, bijectivity
L4.4  J = #cw − #ccw, n + J even, both reversals flip eps
 <- O-Dcover, L3.6 on D-cycles, L3.6 on Q_s-cycles, O-chosen, O-local
L4.6  reversal cw -> ccw raises h_s(w) by [w inside C]; L(C) >= 1
 <- O-spokes, O-genpos, P5, O-homotopy, L3.6
L4.7  finite difference   <- algebra
P5.2  no separating triangle => a pair
 <- O-flow, O-translate, O-components, O-small, O-rootsmall, O-tri-face, O-region, O-euler-K
```

There is no cycle. L3.6 uses bijectivity of a state and nothing downstream. L4.6 uses L3.6 only for `L(C) ≥ 1`.

## 3. Critical findings

### G1. Euler's formula on the disk: an unchecked hypothesis (real, small)

**Where.** Proof of Lemma 3.6, first count: "Euler's formula for the plane graph formed by `Z` and everything inside it, which has `I + h` vertices, `B + W + 1` faces and `(3(B+W)+h)/2` edges".

**What is missing.** Euler's formula needs a connected plane graph (P2). The draft does not say why this graph, call it `R_Z`, is connected, nor why its faces are the `B + W` faces of `T` inside `Z` plus exactly one more. The author knows (`AUDIT.md` F9, `REPORT.md`) and classifies it as a primitive. I do not, for three reasons.
- The hypothesis is the hypothesis of the theorem being cited. The skill asks that every applicability condition of a named theorem be checked.
- The project's formalisation spent its largest block exactly here (`research/2026-11-14_opus_lean-formalisation/LESSONS-FOR-EXPOSITION.md`, section 5: 13% of the Lean against 6% of the paper, "500 lines of Lean and zero sentences in the paper"). An exposition that aims to be clearer than the sources should not be silent in the same place.
- The same unstated fact is used twice more. Lemma 2.4 requires `M` connected, and it is applied to `M = T` where "coloured triangulation" is defined (after Lemma 2.1) without connectedness; in Theorem 6.2 it is applied, through Proposition 2.5, to the pieces `T_1`, `T_2`.

The "no pinched vertex" issue that the Lean had to prove does not arise in draft B. The draft works with the topological inside of `Z`, so "a face with a corner strictly inside `Z` lies inside `Z`" is immediate, and a vertex on `Z` is handled through its outgoing edge. I checked the third count with this in mind and it is complete.

**The missing lemma.** `PROVED-HERE`.

> **Lemma D.** Let `R` be a finite graph embedded in the sphere such that every face of `R` is bounded by a cycle of `R`. Then `R` is connected.
>
> *Proof.* Let `K` be a component of `R`. The boundary of a face is a cycle, which is connected, so it lies in one component. Let `Ω` be the union of `K` with the faces whose boundary lies in `K`, and `Ω'` the union of the other components with the other faces. A point of `K` has a neighbourhood that meets only `K` and faces incident with `K` at that point, and those faces have their boundary in `K`. So `Ω` is open, and so is `Ω'` by the same argument. They are disjoint and cover the sphere, which is connected, and `Ω` is not empty. Hence `Ω'` is empty. ∎

Three consequences, each one sentence.
- A coloured triangulation is connected (every face is bounded by a triangle). This discharges O-conn-T.
- With `Z` as in Lemma 3.6, let `R_Z` consist of `Z` and the vertices and edges of `T` inside `Z`. By P1 the outside of `Z` is an open disk containing no point of `R_Z`, so it is one face of `R_Z`, bounded by `Z`. Every other face of `R_Z` lies inside `Z` and contains no vertex or edge of `T`, so it is a face of `T`, bounded by a triangle. Hence `R_Z` has `B + W + 1` faces, each bounded by a cycle, and is connected by Lemma D. Each inner face has three sides, each edge strictly inside lies on two inner faces, and each edge of `Z` on one inner face and the outer face, which gives the edge count. This discharges O-disk-connected and O-disk-faces.
- The piece `T_D` of Section 6 has the faces of `T` in `D` and the cap, all bounded by triangles, so it is connected. This discharges O-conn-piece.

A proposed insertion is edit 1 in `EDITS.md`.

**Severity.** The statement is true and no reader will doubt it. The OpenAI paper has the same silence ("Euler's formula for the triangulated disk"). For a journal referee this is a remark. For this project, whose formal proof singled out the shape of the disk, it is the one place where draft B does not yet do better than the source.

### G2. Spokes are "segments"

**Where.** Section 4, Heights: "call the segments from `c_t` to the corners of `t` spokes".

A segment from an interior point of a face to a corner stays in the face only if the face is drawn so that this is true (straight sides, or star-shaped from `c_t`). The draft never fixes a straight-line drawing, and the figures draw the sides of `t0` as circular arcs. The proof of Lemma 4.6 needs each spoke to lie in the closed face `t`. It also calls `Γ` and `γ_w` polygonal, which needs the edges of `T` to be polygonal arcs. Both are harmless normalisations (a plane graph has a polygonal embedding, and one can choose arcs inside each face), but they must be said. Classification: side condition, discharged after a change of wording (edit 6).

### G3. "Changing the paths adds a constant"

**Where.** After the definition of `ω`: "Changing the paths adds to each `h_s(w)` a constant that does not depend on `s`; nothing below depends on the choice."

The first half is true but not proved in the draft. A proof (from `research/2026-11-14_astra_referee-combinatorics/REFEREE.md`, "Heights, roots, and volume"): for two states the difference of their selected spokes is a closed 1-chain, because each centre and each non-root vertex is used once by each state, so its crossing number with a path depends only on the endpoints. The second half is what matters: the paths are fixed once, and Lemma 4.6 is proved for the fixed paths. The sentence is not on the route. Either delete the first half or add the one-line proof (edit 7).

### G4. One implicit step in Proposition 4.8

"In each face `t` it has `(r'(t), s'(t)) = (r(t), s(t))` or `(s(t), r(t))`." This needs: the undirected edge set of `D(r,s)` contains exactly one side of each `t ∈ A`, because distinct black faces give distinct edges and an edge has one black face. The fact is stated two pages earlier ("they are distinct even as undirected edges"). Classification: discharged, with a missing back-reference (edit 12).

### G5. The author's own parts

| Part | Verdict | Comment |
| --- | --- | --- |
| Face tree by duality (Lemmas 3.3, 3.4) | correct | `Y_s = T* − S_s*` is a spanning tree of `G` by Lemma 2.4(2), given O-conn-T. Degrees: each `t ∈ A` has one side in `S_s`, `t0` has two. The rooting argument is complete, including that a white face has exactly one selected side. The step "a black child of `y` has a child other than `y`" uses that two faces share at most one side, which holds in a simple triangulation with at least four vertices (it follows from `Y_s ⊆ G` and `G` simple; not said). |
| Winding numbers for the slide (Lemma 4.6) | correct, given G2 | The sign convention is right: a spoke crossing `γ_w` from right to left counts +1, and for a counterclockwise circle around `p` with `γ` going outward this gives `+1 = wind(p) − wind(q)`. `Γ` need not be simple, which is why the slide of OpenAI §5.3 is not needed. The homotopy stays in closed faces of `A`, which contain neither `p_w` nor `q`. |
| `m`-fold finite difference (Lemma 4.7) | correct | Stated for `c ≥ m` only, which is all that is used, since every group has `c ≥ m`. |
| Proposition 4.8 | correct | Signs: `J = c − 2Σx_i`, `ε = (−1)^{(n+c)/2}(−1)^{Σx_i}`; for `c = m` the factor `(−1)^m` from Lemma 4.7 gives `(−1)^{(n−m)/2}`. Additivity over several cycles holds because `h_s(w)` is a sum over faces and the cycles use disjoint face sets. |
| Recovery (Proposition 3.7) | correct | The match count `B − ℓ = W − (h − ℓ)` includes chords with both ends on `Z`: such an edge is strictly inside, so both its faces are inside. |

### G6. Other points on the route, all discharged

- **Lemma 2.1.** The 2-edge-cut argument uses simplicity of `G` for "two vertices have at least four edges leaving". The step "both sides contain vertices" uses P1.
- **Lemma 2.4(2).** The parity argument is complete. It uses that every face is incident with a vertex and that `M` is connected.
- **Disk identity, set-up.** "Every face of `T` lies inside or outside `Z`" and "the roots lie on its boundary, so none of them lies inside `Z`" are P1 plus the fact that roots are not on `Z`.
- **Lemma 4.4.** For a cycle `K` of `Q_s` the disk identity is applied with the chosen sides `r(t) → u(t)` in all faces of `A`, which the draft says before Lemma 4.3. The local identity holds in both cyclic orders.
- **Lemma 4.5.** `K_s` depends on `s` alone. States without a partner contribute nothing to either side of the displayed identity.
- **Proposition 5.2.** I rechecked the translation to (5.3), the component bounds and the chain `2m_K = 4f − (b+w) + Σ(d_F − 4) ≥ 4f − 2b`. The root component with `p = 3` is argued at more length than needed: a second black face on `a, b, c` would share the side `ab` with the black face `t0`.
- **Theorem 6.2.** The theorem is stated for every face and side, so the induction hypothesis applies to the cap of `T_2`, whatever its colour.

## 4. Statements off the route

| Statement | Verdict |
| --- | --- |
| Lemma 3.1 (every acyclic selection containing `e0` gives a state) | correct. `PROVED-HERE` by the draft. |
| Example 3.8, Example 4.9, figure captions | `COMPUTED`, confirmed. See section 6. |
| Remark 4.10, "`i^J = i^{−n} ε`", Taylor coefficient `i^{−n}Σ/m!` | correct. |
| Remark 4.10, coefficient of `(z−1)^m` is `Σ/m!` | correct: `binom(ω, m) = ω^m/m!` plus lower powers, and the lower moments vanish by Lemma 4.7. The draft does not say this. |
| Remark 4.10, "Li counts lists of `m` marks, which are the terms of `ω(s)^m`" | **inaccurate.** Li's marks are sets of distinct intersections (his Definition 14); for `m > 1` his signed count is an elementary symmetric expression in the crossing signs, not the power `ω(s)^m` (astra `REFEREE.md`, "Comparison of the three supplied arguments"). The same applies to "the weight `ω^m` that all three papers use" in the Sources paragraph. See edit 14. |
| Section 7, genus count `|V| = k + 2 − 2g` | correct. |
| Section 7, the 2-connected example from three cubes | correct. |
| Section 7, "different good states give different cycles, since Lemma 3.1 recovers `s` from `P_s`" | correct: in the proof of Proposition 3.7 the edges of `P_0` are directed out of `s(t)` and each tree has one root, so they point towards the root. |
| Section 7, hexagonal prism: "three states, two of them good, and four Hamiltonian cycles avoiding the edge" | `COMPUTED`: true when `e0` is the side of `t0` on the equator of the bipyramid (the avoided edge of the prism is a rung). For each of the two sides at an apex there are 2 Hamiltonian cycles avoiding the edge and both come from good states. The draft does not say which side. See edit 15. |
| Section 5, last paragraph: exact criterion of the constructive paper | not checked here; it is cited, not used. |

## 5. Simplifications a referee would suggest

These are not repairs. The draft's own arguments are valid. Each item would shorten or remove a step.

**S1. Heights without spokes or winding numbers.** `PROVED-HERE` (proof below), `COMPUTED` (`check_face_paths.py`: the running example, the hexagonal bipyramid, and 148 rootings of the lab's generated family up to 12 vertices of `T`, 94 with a pair, 736 reversals of `D`-cycles; output `check_face_paths.txt`). This is the flow device of the Lean proof (`LESSONS-FOR-EXPOSITION.md` section 3) written in the language of draft B.

For each white face `w` fix a path of faces `w = f_0, f_1, …, f_k = t0` in `G`, consecutive faces sharing a side. The path passes through a black face `t ∈ A` by entering across one side and leaving across another. These two sides meet in one corner `v` of `t`. Put `κ_w(t, v) = +1` if the path turns around `v` with `v` on its left, `−1` if on its right, and `κ_w(t, v') = 0` for the other two corners. Define `h_s(w)` and `ω(s)` as in the draft.

*Claim.* For a pair `(r, s)` and a clockwise cycle `C` of `D(r, s)` with reversal `(r', s')`: `h_{s'}(w) − h_s(w) = 1` if `w` is inside `C`, else `0`.

*Proof.* Fix a face `t` supplying `C`; its side on `C` joins `r(t)` and `s(t)`. If the path does not pass through `t`, or passes around `u(t)`, it does not cross that side and `κ_w(t, r(t)) − κ_w(t, s(t)) = 0`. If it passes around `r(t)` or around `s(t)`, it crosses that side once, and a check of the two cyclic orders of the corners shows that `κ_w(t, r(t)) − κ_w(t, s(t))` is `+1` if the crossing goes from the left of the directed edge `s(t) → r(t)` to its right and `−1` otherwise. Every crossing of the path with an edge of `C` occurs next to a passage through the black face of that edge, so the sum over `t` is the number of crossings of `C`, directed counterclockwise, from left to right minus the number from right to left. The left of a counterclockwise cycle is its inside. By Lemma 2.4(1) a step of the path changes sides of `C` exactly when it crosses an edge of `C`. The path ends in `t0`, outside. So the signed count is 1 if `w` is inside and 0 otherwise. ∎

This removes the spokes, the general-position conditions, the polygonal paths, P5 and the homotopy. Figure 3(c) is no longer needed. The price is one local picture of a path turning around a corner. It also keeps the promise of the introduction more literally: no object outside `T` and its faces remains.

**S2. The sign as a product.** `PROVED-HERE` in `research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` section 2; I rechecked it. Put `ε(r, s) = ∏_{t ∈ A} δ(r(t), s(t))`. Since `Σ_t δ = 3J = n − 2·#{δ = −1}`, this is `(−1)^{(n−3J)/2} = (−1)^{(n+J)/2}`, the same sign as in the draft. In a black triangle the directed edges `r → s`, `s → u`, `u → r` have equal `δ`, so `δ(u, s) = −δ(r, s)`. Then both reversals flip every `δ` on the faces of the cycle, the sign changes by `(−1)^{length}`, and the length is odd by the disk identity. Lemma 4.4 shrinks to three lines, `J` is not needed for the cancellation, and integrality of `J` is never an issue. In Proposition 4.8 one still needs the orientation: a counterclockwise cycle of length `h` has `(h+3)/2` negative signs and a clockwise one `(h−3)/2`, which gives `ε = (−1)^{(n+c)/2}(−1)^{Σx_i}` as before.

**S3. Define "good" before Lemma 3.3.** Lemma 3.3 is stated under "`S_s` is a spanning tree", Lemma 3.4 translates, Definition 3.5 names it. In the order 3.5, 3.4, 3.3 the reader meets the condition in the form that is used later.

**S4. One principle, said once.** "If every vertex has outdegree at most one, a cycle is a directed cycle" is proved three times (Proposition 3.7, Lemma 4.2, and inside Lemma 4.3 by reference). State it once before the disk identity.

## 6. The worked example, recomputed

`COMPUTED` by `research/2026-11-14_fable_review-draft-B/recompute.py`, which uses `workings/barnette_lab/barnette_lab/core.py` (`Instance`, its state enumeration, signs and spoke-circulation weights) plus brute force written in the script. It does not import or run the author's `example.py`. Command: `python research/2026-11-14_fable_review-draft-B/recompute.py > research/2026-11-14_fable_review-draft-B/recompute.txt`. Input: `paper/figures/running.json` (13 vertices, 22 faces, `t0 = {0,4,5}`, `e0 = {0,4}`).

| Claim in the draft | Recomputed |
| --- | --- |
| 12 states | 12 |
| 8 ordered pairs | 8 |
| 6 good states (Definition 3.5 tested directly, and by the lab's spoke-tree test) | 6, each with exactly one partner |
| two groups of four pairs, each with `m = 2` cycles | 2 groups, sizes 4 and 4, cycle counts 2 and 2 |
| `L = 6, 1` and `L = 3, 1` | jumps of the lab weight under reversal: (7-cycle 6, triangle 1) and (7-cycle 3, triangle 1); point-in-polygon on the figure layout gives `W = 6, B = 5` and `W = 3, B = 2` for the 7-cycles and `W = 1, B = 0` for the triangles |
| `Σ ε ω^2 = 18` | 18; also `Σ ε = 0` and `Σ ε ω = 0` |
| exactly one state with cyclic `Q_s`, triangle on 1, 8, 9, two partners that cancel | one such state, cycle `[1, 8, 9]`, partners with `ε = −1, +1` |
| six pairs with good second state, three of each sign | `{+1: 3, −1: 3}` |
| 6 Hamiltonian cycles of `G` avoiding the edge across `e0`, all recovered | 6 by enumeration of all perfect matchings with connected complement; the 6 recovered cycles are distinct and are these 6 |
| `P_s` for the state of Figure 4(b) has components `{0,2,4,6,7,8}` and `{1,3,5,9,10,11,12}` | confirmed |
| `D` of the pair of Figure 8: counterclockwise 7-cycle 6,1,2,3,9,10,11 and clockwise triangle 8,7,12 | confirmed against the layout coordinates |

The lab's embedding is the mirror image of the figure's, so its `J` has the opposite sign; `ε` is unchanged because `J` is even here. The lab weights differ from the draft's heights by a constant, which does not affect `Σ` because the lower moments vanish.

The script also reads a state off each of the 6 Hamiltonian cycles as in Lemma 3.1: 6 distinct states, all good.

## 7. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Theorem 1.1 | root | R0 | root | L2.1, T6.2, P2.5(1), O-avoid | discharged after G1 |
| O-avoid | `e ∈ P*` when the edge crossing `e` is in `P` | C0 | R0 AND | definition | Definition 2.3 | discharged |
| L2.1 | `T` is simple, at least 4 vertices, triangular faces, 2-coloured | C0 | R0 AND | major claim | O-cut … O-colour | discharged |
| O-cut | `G` has no edge cut of size at most 2 | L2.1 | AND | hypothesis | 3-connected, cubic, simple; proof ¶1 | discharged |
| O-simple | `T` has no loop or parallel pair | L2.1 | AND | side condition | O-cut, P1 | discharged |
| O-tri | faces of `T` are triangles | L2.1 | AND | algebraic/logical step | cubic, P3, O-simple | discharged |
| O-four | `|V(T)| ≥ 4` | L2.1 | AND | named theorem | P2 for `G` (connected by hypothesis) | discharged |
| O-colour | proper 2-colouring of faces | L2.1 | AND | hypothesis | bipartition | discharged |
| (2.2) | `k` black, `k` white, `3k` edges, `k + 2` vertices | P2.5, §3, P5.2 | side count, Euler | named theorem | P2, O-conn-T | discharged after G1 |
| O-conn-T | a coloured triangulation is connected | (2.2), L2.4 uses, L3.3 | AND | side condition | not in the draft; Lemma D | **missing**; discharged by Lemma D |
| L2.4(1) | cycle `Z ⊆ S`: dual edges across `Z` are those crossing `Z`; `M* − S*` disconnected | P2.5(2), S1 | AND | named theorem | P1, P3 | discharged |
| L2.4(2) | `S` acyclic ⇒ `M* − S*` connected; tree ⇒ tree | P2.5(1), L3.3 | AND | algebraic/logical step | P3, P6, P2 | discharged |
| P2.5(1) | acyclic selection ⇒ Hamiltonian cycle | C0, P3.7 | AND | major claim | L2.4(2), P6 | discharged |
| P2.5(2) | two components; `uv ∈ P` iff ends together | L3.1, O-union-acyclic | AND | major claim | (2.2), L2.4(1), P6 | discharged |
| T6.2 | acyclic selection containing `e0` for every coloured `T` | C0 | induction | major claim | CaseA, CaseB | discharged after G1 |
| O-dichotomy | separating triangle or none | T6.2 | AND | algebraic/logical step | logic | discharged |
| O-swap | colours may be exchanged | CaseA | AND | definition | Definition 2.3 ignores colours | discharged |
| P3.7 | good ⇒ `P_s` acyclic selection containing `e0` | CaseA | AND | major claim | L3.3, L3.4, L3.6, below | discharged after G1 |
| L3.3 | `Y_s` tree; `P_s` selection containing `e0`, sides at `s(t)` | P3.7 | AND | major claim | L2.4(2), O-deg-Y, O-rooting, O-white-once | discharged after G1 |
| O-deg-Y | `t ∈ A` has one side in `S_s`, `t0` two | L3.3 | AND | algebraic/logical step | one black face per edge | discharged |
| O-rooting | each black face has one child | L3.3 | AND | algebraic/logical step | degrees, colours alternate | discharged |
| O-white-once | a white face has exactly one side in `P_s` | L3.3 | AND | algebraic/logical step | unique parent; two faces share at most one side | discharged |
| L3.4 | `S_s` spanning tree ⇔ `s` good | P3.7 | AND | algebraic/logical step | `|S_s| = |V| − 1`, P6 | discharged |
| L3.6 | disk identity `W = B + 1`, `h = 2ℓ + 3` | P3.7, L4.4, L4.6 | AND | major claim | below | discharged after G1 |
| O-noroot | `Z` avoids and does not enclose roots; inner black faces are in `A` | L3.6 | AND | side condition | outdegree, P1 | discharged |
| O-euler-disk | `B + W = 2I + h − 2` | L3.6 | AND | named theorem | P2 applied to `R_Z` | discharged after G1 |
| O-disk-connected | `R_Z` is connected | O-euler-disk | AND | side condition | not in the draft; Lemma D | **missing**; discharged by Lemma D |
| O-disk-faces | faces of `R_Z` are the inner faces of `T` and one outer face; edge count | O-euler-disk | AND | side condition | half-stated ("only the edges of `Z` lie on a single inner face"); P1 | open in the text; discharged in G1 |
| O-sides | `3(B − W) = 2ℓ − h` | L3.6 | AND | algebraic/logical step | colouring | discharged |
| O-state-count | `B = I + ℓ` | L3.6 | AND | algebraic/logical step | injectivity and surjectivity of `r`, P1 | discharged |
| O-outdeg | in `P_0`: outdegree 1 on `X`, 0 at roots | P3.7 | AND | algebraic/logical step | `s` bijective | discharged |
| O-directed | a cycle of `P_0` is a directed cycle of chosen sides | P3.7 | AND | algebraic/logical step | distinct tails | discharged |
| O-match-count | `B − ℓ = W − (h − ℓ)` | P3.7 | AND | algebraic/logical step | one selected side per face | discharged |
| O-roots-split | one root per tree of `P_0`, so `e0` closes no cycle | P3.7 | AND | algebraic/logical step | outdegree count | discharged |
| P4.8 | a pair ⇒ a good state | CaseA | AND | major claim | below | discharged after G1, G2 |
| O-min | `m ≥ 1` exists | P4.8 | AND | hypothesis | a pair exists, finiteness | discharged |
| O-group | a group is the `2^c` orientations | P4.8 | AND | algebraic/logical step | one edge per face of `A` (G4), bijectivity, L4.3(2) | discharged |
| O-additive | reversing several cycles adds the jumps | P4.8 | AND | algebraic/logical step | `h_s(w)` is a sum over faces | discharged |
| L4.2 | partner gives outdegrees; components are rooted trees or rootless unicycles | L4.3, L4.5 | AND | major claim | `r` bijective, P6 | discharged |
| L4.3 | both reversals give pairs; (1) is an involution | L4.5, O-group | AND | major claim | L4.2 | discharged |
| O-Dcover | `D(r,s)` is a set of disjoint directed cycles covering `X` | L4.4 | AND | algebraic/logical step | two bijections, one black face per edge | discharged |
| O-chosen | cycles of `D` and of `Q_s` are cycles of chosen sides for `r` | L4.4, L4.6 | AND | definition | paragraph before Lemma 4.3 | discharged |
| O-local | `δ(u,s) − δ(r,s) = 2δ(r,u)` | L4.4 | AND | algebraic/logical step | two cyclic orders | discharged |
| L4.4 | `J = #cw − #ccw`; `n + J` even; both reversals flip `ε` | L4.5, P4.8 | AND | major claim | L3.6 twice, O-local | discharged after G1 |
| O-Ks | the reversed cycle depends on `s` only | L4.5 | AND | side condition | fixed order on cycles of `T` | discharged |
| L4.5 | `Σ_r ε(r,s) = 0` if `Q_s` has a cycle | P4.8 | AND | major claim | L4.3(1), L4.4, O-Ks | discharged after G1 |
| O-spokes | each spoke lies in its closed face; `Γ`, `γ_w` polygonal | L4.6 | AND | side condition | "segments" (G2) | open as worded; discharged after edit 6 |
| O-genpos | `γ_w` avoids vertices and centres, crosses spokes transversally | L4.6 | AND | side condition | stated | discharged |
| O-homotopy | `Γ ≃ C` in the complement of `p_w` and of `q` | L4.6 | AND | named theorem | P5; closed faces of `A` contain neither point | discharged |
| L4.6 | jump of `h_s(w)` is `[w inside C]`; `L(C) ≥ 1` | P4.8 | AND | major claim | P5, O-homotopy, L3.6 | discharged after G1, G2 |
| L4.7 | finite difference of an `m`-th power | P4.8 | AND | algebraic/logical step | expansion | discharged |
| P5.2 | no separating triangle ⇒ a pair | CaseA | AND | major claim | below | discharged |
| O-flow | (5.1) ⇒ a pair | P5.2 | AND | named theorem | P4, `|A| = |X|` | discharged |
| O-translate | (5.1) ⇔ (5.3) | P5.2 | AND | algebraic/logical step | one black face per edge, (2.2) | discharged |
| O-components | per-component bounds sum to (5.3) | P5.2 | AND | algebraic/logical step | corners of a face pairwise adjacent | discharged |
| O-small | `p ≤ 3`: `m_K ≤ 2p` | P5.2 | AND | algebraic/logical step | simplicity | discharged |
| O-rootsmall | root component with `p = 3` | P5.2 | AND | algebraic/logical step | colouring | discharged |
| O-tri-face | faces of `K` of length 3 are faces of `T` | P5.2 | AND | hypothesis | no separating triangle, simplicity, P1 | discharged |
| O-region | `|β(F)| ≤ d_F − 4` | P5.2 | AND | algebraic/logical step | parity, divisibility | discharged |
| O-euler-K | `m_K − b ≤ 2p − 4` | P5.2 | AND | named theorem | P2; `K` is connected by definition | discharged |
| L6.1 | cap colour forced; piece is a coloured triangulation | CaseB | AND | algebraic/logical step | signed sides, simplicity, P1 | discharged |
| O-smaller | each piece has fewer vertices | CaseB | AND | side condition | separating | discharged |
| O-conn-piece | each piece is connected | CaseB via P2.5 | AND | side condition | not in the draft; Lemma D | **missing**; discharged by Lemma D |
| O-union-selection | `P_1 ∪ P_2` has one side per face and contains `e0` | CaseB | AND | algebraic/logical step | shared edges are the sides of `Δ` | discharged |
| O-side-simple | an edge of `T_2` joining two of `x, y, z` is a side of `Δ` | O-union-acyclic | AND | side condition | `T` simple | discharged |
| O-union-acyclic | `P_1 ∪ P_2` is acyclic | CaseB | AND | algebraic/logical step | P2.5(2) in both pieces | discharged |

## 8. Verdict

**NOT ESTABLISHED BY THIS PROOF, as written, at exactly one kind of node; FOLLOWS after inserting Lemma D.**

Read strictly by the rules of the skill, the route does not close at **O-disk-connected** (with its companions **O-conn-T** and **O-conn-piece**): Euler's formula and the duality lemma are applied to plane graphs whose connectedness the draft does not establish. No other obligation fails. **O-spokes** is open only because of the word "segments". This verdict says nothing against the theorem, and I am not reporting a doubt about any statement in the draft: Lemma D (section 3, G1) is proved here and discharges all three nodes, and with it and the change of wording in G2 every obligation on the supplied route is discharged from the hypotheses and P1 to P6. The decisive nodes are L3.6 (the only place where bijectivity of a state enters a count), L4.4 and L4.6 (which consume L3.6), and O-union-acyclic (which consumes P2.5(2)).

My audit is independent of the author's and of the author's script. It is still one model's reading. No human has checked draft B.
