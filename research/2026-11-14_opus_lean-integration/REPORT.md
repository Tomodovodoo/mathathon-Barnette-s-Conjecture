# Report: integrating the independent Lean check

1. The blueprint is re-extracted against paper version 2 (commit `e97b061`). The statement numbers are unchanged from version 1, and the uses graph has no consistency problem (COMPUTED, `scripts/extract_tex.py`, `scripts/build_blueprint.py`).
2. New four-way status of the 34 route statements, after the independent check: **5 exact, 17 after an unformalised translation, 10 weaker or different, 2 with no counterpart**. Version 1 had 4 / 25 / 5, and the checker's advisory recount 5 / 27 / 2 merges our middle classes. Of the 32 with a counterpart, 24 are upstream only, 4 project only and 4 both.
3. `proofs/lean/` now states exactly what is machine-checked: Lemma 4.5 only in the case used, flow weights instead of heights, and "no polynomial" only for the six named lemmas. TODO T5 is marked false with the checker's hexagonal-prism counterexample, the corrected target is stated, and six omitted obligations (T7 to T12) are added. The README has an "Independently rebuilt and checked" section.
4. `FORMALISATION.md` lists what remains for Section 4 as written: about 530 to 1,010 Lean lines (HUNCH). `SYNTHESIS.md` has one qualified Lean paragraph, a corrected review table, current counts, and seven late runs folded in. Its figures and section 11 are regenerated, and `check.py` passes.
5. `PAPER-SENTENCE.md` proposes two sentences for the paper's closing paragraph. The current wording is true but understates the record.

## What I set out to do

The brief: make the record of what is machine-checked exactly right everywhere it is stated, now that `research/2026-11-14_astra_lean-check` has independently rebuilt and audited the Lean devices. Concretely: re-extract the blueprint on paper version 2, apply the checker's per-theorem verdicts as a four-way status with an origin marker, fix the Lean documentation (T5, README, delta), update FORMALISATION.md and the synthesis, and draft the paper's sentence.

## What I established

**Inputs are the ones checked** (COMPUTED). All 19 hashes in `astra_lean-check/inputs-sha256.json` match the files in `proofs/lean/` before my edits (script inline in this session; it hashes each listed path). The compiled `.lean` files were not touched.

**Re-extraction** (COMPUTED). `scripts/` holds copies of the version 1 scripts with these changes: `extract_tex.py` reads `HEAD` (commit recorded in `data/source-rev.txt`) and has a new anchor for the reworded `D(r,s)` paragraph. `lean_sigs.py` is run twice, once on upstream (689 declarations, identical to version 1's JSON) and once on `proofs/lean/Devices` (58). `curation.py` gains `V2`, `V2_NOTES`, `V2_NOTES_LEAN2`, `WAYPOINTS_V2` and the new involution Lemma 7. `build_blueprint.py` has the four-way status, the origin line, and new legends and colours. `status_table.py` writes `STATUS-TABLE.md` and `data/tables.md`. `extract_tex.py --worktree` reports no number mismatch against `barnette.aux`. Version 2 fixed three of the four implicit uses that version 1 flagged: Prop. 3.9 now cites the disk identity, the heights paragraph cites Lemma 2.5(2), and the inside paragraph uses Jordan, not Schoenflies.

**Statuses** (a reading, recorded with a reason per statement in `STATUS-TABLE.md`). Rules: the checker wins where the two Lean reports disagree. Statements whose whole content is in the Lean's model count as "after translation", with the translation named. Statements of which the Lean has only part count as "weaker". Three statements left "none": Lemma 4.4 (now after translation, B1 only for the word counterclockwise), Lemma 4.7 (exact) and Lemma 3.7 (weaker). Nine version 1 "different form" statements became "weaker": Thm 1.1 (no avoided edge in `MainStatement`), Lemma 2.5(2), Def. 3.4, Lemma 3.5, Lemma 3.6, Lemma 4.2, Lemma 4.5, the heights paragraph and Lemma 4.6. Prop. 4.8 is "after translation" (B3, B4), not exact as the author's delta proposed.

**Charts** (COMPUTED, looked at). `blueprint.png` (fill by status, third line by origin, border by section) and `columns.png` (Lean column grey for upstream, blue `+` for project). Both render legibly at 150 dpi. Graphviz rejected a `<BR/>` between two HTML tables in the first version of the legend, so I merged it into one table.

**Lean docs.** README: a qualified summary, the location of the build (`E:\lbb`, outside the repository) and how to reproduce it, the checker's commands and results, and corrected "checked / not checked" lists, including the step direction (positive when a clockwise cycle is reversed). TODO: T5 marked FALSE with the counterexample and replaced by T5a/T5b (left inverse on good states, image characterisation). T1 to T4 carry the checker's corrections. T7 to T12 are new. BLUEPRINT-DELTA.md lists the final statuses beside the first proposals.

**Synthesis.** I copied Fable's four scripts into `synthesis-audit/` with path changes only, plus the Lean box in `figures.py`, so that their outputs land in my folder. Reruns: 76 folders, 73 reports, 246 routes. The page counts changed (main 20, atlas 34; the primal note read 16 pages on one count and 15 on the final one) and are fixed in the prose. `check.py` passes after this report exists. Folded in: `fable_atlas-finish`, `fable_descent` (193,623,384 pairs through 23), `opus_referee-rainbow` (rainbow results correct), `fable_referee-families` (one count needs its gluing rule), `opus_digestions-audit-2`, `sol_map-final` (already counted), `astra_lean-check`. Still running: `fable_final-polish` (no report), `astra_referee-descent` (checkpoint only, used as such), `sol_digest-fixes` (no report). `sol_lab-tests` reported, and I did not add a line for it because the synthesis has no row its result changes.

## What failed, and why

- The first `sed` on `figures.py` did not match because of escaped `\n` in the source. I caught it on the rendered PNG and redid the edit in Python.
- `opus_referee-rainbow/REPORT.md` is untracked in the shared tree. I cite it, but it may still change.
- I did not rebuild any Lean myself. The "independently rebuilt" claims rest on the checker's logs, which I read but did not rerun.

## What is still open

- The status judgements are one model's reading of the checker's verdicts. A second reader should check the ten "weaker" entries in particular.
- B3 (heights to flow weights) and B4 (good state) remain the two bridges that would most change the counts. Closing both would move Lemma 4.6, the heights paragraph, Def. 3.4, Lemma 4.2 and Lemma 4.5 out of "weaker".
- Whether the paper glues matchings (Prop. 2.6(2) leaves the route) is the owner's decision.

## Three best next steps

1. Formalise T2 (heights as flow weights, 250 to 400 lines) and T7/T8/T10 (Lemma 4.5 in full, 200 to 350), then ask for another independent rebuild.
2. Decide the paper's closing sentence from `PAPER-SENTENCE.md`, and the gluing question.
3. Rerun `scripts/status_table.py` and `synthesis-audit/` after the still-running runs report.

## Leads for others

- `digestions/route-map/` and `routes.py` were modified in the working tree by another run during this session; I did not commit them.
- The checker's hexagonal-prism example belongs in the atlas page on "which cycles arise" if it is not already there.

## Files

`scripts/` (extraction and build), `data/` (statements, Lean headers, analysis, tables, build output), `synthesis-audit/` (copied counting and figure scripts with their outputs), `STATUS-TABLE.md`, `PAPER-SENTENCE.md`, this report. Outside this folder: `proofs/blueprint/` (all files), `proofs/lean/README.md`, `BLUEPRINT-DELTA.md`, `TODO-statements.lean.txt`, `digestions/SYNTHESIS.md`, `digestions/synthesis-figures/`.
