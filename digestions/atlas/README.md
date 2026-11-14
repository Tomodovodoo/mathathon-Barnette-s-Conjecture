# Illustrated atlas of proof routes

[Read the atlas](atlas.pdf): a contents page with thumbnails, 28 route pages, and a two-page table of sources. Each route page is also a separate vector PDF in `pages/`.

This is the second pass. The first pass (28 pages, commit `803f328`) had the right content and computed data but small schematic pictures, several pages with no picture, half-empty pages, and internal status tags and file paths in the text. The review that led to this rebuild, with before and after renders of every page, is in `research/2026-11-14_fable_atlas-review/`.

The atlas compares readings of one proof. It does not claim 28 independent proofs. Nobody has refereed the atlas itself, and no human mathematician has read any page of it. Each page says in plain words where its mathematics comes from and who checked it.

## Build and check

From the repository root, with Python 3 and MiKTeX `pdflatex` on PATH:

```powershell
python -m pip install networkx numpy scipy sympy pymupdf pillow
python digestions/atlas/build.py        # about one minute; add a slug such as "lattice" to rebuild one figure
python digestions/atlas/verify.py       # re-runs every assertion and checks texts, sizes, the TeX log and the PDF
```

`build.py` computes every drawn object, writes one standalone TikZ file per figure in `figs/`, compiles the changed ones, writes and compiles `atlas.tex`, splits it into `pages/NN-slug.pdf` and renders `renders/NN-slug.png` at 110 dpi. It writes only inside this directory. `verify.py` writes `audit.json` and exits non-zero on the first failed check. Last run: 28 routes, 31 pages, all checks passed.

## Files

| File | Role |
| --- | --- |
| `lib.py` | The running example and everything computed on it: 12 states, 8 pairs, 6 tree matchings, heights, the clock order, the eight signed terms, both factorisations, the integer polynomial. Cross-checked against `workings/barnette_lab`. Layout and drawing helpers. |
| `figs_chain.py`, `figs_algebra.py`, `figs_order.py`, `figs_scope.py` | One function per page. Each computes its objects, asserts them, records them in the certificate and returns TikZ. |
| `pages.py`, `pages_more.py` | Titles, texts, status sentences, cross-references and sources. |
| `build.py`, `verify.py` | Build and check. |
| `atlas-figs.sty` | Extra encodings (hatching, half-weight spokes, lighter marks for thumbnails). |
| `toolkit/` | A copy of `paper/figures/` taken on 2026-11-14: `model.py`, `check.py`, `draw.py`, `layout.py`, `barnette-figs.sty`, the running example and the octahedron with their saved layouts. The atlas does not read `paper/figures/`, so later edits there do not change it. One line of `draw.py` differs from the original: if the inscribed-circle search for a face on the outer circle fails, the copy falls back to the midpoint rule instead of stopping. |
| `layouts.json` | Saved coordinates of the other triangulations, so the pictures do not drift between builds. Delete an entry to recompute it. |
| `computed.json` | Certificate: every number and object the pages show. |
| `manifest.json`, `audit.json` | Page list with figure sizes and word counts; result of the last check. |

## Encodings

The toolkit's encodings are unchanged: black faces grey, the outer black face as a grey collar, roots hollow, the second state `s` as solid blue wedges, the first state `r` as outlined wedges, `D` as blue arrows, `Q_s` dashed, kept spokes bold and deleted spokes dotted, the white-face tree green dash-dot, selected edges `P` black and heavy, cycles of `G` purple, the two tree classes as disks and squares.

The atlas adds: diagonal hatching for white faces that a page counts or highlights, a dot pattern for marked black faces, double lines for spokes shared by two states, dashed bold spokes for weight one half, heavy dashes for a cycle of `Q`, and rings round marked vertices. Every pair of objects that appear together differs in shape, weight or dash as well as colour. `research/2026-11-14_fable_atlas-review/greyscale-check.png` is a greyscale proof of two pages.

States are named `s_0` to `s_11` by volume, `s_0` the lowest. The running pair of the paper's figures is `(s_1, s_9)`; its cancelling partner is `(s_2, s_9)`.

## Examples

Most pages use the 13-vertex running example of `paper/figures/`. Other examples, each computed and asserted where it is drawn:

- page 2 (c): the 9-vertex triangulation of the toolkit's gluing figure, rooted so that its separating triangle has black faces inside;
- pages 11, 25, 27: duals of the prisms with 6 and 8 sides; page 27 also a nanotube of width four;
- page 13: the 7-vertex triangulation of the torus dual to the Heawood graph;
- page 16: the 12-vertex witness from `research/2026-11-14_fable_route-combinatorics/data/counterexamples.txt`;
- page 22: the 9-vertex gluing example and a separating 4-cycle of the running example;
- page 23: the running example with vertex 2 removed and its neighbours 3 and 1 merged;
- page 26: the tetrahedron, a 26-vertex graph built from three cubes, the 9-vertex witness in `research/2026-11-14_astra_limits/examples/nonbijective_disk.json`, and a 3 by 3 grid on the torus.

## What is still schematic or thin

- Page 28: the chart quotes its numbers from unrefereed reports. They were not recomputed here. The page says so.
- Page 6: Li's marks for the second pairing are described, not drawn.
- Page 11: the matrix `N(y, w)` of the coefficient formula is stated, not drawn. The page shows the states and signs that make a single evaluation vanish.
- Page 24 (c): under the induced-tree reading of Feder and Subi, all 28 Hamiltonian cycles of the running example pass, for each colour class. The panel is correct but the example is too small to show the condition excluding anything.
- Page 22: patterns on the 4-cycle are label words only. They do not record how each tree connects the cut vertices.
- Page 23 (b): the smaller triangulation is laid out afresh, so it does not line up with panel (a).
- Page 26 (a) and (b): the tetrahedron and the 26-vertex graph have hand-placed coordinates. The graphs themselves are constructed and asserted in code.
- Pages 16 and 25 leave about a quarter of the page white.

## Index

| Page | Route | PDF | Figure, cm | Words |
| --- | --- | --- | --- | --- |
| 1 | The chain, and where the routes branch | [PDF](pages/01-chain.pdf) | 15.05 x 14.82 | 139 |
| 2 | Two states from one count | [PDF](pages/02-pairs.pdf) | 14.64 x 16.43 | 142 |
| 3 | The disk identity, three ways | [PDF](pages/03-disk.pdf) | 14.64 x 19.24 | 133 |
| 4 | Eight terms, grouped twice | [PDF](pages/04-sum.pdf) | 12.75 x 17.13 | 124 |
| 5 | The same sum as an integer polynomial | [PDF](pages/05-polynomial.pdf) | 14.64 x 18.57 | 131 |
| 6 | Cancellation as a pairing of objects | [PDF](pages/06-involutions.pdf) | 14.71 x 16.68 | 149 |
| 7 | The exponent is a volume | [PDF](pages/07-heights.pdf) | 14.64 x 16.43 | 139 |
| 8 | From a forest state to the cycle | [PDF](pages/08-recovery.pdf) | 14.64 x 17.69 | 149 |
| 9 | The same proof inside the cubic graph | [PDF](pages/09-primal.pdf) | 14.64 x 17.41 | 147 |
| 10 | Cancellation is a dependent set of rows | [PDF](pages/10-rowdep.pdf) | 14.64 x 15.25 | 143 |
| 11 | One determinant is not enough | [PDF](pages/11-determinant.pdf) | 15.09 x 13.16 | 144 |
| 12 | Two matchings laid on top of each other | [PDF](pages/12-dimers.pdf) | 14.64 x 20.2 | 150 |
| 13 | Off the sphere: the Heawood graph on a torus | [PDF](pages/13-pfaffian.pdf) | 14.57 x 15.16 | 148 |
| 14 | Twelve states under clock moves | [PDF](pages/14-lattice.pdf) | 12.89 x 17.49 | 148 |
| 15 | The lattice of cycle covers | [PDF](pages/15-pairlattice.pdf) | 14.64 x 19.24 | 144 |
| 16 | The extreme state can have a cycle | [PDF](pages/16-canonical.pdf) | 14.64 x 11.92 | 143 |
| 17 | Three conditions, and any two are easy | [PDF](pages/17-matroids.pdf) | 14.64 x 19.24 | 139 |
| 18 | The relaxed problem has a fractional corner | [PDF](pages/18-lp.pdf) | 14.64 x 19.52 | 137 |
| 19 | A tree that uses every black face once | [PDF](pages/19-rainbow.pdf) | 14.64 x 17.08 | 150 |
| 20 | A random spanning tree with the right degrees | [PDF](pages/20-random.pdf) | 14.64 x 16.33 | 149 |
| 21 | Three graphs inside one triangulation | [PDF](pages/21-trinity.pdf) | 14.64 x 16.41 | 150 |
| 22 | What a small cut has to remember | [PDF](pages/22-cuts.pdf) | 15.11 x 16.42 | 150 |
| 23 | Induction by removing a vertex of degree four | [PDF](pages/23-induction.pdf) | 14.64 x 17.1 | 149 |
| 24 | Where the older methods meet this proof | [PDF](pages/24-earlier.pdf) | 14.64 x 19.24 | 150 |
| 25 | Which Hamiltonian cycles the proof can produce | [PDF](pages/25-produced.pdf) | 14.82 x 14.1 | 141 |
| 26 | What breaks when a hypothesis is dropped | [PDF](pages/26-hypotheses.pdf) | 14.77 x 17.88 | 149 |
| 27 | Two families, counted | [PDF](pages/27-families.pdf) | 14.89 x 13.59 | 139 |
| 28 | What is still open, and how far it was tested | [PDF](pages/28-open.pdf) | 15.11 x 17.55 | 147 |

The text block is 15.92 cm wide, so every figure is between 0.80 and 0.95 of the text width. Word counts include the status sentence and exclude the short labels under the panels. Provenance for each page is in the Sources table at the end of the atlas and in the `sources` fields of `pages.py` and `pages_more.py`.
