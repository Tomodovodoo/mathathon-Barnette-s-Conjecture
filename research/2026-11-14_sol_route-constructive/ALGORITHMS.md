# Algorithms and complexity

## What is executable

COMPUTED. `workings/barnette_lab/barnette_lab` implements integral flow, pruned state enumeration, ordered-token marked walks, random exchange walks, greedy cycle-score walks, determinant state sampling, a two-matroid relaxation, white-tree loop-erased sampling, recovery and recursive separator gluing. `hamiltonian_cycle(g, forbidden)` returns a cyclic list in the input vertex labels. Independent validation checks only the returned cycle and input edges.

LIT. Conditional on the arguments in the supplied papers, the constructive paper Theorem 1.1 gives deterministic polynomial-space search in O(poly(N) 3^(N/4)) time. Its Proposition 6.2 gives O(n^3 M) enumeration, where M=|det K_B| and n=N/2-1. Its Theorem 5.3 gives 2^O(n log n) time and polynomial space for the marked walk. These are upper bounds from the supplied preprint, not complexity conclusions proved by the finite tests.

## Determinants count states, but not the required trees

PROVED-HERE. Assuming the same-sign conclusion of constructive Lemma 6.1, determinants support exact uniform state sampling in polynomial arithmetic time. Fix a partial matching and delete its occupied rows and columns. Every extension determinant term has one common sign because the full extensions do. Thus the absolute residual determinant counts extensions. At each row choose a corner with probability equal to its extension count divided by the current total. The product of these conditional probabilities telescopes to 1/M for each full state. `determinant_sample` implements this argument with exact integer counts.

COMPUTED. The benchmark returned tree states in 319 of 784 determinant-sampled trials. Seeds and sampled instances are fixed. This statistic pools biased small samples and is not a lower bound for an arbitrary instance. A sampled state may have no disjoint mate. The named 48-vertex graph has 384 states but only 22 tree states.

HUNCH. State rejection sampling might work well on some graph families, but a polynomial expected-time guarantee would need an inverse-polynomial lower bound on the tree-state fraction. The supplied proof gives existence, not that bound. An ordinary determinant does not condition on connectivity of the complement.

## A determinant expression with a coefficient bottleneck

PROVED-HERE. The following identity assumes the disk lemma in the supplied paper. Let q=exp(i*pi/6), let y_t be a variable for each bounded black face, and form an n by n matrix indexed by X. Set its diagonal to zero and, for u != v, put

    M_uv(y,z) = sum over black t containing u,v of y_t q^delta(u,v) z^a(t,v).

Then the integer polynomial implemented in this package is

    Z_integer(z) = i^n [product_t y_t] det M(y,z).

Proof. A determinant term chooses a permutation of X. A term surviving the indicated coefficient chooses each black face exactly once. Tails and heads each use X once, so they define disjoint states r and s, with no fixed points because the diagonal is zero. Conversely every disjoint pair supplies one term. Each permutation cycle is a directed cycle supplied by a state, so the disk lemma makes its length odd. The permutation sign is therefore positive. Its q phase is q^(sum delta)=i^J, and multiplication by i^n gives epsilon=(-1)^((n+J)/2). Its remaining monomial is exactly the second-state weight. This proves the identity.

PROVED-HERE. Inclusion-exclusion can extract this squarefree coefficient with 2^n determinant evaluations at y_t in {0,1}. The determinant has homogeneous total y-degree n. Summing evaluations with signs (-1)^(n-|S|) deletes every monomial missing a variable. A surviving monomial has all n variables and total degree n, so every exponent is one. This gives an exponential evaluator, not a polynomial one. The univariate degree in z is at most 6n^2 by the constructive weights, but that does not remove the multivariable extraction.

COMPUTED. `exact_determinant.py` evaluates the hexagonal prism at z=5/4 using exact symbolic arithmetic. With its five faces indexed in A order,

    i^5 det M = 5 y0 y1 y4 (-4 y0 y3 - 5 y1 y2 + 9 y2 y3) / 64.

The squarefree coefficient is 45/64. Setting every y to one gives zero. Repeated-face cycle covers are the extra terms, and they cancel the quantity we wanted. `data/exact_determinant.json` records this witness. The cube happens to agree with the naive determinant, so testing only the cube would have hidden the failure.

PROVED-HERE. A simple product of two scalar weighted incidence determinants cannot encode the local q phases by independent tail and head factors. At a triangle with corners 0,1,2, a separable weight f(u)g(v) would satisfy w01*w12*w20 = w02*w21*w10. The desired phases have ratio q^6=-1, whereas the separable products have ratio one. This rules out that particular factorization. It does not rule out a larger determinant, a Pfaffian gadget or a different global representation.

HUNCH. A Pfaffian representation of the full signed tree sum might exist. None was obtained. Polynomial identity testing is useful only after obtaining a polynomial-size evaluable representation for the constrained sum, including its partial-assignment restrictions. A nonzero polynomial oracle on those restrictions would permit self-reduction: at each face expand the current nonzero sum over its possible corner assignments, retain a nonzero child, and continue. The coefficient determinant above does not provide that oracle in polynomial time.

## Exchange walks

COMPUTED. `data/bad_starts.json` contains ten bad starting pairs from the fixed plantri sample through dual order 17. All 320 random or greedy trials succeeded within the cap of 1,000 moves, with at most ten moves. Each method used sixteen seeds per start. Greedy minimizes the number of Q cycles among all exchange neighbors, allowing sideways moves. Random walks are uniform over the generated neighbors, not over states.

COMPUTED. The marked constructor solved those ten starts with at most three alternating involution moves. Initial counterclockwise normalizations are recorded separately. Two starts take an unsuccessful phase and restart from four D cycles to two, exercising the strict decrease. The sample does not probe the large-state-space bound.

LIT. Constructive Theorem 5.2 ensures each exchange component has a tree. This implies finite reachability, not polynomial component diameter, mixing time, or hitting time. The random walk can also have periodicity because every move reverses the sign. Periodicity does not prevent eventually hitting a reachable target, but it matters to claims about convergence to a stationary sample.

## Matroid and spanning-tree candidates

PROVED-HERE. The omitted-spoke set of a tree matching satisfies three constraints on B's spokes: at most one at each black face, at most one at each nonroot vertex, and independence in the white dual's graphic matroid. With n chosen spokes those constraints give exactly a state and a complementary spanning tree. The two incidence conditions are different partition matroids. Treating the matching condition as one matroid is invalid in general; matchings fail the matroid exchange axiom even on a three-edge path.

COMPUTED. `two_matroid_candidate` uses genuine augmenting paths for the face partition and white graphic matroids, then tests the omitted X partition. It succeeds on the cube and hexagonal prism but fails on the truncated octahedron, truncated cuboctahedron and saved cyclic 20-vertex example. In the truncated octahedron its eleven chosen spokes repeat nonroot 3 at black faces 2 and 8 and repeat nonroot 4 at faces 4 and 15. It has a white tree but is not a state. The entire witness is in `data/other_candidates.json`.

COMPUTED. `wilson_candidate` runs loop-erased walks on the white multigraph with one labeled edge per allowed spoke, then rejects trees failing either incidence partition. Across 100 seeds per graph it accepted 24 cube trees, three hexagonal-prism trees, and zero on each of the two larger named graphs and the cyclic example. These are observed rejection rates, not proofs of low limiting probabilities. No KPW bijection from unrestricted white trees to tree matchings was established.

## Practical scale and precise status

COMPUTED. `growing_family.py` constructs truncated even bipyramids on 24 through 288 primal vertices. Enumeration succeeds on all seven members. Beyond the first member it follows a single successful prefix branch. The marked walk's flow pair is already resolved after normalization, so these are easy scaling cases. They do not support a polynomial worst-case claim.

LIT. The precise search status justified by the supplied constructive paper is deterministic polynomial-space exponential-time construction, with efficiently verifiable certificates. No polynomial-time algorithm, randomized polynomial expected-time bound, NP-hardness result under the Barnette promise, or general Pfaffian formula follows from this investigation. The incidence determinant resolves counting and sampling all states, while the selected tree remains the hard condition.
