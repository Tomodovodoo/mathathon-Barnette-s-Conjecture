# Reproduction commands and output provenance

Run Python commands from the repository root. All runs completed under ten minutes; only one heavy process ran at a time.

| Command | Outputs in this folder |
| --- | --- |
| `python research/2026-11-14_sol_involutions-revision/code/check.py 14` | verification.json, verification-log.txt; all-root ray and two face-tree checks |
| `python research/2026-11-14_sol_involutions-revision/code/referee_rerun.py` | referee-rerun.json, referee-log.txt; all-root referee geometry and full checker |
| `python research/2026-11-14_sol_involutions-revision/code/drawings.py` | drawing-census.json, drawings-log.txt; referee's 69-drawing experiment rerun |
| `python research/2026-11-14_sol_involutions-revision/code/table_check.py` | table-check.json, table-log.txt; independent complete listing comparison |
| `python research/2026-11-14_sol_involutions-revision/code/legacy_checks.py` | census.json, plantri-crosscheck.json, witnesses.json, families.json, polynomial-comparison.json, nonseparating-witness.json, legacy-log.txt; unchanged legacy checks redirected here |
| `python research/2026-11-14_sol_involutions-revision/code/signs.py` | signs.json; octahedron and local/integer sign identities |
| `python research/2026-11-14_sol_involutions-revision/code/figures.py` | figure-data.json and owned TeX figure files; original picture geometry read from commit 55e60f9 |
| `python research/2026-11-14_sol_involutions-revision/code/summary.py` | summary.json and contact-0.png through contact-4.png |

For console logs the commands were followed by `> research/2026-11-14_sol_involutions-revision/<log-name> 2>&1`.

From proofs/involutions/, run twice:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error involutions.tex
```

This creates the final involutions.pdf and its tracked log/aux/out files. Then:

```powershell
pdftoppm -scale-to 1300 -png involutions.pdf ../../research/2026-11-14_sol_involutions-revision/page
```

This creates page-01.png through page-17.png. pdf-qa.json records the final PDF hash, page size, final log checks and inspection result. It was made by parsing involutions.log for leading `!`, `undefined` and `Overfull`, using PyMuPDF for page dimensions and SHA-256 for the final PDF. The full log is proofs/involutions/involutions.log. The contact sheets and individual page renders are retained as visual verification evidence.

edit.py, text.py and companions.py are one-time migration records, not idempotent maintenance commands. The other scripts can be rerun. The table/drawing wrapper outputs may retain the original referee command in a nested metadata field; the actual rerun command is recorded here. No source in another research folder is changed by these wrappers.
