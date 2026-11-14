# Report: independent referee of the primal proof

Summary.
1. Verdict FOLLOWS. `proofs/primal/PRIMAL-PROOF.md` is a correct informal proof of Theorem T relative to standard planar background. No lemma is wrong. One step is asserted without proof (the cancellation in Lemma 3) and I supply it.
2. The list of accepted planar facts is three items short and does not say whether a plane graph is a drawing or a rotation system. It does not hide the hard part. Exact replacement text is in REFEREE.md, F1.
3. STATUS.md matches the Lean sources at commit `4eaee875`: every line number and every cited header is right, no false "machine-checked" label. Five mismatches of scope or citation are listed in LEAN-MATCH.md.
4. COMPUTED with my own code on all 56 graphs with 6 to 14 faces (8 to 24 vertices), 1,214 roots, 15.2 million checks, 0 failures. Both worked examples of the note reproduce exactly.
5. Recommendation for the paper: primal proof as the backbone, dual triangulation as picture language and dictionary. Details in RECOMMENDATION.md.

## What I set out to do

Referee, as a different model from the author, the primal proof in `proofs/primal/`: a reverse-Lamport audit from Theorem T backward, a check of STATUS.md against the Lean declarations, a numerical check of every lemma with my own code, a comparison with Li's note, verdicts per lemma, and a recommendation on the language of the final paper.

## What I established

- PROVED-HERE (by checking the note's proofs line by line, REFEREE.md). Lemmas 1, 4 to 13 and Theorem T are correct as written. Lemma 2 is correct and needs one sentence in part (b). Lemma 3 is correct once `δ` is defined with one sense of rotation at all black vertices and once the pairing with a facial boundary is computed. I give that computation: `δ(f,g)` is the coefficient of the edge `b→w` in the boundary of `g`.
- PROVED-HERE. Lemma 12 holds for any perfect matching whose edge at each `b ∈ A` lies on `s(b)` for some state `s`. The note's own proof shows this. It is the hypothesis set of Lean's `selected_forest`.
- PROVED-HERE. The note's real sign and Lean's phase differ by the factor `(-1)^{(n+3c)/2}·i^c`, which depends on the number `c` of circuits. So the two polynomials are different sums.
- COMPUTED (`code/check_lemmas.py`, 6 to 14 faces, all roots). Every assertion of Lemmas 1 to 13 in primal form, the bijection between bonds and face circuits (1,066,157 of each), the capacity criterion against brute-force pair existence, the structure of minimal deficient sets, all four counts on 84,984 state circuits, slopes for two different flows, the polynomial `Z` with its lowest coefficient, 9,768 recoveries, all 39 nontrivial 3-edge cuts with their caps and gluings, Theorem T by brute force and by running the proof as a recursion on 3,642 rooted inputs.
- COMPUTED (`code/check_examples.py`). Section 11 of the note: 33 comparisons, all agree, including both polynomials.
- COMPUTED. Three observations not in the note: a circuit-free state without a partner never gives a tree in Lemma 9 (25,272 cases); a circuit-free second state with a partner has exactly one (3,256); a perfect matching has a compatible state exactly when its complement is connected (186,476 cases).
- LIT comparison. Against Li's note the primal proof is more complete at every step where the earlier audit of Li had to supply something (balance for the 2-factor, `c_min > 1`, the tree trace, the innermost cycle), and it needs no straight-line drawing. Li has figures and a bijective proof of nonvanishing. Table in REFEREE.md, Section 6.

## What failed, and why

- Nothing in the proof failed. I tried to break each lemma by enumeration and found no counterexample.
- My first parser for the worked examples matched no state line, so two comparisons passed with nothing to compare. A later step crashed and exposed it. Fixed, with a guard. Recorded in `code/README.md`.
- I did not rebuild the Lean. I compared statements with sources and relied on the earlier agent's build report.
- I read the two paper drafts only at the level of outline and referee summaries. The recommendation says so.
- Numerical coverage of Lemma 7 is thin: twenty cancelling second states in the whole range.

## What is still open

- The planar background is accepted, not proved. Whoever writes the paper has to choose between drawings (then the Jordan curve theorem sits under Euler and under "facial boundaries are cycles") and rotation systems (then the corollary needs that planar graphs have genus-0 rotation systems). The note should say which.
- CONJECTURE. For a rooted Barnette graph and a perfect matching `P`, a state compatible with `P` exists if and only if `G - P` is connected. One direction is Lemma 12'. Test for the converse: enumerate at 15 and 16 faces with `check_lemmas.py`, or prove it from the incidence-tree criterion of the constructive paper (Proposition 2.1), which I did not check for this.
- CONJECTURE. A second state with circuit-free `Q_s` has at most one partner. Test: same enumeration. Likely LIT in the constructive paper. I did not verify the reference.
- A human check of REFEREE.md, F3, the one step I added.

## Three best next steps

1. Apply the five replacement texts (F1, F2, F3, F4, F7) and the restatement of Lemma 12 to `proofs/primal/PRIMAL-PROOF.md` and `primal.tex`. This is an hour of editing and removes every finding.
2. Build the final paper on the primal lemmas with the dual pictures listed in RECOMMENDATION.md. Start with the four figures named there.
3. Run `check_lemmas.py` at 15 and 16 faces (57 and 185 graphs, about ten minutes per ten graphs at 16 faces if the pattern holds) to raise the count of cancelling states for Lemma 7 and to test the two conjectures above.

## Leads for others

- For the Lean thread: STATUS.md should cite `make_coloredDual` (ThreeCuts.lean:101), `cap_duality` (CappedDuality.lean:148) and `Duality.bond_of_circuit` (Bonds.lean:109). These carry the planar content that the note replaces by facts on facial walks.
- For the draft authors: both referee gaps in drafts A and B (connectedness under Euler in the disk, the root outside the disk) vanish if the disk is defined as the shore of a bond. That can be adopted in a dual text without rewriting it.
- For the constructive thread: the equivalence "compatible state exists iff complement connected" may be the incidence-tree criterion in another form.

## Files

- `REFEREE.md`: boundary, obligation graph, findings F1 to F9, answers to the brief, verdicts per lemma, comparison with Li, dependency table, verdict.
- `LEAN-MATCH.md`: STATUS.md against the Lean, declaration by declaration, mismatches M1 to M5.
- `RECOMMENDATION.md`: language of the final paper, step by step.
- `code/`: `primal.py`, `gen.py`, `check_lemmas.py`, `check_examples.py`, `README.md`, `out/`.
