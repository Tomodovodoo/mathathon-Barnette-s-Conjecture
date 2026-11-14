# Change log: final polish of the three written proofs

Claude Fable 5.2, 14 November 2026. No statement or proof step changes meaning in any of the three documents. Where an edit touches a sentence of a proof, the entry says what was added.

Renders. `renders/before/` and `renders/after/` hold every page of the three PDFs at 50 dpi (`barnette-pNN.png`, `primal-pNN.png`, `involutions-pNN.png`) and the changed figures at 110 to 150 dpi. `render.py`, `render_figs.py` and `contact.py` made them.

Patch scripts. `patch_draw_labels.py`, `patch_flow.py`, `patch_involutions.py`, `patch_primal.py` and its three follow-ups are the exact substitutions that were applied. They are a record and must not be run again.

## A. Main paper, `paper/main/barnette.tex` (19 pages before, 20 after)

| # | Where | Before | After |
| --- | --- | --- | --- |
| A1 | Figure 2 (`03-dual`) | labels 6, 7 and 11 on vertices of G, label 5 cut into the collar | every label on white, clear of all drawn objects; drawn at unit 0.9 and set at `0.69\textwidth` (was `0.62`). `before/03-dual.png`, `after/03-dual.png` |
| A2 | Figures 1, 4, 5, 6, 8, 9, 10, 13 | same defect found on inspection at 200 dpi: in Figure 5 labels 6, 7, 11 on tree nodes and 10 on a bold edge; in Figure 6 label 12 on a ring; in Figure 8 labels 10 and 12 on edges; in Figure 10 label 1 under a sign and 10 on an arrow; root labels cut into the collar in all of them | labels placed by computation against the objects of each panel (toolkit entry below). `before/` and `after/` hold `07-pair-D`, `08-disk`, `13-selected`, `17-heights` |
| A3 | Figure 12 (`06-flow`) | labels on edges, capacities written on three edges, two long edges across the whole picture, tight set a faint grey wedge | four columns; vertices as numbered circles and triangles as grey boxes; capacities once under the gaps; first state double vermilion, second state solid blue, no-flow incidences thin and light; `S = {2}` ringed; rows folded so that no used incidence spans more than one row. Set at `0.69\textwidth` (was `0.74`). `before/06-flow.png`, `after/06-flow.png` |
| A4 | Caption of Figure 12 | described thin incidences as the capacity-1 edges and the double and solid ones without naming the encodings | names the two encodings and ties them to the wedges of Figure 8, says the two states alternate along a cycle of 14 incidences and one of 6, says the thin lines carry no flow, calls `S` the ringed set |
| A5 | Section 7, last paragraph | "Two companion notes give a primal formulation and an account using two sign-reversing involutions." | a paragraph that names both notes by title and path, says they are unpublished notes in the same repository, and says what each contains. Kept as sentences, not bibliography entries: an entry without author in `amsplain` sorts and reads oddly, and the paths make the notes findable |
| A6 | Section 7, Lean paragraph | two sentences: OpenAI's proof is machine-checked, by a different route | the two sentences kept word for word, then what the Lean check of Section 4 covers (item A6 below) |
| A7 | Section 7, "Cubic" | nine running sentences for the 3-connectivity of the bipyramid incidence graph | the same check as a two-item list by cases (at most one deleted vertex is a face centre; both are). Every claim of the old text is kept |
| A8 | Section 7, "3-connected" | five running sentences | the non-Hamiltonicity first, with its reason written out ("a cycle falls into at most two paths when two of its vertices are deleted"), then 2-connectivity as a two-item list. The reason is an added justification of a claim that was already there |
| A9 | Example 3.3 | array with a vertical rule and `\hline` | `booktabs` rules as in Tables 1 and 2, no vertical rule |
| A10 | Caption of Figure 7 | "Out-lined" broken across lines in the narrow side caption | reworded first sentence, hyphenation switched off in that caption |

A6 in detail. The independent rebuild `research/2026-11-14_astra_lean-check/REPORT.md` finished during this task and confirms the build, the axioms, the statements and the dependency claim, with three corrections to the wording of `proofs/lean/README.md`. The new text follows the corrected wording:

- Lemma 4.5 is claimed only "for a second state whose opposite sides contain a cycle", not as the full identity over good states;
- Proposition 4.8 is claimed as the step "from a pair to a pair whose second state has acyclic opposite sides", which is the statement of `forest_pair_real`, and the word "good" is avoided because the good-state dictionary is not formalised;
- Lemma 4.6 is claimed only as the addition of the steps for a weight that is a sum of local terms;
- the replaced object is "the complex phase and the polynomial of OpenAI's nonvanishing argument", not every polynomial dependency;
- the heights are said to be represented by a flow, and the face-path heights are said not to be formalised.

Typographic pass. All 20 pages rendered and looked at. No heading at the foot of a page, no widow, no figure far from its first reference. Line-end hyphenation checked with `pdftotext`: the only break left is "Computa-tional" in the bibliography. Comparable figures keep equal widths (the three two-panel figures of the example at `0.94\textwidth`).

Build. `latexmk -pdf -interaction=nonstopmode -halt-on-error barnette.tex`: no error, no undefined or multiply defined reference, no overfull box. One underfull box (badness 1694) in the narrow caption of Figure 7.

## Toolkit, `paper/figures/`

| File | Change |
| --- | --- |
| `draw.py` | `Panel` keeps a registry of drawn objects; `place_label` and the rewritten `vertices` place vertex labels against it; `label` registers free labels; `08-disk` and `17-heights` register their rings and path and call `vertices` last; `03-dual` at unit 0.9; `06-flow` redrawn from `run['flow']`; `write()` writes `label-placement.json` and fails if a label is nearer than 0.5pt to a registered object |
| `check.py` | new record `flow` in `running()`: explicit flow, conservation, value 20, maximum flow, capacity of the cut at `S = {2}`, the folded row order with its assertions; one new line in `CHECKS` |
| `label-placement.json` | new, written by `draw.py` |
| `README.md` | new section "Final polish" |
| all `NN-*.tex`, `NN-*-body.tex`, PDFs, `renders/`, `gallery.*`, `captions.json`, `checked.json`, `validation.json`, `style-audit.json` | regenerated by `python paper/figures/build.py` |

The primal note's own figure script (`proofs/primal/figures/check.py`) imports `Panel` and `pt`. The new arguments are optional and it places no vertex labels, so its output does not change. I did not rerun it.

## B. Bijective note, `proofs/involutions/` (18 pages before and after)

| # | File | Change |
| --- | --- | --- |
| B1 | `involutions.tex` | title "Two involutions for the good-pair lemma"; Theorem 1 named "Good-pair lemma"; "forest pair" becomes "good pair" in the abstract and Lemma 8 |
| B2 | `involutions.tex`, after Theorem 1 | new: the definition of good pair, the older name once, the link to the main paper's good state by its Lemma 4.2, and one paragraph on the relation to the main paper (Theorem 1 is its Proposition 4.8; Li's intended proof in full; a term-by-term unpacking of Lemmas 4.5 to 4.7 for one particular height) |
| B3 | `involutions.tex`, Section 2 | after the definition of `D_p`: "the undirected edge set of `D_p` is the cover of `p`"; after `m`: "This is the `m` of the main paper, and a cover with `m` cycles is a minimum cover"; "unoriented cover" becomes "cover" in the display of Lemma 6 and once in Section 5 |
| B4 | `involutions.tex`, Section 5 | `H(s)` was used before it was defined. Now defined there as the signed number of tokens, followed by "So `H` has the opposite sign to the main paper's weight" |
| B5 | `involutions.tex`, Section 8 | label `compare` on the section; after the ray definition of `H`: "This `H` has the opposite sign to the weight of the main paper" |
| B6 | `INVOLUTIONS.md` | title; first paragraph names the good pair, the older name, the main paper and the relation; "forest pair" becomes "good pair"; "unoriented cover" becomes "cover"; the sign of `H` stated |
| B7 | `STATUS.md`, `README.md` | "good pair (earlier name: forest pair)" in the table; "good-pair" elsewhere; README title |
| B8 | git | `involutions.aux`, `.log`, `.out` untracked with `git rm --cached`; `.gitignore` now lists `*.aux *.log *.out *.toc *.fls *.fdb_latexmk build-output.txt` |

The definition of `H` in B4 states the sign that the next sentence of the note already asserted (`H = -omega`). A token with `kappa = -1` counts `+1`, which is "left to right positive" in the ray version, since the note's direction bit is `d = (1 + kappa)/2`.

Build: `latexmk`, no error, no undefined reference, no overfull box.

## C. Primal note, `proofs/primal/` (15 pages before and after)

| # | File | Change |
| --- | --- | --- |
| C1 | `primal.tex`, `PRIMAL-PROOF.md`, Section 6 and Lemma 8 | the edges of `D` are "marked": "A pair marks at each black vertex...", "is marked at most once", "labels exactly one marked edge", "The marked edges of a pair split..."; one new sentence "Its edges are marked; selected is kept for the matching `P`." "Selected" now refers only to `P` |
| C2 | `primal.tex`, `PRIMAL-PROOF.md`, before Section 1 | one sentence on the relation to the main paper: the same proof in `G`, lemma by lemma, with a dictionary; two steps differ (Li's deficit argument for the first pair, flow potentials with a polynomial in place of the heights) |
| C3 | `primal.tex`, `DICTIONARY.md` | second column headed "Main paper, in T" and filled with the main paper's names: state, pair, opposite side in `Q_s`, `D(r,s)` and its cover, good state and good pair, selection, acyclic selection. "Directed selected face links" becomes "Directed marked face links; undirected D". `DICTIONARY.md` gets one explanatory paragraph |
| C4 | `primal.tex` | the three-line lead-in to the figures moved from before the dictionary page to after the dictionary's note, reworded "The figures on the following pages instead use...". With the new sentence of C2 it had been left alone on a page |
| C5 | `EXAMPLES.md` | opening note: these are the first version's worked examples (cube and a 20-vertex graph), and nothing in the file describes the 22-vertex running example; the 20-vertex heading labelled |
| C6 | `STATUS.md` | heading "Exact finite range (first version's checker and worked example)". The paragraph under it already said so |

`primal.tex` was edited by hand in step with the Markdown. Its generator, `research/2026-11-14_astra_primal-revision/build.py`, writes into another agent's folder and was not run. C4 exists only in the TeX.

Build: `pdflatex` three times, no error, no undefined reference, no overfull box.
