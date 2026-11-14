# Statements for the paper and the open-problems digestion

Referee: Claude Fable 5.2. These are proposed final wordings. Review state for every PROVED item: proved by GPT-6.1 Sol, checked by one referee of a different model (this report), human check pending. A referee does not raise the tier.

Terms: good state, good pair, cover, m (least number of cycles of a cover), as in the glossary.

## Safe to cite in the paper's remarks

1. Prisms. PROVED.
   "For the prism on 4m vertices (m >= 2) and any root, there are m states, two pairs, both good, and one cover, a single cycle through all nonroot vertices. The signed polynomial is z^(m-1) - 1 up to sign and a monomial. The prism has 2m+2 Hamiltonian cycles. Two of them avoid a given rail edge and 2m-2 avoid a given rung."
   Checked by enumeration for m = 2..12.

2. Good states can be exponentially rare without separating triangles. PROVED by the author's transfer argument, COMPUTED by this referee for L <= 14.
   "In the width-four tube T(4,L), rooted at the lateral face {v(0,0), v(0,1), v(1,1)}, the number of states is the Fibonacci number F(2L+3) and exactly two states are good. The dual has no separating triangle and the primal has only square and hexagonal faces."
   If the paper wants a statement checked by two models, add "for L <= 14".

3. Equality in #good >= 2^m. PROVED.
   "Glue q hexagonal bipyramids, each into the white face {v_4, v_5, S} of the previous one, and keep the root N v_0 v_1 of the first. Whatever the identifications, there are 3^q states, 2^q pairs, all good, and one cover with q cycles. The signed polynomial is the product of z^(5j+2) - 1 for j = 0..q-1. So the number of good states equals 2^m for every m >= 1."
   Checked by enumeration for q <= 5 and all six identifications. The family has separating triangles.

4. Hamiltonian cycles of the chain. COMPUTED by this referee for q <= 5. For all q it rests on the author's 3 by 3 transfer matrix C, which I did not recompute.
   "If every new piece is glued with its pole on the pole S of the previous piece, the primal graph has 8*3^(q-1) Hamiltonian cycles."
   Or, to keep the author's numbers: "If the second piece is glued with its pole on v_4 and every later piece with its pole on S, the number is 8 for q = 1 and 20*3^(q-2) for q >= 2."
   Do not write "the prism chain has 20*3^(q-2) Hamiltonian cycles" without the rule.

5. Lower bounds. PROVED, given the main theorem and the injectivity of recovery.
   "If the root t0 admits a pair, each of the three edges of G at the vertex dual to t0 is avoided by at least M Hamiltonian cycles, where M is the number of good states, and M >= 2m. Hence G has at least 3M >= 6m Hamiltonian cycles."
   "If the dual of G splits along separating triangles into b pieces without separating triangles, every edge of G is avoided by at least 2^b Hamiltonian cycles and G has at least 3*2^b of them."
   Checked on 1206 roots (first sentence) and 5088 roots (M >= 2m).

6. Six cycles. PROVED, and I recommend this shorter derivation.
   "Every Barnette graph has at least six Hamiltonian cycles, and the cube has exactly six. Indeed every edge is avoided by a Hamiltonian cycle, and in a cubic bipartite graph the number of Hamiltonian cycles avoiding a given edge is even (Thomason 1978, Corollary 1.5). Prisms have N/2 + 2 Hamiltonian cycles, so no lower bound that grows exponentially in N holds for all Barnette graphs."
   Thomason's page 262 was read from the scan in the algebra folder.

7. The signed measure. PROVED.
   "Give each pair (r,s) the sign epsilon(r,s) and record its second state. States that are not good receive total sign zero, and each good state receives +1 or -1, with equally many of each. For heights of inner white faces, the positive and the negative good states have the same moments of every total degree below m, and some product of m heights separates them."
   Checked in degree 1 on 2484 roots and degree 2 on 1464 roots.

8. No shortcut through the zeros. COMPUTED, exact.
   "The signed polynomial need not have only real zeros or only zeros of modulus one. At 9 vertices it can equal (z-1)^2 (z+1)(z^2+1), and at 12 vertices (z-1)(z^2+3)."

9. No sign change of variables makes F positive. PROVED for the stated class, COMPUTED witnesses.
   "Let F be the signed sum in one variable per incidence. There is a rooted triangulation with 13 vertices for which no replacement of the variables by plus or minus themselves, and no global sign, makes all coefficients of F have one sign. Its six good states use every incidence an even number of times and the product of their signs is -1."
   Add the scope: "This concerns signs on the variables of F only."

10. Algebraic forms of F. PROVED. Use as remarks, not as results.
    "All states have the same sign as permutations, because two states differ along cycles of odd length. Hence F(w) is the sum over pairs of sgn(r) sgn(s) times the product of delta(r(t),s(t)) w_(t,s(t)), which can be written as a Berezin integral with one quartic term per black face, or as the expectation E[det K(xi) det K(eta)] for Gaussian matrices with cross-covariance delta(u,v) w_tv in each face."
    Say that neither form gives positivity, since F(1) = 0.

11. Height-marked walk. PROVED.
    "Marking a pair with one integer for each of m fixed white faces, bounded by the shifted height of that face, gives a third form of the two-involution walk. Its second involution needs only the rule 'reverse the first cycle that holds no token'. It is the same proof as in the involution note, with a different marking, and it has no running-time bound."
    In the epsilon sign its fixed objects have sign (-1)^((n-m)/2). Do not merge this with the sign formula of the involution note.

## Must stay labelled computed

- Width-six tube recurrences for S, M, P, H and "m = 1 for all L". A different model has checked S to L=12, M to L=12, P and the least cover to L=9, H to L=6, and the arithmetic of the certificates. The all-L statement is the author's.
- Width-four Hamiltonian recurrence H_L = 2H_(L-1) - H_(L-2) + 4H_(L-3): checked to L=10.
- Growth rates and generating functions derived from those recurrences.
- Root sweeps of M on tubes (L <= 5) and the two root classes of the subdivided octahedron.
- "68 of 7868 roots up to 16 vertices have no sign gauge", and "signs on the incidences of both states always suffice up to 16 vertices". The second has no proof.
- Residue witnesses: M can be 0 modulo 2, 3, 4, 5, 7 (checked). Modulo 11 is the author's computation on the truncated cuboctahedron, not replayed.
- The linear-weight polynomial F(1+xa) having nonreal zeros. It depends on the choice of weights. With my weights it fails at 10 vertices.
- Every sampling, mixing and flip-chain number in the probabilistic folder.

## Must stay labelled conjectural

- M >= 2^m for every root with a pair. No violation on 5088 roots up to 16 vertices in my census. Equality for every m by item 3.
- Whether m can be unbounded without separating triangles in a family with bounded face sizes.
- Whether signs on the incidences of both states can always make all good pairs positive.

## Do not cite

- "Finite positive weights cannot fit the target mean" as an obstruction to probabilistic proofs. If it appears at all, write: "The target degree vector has full degree at the roots and at the outer centre, so it lies on a face of the degree polytope, and only spanning-tree laws supported on that face can have it as their mean."
- The comparisons with Florek and with Pivotto and Royle in BOUNDS.md, until someone opens the sources. They are not held in the project and I did not open them.
- "Only the cube gives 3M = H" outside the prism family. Five other graphs up to 14 vertices do.

## Corrections to apply in the source folders

- `2026-11-14_sol_counting-families/FAMILIES.md` section 4: state the gluing rule (item 4).
- `2026-11-14_sol_counting-families/FAMILIES.md` section 3: say that the numbers for the subdivided octahedron are for the root {0,6,7}, and that 8 of the 32 roots have M=16.
- `2026-11-14_sol_route-probabilistic/PROOFS.md` section 4: replace B1 by B0 in "The only deficit coordinates are A0 and B1" and in "from A2 to B1".
- `2026-11-14_sol_route-probabilistic/ROUTES.md`: the first nonreal zeros over all roots are at 9 vertices.
- `2026-11-14_sol_route-algebra/ROUTES.md`: add the scope of the gauge obstruction (item 9).
