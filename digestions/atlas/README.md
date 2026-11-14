# Illustrated atlas of proof routes

[Read the atlas](atlas.pdf): a contents page with thumbnails, 30 route pages, and a three-page table of sources. Each route page is also a separate vector PDF in `pages/`.

This is the fourth pass, of 2026-11-14. It adds two pages (three written proofs of the key step, and what is machine-checked), fixes the spacing between stacked blocks in one shared macro, reorders the pages, and checks the shape of the 466 unrepaired lifts by computation. Page-by-page inspection notes, the changelog and before and after contact sheets in colour, greyscale and a deuteranopia simulation are in `research/2026-11-14_fable_atlas-finish/`. The third pass (audit integration, naming convention) is in `research/2026-11-14_fable_atlas-final/`, the second in `research/2026-11-14_fable_atlas-review/`.

The atlas compares readings of one proof. It does not claim 30 independent proofs. One model audited the second pass and its corrections are applied; nobody has audited the third or this fourth pass, and no human mathematician has read any page. Each page says in plain words where its mathematics comes from and who checked it. Nothing in the atlas is checked in Lean.

## Build and check

From the repository root, with Python 3 and MiKTeX `pdflatex` on PATH:

```powershell
python -m pip install networkx numpy scipy sympy pymupdf pillow
python digestions/atlas/build.py        # about one minute; add a slug such as "lattice" to rebuild one figure
python digestions/atlas/verify.py       # re-runs every assertion and checks texts, sizes, the TeX log and the PDF
```

`build.py` computes every drawn object, writes one standalone TikZ file per figure in `figs/`, compiles the changed ones, writes and compiles `atlas.tex`, splits it into `pages/NN-slug.pdf` and renders `renders/NN-slug.png` at 110 dpi. It writes only inside this directory. `verify.py` writes `audit.json` and exits non-zero on the first failed check. Last run: 30 routes, 34 pages, all checks passed, no overfull box. `verify.py` also checks the numbers the texts quote from the certificates (the three totals of page 10, the blueprint counts of page 29, the 466 of page 23) and that the page order is `pages.ORDER`.

## Files

| File | Role |
| --- | --- |
| `lib.py` | The running example and everything computed on it: 12 states, 8 pairs, 6 good states, heights, the clock order, the eight signed terms, both factorisations, the integer polynomial. Cross-checked against `workings/barnette_lab`. Layout and drawing helpers. |
| `figs_chain.py`, `figs_algebra.py`, `figs_order.py`, `figs_scope.py`, `figs_proofs.py` | One function per page. Each computes its objects, asserts them, records them in the certificate and returns TikZ. |
| `pages.py`, `pages_more.py` | Titles, texts, status sentences, cross-references and sources. `pages.ORDER` is the page order; a text refers to another page as `@slug@`, so renumbering needs no edits. |
| `build.py`, `verify.py` | Build and check. |
| `atlas-figs.sty` | Extra encodings (hatching, half-weight spokes, lighter marks for thumbnails). |
| `toolkit/` | A copy of `paper/figures/` taken on 2026-11-14: `model.py`, `check.py`, `draw.py`, `layout.py`, `barnette-figs.sty`, the running example and the octahedron with their saved layouts. The atlas does not read `paper/figures/`, so later edits there do not change it. One line of `draw.py` differs from the original: if the inscribed-circle search for a face on the outer circle fails, the copy falls back to the midpoint rule instead of stopping. |
| `layouts.json` | Saved coordinates of the other triangulations, so the pictures do not drift between builds. Delete an entry to recompute it. `induction-aligned` is the least-squares layout of page 23 (b), `feder-subi-10` the example of page 24.

`lib.vs(length)` is the row break between stacked blocks. Inside a tabular, a row break with a length only deepens a strut, so it adds nothing under a nested tabular that is already deeper. `vs` uses an explicit vertical skip instead, and `lib.grid` and every figure function go through it. |
| `computed.json` | Certificate: every number and object the pages show. |
| `manifest.json`, `audit.json` | Page list with figure sizes and word counts; result of the last check. |

## Encodings

The toolkit's encodings are unchanged: black faces grey, the outer black face as a grey collar, roots hollow, the second state `s` as solid blue wedges, the first state `r` as outlined wedges, `D` as blue arrows, `Q_s` dashed, kept spokes bold and deleted spokes dotted, the white-face tree green dash-dot, the selection `P` black and heavy, cycles of `G` purple, the two tree classes as disks and squares.

The atlas adds: diagonal hatching for white faces that a page counts or highlights, a dot pattern for marked black faces, double lines for spokes shared by two states, dashed bold spokes for weight one half, heavy dashes for a cycle of `Q`, and rings round marked vertices. Every pair of objects that appear together differs in shape, weight or dash as well as colour. The green dash-dot curves of the white-face tree are drawn at 1.5pt on pages 8, 10, 19 and 21 so that they hold in greyscale. Page 29 uses fill and outline only: dark, light grey, dashed outline, and a ringed dot. Contact sheets of all 34 pages in colour, greyscale and a deuteranopia simulation are in `research/2026-11-14_fable_atlas-finish/after/`. In that simulation the orange dashes of the opposite edges and the green dash-dot of the white-face tree come out as the same olive. They never share a panel, and they differ in dash pattern.

States are named `s_0` to `s_11` by volume, `s_0` the lowest. The running pair of the paper's figures is `(s_1, s_9)`; its cancelling partner is `(s_2, s_9)`.

## Examples

Most pages use the 13-vertex running example of `paper/figures/`. Other examples, each computed and asserted where it is drawn:

- page 2 (c): the 9-vertex triangulation of the toolkit's gluing figure, rooted so that its separating triangle has black faces inside;
- pages 12, 25, 26: duals of the prisms with 6 and 8 sides; page 26 also a nanotube of width four;
- page 28: the 7-vertex triangulation of the torus dual to the Heawood graph;
- page 16: the 12-vertex witness from `research/2026-11-14_fable_route-combinatorics/data/counterexamples.txt`;
- page 22: the 9-vertex gluing example and a separating 4-cycle of the running example;
- page 23: the running example with vertex 2 removed and its neighbours 3 and 1 merged; the sentence about the 466 unrepaired lifts is checked on the triangulations recorded in `research/2026-11-14_fable_induction-completion/data/exceptions_*.jsonl`;
- page 29: no triangulation. The chart is drawn from `proofs/blueprint/blueprint.json` and `research/2026-11-14_astra_lean-check/recount.json`;
- page 24 (c), (d): the 10-vertex triangulation in `research/2026-11-14_sol_atlas-audit/outputs/fs-witness.json`. Only its edge list is read; the 14 cycles, the colouring and the 13 of 14 count are recomputed;
- page 27: the tetrahedron, a 26-vertex graph built from three cubes, the 9-vertex witness in `research/2026-11-14_astra_limits/examples/nonbijective_disk.json`, and a 3 by 3 grid on the torus.

## Order

The audit proposed a reading order with 32 entries (target and recovery first, then the signed proof, then readings and failed shortcuts). This pass adopts part of it and says here why not all.

Adopted: the heights page now comes before the sum that uses them (pages 4 and 5). The torus page moved from the linear-algebra group to the scope pages, next to the page on dropped hypotheses (27 and 28). The Lean comparison is its own page near the end (29), and the open statements stay last (30). The comparison of the three written proofs follows the primal page (10).

Not adopted: moving recovery and the older two-tree target to pages 2 and 3. Page 1 is a map whose stations are numbered in the order of the proof, and recovery is stations 6 to 9. Putting it second would make the pages run against the map that the reader has just been told to follow. A reader who wants the target first can go from page 1 to page 8 and come back; the cross-references allow it. Also not adopted: separate pages for path marks (they are panel (c) of page 10), for two-tree packing (no computed figure exists for it here) and for evidence ranges (page 30 holds them).

## The proposed figures

The audit left seven proposed figures in `digestions/atlas/proposed/`. All seven were integrated in the third pass, each recomputed and asserted in the atlas's own figure functions, and the folder is removed (last present in commit `6a4fe67`). They are now on page 7 (ray panels), page 12 (coefficient matrix), page 16 (all nine states), page 22 (six connection patterns), page 23 (aligned contraction), page 24 (10-vertex colour example) and page 25 (count bar).

## What is still schematic or thin

- Page 30: the chart quotes its ranges from project reports and from the second models that repeated them. Nothing on it was recomputed here.
- Page 29: the statuses are the blueprint's, a hand curation by one model, read from its JSON file and not re-derived. The second count (5, 27, 2) is another model's advisory recount. "Match after a translation" hides five statements where the Lean proves less than the paper says. The table of translations is a summary in my words of four of the blueprint's bridges.
- Page 10: one face path, one flow and one unpaired object are drawn. The totals are computed for the running example and one choice of paths (shortest paths in `G`, ties by face index). I did not compare these paths with the ones behind the primal note's own flow figure; other paths give other weights, and the proofs say only the lowest coefficient is independent of the choice. The bijective note's second pairing (which objects cancel which) is not drawn or recomputed: the page checks only that the signed count of all 43 marked objects equals the signed count of the 9 unpaired ones.
- Page 7: panels (c) and (d) show one move of one mark on rays, and only the case with a reversal.
- Page 22: the six patterns are those of one 4-cycle of one example. The general list is quoted.
- Page 23: the exception shape is stated in a sentence and checked on the 466 recorded cases, not drawn. The check trusts the census for which lifts are unrepaired; it recomputes the shape of each recorded case.
- Page 24 (c), (d): they test the relaxed reading of Feder and Subi only.
- Page 27 (a) and (b): hand-placed coordinates. The graphs are constructed and asserted in code.
- Page 26 leaves about a fifth of the page white.

## Index

Route-page numbers below match the current combined PDF. The contents is PDF page 1, so route page 1 is PDF page 2. This index was checked against the PDF after the renumbering.

| Page | Route | PDF | Figure, cm | Words |
| --- | --- | --- | --- | --- |
| 1 | The chain, and where the routes branch | [PDF](pages/01-chain.pdf) | 14.97 x 14.82 | 145 |
| 2 | Two states from one count | [PDF](pages/02-pairs.pdf) | 14.64 x 16.73 | 142 |
| 3 | The disk identity, three ways | [PDF](pages/03-disk.pdf) | 14.64 x 19.54 | 133 |
| 4 | The exponent is a volume | [PDF](pages/04-heights.pdf) | 14.64 x 16.73 | 139 |
| 5 | Eight terms, grouped twice | [PDF](pages/05-sum.pdf) | 12.75 x 17.73 | 130 |
| 6 | The same sum as an integer polynomial | [PDF](pages/06-polynomial.pdf) | 14.64 x 18.87 | 131 |
| 7 | Cancellation as a pairing of objects | [PDF](pages/07-involutions.pdf) | 14.64 x 18.05 | 150 |
| 8 | From a good state to the cycle | [PDF](pages/08-recovery.pdf) | 14.64 x 17.99 | 149 |
| 9 | The same proof inside the cubic graph | [PDF](pages/09-primal.pdf) | 14.64 x 17.71 | 147 |
| 10 | Three written proofs of the key step | [PDF](pages/10-keystep.pdf) | 13.59 x 18.57 | 150 |
| 11 | Cancellation is a dependent set of rows | [PDF](pages/11-rowdep.pdf) | 14.64 x 16.61 | 150 |
| 12 | One determinant is not enough | [PDF](pages/12-determinant.pdf) | 15.09 x 17.41 | 149 |
| 13 | Two matchings laid on top of each other | [PDF](pages/13-dimers.pdf) | 14.57 x 19.81 | 150 |
| 14 | Twelve states under clock moves | [PDF](pages/14-lattice.pdf) | 12.89 x 17.49 | 148 |
| 15 | The lattice of covers | [PDF](pages/15-pairlattice.pdf) | 14.64 x 19.54 | 143 |
| 16 | The extreme state can have a cycle | [PDF](pages/16-canonical.pdf) | 14.64 x 17.51 | 143 |
| 17 | Three conditions, and any two are easy | [PDF](pages/17-matroids.pdf) | 14.57 x 19.18 | 147 |
| 18 | The relaxed problem has a fractional corner | [PDF](pages/18-lp.pdf) | 14.57 x 19.12 | 144 |
| 19 | A tree that uses every black face once | [PDF](pages/19-rainbow.pdf) | 14.64 x 17.38 | 150 |
| 20 | A random spanning tree with the right degrees | [PDF](pages/20-random.pdf) | 14.64 x 16.63 | 149 |
| 21 | Three graphs inside one triangulation | [PDF](pages/21-trinity.pdf) | 14.64 x 16.71 | 149 |
| 22 | What a small cut has to remember | [PDF](pages/22-cuts.pdf) | 15.11 x 18.79 | 149 |
| 23 | Induction by removing a vertex of degree four | [PDF](pages/23-induction.pdf) | 14.64 x 17.41 | 150 |
| 24 | Where the older methods meet this proof | [PDF](pages/24-earlier.pdf) | 14.57 x 19.5 | 148 |
| 25 | Which Hamiltonian cycles the proof can produce | [PDF](pages/25-produced.pdf) | 14.82 x 17.02 | 146 |
| 26 | Two families, counted | [PDF](pages/26-families.pdf) | 14.64 x 14.29 | 149 |
| 27 | What breaks when a hypothesis is dropped | [PDF](pages/27-hypotheses.pdf) | 14.77 x 18.18 | 149 |
| 28 | Off the sphere: the Heawood graph on a torus | [PDF](pages/28-pfaffian.pdf) | 14.57 x 15.46 | 147 |
| 29 | What is machine-checked | [PDF](pages/29-blueprint.pdf) | 14.78 x 16.85 | 149 |
| 30 | What is still open, and how far it was tested | [PDF](pages/30-open.pdf) | 14.07 x 19.14 | 149 |

The text block is 15.92 cm wide, so every figure is between 0.80 and 0.95 of the text width. Word counts include the status sentence and exclude the short labels under the panels. Provenance for each page is in the Sources table at the end of the atlas and in the `sources` fields of `pages.py` and `pages_more.py`.
