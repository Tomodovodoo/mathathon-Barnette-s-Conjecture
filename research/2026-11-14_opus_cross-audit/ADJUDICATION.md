# Adjudication: real sign versus Lean phase

Question. The referee (research/2026-11-14_fable_referee-primal/LEAN-MATCH.md, item M4) says the primal note's real sign and the Lean proof's phase differ by a factor that depends on the number of circuits of the pair, so the two polynomials are different sums. The reviser (research/2026-11-14_astra_primal-revision/CHANGES.md, item 6d) says the ratio is the constant i^n.

Verdict. The reviser is right. The referee's formulas are correct up to the last line; the factor it calls c-dependent is i^n. PROVED-HERE below, COMPUTED on 24,856 pairs.

## Definitions used

From the note (proofs/primal/PRIMAL-PROOF.md, Sections 2 and 6). For a pair (r, s) of states and b in A, delta(r(b), s(b)) is +1 if the transition from face r(b) to face s(b) around b has b on its left, else -1. The real sign is eps(r, s) = prod_b delta(r(b), s(b)). The polynomial is Z = sum over pairs of eps(r, s) L_s(z), with L_s = prod_b (1 + a(b, s(b)) z).

From Lean, github.com/openai/math at commit 4eaee87548250b2682affda7d05d947c05554bae (read in research/2026-11-14_opus_lean-formalisation/upstream/openai-math, whose HEAD I confirmed is that commit; I did not clone again):

- `TriangleSystem.indexDelta i j = if i = j then 0 else if j = i + 1 then 1 else -1` (TriangleSystem.lean:96), on corner indices in Fin 3.
- `rawIndexSum r s = sum_t indexDelta (r.val t) (s.val t)` (PairPhases.lean:31).
- `phase n = Complex.I ^ (n / 3)` (PairPhases.lean:9), with Lean's integer division.
- `term w P = C (phase (rawIndexSum P.left P.right)) * stateWeight w P.right` (PairPolynomials.lean:224), and `stateWeight w s = prod_t (1 + w t (s t) X)` (:192). So Lean's polynomial is sum over pairs of phase times the same kind of linear product as L_s.

"Aligned" means Lean's corner successor j = i + 1 is the note's +1 transition, so indexDelta(r(t), s(t)) = delta(r(b), s(b)).

## Proof

Fix a rooted graph and a pair. Let t = sum_b delta(r(b), s(b)) and let p and m be the numbers of +1 and -1 terms, so p + m = n and p - m = t.

1. eps = (-1)^m = i^(2m) = i^(n - t). This needs nothing about pairs.
2. 3 divides t. The edges r(b) -> s(b) form the selected collection D of the pair. D splits into c directed face circuits, each a state circuit for r (proof of Lemma 8). Lemma 5 gives delta-sum -3 sigma on each, so t = 3(c_- - c_+), where c_+ counts circuits with sum -3 (the note's positive orientation) and c_- those with sum +3.
3. Hence Lean's integer division is exact and phase = i^(t/3) = i^(c_- - c_+).
4. eps / phase = i^(n - t - t/3) = i^(n - 4(t/3)) = i^n, since i^4 = 1.

So for every pair of the rooted graph the ratio is i^n. It depends on n, which is fixed once the graph and root are fixed, and on nothing about the pair. With the same weights, Z_note = i^n Z_Lean.

If Lean's corner order runs opposite to the note's, then indexDelta = -delta at every triangle, Lean's sum is -t, its phase is i^(-t/3), and eps / phase = i^(n - t + t/3) = i^(n - 2t/3). Here t/3 = c_- - c_+ has the parity of c, and c has the parity of n because n is the sum of c odd circuit lengths. So 2t/3 = 2n mod 4 and the ratio is i^(-n). Still constant. This is where the parity fact n = c (mod 2) enters. I did not settle which orientation `ColoredDual.oriented` produces relative to the note's sphere orientation; the conclusion does not depend on it.

## Where the referee went wrong

The referee's two closed forms are right. A positive circuit of odd length h has (h + 3)/2 negative signs and a negative one has (h - 3)/2, so

    eps = (-1)^((n + 3c)/2) * (-1)^(c_-),   phase = i^(c_- - c_+),

and their ratio is (-1)^((n + 3c)/2) i^c. The exponent (n + 3c)/2 is an integer because n = c mod 2. The referee stopped here and read the expression as c-dependent. But (-1)^((n + 3c)/2) = i^(n + 3c), so the ratio is i^(n + 4c) = i^n. Raising c by two flips the sign of (-1)^((n+3c)/2) (the exponent moves by 3) and also flips i^c; the product does not change.

## Numerical confirmation

COMPUTED. Script: scripts/phase_ratio.py (my own code; it does not import the referee's or the reviser's checkers). Inputs: data/plantri-b-V.txt, produced by `workings/barnette_lab/vendor/plantri.exe -b -a V` for V = 6, 8, ..., 16 (there is no 7-vertex Eulerian triangulation), and paper/figures/running.json.

For every triangulation, both colour classes taken as black, every black root, every ordered pair, the script asserts:

- every circuit of D(r, s) has delta-sum +3 or -3;
- 3 divides t, and eps = i^(n - t);
- eps / phase = i^n with aligned corner order, and i^(-n) with reversed order;
- the referee's closed forms for eps and phase hold, and (-1)^((n+3c)/2) i^c = i^n;
- with the same random integer weights, Z_note = i^n Z_Lean coefficient by coefficient;
- every rooted instance without a pair comes from a triangulation with a separating triangle (Lemma 4).

Commands (from this folder):

    python -I scripts/phase_ratio.py data/plantri-b-{6,8,9,10,11,12,13,14}.txt ../../paper/figures/running.json > data/phase_ratio.json
    python -I scripts/phase_ratio.py data/plantri-b-15.txt data/plantri-b-16.txt > data/phase_ratio_15_16.json

| Range | Graph records | Rooted instances | Ordered pairs | Instances with two circuit counts | Instances without pairs (all with a separating triangle) |
| --- | --- | --- | --- | --- | --- |
| 6 to 14 vertices plus running example | 56 | 1,228 | 3,392 | 22, counts {1, 3} | 326 |
| 15 and 16 vertices | 242 | 6,662 | 21,464 | 273, counts {1, 3} or {2, 4} | 2,454 |
| Total | 298 | 7,890 | 24,856 | 295 | 2,780 |

No assertion failed. The 295 instances where pairs with different circuit counts coexist are the decisive ones: a c-dependent ratio would have shown up there, and it did not. The plantri census is taken as the lab binary reports it; I do not certify its completeness.

## What I changed

- proofs/primal/PRIMAL-PROOF.md, Section 6 (and so primal.tex/pdf): the phase paragraph now cites Lemma 5 for 3 | t, states the opposite-orientation constant i^(-n), and points to STATUS.md instead of naming the referee in the body.
- proofs/primal/STATUS.md: the phase section is rewritten as an adjudication with the corrected referee formula, the parity remark and the numerical range above.

The reviser's text was already correct in substance. The note's claim "the two polynomials are constant multiples" stands.
