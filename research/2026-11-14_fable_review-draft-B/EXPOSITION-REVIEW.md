# Expository review of draft B

Reviewer: Claude Fable 5.2, 2026-11-14. Object: `paper/draft-B/barnette.pdf` (16 pages) and its source. Evidence: the cold read (`COLD-READ.md`, entries cited as CR n), the summary written from memory, and the source. Everything here is an editorial judgment (`HUNCH` in the vocabulary of the brief) unless it says `COMPUTED`.

Short version. Draft B is a clear paper. Sections 2 and 3 are better than anything in the three sources. Section 4 is in the right order but its hardest paragraph (heights) has the least support. The introduction is half for newcomers and half for insiders. The figures are the weakest part: two are in the wrong place, most lack the labels the text relies on, and the one object that most needs a picture has none.

## (b) The 22 rules of the style guide

Pass or fail, with the offending passage on a fail. "Pass*" means the rule is met and I note a blemish.

| # | Rule | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | Open with the obstacle | pass | "Degree two is easy; connectivity is the problem" names both requirements before any notation. It is the third paragraph, after history and theorem, which is fine. |
| 2 | Route as implications | pass* | The four steps each say what the step delivers. Blemish: step 3 reads as an unconditional nonvanishing and step 4 then says "One pair is needed to start" (CR 8). The claim "each forced by the one before" is not made good for the signed count. |
| 3 | Theorem contract once | pass | Theorem 1.1 with the edge, "The edge e is there for the induction". Theorem 6.2 is the induction statement and is stated for every face and side. |
| 4 | Define an object when the reader wants it | **fail** in two places | (i) The Sources paragraph on page 2 uses `Q_s`, `D(r,s)`, `ε = (−1)^{(n+J)/2}`, `ω^m`, `Y_s` before anything is defined (CR 11). (ii) The caption of Figure 3 uses state, pair, partner, `D(r,s)`, `u(t)`, spoke before the definition of a state (CR 24). In the body the rule is met very well: Lemma 3.1 derives the state from the answer before Definition 3.2. |
| 5 | Names for reusable contracts | pass | Disk identity (three consumers), duality lemma (two). |
| 6 | Order by dependency and reading need | pass* | The disk identity sits at its first use. Blemishes: Lemma 3.3 is stated under "`S_s` is a spanning tree" before "good" is defined (CR 28); Figure 7 lands inside Lemma 4.2 (CR 46). |
| 7 | Separate definition from assertion | pass* | `Q_s` is defined, Lemma 4.2 asserts. Blemish: "`S_s` ..., the set of all excluded edges" asserts something false as stated (CR 26). |
| 8 | Remove stronger targets only after checking the consumer | pass | No algorithm, no determinant. Proposition 2.5(2) is kept because the gluing uses it. Lemma 2.4 is stated for an arbitrary connected simple plane graph `M` but only `M = T` is used. |
| 9 | Retain invariants of repeated operations | pass | "`K_s` ... depends on `s` only", the remark after Lemma 4.5. |
| 10 | Goal before formula | **fail** once | "The total is not zero": "The `m`-th power is what makes the cycles with fewest cycles count, as the following computation shows." The sentence is garbled, and Lemma 4.7 is stated before the reader knows that the sum will run over orientation bits and that `ω` is affine in them (CR 61, 62). Elsewhere the rule is met ("A sign", "Heights"). |
| 11 | Display decisions, inline routine | pass | The three counts are displayed; the algebra is inline. |
| 12 | Cite standard tools at the invocation, with conditions | **fail** twice | Euler's formula on the disk without its hypothesis (REFEREE G1). "For a closed polygonal curve `Γ` and a path ... the signed number of crossings ... is the winding number" is used as a known fact with no reference and no statement of what general position means. |
| 13 | Keep the calculation specific to this proof | pass | `B = I + ℓ` with both halves of bijectivity named. |
| 14 | Audit notation by type and scope | **fail** | `w`: vertex in `δ(v,w)` and Figure 3(c), white face in Section 4, number of white triangular faces in Proposition 5.2. `h`: cycle length and height. `b`: root, real number in Lemma 4.7 and Proposition 4.8, number of black triangular faces. `c`: root and number of cycles, next to `c_t` and `C`. `K`: cycle of `Q_s` and component of `T[U]`. `S`: edge set in Lemma 2.4, vertex set in Section 5, next to `S_s`. `P_0` twice. `D` and the disk `𝖣`. The incidence graph is `ℬ` while `B` counts black faces. There is no notation table. |
| 15 | Each conclusion gets the reason that proves it | pass | Proposition 2.5(1): degree two from one side per face, connectivity from acyclicity. |
| 16 | Distinguish the two reversals first | pass* | Lemma 4.3 and Table 1. The table is never cited in the text and floats into the middle of the definition of `J`. |
| 17 | One example across representations | pass on the rule, **fail** on its check | One triangulation through every step. But "vertex labels and the prescribed edge survive every panel" fails: Figures 4, 6, 7, 8 have no labels while their captions and Example 3.8 name vertices; `e0` and the root `c` are identified only on page 8. |
| 18 | Introduce figures by the question they answer | **fail** for Figures 3 and 7 | Figure 7: "The same selection `P_s` (bold) in the shared figure style." Most in-text introductions are of the form "Figure n shows ..." after the fact. Figure 5 is the model: it answers "what are the five numbers on a real cycle". |
| 19 | Readable figures | **fail** for three | Figure 2 (labels 6, 11, 12 on top of dots), Figure 9 (labels 1, 8, 9 on top of wedges), Figure 11(c) (inner octahedron too small). Line styles are used as well as colour, and the wedges are fill against outline, so grey-scale printing works. |
| 20 | Abstract short and causal, title literal | pass* | Six sentences. Sentence 4 carries the whole of Section 4 in one breath and "suitably rooted" says nothing (CR 1, 2). |
| 21 | Keep process out of the manuscript | **fail** in four sentences | "Figure from the shared figure set of this project." "in the shared figure style." "All numbers we state about it were computed by a short script that is independent of the figure code." "unpublished notes written during a collaborative reading of the three papers". |
| 22 | Compare rendered passages when editing | n/a | A rule for edits. `EDITS.md` gives old and new text for each change. |

Count: 13 pass (5 with a blemish), 1 pass on the rule with its check failed (rule 17), 7 fail, 1 not applicable. None of the fails touches the order of the argument.

## (c) Step by step against the three papers

O = OpenAI, L = Li, C = the constructive paper. I read O in full for this review. For L and C I read L's introduction and otherwise rely on the cross-reference table in `research/2026-11-14_fable_dependency-graph/skeleton.md` and on astra's comparison in `research/2026-11-14_astra_referee-combinatorics/REFEREE.md`; where my judgment about L or C rests on those, I say "per skeleton".

| Step | Best of the three | Draft B | Is B clearer? |
| --- | --- | --- | --- |
| Obstacle | O §1: one paragraph, no picture. C opens with the cube (per the style guide). | A paragraph and Figure 1 on the running example. | Yes against O. Level with C. |
| `T` is a simple triangulation | O proves it in the last section, after using it for nine pages. L stays in `G`. | Lemma 2.1, first thing, same argument. | Yes. Placement alone decides it. |
| Target | O: two induced trees (Theorem 2.2), translated back at the very end with a Jordan-curve labelling. L: perfect matching with connected complement, directly. | Selection, Proposition 2.5 with the even-cut proof. | Yes. "One side per triangle, no cycle" is the shortest statement of the target in any of the four texts. |
| Duality lemma | O Lemma 2.1: four lines by contraction. | Lemma 2.4: fifteen lines by parity. | Longer, and self-contained. Level. A reader who knows tree-cotree duality will prefer O's four lines. |
| Where states come from | O defines a state cold in §2. L motivates by the tree it wants. C has the incidence-tree criterion (per skeleton). | Lemma 3.1 reads the state off an acyclic selection. | Yes, clearly. This is the best single improvement. |
| State to selection | O §6.1: spoke graph `H`, "faces of `H` are the white triangles", dual tree, far-end assignment. L: tree-cotree and tracing in `G`. | `Y_s = T* − S_s*`, rooted at `t0`. | Yes against O (one graph fewer). Level with L. |
| Disk identity | O Lemma 4.1: twelve lines, `δ`-sum form. L Claim 25: hexagon count in the spoke graph (per skeleton). | Lemma 3.6 as `W = B + 1`, Figure 5, both halves of bijectivity named. | Yes. Same silence about the disk as O (REFEREE G1). |
| Acyclicity of the selection | O Lemma 6.2: count (6.1) against the `δ`-sum. L: innermost cycle. | Proposition 3.7: `W − B = 1` against `W − B = 3`. | Yes. The sentence "a selection running along it would force three more" has no counterpart in the sources. |
| Why pairs | O introduces pairs in §2 and gives the reason in §5. C: outdegree description. | "Why a second state", Lemma 4.2. | Yes, though the motivation is three sentences and leans on the lemma (CR 44). |
| Two reversals and the sign | O interleaves both in Lemma 5.2 and §5.3. | Lemma 4.3, Table 1, Lemma 4.4, each separate. | Yes. Could be shorter with the product sign (REFEREE S2). |
| Cancellation | O Lemma 5.2: compact and good. | Lemma 4.5 plus the remark on `K_s`. | Level. |
| Weights | O Lemma 5.3 and the slide. L: vertical rays in a straight-line drawing, the most concrete (per skeleton). | Heights by paths to the outer face, winding numbers. | Yes against O: no `H_0`, no slide. Not against L: a ray is easier to picture than a path with a crossing convention, and B has no figure of `γ_w` at all. |
| Nonvanishing | O (5.4): a product over cycles, each factor with a simple zero. This is the most memorable formula in the three papers. C: coefficient of `(z−1)^m`. | Lemma 4.7, finite difference of `ω^m`. | More elementary, not clearer. B loses the product over cycles, and with it the sentence "each cycle contributes one zero". One sentence would restore it: a group is a `c`-fold difference, one difference per cycle, and a `c`-fold difference kills polynomials of degree below `c`. |
| First pair | O Prop. 3.1: correct and terse, placed before its need. L: minimal deficient set and a 3-edge cut in `G`. | Proposition 5.2, same proof with the steps spelled out, placed after its need. | Yes against O. No picture, though the shared set has one (`06-flow`). |
| Gluing | O: glue induced trees along a vertex or an edge, eight lines. L App. C: glue two Hamiltonian cycles across a 3-edge cut, the most intuitive. | Glue selections, full acyclicity proof, Figure 11, one sentence on the primal reading. | Yes against O for completeness. L's picture is still the one to show first. |
| What the hypotheses do | none | Section 7 | Only B has it. |
| Example | O none; C the cube. | One example through every step, with numbers. | Yes. The promise "few enough to list" is not kept. |

Net, over the seventeen rows: B is clearer than the best of the three at eleven, clearer than O but level with L or C at two (obstacle, state to selection), level at two (duality lemma, cancellation), and not clearer at two (weights against L, nonvanishing against O).

## (d) Unslop audit

The draft is already low on AI patterns: no em dashes, no puffery, no "crucial" or "note that", plain verbs. What survives is mostly of one kind, sentences that say how the paper feels instead of what it does (pattern 27), and process talk. Replacements are proposals; exact edits for the important ones are in `EDITS.md`.

| # | Passage | Pattern | Replacement |
| --- | --- | --- | --- |
| 1 | "The proof turns connectivity into a counting problem in four steps, each forced by the one before." | 27: "forced" is not shown | "The proof has four steps." |
| 2 | "Every construction in this paper is there to enforce connectivity." | 27; also not true of Sections 4 and 5 as told | "The rest of the paper finds a perfect matching whose complement is connected." |
| 3 | "it still shows every phenomenon of the proof: a pair whose ..., and two choices ..." | overclaim plus colon as connector (14) | "It shows a pair whose opposite sides contain a cycle and a cycle of `D` that encloses a vertex." |
| 4 | "few enough to list" | promise not kept | add the table (EDITS 16) or cut the phrase |
| 5 | "All numbers we state about it were computed by a short script that is independent of the figure code." | process talk | "The numbers quoted for the example come from exhaustive enumeration." |
| 6 | "Figure from the shared figure set of this project." | process talk | delete |
| 7 | "The same selection `P_s` (bold) in the shared figure style." | process talk | "The selection `P_s` of Figure 6 (bold) and its Hamiltonian cycle." |
| 8 | "In exchange, the four counts of the proof (the disk identity, the acyclicity of the selected edges, the density bound for the first pair and the colour of a cap) become the same count: Euler's formula on a region of `T`, plus a count of edge sides by the colour of their face." | parenthesis as a list holder (13), colon as connector (14), four undefined terms | "Four steps of the proof then use the same two counts, Euler's formula on a region of `T` and a count of edge sides by the colour of their face." |
| 9 | "The second condition is global and awkward to control. A second state takes care of it." | 27 | "The second condition concerns whole components. A second state turns it into the first: by Lemma 4.2, if `s` has a partner then every component of `Q_s` without a cycle contains exactly one root." |
| 10 | "found in unpublished notes written during a collaborative reading of the three papers" | 5: vague attribution | name the notes (section (f)) |
| 11 | "a suitably rooted forest" (abstract) | 27 | "a forest with one corner of the outer triangle in each tree" |
| 12 | "we count pairs of disjoint corner choices with signs: fixing the second choice cancels ..., while grouping ... shows ..." (abstract) | 14 and 28: one sentence carries Section 4 | split into two sentences (EDITS 20) |
| 13 | "Two smaller changes are ours: we obtain ... (in `G` it is Li's 'black dual trace' ... with one extra leaf), and a winding-number argument replaces ..." | 14, 13, 28 | two sentences, no parenthesis |
| 14 | "The `m`-th power is what makes the cycles with fewest cycles count" | typo and 27 | see EDITS 11 |
| 15 | "One picture" as a paragraph heading and as the title of Section 2 | repetition | title Section 2 "The dual triangulation and the target" |
| 16 | "the whole difficulty is to make it a single cycle" | filler word | "the difficulty is to make it a single cycle" |
| 17 | Semicolons: about 60 in running prose, often "X; so Y" or "X; it is Y" (Lemma 3.3 has five in eleven lines) | rhythm: every proof sentence has the same two-clause shape | split about half of them into two sentences |
| 18 | "Figure n shows ..." as a sentence that ends a paragraph (about ten times) | formula | say what to look at: "In Figure 4(a) the dashed sides close a triangle around a white face." |

Things I checked and found clean: no rule-of-three padding, no synonym cycling ("corner choice" in the introduction and "state" in the body is a deliberate before/after and is announced), no hedging, headings in sentence case.

## (e) Figures

Seven shared (Figures 1, 2, 4, 5, 7, 8, 11) and four drawn by the author (3, 6, 9, 10). All floats are `[t]`.

| Fig. | Page | First cited | Scale and legibility at 130 dpi | Placement | Caption | Notation against the text |
| --- | --- | --- | --- | --- | --- | --- |
| 1 two 2-factors (shared 02) | 2 | p. 1 | good size; wavy edges look unlike every later figure; the two cycles of (a) are not told apart | right | ends with process talk | fine |
| 2 dual with labels (shared 03) | 4 | p. 3 | labels small; 6, 11, 12 collide with dots of `G`, 3 and 8 touch edges | right | does not say that the large hollow circles are the roots, nor which side is `e0` | fine |
| 3 local triangle (own) | 5 | (a) p. 5, (b) p. 9, (c) p. 12 | clear | (a) right; (b) four pages early; (c) seven pages early | describes objects not yet defined | in (c) `w` is a vertex and `y` a white face; in Section 4 `w` is a white face |
| 4 `Q_s`, cycle and forest (shared 09) | 6 | p. 6 | clear | right | names vertices 1, 8, 9 that the figure does not label; "disjoint", "pair" before definition | fine |
| 5 disk identity (shared 08) | 7 | p. 7 | clear; the best figure | right, between statement and proof | good; does not say this is the 7-cycle of Figure 8 | the side table ends with "so `2ℓ − h = −3`", O's form; the lemma states `h = 2ℓ + 3` and `W = B + 1`, and the latter is not in the figure |
| 6 recovery (own) | 8 | p. 8 | dense but readable; lighter grey than the shared figures | right | good | fine; no labels although Example 3.8 gives vertex sets |
| 7 selection and curve (shared 13) | 9 | p. 4 | clear | **wrong**: belongs to Example 3.8, lands between Lemma 4.2 and its proof | process talk | panel (a) is O's tree on the white faces; the draft's object is `Y_s` on all faces, so the caption has to explain a translation |
| 8 pair and `D` (shared 07) | 10 | p. 9 | clear | right | names vertices the figure does not label | fine |
| Table 1 | 10 | never | caption glued to the rule | floats into the definition of `J` | fine | fine |
| 9 cancellation (own) | 11 | p. 11 | labels 1, 8, 9 sit on wedges | right | good | fine |
| 10 white faces inside cycles (own) | 13 | p. 12 | clear; the only example figure after Figure 2 with readable labels | splits Example 4.9 | good | fine |
| 11 gluing (shared 14) | 15 | p. 15 | panels small; (c) inner part unreadable; (b) relabelled and rotated | right | good | fine |

Findings.
1. **No figure for heights.** The definition of `γ_w`, `κ_w`, `h_s(w)` is the hardest paragraph in the paper and has no picture. Figure 10 shows `Γ` for Lemma 4.6 but not a path, a crossing or a sign. One panel is needed: the example, one white face, its path to the outer face, the spokes of one state, the crossings marked with their signs, and the same for the state after one reversal. (With the face-path definition of REFEREE S1 the panel is a chain of triangles and needs no spokes.)
2. **Figure 3 should be split.** (a) where it is, (b) at Definition 4.1, (c) at Lemma 4.6 or dropped.
3. **Figure 7 should move** to Example 3.8, or panel (b) alone to Proposition 2.5, where the reader first wants to see an acyclic selection and its Hamiltonian cycle. Panel (a) duplicates Figure 6(a).
4. **Labels.** Either label the thirteen vertices in every example figure or stop naming vertices in captions. The first is better: the summary from memory shows I could not connect Figure 5's cycle to Figure 8's until page 10.
5. **Consistency.** Own figures use a lighter grey for black faces and the collar than the shared ones (compare Figures 4 and 6). Own figures 9 and 10 carry labels, shared 4, 7, 8 do not. Figure 10 is drawn at a different scale from all the others. Wedges, root markers and arrow colours agree.
6. **Unused shared figures that would help**: `06-flow` for Section 5, which has no picture, and `05-state` or `04-local` if they match the notation (I did not open them).
7. **Float specifier.** `[t]` everywhere is why figures split a lemma from its proof (Figure 7) and an example in two (Figure 10). `[tb]` or `[ht]` with `\FloatBarrier` at section ends would stop a Section 3 figure from entering Section 4.

## (f) Attribution

**Framing.** Honest. The abstract says "a 2026 preprint of OpenAI proves it. We give a self-contained account of that proof", and the Sources paragraph opens "This is an exposition of OpenAI's proof" and gives the objects to OpenAI. The title makes no claim.

**Credit to the literature.** Mostly right. Four corrections.
1. "That the stronger statement is equivalent to the conjecture was known before; see Hertel's survey." The result is Kelmans's. O credits "the work of Kelmans as explained by Hertel [7, Corollary 3] and by Gorsky, Steiner, and Wiederrecht [5, Theorem 4.3]", and Hertel himself records Kelmans's priority (`research/2026-11-14_opus_history-literature/EQUIVALENTS.md`, entry 9). Name Kelmans.
2. The reduction to triangulations without separating triangles is also Kelmans's (cyclically 4-edge-connected graphs suffice; `HISTORY.md` section 4). Section 6 of the draft re-proves it in dual form, as O does, and should say so in one sentence.
3. "Li counts lists of `m` marks, which are the terms of `ω(s)^m`" and "the weight `ω^m` that all three papers use" are not accurate. O uses `exp(xω)` and a Taylor coefficient, C a coefficient of `(z−1)^m`, and Li sets of distinct marks, which give an elementary symmetric function and not a power (astra `REFEREE.md`). Say "all three papers extract a term of order `m`".
4. Barnette 1969: the draft cites "D. W. Barnette, Conjecture 5, ... p. 343". O cites the same page as "Grünbaum, Unsolved problem 5 ... Conjecture attributed to David W. Barnette". `HISTORY.md` says nobody in the project has seen the page. Keep the citation and do not present its form as checked.

Two omissions of context that O supplies and a reader may miss: the regrouping of two matchings by the cycles of their union is the standard double-dimer regrouping (O cites Kenyon), and the passage from a matching to a tree is Temperley's correspondence (O cites Kenyon, Propp and Wilson). One sentence each would place Section 4 and Lemma 3.3.

**The project's own unpublished simplifications.** This is the weak part of the paragraph.
- "found in unpublished notes written during a collaborative reading of the three papers; we checked each one" does not say whose notes. A reader cannot tell whether "we" wrote them. If the paper's authors are the project, the notes are the authors' own working notes and the sentence should say so and say where they can be read (the repository and the folder, here `research/2026-11-14_fable_route-combinatorics/PROOF.md` and `research/2026-11-14_astra_referee-combinatorics/REWRITTEN-PROP-5-1.md` according to the author's `REPORT.md`).
- The split between "found in unpublished notes" and "Two smaller changes are ours" is a trace of the multi-agent process and means nothing to a reader. Use one list headed "Departures from [12]".
- Two bullets overstate. "heights at white faces in place of the circulation lemma of [12], which removes the exponential sum and the complex phase": the heights are the weights that O itself constructs in the proof of its Lemma 5.3 (unit circulation from a dual path for each bounded face), read face by face. They do not remove the exponential sum (Lemma 4.7 does) or the complex phase (the real sign of [1] does). Remark 4.10 says it correctly ("for one particular choice of its spoke circulation"); the Sources bullet should match.
- "we obtain the tree of faces `Y_s` ... directly from `Q_s` by duality in `T`" is presented as the draft's own. According to `research/2026-11-14_opus_lean-formalisation/DIFFERENCES.md` item 19, the formal proof released with [12] does the recovery in exactly this way ("the complement in `G` of `Q_s` plus two root sides is a spanning tree of `G` in which every black vertex has degree 2, except the root"). I did not read the Lean source myself. If that note is right, the sentence should say that the same tree appears in the formal proof and in Li's black dual trace, and claim only the presentation.
- The disk identity "in the form one more white face than black" and "the short acyclicity proof" are rephrasings of O's Lemma 4.1 and of its count (6.1). "Form" and "short" are fair words. Keep them modest.

A proposed replacement paragraph is edit 13 in `EDITS.md`.

**Unsigned source.** Reference [1] is "Unsigned manuscript, dated 18 October 2026". The reader needs to be told where it can be found. If it cannot be cited, results taken from it (the real sign, the exact criterion at the end of Section 5) should be proved or marked as quoted without verification. The sign is proved in the draft. The criterion is quoted and not used.
