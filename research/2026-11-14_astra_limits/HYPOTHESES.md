# Hypotheses and failure points

Every PROVED-HERE result below is T2, unreviewed. Every COMPUTED result is T4 evidence, under review, even where the range is exhaustive. No independent referee ran this campaign. LIT names an exact source; the supplied 2026 manuscripts are preprints, not certified T1 results. REFUTED refers to the stated proposed strengthening, not to Barnette's theorem.

## Bipartiteness

PROVED-HERE. The first missing object is the proper black/white face coloring of T, before a state is defined. Such a coloring is exactly a bipartition of the primal graph. Around an odd-degree dual vertex the colors would have to alternate an odd number of times. K4 is the smallest cubic simple 3-connected example: its dual is K4 and all four degrees are odd. It is Hamiltonian, so failure of the machinery must be distinguished from failure of the conclusion.

COMPUTED. `code/more.py` solves maximum cut using SciPy MILP, with solver gap zero. Of 6, 57 and 69 edges, respectively, K4, BBL38 and Tutte46 have maximum cuts of 4, 50 and 60. Thus even an optimal relaxed coloring leaves 2, 7 and 9 monochromatic adjacencies. `data/nonbipartite.json` stores the colorings, offending edges and odd dual vertices. `examples/K4.json`, `BBL38.json`, and `Tutte46.json` store explicit edges. BBL38 is House of Graphs graph 954, downloaded from https://houseofgraphs.org/api/graphs/954. Tutte46 is NetworkX's named graph.

PROVED-HERE. At a black-black adjacency an edge has two black owners; at a white-white adjacency it has none. Therefore Q no longer selects distinct edges by face ownership, delta has no unique black side, and the signed side-count cancellation fails. Optimizing the coloring cannot repair those definitions. Lesson: odd degrees are a local obstruction to the actual algebra, not merely evidence that a Hamiltonian cycle might be absent.

LIT. The original paper cites Tutte, "On Hamiltonian circuits", JLMS s1-21, 1946, 98-101. The 38-vertex minimality source is Holton and McKay, JCTB 45, 1988, 305-319, DOI 10.1016/0095-8956(88)90075-5. Its full text was not opened here; global 38-vertex minimality is not independently established in this report. We did not rerun Hamiltonicity enumeration on the two large named examples.

## Cubicity

PROVED-HERE. Drop cubicity and even the conclusion fails. Take the radial graph of the triangular bipyramid. The five original vertices form one bipartition class and its six triangular faces form the other. Unequal class sizes exclude a Hamiltonian cycle. Explicit adjacency is in `examples/noncubic11.json`; `code/certificates.py` checks planarity, bipartiteness and 3-connectivity. This is an 11-vertex witness, without a minimality claim here.

PROVED-HERE. Cubicity gives triangular dual faces and exactly one edge opposite a chosen corner. In a larger face there is no such unique opposite edge. Selecting one dual edge per face also leaves degree greater than two at the corresponding primal vertex. Lesson: both the initial state construction and the final degree-two recovery use cubicity.

## 3-connectivity and simplicity

PROVED-HERE. An explicit 26-vertex example consists of terminals 0,1 and three copies of cube-minus-edge. For each copy join one deleted-edge endpoint to 0 and the other to 1. `examples/theta_cube_26.json` gives all 39 edges, embedded faces and dual multiedges. Every vertex has degree three. Each cube-minus-edge has its terminals on one face; placing three such pieces in the three branches of a planar theta drawing proves planarity. Choosing opposite bipartition colors for 0,1 proves bipartiteness. Deleting any one vertex leaves the graph connected: a cube with an edge and a vertex removed stays connected, and the other branches connect the terminals. Deleting 0 and 1 leaves three components. A Hamiltonian cycle minus two vertices has at most two components, so this graph is non-Hamiltonian and exactly 2-connected.

LIT. Asano, Saito, Exoo and Harary, "The smallest 2-connected cubic bipartite planar nonhamiltonian graph", Discrete Mathematics 38, 1982, 1-6, DOI 10.1016/0012-365X(82)90162-5, states that the minimum is 26 and unique. The publisher abstract was returned in search, but opening the article returned HTTP 403. This is an abstract-level literature attribution, not a reproduced minimality proof.

COMPUTED. `code/special.py` preserves parallel dual edges, unlike the reference `dual_graph`, which uses a simple Graph. It enumerates states directly from embedded primal vertex/dual-face incidences. At every one of the 26 roots there are eight states and zero disjoint pairs. The proof stops at Proposition 3.1, before weighted cancellation or forest recovery. The exact parallel classes are in `data/non3connected.json`. At root 0, S={6,7,8,9,10,11,12,13,14} has capacity deficit three. All eight incidence complements are disconnected and have cycle rank three. `code/multimap.py` and `data/non3connected_cut.json` record this additional check.

PROVED-HERE. The disk identity itself survives for a simple directed cycle bounding a disk in this loopless triangular multimap, provided states are bijective, face corners are distinct and each selected edge keeps its incidence identity. The proof still has B+W=2I+h-2, 3(B-W)=2l-h and B=I+l. These are incidence counts and Euler's disk formula, not simplicity arguments. Thus blaming Lemma 4.1 for this example would be wrong. The density proof needs simplicity: a two-sided region has d=2, and the bound |balance| <= d-4 is unavailable. There is no pair on which to run the later steps. We did not implement arbitrary multimap recovery.

PROVED-HERE. In the main theorem, finite cubic 3-vertex-connected multigraphs on at least four vertices cannot have loops or parallel edges: their endpoint would have at most two distinct neighbors, whose removal separates it. Simplicity is therefore redundant if 3-connectivity is understood on the underlying adjacency graph. It is essential in the standalone triangulation formulation and its density proof.

## Planarity and surface topology

PROVED-HERE. For a properly face-bicolored cellular triangulation of a closed orientable genus-g surface, write k for either face-color count. Then E=3k and V=k+2-2g. Removing one black face and its three roots gives |A|=k-1 and |X|=k-1-2g. Therefore the original states do not exist when g>0. On the projective plane the mismatch is one. An abstract even-degree triangulation on a non-spherical surface need not have a global face bicoloring; in our example the bicoloring is explicitly supplied.

COMPUTED. `examples/torus_3x3.json` is the periodic triangular grid on vertices (x,y) modulo 3, encoded by 3x+y. Black faces are [(x,y),(x+1,y),(x+1,y+1)]; white faces are [(x,y),(x+1,y+1),(x,y+1)]. It has nine vertices, 27 edges and 18 triangular faces, all degrees six. The attached face lists specify the torus embedding, not a planar embedding chosen by NetworkX. Exhaustive partitions find no two induced trees; its cubic bipartite dual nevertheless has 36 Hamiltonian cycles. Thus it refutes the two-tree target, not toroidal Hamiltonicity. No smallest-torus claim is made.

PROVED-HERE. The two-tree target is impossible on any face-bicolored torus triangulation. If both classes induce trees, each triangle has exactly one same-class edge. Counting triangle incidences gives k such edges. Two spanning induced trees would have V-2=k-2 edges, a contradiction.

COMPUTED. A natural root-free relaxation on the torus does have states and pairs: assign each black face its first corner for r and its second corner for s. Both are permutations of the nine vertices and disagree everywhere. `data/torus_states.json` records the pair and Q cycles. Q has nine edges and nine vertices, so cannot be a forest.

PROVED-HERE. The disk count remains valid for contractible cycles bounding root-free disks when a valid state is available. Noncontractible cycles have no such disk. A complementary dual of a spanning tree on genus g has cycle rank 2g, not zero. One cannot prescribe positive circulation to every face of a closed oriented surface, since summing all oriented face boundaries gives zero.

PROVED-HERE. A topology-independent exact recovery target is an edge set P with exactly one edge in each triangle such that the complementary dual is connected. That dual is then a Hamiltonian cycle. The planar forest criterion is a sufficient way to force connectedness, unavailable at the torus edge count. Topologically, P is a spine of the surface cut along the dual cycle: each triangle retracts onto its selected edge, compatibly across the uncut sides. A nonseparating torus cycle leaves an annulus, hence P is connected and unicyclic. A separating torus cycle leaves a disk and a punctured torus, hence P has two components of cycle ranks zero and two. These are necessary descriptions, not a new existence theorem. The complementary-dual connectedness criterion avoids mistaking a rank count for a sufficient condition.

Lesson: the first obstruction is cardinality, not merely a later invocation of Euler's formula. Any surface generalization needs a different state definition and a different recovery target.

## Separating triangles

COMPUTED. `code/campaign.py 14` tested all 55 plantri Eulerian triangulations through 14 vertices, all 1,206 outer faces, and three prescriptions per face. Pair existence agrees with absence of a black-inner separator at every root. Of the rooted cases, 538 have separators and 326 have no tree matching. All 3,618 recursive recovery certificates pass independent primal Hamiltonian-cycle membership checks.

COMPUTED. The first separating example is `examples/t9_0.json`. Its separator is {0,3,6}. With outer face 0 it has white inner boundary, four states, four ordered pairs and four tree matchings. With outer face 2 it has black inner boundary, four states and no pairs. Faces 0 and 2 have the same color, so this is genuine root dependence without exchanging colors. These are smallest in the enumerated class.

PROVED-HERE. Nine is also the theoretical lower bound. Each capped side is a simple Eulerian sphere triangulation with at least six vertices: minimum degree four and 3V-6 >= 2V imply V>=6. Gluing two such pieces identifies three vertices, giving at least nine.

PROVED-HERE. The gluing step needs agreement on the same-label edge. For either label, the trees on the two pieces intersect in exactly one vertex or one edge; their union is connected and acyclic. No edge joins strict interiors of different pieces, so inducedness survives. Arbitrarily chosen partitions need not agree. Prescribing the cap edge in the second piece supplies exactly the missing boundary agreement. Lesson: the prescription is part of the induction invariant, not optional decoration.

## The disk identity and bijectivity

COMPUTED. `examples/nonbijective_disk.json` is a nine-vertex witness, smallest in the tested simple Eulerian triangulation range. The roots are {0,4,5}, outer face 2. Bounded black face indices A=[0,4,7,9,10,13] choose [1,3,2,8,6,8]. Vertex 8 is used twice and 7 is unused. The edges 1->6, 6->3, 3->2, 2->1 come from distinct black faces 0,10,4,7. They form a directed 4-cycle with delta-sum zero. All selected tails are nonroots and only bijectivity was relaxed. The disk has B=W=2, I=1, l=2 and h=4, so B-I-l=-1.

PROVED-HERE. Retaining the two topological counts but writing d=B-I-l gives 2l-h=-3-3d. To derive this, substitute B=I+l+d and W=I+h-2-l-d into 3(B-W)=2l-h. The state condition sets d=0; the witness has d=-1 and hence zero boundary sum. The exact missing equality is B=I+l. Lesson: distinct face choices alone are insufficient; every interior vertex must also be covered exactly once.

PROVED-HERE. Lemma 5.2 also needs the selected Q-cycle to depend only on s. Its reversal changes r while fixing s and its weight. A choice depending on r need not select the same cycle on the return step. We did not search a smallest counterexample to an arbitrary r-dependent selection rule; such a rule must first be specified.

## Positive circulation and nonvanishing

PROVED-HERE. Set every spoke weight to zero on the cube. There are exactly two pairs, obtained by reversing its sole D-cycle. Their J values are +1 and -1, so Z(x)=i+(-i)=0 for every x. `data/zero_weights.json` checks the signs. This is the smallest simple Eulerian sphere triangulation. The cancellation lemma still works; the nonvanishing argument fails because the two cycle orientations have equal weight.

PROVED-HERE. The requirement is positive cycle circulation, not positive individual spoke weights. Even setting every spoke weight to the same positive constant makes every state have the same total weight and produces the same cancellation. Conversely, reversing every circulation changes the common leading sign but need not make Z zero. Strict positivity is a convenient sufficient coherent sign choice. The exact nonvanishing requirement is that the signed sum of products of the minimal-cycle circulation gaps does not vanish. We did not find a minimal example with nonzero gaps of mixed signs cancelling across different groups.

## Proposition 5.1, uniqueness and rarity

PROVED-HERE, conditional on the disk identity and cancellation proofs in the supplied manuscripts. Exactly one tree matching is impossible. Each tree matching has a unique mate, obtained by directing Q towards its roots. Group all pairs by their unoriented D-cycles and set all weights to zero. Each group has total sign zero. Cancel nonforest second states by Q-cycle reversal. The remaining signed sum, one term per tree matching, is zero. Thus a nonempty tree set has equally many positive and negative members, at least two. The cube realizes two. This restates and explains constructive Theorem 5.2; the proposed uniqueness experiment is REFUTED before a search is needed.

PROVED-HERE. There is an exponential rarity family. Insert q copies of the hexagonal-prism dual successively into white faces, retaining a black outer face in the first piece. Each new piece has its black cap removed, with three shared boundary roots. It contributes exactly as many bounded black faces as new interior vertices. Old faces cannot match new vertices, so all new vertices must be matched by those new faces, leaving none of those faces available to match old vertices. States therefore factor into states of the capped pieces. Disjoint pairs factor for the same reason.

Each rooted prism dual has three states and two disjoint ordered pairs, both tree pairs; the complete local enumeration is in `examples/rarity_1.json` and can also be verified by listing its three incidence permutations. Gluing local tree matchings adds a forest with three components, one attached at each boundary vertex, to the old incidence tree. It remains a tree. Conversely every global tree matching has a disjoint mate, hence restricts to a disjoint pair in every piece. Therefore the global counts are exactly 3^q states and 2^q tree matchings. V(T)=5q+3 and the primal has 10q+2 vertices. The success fraction is (2/3)^q.

COMPUTED. `code/rarity.py` checked q=1,...,6: states 3,9,27,81,243,729 and trees 2,4,8,16,32,64. The local count used in the proof has not received an independent referee check. The initial wrong-color insertion experiment is retained in `data/rarity_black_obstructed.json`. Lesson: zero trees in an obstructed root is not evidence of rarity among feasible states.

## Forest versus rooted forest

COMPUTED. Already on the hexagonal-prism dual, all three states have acyclic Q, but only two are tree matchings. For its canonical root {0,1,2}, the bad state's components are {0,3,6}, {1,2,7}, {4,5}. One contains two roots and another none. Its state is [5,4,3,6,7] in the stored face order.

PROVED-HERE. The mate supplies outdegree one at each nonroot and zero at each root. A tree component on v vertices with a roots has v-a outgoing edges, equal to v-1, forcing a=1. Without the mate this count is unavailable. Lesson: do not abbreviate a tree matching as merely a forest state unless a partner has already been supplied.

## Root choice, prescription and the image of recovery

COMPUTED. Counts are not root invariant. In `t12_2`, with a fixed black class, outer face 0 gives 9 states, 10 pairs and 8 tree matchings; each other black root gives 9 states, 2 pairs and 2 tree matchings. `data/roots.json` tabulates every root. In all 9,720 recovery images over tested roots and edge prescriptions, multiplicity is one.

PROVED-HERE. For fixed t0,e0, the direct recovery map is injective. From its Hamiltonian cycle recover P as the primal-dual complement. Remove e0. The resulting forest has three components, each with one root. Direct each toward its root. In every bounded black face its selected edge has tail s(t), recovering the state uniquely. No different state can give the same cycle.

PROVED-HERE. More exactly, given any Hamiltonian cycle avoiding e0*, its complementary dual P consists of two induced trees by the sphere Jordan argument. Removing e0 splits the tree containing its endpoints; the third root is in the other tree. Direct the resulting three trees toward their roots. Their tails define a state s, since there is exactly one selected edge per bounded black face and one outgoing edge per nonroot. The cycle is in the image precisely when H-s is a tree. Necessity is the constructor's input condition. For sufficiency, each selected side specifies one endpoint of the corresponding deleted spoke's white-tree edge. Each white face except y0 receives one such edge and y0 receives none; in a tree this is the unique orientation away from y0. Recovery therefore selects exactly P.

COMPUTED. Surjectivity fails first at the hexagonal prism, `examples/prism_recovery.json`. For the stored t0,e0 there are four avoiding cycles, but only two tree matchings and two recovered cycles. The file contains all four cycles and both preimages. This is smallest in the exhaustive range. Thus recovery is a bijection onto the subset characterized above, not a k-to-one parametrization of all avoiding cycles. At black-obstructed roots the direct image is empty, while recursive gluing still works.

Lesson: distinguish every root being solvable recursively from every root admitting a direct pair, and distinguish constructing an avoiding cycle from enumerating all of them.
