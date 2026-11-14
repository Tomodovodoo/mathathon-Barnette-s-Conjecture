# Report: cold read and exposition review of the main paper

Agent: Claude Fable 5.2, 2026-11-14. Folder: `research/2026-11-14_fable_coldread-main/`. Object: `paper/main/barnette.pdf` (18 pages), source `paper/main/barnette.tex`, sha256 `992104f4…056e16`. Nothing under `paper/` was edited.

## Five-line summary

1. The body of the paper (Sections 3 to 6) is clear and in the right order. The opening is not: the abstract has five undefined terms, "The plan" compresses the proof into four clauses and omits the disk identity, and page 2 addresses readers of the other three papers.
2. Nine of thirteen floats cut a statement, a proof, an example or a sentence. A trial copy with my edits applied brings that to three of fourteen and removes the 40 percent blank on page 8.
3. Three steps lack their reason at the point of use (why a tree of faces; what D(r,s) is for; why a weight F). Each reason already exists in the paper's Section 7 or in the digestions, and the edits lift it into place.
4. Four figures are defective at print size (Figure 2, Figure 10, Figure 11(c), Figure 1) and need regeneration by the figure owner. One picture is missing and supplied: the same eight pairs grouped both ways.
5. `EDITS.md` has 40 edits: 59 replacements and 7 block moves, all machine-verified against the source, and 8 structural instructions.

## What I set out to do

Read the paper cold from page images, record the reading experience paragraph by paragraph, summarise the proof from memory, then review the exposition against the style guide, the three source papers, the two earlier drafts' reviews and the figure set, and say exactly how to improve it.

## What I established

All judgments are editorial (`HUNCH`) unless tagged.

- **Cold read** (`COLD-READ.md`). Page-by-page notes with tags for hesitations, undefined terms, objects without purpose, slow proof steps, figures, floats and wording, and a table of where each float lands. Verdict on the first page and a half: a graduate student can state the theorem, the obstacle, the reduction to an acyclic set with one side per triangle, and the order of the sections. The same reader cannot say how an edge set chooses a corner, why the condition falls on opposite sides, what the second corner choice is for, what is counted, or why a nonzero count gives the object.
- **Summary from memory** (`SUMMARY-FROM-MEMORY.md`). The proof in nine steps, reconstructed without looking back. The three things I did not understand: why the faces should form a tree and that goodness is sufficient only; what a height measures; what the cut inequality (5.3) means.
- **Review** (`EXPOSITION-REVIEW.md`), sections (a) to (h).
  - (a) 22 rules: 12 pass (4 with a blemish), 5 mixed or partial (rules 4, 6, 10, 18, 20), 4 fail (rules 2, 14, 19, 21), 1 not applicable. A table checks 24 problems raised on drafts A and B: 9 fixed, 6 partly fixed, 8 not fixed, 1 not addressed.
  - (b) Over 21 steps the merged paper is the clearest text at 13, level at 1, not the clearest at 7. In four of the seven a sentence from `digestions/route-map/HOW-IT-WORKS.md` or `digestions/steps/00-overview.md` is better.
  - (c) Flow per section and seven local moves; no section changes place.
  - (d) A replacement abstract (six sentences) and a replacement for "The plan" (a paragraph and five steps, about 420 words), each claim traced to a lemma of the paper.
  - (e) A table for every figure and table, with actions; the missing picture; a verdict on the overview figure (it does not work at its size or in its panel order).
  - (f) Layout. (g) Unslop audit with replacements. (h) Title, author, credits.
- **Edits** (`EDITS.md`, generated from `edits.json`).
  - `COMPUTED` (`code/verify_edits.py`, log in `verify-log.txt`): each of the 59 old strings and the 14 block boundaries of the 7 moves occurs exactly once in `paper/main/barnette.tex`; each anchor occurs once or is created by an earlier operation of the same edit; no two old strings overlap; the operations apply in the order given.
  - `COMPUTED` (same script with `--trial`): the edited copy `trial/barnette.tex` compiles with `pdflatex`, `bibtex`, `pdflatex` twice, exit code 0, no overfull boxes, 19 pages (`trial/barnette.pdf`). The new TikZ figure of edit 14 compiles and its numbers are those of Table 2.
- **Counts** `COMPUTED` (`code/style_counts.py`): 99 semicolons, 48 uses of "exactly", 23 colons used as connectors, 9 source lines of 45 or more words. Figure label sizes `COMPUTED` with PyMuPDF from the figure PDFs: 8 pt labels and 6 pt subscripts at natural scale; Figure 2 scaled by 1.15.

### Where floats land in the trial build

Read off `trial/barnette.pdf` by page.

| Float | Trial page | Lands |
| --- | --- | --- |
| Figure 1 | 2 | top of the page, between steps 3 and 4 of the plan, which breaks across pages 1 and 2 |
| Figure 2 | 3 | under "The example", before Section 2 |
| Figure 3 (state) | 5 | after the paragraph that defines Q_s and S_s |
| Figure 4 | 6 | after Example 3.3 |
| Figure 5 (selection) | 7 | after the proof of Lemma 3.6 |
| Figure 6 (disk) | 8 | after the sentence that introduces B, W, I, ℓ, h, before Lemma 3.8 |
| Figure 7 (pair, new) | 10 | top of the page, after the proof of Lemma 4.2 |
| Figure 8 (pair and D) | 10 | at its citation; Lemma 4.3 is whole on the page |
| Table 1 | 11 | after Lemma 4.4 and its remark |
| Figure 9 (cancellation) | 12 | after the remark that cites it |
| Figure 10 (heights) | 13 | **top of the page, between the statement of Lemma 4.6 and its proof** |
| Table 2 | 14 | before Example 4.9 |
| Figure 11 (groupings, new) | 15 | top of the page, after Example 4.9 |
| Figure 12 (flow) | 15 | at its citation, before Proposition 5.2 |
| Figure 13 (gluing) | 17 | **top of the page, before the last two lines of the proof of Lemma 6.1** |

Section 4 starts on page 9 with no blank space above it.

## What failed, and why

- **Three floats still interrupt in the trial** (Figure 1, heights, gluing). `[!htb]` sets a float where it is cited when there is room and otherwise at the top of the next page, wherever that falls. These three need hand placement once the text is final. For the heights figure the cause is that Figure 9 takes a third of the same page; the close-up of edit 39 would free the room.
- **I did not read drafts A and B or the three source papers in full.** For the step-by-step comparison I read the openings of the three papers and three passages of the drafts, and otherwise relied on the two earlier reviews. The table in (b) marks those rows. Nor did I read the two earlier `COLD-READ.md` files line by line; I checked their findings through the reviews and `DECISIONS.md`.
- **I could not check two credit questions.** Whether the tree of faces is already in the Lean proof released with OpenAI's paper (another agent's note says so), and the URL in reference 16.
- **A slip in my own phase 1 notes**: the cold read first said the abstract has seven sentences. It has five. Corrected in `COLD-READ.md`.
- **Time.** The brief allowed about two hours; the work took longer, mostly in the trial build.

## What is still open

- The figure regenerations (edits 36 to 39) are instructions to the owner of `paper/figures/draw.py`. I did not touch the figure code.
- The one-paragraph form of "The plan" was an earlier ruling of the user (`DECISIONS.md`). My replacement is a paragraph and five numbered steps. Its sentences run together into one paragraph unchanged if the ruling stands.
- Title and author are the user's decision (edit 35). The replace operation installs one of three proposed titles.
- The punctuation pass (edit 40) lists lines and is not done string by string.
- A local picture for Lemma 4.6 (one black triangle, the side g on C, the two ways a path can cross it) is described in the review and not drawn.
- The mathematics was not refereed here. My replacement texts restate lemmas of the paper and add two sentences of standard fact: a tree has at most one perfect matching, and a coloured triangulation on p vertices has 3p − 6 edges and p − 2 black faces, which is equation (2.3) of the paper. Both should pass the referee's eye before use.

## Three best next steps

1. Apply edits 1 to 8 (abstract, plan, history, the moved "differences" paragraph, Lemma 3.8, the two figure moves, the Section 4 roadmap). They change what a newcomer can say after the first page and a half, and they are verified to apply.
2. Regenerate Figures 1, 2, 10 and 11(c) as specified in edits 36 to 39, then apply the float edits 9, 10 and 21 to 27 and hand-place the three floats that still interrupt.
3. Give the edited paper to a fresh cold reader who has seen none of the project, with one test: after the abstract, the introduction and the plan, write down what each of state, opposite sides, second state, sign and weight is for.

## Leads for others

- **Referee of the mathematics**: l.94 says the heights remove the exponential sum; the finite difference of Lemma 4.7 does. Edit 4 corrects it and moves the paragraph. Please confirm the corrected sentence, and the claim "the sign of a pair is real, as in [5]".
- **Figure owner**: the white backing added to the labels of the running example hides vertices of G in Figure 2 (labels 6, 11, 12). `paper/figures/README.md` says "do not rescale"; the paper includes `03-dual` at 0.55 of the text width against a natural 0.48.
- **Coordinator**: Section 7 carries the project's status tags into the paper ("(proved; computed)", "we have not checked it"). Edit 28 removes them. The paper has no author line.

## Files

| File | What it is |
| --- | --- |
| `COLD-READ.md` | phase 1 notes, page by page |
| `SUMMARY-FROM-MEMORY.md` | the proof in one page from memory; three things not understood |
| `EXPOSITION-REVIEW.md` | phase 2 review, sections (a) to (h) |
| `EDITS.md` | 40 edits, generated; do not edit by hand |
| `edits.json` | the literal old and new strings |
| `code/edits_src.py` | authoring file; writes `edits.json` |
| `code/verify_edits.py` | checks the old strings, writes `EDITS.md`, builds the trial copy with `--trial` |
| `code/style_counts.py` | counts used in the unslop audit |
| `code/render_pages.py` | renders a PDF to PNG pages |
| `verify-log.txt` | output of the last verification and trial build |
| `trial/barnette.tex`, `trial/barnette.pdf` | the paper with all replace and move operations applied (19 pages) |
| `pages/` | the 130 dpi page images of the cold read and five zoomed crops |

Commands, from the repository root:

```
python research/2026-11-14_fable_coldread-main/code/render_pages.py paper/main/barnette.pdf research/2026-11-14_fable_coldread-main/pages 130
python research/2026-11-14_fable_coldread-main/code/style_counts.py
python research/2026-11-14_fable_coldread-main/code/edits_src.py
python research/2026-11-14_fable_coldread-main/code/verify_edits.py --trial
```
