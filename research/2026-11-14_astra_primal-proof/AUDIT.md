# Reverse-Lamport self-audit of the primal proof

PROVED-HERE. This is the author's bounded dependency audit, not independent referee approval. It audits PRIMAL-PROOF.md, Lemmas 1 through 13 and Theorem T. The worked examples and the numerical checker are not premises.

## Audit boundary

Conclusion C0: for every finite simple cubic bipartite 3-edge-connected plane graph G and every edge e, there is a perfect matching P containing e whose complement is connected. The final corollary replaces plane by planar and 3-edge-connected by 3-vertex-connected and concludes a Hamiltonian cycle avoiding e.

The root is the black endpoint of the prescribed edge, R is the set of its three incident faces, A the other black vertices, X the other faces, and a state is a bijection A to X through incidences. There is no assumption that a pair exists until Lemma 4 is applied in the irreducible case. No induction hypothesis is applied to a graph of the same order.

Accepted primitives are finite graph and vector-space definitions, elementary finite counting and polynomial algebra, strong induction, integral max-flow/min-cut for finite integral-capacity networks, and the plane-embedding calculus explicitly listed in Section 2: facial boundary walks and cyclic orders, Euler's formula, edge deletion merging two distinct incident faces, contraction of a nonloop edge, and the boundary-walk criterion for a cut vertex. Cycle-space dimension and cycle/cut orthogonality are elementary linear algebra, with the needed path-sum explanation written in Lemma 2. No Hamiltonicity theorem, two-induced-tree equivalence, Jordan labelling theorem, detour isotopy, or unproved structural-report theorem is accepted as a primitive.

The Lean declarations are provenance and a cross-check of statements. They are not used to waive a missing informal proof. The conversion from face labels to the hypotheses of those declarations is carried by Lemmas 2 and 3.

## Obligation graph

All displayed routes are primary. There are no supplied OR alternatives. The irreducible/reducible split is an AND of exhaustive cases, not a choice between proofs of different scopes.

```text
C0 prescribed-edge matching
 <- R0 strong induction AND H, EX, C1, C2

C1 irreducible case
 <- R1 construction AND C3, C4, C5
C2 reducible case
 <- R2 cap and splice AND C6, DEC, IH, SYNC, GLUE

C3 a pair exists
 <- R3 capacity criterion AND BAL, FLOW, DEFICIT, NONTRIVIAL, IRR
C4 a pair with circuit-free Q exists
 <- R4 two polynomial expansions AND C3, C7, C8
C5 recover the required matching
 <- R5 recovery AND C9, C10, C11

C7 cancellation over a fixed second state
 <- R6 reverse a Q circuit AND TAILS, FIXED, ODD, SIGNFLIP
C8 nonzero lowest coefficient
 <- R7 group by D AND COVER, ORIENTATIONS, EXACT3, C12, MINIMUM
C9 recovery tree exists
 <- R8 delete augmented Q AND ROOTCOUNT, CUTTEST, EDGECOUNT
C10 matching in that tree
 <- R9 white parent edges AND BLACKDEGREES, PARENT, ROOTEDGE
C11 complement connected
 <- R10 exclude a matching-supported bond AND TAILS, C13, C14,
        ROOTCOUNT, CUTTEST
C12 positive slopes
 <- R11 flux AND FLOWCHARGE, POTENTIAL, ORIENTCUT, WHITEPOS
C13 state cut identity h=2ell+3
 <- R12 four counts AND CUBICCOUNT, COLOURCOUNT, EULERREGION, STATECOUNT
C14 matching cut identity h=2ell
 <- R13 subtract two counts AND MATCHINGCOUNT, COLOURCOUNT
C6 caps preserve hypotheses
 <- R14 cut analysis AND SHORECONNECTED, MONOCHROME, DISTINCTENDS,
        CAPPLANE, CAPCUTS

STATECOUNT <- AND BIJECTION, MIXED, ROOTFREE
EULERREGION <- AND SHORECONNECTED, MERGE, EULER
ORIENTCUT <- AND FACEBOUNDARYSPAN, REALORTHOGONALITY, SHORECONNECTED
CUTTEST, SHORECONNECTED, ROOTFREE <- Lemma 2
FACEBOUNDARYSPAN <- AND EULER, FACECONNECTED, BOUNDARYDEPENDENCES
BAL, BLACKDEGREES, EDGECOUNT <- Lemma 1 and the definitions

Cfinal Hamiltonian corollary
 <- R15 AND C0, VERTEXTOEDGE, DEGREETWO
```

## Critical findings and checked boundaries

1. The root charge is attached to a vertex, not to a primal face. The proof consistently sends flow from the root black vertex to white vertices. Calling these white faces would silently switch representation. The statement of Lemma 6 and the stored examples fix this.

2. Face circuits do retain dual incidence data. This is disclosed in the proof and comparison. There is no unproved bridge from a triangulation's “inside” to a vertex set: Lemma 2 proves the bond correspondence, connected shores, root-face exclusion and the region Euler count directly. Lemma 1's forward reference to the general circuit assertion of Lemma 2 is not circular. That assertion uses only a connected plane embedding and facial boundary spaces, not distinct face labels at cubic vertices.

3. Both shores must be connected for the region count. This is supplied by minimality of the cut. The checker also tests the equation on arbitrary small bonds, but those tests are not the justification. The face-deletion proof explains precisely why the incident faces merge to one.

4. Li's omitted balance is supplied by Euler. The proof of the deficit lemma does not use Li's assertion that a connected union of facial cycles is 2-connected. Connectedness alone suffices for Euler. After excluding white vertices incident with exactly one chosen face, it proves that the subgraph is induced and its boundary has only black inner endpoints. The outside shore has both the black root and a white cut endpoint, so the cut is nontrivial. No unfounded assumption that the prescribed white neighbour is outside is needed.

5. The cyclic Q chosen for cancellation must depend on s alone. Section 6 fixes this rule before examining r. Reversing the tails preserves the face set and produces a bijection with no fixed point. Oddness supplies sign reversal. In contrast, nonvanishing needs the exact value three to align all minimal groups. The proof states these different uses explicitly.

6. The local weights can be negative. Positivity is asserted only for the circuit slope, not for the individual polynomial coefficients or factors. The example has negative higher coefficients. Taking a least degree works because the pair set is finite and nonempty, and every circuit factor has a strictly positive linear coefficient after choosing the positive orientation.

7. A forest Q without a partner would be insufficient. Lemma 9 retains the pair and uses its orientation to prove exactly one root per component. The isolated-root case is included. The analogous root count after selected-edge acyclicity is what permits e0 to be added without a circuit. Without this count, the last connectivity argument would have a gap.

8. The induction hypothesis keeps the prescribed-edge quantifier. Each cap is smaller and retains 3-edge-connectivity, simplicity, bipartiteness, cubicity and planarity. In the boundary-edge case the edge omitted by the first cap cycle is the original prescribed edge itself. The second induction call therefore supplies exactly the synchronization needed for splicing.

9. The exact informal proof is not machine-checked. Its real-sign prefactor and Li-style deficit argument differ from the Lean implementation. Both are proved here. The checked development supports the underlying statements; it does not turn an unaudited rewrite into a formal proof automatically.

## Dependency table

The table merges obligations only when their statement and scope agree. A reference to a lemma points to its full proof in PRIMAL-PROOF.md, not to its status label.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Prescribed-edge matching with connected complement | root | R0 | root | Strong induction, C1 and C2 | discharged |
| H | Finite simple cubic bipartite 3-edge-connected plane G | C0 | R0 / AND | hypothesis | Theorem T | discharged |
| EX | Either all 3-cuts are trivial or some is nontrivial | C0 | R0 / AND | algebraic/logical step | Finite case split | discharged |
| C1 | The theorem in the irreducible case | C0 | R1 | major claim | Lemmas 4 through 12 | discharged |
| C2 | The theorem in the reducible case | C0 | R2 | major claim | Lemma 13 and induction | discharged |
| C3 | A pair exists under the irreducibility assumption | C1,C4 | R3 | major claim | Lemma 4 | discharged |
| BAL | Incidence parts both have size n | C3,C9 | R3 / AND | proved earlier | Lemma 1 | discharged |
| FLOW | Capacity criterion yields two disjoint matchings | C3 | R3 / AND | named theorem | Integral max-flow with capacities 2,1,2; alternating even cycles | discharged |
| DEFICIT | Minimal deficient face set yields c=3 | C3 | R3 / AND | proved earlier | Lemma 4: W1 empty, K induced, d=4-2k-c/3 | discharged |
| NONTRIVIAL | Both shores of that cut have at least two vertices | C3 | R3 / AND | side condition | Facial cycle inside; black root and white endpoint outside | discharged |
| IRR | Such a cut is excluded in this case | C3 | R3 / AND | hypothesis | Case assumption of C1 | discharged |
| C4 | A pair with circuit-free Q exists | C1 | R4 | major claim | Lemmas 7 and 8 | discharged |
| C7 | All cyclic second states cancel | C4 | R6 | major claim | Lemma 7 | discharged |
| TAILS | Distinct nonroot tails force any circuit to be directed | C7,C11 | R6,R10 / AND | algebraic/logical step | h edges have h distinct tails on h faces | discharged |
| FIXED | The chosen Q circuit is independent of partner | C7 | R6 / AND | definition | Fixed order on edge subsets, depending only on s | discharged |
| ODD | The chosen directed state circuit has odd length | C7 | R6 / AND | proved earlier | Lemma 5 | discharged |
| SIGNFLIP | The involution preserves states and changes sign | C7 | R6 / AND | algebraic/logical step | Tail/head permutation, odd number of local sign changes | discharged |
| C8 | The polynomial has a nonzero lowest coefficient | C4 | R7 | major claim | Lemma 8, equation (6.4) | discharged |
| COVER | D is a disjoint union of simple circuits covering X | C8 | R7 / AND | algebraic/logical step | Both states bijective; no repeated primal edge or 2-link circuit | discharged |
| ORIENTATIONS | A fixed undirected D has exactly its 2^c orientations as pairs | C8 | R7 / AND | algebraic/logical step | Every black vertex labels one edge; heads and tails remain bijections | discharged |
| EXACT3 | Positive orientation has delta-sum -3 | C8 | R7 / AND | proved earlier | Lemmas 3 and 5 | discharged |
| MINIMUM | Least c exists and every minimal group has a common nonzero sign | C8 | R7 / AND | side condition | C3, finiteness, equation (6.3), positive slopes | discharged |
| C12 | Circuit slopes are strictly positive in the positive orientation | C8 | R11 | major claim | Lemma 6 | discharged |
| FLOWCHARGE | A flow has root supply and unit white demands | C12 | R11 / AND | algebraic/logical step | Sum one chosen root-to-white path per white vertex | discharged |
| POTENTIAL | The three local difference equations are consistent | C12 | R11 / AND | side condition | Zero divergence at every nonroot black vertex | discharged |
| ORIENTCUT | All oriented crossing signs agree with one signed cut indicator | C12,C13 | R11 / AND | proved earlier | Lemma 3 | discharged |
| WHITEPOS | The cut side contains at least one white vertex | C12 | R11 / AND | proved earlier | Lemma 5, W=B+1 | discharged |
| C13 | A directed state circuit has h=2ell+3 | C11,ODD,EXACT3 | R12 | major claim | Lemma 5 | discharged |
| CUBICCOUNT | 3|S|+h=2|E_S| | C13 | R12 / AND | algebraic/logical step | Endpoint count | discharged |
| COLOURCOUNT | 3(b-w)=2ell-h and the second four-count equation | C13,C14,C6 | R12,R13,R14 / AND | algebraic/logical step | Each edge has one end in each colour | discharged |
| EULERREGION | |S|+|U|=|E_S|+1 for connected complementary shores | C13 | R12 / AND | proved earlier | Lemma 2(b) | discharged |
| STATECOUNT | U is state image union circuit faces, intersection of size ell | C13 | R12 / AND | proved earlier | Lemma 5, full inclusion-exclusion argument | discharged |
| BIJECTION | Every nonroot face has one black state partner | STATECOUNT | AND | definition | State | discharged |
| MIXED | A mixed face lies on the cut circuit | STATECOUNT,ROOTFREE | AND | proved earlier | Lemma 2: traverse its boundary | discharged |
| ROOTFREE | No root face meets the root-free shore of a root-avoiding circuit | STATECOUNT | AND | proved earlier | Lemma 2(a), using MIXED | discharged |
| C5 | Recover a perfect matching containing e0 with connected complement | C1 | R5 | major claim | Lemmas 9 through 12 | discharged |
| C9 | Deleted augmented Q has a spanning-tree complement in G | C5 | R8 | major claim | Lemma 9 | discharged |
| ROOTCOUNT | An oriented face-link forest with these outdegrees has one root per component | C9,C11 | R8,R10 / AND | algebraic/logical step | v-k=v-1; applies separately to Q and selected links | discharged |
| CUTTEST | A disconnected complement forces a face circuit in the deleted set | C9,C11 | R8,R10 / AND | proved earlier | Lemma 2, take an inclusion-minimal cut | discharged |
| EDGECOUNT | The connected recovery graph has |V|-1 edges | C9 | R8 / AND | algebraic/logical step | 3(n+1)-(n+2)=2n+1 | discharged |
| C10 | White parent edges give a perfect matching containing e0 | C5 | R9 | major claim | Lemma 10 | discharged |
| BLACKDEGREES | Root black degree one; other black degrees two | C10 | R9 / AND | proved earlier | Lemma 9, distinct black endpoints of removed edges | discharged |
| PARENT | Exactly one white child selects each nonroot black vertex | C10 | R9 / AND | algebraic/logical step | Rooted tree and BLACKDEGREES | discharged |
| ROOTEDGE | The root's unique edge is e0 and is selected by w0 | C10 | R9 / AND | definition | Recovery tree and parent selection | discharged |
| C11 | The selected matching's complement is connected | C5 | R10 | major claim | Lemma 12 | discharged |
| C14 | A matching-supported cut satisfies h=2ell | C11 | R13 | major claim | Lemma 11 | discharged |
| MATCHINGCOUNT | b=p+ell and w=p+h-ell | C14 | R13 / AND | algebraic/logical step | Perfect matching and all boundary edges selected | discharged |
| C6 | Both caps preserve the working hypotheses | C2 | R14 | major claim | Lemma 13 | discharged |
| SHORECONNECTED | A bond, and in particular a 3-cut here, has connected shores | C6,EULERREGION,ORIENTCUT | AND | proved earlier | Lemma 2; Lemma 13 also gives the direct 3-cut count | discharged |
| MONOCHROME | Each side's three cut endpoints have one colour | C6 | R14 / AND | algebraic/logical step | 2ell-3 divisible by three | discharged |
| DISTINCTENDS | The three cut endpoints on a nontrivial shore are distinct | C6 | R14 / AND | algebraic/logical step | Repeated endpoint would leave a cut of size at most two | discharged |
| CAPPLANE | Contracting a connected shore and deleting loops preserves planarity | C6 | R14 / AND | named theorem | Accepted elementary plane contraction calculus | discharged |
| CAPCUTS | Every cap cut lifts to a cut of the same size | C6 | R14 / AND | algebraic/logical step | Put the whole contracted shore with its cap vertex | discharged |
| DEC | Each cap has strictly fewer vertices | C2 | R2 / AND | side condition | Each removed shore has at least two vertices | discharged |
| IH | The prescribed-edge theorem holds on each smaller cap | C2 | R2 / AND | hypothesis | Strong induction, C6 and DEC check applicability | discharged |
| SYNC | The same boundary edge can be omitted in both caps | C2 | R2 / AND | algebraic/logical step | Choose first cycle, prescribe its unused cap edge in second | discharged |
| GLUE | Two spanning paths with synchronized endpoints form one spanning cycle | C2 | R2 / AND | algebraic/logical step | Two disjoint shores and their two used joining edges | discharged |
| MERGE | Deleting connected S merges exactly its incident faces | EULERREGION | AND | algebraic/logical step | Connected sequence of local star-sector mergers | discharged |
| EULER | Euler formula for every connected embedded graph used | BAL,EULERREGION,FACEBOUNDARYSPAN | AND | named theorem | Accepted plane background, connectedness checked | discharged |
| FACECONNECTED | Faces are connected by successive shared-edge incidences | FACEBOUNDARYSPAN | AND | algebraic/logical step | Spanning-tree contraction, then loop deletions | discharged |
| BOUNDARYDEPENDENCES | All facial-boundary linear dependences have equal coefficients | FACEBOUNDARYSPAN | AND | algebraic/logical step | Compare the two coefficients at each edge | discharged |
| FACEBOUNDARYSPAN | Facial boundaries span the cycle space over F2 and R | CUTTEST,ORIENTCUT | AND | algebraic/logical step | Rank F-1=E-V+1 and boundary vectors are cycles | discharged |
| REALORTHOGONALITY | Orthogonal-to-cycles edge vectors are vertex gradients | ORIENTCUT | AND | algebraic/logical step | Path sums from a base vertex | discharged |
| Cfinal | Original Barnette conclusion, with prescribed edge avoidance | root corollary | R15 | major claim | End of Section 8 | discharged |
| VERTEXTOEDGE | Simple cubic 3-vertex-connected implies 3-edge-connected | Cfinal | R15 / AND | proved earlier | Small-shore bound and deletion of at most two endpoints | discharged |
| DEGREETWO | Connected complement of a perfect matching in cubic G is one spanning cycle | Cfinal | R15 / AND | algebraic/logical step | Every vertex has degree two, follow the finite connected component | discharged |

## Verdict

FOLLOWS, relative to the explicitly accepted elementary plane-embedding facts and integral max-flow. C0 closes through both required induction cases C1 and C2. The decisive dependencies are C13, the four-count identity; C12, the flow slope; C8, the common lowest coefficient; C11, direct connectivity; and C6 plus SYNC, the capped induction. This is a self-audit of an informal proof. It neither replaces independent review nor certifies a new Lean formalisation.
