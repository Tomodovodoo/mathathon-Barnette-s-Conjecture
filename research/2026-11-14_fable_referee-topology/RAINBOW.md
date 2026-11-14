# The rainbow route: Step R proved, Step X tested, one strengthening refuted

Fable 5.2, 2026-11-14. Notation as in `research/BRIEF.md`. All code is mine (`code/etri.py`, `code/rainbow.py`, `code/exp_*.py`), commands in `code/README.md`. "All rootings" means every face of every plantri Eulerian triangulation of that order, taken as outer face and coloured black.

Summary of status.

| Statement | Status |
| --- | --- |
| Lemma X1: each point of a rainbow tree has exactly one exchange | PROVED-HERE |
| Theorem R: a point-rainbow tree exists iff no separating triangle has black inner boundary | PROVED-HERE, COMPUTED on 7,868 rooted instances |
| Lemma R2: a face-rainbow tree always exists | PROVED-HERE |
| Lemma X2: surplus inside the fundamental cycle of an exchange | PROVED-HERE, COMPUTED on 102,976 moves |
| Lemma X3, Corollary X4: the surplus walk is reversible; `n` fixed-point-free involutions on tree matchings | PROVED-HERE, COMPUTED |
| Theorem S: every rainbow tree lies in exactly one 2-factor of `B`, as a spanning in-forest of a 2-out digraph. So Theorem R reproves the existence of a pair | PROVED-HERE, COMPUTED |
| Conjecture X: non-increasing exchanges reach a tree matching from every rainbow tree | CONJECTURE. True for every rooted instance with `V <= 17` (exhaustive, with Proposition U for the instances with one 2-factor). No counterexample in sampled runs to `V = 120` |
| X′: the surplus walk is never periodic | REFUTED at `V = 38`. True for all rootings with `V <= 15` |
| Strict descent: some exchange always lowers the excess | REFUTED at `V = 8` |
| M: the set of load vectors is M-convex | REFUTED at `V = 12`. True when `B` has one 2-factor |
| "Mean load is 1 at every face" | REFUTED at `V = 12`. True when `B` has one 2-factor |

## 1. Definitions

**The white-face graph `H*`.** Its vertices are the `n + 1` white faces of `T`. Every spoke `(t, v)` of `H` (black face `t`, corner `v`) gives one edge `e(t, v)`, joining the two white faces that lie across the two sides of `t` at `v`. So `H*` has `3n + 3` edges and is the plane dual of `H`. Two partitions of its edge set matter.

- The **point class** `C_v = { e(t, v) : t at v }`. It is the closed walk through the `d_v` white faces around `v`, a cycle of length `d_v` (two parallel edges if `d_v = 2`).
- The **face class** `Δ_t = { e(t, v) : v corner of t }`, a triangle on the three white neighbours of `t`. They are distinct, because two sides of `t` on the same white face would force a vertex of degree 2.

By tree and cotree duality (OpenAI Lemma 2.1 and its converse), for a set `S` of spokes, `H - S` is a spanning tree iff the edges `e(t, v)`, `(t, v) ∈ S`, form a spanning tree of `H*`.

**Rainbow tree.** A *point-rainbow spanning tree*, from now on a *rainbow tree*, is a map `σ: X -> A` with `x` a corner of `σ(x)`, such that the `n` edges `e(σ(x), x)` form a spanning tree of `H*`. In words, one spoke is deleted at every non-root, none at a root, and what remains of `H` is a spanning tree `F_σ`. The value `t0` cannot occur, because `t0` has only root corners.

**Load and excess.** `c_σ(t) = |σ^{-1}(t)|` for `t ∈ A`. The centre of `t` keeps `3 - c_σ(t)` spokes in the tree `F_σ`, so `c_σ(t) ∈ {0, 1, 2}`, and `Σ_t c_σ(t) = n = |A|`. The *excess* is

    exc(σ) = Σ_{t ∈ A} |c_σ(t) - 1| = 2 · #{t : c_σ(t) = 2} = 2 · #{t : c_σ(t) = 0}.

A rainbow tree of excess 0 is a bijection `X -> A`, and its inverse is a state `s` with `H - s` a tree. So **tree matchings are exactly the rainbow trees of excess 0**.

**Lemma X1 (unique exchange) [PROVED-HERE].** Let `σ` be a rainbow tree and `x ∈ X`. There is exactly one black face `t' ≠ σ(x)` at `x` such that redefining `σ(x) := t'` gives a rainbow tree.

*Proof.* Add the missing spoke `(σ(x), x)` to `F_σ`. The result has one cycle `Γ`. It is a simple cycle through `x`, so it uses exactly two spokes at `x`: the added one and one other, `(t', x)`. Removing a spoke at `x` restores a spanning tree iff that spoke lies on `Γ`. ∎

Call this the *move at `x`* and write `alt_σ(x) = t'`. The move at `x` applied twice is the identity, since the cycle `Γ` is the same both times. So the rainbow trees of an instance form an `n`-regular graph, the *move graph*. A move from `t` to `t'` changes the excess by

| `(c(t), c(t'))` before the move | change |
| --- | --- |
| `(2, 0)` | `-2` |
| `(2, 1)` or `(1, 0)` | `0` |
| `(1, 1)` | `+2` |

The case `c(t') = 2` cannot occur, because the result is a tree.

COMPUTED (`exp_rainbow.py traps`): for all 34,799,040 rainbow trees of all 5,088 rooted instances with `V <= 16` that have one, every point has exactly one exchange, and the move graph is connected in every instance.

## 2. Step R

**Theorem R [PROVED-HERE].** A rooted Eulerian triangulation has a rainbow tree if and only if no separating triangle has black inner boundary. More precisely, let `J ⊆ X` be non-empty with `T[J]` connected, `U = V(T) \ J`, `c` the number of components of `T[U]`, `Φ` the face of the plane graph `T[U]` that contains `J`, `d` its boundary length counted by edge sides, and `σ_Φ` the sum over those sides of `+1` or `-1` according as the face of `T` on the `Φ` side is black or white. Let `w(J)` be the number of white faces with a corner in `J`. Then

    w(J) - |J| - 1 = (c - 1) + (3d - σ_Φ - 12) / 6.                      (R)

The right side is non-negative except when `c = 1`, `d = 3`, `σ_Φ = 3`, where it is `-1`, and that case is exactly a separating triangle with black inner boundary whose interior is `J`.

*Proof.*

*Step 1, Rado.* A rainbow tree is an independent transversal of the family `(C_x)_{x ∈ X}` in the cycle matroid of `H*`. That matroid has rank `n`, the family has `n` members, and they are pairwise disjoint. Rado's theorem says that an independent transversal exists iff `rank(⋃_{x ∈ J} C_x) >= |J|` for every `J ⊆ X`. (R. Rado, A theorem on independence relations, Quart. J. Math. Oxford 13 (1942) 83-89. Cited from memory, not opened in this session.)

The rank of an edge set is the number of vertices it touches minus the number of its components. `C_x` touches the white faces at `x` and is connected. `C_x` and `C_y` share a white face iff `x` and `y` are corners of one white face iff `xy` is an edge of `T`, because every edge lies on exactly one white face. So the components of `⋃_{x ∈ J} C_x` correspond to the components of `T[J]`, and a white face cannot touch two of them. Rado's condition therefore reads

    w(J) >= |J| + 1        for every non-empty J ⊆ X with T[J] connected.       (R1)

*Step 2, the faces of `T[U]`.* Let `J` be as in (R1). `J` is connected and disjoint from `T[U]`, so it lies in one face `Φ` of `T[U]`. Any other face of `T[U]` contains no vertex of `T`. It contains no edge of `T` either, since such an edge would join two vertices of `U` and `T[U]` is induced. So it is a face of `T`. Conversely a face of `T` with all corners in `U` is a face of `T[U]` different from `Φ`. Let `b_U, w_U` count the black and white faces of `T` with all corners in `U`, and put `p = |U|`, `m = e(U)`.

*Step 3, three counts.* Euler's formula for a plane graph with `c` components, the count of edge sides, and the signed side count inside `Φ` give

    p - m + (b_U + w_U + 1) = 1 + c,
    2m = 3(b_U + w_U) + d,
    3( (n + 1 - b_U) - (n + 1 - w_U) ) = σ_Φ.

In the third line, the faces of `T` inside `Φ` are the `n + 1 - b_U` black and `n + 1 - w_U` white faces not counted before. A side interior to `Φ` is shared by a black and a white face and cancels. A bridge of `T[U]` with `Φ` on both sides contributes `+1` and `-1`. Solving,

    w_U = p - c - d/2 + σ_Φ / 6.

*Step 4.* The white faces without a corner in `J` are those counted by `w_U`, so `w(J) = n + 1 - w_U`, and `|J| = n + 3 - p`. Substituting gives (R).

*Step 5, the sign.* `σ_Φ` is a multiple of 3, has the parity of `d`, and `|σ_Φ| <= d`. Also `d >= 3`: the component of `T[U]` containing the roots contains the triangle `t0`, it borders `Φ` (otherwise this component and its incident faces, all of them faces of `T`, would form a set that is open and closed in the sphere, and `J` would be empty), and a facial walk of a simple graph that is not a tree has length at least 3.

- If `c >= 2`, the right side of (R) is at least `1 + (2d - 12)/6 = (d - 3)/3 >= 0`.
- If `c = 1` and `d = 4`, then `σ_Φ = 0` and (R) gives 0. If `d = 5`, `σ_Φ = ±3` and (R) gives at least 0. If `d >= 6`, `3d - σ_Φ >= 2d >= 12`.
- If `c = 1` and `d = 3`, then `σ_Φ = ±3` and (R) gives `0` or `-1`. The value `-1` needs `σ_Φ = 3`. The boundary of `Φ` is a 3-cycle `Δ` of `T`, and `Φ`, which contains `J`, is one of its sides. If `U = R` then `Δ` is the boundary of `t0` and the three faces along it inside `Φ` are white, so `σ_Φ = -3`. Otherwise `U` has a vertex off `Δ`, necessarily on the other side, so `Δ` is a separating triangle. The face `t0` is a face of `T[U]` other than `Φ`, so `Φ` is the side away from `t0`, and `σ_Φ = 3` says that its inner boundary is black.

So (R1) holds for all `J` when no separating triangle has black inner boundary.

*Step 6, the converse.* Let `Δ` be a separating triangle with black inner boundary and `J` the set of its `I` strictly interior vertices. The disk count gives `I` white faces inside (barnette_trees §3). Every white face with a corner in `J` lies inside. So `w(J) <= I = |J|`, and the rank of `⋃_{x ∈ J} C_x` is at most `|J| - 1`. Rado's condition fails. ∎

**Remarks.**

1. This is the same obstruction as for a pair (barnette_trees Thm 1.2 (ii) ⇔ (iii)), and the proof has the same shape as OpenAI Prop. 3.1: a transversal theorem plus one Euler count. Identity (R) plays the role of the Euler identity (2.2) in `research/2026-11-14_opus_route-graph-theory/PROOFS.md`. It is exact, so it also shows which sets are tight when `c = 1`: `d = 4`; `d = 5` with `σ_Φ = 3`; `d = 6` with all six inner sides black; a white-inner separating triangle; and `J = X`.
2. Theorem R removes the dependence on barnette_trees Thm 1.2 from Theorem 5.4 of the refereed report (see `REFEREE.md`, claim (e)).
3. Rado's theorem has an algorithmic proof (matroid intersection), so a rainbow tree is found in polynomial time. `rainbow.py` does this with augmenting paths.

**Lemma R2 (the black side is free) [PROVED-HERE].** There is always a spanning tree of `H*` with exactly one edge in each triangle `Δ_t`, `t ∈ A`.

*Proof.* By Rado it suffices that `rank(⋃_{t ∈ S} Δ_t) >= |S|` for `S ⊆ A`. Split `S` into classes `S_i` generated by "share a white neighbour". The union over `S_i` is connected on the set `N(S_i)` of white neighbours, so its rank is `|N(S_i)| - 1`. The `3|S_i|` sides of the faces of `S_i` are sides of faces in `N(S_i)`, so `|S_i| <= |N(S_i)|`. Equality would mean that every side of every face of `N(S_i)` belongs to a face of `S_i`. Then `S_i ∪ N(S_i)` is closed under adjacency of faces, hence is the set of all faces, and `t0 ∈ S_i`. That contradicts `S ⊆ A`. So `|N(S_i)| - 1 >= |S_i|`. ∎

**Evidence for Step R [COMPUTED].**

- `exp_rainbow.py rado 12`: all 57,901 connected sets `J` in the 262 rootings with `V <= 12`. Formula (R) holds for every one. The 68 violating sets all have `(c, d, σ_Φ) = (1, 3, 3)`. The minimum slack is `-1` in the 54 instances with a black-inner separating triangle and `0` in the other 208. Output `data/rado_12.json`.
- `exp_rainbow.py exist 16`: all 7,868 rootings with `V <= 16`. A rainbow tree exists in 5,088, exactly those with a pair (flow test), exactly those without a black-inner separating triangle. A face-rainbow tree exists in all 7,868. Output `data/exist_16.json`.

## 3. Step X

**Conjecture X.** In every rooted instance, from every rainbow tree there is a sequence of moves, none of which increases the excess, that ends at excess 0.

Equivalently there is no *trap*. Call two rainbow trees of equal excess *plateau-connected* if a sequence of moves of change 0 joins them. A trap is a plateau component of positive excess none of whose members has a move of change `-2`.

Together with Theorem R, Conjecture X is the key lemma (a tree matching exists when no separating triangle has black inner boundary), with no pair, no sign and no weight.

**Evidence [COMPUTED].**

| Range | What was enumerated | Result | Command, output |
| --- | --- | --- | --- |
| `V <= 12`, all rootings | all 74,432 rainbow trees of 208 instances | no trap; plateau depth at most 3 | `exp_rainbow.py traps 6 12 all`, `data/traps_6_12_all.json` |
| `V = 13, 14`, all rootings | all 1,327,360 rainbow trees of 672 instances | no trap; depth at most 4 | `traps 13 14 all` |
| `V = 15`, all rootings | all 4,030,720 rainbow trees of 914 instances | no trap; depth at most 5 | `traps 15 15 all` |
| `V = 16`, all rootings | all 29,366,528 rainbow trees of 3,294 instances | no trap; depth at most 5 | `traps 16 16 all` (467 s) |
| `V = 17`, all 13,980 rootings | 5,938 have no rainbow tree; 6,923 have one 2-factor, where X holds by Proposition U (§5); in the other 1,119 all 34,659,072 rainbow trees were enumerated | no trap; depth at most 7 | `exp_rainbow.py traps_multi 17 0 233`, `traps_multi 17 233 466` (155 s, 478 s) |
| `V = 18, 20, 22`, every 4th, 40th, 400th plantri triangulation, 2 random roots | 3,786 starts, one random and two adversarial per instance | all reach a tree matching, by surplus walks alone | `exp_walk.py sample 18 4 1`, `sample 20 40 1`, `sample 22 400 1` |
| random, `V = 40, 60, 80, 120`, and `V = 45` with glued octahedra | 396 starts on 132 instances | 395 reach a tree matching by surplus walks; the last one after a plateau search of depth 7 | `exp_walk.py random ...`, `exp_cycles.py analyse` |
| the saved `V = 40` to `120` instances of the graph-theory run (11 files) | 99 starts | 91 by surplus walks; the other 8 hit a periodic walk, see §4, and all 5 of them that were stuck at a tree with only periodic walkers escape by a plateau search of depth 3 to 27 | `exp_walk.py saved`, `exp_cycles.py analyse` |
| random, `V = 24` to `70` | 2,923 instances, 3,016,063 walkers classified exactly | 50 periodic walkers, the first at `V = 38`; 32 trees with only periodic walkers, and from every one a plateau search finds a decreasing move | `exp_cycles.py hunt ...`, eleven runs |

"Depth" is the largest plateau distance from a rainbow tree to one that has a decreasing move. "Adversarial start" means a random walk followed by `30n` random moves that never lower the excess. Start excesses went up to `n - 3`.

In the exhaustive rows the whole plateau structure was computed, so those rows are a proof of Conjecture X for the stated instances. For `V = 17` the instances with a single 2-factor are covered by Proposition U instead of enumeration. The filter that separates the two classes (`has_unique_two_factor`, acyclicity of `G_u` for the 2-factor of one rainbow tree) was validated at `V = 14, 15, 16`: it selects 44, 82 and 345 instances, none of which has `2^n` rainbow trees, and at `V = 14` these are exactly the 44 instances where `exp_average.py` finds the slot identity failing. The sampled rows only show that the tested starts are not in traps.

**The strict form is false [REFUTED].** "Every rainbow tree of positive excess has a move of change `-2`" fails from `V = 8` on. Among the rainbow trees with `V <= 16`, 1,684,312 have positive excess and no decreasing move (8,782 for `V <= 12`). So a plateau search cannot be avoided by a one-step rule. This also answers the brief's question "does a state cycle with `W = B + 1` always offer an improving exchange": no.

**Candidate potentials [COMPUTED, negative].** `exp_structure.py potential 12`: for each of the 73,812 rainbow trees of positive excess with `V <= 12`, is there a non-increasing move that lowers the pair (excess, secondary term) lexicographically? With the secondary term "least distance in `F_σ` between a face of load 2 and a face of load 0" this holds for 69,470. With the sum of such distances, 70,332. With distances in `H` instead of `F_σ`, 68,742 and 69,366. None is monotone.

## 4. The surplus walk

A face of load 2 holds two points. This gives a deterministic way to move.

**Definition.** A *walk state* is a triple `(σ, t, x)`: a rainbow tree, a face `t` with `c_σ(t) = 2`, and one of its two points, called the *arrival*. The other point `y` is the *resident*. One *step* applies the move at `y`. If `alt_σ(y)` had load 0, the excess drops by 2 and the walk stops. Otherwise `alt_σ(y) = t'` had load 1 and the new state is `(σ', t', y)`: the evicted point is the arrival at its new face. In words: evict the resident, follow it, repeat.

**Lemma X3 [PROVED-HERE].** The step is injective. The predecessor of a state is found by mirroring it (exchange the roles of arrival and resident), taking one step, and mirroring again. So the walk states of one instance split into paths and cycles. Each path has two ends, and at each end the next move (forward, or backward) lowers the excess by 2.

*Proof.* The move at `y` is an involution by Lemma X1. From `(σ', t', y)` the mirrored state has resident `y`, and evicting `y` returns it to `t`. So the backward step from any state is the forward step of its mirror. A forward step is defined unless its move decreases the excess (a move out of a face of load 2 never increases it). The same holds backwards. ∎

**Corollary X4 (involutions on tree matchings) [PROVED-HERE].** Fix `t ∈ A`. For a tree matching `s`, move the point `s(t)` out of `t` by its unique exchange and run the surplus walk until it stops. It stops at a tree matching `ι_t(s) ≠ s`, and `ι_t` is an involution on the set of tree matchings. In particular the number of tree matchings is even, by a sign-free pairing.

*Proof.* After the first move the excess is 2: `t` is empty and one face `t_1` has load 2, with arrival `x_0 = s(t)`. Backwards from this state the next move returns `x_0` to the empty face `t`, a decreasing move. So this state is an end of its orbit, the orbit is a path, and the forward walk stops. It stops with a move into the only empty face, `t`, at excess 0. Call the result `s'`. Reading the path backwards is the walk started from `s'` at the face `t`, so `ι_t(s') = s`. If `s' = s`, the path `u_1, ..., u_m` would equal its own reversal, `mirror(u_{m+1-i}) = u_i`. For odd `m` the middle state would equal its mirror, which has the other arrival point. For even `m` two consecutive states would have the same tree, but a step changes the tree. ∎

This gives the refereed report what it looked for under R7: a fixed-point-free involution that explains the evenness of the number of tree matchings. There are `n` of them, one for each bounded black face. The mate involution fails (claim (g)), these work. When no face is visited twice, `ι_t(s)` differs from `s` by rotating the assigned corners along one cycle through `t`.

COMPUTED (`exp_walk.py exhaust`): for all rootings with `V <= 15` and two rootings of every triangulation with `V = 16`, every pair (tree matching, face) was followed. All 107,226 pairs give a fixed-point-free involution, and the two ends of every excess-2 path empty the same face. Outputs `data/walk_exhaust_*.json`.

**X′: "the surplus walk is never periodic".** If true, it would settle Conjecture X with a deterministic algorithm: from any walk state, the walk stops at a decreasing move.

- COMPUTED, true in a large range. All rootings with `V <= 15` (5,432,512 rainbow trees, 31.7 million walk states, 7.9 million paths) and two rootings of every triangulation with `V = 16` (2,314,240 trees): no cycle. No path has more than `V + 2` states. Sampled `V = 18, 20, 22` (3,786 starts) and random `V = 24` to `36` (719,999 walkers classified exactly): no cycle.
- **REFUTED at `V = 38`.** Periodic surplus walks exist. Exact periods, found by comparing the full state with the start (`exp_cycles.py analyse`):

| Instance | `V` | excess | period |
| --- | --- | --- | --- |
| random, `hunt 38 400 19` (three trees) | 38 | 2 | 48, 68, 68 |
| `ef_fail_40_40` (graph-theory run) | 40 | 2 | 104 |
| random, `hunt 40 200 5` | 40 | 2 | 60 |
| `deeptrap_50_1` | 50 | 2 | 56 |
| random, `hunt 50 100 6` (two trees) | 50 | 2 | 88 |
| `alpha_min_fail_60_61` | 60 | 2 | 88 |
| `alpha_min_fail_100_7` | 100 | 2 | 132 |
| `alpha_max_fail_120_123` | 120 | 2 | 148 |
| random, `random 120 8 4` | 120 | 2 | 236 |

Machine-readable counterexamples (rotation system, outer face, `σ` as point to face-triple): the `failures` lists in `data/walk_saved.json` and `data/walk_random_120_8_4_0.0.json`, and `examples` in the `data/cycles_hunt_*.json` files (38, 40, 50, 60, 70). To verify one, load it and call `exp_cycles.orbit`. The smallest order with a periodic walk is somewhere between 17 and 38. In random sampling the first appears at `V = 38` (3 of 345,370 walkers), none among 719,999 walkers with `V = 24` to `36`, and the frequency grows with `V` (26 of 369,962 at `V = 70`).

The periodic walks sit on the same adversarial instances that broke single-step descent in the graph-theory run. Theorem S in §5 explains the link: a surplus walk is a `D`-cycle reversal done one point at a time, interrupted by the analogue of a `Q`-cycle reversal whenever a directed cycle would form, and those instances are the ones where the two kinds of reversal chase each other.

**Lesson.** Moving only the surplus is not enough. In all 38 trees found whose walkers are all periodic, moves of type `(1, 0)`, which relocate the empty face, lead to a decreasing move after a short plateau search (depth at most 27 and at most 2,048 trees explored in the cases recorded in detail). So Conjecture X survives, but a proof must use both kinds of plateau move.

## 5. Structure that might carry a proof

**Lemma X2 (fundamental cycle identity) [PROVED-HERE].** Let `σ` be a rainbow tree, `x ∈ X`, `t = σ(x)`, and let `Γ = (x, t, y_1, t_1, ..., y_k, t_k, x)` be the cycle of `F_σ + (t, x)`. Then `C = (x, y_1, ..., y_k)` is a simple cycle of `T` of length at least 3. Let `D` be its disk away from `t0`, with `B` black and `W` white faces. Then

    Σ_{f black in D} (c_σ(f) - 1) = W - B - 1 + [t in D].

*Proof.* `Γ` is simple, so the `y_i` are distinct, and `k >= 2` because an edge of `T` has only one black face. Let `h = k + 1`, `I` the number of vertices strictly inside `C`, `l` the number of edges of `C` whose black face is in `D`, and `m` the number of non-roots `v` on `C` with `σ(v)` in `D`. The spokes strictly inside the curve `Γ` are the three spokes of each of the `B - l` black faces of `D` not on `Γ`, and the third spoke of each of the `l` faces of `Γ` in `D`. That is `3B - 2l` spokes. The missing ones among them number `I + m - [t ∈ D]`: all interior vertices are non-roots with their missing face inside, and the only missing spoke on `Γ` itself is `(t, x)`. Since `F_σ + (t, x)` has the single cycle `Γ`, the tree edges inside `Γ` form a forest hanging from `Γ`, with as many edges as there are vertices of `H` strictly inside, `I + B - l`. So `3B - 2l - I - m + [t ∈ D] = I + B - l`. Euler's formula and the signed side count, valid for any simple cycle, give `B = I + (h + l)/3 - 1` and `W - B = (h - 2l)/3`. The left side of the lemma is `I + m - B`. Eliminating `m` and `I` gives the claim. ∎

For a tree matching the left side is zero, and the lemma says `W - B = 1 - [t ∈ D]`. That is the disk identity read on the fundamental cycle of a deleted spoke. For a rainbow tree with one face `a` of load 2 and one empty face `b`, a surplus step has `W - B = 1 - [b ∈ D]`. This is where the colouring and the disk count enter the exchange. COMPUTED: 102,976 of 102,976 moves, `exp_structure.py identity 12`.

This answers the brief's question about local terms as far as I can. The excess is `2·#{faces of load 2}`. One exchange changes it by `-2`, `0` or `+2`, and Lemma X2 fixes the net surplus enclosed by the exchange cycle in terms of the colour balance of its disk. I did not find a function of these data that decreases along some allowed move.

**Theorem S (rainbow trees are arborescences inside 2-factors) [PROVED-HERE].** Let `σ` be a rainbow tree. Root the tree `F_σ` at the centre of `t0` and let `par_σ(x)` be the parent of the non-root `x`. Then:

1. `σ ⊔ par_σ` is a 2-factor of `B`: every non-root has the two faces `σ(x) ≠ par_σ(x)`, and every `t ∈ A` receives `c_σ(t)` points from `σ` and `2 - c_σ(t)` from `par_σ`.
2. It is the only 2-factor of `B` that contains the edges `(x, σ(x))`.
3. Conversely let `F2` be a 2-factor of `B` and `u(t)` the corner of `t ∈ A` not joined to `t` in `F2` (the deleted corner of the graph-theory report, PROOFS Lemma 3.1). Let `G_u` be the digraph on `V(T)` with the two arcs `v -> u(t)` for the two other corners `v` of each `t ∈ A`. Every non-root has out-degree 2 in `G_u`, and the roots are sinks. A choice of one `F2`-edge `(x, σ(x))` at every non-root is a rainbow tree if and only if the *other* arcs, `x -> u(σ'(x))` with `σ' = F2 - σ`, contain no directed cycle. So the rainbow trees inside `F2` are the spanning in-forests of `G_u` rooted at the three roots, and the tree matchings inside `F2` are those in-forests that use exactly one of the two arcs of every face.

*Proof.* (1) The neighbours of `x` in `F_σ` are all its faces except `σ(x)`, so `par_σ(x) ≠ σ(x)`, and `par_σ(x) ≠ t0` since `x` is not a corner of `t0`. The centre of `t ∈ A` has `3 - c_σ(t)` neighbours in `F_σ`. One is its parent, the others are its children, and `t` is the parent of exactly those. (2) and (3). Let `σ ⊔ σ'` be a 2-factor containing `σ`, with deleted-corner map `u`. The spokes of `H - σ` at `t ∈ A` are the `2 - c_σ(t)` spokes of `σ'` and the spoke to `u(t)`. Orient `x -> σ'(x)` for non-roots, `t -> u(t)` for `t ∈ A`, and each root towards `t0`. Every vertex of `H` except the centre of `t0` gets out-degree exactly 1, and the edge count `n + n + 3 = 2n + 3` shows that all edges of `H - σ` are oriented. So `H - σ` is a tree iff this functional digraph has no cycle iff the map `x -> u(σ'(x))` has none. When it is a tree, the orientation is the one towards `t0`, hence `σ' = par_σ`. ∎

COMPUTED (`exp_selection.py 6 13`): in all 334 rootings with `V <= 13` that have a rainbow tree, each of the 208,320 rainbow trees is a selection from a 2-factor, and unions of selections over the 342 two-factors contain only 768 non-trees.

**Consequences.**

- *Pairs for free.* A rainbow tree gives a 2-factor of `B`, that is, a pair. So Theorem R is a second proof of OpenAI Prop. 3.1 in its sharp form (barnette_trees Thm 1.2 (ii) ⇔ (iii)), and "a pair exists" and "a rainbow tree exists" are equivalent for a structural reason, not only because their obstructions coincide.
- *For a tree matching `s`, `par_s` is the mate.* The digraph statement in (3) is then barnette_trees eq. (3): `Q_s` oriented by the mate is a forest.
- *Counting.* The number of rainbow trees is `Σ_{F2} κ(G_u)`, where `κ` counts spanning in-forests, a determinant by the matrix-tree theorem. It is at most `2^n` times the number of 2-factors.
- *Two kinds of exchange.* Inside its 2-factor, the move at `x` would re-point `x` from the arc through `par_σ(x)` to the arc through `σ(x)`, whose head is `z = u(σ(x))`. If `z` is not a descendant of `x` in the in-forest, this is the exchange, `alt_σ(x) = par_σ(x)`, and the 2-factor is unchanged. If `z` is a descendant of `x`, the re-pointing would close the directed cycle `x -> z -> ... -> w -> x`. Then the exchange is `alt_σ(x) = par_σ(w)`, the face `t'` through which the last vertex `w` of that path points at `x = u(t')`, and the new tree lies in another 2-factor.
- *Relation to the exchange graph of pairs.* The first kind, applied to the points of one cycle of the 2-factor in turn, is a `D`-cycle reversal carried out one point at a time. The intermediate selections have excess 2, and the order in which the points must be taken is the surplus walk of §4. So when no re-pointing on the way is blocked, `ι_t(s)` is `s` with the `D`-cycle through `t` reversed. The second kind happens exactly when a directed cycle of chosen arcs would appear, which for a pair is a cycle of `Q_s`, and it changes the 2-factor as a `Q`-cycle reversal does. The rainbow move graph is thus a version of the exchange graph of barnette_trees §4 in which every intermediate object is a spanning tree. This also explains why periodic surplus walks sit on the instances where `D`-swaps and `Q`-reversals chase each other.

**Proposition U (the easy case) [PROVED-HERE].** `G_u` has a directed cycle if and only if `B` has a second 2-factor. If `F2` is the only 2-factor, then all `2^n` selections are rainbow trees, the tree matchings are the `2^c` states inside `F2` (`c` its number of cycles), every exchange is a re-pointing, the slot identity `c_σ(t) + #{x : alt_σ(x) = t} = 2` holds, each load is a sum of two independent fair bits over the uniform measure, and the surplus walk runs along one cycle of `F2` and stops at the first empty face it meets.

*Proof.* A directed cycle `v_1 -> ... -> v_m -> v_1` of `G_u`, with arcs through faces `t_i` (so `u(t_i) = v_{i+1}`), gives the 2-factor `F2 - {(v_i, t_i)} + {(v_{i+1}, t_i)}`. Conversely the symmetric difference of two 2-factors is a union of alternating cycles, and an edge `(v, t)` outside `F2` has `v = u(t)`, so each alternating cycle is a directed cycle of `G_u`. If `G_u` is acyclic every choice of out-arcs is an in-forest, since the only sinks are the roots. The rest is counting on a cycle of `F2`: walking from a face of load 2 away from its arrival, the points met all select backwards until the first that selects forwards, and the face before it is empty. ∎

COMPUTED (`exp_selection.py`, `exp_average.py`): `B` has one 2-factor in 326 of the 334 instances with `V <= 13`, and these are exactly the instances with `2^n` rainbow trees. Over `V <= 14`, 828 of 880 instances have `2^n` rainbow trees, and these are exactly the instances where the slot identity holds for every tree and where the mean load is 1 at every face. In the other 52, all without separating triangles, all three fail. The first is `V = 12`, plantri index 2, outer face `{0, 1, 6}`: two 2-factors, `2·512 - 2·64 = 896` rainbow trees. It is also the first triangulation in which the mate of a tree matching is not a tree matching.

**What this says about Step X.** The difficulty is located exactly where the original proof has it. A rainbow tree is an acyclic choice of out-arcs in `G_u`. Its excess counts the faces whose two arcs are both used or both unused. Inside one 2-factor the surplus walk is a walk along a `D`-cycle, and it would always succeed if every re-pointing stayed acyclic. A re-pointing that closes a directed cycle is the rainbow version of a cyclic `Q_s`. The exchange then jumps to another 2-factor, the analogue of reversing a `Q`-cycle. So Conjecture X is a sign-free cousin of the component theorem (barnette_trees Thm 5.2), on the larger state space of in-forests instead of pairs. I could not derive X from that theorem or the theorem from X. HUNCH: X follows from the component theorem by lifting exchange paths of pairs to in-forests. Test: for `V <= 14`, check whether the plateau components of rainbow trees map onto exchange components of pairs.

**M-convexity of loads [REFUTED].** Let `L` be the set of load vectors of all rainbow trees. I conjectured that `L` is M-convex, which would have reduced the key lemma to a Hall-type condition on one submodular function. `exp_structure.py loads_sampled 6 13` tests the simultaneous exchange axiom on 4,000 random pairs per instance. It holds in the 326 instances where `B` has one 2-factor and fails in all 8 instances with two (7,758 failed exchanges out of 3,697,049; five violating pairs are in `data/loads_sampled_6_13.json`; the match with the number of 2-factors is checked by `scratch_mconv_vs_factors.py`). With one 2-factor the statement is empty of content: by Proposition U, `L` is the Minkowski sum over the points `x` of the two-element sets `{e_t, e_t'}`, `t, t'` the two faces of `x` in the 2-factor, and Minkowski sums of M-convex sets are M-convex. My first test (`loads 12`, only instances with `|L| <= 400`) had passed in all 108 instances it covered, because the size limit excluded the instances with two 2-factors. That is a selection effect worth remembering. A weaker one-sided statement survived: in all 208 instances with `V <= 12`, for each load vector and each face of load 2 some empty face can take one unit and the result is again a load vector (155,282 cases, `exp_structure.py loads 12`). That is Conjecture X read on load vectors, and it does not help to prove it.

**"Mean load 1 at every face" [REFUTED].** True exactly in the one-2-factor instances (Proposition U), false in the others. The lesson is that averages over rainbow trees do not see the tree matchings.

**The involutions do not connect the tree matchings [COMPUTED].** Join two tree matchings when some `ι_t` exchanges them. The resulting graph is connected in all 208 instances with `V <= 12` and in 648 of the 672 instances with `V = 13, 14` (`exp_walk.py exhaust`, field `iota_graph_connected`). So the `ι_t` pair the tree matchings up but do not act transitively.

## 6. What R plus X would give, said plainly

**A counting-free proof: yes, if X is proved.** Theorem R produces a rainbow tree whenever the triangle obstruction is absent. Conjecture X lowers its excess to 0. A rainbow tree of excess 0 is a tree matching, and its mate is its parent map (Theorem S). No sign, no weight and no cancellation appear. Half of this is done: R is proved, and it already yields the pair. X is open.

**A polynomial-time algorithm: no, not from X as stated.** X asserts that a non-increasing path exists. It does not bound the plateau search. The strict form is false, so some search is needed, and plateau components are large. The deterministic candidate, the surplus walk, has observed length at most `V + 2` per descent for `V <= 16`, but it is periodic on some instances from `V = 38` on. X becomes an algorithm only with a rule that picks plateau moves and has a polynomial bound. The data say that the needed plateau depth is small (at most 5 for `V <= 16`, 7 at `V = 17`, at most 27 in the periodic cases up to `V = 120`), which leaves the question open in both directions.

**What remains.**

1. Prove Conjecture X. The proof must use moves of both types `(2, 1)` and `(1, 0)`, since surplus moves alone can cycle. It must use planarity, since the general problem is NP-hard. In the language of Theorem S it must say how to leave a 2-factor whose in-forests cannot be balanced, which is the content of the cancellation in the original proof. Lemma X2 is the only place where I see the disk identity entering an exchange.
2. Decide whether X follows from barnette_trees Thm 5.2 (the HUNCH above). If it does, X is a theorem and what is missing is only its direct proof. If plateau components do not map onto exchange components, X is a new statement.
3. Find the smallest periodic surplus walk, between `V = 17` and `V = 38`, and read off which directed cycle of `G_u` it keeps running into.
4. Count the in-forests with one arc per face directly. By the matrix-tree theorem the number of tree matchings inside `F2` is the coefficient of `Π_t y_t` in `det L_u(y)`, where the two arcs of `t` carry the weight `y_t`. That is a mixed discriminant of `n` matrices of rank at most 2. I did not pursue it. It may be the same determinant as in the referee-determinants run.

## 7. Counterexamples and data, machine-readable

| What | Where |
| --- | --- |
| Periodic surplus walks (`V = 38` to `120`) | `data/walk_saved.json` (`failures`), `data/walk_random_120_8_4_0.0.json`, `data/cycles_hunt_*.json` (`examples`: rotation system, outer face, `σ`, periods), exact periods of the first group in `data/cycles_analyse.json` |
| Failures of M-convexity | `data/loads_sampled_6_13.json` (`violations`: faces, the two load vectors, the index of the face) |
| Instances where the slot identity and the mean-load guess fail | `data/average_6_14.json` (`mean_load_failures`), `data/selection_6_13.json` (`examples_where_families_differ`) |
| Tree matchings whose mate is not a tree matching | `data/ref_mate.json` (`examples`, 12 with rotation systems) |
| All counts quoted in this file | the JSON file named next to each count; each stores its command |
