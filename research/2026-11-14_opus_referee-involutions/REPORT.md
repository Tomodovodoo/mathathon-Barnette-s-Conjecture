# Referee of proofs/involutions/: report

1. Verdict FOLLOWS: the two-involution proof of the forest-pair lemma for general c_min is correct as written; every lemma on the route checks, by hand and by my own code (COMPUTED, all 1206 rooted instances through 14 vertices, both cycle orders).
2. 279 versus 213 is resolved: same objects, same input, two drawings that differ by swapping the anchors of roots 4 and 5. Both counts are right; the note's explanation of 213 is wrong. Object counts, first fixed sets and path lengths depend on the drawing; the signed sum and F do not.
3. One real error, off the proof route: the Section 7 identity has sign (−1)^{(n−m)/2} where (−1)^{(n+m)/2} is correct; it fails for every odd m (octahedron, n = 3, m = 1).
4. Smaller defects: 56 classes should be 55; Section 6 is unfair to Li in two sentences and does not credit the project audit that first supplied the missing checks; Figures 1 and 2 do not draw the rays.
5. The proof is Li's intended proof, written out; relative to paper/main it is a bijective unpacking of the height proof for one height (rays), not an independent route. 15 exact edits in EDITS.md.

## What I set out to do

Referee proofs/involutions/ independently: read the PDF cold, audit it backward from Theorem 1 with the reverse-Lamport method, verify everything with my own code on all rooted instances up to at least 12 vertices and on c_min = 2 and 3, resolve the 279/213 discrepancy, compare with Li's note and with the project's two other routes, and give per-lemma verdicts and at most 15 edits.

## What I established

- PROVED-HERE (checked): Lemmas 2, 4, 5, 6, Theorem 1 and Lemma 7 are correct. The choice rules of both maps use only data the maps preserve (Q_s from s; unoriented cycles, the token's white point and the crossing's position class). Minimality of m is used once, to force one token per cycle when all cycles are marked. Nonemptiness of the second fixed set comes from orienting each minimum cycle independently. REFEREE.md has the obligation graph and the dependency table.
- COMPUTED (`code/check.py census 14`): 55 classes, 1206 roots, 880 paired, m = 1/2/3 on 560/162/158, 4658 second-fixed objects; every assertion passes in the lexicographic and a random cycle order. These invariants match the author's numbers exactly; the object count (244240 against 221050) and walk lengths (max 4 against 2) differ, as they should in a different drawing.
- COMPUTED (`code/compare_running.py`): the note's 279-object table matches my computation object by object, including both images and signs.
- COMPUTED (`code/running.py`): the 213 of the earlier Li replay comes from the lab's root order 0, 4, 5 in the same recipe. Over 69 drawings of the running example: 35 object counts (103 to 363), walk lengths 0 to 6, signed sum −9 and nine second-fixed objects every time.
- COMPUTED (`code/extras.py 12`, census): H falls by a(C) when C turns counterclockwise (1120 of 1120 reversals), the source of the Section 7 sign slip. With m − 1 marks the signed count is always zero; with m + 1 marks it is zero on 57 of 880 paired roots, so m cannot be replaced by another number of marks.
- Comparison: the note's objects, sign, maps and fixed set are Li's (Def. 14, 21, 22, 23, App. B), with Li's opposite cycle orientation correctly accounted for. In paper/main's language, ι1 is Lemma 4.5 lifted to objects and ι2 is a bijective proof of Lemmas 4.6 and 4.7 together for the ray height.

## What failed or stayed open

Nothing in the proof failed. I did not run the hard families or anything beyond 14 vertices, so m ≥ 4 is untested (it does not occur through 14 vertices). I did not find a drawing-free object model; I think crossing-based tokens cannot avoid the dependence (HUNCH). I did not apply any edit; the folder is the author's.

## Three best next steps

1. Apply EDITS E1 (sign), E4/E5 (fairness and credit), E7/E8 (drawing dependence) and E14 (rays in the figures); rebuild the PDF.
2. In the exposition paper, present ι2 next to the height proof as its bijective form (case 1 = vanishing differences, case 2 = one first exit per enclosed white face), using the running example in one drawing with the rays drawn.
3. Test m ≥ 4 instances (stacks of separating triangles should raise c_min) and record whether alternating paths grow with the drawing; any claim about short paths should fix a drawing rule first.

## Leads for others

- paper/main Proposition 4.8's sign (−1)^{(n−m)/2} is correct for its ω. Anyone transcribing between ω and ray heights must flip the sign of the height and pick up (−1)^m.
- The lab's `li.py` docstring says the multi-mark extension "is intentionally not claimed", but `LiMultiObjects` implements it. In its drawing it gives the same object, first-fixed and second-fixed counts (213, 141, 9) as my implementation of the note's maps; I compared counts, not individual objects.
