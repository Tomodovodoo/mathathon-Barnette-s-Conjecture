# Referee of the sign-free note

## Audit boundary

PROVED-HERE. This is a conclusion-first audit of `proofs/sign-free/sign-free.tex`, as received on 14 November 2026. I read the source, all eleven PDF pages, the author's self-audit, the earlier topology and rainbow referee reports, and the reconciliation table. I checked the arguments myself. Earlier reports were context and comparison, not substitutes for proofs. I wrote `check.py` and `regions.py` without importing the author's code or the lab. No subagents were used.

The domain is a simple sphere triangulation with properly black/white coloured faces and a distinguished black facial triangle. Its three vertices are roots, `n=|X|=|A|`, and `n>=3`. All graphs and sets are finite. The audit accepts Euler's formula including its disconnected form, Jordan separation for a simple cycle, elementary graph and matching facts, graphic matroid rank, and tree/cotree duality. The three less elementary named theorems are checked below. The good-pair lemma, Theorem 1.1, is a cited result, not a proof offered by this note. Step X remains outside the proved conclusions.

## Verified literature and applications

LIT. Schrijver, *A Course in Combinatorial Optimization*, version 23 March 2017, [official PDF](https://homepages.cwi.nl/~lex/files/dict.pdf), printed pp. 188-189, Exercises 10.26, 10.28 and 10.29. I opened these pages independently. Originals Rado 1942 and Nash-Williams 1964 were not opened.

For a finite matroid and subsets `C_1,...,C_m` of its ground set, an independent transversal exists iff every union of `j` sets has rank at least `j`, for every `j>=0`. This is exactly Exercise 10.26, including distinct representatives.

A finite loopless multigraph's edges partition into `k` forests iff every nonempty vertex set `Z` spans at most `k(|Z|-1)` edges. Exercise 10.29 states the graph version. The multigraph extension follows from Exercise 10.28 applied to its cycle matroid. For an edge subset, sum the vertex inequalities over its nontrivial components to get `|D|<=k rank(D)`. Conversely apply that rank inequality to every induced edge set. Parallel edges remain distinct elements; a parallel pair is a cycle.

LIT. Schrijver, *Polyhedral combinatorics*, Chapter 30 of *Handbook of Combinatorics*, edited by R. L. Graham, M. Grotschel and L. Lovasz, Elsevier, 1995, pp. 1649-1704. [CWI catalog](https://ir.cwi.nl/pub/2216) verifies year and page range; the [chapter PDF](https://ir.cwi.nl/pub/2216/2216D.pdf) title page verifies chapter, editors, year and publisher. Application 5.6, p. 1674, defines rooted arborescences and incoming rooted cuts. The paragraph crossing pp. 1685-1686 states that the minimum size of a rooted cut equals the maximum number of pairwise disjoint rooted arborescences. Arborescences here are spanning out-trees, and disjoint means arc-disjoint. Reverse arcs for the note's in-trees and outgoing cuts. Parallel arcs are distinct; loops can be deleted. The bibliography on p. 1699 confirms Edmonds, *Edge-disjoint branchings*, in Rustin's *Combinatorial Algorithms*, Academic Press, New York, 1973, pp. 91-96. I did not open that original.

PROVED-HERE. Every application meets its hypotheses:

| Use | Matroid or graph | Conditions checked |
| --- | --- | --- |
| Rado, Step R | cycle matroid of connected W; n disjoint classes C_x | W has n+1 vertices; rank n; classes indexed by X; rank of their union is w(J)-comp(T[J]); connected components share no white face |
| Rado, Corollary 6.10 | restriction of cycle matroid of W to a cover | n disjoint two-element face classes; two-forest partition implies rank of any j classes is at least j |
| Nash-Williams, Theorem 6.5 | M_u, with doubled spokes | loopless; all vertex sets treated, including sets of centres only; density gives the required inequality; exactly 2(|V(H)|-1) edges |
| Nash-Williams, Theorem 6.8 | selected sides after contracting roots | no selected side joins two roots, so no loops; both cases of a vertex subset checked; n+1 vertices, 2n edges |
| Edmonds, Theorem 6.9 | G_u with roots merged | outdegree two at each nonroot, zero at root; all nonempty Y subset X have outgoing cut size at least two; directed-tree count n per tree exhausts all 2n arcs |

No use asks a two-matroid theorem to enforce three independent conditions. The note stops precisely where those conditions must be combined.

## Obligation graph

PROVED-HERE. Each displayed route is the sole proof-supplied route and is an AND group. There are no alternative routes to rescue a failing branch. `B0` denotes the domain above. `N1`, `N2`, `N3` denote respectively the verified Rado, Nash-Williams and Edmonds implications. Terminal obligations are classified in the dependency table. Major claims use the PDF numbering.

```text
C21  duality, Lemma 2.1 <- R21 AND B0,O1,O2
C23  good iff excess zero, Lemma 2.3 <- R23 AND O3,O4
C31  Step R, Theorem 3.1 <- R31 AND C21,N1,O5,O6,O7,O8,O9
C41  orientation, Lemma 4.1 <- R41 AND O10,O11
C42a unique cover, Theorem 4.2(1) <- R42a AND C41,O12,O13
C42b forest description, Theorem 4.2(2) <- R42b AND C41,O14
C42c second cover iff cycle, Theorem 4.2(3) <- R42c AND O15,O16,C42b
C43  pair criterion, Corollary 4.3 <- R43 AND C31,C42a,O17
C51  exchange, Lemma 5.1 <- R51 AND O18
C52  reversal, Lemma 5.2 <- R52 AND C51,O19
C53  evenness, Theorem 5.3 <- R53 AND C23,C51,C52,O20,O21,O22,O23
C61  shortfall identity (6.1) <- R61 AND O24
C62  Euler identity, Lemma 6.2 <- R62 AND O25,O26
C63  density, Lemma 6.3 <- R63 AND C62,O27,O28,O29
C65  two W trees, Theorem 6.5 <- R65 AND C21,C61,C63,N2,O30,O31,O32
C67  necessity, Remark 6.7 <- R67 AND C62,O33
C68  two rooted forests, Theorem 6.8 <- R68 AND C61,C63,N2,O34,O35,O36
C69  two rainbow trees, Theorem 6.9 <- R69 AND C41,C61,C63,N3,O37,O38
C610 conditions alone, Corollary 6.10 <- R610 AND C65,C69,N1,O39
C71  sixteen-vertex witness, Proposition 7.1 <- R71 AND O40
CX1  Step X for one cover <- RX1 AND C42c,C51,O41
CX2  Step X implies good-pair lemma <- RX2 AND C31,C23,C43
```

## Checks at the delicate steps

PROVED-HERE. In Step R the nonempty connected set J lies in a single face Phi of T[U]. A face of T with its corners in U cannot contain J, since its open interior has no vertex of T. Thus it is not Phi, and the counts of the other faces are exact even when U is disconnected. The root component borders Phi and contains the root triangle. A boundary of length at most two in a simple graph would consist of an isolated vertex or a bridge traversed twice, not the whole boundary of this non-tree component. Hence d>=3. The sign table must use both divisibility by three and parity: d=4 forces varsigma=0, d=5 permits at most 3, d>=6 uses varsigma<=d. At d=3, negativity forces varsigma=3. If the far side has no vertex, its boundary is the root face itself, and its neighbouring inner faces are white, contradicting varsigma=3. This discharges the late outer-face fix. In the converse, the interior may be treated without assuming it connected: w(J)<=|J| already forces rank below |J| for every nonempty J.

PROVED-HERE. The density component sum is sound. All roots present in U lie in the same induced component because they are pairwise adjacent. Consequently the sum of the root penalties over components equals the single global penalty. Summing the individual bounds yields `e(U)-b(U)+max(0,rho(U)-1)<=2|U|-2c<=2|U|-2`. For p<=2 the only nonzero case is an edge, with at most two roots. For p=3 the triangle on all three roots is t0 and has m-b=2; other triangles have at most two roots. For p>=4, a triangular region has a vertex inside, and K has one outside its boundary triangle. It really is separating. All triangular regions away from t0 contribute zero; at most one other region contributes one. Three roots in K make t0 a face rather than a region. No hidden connectedness assumption survives here.

PROVED-HERE. In the Edmonds converse, each spanning in-tree has exactly one outgoing arc at every x in X. Two disjoint ones therefore exhaust all 2n arcs. Choose sigma at each x to be the face of its outgoing arc in the first tree, and sigma' the face of its outgoing arc in the second. Each is the complement of the other's choice in F. Lemma 4.1 therefore makes both rainbow trees. This checks the complement convention, which is easy to reverse incorrectly. The cut estimate counts arcs with multiplicity, through their black face, and every internal arc is charged once. Root contraction introduces no loop because neither endpoint of a selected side can be two different roots.

PROVED-HERE. In Theorem S(3), a simple directed cycle has distinct heads. Since all arcs through one black face have the same head u(t), its faces are distinct. The simultaneous replacement therefore preserves degree two and uses no already-present incidence. Conversely a balanced symmetric difference decomposes into alternating closed trails, not necessarily simple alternating cycles. Each face has at most one new incidence, so orientation of those trails gives directed closed walks and hence a directed cycle. The note uses the corrected closed-trail wording.

PROVED-HERE. The involution argument does not assume that all walks terminate. Only the initial walk state has no predecessor. Injectivity on the finite set then prevents the initial orbit from entering a cycle. Reversal gives the reverse terminal orbit. A hypothetical fixed point would give a mirror-fixed middle state or a middle transition that does not change its tree. Both are impossible. The n>=1 proviso causes no small-order issue in the actual triangulation domain.

## Required and optional changes

REFUTED, fixed. The Section 2 sentence saying either condition forbids edges at both roots and t0 is false. For the first octahedron from `plantri -b -a 6`, take roots `{0,1,4}` and black faces `A={(0,3,2),(1,2,5),(3,4,5)}`. Choose corners `0,1,3` respectively. In W these edges join white-face indices `1-0`, `0-2`, `1-3`, a spanning tree satisfying the face condition while using two root spokes. I replaced the sentence with the correct separate restrictions. The subsequent description allowing arbitrary corners in a face transversal was already correct. No proof uses the false sentence.

COMPUTED, source reconciliation. The C3 range was stale, rather than an invalid mathematical bound. FACTS.md and the completed reports give an independent exhaustive replay through 20 vertices, 3,373,400 pairs, and the original run through 23, 193,623,384 pairs. I updated those numbers in the note and STATUS.md. This is source reconciliation, not an independent rerun at these sizes.

COMPUTED, required before publication. Figure 5 is not just cramped. In each panel the generated TikZ puts vertices 4 and 5 at the identical coordinate `(-2.887,-0.000)`. It draws their edge from that point to itself, and the black triangular face with these two vertices has zero area. The left boundary also has collinear vertices. A larger scale or a different float position cannot separate coincident points or restore a collapsed triangle. The layout must be repaired and all three panels regenerated, preferably from a strictly convex barycentric embedding of the triangulated disk. This exceeds the allowed edits, so I did not rewrite the figure. It does not refute the graph or its computed witness counts.

PROVED-HERE, optional precision. The sentence after Proposition 7.1, "no argument that works inside one cover can prove Theorem 1.1", is broader than the counterexample warrants. It rules out guaranteeing a good state in an arbitrary prescribed cover. It does not rule out selecting a suitable cover first and then staying there. Suggested wording: "Thus an argument starting from an arbitrary cover cannot guarantee a good state while staying inside that cover." I report this editorial change rather than silently rewriting the discussion.

COMPUTED, optional presentation. Page 5 ends early because the next fixed-position exchange figure will not fit. The proof and its figure remain in reading order. Letting that figure float with `[tbp]`, or reducing its height, would fill more of page 5, but the current whitespace is harmless and a local placement edit may move several later figures. I left the pagination alone. Figure 5 needs geometry work before any size adjustment is useful.

## Page-by-page reading

COMPUTED. All eleven original pages were rendered to `page-01.png` through `page-11.png` and inspected. `page-XX.txt` records extracted text; the two sheets are inspection aids.

| Page | Finding |
| --- | --- |
| 1 | Clear cited good-pair theorem and explicit Step X boundary. State, pair, cover, roots, A, X and n are defined. The claim that a sign-free proof must move between covers should be read with the prescribed-cover qualification above. |
| 2 | H, W, loads, excess and both transversal conditions are defined. Figure 1's two load patterns match its caption. The false root restriction is corrected. |
| 3 | Step R includes the outer-face exception and defines p,m,c,d,varsigma. Lemma 4.1 begins near the foot and its proof continues on page 4, without a figure interrupting it. |
| 4 | Theorem S and its three parts are stated before Figure 2. The directed cycle caption and parent-map convention agree. |
| 5 | Pair criterion, exchange and reversal are readable. Resident, arrival, mirror and step are defined. Large bottom whitespace is cosmetic. |
| 6 | Figure 3 deliberately raises excess, as its caption says. The evenness proof is conditional on an existing good state and says explicitly that it gives no existence proof. |
| 7 | Figure 4 traces the stated two-step resident walk. Region, beta, e,b,rho are defined before density is used. |
| 8 | Three external packing inputs are identified. Theorem 6.9 includes the corrected converse and full cut estimate. Corollary proof continues on page 9. |
| 9 | Explicit finite witness and explicit conjecture. Figure 5 has the collapsed-edge defect above. A size change will not fix it. |
| 10 | Strict descent, periodicity, load convexity and sister conjectures are separated from proved results. Larger ranges require provenance qualifications. The argument promises no polynomial bound. |
| 11 | Computation scope and references are present. No model names or mathematical status tags appear in the reader-facing PDF. STATUS.md is a source-provenance pointer, not a status label attached to a theorem. |

## Dependency table

PROVED-HERE. All nonprimitive major nodes are discharged by the routes above, except C71, which is a finite computational assertion. Each leaf below has one primary classification. There are no circular or route-switch leaves.

| ID | Exact obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| B0 | Finite simple face-bicoloured rooted sphere triangulation | all | domain | hypothesis | Section 1 | discharged |
| N1 | Independent transversal iff every class union has enough rank | C31,C610 | Rado | named theorem | course Ex. 10.26, hypotheses above | discharged |
| N2 | Loopless multigraph forest partition criterion | C65,C68 | Nash-Williams | named theorem | course Ex. 10.28-29, extension above | discharged |
| N3 | Arc-disjoint rooted in-trees iff outgoing rooted cuts have required size | C69 | Edmonds | named theorem | handbook pp. 1674,1685-86, arc reversal | discharged |
| O1 | White hexagonal regions exhaust faces of H | C21 | R21/AND | algebraic/logical step | hexagonal boundary and Euler face count | discharged |
| O2 | Complementary plane edge sets are dual spanning trees | C21 | R21/AND | named theorem | tree/cotree duality for connected H | discharged |
| O3 | F_sigma is subdivided Q_s plus root star | C23 | R23/AND | definition | bijective state, one removed spoke per centre | discharged |
| O4 | Acyclic augmentation iff three components each with one root | C23 | R23/AND | algebraic/logical step | n edges on n+3 vertices | discharged |
| O5 | rank of union C_x = w(J)-comp(T[J]) | C31 | R31/AND | algebraic/logical step | closed walks and adjacency iff shared white face | discharged |
| O6 | It suffices to test connected nonempty J | C31 | R31/AND | algebraic/logical step | white-face sets of components are disjoint | discharged |
| O7 | T[U] has one region Phi; three counts give (3.3) | C31 | R31/AND | algebraic/logical step | Euler, edge sides, signed cancellation | discharged |
| O8 | d>=3; complete c,d,varsigma case split, outer triangle excluded | C31 | R31/AND | side condition | detailed check above | discharged |
| O9 | Black-inner triangle has I white and I+1 black interior faces | C31 | R31/AND | algebraic/logical step | disk Euler and signed side count | discharged |
| O10 | All retained spokes oriented once, unique out-edge except at outer centre | C41 | R41/AND | side condition | 2-factor degrees and complement choice | discharged |
| O11 | Directed cycles correspond to cycles in the functional spoke graph | C41 | R41/AND | algebraic/logical step | outdegree one and edge count; contraction of two-edge paths | discharged |
| O12 | Parent centre differs from sigma and lies in A | C42a | R42a/AND | side condition | roots have parent c(t0); X avoids t0 | discharged |
| O13 | Centre t has 2-c_sigma(t) nonroot children | C42a | R42a/AND | algebraic/logical step | tree degree 3-c_sigma(t), one parent | discharged |
| O14 | One chosen arc per face iff both complementary choices are bijections | C42b | R42b/AND | algebraic/logical step | each face has two incidences in F | discharged |
| O15 | Directed simple cycle uses distinct faces; swaps preserve degrees | C42c | R42c/AND | side condition | common face implies common head | discharged |
| O16 | Symmetric difference gives alternating closed trails and a directed cycle | C42c | R42c/AND | algebraic/logical step | balanced degrees, one new incidence per face | discharged |
| O17 | Black-inner triangle admits at most 2I-1 incidences at I interior vertices | C43 | R43/AND | algebraic/logical step | three distinct boundary faces contribute at most one each; I-2 others at most two | discharged |
| O18 | Fundamental cycle uses exactly two spokes at exchanged vertex | C51 | R51/AND | algebraic/logical step | tree plus one edge | discharged |
| O19 | Exchange at resident reverses by the same fundamental cycle | C52 | R52/AND | proved earlier | C51 plus arrival/resident definition | discharged |
| O20 | Unique empty face and excess two persist until stopping | C53 | R53/AND | algebraic/logical step | target load at most one | discharged |
| O21 | First walk state has no predecessor | C53 | R53/AND | proved earlier | C52, mirror's resident returns to the empty face | discharged |
| O22 | Injective partial map on finite walk-state set terminates from a source | C53 | R53/AND | algebraic/logical step | a repeated orbit would give a predecessor at its first entry | discharged |
| O23 | Reverse orbit returns; odd/even middle rules out fixed points | C53 | R53/AND | algebraic/logical step | mirror changes marked vertex; step changes tree | discharged |
| O24 | Each black triangle contributes 2,1,0,0 to e-b for j=3,2,1,0 | C61 | R61/AND | algebraic/logical step | unique black face at each edge | discharged |
| O25 | Connected induced K: Euler and side counts give region identity | C62 | R62/AND | algebraic/logical step | eliminate facial white count, total black=white | discharged |
| O26 | 3 beta is signed boundary sum; parity and divisibility give bounds | C62 | R62/AND | algebraic/logical step | cancellation across internal edges, d=3,4,5 or >=6 | discharged |
| O27 | Components add e,b and the root penalty correctly | C63 | R63/AND | side condition | roots form a clique; nonempty U; component sum above | discharged |
| O28 | p<=3 satisfies density with root penalty | C63 | R63/AND | algebraic/logical step | isolated point, edge, path or triangle cases | discharged |
| O29 | All triangular regions except possibly root region contribute zero | C63 | R63/AND | side condition | p>=4 and no black-inner separator; three roots exclude exception | discharged |
| O30 | M_u has 4n+6 edges, and centre optimisation gives (6.6) | C65 | R65/AND | algebraic/logical step | count doubled spokes; subtract two per included centre | discharged |
| O31 | Local mu table bounds shortfall plus extra root penalty | C65 | R65/AND | algebraic/logical step | j=0,1,2,3 and doubled outer spokes | discharged |
| O32 | Each maximal forest is a tree; parallel copies split; complementary single spokes dualise | C65 | R65/AND | algebraic/logical step | total edge count, no two parallel edges in a forest, C21 | discharged |
| O33 | U on/outside black-inner separator violates (6.6) for stated u choices | C67 | R67/AND | algebraic/logical step | region identity gives e-b=2|U|-3, rho=3 | discharged |
| O34 | Root contraction leaves no selected loops | C68 | R68/AND | side condition | every root-root edge belongs to t0, not A | discharged |
| O35 | Both types of quotient vertex set satisfy two-forest density | C68 | R68/AND | algebraic/logical step | rho=0 or rho=3; subtract t0 contribution two | discharged |
| O36 | Quotient spanning trees lift to three root-separated components | C68 | R68/AND | algebraic/logical step | connectivity to merged root and no quotient cycle | discharged |
| O37 | Splitting corresponds in both directions to two disjoint in-trees | C69 | R69/AND | proved earlier | C41 plus total outdegree/edge counts; detailed complement check above | discharged |
| O38 | Internal arcs in Y at most e(Y)-b(Y)<=2|Y|-2 | C69 | R69/AND | algebraic/logical step | facewise j-1 bound and rho=0 | discharged |
| O39 | j face blocks have 2j edges in two forests, hence rank >=j | C610 | R610/AND | algebraic/logical step | intersect either forest and take larger part | discharged |
| O40 | Enumerated 16-vertex embedding, covers, good states and rainbow counts match proposition | C71 | R71/AND | algebraic/logical step | independent finite enumeration, witness16.json | discharged computationally |
| O41 | In a single cover, a surplus can be pushed along its cycle to a hole | CX1 | RX1/AND | algebraic/logical step | all choices rainbow by C42c; each vertex has only its two cycle neighbours | discharged |

The major claim rows complete the table. The erroneous root-restriction sentence is a separate, non-supporting exposition claim, and was not silently used to discharge any node.

| ID | Exact claim | Needed by | Route / edge | Classification | Support | Status and statement verdict |
| --- | --- | --- | --- | --- | --- | --- |
| C21 | H and W are dual; complementary trees | C31,C65 | R21 | major claim | O1,O2 | discharged, FOLLOWS |
| C23 | State good iff inverse rainbow, hence excess zero | C53,CX2 | R23 | major claim | O3,O4 | discharged, FOLLOWS |
| C31 | Rainbow exists iff no black-inner separator | C43,CX2 | R31 | major claim | C21,N1,O5-O9 | discharged, FOLLOWS |
| C41 | Complementary cover choice gives rooted directed forest iff rainbow | C42a,C42b,C69 | R41 | major claim | O10,O11 | discharged, FOLLOWS |
| C42a | Each rainbow belongs to one cover | C43 | R42a | major claim | C41,O12,O13 | discharged, FOLLOWS |
| C42b | In-forest description and one-arc-per-face criterion | C42c | R42b | major claim | C41,O14 | discharged, FOLLOWS |
| C42c | Directed cycle iff another cover; unique cover makes all choices rainbow | CX1 | R42c | major claim | O15,O16,C42b | discharged, FOLLOWS |
| C43 | Pair iff rainbow iff no black-inner separator | CX2 | R43 | major claim | C31,C42a,O17 | discharged, FOLLOWS |
| C51 | Unique reversible single-vertex exchange | C52,C53,CX1 | R51 | major claim | O18 | discharged, FOLLOWS |
| C52 | Mirrored step reverses a step | C53 | R52 | major claim | C51,O19 | discharged, FOLLOWS |
| C53 | Iota_t terminates from a good state and is fixed-point-free involution | root | R53 | major claim | C23,C51,C52,O20-O23 | discharged, FOLLOWS |
| C61 | Shortfall identity for every U | C65,C68,C69 | R61 | major claim | O24 | discharged, FOLLOWS |
| C62 | Euler region identity and bounds for connected induced K | C63,C67 | R62 | major claim | O25,O26 | discharged, FOLLOWS |
| C63 | Density for every nonempty U under no-black-inner hypothesis | C65,C68,C69 | R63 | major claim | C62,O27-O29 | discharged, FOLLOWS |
| C65 | Two W spanning trees for arbitrary deleted-corner map | C610 | R65 | major claim | C21,C61,C63,N2,O30-O32 | discharged, FOLLOWS |
| C67 | A black-inner separator obstructs a suitable deleted-corner map | root | R67 | major claim | C62,O33 | discharged, FOLLOWS |
| C68 | Two root-separated spanning forests in T | root | R68 | major claim | C61,C63,N2,O34-O36 | discharged, FOLLOWS |
| C69 | Every cover partitions into two rainbow trees | C610 | R69 | major claim | C41,C61,C63,N3,O37,O38 | discharged, FOLLOWS |
| C610 | Each transversal condition separately met in every cover | root | R610 | major claim | C65,C69,N1,O39 | discharged, FOLLOWS |
| C71 | Specific sixteen-vertex bad cover and all stated counts | root | R71 | major claim | O40, check.py and witness_detail.py | discharged computationally, FOLLOWS |
| CX1 | Step X holds when cover is unique | root | RX1 | major claim | C42c,C51,O41 | discharged, FOLLOWS |
| CX2 | Step X would imply good-pair lemma | root | RX2 | major claim | C31,C23,C43 | discharged conditional implication, FOLLOWS |

LIT. Theorem 1.1 is correctly cited as exposition Proposition 4.8. That proposition states exactly the same hypothesis and conclusion. Its signed proof is not re-proved here, since the note does not supply a proof of it. Verdict for the citation is FOLLOWS. The references to exposition Lemmas 2.5 and 4.2 and Proposition 3.9 also match their numbered statements in the main PDF.

## Verdict

PROVED-HERE. Lemmas 2.1, 2.3, 4.1, 5.1, 5.2, 6.2, 6.3; Theorems 3.1, 4.2 in all three parts, 5.3, 6.5, 6.8, 6.9; Corollaries 4.3, 6.10; identity (6.1); Remark 6.7; and the one-cover Step X argument all FOLLOWS. Every supplied route closes at the classified obligations above. I found no gap in a proved theorem.

COMPUTED. Proposition 7.1 FOLLOWS by independent finite enumeration of its specified plantri instance, subject to the evidence recorded in witness16.json. Its picture still needs repair. The numerical strengthening "strict descent always exists" is FALSE; the independent census confirms the first failures at 8 vertices. Step X remains CONJECTURE and was not promoted to a theorem.

REFUTED, then PROVED-HERE. The Section 2 root-restriction sentence was FALSE as received and FOLLOWS WITH FIX after the recorded one-sentence correction. The overall note is mathematically sound after that correction and the range update, but is not ready for publication until Figure 5's collapsed embedding is repaired. This is a figure-source task for the coordinator, not a reason to rewrite the mathematical proofs.
