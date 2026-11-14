# Reverse-Lamport audit of draft A

## Audit boundary

PROVED-HERE, manuscript route audited after the first complete build. The conclusion C0 is Theorem 1: for every finite simple undirected cubic bipartite planar 3-vertex-connected graph G and every edge e, G has a Hamiltonian cycle avoiding e. The audited source is paper/draft-A/barnette.tex, final hash recorded in build-check.json. No numerical experiment is an accepted premise for C0.

The intermediate contract is Proposition 3: every simple face-bicolored sphere triangulation of order at least four admits two induced trees with any prescribed facial edge within one class and the third corner in the other. The face can have either color. The forest-pair proposition assumes a pair exists and does not exclude separating triangles.

Accepted primitives: Euler's formula for a connected sphere graph and a triangulated disk; Jordan separation and the elementary exit-minus-entrance intersection count; finite graph edge counts and permutation of assignments; existence of a polygonal drawing and generic transverse paths; finite distributivity. The integral flow conclusion is also proved by the residual-path argument, though Ford and Fulkerson are cited. Complementary tree duality is proved in Lemma 2. No form of Barnette's conclusion, no state-to-tree theorem, no trinity theorem and no determinant nonvanishing theorem is accepted as a primitive.

LIT provenance: OpenAI, Sections 2--7 supplies the original route; the Fable note, Sections 1--3 and 5 supplies the height reformulation. Their truth is not inferred from their status labels. The referee report was read through its critical findings and rewritten Proposition 5.1 before this audit. Its corrections relevant to this route are present in the draft.

## Obligation graph

Every route below is an AND route; the paper supplies no alternative proof of the main theorem. The two separator cases are both required, not OR alternatives.

```text
C0 <- R0 dual construction: H0, C1, C2, O1
C1 simple properly face-bicolored dual <- R1: O2, O3, O4, O5
C2 prescribed induced trees <- R2 induction: O6, C3, C4
C3 no-separator case <- R3: O7, C5, C6, C7, C8
C4 separator case <- R4: O8, O9, O10, O11, O12
C5 pair exists without separator <- R5: O13, O14, O15, O16, O17, O18
C6 pair implies forest pair <- R6 signed count: O19, C9, C10, O20
C9 cyclic second states cancel <- R7: O21, O22, O23, C11
C10 signed height sum nonzero <- R8: O24, C12, O25, O26, O27
C11 disk identity <- R9: O28, O29, O30, O31
C12 height increment is enclosure indicator <- R10: O32, O33, O34, O35
C7 forest state gives one side per face <- R11: O36, O37, O38, C13
C8 selected sides are two induced trees <- R12: O39, C11, O40, O41, O42, C13
C13 complementary tree/forest duality <- R13: O43, O44
```

## Critical findings and repairs

PROVED-HERE. No failing obligation remains on this route. These are checks of the manuscript, not a claim that the other papers or every assertion in the research notes is correct.

1. C0 is genuinely the prescribed-edge statement. The induction uses exactly the arbitrary-face prescription of C2, including when the second cap is white. Relabeling colors is explicitly allowed. The final cycle omits e because its dual lies within one class.
2. C1 does not assume that the dual is simple. A primal cut of at most two edges has at least three vertices on each side; deleting its endpoints on one side contradicts 3-connectivity. Dual loops and parallel pairs supply such a cut by a Jordan curve. Cubicity then yields triangular facial walks in a simple dual. An unselected edge crosses the recovered cycle once, so both side classes really are nonempty.
3. O16 is where the no-separator hypothesis is used. A triangular face of a component of order at least four cannot be the wrong side of a nonseparating triangle, since that component has an off-cycle vertex. Actual black faces and component faces are not conflated for components of order three. The root component gets the constant -4; other components need only the weaker bound. Repeated bridge sides and faces containing other components are covered in signed counting.
4. O29 uses all of bijectivity. Every interior vertex has its matched black face inside; each boundary vertex uses the black face of its unique outgoing edge; each black face is matched once. At most one selected edge comes from a black face. The resulting identity W=B+1 is about all faces whose interiors are in the disk, not only faces with strictly interior corners.
5. The reversal of Q_s is chosen from s alone. It changes only r and keeps the test F(s), the cycle selection and disjointness fixed. The local delta calculation is checked in both orders. The disk identity applies to this r-directed Q_s cycle, not only to D cycles. Consequently J changes by exactly two in absolute value.
6. Before defining the minimum m the manuscript assumes at least one pair. The finite cover set is nonempty. Because n=|V(T)|-3>=1, its covers have at least one cycle. The m witness positions may use repeated white faces. The four-term nested example does not assume disjoint disks.
7. The paths are fixed, transverse and finite. Heights are signed integers, not assumed nonnegative or independent of paths. Every counterclockwise exit has positive sign under the center-to-corner crossing convention. Distinct centers make the spoke curve simple; the sector slide proves orientation and white-face containment, including a third corner lying elsewhere on the cycle. The draft retains this step rather than claiming it was removed.
8. The Boolean expansion counts labelled bijections. If c>m no term covers all cycle variables. If c=m every surviving term uses all m factors exactly once. The sign exponents differ by 2m, so every minimum group has common sign. The selected witness group contributes at least one. No preferred orientation of a group is asserted to be a forest state.
9. Recovery is independent of the chosen witness cover. Lemma 4 supplies three rooted components of the surviving Q_s. Joining them through the outer center gives the incidence tree; the faces of that graph are explicitly identified with white triangles. Rooting the complementary white tree supplies exactly one selected side per white face and per black face.
10. The short acyclicity argument proves P_0 first. Because P has one edge per face, distinct boundary selected edges pair distinct boundary faces. The remaining interior face pairs give W-B=3, contrary to W-B=1. Chords contribute internally on both sides. The extra root-component argument, requested by the referee, is then explicitly used to add e_0 without creating a cycle.
11. The two induced trees are obtained only after both acyclicity and degree two have been proved. They are not inferred from connectivity alone. The Jordan curve crosses precisely the unselected edges, so same-class edges are exactly P.
12. The separator pieces decrease in vertex count, inherit simple triangular embeddings, and have at least four vertices. The boundary sign sum forces a valid cap color. The prescribed second piece agrees on two vertices of one class and one of the other, so intersections are one edge or one vertex. There are no cross-interior edges. Connected union and the tree edge count finish the induction.

Editorial corrections found in the audit: defined the disk face counts in the lemma statement rather than first in its proof; stated the polygonal embedding convention before defining path crossings; retained the explicit nonempty-pair and repeated-witness conditions from the referee. The manuscript uses all white faces for the height definition, a harmless extension because the increment proof works for each one. It does not require the note's separate count of inner white faces.

COMPUTED checks are separate. examples.py imports the reference implementation, maps faces by corner sets, recomputes both supplied JSON examples, recomputes the figure octahedron and 13-vertex witness, validates their cycles, and checks the displayed Q reversal, disk counts and four-term identity. These checks support the examples only.

## Dependency table

All mathematical checks below have PROVED-HERE status in this audit and the manuscript; source attributions are LIT as specified above. Classification and discharge are separate from that provenance.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Hamiltonian cycle avoiding arbitrary e | root | R0 | root | C1,C2,O1,H0 | discharged |
| H0 | G finite simple cubic bipartite planar 3-connected, e an edge | C0 | R0 | hypothesis | Theorem 1 | discharged |
| C1 | T is simple, triangular, order >=4, properly face-colored | C0 | R1 | major claim | O2--O5 | discharged |
| C2 | Prescribed induced-tree partition for any facial edge | C0 | R2 | major claim | C3,C4,O6 | discharged |
| C3 | Partition when no separating triangle | C2 | R3 | major claim | O7,C5--C8 | discharged |
| C4 | Partition when a separating triangle exists | C2 | R4 | major claim | O8--O12 | discharged |
| C5 | Existence of a disjoint pair | C3 | R5 | major claim | O13--O18 | discharged |
| C6 | A pair implies a forest pair | C3 | R6 | major claim | C9,C10,O19,O20 | discharged |
| C7 | Forest state gives one side per face | C3 | R11 | major claim | O36--O38,C13 | discharged |
| C8 | Selected sides are two induced trees | C3 | R12 | major claim | O39--O42,C11,C13 | discharged |
| C9 | All cyclic second states cancel | C6 | R7 | major claim | O21--O23,C11 | discharged |
| C10 | Some signed height sum is nonzero | C6 | R8 | major claim | O24--O27,C12 | discharged |
| C11 | W=B+1, h-2l=3, oriented delta sum +/-3 | C9,C12,C8 | R9 | major claim | O28--O31 | discharged |
| C12 | Clockwise-to-counterclockwise height increment equals enclosure indicator | C10 | R10 | major claim | O32--O35 | discharged |
| C13 | Complementary tree/forest duality | C7,C8,O1 | R13 | major claim | O43,O44 | discharged |
| O1 | Two induced trees yield one side per triangle, a connected 2-factor, and omit e | C0 | R0 | algebraic/logical step | Final proof and C13 | discharged |
| O2 | No primal edge cut of size <=2 | C1 | R1 | algebraic/logical step | Cut-side sizes and endpoint deletion | discharged |
| O3 | Dual loop/parallel pair gives forbidden cut | C1 | R1 | named theorem | Jordan separation with one crossing per edge | discharged |
| O4 | Dual facial walks are triangles and dual order >=4 | C1 | R1 | algebraic/logical step | Cubicity, simplicity, Euler | discharged |
| O5 | Primal bipartition properly colors dual faces | C1 | R1 | definition | Dual incidence | discharged |
| O6 | Separator/no-separator cases exhaustive, induction well founded | C2 | R2 | side condition | Vertex count and definition | discharged |
| O7 | Counts n=k-1 and |V|=n+3 | C3 | R3 | algebraic/logical step | Side count and Euler | discharged |
| O8 | Capped pieces simple, order >=4, smaller | C4 | R4 | side condition | Separating triangle has vertices on both sides | discharged |
| O9 | Cap colors extend | C4 | R4 | algebraic/logical step | Three signs with sum divisible by three | discharged |
| O10 | First cap has unique same-class edge | C4 | R4 | algebraic/logical step | A tree cannot contain a triangle | discharged |
| O11 | Second induction call accepts arbitrary cap and edge | C4 | R4 | side condition | Exact Proposition 3 contract | discharged |
| O12 | Glued trees remain induced trees and preserve prescription | C4 | R4 | algebraic/logical step | Connected one-edge/one-vertex intersection; no cross edges | discharged |
| O13 | Flow cut minimum equals displayed capacity | C5 | R5 | algebraic/logical step | Minimize each black-face placement independently | discharged |
| O14 | Full integral flow gives two perfect matchings | C5 | R5 | algebraic/logical step | Residual paths, balanced saturated degrees, alternating cycles | discharged |
| O15 | Flow inequality equivalent to e(U)-b(U)<=2|U|-4 | C5 | R5 | algebraic/logical step | Per-black-face shortfall, outer contribution zero | discharged |
| O16 | Density estimate for components of order >=4 | C5 | R5 | proved earlier | Lemma 5 proof, actual-face test and region imbalance | discharged |
| O17 | Small root component and other small components satisfy required bounds | C5 | R5 | side condition | Root triangle and simplicity | discharged |
| O18 | Summed component bounds give density | C5 | R5 | algebraic/logical step | Edges and actual black faces partition by component | discharged |
| O19 | D covers X by distinct simple odd cycles, epsilon is integral exponent | C6 | R6 | proved earlier | Bijections, unique black edge, C11 | discharged |
| O20 | Nonzero surviving sum implies a forest pair | C6 | R6 | algebraic/logical step | Empty finite sum is zero | discharged |
| O21 | Q_s cycle directed, roots absent | C9 | R7 | algebraic/logical step | Outdegree at most one | discharged |
| O22 | Reversal is fixed-point-free, involutive, preserves s and bijectivity | C9 | R7 | side condition | Cyclic permutation of assignments; selection uses s alone | discharged |
| O23 | Local delta identity changes J by +/-2 | C9 | R7 | algebraic/logical step | Two cyclic orders and C11 on Q cycle | discharged |
| O24 | Pair set finite nonempty, m>=1, witness faces exist | C10 | R8 | side condition | Hypothesis, O7, C11 | discharged |
| O25 | A D group consists of exactly its independent orientations | C10 | R8 | algebraic/logical step | Unique supplying faces and in/out-degree one | discharged |
| O26 | Alternating expansion kills c>m and counts bijections for c=m | C10 | R8 | algebraic/logical step | Sum over supersets of image phi | discharged |
| O27 | Minimum groups have common sign and at least one positive count | C10 | R8 | algebraic/logical step | Parity calculation and chosen witness cover | discharged |
| O28 | Directed state cycle and its bounded disk avoid roots | C11 | R9 | side condition | Zero root outdegree, roots incident with infinity | discharged |
| O29 | B=I+l | C11 | R9 | algebraic/logical step | Interior/boundary matching bijection | discharged |
| O30 | Disk edge counts and Euler apply including chords | C11 | R9 | named theorem | Triangulated closed disk, Jordan and Euler | discharged |
| O31 | Counts yield face excess, boundary excess and odd length | C11 | R9 | algebraic/logical step | Substitution in three counts | discharged |
| O32 | Fixed generic paths define finite signed heights | C12 | R10 | definition | Polygonal transverse paths | discharged |
| O33 | Difference of selected spokes equals detoured cycle | C12 | R10 | algebraic/logical step | Head contribution minus tail contribution | discharged |
| O34 | Detour simple, same orientation and white-face interior | C12 | R10 | side condition | Distinct centers, sectors excluding third corner | discharged |
| O35 | Intersection sum equals inside-start minus inside-end | C12 | R10 | named theorem | Jordan exit/entrance alternation; sign checked | discharged |
| O36 | Partnered forest Q_s has one root per component | C7 | R11 | proved earlier | Lemma 4 outdegree count | discharged |
| O37 | H connected, faces white, H minus deleted spokes a tree | C7 | R11 | algebraic/logical step | Sector description and joined root components | discharged |
| O38 | Rooted white tree assigns exactly one side per face | C7 | R11 | algebraic/logical step | One child per edge, all nonroot whites used once | discharged |
| O39 | P_0 has outdegree one on nonroots; any cycle directed | C8 | R12 | definition | State s supplies tails | discharged |
| O40 | Face pairing at a boundary cycle implies W-B=h-2l=3 | C8 | R12 | algebraic/logical step | Remove boundary pairs; interior pairs and chords cancel | discharged |
| O41 | P_0 forest has three rooted components; e_0 joins two | C8 | R12 | proved earlier | Outdegree count as in Lemma 4 | discharged |
| O42 | Dual Jordan cycle identifies exactly two induced classes | C8 | R12 | named theorem | Jordan crossing parity, two forest components | discharged |
| O43 | Tree contraction preserves faces and leaves connected dual | C13 | R13 | algebraic/logical step | Plane contraction and dual paths | discharged |
| O44 | Complement count is |F|-1; extend forests to trees | C13 | R13 | algebraic/logical step | Euler and spanning-tree extension | discharged |

## Verdict

FOLLOWS. The manuscript's supplied route closes at C0 through C1 and C2. The decisive checks are O16, O23, O26--O27, O34--O35, and O40--O42. The graph is acyclic and all reachable leaves are discharged. This is a bounded mathematical audit of draft A, with human review still pending; it makes no claim about a polynomial-time construction or about auxiliary determinant claims omitted from the paper.
