# Report: consistency edits

1. The digestions, route map, labyrinth, atlas texts and lab README now use one name per object, taken from the main paper: good state, good pair, cover, `m`, `q(s)`, `\mathcal B`, selection `P`, `\eta_s(y)`. GLOSSARY.md has a new Synonyms section listing every other name.
2. Every place where "forest" stood for the full condition now says "a forest with one root in each component", or explains that a partner makes the two the same. The prism's two unproduced cycles are described correctly in step 07, HOW-IT-WORKS and atlas page 25: a path of opposite edges joins two roots, and there is no cycle.
3. Stale statements fixed: the phase question is settled (ratio `i^n`); 279 versus 213 is the same file with roots 4 and 5 swapped; packing proved but blind to states; induction still open (G partly proved, X repairs refuted); blueprint coverage 4/25/5 of 34; main and involution referees FOLLOWS.
4. Regenerated: ROUTE-MAP.md and figures (227 routes), labyrinth (`lab.py check` ok, `lab.py build` ok), atlas.pdf (`verify.py` all checks passed).
5. Link check: 323 relative links and backticked paths in digestions/ and the READMEs, 2 broken, both in digestions/SYNTHESIS.md, which I do not own. All 327 file paths in the route catalogue resolve.

## What I set out to do

Apply the convention of `research/2026-11-14_opus_cross-audit/CONSISTENCY.md` to the files I own (digestions/steps, digestions/route-map, labyrinth, atlas text, workings/barnette_lab/README.md). Fix the two stale statements it found and any others the late runs had overtaken. Regenerate everything generated, check links, and remove AI tells from the prose I touched. The main paper's v2 had not landed (no REPORT.md in `research/2026-11-14_astra_main-revision/`), so I used `paper/main/barnette.tex` as of today and its NOTATION.md.

## What I established

Document by document details are in `CHANGELOG.md`. These are editorial changes. The only mathematical claims are statements about other folders' results, and each one names its source.

- **Convention.** I used CONSISTENCY section 4 with one deviation. It proposes `I` for the incidence graph, but the main paper uses `I` for the number of vertices inside a disk and writes the incidence graph as `\mathcal B` (NOTATION.md). I followed the main paper: `\mathcal B` for the incidence graph, plain `B` only for the disk count. `#TM` stays as the symbol for the number of good states, because the census files use it; GLOSSARY and step 09 define it.
- **Heights.** Step 06 now uses the main paper's letters `\eta_s(y)`. It has one paragraph on signs. The digestions' crossing height and the main paper's turn-sign height both rise by one when a cycle around `y` turns counterclockwise, and they differ only by constants. The involution note's `H(s)` is `-\sum_y \eta_s(y)`, which has the opposite sign. I checked the direction against step 06's Lemma H and against main's statement that `\omega` rises by `L(C)` from clockwise to counterclockwise.
- **Letter clashes found while editing.** These were not in CONSISTENCY. A family parameter `m` in 00, 09 and two routes (`T_m` with `c_min = m - 1`) would have read "m = m - 1" after the rename, so I renamed the parameter to `j`. The rarity family's `2^q` among `3^q` in HOW-IT-WORKS clashed with `q(s)` and is now `j`. The cube dimension `k` in step 05 is now `q(s)`. The atlas involutions page used `k` for `Q_s` cycles and now uses `q`.
- **Labyrinth id stability.** U.packing changed from CONJECTURE to PROVED-HERE. Node ids carry the status prefix, and an existing event refers to `k.U.packing`. So `seed.py` now keeps first ids in a `STABLE_ID` table, following the existing D.7 special case.
- **Scripts.** `rename.py` (the term rename, with its per-file counts in `rename-output.txt`), `heights06.py`, `sub.py` (exact one-match substitutions), `linkcheck.py` (output `linkcheck-output.txt`) and `wherecheck.py` (route catalogue paths, `wherecheck-output.txt`). `rename.py` and `heights06.py` are one-shot and must not be rerun. The other three can be run again.

## What failed and why

- The first run of `rename.py` matched `\bcmin\b` inside the data key `r["cmin"]` in `make_frontier.py`. I restored it before any rebuild.
- The atlas has a hard word limit of 150 per page. Writing out the root condition pushed pages 8 and 25 over it, and I trimmed both twice.
- **Atlas figures still say "tree matching" and "tree pair"** in labels drawn inside the figures (`figs_algebra.py` 131 to 151, `figs_order.py` 79, 109, 130 to 133, 177, 256, `figs_scope.py` 73 to 95, 299, 426, 588 to 633, 763). Page 25 shows "tree matching" under two panels while its text says "good". The brief excluded redrawing figures, so I left them for the atlas owner.

## Edits proposed by CONSISTENCY.md that I did not apply (folders I do not own)

paper/main/barnette.tex:
- At the definition of good (line 329): "In the digestions before 2026-11-14 and in the constructive paper a good state is called a tree matching."
- Remark on the phase (around line 815, optional): "Lean's phase is the same `i^J` when its corner order matches; the real sign divided by it is `i^n`."

proofs/involutions/ (involutions.tex and INVOLUTIONS.md):
- "forest pair" -> "good pair" (still present, for example INVOLUTIONS.md lines 17 and 79).
- Where `H(s) = -\sum_w \eta_s(w) = -\omega(s)` is introduced: say explicitly that `H` has the opposite sign to the main paper's weight, or define `H = \omega` and flip the sign statements.
- Use `m` rather than `c_min` where the note still says `c_min`, and "cover" for the unoriented class.

proofs/primal/ (left as a proposal by the cross-audit):
- PRIMAL-PROOF.md Lemma 8 and Section 6: "selects" / "selected edge" for the edges of `D` -> "marks" / "marked edge", so that "selected" only refers to the matching `P`.

## Leads for others

- `digestions/SYNTHESIS.md` line 3 links to `research/2026-11-14_fable_synthesis-audit/FACT-CHECK.md` and `CHANGELOG.md`, which do not exist yet.
- `digestions/atlas/proposed/` is untracked and not mine; I left it alone.
- The census files and the scatter still use `cmin` and `TM` as data keys. That is fine, but a reader of the JSON needs the GLOSSARY synonyms table.

## What is still open

- The atlas figure labels listed above.
- The paper/ and proofs/ edits listed above.
- No human has read the edited documents. I re-read the changed passages but did not reread all 26,000 words of the steps.

## Three best next steps

1. The atlas owner changes the figure labels to "good state" and "good pair" and rebuilds (about 25 strings, no geometry).
2. When main v2 lands, diff its terminology against GLOSSARY's Synonyms table and update the table, plus HOW-IT-WORKS's description of the heights if v2 changes them.
3. Apply the involution-note renames ("good pair", the sign of `H`) in the next revision of proofs/involutions/, then remove that row of exceptions from GLOSSARY.

Opus 5.5, 2026-11-14. Folder `research/2026-11-14_opus_consistency-edits/`. No subagents.
