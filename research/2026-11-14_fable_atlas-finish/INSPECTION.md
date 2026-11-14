# Inspection, page by page

Fable 5.2, 2026-11-14. Renders by `render_pages.py` at 130 dpi: colour, greyscale, and a deuteranopia simulation (Machado, Oliveira and Fernandes 2009, severity 1, in linear RGB). The full-size PNGs are scratch and not committed. The 42 dpi contact sheets are in `before/` and `after/`.

"Before" is the atlas of commit `698b5d1` (31 pages, old numbering). "After" is the final build of this pass (34 pages, new numbering).

## What I looked at, exactly

Before, at full size: colour, all 31 pages. Greyscale, pages 1 to 26 and 28. Not in greyscale: the contents page, page 27 and the two source pages. No deuteranopia render at full size.

After, there were two builds. The first had every change except four: the panel size on pages 13, 17 and 18, a minimum gap above "See also" on every page, three shorter labels on page 29, and ragged-right table columns on pages 10 and 29.

At full size on that first build, in colour: pages 0, 1, 3, 5, 7, 10, 11, 12, 13, 16, 17, 18, 22 to 30 and the last source page.

At full size on the final build: colour of page 13; greyscale of pages 2, 4, 6, 9, 10, 15, 19 and 29; deuteranopia of page 10. Everything else on the final build I saw on contact sheets only (greyscale sheets 1 and 2, deuteranopia sheet 2).

Never at full size after the changes: pages 8, 14, 20, 21 and the first two source pages. Their figure sources differ from the old build by the row-skip macro alone (1 to 2 changed lines each, counted against `698b5d1`), plus one page number in a caption on page 21.

So the brief's "every page at full size in colour and greyscale" is met for the old build except four pages in greyscale, and for the new build only in part. Pages 17 and 18 with their final panel size are the weakest spot: sheet only.

## Defects and fixes

New page numbers. "Old n" gives the number in the previous build where it differs.

| Page | Colour | Greyscale | Simulation | Defect | Fix |
| --- | --- | --- | --- | --- | --- |
| 0 contents | 30 thumbnails in six rows, captions legible | sheet only | sheet only | none found | new rows for the two new pages; `verify.py` now checks the contents page lists every page number |
| 1 chain | ok | before: the white-face tree in station 7 nearly vanished; the label "polynomial 5" touched both ends of its line | n/a | two | tree drawn at 1.2pt in the thumbnail; label shortened to "polynom." so the line shows on both sides |
| 2 pairs | ok | ok after | n/a | none | row gap now 3 mm (was 0) |
| 3 disk | ok | before: the tint of the disk was close to white | sheet | weak tint | tint raised from 13% to 19% blue; boundary arrows and hatching carry the disk as before |
| 4 heights (old 7) | ok | ok after | n/a | none | moved before the sum |
| 5 sum (old 4) | before: headings sat 1 mm above the thumbnails, notes ran into the next row | same | sheet | heading spacing | `lib.vs`; checked in colour after |
| 6 polynomial (old 5) | ok | ok after | n/a | none | |
| 7 involutions (old 6) | ok | ok before | sheet | text said "a complete marked object is not drawn" | text now points to page 10; the `2^q` sentence is back |
| 8 recovery | ok before | ok before | sheet | none | not seen at full size after |
| 9 primal | ok | ok after | n/a | none | status updated (revised, accepted in a cross-audit) |
| 10 keystep (new) | first build: caption widths made the page overflow by 21pt; table columns justified with rivers | ok: path dash-dot at 1.5pt, signs in circles, ring with white halo, boxed flow numbers | ok: blue wedges and olive path differ in shape | three | panels at unit 0.57 and captions cut; ragged-right columns; flow numbers boxed where they cross the cut |
| 11 rowdep (old 10) | before: caption (a) ran into strip (c); vertex numbers 1, 9, 10, 2 sat on wedges | same | n/a | two | `lib.vs` between the blocks and before the caption; numbers placed on the side away from the wedge the vertex carries |
| 12 determinant (old 11) | before: column numbers of the matrix touched the rule above; caption (d) touched the next heading; number 4 on a wedge | same | n/a | three | `lib.vs`; label offsets as on page 11 |
| 13 dimers (old 12) | before: text started 1 mm under caption (d) and "See also" touched the status | same | n/a | page too full | panels at unit 0.585 on this page; minimum gap of 2.5 mm above "See also" in `build.py` |
| 14 lattice | ok before | ok before; hatching is small but readable at 130 dpi | sheet | none | not seen at full size after |
| 15 pairlattice | caption said "Blue: its two cycles" | lines are heavy, wedges outlined | n/a | caption named a colour only | "Heavy blue lines" |
| 16 canonical | before: caption (a) touched the thumbnails; labels of row two touched caption (c) | same | sheet | heading spacing | `lib.vs` |
| 17 matroids | before: "See also" touched the status | same | sheet | page too full | unit 0.585; gap above "See also" |
| 18 lp | same as 17 | same | sheet | page too full | same |
| 19 rainbow | caption said "Each green curve" | curves heavy dash-dot | sheet | caption named a colour only | "heavy green curve" |
| 20 random | ok before | ok before | sheet | none | text regained the sentence on prescribed degrees; not seen at full size after |
| 21 trinity | ok before | ok before | sheet | caption had a literal "page 8" | computed page number; not seen at full size after |
| 22 cuts | ok | ok before | sheet | none (fixed in the previous pass) | text regained "each side only reports how its trees meet the cut" |
| 23 induction | ok | ok before | sheet | none in the figure | new sentence on the shape of the 466 |
| 24 earlier | before: caption (c) touched the table rule | same | n/a | heading spacing | `lib.vs`; (b) stays crowded: 33 counts on 33 edges at this size |
| 25 produced | caption said "(purple)" | cycles are heavy curves, `e` dashed | sheet | caption named a colour only | "heavy purple curves" |
| 26 families (old 27) | before: chart titles touched captions (a), (b) | same | n/a | heading spacing | `lib.vs` (5 mm) |
| 27 hypotheses (old 26) | before: in (d) the vertex numbers sat on the dashed edges and wedges | same | n/a | labels on marks | numbers below the vertex on a white box |
| 28 pfaffian (old 13) | before: last line of caption (a) ran into panel (c) | same | n/a | caption overlap | `lib.vs` in `grid` gives the row a real gap |
| 29 blueprint (new) | first build: chart 1.2 times the text width, legend outside the chart, long labels touching their boxes | ok: dark, light, dashed outline and ringed dot all hold | n/a (no colour) | three | arcs kept inside the column gap, legend as one row, three labels shortened, ragged-right table |
| 30 open (old 28) | before: two-line labels of adjacent rows touched ("...has more" over "good states...") and broke mid-word ("con-traction") | same | n/a | label collisions | chosen line breaks, taller rows for two-line labels |
| 31 to 33 sources | last page ok | sheet | sheet | none found | rows for the two new pages; three pages now |

## What the simulation showed

Blue (wedges, arrows of `D`) stays blue. Orange dashes (opposite edges) and the green dash-dot (white-face tree) both turn olive. They never share a panel, and their dash patterns differ. Purple cycles of `G` turn blue-grey, close to the blue of `D`; the two share page 1 only as separate thumbnails and page 24 (a) not at all. I found no encoding that the simulation collapses.

## Not fixed

- Page 24 (b): the counts are crowded.
- Page 14: the hatching in the thumbnails is small.
- Page 26: about a fifth of the page is white.
- Page 29: some arrows between columns 1 and 2 run close together, and a reader cannot follow each one. The chart shows the shape of the dependencies and the statuses; the JSON file has the edges.
