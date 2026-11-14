# Labyrinth status

Generated 2026-11-14T11:05:50Z by `labyrinth/lab.py build`. Do not edit by hand.

## The frontier

| size | admissible | realized | impossible | conditional | conj. impossible | unknown | resolved | bounds |
|---|---|---|---|---|---|---|---|---|
| |V(T)| = 6 | 6 | 1 | 5 | 0 | 0 | 0 | 100.0% | upper 5, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 2 |
| |V(T)| = 8 | 16 | 1 | 15 | 0 | 0 | 0 | 100.0% | upper 15, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 2 |
| |V(T)| = 9 | 28 | 2 | 26 | 0 | 0 | 0 | 100.0% | upper 27, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 4 |
| |V(T)| = 10 | 47 | 1 | 46 | 0 | 0 | 0 | 100.0% | upper 46, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 2 |
| |V(T)| = 11 | 82 | 2 | 80 | 0 | 0 | 0 | 100.0% | upper 81, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 4 |
| |V(T)| = 12 | 141 | 3 | 138 | 0 | 0 | 0 | 100.0% | upper 140, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 8 |
| |V(T)| = 13 | 244 | 4 | 240 | 0 | 0 | 0 | 100.0% | upper 243, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 8 |
| |V(T)| = 14 | 421 | 5 | 416 | 0 | 0 | 0 | 100.0% | upper 420, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 10 |
| |V(T)| = 15 | 730 | 5 | 725 | 0 | 0 | 0 | 100.0% | upper 729, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 16 |
| |V(T)| = 16 | 1263 | 8 | 1255 | 0 | 0 | 0 | 100.0% | upper 1262, upper_kind 3^(n/2) (trees paper, Lemma 6.1 with Hadamard), max_seen 16 |
| |V(T)| = 17 | 2188 | 1 | 201 | 0 | 0 | 1986 | 9.2% | upper 2187, upper_kind 3^(n/2) |
| |V(T)| = 18 | 3788 | 2 | 201 | 0 | 0 | 3585 | 5.4% | upper 3787, upper_kind 3^(n/2) |
| |V(T)| = 23 | 59050 | 2 | 201 | 0 | 0 | 58847 | 0.3% | upper 59049, upper_kind 3^(n/2) |
| |V(T)| = 28 | 920483 | 2 | 201 | 0 | 0 | 920280 | 0.0% | upper 920482, upper_kind 3^(n/2) |
| |V(T)| = 33 | 14348908 | 2 | 201 | 0 | 0 | 14348705 | 0.0% | upper 14348907, upper_kind 3^(n/2) |

## Conjectures (15)

- **nodal domains of eigenvectors** [`k.TG.h2`, open] Sign patterns of Laplacian eigenvectors of T almost never give two induced trees (predicted below 5 per cent).
- **roots not on a common face** [`k.A.2`, open] For every simple 2-coloured triangulation some triple of roots of three colours, not necessarily the corners of a face, admits two disjoint states.
- **Gauss-Bonnet form for any cycle** [`k.B.5`, open] For a state s and a simple cycle C avoiding the roots, B - W = 2m - h + 2, with m the boundary vertices whose matched face lies inside. The topology agent reports the orientation-free form W = B + 1 as proved (B.6); the status of this exact formula is in topo/ROUTES.md.
- **a test function with one sign on all covers** [`k.N.9`, open] There is a test function of s for which every cycle cover contributes with the same sign, so that no minimum over the number of cycles is taken.
- **at least 2^cmin tree matchings** [`k.D.3`, open] Every rooted triangulation with a pair has at least 2^cmin tree matchings. True for all 5088 cases up to 16 vertices; equality in 4609.
- **a canonical forest pair** [`k.D.6`, open] Under a bijection from states to trinity arborescences, tree matchings have a tree description that singles one out.
- **order-theoretic position in the state lattice** [`k.U.5h`, open] Outcome (topo): the tree matchings are neither an interval nor an antichain of the clock lattice, and the top and bottom states are often tree matchings. No order-theoretic pattern was found.
- **describe partnered Hamiltonian cycles in G alone** [`k.U.6h`, open] There is a description, without states, of the Hamiltonian cycles of G avoiding e0* whose state has a partner.
- **remove a leaf of the white tree** [`k.F.4`, open] Removing a leaf of the white tree with the black face whose spoke it crosses leaves a rooted triangulation with a tree matching, and the cycle of the larger graph is a local detour.
- **a cut-free root** [`k.G.3`, open] Count how often some root (black face on the black side of all separating triangles, or the same with colours swapped) exists.
- **ordered pairs of edges (global H+-)** [`k.G2.5`, open] Some Hamiltonian cycle contains x and avoids y for any two edges. Not implied by the theorem.
- **non-increasing exchange path to a tree pair** [`k.N.11`, open] From every pair there is a path of exchanges along which the number of Q-cycles never increases and reaches 0. A sign-free form of T Theorem 5.2.
- **Li's marked objects are the e_m coefficient** [`k.N.12`, open] Li's objects with cmin distinct marks are the elementary symmetric reading of the linear-weight coefficient.
- **extremes of Felsner's lattice of pairs** [`k.D.7`, open] The face-flip minimum or the face-flip maximum of the lattice of pairs always carries a tree pair. Each extreme alone fails (at 40 and at 80 vertices); they never failed together in 180 random instances.
- **local search from a point-rainbow tree** [`k.U.7h`, open] Same-colour exchanges from a point-rainbow tree, never increasing the black excess, reach a tree matching. A proof would be a cancellation-free local-search proof of the key lemma.

## Open doors (questions) (12)

- **Is there a polynomial-time construction of the Hamiltonian cycle?** [`q.poly-time`, open] The proofs give exponential search (3^(N/4), or 2^O(n log n) for the marked walk). Sampling states is polynomial; tree matchings can be exponentially rare.
- **Is there an existence proof with no signed count?** [`q.structural`, open] Every reformulation of the target is exact and none has an existence argument; every structural shortcut tested fails on long D-cycles.
- **Is there a canonical forest pair?** [`q.canonical`, open] Seven extremal rules are refuted. Only 'lattice min or max' survives, on random samples.
- **How many tree matchings must there be?** [`q.tm-lower`, open] Proved here: at least 2 cmin. Conjectured: at least 2^cmin (no exception among 5088 cases; equality in 4609).
- **Is there a determinant or Pfaffian for Z without coefficient extraction?** [`q.det`, open] Z is the squarefree coefficient of one determinant (2^n evaluations). Raw determinants, doubled edges and scalar factorisations are refuted.
- **Which Hamiltonian cycles come from tree matchings?** [`q.which-hc`, open] Exactly those avoiding e0* whose state has a partner; equivalently partitions with acyclic white parent map. No description in G alone.
- **Is there a second proof of the disk identity?** [`q.disk`, open] All papers use one double count. Parity suffices three times and the value 3 once (p.C.5). The topology agent derives the identity from the theorem of turning tangents (p.B.6); nobody has refereed that.
- **Can a different rooting remove the separating-triangle induction?** [`q.roots`, open] With t0 a face the obstruction is exact. Roots of three colours not on a face are untested.
- **Do Li's higher-mark involutions match the polynomial coefficient?** [`q.li-b`, open] Li's Appendix B leaves three verifications to the reader; li.py was not refereed.
- **What is the right statement on other surfaces?** [`q.surface`, open] States need |A| = |X|, which fails by 2g. The topology-free target is one edge per triangle with connected complementary dual.
- **What is the status of formal verification?** [`q.formal`, open] The Lean proof builds locally with standard axioms and follows a different route in four places. Corollary 7.2 and Theorem 2.2 are not formalised.
- **Has a human checked any of the proofs written here?** [`q.human`, open] No. Two folders are AI-refereed (combinatorics, determinants), two are under review, the rest unreviewed.

## Hunches (speculation, not claims) (25)

- **induced-forest completion** [`h.TG.h1`, live] Start from a large induced forest and exchange vertices until both sides are trees.
- **induction over local expansions** [`h.A.1`, live] Grow rooted Eulerian triangulations by vertex splits and show a pair survives each split.
- **matroid union** [`h.A.3`, live] Two disjoint matchings as a basis of a union of transversal matroids.
- **integer lift of Kasteleyn's sign lemma** [`h.B.1`, live] The faces of the spoke graph are hexagons, 6 = 2 mod 4, which is Kasteleyn's condition. The common sign of all states uses only the parity part of the disk identity.
- **discrete Morse theory** [`h.B.2`, live] Read the state as a pairing of black faces with vertices in the disk and compute the degree from the unpaired cells.
- **peel the disk** [`h.B.3`, live] Remove a boundary vertex with its matched black face and show 2l - h does not change.
- **Grinberg count made rigid by a matching** [`h.B.4`, live] 3(B - W) = 2l - h is a Grinberg balance in the dual; the bijection adds B = I + l.
- **height-function form of J** [`h.C.4`, live] The Q_s-reversal can change the cycle structure of D completely and J still moves by exactly 2.
- **mixed determinant with positive curvature** [`h.N.1`, live] Z = [prod z_t] det(sum z_t M_t) is n! times a mixed discriminant of rank-two blocks. Prove it nonzero from structural hypotheses.
- **2-adic evaluation at z = -1** [`h.N.2`, live] Choose weights with every L+ - L- odd and evaluate T's polynomial at -1.
- **cycle popping, random walk** [`h.N.3`, live] The two moves pop cycles of Q_s and of D, as in Wilson's algorithm. Show the walk hits a tree pair fast.
- **Pfaffian gadget for the turn tensor** [`h.N.4`, live] Replace each black face by a planar matchgate with signature q^delta on distinct ordered corners and zero on equal corners.
- **height potential on pairs** [`h.N.5`, live] A combination of the two state heights that decreases along some exchange move at every non-tree pair.
- **curved double-dimer connection, Lee-Yang** [`h.N.6`, live] Realise the loop factor -i e^{xL+} + i e^{xL-} as the trace of a non-flat connection.
- **LGV after cutting along seams** [`h.N.7`, live] Cut the pair diagram into non-intersecting paths and use a Lindstrom-Gessel-Viennot determinant.
- **abstract valuation theorem** [`h.N.8`, live] Axiomatise: a finite signed cycle system, two involutions, a positive circulation.
- **flux on a small set of faces** [`h.N.10`, live] Put positive flux only on a set of faces that meets the interior of every feasible D-cycle.
- **support of the tree-degree polynomial** [`h.U.1h`, live] Show the target degree vector d* lies in the support of det L_H(y), from plane incidence inequalities.
- **spanning-tree parity / matroid parity** [`h.U.2h`, live] 'Each black centre keeps exactly two of its three spokes' looks like the spanning tree parity problem that Feder and Subi solve in polynomial time for 2- and 3-sided faces.
- **Bernardi process, Schnyder woods, blossom trees** [`h.U.4h`, live] A canonical tree or orientation of the map might produce a tree matching directly.
- **Temperley / Kenyon-Propp-Wilson** [`h.E.2`, live] Read the step as the tree-to-matching bijection of KPW.
- **a potential along the selected out-edges** [`h.F.5`, live] Follow selected out-edges from a vertex to a root; a quantity that decreases along the walk proves connectivity.
- **boundary transfer algebra** [`h.G.4`, live] Give a separating triangle a finite boundary state space and write gluing as a contraction.
- **Hall-free shelling construction** [`h.A.5`, live] Build a pair by a canonical ordering from t0 inward, as for Schnyder woods.
- **finding a tree matching is in PPAD** [`h.D.8`, live] Each phase of the marked walk follows a path in a graph of degree at most 2 with alternating signs.

## Dead ends (refuted) (35)

- **drop bipartite** [`x.S0.x1`, refuted] Without bipartiteness there is no proper face colouring of T, so states are not defined.
- **drop 3-connectivity** [`x.S0.x2`, refuted] A 2-connected cubic bipartite planar graph can be non-Hamiltonian. Its dual has parallel edges.
- **other surfaces** [`x.S0.x3`, refuted] On an orientable surface of genus g, |A| - |X| = 2g, so states with three roots do not exist for g > 0, and the two-tree target is impossible on the torus by an edge count.
- **trees from colour classes** [`x.TG.x1`, refuted] Build a permeating subtree containing all or none of a colour class of the vertex 3-colouring.
- **Grinberg obstruction** [`x.TG.x2`, refuted] Use Grinberg's formula with a modulus to decide Hamiltonicity.
- **every avoiding cycle comes from a tree matching** [`x.A.x1`, refuted] If every Hamiltonian cycle avoiding e0* came from a tree matching, known Hamiltonicity results would give pairs with no flow argument.
- **drop bijectivity** [`x.B.x1`, refuted] Let each black face choose a corner with no injectivity requirement.
- **sign as a product of two dimer weights** [`x.C.x1`, refuted] Write the local phase as alpha(r(t)) beta(s(t)) and get Z as a product of two incidence determinants.
- **choose the cycle using r** [`x.K.x1`, refuted] Let the reversed cycle depend on the partner.
- **zero, vertex-only or face-only weights** [`x.N.x1`, refuted] Use weights alpha_t + beta_v, or none.
- **parity or mod p count without weights** [`x.N.x2`, refuted] Show the number of tree matchings is odd, or nonzero mod p.
- **tree pair among the fewest-cycle pairs** [`x.N.x3`, refuted] Among the pairs with the fewest D-cycles one has Q_s a forest; or every cycle cover D has a forest orientation.
- **highest or lowest partnered state** [`x.N.x4`, refuted] The top (bottom) partnered state of the lattice is a tree matching.
- **minimal cover, all cycles one way** [`x.N.x5`, refuted] Take D with cmin cycles and orient all of them counterclockwise (or clockwise).
- **largest rank difference** [`x.N.x6`, refuted] The pair maximising omega(s) - omega(r) is a forest pair.
- **one cycle always suffices** [`x.N.x7`, refuted] cmin = 1, so a first-order argument is enough.
- **cubes of tree matchings; sign = parity of rank** [`x.N.x8`, refuted] Tree matchings split into cubes of dimension cmin; or eps(s) = (-1)^omega(s) up to a constant.
- **ordinary determinant, all face variables 1** [`x.N.x9`, refuted] Evaluate det(sum_t M_t) with no coefficient extraction.
- **allow doubled edges (standard double dimers)** [`x.N.x10`, refuted] Add a diagonal so that r and s may share edges, as in Kenyon's double-dimer determinant.
- **positive semidefinite blocks** [`x.N.x11`, refuted] Find a gauge in which the local matrices M_t are positive semidefinite, then use mixed-discriminant positivity.
- **Combinatorial Nullstellensatz** [`x.N.x12`, refuted] Get a nonzero evaluation of F from the coefficient form of Alon's theorem.
- **real stability of the tree-state polynomial** [`x.N.x13`, refuted] The unsigned generating polynomial of tree matchings is real stable, like spanning-tree polynomials.
- **matching matroid meets graphic matroid** [`x.U.x1`, refuted] Treat the two endpoint constraints as one matroid and use Edmonds' two-matroid intersection.
- **unconstrained white spanning trees** [`x.U.x2`, refuted] Every spanning tree of the white-face graph, or of its restriction to duals of B, gives a tree matching.
- **trinity arborescences = tree matchings** [`x.U.x3`, refuted] The Hine-Kalman bijection carries all states to arborescences; perhaps every arborescence is a tree matching.
- **Yutsis partition of G** [`x.U.x4`, refuted] Identify the two induced trees with a Yutsis decomposition of the cubic graph.
- **a forest state is enough** [`x.R.x1`, refuted] Call s good as soon as Q_s is acyclic, with no partner assumed.
- **prescribe whatever each cut needs** [`x.G.x1`, refuted] Strengthen the induction hypothesis to an arbitrary set of prescribed edges.
- **LP relaxation of the three constraints is integral** [`x.U.x5`, refuted] Perfect matchings of B intersected with complements of spanning trees of H form an integral polytope.
- **induction by degree-4 expansion** [`x.U.x6`, refuted] Lift a tree matching through the expansion of a degree-4 vertex.
- **positivity of the norm or of the Laplacian terms** [`x.U.x7`, refuted] CT F(w)F(1/w) and the constrained Laplacian coefficient are sums of nonnegative terms, so they are positive.
- **tree count as an unrooted invariant** [`x.U.x8`, refuted] The number of tree matchings equals a fixed evaluation of a Tutte, Penrose, Tait or flow invariant of G.
- **single-swap descent on the number of Q-cycles** [`x.N.x14`, refuted] From every pair with a cycle in Q_s some single exchange lowers the number of cycles.
- **a global sign gauge on incidences** [`x.N.x15`, refuted] Flip signs of incidence variables so that all tree matchings get the same coefficient sign.
- **the partner of a tree matching is a tree matching** [`x.D.x1`, refuted] Swapping r and s would then be a free involution on tree matchings and explain why their number is even.

## Under review (7)

- **tree matchings can be exponentially rare** [`p.D.5`]
- **tree matchings = partnered Hamiltonian cycles** [`p.U.5`]
- **recovery is injective, with known image** [`p.F.3`]
- **the gluing needs the same-label edge** [`p.G.2`]
- **one exact Euler identity, both directions** [`p.A.GT`]
- **pairs are alpha-orientations (Felsner lattice)** [`p.A.6`]
- **sharp primal hypothesis; gluing at black-inner cuts** [`p.G.5`]

## Recent events (50 total)

- 2026-11-14T10:33 · proposed · Conjecture: at least 2^cmin tree matchings (true for all 5088 cases up to 16 vertices)
- 2026-11-14T10:33 · computed · Brute force over 140358 states: tree matching iff exactly one partner
- 2026-11-14T10:36 · refuted · Hypotheses dropped one at a time: bipartite, 3-connected, sphere, bijective state, positive circulation, partner (limits)
- 2026-11-14T10:36 · proved · Rarity family: 3^q states and 2^q tree matchings; recovery is injective with a known image (limits, unreviewed)
- 2026-11-14T10:38 · proved · Dictionary between the three papers; 14 shared core nodes; J is an integer by the 3-colouring alone (dependency-graph, unreviewed)
- 2026-11-14T10:38 · question · Doors opened by the skeleton: roots off a face, leaf removal, cut-free root, second proofs of the disk identity
- 2026-11-14T10:39 · proposed · Topology route predictions P1 to P10 written before the runs
- 2026-11-14T10:47 · proved · Quartic Berezin integral, Cauchy-Binet squared-minor formula, parity of avoiding cycles from Thomason (route-algebra, unreviewed)
- 2026-11-14T10:47 · refuted · Nullstellensatz, real stability, positive semidefinite blocks, universal residues, global sign gauge, unrooted invariants
- 2026-11-14T10:47 · computed · The Lean proof builds locally; axioms propext, Classical.choice, Quot.sound (lean-formalisation)
- 2026-11-14T10:48 · computed · Cross-check for this map: the two independent enumerations agree on all 7868 rooted triangulations up to 16 vertices
- 2026-11-14T10:48 · refuted · Structural shortcuts fail: LP integrality (13 vertices), single-swap descent (50), lattice extremes alone (40, 80), degree-4 induction (route-graph-theory)
- 2026-11-14T10:48 · proved · One exact Euler identity gives the pair criterion in both directions; pairs are alpha-orientations (route-graph-theory, under review)
- 2026-11-14T10:48 · proposed · Conjectures: lattice min or max carries a tree pair; a non-increasing exchange path exists
- 2026-11-14T10:50 · literature · The Lean proof differs from the paper in four places: algebraic dual, H- form, polynomial instead of exp, a flow on G instead of spoke circulations
- 2026-11-14T10:54 · reviewed · astra referee on route-combinatorics: FOLLOWS, with corrections (first-failure sizes 14 and 13 become 12 by reflection; scope of negative conclusions); independent recount to 16 vertices
- 2026-11-14T10:54 · reviewed · fable referee on the determinant claims of route-constructive and route-dimers: all CORRECT, two wording fixes; the two determinants coincide
- 2026-11-14T10:54 · proved · Parity of state cycles is enough for three of the four uses of the disk identity; the value 3 is used once (referee-determinants, unreviewed)
- 2026-11-14T10:54 · refuted · Positivity of the coefficient norm or of the constrained Laplacian terms does not give existence
- 2026-11-14T10:55 · answered · Dependency-graph conjecture A2 answered: not every avoiding Hamiltonian cycle comes from a tree matching (prism: 4 against 2); the image is characterised
- 2026-11-14T10:56 · documented · Lean report: the formal proof is simpler than the paper in five places; flow weights checked on 71224 rooted triangulations up to 18 vertices
- 2026-11-14T11:00 · proved · Topology: the disk identity as the theorem of turning tangents; cancellation as a Morse matching; last step as Alexander duality; tree matchings and sutured Floer homology (route-topology, unreviewed)
- 2026-11-14T11:00 · refuted · The partner of a tree matching need not be a tree matching (6 of 442)
- 2026-11-14T11:00 · proposed · Conjecture R6': local search from a point-rainbow tree reaches a tree matching (450 of 450 up to 16 vertices)
- 2026-11-14T11:15 · documented · Route map and labyrinth seeded: 16 waypoints, 17 steps, 167 routes
