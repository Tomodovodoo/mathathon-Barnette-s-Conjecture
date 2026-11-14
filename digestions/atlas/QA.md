# Visual and mathematical QA

COMPUTED. `python digestions/atlas/build.py` renders every standalone page at 108 dpi. `python digestions/atlas/audit.py` checks the resulting vector PDFs, page counts, explanation lengths, margins and TeX overflow. PNGs and contact sheets are in `renders/`. The collected PDF uses the same generated page bodies.

Visual review used the individual PNGs, not just extracted text. All pages were opened and inspected. The following fixes followed that inspection:

- 01: the right metro track now runs upward in proof order.
- 02: all eight terms and both regroupings fit beside the checked running pair.
- 03: exact cube marks identify the pair as well as the white face and intersection face. The running triangulation, whose minimum cycle count is two, is distinguished from the cube.
- 04: the full degree-ten polynomial made the line unreadable. The figure gives its first two nonzero coefficients and saves the complete expression in JSON.
- 05: integer height labels sit at computed white incentres.
- 06 to 08: tinted disk faces originally hid their edges. Tint now precedes the context-edge layer, with black faces still distinguishable.
- 09: the incidence matrix and its row dependence fit at natural math size.
- 10: the prism formula is explicitly labelled with its source normalization.
- 11: doubled cube spokes use two strokes; no disk is drawn for a backtrack.
- 12 to 13: rings no longer overlap. A lookup table makes every state number recoverable without opening the JSON.
- 14: the harmonic prism picture crowded the central labels. The final picture shows the computed rooted forest and the corner-choice table instead.
- 15: fractional weights have an explicit legend and are never called a state.
- 16: before and after show an actual point-preserving exchange. Every nonroot still supplies one spoke; one face token is repeated and another disappears.
- 17: the caption now says five cube label words, not six richer piece patterns.
- 18 to 19: the G cycle and selected P use the toolkit's checked geometry and encodings.
- 20: produced and missed cycles are compared on identical prism coordinates.
- 21: obligation panels do not pretend to be graph counterexamples.
- 22: log-axis ticks and a directly recomputed nanotube table make the counts readable.
- 23: the witness is enlarged and its crowded cycle labels moved.
- 24 to 26: schematics and endpoint comparisons state their limits; they are not invented constructions.
- 27: the complete two-mate Boolean cube is displayed with opposite computed signs.
- 28: K uses a separately computed plane layout. Overlaying the toolkit's exterior G arcs and exterior H arcs would merge distinct edges, so those routes are not overlaid.

All source lines now allow line breaks at path separators. The final automated audit requires zero overfull TeX boxes and zero raster images inside every delivered PDF. Mathematics in smaller scripts and fractions retains normal TeX sizing; body text is 10pt and graph labels use the toolkit's footnote size.

This review checks legibility and finite illustrated objects. It is not a new independent referee report on the general theorems.
