# Where the formal proof and the paper differ

Summary.
1. The formal statement is Barnette's conjecture as usually stated. All five definitions match (section A), and the build shows that `main` uses only `propext`, `Classical.choice` and `Quot.sound` (`COMPUTED`, `build/`).
2. The formal proof does not follow the paper's route in four places. It uses an algebraic dual instead of a sphere embedding, the H- form instead of Theorem 2.2, a polynomial instead of `exp`, and a flow on `G` instead of spoke circulations. Each change removes topology or analysis. None of them adds a hypothesis.
3. The Lean proves three facts the paper uses without a word. The inside of a `T`-cycle has connected sides and no pinch vertex. A `T`-vertex's link is a face cycle of `G`. Capping a separating triangle gives a graph with a dual again.
4. I found no step of the paper that the formalisation contradicts, and no hidden extra hypothesis in the paper. Every difference is a change of route or of representation.
5. Not formalised: Corollary 7.2 (Pfaffian, `P4`). Corollary 7.1 is proved only in algebraic-dual form, not restated for drawings.

Item numbers are referred to from other files. Paths are relative to `lean/OAI/Combinatorics/Hamiltonian/`.

## A. The top-level statement, definition by definition

Barnette's conjecture as usually stated: every 3-connected cubic bipartite planar graph is Hamiltonian (Grünbaum 1969, as cited by the paper [6]; same wording in Alt-Payne-Schmidt-Wood 2016). The formal statement is `MainStatement` (`Model.lean:42`). I printed it after the build (`build/axioms.out`) and printed the Mathlib definitions it uses (`build/defs.out`).

| Notion | Usual meaning | Formal definition | Verdict |
| --- | --- | --- | --- |
| graph | finite, simple, undirected | `SimpleGraph V` with `[Fintype V]`. Mathlib's `SimpleGraph` is loopless and has no multiple edges | match |
| cubic | every vertex has degree 3 | `G.IsRegularOfDegree 3`: `∀ v, G.degree v = 3` | match |
| bipartite | vertex 2-colouring with no monochromatic edge | `G.IsBipartite`, which unfolds to `G.Colorable 2 = Nonempty (G.Coloring (Fin 2))` | match |
| planar | has a crossing-free drawing in the plane by Jordan arcs | `Nonempty (PlaneEmbedding G)` (`Model.lean:10`): injective `point : V → ℝ × ℝ`; for every adjacent pair an injective continuous `Path` between the points; the reverse arc is the reversed path; an arc meets a vertex point only at its own endpoints; two arcs share an interior point only if they are the same edge | match. The reverse-arc field is harmless, since one arc per edge can always be reversed. `ℝ × ℝ` carries the product topology, which is the usual one. Not vacuous: the cube has such a drawing by straight segments |
| 3-connected | more than 3 vertices, and deleting fewer than 3 vertices leaves a connected graph | `ThreeVertexConnected` (`Model.lean:33`): `4 <= card V` and for every `S` with `\|S\| <= 2`, `G.induce {v ∉ S}` is `Connected`. Mathlib's `Connected` includes nonemptiness, which `\|V\| >= 4` guarantees | match. Same wording as the paper's Section 1 |
| Hamiltonian | has a cycle through every vertex exactly once | `∃ v (p : G.Walk v v), p.IsHamiltonianCycle`. Mathlib: `p` is a cycle (nonempty trail, no repeated vertex except the base) and `p.tail` visits every vertex exactly once | match. A spanning 2-factor with several components does not qualify |

The definitions block of `Model.lean` is textually identical to the challenge file `ComparatorChallenges/BarnetteHamiltonian.lean` (`COMPUTED`, `diff`, see `build/README.md`). The challenge config permits exactly `propext`, `Quot.sound`, `Classical.choice`. The theorem is universe-polymorphic in the vertex type, and `main` removes the decidability instances by `Subsingleton.elim` (`Main.lean:47`), so the instance arguments do not restrict anything.

**Axioms.** `#print axioms OAI.Barnette.main` prints `[propext, Classical.choice, Quot.sound]` (`COMPUTED`, Lean 4.34.1, Mathlib `d13f23b7`, `build/axioms.out`). Grep: no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `opaque`, `implemented_by`, `extern`, `set_option`, `macro`, `elab` in the 31 files. 30 uses of plain `decide` on finite facts about `Fin 3` and `Fin 2`. The proof is classical and not constructive. It uses `Classical.choose` throughout, and Hall's theorem where the paper gives explicit constructions (items 9 and 19).

## B. Representation: what "planar" and "dual" mean inside the proof

**1. No faces, no rotation system, no Jordan curve theorem.** Planarity is used once, in `PlaneEmbedding.exists_exact_dual` (`ExactDual.lean:116`). It produces a second network `D` on the edge set of `G` with `ker ∂_G = im ∇_D` and `ker ∂_D = im ∇_G` over ℝ, with both graphs connected (`Duality`, `Network.lean:145`). This is Whitney's algebraic dual with orientations. The paper's `T = G*` is `D`. The paper says "fix a sphere embedding" and "the sphere dual". The Lean spends 1,078 counted lines proving that a drawn graph has an algebraic dual, by this route:
   - thicken the drawing. Branch sets are a vertex plus the first third of each incident arc. Cores are the middle thirds. Disjoint compact sets have a uniform positive separation (`uniform_thickening`);
   - the grid cells of size `ε/2` meeting a connected compact set form a connected set of the square grid (`cells_connected`). This gives a minor model of `G` in the grid (`exists_lattice_minor_model`), and it fits in a finite box (`lattice_minor_in_rectangle`);
   - the box grid has an explicit dual: inner unit squares plus one outer face (`grid_duality`, `Rectangle.lean:180`);
   - algebraic duality survives deletion and contraction (`Duality.minor`, `CappedDuality.lean:62`). Deleting an edge in the primal contracts it in the dual. A minor of a graph with a dual therefore has a dual.

   The only topology used is compactness, connectedness and uniform separation. The Jordan curve theorem never appears. The same `Duality.minor` is reused in Section 7 for the caps (item 21).

**2. The faces of `T` are the vertices of `G`.** A face of `T` is `D.Triangle (N.star v)`: the three edges at a vertex `v` of `G` form a triangle of `D` (`CutSpaces.lean:222`, built by `triangle_of_flow`). Black and white faces of `T` are the colour classes of `G`. The root face `t0` is a black vertex `root` of `G`.

**3. Orientation is local and comes from the algebra.** Each triangle stores a cyclic labelling of its corners. `oriented_face` (`Circulation.lean:100`) chooses it so that the triangle's cycle flow in `D` equals `∇_G 1_v`. All triangle orientations are then coherent, because they all come from the one pair of oriented incidence matrices. The paper's `δ(v,w)` ("black face on the left") becomes `indexDelta` of the corner labels inside the black triangle (`Triangle.index_delta`, `TriangleSystem.lean:291`). No global notion of counterclockwise is defined.

**4. The inside of a cycle.** A simple cycle `C` of `T` is a minimal flow of `D`. Duality writes it as `c · ∇_G 1_A` with `c = ±1` and `A` a set of vertices of `G` (faces of `T`) not containing the root (`Duality.circuit_cut`, `FlowCircuits.lean:71`). `A` is "the disk", and `c` decides "counterclockwise". Minimality makes `cut(A)` a bond, so `G[A]` and `G[A^c]` are connected (`Bond.connected_shore`). The paper's sentence "its bounded disk contains no root, because the roots are on the outer-face boundary" is true here by definition: the inside is the side that misses the root face.

## C. Differences section by section

### Theorem 1.1 and Section 2

**5. 3-vertex-connected is used only to get 3-edge-connected.** `main` converts at once (`cut_card_three`, `CutSpaces.lean:51`, which needs `|V| >= 5`, from `cubic_bipartite_order`). Everything after it, the induction included, assumes `ThreeEdgeConnected` (`Contraction.lean:291`): every edge cut has at least 3 edges. For cubic graphs the two notions are equivalent, and the paper's own proof also passes through "no edge cut of size one or two". The 3-vertex-connected versions of two lemmas, `Duality.simple_dual` and `Duality.cubic_face_triangles`, are in the files but unused (they are superseded by the `_edge` versions in `ThreeCuts.lean`).

**6. "T is simple" and "faces of T are triangles".** The paper argues with Jordan curves: "a dual loop or a pair of parallel dual edges would be a Jordan curve crossing one or two primal edges". The Lean argues algebraically. A loop or parallel pair of `D` is a flow of `D` supported on at most 2 edges, hence a gradient of `G` supported on at most 2 edges, which is impossible without a cut of size at most 2 (`gradient_small_support_edge`, `simple_dual_edge`, 64 lines). "Cubicity gives each dual face a boundary walk of length three, which in a simple graph is a triangle" becomes `triangle_of_flow` (79 lines): a flow with support exactly 3 in a simple graph is a triangle.

**7. Lemma 2.1 is proved only in the form used, and algebraically.** `Duality.complement_connected` (`Matching.lean:79`): if `S` is acyclic in `T`, then `G - S` is connected. Proof: take `f` constant on the components of `G - S`. Its gradient `∇_G f` is a flow of `T` (exactness) and is supported on `S`. A flow supported on a forest is zero (`conserved_supported_acyclic`), so `∇_G f = 0` and `f` is constant on the connected graph `G`. Three lines of linear algebra. The paper proves it by contracting a spanning tree. The "spanning tree ↔ spanning tree" half of Lemma 2.1 never appears as a lemma.

**8. States are defined for an abstract triangle system.** `TriangleSystem` (`TriangleSystem.lean:9`) is a set `A` of triangles, each with three labelled vertices, such that two triangles sharing two vertices coincide. That is the paper's "every edge has a unique black face". A state picks a corner index per triangle and is bijective onto `X`. Sections 5.1 and 5.3 are proved at this level of generality (item 15).

### Section 3 (Proposition 3.1)

**9. Max-flow is replaced by Hall's theorem, twice.** `two_matchings` (`BMatching.lean:286`) reduces "a degree-2 subgraph of the incidence graph" to a perfect matching in a gadget graph (each `x ∈ X` and `t ∈ A` doubled, each incidence a vertex on both sides), proves Hall's condition from (3.1) (`gadget_hall`, 92 lines), and splits the resulting 2-regular bipartite graph into two perfect matchings by Hall again (`regular_matching`). The paper splits by alternating along cycles. The capacity condition (3.1) is the same.

**10. The density bound (3.2) is proved globally.** The paper applies Euler to each connected component `K` of `T[U]`, with a case split on `p >= 4`. The Lean proves `|E(T[U])| + 2 <= |U| + #regions` for all of `T[U]` at once, from a rank inequality (`induced_euler_bound`, `Contraction.lean:121`). A "region" (a face of `T[U]`) is a connected component of `G` minus the dual edges of `T[U]`, and its boundary length is the `rim` (`Contraction.lean:202`). (3.3) becomes `region_balance_rim` plus `rim_defect` (`3β = 2b - d, b <= d, d >= 4 ⊢ β <= d - 4`), the same parity and divisibility argument as the paper.

**11. Where "no separating triangle" is used.** It is `TrivialThreeCuts`: every 3-edge cut of `G` has a side with one vertex (`Contraction.lean:293`). It is used exactly where the dependency audit `research/2026-11-14_fable_dependency-graph/audit-openai.md` (F1) puts it: a region of rim 3 is a single vertex of `G` (an actual face of `T`) or the complement of the root (`rim_three_cut`, `rim_three_no_internal`, `complement_singleton_root`). Nothing in Sections 4-6 uses it.

### Section 4 (disk identity)

**12. The disk identity is stated on `G`.** `state_disk_delta` (`StateDisk.lean:442`): for a state and a cycle `C` of `T` each of whose edges `v_i v_{i+1}` lies in the black triangle assigned to `v_i`, there are `A` and `c = ±1` with cycle flow `c·∇1_A`, `|cut A| = 2|blackCut A| + 3` and `δ`-sum `-3c`. Here `|cut A| = h` (cycle length) and `blackCut A` = cycle edges whose black triangle is inside (`l`). So the identity reads `h = 2l + 3`, which is the paper's `2l - h = -3`.

**13. The three counts, and the facts the paper skips.**
   - (4.1) Euler for the disk: `region_euler` (`DiskRegions.lean:252`): `|A| + |U| = |E(A)| + 1`, where `U` is the set of vertices of `T` on triangles in `A`, and `E(A)` is the set of edges with an end in `A`. Proved as a dimension count: the cycle space of the "region network" has dimension `|A|` (`region_cycles_eq_range`, 54 lines). It needs both `G[A]` and `G[A^c]` connected (item 4) and the region network connected (`region_connected`, 78 lines). The paper writes "Euler's formula for the triangulated disk" and does not say why the inside is a disk.
   - side counting: `cubic_region_count`, `cubic_black_region_count`, counted on the cubic graph.
   - (4.2) `B = I + l`: `state_disk_count` (`StateDisk.lean:260`, 114 lines, the longest proof in the development). The proof writes `U` as (vertices matched to black triangles in `A`) ∪ (vertices of `C`) and computes the intersection. This needs a fact the paper never states: **a vertex of `T` that touches triangles on both sides lies on `C`** (`mixed_corner_on_boundary`, 29 lines). This is the "no pinch point" property of the disk. It rests on `Duality.vertex_flow_circuit` (59 lines): the link of a vertex `z` of `T` is a face cycle of `G`, a circuit, because `T - z` is connected (`faces_vertex_deleted_connected`).
   - The arithmetic `(4.1), (4.2) ⇒ 2l - h = -3` is one `omega` call (`disk_boundary_imbalance`). The paper's version, with `B, W, I, h, l`, is stated separately as `disk_count_identity` (`PairPhases.lean:22`) and is unused.

**14. The disk identity is never used to make `J` an integer.** The paper (5.1) says `J = (1/3) Σ δ` is an integer by Lemma 4.1. The Lean keeps `rawIndexSum = Σ δ` and defines `phase n = I^(n/3)` with integer division (`PairPhases.lean:9`). The cancellation needs only `phase(n ± 6) = -phase(n)` (`phase_add_six`), which holds for every integer `n`. Integrality is used in Section 5.3 only cycle by cycle (`phase_sum` needs each summand divisible by 3, and each `D`-cycle has `δ`-sum `±3`). `PROVED-HERE`: `(n+6) div 3 = n div 3 + 2` for floor division, and `I^2 = -1`.

### Section 5 (cancellation)

**15. Sections 5.1 and 5.3 are proved for an abstract triangle system.** `forest_pair_of_disk_circulation` (`PairPolynomials.lean:423`): for any `TriangleSystem` with at least one pair, if (H1) every reversible `Q_s`-cycle has index sum `±3`, and (H2) every cycle of every `D` has index sum `-3` with positive weight slope or `+3` with negative slope, then some pair has `Q_s` acyclic. Topology enters only through (H1) and (H2), which `ColoredDual.opposite_disk` and `paired_sign` (`Forest.lean`) supply from the disk identity. The paper interleaves the two levels.

**16. `Z(x)` is a polynomial, not an exponential sum.** `term w P = phase(J) · ∏_t (1 + a(t, s(t)) X)` in `ℂ[X]` (`PairPolynomials.lean:224`). The weight depends only on `s`, so Lemma 5.2 goes through unchanged. It is a product over triangles, so the group of a fixed `D` factorises over cycles (`group_sum_product`): `∏_C phase(δ_C) (∏_{t∈C}(1 + a_right X) - ∏_{t∈C}(1 + a_left X))`. Each factor is `X · (L+(C) - L-(C)) + O(X^2)` (`cycle_factor_witness`). The lowest coefficient of the whole sum is `(-i)^{c_min} Σ (positive)` (`common_phase_sum_ne_zero`). This is the paper's Taylor argument with `exp(x a)` replaced by `1 + aX`, and it needs no analysis. `PROVED-HERE` that the replacement is legitimate: the paper uses only that the weight is multiplicative over triangles, equal to 1 at `x = 0` and has derivative `a` there.

**17. Lemma 5.3 is replaced by one flow on `G`.** The paper builds weights `a(t,v)` on spokes from boundary circulations along dual paths, then needs "the spoke curve is simple and counterclockwise" with an isotopy argument (item N4c of the audit). The Lean takes a flow `α` on `G` with `∂α = whiteCharge`: `+1` at every white vertex of `G` (white triangle of `T`), `-#white` at the root, `0` elsewhere (`Circulation.lean:183`). It exists because the charges sum to zero and `G` is connected (`boundary_of_sum_zero`). Each black non-root vertex has charge 0, so `α` circulates around each black triangle, and the weights are the potentials of `α` around the triangle (`ColoredDual.weights`). Then for a `D`-cycle with disk `A` and sign `c`, the slope is `Σ α · (cycle flow) = c · #(white triangles in A)` (`whiteCharge_cut_integral`). This is positive in the counterclockwise case because some white triangle lies inside: if `A` were all black, every cut edge would have its black end inside and `h = l`, against `h = 2l + 3` (`white_positive_of_boundary`). So the paper's positivity is replaced by a second use of the disk identity. There is no spoke graph `H0`, no dual path and no isotopy. `PROVED-HERE` (reading of the Lean proof): this is the same quantity as the paper's, the number of faces of `H0` inside the spoke curve.

**18. Regrouping by `D` uses permutation cycles.** A pair `(r,s)` gives the permutation `next = r^{-1} ∘ s` of the black triangles. Its cycles are the cycles of `D` (`Pair.next`, `CycleClass`). The group of pairs with the same `D` is in bijection with `CycleClass → Bool`, one orientation bit per cycle (`groupEquiv`). The paper describes `D` as an edge set of `T` and its cycles geometrically. The Lean never needs to know that the cycles of `D` are cycles of `T` until it applies the disk identity, through `pairedCycle` (`Forest.lean:100`).

### Section 6 (recovery)

**19. The tree on the white faces is never built.** The paper deletes the spokes `(t, s(t))` from the spoke graph `H`, gets a spanning tree, dualises it to a tree on the white triangles, roots it at `y0`, and assigns each tree edge to its far end. The Lean works in `G`:
   - `removed` = the `Q_s` edges plus two sides of the root face (`Matching.lean:326`). This set is acyclic in `T` (`removed_acyclic`).
   - by Lemma 2.1 (item 7) its complement in `G` is connected. A count of edges (`removed_card`) makes it a spanning tree of `G` in which every black vertex has degree 2, except the root with degree 1 (`remainder_black_degree`).
   - a perfect matching of `G` inside this tree comes from Hall's theorem (`tree_matching`, `ForestMatching.lean:51`, 98 lines). Hall's condition holds because a forest on `T ∪ Z` has at most `|T| + |Z| - 1` edges, while the `|T|` black vertices of a set send `2|T| - 1` or more tree edges into the white neighbours `Z`.

   So the paper's explicit rooting is replaced by an existence argument. The spoke graph, the faces of `H` and "Temperley's correspondence" do not appear.

**20. Lemma 6.1 by a sink, not by counting.** The paper counts outdegrees per component. The Lean adds two sides of `t0` to `Q_s`, directed from two roots into the third root, and keeps every outdegree at most 1 with the third root a sink. A graph with outdegree at most one and no directed cycle is a forest (`addSink_acyclic`, `Matching.lean:114`). The same principle, "outdegree at most one, so every cycle is directed", is used in Lemmas 5.2, 6.1 and 6.2 alike.

**21. Lemma 6.2 by a cut-balance lemma.** `selectNet_forest` (`ForestMatching.lean:307`): a directed cycle of selected edges is a state cycle for `s`, so the disk identity gives `|cut A| = 2|blackCut A| + 3`. But every edge of `cut A` is in the perfect matching `P`, and `matching_cut_balance` (34 lines) shows that such a cut has `|cut A| = 2|blackCut A|`. The paper's (6.1) is the same count, stated as "count the unique selected edge of every interior face with a sign".

**22. The two induced trees and the Jordan-curve labelling are gone.** The paper ends Section 6 by drawing the dual cycle as a Jordan curve, labelling the vertices of `T` by side, and reading off two induced trees (Theorem 2.2). The Lean stops at "`P` is a perfect matching of `G` containing the prescribed edge, and `P` is acyclic in `T`". Lemma 2.1 then makes `G - P` connected, and a connected 2-regular graph is a single cycle (`cycle_at_of_connected_two`). **Theorem 2.2 is not stated anywhere in the Lean.** The Stein/Alt-Payne-Schmidt-Wood equivalence is not needed in either direction.

### Section 7 (separating triangles)

**23. The induction statement is the H- form.** `matching_strong` (`Gluing.lean:244`) proves, by strong induction on `|V(G)|`: for every cubic, simple, 3-edge-connected, 2-coloured `G` with an algebraic dual and every edge `e`, there is a perfect matching `P ∋ e` with `G - P` connected, i.e. a Hamiltonian cycle avoiding `e`. This is Corollary 7.1 (Kelmans' H-) used as the induction hypothesis. The paper's Theorem 2.2 prescribes a face `t0` and an edge `e0` of it. The face is redundant: once `e0 ∈ P`, both faces at `e0` have `e0` as their selected edge. In `irreducible_matching` the root is the black end of `e`. No colour exchange is ever needed, whereas the paper exchanges colours when `t0` is white, including for the white caps of the induction (audit F11).

**24. Splitting is contraction.** A separating triangle of `T` is a 3-edge cut of `G` with at least 2 vertices on each side (`nontrivial_threeCut_at`). The cap is `G / A^c`, with one new vertex for the other side (`cap`, `ThreeCuts.lean:149`). Its dual exists by `Duality.minor` (`cap_duality`). The paper says "capping each side by a triangle" and treats the pieces as sphere triangulations without comment. The Lean has to prove that the cap is simple, cubic, 3-edge-connected and 2-colourable (`cap_simple`, `cap_cubic`, `cap_threeConnected`, `cap_coloring`). The colour of the new vertex comes from `threeCut_black_card`: the three cut edges have their black ends on the same side. This is the paper's "divisibility by three forces all three signs to be equal", counted in `G`.

**25. Gluing is of matchings, not of trees.** The paper glues two pairs of induced trees along a shared vertex or edge of the separating triangle. The Lean glues two perfect matchings that agree on the 3-cut (`cap_glue_matching`) and shows that the union's complement is connected (`cap_glue_connected`, 48 lines). The prescribed cap edge is the unique cut edge in the first matching (`cap_matching_boundary`).

## D. What is not formalised

**26. Corollary 7.2** (Pfaffian, `P4`-Hamiltonian). Not in the Lean. `lean/docs/180.md` claims only the Hamiltonian cycle ("The selected result is the existence of a cycle visiting every vertex exactly once"). The cert-machine ledger calls the Pfaffian clause "undeclared" (from `research/2026-11-14_opus_history-literature/HISTORY.md`; I did not reread the ledger).

**27. Corollary 7.1 for drawn graphs.** `Duality.connected_complement_matching` is the H- property for graphs with an algebraic dual. There is no theorem stating it for `PlaneEmbedding`. Combining it with `exists_exact_dual`, as `main` does, would take a few lines. It is just not stated.

**28. Theorem 2.2** (two induced trees) is not stated (item 22). Neither is the general Lemma 2.1 for embedded graphs with loops (item 7).

**29. Polynomial-time construction.** Neither the paper nor the Lean claims one. The Lean is less constructive than the paper (Hall's theorem in items 9 and 19, `Classical.choose` everywhere).

## E. Statements where the formal version is stronger or weaker

| Paper | Formal | Comparison |
| --- | --- | --- |
| Thm 1.1 for planar graphs | `main` for `PlaneEmbedding` | equal |
| Thm 2.2: any simple 2-coloured sphere triangulation, any face `t0`, edge `e0 ∈ t0` | `Duality.connected_complement_matching`: any cubic, simple, 3-edge-connected, 2-coloured `G` with an algebraic dual, any edge `e` | equivalent by duality. The formal version has no face parameter |
| Prop 3.1: no separating triangle | `pair_nonempty`: 3-edge-connected and `TrivialThreeCuts` | equal (a separating triangle of `T` is a nontrivial 3-cut of `G`) |
| Lemma 4.1: any state, any simple directed cycle of chosen edges | `state_disk_delta`, same hypotheses | equal. The conclusion adds the disk `A` and the sign `c` as data |
| Lemma 5.2, Prop 5.1 | abstract versions for any `TriangleSystem` plus (H1), (H2) | stronger (more general) |
| Lemma 5.3: weights with positive circulation on every counterclockwise simple spoke cycle | weights with positive slope on every counterclockwise state cycle `D` | weaker, and exactly what (5.3) needs |
| Lemma 6.1: every component of `Q_s` has one root | `Q_s` plus two root sides is acyclic | equivalent for the use made of it |
| Lemma 2.1: any connected embedded graph, spanning trees and forests | acyclic `S` in a simple `T` with algebraic dual `G` | weaker, and enough |
