# Proofs for the categorical route

Everything tagged `PROVED-HERE` is unreviewed. Notation is that of `research/BRIEF.md`. `T` is a simple sphere triangulation with faces properly coloured black and white, `G = T*`. Papers: O is the OpenAI paper.

A labelling is a map `lab: V(T) -> {0, 1}`. An edge is mono if its ends have the same label, crossed otherwise. A labelling is face-proper if no face has three equal labels. Then every face has exactly one mono edge.

## 0. Labellings, 2-factors and loops

**Lemma 0** (`LIT` in substance: Stein; Alt, Payne, Schmidt, Wood, Lemma 5; proof written out because the loop count is used below). `PROVED-HERE`. Face-proper labellings of `T`, up to exchanging the labels, correspond to the 2-factors of `G`. The 2-factor consists of the duals of the crossed edges. If the two label classes induce `c0` and `c1` connected components, the 2-factor has `c0 + c1 - 1` cycles. It is a Hamiltonian cycle exactly when both classes induce trees.

*Proof.* Each face has one mono and two crossed edges, so the duals of the crossed edges have degree two at every vertex of `G`. Conversely a 2-factor is a family of disjoint Jordan curves, and labelling a vertex by the parity of the number of curves around it gives a face-proper labelling. `j` disjoint Jordan curves cut the sphere into `j + 1` regions. A curve cuts each face it meets into a corner with one vertex and a piece that contains the mono edge. So each region retracts onto the vertices and mono edges inside it, and the regions are the components of the two classes. Hence `c0 + c1 = j + 1`. With no monochromatic face there are `k` mono edges on `k + 2` vertices, so the classes are both acyclic exactly when `c0 + c1 = 2`. ∎

## 1. The gluing formula

Let `C = (c_0, ..., c_{m-1})` be a cycle of `T`. It cuts the sphere into two closed disks `D1`, `D2`. Each is a triangulated disk whose vertex set contains `V(C)`.

**Boundary data of a disk `D`.** The sign word `sigma(D)` in `{+, -}^m` records, for each edge of `C`, whether the face of `D` on it is black (`+`) or white (`-`).

**Boundary state of a face-proper labelling of `D`.** The pair `(word, pi)`. Here `word` is the restriction of the labelling to `C`, and `pi` is the partition of `{0, ..., m-1}` in which two positions are together when the two vertices lie in one component of a label class inside `D` (mono edges of `D` only, boundary edges included). The inner number `i` of the labelling is the number of components of the two classes in `D` that contain no vertex of `C`.

Let `N_D[word, pi][i]` be the number of face-proper labellings of `D` with that state and inner number. Normalise `lab(c_0) = 0`.

**Proposition 1** (gluing). `PROVED-HERE`. `COMPUTED`: `code/cuts.py glue 10 6`, all 1157 cycles of length 3 to 6 in the five triangulations with at most 10 vertices. For a variable `d`,

```
sum over 2-factors F of G of d^(number of cycles of F)
   =  sum over (word, pi1, i1) of D1 and (word, pi2, i2) of D2
        N_D1[word, pi1][i1] N_D2[word, pi2][i2] d^(i1 + i2 + |pi1 v pi2| - 1),
```

where `pi1 v pi2` is the join of the two partitions and `|.|` its number of blocks. The number of Hamiltonian cycles of `G` is the coefficient of `d`. It counts the pairs of labellings with `i1 = i2 = 0` and `|pi1 v pi2| = 2`.

*Proof.* A face-proper labelling of `T` with `lab(c_0) = 0` is the same as a pair of face-proper labellings of `D1` and `D2` that agree on `C`. A component of a label class of `T` either misses `C`, and is then an inner component of one disk, or meets `C`. Two vertices of `C` lie in one component of `T` exactly when they are linked by a chain of components inside `D1` and inside `D2`, that is when they are in one block of the join. So `c0 + c1 = i1 + i2 + |pi1 v pi2|`, and Lemma 0 finishes. ∎

**Hamiltonian boundary states.** A state with `i = 0` is called Hamiltonian-compatible. In such a state the classes are forests in `D`. (A cycle of one class inside `D` would enclose vertices of the other class, by face-properness, and those would form an inner component.) The realised set `F(D)` is the set of Hamiltonian-compatible states of `D`.

**Count of states.** `COMPUTED` (`code/cuts.py glue 10 6`): the Hamiltonian-compatible states seen for `m = 3, 4, 5, 6` number `3, 8, 20, 50`. This is `sum_{j >= 1} C(m, 2j) Cat(j)`. A word with `2j` label changes has `2j` arcs, and the partitions that occur are the non-crossing partitions of the `j` arcs of label 0, of which there are `Cat(j)`. `HUNCH` for general `m` (the count was checked for `m <= 6` only; the non-crossing argument is the standard one for planar connectivity and I did not write it out).

## 2. The selection rule

**Proposition 2.** `PROVED-HERE`. `COMPUTED`: `code/cuts.py full 13 m` asserts it for every side of every cycle of length 3 to 6 up to 13 vertices. For a face-proper labelling of a disk `D` with sign word `sigma`,

```
sum over mono boundary edges e of sigma_e  =  (1/3) sum over all boundary edges e of sigma_e.
```

*Proof.* Let `B`, `W` be the numbers of black and white faces of `D`. Counting edge sides by colour gives `3(B - W) = sum_e sigma_e`. Each face has one mono edge. A mono edge inside `D` lies in one black and one white face of `D`. A mono boundary edge lies in one face of `D`, black if `sigma_e = +`. So `B - W` is the left side. ∎

For `m = 3` the sign sum is `+3` or `-3`, so exactly one boundary edge is mono. These are the three patterns of O Theorem 2.2. For `m = 4` the sign sum is `0`, and the sign word is `++--` or `+-+-` up to rotation. Name the eight Hamiltonian-compatible states of a 4-cycle:

- `A_i`: `c_i` has one label, the other three vertices the other label.
- `P01`: `c_0, c_1` against `c_2, c_3`. `P12`: `c_1, c_2` against `c_3, c_0`.
- `X02`: labels alternate, and `c_0, c_2` are joined inside `D`. `X13`: labels alternate, and `c_1, c_3` are joined inside `D`.

The rule leaves six of them in each case:

| signs of `D` on `(c0c1, c1c2, c2c3, c3c0)` | allowed | excluded |
| --- | --- | --- |
| `++--` | `A0, A2, P01, P12, X02, X13` | `A1, A3` |
| `+-+-` | `A0, A1, A2, A3, X02, X13` | `P01, P12` |

Two disks on a common 4-cycle glue to a Hamiltonian cycle exactly when they share an `A` or `P` state, or one has `X02` and the other `X13` (Proposition 1: for the alternating word the join must have two blocks).

## 3. Completeness for cuts of length 4

**Theorem 3.** `PROVED-HERE`, conditional on two `LIT` statements: O Theorem 2.2, and O Corollary 7.2 (every 3-edge path of a Barnette graph lies in a Hamiltonian cycle, which O deduces from Theorem 1.1 and Gorsky, Steiner, Wiederrecht, Theorem 4.16; I did not open that paper). One sub-case rests on a `COMPUTED` finite check, marked below. Let `D` be a simple triangulated disk with properly 2-coloured faces whose boundary is a 4-cycle `(c0, c1, c2, c3)`, with at least one interior vertex.

1. If `sigma(D) = +-+-` then `F(D)` is the whole allowed set `{A0, A1, A2, A3, X02, X13}`. (Such a disk has no chord: a chord would cut off a triangle with two boundary edges of opposite signs and one chord edge, and the sign sum of a triangle is `+3` or `-3`.)
2. If `sigma(D) = ++--` and `c0 c2` is not an edge of `D`, then `F(D) = {A0, A2, P01, P12, X02, X13}`.
3. If `sigma(D) = ++--` and `c0 c2` is an edge of `D`, then `F(D) = {A0, A2, P01, P12, X02}`.

So for 3-cycles and 4-cycles the set of realised boundary patterns depends only on the sign word and the chords.

`COMPUTED` independently of the proof: `code/cuts.py four 15`, 14872 rotated cut sides in all Eulerian triangulations with at most 15 vertices, exactly three pattern sets occur, the ones above.

*Proof.* "At most" is Proposition 2, plus the remark that a chord `c0 c2` joins `c0` to `c2` inside `D` and so excludes `X13`. For "at least" close `D` by a cap `K`, a second disk on the same 4-cycle with the opposite signs, chosen so that `That = D + K` is a simple Eulerian triangulation. Its dual `Ghat` is a Barnette graph. A Hamiltonian cycle of `Ghat` restricts to a Hamiltonian-compatible state of `D`, so it is enough to find, for each allowed pattern, a prescription in `K` that forces it.

*Case 1.* `K` is a new vertex `z` joined to `c0, ..., c3`. In `Ghat` the four cap faces form a quadrilateral face `Q` with edges `q_i` dual to `z c_i`. `That` is simple because `D` has no chord.
- The path `Q - q_i` has three edges. A Hamiltonian cycle through it crosses `z c_j` for `j != i` and not `z c_i`, so `z` has the label of `c_i` and of no other `c_j`. That is `A_i`.
- The edge `q_1` joins the cap faces `(z, c0, c1)` and `(z, c1, c2)`. Let `f` and `f'` be the third edges of `Ghat` at these two faces, dual to `c0 c1` and `c1 c2`. A Hamiltonian cycle through the 3-edge path `f, q_1, f'` avoids `q_0` and `q_2`. So `z c0` and `z c2` are mono and `z c1` is crossed, and then `z c3` is crossed too, because the faces `(z, c2, c3)` and `(z, c3, c0)` already have their mono edge. The labels alternate, and `c0`, `c2` are joined through `z` outside `D`. So they are not joined inside `D`, and `c1, c3` are, since their class is connected and cannot pass through `z`. That is `X13`. The same path around `q_0` gives `X02`.

*Case 2.* First let `K` be the edge `c0 c2` with the two triangles `w = (c0, c1, c2)` and `b = (c2, c3, c0)`. The colours fit: `w` is white because the faces of `D` on `c0c1` and `c1c2` are black, and `b` is black. In `Ghat` the vertices `w`, `b` are joined by the edge `d` dual to `c0 c2`, and `w` carries `e0*, e1*`, `b` carries `e2*, e3*` (duals of the boundary edges).
- A Hamiltonian cycle through the path `e0*, d, e3*` crosses `c0c1`, `c0c2`, `c3c0` and no other edge at `w` or `b`. So `c1 = c2 = c3 != c0`. That is `A0`. The paths `e1* d e2*`, `e1* d e3*`, `e0* d e2*` give `A2`, `P01`, `P12` in the same way.
- A Hamiltonian cycle avoiding `d` (O Corollary 7.1) uses all four `e_i*`. The labels alternate, `c0` and `c2` are joined by the mono edge `c0 c2` outside `D`, so `c1, c3` are joined inside `D`. That is `X13`.
- For `X02` take `K` to be the octahedron with two adjacent faces removed. In `Ghat` this is a cube with two adjacent vertices removed: a hexagon `x1, y1, q, y2, x2, p` with the chord `p q`, where the four cut edges end at `x1, y1, y2, x2`. The ends `x1, x2` have one colour and `y1, y2` the other, so `c1` is the vertex of `T` between the cut edges at `x1` and `x2`, `c3` the one between those at `y1` and `y2`, and `c0`, `c2` lie between an `x` and a `y`. Take the 3-edge path `x2 p, p q, q y2`. A Hamiltonian cycle through it does not use `x1 p` or `y1 q`, so `x1` and `y1` each use the edge `x1 y1` and their cut edge. It does not use `x2 y2` either, since that would close the 4-cycle `x2 p q y2`. So all four cut edges are used, and the cycle meets the cap in the paths `x1 y1` and `x2 p q y2`. Each path cuts off one of `c0`, `c2` inside the cap, and `c1`, `c3` lie in the region between them. So `c1, c3` are joined inside the cap, and therefore `c0, c2` are joined inside `D`. `COMPUTED` agreement: `code/gadgets.py 11 p4`, line `X02` for `++--`, reports this cap and this path (crossed edges `(1,5), (2,5), (3,5)` on the octahedron).

*Case 3.* The diagonal cap is not available. The octahedral cap of Case 2 has no chord, so `That` is simple. `COMPUTED` (`code/gadgets.py 11 p4`, output `data/gadgets_p4_v11.txt`): on this cap there are 3-edge paths that force each of `A0, A2, P01, P12, X02` on `D`. The check is an enumeration of the labellings of a disk with six faces. I did not write the four remaining path arguments by hand. ∎

**Remark (what Theorem 2.2 alone gives).** `COMPUTED`: `code/gadgets.py 11`. Among all caps that occur in triangulations with at most 11 vertices, a single prescribed facial edge forces a boundary pattern in one case only, `X13` through the diagonal cap. The other five patterns need the 3-edge path form.

## 4. Completeness stops at length 5

**Proposition 4.** `COMPUTED`: `code/cuts.py full 13 5` and `full 13 6`, output `data/full_v13.txt`. For 5-cycles the sign word is unique up to symmetry (`---+-`) and the rule allows 14 patterns. Among 450 chordless sides with interior vertices on both sides, 95 realise all 14, 353 miss one and 2 miss two. For 6-cycles 2 of 1258 sides realise everything the rule allows.

Smallest witness: the 9-vertex triangulation `plantri_9_0`, cycle `(0, 1, 6, 8, 4)`, side with 3 interior vertices and signs `---+-`. The pattern with word `00011` (so `c0, c1, c2` against `c3, c4`) obeys the rule and is not realised.

So from length 5 on, `F(D)` is real data about `D`, not a function of the boundary.

## 5. Hamiltonian cycles as triangle factors

Let `K` be the triangulation with vertex set `V(T)` together with a centre in each black and each white face of `T`, and edges: centre to corner, and black centre to white centre across each edge of `T`. Its vertex classes are `V`, `B`, `W`, it has `6k` triangular faces `(v, b, w)`, one for each edge `e` of `T` with a chosen end `v` (`b`, `w` are the faces on `e`). Deleting one class gives `K - W = H` (black spoke graph), `K - B` (white spoke graph), `K - V = G`.

**Proposition 5.** `PROVED-HERE`. `COMPUTED`: `code/trinity.py factors 11` builds the factors for all 2048 triples below. Fix a Hamiltonian cycle of `G` and vertices `v1`, `v2` of `T` on its two sides. Orient the two induced trees towards `v1` and `v2`. The triangles `(tail of e, black face of e, white face of e)`, over the mono edges `e`, are pairwise disjoint and cover every vertex of `K` except `v1` and `v2`. Conversely a set `Phi` of pairwise disjoint faces of `K` covering `V(K) - {v1, v2}` comes from a Hamiltonian cycle exactly when the edges of `T` it uses form a forest.

*Proof.* There is one mono edge in each face, so each `b` and each `w` is used once, and each vertex other than the two roots is the tail of one edge. Conversely the edge set `P` of `Phi` has one edge in every face, so its complement is a 2-factor, and `P` is its set of mono edges. `P` has `k` edges on `k + 2` vertices, so it is a forest exactly when it has two components, which by Lemma 0 means one cycle. ∎

The three projections of a factor are a matching `B -> V` (a bijection from all black faces onto `V - {v1, v2}`, a two-root state), a matching `W -> V`, and the perfect matching of `G` complementary to the cycle. O's construction is the passage from the first to the third: for a tree matching `s` and `e0 = r1 r2`, the factor with roots `r1, r3` has first projection `s` extended by `t0 -> r2`.

## 6. Insertion into a face

**Proposition 6.** `PROVED-HERE`. `COMPUTED`: `code/recursion.py mult 9`, 1016 insertions into white faces and 840 into black faces. Let `(T1, t0)` and `(T2, t0')` be rooted Eulerian triangulations and `f != t0` a face of `T1`. Let `T` be `T1` with `T2` minus `t0'` glued into `f`.

1. If `f` is white, the numbers of states, of pairs and of tree matchings of `(T, t0)` are the products of those of `(T1, t0)` and `(T2, t0')`.
2. If `f` is black, `(T, t0)` has no pair (`LIT`: trees paper Theorem 1.2, the separating triangle has black inner boundary).

*Proof of 1.* The inserted faces along the boundary of `f` meet black faces of `T1`, so they are white in `T`, and the colouring of `T2` in which `t0'` is black is the restriction. `A = A1 + A2` and `X = X1 + X2`, with `|A2| = |X2|`, and no face of `A1` has a corner in `X2`. So a state of `T` maps `A2` onto `X2` and `A1` onto `X1`, and states are pairs of states. Two states are disjoint exactly when both restrictions are. For tree matchings, `H - s` is the union of `H1 - s1` and `F2 = (H2 - s2) - t0'`, which meet in the three corners of `f`. `H - s` has one edge fewer than vertices, so it is a tree exactly when it is acyclic. If it is acyclic then `H1 - s1` is acyclic, hence a tree, hence connected, and then the union is acyclic exactly when `F2` is a forest with the three corners in three different components. That is the statement that `H2 - s2` is a tree. ∎

The limits report proves this for the hexagonal prism dual. The argument is the same.
