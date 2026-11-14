# Report: second pass over the illustrated route atlas

Fable 5.2, 2026-11-14. Folder `research/2026-11-14_fable_atlas-review/`. I own `digestions/atlas/` from this pass on.

1. The atlas is rebuilt: 28 route pages, each with a computed figure at 0.80 to 0.95 of the text width, a contents page with thumbnails and a sources table. `verify.py` passes.
2. Every drawn object is computed and asserted in the function that draws it. Most pages use the 13-vertex running example; eleven other small examples are constructed in code.
3. Texts are 124 to 150 words in plain words, with the review status spelled out. No tags or paths in the body.
4. Four pages are new: the cut inequality, the Heawood torus, the random spanning tree, and induction by contraction. Three first-pass pages were merged into others.
5. Still thin: the chart on page 28 quotes numbers it does not recompute, Li's marks are not drawn, and the Feder and Subi panel is uninformative on so small an example.

## What I set out to do

Look at every page of the first-pass atlas, say for each whether its picture shows the route's mechanism on a concrete object, and redraw all of them in the project's visual language on the running example, with computed objects only, balanced pages and plain text.

## What I established

All mathematical statements below are about finite examples and are `COMPUTED` by `python digestions/atlas/build.py` (objects asserted in `lib.py` and `figs_*.py`, certificate in `digestions/atlas/computed.json`), then re-run by `python digestions/atlas/verify.py`. The atlas proves nothing general.

**The review.** `REVIEW.md` has the table for all 28 first-pass pages. Seven had no picture of an object, seven more reused one generic drawing, and every page was 40 to 60 per cent white. The underlying computations were sound and are kept.

**The rebuild.** `digestions/atlas/` now holds the sources, `atlas.pdf` (31 pages), `pages/` (31 single-page PDFs), `renders/`, the copied toolkit, the certificate and a README with build commands and index. Renders of the first pass are in `before/`, of the second in `after/`.

**Facts computed for the pages that were not in the first pass or differ from it** (all on the 13-vertex running example unless stated):

- `COMPUTED`. With exponents normalised to the volume (sum of heights) of the second state, the eight terms are `-1, +e^x, -e^{2x}, +e^{3x}, +e^{5x}, +e^{6x}, -e^{6x}, -e^{7x}`. The exact rational exponents of the first pass differ from these volumes by one constant; `lib.py` asserts this. The two cycle covers contribute `-(1-e^{6x})(1-e^{x})` and `-e^{2x}(1-e^{3x})(1-e^{x})`, and the lowest coefficient is `-(6·1 + 3·1) = -9`, matching `9x^2` in the integer polynomial up to the global sign.
- `COMPUTED`. For every one of the 12 states the 10 by 10 endpoint matrix of `Q_s` has determinant 0 unless `s` is a tree matching, where it is ±1, and the nonzero terms of the expansion are exactly the partners of `s`.
- `COMPUTED`. The clock order on the 12 states has 15 covers, each a change of height by one on one white face. Six states are tree matchings, among them the lowest and the highest; one has a partner and a cycle; five have no partner.
- `COMPUTED`. The two cycle covers differ over one white face. Each has four orientations, three of them tree pairs.
- `COMPUTED`. Dropping one of the three conditions: 350 choices satisfy face and forest, 12 face and vertex, 304 vertex and forest, 6 all three.
- `COMPUTED`. The half-integral corner of the relaxation found with seed 714 has 14 half spokes on one closed curve and is the average of the cyclic state `s_9` and the tree matching `s_4`.
- `COMPUTED`. The spoke graph has 6,670,188 spanning trees, of which 6 have the prescribed degrees. Of 4000 uniform samples (Wilson's algorithm, seed 2026) none hit them.
- `COMPUTED`. `G` has 28 Hamiltonian cycles. Each edge is avoided by between 4 and 14 of them. Across the separating 4-cycle (1, 6, 11, 8) of `T` they realise five label patterns with frequencies 12, 6, 4, 4, 2.
- `COMPUTED`. Removing vertex 2 and merging 3 with 1 gives an 11-vertex triangulation with 4 tree matchings. Three lifts are tree matchings. The fourth fails and the three-wedge rotation of the induction report repairs it.
- `COMPUTED`, hexagonal prism with a rung as prescribed edge: 8 Hamiltonian cycles, 4 avoid the edge, 2 are produced. The states recovered from the other two are not tree matchings because their opposite edges join two roots. They contain no cycle.
- `COMPUTED`, Heawood torus: 24 states, 48 pairs, every `D` a 7-cycle, left-minus-right sums 7, -7, 1, -1 occurring 3, 3, 21, 21 times, and the two partners of every state have opposite signs. This reproduces the numbers of `research/2026-11-14_astra_route-pfaffian/REPORT.md` with independent code.
- `COMPUTED`, the 12-vertex witness: 9 states, 10 pairs, 8 tree matchings; the highest partnered state has a 3-cycle in `Q`. In the stored orientation it is the highest, as the combinatorics referee said.

## What failed, and why

- **A Feder and Subi picture that says something.** Under the dictionary of `research/2026-11-14_astra_older-approaches/BRIDGES.md` (an induced tree whose vertices outside one colour class are pairwise non-adjacent), all 28 Hamiltonian cycles of the running example qualify for each of the three colour classes. Either the example is too small or the dictionary needs its extra conditions (face lengths, the "proper" restriction) to bite. I drew the panel and said so. `COMPUTED`; I did not investigate further.
- **Li's second involution.** I did not draw the marks. The lab code for them is refereed only for one mark on the cube, and the running example needs two.
- **The matrix `N(y, w)`.** I did not open the determinant referee's definition far enough to rebuild it, so page 11 states the formula and draws only the sign balance.
- **Visual continuity on the induction page.** Placing the merged vertex at the midpoint gives a valid but nearly degenerate drawing, so I relaxed the layout, and panel (b) no longer lines up with panel (a).
- **Two tooling problems cost time.** Shell here-documents in this environment halve backslashes, which corrupted TeX strings twice. And `Panel.centre` in the toolkit stops with an assertion when its inscribed-circle search fails on a new triangulation; my copy falls back to the midpoint rule.

## What is still open

- Page 28's numbers come from four unrefereed reports. Nobody has recomputed them.
- No human has read the atlas. The status sentences repeat what the reports and referees say about themselves.
- The text length rule holds for the body. The panel labels add 60 to 160 words per page on top of it.
- I did not produce a full greyscale proof, only `greyscale-check.png` for two pages.

## Three best next steps

1. Have a second model referee the atlas texts against the sources, page by page. The risk is in the status sentences and in my one-line summaries of unrefereed reports (pages 13, 19, 20, 23, 28).
2. Replace the quoted chart on page 28 by recomputed ranges for at least the two cheapest statements (the `2^c` bound and the contraction inequality up to 14 vertices), using `workings/barnette_lab`.
3. Draw Li's marks for the running example once the multi-mark code has been refereed, and the matrix `N(y, w)` for the prism, so that pages 6 and 11 show their second halves.

## Leads for others

- `paper/figures/draw.py`, `Panel.centre`: the SLSQP incentre search asserts on some rooted triangulations (the 9-vertex non-bijective witness). Whoever owns the figure toolkit may want the same fallback.
- The prism example on page 25 shows a failure mode the first-pass text did not name: a recovered state can fail to be a tree matching with no cycle in `Q`, because a path of opposite edges joins two roots. Texts that say "`Q_s` is a forest" as shorthand for "tree matching" should say "three trees, one at each root".
- The Feder and Subi dictionary in `BRIDGES.md` deserves a test on a larger example where it excludes some Hamiltonian cycle.
