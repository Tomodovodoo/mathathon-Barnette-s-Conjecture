# Cold read of `paper/main/barnette.pdf`, version 2 (19 pages)

Reader: a graduate student in combinatorics who has never seen the proof. I read the
19 pages rendered at 130 dpi (`renders/before/pNN.png`), in order, before opening any
other project file except `research/BRIEF.md`. Page numbers are PDF pages.

Notes run paragraph by paragraph. **H** marks a hesitation, **F** a figure or layout
note, **D** a dense or insider sentence, **+** something that worked.

## Page 1: abstract, introduction, the plan

- Abstract. **+** It says what is proved (the version that avoids an edge), why
  connectivity is the issue (the complement of a perfect matching has degree two), what
  the dual object is (a selection with no cycle), and gives a one-line picture of the
  method ("a signed count over pairs ... the unsuitable ones cancel ... a second grouping
  shows that it is not zero"). The last sentence about the avoided edge also helps.
- Intro paragraph 1. **+** "Connectivity is the whole problem" plus the cube with two
  squares makes the issue concrete in four lines.
- Theorem 1.1. **+** Clear.
- "Here 3-connected means ..." **+** Explains why `e` is present. Fine.
- "The plan", first paragraph. **+** Clear. The sentence "a cycle would separate the
  triangles inside it from those outside" gives the reason for acyclicity in one clause.
- Plan step (1). **H** "Removing `e0` from the desired selection leaves three trees,
  each containing one corner of `t0`." I accepted this on trust (why three, why one
  corner each?). That is acceptable for a plan, but a parenthetical pointer ("Lemma 3.1")
  would stop me looking for the reason. **H** "The selected side in each other black
  triangle leaves one corner": I read "leaves" first as "leaves out". It means "points
  away from", i.e. the corner is the tail. This cost me a re-read.
- Plan step (2). **D** "They give a tree joining the triangles, which forces a
  selection (panels (d)–(e))." "They" is the opposite sides, but the tree is on the faces
  and is made from the edges *not* avoided. I only understood this sentence after
  Section 3.
- Plan step (3). **+/H** "orients the opposite sides with one edge leaving every vertex
  off `t0`" is fine. I did not yet see why that makes "no cycle" enough; the next
  sentence asserts it. Acceptable.
- Plan step (4). **D** "Grouping by these cycles, with weight increments counting
  enclosed white triangles, proves that the sum is nonzero." This is the main idea of the
  paper and on page 1 it is a compressed half-sentence. I could not say after page 1 *why*
  the second grouping gives a nonzero number. One more sentence ("each cycle of arrows
  can be reversed; reversing flips the sign and raises the weight by the number of white
  triangles inside, which is at least one; so each group sums to a product of these
  positive numbers") would let the idea land on page 1.
- Plan step (5). **+** Clear.

Judgement (a): after page 1 I can say what will be proved and why connectivity is the
problem. I can say why steps 1, 2, 3 and 5 exist. For step 4 I know *that* a signed
count is used but not *why it cannot vanish*.

## Page 2: Figure 1, history, the example

- Figure 1. **+** Six panels in two rows, read along the rows, each panel captioned.
  It is the right figure for the plan. **F** Panel (b): the grey edges of the cube are
  very faint at print size; the small hollow and solid G-vertices are hard to see. **F**
  Vertex labels 0 to 5 are small but legible. **H** Panel (d) caption speaks of "the
  avoided edges", a term not yet defined (it is `S_s`, Section 3). Fine as a preview.
  **+** Panel (e) with the magenta cycle crossing the non-bold edges is the payoff
  picture; it is good.
- History and sources. **D** "as explained by Hertel [9]" occurs four times in one
  paragraph. Reads like a list of citations, not a history. The facts are useful.
- The example. **H** "It has 12 states and 8 pairs" before either word is defined;
  harmless since it is a preview, but a reader notices.

## Page 3: Figure 2, Section 2 opening

- Figure 2. **F** Labels are small (about 7 pt at print size). The label "11" is
  overprinted by a small hollow G-vertex; "7" sits on a hollow G-vertex too. The grey G
  edges add clutter that the later figures (4, 5, 8) drop. The caption is good: it says
  what the collar means and gives the counts.
- "The dual" and Lemma 2.1. **+** Clean. The proof's first paragraph (3-edge-connectivity)
  could announce its goal first ("We first show that `G` is 3-edge-connected"), since the
  reader does not know why edge cuts are being discussed until the second paragraph.
- "From now on `T` is a coloured triangulation". **H** "The next lemma shows that `T`
  is connected." `T` is a dual of a connected plane graph, so this is not where I wanted
  Lemma 2.2. The real reason (the inside of a cycle, the pieces) comes in the next
  sentence. Put the real reason first.

## Page 4: Lemma 2.2, (2.3), the target, Lemma 2.5, Proposition 2.6

- Lemma 2.2. **+** Short topological proof. Fine.
- (2.3). **+** The counts `k`, `3k`, `k+2` arrive when needed.
- Definition 2.4 (selection). **+** Arrives exactly when wanted.
- Lemma 2.5 setup. **H** The notation `M* − N*` (the dual edges crossing edges not in
  `N`) took a moment. It is defined, but the minus sign reads as set difference of two
  graphs that live in different places.
- Lemma 2.5 proof (2). **+** The parity argument around a vertex is clear.
- "A reader who knows plane duality ..." **+** Good escape hatch.
- Proposition 2.6. **+** Clear.

## Page 5: Section 3 start, Lemma 3.1, Definition 3.2, Figure 3, Example 3.3

- Paragraph after Proposition 2.6. **D** "Part (1) says why the target has two
  conditions with two different reasons" is clumsy.
- Section 3 opening. **+** "selections do not depend on the colours" pre-empts my
  question. `A`, `X`, `n` arrive with a reason.
- Lemma 3.1. **+** This is where step (1) of the plan is proved, and it reads well.
- "So the unknown is a choice of one corner ..." **+** Excellent bridging sentence.
- Definition 3.2 and the `Q_s`, `S_s` paragraph. **+** Natural.
- Figure 3. **F** A single triangle occupying about a sixth of a page. It is clear but
  costs a lot of space for little; Figure 7 is the same picture with a pair. Acceptable.
- Example 3.3. **+** The table of two states is very helpful. **F** About 8% of the page
  is blank below the table (Figure 4 did not fit).

## Page 6: Figure 4, the tree of faces, Definition 3.4, Lemmas 3.5, 3.6

- Figure 4. **+** Clear contrast: (a) a cycle, (b) a forest with one root per tree. The
  caption ends with "The proof needs a state that looks like (b)". Good.
- "The tree of faces". **D** One paragraph carries four ideas: a selection avoiding `S_s`
  is a perfect matching of `Y_s`; `Y_s` is a subgraph of `G`; a tree has at most one
  perfect matching; goodness is sufficient but not necessary. I had to read it twice.
  Splitting it after "... no choice is left." would help.
- Definition 3.4, Lemma 3.5. **+** Short, natural.
- Lemma 3.6. **+** The statement is concrete. The proof is long but each sentence is
  checkable.

## Page 7: Figure 5, "the inside of a cycle", Lemma 3.7

- Figure 5. **+** Good. Panel (b) shows the Hamiltonian cycle for the example; the
  disks and squares for the two trees are a nice touch.
- "For a good state Lemma 3.6 produces ..." **+** Clear statement of what is left.
- "The inside of a cycle". **H** The state is suddenly called `r`, not `s`. I stopped to
  ask whether this is a new object. The reason (Section 4 applies the same facts to the
  first state of a pair) is not given. One clause would fix it.
- Lemma 3.7. **+** Clean, and the proof is two lines.
- "The chosen sides have outdegree one ..." **+** Defines `B, W, I, ℓ` and points to
  Figure 6. **F** Page 7 ends about 10% blank because Figure 6 moved on.

## Page 8: Figure 6, `R_Z`, Lemma 3.8 (disk identity)

- Figure 6. **+** The best figure in the paper: the picture, the five counts in a side
  column, and the three equations. This is where the disk identity lands.
- `R_Z` paragraph. **D** Technical; most readers will skip it, which is fine because it
  only justifies Euler's formula.
- Lemma 3.8 and proof. **+** Three counts, each one line. The closing paragraph
  ("Only the third count uses the state ... both halves of bijectivity") is exactly the
  insight a reader wants.

## Page 9: Proposition 3.9, Example 3.10, Section 4 opening, Definition 4.1, Figure 7

- "The selection has no cycle" and Proposition 3.9. **+** The proof is clear, and the
  sentence "In words: a cycle of chosen sides encloses one more white face than black,
  but a selection running along it would force three more" is excellent.
- Example 3.10. **H** "On the cube (Figure 1), with `t0 = {0,1,2}` and `e0 = {0,1}`, both
  states are good; for `s` the tree `Y_s` makes ..." Which two states? I guessed the two
  states of Figure 1(f), and that `s` is the solid one, but neither is said.
- "So Theorem 1.1 follows once ..." **+** Good signpost.
- Section 4 roadmap. **+** Four steps with lemma numbers. Very helpful.
- "Why two states". **H** "Another state `r` that differs from `s` in every face turns
  it into the first." "It" is the second condition, "the first" is "no cycle". I parsed
  it on the second try.
- Figure 7 with side caption. **+** Good, and placed between the definition and the
  lemma, not inside either.
- Lemma 4.2. **+** Clear.

## Page 10: `D(r,s)`, Figure 8, Lemma 4.3

- `D(r,s)` paragraph. **+** Clear; the last sentence ("So the disk identity applies to
  every cycle of `D(r,s)` and to every cycle of `Q_s`") is the hinge of the section, and
  it is stated.
- Figure 8. **F** A legend line under the drawing ("Outlined: first state β; solid:
  second state α") repeats the caption. Remove one. The figure is large (half a page)
  and clear.
- "In the example (β,α) is a pair ..." **+** Fine.
- Lemma 4.3. **+** Fine. **F** Page ends about 10% blank.

## Page 11: the sign, Lemma 4.4, Table 1, cancellation, Lemma 4.5

- "A sign." **+** This is where "why a signed count" lands: "Reversing a cycle of
  `Q_s` pairs them up, so we need a sign that this reversal changes." Then `δ`, and the
  disk identity makes the δ-sum on a cycle ±3, hence odd. I understood why the sign
  flips. Good.
- Lemma 4.4. **+** Fine.
- Paragraph after it. **+** "a sign defined by counting the cycles of D would not be
  controlled" answers my next question.
- Table 1. **+** Useful summary of the two reversals.
- Lemma 4.5. **+** Clear, and the remark that `K_s` must depend on `s` alone is the right
  warning.
- "In the example only α has a cycle in `Q_α`". **H** The example has 12 states and 6 are
  good, so 6 are not good. "Only α" must mean "only α among the second states of pairs".
  Say so.

## Page 12: Figure 9, heights, Lemma 4.6

- Figure 9. **+** Good choice to enlarge the three affected faces.
- "Heights", first paragraph. **+** The motivation is right: with `F = 1` the sum
  vanishes because reversing a cycle of `D` also pairs things off, so `F` must tell the
  two orientations apart, and the disk identity guarantees a white face inside. This is
  the second half of the main idea and it is stated.
- Path of faces and `κ`. **D** The "in combinatorial terms" sentence (`v, a', b'` in
  counterclockwise order) is hard to read; I skipped it and used the left/right picture.
- "Reversing a clockwise cycle C of D raises the height ..." **+** The intuition before
  the lemma. Good.
- Lemma 4.6 proof. **H** Case analysis that takes more than a minute. It is correct as
  far as I can follow; Figure 10 helps.

## Page 13: Figure 10, "the total is not zero", Lemma 4.7

- Figure 10. **F** The circled ± signs are small. The caption is eight lines and reads
  as a second proof. It works, but I would cut it to what to look at.
- "Since `η_s(y)` is a sum over faces ..." **+** Necessary sentence.
- "The total is not zero." **H** This is the climax and it gets one paragraph of six
  lines. "Here is why a power." is abrupt. The key image (a class of pairs is a cube
  `{0,1}^c` of orientations; the signed sum is a `c`-fold finite difference; a difference
  of a degree-`c` polynomial is `c!` times the product of the steps; each step is the
  number of white faces inside a cycle, at least 1) is all there, but compressed. A
  one-cycle warm-up (two orientations contribute `ω₀` and `−(ω₀ + L)`, total `−L ≠ 0`)
  would let the idea land before the general case. Judgement (c): the "why signed"
  moment has room and a picture (Figure 9); the "why nonzero" moment is cramped, and its
  picture (Figure 11) comes a page later and is a grid of numbers.
- Lemma 4.7. **+** Clean.

## Page 14: Proposition 4.8, Table 2, Example 4.9, Figure 11

- Proposition 4.8 proof. **+** Clear given Lemma 4.7.
- "The minimum cannot be dropped" **+** Good.
- Table 2 and Example 4.9. **+** The arithmetic `16 − 9 − 4 + 9 = 12`, `4 − 1 − 1 + 4 = 6`,
  `Σ = 18` is satisfying. I checked it against `2·(6·1 + 3·1) = 18`.
- Figure 11. **F** The boxes repeat Table 2; text in the boxes is small. It does show
  the two rows and the cancelling pair. It would carry more if it showed the
  difference structure (ω values ω₀, ω₀+L₁, ω₀+L₂, ω₀+L₁+L₂) rather than copying the table.

## Page 15: Remark 4.10, Section 5, Figure 12

- Remark 4.10. **D** For experts. "the phase `i^J`" and the exponential sum are not
  needed by the reader of this paper. Acceptable as a remark.
- Section 5 opening. **+** Short, and the reduction to a flow is easy.
- Figure 12. **F** Cluttered: the double orange and solid blue edges cross each other
  many times, the thin incidence edges are very faint, and the grey highlight that
  marks the tight set `S = {2}` is barely visible. The capacity labels "2" and "1" are
  small. It tells me the network is bipartite between `X` and `A`, which I knew.

## Page 16: Proposition 5.2 proof, Section 6 opening, Lemma 6.1

- Proposition 5.2 proof. **+** "This is a planar edge count" is the right orienting
  sentence. **H** The step `bal(Ψ) ≤ dΨ − 4` by cases took me more than a minute.
- Equation numbering (5.1), Proposition 5.2, (5.3). Fine but odd at first glance.
- Section 6 opening, Lemma 6.1. **+** Fine.
- **F** About 20% of page 16 is blank: Figure 13 moved to page 17. Close to the limit.

## Page 17: Figure 13, Theorem 6.2, proof of Theorem 1.1, Section 7 start

- Figure 13. **+** Small concrete gluing. **H** Caption (c): "its trees meet those of the
  pieces in the edge {3,5} or in the vertex 4" — I could not parse which trees meet
  which.
- Theorem 6.2 proof. **+** Clear. The paragraph after it ("The prescribed edge is what
  makes the gluing work") is the right closing sentence for the induction.
- Proof of Theorem 1.1. **+** Three lines; satisfying.

## Pages 17 to 19: Section 7

- "How this account differs". **+** Useful for a reader of the sources. **D** For a
  newcomer it is a list of names.
- "Which Hamiltonian cycles arise". **+** Interesting and short.
- "Why each hypothesis is needed". **+** Good idea. **D** The *Cubic* and *3-connected*
  paragraphs each contain a long connectivity verification of an example graph (about
  ten lines on the bipyramid incidence graph, six on the 26-vertex graph). They read like
  answers to a referee and bury the point of each paragraph.
- "The polynomial behind the count". **+** Nice reformulation. **H** "spoke weights `𝔞`"
  is never defined in this paper.
- "No polynomial-time construction is known." **+** Honest and short.
- "Consequences and open questions". **+** Useful. **H** The last sentence ("Two
  companion notes give a primal formulation and an account using two sign-reversing
  involutions") has no citation; I cannot find these notes.

Judgement (e): the closing section is useful, but two verification passages inflate it.

## Summary of the judgements asked for

(a) After the abstract and page 1: what is proved, yes; why connectivity, yes; why each
step exists, yes for steps 1, 2, 3, 5, and only partly for step 4 (the "why nonzero"
half is compressed).

(b) Definitions mostly arrive when wanted. Misses: `r` in "the inside of a cycle" without
a reason; "avoided edges" in Figure 1 before `S_s`; "spoke weights 𝔞" never defined;
the two states of the cube in Example 3.10 never named.

(c) "Why a signed count" lands well (A sign, Lemma 4.5, Figure 9). "Why it cannot vanish"
is stated correctly but in one cramped paragraph without a warm-up and without a
picture of the mechanism.

(d) The α/β thread carries me: Figures 4, 5, 6, 8, 9, 10 and Table 2 all use the same
example and each answers a question I had. Figure 10's caption is too long; Figure 11
repeats Table 2; Figure 12 is cluttered.

(e) Section 7 is useful; trim the two connectivity checks and fix the uncited closing
sentence.

Floats: no float sits inside a statement or proof. Blank space: no page is more than a
quarter blank; page 16 (about 20%) is the worst.
