# Figures for the Barnette exposition

Sixteen vector figures and a gallery. `gallery.pdf` sets every figure at its final size in the paper's text block (10pt `amsart`, A4, 1in margins, 15.92cm wide), at most two per page, with a line of body text between them so scale can be judged.

## Build

From the repository root, with Python 3 and `pdflatex` on PATH:

```powershell
python -m pip install networkx numpy scipy pymupdf pillow
python paper/figures/build.py
```

`build.py` runs `check.py` (every assertion), then `draw.py`, compiles the sixteen standalone files and the gallery, and renders each PDF to `renders/` at 150 dpi (gallery pages at 100 dpi). It stops at the first failed assertion or TeX error. `python paper/figures/build.py 08 gallery` rebuilds only the files whose names contain those strings.

Optional:

```powershell
python paper/figures/layout.py running octahedron   # recompute the saved coordinates
python -m pip install sympy
python paper/figures/crosscheck_lab.py              # independent check against workings/barnette_lab
```

Normal builds read the saved coordinates in `layout-*.json`, so the pictures do not drift.

## Files

| File | Role |
| --- | --- |
| `running.json`, `octahedron.json` | The two triangulations: oriented faces, the outer face `t0`, the prescribed edge `e0`. |
| `running-primal.adjlist` | The cubic graph G of the running example. `check.py` asserts that its dual is `running.json`. |
| `model.py` | Combinatorics: states, pairs, `Q`, `D`, `J`, cycle reversal, disk counts, the recovery of Section 6, the incidence graph and cut inequality. |
| `layout.py` | Disk layout: roots on a circle, interior relaxed for corner angles and face areas. |
| `check.py` | Computes and asserts every drawn object. Writes `checked.json` and `validation.json`. |
| `draw.py` | Layers (`Panel`) and the fifteen figures. Writes `NN-name.tex`, `NN-name-body.tex`, `gallery.tex`, `captions.json`. |
| `barnette-figs.sty` | All visual encodings. |
| `crosscheck_lab.py`, `lab-crosscheck.json` | Comparison with the lab implementation. |

## The examples

The running example is a 13-vertex Eulerian triangulation without separating triangles, with outer face `t0 = {0,4,5}`. Its dual G has 22 vertices. It replaces the 14-vertex example of the first pass, which had a vertex of degree 8 at a root and could not be drawn without slivers.

- COMPUTED (`research/2026-11-14_fable_figures-review/search_example.py`, all 4-connected Eulerian triangulations with 8 to 14 vertices from `plantri -bc4`, every face as `t0`): this triangulation is the only one with at most 13 vertices that has both a pair with cyclic `Q_s` and a cycle of `D` enclosing a vertex. Its maximum degree is 6.
- COMPUTED (`check.py`): 12 states, 8 ordered pairs, 2 pairs with cyclic `Q_s`. The displayed pair `(r,s)` is the unique pair with `Q_s` cyclic, `Q_r` a forest, and a `D`-cycle enclosing a vertex. That one pair carries Figures 5 to 13: `(r,s)` and `(r~,s)` cancel, and `(s,r)` is a forest pair that yields the Hamiltonian cycle.
- COMPUTED (`check.py`): the long cycle of `D` has `B=5, W=6, I=3, h=7, l=2`. The disk identity holds on every directed cycle of `D` and `Q_s` over all 8 pairs. With unit spoke circulations, `L+ - L-` equals the number of white faces inside each `D`-cycle (6 and 1).
- COMPUTED (`check.py`): the cut inequality (3.1) for all 1024 subsets of `X`; `H - r` and the white-face tree are trees; `P` has one edge per face and two components, both classes induce trees, and the complementary dual is one cycle through all 22 faces.
- COMPUTED (`crosscheck_lab.py`): `workings/barnette_lab` gives the same counts, the same two cyclic pairs, the same `P` and the same Hamiltonian cycle.
- COMPUTED (`check.gluing`): the 9-vertex gluing example (an octahedron inside a face of an octahedron) has one separating triangle; the partitions of the two pieces agree on it and glue to two induced trees.
- LIT: Figure 15 records the dependence of Sections 2 to 7 of `papers/OpenAI-Barnette.pdf`. Figure 4 is a schematic of one triangle.

None of this is a proof of a general statement. The figures illustrate the proof on finite examples.

## Layout

The outer black face `t0` is the unbounded region. Its three edges are arcs of one circle and the roots sit on it 120 degrees apart, with `e0` at the bottom. A grey collar around the disk is the same grey as the black faces and says that the outside is a black face. The vertex of G in `t0`, which is also the centre `c0` of `t0`, is the small square or dot below the disk; edges that reach it run inside the collar. The cubic graph G is always drawn on this layout: its vertices are the face centres and each of its edges crosses one edge of T.

Saved layout of the running example: smallest corner 20 degrees, bounded faces away from the outer arcs within a factor 2.4 in area. The three faces on the outer arcs are larger by design.

## Encodings

| Object | Encoding |
| --- | --- |
| Edge of T | grey, 0.4pt |
| Black face | 17% grey fill; the collar for `t0` |
| Vertex, root | dot; hollow circle |
| State `s` (second state) | solid blue wedge inside the black triangle at the chosen corner |
| State `r` (first state) | outlined vermilion wedge, white inside |
| `D` | blue arrows, 1.1pt |
| `Q_s` | vermilion dashed, 1.1pt; arrows where a direction matters |
| Spoke, kept spoke, deleted spoke | thin grey; bold black; dotted |
| Centre of a black triangle | small black square |
| Tree on the white faces | green dash-dot, hollow green circles, root `y0` ringed |
| Selected edges `P` | black, 1.6pt |
| Graph G | grey 0.4pt, vertices filled or hollow by class |
| Cycle or 2-factor in G | purple, 1.3pt |
| The two tree classes | black disks and white squares |

Colours are Okabe-Ito. Every pair of objects that appear together also differs in shape, weight or dash.

## Using a figure in the paper

Put this directory on TeX's input path, load `barnette-figs`, and write `\input{08-disk-body.tex}` inside a centred `figure`. Captions are in `captions.json` (field `caption`; `drawn_from` says which checked object the figure shows). Do not rescale: the bodies are at final size, labels are `\footnotesize`, and line weights match across figures. Half-width panels are 7.2cm, which is 0.45 of the text width.

The first pass (14 figures on the 14-vertex example in a straight outer triangle) is at commit `af6c63a`.

## Finishing pass, 14 November 2026

Every original filename is retained. `16-at-a-glance-body.tex` and its standalone
PDF add the six-panel introduction strip at natural text width. Its small graphs
are orientation aids; Figures 3 to 13 carry the detailed constructions. The cube
uses a square-in-square embedding; the following panels use its checked octahedral
dual. The worked example and caption occupy about half a text page.

The gallery has nine pages, with body text and at most two figures on each page.
The worked cube and the introduction strip each have their own page. Figure bodies
and captions are kept in nonfloating minipages, so a float cannot leave an empty page.

White centres are incentres. For the three curved boundary faces this means the
largest inscribed circle of the circular-sided region, computed by SciPy SLSQP.
The remaining centres retain the second-pass positions. White-tree curves pass
through the midpoint of the deleted spoke with a transverse tangent. Curves of G
pass through their corresponding T-edge midpoints. Both use the same numeric
cubic controls for TikZ output and intersection validation, rounded to three decimals.

COMPUTED (`check.py`, `geometry_check.py`, `geometry-validation.json`): every G edge
and every white-tree edge on both examples crosses exactly its corresponding dual
edge or spoke, once. Every cubic is sampled at 160 intervals; circular boundaries
and collar arcs at 360 intervals. This is a sampled numerical check, not an exact
geometric proof. All measured crossing angles exceed ten degrees. Outer spokes
are included among the forbidden crossings.

The first-pass `research/2026-11-14_astra_figures/FIGURE-STYLE.md` is historical.
The current encodings are those of this README and `barnette-figs.sty`.
`style-audit.json` inventories every generated body, the generator and style file,
including all explicit width, font and colour declarations, and rendered PDF font
sizes. It records the intentional departures from that historical specification.
Text labels remain footnote size at final scale; TeX math scripts use their normal
smaller sizes. Stroke weights are physical, including in the introduction strip.

Additional verification commands, from the repository root:

```powershell
python paper/figures/audit.py
python research/2026-11-14_sol_figures-polish/check_hunch.py
python research/2026-11-14_sol_figures-polish/proofs.py
```

The last command needs Pillow and writes 150 dpi before/after review material,
greyscale and full-severity deuteranopia proofs in the finishing-pass research
folder. Run it after building. The deuteranopia matrix and sRGB transfer functions
are explicit in the script. The PDFs are raster review proofs; the manuscript
figures remain vector PDFs.

COMPUTED (`research/2026-11-14_sol_figures-polish/check_hunch.py`, `hunch-results.json`):
L+ minus L- equals the number of white faces inside C on 322 rooted instances,
1,784 ordered pairs and 2,320 D-cycle occurrences, with 6 to 26 vertices in T.
The range includes every stored JSON lab instance, all four named examples,
and `generated(12)`, each with every face as outer face. Provenance duplicates
are retained. This verifies the second-pass HUNCH on that range, not in general.
The region counts in Figure 11 are separately asserted for the running example
by `check.py`.
