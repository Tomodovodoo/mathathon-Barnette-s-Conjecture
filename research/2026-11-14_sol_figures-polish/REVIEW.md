# Finishing review

I inspected all fifteen initial PDFs after rendering them with PyMuPDF, then all sixteen final figures in colour, greyscale and full-severity deuteranopia simulation. The initial and final images are 150 dpi. The contact sheets are review aids; use the individual images for close inspection.

## Figure by figure

### 01-cube

Replaced the below-picture cube by two concentric squares, using the checked four-cycles to assign vertices. Panel b now shows the octahedron alone, rather than repeating the distorted cube overlay. Reduced geometry to 0.34cm per unit while keeping physical fonts and strokes, and shortened the worked caption.

[Before](before/01-cube.png) | [After](after/01-cube.png)

### 02-two-factors

Routed every edge through its exact dual midpoint. Standardized G dots to 1.5pt. Shortened caption and corrected the reference to the final cycle.

[Before](before/02-two-factors.png) | [After](after/02-two-factors.png)

### 03-dual

White centres moved to incentres, including circular-sided boundary faces. All dual routes have explicit midpoint joins and computed crossing checks. Shortened caption.

[Before](before/03-dual.png) | [After](after/03-dual.png)

### 04-local

Kept the local geometry and its solid/dashed distinction. Shortened the caption to the choices and spoke weight. Inspected both accessibility proofs.

[Before](before/04-local.png) | [After](after/04-local.png)

### 05-state

Kept the wedges and the double/single incidence edges. Shortened caption to the matching interpretation. Inspected both accessibility proofs.

[Before](before/05-state.png) | [After](after/05-state.png)

### 06-flow

Kept the flow geometry and capacities. Caption now isolates the integral degree-two flow and tight cut; its value and tight vertex are asserted in check.py.

[Before](before/06-flow.png) | [After](after/06-flow.png)

### 07-pair-D

Kept checked states, directions and cycle lengths. Inspected colour, greyscale and simulation; outlined/filled wedges remain distinct.

[Before](before/07-pair-D.png) | [After](after/07-pair-D.png)

### 08-disk

Kept disk geometry and ringed interior vertices. Shortened the caption around the face-to-choice count rather than repeating the whole display.

[Before](before/08-disk.png) | [After](after/08-disk.png)

### 09-Q

Kept the two opposite-side edge sets. Shortened caption and made the recovery pair (s,r) explicit.

[Before](before/09-Q.png) | [After](after/09-Q.png)

### 10-cancellation

Kept heavy directed cycle emphasis and phase display. Shortened caption to what changes, what stays fixed and why the signs cancel.

[Before](before/10-cancellation.png) | [After](after/10-cancellation.png)

### 11-spokes

Added W=6 and W=1 labels in separated white regions. Moved the large count away from the nested small region. Shortened caption. All-cycle lab check supports the count interpretation on the stated finite range.

[Before](before/11-spokes.png) | [After](after/11-spokes.png)

### 12-tree-cotree

Replaced the wandering five-waypoint spline by two short cubic pieces through each deleted-spoke midpoint. The common tangent is transverse to the spoke. Moved white centres to incentres. All spokes, including the exterior ones, are tested as forbidden crossings except the intended spoke.

[Before](before/12-tree-cotree.png) | [After](after/12-tree-cotree.png)

### 13-selected

Uses exactly the same incentres and white-tree curves as Figure 12. The complementary Jordan curve uses the same checked G routes as Figures 2 and 3. Shortened caption.

[Before](before/13-selected.png) | [After](after/13-selected.png)

### 14-gluing

Kept the three constructions. Shortened the caption and added explicit assertions for the cap vertices and prescribed edge named there.

[Before](before/14-gluing.png) | [After](after/14-gluing.png)

### 15-overview

Kept the dependency chart. The new gallery pairs it with gluing, with no float deferral. Inspected both accessibility proofs.

[Before](before/15-overview.png) | [After](after/15-overview.png)

### 16-at-a-glance

New six-panel horizontal strip of the running example, with six explanations below. States and selected objects come from the same checked data as the detailed sequence. Separates cancellation from the nonvanishing step that supplies a forest pair.

[New figure](after/16-at-a-glance.png)

## Accessibility

Black faces remain grey and white faces remain unfilled. Outlined r wedges and filled s wedges survive both conversions. Incidence matchings use double and single strokes. D is solid and Q is dashed. The white tree is dash-dot with hollow circles. P is heavier and black; the Jordan curve has a lighter grey value and runs across the complementary edges. Filled disks and hollow squares distinguish the induced classes. I found no encoding failure requiring a palette change.

[Greyscale proof](greyscale-proof.pdf) | [Deuteranopia proof](deuteranopia-proof.pdf) | [Gallery contact sheet](gallery-sheet.png)

The simulation applies the explicit full-severity deuteranopia matrix in proofs.py to linear RGB, then returns to sRGB. It is a simulation, not a physical print test.

## Computed audits

COMPUTED, `paper/figures/check.py` and `geometry_check.py`. The drawing and validator share the cubic controls, rounded as emitted to TeX. Every G edge crosses exactly its T edge once, and every white-tree edge exactly its deleted spoke once, at 160 samples per cubic. Boundary circles and exterior arcs have 360 intervals. This checks the displayed running and octahedral examples, not arbitrary drawings. See `paper/figures/geometry-validation.json` for minimum crossing angles.

COMPUTED, `caption-audit.json`, produced by proofs.py from the rendered gallery. Captions 2 to 16 use three to five lines. Caption 1 carries the worked example and uses eight. Page groups are [1], [2,3], [4,5], [6,7], [8,9], [10,11], [12,13], [14,15], [16]. No page is blank; no page has more than two figures.

COMPUTED, `paper/figures/audit.py` and `style-audit.json`. All explicit font declarations are footnotesize. Smaller PDF glyphs are TeX math scripts and display limits. The source inventory includes line widths, font commands and colour declarations from every figure body and standalone wrapper, draw.py and the style file. The historical first-pass style differs from the current second-pass implementation; all retained differences and local emphasis overrides are listed in that JSON. No new colour or label-size exception was introduced.

COMPUTED, `check_hunch.py`, `hunch-results.json`. Every face choice on every stored JSON lab instance, all four named examples and generated(12): 322 rooted instances, 1,784 ordered pairs, 2,320 D-cycle occurrences, 6 to 26 vertices in T. Exact integer spoke weights from the lab give L+ - L- = W in every case. Provenance duplicates are retained. This is finite evidence for the second-pass HUNCH.

## Remaining limits

The square cube and the octahedron are separate plane embeddings of a checked dual pair. Their vertices are not positioned as an overlay. The introduction strip is deliberately small and should be read together with its explanations and the detailed figures. Geometry validation samples curves rather than certifying them symbolically. The second-pass historical style file remains unchanged in its owner folder.
