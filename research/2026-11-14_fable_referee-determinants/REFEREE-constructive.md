# Referee report on route-constructive (sol) and workings/barnette_lab

Refereed: `research/2026-11-14_sol_route-constructive/` (REPORT, ALGORITHMS, VERIFICATION, DATA) and `workings/barnette_lab/`.
Referee: Fable, 2026-11-14. Independent code in `code/` (standard library only, own data structures).

Review state after this report. The six mathematical claims below are refereed by one independent AI referee, human check pending. They stay at the tier the author gave them. The 77-run campaign is partly refereed, see section 7 for what I did and did not replay.

Conventions I used. `T` is an Eulerian triangulation with root black face `t0`, `A` the other black faces, `X` the nonroot vertices, `n = |A| = |X|`. `delta(u,v) = +1` when the black face of `uv` is on the left of `u -> v`. My code checks every statement in both mirror images of the embedding.

## Summary of verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| A1 | Determinant coefficient formula over Q(zeta_12) | CORRECT. It is the same determinant as astra's real one, see A1 |
| A2 | Inclusion-exclusion extraction with 2^n determinants | CORRECT |
| A3 | Single evaluation fails on the hexagonal prism, exact polynomial | CORRECT, polynomial reproduced exactly |
| A4 | Two-matroid relaxation fails | CORRECT AFTER THE FOLLOWING FIX: the hexagonal prism is already a counterexample |
| A5 | Uniform sampling of states by determinant self-reduction | CORRECT |
| A6 | Local phase does not factor into tail and head scalars | CORRECT |
| A7 | Verification campaign, 77 rooted instances | Numbers reproduced where I replayed them. Three coverage findings, no wrong test |

## A1. Determinant coefficient formula

Restatement. Let `q = exp(i pi/6)`. Let `a(t,v)` be non-negative integers, `y_t` one variable per `t` in `A`. Let `M` be the `X` by `X` matrix with zero diagonal and, for `u != v`, `M_uv = sum over t in A containing u and v of y_t q^delta(u,v) z^a(t,v)`. Then `Z_integer(z) := sum over pairs (r,s) of (-1)^((n+J(r,s))/2) z^omega(s)` equals `i^n [prod_t y_t] det M`. The claim holds for every choice of the exponents `a`, the positive circulation plays no part in it.

Proof check. PROVED-HERE in ALGORITHMS.md, and I agree with every step.

1. A term of `det M` is a permutation `pi` of `X` together with, for each `u`, a face containing `u` and `pi(u)`. Two distinct vertices lie on at most one common black face, so the face is forced by `pi`. Correct.
2. The coefficient of `prod y_t` keeps the terms whose faces are all distinct. Then `r(t) = u`, `s(t) = pi(u)` are two states with `r(t) != s(t)`. Conversely a pair gives one term. Correct.
3. Every cycle of `pi = s r^-1` is a simple directed cycle in outgoing choices of the state `r`. It has length at least 3, because a 2-cycle would put the edge `uv` on two black faces. Lemma 4.1 gives `2l - h = -3`, so `h` is odd and `sgn(pi) = +1`. Correct.
4. The phase is `q^(sum delta) = q^(3J) = i^J`, and `i^n i^J = (-1)^((n+J)/2)` because `J` and `n` have the same parity. Correct.

Numerical check. COMPUTED, `code/referee.py`. The squarefree coefficient equals the pair sum at random integer weights on 300 rooted instances, `n` up to 11, by `2^n` Bareiss determinants, and again by Fraction elimination on 136 of them. The number-field version is checked on the hexagonal prism by exact arithmetic in `Q[x]/(x^4 - x^2 + 1)`, `code/compare_lab.py`.

Addition by the referee. PROVED-HERE, `SIGNIFICANCE.md` section 3. Sol's matrix and astra's real matrix are conjugate up to the scalar `-i`. With `omega = exp(2 pi i/3)` and `c` the proper vertex 3-colouring of `T` normalised by `c(v) - c(u) = delta(u,v) mod 3`,

    q^delta(u,v) = -i * delta(u,v) * omega^(c(v) - c(u)),

so `M_sol = -i D^-1 N D` with `D = diag(omega^c(u))` and `N` the real matrix of astra. Hence `i^n det M_sol = det N` as polynomials in all `y_t` and all weights. The two agents found the same determinant. The number field is a gauge choice and can be dropped.

Correction ready to apply. In ALGORITHMS.md replace "over a fixed algebraic number field" by "over the integers", and add the sentence: "Multiplying row `u` by `omega^c(u)` and column `v` by `omega^-c(v)` turns `q^delta(u,v)` into `-i delta(u,v)`, so the same coefficient is `[prod y_t] det(sum_t y_t M_t)` with the integer matrices of astra's PROOF.md section 2."

## A2. Extraction by inclusion-exclusion

Restatement. `[prod y_t] det M = sum over S subset A of (-1)^(n-|S|) det M(y = 1_S)`.

Verdict. CORRECT. `det M` is homogeneous of degree `n` in `y`. The alternating sum kills every monomial missing a variable. A surviving monomial has `n` variables and degree `n`, so it is `prod y_t`. This is the evaluator I used for the check in A1. It costs `2^n` determinants, as the author says.

## A3. The single-evaluation shortcut fails on the hexagonal prism

Restatement. For the hexagonal prism, with the lab's face order, vertex order and weights, at `z = 5/4`,

    i^5 det M = 5 y0 y1 y4 (-4 y0 y3 - 5 y1 y2 + 9 y2 y3) / 64.

Its squarefree coefficient is 45/64 and its value at `y = 1` is 0.

Verdict. CORRECT. COMPUTED, `code/compare_lab.py`. I read the lab's labels, `delta` and weights as data, built the matrix myself, expanded the determinant by the Leibniz formula with my own number-field arithmetic, and got exactly

    (45/64) y0 y1 y2 y3 y4 - (25/64) y0 y1^2 y2 y4 - (5/16) y0^2 y1 y3 y4.

This is the claimed polynomial. I also confirmed that the lab's weights are a unit circulation. My own routine finds circulation exactly 1 around every bounded spoke face.

Three remarks that sharpen the statement.

1. PROVED-HERE. At weights `w = 1` the unextracted matrix is skew-symmetric, so its determinant is 0 for every odd `n`. The vanishing of the all-ones value is forced there. At the lab's weights it is a coincidence of that gauge. With random integer weights on the hexagonal bipyramid my code gives raw determinant 236782 against `F = -36120`, and four more pairs of unequal values. The refutation does not depend on the weights.
2. PROVED-HERE. On the octahedron the raw determinant equals `F` identically. The three nonroots form a white triangle whose three edges lie on three different black faces, and every fixed-point-free permutation of three points is a 3-cycle along those edges. So every term is squarefree. This explains "the cube happens to agree".
3. COMPUTED. On the dual of the truncated octahedron the raw determinant and `F` differ at all five random weights tried.

## A4. The two-matroid relaxation

Restatement. Take the spokes `(t,v)`, `t` in `A`, `v` in `X`, as ground set. A tree matching is a set of `n` spokes that is independent in the face partition matroid, in the nonroot partition matroid, and whose duals form a spanning tree of the white faces. The claim is that dropping the nonroot partition and intersecting the other two matroids can return a set that is not a state.

Verdict. CORRECT AFTER THE FOLLOWING FIX. The mathematical statement and the truncated octahedron witness are right. I rebuilt the white graph from scratch and confirmed the lab's 11 spokes use each face once, form a white spanning tree, and repeat nonroots 3 and 4. The cyclic 12-vertex witness repeats nonroot 3. The sentence "It succeeds on the cube and hexagonal prism" is misleading, though. Success there is an accident of the augmenting order.

COMPUTED, `code/referee.py` and `code/extra_checks.py`. Number of white spanning trees with one spoke per face, and how many of them are states:

| Triangulation | one spoke per face | states among them | false positives |
| --- | --- | --- | --- |
| octahedron | 2 | 2 | 0 |
| hexagonal bipyramid | 6 | 2 | 4 |
| octagonal bipyramid | 16 | 2 | 14 |
| dual of truncated octahedron | 888 | 4 | 884 |
| cyclic 12-vertex example | 70 | 8 | 62 |

Of the 1,244 rooted instances in `code/results.json` with `n <= 11` (every Eulerian triangulation with at most 14 vertices at every root, plus my named examples), 1,234 have false positives. The ten exceptions are all the octahedron. The relaxation is not close to exact anywhere else.

PROVED-HERE, a description of the false positives. A function `s: A -> X` with `s(t)` a corner of `t` gives a white spanning tree exactly when `Q_s` is a spanning forest with one root in each of its three components. Orienting that forest towards the roots gives a state `r` with `r(t) != s(t)`. Nothing forces `s` to be injective. The proof is the tree and cotree duality used in the paper's section 6.1, which never uses that `s` is a state.

Correction ready to apply. In ALGORITHMS.md replace "It succeeds on the cube and hexagonal prism but fails on" by "On the cube all 2 common bases are states. On the hexagonal prism 4 of the 6 common bases are not states, although the augmenting order used here happens to return a state. It fails on".

## A5. Uniform sampling of states

Restatement. Assume all states have the same permutation sign. Process the faces in a fixed order. At each face choose an unused corner with probability proportional to the absolute value of the determinant of the residual incidence matrix. Then each state has probability `1/M`, `M = |det K|`.

Proof check. CORRECT. The step "every extension determinant term has one common sign because the full extensions do" is right. For a fixed partial matching, the sign of a full state is the sign of the residual permutation times a factor that depends only on the deleted rows and columns and on the partial matching. This is the generalized Laplace expansion of a permutation matrix. So the residual determinant has terms of one sign and its absolute value counts extensions. The conditional probabilities telescope.

COMPUTED. I computed the exact probability of every state with my own determinants. It equals `1/M` for all states of 1,244 rooted instances. The lab's sampler, run with 3,000 seeds, gives chi-square 0.03, 0.17, 19.33 and 3.41 on 1, 2, 15 and 8 degrees of freedom for the cube, hexagonal prism, truncated octahedron and cyclic example.

The dependence on the same-sign lemma is stated by the author. I confirm that lemma independently in REFEREE-dimers.md, B2.

## A6. The local phases do not factor

Restatement. There are no scalars `f(u)`, `g(v)` on the three corners of a triangle with `f(u) g(v) = q^delta(u,v)` for all six ordered pairs.

Verdict. CORRECT. Under a factorisation the two cyclic products `w01 w12 w20` and `w02 w21 w10` are equal. For the phases they are `q^(3 eta)` and `q^(-3 eta)` with `eta = +-1`, ratio `q^(+-6) = -1`. The author's stated scope is right. This kills only the product of two scalar incidence determinants.

## A7. The verification campaign and the test suite

What I replayed. I ran `python -m unittest discover -s workings/barnette_lab/tests -v`. All 9 tests pass. I read `tests/test_proof.py`, `verify.py`, `core.py`, `algorithms.py` and `supplemental.py` in full, and the first half of `li.py`. I did not rerun the 77-run campaign or the benchmarks. I checked that `data/verification.json` holds 77 rows with 1,040 states and 254 pairs, as VERIFICATION.md says.

Spot check of the lab against my implementation. COMPUTED, `code/export_lab.py` and `code/compare_lab.py`, 19 rooted instances. The lab is used only to dump its results as data.

| Instance | states | pairs | tree matchings | J values | c_min |
| --- | --- | --- | --- | --- | --- |
| cube (octahedron) | 2 | 2 | 2 | -1, 1 | 1 |
| hexagonal prism | 3 | 2 | 2 | -1, 1 | 1 |
| truncated octahedron | 16 | 4 | 4 | -1, -1, 1, 1 | 1 |
| truncated cuboctahedron | 384 | 22 | 22 | eleven -1, eleven 1 | 1 |
| cyclic 12-vertex example | 9 | 10 | 8 | -3, four -1, four 1, 3 | 1 |
| double octahedron, 14 roots | 4 | 4 or 0 | 4 or 0 | | 2 or none |

Every number agrees between the two implementations. The sets of states and of tree matchings agree as sets, not only in size. The lab's integer polynomial `Z` is reproduced exactly from its weights by my pair enumeration. For the final cycle, I ran my own recovery from the lab's tree state on the cube, hexagonal prism, truncated octahedron and truncated cuboctahedron. The edge set `P` and the two vertex classes are identical, the lab's dual cycle visits every face once and crosses no edge of `P`, and the 24 cycles returned by `hamiltonian_cycle` for prescribed edges are Hamiltonian in the input graph and avoid the edge.

Does the suite test what VERIFICATION.md says? Mostly yes. I found no test that is wrong and no assertion that is a tautology. Three findings concern coverage.

Finding 1, Lemma 5.2 is exercised on three runs. In `verify()` the line `if b.qcycles(s): assert sum(b.sign(r, s) for r in mates) == 0` passes with an empty sum whenever the cyclic state has no mate. A cyclic `Q_s` with mates occurs in 3 of the 77 runs (`plantri_12_2`, `plantri_14_7`, `plantri_14_8`), two non-tree pairs each. So the cancellation that carries Proposition 5.1 is tested on six pairs. VERIFICATION.md says "Includes actual cyclic second states at 20 primal vertices", which is true but hides how thin this is. My census roots every graph at every face and finds 22 rooted instances with such states, all cancelling. Fix: root at every face in `main()`, and record the number of states with more than one mate in each row.

Finding 2, 18 of the 77 runs have no pair. For these every pair-level check is an empty loop. They do test the equivalence between pairs, tree states and black separators. VERIFICATION.md should say "59 runs with pairs".

Finding 3, uniformity of the sampler has no test. `test_sampling_stays_a_state` compares the set of 100 samples with the set of states on a 3-state instance. The name is honest, but ALGORITHMS.md claims uniformity. Fix: assert that the product of the conditional ratios equals `1/M` for every state, as in `code/referee.py`.

Smaller points.

- All per-lemma checks are plain `assert` statements. DATA.md warns about `-O`. Under `-O` the unit test `test_cube_all_outgoing_choices` would still pass and test nothing but two counts.
- In the disk check, the last assertion follows from the three before it. Orientation is read from the same `sides` table that defines `delta`, so the check cannot see a globally mirrored embedding. This does no harm, every statement is mirror-symmetric, and my code decides inside and outside by flood fill from `t0` and passes in both mirrors (7,076 D cycles, 7,724 cycles from arbitrary outgoing choices).
- The comment in `test_all_cube_incidence_forests_dual_connected`, "duality itself is embedding independent", is false in general. It is harmless here because `H` of the cube is a subdivided `K4` and has one embedding.
- The Lemma 6.1 row describes a check conditional on "forest with a mate". The code conditions on `is_tree(s)`. The stronger mate-count assertion on the lines above covers the stated claim.
- The row for Lemma 5.3 is accurate. The lab's weights pass my own circulation test on all 19 exported instances.

Not refereed. `li.py` and the Li involution counts, the marked walk and its restart fixture, the exchange-walk benchmarks, the growing family, the region bound 3.3, the density bound 3.4, and the plantri provenance. These are outside the determinant brief. Their status stays COMPUTED, unreviewed.
