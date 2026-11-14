COMPUTED. Rewrote the overview and open-problems chapter, corrected the route source and rebuilt the map and labyrinth.
COMPUTED. All facial roots through dual order 12 confirm that the first partnered cyclic-Q state occurs at 12, not the chosen running example's 13.
COMPUTED. The fresh full lab replay passes all 14 unit tests and 1,209 rooted runs; the descent output sum is 193,623,384 pairs through 23.
COMPUTED. Atlas route-page titles match the combined PDF; generated figures were inspected and both labyrinth checks pass.
CONJECTURE. C3, rainbow Step X, the two induction lemmas and P2 remain open; the completed descent referee supports the named structural claims with explicit qualifications.

# Report

## What I set out to do

Apply the second digestion audit's corrections to the owned overview and open-problems chapter. Replace spoke-based recovery with the final paper's tree of faces, distinguish the two descents and the two lattices, repair the induction table, integrate late reviews, regenerate the route catalogue and labyrinth, check links and commit only owned paths.

I read research/BRIEF.md, the repository README, the full repository unslop skill, all three named audit documents, the current glossary and recovery digestion, the relevant manuscript passages, the labyrinth rebuild instructions and the late reports. The route-map folder has no README.md; its source docstring and labyrinth/README.md describe its rebuild. No subagents were used.

## What I established

- COMPUTED, [recompute.py](code/recompute.py), [output](recompute.json). Enumerated all plantri Eulerian triangulations and every facial root from dual order 6 through 12 with barnette_lab. No partnered state has cyclic Q below 12; two such rooted-state occurrences appear at 12. The 13-vertex running example is a chosen illustration, with no minimality claim for the conjunction involving an enclosing D-cycle.
- COMPUTED, [recheck.py](code/recheck.py), [worked examples](worked-examples.txt). Reran the second auditor's implementation read-only and redirected its output here. Cube, prism, running example, double octahedron and order-16 fixture pass all assertions, including independent lab comparisons. This reuses the auditor's code; it is a fresh replay, not a new independent implementation.
- COMPUTED, `python -X utf8 -B workings/barnette_lab/run_tests.py full --output research/2026-11-14_sol_digest-fixes/lab-replay`. All 14 unit tests pass. The [full evidence](lab-replay/full.json) records 1,209 rooted runs and the exact ranges and vacuity. The campaign took 219.24 seconds, excluding unit tests. Its exhaustive census reaches 14, with larger saved fixtures and independent comparisons through 12. No general theorem or running-time bound follows.
- COMPUTED, [numbers.json](numbers.json). Re-summed the stored descent census through 22 and all eight order-23 shards. The result is 193,623,384 pairs. Re-summed the completed part of the new rainbow referee's order-18 run, obtaining seven completed graphs, 224 roots and 7,999,488 explicitly enumerated multiple-cover rainbow trees. Single-cover roots use the referee's Proposition U rather than tree enumeration.
- COMPUTED, [atlas index check](atlas-index-check.json). Verified every current route-page title against the actual combined atlas PDF. Its contents page creates a one-page offset between route-page and PDF-page numbers. The atlas owner committed the old-numbering correction while this task ran; I preserved that work and added the explicit offset explanation.
- COMPUTED, [build/check log](build-check.txt). Regenerated the catalogue and all route figures from routes.py, rebuilt frontier data, seeded the labyrinth, and ran lab.py check and lab.py build successfully. The catalogue has 246 routes and the graph 366 nodes. These are catalogue counts, not counts of independent proofs.

## What changed

The overview follows S_s, the spanning tree of T, then Y_s, the dual tree of faces rooted at t0. Its diagram and table link the audited digestions, manuscript locations and current atlas pages. It explains the exact-count use in recovery as well as signs and nonvanishing.

The open chapter is about 2,200 whitespace-separated words; the overview about 1,000, including diagram and table markup. Both use the glossary's definitions. Strict black-excess descent concerns rainbow trees and fails at order 8. Strict q-descent concerns pairs and fails at order 16. Propp's state-clock lattice and Felsner's pair lattice have separate definitions and witnesses. No new minimality claim is made for the order-18 pair-lattice witness. All thirteen induction rows now state complete claims and name readable witnesses with data links; the full graveyard remains in the generated catalogue.

The same distinctions appear in routes.py and current labyrinth rows. Historical events and previous state-of-the-art versions remain historical. The source's recovery waypoints and figure labels now follow the final paper. I also corrected the misleading old row label that called ordinary acyclicity a good state.

## Late reports and review status

The [final scan](final-report-scan.json) records hashes of all six relevant reports.

- Descent author. The large COMPUTED ranges remain attributed to the author. The conserved three-height identity and structural descent lemmas are now independently AI-refereed, but supply no progress potential. The conditional PPADS reduction is supported with encoding and citation qualifications.
- Descent referee. Its completed report arrived during the last scan and is integrated. It independently confirms C3 through 19 and on all 335,704 pairs of the named 40-graph order-40 batch, supports the structural identities and qualified sink reduction, and confirms all 27 named alternative potentials fail. Its recovered graph-3 radius-four certificate replaces an incorrectly selected radius-three line. It independently checks all 7,940 induction exceptions through 18, the rotation bijection and counting inequality. The author census through 23 and the entire 230-graph campaign were not independently replayed. The claimed induction converse is unsupported; the symmetric nonexceptional-state lemma is only a sufficient route to induction.
- Lean reviewer. The independent rebuild and statement/dependency review is complete. It rejects TODO T5 surjectivity, limits the full Lemma 4.5 claim, retains generic Mathlib polynomial dependencies, and distinguishes the formal flow from the unformalised face-path translation. The chapter and catalogue retain all four qualifications.
- Rainbow/packing reviewer. The completed REPORT accepts Step R, unique-factor completion, resident eviction and the named packing theorems, with corrections. P2 and Step X remain conjectures. Its order-18 partial result is included. The packing review uses a fresh instance of the author's model with independent code.
- Different-model families reviewer. The completed REPORT confirms named finite checks and proofs but leaves the all-length transfer code unchecked. Chain Hamiltonian counts depend on the gluing rule. The one-state sign-gauge obstruction does not refute signs on both states. The earlier all-length transfer referee and this finite check have different scopes.
- Lab tests. The completed REPORT finds no production-code bug; absolute heights and drawing-dependent raw marked counts need the stated qualifications. The fresh replay here agrees.

## What failed or was not done

- The large descent, all-root C1 and separator-free order-24 campaigns were not rerun here. Their stated ranges remain attributed COMPUTED results with their existing review limits. Re-summing data is not independent verification of a search.
- No Lean rebuild was attempted here; the independent review supplies that evidence.
- A four-move escape witness refutes three-move lookahead, not four-move lookahead. The source's earlier wording risked that confusion. Lookahead four and unbounded escape radius remain open. The slogan "every bounded variant is dead" would overstate the reports.
- One intermediate arithmetic assertion counted only enumerated multiple-cover rows as if they were all roots. I corrected it by including the single-cover roots through the fixed number of faces per triangulation; the saved evidence distinguishes the two.
- The figure inspection covers the full map, overview and kinds chart. Current labels fit their boxes. The detailed map intentionally truncates long row labels; full statements remain in ROUTE-MAP.md. No interactive dashboard/browser audit is claimed.

## What is still open

CONJECTURE. C3 and rainbow Step X need proofs controlling entire plateaus. Induction G and induction X need the remaining contraction and repair steps. C1 and P2 remain conjectures. The Lean statement bridges and human review remain unfinished. This editorial task closes none of those mathematical questions.

## Three best next steps

1. Attack the remaining positive-level plateau obligation for C3; the completed referee validates its surrounding identities but supplies no general exit argument.
2. Finish the remaining rainbow order-18 cases, keeping single-cover proofs separate from enumerated multiple-cover trees.
3. Correct the false Lean TODO, formalise the face-path-to-flow dictionary and general cancellation statement, then obtain a human reading of the paper and digestions.

## Leads for others

The atlas index was already corrected concurrently; its verified current numbering is retained. Sources outside this task's ownership still contain older verdicts and terminology. They should be updated by their owners from the named completed reviews, particularly the gluing-dependent chain count and the distinction between one-state and two-state gauges.

## Delivery

[CHANGELOG.md](CHANGELOG.md) lists the edited areas and commands. [link-check.txt](link-check.txt) records local Markdown and static dashboard target checks. Only owned paths were staged. The first checkpoint is commit 444aaf6; final commit and push are recorded in the chat handoff.
