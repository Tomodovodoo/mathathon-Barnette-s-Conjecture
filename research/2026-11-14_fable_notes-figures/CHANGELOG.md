# Changelog: figures of the primal and involutions notes

No prose changed. `primal.tex` and `involutions.tex` are untouched. No figure shows a different mathematical object than before.

## proofs/primal/figures/check.py (generator of all eight primal figures)

- New helpers `full_path`, `along`, `box`, `place`, `anchors`. `place` puts a label box at the point nearest its anchor that keeps 1.5pt from every object the panel has registered (`Panel.obs` and `Panel.label_clear` from `paper/figures/draw.py`, imported, not edited). The build fails if a label ends nearer than `LABEL_MIN` = 0.5pt.
- `panel()` now also registers the arcs that lead to `b_0`; the shared `graphG` registers only the curved part of those edges.
- Figures 1 and 2: each face label has one computed anchor, shared by Figures 1, 2 and 5. Seven labels moved by 4 to 5.5pt: `f_0`, `f_1` (cube); `f_0`, `f_3`, `f_4`, `f_6`, `f_11` (running graph). The state segments of Figures 2 and 5 end at the same anchors.
- Figure 4: flow numbers sit beside their edges, not on them, clear of edges, vertices, halos, arrowheads and each other. Five cut edges that carry flow were hidden under the blue arrow (one in the cube, four in the running graph); their dashes are now drawn as a sleeve round the arrow.
- Figure 8: both `cap` labels placed by the same search.
- Face labels, `b_0` and the formula lines under Figures 3, 4, 5 are set in `\small`, so their subscripts are 7pt (were 6pt).
- New output `label-placement.json`: every placed label with its clearance. Least clearance 1.51pt.
- `checked.json` and `captions.json` are byte-identical to the committed versions.

## proofs/involutions/figures (edited by research/2026-11-14_fable_notes-figures/fix_involutions.py)

- `marked.tex` (Figure 1, right panel): `w_6` covered blue cycle edges. Its point is now a green dot; the circled label stands 18pt away with a leader. `w_5` treated the same way (10pt).
- `second.tex` (Figure 2, both panels): the same for `w_16` (17pt) and `w_5`.
- `paths.tex` (Figure 3): text at `\normalsize` (was `\footnotesize`), column spacing 2.3cm (was 1.6cm). The figure is now 12.5cm wide, was 8.7cm.
- `first.tex`, `panels.tex`: unchanged.

## Built files

- `proofs/primal/primal.pdf`: 15 pages, as before.
- `proofs/involutions/involutions.pdf`: 18 pages, as before.
- Eight standalone PDFs and PNGs in `proofs/primal/figures/`.

## Research folder

- `render.py`, `fontsizes.py`, `fix_involutions.py`.
- `before/`, `after/`: the five figure pages that changed, 150 dpi.
