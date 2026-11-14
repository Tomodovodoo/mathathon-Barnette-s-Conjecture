# Referee report on proofs/involutions/ (two involutions for the forest-pair lemma)

Referee: Claude Opus 5.5, 14 November 2026. Independent of the author (a different model). I read the PDF first, then the TeX, the companion INVOLUTIONS.md, STATUS.md, the author's REPORT.md and AUDIT.md. I wrote my own verifier from the PDF text (`code/ref.py`, `code/check.py`) and did not reuse the author's code. I used `workings/barnette_lab/` only to read the face order its Li replay uses (for the 213 count), and `plantri.exe` only to generate inputs.

Tags follow research/BRIEF.md. A verdict of CORRECT below means: I checked every step myself and found it valid (PROVED-HERE by the author, checked here). It is not a human review.

## 0. Phase 1: the PDF read cold, and where I got lost

I read all 15 rendered pages before opening anything else. The proof itself (Sections 1 to 5, pages 1 to 4) reads in about twenty minutes and I could follow every lemma. The places where I stopped:

1. Page 1, the paragraph "In Li's incidence language ...". Six sentences translate Li's cycle-breaking condition into "Q_s is a forest". I had to reconstruct that "after deleting the second matching" means deleting the s-edges of the incidence graph, so each centre keeps its two other corners and subdivides the side opposite s(t). Correct, but too compressed for a first page.
2. Page 2, the spoke-cycle paragraph ("Sliding successively across these subdisks ..."). The claim is right. The sliding argument is informal, and I checked it by a winding-number argument instead (EDITS E9).
3. Definition 3 defines d(w,t) by the direction of the spoke t → s(t). Lemma 5 then speaks of the directions of crossings with r-spokes. I had to work out that the spoke cycle is traversed r(t) → t → s(t), so an r-spoke is traversed toward the centre, and that after a reversal it becomes an s-spoke traversed away from the centre. The note never says this.
4. Lemma 6, "first exits". I checked by hand that the first crossing from an inside point is an exit and that a counterclockwise cycle is crossed right to left there. Correct.
5. Section 7, "The height-product proof in the project fixes an indexed list of white faces". I could not find what this refers to. paper/main sums heights over all white faces.
6. Section 7, the displayed identity. I tried n = 3, m = 1 by hand and the two ends of the display had opposite signs. Computation confirms a sign slip (finding F1).
7. Figures 1 and 2. I could not read them. The whole interior of the drawing occupies about a tenth of the disk, the labels t7, w6, t0 overlap, and the rays, which carry the tokens, are not drawn at all. The caption says the rays "are encoded by the stored exact layout", so a reader cannot see a single crossing.
8. Section 8 says "roots 0,4,5" and "root positions ... in stored face order". The stored order is 0, 5, 4. I needed the JSON to know which root goes where. This matters, because swapping 4 and 5 changes 279 into 213 (DISCREPANCY-279-213.md).
9. The tables (pages 8 to 14) are complete. I used them as a machine check (all 279 rows agree with my code), but as reading matter 279 rows are too many. One fully worked pair would teach more.

## 1. Audit boundary

**Conclusion C0 (Theorem 1).** Let T be a finite simple sphere triangulation with a proper black/white face colouring, t0 a black face, R its corners, A the other black faces, X = V(T) \ R. If there is a pair (r, s) of states with r(t) ≠ s(t) for all t ∈ A, then there is a pair with Q_s a forest.

**Hypotheses.** Only the above. No connectivity beyond simplicity, separating triangles allowed. The existence of one pair is assumed, not proved.

**Scope.** Sections 1 to 5 of involutions.tex (the proof and the constructor). Section 6 (attribution), Section 7 (relations and computations) and Section 8 (example) are audited as claims, not as part of the route to C0.

**Accepted primitives.** Euler's formula for a disk; existence of a plane straight-line drawing of a simple plane graph (Fáry), with a centre inside each black triangle; the Jordan curve theorem for polygons, in the form "crossings of a generic ray with a simple closed polygon alternate entry and exit, their number is odd iff the start is inside, and at an exit the interior is behind the ray"; finite counting (an involution without fixed points on a signed set with opposite-sign pairs gives signed sum zero).

**Separate conclusion C5 (Lemma 7).** The alternating procedure from an ι2-fixed object stops at a forest pair without repeating an object.

## 2. Obligation graph

```text
C0 <- R0 (signed count with two involutions on Omega; AND: O1, O2, C1, C2, C3, O3)
  O1  Omega is a well-defined finite set: drawing D0, m = min_p c(p) exists (O1a), tokens defined (Def. 3)
  O1a m exists and m >= 1: hypothesis (a pair exists) + finiteness + C(D) >= 1
  O2  sigma well defined: J(p) integer with J = #cw - #ccw (L2, O4)
  O3  counting step: no iota1-fixed point => signed sum 0; iota2 => signed sum = (-1)^floor(m/2) F != 0

C1 (Lemma 4: iota1 involution, sign-reversing, Fix = forest) <- AND: O5, O6, O7, O8, O9, O10
  O5  first cycle K of Q_s chosen from s alone (order on unoriented cycles)
  O6  every cycle of Q_s is directed by r (outdegree argument), so avoids roots
  O7  replacing r by u on K gives a state disjoint from s
  O8  s unchanged => tokens, directions, K unchanged => involution
  O9  sign: delta(u,s) - delta(r,s) = 2 delta(r,u); L2 on K => J changes by +-2
  O10 fixed set = {Q_s forest}

C2 (Lemma 5: iota2 involution, sign-reversing, fixed set description) <- AND: O11..O19
  O11 reversing any cycle of D_p gives a pair with the same unoriented cycles
  O12 case 1: same first unmarked cycle after reversal; tokens stay valid; J changes by +-2
  O13 case 2 entry: all cycles marked, c(p) >= m, |M| = m => c(p) = m, one token each (uses minimality)
  O14 partner exists (index 1 for inside w excluded by the selection rule)
  O15 moved token is a valid s-token after the move, and distinct from the others
  O16 selection is invariant (w_C, C, parity, index != 1 preserved by the pairing)
  O17 return move: reversal happens again iff it happened (spoke membership flips)
  O18 sign: keep-case flips one direction (O20); reverse-case flips J/2 parity, direction flipped twice
  O19 fixed set: m cycles, one token each, w inside, crossing number 1
  O20 Jordan facts for spoke cycles: alternation, parity = inside, consecutive crossings opposite (D0, O4)

C3 (Lemma 6: Fix(iota2) nonempty, one sign, |Fix| = F) <- AND: O1a, O21..O25
  O21 each cycle of D_p encloses a white face (L2)
  O22 per-cycle orientation can be chosen independently, and exactly one makes the first-crossed spoke an s-spoke (O11)
  O23 tokens on distinct cycles are distinct
  O24 sign: first exit of a ccw cycle crosses right to left; J = m - 2q; exponent floor(m/2) (O20)
  O25 count: bijection between fixed objects and (minimum unoriented cover, enclosed white face per cycle)

L2 (Lemma 2, disk identity) <- AND: O26 (roots excluded), O27 (B = I + l), O28 (two edge counts), Euler
O4 (spoke cycles are simple, same orientation and enclosed white points as D_p cycles) <- sliding argument; D0
D0 (drawing: straight-line, centres in black faces, generic white points and upward rays) <- Fary + general position

C5 (Lemma 7) <- AND: C1, C2, C3, O29 (two-labelled graph has max degree one per label), O30 (odd path => opposite sign)
```

No route switch, no cycle in the graph. ι1 and ι2 are each defined from data that the map itself does not change: ι1 picks K from s, and s is fixed; ι2 picks from the unoriented cycles, the white point of the token and the position class of the crossing (outside, or inside and not first), and all three survive the move. This is the place where such proofs usually fail. Here it holds. My code checks ι(ι(o)) = o and that both applications take the same case on every object of the census (`check.py`, assertion `case_back == case`).

## 3. Critical findings

None of the findings below touches the route to C0 or C5. The proof of Theorem 1 and Lemma 7 is correct as written.

**F1. Sign slip in the Section 7 comparison (WRONG as printed, off the proof route).** The display ends with `(-1)^{(n-m)/2} F`. The correct value is `(-1)^{(n+m)/2} F`. The step "the last signs agree since n ≡ m (mod 2)" is false for odd m: `⌈n/2⌉ + ⌊m/2⌋ = (n+m)/2`, which differs from `(n-m)/2` by m. Smallest counterexample: the octahedron, n = 3, m = 1, F = 1. The middle term is `(-1)^2 · 1 = 1`, the printed right end is `(-1)^1 · 1 = -1`. COMPUTED: the printed sign fails on exactly the 718 paired roots with m odd, out of 880, through 14 vertices (`code/out/census-14.json`, field `section7_printed_sign_fails_m_odd`). The author's verifier checks only the middle equality (`verify.py` line 144), which is why the slip survived. The source of the slip: H(s) as defined (left-to-right positive) falls by a(C) when C turns from clockwise to counterclockwise (COMPUTED, all 1120 reversals through 12 vertices, `code/out/extras-12.json`), while paper/main's ω rises by L(C) (Lemma 4.6 there). So H is −ω up to a constant on each class, and the main paper's sign `(-1)^{(n-m)/2}` (Proposition 4.8) must be multiplied by `(-1)^m`. Fix: EDITS E1.

**F2. Class count 56 should be 55.** plantri -b gives 1, 0, 1, 1, 2, 2, 8, 8, 32 classes for 6 to 14 vertices, total 55. The author's own census.json lists exactly these numbers. The rooted count 1206 = Σ classes × (2v − 4) is consistent with 55, not 56. The 56 appears in involutions.tex Section 7, STATUS.md and INVOLUTIONS.md. COMPUTED. Fix: EDITS E2.

**F3. The 279/213 explanation is wrong; the dependence on the drawing is not explained.** See DISCREPANCY-279-213.md. Both counts are correct. They are the same object model on the same input in two drawings that differ by swapping the anchor points of roots 4 and 5. The note attributes 213 to "an earlier layout" and contrasts its own geometry with "the manuscript's optimized disk layout", neither of which is where 213 comes from. The drawing changes |Ω| (35 different values between 103 and 363 over 69 computed drawings), the first fixed set (89 to 303 objects) and the alternating path lengths (0 to 6 moves). It does not change the signed sum (−9) or the second fixed count (9). Fix: EDITS E7, E8.

**F4. Path lengths depend on the drawing; "maximum two" is a property of the author's drawings.** In my census (Tutte layout with plantri's face order, vertical rays, first generic shear ≥ 0) all the same invariants agree with the author's (1206 roots, 880 paired, m = 1, 2, 3 on 560, 162, 158 roots, 4658 second-fixed objects), but |Ω| is 244240 rather than 221050 and one alternating path has four moves (13-vertex class 7, root 15, m = 2). On the running example with unsheared vertical rays, paths of six moves occur. The note does call the bound "a finite census result", so nothing false is claimed, but the text invites the reading that short paths are structural. Fix: EDITS E6.

**F5. Section 6 is not quite fair to Li, and does not credit the project audit.** Li's Appendix B (read in the PDF, page 12) states the set convention (`o = (M1, M2, {(w1, e_{2,1}), ...})`, and Definition 14 writes a set), the unmarked-cycle rule ("Most cases of ι2 also remain unchanged. Namely when there is a cycle without any intersection edges"), the case "exactly c_min cycles and each cycle C_i contains a different edge", the per-cycle swap `M1 △ C_i` in the exterior case, the same priority rule, the fixed set and its sign. Li fixes a total order on cycles in Section 4.3. What Li does not write: why all-marked forces one mark per cycle, that ι2 is an involution, that it reverses sign, the swap in the interior non-first case (only "switch to the other edge"), and why the fixed set is nonempty for c_min > 1. The note's list mixes the first group (set convention, invariant cycle choice) with the second. The sentence "The issue is already present at m = 2 ... so the unmarked-cycle rule is necessary" reads as if Li lacked that rule. Also, the project audit research/2026-11-14_fable_dependency-graph/audit-li.md (L-F5, L-F6) had already called the appendix "a correct sketch" and supplied the involution, sign-reversal and nonemptiness checks. The note's real contribution is a complete, careful write-up in one place, plus the cardinality F, the constructor and the computations. Fix: EDITS E4, E5.

**F6. Section 7's description of the height route is inaccurate.** "The height-product proof in the project fixes an indexed list of white faces" does not describe paper/main Section 4, which sums heights over all white faces along fixed paths of faces. Fix: EDITS E3.

**F7. Exposition gaps on the route (CORRECT, wording only).**
- Lemma 2's sentence "Indeed a black triangle inside must select an interior vertex, unless its selected vertex is on the boundary" is a tautology. The content is the bijection between inside triangles and interior-or-specified vertices (EDITS E10).
- The spoke-cycle paragraph (O4) is informal. A two-line winding-number argument replaces it (EDITS E9).
- Lemma 5, case 1, does not say that M remains a set of tokens of the new pair. It does, because the reversed cycle carries no token (EDITS E11).
- The traversal convention for r-spokes (point 3 of Section 0) should be stated once (EDITS E12).
- "Lexicographic order on sorted supplying-face sets" is not a total order on all unoriented cycles (two cycles can use the same faces with different sides). It is total on any family of face-disjoint cycles, which is all the maps compare (EDITS E13).

**F8. Figures.** Figures 1 and 2 do not draw the rays, so the tokens cannot be seen, and the interior is too small to read. A tested fix that draws both rays and adds a zoomed panel is EDITS E14; the result is `code/out/figure1-proposed.png`. Figure 3 is readable.

## 4. The questions in the brief

**What is a marked object?** A pair p = (r, s) together with an unordered set M of exactly m distinct tokens. A token is a pair (w, t): w a white face (through its chosen point and upward ray), t ∈ A, such that the ray from w crosses the spoke from the centre of t to s(t). The same white face may appear in several tokens, the same spoke in several tokens, but no token twice. A mark is therefore a ray crossing, not a white face. With straight spokes and straight rays a ray meets a spoke at most once, so (w, t) determines the crossing. This matches Li's Definition 14 and Appendix B exactly (both write a set). CORRECT.

**Canonical choices depend only on preserved data.** Verified, see Section 2. COMPUTED on every object of the census in two orders on cycles (lexicographic and a random order), so the result does not depend on the particular total order.

**Sign reversal, fixed sets, nonempty and one-signed second fixed set, final counting.** All CORRECT; details in the table.

**c_min and the "minimum cover search".** The existence proof needs only the number m = min_p c(p), which exists because the set of pairs is finite and nonempty. Nothing is searched. Minimality is used in exactly one place, O13. The constructor (Section 5) needs an actual minimum cover to build its first ι2-fixed object, and finds it by enumerating all pairs. So the search belongs to the algorithm, and the note says so ("It requires a minimum cover at initialization").

**Can the argument run with another number k of marks?** No, not as written. With k < m, case 1 of ι2 always applies (k tokens cannot mark c ≥ m > k cycles), so ι2 has no fixed point and the signed count is zero: COMPUTED zero in all 880 paired roots for k = m − 1. With k > m, case 2 is undefined (a cycle may carry two tokens). ι1 is still a sign-reversing involution for every k, so any k with a nonzero signed count would also prove the theorem. But with k = m + 1 the signed count is zero on 20 of 208 paired roots through 12 vertices and has the "wrong" sign on 75 (`code/out/extras-12.json`). So m is the right number and cannot be replaced by an arbitrary admissible one. This matches the remark after Proposition 4.8 of paper/main that the minimum cannot be dropped.

**Garsia–Milne alternation and termination.** CORRECT. The two-labelled graph has at most one edge of each label at each vertex, the start has no label-2 edge, the component is a path, and an odd path would join two ι2-fixed objects of opposite sign. COMPUTED: from every one of the 4658 second-fixed objects through 14 vertices, the walk ends at a forest pair without repetition.

## 5. Comparison with Li's note

| Note | Li | Same or different |
| --- | --- | --- |
| Def. 3, tokens and sign | Defs. 13, 14, 18, 21, App. B | Same objects (set of c_min distinct crossings with M2-edges); M2 = s-spokes, M1 = r-spokes. Li orients cycles s(t) → t → r(t), the note r(t) → t → s(t). I checked the claim that the two signs agree: Li's exponent is ⌊−J/2⌋ + Σ(1 − d) ≡ ⌊J/2⌋ + [J odd] + m + Σd, and [J odd] ≡ n ≡ m. CORRECT. |
| Lemma 2 (disk identity) | Claim 25 (|C|/4 ± 3/2 by Euler in G_FB) | Same count in two languages; the note uses OpenAI Lemma 4.1's form. |
| Lemma 4 (ι1) | Def. 22, Lemma 17 (via Claim 26, local τ), Lemma 34 | Same map. Different proof of the sign change: the note uses δ and the disk identity, Li uses the turn count τ. Equivalent. |
| Lemma 5 (ι2) | Def. 20, 23, Lemma 35, App. B | Same map, same pairing, same priority. The note writes out what App. B leaves (F5). |
| Lemma 6 | Lemma 24, proof of Lemma 7, App. B last paragraph | Same fixed set and sign; the count F and the per-cycle orientation argument are written here. |
| Lemma 7 | none | New in this note; the method is the Garsia–Milne principle, attributed correctly to its use in barnette_trees Section 5.1. |

The completed argument is Li's intended proof, not a different one. Every step is attributed in STATUS.md. Attribution is accurate except for the fairness points of F5.

## 6. Relation to the other two routes

paper/main Section 4 (heights) and proofs/primal (integer polynomial in the primal) prove the same lemma by one computation: group the pairs into classes of 2^c with the same unoriented cover, observe that the sign alternates and a height ω changes by L(C) under each cycle reversal, and take an m-th finite difference (paper/main Lemma 4.7). The cancellation of states with cyclic Q_s (Lemma 4.5 there) is the same involution as ι1.

The dictionary, in my words, all checked against the computations:

1. ι1 is paper/main Lemma 4.5 lifted to objects. The lift works because tokens depend on s only, just as Lemma 4.5 works for any function F of the second state.
2. H(s) = Σ over tokens of ±1 is a height in the sense of paper/main, measured along rays instead of paths of faces, with the opposite normalisation: it falls by a(C) when C turns counterclockwise (COMPUTED, 1120 of 1120 reversals). Expanding H(s)^m into ordered lists of tokens gives `(1/m!) Σ_p ε(p) H(s)^m = (−1)^{⌈n/2⌉} Σ_o σ(o)` (COMPUTED in every paired root through 14 vertices, my `check.py`). So the note's signed count is, up to the explicit sign, the m-th coefficient of the height polynomial for this height. That is the audit's statement that Li's marks are the Taylor coefficient of order c_min for one concrete weight.
3. ι2 is a bijective proof of the finite-difference lemma and the height lemma together. Case 1 (reverse an unmarked cycle) is the vanishing of `Σ_{x_i} (−1)^{x_i}` for an index that no monomial uses. Case 2 is the height lemma made bijective: along the ray from w, crossings of C pair off and one first exit survives exactly when w is inside C, which is the statement "η changes by 1 iff y is inside C". The fixed set is the monomial `L(C_1) ⋯ L(C_m)` written out as one enclosed white face per cycle.

So the bijective proof is a term-by-term unpacking of the height proof for one specific height. It is genuinely free of polynomials and gives a constructor, which the algebraic route does not. It is not mathematically independent: both routes stand on the same three facts (disk identity, sign change under the two reversals, a height whose increment is the enclosed white-face count) and use minimality in the same place. The primal proof is the same computation again in G with an integer polynomial (proofs/primal/COMPARISON.md says as much).

## 7. Verdict per lemma

| Item | Verdict | Note |
| --- | --- | --- |
| Lemma 2 (disk identity) | CORRECT | One tautological sentence, EDITS E10. COMPUTED: δ-sum ±3 on every D_p cycle and every directed Q_s cycle through 14 vertices; orientation by δ equals orientation by signed area. |
| Spoke cycles (O4) | CORRECT AFTER FIX | Claim true; argument informal. Replacement in EDITS E9. COMPUTED: same enclosed white points for vertex and spoke polygons, and ray parity equals inside, on every cycle. |
| Definition 3 | CORRECT | Precise. The dependence of Ω on the drawing should be said (EDITS E8). |
| Lemma 4 (ι1) | CORRECT | COMPUTED on 244240 objects through 14 vertices. |
| Lemma 5 (ι2) | CORRECT | Two missing sentences (EDITS E11, E12). COMPUTED, both cycle orders. |
| Lemma 6 (fixed set) | CORRECT | F formula COMPUTED: |Fix(ι2)| = F and every class has 2^m orientations. |
| Theorem 1 | CORRECT | |
| Lemma 7 (constructor) | CORRECT | Initialisation by exhaustive search, as stated. |
| Section 6 (what Li leaves unwritten) | CORRECT AFTER FIX | Fairness and credit, EDITS E4, E5. |
| Section 7 moment identity | WRONG as printed for odd m | Counterexample: octahedron, n = 3, m = 1. Replacement EDITS E1. Not used by the proof. |
| Section 7 census numbers | CORRECT AFTER FIX | 56 → 55 (E2); path lengths drawing-dependent (E6). Everything else reproduced: 1206, 880, 560/162/158, 4658. |
| Section 8 example | CORRECT AFTER FIX | All 279 objects, signs and both images reproduced exactly. Explanation of 213 wrong (E7). |

## 8. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | If a pair exists, a pair with Q_s a forest exists | root | R0 | root | O1, O2, O3, C1, C2, C3 | discharged |
| D0 | Straight-line drawing, centres inside black faces, white points and upward rays in general position | O1, O4, O20 | R0 / AND | named theorem | Fáry; finitely many bad directions | discharged |
| O1 | Ω is a well-defined finite set of objects with m distinct tokens | C0 | R0 / AND | definition | Def. 3, D0, O1a | discharged |
| O1a | m = min_p c(p) exists and m ≥ 1 | O1, O13, C3 | R0 / AND | hypothesis | a pair exists; finite set; c ≥ 1 | discharged |
| O2 | J(p) is an integer, J = #cw − #ccw, J ≡ c ≡ n (mod 2) | C0, O9, O18, O24 | definition / AND | algebraic/logical step | L2, O4 | discharged |
| O3 | No ι1-fixed point ⇒ Σσ = 0; ι2 ⇒ Σσ = (−1)^⌊m/2⌋F ≠ 0 | C0 | R0 / AND | algebraic/logical step | C1, C2, C3 | discharged |
| L2 | Disk identity: simple directed cycle of selected sides avoids roots, h − 2ℓ = 3, odd, encloses a white face, δ-sum ∓3 | O2, O9, O21 | proved earlier | proved earlier | O26, O27, O28, Euler | discharged |
| O26 | Selected sides never have a root as tail, so the disk contains no root | L2 | AND | definition | X = V \ R | discharged |
| O27 | B = I + ℓ | L2 | AND | algebraic/logical step | state bijectivity; wording fix E10 | discharged |
| O28 | E = 3B + h − ℓ = 3W + ℓ | L2 | AND | algebraic/logical step | each edge has one black and one white face | discharged |
| O4 | Spoke cycles are simple polygons with the orientation and enclosed white points of the D_p cycles | O20, O21 | AND | side condition | sliding argument, replaced by E9 | discharged |
| C1 | ι1 is a sign-reversing involution with Fix = {Q_s forest} | C0, C5 | R1 | major claim | O5–O10 | discharged |
| O5 | K is chosen from s alone | C1 | R1 / AND | definition | order on unoriented cycles (E13) | discharged |
| O6 | Every cycle of Q_s is directed by r and avoids roots | C1 | R1 / AND | algebraic/logical step | out-degree one at nonroots, zero at roots | discharged |
| O7 | r with u on K is a state disjoint from s | C1 | R1 / AND | algebraic/logical step | O6 | discharged |
| O8 | Tokens, directions and K unchanged; second application restores r | C1 | R1 / AND | algebraic/logical step | s fixed | discharged |
| O9 | J changes by ±2 under ι1 | C1 | R1 / AND | algebraic/logical step | δ(u,s) − δ(r,s) = 2δ(r,u); L2 on K | discharged |
| O10 | Fix(ι1) = objects with Q_s a forest | C1 | R1 / AND | definition | nonempty K changes r | discharged |
| C2 | ι2 is a sign-reversing involution with the stated fixed set | C0, C5 | R2 | major claim | O11–O20 | discharged |
| O11 | Reversing a D_p cycle gives a pair with the same unoriented cycles | C2, O22 | R2 / AND | algebraic/logical step | values on C are permuted | discharged |
| O12 | Case 1 is an involution, keeps tokens valid, flips sign | C2 | R2 / AND | algebraic/logical step | unmarked cycle; J ± 2; wording E11 | discharged |
| O13 | All cycles marked ⇒ exactly m cycles, one token each | C2 | R2 / AND | side condition | O1a (minimality), pigeonhole | discharged |
| O14 | The partner of the token exists | C2 | R2 / AND | side condition | selection excludes index 1 | discharged |
| O15 | The moved token is a valid s-token distinct from the others | C2 | R2 / AND | side condition | one token per cycle; reversal relabels spokes | discharged |
| O16 | The same cycle is selected on the second application | C2 | R2 / AND | algebraic/logical step | w_C, C, parity, index ≠ 1 preserved | discharged |
| O17 | The return move reverses iff the first did | C2 | R2 / AND | algebraic/logical step | spoke membership flips with reversal | discharged |
| O18 | Both case-2 moves flip σ | C2 | R2 / AND | algebraic/logical step | O20, O2; convention E12 | discharged |
| O19 | Fixed set: m cycles, one token each, w inside, first crossing | C2, C3 | R2 / AND | definition | all other rules move something | discharged |
| O20 | Ray crossings of a simple closed polygon alternate entry/exit, parity = inside, consecutive ones opposite | O14, O16, O18, O24 | AND | named theorem | Jordan for polygons; D0; O4 | discharged |
| C3 | Fix(ι2) nonempty, all of sign (−1)^⌊m/2⌋, size F | C0, C5 | R3 | major claim | O1a, O19, O21–O25 | discharged |
| O21 | Each D_p cycle encloses a white face | C3 | R3 / AND | proved earlier | L2, O4 | discharged |
| O22 | Exactly one orientation per cycle makes the first-crossed spoke an s-spoke; choices independent | C3 | R3 / AND | algebraic/logical step | O11 | discharged |
| O23 | Tokens on distinct cycles are distinct | C3 | R3 / AND | algebraic/logical step | distinct spokes | discharged |
| O24 | A ccw cycle's first exit crosses right to left; J = m − 2q; exponent ⌊m/2⌋ | C3 | R3 / AND | algebraic/logical step | O20, O2 | discharged |
| O25 | Fixed objects ↔ (minimum unoriented cover, one enclosed white face per cycle) | C3 | R3 / AND | algebraic/logical step | O19, O22; COMPUTED | discharged |
| C5 | The alternating walk from an ι2-fixed object ends at a forest pair without repetition | separate root | R5 | major claim | C1, C2, C3, O29, O30 | discharged |
| O29 | The two-labelled graph has at most one edge of each label at each vertex; the start has no label-2 edge | C5 | R5 / AND | definition | involutions | discharged |
| O30 | An odd alternating path joins objects of opposite sign | C5 | R5 / AND | algebraic/logical step | C1, C2 sign reversal | discharged |
| S7 | (1/m!) Σ ε H^m = (−1)^{(n−m)/2} F (Section 7, off route) | none | comparison only | too strong | true with (−1)^{(n+m)/2}; F1 | failing |

## 9. Verdict

**FOLLOWS.** Theorem 1 follows from its hypotheses by the route the note supplies. Every obligation on R0 and its sub-routes (C1, C2, C3, L2, O4, D0) is discharged, with no hidden assumption, cycle, overreach or route switch. The decisive nodes are O5 and O16 (the choice rules use only data the maps preserve), O13 (the only use of minimality) and O22 (the independent orientations behind nonemptiness). They hold as written. The constructor C5 also FOLLOWS.

The defects are off the proof route: a sign error in the Section 7 comparison (S7, wrong for odd m, with an octahedron counterexample), a wrong explanation of 279 against 213, a miscounted class total, an attribution section that is unfair to Li in two sentences and does not credit the project's earlier audit, and figures that do not show the rays. EDITS.md fixes all of them in 15 edits. After those edits I would call the note a complete and correct write-up of Li's two-involution proof for every c_min. It is a bijective unpacking of the height proof for one particular height, not an independent proof. Status: PROVED-HERE by the author, refereed by one independent AI referee with its own code, human check pending.
