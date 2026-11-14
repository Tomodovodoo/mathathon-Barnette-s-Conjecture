# Changelog: Figure 5 of the sign-free note

All paths are under `proofs/sign-free/`. `sign-free.tex`, `SIGN-FREE.md`, `STATUS.md` and `refs.bib` are unchanged.

## `figures/make_figs.py`

- **Figure 5 layout.** The old `tutte` reweighted its edges for 120 rounds and ended with vertices 4 and 5 at the same point `(-2.887, 0)`. It is replaced by two functions.
  - `tutte(inst)`: the plain barycentric embedding with uniform weights, the roots 0, 1, 2 on the same equilateral triangle as before.
  - `spread(inst, P)`: moves one inner vertex at a time to lower a repulsion energy (`1/d^2` over vertex pairs, `8/d^2` over pairs of a vertex and an edge it is not on). A move is accepted only if every face at the vertex keeps its orientation, so the drawing stays planar at every step.
  - `layout_facts` measures the result, and the script stops unless there is no crossing, the vertices are at least 12pt apart and no vertex is within 4pt of an edge it is not on.
- **Figure 5 panels.** Panel (a), which carries the 16 labels, is now 0.42 of the text width (was 0.325). Panels (b) and (c) are 0.265 each (were 0.325). The three covers of the caption, the single cycle, the face colours, both states, the directed triangles and the labels are drawn from the same computed data as before.
- **Label placement, all five figures.** `Panel.label` no longer places a label at a fixed distance in the widest angular gap. Every drawing call now records what it draws (`Panel.ob`: edges, collar, vertices, wedges, rings, boxes, spokes, tree curves, arrows, cover edges). `Panel.place_labels` then puts each label at the nearest point to its vertex where the label box keeps 1.2pt from every recorded object and from the labels already placed. In Figure 5(a) the label of an inner vertex must also lie inside a face at that vertex. The script stops if any label has less than 0.5pt.
- **Panel tags.** A tag such as `$S_2$` is placed below the lowest label of its panel. In Figure 4 the label 3 sat on top of the tags.
- `figdata.json` gains `layouts` (coordinates and scale of both layouts) and `label_clearance_pt`.

## `figures/check.py`

15 new assertions, 76 in total (61 before, all still passing). From `figdata.json` alone:

- every figure has a layout; in both layouts the vertex positions are pairwise distinct and at least 12pt apart at the smallest panel drawn;
- in both layouts, with the three sides of `t0` left out, no two edges cross and no vertex is within 4pt of an edge it is not on;
- Figure 5 is a planar straight-line drawing with all edges included, every inner vertex lies inside the root triangle, and every face has area at least 30 square points;
- the layout of Figures 1 to 4 has exactly ten crossings, each with a side of `t0` (see REPORT.md);
- every label box clears every drawn object by at least 0.5pt.

## Other files

- `figures/fig-*.tex`, `figures/figdata.json`, `figures/check-output.txt`: regenerated.
- `sign-free.pdf`: rebuilt with two runs of `pdflatex`. 11 pages as before.
- `build-output.txt`: now the second `pdflatex` run of this build.
- `README.md`: the count of assertions, the build command, a note on the layouts and labels.
- `.gitignore` (new): `*.aux *.log *.out *.fls *.fdb_latexmk *.synctex.gz *.toc *.bbl *.blg __pycache__/`.
- `sign-free.log`, `sign-free.out`: removed from the index with `git rm --cached`. They stay on disk.

## Commands

```
cd proofs/sign-free/figures
python make_figs.py            # about 6 s
python check.py                # all 76 figure checks passed
cd ..
pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex    # twice
cd ../../research/2026-11-14_fable_sign-free-figure
python render.py after 1.6     # every page to PNG, for inspection
```

The renders kept in `before/` and `after/` are pages 2, 4, 6, 7 and 9 at zoom 1.05, plus crops of Figures 4 and 5 at zoom 2.6. Pages 10 and 11 changed only because the text after Figure 5 moved down; their renders are not kept.
