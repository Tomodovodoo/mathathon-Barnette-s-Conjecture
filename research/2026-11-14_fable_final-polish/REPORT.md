# Report: final polish of the three written proofs

**Summary.**
1. All six items on the main paper are done. It builds clean with `latexmk` and now has 20 pages, one more than before, because the closing section grew by about fifteen lines.
2. The label defect was not confined to Figure 2. Five more figures had it, so vertex labels are now placed by computation in every figure, and `draw.py` fails if a label comes nearer than 0.5pt to a drawn object.
3. Figure 12 is redrawn in four columns from a flow that `check.py` now builds and asserts (value 20, maximum flow, tight cut at `S = {2}`).
4. The independent Lean check finished and confirms, with three corrections to wording. The paper's new Lean paragraph follows the corrected wording.
5. Both companion notes carry the project's names (good pair, cover, `m`, marked versus selected), a sentence on their relation to the main paper, and keep their page counts (18 and 15). No mathematics changed anywhere.

Claude Fable 5.2, 14 November 2026. Folder `research/2026-11-14_fable_final-polish/`. No subagents. Every edit is listed in CHANGELOG.md.

## What I set out to do

Close the last known items on `paper/main/barnette.pdf`, `proofs/primal/primal.pdf` and `proofs/involutions/involutions.pdf` without changing a statement or a proof step: the three items the cold reader left for a human editor, the two long connectivity checks, a typographic pass, an accurate sentence on formal verification, and the naming edits the consistency audit had proposed for the two notes.

## What I established

COMPUTED (`python paper/figures/build.py`, which runs `check.py`, `draw.py`, all eighteen figures, the gallery and `audit.py`): every assertion passes, including the new ones.

- New record `flow` in `check.running()`. The displayed pair `(beta, alpha)` gives an integral flow that respects every capacity, is conserved at every vertex and triangle, and has value `2|X| = 20`. NetworkX's maximum flow is 20. The cut with source side `{source, 2}` has capacity `2(n - 1) + 2 = 20`. The 5 incidences without flow are listed (25 incidences between `A` and `X`, of which 20 are used). In the folded row order every used incidence joins equal or neighbouring rows and the used incidences cross 8 times.
- `label-placement.json`: 129 placed vertex labels in the eighteen figures, root labels aside. All are at least 0.5pt from every registered object, and all but four at least 0.95pt. The registry holds line widths and marker radii entered by hand from the style file, so this checks the stated geometry, not the pixels.

COMPUTED (`latexmk -pdf -interaction=nonstopmode -halt-on-error`, and `pdflatex` three times for the primal note): the three documents build with no error, no undefined or multiply defined reference and no overfull box. The main paper has one underfull box, badness 1694, in the narrow caption of Figure 7. Page counts: 20, 15, 18.

Visual inspection, which is a judgement and not a computation: every figure used in the main paper at 200 dpi after the rebuild; all 20 pages of the main paper; the pages of both notes that changed, and contact sheets of the rest.

LIT, read and followed for the Lean paragraph: `proofs/lean/README.md`, `research/2026-11-14_opus_lean-devices/REPORT.md`, `research/2026-11-14_astra_lean-check/REPORT.md` and its `FAITHFULNESS.md`. The independent check rebuilt the upstream development, the devices and the replacement route from a fresh clone, found only the three standard axioms, and confirmed that the replaced phase and polynomial argument is unreachable from the main theorem. It rejected three wordings of the README: the full Lemma 4.5, the literal "no polynomial", and TODO T5. The paper's paragraph claims none of them.

## Judgement calls

- **Flow figure.** A cycle of `2h` incidences drawn on two columns needs a long closing edge if its vertices are listed in cyclic order. That edge was the main clutter. I folded each cycle instead, so the used incidences form short X shapes between neighbouring rows. The price is that one cannot follow a cycle by reading down the column. The caption says the two states alternate along a cycle of 14 and a cycle of 6.
- **Companion notes in the bibliography.** Kept as sentences with titles and paths. An `amsplain` entry without an author reads oddly, and a path is what lets a reader find the file.
- **Connectivity checks.** Kept in the text as short lists by cases, not moved to a footnote. Each list item is one case of the deletion.
- **Figure 2.** Enlarged from 9.5cm to 10.9cm rather than accepting labels on grey. This and the closing section are why the paper has 20 pages. The last page holds only the references.
- **Title of the bijective note.** Changed to "Two involutions for the good-pair lemma", since the naming rule would otherwise leave the old name in the most visible place. The older name is mentioned once, after Theorem 1.

## What failed, and why

- Three attempts to keep the primal note at 15 pages by shortening the new sentence failed, because the page before the dictionary was exactly full. Moving the three-line lead-in to the figures behind the dictionary's note fixed it (CHANGELOG C4).
- One `pdflatex` run of the primal note stopped with "I can't write on file primal.pdf" while my own render script still held the file. The rerun succeeded.
- I did not rerun `proofs/primal/figures/check.py --build` or the primal generator `research/2026-11-14_astra_primal-revision/build.py`. The second writes into a folder I do not own. `primal.tex` and the Markdown were edited by hand in step.
- The gallery (`paper/figures/gallery.pdf`, now ten pages) was rebuilt but not inspected page by page.
- The page renders tracked in `proofs/involutions/figures/page-*.png` and `contact-*.png` were not regenerated. They show the note before the renaming.

## What is still open

- No human has read the final PDFs.
- Nothing mathematical was reopened. The open items of the two referee reports stand as they are.

## Leads for others

- **Lean owner.** `proofs/lean/README.md` still carries the three wordings that the independent check rejects ("Lemma 4.5" entire, "no polynomial lemma", TODO T5), and its "what is checked" list says "Lemma 4.5 (with epsilon)" without the restriction. The paper no longer depends on those wordings.
- **Blueprint and synthesis owners.** The bijective note's theorem is now called the good-pair lemma. `digestions/` and the GLOSSARY row of exceptions for the involution note can drop "forest pair".
- **Primal owner.** If `build.py` is run again from the Markdown, CHANGELOG C4 (a TeX-only move) has to be reapplied, or page 11 gets three lines alone.

## Three best next steps

1. One human read of the closing section of the main paper, pages 18 and 19: the two lists and the Lean paragraph are new prose.
2. Correct `proofs/lean/README.md` to the independent check's wording, so that the paper and the README say the same thing.
3. Regenerate the tracked page renders of the bijective note, or untrack them.

## For a human editor

1. **Page count.** The paper has 20 pages and page 20 holds only the 17 references. I did not test which cut recovers the page. The closing section is about fifteen lines longer than before and Figure 2 about 1.4cm taller.
2. **The Lean paragraph** (page 19) is long for a remark. It lists exactly what was checked, as asked. An editor may prefer two sentences and a pointer to `proofs/lean/README.md`, once that README is corrected. `research/2026-11-14_opus_lean-integration/PAPER-SENTENCE.md`, written while I worked, offers a two-sentence and a one-sentence wording with the same qualifications. I took from it the words "in its algebraic model".
3. **Figure 2, label 11.** It is clear of everything, but it sits about as near to a hollow vertex of G as to its own vertex. Label 10 in Figure 5(a) lies on a shaded face with a white halo, the only label in the paper that does.
4. **Figure 12.** Check that the folded rows read well to someone who has not seen the old figure. The alternative, cyclic order with one long closing edge per cycle, is a one-line change in `check.py` (`fold`).
5. **Figure 13(c).** Labels 6, 7, 8 are clear by 0.56pt to 0.92pt only. The panel is small.
6. **The two lists in "Why each hypothesis is needed".** They are the only bulleted lists in the paper. A footnote is the alternative.
7. **Example 3.3.** The table lost its vertical rule to match Tables 1 and 2. Check that the row labels still read as labels.
8. **Author lines.** The main paper's is empty by decision. The notes still say "Primal reconstruction, gpt-6-astra" and "Research note, 14 November 2026", and the primal note's running head repeats the first.
9. **The primal note's figures.** I did not touch them. In its Figures 1 and 2 some face labels (`f6`, `f11`, `f12`) looked close to curves of G on a 66 dpi contact sheet. I did not inspect them at 200 dpi. The label placer added here would fix that if those panels called `vertices(labels=...)`, which they do not.
10. **The bibliography** breaks "Computa-tional" in entry 5. It is the only line-end hyphen left in the paper.
