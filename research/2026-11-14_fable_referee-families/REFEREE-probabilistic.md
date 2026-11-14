# Referee report on `2026-11-14_sol_route-probabilistic`

Referee: Claude Fable 5.2, a different model from the author (GPT-6.1 Sol). 14 November 2026. Code in `code/`, independent of the laboratory.

## Verdict table

| # | Claim (PROOFS section) | Verdict | My range |
|---|---|---|---|
| P1 | Pr[deg(T)=d*] = sum over good states of the product of kept weights, over tau_H(w). Uniform case M/tau(H) (1) | CORRECT | tau(H)=128 for the cube, 2700 for the hexagonal prism |
| P2 | No finite positive weighting of H has mean degree d* (2) | CORRECT, and narrow | proof read; H bridgeless on 55 graphs |
| P3 | Mean range of an exponential family is the relative interior of the hull (3) | CORRECT | proof read, standard |
| P4 | Six-cycle counterexample to joint M-convexity (4) | CORRECT AFTER FIX (a mislabelled vertex) | checked by hand |
| P5 | Signed measure: masses M/(2P), moments below m agree (5) | CORRECT | degree 1 on 2484 roots, degree 2 on 1464 roots, V<=16 |
| P6 | Height-marked walk (6) | CORRECT | every marked object of 215 rooted instances |
| P7 | Cycle-rank tilt is bounded by M/A (7) | CORRECT, trivial | proof read; A=68 not replayed |
| P8 | Root-location shortcuts fail (ROUTES, EXPERIMENTS) | CORRECT | all 7868 roots, V<=16 |
| P9 | Sampling, mixing, flip chains, packing runs | NOT CHECKED | |

## P1. What the UST probability counts

H has 2n+4 vertices and 3n+3 spokes. A spanning tree drops n spokes. The target degrees drop one spoke at each bounded centre, none at t0, one at each nonroot vertex, none at roots. So the dropped set is a state, and the complement is a tree exactly when the state is good. The proof is complete.

COMPUTED, `code/t_misc.py`: tau(H)=128 for the cube and 2700 for the hexagonal prism by the matrix-tree theorem in exact arithmetic, and M=2 for both. So the uniform success probabilities are 1/64 and 1/1350, as in EXPERIMENTS.

## P2. The finite-positive-weight mean obstruction

Restatement. For every instance and every assignment of finite positive weights to the spokes of H, the weighted spanning tree T has E deg_T(t0) < 3, and E deg_T(v) < deg_H(v) at each root v. So the mean degree vector is never d*.

Proof check. Every spoke lies on the hexagon around a white face. The hexagon alternates three corners and three centres, all distinct. So no spoke is a bridge, H minus a spoke has a spanning tree, that tree has positive probability, and the spoke's inclusion probability is below 1. Correct.

Decision. I agree with the packing referee (`2026-11-14_opus_two-tree-packing/REFEREE.md` section 3): correct, and narrow. Here is exactly how narrow. The vector d* has the largest possible degree at t0 and at the three roots. A probability law on spanning trees has mean d* only if almost every tree contains all spokes at t0 and at the roots. So the statement is equivalent to "d* lies on a proper face of the degree polytope". It excludes laws that charge at least one tree missing a forced spoke. Laws with full support are of that kind. It excludes nothing else. In particular it says nothing about the spanning-tree law of H with the forced spokes contracted, nor about any law on the face, and it gives no information on whether d* is a degree vector of a tree. The word "obstruction" is too strong for the paper. One sentence is enough, see INTEGRATION.

The same remark applies to PROOFS 3. It is the standard description of exponential families and is correct. It turns "fit the mean" into "d* is in the relative interior of the hull of the tree degree vectors on its face", which is a statement about convex combinations and not about existence of a tree at d*. The author says this.

## P4. The six-cycle counterexample

The cycle is A0 B0 A1 B1 A2 B2. Deleting A0B0 gives degrees a with A0=B0=1. Deleting A2B1 gives b with A2=B1=1. At A2, a exceeds b. The coordinates where a is below b are A0 and B0. The text says "A0 and B1" and then "transferring one unit from A2 to B1". Both should read B0. The argument is unchanged: a transfer to B0 changes the two class sums, and a transfer to A0 leaves the leaves A2 and B0, which are not adjacent, while a tree of a cycle has adjacent leaves. So the exchange axiom fails. Correct after replacing B1 by B0 twice.

The cube witness (220 deletions, 128 trees) agrees with my tau(H)=128. I did not replay the degree-vector search.

## P5. The signed measure

Restatement. Push the uniform signed measure on pairs forward to the second state. The result lambda is supported on good states with atoms of size 1/P, its positive and negative parts each have mass M/(2P), and for heights of inner white faces the two parts have equal moments of every total degree below m and differ on some product of degree m.

Proof check. Fixed-s cancellation kills states that are not good. A good state has one partner. Reversing one cycle of the cover is a sign-reversing involution without fixed points on all pairs, so the total is zero. For the moments, on one cover the height of a white face y is b_y plus the number of counterclockwise cycles around y. A product of fewer heights than cycles, expanded, has in every monomial a cycle variable that does not occur, and summing over that cycle's two orientations gives zero. Correct.

COMPUTED, `code/t_census.py 16`, with my own heights (path cochains of Lemma 5.3, one per inner white face). On every root: the signed sum over pairs is 0, the number of good pairs equals the number of good states, M is even, and the two signs occur M/2 times each (7868 roots, 5088 with a pair). Height increments are 0 or 1 under a counterclockwise turn (asserted in `code/t_walk.py`). First moments sum over pairs of epsilon times eta_y vanish for every inner white face on all 2484 roots with m>=2. Second mixed moments vanish for every pair of faces on all 1464 roots with m>=3. The nonzero degree-m product is confirmed through P6 on 215 instances, 58 of them with m>=2.

The moment statement is a reformulation of "F has a zero of order m in every direction", and the author says so. It is a good way to say it. It is not a new result.

## P6. The height-marked walk

Restatement. Fix m inner white faces w_1..w_m, one inside each cycle of some cover with m cycles. Shift each height so that H_i(s) >= 0 on all states. A marked object is a pair (r,s) with integers k_i in {1..H_i(s)}. The Q-map reverses a cycle of Q_s chosen from s alone. The D-map reads k_i as a token in the ordered pool made of b_i base tokens followed by one token for each counterclockwise cycle around w_i, reverses the first cycle whose token no slot holds, and re-encodes the ranks. Starting at a D-fixed object and alternating Q and D, the walk ends at a marked good pair.

Proof check, line by line.

1. b_i >= 0 because the all-clockwise orientation of the cover is a state and heights were shifted to be nonnegative on states.
2. The Q-map keeps s, hence all H_i(s) and all marks. It reverses epsilon by the disk identity. Its fixed objects are those with Q_s acyclic, which for a pair means s is good.
3. The D-map is an involution. The set of tokens held by the slots does not change when an unheld cycle is reversed, so the same cycle is chosen on the way back. The pools change only by the token of that cycle, which no slot holds, so every held token stays in its pool. It reverses epsilon because J changes by 2.
4. A D-fixed object has every cycle held by some slot. A held cycle token exists only for a counterclockwise cycle. There are m slots and at least m cycles, so the cover has exactly m cycles, all counterclockwise, and the slots hold them bijectively. Then J=-m and epsilon=(-1)^((n-m)/2) for all of them.
5. There is at least one D-fixed object: the chosen cover, all counterclockwise, slot i holding the cycle around w_i.
6. The graph of the two maps has degree at most two. The walk from a D-fixed object is a path. If it ended at another D-fixed object it would have an odd number of edges and the two ends would have opposite signs, which contradicts 4. So it ends at a Q-fixed object.

I found no gap. The pool order must depend only on the cover, which it does.

COMPUTED, `code/t_walk.py 12`. On the cube, the octagonal prism, prism chains q=2,3, width-6 tubes L=1,2,3, and all 208 roots with a pair of the triangulations with at most 12 vertices, I list every marked object and check: both maps land in the object set, both are involutions, both reverse epsilon off their fixed sets, D-fixed objects have m cycles all counterclockwise, all D-fixed objects have sign (-1)^((n-m)/2), the signed count equals the signed count of either fixed set, and every walk from a D-fixed object ends at a good pair. No failure. The longest walk has 6 moves (width-6 tube, L=3).

Is it a correct algorithm? Yes, as a finite procedure. It needs m, a minimum cover, and a lower bound for each height over all states. My code gets the bound by listing all states. The author's text only says "shift by a state-independent integer". A bound that needs no enumeration exists. A state uses each spoke at most once and the path from w_i crosses each spoke at most once, so the height is at most the number of spokes the path crosses in absolute value, and shifting by that number works. With such a shift the object set grows and the walk may get longer, and no running-time bound is claimed or proved.

Relation to `proofs/involutions/`. Both are Garsia and Milne walks built from the same two cancellations. They mark differently.

- The note marks a pair with an unordered set of m distinct crossings (Li's marks). Its second map needs a token-moving rule when every cycle is marked. Its fixed objects are counted by the sum over minimum covers of the product of the numbers of white faces inside the cycles.
- The height-marked walk fixes m white faces once and marks with m ordered integers. Its D-map has one rule only. Its fixed objects are counted by the sum over minimum covers of the number of bijections from slots to cycles with w_i inside its cycle (a permanent of a 0/1 matrix). It evaluates the signed sum of the product eta_(w_1)...eta_(w_m), a mixed coefficient in m separate height variables. The note and the trees paper evaluate the m-th coefficient in one variable.
- It is the trees paper's ordered-token walk with the single weight omega replaced by m heights. So it is a third presentation of the same proof, shorter to state than the note's second map, and it should be described that way.

The signs do not conflict. The note's fixed objects have sign (-1)^floor(m/2) in the note's own sign (floor(J/2) plus marked directions). Here the sign is epsilon and the value is (-1)^((n-m)/2). INVOLUTIONS.md calls "the former exponent (n-m)/2" refuted. That refers to the note's sign. With epsilon the exponent (n-m)/2 is right, and my run confirms it on all 215 instances. An integrator should not copy either formula into the other document.

## P7. Zero-cycle tilts

The bound M/A is immediate. I did not replay A=68 for the width-4 tube at L=4 or A=S=3 for the hexagonal prism.

## P8. Root-location shortcuts

Restatement. The normalised signed polynomial need not have only real zeros, nor only zeros on the unit circle, and F(1+xa) need not have only real zeros.

COMPUTED, `code/t_census.py 16`, all facial roots, my own weights. The signed polynomial in z does not depend on the choice of weights up to a monomial, because two unit circulations differ by a potential and every state uses each face and each nonroot once.

- Nonreal zeros. The first case over all roots is at 9 vertices: plantri 9_0, root {1,2,7}, polynomial z^5-z^4-z+1 = (z-1)^2 (z+1)(z^2+1). The author's "first at V=10, 1-z^3" is the first case in a scan of one root per graph, and is stated as such. The octagonal prism does give z^3-1.
- Zeros off the unit circle. First case at 12 vertices, plantri 12_2, root {0,1,6}: z^3-z^2+3z-3 = (z-1)(z^2+3). This is the author's example.
- The polynomials (z-1)^2(z^2+z+1)(z^3+z+1) and (z-1)(z+1)(z^2+z+1) of EXPERIMENTS occur at 13 and 16 vertices in my census.
- F(1+xa). This polynomial depends on the choice of weights. With mine, plantri 10_1, root {0,3,4}, gives -x(x^2-3x+3), with nonreal zeros. So the refutation holds, already at 10 vertices. I did not reproduce the author's x(x+1)(2x+1)(2x^2+5x+4), which belongs to the laboratory's weights.

All three are exact: the coefficients are integers and the factors can be read off.

## What I did not check

The sampler, the flip chains, the mixing spectra, the packing runs and the half-pair tests (the packing has its own referee), the cube degree-vector witness, the Lorentzian literature (Branden and Huh, Kalman, Borcea, Branden and Liggett are not held in the project and I did not open them).
