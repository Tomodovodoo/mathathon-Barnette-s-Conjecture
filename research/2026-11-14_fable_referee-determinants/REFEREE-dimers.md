# Referee report on route-dimers (astra)

Refereed: `research/2026-11-14_astra_route-dimers/` (REPORT, PROOF, IDENTITIES, ROUTES, code/).
Referee: Fable, 2026-11-14. Independent code in `code/` (standard library only, own data structures, own spoke weights).

Review state after this report. Every PROVED-HERE statement of PROOF.md sections 1 to 8 is refereed by one independent AI referee, human check pending. They remain T2. The computed rows of IDENTITIES.md are reproduced by an independent implementation on a larger set, with the exceptions listed at the end.

Conventions. As in the brief. `delta(u,v) = +1` when the black face of `uv` is on the left of `u -> v`. `eps(r,s) = prod_t delta(r(t), s(t))`. `w^s = prod_t w_{t,s(t)}`. A tree matching is a state `s` with `H - s` a tree. My census is every Eulerian triangulation with at most 14 vertices (55 graphs from plantri) rooted at every face, plus named examples in both mirror images: 1,246 rooted instances, 13,872 states, 3,428 pairs, 908 instances with a pair, `c_min` equal to 1, 2 and 3 on 572, 178 and 158 of them.

## Summary of verdicts

| # | PROOF.md | Claim | Verdict |
| --- | --- | --- | --- |
| B1 | 1 | Disk identity, with odd length | CORRECT |
| B2 | 1 | All states have one permutation sign, `det K(w) = sigma sum_s w^s` | CORRECT |
| B3 | 2 | `F(w) = [prod y_t] det(sum_t y_t M_t(w)) = sum_pairs eps(r,s) w^s`, and `F = i^n Z` | CORRECT |
| B4 | 2 | Polarization, block Pfaffian, rank at most two | CORRECT |
| B5 | 3 | Doubled extension `F_lambda`, `F_lambda(1) = lambda^n #states`, 9-vertex witness | CORRECT |
| B6 | 4 | Mate count `2^k`, tree matching iff one mate | CORRECT |
| B7 | 4 | `F = sum over tree matchings of +-w^s`, coefficients in {0, 1, -1} | CORRECT |
| B8 | 4 | Coefficient norm counts tree matchings | CORRECT, and it is a restatement, see SIGNIFICANCE.md |
| B9 | 4 | Lowest moment equals a positive sum over minimum-cycle `D` | CORRECT AFTER THE FOLLOWING FIX: say which weights are integers |
| B10 | 5 | Constrained matrix-tree coefficient | CORRECT |
| B11 | 6 | Gauge weights give `Z = 0`, local phase does not factor | CORRECT |
| B12 | 7 | Linear weights `1 + x a_tv` suffice, degree at most `n` | CORRECT |
| B13 | 8 | Normalisation of the doubled complex sum | CORRECT |
| B14 | IDENTITIES | Raw determinant, unconstrained trees, unweighted signed count fail | CORRECT |

## B1. Disk identity

Restatement. Fix a state `r` and one edge out of `r(t)` in each `t` in `A`. A simple directed cycle in the chosen edges avoids the roots, has odd length, and has delta-sum -3 if counterclockwise and +3 if clockwise.

Verdict. CORRECT. The proof is the paper's Lemma 4.1. The three counts are `b + w = 2I + h - 2`, `3(b - w) = 2l - h`, `b = I + l`. Eliminating gives `2l - h = -3`, hence `h` odd. COMPUTED: I decide inside and outside by flood fill of the faces from `t0`, then test the three counts and the sum on 7,076 cycles of pairs and on 7,724 cycles from every outgoing choice of every state when `n <= 7`. No failure, in either mirror.

## B2. Common sign

Restatement. For any two states `r, s` the permutation `s r^-1` of `X` is even. So `det K(w) = sigma sum_s w^s` with one global sign, for arbitrary commuting weights. No hypothesis on separating triangles.

Proof check. CORRECT. On a nontrivial cycle of `s r^-1` every vertex `u = r(t)` has `s(t) != u`, so `r(t) -> s(t)` is an edge of `t`. Completing the choice arbitrarily on the other faces puts the cycle inside one outgoing choice of `r`, and B1 makes it odd. One point the text skips: the cycle has length at least 3 and is a simple closed curve. A 2-cycle `u -> v -> u` would use two different faces that both contain the edge `uv`, and an edge has one black face. With that sentence added the proof is complete.

COMPUTED. Same sign on all 13,872 states, `|det K| = #states` on all 1,246 instances, weighted identity at random integer weights on all of them.

## B3. The mixed determinant

Restatement. For `t` in `A` let `M_t(w)` be the `X` by `X` matrix with `M_t[u,v] = delta(u,v) w_tv` for distinct nonroot corners `u, v` of `t` and zero elsewhere. Then for independent commuting `w_tv`

    F(w) := [prod_t y_t] det(sum_t y_t M_t(w)) = sum over pairs (r,s) of eps(r,s) w^s,

and `eps(r,s) = i^(n + J(r,s))`, so `F(exp(xa)) = i^n Z(x)`.

Proof check. CORRECT. The expansion argument is the one in REFEREE-constructive.md A1. The sign `sgn(s r^-1) = +1` is B2. For the phase, `n` signs with sum `3J` contain `(n - 3J)/2` minus signs, and `(n - 3J)/2 = (n + J)/2 mod 2`. So `eps = (-1)^((n+J)/2) = i^(n+J)`. Note that `J` is an integer for a simpler reason than the disk identity: `delta` is the coboundary mod 3 of the vertex 3-colouring.

COMPUTED. Polarization against pair enumeration at random integer weights, 300 instances, `n` up to 11. `eps = (-1)^((n+J)/2)` on all 3,428 pairs.

Are the two agents' formulas the same? Yes, exactly. PROVED-HERE in SIGNIFICANCE.md section 3. Sol's matrix with entries `q^delta(u,v)` is `-i D^-1 N D` for a diagonal `D` built from the vertex 3-colouring, so `i^n det M_sol = det N` identically in `y` and `w`. COMPUTED on the hexagonal prism: both full `y`-polynomials are `(45/64) y0y1y2y3y4 - (25/64) y0 y1^2 y2 y4 - (5/16) y0^2 y1 y3 y4` at `z = 5/4`. Astra's statement is the stronger one to cite. It has integer entries, allows arbitrary weights, and comes with B7 and the `D`-side expansion. Sol's adds the exact witness polynomial and the remark about self-reduction.

## B4. Polarization, Pfaffian, rank

Verdict. CORRECT. Polarization is A2 of the other report. The block identity `Pf [[0,N],[-N^T,0]] = (-1)^(n(n-1)/2) det N` is standard, I checked it by algebra only. `M_t(w) = M_t(1) diag(w_t.)`, and `M_t(1)` is a skew matrix supported on at most three indices, so the rank is at most 2. The remark that the `M_t` are not positive semidefinite, so mixed-discriminant positivity theorems do not apply, is right and worth keeping.

## B5. Doubling

Restatement. Put `lambda w_tu` on the diagonal entry `(u,u)` of `M_t` for each nonroot corner `u`. Then `F_lambda(w) = sum over all ordered pairs of states of lambda^#{r(t)=s(t)} prod_{r(t)!=s(t)} delta(r(t),s(t)) w^s`, and `F_lambda(1) = lambda^n #states`.

Proof check. CORRECT. Fixed points of the permutation carry a face label too, and the label of a fixed point `u` is a face `t` with `r(t) = s(t) = u`. The sign is `+1` by B2. At `w = 1`, swap `r` and `s` on the nontrivial cycle containing the smallest face. The union of the two matchings does not change, so the rule picks the same cycle again. The product of `delta` is multiplied by `(-1)^h = -1`. Only `r = s` survives.

COMPUTED. `F_lambda(1) = lambda^n #states` for `lambda = 1, 2, 3` on 300 instances. The witness is confirmed: the 9-vertex gluing of two octahedra has 4 states at every root. At the six roots that meet the separating triangle in exactly one vertex it has no pair, no tree matching, and `F_1(1) = 4`. I replayed the stored row `random_9_1` from its edge list and root.

## B6. Mates

Restatement. A state `s` has a mate exactly when every component of `Q_s` is a tree with exactly one root or is unicyclic with no root. With `k` unicyclic components there are `2^k` mates. `H - s` is a tree exactly when there is one mate.

Proof check. CORRECT. Mates of `s` correspond to orientations of `Q_s` with outdegree 1 at nonroots and 0 at roots. A component with `v` vertices and `a` roots then has `v - a` edges, and connectivity forces `a <= 1`. Both cases have the stated orientations. `H - s` is `Q_s` with subdivided edges plus the star at the centre of `t0`, so it is a tree exactly when all three roots lie in different tree components and there is no other component.

COMPUTED. Predicted and enumerated mate counts agree for all 13,872 states. Three criteria for a tree matching agree on every state: one mate, rooted forest `Q_s`, and the duals of the selected spokes form a white spanning tree.

## B7. Forest support

Restatement. `F(w) = sum over tree matchings s of eps(r_s, s) w^s`, with `r_s` the unique mate.

Proof check. CORRECT. For a state with at least two mates, reversing one cycle of `Q_s` chosen from `s` alone changes `r` only and flips `eps`. The author derives the flip from `J -> J +- 2`. A shorter argument: on each face of the cycle `delta(u,s) = -delta(r,s)`, so `eps` is multiplied by `(-1)^h`, and `h` is odd by B1. Distinct states have distinct squarefree monomials, so no further cancellation can occur.

COMPUTED. The coefficient at each of the 13,872 states is `+-1` on tree matchings and 0 elsewhere. Real cancellation (a cyclic `Q_s` with mates) occurs on 22 rooted instances.

## B8. Coefficient norm

Restatement. `#tree matchings = CT_w F(w) F(w^-1) = integral over the torus of |F(e^(i theta))|^2`.

Verdict. CORRECT. Given B7 this is Parseval for a polynomial with coefficients in {0, 1, -1}. COMPUTED on all instances. The author's own caveat is the right reading, proving the norm positive is the same as proving `F != 0`. See SIGNIFICANCE.md section 1.

## B9. Lowest moment

Restatement. Let `a` have positive counterclockwise circulation, `m = c_min`, `A_C = L+(C) - L-(C) > 0`. Then

    sum over tree matchings s of eps_s binom(omega(s), m) = (-1)^((n-m)/2) sum over D with c(D) = m of prod_{C in D} A_C,

and the lower binomial moments vanish.

Verdict. CORRECT AFTER THE FOLLOWING FIX. The binomial form needs integer weights, so that `q^omega(s)` is a Laurent polynomial. The proof never says so. Insert "Assume the `a_tv` are integers" before the binomial statement. For real weights only the exponential form `omega^m/m!` makes sense, and the text gives it. The sign bookkeeping is right: a counterclockwise cycle of length `h` has `(h+3)/2` minus signs, a clockwise one `(h-3)/2`, so a group contributes `(-1)^((n-c)/2) prod_C (w^{C+} - w^{C-})`.

COMPUTED. The full identity `F(w) = sum_D (-1)^((n-c(D))/2) prod_C (w^{C+} - w^{C-})` holds at random integer weights on all 1,246 instances. The moment identity holds on all 908 instances with a pair, with my own weights, which differ from the lab's by a gauge. The lowest coefficient is gauge-invariant, and mine equals the stored `leading` on all 18 of the author's rows.

A weakness in the author's test. `explore.py` computes `area` with `abs(...)` around every cycle gap. So that script never tests that `A_C` is positive. Mine does: `A_C >= 1` on every cycle of every `D` group, all 1,246 instances. Fix: drop the `abs` and assert the sign.

## B10. Constrained matrix-tree formula

Restatement. Let `W` have the white triangles as vertices and one edge for each spoke `(t,v)` with `t` in `A`, `v` in `X`, joining the two white triangles across the two sides of `t` at `v`, with weight `p_t z_v w_tv`. Then `[prod_t p_t prod_v z_v] det L_W = sum over tree matchings of w^s` for any reduced Laplacian `L_W`.

Verdict. CORRECT. The matrix-tree theorem holds for multigraphs, the coefficient forces one spoke per face and per nonroot, and tree and cotree duality in `H` turns "the duals form a white tree" into "`H - s` is a tree". The prescribed-degree version on `H` is also right, I checked it by the degree count only.

COMPUTED. Symbolic expansion of the reduced Laplacian in the `2n` label variables, coefficient extracted, on 24 instances with `n <= 5`. For larger `n` I enumerate one nonroot corner per face and test the white tree by union-find, on 1,244 instances. The stored counts are reproduced: octahedron 128, 8, 2. Hexagonal prism dual 2700, 80, 2. All 18 rows of `data.json` agree for both Laplacian determinants.

## B11. Weights that cannot work

Verdict. CORRECT. If `a_tv = alpha_t + beta_v` then `omega` is constant on states and every `D` group sums to zero because each cycle contributes `-i + i`. The local obstruction is A6 of the other report. Checked by proof, not by computation.

## B12. Linear weights

Restatement. `P(x) = F(1 + xa)` is a polynomial of degree at most `n`. If a pair exists, its order of vanishing at 0 is exactly `c_min` and its lowest coefficient is `(-1)^((n-m)/2) sum_{c(D)=m} prod_C A_C`, which also equals `sum over tree matchings of eps_s e_m(a_{t,s(t)} : t in A)`.

Verdict. CORRECT. Degree at most `n` holds because `F` is multilinear with `n` factors per monomial. Each factor `prod(1 + x a_plus) - prod(1 + x a_minus)` vanishes at 0 with derivative `A_C`. The rest is B7 and B9. COMPUTED on all 908 instances with a pair, including 158 with `c_min = 3`. I wrote the resulting proof of Proposition 5.1 out in full in SIGNIFICANCE.md section 2.

## B13. The doubled complex sum

Verdict. CORRECT. With `d` coincidences and `k = n - d` transitions, `i^J = (-i)^k prod delta`, and `(-i)^n i^d = (-i)^k`. So `Ztilde = (-i)^n F_i(exp(xa))` and `Ztilde(0) = #states`. Checked by algebra, and the value at 0 is the `lambda`-identity of B5.

## B14. The refuted shortcuts

- Raw determinant equals `F`. REFUTED, CORRECT. With the lab's weights at `q = 2` my arithmetic gives the `y`-polynomial `6 y0y1y2y3y4 - 4 y0 y1^2 y2 y4 - 2 y0^2 y1 y3 y4`, so 6 against 0. With random weights the two differ as well, see A3 of the other report. The octahedron passes for a structural reason given there.
- `det(K1 + z K2)` counts two matchings. REFUTED, CORRECT. The expansion picks one permutation.
- Nonzero doubled extension implies a tree matching. REFUTED, CORRECT, B5.
- Lowest coefficient equals the unweighted signed tree count. REFUTED, CORRECT. The signed count is `F(1) = 0` whenever `n > 0`. COMPUTED: it is 0 on every instance.
- Tree count equals an unconstrained white Laplacian determinant. REFUTED, CORRECT, B10.
- Trinity arborescence count equals tree-matching count. I confirm 3 states against 2 tree matchings on the hexagonal prism dual. I did not recompute the trinity cofactors, so "all three cofactors equal the number of states" stays LIT plus the author's computation.

## Findings on the evidence

1. Seven of the 18 examples have no pair. On those, every pair identity reads `0 = 0`. Two of the twelve polarization examples are among them. REPORT.md says "18 rooted examples support the formulas". Write "11 with pairs".
2. One example, the 12-vertex one borrowed from sol, has a cyclic `Q_s` with mates. Forest cancellation was tested on that single graph.
3. The `abs` in `explore.py`, see B9.
4. The examples are gluings of octahedra and bipyramids. The author says so. My census replaces them with the complete list up to 14 vertices at every root.
5. The code imports the lab's embedding, states and weights. The author says so too. My implementation shares nothing with the lab, and all 18 stored rows agree with it on states, pairs, tree matchings, `c_min`, both Laplacian determinants, the lowest coefficient and the norm (`code/extra_checks.py`).

## Corrections ready to apply

1. PROOF.md section 1, common sign. After "Each nontrivial cycle of the relative permutation is a simple directed cycle in these choices." add "It has length at least 3, since a 2-cycle would place one edge on two black faces."
2. PROOF.md section 4, moment identity. Before "Then" insert "Assume the `a_tv` are integers for the binomial form."
3. PROOF.md section 4, forest support. Replace the `J` argument by "On each face of the reversed cycle `delta(u,s) = -delta(r,s)`. The cycle has odd length, so `eps` changes sign."
4. REPORT.md first lines. Replace "18 rooted examples" by "18 rooted examples, 11 of them with pairs".
5. `code/explore.py`. Remove `abs` in the computation of `area` and assert each gap is positive.
6. IDENTITIES.md. Add the row "Sol's number-field determinant equals the real mixed determinant identically, PROVED-HERE by the referee, `research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` section 3".
