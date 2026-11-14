# Claims and sources

This synthesis asserts no new mathematical theorem. Tags below describe the underlying claim type, not a promotion of its review status. The prose cites the report that establishes the claim and the referee where available. Every cited source was read; no mathematical census was rerun here.

| Claim group | Protocol status | Review and source |
|---|---|---|
| Supplied signed-count route | LIT | Supplied preprints, not externally peer-reviewed; [main AI referee](../2026-11-14_sol_referee-main/REPORT.md). |
| Disk balance, height argument, count bounds | PROVED-HERE | Existing proofs accepted by [combinatorics referee](../2026-11-14_astra_referee-combinatorics/REPORT.md). No new proof here. |
| Exact pair criterion, gluing, recovery image | PROVED-HERE | [Structure referee](../2026-11-14_sol_referee-structure/INTEGRATION.md). |
| Mixed determinants and linear weights | PROVED-HERE | [Determinant referee](../2026-11-14_fable_referee-determinants/REPORT.md). |
| Turning and Morse readings | PROVED-HERE | [Topology referee](../2026-11-14_fable_referee-topology/REPORT.md); its new rainbow lemmas have no further review. |
| Packing and induction additions | PROVED-HERE | Author-written proofs, unreviewed; [packing](../2026-11-14_opus_two-tree-packing/REPORT.md), [induction](../2026-11-14_astra_induction-lemmas/REPORT.md). |
| Canonical choices, matroid relaxations, gauges, lifting, lattice extremes | REFUTED | Exact scope and smallest-known versus proved-minimum distinctions retained in synthesis section 5 and linked reviews. |
| Exponential bound, monotone descent, induction G and X | CONJECTURE | Tests and ranges in synthesis section 7; no general proof claimed. |
| Why signed counting seems necessary | HUNCH | Explicit interpretation in synthesis section 6, not an impossibility theorem. |
| Reported census sizes and product inventory | COMPUTED | [count.py](count.py), [evidence.py](evidence.py); source outputs extracted, not mathematical computations replayed. |
| Phase adjudication | PROVED-HERE; COMPUTED | [Cross-audit](../2026-11-14_opus_cross-audit/ADJUDICATION.md), independent proof and own code. |
| New involution path model | PROVED-HERE | [Author revision](../2026-11-14_sol_involutions-revision/REPORT.md); independent new-lemma review pending at writing. |
| Cover identity and two-cover bound | PROVED-HERE | [Cover referee](../2026-11-14_sol_referee-covers/REFEREE-covers.md). Large census independently replayed only through order 16. |
| Family counts | PROVED-HERE; COMPUTED | [Families referee](../2026-11-14_sol_referee-covers/REFEREE-families.md); exact transfer replay distinct from larger census and decimal asymptotics. |
| Formal finite difference | COMPUTED | [Blueprint report](../2026-11-14_opus_blueprint/REPORT.md), own compilation; surrounding translations remain informal. |

## Paragraph and table-row traceability

The excerpt identifies a paragraph or table row in SYNTHESIS.md. Its links support the complete block. Recommendations are editorial judgments. Lists in the exposition-method section inherit that section's two explicit sources.

| Block | Opening words | Sources |
|---|---|---|
| C001 | A Hamiltonian cycle has two jobs: use exactly two edges at each vertex, and connect all vertices. | [Source](../../paper/main/barnette.pdf), [Source](../../digestions/steps/01-degree-two-and-connectivity.md) |
| C002 | The dual $T=G^*$ has triangular faces coloured black and white. Choose one black face as the outside; | [Source](../../digestions/steps/03-states-and-pairs.md) |
| C003 | The key planar fact is a disk count. A directed cycle made from state choices encloses exactly | [Source](../../digestions/steps/04-disk-identity.md) |
| C004 | Now count pairs with signs and weights. First hold the second state $s$ fixed. If $Q_s$ contains | [Source](../../digestions/steps/05-cancellation.md), [Source](../../digestions/steps/06-nonvanishing.md) |
| C005 | A forest pair gives an incidence tree, then a tree on white faces. Root that tree and | [Source](../../digestions/steps/07-recovery.md), [Source](../../digestions/steps/08-gluing-and-hypotheses.md) |
| C006 | The history review identifies the new mechanism as the disk identity coupled to this two-way signed count. | [Source](../../research/2026-11-14_opus_history-literature/REPORT.md), [Source](../../digestions/route-map/HOW-IT-WORKS.md) |
| C007 | The merged exposition keeps the geometry in $T$, replaces complex phases by local signs, replaces spoke circulations | [Source](../../research/2026-11-14_opus_manuscript-merge/REPORT.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C008 | The diagram shows source and evidence relationships. The companion texts explain the same signed mechanism in different | [Source](../../research/2026-11-14_fable_dependency-graph/correspondence.md) |
| C009 | !Products and their supporting evidence | [Source](../../digestions/synthesis-figures/products.png) |
| C010 | Vector PDF. | [Source](../../digestions/synthesis-figures/products.pdf) |
| C011 | / Main paper / Opening, dual target, corner choices, disk count, paired count, initial pair and gluing. | [Source](../../paper/main/barnette.pdf) |
| C012 | / Proof blueprint / Statement-level correspondences to the papers and Lean, with explicit translation gaps. / | [Source](../../proofs/blueprint/README.md) |
| C013 | / Primal companion / A complete route in $G$, using cut shores, a charge flow and direct | [Source](../../proofs/primal/README.md) |
| C014 | / Involution companion / Li's general multi-mark argument written out as two finite involutions. / | [Source](../../proofs/involutions/README.md) |
| C015 | / Step digestions / Longer proofs, worked examples and failed alternatives at each step. / | [Source](../../digestions/steps/00-overview.md) |
| C016 | / Route map / Routes organized by the obligation they address; begin with how it works. / | [Source](../../digestions/route-map/ROUTE-MAP.md), [Source](../../digestions/route-map/HOW-IT-WORKS.md) |
| C017 | / Atlas / Computed pictures of the routes, not independent proofs. / | [Source](../../digestions/atlas/README.md) |
| C018 | / Labyrinth / Structured claims, dependencies, evidence and unresolved frontiers. / | [Source](../../labyrinth/README.md) |
| C019 | / Reference lab / Enumerate states and pairs, evaluate counts, recover cycles and check certificates. / | [Source](../../workings/barnette_lab/README.md) |
| C020 | / Library / Sources, access status, bibliography and links to their uses. / | [Source](../../papers/INDEX.md) |
| C021 | / Figures / Shared graph objects and drawings; polish report records checks. / | [Source](../../paper/figures), [Source](../../research/2026-11-14_sol_figures-polish/REPORT.md) |
| C022 | Write $\#TM$ for the number of tree-matching states at the chosen facial root, $\#HC$ for all Hamiltonian | [Source](../../research/2026-11-14_sol_referee-covers/INTEGRATION.md) |
| C023 | **Read the disk identity as a face balance.** For chosen-edge cycles, $W=B+1$ says what the arithmetic measures. | [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| C024 | **Multiply local signs.** Set $\epsilon(r,s)=\prod_{t\in A}\delta(r(t),s(t))$, where $\delta$ records direction around the black triangle. This replaces the | [Source](../../research/2026-11-14_opus_review-draft-A/REPORT.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C025 | **Define heights where needed.** Paths of faces from the outside define signed crossing counts. Summing heights over | [Source](../../research/2026-11-14_fable_review-draft-B/REPORT.md), [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| C026 | **Use finite differences or one polynomial.** Orienting a cover's $c$ cycles gives a Boolean cube. Alternating over | [Source](../../research/2026-11-14_fable_referee-determinants/REPORT.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C027 | **Supply inside connectivity.** Euler on everything inside a cycle requires a connected plane graph. Draft B left | [Source](../../research/2026-11-14_fable_review-draft-B/REPORT.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C028 | **Read the disk count as turning.** Signed angles give a Gauss-Bonnet account of the identity. Fable accepted | [Source](../../research/2026-11-14_fable_referee-topology/REPORT.md) |
| C029 | **Make pair existence exact.** The Euler region identity is $e-b-(2p-4)=\frac12\sum_F(\beta(F)-d(F)+4)$. A connected induced subgraph has $p$ vertices, | [Source](../../research/2026-11-14_sol_referee-structure/INTEGRATION.md) |
| C030 | **Cut only where necessary.** The exact obstruction permits gluing only at black-inner separating triangles. In primal language, | [Source](../../research/2026-11-14_sol_referee-structure/INTEGRATION.md) |
| C031 | **Say which cycles recovery finds.** For a fixed prescription, recovery is injective but need not be surjective. | [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md) |
| C032 | **Translate counts back to $G$.** For the admissible primal deletion $S$ corresponding to a cover $D$, $c(D)=\kappa(G-S)-1$. | [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-covers.md), [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| C033 | **Obtain inclusion from avoidance.** To include an edge at a cubic vertex, avoid a different incident edge. | [Source](../../research/2026-11-14_astra_older-approaches/REPORT.md) |
| C034 | **Keep the determinant's qualification.** The signed count is a squarefree face coefficient of a mixed determinant. Fable | [Source](../../research/2026-11-14_fable_referee-determinants/REPORT.md) |
| C035 | A useful answer to "how many cycles in $G$?" is now available for specific families. For the | [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-families.md) |
| C036 | The dependency audit isolates fourteen shared nodes: dual and root; balanced incidence graph; first pair; disk identity; | [Source](../../research/2026-11-14_fable_dependency-graph/skeleton.md) |
| C037 | The correspondence table gives exact translations, including conflicting uses of $H$. Four points differ materially: first pair, | [Source](../../research/2026-11-14_fable_dependency-graph/correspondence.md), [Source](../../research/2026-11-14_fable_dependency-graph/skeleton.md) |
| C038 | The audit found OpenAI and the constructive route closed within its boundary. Li needed the balance count | [Source](../../research/2026-11-14_fable_dependency-graph/REPORT.md), [Source](../../research/2026-11-14_opus_referee-involutions/REPORT.md) |
| C039 | Lean obtains an algebraic dual from a drawing, uses root-free bond shores in $G$, one charge flow | [Source](../../research/2026-11-14_opus_lean-formalisation/REPORT.md), [Source](../../proofs/primal/DICTIONARY.md) |
| C040 | The late blueprint pins its extraction to a committed manuscript, rather than silently mixing revisions. It distinguishes | [Source](../../research/2026-11-14_opus_blueprint/REPORT.md), [Source](../../proofs/blueprint/FORMALISATION.md) |
| C041 | Unless marked primal, sizes below count vertices of $T$. "First" means the cited exhaustive range establishes minimality; | [Source](../../digestions/route-map/ROUTE-MAP.md) |
| C042 | / Combinatorial / Heights, reversal and finite differences give a checked proof. / Highest/lowest-state and uniform-direction shortcuts | [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| C043 | / Graph-theoretic / structural / Exact pair criterion and three-matroid formulations are checked. Two-tree packing has an | [Source](../../research/2026-11-14_fable_referee-determinants/REPORT.md), [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md), [Source](../../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| C044 | / Constructive / algorithmic / Enumeration, marked walks, recovery and recursion have implementations. / No polynomial-time bound. | [Source](../../workings/barnette_lab/README.md), [Source](../../research/2026-11-14_fable_referee-topology/REPORT.md) |
| C045 | / Algebraic / determinantal / Equivalent mixed determinants and linear weights are checked. / Raw determinants fail | [Source](../../research/2026-11-14_fable_referee-determinants/REPORT.md), [Source](../../research/2026-11-14_sol_route-algebra/REPORT.md) |
| C046 | / Topological / Turning number and dual rank explain disk and recovery. Corrected Morse reading passes review. | [Source](../../research/2026-11-14_fable_referee-topology/REPORT.md) |
| C047 | / Probabilistic / Packing gives a feasible fractional point; explicit families show exponential rarity. / Positive full-support | [Source](../../research/2026-11-14_sol_route-probabilistic/REPORT.md), [Source](../../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| C048 | / Categorical / Boundary-pattern vectors compose across cuts: three triangular patterns, six allowed quadrilateral patterns, conditional on | [Source](../../research/2026-11-14_fable_route-categorical/REPORT.md) |
| C049 | / Inductive / Splitting, conditional lift criterion and rotation pass review. One-sided induction has a written proof. | [Source](../../research/2026-11-14_fable_induction-completion/REPORT.md), [Source](../../research/2026-11-14_astra_induction-lemmas/REPORT.md) |
| C050 | / Lattice-theoretic / Alpha-orientation lattice and decorated ideals describe the objects and cancellations. / Both extremes fail | [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md), [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-covers.md) |
| C051 | / Non-planar / Pfaffian / The corollary follows through Gorsky-Steiner-Wiederrecht; six trisum path signatures support gluing. / | [Source](../../research/2026-11-14_astra_route-pfaffian/REPORT.md) |
| C052 | !Kinds of route by recorded outcome | [Source](../../digestions/synthesis-figures/route-outcomes.png) |
| C053 | Vector PDF. Counts come from routes.py, with one editorial primary kind per record, assigned by explicit rules | [Source](../../digestions/synthesis-figures/route-outcomes.pdf), [Source](../../digestions/route-map/routes.py), [Source](../../research/2026-11-14_astra_synthesis/count.py), [Source](../../research/2026-11-14_astra_synthesis/route-classification.json) |
| C054 | This is an interpretation, not an impossibility theorem. The packing report proves that every pair support contains | [Source](../../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| C055 | The 16-vertex support with no tree matching makes the obstruction concrete. Reorienting its cycles cannot create the | [Source](../../research/2026-11-14_opus_two-tree-packing/REPORT.md), [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md), [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md) |
| C056 | The signed count compares supports while cancelling bad fixed states. This explains its current role and leaves | [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| C057 | 1. **Close the induction without borrowing cancellation.** G asks whether every separator-free rooted triangulation above order 6 | [Source](../../research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md), [Source](../../research/2026-11-14_astra_induction-lemmas/REPORT.md) |
| C058 | 2. **Prove $\#TM\geq2^{c_{\min}}$.** Independently reproduced all-root evidence covers 4,656,948 feasible instances through order 22. The separator-free author | [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md), [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-covers.md) |
| C059 | 3. **Prove monotone descent with plateaus.** Pair descent asks for allowed reversals reaching a forest without increasing | [Source](../../research/2026-11-14_fable_referee-topology/REPORT.md), [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md) |
| C060 | 4. **Find a polynomial-time constructor.** Testing a specified direction choice is easy; finding one across arbitrary supports | [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md), [Source](../../research/2026-11-14_sol_counting-families/REPORT.md) |
| C061 | 5. **Prove the non-planar statement directly.** Replace planar positivity in the Pfaffian setting without importing the structural | [Source](../../research/2026-11-14_astra_route-pfaffian/REPORT.md) |
| C062 | 6. **Formalize this exposition's route.** The upstream theorem is built, but face-path heights, the geometric inside lemma | [Source](../../research/2026-11-14_opus_blueprint/REPORT.md), [Source](../../research/2026-11-14_opus_lean-formalisation/REPORT.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C063 | 1. Stein's two-induced-trees formulation predates the supplied proof. History 2. Edge avoidance and separator reduction also have | [Source](../../research/2026-11-14_opus_history-literature/REPORT.md), [Source](../../research/2026-11-14_astra_older-approaches/REPORT.md), [Source](../../research/2026-11-14_opus_history-literature/REPORT.md), [Source](../../research/2026-11-14_opus_history-literature/RESULTS-TABLE.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md), [Source](../../research/2026-11-14_sol_machinery-literature/REPORT.md), [Source](../../research/2026-11-14_astra_older-approaches/REPORT.md), [Source](../../research/2026-11-14_astra_literature-consolidation/REPORT.md), [Source](../../papers/INDEX.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C064 | These lessons come from the floating-proof reconstruction and style guide. | [Source](../../research/2026-11-14_astra_exposition-method/HOW-THE-REWRITE-WORKED.md), [Source](../../research/2026-11-14_astra_exposition-method/STYLE-GUIDE.md) |
| C065 | The merge applies local signs, face-path heights and the inside lemma. Its cold reader still found an | [Source](../../research/2026-11-14_opus_manuscript-merge/REPORT.md), [Source](../../research/2026-11-14_fable_coldread-main/REPORT.md) |
| C066 | "Refereed" here means another AI model read a specified argument and, where recorded, wrote its own checking | [Source](../../research/2026-11-14_sol_referee-main/REPORT.md), [Source](../../research/2026-11-14_fable_referee-primal/REPORT.md), [Source](../../research/2026-11-14_opus_referee-involutions/REPORT.md) |
| C067 | Corrections matter. Reflection lowers two counterexamples to order 12. True lattice extremes replace mislabeled facial terminals, then | [Source](../../research/2026-11-14_opus_cross-audit/ADJUDICATION.md), [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md), [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md), [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md), [Source](../../research/2026-11-14_astra_primal-revision/REPORT.md) |
| C068 | The involution referee resolves 279 versus 213 marked objects: two drawings swap root anchors 4 and 5. | [Source](../../research/2026-11-14_sol_involutions-revision/REPORT.md), [Source](../../research/2026-11-14_astra_main-revision/CHANGES.md), [Source](../../research/2026-11-14_opus_referee-involutions/REPORT.md), [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C069 | Separate reviews remain missing for the new induction lemmas, packing theorems, algebra extensions, categorical investigation, direct Pfaffian | [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-families.md), [Source](../../research/2026-11-14_astra_induction-lemmas/REPORT.md), [Source](../../research/2026-11-14_opus_two-tree-packing/REPORT.md), [Source](../../research/2026-11-14_sol_route-algebra/REPORT.md), [Source](../../research/2026-11-14_fable_route-categorical/REPORT.md), [Source](../../research/2026-11-14_astra_route-pfaffian/REPORT.md), [Source](../../research/2026-11-14_sol_counting-families/REPORT.md), [Source](../../research/2026-11-14_fable_referee-topology/REPORT.md), [Source](../../digestions/atlas/README.md), [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-covers.md) |
| C070 | The late families review also corrects the Florek comparison's degree parameter and hypothesis, and distinguishes a published | [Source](../../research/2026-11-14_sol_referee-covers/REPORT.md) |
| C071 | For a human check, I recommend the main paper, for the complete explanatory route; the main referee, | [Source](../../paper/main/barnette.pdf), [Source](../../research/2026-11-14_sol_referee-main/REFEREE.md), [Source](../../research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md), [Source](../../research/2026-11-14_astra_induction-lemmas/REPORT.md) |
| C072 | The script records its timestamp, report hashes, product pages and chart assignments in counts.json. It counts run | [Source](../../research/2026-11-14_astra_synthesis/count.py), [Source](../../research/2026-11-14_astra_synthesis/counts.json), [Source](../../research/INDEX.md) |
| C073 | <!-- inventory-start --> At 2026-11-14T12:58:26.541101+00:00, the inventory has 59 run folders and 55 delivered REPORT files, including | [Source](../../research/2026-11-14_astra_synthesis/counts.json) |
| C074 | / paper/main/barnette.pdf / 19 / | [Source](../../paper/main/barnette.pdf) |
| C075 | / proofs/primal/primal.pdf / 15 / | [Source](../../proofs/primal/primal.pdf) |
| C076 | / proofs/involutions/involutions.pdf / 17 / | [Source](../../proofs/involutions/involutions.pdf) |
| C077 | / proofs/blueprint/blueprint.pdf / 1 / | [Source](../../proofs/blueprint/blueprint.pdf) |
| C078 | / proofs/blueprint/columns.pdf / 1 / | [Source](../../proofs/blueprint/columns.pdf) |
| C079 | / digestions/atlas/atlas.pdf / 31 / | [Source](../../digestions/atlas/atlas.pdf) |
| C080 | These six PDFs total 84 pages, including two one-page blueprint diagrams. Drafts, archived versions and individual figure | [Source](../../research/2026-11-14_astra_synthesis/count.py) |
| C081 | The computation ledger gives each largest cited census by claim, with its own population and review scope. | [Source](../../research/2026-11-14_astra_synthesis/EVIDENCE.md), [Source](../../research/2026-11-14_astra_synthesis/evidence.py) |
| C082 | The largest independent all-root exponential-bound check covers 4,656,948 feasible roots through dual order 22. The larger separator-free | [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md), [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-covers.md), [Source](../../research/2026-11-14_fable_referee-topology/REPORT.md) |
| C083 | <!-- late-start --> The closing scan incorporated the induction-lemmas report, topology referee, finished cover and families referee | [Source](../../research/2026-11-14_astra_synthesis/late-scan.json) |

## Retained negative routes

REFUTED entries below are copied from the route map snapshot. Their labels do not refute broader unnamed routes. The full scope, counterexample and source locator are retained in routes.py.

| Route | Rejected proposal | Source locator |
|---|---|---|
| S0.x1 | drop bipartite | lim/HYPOTHESES.md; examples/K4.json, Tutte46.json |
| S0.x2 | drop 3-connectivity | lim/HYPOTHESES.md; examples/theta_cube_26.json |
| S0.x3 | other surfaces | lim/HYPOTHESES.md; examples/torus_3x3.json |
| TG.x1 | trees from colour classes | APSW 2016 (limitation theorem); hist/WHAT-WAS-HARD.md 5 |
| TG.x2 | Grinberg obstruction | hist/WHAT-WAS-HARD.md 2; gt/PROOFS.md (Grinberg's identity is automatic for two induced trees) |
| A.x1 | every avoiding cycle comes from a tree matching | posed in dep/skeleton.md A2; refuted by comb/ROUTES.md 12 (E8) and lim/examples/prism_recovery.json |
| B.x1 | drop bijectivity | lim/examples/nonbijective_disk.json |
| C.x1 | sign as a product of two dimer weights | mach/REFORMULATIONS.md 3; con/ALGORITHMS.md; dim/PROOF.md 6 |
| K.x1 | choose the cycle using r | lim/HYPOTHESES.md (disk identity and bijectivity) |
| N.x1 | zero, vertex-only or face-only weights | lim/data/zero_weights.json; dim/PROOF.md 6; alg/PROOF.md 1 |
| N.x2 | parity or mod p count without weights | comb/ROUTES.md 8; dep/skeleton.md D3; alg/PROOF.md 2; alg/TABLES.md (residues mod 2, 3, 4, 5, 7, 11) |
| N.x3 | tree pair among the fewest-cycle pairs | dep/skeleton.md D2; comb/ROUTES.md 7 (E2d, E3); refc/REFEREE.md; gt/ROUTES.md O3 (a 40-vertex one-cycle cover with no tree pair) |
| N.x4 | highest or lowest partnered state | comb/ROUTES.md 4 (E1, E1c); refc/REFEREE.md; gt/ROUTES.md O1 (extremes of the whole matching lattice fail at 10 vertices) |
| N.x5 | minimal cover, all cycles one way | comb/ROUTES.md 5 (E2, E2c); refc/REFEREE.md |
| N.x6 | largest rank difference | comb/ROUTES.md 6 (E5) |
| N.x7 | one cycle always suffices | comb/ROUTES.md 13 |
| N.x8 | cubes of tree matchings; sign = parity of rank | comb/ROUTES.md 9, 10 |
| N.x9 | ordinary determinant, all face variables 1 | con/ALGORITHMS.md, data/exact_determinant.json; dim/IDENTITIES.md |
| N.x10 | allow doubled edges (standard double dimers) | dim/PROOF.md 3; dim/ROUTES.md |
| N.x11 | positive semidefinite blocks | alg/PROOF.md 4; comb/ROUTES.md 3 |
| N.x12 | Combinatorial Nullstellensatz | alg/PROOF.md 1 |
| N.x13 | real stability of the tree-state polynomial | alg/PROOF.md 3 |
| U.x1 | matching matroid meets graphic matroid | mach/REFORMULATIONS.md 6; con/data/other_candidates.json; refd/REFEREE-constructive.md |
| U.x2 | unconstrained white spanning trees | dim/ROUTES.md; con/ALGORITHMS.md (wilson_candidate) |
| U.x3 | trinity arborescences = tree matchings | dim/ROUTES.md (trees and trinity) |
| U.x4 | Yutsis partition of G | mach/REFORMULATIONS.md 11 |
| R.x1 | a forest state is enough | lim/HYPOTHESES.md (forest versus rooted forest); dep/correspondence.md 3.5 |
| G.x1 | prescribe whatever each cut needs | Bagheri Gh. et al. 2022, proof of Thm 4.6; hist/WHAT-WAS-HARD.md 6 |
| U.x5 | LP relaxation of the three constraints is integral | gt/ROUTES.md M1-M4; posed in mach/ROUTE-IDEAS.md 5 |
| U.x6 | induction by degree-4 expansion | gt/ROUTES.md I1; gt/PROOFS.md |
| U.x7 | positivity of the norm or of the Laplacian terms | refd/REPORT.md; alg/PROOF.md 6 |
| U.x8 | tree count as an unrooted invariant | alg/REPORT.md; alg/invariants.json |
| N.x14 | single-swap descent on the number of Q-cycles | gt/ROUTES.md D1, D2 |
| N.x15 | a global sign gauge on incidences | alg/PROOF.md 2; alg/REPORT.md |
| D.7 | extremes of Felsner's lattice of pairs | rc/REFEREE.md; rc/data/v18.json; rc/data/census_18.json |
| D.x1 | the partner of a tree matching is a tree matching | topo/REPORT.md item 5 |
| G.x2 | a uniform boundary condition for longer cuts | cat/PROOF.md Prop. 4; cat/EXPERIMENTS.md |
| A.x2 | two roots instead of a root face | cat/REPORT.md (what failed); cat/CATEGORICAL.md |
| K.x2 | the two cube structures form a bicomplex | cat/REPORT.md (what failed) |
| U.x9 | topological Hall for partial tree matchings | cat/REPORT.md (what failed) |
| D.ext1 | distance one from a lattice extreme | rc/REFEREE.md; rc/data/r1.json |
| D.ext2 | R2: extreme or irreducible | rc/LATTICE-READING.md Section 6; rc/data/R2_glued_V33.json |
| TG.parity | BF21 parity equals black-inner obstruction | older/BRIDGES.md; older/REPORT.md |
| N.rank-dead | signed sum as base-lattice rank polynomial | rc/LATTICE-READING.md; rc/data/examples.json |
| D.level-dead | fixed-cycle-count flip connectivity | covers/data/levels.json; covers/PROOFS.md |
| U.lift-dead | some contracted tree matching lifts directly | ri/data/nolift_18.jsonl; ri/REFEREE.md |
| U.walk-dead | surplus walk always terminates | reft/RAINBOW.md; reft/data/ |
| U.mean-dead | positive full-spoke UST mean fitting | prob/PROOFS.md Sections 1-3 |
| U.support-dead | joint Lorentzian rounding | prob/PROOFS.md; prob/code/campaign.py |
| N.zeros-dead | universal analytic root locations | prob/PROOFS.md; prob/code/secondary.py |
| N.heawood | root-free torus nonvanishing | pf/PROOFS.md; pf/data/results.json; pf/data/verification.json |
| U.ind-R1 | induction R1: Lift lemma, only-if half (route-graph-theory PROOFS Lemma 6. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R2 | induction R2: Degree-4 contraction preserves the existence of a pair | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R3 | induction R3: Every TM of T/M lifts to a TM of T | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R4 | induction R4: Failing lifts are compensated within the same type (B >= b) | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R5 | induction R5: Some TM of T/M satisfies the local condition LC (edge a v in | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R6 | induction R6: rho(lift) is a TM for every failing lift | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R7 | induction R7: TM(T) >= 2 TM(T/M) | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R8 | induction R8: lowest coefficient lc = sum over D with c_min cycles of prod | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R9 | induction R9: c_min(T) = c_min(T/M) (when both have pairs) | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R10 | induction R10: Skein relation TM(T) = TM(T/M) + TM(T/N) (both merges define | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R11 | induction R11: Prescribed corner: for every face t in A and non-root corner | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R12 | induction R12: A good contraction (result has a pair) always exists | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R13 | induction R13: Inverse P-operation (Batagelj) preserves pairs | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.loads-dead | rainbow loads are M-convex | reft/RAINBOW.md; reft/data/loads_sampled_6_13.json |
| D.chain-dead | every maximal lattice chain hits success | rc/REFEREE.md; rc/data/r3.json; rc/data/R2_glued_V33.json |
| D.fraction-dead | at least half the lattice succeeds | rc/REFEREE.md; rc/data/r5.json; rc/data/R2_glued_V33.json |

Source: [routes.py](../../digestions/route-map/routes.py). Folder abbreviations resolve through its FOLDERS table.
