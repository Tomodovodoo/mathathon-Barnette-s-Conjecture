# Integration: what can be cited, with proofs

Opus 5.5, 2026-11-14. Every statement here was refereed in `REFEREE-rainbow.md` or `REFEREE-packing.md`, and is PROVED-HERE (tier T2, refereed by one independent AI referee, human check pending). Authors: Fable (§1 to §3) and Opus, two-tree packing folder (§4); the proofs below are rewritten by me and differ in places from the originals.

## Setting

`T` is an Eulerian triangulation of the sphere with faces coloured black and white, `t0` a black face, `R` its corners (the roots), `A` the other black faces, `X = V(T) \ R`, and `n = |A| = |X|`. `H` is the spoke graph: the centre of every black face (including `t0`) joined to its three corners. `W` is the white-face graph: one vertex per white face, and for each spoke `(t, v)` one edge `e(t, v)` joining the two white faces across the two sides of `t` at `v`.

**Fact 0 (duality).** `W` is the plane dual of `H`. Hence, for a set `S` of spokes, `H - S` is a spanning tree of `H` iff `{e(t, v) : (t, v) ∈ S}` is a spanning tree of `W`.

*Proof.* The face of `H` containing a white face `w` with corners `v1, v2, v3` is bounded by `v1, c(t1), v2, c(t2), v3, c(t3)`, where `ti` is the black face across the side `vi v(i+1)` and `c(ti)` its centre. These are all the faces of `H`, since `|E(H)| - |V(H)| + 2 = (3n + 3) - (2n + 4) + 2 = n + 1`. The spoke `(t, v)` separates the faces of `H` around the two white faces that touch `t` along its sides at `v`. The second sentence is the tree-cotree theorem for connected plane graphs. ∎

A **rainbow tree** is a map `σ: X -> A` with `x` a corner of `σ(x)` such that `F_σ = H - {(σ(x), x)}` is a spanning tree. The **load** of `t ∈ A` is `c_σ(t) = |σ^{-1}(t)| ∈ {0, 1, 2}`, the **excess** is `Σ_t |c_σ(t) - 1|`. A rainbow tree of excess 0 is the inverse of a good state, and every good state arises this way.

Two theorems from the literature are used, both in the form of Schrijver, *A Course in Combinatorial Optimization* (CWI, version of March 23, 2017):

- **Rado** (Exercise 10.26; R. Rado, Quart. J. Math. 13 (1942) 83-89). Subsets `X_1, ..., X_m` of the ground set of a matroid have an independent transversal iff the union of any `t` of them has rank at least `t`.
- **Nash-Williams** (Exercise 10.29, via Edmonds' covering theorem, Exercise 10.28; C. St. J. A. Nash-Williams, J. London Math. Soc. 39 (1964) 12). The edges of a multigraph without loops split into `k` forests iff every nonempty vertex set `Z` spans at most `k(|Z| - 1)` edges.

And one from Schrijver, *Polyhedral combinatorics*, Handbook of Combinatorics, ch. 30, pp. 1674 and 1685-1686:

- **Edmonds** (J. Edmonds, Edge-disjoint branchings, in *Combinatorial Algorithms*, ed. R. Rustin, Academic Press, New York, 1973, 91-96). In a digraph with root `r`, the largest number of pairwise arc-disjoint spanning `r`-arborescences equals the smallest number of arcs entering a nonempty set `U ⊆ V \ {r}`.

## 1. Step R: when a rainbow tree exists

**Theorem 1.** A rainbow tree exists iff no separating triangle of `T` has black inner boundary (the three faces along it, on the side away from `t0`, all black).

*Proof.* For `x ∈ X` let `C_x = {e(t, x) : t ∋ x}`. These sets are disjoint and `C_x` is a cycle through the white faces at `x`. By Fact 0 a rainbow tree is an independent transversal of `(C_x)_{x ∈ X}` in the cycle matroid of `W`, which has rank `n`. Two classes `C_x, C_y` share a white face iff `x` and `y` lie on a common white face, iff `xy ∈ E(T)`. So for `J ⊆ X` the union `⋃_{x ∈ J} C_x` has one component for each component of `T[J]`, and different components touch disjoint sets of white faces. Its rank is `w(J) - comp(T[J])`, where `w(J)` is the number of white faces with a corner in `J`. By Rado, a rainbow tree exists iff

    w(J) >= |J| + 1   for every nonempty J ⊆ X with T[J] connected.     (1)

Fix such a `J` and put `U = V(T) \ J ⊇ R`, `p = |U|`, `m = e(T[U])`, `c` the number of components of `T[U]`. The connected set `J` lies in one face `Φ` of the plane graph `T[U]`. Every other face of `T[U]` contains no vertex of `T` (they are all in `U` or in `Φ`) and no edge of `T` (an edge inside it would join two vertices of `U`, so it would belong to `T[U]`), so it is a face of `T`; conversely a face of `T` with all corners in `U` is open and closed in the complement of `T[U]`, so it is a face of `T[U]`, and it is not `Φ`. Let `b_U`, `w_U` count the black and white faces of `T` with all corners in `U`, let `d` be the number of edge sides on the boundary of `Φ`, and `σ_Φ` the sum over these sides of `+1` or `-1` according as the face of `T` on the `Φ` side is black or white. Then

    p - m + (b_U + w_U + 1) = 1 + c                       (Euler)
    2m = 3(b_U + w_U) + d                                  (sides)
    σ_Φ = 3((n + 1 - b_U) - (n + 1 - w_U)).                (signed sides inside Φ)

The last line holds because each face of `T` inside `Φ` contributes `±3` to its own sides and the sides interior to `Φ` cancel in pairs. Solving gives `w_U = p - c - d/2 + σ_Φ/6`. Since `w(J) = n + 1 - w_U` and `|J| = n + 3 - p`,

    w(J) - |J| - 1 = (c - 1) + (3d - σ_Φ - 12)/6.          (2)

Now `σ_Φ` is a multiple of 3 with the parity of `d` and `|σ_Φ| <= d`, and `d >= 3` because the component of `T[U]` that contains `t0` borders `Φ` and is not a tree. If `c >= 2`, (2) is at least `(d - 3)/3 >= 0`. If `c = 1` and `d >= 4`, (2) is `>= 0`: for `d = 4`, `σ_Φ = 0`; for `d = 5`, `σ_Φ <= 3`; for `d >= 6`, `3d - σ_Φ >= 2d >= 12`. If `c = 1` and `d = 3`, the boundary of `Φ` is a triangle `Δ`, and (2) is negative only for `σ_Φ = 3`. Then `U ≠ R` (if `U = R`, the faces inside along `Δ` touch `t0` and are white), so `U` has a vertex off `Δ`, `Δ` is separating, `t0` is on the other side, and `Δ` has black inner boundary. So (1) holds when there is no such triangle.

Conversely let `Δ` be a separating triangle with black inner boundary and `J` its `I >= 1` interior vertices. For the disk inside `Δ`, Euler and the signed side count give `B = I + 1` black and `W = I` white faces. Every white face with a corner in `J` is inside, so `w(J) <= |J|` and the rank of `⋃_{x ∈ J} C_x` is less than `|J|`. By Rado no rainbow tree exists. ∎

Remark. The obstruction is the same as for a pair (OpenAI Proposition 3.1 in its sharp form). Theorem 3 below shows this is no coincidence.

## 2. Rainbow trees live in 2-factors

For a 2-factor `F` of the incidence graph `B` (equivalently a cover, that is a pair up to orientation), its **deleted-corner map** `u` sends `t ∈ A` to the corner of `t` not joined to `t` in `F`. Let `G_u` be the digraph on `V(T)` with an arc `v -> u(t)` for each of the two used corners `v` of each `t ∈ A`. Each non-root has out-degree 2 in `G_u`; the roots have out-degree 0.

**Lemma 2 (orientation).** Let `F` be a 2-factor and `σ` a choice of one `F`-edge `(x, σ(x))` at each non-root, `σ'(x)` the other one. Then `F_σ` is a spanning tree iff the arcs `x -> u(σ'(x))` contain no directed cycle. In that case `σ'(x)` is the parent of `x` in `F_σ` rooted at the centre of `t0`.

*Proof.* Orient the spokes of `H - σ` as `x -> σ'(x)` at non-roots, `t -> u(t)` at `t ∈ A`, `r -> t0` at roots. A spoke `(t, x)` outside `F` has `x = u(t)`, so every spoke of `H - σ` gets exactly one direction. Every vertex of `H` except the centre of `t0` has out-degree 1, and there are `2n + 3 = |V(H)| - 1` arcs. Such a functional digraph is a spanning in-arborescence iff it has no directed cycle, and its directed cycles alternate `x -> σ'(x) -> u(σ'(x))`. In an in-arborescence every out-arc points to the parent. ∎

**Theorem 3.** (a) Every rainbow tree `σ` lies in exactly one 2-factor of `B`, namely `σ ⊔ par_σ`. (b) Inside a 2-factor `F`, the rainbow trees are the spanning in-forests of `G_u` rooted at the roots (read through `σ ↦ {x -> u(σ'(x))}`), and the good states inside `F` are those in-forests that use exactly one of the two arcs of every face. (c) `G_u` has a directed cycle iff `B` has a 2-factor other than `F`. So if `F` is the only 2-factor, all `2^n` choices are rainbow trees and all `2^{c(F)}` states inside `F` are good.

*Proof.* (a) In `F_σ` the neighbours of a non-root `x` are its faces other than `σ(x)`, and the centre of `t ∈ A` has `3 - c_σ(t)` neighbours, one of them its parent. So `par_σ(x) ≠ σ(x)`, `par_σ(x) ∈ A`, and `t` is the parent of `2 - c_σ(t)` points: `σ ⊔ par_σ` is a 2-factor. If `σ ⊔ σ'` is any 2-factor, Lemma 2 applied to it (with `F_σ` a tree) gives `σ' = par_σ`. (b) is Lemma 2; the arc from `v` through `t` is used iff `σ'(v) = t`, so one arc per face means `c_{σ'} ≡ 1`, equivalently `c_σ ≡ 1`. (c) A directed cycle `v_1 -> ... -> v_k -> v_1` with arcs through `t_1, ..., t_k` has distinct `t_i` (since `u(t_i) = v_{i+1}`), and replacing the edges `(v_i, t_i)` by `(v_{i+1}, t_i)` gives a new 2-factor. Conversely the symmetric difference of two 2-factors splits into closed trails alternating between them, and an edge `(v, t)` outside `F` has `v = u(t)`, so each trail is a closed directed walk of `G_u`, which contains a directed cycle. ∎

**Corollary 4.** Theorem 1 gives a pair whenever no separating triangle has black inner boundary: take a rainbow tree `σ`; then `σ ⊔ par_σ` is a 2-factor, and any orientation of its cycles is a pair.

## 3. The number of good states is even, without signs

Fix a rooted instance with `n >= 1`.

**Lemma 5 (unique exchange).** For a rainbow tree `σ` and `x ∈ X` there is exactly one face `t' ≠ σ(x)` at `x` such that `σ[x := t']` is a rainbow tree. Applying the same exchange again returns `σ`.

*Proof.* `F_σ + (σ(x), x)` has exactly one cycle `Γ`, which passes through `x` and uses exactly two spokes there. Deleting a spoke at `x` leaves a spanning tree iff the spoke is on `Γ`. The second exchange sees the same cycle. ∎

Write `alt_σ(x)` for `t'`. Because the target of an exchange has load at most 1 before the move (a load of 3 would isolate a centre), an exchange out of a face of load 2 never raises the excess.

**The walk.** A walk state is `(σ, t, a)` with `c_σ(t) = 2` and `a` one of the two points of `t` (the arrival); the other is the resident `y`. A step moves `y` to `t' = alt_σ(y)`. If `t'` was empty, the walk stops. Otherwise `t'` had load 1, and the new walk state is `(σ[y := t'], t', y)`. The mirror of `(σ, t, a)` is `(σ, t, y)`.

**Lemma 6.** If `step(S) = S'`, then `step(mirror(S')) = mirror(S)`. In particular `step` is injective.

*Proof.* `S' = (σ', t', y)` with `σ' = σ[y := t']`. In `mirror(S')` the resident is `y`. By Lemma 5 its exchange in `σ'` is `t`, which now has load 1. So the step gives `(σ, t, y) = mirror(S)`. ∎

**Theorem 7.** For `t ∈ A` and a good state `s` (with `σ = s^{-1}`), move `x_0 = s(t)` to `t_1 = alt_σ(x_0)` and run the walk from `(σ[x_0 := t_1], t_1, x_0)`. It stops, at a good state `ι_t(s)`. The map `ι_t` is an involution on good states without fixed points. Hence the number of good states is even.

*Proof.* Every walk state reached has excess 2, with `t` the only empty face, so the walk stops exactly when it moves a point into `t`, and then the excess is 0. It stops: let `S_1` be the first walk state. If `S_1 = step(S)` for some `S`, then by Lemma 6 `step(mirror(S_1)) = mirror(S)` would be a walk state, but the step from `mirror(S_1)` moves `x_0` back into the empty face `t` and stops. So `S_1` has no predecessor. Since `step` is injective on a finite set, the forward orbit of a state without predecessor cannot return to an earlier state, so it ends, at some `S_m` whose step stops. Call the result `s'`.

Run the construction from `s'` at `t`. The point `s'(t)` is the resident `y_m` of `S_m`, and its exchange in `s'^{-1}` returns it to the face of `S_m`, giving `mirror(S_m)`. By Lemma 6 the walk continues `mirror(S_{m-1}), ..., mirror(S_1)`, and the step from `mirror(S_1)` puts `x_0` into `t` and stops at `s`. So `ι_t(s') = s`.

If `s' = s`, the two walks coincide, so `S_i = mirror(S_{m+1-i})` for all `i`. For odd `m` the middle state equals its mirror, impossible since the arrival differs. For even `m`, `S_{m/2}` and `S_{m/2+1}` would have the same tree, but every step changes the tree. ∎

COMPUTED (`code/check_rainbow.py S 6 12`): 5,052 evaluations of `ι_t` over all rootings with `V <= 12`, all as claimed; the number of good states is even in all 208 instances.

Remarks. The walk is not always finite from an arbitrary walk state: periodic orbits exist from `V = 38` on (Fable's examples, replayed here). Theorem 7 avoids them because it starts at a state without predecessor. The involutions `ι_t` do not act transitively on good states (Fable, `V = 13, 14`).

## 4. Density, packing and branchings

Write `e(U)` for the number of edges of `T[U]`, `b(U)` for the number of black faces (including `t0`) with all corners in `U`, `ρ(U) = |U ∩ R|`, `j_t = |V(t) ∩ U|`. Every edge of `T` has exactly one black face, so

    e(U) - b(U) = Σ_{t black} max(0, j_t - 1).                  (3)

**Lemma 8 (density; Opus).** If no separating triangle has black inner boundary, then `e(U) - b(U) + max(0, ρ(U) - 1) <= 2|U| - 2` for every nonempty `U ⊆ V(T)`.

*Proof.* Proof as in `research/2026-11-14_opus_two-tree-packing/PROOFS.md` Lemmas 1.1 and 1.2, checked line by line in `REFEREE-packing.md`. Sketch: reduce to a component `K` of `T[U]` with `p` vertices; `p <= 3` by inspection; for `p >= 4`, Euler and the signed side count give `m - b - (2p - 4) = (1/2) Σ_F (β(F) - d(F) + 4)` over the faces `F` of `K` that are not faces of `T`, with `β` the black-minus-white count inside. Each term is `<= 0` except for a triangular region, which is a separating triangle, contributes 0 when it misses `t0` (by the hypothesis) and at most 1 when it contains `t0`, and that cannot happen when `ρ_K = 3`. ∎

COMPUTED: every nonempty `U`, every rooting, `V <= 14`: holds in all 880 rootings without a black-inner triangle (minimum slack 0), fails in all 308 with one.

**Theorem 9 (two spanning trees; Opus).** Under the hypothesis of Lemma 8, for every map `u` choosing a corner `u(t)` of each `t ∈ A`, the `2n` edges `e(t, v)`, `v ≠ u(t)`, of `W` split into two spanning trees of `W`.

*Proof.* Let `M_u` be the multigraph on `V(H)` with the spokes of `t0` and the spokes `(t, u(t))` doubled and the other spokes single; it has `2(|V(H)| - 1)` edges. For a vertex set `Z` with `U = Z ∩ V(T)` nonempty, the edges inside `Z` are at most `2(|Z| - 1)` for every choice of centres in `Z` iff `Σ_t max(0, μ_t - 2) <= 2|U| - 2`, where `μ_t` is the number of edges of `M_u` from `t` to `U`. For `t0` the term is `2 max(0, ρ(U) - 1)`; for `t ∈ A` it is at most `max(0, j_t - 1)` (cases `j_t = 3, 2, <= 1`). By (3) and Lemma 8 the sum is at most `e(U) - b(U) + max(0, ρ(U) - 1) <= 2|U| - 2`. By Nash-Williams `M_u` is two forests, which by the edge count are spanning trees, each containing one copy of every doubled spoke. Their complements in `H` are the two halves of the support of `u`, and by Fact 0 these are spanning trees of `W`. ∎

**Proposition 10 (Opus).** If `Δ` is a separating triangle with black inner boundary and `u` puts `u(t_i)` on `Δ` for the three inner faces `t_i` along its sides, the conclusion of Theorem 9 fails. (Take `U` the closed outside of `Δ`: the left side of the Nash-Williams sum is `2|U| - 1`.)

**Theorem 11 (`T/R` side; Opus).** Under the same hypothesis, for every `u` the `2n` edges of `T` at `u(t)` inside the faces `t ∈ A` split into two spanning forests of `T`, each with three components and one root in each.

**Theorem 12 (two rainbow trees per cover; Opus).** Under the same hypothesis, every 2-factor `F` of `B` splits as `σ ⊔ σ'` with both `σ` and `σ'` rainbow trees.

*Proof.* By Lemma 2 such a split is a partition of the arcs of `G_u`, with the roots merged into one vertex `ρ`, into two spanning in-arborescences towards `ρ`. By Edmonds (applied to the reversed digraph) these exist iff at least two arcs leave every nonempty `Y ⊆ X`. Each vertex has out-degree 2, so this says at most `2|Y| - 2` arcs lie inside `Y`. A face `t` contributes `[u(t) ∈ Y]·|(V(t) - u(t)) ∩ Y| <= max(0, j_t - 1)` such arcs, and Lemma 8 with `ρ(Y) = 0` and (3) bound the total by `2|Y| - 2`. ∎

COMPUTED for Theorems 9, 11, 12 and Proposition 10: `REFEREE-packing.md` (all rootings `V <= 14`).

## 5. What R plus X would and would not give

Step X is the statement that from every rainbow tree some sequence of exchanges, none of which raises the excess, reaches excess 0. It is a conjecture, checked exhaustively for all rootings with `V <= 17` and for most with `V = 18` by Fable and for `V <= 12` by me. If it were proved, Theorem 1 would supply a rainbow tree whenever no separating triangle has black inner boundary, Step X would carry it to a good state, and Theorem 3 would hand over its partner. That is the key lemma of the OpenAI paper (a good pair exists) with no signed count, no exponential sum and no weight, and with planarity entering through one Euler identity and through whatever the proof of X uses. Barnette's conjecture would then follow by the standard recovery (the selection of a good state is a forest; gluing over separating triangles), which does not use the cancellation either. It would not give a polynomial-time algorithm by itself: X asserts that a non-increasing path exists, the strict version (always a decreasing exchange) is false at `V = 8`, the deterministic surplus walk can cycle from `V = 38` on, and nothing bounds the length of the plateau search. Nor would it give more than one good state; the evenness in Theorem 7 then gives at least two. Finally, nothing in Theorems 9 to 12 brings X closer in a direct way. They hold for every deleted-corner map or every cover, so they cannot tell a cover that contains a good state from one that does not, and such bad covers exist (plantri index 27 at `V = 16`, outer face `{0, 1, 2}`, a cover with one cycle and no good state; `data/BAD_16_16_27.json`). A proof of X must move between covers, which is what the exchanges of the second kind in Theorem 3 do.
