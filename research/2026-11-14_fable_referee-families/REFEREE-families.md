# Referee report on `2026-11-14_sol_counting-families`

Referee: Claude Fable 5.2, a different model from the author (GPT-6.1 Sol). 14 November 2026.

All checks below use `code/core.py`, written from the OpenAI paper and the glossary. It does not import the laboratory. plantri is used only to list triangulations. Naming follows the glossary: good state, good pair, cover, m. The author's "tree matching", "forest pair", "c_min" are the same objects.

A referee raises the review state and never the tier. PROVED-HERE below means the author's proof, read line by line by me. COMPUTED means my own run, with script and range.

## Verdict table

| # | Claim | Verdict | My range |
|---|---|---|---|
| F1 | Even prisms: S=m, P=M=2, m_cover=1, polynomial z^(m-1)-1, H=2m+2, rail avoided by 2, rung by 2m-2 | CORRECT | proof read; COMPUTED m=2..12, every edge |
| F2 | Tube T(p,L) is a simple Eulerian triangulation without separating triangles | CORRECT | COMPUTED p=4,6,8, L<=6 |
| F3 | Root sweeps of M, width 4 and 6, L<=5 | CORRECT | COMPUTED, identical sets |
| F4 | Width-4 tube: S_L=Fib(2L+3), P=M=2, m=1, polynomial z^(2L+1)-1, H recurrence [2,-1,4] | CORRECT for the range; all L rests on the transfer argument | S to L=20, P,M,m to L=14, polynomial to L=6, H to L=10 |
| F5 | Width-6 tube: recurrences for S, M, P, H; m=1 | CORRECT for the range; all L rests on the transfer argument | S to L=12, M to L=12, P,m to L=9, H to L=6 |
| F6 | Certificate arithmetic (eight integer matrices) | CORRECT | replayed, D+10 consecutive terms each |
| F7 | Edge-avoidance counts at the three root edges | CORRECT | COMPUTED p=4 L<=6, p=6 L<=4 |
| F8 | Good states exponentially rare without separating triangles | CORRECT, conditional on F4 for all L | M/S=2/Fib(2L+3) to L=14 |
| F9 | First octahedral four-subdivision: S=54, P=20, M=12, m=1, H=84, 28 per root edge, the stated polynomial | CORRECT, with a root caveat | COMPUTED all 32 roots |
| F10 | Prism chain: S=3^q, P=M=2^q, m=q, polynomial prod (z^(5j+2)-1) | CORRECT | proof read; COMPUTED q<=5, six gluings |
| F11 | Prism chain: H_1=8, H_q=20*3^(q-2) | CORRECT AFTER FIX | COMPUTED q<=5 |
| F12 | #good = 2^m attained for every m | CORRECT | follows from F10 |
| F13 | H_avoid(e) >= M >= 2m, H >= 3M >= 6m | CORRECT | COMPUTED 1206 roots, V<=14; M>=2m on 5088 roots, V<=16 |
| F14 | H >= (2/N) sum_e max(M_u,M_v) | CORRECT | proof read |
| F15 | H_avoid(e) >= 2^b, H >= 3*2^b >= 6, six is tight | CORRECT | proof read; cube H=6 |
| F16 | No exponential lower bound in N for all Barnette graphs | CORRECT | prisms, H=N/2+2 |
| F17 | Literature comparisons (Florek 2020, Florek 2024, Pivotto and Royle) | NOT CHECKED | sources not held in the project |

## F1. Even prisms

Restatement. The dual of the 2m-prism is the bipyramid over a cycle v_0..v_(p-1), p=2m, with poles N, S. All faces are equivalent, so one root t0=N v_0 v_1 covers every root. Then S=m, P=M=2, the least number of cycles of a cover is 1, the normalised signed polynomial is z^(m-1)-1, H=2m+2, a rail edge is avoided by 2 Hamiltonian cycles and a rung by 2m-2.

Proof check. The black faces are N v_(2i) v_(2i+1) and S v_(2i+1) v_(2i+2). Exactly one southern face takes S, since S must be matched once. With that face fixed the rest is forced along the equator. That gives m states s_0..s_(m-1). Two states differ at northern face i exactly when one index is below i and the other at least i. For this to hold for all i in 1..m-1 the indices are 0 and m-1. So P=2. The single cover is a cycle through all n=2m-1 nonroot vertices. The disk identity with I=0 gives l=(h-3)/2=m-2, B=m-2 and W=m-1, and the two orientations differ in omega by W. This gives z^(m-1)-1. The Hamiltonian count is the standard argument: two used rungs force them adjacent (p cycles), more than two force all rungs and two alternating rail matchings in opposite phase (2 cycles). I found no gap.

COMPUTED. `code/t_families.py`, m=2..12: S, P, M, m, the polynomial, H and the avoidance count of every one of the 3p edges agree. Output `code/out_families.json`.

## F2 to F8. Tubes

Restatement. T(p,L) has rings v(j,i), vertical edges, diagonal v(j,i)v(j+1,i+1) for even i and v(j,i+1)v(j+1,i) for odd i, and two poles. The root is {v(0,0),v(0,1),v(1,1)} for L>=1.

COMPUTED, `code/t_tubes_long.py`, `code/t_families.py`, `code/t_misc.py`.

- The construction is a triangulation with 2-colourable faces. `Inst` asserts both. The number of 3-cycles equals the number of faces for p=4,6,8 and L<=6, so there is no separating triangle.
- Width 4. S by exact determinant equals Fib(2L+3) for L=0..20, including 433494437 at L=20. P=M=2 and the least cover has one cycle for L=0..14. The polynomial is z^(2L+1)-1 for L<=6. H = 6,14,30,70,166,382,878,2038,4726,10926,25278 for L=0..10 and the recurrence [2,-1,4] predicts L=3..10 correctly.
- Width 6. S for L=0..12 and the recurrence [7,-9,7,-1] predicts L=6..12. M by a pruned search for L=0..12: 2,4,12,34,82,194,464,1104,2642,6290,14994,35728,85136, so the order-8 recurrence predicts L=10,11,12 beyond its eight initial values. P = 2,4,16,56,176,544,1696,5312,16640,52096 for L=0..9 and [4,-4,4] predicts L=5..9. The least cover has one cycle for L<=9. H = 8,44,176,752,3200,13568,58112 for L=0..6, so the order-6 recurrence is tested at one value beyond its initial six.
- Avoidance at the three root edges agrees with the table for every row I ran (p=4, L=1..6 and p=6, L=1..4). Two rows of the table, L=8 at each width, were not replayed.
- Root sweeps of M over all facial roots agree exactly: width 4 gives {2} for L<=5, width 6 gives {4}, {12,14}, {34,38,40}, {82,96,98}, {194,230,232,240,242}.
- The width-6 polynomial at L=1 is (1+z)(z^5-1). Polynomials for L=2,3,4 are in `out_families.json` and were not compared coefficient by coefficient with the author's file.

Certificates, `code/t_certs.py`. I read the eight matrices, initial and terminal vectors from the author's JSON and did the multiplication with my own code. Each recurrence holds on D+10 consecutive terms, D the matrix dimension, which by Cayley and Hamilton settles the matrix sequence for all lengths. Each matrix sequence equals my brute-force counts over the whole range above.

What this does and does not show. The matrix sequence satisfies the recurrence for every L. That is arithmetic and I confirm it. That the matrix sequence equals the graph count for every L is the author's transfer argument (FAMILIES section 2, "The exact transfers and why they count"). I read it and found no error in the reasoning. I did not check the transfer code against that prose. So my independent support for "all L" is the agreement on the ranges listed plus the arithmetic. The certification principle in the text is correct as stated.

F8. M/S = 2/Fib(2L+3) is verified to L=14. For all L it inherits the status of F4. The width-4 graphs have no separating triangle, so rarity of good states does not need separators.

One small point. The text says "p(L+1)-p hexagons" and "When p=4 or 6, coincident face sizes must be combined". That is correct and only says that the two p-gons are squares or hexagons at those widths.

## F9. Four-subdivision of the octahedron

COMPUTED, `code/t_chain.py`. V=18, N=32, H=84 and every edge is avoided by 28 cycles. Of the 32 facial roots, 24 have S=54, P=20, M=12, one-cycle least cover and exactly the polynomial printed in FAMILIES. The other 8 roots have M=16 and polynomial 3z^6+z^5-4z^4+4z^2-z-3. The author's numbers are for the root {0,6,7}, which is in the class of 24. The text does not say that M depends on the root here. It should.

The four-subdivided stacked cubes (S=1944, 69984 and so on) were not replayed.

## F10 to F12. The prism chain

Restatement. Glue q hexagonal bipyramids, each into the white face {v_4,v_5,S} of the previous one, keeping the first root N v_0 v_1. Then S=3^q, P=M=2^q, the only cover has q cycles, and the polynomial is the product of z^(5j+2)-1 for j=0..q-1.

Proof check. A new piece brings five new vertices and five new black faces, and new vertices lie only on new faces. So new faces take new vertices, and states, pairs and covers factor over the pieces. Each piece has 3 states, 2 pairs and one cover. The local cycle is S v_2 v_3 v_4 v_5, and the faces inside it are S v_2 v_3 (white), S v_3 v_4 (black), S v_4 v_5 (white). So the outgoing face is inside and the disks nest. Each insertion replaces one white face by six, which adds 5 to every enclosing disk. The areas are 2, 7, ..., 5q-3. Local forests attach at single vertices, so every pair is good. I found no gap. These statements do not depend on how the new cap is identified with {v_4,v_5,S}.

COMPUTED, `code/t_chain.py` and `code/t_chain_perms.py`: for all six identifications and q<=5, S=3^q, P=M=2^q, one cover with q cycles, and the product polynomial.

F11 needs a fix. H does depend on the identification, and the text does not state it. With the same identification at every step I get, for q=1..5:

| New pole N goes to | H | avoidance at the root edges |
|---|---|---|
| S (rung on rung) | 8, 24, 72, 216, 648 | (2,2,4), (6,6,12), then times 3 |
| v_4 | 8, 20, 52, 136, 356 | (2,2,4), (6,4,10), (16,10,26), ... |
| v_5 | 8, 20, 48, 116, 280 | (2,2,4), (4,6,10), (10,14,24), ... |

None of these is 8, 20, 60, 180, 540. The author's graphs, generated by their `stack(6,q)` and counted with my code (`code/t_chain_lab.py`), do give 8, 20, 60, 180, 540 and root avoidance 3^(q-2)(4,6,10). A search over mixed rules shows what they are: the second piece is glued with its pole on v_4 or v_5, and every later piece with its pole on S. All eight such mixed rules give 8, 20, 60, 180.

Fix. Replace "This labeling fixes the gluing permutation" by the rule itself: "the second piece is glued with its pole N on v_4 (or v_5); every later piece is glued with its pole N on the pole S of the previous piece". With that sentence H_1=8 and H_q=20*3^(q-2) is correct. The gluing formula H(A+B) = sum over the three interface edges of H_A(avoid i) H_B(avoid i) is correct and my q=2 values (20 and 24) are what it predicts from the vectors (4,2,2) and (2,2,4). The uniform rule "pole on pole" gives the cleaner family H_q = 8*3^(q-1).

F12 follows from F10: #good = 2^m with m=q for every q>=1. The family has separating triangles.

## F13 to F16. Lower bounds on Hamiltonian cycles

F13. H_avoid(e) >= M for each of the three edges at the root, and H >= 3M, rest on the injectivity of recovery, which another referee checked. I did not re-prove injectivity. COMPUTED consequence, `code/t_misc.py`: on all 1206 roots of the 55 triangulations with at most 14 vertices, H_avoid(e0) >= M for all three root edges and 3M <= H, with no violation. Equality 3M=H occurs at the cube and at five other graphs (plantri 9_0, 12_2, 12_5, 12_6, 12_7), so "only the cube gives equality" is true among prisms and false in general. The text says it only for prisms.

M >= 2m. BOUNDS cites it from another report. I checked it myself. The polynomial F(z) = sum over good states of epsilon z^omega is nonzero, has M/2 terms of each sign, and is divisible by (z-1)^m. So the two multisets of exponents have equal power sums of orders 1..m-1 and are different. By Newton's identities two different multisets of size k cannot agree in their first k power sums, so M/2 >= m. COMPUTED: M >= 2m, and also M >= 2^m, on all 5088 roots with a pair up to 16 vertices (`code/t_census.py 16`).

F14 is correct. Every Hamiltonian cycle omits N/2 edges, so the avoidance counts sum to (N/2)H, and each is at least the larger of the two root counts.

F15 is correct. In each irreducible piece and for each prescription there are at least two good states, hence at least two partitions, and the choices are independent because restriction to a piece recovers the local partition. One remark for the paper: H >= 6 needs less. Every edge is avoided by some Hamiltonian cycle (Corollary 7.1 of the OpenAI paper) and by an even number of them (Thomason's Corollary 1.5, see REFEREE-algebra). So every edge is avoided by at least 2 and the three edges at a vertex give 6. The cube has H=6, confirmed.

F16 is correct. Prisms have H=N/2+2 and no separating triangle in the dual.

## F17. Literature

BOUNDS.md cites Florek (J. Comb. Optim. 39, 2020, Theorem 1), Florek (arXiv:2309.09578v2) and Pivotto and Royle (arXiv:1901.10683v2). `papers/INDEX.md` lists all three as not held. I did not open them in this run. I cannot confirm the exponents 3^ceil(2|P*|/Delta(P*)^2) and 2^k with k=ceil((|B|-2)/(4 Delta(B)-7)), nor the hypotheses. The same-model review opened them and corrects the second attribution (Proposition 1.4, with Delta of the graph induced on big faces). That correction is unverified by a different model.

## What I did not check

The transfer code itself, the stacked-cube subdivisions, the L=8 avoidance rows, L=40 and L=102 values, growth rates and generating functions (these follow from the recurrences by algebra I did not redo), and the three literature sources.
