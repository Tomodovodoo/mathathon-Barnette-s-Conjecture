# Referee report on `2026-11-14_sol_route-algebra`

Referee: Claude Fable 5.2, a different model from the author (GPT-6.1 Sol). 14 November 2026. Nobody had refereed this folder. Code in `code/`, independent of the laboratory.

Notation. F(w) is the sum over pairs (r,s) of epsilon(r,s) times the product of w_(t,s(t)), with one variable per incidence (t,v). M is the number of good states. The author writes T for M.

## Verdict table

| # | Claim (PROOF section) | Verdict | My range |
|---|---|---|---|
| A1 | F has coefficients 0, 1, -1, support the good states, equally many of each sign, F(1)=0 (1) | CORRECT | 7868 roots, V<=16 |
| A2 | Substituting w_tv = a_t b_v gives 0. Positive rescaling cannot make the signs equal (1) | CORRECT | follows from A1 |
| A3 | Nullstellensatz and binary compression remarks (1) | CORRECT, circular as the author says | proof read |
| A4 | Six-state certificate: no sign gauge on incidence variables makes all coefficients one sign (2) | CORRECT, for that definition of gauge only | same 68 roots as the author, V<=16 |
| A5 | M = N_0, P = sum 2^j N_j, M = P - 2N_1 mod 4, M even, 2^m divides P (2) | CORRECT | M even and 2^m divides P on 5088 roots |
| A6 | Every edge of a cubic bipartite graph is avoided by an even number of Hamiltonian cycles (2) | CORRECT, source opened | scan of Thomason p. 262 read |
| A7 | A connected cubic bipartite graph has exactly two nowhere-zero Z_3 flows (2) | CORRECT | proof read |
| A8 | Cauchy and Binet formula for M on the opposite-edge graph (3) | CORRECT | proof read |
| A9 | The unsigned good-state polynomial of the cube is not real stable (3) | CORRECT | checked by hand |
| A10 | The local matrices cannot be made positive (4) | CORRECT | proof read |
| A11 | Berezin integral formula for F (5) | CORRECT | common sign of states on 7868 roots |
| A12 | Gaussian determinant-product formula for F (5) | CORRECT | proof read |
| A13 | Constant term of F(w)F(1/w) is M (6) | CORRECT | follows from A1 |
| A14 | No universal nonzero residue of M modulo 2, 3, 4, 5, 7, 11 (ROUTES, TABLES) | CORRECT for 2, 3, 4, 5, 7. Modulus 11 not replayed | same witnesses, V<=16 |
| A15 | M depends on the root (plantri 12_2: 2 and 8) | CORRECT | COMPUTED |
| A16 | Tutte, hypergraph, Tait and Penrose tables | NOT CHECKED | |

## A1 to A3. The sign barrier

Proof check. Fix s. If Q_s has a cycle, reversing a cycle chosen from s alone changes r, keeps the monomial and flips epsilon. If s is good its partner is unique. So the coefficient of the monomial of s is epsilon for good s and 0 otherwise, and distinct states have distinct monomials. Grouping by covers and reversing one cycle gives F(1)=0, so the good states split evenly by sign. Correct. This is the paper's Lemma 5.2 and the first line of its section 5.3, restated for independent variables.

COMPUTED, `code/t_census.py 16`: on each of the 7868 roots of the 297 triangulations with at most 16 vertices, the signed sum over pairs is 0, the good pairs have distinct second states, their number equals the number of good states found by a separate search, M is even and the two signs are balanced.

A2 follows. Under w_tv = a_t b_v every state gives the same monomial, with coefficient F(1)=0. A3 is correct and proves nothing new, as the text says. In the binary compression, the exponent of x_v is 2^i for the one face t_i that takes v, so the state is determined.

## A4. The six-state certificate

Restatement. Take plantri 13_7 with root {0,4,5}. It has six good states. Every incidence (t,v) occurs in an even number of them, and the product of their six coefficients is -1. Then for no choice of signs g_(t,v) and no global sign do the coefficients of F(g w) all have the same sign.

Proof check. After the substitution the coefficient of state s is c_s times the product of g over the incidences of s. The product of the six new coefficients is the product of the old ones times a product of even powers of the g, so it is -1. Six equal signs have product +1. A global sign contributes its sixth power. Correct.

COMPUTED, two ways. By hand from the author's saved states: the ten columns of the six state vectors each contain every value an even number of times, and the signs are -,+,-,+,+,- with product -1. By my own code: for every root I write one equation over GF(2) per good state, with one unknown per incidence and one for the global sign, and test solvability. On 7868 roots the system is unsolvable at exactly 68 roots. My list of 68 (graph, root, M) is identical to the author's list restricted to the plantri corpus. The first four are the four roots of plantri 13_7 with M=6.

Under exactly what definition of gauge. The statement is about replacing each incidence variable w_(t,v) of the second state by plus or minus itself. That is the natural class if the aim is a positive evaluation F(g) of the polynomial F. Two wider classes behave differently, and the document should say so.

- Signs on the incidences of both states. Multiply the term of (r,s) by a product over faces of g'_(t,r(t)) g_(t,s(t)). COMPUTED: this system is solvable on all 5088 roots with a pair up to 16 vertices, including the 68. So the certificate does not obstruct this class in that range. I have no proof that it is always solvable, and no interpretation of the solutions.
- A sign for each ordered pair of corners of each face. This class contains delta itself, and h_t(a,b) = delta(a,b) makes every term +1. It is trivial and gives the unsigned count of pairs, which is not the object of the proof.

So the correct summary is: no sign change of the variables of F makes F coefficientwise of one sign, on 68 of 7868 roots, first at 13 vertices. Complex gauges on the variables remain untested, as the author says.

## A5 to A7. Parity

A5. A state with a partner has 2^q(s) partners, so P = sum 2^j N_j and M = N_0. Modulo 4 this gives M = P - 2 N_1. M is even by A1. Grouping pairs by covers gives 2^m | P. Correct, and none of it forces M > 0. COMPUTED: M even on all roots, 2^m | P on all 5088 roots with a pair.

A6. The source is held in the author's folder as `Thomason-page262.png`. I read the scan. Corollary 1.5 says: for a cubic graph G, with H the number of Hamiltonian cycles, g(v) the number of (n-1)-cycles not containing v, and h(e,f) the number of Hamiltonian cycles containing two incident edges e and f, one has g(v) = h(e,f) = H modulo 2. The paragraph above it derives Kotzig's theorem for cubic bipartite graphs. The author's deduction is right: a cubic bipartite graph has even order and no odd cycle, so g(v)=0, and the cycles avoiding an edge e at a vertex are the cycles through the other two edges there. COMPUTED: every avoidance count in my prism, tube and chain outputs is even. I did not test evenness on the census.

A7. Orient all edges from one colour class to the other. At each vertex the three values, each +1 or -1 in Z_3, sum to zero only if they are equal. Connectivity makes them equal everywhere. Correct.

## A8 to A10

A8. Cauchy and Binet for B diag(p_t z_v) B^T with B the reduced incidence matrix of the opposite-edge graph after identifying the roots. A minor is 0 or plus or minus 1 and is nonzero exactly for spanning trees. Extracting the squarefree monomial selects a state, and the selected edges form a tree after identification exactly when the state is good. The equivalence is argued correctly in both directions. This criterion is the one `core.py` uses for "good". I did not test it separately against "Q_s is a forest" on pairs. Correct. It is a positive formula that does not show the coefficient is nonzero, as stated.

A9. The cube has two good states and unsigned polynomial abc+def. With a=b=c=exp(i pi/6) and d=e=f=i the value is i + i^3 = 0 and all six variables are in the open upper half plane. Correct.

A10. M_t = S_t D_t with S_t real skew and D_t positive diagonal, so M_t is similar to D^(1/2) S D^(1/2), a real skew matrix. Times i it is Hermitian with trace 0 and rank 2, so one positive and one negative eigenvalue. The product M_uv M_vu = -w_tu w_tv is negative and invariant under diagonal similarity. Correct, for the transformations named.

## A11. The Berezin integral

Restatement. With two species of Grassmann variables and V_t = sum over ordered pairs u != v of corners of t in X of delta(u,v) w_tv (psibar_t psi_u)(chibar_t chi_v), the double Berezin integral of exp(sum V_t) equals F(w).

Proof check. V_t^2 = 0 and the V_t are even, so the exponential is the product of 1+V_t. The integral keeps the terms with one choice (u,v) per face in which the u form a bijection r and the v a bijection s. The restriction u != v is disjointness. The sign of the term is sgn(r) sgn(s), and both species factor because the bilinears are even. What remains is the claim that all states have the same permutation sign. The text cites the trees paper for it. Here is the reason, which I checked: for two states r, s the faces where they differ carry directed edges r(t) to s(t) forming cycles, the disk identity gives each cycle length h = 2l+3, which is odd, so s after r inverse is an even permutation. With that, sgn(r)sgn(s)=1 and the integral is F. Correct.

COMPUTED: on all 7868 roots the number of states equals the absolute value of the determinant of the 0/1 incidence matrix, computed exactly. That is the common-sign statement.

## A12. The Gaussian determinant-product formula

Restatement. For each face t let (xi_t, eta_t) be centred Gaussian vectors indexed by the corners of t, independent over faces, with Cov(xi_tu, eta_tv) = delta(u,v) w_tv for u != v, Cov(xi_tu, eta_tu) = 0, and same-species covariance c_t times the identity with c_t larger than the norm of the cross block. Let K(xi) be the matrix with entry xi_tv at allowed incidences and 0 elsewhere. Then F(w) = E[det K(xi) det K(eta)].

Proof check. The covariance is positive definite for c_t above the norm of C_t, so the Gaussians exist. Expanding both determinants, the expectation of a term factors over faces by independence, and each factor is E[xi_(t,r(t)) eta_(t,s(t))] = C_t[r(t),s(t)], which is 0 when r(t)=s(t). The same-species covariances never enter because each determinant uses one entry per row. So the expectation is the sum over pairs of sgn(r)sgn(s) times the product of delta w, which is F by A11. Correct. The proof in the text goes through the Grassmann form. The direct expansion above is shorter and I recommend it.

Assessment. The formula is the identity F = sum over pairs of sgn(r) sgn(s) prod C_t[r(t),s(t)] written with Gaussian notation. It is exact and it is the same information as A11. It gives no positivity: F(1)=0, so no representation as an expected square can hold for all positive weights, and the author says this. I would not present it as more than a remark.

## A14, A15. Residues and root dependence

COMPUTED, `code/t_census.py 16`. The first roots with M > 0 and M divisible by q:

| q | Witness | M | Author's witness |
|---|---|---|---|
| 2 | plantri 6_0 (octahedron) | 2 | the same |
| 4 | plantri 9_0, root {0,1,6} | 4 | the same graph |
| 3 | plantri 13_7, root {0,4,5} | 6 | the same |
| 5 | plantri 14_7, root {0,2,3} | 10 | M values 2, 8, 10 in TABLES |
| 7 | plantri 16_27, root {5,13,14} | 14 | the same graph, T=14 |

No root with M divisible by 11 or 13 exists up to 16 vertices. The author's witness for 11 is the truncated cuboctahedron with M=22 at one root. I did not build that graph, so modulus 11 is not replayed.

The sets of M over all roots agree with TABLES for the graphs I compared: 6_0 {2}, 8_0 {2}, 9_0 {0,4}, 12_2 {2,8}, 13_7 {4,6,8}, 14_7 {2,8,10}, 14_22 {8}. So M is not an invariant of the unrooted triangulation (A15).

One more observation from the census. On all 5088 roots with a pair, M >= 2^m. This is the open conjecture and not a claim of this folder.

## What I did not check

The Tutte and hypergraph polynomial table, the Tait counts, the Penrose remark, the Hamiltonian totals and avoidance values of TABLES beyond the families in REFEREE-families, the two named larger graphs, and the 17-vertex fixture. Kalman's paper is not held in the project and I did not open it.
