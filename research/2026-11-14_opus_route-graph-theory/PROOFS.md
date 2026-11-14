# Proofs: structural facts around the tree matching

Opus 5.5, 2026-11-14. Notation as in `research/BRIEF.md`. In addition:

- `d_v` = number of black faces at a vertex `v` of `T` (so `deg_T(v) = 2 d_v`).
- `H` = the full spoke graph (all black centres, including `t0`, joined to their corners). `H_0 = H - t0`.
- A *tree matching* is a state `s` with `H - s` a spanning tree, equivalently `Q_s` a forest with one root per component (barnette_trees, eq. (3)).
- `TM` = the set of tree matchings, `ST` = the set of states.
- "OpenAI" = `papers/OpenAI-Barnette.pdf`, "Li" = `papers/A-Note-On-Barnette.pdf`, "BT" = `papers/barnette_trees.pdf`.

Every statement carries a tag. `PROVED-HERE` means the full proof is in this file. Computations are in `code/` (see `code/README.md`).

Contents:

1. The three-matroid form of the tree-matching problem, and why it is not a two-matroid problem
2. The exact obstruction to a pair, with an Euler identity that makes the density bound one line
3. Pairs as alpha-orientations (the deleted-corner form)
4. The primal reading: which 3-edge cuts matter (Li's hypothesis)
5. Gluing across separating triangles
6. Degree-4 expansion: generation and the lift of states
7. Two induced trees versus tree matchings
8. Why the strong descent lemma must fail
9. Small remarks (Grinberg, colourings)

---

## 1. The three-matroid form

**Lemma 1.1** (`PROVED-HERE`). Let `E_B` be the spokes of `B` (centre `t in A`, corner `x in X`). A set `s` of spokes is a tree matching if and only if it is a common basis of three matroids on the spokes of `H`:

1. the cographic matroid `M*(H)` (so `H - s` is a spanning tree);
2. the partition matroid `P_c` with blocks "spokes at the centre `t`", capacity 1 for `t in A` and 0 for `t0`;
3. the partition matroid `P_v` with blocks "spokes at the vertex `v`", capacity 1 for `v in X` and 0 for roots.

*Proof.* A common basis of `P_c` and `P_v` with `n` elements is a perfect matching of `B`. Its complement is a spanning tree of `H` exactly when it is a basis of `M*(H)`. Cardinalities match: `|E(H)| - (|V(H)| - 1) = (3n+3) - (2n+3) = n`. ∎

The same set in the triangulation: send the spoke `(t, x)` to the edge of `t` opposite `x`. This is a bijection from `E_B` onto the edges of bounded black faces whose opposite corner is a nonroot (each edge of `T` has exactly one black face). Under it, `M*(H)` restricted to these edges becomes the graphic matroid of `T/R` (the roots identified), `P_c` becomes "one edge per bounded black face" and `P_v` becomes "one edge opposite each nonroot". This is just eq. (3) of BT.

**Duality does not reduce the count.** Planar duality sends `M*(H)` to the graphic matroid `M(H*)` of the white-face graph `H*`, and sends each partition matroid to a partition matroid (the dual of a partition matroid with capacities `c_i` on blocks of size `m_i` is the partition matroid with capacities `m_i - c_i`). So complementing (`F = H - s` instead of `s`) or dualising produces again one graphic or cographic matroid and two partition matroids. The two partition matroids are on the same ground set with blocks given by the two ends of each spoke. Their common bases are perfect matchings of `B`, which do not form the bases of a matroid in general.

A pleasant restatement (`PROVED-HERE`, immediate from Lemma 1.1 and Lemma 2.1 of OpenAI): `H*` is a 6-regular plane graph whose faces are the black centres (triangles) and the vertices of `T` (`d_v`-gons). Every edge of `H*` lies on exactly one centre-face and one vertex-face. A tree matching is the same thing as **a spanning tree of `H*` that contains exactly one edge of every face**, except that it avoids the faces `t0, r0, r1, r2` completely.

**Proposition 1.2** (`PROVED-HERE`, relying on `LIT` [ANS]). The following problem is NP-hard under polynomial-time Turing reductions: given a planar bipartite graph `K` of maximum degree 3, decide whether `K` has a perfect matching `M` such that `K - M` is a spanning tree.

*Proof.* Reduce from Hamiltonian cycle in planar cubic bipartite graphs [ANS]. Let `G` be such a graph and `v` a vertex with edges `e1, e2, e3`. A Hamiltonian cycle uses two of the three, so `G` is Hamiltonian iff it has a Hamiltonian cycle through `e1` or one through `e2`. For an edge `e = uw`, put `K = G - e`. If `C` is a Hamiltonian cycle through `e`, then `M = E(G) - C` is a perfect matching of `G` avoiding `e`, hence of `K`, and `K - M = C - e` is a Hamiltonian path, a spanning tree. Conversely, if `M` is a perfect matching of `K` with `K - M` a spanning tree, then in `K - M` the vertices `u, w` have degree 1 and every other vertex degree 2. A tree with exactly two leaves is a path, so `K - M` is a Hamiltonian `u`-`w` path and adding `e` gives a Hamiltonian cycle of `G`. ∎

[ANS] T. Akiyama, T. Nishizeki, N. Saito, *NP-completeness of the Hamiltonian cycle problem for bipartite graphs*, J. Information Processing 3 (1980) 73–76. They prove NP-completeness for 2-connected cubic bipartite planar graphs. I cite from memory and did not open the paper here, so check the exact class before relying on it.

**Consequence.** "Delete a perfect matching and keep a spanning tree" has no good characterisation (an NP ∩ coNP certificate of non-existence) on planar bipartite graphs unless NP = coNP. In particular it is not a two-matroid intersection on this class, where Edmonds' theorem would give such a characterisation. Whatever makes the spoke graphs of Eulerian triangulations special (all faces hexagons, all centres of degree 3, the roots) has to enter any min-max proof. This is consistent with the existence theorem: on spoke graphs the answer is always yes once the obstruction of Section 2 is absent, so the problem is a total search problem, and its complexity is a different question (see REPORT, leads).

The computations behind the matroid verdict are listed in `ROUTES.md`, route M. In short: none of the three two-matroid relaxations equals `TM` (`COMPUTED`). The tree matchings do not form the bases of a matroid. The natural polyhedral relaxation (perfect-matching polytope of `B` intersected with the cographic base polytope of `H`) is **not integral** (`COMPUTED`, first at `V = 13`).

---

## 2. The exact obstruction to a pair

**Theorem 2.1** (`LIT`: BT Theorem 1.2 (ii)⇔(iii), sharpening OpenAI Prop. 3.1; the proof below is `PROVED-HERE` and shorter). `B` has two edge-disjoint perfect matchings if and only if no separating triangle of `T` has black inner boundary. Here a separating triangle has black inner boundary when the three faces incident with its edges on the side not containing `t0` are black.

The reduction to a density bound is standard: by integral max-flow (or Ore's 2-factor theorem, as in Li Thm 10), a 2-factor of `B` exists iff `sum_{t in A} min(2, |V(t) ∩ S|) >= 2|S|` for all `S ⊆ X`. With `U = V(T) - S` (which contains `R`) this is equivalent to (OpenAI (3.2), BT (5))

    e(U) - b(U) <= 2|U| - 4        for all U ⊇ R,        (2.1)

where `e(U)` counts edges of `T[U]` and `b(U)` counts black faces of `T` (including `t0`) with all three corners in `U`. OpenAI and BT both derive this equivalence. The step is: a black face with `j` corners in `U` falls short of 2 by `max(0, j-1)`, which is its number of edges in `T[U]` minus one if `j = 3`.

The proof of (2.1) rests on one exact identity.

**Lemma 2.2** (Euler identity, `PROVED-HERE`). Let `K` be a connected subgraph of `T` induced on `p >= 3` vertices, with `m` edges. Call a face of the plane graph `K` *actual* if it is a face of `T`, and a *region* otherwise. Let `b` be the number of actual black faces of `K` and, for each region `F_i`, let `d_i` be its boundary length (edge sides) and `beta_i` the number of black faces of `T` inside it minus the number of white faces inside it. Then

    m - b - (2p - 4) = (1/2) * sum_i ( beta_i - (d_i - 4) ).        (2.2)

*Proof.* Let `w` be the number of actual white faces and `k` the number of regions. Euler's formula gives `p - m + (b + w + k) = 2`, and counting edge sides gives `2m = 3b + 3w + sum_i d_i`. Hence

    m - b - (2p - 4) = -m + b + 2w + 2k = (1/2)( w - b - sum_i (d_i - 4) ).

`T` has as many black faces as white faces (each edge has one of each, and both colour classes have exactly `|E|/3` faces). The faces of `T` are the actual faces of `K` together with the faces inside regions, so `w - b = sum_i beta_i`. ∎

**Lemma 2.3** (signed side count, `LIT`: OpenAI §3, BT (6); restated). For a region of boundary length `d`, `3 beta = sum_{j=1}^{d} sigma_j`, where `sigma_j = +1` if the face of `T` inside the region along the `j`-th boundary side is black and `-1` if white. Consequently `beta ≡ d (mod 2)`, `|beta| <= d/3`, and

- `d = 3`: `beta = ±1`, with `beta = +1` exactly when all three inner faces are black;
- `d >= 4`: `beta <= d - 4`.

*Proof.* Sum `+3` over black and `-3` over white faces of `T` inside the region, distributed over their sides. A side interior to the region is shared by a black and a white face and cancels. The remaining sides are the boundary sides. For the bounds: `3 beta` has the parity of `d` and is a multiple of 3. If `d = 4`, then `|3 beta| <= 4` and `beta` is even, so `beta = 0`. If `d = 5`, then `beta` is odd and `|beta| <= 1`. If `d >= 6`, `d/3 <= d - 4`. ∎

*Proof of Theorem 2.1.*

Necessity. Let `Delta` be a separating triangle with black inner boundary and `U` the set of vertices not strictly inside it. Then `U ⊇ R`, `T[U]` is connected, and every face of `T[U]` except the inside of `Delta` is actual. The single region has `d = 3` and `beta = +1`, so (2.2) gives `e(U) - b(U) - (2|U| - 4) = (1/2)(1 + 1) = 1 > 0`, violating (2.1).

Sufficiency. Assume no separating triangle has black inner boundary, and let `U ⊇ R`. Split `T[U]` into components. Every edge of `T[U]` and every black face counted by `b(U)` belongs to one component, and an actual face of `T` with corners in a component is a face of that component. So `e(U) - b(U) = sum_K (m_K - b_K)`.

- *The root component* `K_R` contains `r0, r1, r2` (they are pairwise adjacent). If `p = 3` it is `t0` itself: `m - b = 3 - 1 = 2 = 2p - 4`. If `p >= 4`, apply (2.2). A region of length `d >= 4` contributes `<= 0` by Lemma 2.3. A region of length 3 is bounded by a 3-cycle. Since `p >= 4` there is a vertex of `K` on the other side. If the region contained no vertex of `T` it would be a face of `T`, because any edge of `T` inside it joins two corners of the triangle, and in a simple graph those edges are the triangle's own sides. So the 3-cycle is a separating triangle. `t0` is an actual face of `K_R`, hence lies on the other side, so the region side is the inner side. Its boundary is not all black, so `beta = -1` and the region contributes 0. Hence `m - b <= 2p - 4`.
- *Any other component* `K` with `p >= 4`: the same argument applies to every region except possibly the one region containing `t0`, which contributes at most `(1/2)(1 + 1) = 1`. So `m - b <= 2p - 3 <= 2p`. For `p <= 3`, simplicity gives `m - b <= 3 <= 2p`.

Summing, `e(U) - b(U) <= (2p_R - 4) + sum_{K != K_R} 2p_K = 2|U| - 4`. ∎

**Remarks.**

1. The identity (2.2) shows exactly where the slack goes. Each region with `d >= 4` has slack `d - 4 - beta >= 0`, each "white-inner" separating triangle has slack 0, and each "black-inner" separating triangle has excess 2. In particular the deficiency `max_U [e(U) - b(U) - 2|U| + 4]` is at least the number of black-inner separating triangles that are not nested inside one another. I did not check whether it equals that number.
2. Hall-free construction. I did not find a construction of the pair that avoids max-flow. The proof shows the *certificate of non-existence* is always a single triangle, which is a strong hint that an explicit construction should exist (as for Schnyder woods, whose existence also follows from a density count but which have a canonical-order construction). See `ROUTES.md`, route F.

---

## 3. Pairs as alpha-orientations

**Lemma 3.1** (`PROVED-HERE`). The following are in bijection:

(a) 2-factors of `B` (equivalently, unordered pairs `{r, s}` up to reversing cycles of `D(r,s)`);

(b) maps `u: A -> V(T)` with `u(t) in V(t)`, `|u^{-1}(x)| = d_x - 2` for every nonroot `x` and `|u^{-1}(r)| = d_r - 1` for every root `r` (the *deleted corner*);

(c) orientations of `H_0` with out-degree 2 at every bounded centre, `d_x - 2` at every nonroot and `d_r - 1` at every root (an alpha-orientation in Felsner's sense).

*Proof.* (a)→(b): `u(t)` is the corner of `t` not used by the 2-factor. A nonroot `x` has `d_x` black faces, all in `A`, and is used by exactly 2. A bounded black face at a root `r` has `r` as its only root corner (the edge between two roots lies in `t0`), so its two `B`-spokes are both used and `u(t) = r`. (b)→(c): orient `(t, v)` from `t` to `v` if `v != u(t)` and from `v` to `t` otherwise. (c)→(a): the spokes leaving centres form the 2-factor. The counts match because `sum_v d_v = 3(n+1)`. ∎

Felsner's theorem (`LIT`: S. Felsner, *Lattice structures from planar graphs*, Electron. J. Combin. 11 (2004) R15; cited from memory, not opened here) makes the set (c) a distributive lattice, generated by reversing directed essential cycles. Its unique minimum has no counterclockwise directed cycle. Since `H_0` has hexagonal bounded faces, a face flip is the rotation of `u` around a white triangle that avoids the roots. The ordered pairs inside one 2-factor are the `2^c` orientations of its `c` cycles. Route O in `ROUTES.md` reports what the extremes of this lattice do (`COMPUTED`): the maximum always carried a tree pair in my samples, the minimum did not.

---

## 4. The primal reading: which 3-edge cuts matter

Let `G = T*` be the Barnette graph, `b0` the black vertex dual to `t0`.

**Proposition 4.1** (`PROVED-HERE`; the colour statement is `LIT`, Li Appendix C).

(i) Separating triangles of `T` correspond to nontrivial 3-edge cuts of `G` (both sides with at least two vertices). For a cubic 3-connected graph these are the same as cyclic 3-edge cuts.

(ii) For every nontrivial 3-edge cut `delta(Y)`, the three cut edges have ends of one colour in `Y` and of the other colour outside `Y`.

(iii) A separating triangle has black inner boundary (relative to `t0`) iff the corresponding cut `delta(Y)`, with `Y` the side not containing `b0`, has its three `Y`-ends black.

*Proof.* (i) A 3-cycle of `T` with vertices strictly on both sides is a closed curve crossing three edges of `G` and separating faces of `G` on both sides. Each side contains a face of `G`, hence a cycle, hence at least three vertices. Conversely, both sides of a nontrivial 3-edge cut induce connected subgraphs (Li App. C), so the cut is a bond and dualises to a 3-cycle of `T`: a closed curve through three pairwise adjacent faces, giving a 3-cycle of `T` with faces of `G` (vertices of `T`) on both sides. A side `Y` of a 3-edge cut with `|Y| >= 2` spans `(3|Y| - 3)/2 >= |Y|` edges when `|Y| >= 3`, and `|Y| = 2` is impossible by parity, so it contains a cycle. (ii) Counting the edges of `G[Y]` from both colour classes gives `3(|B ∩ Y| - |W ∩ Y|) = |delta_B| - |delta_W|`, which lies in `{±1, ±3}` and is a multiple of 3. (iii) The face of `T` on the inner side of a triangle edge is the `Y`-end of the dual cut edge, and faces of `T` are black exactly when the dual vertex of `G` is black. ∎

**Corollary 4.2** (`PROVED-HERE` from Thm 2.1 and Prop. 4.1). Li's Lemma 9 (`G_FB - N[b0]` has a 2-factor) holds **exactly** when every nontrivial 3-edge cut has `b0` on its black-ended side. Cyclic 4-edge-connectivity is sufficient but not necessary.

`COMPUTED` (`code/exp_obstruction.py`, `data/obstruction_16.txt`): over all 7,868 rooted Eulerian triangulations with `V <= 16`, the flow test agrees with the black-inner criterion every time. Of the 4,494 rooted instances that have a separating triangle (primal not cyclically 4-edge-connected), 1,714 still have pairs. The smallest is `V = 9` (two octahedra glued on a face), where 8 of 14 rootings have pairs.

So Li's choice is the convenient one, not the sharp one. It is "right" in the sense that after splitting along all separating triangles the pieces are cyclically 4-edge-connected, which makes the induction canonical. BT §7.3 shows that one only needs to split at black-inner triangles.

---

## 5. Gluing across separating triangles

**Theorem 5.1** (`LIT`: OpenAI Thm 2.2 and §7; BT §7.3. The version below is `PROVED-HERE`). Let `T` be an Eulerian triangulation, `t0` a face and `e0` an edge of `t0`. Then `V(T)` splits into two sets, each inducing a tree, with the ends of `e0` in one set and the third corner of `t0` in the other.

*Proof.* Induction on `|V(T)|`. Colour `t0` black. If no separating triangle has black inner boundary, use Theorem 2.1, the existence of a tree matching (OpenAI Prop. 5.1 or BT Thm 5.2), and the construction of OpenAI §6 / BT Lemma 7.1. Otherwise let `Delta` be a black-inner separating triangle. Cut along it and cap each side with a new triangular face on `Delta`. Both pieces are simple triangulations with fewer vertices: each side has at least one vertex strictly inside.

*Cap colour.* On one side, `3(B - W)` equals the sum of the three boundary signs (Lemma 2.3 with `d = 3`), so the three faces along `Delta` on that side all have the same colour. Give the cap the opposite colour. Every vertex keeps an even degree. At a vertex of `Delta`, the faces on one side form a fan between the two triangle edges. The fan alternates in colour and starts and ends with the common boundary colour, so it has odd length, and the cap makes the count even. So both pieces are Eulerian and properly coloured.

*Glue.* Solve the outer piece (containing `t0`) with `(t0, e0)`. In its cap both labels occur: an induced tree cannot contain a triangle. So exactly one cap edge `e1` is monochromatic. Solve the inner piece with root face its cap and prescribed edge `e1`, then rename its labels to agree on `Delta`. For each label, the two trees meet in the vertices of `Delta` with that label, which is one vertex or one edge with its two ends (a connected set). So their union is a tree. It is induced because no edge of `T` joins the strict interiors of the two sides, and on `Delta` the two pieces induce the same edges. The labels of `t0` and `e0` are unchanged. ∎

*Hamiltonian cycle.* Given the partition, every face of `T` has exactly one monochromatic edge (two would close a monochromatic triangle). The bichromatic edges dualise to a 2-regular spanning subgraph of `G` which is connected by complementary plane-tree duality (OpenAI Lemma 2.1), hence a Hamiltonian cycle avoiding `e0*`. See also Lemma 7.1 below.

---

## 6. Degree-4 expansion

**Lemma 6.1** (generation, `PROVED-HERE`). Let `T` be an Eulerian triangulation without separating triangles and `|V(T)| > 6`. Then `T` has a vertex `x` of degree 4, with neighbours `a, v1, b, v2` in rotation order, such that merging `v1` and `v2` (deleting `x`) or merging `a` and `b` gives a simple Eulerian triangulation with two fewer vertices.

*Proof.* A vertex of degree 4 exists: degrees are even and at least 4 (a degree-2 vertex is impossible in a simple triangulation on more than 3 vertices), and the average is below 6. Merging `v1, v2` changes degrees by `deg(v1) + deg(v2) - 4` at the new vertex and by `-2` at `a` and `b`. All stay even. The merge is simple unless `v1 ~ v2` or `v1, v2` have a common neighbour `c` outside `{a, b, x}`. If `v1 ~ v2`, the triangles `a v1 v2` and `b v1 v2` are faces (no separating triangles), which forces `deg(a) = 3`, impossible. If both merges fail, take `c` for `v1, v2` and `c'` for `a, b`. The 4-cycle `x v1 c v2` separates `a` from `b` locally at `x`, so the path `a c' b` meets it, forcing `c' = c`. Then `c` is adjacent to `a, v1, b, v2`, and the four triangles `c a v1, c v1 b, c b v2, c v2 a` are faces, so `T` is the octahedron. ∎

Hence every Eulerian triangulation arises from the octahedron by degree-4 insertions (the inverse merge) and by gluing two smaller ones along a face. `code/tri.py` uses exactly this. Its counts 1, 0, 1, 1, 2, 2, 8 for `V = 6..12` agree with an independent enumeration of all triangulations by flips (`code/flipcheck.py`; the total triangulation counts 2, 5, 14, 50, 233, 1249, 7595 are the known ones). Further counts: 8, 32, 57, 185 for `V = 13..16`.

**Lemma 6.2** (lift of states, `PROVED-HERE`; `COMPUTED` check `code/exp_lift.py`, `data/lift_13.txt`). Let `T'` arise from `T` by merging `v1, v2` into `v` at the degree-4 vertex `x` (with `x` not on `t0`). Let `beta_a, beta_b` be the two black faces at `x`, containing `a` and `b` respectively. Then:

(i) `pi: s -> s'` (forget `beta_a, beta_b`, rename `v1, v2 -> v`) is a bijection from the states of `T` with `s(beta_a), s(beta_b) ∉ {a, b}` onto the states of `T'`.

(ii) For such `s`, let `t*` be the old face with `s'(t*) = v`, let `v*` be its corner among `v1, v2` and `v_o` the other. The black face at `x` through `v*` takes `x`; call its `a/b`-corner `c2`. The other black face at `x` takes `v_o`; call its `a/b`-corner `c1`. Then

    Q_s = split(Q_{s'}) + {x c1} + {c2 v*},

where `split` renames each edge at `v` to `v1` or `v2` according to the side of its black face.

(iii) Hence `s` is a tree matching iff `s'` is, and `c2` lies in the component of `v_o` after splitting `v` in the spanning tree `Q_{s'} + {r0 r1, r1 r2}`.

*Proof.* (i) `x` is a corner only of the four faces at `x`, and each old face contains exactly one of `v1, v2` wherever `T'` had `v`. So `s'` is a state. Conversely, given `s'`, the old faces cover all nonroots except `x` and `v_o`. `v_o` is a corner of exactly one of `beta_a, beta_b` (each contains one of `v1, v2`), which must take it, and the other takes `x`. (ii) Read off the opposite edges. (iii) The edge `x c1` makes `x` a leaf. Splitting `v` in a spanning tree leaves two components, one containing `v1` and one containing `v2`. The edge `c2 v*` joins them iff `c2` is in the `v_o` component. ∎

`COMPUTED` (`code/exp_induction.py`, `data/induction_13.txt`): when `T'` has a tree matching, some tree matching of `T` always projects to one (all 1,516 such cases, `V <= 13`). But in 708 of these 1,516 cases some tree matching of `T'` does not lift (`P3` counts the 808 cases where all lift). The contraction can also create a black-inner separating triangle: 132 of 1,648 cases, first at `V = 11`. So degree-4 induction needs a boundary condition at the split vertex (part (iii)) that the induction hypothesis does not supply. That is where the step breaks.

---

## 7. Two induced trees versus tree matchings

**Lemma 7.1** (`PROVED-HERE`, standard). For a partition `V(T) = U ∪ U'` the following are equivalent:

(a) `U` and `U'` induce trees;

(b) no face of `T` is monochromatic, and `T[U]`, `T[U']` are connected;

(c) the bichromatic edges dualise to a Hamiltonian cycle of `G`.

*Proof.* If no face is monochromatic, every face has exactly one monochromatic edge, and every monochromatic edge is the monochromatic edge of both its faces. So there are `|F|/2 = |V| - 2` monochromatic edges. If both classes are connected they have at least `|U| - 1 + |U'| - 1 = |V| - 2` edges, hence exactly that many, so both are trees. Conversely, an induced tree contains no triangle. For (c): the bichromatic edges form an edge cut of `T`, whose dual is an even subgraph of `G`. It has degree 2 at every vertex of `G` iff every face of `T` is non-monochromatic. Its dual complement is the monochromatic forest, so it is connected iff that forest has exactly two components (OpenAI Lemma 2.1 and its converse). ∎

Fix `e0 ∈ t0`. Let `Part(e0)` be the partitions as in (a) with the ends of `e0` together and the third root apart. Let `construct(s)` be the construction of OpenAI §6.1–6.2.

**Theorem 7.2** (`PROVED-HERE`). Define `derive: Part(e0) -> ST` by: orient the forest `P_0 = P - e0` (`P` = monochromatic edges) towards the roots, and let `s(t)` be the tail of the unique `P_0`-edge in `t`. Then:

(i) `derive(U)` is a state for every `U ∈ Part(e0)`;

(ii) `derive(construct(s)) = s` for every tree matching `s`, so `construct` is injective;

(iii) the image of `construct` is `{U : derive(U) ∈ TM}`. Equivalently, it is the set of partitions whose *white parent map* is acyclic, where `par(z)` is the white face across the other side, at `s(t_z)`, of the black face `t_z` sharing `z`'s monochromatic edge.

*Proof.* (i) Removing `e0` from the two trees leaves three trees, each with one root, so orienting towards the roots gives out-degree 1 at nonroots and 0 at roots. Every black face in `A` has exactly one `P_0`-edge (`e0` belongs to `t0`), and every nonroot is the tail of exactly one `P_0`-edge, lying in exactly one face of `A`. So `s` is a bijection.

(ii) In `construct(s)`, the edge of `P_0` in `t` contains `s(t)` and is oriented away from it, which gives out-degree exactly 1 at nonroots. In a forest with one root per component, such an orientation is the orientation towards the roots. So `derive` reads `s` back.

(iii) If `U = construct(s)`, then `derive(U) = s ∈ TM`. Conversely let `s = derive(U) ∈ TM` with white tree `W_s`. Every white face `z != y0` has its monochromatic edge `e_z`, a side of the black face `t_z` across it, and `e_z ∋ s(t_z)`. The spoke `(t_z, s(t_z))` is dual to the `W_s`-edge joining `z` to `par(z)`. The map `z -> t_z` is a bijection from `W - {y0}` onto `A`, since each black face of `A` shares its unique monochromatic edge with exactly one white face, and that face is not `y0`, whose edge is `e0`. So the `n` edges of the tree `W_s` are assigned bijectively to the `n` non-root vertices, each to an incident edge. Orienting each edge away from its assigned vertex gives out-degree 1 off `y0`, which in a tree is the orientation towards `y0`. So `par` is the parent map of `W_s` rooted at `y0`. `construct` selects for `z` the side of `t_z` at `s(t_z)` bordering `z`, namely `e_z`. Hence `construct(s) = U`. The last sentence holds because `{z, par(z)}` are the duals of the spokes of `s`, and `s` is a tree matching iff these duals form a spanning tree of the white faces (OpenAI Lemma 2.1 and its converse), that is, iff `par` is acyclic. ∎

`COMPUTED` (`code/exp_induced.py`, `exp_induced2.py`; `data/induced_12.txt`, `data/induced2_12.txt`): `construct` is not onto. At `V = 8`, 4 of 12 rooted instances have 2 tree matchings but 4 partitions. Rooting at the other face through `e0` (colours swapped) does not cover the rest either: at `V = 12`, the two images together miss partitions for 118 of 209 edges. So the tree-matching certificate captures a proper, root-dependent part of the Hamiltonian cycles. Any route that works on partitions directly (decycling sets, Stein's B-sets) is aiming at a strictly larger target, which is easier to hit but harder to steer.

---

## 8. Why the strong descent lemma must fail

For a pair `(r, s)` let `f(x) = u(r^{-1}(x))` (the `Q_s` edge out of `x`, oriented by `r`), and `k(r, s)` the number of cycles of `f`. `k` depends only on `s` (it is the number of unicyclic components of `Q_s`, BT Prop. 2.1). A *D-swap* along a cycle `C` of `D(r,s)` exchanges `r` and `s` on the faces of `C`.

**Proposition 8.1** (`PROVED-HERE`). The statement "a D-swap along any `D`-cycle that meets a cycle of `f` strictly decreases `k`" is false whenever some pair `(r, s)` has `D(r,s)` a single cycle and both `Q_r` and `Q_s` contain cycles.

*Proof.* If `D(r,s)` is one cycle `C`, the swap along `C` produces `(s, r)`, whose `D` is again `C`. Every nonroot lies on `C`, so `C` meets every cycle of `Q_s` and of `Q_r`. The statement would give `k(s) > k(r)` and `k(r) > k(s)`. ∎

`COMPUTED`: such pairs exist (`data/strongviol_50_seed50.json`, `V = 50`, verified by `code/verify_trap.py`). The same file also shows the strong form failing in the D-Hamiltonian case. Exhaustively for `V <= 15` the strong form holds (`data/moves_13_15.txt`). The weak form (some swap under some mate decreases `k`) fails at `V = 50`: `data/deeptrap_50_1.json` is a 4-connected rooted triangulation with a pair with `k = 1` where all D-swaps under both mates give `k = 1`. Two swaps reach `k = 0` there.

---

## 9. Small remarks

**9.1 Grinberg is automatic** (`PROVED-HERE`). For a partition into two induced trees with `c` bichromatic edges (the Hamiltonian cycle has `c = |V(G)| = 2(n+1)` edges), `sum_{v in U} (deg v - 2) = 2(|U| - 1) + c - 2|U| = c - 2`, and the same for `U'`. So Grinberg's identity carries no information beyond "both sides are trees". In the Eulerian case it reads `sum_{v in U} (d_v - 1) = n` for each class.

**9.2 Black faces split as `|U| - 1` and `|U'| - 1`** (`PROVED-HERE`). Each black face has its monochromatic edge in `U` or in `U'`, and each edge of `T[U]` has exactly one black face. So exactly `|U| - 1` black faces have two corners in `U`, and likewise for white faces. Both colour classes "see" the two trees with the same multiplicities. This is the combinatorial shadow of the disk identity.
