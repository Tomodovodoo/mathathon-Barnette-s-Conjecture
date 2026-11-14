# The induction does not close: the two missing lemmas

Fable 5.2, 2026-11-14. Notation of `research/BRIEF.md`, `RESIDUAL-CASES.md` (cited as RC) and `research/2026-11-14_opus_route-induction/PROOFS.md` (OP). There is no `INDUCTIVE-PROOF.md`, because the proof is not complete. This file says exactly what is proved, what is missing, and what the evidence is.

## 1. The induction, with every step tagged

Statement `P(T, t0)`: if the rooted Eulerian triangulation `(T, t0)` has a pair, it has a tree matching. Strong induction on `|V(T)|` over all simple Eulerian triangulations and all black roots.

| Step | Statement | Status |
| --- | --- | --- |
| 0 | Every Eulerian triangulation has at least 6 vertices and at least 6 vertices of degree 4 (degrees are even and at least 4, and `sum (6 - deg) = 12`). | `PROVED-HERE` |
| 1 | Base: the octahedron has 2 tree matchings at every root. | `COMPUTED` (`data/census_6_13.json`, 8 rooted instances) |
| 2 | `T` has a separating triangle and a pair. Then the triangle has white inner boundary, `T` is `T1` with `T2` glued into a white face, both are smaller, pairs and tree matchings multiply. So `P(T1)`, `P(T2)` give `P(T)`. | Imported: pair criterion (`research/2026-11-14_opus_route-graph-theory/PROOFS.md` Thm 2.1, refereed in `research/2026-11-14_sol_referee-structure/INTEGRATION.md` §2) and multiplicativity (`research/2026-11-14_fable_route-categorical/PROOF.md` Prop. 6). I re-read the proof of Prop. 6 and found it correct. |
| 3a | `T` has no separating triangle and `V > 6`. At every degree-4 vertex at least one of the two merges gives a simple triangulation. | `PROVED-HERE` (REFEREE.md §4, a short proof of route-graph-theory Lemma 6.1) |
| 3b | (G) Some non-root degree-4 vertex `x` and merge `M` give a simple `T/M` with a pair. | `CONJECTURE`. `COMPUTED`: all 62,416 rooted instances without separating triangle, `8 <= V <= 19`. |
| 3c | `T/M` is a simple rooted Eulerian triangulation with `V - 2` vertices and a pair. By induction it has a tree matching. It may have separating triangles. That is allowed. | `PROVED-HERE` (nothing to prove beyond 3b) |
| 3d | One-sided case. If `T/N` has no tree matching, then `#TM(T) >= #TM(T/M) > 0`. | `PROVED-HERE` (RC Theorem 4(a)) |
| 3e | Two-sided case. If `T/M` and `T/N` both have tree matchings, then `T` has one. | `CONJECTURE` (ML2 below) |

Everything except 3b and 3e is proved without a signed count. The generation theorem of Batagelj is not used anywhere: step 0 supplies the degree-4 vertex and step 3a the simple merge.

## 2. Missing lemma ML2 (the two-sided step)

**ML2.** Let `x` be a non-root vertex of degree 4 of a rooted Eulerian triangulation, and suppose `T/M` and `T/N` both have tree matchings. Then not every tree matching of `T/M` is exceptional.

Here a tree matching of `T/M` is *exceptional* if, as an outer state (RC §1), it has pattern `P_1 = {a v1 | b v2}` and its rotation again has pattern `P_1`. In the words of OP: the lift fails and `b` lies in `K2'`. By RC Theorem 4(c), ML2 is equivalent to "`T` has a tree matching" in this situation, and by RC Theorem 3 it is symmetric in `M` and `N`.

Why this is the smallest statement I can isolate.

- It is exactly what existence needs. The inequality `#TM(T) >= #TM(T/M)` (OP's (L)) is stronger. By RC Theorem 4(b) it would follow from `#TM(T/N) >= 2 |E_N|`, that is, from "at most half of the tree matchings of the other contraction are exceptional".
- It cannot be weakened to "some tree matching of `T/M` lifts". That statement is `REFUTED`: at `V = 18` there are 50 rooted contractions, all with `T` free of separating triangles and `x` without root neighbour, in which `T/M` has 2 tree matchings and neither lifts. Both rotate. First instance: `plantri -b -a 18` graph 309, root `(5, 0, 6)`, `x = 11`, merge `{10, 2}` (`data/nolift_18.jsonl`).
- It cannot be avoided by choosing `x`. A vertex with exactly one good contraction closes the step by 3d, and such a vertex exists in most instances, but not all: `V = 14`, graph 31, has only two-sided vertices at all 24 roots, and there are 2, 30, 97, 46 such rooted instances at `V = 16, 17, 18, 19` (`data/onesided_*.json`).

Evidence for ML2 (`COMPUTED`).

- Some tree matching of `T/M` lifts or rotates in every one of the 203,497 contractions with tree matchings at `V = 18` (`data/nolift_18.log`) and in all smaller ones (`V <= 17`: follows from `some_lift_fail = 0` in `data/census_*.json`).
- `#TM(T) >= #TM(T/M)` on all 1,202,792 rooted contractions with `V <= 18`.
- The exceptional fraction `|E_M| / #TM(T/M)` never exceeds 1/2 for `V <= 17` and equals 1/2 in some cases (`data/superadd_6_17.json`). `CONJECTURE` ML2+: `2 |E_M| <= #TM(T/M)`. Together with RC Theorem 4(b) this would give the contraction inequality in full. Test: extend `code/superadd.py` to `V = 18, 19`.

A possible line of attack, `HUNCH`. An exceptional tree matching has a floating or rooted component `K2` containing `v2`, `b` and `c`, with the black faces `g`, `g'` both on the dual cycle of the forest. The value 1/2 suggests an involution on `TM(T/M)` that maps exceptional tree matchings to non-exceptional ones. Sign reversal is a candidate, since `TM(T/M)` is sign-balanced (OP Prop. 4.1), but the known proof of sign balance goes through pairs with cyclic `Q_s` and gives no involution on tree matchings. Test: on `data/exceptions_*.jsonl`, check whether the exceptional tree matchings of one contraction all have the sign of the minority.

## 3. Missing lemma ML1 = (G), and what I proved about it

**ML1.** Let `T` have no separating triangle and more than 6 vertices, and let `t0` be a black face. Then some non-root degree-4 vertex `x` has a merge `M` with `T/M` simple and without black-inner separating triangle relative to `t0`.

I did not prove it. I did turn it into a statement about short cycles and tight sets, and proved one restriction on a counterexample.

Notation. For `S ⊆ X` let `f(S) = sum_{t in A} min(2, |t ∩ S|) - 2|S|`. A pair exists iff `f >= 0` (OpenAI (3.1)). `f` is submodular, because `min(2, |t ∩ S|)` is a concave function of `|t ∩ S|`. So when a pair exists the *tight* sets (`f = 0`) are closed under union and intersection.

**Lemma A (deficiency formula).** `PROVED-HERE` by rearranging the proof of OpenAI Prop. 3.1. Not machine-checked. Let `U = V - S` with `T[U]` connected. Then

    f(S) = sum over the faces R of T[U] that are not faces of T of (d_R + w_R - 6) / 3,

where `d_R` is the boundary length of `R` and `w_R` the number of boundary sides whose face of `T` inside `R` is white.

*Proof.* With `p, m` the vertices and edges of `T[U]`, `b, w` its actual black and white faces and `beta_R` the black minus white faces of `T` inside `R`: `2m = 3(b + w) + sum d_R`, Euler's formula, and `w - b = sum beta_R` give `m - b = 2p - 4 - (1/2) sum ((d_R - 4) - beta_R)`. The paper shows `f(S) = (2p - 4) - (m - b)`. Side counting gives `3 beta_R = d_R - 2 w_R`. ∎

So a cycle of length 4 always bounds two regions of deficiency 0. A cycle of length 5 has one side with `w = 1` (four black faces and one white face along it, deficiency 0) and one side with `w = 4` (deficiency 1). Call the first the *black side*.

**Lemma B (bad merges).** `PROVED-HERE`; the equivalence with the pair criterion is also `COMPUTED` (`criterion_fail = 0` on 71,224 rooted instances, `V <= 18`). Let `T` have no separating triangle. The merge `M` at `x` fails to give a simple triangulation with a pair iff there is a cycle `Z` through `v1 x v2` of length 4, or of length 5 with `t0` not on its black side.

*Proof.* `T/M` is not simple iff `v1, v2` have a common neighbour outside `{x, a, b}` (Lemma 0 of RC excludes a loop), that is, iff there is a 4-cycle `x v1 w v2`. A simple `T/M` loses the pair iff it has a separating triangle with black inner boundary. A separating triangle of `T/M` passes through `v` and comes from a path `v1 y z v2` of `T`, so from a 5-cycle `x v1 y z v2`. Its two sides in `T/M` are the two sides of the 5-cycle with the two faces at `x` removed. On each side those two faces have different colours, so the remaining three boundary faces on the black side are black and on the other side white. The inner side is the one without `t0`. ∎

**Lemma C (contraction and tight sets).** `PROVED-HERE`. For `S ⊆ X(T/M)`: if `v` is not in `S` then `f_{T/M}(S) = f_T(S) - [a in S] - [b in S]`, and if `v` is in `S` then `f_{T/M}(S) = f_T(S - v + {v1, v2, x})`. So `T/M` loses the pair iff some `S` avoiding `x, v1, v2` is tight and contains `a` or `b`, or has `f_T(S) = 1` and contains both.

*Proof.* Only `beta1` and `beta2` change. For `v` not in `S` they contributed `[a in S]` and `[b in S]`. For `v` in `S`, put `S'' = S - v + {v1, v2, x}`: the outer faces contribute the same, `beta1` and `beta2` contribute 2 each, and `|S''| = |S| + 2`. ∎

**Proposition D (restriction on a counterexample).** `PROVED-HERE`. Suppose (G) fails for `(T, t0)`. Let `S` be an inclusion-minimal nonempty tight set of `T`. Then every degree-4 vertex `x` in `S` has two neighbours outside `S` that are consecutive in the rotation at `x`.

*Proof.* `T` has a pair, so `f >= 0`. `x` is a non-root, so both merges at `x` are bad. For the merge `M`, Lemma B gives a cycle `Z` through `v1 x v2`, of length 4 or of length 5 with `t0` off its black side. Let `S'` be the set of vertices strictly on the side of `Z` away from `t0`. That side has no chord (a chord would give a triangle at `x`, or one of the triangles excluded in the proof of Lemma B), so it is the only face of `T[V - S']` that is not a face of `T`, and Lemma A gives `f(S') = 0`. `S'` avoids `x` and contains `a` or `b`. `S ∩ S'` is tight and properly contained in `S`, so it is empty, and that neighbour is outside `S`. The merge `N` gives in the same way `v1` or `v2` outside `S`. One of `a, b` and one of `v1, v2` are always consecutive. ∎

What should come next, as a sketch and not a proof (`HUNCH`): by Lemma A a minimal tight set should be the interior of one cycle of length 4, 5 or 6 with `w = 2, 1, 0`, and Euler's formula then puts at least one degree-4 vertex in that interior. Proposition D says each of them is the apex of a face on the boundary cycle. A proof of (G) would then be a finite analysis of at most 6 boundary faces. I did not write this out and I claim nothing beyond Proposition D.

Test for a referee: on the census, list the minimal tight cycles and check that some interior degree-4 vertex is not a boundary apex. If one always exists, (G) follows from Proposition D.

## 4. What is imported if ML1 and ML2 are proved

1. The pair criterion (Hall plus the Euler identity), used in step 2 and in Lemma B. Refereed in this project.
2. Multiplicativity of pairs and tree matchings under gluing into a white face. Refereed in this project.
3. OP Prop. 2.1, Lemma 3.1, Prop. 3.2, Cor. 3.3, which I checked line by line (REFEREE.md).

No signed sum, no disk identity and no generation theorem would be used. The disk identity enters only OP Prop. 4.1 (evenness), which the induction does not need.
