# The proof as I understood it (written from memory, without looking back)

**Goal.** `G` cubic, bipartite, planar, 3-connected; `e` an edge. Find a Hamiltonian
cycle avoiding `e`. Removing a perfect matching leaves a 2-regular graph, so the
whole problem is to choose the matching so that what remains is connected.

**Dual.** `T = G*` is a triangulation (simple, by 3-connectivity) whose faces are
coloured black and white by the bipartition of `G`; every edge has one face of each
colour. A perfect matching of `G` is a *selection*: one side of every triangle. Its
complement in `G` is connected exactly when the selection has no cycle (a cycle of
selected sides would cut off the faces inside it). An acyclic selection has `k` edges on
`k + 2` vertices, so it is two trees. Avoiding `e` means the selection contains the dual
edge `e0`, a side of a black face `t0` with corners `a, b` (on `e0`) and `o`.

**Step 1: states.** Remove `e0`: three trees, one through each root `a, b, o`. Direct
them to the roots. Every other vertex is the tail of exactly one edge, and every edge is
the selected side of exactly one black face, so "tail of the selected side" is a
bijection `s` from the black faces other than `t0` to the non-root vertices, with `s(t)`
a corner of `t`. That is a *state*.

**Step 2: from a state back to a selection.** The side of `t` we want must contain
`s(t)`, so the side opposite `s(t)` is forbidden; together with the two sides `ao, bo` of
`t0` this is a set `S_s` of `|V| − 1` edges. Call `s` good when the opposite sides form a
forest with one root per tree, equivalently `S_s` is a spanning tree. Then by duality
the remaining edges form a spanning tree `Y_s` of `G` on the faces, in which black faces
have degree two; a tree has at most one perfect matching, and rooting at `t0` gives one.
This is the selection `P_s`.

**Disk identity.** If arrows leave chosen corners (one outgoing edge per non-root
vertex), any cycle `Z` of such arrows has length `h = 2ℓ + 3` and encloses one more white
face than black (`W = B + 1`), where `ℓ` counts edges of `Z` whose black face is inside.
Proof: Euler, a signed side count, and the bijection gives `B = I + ℓ`. Consequence: `P_s`
has no cycle, because a selection running along a cycle would force `W − B = 3`.

**Step 3: pairs.** A pair `(r, s)` is two states that differ on every face. The first
state orients the opposite sides of `s` so that each non-root has outdegree one; then a
component without a cycle has exactly one root, so `s` is good iff `Q_s` is acyclic, and a
good state has exactly one partner. The arrows `r(t) → s(t)` form `D(r, s)`, a disjoint
union of directed cycles covering `X`; the disk identity applies to them, so they have
odd length.

**Step 4: signed count.** Sign `ε(r,s) = ∏ δ(r(t), s(t))`, `δ = ±1` according to whether
the black face is on the left. Reversing a cycle of `Q_s` (changing `r` on its faces) or a
cycle of `D` flips an odd number of factors, so flips the sign. So the sum over pairs of
`ε · F(s)` with `F` depending on the second state only collapses to a sum over good
states (cyclic `Q_s` cancel in pairs). Take `F = ω^m`, with `ω` a "weight" made of heights:
for each white face a fixed path of faces to `t0`, and a ±1 at each black face where the
path turns around the chosen corner. Reversing a clockwise cycle `C` of `D` raises `ω` by
`L(C)`, the number of white faces inside, which is at least one. Group pairs by the
undirected `D`: a class with `c` cycles is a `c`-cube of orientations, the signed sum is a
`c`-fold difference of a polynomial of degree `m`, zero if `c > m` and
`±m! ∏ L(C_i)` if `c = m`. With `m` the minimum number of cycles all surviving classes
have the same sign, so the total is nonzero and a good state exists.

**Step 5: a first pair and induction.** A pair is a 2-factor in the incidence graph of
black faces and non-root vertices; Hall/max-flow reduces it to an edge count
`e(U) − b(U) ≤ 2|U| − 4`, which holds when there is no separating triangle. Otherwise cut
along a separating triangle into two smaller coloured triangulations (cap the hole), get
an acyclic selection in the outer piece containing `e0`, read off its side `e'` on the
triangle, prescribe `e'` in the inner piece, and glue. This is why the theorem carries
the avoided edge.

## Three things still unclear

1. Why exactly the path-of-faces height increases by one per enclosed white face only:
   I believe the crossing count (each crossing of `C` contributes ±1 by a left/right
   check), but the case analysis in Lemma 4.6 is where I would have to re-read with a
   pencil.
2. The density bound in Proposition 5.2: why a face of `H` of length `d ≥ 6` has balance
   at most `d − 4`, and where exactly "no separating triangle" enters (I remember: faces
   of length three of `H` are faces of `T`).
3. Whether the heights depend on the choice of paths in any way that matters; I think not
   (only differences enter), but the paper does not say it in one sentence.
