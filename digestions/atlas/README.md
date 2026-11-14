# Illustrated atlas of proof routes

[Read the atlas](atlas.pdf): a contents page with thumbnails, 28 route pages, and a two-page table of sources. Each route page is also a separate vector PDF in `pages/`.

This is the third pass, the final integration of 2026-11-14. It merges an independent page-by-page audit by another model (`research/2026-11-14_sol_atlas-audit/`), the project's naming convention (good state, good pair, cover, `m`, selection `P`) inside the figures as well as the text, and the second-pass author's list of thin spots. What changed, finding by finding, is in `research/2026-11-14_fable_atlas-final/CHANGELOG.md`, with before and after contact sheets in colour and greyscale.

The first pass (28 pages, commit `803f328`) had the right content and computed data but small schematic pictures, several pages with no picture, half-empty pages, and internal status tags and file paths in the text. The review that led to this rebuild, with before and after renders of every page, is in `research/2026-11-14_fable_atlas-review/`.

The atlas compares readings of one proof. It does not claim 28 independent proofs. One model audited the second pass and its corrections are applied here; nobody has audited this third pass, and no human mathematician has read any page of it. Each page says in plain words where its mathematics comes from and who checked it.

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
| `lib.py` | The running example and everything computed on it: 12 states, 8 pairs, 6 good states, heights, the clock order, the eight signed terms, both factorisations, the integer polynomial. Cross-checked against `workings/barnette_lab`. Layout and drawing helpers. |
| `figs_chain.py`, `figs_algebra.py`, `figs_order.py`, `figs_scope.py` | One function per page. Each computes its objects, asserts them, records them in the certificate and returns TikZ. |
| `pages.py`, `pages_more.py` | Titles, texts, status sentences, cross-references and sources. |
| `build.py`, `verify.py` | Build and check. |
| `atlas-figs.sty` | Extra encodings (hatching, half-weight spokes, lighter marks for thumbnails). |
| `toolkit/` | A copy of `paper/figures/` taken on 2026-11-14: `model.py`, `check.py`, `draw.py`, `layout.py`, `barnette-figs.sty`, the running example and the octahedron with their saved layouts. The atlas does not read `paper/figures/`, so later edits there do not change it. One line of `draw.py` differs from the original: if the inscribed-circle search for a face on the outer circle fails, the copy falls back to the midpoint rule instead of stopping. |
| `layouts.json` | Saved coordinates of the other triangulations, so the pictures do not drift between builds. Delete an entry to recompute it. `induction-aligned` is the least-squares layout of page 23 (b), `feder-subi-10` the example of page 24. |
| `computed.json` | Certificate: every number and object the pages show. |
| `manifest.json`, `audit.json` | Page list with figure sizes and word counts; result of the last check. |

## Encodings

The toolkit's encodings are unchanged: black faces grey, the outer black face as a grey collar, roots hollow, the second state `s` as solid blue wedges, the first state `r` as outlined wedges, `D` as blue arrows, `Q_s` dashed, kept spokes bold and deleted spokes dotted, the white-face tree green dash-dot, the selection `P` black and heavy, cycles of `G` purple, the two tree classes as disks and squares.

The atlas adds: diagonal hatching for white faces that a page counts or highlights, a dot pattern for marked black faces, double lines for spokes shared by two states, dashed bold spokes for weight one half, heavy dashes for a cycle of `Q`, and rings round marked vertices. Every pair of objects that appear together differs in shape, weight or dash as well as colour. The green dash-dot curves of the white-face tree are drawn at 1.5pt on pages 8, 19 and 21 so that they hold in greyscale. Greyscale contact sheets of all 31 pages are in `research/2026-11-14_fable_atlas-final/after/`.

States are named `s_0` to `s_11` by volume, `s_0` the lowest. The running pair of the paper's figures is `(s_1, s_9)`; its cancelling partner is `(s_2, s_9)`.

## Examples

Most pages use the 13-vertex running example of `paper/figures/`. Other examples, each computed and asserted where it is drawn:

- page 2 (c): the 9-vertex triangulation of the toolkit's gluing figure, rooted so that its separating triangle has black faces inside;
- pages 11, 25, 27: duals of the prisms with 6 and 8 sides; page 27 also a nanotube of width four;
- page 13: the 7-vertex triangulation of the torus dual to the Heawood graph;
- page 16: the 12-vertex witness from `research/2026-11-14_fable_route-combinatorics/data/counterexamples.txt`;
- page 22: the 9-vertex gluing example and a separating 4-cycle of the running example;
- page 23: the running example with vertex 2 removed and its neighbours 3 and 1 merged;
- page 24 (c), (d): the 10-vertex triangulation in `research/2026-11-14_sol_atlas-audit/outputs/fs-witness.json`. Only its edge list is read; the 14 cycles, the colouring and the 13 of 14 count are recomputed;
- page 26: the tetrahedron, a 26-vertex graph built from three cubes, the 9-vertex witness in `research/2026-11-14_astra_limits/examples/nonbijective_disk.json`, and a 3 by 3 grid on the torus.

## The proposed figures

The audit left seven proposed figures in `digestions/atlas/proposed/`. All seven are integrated, each recomputed and asserted in the atlas's own figure functions and redrawn in its encodings, and the folder is removed (it stays in git history, last present in commit `6a4fe67`). Page 6 has the ray panels, page 11 the coefficient matrix, page 16 all nine states in place of the count strip, page 22 the six connection patterns, page 23 the aligned contraction, page 24 the 10-vertex colour example, page 25 the count bar.

## What is still schematic or thin

- Page 28: the chart quotes its ranges from project reports and from the second models that repeated them. Nothing on it was recomputed here. The page says so, and separates checks by two programs from checks by one.
- Page 6: panels (c) and (d) show one move of one mark. A complete marked object of the running example carries two marks and is not drawn, and the second case of the rule (no reversal) is not shown. The face-path marks of the project's own involution note are not drawn either.
- Page 22: the six patterns are those that occur on one 4-cycle of one example. The general list is quoted, not derived.
- Page 23: the exception pattern of the 466 unrepaired lifts is not drawn.
- Page 24 (c), (d): they test the relaxed reading of Feder and Subi only. Their extra degree condition is stated in the table and not tested.
- Page 26 (a) and (b): the tetrahedron and the 26-vertex graph have hand-placed coordinates. The graphs themselves are constructed and asserted in code.
- Page 27 leaves about a quarter of the page white.
- Not added: a page comparing the blueprint with the Lean proof, and a page showing the three written proofs side by side on one step. See the report.

## Index

| Page | Route | PDF | Figure, cm | Words |
| --- | --- | --- | --- | --- |
| 1 | The chain, and where the routes branch | [PDF](pages/01-chain.pdf) | 14.97 x 14.82 | 145 |
| 2 | Two states from one count | [PDF](pages/02-pairs.pdf) | 14.64 x 16.43 | 142 |
| 3 | The disk identity, three ways | [PDF](pages/03-disk.pdf) | 14.64 x 19.24 | 133 |
| 4 | Eight terms, grouped twice | [PDF](pages/04-sum.pdf) | 12.75 x 17.13 | 130 |
| 5 | The same sum as an integer polynomial | [PDF](pages/05-polynomial.pdf) | 14.64 x 18.57 | 131 |
| 6 | Cancellation as a pairing of objects | [PDF](pages/06-involutions.pdf) | 14.64 x 17.75 | 148 |
| 7 | The exponent is a volume | [PDF](pages/07-heights.pdf) | 14.64 x 16.43 | 139 |
| 8 | From a good state to the cycle | [PDF](pages/08-recovery.pdf) | 14.64 x 17.69 | 149 |
| 9 | The same proof inside the cubic graph | [PDF](pages/09-primal.pdf) | 14.64 x 17.41 | 147 |
| 10 | Cancellation is a dependent set of rows | [PDF](pages/10-rowdep.pdf) | 14.64 x 16.18 | 149 |
| 11 | One determinant is not enough | [PDF](pages/11-determinant.pdf) | 15.09 x 16.26 | 149 |
| 12 | Two matchings laid on top of each other | [PDF](pages/12-dimers.pdf) | 14.64 x 20.2 | 150 |
| 13 | Off the sphere: the Heawood graph on a torus | [PDF](pages/13-pfaffian.pdf) | 14.57 x 15.16 | 147 |
| 14 | Twelve states under clock moves | [PDF](pages/14-lattice.pdf) | 12.89 x 17.49 | 148 |
| 15 | The lattice of covers | [PDF](pages/15-pairlattice.pdf) | 14.64 x 19.24 | 143 |
| 16 | The extreme state can have a cycle | [PDF](pages/16-canonical.pdf) | 14.64 x 16.76 | 143 |
| 17 | Three conditions, and any two are easy | [PDF](pages/17-matroids.pdf) | 14.64 x 19.57 | 147 |
| 18 | The relaxed problem has a fractional corner | [PDF](pages/18-lp.pdf) | 14.64 x 19.52 | 144 |
| 19 | A tree that uses every black face once | [PDF](pages/19-rainbow.pdf) | 14.64 x 17.08 | 150 |
| 20 | A random spanning tree with the right degrees | [PDF](pages/20-random.pdf) | 14.64 x 16.33 | 145 |
| 21 | Three graphs inside one triangulation | [PDF](pages/21-trinity.pdf) | 14.64 x 16.41 | 149 |
| 22 | What a small cut has to remember | [PDF](pages/22-cuts.pdf) | 15.11 x 17.94 | 149 |
| 23 | Induction by removing a vertex of degree four | [PDF](pages/23-induction.pdf) | 14.64 x 17.11 | 149 |
| 24 | Where the older methods meet this proof | [PDF](pages/24-earlier.pdf) | 14.57 x 18.9 | 148 |
| 25 | Which Hamiltonian cycles the proof can produce | [PDF](pages/25-produced.pdf) | 14.82 x 15.52 | 146 |
| 26 | What breaks when a hypothesis is dropped | [PDF](pages/26-hypotheses.pdf) | 14.77 x 17.88 | 149 |
| 27 | Two families, counted | [PDF](pages/27-families.pdf) | 14.64 x 13.59 | 149 |
| 28 | What is still open, and how far it was tested | [PDF](pages/28-open.pdf) | 14.22 x 17.77 | 149 |

The text block is 15.92 cm wide, so every figure is between 0.80 and 0.95 of the text width. Word counts include the status sentence and exclude the short labels under the panels. Provenance for each page is in the Sources table at the end of the atlas and in the `sources` fields of `pages.py` and `pages_more.py`.
