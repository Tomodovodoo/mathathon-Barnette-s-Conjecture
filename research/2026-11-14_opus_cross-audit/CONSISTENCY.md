# Consistency of names, symbols and numbers across the project

Documents compared (abbreviations used in the tables):

- **main**: paper/main/barnette.tex as of today (read-only; a revision is in progress). **v1**: paper/main/history/barnette-v1.tex. v1 and main agree on every item below unless a cell says otherwise.
- **inv**: proofs/involutions/involutions.tex and INVOLUTIONS.md (read-only).
- **steps**: digestions/steps/00 to 09 and GLOSSARY.md. **HOW**: digestions/route-map/HOW-IT-WORKS.md.
- **pri**: proofs/primal/PRIMAL-PROOF.md and DICTIONARY.md.

Method. scripts/terms.py counts each term in each document and prints the first defining context (output data/terms.txt). I then read the defining sentences. scripts/recount.py recomputes the example numbers (data/recount.json). I did not read every page of main and steps; the term counts are exact, the "meaning" cells come from the definitions I read.

## 1. Objects and symbols

"=" means the same name and meaning as main. **Bold** cells are conflicts, explained in Section 2.

| Object | main | inv | steps / GLOSSARY | HOW | pri |
| --- | --- | --- | --- | --- | --- |
| The graph; its dual | G (cubic), T coloured triangulation | = | = | = | G is the object; T only in the dictionary |
| Black objects | black faces of T; t0 outer; A the others | = | = | = | **black vertices of G; b0 root; A the others; B = all black vertices** |
| Non-root corners | X | = | = | = | X = non-root faces of G |
| n | n = abs(A) = k - 1 | = | = (GLOSSARY: n = k - 1 = N/2 - 1) | = | n = abs(A); abs(B) = n + 1; k not used globally |
| k | number of black faces ("2k faces of T") | not used | **number of black faces, and k(s) = number of cycles of Q_s** | k - 1 once | **local count in Lemma 4 (new faces of K)** |
| State | state, s : A -> X | = | = (T: perfect matching of B; Li: perfect matching of H) | = | = |
| Pair | ordered pair (r, s), r a partner, s the second state | pair p = (r, s) | = (Li: ordered 2-factor (M1, M2)) | = | = |
| Partner | partner | partner | partner; T: disjoint mate | partner | partner |
| Q_s | Q_s, sides opposite s(t) | = | = | = | Q_s as face links (edge of G not on s(b)) |
| The good condition on s | **good state** (Q_s a forest, one root per component) | **forest pair** (for the pair) | **tree matching** (state), **forest pair** (pair); T: tree pair | tree matching | **"circuit-free Q_s with a partner", "forest state"** |
| D(r, s) | D(r, s), edges r(t) -> s(t) | cover of p | D(r, s); T: D_{r,s}; Li orients the other way | D | D, "selected collection" |
| Undirected D | "group" / cycles of D | **cover**, unoriented-cover class | **cover, cycle cover, 2-factor (for Li)** | cover | "the undirected collection D", group |
| Number of cycles of D; least one | c, c^+ (counterclockwise); m | c(p), m = min c(p) | **c(D), c_min, m** | **c_min** | c(D), c_+, c_-, m |
| delta | delta(v, w) = 1 if black face left of v -> w | = | = | not used | delta(f, g) = 1 if black vertex left of f -> g. Same sign under duality. |
| Positive / ccw circuit | ccw has delta-sum -3 | ccw sum -3, cw sum +3 | = | = | sigma = +1 "positive" has sum -3; equals ccw |
| Sign | eps = prod delta = (-1)^((n+c)/2) (-1)^(c^+) | eps; J = cw - ccw; J = c = n mod 2 | eps = (-1)^((n+J)/2) | not used | eps = (-1)^((n+3c)/2)(-1)^(c_-) |
| J | J = (1/3) sum delta (only in a remark) | = | = | not used | t = sum delta = 3J (pri writes t) |
| Phase | i^J = i^(-n) eps | "standard phase normalization" | i^J = i^(-n) eps; cites the old dispute | not used | eps = i^n * (Lean phase) |
| Heights | eta_s(y) = sum of turn signs kappa_y(t, s(t)) along a face path from white y to t0; weight omega(s) = sum_y eta_s(y) | **H(s) = - sum_w eta_s(w) = - omega(s)**; rays give the same increments up to a constant per cover class | **h_s(w)**: signed crossings from an inner white face to t0 with the spokes of s | heights via unit flow from every white face | no heights; integer potentials a(b, f) from one path flow |
| Weight increment of a cycle | L(C) = number of white faces inside | = | L^+(C) - L^-(C) | = | lambda_C = abs(W cap S_C) |
| Roots | R, corners of t0 | = | = | = | R, the three faces at b0 |
| Selected edges P | **selection, chosen sides** (P a selection containing e0) | not central | **selected edges, P** | P | **P = "the selected matching"; but "selected" also names D in Lemma 8** |
| White-face tree | W_s once, as background | not used | white-face tree, W_s | once | "a different auxiliary tree" |
| Recovery tree | Y_s, a tree on the 2k faces of T | not used | incidence tree H - s | H - s | K, a spanning tree of G |
| Black-inner separating triangle | separating triangle (the colour fact appears inside a proof) | not used | **black inner boundary** (12 uses) | not used | "root-free three-edge cut whose inner ends are black" |
| Spoke graph and incidence graph | H used twice | spokes | **H = spoke graph (O, T); Li's H = our B; B = incidence graph** | spokes | **B = black vertex class**; incidence relation unnamed |
| Disk counts | h, l, B, W | = | h, l, I, B, W | B + 1 | h, l, abs(B cap S), abs(W cap S) |

## 2. Conflicts

**C1. One condition, five names.** A state s with Q_s a forest whose components each contain one root: main says *good state*, steps and HOW say *tree matching*, inv says *forest pair* (of the pair), steps also say *forest pair* and T's *tree pair*, pri says *circuit-free Q_s with a partner* or *forest state*. These are equivalent only through Remark 14 of pri: for a forest Q_s, "has a partner" is the same as "one root per component". A reader moving from main to the digestions meets two names for one object. main's own choice ("good") is the easiest to read.

**C2. Same letter, different things: k.** main and GLOSSARY: number of black faces. GLOSSARY also: k(s), number of cycles of Q_s (from T's Proposition 2.1). pri Lemma 4: number of faces of K not in Y. Only the last is local and harmless; k(s) collides with k.

**C3. Same letter, different things: B and H.** GLOSSARY: B is the incidence graph between A and X, and also the number of black faces inside a disk. pri: B is the set of black vertices of G. Li's H is our B, while O and T use H for the spoke graph (GLOSSARY flags this). pri's dictionary lists Li's state as "perfect matching of H" and T's as "perfect matching of B" without that warning.

**C4. Opposite height normalisation.** main: omega(s) = sum over white faces of eta_s(y), increasing by L(C) when a cycle is turned from clockwise to counterclockwise. inv: H(s) = -omega(s). GLOSSARY: h_s(w) counts crossings with spokes, summed over inner white faces only; outer white faces contribute zero in main's definition too, so that part is a difference of wording, but the sign of inv's H is opposite to main's omega. inv also says ray heights agree with turn heights only up to an additive constant on each cover class. Nothing is wrong: the lowest coefficient is computed from differences. But three documents use three symbols (eta and omega, H, h_s) for two quantities of opposite sign.

**C5. "Selected" means two things in pri.** In Lemma 8 the edges r(b) -> s(b) are "selected" (the collection D); in Lemma 10 and Section 7, and everywhere in steps, the "selected edges" are the perfect matching P. main avoids the clash by saying *selection* for P.

**C6. c_min versus m.** main, inv, pri: m. steps and HOW: c_min (GLOSSARY lists both). Harmless, but one symbol should be chosen.

**C7. The undirected D.** main: "group" (following O). inv, steps, HOW: "cover" or "cycle cover". steps also say "2-factor" in the Li translation, where a 2-factor is of the incidence graph, while a "2-factor" of G is a spanning cycle cover of G. The brief's question "cover / 2-factor / cycle cover" is this.

**C8. Stale pointer on the phase dispute.** steps (00-overview.md) says the primal revision "disputes the referee's circuit-dependent phase normalization ... recorded in research/2026-11-14_astra_primal-revision/REPORT.md". The dispute is now settled (ADJUDICATION.md): the ratio is i^n. main's "i^J = i^(-n) eps" and pri's "eps = i^n times Lean's phase" are the same statement, with Lean's phase equal to O's i^J when corner orders agree.

**C9. Wrong explanation of 279 versus 213.** HOW-IT-WORKS.md line 141: "the older digestion audit counted 213 with a different fixture or convention". The referee (research/2026-11-14_opus_referee-involutions/DISCREPANCY-279-213.md) showed both counts come from the same running.json and the same Tutte-layout recipe, with roots 4 and 5 sent to different anchor points. INVOLUTIONS.md already says this correctly ("roots 4 and 5 interchanged"). The count of marked objects depends on the drawing (69 drawings give 35 values from 103 to 363); the signed sum and the nine second-fixed objects do not.

**C10. Two "running examples" in pri.** STATUS.md "Exact finite range" and EXAMPLES.md describe the first version's 20-vertex worked example ("nine states and ten ordered pairs", polynomial 4z + 9z^2 - ...). The PDF's running example is the 22-vertex graph of running.json. Both are labelled, but a reader can confuse them; no other document uses the 20-vertex example.

No conflict found in: the definition of delta (all documents put the black face on the left), the sign formula (main's (-1)^((n+c)/2)(-1)^(c^+), GLOSSARY's (-1)^((n+J)/2) and pri's (-1)^((n+3c)/2)(-1)^(c_-) are equal since J = c - 2c^+ and c_+ = c^+), the orientation that raises the weight (counterclockwise in main, sigma = +1 in pri), n = k - 1, t0 and e0 of the running example (t0 = {0, 4, 5}, e0 = 04; pri's figures show root faces f0, f4, f5 and e0 between f0 and f4).

## 3. Numbers recomputed

COMPUTED, scripts/recount.py (my own enumeration; imports only my phase_ratio.py), output data/recount.json.

| Claim | Where stated | Recomputed |
| --- | --- | --- |
| Running example: 12 states, 8 pairs, 7 states with a partner, 6 tree matchings, one state with two partners and a cycle in Q | steps 03, 05 | 12 states, 8 ordered pairs, 7 with a partner, 6 tree matchings, 1 cancelling state. Agrees. 11 states have Q_s a forest. |
| Running example: two covers, each with two cycles, m = 2 | steps 06, inv | 2 covers, circuit counts (2, 2), m = 2. Agrees. |
| Lowest coefficient nine | inv ("lowest coefficient nine", nine second-fixed objects) | sum over covers with m circuits of prod abs(W cap S_C) = 9. Agrees. |
| 28 Hamiltonian cycles, 6 avoid the dual of e0 = 04 | steps 07 | 28 and 6. Agrees. |
| 279 versus 213 marked objects | inv 279; HOW and the digestion audit 213 | Not recomputed by me: Li's marked objects depend on a drawing that I did not reimplement in the time. The involutions referee recomputed both with independent code from the same file (C9). The drawing-independent invariants that both runs share, the signed sum 9 and the second-fixed count 9, I confirm through the lowest coefficient above. |
| Hexagonal prism, t0 = (6,0,1): 3 states, 2 good (tree matchings), 4 Hamiltonian cycles avoid e0 on the equator | main, v1, steps 07, HOW, INTEGRATION.md | 3 states, 2 tree matchings, all 3 with Q_s a forest. Avoiding cycles: 4 for e0 = 01 (equator side), 2 for 60, 2 for 61. Agrees with steps 07 ("two and two"). 8 Hamiltonian cycles in all. |
| Hexagonal prism, the other colour class black, t0 = (7,1,0) | not stated anywhere | Same: 3 states, 2 tree matchings, avoiding counts 4 (equator side 10), 2, 2. |
| Primal note's running example: 22 vertices, 13 faces | pri | n = 10, so 2(n + 1) = 22 vertices and n + 3 = 13 faces. Agrees. |

## 4. Proposed project-wide convention

Use main's vocabulary, which is the most readable, with these fixes:

1. **good state** for "Q_s a forest with one root per component", **good pair** for a pair whose second state is good. Mention once that T says tree matching / tree pair and that, for a forest Q_s, good is the same as "has a partner" (pri Remark 14).
2. **k** only for the number of black faces (n = k - 1). Rename T's k(s) to **q(s)**, the number of cycles of Q_s. pri's local k in Lemma 4 may stay; rename to **j** if a global k is ever used there.
3. **B** only for the black vertices of G (or black faces of T); call the incidence graph **I** (or "the incidence graph"), and keep **H** for the spoke graph. Write abs(B cap S), abs(W cap S) for disk counts rather than bare B, W.
4. **omega(s) = sum_y eta_s(y)** as the one height normalisation, increasing when a cycle turns counterclockwise. inv's H(s) becomes -omega(s) written out, or is renamed.
5. **selection P** for the perfect matching (main); never "selected" for D.
6. **cover** for the undirected D (with "group" noted once as O's word); keep "2-factor" only for spanning 2-regular subgraphs of G, and say "2-factor of the incidence graph" when translating Li.
7. **m** for the least number of cycles over all covers.
8. The phase relation, stated once: **eps = i^n i^(-J)**, equivalently i^J = i^(-n) eps, with J = (1/3) sum delta; Lean's phase is i^J when its corner order matches.

## 5. Exact edits each document would need

I applied the pri edits; the others are proposals only.

**paper/main/barnette.tex** (none required for correctness):
- Where "good" is defined (line 329), add: "In the digestions and in the constructive paper a good state is called a tree matching."
- Line 815 remark: optional "Lean's phase is the same i^J."

**proofs/involutions/involutions.tex and INVOLUTIONS.md:**
- Replace "forest pair" (2 uses each) by "good pair".
- Where H(s) = -sum_w eta_s(w) = -omega(s) is introduced: say explicitly that H has the opposite sign of main's weight, or define H(s) = omega(s) and flip the sign statements that use it.

**digestions/steps/** (GLOSSARY.md, 00 to 09):
- GLOSSARY: rename k(s) to q(s); add a row "good state = tree matching"; say that B is the incidence graph only inside the GLOSSARY's incidence table and not the disk count.
- 00-overview.md: replace the sentence on the phase dispute by "the revision showed the ratio is the constant i^n; research/2026-11-14_opus_cross-audit/ADJUDICATION.md".
- All files: "tree matching" -> "good state (tree matching)" at first use per file; c_min -> m.

**digestions/route-map/HOW-IT-WORKS.md:**
- Line 141: replace "while the older digestion audit counted 213 with a different fixture or convention" by "while the digestion audit counted 213 on the same file with roots 4 and 5 sent to the other anchor points; the count depends on the drawing, the signed sum and the nine fixed objects do not".
- c_min -> m.

**proofs/primal/** (applied in this run except where noted):
- PRIMAL-PROOF.md Lemma 8 and Section 6: "selected" for D is left as is in this run; proposal: replace "A pair selects at each black vertex the edge ..." by "A pair marks at each black vertex the edge ...", and "labels exactly one selected edge" by "labels exactly one marked edge". Not applied, because it touches the proof text that two audits refer to by phrase; recorded for the next revision.
- DICTIONARY.md: added a naming warning under the table (Li's H = the constructive paper's B = the incidence graph; H is the spoke graph in O and T). Applied in the Markdown; the PDF dictionary page is built from the table rows only, so it does not show the warning.
- STATUS.md "Exact finite range": added a first sentence saying it describes the first version's checker and 20-vertex example. Applied.
