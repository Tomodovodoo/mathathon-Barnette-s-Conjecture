# Changes I could not make myself

For the owners of `paper/main/`, `proofs/` and the atlas figures. I edited none of these files.

## paper/main/barnette.tex, "Consequences and open questions"

The section states no counterexample, range or review status, so only one sentence touches the fact table.

Line 1078 now:

```tex
With these in place of the complex phase and the polynomial of OpenAI's nonvanishing argument, their main theorem compiles unchanged.
```

It is true. A reader may still take it to mean that the formal proof uses no polynomial at all. The rebuilt main theorem reaches 276 general Mathlib `Polynomial` declarations through the unchanged dual construction (`research/2026-11-14_astra_lean-check/REACHABILITY.md`). Suggested wording:

```tex
With these in place of the complex phase and the polynomial of OpenAI's nonvanishing argument, their main theorem compiles unchanged; it still uses general polynomial algebra elsewhere, in the construction of the dual.
```

Nothing else in the section disagrees with FACTS.md. The Remarks section (hexagonal prism, 4 eligible cycles and 2 produced; the 26-vertex example; the 9-vertex double octahedron) agrees as well.

## proofs/

`proofs/lean/README.md` already qualifies "no polynomial" (six named lemmas). `proofs/blueprint/` carries the final 5 / 17 / 10 / 2. I found no sentence in `proofs/` that disagrees with the fact table.

## Atlas (text and one figure)

`digestions/atlas/verify.py` fails at HEAD before any edit of mine: `figs_proofs.py` line 257 raises `KeyError: 'weaker'`, because `proofs/blueprint/blueprint.json` now holds the four-way statuses and the page-29 figure maps only the old three. So I could not rebuild the atlas, and I left its texts alone so that the source and the PDF stay in step. What the owner needs to do:

1. Figure of page 29: read `analysis.status_counts_skeleton` (5 exact, 17 translation, 10 weaker, 2 none) and add a fill for "weaker"; update the two checks in `verify.py` lines 46 and 47.
2. Text of page 29 (`pages_more.py`, page `blueprint`). Replace "Four match a Lean declaration exactly. Twenty-five match only after a translation, and five have no counterpart." and "A later Lean version follows the paper's sign and finite-difference route. With it a second model counts 5, 27 and 2." by: "Five match a Lean declaration exactly, seventeen match after a translation, ten have only a weaker or different counterpart and two have none. These counts include a later Lean version that follows the paper's sign and finite-difference route, rebuilt and checked by a second model."
3. Status of page 26 (`families`). Replace "a second model rebuilt their proofs independently" by "a second run of the author's model checked them for every length, and a different model confirmed the counts on finite ranges".
4. Page 30 (`open`). The pair-descent bar is drawn from the check through 16. The independent check now reaches 20 (3,373,400 pairs, `research/2026-11-14_astra_referee-descent/REPORT.md`). Redraw the bar and change the sources note "descent on all 24,744 pairs through 16" to add the descent referee through 20.
