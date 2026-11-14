# Report: finishing the illustrated atlas

1. The atlas now has 30 route pages on 34 PDF pages. `verify.py` passes: no TeX error, no overfull box, texts 130 to 150 words, figures 0.80 to 0.95 of the text width.
2. Two pages are new, both computed and asserted: three written proofs of the key step on the running example (page 10), and the main paper's 34 route statements against the Lean proof (page 29).
3. The spacing fault is fixed once, in a shared macro, and I listed and fixed 20 further defects found on the renders (labels on marks, captions running into panels, colour-only captions, crowded chart labels, three overfull pages).
4. Both declined audit items are settled: all 466 unrepaired lifts share one shape, checked here on the recorded cases, and the reading order is adopted in part with reasons in the README.
5. Not fully done: the final build was looked at in full size only in part. `INSPECTION.md` says exactly which pages.

Fable 5.2, 2026-11-14. Folder `research/2026-11-14_fable_atlas-finish/`. I own `digestions/atlas/` for this task. No subagents.

## What I set out to do

Finish `digestions/atlas/atlas.pdf`: inspect every page in colour, greyscale and a colour-blindness simulation and fix what shows; fix the heading spacing everywhere; add two computed pages; settle the two audit items the previous pass declined; rebuild, verify, and update contents, sources, README and renders.

## What I established

All `COMPUTED` statements are produced by `python digestions/atlas/build.py` (about one minute), asserted in `digestions/atlas/figs_proofs.py` and `figs_scope.py`, re-run by `python digestions/atlas/verify.py`, and recorded in `digestions/atlas/computed.json`. Each is about one finite example and proves nothing general.

- `COMPUTED`, running example (13 vertices, 8 pairs, 12 states), with face paths along shortest paths in `G` to the outer face. Reversing a clockwise cycle of `D` raises the path height of a white face by 1 if the face is inside the cycle and by 0 otherwise, on all 176 (pair, cycle, white face) triples. This is Lemma 4.6 of `paper/main/barnette.tex` on this example.
- `COMPUTED`, same example. The paper's sum `Σ ε(r,s) ω(s)^2` over pairs is `+18 = 2!·9`, and equals the sum over the six good states. The primal note's polynomial with weights read from the flow of the same paths has lowest coefficient `+9` at degree 2. The bijective note's signed count of pairs with two path marks is `-9` over 43 objects, and its 9 unpaired objects all have sign `-1`. Here `9 = 6·1 + 3·1`, the white faces inside the cycles of the two covers.
- `COMPUTED`, same example. The summed turn signs of the paths are local potentials of the flow, in the sense of the primal note's equation (5.2). That is the concrete form of "the primal flow is the same weight read in G".
- `COMPUTED` from `proofs/blueprint/blueprint.json`: 34 route statements, statuses 4 exact, 25 after translation, 5 without counterpart; 67 uses, acyclic, 51 after transitive reduction; no statement uses a later section. From `research/2026-11-14_astra_lean-check/recount.json`: 5, 27, 2, with exactly three statements moved. These are counts of two hand curations. I did not re-derive any status.
- `COMPUTED`, 466 recorded cases (`research/2026-11-14_fable_induction-completion/data/exceptions_*.jsonl`, `V` = 13 to 16). Each stored triangulation is valid, and in each, with `x` removed, the opposite edges plus two root edges form two trees, one through `a` and `v1`, one through `b` and `v2`. So the sentence the previous pass declined is true for the 466, and page 23 has it.
- `LIT` (project reports, read, not recomputed): the review statuses on pages 9, 10 and 29, and everything on the chart of page 30. The review statuses of the three written proofs on page 10 are the wording of my brief. I did not open the referee reports of the main paper or the bijective note in this pass.

Files in this folder: `INSPECTION.md`, `CHANGELOG.md`, `render_pages.py`, `before/` and `after/` (nine contact sheets each, 42 dpi).

## What failed, and why

- **Full inspection of the final build.** I looked at all 31 old pages in colour and 27 of them in greyscale at full size, fixed what I found, rebuilt, and looked at 22 pages of the new build in colour. Then a last round of fixes changed the panel size on three pages and the gap above the cross-references on all. After that I looked at ten pages at full size and the rest on contact sheets. Pages 17 and 18 at their final size, and pages 8, 14, 20, 21 after any change, were seen on sheets only. Time ran out; I had spent it on the two new pages.
- **Page 29, status sentence.** The brief gave two wordings, depending on whether the independent Lean check existed. Its report appeared mid-task and neither wording fits: the rebuild confirms, but the checker calls its own recount advisory, left the blueprint unchanged, and corrected three claims. I show the blueprint's count as the fill, the recount as marks and in the text, and say both things in the status. This is my reading of that report. Its author has not seen the page.
- **Page 10, first layout.** Captions of full width pushed the page over by 21pt. Fixed by smaller panels and shorter captions, not by cutting content.
- **Two patch scripts died on shell quoting.** As the two earlier passes reported, here-documents halve backslashes here. I moved the patches to files.

## What is still open

- Nobody has audited this pass or the third. No human has read any page.
- The paths on page 10 are the copied toolkit's. Whether the primal note's own figure uses the same ones, I did not check. The bijective note's second pairing is not recomputed, only its fixed points and the signed total.
- Page 29 would be stronger if the blueprint's owner applied or rejected the recount. Then one count would do.
- The 466 are checked as recorded. Rerunning the census that produces them is a separate job (about two minutes with `fable_induction-completion/code/census.py`, by its README).

## Three best next steps

1. Have a second model inspect the final build page by page at full size, starting with pages 8, 14, 17, 18, 20 and 21, and audit pages 10 and 29 against `paper/main/barnette.tex`, `proofs/primal/primal.tex`, `proofs/involutions/involutions.tex` and `proofs/blueprint/BLUEPRINT.md`.
2. Ask the blueprint's owner to settle the three moved statements, then regenerate page 29 with a single count.
3. Draw the exception shape of the 466 on page 23 in place of the sentence: one recorded 13-vertex case, the two trees in two line styles.

## Leads for others

- `digestions/atlas/figs_proofs.py` computes face-path heights, the path flow and path marks on any toolkit `Model`. `paper/figures/` could assert Lemma 4.6 on its heights figure with ten lines from it.
- `research/2026-11-14_astra_lean-check/REPORT.md` says `proofs/lean/README.md` overstates three things (a refuted target T5, "full Lemma 4.5", "no polynomial lemma"). The atlas does not repeat them, but the README still does.

## What in the atlas remains schematic, unverified or quoted

Schematic:
- Page 27 (a) and (b): hand-placed coordinates. The graphs are built and asserted in code.
- Page 29: the chart's layout is by section and reading order, chosen by me. Arrows between the first two columns run close together and cannot all be followed.
- Page 10 (b): arrow widths grow with the flow but not in proportion.

Shown for one case only:
- Page 10: one face path, one flow, one of nine unpaired objects, one choice of paths.
- Page 7 (c), (d): one move of one ray mark, the case with a reversal.
- Page 22: the six connection patterns of one 4-cycle of one example. The general list is quoted.
- Page 24 (c), (d): the relaxed reading of Feder and Subi. Their degree condition is stated, not tested, and I did not open their paper.

Quoted, not recomputed:
- Page 30: every range and every counterexample size on the chart. "Two programs" means the original report and one referee model.
- Page 29: every status, from one model's curation; the second count from another model's advisory recount; the four translations are my summary of the blueprint's bridge notes.
- Page 23: which lifts fail and which the rotation repairs, up to 16 vertices; the failures at 18 vertices.
- Pages 15, 19, 20, 26: the ranges and formulas named in their status sentences.
- The review status of every page. "Checked by a second model" is a statement about project reports. It is not peer review.

Quoted from unrefereed reports:
- Page 19: the first step (a spanning tree with one passage per vertex).
- Page 22: the general list of patterns for a cut of length four.
- Page 24: the translation of Feder and Subi.
- Page 28: the torus computation comes from an unrefereed report, and is recomputed here.

Unverified in this pass:
- The final appearance at full size of the pages listed under "What failed".
- The agreement of the atlas's wording on pages 10 and 29 with the three notes and the blueprint, by anyone but me.
