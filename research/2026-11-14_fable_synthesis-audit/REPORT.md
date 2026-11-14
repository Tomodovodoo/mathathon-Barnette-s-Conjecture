# Report: fact-check and final edit of the synthesis

Fable 5.2, 14 November 2026. Folder `research/2026-11-14_fable_synthesis-audit/`. I also own, for this task, `digestions/SYNTHESIS.md` and `digestions/synthesis-figures/`. No subagents.

1. Every mathematical number in the first version of the synthesis agrees with its source. I found no wrong counterexample size, no wrong census figure and no "refuted" that its counterexample does not support.
2. Of 105 ledger rows, 20 are corrected or softened. About half of those were only out of date when I read them. The others were wrong or wider than their source. The ones that matter: the referee of the main paper had read version 1, not version 2; two "referee" reports are by the same model as the author; a parity condition was credited to the wrong paper; the blueprint's numbers (4, 25, 5 of 34) were missing.
3. The document is rewritten in the main paper's names, with a first page that answers five questions, a table of who wrote and who checked each piece of work, and a housekeeping section for the owner.
4. Nine late runs are folded in: version 2 of the paper, its cold read and its referee, the second involution referee, the consistency edits, the atlas audit, the Lean devices run and the descent study. Two runs were still open at my last scan.
5. Both figures are regenerated from a recount (`count.py`, `figures.py`). `inventory.py` writes the snapshot numbers into the text and `check.py` verifies them.

## What I set out to do

Read the synthesis as its reader, check every factual sentence against its source, fold in the runs that finished after its snapshot, move it to the project's naming convention, recount section 11, edit it for honesty and length, check both figures, and add the owner's open decisions.

## What I established

All claims below are about the repository, not new mathematics. Mathematical statements in the synthesis keep the status their source gives them, and FACT-CHECK.md names that source row by row.

**The first version was accurate on the mathematics.** `COMPUTED` in the sense of sums redone by hand from the reports: 62,416 = 7,386 + 16,032 + 38,998 (Lemma G), 1,202,792 = 344,872 + 857,920 (contraction inequality), 69,458,112 as the sum of the five rainbow enumerations. Every counterexample size I checked matches the report that owns it: lattice extremes fail first at 18, the extreme-or-irreducible rule at a 33-vertex witness, a cover without a good state at 16, "some good state lifts" at 18, the half-integral LP vertex at 13, the reflected failures at 12, residues modulo 2, 3, 4, 5, 7, 11 at 6, 13, 9, 14, 16, 26. The phase adjudication ($i^n$, 24,856 pairs) and the 279 against 213 resolution (roots 4 and 5 swapped, 69 drawings, 35 values) are stated as their sources state them.

**What was wrong or misleading.** The full list is in FACT-CHECK.md. In order of weight:

- "Its main theorem has an independent AI referee" described version 1. The referee of version 2 reported while I worked, and the text now gives both.
- `sol_referee-covers` referees `sol_counting-families` and `sol_route-probabilistic`. Author and referee are the same model. The first version called this a referee check without that caveat.
- The parity condition refuted on the truncated octahedron is that of Bagheri Gh., Feder, Fleischner and Subi (2021), not "Feder-Subi".
- "Draft B left that premise unwritten": both drafts did.
- The exact pair criterion is stated in the constructive manuscript; the project's contribution is a proof and its review.
- "Four false states" on the hexagonal prism: four of six solutions of the relaxation are not states at all.
- "Pairs form a lattice": covers do.
- Out of date by the time I read it: the path-mark lemma has a referee, the atlas has an audit, the involution note has 18 pages, the route map has 227 records.
- The blueprint's headline numbers were absent, as were the caveats that Kelmans's papers were never opened and that the 33-vertex lattice witness has a separating triangle.

**Counts** (`COMPUTED`, `count.py`, output in count-output.txt and counts.json; command in the script header). The final numbers are in section 11 of the synthesis and are checked against counts.json by `check.py` (output in check-output.txt).

**Figures.** Both were rendered and looked at. The products figure is redrawn: the first version sent the Lean proof into all "companion proofs", gave no review status, and had no blueprint. The route chart has the same keyword rules as the first version, a totals row and the new count.

## What failed, and what I did not do

- I did not rerun any census or open the code behind any counterexample. The check is of the synthesis against the reports, and of reports against each other where two state the same number.
- I read in full the referee reports, the blueprint, the cross-audit, the history review, the merge and revision reports, the packing report and the two induction reports. For the other route reports I read the summary and searched for the number in question. FACT-CHECK.md says this at its top.
- I read the OpenAI paper only through its text dump, for statement numbers and the names of its devices.
- The text is longer than the first version (the count is in check-output.txt against 4,163 before). The additions are the ones the brief asked for. I cut detail elsewhere, and CHANGELOG.md lists what went.
- The main paper's PDF changed page count between my counts (19, then 20, then 19) while two other runs were editing and rebuilding it. The final referee report fixes it at 19 pages, and `check.py` ties the number in the text to the PDF.
- A heredoc mangled backslashes in my figure script once. I repaired the file and rebuilt before committing.

## What is still open

- The runs without a report at my last scan are listed in the last paragraph of section 11 of the synthesis. One of them bears on a headline claim: `astra_lean-check`, an independent check of the Lean devices.
- The tally "8 exact, 24 translated, 2 without a counterpart" after the Lean devices run is my count from `proofs/lean/BLUEPRINT-DELTA.md`. The blueprint's owner has not updated the blueprint, and the delta qualifies two of the four new exact matches.
- The review table in section 10 takes authors and referees from folder names and report headers. Nobody else has checked it.
- No human has read the synthesis.

## Three best next steps

1. When the open runs report, run `count.py`, `inventory.py`, `figures.py` and `check.py`, and update by hand "What is solid" on page one, the two Lean paragraphs of section 4 and the review table of section 10.
2. Have a different model referee the Sol-on-Sol items (prism and tube family counts, the Hamiltonian lower bounds $2^b$ and $3\cdot2^b$, the probabilistic claims) so that every "proved" in section 3 has a second model.
3. Give the owner the three files a human should read, in order: the main paper, the version 2 referee report, and section 10 of the synthesis.

## Leads for others

- `digestions/atlas/`: the atlas audit (`sol_atlas-audit`) found that page 10 states an implication that is false as written (an acyclic $Q_s$ is not enough without a partner). Its edits were not applied when I finished.
- `proofs/blueprint/BLUEPRINT.md` was extracted from version 1 of the paper. The final version 2 keeps every statement number (I recomputed them from both sources after the last edits). The Lean devices run changes the status column, so the blueprint needs a rerun.
- `research/INDEX.md` lists 46 rows for 66 folders, and several rows still say "running".
- `research/2026-11-14_opus_cross-audit/CLEANUP-PROPOSAL.md` measured the two literature PDF folders at 41.6 MB and 11.4 MB. They are now 38.8 MB and 11.3 MB, 28 and 25 tracked files.

## Files

- `FACT-CHECK.md`: claim, source, verdict, for every block of the first version and for the added claims.
- `CHANGELOG.md`: what changed in the synthesis and the figures.
- `count.py`, `counts.json`, `count-output.txt`, `route-classification.json`: the inventory.
- `inventory.py`: writes the snapshot blocks of section 11 and the two route counts from counts.json.
- `figures.py`: both figures. `check.py`, `check-output.txt`: links, typography, numbers. `sub.py`: the exact-substitution helper I used for edits.

Commands, from the repository root:

    python research/2026-11-14_fable_synthesis-audit/count.py
    python research/2026-11-14_fable_synthesis-audit/inventory.py
    python research/2026-11-14_fable_synthesis-audit/figures.py
    python research/2026-11-14_fable_synthesis-audit/check.py
