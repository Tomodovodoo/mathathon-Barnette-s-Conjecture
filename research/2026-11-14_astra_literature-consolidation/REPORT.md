# Literature consolidation report

Built a canonical index and BibTeX library covering 87 sources.
Added five licensed PDFs in two commits; the three supplied originals remain unchanged.
Checked the drafts' numbered citations and the OpenAI original's external numbered citations; no numbering mismatch found.
Recorded the unresolved Waterloo attribution, source-version cautions and renewed retrieval outcomes.
Most free reading copies lack established redistribution permission, so the index links them instead of duplicating them.

## Scope and result

The task was to consolidate the research agents' literature into papers/, preserving the originals and research folders. I read BRIEF.md, the repository Literature rule and the unslop skill. All changes are confined to papers/ and this research folder.

Deliverables are papers/INDEX.md, papers/barnette.bib, papers/README.md, papers/2026/README.md, the held PDFs, MISMATCHES.md, manifest.csv and manifest.json. The index includes full citations, identifiers, access limits, project uses, dependencies and verification scope. `catalog.json` retains provenance fields. KEY-MAP.md maps old keys to canonical keys. SELECTION.md explains exclusions.

The held PDFs total 4,254,866 bytes, about 4.1 MiB, including the originals. No size-driven exclusion was necessary. Selection instead removes peripheral commentary, unaccepted proof claims and duplicate versions from the central catalogue. Their original research files remain untouched.

## What was established

`LIT` statement comparisons are recorded individually in MISMATCHES.md. Stein Theorem 2.2, Alt Lemma 5, OpenAI Proposition 3.1 and Lemma 4.1 have the cited numbers and hypotheses. Further checks cover positive circulation, recovery, Li's gluing, GSW's universal equivalences, Schnieders, Kenyon's double-dimer expansion and KPW's root convention. These are statement checks, not independent proof certifications.

Metadata checks use publisher/arXiv records, downloaded title pages and the prior agents' explicit inspection notes. `metadata-checks.json` records success and failure. `extra-metadata.json` records targeted searches; wrong search hits were rejected rather than imported. Diacritics were restored for Kálmán, Tóthmérész, Juhász, Lovász, Lindström and other names. Unverified fields remain omitted. This is not a claim that every historical source was obtained: some metadata still rests on the named secondary bibliography.

The library keeps GSW arXiv v3. Stein and Hine–Kálmán duplicate candidates were recognized by bibliographic identity, independently of byte equality. Kálmán–Tóthmérész uses the licensed journal version. No PDF is copied twice in papers/.

## What failed and why

RETRIEVAL.md lists each renewed attempt. Several originals remain inaccessible; AMS returned 403, some requests timed out, and PMC returned an HTML challenge instead of a PDF. A free author-hosted scan was not treated as blanket redistribution permission. Most arXiv copies use the arXiv-only licence. This is why the central library holds fewer PDFs than the research inventories, while retaining their citations and reading URLs.

The original Waterloo page remains unavailable. Drafts A and B disagree about the credited author and title. Neither variant was silently promoted to verified metadata. KPW's publisher page has a 1999 date but a 2000 issue and PDF heading; the bibliography keeps 2000. Berman's publisher title typo is noted. Missing metadata for older books and chapters was not guessed.

## Reproduction and validation

Run from the repository root:

```
python research/2026-11-14_astra_literature-consolidation/prepare.py
python research/2026-11-14_astra_literature-consolidation/retry.py
python research/2026-11-14_astra_literature-consolidation/enrich.py
python research/2026-11-14_astra_literature-consolidation/curate.py
python research/2026-11-14_astra_literature-consolidation/validate.py
```

The first three scripts acquire evidence, with network results that can change. They are not a substitute for reviewing the resulting records. `curate.py` reproduces the catalogue from the recorded evidence. `validate.py` checks key uniqueness, coverage, hashes, file sizes, duplicate held PDFs, preservation of the originals and bibliography fields.

PDF text extraction uses `pdftotext -layout INPUT.pdf OUTPUT.txt`. The visual checks used `pdftoppm -f N -l N -scale-to 1400 -png -singlefile INPUT.pdf OUTPUT_PREFIX`, with Stein scan page 3, Alt page 3, OpenAI page 5 and Ford page 2. Scratch text, downloaded PDFs, metadata bodies and renders are ignored by git. No mathematical experiment was run.

## Three next steps

1. Obtain an authorized scan of Waterloo p. 343 and resolve the attribution before changing either draft's historical citation.
2. Apply KEY-MAP.md to both draft bibliographies and citation commands together; split the HMM 64 and BGM 90 attribution in draft B.
3. Obtain explicit redistribution permission or licensed journal copies for the central URL-only sources, especially Stein, Alt, Hine–Kálmán and KPW. Preserve theorem numbering when adding them.

## Leads for the coordinator

The renewed search found Ford–Fulkerson, Felsner and Akiyama–Nishizeki–Saito in full, correcting earlier "not obtained" reports. See RETRIEVAL.md before repeating those searches. GSW's existing proof-typo audit remains in the Pfaffian route folder.

Commits and final validation results are recorded in VALIDATION.md. The final push is attempted only after committing the owned paths, as required by BRIEF.md.
