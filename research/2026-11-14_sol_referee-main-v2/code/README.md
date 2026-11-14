# Reproduction

All commands below run from the repository root unless a working directory is specified. The code is new for this review. No project or previous referee Python implementation is imported. `verify_numbers.py` reads the face fixtures in `paper/figures/running.json` and `octahedron.json`; `supplement.py` imports only that new engine and uses the existing plantri executable as a graph generator. No subagents or heavy background jobs were used. The longest computation took under two seconds here.

## Commands and outputs

```powershell
python research/2026-11-14_sol_referee-main-v2/code/regression.py
python research/2026-11-14_sol_referee-main-v2/code/verify_numbers.py
python research/2026-11-14_sol_referee-main-v2/code/supplement.py
python research/2026-11-14_sol_referee-main-v2/code/sources.py
python research/2026-11-14_sol_referee-main-v2/code/final_snapshot.py
```

`regression.py` freezes v2-start.tex only if absent. It compares that frozen source with the historical v1, and separately compares the frozen source with the current corrected manuscript. It writes `full.diff`, `environments.diff`, `environments.json`, `displays-captions.json`, `refs.json` and `corrections.diff`. `fingerprints.json` preserves the initial source and PDF hashes and is not overwritten. New final hashes are in `build-verification.json`.

While this review was being written, a concurrent finishing pass modified the shared manuscript in commits edd9c0c,26fa43b,f04e0d1. `final_snapshot.py` freezes the resulting final source, records its full and structured v1 comparisons, isolates the finishing pass, and isolates this referee's changes in `own-corrections.diff` and `last-correction.diff`. The latter is commit e97b061, specifying clockwise reversal in the expanded plan. `corrections.diff` is the aggregate difference from the original v2, including the other agent's finishing pass; CHANGELOG.md lists only this referee's applied edits.

`verify_numbers.py` writes `numbers.json`. Its exhaustive domains are the two states/two pairs of the cube, twelve states/eight pairs of the running example, and three states/two pairs of the hexagonal-prism dual. It lists every state, ordered pair, sign, weight, cycle interior, recovery edge set and component, and the sorted shortest face paths. Hamiltonian counts come from independent enumeration of all primal perfect matchings, not from the state constructor. The respective perfect-matching totals are 9,112,20; Hamiltonian totals are 6,28,8. It also computes Laurent coefficients using falling factorials, including negative weights.

`supplement.py` writes `supplement.json` and `plantri-6.txt` through `plantri-12.txt`. It checks all chosen-side systems, individual height changes under D reversal, signs, exact multivariate monomial dictionaries, cancellation, and the matching-complement connectedness iff. It checks the reverse cycle-to-state map for all root-side prescriptions. The literal eight rows of Table 2 and Figure 11 are asserted rather than reconstructed from their source code. It enters the gluing figure's edges from the rendered picture and checks the resulting 9-vertex selection. It also constructs the radial 11-vertex and three-cubes 26-vertex counterexamples.

The census invokes, serially:

```powershell
workings/barnette_lab/vendor/plantri.exe -b -a N
```

for every integer N from 6 through 12. Standard output and error are retained. A newly written rotation-system face walker decodes each ASCII map. Every face of each generated class is made the black outer face and all its states and pairs are enumerated. There are 15 classes and 262 face rootings. The root-variation fields record whether pair existence differs within one face colour. No coloured simple sphere triangulation has fewer than six vertices, as proved in REFEREE.md. The generator's SHA256 is recorded in supplement.json.

`sources.py` opens the eleven local primary PDFs named in its source map. It extracts their texts to `source-KEY.txt`, then writes `source-locators.json` with PDF page numbers and contexts for each requested locator. The Feder scan has a broken character map, so its first page was rendered and read visually. The textual locator is only a search aid, not a claim that the first occurrence is the theorem rather than an introduction's forward reference. The primary pages and full relevant source text were consulted to resolve this.

## Build

MiKTeX's `latexmk` initially failed because Perl was absent from PATH. Git's existing bundled Perl works; no system installation or persistent environment change was made. From `paper/main`:

```powershell
$env:PATH='C:\Program Files\Git\usr\bin;'+$env:PATH
latexmk -pdf -interaction=nonstopmode -halt-on-error barnette.tex
```

Exit status was zero. The corrected pair was committed immediately as `d3b3651`, touching only `paper/main/barnette.tex` and `.pdf`. The correction list was committed in `24df755`. The final directional correction and rebuild are e97b061. `latex-final.txt` retains the final TeX log, and `latexmk-build.txt` records the final build command's output. There are no undefined references, multiply defined labels, TeX errors or overfull boxes, including boxes under 2pt. The MiKTeX reminder about checking for updates is an installation notice, not a TeX error.

## Rendering, references and bibliography

```powershell
python research/2026-11-14_sol_referee-main-v2/code/render_and_refs.py
```

Uses PyMuPDF 1.27.2.3 to render all 19 pages at 130 dpi into `outputs/renders/page-NN.png`; all were opened and inspected, including a second complete pass after the concurrent finishing edits. It also writes per-page text, `pdf-text.txt`, the resolved-reference JSON and text ledgers, `citations.json`, `latex-final.txt` and `build-verification.json`. It asserts that all 131 final references resolve, all cited keys equal the 17 rendered bibliography entries, and the log has no undefined/multiply defined references or errors and no overfull box beyond 2pt.

Additional read-only source renderings were made with PyMuPDF using `fitz.open(path)[index].get_pixmap(dpi=115).save(output)`: OpenAI PDF pp7,10; unsigned manuscript p2; Feder-Subi p1; GSW v3 p12. Their images are `openai-7.png`, `openai-10.png`, `unsigned-2.png`, `feder-1.png`, `gsw-12.png`. The gluing detail is main p17 clipped to PDF-point rectangle (65,65,535,240) at 220 dpi, saved as `gluing-detail.png`. These were opened to inspect formulas, theorem wording and actual labels.

Online bibliographic spot checks used the publisher/author pages linked in REFEREE.md. Metadata of Tutte, Holton-McKay and Georges was checked; their full original proofs were not accessed. Direct DOI opens for Georges and Ford returned tool accessibility errors; the Georges entry is independently present in BGM's primary bibliography and the Ford record and statement were inspected in the supplied literature consolidation. These are source-access limits, not invented full-proof checks.

A final publisher search also located the Georges Elsevier record and Ford-Fulkerson Cambridge record directly, as linked in REFEREE.md. Their metadata and abstracts were checked, resolving existence independently of the failed DOI resolver opens.

## Limits

COMPUTED results certify the finite domains above. They do not prove the main theorem. The reverse audit in REFEREE.md checks the supplied mathematical route independently of the numerical scripts and the upstream Lean theorem. No new all-order cycle-cover, lattice, complexity, sampler or Pfaffian-proof certification is claimed. No Lean build was repeated. The initial report path `research/2026-11-14_opus_blueprint/BLUEPRINT.md` no longer exists; the maintained document is `proofs/blueprint/BLUEPRINT.md`, and the research folder's REPORT.md confirms that move.
