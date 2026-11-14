# Proposed atlas figures

These files are proposals. No live atlas text or existing figure was edited.

| Source and PDF stem | Destination | Integration |
|---|---|---|
| p06-rays | route 6 | Add beside or below the first involution. Two panels show an actual crossing-pairing move on the running example. A single token is shown, not a complete marked object. |
| p11-matrix | route 11 or companion page | The actual symbolic 5 by 5 coefficient matrix for the hexagonal-prism dual, with graph labels and extracted coefficient. Replace the formula-only ledger or allocate a companion page. |
| p16-count-strip | route 16 | Insert into the empty band below the nine-state row. |
| p22-connections | route 22 bottom section | Six connection signatures on the same four-cut. Retain the triangle row. Boundary labels 0,1,2,3 mean vertices 1,6,11,8 in that order. Inside and outside are relative to the root face. A semicolon separates disconnected boundary blocks; a slash separates the two tree classes. |
| p23-aligned | route 23 panels a and b | Replace both panels together. Roots and vertex labels persist; the smaller layout minimizes displacement subject to positive oriented face areas. Use the existing lift and repair panels below. |
| p24-colour-restriction | route 24 panel c, preferably two panels | A 10-vertex triangulation where the relaxed radial-tree condition passes on 13 of 14 Hamiltonian partitions for colour class 2, encoded as triangles. Filled tree qualifies on the left. Both trees fail on the right. This is not a test of the extra proper-quasi-vertex restriction. |
| p25-count-strip | route 25 | Insert into the empty band below the four backward-state panels. |

COMPUTED. Generated and asserted by research/2026-11-14_sol_atlas-audit/code/proposed.py. The matrix coefficient is compared symbolically with an independent pair expansion. Rays use rational line intersections and an involutive return check. The cut diagram groups all 28 independently enumerated induced-tree partitions by complete side signatures. The colour example is found by find_fs.py, with all fourteen partitions enumerated. Contraction orientation and absence of edge crossings are checked with the toolkit.

Compile from the repository root with `python -B research/2026-11-14_sol_atlas-audit/code/proposed.py`. Dependencies and evidence are in that folder's code/README.md. The script imports the permitted toolkit only for modelling, layout and drawing, and writes no cache into the atlas. The .tex and .pdf files are retained; TeX logs are ignored. Atlas styles are found through TEXINPUTS.

All PDFs were rendered and inspected during the review. The strips are supplements, not full page replacements. Scale the matrix by the page width only if its letters remain readable; it is designed as a vertically stacked graph and matrix, rather than two small side-by-side panels. No proposed exception-pattern panel or drawing-free-marks panel is supplied; those remain listed in the audit.
