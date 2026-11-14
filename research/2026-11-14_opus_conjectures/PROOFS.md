# Proofs

Notation is the shared one (`research/BRIEF.md`). A 2-factor of `B` is written through its deleted-corner map `u: A -> V(T)`: `u(t)` is the corner of `t` not used by the 2-factor. The pairs `(r, s)` with deleted corners `u` are the `2^c` orientations of the `c` cycles of `D` (graph-theory folder, PROOFS Lemma 3.1). `H_0` is the spoke graph without the centre of `t0`. `O_u` is the orientation of `H_0` with `u(t) -> t` and `t -> v` for the two other corners `v` of `t`. All roots have every spoke pointing out (the faces at a root delete the root), so the orientations `O_u` are exactly the alpha-orientations with out-degree 2 at centres, `d_x - 2` at nonroots and `d_r - 1` at roots (`d` = number of black faces at the vertex).

Faces of `T` are traced with the interior on the left and called counterclockwise. The faces of `H_0` are the hexagons around the inner white faces plus one outer face `O` (the three white faces at `t0` merged with `t0`).

Each proof was re-read once adversarially. The objections raised in that reading and how they were met are listed after each proof.

---

## Lemma 1. The lattice of 2-factors as a system of difference constraints

`PROVED-HERE`. Felsner (`LIT`: S. Felsner, Lattice structures from planar graphs, Electron. J. Combin. 11 (2004) R15, cited from memory, not opened) proves the lattice property in general. The version below is self-contained and is what `code/bar.c` computes.

Fix one 2-factor `u0` and its orientation `O_0 = O_{u0}`. For each spoke `e` let `L(e)`, `R(e)` be the faces of `H_0` to the left and right of `e` directed as in `O_0`.

**Statement.** The map `O -> phi_O` defined below is a bijection from alpha-orientations of `H_0` onto the integer functions `phi` on the faces of `H_0` with `phi(O) = 0` and

    phi(R(e)) - phi(L(e))  in  {-1, 0}      for every spoke e,                    (1)

and `O` reverses `e` relative to `O_0` iff the difference in (1) is `-1`. Under the componentwise order the solutions of (1) form a distributive lattice with least element `phi_lo(f) = -dist(f, O)` and greatest element `phi_hi(f) = dist(O, f)`. The distances are taken in the digraph with an arc `L(e) -> R(e)` of weight 0 and an arc `R(e) -> L(e)` of weight 1 for every spoke. The element `E_lo` (from `phi_lo`) has no clockwise directed cycle, and `E_hi` has no counterclockwise one.

*Proof.* `H_0` is connected. Every edge `xy` of `T` lies in exactly one black face `t`. If `t != t0`, `x - t - y` is a path in `H_0`. The edges of `t0` join roots. Every root lies in a bounded black face (its degree is at least 4, so it lies in at least two black faces), and that face has nonroot corners. `T` minus the three edges of `t0` is connected because `T` is 3-connected. So `H_0` is connected.

Let `O` be an alpha-orientation. Let `c_O` be the 1-chain that puts `+1` on each spoke reversed by `O`, in its `O`-direction. At every vertex `O` and `O_0` have the same out-degree, so the reversed spokes leaving a vertex in `O` are as many as those entering it. Hence `c_O` is a circulation. In a connected plane graph every integer circulation is `sum_f phi(f) d(f)`, where `d(f)` is the clockwise boundary of `f`. The function `phi` is unique up to an additive constant, which we fix by `phi(O) = 0`. Written edge by edge, the value of the chain on `e` along a direction `d` is `phi(right of d) - phi(left of d)`. Along the `O_0`-direction a reversed spoke carries `-1` and an unreversed one `0`. This is (1), and the reversal criterion.

Conversely, let `phi` satisfy (1). Reverse the spokes where the difference is `-1`. The reversed spokes, in their new direction, form the circulation `sum phi(f) d(f)`, so in-degree and out-degree change equally at each vertex and the out-degrees stay the same. So we get an alpha-orientation, and the two maps are inverse to each other.

Each constraint has the form `x_i - x_j <= w`. If `phi` and `psi` satisfy such a constraint, so do their pointwise minimum and maximum. The solution set is therefore a sublattice of `Z^faces`, and a sublattice of a product of chains is distributive. It is finite because the constraint digraph is strongly connected (every spoke gives arcs both ways) and `phi(O) = 0`. The formulas for the extremes are the standard shortest-path solution of a difference system. `phi(f) <= phi(O) + dist(O, f)` for every solution, and `dist(O, .)` is itself a solution. The same argument on the reversed digraph gives the least element.

Senses. Let `Z` be a simple directed cycle of `O` and `O'` the orientation with `Z` reversed (again an alpha-orientation). Then `c_{O'} - c_O` is the chain of `Z` traversed backwards. If `Z` is counterclockwise, the backwards traversal is clockwise and equals `d(int Z) = sum_{f inside Z} d(f)`. Then `phi_{O'} = phi_O + 1` on the faces inside `Z`, so `phi_{O'} > phi_O`. If `Z` is clockwise, `phi_{O'} < phi_O`. The least element therefore has no clockwise directed cycle, and the greatest element no counterclockwise one. ∎

*Adversarial reading.*
- "Spokes with the same face on both sides break (1)." Such a spoke has `L = R`, so (1) reads `0 in {-1, 0}`. It is never reversed, which is correct: reversing a single spoke changes out-degrees. The code skips these spokes.
- "The sign convention could be flipped in the code." `bar.c` counts directed facial hexagons at both extremes. Over all 3,301,113 rooted instances at `V = 22`, `E_lo` had 548,937 counterclockwise directed hexagons and no clockwise one, and `E_hi` the reverse. This agrees with the lemma.
- "Is this Felsner's lattice?" Yes as a set and an order. The cover relations are raising a minimal forced set of faces by 1 (`bar.c`, `closure`). When rigid spokes glue faces, such a set has more than one face, and a single hexagon flip cannot reach it. That explains Remark 1.1.

**Remark 1.1** (`COMPUTED`, `code/checku.py`). The graph-theory folder computed its "face-flip minimum and maximum" greedily, one hexagon at a time. In 7 of its 9 saved files the greedy result is a local extreme (no single hexagon can move) but not the true extreme of the lattice. In one more file (`alpha_max_fail_120_123`) it is the true greatest element. The ordered names "min" and "max" there are the mirror image of the convention here: on `ef_fail_40_40` their "minimum" equals `E_lo` exactly. So the old failure rates for O4, O5 and O6 refer to a greedy procedure, not to the lattice.

---

## Lemma 2. Tree pairs are orientations that cut every directed cycle

`PROVED-HERE`. `COMPUTED` cross-check in `code/anatomy.py`, where every orientation of every 2-factor of the `V = 18` counterexample agrees with the direct forest test.

**Statement.** Let `(r, s)` be a pair with deleted corners `u`. Then `s` is a tree matching iff no directed cycle of `O_u` leaves every centre it passes, `t`, towards `r(t)`.

*Proof.* Let `F` be the subgraph of `O_u` with the spokes `u(t) -> t` and `t -> r(t)` for `t in A`. In `F` every centre has in-degree 1. Every nonroot `x` has in-degree 1, from the face `r^{-1}(x)`, because the spokes into `x` in `O_u` come from the faces with `x in {r(t), s(t)}`. Roots have in-degree 0. The edge of `Q_s` in `t` is `{r(t), u(t)}`, the pair of `F`-neighbours of the centre `t`. So `F` is `Q_s` with each edge subdivided by its own centre. Different faces give different edges of `T`, since every edge has exactly one black face. Hence `F` has a cycle iff `Q_s` has one. In a digraph with all in-degrees at most 1, a cycle of the underlying graph with `k` vertices has `k` edges and `k` heads, one per vertex, so it is a directed cycle.

So `Q_s` is a forest iff `F` has no directed cycle. A directed cycle of `O_u` lies in `F` iff it leaves each of its centres towards `r(t)`. At a centre it always enters from `u(t)`, the only spoke into `t`. At a vertex `x` it leaves along some `x -> t` with `u(t) = x`, which is in `F`.

Finally, if `Q_s` is a forest, it has `n` edges on `n + 3` vertices, so 3 components. In `F` each component has exactly one vertex of in-degree 0, so each contains exactly one root. This is the tree-matching condition. ∎

**Corollary 2.1** (`PROVED-HERE`). Fix `u` with D-cycles `C_1, ..., C_c` and a reference orientation of each. Call a directed cycle `Z` of `O_u` *dangerous* if, on every D-cycle it meets, it leaves all faces of that cycle in the same direction (all towards heads, or all towards tails). A dangerous `Z` excludes exactly the orientations that agree with its pattern on the cycles it meets, which is a subcube of `{+,-}^c`. Every other directed cycle excludes nothing. So `u` carries a tree pair iff the subcubes of its dangerous cycles do not cover `{+,-}^c`. When `c = 1`, `u` fails iff it has a dangerous cycle of each direction.

**Corollary 2.2** (`PROVED-HERE`). The hexagon around an inner white face `y = (a, b, c)` is a directed cycle of `O_u` iff, up to rotating `y`, `u(t_ab) = a`, `u(t_bc) = b`, `u(t_ca) = c`, where `t_ab` is the black face across `ab`. It lies in `F` iff moreover `r(t_ab) = b`, `r(t_bc) = c`, `r(t_ca) = a`, and that holds iff `Q_s` contains the three sides of `y`. So a directed facial hexagon kills exactly the orientations in which `Q_s` contains the white triangle `y`.

*Adversarial reading of Lemma 2.* "Could `Q_s` have a 2-cycle (a doubled edge)?" No: the edges come from distinct black faces, and an edge of `T` has one black face. "Does 'Q_s forest' alone give a tree matching without the partner?" It does here because the partner `r` is given. The limits folder shows that without a partner a forest `Q` can have a component with two roots.

---

## Lemma 3. A unique 2-factor forces equality in C1

`PROVED-HERE`. The converse is `COMPUTED`; see CONJECTURES.md, C1.

**Statement.** If `B` has exactly one 2-factor `u`, with `c` cycles, then all `2^c` pairs are tree pairs, `c_min = c`, and `#TM = 2^{c_min}`.

*Proof.* Let `(r, s)` be a pair, necessarily with deleted corners `u`. Suppose `Q_s` has a cycle `K`. Reversing `K` gives a partner `r'` of `s`, with `r'(t) = u(t)` on the faces supplying `K` and `r' = r` elsewhere (trees paper, Prop. 2.1, re-proved as Lemma 2 in the combinatorics folder). The deleted corner of `(r', s)` on a face of `K` is the third corner, `r(t) != u(t)`. So `(r', s)` belongs to a different 2-factor, a contradiction. Hence every `Q_s` is a forest and every pair is a tree pair. Different orientations give different second states, and each tree matching has exactly one partner (k = 0), so `#TM = 2^c`. With only one 2-factor, `c_min = c`. ∎

---

## Proposition 4. The moment identities of Theorem B cannot give `2^{c_min}`

`PROVED-HERE`. The arithmetic is checked by hand below.

Theorem B (combinatorics folder, refereed) says that the signed measure `mu = sum over tree matchings of eps(s) delta_{h_s}` on `Z^{inner white faces}` kills every polynomial of degree less than `m = c_min` and some monomial of degree `m`. The corollary `#TM >= 2m` uses only this.

**Statement.** For `m = 3` and `m = 4` there are signed measures with these two properties, with weights `±1`, on `2m < 2^m` distinct integer points. So no argument that uses only these properties can prove C1.

*Proof.* Put points on the diagonal line `h = x (1, ..., 1)`. On that line a polynomial of degree `< m` in the heights is a polynomial of degree `< m` in `x`. Take the Prouhet-Tarry-Escott solutions

    m = 3:  {0, 4, 5}  vs  {1, 2, 6}:       sums 9 = 9,  squares 41 = 41,  cubes 189 vs 225;
    m = 4:  {0, 4, 7, 11}  vs  {1, 2, 9, 10}:  sums 22, squares 186, cubes 1738 on both sides,  fourth powers 17298 vs 16578.

Weight the first set `+1` and the second `-1`. The power sums of degree `< m` agree, so all polynomials of degree `< m` in `x` are killed. The degree-`m` power sums differ, so the monomial `x^m` (the product of the heights at `m` faces, restricted to the line) is not killed. These are 6 and 8 points, fewer than 8 and 16. ∎

So a proof of `#TM >= 2^{c_min}` has to use structure that Theorem B does not see: the cubes themselves, the exchange moves, or the integrality of the minimal-cover counts `N(w_1, ..., w_m)` over all choices of faces. The data in CONJECTURES.md (C1) point at the lattice of 2-factors: equality holds exactly when the lattice has one element.

*Adversarial reading.* "Theorem B also fixes the degree-`m` values to be `±N(w)` for every choice of `w`, a whole family of constraints." True. The proposition only says the vanishing part plus nonvanishing is not enough. Whether the full family of values `N(w)` forces `2^m` is open. I did not find a construction either way.

---

## What I tried to prove and could not

1. **Some extreme carries a tree pair (C2).** It is false (CONJECTURES.md). The obstruction is now explicit (Corollaries 2.1, 2.2). At `E_lo` every directed cycle is counterclockwise, but nothing ties the direction in which a counterclockwise cycle leaves its centres to the orientation of the D-cycles. In the `V = 18` example both directed cycles at each extreme are facial hexagons on the single Hamiltonian D-cycle, one leaving forwards and one backwards. The orientation `+` makes `Q_s` contain one white triangle, and `-` the other.
2. **C1 by induction on the lattice.** Lemma 3 settles the one-element lattice. The next case, two elements, already fails the naive step. In 936 of the 287,110 rooted instances at `V = 20` the minimal 2-factors carry no tree pair at all, so any injection of `{0,1}^{c_min}` into tree matchings must leave the minimal cubes.
