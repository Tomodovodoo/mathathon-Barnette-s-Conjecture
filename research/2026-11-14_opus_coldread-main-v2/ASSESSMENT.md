# Informed assessment of version 2

Read after the cold read: `skills/unslop/SKILL.md`, `STYLE-GUIDE.md` and `HOW-THE-REWRITE-WORKED.md`
(astra exposition method), the earlier cold read (`EXPOSITION-REVIEW.md`, `EDITS.md`, skimmed for
items), the reviser's `CHANGES.md`, `digestions/steps/00-overview.md`,
`digestions/route-map/HOW-IT-WORKS.md` sections 3 to 5, atlas pages 1 to 8 (rendered),
`CONSISTENCY.md`, and Section 5 of the OpenAI paper in the text dump, plus the section headings
of Li and the trees paper. I did not re-read Li and the trees paper in full. Where I compare
with them below, I rely on their structure and on the digestions. All judgements are editorial
(HUNCH in the brief's vocabulary).

The source I assessed is `paper/main/barnette.tex` at commit `d3b3651`. That commit is the
parallel referee's small correction batch, made after my cold-read renders. It does not touch
any passage my cold read flagged.

## 1. The 22 style rules

| # | Rule | v2 | Evidence |
| --- | --- | --- | --- |
| 1 | Open with the obstacle | pass | "Connectivity is the whole problem", cube with two squares. |
| 2 | Route as implications | pass, one weak step | The plan's steps (1), (2), (3), (5) each give a reason. Step (4) says the sum is nonzero but not why. |
| 3 | Theorem contract once | pass | Theorem 1.1 with `e`. Theorem 6.2 for the induction. |
| 4 | Define when wanted | pass, three blemishes | `r` in "The inside of a cycle" arrives without a reason. "Spoke weights 𝔞" (Section 7) is never defined. The two cube states in Example 3.10 are never named. |
| 5 | Names for reusable contracts | pass | Disk identity, outdegree, duality lemmas. |
| 6 | Order by dependency | pass | Every figure follows its first reference. No float sits inside a statement or proof. |
| 7 | Definition apart from assertion | pass | `Q_s` defined, then Lemma 4.2. |
| 8 | Remove stronger targets | pass | No algorithm, no determinant in the main line. |
| 9 | Invariants of repeated operations | pass | "The cycle `K_s` must be chosen from `s` alone." |
| 10 | Goal before formula | pass, one miss | "The total is not zero" opens with "take `F = ω^m`. Here is why a power." The formula comes before the goal. |
| 11 | Display decisions | pass | Disk counts and the class contribution are displayed. |
| 12 | Cite tools at invocation | pass | Hall, Jordan, Euler, max-flow min-cut. |
| 13 | Calculation specific to this proof | pass | `B = I + ℓ` with both halves of bijectivity. |
| 14 | Notation audit | pass | Overloads from v1 removed (`o`, `ν`, `Ψ`, `Π`). Naming convention: "good state" is used; "cover" (convention item 6) is not used, and the trees paper's "tree matching" is not mentioned. |
| 15 | Each conclusion its reason | pass | Paragraph after Proposition 2.6. |
| 16 | Distinguish the two reversals | pass | Lemma 4.3 and Table 1. |
| 17 | One example across representations | pass | α/β thread through Figures 4 to 12 and Table 2. |
| 18 | Figures introduced by their question | pass, two weak captions | Figure 13(c) caption is unclear; Figure 10's caption is a second proof. |
| 19 | Readable figures | mostly pass | Figure 2: labels 7 and 11 still overprint small G-vertices (the earlier review's complaint is only half fixed). Figure 8: legend under the drawing repeats the caption. Figure 11 copies Table 2 and does not show the mechanism. Figure 12 is cluttered. |
| 20 | Abstract short and causal | pass | Six sentences. |
| 21 | Audits out of the manuscript | pass, one residue | No status tags. "Two companion notes ..." cites nothing the reader can find. Two connectivity checks in Section 7 read as referee answers, but the referee asked for them (CHANGES E6, E7), so they stay. |
| 22 | Compare rendered passages | n/a | Done in this review: before/after renders. |

Count: 18 pass (several with a blemish), 0 outright fail, 1 not applicable; the weak spots are
rules 2, 4, 10, 18 and 19.

### Earlier complaints: are they fixed in what I see?

Checked against the v2 PDF, using the earlier review's verdict list and `CHANGES.md`.

| Earlier complaint | Status in v2 |
| --- | --- |
| Plan omits the disk identity, never says a nonzero sum proves existence | Fixed (steps (2), (4): "Thus a good state survives"). |
| Abstract has undefined terms | Fixed. |
| Nine of thirteen floats cut statements or proofs | Fixed. All floats are `[H]` between blocks. |
| Disk figure after its proof | Fixed. Figure 6 precedes Lemma 3.8. |
| Page 8 40% blank | Fixed. Worst page now about 20% (page 16). |
| Figure 2 labels hide vertices of G | Half fixed. Labels 7 and 11 still sit on small G-vertices. |
| Figure 10 labels struck through | Fixed (now Figure 9 is a close-up). |
| Gluing panel (c) too small | Fixed. |
| Figure 1 rows collide, panels out of order | Fixed. |
| Why the faces should form a tree | Fixed ("A tree has at most one perfect matching ..."). |
| What `D(r,s)` is for | Fixed ("gives the second way of grouping the count"). |
| Why a weight `F` is allowed in Lemma 4.5 | Fixed (sentence before the lemma). |
| Status tags in Section 7 | Fixed. |
| Notation overloads (`c`, `F`, `x`, `f`) | Fixed. |
| Table 1 before the sign exists | Fixed. |
| "Second state" names `r` in places | Fixed. |

## 2. Step by step: is v2 the clearest account available?

| Step | Best of the three sources | v2 | Verdict |
| --- | --- | --- | --- |
| Degree two vs connectivity, dual | OpenAI §1.1 (short), trees §1 (cube) | Intro plus Figure 1 on the cube, Section 2 with the duality lemma proved | v2 clearest. |
| States from an acyclic selection | Trees paper (incidence tree), OpenAI §2 | Lemma 3.1 reads the state off the forest, then "So the unknown is a choice ..." | v2 clearest; the motivation is backwards-from-the-answer, which none of the sources does. |
| Tree of faces, recovery | OpenAI §6 (spokes minus state), Li Lemma 30 | `Y_s`, "a tree has at most one perfect matching", Lemma 3.6, Figure 5 | v2 clearest. |
| Disk identity | OpenAI Lemma 4.1 | Lemma 3.8 with Figure 6 and the remark on both halves of bijectivity | v2 clearest. Figure 6 is the best figure in any of the four texts. |
| Partner, `Q_s` orientation | OpenAI Lemma 6.1, trees Prop 2.1 | "Why two states", Lemma 4.2 | v2 clear; one pronoun to fix. |
| Sign and cancellation | Li (involution), OpenAI 5.1 | Product of local signs, Lemma 4.4, Table 1, Lemma 4.5, Figure 9 | v2 clearest. |
| Nonvanishing | OpenAI 5.2 to 5.3 (spokes, exponential), Li (marks), trees (integer polynomial); the route map's §5 explains it best of all project texts | Heights, Lemma 4.6, finite difference Lemma 4.7, Prop 4.8 | v2 is the most elementary proof, but its "why" paragraph is cramped. `HOW-IT-WORKS.md` §4 to §5 and atlas page 6 show the mechanism better: "each cycle contributes a difference whose constant terms cancel" and a 2×2 square of orientations per cover. **Not yet the clearest explanation; it is the clearest proof.** |
| First pair | OpenAI Prop 3.1, trees §3 | Flow, (5.1), Prop 5.2 with the density bound | v2 clear; Figure 12 cluttered. |
| Gluing | Li App. C, OpenAI §7 | Lemma 6.1, Theorem 6.2, Figure 13 | v2 clearest; one caption to fix. |

## 3. Verdict on the owner's standard

**Nearly.** Version 2 starts from the right principle (degree two is free, connectivity is the
problem), works backwards from an acyclic selection to states in a way none of the source papers
does, and keeps one worked example through every step. Definitions arrive when they are wanted,
floats no longer cut proofs, and figures are mostly right. It is far clearer than the three
papers on every step except one. The exception is the moment the main idea should land: why
the signed count cannot vanish. That gets one six-line paragraph with "Here is why a power", no
small case, and a figure that copies a table. A reader finishes the proof convinced but not
seeing it. Smaller items: four sentences that make a cold reader stop (plan step (1) "leaves",
"turns it into the first", Example 3.10's unnamed cube states, "only α has a cycle"), an
undefined symbol and an uncited sentence in Section 7, the Figure 8 legend, and the Figure 13
caption.

## 4. Ranked improvements

Exact strings refer to `barnette.tex` at `d3b3651`.

1. **Give "The total is not zero" its room.** Replace the paragraph from "Let $m\ge1$ be the
   smallest number of cycles" to "the product of the $c$ steps." with a goal-first version:
   (i) name the cover (naming convention item 6); (ii) one cycle first: on the cube the two
   pairs have the same cover, a triangle around one white face, opposite signs, and weights
   that differ by 1, so `Σ εω = ±1`; with `F = 1` it would be zero; (iii) then the general class
   as a `c`-cube of orientations, a `c`-fold difference, which needs the power `m`; (iv) why
   `m` is the minimum. Applied, see CHANGELOG item 1.
2. **Redraw Figure 11 as the mechanism.** Two 2×2 squares, one per cover, columns = 7-cycle
   cw/ccw, rows = triangle cw/ccw, each cell `ε`, `ω`; arrows "+6" (or "+3") across and "+1"
   down; under each square `Σεω² = 16 − 9 − 4 + 9 = 12 = 2·6·1`. Keep the connector between
   the two α cells. Applied (item 2).
3. **Plan step (4): say why the sum is nonzero.** Old: "Grouping by these cycles, with weight
   increments counting enclosed white triangles, proves that the sum is nonzero." New:
   "Reversing one of these cycles flips the sign and raises the weight by the number of white
   triangles it encloses, at least one. Grouped by these cycles and with the weight raised to a
   suitable power, the sum becomes a sum of products of these numbers, all of one sign, so it
   is not zero." Applied (item 3).
4. **Plan step (1) wording.** Old: "The selected side in each other black triangle leaves one
   corner, and uses every vertex off $t_0$ once as a tail." New: "In each other black triangle
   the selected side points away from one corner, its tail, and every vertex off $t_0$ is a tail
   exactly once." Also add "(Lemma 3.1)" pointer via the section reference already present.
   Applied (item 4).
5. **Plan step (2) "They give a tree".** Old: "They give a tree joining the triangles, which
   forces a selection (panels (d)--(e))." New: "The other sides then join the triangles into a
   tree, and a tree leaves at most one way to select a side in every triangle (panels
   (d)--(e))." Applied (item 5).
6. **The letter `r` in "The inside of a cycle".** Add after "Let $r$ be a state": "(we write
   $r$ because Section 4 applies this to the first state of a pair)". Without parentheses:
   new sentence "We call the state $r$ because Section 4 applies these facts to the first state
   of a pair." Applied (item 6).
7. **Example 3.10, cube states.** Old: "both states are good; for $s$ the tree". New: "the cube
   has exactly two states, those of Figure 1(f), and both are good; for the solid one, $s$, the
   tree". Needs a check that the solid state is the one with the quoted sides. Applied after
   check (item 7).
8. **"Why two states" pronoun.** Old: "Another state $r$ that differs from $s$ in every face
   turns it into the first." New: "Another state $r$ that differs from $s$ in every face reduces
   the second condition to the first." Applied (item 8).
9. **"Only α has a cycle".** Old: "In the example only $\alpha$ has a cycle in $Q_\alpha$, and its
   two partners". New: "In the example $\alpha$ is the only second state of a pair whose opposite
   sides contain a cycle, and its two partners". Applied (item 9).
10. **Figure 13 caption (c).** Old: "its trees meet those of the pieces in the edge $\{3,5\}$ or
    in the vertex $4$." New: "each of its two trees is a tree of (a) joined to a tree of (b),
    the square trees along the edge $\{3,5\}$ and the disk trees at the vertex $4$." Applied
    (item 10).
11. **Figure 8 legend.** Trim the legend line under the drawing (the caption already says it)
    with `trim` on `\includegraphics`, filename unchanged. Applied (item 11).
12. **Section 7: undefined 𝔞.** Old: "with their spoke weights $\mathfrak a$." New: "with the spoke
    weights $\mathfrak a$ of \cite[Lemma~5.3]{OpenAI2026}." Applied (item 12).
13. **Paragraph after Proposition 2.6.** Old: "Part (1) says why the target has two conditions with
    two different reasons:". New: "Part (1) shows that the two conditions on the target do
    different jobs:". Applied (item 13).
14. **Lemma 2.2 lead-in.** Old: "The next lemma shows that $\T$ is connected. We use it again
    for the inside of a cycle and for the pieces of Section 6." New: "Euler's formula needs a
    connected graph. The next lemma supplies it for $\T$, for the inside of a cycle and for the
    pieces of Section 6." Applied (item 14).
15. **History paragraph.** Four "as explained by Hertel" in one paragraph. Cite the survey once
    as the source for the pre-2005 history. Applied (item 15).
16. **Naming convention.** After Definition 3.4 add "The unsigned manuscript [4] calls a good
    state a tree matching." Applied (item 16). "Cover" is introduced in item 1.
17. **Split "The tree of faces" paragraph** after "no choice is left." Applied (item 17).
18. **Figure 2 labels 7 and 11.** Move the two labels off the G-vertices in the toolkit's label
    offsets. Not applied (time); recorded for the human editor.
19. **Figure 12 clutter.** Lighten the crossing double/solid edges or order the `X` column by
    the cycles so that most flow edges are horizontal. Not applied (time).
20. **"Two companion notes ..." without citation.** Either cite them or delete the sentence.
    Owner's decision; not applied.
21. **Figure 10 caption.** Cut to what to look at; the computation is in the text. Not applied
    (it is correct and the earlier review asked for its content).
