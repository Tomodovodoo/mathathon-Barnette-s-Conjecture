# Referee report on version 2 of the involution note

Object: `proofs/involutions/involutions.pdf` as committed in d4cd3f1 (17 pages), its source and companions. This is the independent review of the new Section 5 (marks without a drawing) and the final check of the whole note. Status tags are those of `research/BRIEF.md`. Lemma numbers are the note's.

## Summary

1. The new face-path lemma (Lemma 7) is correct. Its statement was too loose to referee and two sentences of its proof described the sectors wrongly. Verdict CORRECT AFTER FIX, and the fix is applied.
2. Code written from the text alone reproduces every count printed in the note, in the note's own encoding, and all 279 rows of the worked example.
3. All 15 edits of the first referee are in place and correct. Nothing regressed in the text.
4. One figure was wrong. Figure 2 showed the reversal of an unmarked cycle under a caption that described a token move. It is replaced by a real token move.
5. Final verdict FOLLOWS, for Theorem 1 by the ray route and by the face-path route.

## 1. The face-path section, line by line

### Definition of a mark

A white face `w` has a tree path `w = f_0, ..., f_j = t_0`. At a black face `f_i` strictly between the ends the path turns around the common corner `v` of the entering and leaving sides, `kappa_w(i) = +1` if `v` is on the left. A token for `s` is `(w, i)` with `s(f_i) = v`, and `d = (1 + kappa)/2`.

Checked. PROVED-HERE (below) and COMPUTED.

- Faces alternate in colour along a dual path, so `f_1` is black and the path is well formed. The root of the tree is `t_0`, so `t_0` occurs only at the end. The note did not say this, and the phrase "each bounded black face" leaned on a drawing in a section that claims to use none. Fixed in the text.
- The direction bit matches Definition 3. If `v` is on the left of the step, the incidence from the centre to `v` points to the left of the path, so it crosses from right to left, which is `d = 1` in Definition 3. So `d = (1 + kappa)/2`, and the signed crossing with left to right positive is `-kappa`. The note states both. COMPUTED against coordinates: 5064 turns in exact Tutte drawings, the corner cut off lies on the left of the chord between the two side midpoints exactly when my combinatorial `kappa` is `+1`.
- The convention is the main paper's. Its rule "`v` is on the left exactly when `v, a', b'` is counterclockwise" is what `fp.py` implements. With breadth-first paths my code returns the eight pairs `(eps, omega)` of the main paper's Table 2 exactly.
- "Inside", "counterclockwise" and "clockwise" had no drawing-free meaning in the section. They need one: inside is the side of a cycle away from `t_0`, counterclockwise means inside on the left. Added.

### Lemma 7. Verdict: CORRECT AFTER FIX

The old statement was "These lists have the same parity, alternation, and first-exit sign rules as the ray lists. With these lists and direction bits, both involutions, the fixed-set formula, and the alternating constructor hold unchanged." A reader cannot check "the same rules" without reconstructing them. The statement is now three claims and a consequence:

1. the list of `C` at `w` has odd length exactly when `w` is inside `C`;
2. at consecutive entries `C` crosses the path in opposite directions;
3. if `w` is inside, at the first entry `C` crosses the path from right to left when `C` is counterclockwise and from left to right when clockwise;

and then Lemmas 4, 5, 6, 8 and the proof of Theorem 1 hold for path tokens with the same `F`.

The proof is right in substance. I rederived it as follows, and this is what the corrected text says.

- Cut each triangle of `A` by its three centre-to-corner incidences. This gives three sectors, one on each side. The note called them "corner sectors", which they are not. The sectors on two sides share the incidence at the common corner. A step entering by one side and leaving by another passes from one sector to the next and crosses exactly that incidence, once. So a step is a token position for exactly one corner, and the refined path is a path in the dual of the subdivided map.
- The incidence cycle `C` (corners `r(t), s(t)` and centres `t`) is simple. By the combinatorial Jordan property of the sphere map, the refined path changes sides exactly when it crosses an incidence of `C`. In a triangle on `C` those are the incidences at `r(t)` and `s(t)`. The note said the route `r(t), t, s(t)` "separates precisely the corner sectors at `r(t)` and `s(t)` from each other". It does not. It separates the sector on the side `r(t)s(t)` from the other two. The conclusion drawn (turns around `r(t)` or `s(t)` cross once, the turn around `u(t)` does not) is correct. Rewritten.
- The proof never said why "inside `C`" for the incidence cycle agrees with "inside" for the side cycle of `D_p`, which is where `a(C)` is counted. The two cycles differ by the sectors on the sides `r(t)s(t)`, which contain no white face. In the ray version this is the winding-number paragraph of Section 2, which uses a drawing. One sentence added.
- Parity and alternation follow, since the path ends in `t_0` outside. For claim 3, a counterclockwise cycle has its inside on the left, and a path leaving the inside crosses it from its left to its right, which is the cycle crossing the path from right to left.

COMPUTED. Claims 1 to 3 are asserted for every pair, every cycle and every white face in every mode: 77952 lists per path family on the 880 paired roots through 14 vertices (`census.py`, function `lemma7`). No failure.

### Both involutions "go through verbatim"

Verdict: CORRECT. I checked each rule of Section 4 against what the path model preserves.

| Rule | Data it reads | Preserved by the move | Why |
| --- | --- | --- | --- |
| first cycle of `Q_s` | `s` | yes | the first map keeps `s`. COMPUTED: the cycles of `Q_s` found from `s` alone (2-core) equal those found through `r`, at every object |
| token eligibility after the first map | `s(f_i) = v` | yes | `s` is kept |
| first unmarked cycle | unoriented cover, token faces | yes | reversal keeps the cover; tokens sit on other cycles, where `s` is unchanged |
| one token per cycle | `c >= m`, exactly `m` tokens | n/a | a token `(w, i)` lies on the cycle through `f_i`; counting as before |
| first cycle with `w_C` outside | unoriented `C`, the white face of its token | yes | the moved token keeps its white face and its cycle |
| first cycle with a nonfirst token | the list of `C` at `w_C`, and the index | yes | the list is defined by "turns around `r(t)` or `s(t)`", symmetric in `r, s`; the pairing never touches index 1 |
| partner | consecutive list entries | yes | pairing is an involution on indices |
| reverse or not | whether the partner corner is `s(t)` or `r(t)` | returns | as in Lemma 5 |
| no collision | `(w, i)` determines `f_i`; distinct cycles use distinct faces | n/a | |

Sign reversal. Without reversal both entries are `s`-incidences, crossed away from the centre, and by claim 2 in opposite directions, so `d` flips and `J` stays. With reversal the partner is an `r`-incidence. It is traversed towards its centre in the direction opposite to the old token's traversal, so directed away from its centre it crosses the path the same way as the old token did. After the reversal it is an `s`-incidence with that same `d`, and `J` has changed by 2. Either way the sign flips.

COMPUTED on every object of five path families (`bfs+` 16586, `bfs-` 17882, `dfs` 717994, random tree 49436, non-tree paths 139262 objects): membership of both images, both involution identities, the same branch on the return move, sign reversal off the fixed sets, fixed set of the first map equal to forest pairs. Two cycle orders were used, lexicographic and random. All three branches of the second map occur in every family (for `bfs+`: 10468 unmarked reversals, 1032 moves, 428 moves with reversal).

### Fixed set, its sign, the count

Verdict: CORRECT. For each minimum cover choose an inside white face per cycle. Its list is odd, so it has a first entry, and exactly one orientation of the cycle makes that entry an `s`-incidence. By claim 3 a counterclockwise cycle contributes `d = 1`, so with `q` such cycles the exponent is `floor((m - 2q)/2) + q = floor(m/2)`.

COMPUTED. `F` is computed independently of any marks, as the sum over minimum unoriented covers of the product of the numbers of white faces inside each cycle (flood fill of the dual). In every mode on every paired root: the number of second-fixed objects equals `F`, each has the stated form and sign, and the signed size of `Omega` is `(-1)^floor(m/2) F`. The total of `F` over the 880 roots is 4658. Rays in two directions through 12 vertices give the same `m`, `F` and signed sum as the path families (742 on 208 roots).

### Agreement with the main paper's Section 4

Verdict: CORRECT, with one clarification added.

- `H(s) = -omega(s)` for path tokens. COMPUTED together with Lemma 4.6 of the main paper: reversing a clockwise cycle raises `eta_s(y)` by 1 if `y` is inside and by 0 otherwise, asserted for every pair, cycle and white face.
- The coefficient. `sum_p eps(p) H(s)^j = 0` for `j < m` and `= m! (-1)^((n+m)/2) F` for `j = m`, and `sum_p eps(p) omega(s)^m = (-1)^((n-m)/2) m! F`, which is the displayed value of Proposition 4.8 after Lemma 4.7. Asserted on all 880 roots in all path modes; the `H` form also for rays. `eps = prod delta = (-1)^((n+J)/2)` is asserted as well.
- Clarification. The identity `H = -omega` is for the same paths and the same orientation of the sphere. The note's layout of the running example shows the stored triples of `running.json` clockwise, and the main paper draws them counterclockwise (COMPUTED: in the stored orientation the pair `(beta, alpha)` has a counterclockwise 7-cycle and a clockwise triangle, as the caption of the main paper's figure of that pair says; in the note's layout it is the reverse). So Figure 3's `kappa = +1` at corner 6 of face `{0,1,6}` is `-1` in the main paper's height figure for the same turn. Nothing is wrong, since the sign of an object does not change under a mirror image when `n = m` mod 2, but a reader comparing the two figures would see a contradiction. Section 9 and the caption of Figure 3 now say it.

### Dependence on the tree

Verdict: CORRECT, and slightly understated. The object count, the first-fixed count, the walk lengths and the identities of the fixed objects depend on the paths; `m`, `F`, the fixed sign and the signed sum do not. COMPUTED on the running example: 31, 49, 161, 33, 85 objects for the five families, always nine second-fixed and signed sum -9. Over the census the families have between 16586 and 717994 objects.

The tree is not needed. The proof uses only that each path is simple and ends at `t_0`. COMPUTED with independent loop-erased random walks for each white face, which form no tree: all checks pass, 139262 objects, walks of up to six moves. The note now says so. This also matches the main paper, which fixes a path per white face and no tree.

Two measured facts that the note does not claim and should not: walks reach six moves with non-tree paths (four with the two breadth-first trees, two with the depth-first and the random tree), and the number of roots where the count with `m + 1` marks vanishes varies from 36 to 150 across families.

## 2. Verdict per lemma

| Item | Verdict | Basis |
| --- | --- | --- |
| Theorem 1 | CORRECT | Lemmas 2, 4, 5, 6 |
| Lemma 2, disk identity | CORRECT | reread; COMPUTED on 6832 cycles of 3280 pairs: odd, delta-sum -3 or +3 by orientation, a white face inside |
| Definition 3, sign | CORRECT | `J = cw - ccw` and `J = c = n` mod 2 asserted on all pairs |
| Lemma 4, first map | CORRECT | the local identity `delta(u,s) - delta(r,s) = 2 delta(r,u)` asserted in every face of every pair |
| Lemma 5, second map | CORRECT | all objects, ray and path |
| Lemma 6, fixed set | CORRECT | count equals `F` computed without marks |
| Lemma 7, face paths | CORRECT AFTER FIX | statement made exact; sector wording corrected; one bridge sentence added |
| Lemma 8, constructor | CORRECT | every second-fixed start walked to a forest pair without repetition, in every mode |
| Section 8 identity | CORRECT | `(n+m)/2`, all 880 roots |

No GAP and no WRONG.

## 3. The 15 edits of the first referee

| Edit | Applied | Checked here |
| --- | --- | --- |
| E1, sign `(-1)^((n+m)/2)` | yes | asserted on all 880 paired roots, 718 of them with `m` odd, in every mode |
| E2, 55 classes | yes, in all three files | 1+0+1+1+2+2+8+8+32 = 55 from plantri and from the canonical census |
| E3, relation to the height proof | yes | consistent with `paper/main/barnette.tex` Section 4; numbering 4.6, 4.7, 4.8 confirmed in `barnette.aux` |
| E4, what Li leaves unwritten | yes | read against Li's Definition 14, Definitions 20 to 23, Section 4.3 and Appendix B. Accurate. One refinement: the set convention is in Definition 14, Appendix B writes the tuple. Text adjusted |
| E5, the `m = 2` and `m = 3` sentence | yes | Li's Definition 23 does write `(M_2, M_1)` in the one-cycle case |
| E6, walk lengths depend on the drawing | yes | in the note's drawings 4617 starts take 0 moves and 41 take 2 |
| E7, 279 and 213 | yes | 279 reproduced; the 213 and the 69 drawings are the first referee's, not rerun here |
| E8, `Omega` depends on the drawing | yes | two ray directions give 16662 and 25060 objects through 12 vertices |
| E9 to E13, wording of proofs | yes | reread; each is as proposed, E10 with an added sentence on connectedness |
| E14, rays and zoom in Figures 1 and 2 | yes | but see Section 4 below |
| E15, Markdown companions | yes | counts and the mirror-image explanation agree with the TeX |

Regression check. Every displayed sign in Sections 2 to 5 and 8 is asserted by `census.py` or `extra.py`. The numbers of Section 7 (40 and 4, 1200 and 28, 826 and 8 and separator-free, the interior nonfirst branch at `m = 2` on the 11-vertex class 1 root 0) are reproduced by `canonical.py` and `extra.py`. The numbers of Section 8 (55, 1206, 880, 221050, 4658, 17832, 18362, walks, 78) are reproduced by `canonical.py`. The 57 belongs to the first referee's drawings and is taken from that report. Section 9: 12 states, 8 pairs, `m = 2`, 279 objects, nine second-fixed, all negative, all first-fixed, signed sum -9, coefficient 9, and every row of the table (object, sign, both images) agree with `running.py`. Not rechecked: the hard-family paragraph (tubes, stacks, subdivided octahedron) and the comparison with the lab's integer polynomial, both unchanged since version 1 and covered by the first referee. Li's orientation dictionary (`cw' = -J`) was also checked only by the first referee and the reviser.

## 4. Figures

| Figure | Before | Now |
| --- | --- | --- |
| 1 | rays and zoom present; labels `t_0`, `t_7` sat on the thick spokes; crossings unmarked; caption did not say which object | labels moved off the spokes, the two marked crossings dotted, caption names object 1 and says the triangle is unmarked |
| 2 | WRONG caption. The object drawn (object 1, tokens 5:0 and 6:7) has both tokens on the 7-cycle, so the second map reverses the unmarked triangle and no token moves. The caption said "The token moves to its partner crossing" | replaced. Object 2 (tokens 5:0, 16:11) and its image, object 6 (5:7, 16:11). The token moves along the ray of `w_5` from the spoke of `t_0` to the spoke of `t_7`; the list has exactly these two entries; no reversal; sign - to + |
| 3 | correct data (paths, corners and signs reproduced), schematic only | caption now warns that the signs are those of the mirror image of the main paper's drawing. Still a schematic of two paths, not a picture on the triangulation |
| 4 | labels `t_0` and `w_3` overlapped | `t_0` moved left, `w_3` moved off with a leader; caption says what changes |

All four floats are `[p]` floats after the last paragraph of Section 9, so none interrupts a statement or a proof. Labels are `\footnotesize`. The left panel of Figure 1 is too small to read anything but the position of the zoom, and the caption now uses it only for that.

## 5. Reverse-Lamport audit of the face-path route

### Audit boundary

Conclusion C0: for every finite simple sphere triangulation with a proper black and white face colouring and an outer black face `t_0`, if a pair of states exists then a pair exists with `Q_s` a forest. Source: `involutions.tex` after this pass, Sections 1 to 5. Accepted primitives: finite signed counting, Euler's formula for a triangulated disk, and the Jordan property of a simple cycle in a sphere map (a dual path changes sides exactly when it crosses an edge of the cycle). Pair existence is a hypothesis. Computation supports the audit and discharges nothing.

### Obligation graph

```text
C0 <- R0 (AND: H, M, A, B, F, N)
A  <- R1 (AND: A1, A2, A3)
B  <- R2 (AND: L, B1, B2, B3, B4)
L  <- R3 (AND: L1, L2, L3, L4, D)
F  <- R4 (AND: L, D, F1, F2)
N  <- R5 (AND: A, B, F)
C0 <- R0' (supplied alternative, ray route: same graph with L replaced by Lray, which adds G1 and G2)
```

### Critical findings

None failing. L2 and L4 were stated wrongly or not at all in version 2 and are discharged by the corrected text. The first sentence of the old Lemma 7 was a statement by analogy; it is replaced by L's three claims.

### Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | forest pair exists under H | root | R0 | root | H, M, A, B, F, N | discharged |
| H | `T` as stated and a pair exists | C0 | R0 | hypothesis | theorem statement | discharged |
| M | `m = min c(p)` exists and `m >= 1` | C0, B, F | R0 | algebraic/logical step | finitely many pairs, each cover nonempty | discharged |
| D | disk identity: cycles of chosen sides are odd, enclose a white face, delta-sum -3 or +3 | L, F, A3 | R3, R4 | proved earlier | Lemma 2 | discharged |
| A | first map is an involution, fixes exactly forest pairs, reverses sign elsewhere | C0, N | R1 | major claim | A1, A2, A3 | discharged |
| A1 | the cycle of `Q_s` is chosen from `s` alone | A | R1 | definition | Section 3 | discharged |
| A2 | reversal keeps `r` a bijection disjoint from `s`, and keeps every token | A | R1 | algebraic/logical step | Lemma 4; token eligibility reads `s` only | discharged |
| A3 | `J` changes by 2, token bits unchanged | A | R1 | algebraic/logical step | local delta identity and D | discharged |
| L | claims 1 to 3 of Lemma 7 | B, F | R3 | major claim | L1 to L4, D | discharged |
| L1 | a tree path is simple and meets `t_0` only at its end | L | R3 | definition | tree rooted at `t_0` | discharged |
| L2 | a step crosses exactly the incidence at its turned corner, with signed crossing `-kappa` | L | R3 | algebraic/logical step | three sectors, one per side | discharged |
| L3 | the refined path changes sides of `C` exactly at the listed steps; it ends outside | L | R3 | named theorem | Jordan property for the simple incidence cycle; premises: `C` simple, path in the dual of the subdivided map | discharged |
| L4 | the incidence cycle and the side cycle have the same white faces inside and the same orientation | L, F | R3 | side condition | they differ by sectors on the sides `r(t)s(t)` | discharged |
| B | second map is an involution with the stated fixed set, reversing sign elsewhere | C0, N | R2 | major claim | L, B1 to B4 | discharged |
| B1 | all cycles marked implies `m` cycles, one token each | B | R2 | algebraic/logical step | `c >= m`, `m` tokens | discharged |
| B2 | the partner exists, becomes eligible, collides with no token | B | R2 | side condition | L claim 1 for index ranges; reversal swaps `r, s` on one cycle; distinct cycles have distinct faces | discharged |
| B3 | the same cycle and the same branch are chosen on the return move | B | R2 | algebraic/logical step | choice reads the unoriented cover, the white face and first or nonfirst status | discharged |
| B4 | the sign flips in both branches | B | R2 | algebraic/logical step | L claim 2 and the away-from-centre convention | discharged |
| F | the second-fixed set has `F > 0` members, all of sign `(-1)^floor(m/2)` | C0, N | R4 | major claim | L, D, F1, F2 | discharged |
| F1 | per cycle and inside white face, exactly one orientation makes the first entry an `s`-incidence; choices are independent | F | R4 | algebraic/logical step | reversal on one cycle | discharged |
| F2 | direction sum `q`, `J = m - 2q` | F | R4 | algebraic/logical step | L claim 3 | discharged |
| N | the signed size of `Omega` is nonzero, so the first map has a fixed object | C0 | R5 | algebraic/logical step | A, B, F | discharged |
| G1 | ray route: a generic straight-line drawing exists | Lray | R0' | named theorem | Fary's theorem for simple plane graphs, plus a small rotation | discharged |
| G2 | ray route: entry and exit alternate along a ray, and the two-spoke route has the winding numbers of the side cycle | Lray | R0' | named theorem | Jordan curve theorem for polygons; Section 2 | discharged |

### Verdict

FOLLOWS. The face-path route R0 closes through L1, L2, L3, L4 and D, with B1 to B4 and F1, F2 checked against the corrected text; the ray route R0' closes as the first referee found. No obligation on either route is missing, circular or too strong. The coefficient comparison of Section 8 is off both routes.

## 6. Statement for the synthesis

`proofs/involutions/involutions.pdf` proves the forest-pair lemma (OpenAI Proposition 5.1, the cancellation half of Li's Key Lemma 7): if a rooted Eulerian triangulation has a pair of states, it has a pair whose `Q_s` is a forest, with no hypothesis on separating triangles. The proof is Li's two sign-reversing involutions on pairs carrying `m` marks, written out for every minimum cycle count `m`, in two forms: marks as ray crossings in a drawing (Li's form) and marks as turns of fixed face paths around selected corners (no drawing; the tree of paths is a convenience). It also proves that the alternating walk from a second-fixed object ends at a forest pair, and identifies the signed count as `(-1)^floor(m/2) F`, where `F` sums, over minimum unoriented covers, the product of the numbers of white faces enclosed, which is `(-1)^((n-m)/2)` times the coefficient of the main paper's Proposition 4.8 divided by `m!`. It imports Euler's formula for a disk, the Jordan property of a simple cycle in a sphere map, the existence of a straight-line drawing (ray form only), and the existence of a pair as a hypothesis; it does not prove pair existence, a walk bound, or anything about more than `m` marks. Checked by: the author's self-audit; an independent referee (Opus) for version 1, verdict FOLLOWS with 15 edits, all applied; this second independent referee (Fable) for the face-path section and the final text, verdict FOLLOWS after a fix to the wording of Lemma 7. COMPUTED by three independent code bases on all 1206 rooted instances through 14 triangulation vertices (880 with a pair; `m = 1, 2, 3` on 560, 162, 158), with rays in several drawings and face paths in five families. No human has read it.
