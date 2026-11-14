# Report: fresh cold read and finishing edit of the main paper, version 2

**Summary.**
1. Cold read of the 19-page v2 PDF as a newcomer (COLD-READ.md, SUMMARY-FROM-MEMORY.md). It is clear and well ordered. The one weak moment was why the signed count cannot vanish.
2. Informed assessment (ASSESSMENT.md): 18 of 22 style rules pass, none fail outright. Every complaint of the first cold read is fixed except Figure 2's labels. Verdict before editing: *nearly* meets the owner's standard.
3. Applied 17 edits in three committed batches (CHANGELOG.md): plan wording, pronouns, the cube example, captions, history citations, the naming convention ("cover", "tree matching").
4. The main idea now has room: a one-cycle warm-up on the cube, then the $c$-fold difference, and a new Figure 11 that shows each cover as a square of orientations.
5. No mathematical problem found (MATH-ISSUES.md). Build clean, 19 pages, check.py passes. My verdict now: the paper meets the standard in its text; three figure items remain for a human editor.

## What I set out to do

The task had three phases: read v2 cold, assess it against the style guide, the sources, the
earlier review and the naming convention, then finish it without changing the mathematics.

## What I established (editorial judgements, HUNCH)

- After page 1 a newcomer can say what is proved, why connectivity is the problem, and why
  steps 1, 2, 3 and 5 exist. Step 4 lacked its reason. It has one now.
- On every step v2 is the clearest of the available accounts. The exception was the
  nonvanishing step: its proof was the most elementary, but its explanation was cramped. The
  project's route map (`HOW-IT-WORKS.md` §4 to §5) and atlas page 6 explained it better. The
  new text and Figure 11 bring that explanation into the paper.
- The worked example (α, β) carries the reader through Figures 4 to 12. This is the paper's
  biggest asset.

## What I changed

See CHANGELOG.md. The three batches are commits `edd9c0c`, `26fa43b` and `f04e0d1`. Each batch
started by re-checking `git log` on the file and re-reading it from disk. No other agent
committed to the file during my session.

## What failed or was not done

- Figure 2: labels 7 and 11 still sit on small G-vertices. Moving them needs the toolkit's
  label offsets, and I ran out of time.
- Figure 12 (flow network) is still cluttered.
- "Two companion notes give a primal formulation and an account using two sign-reversing
  involutions" has no citation. Citing or deleting it is the owner's call.
- The Section 7 connectivity checks for the bipyramid incidence graph and the 26-vertex graph
  are long, but the referee asked for them (CHANGES E6, E7). I left them.
- I deleted my 130 dpi cold-read renders by mistake. The low-resolution base renders of the
  starting PDF remain (`renders/before/`).

## Leads for others

- Referee: confirm the cube statement and the "tree matching" sentence (MATH-ISSUES.md items 1
  and 2).

## Three best next steps

1. Regenerate `03-dual` with labels 7 and 11 moved off the G-vertices, keeping the filename and
   rerunning `check.py`.
2. Redraw `06-flow` with the `X` column ordered along the cycles of the 2-factor, so the double
   and solid edges stop crossing, and with a darker shading for the tight set $S=\{2\}$.
3. Have one human reader do a one-hour read of pages 11 to 15, the sign, the heights and the new
   nonvanishing passage. That is where a reader's attention is most likely to fail.

## Honest verdict

The text now meets the owner's standard. It starts from the obstacle, every definition arrives
with a reason, and the main idea gets a small case, a general mechanism and a picture of that
mechanism. No float interrupts a statement or proof, and no page is more than about a tenth
blank. The paper is not yet perfect as a printed object. A human editor should look at Figure 2
(labels), Figure 12 (clutter), the uncited "companion notes" sentence, and whether the long
Cubic and 3-connected checks in Section 7 belong in a footnote.
