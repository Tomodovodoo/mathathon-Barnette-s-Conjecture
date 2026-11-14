# The two-tree packing statement: precise form, status, relationships

Opus 5.5, 2026-11-14. Notation as in `research/BRIEF.md`, plus `H` (all spokes, including those of `t0`), `W` (the white-face graph, plane dual of `H`; the spoke `(t, v)` is the edge joining the two white faces across the sides of `t` at `v`), and `T/R` (roots identified). Full proofs are in `PROOFS.md`; the referee verdicts on the probabilistic folder are in `REFEREE.md`.

## 1. The statement, and what it does and does not give

The probabilistic folder (`2026-11-14_sol_route-probabilistic`, ROUTES.md) conjectured:

> For every rooted instance with a pair `(r, s)`, the `2n` edges of `W` dual to the spokes of `r ∪ s` split into two spanning trees of `W`.

It is true, and stronger statements are true.

| Statement | Status | Where |
| --- | --- | --- |
| The half-pair conjecture above | `PROVED-HERE` | PROOFS Thm 2.1 |
| The same for **every** deleted-corner map `u` (any choice of one corner `u(t)` per `t ∈ A`, not necessarily from a pair), whenever a pair exists in the instance | `PROVED-HERE` | PROOFS Thm 2.1 |
| Without a pair it fails for some `u`: exactly the maps that delete a triangle corner in all three inner faces along some black-inner separating triangle fail ("if" proved; "only if" computed) | `PROVED-HERE` (if), `COMPUTED` (only if: 5,440 random maps on 136 rooted instances, `code/big.py`) | PROOFS Prop 2.3 |
| Every `y` with face sums 1 and `0 <= y <= 1/2` on bounded spokes is in the spanning-tree polytope of `W` | `PROVED-HERE` | PROOFS Thm 2.5 |
| `W` minus the triangle of `t0` is three spanning trees | `PROVED-HERE` with a pair; `COMPUTED` without (all rootings `V <= 17`) | PROOFS Cor 2.6 |
| `T`-side: `E(T) - E(t0) - D_u` is two spanning trees of `T/R`; for a pair, `Q_r ∪ Q_s` re-splits into two root-separating forests | `PROVED-HERE` | PROOFS Thm 2.7 |
| Inside every pair support: a face-rainbow tree and a point-rainbow tree | `PROVED-HERE` (Rado) | PROOFS Cor 3.2 |
| Every pair support splits into two **point**-rainbow trees | `PROVED-HERE` (Edmonds' branching theorem) | PROOFS Thm 3.3 |
| Every pair support splits into two **face**-rainbow trees (P2) | `CONJECTURE`; `COMPUTED` on all 14,881 supports, `V <= 17` | PROOFS Conj 3.4 |
| Every pair support contains a tree matching | `REFUTED` at `V = 16` (bad cover, plantri index 27, outer face 0 in my numbering) | `data/census_V16-17.json` |

What the packing theorem implies.

- **Not a tree matching.** It says nothing about states. The bijection property of `r` and `s` is never used: the theorem holds for all `3^n` deleted-corner maps. A tree matching is a spanning tree of `W` that is rainbow for both the face partition and the point partition; the two trees produced by the packing are in general rainbow for neither.
- **Not a tree pair.** A split of `r ∪ s` into `E_r` and `E_s` themselves would make both states tree matchings. That fails for some supports (239 of 9,290 at `V = 17`).
- **Fractional feasibility of the three-matroid LP, sign-free.** The point `(1/2)(1_r + 1_s)` lies in the tree polytope of `W` and has all face and point sums equal to one. So the natural LP (tree polytope ∩ perfect-matching polytope of `B`) is nonempty whenever a pair exists. Before this, that followed only from the existence of a tree matching, which is the signed theorem. The LP is not integral (graph-theory ROUTES M1–M4, half-integral vertex at `V = 13`), so this does not round.
- **Not a necessary condition for anything.** It is a property of every pair (indeed of every deleted-corner map) and carries no information that distinguishes good pairs from bad ones.

## 2. Why it is true: the density bound is a Nash-Williams condition

OpenAI (3.2), `e(U) - b(U) <= 2|U| - 4` for `U ⊇ R`, is the Hall condition for a 2-factor of `B`, rewritten. Its left side is `Σ_t max(0, j_t - 1)` over black faces, where `j_t` counts corners of `t` in `U`; that is the sum over black faces of the graphic rank of the face's edges inside `U`.

The brief asked whether (3.2) is a two-forest condition in disguise. It is, after one extension. PROOFS Lemma 1.2 extends (3.2) to **all** nonempty `U`:

    e(U) - b(U) + max(0, |U ∩ R| - 1) <= 2|U| - 2,

under the same hypothesis (no black-inner separating triangle, equivalently a pair exists). The proof is the refereed Euler identity plus a component count; the only new case is a component that holds two roots and has `t0` in a triangular region.

The Nash-Williams covering condition for two forests in the multigraph `M_u` (the doubled spokes `(t, u(t))` and spokes of `t0`, plus the support of `u` once) reduces, after optimising which black centres to include, to `Σ_t max(0, μ_t - 2) <= 2|U| - 2`. Each term is at most the shortfall `max(0, j_t - 1)`:

| corners of `t` in `U` | Nash-Williams term | shortfall |
| --- | --- | --- |
| all three | 2 | 2 |
| two, including `u(t)` | 1 | 1 |
| two, not `u(t)` | 0 | 1 |
| at most one | 0 | 0 |

So the extended (3.2) **is** the two-forest condition, with slack exactly at the faces whose two corners in `U` are the two used ones. The same table appears three times: in `H` (Theorem 2.1), in `T/R` (Theorem 2.7), and in the digraph `G_u` for Edmonds' branching theorem (Theorem 3.3). One count, three matroids.

The slack is lost precisely at a separating triangle with black inner boundary. Its outside `U` has `e(U) - b(U) = 2|U| - 3`, one too many, and a map `u` fails iff it uses no interior corner on the three inner faces along the triangle (PROOFS Prop 2.3). That is the same triangle that blocks the pair. A deleted-corner map that comes from a pair can never be in this position, because pairs do not exist there.

## 3. A pair as a decomposition of `E(T)`

PROOFS Prop 4.1 (`PROVED-HERE`, a two-line check). In each `t ∈ A` the three edges are: opposite `s(t)` (in `Q_s`), opposite `r(t)` (in `Q_r`), and `r(t)s(t)` (in `D`). So

    E(T) - E(t0) = Q_r ⊔ Q_s ⊔ D,

each part a transversal of the bounded black faces, `D` 2-regular on `X`. The brief's guess is right, with one correction: the forests that the packing produces live in `T/R` and are not transversal. Theorem 2.7 says that `Q_r ∪ Q_s` always re-splits into two spanning trees of `T/R` (two spanning forests of `T` with one root per component). The key lemma asks for some pair where one of the two transversal parts, `Q_s`, is already such a forest. The packing gives the non-transversal version for free and cannot see the transversal one.

**Schnyder woods and arboricity.** `T` minus the edges of `t0` has `3n` edges and is three trees: that is Schnyder's theorem (`LIT`, W. Schnyder, Order 5 (1989); cited from memory). PROOFS Prop 4.2 shows that a pair is a special 3-orientation of `E(T) - E(t0)`: orient `r(t) -> s(t)`, `r(t) -> u(t)`, `s(t) -> u(t)` in each `t ∈ A`. Every nonroot gets out-degree 3, every root 0, and every bounded black triangle is transitive with sink `u(t)`. Conversely such an orientation with no nonroot being the middle of three faces is exactly a pair. By de Fraysseix and Ossona de Mendez (`LIT`, Discrete Math. 229 (2001); cited from memory) every 3-orientation is a Schnyder wood, so every pair determines a Schnyder wood. Its colour classes are cut by the cyclic order of out-edges at each vertex, not by black faces, and are not `Q_r, Q_s, D`. On the white side, Corollary 2.6 is the analogue of Schnyder's three trees for `W`: `W` minus the triangle of `t0` is three spanning trees.

**The three bipartite colour-pair graphs.** Let `1, 2, 3` colour the vertices of `T`. The edge of `t` opposite `v` joins the two colours other than `c(v)`, so `Q_s ∩ T_{ab}` is dual to the spokes of `s` at vertices of the third colour, that is, to the `W`-edges of colour `c`. Each black triangle is rainbow in `W`, and each vertex face of `W` is monochromatic. The topology folder (TOPOLOGY §4.3, Kálmán, Tutte's tree trinity) shows that `T_{ab} - Q_s` is a spanning tree of `T_{ab}` for every state. Neither fact interacts with the packing: Theorem 2.1 holds for all deleted-corner maps, and the colour of `u(t)` plays no role in its count. I did not find a use of the 3-colouring that would select a good pair.

**Matroid union, Edmonds' branchings and what each handles.**

| Tool | What it proves here |
| --- | --- |
| Matroid union / Nash-Williams (`k = 2`) | pair supports, and all supports of deleted-corner maps, are two `W`-trees (Thm 2.1) and two `T/R`-trees (Thm 2.7) |
| Nash-Williams (`k = 3`) | `W - Δ_{t0}` is three trees (Cor 2.6) |
| Rado / two-matroid intersection | a face-rainbow and a point-rainbow tree inside every support (Cor 3.2) |
| Edmonds' disjoint branchings | every support splits into two point-rainbow trees (Thm 3.3) |
| none | a tree that is rainbow for faces **and** points (the key lemma) |

The earlier verdict "three matroids, not two" (graph-theory PROOFS §1, referee INTEGRATION §7) stands. Within a fixed support `F`, the face blocks and the point blocks together form the alternating cycles of the 2-factor, and a doubly rainbow choice is one of the `2^c` alternating halves, a state of the `D`-group. Each one-sided constraint is a matroid intersection and is always solvable inside `F`; the alternating one is not a matroid condition and can fail for a fixed `F` (the `V = 16` bad cover). So the extra argument must move between 2-factors. Two places where the disk identity could enter: fable's Lemma X2 (surplus inside an exchange cycle) and the `Q`-cycle reversal, which changes the 2-factor. The packing statements here use only the density count, never the disk identity `W = B + 1` and never the 3-colouring. That is a sign that they sit strictly below the hard part.

## 4. New conjecture and tests

- **P2** (PROOFS Conj 3.4): every pair support splits into two face-rainbow trees, equivalently `Q_r ∪ Q_s` splits into two transversal spanning trees of `T/R`. `COMPUTED` on 14,881 supports, `V <= 17`. The point-side twin is Theorem 3.3. A proof would need a face-side analogue of Edmonds' branching theorem; I do not see one. Test: random pair supports on tubes and prism sums at `V ~ 100` with a matroid-intersection search rather than brute force.
- **P2 plus alternation.** P2 and Theorem 3.3 together on one split would be a tree pair with both states tree matchings. That fails for some supports, so no argument that treats faces and points separately can finish.

## 5. What a proof gives, said plainly

The packing theorem has a short sign-free proof (PROOFS §1–2). What it buys:

- **No proof of Barnette's conjecture.** It does not produce a tree matching or a Hamiltonian cycle. The gap is exactly the key lemma (Proposition 5.1 of the OpenAI paper), restated as: some 2-factor of `B` has an alternating half that is a spanning tree of `W`.
- **Polynomial-time algorithms, but for the wrong objects.** The two trees of Theorem 2.1, the rainbow trees of Corollary 3.2 and the branchings of Theorem 3.3 are all computable in polynomial time (matroid partition, matroid intersection, Edmonds' branching algorithm). None of them is a tree matching. Fable's Conjecture X starts from such a rainbow tree, so Theorem 3.3 gives it a polynomial supply of starting points, two per 2-factor.
- **A sign-free proof of LP feasibility.** Corollary 3.1 replaces "the LP is feasible because the signed theorem gives an integer point" by a three-line density argument. The previous positive-measure obstruction (`REFEREE.md` §3) does not apply to this LP.
- **An honest map entry.** The packing route is closed as a route to the key lemma: everything it can say is true and has nothing to do with whether a state is a tree. The remaining door is an exchange argument between 2-factors.
