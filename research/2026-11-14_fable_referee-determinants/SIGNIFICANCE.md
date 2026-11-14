# What these results are worth

Referee's assessment of the determinant and dimer results of sol and astra, for the exposition. Every numbered statement carries a status tag. PROVED-HERE means the proof is written in this file.

Short version. One result changes the exposition: the real-sign polynomial `F` with linear weights gives a proof of Proposition 5.1 with no exponential, no complex number and no Taylor series. It is written out in section 2. The positive coefficient norm does not give a cancellation-free existence proof, section 1 says why. Everything else is a side remark, some of them good ones.

## 1. The coefficient norm is not an existence proof

REFUTED, as a route to existence. The formula is correct (REFEREE-dimers B8):

    #tree matchings = CT F(w) F(1/w) = sum over states s of (coefficient of w^s in F)^2.

Every term on the right is a square, so nothing cancels. But the formula says only that the number of tree matchings is the number of nonzero coefficients of `F`. To get existence you must show one coefficient is nonzero, that is `F != 0`, and the formula gives no handle on that. It is a restatement of "the support of `F` is the set of tree matchings".

The cancellation in the proof does not live where the norm looks. `F` has two expansions.

- Over second states `s`. After Lemma 5.2 the coefficients are 0 or +-1 and distinct `s` have distinct monomials. Nothing cancels here, but nothing shows the sum is non-empty either.
- Over undirected `D`. Each `D` contributes `+-prod_C (w^{C+} - w^{C-})`. These products do cancel against each other when expanded into monomials. COMPUTED: on the 12-vertex cyclic example there are 10 pairs and 8 tree matchings, so two monomials cancel.

Existence comes from comparing the two expansions at lowest order in a good direction, where all `D` terms have one sign. That step is positive but it is on the `D` side. The norm formula is on the `s` side. I see no way to move the positivity across without the comparison, and the comparison is the paper's proof.

A second candidate fails for a different reason. The constrained Laplacian coefficient of astra's PROOF section 5 is a sum of non-negative terms, one per tree matching. Positive terms do not make the sum non-empty. COMPUTED: at the six obstructed roots of the 9-vertex double octahedron the restricted white graph has 360 spanning trees, 16 of them use each face once, and none is a tree matching.

So there is no headline here. The honest statement for the paper is one sentence: tree matchings are exactly the monomials of `F`, and the proof shows `F != 0`.

## 2. Proposition 5.1 as a polynomial identity

This is the result worth adopting. It is astra's section 7 combined with the real sign of section 2, plus two simplifications of mine (the parity argument in Step 1 and the removal of `J`). PROVED-HERE, checked twice, and COMPUTED on 1,246 rooted instances.

Setting. `T`, `t0`, `A`, `X`, states and pairs as in the paper. Assume Lemma 4.1 in this form.

(P) Let `r` be a state and choose in each `t` in `A` an edge directed from `r(t)` to another corner. A simple directed cycle of chosen edges has odd length. Its delta-sum is -3 if it is counterclockwise and +3 if it is clockwise.

For a pair put `eps(r,s) = prod over t in A of delta(r(t), s(t))`, a sign. Take one indeterminate `w_tv` for each `t` in `A` and corner `v`, write `w^s = prod_t w_{t,s(t)}`, and define

    F(w) = sum over pairs (r,s) of eps(r,s) w^s.

Proposition. If a pair exists, `F` is not the zero polynomial, and every monomial `w^s` of `F` has `Q_s` a forest. So some pair has `Q_s` a forest.

Step 1, support. Fix a state `s` with a mate and a cycle in `Q_s`. I claim the coefficient `sum over mates r of eps(r,s)` is zero.

Choose a simple cycle `Z` of `Q_s` by a rule that uses `s` only. For a mate `r` write `u(t)` for the corner of `t` other than `r(t)` and `s(t)`. The edge of `Q_s` in `t` joins `r(t)` and `u(t)`. Orient it from `r(t)` to `u(t)`. The tails `r(t)` are distinct nonroots. `Z` has as many edges as vertices and every edge of `Z` has its tail on `Z`, so every vertex of `Z` is the tail of exactly one edge of `Z`. Hence `Z` is a directed cycle and contains no root.

Define `r'` by `r'(t) = u(t)` on the faces of `Z` and `r'(t) = r(t)` elsewhere. On `Z` the heads are the same set of vertices as the tails, so `r'` is a bijection. Also `r'(t) != s(t)`, so `r'` is a mate of `s`. For `r'` the third corner on a face of `Z` is `r(t)`, and `Z` was chosen from `s` alone, so the same operation sends `r'` back to `r`. It has no fixed point.

Sign. In a black triangle the three directed edges `r -> s`, `s -> u`, `u -> r` run the same way round, so they have equal delta. Therefore `delta(u(t), s(t)) = -delta(r(t), s(t))`, and `eps(r', s) = (-1)^|Z| eps(r, s)`. The cycle `Z` is a directed cycle of edges `r(t) -> u(t)` chosen out of the state `r`, so (P) says `|Z|` is odd. The mates of `s` cancel in pairs.

Step 2, grouping. Group the pairs by the undirected edge set `D = { r(t)s(t) : t in A }`. As in the paper, `D` is a disjoint union of cycles through all of `X`, each face lies on exactly one cycle, and the pairs in a group are the independent orientations of the cycles. Each cycle is a directed cycle of edges chosen out of `r`, so (P) applies. A cycle `C` of length `h` oriented counterclockwise has `h` signs with sum -3, hence `(h+3)/2` minus signs. Oriented clockwise it has `(h-3)/2`. Write `w^{C+}` for the product of `w_{t,head}` over the faces of `C` in the counterclockwise orientation and `w^{C-}` for the clockwise one. The group of `D` sums to

    prod over C of (-1)^((h_C+3)/2) (w^{C+} - w^{C-}).

The lengths add up to `n` and each is odd, so with `c(D)` the number of cycles, `c(D) = n mod 2` and the sign is `(-1)^((n+3c(D))/2) = (-1)^((n-c(D))/2)`. Therefore

    F(w) = sum over D of (-1)^((n-c(D))/2) prod over C in D of (w^{C+} - w^{C-}).        (*)

Step 3, nonvanishing. Take the spoke weights `a(t,v)` of Lemma 5.3. By the detour argument of the paper's section 5.3, `A_C := sum over t in C of (a(t, head+) - a(t, head-)) > 0` for every cycle `C` of every `D`. Substitute `w_tv = 1 + x a(t,v)`. Then

    w^{C+} - w^{C-} = x A_C + x^2 (...),

so the group of `D` is `(-1)^((n-c(D))/2) x^c(D) prod_C A_C` plus higher powers of `x`. Let `m` be the least `c(D)`. The coefficient of `x^m` in `P(x) = F(1 + xa)` is

    (-1)^((n-m)/2) * sum over D with c(D) = m of prod over C in D of A_C,

a sum of positive numbers times one sign. So `P != 0`, so `F != 0`. By Step 1 any monomial `w^s` of `F` has a mate and has `Q_s` without a cycle. This proves the proposition.

Second check of the proof. I reread each step against the following list and tested each numerically.

- Step 1 uses of `r`: injective (distinct tails), `r(t) != s(t)` (tail on the `Q_s` edge), no root is a tail. All three are in the definition of a pair.
- Step 1, the rule choosing `Z` must not depend on `r`. It depends on `Q_s`, which depends on `s` only.
- Step 2, exponent `(h+3)/2` is an integer because `h` is odd. `(n - c)/2` is an integer because `c = n mod 2`.
- Step 2, all groups with the same `c(D)` have the same sign. This is the one place where the value -3 is needed and parity is not enough.
- Step 3, `P` has degree at most `n` because every monomial of `F` has `n` factors.
- COMPUTED, `code/referee.py`. Identity (*) at random integer weights, 1,246 instances. Coefficients of `F` equal to 0 or +-1 with support the tree matchings, 13,872 states. Order of vanishing of `P` equal to `c_min` and lowest coefficient equal to the displayed sum, 908 instances with a pair, `c_min` up to 3. `A_C >= 1` on every cycle, with my own construction of the weights. Flip of `eps` by `(-1)^length` under both reversals, `code/extra_checks.py`.

What this buys against the paper's version.

- The exponential sum `Z(x)`, the phases `i^J`, the integer `J` of (5.1) and the Taylor expansion all go away. What is left is a polynomial with integer coefficients, of degree at most `n` after substitution.
- Lemma 5.2 gets shorter. The paper needs the identity `delta(u,s) - delta(r,s) = 2 delta(r,u)` and then the disk identity to get `J -> J +- 2`. Here the sign flips because an odd number of local signs flip.
- The statement "the two analyses of one sum" becomes literal: (*) and Step 1 are two expansions of one polynomial.
- It is not shorter by much. Lemma 5.3 and the detour argument are still needed, and they are the longest part.

Relation to the other two papers. The three nonvanishing arguments are three ways to probe the same multilinear `F` at the point `w = 1`, where it vanishes to order `c_min`. OpenAI uses `w = exp(xa)`. The constructive paper uses `w = q^a` with integer `a` and reads the lowest coefficient as a count of marked objects. The linear substitution reads it as `sum over pairs of eps(r,s) e_m(a_{t,s(t)})`, that is, as a signed count of pairs with `m` distinct marked faces weighted by `a`. HUNCH: Li's objects with `c_min` distinct intersections are this `e_m` form with unit marks. I did not check Li's appendix B line by line.

## 3. The two determinants are one determinant

PROVED-HERE. Side remark for the proof, useful for anyone computing.

Lemma. There is `c: V(T) -> Z/3` with `c(v) - c(u) = delta(u,v) mod 3` for every directed edge.

Proof. Around a black face, counterclockwise, each edge has the face on its left, so the delta-sum is 3. Around a white face, counterclockwise, each edge has its black face on the right, so the sum is -3. Both vanish mod 3. Every closed walk in a connected plane graph is a sum of face boundaries in the cycle space, and `delta` is antisymmetric, so its sum over every closed walk vanishes mod 3. Define `c(v)` as the delta-sum along any path from a base vertex. This `c` is the proper 3-colouring of the Eulerian triangulation.

Consequence 1. For `delta = +-1` one has `q^delta = -i * delta * omega^delta` with `q = exp(i pi/6)`, `omega = exp(2 pi i/3)`. Check: `-i omega = exp(-i pi/2 + 2 pi i/3) = exp(i pi/6)`, and `i / omega = exp(i pi/2 - 2 pi i/3) = exp(-i pi/6)`. Since `omega^delta(u,v) = omega^(c(v) - c(u))`, sol's matrix is `M_sol = -i D^-1 N D` with `D = diag(omega^c(u))` and `N = sum_t y_t M_t(w)` astra's matrix. So

    i^n det M_sol = det N

identically in the `y_t` and the weights. COMPUTED: entrywise identity on 46 oriented instances, full `y`-polynomials equal on the hexagonal prism.

Consequence 2. `J(r,s)` is an integer because the edges `r(t) -> s(t)` form closed walks. The paper derives (5.1) from Lemma 4.1. That is more than is needed.

## 4. Where the disk identity is used, and how much of it

PROVED-HERE, an observation for the dependency graph. The disk identity enters the paper three times.

| Use | What is needed |
| --- | --- |
| Lemma 5.2, cancellation over `Q_s` cycles | the cycle is odd |
| (5.4) and (5.5), common phase of the minimal groups | the delta-sum is exactly -3 for counterclockwise, +3 for clockwise |
| Lemma 6.2, `P0` is acyclic | the cycle is odd. The proof reaches `2l - h = 0`, which is impossible for odd `h` |

A fourth use appears in the determinant formulas (common permutation sign), again parity only. So parity carries three of the four uses, and the exact value is needed once, to align signs across different `D`. An exposition can state the parity corollary first and save the value 3 for the one step that needs it.

## 5. The rest, ranked

| Result | Source | Verdict | Worth |
| --- | --- | --- | --- |
| Polynomial form of Proposition 5.1 with linear weights | astra 7, this file 2 | CORRECT | Use in the main text |
| Coefficients of `F` are 0, +-1, support = tree matchings | astra 4 | CORRECT | Use in the main text, it is Step 1 |
| Mate count `2^k`, tree matching iff unique mate | astra 4, constructive paper | CORRECT | Use, it ties `Q_s` to the incidence tree |
| Parity is enough except once | this file 4 | PROVED-HERE | Use in the dependency discussion |
| `F` is a squarefree coefficient of an integer determinant | astra 2, sol | CORRECT | A remark. It does not shorten any proof. It names the missing constraint, each face used once |
| Number-field and real determinants coincide | this file 3 | PROVED-HERE | Footnote |
| Raw determinant fails, hexagonal prism polynomial | sol, astra | CORRECT | One line in a "what does not work" paragraph, good regression test |
| Doubled edges make nonvanishing trivial | astra 3, 8 | CORRECT | One line, it explains why disjointness is needed |
| Two-matroid relaxation fails | sol | CORRECT after fix | One line. Smallest witness is the hexagonal prism |
| Constrained matrix-tree coefficient | astra 5 | CORRECT | Remark only, no positivity argument comes with it |
| Coefficient norm counts tree matchings | astra 4 | CORRECT | Restatement, section 1 |
| Uniform sampling of states | sol | CORRECT | Algorithmic remark. Samples states, not tree matchings |
| Scalar gauge weights give `Z = 0`, phases do not factor | astra 6, sol | CORRECT | Remark motivating incidence weights |

One caution about the determinant. The matrices `M_t` are skew times diagonal and are not positive semidefinite, as astra notes. No known positivity theorem for mixed discriminants applies. The determinant formula is a way to compute `F`, with `2^n` determinants, and so far nothing more.
