# Change log for digestions/SYNTHESIS.md and digestions/synthesis-figures/

Editor: Fable 5.2, 14 November 2026. Base: commit `0d2c5cc` (GPT-6 Astra). The reason for each factual change is in FACT-CHECK.md. This file lists what changed, in the order of the document.

## Whole document

- Terminology follows the main paper and `research/2026-11-14_opus_cross-audit/CONSISTENCY.md` section 4: good state (was tree matching), good pair (was forest pair), cover (was pair support, cycle cover), $m$ (was $c_{\min}$). The header gives the old names once. Where "forest" alone would be wrong the text says "a forest with exactly one root in each tree".
- A three-line header says who wrote the document, who checked it, and that no human has.
- Every "refereed" or "checked" now names the model. Where the referee is the same model as the author, the text says so.
- Prose tightened under `skills/unslop/SKILL.md`: no em or en dashes, sentence-case headings, fewer semicolons and colons, active verbs, no "substantial", "chiefly", "materially".
- Length: 4,163 words before, by the counter in count.py. The final count is in check-output.txt. The additions are the header, the blueprint numbers, the review table, the census table and the housekeeping section.

## Section 1

- Rewritten as five labelled paragraphs: how the proof works, what we added, what is solid, what is open, what a human should read first.
- The proof description follows the main paper: selection, good state, tree on the faces, disk identity, pairs, the two groupings, the flow argument for the first pair, gluing.
- Added: where the first pair comes from. Added: the blueprint numbers 4, 25, 5 of 34. Added: the review status of each proof text.
- Corrected: the main paper's referee read version 1.

## Section 2

- Figure redrawn (see below). Table rows carry page counts and review status. The blueprint row links to BLUEPRINT.md.

## Section 3

- Each item now ends with who found it and who checked it.
- "Make pair existence exact" and "Cut only where necessary" merged; the displayed Euler identity removed; the criterion attributed to the constructive manuscript, the proof to Opus, the check to Sol.
- "Supply inside connectivity": both drafts had the gap, not only draft B.
- Recovery: the hexagonal prism example added.
- Families: the prism parameter is $j$; the referee is named as a second Sol run.
- "Obtain inclusion from avoidance" and "Keep the determinant's qualification" merged into "Two smaller points".
- Removed for length: the Morse detail, the remark on reference normalisation of heights.

## Section 4

- Added that the dependency audit found no error in the three papers.
- The blueprint paragraph now gives the numbers and names the four exact matches and the five statements without a counterpart, says the blueprint was extracted from version 1, and says nobody reviewed it.
- Removed: the sentence about differing line estimates (true, but no estimate is quoted now).

## Section 5

- Table rows reworded with the new names. Corrected: "four false states" on the hexagonal prism; "pairs form a lattice". Added: the 33-vertex witness has a separating triangle; review status of the algebra, probability, category and Pfaffian rows.
- Chart caption points to the new count script and assignments.

## Section 6

- Reordered: what is easy inside a cover, then the 16-vertex cover, then what the signed count does. Added the census size 14,881 and "not reviewed".

## Section 7

- Lemma X stated in the direction that is proved to suffice. Added who computed the two large censuses and the pair-descent range. Removed three "first try" suggestions that the linked reports already give.

## Section 8

- Item 2 says Kelmans's papers were never opened. Item 3 adds Tutte's states. Item 7 corrects the authors of the parity condition. Item 9 is specific about the Waterloo proceedings. Item 10 is new (preprint status and the third-party kernel check); the old item 10 is folded into item 2.

## Section 9

- Lessons reworded. Added what version 2 of the paper did with the cold reader's list.

## Section 10

- New table: work, author, checker, what the check did not cover.
- The three corrections are told as short stories with the parties named.
- Updated: the path-mark lemma has a referee (Fable); the atlas has had two models and an audit in progress; version 2 of the paper has a referee run in progress.
- Removed for length: the Florek correction and the prism-chain control (both in FACT-CHECK.md).

## Section 11

- Inventory recounted by `count.py` in this folder: run folders, reports, model labels, route records, page counts.
- Removed: the 84-page total. Added: a table of the cited censuses with range, size and who computed them.
- The late paragraph lists the folders without a final report at the last scan.

## Housekeeping for the owner

- New section: author line, third-party PDFs, the Lean build directory, drafts A and B.

## Figures

- `products.pdf/.png` redrawn by `figures.py` in this folder. Three rows: sources, proofs written here, guides and tools. Each proof box names its checker. The blueprint is a box. Arrows from the Lean proof go only to the primal companion and the blueprint. Page counts and the route count are read from counts.json.
- `route-outcomes.pdf/.png` regenerated from the recount. New totals row. The footer names the count time and this folder. The keyword rules are the first version's, unchanged.
- `README.md` in the figures folder rewritten to match.

## Late arrivals folded in while editing

- Version 2 of the main paper (astra_main-revision REPORT) and its cold read (opus_coldread-main-v2 REPORT): sections 1, 2, 9, 10.
- The second involution referee (fable_referee-involutions-v2 REPORT): sections 1, 2, 10.
- The consistency edits (opus_consistency-edits REPORT): the route map now has 227 records, and its names agree with this document.
- The atlas audit (sol_atlas-audit REPORT): sections 2 and 10.
- The Lean devices run (opus_lean-devices REPORT, proofs/lean/): a new product row, a new paragraph in section 4, open problem 6 rewritten, a row in the review table, the blueprint box of the products figure.
- Section 11's inventory and its list of open runs are written by `inventory.py` from counts.json, because the numbers changed several times while I worked.
