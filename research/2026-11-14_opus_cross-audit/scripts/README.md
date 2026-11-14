# Scripts

All are plain Python 3.14 with the standard library, except build_primal.py (needs MiKTeX, PyMuPDF and Pillow).

| Script | Run from | Command | Output | What it checks |
| --- | --- | --- | --- | --- |
| phase_ratio.py | this folder | `python -I scripts/phase_ratio.py data/plantri-b-{6,8,9,10,11,12,13,14}.txt ../../paper/figures/running.json > data/phase_ratio.json`; same with `data/plantri-b-15.txt data/plantri-b-16.txt > data/phase_ratio_15_16.json` | data/phase_ratio*.json | Real sign versus Lean phase for every pair (ADJUDICATION.md). Asserts; a failure stops the run. |
| recount.py | this folder | `python -I scripts/recount.py > data/recount.json` | data/recount.json | Running-example and hexagonal-prism counts (CONSISTENCY.md, Section 3). |
| terms.py | repository root | `python research/2026-11-14_opus_cross-audit/scripts/terms.py > research/2026-11-14_opus_cross-audit/data/terms.txt` | data/terms.txt | Term counts and defining contexts per document. Set `PYTHONIOENCODING=utf-8` on Windows if the console rejects Greek letters. |
| hygiene.py | repository root | `python research/2026-11-14_opus_cross-audit/scripts/hygiene.py > research/2026-11-14_opus_cross-audit/data/hygiene.json` | data/hygiene.json | Tracked build artefacts, large and duplicate files, missing reports, broken Markdown links. Read-only. |
| build_primal.py | repository root | `python research/2026-11-14_opus_cross-audit/scripts/build_primal.py` | proofs/primal/primal.tex, primal.pdf; logs and renders in build-primal/ (ignored) | Copy of the revision's build.py with its logs redirected here. |

Inputs data/plantri-b-V.txt were produced by `workings/barnette_lab/vendor/plantri.exe -b -a V` (V = 6, 8, ..., 16; plantri prints nothing for V = 7). data/untrack-list.txt is the exact list of files removed from the index in commit 670951a.
