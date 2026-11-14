# Cold read of draft A (paper/draft-A/barnette.pdf)

Phase 1 log. Read from rendered PNGs at 130 dpi, one page at a time. The only other file read before this log was `research/BRIEF.md`. References are page.paragraph (p2.¶3 = third paragraph on page 2) or the numbered item. Each entry: what I expected, what I got, the question in my mind.

## Page 1

- **Abstract.** Clear first sentence. "Two disjoint face–vertex matchings" reads as "edge-disjoint matchings", which is the right notion ("differ at every face"), but "disjoint" will only be pinned down on p2. "heights at white faces" is opaque but tolerable in an abstract.
- **p1.¶1.** Good opening: degree two is easy, connectivity is the problem, cube example. *Expected a figure of the cube with the two-square 2-factor here.* Got none; I drew it in my head.
- **p1.¶2.** "There, omitted edges become a forest." Hesitated: which omitted edges? The duals of the matching edges. Readable after a second pass. "Planarity turns acyclicity of those edges into connectivity of their complement" is the key duality fact, stated before Lemma 2. Good order.
- **p1.¶3.** Definitions of cubic and 3-connected arrive just before the theorem. Fine.
- **Theorem 1.** "For every edge e, a Hamiltonian cycle avoiding e." Expected a sentence saying this is stronger than Barnette's conjecture and why we want it; got it in the next line ("The edge prescription will let solutions on smaller pieces agree when we glue them"). Good.
- **p1.¶4 (history).** Dense chain of five citations in four sentences. Fine for a historian, heavy for a learner. "Stein's region-partition formulation led to the two-induced-tree formulation" — at this point I do not know what either is.
- **p1.¶5 ("Our main change").** Here I stalled. "root-component count", "product of face heights", "disk identity", "recovery argument", "each factor detecting enclosure of one face": five undefined terms in one paragraph. Question: is this paragraph for me now, or for a referee comparing with OpenAI? It reads as the second. It also cites "the project note [4, Sections 1–3]" as a source of the main new idea. *What is [4]? Can I read it?* I cannot tell from here whether it is published.
- **p1.¶6 (simplicity of the dual).** Placed after the history and the roadmap, so the reader switches from "what we do differently" back to basic set-up. I checked the cut argument (singleton has 3 outgoing edges, adjacent pair has 4, so a 1- or 2-edge cut has ≥3 vertices on each side; deleting ≤2 endpoints disconnects). OK in about a minute. Euler: |V(T)| = |F(G)| = 2 − V + 3V/2 = 2 + V/2 ≥ 4. OK.
- **p1 last ¶.** "We use the following elementary fact about duality." Then a definition of spanning forest, then the lemma is on the next page. The page break splits announcement from lemma (layout, minor).

## Page 2

- **Lemma 2.** Proof is three sentences; "Contract the tree to one vertex. Faces are preserved, and its edges disappear from the dual." I had to think: contracting primal edges deletes the corresponding dual edges, and the remaining dual (dual of a one-vertex bouquet) is connected; the count |E|−|V|+1 = |F|−1 makes it a tree. Verified in ~1 min. Fine for a reader who knows planar duality; a figure (tree + dual cotree) would make it immediate.
- **p2.¶1.** "Thus we want a forest P in T with exactly one side of each triangular face." Clear and good: this is the target object. I underlined it.
- **p2.¶2 (induced trees).** "For gluing, we will obtain this forest as two induced trees." Question: why induced trees *rather than any forest*? The answer "for gluing" is a promissory note to §6. The deduction "no triangle is monochromatic, so each triangle has exactly one edge within a class" is right, but it never says that P *is* the union of the two trees' edge sets. I inferred it.
- **Proposition 3.** Clear statement. I checked the direction: e0 has both ends in one tree, so its dual edge is not on the cycle; t0's other two sides cross. Consistent with Theorem 1 (avoid e = e0*). The text never spells out this translation (which edge of G is e0*, why the cycle avoids it). A one-line "the Hamiltonian cycle is the set of edges of G dual to bichromatic edges of T" would help.
- **p2.¶4.** "The matching and cancellation arguments in between will also apply whenever a pair of states exists." Forward reference to "pair of states" before states are defined. Mild.
- **Example (cube).** Good that an example appears early. I checked the face list is a proper 2-colouring of the octahedron (antipodes 0–3, 1–4, 2–5). "The octahedron labels in Figure 1 are these vertex labels." **Figure 1 is not on this page.** I looked for it and did not find it on p2. Expected to see it here.
- **"so the eventual cube cycle must omit t0y0"**: notation switch: t0y0 is now a *primal* edge named by its two dual faces. Took a moment.
- **§2 ¶1.** Euler count k+2 vertices: 2k faces, 3k edges, V = 2 − 2k + 3k. Fine, quick.
- **§2 ¶2 (spokes).** "We need a local choice whose acyclicity can eventually be tested." Vague; I did not know what "local choice" ranges over. "We will delete one spoke at each bounded black center and one at each nonroot" — I read this twice. It means: the deleted spokes form a perfect matching between centres of A and X. Then the state is defined as the bijection. Question: **why introduce spokes and centres at all**, when the next paragraph immediately "suppresses the centre" to get Q_s = side opposite s(t)? I expected the spokes to be needed later; at this point they are a detour.
- **§2 ¶3.** Q_s defined. Clear once decoded: one side per bounded black face, the side opposite s(t). Question in my mind: **how does Q_s relate to the target forest P?** P needs one side of *every* triangle including white ones and t0; Q_s has one side per bounded black face only. The draft does not say here what the relationship is. I expected "Q_s will be one of the two induced trees" or similar.
- **§2 ¶4.** "A forest Q_s would be useful only if its components keep the three roots separate." Useful for what? I did not know. Pair (r,s) and orientation r(t)→u(t) defined; outdegree one at nonroots, zero at roots: clear and checkable instantly.
- **Lemma 4.** Statement mixes two hypotheses. Sentence 2 ("If Q_s is a forest, it has three components, one at each root, and s has exactly one partner") is only true under the standing hypothesis of sentence 1 (s has a partner): a forest Q_s with a rootless component has no partner. Read literally, the second sentence asserts existence of a partner for every forest Q_s. Should read "If s has a partner and Q_s is a forest, ...". Proof itself is clean (v − a edges ≥ v − 1).
- **p2 last ¶.** The "outdegree observation" stated as a reusable tool. Good practice.

## Page 3

- **Figure 1** (top of p3, first cited on p2). Six panels at a good size; read at 130 dpi without zoom, except the vertex labels in (b), which are small but legible. Only panel (b) carries vertex labels; (c)–(f) are unlabelled, so I had to carry 0–5 over by position. I checked (d) against the text: dashed sides 24, 13, 05 and filled wedges at s(t2)=3, s(t3)=4, s(t1)=5. Correct.
- **Panels (c) and (e) arrive too early.** (c) is titled "two states and D": D is not defined until p6. (e) "kept spokes and the white tree": both concepts arrive on p8–9. The caption says "Later sections justify each transition", which admits this. On first sight I could not tell what the green curve with a double ring in (e) was. I came back to it on p10.
- **Caption of Fig. 1.** Says what each panel shows, in order. Good. But "the opposite edges form three rooted trees. Deleting the filled spokes gives an incidence tree and a complementary tree on white faces" is three new ideas in two sentences for a reader on p3.
- **Example (cube continued).** r = (3,4,5), s = (5,3,4) in face order t1,t2,t3. Q_s = {13, 24, 05}, Q_r = {15, 23, 04}: both forests. Verified in < 1 min. "To see cancellation of a cyclic Q_s, we need a larger example." *Cancellation of what?* The signed count has not been mentioned since the intro. Forward reference.
- **Table (2).** I verified that r and s are states (each value a corner, both bijective onto X = {1,2,3,6,…,12}), that they differ at every face, that 18, 19, 89 form a cycle in Q_s, and that Q_r = {01,03,17,29,49,4·11,56,6·12,8·11,8·10} is a forest with components {0,1,3,7}, {4,2,9,11,8,10}, {5,6,12}, one root each. Took ~4 minutes; all correct. The face names a_j (a0, a2, a7, …) with gaps in the indices puzzled me: "the numerical face identifiers used in the figures", but **no figure shows a_j labels** (Fig. 2 labels only vertices). Question: why these indices and not t1..t10?
- **Citation [2] "the companion calculation"**: what is it? (Checked bibliography at the end: an internal project folder.)
- **Last ¶.** "We now have two tasks: obtain a pair at all, then find a pair whose second state has forest Q_s." Excellent: this is the sentence I needed, and it is the clearest roadmap sentence so far. It should come before the 13-vertex example, not after.

## Page 4 (figures only)

- **Figure 2.** Large (half page), appropriate for a 13-vertex example. Problems: the labels 6, 11, 12 sit on top of white vertices of G and are partly obscured (the "11" is struck through by a circle). Primal G is drawn in thin grey and is hard to follow among the triangles; the large black dots of G inside black faces look like the vertices of T. The caption says "Each grey vertex of G", but G's vertices are drawn black and white, not grey. No face labels a_j, contrary to p3.
- **Figure 3.** Q_s and Q_r side by side, no vertex labels. The caption names the triangle 1,8,9; I located it by comparing with Fig. 2 above. Fine because both figures are on the same page. Caption ends with a sentence that says what to see ("The proof must guarantee a pair with the second behavior"). Good.

## Page 5

- **Lemma 5 (a pair exists).** Statement clear. The proof starts with the network without saying what we want from it (a 2-regular spanning subgraph of B, i.e. two disjoint perfect matchings). That sentence comes after the flow. I expected the goal first.
- "minimizing over the placement of the black faces gives capacity 2(n−|S|) + Σ min(2, |V(t)∩S|)": checked (a black face on the source side costs 2, on the sink side costs its incidences into S). OK.
- "For completeness, integrality follows by augmenting from zero along residual paths …": a two-line proof of the integral max-flow theorem after citing Ford–Fulkerson. **Too slow here**; nobody reading this needs it.
- **"Include t0 in the sum with contribution zero."** I stopped here for several minutes. b(U) counts "actual black faces" with all corners in U; t0 has all corners in U (roots ⊂ U) and later (bottom of p5) is counted in b. The sum Σ_{t∈A} shortfall = Σ_{t∈A}(induced sides − [j=3]) equals e(U) − 3 − (b(U) − 1) = e(U) − b(U) − 2 when b includes t0. So t0 contributes 3 − 1 = 2 to "induced sides minus one", not zero; what is zero is its shortfall. I reconstructed (3) ⇔ (4) myself; the text does not show it. **Step not verifiable within a minute.**
- **"actual black faces"**: "actual" is a defined-by-contrast word (actual faces of T versus faces of K), but the contrast appears a paragraph later.
- **Component argument for (4).** "Every triangular face of K is an actual face of T": this is where the no-separating-triangle hypothesis enters. The text does not flag that this is the (only) use of the hypothesis. I had to check that the K-vertex off the cycle forces the empty side to be the K-face. OK after ~2 min.
- **Signed side count, |b′ − w′| ≤ d − 4.** Clever and correct (Σσ ≡ d mod 2, divisible by 3, |Σσ| ≤ d). I checked d = 4, 5, ≥6. A figure of one non-triangular region of K with its ± sides would make this immediate. None exists.
- Displayed chain 2m = 4f − b − w + Σ(d−4) ≥ 4f − 2b, then Euler, then m − b ≤ 2p − 4: checked, OK.
- **Pace of Lemma 5 overall:** the hardest counting in the paper, delivered faster than anything else, with the one unnecessary detail (Ford–Fulkerson integrality) spelled out. Inverted emphasis.
- **§3 ¶1.** "To choose the sign, we first need a restriction on cycles made from state choices. It will also prove acyclicity at the end." Good motivation; tells me why the disk identity comes now.
- **δ convention.** "black face on the left": clear. I immediately wanted to know the sign for a counterclockwise boundary of a black triangle (+1). Not stated here; it is used on p7.
- **Lemma 6.** Statement packs three facts and a convention. "B, W" clash with the incidence graph B; the proof even says "Here B, W are face counts, not the incidence graph B." That is a patch, not a fix: rename one of them.

## Page 6

- **Proof of Lemma 6.** B = I + ℓ (the state's bijectivity) is the heart; the text says so after the proof ("The matching count B = I + ℓ is the reason it holds for state cycles"). Very good remark. I verified the three counts and the elimination in ~2 min.
- **Example (the larger disk).** D(r,s) cycles 1,2,3,9,10,11,6 and 8,7,12: checked from table (2). Uses "join r(a_j) to s(a_j)" before D is named (D is named 20 lines later). Fine.
- **Figure 4.** The best figure in the paper: one cycle, ringed interior vertices, ℓ marked, counts beside it. But the **side panel equations differ from (6)**: the figure shows B + W = 2I + h − 2 and 3(B − W) = 2ℓ − h, the text shows E_d = 3B + h − ℓ = 3W + ℓ and an Euler count with E_d. They are equivalent, but I had to derive B + W = 2I + h − 2 (Euler for a triangulated disk) to see that. The small clockwise cycle 8,7,12 is mentioned in the text but not drawn in Fig. 4. No vertex labels, so "1,2,3,9,10,11,6" cannot be read off the figure.
- **Proposition 7 and its two-line plan.** "Fixing s will cancel every cyclic Q_s. Fixing the undirected cycles formed by both states will show that a suitable sum is nonzero." Excellent: exactly what a reader needs before the sum.
- **D(r,s).** Clear. "There are no loops or doubled undirected edges": checked.
- **(7)** J and ε. I asked "why is the exponent an integer?" and the answer is on the next page. Good order, but the page break separates it.

## Page 7

- **Table of the two operations.** Very helpful. This is the kind of summary the whole paper could use more of.
- **Involution on cyclic Q_s.** "Choose a simple cycle K by any fixed ordering of the cycles of Q_s, using s alone." Clear. Why K is directed: the outdegree observation from p2 (named "the same outdegree observation will be used repeatedly"); the text does not point back to it here.
- **δ(u,s) − δ(r,s) = 2δ(r,u)**: verified with the ccw example given. Then "Lemma 6 on K therefore gives J(r′,s) − J(r,s) = ±2": I had to supply that Lemma 6 is applied with the *state r* and chosen edges r(t)→u(t) (not D). One clause would fix this.
- **Running example.** K = 8,1,9; r changes at a7, a9, a21 from (8,1,9) to (1,9,8). Checked u(t) at each. "The values of J are 0 and −2": J(r,s) = 0 checked from p6; J(r′,s) = −2 I checked partly by hand: D(r′,s) has cycles 1,7,12,8,10,11,6 and 2,3,9; to recompute in phase 2.
- **"The unweighted sum cannot prove existence"**: the best motivating paragraph in the paper. It tells me why F is needed and what F must do.
- **Heights.** Definition clear; Figure 5 placed right after it. Why *white* faces? Answer is implicit (cycles enclose white faces; Lemma 6 guarantees one). Why are spokes back? Here the reader finally sees why centres and spokes were introduced on p2: the height is a crossing count of spokes. **That explanation should be on p2 when spokes first appear,** or the spokes should be introduced here.
- **Figure 5.** Small, clean, correct. Caption's last sentence ("Replacing an edge of D by its two-spoke route changes no white face's side of the curve") belongs to the proof of (10), which has not started yet. OK.
- **Paragraph introducing (10).** "Its pairs are exactly the independent orientations of its cycles": clear. s_− and U defined, then (10). Good.

## Page 8

- **Proof of (10).** Checked: the change at one face is κ_w(t,v′) − κ_w(t,v), the crossing count of v → c_t → v′; the routes form a simple closed curve isotopic to C through black sectors; exit counts +1. The sign convention check (exit = +1 for ccw) took me ~2 min with Fig. 5.
- **Choice of F.** m = minimum number of D-cycles; w_i inside the i-th cycle of a minimiser D*. Clear and well motivated by the previous page.
- **(12)–(13).** The inclusion–exclusion is cleanly done. I verified the sign (−1)^{(n+m)/2+m} = (−1)^{(n−m)/2}. "Here is the full counting argument, for arbitrary m": "full" made me wonder whether an earlier partial argument existed (it did not).
- **Example (what the count sees).** The four-term difference = 1: verified by expansion. "Six pairs have forest Q_s and two cancel": I cannot check without computation. "The other group contributes a nonnegative integer with the same overall sign": slightly garbled (a nonnegative count times the common sign).
- **"The proof does not assert that a preferred orientation within the displayed group survives cancellation."** I read it three times. I think it means: do not conclude that the pair with all-clockwise D is a forest pair. Useful warning, unclear phrasing.
- **§5 ¶2.** "We still need one selected side at every white triangle as well as every black triangle." This answers my p2 question about how Q_s relates to P, three pages late. And the answer is surprising: P does **not** contain Q_s; P takes in each black face a side *through* s(t), not opposite it. Nobody told me Q_s was scaffolding.

## Page 9

- **H and its faces.** "Its faces correspond exactly to the white triangles": checked. OK.
- **Spanning tree of H, dual tree W_s.** Uses Lemma 2 again. Clear. Notation load now: H (spoke graph), h (cycle length), h_s (height); W (white count), W_s (white tree), w (white face); B (incidence graph and black count). Three collisions.
- **Selection rule.** Clear, and the cube table on p10 confirms it. "Each bounded black face contributes one side … y0 receives e0. Thus P has exactly one side of every face." Checked.
- **Figure 6.** No in-text reference found anywhere on pp8–10. Caption: "now using the state r of (2) as the forest second state". **The roles of r and s swap here.** I had to re-read table (2) to follow. The label e0 sits next to the outer centre square at the bottom, so it looks like it labels the centre, not the arc 04.
- **Lemma 8 proof.** The pairing argument (selected edges pair black faces with white faces; inside the disk the unpaired faces are exactly the inner faces of boundary edges) is lovely, and I could verify it. One unstated point: y0 (paired with t0 through e0, which is not in P0) must lie outside the disk. True because y0 has two roots as corners and the closed disk has no roots, but not said.
- **Jordan-curve ending.** "Both sides contain vertices, as any unselected edge shows. Each component of P lies on one side, and there are two components, so they are exactly the two side classes." Verified. Nice.

## Page 10

- **Figure 7.** Placed above its reference at the bottom of p10. Panel (b) uses dots vs squares for the two classes, consistent with Fig. 1(f). Readable.
- **Cube completed.** Assignment table checked row by row. The Hamiltonian cycle t0, y2, t2, y3, t3, y0, t1, y1, t0: I checked every edge is a T-edge not in P and t0y0 is avoided. Correct. Very satisfying to see the example closed.
- **§6 Gluing.** Colour of the cap: three signs ±1 summing to a multiple of 3. Neat and quick. "Apply induction first to the piece containing the original face t0." Clear. "Rename the two labels to agree on the common triangle." Clear.

## Page 11

- **Union is a tree / induced.** Checked. Short and right.
- **Figure 8.** Panels (a) and (b) legible. Panel (c) "glued": the inner octahedron is squeezed into triangle 345, its vertices 6, 7, 8 are unlabelled and the markers overlap; I could not read (c) and relied on the caption.
- **Proof of Theorem 1.** It comes after §6, on the last page. Fine logically. The translation "the cycle avoids e because e0 lies within one tree class" finally makes explicit what I asked on p2.
- **References.** [2] is a folder path in this project; [3] is "supplied as papers/barnette_trees.pdf"; [4] is "Fable, project research agent … Unpublished project note … research/2026-11-14_fable_route-combinatorics/PROOF.md". A reader outside the project cannot open any of these. The intro credits the paper's main simplification to [4]. Kelmans is credited in the text but has no bibliography entry. [10] ends with "family 180": meaningless to an outside reader.

## Global impressions at the end of the cold read

1. **Proof structure is visible and correct as far as I could check.** Every lemma I tried closed. The arc pair → forest pair → two trees → glue is clear by p8.
2. **The paper never says early what Q_s is for.** Q_s is defined on p2 and dropped on p9 for P, a different set. The reader carries an unanswered "how does Q_s become P?" for seven pages.
3. **Spokes are introduced on p2 with no role and used on p7.**
4. **Lemma 5's proof is the densest passage and has the one genuinely hard-to-verify step ("include t0 with contribution zero").**
5. **Figures are mostly good** (Fig. 4 best; Fig. 1 a useful overview but two panels premature; Fig. 2 has label collisions; Fig. 6 unreferenced; Fig. 8(c) unreadable). No figure for Lemma 2 (tree/cotree) or for the region count in Lemma 5.
6. **Notation collisions:** B, W, H/h, r/s role swap in Fig. 6.
7. **Intro paragraph "Our main change"** front-loads undefined terms and cites an internal note.
8. **Pace:** §1–2 good; Lemma 5 too fast; §4 just right; §5 good; §6 good.
