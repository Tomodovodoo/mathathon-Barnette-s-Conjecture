# Build and use the figures

The gallery is the entry point. It contains fourteen figures at natural size in a 10pt `amsart` A4 document with 1in margins. The standalone PDFs are vector drawings with embedded LaTeX fonts. Every PDF has a corresponding `.tex` source. The `-body.tex` files omit the document wrapper for direct manuscript inclusion.

## Build

From the repository root, with Python and `pdflatex` on PATH:

```powershell
python -m pip install networkx numpy scipy pymupdf pillow
python paper/figures/build.py
```

This runs `model.py`, `check.py`, `draw.py`, compiles all fourteen standalone files and the gallery, then renders every PDF page to `renders/`. It stops on a failed mathematical assertion or TeX error. The main build uses saved coordinates and does not require SciPy. SciPy is only needed to rerun layout optimization.

Optional independent check, once `workings/barnette_lab` exists:

```powershell
python -m pip install sympy
python paper/figures/crosscheck_lab.py
```

This writes `lab-export.json` using the reference implementation's schema-1 exporter, plus `lab-crosscheck.json`. It does not modify that implementation. Its face numbering can differ from ours; the checker maps faces by their vertex sets.

To regenerate the source-paper inspection images, run from the repository root:

```powershell
python paper/figures/audit_render.py
```

To repeat the deterministic witness search, run `python paper/figures/search.py`. It starts with the octahedron, applies seeded even-degree vertex splits, and checks each candidate exhaustively until it finds a cyclic paired state. This overwrites `running-primal.adjlist`. Normal builds read that fixed adjacency list. `python paper/figures/layout.py` recomputes the optimized coordinates from `example.json`; normal builds read `layout.json`.

## Files and data contract

- `running-primal.adjlist` is the combinatorial input, a 24-vertex cubic bipartite planar graph. `model.py` takes its planar dual and enumerates all states and disjoint pairs. Vertices and faces are integers.
- `example.json` records `vertices`, `edges`, cyclic boundary lists `faces`, face-index lists `black`, `white`, `A`, vertex lists `roots`, `X`, two ordered state arrays `cyclic_pair`, `forest_pair`, and `coordinates`. Face zero is the black outer face. A state array is indexed by `A`, not by all faces. Coordinates have stringified vertex keys.
- The root array has geometric order lower left, lower right, apex. Its coordinates are `[0,0]`, `[12,0]`, `[6,10.392]`. Other vertices lie strictly inside. This explicit boundary convention controls exterior routes.
- `check.py` derives `checked.json`, including Q's reversal cycle, the reversed pair, white-tree edges, selected edges, induced-tree classes, Hamiltonian edges, dual crossings, disk counts, spoke weights and positive circulations. `validation.json` lists the assertions run.
- `draw.py` consumes `checked.json` and writes the TikZ sources and captions. `barnette-figs.sty` owns all encodings. Its `panel` renderer supports face colouring, state marks, both pair marks, D, Q, the counted disk, incidence spokes, detours, the white tree, P, induced classes and the Jordan curve.
- `gluing.json` records the separate checked nine-vertex example used only in Figure 13.

To swap a reference implementation's export later, map its `T_edges` to `edges`, preserve `faces` and face-index arrays, put the outer face first and remap all face IDs, and select a forest pair and a cyclic pair from its states. Supply the boundary coordinates above. Then run `python paper/figures/build.py --from-json`. This skips `model.py` and preserves the replacement `example.json`. The current sequence and some captions intentionally specialize to the delivered 14-vertex witness: update its named disk counts, phase labels and figure counts when changing examples. The shared export was not ready when the witness search started; it was used for the later independent check.

## Mathematical scope

COMPUTED: `model.py` and `check.py` exhaust all 15 states and 10 ordered disjoint pairs of the fixed witness. Two pairs have cyclic Q. The displayed involution exchanges them. The other eight pairs have forest Q. Assertions verify the selected forest, both induced trees, the complete Hamiltonian cycle, and the separate two-component 2-factor. This is finite verification, not a new general proof.

LIT: the general implications and the overview follow OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, September 24, 2026, Sections 3-7, supplied as `papers/OpenAI-Barnette.pdf`. The source audit and fixed design rules are in `research/2026-11-14_astra_figures/`.

The disk shown has no strictly interior vertex. Its values are B=1, W=2, I=0, h=5, l=1. The full running example still shows three D cycles, a cyclic Q, the cancellation involution, the detour, and recovery. The gluing witness must be separate because the running triangulation has no separating triangle.

## Manuscript inclusion

Make this directory available to TeX's input path, load `barnette-figs`, and use `\input{05-pair-D-body.tex}` inside a centred figure environment. Use the caption from `captions.json`. Do not use `\resizebox` or `\includegraphics[width=\textwidth]`: the natural dimensions are deliberate, and rescaling would change fonts and stroke weights. The standalone files include a 6pt white border.

All renders are QA artifacts. The manuscript should include TeX or PDF, not PNG. `.aux`, `.log` and Python caches are ignored.

Run python paper/figures/qa.py after a build to refresh qa.json, the gallery contact sheet, and selected greyscale renders. Run python paper/figures/candidates.py to reproduce the rejected symmetric-example counts.
