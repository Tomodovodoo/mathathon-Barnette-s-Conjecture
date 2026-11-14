# Citation and library audit

The four manuscripts contain 63 cite commands using 23 distinct keys; none is missing from the library.
The ledger retains 321 citation contexts, including prose references and the atlas sources table.
The main bibliography is an exact 17-entry subset of the 96-entry canonical bibliography; its PDF was rebuilt.
All 50 research PDFs have rights records, totaling 49,808,134 bytes, and all held source PDF hashes are unchanged.
Numbered literature checks passed, but some metadata fields and project-report claims remain unverified; this is not an exhaustive content clearance.

## Assignment and scope

I audited citations in `paper/main/barnette.tex`, `proofs/primal/primal.tex`, `proofs/involutions/involutions.tex`, the newly appearing `proofs/sign-free/sign-free.tex`, the step digestions, synthesis, route-map explanation, and atlas sources table. I read BRIEF.md, README.md and the repository unslop skill. No subagents were used. All source text changes are recommendations in TEXT-FIXES.md.

The sign-free file did not exist at the start. It appeared during the run and was included on the second inventory pass. Its bibliography is inline, so I did not alter it or rebuild its PDF. Neither the primal nor involution note has a separate bibliography file to update.

## What was established

LIT, statement comparison only. OpenAI Theorem 1.1, Proposition 3.1, Lemmas 4.1, 5.2 and 5.3, Sections 5.3 and 6, and Corollaries 7.1 and 7.2 match their uses. Li's numbered definitions, one-mark lemmas, disk count and gluing appendix match. The prose distinguishes the project's complete multi-mark proof from Li's sketch. The unsigned manuscript's title page has no author, and its criterion and algorithm statements are cited without inventing one.

LIT. GSW arXiv v3 Theorems 4.3 and 4.16 match the universal equivalences used. Theorem 4.3 is on PDF page 7 in the held file, correcting the earlier consolidation's page locator. Hertel Corollary 3, Alt Lemma 5 and Stein Theorem 2.2 match. The main paper uses the secondary chain for Kelmans.

LIT. HMM's 64-vertex bound is verified secondarily through Hertel and Bagheri Gh. 2022. BGM's 90-vertex bound is directly in Theorem 4.1(a). Schnieders Corollary 1.13 states the face-size-eight result. Kardos Theorem 1 does not require bipartiteness. The main text does not confuse these statements.

LIT. Rendering the Feder-Subi ECCC scan allowed direct checking of the face-colour claim. Its manuscript is dated 2004 and its report header 2006. The triangle-parity result is Bagheri Gh., Feder, Fleischner and Subi Theorem 11, with additional hypotheses; it is not Feder-Subi's result.

LIT, secondary. The published Alt et al. bibliography, reference 3 on printed p. 364, supports Barnette, "Conjecture 5," Waterloo proceedings p. 343. I changed the canonical note to cite this evidence. I did not obtain or claim to read the original proceedings page.

LIT. KPW's bijection requires incident roots. Hine-Kalman supports the Tutte-state attribution. Juhasz-Kalman-Rasmussen Theorem 1.1 is a hypertree/Floer dictionary, not a Hamiltonicity theorem. Thomason's author-hosted scan was rendered at pp. 261-262; Corollary 1.5 supports the cubic bipartite avoiding-cycle parity consequence. No Thomason citation occurs in the four TeX documents; this was an additional requested attention check.

LIT, secondary for the original theorems. Schrijver course Exercises 10.26 and 10.29 and handbook pp. 1674, 1685-1686 match the sign-free citations. The directed-tree statement reverses arcs. The original Rado, Nash-Williams and Edmonds papers were not opened in full. The sign-free inline bibliography already has Academic Press for Edmonds.

COMPUTED. The upstream Lean checkout HEAD is `4eaee87548250b2682affda7d05d947c05554bae`. The repository citation now pins that full hash. The claimed successful formal build remains secondary to the independent Lean-check report; I did not rerun Lean.

## Library changes and verification

Added missing Georges and Holton-McKay entries and the sign-free inline bibliography sources to the canonical library. Added Schrijver course and Thomason entries. Alias mappings are in papers/README.md. Retained every existing canonical entry. UNUSED-KEYS.md flags lack of explicit TeX citations, not lack of every possible prose use.

COMPUTED. `validate.py` checks that every explicit citation key exists, every key has a current index row, main entries equal the canonical entries byte for byte, all 58 inventoried source PDFs retain their SHA-256 values, and all 50 research PDFs have rights records. VALIDATION.json records counts and the four TeX snapshot hashes.

The PDF build used `pdflatex -interaction=nonstopmode -halt-on-error`, `bibtex`, then two pdflatex passes. Auxiliary files stayed in this research folder's ignored build directory. `TEXINPUTS` put that directory before the working directory so the fresh bibliography was used instead of the old main-directory BBL. Bibliography notes needed TeX-escaped underscores. Final build succeeded without undefined citations or overfull-box warnings; the final bibliography page was rendered and visually checked. Only `paper/main/barnette.pdf` was copied back. No TeX prose or other document PDF was changed by this audit.

## What failed or remains open

The deliverable is not a full independent verification of all 321 contexts. Project-report links, computation ranges, and review-status claims are inventoried, but many only received an existence check. The ledger says so. Those require the documents' owners or a further content audit. Opening a linked file and verifying its mathematical argument are different tasks.

Metadata checking is also incomplete at field level. The current web pass attempted 63 lookups and obtained 49 responses; some publisher pages blocked access, and a successful response without citation fields is not certification. METADATA-AUDIT.md preserves this distinction and links prior publisher/Crossref evidence. Unverified fields were retained rather than replaced with guesses. Original Waterloo wording, several historical originals, and full redistribution permission for most research downloads remain unresolved.

Most arXiv records grant arXiv distribution rights without granting general downstream redistribution. PDF-RIGHTS.md records per-file source and licence evidence, including explicit CC licences when available, and recommends links or owner decisions otherwise. No owner decision was made and no retained file was deleted.

Another active agent committed the modified papers/INDEX.md as commit `e095165` during this run. I did not undo that commit or touch its other paths. The index content is included in validation. The shared repository continued changing while the audit ran; the snapshot hashes delimit this report.

## Reproduction

From the repository root:

```powershell
python research/2026-11-14_astra_citation-audit/inventory.py
python research/2026-11-14_astra_citation-audit/check_web.py
python research/2026-11-14_astra_citation-audit/finalize.py
python research/2026-11-14_astra_citation-audit/rights.py
python research/2026-11-14_astra_citation-audit/validate.py
```

The finalizer changes the authorized bibliography and index files; it is not a read-only check. Build commands are in build-log.json and build-final.json. PDF extraction uses `pdftotext -layout`; images were rendered with PyMuPDF. Downloaded source texts and renderings are ignored to avoid adding unlicensed copies.

## Three next steps

1. Have document owners apply the provenance and decision-problem wording in TEXT-FIXES.md, then recheck citations against any changed theorem numbering.
2. Finish the explicitly unverified project-report contexts and blocked metadata fields. Obtain an authorized copy of Waterloo p. 343 if exact original wording is needed.
3. Ask the repository owner to decide retention of the research downloads using PDF-RIGHTS.md; keep only appropriately licensed canonical copies when preparing a public release.
