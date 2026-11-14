# Review of the figure sequence, second pass

Before and after renders are in `before-after/` (`before-NN-*.png` from commit `af6c63a`, `after-NN-*.png` from this pass, both at 150 dpi; `before-gallery-*` and `after-gallery-*` are whole pages at 70 dpi). I looked at every one of them.

## What I changed across the whole sequence

**The example.** The first pass drew a 14-vertex triangulation whose root face contained a vertex of degree 8. Seven faces had to share that 60 degree corner, so slivers were unavoidable in any layout with that outer face. I first tried the other faces of the same triangulation as `t0` (`explore_roots.py`, output in `explore_roots.json`; it ran against the first-pass `example.json`, which is now only in git history). Two choices keep a cyclic pair and add `D`-cycles with interior vertices, but the degree-8 vertex stays next to two roots. So I searched for a better triangulation.

COMPUTED (`search_example.py`, `plantri -bc4`, all 4-connected Eulerian triangulations with 8 to 14 vertices, every face as `t0`; candidates in `search_example.json`, the 13-vertex ones in `search_example_13.json`):

- no rooted triangulation with at most 11 vertices has a pair with cyclic `Q_s`; 2 of the 100 with 12 vertices do, and 4 of the 66 with 13 vertices;
- exactly one triangulation with at most 13 vertices has a rooting with both a cyclic `Q_s` and a `D`-cycle that encloses a vertex. It has 13 vertices, maximum degree 6, and four such rootings;
- at 14 vertices the only triangulation with both properties is the first-pass one, with its degree-8 vertex.

The 13-vertex triangulation with `t0 = {0,4,5}` is now the running example. It is smaller than the old one and shows more. One pair of states `(r,s)` carries the whole middle of the proof: `Q_s` has a cycle, so `(r,s)` cancels against `(r~,s)`; the same two states in the other order have `Q_r` a forest, and recovery from `(s,r)` gives the Hamiltonian cycle. Its `D` has a 7-cycle with three interior vertices and a triangle nested inside it.

**The layout (problem 1).** The outer face is now the outside of a circle, with the roots on the circle and the outer edges as arcs. A root then has 180 degrees for its edges instead of 60. Interior coordinates come from a Tutte start and a relaxation that penalises small corners and unequal areas (`layout.py`). An equal-area target for every face failed: the three faces on the arcs each contain a circular segment about four times the mean area, and the optimiser pushed their apexes onto the rim to shrink them. Letting those three faces be three times larger fixed it. Result: smallest corner 20.2 degrees (Tutte start 6.3), area ratio 2.4 among the other faces (Tutte start 32.5). Every figure of the running example uses these coordinates.

**The marks (problem 2).** A state is a filled sector inside its black triangle at the chosen corner, clipped to the triangle. `s` is solid blue. `r` is a vermilion outline with a white inside. They differ in fill, so greyscale keeps them apart, and a wedge cannot be read as belonging to a neighbouring triangle.

**Captions (problem 3).** No status tags, no repeated "t0 is the outer black face". Each caption says what to look at and what follows. Numbers in captions are either formatted from checked values or asserted in `check.py` ("facts the captions state in words"). Status tags are in `paper/figures/README.md` and in the `drawn_from` field of `captions.json`.

**Scale (problem 4).** Comparisons are side by side at 7.2cm per panel (0.45 of the text width). Single-panel figures keep the same unit, so line weights, wedges and labels have the same size everywhere. Labels are `\footnotesize`. The gallery went from 14 pages for 14 figures to 10 pages for 15, two figures per page with body text between them.

**The outer face (problem 5).** A grey collar round the disk, in the grey of the black faces, shows that the outside is a black face. Its centre `c0`, which is also the vertex of `G` in `t0`, is a mark below the disk inside the collar. Spokes and edges of `G` that reach it run along the collar as arcs. No rectangle.

**Consistency (problem 7).** One style file defines every encoding and the README has the table. `G` is always drawn on the layout of `T`, with its vertices at face centres and each edge crossing its dual edge, so the cycle in Figure 2(b) is visibly the curve in Figure 13(b). Black faces went from 9% to 17% grey.

## Figure by figure

| New | Old | What was wrong | What I did |
| --- | --- | --- | --- |
| 01 cube | none | No small complete example. The outline wants the cube first. | New. Six panels on about half a page: the cube with a disconnected 2-factor, the cube inside the octahedron, the two states and `D`, `Q_s`, kept spokes with the white tree, and `P` with the two trees and the cycle. All from `check.octahedron()`. |
| 02 two factors | 01 | `G` had its own Tutte layout unrelated to `T`. Two stacked panels took a page. | `G` on the layout of `T`, side by side. The 2-factor is chosen with exactly two components. |
| 03 dual | 02 | Slivers at the apex, labels on top of edges, faint face colour. | New layout, `G` overlaid in grey, labels pushed off the edges, `t0` named once. |
| 04 local | none | The paper's Figure 1 had no counterpart. | New schematic of one triangle: `r(t)`, `s(t)`, `u(t)`, the `D` edge, the `Q_s` edge, and the two-spoke detour with its weights. |
| 05 state | 04 | Disks near vertices; one could not tell which triangle a mark belonged to. | Wedges. A second panel shows the same data as the incidence graph with `r` and `s` as two disjoint perfect matchings. |
| 06 flow | none | Proposition 3.1 had no picture. | New. The network with capacities 2, 1, 2 on the real incidence graph, the flow `r + s` highlighted, and the tight set `S = {2}` named in the caption. |
| 07 pair and D | 05 | Marks ambiguous, arrowheads invisible, a page tall. | Wedges for both states, visible arrowheads, side by side. |
| 08 disk | 07 | `I = 0`, so `I` taught nothing; counts in a line under the picture. | The 7-cycle with `B=5, W=6, I=3, h=7, l=2`. Interior vertices ringed, the two `l` arrows marked, and the `r`-wedges of the five inside black faces drawn, so `B = I + l` can be read off face by face. Counts and the three equations sit beside the picture. |
| 09 Q | 06 | Two unrelated states; marks ambiguous. | The two states of the one pair: `Q_s` cyclic, `Q_r` a forest. |
| 10 cancellation | 08 | The reversed cycle was hard to find among the dashed edges. | The cycle is heavier and directed, the face it encloses is tinted, and the phases `i^0` and `i^-2` are under the panels. |
| 11 spokes | 09 | Two panels, no link to the leading coefficient, circulations given as decimals in coordinate units. | One panel plus the formula. Detours solid, original arrows dashed, enclosed regions tinted. With unit circulations `L+ - L-` is the number of white faces inside, 6 and 1, and the group's contribution to `Z(x)` is written out. This also covers missing figure (d). |
| 12 tree and cotree | 10 | Rectangular detour to `c0`; jagged white tree; a page tall. | `c0` on the collar, spokes along it. Panel (b) shows only the deleted spokes and the white tree. |
| 13 selected | 11, 12, 03 | Three figures said the same thing; the old 03 and 12 were near duplicates. | One figure: `P` with the white tree that selects it, then `P`, the two classes and the closed curve. |
| 14 gluing | 13 | Two disconnected pieces, no glued result, partition found by brute force. | Three panels: outer piece with the cap tinted, inner piece with the cap as outer face, glued result. The partition comes from running the construction on each piece with the prescribed edge, as in the proof. |
| 15 overview | 14 | A plain chain of boxes that left out the disk identity and the gluing. | Side boxes for the disk identity (used twice), the no-separating-triangle hypothesis and the gluing, with figure numbers. |

## Missing figures (problem 8)

(a) Added as Figure 1. (b) Added as Figures 5(b) and 6. (c) Added as Figure 4. (d) Folded into Figure 11, because the two orientations and the enclosed region are the same picture as the detour.

## What is still not good

- The white-face tree (12b, 13a) is routed around the corner of each deleted spoke. It is correct and each edge crosses exactly its spoke, but the curves wander. A hand-tuned route per edge would read better.
- In the cube figure the cube has one vertex below the picture. That is what a vertex in the outer face looks like, and it keeps `G` and `T` on one layout, but it is not the square-in-square drawing a reader knows.
- Smallest corner is 20 degrees. With 13 vertices and three roots on the boundary I could not get above 24 without making the middle faces much smaller than the rest.
- Figure 6 orders the vertices along the cycles of `D`, so the unused incidences cross the picture. They are thin, and I left them.
- I checked edge crossings of `T` by computation. I did not check by computation that the curved edges of `G` and the white tree cross only what they should; I checked those by eye in the renders.
- Greyscale: I designed for it (fill versus outline, dash patterns, weights) and looked at the colour renders. I did not produce greyscale proofs in this pass.
