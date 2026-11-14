# Regression referee of version 2

Reviewer: gpt-6.1-sol, 14 November 2026. No subagents were used. The starting version is frozen in `code/outputs/v2-start.tex`; hashes are in `code/outputs/fingerprints.json`. The first corrected source/PDF commit is `d3b3651`. A concurrent finishing pass through `f04e0d1` was then checked, with one further correction committed as `e97b061`. This review covers that final source, frozen in `code/outputs/v2-final.tex`, and all 19 pages of its rebuilt PDF. The final hashes are in `code/outputs/build-verification.json`.

Status convention: the deductions and audit arguments here are **PROVED-HERE**. Finite checks are **COMPUTED**, with programs and exact ranges below. **LIT** means an identified source states the result, with publication status distinguished from supplied preprints. It does not certify the source's proof. No CONJECTURE or HUNCH discharges a dependency.

## Audit boundary

PROVED-HERE audit contract. The root is Theorem 1.1: for every finite simple cubic bipartite planar 3-connected graph G and each e in E(G), a Hamiltonian cycle avoids e. The supplied route proves the stronger dual induction contract, Theorem 6.2: every coloured simple sphere triangulation T, every face t0, and every side e0 of t0 admit an acyclic selection containing e0. Here a selection contains exactly one side of every face; T has at least four vertices and opposite face colours across every edge.

The source boundary is `paper/main/barnette.tex`, including its proofs and explanatory bridges. The sources and project reports supply attribution checks and checks of off-route remarks. They are not replacement proofs. In particular neither the original OpenAI theorem nor the Lean theorem is accepted as a premise of this audit.

Accepted background is the Jordan separation theorem for an embedded simple cycle, Euler's formula for a connected sphere graph, elementary plane dual construction and the cyclic order at a vertex, integral max-flow/min-cut on a finite integral network, and elementary finite graph theory and polynomial algebra. Graph facts accepted at this boundary include tree edge counts and unique paths, a finite connected 2-regular graph being a cycle, a nonempty finite even-degree graph containing a cycle, and even intersection of a cycle with an edge cut. A polygonal drawing of a finite planar graph is accepted. None of the disk identity, density bound, positive height increment, pair cancellation, or selection recovery is accepted without checking its proof here.

## Obligation graph

PROVED-HERE. Each arrow below is the primary sufficient AND route supplied by the paper. The two induction cases are both required, not competing OR routes. Induction hypotheses are restricted to strictly smaller orders. The only supplied alternative is the contraction proof of the forest-connectivity half of Lemma 2.5(2); it is checked separately and is not needed to repair the primary proof.

```text
T0, main theorem <- R0 AND H, D0, I0, H0, X0
I0, prescribed selection <- R1 AND WF, A0, B0
A0, nonseparating case <- R2 AND COL, P0, N0, R0c
B0, separating case <- R3 AND K0, IH, PRES, GLUE, H0
D0, valid dual <- R4 AND CUT, DUAL
H0, Hamiltonian complement and induced trees <- R5 AND CON, U0, CARD, HC

R0c, good-state recovery <- R6 AND Y0, O0, J0, MATCHDISK, ADDROOT
Y0, tree of faces and selection <- R7 AND S0, CON, U0, CHILD
S0, good iff augmented Q tree <- R8 AND CARD, QCOUNT
J0, disk identity <- R9 AND CON, REGION, BIJ, DISKCOUNT
O0, outdegree lemma <- R10 AND OUTCOUNT
CON, cyclic facial boundaries imply connected <- R11 AND OPEN
U0, cycle/forest duality <- R12 AND JORDAN, EVENBOUNDARY, EULERCOTREE
  U0 connectivity <- R12a supplied alternative AND CONTRACT

N0, pair gives good state <- R13 AND C0, SGN, V0, F0, CLASSES, MINIMUM
C0, fixed-second-state cancellation <- R14 AND M0, REV, SGN, FIXED
SGN, sign formula and flips <- R15 AND J0, LOCAL
REV, both reversals preserve pairs <- R16 AND M0, PERM
M0, partner structure and unique partner of good state <- R17 AND O0, PARTNER
V0, height increment equals enclosed white faces <- R18 AND U0, J0, PATH, CROSS
F0, finite difference formula <- R19 AND BOOLEAN

P0, first pair <- R20 AND FLOW, CUTALG, DENSITY
DENSITY, induced density bound <- R21 AND CON, CARD, TRIANGLES, BALANCE, SMALL
K0, smaller coloured caps <- R22 AND CON, CAPCOLOUR, CAPSIZE
```

The reused J0 node concerns cycles of chosen sides for a single state. It does not require a pair. M0 supplies the extra orientation that makes an acyclic Q good. N0 requires a pair but neither assumes goodness nor invokes recovery. R0c assumes goodness and proves recovery without invoking existence. These distinctions prevent circularity.

## Findings by severity

### Mathematical scope errors in the new summaries, corrected

PROVED-HERE, F1. Immediately before Proposition 3.9, v2 line 443 claimed that a cycle in P_s would be a cycle of chosen sides. The prescribed edge e0 is not a chosen side of a bounded black face. Only a cycle in P_s minus e0 has the asserted description. The actual proof already first excludes such cycles and then shows that adding e0 joins distinct rooted components. C4 in CHANGELOG restricts the introductory sentence. No theorem statement or inference needed replacement.

PROVED-HERE, F2. In the plan, fourth step, the reversal was said to pair off unsuitable second states. It fixes the second state and pairs its partners, so the cancelled terms can have the same second state. The new eight-pairs figure illustrates exactly this: the two shaded terms both have s=alpha. C2 corrects the object being paired.

PROVED-HERE, F3. The new abstract used "one side" without "exactly" and left the graph containing the connected complement implicit after moving into the dual. C1 makes both points explicit and states the iff. For a selection P, Lemma 2.5(1) gives the obstruction if P contains a cycle; Lemma 2.5(2) gives connected G minus P* if P is acyclic. Every vertex of G has two remaining edges. It is connectivity of this original graph complement that matters. The corrected sentence states exactly what Section 2 proves.

PROVED-HERE, F6, late finishing pass. Its expanded fourth plan step said that reversing one of the D cycles raises the weight. Only clockwise-to-counterclockwise reversal raises it; the inverse lowers it. C8 specifies a clockwise cycle. Lemma 4.6 and the new orientation-square arrows already use the correct direction. This is a summary error, not a failing proof node.

### Implicit dependencies and formalisation scope, corrected

PROVED-HERE, F4. All three blueprint suggestions remained in v2. C5 adds Lemma 3.8 where Proposition 3.9 names the disk identity. C6 cites Lemma 2.5(2) with M=T and N empty for the heights paragraph's path existence. T is connected by Lemma 2.2, so the premise holds for arbitrary coloured triangulations, including capped pieces. C3 changes both unnecessary "open disk" claims, in Lemma 2.5 and before Lemma 3.8, to connected open regions with boundary Z. Jordan supplies exactly this. This correction does not deny that polygonal Jordan curves bound disks; it removes the stronger conclusion from invocations that need only separation.

LIT and COMPUTED source-scope check, F5. The new sentence saying that OpenAI's Lean development proves Barnette's conjecture is supported by the retained build and `#print axioms OAI.Barnette.main`, which reports only `propext`, `Classical.choice`, and `Quot.sound`. It does not mean that the present exposition is checked line by line. C7 adds that distinction and names the two-induced-trees statement as an example without a formal counterpart. The blueprint's translations between plane triangulations and algebraic duals, local signs and phases, and heights and flow are informal. The standalone finite-difference proof is not connected to the upstream development. I inspected the retained logs and signatures, not a new Lean rebuild.

### No remaining blocking finding

PROVED-HERE. No changed theorem-like statement, proof, definition, formula, or caption leaves a failing dependency after these small corrections. No printed example number required correction. No wrong numbered citation or wrong resolved internal reference was found. The off-route results retain the strength established by their sources, with the limits specified below.

## Regression of statements, proofs, moves and references

COMPUTED inventory. `regression.py` scripts the theorem-like-environment and proof comparison, then inventories all displays, captions and references. There are 50 statement/proof blocks, 20 textually changed, 15 displays and 15 captions. `environments.diff` is the structured comparison; `full.diff` is the complete source diff. The final main-theorem proof is matched by its explicit title, not mistaken for a second proof of Theorem 6.2. Both diffs were read in full.

PROVED-HERE review of the changed blocks:

| Changed block | Check |
| --- | --- |
| Theorem 1.1 | Citation key only; graph hypotheses and edge prescription unchanged. |
| Lemma 2.1 proof | The explicit singleton and two-vertex cases give 3 and at least 4 outgoing edges; the remaining shores survive deletion of at most two cut endpoints. |
| Lemma 3.1 proof; Lemma 3.5 proof | c to o is consistent in both the root separation and the two added root edges. |
| Example 3.3 | Dot-separated face labels represent exactly the original ten triples; both state rows are unchanged bijections. |
| Lemma 3.6 proof | Root edges are ao,bo; the root degree and all other black degrees are unchanged. Sentence splitting changes no quantifier. |
| Lemma 3.7 and proof | F to directed E and q to nu are consistent. At most one outgoing edge is still the premise; component edge count is nu minus gamma. |
| Lemma 3.8 and proof | The now standalone statement supplies the state and directed chosen-side hypotheses formerly inherited from the preceding paragraph. The three counts are unchanged. |
| Example 3.10 | All numbers, trees and exhaustive-cycle assertions pass the new enumeration. |
| Lemma 4.2 proof | Root orientation and converse construction remain valid. |
| Lemma 4.4 proof | The expanded t arguments distinguish all three corners correctly. Each reversal changes one factor per cycle edge, an odd number. |
| Lemma 4.5 proof | The selected cycle still depends on s only. Splitting the sentence preserves that condition. |
| Lemma 4.6 proof | No sign or crossing convention changed. Entry and exit are counted through the same black face, visited at most once. |
| Lemma 4.7 proof | I to calligraphic I avoids collision with the interior-vertex count and changes no Boolean-monomial argument. |
| Example 4.9 | The added figure reference resolves to the new eight-pairs figure; counts and signs agree with it. |
| Remark 4.10 | Both the Laurent correction and the limited claim about efficient construction survive. See the eight-correction check below. |
| Proposition 5.2 proof | New equality explanation is 3p-6 minus p-2 = 2p-4. Root renaming and Psi renaming are consistent in every balance sum. No Phi/Psi mismatch remains. |
| Theorem 6.2 proof | Only sentence splitting; both induction calls are smaller, and the second still prescribes the first cap's selected side. |

PROVED-HERE display check. Of the 15 displayed formulas, 12 are byte-identical to v1 after newline normalization. The three changes are the face-table separators, the density sum's F to Psi, and the polynomial's F to Pi. Each preserves its mathematical content. The formula's leading sign in Section 7 is correct: the product of orientation differences contributes a minus sign for each clockwise cycle, converting the pair sign to (-1)^((n-c)/2). The substitution 1+xi kappa has first coefficient L(C), and only the minimum-cycle classes contribute in the first surviving degree.

PROVED-HERE movement check. The moved sign definition and proof now precede the reversal table. The table no longer mentions F before its introduction. D is introduced after the pair definition, and the local-pair caption explicitly says that D is defined below. The example's pair table precedes its arithmetic. The disk figure uses the already defined alpha and beta, and points forward only illustratively to the later pair figure. No proof relies on that figure. All complete proof blocks remain with their statements, with natural page breaks but no inserted figure or table. Overview and section-plan forward references are descriptions of later results, not assumptions in their proofs.

COMPUTED plus PROVED-HERE semantic reference check. `render_and_refs.py` resolves all 131 final `ref` and `eqref` uses, with auxiliary-file page, number, line and full sentence in `refs-review.txt`. I checked every sentence against its target, including part numbers and panel letters. All match. Relevant newly changed targets are Figure 7 for the local pair, Figure 8 for D(beta,alpha), Figure 10 for heights, Figure 11 for two groupings, Table 2 for all eight pairs, Lemma 3.8 for the disk identity and Theorem 6.2 for prescribed gluing. Statement numbering is stable; figure numbers change after the split local figure. At a page break an auxiliary-file page can precede the visible theorem heading, as for Lemma 4.7. The manuscript uses no pageref; its object numbers are correct.

### Additional concurrent finishing-pass check

PROVED-HERE and COMPUTED. `concurrent-finishing.diff` was read in full, separately from this referee's two source-edit commits. `final-environments.diff` and `final-source.diff` record the complete v1-to-final comparisons. The new cube warm-up is correct: its only cover is triangle 345 around one white face, its two pair weights differ by one, and its signed first moment is -1. Thus the weaker printed plus-or-minus-one claim is valid. The term "cover" names exactly the undirected edge set already used by the proof; the source's group is the class of pairs indexed by that set, so this naming introduces no new mathematical object or assumption.

PROVED-HERE. "Good state" and the unsigned manuscript's "tree matching" agree. Deleting the matching spokes from its full black-face incidence graph leaves two spokes at each bounded black centre and all three at the outer centre. Suppressing the degree-two bounded centres leaves Q_s plus the outer three-spoke star. This is a tree exactly when Q_s is a forest with the three roots in different components. This is precisely Definition 3.4. The new sentence is a correct attribution of terminology, not a stronger criterion.

COMPUTED and visual inspection. Figure 11 is now two orientation squares rather than two rows. Its left square has top-left, top-right, bottom-left, bottom-right weights -4,2,-3,3; the right has -2,1,-1,2. Their signs are +,-,-,+, horizontal increments are 6 and 3, and vertical increments are 1. The two shaded alpha boxes have weight 2 with opposite signs. Its printed equations 16-9-4+9=12=2*6*1 and 4-1-1+4=6=2*3*1 agree with Table 2 and the independent enumeration. Its new caption and the single-cycle explanation were read against Lemmas 4.6 and 4.7. The only needed correction was F6 above.

PROVED-HERE. The revised history still explicitly credits Hertel for the older history. The new root-orientation phrasing, condition wording, state-name explanation and the added reference to OpenAI Lemma 5.3 are accurate. The gluing caption correctly identifies the square trees' shared edge 35 and the disk trees' shared vertex 4, as checked from the rendered shapes. The flow figure now follows Proposition 5.2 and its proof, and the trimmed pair figure removes only a duplicate legend. No proof or definition is displaced. All 19 final pages were rendered and opened again after these changes. The plan's fifth step now continues at the top of p2; this is a page break within an overview list and has no mathematical effect. I made no expository or layout edits.

## The eight v1 corrections

All eight have been applied correctly. Mathematical assessments in this table are PROVED-HERE; finite witnesses are COMPUTED by this review's programs.

| v1 edit | v2 verification |
| --- | --- |
| E1 | Remark 4.10 says integer Laurent polynomial, distinguishes the unsigned source's nonnegative weights, and uses the polynomial binomial coefficient at negative exponents. The independent example gives z^-4-z^-3+z^-2-z^-1-z+z^3, with coefficient 9 at degree two in z-1, equal to Sigma/2!=18/2. |
| E2 | Pi nonzero is conditional on a pair, and the common leading sign is asserted only for minimum-cycle classes. |
| E3 | The recovery converse starts by assuming s_C good before calling Y a tree. The opposite direction uses the unique root orientation. This proves injection from good states, not from all Hamiltonian cycles to states. |
| E4 | The introduction says the table lists all eight pairs, without claiming it lists all twelve states. |
| E5 | The range is explicitly every facial root through 12 vertices. This review reruns the whole range and confirms the 9-vertex witness and lack of smaller ones. |
| E6 | The triangular-bipyramid radial graph's 3-connectivity proof covers 0,1,2 deleted face centres separately and leaves every surviving face centre attached. Independent code confirms order 11, class sizes 5 and 6, planarity and connectivity 3. |
| E7 | The three-cubes construction's one-vertex-deletion argument is present. Code confirms order 26, cubicity, bipartiteness, planarity, connectivity 2, and three components after deletion of the two added vertices. A Hamiltonian cycle minus two vertices has at most two components, so this graph is not Hamiltonian. |
| E8 | The sentence now denies an efficient construction from these nonvanishing calculations alone. It no longer denies finite constructive interpretations such as the unsigned manuscript's marked walk. |

## Independent numbers and rendered figures

COMPUTED. `verify_numbers.py` was written for this review and imports no project or previous referee code. It reads only the two oriented face fixtures. It reconstructs the primal graph, enumerates states and pairs, finds interiors by deleting the cycle's crossing dual edges, computes heights with a fresh sorted shortest-path search, reconstructs selections, and enumerates all primal perfect matchings to count Hamiltonian complements. The prism is generated independently as a six-gon bipyramid. The literal table and eight-box data are asserted in `supplement.py`.

| Object | Recomputed results |
| --- | --- |
| Cube dual | V=6, E=12, F=8; n=3; two states, both good; two pairs; six Hamiltonian cycles in total, two avoiding each root side. For the rendered state s=(5,3,4), the selected sides are 35,23,04 and 01, with components 014 and 235. |
| Running example | V=13, E=33, F=22, 11 faces of each colour, n=10, no separating triangle; 12 states, 8 pairs, 6 good states. There are 28 Hamiltonian cycles in all and exactly 6 avoiding the edge across 04. |
| Named states | alpha=(1,3,7,2,9,11,6,12,8,10); beta=(6,2,8,1,3,10,11,7,12,9). Q_alpha has exactly the cycle 189; Q_beta's components are 0137, 2489(10)(11), and 56(12). All twelve states were checked, so "only alpha" is literal. |
| Recovered beta | Eleven edges, components {0,2,4,6,7,8} and {1,3,5,9,10,11,12}; the Hamiltonian complement crosses the other 22 edges. |
| Disk | The directed 7-cycle 1,2,3,9,10,11,6 has B=5, W=6, I=3, ell=2; strictly interior vertices are 7,8,12. The marked inner-black edges are 12 and 9(10). |
| Pair classes | Cycle lengths 7 and 3 in both classes; white counts 6,1 and 3,1; m=2. Sorted cw/cw, cw/ccw, ccw/cw, ccw/ccw weights are -4,-3,2,3 and -2,-1,1,2. Signs are +,-,-,+. |
| Arithmetic | Moments 0,0,18. Class sums 16-9-4+9=12 and 4-1-1+4=6. Three positive and three negative surviving good-state signs. |
| Height figure | The face path 189,178,167,016,056,t0 is valid and shortest. Turn signs at 1 in 178 and 6 in 016 are + and -. The two displayed heights are -1 and 0. |
| Flow figure | Ten nonroots and ten bounded black faces; capacities 2,1,2; full flow value 20. Vertex 2 belongs to exactly 023 and 129, giving equality for S={2}. |
| Hexagonal prism | Dual V=8,E=18,F=12,n=5; three states, two good, two pairs; eight Hamiltonian cycles total; four avoid the equatorial prescribed side, two avoid either other root side. Both constructor outputs are distinct for every prescription. |
| Gluing figure | Two 6-vertex octahedra share three corners, giving 9 vertices. The rendered selections are {01,04,23,35} and {35,56,48,78}; their union has seven edges and components {0,1,4,7,8}, {2,3,5,6}. Their trees meet at edge 35 or vertex 4 as claimed. |

COMPUTED range checks. Beyond the displayed numbers, `supplement.py` tests all 12,288 chosen-side systems for the running example, all 16 for the cube and all 96 for the prism; their 5,076, 2 and 18 detected cycles satisfy all disk counts. It checks every D-cycle reversal's sign and every individual white-face height increment, fixed-s cancellation, multivariate polynomial regrouping, and the connected-complement iff for all 112, 9 and 20 primal perfect matchings respectively. These are finite regression checks, not substitutes for the proof.

COMPUTED census. Fresh `plantri -b -a N` calls for N=6,...,12 give class counts 1,0,1,1,2,2,8 and facial-root counts 8,0,12,14,32,36,160, totalling 15 classes and 262 roots. The v1 referee's 265 "rootings" included its three additional displayed-example calls and is not the census-only total. Every face was rooted, with colour chosen to make it black. Same-colour root dependence first occurs at order 9. Orders below 6 cannot be coloured simple triangulations: alternating face colours give even vertex degree, simplicity and triangular faces give degree at least 3, hence degree at least 4, and 2E=6V-12>=4V forces V>=6. Each piece at a separator has at least six vertices, so a separating example has at least 6+6-3=9. This also proves the minimality independently of the census.

COMPUTED and visual inspection. All 19 pages were rendered at 130 dpi and opened, including the bibliography. Figures 1 through 13 were checked from their rendered labels, not just their captions or generation code. The running labels 0 through 12, root labels, ten flow triples, long-cycle ordering, ringed interior vertices, two cancellation signs, height signs and all eight boxes agree with the inputs and recomputation above. The regenerated gluing labels 0 through 8 and shape classes agree with the independently entered selections. No missing glyph, clipped content, overlapping mathematical label or broken reference was observed. The final log has zero overfull boxes, zero undefined or multiply defined references and zero TeX errors. The PDF remains 19 pages.

## Closing remarks and bibliography

LIT source comparisons and PROVED-HERE deductions. The new closing text has the following strength; no optional research claim is silently promoted.

| Passage | Exact support and allowed strength |
| --- | --- |
| Differences from OpenAI: disk identity, connected region and recovery | The manuscript proves these steps. PROVED-HERE, no claim of new theorem. |
| Real local sign; heights as path counts | Unsigned manuscript Section 4 and Li Section 4 are supplied preprints. The local-sign formula is proved here. OpenAI Lemma 5.3 on PDF p7 constructs circulations by dual paths; our corner potentials are this construction read through each black triangle. The height proof supplies the needed increment directly. |
| Removal of spokes/sliding; finite difference replacing exponential sum | OpenAI Section 5.3, PDF p7, has the spoke detour and sliding argument and the exponential product. The present Lemmas 4.6 and 4.7 replace those devices. It is the finite difference, not positivity alone, that proves nonvanishing. |
| Face tree as black dual trace plus a leaf | Li Definition 28 and Lemma 30, Section 6, PDF pp10-11. Suppressing the degree-two black nodes gives the same tree on white nodes; reinstating them gives Li's trace on G minus b0, and adding t0 gives the extra leaf. |
| Which cycles arise and injection | PROVED-HERE by the good-state-scoped argument now in Section 7. Its prism and running-example claims are COMPUTED here. The stronger mate criterion in `sol_referee-structure/INTEGRATION.md` is consistent but is not claimed or needed in this paper. |
| Hypothesis examples | The two expanded connectivity arguments are PROVED-HERE and independently COMPUTED here. The historical 46-,38-,50-vertex claims are LIT, not new enumerations. |
| Separator criterion | Anonymous Theorem 1.2, PDF p2, has precisely the rooted black-inner-boundary obstruction. The independent structure referee supplies a full matching proof of the same criterion. It is not a claim that all separating triangles obstruct a pair. The census/minimality range is independently replayed here. |
| Polynomial | PROVED-HERE by the paper's cancellation and its orientation expansion; independently compared as an exact monomial dictionary on all three examples. The pair-existence condition remains explicit. |
| Enumeration bound | Anonymous Section 6.1, Lemma 6.1 and Proposition 6.2, PDF pp11-12. M<=3^(n/2) and O(n^3 M), with n=|V(G)|/2-1, give the stated polynomial-times-3^(|V(G)|/4) bound. The paper correctly attributes this claim and does not rely on it. Source algorithm stops at the first tree matching; continuing its same finite search enumerates them within the same total-prefix bound. This review checks the bound's transcription, not a full new referee of the algorithm. |
| No known polynomial constructor | Open problem in the supplied constructive and research accounts. Neither a finite marked walk nor efficient verification of a proposed pair proves a polynomial search algorithm. This is an absence-of-known-result statement, not a complexity lower bound. |
| Pfaffian consequence and new decomposition explanation | GSW Theorem 4.16, v3 pp12-13, equivalence (i) to (v), and OpenAI Corollary 7.2, PDF p10. The chain uses planar P4-Hamiltonicity, cubic Pfaffian braces via trisums, and general cubic graphs via tight cuts. GSW's published theorem is accepted at the stated named-theorem boundary; the known typos in its gluing proof are not re-certified here. |
| Same-face inclusion/avoidance; arbitrary edges | Hertel Theorem 10 and Corollary 3, PDF p7, and Alt Section 5. Distinctness is now explicit. The two-arbitrary-edges version remains CONJECTURE in these accounts; the paper does not assert it as a consequence of P4-Hamiltonicity. |
| Lean and two companion notes | The upstream main theorem's retained axiom output supports ordinary Barnette. The stronger edge-avoidance result is formalised for algebraic duals but not restated for drawings. Not every statement or route of this exposition is checked. The two project notes exist in proofs/primal and proofs/involutions; their existence and methods, not formal certification of their entire contents, are asserted. |

PROVED-HERE source-boundary check. The lattice-extreme and irreducible claims are absent from v2. Thus it does not contradict the independently checked order-18 failure of extremes or the order-33 failure of extrema-or-irreducibles in `sol_referee-conjectures/REPORT.md`. Cycle-cover census claims and the unbounded-minimum-cover families are also absent. In particular v2 does not mislabel the source's order-24 census as independently verified beyond order 16. Those reports were read for this check; none supplies a premise for the main proof.

LIT bibliographic check. The 17 cited entries all produce bibliography items, with no missing cite key. Their rendering on p19 was inspected. All numbered source citations were checked against the local primary texts:

| Citation | Checked location and result |
| --- | --- |
| OpenAI Theorem 1.1, Corollary 7.1 | Supplied PDF pp1,10: ordinary theorem and avoidance strengthening, exactly the finite simple cubic bipartite planar 3-connected contract. |
| Hertel Corollary 3 | PDF p7: universal edge-avoidance equivalence. |
| GSW Theorem 4.3 | v3 PDF p7: same universal H-minus equivalence. |
| Alt Lemma 5 | PDF p3: Hamiltonian dual iff two disjoint permeating induced subtrees partition the vertices. |
| Anonymous Theorem 1.2 | PDF p2: exact pair criterion, including chosen outer black face. |
| GSW Theorem 4.16; OpenAI Corollary 7.2 | v3 PDF pp12-13; supplied PDF p10: three-edge simple paths in cubic 3-connected bipartite Pfaffian graphs. |
| OpenAI Lemma 5.3 and Section 5.3 | Both on PDF p7; the lemma's location is Section 5.2, while the spoke sliding is in 5.3. The paper cites each correctly. |
| Li Sections 4,6 and Appendix C | Path/ray crossing counts, black dual trace, and cut gluing respectively; the labels and roles match. |
| Alt Section 5 | Kelmans's reduction to the absence of nontrivial three-edge cuts is the topic cited. |

LIT existence/metadata checks. The three 2026 texts are supplied manuscripts, not invented published journal articles; Anonymous has no invented author. The local primary PDFs also establish existence of Hertel, Alt, GSW, Stein, Hine-Kalman, Feder-Subi, Schnieders and Brinkmann-Goedgebeur-McKay. Ford-Fulkerson's primary record and theorem were inspected in the supplied consolidation, whose exact DOI is 10.4153/CJM-1956-045-5. The inherited 64 versus 90 distinction is correct: Hertel explains HMM's 64 bound; BGM Theorem 4.1 gives 90, with publication year 2022 and preprint year 2021. Schnieders is correctly an arXiv preprint, not a refereed theorem claim. Feder's ECCC cover says report 15 of 2006 even though the manuscript title page is dated January 2004; the bibliography cites the report's year.

LIT online spot checks for originals not held here: the [Holton-McKay publisher record](https://www.sciencedirect.com/science/article/pii/0095895688900755) confirms the 38-vertex statement and 45(3),305-319,1988; the [Tutte publisher record](https://academic.oup.com/jlms/article-abstract/s1-21/2/98/2194241) confirms s1-21(2),98-101,1946. The [Akiyama-Nishizeki-Saito author-hosted original](https://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J029.pdf) states exactly the two-connected cubic bipartite planar NP-completeness claim. The [BGM primary publisher page](https://doi.org/10.1090/mcom/3701) identifies Georges's 1989 article, DOI 10.1016/0095-8956(89)90012-9, and the independently discovered 50-vertex example. Full proofs of Tutte, Georges and Holton-McKay were not opened in this review. This is an existence and citation check, not a new certification of their historical computations. The unresolved Barnette1969 attribution flagged in MISMATCHES.md is not cited in v2.

LIT final metadata follow-up. Although direct DOI opens failed, publisher search located both missing records directly: [Georges at Elsevier](https://www.sciencedirect.com/science/article/pii/0095895689900129), whose abstract gives a cyclically four-edge-connected bicubic 50-vertex counterexample, and [Ford-Fulkerson at Cambridge](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/maximal-flow-through-a-network/5D6E55D3B06C4F7B1043BC1D82D40764), confirming Canadian Journal of Mathematics 8,399-404,1956 and its DOI. Neither metadata entry is merely inferred from an unavailable source.

## Dependency table

PROVED-HERE. The exact obligations below discharge the graph from its leaves. Each obligation has one classification. Nonprimitive claim nodes link to their checked AND route. All statuses concern the corrected v2 proof, not the literature's independent proof status.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T0 | Every G in the contract has a Hamiltonian cycle avoiding any prescribed e | root | R0 | root | D0,I0,H0,X0 | discharged |
| H | G finite simple cubic bipartite planar 3-connected; e an edge | T0,D0 | R0,R4 | hypothesis | Theorem 1.1 | discharged |
| X0 | e0 crossing e lies in P, hence e lies in deleted matching P* | T0 | R0 | definition | Final proof, dual crossing correspondence | discharged |
| D0 | The embedded dual is a coloured simple triangulation with at least four vertices | T0 | R4 | major claim | Lemma 2.1, CUT,DUAL | discharged |
| CUT | G has no cut of one or two edges | D0 | R4 | algebraic/logical step | Shores of order 1 or 2 have >=3 or >=4 outgoing edges. Larger shores survive deletion of cut endpoints, contradicting vertex connectivity. | discharged |
| DUAL | No dual loop/parallel pair; triangular boundaries, size and colouring | D0 | R4 | algebraic/logical step | Such a closed curve would cross a cut of size <=2. Cubicity gives length-three facial walks, simplicity makes triangles. Euler gives V(T)=2+V(G)/2>=4. The bipartition supplies face colours. | discharged |
| I0 | Every coloured T and facial side e0 have a containing acyclic selection | T0 | R1 | major claim | Theorem 6.2, WF,A0,B0 | discharged |
| WF | Strong induction on finite order is valid, with separating/nonseparating cases exhaustive | I0 | R1 | side condition | Positive integer order; K0 ensures strict decrease | discharged |
| A0 | I0 in the absence of a separating triangle | I0 | R2 | major claim | COL,P0,N0,R0c | discharged |
| COL | Exchanging face colours makes t0 black without changing selections or e0 | A0 | R2 | definition | Selection does not mention colours | discharged |
| B0 | I0 in the presence of a separating triangle | I0 | R3 | major claim | K0,IH,PRES,GLUE,H0 | discharged |
| IH | Each strictly smaller capped piece has a selection for any facial prescription | B0 | R3 | hypothesis | Strong induction hypothesis, invoked only after K0 | discharged |
| PRES | t0 is retained on one side; the first cap selects exactly one edge e', prescribed on the second cap | B0 | R3 | side condition | t0 facial; separator has vertices on both sides; cap is a face in each child | discharged |
| GLUE | Union is a selection and has no cycle crossing pieces | B0 | R3 | algebraic/logical step | Only common selected edge is e'. By H0 its two ends are in one induced tree, third root in the other. Any mixed cycle would give a length>=2 path between boundary corners within a piece, contrary to their unique allowed edge path. | discharged |
| H0 | Acyclic selection gives Hamiltonian complementary dual and two induced tree components | T0,B0 | R5 | major claim | Proposition 2.6, CON,U0,CARD,HC | discharged |
| CARD | k black faces, k white, 3k edges, k+2 vertices; selection has k edges | H0,S0,N0,P0 | R5 | algebraic/logical step | Triangular side counts, one face of each colour per edge, CON and Euler | discharged |
| HC | Complement is connected 2-regular; no unselected edge has ends in one P component | H0 | R5 | algebraic/logical step | U0 gives connectivity. A missing intra-component edge would close a primal cycle whose dual cut meets the Hamiltonian cycle once, violating cut parity. Forest count gives two components. | discharged |
| CON | Cyclic facial boundaries force connectivity of a finite sphere graph | H0,J0,DENSITY,K0 | R11 | major claim | Lemma 2.2, OPEN | discharged |
| OPEN | Union of one component and its incident faces is nonempty, open and closed | CON | R11 | algebraic/logical step | Connected boundary lies in one component; local vertex/edge neighbourhoods and face interiors make both complementary unions open; sphere connectedness | discharged |
| U0 | Cycles disconnect the complementary dual; forests leave it connected; tree gives cotree | H0,Y0,V0 | R12 | major claim | Lemma 2.5, JORDAN,EVENBOUNDARY,EULERCOTREE | discharged |
| JORDAN | A simple cycle separates into two nonempty regions, with dual steps changing sides exactly across it | U0,J0 | R12 | named theorem | Jordan curve theorem and definition of crossing dual edges; both adjacent facial regions occur | discharged |
| EVENBOUNDARY | A disconnected complementary dual yields a nonempty even boundary-edge set contained in N | U0 | R12 | algebraic/logical step | Choose a component of dual faces. Membership changes evenly in each vertex rotation. Connected primal M makes the boundary nonempty. Its cycle contradicts acyclic N. | discharged |
| EULERCOTREE | Complement of a spanning tree has F(M)-1 dual edges | U0 | R12 | named theorem | Euler for connected M, tree has V(M)-1 edges; use connectivity already proved | discharged |
| CONTRACT | Contracting a spanning tree containing the forest also proves dual connectivity | U0 connectivity | R12a supplied alternative | named theorem | Forest extends to spanning tree of connected M. Contract its nonloop edges successively; primal contraction deletes the crossing dual edges. Dual of the resulting one-vertex sphere graph is connected. Restoring deleted edges preserves this. | discharged |
| R0c | Good state gives an acyclic selection containing e0 | A0 | R6 | major claim | Proposition 3.9, Y0,O0,J0,MATCHDISK,ADDROOT | discharged |
| Y0 | Face tree gives one selected side per face, containing s(t) in each bounded black t | R0c | R7 | major claim | Lemma 3.6, S0,U0,CHILD | discharged |
| S0 | Good s iff S_s=Q_s plus ao,bo is a spanning tree | Y0 | R8 | major claim | Lemma 3.5, QCOUNT | discharged |
| QCOUNT | Q_s has n distinct edges on n+3 vertices; its forest has three components | S0 | R8 | algebraic/logical step | Unique black owner of each edge; adding ao,bo creates no cycle exactly when all three roots are in different components | discharged |
| CHILD | In rooted Y_s each black node has one child, each white node has a black parent | Y0 | R7 | algebraic/logical step | Tree/cotree U0; black degree two except t0 degree one; colours alternate. Each white node's parent edge is selected and no other incident side is. | discharged |
| O0 | At most one outgoing edge forces directed cycles and nu-gamma edge component count | R0c,M0 | R10 | major claim | Lemma 3.7, OUTCOUNT | discharged |
| OUTCOUNT | A cycle has as many distinct tails as vertices; a connected component has >=nu-1 edges | O0 | R10 | algebraic/logical step | Summed outdegrees equal nu-gamma; gamma is 0 or 1; tree or unicyclic respectively | discharged |
| MATCHDISK | A cycle of P_s minus e0 forces W-B=3, contrary to J0 giving 1 | R0c | R6 | algebraic/logical step | P_s matches faces. ell black and h-ell white faces are matched outside the disk, the rest in opposite-colour pairs; hence B-ell=W-h+ell | discharged |
| ADDROOT | Adding e0 after excluding cycles does not close one | R0c | R6 | algebraic/logical step | Outdegree one on X and zero on roots, together with O0, gives exactly one root per forest component; e0 joins distinct components | discharged |
| J0 | A chosen-side directed cycle obeys W=B+1 and h=2ell+3 | R0c,SGN,V0 | R9 | major claim | Lemma 3.8, REGION,CON,BIJ,DISKCOUNT | discharged |
| REGION | All roots are outside; inside graph has exactly the inner T faces and exterior face, each with cyclic boundary | J0 | R9 | side condition | Every cycle vertex is nonroot; closure of t0 is connected and disjoint from the cycle. Jordan separation identifies the exterior; all interior edges are retained. Apply CON before Euler. | discharged |
| BIJ | Interior black faces correspond to all I interior vertices and ell boundary tails | J0 | R9 | algebraic/logical step | Injectivity avoids repetition; surjectivity hits each interior vertex, whose incident face is inside. On the boundary its unique outgoing chosen edge identifies exactly its black owner. | discharged |
| DISKCOUNT | Euler and signed side count plus B=I+ell imply the two identities | J0 | R9 | algebraic/logical step | B+W=2I+h-2 and 3(B-W)=2ell-h. Substitute to obtain h=2ell+3 and W-B=1. | discharged |
| M0 | Partner orients Q_s into rooted trees or root-free unicyclic components; good state has one partner | C0,REV | R17 | major claim | Lemma 4.2, O0,PARTNER | discharged |
| PARTNER | Every nonroot is the tail of one Q edge; conversely rooted tree orientation defines a disjoint state | M0 | R17 | algebraic/logical step | r bijective; opposite side avoids s(t). Tree orientation forces the unique tail choices and uses each nonroot once. | discharged |
| REV | Both Q and D reversals preserve the two bijections and are involutive | C0 | R16 | major claim | Lemma 4.3, PERM,M0 | discharged |
| PERM | The cycle's heads and tails are the same distinct vertex set | REV | R16 | algebraic/logical step | Replacing all tails by heads on Q or swapping r,s on D merely permutes each affected image set; differing choices stay distinct | discharged |
| SGN | Reversals negate eps; eps=(-1)^((n+c)/2+c+) | N0,C0 | R15 | major claim | Lemma 4.4, LOCAL,J0 | discharged |
| LOCAL | Each changed local factor negates; the count of negative factors has the displayed parity | SGN | R15 | algebraic/logical step | Triangle cyclic orders; J0 makes lengths odd and delta sums +/-3. Sum (h-3)/2 over clockwise and (h+3)/2 over counterclockwise cycles. | discharged |
| C0 | All pairs with cyclic second Q cancel for every function of the second state | N0 | R14 | major claim | Lemma 4.5, REV,SGN,M0,FIXED | discharged |
| FIXED | Choose the reversal cycle using s alone; involution has no fixed point and keeps the weight | C0 | R14 | side condition | Fixed order on finite T cycles. Same s means same cycle after reversal; local choices really change. Good s has its unique partner. | discharged |
| V0 | Clockwise-to-counterclockwise reversal increases eta(y) by the interior indicator and omega by positive L(C) | N0 | R18 | major claim | Lemma 4.6, PATH,CROSS,U0,J0 | discharged |
| PATH | Each fixed simple face path from white y to t0 exists and visits any black face at most once | V0 | R18 | side condition | U0 with N empty after CON gives G connected. Take a simple path; black faces in A are not path endpoints. | discharged |
| CROSS | Local kappa difference is +1 on exiting the counterclockwise interior and -1 on entering; increments add | V0 | R18 | algebraic/logical step | Check the two side choices in a black triangle on either side of C. Side changes telescope to the starting interior indicator; J0 gives at least one white face. Distinct cycles use disjoint black faces. | discharged |
| F0 | c-fold alternating difference kills degree m<c and gives (-1)^c c! product L_i at m=c | N0 | R19 | major claim | Lemma 4.7, BOOLEAN | discharged |
| BOOLEAN | Only Boolean monomials containing all c indices survive; at degree c there are c! such terms | F0 | R19 | algebraic/logical step | Factor alternating sum by index; missing index contributes 1-1. Applies also to empty index set and degree zero with empty product conventions. | discharged |
| N0 | A pair guarantees a good state | A0 | R13 | major claim | Proposition 4.8, C0,SGN,V0,F0,CLASSES,MINIMUM | discharged |
| CLASSES | Fixed undirected D has exactly 2^c pairs and affine orientation weight | N0 | R13 | algebraic/logical step | D has one edge per black face and indegree/outdegree one on X. Reversing just one incident edge duplicates an r or s value, so changes must cover whole cycles. REV realizes all choices. V0 gives positive independent increments. | discharged |
| MINIMUM | Nonempty pair set defines m>=1; only c=m classes survive and have a common nonzero sign | N0 | R13 | side condition | Finite nonempty pair set, X nonempty since V(T)>=4 and CARD. F0 kills c>m. SGN gives n congruent m; each minimal contribution is (-1)^((n-m)/2)m! product L_i. At least one exists, all products positive. C0 then forces a good state. | discharged |
| P0 | No separating triangle guarantees a pair | A0 | R20 | major claim | Proposition 5.2, FLOW,CUTALG,DENSITY | discharged |
| FLOW | Stated cut inequality supplies integral 2n flow, split into two disjoint perfect matchings | P0 | R20 | named theorem | Integral max-flow/min-cut with capacities 2,1,2. Both size-n vertex classes saturate; degree-two bipartite components are even cycles, split alternately. | discharged |
| CUTALG | Minimizing over triangle positions gives Hall inequality equivalent to e(U)-b(U)<=2|U|-4 | P0 | R20 | algebraic/logical step | Each face contributes min(2,3-j)=2-max(0,j-1); unique black ownership counts e(U), with the three edges and one face of t0 restored separately | discharged |
| DENSITY | Every U containing the roots obeys the required density inequality | P0 | R21 | major claim | TRIANGLES,BALANCE,SMALL,CON | discharged |
| TRIANGLES | For a connected induced component with p>=4, length-three faces are exactly original T faces on its vertices | DENSITY | R21 | side condition | Simple connected graph has no facial walk of length <3 here. A triangular facial side has another H vertex on the other side; no separating triangle excludes interior T vertices, and simplicity excludes extra boundary-only edges. | discharged |
| BALANCE | Every nontriangular face region satisfies bal<=d-4 and summing yields q-b_H<=2p-4 | DENSITY | R21 | algebraic/logical step | Signed boundary count 3bal=sum of d signs, with bridge occurrences counted twice. Parity gives bal=0 at d4, +/-1 at d5; magnitude bounds d>=6. Sum face balances on the sphere, side count, Euler for connected H. | discharged |
| SMALL | Small components obey q-b_H<=2p; root component at p3 has q3,b_H1 and equality 2p-4 | DENSITY | R21 | algebraic/logical step | Simplicity gives q<=p(p-1)/2. All roots belong to the same component because t0 joins them. Summing the strong root-component bound and weaker other bounds suffices. | discharged |
| K0 | Capped separator pieces are smaller valid coloured triangulations | B0 | R22 | major claim | Lemma 6.1, CON,CAPCOLOUR,CAPSIZE | discharged |
| CAPCOLOUR | Each side's three boundary incidences have the same colour | K0 | R22 | algebraic/logical step | 3(B-W) equals three boundary signs; divisibility forces all equal. The opposite cap colour restores alternation. | discharged |
| CAPSIZE | Piece simple, connected, at least four vertices and strictly smaller | K0 | R22 | side condition | Subgraph simplicity; cyclic triangular facial boundaries give CON. Each shore has an interior vertex, one retained and one omitted. | discharged |

## Verdict

**FOLLOWS.** PROVED-HERE: T0 closes through D0, I0 and H0. Both induction cases close. The decisive shared nodes J0, C0, V0, F0, DENSITY and R0c are discharged without a hidden hypothesis, circularity or unbridged route switch. The corrections repair new summary scopes and expose existing dependencies; they do not replace the proof. This is an independent regression audit of the corrected version 2, with finite and literature checks limited to the ranges and source boundaries stated above.
