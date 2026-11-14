# What the mathathon found

Snapshot of 14 November 2026. GPT-6 Astra wrote this document. Fable 5.2 then checked every claim against its source and edited it ([ledger](../research/2026-11-14_fable_synthesis-audit/FACT-CHECK.md), [change log](../research/2026-11-14_fable_synthesis-audit/CHANGELOG.md)). No human has checked this document or any proof it describes.

Names follow the main paper. A **good state** is what most research reports call a tree matching. A **good pair** is their forest pair or tree pair. A **cover** is the set of undirected cycles of a pair, and $m$ is the least number of cycles in a cover, their $c_{\min}$.

## 1. The answer in one page

**How the proof works.** A Hamiltonian cycle needs degree two at every vertex and one component. In a cubic graph $G$, deleting a perfect matching gives degree two, so the whole problem is connectivity. Pass to the planar dual $T$, a triangulation whose triangles are coloured black and white. A perfect matching of $G$ becomes a selection, one side of every triangle, and its complement is connected exactly when the selection contains no cycle. So the theorem asks for an acyclic selection through a prescribed side $e_0$.

Fix a black triangle $t_0$ at $e_0$ and call its corners roots. A state chooses one corner in every other black triangle and uses every vertex that is not a root exactly once. A state is good when the sides opposite its chosen corners form a forest with exactly one root in each tree. A good state forces a selection through a tree on the faces. That selection is acyclic by the disk identity: a directed cycle of sides leaving chosen corners encloses exactly one more white triangle than black.

Nobody knows how to point to a good state, so the proof counts. A pair is two states that differ in every triangle. Each pair gets a sign, and a weight that depends only on its second state. If the opposite sides of the second state contain a cycle, reversing that cycle changes the first state, keeps the weight and flips the sign, so all such pairs cancel. The same sum, grouped by the cycles along which the two states differ, is a repeated difference. Its first surviving term is a product of positive numbers, the counts of white triangles inside those cycles. So the sum is nonzero, and a good state exists as soon as one pair exists. A flow argument gives a pair when $T$ has no separating triangle. Otherwise the induction cuts along a separating triangle, and the prescribed side makes the two halves agree.

**What we added.** No new theorem about Barnette's conjecture. The proof is OpenAI's. We wrote a 19-page exposition with one running example, two companion proofs, a statement-by-statement link to the Lean formalisation, and Lean files that check the paper's own sign and counting step. Four changes shorten the argument: the disk identity stated as "one more white than black", a real sign that is a product of local signs, weights read as heights along paths of faces, and a finite difference in place of the exponential sum. One step the OpenAI paper leaves tacit is now proved: the inside of a cycle is a connected plane graph, so Euler's formula applies. Around the proof we have an exact criterion for the first pair, the set of Hamiltonian cycles the construction finds, counts on explicit families, and a map of 244 attempted routes, 77 of them recorded as refuted.

**What is solid.** The theorem itself: OpenAI's Lean proof builds locally and uses only the three standard axioms. That certifies OpenAI's formal route, not our text. Our main paper: Sol, a different model from its authors, refereed version 1 and found the route sound, with eight corrections off the route. Version 2 applies them. Sol's second audit, of the final text of version 2, again returns "follows", after eight small corrections of wording and scope. Of the 34 statements on the paper's route, the blueprint matched 4 to a Lean declaration exactly, 25 after a translation nobody has formalised, and 5 not at all. A late Lean run then checked the sign, the cancellation and the nonvanishing step in the paper's form. By the checker's count from its list, that leaves 8 exact, 24 translated and 2 without a counterpart. Each companion proof passed two reviews by models other than its author. All of these checks are by AI models. No human has checked any of it.

**What is open.** A proof that avoids the signed count. We have none, and section 6 says why the obvious shortcuts fail. A polynomial-time way to find the cycle. The bound that there are at least $2^m$ good states. A direct proof for non-planar Pfaffian graphs. A complete formal proof of our own route.

**What a human should read first.** The [main paper](../paper/main/barnette.pdf), whose first two pages give the plan on the cube. Then the [referee's report](../research/2026-11-14_sol_referee-main-v2/REFEREE.md) on version 2, which lists every obligation it checked. For a ten-minute tour of the mechanism, [how it works](route-map/HOW-IT-WORKS.md).

## 2. What exists now

![Products, their sources and who checked them](synthesis-figures/products.png)

[Vector PDF](synthesis-figures/products.pdf).

| Product | What it is, and its review status |
|---|---|
| [Main paper](../paper/main/barnette.pdf) | Version 2, 19 pages: target, corner choices, disk identity, signed count, first pair, gluing. Refereed in both versions. [Version 1](../paper/main/history/barnette-v1.pdf), 18 pages, is kept. |
| [Primal companion](../proofs/primal/primal.pdf) | 15 pages. The whole proof in $G$, without the dual, close to the Lean route. Refereed, then accepted in a final review. |
| [Involution companion](../proofs/involutions/involutions.pdf) | 18 pages. Li's argument for general $m$, written out as two sign-reversing involutions. Refereed twice. |
| [Proof blueprint](../proofs/blueprint/BLUEPRINT.md) | Each statement of the main paper beside its counterparts in the OpenAI paper, the companions and Lean. Not reviewed. |
| [Lean devices](../proofs/lean/README.md) | 866 lines of Lean that prove the paper's sign lemma, cancellation, finite difference and nonvanishing step on top of OpenAI's proof. Checked by the Lean kernel. The reading against the paper is not reviewed. |
| [Step digestions](steps/00-overview.md) | Eleven files with longer proofs, worked examples and failed alternatives for each step. Audited once. |
| [Route map](route-map/ROUTE-MAP.md) | 244 route records sorted by the step they address. Start with [how it works](route-map/HOW-IT-WORKS.md). |
| [Atlas](atlas/atlas.pdf) | 31 pages of computed pictures of 28 routes. Readings of one proof, not 28 proofs. Audited, and rebuilt with the audit's corrections. |
| [Labyrinth](../labyrinth/README.md) | Claims, dependencies, evidence and open frontiers as structured data. |
| [Reference lab](../workings/barnette_lab/README.md) | Code that enumerates states and pairs, evaluates the count and recovers cycles. |
| [Library](../papers/INDEX.md) | 87 sources with access status, and a bibliography. |

## 3. Simplifications worth keeping

Each item names who found it and which other model checked it. Section 10 says what such a check is worth.

**The disk identity as a face balance.** For a directed cycle of chosen sides, $W=B+1$: one more white face inside than black. It needs the state and is false for arbitrary cycles. Astra and Fable checked it in separate referee runs, and Sol checked its use in the main paper. [Combinatorics referee](../research/2026-11-14_astra_referee-combinatorics/REPORT.md), [topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md)

**A sign made of local signs.** Put $\epsilon(r,s)=\prod_t\delta(r(t),s(t))$, where $\delta$ is $+1$ when the black face lies to the left of the arrow. It replaces the complex phase $i^J$ up to the constant $i^{-n}$. Opus and Fable each found it while reviewing a draft, Sol checked it in the merged paper, and it now compiles in Lean. [Draft A review](../research/2026-11-14_opus_review-draft-A/REPORT.md), [draft B review](../research/2026-11-14_fable_review-draft-B/REPORT.md)

**Heights along paths of faces.** Fix a path of faces from every white face to $t_0$, and count with sign the black faces where the path turns around the chosen corner. Reversing a clockwise cycle raises the total by the number of white faces inside. This removes the spokes and the sliding argument of the OpenAI paper. Fable supplied the construction and Sol checked it in the merged paper. [Draft B review](../research/2026-11-14_fable_review-draft-B/REPORT.md), [main referee](../research/2026-11-14_sol_referee-main/REPORT.md)

**A finite difference in place of the exponential.** The $2^c$ orientations of a cover with $c$ cycles form a cube. The alternating sum of $\omega^m$ over it vanishes when $c>m$ and is a signed product of white-face counts when $c=m$. Sol checked the proof, and Opus then proved the lemma in Lean. A second form uses linear weights and one integer polynomial. Astra found it, Fable refereed it, and the Lean proof uses the same device. With our signed heights, $\sum\epsilon z^{\omega(s)}$ is a Laurent polynomial. Version 1 called it a polynomial and version 2 corrects that. [Blueprint report](../research/2026-11-14_opus_blueprint/REPORT.md), [determinant referee](../research/2026-11-14_fable_referee-determinants/REPORT.md)

**Connectivity inside a cycle.** Euler's formula needs a connected plane graph. Both drafts applied it to the inside of a cycle without proof. Fable supplied a five-line lemma, and Sol checked that the repair is not circular. [Draft B review](../research/2026-11-14_fable_review-draft-B/REPORT.md)

**An exact criterion for the first pair.** The constructive manuscript states that a pair exists exactly when no separating triangle has black faces along its inner side, the side away from $t_0$. Opus proved it from one Euler identity for induced subgraphs, and Sol checked both directions. So gluing is needed only at such triangles. [Integration, sections 1 and 2](../research/2026-11-14_sol_referee-structure/INTEGRATION.md)

**Which cycles the construction finds.** For fixed $t_0$ and $e_0$, different good states give different Hamiltonian cycles, and some cycles are missed. A cycle avoiding the edge yields a state, and the construction finds the cycle exactly when that state is good. Otherwise the state has no partner. On the hexagonal prism with $e_0$ on the equator there are three states, two of them good, and four cycles avoiding the edge. Astra and Fable proved this and Sol checked it. [Structure referee](../research/2026-11-14_sol_referee-structure/REPORT.md)

**Counts.** Write $g$ for the number of good states at a root, $\#TM$ in the reports, and $h$ for the number of Hamiltonian cycles of $G$. Then $3g\le h$ and $g\ge 2m$. Fable proved both and Astra checked them. In $G$, a cover is an edge set $S$ with prescribed local degrees, and its number of cycles is $\kappa(G-S)-1$, one less than the number of components. Astra proved this and Sol checked it. $S$ is not the matching that the proof deletes. [Combinatorics referee](../research/2026-11-14_astra_referee-combinatorics/REPORT.md), [cover referee](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md)

**Families.** The prism over a $2j$-gon has $2j+2$ Hamiltonian cycles, so no exponential lower bound in the number of vertices holds for the whole class. A graph with $b$ irreducible pieces has at least $2^b$ cycles avoiding any given edge and at least $3\cdot2^b$ in all. The cube has six, so six is sharp. Sol proved these. Their referee was a second Sol run, so no different model has checked them. [Families referee, F1 and F5](../research/2026-11-14_sol_referee-covers/REFEREE-families.md)

**Two smaller points.** To force a cycle through an edge at a cubic vertex, avoid another edge at that vertex. And the signed count is one coefficient of an integer determinant, whose positivity restates the theorem without proving it. [Older approaches](../research/2026-11-14_astra_older-approaches/REPORT.md), [determinant referee](../research/2026-11-14_fable_referee-determinants/REPORT.md)

## 4. The three papers connected

The dependency audit found no error in any of the three papers and one shared skeleton of fourteen steps, from the dual and its root through the first pair, the disk identity, the two cancellations and the recovery to gluing. [Skeleton](../research/2026-11-14_fable_dependency-graph/skeleton.md)

| Object | OpenAI | Li | Constructive manuscript |
|---|---|---|---|
| State | Bijection from triangles to corners | Perfect matching of the reduced incidence graph | Perfect matching of the incidence graph |
| Pair | Two disjoint states | Ordered 2-factor of the incidence graph | Pair of disjoint matchings |
| Bad second state | $Q_s$ has a cycle | The 2-factor is not cycle-breaking | Not a tree matching |
| Nonzero count | Lowest Taylor coefficient | Fixed objects of a second involution | Coefficient of an integer polynomial, or a marked walk |
| Recovery | Tree on white faces, two induced trees | Connected complement in $G$ | Incidence tree and rooted selection |

The papers differ in substance at four steps: how the first pair is found, the weights, the nonvanishing count, and the last step to one cycle. The [correspondence table](../research/2026-11-14_fable_dependency-graph/correspondence.md) gives exact translations, including the two conflicting uses of the letter $H$. OpenAI's paper and the constructive manuscript close as written. Li's note closes once four routine steps are supplied, the balance count for Ore's theorem and three checks in Appendix B. The involution companion writes out Li's general argument. It is Li's proof unpacked, not a new route. [Dependency report](../research/2026-11-14_fable_dependency-graph/REPORT.md), [involution referee](../research/2026-11-14_opus_referee-involutions/REPORT.md)

The Lean proof never uses faces or the Jordan curve theorem. It turns a drawing into an algebraic dual, treats the inside of a cycle as one shore of a bond of $G$, uses one flow and linear polynomial factors, recovers the cycle in $G$, and runs its induction on the avoided edge. It never states the two-induced-trees theorem and does not formalise the Pfaffian corollary. Opus built its 31 files, 8,936 lines, locally. The build prints only `propext`, `Classical.choice` and `Quot.sound`. [Lean report](../research/2026-11-14_opus_lean-formalisation/REPORT.md)

The blueprint compares the main paper with that build. It was extracted from version 1, and version 2 keeps the statement numbers. Of the 34 statements on the route, four have an exact Lean counterpart: the definitions of state and pair, the two reversals, and the max-flow step. Twenty-five have a counterpart in another form and rest on five translations that are written down but not formalised. Five have none: connectivity from faces bounded by cycles, the two induced trees, a component count, the sign as a product, and the finite difference. Statements match more often than proofs. Only ten proofs follow Lean's argument, and the paper glues two trees where Lean glues matchings. Nobody has reviewed the blueprint's judgements. [Blueprint](../proofs/blueprint/BLUEPRINT.md)

A later run by the same author closed part of that gap. In Lean's model it proves the sign as a product with both reversals, the cancellation with the real sign, the finite difference, and the nonvanishing step by $\epsilon\,\omega^m$. OpenAI's main theorem then rebuilds with its phase-and-polynomial lemma replaced by this one, on the same three axioms, and no longer uses the phase or the polynomial. Still unchecked: the heights as the paper defines them, since the Lean statement uses Lean's flow weights, and the two statements that need the Jordan curve theorem, connectivity from faces and the two induced trees. The blueprint is not yet updated, and no second model had finished reading the new statements against the paper. [Lean devices report](../research/2026-11-14_opus_lean-devices/REPORT.md), [blueprint delta](../proofs/lean/BLUEPRINT-DELTA.md)

## 5. Proof routes and failures

Sizes count vertices of $T$ unless marked primal. "First" means an exhaustive search found nothing smaller. "Witness" claims no minimality. The [route map](route-map/ROUTE-MAP.md) lists every refutation.

| Kind | What worked | What failed, and what remains |
|---|---|---|
| Combinatorial | Heights, reversal and finite differences give the refereed proof. | Choosing the highest or lowest state, or turning all cycles of a smallest cover one way, fails at 12 once reflections are counted. A 13-vertex instance has six good states and $m=2$, so good states do not split into cubes of four. [Referee](../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| Graph-theoretic | The exact pair criterion and the three-matroid description are refereed. Two-tree packing has a proof nobody has reviewed. | A two-matroid relaxation fails on the hexagonal prism, 8 vertices: four of its six solutions are not states. The linear program has a half-integral vertex at 13, a witness. A cover with no good state occurs at 16. [Determinants](../research/2026-11-14_fable_referee-determinants/REPORT.md), [structure](../research/2026-11-14_sol_referee-structure/REPORT.md), [packing](../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| Constructive | The lab enumerates, runs marked walks and recovers cycles. | No polynomial bound. Strict descent fails first at 16 for pairs and at 8 for rainbow trees. The surplus walk cycles at 38, a witness. A search over plateaus has not failed yet. [Lab](../workings/barnette_lab/README.md), [topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md) |
| Algebraic | Two equivalent determinants and the linear weights are refereed. | The plain determinant fails on the hexagonal prism, and doubled edges fail at 9. No sign change on incidences removes the cancellation, by a 13-vertex witness. The number of good states can vanish modulo 2, 3, 4, 5, 7 and 11, witnesses at 6, 13, 9, 14, 16 and 26. The algebra report is not reviewed. [Referee](../research/2026-11-14_fable_referee-determinants/REPORT.md), [algebra](../research/2026-11-14_sol_route-algebra/REPORT.md) |
| Topological | Signed angles give a Gauss-Bonnet reading of the disk identity, and a dual rank formula counts the cycles a selection leaves. Opus derived both and Fable refereed them. They are intuition, not a second proof. | The plain Euler characteristic loses the grading. The referee's own new results, that a rainbow tree exists and lies in a unique cover, are not reviewed. Exchange descent is open. [Topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md) |
| Probabilistic | Explicit families show that good states can be exponentially rare. | Positive weights on all spanning trees cannot match the target degrees, already on the cube, primal order 8. That excludes full-support measures only. Real roots and roots on the unit circle both fail at 12. Opus checked the degree obstruction, and otherwise only a second run of the author's model reviewed this. [Probability](../research/2026-11-14_sol_route-probabilistic/REPORT.md), [packing](../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| Categorical | Cutting along a cycle and recording a boundary pattern composes: 3 patterns on triangles, 6 on quadrilaterals, given the theorem. | On 5-cycles the patterns depend on the piece, witness at 9. Homology and Belyi maps gave vocabulary only. Not reviewed. [Report](../research/2026-11-14_fable_route-categorical/REPORT.md) |
| Inductive | Splitting of states, a lift criterion and a rotation are refereed. A one-sided induction step has a written proof. | The converse of the lift criterion fails at 11. "Some good state lifts" fails at 18. Selecting inward fails at 11, 13 and 14. Repair by the partner fails at 16, by one cycle at 17, by any reorientation of a fixed cover at 18. Lemmas G and X are open. [Referee](../research/2026-11-14_fable_induction-completion/REPORT.md), [later lemmas](../research/2026-11-14_astra_induction-lemmas/REPORT.md) |
| Lattice | Covers form a distributive lattice, and both cancellations have a reading on it. | Both extremes fail first at 18. "An extreme or an irreducible element" fails at a 33-vertex witness, which has a separating triangle. Without separating triangles that question is open. Levels with a fixed number of cycles can be disconnected, witnesses at 18. [Referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [covers](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md) |
| Non-planar | The Pfaffian corollary follows from the theorem through Gorsky, Steiner and Wiederrecht. | On the Heawood graph, 14 primal vertices, the cancellation survives but the count is zero. A direct proof is open. Not reviewed. [Report](../research/2026-11-14_astra_route-pfaffian/REPORT.md) |

![Route records by kind and recorded status](synthesis-figures/route-outcomes.png)

[Vector PDF](synthesis-figures/route-outcomes.pdf). The chart counts the records of [routes.py](route-map/routes.py). Keyword rules in [count.py](../research/2026-11-14_fable_synthesis-audit/count.py) give each record one kind, and the kinds overlap, so the rows are a rough guide. "Proved" joins source arguments and proofs written here, reviewed or not. "Open" joins conjectures and hunches.

## 6. Why the signed count seems necessary

This section is an interpretation. Nobody has proved that an unsigned proof is impossible.

Each half of the target is easy inside any cover. Opus's packing report proves that every cover contains a spanning tree of the white faces that meets the degree condition at the black faces, and another that meets it at the vertices. It even splits a cover into two trees of the second kind. A good state needs both conditions in one tree. These proofs are not reviewed. [Packing report](../research/2026-11-14_opus_two-tree-packing/REPORT.md)

A 16-vertex cover contains no good state. No reorientation of its cycles helps. The midpoint $(r+s)/2$ of any of its pairs satisfies the linear program and lies outside the convex hull of good states. So a method must sometimes leave the cover it started in. Choosing a canonical cover fails too, by the lattice counterexamples at 18 and 33. The signed count compares all covers at once and cancels the bad second states among them. Nothing we tried does that without signs. The refutations rule out named shortcuts, not every unsigned proof. [Structure referee](../research/2026-11-14_sol_referee-structure/REPORT.md), [lattice referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md)

## 7. Open problems, ranked

1. **Close the induction without the signed count.** Contract at a vertex of degree four. Lemma G asks that, without separating triangles and above 6 vertices, some such contraction stays simple and keeps a pair. It holds on all 62,416 rooted instances from 8 to 19 vertices. Lemma X asks, when both contractions at a vertex have good states, that some good state of a contraction is not exceptional, which gives a good state before contraction. The stronger inequality, that contraction never increases the number of good states, holds on 1,202,792 contractions through 18 vertices. Astra's later report proves G when there is no chordless 5-cycle and shows that every repair confined to one cover fails. The next step is a move that changes the cover. [Missing lemmas](../research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md), [later report](../research/2026-11-14_astra_induction-lemmas/REPORT.md)

2. **Prove at least $2^m$ good states.** It holds on all 4,656,948 rooted instances with a pair through 22 vertices, computed by Opus and reproduced by Sol with separate code. Astra's census without separating triangles reports no failure on 23,824,742 rooted faces through 24 vertices, and Sol replayed it through 16. The cases of one cover and of two covers are proved and refereed. Explicit families attain equality for every $m$, and $m$ is unbounded even without separating triangles. The next step is the two-cover calculation for more covers. An induction on levels with a fixed number of cycles cannot work, because such levels can be disconnected. [Conjecture referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [cover referee](../research/2026-11-14_sol_referee-covers/REFEREE-covers.md)

3. **Prove descent with plateaus.** There are two conjectures. Pair descent says that reversals reach a good pair without ever increasing the number of cycles of $Q_s$. Fable's descent study confirms it for all 49,325,864 pairs through 22 vertices. Every sharper rule it tried fails: strict descent first at 16, a lookahead of two moves first at 21, and 27 of 28 potentials. Rainbow descent says the same for exchanges on rainbow trees. It holds for every root through 17 vertices, for 1,485 of the 1,543 triangulations at 18, and in samples to 120. Neither study is reviewed. [Descent study](../research/2026-11-14_fable_descent/REPORT.md), [topology referee](../research/2026-11-14_fable_referee-topology/REPORT.md)

4. **Find a polynomial-time construction.** Testing one orientation of a cover is linear. Finding a good one among all covers has no polynomial bound. Sampling states at random cannot work in general, because good states can be exponentially rare even without separating triangles. [Conjecture referee](../research/2026-11-14_sol_referee-conjectures/REPORT.md), [families](../research/2026-11-14_sol_counting-families/REPORT.md)

5. **Prove the non-planar statement directly.** The Pfaffian corollary rests on the planar theorem and a structure theorem. Start from the Heawood graph, where the count vanishes. [Pfaffian report](../research/2026-11-14_astra_route-pfaffian/REPORT.md)

6. **Finish formalising our route.** The sign and the counting step are done. Next comes the bridge from the paper's heights to Lean's flow weights. The connectivity lemma and the two induced trees need a Jordan curve theorem, which Mathlib lacks. The paper could drop the second by gluing matchings as Lean does. [Lean devices report](../research/2026-11-14_opus_lean-devices/REPORT.md)

## 8. What the literature review established

These points summarise the project's library. Several older originals were never opened, and the list says which.

1. The target, two induced trees in the dual, is Stein's from 1971, in the form of Alt, Payne, Schmidt and Wood from 2016. Both were opened. [History](../research/2026-11-14_opus_history-literature/REPORT.md)
2. The version with an avoided edge and the reduction at separating triangles go back to Kelmans. His papers were not opened. We know them through Hertel's survey and through Alt and coauthors, whose PDFs sit in the history folder and not in the library.
3. States are the corner choices of Tutte's trinity theory, known here through Hine and Kálmán. The disk identity and the signed count over pairs appear in none of the 23 Barnette papers the history run collected. [Novelty note](../research/2026-11-14_astra_older-approaches/NOVELTY.md)
4. Earlier partial results cover faces of size four and six, leapfrog graphs and, in a preprint, faces of size at most eight. [Results table](../research/2026-11-14_opus_history-literature/RESULTS-TABLE.md)
5. The largest computer check before the proof reached 90 primal vertices, by Brinkmann, Goedgebeur and McKay in 2022. The source was opened. [Main referee](../research/2026-11-14_sol_referee-main/REPORT.md)
6. The machinery review separates eleven reformulations and ranks eighteen route ideas. [Report](../research/2026-11-14_sol_machinery-literature/REPORT.md)
7. A proposed link between the parity condition of Bagheri Gh., Feder, Fleischner and Subi and the black-inner triangle obstruction is false on the truncated octahedron. [Older approaches](../research/2026-11-14_astra_older-approaches/REPORT.md)
8. The constructive manuscript is unsigned. No author or public source was found. [Library report](../research/2026-11-14_astra_literature-consolidation/REPORT.md)
9. How the 1969 Waterloo proceedings attribute the conjecture is unresolved. The original page was not obtained, and the two drafts disagreed. [Index](../papers/INDEX.md)
10. The OpenAI proof is a preprint that no journal has refereed. A third party reports that two Lean kernels accept the formal proof, and our own build agrees.

## 9. What the earlier rewrite taught us

The lessons come from a study of an earlier rewrite of another paper and its [style guide](../research/2026-11-14_astra_exposition-method/STYLE-GUIDE.md) of 22 rules. [History of that rewrite](../research/2026-11-14_astra_exposition-method/HOW-THE-REWRITE-WORKED.md)

1. Remove proof obligations before shortening sentences.
2. Open with the obstacle, here connectivity, then bring in the object that answers it.
3. Define an object when the reader has a reason to want it.
4. Keep one main route and put algorithmic extensions elsewhere.
5. Say what each reversal changes and what it keeps.
6. Keep degree two and connectedness apart, each with its own reason.
7. Carry one example through every representation.
8. Put each figure next to the question it answers.
9. Keep quantifiers, domains and normalisations when cutting.
10. Compare rendered pages. A clean build does not show that the text is clear.

The merge followed these, and a cold reader still found the opening overloaded, three steps without their reason, and nine of thirteen floats cutting into a proof or a sentence. Version 2 answers that list with a five-step plan on page 1 and every figure placed outside proofs. [Cold read](../research/2026-11-14_fable_coldread-main/REPORT.md), [version 2 report](../research/2026-11-14_astra_main-revision/REPORT.md)

## 10. Review status and limits

"Refereed" means that a run of another AI model read a stated argument and, in most cases, wrote its own checking code. It is not journal review, human approval or formal verification. When a referee proves something new, that new result has no second reader.

| Work | Written by | Checked by | Not covered |
|---|---|---|---|
| OpenAI's Lean proof | OpenAI | Lean kernel, built locally by Opus | Our texts |
| Main paper, version 1 | Opus, merging drafts by Astra and Opus | Sol: follows, eight corrections. Fable: cold read, 40 edits | |
| Main paper, version 2 | Astra, then 17 finishing edits by Opus | Sol, on the final text: follows, eight small corrections. Opus: cold read, no mathematical problem | |
| Primal companion | Astra | Fable: follows, one gap closed. Opus: final review, accept | |
| Involution companion | Sol | Opus: follows, 15 edits. Fable, on the revision: follows, new lemma correct after a fix | |
| Blueprint | Opus | Nobody | The 25 matches in another form |
| Lean devices | Opus | Lean kernel | Whether each Lean statement says what the paper says |
| Weight-free proof, counts | Fable | Astra | |
| Pair criterion, gluing, recovery | Opus, Astra | Sol | |
| Determinants, linear weights | Sol, Astra | Fable | Parts of the lab |
| Topology | Opus | Fable | Fable's new rainbow results |
| Lattice conjectures | Opus | Sol | Sol's 33-vertex refutation |
| Induction | Opus | Fable | Fable's and Astra's later lemmas |
| Descent study | Fable | Nobody | |
| Cycle covers | Astra | Sol | The census from 17 to 24 vertices |
| Families, probability | Sol | A second Sol run. Opus checked one probability result | A different model, for the rest |
| Packing, algebra, category, Pfaffian | Opus, Sol, Fable, Astra | Nobody | |
| Step digestions | Fable | Astra, then Opus for names | |
| Atlas | Sol, rebuilt by Fable | Sol: 78 computed checks pass, wording errors on several pages. Fable applied the corrections | The rebuilt pages |
| This synthesis | Astra | Fable | |

Two disputes were settled by a model that was not a party, and referees corrected two sets of first-failure claims.

**Real sign against Lean's phase.** The primal referee warned that the two differ by a factor depending on the number of cycles. The reviser disagreed. Opus adjudicated for the reviser. The ratio is the constant $i^n$, or $i^{-n}$ if the corner order is reversed. The referee's formula was right and simplifies to that constant. Opus proved it, checked 24,856 pairs with its own code, and later proved it in Lean. [Adjudication](../research/2026-11-14_opus_cross-audit/ADJUDICATION.md)

**279 against 213 marked objects.** Two runs counted Li's marked objects on the running example and disagreed. Opus reproduced both. They use the same input and two drawings that swap the positions of roots 4 and 5. The count depends on the drawing: 69 drawings give 35 values from 103 to 363. The signed sum, $-9$, and the number of surviving objects, nine, never change. The same referee found one wrong sign in a side formula, for odd $m$, and the revision corrects it. [Discrepancy note](../research/2026-11-14_opus_referee-involutions/DISCREPANCY-279-213.md), [second referee](../research/2026-11-14_fable_referee-involutions-v2/REPORT.md)

**First failures.** A search that identifies mirror images cannot report first sizes for claims that depend on orientation. Counting reflections moved two counterexamples down to 12 vertices. Several saved "lattice extremes" were only greedy end points, and the true extremes fail together first at 18. [Combinatorics referee](../research/2026-11-14_astra_referee-combinatorics/REPORT.md), [structure referee](../research/2026-11-14_sol_referee-structure/REPORT.md)

## 11. Numbers and snapshot

<!-- inventory-start -->
The inventory was taken at 2026-11-14 13:48 UTC by [count.py](../research/2026-11-14_fable_synthesis-audit/count.py), with output in [counts.json](../research/2026-11-14_fable_synthesis-audit/counts.json). It counts folders and files. It reruns no census.

There are 69 run folders and 66 of them hold a final report. By folder name, 17 are GPT-6 Astra, 19 Fable 5.2, 16 Opus 5.5 and 17 GPT-6.1 Sol. The route map has 244 records: 46 arguments from the sources, 64 proofs written here, 13 computations, 19 conjectures, 25 hunches and 77 refutations. Those are recorded statuses, not review verdicts.

| PDF | Pages |
|---|---:|
| [Main paper, version 2, at the time of the count](../paper/main/barnette.pdf) | 19 |
| [Main paper, version 1](../paper/main/history/barnette-v1.pdf) | 18 |
| [Primal companion](../proofs/primal/primal.pdf) | 15 |
| [Involution companion](../proofs/involutions/involutions.pdf) | 18 |
| [Atlas](atlas/atlas.pdf) | 31 |

The eleven step files hold about 32,000 words, counting headings and link text.
<!-- inventory-end -->

The censuses cover different populations and must not be added up. The numbers are quoted from the reports, not rerun. [Ledger of computations](../research/2026-11-14_astra_synthesis/EVIDENCE.md)

| Claim tested | Range | Size | Computed by |
|---|---|---|---|
| At least $2^m$ good states | every root, to 22 vertices | 4,656,948 rooted instances with a pair | Opus, reproduced by Sol |
| The same, no separating triangle | to 24 vertices | 23,824,742 rooted faces | Astra. Sol replayed 3,374 through 16 |
| Pair descent | every root, to 22 vertices | 49,325,864 pairs | Fable, not reviewed |
| Rainbow descent | every root, to 17 vertices | 69,458,112 rainbow trees, the rest by a proposition | Fable, not reviewed |
| Lemma G | 8 to 19 vertices | 62,416 rooted instances | Fable. Astra's criterion agrees |
| Contraction inequality | to 18 vertices | 1,202,792 contractions | Fable |
| Sign against phase | to 16 vertices | 24,856 pairs | Opus |
| Main paper's identities | to 12 vertices | 262 rooted faces of 15 triangulations | Sol |

<!-- late-start -->
**Runs still open at this snapshot.** Three folders hold no final report: `astra_lean-check`, `fable_atlas-finish`, `fable_final-polish`. Nothing from them is counted as a result above.
<!-- late-end -->

## Housekeeping for the owner

Four decisions are yours.

1. **The author line.** The main paper has an empty `\author{}` and a comment that marks it for you.
2. **Third-party PDFs.** Two research folders hold 53 PDFs of other people's papers, about 50 MB: [machinery literature](../research/2026-11-14_sol_machinery-literature/pdf/) and [history literature](../research/2026-11-14_opus_history-literature/pdf/). The repository is private, but nobody established the right to redistribute them. The [cleanup proposal](../research/2026-11-14_opus_cross-audit/CLEANUP-PROPOSAL.md), items C3 to C5, suggests moving the few the proof uses into the library and replacing the rest by links. Decide before the repository is shared.
3. **The Lean build directory.** `E:\lbb`, about 7.7 GB, lies outside the repository. Delete it when no more Lean work is planned. The [Lean README](../proofs/lean/README.md) says how to rebuild it.
4. **Drafts A and B.** `paper/draft-A/` and `paper/draft-B/` are superseded by the main paper and kept as records. Leave them, or move them under a history folder.
