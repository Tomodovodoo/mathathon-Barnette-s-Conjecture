# What the mathathon found

## 1. The answer in one page

A Hamiltonian cycle has two jobs: use exactly two edges at each vertex, and connect all vertices. In a cubic bipartite graph, deleting a perfect matching does the first job. The remaining edges can still form several cycles. The proof constructs a matching whose complement is connected by building a forest in the planar dual. This is the organizing question of the [main paper](../paper/main/barnette.pdf) and the [first digestion](steps/01-degree-two-and-connectivity.md).

The dual $T=G^*$ has triangular faces coloured black and white. Choose one black face as the outside; its three vertices are roots. A state assigns each other black triangle a distinct nonroot corner, using every nonroot once. Draw the side opposite each chosen corner to obtain $Q_s$. We want a state with a partner, another state choosing a different corner at every triangle, for which $Q_s$ is a forest. The partner orients the opposite sides, making every nonroot have one outgoing edge. Components therefore lead to a root or contain a directed cycle. This makes the connectivity obstruction visible. [States and pairs](steps/03-states-and-pairs.md)

The key planar fact is a disk count. A directed cycle made from state choices encloses exactly one more white face than black face. The state bijection connects the interior vertex count to the black-face count; Euler's formula then supplies the difference of one. This identity controls signs under two different cycle reversals. It is not a claim about arbitrary cycles in arbitrary triangulations. [Disk identity](steps/04-disk-identity.md)

Now count pairs with signs and weights. First hold the second state $s$ fixed. If $Q_s$ contains a cycle, reversing that cycle changes its partner, preserves the weight, and reverses the sign. All such pairs cancel. Next group the same sum by the unoriented cycles formed by the two states. Their orientations vary independently. Give a cycle a positive increment equal to the number of white faces inside it. At the first possible degree, groups with the fewest cycles contribute with one common sign. The sum is nonzero, so the first cancellation must have left a forest pair. [Cancellation](steps/05-cancellation.md), [nonvanishing](steps/06-nonvanishing.md)

A forest pair gives an incidence tree, then a tree on white faces. Root that tree and select sides toward its root. The selected dual edges yield a primal perfect matching with connected complement, hence one Hamiltonian cycle. Separating triangles require recursion: cap each piece, prescribe compatible boundary choices, and glue the resulting paths. Prescribing an avoided edge makes that compatibility available. [Recovery](steps/07-recovery.md), [gluing](steps/08-gluing-and-hypotheses.md)

The history review identifies the new mechanism as the disk identity coupled to this two-way signed count. The dual formulation, edge avoidance, and separator reduction have older precedents. The mathathon's contribution is chiefly an explanation of that mechanism, several simpler forms, and a substantial record of unsuccessful replacements. It has not produced a general unsigned proof or a polynomial-time constructor. [History report](../research/2026-11-14_opus_history-literature/REPORT.md), [route map](route-map/HOW-IT-WORKS.md)

The merged exposition keeps the geometry in $T$, replaces complex phases by local signs, replaces spoke circulations by heights along face paths, and proves connectivity inside a cycle before applying Euler. Its main theorem has an independent AI referee. This is review of an informal proof, not human peer review of the new manuscript. [Merge](../research/2026-11-14_opus_manuscript-merge/REPORT.md), [main referee](../research/2026-11-14_sol_referee-main/REPORT.md)

## 2. What exists now

The diagram shows source and evidence relationships. The companion texts explain the same signed mechanism in different languages. [Correspondence](../research/2026-11-14_fable_dependency-graph/correspondence.md)

![Products and their supporting evidence](synthesis-figures/products.png)

[Vector PDF](synthesis-figures/products.pdf).

| Product | What it provides and where to begin |
|---|---|
| [Main paper](../paper/main/barnette.pdf) | Opening, dual target, corner choices, disk count, paired count, initial pair and gluing. |
| [Proof blueprint](../proofs/blueprint/README.md) | Statement-level correspondences to the papers and Lean, with explicit translation gaps. |
| [Primal companion](../proofs/primal/README.md) | A complete route in $G$, using cut shores, a charge flow and direct recovery. |
| [Involution companion](../proofs/involutions/README.md) | Li's general multi-mark argument written out as two finite involutions. |
| [Step digestions](steps/00-overview.md) | Longer proofs, worked examples and failed alternatives at each step. |
| [Route map](route-map/ROUTE-MAP.md) | Routes organized by the obligation they address; begin with [how it works](route-map/HOW-IT-WORKS.md). |
| [Atlas](atlas/README.md) | Computed pictures of the routes, not independent proofs. |
| [Labyrinth](../labyrinth/README.md) | Structured claims, dependencies, evidence and unresolved frontiers. |
| [Reference lab](../workings/barnette_lab/README.md) | Enumerate states and pairs, evaluate counts, recover cycles and check certificates. |
| [Library](../papers/INDEX.md) | Sources, access status, bibliography and links to their uses. |
| [Figures](../paper/figures/) | Shared graph objects and drawings; [polish report](../research/2026-11-14_sol_figures-polish/REPORT.md) records checks. |

## 3. Simplifications worth keeping

Write $\#TM$ for the number of tree-matching states at the chosen facial root, $\#HC$ for all Hamiltonian cycles of $G$, and $c_{\min}$ for the least number of cycles in an unoriented pair cover. These count different objects; the leading signed coefficient is yet another count. [Counting conventions](../research/2026-11-14_sol_referee-covers/INTEGRATION.md)

**Read the disk identity as a face balance.** For chosen-edge cycles, $W=B+1$ says what the arithmetic measures. Astra checked the proof and independently enumerated its consequences; topology referee Fable also confirmed it. Keep the state hypothesis beside the formula. [Combinatorics review](../research/2026-11-14_astra_referee-combinatorics/REPORT.md)

**Multiply local signs.** Set $\epsilon(r,s)=\prod_{t\in A}\delta(r(t),s(t))$, where $\delta$ records direction around the black triangle. This replaces the complex phase up to a global normalization. Opus's draft A review and Fable's draft B review found the simplification; Sol checked its merged use. [Draft A review](../research/2026-11-14_opus_review-draft-A/REPORT.md), [main review](../research/2026-11-14_sol_referee-main/REPORT.md)

**Define heights where needed.** Paths of faces from the outside define signed crossing counts. Summing heights over white faces makes the change under a cycle reversal equal, with the chosen orientation convention, to the enclosed white-face count. Fixed paths or a reference normalization matter. Fable supplied face-path heights; Astra checked the earlier height proof; Sol checked the merged version. [Draft B review](../research/2026-11-14_fable_review-draft-B/REPORT.md), [height referee](../research/2026-11-14_astra_referee-combinatorics/REPORT.md)

**Use finite differences or one polynomial.** Orienting a cover's $c$ cycles gives a Boolean cube. Alternating over it kills every height polynomial of degree below $c$. At degree $c$, the product of positive cycle increments survives with controlled sign. Linear incidence weights also give a single ordinary polynomial of degree at most $n$. Fable checked that proof; Sol checked the main finite-difference proof. The separate expression $\sum\epsilon z^{\omega(s)}$ can be Laurent when heights are negative. [Determinant review](../research/2026-11-14_fable_referee-determinants/REPORT.md), [main correction](../research/2026-11-14_sol_referee-main/REPORT.md)

**Supply inside connectivity.** Euler on everything inside a cycle requires a connected plane graph. Draft B left that premise unwritten. Its referee supplied a short lemma; the merge incorporated it, and Sol checked that the repair is noncircular. [Draft B review](../research/2026-11-14_fable_review-draft-B/REPORT.md), [main referee](../research/2026-11-14_sol_referee-main/REPORT.md)

**Read the disk count as turning.** Signed angles give a Gauss-Bonnet account of the identity. Fable accepted Opus's derivation after supplying boundary-flatness and disk hypotheses. This gives intuition without bypassing the count. The corrected Morse interpretation also needs root spokes in its matching. [Topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md)

**Make pair existence exact.** The Euler region identity is $e-b-(2p-4)=\frac12\sum_F(\beta(F)-d(F)+4)$. A connected induced subgraph has $p$ vertices, $e$ edges and $b$ actual black faces; other regions have boundary length $d(F)$ and black-minus-white count $\beta(F)$. Repeated boundary sides count separately. With the capacity-two Hall condition, this says a pair exists exactly when no separating triangle has black inner boundary. Sol independently checked both directions, including disconnected sets in the cut argument. [Integration, sections 1 and 2](../research/2026-11-14_sol_referee-structure/INTEGRATION.md)

**Cut only where necessary.** The exact obstruction permits gluing only at black-inner separating triangles. In primal language, every nontrivial three-edge cut must put the chosen black root on its black-ended shore for the reduced incidence graph to have its required two-factor. Sol checked this sharper criterion and gluing. [Integration](../research/2026-11-14_sol_referee-structure/INTEGRATION.md)

**Say which cycles recovery finds.** For a fixed prescription, recovery is injective but need not be surjective. A Hamiltonian cycle yields a state; it is recovered exactly when that state is a tree matching. Otherwise the state has no partner. White-parent acyclicity gives the explicit image test. Sol checked this stronger dichotomy. [Recovery review](../research/2026-11-14_sol_referee-structure/REPORT.md)

**Translate counts back to $G$.** For the admissible primal deletion $S$ corresponding to a cover $D$, $c(D)=\kappa(G-S)-1$. The deletion constraints are essential; $S$ is not the recovery matching. Sol's cover review accepts this dictionary. Separately, Astra's combinatorics review accepts $3\#TM\leq\#HC$, with the source's rooting conventions, and $\#TM\geq2c_{\min}$. These are bounds, not an exact formula for all Hamiltonian cycles. [Cover review](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md), [count review](../research/2026-11-14_astra_referee-combinatorics/REPORT.md)

**Obtain inclusion from avoidance.** To include an edge at a cubic vertex, avoid a different incident edge. A Hamiltonian cycle must use the other two. The older-approaches report supplies this elementary consequence and finite checks; it has no separate referee. [Older approaches](../research/2026-11-14_astra_older-approaches/REPORT.md)

**Keep the determinant's qualification.** The signed count is a squarefree face coefficient of a mixed determinant. Fable showed that the constructive and dimer formulas coincide up to diagonal conjugation and scalar. Setting every variable to one loses the needed information. A positive coefficient norm still requires nonvanishing and supplies no independent existence proof. [Determinant referee](../research/2026-11-14_fable_referee-determinants/REPORT.md)

A useful answer to "how many cycles in $G$?" is now available for specific families. For the even $2m$-prism the total is $2m+2$; the avoidance counts are two for a rail and $2m-2$ for a rung. More generally, with $b$ irreducible pieces the reviewed separator argument gives at least $2^b$ cycles avoiding a prescribed edge and at least $3·2^b$ cycles overall. The cube has six. Prisms rule out a universal exponential lower bound in primal order over the entire class. The families referee checks these statements; none is an exact count for arbitrary $G$. [Families review, F1 and F5](../research/2026-11-14_sol_referee-covers/REFEREE-families.md)

## 4. The three papers connected

The dependency audit isolates fourteen shared nodes: dual and root; balanced incidence graph; first pair; disk identity; reversing signs; positive cycle increments; fixed-state cancellation; nonvanishing; forest pair and incidence tree; white-face tree; selected matching; one cycle; separator gluing; prescribed-edge theorem. "Shared" describes these proofs, not every possible proof. [Minimal skeleton](../research/2026-11-14_fable_dependency-graph/skeleton.md)

| Object | OpenAI | Li | Constructive paper |
|---|---|---|---|
| State | Triangle-to-corner bijection | Matching in reduced incidence graph | Matching of $B$ |
| Pair | Disjoint states | Ordered two-factor | Matching pair |
| Obstruction | Cyclic $Q_s$ | Failure of cycle-breaking condition | Non-tree matching |
| Nonzero count | Lowest Taylor coefficient | Fixed objects of second involution | Polynomial coefficient or marked walk |
| Recovery | White tree, two induced trees | Connected complement in $G$ | Incidence tree, rooted selection |

The [correspondence table](../research/2026-11-14_fable_dependency-graph/correspondence.md) gives exact translations, including conflicting uses of $H$. Four points differ materially: first pair, weights, nonvanishing, and final connectivity. Li's marks encode the same lowest-degree information as the weighted sum. [Skeleton](../research/2026-11-14_fable_dependency-graph/skeleton.md)

The audit found OpenAI and the constructive route closed within its boundary. Li needed the balance count for Ore's theorem and three Appendix B verifications supplied. The involution companion now writes out the general argument, accepted by Opus's independent referee. It is Li's intended proof unpacked, not a new unsigned route. [Dependency report](../research/2026-11-14_fable_dependency-graph/REPORT.md), [involution referee](../research/2026-11-14_opus_referee-involutions/REPORT.md)

Lean obtains an algebraic dual from a drawing, uses root-free bond shores in $G$, one charge flow and linear polynomial factors, recovers directly in $G$, and inducts on edge avoidance. It does not state the two-induced-trees theorem or formalize the Pfaffian corollary. The local rebuild reports only `propext`, `Classical.choice` and `Quot.sound`. That check covers the upstream formal development, not the new heights or involution manuscripts. [Lean report](../research/2026-11-14_opus_lean-formalisation/REPORT.md), [primal dictionary](../proofs/primal/DICTIONARY.md)

The late blueprint pins its extraction to a committed manuscript, rather than silently mixing revisions. It distinguishes exact Lean statements, statements requiring informal translations, and unmatched statements. A matching theorem statement does not certify the manuscript's proof: its two-tree gluing differs from Lean's matching gluing. The blueprint's formalization line estimates differ between its feasibility note and report, so no effort estimate is adopted here. [Blueprint report](../research/2026-11-14_opus_blueprint/REPORT.md), [feasibility note](../proofs/blueprint/FORMALISATION.md)

## 5. Proof routes and failures

Unless marked primal, sizes below count vertices of $T$. "First" means the cited exhaustive range establishes minimality; "witness" makes no such claim. The full negative inventory is in the [route map](route-map/ROUTE-MAP.md).

| Kind | What worked | What failed, and what remains |
|---|---|---|
| Combinatorial | Heights, reversal and finite differences give a checked proof. | Highest/lowest-state and uniform-direction shortcuts fail at 12 after reflection is included. Six tree matchings with $c_{\min}=2$ at order 13 refute a partition into four-element cubes. The exponential bound remains open. [Review](../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| Graph-theoretic / structural | Exact pair criterion and three-matroid formulations are checked. Two-tree packing has an unreviewed new proof. | The natural two-matroid relaxation admits four false states on the hexagonal prism, dual order 8. A fractional LP vertex exists at 13, without minimum-order proof. A support with no tree matching occurs at 16. Hidden alternative encodings are not excluded. [Determinants](../research/2026-11-14_fable_referee-determinants/REPORT.md), [structure](../research/2026-11-14_sol_referee-structure/REPORT.md), [packing](../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| Constructive / algorithmic | Enumeration, marked walks, recovery and recursion have implementations. | No polynomial-time bound. Strict rainbow descent fails at 8; a surplus walk cycles at 38, a witness rather than proved minimum. Plateau search remains a candidate. [Lab](../workings/barnette_lab/README.md), [topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md) |
| Algebraic / determinantal | Equivalent mixed determinants and linear weights are checked. | Raw determinants fail on the hexagonal prism; doubled edges fail at 9. A sign gauge fails at a 13-vertex witness. Smallest tested zero-residue witnesses for moduli 2, 3, 4, 5, 7 and 11 have dual orders 6, 13, 9, 14, 16 and 26 respectively; the last is not an exhaustive minimum. No independent positivity theorem. [Referee](../research/2026-11-14_fable_referee-determinants/REPORT.md), [algebra](../research/2026-11-14_sol_route-algebra/REPORT.md) |
| Topological | Turning number and dual rank explain disk and recovery. Corrected Morse reading passes review. | Ordinary Euler characteristic loses the graded information. New rainbow existence and completion proofs await another reader; exchange descent remains open. [Topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md) |
| Probabilistic | Packing gives a feasible fractional point; explicit families show exponential rarity. | Positive full-support tree measures miss the target mean even on the cube, primal order 8. Conditioning changes that obstruction's scope. Unit-circle and real-rootedness shortcuts fail at dual order 12. [Probability](../research/2026-11-14_sol_route-probabilistic/REPORT.md), [packing correction](../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| Categorical | Boundary-pattern vectors compose across cuts: three triangular patterns, six allowed quadrilateral patterns, conditional on the supplied theorem. | Five-cycle boundaries have piece-dependent patterns at order 9. Homology and Belyi vocabulary gave no existence proof. The useful output is the boundary table; the report is unrefereed. [Report](../research/2026-11-14_fable_route-categorical/REPORT.md) |
| Inductive | Splitting, conditional lift criterion and rotation pass review. One-sided induction has a written proof. | Reverse lifting fails at 11; no directly lifting matching at some contractions at 18. Inward selection fails at 11, 13 and 14; mate repair at 16, single-cycle repair at 17, all fixed-cover direction repair at 18. G and X remain open. [Referee](../research/2026-11-14_fable_induction-completion/REPORT.md), [latest lemmas](../research/2026-11-14_astra_induction-lemmas/REPORT.md) |
| Lattice-theoretic | Alpha-orientation lattice and decorated ideals describe the objects and cancellations. | Both extremes fail first at 18. Extremes-or-irreducibles fail at a 33-vertex witness, not a proved minimum. Fixed-cycle-count levels can disconnect at 18. No canonical lattice selection. [Referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [cover review](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md) |
| Non-planar / Pfaffian | The corollary follows through Gorsky-Steiner-Wiederrecht; six trisum path signatures support gluing. | On Heawood, primal order 14, the root-free torus count is zero although cancellation survives. Direct non-planar nonvanishing remains open; the investigation is unrefereed. [Report](../research/2026-11-14_astra_route-pfaffian/REPORT.md) |

![Kinds of route by recorded outcome](synthesis-figures/route-outcomes.png)

[Vector PDF](synthesis-figures/route-outcomes.pdf). Counts come from [routes.py](route-map/routes.py), with one editorial primary kind per record, assigned by explicit rules in [count.py](../research/2026-11-14_astra_synthesis/count.py). "Proved" combines source arguments and written project proofs, including unreviewed work. "Open" includes suggestions. Categories overlap mathematically; the [assignment ledger](../research/2026-11-14_astra_synthesis/route-classification.json) makes this forced classification inspectable.

## 6. Why the signed count seems necessary

This is an interpretation, not an impossibility theorem. The packing report proves that every pair support contains a white spanning tree satisfying either side's degree requirement separately. It also proves a split into two point-rainbow trees. A split into two face-rainbow trees remains conjectural. Neither supplies a tree satisfying both requirements at once. [Packing report](../research/2026-11-14_opus_two-tree-packing/REPORT.md)

The 16-vertex support with no tree matching makes the obstruction concrete. Reorienting its cycles cannot create the missing object. Its LP midpoint is feasible but outside the convex hull of tree matchings. The three-matroid formulation explains why dropping one constraint solves an easier problem; the lattice counterexamples show why choosing an extreme support does not fix it. A general method must sometimes change supports, or justify selecting a good one. [Packing](../research/2026-11-14_opus_two-tree-packing/REPORT.md), [structure](../research/2026-11-14_sol_referee-structure/REPORT.md), [lattice](../research/2026-11-14_sol_referee-conjectures/REPORT.md)

The signed count compares supports while cancelling bad fixed states. This explains its current role and leaves room for a global exchange or induction. The negative results refute specified shortcuts, not all unsigned proofs. [Scope corrections](../research/2026-11-14_astra_referee-combinatorics/REPORT.md)

## 7. Open problems, ranked

1. **Close the induction without borrowing cancellation.** G asks whether every separator-free rooted triangulation above order 6 has a nonroot degree-four merge that remains simple and admits a pair. X asks, in the two-sided case, for a nonexceptional tree matching of a contraction; rotation handles the one-sided case. G passes 62,416 rooted instances through order 19. The contraction inequality passes 1,202,792 contractions through order 18. The latest report proves G without chordless five-cycles and extends global half-exception tests through 18. First try global uncrossing of four- and five-cycle obstructions and a cover-changing repair on the order-18 exception. The latest report corrects the earlier claimed equivalence: the strict counting inequality is sufficient, not proved necessary. [Missing lemmas](../research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md), [latest report](../research/2026-11-14_astra_induction-lemmas/REPORT.md)

2. **Prove $\#TM\geq2^{c_{\min}}$.** Independently reproduced all-root evidence covers 4,656,948 feasible instances through order 22. The separator-free author census reaches 24, but its full replay is not independently certified. Unique-cover equality and a separator-free family with unbounded $c_{\min}$ now have a referee; the two-cover result also has a written review. First extend the shared-state calculation beyond two covers. Fixed-cycle-count connectivity is already false. [Conjecture referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [cover referee](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md)

3. **Prove monotone descent with plateaus.** Pair descent asks for allowed reversals reaching a forest without increasing the number of $Q$-cycles. Rainbow descent asks for nonincreasing black-face excess under exchanges. They are different conjectures. Rainbow descent passes all roots through order 17, by exhaustive enumeration or the unique-cover proposition, plus samples to 120. First compare their plateau components using the rainbow-to-cover dictionary. A proof must explain escape from periodic surplus walks. [Topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md), [pair descent](../research/2026-11-14_sol_referee-structure/REPORT.md)

4. **Find a polynomial-time constructor.** Testing a specified direction choice is easy; finding one across arbitrary supports has no polynomial guarantee here. First seek a polynomial plateau-diameter bound or a potential surviving the stored traps. Uniform sampling is not justified by existence because successful states can be exponentially rare. [Conjecture referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [families](../research/2026-11-14_sol_counting-families/REPORT.md)

5. **Prove the non-planar statement directly.** Replace planar positivity in the Pfaffian setting without importing the structural theorem. First work through Heawood's zero polynomial and the six trisum signatures; a sign convention alone cannot restore nonvanishing. [Pfaffian investigation](../research/2026-11-14_astra_route-pfaffian/REPORT.md)

6. **Formalize this exposition's route.** The upstream theorem is built, but face-path heights, the geometric inside lemma and this exact recovery presentation are not thereby formalized. The new blueprint has already compiled the finite-difference lemma independently. First formalize the local-sign normalization and height/path-flow translation against the existing algebraic dual model; those bridges cover more of the route than starting geometric topology anew. [Blueprint](../research/2026-11-14_opus_blueprint/REPORT.md) [Lean comparison](../research/2026-11-14_opus_lean-formalisation/REPORT.md), [main referee](../research/2026-11-14_sol_referee-main/REPORT.md)

## 8. What the literature review established

These ten points summarize the library's findings, not a fresh literature search.

1. Stein's two-induced-trees formulation predates the supplied proof. [History](../research/2026-11-14_opus_history-literature/REPORT.md)
2. Edge avoidance and separator reduction also have older precedents. [Novelty review](../research/2026-11-14_astra_older-approaches/REPORT.md)
3. The paired-state mechanism was not found in the history review's 23 collected Barnette papers. [History](../research/2026-11-14_opus_history-literature/REPORT.md)
4. Earlier progress includes restricted face sizes, face-colour conditions, leapfrogs and computation. [Results](../research/2026-11-14_opus_history-literature/RESULTS-TABLE.md)
5. The cited general computation reaches 90 primal vertices. [Source check](../research/2026-11-14_sol_referee-main/REPORT.md)
6. The machinery review distinguishes eleven reformulations and eighteen proposed routes. [Report](../research/2026-11-14_sol_machinery-literature/REPORT.md)
7. The proposed Feder-Subi parity identification fails on the truncated octahedron. [Older approaches](../research/2026-11-14_astra_older-approaches/REPORT.md)
8. The constructive manuscript's author and public provenance were not established. [Library review](../research/2026-11-14_astra_literature-consolidation/REPORT.md)
9. Waterloo attribution remains unresolved; several older originals were available only through secondary citations. [Index](../papers/INDEX.md)
10. "Not held in papers" does not mean unopened: the main referee found Hertel and Alt-Payne-Schmidt-Wood originals in the history folder. [Correction](../research/2026-11-14_sol_referee-main/REPORT.md)

## 9. What the earlier rewrite taught us

These lessons come from the [floating-proof reconstruction](../research/2026-11-14_astra_exposition-method/HOW-THE-REWRITE-WORKED.md) and [style guide](../research/2026-11-14_astra_exposition-method/STYLE-GUIDE.md).

1. Remove unnecessary proof obligations before shortening sentences.
2. Begin with connectivity, then introduce the object that addresses it.
3. Give a definition when its purpose becomes visible.
4. Keep one main route; separate algorithmic extensions.
5. Name what each reversal changes and preserves.
6. Distinguish degree two from connectedness.
7. Keep example labels across representations.
8. Put figures beside the questions they answer.
9. Preserve quantifiers, domains and normalization.
10. Compare rendered passages; a clean build does not establish clarity or preservation.

The merge applies local signs, face-path heights and the inside lemma. Its cold reader still found an overloaded opening, missing motivations and floats interrupting proofs. Those findings explain the second revision; earlier praise cannot replace checking revised pages. [Merge](../research/2026-11-14_opus_manuscript-merge/REPORT.md), [cold read](../research/2026-11-14_fable_coldread-main/REPORT.md)

## 10. Review status and limits

"Refereed" here means another AI model read a specified argument and, where recorded, wrote its own checking code. It does not mean journal review, human approval or formal verification of new prose. The main, primal and involution referees state their background assumptions and claim boundaries. New lemmas inside a referee report do not automatically acquire a second reader. [Main](../research/2026-11-14_sol_referee-main/REPORT.md), [primal](../research/2026-11-14_fable_referee-primal/REPORT.md), [involutions](../research/2026-11-14_opus_referee-involutions/REPORT.md)

Corrections matter. Reflection lowers two counterexamples to order 12. True lattice extremes replace mislabeled facial terminals, then fail jointly at 18. The 33-vertex construction refutes the irreducible variant. The primal revision disputed the phase warning. Opus's late cross-audit settles it in favour of the revision: the aligned ratio is $i^n$, independent of cycle count; reversing all corner conventions gives $i^{-n}$. Its own code checks 24,856 pairs. [Adjudication](../research/2026-11-14_opus_cross-audit/ADJUDICATION.md) [Combinatorics](../research/2026-11-14_astra_referee-combinatorics/REPORT.md), [structure](../research/2026-11-14_sol_referee-structure/REPORT.md), [conjectures](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [primal revision](../research/2026-11-14_astra_primal-revision/REPORT.md)

The involution referee resolves 279 versus 213 marked objects: two drawings swap root anchors 4 and 5. Both totals are correct; the signed sum is invariant. The reviewed version had an off-route sign error for odd numbers of marks. The revision corrects it and adds a drawing-free path-mark lemma, whose self-audit is not an independent review. [Revision](../research/2026-11-14_sol_involutions-revision/REPORT.md) The main referee's Laurent correction is also outside the theorem route, and the version 2 change record says it has been applied. [Main changes](../research/2026-11-14_astra_main-revision/CHANGES.md) These are precise corrections, not reasons to reject the main theorem or ignore faulty side formulas. [Involution referee](../research/2026-11-14_opus_referee-involutions/REPORT.md), [main referee](../research/2026-11-14_sol_referee-main/REPORT.md)

Separate reviews remain missing for the new induction lemmas, packing theorems, algebra extensions, categorical investigation, direct Pfaffian investigation, the new path-mark lemma and new rainbow results inside the topology referee. The late families referee accepts prisms, prism chains, rebuilt tube recurrences and rarity; larger direct censuses, decimal asymptotics and subdivision tables remain outside its replay. [Families review](../research/2026-11-14_sol_referee-covers/REFEREE-families.md) The atlas and this synthesis have no second-model review. The complete order-24 cover census has not been independently replayed. These limits are recorded in the [induction](../research/2026-11-14_astra_induction-lemmas/REPORT.md), [packing](../research/2026-11-14_opus_two-tree-packing/REPORT.md), [algebra](../research/2026-11-14_sol_route-algebra/REPORT.md), [category](../research/2026-11-14_fable_route-categorical/REPORT.md), [Pfaffian](../research/2026-11-14_astra_route-pfaffian/REPORT.md), [families](../research/2026-11-14_sol_counting-families/REPORT.md), [topology](../research/2026-11-14_fable_referee-topology/REPORT.md), [atlas](atlas/README.md) and [cover review](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md).

The late families review also corrects the Florek comparison's degree parameter and hypothesis, and distinguishes a published ceiling from its absence in an older preprint. A prism-chain control gives a different Hamiltonian count under a different gluing permutation; this is not a contradiction once the labelled construction is retained. [Final cover and families report](../research/2026-11-14_sol_referee-covers/REPORT.md)

For a human check, I recommend the [main paper](../paper/main/barnette.pdf), for the complete explanatory route; the [main referee](../research/2026-11-14_sol_referee-main/REFEREE.md), for exact obligations and repairs; and the [missing induction lemmas](../research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md), read with the [latest counterexamples](../research/2026-11-14_astra_induction-lemmas/REPORT.md), for the clearest unfinished alternative.

## 11. Numbers and snapshot

The [script](../research/2026-11-14_astra_synthesis/count.py) records its timestamp, report hashes, product pages and chart assignments in [counts.json](../research/2026-11-14_astra_synthesis/counts.json). It counts run folders, not sessions or independent discoveries. Model labels follow folder names and the [index](../research/INDEX.md). Census ranges are extracted from reports, not rerun here.

<!-- inventory-start -->
At 2026-11-14T12:58:26.541101+00:00, the inventory has 59 run folders and 55 delivered REPORT files, including this synthesis. Four model labels occur: GPT-6 Astra, 16 runs, Fable 5.2, 15 runs, Opus 5.5, 14 runs, GPT-6.1 Sol, 14 runs. The route map has 226 records: 46 source arguments, 57 project proofs, 12 computed routes, 19 conjectures, 25 suggestions and 67 refutations. These are recorded statuses, not a fresh adjudication. [Inventory](../research/2026-11-14_astra_synthesis/counts.json)

| Current product PDF | Pages |
|---|---:|
| [paper/main/barnette.pdf](../paper/main/barnette.pdf) | 19 |
| [proofs/primal/primal.pdf](../proofs/primal/primal.pdf) | 15 |
| [proofs/involutions/involutions.pdf](../proofs/involutions/involutions.pdf) | 17 |
| [proofs/blueprint/blueprint.pdf](../proofs/blueprint/blueprint.pdf) | 1 |
| [proofs/blueprint/columns.pdf](../proofs/blueprint/columns.pdf) | 1 |
| [digestions/atlas/atlas.pdf](../digestions/atlas/atlas.pdf) | 31 |

These six PDFs total 84 pages, including two one-page blueprint diagrams. Drafts, archived versions and individual figure PDFs are excluded. The step files contain 26,413 regex-counted word tokens, including headings and Markdown targets, so that count is not reading-time prose. [Counting method](../research/2026-11-14_astra_synthesis/count.py)

The [computation ledger](../research/2026-11-14_astra_synthesis/EVIDENCE.md) gives each largest cited census by claim, with its own population and review scope. Its rainbow total is 69,458,112 enumerated trees; unique-cover instances settled by a proposition are separate. [Extraction script](../research/2026-11-14_astra_synthesis/evidence.py)
<!-- inventory-end -->

The largest independent all-root exponential-bound check covers 4,656,948 feasible roots through dual order 22. The larger separator-free author check covers 23,824,742 facial roots through order 24. Rainbow descent was checked through order 17 by enumeration and a unique-cover proposition. These populations overlap and must not be added into one "instances checked" total. [Conjecture referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [cover review](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md), [topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md)

<!-- late-start -->
The closing scan incorporated the induction-lemmas report, topology referee, finished cover and families referee report, cross-audit adjudication, blueprint and involution revision. The main paper has a revised working PDF and an archived version 1, but no main-revision REPORT at this scan; version 2 is not certified here as finished. Descent, the new involution referee and Lean-devices runs also have no REPORT. Their existence is not a mathematical result. This document freezes that boundary instead of promoting unfinished work. [Scan record](../research/2026-11-14_astra_synthesis/late-scan.json)
<!-- late-end -->
