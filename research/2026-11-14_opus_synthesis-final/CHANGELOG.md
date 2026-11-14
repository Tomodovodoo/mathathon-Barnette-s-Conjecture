# Changelog, synthesis final pass (Opus 5.5, 2026-11-14)

Files changed: `digestions/SYNTHESIS.md`, `digestions/synthesis-figures/products.{pdf,png}` (run-folder count 80 to 88), `digestions/synthesis-figures/README.md` (script paths). `route-outcomes` was regenerated, showed no changed count (246 routes, 77 refuted), and was restored.

Scripts: copies of `opus_reconcile/synthesis-audit/` in `synthesis-audit/` and of the gate `astra_synthesis/audit.py` as `audit.py`, paths only changed, so reruns write here. One fix in `check.py`: with no open run, `inventory.py` writes "Every run folder holds a final report", which the old regex rejected. The gate (3,500 to 5,000 whitespace words, links, tags, dashes) is unchanged.

Length: 5,910 to 4,972 gate words. Cuts, each pointing to FACTS.md, INDEX.md or a report:
- header shortened; "what we added" points to section 3 instead of repeating its four items;
- "what a human should read first" moved into the owner section, item 9, now starting at Section 4 of the paper;
- the object correspondence table in section 4 removed (it is in `fable_dependency-graph/correspondence.md`);
- census sizes in section 7 removed where section 11 repeats them; sharper-descent failures there point to section 5, where the sizes stay;
- section 9's ten lessons cut to the style guide link and the cold-read finding;
- the three dispute paragraphs in section 10 shortened, all numbers kept except the per-instance detail of the 279/213 drawings (roots 4 and 5 swap) and the odd-m side sign;
- "two smaller points" in section 3 removed (cubic-vertex trick and determinant restatement; both in the older-approaches report);
- the Laurent-polynomial remark removed (it is a correction already applied in version 2);
- second links per item removed where the first link reaches the same evidence.
No review status, qualification, counterexample size or housekeeping item was removed.

Corrections: third-party PDFs are 50 files, 50,103,101 bytes (counted here; PDF-RIGHTS.md gives 49,808,134 for the same 50), not 53.

Added: sign-free row in section 2 and section 10; section 12 on the closing runs (sign-free note and its referee, Figure 5 redrawn and not re-reviewed, descent referee, citation audit with the Grünbaum discrepancy, release check with its red gates, paper proofread and the refs.bib divergence, notes proofread with primal.tex as source, atlas repair unaudited, final recheck); literature item 7 on Waterloo and Grünbaum; owner section items 1 to 9 as briefed, keeping the four earlier items.
