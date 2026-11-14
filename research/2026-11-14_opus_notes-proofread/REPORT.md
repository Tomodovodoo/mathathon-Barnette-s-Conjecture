# Report: proofreading the two companion notes

- Both notes (proofs/primal/primal.pdf, proofs/involutions/involutions.pdf) now read as papers. Status tags, agent and folder names, mentions of referees and earlier versions are gone. The internal status line on the primal note's first page is replaced by a statement of what the note proves and how it relates to the main paper.
- No mathematical statement or proof step was changed. I found no mathematical problem (PROBLEMS.md).
- Every main-paper statement number the notes cite matches paper/main/barnette.aux (version 2): Lemma 3.8, Lemma 4.2, Lemmas 4.5 to 4.7, Proposition 4.8, Proposition 5.2, Section 4.
- Both PDFs rebuild with no undefined references and no overfull boxes. Page counts are unchanged (primal 15, involutions 18).
- Four small figure defects are reported, not fixed, because fixing them means redrawing. Also: rerunning the primal note's Markdown build script would overwrite these edits.

## What I set out to do

The brief: make the two refereed companion notes ready for a human reader without touching their mathematics. That meant removing process residue, checking cross-references, captions, notation and references to the main paper, rebuilding the PDFs, and logging every edit.

## What was done

Every edit is in CHANGELOG.md, with old and new text. In summary:

**primal.tex**
- Replaced the status paragraph and the following sentence with one paragraph. It names the theorem (OpenAI, Theorem 1.1 and Corollary 7.1) and the main paper, says the note follows it lemma by lemma in $G$, and gives the two departures with main-paper numbers: the first pair (Proposition 5.2) comes from Li's deficit argument (Lemma 4), and the heights of Section 4 are replaced by flow potentials and a polynomial (Lemmas 6 to 8), which give Proposition 4.8. It also names the Lean commit and the two departures from it, and says the text is not machine-checked.
- Date line: dropped "refereed revision". The empty author line and its comment are unchanged.
- Removed PROVED-HERE, LIT and COMPUTED from all lemma headers, remarks, the sources and the dictionary note. Where a tag carried attribution ("PROVED-HERE, restating Lean's ..."), the attribution stays as a sentence ("This restates Lean's ...").
- Lemma 5 now also says it is the main paper's Lemma 3.8.
- Removed references to research folders (fable, sol, astra), to "the referee's code", to "the first reconstruction", and the sentence about "the adjudication of an earlier claim".
- Section 9: the sentence crediting a research file for the real-sign polynomial now says what the polynomial replaces (OpenAI's exponential sum and complex phases).
- Sources moved after the remarks section (old 10 and 11 swapped), so the text ends with the sources. Added a sources entry for the Lean development, using the title and URL of `OpenAI2026b` in paper/main/refs.bib.
- Captions of Figures 1 to 6 and the dictionary table now set symbols in math mode. Before, they showed "e0", "b0", "Q\_s", "h=7 and ell=2", "G-P" and "i to the power n" as plain text.
- Dictionary: "Good state; good pair" became "Good state and its partner", because the main paper defines good states, not good pairs. "Capped piece" became "piece with its cap", the main paper's words.
- Fixed straight double quotes (two places), the heading "in G", and one unclear sentence in the proof of Lemma 8.

**involutions.tex**
- Rewrote the abstract to say exactly what the note delivers: Theorem 1, the full form of Li's Appendix B argument, the drawing-free Section 5 and its relation to the main paper's Proposition 4.8, the constructor, the separate coefficient check, and the listed example.
- "Contract and notation" became "Setting and notation".
- Removed "Earlier versions of this note said forest pair". Reordered the first paragraph so the main paper is introduced before its Lemma 4.2 is cited, and gave its repository path.
- Added `\cite` to the first mentions of OpenAI, Li and the constructive paper. The bibliography entries were not touched.
- Removed the COMPUTED and PROVED-HERE/LIT tags, "the referee's", "original author's", "revision verifier", "refereed height polynomial", "corrected coefficient", "existing lab", and three research-folder paths. The computational paragraph now speaks of three programs, and points to the README beside the note for code and outputs.
- Section 9: removed "The requested older name example.json is absent. We copy the current input into this folder" and the workings/barnette\_lab path.
- Added in-text references to Figures 1, 2 and 4, which were never cited (only Figure 3 was).

**Checks.** Read every page of both PDFs as rendered PNGs, before and after, with the .tex alongside. pdflatex twice per note (latexmk was not used, since MiKTeX shows its update prompt). Both logs have no `Overfull`, no undefined references and no undefined citations. Before each build I ran `git log -3 -- proofs/`: no other agent had touched either note.

EXAMPLES.md and the "Exact finite range" section of proofs/primal/STATUS.md already say they describe the first version's 20-vertex example, so I left them alone. Page counts did not change, so no README or STATUS edit was needed.

## What failed or was left

- Figure defects (PROBLEMS.md): label overlaps in primal Figures 4 and 8 and involutions Figure 1, and small labels in involutions Figure 3. Fixing them needs a redraw, which this task excludes.
- The `thebibliography` entries inside involutions.tex still say "local source" and "local project source". I left them because another agent is auditing bibliographies.
- The primal note still points readers to STATUS.md and EXAMPLES.md "beside this note". That is fine for a repository companion, but the pointers would need replacing if the note is ever circulated alone.

## Leads for others

- proofs/primal/README.md says research/2026-11-14_astra_primal-revision/build.py regenerates primal.tex from PRIMAL-PROOF.md. Running it would undo this proofread. Whoever owns PRIMAL-PROOF.md should either port these edits or retire the generator.
- proofs/involutions/README.md and proofs/primal/README.md still describe the notes in research-process terms (revision folders, referees). They are repository docs, not the papers, so I left them.

## Three best next steps

1. Redraw primal Figure 4 with flow labels offset from arrow heads and vertices, and move the "cap" label in Figure 8.
2. Port the primal.tex edits back into PRIMAL-PROOF.md, or mark primal.tex as the source in the README.
3. Let the bibliography agent turn the involutions note's `thebibliography` into proper entries (titles, dates, no "local source").
