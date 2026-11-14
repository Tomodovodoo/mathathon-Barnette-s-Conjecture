# Build draft A

This directory is a historical record. It uses the current shared figures, so rebuilding can change its appearance.

Run from this directory with `pdflatex` and `bibtex` on PATH:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
bibtex barnette
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
```

The output is `barnette.pdf`. The inputs are `barnette.tex`, `refs.bib`, and the committed PDFs in `../figures/`. `latexmk -pdf -interaction=nonstopmode -halt-on-error barnette.tex` is an alternative when Perl is installed and MiKTeX does not stop at its update prompt.
