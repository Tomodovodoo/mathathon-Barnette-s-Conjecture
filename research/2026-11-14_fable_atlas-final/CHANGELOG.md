# Changelog: final integration of the atlas

Fable 5.2, 2026-11-14. Everything here concerns `digestions/atlas/`. "Asserted" means an `assert` in the figure function, which `build.py` and `verify.py` both run. All such statements are `COMPUTED` on the named finite example by `python digestions/atlas/build.py` and say nothing general.

## 1. Audit findings (research/2026-11-14_sol_atlas-audit/)

| Finding | How I checked it | Outcome |
| --- | --- | --- |
| E1, page 10: "forest implies determinant ±1" is false without root separation | Asserted: five states have acyclic opposite edges, a path of them joining two roots, no partner and determinant 0. The six good states have ±1, one state has a cycle. | Applied. The text had already been corrected to "three trees, one at each root". I added the sentence that acyclic is not enough, changed caption (b), and added strip (c) listing all twelve states by case. |
| E2, E3, page 17: the forest matroid is on `T` with the roots merged; "one cyclic state" does not account for six failures | Asserted `(1, 5)`: one state with a cycle, five with a tree holding two roots. | Applied in the text, in caption (b), in the table labels ("trees at the roots") and in a note under the table. |
| E4, E5, page 18: subsets are taken after merging roots; a fractional corner does not rule out every rounding rule | The LP code already merges the roots (vertex 0 stands for all three). The second point is logic. | Applied in the ledger and the text. I also removed the fourteen "1/2" labels, which touched each other; the dash pattern and the caption carry the value. |
| E6, E7, page 20: the mean obstruction only excludes weights on the whole spoke graph | `LIT`: `sol_referee-covers/INTEGRATION.md` line 25 and the summary of `opus_two-tree-packing/REPORT.md` say exactly this. | Applied, shortened to fit the word limit. Status no longer says "unrefereed". |
| E8, E9, page 23: 466 exceptions of 28,189; direct lift refuted at 18; 857,920 contractions at 18; opening sentence | `LIT`: `fable_induction-completion/REFEREE.md` lines 16, 25, 29 and its REPORT line 21. 28,189 − 466 = 27,723. | Applied. Declined one clause: "all have the two-sided outer-forest pattern". I did not find time to verify it in the source, so the page says only that the 466 need a rule nobody has found. |
| E10, page 24: the Feder and Subi dictionary omits the "proper" condition | `LIT`: `astra_older-approaches/BRIDGES.md` line 7 states the extra condition (degree four, no incident digon). | Applied in text and table, as "a degree condition on omitted vertices". The digon clause is left out for length; the table says the panels do not test the extra condition. |
| E11, page 15: 18-vertex failure independently checked and minimal | `LIT`: `sol_referee-conjectures/REPORT.md` summary line 2. | Applied. |
| E12, page 6: stale "checked on the cube only" | `LIT`: `opus_referee-involutions/REPORT.md` and `fable_referee-involutions-v2/REPORT.md`, 1,206 rooted instances through 14 vertices. | Applied, reworded: the check is of this project's write-up of both pairings, not of Li's text alone. |
| E13, E17, page 19 and chart: rainbow descent reaches 17 by enumeration plus a theorem | `LIT`: `fable_referee-topology/RAINBOW.md` line 125 (34,659,072 trees in 1,119 rootings, Proposition U for 6,923). | Applied. The status now says "with a theorem for part of the cases" and no longer calls it one uniform enumeration. |
| E14, E15, page 28: counterexample sizes 60 and 70 become 33; "first failure" overstates | `LIT`: `sol_referee-conjectures/LATTICE-READING.md` line 115 (33-vertex witness, 2,916 states). | Applied. The heading is "counterexample known at", and a ring marks the two cases where every smaller instance was checked. |
| E16 and the range ledger, page 28 | Each row against the reports: bound replayed on 9,531,638 roots through 22 (`sol_referee-conjectures/REFEREE.md` line 26); descent on 24,744 pairs through 16 (line 27); the 23,824,742-root census replayed through 16 only (`sol_referee-covers/REFEREE-covers.md` line 51); contractions (`fable_induction-completion`). | Applied as a redrawn chart: solid bar = every case by two programs, outlined = by one, dashed = samples. Six open rows, with the separator-free census and the two contraction statements split out; eight refuted rows, R2 and the direct lift added. |
| Page 22: five words hide six connection signatures, alternating word 8 + 4 | Asserted: 5 splits, 6 patterns, 28 cycles, alternating split `[4, 8]`, every other split one pattern. My signature uses open sides with the cut edges removed; the audit's used closed sides. Both give six. | Applied. The bottom row now has six panels with the joins written out. |
| Page 13: this is an unrooted diagnostic | Logic: seven black faces, seven vertices. | Applied, one sentence. |
| Page 21: "delete the white centres" still leaves edges of T | Reading the picture. | Applied: the text now says which layer to keep. |
| Page 4: "no bracket is zero" | The brackets vanish at x = 0. | Applied: "no bracket vanishes identically". |
| Contents: a state uses every non-root vertex once | The intro on the contents page says "one in each black face" only. | Declined for space; page 2 opens with the full definition. |
| Page 1: the matrix branch is a rewriting, not another nonvanishing theorem | The page already says "They are not four proofs". | No change. |
| Sources: add later referees, do not call refereed results unrefereed | Row by row while editing statuses. | Applied on pages 6, 15, 20, 22, 23, 24, 27, 28. The intro to the table now says a check by a second model is not peer review. |
| Greyscale: thin white-tree curves on 8 (b, c), 19 (a, b), 21 (a, c) | Greyscale contact sheets. | Applied: 1.5pt (1.1pt in the crowded 21 (a)). |
| Greyscale: Q strokes with a white halo; page 3 tint; page 24 (b) crowded counts; page 14 small hatching | Greyscale sheets. | Declined or partial. Q is orange dashed on thin grey and stays readable in grey. Page 24 (b) got smaller dots and tighter labels only. Pages 3 and 14 are unchanged. |
| Proposed reading order (32 entries) | Editorial. | Declined: renumbering 28 pages and every cross-reference was outside what two hours allowed. |

## 2. Proposed figures (digestions/atlas/proposed/, now removed)

None of the seven TikZ files was pasted in. Each was recomputed in `figs_*.py` and redrawn with the atlas's own panels.

| Proposal | Integrated as | Asserted |
| --- | --- | --- |
| p06-rays | Page 6 (c), (d), replacing the two squares of orientations (page 4 already shows all eight orientations). I chose a move whose partner crossing is a spoke of `r`, so the cycle is reversed and the pair changes; the proposal showed the case with no change. | Ray crossings are odd exactly for white faces inside the cycle, on all 176 (pair, cycle, white face) triples; the image is a pair with the opposite sign; the same rule leads back. |
| p11-matrix | Page 11 (d), as a 5 by 5 grid in the style of page 10, with faces lettered `a` to `e`. | `[y_a…y_e] det N` equals the pair polynomial symbolically; it has two monomials, one for each good state; each edge lies in one black face. |
| p16-count-strip | Page 16 (c): all nine states drawn in volume order instead of a sentence. | Nine states, eight good, one with a cycle, none without a partner; the cycle is the boundary of a white face. |
| p22-connections | Page 22, bottom row. | See the table above. |
| p23-aligned | Page 23 (b). The proposal's layout had near-degenerate faces. `lib.aligned_layout` minimises the squared displacement from panel (a) with every face keeping 55% of the smallest area of a relaxed drawing. | The toolkit's layout check (orientation, no crossings). |
| p24-colour-restriction | Page 24 (c), (d), with the table moved below at full width. | 10 vertices, 24 edges, even degrees; 14 Hamiltonian cycles; passing counts per colour class `[13, 14, 14]`; in the excluded partition each tree contains an offending edge. On the running example still 28 of 28 for every class. |
| p25-count-strip | Page 25, a bar of eight boxes, and the root-joining paths drawn heavy. | Counts `(4, 2, 2)`; a cycle is produced exactly when its state has no cycle and no path joining two roots. |

## 3. Naming convention in the figures

`rename_labels.py` (output in `rename-output.txt`) replaced 38 strings in the figure sources and `lib.py`: "tree matching(s)" to "good state(s)", "tree pair(s)" to "good pair(s)", "forest state" to "good state". By hand: "cycle cover" to "cover" in five labels and two page texts, "Q_s is a forest" to "s is good" on page 4, the station caption on page 1, "forest" to "trees at the roots" in the table of page 17. Data keys in `computed.json` keep their old names.

## 4. Thin spots from the second pass

| Item | Outcome |
| --- | --- |
| Pages 16 and 25 a quarter white | Filled: the figures grew from 11.9 to 16.8 cm and from 14.1 to about 16 cm. |
| Page 11 states the matrix without drawing it | Drawn. |
| Page 6 marks not drawn | One move drawn; a complete marked object still is not. |
| Page 22 label words only | Six patterns with their joins. |
| Page 23 (b) not aligned with (a) | Aligned. |
| Page 24 (c) uninformative | Replaced by an example where the condition excludes a cycle. |
| Page 28 quotes unrefereed numbers | Still quoted, now with the referees' ranges and who repeated what. |
| Page 26 hand-placed coordinates | Unchanged. |
| Greyscale proofed on two pages | Greyscale contact sheets of all 31 pages, in `after/`. |
| Headings too close to labels | Cause found: inside a tabular, a row break with a length adds nothing under a deep nested tabular. Replaced by an explicit vertical skip on pages 22 and 25 and checked on the renders. Other pages with stacked blocks were not changed. |

## 5. Not done

- The page on the blueprint against the Lean proof and the page with the three written proofs side by side. Neither was started.
- The contents intro and page numbering are as before: 28 route pages, 31 PDF pages.
