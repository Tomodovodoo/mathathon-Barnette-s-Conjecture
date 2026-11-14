# Fact-check of digestions/SYNTHESIS.md

Checker: Fable 5.2, 14 November 2026. The document checked is the version GPT-6 Astra committed in `0d2c5cc`. Block numbers C001 to C083 are those of the author's ledger, `research/2026-11-14_astra_synthesis/CLAIMS.md`. Each row gives the claim, the file I opened to check it, and a verdict.

Verdicts: **correct** (kept, perhaps reworded), **corrected** (the claim was wrong or out of date and the text now says something else), **softened** (true in a narrower sense than stated), **removed** (unsupported, or cut for length; the row says which), **added** (a claim the first version lacked).

Folder names are short for `research/2026-11-14_<name>/`. "main" is `paper/main/barnette.tex` as it stood at 13:00 UTC, which is version 2. I read that file in full. I read in full the reports of the referee runs, of the blueprint, the cross-audit, the history review, the merge, the main revision, the packing run and the two induction runs. For the other folders I read the report's summary and searched the report for the number or phrase in question. Where a row cites REFEREE, INTEGRATION or another file, I opened that file. I did not rerun any census. Sums of quoted counts are recomputed by hand where the row says "sum".

## Section 1, the answer in one page

| Block | Claim in the first version | Source checked | Verdict |
|---|---|---|---|
| C001 | A Hamiltonian cycle needs degree two and connectivity; deleting a perfect matching gives degree two. | main, Introduction | correct |
| C001 | "The proof constructs a matching whose complement is connected by building a forest in the planar dual." | main, Prop. 2.6 | softened: the object is an acyclic selection, one side of every triangle. "Forest" alone hides the one-side condition. |
| C002 | States, partner, $Q_s$, outdegree one at every non-root, components reach a root or hold a directed cycle. | main, Def. 3.2, Def. 4.1, Lemma 4.2 | correct. The text now defines a good state as main does (Def. 3.4): forest with one root per tree. |
| C003 | A directed cycle of state choices encloses one more white face than black; the state bijection and Euler give it; false for arbitrary cycles. | main, Lemma 3.8 and the paragraph after it; OpenAI text, Lemma 4.1 | correct |
| C004 | Cancellation at a fixed second state; regrouping by unoriented cycles; positive increments equal to white faces inside; the groups with fewest cycles share a sign. | main, Lemmas 4.5, 4.6, 4.7, Prop. 4.8 | correct |
| C005 | "A forest pair gives an incidence tree, then a tree on white faces. Root that tree and select sides toward its root." | main, Lemma 3.6; OpenAI text, Section 6 | corrected: that is OpenAI's recovery. The main paper uses a tree on all faces rooted at $t_0$. The text now says "a tree on the faces". |
| C005 | Separating triangles: cap, prescribe, glue. | main, Theorem 6.2 | correct |
| none | Where the first pair comes from. | main, Prop. 5.2 | added: the first version's page one never said it (a flow argument, when there is no separating triangle). |
| C006 | New mechanism = disk identity with the two-way signed count; dual form, edge avoidance and separator reduction are older. | opus_history-literature REPORT, item 2 | correct |
| C006 | The mathathon produced an explanation, simpler forms and a record of failed replacements; no unsigned proof, no polynomial constructor. | sol_referee-conjectures, fable_referee-topology, astra_induction-lemmas REPORTs | correct. "Substantial" removed. |
| C007 | The merge keeps the geometry in $T$, uses local signs, face-path heights and an inside-connectivity lemma. | opus_manuscript-merge REPORT; main, Section 7 | correct |
| C007 | "Its main theorem has an independent AI referee." | sol_referee-main REPORT | corrected: the referee read version 1 (18 pages). The text now says that Sol refereed version 1, and that Sol's second audit (sol_referee-main-v2 REPORT, delivered while I worked) covers the final text of version 2, verdict follows, eight small corrections. |
| none | 4 exact, 25 after translation, 5 without counterpart, of 34. | proofs/blueprint/BLUEPRINT.md, lines 4, 5, 41 to 46 | added |
| none | Reading order for a human. | | added on page one: main paper, the version 2 referee report, HOW-IT-WORKS. |
| none | A late Lean run checked the sign, the cancellation and the nonvanishing step; 8 exact, 24 translated, 2 without counterpart. | opus_lean-devices REPORT; proofs/lean/BLUEPRINT-DELTA.md | added. The tally 8, 24, 2 is my count from the delta's rows (4.4 and 4.7 from none to exact, 4.5 and 4.8 from translated to exact, 3.7 from none to translated). The delta prints no totals, and it calls 4.4 exact "in the Lean's model" and 4.8 exact "for the method". |
| none | A cold read of version 2 by Opus found no mathematical problem. | opus_coldread-main-v2 REPORT item 5 | added |

## Section 2, what exists

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C008, C009 | The diagram of sources and evidence. | rendered and looked at | corrected: redrawn. The old figure sent the Lean proof into "companion proofs" as a whole, gave the main paper no review mark, and left out the blueprint. |
| C011 | Main paper: contents. | main | correct. Page count (19) and the version distinction added. |
| C012 | Blueprint: statement-level correspondences with explicit gaps. | proofs/blueprint/README.md, BLUEPRINT.md | correct. "Not reviewed" added (opus_blueprint REPORT asks for a second reader). |
| C013 | Primal companion: complete route in $G$. | fable_referee-primal REPORT, opus_cross-audit REPORT | correct. Review status added. |
| C014 | Involution companion: Li's multi-mark argument as two involutions. | opus_referee-involutions REPORT | correct. Page count is now 18 (was 17), after the second referee's figure fixes. |
| C015 to C021 | Digestions, route map, atlas, labyrinth, lab, library, figures. | the linked READMEs; astra_literature-consolidation REPORT (87 sources); digestions/atlas/README.md (28 routes, 31 pages) | correct |

## Section 3, simplifications

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C022 | $\#TM$, $\#HC$, $c_{\min}$ count different objects. | sol_referee-covers INTEGRATION | correct. Renamed $g$, $h$, $m$, with the reports' names given once. |
| C023 | $W=B+1$; checked by Astra, confirmed by Fable. | astra_referee-combinatorics REPORT; fable_referee-topology REPORT, claims (a), (b) | correct. Sol's check in the main paper added. |
| C024 | $\epsilon=\prod\delta$ replaces the phase "up to a global normalization"; found by Opus and Fable; checked by Sol. | opus_review-draft-A REPORT item 4; fable_review-draft-B REPORT item 4; main, Remark 4.10 | correct. The constant is now stated: $i^J=i^{-n}\epsilon$. |
| C025 | Face-path heights; fixed paths matter; Fable supplied them, Sol checked the merged version. | fable_review-draft-B REPORT (S1, 736 reversals); main, Lemma 4.6 | correct |
| C026 | Finite difference over the cube of orientations; linear weights give one polynomial; Laurent caveat. | main, Lemma 4.7 and Remark 4.10; fable_referee-determinants REPORT; sol_referee-main REPORT item 3 | correct. Added: Opus proved the lemma in Lean (opus_blueprint REPORT item 3). |
| C027 | "Draft B left that premise unwritten." | opus_manuscript-merge REPORT item 3 ("the gap both drafts shared") | corrected: both drafts |
| C028 | Gauss-Bonnet reading; Fable accepted Opus's derivation after two additions; Morse reading needs the root spokes. | fable_referee-topology REPORT, claims (a), (d) | correct. The item now sits in the topological row of section 5; the Morse detail is cut for length. |
| C029 | The Euler identity $e-b-(2p-4)=\frac12\sum(\beta-d+4)$ and the exact pair criterion; Sol checked both directions. | sol_referee-structure INTEGRATION, sections 1 and 2 | correct. Formula cut for length. Attribution corrected: the criterion is stated in the constructive manuscript (main, Section 7, citing its Theorem 1.2); Opus's contribution is the proof from the Euler identity. |
| C030 | Gluing only at black-inner separating triangles. | same file | correct, merged into the previous item |
| C031 | Recovery is injective, not surjective; found exactly when the state is good; otherwise no partner. | sol_referee-structure REPORT; main, Section 7; opus_cross-audit CONSISTENCY section 3 (prism: 3 states, 2 good, 4 cycles) | correct. Prism example added. |
| C032 | $c(D)=\kappa(G-S)-1$; $3\#TM\le\#HC$; $\#TM\ge 2c_{\min}$. | sol_referee-covers REFEREE-covers C2; astra_referee-combinatorics REPORT, last section | correct |
| C033 | Inclusion from avoidance; no separate referee. | astra_older-approaches REPORT | correct |
| C034 | Squarefree coefficient of a determinant; the two formulas coincide; the norm is no independent proof. | fable_referee-determinants REPORT | correct |
| C035 | Prism counts $2m+2$, 2, $2m-2$; $2^b$ and $3\cdot2^b$; cube has six; "the families referee checks these statements". | sol_referee-covers REFEREE-families F1, F5; INTEGRATION | corrected: the numbers are right, but the referee (Sol) is the same model as the author of `sol_counting-families`. The text now says no different model has checked them. The prism parameter is renamed $j$ because $m$ is taken. The two avoidance counts (2 and $2m-2$) are cut for length. |

## Section 4, the three papers

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C036 | Fourteen shared nodes, listed. | fable_dependency-graph skeleton.md, table K0 to K16 | correct. The list is shortened to its ends and middle; the link gives all fourteen. |
| C037 | Four points differ: first pair, weights, nonvanishing, final connectivity. | fable_dependency-graph REPORT item 2 | correct |
| C037 | "Li's marks encode the same lowest-degree information as the weighted sum." | opus_referee-involutions REPORT (last finding); main, Remark 4.10 | correct, cut for length |
| C038 | OpenAI and the constructive paper close; Li needs the balance count and three Appendix B checks; the involution companion is Li's proof unpacked, accepted by Opus. | fable_dependency-graph REPORT item 1; opus_referee-involutions REPORT items 1, 5 | correct. Added: "no error found in any of the three papers" (same report). |
| C039 | Lean: algebraic dual from a drawing, bond shores, one flow, linear factors, recovery in $G$, induction on the avoided edge; no two-trees theorem, no Pfaffian corollary; three axioms. | opus_lean-formalisation REPORT items 1 to 3, and lines 25, 30 | correct. File and line counts added (31 files, 8,936 lines). |
| C040 | Blueprint pinned to a committed manuscript; exact / translated / unmatched; matching statement is not a matching proof. | opus_blueprint REPORT; BLUEPRINT.md | correct. Added: the pinned text is version 1, and I checked by hand that version 2 keeps the statement numbers the blueprint cites (2.2, 2.6, 3.2, 3.7, 4.1, 4.3, 4.4, 4.7, 5.2, 6.2). |
| none | The Lean devices paragraph: Lemmas 4.4, 4.5, 4.7 and Prop. 4.8 compile; OpenAI's main theorem rebuilds through the real-sign lemma on the same axioms and no longer reaches the phase or the polynomial; heights, Lemma 2.2 and Prop. 2.6(2) are not checked. | opus_lean-devices REPORT items 2 to 5; proofs/lean/README.md | added. I did not rebuild the Lean files. An independent check (`astra_lean-check`) had no report at my last scan. |
| C040 | The line estimates of the feasibility note and the report differ. | FORMALISATION.md lines 6 and 75; opus_blueprint REPORT item 5 | correct (900 to 1,500 against 530 to 710 or 820 to 1,170). No estimate is quoted. |

## Section 5, routes and failures

Sizes checked against the report that owns each counterexample.

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C042 | Highest or lowest state and uniform direction fail at 12 with reflections. | astra_referee-combinatorics REPORT item 4 | correct. "Uniform direction" now says "all cycles of a smallest cover". No "first" is claimed. |
| C042 | Six good states with $m=2$ at 13 refute cubes of four. | same, "What failed" | correct |
| C043 | Two-matroid relaxation: "four false states" on the hexagonal prism. | fable_referee-determinants REPORT ("4 of the 6 common bases are not states") | corrected wording |
| C043 | Fractional LP vertex at 13, no minimality. | sol_referee-structure REPORT (rank-25 certificate) | correct |
| C043 | A support with no tree matching at 16. | sol_referee-structure REPORT; opus_two-tree-packing REPORT | correct |
| C043 | Two-tree packing: new proof, unreviewed. | opus_two-tree-packing REPORT ("T2, unreviewed") | correct |
| C044 | Strict rainbow descent fails at 8; surplus walk cycles at 38, a witness. | fable_referee-topology REPORT, "What failed" | correct |
| C045 | Raw determinant fails on the hexagonal prism; doubled edges at 9; sign gauge at a 13-vertex witness. | fable_referee-determinants REPORT; sol_route-algebra REPORT lines 23, 39 | correct |
| C045 | Zero residues mod 2, 3, 4, 5, 7, 11 at orders 6, 13, 9, 14, 16, 26. | sol_route-algebra REPORT line 33 | correct. The algebra report has no reviewer; said so. |
| C046 | Turning number and dual rank; Morse reading passes; rainbow results await a reader. | fable_referee-topology REPORT | correct |
| C047 | Mean obstruction on the cube; unit-circle and real-rootedness fail at 12; packing gives a feasible fractional point. | sol_route-probabilistic REPORT; opus_two-tree-packing REPORT, Cor. 3.1 and REFEREE verdict | correct. Review status corrected: Opus checked the mean obstruction; the other review is by Sol, the author's model. |
| C048 | 3 patterns on triangles, 6 on quadrilaterals, 5-cycles fail at 9; unrefereed. | fable_route-categorical REPORT items 2, 3 | correct |
| C049 | Reverse lifting fails at 11; no lifting good state at 18; inward selection fails at 11, 13, 14; repairs fail at 16, 17, 18. | sol_referee-structure REPORT; fable_induction-completion REPORT item 3; astra_induction-lemmas REPORT | correct |
| C050 | Both extremes fail first at 18; extremes-or-irreducibles at 33, a witness; levels disconnect at 18. | sol_referee-conjectures REPORT; sol_referee-covers REFEREE-covers C5 | correct. Added: the 33-vertex witness has a separating triangle, and the question without them is open (same report). "Pairs form a lattice" corrected to "covers". |
| C051 | Pfaffian corollary through GSW; Heawood count zero with cancellation surviving; unrefereed. | astra_route-pfaffian REPORT | correct |
| C052, C053 | The route chart, 226 records. | routes.py, recounted | corrected: the map grew to 227 and then, after the final map run (sol_map-final REPORT), to 244 records with 77 refutations. `inventory.py` writes the current number, and the chart is regenerated with a totals row. |

## Section 6, why the signed count

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C054 | Every pair support has a tree meeting either degree requirement; splits into two point-rainbow trees; two face-rainbow trees is a conjecture. | opus_two-tree-packing REPORT, Cor. 3.2, Thm 3.3, Conj. P2 | correct. Added: 14,881 supports through 17 vertices, and "not reviewed". |
| C055 | The 16-vertex support; LP midpoint outside the hull; lattice counterexamples. | same report, "What failed"; sol_referee-conjectures REPORT | correct |
| C056 | The signed count compares supports; the refutations rule out named shortcuts only. | astra_referee-combinatorics REPORT, "What failed" | correct |

## Section 7, open problems

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C057 | G on 62,416 rooted instances through 19. | fable_induction-completion REPORT (7,386 + 16,032 + 38,998, sum) | correct |
| C057 | Contraction inequality on 1,202,792 contractions through 18. | same (344,872 + 857,920, sum) | correct |
| C057 | Later report proves G without chordless 5-cycles; the strict inequality is sufficient, not proved necessary. | astra_induction-lemmas REPORT | correct. X restated in the sufficient direction only. |
| C058 | 4,656,948 instances through 22, independently reproduced; separator-free census to 24 not independently replayed; one-cover and two-cover cases refereed. | sol_referee-conjectures REPORT; sol_referee-covers REFEREE-covers C3, C4 | correct. Added: who computed and who reproduced. |
| C059 | Pair descent and rainbow descent differ; rainbow descent through 17 and samples to 120. | fable_referee-topology REPORT (updated at 14:33 local: also 1,485 of 1,543 triangulations at 18); sol_referee-structure REPORT | correct. Added from the descent study (fable_descent REPORT, delivered while I worked): pair descent on all 49,325,864 pairs through 22 vertices; strict descent fails first at 16, lookahead two first at 21; 27 of 28 potentials fail. The pair total equals the pair count of Sol's census (sol_referee-conjectures REPORT). The study is not reviewed. |
| C060 | Testing a direction choice is easy, search is not; rarity defeats sampling. | sol_referee-conjectures REPORT (GAP); sol_referee-covers INTEGRATION (width-four tube) | correct |
| C061 | Direct non-planar proof; Heawood; six trisum signatures. | astra_route-pfaffian REPORT | correct |
| C062 | Formalise the exposition's route; start with sign and path flow. | opus_blueprint REPORT, next steps; opus_lean-devices REPORT, "still open" | corrected: the sign and the counting step are now done. What remains is the heights bridge (T2) and the two statements that need a Jordan curve theorem (T6). |

## Section 8, literature

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C063.1 | Stein's two-trees formulation predates the proof. | opus_history-literature REPORT; papers/INDEX.md (Stein1971 and Alt2016 "opened and statement checked") | correct |
| C063.2 | Edge avoidance and separator reduction are older. | same; papers/INDEX.md (Kelmans1994 "not held", "content via Alt and Hertel") | softened: the caveat that Kelmans's papers were never opened is now in the text. |
| C063.3 | The paired-state mechanism is in none of the 23 collected Barnette papers. | opus_history-literature REPORT item 2 | correct. Added: states are Tutte's (main, Introduction; INDEX Tutte1975, via Hine and Kálmán). |
| C063.4 | Earlier progress. | RESULTS-TABLE.md; history REPORT | correct. Schnieders 2025 marked as a preprint. |
| C063.5 | Computation to 90 primal vertices. | INDEX Brinkmann2022 ("opened", Theorem 4.1) | correct |
| C063.6 | Eleven reformulations, eighteen routes. | sol_machinery-literature REPORT | correct |
| C063.7 | "The proposed Feder-Subi parity identification fails on the truncated octahedron." | astra_older-approaches REPORT ("BF21"); history REPORT, last open item | corrected: the parity condition is that of Bagheri Gh., Feder, Fleischner and Subi (2021), not of Feder and Subi (2006). |
| C063.8 | The constructive manuscript's author is unknown. | history REPORT; astra_literature-consolidation REPORT | correct |
| C063.9 | Waterloo attribution unresolved. | papers/INDEX.md, Barnette1969 | correct, made specific |
| C063.10 | Hertel and Alt et al. were opened in the history folder. | sol_referee-main REPORT | correct, folded into item 2 |
| none | The OpenAI proof is an unrefereed preprint; a third party reports two Lean kernels accept it. | history REPORT item 3 | added |

## Section 9, the earlier rewrite

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C064 | Ten lessons. | astra_exposition-method STYLE-GUIDE.md rules 1, 4, 8, 9, 16, 17, 18, 22; HOW-THE-REWRITE-WORKED.md, last section | correct |
| C065 | The cold reader found an overloaded opening, missing motivations, floats in proofs. | fable_coldread-main REPORT items 1 to 3 | correct. Added what version 2 did about it (astra_main-revision REPORT). |

## Section 10, review status

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C066 | What "refereed" means. | the three referee reports | correct |
| C067 | Reflection lowers two counterexamples to 12; true extremes fail at 18; 33-vertex construction. | astra_referee-combinatorics, sol_referee-structure, sol_referee-conjectures REPORTs | correct |
| C067 | Phase: ratio $i^n$, independent of cycle count; $i^{-n}$ with reversed corners; 24,856 pairs. | opus_cross-audit ADJUDICATION.md | correct. The text now names the parties: Fable's referee warning, Astra's revision, Opus's adjudication. Added: Opus later proved the relation in Lean for the formal proof's own system (opus_lean-devices REPORT item 2). |
| C068 | 279 against 213: two drawings swap root anchors 4 and 5; both totals right; signed sum invariant. | opus_referee-involutions DISCREPANCY-279-213.md | correct. Added: 69 drawings, 35 values, 103 to 363. |
| C068 | Off-route sign error for odd numbers of marks, corrected in the revision. | opus_referee-involutions REPORT item 3; sol_involutions-revision REPORT | correct |
| C068 | The path-mark lemma has only a self-audit. | fable_referee-involutions-v2 REPORT (delivered after the first version) | corrected: Fable refereed it, "correct after fix", final verdict follows. |
| C068 | The Laurent correction is applied in version 2. | main, Remark 4.10; astra_main-revision CHANGES.md, E1 | correct |
| C069 | No separate review for induction lemmas, packing, algebra, category, Pfaffian, path-mark lemma, rainbow results. | the seven reports | corrected for the path-mark lemma; the rest correct |
| C069 | "The late families referee accepts prisms, chains, tube recurrences and rarity." | sol_referee-covers REPORT | softened: same-model referee |
| C069 | "The atlas and this synthesis have no second-model review." | fable_atlas-review REPORT; sol_atlas-audit REPORT | corrected: the atlas was built by Sol and rebuilt by Fable. Sol's audit passed 78 computed checks and found wording errors on several pages. Fable's final atlas run applied the corrections (fable_atlas-final REPORT). This synthesis now has this check. |
| C070 | Florek correction; the prism-chain control. | sol_referee-covers REPORT | correct. Florek kept in the ledger only; both cut from the text for length. |
| C071 | Reading recommendation. | | moved to page one |
| none | The review table. | every referee report named in it; author and referee model read from the folder names | added |

## Section 11, numbers

| Block | Claim | Source checked | Verdict |
|---|---|---|---|
| C073 | 59 run folders, 55 reports; Astra 16, Fable 15, Opus 14, Sol 14. | my count.py | corrected to the state at my last count: see count-output.txt |
| C073 | 226 records: 46, 57, 12, 19, 25, 67. | routes.py, recounted | corrected to the final count in count-output.txt (244 at my last run) |
| C074 to C079 | Page counts 19, 15, 17, 1, 1, 31. | PDFs opened by count.py | corrected: the involution note has 18 pages. Version 1 of the main paper (18) added. |
| C080 | "These six PDFs total 84 pages." | | removed: a sum of unlike documents |
| C080 | 26,413 word tokens in the step files. | recounted | corrected: `inventory.py` writes the current count, rounded to a thousand |
| C081 | Rainbow total 69,458,112. | fable_referee-topology REPORT (74,432 + 1,327,360 + 4,030,720 + 29,366,528 + 34,659,072, sum) | correct |
| C082 | 4,656,948 through 22; 23,824,742 through 24; populations must not be added. | sol_referee-conjectures REPORT; sol_referee-covers REFEREE-covers C4 | correct. Now a table with who computed each. |
| C083 | Late scan: no report yet from main-revision, descent, involution referee, Lean devices. | folder listing at my last scan | corrected: main-revision, the second involution referee, the consistency edits, the atlas audit, the Lean devices run and the cold read of version 2 have reported and are folded in. `inventory.py` writes the list of open folders into the text. |

## Housekeeping

| Claim | Source checked | Verdict |
|---|---|---|
| Empty author line with a comment. | main, lines 31, 32 | added |
| 53 third-party PDFs, about 50 MB, in two research folders; rights not established. | `du -sb` (38,782,008 and 11,321,093 bytes), `git ls-files` (28 and 25 files); opus_cross-audit CLEANUP-PROPOSAL.md C3 to C5 (which measured 41.6 MB and 11.4 MB) | added |
| `E:\lbb` is about 7.7 GB. | `du -sh` | added |
| Drafts A and B are kept as records. | CLEANUP-PROPOSAL.md E3; `paper/draft-A/`, `paper/draft-B/` exist | added |

## What I could not check

- I did not rerun any census, and I did not open the code behind the counterexamples. The sizes are those the owning reports state, and where two reports state a size they agree.
- I read the OpenAI paper only through `papers/text/OpenAI-Barnette.txt`, to confirm statement numbers and the devices named (phase, exponential, spokes, two induced trees, Pfaffian corollary).
- The "written by" column of the review table comes from folder names and report headers.
- Section 6 is an interpretation. I checked the facts it leans on, not the interpretation.
