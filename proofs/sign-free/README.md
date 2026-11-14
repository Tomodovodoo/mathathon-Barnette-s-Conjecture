# Good states without signs

The project's fourth proof note. Read `sign-free.pdf` (11 pages, five computed figures). It contains complete proofs of everything about the good-pair lemma that is proved with no signed count, and says where that approach stops: one conjecture (Step X), a 16-vertex cover with no good state, and the stronger forms that fail.

| File | What |
| --- | --- |
| `sign-free.tex`, `sign-free.pdf` | the note (amsart, A4, one-inch margins) |
| `SIGN-FREE.md` | the same text in Markdown, generated from the tex |
| `STATUS.md` | every statement with its tag, author, checker and verified range |
| `refs.bib` | the nine references (the tex carries them inline) |
| `barnette-figs.sty` | the paper's figure style, copied from `paper/figures/` with two arrow styles added |
| `figures/sf.py` | the graph objects, written for this note |
| `figures/make_figs.py` | computes and draws the five figures, writes `fig-*.tex` and `figdata.json` |
| `figures/check.py` | asserts 76 facts from `figdata.json`: 61 shown in the figures and captions, 15 about the two layouts and the labels; output in `figures/check-output.txt` |
| `figures/running.json`, `layout-running.json` | the paper's example and its layout, copied from `paper/figures/` |

## Build

From `proofs/sign-free/figures/` (Python 3.14, no packages; the 16-vertex figure calls `workings/barnette_lab/vendor/plantri.exe`):

```
python make_figs.py
python check.py
```

From `proofs/sign-free/`:

```
pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex
pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex
```

The second run of the last build is logged in `build-output.txt`: no errors, no undefined references, no overfull boxes. The bibliography is inline, so there is no bibtex run. LaTeX build files are ignored by the local `.gitignore`.

Figure 5 is drawn from a planar straight-line layout computed in `make_figs.py` (Tutte's barycentric embedding, then a repulsion step that keeps every face's orientation). Labels in all five figures are placed by a search that keeps each label box clear of every drawn object. Figures 1 to 4 use the paper's layout of the example, in which the three faces next to `t0` are folded outwards and the sides of `t0` cross ten inner edges; `check.py` records this. Figures are `[H]` floats placed between paragraphs, none inside a statement or proof.

## Verification

From `research/2026-11-14_fable_sign-free-note/code/`:

```
python verify.py 6 12 ../data/verify_6_12.json      # about 70 s
python tex2md.py ../../../proofs/sign-free/sign-free.tex ../../../proofs/sign-free/SIGN-FREE.md
```

`verify.py` tests every statement of Sections 2 to 6, and Conjecture 7.2, on all 262 rooted instances with at most 12 vertices. Page renders, the audit and the report are in the same research folder.
