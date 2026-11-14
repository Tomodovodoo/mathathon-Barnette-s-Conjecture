# Report: different-model referee of the counting, probabilistic and algebra folders

Summary.
1. I refereed three folders by GPT-6.1 Sol with my own code and reasoning. Every number I replayed agrees with the authors'.
2. One claim needs a fix: the prism chain's Hamiltonian count 20*3^(q-2) holds only for a gluing rule the text does not state (second piece on v_4 or v_5, later pieces pole on pole). A uniform rule gives 8*3^(q-1) or two other sequences.
3. One proof has a mislabelled vertex (six-cycle counterexample, B1 should be B0). Nothing is wrong beyond that.
4. The mean obstruction is correct and narrow: it says the target lies on a face of the degree polytope. The six-state gauge certificate is correct for signs on the variables of F only. With signs on both states' incidences the equations are solvable on all 5088 paired roots up to 16 vertices.
5. Not checked: the transfer code behind "for all L", the literature comparisons in BOUNDS.md (sources not held), modulus 11, and all sampling and mixing numbers.

## What I set out to do

Check, as a model different from the author, the claims of `2026-11-14_sol_counting-families`, `2026-11-14_sol_route-probabilistic` and `2026-11-14_sol_route-algebra`: restate, replay small cases with my own code, read the proofs, give verdicts, compare with the same-model review, and write integration wording.

## What I established

Status tags as in the brief. COMPUTED items name the script in `code/` and the range.

- COMPUTED, `t_families.py`. Prism formulas for m=2..12, every edge.
- COMPUTED, `t_tubes_long.py`. Width-4 tube: S=Fib(2L+3) to L=20, P=M=2 and one-cycle least cover to L=14, H to L=10. Width-6 tube: S to L=12, M to L=12, P to L=9, H to L=6. Each recurrence predicts every computed term past its initial values (H at width 6: one term, 58112).
- COMPUTED, `t_certs.py`. The eight matrix certificates satisfy their recurrences on D+10 consecutive terms and reproduce my brute-force sequences.
- COMPUTED, `t_chain.py`, `t_chain_perms.py`, `t_chain_lab.py`. Chain: S=3^q, P=M=2^q, one cover with q cycles, product polynomial, for six identifications and q<=5. H depends on the identification. The author's sequence comes from a mixed rule.
- COMPUTED, `t_census.py 16`. On 7868 roots: states share one permutation sign, signed sum zero, good states balanced, M even. On 5088 roots with a pair: M>=2m, M>=2^m, 2^m divides P. First moments vanish on 2484 roots with m>=2, second moments on 1464 roots with m>=3. Gauge equations on the variables of F fail at exactly the author's 68 roots. Residue witnesses for 2, 3, 4, 5, 7 agree.
- COMPUTED, `t_walk.py 12`. The height-marked walk is correct on every marked object of 215 rooted instances.
- COMPUTED, `t_misc.py`. tau(H)=128 and 2700. H_avoid(e0)>=M and 3M<=H on 1206 roots.
- Proofs read line by line and found correct: prisms, chain factorisation and polynomial, the gluing formula for H, the bounds (with M>=2m rederived by Newton's identities), the mean obstruction, the exponential-family lemma, the signed measure and moments, the walk, the sign barrier, parity, Cauchy and Binet, the stability counterexample, the local matrices, the Berezin and Gaussian formulas.
- LIT. Thomason's Corollary 1.5 read from the scan `2026-11-14_sol_route-algebra/Thomason-page262.png`. It says what the author says.

Verdicts are in REFEREE-families.md, REFEREE-probabilistic.md and REFEREE-algebra.md. Differences from the same-model review are in DISAGREEMENTS.md. Wording for the paper is in INTEGRATION.md.

## What failed or was not done, and why

- I did not check the author's transfer code against their prose argument. So "for all L" on the tubes has no different-model check beyond arithmetic and finite ranges. Time.
- Florek 2020, Florek 2024 and Pivotto and Royle are not held in the project and I did not open them. The comparisons in BOUNDS.md are unverified by me.
- Modulus 11 (truncated cuboctahedron) was not replayed. I did not build that graph.
- Not replayed: four-subdivided stacked cubes, avoidance rows at L=8, the zero-cycle count A=68, the cube degree-vector witness, the Tutte, hypergraph and Tait tables, all sampling, mixing, flip-chain and packing numbers.
- The injectivity of recovery was taken from its own referee. I tested only its consequence H_avoid>=M.
- The run went over the ninety minutes by roughly a quarter of an hour.

## Still open

- Whether signs on the incidences of both states can always make every good pair positive. It holds on 5088 roots and I have no proof and no reading of what such a gauge would mean.
- M >= 2^m. No violation up to 16 vertices here.
- A different-model check of the two tube transfers.

## Three best next steps

1. Have a different model rebuild one transfer (say M at width 6) from the text alone and compare matrices or sequences to L=40. That would close "for all L".
2. Open the three literature sources and settle the exponents quoted in BOUNDS.md, including the same-model correction to Proposition 1.4.
3. Look at the two-state gauge. Either find a rule for the signs g' and g that works for every root, which would be a positive formula for the number of good states, or find a counterexample at 17 or 18 vertices.

## Leads for others

- `proofs/involutions/INVOLUTIONS.md` calls the exponent (n-m)/2 refuted. That is true for the note's sign and false for epsilon. A reader comparing it with the probabilistic folder will be confused. One clarifying sentence there would help.
- The paper can derive "at least six Hamiltonian cycles" from Corollary 7.1 and Thomason's parity alone.
