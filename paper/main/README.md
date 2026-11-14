# Build the exposition

Run from this directory with MiKTeX or another TeX distribution on PATH:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error barnette.tex
```

If `latexmk` cannot find Perl or stops at a MiKTeX update prompt, use the underlying tools directly:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
bibtex barnette
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
pdflatex -interaction=nonstopmode -halt-on-error barnette.tex
```

The output is `barnette.pdf`. Source bibliography: `refs.bib`. Figures are committed in `../figures/`; rebuilding the paper does not require regenerating them. To rebuild the figure sources and PDFs, follow [the figure toolkit README](../figures/README.md) from the repository root. The tested Python packages are listed in [requirements.txt](../../requirements.txt).

`history/barnette-v1.tex` is a historical source snapshot, not a separate build directory. It expects the main directory's bibliography and the shared figure paths.
