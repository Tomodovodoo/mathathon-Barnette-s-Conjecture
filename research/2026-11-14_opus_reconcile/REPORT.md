# Report: reconciling the five summaries

1. FACTS.md has the fact table: about forty facts, one row each, with the value in each document, the authority and a verdict.
2. Fourteen disagreements were fixed at their source: in routes.py and seed.py (map, sota and dashboard rebuilt; `lab.py check` ok), and in SYNTHESIS.md, 09, HOW-IT-WORKS.md and the labyrinth README.
3. The main errors were stale review states (packing, families, algebra, descent, Lean), the unscoped sign-gauge claim, the independent C3 range (20, not 16 or 19) and the first nonreal zeros (9, not 10 or 12).
4. The atlas cannot be rebuilt: `verify.py` fails at HEAD on the page-29 figure, because the blueprint now has four statuses. PAPER-FIXES.md has the fix and the text for pages 26, 29 and 30.
5. The paper's closing section agrees with the table. PAPER-FIXES.md proposes one optional clause on what "no polynomial" covers.

Opus 5.5, 2026-11-14. No subagents.

## What I set out to do

Make SYNTHESIS.md, steps 00 and 09, the route map with HOW-IT-WORKS and sota.json, the atlas's last pages and the paper's closing section agree with each other and with the final referee reports, and propagate corrections (a) to (g) of the brief.

## What I established

- Fact table (FACTS.md). Most counterexample sizes already agreed across documents: lattice of states 10 (whole lattice) and 12 (highest partnered state), pair lattice 18, R2 33, bad cover 16, lift 18, LP 13, strict descent 8 / 16, walk 38, levels 18. The pair-lattice "first at 18" is justified by Sol's all-root census through 18.
- Disagreements found and fixed (CHANGELOG.md): sign gauge (correction a) in SYNTHESIS and the map; prism-chain count (b) now given with its rule in the map; tube recurrences (c) in the map, sota and HOW-IT-WORKS; same-model reviews (d) in SYNTHESIS, 09 and the map; "no polynomial" (e) in HOW-IT-WORKS; Step R and sign-free evenness (f) in SYNTHESIS, HOW-IT-WORKS and sota; independent C3 range 20; lookahead minimality; first nonreal zeros at 9; mean obstruction wording; mod 11 not replayed.
- Counts rerun (COMPUTED, `synthesis-audit/count.py`, output `synthesis-audit/counts.json` and `count-output.txt`): 80 run folders, 77 with a report, 246 routes, 77 refuted, atlas 34 pages, paper 20 pages. `check.py` passes: 117 links, no problem. A link check over the other edited Markdown files finds no broken link.
- Same-model reviews: Sol on the Sol families and probability reports, Opus on the Opus packing report, Astra on Astra's partial G. The first now also has a different-model check (Fable).

## What failed or was not done

- Atlas. `digestions/atlas/verify.py` stops with `KeyError: 'weaker'` in `figs_proofs.py` line 257 before any edit of mine, because `proofs/blueprint/blueprint.json` was rebuilt with four statuses after the atlas. Fixing that means changing a figure, which this brief does not allow. I left the atlas texts unchanged so that `pages_more.py` and atlas.pdf stay in step, and wrote the needed changes in PAPER-FIXES.md.
- `research/2026-11-14_astra_referee-descent/` was still being edited while I worked (uncommitted). I used its working-tree text; if its final numbers change, rows C3 and lookahead of FACTS.md need a second look.
- I did not reread the step files 01 to 08 or the dashboard HTML beyond the build.

## Still open

- The atlas's page-29 figure and the page-30 descent bar.
- `research/INDEX.md` still says 244 routes for the map runs; the map has 246.

## Next steps

1. Atlas owner: apply PAPER-FIXES.md (atlas section), rebuild, run `verify.py`.
2. Paper owner: decide on the one-clause Lean qualification.
3. After `astra_referee-descent` and `fable_sign-free-note` finish, rerun `synthesis-audit/count.py` and `inventory.py`, and recheck the C3 rows.

## Leads for others

- Coordinator: INDEX.md rows for `astra_lean-check` ("running") and `fable_final-polish` ("running") are out of date.
