# Report: manuscript merge

1. Deliverable: `paper/main/barnette.tex` and `barnette.pdf`, 18 pages including one page of references (17 of text), amsart, A4, 1in margins; builds with latexmk/pdflatex with no errors, no warnings, no undefined references and no overfull boxes.
2. Structure: draft B's dual-triangulation skeleton with draft A's opening, the cube as a six-panel overview, printed example states, and a closing section of remarks labelled proved / computed / open.
3. Mathematics: the gap both drafts shared (Euler on the inside of a cycle) is closed by a connectivity lemma used three times; the refereed product sign and face-path heights are adopted after a line-by-line check (`DECISIONS.md` section 4); spokes, winding numbers, `J` and the exponential sum are gone from the main line.
4. Figures: 11 figures from the shared toolkit, all with vertex labels where text names vertices; a new heights figure (`17-heights`); stale notation (phases, `Z(x)`, spokes in the overview) regenerated; `check.py` and the build pass; filenames unchanged.
5. Every printed number about the examples is recomputed by `example.py` (`example.txt`), cross-checked against `workings/barnette_lab`. Audit verdict FOLLOWS (`AUDIT.md`), author's own audit.

## What I set out to do

Produce one manuscript from the two drafts and their reviews, clearer than the sources, starting from the obstacle, with each object introduced with its purpose, one meaning per symbol, complete proofs, honest attribution in the paper's own voice, and properly scaled figures.

## What I established

- `paper/main/barnette.tex`, `barnette.pdf`, `refs.bib`, `.gitignore`. Sections: 1 Introduction (obstacle, Theorem 1.1, the plan with Figure 1, history and sources, the example); 2 the dual triangulation and the target (Lemma 2.1 dual, Lemma 2.2 connectivity, duality lemma, Proposition 2.6); 3 corner choices and the tree of faces (states read off the answer, `Q_s`, `S_s`, good states, `Y_s`, outdegree lemma, the inside of a cycle, disk identity, acyclicity); 4 pairs (partner lemma with the unique partner of a good state, two reversals, product sign, cancellation, heights by paths of faces, finite difference, nonvanishing, table of the eight pairs); 5 the first pair; 6 separating triangles and the proof of Theorem 1.1; 7 remarks.
- `DECISIONS.md`: every merge decision and every finding of both review folders (REFEREE, EDITS 1-25 and E1-E25, exposition reviews, cold reads, comparison, primal recommendation) with accepted / rejected / moot and why.
- `NOTATION.md`: symbol table, scopes, and how each overload the reviews listed was resolved. The example's states are named `α` and `β` so that `r` and `s` keep their roles in text and figures.
- `AUDIT.md`: reverse-Lamport audit from Theorem 1.1, 48 nodes, all discharged.
- `example.py` / `example.txt` / `example.json` (`COMPUTED`, command in the script header): running example 12 states, 8 pairs, 6 good states (each with one partner), `ε = ∏δ = (−1)^{(n+J)/2}` on all pairs, the height lemma on all 16 reversals and every white face, the eight-pair table, `Σεω^j = 0, 0, 18` for `j = 0, 1, 2`, the recovered selection and its two trees, 6 Hamiltonian cycles avoiding the edge and all 6 produced; cube states; hexagonal prism 3 states, 2 good, 4 / 2 / 2 avoiding cycles by side; two glued octahedra: pair existence depends on the outer face within one colour class; the bipyramid incidence graph is planar, bipartite 5/6, 3-connected.
- `paper/figures/draw.py` changes (all filenames kept): example states renamed in captions and panel labels; `10`, `11`, `16` without phases or `Z(x)`; `01` panel (e) shows `S_s` and the tree of faces; vertex labels with white backing; new `17-heights`. `python paper/figures/build.py` runs `check.py` first and passed; log in `figure-build.txt`.

## What failed or was cut, and why

- The primal backbone recommended by `research/2026-11-14_fable_referee-primal/RECOMMENDATION.md` was not adopted (reasons in `DECISIONS.md` section 1). Its strongest argument, the inside of a cycle, is answered in the dual by Lemma 2.2 and one paragraph.
- Not in the paper: the rarity family `(2/3)^q`, the proof of the exact pair criterion (quoted from the unsigned manuscript instead), Hall in place of max-flow, the full cube recovery table, a notation table inside the paper.
- `papers/barnette.bib` did not exist; `refs.bib` merges the drafts' files plus entries from the history folder. Barnette 1969 and Kelmans have not been seen by anyone in the project; Kelmans is credited "as explained by" Hertel and Gorsky-Steiner-Wiederrecht and has no bibliography entry.
- The heights figure's path curve is wiggly in the long thin face `{0,1,6}`; it is correct and readable at print size but not pretty.
- No independent cold read of the merged text was possible inside this task.

## What is still open

- A cold read by a reader who has seen neither draft, logging stalls only.
- A human check of the two adopted simplifications (product sign, face-path heights) and of Lemma 2.2.
- If `papers/barnette.bib` appears with corrected theorem numbers, re-point `refs.bib` and re-check the pinpoints: OpenAI Theorem 1.1, Corollary 7.1, Lemma 5.3, Section 5.3; Li Section 4, Section 6, Appendix C; Hertel Corollary 3; GSW Theorems 4.3, 4.16; APSW Lemma 5, Section 5; the unsigned manuscript Theorem 1.2.

## Three best next steps

1. Cold read of `paper/main/barnette.pdf` by a fresh agent, then fix the stalls.
2. Check every pinpoint citation against `papers/barnette.bib` and `MISMATCHES.md` once they exist.
3. Smooth the face path in `17-heights` (choose a path through fatter faces, or bend the curve less), and decide whether `16-at-a-glance` should replace Figure 1 for readers who want the running example on page 1.

## Leads for others

- The closing remark "a Hamiltonian cycle arises from the construction exactly when its state is good" has a two-line proof (a tree has at most one perfect matching). It may shorten the corresponding statement in the structure referee's integration note.
