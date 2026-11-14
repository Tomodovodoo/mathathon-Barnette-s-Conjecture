# Exposition review of `paper/main/barnette.pdf`

Reviewer: Claude Fable 5.2, 2026-11-14. Object: the 18-page merged paper and its source `paper/main/barnette.tex` (935 lines). Evidence: my cold read (`COLD-READ.md`), the summary written from memory, the source, the style guide, the two earlier reviews, the merge decisions, the two digestions and the figure set. Line numbers (l.) are lines of `barnette.tex`. Every judgment here is editorial, `HUNCH` in the vocabulary of the brief, unless marked `COMPUTED` with a script.

What I read and what I did not. I read in full: the paper (PDF, then source), `skills/unslop/SKILL.md`, `STYLE-GUIDE.md`, `HOW-THE-REWRITE-WORKED.md`, both earlier `EXPOSITION-REVIEW.md` files, `DECISIONS.md`, `NOTATION.md`, `HOW-IT-WORKS.md`, `00-overview.md`, `paper/figures/README.md`. I read the first two pages of each of the three source papers from the text dumps, and the first page of `proofs/primal/primal.pdf`. I looked at the renders of the unused shared figures 02, 15 and 16 and of two primal figures. I did not read drafts A and B themselves beyond three passages, nor the two earlier `COLD-READ.md` files line by line. For those I rely on their reviews and on `DECISIONS.md`. Where a judgment about a source paper rests on an earlier review and not on my own reading, the table says "per RA" or "per RB".

## Verdict in six lines

1. Sections 3 to 6 are in the right order, and most definitions arrive with a reason. Lemma 3.1 before Definition 3.2, "A sign", "Heights" and the remark after Proposition 3.9 are as good as exposition of this proof gets.
2. The first page and a half is the weakest part. The abstract has five undefined terms. "The plan" compresses the proof into four clauses, omits the disk identity, and never says that a nonzero sum proves existence. Page 2 then addresses readers of the other three papers.
3. Nine of thirteen floats cut a statement, a proof, an example or a sentence. The disk figure comes after the proof it illustrates, the tree-of-faces figure three pages late, and page 8 is 40 percent blank.
4. Four figures have defects visible at print size: Figure 2 (labels hide vertices of G), Figure 10 (labels struck through), Figure 11(c) (inner piece too small), Figure 1 (rows collide, panels out of the plan's order).
5. Three steps still lack their reason at the point of use: why the faces should form a tree (Definition 3.4), what D(r,s) is for, and why a weight F is allowed in Lemma 4.5. Each reason exists elsewhere in the paper or in the digestions.
6. The Remarks section carries the project's status tags into the paper, and the title page has no author.

---

## (a) The 22 rules

| # | Rule | Verdict | Passage |
| --- | --- | --- | --- |
| 1 | Open with the obstacle | pass | l.46 to 50: degree two is free, "Connectivity is the whole problem", the cube. |
| 2 | Route as implications | **fail** | "The plan", l.66 to 69. "Such an acyclic set chooses ... one corner" gives no mechanism. "A second state r ... orients these opposite sides and reduces the condition to 'no cycle'" gives no reason. "Counting such pairs with a sign, ... shows that the total is not zero" never says that a nonzero total, with the bad pairs cancelling, forces a good state. The disk identity, which every later section uses, is absent from the plan. Draft B's four-step list had it ("Acyclicity comes from a single count"). |
| 3 | Theorem contract once | pass | Theorem 1.1 with the edge and its reason (l.59). Theorem 6.2 is the induction statement. |
| 4 | Define an object when the reader wants it | pass in most of the body, **fail** in six places | (i) l.320, "For this graph to be a tree we need the following condition": no reason to want a tree. (ii) l.497, "Besides Q_s a pair gives the set D(r,s)": no purpose. (iii) l.584, "for every function F on states": the reason is on the next page (l.610). (iv) Figure 3(b) and its caption use pair, partner, D(r,s), u(t) four pages early. (v) Table 1 uses sign, F(s) and "the sum" before each exists. (vi) l.84 and l.91 to 95 name the disk identity, heights, spokes, circulations, the sliding argument and the black dual trace on pages 1 and 2. Also the subcaptions of Figure 1(c) to (f). |
| 5 | Names for reusable contracts | pass, one blemish | Disk identity (cited nine times), outdegree lemma (four), duality lemma (four). Blemish: Lemma 3.8 says "In this situation" (l.391), so the most cited statement in the paper cannot be read on its own. |
| 6 | Order by dependency and reading need | pass for the text, **fail** for floats and one paragraph | Figure 5 follows the proof of Lemma 3.8. Figure 6 illustrates Lemma 3.6 (p. 6) and appears on p. 9. Table 1 precedes the sign it tabulates. "Our account differs from [16] in four places" (l.91) is on page 2 and can only be read after Section 4. |
| 7 | Separate definition from assertion | pass, one blemish | Q_s defined (l.261), asserted about in Lemma 4.2. Blemish: "second state" names r in l.474 and l.477 and s from Definition 4.1 on. |
| 8 | Remove stronger targets | pass, one blemish | No algorithm, no determinant. Lemma 2.5 is stated for an arbitrary connected plane graph M, and every use has M = T (Proposition 2.6, Lemma 3.6, Lemma 4.6). RB raised this; it stands. |
| 9 | Invariants of repeated operations | pass | l.592 and l.599 (K_s chosen from s alone), l.626 (paths fixed). |
| 10 | Goal before formula | pass in Section 4, **fail** twice | Lemma 4.5 (see rule 4 iii). Proposition 5.2: "We rewrite (5.1) in terms of U" (l.784) does not say what the rewriting aims at; (5.3) is a planar edge bound with equality for coloured triangulations, and the paper does not say so. |
| 11 | Display decisions, inline routine | pass | The three counts of the disk identity are displayed. l.816 is a long inline chain, acceptable. |
| 12 | Cite standard tools at the invocation | pass | Hall (l.48), Jordan curve theorem (l.187, l.385), Ford and Fulkerson (l.767), Euler with its connectedness hypothesis supplied by Lemma 2.2. |
| 13 | Keep the calculation specific | pass | B = I + ℓ with both halves of bijectivity (l.403 to 416). |
| 14 | Audit notation | **fail**, smaller than in the drafts | `c`: third root (l.229) and number of cycles (l.561). `F`: directed edge set (l.367), function on states (l.584), face of H (l.807), polynomial (l.911). `x`: element of X, bit vector (l.676), corner of Δ (l.823), OpenAI's variable (l.749). `f`: face (l.856), number of faces (l.798), path faces f_i (l.616), an edge (l.928). `w`: vertex in δ(v,w) (l.552), variable w_{t,v} (l.911). `D(r,s)` and the disk 𝖣. `R` (l.137) next to "roots" and R_Z. `q` twice. `NOTATION.md` records the F and c overloads as acceptable because scopes do not overlap. A reader does not know the scopes. |
| 15 | Each conclusion its reason | pass | l.222: "one side per face gives degree two, and acyclicity gives connectivity". |
| 16 | Distinguish the two reversals | pass on content | Lemma 4.3 and Table 1. The table lands inside the statement of the lemma. |
| 17 | One example across representations | pass, one blemish | The 13-vertex example carries Figures 2, 4 to 10 with labels in every panel. Blemish: β has solid wedges in Figure 4(b) and outlined wedges in Figures 5, 7, 8, because the encoding is "solid for the second state". The paper never states the encoding. |
| 18 | Introduce figures by their question | partial | Captions are good and several end by saying what to see ("The proof needs a state that looks like (b)"). In the text ten sentences still have the form "Figure n shows ...". Figure 1 answers no question at the place it appears. |
| 19 | Readable figures | **fail** for four | Figure 2, Figure 10, Figure 11(c), Figure 1. Details in (e). |
| 20 | Abstract short and causal, title literal | partial | Five sentences, causal. Not self-contained. Title in (h). |
| 21 | Keep audits out of the manuscript | **fail** in Section 7 | l.891 "Each remark says whether it is proved here, computed, or open." Headings "(proved; computed)", "(proved; literature)", "(proved)", "(open)". l.923 "we have not checked it". l.908 "(computed)". l.927 "(literature)". |
| 22 | Compare rendered passages | n/a here | `EDITS.md` gives old and new text; `code/verify_edits.py` checks the old strings. |

Count: 12 pass (rules 5, 7, 8, 17 with a blemish), 5 mixed or partial (rules 4, 6, 10, 18, 20), 4 fail (rules 2, 14, 19, 21), 1 not applicable. None of the fails changes the mathematics.

### Problems raised on the drafts: fixed or not

Checked against the merged PDF. "RA" is the review of draft A, "RB" of draft B.

| Problem | Source | Status in the merged paper |
| --- | --- | --- |
| Spokes with no purpose; P not built from Q_s | RA | fixed. No spokes; l.259 to 263 says which sides P uses and which it excludes. |
| Lemma 5 copied from OpenAI, opaque t0 sentence | RA | fixed. l.786 to 787 counts t0 explicitly. |
| Internal notes in the bibliography | RA | fixed. |
| Figures never referenced | RA | fixed. All eleven are cited. |
| Figure 2: labels 6, 11, 12 collide with vertices of G | RA, RB | **not fixed**. The labels now have a white backing, which hides the vertices instead of colliding with them. |
| Gluing figure, panel (c) unreadable | RA, RB | **not fixed**. |
| Notation overloads | RA, RB | mostly fixed; residue under rule 14. |
| Objects before definition in the Sources paragraph | RB | half fixed. The symbols are gone; the names remain (l.84, l.91 to 95). |
| Figure 3 caption uses pair, partner, D before the definitions | RB | **not fixed**. Panel (b) is still in Section 3 with a pointer "(Section 4)". |
| Selection figure lands between Lemma 4.2 and its proof | RB | half fixed. It no longer splits a lemma; it is still three pages after Lemma 3.6. |
| Table 1 never cited, floats into a definition | RB | half fixed. It is cited; it now floats into the statement of Lemma 4.3. |
| A float splits Example 4.9 | RB | **not fixed**. Table 2 does it now. |
| No figure for heights | RB | fixed (Figure 9), with a caption that calls both panels "reversed". |
| Labels 1, 8, 9 on wedges in the cancellation figure | RB | **not fixed**. Also in Figures 4, 7, 9. |
| Process talk | RA, RB | fixed in Sections 1 to 6, reintroduced in Section 7. |
| About 60 semicolons | RB | **not fixed**. 99 now (`COMPUTED`, `code/style_counts.py`). |
| "Figure n shows" as a closing sentence | RB | partly; about ten remain. |
| Garbled sentence about the m-th power; no reason for a power | RB | fixed (l.666 to 670). |
| Winding numbers used without reference | RB | fixed by removal. |
| Euler's formula without connectedness | RB | fixed (Lemma 2.2, l.383 to 388). |
| "Heights remove the exponential sum" overstates | RB | **not fixed**. l.94 still says the heights remove "the spokes, the sliding argument ... and the exponential sum". Lemma 4.7 removes the exponential; the heights remove the spokes and the slide. |
| The tree of faces is also in the formal proof released with [16] | RB (from another agent's note) | not addressed. l.95 presents it as a difference from [16]. I did not check the Lean source. |
| Where the unsigned manuscript [5] can be found | RB | **not fixed**. |
| Kelmans credited without a citation | RA, RB | handled as well as the project can: "goes back to Kelmans, as explained by" two sources that are cited. |

---

## (b) Step by step: is the merged paper the clearest text for each step?

O = OpenAI, L = Li, C = the constructive manuscript, A and B = the two drafts, HIW = `digestions/route-map/HOW-IT-WORKS.md`, OV = `digestions/steps/00-overview.md`, M = the merged paper.

| Step | Clearest text | Is M the clearest? | If not, what the better text does |
| --- | --- | --- | --- |
| Obstacle | M l.46 to 50 (from A) | yes | |
| Separate reasons for degree and connectivity | A, second paragraph: "We will enforce connectivity in the dual graph. There, omitted edges become a forest. Planarity turns acyclicity of those edges into connectivity of their complement. The local degree condition and the global connectivity condition then have separate certificates." | **no** in the introduction | M has the idea at l.222, after Proposition 2.6, in a very good sentence. The introduction lost A's paragraph. My replacement plan restores it in two sentences. |
| Plan of the proof | OV, "The argument in ten sentences", and HIW section 2, "Read the answer backwards" | **no** | OV gives one sentence per step, each with its consequence. HIW starts from a Hamiltonian cycle and asks what it looks like in T, which is what Lemma 3.1 does, and says so up front. B's four-step list is also better than M's paragraph: it names the disk identity. |
| T is a simple coloured triangulation | M Lemma 2.1 (from B) | yes | One dense sentence (l.118). |
| Target | M Definition 2.4, Proposition 2.6 (from B) | yes | "One side per triangle, no cycle" is the shortest statement of the target in any of the texts. |
| Where states come from | M Lemma 3.1 (from B); HIW section 2 says the same in prose | yes | |
| Why the faces should form a tree; what "good" selects | C section 1: "We seek a tree matching ... The matching fixes the degrees of the retained graph; the tree condition ensures that it is connected." HIW section 2: "A state fixes the tail of the selected edge in each black face, and that determines the edge only when H − s is a tree. The proof finds a special kind of cycle." | **no** | M says "For this graph to be a tree we need the following condition" and gives the reason only in Section 7 (l.896). The warning that goodness is sufficient and not necessary is the missing sentence. This was the first of my three open questions after the cold read. |
| State to selection | M Lemma 3.6 (from B) | yes against O and A (one graph fewer). Needs Figure 6(a) beside it. | |
| Disk identity | M Lemma 3.8 and Figure 5 | yes | The statement should carry its own hypotheses. The figure should precede the proof. |
| Acyclicity of the selection | M Proposition 3.9 and the sentence after it | yes | |
| Why two states | HIW section 3: "The partner r is a certificate. It orients Q_s, and the orientation does the counting. Without it the statement is false. On the hexagonal prism all three states have Q_s a forest and only two are tree matchings." | **no**, narrowly | M's three sentences (l.475 to 477) are correct and abstract. HIW has a counterexample that makes the need concrete. M already uses the hexagonal prism in Section 7. |
| Why count at all | HIW section 4: "Nobody knows how to point at a pair with Q_s a forest. ... The proof counts instead. Attach a sign to every pair, add up the signs of all pairs with a weight that depends only on s, and compute the sum twice." | **no** | M never says that the same sum is computed twice, or that the argument is an existence proof by a nonzero count. Each half is motivated locally (l.550, l.610). The frame is missing. |
| Two reversals and the sign | M Lemma 4.3, "A sign", Lemma 4.4 | yes | Product of local signs is simpler than O's phase. Table 1 is in the wrong place. |
| Cancellation | M Lemma 4.5 and l.599; O Lemma 5.2 is as compact | level | |
| Weights | L's vertical rays are the most concrete picture (per RB). The primal note's flow picture (`proofs/primal/figures/04-flow.png`, "weight(C) = number of white vertices inside") is the most direct statement of what the weight measures. | **no** on intuition, yes on rigour | M defines the height by turned corners and proves Lemma 4.6 by a four-case check with no picture. The statement that carries the intuition, "the change of height is the number of times the path leaves C minus the number of times it enters", is inside the proof (l.656). Put it before the lemma. |
| Nonvanishing | M l.666 to 670 and Lemma 4.7 | yes for the audience; O's product over cycles is more memorable and M has it in Section 7 (l.915) | |
| The two groupings on the example | nowhere | **no text has it** | Table 2 has the data. A picture of the eight pairs in two rows with the cancelling couple linked would show both groupings at once. TikZ supplied in `EDITS.md`, edit 14. |
| First pair | M Section 5 opening (the 2-regular subgraph of ℬ) | yes for the proof | For the meaning of the hypothesis, HIW section 6 is clearer than M's l.908: "A separating triangle has exactly one side whose faces along the triangle are black. ... A pair exists if and only if t0 lies on the black side of every separating triangle." |
| Gluing | M Theorem 6.2 for the proof; L Appendix C for the picture (two Hamiltonian cycles across a 3-edge cut, per RB) | yes | M has L's reading in one sentence (l.871). |
| What the hypotheses do | M Section 7 | only M has it | One 19-line paragraph; break it. |
| Example | M | yes | |

Net over 21 rows: M is the clearest text at 13, level at 1, and not the clearest at 7. Four of the seven (plan, tree of faces, two states, why count) are places where a plain-language sentence from the digestions should be lifted into the paper. The other three are the introduction's lost paragraph from draft A, the intuition for the weights (Li, the primal note), and the missing regrouping picture.

---

## (c) Flow, section by section

**Abstract and Section 1.** Question on arrival: what is proved, why is it hard, how does the proof go? The first two are answered well. The third is answered in outline only. Arrives too early: the list of credited objects (l.84), the comparison with the two other expositions (l.88 to 89), the four departures from [16] (l.91 to 95), and four of the six panels of Figure 1. Arrives too late: the definition of the dual (Section 2) and of a separating triangle (never formally).

**Section 2.** Question on arrival: what exactly is the target in T, and why does "no cycle" give "one cycle"? Answered by Definition 2.4 and Proposition 2.6. The reader passes through Lemma 2.1's proof and Lemma 2.2 first, about a page. That is acceptable if the plan has already promised the target. Figure 2 arrives inside the proof of Lemma 2.5. Wanted and missing: a picture of the target at the end of the section. The text points five pages ahead to Figure 6(b).

**Section 3.** Question on arrival: how do I find an acyclic selection through e0? The section answers with a change of unknown (states), a sufficient condition (good), and a proof that the condition suffices. The order is right. Three local faults: the reason for wanting a tree is missing (l.320); Lemma 3.6 is proved three pages before its picture; the disk identity is stated after two paragraphs of set-up with its figure after the proof. Arrives too early: Figure 3(b).

**Section 4.** Question on arrival: how do I find a good state? The answer is a four-part argument, and the section never lays it out. The reader meets a definition, a lemma, an edge set D "besides", two reversals, a sign, a cancellation "for every function F", heights, and a power. Each has a local motivation and most are good. What is missing is four lines at the head of the section saying that a signed, weighted sum over all pairs will be computed twice. Arrives too early: Table 1. Arrives too late: the reason for F.

**Section 5.** Question on arrival: where does the first pair come from? Answered directly and well in the first paragraph. Figure 10 belongs with that paragraph and lands inside the proof. "Separating triangle" is used in the proposition without a definition. The proof of the density bound is a correct computation without a stated aim.

**Section 6.** Question on arrival: what if there is a separating triangle? Answered. The closing paragraph (l.870) says why the theorem needed the prescribed edge, which closes the loop opened on page 1.

**Section 7.** Question on arrival: what did I not get told? Good content. The first remark answers a question that arises at Definition 3.4, forty lines of which belong there in one sentence.

### Proposed reordering

No section moves. Seven local moves, all in `EDITS.md`:

1. "Our account differs from [16]" leaves page 2 and becomes the first remark of Section 7, with its two overstatements corrected.
2. "History and sources" keeps the history and the credits and loses the technical comparison of the two expositions, which Remark 4.10 already makes.
3. Figure 3(b) moves to Definition 4.1.
4. Figure 5 moves to the sentence that introduces B, W, I, ℓ, h, before Lemma 3.8.
5. Figure 6 moves to Lemma 3.6.
6. Table 1 moves to after Lemma 4.4, where its "sign" column has a meaning.
7. Figure 10 moves to the first paragraph of Section 5, before Proposition 5.2.

---

## (d) The opening: replacement text

### Abstract (six sentences, no undefined term)

> We give a self-contained exposition of OpenAI's 2026 proof of Barnette's conjecture, in the form that every cubic, bipartite, 3-connected planar graph has a Hamiltonian cycle avoiding any given edge. In a cubic graph the complement of a perfect matching has degree two at every vertex, so the task is to find a perfect matching whose complement is connected. In the planar dual, a triangulation whose triangles are coloured black and white, a perfect matching is a set of edges containing one side of every triangle, and its complement is connected when the set contains no cycle. We reduce the search for such a set to a choice of one corner in each black triangle. A suitable choice exists because of a signed count over pairs of choices, in which the unsuitable ones cancel and a second grouping of the same sum shows that it is not zero. The avoided edge is what lets an induction cut the triangulation along triangles that are not faces.

Terms used: cubic, bipartite, 3-connected, planar, Hamiltonian cycle, perfect matching, planar dual, triangulation. All are standard for the stated reader. "Black triangle" is defined inside the sentence that first uses it.

### The first page

Keep the first paragraph (l.46 to 50), Theorem 1.1, and the paragraph after it (l.57 to 60) as they are. Replace "The plan" (l.62 to 70) by the text below. It is longer, about 420 words against 190. It gives each object the one-line reason that the body gives later, in the body's own words where possible. Earlier the user asked for the plan as one paragraph (`DECISIONS.md`, section 2). The five steps below are complete sentences and can be run together without changing a word; I think the numbered form reads better and say so as a recommendation, not a requirement.

> **The plan.** The proof takes place in the planar dual T of G. It has a vertex in each face of G and an edge across each edge of G. Each vertex of G lies in a face of T, which is a triangle because G is cubic, and we colour that triangle black or white by the class of the vertex (Figure 1(b)). A perfect matching of G is then a set P of edges of T that contains exactly one side of every triangle. One side per triangle gives the rest of G degree two. The rest of G is connected exactly when P contains no cycle, because a cycle of P would separate the triangles inside it from those outside (Section 2). So we look for a set of edges of T with one side in every triangle and no cycle, and we want it to contain the edge e0 that crosses e.
>
> 1. *Corner choices.* Let t0 be a black triangle at e0. A set P as above is a forest, and once e0 is removed each of its trees contains one corner of t0. Direct the trees towards these corners. Every other black triangle t has one side in P, and that side leaves a corner s(t) of t. Every vertex off t0 is s(t) for exactly one t. A choice of corners with this property is called a *state*, and states are what we search for (Section 3).
> 2. *From a state back to P.* A set built from a state s uses a side at the chosen corner in each black triangle, so it avoids the opposite side. Call s *good* if the opposite sides form a forest with one corner of t0 in each tree. Then the opposite sides and the two sides of t0 other than e0 form a spanning tree of T, the other edges join the triangles into a tree, and that tree leaves only one way to take a side in every triangle (Figure 1(d) to (f)). The set obtained has no cycle because of one count, the *disk identity*. It says that a cycle made of sides leaving chosen corners encloses exactly one more white triangle than black.
> 3. *Two states.* Take another state r that differs from s in every black triangle. Then r(t) is an end of the side opposite s(t). Directing that side out of r(t) gives every vertex off t0 exactly one outgoing side, and then a tree of opposite sides contains exactly one corner of t0. So s is good as soon as its opposite sides contain no cycle (Section 4).
> 4. *A count.* We cannot point to a pair (r, s) of this kind. We count instead. Every pair gets a sign and a weight that depends on s alone. If the opposite sides of s contain a cycle, reversing it gives another pair with the same s and the opposite sign, so in the sum of sign times weight over all pairs only good states remain. The same sum can be grouped in a second way. The arrows from r(t) to s(t) form cycles (Figure 1(c)), and reversing one of them exchanges r and s along it. With weights that count the white triangles inside these cycles, the second grouping shows that the sum is not zero. So a good state exists as soon as one pair exists. The disk identity is used again here. It makes both reversals change the sign, and it puts a white triangle inside every cycle.
> 5. *The first pair and the induction.* A flow argument gives a pair when every 3-cycle of T bounds a triangle (Section 5). Otherwise some 3-cycle has vertices on both sides; it is called a *separating triangle*. Cutting T along it gives two smaller triangulations. The solution of the first decides which side of the cut the second must use, and this is why Theorem 1.1 prescribes an edge (Section 6).

Then "History and sources", shortened (edits 3 and 4), and "The example".

Checks on the replacement. Step 1 is Lemma 3.1. Step 2 is l.259 to 263, Definition 3.4, Lemmas 3.5 and 3.6, the uniqueness remark of l.896, and Proposition 3.9. Step 3 is Lemma 4.2. Step 4 is Lemmas 4.5 and 4.6 and Proposition 4.8. Step 5 is Proposition 5.2 and Theorem 6.2. I added no claim that the paper does not prove. "Every 3-cycle of T bounds a triangle" is the hypothesis of Proposition 5.2 in the form its proof uses (l.799 to 803).

---

## (e) Figures

Text width is 451 pt (159 mm). The shared figures are included at their natural size, so their labels are 8 pt (`\footnotesize`) with 6 pt subscripts against 10 pt body text (`COMPUTED` from the PDFs with PyMuPDF). Figure 2 is scaled by 1.15. The README of the figure set says not to rescale.

| Fig. | Width / tw | Labels | Lines, colour, greyscale | Clutter | Placement against first citation | Caption | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 overview (`01-cube`) | 0.78; six disks of 37 mm | vertex labels 8 pt, legible; subcaption text collides with the label "2" of the second row | good; the grey collar is not self-explanatory | low per panel | cited l.50 (p. 1), printed p. 2; fine | 10 lines; a second plan with symbols D, S_s | **regenerate**: full text width, 4 mm between rows, the cube drawn in grey over the octahedron in (b), panels in the order of the plan (pair and D last), word subcaptions ("a state and its opposite sides") in place of "Q_s, opposite the wedges". Shorten the caption (edit 30). |
| 2 example (`03-dual`) | 0.55 | labels 6, 11, 12 hide white vertices of G; "9" far from its vertex | G in thin grey S-curves; legible in grey | high: T and G drawn with equal presence | cited l.98 (p. 2), printed p. 4 inside a proof | good | **regenerate**: label offsets so that no label covers a vertex; G at 0.3 pt in a lighter grey or as a second panel "T with G"; width 0.62. Move the float (edit 21). |
| 3 local triangle (inline TikZ) | two triangles of 29 mm | `\footnotesize`; smaller than they need to be | good | none | (a) right; (b) four pages early | (b) uses undefined terms | **split and enlarge** (edit 9). |
| 4 Q_α, Q_β (`09-Q`) | 0.94 | labels 1, 3, 7, 9, 10 touch wedges or edges | dashed vermilion against grey edges survives greyscale; solid blue wedges read as dark grey | medium | cited p. 5, printed p. 6 between Lemma 3.5 and its proof | good; says what to see | move the float (edit 22). Nudge five labels on regeneration. |
| 5 disk identity (`08-disk`) | 0.78 | good; side list 8 pt | tinted disk, ringed vertices, marked arrows; good | low | printed one page **after** the proof | good | **move before Lemma 3.8** (edit 6). The best figure; leave the drawing alone. |
| 6 selection (`13-selected`) | 0.94 | (a): labels 3, 6, 7, 11, 12 crossed by the green tree or bold edges | bold black, green dash-dot, purple curve; distinct in grey by weight and dash | medium | cited l.225 (p. 4) and l.456 (p. 8), printed p. 9 | good | **move to Lemma 3.6** (edit 7). Consider showing panel (b) alone at the end of Section 2. |
| 7 pair and D (`07-pair-D`) | 0.94 | twenty wedges; labels on wedges | arrowheads on the 7-cycle are hard to find | high; panel (a) is panel (b) without arrows | printed inside the statement of Lemma 4.3 | fine | **regenerate as one panel** at 0.6 tw with larger arrowheads; or keep both and put the encoding legend ("outlined: first state; solid: second state") in (a). Move the float (edit 23). |
| Table 1 | | | | | inside the statement of Lemma 4.3; before the sign | fine | move after Lemma 4.4; reword one cell (edit 10). |
| 8 cancellation (`10-cancellation`) | 0.94 | labels 1, 8, 9 on wedges | tinted triangle helps | high; the two panels differ in three wedges | printed inside the proof of Lemma 4.4 | good | **regenerate as a close-up** of the three faces 178, 129, 8 9 10 and the white face 1 8 9, before and after, at twice the scale. Move the float (edit 24). |
| 9 heights (`17-heights`) | 0.94 | good; circled signs clear | green dash-dot path; fine in grey | medium; the hairpin of the path in face {0,1,6} looks like a second crossing | printed before the definition, same page | says "reversed" of both panels | fix the caption (edit 12); on regeneration shorten the hairpin. |
| Table 2 | | | | | splits Example 4.9 | good | move the float after the example (edit 25). |
| 10 flow (`06-flow`) | 0.70 | six triangle labels are struck through by the edges to the sink; "12" overprinted | double vermilion against single blue reads in grey | medium | cited l.763, printed inside the proof of Proposition 5.2 | good; the equality case S = {2} is a nice touch | **regenerate**: triangle labels to the left of their squares or the sink 15 mm further right; capacities written on one edge of each kind. Move the float (edit 26). |
| 11 gluing (`14-gluing`) | 1.00 | (c): inner vertices unlabelled, inner octahedron about 6 mm | fine | (c) unreadable | printed inside the proof of Lemma 6.1 | good | **regenerate (c)** with the inner triangle 3, 4, 5 enlarged (a layout for the 9-vertex graph with a large central face), labels 6, 7, 8. Move the float (edit 27). |

### Merge, split, enlarge, move

- Split: Figure 3 into (a) at Definition 3.2 and (b) at Definition 4.1.
- Merge: Figure 7(a) into 7(b).
- Enlarge: Figure 1 to the text width, Figure 2 to 0.62, Figure 3 by a third.
- Zoom: Figure 8.
- Move: Figures 2, 4, 5, 6, 7, 8, 10, 11 and both tables.

### The missing picture that would help most

The two groupings of the same eight pairs. Section 4 turns on computing one sum in two ways, and no figure or table shows the two ways together. `EDITS.md` edit 14 supplies TikZ for it: two rows of four boxes (the two classes by undirected D, each row summing to 2·L1·L2), with the two pairs that share the second state α joined by a bracket marked "same s, opposite signs". It compiles in my trial build.

Second: a local picture for Lemma 4.6. One black triangle with its side g on C, and the two ways a path can cross g (turning around r(t) on its left, or around s(t) on its right). It replaces the four-case check for most readers. Not drawn here.

Third: the target on the example at the end of Section 2 (panel (b) of Figure 6).

The inside of a cycle as a disk and the flow network both exist (Figures 5 and 10). They need to be in the right place and, for the flow network, legible.

### Does the overview figure on page 2 work at its size?

No. On first contact a reader can use panels (a) and (b). Panels (c) to (f) have symbol subcaptions that are defined three to eight pages later, the outlined wedges of r are about 1 mm across, and the rows touch. The order of the panels (pair, opposite sides, tree, selection) is not the order of the plan (opposite sides, tree, selection, pair). With the replacement plan of (d), which cites the panels in the plan's order, a full-width regenerated figure with word subcaptions would work. The unused `16-at-a-glance` strip is worse for this purpose: six 25 mm disks of the 13-vertex example and a caption that is a third copy of the plan.

---

## (f) Layout

**Floats.** All floats are `[tb]`, and LaTeX puts each at the top of the first page with room, which is usually the page after the citation and usually mid-proof. The table at the end of `COLD-READ.md` lists where each lands. Nine of thirteen interrupt something. The fix has two parts: place each float in the source after a complete unit (never between a statement and its proof), and give the large ones `[!ht]` or `[p]` only where a top float would split a statement. I tested the placements of edits 6, 7 and 21 to 27 in a trial build (`trial/`); the result is reported in `REPORT.md`.

**Blank space.** Page 8 is 40 percent blank because `\FloatBarrier` before Section 4 forces Figure 6 out and the section cannot start above it. Moving Figure 6 to Lemma 3.6 removes the cause.

**Statements broken across pages.** Lemma 4.3 (p. 9 to 10) and the pair Lemma 3.5 and its proof (p. 5 to 6).

**Headings with no text.** "The recovered selection has no cycle" (l.426) and "Cancellation" (l.579) are followed at once by a statement. Each needs one sentence (edits 11 and 17).

**Tables.** Example 3.3 names faces by run-together digits ("81112"). Use centred dots, 8·11·12 (edit 16). Table 1 and Table 2 are well set.

**Display density.** Fine everywhere. Section 5 has two long inline chains (l.810, l.816) that would be easier as displays, low priority.

**Paragraph length.** l.80 to 89 (20 printed lines) and l.903 to 908 (19 lines) are walls. Break the second at each italic run-in.

**Widows.** None seen at 130 dpi apart from the broken lemma statements above.

---

## (g) Unslop audit

The paper is free of the loud patterns: no puffery, no AI vocabulary, no em dashes, no bold in running text, headings in sentence case, no chatbot phrases. What survives, by pattern number of the skill:

| Pattern | Passage | Replacement |
| --- | --- | --- |
| 11 synonym cycling | "avoiding any given edge" (abstract), "A prescribed edge" (abstract), "the prescribed side" (Fig. 1), "an avoided edge" (l.930). Also triangle / face / black triangle / black face; corner choice / state; outer triangle / outer face. | In G: "the avoided edge e". In T: "the prescribed side e0". Faces of T are "faces" from Section 2 on; say once that the plan's "triangles" are these faces. |
| 11 | "second state" for r (l.474, l.477) and for s (l.480 on) | Heading "Why two states"; "Another state r that differs from s" (edit 8). |
| 11 | P_s is "produced" (l.356), "recovered" (l.426), "read off" (l.92), "selects" (l.95) | "the selection P_s of Lemma 3.6" throughout; heading "P_s has no cycle". |
| 13 parenthetical asides | l.362 "(we will apply this to both states of a pair, which is why it is called r)" | delete (edit 18). |
| 13 | l.621 "(Combinatorially: if a′ is the far end ...)" | A sentence of its own: "In combinatorial terms, let a′ be ...". |
| 13 | l.900 "(For the two other sides of t0 there are two such cycles, and both arise.)" | Remove the parentheses. |
| 14 colon as connector | 23 in prose (`COMPUTED`, `code/style_counts.py`). Worst: l.84 "The objects of the proof are theirs: pairs of states, ..."; l.477 "turns it into the first: it gives"; l.596 "group the pairs by s: the states with"; l.715 "The minimum cannot be dropped: a class with"; l.870 "is what makes the gluing work: P_2 must"; l.908 "it is not necessary: by" | Full stop and a new sentence in each. l.452 "In words:" can stay. |
| 23 filler | l.364 "One principle about them is used four times." | delete. |
| 23 | l.391 "In this situation" | state the hypotheses (edit 5). |
| 23 | l.361 "Throughout the paper, the cycles we need are made of sides leaving corners chosen by a state." | "Every cycle we need is made of sides leaving corners chosen by a state." |
| 27 says how it feels | l.576 "can rearrange the cycles of D completely, so a sign defined by counting the cycles of D would not be controlled" | "can merge or split cycles of D, so the number of cycles of D does not change in a predictable way". |
| 27 | l.613 "The disk identity offers a way, because every such cycle encloses a white face." | "Every such cycle encloses a white face, by the disk identity, and F will count enclosed white faces." |
| 28 dense sentences | l.66, l.68, l.69 (the plan) | replaced in (d). |
| 28 | l.118 "One vertex has three edges leaving it, and two vertices have at least four" | "If |U| = 1 then three edges leave U, and if |U| = 2 at least four do" (edit 19). |
| 28 | l.250 (48 words), l.351 (46), l.407 (50), l.907 (108) | split each at its semicolon or its second "and". |
| 28 | l.388 "so no vertex is pinched between the two sides" | "We also use that every face at a vertex strictly inside Z lies inside Z." (edit 20). |
| 28 | 99 semicolons, many "X; so Y" | make about half of them full stops; start with proofs of Lemmas 3.6, 3.8 and Proposition 5.2. |
| 29 passive | l.907 "It is used once, to make T simple" | "The proof uses it once, to make T simple". |
| 30 adverbs | "exactly" 48 times. It carries meaning in "exactly one". It carries none in l.332 "That happens exactly when" twice in two lines, l.64, l.896. | keep "exactly one"; elsewhere "if and only if" once, then "when". |
| 20, 21 communication artifacts | l.891 "Each remark says whether it is proved here, computed, or open."; the bracketed tags in four headings; l.923 "we have not checked it"; "(computed)", "(literature)" | delete the sentence and the tags (edit 28). l.923: "The unsigned manuscript [5] states an algorithm that ...; we do not use it." |
| 5 vague attribution | l.89 "An unsigned manuscript [5]" | say where the reader can obtain it, or say that it circulated privately. |
| "Figure n shows" | l.156, l.225, l.417, l.456, l.626, l.873 and four captions | say what to look at. l.873: "In Figure 11 the two pieces agree on the side {3,5} of the separating triangle." |

Voice. The prose is plain and mostly active. It has rhythm in the motivating paragraphs ("Connectivity is the whole problem." "Here is why a power.") and loses it in the proofs, where nearly every sentence has two clauses joined by a semicolon or "so". The skill asks for opinions and some unevenness. The paper has a few and they are its best lines: "In words: a cycle of chosen sides encloses one more white face than black, but a selection running along it would force three more."

---

## (h) Title and framing

**Title.** "Barnette's conjecture in the dual triangulation" is literal about the setting and silent about what the paper is. Two objections. It does not say that the paper is an exposition, or that the conjecture has been proved. And "in the dual triangulation" does not distinguish this account from OpenAI's, which is also set in the dual triangulation; it distinguishes it from Li's. What is characteristic here is the route by corner choices and the derivation of each object from the target. Options, in my order of preference:

1. "The proof of Barnette's conjecture: an exposition"
2. "Hamiltonian cycles from corner choices: an exposition of the proof of Barnette's conjecture"
3. the present title with the subtitle "an exposition of OpenAI's proof"

The running head "Barnette's conjecture" is fine.

**Author.** There is none. The paper says "we", "our account", "we have not checked it". A reader needs to know who vouches for the "four places, each proved in full below". The author line is the user's decision; the paper should not go out without one or without a statement of how it was produced.

**Honesty as an exposition.** Good. The abstract says "We explain OpenAI's proof". Theorem 1.1 is attributed with pinpoints. "The objects of the proof are theirs" (l.84) is the right sentence. Tutte, Hine and Kálmán, Stein, and Alt, Payne, Schmidt and Wood are credited at the right objects. Li's half-ray counts are identified with the heights (l.88, l.663).

**Three corrections to the credits.**

1. l.94 says the heights remove "the spokes, the sliding argument ... and the exponential sum". The finite difference of Lemma 4.7 removes the exponential sum. Say "this removes the spokes and the sliding argument ...; a finite difference (Lemma 4.7) replaces the exponential sum".
2. l.95 lists the tree of faces obtained by duality as a difference from [16]. Another agent's note (`research/2026-11-14_opus_lean-formalisation/DIFFERENCES.md`, item 19, cited by RB) says the formal proof released with [16] recovers the cycle the same way. I did not check that. If it is right, the sentence should claim the presentation only.
3. l.89 and l.908 rest on an unsigned manuscript that the reader cannot locate from the bibliography entry. The criterion quoted at l.908 is not used in the proof. Say so, and say where the manuscript is.

**Process talk.** Sections 1 to 6 are clean. "The numbers quoted for the example come from exhaustive enumeration" (l.102) is a fair sentence. Section 7 is where the project shows: the status tags and "we have not checked it".

**References I could not verify.** I confirmed from the text dumps in `papers/text/` that Li's note carries arXiv:2610.30490v1 and the date 21 October 2026, that the constructive manuscript is unsigned and dated 18 October 2026, and that OpenAI's paper is dated 24 September 2026 with the cited theorem and corollary numbers in its introduction. I did not check the URL in reference 16 or any of the older references.
