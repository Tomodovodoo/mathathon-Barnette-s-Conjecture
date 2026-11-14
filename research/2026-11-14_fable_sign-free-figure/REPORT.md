# Report: Figure 5 of the sign-free note

1. COMPUTED. Figure 5 now has a planar straight-line layout: no crossing, vertices at least 13.5pt apart, every vertex at least 4.8pt from any edge it is not on. Before, vertices 4 and 5 shared the point `(-2.887, 0)`.
2. COMPUTED. Labels in all five figures are placed by a search and clear every drawn object: by at least 1.2pt in Figures 1 to 4 and 0.66pt in Figure 5.
3. COMPUTED. `check.py` passes with 76 assertions (61 old, 15 new on layouts and labels). The PDF builds with `pdflatex` alone: 11 pages, no undefined reference, no overfull or underfull box.
4. COMPUTED, not fixed. Figures 1 to 4 have no coincident vertices, but their layout is not planar: the three sides of `t0` cross ten inner edges. It is the paper's layout, so I recorded it and left it.
5. Not done: the white space on page 5. The only placement change that fills it puts Figure 3 inside the proof of the evenness theorem.

## What I set out to do

Repair Figure 5 of `proofs/sign-free/sign-free.tex` in its generating script, check the other four figures for the same fault and for labels touching marks, reduce the white space on page 5 if that was trivial, rebuild the PDF, and untrack the note's LaTeX build files.

## What I established

**Figure 5.** COMPUTED (`proofs/sign-free/figures/make_figs.py`, functions `tutte`, `spread`, `layout_facts`; asserted again in `figures/check.py` from `figdata.json`). The old layout reweighted a barycentric embedding for 120 rounds and collapsed the edge 4–5. The new one is the plain barycentric embedding followed by a repulsion step that only accepts moves keeping every face's orientation. At the scale of the smallest panel (12.4pt per unit): smallest vertex distance 13.5pt, smallest vertex-to-edge distance 4.8pt, no crossing, every inner vertex inside the root triangle, every face at least 30 square points. The 4.8pt comes from the fan at root 0, which has seven faces inside a 60 degree corner; it cannot be made much larger with an equilateral frame.

Panel (a) grew from 0.325 to 0.42 of the text width so that all 16 labels fit inside faces next to their vertices. Panels (b) and (c) shrank from 0.325 to 0.265. That is the price of the labels: with three equal panels at least one label had no clear position. Everything the figure shows is drawn from the same computed objects as before, and the 61 old assertions about them still pass.

**Labels.** COMPUTED (`Panel.place_labels`). Each label goes to the nearest point to its vertex where its box keeps 1.2pt from every drawn object and every earlier label. Smallest clearance per figure, in pt: 1.22, 1.21, 1.21, 1.23, 0.66. The model of the label box (digit width 4.25pt, height 5.15pt, inner separation 0.5pt) and of the smooth tree curves in Figure 1 (a polyline with 1.6pt half width) are estimates, so I also looked at every figure page rendered to PNG. I saw no label touching a mark. In Figure 4 the label 3 used to sit on the panel tags; tags now go below the lowest label.

**Other four figures.** COMPUTED. Their 13 vertices are distinct and at least 19.8pt apart at the smallest panel, so the Figure 5 fault does not occur. A different defect does: see below.

**Build.** COMPUTED. Two runs of `pdflatex`; the log has no `Overfull`, `Underfull`, `undefined` or `Rerun` line. The bibliography is inline, so bibtex is not used. `sign-free.tex` is unchanged, so the captions are unchanged and `SIGN-FREE.md` was not regenerated. `sign-free.log` and `sign-free.out` are untracked and covered by a new local `.gitignore`. No `.aux` file was tracked.

## What failed or was left, and why

**The layout of Figures 1 to 4 is not a planar drawing.** COMPUTED (`check.py`, the assertion "running layout: exactly ten crossings, each with a side of t0"). In `figures/layout-running.json`, copied from `paper/figures/`, vertices 3, 6 and 11 lie outside the root triangle 0, 4, 5. The three faces next to `t0` are folded outwards, and the sides of `t0` are drawn as chords that cross ten inner edges: side 0–4 crosses 2–3 and 3–9; side 0–5 crosses 1–6, 6–7, 6–11 and 6–12; side 4–5 crosses 6–11, 8–11, 10–11 and 11–12. Vertex 2 is 0.134 units from the side 0–4, which is 1.5pt in Figure 4 and 2.9pt in Figure 1, and vertex 9 is nearly as close. With the three sides left out the drawing is planar and no vertex is within 4pt of an edge. The referee did not report this. I did not change it: the layout belongs to the paper, the note's captions say the figures show the paper's example, and a new layout here would make the note and the paper draw the same example differently. The new assertion states the fact exactly so that a later change of layout is noticed.

**Page 5.** Figure 3 is an `[H]` float between the proof of the mirror lemma and the evenness theorem. Page 5 still ends about 175pt early. Letting Figure 3 float would pull the theorem and the start of its proof onto page 5 and put the figure at the top of page 6 inside that proof. The README states that no figure sits inside a statement or proof, so this is not a safe change, and I made none. I did not test other placements.

**Earlier attempts at the Figure 5 layout, kept as lessons.** REFUTED as layouts. An energy of `1/altitude^2` over face corners gave a planar drawing with the inner vertices bunched at the centre, because it punishes the thin faces at the roots as much as any other. An isosceles frame with an 84 degree corner at root 0 lost a third of the area and several labels had no clear position.

## Still open

- Whether Figures 1 to 4, and the paper's figures that share the layout, should be redrawn planar.
- Panels (b) and (c) of Figure 5 carry no labels, while the caption names the triangles 5→13→14→5 and 9→12→14→9. The reader has to carry the numbers over from panel (a).
- The white space on page 5.

## Three best next steps

1. Decide, for the paper and the note together, whether the example's layout should be planar. If yes, `spread(tutte(...))` from `make_figs.py` works on it unchanged, and the ten-crossings assertion in `check.py` should then be replaced by the Figure 5 assertions.
2. Label the three vertices of the directed triangle in panels (b) and (c) of Figure 5. The label placer handles a subset of vertices already (Figure 4 uses it that way).
3. If the page 5 gap matters, shorten Figure 3 or move the remark that follows the evenness theorem; both are prose or size decisions for the author.

## Leads for others

- `paper/figures/` holds the layout with the ten crossings (`layout-running.json`, fields `relaxed`, `max_angle_deg: 227.5`). Whoever owns the paper's figures should know.
- `git commit -m ... -- <dir>` re-adds a file that was just removed with `git rm --cached` when the file is still on disk. To commit an untracking, stage it and commit without a pathspec after checking `git diff --cached --name-only`.

## Files

- `CHANGELOG.md`: every change and the commands.
- `render.py`: renders the PDF pages.
- `before/`, `after/`: pages 2, 4, 6, 7, 9 and crops of Figures 4 and 5 (1.8 MB together).
