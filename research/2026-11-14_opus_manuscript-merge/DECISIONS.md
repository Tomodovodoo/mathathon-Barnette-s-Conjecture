# Merge decisions

Object: `paper/main/barnette.tex` (18 pages with references, built from draft B's skeleton). Every finding of the two review folders is listed below with its fate. "B" is `paper/draft-B`, "A" is `paper/draft-A`. Review files: `research/2026-11-14_fable_review-draft-B/` (RB) and `research/2026-11-14_opus_review-draft-A/` (RA).

## 1. Backbone

**Decision: dual triangulation as the backbone, with primal readings in remarks.** `research/2026-11-14_fable_referee-primal/RECOMMENDATION.md` exists and recommends a primal backbone with dual pictures. I did not follow it, for four reasons.

1. Its main evidence is that both dual drafts tripped on the inside of a cycle. RB's Lemma D (here Lemma 2.2) closes that in five lines, and the manuscript now spends a full paragraph on what the inside of a cycle is: `R_Z` is a plane graph whose faces are the inner faces of `T` and the outside of `Z`, each bounded by a cycle, so it is connected and Euler applies; a vertex strictly inside has all its faces inside (no pinch). A's missing "y0 is outside" (RA N12c) is closed by the sentence "it is not e0, whose ends are roots".
2. Its second argument is the weights: the primal flow replaces spokes. The face-path heights adopted here are the same flow written in the dual (RB S1 says so), so the spokes, the slide and the winding numbers are gone in the dual too.
3. All refereed text (both drafts, both referee reports, 25 + 25 edits) and the entire figure toolkit are in the dual. A primal rewrite in the time available would have produced an unrefereed text with no figures. The recommendation itself calls the primal note "not paper-ready".
4. The recommendation keeps the dual for the two steps a reader must see (states, disk identity). Those are the heart of the paper.

What I took from it: the recovery tree `Y_s` is presented as a subgraph of `G` (it is `T* - S_s*`); the gluing is read in `G` in one paragraph (3-edge cut, contraction, Li Appendix C); the real sign `∏δ` and the polynomial `F(w)` (Remarks) are as it recommends. No dictionary table: the paper uses `G` only in Section 2 and in two remarks, so a table would add an object without a consumer.

## 2. Structure (COMPARISON.md merge plan)

| Plan item | Fate | Reason |
| --- | --- | --- |
| B's skeleton and order | accepted | Sections 2 to 6 follow B. |
| A's first paragraph | accepted, edited | "A Hamiltonian cycle is a connected spanning subgraph in which every vertex has degree two..." then Hall, then the cube. |
| A's cube overview as Figure 1 | accepted | `01-cube` regenerated: panel (e) shows `S_s` and the tree of faces instead of kept spokes, vertex labels in (b)-(f). The user named it as an option; it is lighter than `16-at-a-glance`, whose notes text is a second caption. |
| B's four-step route | accepted as one paragraph "The plan" with panel pointers | user asked for the plan in one paragraph. Edit RB-8 included ("as soon as one pair exists", separating triangle defined in place). |
| History after the theorem, credits after the plan | accepted | "History and sources" follows "The plan". |
| "Sources" as a final section | rejected | the user asked for history and credits after the reader knows what is proved, and for a closing section of remarks of about a page and a half. Credits went into the introduction (one paragraph plus one paragraph of departures), the closing section is remarks only. |
| Lemma D in Section 2 | accepted (Lemma 2.2) | used three times. |
| Keep B's parity proof of duality, A's contraction proof as a remark | accepted | one sentence after the proof. |
| Hamiltonian-curve panel right after Prop 2.5 | partly | Figure 6 (13-selected) is cited there and placed at Example 3.10, where its object is built. Moving it to Section 2 would show `Y_s` before it is defined. |
| Print two states (A's table) | accepted | Example 3.3 prints `α` and `β` face by face. |
| Cube recovery table from A | condensed | one sentence in Example 3.10 gives the three selected sides and the two trees; the full table would repeat Figure 1(e)-(f). |
| A's remark "a good state has exactly one partner" | accepted, proved | last sentence of Lemma 4.2 with proof. |
| Outdegree principle once | accepted | Lemma 3.7, used in Prop 3.9, Lemma 4.2 and Lemma 4.3. |
| Product sign | accepted | see section 4 below. |
| Face-path heights + new figure | accepted | see section 4 below; Figure 9 (`17-heights`). |
| Table of the eight pairs (RB-16) | accepted, values recomputed | the ω column changed because the heights are now defined by face paths (shortest paths, ties by face index); class sums 12 and 6, total 18, as before. |
| A's "what the count sees" | condensed | two sentences in Example 4.9 with the class sums. |
| Remark 4.10 with RB-14 and Li credit | accepted | Remark 4.10 and the credit sentence after Lemma 4.6. |
| Section 5 with `06-flow` | accepted | Figure 10. |
| Section 6 with RB-1c, RB-20b | accepted | |
| Section 7 hypotheses with RB-15 | accepted, merged into the closing Remarks | |
| One example or two | two, as A and RB propose | the cube is confined to Figure 1 and one sentence of Example 3.10; the 13-vertex triangulation carries every step. |
| How to cite project notes | neither A's bibliography entries nor B's "unpublished notes" | the user ruled: no internal citations, simplifications in the paper's own voice. The departures paragraph says what differs from OpenAI and that each is proved below. |

## 3. Findings of the review of draft B

### REFEREE.md

| Finding | Fate | Where / why |
| --- | --- | --- |
| G1 Euler on the disk without connectedness | accepted | Lemma 2.2 and the paragraph "The inside of a cycle" before Lemma 3.8. Also used for connectivity of `T` (stated after Lemma 2.2) and of the pieces (Lemma 6.1). |
| G2 spokes are "segments" | moot | no spokes in the paper. The edges of `G` are drawn as polygonal arcs (Section 2), which the Jordan curve arguments need. |
| G3 "changing the paths adds a constant" | accepted (dropped) | "The paths are fixed once and for all." |
| G4 back-reference in Prop 4.8 | accepted | "This edge set contains exactly one side of each face t ∈ A". |
| G5 two faces share at most one side (unstated) | accepted | stated and proved after Lemma 2.1, used in Lemma 3.6. |
| Section 4: Li's marks are not `ω^m` | accepted | Remark 4.10 says "symmetric function of degree m"; the introduction no longer says "the weight ω^m that all three papers use". |
| Section 4: hexagonal prism holds for one side only | accepted, recomputed | Remarks: the equator side gives 4 cycles, 2 produced; the two apex sides give 2 and 2 (`example.txt`). |
| S1 heights by a path of faces | accepted after my own check | section 4 below. |
| S2 product sign | accepted after my own check | section 4 below. |
| S3 define "good" before Lemma 3.3 | accepted | Definition 3.4, Lemma 3.5, then Lemma 3.6. |
| S4 outdegree principle once | accepted | Lemma 3.7. |

### EDITS.md (25)

| Edit | Fate |
| --- | --- |
| 1a, 1b, 1c Lemma D and its three uses | accepted |
| 2 split Figure 3 | accepted differently: one figure with panels (a) a state and (b) a pair, placed in Section 3; (b) is cited again in Section 4. Panel (c) dropped with the spokes. A separate float for (b) in Section 4 would have added a page for a three-line picture. |
| 3 FloatBarrier, `[tb]`, caption of Figure 7 | accepted (`\FloatBarrier` before Sections 4, 5, 6; all floats `[tb]`; new caption without process talk) |
| 4 a figure for heights | accepted: `17-heights`, two panels, face `{1,8,9}`, signed turned corners, heights −1 and 0 |
| 5 face-path heights | accepted with my notation (`η_s(y)`, path `f_0..f_j`) and an added combinatorial description of "left" |
| 6, 7 | moot (no spokes) / accepted (G3) |
| 8 route sentence | accepted inside "The plan" |
| 9 notation renames | accepted: white face `y`; height `η`; constant `ω_0`; `f_•, f_∘`; component `H`; region balance renamed `bal(F)` (because `β` is now a state). Instead of a table in the paper, `NOTATION.md` here; the paper defines each symbol at its first use and the reviews' overloads are gone. |
| 10 define good first | accepted |
| 11 why a power | accepted (paragraph before Lemma 4.7) |
| 12a missing reason; 12b "group" to "class" | accepted |
| 13 sources paragraph | accepted in substance, rewritten in the paper's own voice without "working notes" |
| 14 Remark 4.10 | accepted |
| 15 prism side | accepted |
| 16 table of the eight pairs | accepted, values recomputed for face-path heights |
| 17 abstract | accepted in substance (the condition is said; long sentence split) |
| 18a, 18b two slips | accepted ("acyclic" added; part (2) said to be used in Lemma 3.1 and the gluing) |
| 19a, 19b process talk | accepted ("The numbers quoted for the example come from exhaustive enumeration.") |
| 20a, 20b Kelmans | accepted with the history folder's caution: "goes back to Kelmans, as explained by Hertel [Cor. 3] and Gorsky-Steiner-Wiederrecht [Thm 4.3]"; reduction "goes back to Kelmans; see APSW Section 5". Kelmans's paper is not in the bibliography because nobody in the project has seen it. |
| 21 Figure 2 caption and labels | accepted: roots and `e0` named; labels got a white backing in every figure (draw.py) |
| 22 `S_s` "excluded by every such selection" | accepted |
| 23 cite Table 1 | accepted; table gained "sign" and "used for" columns (RA E13) |
| 24 Section 2 title | accepted |
| 25 why a second state | accepted |

### EXPOSITION-REVIEW.md, the seven failed rules

| Rule | Fix |
| --- | --- |
| 4 objects before definition (Sources paragraph, Figure 3 caption) | the sources paragraph uses no symbols; Figure 3 sits after Definition 3.2 and its panel (b) caption says "(Section 4)". |
| 10 goal before formula at the `m`-th power | paragraph "Here is why a power" before Lemma 4.7 |
| 12 Euler hypothesis; winding-number fact | Lemma 2.2; winding numbers removed |
| 14 notation | see edit 9 and `NOTATION.md` |
| 17 labels in every panel | labels added to Figures 1(b)-(f), 4, 5, 6(b), 7, 8, 9 |
| 18 figures by the question | captions rewritten to say what to look at; text cites each figure at or just before its float |
| 21 process talk | removed |

### COLD-READ.md

Every **T** entry (term before definition) is fixed by the reordering above; the **V** entries are G1 (fixed), the path-change remark (dropped), Lemma 4.6 (new shorter proof) and Prop 5.2 (unchanged; root case shortened as RB suggests). CR 76 (why only good states) is answered in the closing remark "Which Hamiltonian cycles arise", with a two-line proof that a cycle arises exactly when its state is good.

## 4. The two refereed simplifications, checked line by line

**Product sign (RB S2, RA N7).** Checked: in a black triangle the directed edges `r→s`, `s→u`, `u→r` run the same way round, so they have equal `δ`, hence `δ(u,s) = −δ(r,s)` and `δ(s,r) = −δ(r,s)`. Both reversals flip every factor on the cycle; the cycle is a directed cycle of chosen sides for `r` (the `Q_s`-cycle with sides `r(t)→u(t)`, the `D`-cycle with `r(t)→s(t)`), so it has odd length by the disk identity. For the grouping: a cycle of length `h` with `δ`-sum `∓3` has `(h±3)/2` factors −1; the total is `(n−3c)/2 + 3c⁺`, same parity as `(n+c)/2 + c⁺`; so `ε = (−1)^{(n+c)/2}(−1)^{c⁺}`, equal to draft B's `(−1)^{(n+J)/2}` with `J = c − 2c⁺`. `COMPUTED`: equality on all 8 pairs of the example (`example.py`); RA checked 196 pairs, RB's reviewer 1,246 instances.

**Face-path heights (RB S1).** Checked: (i) a shortest path in `G` from `y` to `t0` exists and repeats no face; a black face on it is entered and left across two distinct sides (two faces share at most one side), which meet in one corner. (ii) The summand of a face `t` on the reversed cycle is 0 unless the path crosses `g = s(t)r(t)` inside `t`, i.e. turns around `r(t)` or `s(t)`. (iii) The four cases (t left or right of `s(t)→r(t)`, path turning around `r(t)` or `s(t)`) all give +1 for a left-to-right crossing; I verified each with explicit coordinates (s=(0,0), r=(1,0), u=(0.5,±1)). (iv) Every crossing of the path with `C` is counted once, at the black face of the crossed edge, which is in `A`, not an end of the path, and visited once. (v) Exits minus entries of a counterclockwise cycle along a walk from `y` to the outside equals `[y inside]`, by Lemma 2.5(1). (vi) The combinatorial form of "left" (corners `v, a', b'` counterclockwise) agrees with the coordinate check. `COMPUTED`: the lemma on all 16 reversals of `D`-cycles of the example, every white face (`example.py`), and RB's 736 reversals on 148 rootings.

## 5. Findings of the review of draft A

### REFEREE.md

| Finding | Fate |
| --- | --- |
| N4 Lemma 4 sentence false without the partner | moot in B's lemma; my Lemma 4.2 states "a good state has exactly one partner" with proof. |
| N5b "include t0 with contribution zero" | accepted: B's computation `2n − (e(U) − 3) + (b(U) − 1)` with `b(U)` counting `t0`, stated explicitly; I re-derived it. |
| N12c `y0` outside the disk | accepted: "it is not `e0`, whose ends are roots" in Prop 3.9. |
| N12d Lemma 4 cited for `P0` | accepted: both now cite Lemma 3.7 (outdegree). |
| N7 product sign | accepted (above). |
| "the other group contributes 0" (A's `F = ∏ h_s(w_i)`) | moot: the paper uses B's `ω^m`. |
| N1 "both sides nonempty" in the simplicity proof | accepted (sentence in Lemma 2.1). |

### EDITS.md (E1 to E25)

E1 (honest differences, Li's half-rays = heights): accepted in the introduction and after Lemma 4.6. E2 (route as implications): accepted as "The plan". E3, E4 (job for spokes, `04-local`): moot, no spokes; Figure 3 is the local picture and says what `Q_s` is for. E5: see N4. E6, E7: two tasks and why the cube is not enough are in the plan and in Example 3.10. E8 (goal before the network; no re-proof of integrality): accepted. E9: accepted. E10: accepted. E11 (displayed counts match the figure): accepted; the proof displays `B+W = 2I+h−2`, `3(B−W) = 2ℓ−h`, `B = I+ℓ`, exactly the side panel of Figure 5. E12 (P uses the side through `s(t)`): accepted (Figure 3(a) caption and Lemma 3.6). E13: accepted (Table 1). E14: accepted. E15 (B, W overload): resolved differently: the incidence graph is `𝓑` (only in Section 5), so `B`, `W` are free for face counts. E16 (m, u, K overloads): resolved (component `H`, its edge count `q`; no index `u` in examples). E17: moot. E18 (every figure referenced): accepted. E19 (Figure 1 panel pointers): accepted. E20: moot (no `a_j`). E21 (role swap of r and s): resolved by naming the example's states `α`, `β`; `r`, `s` keep their roles everywhere, and the figures were relabelled. E22 (unslop): applied. E23 (pinpoint): accepted, Theorem 1.1 and Corollary 7.1. E24 (no internal paths, Kelmans): accepted, see edit 20. E25 (why no separating triangle): accepted in the closing remarks, cited as a claim of the unsigned manuscript, with the 9-vertex example recomputed.

### EXPOSITION-REVIEW.md

Its structural fails (rules 2, 4, 14) are fixed by taking B's order, dropping spokes, and the notation table. Its missing figure (`04-local` panel (a)) is my Figure 3, drawn without OpenAI's weights.

## 6. Other decisions

- **Figures.** Regenerated with stale notation removed: `10-cancellation` (panel labels `ε = −1`, `+1` instead of phases), `11-spokes` (no `Z(x)`), `16-at-a-glance` (no phases or spoke circulations), `01-cube` (panel (e)), captions of `07`, `09`, `12`. New: `17-heights`. Vertex labels with a white backing in all running-example panels. `check.py` still passes (it runs first in `build.py`); filenames unchanged; `audit.py` inventories 17 PDFs. Not used in the paper: `02` (the cube panel shows the same point), `04` (spokes in (b)), `05`, `11`, `12` (spokes), `15`, `16` (Figure 1 is the overview).
- **Example state names.** `α` (cyclic `Q`) and `β` (good) replace the figures' `s`, `r`, so that `s` always means "the second state".
- **Bibliography.** `papers/barnette.bib` and `MISMATCHES.md` did not exist when I wrote the references, so `paper/main/refs.bib` merges the two drafts' files plus five entries from `research/2026-11-14_opus_history-literature/bibliography.bib` (Holton-McKay, Akiyama-Nishizeki-Saito, Georges, Kardoš unused, BGM). Barnette 1969 keeps B's form with the note that Grünbaum recorded it. Nobody in the project has seen that page.
- **Closing remarks.** Which cycles arise (proved, with a new two-line proof that a cycle arises iff its state is good); each hypothesis (literature plus recomputed examples: the 11-vertex bipyramid incidence graph is checked planar, bipartite 5/6, 3-connected); the polynomial `F(w)` and its class expansion (proved, follows from Lemmas 4.2, 4.4, 4.5); no polynomial-time construction (open); consequences and one open question (H+− for two arbitrary edges). I dropped the rarity family `(2/3)^q` and the exact pair criterion's proof for length; the criterion is quoted from the unsigned manuscript and the project's proof is not cited, per the no-internal-citations rule.
- **Not adopted:** the polynomial `w = 1 + ξκ` as the main proof (kept as a remark; `ω^m` with a finite difference is shorter to state for this audience); Hall instead of max-flow (taste; RB and RA both keep max-flow).
