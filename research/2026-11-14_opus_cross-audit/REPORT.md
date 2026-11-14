# Cross-audit report

1. The phase dispute: the reviser is right. Real sign / Lean phase = i^n for every pair (i^(-n) with the opposite corner order); the referee's formula is correct but equals i^n. PROVED-HERE, COMPUTED on 24,856 pairs.
2. The primal note gets ACCEPT. Every referee item was applied, Remarks 14 and 15 are correct, the figures match the text. I made nine small edits and rebuilt the 15-page PDF.
3. Consistency: delta, the sign, J and every example number agree across documents. The conflicts are names: one condition has five names (good state, tree matching, forest pair, tree pair, forest state); k, B, H and "selected" are overloaded; inv's height has the opposite sign to main's weight.
4. Hygiene: 15 .pyc and 3 LaTeX logs untracked, top-level .gitignore added, no broken relative links (111 checked), 7 research folders without REPORT.md, about 150 MB of proposed cleanup listed for the coordinator.
5. Open: Li's marked-object counts (279/213) I did not reimplement; the three remaining naming edits outside proofs/primal/ are proposals only.

## What I set out to do

The brief (user message of 2026-11-14) had three parts: adjudicate the referee/reviser disagreement on the real sign versus Lean's phase and give the primal note a final read; build a project-wide table of names and symbols with conflicts and recomputed numbers; survey repository hygiene, untrack build artefacts and propose the rest.

## What I established

**Part 1.** ADJUDICATION.md. For a pair with t = sum delta, the real sign is i^(n - t) for any n signs, and 3 | t by Lemma 5 on the circuits of D, so Lean's phase `I ^ (rawIndexSum / 3)` is exactly i^(t/3) and the ratio is i^n (PROVED-HERE). The referee's ratio (-1)^((n+3c)/2) i^c is right as an expression and equals i^(n+4c) = i^n; the parity fact n = c (mod 2) only makes the exponent an integer and, for the opposite corner order, makes the constant i^(-n). COMPUTED with scripts/phase_ratio.py on all 297 plantri Eulerian triangulations with 6 to 16 vertices plus the running example, both colour classes, every root, every ordered pair: 7,890 rooted instances, 24,856 pairs, 295 instances with two different circuit counts, no failure; polynomials agree coefficientwise up to i^n; all 2,780 pairless rooted instances have a separating triangle.

PRIMAL-FINAL-REVIEW.md. Line-by-line read of the TeX and all 15 rendered pages; all four counts of Figure 3 and the flow totals of Figure 4 rechecked by hand; each of F1 to F9 and M1 to M5 traced to the text. Edits applied in proofs/primal/: phase paragraph, definition of "compatible", embedding sentence for the planar corollary (the one residue of referee F1), two internal references made into paths (one had the wrong section numbers), two captions, Figure 8 label collision, small wording. STATUS.md phase section rewritten as the adjudication. Verdict ACCEPT.

**Part 2.** CONSISTENCY.md. A table of 25 objects across main, v1, involutions, steps and GLOSSARY, HOW-IT-WORKS and the primal note, with ten numbered conflicts. Recomputed with scripts/recount.py: running example 12 states, 8 ordered pairs, 7 with a partner, 6 tree matchings, 2 covers of 2 cycles, m = 2, lowest coefficient 9, 28 Hamiltonian cycles of which 6 avoid e0; hexagonal prism 3 states, 2 good, avoiding cycles 4 / 2 / 2 for the three sides of t0, the same for the other colour class. All agree with the documents that state them. Proposed convention: main's vocabulary (good state, selection, cover, m), k only for black faces, B only for black vertices, one height sign.

**Part 3.** HYGIENE.md and CLEANUP-PROPOSAL.md. Commit 670951a removes 18 build artefacts from the index (list in data/untrack-list.txt; files stay on disk) and adds a top-level .gitignore. I did not ignore `*.log` or `*.out` globally because 23 tracked files with those extensions are computation transcripts or Lean outputs cited as provenance. No cloned upstream is tracked. No relative Markdown link in digestions/ or any README is broken. INDEX.md misses 12 folders.

## What failed and why

- I did not recompute Li's marked-object counts (279 versus 213). It needs Li's drawing-dependent construction, which I could not reimplement in the time. The involutions referee had already reproduced both with independent code; I confirmed the drawing-independent invariant (lowest coefficient 9) and corrected the wrong explanation in HOW-IT-WORKS (proposal C9).
- My first commit added 19 page renders by mistake; `git commit -- <paths>` re-added files I had removed from the index. Fixed in 670951a. Lesson: a pathspec commit takes the working-tree state of the paths, so index-only removals must be committed without a pathspec after checking that nothing else is staged.
- I did not settle which corner orientation Lean's `ColoredDual.oriented` produces relative to the note's sphere orientation. The ratio is i^n or i^(-n); the conclusion does not depend on it.

## Still open

- Human review of the primal note's Section 2 and Remarks 14 and 15.
- The naming convention needs the owners of main, involutions and the digestions to agree; CONSISTENCY.md Section 5 lists the exact edits.
- The cleanup items need the coordinator's decision.

## Three best next steps

1. Adopt the convention of CONSISTENCY.md Section 4 in the paper/main revision now in progress (good state, selection, cover, m), and add one sentence there mapping "good state" to "tree matching".
2. Fix the two stale statements: the phase-dispute sentence in digestions/steps/00-overview.md and the 279/213 sentence in HOW-IT-WORKS.md.
3. Act on CLEANUP-PROPOSAL.md items A1, B1 and C4 (record-24.txt, the 17.8 MB proof PDFs, the literature PDFs in research folders); together about 100 MB.

## Leads for others

- The involutions referee or reviser: inv's H(s) = -omega(s) has the opposite sign of main's weight; say so in the text.
- The digestions owner: GLOSSARY uses k for black faces and k(s) for cycles of Q_s.
- Whoever next touches proofs/primal/: the word "selected" names D in Lemma 8 and P in Lemma 10.

## Files

ADJUDICATION.md, PRIMAL-FINAL-REVIEW.md, CONSISTENCY.md, CLEANUP-PROPOSAL.md, HYGIENE.md, scripts/ (README.md, phase_ratio.py, recount.py, terms.py, hygiene.py, build_primal.py), data/.
