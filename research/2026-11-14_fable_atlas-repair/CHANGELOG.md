# Changelog, atlas repair pass

Fable 5.2, 2026-11-14. All edits are inside `digestions/atlas/`. Authorities: `research/2026-11-14_opus_reconcile/FACTS.md` and `PAPER-FIXES.md`, plus the reports they name.

Commands, from the repository root:

```powershell
python digestions/atlas/build.py blueprint open families   # recompiles figures 29 and 30, then the whole atlas
python digestions/atlas/verify.py                           # checked 30 routes, 34 pages: all checks passed
```

`build.py` calls `pdflatex` directly, so the MiKTeX update prompt of `latexmk` never came up. The README now says so.

## Page 29, "What is machine-checked"

Figure (`figs_proofs.py`, `blueprint_fig`).

- Reads the four-way status of `proofs/blueprint/blueprint.json` directly. The old three-way mapping raised `KeyError: 'weaker'`.
- Asserts 5 exact, 17 translation, 10 weaker, 2 none, that this equals `analysis.status_counts_skeleton`, that the two with no counterpart are `lem:connected` and `prop:target.2`, and that every weaker statement records what is missing.
- New assertion: the advisory recount in `research/2026-11-14_astra_lean-check/recount.json` (5, 27, 2) is the same classification with "translation" and "weaker" merged, statement by statement.
- Four encodings by fill and outline: dark fill (exact), grey fill (translation), white with a 1.5pt outline (weaker or different), white with a dashed outline (none). The ringed dots of the old recount are gone.
- Legend and bar (b) carry direct labels with counts: "5 exact", "17 after an unformalised translation", "10 weaker or different", "2" with "no counterpart" under it.
- Figure size 14.79 x 17.22 cm, 0.929 of the text width (was 14.78 x 16.85).

Text and status (`pages_more.py`). 150 words (was 149).

- "Four match ... Twenty-five ... five have no counterpart" and "a second model counts 5, 27 and 2" replaced by the wording of PAPER-FIXES item 2.
- New sentence pair on the polynomial: the main theorem avoids six named lemmas of OpenAI's phase and polynomial argument, and the dual construction still uses general polynomial algebra. Source: `proofs/lean/README.md` line 10 and `astra_lean-check/REACHABILITY.md` (276 general Mathlib `Polynomial` declarations still reached).
- Status now says one model made the blueprint and its four-way count, and that the second model's recount has three classes and agrees. "Nothing in this atlas is checked in Lean" moved from the text into the status.
- Sources: added `opus_lean-integration/STATUS-TABLE.md` and `astra_lean-check/REACHABILITY.md`.

`verify.py`: the two blueprint checks now expect the four-way counts and the merged recount; a third check compares the lengths of the four lists with the counts.

## Page 30, "What is still open, and how far it was tested"

Chart (`figs_scope.py`, `open_fig`).

| Bar | Before (two programs, one program) | After | Authority |
| --- | --- | --- | --- |
| pair descent (C3) | none, 16 | 20, 23 | `astra_referee-descent/REPORT.md` and `INTEGRATION.md`: 3,373,400 pairs through 20. `fable_descent/REPORT.md`: 193,623,384 pairs through 23 |
| rainbow descent (Step X) | none, 17 | 12, 17 | `opus_referee-rainbow/REPORT.md` item 5: reproduced for V <= 12 with its own code. FACTS row "Step X" |

- The C3 bar is relabelled "pair descent that never adds a cycle reaches a good pair". The old label, "greedy descent in the lattice reaches a good state", described neither the objects (pairs) nor the rule (the number of cycles of `Q_s` never goes up).
- Checked against FACTS and left unchanged: counting bound 22 and 22; without separating triangles 16 and 24; contraction keeps a pair 17 and 19; contraction count 17 and 18; crosses at 12, 18, 18, 24, 33, 33, 33, 38; samples to 100, 150, 120.
- A new assertion pins the six (two-program, one-program) ranges.

Text and status. 149 words (unchanged count).

- New sentence with both C3 figures: author's census 193,623,384 pairs up to 23, another model's program 3,373,400 pairs up to 20.
- Status says "the other models that repeated them" in place of "the second models".
- Sources: Sol's note now gives both of its counts (9,531,638 roots, of which 4,656,948 have a pair). Added `fable_descent/REPORT.md`, `astra_referee-descent/REPORT.md`, `opus_referee-rainbow/REPORT.md`.

## Page 26, "Two families, counted"

Status: "a second model rebuilt their proofs independently" replaced by "A second run of the author's model checked them for every length, and a different model confirmed the counts on finite ranges" (PAPER-FIXES item 3, FACTS row "Tube recurrences"). Four sentences of the text were shortened to stay at 149 words. No mathematical content changed and the figure is untouched. Sources: the same-model referee is named as such and `fable_referee-families/` is added.

## Sign gauge

No page text, caption, figure or README sentence of the atlas mentions a sign gauge, so there was nothing to correct. I searched `pages.py`, `pages_more.py`, the five figure scripts and the README for "gauge".

## Sources pages and README

The three sources pages reflowed because pages 26, 29 and 30 list more sources. The atlas still has 34 pages. README: repair-pass paragraph, the `pdflatex` note, the page-29 encodings, two "still schematic" bullets and the index row of page 29.

## Renders

`before/` and `after/` hold pages 26, 29, 30 and the three sources pages at 110 dpi. `after/29-blueprint-grey.png` and `after/30-open-grey.png` are greyscale renders.
