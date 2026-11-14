# The minimal skeleton

Summary.
1. Every one of the three proofs passes through the same 14 nodes (`K0` to `K16` below). No paper has a second way to get a tree matching. All three use pairs, the disk identity, the `Q_s`-reversal and a weighted regrouping by `D`.
2. The proofs take different routes at four nodes only: how the first pair is found, how the weights are built, how the grouped count is shown nonzero, and how `P` is shown to give one cycle.
3. A good deal is packaging: the complex phase, the exponential, the slide across subdisks, `c_min`, the induced trees, the partner in the recovery step, and the integrality of `J`.
4. Two new facts for other agents. The OpenAI sum is the multilinear coefficient of one determinant (lead L1, proved and checked). The natural extremal shortcut "look for a tree pair among the pairs with fewest cycles" is false (lead D2, counterexample with `n = 15`).
5. Each core edge below lists what the papers do and at least two other kinds of argument, tagged `HUNCH` or `CONJECTURE` with a test.

The picture is `graphs/merged.pdf` (source `graphs/merged.dot`). Node ids `K*`, `V*`, `X*` are the ids in that file.

## 1. The unavoidable core

| Node | Statement | O | L | T |
| --- | --- | --- | --- | --- |
| K0 | `T = G*` is a simple, 2-coloured sphere triangulation, rooted at a black face `t0` with an edge `e0` | `O1`, `O2` | `aux(G)`, `b0 w0` | `O1` |
| K1 | the incidence graph `B` on `A` and `X` is balanced, `|A| = |X| = n` | (2.1) | not stated | (2) |
| K2 | `B` has two disjoint perfect matchings (a pair) | Prop. 3.1 | Lemma 9 | Section 3 |
| K3 | disk identity: a directed cycle of state edges has `2l - h = -3` | Lemma 4.1 | Claim 25 | Lemma 4.1 |
| K4 | a pair has a sign, and both cycle reversals flip it | (5.1), Lemma 5.2 | Lemmas 16, 17 | Lemma 4.2 |
| K5 | weights with `L+(C) > L-(C)` on every `D`-cycle | Lemma 5.3, (5.3) | rays | Lemma 5.1 |
| K6 | for fixed `s` with a cycle in `Q_s`, the pairs cancel | Lemma 5.2 | `ι1` | `β` |
| K7 | grouped by `D`, the count is not zero | (5.5) | `ι2` | (11), walk |
| K8 | some pair has `Q_s` a forest, so `H - s` is a spanning tree | Prop. 5.1, Lemma 6.1 | Lemmas 7, 8 | Thm 5.2, (3) |
| K10 | the duals of the deleted spokes form a spanning tree on the white faces | 6.1 | Cor. 27 | 7.1 |
| K11 | rooting it at `y0` selects one side per face of `T`, a perfect matching `P` of `G` | 6.1 | Claim 31 | 7.1 |
| K12 | `E(G) - P` is a Hamiltonian cycle that avoids `e0` | Lemma 6.2, 6.2 | Lemma 30 | Lemma 7.1 |
| K15 | cut at a separating triangle, prescribe the cap edge, glue | Section 7 | App. C | 7.3 |
| K16 | Barnette's conjecture with a prescribed avoided edge | Thm 1.1, Cor. 7.1 | Thm 3 | Thm 1.1 |

The dependency shape is a chain with two side inputs:

    K0 -> K1 -> K2 --+
    K0 -> K3 -> K4 --+--> K6, K7 -> K8 -> K10 -> K11 -> K12 --+--> K16
                K5 --+                                  K15 --+

`K3` is used by `K4` (twice: on `D`-cycles and on the `Q_s`-cycle). In O and T it is used once more at `K12`.

## 2. Where the routes differ

| Core node | Variants | Difference |
| --- | --- | --- |
| K2 | `V2a` (O), `V2b` (L), `V2c` (T) | O bounds every component of `T[U]`. L takes a minimal deficient set and finds a 3-edge cut. T treats the region of `t0` separately and gets an equivalence with "no black-inner separating triangle" |
| K5 | `V5a` (O, T), `V5b` (L) | unit circulations from dual paths, then a slide from `T`-edges onto spokes. Or vertical rays in a straight-line drawing, with cycles defined on spokes from the start |
| K7 | `V7a` (O), `V7b` (L), `V7c`, `V7d` (T) | Taylor coefficient of order `c_min`. Fixed points of a second involution. Coefficient of `(z-1)^m` inside one exchange component. A path-following walk that restarts with fewer cycles |
| K12 | `V12a` (O, T), `V12b` (L) | a count against the disk identity shows `P` is a forest. Or an innermost-cycle argument shows the complement is connected |

Only in one paper: `X1` (T: tree matching if and only if exactly one mate), `X2` (T: common permutation sign, determinant count, enumeration), `X3` (O: Corollary 7.2).

## 3. Essential and packaging

**Essential.** I could not remove any of these from any of the three proofs.
- The rooted incidence graph `B` and its perfect matchings.
- A second, disjoint matching `r`. It is the certificate that orients `Q_s` and makes the reversal possible.
- The disk identity.
- The `Q_s`-reversal as a sign-reversing involution whose weight depends on `s` only.
- The regrouping by `D` with weights that prefer one orientation of every cycle.
- Tree-cotree duality and the rooted selection.
- The prescribed edge, which is what lets the pieces glue.

**Packaging.** Each of these can be dropped or swapped, and at least one paper does so.
- The complex phase `i^J`. A sign `±1` is enough (T). The two differ by `i^{-n}`.
- The exponential and its Taylor expansion. An integer polynomial (T) or a plain count (L) does the same job.
- The slide of an edge across a subdisk (`N4c`). It exists because `D` lives on edges of `T` and the weights on spokes. L puts both on spokes.
- The dual-path construction of Lemma 5.3. Any weight field with positive circulation on counterclockwise spoke cycles works. L's ray count is one.
- `c_min`. The marked walk never computes it.
- The two induced trees. L goes from `P` to the Hamiltonian cycle directly.
- The hypothesis "no separating triangle". "No black-inner separating triangle" is enough, and is exact (T).
- The partner `r` in the recovery step. A tree matching alone suffices (T, and L's Lemma 30).
- The integrality of `J` as a consequence of the disk identity. It follows from the vertex 3-colouring alone (see B0 below).

## 4. Core edges and other ways to cross them

For each edge: what the papers do, then other kinds of argument. `HUNCH` means I have a reason but no proof. `CONJECTURE` means a precise statement with a test. Script references are to `scripts/check_nodes.py`, output `data/check_nodes.txt`.

### Edge A. `K0, K1 ⟹ K2` (a pair exists)

**Papers.** A Hall-type deficiency condition (max-flow in O and T, Ore in L) plus a planar Euler count. Kind: flow duality with a density inequality.

**A1. Inductive, `HUNCH`.** Rooted Eulerian triangulations can be grown by local expansions. One of them is the vertex split used in the script (`split_vertex`, the dual of adding a square across a face of `G`). Show that a pair survives each expansion as long as `t0` stays on the black side of every separating triangle. Test: for each expansion, find a local rule that maps a pair to a pair, and check it on all pairs for `n ≤ 15`.

**A2. From the conclusion backwards, `CONJECTURE`.** In a rooted triangulation with no black-inner separating triangle, every Hamiltonian cycle of `G` that avoids `e0` arises from some tree matching by the recovery of `K10` to `K12`. If true, a pair exists exactly when such a cycle exists, and known partial results (Goodey for faces of size 4 and 6) would give pairs in those classes with no flow argument. Test: enumerate Hamiltonian cycles avoiding `e0` for small `G` and compare with the image of the recovery map. The script's `recover` gives the image.

**A3. Matroidal, `HUNCH` that it adds nothing.** Two disjoint perfect matchings are a basis of the union of two copies of a transversal matroid. The matroid union rank formula reduces to the same deficiency count (3.1). I expect no new content here, only the same inequality in other words. Recorded so nobody spends an afternoon on it.

### Edge B. `K0 ⟹ K3` (the disk identity)

**Papers.** Euler's formula, signed side counting, and a double count through the matching. O and T do it on the triangulated disk, L on the hexagon-faced spoke disk. Kind: double counting.

**B0. What the identity says, `PROVED-HERE`.** A properly 2-coloured sphere triangulation has a proper vertex 3-colouring `c` with values in `Z/3` (standard, `LIT` without a reference checked). The colours increase counterclockwise around black faces, so `δ(v, w) ≡ c(w) - c(v) mod 3` for every directed edge. Two consequences.
- `3J = Σ_t δ(r(t), s(t)) ≡ Σ_t c(s(t)) - Σ_t c(r(t)) = 0 mod 3`, because `r` and `s` are both bijections onto `X`. So `J` is an integer for a one-line reason, with no disk identity.
- The `δ`-sum of a closed cycle is 3 times the winding number of `c` around the triangle of colours, and by the side count it is `3(B - W)` for a counterclockwise cycle. So the disk identity says: the disk of a directed state cycle contains exactly one more white face than black faces, or, the colouring map has degree `-1` on it.

**B1. Linear-algebraic, `HUNCH`.** The faces of the spoke graph `H` are hexagons, and `6 ≡ 2 mod 4`. That is Kasteleyn's condition for the constant signing to count perfect matchings by a determinant (`LIT`: Kasteleyn, "Graph theory and crystal physics", 1967; cited from memory, not opened). T's Lemma 6.1 (all states have one permutation sign) is exactly that statement for `B`, and its proof uses only the parity part of the disk identity. So the disk identity is an integer lift of Kasteleyn's sign lemma, available because every inner face is exactly a hexagon. Test: derive `t_out - t_in = 3` from a flatness condition for a `Z/4`-valued or complex signing of the spokes.

**B2. Topological, `HUNCH`.** Prove "degree `-1`" directly. The state pairs every black face in the disk with a vertex of the disk (`B = I + l`). Read this as a cancellation of cells, as in discrete Morse theory, and compute the degree from what is left. Test: write the pairing as a discrete vector field on the disk and check that the uncancelled cells always give Euler characteristic 1 with one white face left over.

**B3. Inductive, `HUNCH`.** Peel the disk. Remove a boundary vertex together with its matched black face and show that `2l - h` does not change. Test: implement the peeling on the cycles enumerated by the script.

### Edge C. `K3 ⟹ K4` (both reversals flip the sign)

**Papers.** O and T use the local identity `δ(u,s) - δ(r,s) = 2δ(r,u)` and the disk identity on the `Q_s`-cycle. L writes `cw'` as a sum of local turns and counts flips. Kind: local-to-global by the disk identity.

**C1. Linear-algebraic, `PROVED-HERE`.** Put `ζ = e^{iπ/6}`. For a state `s` let `N_s` be the `X × A` matrix with `N_s[v, t] = ζ^{δ(v, s(t))}` for the two nonroot corners `v ≠ s(t)` of `t`, and zero elsewhere. Column `t` is supported on the nonroot ends of the `Q_s`-edge of `t`, with entries `ζ` and `ζ^{-1}`. So `N_s` is an incidence matrix of `Q_s`, reduced at the roots and twisted by `ζ`. Its determinant expands over the mates `r` of `s`, each with the same permutation sign `κ` (T, Lemma 6.1), and the term of `r` is `i^{J(r,s)}`. Two mates that differ on one unicyclic component differ by the factor `ζ^{2 · (±3)} = -1`. So `det N_s = 0` when `Q_s` has a cycle, and `det N_s = κ i^{J}` when `s` is a tree matching. This is the cancellation `K6` as the statement that a twisted incidence determinant vanishes on a cycle whose holonomy is `-1`. It is the same computation as Lemma 5.2, written as linear algebra. `COMPUTED`: `det N_s` equals `κ Σ_r i^{J(r,s)}` and vanishes exactly when `s` is not a tree matching, for every `s` with a mate in all 35 test cases that have pairs (`twisted_incidence_det_N_s`).

**C2. Topological, `HUNCH`.** `J` is a sum of rotation numbers `±1` of the spoke cycles. The `Q_s`-reversal can change the cycle structure of `D` completely, and still `J` moves by exactly 2 (`COMPUTED` on every move of every test case). That rigidity suggests an invariant of the form `J(r, s) = g(s) - g(r)` plus a term local to `Q_s`, like a height function for dimers. Test: fit `g` on the enumerated pairs of the `n = 15` and `n = 23` examples.

### Edge D. `K2, K4, K5, K6 ⟹ K8` through `K7` (a pair gives a tree pair)

**Papers.** One signed weighted sum, evaluated by fixing `s` (cancellation) and by fixing `D` (positivity at lowest order). Kinds: analytic (O), bijective (L), algebraic per component (T), path-following (T).

**L1. The sum is a multilinear determinant coefficient, `PROVED-HERE` and `COMPUTED`.** For `t ∈ A` let `W_t(a)` be the `X × X` matrix with `W_t[v, w] = ζ^{δ(v,w)} a(t, w)` for distinct nonroot corners `v, w` of `t`, and zero elsewhere. Then

    Σ_{pairs (r,s)} i^{J(r,s)} Π_t a(t, s(t))  =  [λ_1 ⋯ λ_n] det( Σ_t λ_t W_t(a) ).

Proof. Expand the determinant over permutations `π` of `X`. A term is multilinear in `λ` exactly when the factors come from `n` different faces. Let `t(v)` be the face that supplies the factor in row `v`. Then `r(t(v)) = v` and `s(t(v)) = π(v)` define two states with `r(t) ≠ s(t)`, because the diagonal of each `W_t` is zero, and every pair arises once. The permutation is `π = s r^{-1}`, whose cycles are the `D`-cycles. They have odd length by the disk identity, so `sgn π = 1`. The product of the entries is `ζ^{3J} Π a = i^J Π a`. ∎

With `a(t, w) = e^{x a_0(t, w)}` the left side is `Z(x)`. The script checks the identity numerically for random `a` on 21 rooted triangulations with pairs, up to `n = 15` (`multilinear_det_identity`). Combined with C1,

    Z = κ Σ_s det N_s · Π_t a(t, s(t)),

and distinct `s` give distinct monomials. So a tree matching exists if and only if this polynomial in the `a(t, v)` is not identically zero. The papers' nonvanishing argument is one way to show that. At `a ≡ 1` the matrix `Σ λ_t W_t` is Hermitian for real `λ`: it is the adjacency matrix of `T[X]` with a `U(1)` connection of holonomy `i` around black triangles and `-i` around white ones.

**D1. Linear-algebraic, `HUNCH`.** The right side of L1 is `n!` times a mixed discriminant of the matrices `W_t`, each supported on at most three rows and columns. For positive semidefinite matrices, positivity of the mixed discriminant is governed by a Rado-Hall rank condition (`LIT` pointer only: results of Panov and of Bapat on mixed discriminants, not opened, so treat the attribution as unverified). Our `W_t` are not positive semidefinite. Test: look for a change of variables that makes them so, and compute `rank(Σ_{t ∈ S} W_t)` against `|S|` on the test cases with and without pairs.

**D2. Extremal, `REFUTED`.** Statement tried: among the pairs with the fewest `D`-cycles there is one with `Q_s` a forest. Counterexample: the octahedron with every face split in four (`n = 15`, any `t0`). It has 20 pairs. The 4 pairs with one cycle all have a cycle in `Q_s`. The 12 tree pairs all have three cycles. The same happens for the double wheel of rim 6 split in four (`n = 23`): 16 one-cycle pairs, none a tree pair. Lesson: the lowest-order coefficient is nonzero because of the pairs with fewest cycles, but the pairs that survive the cancellation live elsewhere. A potential-function proof cannot minimise the number of cycles first. `COMPUTED` (`pairs_by_cycle_count`).

**D3. Parity, `PROVED-HERE` that the naive version fails.** A state is a tree matching if and only if it has an odd number of mates (T, Prop. 2.1: the number is `2^k`). So the number of tree matchings has the parity of the number of ordered pairs, which is even because `(r, s) ↦ (s, r)` has no fixed point. Counting mod 2 proves nothing. The weighted sums of the papers are the refinement that does. A `2`-adic version (evaluate T's polynomial at `z = -1` with weights chosen so that every `L+ - L-` is odd) is a `HUNCH`. Test: check on the examples whether such weights exist and whether the value at `-1` is nonzero.

**D4. Probabilistic, `HUNCH`.** The two moves are cycle popping in the sense of Wilson's algorithm: move (b) pops a cycle of `Q_s`, move (a) pops a cycle of `D`. A random-walk proof would show that the walk on an exchange component hits a tree pair in finite expected time, with a bound. T mentions a random-walk constructor in a companion I do not have. Test: measure hitting times on the components of the `n = 23` example and on larger ones.

### Edge E. `K8 ⟹ K10 ⟹ K11` (white tree and selection)

**Papers.** Tree-cotree duality, then orient the dual tree towards `y0`. Kind: planar duality.

**E1. Matroidal, `HUNCH` that it is the same.** The complement of a basis is a basis of the dual matroid, and the dual of a planar graphic matroid is the graphic matroid of the dual. Same statement.

**E2. Via Temperley, `HUNCH`.** Tree matchings should correspond to spanning trees of a graph on the white faces with a degree condition, by the Kenyon-Propp-Wilson correspondence that O and T cite. I did not open that paper. If the correspondence is explicit, `K10` and `K11` are one step. Test: write the bijection for the octahedron and the `n = 15` example.

I see no reason to look for a third route here. This edge is rigid.

### Edge F. `K11 ⟹ K12` (one cycle)

**Papers.** Two kinds already. O and T count selected sides and contradict the disk identity for `s`. L uses planarity and an out-degree-one walk on a tree of faces.

**F1. Inductive, `CONJECTURE`.** Remove a leaf `y` of the white tree together with the black face whose spoke it crosses. The result is again a rooted triangulation with a tree matching, with two fewer vertices in `G`, and the Hamiltonian cycle of the larger graph is a local detour of the smaller one. Test: implement leaf removal on the trees produced by the script and check that the smaller object is valid.

**F2. Explicit classes, `HUNCH`.** The class of a vertex `v` is the root reached by following the selected out-edges from `v`. Two roots are then merged by `e0`. A proof that this walk always ends at a root is a proof of `K12`. L's argument and the disk-identity argument are both proofs of that termination. A third could come from a potential that decreases along the walk, for instance the distance to `y0` in the white tree. Test: compute, along each selected out-edge, the change in white-tree depth of the two white faces at the edge, and look for monotonicity.

### Edge G. `K12, K15 ⟹ K16` (gluing)

**Papers.** Induction on the number of vertices (O, T) or a minimum counterexample (L), always with a prescribed edge at the cap.

**G1. Choose the root to avoid cuts, `PROVED-HERE` in part.** Every separating triangle has exactly one black side (`audit-trees.md`, T-F1). The state method works without cutting exactly when `t0` is on the black side of every separating triangle. For Hamiltonicity alone the root is free, and so is the colour swap. So no cut is needed whenever some black face lies on the black side of all separating triangles, or some white face lies on the white side of all of them. This can fail when three or more separating triangles are arranged with alternating black sides, so it does not remove `K15`. Test: count, over generated Barnette graphs, how often a cut-free root exists.

**G2. Other roots, `CONJECTURE`.** Tutte's trinity allows any three roots of three different colours, not only the corners of one face. Conjecture: for every simple 2-coloured triangulation there is a choice of three such roots for which two disjoint states exist. If so, the obstruction is an artefact of rooting at a face. The recovery step would need a replacement for the three spokes at `t0`. Test: on the black-inner example of the script (0 pairs with `t0` outside), enumerate all root triples and count pairs.

**G3. Matroidal, `HUNCH` that it is the same.** Gluing along a triangle is a 3-sum. Hamiltonian cycles with one prescribed missing edge at the summing triangle compose under 3-sums. This is the same induction.

## 5. What I would try first

1. A2. It tests whether the state method sees every Hamiltonian cycle. Cheap to run, and either answer is informative.
2. L1 with D1. The determinant form puts the problem in reach of mixed-discriminant and matrix-pencil tools.
3. G2. If roots off a face remove the obstruction, the induction over separating triangles disappears from the exposition.
