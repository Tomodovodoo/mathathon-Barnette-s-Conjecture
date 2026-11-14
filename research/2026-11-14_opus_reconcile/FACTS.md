# Fact table

Opus 5.5, 2026-11-14. One row per fact that at least two of the five reader documents state. Columns: SYN = `digestions/SYNTHESIS.md`; 09 = `digestions/steps/09-what-is-still-open.md` (00-overview states none of these facts any more); MAP = `digestions/route-map/ROUTE-MAP.md` (from `routes.py`), `HOW-IT-WORKS.md` and `labyrinth/sota.json`; ATL = `digestions/atlas/atlas.pdf` pages 26, 29, 30; PAP = `paper/main/barnette.tex`, section "Consequences and open questions" and the Remarks it closes. "-" means the document does not state it. Values are as found before this pass. The verdict says which document was wrong and whether this pass fixed it.

Sizes are dual order V unless marked primal.

## Counterexamples and witness sizes

| Fact | SYN | 09 | MAP | ATL | PAP | Authority | Verdict |
|---|---|---|---|---|---|---|---|
| Extreme of Propp's lattice of states need not have a partner | - | V=10 | V=10 | - | - | `opus_route-graph-theory/ROUTES.md` O1 | agree |
| Highest or lowest partnered state not good | 12 | - | 12 | - | - | `astra_referee-combinatorics` (reflections counted) | agree |
| Both extremes of the pair lattice carry no good pair | first at 18 | 18, no minimality | 18 | - | - | `sol_referee-conjectures`: all roots through 18, none earlier, 26 failures at 18 | agree. "First" is justified by Sol's census |
| Extremes or irreducibles (R2) | 33, has a separating triangle | 33 | 33 | three crosses at 33 | - | `sol_referee-conjectures` (two programs) | agree |
| A cover with no good state | 16 | 16 | 16 | - | - | `opus_referee-rainbow` INTEGRATION section 5 (`BAD_16_16_27.json`) | agree. HOW-IT-WORKS said "from 16 on"; now "witness at 16" |
| "Some good state lifts" | 18 | 18 | 18 | - | - | `fable_induction-completion` (50 contractions) | agree |
| Half-integral LP vertex | 13, witness | - | 13 | - | - | `sol_referee-structure` | agree |
| Strict descent, rainbow trees / pairs | 8 / 16 | 8 / 16 | 8 / 16 | - | - | `opus_referee-rainbow` (8); `astra_referee-descent` (16) | agree |
| Lookahead two / three | 21 / missing | 21 / 40 | 21 "minimality from author census" / 40 | - | - | `astra_referee-descent` INTEGRATION: 21 least, confirmed by its own census through 20; 40 a witness needing four exchanges | SYN lacked 40 and MAP called 21's minimality author-only. Fixed in SYN, MAP, HOW-IT-WORKS, 09 |
| Evict / surplus walk cycles | 38 | - | 38 | - | - | `fable_referee-topology`, replayed in `opus_referee-rainbow` | agree |
| Rainbow loads M-convex | - | - | 12 | - | - | `fable_referee-topology` RAINBOW.md | single document |
| Sign gauge | "No sign change on incidences removes the cancellation", 13 | - | label "a global sign gauge on incidences" | - | - | `fable_referee-families` INTEGRATION item 9: only signs on the variables of F; with signs on the incidences of both states the equations are solvable on all 5,088 paired roots to 16, no proof | SYN and MAP label wrong. Fixed in both and in `routes.py` |
| First nonreal zeros / off-circle zeros | both at 12 | - | "real-rooted fails at V=10" / 12 | - | - | `fable_referee-families` item 8: nonreal zeros at 9, off-circle at 12 | SYN and MAP wrong. Fixed |
| Mean obstruction | "cannot match the target degrees" | - | "excludes full-support measures" | - | - | `fable_referee-families` "Do not cite": target on a face of the degree polytope | SYN reworded to the referee's sentence |
| Residues of the number of good states | 2,3,4,5,7,11 at 6,13,9,14,16,26 | - | - | - | - | `fable_referee-families`: 2..7 checked; 11 is the author's, not replayed | SYN now says 11 was not replayed |
| Hexagonal prism: eligible cycles / produced | 4 / 2 | 4 / 2 | 4 / 2 | - (page 25) | 4 / 2 | `sol_referee-structure`, `astra_lean-check` COUNTEREXAMPLE.md | agree |
| Fixed-cycle levels disconnected | 18, witnesses | - | 18 | - | - | `sol_referee-covers` C5 | agree |
| Repair inside one cover fails | 18 | 18 | 18 | - | - | `astra_induction-lemmas` X.md, `astra_referee-descent` | agree |

## Verified ranges

| Fact | SYN | 09 | MAP | ATL | Authority | Verdict |
|---|---|---|---|---|---|---|
| C1 (at least 2^m good states), all roots | 22, 4,656,948 instances, two programs | 22 | 22 | 22, two programs | `sol_referee-conjectures` | agree |
| C1 without separating triangles | 24, 23,824,742 roots; replay to 16 | 24 | 24, T4 | 24, replay to 16 | `astra_cycle-covers`, `sol_referee-covers` (3,374 occurrences to 16) | agree |
| C3 (pair descent), author | 193,623,384 pairs to 23 | same | same | - | `fable_descent` REPORT | agree |
| C3, independent | "reproduced through 16, still running" | "through V=19" | "through V=19" | descent "through 16" in sources list | `astra_referee-descent` REPORT (final, still being edited in the working tree): 3,373,400 pairs through 20, and the V=40 batch | SYN, 09, MAP, labyrinth README wrong. Fixed. ATL sources line still says 16 (see PAPER-FIXES, atlas section) |
| Step X (rainbow descent) | 17; 1,485 of 1,543 at 18; "not reviewed" | 17; Opus to 12 and 7 more at 18, 51 left | same as 09 | 17 | `opus_referee-rainbow` | SYN wrong about review. Fixed |
| Lemma G | 62,416 instances, 8 to 19 | to 19 | 62,416 | - | `fable_induction-completion`, `astra_induction-lemmas` | agree |
| Contraction inequality | 1,202,792 to 18 | - | - | - | `fable_induction-completion` | single document |
| 2^m bound proved cases | one and two covers | one cover; two-cover weak bound | same | - | `sol_referee-covers` C3 | agree |
| Tube recurrences | - | "independent AI checks in the stated scopes" | "independently AI-refereed all-length" (sota rarity) | "a second model rebuilt their proofs independently" | `fable_referee-families` DISAGREEMENTS: first referee is the author's model; different model finite only (width 4: S to L=20, M, P to 14, H to 10; width 6: S, M to 12, P to 9, H to 6) | MAP, sota and ATL wrong. MAP, sota, HOW-IT-WORKS fixed; ATL in PAPER-FIXES |
| Prism-chain Hamiltonian count | - | "corrects gluing-dependent counts" | not stated | - | `fable_referee-families` item 4: 8*3^(q-1) pole on pole; 8 then 20*3^(q-2) for the mixed rule | no document quoted the formula without rule. MAP now states both with rules |
| Sign against phase | 24,856 pairs to 16; 174,763 words | - | - | - | `opus_cross-audit`, `astra_lean-check` | agree |

## Counts

| Fact | SYN | MAP | ATL | PAP | Authority | Verdict |
|---|---|---|---|---|---|---|
| Route records / refutations | 246 / 77 | 246 / 77 | 30 routes drawn | - | `routes.py` rebuilt: 246 / 77 | agree. INDEX row says 244 (older map run) |
| Blueprint, route statements | 5 / 17 / 10 / 2 of 34 | "Do not read 4/25/5 as current" (HOW-IT-WORKS) | 4 / 25 / 5, then 5 / 27 / 2 | - | `opus_lean-integration/STATUS-TABLE.md`: 5 / 17 / 10 / 2 | ATL and HOW-IT-WORKS out of date. HOW-IT-WORKS fixed; ATL in PAPER-FIXES |
| Atlas pages / routes | 34 / 30 | - | 34 / 30 | - | `atlas/README.md` | agree |
| Lean "no polynomial" | qualified (six lemmas) | qualified in MAP; HOW-IT-WORKS "excludes the complex phase and polynomial", "check pending" | - | "in place of the complex phase and the polynomial of OpenAI's nonvanishing argument" | `astra_lean-check` REACHABILITY.md, `proofs/lean/README.md` | HOW-IT-WORKS wrong, fixed. PAP accurate but could name the scope (PAPER-FIXES) |

## Review status

| Work | Author | Referee | Same model? | Documents before this pass |
|---|---|---|---|---|
| Families, probability | Sol | `sol_referee-covers` (Sol); `fable_referee-families` (Fable) | first yes, second no | SYN section 3 said "no different model has checked them". Fixed |
| Algebra | Sol | `fable_referee-families` REFEREE-algebra (Fable) | no | SYN: "not reviewed". Fixed |
| Two-tree packing | Opus | `opus_referee-rainbow` REFEREE-packing (fresh Opus) | yes | SYN: "nobody has reviewed", "not reviewed". MAP text: "author proof unreviewed". Fixed |
| Step R, unique cover, sign-free evenness | Fable | `opus_referee-rainbow` (Opus) | no | SYN partial; HOW-IT-WORKS "unreviewed". Fixed |
| Partial G, induction lemmas | Astra, Fable | `astra_referee-descent` REFEREE-induction (fresh Astra) | yes for Astra's G | 09: "independently AI-refereed". Fixed to name the same model |
| Descent study | Fable | `astra_referee-descent` (Astra) | no | SYN: "at a checkpoint". Fixed |
| Lean devices | Opus | `astra_lean-check` (Astra) | no | HOW-IT-WORKS: "pending". Fixed |
| Cycle covers | Astra | `sol_referee-covers` (Sol) | no | agree |
| Lattice conjectures | Opus | `sol_referee-conjectures` (Sol) | no | agree |

## Names

good state, good pair, cover, m: SYN, 09 and MAP use them and gloss the older names (tree matching, forest pair, c_min, `#TM`). The map still prints `#TM` and `TM` inside some route texts quoted from census files, which the head of ROUTE-MAP.md explains. No change.

## Notes on sources

- `astra_referee-descent` had uncommitted edits to INTEGRATION.md, REPORT.md and the two referee files while I worked. I used the working-tree text (V=20).
- `proofs/sign-free/sign-free.pdf` existed at the end of this pass. SYNTHESIS lists it as being written.
- The "two same-model referee reports" of the brief are Sol's REFEREE-families.md and REFEREE-probabilistic.md in `sol_referee-covers`. Astra's review of Astra's partial G is a third case.
