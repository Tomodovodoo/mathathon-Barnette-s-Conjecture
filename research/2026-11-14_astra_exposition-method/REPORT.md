Traced all 55 runs and retrieved all 2,765 activity items of the floating rewrite thread.
The largest improvements removed unnecessary intermediate obligations before shortening prose.
The strongest writing changes put objectives, definitions and proofs at their point of use.
Produced the requested history, 22-rule guide, three-paper critique and first-principles outline.
Recommend one main proof route, with algorithmic extensions separated and proof-critical invariants retained.

# Report

## Aim and deliverables

I set out to identify how the floating-body rewrite improved exposition and convert that history into a checkable method for Barnette. The required deliverables are `HOW-THE-REWRITE-WORKED.md`, `STYLE-GUIDE.md`, `CRITIQUE-OF-THREE-PAPERS.md`, `OUTLINE-PROPOSAL.md`, and this report. The style guide gives a Barnette example and an acceptance test for every rule. The critique ranks ten concrete edits. The outline starts from degree two plus connectivity and states the reader's question for every section.

Supplementary evidence consists of a complete user-turn index, full conversation messages, the twenty approved before/after comparisons, a source manifest with SHA-256 hashes, an original-PDF text extraction, three inspected source-page renders, and a bounded dependency audit. All files are inside the assigned folder. The floating source tree was read-only. No subagents were started.

## What was established

Documentary finding: the first mathematical simplifications were a fixed-order shape approximation and iteration on nested closed admissible sets with the physical residual. Later, changing the side of Neumann inversion removed a two-index norm. In the expanded theorem, polynomial divisor thresholds permitted finite-order operator reduction. These are attributed historical changes, not independent proofs of their analytic validity here.

Documentary finding: shortening was not monotone. V4 expanded to seven pages because review calculations entered the manuscript; the user rejected this, and the draft returned to six pages with the necessary remainder correction retained. V5 and V6 concern a broader theorem, so their ten- and nine-page counts are not regressions against the four-dimensional six-page draft. Readable figures subsequently justified eleven pages.

Documentary finding: the user repeatedly preferred a named objective before an ansatz or transformation, precise names instead of vague references to bounds, and essential proofs beside their uses. The twenty-edit record gives unusually controlled evidence: the saved comparison reports six statements and 48 displays unchanged while prose and order improved. The title change remained a proposal in a separate file at the end of the thread.

PROVED-HERE: the conditional forest-certificate conversion in `DEPENDENCY-AUDIT.md`. Its exact contract assumes a spanning forest selecting one side per triangular face, and proves that the complementary dual is a Hamiltonian cycle. It does not prove the forest exists.

LIT source routes used for examples: OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, September 24, 2026, especially Lemmas 2.1 and 4.1, Proposition 5.1 and §§6–7; Zhentao Li, *A note on the proof of Barnette's conjecture*, arXiv:2610.30490v1, October 21, 2026, especially Lemma 7, §4 and Appendices A–C. The constructive draft's extra criterion, component and complexity claims remain HUNCH for this report pending independent audit and publication identification. No general theorem is labeled COMPUTED on the strength of an example or a rendered page.

## What failed or remains limited

The history does not justify the claim that all audits endorsed the proof. Audit 3 withdraws an earlier verdict, and Audit 5 rejects proposed shortcuts. Their failed routes are retained in the history. An assistant's report that checks passed is evidence of the workflow, not an independent theorem certificate.

I retrieved the whole thread, including continuations of truncated items, and reviewed all user questions/corrections and the corresponding assistant explanations. The committed archive contains conversational messages, not the entire several-megabyte tool transcript. Tool records were used to locate sources and changes. The 211-entry source manifest is an inventory, not a claim that every saved variant or review was independently verified. Manuscript comparisons concentrate on the original, successive Astra versions, the saved editorial diffs, selected competing drafts and the relevant audits. The same named source file was sometimes replaced during the historical conversation; the position references and preserved snapshots matter more than its current filename alone.

The current `output/` directory yielded no files in the inventory command. I did not manufacture a missing output version. The final proposed abstract and title were distinguished from the canonical source. The source PDFs and primary text dumps supplied the Barnette claims; no external publication history was inferred from the repository brief.

This is not a full reverse-Lamport audit of any of the three Barnette proofs or the floating theorem. The bounded audit validates only the final conversion so that the guide has a concrete example of keeping degree and connectivity obligations separate. The apparent mark-convention ambiguities in Li are questions for a mathematical audit, not asserted counterexamples. PDF page 12's overflowing tuple formulas were visually confirmed, not inferred solely from text extraction.

## Three best next steps

1. Freeze the main contract: an explanation of prescribed-edge existence, or a time-bounded constructive theorem. Use the proposed existence outline unless the algorithmic claim is an explicit objective.
2. Draft the first three sections and the conditional recovery picture. Test whether a reader can explain the incidence-tree target and the second matching before seeing cancellation.
3. Audit the chosen cancellation route and separator gluing with exact invariants and notation types. Then render a before/after comparison of the draft, including figures at their actual reading locations.

## Leads for others

Li's general mark convention deserves an explicit check of order, repetition and invariant cycle selection. The constructive draft's exact black-inner-boundary criterion and component theorem are valuable separate audit targets. Neither should be imported silently into the simpler OpenAI route. A figure specialist could make the disk count and the two reversals much easier to learn than another page of prose.

## Reproduction and validation

Run from the repository root:

```powershell
python research/2026-11-14_astra_exposition-method/inspect_sources.py
```

This records source hashes, runs `pdftotext -layout` on the original floating PDF and extracts the twenty approved edit pairs from their saved JSON. The script reads the external source tree and writes only beside itself. The three PDF inspection images were generated with PyMuPDF at scale 1.4 from zero-based pages 5, 11 and 8 of OpenAI-Barnette.pdf, A-Note-On-Barnette.pdf and barnette_trees.pdf respectively. The exact rendering logic is included in the script.

Thread retrieval used `t3_thread_read`, `view=activity`, `afterPosition=-1`, `limit=100`, `maxCharsPerItem=20000`, then each returned `nextPosition` until `hasMore=false`. Every truncated item's `nextTextOffset` was followed. Result: positions 0–2764 with no remaining truncated item. The conversation JSON retains item IDs, run IDs and positions for checking quotations.

Checks covered required-file presence, valid JSON, complete activity positions, retained user turns, source quotation anchors, and final prose/status review. No source manuscript was edited or recompiled. Git commits were restricted to this folder; push outcome is recorded in the final handoff.
