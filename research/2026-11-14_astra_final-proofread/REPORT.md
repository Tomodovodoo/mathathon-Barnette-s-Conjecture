Reviewed all 20 rendered pages and the full TeX source without changing the manuscript.
Found no new proof gap or incorrect running-example number.
Recorded seven should-fix source edits with unique exact old/new strings.
Flagged internal bibliography verification notes as must-fix publication residue.
Saved 20 page PNGs totalling 1.61 MB, computations, source snapshot and review reports.

# Report

## Assignment

Give the final exposition a fresh line-by-line mathematical and copy-editing proofread, including the rendered pages, references, notation, figures, source statement numbers, example arithmetic, late closing material and final-page layout. Work only in research/2026-11-14_astra_final-proofread, following research/BRIEF.md and skills/unslop/SKILL.md. The PDF review skill was also read and applied to the visual inspection.

## Established

The detailed record is PROOFREAD.md. EDITS.md contains seven should-fix unique-string source patches. No must-fix change to the mathematical proof was found. The must-fix bibliography finding belongs to refs.bib and is explicitly separated from the TeX patches so the concurrently working bibliography agent can resolve it.

COMPUTED. check.py checks every state and ordered pair of the rooted running.json example and enumerates perfect matchings of its dual to count the edge-avoiding Hamiltonian cycles. It confirms 12 states, 8 pairs, 6 good states, 6 such cycles, the displayed components, disk counts, all Table 2 weights, and signed moments 0,0,18. checks.json contains the results and command. All 144 ref/eqref occurrences resolve to 49 distinct labels. Semantic uses were read against their targets.

LIT. The requested OpenAI statement references, Li section references and constructive manuscript Theorem 1.2 agree with the texts in papers/text. PROOFREAD.md records precise source locations. The Lean paragraph agrees with the restricted scope described in proofs/lean/README.md; no fresh Lean build is claimed.

All 20 pages were rendered and visually inspected. No clipping, overfull line, isolated heading or broken figure was found. Figure 7 is cited a page too late. A caption could distinguish deleting the outer leaf from suppressing the degree-two black nodes. British spelling is consistent. The bibliography has internal verification prose, including a local review-report path, and should be cleaned before publication.

## What failed and why

The first version of the numerical checker tested acyclicity alone when counting good states. That fails to enforce root separation for states without partners. The checker was corrected to use the paper's full definition; the final run passes. This was a reviewer-code error, not a paper error.

One exploratory PowerShell search used unsupported brace syntax and one diagnostic command had incorrect nested quoting. Both were replaced with direct commands. Neither changed project sources.

No manuscript rebuild or layout experiment was performed because this assignment is report-only and another agent owns the bibliography rebuild. Consequently a 19-page layout is not certified. The inspected last page contains roughly half a page of references, too much to remove with a token prose cut. A specific optional clearpage before the bibliography gives the references a clean start on page 20; reassess after the bibliography cleanup first.

## Still open

Apply or reject the source edits, rebuild after the bibliography changes, and inspect the final pagination. This review covers the hashes in manifest.json, not any later rebuild. The underlying Lean compilation, all historical bibliographic metadata, and the census through 12 vertices were not independently rerun. The task asked for a sample recomputation of the example; the script does not purport to prove universal claims by computation.

## Three best next steps

1. Apply S1–S7 from EDITS.md, treating S4 and S5 as a coupled correction.
2. Remove publication-facing internal bibliography verification notes while retaining the evidence in the citation audit.
3. Rebuild once both edit sets are complete and check Figures 5 and 7, the closing section, and the reference-page break.

## Artifacts and reproduction

- PROOFREAD.md: findings, source comparisons, computations and the page-by-page visual log.
- EDITS.md and edits.json: exact, unique source replacements.
- source.tex and manifest.json: reviewed source and PDF hashes.
- renders/page-01.png through page-20.png: all pages, 1,610,271 bytes total.
- render.py: `python research/2026-11-14_astra_final-proofread/render.py`, generates renders, manifest, source snapshot and pdf-text.txt. It reads the live paper, so rerunning after publication changes creates a new review snapshot.
- check.py: `python research/2026-11-14_astra_final-proofread/check.py`, generates checks.json and crossrefs.txt from running.json and the saved source.
- write_edits.py: `python research/2026-11-14_astra_final-proofread/write_edits.py`, validates unique old strings and generates EDITS.md and edits.json.

## Git and ownership

Only this research folder was staged and committed. The first stable checkpoint was commit 7d2e439, with the source snapshot and page renders, and origin main was pushed successfully. The final reports and checks are committed in a second checkpoint. No other agent's work was staged, amended, reverted or rebuilt.

## Leads for others

The bibliography residue overlaps the active bibliography task. Please use the finding against the finished bibliography rather than restoring or retaining outdated notes from this snapshot. No further research lead was needed for this bounded proofread.
