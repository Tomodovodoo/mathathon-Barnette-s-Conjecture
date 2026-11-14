# Proofs: the two-tree packing theorem and what follows from it

Opus 5.5, 2026-11-14. Notation as in `research/BRIEF.md`. All results below are `PROVED-HERE` (tier T2, unreviewed) unless tagged otherwise. Inputs from the literature are tagged `LIT` and were cited from memory; I did not open those sources in this session.

Extra notation.

- `H`: the spoke graph, all black centres including `t0` joined to their corners. `|V(H)| = 2n + 4`, `|E(H)| = 3n + 3`.
- `W`: the white-face graph, the plane dual of `H`. Its vertices are the `n + 1` white faces. The spoke `(t, v)` gives the edge `w(t, v)` joining the white faces across the two sides of `t` at `v`. `W` may have parallel edges (at a vertex of degree 4), never loops.
- For a set `S` of spokes, `S*` is the set of its `W`-edges.
- A **deleted-corner map** is any map `u: A -> V(T)` with `u(t) ∈ V(t)`. Its **support** is `F_u = {(t, v) : t ∈ A, v ∈ V(t), v ≠ u(t)}`, `2n` spokes. The pair supports are the supports of the maps `u` coming from 2-factors of `B` (graph-theory folder, Lemma 3.1): for a pair `(r, s)`, `F_u = r ∪ s` with `u(t)` the third corner. A general `u` need not come from any pair.
- `U ⊆ V(T)`; `e(U)` counts edges of `T[U]`; `b(U)` counts black faces of `T`, including `t0`, with all three corners in `U`; `ρ(U) = |U ∩ R|`.
- "Black inner boundary": a separating triangle whose three faces along its edges, on the side not containing `t0`, are black.

`LIT` inputs.

- (L1) Tree–cotree duality on the sphere: for a connected plane graph `M` and `S ⊆ E(M)`, `M - S` is a spanning tree of `M` iff `S*` is a spanning tree of `M*`. (OpenAI Lemma 2.1 proves one direction; the converse is the same statement applied to `M*`.)
- (L2) Nash-Williams' covering theorem: the edges of a finite multigraph `G` without loops are a union of `k` forests iff `|E(G[Z])| <= k(|Z| - 1)` for every nonempty `Z ⊆ V(G)`. C. St. J. A. Nash-Williams, Decomposition of finite graphs into forests, J. London Math. Soc. 39 (1964) 12.
- (L3) Rado's theorem: in a matroid, a family of `m` sets has an independent transversal iff every subfamily of `j` sets has a union of rank at least `j`. R. Rado, Quart. J. Math. 13 (1942) 83–89.
- (L4) The pair criterion: a pair exists iff no separating triangle has black inner boundary. `PROVED-HERE` in the graph-theory folder (Theorem 2.1) and refereed in `2026-11-14_sol_referee-structure/INTEGRATION.md` §2; also barnette_trees Thm 1.2. I use only the direction "pair ⇒ no black-inner triangle" (a short Hall count, recalled in Remark 2.4) and the identity of Lemma 1.1, whose proof I repeat.

---

## 1. A density lemma for all vertex sets

**Lemma 1.1** (Euler identity; graph-theory PROOFS Lemma 2.2, refereed INTEGRATION §1). Let `K` be a connected induced subgraph of `T` with `p >= 3` vertices and `m` edges. Call a face of the plane graph `K` *actual* if it is a face of `T` and a *region* otherwise. Let `b` count the actual black faces of `K`, and for each region `F` let `d(F)` be its boundary length in edge sides and `β(F)` the number of black minus white faces of `T` inside it. Then

    m - b - (2p - 4) = (1/2) Σ_F ( β(F) - d(F) + 4 ).

Moreover `3β(F)` is the sum, over the boundary sides of `F`, of `+1` or `-1` according as the face of `T` on the region side is black or white. Hence `β(F) <= d(F) - 4` when `d(F) >= 4`, and `β(F) = ±1` when `d(F) = 3`, with `+1` iff all three region-side faces are black.

*Proof.* Let `w` count the actual white faces and `q` the regions. Euler: `p - m + b + w + q = 2`. Sides: `2m = 3b + 3w + Σ d(F)`. Eliminating `q` gives `m - b - 2p + 4 = (1/2)(w - b - Σ (d(F) - 4))`. The faces of `T` are the actual faces of `K` and the faces inside regions, and `T` has equally many black and white faces, so `w - b = Σ β(F)`. For the side count, give each face of `T` in the region `+3` or `-3` and distribute it over its sides; interior sides cancel. Then `3β` has the parity of `d` and `|3β| <= d`, which gives `β = 0` for `d = 4`, `|β| <= 1` for `d = 5` and `|β| <= d/3 <= d - 4` for `d >= 6`. ∎

**Lemma 1.2** (density for every vertex set). Suppose no separating triangle has black inner boundary. Then for every nonempty `U ⊆ V(T)`

    e(U) - b(U) + max(0, ρ(U) - 1) <= 2|U| - 2.                 (1.2)

For `U ⊇ R` this is the paper's inequality (3.2), `e(U) - b(U) <= 2|U| - 4`.

*Proof.* Every edge of `T[U]` and every black face with its corners in `U` lies in one component of `T[U]`, and the roots in `U` lie in one component because they are pairwise adjacent. It therefore suffices to prove, for each component `K` with `p` vertices, `m` edges, `b` black faces of `T` with corners in `K`, and `ρ_K = |R ∩ V(K)|`,

    m - b <= 2p - 2 - max(0, ρ_K - 1),                         (1.3)

and then to sum, using `Σ_K (2p_K - 2) <= 2|U| - 2`.

- `p = 1`: `0 <= 0`.
- `p = 2`: `m = 1`, `b = 0`, `ρ_K <= 2`: `1 <= 2 - max(0, ρ_K - 1)`.
- `p = 3`: `K` is a path (`m = 2`, `b = 0`, and `ρ_K <= 2` since three roots would span a triangle), or a triangle. A triangle that is a black face has `m - b = 2 <= 4 - 2`. Any other triangle has `m - b = 3` and `ρ_K <= 2`, because the triangle on the three roots is `t0`, a black face.
- `p >= 4`: apply Lemma 1.1. A region with `d >= 4` contributes at most 0. A region with `d = 3` is bounded by a 3-cycle (a closed walk of length 3 in a simple graph). It is not a face of `T`, so it contains a vertex of `T`: otherwise every edge of `T` inside it would join two of its three corners, and in a simple graph those are its sides. `K` has a vertex on the other side, since `p >= 4`. So the 3-cycle is a separating triangle. If the region does not contain `t0`, it is the inner side; by hypothesis `β = -1` and the contribution is 0. At most one region contains `t0`, and it contributes at most `(1/2)(1 + 1) = 1`. Hence `m - b <= 2p - 4 + ε`, where `ε = 1` if `t0` lies in a triangular region of `K` and `ε = 0` otherwise. If `ρ_K = 3`, `t0` is an actual face of `K`, so `ε = 0` and `m - b <= 2p - 4`, which is (1.3). If `ρ_K <= 2`, `m - b <= 2p - 3 <= 2p - 2 - max(0, ρ_K - 1)`. ∎

**Remark 1.3.** Lemma 1.2 is the only place where planarity, the colouring and the hypothesis enter. The case `ρ_K = 2`, `ε = 1` really occurs: `t0` sits in a separating triangle through the root edge, whose `t0`-side faces are black. The bound (1.3) is then tight.

---

## 2. The packing theorem

**Theorem 2.1** (two-tree packing). Suppose no separating triangle has black inner boundary, equivalently (L4) a pair exists. Then for **every** deleted-corner map `u`, the `2n` edges `F_u*` of `W` split into two spanning trees of `W`. In particular, for every pair `(r, s)`, the `W`-edges of `r ∪ s` split into two spanning trees. This is the half-pair packing conjecture of `2026-11-14_sol_route-probabilistic` (ROUTES.md, "Scope of the fractional conjecture").

*Proof.* Let `M_u` be the multigraph on `V(H)` that contains each spoke of `t0` and each spoke `(t, u(t))`, `t ∈ A`, twice (as two parallel copies), and each spoke of `F_u` once. It has `2(n + 3) + 2n = 2(|V(H)| - 1)` edges and no loops.

*Step 1: `M_u` is a union of two forests.* By (L2) we must show `|M_u[Z]| <= 2(|Z| - 1)` for nonempty `Z ⊆ V(H)`. Write `U = Z ∩ V(T)` and `C` for the centres in `Z`. If `U = ∅` there are no edges and the bound holds. Otherwise `|M_u[Z]| = Σ_{t ∈ C} μ_t(U)`, where `μ_t(U)` is the number of edges of `M_u` from the centre of `t` to `U`. The bound for all `C` at once is equivalent to

    Σ_{all black t} max(0, μ_t(U) - 2) <= 2|U| - 2.            (2.2)

For `t0`, `μ = 2ρ(U)`, so its term is `2 max(0, ρ(U) - 1)`. For `t ∈ A` with `j = |V(t) ∩ U|` corners in `U`:

| `j` | `μ_t(U)` | term | `max(0, j - 1)` |
| --- | --- | --- | --- |
| 3 | `2 + 1 + 1 = 4` | 2 | 2 |
| 2, `u(t) ∈ U` | `2 + 1 = 3` | 1 | 1 |
| 2, `u(t) ∉ U` | `1 + 1 = 2` | 0 | 1 |
| 0 or 1 | `<= 2` | 0 | 0 |

So each term is at most the shortfall `max(0, j - 1)`, which is the number of edges of `t` inside `U` minus one if `j = 3`. Every edge of `T` has exactly one black face. Summing over `A`, the left side of (2.2) is at most

    Σ_{t ∈ A} max(0, j_t - 1) + 2 max(0, ρ - 1) = e(U) - b(U) + max(0, ρ - 1),

because `t0` itself contributes `max(0, ρ - 1)` to `e(U) - b(U)`. Lemma 1.2 bounds this by `2|U| - 2`.

*Step 2: the two forests are spanning trees of `H` that contain every doubled spoke.* Each forest has at most `|V(H)| - 1` edges, and together they have `2(|V(H)| - 1)`, so both are spanning trees `τ_1, τ_2`. A forest contains at most one of two parallel copies, so each `τ_i` contains every doubled spoke once, and `F_u` is split as `F_u = (F_u ∩ τ_1) ⊔ (F_u ∩ τ_2)`.

*Step 3: duality.* `E(H) - τ_1 = F_u ∩ τ_2` and `E(H) - τ_2 = F_u ∩ τ_1`. By (L1) the duals of both are spanning trees of `W`. ∎

**Proposition 2.2** (the converse inside the proof). For any deleted-corner map `u`, without hypothesis on `T`: `F_u*` splits into two spanning trees of `W` iff `M_u` is a union of two spanning trees of `H` iff (2.2) holds for every nonempty `U`.

*Proof.* If `F_u* = B_1 ⊔ B_2` with `B_i` spanning trees of `W`, then by (L1) `τ_i = E(H) - B_i` (with `B_i` read as spokes) are spanning trees of `H`, and as multisets `τ_1 + τ_2 = M_u`. The rest is Steps 1–3 and (L2). ∎

**Proposition 2.3** (the hypothesis is needed for arbitrary `u`). Let `Δ` be a separating triangle with black inner boundary, and let `t_1, t_2, t_3` be the three inner black faces along its sides. Every deleted-corner map `u` with `u(t_i) ∈ V(Δ)` for `i = 1, 2, 3` fails: `F_u*` does not split into two spanning trees of `W`.

*Proof.* Let `U` be the set of vertices not strictly inside `Δ`. Then `U ⊇ R`, and by Lemma 1.1 (`T[U]` is connected with one region, `d = 3`, `β = 1`) `e(U) - b(U) = 2|U| - 3`. The black faces with `j = 3` are the actual black faces of `T[U]`; the faces with `j = 2` are exactly `t_1, t_2, t_3` (a face with two corners on `Δ` contains the side between them, and simplicity rules out other edges between them); all other faces have `j <= 1`. With `u(t_i) ∈ U`, every term of (2.2) equals its shortfall, so the left side of (2.2) equals `e(U) - b(U) + 2·2 - 2 = 2|U| - 1 > 2|U| - 2`. By Proposition 2.2, `F_u*` does not split. ∎

Remark 2.4 shows that no pair exists when such a `Δ` is present, so Proposition 2.3 does not contradict the conjecture as stated, which quantifies over pairs. It shows that the conjecture is exactly as strong as "no black-inner separating triangle" once one asks it for all deleted-corner maps.

**Remark 2.4** (no pair under a black-inner triangle; recalled). Let `I >= 1` count the vertices strictly inside such a `Δ`. Lemma 1.1 on the disk gives `B = I + 1` black faces inside. Take `S` = the strict interior in the Hall condition `Σ_{t ∈ A} min(2, |V(t) ∩ S|) >= 2|S|`. The three faces `t_i` have one corner in `S`, the other `I - 2` inner faces have two or three, and outer faces none. The sum is `3 + 2(I - 2) = 2I - 1 < 2I`. So `B` has no 2-factor and no pair exists.

**Theorem 2.5** (fractional form). Under the hypothesis of Theorem 2.1, every `y` on the spokes with `y = 0` on the spokes of `t0`, `Σ_{v ∈ V(t)} y(t, v) = 1` and `0 <= y(t, v) <= 1/2` for `t ∈ A`, lies in the spanning-tree polytope of `W` (read through `*`).

*Proof.* For one face, `{y ∈ [0, 1/2]^3 : Σ y = 1}` is the triangle with vertices the three permutations of `(1/2, 1/2, 0)`. The product over `t ∈ A` is therefore the convex hull of the points `(1/2) 1_{F_u}` over all deleted-corner maps `u`. By Theorem 2.1 each such point is the average of two spanning trees. ∎

**Corollary 2.6** (three trees). Under the same hypothesis, the `3n` edges of `W` other than the triangle `Δ_{t0}` of `t0` are a union of three spanning trees of `W`.

*Proof.* The point `y = 1/3` on every spoke of every `t ∈ A` satisfies Theorem 2.5, so it is a convex combination of spanning trees of `W`. Each spanning tree has at most `|S| - 1` edges inside any nonempty set `S` of white faces, so `y(E(W[S])) <= |S| - 1`, that is, `|E(W[S]) - Δ_{t0}| <= 3(|S| - 1)`. By (L2) with `k = 3` these edges are three forests. They have `3n = 3(|V(W)| - 1)` edges in total, so the forests are spanning trees. ∎

This is a Schnyder-type statement for the white-face graph: `T` minus its outer edges is three trees (Schnyder), and so is `W` minus the outer triangle. `COMPUTED` (`code/rainbow.py`, all rootings `V <= 17`): it also holds in every rooted instance **without** a pair, so the hypothesis is not needed here; I have no proof of that.

**Theorem 2.7** (the same packing on the triangulation side). Under the hypothesis of Theorem 2.1, let `u` be any deleted-corner map and `D_u` the set of edges of `T` opposite `u(t)`, `t ∈ A`. Then the `2n` edges of `E(T) - E(t0) - D_u` split into two spanning trees of `T/R`, the multigraph obtained by identifying the three roots to one vertex `ρ`. Equivalently they split into two spanning forests of `T`, each with three components and one root in each. For a pair, `E(T) - E(t0) - D(r,s) = Q_r ⊔ Q_s` (Proposition 4.1), so `Q_r ∪ Q_s` always re-splits into two root-separating spanning forests.

*Proof.* `T/R` has `n + 1` vertices and no loops (the edges between roots are the edges of `t0`, which are removed). By (L2) it suffices to bound the number of kept edges inside a nonempty vertex set `S` of `T/R` by `2(|S| - 1)`. A black face `t ∈ A` with `j` corners in the corresponding vertex set of `T` keeps at most `max(0, j - 1)` of its edges there (all three corners: two kept edges; two corners: at most the one edge). If `ρ ∉ S`, then `S ⊆ X`, the count is at most `e(S) - b(S) <= 2|S| - 2` by Lemma 1.2 with `ρ(S) = 0`. If `ρ ∈ S`, put `U = (S - ρ) ∪ R`, so `|U| = |S| + 2`. The count is at most `Σ_{t ∈ A} max(0, j_t - 1) = e(U) - b(U) - 2 <= 2|U| - 6 = 2|S| - 2`, by Lemma 1.2 with `ρ(U) = 3`. The two forests have `2n = 2(|V(T/R)| - 1)` edges, so they are spanning trees. The translation to `T` is the usual one: a spanning tree of `T/R` lifts to a spanning forest of `T` whose components each contain exactly one root. ∎

`COMPUTED` (`code/tside.py 6 16 5 7`): every pair support and 25,440 random maps in instances with a pair split; random maps fail only in instances without a pair, at the same triangles as in Proposition 2.3 (the failing count is again `2|U| - 1` at the outside of a black-inner triangle when all three `u(t_i)` lie on it).

The two-sided relation between Theorems 2.1 and 2.7: a set `σ` of spokes with exactly one spoke per `t ∈ A` (a face-rainbow set) has `σ*` a spanning tree of `W` iff `Q_σ`, the opposite edges, is a spanning tree of `T/R` (graph-theory PROOFS Lemma 1.1, with the referee's caveat that this identification is valid only for face-rainbow sets). The two trees produced by Theorem 2.1 or by Theorem 2.7 are in general not face-rainbow, so the two theorems are separate statements with the same proof skeleton. A split of `F_u` into two **face-rainbow** trees would be one statement for both sides; that is Conjecture P2 in `PACKING.md`.

---

## 3. Consequences for the three-matroid problem

Recall (graph-theory PROOFS Lemma 1.1, refereed INTEGRATION §7): a tree matching is a common basis of `M(W)` (read through `*`), the face partition `P_c` (one spoke per `t ∈ A`, none at `t0`) and the point partition `P_v` (one spoke per nonroot, none at a root).

**Corollary 3.1** (the natural LP is feasible, without signs). If a pair `(r, s)` exists, `x = (1/2)(1_r + 1_s)` lies in the spanning-tree polytope of `W`, has face sums 1 on `A` and 0 on `t0`, and point sums 1 on `X` and 0 on `R`. So it lies in the intersection of the three base polytopes.

*Proof.* Theorem 2.1 for the pair support; the two sum conditions hold because `r` and `s` are states. ∎

This is fractional only. The same LP has non-integral vertices (graph-theory ROUTES M1–M4, half-integral vertex at `V = 13`), and a fixed pair support need not contain a tree matching (the `V = 16` bad cover; see `REFEREE.md`).

**Corollary 3.2** (both one-sided problems are solvable inside every pair support). Let `(r, s)` be a pair with support `F = r ∪ s`.

(a) There is `σ: A -> V(T)` with `σ(t) ∈ {r(t), s(t)}` for every `t ∈ A` such that `H - σ` is a spanning tree (a face-rainbow tree inside `F`).

(b) There is `π: X -> A` with `π(x) ∈ {r^{-1}(x), s^{-1}(x)}` for every `x ∈ X` such that `H - {(π(x), x) : x ∈ X}` is a spanning tree (a point-rainbow tree inside `F`).

*Proof.* `F*` is a union of two forests (Theorem 2.1), so every `Y ⊆ F*` has `|Y| <= 2 rank(Y)`. For (a) the blocks are the cherries `{(t, r(t)), (t, s(t))}`, for (b) the point pairs `{(r^{-1}(x), x), (s^{-1}(x), x)}`. In both cases they are `n` disjoint 2-sets partitioning `F`, so a subfamily of `j` blocks has union of size `2j` and rank at least `j`. Rado (L3) gives an independent transversal with `n` elements, a spanning tree of `W`. Translate by (L1). ∎

Part (a) applies verbatim to every deleted-corner map `u`, with blocks `V(t) - u(t)`. Part (b) combined with the fable topology referee's Theorem S (each point-rainbow tree lies in exactly one 2-factor of `B`) says that the map from point-rainbow trees to 2-factors is **onto**: every 2-factor carries a point-rainbow tree. Fable's Theorem R (a rainbow tree exists iff no black-inner triangle) follows from Corollary 3.2(b) in the direction "pair ⇒ rainbow tree", by a route that uses Rado once instead of a Rado computation over all connected `J`.

**Theorem 3.3** (a 2-factor splits into two point-rainbow trees). Let `F` be a pair support (a 2-factor of `B`) with deleted-corner map `u`. Then `F = σ ⊔ σ'`, where `σ` and `σ'` each contain exactly one spoke at every nonroot and `σ*`, `σ'*` are both spanning trees of `W`. Equivalently (by (L1)), `H - σ` and `H - σ'` are both spanning trees.

*Proof.* Every nonroot `x` lies in exactly two spokes of `F`, at faces `t_1(x), t_2(x)`. Let `G_u` be the digraph on `V(T)` with one arc `x -> u(t)` for every spoke `(t, x) ∈ F` (the digraph of the fable topology referee's Theorem S). Every nonroot has out-degree 2 and the roots have out-degree 0, because roots are never used by a 2-factor.

*Step 1 (a choice is a tree iff its arcs are acyclic).* Let `σ` choose one spoke `(σ(x), x)` at every nonroot and let `σ'(x)` be the other face. In `H - σ` orient `x -> σ'(x)` for nonroots, `t -> u(t)` for `t ∈ A`, and `r -> t0` for roots. Every spoke of `H - σ` gets exactly one orientation: at `t ∈ A` the kept spokes are `(t, u(t))` and the spokes `(t, v)` with `σ'(v) = t`; a root `r` meets `t0` and the faces with `u(t) = r`. Every vertex of `H` except the centre of `t0` has out-degree 1, and `|E(H - σ)| = 2n + 3 = |V(H)| - 1`. So `H - σ` is a spanning tree iff this functional digraph has no directed cycle, iff the map `x -> u(σ'(x))` has no cycle on `X`, iff the arcs `{x -> u(σ'(x))}` of `G_u` form an in-forest whose sinks are roots. (This is the fable referee's Theorem S(3); the proof is repeated so that this section is self-contained.)

*Step 2 (Edmonds).* Merge the roots of `G_u` into one vertex `ρ`. By Step 1, a split `F = σ ⊔ σ'` into two point-rainbow trees is exactly a partition of the arcs of `G_u` into two spanning in-arborescences towards `ρ`. Edmonds' branching theorem (`LIT`: J. Edmonds, Edge-disjoint branchings, in Combinatorial Algorithms, Algorithmics Press 1973, 91–96; cited from memory), applied to the reversed digraph, says such a pair of arc-disjoint in-arborescences exists iff every nonempty `Y ⊆ X` has at least two arcs leaving it. Two arc-disjoint spanning in-arborescences have `2n` arcs, all of `G_u`, so they partition it. Since every vertex of `Y` has out-degree 2, the condition reads: at most `2|Y| - 2` arcs have both ends in `Y`.

*Step 3 (count).* A face `t ∈ A` with `j` corners in `Y` contributes `[u(t) ∈ Y] · |(V(t) - u(t)) ∩ Y|` arcs inside `Y`: 2 if `j = 3`, 1 if `j = 2` and `u(t) ∈ Y`, 0 otherwise. This is at most `max(0, j - 1)`, so the number of arcs inside `Y` is at most `e(Y) - b(Y) <= 2|Y| - 2` by Lemma 1.2 (with `ρ(Y) = 0`). ∎

This is the same table as in Step 1 of Theorem 2.1, so the two proofs are one count read in two ways. Theorem 3.3 is stronger than Corollary 3.2(b): the second half is again a point-rainbow tree. `COMPUTED` agreement: `code/rainbow.py`, all 14,881 pair supports of all rootings with `V <= 17`.

**Conjecture 3.4** (P2, the face side). Every pair support `F` splits into two face-rainbow trees: `F = σ ⊔ σ'` with `σ(t), σ'(t)` the two used corners of `t` and `σ*`, `σ'*` spanning trees of `W`. Equivalently (Lemma 1.1 of the graph-theory folder), `Q_r ∪ Q_s` splits into two spanning trees of `T/R` each taking one edge of every bounded black face. `COMPUTED`: true for all 14,881 pair supports with `V <= 17` (`code/rainbow.py`). The branching argument does not transfer: the face-rainbow constraint pairs the two arcs entering `u(t)` from one face, not the two arcs leaving one vertex. A split that is rainbow for faces and points at once is a pair `(r, s)` with both `r` and `s` tree matchings; that fails for some supports (239 of 9,290 at `V = 17`).

**What is left.** A tree matching inside `F` is a common transversal of both block systems that is a spanning tree. The cherries and the point pairs together form the alternating cycles of the 2-factor, and a common transversal is one of the `2^c` alternating halves, a state of the `D`-group. Two-matroid theory gives each one-sided transversal; nothing gives the alternating one, and for a fixed `F` it can fail. So the remaining content of the key lemma is: **some 2-factor has an alternating half that is a spanning tree of `W`.** No statement about a single `F` can prove this, and any proof must move between 2-factors.

---

## 4. A pair as a decomposition of the edges of `T`

**Proposition 4.1.** For a pair `(r, s)` with third corner `u(t)`, the three edges of each `t ∈ A` are: the edge opposite `s(t)` (in `Q_s`), the edge opposite `r(t)` (in `Q_r`), and the edge opposite `u(t)`, which is `r(t)s(t)` (in `D`). Hence `E(T) - E(t0) = Q_r ⊔ Q_s ⊔ D`, each part containing exactly one edge of every bounded black face.

*Proof.* `r(t)`, `s(t)`, `u(t)` are the three corners; the edge opposite a corner is the side joining the other two. Each edge of `T` has exactly one black face, and the edges of `t0` belong to `t0`. ∎

**Proposition 4.2** (a pair is a 3-orientation). Orient, in each `t ∈ A`, the three edges `r(t) -> s(t)`, `r(t) -> u(t)`, `s(t) -> u(t)`. Every nonroot gets out-degree 3 (once as `r(t)`, contributing 2, once as `s(t')`, contributing 1), every root out-degree 0, and every bounded black triangle is transitively oriented with sink `u(t)`. Conversely, every orientation of `E(T) - E(t0)` with out-degree 3 at nonroots and 0 at roots in which every bounded black triangle is transitive, and no nonroot is the middle vertex of three black triangles, arises from exactly one ordered pair (source = `r(t)`, middle = `s(t)`).

*Proof.* The out-degree of `x` is `2·#{t : x source in t} + #{t : x middle in t}`, since every edge lies in exactly one black face. Setting this to 3 gives `(1, 1)` or `(0, 3)`; excluding `(0, 3)` makes "source" and "middle" two disjoint bijections `A -> X`. At a root, out-degree 0 forces the root to be the sink of each bounded face containing it. ∎

`LIT` (cited from memory, not opened): out-degree-3 orientations of a triangulation minus its outer edges are in bijection with Schnyder woods (H. de Fraysseix and P. Ossona de Mendez, On topological aspects of orientations, Discrete Math. 229 (2001) 57–72; W. Schnyder, Planar graphs and poset dimension, Order 5 (1989) 323–343). So every pair determines a Schnyder wood of `T` rooted at `t0`, whose three colour classes are trees. Those colour classes are cut by the cyclic order of out-edges at each vertex, not by black faces, and they are not `Q_r, Q_s, D` in general. `HUNCH`: a pair whose `Q_s` is a Schnyder colour class would be a tree pair; I did not test this.

---

## 5. Adversarial re-reading

I re-read the proofs above against the following failure modes.

1. *Parallel edges and loops.* `W` can have parallel edges (vertices of degree 4); (L2) and (L1) hold for multigraphs. `W` has no loops: the two white faces across two sides of `t` at `v` coincide only if a white face has the same three corners as `t`, impossible in a simple triangulation with more than four vertices; the smallest Eulerian triangulation is the octahedron, `V = 6`. `M_u` has no loops.
2. *Roots in bounded faces.* A bounded face has at most one root (the edge between two roots lies in `t0`). The proof of Theorem 2.1 never needs `u(t)` to be the root; the table in Step 1 is valid for any `u`.
3. *Component bookkeeping.* A black face with all corners in `U` lies in one component (its corners are pairwise adjacent), and is counted in that component's `b`. A black face with `j = 2` corners in `U` contributes its one edge to that component's `m` and nothing to `b`. So `e(U) - b(U) = Σ_K (m_K - b_K)`.
4. *Regions containing other components.* Lemma 1.1 counts every face of `T` inside a region, including faces of other components; the identity and the side count are unaffected.
5. *The case where `U` contains no root.* Then `ρ = 0`, Lemma 1.2 gives `e - b <= 2|U| - 2`, and the left side of (2.2) has no `t0` term. Fine.
6. *Equality cases.* The bound is tight in the instances computed (single-vertex `U` and `U = V(T)` give equality: for `U = V(T)`, `e - b + 2 = 3(n+1) - (n+1) + 2 = 2(n+3) - 2`). Tightness at `U = V(T)` is forced by the edge count and is not a flaw.
7. *Converse (Prop. 2.2) uses that `B_i` read as spokes complement to trees in `H`.* That is (L1) applied to `W` and its dual `H`.
