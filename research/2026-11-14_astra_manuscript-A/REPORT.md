# Report: manuscript A

1. Delivered a complete 11-page LaTeX exposition and compiled PDF in paper/draft-A.
2. PROVED-HERE: the main route uses the verified height-product count, with the disk identity and all recovery and gluing steps proved.
3. COMPUTED: both supplied examples and the revised figure examples were checked with barnette_lab; the larger example shows two cyclic pairs cancelling and six forest pairs surviving.
4. The reverse-Lamport audit concludes FOLLOWS for the draft's prescribed-edge theorem; the referee's relevant corrections were incorporated.
5. The final build has no errors, undefined references or overfull boxes; every PDF page was rendered and visually inspected.

## What I set out to do

Write the first complete, rigorous, self-contained exposition of OpenAI's proof, following the requested dependency order, running examples, source attribution, layout and ownership rules. Owned paths are research/2026-11-14_astra_manuscript-A and paper/draft-A. Shared figure PDFs were read and referenced, never edited or rebuilt by this task.

## What I established

PROVED-HERE. paper/draft-A/barnette.tex contains the full route: simple dual triangulation; the forest certificate; states and partner orientations; no-separator density and integral flow; disk identity as one excess white face; fixed-second-state cancellation; the product-of-heights nonvanishing count for arbitrary minimum cycle count; the white-face tree; selected-side acyclicity and inducedness; compatible gluing; prescribed-edge Hamiltonicity. AUDIT.md records the bounded conclusion-first AND graph, its exact side conditions and a dependency table. The verdict is about this proof route, with human review pending.

LIT. The original proof is credited to OpenAI. Stein and Alt--Payne--Schmidt--Wood receive the dual induced-tree attribution; Kelmans and Hertel the strengthening/reduction context; Tutte and Hine--Kalman the states attribution. Li and the unsigned constructive manuscript are distinguished. The unpublished Fable note receives explicit credit for the adopted height and disk simplifications. No auxiliary conjecture or experimental claim is promoted to a theorem.

COMPUTED. examples.py checks four explicitly named input configurations: the two reference JSON exports, the figure octahedron, and the figure 13-vertex triangulation. The latter has 12 states and eight ordered disjoint pairs, six forest pairs and two cyclic pairs, with minimum D-cycle count two. It verifies the displayed reversal, J values 0 and -2, disk counts (B,W,I,h,l)=(5,6,3,7,2), recovery and the four-term nested height identity. Full commands are in CHOICES.md and the scripts' docstrings; outputs are in examples.json. This is finite verification, not the proof of the general theorem.

COMPUTED. build.py produces the final PDF and page PNGs. The clean final log has no TeX errors, undefined citations or references, or overfull boxes. build-check.json pins the manuscript, bibliography, PDF and every shared figure consumed. The eight figures consist of seven read-only shared PDFs and one local TikZ schematic. Rendered PNGs and intermediate TeX files are ignored reproducible QA artifacts.

## What failed and why

The initial long PowerShell authoring command exceeded Windows' process command-line limit. Writing the source in smaller patches resolved it without changing the intended proof.

The first 11pt layout let figures float above their definitions and made some shared figure labels smaller than the document's footnote font. The final 10pt amsart layout uses flafter, needspace and natural-size-compatible figure widths. All pages were inspected again.

No proposed mathematical simplification used in the draft failed the independent check. The exponential fallback was therefore unnecessary. The determinant route was omitted because it adds machinery without replacing the nonvanishing argument; the stronger separator obstruction and algorithmic conclusions were also outside the chosen existence contract.

## What is still open

HUNCH. Whether this is clearer to a reader unfamiliar with the original papers needs human reading. The signed path convention is the part most likely to need a spoken explanation or another small local figure.

The main paper makes no complexity claim and does not try to derive nonvanishing from a determinant. Those are separate research questions, not gaps in its existence proof.

Source limitations: I read the supplied texts and inspected selected PDF pages containing the central formulas. Historical attributions use the provided literature investigation and bibliographic data; I did not independently reopen every historical original. No assertion of journal acceptance or a newly replayed Lean proof appears in the manuscript.

Shared figures are being revised independently. A later change to their combinatorial labels requires rerunning examples.py and the build; the hashes in build-check.json identify the versions inspected here.

## Three best next steps

1. Have a human read Sections 2 and 4 without the source papers and explain why the second state and the product of heights are necessary.
2. Compare this complete route with the other draft at the level of proof obligations and definition placement before merging prose.
3. Freeze the final shared figures, rerun the example and layout commands, and decide the public authorship and citation form for the unpublished project height note.

## Leads for others

The larger shared example is better than the cube for explaining the count: its two nested cycles require two factors, and the increment product is (b1+u)(b2+u+v). The alternating sum is exactly one. The manuscript supplies a corrected cyclic-Q caption using triangle 1,8,9 rather than the obsolete length-six description encountered in the shared caption file.

## Deliverables and reproduction

- paper/draft-A/barnette.tex, barnette.pdf, refs.bib, figures/height.tex.
- This folder: AUDIT.md, CHOICES.md, REPORT.md, examples.py, examples.json, build.py, build-check.json.
- From the repository root, run `python research/2026-11-14_astra_manuscript-A/examples.py` and then `python research/2026-11-14_astra_manuscript-A/build.py`.

Commits were restricted to the two owned paths. The final push outcome is recorded in the completion message.
