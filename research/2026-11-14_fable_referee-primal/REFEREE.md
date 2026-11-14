# Referee report on the primal proof

Reviewer: Claude Fable 5.2, 2026-11-14. Object: `proofs/primal/PRIMAL-PROOF.md` (with `primal.tex`, `STATUS.md`, `COMPARISON.md`) as found in the working tree at commit `9184b70`. Method: `skills/reverse-lamport/SKILL.md`, from Theorem T backward. I read the proof and wrote my findings before opening the author's `AUDIT.md`. Status tags follow `research/BRIEF.md`.

Summary.
1. The route closes. I found no false statement and no failing node on the way to Theorem T. All thirteen lemmas are true as stated.
2. The weakest spot is the planar background, not the combinatorics. The list of accepted planar facts in Section 2 is three items short, and the note never says whether a plane graph is a drawing or a rotation system. The proofs of Lemma 2(b) and Lemma 3 each lean on one unlisted fact (F1, F3, F4).
3. Two lemmas need a wording repair to be right as written: the "equivalently" in the definition of `δ` (F2) and the hypothesis ledger of Section 9 (F7). Exact replacement text is given.
4. Lemma 12 proves more than it states, and the stronger statement is the one the Lean checks (F5). Lemma 9 does need its partner (F6, COMPUTED).
5. COMPUTED with my own code, on all 56 Eulerian triangulations with 6 to 14 vertices (cubic graphs with 8 to 24 vertices), all rootings: every lemma in its primal form holds, and both worked examples of Section 11 reproduce digit for digit. Counts are in `code/README.md`.

## 1. Audit boundary

**Conclusion C0 (Theorem T).** For every finite simple cubic bipartite 3-edge-connected plane graph `G` and every edge `e0` of `G`, there is a perfect matching `P` with `e0 ∈ P` and `G - P` connected.

**Corollary C0'.** Every simple cubic bipartite 3-vertex-connected planar graph has, for each edge, a Hamiltonian cycle avoiding it.

**Hypotheses.** Finite, simple, cubic, bipartite, 3-edge-connected, embedded in the oriented sphere. For Lemmas 4 to 12 also: every 3-edge cut has a singleton shore.

**Fixed data.** A bipartition `B, W`. The edge `e0 = b0 w0` with `b0 ∈ B`. `R` the three faces at `b0`, `A = B \ {b0}`, `X` the other faces.

**Accepted primitives.** I accept what the note lists in Section 2, read as statements about a connected graph embedded in the sphere:
- P1. Euler's formula `|V| - |E| + |F| = 2` for a connected plane graph.
- P2. Facial boundary walks: every face has a closed boundary walk, and the three sectors at a cubic vertex are consecutive in the rotation.
- P3. Deleting an edge whose two sides are distinct faces merges those two faces and changes no other face.
- P4. Contracting a nonloop edge keeps a plane embedding with the same faces.
- P5. In a 2-connected plane graph no facial boundary walk repeats a vertex.
I also accept integral max-flow min-cut, finite-dimensional linear algebra over `F_2` and over the reals, and that an even-degree finite multigraph with an edge contains a circuit.

**Not accepted by name alone.** Three planar facts the proofs use and Section 2 does not list. I name them P6 to P8 and treat them in F1. They are standard and true. They are missing from the list, which the brief asks me to check for completeness.

**In scope.** Sections 1 to 9 and 11 of the note. The LaTeX file is a typeset copy of the same text; I compared the lemma statements and the displayed equations and found no difference.

## 2. Obligation graph

```text
C0' Barnette's statement
    <- R, AND: C0, V1 (3-vertex-connected cubic simple => 3-edge-connected)

C0  Theorem T
    <- R0, strong induction on |V(G)| with "for every e0" inside the hypothesis
       AND: C1, L13, I1, I2

C1  Theorem T when every 3-edge cut has a singleton shore
    <- R1  AND: L4, L8, L9, L10, L12

I1  the cap that keeps e0 is a valid smaller input, and e0 is an edge of it
I2  the second cap is a valid smaller input, the edge a omitted by the first cycle is an edge of it,
    and if e0 is a cut edge then a = e0

L13 caps and gluing
    <- AND: K1 (shores connected), K2 (ell in {0,3}, so the cut ends on one side share a colour),
            K3 (three distinct ends on each side), K4 (cap simple, cubic, bipartite),
            K5 (cap plane: P4), K6 (cap 3-edge-connected: cuts lift), K7 (cap smaller),
            K8 (two cap cycles omitting the same cut edge glue to a Hamiltonian cycle)

L4  a pair exists
    <- AND: L1 (|A| = |X|), M1 (capacity criterion (3.1) by integral max-flow),
            M2 (minimal deficient Y: K connected), M3 (W_1 empty), M4 (K induced, cut = |B_1|, black inner ends),
            M5 (Euler for K: d(Y) = 4 - 2k - c/3, uses P7), M6 (k >= 1, c >= 3, hence k = 1, c = 3),
            M7 (the cut is nontrivial, contradiction with the hypothesis)

L8  some pair has circuit-free Q_s
    <- AND: L4, N1 (D(r,s) is a disjoint union of face circuits covering X, each a state circuit for r),
            N2 (pairs with the same D are the 2^c orientations), L5 (h odd, delta-sum -3 sigma),
            L6 (slope = sigma |W ∩ S| > 0), N3 (group sum (6.3) and its prefactor),
            N4 (lowest coefficient (6.4) is a nonempty sum of positive terms), L7

L7  cancellation for a cyclic second state
    <- AND: S3 (a circuit of Q_s is directed by every partner and avoids R), L5 (h odd),
            N5 (reversal is a fixed-point-free involution on partners that flips the sign)

L6  flow weights
    <- AND: F0 (the path flow has divergence |W| at b0, -1 at whites, 0 elsewhere),
            F1' (local potentials are consistent at each b in A), L3, L2a (cut side avoids b0)

L5  four counts
    <- AND: L2a (circuit = bond, shores connected, no root face meets S),
            L2b (Euler (2.1) and no pinch), Q1 (cubic count), Q2 (colour count),
            Q3 (state count: U = r(B∩S) ∪ C, overlap ell), L3 (signed part only)

L3  one sign sigma around an oriented face circuit
    <- AND: D1 (delta is defined with one sense of rotation at all black vertices),
            P6 (coherent orientation of all facial boundaries),
            O1 (delta(f,g) is the coefficient of the edge b->w in the boundary of g),
            O2 (real facial boundaries span the real cycle space), L2a

L2a face circuits are exactly bonds; shores connected; cut side
    <- AND: T1 (faces are linked through edges: P3, P4, P1), T2 (boundary vectors span the cycle space: P1),
            T3 (cut space is the orthogonal complement of the cycle space),
            T4 (a face circuit is a minimal cut), T5 (a cut contains a face circuit),
            T6 (bond <=> both shores connected), T7 (mixed face has a cut edge: P2)

L2b |S| + |U_S| = |E_S| + 1 for connected complementary shores; mixed faces are the circuit faces
    <- AND: P1 for G and for G[S-bar], P3, P8, T7

L1  facial cycles, three faces at a vertex, two faces share at most one edge, counts
    <- AND: G 2-connected (bridge argument), P5, L2a (general part only), P1

L9  recovery tree           <- AND: partner r (one root face per component), L2a (T5), L1 (counts)
L10 matching from the tree  <- AND: L9
L11 matching cut balance    <- AND: cubic, bipartite, perfect matching
L12 connected complement    <- AND: L10 (P's edge at b lies on s(b)), L5 applied to s, L11, L2a (T5)
```

No cycle. Lemma 1 cites Lemma 2 for "two faces share at most one edge", and Lemma 2 cites Lemma 1 nowhere in its general part (T1 to T6 hold for any connected plane graph). The note says this. It would read better with the order swapped (F8).

## 3. Critical findings

### F1. The list of accepted planar facts is incomplete, and the setting is not fixed (`side condition`, discharged with the additions below)

Section 2 says what is accepted: boundary walks with cyclic orders, Euler, deletion merging two distinct faces, contraction of a nonloop edge, the cut-vertex criterion. The proofs also use:

- P6. Coherent orientation. All facial boundary walks can be traversed with the face on the left, and then every edge is traversed once in each direction, by the walks of its two sides. Used in Lemma 3 ("orienting every facial boundary consistently") and already in Lemma 2 ("assigns equal coefficients to the two faces at each edge", which is the unoriented shadow of it).
- P7. Faces of a subgraph. If `K ⊆ G` then a face of `G` whose boundary lies in `K` is a face of `K`, every other face of `K` is a union of faces of `G` with deleted edges and vertices, and Euler holds for `K` when `K` is connected. Used in Lemma 4 for `K`, with the sentence "the omitted root lies in one of these faces".
- P8. Deleting an edge whose two sides are the same face, or an isolated vertex, creates no face and changes no other face. Used in Lemma 2(b): while the stars of `S` are removed, later edges do have the same merged face on both sides.

All three are true and standard. The question the brief asks is whether the list hides the hard part. It does not. Here is where each item that costs the Lean hundreds of lines lands in the note.

| Lean effort (DIFFERENCES.md) | Where the note does it | My judgement |
| --- | --- | --- |
| both sides of a minimal cut connected (`Bond.connected_shore`) | Lemma 2, "a cut is minimal precisely when both shores are connected" | Complete, four lines, no planarity. |
| no vertex pinched (`mixed_corner_on_boundary`, with `vertex_flow_circuit`) | Lemma 2, "traverse the boundary walk of a face with vertices in both shores" | Complete given P2. In the primal the pinch question is whether a face boundary is one closed walk. That is P2. |
| Euler for the cut side (`region_euler`, `region_connected`) | Lemma 2(b), deletion of the stars of `S` | Correct. The thinnest proof in the note. Needs P8 and uses both connectivities. See F4. |
| the dual is simple, each vertex star a triangle (`make_coloredDual`) | Lemma 1 | Complete given P5. |
| a cap has a dual again (`cap_duality`) | Lemma 13, one sentence on contraction | Complete given P4. |
| a drawing has an algebraic dual (1,078 lines) | Lemma 2, face boundaries span the cycle space | Complete given P1, P3, P4. This is Whitney's argument and is the right length. |

What the list does hide is the Jordan curve theorem, if "plane graph" means a drawing. P1 and P5 are proved from it in every textbook (for example Diestel, Graph Theory, Section 4.2). The sentence "We do not invoke a Jordan curve labelling theorem" is true of what the note adds and should not be read as "the proof is free of the Jordan curve theorem". If instead a plane graph is a rotation system of genus zero, P1 is the definition and P3, P4, P5, P8 are short lemmas about maps, but then the corollary for planar graphs needs the theorem that a planar graph has such a rotation system. Either choice is fine. The note should make one.

Exact replacement for the first paragraph of Section 2:

> A plane graph is a connected graph drawn on the oriented sphere. We use the following standard facts and nothing else about the drawing. (P1) Euler's formula. (P2) Every face has a closed boundary walk, and consecutive edges of the walk are consecutive in the rotation at their common vertex. (P3) When all boundary walks are traversed with the face on the left, every edge is traversed exactly twice, once in each direction. (P4) Deleting an edge with two distinct faces on its sides merges these two faces. Deleting an edge with the same face on both sides, or an isolated vertex, creates no new face. No other face changes. In particular a face of `G` whose boundary lies in a subgraph is a face of that subgraph. (P5) Contracting a nonloop edge gives a plane graph with the same faces. (P6) In a 2-connected plane graph no boundary walk repeats a vertex. These facts rest on the Jordan curve theorem in the usual way. Beyond them we use no separation argument: no curve is drawn through faces, no cycle is detoured, and no region is labelled by the two sides of a cycle.

### F2. The second definition of `δ` allows a choice that breaks Lemma 3 (`side condition`, CORRECT AFTER FIX)

Section 2: "Equivalently, fix the cyclic order of the three faces around `b` and give its three cyclic transitions sign `+1`." A reader can take this as a free choice of one of the two cyclic orders at each black vertex. Then Lemma 3 is false: reverse the order at one black vertex `b`, and (2.2) fails on every face circuit through an edge at `b`, since `δ` changes sign on that edge and on no other. Lemma 7 survives (it uses only that the two transitions into `s(b)` have opposite signs), and that is why the slip is easy to miss. Lemmas 3, 5 (signed part), 6 and 8 need the coherent choice.

Exact replacement:

> Equivalently, list the three faces around `b` in counterclockwise order, the same sense at every black vertex, and give the three transitions that follow this order the sign `+1` and their reverses the sign `-1`.

### F3. The proof of Lemma 3 asserts its key cancellation (`missing` step, supplied; GAP closed below)

The proof says: "Its pairing with a facial boundary is zero: arrival and departure at each listed face cancel." Nothing before this sentence connects `δ`, which is defined at a black vertex, with the sign of an edge in a facial boundary. That connection is the whole content of the lemma. The following is mine.

> Orient every facial boundary with its face on the left, and every edge from its black end `b` to its white end `w`. Let `f, g` be the two faces at `e`. Crossing `e` from `f` to `g` with `b` on the left means that `e`, directed from `b` to `w`, has `g` on its left and `f` on its right. So `e` has coefficient `+1` in `∂g` and `-1` in `∂f`. In both cases
> `δ(f,g) = [∂g](e) = -[∂f](e)`.
> Now let `x(e_i) = δ(f_i, f_{i+1})` and `x = 0` off the circuit. The only circuit edges on `∂f_i` are `e_{i-1}` and `e_i`, so
> `⟨x, ∂f_i⟩ = δ(f_{i-1}, f_i)·[∂f_i](e_{i-1}) + δ(f_i, f_{i+1})·[∂f_i](e_i) = δ(f_{i-1},f_i)² - δ(f_i,f_{i+1})² = 0`,
> and `⟨x, ∂f⟩ = 0` for a face off the circuit.

With this inserted the rest of the proof is right: `x` is orthogonal to the real cycle space, so it is a gradient, its potential is constant on each shore because the shores are connected and `x` vanishes inside them, and its values are `±1`. COMPUTED: a single `σ` on all 1,066,157 face circuits of the 56 graphs, for both shores and both colourings (4,264,628 checks), and on all 84,984 state circuits (`code/check_lemmas.py`, checks `L3 …`).

### F4. Lemma 2(b), the Euler count for a shore (`side condition`, discharged; one sentence to add)

The identity `|S| + |U_S| = |E_S| + 1` is true, and it does need both shores connected. `G[S]` connected makes all faces of `U_S` merge into one. `G[S̄]` connected gives Euler for the remainder. The proof is right but silent on why no face is created or lost beyond the merging. Add after "No face outside `U_S` changes":

> Each deleted edge has both its sides in `U_S`, so by (P4) every step either merges two faces that come from `U_S` or changes nothing, and removing the isolated vertices of `S` at the end changes nothing.

I checked the algebra: subtracting Euler for `G[S̄]`, which has `|V|-|S|` vertices, `|E|-|E_S|` edges and `|F|-|U_S|+1` faces, from Euler for `G` gives (2.1). COMPUTED: (2.1) on both shores of all 1,066,157 bonds of the 56 graphs. The number of bonds, found by running over all vertex subsets, equals the number of face circuits in every graph.

### F5. Lemma 12 proves more than it states (`too strong` in reverse: the statement is weaker than the proof)

The proof of Lemma 12 uses three things about `P`: it is a perfect matching, `s` is a state, and the edge of `P` at each `b ∈ A` lies on the face `s(b)`. It never uses that `P` came from the tree of Lemma 9, that `Q_s` is circuit-free, or that `s` has a partner. So it proves:

> **Lemma 12'.** Let `s` be a state and `P` a perfect matching of `G` whose edge at every `b ∈ A` lies on `s(b)`. Then `G - P` is a Hamiltonian cycle.

This is exactly the hypothesis set of Lean's `selected_forest` (LEAN-MATCH.md, M5). It is the cleaner statement and it shows the reader what the pair and the forest are for: they are needed only to produce such a `P` (Lemmas 9 and 10). COMPUTED: for every perfect matching and every root on 8 to 24 vertices (186,476 cases), "a compatible state exists" and "the complement is connected" coincide (`L12 general`). The converse direction is an observation in this range only.

### F6. Lemma 9 needs the partner (COMPUTED, supports the text)

The note says the partner is used to get one root face per component. I tested the hypothesis. For every state `s` with circuit-free `Q_s` and no partner, and every root edge, the graph `K` is not a tree: 25,272 cases on 8 to 24 vertices, none the other way. In the same range every circuit-free second state that has a partner has exactly one (3,256 states). So "circuit-free `Q_s`" alone is not enough and the lemma is stated with the right hypothesis.

### F7. The hypothesis ledger of Section 9 is wrong in three places (`too strong`, wording; CORRECT AFTER FIX)

- "Simplicity rules out two-vertex facial cycles and ensures the small-shore cut argument." Simplicity is not an independent hypothesis. A loop cannot occur in a cubic bridgeless graph, and two parallel edges `uv` in a cubic 3-edge-connected graph force `|V| = 2`, since otherwise `{u,v}` has at most two outgoing edges. So "simple" can be replaced by "`|V| > 2`" in Theorem T. In Lemma 4 the phrase "of length at least four by simplicity and bipartiteness" is more than the argument needs. A cycle has at least two vertices and that is all that is used.
- "Three-edge-connectivity … excludes a deficient cut of size less than three." The proof of Lemma 4 gets `c ≥ 3` from `c > 0` and `3 | c`, not from connectivity.
- Missing from the ledger: 3-edge-connectivity is what makes `G` 2-connected in Lemma 1, hence the facial cycles, the three distinct faces at a vertex and, through Lemma 2, the simple face links.

Exact replacement for the two sentences:

> Simplicity is automatic once `|V| > 2`: parallel edges in a cubic 3-edge-connected graph force two vertices. We keep the word because Barnette's conjecture is stated for simple graphs. Three-edge-connectivity makes `G` 2-connected, which gives facial cycles and three distinct faces at each vertex (Lemma 1). It makes face links simple, it is the induction hypothesis that survives capping, and it makes the shores of a 3-edge cut connected with three distinct ends (Lemma 13).

### F8. Smaller points, none on a failing node

- Lemma 1 before Lemma 2. Lemma 1 uses the general part of Lemma 2(a). Move the first four paragraphs of the proof of Lemma 2 (span, cut space, circuits are bonds, shores) in front of Lemma 1 as a lemma about connected plane graphs, and keep cut sides, no pinch and (2.1) after it.
- Lemma 4, `W_1`. "Each is incident with a face outside `Y`" is right. Add that the two neighbours lie in `A`, since `b0 ∉ K`. Otherwise the deficit sum, which runs over `A`, is not visibly the one that drops. Also say that `Y \ {f}` is nonempty because its deficit is positive.
- Lemma 4, `k ≥ 1`. This uses P7.
- Lemma 5. `|W∩S| = |B∩S| + 1` is a consequence that Lean does not state. Keep it, it is what makes the slope a count of white vertices.
- Lemma 8. The prefactor `(-1)^{(n-c(D))/2}` is right. I recomputed it by hand and on every group (`L8 group sum equals (6.3)`).
- Lemma 13. The statement says "contract either shore". The proof shows that the result does not depend on the spanning tree. One clause would say so.
- Theorem T, last paragraph. Right. The case of an empty cut is disconnection, excluded by 3-vertex-connectivity.
- Section 6. "There is no index `J`, exponential, or analytic limit" is accurate.

### F9. Coverage of the numerical evidence for Lemma 7

Cancellation is rare in small cases. A second state that has a partner and a circuit in `Q_s` occurs twice up to 12 faces, four times at 13 faces and fourteen times at 14 faces, twenty in all. Lemma 7 is therefore the least tested lemma numerically. Its proof is short and I checked each line, including the two facts that reversal keeps `r` a bijection onto `X` and that the circuit avoids `R`.

## 4. Answers to the specific questions of the brief

(a) Planar facts. See F1. The list is true, standard, three items short, and silent on the setting. It does not hide the hard part. The hard parts are proved in Lemmas 1 and 2, with Lemma 2(b) the thinnest.

(b) The cut side and the four counts. Correct. "Inside" is the shore of the bond that misses `b0`. It exists because a face circuit is a bond (L2a), it is connected, and no root face meets it because a face with vertices on both shores lies on the circuit. I re-derived all four counts and the elimination `h = 2ℓ + 3`.

(c) The flow and `1 + aX`. Correct. The local potentials are consistent because the flow has zero divergence at every black vertex other than `b0`. The slope on a circuit is `σ` times the number of white vertices in the cut side. A second flow with the same divergences gives the same slopes (COMPUTED, `L6 … second flow`).

(d) Cancellation and nonvanishing. Correct. Oddness of `h` is all that Lemma 7 uses. The exact value `-3σ` is used in Lemma 8 to give all groups with `m` circuits the sign `(-1)^{(n-m)/2}`. The polynomial has integer coefficients, and its lowest coefficient is `(-1)^{(n-m)/2} Σ_D ∏_C |W ∩ S_C|` (COMPUTED on every rooting with a pair).

(e) Recovery. Correct. Lemma 9 gives a spanning tree of `G`, Lemma 10 a perfect matching inside it, Lemmas 11 and 12 a contradiction between `h = 2ℓ` and `h = 2ℓ + 3` for any face circuit inside `P`. See F5 for the sharper statement.

(f) Induction. Correct. The induction statement is Theorem T itself with the quantifier over `e0`, by strong induction on `|V|`. No base case is needed, since a graph with no nontrivial 3-edge cut is handled directly. The first cap keeps `e0`, the second is asked to contain the edge the first cycle omits. If `e0` is a cut edge, that omitted edge is `e0`. COMPUTED: I ran the proof as a recursive procedure for every graph, every edge and both choices of black end (3,642 runs, recursion depth up to 2).

(g) Where each hypothesis is used. Bipartite: `|A| = |X|`, the black end of an edge, the colour counts in Lemmas 4, 5, 11, 13, the matching in Lemma 10. Cubic: three faces at a vertex, `q_s(b)`, the counts, degrees in Lemma 9, caps. 3-edge-connected: 2-connectivity and so Lemma 1, simple face links, Lemma 13. No nontrivial 3-edge cut: Lemma 4 only. Planar: Lemmas 1 to 3, Euler for `K` in Lemma 4, contraction in Lemma 13. Simple: see F7. The note's Section 9 agrees except as noted there.

## 5. Verdicts per lemma

| Lemma | Verdict | Remark |
| --- | --- | --- |
| 1 | CORRECT | Depends on P5 and on the general part of Lemma 2. Reorder (F8). |
| 2 | CORRECT AFTER FIX | Add the sentence of F4. Replace the list of planar facts (F1). |
| 3 | GAP, closed | The cancellation is asserted. Missing argument supplied in F3. Fix `δ` (F2). |
| 4 | CORRECT | Two clauses to add (F8). Supplies what Li omits. |
| 5 | CORRECT | Matches `state_disk_count` and `disk_boundary_imbalance` hypothesis for hypothesis. |
| 6 | CORRECT | |
| 7 | CORRECT | Not machine-checked in this form, as STATUS says. |
| 8 | CORRECT | Not machine-checked in this form. |
| 9 | CORRECT | Partner needed (F6). |
| 10 | CORRECT | |
| 11 | CORRECT | Identical to Lean. |
| 12 | CORRECT | Restate as Lemma 12' (F5). |
| 13 | CORRECT | |
| Theorem T | CORRECT | |
| Section 9 | CORRECT AFTER FIX | Replacement text in F7. |

No lemma is WRONG. I looked for counterexamples to each by enumeration and found none.

## 6. Comparison with Li's note, step by step

Sources: `papers/A-Note-On-Barnette.pdf` and the audit `research/2026-11-14_fable_dependency-graph/audit-li.md`, whose finding numbers (L-F…) I quote.

| Step | Li | Primal note | Clearer | More complete |
| --- | --- | --- | --- | --- |
| Objects | `aux(G)`, the face and black vertex incidence graph `G_FB`, 2-factors of `H = G_FB - N[b0]`, cycle-breaking 2-factor | states `A → X`, pairs, `Q_s` | Even. Li's 2-factor is one object where the note has an ordered pair. The note's `Q_s` is lighter than "cycle-breaking". | Even. |
| First pair | Lemma 9 with Ore's theorem and Claim 12 | Lemma 4 with max-flow | Note | Note. It states the balance `\|A\| = \|X\|` that Li omits (L-F1), the divisibility that gives `c = 3` (L-F3), and why the cut is nontrivial. |
| Inside of a cycle | bounded side of a polygon in a straight-line drawing | shore of a bond missing `b0` | Li for the picture, note for the proof | Note. Li needs Fáry and general position, never defined (L-F4). |
| Disk identity | Claim 25, `t_out = \|C\|/4 + 3/2`, by Euler inside the cycle with hexagonal inner faces | Lemma 5, four counts | Note | Note. Li leaves V1 (everything inside is in `H`) and the no-pinch fact unsaid. |
| Signs and weights | `cw`, `τ`, `dir`, half-rays to the top, crossings of a ray with a cycle | `δ`, one flow, local potentials | Note, clearly. No coordinates. | Note. |
| Cancellation | involution `ι_1` | Lemma 7 | Even | Even. |
| Nonvanishing | involution `ι_2` on marked objects, written for `c_min = 1`, sketched for `c_min > 1` in Appendix B | Lemma 8, one polynomial, any `m` | Li is the more bijective and some readers will prefer it. The note is shorter. | Note. Li's B2, B3, B5 are unwritten (L-F6). |
| Tree | Lemma 8, `G_FB - M2` is a spanning tree, then tree-cotree to a tree on white vertices | Lemma 9, a spanning tree of `G` itself | Note | Even. Li's T1 is unwritten (L-F9). |
| Matching | Claim 31 | Lemma 10 | Even | Even. |
| One cycle | Lemma 30, innermost cycle and oriented traces | Lemmas 11 and 12, cut balance | Note | Note. Li's argument is correct (L-F8) but needs nesting of cycles. |
| Reducible case | Appendix C | Lemma 13 | Even | Note. It separates the case `e0` in the cut and keeps edge connectivity, so no appeal to "vertex and edge connectivity agree for cubic graphs" at each step (L-F12). |

Overall. Li's note is the better first read for someone who wants pictures and a bijective proof. The primal note is the more complete proof. Every step that the audit of Li had to supply is written out here, and the note avoids the straight-line drawing altogether. What the note lacks and Li has is figures. It has none.

## 7. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0' | Barnette's statement, any edge avoided | root | R / claim | root | C0, V1 | discharged |
| C0 | Theorem T | C0' | R0 / AND | major claim | C1, L13, I1, I2 | discharged |
| V1 | cubic simple 3-vertex-connected implies 3-edge-connected | C0' | AND | algebraic/logical step | Section 8, last paragraph | discharged |
| I1 | first cap valid, contains `e0` | C0 | AND | proved earlier | L13 | discharged |
| I2 | second cap valid, contains the omitted edge `a`; `a = e0` if `e0` is a cut edge | C0 | AND | algebraic/logical step | L13, the cycle uses two of three edges at the cap vertex | discharged |
| C1 | Theorem T with only trivial 3-edge cuts | C0 | R0 / AND | major claim | L4, L8, L9, L10, L12 | discharged |
| L13 | caps and gluing | C0 | AND | major claim | K1 to K8 | discharged |
| K1 | both shores of a 3-edge cut connected | L13 | AND | hypothesis | 3-edge-connectivity | discharged |
| K2 | `ℓ ∈ {0,3}` | L13 | AND | algebraic/logical step | colour count mod 3 | discharged |
| K3 | three distinct ends on each side | L13 | AND | side condition | 3-edge-connectivity, both shores have two vertices | discharged |
| K4 | cap simple, cubic, bipartite | L13 | AND | algebraic/logical step | K2, K3 | discharged |
| K5 | cap is a plane graph | L13 | AND | named theorem | P4 (contraction), K1 | discharged |
| K6 | cap 3-edge-connected | L13 | AND | algebraic/logical step | cuts lift | discharged |
| K7 | cap smaller | L13 | AND | side condition | contracted shore has two vertices | discharged |
| K8 | gluing | L13 | AND | algebraic/logical step | two spanning paths and two cut edges | discharged |
| L1 | Lemma 1 | L4, L8, L9 | AND | major claim | P5, P1, L2a, bridge argument | discharged |
| L2a | face circuits are bonds and conversely, shores connected, cut side root-free | L1, L3, L5, L6, L9, L12 | AND | major claim | T1 to T7 | discharged |
| T1 | faces are linked through edges | L2a | AND | named theorem | P1, P3, P4 | discharged |
| T2 | boundary vectors span the cycle space | L2a | AND | algebraic/logical step | T1, P1 | discharged |
| T3 | cut space is the orthogonal complement of the cycle space | L2a | AND | algebraic/logical step | path sums | discharged |
| T4 | a face circuit is a minimal cut | L2a | AND | algebraic/logical step | T2, T3 | discharged |
| T5 | every cut contains a face circuit | L2a, L9, L12 | AND | algebraic/logical step | even degrees | discharged |
| T6 | bond iff both shores connected | L2a | AND | algebraic/logical step | `G` connected | discharged |
| T7 | a face with vertices in both shores has a cut edge | L2a, L2b | AND | side condition | P2 | discharged |
| L2b | (2.1) and mixed faces are the circuit faces | L5 | AND | major claim | P1, P3, P8, T7 | discharged, with F4 |
| P6 | coherent orientation of facial boundaries | L3 | AND | missing from the list | standard, F1 | discharged by addition |
| P7 | faces of a subgraph | L4 | AND | missing from the list | standard, F1 | discharged by addition |
| P8 | deleting an edge with one face on both sides, or an isolated vertex | L2b | AND | missing from the list | standard, F1 | discharged by addition |
| D1 | `δ` uses one sense of rotation at all black vertices | L3 | AND | definition | first definition yes, "equivalently" no | discharged with F2 |
| O1 | `δ(f,g)` is the coefficient of the edge `b→w` in `∂g` | L3 | AND | missing | supplied in F3 | discharged by the referee's argument |
| O2 | real facial boundaries span the real cycle space | L3 | AND | algebraic/logical step | T1, P1, P6 | discharged |
| L3 | Lemma 3 | L5, L6 | AND | major claim | D1, P6, O1, O2, L2a | discharged, with F2 and F3 |
| L4 | Lemma 4 | C1, L8 | AND | major claim | L1, M1 to M7 | discharged |
| M1 | capacity criterion by integral max-flow | L4 | AND | named theorem | `\|A\| = \|X\|`, unit capacities | discharged |
| M2 to M4 | `K` connected, `W_1` empty, `K` induced with `\|B_1\|` black-ended cut edges | L4 | AND | algebraic/logical step | minimality of `Y` | discharged |
| M5 | `d(Y) = 4 - 2k - c/3` | L4 | AND | named theorem | P1 for `K`, P7 | discharged |
| M6, M7 | `k = 1`, `c = 3`, the cut is nontrivial | L4 | AND | algebraic/logical step | `3 \| c`, `c > 0`, `b0` and a white end outside | discharged |
| L5 | Lemma 5 | L6, L7, L8, L12 | AND | major claim | L2a, L2b, Q1 to Q3, L3 | discharged |
| Q1, Q2 | cubic and colour counts | L5 | AND | algebraic/logical step | cubic, bipartite | discharged |
| Q3 | `U = r(B∩S) ∪ C` with overlap `ℓ` | L5 | AND | algebraic/logical step | `r` bijective, T7, cut side root-free | discharged |
| L6 | Lemma 6 | L8 | AND | major claim | F0, F1', L3, L2a | discharged |
| L7 | Lemma 7 | L8 | AND | major claim | S3, L5, N5 | discharged |
| S3 | a circuit of `Q_s` is directed by every partner and avoids `R` | L7 | AND | algebraic/logical step | tails are distinct and lie in `X` | discharged |
| L8 | Lemma 8 | C1 | AND | major claim | L4, N1 to N4, L5, L6, L7 | discharged |
| L9 | Lemma 9 | L10 | AND | major claim | partner, T5, L1 | discharged |
| L10 | Lemma 10 | L12, C1 | AND | major claim | L9 | discharged |
| L11 | Lemma 11 | L12 | AND | algebraic/logical step | two degree counts | discharged |
| L12 | Lemma 12 | C1 | AND | major claim | L10, L5 for `s`, L11, T5 | discharged |

## 8. Verdict

**FOLLOWS.** Every obligation on the one route the note supplies is discharged: C0 from C1, L13, I1, I2, and C1 from L4, L8, L9, L10, L12. Three nodes are discharged only with material that is not in the note as written. P6, P7 and P8 are planar facts the proofs use and the list in Section 2 omits. O1 is the step in Lemma 3 that I supply in F3. D1 needs the rewording of F2. None of these is a wrong statement and none changes the route. With the replacement texts of F1, F2, F3, F4 and F7 applied, I regard the note as a correct and complete informal proof of Theorem T relative to the stated planar background.

Review state for the map: proved, one independent AI referee (this report) plus the author's own audit, human check pending. A referee raises the review state, not the tier.
