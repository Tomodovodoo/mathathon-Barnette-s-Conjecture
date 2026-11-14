# Report, atlas repair

1. `digestions/atlas/verify.py` passes again: 30 routes, 34 pages, no overfull box.
2. Page 29 draws the four-way Lean status, 5 exact, 17 after an unformalised translation, 10 weaker or different, 2 none, read from the blueprint.
3. Page 30 draws the pair descent at 20 vertices by two programs and 23 by its author, and the rainbow descent at 12 and 17.
4. Pages 26, 29 and 30 use the review wording of the fact table. "No polynomial" is stated as six named lemmas.
5. Open: the two contraction bars may deserve a longer solid part. I could not confirm it in the time I had.

## What I set out to do

Repair the atlas after the blueprint data changed under it: fix the page-29 figure script, apply the wording of `research/2026-11-14_opus_reconcile/PAPER-FIXES.md` to pages 26, 29 and 30, redraw the evidence chart of page 30, rebuild, and pass `verify.py`. Fable 5.2 did this alone, with no subagents, and wrote only in `digestions/atlas/` and this folder.

## What I established

All numbers below are quoted. Nothing was recomputed here except the consistency checks named.

- COMPUTED (`digestions/atlas/figs_proofs.py`, function `blueprint_fig`, on the 34 route statements of `proofs/blueprint/blueprint.json`). The statuses count 5, 17, 10, 2. The advisory recount of `research/2026-11-14_astra_lean-check/recount.json` (5, 27, 2) agrees with them statement by statement once "translation" and "weaker" are merged.
- COMPUTED elsewhere, quoted on page 30. Pair descent C3: 3,373,400 pairs through 20 vertices in `research/2026-11-14_astra_referee-descent/REPORT.md` and `INTEGRATION.md`, 193,623,384 pairs through 23 in `research/2026-11-14_fable_descent/REPORT.md`. Both files existed when I read them and agree with FACTS.md.
- COMPUTED elsewhere, quoted on page 30. Rainbow descent, Step X: every case through 17 by its author, and through 12 by `research/2026-11-14_opus_referee-rainbow/code/stepx.py`, which imports only that folder's own modules.
- The build is the documented one. `build.py` runs `pdflatex` itself, so `latexmk` was never needed.
- I looked at the rendered pages 26, 29 and 30 in colour and at 29 in greyscale. No label overlaps another. Figure widths are 0.919, 0.929 and 0.884 of the text width. Word counts are 149, 150 and 149.

Details, file by file, are in `CHANGELOG.md`. Renders are in `before/` and `after/`.

## What failed or was left

- The sign-gauge correction had no target. The atlas never mentions a sign gauge.
- Page 30, "some contraction keeps a pair" (17 by two programs, 19 by one). `research/2026-11-14_astra_induction-lemmas/G.md` line 79 says a second program "reproduces 62,416 rooted instances" through 19. Its stated test compares a structural criterion with a flow test on every merge. I could not tell in the time whether that also confirms the statement on the chart for every instance, so the solid part stays at 17.
- Page 30, "a contraction never has more good states than the original" (17 and 18). The descent referee replayed a two-sided counting inequality on all 1,202,792 contractions through 18. That is a different inequality from the one on the chart, and I found no replay of the chart's statement at 18. The solid part stays at 17. The README records both decisions.
- The "sampled to 150" end of the C3 bar comes from `opus_conjectures` (940 random starts). The descent author's own random runs stop at 80. I kept 150 because the earlier audit ledger accepted it for the same statement. I did not reopen that judgement.
- Nobody has audited this pass.

## Still open

- Whether the two contraction bars should be solid to 19 and 18.
- The page-29 statuses are one model's hand curation. The second model checked a three-class version of them, not the split into "translation" and "weaker".

## Three best next steps

1. Have the owner of `astra_induction-lemmas` say whether `g_structure.py` confirms Lemma G instance by instance through 19. If yes, change one number in `open_fig` and rebuild.
2. Ask a model other than Opus to recheck the ten "weaker or different" statuses against the Lean source, since that split has had no second reader.
3. Apply the remaining PAPER-FIXES item, the sentence at line 1078 of `paper/main/barnette.tex`. It belongs to the owner of `paper/main/`.

## Leads for others

- `paper/main/barnette.tex` line 1078 still reads as if the formal proof used no polynomial at all. PAPER-FIXES has the replacement sentence.
- FACTS.md gives the atlas value for Lemma G as "-". The atlas does state it, on page 30, as 19.
