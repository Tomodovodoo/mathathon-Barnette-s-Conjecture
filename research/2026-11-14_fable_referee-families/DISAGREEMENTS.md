# Where I disagree with the same-model review

The earlier review is `research/2026-11-14_sol_referee-covers/` (REFEREE-families.md, REFEREE-probabilistic.md, INTEGRATION.md), written by GPT-6.1 Sol, the model that wrote the work. I read it after fixing my own verdicts. The algebra folder had no earlier review, so there is nothing to compare for it.

On the numbers we agree everywhere I ran: every table entry I replayed is the same. The disagreements are about status, wording and three details.

## 1. Tube recurrences "for every length"

The earlier review says PROVED-HERE for all L, on the ground that it rebuilt the transfers and checked the recurrences by Cayley and Hamilton. I confirm the arithmetic on the author's matrices and I confirm the sequences by brute force on finite ranges (REFEREE-families F4 to F6). I do not confirm, as a different model, that the matrices count the graph objects for all L. Both transfer implementations come from one model. The prose argument for the transfers looks right to me, and I did not check code against it.

Status I recommend: the recurrences are PROVED-HERE by the author with a same-model referee, and COMPUTED by a different model for S to L=20 (width 4) and L=12 (width 6), M to L=14 and L=12, P and the least cover to L=14 and L=9, H to L=10 and L=6. The earlier INTEGRATION sentence "PROVED-HERE with independent finite certificates" should not use the word independent.

## 2. The prism chain's Hamiltonian count

The earlier review says CORRECT "for the submitted gluing permutation" and notes that another permutation gives 8, 24, 72, 216. I say CORRECT AFTER FIX. The text of FAMILIES does not determine the permutation, and "the submitted permutation" is not one permutation: the author's graphs use one identification for the second piece (pole on v_4 or v_5) and another for all later pieces (pole on S). With one identification throughout, the possible sequences are 8, 24, 72, 216, 648 and 8, 20, 52, 136, 356 and 8, 20, 48, 116, 280. The sequence 8, 20, 60, 180, 540 arises only from the mixed rule. A paper cannot cite "the submitted gluing". INTEGRATION gives a wording that states the rule, and offers the uniform family H_q = 8*3^(q-1) as the cleaner statement.

## 3. The six-cycle counterexample has a mislabelled vertex

The earlier review says CORRECT. The text names the deficit coordinates "A0 and B1" and transfers "from A2 to B1". The deficit coordinates are A0 and B0. The argument works after the replacement. This is a typo, and a referee should have caught it.

## 4. First nonreal zero

The earlier review repeats the author's example at 10 vertices without a minimality claim. Over all roots the first nonreal zeros are at 9 vertices: plantri 9_0, root {1,2,7}, (z-1)^2(z+1)(z^2+1). Not an error in either document, since the author's scan used one root per graph and says so. The paper should quote the 9-vertex case or avoid "first".

## 5. The mean obstruction

No disagreement with the packing referee, who is a third model: correct and narrow. I disagree with the wording of the earlier INTEGRATION, which presents it as a result about the route ("cannot fit the prescribed tree degrees in expectation"). The content is that d* lies on a face of the degree polytope. See REFEREE-probabilistic P2.

## 6. Sign of the fixed objects

The earlier review accepts the height-marked walk, as I do. Neither it nor the author mentions that `proofs/involutions/INVOLUTIONS.md` calls the exponent (n-m)/2 refuted. That sentence is about the note's own sign. For epsilon the exponent (n-m)/2 is correct (215 instances). The two documents use different signs, and the integrator should keep them apart.

## 7. The universal six

Both the author and the earlier review derive H >= 6 from the signed count and recovery. That is correct. It also follows from two facts with no counting of good states: every edge is avoided by a Hamiltonian cycle (Corollary 7.1) and by an even number of them (Thomason). I would state it that way in the paper, since it uses less.

## 8. Things the earlier review cleared that I could not check

The literature corrections (Florek's Proposition 1.4 and the ceiling in the 2020 theorem) were made by the same model from sources the project does not hold. I did not open those sources. They stay unverified by a different model.

## 9. Things I add that neither document has

- With signs allowed on the incidences of both states, the gauge equations are solvable on all 5088 roots with a pair up to 16 vertices. The six-state certificate is an obstruction only for signs on the variables of F (REFEREE-algebra A4).
- The four-subdivided octahedron has two root classes, with M=12 on 24 roots and M=16 on 8.
- Equality 3M=H holds at five graphs other than the cube up to 14 vertices.
