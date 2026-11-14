# Report: review of draft A

1. Mathematics: the reverse-Lamport audit gives **FOLLOWS** for Theorem 1 (`PROVED-HERE`, human review pending). It found four text defects, none fatal: Lemma 4 is missing a hypothesis; Lemma 5's "t0 with contribution zero" (copied from OpenAI) cannot be checked as written; Lemma 8 never says that y0 lies outside the disk, and it cites Lemma 4 for a graph that lemma does not cover.
2. Examples: every number in both worked examples recomputes (`COMPUTED`, independent script). One claim is imprecise: the "other group" contributes exactly 0.
3. Exposition: correct and readable, and clearer than all three source papers at six of ten steps, but not yet "far clearer". Q_s and the spokes have no stated purpose until §5, Lemma 5 is OpenAI's text copied nearly unchanged, notation collides at nine symbols, and three figures are never referenced.
4. Simplification found: the sign of a pair is ε(r,s) = ∏_t δ(r(t), s(t)), which removes J (`PROVED-HERE`, `COMPUTED` on 196 pairs).
5. Deliverable: 25 exact edits (`EDITS.md`), each checked against the source. Applied to a scratch copy, they build cleanly (12 pages). Attribution needs fixing: three internal project paths are cited as references, and Li's half-ray counts, which are the same objects as heights, are not credited.

## What I set out to do

Review `paper/draft-A/barnette.pdf` in two separate phases, as the brief required. Phase 1: a cold read of the PDF with no other file open except `research/BRIEF.md`, then a summary written from memory. Phase 2: an informed review against the skills, the style guide, the three papers, the dependency skeleton, the referee reports and the author's notes. I did not open `paper/draft-B/`. I did not edit `paper/draft-A/` or `paper/figures/`.

## What I established

- **COLD-READ.md.** A page-by-page log of every hesitation. The main stalls: p2 (why spokes; how Q_s relates to P), p5 (the t0 sentence in Lemma 5), p6 (Fig. 4's equations differ from eq. (6)), p8 (the switch from Q_s to sides through s(t)), p9 (r and s swap roles in Fig. 6).
- **SUMMARY-FROM-MEMORY.md.** I reconstructed the whole proof except the reduction (3)⇔(4). I also first misremembered P as containing Q_s. Both gaps match the cold-read stalls.
- **REFEREE.md** (`PROVED-HERE`). Obligation graph with 28 nodes, dependency table and verdict FOLLOWS. Decisive nodes: N5c (the only use of "no separating triangle"), N6a (B = I + ℓ, the only place bijectivity enters the disk identity), N9 (heights detect enclosure), N10 (common sign at the minimum cycle count) and N12b (P0 is acyclic). Repairs needed: N4, N5b, N12c, N12d. The author's `AUDIT.md` misses all four.
- **check_examples.py / check_examples.json** (`COMPUTED`). Independent recomputation from the oriented face lists in `paper/figures/{octahedron,running}.json`, on a Tutte straight-line embedding with the figures' root angles. Heights are computed literally as signed spoke crossings of straight rays, in two directions. Checked: every row of my table in REFEREE §4; (3)⇔(4) for all 1024 subsets S of the running example; equation (10) on every white face and every pair of the displayed group; ε = ∏δ on all pairs of both examples and on 192 pairs of `barnette_lab.core.generated(12)` with every black outer face. Command: `python research/2026-11-14_opus_review-draft-A/check_examples.py` from the repository root (about one minute).
- **EXPOSITION-REVIEW.md.** The 22 style rules: 9 pass, 2 partial, 11 fail, with the offending lines. A step-by-step comparison with OpenAI, Li and the constructive paper. The unslop audit (the loud tells are absent; synonym cycling between side and edge, colon connectors, filler and an unsupported "exactly" survived). A table for each figure. The attribution findings.
- **EDITS.md.** 25 edits ordered by value to the reader. Every quoted old string occurs exactly once in `barnette.tex` (checked by script). Applying the edits mechanically to a scratch copy builds with no errors, undefined references or overfull boxes.

## What failed and why

- The shared layout coordinates (`layout-running.json`) do not form a straight-line embedding: some faces have inconsistent orientation. The figures use curved edges. I replaced them with my own Tutte embedding with the same root angles, which preserves orientation. Orientation-sensitive results are therefore relative to the figure's orientation, which the face triples fix.
- My first draft of E17 explained the expansion wrongly, saying the surviving term lies at the cyclic pair. It lies at U = all cycles, which in the example is a forest pair. I corrected it before committing.
- I did not independently verify the constructive manuscript's exact separating-triangle criterion. E25 cites it as that paper's claim, not as a fact.

## What is still open

- Whether the edits make draft A "far clearer" needs a second cold reader. I cannot un-read the draft.
- E10 (ε = ∏δ) changes the sign used throughout §4. It is proved and computed here, but the draft's owner should re-run the author's `examples.py` after applying it.
- Figure changes need the figure owner: labels in Fig. 1(c)–(f); label collisions in Fig. 2; Fig. 8(c) redrawn; a variant of `04-local` without OpenAI's weights; B_d, W_d in Fig. 4.
- The shared figures `01-cube.pdf` and `11-spokes.pdf` are modified and uncommitted in the working tree. Any rebuild of draft A will pick them up. Fig. 1 must be re-checked after the next build.

## Three best next steps

1. The draft's owner applies E1–E14 (purpose of the spokes and Q_s, the Lemma 5 fixes, the sign simplification, the disk counts, the Lemma 8 bridges), rebuilds, and re-runs both `examples.py` and `check_examples.py`.
2. A fresh agent repeats the cold read on the edited draft and logs stalls only, to test whether the p2 and p5 stalls are gone.
3. The figure owner makes `04-local` panel (a) a standalone figure with one more side marked (the side of P through s(t)), and fixes Fig. 2 and Fig. 8(c).

## Leads for others

- **The sign of a pair is a product of local signs** (`PROVED-HERE`, REFEREE N7). The identity ε = ∏δ(r(t), s(t)) holds for draft A's sign. It probably also holds for any draft that uses (−1)^{(n+J)/2}: the proof is a per-cycle parity count from the disk identity. Draft B and the merge agent should consider it.
- **Heights are Li's half-ray counts** (Li, Definitions 13–21). Any draft that uses heights should credit Li for the object and claim only the product form.
- **OpenAI's sentence "Include t0 in the sum in (3.1), with contribution zero"** cannot be checked as written. Any draft that copies OpenAI's Proposition 3.1 inherits it. E9 gives a replacement that can be checked.
