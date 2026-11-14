# Draft A against draft B, and a merge plan

Reviewer: Claude Fable 5.2, 2026-11-14. I read draft B cold and then in depth (`COLD-READ.md`, `REFEREE.md`, `EXPOSITION-REVIEW.md`). I read draft A (`paper/draft-A/barnette.pdf`, 11 pages) once, after finishing the review of B, together with `research/2026-11-14_opus_review-draft-A/REPORT.md` and the parts of its `EXPOSITION-REVIEW.md` on attribution. So I know B far better than A. Where I lean on the other reviewer's findings about A, I say "per the review of A". These are editorial judgments.

Short version. B has the better architecture: one graph, the target as "one side per triangle, no cycle", states read off the answer, recovery by one duality, each section removing the assumption of the one before. A has the better first page, a cube that shows the whole construction in one figure, explicit data for the examples, and two thirds of the length. The final paper should be B's skeleton with A's opening, A's cube overview and A's habit of printing the actual states.

## Section by section

| Step | Draft A | Draft B | Better, and why |
| --- | --- | --- | --- |
| Title | "Hamiltonian cycles from states. An exposition of OpenAI's proof" | "Barnette's conjecture in the dual triangulation" | A's subtitle. It says what the paper is before the abstract does. |
| Abstract | Six short causal sentences. "A signed count cancels every cyclic choice, while heights at white faces show that the count is nonzero." | Six sentences, the fourth carries all of Section 4 and "suitably rooted" is empty. | A. |
| Opening | First sentence: "A Hamiltonian cycle is a connected spanning subgraph of degree two." The obstacle and the cube in four sentences, then "The local degree condition and the global connectivity condition then have separate certificates." | History first, then the theorem, then the same obstacle with Figure 1, then a four-step route, then two insider paragraphs. | A for the first paragraph. B for the four-step route, which A lacks (per the review of A, rule 2 fails there). |
| Dual reduction | One dense paragraph proves that `T` is simple; Lemma 2 by contracting a tree, four lines; the target is two induced trees (Proposition 3). | Lemma 2.1 with a proof in steps; "selection"; Lemma 2.4 by parity; Proposition 2.5 with both halves. | B. The selection is a lighter target than two induced trees, and the induced-tree statement appears in B as a consequence, used only for gluing. A's four-line proof of duality is the one to keep as an alternative for readers who know contraction. |
| Where states come from | "We will delete one spoke at each bounded black center and one at each nonroot." The reason for spokes and for `Q_s` arrives in Section 5 (per the review of A: the main stall of its cold read). | Lemma 3.1 reads the state off an acyclic selection; `Q_s` is "the excluded side". | B, clearly. |
| Pairs | "A forest `Q_s` would be useful only if its components keep the three roots separate. A second state supplies exactly this control." Lemma 4 adds that a forest state has exactly one partner. Then table (2) prints `r` and `s` for the running example. The outdegree principle is stated once for later use. | "Why a second state" in three sentences, Lemma 4.2. No states are ever printed. | Level on motivation. A for printing the states and for saying the outdegree principle once. B for the proof. |
| First pair | Lemma 5 on page 5, before the reader knows what a pair is for; text close to OpenAI's, including "Include `t0` in the sum with contribution zero", which cannot be checked as written (per the review of A). | Section 5, after the need is established; the count for `t0` is written out (`2n − (e(U) − 3) + (b(U) − 1)`) and checks. | B, on placement and on that step. |
| Disk identity | Lemma 6, `W = B + 1` and `h − 2ℓ = 3`, proved with an edge count `E_d = 3B + h − ℓ = 3W + ℓ`. Followed by "Example (The larger disk)", which names the cycle and says it is a cycle of `D`. | Lemma 3.6, same statement, signed side count, both halves of bijectivity named, at its first use. Figure 5 is the same shared figure. | B for the proof and the position. A for the example paragraph, which answers a question B leaves open (CR 35). Both apply Euler to the disk without checking connectedness (REFEREE G1). |
| Sign and the two reversals | `J` and `ε` in one display (7), table of the two operations, cancellation in running prose ending in (8). | Lemma 4.3, Table 1, Lemma 4.4, Lemma 4.5, each separate, with the remark on `K_s`. | B for checkability. Both should adopt `ε = ∏ δ(r(t), s(t))`: I found it in `research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` (REFEREE S2) and the reviewer of A found it independently (its REPORT, item 4). A's sentence "Reversal changes the entries of `r` at `a_7, a_9, a_21` from (8,1,9) to (1,9,8)" is the kind of concreteness B lacks. |
| Why weights | "The unweighted sum cannot prove existence: reversing just one cycle of `D` also changes the sign, so that sum is zero." | "With `F = 1` the answer is no, since reversing the cycle of `D(r,s)` through a fixed vertex pairs every pair with one of opposite sign." | Level. Both are good and say the same thing. |
| Heights | Paths `γ_w`, spokes, and a schematic Figure 5 (start inside, start outside) for the crossing count. The slide of OpenAI §5.3 is kept. | Same definition, no figure, winding numbers in place of the slide. | A for having a figure at all. B for the proof. Better than both: heights by a path of faces (REFEREE S1, EDITS 5), which needs neither spokes nor the slide nor winding numbers. |
| Nonvanishing | `F(s) = ∏ h_s(w_i)` with a white face chosen inside each cycle of one minimal `D_*`; the count is a number of bijections (13). "Example (What the count sees)" displays the four-term difference and says why nesting is harmless. | `F = ω^m`, Lemma 4.7, total `±m! Σ ∏ L(C)`. Example 4.9 gives 18. | B's weight: one function of the state, no choice of `D_*` or of faces, and it is the quantity the published papers compute. A's example: it shows the difference at work. Take B's lemma and A's way of showing it; EDITS 16 gives the table that does this for `ω^2` (`4 − 1 − 16 + 25 = 12 = 2·6·1`). |
| Recovery | Spoke graph `H` with the centre of `t0`, "its faces correspond exactly to the white triangles", the white tree `W_s`, Lemma 8 with a Jordan-curve labelling for the induced trees. Per the review of A, Lemma 8 has two defects (it never says `y_0` is outside the disk, and it cites Lemma 4 for a graph that lemma does not cover). A table walks the cube through the recovery. | `Y_s = T* − S_s*` on all faces, rooted at `t0`; Proposition 3.7. No spoke graph, no Jordan labelling. | B. A's cube table (black face, deleted corner, tree edge, child, selected side) is worth importing in B's language. |
| Gluing | Induced trees meet in a vertex or an edge; two short paragraphs as in OpenAI. | Selections; a complete acyclicity proof; a sentence on the primal reading. | B for the proof. A is shorter because Proposition 3 already carries induced trees. |
| What the hypotheses do | none | Section 7 | B. |
| Examples | Two: the cube (octahedron) for the whole pipeline, and the 13-vertex triangulation for cancellation. Face lists, states and the recovery are printed. | One, the 13-vertex triangulation, at every step, with counts but without lists; the promise "few enough to list" is not kept. | A for data, B for discipline. The cube cannot show a cyclic `Q_s`, which A says. |
| Figures | Figure 1 runs the cube through six panels on page 3 ("read from left to right along each row"). Figure 5 is a schematic of the crossing count. Per the review of A, three figures are never cited and Figure 2 has the same label collisions. | Eleven figures, four own; two misplaced, none for heights (EXPOSITION-REVIEW (e)). | A's Figure 1 is the best orienting figure in either draft. B's own Figures 6, 9, 10 are the best step figures. |
| Attribution | Names Kelmans. Cites the project note and its own script as references [2] and [4] with repository paths (per the review of A, a defect). Does not say that heights are Li's ray counts. | "unpublished notes written during a collaborative reading"; "ours" against "notes"; two overstated bullets; Kelmans missing. | Neither. A is more open about where things come from, B is cleaner in the bibliography. See the plan. |
| Length | 11 pages. Dense: Lemma 5 and the disk identity are OpenAI's text compressed. | 16 pages, of which about one page is introduction for insiders. | B's pace is right for the stated aim. Length is not the problem with either draft. |

## What each draft should learn from the other

From A into B:
1. The first paragraph.
2. The cube in one six-panel figure as a preview of the whole construction.
3. Printed data: the two states of the running pair (A's table (2)), the reversal as a change of three entries, the cube recovery table.
4. A schematic at the crossing count.
5. The outdegree principle stated once.
6. "A forest state has exactly one partner" as a remark after Lemma 4.2 (it explains why the example has six good states and six good pairs).
7. Kelmans by name.

From B into A (if A were kept): the selection as the target, Lemma 3.1, recovery without the spoke graph, the first pair after its need, the hypotheses section, the route in four steps.

## Merge plan

One paper, B's order. "A" and "B" below name the text to start from. Edit numbers refer to `EDITS.md`.

**Title and abstract.** B's title with A's subtitle: "Barnette's conjecture in the dual triangulation. An exposition of OpenAI's proof". Abstract: A's, with its second sentence changed to say "an acyclic set of edges with one side of every triangle" in place of "a forest in the planar dual", and one sentence for the gluing.

**1. Introduction** (about one and a half pages).
- Paragraph 1: A's opening paragraph, unchanged.
- Theorem 1.1 and the two sentences after it: B, with Kelmans (edit 20a).
- History: B's sentence on special cases, moved after the theorem.
- Overview figure: A's Figure 1 (the cube in six panels), with panel labels in B's vocabulary (state, opposite sides, tree of faces, selection). Panels (e) and (f) need redrawing if the spoke graph goes: (e) becomes `S_s` with `Y_s`.
- The route: B's four steps with edit 8, each step pointing to a panel of the overview figure.
- "The example": B's paragraph with edit 19b.
- Drop B's "One picture" paragraph except its first three sentences. Move "Sources" to a final section (below).

**2. The dual triangulation and the target.** B's Section 2 with edits 1a, 18, 21, 24. Lemma D (edit 1a) goes here. Keep B's parity proof of the duality lemma; add A's contraction proof as a two-line remark. Put the Hamiltonian-curve panel (shared 13(b)) right after Proposition 2.5.

**3. Corner choices and the tree of faces.** B's Section 3 with edits 1b, 2 (panel (a) only here), 10, 22. After Definition 3.2 print two states of the running example as A's table (2) does, in B's notation, and use the same two states in every later figure. After Proposition 3.7 add the cube recovery table from A, rewritten for `Y_s`. Import A's sentence that the long cycle of Figure 5 is a cycle of `D` for the pair of Figure 8.

**4. Pairs of states.** B's Section 4, with these changes.
- "Why a second state": edit 25, then Lemma 4.2, then A's remark that a good state has exactly one partner, then the outdegree principle stated once.
- Sign: `ε = ∏ δ(r(t), s(t))` (REFEREE S2). Lemma 4.4 becomes: both reversals change the sign, because each flips every `δ` on a cycle of odd length. Keep `J` only as a remark connecting to OpenAI's `i^J`.
- Cancellation: B's Lemma 4.5, plus A's sentence on the three entries that change.
- Heights: the face-path definition (edit 5) with the new figure (edit 4). If the editors keep spokes, B's winding-number proof with edits 6 and 7 and A's Figure 5.
- Nonvanishing: B's Lemma 4.7 and Proposition 4.8 with edits 11, 12 and the table of the eight pairs (edit 16). A's "what the count sees" becomes two sentences after the table.
- Remark 4.10: edit 14, and one sentence crediting Li's ray counts as the same object as a height (per the review of A).

**5. The first pair.** B's Section 5 unchanged apart from the renames of edit 9, with the shared figure `06-flow` if it matches.

**6. Separating triangles.** B's Section 6 with edits 1c and 20b. Figure 11 redrawn with one labelling.

**7. What each hypothesis does.** B's Section 7 with edit 15.

**8. Sources and what is different here.** Edit 13, extended by: the double-dimer regrouping and Temperley's correspondence as context (one sentence each, as in OpenAI's introduction); Li for the ray counts; the constructive paper for the real sign and the rooted-forest target. The project's notes are acknowledged in one sentence with the repository address, and are not entries in the bibliography. The companion scripts are mentioned once ("the numbers for the example were computed by exhaustive enumeration; the scripts are in the repository").

**Figures for the merged paper**, in order: cube overview (A Fig. 1, adapted); two 2-factors (shared 02) or drop it, since the cube overview has the same panel; dual with labels (shared 03, labels fixed); local triangle (a) (B); `Q_s` cycle and forest (shared 09, labelled); disk identity (shared 08); recovery (B Fig. 6, labelled); selection and curve (shared 13(b)); pair in a triangle (B Fig. 3(b)); pair and `D` (shared 07, labelled); cancellation (B Fig. 9, labels moved); heights (new); white faces inside cycles (B Fig. 10); flow (shared 06); gluing (shared 14, redrawn). Fourteen or fifteen figures.

**Expected length.** About 16 pages: B's 16, minus one page of introduction, minus half a page in the heights proof, plus the cube overview, two tables and the sources section.

**Order of work.**
1. Apply edits 1, 8, 10 to 25 to B. They are independent of the merge decisions.
2. Decide the two mathematical options together: product sign (REFEREE S2) and face-path heights (edit 5). Both are proved in `REFEREE.md` and checked by `check_face_paths.py` and, for the sign, by the other reviewer's `check_examples.py`. They need a human reading before they go in.
3. Import from A: opening paragraph, cube overview, state table, recovery table.
4. Figure pass by the figure owner: labels everywhere, one grey, the new heights figure.
5. A cold read of the merged text by a reader who has seen neither draft.

## Disagreements between the two reviews that the merge must settle

- **Kelmans and the reduction to no separating triangle.** The review of A recommends cutting A's clause that credits Kelmans with the reduction, because the draft gives no pinpoint. `research/2026-11-14_opus_history-literature/HISTORY.md` section 4 and `EQUIVALENTS.md` entry 8 say the reduction is Kelmans's, known through Alt, Payne, Schmidt and Wood 2016, Section 5, and that Kelmans's own paper was not seen. My edit 20b credits Kelmans "see Hertel, APSW". The merge should cite APSW Section 5 for the statement and say "attributed to Kelmans", unless someone reads Kelmans.
- **How to cite the project's notes.** A puts them in the bibliography with repository paths; the review of A calls that a defect; B hides them behind "unpublished notes". My proposal is an acknowledgement sentence with the repository address.
- **One example or two.** The style guide's rule 17 asks for one example across representations. A uses two and says why (the cube has no cyclic `Q_s`). I side with A here, with the cube confined to the overview figure and the recovery table.
