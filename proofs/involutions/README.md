# Forest pairs by two involutions

Read involutions.pdf for the complete standalone proof and every marked object of the current running example. INVOLUTIONS.md is a shorter companion. STATUS.md separates source results, completed proofs and computations. The research folder contains the independent verifier, raw census, family measurements, witnesses and reverse-Lamport audit.

Run from the repository root with Python, NetworkX, SymPy, NumPy, SciPy and MiKTeX available:

```powershell
python research/2026-11-14_sol_li-completion/verify.py 14
python research/2026-11-14_sol_li-completion/extras.py
python research/2026-11-14_sol_li-completion/more_checks.py
python research/2026-11-14_sol_li-completion/build.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=proofs/involutions proofs/involutions/involutions.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=proofs/involutions proofs/involutions/involutions.tex
```

extras.py expects the repository's installed workings/barnette_lab/vendor/plantri.exe. It compares complete canonical map sets with the census generator. The verifier itself imports only the census input generator; it implements states, cycles, exact ray intersections, signs, both maps, fixed counts and paths independently of the existing Li implementation.

The figure generator imports paper/figures/model.py and draw.py read-only. Blue arrows, thick marked spokes, white points and root circles use the existing encodings. No file in the shared toolkit is modified. Figure inputs and the example tables are generated under this folder.

To render with PyMuPDF:

```powershell
python -c "import fitz;from pathlib import Path;d=fitz.open('proofs/involutions/involutions.pdf');[p.get_pixmap(matrix=fitz.Matrix(1.15,1.15)).save(Path('proofs/involutions/figures')/('page-%02d.png'%(i+1))) for i,p in enumerate(d)]"
```

The manuscript is amsart on A4 with one-inch margins. Build diagnostics and visual QA are recorded in the research REPORT.md. No polynomial is used in the existence proof or constructor. The separate coefficient comparison explains the relation to the refereed algebraic route.
