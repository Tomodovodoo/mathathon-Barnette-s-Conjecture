# Repository hygiene: what I changed and what I found

Survey script: scripts/hygiene.py (read-only), output data/hygiene.json, run from the repository root on 2026-11-14 before the index change below. At that time the tree had 2,246 tracked files, 305 MB.

## 1. Removed from the index (files left on disk)

Commit 670951a. `git rm --cached` only; every file is still in the working tree. The exact list is data/untrack-list.txt.

Python bytecode (15 files):

- research/2026-11-14_fable_digestions/code/__pycache__/dig.cpython-314.pyc
- research/2026-11-14_fable_referee-topology/code/__pycache__/etri.cpython-314.pyc
- research/2026-11-14_fable_referee-topology/code/__pycache__/rainbow.cpython-314.pyc
- research/2026-11-14_fable_route-categorical/code/__pycache__/common.cpython-314.pyc
- research/2026-11-14_fable_route-categorical/code/__pycache__/cuts.cpython-314.pyc
- research/2026-11-14_fable_route-categorical/code/__pycache__/trinity.cpython-314.pyc
- research/2026-11-14_fable_route-combinatorics/lab/__pycache__/analyze.cpython-314.pyc
- research/2026-11-14_fable_route-combinatorics/lab/__pycache__/rooted.cpython-314.pyc
- research/2026-11-14_fable_route-combinatorics/lab/__pycache__/tri.cpython-314.pyc
- research/2026-11-14_opus_blueprint/scripts/__pycache__/curation.cpython-314.pyc
- research/2026-11-14_opus_blueprint/scripts/__pycache__/extract_tex.cpython-314.pyc
- research/2026-11-14_opus_referee-involutions/code/__pycache__/check.cpython-314.pyc
- research/2026-11-14_opus_referee-involutions/code/__pycache__/ref.cpython-314.pyc
- research/2026-11-14_opus_two-tree-packing/code/__pycache__/referee_sol.cpython-314.pyc
- research/2026-11-14_opus_two-tree-packing/code/__pycache__/tp.cpython-314.pyc

LaTeX build logs (3 files; I opened each and it is a pdfTeX transcript):

- research/2026-11-14_astra_primal-proof/latex-build.log
- research/2026-11-14_astra_primal-revision/latex-1.log
- research/2026-11-14_astra_primal-revision/latex-2.log

Also my own 19 page renders under build-primal/renders/ (regenerable by scripts/build_primal.py), which an earlier commit of mine had added by mistake.

New top-level .gitignore: `*.aux *.fls *.fdb_latexmk *.synctex.gz *.toc *.nav *.snm texput.log latex-*.log __pycache__/ *.pyc`.

## 2. Build-pattern files I deliberately left tracked

The pattern scan found 46 tracked files with build extensions. Besides the 18 above:

| Files | Why I left them |
| --- | --- |
| proofs/involutions/involutions.aux, .log, .out | The brief makes proofs/involutions/ read-only while it is under referee. They are pure LaTeX artefacts; recommend untracking once the referee is done (CLEANUP-PROPOSAL.md, item C1). |
| paper/main/barnette.bbl, paper/draft-B/barnette.bbl | paper/ is read-only for me. A .bbl is often kept on purpose for arXiv upload; coordinator's call (C2). |
| 23 other `*.log` and `*.out` files in research folders (census logs, check transcripts, verification logs, Lean `axioms.out`, `defs.out`, `build.log`, `FiniteDifference.out`) | These are computation transcripts and Lean outputs. Several reports cite them as provenance, which the brief requires. They are data, not build artefacts. For the same reason the new .gitignore does not ignore `*.log` or `*.out` globally: doing so would make `git add <folder>` silently skip future census logs. LaTeX folders should ignore their own logs locally, as proofs/primal/.gitignore already does. |

Untracked bytecode still on disk (ignored from now on): four `__pycache__` files in research/2026-11-14_astra_main-revision/independent/ and research/2026-11-14_fable_referee-primal/code/.

## 3. Cloned or vendored sources

None tracked. research/2026-11-14_opus_lean-formalisation/upstream/ (openai/math clone) is ignored by that folder's .gitignore; research/2026-11-14_opus_blueprint/upstream/ is untracked on disk (it should get a .gitignore, item C9); workings/barnette_lab/vendor/ (plantri.c, plantri.exe) is ignored by workings/barnette_lab/.gitignore.

## 4. Research folders without REPORT.md

57 folders under research/. Seven have no REPORT.md at survey time:

| Folder | State on disk | Likely reason |
| --- | --- | --- |
| 2026-11-14_astra_main-revision | nothing tracked | run in progress (revising paper/main/) |
| 2026-11-14_astra_synthesis | nothing tracked; count.py, counts.json, figures.py | in progress or abandoned |
| 2026-11-14_fable_descent | 2 tracked files (code, data) | in progress |
| 2026-11-14_opus_blueprint | 17 tracked files, no report | in progress |
| 2026-11-14_sol_involutions-revision | 19 tracked, has AUDIT.md and CHANGES.md | in progress |
| 2026-11-14_sol_referee-covers | 6 tracked, has two REFEREE files | report not yet written |
| 2026-11-14_opus_cross-audit | this run | REPORT.md added at the end of this run |

research/INDEX.md has no row for 12 folders: astra_induction-lemmas, astra_main-revision, astra_synthesis, fable_coldread-main, fable_descent, opus_blueprint, opus_cross-audit, opus_referee-involutions, sol_involutions-revision, sol_map-update, sol_referee-covers, sol_referee-main. Every INDEX row names an existing folder.

## 5. Relative links

Checked every tracked Markdown file under digestions/ and every tracked README*.md anywhere: 70 files, 111 relative links (http(s), mailto and pure #anchors skipped; fenced code skipped). **No broken link.** The script resolves each target against the linking file's folder and, for a miss, lists files with the same name as candidate fixes; there were none to list.

Limitations: the script checks Markdown `[text](target)` links only. It does not check anchors inside files, bare paths written in backticks (many documents cite paths that way), or links in .tex files.

## 6. Layout

The top-level README describes papers/, digestions/, workings/, proofs/, paper/, skills/. Two tracked top-level folders are outside that layout: research/ (all agent runs, described only in research/BRIEF.md and research/INDEX.md) and labyrinth/ (the exploration map: lab.py, frontier.json, dashboard/). Recommend adding both to the README table (C10).
