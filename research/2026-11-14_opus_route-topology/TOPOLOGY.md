# Topological readings of the proof

Notation follows `research/BRIEF.md`: `T` is the Eulerian triangulation with black and white faces, `t0` the outer black face, `R` its three roots, `A` the other black faces, `X` the non-root vertices, `|A| = |X| = n`, `k = n + 1` black faces in all. `G = T*` is the Barnette graph. `delta(v,w) = +1` when the black face of `vw` is on the left of `v -> w`. For a simple cycle `C` of `T` bounding a disk `D` on the side away from `t0`: `h` is its length, `I` the number of strictly interior vertices, `B` and `W` the black and white faces in `D`, and `l` the number of boundary edges whose black face is in `D`.

Every numbered claim carries a status tag. Script references point into `code/topo.py`; the commands and the ranges are in `code/README.md` and in each JSON file under `data/`.

The short version. Three of the proof's steps have exact topological meanings:

- The disk identity is Hopf's Umlaufsatz (discrete Gauss-Bonnet) for a flat structure that the state defines, combined with a vertex-by-vertex identity between turning and the winding number of the vertex colouring.
- The final step is Alexander duality: the complement of the 2-factor retracts onto the selected edges, so the number of cycles of the 2-factor is one more than the cycle rank of the selected edges.
- The cancellation is an acyclic matching on a union of Boolean lattices whose critical cells are the forest pairs. The sum `Z(1)` is an Euler characteristic, and it is always zero. The proof needs the graded version `Z(z)`, which plays the role of an Alexander polynomial.

The Floer and dessin dictionaries are real (they are theorems of Tutte, Berman, Kálmán, Juhász-Kálmán-Rasmussen and Kálmán-Murakami), but so far they only re-describe the objects. The one place where Floer theory says something about existence is §5.4. There, the obstruction to a tree matching is exactly the failure of one spin^c structure of the Barnette graph's own special alternating link to be supported. That is proved, given the constructive paper's criterion.

## 1. The colour map, and delta as a pulled-back 1-form

**1.1 [LIT].** A sphere triangulation has a proper vertex 3-colouring iff every vertex has even degree. The colouring is unique up to permuting the colours. This is classical (Heawood). Hine and Kálmán, *Clock theorems for triangulated surfaces*, arXiv:1808.06091, §2.1, use exactly this structure under the name trinity, and so do Kálmán, *Adv. Math.* 244 (2013) 823-873, Def. 9.1, and Juhász-Kálmán-Rasmussen, arXiv:1112.2632, §2. In a trinity the black triangles are the triangles in which the colours appear in one cyclic order, and the white ones are those with the other order.

**1.2 [PROVED-HERE].** There is a colouring `c: V(T) -> Z/3` with `delta(v,w) ≡ c(w) - c(v) (mod 3)` for every edge. In words, `delta` is the lift to `{+1,-1}` of the colour difference.

*Proof.* Inside a black triangle the three edges traversed with the black face on the left form a directed 3-cycle, and every such edge has `delta = +1`. Across an edge, `delta(v,w) = -delta(w,v)`. Define `c` along a spanning tree. Consistency around each white or black triangle holds because the `delta`-sum around the boundary of any face is `±3 ≡ 0`. Face boundaries generate the cycle space of the sphere. ∎ [COMPUTED: `exp_disk`, all 262 rooted instances with at most 12 vertices, colouring consistent in every one.]

**1.3 The folding map.** Let `Δ` be one triangle with corners labelled 0, 1, 2. The colouring gives a simplicial map `f: T -> Δ` that sends each face onto `Δ`. It preserves orientation on white faces and reverses it on black ones, so it is the "fold". Doubling `Δ` gives the two-triangle sphere `S_Δ`, with `Δ+` in front and `Δ-` behind. Send black faces to `Δ+` and white faces to `Δ-`. This gives an orientation-preserving branched cover `F: S^2 -> S_Δ` of degree `k`, branched only over the three corners. A vertex of degree `2d` has ramification index `d`.

Let `θ` be the 1-cochain on `∂Δ` that gives each of the three edges, oriented `0 -> 1 -> 2 -> 0`, the weight `1/3`. By 1.2, `delta = 3 f*θ`. So for every closed edge path `γ` in `T`:

    sum_γ delta = 3 · wind(f∘γ),   wind = degree of f∘γ : S^1 -> ∂Δ ≅ S^1.        (1.3)

In particular `J(r,s) = Σ_C wind(f∘C)`, summed over the cycles `C` of `D(r,s)`. The number `J` is the total colour winding number of the relative permutation `r(t) -> s(t)`. [PROVED-HERE; COMPUTED in `exp_disk` (P3): 3264 of 3264 cycles.]

**1.4 Argument principle [PROVED-HERE].** If `C` is a simple counterclockwise cycle bounding `D`, then

    wind(f∘C) = B - W.                                                               (1.4)

*Proof.* `F|_D` maps `(D, ∂D)` into `(S_Δ, ∂Δ)`. Its local degree over an interior point of `Δ+` is `B`, and over `Δ-` it is `W`, because every face maps homeomorphically and preserves orientation. For any map of a disk into a sphere with boundary on an embedded circle, the difference of the local degrees on the two sides equals the degree of the boundary map onto that circle. ∎ Unwinding the definitions gives exactly the paper's signed side count `3(B - W) = 2l - h`.

A complex-analytic version: by the Riemann existence theorem, `F` is a Belyi map `β` once the target is the Riemann sphere with corners at the cube roots of unity, black centres at 0 and white centres at ∞. Then `sum_C delta = (1/2πi) ∮_C d log(β^3)`. That is the argument principle for `β^3`, which has a zero of order 3 at every black centre and a pole of order 3 at every white centre. (The Riemann existence theorem is standard; see for example Lando and Zvonkin, *Graphs on Surfaces and Their Applications*, Springer 2004, ch. 1-2. I did not open that book during this session.)

## 2. The disk identity is Hopf's Umlaufsatz

**2.1 The state's angle structure.** Fix a state `s` and write `φ(v) = s^{-1}(v)` for the black face matched to a non-root `v`. Assign corner angles, in units of `π/3`:

| corner | angle |
| --- | --- |
| corner of a white face | +1 |
| corner `(t, s(t))` of a face `t ∈ A` (the matched corner) | +5 |
| the other two corners of `t ∈ A` | -1 |
| corners of `t0` | -1 |

**Lemma 2.1 [PROVED-HERE].** Every face except `t0` has angle sum `π`. Every non-root vertex has total angle `2π`.

*Proof.* A non-root vertex of degree `2d` has `d` white corners, one matched corner and `d - 1` other black corners. The total is `d + 5 - (d - 1) = 6` units. ∎

The white corners are those of an equilateral triangle. The black ones are those of an equilateral triangle with its orientation reversed (`-π/3` each), plus a full turn `2π` at the matched corner. So the developing map of this structure is the folding map `f` itself. The state changes nothing in the picture, because a full turn is invisible there. What it does is lift the angle data from `R/2πZ` to `R`, choosing at each non-root vertex the black corner that carries the extra `2π` so that the vertex becomes flat. Seen as curvature bookkeeping: the folded structure has curvature `+2π` at every vertex and `-2π` in every black face. A state is a perfect matching that cancels these in pairs, leaving `t0` (`-2π`) and the three roots (`+2π` each). The total is `4π`, as Gauss-Bonnet requires.

**2.2 Discrete Gauss-Bonnet [standard; PROVED-HERE for this setting].** For any real corner angles on a triangulated disk `D` in which every face has angle sum `π`:

    Σ_{interior v} (2π - θ_v) + Σ_{boundary v} (π - θ_v) = 2π.

*Proof.* Use `V - E + F = 1` and `2E = 3F + h`. ∎ No positivity of angles is needed.

**2.3 Local identity [PROVED-HERE].** Let `γ` be a closed path (not necessarily simple) such that at every vertex `v` the outgoing edge of `γ` lies in the matched face `φ(v)`. Measure the left exterior angle `ε_v = π - θ_v^left`, where `θ_v^left` is the angle sum of the corners on the left of `γ` at `v`. Then

    ε_v = (π/3) ( (delta_in + delta_out)/2 - 3 delta_out ),   so   Σ_v ε_v = -(2π/3) sum_γ delta = -2π J(γ).

*Proof.* The faces on the left of `v`, between the outgoing and incoming edges, alternate in colour. The face next to the outgoing edge is black iff `delta_out = +1`, and the face next to the incoming edge is black iff `delta_in = +1`. Their white-minus-black count is `-(delta_in + delta_out)/2`. The matched face `φ(v)` is the black face of the outgoing edge, so it is on the left iff `delta_out = +1`, and then it adds 6 units. ∎

**Theorem 2.4 (disk identity) [PROVED-HERE].** The rotation number of `γ` in the state's flat structure is `-J(γ)`, by 2.3. A simple cycle that avoids the roots bounds a disk all of whose interior vertices are flat, by 2.1. By 2.2 its rotation number is `+1` if it is counterclockwise and `-1` if it is clockwise. Hence `J = -1` or `+1`, which is Lemma 4.1 of the OpenAI paper.

With (1.4) the identity becomes orientation-free:

    every disk bounded by a cycle of chosen edges of a state has exactly one more white face than black faces: W = B + 1.

[COMPUTED: `exp_disk` (P1), 3264 of 3264 random chosen-edge cycles over 262 rooted instances with at most 12 vertices. `exp_lattice2`: all 17,312 relative cycles of random pairs of (not necessarily disjoint) states satisfy `W = B + 1`.]

**2.5 The general version, for any cycle [PROVED-HERE].** Let `s` be any state and `C` any simple cycle avoiding the roots. Let `m` count the vertices of `C` whose matched face lies inside. Gauss-Bonnet with 2.1 gives

    B - W = 2m - h + 2.

For a chosen-edge cycle `m = l`, and with `3(B - W) = 2l - h` this forces `B - W = -1`. [COMPUTED: `exp_disk` (P2), 49,680 of 49,680 cycle-state samples.]

**Where the 3 comes from.** One edge of `T` is one third of a turn of the colour map around `Δ`, and one unit of angle is `π/3`. A full rotation `2π` is six units. Along a chosen-edge path each unit of `delta` costs two units of turning (2.3), so a full rotation corresponds to `delta`-sum 3. A one-line slogan: *a state is a flat structure in which every chosen-edge cycle turns once, while the folding map wraps it once backwards around the triangle.*

**2.6 The cancellation sign, topologically.** In Lemma 5.2 a `Q_s`-cycle reversal changes `J` by `∓2`. The reversed cycle `Z` is a chosen-edge cycle for `r`, so its own winding is `±1`. Each triangle on `Z` changes its `r -> s` step by twice its `r -> u` step, so `J` changes by `2·wind(f∘Z)`. That is why the cancellation phase is a sign. [LIT: OpenAI Lemma 5.2; restated.]

## 3. The final step: Jordan curve, tree-cotree, Alexander duality

**Lemma 3.1 [PROVED-HERE].** Let `P ⊆ E(T)` contain exactly one edge of every face, and let `F` be the dual edges of `E(T) \ P`. Then:

1. `P*` is a perfect matching of `G`, and `F = G - P*` is a 2-factor with `c` cycles.
2. `S^2 \ F` deformation retracts onto the graph `(V(T), P)`.
3. Hence `b0(P) = c + 1` and `b1(P) = c - 1`. In particular `F` is a Hamiltonian cycle iff `P` is a forest. When it is, `P` has exactly two components, which are the two induced trees, and each side of the Jordan curve `F` is a disk (Schoenflies) retracting to its tree.

*Proof.* (1) Each face has exactly two unselected sides. Since every edge lies in two faces, a selected edge is the selected edge of both of its faces, so `P*` is a perfect matching. (2) Draw each cycle of `F` crossing its edges once. Inside every face the arc of `F` cuts off the corner where the two unselected sides meet. The two pieces are a corner piece, which retracts radially to its vertex, and an edge piece, which retracts onto the selected edge. The retractions agree on shared boundary segments: each half-edge goes to its vertex, and a selected edge stays fixed. (3) Alexander duality for `c` disjoint circles in `S^2` gives `H̃_0(S^2 \ F) = Z^c` and `H_1(S^2 \ F) = Z^{c-1}`. An edge of `T` with both ends in one component of `P` does not cross `F`, so it is selected. That is inducedness. ∎

This replaces the counting in OpenAI §6.2 and Li Lemma 30 by one homotopy equivalence. It also gives the clean equivalence behind the whole proof:

> **Hamiltonian cycles of `G`** = **perfect matchings `M` of `G` whose dual edge set `M*` is acyclic in `T`.** The number of cycles of `G - M` is `1 + b1(M*)`.

The edge-count form appears in the papers through Lemma 2.1 and Euler's formula. The equivalence between Hamiltonicity and a partition into two induced trees is due to Stein (1971) and Alt-Payne-Schmidt-Wood (2016, Lemma 5), as cited in the OpenAI paper. I could not find the identity `c = 1 + b1(M*)` stated in that form. I believe it is folklore, but I have no citation.

**3.2 Selected-edge acyclicity, topologically [PROVED-HERE, a restatement of OpenAI Lemma 6.2].** Suppose a cycle `Z` of `P0` existed. Its edges are chosen edges of the state `s`, so `wind(f∘Z) = -1` by Theorem 2.4. But `P*` matches the faces inside `Z` black-to-white, except across the boundary edges of `Z`. Hence `B - W = 2l - h = 3(B - W)`, so `wind = B - W = 0`. The contradiction is a winding number 0 against a winding number -1.

**3.3 [PROVED-HERE] Hamiltonicity as a nodal-line condition.** A 2-colouring of `V(T)` gives a Hamiltonian cycle iff no triangle is monochromatic and both colour classes induce connected subgraphs. If no face is monochromatic, the monochromatic edges form a `P` as in 3.1, with `b0(P) = 2` exactly when both classes are connected. In continuous language: a function on `S^2` whose zero set crosses every face and has exactly two nodal domains. §6 explains why this is the opposite of Courant-type behaviour.

**3.4 Tree matchings inside the set of Hamiltonian cycles [PROVED-HERE, COMPUTED].** Let `Φ` send a Hamiltonian cycle avoiding `e0*` to its state: orient `P - e0` towards the roots and let `s(t)` be the tail of the selected edge of `t`. Then `Φ` is injective onto valid states. The recovery map of OpenAI §6 is a section of `Φ` over the tree matchings. So tree matchings are in bijection with the Hamiltonian cycles avoiding `e0*` whose state is a tree matching. Equivalently, the "white parent map" `y -> t(y) -> next white face around s(t(y))` is acyclic. [COMPUTED: `exp_ham`, 166 rooted instances, V ≤ 14. The recovery is injective in every one; the inclusion is strict in 109 of 166, for example V = 8 with 2 tree matchings out of 4 avoiding cycles. Instances with no pair have avoiding cycles, but none of them yields a tree matching.]

## 4. The states as a topological space

**4.1 Distributive lattice [LIT, COMPUTED].** Under clock moves the states of a planar trinity form a connected distributive lattice (Hine-Kálmán, arXiv:1808.06091, main theorem for genus 0). In our colouring a clock move rotates the three matched corners around an empty white triangle, or around a separating triangle. These are exactly the pairs of states whose difference is a single `D`-cycle of length 3. [COMPUTED `exp_lattice`: connected, acyclic, one source and one sink in all 166 rooted instances, V ≤ 14.] The order complex has a minimum, so it is a cone and contractible. That is a true but useless answer to "what is its topology".

**4.2 The lattice height is a signed enclosed area [PROVED-HERE for one move; COMPUTED in general; CONJECTURE for all triangulations without separating triangles].** For states `r, s`, let `D(r,s)` be the cycles of `r(t) -> s(t)` over the faces where they differ. Then

    height(s) - height(r) = Σ_{C ∈ D(r,s)} (-J(C)) · W_in(C),

the signed number of white faces enclosed, with `W_in = B_in + 1` by the disk identity. [COMPUTED `exp_sepcheck`: 17,153 of 17,153 sampled pairs in triangulations without separating triangles. It fails in 629 of 10,352 samples from triangulations with separating triangles, because there one clock move around a separating triangle encloses more than one white face.] This is the Thurston-style height function: the lattice is graded by enclosed white area.

**4.3 The root-polytope ball [LIT, COMPUTED].** For each colour class `c`, let `G_c` be the bipartite plane graph formed by the edges of `T` whose endpoints avoid colour `c`. Then:

- For every state `s`, the edges of `G_c` not in `Q_s` form a spanning tree of `G_c`. Their duals form an arborescence of `G_c*`. (Tutte's tree trinity theorem, in Kálmán, *Adv. Math.* 244 (2013), proof of Thm 9.9.) So `Q_s` is the union of three cotrees, one in each `G_c`.
- Kálmán-Murakami (arXiv:1305.4925, Thm 1.1 and Prop. 1.2) show that these trees index the maximal simplices of a shellable triangulation of the root polytope `Q_{G_c}`, which is a ball.

So for each colour the states are the facets of a shellable triangulated ball. [COMPUTED `exp_rootpoly`: in all 498 (instance, colour) cases the complement is a spanning tree and the map is injective. Every clock move is a facet adjacency of this triangulation. They coincide in 156 of 498 cases; in the others the triangulation has facet adjacencies that are not clock moves.]

**4.4 Where the tree matchings sit [COMPUTED].**

- In the lattice: the bottom state is a tree matching in 107 of the 135 instances that have tree matchings, and the top state in 95. The tree matchings form an antichain in only 31 instances and an interval in only 20. They are not an order-theoretic feature of the lattice.
- In the Kálmán hypertree polytopes (all six hypergraphs of the trinity, 86 rooted instances, V ≤ 12): 1254 of 1260 tree-matching hypertrees are extreme points of the hull of all hypertrees, against 906 of 1140 for non-tree states. That is a strong bias, but not a characterisation.
- The guess "the unique mate of a tree matching is a tree matching" (it would explain the evenness by a fixed-point-free involution) is **REFUTED**. There are 6 failures, already in triangulations without separating triangles; the first is V = 12, plantri index 2, outer face 0, in `data/sepcheck.json`. In those examples two different tree matchings share one mate `m`, and `Q_m` has a single 3-cycle.

**4.5 The cancellation as discrete Morse theory [PROVED-HERE].** Fix `s`, and let `k` be the number of cycles of `Q_s`. The mates of `s` correspond to the orientations of those `k` cycles (barnette_trees Prop. 2.1), and `J(r,s) = J_ccw(s) + 2·#{clockwise Q-cycles}`. So, graded by `(n + J)/2`, the mates form the Boolean lattice `2^[k]`, which is the augmented face poset of the simplex `Δ^{k-1}`. The cancellation "reverse the first cycle" is the standard cone collapse: an acyclic matching with no critical cell if `k ≥ 1`, and one critical cell (the tree pair) if `k = 0`. [COMPUTED `exp_morse`: in all 445 states with mates there are `2^k` mates, the `J`-levels are binomial, and the signed sum is the indicator of `k = 0`.]

Algebraic Morse theory therefore says: the chain complex `C = ⊕_s C̃_*(Δ^{k_s - 1})[shift]` (basis: pairs; differential: reversing a clockwise `Q`-cycle) has homology free on the forest pairs. The differential preserves `ω(s)`, so

    Z(z) = graded Euler characteristic of H_*(C) = Σ_{tree pairs} ε · z^{ω(s)}.

The `D`-regrouping is a second acyclic matching on the same graded set: every undirected `D` has at least one cycle, so its orientation cube has no critical cell. It does not preserve `ω`. Consequently `Z(1) = 0` for every instance: the ungraded Euler characteristic vanishes, and the tree pairs carry equal numbers of both signs (barnette_trees Thm 5.2, the evenness). The proof works because the `ω`-grading survives one matching and not the other. That is the pattern of a graded Euler characteristic, such as an Alexander polynomial computed as `χ` of knot Floer homology, where one differential preserves the Alexander grading. The analogy is made sharper by the next point. The leading coefficient at `(z - 1)^{c_min}` is a sum over minimal `D` of products of enclosed areas (fluxes), which has the shape of Hosokawa-Torres leading coefficients. That last remark is a HUNCH.

Alternative reading [PROVED-HERE]: a pair `(r,s)` is a Forman combinatorial vector field on the 1-skeleton `H`, whose critical edges are the `s`-spokes and whose only critical vertex is the centre of `t0`. Pair each point `r(t)` with the spoke `(r(t), t)` and each centre `t` with `(t, u(t))`. Its closed V-paths are exactly the directed `Q_s`-cycles. **Tree pairs are the gradient fields**, and the cancellation reverses a closed orbit. A tree matching extends to a perfect discrete Morse function on the sphere complex `X_H` (1-skeleton `H`, one 2-cell per white face). It has two critical cells: the outer centre, and the white face `y0`. Its gradient pairs the tree `H - s` downward and the dual tree `W_s` upward. **Barnette's theorem is equivalent to: `X_H` has a perfect discrete Morse function whose upward-paired edges form a perfect matching of `B`.**

**4.6 A parity, and an oriented path-following reading [PROVED-HERE conditional on barnette_trees Thm 5.3].** The marked walk of the constructive paper alternates two sign-reversing involutions, `β` (forest) and `α` (orientation). Orient each `α`-edge from sign `+` to `-` and each `β`-edge from `-` to `+`. Every node then has in-degree and out-degree at most one, so the graph on marked pairs is a disjoint union of directed paths and cycles. Each node has a polynomial-size description and its neighbours are computable in polynomial time. So each phase of the walk is an instance of END-OF-LINE: the oriented (PPAD-type) analogue of Thomason's lollipop, which is the unoriented (PPA) parity argument for Hamiltonian cycles in cubic graphs. Whether the restarts between phases can be merged into a single END-OF-LINE instance, which would put "find a Hamiltonian cycle in a Barnette graph" in PPAD, is open here (see ROUTES.md R9).

## 5. Floer and trinity dictionary

Everything in this section is checked against the text of the sources in `research/2026-11-14_sol_machinery-literature/source-text/`. Colour convention: OpenAI's black faces are the white triangles of Hine-Kálmán, JKR and Kálmán.

**5.1 Two trinities [LIT, PROVED-HERE for the identification].**

- *The trinity `T`.* The Eulerian triangulation with its vertex 3-colouring is itself a trinity. Its three graphs are the colour-pair graphs `G_c`. States are Tutte matchings (Kálmán 2013 §9.2, Berman's theorem, Thm 9.10).
- *The trinity `T'` of the Barnette graph.* Put a point in every face of `T` and join it to the face's corners. Keep the edges of `G` and drop the edges of `T`. The result `T'` is a triangulation with points `V(T)`, black centres and white centres, properly 3-coloured. Its three graphs are `H` (black spokes, which is Li's `G_FB`), `H_w` (white spokes) and **`G` itself**. So the Barnette graph is one of the three graphs of a trinity whose other two are the face-incidence graphs used by the proof.

**5.2 What a state is in Floer terms [LIT].**

- Kálmán (2013) Thm 10.1, Cor. 10.3 and Thm 10.5: each Tutte matching of a trinity determines a hypertree in each of the six hypergraphs of the trinity, and each hypertree arises from exactly one Tutte matching.
- JKR Thm 1.1: for a plane bipartite graph `Γ`, the support of `SFH(S^3 - F_Γ, L_Γ)` is affinely the hypertree set `Q(E,R)`. Here `L_Γ` is the positive special alternating link given by the median construction, and `F_Γ` is its Seifert surface, which retracts to `Γ`. JKR §1 also quotes [5, Cor. 6.11]: each nonzero group is `Z`, all in one `Z/2` grading.

Together: **a state is a generator of `SFH(S^3 - F_{G_c}, L_{G_c})`, one for each supported relative spin^c structure, for each of the three links `L_{G_c}` built from the colour-pair graphs of `T`.** The number of states, the trinity arborescence number, is the total rank of each of these Floer groups. [COMPUTED `exp_hyper`: the hypertree map is injective for all six hypergraphs in all 86 rooted instances with V ≤ 12.]

**5.3 Pairs, `D`, `Q_s`, `J` [PROVED-HERE as restatements; their Floer meaning is a HUNCH].**

- `Q_s` is the union of three cotrees, one in each `G_c` (4.3). Its duals are the three arborescences. A pair `(r,s)` therefore gives two triples of arborescences that disagree at every face.
- `J(r,s)` is the colour winding number (1.3). For generators of a Floer complex, a grading difference is computed from a domain with boundary on the attaching curves (Lipshitz's index formula `μ = e(D) + n_x + n_y`, with `e` the Euler measure). Lemma 2.5 has exactly this shape: Euler-measure-type counting plus a correction at the corners where the states sit. I have not built a Heegaard diagram in which states are intersection points and the `D`-cycles bound Whitney disks. That would be the test. **HUNCH.**
- Berman's theorem (all expansion terms of the determinant have the same sign) is the Floer-side statement that all generators sit in one `Z/2` grading (JKR quoting [5, Cor. 6.11]). The disk identity proves Berman's theorem: every relative cycle has odd length, so every relative permutation is even (barnette_trees Lemma 6.1).

**5.4 Does "there is a state with `H - s` a tree" have a meaning? Yes: one spin^c structure decides.** A tree matching is a spanning tree of `H` with two prescribed degree vectors:

- on the black side, `f = 1` on `A` and `2` on `t0`. This is a hypertree of the hypergraph whose vertices are the points and whose hyperedges are the black faces;
- on the point side, `g(x) = deg_H(x) - 2` at non-roots and `deg_H(x) - 1` at roots. This is a hypertree of the hypergraph whose vertices are the black centres and whose hyperedges are the points.

JKR's Theorem 1.1 is stated for a plane bipartite graph `Γ` with colour classes `E, V` and regions `R`, and identifies the support of `SFH(S^3 - F_Γ, L_Γ)` with `Q(E,R)`: hypertrees with vertex set `E` and hyperedges `R`. Take `Γ = G`, the Barnette graph. Then `E` is the set of black vertices of `G` (black centres), `R` is the set of faces of `G` (points of `T`), and `Bip(E,R) = H`. So **`g` is a relative spin^c structure of the sutured complement of the Seifert surface of `L_G`, the special alternating link of the Barnette graph itself.** Likewise `f` belongs to the link of `H_w`, the white spoke graph, whose regions are the black faces.

By Lemma 2.1 of the OpenAI paper (the complement of a spanning tree dualises to a spanning tree), `g` is a hypertree iff the following holds. In the multigraph on white faces whose edges are the duals of the spokes, coloured by their point, choose exactly one edge from each non-root point's colour class. The duals of the spokes at `x` form the cycle of white faces around `x`. We need the chosen edges to form a spanning tree: a **rainbow spanning tree**. The black side is the same with colours given by black faces.

**Theorem 5.4 [PROVED-HERE, conditional on barnette_trees Thm 1.2].** For a rooted Eulerian triangulation the following are equivalent:

1. a tree matching exists;
2. `g` is a hypertree, i.e. the spin^c structure `g` is in the support of `SFH(S^3 - F_G, L_G)`;
3. no separating triangle has black inner boundary.

*Proof.* (1)⇒(2) is immediate. (2)⇒(3): let a separating triangle have black inner boundary, with `I` strictly interior vertices. The disk count gives `B_d = I + 1` and `W_d = I` (barnette_trees §3). The cycle of white faces around an interior point uses only white faces inside the disk, so a rainbow choice picks `I` edges on the `I` inside white faces, and they cannot be acyclic. (3)⇒(1) is barnette_trees Thm 1.2 ((iii)⇒(ii)⇒(i)), whose proof uses the whole cancellation argument. ∎

[COMPUTED `exp_rainbow`, rainbow spanning trees by matroid intersection, all 826 rooted instances with V ≤ 16: 580 with a pair, all with `g` and `f` realisable; 246 without a pair, all with `g` not realisable and `f` realisable. Cross-check: `exp_degpoly` finds the same split by brute-force enumeration of spanning trees on its 66 instances with V ≤ 10. In the 6 instances without a pair the two-sided target is also outside the convex hull of two-sided degree vectors.]

*What this does and does not give.* Within the Floer dictionary the key lemma reads: **"if the spin^c structure `g` is supported, then some spanning tree realising it also has the black-side degrees `f`."** The one-sided condition (2) is a Rado/Hall-type inequality family (Kálmán's polytope description), checkable as in OpenAI §3. The exchange step from one-sided to two-sided is a three-matroid intersection. It is exactly as hard as the original key lemma, and here it is proved only through the cancellation. So the Floer reading localises the difficulty but does not remove it. It suggests one concrete new question (ROUTES.md R6): is there a direct exchange argument, for example a walk through rainbow spanning trees that fixes the black-side degrees one face at a time?

## 6. Continuous versions [HUNCH, with tests]

**6.1 Dessin [PROVED-HERE, given the Riemann existence theorem].** With `β` as in 1.4, `T = β^{-1}(unit circle)`. With `γ = β^3`, which has zeros of order 3 at black centres, poles of order 3 at white centres and value 1 at the vertices, the Barnette graph is the dessin `G = γ^{-1}((-∞, 0])`: its edges are the preimages of the rays through the midpoints of the equator arcs. A cubic bipartite plane map is a dessin with passport `[3^k, 3^k, (d_v)]`. Since cubic bipartite plane graphs are 3-face-colourable, every such dessin is a perfect cube `γ = β^3`. In this language:

- `delta` is `(1/2πi) d log γ` along the edges.
- A state is a system of distinct representatives for the cycles of the monodromy permutations `σ_0, σ_1, σ_2` on the `k` black sheets. Leave out the three cycles through the base sheet `t0`, and the base sheet itself. (Genus 0 means the total number of cycles is `k + 2`.)
- `J` is the winding of `β` along the cycles of `s∘r^{-1}`.

**6.2 Cubic differential [PROVED-HERE computation].** The equilateral metric on `T` is `|q|^{2/3}` for the meromorphic cubic differential

    q = β*( dz^3 / (z^3 - 1)^2 ),

which has order `d_v - 3` at a vertex of degree `2 d_v`: a pole at degree 4, regular at degree 6, a zero at degree 8 and above. Total order `-6`. Along `G`'s edges and along the spokes `q` is real. Along `T`'s edges it is imaginary. A state chooses, at each black centre, one of the three positive real directions of `q` (one cube root of `q`). It is a choice of sheet of the spectral cover `λ^3 = q` over each black centre. A Hamiltonian cycle is a closed real-trajectory polygon through every centre, turning `±π/3` at each. Gauss-Bonnet then gives `L - R = 2(|V2| - |V1|)`, the turning imbalance against the tree sizes, which is trivially true combinatorially. The link to harmonic maps into `A_2` buildings (Katzarkov, Noll, Pandit and Simpson relate cubic differentials and spectral networks to harmonic maps to buildings of type `A_2`; I have not opened their paper) is a HUNCH. The only concrete content found is that `T` is an `A_2` chamber complex and the folding map is a retraction onto one chamber.

*Test for the spectral-cover HUNCH:* if the sheet choice carried the tree property, two states with the same colour vector `κ_s(t) = c(s(t))` should never differ in tree-ness. Not run (see ROUTES.md R11).

**6.3 Nodal lines [COMPUTED].** By 3.3 a Hamiltonian cycle is a sign pattern with two nodal domains whose nodal line visits every face. Courant-type theorems give few nodal domains for low eigenfunctions, but their nodal lines avoid most faces. High eigenfunctions visit every face, but have many domains. [COMPUTED `exp_nodal`, all plantri Eulerian triangulations with V ≤ 14.] Of 364 Laplacian eigenvectors without zero entries, 17 (4.7%) have a sign pattern that is an induced-tree partition, mostly at high eigenvalues. Among all 2-colourings of the triangulations with V ≤ 12 the rate is 258 of 19,857 (1.3%). Eigenvectors are enriched about 3.6-fold, but they are no mechanism.
