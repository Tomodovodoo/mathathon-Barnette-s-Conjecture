# Report: blueprint of the proofs

1. `proofs/blueprint/` now holds a statement-level blueprint: 38 nodes from the merged paper, 17 from the primal note, 7 from the involution note and 105 Lean declarations, with `uses` and `corresponds-to` edges, a layered dependency graph and a five-column chart (COMPUTED, scripts in `scripts/`).
2. Of the 34 nodes on the route to Theorem 1.1, 4 have an exact Lean counterpart and 25 a counterpart in different form. Five have none: Lemma 2.2, Prop. 2.6(2), the component count of Lemma 3.7, Lemma 4.4 (the sign) and Lemma 4.7 (finite differences).
3. Lemma 4.7 is now proved in Lean 4 with Mathlib, 90 lines, first compile; the axioms are the standard three (COMPUTED, `lean/FiniteDifference.lean`, `lean/FiniteDifference.out`).
4. Statements match far more often than proofs do. Only ten of the paper's proofs follow the Lean's argument, and Theorem 6.2's gluing rests on Prop. 2.6(2), which is not formalised.
5. Nothing is used before it is proved. Four items are never used for Theorem 1.1. Formalising the paper's route on the Lean's algebraic model would take 530 to 710 new lines (HUNCH, by analogy), 90 of which now exist.

## What I set out to do

The brief asked for a Lean-style blueprint connecting the merged paper, the primal note, the involution note, the OpenAI paper and the Lean proof at `4eaee875`, statement by statement. It also asked for an honest account of which statements of the merged paper are machine-checked, a feasibility note on formalising the merged route, and, if feasible in under thirty minutes, a small Lean lemma.

## What I established

**Extraction** (COMPUTED). `scripts/extract_tex.py` reads the three TeX sources with `git show` at commit `b0fc398`. It extracts every theorem-like environment, its number (recomputed with the shared equation counter, which matches `barnette.aux` for the working-tree build), its proof, the labels cited in it and the proof length. It also extracts six claims made in running text that later proofs use: two faces share at most one side, the inside of `Z`, `D(r,s)`, `delta`, heights, and the max-flow paragraph. The primal note's run-in headings ("Lemma 5, ...") and the involution note's amsthm labels are handled separately. Output: `data/statements-*.json`.

**Lean headers** (COMPUTED). `scripts/lean_sigs.py` reads the 31 files of my own clone at `4eaee875` and writes the header of all 689 declarations it finds to `data/lean-sigs.json`. Every Lean name cited in `proofs/blueprint/` resolves there to a file, line and header.

**Curation** (PROVED-HERE in the sense of a reading; no new mathematics). `scripts/curation.py` holds, for each merged-paper statement:
- its final uses, including those the proof makes without `\ref`;
- the OpenAI, primal and involution counterparts;
- the Lean declarations, their relation and whether the used part is covered;
- the translation (bridge) needed, or, for uncovered statements, the nearest lemma and the distance.

I read every proof of the merged paper to add the uses that have no `\ref`. The build script checks that every cited label is among the curated uses; it reports none missing.

**Findings from the reading.**
- The verification answer, in numbers: 4 exact, 25 different form, 5 none on the route; 90% of the route's proof words sit in statements with a counterpart. The 25 rest on five informal translations, B1 to B5 in BLUEPRINT.md.
- Lemma 4.4 (the sign as a product of local signs) is exactly the translation that would let Lean's phase-based cancellation stand for the paper's. It is the most useful missing piece.
- The heights are covered by the Lean in summed form. A path flow is one of the flows `whiteCharge_cut_integral` quantifies over, so the "heights along face paths" simplification is a special case of the Lean device, not a different one. The per-white-face jump of Lemma 4.6 is stronger than anything in the Lean, and the route never needs it.
- Theorem 6.2 has a checked statement but an unchecked proof. Its gluing uses the two-tree Prop. 2.6(2); the Lean glues matchings instead. If the paper glued matchings, Prop. 2.6(2) and Lemma 3.1 could move to the remarks.
- Implicit uses: Prop. 3.9 cites the disk identity by name only. The heights paragraph needs `G` connected for an arbitrary coloured triangulation, which is Lemma 2.5(2) with `N` empty and is not said. The inside paragraph calls the outside of `Z` "an open disk" (Schoenflies) where Jordan suffices.
- Order: nothing used before it is proved. Lemma 3.1 precedes Definition 3.2 but does not use it.
- Never used for Theorem 1.1: Lemma 3.1, Remark 4.10, the two proved remarks of Section 7, plus several parts of statements (partner uniqueness, converse of Lemma 3.5, regrouped formula of Lemma 4.5, per-face heights).

**Graphs** (COMPUTED). Graphviz 16.1.1 installed with winget. `blueprint.pdf` is the transitive reduction of the uses graph, layered by depth, fill by status, border by section. Section clusters made long crossing edges, so I dropped them after the first render. `columns.pdf` is the five-column chart with 18 waypoints.

**Lean** (COMPUTED). `lean/FiniteDifference.lean` proves Lemma 4.7 for any finite index set over any commutative ring (`Blueprint.finite_difference`) and in the paper's `Fin c` form (`Blueprint.finite_difference_fin`). It was compiled with Lean v4.34.1 and Mathlib `d13f23b7` in the existing Mathlib-only project at `E:\lbb`, with `~/.elan/bin/lake env lean`. Wall time was 112 s, almost all of it loading Mathlib. `#print axioms` gives `[propext, Classical.choice, Quot.sound]`. Standalone; it does not import the OpenAI files.

**Version drift.** During the session other agents edited `paper/main/barnette.tex` and `proofs/involutions/involutions.tex` in the working tree (uncommitted). I pinned the extraction to the committed, refereed text. With `--worktree`, the paper has the same 31 numbered statements and numbers; the changes are notation and self-contained restatements of Lemmas 3.7 and 3.8. The involution note gains an off-route statement. The involution referee finished during the session (FOLLOWS, `45c4cea`), so I marked the involution statements as refereed.

## What failed and why

- The first `lake env lean` call used the `lake` on the Git Bash PATH (`/c/Users/Tom/bin/lake`), which could not parse Mathlib's `lakefile.lean`. Calling elan's `lake` worked.
- My first header scanner ran past a `def` with pattern-matching equations and swallowed the next declaration (`cap_coloring`). Fixed by stopping at the next column-0 declaration.
- I did not attempt the sign identity (Lemma 4.4) in Lean. It needs the OpenAI development's `TriangleSystem` and a build of all 31 files, more than the thirty minutes the brief allows.
- I did not rebuild the OpenAI Lean development. "Machine-checked" relies on the earlier build in `research/2026-11-14_opus_lean-formalisation/build/`.

## What is still open

- The five translations B1 to B5 are informal. B2 (sign = `i^n` times phase) and B3 (heights = weights of a path flow) are short and would turn several "different form" entries into checked ones.
- Whether the paper should switch its gluing to the Lean's matching gluing. That would remove Prop. 2.6(2) from the route, and with it one of the five uncovered statements.
- The relation column is my reading of statements against headers. A second reader should check the 25 "different form" entries, especially Lemma 3.6, where the Lean proves existence by Hall and the paper constructs `P_s`.

## Three best next steps

1. Formalise steps 2 to 4 of `proofs/blueprint/FORMALISATION.md` (sign, path flow, `omega^m` nonvanishing) against the OpenAI files, ending with a second proof of `ColoredDual.forest_pair`. Then the merged paper's Section 4 would be machine-checked on its own route.
2. Decide the gluing question in the paper (see `BLUEPRINT.md`, "Proved but not used"), and add the three implicit uses listed above as explicit references.
3. Rerun the extraction on the next committed version of the paper (`extract_tex.py` with the new commit as `REV`, then `build_blueprint.py`), so the blueprint tracks the text that the referees read.

## Leads for others

- The involution referee found a sign error in the off-route Section 7 identity of `proofs/involutions/` (see their REPORT). The blueprint does not depend on it.
- Remark 4.10 of the merged paper still calls `sum eps z^omega` an integer polynomial; the merged-paper referee showed it is a Laurent polynomial.
