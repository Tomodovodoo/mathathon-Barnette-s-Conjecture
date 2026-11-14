# Changelog: consistency edits, 2026-11-14

Convention applied (CONSISTENCY.md section 4, based on `paper/main/barnette.tex` v1; no v2 had landed, since `research/2026-11-14_astra_main-revision/` has no REPORT.md):

| Object | Name now | Replaced |
| --- | --- | --- |
| state with `Q_s` a forest, one root per component | good state | tree matching, forest state |
| pair whose second state is good | good pair | forest pair, tree pair |
| undirected `D` | cover | cycle cover |
| least number of cycles of a cover | `m` | `c_min`, `cmin` |
| number of cycles of `Q_s` | `q(s)` | `k`, `k(s)` (k stays the number of black faces) |
| incidence graph on `A`, `X` | `\mathcal B` | `B` (plain `B` is now only the disk count) |
| perfect matching `P` | selection `P` | "selected edges `P`" as a noun |
| height at a white face | `\eta_s(y)` | `h_s(w)` |

`#TM` is kept as the symbol for the number of good states, defined in GLOSSARY and step 09, because the census files use it. Source-paper columns of GLOSSARY keep each paper's own words. Historical labyrinth events (`ev(...)` lines in `seed.py`, `events.jsonl`) were not rewritten.

Mechanical renames were made by `rename.py` (counts per file and rule in `rename-output.txt`) and `heights06.py`; everything else by hand with `sub.py` (exact one-match substitutions).

## digestions/steps/

- **GLOSSARY.md.** New opening sentence (names follow the main paper; synonyms in the last section). Warning on `H`/`B` rewritten: Li's `H` = T's `B` = our `\mathcal B`. Rows: `B`, `K_B`, state use `\mathcal B`; `k(s)` -> `q(s)` with a note; good state row says the root condition cannot be dropped and keeps T's "tree matching" in the T column; good pair row redefined as "second state good", with T's "tree pair"; new `#TM` row; "cycle cover" -> cover; `c(D), m` row with O/L's `c_min` restored in their columns; height row -> `\eta_s(y)`, with the main paper's face-path version and the involution note's opposite-sign `H(s)`; `omega(s)` row says it equals `sum_y eta_s(y)` and rises counterclockwise like main's weight, and that inv's `H = -omega`; sign row adds `eps = i^n i^{-J}` and the settled Lean ratio `i^n`; "selected edges, P" -> "selection P"; "the selected edges form a forest" -> "the selection is a forest". New section **Synonyms** listing every other name in use.
- **00-overview.md.** Sentence 4: "called good, following the main paper (the trees paper says tree matching)". Sentence 8 now says why a forest `Q_s` of a surviving pair is good (the partner). "once that matching is supplied" -> "once that state is supplied". Mermaid: "selection P", "covers with fewest cycles share one sign". **Section "Where the project stands now" rewritten**: stale "disputes the referee's ... phase normalization" replaced by the adjudication (ratio `i^n`); main paper FOLLOWS with v2 in progress; involution note FOLLOWS, edits applied; blueprint counts (4 / 25 / 5 of 34, Lemma 4.7 in Lean); `m` vs `q(s)`; family parameter renamed `j` (was `m`, which clashed); induction does not close (two missing lemmas; G proved without chordless five-cycles, X repairs refuted); two-tree packing proved but blind to states. The trailing "Late review update" paragraph was absorbed.
- **03-states-and-pairs.md.** Incidence graph `B` -> `\mathcal B` with a sentence on the letters; good state definition names its synonyms; Lemma 1 `k` -> `q(s)`; "forest already implies one root per component" now says this holds only with a partner and points to the prism; "2-factor of B" -> "2-factor of the incidence graph `\mathcal B`", distinguished from 2-factors of `G`.
- **04-disk-identity.md.** forest pair -> good pair.
- **05-cancellation.md.** "The cycle cover D(r,s)" -> "The directed cycles D(r,s)", plus the definition of the cover (O's group); `2^k` -> `2^{q(s)}`; cube dimension `k >= 1` -> `q(s) >= 1`; first-use note for tree matching.
- **06-nonvanishing.md.** White faces `w` -> `y` and `h_s` -> `\eta_s` (lines 37 to 156; polynomial variables `w_{t,v}` untouched); new paragraph stating the sign convention against main (`eta`) and inv (`H = -sum eta`, rays only up to a constant per cover); "cycle cover" -> cover (O's group); `c_min` -> `m`; tree matching -> good state with first-use note; "forest" stated as the whole condition only for pairs; **213 objects**: added that the involution note's 279 is the same file and recipe with roots 4 and 5 swapped (a reflection), counts depend on the drawing (69 drawings, 35 values, 103 to 363), signed sum -9 and nine second-fixed objects do not.
- **07-recovery.md.** Title and chain: good pair, selection `P`; Link 3 heading "The selection"; definition sentence says "selected" never refers to `D` here; opening explains why the forest `Q_s` of the pair is good; **non-surjectivity on the prism**: the two cycles not produced fail because a path of opposite edges joins two roots, not because of a cycle (fable atlas review), so "good" must not be read as "a forest".
- **08-gluing-and-hypotheses.md.** tree matching -> good state.
- **09-what-is-still-open.md.** Definitions paragraph: `m` (was c_min), `q(s)`, good state with all three equivalent forms, good pair, `#TM`. Family `T_m` -> `T_j`. Section 6 (packing): CONJECTURE -> PROVED-HERE unreviewed, what it does not give, P2 conjecture with its range. ML2 section: induction-lemmas results (G = ML1, X = ML2). Section 10: M4 dispute replaced by the adjudication; blueprint counts; involution referee; main v2 in progress. "What survives": packing updated.

## digestions/route-map/

- **HOW-IT-WORKS.md.** Good state introduced as the main paper's word with T's and O's names; prism warning adds the two-roots failure; `k` -> `q(s)`; "cycle cover" -> cover (O's group); family exponent `q` -> `j`; cmin -> m; **"Current written routes" rewritten**: wrong 279/213 explanation ("different fixture or convention") replaced by the referee's (same file, roots 4 and 5 swapped, count depends on drawing); M4 settled; involution referee FOLLOWS; blueprint; induction-lemmas; packing; heights described as turn signs along face paths (was "crossing counts").
- **ROUTE-MAP.head.md.** New naming paragraph with link to GLOSSARY#synonyms; "selected edges" -> "selection".
- **ROUTE-MAP.tail.md.** Packing sentence updated.
- **routes.py.** 171 renames by `rename.py`, prism parameter `m` -> `j` in D.families and D.covers, `2^k` -> `2^q(s)` (3 places), "12 tree states" -> "12 good states", "cycle cover" -> cover (3), waypoint SE "Selection P". Appended a "Consistency pass" block: N.li-check (279/213, full paths), G2.primal (M4 settled, cross-audit review), G2.main (v2 in progress, blueprint), G2.inv (refereed FOLLOWS), U.packing (CONJECTURE -> PROVED-HERE, src = packing folder), new U.packing-P2 (CONJECTURE), U.G and U.ML2 (induction-lemmas results), step U freedom text. Route count 226 -> 227.
- **build_map.py.** Figure labels: "perfect matchings of the incidence graph", "Q_s a forest, one root per tree", "only good pairs survive".
- Regenerated: ROUTE-MAP.md, routes.json, route-map*, route-kinds*.

## labyrinth/

- **seed.py.** 45 renames (event lines skipped); `nid()` now uses a `STABLE_ID` table so U.packing keeps node id `k.U.packing` after its status change (an existing event refers to it; same precedent as D.7); status rows `q.structural`, `new-presentations`, `structural`, `review` updated (packing, M4 settled, involution referee, blueprint).
- **make_frontier.py.** Labels renamed (good states, m); the data key `r["cmin"]` was restored after the rename touched it.
- **README.md.** c_min -> m, tree matchings -> good states.
- Regenerated: knowledge.json, sota.json, STATUS.md, frontier.json, scatter.json, dashboard. `lab.py check` ok, `lab.py build` ok.

## digestions/atlas/ (text only)

- pages.py: chain ("some state is good: its opposite edges form three trees, one at each root"), involutions (`k` -> `q`, "A good state has one partner"), sum ("only good states survive"), recovery (good state with the root condition; "selection").
- pages_more.py: 27 renames; rowdep ("three trees, one at each root"; "any state is good"); matroids (forest "with one root in each tree"); produced (the two unproduced cycles: a path of opposite edges joins two roots).
- README.md: tree matchings -> good states, "the selection `P`", word counts synced with manifest.
- Rebuilt atlas.pdf, pages, renders; `verify.py`: all checks passed (`atlas-verify.txt`). Pages 25 and 8 inspected as renders.

## workings/barnette_lab/README.md

- c_min -> m, tree matching -> good state (2 replacements).
