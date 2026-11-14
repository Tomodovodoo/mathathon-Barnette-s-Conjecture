# What a categorical viewpoint gives for the paired-state proof

Five viewpoints, each with definitions, what it explains, what it proves, and a verdict. Status tags follow `research/BRIEF.md`. Proofs are in `PROOF.md`, runs in `EXPERIMENTS.md`. O, L, T are the OpenAI paper, Li's note and the trees paper.

| # | Viewpoint | Verdict |
| --- | --- | --- |
| 1 | Cutting along cycles: boundary states, gluing, a Temperley-Lieb pairing | substantive. It explains the prescribed edge and both corollaries, and gives one new theorem (conditional on O) and one negative |
| 2 | Trinity and triality: triangle factors, two-root states | the reformulation is worth having. The categorical language adds nothing to it |
| 3 | Homology: complexes whose Euler characteristic is the signed sum | vocabulary only, and the one homological existence criterion I could test fails on the octahedron |
| 4 | Operads and recursions: insertion into faces, vertex contraction | multiplicativity is a small real statement. No deletion-contraction recursion. One monotonicity conjecture |
| 5 | Belyi maps and the permutation triple | vocabulary only |

## 1. Cutting along cycles

### Definitions

A boundary type is a cyclic word `sigma` in `{+, -}^m` whose sum is divisible by 3. A piece of type `sigma` is a simple triangulated disk with properly 2-coloured faces whose boundary is an `m`-cycle and whose boundary faces have the colours `sigma` (`+` for black). Two pieces of types `sigma` and `-sigma` glue to a 2-coloured sphere triangulation.

The boundary states `S(m)` of an `m`-cycle are the pairs (label word, partition of the boundary positions into connected pieces of the two label classes). For Hamiltonian cycles only the states with no inner component matter, and there are `sum_j C(m, 2j) Cat(j)` of them: 3, 8, 20, 50 for `m` = 3, 4, 5, 6 (`COMPUTED`). In the cubic graph `G` such a state is the set of `2j` cut edges used by the cycle together with the non-crossing pairing that says how the paths inside the piece join them. That is a basis diagram of the Temperley-Lieb algebra on `2j` strands, placed on `2j` of the `m` cut edges.

**The functor.** Source: the category whose objects are boundary types and whose morphisms from the empty type to `sigma` are pieces of type `sigma`. I only use and test these "states" and their pairing, not general annuli. Target: modules over `Z[d]`. A type goes to the free module `V(sigma)` on `S(m)`. A piece `D` goes to the vector

```
Z(D) = sum over face-proper labellings of D of  d^(inner components) [state]   in V(sigma).
```

The pairing `V(sigma) x V(-sigma) -> Z[d]` sends two states with the same word to `d^(|pi1 v pi2| - 1)` and to zero otherwise. On Hamiltonian-compatible states `|pi1 v pi2| - 1` is the number of loops of the meander formed by the two pairings, so this is the Temperley-Lieb bilinear form with loop value `d` (`LIT` pointer, from memory and not opened: Di Francesco, Golinelli, Guitter, "Meanders and the Temperley-Lieb algebra", Comm. Math. Phys. 1997).

**Gluing theorem** (`PROVED-HERE`, Proposition 1; `COMPUTED` on 1157 cycles). `<Z(D1), Z(D2)>` is the generating polynomial of the 2-factors of `G` by number of cycles. The number of Hamiltonian cycles is its coefficient of `d`.

So the count of Hamiltonian cycles is not itself multiplicative. It is the linear term of a multiplicative quantity. In physics terms it is the `n -> 0` limit of a fully packed loop model. The same proof gives the statement for annuli (a matrix between two boundary modules, composing by matrix product with the loop weights). I did not test annuli, so that part is a `HUNCH` about a routine extension.

For existence one can forget the counts. Then a piece gives a subset `F(D)` of `S(m)`, the realised Hamiltonian-compatible states, and two pieces glue to a Hamiltonian graph exactly when `F(D1)` and `F(D2)` contain a matching pair. This is a relation-valued version of the same thing.

### What it explains

**Why an edge is prescribed.** For `m = 3` the selection rule (Proposition 2) leaves exactly three states, one for each choice of same-label edge. O Theorem 2.2 says `F(D) = S(3)` for every piece with triangular boundary. Any two full sets glue. The induction over separating triangles in O Section 7 is the remark that fullness at `m = 3` is closed under gluing. The prescription `e0` is not a technical strengthening chosen for convenience. It is the whole boundary state space of a triangle.

**Why the two corollaries are what they are.** Corollary 7.1 (avoid an edge) is fullness at `m = 3` read in `G`. Corollary 7.2 (every 3-edge path extends) is, by Theorem 3, fullness at `m = 4`. O imports 7.2 from Gorsky, Steiner and Wiederrecht. In this picture it is the next entry of the same table.

**Where the table ends.** At `m = 5` fullness fails (`COMPUTED`, Proposition 4): the realised set depends on the piece. So there is no third corollary of the same kind, and an induction that cuts along 5-cycles must carry real boundary data.

### What it proves

- Proposition 1, the gluing formula. `PROVED-HERE`, `COMPUTED`.
- Proposition 2, the selection rule: mono boundary edges carry one third of the boundary sign sum. `PROVED-HERE`, `COMPUTED`.
- Theorem 3, completeness at `m = 4`: for a piece with quadrilateral boundary and an interior vertex, every pattern allowed by the selection rule and the chords is realised. `PROVED-HERE` conditional on O Theorem 2.2 and Corollary 7.2, with one sub-case resting on a finite `COMPUTED` check. Checked independently on all cuts up to 15 vertices.
- Proposition 4, failure at `m = 5` and `m = 6`. `COMPUTED` up to 13 vertices, witness with 9 vertices.

None of this is a new proof of Barnette's conjecture. Theorem 3 is deduced from it.

### What an inductive proof along longer cuts would need

Fix a class of pieces and a property `Pi` of subsets of `S(m)`, one for each boundary type, such that

1. every piece in the class has `Pi`, and
2. any two subsets with `Pi`, of opposite types, contain a matching pair.

For `m = 3` and `m = 4`, `Pi` is "everything the selection rule allows", and (2) is immediate. Then Hamiltonicity of `T` follows from the property for the two sides of any separating 3-cycle or 4-cycle. The property itself must be proved for all pieces, and by Theorem 3 it is equivalent to the 3-edge-path statement for the closed-up graphs. So an induction along 4-cuts reduces Barnette's conjecture with prescribed 3-edge paths to triangulations with no separating 3-cycle or 4-cycle, and for those a direct argument is still needed. O's state method is such an argument for the weaker `m = 3` statement, and I do not see how to make it produce a prescribed 3-edge path: `COMPUTED` (`code/gadgets.py 11`), a single prescribed facial edge forces a 4-cut pattern in only one case out of six.

For `m >= 5` there is no uniform `Pi`. The data show at least three different realised sets for the one sign word of length 5.

### Verdict

Substantive. The functor is real, the Temperley-Lieb form is the right target, and the viewpoint produces statements that can be right or wrong and were checked. Its value for the exposition is explanatory. It tells the reader why Theorem 2.2 has the shape it has and why Corollaries 7.1 and 7.2 are natural. It does not shorten the proof.

## 2. Trinity and triality

### Definitions

`T` with its vertex 3-colouring is a trinity in Tutte's sense, and O's states are its Tutte matchings (`LIT`: Tutte 1975, Berman 1980, Hine and Kálmán 2018, as checked by the machinery report). There is a second trinity. Let `K` have vertex classes `V` (vertices of `T`), `B`, `W` (black and white face centres), with edges centre to corner and black centre to white centre across each edge of `T`. `K` is a 3-coloured Eulerian triangulation with `6k` faces, one for each edge of `T` with a chosen end. Its three bipartite graphs are

```
K - W = H   (the spoke graph of O),      K - B = H'  (white spokes),      K - V = G.
```

So the Barnette graph and the spoke graph are two of the three graphs of one trinity. The symmetry group of the roles is `S3`, but `K` is special: `B` and `W` have degree 6 and `V` does not, so only the exchange of `B` and `W` (the colour swap) is a symmetry of the class.

### Tutte's bijections

`COMPUTED` (`code/trinity.py tutte 11`, 153 rooted triangulations with colour): for each colour `c`, the map sending a state `s` to the arcs "from `s(t)` to the vertex of the same colour across the opposite edge", over the faces with `s(t)` of colour `c`, is injective, its image consists of arborescences into the root of colour `c`, and the number of states is the determinant of the reduced Laplacian of that digraph. This is the tree trinity theorem, `LIT`.

One can call the three maps natural isomorphisms between four functors (states, and arborescences in three digraphs) on the groupoid of rooted 3-coloured triangulations. With isomorphisms as the only morphisms this says that the bijections commute with relabelling, which is true and empty. I found no non-invertible morphism (deletion, contraction, insertion) for which all four sides are functorial and the bijections natural, apart from insertion into a white face, where everything is a product (Section 4). So here the categorical language is vocabulary.

A fact that deserves a place in the exposition: for every single state, reflecting each vertex across the edge opposite to it in its matched face is acyclic. Acyclicity is free for one state. The difficulty of Proposition 5.1 is acyclicity of `Q_s`, which uses the opposite edges themselves and not the reflections.

### The other roles

Call a perfect matching `M` of a plane bipartite graph `Gamma` (after deleting enough roots to balance the classes) a cotree matching if `Gamma - M` has as few components as the edge count allows. Then:

| pair of classes | graph | cotree matching | cotree lives on |
| --- | --- | --- | --- |
| `B, V` | `H`, roots `t0` and its corners | tree matching of O | `W` |
| `W, V` | `H'` | tree matching for the swapped colours | `B` |
| `B, W` | `G`, no roots | complement of a Hamiltonian cycle | `V` (the two induced trees) |

O's Section 6 is a map from the first row to the third: the cotree of a tree matching, rooted at `y0`, picks a white neighbour for each black face. Proposition 7 of the combinatorics report describes its image.

**Triangle factors** (`PROVED-HERE`, Proposition 5). A Hamiltonian cycle of `G` with one chosen vertex of `T` on each side is the same thing as a set of pairwise disjoint faces of `K` that covers all of `K` except the two chosen vertices and whose `T`-edges form a forest. This is the form of the statement in which the three classes enter alike. Its three projections are a `B-V` matching, a `W-V` matching and the `B-W` matching complementary to the cycle.

So Barnette's conjecture is equivalent to: `K` has an acyclic triangle factor. I do not know a theorem about triangle factors of 3-coloured Eulerian triangulations that applies. The reformulation is exact and I have not seen it in the three papers.

**Is the theorem easier in another role?** No, as far as I can see. The `B, W` role is the conjecture itself. The `W, V` role is the same theorem with colours exchanged. What triality does give is a question the papers do not ask: when is the `B-V` projection of a triangle factor itself a tree matching?

`COMPUTED` (`code/trinity.py factors 11`): of 2048 factors (Hamiltonian cycle and one root on each side) in the triangulations with at most 11 vertices, the black projection has acyclic `Q` in 1839, the white one in 1875, both in 1681, neither in 15.

### Two-root states

A two-root state is a bijection from all black faces onto `V - {v1, v2}` with `s(t)` a corner of `t`. It is a two-root tree matching if `Q_s` is a forest, equivalently `H - s` is a spanning forest with two components. O's tree matchings are the special case `{v1, v2}` in `t0` (extend `s` by sending `t0` to its third corner). The dual of the deleted spokes is then a connected graph with one cycle on the white faces, and it has exactly two orientations, each of which selects one edge per face.

`COMPUTED` (`code/trinity.py tworoot 12`, all 15 triangulations with at most 12 vertices, output `data/tworoot_v12.txt`):

- Every Hamiltonian cycle of `G` is selected by some two-root tree matching (all 15 triangulations, 258 cycles). `CONJECTURE`: this holds always. Test: one Hamiltonian cycle of a Barnette graph that is not reached. Compare with the face-rooted version, where most cycles are not reached (combinatorics report, Proposition 7).
- For the 10 triangulations without separating triangle, every pair `{v1, v2}` has a two-root tree matching. `CONJECTURE` for all triangulations without separating triangle. With separating triangles it is `REFUTED`: `plantri_12_6` has one for only 51 of 66 pairs. Lesson: two roots do not remove the separating-triangle obstruction, they move it.
- A two-root tree matching does not always give a Hamiltonian cycle. Of 5154 two-root tree matchings, 1327 have no Hamiltonian orientation, 1230 have one and 2597 have two. So O Lemma 6.2 fails for general roots. The reason is visible in the disk identity: a cycle of selected edges may now separate `v1` from `v2`, and for such a cycle the count `B = I + l` is off by one. Rooting at a face keeps all roots on one side of every cycle. That is what the face is for.

### Verdict

The trinity `K` and the triangle-factor statement are a real reorganisation: they put `G`, `H` and the selected set `P` in one object and show which symmetry the proof breaks. The functorial packaging is vocabulary only.

## 3. Homology

### The tautological complex

For a state `s` with `k(s)` cycles in `Q_s`, its partners form a cube of dimension `k(s)` on which the sign alternates (combinatorics report, Lemmas 2 and 3). Let `C` be the direct sum over `s` of the cube complexes, each the tensor product of `k(s)` copies of `Z -> Z` with the identity map, graded by `(n + J)/2` and by `omega(s)`. Then `H(C)` is free on the forest pairs, and its graded Euler characteristic is the sign-corrected `Z`. `PROVED-HERE` in one line: a tensor product of acyclic complexes is acyclic, and the cubes of dimension zero are the tree matchings.

This categorifies the cancellation and proves nothing: the homology is nonzero exactly when a tree matching exists, and I know no second description of `C`. In discrete Morse language, O Lemma 5.2 is an acyclic matching on `C` with the forest pairs as critical cells. Same content.

### A bicomplex?

The regrouping by `D` is a second family of cubes. If reversing a `Q_s`-cycle and reversing a `D`-cycle commuted as moves, the two cube differentials would form a bicomplex, and the proof would be a comparison of two spectral sequences. `REFUTED`, `COMPUTED` (`code/homology.py bicomplex 12`): among the 624 pairs of all rooted triangulations with at most 12 vertices, there are 12 for which "a `Q`-move then a `D`-move" and "a `D`-move then a `Q`-move" reach different sets of pairs. Lesson: the two cube structures are not compatible on the nose, which is why every published proof needs a weight and a leading term.

### A homological existence criterion

Tree matchings are the common bases of three matroids (machinery report, Section 6). For this situation there is a topological Hall theorem (`LIT` from memory, not opened: Aharoni and Haxell, J. Graph Theory 2000; Meshulam, Combinatorica 2001): if a complex on a ground set split into `n` parts has, for every set `S` of parts, vanishing reduced homology below dimension `|S| - 1` on the union of those parts, it has a simplex with one vertex in each part.

Take the complex of partial tree matchings: sets of incidences `(t, v)` with distinct faces, distinct vertices, and opposite edges forming a forest after the roots are identified. Parts are the faces of `A`. A full transversal simplex is a tree matching.

`REFUTED`, `COMPUTED` (`code/homology.py hall 9`): the hypothesis fails for all 17 rooted triangulations with at most 9 vertices, already for two faces of the octahedron, where the subcomplex is disconnected. For the octahedron the whole complex has Betti numbers `(1, 0, 0)`. Lesson: the complex is far from highly connected, as expected for an intersection of three matroids, and existence cannot come from connectivity alone.

### Verdict

Vocabulary only. Both ways I could think of to make homology do work fail on the smallest example.

## 4. Operads, species, recursions

### Insertion into a face

Rooted Eulerian triangulations form an operad: the inputs of `(T, t0)` are its faces other than `t0`, and composition glues another rooted triangulation, minus its root face, into an input.

**Proposition 6** (`PROVED-HERE`, `COMPUTED` on 1856 insertions). The numbers of states, of pairs and of tree matchings are multiplicative under insertion into a white face. Insertion into a black face other than `t0` kills all pairs. So these three counts are morphisms from the white-insertion operad to the monoid `(N, x)`, and the sub-operad of rooted triangulations with a tree matching is closed under white insertion.

This is the structure behind the exponential rarity family of the limits report, and behind the "black inner boundary" criterion of T. It is a small statement, and it is the only place where I found an honest functor to a simple target.

### Deletion and contraction

The number of tree matchings is a coefficient of the degree-tracking spanning tree polynomial of `H` (machinery report, Section 4). That polynomial satisfies deletion-contraction, but contraction merges two vertices and adds their degrees, so a single prescribed coefficient does not obey a recursion inside the class. I found no Tutte-Grothendieck invariant behind `tau`. Supporting data from the algebra report: `tau` depends on the root, so it is no evaluation of an unrooted invariant.

### A monotonicity conjecture

Let `v` be a nonroot vertex of degree 4 with neighbours `a, b, c, d` in order, and suppose deleting `v` and identifying `a` with `c` gives a simple triangulation `T/ac` in which `t0` survives.

`CONJECTURE`: `tau(T, t0) >= tau(T/ac, t0)`. `COMPUTED` (`code/recursion.py contract 12`): true in all 948 such contractions up to 12 vertices, and in 36 cases `tau(T/ac) = 0 < tau(T)`. Test: one contraction with more tree matchings below than above.

If an injection realises this, tree matchings lift along the inverse operation (splitting a vertex, which in `G` adds a quadrilateral face). That would give existence by induction for every rooted triangulation that can be reduced to a known case through simple contractions. It would not give Barnette's conjecture by itself: the known difficulty is that contractions leave the class. I did not look for the injection.

### Verdict

Multiplicativity is substantive and small. There is no recursion with nonnegative terms that I could find, only the conjectured inequality.

## 5. Belyi maps and the permutation triple

### Dictionary

A sphere triangulation with 2-coloured faces is the same as a covering of the sphere branched over three points: black faces go to the upper hemisphere, white faces to the lower, and the three vertex colours to the branch points. Its degree is `k`, the ramification at a vertex is half its degree, and the monodromy is a triple of permutations of the `k` black faces, `sigma_c` rotating a face about its corner of colour `c`. Checked (`COMPUTED`, `code/monodromy.py 12`, 15 triangulations): the cycles of `sigma_c` are the vertices of colour `c` with lengths `deg/2`, the product in a suitable order is the identity, and the number of cycles is `k + 2`, which is genus zero.

Every dessin on the sphere arises: `T` is the canonical triangulation of the bipartite map on two of the colours. There is no restriction of the type "all cycles of length 2". The only hypothesis is that `T` is simple.

`G` is the preimage of the theta graph (two vertices in the hemispheres, three edges across the three arcs of the equator). So `G` is a `k`-fold covering graph of the theta graph, with black vertices the points, white vertices identified with the points by one of the three matchings, and the two others given by the permutations. A Hamiltonian cycle is a closed non-backtracking walk of length `2k` in the theta graph whose lift is a single closed curve through the whole fibre. The count from the triple alone agrees with the count from the map (`COMPUTED`, same script).

A state is a transversal: a choice of colour `c(t)` for every black face `t != t0` such that every cycle of every `sigma_c` not through `t0` contains exactly one `t` with `c(t) = c`. A pair is two transversals that differ everywhere. `delta` is `+1` when the second colour is the first plus one. `COMPUTED`: the number of such transversals equals the number of states.

### What it gives

A compact encoding, and one caution. The passport (the three cycle types) does not determine the number of Hamiltonian cycles: `plantri_12_2` and `plantri_12_4` share the passport `(2,2,3,3)` three times and have 24 and 20 Hamiltonian cycles (`COMPUTED`).

I found no group-theoretic content. The monodromy group is generically large and knows the map only through the triple, the disk identity is a statement about disks and has no formulation I could find in terms of the group, and the Hamiltonian-walk statement is of the Lovász type for a Schreier graph, for which no group-theoretic method is known to me. Planarity enters the triple only through the cycle count, and the proof uses planarity through the Jordan curve theorem, many times.

### Verdict

Vocabulary only. Worth one sentence in an introduction, because it says how general the class is: all genus-zero three-point covers whose triangulation is simple.

## Overall

Category theory earns a place in the exposition in one spot, and it is a modest one. The cut-and-glue picture of Section 1 should appear when the paper reaches separating triangles: the boundary of a piece has a finite state space, for a triangle it has three elements, Theorem 2.2 says every piece realises all three, and that is why the induction closes. A remark can add that the same statement for quadrilaterals is the 3-edge-path corollary and that it stops there. This needs no word of category theory beyond "the count is the linear term of a quantity that multiplies under gluing".

The trinity `K` is a good picture for the recovery step and costs one figure. The homological and Galois vocabularies should stay out of the paper.
