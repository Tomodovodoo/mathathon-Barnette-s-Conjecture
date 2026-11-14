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
| C001 | Snapshot of 14 November 2026. GPT-6 Astra wrote this document, Fable 5.2 checked every claim against its | [Source](../../research/2026-11-14_fable_synthesis-audit/FACT-CHECK.md), [Source](../../research/2026-11-14_opus_synthesis-final/CHANGELOG.md), [Source](../../research/2026-11-14_opus_reconcile/FACTS.md), [Source](../../research/INDEX.md) |
| C002 | !Products, their sources and who checked them | [Source](../../digestions/synthesis-figures/products.png) |
| C003 | Vector PDF. | [Source](../../digestions/synthesis-figures/products.pdf) |
| C004 | / Main paper / Version 2, 20 pages. Refereed in both versions. Version 1, 18 pages, is | [Source](../../paper/main/barnette.pdf), [Source](../../paper/main/history/barnette-v1.pdf) |
| C005 | / Primal companion / 15 pages. The whole proof in $G$, without the dual, close to the | [Source](../../proofs/primal/primal.pdf) |
| C006 | / Involution companion / 18 pages. Li's argument for general $m$, written out as two sign-reversing involutions. | [Source](../../proofs/involutions/involutions.pdf) |
| C007 | / Sign-free note / 11 pages. What can be proved without signs, and where that stops. Refereed | [Source](../../proofs/sign-free/sign-free.pdf) |
| C008 | / Proof blueprint / Each statement of the main paper beside its counterparts elsewhere and in Lean. | [Source](../../proofs/blueprint/BLUEPRINT.md) |
| C009 | / Lean devices / 866 lines of Lean for the paper's sign and counting step, section 4. | [Source](../../proofs/lean/README.md) |
| C010 | / Step digestions / Eleven files with longer proofs, worked examples and failed alternatives for each step. | [Source](../../digestions/steps/00-overview.md) |
| C011 | / Route map / 246 route records sorted by the step they address. Start with how it | [Source](../../digestions/route-map/ROUTE-MAP.md), [Source](../../digestions/route-map/HOW-IT-WORKS.md) |
| C012 | / Atlas / 34 pages of computed pictures of 30 routes. Readings of one proof, not 30 | [Source](../../digestions/atlas/atlas.pdf) |
| C013 | / Labyrinth / Claims and their dependencies as structured data. / | [Source](../../labyrinth/README.md) |
| C014 | / Reference lab / Code that enumerates states and pairs and recovers cycles. / | [Source](../../workings/barnette_lab/README.md) |
| C015 | / Library / 87 sources with access status, and a bibliography. / | [Source](../../papers/INDEX.md) |
| C016 | **The disk identity as a face balance.** For a directed cycle of chosen sides, $W=B+1$. It needs | [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| C017 | **A sign made of local signs.** $\epsilon(r,s)=\prod_t\delta(r(t),s(t))$, where $\delta$ is $+1$ when the black face lies left | [Source](../../research/2026-11-14_fable_review-draft-B/REPORT.md) |
| C018 | **Heights along paths of faces.** Fix a path of faces from every white face to $t_0$, and | [Source](../../research/2026-11-14_sol_referee-main/REPORT.md) |
| C019 | **A finite difference in place of the exponential.** The $2^c$ orientations of a cover with $c$ cycles | [Source](../../research/2026-11-14_fable_referee-determinants/REPORT.md) |
| C020 | **An exact criterion for the first pair.** A pair exists exactly when no separating triangle has black | [Source](../../research/2026-11-14_sol_referee-structure/INTEGRATION.md) |
| C021 | **Which cycles the construction finds.** For fixed $t_0$ and $e_0$, different good states give different Hamiltonian cycles, | [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md) |
| C022 | **Counts.** With $g$ good states at a root and $h$ Hamiltonian cycles, $3g\le h$ and $g\ge 2m$, | [Source](../../research/2026-11-14_sol_referee-covers/REFEREE-covers.md) |
| C023 | **Families.** The prism over a $2j$-gon has $2j+2$ Hamiltonian cycles, so no exponential lower bound in the | [Source](../../research/2026-11-14_fable_referee-families/INTEGRATION.md) |
| C024 | The dependency audit found no error in the three papers and one shared skeleton of fourteen steps. | [Source](../../research/2026-11-14_fable_dependency-graph/skeleton.md) |
| C025 | The papers differ at four steps: the first pair, the weights, the nonvanishing count and the last | [Source](../../research/2026-11-14_fable_dependency-graph/correspondence.md), [Source](../../research/2026-11-14_fable_dependency-graph/REPORT.md) |
| C026 | The Lean proof never uses faces or the Jordan curve theorem. It uses an algebraic dual, one | [Source](../../research/2026-11-14_opus_lean-formalisation/REPORT.md) |
| C027 | Opus's 866 further lines check, in Lean's model: the local sign and its closed formula; $\epsilon = | [Source](../../research/2026-11-14_astra_lean-check/REPORT.md), [Source](../../proofs/blueprint/BLUEPRINT.md) |
| C028 | Sizes count vertices of $T$ unless marked primal. "First" means an exhaustive search found nothing smaller. "Witness" | [Source](../../digestions/route-map/ROUTE-MAP.md) |
| C029 | / Combinatorial / The refereed proof. / Choosing the highest or lowest state, or turning all cycles | [Source](../../research/2026-11-14_astra_referee-combinatorics/REPORT.md) |
| C030 | / Graph-theoretic / Pair criterion and three-matroid description, refereed. Two-tree packing, refereed by its author's model. / | [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md), [Source](../../research/2026-11-14_opus_referee-rainbow/REFEREE-packing.md) |
| C031 | / Constructive / The lab recovers cycles. / No polynomial bound. Strict descent fails first at 16 | [Source](../../workings/barnette_lab/README.md) |
| C032 | / Algebraic / Two determinants and the linear weights, refereed. / The plain determinant fails on the | [Source](../../research/2026-11-14_sol_route-algebra/REPORT.md), [Source](../../research/2026-11-14_fable_referee-families/REFEREE-algebra.md) |
| C033 | / Topological / A Gauss-Bonnet reading of the disk identity and a dual rank formula, by Opus, | [Source](../../research/2026-11-14_fable_referee-topology/REPORT.md) |
| C034 | / Probabilistic / Explicit families show that good states can be exponentially rare. / The target degree | [Source](../../research/2026-11-14_fable_referee-families/REFEREE-probabilistic.md) |
| C035 | / Categorical / Cutting along a cycle and recording a boundary pattern composes: 3 patterns on triangles, | [Source](../../research/2026-11-14_fable_route-categorical/REPORT.md) |
| C036 | / Inductive / Splitting of states, a lift criterion and a rotation, refereed. A one-sided step, written. | [Source](../../research/2026-11-14_fable_induction-completion/REPORT.md), [Source](../../research/2026-11-14_astra_induction-lemmas/REPORT.md) |
| C037 | / Lattice / Covers form a distributive lattice. / Both extremes fail first at 18. "An extreme | [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md) |
| C038 | / Non-planar / The Pfaffian corollary follows from the theorem through Gorsky, Steiner and Wiederrecht. / On | [Source](../../research/2026-11-14_astra_route-pfaffian/REPORT.md) |
| C039 | !Route records by kind and recorded status | [Source](../../digestions/synthesis-figures/route-outcomes.png) |
| C040 | Vector PDF. The chart counts the records of routes.py. Keyword rules in count.py give each record one | [Source](../../digestions/synthesis-figures/route-outcomes.pdf), [Source](../../digestions/route-map/routes.py), [Source](../../research/2026-11-14_opus_synthesis-final/synthesis-audit/count.py) |
| C041 | Each half of the target is easy inside any cover: it contains a spanning tree of the | [Source](../../research/2026-11-14_opus_two-tree-packing/REPORT.md) |
| C042 | A 16-vertex cover contains no good state, however its cycles are oriented. The midpoint $(r+s)/2$ of any | [Source](../../proofs/sign-free/sign-free.pdf) |
| C043 | 1. **Close the induction without the signed count.** Contract at a vertex of degree four. Lemma G | [Source](../../research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md) |
| C044 | 2. **Prove at least $2^m$ good states.** It holds through 22 vertices, and through 24 without separating | [Source](../../research/2026-11-14_sol_referee-conjectures/REPORT.md) |
| C045 | 3. **Prove descent with plateaus.** Pair descent says that reversals reach a good pair without ever increasing | [Source](../../research/2026-11-14_fable_descent/REPORT.md), [Source](../../research/2026-11-14_astra_referee-descent/REPORT.md) |
| C046 | 4. **Find a polynomial-time construction.** Testing one orientation of a cover is linear; searching all covers has | [Source](../../research/2026-11-14_sol_counting-families/REPORT.md) |
| C047 | 6. **Finish formalising our route.** Section 4 of the paper still needs the bridge from heights to | [Source](../../proofs/blueprint/FORMALISATION.md) |
| C048 | 1. The target, two induced trees in the dual, is Stein's from 1971, in the form of | [Source](../../research/2026-11-14_opus_history-literature/REPORT.md), [Source](../../research/2026-11-14_astra_older-approaches/NOVELTY.md), [Source](../../research/2026-11-14_opus_history-literature/RESULTS-TABLE.md), [Source](../../research/2026-11-14_astra_literature-consolidation/REPORT.md), [Source](../../research/2026-11-14_astra_citation-audit/REPORT.md) |
| C049 | An earlier rewrite of another paper gave a style guide of 22 rules, which the merge followed. | [Source](../../research/2026-11-14_astra_exposition-method/STYLE-GUIDE.md), [Source](../../research/2026-11-14_fable_coldread-main/REPORT.md) |
| C050 | **Real sign against Lean's phase.** The primal referee feared a factor depending on the number of cycles. | [Source](../../research/2026-11-14_opus_cross-audit/ADJUDICATION.md) |
| C051 | **279 against 213 marked objects.** Two counts of Li's marked objects disagreed because the count depends on | [Source](../../research/2026-11-14_opus_referee-involutions/DISCREPANCY-279-213.md) |
| C052 | **First failures.** Counting mirror images separately moved two counterexamples down to 12 vertices, and several saved "lattice | [Source](../../research/2026-11-14_sol_referee-structure/REPORT.md) |
| C053 | <!-- inventory-start --> The inventory was taken at 2026-11-14 15:22 UTC by count.py, with output in counts.json. | [Source](../../research/2026-11-14_opus_synthesis-final/synthesis-audit/count.py), [Source](../../research/2026-11-14_opus_synthesis-final/synthesis-audit/counts.json) |
| C054 | / Main paper, version 2, at the time of the count / 20 / | [Source](../../paper/main/barnette.pdf) |
| C055 | / Main paper, version 1 / 18 / | [Source](../../paper/main/history/barnette-v1.pdf) |
| C056 | / Primal companion / 15 / | [Source](../../proofs/primal/primal.pdf) |
| C057 | / Involution companion / 18 / | [Source](../../proofs/involutions/involutions.pdf) |
| C058 | / Atlas / 34 / | [Source](../../digestions/atlas/atlas.pdf) |
| C059 | The censuses cover different populations and must not be added up. The numbers are quoted from the | [Source](../../research/2026-11-14_astra_synthesis/EVIDENCE.md) |
| C060 | - **Sign-free note.** Fable wrote the note and tested every statement through 12 vertices. Sol, a different | [Source](../../proofs/sign-free/sign-free.pdf), [Source](../../research/2026-11-14_sol_referee-sign-free/REPORT.md), [Source](../../research/2026-11-14_fable_sign-free-figure/REPORT.md), [Source](../../research/2026-11-14_astra_referee-descent/REPORT.md), [Source](../../research/2026-11-14_astra_citation-audit/REPORT.md), [Source](../../research/2026-11-14_astra_citation-audit/PDF-RIGHTS.md), [Source](../../research/2026-11-14_sol_release-check/REPORT.md), [Source](../../research/2026-11-14_astra_final-recheck/REPORT.md), [Source](../../paper/main/refs.bib), [Source](../../papers/barnette.bib), [Source](../../research/2026-11-14_opus_notes-proofread/REPORT.md), [Source](../../research/2026-11-14_fable_notes-figures/REPORT.md), [Source](../../research/2026-11-14_fable_atlas-repair/REPORT.md) |
| C061 | 1. **Author lines.** The main paper and the primal, involution and sign-free notes all have an empty | [Source](../../research/2026-11-14_sol_machinery-literature/pdf), [Source](../../research/2026-11-14_opus_history-literature/pdf), [Source](../../research/2026-11-14_astra_citation-audit/PDF-RIGHTS.md), [Source](../../research/2026-11-14_opus_cross-audit/CLEANUP-PROPOSAL.md), [Source](../../proofs/lean/README.md), [Source](../../research/2026-11-14_sol_figures-polish), [Source](../../proofs/blueprint/FORMALISATION.md), [Source](../../paper/main/barnette.pdf), [Source](../../research/2026-11-14_sol_referee-main-v2/REFEREE.md), [Source](../../digestions/route-map/HOW-IT-WORKS.md) |

## Retained negative routes

REFUTED entries below are copied from the route map snapshot. Their labels do not refute broader unnamed routes. The full scope, counterexample and source locator are retained in routes.py.

| Route | Rejected proposal | Source locator |
|---|---|---|
| S0.x1 | drop bipartite | lim/HYPOTHESES.md; examples/K4.json, Tutte46.json |
| S0.x2 | drop 3-connectivity | lim/HYPOTHESES.md; examples/theta_cube_26.json |
| S0.x3 | other surfaces | lim/HYPOTHESES.md; examples/torus_3x3.json |
| TG.x1 | trees from colour classes | APSW 2016 (limitation theorem); hist/WHAT-WAS-HARD.md 5 |
| TG.x2 | Grinberg obstruction | hist/WHAT-WAS-HARD.md 2; gt/PROOFS.md (Grinberg's identity is automatic for two induced trees) |
| A.x1 | every avoiding cycle comes from a good state | posed in dep/skeleton.md A2; refuted by comb/ROUTES.md 12 (E8) and lim/examples/prism_recovery.json |
| B.x1 | drop bijectivity | lim/examples/nonbijective_disk.json |
| C.x1 | sign as a product of two dimer weights | mach/REFORMULATIONS.md 3; con/ALGORITHMS.md; dim/PROOF.md 6 |
| K.x1 | choose the cycle using r | lim/HYPOTHESES.md (disk identity and bijectivity) |
| N.x1 | zero, vertex-only or face-only weights | lim/data/zero_weights.json; dim/PROOF.md 6; alg/PROOF.md 1 |
| N.x2 | parity or mod p count without weights | comb/ROUTES.md 8; dep/skeleton.md D3; alg/PROOF.md 2; alg/TABLES.md (residues mod 2, 3, 4, 5, 7, 11) |
| N.x3 | good pair among the fewest-cycle pairs | dep/skeleton.md D2; comb/ROUTES.md 7 (E2d, E3); refc/REFEREE.md; gt/ROUTES.md O3 (a 40-vertex one-cycle cover with no good pair) |
| N.x4 | highest or lowest partnered state | comb/ROUTES.md 4 (E1, E1c); refc/REFEREE.md; gt/ROUTES.md O1 (extremes of Propp's state clock lattice fail at V=10) |
| N.x5 | minimal cover, all cycles one way | comb/ROUTES.md 5 (E2, E2c); refc/REFEREE.md |
| N.x6 | largest rank difference | comb/ROUTES.md 6 (E5) |
| N.x7 | one cycle always suffices | comb/ROUTES.md 13 |
| N.x8 | cubes of good states; sign = parity of rank | comb/ROUTES.md 9, 10 |
| N.x9 | ordinary determinant, all face variables 1 | con/ALGORITHMS.md, data/exact_determinant.json; dim/IDENTITIES.md |
| N.x10 | allow doubled edges (standard double dimers) | dim/PROOF.md 3; dim/ROUTES.md |
| N.x11 | positive semidefinite blocks | alg/PROOF.md 4; comb/ROUTES.md 3 |
| N.x12 | Combinatorial Nullstellensatz | alg/PROOF.md 1 |
| N.x13 | real stability of the tree-state polynomial | alg/PROOF.md 3 |
| U.x1 | matching matroid meets graphic matroid | mach/REFORMULATIONS.md 6; con/data/other_candidates.json; refd/REFEREE-constructive.md |
| U.x2 | unconstrained white spanning trees | dim/ROUTES.md; con/ALGORITHMS.md (wilson_candidate) |
| U.x3 | trinity arborescences = good states | dim/ROUTES.md (trees and trinity) |
| U.x4 | Yutsis partition of G | mach/REFORMULATIONS.md 11 |
| R.x1 | acyclic Q_s alone is enough | lim/HYPOTHESES.md (forest versus rooted forest); dep/correspondence.md 3.5 |
| G.x1 | prescribe whatever each cut needs | Bagheri Gh. et al. 2022, proof of Thm 4.6; hist/WHAT-WAS-HARD.md 6 |
| U.x5 | LP relaxation of the three constraints is integral | gt/ROUTES.md M1-M4; posed in mach/ROUTE-IDEAS.md 5 |
| U.x6 | induction by degree-4 expansion | gt/ROUTES.md I1; gt/PROOFS.md |
| U.x7 | positivity of the norm or of the Laplacian terms | refd/REPORT.md; alg/PROOF.md 6 |
| U.x8 | tree count as an unrooted invariant | alg/REPORT.md; alg/invariants.json |
| N.x14 | strict q-descent | des/DESCENT.md; rd/REPORT.md |
| N.x15 | a sign gauge on the variables of F | alg/PROOF.md 2; alg/REPORT.md; rf/REPORT.md |
| D.7 | extremes of Felsner's lattice of pairs | rc/REFEREE.md; rc/data/v18.json; rc/data/census_18.json |
| D.x1 | the partner of a good state is a good state | topo/REPORT.md item 5 |
| G.x2 | a uniform boundary condition for longer cuts | cat/PROOF.md Prop. 4; cat/EXPERIMENTS.md |
| A.x2 | two roots instead of a root face | cat/REPORT.md (what failed); cat/CATEGORICAL.md |
| K.x2 | the two cube structures form a bicomplex | cat/REPORT.md (what failed) |
| U.x9 | topological Hall for partial good states | cat/REPORT.md (what failed) |
| D.ext1 | distance one from a lattice extreme | rc/REFEREE.md; rc/data/r1.json |
| D.ext2 | R2: extreme or irreducible | rc/LATTICE-READING.md Section 6; rc/data/R2_glued_V33.json |
| TG.parity | BF21 parity equals black-inner obstruction | older/BRIDGES.md; older/REPORT.md |
| N.rank-dead | signed sum as base-lattice rank polynomial | rc/LATTICE-READING.md; rc/data/examples.json |
| D.level-dead | fixed-cycle-count flip connectivity | covers/data/levels.json; cr/code/witnesses.json; cr/INTEGRATION.md |
| U.lift-dead | some contracted good state lifts directly | ri/data/nolift_18.jsonl; ri/REFEREE.md |
| U.walk-dead | surplus walk always terminates | reft/RAINBOW.md; reft/data/cycles_hunt_38_400_19_0.0.json |
| U.mean-dead | positive full-spoke UST mean fitting | prob/PROOFS.md; cr/INTEGRATION.md |
| U.support-dead | joint Lorentzian rounding | prob/PROOFS.md; prob/code/campaign.py |
| N.zeros-dead | universal analytic root locations | prob/PROOFS.md; cr/code/polynomials.json; cr/INTEGRATION.md |
| N.heawood | root-free torus nonvanishing | pf/PROOFS.md; pf/data/results.json; pf/data/verification.json |
| U.ind-R1 | induction R1: A good lifted state must come from a good contracted state. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R2 | induction R2: Every simple degree-four contraction preserves a pair. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R3 | induction R3: Every contracted good state lifts to a good state. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R4 | induction R4: Failed lifts can be compensated by good states of the same contraction type. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R5 | induction R5: Some contracted good state uses the prescribed local opposite edge. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R6 | induction R6: The original rotation repairs every failed lift. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R7 | induction R7: $g(T)\geq2g(T/M)$. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R8 | induction R8: The lowest nonzero cover-area coefficient is monotone under contraction. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R9 | induction R9: $m(T)=m(T/M)$ whenever both admit pairs. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R10 | induction R10: $g(T)=g(T/M)+g(T/N)$ for the two contractions. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R11 | induction R11: Every allowed non-root corner can be prescribed in a good state. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R12 | induction R12: Some pair-preserving contraction always exists, even with separators. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.ind-R13 | induction R13: Every inverse Batagelj P-operation preserves a pair. | ind/data/failed_inductions.json; ri/REFEREE.md |
| U.loads-dead | rainbow loads are M-convex | reft/RAINBOW.md; reft/data/loads_sampled_6_13.json |
| D.chain-dead | every maximal lattice chain hits success | rc/REFEREE.md; rc/data/r3.json; rc/data/R2_glued_V33.json |
| D.fraction-dead | at least half the lattice succeeds | rc/REFEREE.md; rc/data/r5.json; rc/data/R2_glued_V33.json |
| U.rainbow-strict | strict black-excess descent | reft/RAINBOW.md; reft/data/traps_16_16_all.json; rr/REFEREE-rainbow.md |
| U.rainbow-pot | four rainbow distance potentials | reft/RAINBOW.md; reft/data/potential_10.json; reft/data/potential_12.json |
| U.G-inward | innermost bad-disk selection | il/REPORT.md; il/data/certificates.json; il/data/g_five_certificates.json |
| U.G-five | innermost bad five-cycle selection | il/REPORT.md; il/data/g_five_certificates.json |
| U.X-cover | fixed-cover exceptional repair | il/REPORT.md; il/data/cube_witness.json |
| U.pack-support | round within a fixed pair support | pack/REPORT.md; pack/data/rainbow_V14-17.json |
| N.lookahead | bounded-lookahead q descent | des/DESCENT.md; des/data/witnesses.txt; des/data/witnesses_verified.json; des/data/census_tables.md; rd/REPORT.md; rd/code/recovered40_0_40.json |
| N.height-ties | height and cover-count tie-breaks | des/DESCENT.md; des/data/witnesses.txt; des/data/witnesses_verified.json; des/data/census_tables.md; rd/REPORT.md; rd/code/all_potentials.json; rd/code/recovered40_0_40.json |
| U.rainbow-mean | uniform rainbow mean load one | reft/RAINBOW.md; reft/data/average_6_14.json |
| U.evict-transitive | resident involutions act transitively | reft/RAINBOW.md; reft/data/walk_exhaust_13_14_all.json |

Source: [routes.py](../../digestions/route-map/routes.py). Folder abbreviations resolve through its FOLDERS table.
