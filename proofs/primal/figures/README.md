# Primal figure sources

Run `python proofs/primal/figures/check.py --build` from the repository root. The command computes and asserts every drawn object, writes eight TikZ bodies and standalone sources, compiles PDFs, and renders PNGs. `checked.json` records the main data; `captions.json` supplies the note captions.

Every panel is an actual drawing of G on the shared dual-derived layout. State segments join black vertices to face labels. Colours, dashes, vertex fills and edge weights come from paper/figures/barnette-figs.sty. Each panel occupies 0.48 textwidth and retains native footnote-size labels. The shared toolkit is read-only.

The primal graph conversion and four-count, flux, tree and matching assertions use the independent referee's PG and Rooted routines. The gluing example is computed by the shared toolkit and checked again for a nontrivial three-edge cut and cube caps. No drawing is a proof of its general lemma.
