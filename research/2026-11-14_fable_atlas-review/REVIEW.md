# Review of the first-pass atlas, page by page

Fable 5.2, 2026-11-14. I rendered all 28 pages of the first pass at 110 dpi (`before/p01.png` to `before/p28.png`) and read every one. The rebuilt atlas has 28 route pages, a contents page and a sources table; its renders are in `after/`.

## What was wrong across the whole first pass

1. Seven pages had no picture of a mathematical object: 9 and 10 were formulas, 14 a small tree diagram and a table, 21, 25 and 26 four text boxes each, and 1 a line with labels.
2. Where there was a picture, it was usually one generic drawing of the running pair. Pages 4, 6, 7, 8, 19, 24 and 27 show nearly the same image. The picture did not change with the route, so it could not show the route's mechanism.
3. Several routes left the running example without need (page 11 the cube, 14 the prism as an abstract tree, 17 dots on a triangle and a square, 28 a second layout of the cube).
4. Multi-panel pictures were about 4 cm wide per panel. Single pictures were 12 cm wide and the page below them was empty. Every page was between 40 and 60 per cent white.
5. The text carried `LIT`, `PROVED-HERE`, `COMPUTED`, `REFUTED`, file names and paths, and sentences about the build ("the build enumerates"). Much of it described the checking instead of the route.
6. The disk identity took three pages with three near-identical pictures, so the reader could not compare the three arguments.

The computations behind the pages were sound and I kept them: the 12 states and 8 pairs, exact heights, both orders, the signed terms, the polynomial, the half-integral point with its rank certificate, the prism counts, the 12-vertex witness, the lab cross-check.

## Page by page

"Shows the mechanism" means: the picture shows a concrete object on which the route's own step can be seen.

| Old page | Route | Did the picture show the mechanism? | What the picture should be | New page |
| --- | --- | --- | --- | --- |
| 1 One proof, several readings | the chain of the proof | No. A thin line with nine labels. | A metro map with a thumbnail of the running example at each station, forced and existence steps drawn differently, parallel lines for the four readings of the hard step, stubs for refuted shortcuts. | 1 |
| 2 Eight terms, two regroupings | the exponential sum | Partly. One small pair and a table of eight rows with exponents such as -589/156. | All eight pairs as small multiples, once grouped by `s` with the cancelling pair bracketed, once grouped by `D` with the factorisation under each group. Exponents normalised to the volume so that terms read `+e^{6x}`. | 4 |
| 3 Li turns the sum into paired objects | Li's involutions | Partly. Two 4 cm panels; the second involution was three lines of symbols on the cube. | The first pairing as two large panels with the reversed cycle of `Q_s`; the four orientations of each cycle cover as a square, with signs and weights, to show why reversing a cycle of `D` does not cancel. | 6 |
| 4 The same argument with linear weights | integer polynomial | No. The generic pair picture, with the polynomial as a caption. | Both cycle covers with the white faces inside each cycle hatched and numbered, the spoke detour that explains the count, and the identity 6 + 3 = 9. | 5 |
| 5 Put the height on white faces | heights | Partly. One state with labels 0 and 1; no reference state, no move. | The lowest state, one clock move with the old wedges outlined, the running state and the highest state, each with heights in the white faces and the raised faces hatched. | 7 |
| 6 The disk identity as a census | Euler count | Yes, but it shared its picture with pages 7 and 8. | One page, three panels on the same cycle, and a ledger of the three identities. | 3 |
| 7 The disk has one extra white face | `W = B + 1` | Yes, as above. | Merged into the same page. | 3 |
| 8 The disk identity as turning number | turning angles | Yes, but only the boundary turns were shown, not the corner angles that make the disk flat. | Merged; corner angles written in the black faces, boundary turns in bold. | 3 |
| 9 Cancellation is a row dependence | incidence matrix | No picture. A 10 by 10 matrix of numbers with no link to the triangulation. | The matrix for a cyclic state and for a forest state side by side, each under its triangulation with faces lettered and vertices numbered, dependent rows shaded next to the cycle they come from. | 10 |
| 10 A determinant needs coefficient extraction | determinant formula | No picture. Two formulas. | The three states of the prism dual with the signs of its two tree matchings, the six signed tree matchings of the running example, and the statement of what one evaluation loses. | 11 |
| 11 A doubled spoke is not a D-cycle | double dimers | Schematic. The cube dual with three double lines. | On the running example: a pair as alternating spokes with the cycles of `D`, two overlays with shared spokes drawn double, and the 12 by 12 table of shared spokes with the eight pairs marked. | 12 |
| 12 Forget orientations, keep the pair lattice | lattice of cycle covers | Partly. Two 4 cm panels and a diagram with two numbered circles. | Both covers large, with the unused corners; the step between them drawn on the spokes with the raised white face; the two-node diagram with tree counts. | 15 |
| 13 The twelve states under clock moves | clock lattice | No. An abstract Hasse diagram of numbered circles beside a table of 120 numbers. | The Hasse diagram with a thumbnail of the state at every node, raised faces hatched, tree matchings ringed. | 14 |
| 14 Three constraints, not two | three matroids | No. A tree diagram of numbered dots for the prism and a five-row table. | Three witnesses on the running example, one for each dropped condition, with the repeated and missed vertex ringed, and a table of the counts. | 17 |
| 15 The natural relaxation has a fractional vertex | half-integral LP point | Partly. Wedges for weights, which reads as a state. | Half-weight spokes with their closed curve, the two states it averages, and the size of the inequality system. | 18 |
| 16 A white tree with one token per face | rainbow tree and exchange | Yes, but at 4 cm and with the changed faces unmarked. | Before and after at full size with faces lettered and the doubled and missed face marked; the same two objects as spanning trees of spokes. | 19 |
| 17 What a small cut must remember | boundary patterns | No. Dots on three triangles and five squares. | Every pattern drawn on a triangulation that has the cut: three for a separating triangle, five for a separating 4-cycle of the running example, with their frequencies. | 22 |
| 18 Keep the construction inside G | primal reading | Partly. The final cycle only. | `G` on the layout with its root vertex and edge; a cycle of `D` as an edge cut with its shore tinted and counted; a state as arrows from black vertices; the matching and the cycle. | 9 |
| 19 From a white tree to one Jordan curve | recovery | Partly. Only the end result. | Four steps: forest state, spanning tree of spokes with the white tree, selected sides, two trees and the cycle. | 8 |
| 20 Two produced cycles, six missed cycles | image of the construction | Partly. Two of the eight cycles. | All eight cycles as small multiples with their status, and the state recovered from each of the four that avoid the edge. | 25 |
| 21 Four places a hypothesis enters | hypotheses | No picture. Four text boxes. | The smallest example for each hypothesis, drawn: tetrahedron, the 26-vertex graph, the 9-vertex non-bijective witness, the torus grid. | 26 |
| 22 Counts separate existence from abundance | families | No drawing of either family; a chart and a table. | One prism dual and one nanotube with a tree matching, and two charts with direct labels. | 27 |
| 23 The tempting highest state can be cyclic | canonical choice refuted | Partly. The witness drawn by a Tutte embedding with slivers and stray vertex numbers. | The witness in a relaxed layout with heights and the cycle, the nearest tree matching, and all nine states by volume. | 16 |
| 24 Earlier methods meet the new forest step | Stein, Kelmans, Feder and Subi | No. The recovery picture again. | Stein's two trees, the number of cycles avoiding each edge for Kelmans, a three-coloured induced tree for Feder and Subi, and a table of what each supplies. | 24 |
| 25 Grassmann variables package the same coefficient | Berezin integral | No picture. Four text boxes. | No separate page. It is a rewriting of the coefficient formula and has no object of its own to draw. One sentence on page 11. | 11 |
| 26 The doors that are actually still open | open questions | No picture. Four text boxes. | A chart of how far each open statement was tested and where each refuted variant first fails, with the mechanism of the failures drawn on the running example. | 28 |
| 27 Morse cancellation pairs the bad orientations | Morse reading | Partly. The cyclic state once more. | Merged into page 6: the pairing on the cube of partners is the first involution. | 6 |
| 28 Three incidence graphs in one triangulation | trinity | Poor. A different layout of the cube with long crossing-like edges. | The running example four times: all three graphs, then each alone. | 21 |

## Pages added

| New page | Why |
| --- | --- |
| 2 Two states from one count | The first step of the chain had no page. Shows the count for one set, the pair it yields, a triangulation where it fails, and the pair as a 2-factor of spokes. |
| 13 The Heawood graph on a torus | The Pfaffian route arrived after the first pass. |
| 20 A random spanning tree with the right degrees | The probabilistic route's report appeared while I was working. |
| 23 Induction by removing a vertex of degree four | The induction route arrived after the first pass. |

The conjecture attack has no page of its own. Its refutation of the extreme-cover conjecture is on page 15, its test ranges are on page 28, and its mechanism for the failures is panel (b) of page 28. The rainbow referee's results are on page 19.

## Rules I applied to every new page

- One figure, 0.80 to 0.95 of the text width, built from two to sixteen panels. Each panel carries its own label of one to four lines.
- Every drawn object is computed and asserted in the function that draws it. The check script re-runs all of them.
- Body text of 124 to 150 words including the status sentence. It says what the route does and where it stops. Status is in plain words. No tags, no paths.
- Text at 10 pt, labels at footnote size (8 pt). Page numbers in cross-references are generated.
- Hatching, dot patterns, dashes and rings carry the meaning next to colour.

## What I looked at after the rebuild

I rendered all pages after every build and looked at every page at least once after its last change to figure or layout. Faults found and fixed that way: labels colliding on the metro map; captions overlapping panels on the torus page; the white corner angles on page 3 printed although the caption said they were not; a table running off the panel on page 24; headings touching labels on pages 22 and 25; a degenerate face in the contracted triangulation on page 23.

Faults I left: pages 16 and 25 have about a quarter of the page white; on pages 22 and 25 the second heading sits close to the labels above it; on page 18 two of the fourteen one-half labels touch; the contents thumbnails are too small to read their inner labels, as thumbnails are.
