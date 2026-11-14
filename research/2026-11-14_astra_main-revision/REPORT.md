Version 2 is complete: the main paper is 19 pages, with version 1 preserved in `paper/main/history/`.
All eight mathematical corrections and all forty cold-reader items are resolved in `CHANGES.md`.
PROVED-HERE: the bounded revision audit in `AUDIT.md` returns FOLLOWS for Theorem 1.1.
COMPUTED: example checks, figure checks and the full TeX build pass, with zero warnings, undefined references or overfull boxes.
Every original and final page was rendered and inspected; before/after PNGs are retained in this folder.

## Goal and scope

Finish the main exposition after the independent referee and cold reader, retaining its proof while improving the opening, explanations, notation, figures and placement. Work was confined to this research folder, `paper/main/` and `paper/figures/`. The version-1 backup was committed before edits. No draft, proof, digestion or other agent's folder was edited.

The title is the coordinator's exact title. The author command is empty with the requested single comment. No project status tags or production narrative appear in the paper.

## Results

The first page now contains a six-sentence abstract, the full theorem contract and a five-step causal plan. The full-width overview occupies the top of page 2, with panels in the order of the plan. The body explains why a tree of faces is useful, why `D(r,s)` is introduced and why fixed-second-state cancellation permits a weight.

All 13 figures and both tables are fixed outside statements, proofs, examples and remarks. The disk figure precedes its lemma and proof. The flow figure precedes the pair-existence proposition. The gluing figure follows the cap lemma and precedes the induction theorem. The height picture follows the complete height proof. No figure interrupts a sentence or proof, and no final page has more than about a quarter of its text area unused.

Regenerated the overview, dual overlay, flow network, pair diagram, cancellation close-up, gluing diagram and height path, keeping all existing filenames. Added the eight-pairs/two-groupings diagram and the toolkit export `18-groupings`. State wedges, line patterns and vertex shapes retain their meanings. Labels no longer hide primal vertices or the affected state wedges.

The standalone bibliography is a copy of `papers/barnette.bib`, supplemented by the two still-cited entries missing there and adjusted as recorded in `CHANGES.md`. The paper credits unavailable historical originals through inspected secondary accounts. It distinguishes the older 64-vertex check from the 90-vertex bound, and includes short remarks about the Pfaffian chain, the Lean formalisation and the companion notes. Optional lattice and unreviewed cycle-cover results were omitted for the reasons in the change log.

PROVED-HERE: `AUDIT.md` reconstructs the actual proof route from the main theorem backward, including both induction cases, the shared disk identity, the two different reversals, the weight increment, the minimum-cycle finite difference, the flow inequality and prescribed gluing. It also records the supplied contraction alternative to forest-dual connectivity. No new gap or mathematical regression was found. This audit is by the reviser and does not claim to be a second independent referee report.

COMPUTED: `example.py` reruns the original manuscript checks. The 13-vertex running triangulation has 12 states, eight pairs and six good states; the displayed second signed moment is 18. The cube, hexagonal prism, nine-vertex gluing example and eleven-vertex incidence example agree with the text. `independent/examples.py`, copied from the referee's separate implementation, also checks every table row, both height values, the Laurent coefficients and the 26-vertex connectivity example. Its input triangulations are copied into `independent/`. The 12-vertex census statement in the paper is the supplied referee's previously completed exhaustive result; this revision did not rerun that census.

## Reproduction and files

Run these from the repository root:

```powershell
python paper/figures/build.py
python research/2026-11-14_astra_main-revision/build.py
python research/2026-11-14_astra_main-revision/verify_final.py
python research/2026-11-14_astra_main-revision/render_final.py
```

The first command checks the figure data, generates 18 vector figures and compiles the gallery. The second runs pdflatex, bibtex and two further pdflatex passes. The third records numerical checks, fixed-placement checks, label sizes and exact artifact hashes in `verification.json`. The last renders every final page at 130 dpi and records text extents in `page-metrics.json`.

`before/` contains the 18 original pages at 110 dpi, produced by `render.py`. `after-v2/` contains all 19 final pages and contact sheets. The pagination changes throughout, so the full sets are retained. `proof-comparison.diff` records the complete source comparison. `build.txt`, `example.txt`, `independent-check.txt` and `figure-check.txt` retain the command output.

`review_artifacts.py` produces the source diff and five grey print proofs in `greyscale/`; these were inspected too. Superseded local render sets and one-use edit scripts are ignored by Git.

## What failed and why

`latexmk` cannot run in the installed MiKTeX environment because Perl is missing. The direct pdflatex/bibtex sequence succeeds. No installation or system change was needed.

The cold-reader trial still allowed three float interruptions. Fixed placement resolved them, but initially left excessive blank space before the gluing figure. Moving that figure after the cap proof filled the page while preserving the reading order. A final visual pass found several labels still touching wedges; moving them into white sectors resolved those collisions. The source comparison caught and corrected two stray symbols from a notation rename.

## What is still open

The owner still has to choose the author line; the requested placeholder is in place. There is no remaining implementation blocker for version 2. The paper's open questions and attributed algorithmic claims remain explicitly separate from its proved theorem. The reviser did not audit the unsigned manuscript's enumeration algorithm or rerun the accompanying Lean build.

## Three next steps

1. Choose the author line and release metadata.
2. Ask a reader unfamiliar with the sources to read the revised first two pages and explain the role of each construction.
3. Archive this source/PDF pair with the existing independent referee report and this revision audit when preparing the release.

## Git

The initial preservation commit is `0881bf7`. The main source, PDF, bibliography and figure revision is `8317608`. The final report commit contains only this research folder; the final chat reports its identifier and push outcome.
