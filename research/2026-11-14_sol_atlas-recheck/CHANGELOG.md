# Changelog

2026-11-14, GPT-6.1 Sol. Changes only in the assigned research folder and `digestions/atlas/`.

- `figs_scope.py`, page 24: reduce the ledger's second column from 12.0 to 11.8 cm, eliminating the standalone 3.46451 pt overfull box.
- `pages_more.py`, page 24: name ECCC TR06-015, Hertel and Alt and coauthors, and the unopened original Kelmans paper. Preserve the unrefereed status of the project's translation. Shorten the explanatory text to keep the combined prose/status at 130 words. Add the citation-audit source.
- `figs_scope.py`, page 30: extend the pair-preserving contraction's two-program endpoint from 17 to 19 and state its separator-free hypothesis. Extend the good-state contraction inequality's two-program endpoint from 17 to 18. These corrections follow explicit code and the half-exception implication, detailed in AUDIT.md.
- Page 30: extend sampled pair descent from 150 to 200, rescale the logarithmic axis, name the nonroot degree-four contraction domain, and cite the supporting reports and code. The source entry explicitly excludes capped order-300 starts from successful evidence.
- Pages 26 and 29: no content correction needed. Their counts, class membership, qualifications and review provenance passed the bounded audit.
- `verify.py`: enforce 130 to 150 words and 0.80 to 0.95 figure/text width. Also inspect available standalone figure logs for overfull boxes above 2 pt.
- `pages.py` sources introduction and README: distinguish the earlier whole-atlas review from this bounded repair audit; update the limitations and page metrics.
- Regenerate the atlas, standalone figures 24/30, per-page PDFs, renders and certificates. Even unchanged per-page PDFs get regenerated PDF metadata/resource bytes; no other figure source changed.
- `recheck.py` and `recheck.json`: independent grouping of 34 blueprint IDs, comparison with every status-table row and figure certificate; aggregate reconciliation of saved induction/G data and exact expected chart values.
- `AUDIT.md`, `REPORT.md`: check ledger, bounded dependency argument, verdicts, scope and remaining work. `sources.png` and `title30.png` are visual inspection artifacts generated from the built PDF.

Commands, all from the repository root:

```powershell
python -X utf8 digestions/atlas/build.py
python -X utf8 digestions/atlas/verify.py
python -X utf8 research/2026-11-14_sol_atlas-recheck/recheck.py
```

The final build includes all figures so `computed.json` contains every route certificate. A selective build writes certificates for selected figures only, so the final reconciliation uses the complete build. No underlying graph census was rerun. `build.py` produces the page PNGs at 110 dpi. The source-page contact sheet uses PyMuPDF at 65 dpi and Pillow to place physical PDF pages 31 to 33 side by side; the title crop uses PyMuPDF at 180 dpi over rectangle 65,40,530,75 on physical page 30.

COMPUTED final metrics from `manifest.json` and `audit.json`:

| Page | Words including status | Figure cm | Fraction of text width |
| --- | --- | --- | --- |
| 24 | 130 | 14.57 x 19.50 | 0.915 |
| 26 | 149 | 14.64 x 14.29 | 0.919 |
| 29 | 150 | 14.79 x 17.22 | 0.929 |
| 30 | 149 | 14.07 x 19.48 | 0.884 |

The verifier passes for 30 routes and 34 pages. Main and standalone logs have no remaining overfull box above 2 pt; page 24's old warning is absent. Visual inspection covers 24, 26, 29, 30 and the sources pages. Reports were not treated as human peer review.
