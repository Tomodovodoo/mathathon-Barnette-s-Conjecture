# Reproducing the primal proof checks

Run from the repository root with Python, NetworkX and the existing lab dependencies. The checker imports only `faces_of`, `named_graphs` and `plantri_graphs` from the lab. It does not call the lab's state enumeration, weights, polynomial or recovery functions.

```powershell
python research/2026-11-14_astra_primal-proof/check_primal.py --max-order 20 > research/2026-11-14_astra_primal-proof/check.log
python research/2026-11-14_astra_primal-proof/extract_lean.py
python research/2026-11-14_astra_primal-proof/build_note.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory proofs/primal proofs/primal/primal.tex > research/2026-11-14_astra_primal-proof/latex-build.log
pdftoppm -scale-to 1200 -png proofs/primal/primal.pdf research/2026-11-14_astra_primal-proof/renders/page
```

Create `renders/` before the last command. It is ignored by git. `primal.tex` uses amsart, A4 and a one-inch margin. `build_note.py` appends the exact examples to PRIMAL-PROOF.md, also writes EXAMPLES.md, and translates that same content to TeX. TeX inserts optional line breaks in long numeric lists but omits no prose or formulas. The font packages are Latin Modern and microtype. This avoids MiKTeX's bitmap-font expansion error.

The run uses `workings/barnette_lab/vendor/plantri.exe` if present. Generation uses plane triangulations only as an input census. After conversion to G, every tested object is rebuilt from G and its faces. The checker itself has no dual Instance, spoke graph, or Jordan labelling. `outputs/summary.json` records every primal edge set, so the finite input can be inspected independently of the generator. If plantri is missing, the small prism fallback may lack a cancellation witness and the script deliberately fails its final coverage assertion. The successful committed run used plantri.

Outputs:

- `outputs/summary.json`: command, graph-edge manifest and all check counts.
- `outputs/cube.json` and `outputs/cancellation.json`: vertices, faces, incidences, edges, all states, all ordered pairs and their cut data, flow, weights, polynomial coefficients and explicit recovered cycle.
- `check.log`: one progress line per input graph record.
- `LEAN-EXTRACTS.md`: actual declaration headers read from the existing upstream source clone at the commit stated there.
- `latex-build.log`: successful compilation log. Rendered pages were visually inspected; no overfull boxes remain.

The 16 input records contain 15 plantri classes and the separately named cube. The duplication is intentional for a stable named example. All vertices of each input are used as roots, with the root's colour class called black. Tests enumerate all states and ordered pairs for each rooting, all subsets in the capacity criterion, all three root-edge choices for every eligible recovery state, and all primal perfect matchings. For graphs of at most 12 vertices they also enumerate every bond and every outgoing choice at every state. General-state circuits and pair-related circuits are recorded separately.

Every three-edge cut is checked once per input graph. For each nontrivial one, both caps are built, all their Hamiltonian complements are enumerated, and every compatible pair is spliced and checked in G. Only one process was used for the numerical campaign; the final run took seconds, well below the ten-minute limit.

## Limitations

COMPUTED means finite verification only. The independent mathematical proofs are in PRIMAL-PROOF.md. The code relies on NetworkX's planar embedding and connectivity routines and on the existing generator. No benchmark, polynomial running-time claim, independent generator certification, or new Lean build is claimed.

An early attempt to rebuild an example's embedding by reinserting sorted edges changed NetworkX's face labels. The note builder now reads the exported facial boundary cycles directly. This is why the saved face lists are part of the reproducibility data, not optional decoration.
