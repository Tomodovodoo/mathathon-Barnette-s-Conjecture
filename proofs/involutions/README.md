# Good pairs by two involutions

Read involutions.pdf for the complete note, its drawing-free version, four computed figures and the complete 279-object ray listing. INVOLUTIONS.md is the companion proof; STATUS.md records provenance.

The revision records, code, raw verification outputs, page renders and reverse-Lamport audit are in research/2026-11-14_sol_involutions-revision/. The second referee's report on the drawing-free section, its change log and its independent code are in research/2026-11-14_fable_referee-involutions-v2/. The original census and hard-family evidence remain in research/2026-11-14_sol_li-completion/; the independent referee is research/2026-11-14_opus_referee-involutions/.

From the repository root:

```powershell
python research/2026-11-14_sol_involutions-revision/code/check.py 14
python research/2026-11-14_sol_involutions-revision/code/referee_rerun.py
python research/2026-11-14_sol_involutions-revision/code/drawings.py
```

Build from proofs/involutions/ with `latexmk -pdf -interaction=nonstopmode -halt-on-error involutions.tex`. figures/second.tex is written by research/2026-11-14_fable_referee-involutions-v2/code/figure2.py. Render from there with `pdftoppm -scale-to 1300 -png involutions.pdf ../../research/2026-11-14_sol_involutions-revision/page`. Python uses NetworkX, SymPy, and Pillow; plantri.exe is the existing census generator. The figure script reads the original figure sources from commit 55e60f9 and only writes the owned paths. The common figure style is imported read-only.

If MiKTeX cannot find Perl or stops at its update check, run these commands from `proofs/involutions/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error involutions.tex
pdflatex -interaction=nonstopmode -halt-on-error involutions.tex
```

Use the committed `figures/*.tex` to reproduce this edition. The historical `research/2026-11-14_sol_involutions-revision/code/figures.py` predates the final figure edits: it overwrites captions and removes the `fig:paths` label. It is an editorial record, not a current build step. The later `figure2.py` rebuilds the second drawing only and does not repair that caption file.

The note uses amsart, A4 paper and one-inch margins. No float occurs within a statement or proof. The coefficient comparison is separate from the good-pair proof.
