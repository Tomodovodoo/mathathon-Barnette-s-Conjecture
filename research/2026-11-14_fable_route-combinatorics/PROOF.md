# A weight-free proof of Proposition 5.1, and why the signs are what they are

This file proves the heart of the argument, Proposition 5.1 of the OpenAI paper, in a form that needs no spoke weights, no exponential sum and no ordering of tokens. The test functions are heights of states at white faces, and the nonvanishing is the remark that a simple closed curve winds around every point inside it exactly once, never minus once.

The route is a cleaned-up version of the existing ones. Sections 1 to 3 are the proof. Section 4 explains the signs by an incidence determinant. Section 5 gives short proofs of the disk identity consequences used later in the paper, Lemma 6.2 included. Section 6 is a new statement about Hamiltonian cycles and states.

Status tags follow `research/BRIEF.md`. Every `COMPUTED` claim names its script in `lab/`.

## 0. Setting

Notation is the shared one. `T` is a simple sphere triangulation with faces properly coloured black and white. `t0` is the outer black face, `R` its three vertices (roots), `A` the other black faces, `X` the nonroot vertices, `|A| = |X| = n`. Every face other than `t0` is drawn counterclockwise.

A state is a bijection `s: A -> X` with `s(t)` a corner of `t`. A pair `(r, s)` is two states with `r(t) != s(t)` for all `t`. For a pair, `u(t)` is the third corner of `t`.

- `D(r, s)` is the set of directed edges `r(t) -> s(t)`.
- `Q_s` is the set of edges opposite `s(t)`. A partner `r` directs the edge of `Q_s` in `t` from `r(t)` to `u(t)`.
- `delta(v, w) = +1` if the black face of the edge `vw` is on the left of `v -> w`, and `-1` otherwise.

A tree matching is a state `s` that has a partner and whose `Q_s` is a forest. A forest pair is a pair `(r, s)` with `Q_s` a forest.

**Theorem A** (OpenAI Proposition 5.1). `PROVED-HERE`, and `LIT` in all three papers. If a pair exists, a forest pair exists.

**Theorem B** (signed height identity). `PROVED-HERE`. Let `m` be the least number of cycles of `D(r, s)` over all pairs. Let `eps(s)` be the sign of a tree matching (Lemma 3) and `h_s(w)` the height of `s` at an inner white face `w` (Section 2.3). For inner white faces `w_1, ..., w_j`:

```
sum over tree matchings s of  eps(s) h_s(w_1) ... h_s(w_j)
      =  0                                   if j < m,
      =  (-1)^((n-m)/2) N(w_1, ..., w_m)     if j = m,
```

where `N(w_1, ..., w_m)` is the number of ways to choose an undirected cycle cover `D` with exactly `m` cycles together with a bijection from `{1, ..., m}` to its cycles that sends each `i` to a cycle enclosing `w_i`.

Theorem A follows at once. Take a pair whose `D` has `m` cycles and pick `w_i` inside the `i`-th cycle. Then `N >= 1`, the left side is not an empty sum, and a tree matching exists.

`COMPUTED`: `lab/dets.py 12`, check D4, 1248 random choices of `(w_1, ..., w_j)` on all rooted triangulations with at most 12 vertices. The summed version with `omega(s) = sum_w h_s(w)` is asserted inside `lab/analyze.py` for all 5088 rooted triangulations with a pair and at most 16 vertices.

## 1. The disk identity says "one more white face"

**Lemma 1** (disk identity). `PROVED-HERE`; `LIT` OpenAI Lemma 4.1, with the same three counts arranged differently. Let `r` be a state. In each `t` in `A` choose one edge directed from `r(t)` to another corner of `t`. Let `C` be a simple directed cycle of chosen edges, of length `h`, and let `Disk` be the closed disk it bounds on the side away from `t0`. Write `B`, `W` for the numbers of black and white faces in `Disk`, and `l` for the number of edges of `C` whose black face lies in `Disk`. Then

```
W = B + 1,        (h - l) - l = 3.
```

So `C` has `delta`-sum `-3` if it is counterclockwise and `+3` if it is clockwise, and `h` is odd.

*Proof.* Only nonroots have outgoing chosen edges, so `C` avoids the roots. The roots are joined to each other by the sides of `t0`, which `C` does not use, so they lie outside `Disk`. All vertices in `Disk` are nonroots and all black faces in `Disk` belong to `A`. Let `I` be the number of vertices strictly inside.

*Count 1, `B = I + l`.* Send each black face `t` in `Disk` to `r(t)`. This is injective. Every interior vertex is hit, because the face matched to an interior vertex touches it and so lies in `Disk`. A vertex `v` on `C` has exactly one outgoing chosen edge, the edge of `C` leaving `v`, and that edge lies in the black face matched to `v`. So `v` is hit exactly when the edge of `C` leaving `v` has its black face inside. That happens `l` times.

*Count 2, edges.* Every edge has one black and one white face. The edges of `Disk` whose black face is in `Disk` number `3B`. The others are edges of `C` with the black face outside, and there are `h - l` of them. The same count with white faces gives

```
E = 3B + (h - l) = 3W + l.
```

*Count 3, Euler.* `(I + h) - E + (B + W) = 1`.

Put the first form of `E` into Euler's formula. The `h` cancels and `I + l - 2B + W = 1`. With Count 1 this is `W - B = 1`. Count 2 then gives `h - 2l = 3(W - B) = 3`.

Going counterclockwise, `Disk` is on the left, so an edge of `C` has `delta = +1` exactly when its black face is inside. The sum is `l - (h - l) = -3`. The clockwise sum is `+3`. Finally `h = 2l + 3` is odd. ∎

**What the lemma says.** A cycle made of state edges encloses exactly one more white face than black faces, and has three more boundary edges with white inside than with black inside. In the cubic graph `G` the cycle is a cut. Its inner side has one more white vertex than black vertices.

**Colours.** `LIT`, standard and usually attributed to Heawood. I did not open a source, so the attribution is unchecked. The proof is a propagation across edges, consistent around each vertex because degrees are even. An Eulerian triangulation of the sphere has a proper vertex colouring `col: V(T) -> Z/3` in which every black face reads `0, 1, 2` counterclockwise and every white face clockwise. Then `delta(v, w) = +1` exactly when `col(w) = col(v) + 1`. Along a closed walk the `delta`-sum is three times the number of times the colour runs around `Z/3`. So Lemma 1 says that the colour winds once backwards along a counterclockwise state cycle. `COMPUTED`: the colouring exists and agrees with `delta` on every triangulation with at most 12 vertices (`lab/dets.py`, check D3 depends on it).

This answers the question of what `J` is. For a pair,

```
J(r, s) = (1/3) sum_t delta(r(t), s(t)) = #clockwise cycles of D - #counterclockwise cycles of D.
```

It is the total colour winding of `D`, and it is minus the turning number of `D` as an oriented family of disjoint simple closed curves. `PROVED-HERE` by Lemma 1.

## 2. Two families of cubes

### 2.1 Pairs with the same cycles

Let `(r, s)` be a pair. Each nonroot is `r(t)` for one `t` and `s(t')` for one `t'`, so `D(r, s)` is a set of disjoint directed cycles covering `X`. Distinct black faces supply distinct edges of `T`, so no cycle has length two and every cycle is a simple cycle of `T`. It consists of edges chosen from `r`, so Lemma 1 applies to it. Let `c(r, s)` be the number of cycles. Their lengths are odd and add up to `n`, so `c = n mod 2`. Also `J = c mod 2`. Put

```
eps(r, s) = (-1)^((n + J(r, s)) / 2).
```

Reversing one cycle `C` of `D` means exchanging `r(t)` and `s(t)` on the faces that supply `C`. Both new maps are bijections, because the tails and the heads of `C` are the same vertex set. The result is a pair with the same undirected edges. `J` changes by `2` or `-2`, so `eps` changes sign.

The `2^c` pairs with a given undirected cycle cover `D` form the cube of `D`. Index them by `o` in `{+, -}^cycles`, where `o_C = +` means that `C` runs counterclockwise. With `p(o)` the number of plus signs, `J = c - 2p`, hence

```
eps(r_o, s_o) = (-1)^((n + c) / 2) (-1)^p(o).                         (2.1)
```

### 2.2 Partners of a fixed second state

**Lemma 2** (`LIT`: trees paper, Proposition 2.1; proof repeated because Section 6 uses it). Let `s` be a state. Its partners correspond to the orientations of `Q_s` with outdegree one at every nonroot and zero at every root, by letting `r(t)` be the tail of the edge of `Q_s` in `t`. If `s` has a partner, every component of `Q_s` is a tree with exactly one root or a unicyclic graph with no root. With `k` unicyclic components there are exactly `2^k` partners.

*Proof.* The tail of the edge in `t` is a corner other than `s(t)`, and the tails form a bijection onto `X` exactly when the outdegrees are as stated. A component with `v` vertices and `a` roots then has `v - a` edges. Being connected it has at least `v - 1`, so `a <= 1`. If `a = 1` it is a tree and all edges point to the root. If `a = 0` it has one cycle, which can run either way, and the rest points to the cycle. ∎

If `Q_s` has a cycle `K`, a partner `r` directs it. Reversing `K` gives the partner `r'` with `r'(t) = u(t)` on the faces supplying `K`. In such a face

```
delta(u, s) - delta(r, s) = 2 delta(r, u),
```

which one checks on the two cyclic positions of `(r, u, s)`. The edges `r(t) -> u(t)` of `K` are chosen from `r`, so Lemma 1 gives `J(r', s) - J(r, s) = (2/3)(-3 or +3)`, that is `-2` or `+2`. So `eps(r', s) = -eps(r, s)`.

**Lemma 3** (cancellation; `LIT` OpenAI Lemma 5.2). `PROVED-HERE`. For a state `s` put `mu(s) = sum over partners r of eps(r, s)`. Then `mu(s) = 0` unless `s` is a tree matching. A tree matching has exactly one partner `r_s`, and `mu(s) = eps(r_s, s) =: eps(s)`.

*Proof.* If `Q_s` has a cycle, fix one, using `s` only. Reversing it is a fixed-point-free involution on the partners of `s` that changes the sign. If `Q_s` is a forest and `s` has a partner, Lemma 2 with `k = 0` gives one partner. ∎

So the partners of `s` form a second kind of cube, of dimension `k(s)`, and `eps` alternates on it too. Tree matchings are the cubes of dimension zero.

### 2.3 Heights

Put a centre in each face of `A` and join it to its three corners by spokes. An inner white face is a white face that shares no edge with `t0`. There are `n - 2` of them.

For each inner white face `w` fix a path `gamma_w` in the plane from a point of `w` to a point of `t0`. It avoids vertices and centres and crosses spokes transversally. For a spoke `(t, v)` let `kappa_w(t, v)` be the number of times the spoke, directed from the centre to `v`, crosses `gamma_w` from right to left, minus the number of times from left to right. The height of a state at `w` is

```
h_s(w) = sum over t in A of kappa_w(t, s(t)).
```

For a directed cycle `C` of some `D(r, s)`, the spoke detour of `C` replaces each edge `r(t) -> s(t)` by the route `r(t) -> centre of t -> s(t)`. Different edges of `C` come from different black faces, so the detour is again a simple closed curve. It differs from `C` only inside black faces. Hence a white face lies inside the detour exactly when it lies inside `C`, and the detour has the orientation of `C`. (The second point is the sliding argument of OpenAI Section 5.3: each edge is pushed across a third of its black triangle, which contains no vertex.) Write `In(C)` for the set of white faces inside `C`. By Lemma 1,

```
|In(C)| = W = B + 1 >= 1.                                             (2.2)
```

All faces in `In(C)` are inner, because white faces next to `t0` contain a root and roots lie outside `C`.

**Lemma 4** (heights on a cube). `PROVED-HERE`. Let `D` be an undirected cycle cover coming from a pair, and `s_o` the second state of its orientation `o`. For every inner white face `w`,

```
h_{s_o}(w) = h_{s_-}(w) + #{ C : o_C = + and w in In(C) },
```

where `s_-` belongs to the all-clockwise orientation.

*Proof.* Let `o` and `o'` differ only on `C`, with `o_C = +`. The states `s_o` and `s_o'` agree off `C`. On a face `t` supplying `C`, `s_o(t)` is the counterclockwise head and `s_o'(t)` the counterclockwise tail. So `h_{s_o}(w) - h_{s_o'}(w)` is the signed number of crossings of `gamma_w` by the counterclockwise detour of `C`. A counterclockwise simple closed curve crosses a path from `p` to `q` with signed count `[p inside] - [q inside]`, in the right-to-left convention. Here `p` is in `w` and `q` in `t0`, which is outside. The difference is `1` if `w` is in `In(C)` and `0` otherwise. ∎

Summing over `w` gives a rank function `omega(s) = sum_w h_s(w)`. Up to an additive constant it is the function `omega` of the OpenAI paper for the circulation of its Lemma 5.3, and `L+(C) - L-(C) = |In(C)|`. `COMPUTED`: `lab/analyze.py` asserts `L+ - L- = |In(C)| >= 1` for every cycle of every `D` up to 12 vertices, with the enclosed faces found by an independent flood fill.

So the weights of the OpenAI paper have a plain meaning. The exponent `omega(s)` is the volume under the height function of `s`, and the inequality `L+ > L-` says that a cycle has white faces inside it.

## 3. Proof of Theorem B

Let `F(s) = h_s(w_1) ... h_s(w_j)`. Sum `eps(r, s) F(s)` over all pairs in two ways.

*By the second state.* The sum is `sum_s F(s) mu(s)`. By Lemma 3 it equals the sum over tree matchings of `eps(s) F(s)`. This is the left side of Theorem B.

*By the cycle cover.* Fix `D` with cycles `C_1, ..., C_c`. Write `b_i = h_{s_-}(w_i)` and `1_C(w) = 1` if `w` is in `In(C)`, else `0`. By (2.1) and Lemma 4 the cube of `D` contributes

```
(-1)^((n+c)/2)  sum over o of  (-1)^p(o)  prod_{i=1..j} ( b_i + sum_{C : o_C = +} 1_C(w_i) ).
```

Expand the product. A term chooses a subset `I` of `{1, ..., j}` and a map `phi` from `I` to the cycles, and equals `prod_{i not in I} b_i prod_{i in I} 1_{phi(i)}(w_i)`. It occurs for exactly those `o` that are `+` on the image of `phi`. The signed number of such `o` is

```
(-1)^|image|  prod over cycles C not in the image of (1 - 1),
```

which is zero unless `phi` is onto, and `(-1)^c` if it is onto. A map from a subset of `{1, ..., j}` onto `c` cycles needs `j >= c`. If `j < c` the cube contributes nothing. If `j = c`, then `I` is everything, `phi` is a bijection `beta`, and the cube contributes

```
(-1)^((n+c)/2) (-1)^c  #{ bijections beta with w_i in In(beta(i)) for all i }
   = (-1)^((n-c)/2)  #{ ... }.
```

Now let `m` be the least `c`. For `j < m` every cube contributes zero. For `j = m` the cubes with more than `m` cycles contribute zero and the cubes with exactly `m` cycles contribute `(-1)^((n-m)/2)` times a nonnegative integer. Their sum is `(-1)^((n-m)/2) N(w_1, ..., w_m)`. ∎

**Proof of Theorem A.** Let `D*` be a cycle cover with `m` cycles `C_1, ..., C_m`. By (2.2) pick `w_i` in `In(C_i)`. The identity bijection is counted in `N`, so `N >= 1`. The left side of Theorem B is then a nonzero sum over tree matchings, so there is a tree matching `s`, and `(r_s, s)` is a forest pair. ∎

**Where each hypothesis is used.** Planarity enters twice. Lemma 1 makes both kinds of cycle reversal change the sign. The fact that every cycle has an inside, entered with sign `+1` by every enclosing counterclockwise cycle, makes all minimal cubes contribute with the same sign. The minimum over `c` is needed because cubes whose cycle numbers differ by two have opposite leading signs.

**What the identity says.** The signed measure `sum eps(s) delta_s` on tree matchings is a sum, over cycle covers `D`, of `c(D)`-fold differences in the directions `1_C >= 0`. It kills every polynomial of degree less than `m` in the heights. On a product of `m` heights it gives a count. The three published proofs test it against `exp(x omega)` (OpenAI), against `omega^m` written as lists of `m` tokens (trees paper), and against crossings of a vertical ray (Li). The product of heights at chosen faces is the simplest test function that works.

**Corollaries.** `PROVED-HERE`.

1. Tree matchings of sign `+1` and `-1` are equally many (`j = 0 < m`). This is in the trees paper, Theorem 5.2.
2. `sum over tree matchings of eps(s) omega(s)^j` is `0` for `j < m` and `(-1)^((n-m)/2) m! sum over D with m cycles of prod_C |In(C)|` for `j = m`. Sum Theorem B over all `(w_1, ..., w_j)`.
3. The number of tree matchings is at least `2m`. *Proof.* Let `P` and `M` be the multisets of values `omega(s)` over tree matchings of sign `+1` and `-1`. By Corollary 2 they have the same power sums of degrees `0, ..., m-1`, so the same size `N`. If `N <= m - 1`, Newton's identities give equal elementary symmetric functions, so `P = M` as multisets, and then all power sums agree. This contradicts the nonzero `m`-th moment. So `N >= m`. ∎

`CONJECTURE`: the number of tree matchings is at least `2^m`. Test: any rooted triangulation with a pair and fewer than `2^cmin` tree matchings refutes it. `COMPUTED` true for all 5088 rooted triangulations with a pair up to 16 vertices (`lab/survey.py 16`, line E7), with equality in 4609 of them.

## 4. The signs are determinant signs

This section explains Lemma 3 by linear algebra. It is not needed for Theorem A.

Let `zeta = exp(i pi / 6)`, so that `i^J(r,s) = prod_t zeta^delta(r(t), s(t))`. Let `sigma` be the permutation sign of a state, as a bijection between the ordered sets `A` and `X`. All states have the same sign (`LIT`: trees paper Lemma 6.1; the proof is Lemma 1, since two states differ by a permutation with odd cycles). `COMPUTED` in `lab/analyze.py` for every rooted triangulation up to 16 vertices.

For a state `s` let `N_s` be the `n x n` matrix with rows `A` and columns `X`,

```
N_s(t, x) = zeta^delta(x, s(t))   if x is a nonroot corner of t other than s(t),   0 otherwise.
```

**Proposition 5** (twisted incidence matrix). `PROVED-HERE`.

1. `sum over partners r of i^J(r,s) = sigma det N_s`.
2. Let `col` be the vertex colouring of Section 1, `omega3 = exp(2 pi i / 3)`, and `Omega = diag(omega3^col(x))`. Then `N_s Omega = diag(rho) d_s`, where `d_s` is the ordinary signed incidence matrix of `Q_s` with the three root columns deleted (row `t` is `e_x - e_y` for the edge `xy` of `Q_s` in `t`, with `col(x) = col(s(t)) + 1`), and every `rho_t` has modulus one.
3. Hence `|det N_s| = 1` if `s` is a tree matching and `det N_s = 0` otherwise.

*Proof.* (1) Expand the determinant over bijections `r: A -> X`. A term is nonzero exactly when `r(t)` is a corner of `t` other than `s(t)` for all `t`, that is, when `r` is a partner. Its sign is `sigma`.

(2) For adjacent `v, w` one has `zeta^delta(v, w) = (1 - omega3^(col v - col w)) / sqrt 3`. Check: if `col w = col v + 1` then `delta = 1` and `(1 - omega3^-1)/sqrt 3 = zeta`; the other case is the conjugate. Let the corners of `t` be `s(t), x, y` with colours `a, a+1, a+2`. Row `t` of `N_s` is `((1 - omega3) e_x + (1 - omega3^2) e_y) / sqrt 3`. Since `(1 - omega3^2)/(1 - omega3) = -omega3^2`, row `t` of `N_s Omega` is

```
((1 - omega3)/sqrt 3) omega3^(a+1) ( e_x - omega3^2 omega3 e_y ) = rho_t (e_x - e_y),
```

with `|rho_t| = 1`. Root columns are absent from both sides.

(3) Contract the three roots to one vertex. `d_s` is the incidence matrix of `n` edges on `n + 1` vertices with one column deleted. By the standard lemma behind the matrix-tree theorem its determinant is `+1` or `-1` if the edges form a spanning tree of the contracted graph, and `0` otherwise. The edges of `Q_s` form such a tree exactly when `Q_s` is a forest with one root in each component. By Lemma 2 that is the same as being a tree matching. ∎

So the cancellation of Lemma 3 is the linear dependence of the rows of an incidence matrix along a cycle, and `eps(r, s)` is, up to a factor that depends on `s` only, the sign of the term of `r` in the expansion of `det d_s`. The disk identity is used once, to know that all states have the same permutation sign. The colouring does the rest.

`COMPUTED`: `lab/dets.py 12`, check D1, 1706 states: `det N_s = sigma sum_r zeta^(3J)` and `|det N_s|` is `1` on tree matchings and `0` elsewhere.

**Two closed formulas for the whole sum.** Let `g` be any function on incidences and `g(s) = prod_t g_t(s(t))`.

*Magnetic adjacency matrix.* `PROVED-HERE`. Let `AA(x)` be the `X x X` matrix with `AA(v, w) = x_t zeta^delta(v, w) g_t(w)` when `v, w` are adjacent nonroots and `t` is the black face of `vw`, and zero otherwise. Then

```
sum over pairs of i^J(r,s) g(s)  =  coefficient of x_1 x_2 ... x_n in det AA(x).
```

*Proof.* A term of the determinant is a permutation `pi` of `X` moving each `v` along an edge. Its monomial is multilinear exactly when the `n` edges lie in `n` distinct black faces. Then tails and heads define a pair with `D = pi`, and every pair arises once. The cycles of `pi` are cycles of `D`, of odd length by Lemma 1, so `sgn(pi) = 1`. ∎

For `g = 1` the matrix is Hermitian. Its phases put flux `+pi/2` through every black face and `-pi/2` through every white face.

*Fourier expansion.* `PROVED-HERE`. With `col_S(s) = sum_{t in S} col(s(t))`,

```
sum over pairs of i^J(r,s) g(s)
   = 3^(-n/2) sum over subsets S of A of (-1)^|S| ( sum_r omega3^col_S(r) ) ( sum_s g(s) omega3^(-col_S(s)) ),
```

both inner sums over all states. *Proof.* `prod_t (1 - omega3^(col r(t) - col s(t))) / sqrt 3` equals `i^J(r,s)` on pairs and vanishes when `r(t) = s(t)` for some `t`. Expand the product. ∎

`COMPUTED`: `lab/dets.py 12`, checks D2 and D3, 262 rooted triangulations with `n <= 10`, with `g_t(w) = 1.3^a(t,w)`.

**Gap.** I did not find a proof of nonvanishing from either formula. The Fourier formula at `g = 1` reads `sum_S (-1)^|S| |chi_S|^2 = 0`, a statement about character sums over states that I cannot use. The proof of nonvanishing in this file is the one in Section 3.

**A side remark that shows where the difficulty sits.** Proposition 5 never uses that `s` is a bijection. For any choice function `c` (one corner per face of `A`, roots allowed, repetitions allowed) the same proof gives `sum over states r disjoint from c of prod zeta^delta(r(t), c(t)) = sigma (unit) det d_c`, and `det d_c != 0` exactly when `Q_c` is a forest with one root per component. Summing over all `c` gives `(#states) 3^(n/2) != 0`. So a single state already yields a choice function whose `Q_c` is a rooted forest. That is easy and useless. Theorem A is the statement that `c` can be taken injective, and injectivity is what the later steps (Lemma 6.2) need. The whole difficulty of Proposition 5.1 is the second bijection.

## 5. Lemma 6.2 in two lines

Setting of OpenAI Section 6.2: `s` is a tree matching, `P` is a set of edges with exactly one edge in every face, black and white, the edge of `P` in `t` in `A` is incident with `s(t)`, and `P0 = P - e0` is directed out of `s(t)`.

**Lemma 6** (`LIT`: OpenAI Lemma 6.2). `PROVED-HERE`. `P0` has no cycle.

*Proof.* Every nonroot has outdegree one in `P0`, so a cycle `C` would be directed, and its edges are chosen from the state `s`. Lemma 1 gives `W = B + 1` and `(h - l) - l = 3` for its disk. Since `P` has one edge in each face and each edge lies in one black and one white face, `P` pairs black faces with white faces. A face in the disk is paired inside the disk unless its edge of `P` is on `C`. All `h` edges of `C` are in `P`, with `l` black and `h - l` white faces on the inner side. So `B - l = W - (h - l)`, that is `W - B = 3`. But `W - B = 1`. ∎

In words: a state cycle has one more white face inside and three more white faces along its inner boundary, and a face pairing cannot absorb both.

## 6. Hamiltonian cycles give states, and tree matchings are the ones with a partner

Let `G = T*`, and let `e0` be an edge of `t0`. A Hamiltonian cycle `C` of `G` that avoids the dual of `e0` leaves a set `P` of uncrossed edges of `T`, one in every face, with `e0` in `P`. The graph `(V(T), P)` is two trees, one on each side of `C` (`LIT`: Stein; Alt, Payne, Schmidt, Wood, Lemma 5, as used in OpenAI Section 6.2). The other two sides of `t0` are crossed, so `P0 = P - e0` is a forest with exactly one root in each of its three components. Direct `P0` towards the roots and let `s_C(t)` be the tail of the edge of `P` in `t`. Each nonroot is a tail once and the `n` edges lie in the `n` faces of `A`, so `s_C` is a state.

**Proposition 7.** `PROVED-HERE`.

1. For a tree matching `s`, the cycle `C(s)` built in OpenAI Section 6 satisfies `s_{C(s)} = s`. So `s -> C(s)` is injective, and the number of tree matchings is at most the number of Hamiltonian cycles of `G` avoiding any one of the three edges at the vertex `t0*`. In particular `3 #(tree matchings) <= #(Hamiltonian cycles of G)`.
2. For every Hamiltonian cycle `C` avoiding `e0*`, the state `s_C` is either a tree matching, and then `C = C(s_C)`, or it has no partner at all.

So among the states that come from Hamiltonian cycles, the tree matchings are exactly those with a partner.

*Proof.* (1) In the construction, the edge of `P` in `t` is incident with `s(t)`, and `P0` directed out of `s(t)` has outdegree one at nonroots and zero at roots. In a forest with one root per component that is the orientation towards the roots. So `s_{C(s)} = s`.

(2) Write `s = s_C`. Let `W_s` be the graph on the white faces with one edge for each `t` in `A`, joining the two white faces across the sides of `t` at `s(t)`. Then `s` is a tree matching exactly when `W_s` is a tree (`LIT`: OpenAI Section 6.1 and trees paper (3): `W_s` is the plane dual of the deleted spokes, and `H - s` is a tree exactly when `Q_s` is a forest with one root per component).

Suppose `W_s` is a tree. Both `P` and the set built in the construction contain `e0` and one side at `s(t)` for each `t`, and both pair black with white faces. Such a pairing matches each `t` with an end of its edge in `W_s`, uses every white face except `y0` once, and does not use `y0`. On a tree rooted at `y0` there is one such choice. So `C = C(s)`.

Suppose `W_s` is not a tree. It has `n` edges on `n + 1` vertices, so it contains a cycle through white faces `w_1, ..., w_k` and black faces `t_1, ..., t_k`. Draw it as a simple closed curve `Gamma` that crosses exactly the two sides of each `t_i` at `s(t_i)`. `Gamma` crosses no side of `t0`, so the roots lie on one side, the outside. Let `S` be the set of vertices inside, `sigma = |S|`. Let `B_in` and `W_in` count the faces strictly inside, and let `a` be the number of `i` with `s(t_i)` inside.

*No edge of `Q_s` crosses `Gamma`.* The crossed edges are sides at `s(t_i)`. The edge of `Q_s` in `t_i` is the opposite side.

*`B_in = W_in`.* The edge of `P` in `t_i` is a side at `s(t_i)`, so it is crossed by `Gamma` and pairs `t_i` with a white face on `Gamma`. The `k` black faces on `Gamma` are thus paired with the `k` white faces on `Gamma`. A black face strictly inside is then paired with a white face that is not on `Gamma` and shares an uncrossed edge with it, so strictly inside. The same holds from the white side.

*Edges inside.* An edge with both ends in `S` has its black face strictly inside or equal to a `t_i` with `s(t_i)` outside. So there are `3 B_in + (k - a)` of them, and the same count from the white side is `3 W_in + c'` for some `c'`.

*Euler.* The disk inside `Gamma` is cut into `B_in + W_in` triangles and `2k` pieces of the faces on `Gamma`. With the `2k` crossing points as extra vertices, Euler's formula on the sphere reads

```
(sigma + 2k) - (e(S) + 2k + 2k) + (B_in + W_in + 2k + 1) = 2,
```

so `sigma = e(S) - B_in - W_in + 1 = B_in + (k - a) + 1`.

*Count of `Q_s`.* The edges of `Q_s` with both ends in `S` come from the `B_in` faces strictly inside and from the `k - a` faces `t_i` with `s(t_i)` outside. That is `sigma - 1` edges.

So `Q_s` has `sigma - 1` edges on the `sigma` vertices of `S`, no edge leaving `S`, and no root in `S`. If `s` had a partner, Lemma 2 would make every component inside `S` unicyclic, with as many edges as vertices, `sigma` in total. So `s` has no partner. ∎

`COMPUTED`: `lab/survey.py 16`, lines E8, E8b, E8c. On all 5088 rooted triangulations with a pair up to 16 vertices and all three choices of `e0`, the map `s -> C(s)` is injective with inverse `C -> s_C`, and each of the 176726 Hamiltonian cycles that is not of the form `C(s)` gives a state with no partner. The cycle to state map itself is not injective in general (`lab/zpoly.py 15`, line Z3, first failure at 8 vertices).

**Reading.** Proposition 5.1 can be restated without pairs of cycle covers: if the rooted triangulation has two disjoint states, then some Hamiltonian cycle of `G` avoiding `e0*` has a state `s_C` with a partner. Most Hamiltonian cycles are not of this kind. In the data the number of cycles avoiding one edge at `t0*` is between `1` and `26` times the number of tree matchings.

## 7. What is proved here and what is only computed

| Statement | Status |
| --- | --- |
| Lemma 1 (disk identity as `W = B + 1`) | `PROVED-HERE`, `LIT` |
| `J` = clockwise minus counterclockwise cycles = colour winding | `PROVED-HERE` given the 3-colouring (`LIT`, proof not written here) |
| Lemmas 2, 3, 4 | `PROVED-HERE` |
| Theorem B and Theorem A | `PROVED-HERE`; one step cites the sliding argument of OpenAI Section 5.3 for "the detour has the orientation of the cycle" |
| Corollaries 1 to 3 (`#tree matchings >= 2 cmin`) | `PROVED-HERE` |
| `#tree matchings >= 2^cmin` | `CONJECTURE`, `COMPUTED` up to 16 vertices |
| Proposition 5 and the two closed formulas | `PROVED-HERE`, `COMPUTED` up to 12 vertices |
| Nonvanishing from the determinant formulas | open, no proof found |
| Lemma 6 | `PROVED-HERE`, `LIT` |
| Proposition 7 | `PROVED-HERE`, `COMPUTED` up to 16 vertices; cites the two-trees fact and the dual-tree equivalences as `LIT` |

None of this has been refereed. The proofs are short, and the computations check their conclusions on 7868 rooted triangulations, but an independent reader should go through Sections 3 and 6 before anything here is promoted.
