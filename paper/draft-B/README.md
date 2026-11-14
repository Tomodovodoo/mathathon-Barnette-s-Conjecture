# Build draft B

This directory is a historical record. It uses shared figures and local TikZ figure sources, so rebuilding against newer shared figures can change its appearance.

Run from this directory with `pdflatex` and `bibtex` on PATH:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
bibtex barnette
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
```

The output is `barnette.pdf`. The inputs are `barnette.tex`, `refs.bib`, `figures/`, and the committed PDFs in `../figures/`. `latexmk -pdf -interaction=nonstopmode -halt-on-error barnette.tex` is an alternative when MiKTeX does not stop at its update prompt.
