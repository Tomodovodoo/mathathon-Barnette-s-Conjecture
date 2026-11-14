# Cold read of draft B

Read from the PDF only (`paper/draft-B/barnette.pdf`, 16 pages, rendered to PNG at 130 dpi, in `pages/`), before opening any other project file except `research/BRIEF.md`. Entries are in reading order. Each one says where I stopped, what I expected, what I got, and the question I had.

Marks: **T** = term or symbol used before it is defined; **P** = purpose unclear when introduced; **V** = step I could not verify within a minute; **F** = figure problem; **S** = pacing; **ok** = a place where the text did what I wanted (kept so that the merge does not lose it).

## Page 1

1. **Abstract, sentence 4** ("such a set can be built from a choice of one corner in each black triangle whose opposite sides form a suitably rooted forest"). **T**. "Suitably rooted" tells me nothing. I expected either the condition in plain words (one corner of the outer triangle in each tree) or no mention. Question: rooted where?
2. **Abstract, sentence 5** ("fixing the second choice cancels every pair whose opposite sides contain a cycle, while grouping by the cycles along which the two choices differ shows that the total is not zero"). Too compressed for an abstract. I could not parse "fixing the second choice cancels" on first reading. Whose opposite sides, the first choice's or the second's?
3. **Abstract, sentence 6** ("a cycle of edges leaving chosen corners encloses exactly one more white triangle than black"). **T**. "Edges leaving chosen corners" is not yet a notion. I guessed: edges of the triangle that start at the chosen corner. That guess turned out right, but only on page 6.
4. **Intro, paragraph 1.** **ok**. History in six sentences, then the theorem. No complaint. "For 57 years" checks (1969 to 2026).
5. **"Degree two is easy; connectivity is the problem."** **ok**. This is the paragraph I wanted first. It says what is hard before any machinery. The last sentence ("Every construction in this paper is there to enforce connectivity") made me expect each later section to say how it enforces connectivity. Sections 4 and 5 do not come back to this.
6. **The route, step 2.** **T**. "Fix a black triangle" comes before the colouring is introduced in the body (only the abstract mentions colours). "Edges leaving chosen corners" again.
7. **The route, step 3** ("A second corner choice, disjoint from the first, orients the opposite sides and turns the condition of step 2 into 'no cycle'"). I expected a reason for bringing in a second choice. The sentence gives one, and it is the right one. Good, but "disjoint" for two corner choices is undefined (I read it as: different corner in every triangle).
8. **The route, step 4** (on page 2: "One pair is needed to start"). I had understood step 3 as already proving the total is nonzero. So what is started? Question: does the nonvanishing in step 3 assume that a pair exists? (Yes, it turns out. The route should say "if there is at least one pair" in step 3.)

## Page 2

9. **Figure 1.** **F**. The edges of G are drawn as wavy curves, which looks hand-made next to the straight-line figures later. I could not check by eye that (a) has two cycles; a second colour for the second cycle would let me. Placement is right (top of the page after its first mention).
10. **"One picture" paragraph, last sentence** ("the four counts of the proof (the disk identity, the acyclicity of the selected edges, the density bound for the first pair and the colour of a cap)"). **T** four times. None of "disk identity", "density bound", "cap" has been explained. I skipped the sentence. It reads as written for someone who knows the proof.
11. **"Sources" paragraph.** **T**: `Q_s`, `D(r,s)`, `ε = (-1)^{(n+J)/2}`, `ω^m`, `Y_s`, "sliding of edges onto spokes", "black dual trace", "circulation lemma". A whole paragraph of forward references on page 2. I expected this paragraph at the end of the introduction or the end of the paper, written in words. Also unclear: "found in unpublished notes written during a collaborative reading" versus "Two smaller changes are ours". Who are "we" if not the authors of the notes?

## Page 3

12. **"The example."** **ok** in intent. "12 corner choices and 8 pairs, few enough to list" made me expect a table listing them. No such table appears anywhere in the paper.
13. **Section title "One picture"** repeats the run-in heading of the introduction paragraph on page 2. I expected a title naming the content ("The dual triangulation and the target").
14. **Lemma 2.1, proof.** Verified. The first paragraph (no 2-edge cut) took me two readings: "two vertices have at least four" needs simplicity, which is in the hypothesis. The step from "closed walk of length three" to "triangle" is fine.
15. **"From now on T is a coloured triangulation."** **ok**. A clean reset of the standing object. Equation (2.2) is numbered (2.2) with no (2.1) visible because equations share the theorem counter; I looked for (2.1).
16. **"Figure 2 shows the example."** One orphan sentence. Fine.
17. **Definition 2.3 and the line after Lemma-2.4 announcement** ("We use the following lemma twice, once for M = T in Section 3 and once below"). I stopped. Below (Proposition 2.5) it is also used with M = T. So what are the two uses and why name M at all? I expected "once in Proposition 2.5 and once in Lemma 3.3, both with M = T". Question: is the generality (arbitrary connected simple plane M) ever used? It seems not.
18. **Lemma 2.4, proof of (2).** Verified, about two minutes. The parity argument around a vertex is short and complete. I did wonder whether M* is allowed loops and multiple edges (yes for general M; harmless).

## Page 4

19. **Figure 2.** **F**. Labels 6, 11 and 12 sit on top of dots of G ("11" reads as "1d"); 3 and 8 touch edges. The picture carries both T and G, which is right here and only here. The roots 0, 4, 5 are drawn as larger hollow circles; the caption does not say so. The caption does not say which root is c or which side is e0; I found out on page 8 (Example 3.8).
20. **Proposition 2.5(2), proof.** **ok**. The even-cut argument is short and I verified it at once.
21. **Proposition 2.5(2), purpose.** **P**. When I read it I did not know why I need "an edge lies in P exactly when its ends lie in the same component". It is used in Lemma 3.1 (five lines later, good) and in Theorem 6.2. One clause would settle it: "we use (2) in Lemma 3.1 and in the gluing".
22. **Paragraph after Proposition 2.5** ("A selection P containing an edge e0 of T gives a Hamiltonian cycle"). The word "acyclic" is missing. Then "Figure 7 shows one in the example": Figure 7 is five pages ahead, in the middle of Section 4.
23. **Section 3, first paragraph.** "Exchanging the two colours if necessary, t0 is black; selections do not depend on the colours." **ok**, exactly the remark I needed.

## Page 5

24. **Figure 3.** **F**, **S**. The figure arrives before states are defined. Its caption uses "state", `Q_s`, "pair", "partner", `D(r,s)`, `u(t)`, "spoke", and panel (c) describes a "tinted region" that "contains no point p of a white face such as y". At this point of the paper panels (b) and (c) are noise: (b) belongs to Definition 4.1 on page 8 and (c) to Lemma 4.6 on page 12, seven pages later. When I reached Lemma 4.6 I had to page back to find it.
25. **"Where the corner choices come from", Lemma 3.1.** **ok**. This is the best expository move in the paper. The state is derived from the answer instead of postulated. Verified in under a minute.
26. **Definition of `S_s`** ("the set of all excluded edges"). Not all: the selection also excludes one of the two sides at `s(t)`. I expected "the edges we already know to be excluded".
27. **"The tree of faces", definition of `Y_s`.** I had to hold five objects defined within one page: `P_0`, `s`, `Q_s`, `S_s`, `Y_s`, and `P_s` comes next. Each is motivated, so this is a density complaint, not an order complaint. A small table (symbol, what it is, where it lives) would have helped here.
28. **Lemma 3.3, statement.** Hypothesis is "S_s is a spanning tree of T", but the natural condition (Lemma 3.4, Definition 3.5) comes after. I expected the definition of good state first, then Lemma 3.4, then Lemma 3.3 stated for good states.
29. **Lemma 3.3, proof.** Verified. "every t in A has a parent and therefore exactly one child" needs degree two; it is there.

## Page 6

30. **Figure 4.** **F** (minor). No vertex labels, but the caption speaks of "the vertices 1, 8, 9" and "the roots 0, 4, 5". I flipped back to Figure 2. The picture itself is clear: wedges and dashed sides read well.
31. **Figure 4 caption, last sentence** ("The two states are disjoint; they form the pair of Figure 8"). **T**: "disjoint", "pair".
32. **After Definition 3.5** ("A cycle in `P_s \ {e0}` would be made of sides leaving chosen corners"). Question: why only cycles avoiding e0, and why would a cycle be directed? Both are answered in the proof of Proposition 3.7, but the sentence asserts them early.
33. **"The disk identity", set-up paragraph.** The state is suddenly called r, not s. I looked for a reason. (Later: because it is applied with the first state of a pair. A reader cannot know that here.)
34. **Same paragraph.** "Every face of T lies inside or outside Z, and the outer face lies outside" defines "inside" implicitly. Fine. `I` for the number of interior vertices, `ℓ`, `h`, `B`, `W`: five letters introduced in two lines, but Figure 5 lists them, which rescued me.

## Page 7

35. **Figure 5.** **ok**, the best figure. The table of the five numbers and the three equations beside the picture let me check the lemma on the example before reading the proof. The caption does not say that this cycle is the 7-cycle of `D(r,s)` in Figure 8; I noticed on page 10.
36. **Lemma 3.6, proof, first count.** **V**. "Euler's formula for the plane graph formed by Z and everything inside it, which has I + h vertices, B + W + 1 faces". Euler needs a connected plane graph. I asked: why is this graph connected, and why are its bounded faces exactly the B + W faces of T inside Z? I could supply the first (walk in T from an inside vertex to Z and stop at the first vertex of Z), but the paper says nothing. This is the one place in Sections 2 to 4 where I filled a hole myself.
37. **Lemma 3.6, proof, third count.** Verified. This is the heart and it is written carefully: both halves of bijectivity are named.
38. **Paragraph after the proof** ("Only the third count uses the state ... Without it the conclusion fails for directed cycles of T in general"). **ok**.
39. **Proposition 3.7.** Verified. The second count of faces (through `P_s`) against the disk identity is a two-line contradiction. The sentence after the proof ("a cycle of chosen sides encloses one more white face than black, but a selection running along it would force three more") is the sentence I will remember.
40. `P_0` is reused with a new definition (`P_s \ {e0}`), consistent with Lemma 3.1. Fine.

## Page 8

41. **Figure 6.** **F** (minor). Dense but readable. No vertex labels, while Example 3.8 gives vertex sets `{0,2,4,6,7,8}` and `{1,3,5,9,10,11,12}` that I could not check on the figure.
42. **Example 3.8.** Here I finally learn `e0 = {0,4}` and `c = 5`. "these are all such cycles of this G": six cycles from six good states. I cannot verify; noted as a computed claim.
43. **Signpost before Section 4** ("So Theorem 1.1 follows once we find a good state ..."). **ok**. "Separating triangle" is used here and defined on page 13.
44. **"Why a second state."** Three sentences. I expected more: the claim "A second state takes care of it" is the entire motivation for the central object of the proof. Lemma 4.2 delivers on it, so a forward pointer ("Lemma 4.2 shows that a partner forces one root per tree, leaving only cycles to exclude") would be enough.
45. **Definition 4.1.** "ordered pair (r,s)": I asked which of the two is the one we want to be good. Lemma 4.2 answers (the second). Say it in the definition.
46. **Lemma 4.2 is split from its proof by Figure 7** (statement at the bottom of page 8, Figure 7 at the top of page 9, proof below it).

## Page 9

47. **Figure 7.** **F**, **S**. It illustrates Example 3.8 (Section 3) and was first cited on page 4, but it lands inside Section 4. Caption: "The same selection P_s (bold) in the shared figure style". "Shared figure style" is project talk and means nothing to a reader. Panel (a) repeats Figure 6(a) with half the nodes removed; I did not see what it adds. Panel (b) is useful (the Hamiltonian cycle as a curve between the two trees) and is the picture I wanted near Proposition 2.5.
48. **Lemma 4.2, proof.** Verified.
49. **Paragraph on `D(r,s)`.** Verified; "each of length at least three" uses simplicity (not said). "Its edges are chosen sides for the state r, and so are the edges of Q_s directed as in Lemma 4.2" **ok**: this is where I understood why the disk identity was stated for "chosen sides", and why the state there was called r.
50. **Lemma 4.3.** "the faces t supplying K" **T**: "supplying" is never defined. Clear enough from context (the faces whose side lies on K).
51. **"A sign."** "The reversal of a cycle of Q_s pairs them up" stopped me: if `Q_s` has two cycles, which one? Answered in Lemma 4.5. The definition of `δ` by "to the left" and by "counterclockwise order of the corners" was clear.

## Page 10

52. **Figure 8.** Readable. The caption lists the cycles by vertex number; the figure has no numbers.
53. **Table 1.** Caption is glued to the bottom rule. The table is useful, but it floats above Lemma 4.4, between the definition of `Σ δ` and the definition of J, in the middle of a sentence that began on page 9.
54. **Lemma 4.4.** Verified, including the three-corner identity `δ(u,s) − δ(r,s) = 2δ(r,u)`. The remark after it ("a sign defined by counting cycles alone would not be controlled") answered the question I was about to ask.

## Page 11

55. **Figure 9.** **F**. Labels 1, 8, 9 are printed on top of wedges and edges and are hard to read. Otherwise clear. I checked both signs from the caption values.
56. **Lemma 4.5.** Verified. "Fix an order on the cycles of T" and the following remark ("must be chosen from s alone") are the right care.
57. **"Heights", first paragraph.** **ok** on motivation: "With F = 1 the answer is no" and why. This is the question I had. Then: "We measure, for each white face, how often the chosen corners of s wind around it." **P**. A set of corners is not a closed curve, so "wind around" has no meaning yet. I expected a picture at exactly this point: one white face, its path `γ_w` to the outer face, a few spokes crossing it. There is none in the paper.
58. **Definition of spokes, `γ_w`, `κ_w`, `h_s(w)`, `ω(s)`.** **T**/clash: `w` is a white face here, but a vertex in `δ(v,w)` (page 9) and in Figure 3(c), where the white face is `y`. `h` is already the length of Z; `c_t` next to the root `c` and (soon) the number `c` of cycles; `b` is a root and, in Lemma 4.7, a real number. "segments from c_t to the corners": are the edges of T assumed straight? Nothing says so.
59. **"Changing the paths adds to each h_s(w) a constant that does not depend on s."** **V**. Not proved, and I could not see it in a minute. (It is true, by bijectivity of s, and it is never used, since the paths are fixed once. So why state it?)

## Page 12

60. **Lemma 4.6.** Verified, in about four minutes. I checked the crossing-sign convention against a counterclockwise circle. The deformation of `Γ` to `C` inside the black triangles is convincing. Needed Figure 3(c) from page 5 here. One implicit point: `L(C) ≥ 1` cites the disk identity for C, which holds because C (in either direction) is a cycle of chosen sides for r or for r'.
61. **"The total is not zero."** Typo: "makes the cycles with fewest cycles count". "assuming a pair exists" **ok** (answers entry 8).
62. **Lemma 4.7.** Verified in a minute. Short and elementary. I expected one sentence before it saying why a power: `ω` is affine in the orientation bits, and an alternating sum over c bits kills polynomials of degree below c.
63. **Proposition 4.8.** Verified. One gap of a sentence: "In each face t it has (r'(t), s'(t)) = (r(t), s(t)) or (s(t), r(t))" needs "because the undirected edge set has exactly one edge in each face of A". "the group of (r,s)" would be better "class". "undirected cycle covers" appears only in the last line.
64. **Remark after the proof** ("The minimum m cannot be dropped"). **ok**.

## Page 13

65. **Example 4.9 is split by Figure 10** across pages 12 and 13. "the value of the sum computed pair by pair": I wanted the eight rows (r, s, ε, ω, good or not). Without them `Σ = 18` is an assertion.
66. **Figure 10.** **ok**. First example figure since Figure 2 with readable vertex labels. Shows `Γ`. Arrives a page after Lemma 4.6.
67. **Remark 4.10.** Dense, for readers of the three papers. Fine as a remark. "`i^J = i^{-n} ε`" checks.
68. **Section 5, flow network.** Verified. "a pair is the same as a spanning subgraph ... in which every vertex has degree two" is loose (one subgraph gives `2^c` ordered pairs) but harmless. `V(t)` undefined (corners of t).
69. **"A separating triangle of T is ..."** defined here; used on pages 2, 3 and 8.

## Page 14

70. **Proposition 5.2, proof.** Verified, about six minutes; this is the longest verification in the paper. The reduction to (5.3) is clean. The p = 3 root case is argued at more length than needed (a second black face on a, b, c would share the edge ab with the black face t0). "Let b and w be the numbers of black and white faces of K of length three": `b` and `w` again. The case analysis for `|β(F)| ≤ d_F − 4` is fine.
71. **After the proof.** "The hypothesis entered only to show that a face of K of length three is a face of T." **ok**.
72. **Section 6, Lemma 6.1.** Verified.

## Page 15

73. **Figure 11.** **F**. Panel (b) relabels the inner piece (4, 6, 8, 5, 7, 3) and rotates it relative to (a) and (c), so I had to match the triangle {3,4,5} by marker shape. The inner octahedron in (c) is too small to read. The cap in (b) is drawn as the grey collar (black), which is right but the three panels took a while.
74. **Theorem 6.2, proof.** Verified. The acyclicity paragraph is complete; this is where Proposition 2.5(2) pays off. Base of the induction is the case without separating triangle; fine.
75. **Section 7.** **ok**. Short and each hypothesis gets its place of use. The 2-connected counterexample is described in words without a figure; I could follow it.

## Page 16

76. **"Not every Hamiltonian cycle arises."** I stopped: Lemma 3.1 gives a state for every acyclic selection, and this paragraph says two cycles of the hexagonal prism get the same state, which is not good. So the converse of Proposition 3.7 fails, and the paper's opening promise (step 2 of the route) is one-directional. That is consistent, but it left me asking why the proof finds a cycle through good states at all if not all cycles come from good states. A sentence on that would help.
77. **End.** The paper stops after Section 7. No closing paragraph, which I did not miss.
78. **References.** [1] is "Unsigned manuscript". I cannot judge the arXiv numbers from the PDF.

## Summary of the cold read

Terms used before definition: black/white (route), "edges leaving chosen corners" (abstract, route), disk identity, density bound, cap, `Q_s`, `D(r,s)`, `J`, `ω`, `Y_s` (all in the introduction), state/pair/partner/spoke/`u(t)` (Figure 3 caption), disjoint states and pair (Figure 4 caption), separating triangle (pages 2 to 8, defined page 13), "supplying", `V(t)`, "undirected cycle cover".

Symbols with two meanings: `w` (vertex, white face, number of white triangular faces), `h` (cycle length, height), `b` (root, real constant, number of black triangular faces), `c` (root, number of cycles) with `c_t` and `C` nearby, `P_0`, `K` (cycle of `Q_s`, component of `T[U]`), `S` (edge set in Lemma 2.4, vertex set in Section 5) with `S_s`, `D` (the cycle set `D(r,s)`, the disk `D`), `L`/`ℓ`.

Steps not verified within a minute: Euler on the disk (entry 36, a real omission); path independence of heights (entry 59, unproved and unused); Lemma 4.6 (four minutes, correct); Proposition 5.2 (six minutes, correct); all example numbers.

Figures: 3 is too early and mixes three sections; 7 is too late and in the wrong section; 2, 9 have label collisions; 4, 6, 8 lack the labels their captions and the text use; 11(b) is relabelled; there is no figure for heights. 5 and 10 are good.

Pacing: Sections 2 and 3 are well paced apart from the object pile-up on page 5. Section 4 is the right order (why a second state, reversals, sign, cancellation, heights, nonvanishing) but the heights definition is the hardest paragraph of the paper and has the least support. Section 5 is a correct calculation with no picture. Introduction: the "One picture" and "Sources" paragraphs are written for insiders and sit where a newcomer is still orienting.

I never lost the thread of the argument. After one reading I believe the proof, with the single reservation of entry 36.
