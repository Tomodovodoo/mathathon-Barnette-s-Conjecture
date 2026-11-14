# Report: final integration of the illustrated atlas

1. The atlas is rebuilt with the audit's corrections, the naming convention inside the figures, and all seven proposed figures recomputed in its own toolkit. `verify.py` passes: 28 routes, 31 pages, no overfull box, texts 130 to 150 words.
2. Every audit finding was checked against the cited referee report or by an assertion before it was applied. Two were confirmed by computation here: five states with acyclic opposite edges have determinant zero, and the 4-cut has six connection patterns behind five splits (8 + 4 on the alternating one).
3. The last page now shows the referees' qualified ranges: which sizes two programs checked exhaustively, which only one, which are samples. Census claims beyond 16 vertices without separating triangles are marked as checked once.
4. Not done: the two optional pages (blueprint against Lean, three proofs side by side). Not done either: a full-size look at every page after the last edits.
5. `digestions/atlas/proposed/` is removed and the README says where it went.

Fable 5.2, 2026-11-14. Folder `research/2026-11-14_fable_atlas-final/`. I own `digestions/atlas/` for this task. No subagents.

## What I set out to do

Merge three inputs into one consistent, verified `digestions/atlas/atlas.pdf`: the independent audit (`research/2026-11-14_sol_atlas-audit/`) with its seven proposed figures, the naming convention already applied to the text, and the second-pass author's list of thin spots. If time allowed, add two pages. Then rebuild, verify, look at every page in colour and greyscale, and update contents, sources, README and renders.

## What I established

All statements below are `COMPUTED` on the named finite examples by `python digestions/atlas/build.py`, with the assertions in `figs_chain.py`, `figs_algebra.py`, `figs_order.py`, `figs_scope.py` and the certificate in `digestions/atlas/computed.json`. The atlas proves nothing general. `CHANGELOG.md` has the finding-by-finding table.

- `COMPUTED`, running example. Of the twelve states, six are good (determinant ±1), one has a cycle among its opposite edges, and five have no cycle but a path of opposite edges joining two roots. Those five have no partner and determinant 0. So "forest implies ±1" was false as the audit said.
- `COMPUTED`, running example, 4-cycle (1, 6, 11, 8). Its 28 induced-tree partitions give five splits of the cut vertices and six patterns once one records which cut vertices each tree joins through each open side. The alternating split occurs 8 times with one tree joined inside and 4 times with the other.
- `COMPUTED`, running example. For every pair, every cycle of `D` and every white face (176 triples), a ray in the fixed direction (1, 7) from the face's centre crosses the cycle's spokes an odd number of times exactly when the face lies inside the cycle. The move drawn on page 6 changes the pair to one of opposite sign, and the same rule returns it.
- `COMPUTED`, dual of the hexagonal prism. The coefficient of `y_a y_b y_c y_d y_e` in `det N(y, w)` equals the pair polynomial, two monomials of opposite sign. The determinant has six terms.
- `COMPUTED`, the audit's 10-vertex triangulation. It has 14 Hamiltonian cycles. Under the relaxed Feder and Subi reading, 13 pass for one colour class and 14 for the other two. On the running example all 28 pass for every class.
- `COMPUTED`, the 12-vertex witness. Nine states, all with a partner, eight good, and the cycle of the ninth is the boundary of a white face.
- `LIT` (project reports, read here, not recomputed): every range on page 28 and every changed status sentence. Sources are in the atlas's sources table and in section 1 of `CHANGELOG.md`.

Files: `CHANGELOG.md`; `rename_labels.py` and `rename-output.txt` (one-shot, do not rerun); `sheets.py`; `before/` and `after/` with three colour and three greyscale contact sheets each, 42 dpi.

## What failed, and why

- **The two optional pages.** I did not start them. Reading the atlas and the audit, porting seven figures and fitting the texts back under 150 words used the two hours.
- **Looking at every page.** After the final build I looked at pages 6, 11, 22, 23, 24, 25 and 28 at full size in colour, at the colour contact sheet of pages 0 to 11, and at the greyscale contact sheets of pages 12 to 30. I did not look at pages 10, 16, 17 or 18 at full size after their edits, nor at pages 0 to 11 in greyscale after the last build. The brief asked for every page in both modes.
- **Text length.** Writing the referees' qualifications into the statuses pushed fourteen pages over 150 words. I cut whole sentences to get back. Lost on the way: the remark that `2^q` partners pair off (page 6), "the determinant adds up the partners with signs" (page 10), "a good state is a spanning tree with prescribed degrees" (page 20, still in the caption), "each side must only report how its trees meet the cut" (page 22).
- **Heading spacing.** I found the cause of "headings too close to labels" late: inside a tabular, `\\[5mm]` adds nothing under a nested tabular that is deeper than 5 mm. I replaced it by `\noalign{\vskip}` on pages 22 and 25 only. Pages 4, 10, 11, 16, 24 and 27 use the same construction between stacked blocks and may still be tight.
- **Shell here-documents halve backslashes here**, as the second pass reported. I lost two builds to it before switching to file edits.

## What in the atlas is still schematic or unverified

- Page 28: no number on the chart was recomputed. "Two programs" means the original report and one referee model, both AI. I read the referee summaries and the lines cited in `CHANGELOG.md`, not the censuses.
- Page 28, row "some contraction keeps a pair": I put the two-program range at 17 and the one-program range at 19. `astra_induction-lemmas` also reports "G structure through V = 19"; I did not check whether that is a second exhaustive test of the same statement.
- Page 6: one move of one mark. No complete marked object, no fixed object, and only the case with a reversal. The crossing-parity assertion is for one ray direction on one drawing.
- Page 22: six patterns on one cycle of one example. I did not compare them with the general list in `fable_route-categorical`.
- Page 23: the layout of (b) is a least-squares fit with an area floor I chose by eye (55%). The 466 exceptions are not drawn, and I declined the audit's sentence about their common pattern because I did not verify it.
- Page 24: the extra Feder and Subi condition is stated from `BRIDGES.md`; I did not open their paper. The panels test the relaxed reading only.
- Page 26 (a), (b): hand-placed coordinates, as before.
- Pages 3, 14: the audit's greyscale remarks (tint contrast, small hatching) are not addressed.
- Nobody has audited this third pass, and no human has read any page.

## What is still open

- The blueprint page and the three-proofs page.
- The audit's reading order (32 entries) was not adopted.
- A full-size greyscale proof of every page.

## Three best next steps

1. Look at all 31 pages at full size in greyscale, and replace `\\[..]` by `\noalign{\vskip ..}` wherever two blocks are stacked in `figs_*.py`. This is an hour of work with no mathematics in it.
2. Add the blueprint page from `proofs/blueprint/blueprint.json` (4 exact, 25 translated, 5 without counterpart, of 34), drawn as the five-column chart, with the caution that the atlas is not checked in Lean.
3. Have a second model check page 28's chart row by row against the six referee reports, in particular the two contraction rows and the "smallest" rings.

## Leads for others

- `digestions/atlas/lib.py: aligned_layout` keeps a contracted triangulation aligned with its parent. `paper/figures/` could use it for any contraction figure.
- The audit's sentence "all 466 exceptions have the two-sided outer-forest pattern" should be checked against `fable_induction-completion/RESIDUAL-CASES.md` before anyone quotes it.
