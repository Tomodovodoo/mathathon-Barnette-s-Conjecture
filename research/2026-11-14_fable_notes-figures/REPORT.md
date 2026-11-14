# Report: figure defects in the primal and involutions notes

1. All four defects in the proofreader's PROBLEMS.md are fixed, and five more that I found on the rendered pages.
2. Labels in the primal figures are now placed by computation against the drawn objects; the least clearance is 1.51pt and the build fails under 0.5pt.
3. Both PDFs rebuild with pdflatex: no undefined reference, no overfull box, page counts unchanged (primal 15, involutions 18).
4. Not fixed: the 6pt subscripts of the `w` and `t` labels in involutions Figures 1, 2 and 4.
5. The proofreader's size for involutions Figure 3 was wrong (9pt, not 6pt); I enlarged the figure anyway because it was narrow.

## What I set out to do

Redraw the figures whose labels touch other marks, check every figure of both notes at printed size, and rebuild the PDFs without touching prose.

## What I established

Status tags apply to statements about the figures; this task makes no mathematical claim.

**Defects from PROBLEMS.md**

| Defect | Fix | Status |
| --- | --- | --- |
| primal Fig. 4: flow numbers on arrows and vertices | numbers placed beside the edge by search | COMPUTED: `proofs/primal/figures/check.py`, 22 labels, least clearance 1.51pt in `label-placement.json` |
| primal Fig. 8: `cap` touches the cap vertex | same search | COMPUTED: same script, clearances 1.66 and 1.55pt |
| involutions Fig. 1: `w_6` on a blue edge | point drawn as a dot, label moved with a leader | COMPUTED: `fix_involutions.py`, clearance 1.67pt |
| involutions Fig. 3: small labels | `\normalsize`, wider spacing | measured with `fontsizes.py`: 10.9pt text, 8pt subscripts |

**Defects I added**

- primal Figs. 1 and 2: `f_3` lay on a white vertex; `f_6` and `f_11` touched edges; the outer labels `f_0`, `f_1`, `f_4` touched the arc. All moved (4 to 5.5pt).
- primal Fig. 4: five cut edges were invisible under the flow arrows (one in the cube, four in the running graph). The caption speaks of the dashed cut, so they are drawn as a dashed sleeve round the arrow.
- primal Figs. 1 to 5: subscripts of the face labels and of the formula lines were 6pt. Now 7pt.
- involutions Fig. 2: `w_16` covered blue arrows in both panels. Same fix as `w_6`.
- involutions Fig. 3: 8.7cm wide in a 15.9cm block. Now 12.5cm.

**Checks**

- `python proofs/primal/figures/check.py --build` passes all its assertions. `checked.json` and `captions.json` did not change by a byte.
- I looked at every changed figure after the rebuild, at 150 dpi pages and 200 dpi standalone renders.
- No colour-only distinction found: each coloured object also differs in dash, weight or outline.
- No figure is wider than the text block.

## What failed or is uncertain

- The label sizes used by the search are estimates of the glyph boxes (for example 2.4 by 3.1pt half sizes for a 9pt digit), not sizes read back from the PDF. The 1.5pt target leaves room for the estimate; I confirmed by eye, not by a pixel test.
- `label-placement.json` records a figure-level index in its first column, not the panel number.
- In `fix_involutions.py` a label's own ray counts as an obstacle, so `w_5` also became dot plus leader. It was not a defect before. The result is consistent across Figures 1, 2 and 4.
- The proofreader's "about 6pt" for involutions Fig. 3 does not match the PDF: the labels were 9pt with 6pt subscripts.

## Still open

- involutions Figs. 1, 2, 4: `w_k` and `t_k` labels keep 6pt subscripts. Raising them to `\small` needs a re-check of every label in three hand-edited files.
- The leaders of `w_6` and `w_16` cross one blue arrow each; the faces are too small to hold the label.
- `proofs/involutions/figures/page-*.png` and `contact-*.png` are old renders and were already stale. I did not regenerate them.
- I did not run `research/2026-11-14_astra_primal-revision/inspect_figures.py`; it writes outside my paths.
- `involutions.aux`, `.log`, `.out` are tracked and were dirty before I started; my build changed them again and I did not commit them.

## Three best next steps

1. Read the label boxes back from the standalone PDFs with PyMuPDF and assert the clearance on real glyph boxes.
2. Set the involutions `w` and `t` labels in `\small` and place all of them with the same search.
3. Untrack the involutions build by-products and the stale page renders, or regenerate the renders.

## Leads for others

- `proofs/primal/README.md` and `proofs/primal/figures/README.md` do not mention `label-placement.json` or the new placement rule. Both are prose outside this task.
- `Panel.graphG` in `paper/figures/draw.py` registers the curved part of an edge to `b_0` but not its arc, so labels in the main paper's `G` panels are not checked against those arcs.
