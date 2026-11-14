# Experiments

Every output is COMPUTED, T4, unreviewed. Exact enumeration is distinguished from floating-point calculations. Commands are in code/README.md. Only one process ran at a time. The longest run was the 14-instance sampler, about 47 seconds. No job remains running.

## Exact worked examples

The lab's integer spoke circulation is used throughout. Its sign convention is epsilon. Histograms below give counts of ordered pairs by sign and height omega, so multiplying each histogram by z^omega reconstructs the two positive pieces. Height here is the scalar sum of lab incidence weights, not an individual white-face height.

| Example | S | Ordered pairs | Tree states | c_min | Uniform-H UST success |
| --- | ---: | ---: | ---: | ---: | --- |
| Cube | 2 | 2 | 2 | 1 | 1/64 |
| Hexagonal prism | 3 | 2 | 2 | 1 | 1/1350 |
| Reconstructed 13-vertex candidate | 12 | 8 | 6 | 2 | See exact.json |
| Bad-cover 16-vertex example | 26 | 18 | 12 | 1 | See exact.json |

Cube positive heights {0:1}, negative {1:1}. Its signed sum is 1-z.

Hexagonal prism positive {3:1}, negative {1:1}. Its signed sum is z^3-z. The third state has no partner and Q acyclic. It cannot enter the signed count.

13-vertex candidate positive {0:1,1:1,5:1,7:1}, negative {1:1,2:1,4:1,6:1}. The repeated height 1 cancels between different pairs. The normalized polynomial is (z-1)^2(z^2+z+1)(z^3+z+1). It has off-circle roots as well as the double zero at 1. The 8 pair terms leave 6 distinct forest monomials.

Bad-cover16 positive {4:1,5:1,6:1,7:1,8:2,9:2,10:1}, negative {4:1,5:2,6:2,7:1,8:1,9:1,10:1}. The normalized polynomial is (z-1)(z+1)(z^2+z+1). Cancellation can lower both the number of monomials and the univariate support. The saved bad cover has one cycle and neither orientation forest, while the instance has 12 forest states. It was reconstructed from the structure referee's fable16.json, matching its totals.

Source limitation. paper/figures/example.json does not exist in this checkout. The figure code expects missing JSON input files. I reconstructed the 13-vertex candidate from the first record in research/2026-11-14_fable_figures-review/search_example.json, using its face t0=4. This is explicitly a candidate, not a claim of byte-for-byte identity to the unavailable input. Its counts agree with the candidate search file. All input paths are encoded in code/explore.py.

## Fractional tests and the joint exchange obstruction

code/campaign.py scan checks one root on every plantri triangulation at V=6,...,14, 55 cases. code/half16.py checks roots 0 and 1 at V=16, 370 cases. These are not all roots. For every undirected pair support, all nonempty subsets of white vertices satisfy mass(S)<=|S|-1 for x=1/2 on that support. Cases without pairs are vacuous and must not be counted as positive witnesses. data/scan.json and data/half16.json retain the pair counts.

code/packing.py finds and checks an explicit partition into two trees in 27 further instances, through dual order 120. Families include width 4,6,8,10 tubes at lengths 2,5,10, two subdivisions, prism chains and ten seeded random recursive sums. Only the maximum-flow pair was tested on each larger instance. These are certificates of fractional target feasibility in the tested cases, not certificates of a doubly rainbow tree.

code/secondary.py also solves the edge-marginal mixture LP explicitly on cube and hexagonal prism pair supports. The tree lists and mixture weights are in data/lp.json. The target is feasible there despite finite-positive full-H mean fitting being impossible. No general LP integrality claim follows.

code/campaign.py independently enumerates the cube spoke graph's 220 possible three-edge deletions and finds 128 spanning trees. It detects a joint M-convex exchange failure. The lab's exact Laplacian determinant independently gives 128. This cross-check is internal to one author; no T3 promotion.

## Zeros

code/secondary.py scans all 55 unrooted plantri inputs at V<=14 with outer face 0 and nonempty pairs. It computes exact z-polynomials and exact linear substitution polynomials. Floating approximations select counterexamples; their displayed integer factors certify the actual failures.

The first nonreal z roots in this scan are at V=10, with normalized 1-z^3. The first off-circle roots are at V=12 index 2, with normalized (z-1)(z^2+3). The first nonreal roots for F(1+xa) are at V=12 index 0, with polynomial x(x+1)(2x+1)(2x^2+5x+4). These minimality statements concern this root choice and this weight construction. They are not all-root or all-gauge minimality results.

The origin of the exponential parameter is z=1 after z=exp(x). An additional monomial factor z^a from gauge shifts is removed before discussing the other roots. Prisms give z^(m-1)-1 and nested sums give products of such factors, as in the counting-family report. Their roots of unity do not extend to general instances. There is no proposed universal interlacing theorem left supported by these tests.

## Sampling and flip chains

code/campaign.py random uses seed 11714 and three kinds of random data: uniform choices among unlabelled plantri V=16 objects followed by a uniform face, recursive random white-face octahedral insertions with the initial root retained, and determinant sampling on a subdivided tube. Two rare deterministic families are controls. This does not sample a uniform distribution on large Eulerian triangulations.

State sampling evaluates determinant self-reduction with numpy inverses. The exact common-sign determinant formula motivates the conditional probabilities. Every raw probability is checked for nonnegativity within 1e-7 and sums to one within 1e-7; every returned state is validated. Floating arithmetic means this is an approximate uniform sampler, not an exact integer implementation or a perfect-sampling certificate. The integer state total is independently computed from the lab incidence determinant.

| Sample | Dual V | Exact S | TM hits / 160 | Downhill flip successes / 12 |
| --- | ---: | ---: | ---: | ---: |
| Plantri index 40 | 16 | 19 | 13 | 12 |
| Plantri index 126 | 16 | 22 | 53 | 12 |
| Plantri index 58 | 16 | 21 | 12 | 12 |
| Random white sum 0,1,2, separately | 36 | 2048 each | 160 each | 12 each |
| Subdivided width-6 tube | 50 | 1037232 | 1 | 12 |
| Rare width-4 tube L=12 | 54 | 196418 | 0 | 0 |
| Rare prism chain q=8 | 43 | 6561 | 5 | 10 |

The other five plantri samples have no pair by exact flow, so their zero successes diagnose obstructed roots, not an algorithm failure on a feasible instance. Sampled pair-cycle histograms give only upper bounds on c_min, with no bound when no sampled state has a partner. The random white sums have sampled upper bound 11; they illustrate how separating sums can make c_min large while all states are trees. The rare chain upper bound is 8. These are not general random-instance c_min laws.

The downhill chain proposes a uniform white triangle, reverses its alternating six-spoke matching if available, and accepts if cycle rank of Q does not increase. It runs at most 2000 proposals per trial. This preserves states but is not a stationary sampler. Early terminations stop at a tree state. Successful runs do not prove connectivity or a polynomial hitting bound.

A separate uniform lazy flip chain was fully enumerated on width-4 tubes L=1,...,6. At each step it holds with probability 1/2 and otherwise proposes one white face uniformly. The transition matrices are symmetric and stochastic; eigenvalues and hitting times use floating linear algebra. Results in data/mixing.json include a spectral gap about 0.000670 at L=6, with 610 states and two successes. Its mean first hit from a uniform start is about 23119 proposals, counting a start already successful as time zero. Thus even these modest instances distinguish mixing of states from hitting a rare set. No asymptotic mixing theorem is inferred.

## Predictions, failures and open checks

Prediction 1, joint M-convexity fails, was confirmed computationally on the cube and by a separate hand proof on a six-cycle. Prediction 2, full-H mean fitting fails, was proved. Prediction 3, half-pair feasibility, survived all tested cases. Prediction 4, universal real-rootedness fails, was confirmed by exact factors. Prediction 5, unrestricted alternating triangle flips with nonincreasing Q cycle rank reach a tree from every state, survived the 15 named examples; it was not tested exhaustively on the large samples. Those flips allow any three-position change forming a state, which can include nonfacial triangles. The local white-face chain is a narrower move set and has separate results. Prediction 6, cycle penalty misses root defects, was confirmed already by the hexagonal prism; an exponential formula for the zero-cycle bad states remains open.

Independent referee replay is needed for the two-tree packing implementation, degree-vector witness, exact factor scan and sampling move conventions. The height-marked proof needs independent review of token-rank changes across the two involutions.
