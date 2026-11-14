# Audit code and outputs

Run from the repository root with Python, NetworkX, SymPy, NumPy, SciPy, PyMuPDF and Pillow installed. pdflatex must be on PATH.

```powershell
python -B research/2026-11-14_sol_atlas-audit/code/render.py
python -B research/2026-11-14_sol_atlas-audit/code/closing_checks.py
python -B research/2026-11-14_sol_atlas-audit/code/find_fs.py
python -B research/2026-11-14_sol_atlas-audit/code/proposed.py
python -B research/2026-11-14_sol_atlas-audit/code/write_edits.py
```

render.py snapshots the atlas, computes its SHA256, extracts its text, renders all 31 pages at 120 dpi and makes eight 4-page contact sheets per mode. It must be run only when intentionally taking a NEW snapshot. Rerunning it against a later atlas replaces the reviewed baseline. Full-size page PNGs stay locally available but are ignored by Git; contact sheets, extracted text and the snapshot PDF are retained. A page's file index is its PDF index. Zero is contents; 1–28 are route pages; 29–30 are sources. The simulation uses the full-severity deuteranopia matrix recorded in the source, applied in linear sRGB and encoded back to sRGB. It is a simulation, not a clinical test.

closing_checks.py imports final_checks.py, which imports remaining.py, which imports extra.py, which imports independent.py. This is a serial chain, not parallel heavy computation. Every stage reconstructs objects from fixtures and the retained certificate, never importing atlas/lib.py, atlas/verify.py or the atlas figure generators. The final JSON contains all 78 checks with expected and actual values. A printed mismatch remains in JSON and must be investigated; the current retained run has zero. It does not independently certify every auxiliary graphic or source proof. Additional asserted facts, such as one compatible lift per small good state, are enforced directly in Python.

The only lab import is the primal-to-dual planar graph adapter used to construct prism inputs. Independent computations enumerate matchings, induced-tree partitions, potentials, determinants, forest constraints, cycles and lifts in this folder. proposed.py imports the copied toolkit to use the atlas's drawing system. It does not call its running() function, shared atlas computations, or write its layout cache. The FS search invokes plantri -ba at successive orders from 6 and stops at the first order with an example excluding some but not all cycles for one class. It finds order 10, index 1, fourteen cycles and thirteen qualifying. This is not a census of all larger graphs.

| Output | Producer |
|---|---|
| snapshot-*, snapshot.json, extracted.txt, p-sheet-*, gray-sheet-*, deut-sheet-* | render.py |
| independent.json | independent.py |
| extra.json | extra.py |
| remaining.json | remaining.py |
| final-checks.json | final_checks.py |
| closing-checks.json | closing_checks.py |
| fs-witness.json | find_fs.py |
| cut-connections.json, aligned.json, rays.json and proposed .tex/.pdf | proposed.py |
| edits.json, EDITS.md | write_edits.py |
| root-separation-witnesses.json | one-off command recorded below |

The root-separation witnesses were generated after importing independent.py, selecting each z with nx.is_forest(qgraph(z)) and not good(z), and recording nx.shortest_path(qgraph(z),a,b) for each connected root pair and dets[names[z]]. They are states 3,5,6,7,10. This is equivalent to the predicates already checked by final_checks.py.

The proposed PDFs were rendered for inspection with PyMuPDF get_pixmap(dpi=110). Those PNGs are in outputs/p06-rays.png, p11-matrix.png, p22-connections.png, p23-aligned.png, p24-colour-restriction.png, p16-count-strip.png and p25-count-strip.png. The mathematical source is the PDF/TikZ, not the render.

Source review is manual, documented page by page in AUDIT.md. The large source-reported censuses and the entire geometric marked set were not rerun. closing_checks.py independently reproduces the exact 4,000-tree histogram and reconstructs all four backward prism states. The independent matrix checks and coefficient comparison do not imply that the atlas itself has been machine-formalized.
