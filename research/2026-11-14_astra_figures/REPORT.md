COMPUTED: Delivered fourteen compiled vector figures and an A4 amsart gallery, generated from checked data.
COMPUTED: The running 14-vertex triangulation has 15 states, 10 ordered disjoint pairs, and two cyclic pairs.
COMPUTED: Independent barnette_lab checks agree and recover the forest-state certificate.
The audit covers every figure in all three supplied PDFs, using rendered pages.
The main limitation is a specialized example pipeline; swapping examples still requires caption and boundary-convention updates.

# Report

## Aim and delivery

I set out to make the whole dual proof visible on one example, while replacing inconsistent scaling and tiny subfigures with fixed physical dimensions. The files are restricted to this research directory and `paper/figures/`.

`FIGURE-AUDIT.md` records the source review. `FIGURE-STYLE.md` fixes widths, unit scale, labels, strokes, palette, conventions, caption rules and placement. `paper/figures/README.md` gives the build commands and JSON contract. `gallery.pdf` is the fourteen-page scale review. Each figure has a standalone PDF, wrapper TeX and inclusion body. Every final PDF was rendered, and the individual figures plus the page gallery were visually inspected. The final review also included greyscale cancellation and a gallery contact sheet. `qa.json` confirms fourteen single-page figure PDFs and a fourteen-page gallery, no embedded raster images, and no overfull TeX boxes.

## Established

COMPUTED, `paper/figures/model.py`, range all states of the fixed 14-vertex witness: 15 states and 10 ordered disjoint pairs. Two ordered pairs have cyclic Q; the other eight have forest Q. The displayed cyclic pair has three D cycles. The involution fixes its second state and changes J from 3 to 1. `check.py` verifies the inverse move, state bijections, pair disjointness, and phase difference.

COMPUTED, `check.py`, displayed forest pair: the retained incidence graph is a tree; the white-face tree has 12 vertices and 11 edges; P has exactly one side in every face and induces two trees. The complementary dual is connected and degree two on all 24 vertices. A separate displayed 2-factor has exactly two components. The primal is cubic, bipartite and 3-connected, and the dual has no separating triangle. These finite certificates are in `checked.json` and `validation.json`.

COMPUTED, `check.py`, displayed disk: B=1, W=2, I=0, h=5, l=1. It satisfies all three disk equations. Strictly interior vertices are absent in this chosen disk; the zero is stated explicitly rather than hidden.

PROVED-HERE, `AREA-CIRCULATION.md`: determinant spoke weights give the positive area of a counterclockwise simple spoke polygon. This provides a direct weight assignment for the straight-line figures. COMPUTED, `check.py`: the three displayed counterclockwise spoke cycles have positive circulations, approximately 5.641, 5.289 and 11.033 in coordinate-area units. Physical area changes by the square of the fixed TikZ scale; the sign does not.

COMPUTED, `draw.py`, the first 19 of 64 possible partitions with fixed boundary labels in the nine-vertex gluing witness: a valid pair of induced trees is found in two octahedra glued across a triangular face. The classes intersect in edge 01 and vertex 2 respectively. The output records the actual graph and partition in `gluing.json`.

COMPUTED, `crosscheck_lab.py`: a later independent check with the shared implementation agrees on the state and pair counts, validates both displayed pairs and their reversal, and recovers exactly the same selected edges and Hamiltonian cycle. It exports the witness through that implementation's schema-1 exporter as `lab-export.json`. The implementation was read but not edited.

LIT: the universal proof dependencies in Figure 14 follow Sections 3-7 of the supplied OpenAI paper. The gallery labels finite illustrations COMPUTED and the overview LIT. No finite enumeration is presented as a proof of Barnette's conjecture.

## What failed and why

COMPUTED, `candidates.py` and `candidate-checks.json`: the cube, truncated octahedron, and even prisms with base lengths 6 through 24 have no cyclic Q among their disjoint pairs for the chosen roots. They cannot illustrate fixed-second-state cancellation. The seeded vertex-split search in `search.py` finds a less symmetric 14-vertex example that can.

The raw Tutte embedding clustered several vertices near the apex. An initial repulsion-only optimization spread vertices but made boundary faces nearly flat. The final optimization balances vertex separation with a log-area objective, preserves signed triangular orientation and keeps a positive area lower bound. Saved coordinates make the ordinary build repeatable.

The initial two-column grid forced cramped marks. Stacking panels keeps the graph unit at 0.72cm throughout. Inspection caught exterior routes and count labels outside the reserved TikZ bounds; the final bounds include them. A check also caught a caption that said two cycles while the first enumerated disconnected 2-factor had more. The search now explicitly selects two components and asserts that count.

## Open limits

The pipeline is a reproducible example generator and renderer, not a general graph-drawing library. `build.py --from-json` accepts prepared replacement example data, but the outer-boundary ordering, some count labels and captions are specialized. The README identifies these assumptions rather than promising automatic replacement of every example.

The running example has no separating triangle, so gluing necessarily uses a separate witness. The disk example has I=0. A supplementary disk with a strictly interior vertex would help teach the role of I. The requested sequence is complete, but the capacity network, two groupings of the exponential sum, and constructive marked walk remain useful supplementary diagrams.

The mathematical code validates combinatorics and coordinate orientations. Visual routing was also inspected. It does not yet run a general exact segment-intersection and label-collision checker. Printer proofing on paper remains useful for the 0.35pt context edges.

## Three next steps

1. Integrate the body files at natural size beside their first references, using the generated captions and the placement rules.
2. Add a schema-1 adapter that remaps face IDs and generates example-dependent caption values automatically. Keep the independent checker as a regression check.
3. Add supplementary pictures for the flow cut, the two groupings of Z, and a disk with I greater than zero.

## Leads for others

COMPUTED: the small symmetric examples conceal cancellation entirely. Expositions should not infer the general structure of paired states from the cube. The checked 14-vertex witness and its independent schema-1 export are available for the algebra, algorithm and proof-audit agents.

PROVED-HERE: area-based spoke weights may simplify the geometric explanation in the exposition when a straight-line embedding is already fixed. The proof is in `AREA-CIRCULATION.md`; the paper's unit-face circulation construction remains the embedding-independent presentation to cite.
