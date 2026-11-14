# Independent referee report on limits and strengthenings

Referee: gpt-6.1-sol. The source boundary is Astra's `REPORT.md`, `HYPOTHESES.md`, `STRENGTHENINGS.md` and saved examples, together with the relevant supplied paper arguments. I also compared Opus Section 7 and fable Proposition 7. No author code or reference implementation was imported or executed. The independent programs are `code/audit.py`, `code/limits.py` and `code/extras.py`.

The accepted inputs are the definitions, elementary graph counting, sphere tree/cotree duality, the supplied disk identity and direct recovery theorem. Their hypotheses are checked where invoked. An example that breaks the state machinery need not be a counterexample to Hamiltonicity. Published source attributions remain separate from new T2 proofs and finite `COMPUTED` results.

## 1. Injectivity, image and the prism

Exact claim: for fixed t0,e0, the map from tree matchings to Hamiltonian cycles avoiding e0* is injective, but need not be onto. Its image consists of cycles whose recovered tail state is a tree matching.

Proof ledger:

1. `PROVED-HERE`. The complement of a sphere Hamiltonian cycle consists of two induced trees. One direct proof removes an edge from the Hamiltonian cycle to make a spanning tree; its complementary dual is the selected forest plus one edge, so the selected graph is a forest with two components. Jordan labels identify those two components with the induced colour classes.
2. `PROVED-HERE`. Removing e0 splits the tree containing its endpoints. The third root is in the other tree. Thus there are three components with one root each. Orienting towards the roots makes each nonroot a tail once. Unique black-face ownership makes these tails a state.
3. `PROVED-HERE`. The constructor orients the selected side in t out of s(t). The orientation in a rooted forest is forced, so the tail inverse reads s back. This proves forward injectivity.
4. `PROVED-HERE`. If the recovered state is a tree matching, its deleted-spoke dual graph is a white tree. Each selected side assigns a different white face to an incident edge, except at the prescribed white root. The assignment is unique on a tree. This proves sufficiency, not just necessity, for the image criterion.

Verdict: CORRECT. Complete final proofs, including the stronger fable statement, are in `INTEGRATION.md`, Section 5.

`COMPUTED`. Independently enumerating all 1,206 facial roots in the 55 saved graphs through dual order 14 checks 9,720 constructor images with no collisions. Independently enumerating the two induced vertex classes checks 35,664 prescribed partitions and their inverse states. On the saved prism there are three states, two tree matchings, two images and four avoiding cycles. The inverse on the entire set of avoiding cycles is not asserted to be injective. The forward map on tree matchings is injective.

`PROVED-HERE`. Opus and Astra agree exactly. Fable's extra conclusion is compatible and stronger: the state of a missed cycle has no mate at all. Its supplied white-cycle disk argument correctly uses the pairing of crossed faces before claiming equality of the strictly interior face counts. That bridge is essential. I checked the disk Euler count independently and tested the dichotomy on every partition just counted. There is no contradiction between the reports.

## 2. Rarity and the minimum positive count

Exact claim: white-face sums of q rooted hexagonal-prism duals have 3^q states and 2^q tree matchings, of primal order 10q+2. A nonempty tree-matching set never has size one.

Proof ledger for the rarity family:

1. `PROVED-HERE`. Insert a prism disk with its black cap removed into an old white face. Its five new vertices and five new bounded black faces have equal size. No old black face can cover a new vertex, so every new black face must cover a new vertex. Thus the state restricts to a rooted local state, and the old state survives. This proves factorization of all states, not just a lower bound.
2. `PROVED-HERE`, local enumeration `COMPUTED`. In the saved local order, the faces are `(0,5,6),(0,3,4),(2,7,3),(1,6,7),(4,7,5)`, with roots `{0,1,2}`. Their states are `(5,3,7,6,4)`, `(5,4,3,6,7)`, `(6,4,3,7,5)`. Only the first and third are disjoint, and both are tree matchings. This closes the author's explicitly outstanding local check.
3. `PROVED-HERE`. A local tree state's opposite-edge forest has one boundary root per component. Attaching it to the old forest cannot join two old vertices or make a cycle; it attaches a separate tree at each boundary vertex. This proves that all 2^q tuples of local tree states are global tree states.
4. `PROVED-HERE`. Every global tree matching has a mate by the rooted-tree orientation. Both states restrict locally, so their restrictions are disjoint local states. Therefore every local state of a global tree must be one of the two listed tree states. This gives the matching upper bound 2^q.
5. `PROVED-HERE`. Vertex count is 8+5(q−1)=5q+3 in the dual and 2(5q+3)−4=10q+2 in the primal. The success fraction is (2/3)^q. The family is feasible and rare, rather than obstructed.

Verdict: CORRECT. `code/limits.py examples` independently checks q=1,...,6, with state counts 3,9,27,81,243,729 and tree counts 2,4,8,16,32,64. The local enumeration is now recorded as data as well as in the final proof.

Proof ledger for non-uniqueness:

1. Each tree matching has exactly one mate, since its rooted forest has exactly one orientation with outdegree one off the roots.
2. At zero weights, each nonempty unoriented D-cycle group contributes a product of factors `−i+i`, and hence zero.
3. Fixed-second-state cancellation removes every partnered state with a Q-cycle. States without mates contribute nothing. The only terms left are one per tree matching.
4. The disk identity makes every D-cycle odd, so J has the parity of n and the remaining phases are ±i^n. Their sum zero forces equally many of the two signs, in particular at least two if nonempty.

All four steps are `PROVED-HERE`, relative to the supplied disk identity and cancellation argument. The cube has exactly two tree matchings by independent enumeration. Verdict: CORRECT. This is a conditional reuse of the supplied central machinery, not a new proof avoiding it.

## 3. Colouring and cubicity examples

Exact claims: removing bipartiteness can prevent the proper face colouring before states are defined; a maximum-cut substitute does not restore unique black ownership. Removing cubicity can invalidate the Hamiltonian conclusion even with the remaining hypotheses.

`PROVED-HERE`. Proper black/white dual-face colouring is exactly a primal bipartition. At a monochromatic primal edge the dual edge has either two black incident faces or none. Thus neither its unique black owner nor the signed side cancellation survives. K4 is a machinery failure, even though K4 is Hamiltonian. This distinction is correctly made by the report.

`COMPUTED`. An independent binary-label/cut-indicator MILP gives maximum cuts 4,50,60 on the saved K4, BBL38, Tutte46 graphs, respectively, with reported solver gap zero. Thus their 6,57,69 edges leave 2,7,9 monochromatic edges. The saved colouring need not be identical to the author's optimal colouring. It has the same optimum and the required defective edges. This is an independent numerical optimization result, not an exact symbolic MILP proof certificate. No new minimality or non-Hamiltonicity claim about the two large named graphs is certified here.

`PROVED-HERE`, graph properties `COMPUTED`. The saved noncubic 11-vertex radial graph is planar, bipartite and 3-connected, with class sizes five and six. A Hamiltonian cycle alternates the bipartition and cannot exist. In a nontriangular dual face there is no unique edge opposite a selected corner, and selecting one edge per face does not leave dual degree two. The claimed failure point is correct.

Verdict: CORRECT. Global minimality at 38 vertices remains the author's explicitly unverified literature attribution and is not needed for the machinery example. I did not promote it.

## 4. The 26-vertex connectivity example

Exact claim: the theta of three cube-minus-edge branches is cubic, planar, bipartite and exactly 2-connected, non-Hamiltonian, and has eight states but no pairs at every black-root choice after retaining incidence identities in the dual multimap.

Proof ledger:

1. `PROVED-HERE`. Each endpoint of the removed cube edge gains one terminal edge, so all degrees are three. The terminal colours extend a bipartition, and the three branches can be embedded in a planar theta arrangement.
2. `PROVED-HERE`. Deleting one vertex leaves connected branches or alternate terminal connections. Deleting both terminals leaves exactly three components. Thus the graph has connectivity two.
3. `PROVED-HERE`. Removing two vertices from a spanning cycle leaves at most two path components. It cannot span the three surviving branch components. Hence no Hamiltonian cycle exists.
4. `COMPUTED`. Direct face-incidence backtracking using the saved `dual_triangles` gives eight states and zero disjoint pairs at all 26 roots. Every incidence complement is disconnected; each has cycle rank three. Independent perfect-matching-complement enumeration also gives zero Hamiltonian cycles of the primal graph.
5. `PROVED-HERE`. The disk identity's incidence proof still works for a simple directed boundary in this loopless triangular multimap when corners are distinct and the state is bijective. Simplicity fails at the density step: a region can have boundary length two, where the d≥4 bound is unavailable. Thus the first failed existence assertion is pair existence, rather than the disk identity. This claim has the right restricted domain; it does not assert a general multimap recovery theorem.

`COMPUTED`, certificate correction. With the face labels actually saved in `examples/theta_cube_26.json`, the author's named root-zero set S={6,7,8,9,10,11,12,13,14} has deficit two, not three. The data in `non3connected_cut.json` came from a different face indexing or contains a stale label set. Exhaustive subset checking on the saved triangles gives maximum deficit three, attained by

\[
S=\{4,5,6,8,9,10,12,13,14\}.
\]

`code/limits-examples.json` supplies the corrected cut in the example's own labels. Either set is a valid obstruction; the claimed numerical deficit needs this correction.

Verdict: CORRECT AFTER FIX to the capacity-certificate labels. The underlying counterexample and first failure point are CORRECT. No 26-vertex minimality proof is supplied or needed. The cited Asano–Saito–Exoo–Harary minimality attribution stays separate from this check.

`PROVED-HERE`. The report's redundancy statement about simplicity is also correct under its explicit convention: a cubic multigraph on at least four vertices with a loop or parallel pair has a vertex with at most two distinct neighbours. Deleting those neighbours isolates a nonempty remnant, contradicting 3-vertex-connectivity of the underlying adjacency graph. This does not allow non-simple triangulations in the density theorem.

## 5. Torus and topology

Exact claims: the original rooted state sizes fail on genus g>0; the saved torus has no two-induced-tree partition but does have Hamiltonian cycles in its dual; a root-free relaxed pair exists and its Q is necessarily cyclic.

Proof ledger:

1. `PROVED-HERE`. With k faces of each colour on an orientable genus-g surface, E=3k and V=k+2−2g. Removing one black face and three roots gives |A|=k−1 and |X|=k−1−2g. A state bijection cannot exist for g>0. The nonorientable projective-plane mismatch is one by the same Euler count.
2. `PROVED-HERE`. If two vertex classes induced trees, no triangle could be monochromatic. Every triangle would have exactly one same-class edge, giving k such edges in total, since each edge has two face sides. But two trees have V−2=k−2g edges. This is a contradiction whenever g>0. This argument directly establishes the torus partition obstruction without enumeration.
3. `COMPUTED`. The supplied cellular torus faces define V=9,E=27,F=18 and degree six everywhere. Exhaustive partitions in that supplied embedding give no two induced trees. Independent primal perfect-matching-complement enumeration finds 36 Hamiltonian cycles of its 18-vertex dual.
4. `COMPUTED`. First-corner and second-corner assignments of the nine black faces are both bijections of the nine torus vertices and disagree everywhere. Their Q has nine edges on nine vertices, so cannot be a forest. This uses the stated root-free relaxation, not the impossible original rooted state convention.
5. `PROVED-HERE`. A dual complement of a surface spanning tree is connected and has cycle rank 2g. Contracting the primal tree proves connectedness, and Euler gives the rank. Thus one cannot replace sphere tree/cotree duality by tree/tree duality on a torus.
6. `PROVED-HERE`. One selected side per triangle makes the complementary dual 2-regular on any surface. Adding connectedness is exactly the Hamiltonian condition. The report explicitly includes connectedness, avoiding the false implication from cycle rank alone.

Verdict: CORRECT. The torus example refutes the two-tree target, not toroidal Hamiltonicity. A globally proper face colouring is part of the surface hypothesis and does not follow just from even vertex degrees there. The source is careful about this distinction.

## 6. Bijectivity and disk balance

Exact claim: relaxing only the state bijection gives a directed four-cycle of signed sum zero, and the missing state equality is exactly B=I+ell.

`COMPUTED`. From the saved nine-vertex face list and assignment, I checked the directed cycle 1→6→3→2→1 and its four distinct black owners. Its signed sum is zero. Cutting the face adjacency graph along that boundary gives B=W=2, I=1, ell=2 and h=4. Vertex 8 is chosen twice and vertex 7 is unused. All chosen tails are nonroots.

`PROVED-HERE`. Define d=B−I−ell. Substituting B=I+ell+d into B+W=2I+h−2 and 3(B−W)=2ell−h gives

\[
2\ell-h=-3-3d.
\]

The valid state condition sets d=0. The saved assignment has d=−1 and therefore boundary sum zero. This is the exact failed obligation, and the example is valid. Distinct black owners alone do not imply bijective coverage of vertices.

`PROVED-HERE`. Selecting a Q-cycle using s alone makes the fixed-second-state reversal an involution. An unspecified rule depending on r need not be involutive, but no particular r-dependent rule has been refuted. The report correctly says that no smallest counterexample for such an unspecified rule was found.

Verdict: CORRECT. The claimed smallest size is only smallest within the reported tested class, not a new unrestricted minimality theorem.

## 7. Weights and nonvanishing

Exact positive result: strict coherent cycle circulations suffice for the leading-coefficient argument. Zero weights, or equal individual spoke weights, can leave the sum identically zero.

`PROVED-HERE`, cube count `COMPUTED`. The cube has two ordered pairs with J=±1. With all spoke weights zero, Z(x)=i−i=0. Equal spoke weights make every state's weight the same, so multiplying by a common exponential preserves the same cancellation. Thus positive individual spoke values do not imply positive cycle circulation. Conversely reversing all circulation signs need not destroy the common leading phase.

Verdict: CORRECT for those claims.

`REFUTED`. The sentence calling nonvanishing of the signed product-sum over minimal cycle groups the "exact nonvanishing requirement" is too strong. That coefficient being nonzero is sufficient. If it vanishes, a higher coefficient can still survive.

I found and checked an explicit integer-weight V=14 example with c_min=1. Normalizing the common phase i^n gives

\[
Z(x)/i^n=\sum_j c_j e^{jx},\qquad
\sum_jc_j=0,\quad \sum_jj c_j=0,
\]

but the coefficient dictionary c_j is not zero. `code/weights-leading-zero.json` gives the graph, all nonzero spoke weights and that dictionary. The checker aggregates all pairs directly and separately aggregates tree states; the two polynomials agree exactly. Thus the first possible coefficient vanishes although Z is not identically zero. The fix is to call the displayed minimal-cycle coefficient the first potentially nonzero coefficient, or a sufficient nonvanishing test.

Verdict for the paragraph as a whole: CORRECT AFTER FIX.

## 8. Root dependence, gluing and an unpartnered forest

`COMPUTED`. In the saved nine-vertex example, outer face 0 has four states, four ordered pairs and four tree matchings. Outer face 2, in the same black colour class, has four states and no pairs or tree matchings. This is genuine root dependence, not a colour exchange.

`PROVED-HERE`. A separating triangle cuts into two capped simple Eulerian triangulations, each on at least six vertices because minimum degree is four and 3V−6≥2V. Their union has at least 6+6−3=9 vertices. Thus nine is a theoretical lower bound for a separator, attained by the saved example.

`PROVED-HERE`. Gluing must prescribe the same-label cap edge in the second piece. With that agreement, the corresponding trees meet in one vertex or one edge, and inducedness survives. This is the same correct gluing argument as Opus. The independent checker verifies all 3,618 root-edge prescriptions through V=14 using only black-inner cuts.

`COMPUTED`. All three prism states have Q acyclic, but one has a component with two roots and a component with no root. It has no mate. This is a valid refutation of "an acyclic Q for an arbitrary state is enough". The shared papers' "forest pair" includes a partner, so it is not refuted.

`PROVED-HERE`. For a partnered state, a tree component with v vertices and a roots has v−a outgoing edges and v−1 edges. Therefore a=1. This is the missing implication without the mate.

Verdict: CORRECT. The root counts for all small inputs are independently available in `code/census.json`. The particular 12-vertex root-count table was not used as a theorem; it is consistent with the independently recalculated full census.

## 9. Strengthening tables and P5

Exact finite claims: every graph in the 55-input corpus, of primal order at most 24, has a Hamiltonian cycle using any given edge and avoiding any other edge; every three-edge path lies on a Hamiltonian cycle; every opposite-colour endpoint pair has a Hamiltonian path.

`COMPUTED`. I independently enumerated all perfect matchings of every saved primal graph and retained exactly those with connected complements. The resulting Hamiltonian-cycle counts agree with every row of `data/strengthenings.json`. For every ordered edge pair and every simple three-edge path I tested membership against that complete cycle list. I separately tested every opposite-colour endpoint pair by exact bitmask DFS with memoization. All failure lists are empty in `code/strengthenings.json`. This reproduces the tables on their full stated corpus. It does not certify the independently ungenerated census is exhaustive on all isomorphism classes.

`PROVED-HERE`. Single-edge avoidance in a cubic graph implies a cycle containing any prescribed two-edge path: avoid the third edge at the middle vertex. It also implies a cycle containing any given edge. Deleting that edge gives a Hamiltonian path between its adjacent endpoints. A spanning path in a balanced bipartite graph has opposite-colour endpoints, so same-colour Hamiltonian-connectedness is impossible.

`LIT`. I opened the primary source Gorsky, Steiner and Wiederrecht, *Matching Theory and Barnette's Conjecture*, arXiv:2202.11641v3, Theorems 4.4 and 4.16, [full HTML](https://arxiv.org/html/2202.11641v3). The indicated equivalence really includes P4-Hamiltonicity for cubic 3-connected Pfaffian bipartite graphs. Thus applying the supplied existence theorem yields the reported P4 consequence. This is distinct from a direct local recovery construction for a prescribed three-edge path.

`CONJECTURE`. The arbitrary include-one/avoid-another and Hamilton-laceability statements remain general hypotheses in these reports. Their global current status is not decided by the finite table. The cofacial Kelmans attribution is explicitly just a literature lead in Astra's text. I do not treat it as an opened primary proof, nor use it to settle arbitrary edge pairs.

`PROVED-HERE`, witness `COMPUTED`. P5-Hamiltonicity fails on the saved cube. The path is 0−3−2−7−6. Vertex 5 has neighbours 3,4,7. The path already fixes two incident cycle edges at 3 and at 7, leaving 5 with only neighbour 4 available in a purported containing cycle. That is impossible. Independent enumeration gives all six cube Hamiltonian cycles and none contains the path. The cube is the smallest Barnette graph by the dual minimum-degree bound, so the stated minimal Barnette witness claim follows.

Verdict: CORRECT, with the finite/global and direct-constructor/published-equivalence qualifications retained.

## Bounded reverse-Lamport graph

```text
Cimage <- inverse route AND(two-tree complement, three-root orientation,
                           white-tree endpoint uniqueness)
Crare <- product route AND(local enumeration, equal-size disk saturation,
                          rooted-forest attachment, unique-mate restriction)
Chyp <- examples route AND(saved graph properties, exact failed obligation)
Ctorus <- counting route AND(cellular Euler count, one side per triangle)
Cweights_exact <- coefficient route AND(nonzero first coefficient,
                                      necessity of the coefficient test)
Ctables <- enumeration route AND(all perfect matchings enumerated,
                                cubic cycle-complement equivalence,
                                all endpoint searches complete)
CP5 <- forced-degree route AND(saved cube adjacency, internal path saturation)
```

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Cimage | Injectivity and exact image | root | inverse / AND | major claim | Section 1 and integration 5 | discharged |
| two-tree complement | Avoiding cycle leaves two induced trees | Cimage | inverse / AND | named theorem | sphere duality plus Jordan labels | discharged |
| three-root orientation | Tails form a state | Cimage | inverse / AND | algebraic/logical step | one root per component after e0 removal | discharged |
| white-tree endpoint uniqueness | A tree recovered state reconstructs the cycle | Cimage | inverse / AND | algebraic/logical step | unique assignment on rooted white tree | discharged |
| Crare | Exactly 3^q states, 2^q trees | root | product / AND | major claim | Section 2 and integration 6 | discharged |
| local enumeration | Three local states, only two tree/paired states | Crare | product / AND | proved earlier | independent five-row enumeration | discharged |
| equal-size disk saturation | States and pairs factor | Crare | product / AND | algebraic/logical step | new faces must cover all new vertices | discharged |
| rooted-forest attachment | Every tuple of tree states glues to a tree state | Crare | product / AND | side condition | one boundary root per local component | discharged |
| unique-mate restriction | No additional tree states exist | Crare | product / AND | proved earlier | rooted tree orientation yields a mate | discharged |
| Chyp | Saved failures isolate the named hypotheses | root | examples / AND | major claim | Sections 3–6 | discharged with cut-label fix |
| saved graph properties | Explicit adjacency has asserted structure | Chyp | examples / AND | side condition | independent property and incidence checks | discharged |
| exact failed obligation | A failure occurs at the asserted step | Chyp | examples / AND | algebraic/logical step | ownership, balance, density or cardinality as specified | discharged |
| Ctorus | Original states and two-tree target fail | root | counting / AND | major claim | Section 5 | discharged |
| cellular Euler count | V=k+2−2g | Ctorus | counting / AND | algebraic/logical step | proper face colouring, triangulation, cellular embedding | discharged |
| one side per triangle | Two induced trees would have k edges | Ctorus | counting / AND | algebraic/logical step | no monochromatic triangle and two incidences per edge | discharged |
| Cweights_exact | First minimal-cycle coefficient is an iff test | root | coefficient / AND | major claim | Section 7 | failing |
| nonzero first coefficient | Nonzero coefficient proves Z nonzero | Cweights_exact | coefficient / AND | algebraic/logical step | finite analytic sum | discharged as sufficient test |
| necessity of the coefficient test | If it vanishes then Z is zero | Cweights_exact | coefficient / AND | too strong | independent V=14 polynomial counterexample | failing |
| Ctables | Three finite strengthening tables are correct | root | enumeration / AND | major claim | Section 9, independent output | discharged on saved corpus |
| all perfect matchings enumerated | No cubic cycle complement is missed | Ctables | enumeration / AND | definition | recursive pairing of first remaining vertex | discharged |
| cubic cycle-complement equivalence | Connected matching complement is Hamiltonian | Ctables | enumeration / AND | algebraic/logical step | residual degree exactly two | discharged |
| all endpoint searches complete | Every endpoint row is decided | Ctables | enumeration / AND | algebraic/logical step | finite exact DFS over remaining-vertex masks | discharged |
| CP5 | Cube has a forbidden prescribed P5 | root | forced-degree / AND | major claim | Section 9 | discharged |
| saved cube adjacency | Vertex 5 has neighbours 3,4,7 | CP5 | forced-degree / AND | definition | supplied edges independently read | discharged |
| internal path saturation | 3 and 7 cannot accept edge to 5 | CP5 | forced-degree / AND | algebraic/logical step | two prescribed cycle edges at each vertex | discharged |

## Verdict

The recovery, rarity, non-uniqueness, hypothesis examples, torus obstruction and finite strengthening tables are correct. The root-zero deficient-set certificate needs its face labels corrected if it is presented beside the saved theta example. The proposed exact arbitrary-weight nonvanishing criterion is false and must be weakened to a sufficient test. No finite table here establishes an unproved global strengthening or a new minimality assertion about the large named counterexamples.
