The finishing pass keeps all fifteen original filenames and adds the six-panel introduction strip.
White-tree edges are short midpoint arcs; sampled crossing checks pass on both displayed examples.
COMPUTED: the circulation identity passes for 322 rooted lab instances, 1,784 pairs and 2,320 D-cycle occurrences.
All sixteen figures were inspected in colour, greyscale and deuteranopia simulation; the gallery has nine pages.
The remaining limits are sampled geometry, small introduction panels and no general proof of the circulation refinement.

# Finishing report

## What I set out to do

Finish the second-pass figures in paper/figures while preserving every manuscript-facing filename. I took ownership of that folder and wrote review evidence only here. Neither manuscript draft nor any other research folder was edited. I read the repository brief, README, both previous reviews, the historical figure style, the unslop skill and the original PDF. I inspected the source PDF pages containing Lemma 5.3, the detour and the recovery argument.

## What I established

COMPUTED, paper/figures/check.py and geometry_check.py. On the running triangulation and octahedron, every sampled G edge crosses exactly its own T edge once; every sampled white-tree edge crosses exactly its deleted spoke once. Every other spoke, including the exterior ones, is tested. Each cubic has 160 sample intervals and exterior arcs 360. The validator uses the rounded controls emitted to TikZ. The minimum measured crossing angles are in geometry-validation.json. This is numerical validation of these drawings.

The white tree uses one explicit midpoint join, rather than detouring through two unnecessary triangle-side waypoints. White centres are incentres. For a circular-sided face, that means the largest disk inside the actual region, not the straight chord triangle. Figures 12 and 13 share these paths; the other uses of the same tree share them too.

The cube now uses concentric squares. Its octahedral dual is shown separately, without repeating the below-picture cube vertex. The complete worked construction and its caption occupy about half a text page. Figure 16 adds the proof strip at full text width. The gallery uses explicit nonfloating page groups, body text and no blank pages.

COMPUTED, proofs.py and caption-audit.json. Captions 2 through 16 occupy three to five rendered lines. The cube caption is the worked-example exception, at eight lines. Caption numbers for vertex, face, flow, cycle and cap counts are covered by assertions in check.py and model.recover. Cross-references refer to the fixed sequence. Shared notation is retained; recovery from the original pair is explicitly the swapped pair (s,r).

COMPUTED, paper/figures/audit.py and style-audit.json. The inventory covers all sixteen generated body sources and their standalone wrappers, draw.py and barnette-figs.sty, plus font sizes in all sixteen standalone PDFs. Source labels use footnotesize. Smaller rendered glyphs are standard math scripts, fractions and display limits. The historical first-pass style has several known differences from the accepted second pass; the inventory lists them rather than silently reverting the improvements. Face-centre G dots were standardized to 1.5pt.

I inspected all before and after renders and both accessibility conversions. Outlined versus filled choices, single versus double incidence edges, solid versus dashed graph edges, and black disks versus hollow squares remain distinguishable. The palette did not need a change. The proofs are raster inspection copies; all manuscript outputs remain vector PDFs.

COMPUTED, check_hunch.py and hunch-results.json. L+(C)-L-(C)=W(C) holds with the lab's exact integer unit-circulation weights for every D cycle in every ordered pair on every outer-face choice of every stored JSON lab instance, the four named graphs, and generated(12). The range is 322 rooted instances, 1,784 ordered pairs, 2,320 cycle occurrences, 6 to 26 vertices in T. Duplicate provenance entries remain in the counts. Figure 11 labels its two regions by the separately checked running-example counts.

HUNCH, general refinement. The finite test does not establish the identity for arbitrary instances, especially the componentwise interpretation when H0 is disconnected. The general statement remains a proof obligation.

LIT. The proof dependencies and detour construction follow OpenAI, Paired states and Hamiltonian cycles in cubic bipartite planar graphs, September 24, 2026, Sections 2 to 7, especially Lemma 5.3 and equations 5.3 to 5.5. The local PDF was opened directly. No external source was needed.

## What failed and why

A first route retained side-midpoint waypoints and still wandered. Removing those waypoints gave the short white-tree arcs. A straight-triangle incentre on an outer circular face could lie outside the actual face; the numerical crossing test caught that error. I replaced it by the curved-region incentre. Long Bezier handles initially crossed extra edges; the checker rejected them before a commit. The accepted handles pass all recorded crossing tests.

Float placement still left a small figure alone after the worked example. Explicit page groups fixed that. The groups are [1], [2,3], [4,5], [6,7], [8,9], [10,11], [12,13], [14,15], [16]. The worked example and introduction strip have their own context pages.

## Still open

A sampled intersection test is not a symbolic certificate. The introduction strip is small; its explanations and the detailed sequence are needed to read individual choices. I did not run a physical printer test. The cube and its dual use different plane embeddings rather than an overlay. The two manuscript drafts may need placement adjustments, but were outside my ownership.

## Reproduction

Run from the repository root:

```powershell
python paper/figures/build.py
python paper/figures/crosscheck_lab.py
python research/2026-11-14_sol_figures-polish/check_hunch.py > research/2026-11-14_sol_figures-polish/hunch-run.txt
python research/2026-11-14_sol_figures-polish/proofs.py
```

The full build runs all object and geometry assertions, writes checked.json, validation.json and geometry-validation.json, draws and compiles the figures and gallery, renders PNGs with PyMuPDF and writes style-audit.json. proofs.py writes after images, greyscale and deuteranopia images and PDFs, contact sheets and caption-audit.json. capture_before.py reproduces the initial images and source-PDF extracts from the parent of commit cc6d9e3. REVIEW.md links every before and after image.

## Three best next steps

1. Have the manuscript owners place Figure 16 near the introduction and include the detailed figures at natural size.
2. Prove or refute the circulation refinement for arbitrary components of H0, keeping the finite evidence separate.
3. If the figures are rescaled or rerouted, rerun the rendered font, caption and crossing audits and inspect a physical greyscale print.

## Leads for others

The complete finite circulation table is hunch-results.json. It includes rootings with no pair, which contribute no cycle checks. This distinction matters when quoting the checked range.
