# Independent referee report on the graph-theory route

Referee: gpt-6.1-sol. Source boundary: the submitted `REPORT.md`, `PROOFS.md`, `ROUTES.md`, saved input instances, and the three supplied papers. I read author code to identify what was claimed and what fields were saved, but imported and executed none of it. Every computation below uses my own implementation in `code/`. The reference implementation was not used either.

The verdict concerns the supplied route, rather than every conceivable proof of the theorem. `CORRECT` means the stated argument closes after routine details are made explicit. `CORRECT AFTER FIX` records a necessary change. `GAP` does not mean false. `WRONG` is accompanied by an independently checked counterexample. Results established here remain T2 with one AI referee, human check pending. Finite computations are `COMPUTED`, without a claim that my audit independently generated the entire isomorphism census.

## Boundary and accepted inputs

T is a simple sphere triangulation with proper black/white face colouring, t0 is black, R its three corners, A the remaining black faces, and X the nonroots. A state is a perfect matching A→X. A pair is ordered and disjoint at every face. A tree matching satisfies H−s being a spanning tree. A forest Q_s without a partner or a root condition is not enough.

Accepted primitives are Euler's formula, signed incidence counting, integral max-flow, elementary matroid definitions and duality, sphere tree/cotree duality, and Jordan separation. For the pair-to-tree existence implication I use the supplied central Proposition 5.1 as an explicit earlier input. I checked its stated hypothesis: its cancellation and nonvanishing proof requires a pair, not an absence of all separating triangles. I do not confer publication status on the supplied 2026 preprints.

## A. The three-matroid formulation

Exact claim: tree matchings are common bases of the cographic matroid of H and the two capacity-one incidence partition matroids, or of the opposite-edge graphic matroid of T/R and the two corresponding partitions. No constraint in either natural triple can simply be omitted. Duality leaves a triple.

Proof ledger for Lemma 1.1:

1. `PROVED-HERE`. H has 2n+4 vertices and 3n+3 edges, so its cographic rank is n. The two partition ranks are also n. Their common bases are exactly perfect matchings of B with tree complement. This inference is correct on the full spoke set, with capacity zero at the outer centre and at roots.
2. `PROVED-HERE`. Mapping a spoke to the opposite side is an edge bijection. Once the centre partition is imposed, the retained incidence graph is a subdivision of Q_s plus the outer star. Its tree condition is equivalent to the opposite edges being a tree after identifying R. Thus the alternative triple is correct.
3. `REFUTED`. The text goes further and says that the restricted cographic matroid itself becomes the graphic matroid under this map. That statement is false before imposing the centre condition. In the octahedron with roots {0,3,4}, choose spokes ((0,2,1),1), ((0,2,1),2), ((1,5,4),1). The cographic set is not a basis, whereas its opposite edges are a graphic basis of T/R. This is the saved counterexample in `code/matroids.json`. Repeated deletion at one centre destroys the subdivision argument.
4. `PROVED-HERE`, finite witnesses `COMPUTED`. All three conditions are needed. On the full spoke ground set of the octahedron, cographic∩centre has 14 bases and cographic∩vertex has 8, against 2 tree matchings. For the graphic formulation, graphic∩centre has 14 and graphic∩opposite-vertex has 2 there; the latter grows to 6 against 2 tree matchings at V=8. Dropping the graphic/cographic condition gives 3 states against 2 trees at V=8. These counts use all full-graph spokes when a dropped partition would otherwise exclude root spokes.
5. `PROVED-HERE`. Complementing common bases dualizes each matroid. A partition dual has block capacity block-size minus the original capacity. Relabelling by plane duality makes the cographic matroid graphic and leaves two partition constraints. Both operations preserve the number of constraints in this displayed formulation.
6. `GAP`. None of those steps proves that no other pair of matroids, perhaps on another ground set or using another encoding, can describe the special spoke class. The claim that no Edmonds-type theorem can exist in any form is stronger than the evidence. The report itself acknowledges this in its hole-test discussion.

Verdict: CORRECT AFTER FIX. Retain the two natural triples and their irredundancy. Remove the asserted unrestricted matroid isomorphism and the universal impossibility conclusion. The failure of the base-exchange axiom for tree matchings is immediate: distinct perfect matchings cannot differ by replacing a single spoke, so the nontrivial common-base family is not itself a matroid base family.

## B. Abstract NP-hardness

Exact claim: on planar bipartite graphs of maximum degree three, deciding whether some perfect matching leaves a spanning tree is NP-hard under polynomial-time Turing reductions.

`LIT`. I located and opened the actual source: Takanori Akiyama, Takao Nishizeki and Nobuji Saito, *NP-Completeness of the Hamiltonian Cycle Problem for Bipartite Graphs*, Journal of Information Processing 3(2), 1980, 73–76. Its first page and Section 2 explicitly treat 2-connected cubic bipartite planar graphs. The other class in the abstract is 3-connected cubic bipartite graphs without a planarity restriction. The author-hosted scan is [here](https://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J029.pdf). A local source copy and first-page rendering are in `sources/`.

Proof ledger for Proposition 1.2:

1. Choose two incident edges e1,e2 at one vertex of a cubic input G. Every Hamiltonian cycle uses at least one of them. Correct.
2. Query K=G−e for each chosen e=uw. Planarity, bipartiteness and maximum degree three survive. Correct; 3-connectivity is not promised or needed.
3. A Hamiltonian cycle through e leaves a perfect matching of G avoiding e. In K its complement is the Hamiltonian path C−e. Correct.
4. Conversely, a perfect matching of K leaves degree one at u,w and degree two elsewhere. A connected acyclic graph with those degrees is a spanning u-to-w path. Restoring e makes a Hamiltonian cycle. Correct.
5. The original answer is the OR of the two oracle answers. This is a polynomial Turing reduction. It is not, as written, a many-one reduction. Correct under the stated reduction convention.

Verdict: CORRECT. `PROVED-HERE` conditional on the exactly applicable published hardness theorem, whose source is now checked. A small definition-level check is available on the cube and prism from the complete Hamiltonian-cycle enumerations in `code/limits.py`; the reduction equivalence is also an elementary proof for every cubic input. The complexity result concerns the broader maximum-degree-three class. It does not settle the complexity of the total search problem on the special rooted spoke graphs.

## C. A fractional LP vertex

Exact claim: the perfect-matching polytope of B intersected with the cographic base polytope of H has a half-integral vertex at dual order 13.

`COMPUTED`, exact certificate. `code/structure.py lp` reconstructs the saved rotation and root. It passes to the plane dual H*, whose vertices are the 11 white faces, and checks all 2,047 nonempty vertex-subset forest inequalities. The point has matching row and column sums one and total weight ten. Its nonnegativity constraints, matching equations and tight subset constraints have rank 25 over the rationals, equal to the full number of variables. Thus it is feasible and is an actual vertex. This is stronger than merely finding a fractional optimizer numerically.

The submitted output saves only the fourteen fractional coordinates, all 1/2. It omits the three coordinates equal to one. There are two feasible integral completions of this partial dump. The complete certificate I use sets

\[
x_{((4,9,8),8)}=x_{((7,9,11),9)}=x_{((7,6,8),7)}=1.
\]

All unspecified coordinates are zero. `code/lp-certificate.json` records the complete variable list, dual edges, a full-rank independent set of active rows, and both support matchings.

`REFUTED`. The subsidiary description "the average of two non-tree states" is wrong for the saved fractional support with this completion: its two support states have tree flags `[true,false]`. Testing the other integral completion also does not produce two non-tree support states. This does not affect the fractional-vertex conclusion. A midpoint of a feasible state and an infeasible state can be an extreme point of an intersection.

`GAP`. Ten random objectives per instance do not prove that V=13 is the first fractional order. I certify existence at 13, not minimality.

Verdict: CORRECT AFTER FIX for the report's full paragraph; CORRECT for the specific half-integral-vertex claim in the assignment.

## D. Euler identity and the exact obstruction

Exact claim: for a connected induced K on p≥3 vertices, m edges and b actual black faces,

\[
m-b-2p+4=\tfrac12\sum_F(\beta(F)-d(F)+4).
\]

A pair exists exactly when there is no black inner-boundary separating triangle.

Proof ledger for Lemmas 2.2, 2.3 and Theorem 2.1:

1. Euler gives p−m+b+w+q=2. Side counting gives 2m=3b+3w+Σd. Eliminating m and p yields one-half of w−b−Σ(d−4). Correct algebra.
2. Actual faces together with the original faces in the other regions partition the sphere faces. Their total signed balance is zero, so w−b=Σβ. Correct, including non-simple boundary walks.
3. Cancelling internal black/white edge sides gives 3β=Σσ. Parity gives β≡d modulo two. The d=4,5,≥6 bounds are each valid. Correct.
4. The capacity-one incidence network gives the exact two-matching cut inequality. Including t0 in the shortfall count gives the density inequality with constant four, not two. Correct.
5. Removing the strict interior of a black-inner triangle leaves one nonactual region of d=3,β=1, hence excess one. Correct and sharp.
6. For sufficiency the root component has no bad bounded triangular region. Other components may have one exceptional triangular region containing t0, costing at most one. The weaker bound 2p for those components suffices. Correct. The source's phrase `m−b≤3≤2p` needs the trivial separate p=1 check, since 3≤2 fails there; the actual one-vertex contribution is zero. This is an arithmetic presentation issue, not a gap in the result.

`COMPUTED`. `code/euler_alpha.py euler` checked the identity on 28,718 connected induced subgraphs, all such vertex subsets of size at least three in every saved graph through V=12. `code/audit.py census` independently checked matching enumeration, flow, the separator test and tree-complement existence on all 1,206 facial rootings through V=14. No disagreement occurred.

Verdict: CORRECT, with the singleton wording repaired. Complete final proofs are in `INTEGRATION.md`, Sections 1 and 2.

## E. Sharp primal condition and gluing

Exact claims: Li's reduced incidence graph has a 2-factor exactly when b0 belongs to the black-ended shore of every nontrivial 3-edge cut. The induced-tree theorem can be proved by splitting only at obstructing black-inner triangles.

Proof ledger for Sections 4 and 5:

1. A 3-connected cubic simple graph has no edge cut of size one or two. Thus every shore of a 3-cut is connected, since otherwise its components each need boundary at least three. The cut is a bond and dualizes to a triangle. Correct.
2. A nontrivial shore has odd order at least three and at least as many internal edges as vertices. Thus the triangle is separating exactly for nontrivial cuts, which are cyclic cuts here. Correct.
3. The displayed bipartite degree balance forces all three cut endpoints on each shore to have the same colour. Identifying inner faces with shore endpoints gives the exact root condition. Correct.
4. The direct recovery and Proposition 5.1 require only a pair after the density step. Hence a white-inner separator does not force recursion. Correct applicability check.
5. The cap signs are equal by divisibility by three. Adding the opposite-colour cap preserves face bicolouring and even degrees. Both pieces are smaller and simple. Correct.
6. The first piece determines one same-label cap edge; prescribing that edge in the second piece aligns the labels. Each pair of same-label trees meets in exactly a vertex or an edge, so its union is a tree. No edge joins strict interiors. Correct, and this boundary prescription cannot be dropped.

Li's alternative minimal-deficit proof also supports the sharp sufficient hypothesis directly. Its connected union G_S of selected facial cycles has no bridge. In maximum degree three such a connected union cannot have a cut vertex: two components at that vertex would each need at least two incident edges, since a single incident edge would be a bridge. This supplies the omitted justification for 2-connectivity. If a white vertex sees just one selected face, deleting that face drops the two neighbouring black contributions by at least one each and preserves positive deficit, contradicting minimality. Thus the cut has only black ends in G_S. The displayed Euler calculation gives deficit `4−2k−|δ(G_S)|/3`; the excluded root face ensures k≥1, so positive deficit gives |δ(G_S)|≤3. Edge connectivity forces equality. The nontrivial cut's black-ended shore is G_S and avoids b0, contradicting precisely the sharp rooted condition. This checks the substantive steps of Li's Lemma 9 without treating its original cyclic-connectivity assumption as necessary.

`COMPUTED`. The independent gluing checker handles all 3,618 prescribed root edges in the 55 saved graphs. It cuts only at black-inner separators and verifies the induced-tree result after every union. Its base solver is fresh exhaustive partition enumeration, not the author's matching constructor. Thus it checks the gluing mechanism separately from the central existence proof.

Verdict: CORRECT. The theorem is sharp for the rooted 2-factor conclusion of Li's Lemma 9. It is not a replacement for the whole main theorem's 3-connectivity assumption. Final statements and proofs are in `INTEGRATION.md`, Sections 3 and 4.

## F. Alpha-orientations and the lattice

Exact claim: ordered pairs modulo independent reversals of their D-cycles are in bijection with alpha-orientations of H−t0, with outdegrees 2 at bounded black centres, d_x−2 at nonroots, and d_r−1 at roots, where d_v counts black incident faces in the full graph.

Proof ledger for Lemma 3.1:

1. The pair union is a 2-factor of B, and its alternating decompositions are exactly its independent cycle orientations. Correct; quotienting only by a global swap would be insufficient when there is more than one cycle.
2. Deleting the unused corner in each bounded black face gives the required vertex multiplicities. A root's every remaining spoke is unused, since roots are not in B. Correct. A black face other than t0 cannot contain two roots, since their edge already has t0 as its black owner.
3. Direct used spokes centre-to-corner and unused spokes corner-to-centre. Every centre has outdegree two and the stated corner outdegrees follow. Conversely a root has outdegree equal to its entire degree in H−t0, so no used spoke ends at a root. Every nonroot receives precisely two used spokes. The used graph is therefore exactly a 2-factor of B. Correct.
4. `LIT`. Felsner's Theorem 1 applies to every plane graph with a feasible alpha function. Feasibility here is equivalent to a pair. The theorem is in Stefan Felsner, *Lattice Structures from Planar Graphs*, Electronic Journal of Combinatorics 11(1), 2004, R15, DOI 10.37236/1768. I opened the [full paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r15/pdf/). Essential directed cycles, rather than merely original facial cycles, are the cover operations in the general case.

`COMPUTED`. `code/euler_alpha.py alpha_small` separately enumerates every capacity-valid deleted-corner map and compares it with every pair quotient, on all 1,206 roots through V=14. The 932 factor occurrences agree exactly. The lattice statement is conditional on nonemptiness, as required by Felsner.

Verdict: CORRECT for the bijection and lattice; CORRECT AFTER FIX if the prose identifies the facial-flip order with the entire lattice without checking rigid-edge effects.

## G. Degree-four expansion

Exact claim of Lemma 6.2: the restricted states lift bijectively, their opposite edges have the displayed split-plus-two-edges description, and a lifted state is a tree matching if and only if the contracted state is a tree matching and the side test succeeds.

1. `PROVED-HERE`. With x and both split vertices nonroots, the old state covers every old nonroot except the unused split copy. The two new black faces then have exactly one way to cover that copy and x while avoiding their a,b corners. Projection and lifting are inverse. Correct.
2. `PROVED-HERE`. Reading the two opposite edges gives `split(Q_s') + {x c1,c2 v*}`. Correct.
3. `PROVED-HERE`. If s' is a tree matching, splitting v in its root-augmented tree gives two components; x c1 makes x a leaf, and c2 v* joins the components exactly when c2 lies on the other-copy side. This proves the stated side test conditional on s' being a tree matching. Correct.
4. `REFUTED`. The word "Hence" does not prove that a tree lift must contract to a tree state. Splitting can destroy a pre-existing cycle. `code/contractions.json` gives V=11, outer face (3,5,2), x=9, split copies 4 and 10. The contracted state's face list is

   `(3,7,0),(3,4,8),(4,0,6),(4,5,1),(7,8,6),(0,1,2)`

   and its state is `(0,8,6,4,7,1)`. It is not a tree matching. Its unique restricted lift is `(0,8,6,4,9,7,1,10)` in the saved large-face order and is a tree matching. The rotation and both complete states are saved.
5. `GAP` in the original domain. Merely saying x is not on t0 does not ensure both merged vertices are nonroots. If the merged vertex is a root there is no t* with s'(t*)=v. Add the nonroot hypothesis for the given formula or prove a separate root case.

`COMPUTED`. Through V=13 I checked 6,638 restricted state lifts for valid simple contractions with both split copies nonroots. The conditional side test passed all 2,896 tree inputs. There were 274 failed lifts of tree inputs and 214 tree lifts from non-tree inputs. Counts here include all labelled facial rootings and therefore are not the author's symmetry-reduced case counts.

Verdict: WRONG as the unconditional biconditional, CORRECT AFTER FIX as the restricted lift bijection and conditional side test. The generation lemma's local planarity argument is separate and is not refuted by this failure.

## H. Induced-tree partitions and the exact image

Exact claim: for fixed t0,e0, orient the monochromatic forest minus e0 towards its three roots, read the tail in each bounded black face, and recover a state. This is a left inverse to the constructor on tree matchings. The image consists exactly of partitions with acyclic white parent map.

Proof ledger for Theorem 7.2:

1. Removing e0 separates its root endpoints and leaves the third root in the other tree. The resulting three components each have one root. Outdegree one at each nonroot supplies the bijection. Correct.
2. In a constructed forest the edge at t is oriented from s(t). A rooted tree has a unique orientation with those outdegrees, so the inverse reads s. Correct.
3. Given an inverse state with white graph a tree, the selected side assigns each white-tree edge to an incident non-root endpoint once. Peeling leaves, or orienting towards y0, shows that assignment is unique. Therefore reconstruction returns the original partition. Correct.
4. The white parent map's arcs are precisely the deleted-spoke dual edges, with one outgoing arc off y0 and none at y0. It is acyclic exactly when that graph is a tree. Correct. For the constructor's endpoint assignment one may say the edge is assigned away from y0; for the resulting parent arc one says towards y0. These are compatible descriptions, not conflicting orientation rules.

`COMPUTED`. The independent census checks 9,720 constructed images and 35,664 prescribed induced-tree partitions through V=14. There are no collisions or inverse failures. The stronger fable dichotomy, "tree matching or no partner", also passes all these partitions.

Verdict: CORRECT. Section 5 of `INTEGRATION.md` gives the full proof and incorporates the stronger dichotomy with an independent check of its supplied geometric argument.

## I. Saved counterexamples

All entries below are `COMPUTED` or `REFUTED`, supported by fresh definition-level checks. The size refers to dual vertices.

| Saved claim | Independent result | Verdict |
| --- | --- | --- |
| V=10 matching-lattice minimum need not be a tree | Exhaustive all-cycle extremality and tree-complement tests reproduce failures | CORRECT |
| V=12 neither matching-lattice extreme need be a tree | Ten feasible facial roots have both extremes non-tree | CORRECT |
| V=40 `ef_fail_40_40` has no tree orientation | D has length 37; both second states have k=1 | CORRECT |
| Same V=40 factor is a minimum | No counterclockwise directed cycle, certified with rational area weights and feasible shortest-path potentials | CORRECT |
| `alpha_min_fail_40_41` is a lattice minimum | It has directed cycles in both senses; one full reversal reaches a minimum with six tree seconds | WRONG for that saved label |
| V=50 strong descent fails | The saved mate has D lengths 27,5,15; the 15-cycle meets a Q-cycle and preserves k=1. The other mate has one 47-cycle and also preserves k | CORRECT AFTER FIX to the caption that called the stored mate itself Hamiltonian |
| V=50 `deeptrap_50_1` is a weak-descent trap | Both mates checked; all six single swaps preserve k=1; a non-increasing two-move path reaches k=0 | CORRECT |
| V=80 `alpha_max_fail_80_83` is a lattice maximum without trees | Its D is a 77-cycle and both orientations are non-tree, but it has directed cycles in both senses. A full clockwise-cycle reversal reaches a maximum with six tree seconds | WRONG as a maximum certificate; CORRECT as a no-tree factor |
| A genuine maximum can have no tree orientation | The saved V=120 `alpha_max_fail_120_123` requires zero full reversals towards its maximum and has no tree second state | CORRECT, independently certified |
| fable's V=16 factor has no forest pair | 26 states, 18 ordered pairs, 12 tree matchings, three factors; one factor has two non-tree orientations | CORRECT; smaller than Opus's example |

The rational extremality test does not assume facial flips suffice. It solves the Tutte barycentric embedding exactly, places black centres at their corner means, and gives an oriented spoke the signed area weight x_u y_v−y_u x_v. A simple cycle's weight is twice its signed area. Bellman–Ford detects a cycle of either sign. A shortest-path potential is an exact certificate that no cycle of one sign exists. The embedded edges do not cross, so the signs detect the required sense of every directed cycle.

## J. Precisely stated conjectures and independent tests

`CONJECTURE`, O6. For every rooted simple Eulerian sphere triangulation with at least one pair, at least one of the true minimum and true maximum alpha-orientations of H−t0 has a 2-factor whose independent alternating decompositions contain a second state s with H−s a tree. The order is Felsner's full directed-cycle order with the given outer face. This differs from terminating a greedy search on original faces. The claim has no polynomial-time consequence until the search among a factor's 2^c decompositions is bounded or replaced.

`COMPUTED`. All 880 feasible rootings through V=14 pass O6. I also computed both true extremes on eight saved stress inputs of order 40,60,80,100,120. None is a joint failure. Some reported facial failures disappear when an essential nonfacial cycle is reversed. `code/alpha-large.json` gives the actual factors and counts. This modest test supports the corrected conjecture, not the author's unverified facial interpretation.

`CONJECTURE`, monotone D3. In the exchange graph on ordered pairs, whose edges are one D-cycle swap or one Q_s-cycle reversal, every vertex has a path to a tree pair on which k(s), the number of rootless unicyclic components of Q_s, never increases. Q-reversals keep s fixed. Allowing a new mate between D-swaps means traversing these Q-edges; it is not an unrecorded free move.

`COMPUTED`. A reverse-reachability search in the directed graph of non-increasing exchanges checks every one of the 3,280 ordered pairs in all roots through V=14. It also checks all 18 pairs of the fable V=16 example. The saved V=50 trap has a two-edge non-increasing path to a tree pair. This is an exact finite graph test. It is not evidence of a uniform two-swap bound, which is a different stronger conjecture.

## Overlap and disagreements

`PROVED-HERE`. Opus and Astra give the same inverse construction and exact image criterion. Their use of "towards" or "away" in assigning white-tree edges describes opposite directions of the same endpoint assignment. There is no contradiction. Fable's Proposition 7 adds that a cycle outside the image gives a state with no partner, rather than a partnered cyclic state. Its supplied disk argument closes, as detailed in `INTEGRATION.md`, and the independent tests support it.

`COMPUTED`. Fable's V=16 no-tree factor is a stronger counterexample than Opus's V=40 example. Opus did not claim a complete search for this question through 39, so those sizes are not contradictory minima. Its phrase "first at 40" should mean first found in that particular random search.

`REFUTED`. The unconditional degree-four biconditional and the assertion that original-face terminals always equal lattice extremes are actual disagreements between the mathematical descriptions and the independent checks. They require corrections before integration.

## Bounded reverse-Lamport graph

```text
Cpair <- density route AND(Euler, signed sides, component bounds, integral flow)
Csharp <- dual-cut route AND(Cpair, bond/triangle correspondence, bipartite balance)
Cglue <- induction AND(Cpair, central pair-to-tree input, direct recovery,
                      cap colouring, matching boundary prescription, tree union)
Cimage <- inverse route AND(rooted monochromatic forest, white endpoint uniqueness)
Cdichotomy <- supplied Gamma route AND(white cycle, interior face pairing,
                                     disk Euler count, mate outdegree count)
Clift_iff <- supplied split route AND(lift bijection, split edge formula,
                                    tree-input side test, reverse implication)
Clattice <- orientation route AND(quotient bijection, feasible alpha, Felsner)
Cfacial_extreme <- facial route AND(no flippable original face,
                                  facial/essential-cycle equivalence)
```

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Cpair | Pair iff no black-inner separator | root | density / AND | major claim | Sections D, integration 1–2 | discharged |
| Euler | Exact region identity | Cpair | density / AND | algebraic/logical step | Euler and total colour balance | discharged |
| signed sides | Region bound and triangular signs | Cpair | density / AND | algebraic/logical step | incidence cancellation and parity | discharged |
| component bounds | Constant four survives disconnection | Cpair | density / AND | side condition | separate root component and outer exception | discharged |
| integral flow | Capacity inequality gives two matchings | Cpair | density / AND | named theorem | integral max-flow; exact capacities checked | discharged |
| Csharp | Exact rooted primal cut condition | root | dual-cut / AND | major claim | Section E | discharged |
| bond/triangle correspondence | Nontrivial 3-cuts dualize to separators | Csharp | dual-cut / AND | algebraic/logical step | edge connectivity and plane duality | discharged |
| bipartite balance | Cut endpoints have one colour per shore | Csharp | dual-cut / AND | algebraic/logical step | degree equation | discharged |
| Cglue | Cutting only at obstruction suffices | root | induction / AND | major claim | Section E | discharged relative to named central input |
| central pair-to-tree input | Some pair has rooted-forest second state | Cglue | induction / AND | proved earlier | supplied OpenAI Proposition 5.1 | explicit input |
| direct recovery | A tree matching gives prescribed partition | Cglue | induction / AND | proved earlier | supplied OpenAI Section 6, exact hypothesis checked | explicit input |
| cap colouring | Both pieces remain Eulerian | Cglue | induction / AND | side condition | three equal boundary signs | discharged |
| matching boundary prescription | Labels agree on separator | Cglue | induction / AND | side condition | prescribed same-label cap edge | discharged |
| tree union | Glued classes induce trees | Cglue | induction / AND | algebraic/logical step | connected intersection and no cross-interior edges | discharged |
| Cimage | Inverse and image criterion | root | inverse / AND | major claim | Section H, integration 5 | discharged |
| rooted monochromatic forest | Three rooted components after removing e0 | Cimage | inverse / AND | algebraic/logical step | complement of a dual Hamiltonian cycle | discharged |
| white endpoint uniqueness | Tree endpoint assignment is forced | Cimage | inverse / AND | algebraic/logical step | unique rooted tree orientation | discharged |
| Cdichotomy | A missed cycle's state has no partner | root | Gamma / AND | major claim | integration 5 | discharged |
| white cycle | Non-tree W_s contains an embedded cycle | Cdichotomy | Gamma / AND | algebraic/logical step | n edges on n+1 vertices | discharged |
| interior face pairing | B_i=W_i | Cdichotomy | Gamma / AND | side condition | all crossed faces consumed on Gamma | discharged |
| disk Euler count | Q_s has σ−1 internal edges | Cdichotomy | Gamma / AND | algebraic/logical step | explicit subdivided disk count | discharged |
| mate outdegree count | A mate would require σ internal edges | Cdichotomy | Gamma / AND | definition | one outgoing edge at every interior nonroot | discharged |
| Clift_iff | Full degree-four biconditional | root | split / AND | major claim | Section G | failing |
| lift bijection | Restricted states project and lift uniquely | Clift_iff | split / AND | algebraic/logical step | unused split copy and x | discharged in corrected domain |
| split edge formula | The two new opposite edges are as stated | Clift_iff | split / AND | definition | local face inspection | discharged |
| tree-input side test | A tree input lifts iff the side test holds | Clift_iff | split / AND | algebraic/logical step | split tree has two components | discharged |
| reverse implication | Tree lift forces tree contraction | Clift_iff | split / AND | too strong | independently saved V=11 counterexample | failing |
| Clattice | Feasible alpha-orientations form the lattice | root | orientation / AND | major claim | Section F | discharged |
| quotient bijection | Pair quotient equals deleted-corner maps | Clattice | orientation / AND | definition | explicit maps both ways | discharged |
| feasible alpha | The prescribed orientations exist | Clattice | orientation / AND | side condition | hypothesis of at least one pair | discharged |
| Felsner | Applicable lattice theorem | Clattice | orientation / AND | named theorem | Theorem 1, full source opened | discharged |
| Cfacial_extreme | A facial terminal is a true extreme | root | facial / AND | major claim | saved V=80 description | failing |
| no flippable original face | The author's terminal test holds | Cfacial_extreme | facial / AND | hypothesis | author's facial computation; insufficient even if true | open |
| facial/essential-cycle equivalence | Original faces generate the required order | Cfacial_extreme | facial / AND | missing | saved orientation has both cycle senses | failing |

## Verdict

The Euler criterion, rooted primal condition, sharp gluing, alpha-orientation bijection, and recovery image follow by their supplied routes. The stronger fable dichotomy also follows after its geometric counts are made explicit. The full lift biconditional does not follow from the stated assumptions, as the V=11 counterexample shows. The named V=80 lattice-maximum certificate is false. The broad two-matroid impossibility claim is not established by the supplied evidence. The specific NP-hardness and half-integral-vertex results are safe with the qualifications above.
