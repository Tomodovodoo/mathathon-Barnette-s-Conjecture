# Labyrinth status

Generated 2026-11-14T13:45:27Z by `labyrinth/lab.py build`. Do not edit by hand.

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
| |V(T)| = 19 | 6562 | 1 | 201 | 0 | 0 | 6360 | 3.1% | upper 6561, upper_kind 3^(n/2) |
| |V(T)| = 20 | 11364 | 1 | 201 | 0 | 0 | 11162 | 1.8% | upper 11363, upper_kind 3^(n/2) |
| |V(T)| = 21 | 19684 | 1 | 201 | 0 | 0 | 19482 | 1.0% | upper 19683, upper_kind 3^(n/2) |
| |V(T)| = 22 | 34092 | 1 | 201 | 0 | 0 | 33890 | 0.6% | upper 34091, upper_kind 3^(n/2) |
| |V(T)| = 23 | 59050 | 2 | 201 | 0 | 0 | 58847 | 0.3% | upper 59049, upper_kind 3^(n/2) |
| |V(T)| = 24 | 102276 | 1 | 201 | 0 | 0 | 102074 | 0.2% | upper 102275, upper_kind 3^(n/2) |
| |V(T)| = 28 | 920483 | 2 | 201 | 0 | 0 | 920280 | 0.0% | upper 920482, upper_kind 3^(n/2) |
| |V(T)| = 33 | 14348908 | 2 | 201 | 0 | 0 | 14348705 | 0.0% | upper 14348907, upper_kind 3^(n/2) |

## Conjectures (19)

- **nodal domains of eigenvectors** [`k.TG.h2`, open] Sign patterns of Laplacian eigenvectors of T almost never give two induced trees (predicted below 5 per cent).
- **roots not on a common face** [`k.A.2`, open] For every simple 2-coloured triangulation some triple of roots of three colours, not necessarily the corners of a face, admits two disjoint states. The categorical agent tested the two-root version: the obstruction moves and the recovery lemma fails without a root face (A.x2).
- **Gauss-Bonnet form for any cycle** [`k.B.5`, open] For a state s and a simple cycle C avoiding the roots, B - W = 2m - h + 2, with m the boundary vertices whose matched face lies inside. The topology agent reports the orientation-free form W = B + 1 as proved (B.6); the status of this exact formula is in topo/ROUTES.md.
- **a test function with one sign on all covers** [`k.N.9`, open] There is a test function of s for which every cover contributes with the same sign, so that no minimum over the number of cycles is taken.
- **at least 2^m good states** [`k.D.3`, open] C1: every feasible root has #TM >= 2^m. Independently replayed on all rooted Eulerian triangulations through V=22; extended evidence on 23,824,742 separator-free facial roots through V=24. Equality iff one cover is also open beyond this range.
- **a canonical good pair** [`k.D.6`, open] Under a bijection from states to trinity arborescences, good states have a tree description that singles one out.
- **order-theoretic position in the state lattice** [`k.U.5h`, open] Outcome (topo): the good states are neither an interval nor an antichain of the clock lattice, and the top and bottom states are often good states. No order-theoretic pattern was found.
- **describe partnered Hamiltonian cycles in G alone** [`k.U.6h`, open] There is a description, without states, of the Hamiltonian cycles of G avoiding e0* whose state has a partner.
- **remove a leaf of the white tree** [`k.F.4`, open] Removing a leaf of the white tree with the black face whose spoke it crosses leaves a rooted triangulation with a good state, and the cycle of the larger graph is a local detour.
- **a cut-free root** [`k.G.3`, open] Count how often some root (black face on the black side of all separating triangles, or the same with colours swapped) exists.
- **ordered pairs of edges (global H+-)** [`k.G2.5`, open] Some Hamiltonian cycle contains x and avoids y for any two edges. Not implied by the theorem.
- **non-increasing exchange path to a good pair** [`k.N.11`, open] C3: from every ordered pair, D-swaps and Q-reversals never increasing q(s) reach a good pair. New T4 author census checks all 49,325,864 pairs through V=22 and all 9,970,784 pairs of 230 random triangulations at V=26..80. Sampled starts to V=200 succeed; three capped starts at V=300 undecided. Independent earlier reachability replay only through V=16.
- **Li's marked objects are the e_m coefficient** [`k.N.12`, open] Li's objects with m distinct marks are the elementary symmetric reading of the linear-weight coefficient.
- **local search from a point-rainbow tree** [`k.U.7h`, open] Step X: every point-rainbow tree reaches a good state by exchanges never increasing black excess. All rooted instances through V=17; all rootings of 1,485 of 1,543 triangulations at V=18, remaining 58 untested; samples to V=120. T4 evidence. R plus X would be counting-free, with no polynomial-time bound on plateau search.
- **every Hamiltonian cycle from a two-root good state** [`k.U.8h`, open] With two roots allowed to vary, the state method sees every Hamiltonian cycle.
- **contraction inequality tau(T) >= tau(T/ac)** [`k.D.9`, open] Contraction inequality #TM(T) >= #TM(T/M), conjectural on the rooted degree-four merge class. Checked on 1,202,792 rooted contractions through V=18. It does not imply that any contracted good state lifts directly.
- **ML1: preserve a pair in some merge** [`k.U.G`, open] G: every separator-free rooted T with V>6 has a non-root degree-four vertex with a simple opposite-neighbour merge admitting a pair. Checked on 62,416 separator-free facial roots through V=19. Proved without chordless five-cycles, separately U.G-partial; unrestricted G remains open.
- **ML2: two-sided existence lifting** [`k.U.ML2`, open] Induction X, also ML2: when both contractions have good states, some good state is non-exceptional and lifts or rotates successfully. One-sided case proved, new extension unreviewed. The whole-contraction half-exception bound survives all 7,940 exceptions through V=18. Repair confined to a cover fails; do not confuse induction X with rainbow Step X.
- **P2: two face-rainbow trees in every pair support** [`k.U.packing-P2`, open] Every pair support splits into two face-rainbow trees. True on all 14,881 supports with V<=17. Doing the face and point sides at once is the key lemma and fails inside a fixed support.

## Open doors (questions) (12)

- **Is there a polynomial-time construction of the Hamiltonian cycle?** [`q.poly-time`, open] The proofs give exponential search (3^(N/4), or 2^O(n log n) for the marked walk). Sampling states is polynomial; good states can be exponentially rare.
- **Is there an existence proof with no signed count?** [`q.structural`, open] No unsigned existence proof yet. Contraction has ML1 and ML2 open; C3 and rainbow exchange require plateaus. Two-tree packing is proved but does not see the states; its face-side twin P2 and exact rounding are open.
- **Is there a canonical good pair?** [`q.canonical`, open] No universal canonical good pair is known. C2 fails first at V=18; R2 fails at V=33. The signed sum is not a rank polynomial of the base lattice.
- **How many good states must there be?** [`q.tm-lower`, open] C1 is open. Independent all-root census through V=22; separator-free evidence through V=24. One cover implies equality; converse open.
- **Is there a determinant or Pfaffian for Z without coefficient extraction?** [`q.det`, open] Z is the squarefree coefficient of one determinant (2^n evaluations). Raw determinants, doubled edges and scalar factorisations are refuted.
- **Which Hamiltonian cycles come from good states?** [`q.which-hc`, open] Exactly those avoiding e0* whose state has a partner; equivalently partitions with acyclic white parent map. No description in G alone.
- **Is there a second proof of the disk identity?** [`q.disk`, answered] Signed-angle Gauss-Bonnet derivation independently AI-refereed with boundary corrections. No human check.
- **Can a different rooting remove the separating-triangle induction?** [`q.roots`, open] With t0 a face the obstruction is exact. Two roots off a face move the obstruction and break the recovery lemma (x.A.x2). Three roots of three colours off a face are untested, and the statement needs fixing first (which black face is dropped).
- **Do Li's higher-mark involutions match the polynomial coefficient?** [`q.li-b`, open] The marked-involution writeup has two AI referees, FOLLOWS on rays and drawing-free face paths.
- **What is the right statement on other surfaces?** [`q.surface`, open] Rooted cardinality fails by 2g. Root-free Heawood has odd-cycle cancellation but identically zero polynomial.
- **What is the status of formal verification?** [`q.formal`, open] The Lean proof builds locally with standard axioms and follows a different route in four places. Corollary 7.2 and Theorem 2.2 are not formalised.
- **Has a human checked any of the proofs written here?** [`q.human`, open] No human-checked claim is recorded. Claim-specific AI reviews are in the route nodes; new referee discoveries remain unreviewed.

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
- **cycle popping, random walk** [`h.N.3`, live] The two moves pop cycles of Q_s and of D, as in Wilson's algorithm. Show the walk hits a good pair fast.
- **Pfaffian gadget for the turn tensor** [`h.N.4`, live] Replace each black face by a planar matchgate with signature q^delta on distinct ordered corners and zero on equal corners.
- **height potential on pairs** [`h.N.5`, live] A combination of the two state heights that decreases along some exchange move at every non-good pair.
- **curved double-dimer connection, Lee-Yang** [`h.N.6`, live] Realise the loop factor -i e^{xL+} + i e^{xL-} as the trace of a non-flat connection.
- **LGV after cutting along seams** [`h.N.7`, live] Cut the pair diagram into non-intersecting paths and use a Lindstrom-Gessel-Viennot determinant.
- **abstract valuation theorem** [`h.N.8`, live] Axiomatise: a finite signed cycle system, two involutions, a positive circulation.
- **flux on a small set of faces** [`h.N.10`, live] Put positive flux only on a set of faces that meets the interior of every feasible D-cycle.
- **support of the tree-degree polynomial** [`h.U.1h`, live] Show the target degree vector d* lies in the support of det L_H(y), from plane incidence inequalities.
- **spanning-tree parity / matroid parity** [`h.U.2h`, live] 'Each black centre keeps exactly two of its three spokes' looks like the spanning tree parity problem that Feder and Subi solve in polynomial time for 2- and 3-sided faces. The exact Feder-Subi predicate also imposes the proper-quasi-vertex condition. This is a lead, not an algorithm for the joint state constraints.
- **Bernardi process, Schnyder woods, blossom trees** [`h.U.4h`, live] A canonical tree or orientation of the map might produce a good state directly.
- **Temperley / Kenyon-Propp-Wilson** [`h.E.2`, live] Read the step as the tree-to-matching bijection of KPW.
- **a potential along the selected out-edges** [`h.F.5`, live] Follow selected out-edges from a vertex to a root; a quantity that decreases along the walk proves connectivity.
- **Hall-free shelling construction** [`h.A.5`, live] Build a pair by a canonical ordering from t0 inward, as for Schnyder woods.
- **finding a good state is in PPAD** [`h.D.8`, live] Each phase of the marked walk follows a path in a graph of degree at most 2 with alternating signs.
- **older radial-tree dictionary and limits** [`h.TG.older`, live] The final report gives a radial/permeating-tree dictionary and rejects a direct identification with H-s. A direct Pfaffian transfer still lacks balanced incidence objects, disk identity and recovery.

## Dead ends (refuted) (77)

- **drop bipartite** [`x.S0.x1`, refuted] Without bipartiteness there is no proper face colouring of T, so states are not defined.
- **drop 3-connectivity** [`x.S0.x2`, refuted] A 2-connected cubic bipartite planar graph can be non-Hamiltonian. Its dual has parallel edges.
- **other surfaces** [`x.S0.x3`, refuted] On an orientable surface of genus g, |A| - |X| = 2g, so states with three roots do not exist for g > 0, and the two-tree target is impossible on the torus by an edge count.
- **trees from colour classes** [`x.TG.x1`, refuted] Build a permeating subtree containing all or none of a colour class of the vertex 3-colouring.
- **Grinberg obstruction** [`x.TG.x2`, refuted] Use Grinberg's formula with a modulus to decide Hamiltonicity.
- **every avoiding cycle comes from a good state** [`x.A.x1`, refuted] If every Hamiltonian cycle avoiding e0* came from a good state, known Hamiltonicity results would give pairs with no flow argument.
- **drop bijectivity** [`x.B.x1`, refuted] Let each black face choose a corner with no injectivity requirement.
- **sign as a product of two dimer weights** [`x.C.x1`, refuted] Write the local phase as alpha(r(t)) beta(s(t)) and get Z as a product of two incidence determinants.
- **choose the cycle using r** [`x.K.x1`, refuted] Let the reversed cycle depend on the partner.
- **zero, vertex-only or face-only weights** [`x.N.x1`, refuted] Use weights alpha_t + beta_v, or none.
- **parity or mod p count without weights** [`x.N.x2`, refuted] Show the number of good states is odd, or nonzero mod p.
- **good pair among the fewest-cycle pairs** [`x.N.x3`, refuted] Among the pairs with the fewest D-cycles one has Q_s a forest; or every cover D has an orientation that is a good pair.
- **highest or lowest partnered state** [`x.N.x4`, refuted] The top (bottom) partnered state of the lattice is a good state.
- **minimal cover, all cycles one way** [`x.N.x5`, refuted] Take D with m cycles and orient all of them counterclockwise (or clockwise).
- **largest rank difference** [`x.N.x6`, refuted] The pair maximising omega(s) - omega(r) is a good pair.
- **one cycle always suffices** [`x.N.x7`, refuted] m = 1, so a first-order argument is enough.
- **cubes of good states; sign = parity of rank** [`x.N.x8`, refuted] Good states split into cubes of dimension m; or eps(s) = (-1)^omega(s) up to a constant.
- **ordinary determinant, all face variables 1** [`x.N.x9`, refuted] Evaluate det(sum_t M_t) with no coefficient extraction.
- **allow doubled edges (standard double dimers)** [`x.N.x10`, refuted] Add a diagonal so that r and s may share edges, as in Kenyon's double-dimer determinant.
- **positive semidefinite blocks** [`x.N.x11`, refuted] Find a gauge in which the local matrices M_t are positive semidefinite, then use mixed-discriminant positivity.
- **Combinatorial Nullstellensatz** [`x.N.x12`, refuted] Get a nonzero evaluation of F from the coefficient form of Alon's theorem.
- **real stability of the tree-state polynomial** [`x.N.x13`, refuted] The unsigned generating polynomial of good states is real stable, like spanning-tree polynomials.
- **matching matroid meets graphic matroid** [`x.U.x1`, refuted] Treat the two endpoint constraints as one matroid and use Edmonds' two-matroid intersection.
- **unconstrained white spanning trees** [`x.U.x2`, refuted] Every spanning tree of the white-face graph, or of its restriction to duals of B, gives a good state.
- **trinity arborescences = good states** [`x.U.x3`, refuted] The Hine-Kalman bijection carries all states to arborescences; perhaps every arborescence is a good state.
- **Yutsis partition of G** [`x.U.x4`, refuted] Identify the two induced trees with a Yutsis decomposition of the cubic graph.
- **a good state is enough** [`x.R.x1`, refuted] Call s good as soon as Q_s is acyclic, with no partner assumed.
- **prescribe whatever each cut needs** [`x.G.x1`, refuted] Strengthen the induction hypothesis to an arbitrary set of prescribed edges.
- **LP relaxation of the three constraints is integral** [`x.U.x5`, refuted] Perfect matchings of B intersected with complements of spanning trees of H form an integral polytope.
- **induction by degree-4 expansion** [`x.U.x6`, refuted] Lift a good state through the expansion of a degree-4 vertex.
- **positivity of the norm or of the Laplacian terms** [`x.U.x7`, refuted] CT F(w)F(1/w) and the constrained Laplacian coefficient are sums of nonnegative terms, so they are positive.
- **tree count as an unrooted invariant** [`x.U.x8`, refuted] The number of good states equals a fixed evaluation of a Tutte, Penrose, Tait or flow invariant of G.
- **single-swap descent on the number of Q-cycles** [`x.N.x14`, refuted] From every pair with a cycle in Q_s some single exchange lowers the number of cycles.
- **a global sign gauge on incidences** [`x.N.x15`, refuted] Flip signs of incidence variables so that all good states get the same coefficient sign.
- **extremes of Felsner's lattice of pairs** [`k.D.7`, refuted] C2 is false. Both true lattice extremes can have no good pair. Independent exhaustive minimum-order check finds 26 failures at V=18 and none below.
- **the partner of a good state is a good state** [`x.D.x1`, refuted] Swapping r and s would then be a free involution on good states and explain why their number is even.
- **a uniform boundary condition for longer cuts** [`x.G.x2`, refuted] Induct along cuts of length 5 or more with a boundary condition that every piece satisfies.
- **two roots instead of a root face** [`x.A.x2`, refuted] Root at two vertices not tied to a face; every root pair then has a two-root good state, and it gives a Hamiltonian cycle.
- **the two cube structures form a bicomplex** [`x.K.x2`, refuted] Treat reversal of Q-cycles and reversal of D-cycles as two commuting differentials and read the proof as homology.
- **topological Hall for partial good states** [`x.U.x9`, refuted] Get a good state from connectivity of the complex of partial good states.
- **distance one from a lattice extreme** [`x.D.ext1`, refuted] R1: success within cover-distance one of an extreme.
- **R2: extreme or irreducible** [`x.D.ext2`, refuted] A bottom, top, join-irreducible or meet-irreducible element need not carry a good pair.
- **BF21 parity equals black-inner obstruction** [`x.TG.parity`, refuted] Identify the even-interior condition of the older contracted graph with the black-inner separator obstruction.
- **signed sum as base-lattice rank polynomial** [`x.N.rank-dead`, refuted] Read the pair sum from the ordinary rank polynomial of the factor lattice.
- **fixed-cycle-count flip connectivity** [`x.D.level-dead`, refuted] Covers with the same c, including minimum-c covers, form a connected flip level.
- **some contracted good state lifts directly** [`x.U.lift-dead`, refuted] If T/M has good states, at least one lifts directly to T.
- **surplus walk always terminates** [`x.U.walk-dead`, refuted] The surplus walk alone reaches smaller black excess.
- **positive full-spoke UST mean fitting** [`x.U.mean-dead`, refuted] Finite positive weights on the full spoke graph cannot attain the forced target degrees in expectation under a full-support spanning-tree law. This does not exclude conditioned or boundary-supported positive measures.
- **joint Lorentzian rounding** [`x.U.support-dead`, refuted] Joint endpoint degree support inherits M-convexity from the spanning-tree polynomial.
- **universal analytic root locations** [`x.N.zeros-dead`, refuted] Signed z-polynomials have unit-circle roots or linear-weight polynomials have only real roots.
- **root-free torus nonvanishing** [`x.N.heawood`, refuted] Transfer spherical signed nonvanishing directly to Heawood on the torus.
- **induction R1: Lift lemma, only-if half (route-graph-theory PROOFS Lemma 6.** [`x.U.ind-R1`, refuted] Lift lemma, only-if half (route-graph-theory PROOFS Lemma 6.2(iii)): if the lift s of s' is a TM then s' is a TM R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R2: Degree-4 contraction preserves the existence of a pair** [`x.U.ind-R2`, refuted] Degree-4 contraction preserves the existence of a pair R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R3: Every TM of T/M lifts to a TM of T** [`x.U.ind-R3`, refuted] Every TM of T/M lifts to a TM of T R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R4: Failing lifts are compensated within the same type (B >= b)** [`x.U.ind-R4`, refuted] Failing lifts are compensated within the same type (B >= b) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R5: Some TM of T/M satisfies the local condition LC (edge a v in** [`x.U.ind-R5`, refuted] Some TM of T/M satisfies the local condition LC (edge a v in Q) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R6: rho(lift) is a TM for every failing lift** [`x.U.ind-R6`, refuted] rho(lift) is a TM for every failing lift R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R7: TM(T) >= 2 TM(T/M)** [`x.U.ind-R7`, refuted] TM(T) >= 2 TM(T/M) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R8: lowest coefficient lc = sum over D with m cycles of prod** [`x.U.ind-R8`, refuted] lowest coefficient lc = sum over D with m cycles of prod_C (white faces inside C) is monotone under contraction R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R9: m(T) = m(T/M) (when both have pairs)** [`x.U.ind-R9`, refuted] m(T) = m(T/M) (when both have pairs) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R10: Skein relation TM(T) = TM(T/M) + TM(T/N) (both merges define** [`x.U.ind-R10`, refuted] Skein relation TM(T) = TM(T/M) + TM(T/N) (both merges defined) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R11: Prescribed corner: for every face t in A and non-root corner** [`x.U.ind-R11`, refuted] Prescribed corner: for every face t in A and non-root corner u, some TM has s(t)=u (HCs); same for the mate r (HCr) R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R12: A good contraction (result has a pair) always exists** [`x.U.ind-R12`, refuted] A good contraction (result has a pair) always exists R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **induction R13: Inverse P-operation (Batagelj) preserves pairs** [`x.U.ind-R13`, refuted] Inverse P-operation (Batagelj) preserves pairs R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.
- **rainbow loads are M-convex** [`x.U.loads-dead`, refuted] Rainbow load vectors satisfy simultaneous M-exchange.
- **every maximal lattice chain hits success** [`x.D.chain-dead`, refuted] Every maximal chain contains an element carrying a good pair.
- **at least half the lattice succeeds** [`x.D.fraction-dead`, refuted] At least half the factor lattice admits a successful direction choice.
- **strict black-excess descent** [`x.U.rainbow-strict`, refuted] Every positive-excess rainbow tree has an immediately decreasing exchange.
- **four rainbow distance potentials** [`x.U.rainbow-pot`, refuted] Tree or spoke-graph distances between loaded and empty faces, minimized or summed, always guide exchange.
- **innermost bad-disk selection** [`x.U.G-inward`, refuted] The specified local repair always closes the induction.
- **innermost bad five-cycle selection** [`x.U.G-five`, refuted] The specified local repair always closes the induction.
- **fixed-cover exceptional repair** [`x.U.X-cover`, refuted] The specified local repair always closes the induction.
- **round within a fixed pair support** [`x.U.pack-support`, refuted] Every pair support contains a good state, meeting both rainbow constraints.
- **bounded-lookahead q descent** [`x.N.lookahead`, refuted] The specified potential or lookahead always reaches a good pair.
- **height and cover-count tie-breaks** [`x.N.height-ties`, refuted] The specified potential or lookahead always reaches a good pair.
- **uniform rainbow mean load one** [`x.U.rainbow-mean`, refuted] The uniform rainbow tree has expected load one at every bounded black face.
- **resident involutions act transitively** [`x.U.evict-transitive`, refuted] The n resident-eviction involutions connect every good state.

## Under review (4)

- **exactly one good state is impossible** [`p.D.4`]
- **the gluing needs the same-label edge** [`p.G.2`]
- **pairs are alpha-orientations (Felsner lattice)** [`p.A.6`]
- **real-sign and finite-difference Lean replacement** [`c.G2.devices`]

## Recent events (76 total)

- 2026-11-14T11:12 · refuted · No uniform boundary condition at cut length 5; two roots do not replace the root face; the two reversals do not commute; topological Hall fails
- 2026-11-14T11:12 · proposed · Conjectures: every Hamiltonian cycle comes from a two-root tree matching; contraction never increases the number of tree matchings
- 2026-11-14T11:08 · computed · Own spot check on bipyramids: counts, signs, odd D-cycles confirmed; the cycle-to-state map is not injective off the tree matchings (prism: 4 avoiding cycles, 3 states)
- 2026-11-14T14:00 · reviewed · Digestion audit: corrected polynomial reflection, replayed Li multi-mark involutions, integrated provisional 18-vertex lattice refutation and new manuscript routes; preprints no longer imply T1. Timestamp is audit-day bookkeeping, not a claimed discovery time.
- 2026-11-14T14:01 · reviewed · Late report integration: topology referee corrections and older-approaches unbounded-chain result. Audit-day bookkeeping timestamp. New RAINBOW proof file still unavailable.
- 2026-11-14T15:00 · refuted · Map refresh, attributed report integration: R2: extreme or irreducible. A bottom, top, join-irreducible or meet-irreducible element need not carry a tree pair. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:01 · reviewed · Map refresh, attributed report integration: extremes of Felsner's lattice of pairs. C2 is false. Both true lattice extremes can have no forest pair. Independent exhaustive minimum-order check finds 26 failures at V=18 and none below. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:02 · computed · Map refresh, attributed report integration: C1 and equality census through dual order 24. 23,824,742 facial roots of 4-connected Eulerian triangulations, V<=24: no C1 or equality-characterization violation. Maximum c_min=6 at V=23. T4 under review, not an independent certification of the inherited C engine. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:03 · proved · Map refresh, attributed report integration: primal meaning and unbounded c_min without separators. For an admissible edge deletion S, c(D)=components(G-S)-1. Explicit T_m, V=3m+2, has no separating triangle, one cover with m-2 triangles and one pentagon, c_min=m-1 and #TM=2^(m-1). Author proof and finite checks, unreviewed. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:04 · refuted · Map refresh, attributed report integration: some contracted tree matching lifts directly. If T/M has tree matchings, at least one lifts directly to T. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:05 · proved · Map refresh, attributed report integration: degree-four contraction and rotation. State splitting, exact lift criterion, local sufficient condition, rotation and partial injection are AI-refereed. One-sided existence lifting is proved in ri/RESIDUAL-CASES.md; this new extension is unreviewed. Full induction has two missing lemmas. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:06 · proposed · Map refresh, attributed report integration: ML1: preserve a pair in some merge. Every separator-free rooted T with V>6 has a non-root degree-four vertex and a simple opposite-neighbour merge with a pair. All 62,416 separator-free facial roots, 8<=V<=19, pass. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:07 · proposed · Map refresh, attributed report integration: ML2: two-sided existence lifting. If both contractions at a non-root degree-four vertex have tree matchings, not all matchings of either contraction are exceptional. One-sided case is proved; all tested cases through V=18 pass. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:08 · proved · Map refresh, attributed report integration: Rado-Euler rainbow tree and unique factor. Theorem R proves rainbow existence exactly at feasible roots. Theorem S completes each rainbow tree to a unique incidence 2-factor. Reversible surplus walks give fixed-point-free involutions on tree matchings. New proofs T2 unreviewed. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:09 · refuted · Map refresh, attributed report integration: surplus walk always terminates. The surplus walk alone reaches smaller black excess. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:10 · refuted · Map refresh, attributed report integration: positive full-spoke UST mean fitting. Finite positive weights attain the target degrees on all of H. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:11 · proposed · Map refresh, attributed report integration: two white trees in every pair support. Every selected pair support partitions into two white spanning trees. 278 nonvacuous rank tests and 27 larger packings through V=120 support it. Packing supplies fractional feasibility, not degree-preserving rounding. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:12 · proved · Map refresh, attributed report integration: Pfaffian corollary through GSW 4.16. Conditional on the supplied planar theorem, the opened GSW Theorems 4.4, 4.9, 4.12, 1.7 and 4.16 imply Corollary 7.2. One-step trisum gluing uses six path signatures. New inference unreviewed. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:13 · refuted · Map refresh, attributed report integration: root-free torus nonvanishing. Transfer spherical signed nonvanishing directly to Heawood on the torus. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:14 · documented · Map refresh, attributed report integration: merged dual exposition. Written dual route uses product of local signs, heights along face paths, and an explicit connectivity lemma inside a selected cycle. Under two AI reader reviews; no final verdict at integration. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T15:15 · documented · Map refresh, attributed report integration: complete marked involution exposition. Written bijective route through marked objects and two involutions. Under independent AI referee; no final verdict at integration. New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.
- 2026-11-14T12:30 · reviewed · Late merged-paper referee: main theorem FOLLOWS; eight edits proposed, including off-route Laurent terminology; application not certified. Human check pending.
- 2026-11-14T13:45 · documented · Final map integration: 244 routes, 77 retained refutations; tiers kept separate from AI review.
- 2026-11-14T13:45 · reviewed · Main v2 FOLLOWS, both involution routes FOLLOWS, revised primal ACCEPT; no human check. Covers and prescribed-root families have claim-specific AI reviews.
- 2026-11-14T13:45 · computed · Reference-checker replay of four descent certificates at dual orders 16, 21, 60 and 40: escape radii 2, 3, 4 and 3. Not a new census.
