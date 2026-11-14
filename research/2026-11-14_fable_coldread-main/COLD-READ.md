# Cold read of `paper/main/barnette.pdf` (18 pages)

Read on 2026-11-14 from page images only (PyMuPDF, 130 dpi, `pages/p01.png` to `pages/p18.png`; zoomed crops of Figures 1, 2, 3, 9, 10 at 200 to 280 dpi). No other project file except `research/BRIEF.md` was open while these notes were taken. I had not seen any of the three source papers.

Tags: **H** hesitated. **E** expected one thing, got another. **Q** question in my mind. **U** term or symbol used before its definition, or hunted for. **P** object without a stated purpose. **S** proof step I could not follow within a minute. **F** figure. **L** float or layout. **W** wording (dense, insider, or machine-sounding).

---

## Page 1

### Title block

- **W** No author line. The page gives a title, an abstract, a date and an MSC code. A reader cannot tell who is speaking when the text says "we" and "our account".

### Abstract (seven sentences)

1. "A spanning subgraph in which every vertex has degree two need not be a single cycle." **E** I expected the first sentence to say what is proved. This one states a difficulty before the problem has been named. Barnette's conjecture is named only in the title.
2. "We explain OpenAI's proof that every cubic, bipartite, 3-connected planar graph has a Hamiltonian cycle avoiding any given edge, working in the dual triangulation, where such a cycle is an acyclic set of edges containing exactly one side of every triangle." **H** "such a cycle is an acyclic set" reads as a contradiction on first pass. It took a second reading to see that the cycle lives in the graph and the acyclic set in the dual. **U** "the dual triangulation".
3. "The set is built from a choice of one corner in each black triangle, provided the sides opposite the chosen corners form a forest with one corner of the outer triangle in each tree." **U** "black triangle" (no colouring has been mentioned), "the outer triangle".
4. "A signed count of pairs of corner choices that differ in every triangle cancels the pairs whose opposite sides contain a cycle, while heights at the white triangles show that the count is not zero." **U** "heights at the white triangles", "white". **Q** A count of what, weighted how, and why would a nonzero count give me the forest of sentence 3? The inference (nonzero total, bad terms cancel, so a good term exists) is left to the reader.
5. "A prescribed edge lets the construction pass across separating triangles." **U** "separating triangles". **H** "a prescribed edge": sentence 2 said "avoiding any given edge". Is the prescribed edge the avoided one? (It is its dual, as I learned on page 4.)

Verdict: the abstract is not comprehensible on its own. It has five undefined terms (dual triangulation, black/white triangle, outer triangle, heights, separating triangle) and its logic is carried by the reader. A graduate student gets "they prove Barnette's conjecture in the dual by choosing corners and counting something with signs" and nothing firmer.

### Introduction, paragraph 1

"A Hamiltonian cycle is a connected spanning subgraph in which every vertex has degree two. In a cubic graph the degree condition is the easy half. ... Connectivity is the whole problem." Clear, and the best paragraph on the page. This is the right first principle. **F** It cites Figure 1(a), which is on the next page.

### Theorem 1.1 and the paragraph after it

Clear. "The edge e is there for the induction of Section 6, which cuts G into smaller graphs and needs their cycles to agree on the cut" tells me why the theorem is stronger than the conjecture. Good.

- **W** "That the version with e is equivalent to the conjecture goes back to Kelmans, as explained by Hertel ... and by Gorsky, Steiner and Wiederrecht": fine, though it delays the plan by two lines for a point the newcomer does not need yet.

### "The plan" (one paragraph, 14 lines, 9 sentences)

Sentence by sentence:

1. "We work in the dual triangulation T of G, whose triangles are coloured black and white by the two classes of G (Figure 1(b))." **U** The dual is defined on page 2 ("The dual"). Here I had to supply it: one vertex of T per face of G, one triangle of T per vertex of G. The sentence does not say that triangles of T are vertices of G, which is the dictionary every later sentence uses.
2. "A perfect matching of G is a set of edges of T containing exactly one side of every triangle, and its complement in G is a single cycle exactly when this set has no cycle (Section 2)." Clear once sentence 1 is unpacked. This is the key reduction and it is stated well.
3. "Fix a black triangle t0 containing the edge e0 of T that crosses e." Fine.
4. "Such an acyclic set chooses, in every other black triangle, one corner, and uses every vertex off t0 exactly once; we call such a choice a state." **H** How does a set of edges choose a corner? Which corner? Nothing here says. (Page 5: orient the forest towards t0; the corner is the tail.) "Uses every vertex off t0 exactly once" is unexplained and I could not reconstruct it.
5. "Conversely a state s yields an acyclic set whenever the sides opposite the chosen corners form a forest with one corner of t0 in each tree (Section 3, Figure 1(d)–(f))." **Q** Why the opposite sides? The set I want contains sides at the chosen corner; the condition is on the sides it avoids. No hint of the reason (the avoided sides form a spanning tree, and the dual tree forces the set).
6. "A second state r that differs from s in every triangle orients these opposite sides and reduces the condition to 'no cycle'." **H** Dense. How does r orient a side opposite s(t)? I read it three times and moved on.
7. "Counting such pairs with a sign, the pairs whose opposite sides contain a cycle cancel, and a regrouping by the cycles along which r and s differ (Figure 1(c)) shows that the total is not zero as soon as one pair exists (Section 4)." **H** "the cycles along which r and s differ" has no meaning yet: two corner choices differ in triangles, not along cycles. **Q** Which count? The sentence hides that the count carries a weight, and that the weight is the whole difficulty.
8. "A flow argument gives one pair when T has no separating triangle, that is, no triangle with vertices on both sides (Section 5)," Fine. This is the only definition of "separating triangle" in the paper (see pages 14 to 16).
9. "and separating triangles are removed by cutting T into smaller triangulations whose solutions agree along the prescribed edge (Section 6)." Fine.

Verdict on "The plan": too compressed. Sentences 4 to 7 hold the whole proof in four clauses, each of which needs an object that has not been shown. After reading it I could say the outline in the order of the sections (dual; corners; pairs and a signed count; flow; cutting). I could not say why opposite sides matter, why a second state appears, what is counted, or why a count proves existence. A numbered list with one line of reason per step would cure most of this.

### "History and sources" (begins page 1, ends page 2)

- **W** One paragraph of 20 lines that mixes three things: the history of the conjecture, credit for the objects, and a comparison with two other expositions. The first is for everyone. The other two are for a reader who already knows the three papers.
- **U** "the disk identity", "the cancellation for a fixed second state", "the regrouping by cycles", "heights": all named here as credits before any of them exists for the reader.
- **W** "An unsigned manuscript [5] uses a real sign and an integer polynomial, describes partners by outdegrees, and gives an exact criterion for the existence of a pair and an enumeration algorithm." Insider shorthand. "Partners" is defined on page 9.

## Page 2

### Figure 1 (six panels, top of page)

- **F** Works as an overview only after Section 3. On first contact, panels (a) and (b) are readable and panels (c) to (f) are not: their subcaptions are "two states and D", "Q_s, opposite the wedges", "S_s and the tree of faces", "P, two trees, one cycle". D, Q_s, S_s and P are all undefined at this point.
- **F** Scale. The six panels occupy about 600 of the 815 pixels of text width, each disk about 190 px (37 mm). At that size the outlined wedges of r in (c) are a few pixels across.
- **F** Collision. The subcaptions of the top row sit directly on the vertex label "2" of the bottom row. There is no vertical gap between the rows.
- **F** Nothing ties (a) to (b). The cube in (a) is drawn alone, in a smaller frame, and the octahedron in (b) alone. The claim "its dual" is not visible: no cube vertex sits in an octahedron face. The one picture that would teach duality (the cube drawn in grey over the octahedron) is missing here, though Figure 2 does it for the big example.
- **F** The grey collar for the outer face is a good device, but it is explained only inside a long caption. I first read the collar as decoration.
- **F** (e): the double ring on one green node is not explained in the caption. (In Figure 6 it is: the root face y0.)
- **F** (f): square and round vertex marks are not explained in this caption. (Figure 6 again.)
- **F** Caption: 10 lines. It reads as a second copy of "The plan" using symbols the plan avoided.
- **L** The figure sits inside the "History and sources" paragraph, which breaks across the page in mid-sentence ("An unsigned manuscript [5]" / "uses a real sign").

### "Our account differs from [16] in four places ..."

- **W** The most insider paragraph in the paper, on page 2. "This removes the spokes, the sliding argument of [16, Section 5.3] and the exponential sum." "In G it is Li's black dual trace [15, Section 6] with one extra leaf." None of these objects is in this paper. A newcomer learns nothing and is made to feel late.
- **Q** Is this an exposition of a known proof or a new proof? The paragraph says both: "We explain OpenAI's proof" in the abstract, "each proved in full below" here.

### "The example."

Good idea, welcome. **E** "all listed in Table 2": Table 2 is cited here, eight pages before it appears and before Table 1.

- **W** "Among them are a state whose opposite sides contain a cycle and two states that differ along a cycle enclosing three vertices." The second half cannot be parsed yet.
- **W** "The numbers quoted for the example come from exhaustive enumeration." Fine, though it is a sentence about process.

### Section 2, "The dual" and Lemma 2.1

- Definition of the dual: clear, and this is where the plan's first sentence wanted to be.
- **E** After the plan I expected the dictionary (vertex of G = triangle of T; edge = edge; face = vertex) in one displayed line or small table. It is given in prose only.

## Page 3

### Proof of Lemma 2.1

- **S** "One vertex has three edges leaving it, and two vertices have at least four, since G is simple. So |U| ≥ 3". This means "a set U of one vertex sends out three edges and a set of two sends out at least four". As written, "one vertex has three edges, two vertices have at least four" reads as a statement about degrees. I needed two passes.
- The rest is fine. It is standard and takes 12 lines before any idea of the proof has been seen.

### "From now on T is a coloured triangulation ..." and Lemma 2.2

- **P** Lemma 2.2 (a sphere graph whose faces are bounded by cycles is connected) has its purpose stated: "We use it again for the inside of a cycle and for the pieces of Section 6." Good.
- **U** The lemma calls its graph R. Harmless here; later the outer corners are "the roots", and the graph inside a cycle is R_Z.
- **E** A newcomer who came for the idea has now read a page of point-set care (open sets Ω, Ω′) and has not yet met a corner choice.

### Equation (2.3), "The target", Definition 2.4

- Clear. "A selection matches each black face with the white face across its selected side, so it has k edges." Good sentence, and it is used again in Proposition 3.9.
- **H** "For a plane graph M and N ⊆ E(M) write M* − N* ...": the lemma is stated for a general plane graph M with no reason given. I expected "P is acyclic if and only if the rest of G is a Hamiltonian cycle" directly. (The generality is needed once, in Lemma 3.6, where N is a spanning tree and not a selection.) One clause would settle it: "We state it for any edge set N because it is used for P here and for S_s in Section 3."

### Lemma 2.5 (duality)

- Statement clear. Proof (1) clear.
- **S** Proof (2), the Φ argument, is correct but long for a fact most readers know. The remark that follows on page 4 ("A reader who knows plane duality may prefer the classical proof") admits this.

## Page 4

- **L** Figure 2 sits in the middle of the proof of Lemma 2.5(2): the proof starts on page 3, the figure takes the top of page 4, and the last four lines of the proof follow the caption.

### Figure 2 (the example)

- **F** Half the text width. It is the base picture for seven later figures and deserves more.
- **F** Label collisions: the labels 6, 11 and 12 (white boxes) sit on top of white vertices of G; a hollow dot is visible behind "6" and behind "11".
- **F** Label placement is inconsistent: "9" is far below-right of its vertex inside a black face, "2" is up-left, "1" is left. I had to trace edges to be sure which dot is vertex 9.
- **F** G in grey is drawn with S-shaped curves that weave through the faces. It doubles the ink and is used only once, to show what the dual is. The edges of G at the outer vertex run inside the collar as a second concentric arc and read as part of the frame.
- **F** Caption: good and complete.

### End of proof of Lemma 2.5, the remark, Proposition 2.6

- Proposition 2.6(1) is the statement I wanted on page 3. Proof clear.
- **S** 2.6(2): clear within a minute.
- "Part (1) says why the target has two conditions with two different reasons: one side per face gives degree two, and acyclicity gives connectivity." Excellent sentence. It would serve the introduction.
- **F** "Figure 6(b) shows one in the example": a forward reference of five pages.

### Section 3 opening

"Fix a face t0 of T and one of its sides e0 = ab, and let c be the third corner of t0. ... We draw t0 as the outer face, so" (sentence continues on page 5 after Figure 3).

- **U** The letter c is fixed here as a vertex. On pages 10 to 13 c is the number of cycles of D(r,s).

## Page 5

- **L** Figure 3 opens the page and cuts the sentence "We draw t0 as the outer face, so / that 'inside' a cycle means ...".

### Figure 3

- **F** Small: two triangles about 30 mm wide in a 150 mm text block, with labels (x, y, s(t), Q_s, D(r,s)) visibly smaller than the caption type.
- **F** Panel (b) belongs to Section 4. Its caption uses "pair", "partner" and D(r,s), all defined four pages later. At this point only (a) can be read.

### Roots, A, X, n; "Where the corner choices come from"; Lemma 3.1

- This is the best-motivated passage in the paper. The definition of a state is derived from the target: take an acyclic selection, orient it to the roots, read off a corner per black face. "So the unknown is a choice of one corner in every face of A that uses every vertex of X once." I expected a definition and was given a reason for it.
- **S** Proof of 3.1: clear.

### Definition 3.2 and the paragraph after it

- Clear. "The third side of t, opposite s(t), is excluded" answers the plan's unanswered question (why opposite sides) in one line. S_s = Q_s ∪ {ac, bc} has a stated meaning ("the set of edges that every such selection excludes").

### Example 3.3

- **H** The table header names faces by concatenated corners: "4 10 11", "5 6 11", "6 7 12", "8 11 12", "8 9 10" print as 41011, 5611, 6712, 81112, 8910 with slightly wider gaps. I misread 81112 at first.
- **L** The table is unnumbered and inline, which is right for its size.

### "The tree of faces."

- **Q** "So consider the graph Y_s = T* − S_s* ... For this graph to be a tree we need the following condition on s." Why do I want it to be a tree? The reason (a tree has at most one perfect matching, and here exactly one, read off from the leaves) is never stated before Lemma 3.6. It appears in passing on page 17 ("a tree has at most one perfect matching"). This is the least motivated step of Section 3.
- **U** Y_s: nodes are faces of T. The word "node" is introduced silently for vertices of G.

### Definition 3.4, Lemma 3.5

- Clear.
- **L** The statement of Lemma 3.5 ends the page; Figure 4 opens the next; the proof follows the figure.

## Page 6

### Figure 4

- **F** Good figure, correctly placed against Example 3.3 (one page late). Full width, two panels.
- **F** Vertex labels are small and several sit on wedges or edges (1, 7, 9, 3, 10).
- **F** Caption ends "The proof needs a state that looks like (b)." Good: it says what to see.

### Lemma 3.6

- **S** The statement is clear. The proof took me a little over a minute at "Any other side of y would be shared with a black child t of y, and the side that t selects is shared with the child of t, which is not y". A picture of Y_s on the example would carry it; that picture is Figure 6(a), three pages later.
- **Q** "It remains to see that P_s has no cycle. A cycle in P_s \ {e0} would be made of sides leaving chosen corners". What about a cycle through e0? (Answered at the end of the proof of 3.9.)

### "The inside of a cycle."

- **W** "Let r be a state (we will apply this to both states of a pair, which is why it is called r)". An apology for notation in mid-definition. It also does not explain the choice: the lemma is first applied to s.
- **W** "One principle about them is used four times." I could not check the count and it gives me nothing.
- Lemma 3.7 (outdegree): clear. **U** F is a set of directed edges here; on page 11 F is a function on states; on page 15 F is a face of H; on page 17 F(w) is a polynomial.

## Page 7 (text only)

### Set-up of the disk identity

- **H** Five quantities (B, W, I, ℓ, h) are introduced in one sentence with no picture on the page. Figure 5, which shows exactly these five numbers, is on the next page, after the proof.
- **W** "A vertex strictly inside Z has all its faces inside Z, so no vertex is pinched between the two sides." I do not know what "pinched" means here or what the sentence is for.
- The R_Z paragraph is careful and clear, but it stands between the definition of the five numbers and the lemma that relates them.

### Lemma 3.8 (disk identity)

- **U** "In this situation W = B + 1 and h = 2ℓ + 3." The statement cannot be read alone; "this situation" is the two paragraphs above. This is the lemma the whole paper turns on, and it is cited eight more times.
- **S** Proof: three counts, each followed in under a minute. The closing remark ("Only the third count uses the state, and it uses both halves of bijectivity") is helpful.

### "The recovered selection has no cycle." and Proposition 3.9

- **L** A run-in heading with no text of its own, followed at once by a proposition.
- **U** "recovered": the selection was "produced" on page 6.
- Proof clear. "In words: a cycle of chosen sides encloses one more white face than black, but a selection running along it would force three more." The best one-line explanation in the paper.

## Page 8

- **L** The lower 40 percent of the page is blank. Section 4 starts on page 9 below Figure 6.

### Figure 5

- **F** The best figure in the paper: one cycle, the five numbers listed beside it, the three equations under them. It arrives a page after the proof it illustrates.
- **H** "the corners chosen by the state β (outlined wedges)". In Figure 4(b) the corners of β are solid wedges. The convention (outlined for the first state of a pair, solid for the second) has not been stated yet; it arrives with Figure 7.
- **F** "it is the long cycle of Figure 7": forward reference.

### Example 3.10 and the closing paragraph of Section 3

- Clear. "So Theorem 1.1 follows once we find a good state, and once we can deal with triangulations that have none. Section 4 finds a good state from a pair of states, Section 5 finds a pair when T has no separating triangle, and Section 6 removes separating triangles." This is the signpost I wanted, and it lands at the right moment.

## Page 9

### Figure 6

- **F** Two pages late. It illustrates Lemma 3.6 (page 6) and Example 3.10 (page 8) and appears at the head of Section 4.
- **F** (a): the labels 6, 12, 11, 7, 3 are crossed by the green tree or by bold edges.
- **F** Caption good; it explains the ring and the squares that Figure 1 left unexplained.

### "Why a second state."

- Good: "Goodness asks two things of Q_s: no cycle, and one root per component. ... A second state r that differs from s in every face turns it into the first".
- **H** Name clash. The heading and the third sentence call r "a second state". Definition 4.1 then says "we call r a partner of s, and s the second state". So "second state" means r for three lines and s for the rest of the paper.
- **Q** I am not told the plan of Section 4. I know a pair turns "good" into "Q_s acyclic". I do not know that the section will (i) define a sign, (ii) cancel the pairs with cyclic Q_s, (iii) weight the count, (iv) show the weighted count is not zero. Each piece arrives with its own local motivation, which is good, but the overall argument (a nonzero total with all bad terms cancelling forces a good term) is never stated before it is carried out.

### Definition 4.1, Lemma 4.2

- Clear.

### "Besides Q_s a pair gives the set D(r,s) ..."

- **P** D(r,s) is introduced with "Besides". No purpose is given. Its use (the second way to change a pair, and the grouping that makes the sum computable) appears a page later.
- The derivation that D is a disjoint union of directed cycles covering X is clear.

### "Two reversals." and Lemma 4.3

- **L** The statement of Lemma 4.3 begins at the foot of page 9 ("Let (r,s) be a pair.") and its two items are on page 10 below Figure 7 and Table 1. A reader at the foot of page 9 sees a lemma with no content.

## Page 10

### Figure 7

- **F** Panel (a) is panel (b) without the arrows. One panel would do.
- **F** Twenty wedges and thirteen labels in a 70 mm disk; labels 1, 3, 7, 9, 10 sit on wedges. The arrowheads of the 7-cycle are hard to find, so its direction is not readable without the caption.

### Table 1

- **U** Its columns use "sign" (defined ten lines below), "F(s)" (defined on page 11) and "the sum" (page 13). As a summary after Lemma 4.5 it would be useful. Here it is a preview in undefined terms, inside a lemma statement.

### Lemma 4.3 items and proof

- Clear.

### "A sign."

- Good motivation: "We want to count pairs so that the pairs with cyclic Q_s cancel. Reversing a cycle of Q_s pairs them up, so we need a sign that this reversal changes."
- **S** "the sum of δ along Z is ℓ − (h − ℓ) = 2ℓ − h, and by the disk identity a counterclockwise cycle of chosen sides has δ-sum −3 and a clockwise one +3." Clear, and a nice restatement of the disk identity.

### Lemma 4.4

- **U** "D(r,s) has c cycles": c was the third root.
- **L** Figure 8 splits the proof (it starts on page 10 and ends on page 11 below the figure).

## Page 11

### Figure 8

- **F** Two full disks that differ in three outlined wedges around the triangle 1, 8, 9. I had to compare the panels wedge by wedge. A close-up of the three faces around that triangle, before and after, would show the move at once.

### Rest of the proof of 4.4 and the remark after it

- **S** The parity computation is clear.
- "The reversal of a cycle of Q_s can rearrange the cycles of D completely, so a sign defined by counting the cycles of D would not be controlled." Useful.

### "Cancellation." and Lemma 4.5

- **L** Again a run-in heading with no text before the lemma.
- **Q** "for every function F on states": why a weight F at all? The answer is the first paragraph of "Heights" on page 12, one page later.
- Proof clear. The remark on choosing K_s from s alone is good.

## Page 12

### Figure 9

- **F** Appears before heights are defined (the definition is below it on the same page; acceptable).
- **H** The two panels are in reverse order. The caption says (a) is "the pair obtained from (β, α) by reversing the 7-cycle" and (b) is "the pair (β, α)". The subcaption of (b) says "reversed". So both panels are called reversed.
- **F** The path of faces has a long hairpin inside the face {0, 1, 6} that looks like a second crossing.
- **F** Caption: 10 lines, and it carries the definition of height before the text does.

### "Heights."

- First paragraph: very good. "With F = 1 the answer is no, since reversing the cycle of D(r,s) through a fixed vertex pairs every pair with one of opposite sign. So F must tell apart the two orientations of a cycle of D." This is the question I had on page 11.
- **S** Definition of κ_y(t, v): followed, slowly. Three cases and a parenthetical combinatorial restatement in one paragraph.
- **U** Greek letters in use by now: α, β (two states), γ (a count in 3.7), δ (local sign), ε (sign of a pair), η (height), κ (turn), ω (weight), Σ, Δ, Φ, Ω, and ξ on page 17. η and ω are not mnemonic.

### Lemma 4.6

- **S** The proof (pages 12 to 13) is the one place where I did not get every step within a minute. "Either the path entered across r(t)u(t) and turns around r(t), which is then on its left, or it entered across s(t)u(t) and turns around s(t), which is then on its right. In both cases the summand is +1." I verified it by drawing a triangle. A small figure of one black triangle with the edge g and the two possible paths would make it immediate.

## Page 13 (text only)

- **W** "These heights are the weights that OpenAI construct in the proof of [16, Lemma 5.3] for one choice of their circulations, read face by face, and they are the half-ray counts of Li [15, Section 4] taken along fixed paths." A source note inside the argument.

### "The total is not zero."

- "Here is why a power." followed by a clear explanation (repeated differences). Good.
- Lemma 4.7: clear.
- Proposition 4.8: clear, and the grouping "by the undirected edge set of D(r,s)" is explained well.
- **E** I expected a picture or table at this point showing the same pairs grouped two ways: by second state (where the bad ones cancel) and by undirected D (where each class contributes a product). Table 2 has the data but shows only the second grouping; the first is hidden in the last column.
- "The minimum cannot be dropped ..." Good.

## Page 14

### Table 2 and Example 4.9

- **L** The table splits Example 4.9 across the page break.
- Clear and checkable: 16 − 9 − 4 + 9 = 12.

### Remark 4.10

- **W** Insider, but placed in a remark, which is the right place.

### Section 5 opening

- Clear and well motivated: "States are the perfect matchings of ℬ. A spanning subgraph of ℬ with all degrees two ... splits it into two states that differ in every face".
- **L** Figure 10 is cited here and printed on the next page, inside the proof of Proposition 5.2.

### Proposition 5.2

- **U** "separating triangle" has no definition in Section 5 or Section 6. The only one is the clause in "The plan" on page 1.
- **S** The rewriting of (5.1) as (5.3) is a computation I could verify but not anticipate. **Q** What does e(U) − b(U) ≤ 2|U| − 4 mean? It looks like a planar edge bound; one sentence saying so would help.

## Page 15

### Figure 10

- **F** The triangle labels on the right are struck through by the edges to the sink: {0,2,3}, {3,4,9}, {8,9,10}, {4,10,11}, {0,1,6}, {6,7,12}. The label 12 on the left is overprinted.
- **F** The picture shows a solution. It does not show the capacities on the edges (they are column headings) or a cut.
- **L** It splits the proof of Proposition 5.2.

### Rest of the proof of 5.2

- **S** Followed with effort. Symbols p, q, f, d, f•, f◦, d_F, bal(F), b_H in two paragraphs.
- "This is the only use of the hypothesis." Good.

### Section 6

- **U** The disk is a sans-serif D, next to D(r,s) in italic.
- Lemma 6.1: clear.

## Page 16

- **L** Figure 11 splits the proof of Lemma 6.1.
- **F** Figure 11: panel (c), the glued triangulation, shows the inner octahedron at about 6 mm, too small to check the claim of the caption. The inner vertices are unlabelled in (c) though labelled 6, 7, 8 in (b).
- Theorem 6.2 and its proof: clear. The italic run-in claims ("P is a selection containing e0." "P is acyclic.") organise the proof well.
- "The prescribed edge is what makes the gluing work": good closing remark.
- Proof of Theorem 1.1: four lines, clear.

## Page 17, "Remarks"

- **W** "Each remark says whether it is proved here, computed, or open." and the bracketed tags in the headings ("(proved; computed)", "(proved; literature)", "(open)") are a status vocabulary from somewhere else. A paper says "we checked by computer" where it applies.
- **W** "Why each hypothesis is needed" is one paragraph of 19 lines with five italic run-ins. The content is good.
- **U** "The polynomial behind the count": F(w), c(D), w^{C±}, ξ, a(t, v) in seven lines. Readable only with [16] at hand.
- **W** "we have not checked it" (of the algorithm in [5]).

## Page 18, references

- Reference 5 is cited as "Unsigned manuscript". Reference 16 is "Preprint in the OpenAI mathematics release".

---

## The first page and a half: can a graduate student say what will be done and why?

After the abstract, the introduction and "The plan", such a reader can say:

- the theorem, and why the avoided edge is there;
- that connectivity is the difficulty and degree two is free;
- that the work happens in the dual, and that a Hamiltonian cycle is the complement of an acyclic set with one side in every triangle;
- the order of the sections.

The same reader cannot say:

- how an edge set "chooses" a corner, or why the corner choice is a bijection;
- why the condition falls on the sides opposite the chosen corners;
- what a second corner choice is for;
- what is counted, with what sign and weight, and why a nonzero count yields the object wanted;
- what a height is.

Each of the five gaps is closed later, mostly well (pages 5, 5, 9, 10 to 13, 12). The opening names the objects in the order of the proof but withholds the one-line reason for each, and those reasons exist in the body in good sentences that could be lifted.

## Summary list of floats that interrupt

| Float | Lands | Interrupts |
| --- | --- | --- |
| Figure 1 | top of p. 2 | the "History and sources" paragraph, mid-sentence |
| Figure 2 | top of p. 4 | proof of Lemma 2.5(2) |
| Figure 3 | top of p. 5 | a sentence of the Section 3 opening |
| Figure 4 | top of p. 6 | between the statement and the proof of Lemma 3.5 |
| Figure 5 | top of p. 8 | nothing; it is one page after the proof it illustrates, and the page is 40 percent blank |
| Figure 6 | top of p. 9 | nothing; it is two to three pages late |
| Figure 7, Table 1 | top of p. 10 | the statement of Lemma 4.3 |
| Figure 8 | top of p. 11 | proof of Lemma 4.4 |
| Figure 9 | top of p. 12 | nothing |
| Table 2 | top of p. 14 | Example 4.9 |
| Figure 10 | top of p. 15 | proof of Proposition 5.2 |
| Figure 11 | top of p. 16 | proof of Lemma 6.1 |

Nine of the thirteen floats cut a statement, a proof, an example or a sentence.
