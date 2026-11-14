# Building the primal note

The entry point is primal.pdf, built from primal.tex, which is now the source: it was proofread by hand after generation, so do not regenerate it from PRIMAL-PROOF.md with the revision folder's build.py (that would overwrite the edits). PRIMAL-PROOF.md is the earlier Markdown form of the same proof. The PDF has the proof, followed by the one-page DICTIONARY.md table and eight computed figures. EXAMPLES.md retains the first version's exact cube and 20-vertex data. The illustrated running example instead has 13 faces and 22 vertices.

From the repository root, with Python, MiKTeX, NetworkX, NumPy, SciPy, PyMuPDF and Pillow installed:

```powershell
python proofs/primal/figures/check.py --build
cd proofs/primal
pdflatex -interaction=nonstopmode -halt-on-error primal.tex
pdflatex -interaction=nonstopmode -halt-on-error primal.tex
```

The first command computes and asserts the drawn objects, writes TikZ sources and checked.json, builds each standalone PDF, and renders each PNG. It imports paper/figures/model.py, check.py and draw.py read-only. The current shared inputs are running.json and layout-running.json, formerly called example.json and layout.json. All writes stay in proofs/primal/figures/.

The direct TeX commands build the committed edition. The historical `research/2026-11-14_astra_primal-revision/build.py` regenerates primal.tex from Markdown and also renders the pages, but it predates later source edits: it restores an old author line and moves the worked-example paragraph. Do not use it to reproduce the committed edition. Panels occupy 0.48 textwidth each, at native TikZ scale; labels use footnotesize without image rescaling. Black/white dots, solid blue and outlined vermilion state incidences, dashed vermilion Q, bold black matching and purple cycle follow the shared encodings. Incidence segments replace dual-triangle wedges because these figures display G itself.

To reproduce the extended cancellation and phase-normalization checks:

Return to the repository root before running these commands.

```powershell
python research/2026-11-14_astra_primal-revision/check_cancellation.py 15
python research/2026-11-14_astra_primal-revision/check_cancellation.py 16
python research/2026-11-14_astra_primal-revision/inspect_figures.py
```

The last command also checks all 22 roots of the running example and makes review contact sheets. The dedicated checker uses the independent referee's graph and rotation routines read-only. It targets Lemma 7 and phase normalization; it does not rerun the expensive all-bonds census. Counts and scope are in STATUS.md and the revision REPORT.md.

Do not rerun revise.py as a build step: it records the initial editorial patch and predates the subsequent phase correction. No Lean build is claimed. The independent referee reviewed the first version; the corrected version has the author's reverse-Lamport audit in the revision folder.
