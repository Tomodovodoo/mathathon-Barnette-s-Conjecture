# Independent checks

Status COMPUTED. Run commands from the repository root with Python 3.14 and NetworkX installed. No project proof implementation is imported. `check.py` has its own state enumeration, pair operations, side choices, sign product, face paths, heights, cycle interiors, selections, recovery and disk counts. It reuses only the existing plantri executable as a generator. `examples.py` imports this independent implementation.

```powershell
python research/2026-11-14_sol_referee-main/code/check.py
python research/2026-11-14_sol_referee-main/code/examples.py
python research/2026-11-14_sol_referee-main/code/supplement.py
python research/2026-11-14_sol_referee-main/code/make_edits.py
python research/2026-11-14_sol_referee-main/code/insert_replacements.py
```

The full census took about five minutes in this environment. Each other command took seconds. The initial attempt to generate order 4 failed because plantri's Eulerian generator requires order at least 6; the script was corrected before the successful run. There are no missing coloured inputs at orders 4 and 5: alternating face colours force even vertex degree, triangular simple faces force degree at least 3, hence at least 4, whereas the total degree is 6V-12. This is impossible at V=4 or 5. Order 7 is generated and returns zero classes.

## Files and ranges

| Output | Producer and range |
| --- | --- |
| plantri-6.txt through plantri-12.txt | `check.py` runs `workings/barnette_lab/vendor/plantri.exe -b -a N`, N=6 through 12; records stdout and stderr. Numbers of classes are 1,0,1,1,2,2,8. |
| census.json | `check.py`, all 15 generated classes, every face as t0, both induced choices of black colour, 262 rootings; adds running example, one cube rooting and one prism rooting, giving 265 recorded model checks. Mirror embeddings are represented once, as in plantri's unoriented census; the proof's sign conventions were checked locally for both directed orientations. |
| running.json | `check.py`, all states, pairs, heights along specified shortest paths, and all acyclic selections of paper/figures/running.json. Includes the 12 state tuples and every avoiding-cycle complement. |
| cube.json | `check.py`, the unique six-vertex triangulation with one root. The exact labels of the printed cube are separately checked in examples.py. |
| prism.json | `check.py`, hexagonal bipyramid, equator 0 through 5 and apices 6,7; one root, all three prescribed sides. |
| examples.json | `examples.py`, all printed rows of Table 2, both named running states, changed partner, listed vertex sets and cycles, both Figure 9 heights, exact labelled cube selection, exact Figure 11 selections and their union, 9-vertex double octahedron at every root, and the 11- and 26-vertex examples. Table 1's reversal properties are checked by the census. |
| supplement.json | `supplement.py`, direct max-flow and generic corner-weight polynomial evaluations on all 262 roots; S_s tree equivalence on 5,118 state-side choices; 290 representative D disks; 560 finite-difference examples, c=0 through 6 and m=0 through c, 20 integral choices each. Includes a complete 9-vertex no-pair witness for the suppressed hypothesis in the polynomial remark. |
| edits.json, ../EDITS.md | `make_edits.py`, eight exact replacements with source line numbers, asserting one occurrence of each old string. Never writes paper/. |
| fingerprints.json | `make_edits.py`, SHA256 of audited PDF and TeX, example input, and held sources. |
| environment.json | Python command below, dependency versions and interpreter. |

The combined census checks 1,723 states, 636 pairs, 1,140 D-cycle reversals, 6 Q-cycle reversals, 707,952 arbitrary chosen-side systems, 239,180 chosen directed cycles, 97,640 density subsets, 1,890 good-state recoveries, 4,826 rooted acyclic selections and 3,336 compatible pairs of acyclic selections over 152 rooted separator occurrences. These counts include repeated underlying graphs under different roots and the three extra example calls. They count checks, not nonisomorphic mathematical objects.

Every arbitrary side system takes one of the two edges at every state corner, exhaustively. Every selection is enumerated as a perfect matching between all black and white faces, independently of good-state recovery. Hamiltonian cycles are counted by connectedness of the degree-two complement of such a matching. All face rootings of the generated triangulations are included, even when there is no pair. All root-containing vertex subsets are included in the density check, without imposing no separating triangles until testing the conclusion of Proposition 5.2. Cap colour and gluing are tested at every generated separating triangle, with every acyclic selection in each capped piece that agrees on the triangle.

The scripts do not enumerate every possible unrelated connected plane graph in Lemma 2.5, or every simple face path. Those general statements were audited by proof. The code is finite corroboration and a counterexample search, not a substitute for that audit. No failures of a core claim occurred.

## Rendering and source extraction

The Phase 1 pages were produced before source reading by the following command, then each page image was opened in order with the image viewer:

```powershell
python -c "import fitz; d=fitz.open('paper/main/barnette.pdf'); [(p.get_pixmap(dpi=130).save('research/2026-11-14_sol_referee-main/pages/page-%02d.png'%(i+1))) for i,p in enumerate(d)]"
```

The held PDF text files in this folder are extraction aids produced by PyMuPDF, not new source versions. To reproduce them and the citation-page PNGs:

```powershell
python research/2026-11-14_sol_referee-main/code/render_sources.py
```

This includes PDFs found in the history-literature folder after the first papers/ inventory: Hertel, Alt et al., Brinkmann-Goedgebeur-McKay and Schnieders. The indexed papers/ holdings alone are incomplete.

The environment record was generated with:

```powershell
python -c "import sys,json,networkx,fitz,pathlib; pathlib.Path('research/2026-11-14_sol_referee-main/code/environment.json').write_text(json.dumps(dict(python=sys.version,networkx=networkx.__version__,pymupdf=fitz.VersionBind),indent=2))"
```

No server, browser preview, external theorem database, or external model was used. The input rotation systems and the independent scripts are sufficient to rerun the mathematical checks with the stated dependencies.
