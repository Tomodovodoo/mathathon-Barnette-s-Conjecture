# Mathathon project report

Read [report.pdf](report.pdf). The four-page report covers our goals, proof simplifications, attempted routes, visual explanations, checks and AI use.

[report.tex](report.tex) is the complete editable source, including the bibliography. The mathematical exposition is separate: [barnette.pdf](../paper/barnette.pdf).

## Build

From the repository root, run:

```powershell
python submission/build_report.py
```

The script runs `pdflatex` three times. A TeX installation with the packages listed in `report.tex` is required. To compile without Python, run `pdflatex -interaction=nonstopmode -halt-on-error report.tex` three times from this folder.

The source needs no external images, bibliography files or other project files. Build logs, temporary files and superseded drafts stay out of Git.
