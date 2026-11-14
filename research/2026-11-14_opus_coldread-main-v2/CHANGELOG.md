# Edits applied to `paper/main/barnette.tex`

Base: commit `d3b3651` (the parallel referee's last change). Three batches, each committed
with `paper/main/barnette.pdf`: `edd9c0c`, `26fa43b`, `f04e0d1`. No statement, proof step,
hypothesis or printed number changed meaning. Every build had no errors, no undefined
references and no overfull boxes (`build1.txt` to `build3.txt`). The paper is still 19 pages.
`paper/figures/check.py` passes. No figure file was changed.

Numbers below match ASSESSMENT.md section 4.

## Batch 1 (`edd9c0c`)

| # | Where | Old | New |
| --- | --- | --- | --- |
| 4 | Plan step (1) | "The selected side in each other black triangle leaves one corner, and uses every vertex off $t_0$ once as a tail." | "In each other black triangle the selected side then points away from one corner, its tail, and every vertex off $t_0$ is a tail exactly once." |
| 5 | Plan step (2) | "They give a tree joining the triangles, which forces a selection (panels (d)--(e))." | "The sides that are not avoided then join the triangles into a tree, and this tree forces a selection (panels (d)--(e))." |
| 3 | Plan step (4) | "Grouping by these cycles, with weight increments counting enclosed white triangles, proves that the sum is nonzero. Thus a good state survives." | "Reversing one of these cycles flips the sign and raises the weight by the number of white triangles inside the cycle, which is at least one. Grouped by these cycles, with the weight raised to a suitable power, the sum becomes a sum of products of these numbers, all of one sign. So the sum is not zero, and a good state survives." |
| 15 | History | Four uses of "as explained by / as recounted by Hertel" | "We follow Hertel's survey [9] for the older history." The later facts cite [9] directly. Attributions unchanged. |
| 14 | Before Lemma 2.2 | "The next lemma shows that $\T$ is connected. We use it again for the inside of a cycle and for the pieces of Section 6." | "Euler's formula needs a connected graph. The next lemma supplies connectivity for $\T$, for the inside of a cycle in Section 3 and for the pieces of Section 6." |
| 13 | After Proposition 2.6 | "Part (1) says why the target has two conditions with two different reasons:" | "Part (1) shows that the two conditions on the target do different jobs:" |
| 17 | The tree of faces | one paragraph | paragraph break before "For $Y_s$ to be a tree ..." |
| 16 | After Definition 3.4 | none | "The unsigned manuscript [4] calls a good state a *tree matching*." (naming convention, CONSISTENCY.md C1 and section 5) |
| 6 | The inside of a cycle | none | "The state is called $r$ here because Section 4 applies these facts to the first state of a pair." |
| 7 | Example 3.10 | "both states are good; for $s$ the tree $Y_s$ makes" | "the cube has exactly two states, those of Figure 1(f), and both are good. For the solid one, $s$, the tree $Y_s$ makes". Checked by hand: the cube has exactly two states, (4,3,5) and (5,4,3) on faces 045, 234, 135, and the solid one has the quoted sides 04, 23, 35. |
| 8 | Why two states | "turns it into the first." | "reduces the second condition to the first." |
| 9 | After Lemma 4.5 | "In the example only $\alpha$ has a cycle in $Q_\alpha$, and its two partners" | "In the example $\alpha$ is the only second state of a pair whose opposite sides contain a cycle, and its two partners" |
| 12 | Section 7, polynomial | "with their spoke weights $\mathfrak a$." | "with the spoke weights $\mathfrak a$ of [14, Lemma 5.3]." |
| 10 | Figure 13 caption (c) | "its trees meet those of the pieces in the edge {3,5} or in the vertex 4. Disks and squares mark the two trees." | "Disks and squares mark its two trees. Each is a tree of (a) joined to a tree of (b): the square trees share the edge {3,5}, and the disk trees share the vertex 4." Checked against `check.py` output (gluing parts [0,1,4,7,8], [2,3,5,6]; shared edge (3,5)). |

## Batch 2 (`26fa43b`)

| # | Where | Change |
| --- | --- | --- |
| 1 | "The total is not zero" | Replaced the six-line paragraph that began "Let $m\ge1$ ... take $F=\omega^m$. Here is why a power." with three short paragraphs: (i) define the **cover** (naming convention item 6, "OpenAI call it a group"); (ii) one cycle first: on the cube the two pairs share the cover "triangle 3,4,5 around one white face", have opposite signs (Lemma 4.4) and weights differing by 1 (Lemma 4.6), so $F=1$ cancels and $F=\omega$ leaves $\pm1$; (iii) a cover with $c$ cycles gives a $c$-fold difference; Lemma 4.7 kills powers below $c$ and leaves $\pm c!\prod L(C)$; hence $F=\omega^m$ with $m$ the least number of cycles; then a pointer to Figure 11. The definition of $m$ and the choice $F=\omega^m$ are the same as before. |
| 1 | Proof of Prop. 4.8 | "Sort the pairs into classes by the undirected edge set of $D(r,s)$." becomes "Sort the pairs into classes by their cover, the undirected edge set of $D(r,s)$." |
| 2 | Figure 11 | Redrawn (inline TikZ in the paper, as before). It was a row of eight boxes copying Table 2. It is now two 2×2 squares, one per cover. Columns are 7-cycle cw/ccw, rows are triangle cw/ccw, and each cell gives $\varepsilon$ and $\omega$. Blue arrows labelled $+L_1$ across and $+1$ down. The α cells are shaded and labelled $s=\alpha$. Under each square: $\sum\varepsilon\omega^2=16-9-4+9=12=2\cdot6\cdot1$ and $4-1-1+4=6=2\cdot3\cdot1$. All values are from Table 2. New caption explains "a difference across and a difference down". Footnote-size labels. |
| layout | Section 5 | The paragraph "Figure 12 shows the network and a tight cut in the example." and Figure 12 moved from before the definition of separating triangle to after the proof of Proposition 5.2 (script `move_flow_figure.py`, text unchanged). Without it page 15 was 40% blank. |

## Batch 3 (`f04e0d1`)

| # | Where | Change |
| --- | --- | --- |
| 11 | Figure 8 | `\includegraphics[...,trim=0 17bp 0 0,clip]{07-pair-D.pdf}` removes the legend line "Outlined: first state β; solid: second state α", which repeated the caption. The figure file is unchanged. |

## Renders

`renders/before/base-pNN.png`: all 19 pages of the PDF at `d3b3651`, 60 dpi.
`renders/after/pNN.png`: all 19 pages after batch 3, 60 dpi. Pagination moved only from page 13
on. The pages whose content changed are 1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 15, 16, 17 and 19. The
130 dpi renders I used for the cold read were of the PDF at `8317608`, and I deleted them by
mistake when I saved the base renders. The base renders differ from them only by the
referee's seven-line commit.
