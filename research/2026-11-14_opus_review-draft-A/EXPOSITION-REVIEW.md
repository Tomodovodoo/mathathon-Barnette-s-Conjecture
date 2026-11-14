# Expository review of draft A

Summary.
1. Draft A is correct, short and readable. Its core is clearer than all three source papers: the disk identity as W = B + 1 with Figure 4, the "unweighted sum is zero" motivation for heights, and the closed cube example.
2. It is not yet "far clearer". The reader is never told what Q_s and the spokes are *for* until §5, and the paper never says that P is not built from Q_s. The constructive paper's framing ("we seek s with H − s a spanning tree") already solves this.
3. Lemma 5 is OpenAI's proof copied nearly word for word, including OpenAI's least checkable sentence about t0. It is the one section where draft A is no clearer than its source.
4. Notation is overloaded: B, W, H/h, m, I, U, K, u and b, w each have two meanings, and r and s swap roles in Figure 6.
5. Three of the eight figures are never referenced in the text. Figure 8(c) is unreadable. The most useful missing figure is the shared one-triangle picture `04-local` (D, Q_s and the spokes in one black face), placed at the definition of Q_s.

Line numbers refer to `paper/draft-A/barnette.tex`. Editorial judgments are `HUNCH` (the protocol's term for an unproved judgment); the cold-read evidence for each is in `COLD-READ.md`.

## (b) The style guide's 22 rules

| # | Rule | Verdict | Offending passage or evidence |
| --- | --- | --- | --- |
| 1 | Open with the obstacle | PASS | l.32: degree two is easy, connectivity is the problem, cube example. |
| 2 | Route as implications | FAIL (partial) | §1 gives "forest ⇒ connected complement" well (l.34, l.54). But no paragraph says *pair ⇒ forest Q_s ⇒ H − s spanning tree ⇒ white tree ⇒ P ⇒ two trees*. l.42 ("Our main change is in the signed count. Li … replaces … The constructive exposition … uses … We use the product of face heights …") lists techniques and sources, the pattern rule 2 rejects. |
| 3 | State the contract once | PASS | Theorem 1 (l.37) and Proposition 3 (l.58), each once; the edge prescription is explained (l.40). |
| 4 | Define when the reader wants it | FAIL | l.81: "We need a local choice whose acyclicity can eventually be tested. Put a center c_t in each black face and join it to its corners by three spokes." The spokes have no stated purpose until l.213 (heights) and l.267 (recovery). l.83–85: Q_s is defined and "would be useful only if its components keep the three roots separate", useful for what is never said. Heights (l.211–216) PASS: motivated by "the unweighted sum cannot prove existence". |
| 5 | Names for reusable contracts | PASS | Disk identity named and used three times. Lemma 4 used twice. |
| 6 | Order by dependency and need | FAIL (minor) | l.98–107: the 13-vertex example arrives before the sentence that says what it is for (l.112, "We now have two tasks …"). l.40–42: history and attribution sit between the theorem and the set-up it needs. |
| 7 | Separate definition from assertion | FAIL (minor) | Eq. (7), l.184–185: the definition of J contains the assertion "= #cw − #ccw", which needs Lemma 6. Lemma 4 (l.88): the second sentence asserts existence of a partner without the hypothesis. |
| 8 | Remove stronger targets only after checking | PASS | No algorithm, no exchange components, no determinant. The theorem contract is unchanged. |
| 9 | Retain invariants of repeated operations | PASS | l.198, l.207: cycle chosen from s alone; "The cycle selection stays the same on the return step because s stays fixed." |
| 10 | Goal before formula | FAIL (local) | Lemma 5 proof, l.118: the network comes before the goal (a 2-regular spanning subgraph of B); the goal arrives in l.124. l.238: "Here is the full counting argument, for arbitrary m." names no goal. Elsewhere PASS (l.181 "To assign a sign that reverses on either kind of cycle, put"). |
| 11 | Display decisions; inline routine steps | FAIL (minor) | Eq. (6), l.160, displays E_d counts that Figure 4 does not show; the figure displays B + W = 2I + h − 2 and 3(B − W) = 2ℓ − h. The reader has to reconcile two sets of equations for one identity. |
| 12 | Cite standard tools at the invocation | FAIL (minor) | l.124 cites Ford–Fulkerson correctly, then re-proves integrality ("For completeness, integrality follows by augmenting …"), which the citation already covers. |
| 13 | Keep the calculation specific | PASS | l.165: "The matching count B = I + ℓ is the reason it holds for state cycles. Euler's formula and face coloring alone do not give the conclusion." The best sentence in the paper for this rule. |
| 14 | Audit notation | FAIL | B: incidence graph (l.81) and black face count (l.149; patched by "Here B,W are face counts, not the incidence graph B", l.156). W: white count and the tree W_s (l.269). H (spoke graph), h (cycle length), h_s (height). m: min cycle count (l.232) and edge count of K (l.131). I: interior vertices (l.156) and index set (l.243). U: vertex set (l.126) and set of cycles (l.224). K: component (l.131) and Q_s-cycle (l.198). u: third corner (l.85) and an index (l.258). b, w: face counts (l.133) and b_i heights, w white face. r and s swap roles in Fig. 6 (l.274). |
| 15 | Each conclusion its own reason | PASS | l.54, l.273, l.287 keep degree and connectivity separate. |
| 16 | Distinguish the two reversals | PASS (could be stronger) | The table at l.190–196 is very good. Rule 16 also asks for "purpose and sign effect" columns; adding them makes the table the summary of §4 (E13). |
| 17 | One example across representations | FAIL (partial) | Cube: labels appear only in Fig. 1(b); (c)–(f) unlabelled. 13-vertex example: Fig. 3, 4, 6, 7 have no vertex labels; Fig. 4 shows a cycle the text names by vertex numbers ("1,2,3,9,10,11,6") that cannot be read off it. |
| 18 | Introduce figures by their question | FAIL | Figures 3 (`09-Q`), 5 (`height`) and 6 (`12-tree-cotree`) are never referenced (`grep ref{fig:` gives only 01, 03, 08, 13). Fig. 1(c) and (e) show D, kept spokes and the white tree three to seven pages before they are defined. |
| 19 | Figures readable at print size | FAIL (two figures) | Fig. 2: labels 6, 11, 12 overprinted by white G-vertices. Fig. 8(c): inner octahedron squeezed into triangle 345, vertices 6, 7, 8 unlabelled, markers overlap. Others readable at 130 dpi. |
| 20 | Short causal abstract, literal title | PASS | Five sentences, causal. Title literal. |
| 21 | Keep audits outside the manuscript | FAIL | Bibliography [2], [3], [4] are project folder paths; [4] is authored by "Fable, project research agent". l.107 "the companion calculation [2] also recomputes them with the reference implementation". l.262 "The proof does not assert that a preferred orientation within the displayed group survives cancellation" is a referee's caution in the text. |
| 22 | Compare rendered passages, verify preservation | PASS (author's process), with a risk | The author pinned figure hashes in `build-check.json`. The shared figures `01-cube.pdf`, `11-spokes.pdf` are currently modified, uncommitted, in the working tree by another agent. A rebuild of draft A will silently pick up those versions. Re-check Fig. 1 after any rebuild. |

Score: 9 pass, 2 partial pass, 11 fail. Most fails are local and fixed by edits E1–E25 in `EDITS.md`. Rules 2, 4 and 14 are structural.

## (c) Comparison with the three papers, step by step

O = OpenAI, L = Li, C = constructive paper. "Clearer" means: the cold reader could verify the step and say why it is there.

| Step | Best of the three | Draft A | What the better paper does |
| --- | --- | --- | --- |
| Opening: degree two vs connectivity | C (cube, Fig. 1 two subgraphs side by side) | **As clear as C**, and clearer than O and L. | — |
| Dual reformulation, induced trees | O §2, §7 | Same content, slightly better motivated ("for gluing"). | O states the converse (cycle ⇒ trees) too; neither needs it. |
| Why states, spokes and Q_s | **C §1**: "Join the centre of every black face to its three corners … the resulting graph is H … We seek a tree matching, H − s is a spanning tree. The matching fixes the degrees of the retained graph; the tree condition ensures that it is connected." | **Less clear than C.** Spokes are introduced with no purpose (l.81), Q_s with an unexplained purpose (l.85), and the link Q_s forest ⇔ H − s tree only appears in §5. | C gives the spokes a job in the first paragraph that introduces them. O's Fig. 1(a) puts D and Q_s in one triangle; draft A has no local picture. |
| Pair existence (Lemma 5) | O §3 for the proof; **C Thm 1.2** for the *meaning* of the hypothesis | **Identical to O**, including O's opaque t0 sentence and O's redundant integrality paragraph. Not clearer. | C states the exact criterion (a pair exists iff no separating triangle has black inner boundary). One sentence citing it tells the reader why "no separating triangle" appears and that it is not the true obstruction. |
| Disk identity | O Lemma 4.1 | **Clearer than all three.** W = B + 1 is memorable; Fig. 4 is the best figure in any of the four documents; the remark after the proof (l.165) explains where the state enters. | — (but align eq. (6) with Fig. 4, E11) |
| Sign of a pair | C (integer sign) | Same as O with (−1) in place of i. | The product of local signs ε = ∏δ(r(t), s(t)) (proved in REFEREE.md §3 N7) is simpler than all four. It removes J and its integrality paragraph. |
| Cancellation of cyclic Q_s | O Lemma 5.2 | **Clearer than O** thanks to the two-reversal table and the worked reversal K = 8,1,9. | — |
| Nonvanishing | L (no analysis) | **Clearer than all three.** l.211 ("The unweighted sum cannot prove existence …") states the need for weights better than any source. Heights avoid O's circulation lemma, exponential and Taylor expansion, and L's marked objects. | L's half-rays from white vertices (L Def. 13) are the same idea as heights; the draft should say so (attribution, §(f)). |
| Recovery: white tree, one side per face | O §6.1 | Same as O, plus the cube table. **Clearer.** | Should flag that P uses the side *through* s(t), not Q_s. |
| P is a forest, two induced trees | O Lemma 6.2 | Pairing argument is cleaner than O's signed count. **Clearer**, modulo the two unstated bridges (REFEREE N12c, N12d). | — |
| Gluing | O §7 | Same text plus Fig. 8. **Clearer** if Fig. 8(c) is fixed. | — |

Net: draft A beats the best source at six of ten steps, ties at two, and loses at two (the purpose of states/spokes/Q_s, and Lemma 5). Both losses are at the start of the technical part, where a reader decides whether to continue.

## (d) Unslop audit

The draft is already clean of the loud tells (no puffery, no AI vocabulary, no em dashes, no bold, no chatbot phrases). What survived:

| # | Pattern | Passage | Replacement |
| --- | --- | --- | --- |
| 11 | Synonym cycling | "side" and "edge" for the same object throughout: "one side of each triangular face" (l.54), "edge of Q_s" (l.85), "selected side" (l.273) vs "selected edge" (l.283, l.287). Also "corner" and "vertex" of a triangle. | Use *side* for an edge of T considered as a side of a face, *corner* for a vertex of a face, everywhere. In Lemma 8: "Every boundary side is selected", "selected sides pair black faces with white faces". |
| 14 | Colon as connector | l.32 "the easy part: the complement of a perfect matching"; l.44 "on either side: a singleton"; l.133 "d − 4: for d = 4"; l.230 "outside: the crossings alternate"; l.267 "It is connected: each edge"; l.287 "when it is selected: it crosses". | Make each a new sentence. E.g. l.32 "… is the easy part. The complement of a perfect matching has degree two everywhere." |
| 23 | Filler | l.44 "Here are the details needed for simplicity."; l.124 "For completeness, …"; l.238 "Here is the full counting argument, for arbitrary m."; l.267 "In fact the spokes split …"; l.224 "Indeed, in any such orientation …"; l.254 "Indeed the sign is …". | Delete the first three (E8 removes the second). l.238 → "Now let m be arbitrary." Drop "In fact", "Indeed". |
| 27 | Says how it feels, not what it does | l.85 "A second state supplies exactly this control."; l.81 "We need a local choice whose acyclicity can eventually be tested."; l.42 "The product of heights uses the same cancellation mechanism, with each factor detecting enclosure of one face."; Fig. 7 caption "The separate degree and connectivity arguments are both needed."; l.262 "This displays why two heights are needed here and why nesting causes no problem." | l.85 → "A second state r orients Q_s so that every nonroot has one outgoing edge, which forces each component to contain one root or one cycle." Cut the Fig. 7 sentence. l.262 → "The small cycle lies inside the long one, so w2 sees both reversals, and still only one bijection survives." Others in E1, E3. |
| 28 | Dense sentence | l.44 "A cut of one or two edges in G would have at least three vertices on either side: a singleton in a simple cubic graph has three outgoing edges and a pair has at least four." l.230 "The sector excludes the third corner, even if that corner occurs elsewhere on C, and its interior meets no other part of the curve." | Split each in two. |
| 29 | Passive voice | l.107 "These assignments and all examples below can be checked directly from the face lists"; l.98 "The symbols a_j are the numerical face identifiers used in the figures". | "The reader can check …"; see E20 for the a_j sentence, which is also false (no figure shows a_j). |
| 30 | Adverb propping a verb | "exactly" appears 15 times; at l.85 ("supplies exactly this control"), l.267 ("correspond exactly"), l.287 ("are exactly the two side classes") it adds nothing. | Delete those three. Keep it where it means "one and only one" (l.88, l.149, l.273). |
| 10 | Rule of three | l.42 lists three sources in three sentences in parallel form. | Rewritten in E1. |

## (e) Figures

Widths are fractions of `\textwidth` from the `\fig` calls. "Placement" compares the page of the float with the page of its first in-text reference.

| Fig. | File | Width | Labels | Placement vs first reference | Caption says what to see? | Problems |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `01-cube` | 1.0 | Legible; only panel (b) carries vertex labels | p3; first ref p2. Good. But panels (c) and (e) show D, kept spokes and the white tree, defined on p6–9. | Narrates all six panels; ends "Later sections justify each transition". | Add section pointers per panel (E19). Add labels 0–5 to (c)–(f) (figure owner). |
| 2 | `03-dual` | 0.72 | **Labels 6, 11, 12 collide with white G-vertices** | p4; ref p3. Good. | "Each grey vertex of G" is wrong (G's vertices are drawn black and white). Says a_j appear in figures; they don't. | Move labels off the G-vertices (figure owner); fix caption (E20). |
| 3 | `09-Q` | 1.0 | No vertex labels; caption names 1,8,9 | p4; **never referenced** | Yes, and the last sentence tells the reader what matters. | Add reference (E18). |
| 4 | `08-disk` | 0.85 | ℓ labels legible; no vertex numbers | p6; ref p6. Good. | Yes: B = I + ℓ, the key fact. Best caption in the paper. | Side-panel equations differ from eq. (6) (E11). Small cycle 8,7,12 not drawn. |
| 5 | local `height.tex` | ~0.6 | Legible | p7; **never referenced** | Yes. Last sentence belongs to the proof of (10), two paragraphs later. | Add reference at the definition of height (E18). |
| 6 | `12-tree-cotree` | 1.0 | No vertex labels; "e0" placed beside the outer centre, reads as a label of the centre | p9; **never referenced** | Yes, but "now using the state r of (2) as the forest second state" swaps r and s without warning in the text. | Add reference and the role swap in text (E18, E21). |
| 7 | `13-selected` | 1.0 | Two class markers (dots, squares), legible | p10; ref p10. Good. | Yes; last sentence is filler (§d). | — |
| 8 | `14-gluing` | 1.0 | (a), (b) legible; **(c) unreadable** | p11; never referenced by number but sits right after §6. | Yes. | Redraw (c) with the inner piece enlarged, or drop (c) and say "glued" in the caption (figure owner). Add reference (E18). |

**The missing figure that would help most:** `paper/figures/04-local.pdf` panel (a), "the two edges of a pair in t": one black triangle with r(t), s(t), u(t), the D arrow and the dashed Q_s side. Place it at the definition of Q_s and the pair (§2, l.83–85). It answers the two cold-read stalls ("what is Q_s relative to the state?" and, once the selected side through s(t) is added, "how does P differ from Q_s?"). Its panel (b) carries OpenAI's weights a(t, ·), which draft A does not use. Either clip to panel (a) (`trim` in `\includegraphics`) or ask the figure owner for a variant whose panel (b) shows the three candidate sides: Q_s (opposite s), D (r → s), and the two sides through s(t) from which P selects. Second choice: `15-overview.pdf` as a one-glance map at the end of §1, after its box labels are renumbered to draft A's figures.

## (f) Attribution and framing

What is right. The title and abstract say "an exposition of OpenAI's proof". Theorem 1 is credited to OpenAI. Barnette/Grünbaum 1969, Stein [Thm 2.2], Alt–Payne–Schmidt–Wood [Lemma 5], Tutte, Hine–Kálmán and Ford–Fulkerson are cited at the right places. Li's involutions and the constructive paper's integer signs are distinguished.

What is wrong.
1. **Internal notes cited as publications.** [4] "Fable, project research agent, *A weight-free proof of Proposition 5.1 …*, Unpublished project note, research/2026-11-14_fable_route-combinatorics/PROOF.md" is cited in the introduction as the source of the paper's main change, the disk formulation and the recovery argument. [2] is a script folder. [3] says "supplied as papers/barnette_trees.pdf". An outside reader can open none of these. A model name as author of a citation is not a bibliographic entry.
2. **Pinpoint for Theorem 1.** The edge-avoiding form is OpenAI's Corollary 7.1; the paper should cite `[10, Corollary 7.1]` (and Theorem 1.1 for Hamiltonicity).
3. **Kelmans.** Credited in the text, absent from the bibliography. The clause "and the reduction to graphs without nontrivial three-edge cuts belong to the earlier work of Kelmans" is not supported by any pinpoint the draft gives. OpenAI cites Hertel [Corollary 3] for the edge-avoiding equivalence only. Draft A does not use a three-edge-cut reduction. Cut the clause and cite Hertel's corollary for the equivalence (E24).
4. **Li's crossing counts.** Li's Definition 13 counts crossings of upward half-rays from white vertices with matching edges: the same object as a height. The draft credits Li only for "involutions on marked crossings". It should say that heights are Li's ray counts along fixed paths, combined by a product instead of marked involutions. Not saying this makes the height product look more original than it is. (The combinatorics referee reached the same assessment: "a useful compression and localization of the existing mechanism".)
5. **OpenAI entry** ends "family 180", which means nothing outside the project.

How an expository paper should present the project's simplifications. State them in the paper's own voice, once, with no internal citation:

> Two arguments here differ from the sources. Proposition 7 replaces OpenAI's positive spoke circulations and exponential sum by a product of signed crossing counts at white faces, a close relative of Li's half-ray counts. Lemma 8 proves acyclicity by pairing faces through selected sides. Both work inside OpenAI's mechanism, with the same disk identity and the same two regroupings, and both are proved in full below.

If the project wants to record who found them, an acknowledgement does that ("The height formulation of Proposition 7 and the face-pairing proof of Lemma 8 were worked out while preparing this exposition."). The companion scripts belong in a "Data availability" sentence that names a public repository, not in the bibliography. E1 and E24 give the exact text.
