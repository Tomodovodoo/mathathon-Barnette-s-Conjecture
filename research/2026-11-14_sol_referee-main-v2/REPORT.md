PROVED-HERE: the final version-2 proof passes a fresh reverse-Lamport audit, verdict FOLLOWS.
PROVED-HERE: eight small correction items address summary scopes, explicit dependencies, topology wording and formalisation scope.
COMPUTED: all cube, running-example and prism numbers agree, including every table row and final Figure 11 square.
COMPUTED: a new all-root census through dual order 12 confirms the 9-vertex minimal example; all 131 final references resolve.
COMPUTED and visual inspection: latexmk succeeds, all 19 final pages were inspected, with no TeX errors, undefined references or overfull boxes.

# Regression-referee report

gpt-6.1-sol, 14 November 2026. Work used the assigned folder and the explicitly authorised main TeX/PDF paths. No subagents were used. All other research and proof folders were read only.

## What I set out to do

Check whether the revision from the historical 18-page v1 to the new 19-page v2 preserved every mathematical statement and proof, correctly applied the previous eight corrections, represented the literature and formalisation honestly, and printed correct examples. Produce an independent bounded dependency audit, computations, correction log and checked PDF.

## What I established

PROVED-HERE. REFEREE.md contains the exact theorem contract, accepted background, AND obligation graph, findings by severity, v1 correction checks, changed-block checks, closing-remarks source table and complete dependency table. Its final verdict is FOLLOWS. The first pair, cancellation, height increment, finite-difference nonvanishing, recovery and both induction cases close. No computation or upstream theorem is substituted for a proof obligation.

PROVED-HERE. The initial eight v1 corrections were all correctly applied. In particular Remark 4.10 now calls the signed-height expression a Laurent polynomial and interprets its expansion at z=1 correctly for negative exponents. The new independent example gives coefficient 9 at degree two, equal to Sigma/2!=18/2.

PROVED-HERE. CHANGELOG.md records every edit I applied, eight items in two source/PDF commits. The material scope corrections are: a cycle of chosen sides belongs to P_s minus e0; cancellation pairs pairs with the same second state rather than pairing second states; and weight increase under reversal requires a clockwise starting cycle. The abstract now specifies exactly one side per face and the original graph's complement. The three blueprint suggestions are implemented. The Lean sentence is qualified to distinguish the checked theorem from the exposition's partly informal translations and different route.

COMPUTED. The finite engine is new and imports no previous project implementation. It reconstructs the dual graphs and counts all states, pairs, recoveries and Hamiltonian complements independently. The running example has 12 states, 8 pairs and 6 good states, and moments 0,0,18. The prism has 3 states, 2 good states, and 4,2,2 avoidance counts at the root sides. The cube has 2 states, both good, with one-cycle signed first moment -1. All signs, weights, cycle interiors, component vertex sets, flow labels, height values and gluing labels match the displayed data.

COMPUTED. All 12,288 running-example chosen-side systems were tested, plus all cube and prism systems. The literal eight rows and eight final square entries match exactly. A fresh serial plantri census over every face of each Eulerian simple triangulation through order 12 covers 15 classes and 262 facial roots. It confirms first same-colour root dependence at order 9. The 11-vertex and 26-vertex counterexamples' stated structural properties also pass independent reconstruction.

LIT and PROVED-HERE source comparisons. All 17 cited bibliography entries exist and render. Every numbered citation matches its source. The GSW implication is universal, with planar braces, trisums and tight cuts in the correct order. Optional lattice and cycle-cover findings were omitted from v2, so no refuted conjecture or overstated census range enters the paper. The report records supplied-preprint versus published status, metadata-only checks, the access limits for historical originals, and the difference between the main Lean theorem and this exposition's route.

COMPUTED and visual inspection. `latexmk -pdf -interaction=nonstopmode -halt-on-error barnette.tex` builds successfully once Git's bundled Perl is added to the process PATH. The final PDF has 19 pages. There are zero overfull boxes, zero undefined or multiply defined references, and zero TeX errors. All 131 references were checked semantically as well as resolved mechanically. Every final page was rendered at 130 dpi and opened. The final source SHA256 is `733be1d43245571e435415bc52473cb55f68b04f6cff0bf8d7a904e54976a632`; PDF SHA256 is `e4603901047cf6078889bc83ada40c5a940372222bc773f3a9f1f4cf850ea887`.

## Concurrent finishing pass

While I wrote the first report, the reader agent committed finishing edits in edd9c0c,26fa43b,f04e0d1. I noticed this when the final hash changed, preserved the original v2 input, read that full additional diff and its MATH-ISSUES.md, and extended the review to the resulting final source. The new cube warm-up and good-state/tree-matching terminology are correct. The new Figure 11 squares have the same eight pairs and correct increments. The newly expanded plan needed the clockwise-reversal qualifier, corrected in e97b061. The full final PDF was rendered and inspected again. No other agent's edit was reverted or claimed as mine.

## What failed and why

The first latexmk invocation failed because MiKTeX could not find Perl. An existing Git-bundled Perl resolved this without installing software or changing persistent settings. A provisional script filename shadowed Python's standard-library numbers module; it was renamed verify_numbers.py before retaining any numerical output. One scratch one-line diagnostic had a syntax typo; the checked script output, not that failed diagnostic, supplies the result.

The requested `research/2026-11-14_opus_blueprint/BLUEPRINT.md` path is absent. Its maintained successor is `proofs/blueprint/BLUEPRINT.md`, identified by that research folder's REPORT.md, and that is what I read. The local Feder scan's text map is garbled, so the relevant page was rendered and read. Direct web-tool DOI opens for Georges and Ford failed; Georges's metadata appears in the primary BGM bibliography, and Ford's primary record and theorem were already inspected in the supplied consolidation. I do not claim to have opened full historical proofs that were unavailable.

A follow-up publisher search found Georges's Elsevier record and Ford-Fulkerson's Cambridge record directly. Their existence and metadata were checked there despite the DOI resolver errors.

## What is still open

CONJECTURE. An efficient polynomial-time constructor and the arbitrary-two-edge inclusion/avoidance strengthening remain open in the supplied accounts. They are not required for the theorem and are not settled by this review's finite tests.

PROVED-HERE scope limit. This is an independent model referee of the mathematical route, not human peer review or a new Lean formalisation. The retained Lean build was inspected but not repeated. Historical large census numbers are source claims, not independently recomputed here. All finite domains independently replayed in this task are listed in code/README.md.

## Three best next steps

1. Freeze and archive the final source/PDF pair together with this referee folder; any further mathematical edits need a targeted recheck against its hashes.
2. Have a human referee inspect the shared disk-count, nonvanishing and recovery nodes in REFEREE.md, including the distinction between the two reversals.
3. Finish the author line and release metadata. Keep the formalisation-scope qualification and the explicit finite computation ranges in any release notes.

## Git and files

The first correction/rebuild commit is d3b3651. Initial independent scripts and the change log were committed in 24df755. The final directional correction/rebuild is e97b061. The final research-folder commit contains this report, the full audit, scripts, outputs and all page renders. A push to origin/main is attempted at completion under the brief's shared-tree rule; its result is reported in the final chat.

The main deliverables are REFEREE.md, CHANGELOG.md, this REPORT.md, and code/README.md. Frozen starting and final sources, initial and final hashes, structured and full diffs, separated referee and concurrent edits, exact computation outputs, resolved-reference and source-locator ledgers, build logs and all page renders are under code/outputs/.
