# Final recheck

COMPUTED. Snapshot `286bcdc02748421933c7cd001c88aa4b89f4ab3e`, fetched from origin/main and checked out detached in `E:/rc-sol-late`. This is a build and finite-test check, not a mathematical proof audit.

The clone retained plantri/vendor inputs from the earlier release check. Tracked inputs were restored to origin/main before checkout; the first checkout attempt failed because the worktree restoration had not updated the index. Restoring both index and worktree resolved it. The old untracked release_verify_6_12.json was not used. Setup_plantri ran again successfully. Dependencies are those pinned in requirements.txt.

## Results

- GREEN: main, primal, involution and sign-free direct builds passed, at 20, 15, 18 and 11 pages. Each matches the committed PDF's extracted text exactly before the mechanical fixes. Main used pdflatex, bibtex, then two pdflatex passes; the inline-bibliography notes used three pdflatex passes.
- GREEN: no errors, undefined citations/references or overfull boxes above 2pt in the four final document logs, including the corrected involution build.
- GREEN: extracted main bibliography contains none of `content checked`, `not opened`, `research/`, `Wikipedia`.
- GREEN: atlas full rebuild with all figure PDFs removed first, and verify.py; primal figure check with --build; sign-free figure check; paper figure check; plantri setup; quick lab tests; Labyrinth check; route-map regeneration.
- GREEN: route-map PDF text and pixels match; SVGs match after date/ID normalization. Raw diff is logs/22.txt. No route-map edits were copied back.
- GREEN: requested Markdown link scopes have zero broken links. At the snapshot, no research folders lack REPORT.md and none are missing from INDEX. This new report folder postdates that snapshot and is deliberately not added to the protected index.
- GREEN: citation validator passes after ignoring note/annote fields. The comparison preserves all remaining entry bytes. Ran in the disposable clone so its generated validation and metadata reports did not alter the other agent's folder in the shared tree.
- GREEN: inline OAI and trees references confidently match canonical OpenAI2026 and Anonymous2026. Full publication identification replaces local-source wording; the unsigned manuscript has no public URL in the canonical entry. Corrected PDF is still 18 pages.
- RED/nonblocking: atlas standalone figure diagnostics are listed in logs/atlas-warnings.json. No protected figure was changed.
- An initial sign-free check invocation from the root failed on figdata.json. The documented figure-directory invocation passed; both logs are retained.

## Reproduction and command ledger

Run `python -B research/2026-11-14_astra_final-recheck/run.py` from the shared repository root after preparing the pinned disposable clone. Then run `check_fixes.py` after applying the two source fixes, followed by `diagnostics.py` and `report.py`. The scripts use one child process at a time, each with a 540-second timeout. `fixes.py` records the source transformations and should not be rerun blindly because its README append is not idempotent.

Preparation commands, in E:/rc-sol-late: `git fetch origin`; `git restore --source=origin/main --worktree -- .`; failed `git checkout --detach origin/main`; `git restore --source=origin/main --staged --worktree -- .`; successful `git checkout --detach origin/main`; `git rev-parse HEAD`.

| Directory | Command | Exit | Seconds | Log |
|---|---|---:|---:|---|
| paper/main | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` | 0 | 1.55 | logs/00.txt |
| paper/main | `bibtex barnette` | 0 | 0.27 | logs/01.txt |
| paper/main | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` | 0 | 1.49 | logs/02.txt |
| paper/main | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` | 0 | 1.56 | logs/03.txt |
| proofs/primal | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` | 0 | 3.43 | logs/04.txt |
| proofs/primal | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` | 0 | 3.35 | logs/05.txt |
| proofs/primal | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` | 0 | 3.36 | logs/06.txt |
| proofs/involutions | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` | 0 | 1.7 | logs/07.txt |
| proofs/involutions | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` | 0 | 1.7 | logs/08.txt |
| proofs/involutions | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` | 0 | 1.59 | logs/09.txt |
| proofs/sign-free | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` | 0 | 3.63 | logs/10.txt |
| proofs/sign-free | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` | 0 | 3.51 | logs/11.txt |
| proofs/sign-free | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` | 0 | 3.62 | logs/12.txt |
| . | `python -B digestions/atlas/build.py` | 0 | 61.65 | logs/13.txt |
| . | `python -B digestions/atlas/verify.py` | 0 | 11.49 | logs/14.txt |
| . | `python -B proofs/primal/figures/check.py --build` | 0 | 28.41 | logs/15.txt |
| . | `python -B proofs/sign-free/figures/check.py` | 1 | 0.1 | logs/16.txt |
| . | `python -B paper/figures/check.py` | 0 | 3.03 | logs/17.txt |
| . | `python -B workings/barnette_lab/setup_plantri.py` | 0 | 7.54 | logs/18.txt |
| . | `python -B workings/barnette_lab/run_tests.py quick` | 0 | 19.74 | logs/19.txt |
| . | `python -B labyrinth/lab.py check` | 0 | 0.07 | logs/20.txt |
| . | `python -B digestions/route-map/build_map.py` | 0 | 11.05 | logs/21.txt |
| . | `git diff -- digestions/route-map` | 0 | 1.01 | logs/22.txt |
| . | `python -B E:\rc-sol-late\research\2026-11-14_sol_release-check\scan.py E:\rc-sol-late E:\Personal\Math\mathathon\barnette-s-conjecture\research\2026-11-14_astra_final-recheck\logs` | 0 | 20.37 | logs/23.txt |
| . | `python -B E:\rc-sol-late\research\2026-11-14_sol_release-check\route_compare.py E:\rc-sol-late E:\Personal\Math\mathathon\barnette-s-conjecture\research\2026-11-14_astra_final-recheck\logs` | 0 | 0.83 | logs/24.txt |
| proofs/sign-free/figures | `python -B check.py` | 0 | 0.26 | logs/fix-0.txt |
| . | `python -B research/2026-11-14_astra_citation-audit/validate.py` | 0 | 0.15 | logs/fix-1.txt |
| proofs/involutions | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` | 0 | 1.59 | logs/fix-2.txt |
| proofs/involutions | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` | 0 | 1.59 | logs/fix-3.txt |
| proofs/involutions | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` | 0 | 1.62 | logs/fix-4.txt |
