# Referee report: determinants and dimers

Every refereed claim of sol and astra is CORRECT. Two need a wording fix: sol's two-matroid sentence about the hexagonal prism, and astra's binomial moment (integer weights).
Their two determinant formulas are the same determinant. PROVED-HERE: sol's number-field matrix is `-i` times a diagonal conjugate of astra's integer matrix.
The positive coefficient norm does not give a cancellation-free existence proof. It restates "tree matchings are the monomials of `F`".
The linear-weight polynomial does improve Proposition 5.1. The full proof is in SIGNIFICANCE.md section 2, with real signs and parity only.
COMPUTED with independent code: 1,246 rooted instances, 13,872 states, 3,428 pairs, no failure, and the lab agrees with it on all 19 instances compared.

## What I set out to do

Referee the overlapping PROVED-HERE claims of `2026-11-14_sol_route-constructive` (with `workings/barnette_lab`) and `2026-11-14_astra_route-dimers`. Check each proof line by line, reproduce the numbers with code that shares nothing with theirs, audit the lab's test suite, and say which results matter for the exposition.

## What I established

Verdicts. The claim-by-claim reports are REFEREE-constructive.md (A1 to A7) and REFEREE-dimers.md (B1 to B14). Corrections are listed there in a form that can be pasted.

- CORRECT without change: the determinant coefficient formula in both versions, the `2^n` extraction, the hexagonal-prism polynomial `5 y0 y1 y4 (-4 y0 y3 - 5 y1 y2 + 9 y2 y3)/64` (reproduced exactly with my own number-field arithmetic), uniform sampling by self-reduction, the common sign of all states, the doubled extension and its 9-vertex witness, the mate count, forest support with coefficients 0 and +-1, the coefficient norm, the constrained matrix-tree coefficient, the gauge and factorisation obstructions, linear weights, and all the refuted shortcuts.
- CORRECT AFTER A FIX: sol's two-matroid paragraph. The relaxation already fails on the hexagonal prism, where 4 of the 6 common bases are not states. Astra's binomial moment identity needs "integer weights" stated.
- No GAP and no WRONG verdict.

New in this folder, all PROVED-HERE in SIGNIFICANCE.md.

1. The two determinants coincide identically, through the vertex 3-colouring `c` with `c(v) - c(u) = delta(u,v) mod 3`. The number field can be dropped.
2. In the real-sign form, reversing a `Q_s` cycle or a `D` cycle multiplies the pair sign by `(-1)^length`. So Lemma 5.2, Lemma 6.2 and the permutation sign need only "the cycle is odd". The value 3 of the disk identity is needed once, to align the signs of the minimal `D` groups.
3. A complete proof of Proposition 5.1 as a statement about one integer polynomial `F`, with linear weights. No exponential, no `i^J`, no Taylor series.
4. `J` is an integer because of the 3-colouring. The disk identity is not needed for (5.1).
5. The false positives of the two-matroid relaxation are the corner choices `s` with `Q_s` a rooted spanning forest, injective or not.

COMPUTED. `code/referee.py` runs 28 checks on the octahedron, the hexagonal and octagonal bipyramids, the duals of the truncated octahedron and truncated cuboctahedron, the 12-vertex cyclic example, the double octahedron at all 14 roots (all in both mirrors), and all 55 Eulerian triangulations of order at most 14 at every root. Against the lab: states, pairs, tree matchings, `J` multisets and `c_min` agree on 19 instances, the sets of states and tree matchings agree as sets, and the final Hamiltonian cycle, the edge set `P` and the two induced trees agree on the cube, hexagonal prism, truncated octahedron and truncated cuboctahedron.

Test-suite audit. All 9 lab tests pass. No test is wrong and none is a tautology. Three coverage findings: the Lemma 5.2 cancellation is exercised on 3 of the 77 runs (6 non-tree pairs), 18 of the 77 runs have no pair, and the sampler's uniformity has no test. Astra's examples have the same weakness: 7 of 18 have no pair, one exercises cancellation, and `explore.py` takes `abs` of the cycle gaps so it never tests their sign.

## What failed and why

- REFUTED: the coefficient norm as a cancellation-free route to existence. The norm is positive exactly when `F != 0`, and proving `F != 0` is the paper's argument. The positivity in that argument sits on the `D` side, the norm on the `s` side.
- REFUTED: positivity of the constrained Laplacian terms as a route to existence. At the obstructed roots of the double octahedron there are 360 restricted white trees, 16 with one spoke per face, and no tree matching.
- Not done: I did not rerun sol's 77-run campaign or benchmarks, and did not referee `li.py`, the marked walk, the exchange walks, the bounds (3.3) and (3.4), or astra's trinity cofactors. Those stay COMPUTED, unreviewed.

## Still open

- CONJECTURE: Li's objects with `c_min` distinct marks are the `e_m` reading of the linear-weight coefficient. Test: enumerate Li's objects on an instance with `c_min = 2` and compare the signed count with the coefficient of `x^2` in `F(1 + xa)` for unit marks.
- HUNCH: a determinant or Pfaffian for `F` without coefficient extraction. Nothing here supports or excludes it. The matrices are not positive semidefinite.
- A human check of SIGNIFICANCE.md section 2 before it goes into the paper.

## Three best next steps

1. Rewrite Proposition 5.1 in the paper in the polynomial form of SIGNIFICANCE.md section 2, and state the parity corollary of the disk identity separately.
2. Apply the corrections listed in the two referee reports, and add the every-root loop to `barnette_lab.verify` so that Lemma 5.2 is exercised on more than three runs.
3. Referee the parts I left out, first `li.py`, since the Li involutions are the other candidate for the main-text proof.

## Leads for others

- Dependency graph: the node "disk identity" can split into "odd length" (three uses) and "value 3" (one use).
- Exposition: `F` has two expansions, over tree matchings and over `D`. The proof compares them at lowest order. The three source papers differ only in the substitution used.
- Figures: the hexagonal prism is the smallest example where the raw determinant, the two-matroid relaxation and the state count (3 states, 2 tree matchings) all differ from the truth. It is a good running counterexample.

## Files

REFEREE-constructive.md, REFEREE-dimers.md, SIGNIFICANCE.md, `code/` with README.md, four scripts and their JSON outputs.
