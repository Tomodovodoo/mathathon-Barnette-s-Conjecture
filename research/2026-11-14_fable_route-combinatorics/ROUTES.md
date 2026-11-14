# Routes tried for Proposition 5.1

Target: if the rooted Eulerian triangulation has a pair of disjoint states, some pair `(r, s)` has `Q_s` a forest.

Each route has a status, the evidence, and the lesson. Predictions were written down before the runs and are quoted as made. "Up to 16 vertices" means all 7868 rooted triangulations `(T, t0)` with `|V(T)| <= 16`, of which 5088 have a pair. Commands are in `lab/README.md`. Counterexamples are printed in full in `data/counterexamples.txt`.

## Summary

| # | Route | Status |
| --- | --- | --- |
| 1 | Heights as test functions, two families of cubes | `PROVED-HERE` (PROOF.md, Sections 1 to 3) |
| 2 | Cancellation as an incidence determinant | `PROVED-HERE`, `COMPUTED` |
| 3 | Whole sum as a determinant coefficient, Fourier expansion | formulas `PROVED-HERE`; nonvanishing not obtained |
| 4 | Highest or lowest partnered state is a tree matching | `REFUTED` at 12 and 14 vertices |
| 5 | Minimal cycle cover, all cycles one way | `REFUTED` at 12 and 13 vertices |
| 6 | Pair with the largest rank difference | `REFUTED` at 12 vertices |
| 7 | Every cycle cover has an orientation that is a forest pair | `REFUTED` at 16 vertices, true up to 15 |
| 8 | Parity and mod 4 counts with no weights | gives identities, no existence |
| 9 | Tree matchings split into cubes of dimension `cmin` | `REFUTED` at 14 vertices |
| 10 | Sign of a tree matching is the parity of its rank | `REFUTED` at 8 vertices |
| 11 | Lower bound on the number of tree matchings | `>= 2 cmin` `PROVED-HERE`; `>= 2^cmin` `CONJECTURE` |
| 12 | Tree matchings as the partnered states of Hamiltonian cycles | `PROVED-HERE`, `COMPUTED` |
| 13 | A single cycle always suffices (`cmin = 1`) | `REFUTED` at 9 vertices |

## 1. Heights as test functions

`PROVED-HERE`, PROOF.md Sections 1 to 3.

The set of pairs is cut into cubes in two ways. Pairs with the same undirected `D` form a cube of dimension `c(D)`. Partners of a fixed `s` form a cube of dimension `k(s)`, the number of cycles of `Q_s`. The sign `eps` alternates on both. Summing `eps(r, s) F(s)` over the second kind of cube leaves the tree matchings, for any `F`. Summing over the first kind gives a `c(D)`-fold difference of `F` in the directions "indicator of the inside of a cycle". For `F` a product of `m = cmin` heights at white faces, only cubes with exactly `m` cycles survive and each contributes a count with the same sign.

Lesson. The spoke circulation of the OpenAI paper is a height function in disguise: `omega(s)` is the volume under the height of `s`, and `L+(C) - L-(C)` is the number of white faces inside `C`, which is `B + 1` by the disk identity. The exponential, the integer polynomial and the token lists are three ways to test the same signed measure against a function of degree `m` in the heights. Nothing in the argument is analytic.

## 2. Cancellation as an incidence determinant

`PROVED-HERE`, PROOF.md Proposition 5. `COMPUTED`: `lab/dets.py 12`, D1.

For fixed `s` the signed sum over partners is `sigma det N_s`, where `N_s` has entries `zeta^(+1 or -1)` at the two ends of each edge of `Q_s`. After multiplying column `x` by `omega3^col(x)`, with `col` the vertex 3-colouring, `N_s` becomes the ordinary incidence matrix of `Q_s` with the root columns deleted. Its determinant is `0` when `Q_s` has a cycle and `+1` or `-1` when `Q_s` is a rooted forest.

Lesson. The phase `i^J` is not mysterious. It is the Leibniz sign of an incidence determinant, written in a gauge where the 3-colouring has been absorbed. Lemma 5.2 of the OpenAI paper is "rows of an incidence matrix around a cycle are dependent".

## 3. Determinant coefficient and Fourier expansion

Formulas `PROVED-HERE` (PROOF.md Section 4), `COMPUTED` (`lab/dets.py 12`, D2 and D3).

The full sum is the coefficient of `x_1 ... x_n` in the determinant of a Hermitian adjacency matrix of `T - R` with phases `zeta^delta` and one variable per black face. It is also `3^(-n/2) sum_S (-1)^|S| conj(chi_S) chi_S(g)`, where `chi_S` are character sums over states.

Prediction before working it out: a determinant formula would give nonvanishing by a positivity argument. Outcome: no. Each block `M_t` is Hermitian of signature `(1, 1, 0)`, so the mixed discriminant is an alternating sum of squares, and at `g = 1` it is zero.

Lesson. The determinant structure explains the cancellation and does not replace the planar positivity. The side remark in PROOF.md Section 4 shows why: without injectivity of `s` the statement is trivial, and injectivity is exactly what stops the sum from being a single determinant.

## 4. Highest or lowest partnered state

`REFUTED`. `COMPUTED`: `lab/survey.py 16`, lines E1, E1b, E1c.

Prediction: "probably false, perhaps 35% that the highest partnered state is always a tree matching".

Up to 12 vertices the lowest partnered state was a tree matching in all 208 cases and the highest failed twice. At 14 vertices the lowest fails as well.

- Highest fails at 12 vertices, class 6, `t0 = (2, 7, 3)`. The top partnered state has rank 3 and `Q_s` contains the triangle `4, 5, 10`. The eight tree matchings have ranks `-1, 0, 1, 1, 1, 2, 2, 2`.
- Lowest fails at 14 vertices, class 21, `t0 = (4, 10, 5)`. The bottom partnered state has rank `-2` and `Q_s` contains the triangle `7, 13, 6`.

Totals up to 16 vertices: the highest fails in 95 of 5088 cases, the lowest in 56.

Lesson. For an extreme `s`, every partner gives a `D` with all cycles one way. Reversing a cycle of `Q_s` changes the number of cycles of `D` by two, and nothing forbids that. The topological analysis I tried before computing found no contradiction, and there is none.

## 5. Minimal cycle cover with all cycles one way

`REFUTED`. `COMPUTED`: `lab/survey.py 16`, lines E2, E2b, E2c.

Candidates: take `D` with `cmin` cycles and orient all cycles counterclockwise (or all clockwise). All counterclockwise fails in 163 cases, first at 12 vertices, class 6, `t0 = (2, 7, 3)`. All clockwise fails in 119 cases, first at 13 vertices, class 6, face 6.

Lesson. The leading coefficient of the proof is a sum over all minimal `D`, and it does not single out an orientation.

## 6. Largest rank difference

`REFUTED`. `COMPUTED`: `lab/survey.py 16`, lines E5, E5b.

If `(r, s)` maximises `omega(s) - omega(r)`, every cycle of `Q_s` is counterclockwise. `PROVED-HERE`: reversing a clockwise cycle `K` of `Q_s` replaces `r` by `r'` whose height is lower by one on the white faces inside `K`, which would increase the difference. That is not enough. The pair fails to be a forest pair in 101 cases, first at 12 vertices, class 6, `t0 = (2, 7, 3)`.

## 7. Every cycle cover contains a forest pair

`REFUTED` at 16 vertices. `COMPUTED`: `lab/survey.py 16`, line E3.

Statement: for every undirected `D`, one of its `2^c(D)` orientations is a forest pair. I did not predict this one. It appeared in the data, held for all 1794 rooted triangulations with a pair up to 15 vertices, and I spent some time on a proof for a single cycle.

Counterexample: 16 vertices, class 158, `t0 = (2, 7, 3)`, `n = 13`. The cover `D` is the single cycle `0, 4, 9, 8, 14, 13, 12, 15, 10, 11, 6, 5, 1` with 6 white faces inside. Counterclockwise, `Q_s` contains the triangle `4, 5, 10`. Clockwise, `Q_s` contains the triangle `9, 13, 10`. This rooted triangulation has 12 tree matchings, all in the two other cycle covers. It is the only failure among 5088.

Lesson. There is no proof that works inside one cube of `D`. The cancellation between different cycle covers is needed, even when a Hamiltonian cycle cover exists. A statement that survives 1794 cases can still be false.

## 8. Counting with no weights

No existence proof. The identities are `PROVED-HERE` in two lines each and `COMPUTED` (`data/rows_v16.json`, zero failures).

- The number of pairs is `sum_D 2^c(D) = sum_s 2^k(s)`, the sum over partnered `s`.
- The signed count of all pairs is zero from both sides. So the weight-free signed count says `0 = 0`. It shows that tree matchings of the two signs are equally many, and nothing about existence.
- Modulo 4, with `tau+` the number of tree matchings of sign `+1`: `tau+ + #{s : k(s) = 1} = #{D : c(D) = 1}` modulo 2.
- `c(D) = n` modulo 2 for every `D`, so `cmin = n` modulo 2.

Lesson. Any function of `s` alone can be used as a weight, and nothing else can, because the first cancellation must fix `s`. A constant weight gives zero. The lowest degree at which something survives is `cmin`, and there the answer is a count of cycle covers. A count modulo a prime would have to be nonzero for a reason, and I found none simpler than the positivity in route 1.

## 9. Cubes of tree matchings

`REFUTED`. `COMPUTED`: `lab/zpoly.py 15`, line Z1.

The number of tree matchings equals `2^cmin` in 4609 of 5088 cases. That suggested that tree matchings come in cubes of dimension `cmin`, which would make `Z(q) / (q - 1)^cmin` a polynomial with coefficients of one sign, `Z(q)` being the sum of `eps(s) q^omega(s)` over tree matchings.

Counterexample: 14 vertices, class 24, face 6. `Z(q) = -1 + 2q + q^5 - 2q^6` after a shift, and `Z / (q - 1) = 1 - q - q^2 - q^3 - q^4 - 2q^5`. The quotient has mixed signs in 8 of 1794 cases up to 15 vertices.

## 10. Sign and parity of rank

`REFUTED` at 8 vertices (`lab/survey.py 16`, line E6; fails in 3837 of 5088 cases). If `eps(s)` were `(-1)^omega(s)` up to a constant, then `Z(-1)` would count tree matchings. It is not so.

## 11. How many tree matchings

`PROVED-HERE`: at least `2 cmin` (PROOF.md, Corollary 3). The signed measure kills all polynomials of degree below `cmin` in the rank, and two different multisets of integers with equal power sums up to degree `m - 1` have at least `m` elements each.

`CONJECTURE`: at least `2^cmin`. `COMPUTED` up to 16 vertices with no exception. The observed values are in `DATA.md`. Test: find a rooted triangulation with a pair and fewer than `2^cmin` tree matchings.

Lesson. Instances whose cycle covers need many cycles have more tree matchings, not fewer.

## 12. Hamiltonian cycles and states

`PROVED-HERE`, PROOF.md Proposition 7. `COMPUTED`: `lab/survey.py 16`, lines E8, E8b, E8c.

Every Hamiltonian cycle of `G` avoiding `e0*` defines a state. That state is a tree matching or has no partner. The tree matchings are in bijection with the Hamiltonian cycles whose state has a partner.

Prediction: "the map from tree matchings to cycles is injective and not onto". Both parts held. The dichotomy "tree matching or no partner" was not predicted. It showed up as a column of zeros in the survey, and the proof is an Euler count inside a cycle of the white-face graph.

Lesson. Proposition 5.1 selects a special kind of Hamiltonian cycle. In the data most Hamiltonian cycles are not of this kind (the ratio of cycles avoiding an edge to tree matchings ranges from 1 to 26). A proof that tries to show that an arbitrary Hamiltonian cycle comes from a forest pair is aiming at a false statement.

## 13. One cycle is not always enough

`REFUTED` at 9 vertices. `cmin = 2` for the octahedron with an octahedron glued into a face. Without separating triangles `cmin` still reaches 3 (192 of 3374 rooted cases up to 16 vertices). So the degree of the test function cannot be bounded in advance, and the appendix of Li's note on more than one cycle is needed.

## Routes not tried

- Tutte's trinity. The number of states is `|det K_B|`, which in trinity theory is a number of spanning arborescences. Under such a bijection a pair and a tree matching should have a tree description. I did not work it out.
- Induction on the triangulation by the two generating operations of `lab/tri.py`. The profiles in `DATA.md` change a lot under one operation.
- The exchange graph of the trees paper and the length of the marked walk.
