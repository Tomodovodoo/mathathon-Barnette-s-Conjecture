# Routes and lessons

## Determinants and double dimers

PROVED-HERE, T2 unreviewed. The zero-one incidence matrix counts all states up to a global sign. The real mixed determinant in PROOF section 2 computes the signed pair sum exactly, including disjointness. Its face coefficient is essential. Each local matrix has rank at most two. This is a useful linear-algebra formulation, not yet an efficient evaluation algorithm.

REFUTED, COMPUTED T4. Setting every face marker to one is wrong. On the hexagonal-prism dual at q=2, the mixed coefficient is 6 and the raw determinant is 0. The raw determinant allows the same black face to supply several transitions and another face none. Cancellation among those extra terms can even destroy the desired answer. The constructive agent independently tested a sixth-root version in its exact_determinant.py; this report uses real local signs and exact integer determinants.

PROVED-HERE. For scalar weighted incidence matrices, det(K1+z K2) enumerates one perfect matching with a choice of weight type on each used edge. Its coefficient of z^j chooses j of that matching's edges for type 2. It does not enumerate two perfect matchings. det(K1)det(K2) does enumerate ordered pairs, but permits shared edges and factors weights independently between matchings. The local rank-one obstruction in PROOF section 6 explains why simply changing those weights does not encode the turn phase at a three-corner black center.

LIT. Kenyon, Conformal invariance of loops in the double-dimer model, arXiv:1105.4158v2, sections 3.2.1 and 3.3, Lemma 1 and Theorem 2, proves the ordinary product formula and its SL2 quaternion-determinant extension. In the SL2 expansion, nontrivial loops get a monodromy trace; doubled edges get the square of their scalar edge weight. Their transport followed by its inverse is identity, so changing the connection does not kill a doubled edge with nonzero scalar weight. This is the precise obstacle to using that theorem directly. I read the local source dump supplied in the machinery agent's folder, including these formulas.

HUNCH, T6. A decorated graph with a local antisymmetric three-leg tensor might give a useful Pfaffian encoding with the no-doubling condition built in. The immediate block Pfaffian identity only restates our determinant coefficient. A real advance would remove coefficient extraction. Test a proposed gadget's complete local signature, including all unwanted doubled-edge states, before testing whole graphs. No such gadget or SL2 connection was established here.

## Trees and trinity

PROVED-HERE, T2 unreviewed. Tree matchings correspond exactly to white-face spanning trees whose edge labels use every t in A and v in X once. The matrix-tree coefficient in PROOF section 5 is their positive weighted count. Ordinary or all-minors matrix-tree formulas impose connectivity or component-root conditions, not both label-transversal constraints. One cannot discard those constraints.

COMPUTED, T4. On the octahedron, H* has 128 spanning trees; retaining only duals of B leaves 8; only 2 are tree matchings. On the hexagonal-prism dual the corresponding counts are 2700, 80, and 2. The full dual is a multigraph, so parallel edges must be retained.

LIT. Hine and Kalman, Clock theorems for triangulated surfaces, arXiv:1808.06091v1, Theorem 4.3 and Lemma 4.4, states that the three directed trinity graphs have the same rooted arborescence count and that restriction of a state to any vertex color gives a bijection with that color's arborescences. The paper uses white matched triangles; swap black and white for our convention. Its arborescences point away from the root.

COMPUTED, T4. Our trinity graph for a vertex color has an arc from the opposite vertex in the adjacent white triangle to the vertex in the black triangle across each edge of the other two colors. The incoming Laplacian cofactor counts out-arborescences. All three cofactors equal the state count on all 18 examples. Root each at its vertex of t0. These graphs have vertices in one vertex-color class of T. They are not the white-face graph H*.

LIT plus PROVED-HERE characterization. Tree matchings are a subset of those trinity arborescences under the bijection. The subset consists of states having a unique disjoint mate, or equivalently giving the prescribed-degree incidence tree. I found no purely one-color local criterion for this subset. The 8-vertex hexagonal-prism dual already has 3 arborescences in each color but only 2 tree matchings.

LIT. Kenyon, Propp and Wilson, Trees and matchings, arXiv:math/9903025v2, section 2, Theorem 1, constructs an overlay with vertex, edge and face nodes, deleting an incident root vertex and face. It gives a weight-preserving tree-to-matching bijection. Applying it to H* encodes all its spanning trees and carries the label constraints along. It does not identify those unconstrained dimers with our B. Trinity gives the exact state count here; KPW alone does not remove the tree-matching restriction.

## Zeros and minimal marks

PROVED-HERE, T2 unreviewed. The positive leading coefficient counts minimum-cycle undirected pairs with one enclosed spoke face marked per cycle, for unit face circulation. It equals a signed moment of tree states, not their signed unweighted count. That unweighted count is zero. Formula and proof are in PROOF section 4.

COMPUTED, T4. The stored 9-vertex nonobstructed gluing has F(q)=(q-1)^2, cmin=2, leading coefficient 1 and four tree states. The 12-vertex cyclic-mate example has ten ordered pairs, eight tree states, and F(q)=-3q^4+3q^5-q^6+q^7. The two non-tree pairs cancel. Its first derivative at 1 is 4, while the unweighted signed tree count is zero.

## Economical weights

PROVED-HERE, T2 unreviewed. Linear incidence weights 1+x a_tv suffice. This yields a polynomial of degree at most n instead of exponentials or large integer powers, and retains exactly the leading positive cycle-circulation coefficient. The matching-side invariant is a signed elementary symmetric moment. This is the cleanest simplification found here.

PROVED-HERE. Separate formal variables for each incidence make forest support literal: nonzero monomials are precisely tree matchings and each coefficient is +1 or -1. Integer face circulations give a one-variable q specialization. More generally prescribe positive real fluxes on bounded spoke faces; the same dual routing gives circulation equal to the sum of enclosed fluxes. Gauge terms alpha_t+beta_v do not affect cycle differences. Vertex-only or black-face-only weights are pure gauge and fail.

HUNCH. It may suffice to put flux on a small face set meeting the interior of every feasible D cycle. Test minimum hitting sets for the interiors on enumerated instances. A single marked face fails as a general strategy if feasible cycles have disjoint interiors. I did not compute optimal flux support.

## Probability

PROVED-HERE consequence. After choosing a small nonzero x with Z(x) nonzero, the normalized complex measure proportional to i^J exp(x omega(s)) gives total mass one to the forest event, because its complement has total mass zero. Individual nonforest configurations can still have nonzero weights. This is not a positive probability measure.

PROVED-HERE consequence. Under a uniform state of B, the tree probability is N_tree/abs(det K). Under a uniform spanning tree of the restricted white graph it is N_tree/tau(W_B), and under the full white graph it is N_tree/tau(H*). These are positive when a pair exists, using the cancellation proof. There is no new transparent proof of that positivity from the denominators alone: the obstructed 9-vertex example has positive denominators and zero numerator.

PROVED-HERE. The constant-term norm in PROOF section 4 is positive exactly when a tree matching exists. It defines a positive torus density |F|^2 after normalization, but constructing this density presupposes nonvanishing. Uniform trinity arborescences are uniform states through the bijection; the same subset problem remains.

## Scope and provenance

Read all three supplied text dumps and inspected relevant rendered PDF pages: original page 7, constructive page 11, Li page 8. The original disk and circulation formulas, constructive sign count, and Li turn identity agree with the rendered pages. Read local primary-source extracts for Kenyon, KPW, and Hine-Kalman. No external bibliographic inference is treated as checked.

All code imports the reference graph model read-only, with bytecode disabled. The 12-vertex graph came from the constructive agent's stored counterexample and was re-enumerated here. No independent referee reviewed this report. Computations remain T4. The tests are 18 rooted examples, not all triangulations of orders 6 through 14.
