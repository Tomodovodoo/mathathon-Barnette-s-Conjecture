# Validation

- 87 catalogue records and unique BibTeX keys; exact coverage.
- 8 held PDFs; all headers, hashes and sizes match.
- No duplicate SHA-256 among held PDFs.
- All three original PDFs match the committed originals byte for byte.
- Every row has a project use, dependency and verification field.
- Rejected metadata search hits were not imported.
- Total held PDF bytes: 4,254,866.

Command: `python research/2026-11-14_astra_literature-consolidation/validate.py`.
This checks library consistency, not mathematical correctness or completeness of historical metadata.

BibTeX 0.99e parsed all 87 entries using plain.bst. One warning remains: publisher omitted in Lovasz1982 because it was not verified. No syntax errors. 52 candidate PDFs have SHA-256 records in candidate-audit.csv.

Binary batch commits: 7d25c85 and bd7eea9.

Catalogue commit: 13a7402. Required push to origin/main succeeded.
