# Referee of the probabilistic routes

Reviewer GPT-6.1-sol. Scope is REPORT, ROUTES, PROOFS and EXPERIMENTS in `../2026-11-14_sol_route-probabilistic/`, excluding the two-tree packing claim. I read `../2026-11-14_opus_two-tree-packing/REPORT.md`; its new packing proofs are not independently refereed here. All proofs below are PROVED-HERE, T2; finite outputs are COMPUTED. The disk and height identities are accepted supplied-preprint inputs as in REFEREE-covers.md.

## Claims and findings

### P1. Full-support mean obstruction

Exact claim: on the full spoke graph H, with finite strictly positive edge weights, a weighted spanning tree cannot have mean degree vector d*, where the outer black centre has prescribed degree three, bounded centres degree two, nonroots their full spoke degree minus one, and roots their full spoke degree.

Verdict CORRECT, PROVED-HERE. Every spoke belongs to a six-sided face boundary. Its three black centres are distinct because distinct faces of a simple sphere triangulation share at most one edge. Thus each spoke is on a cycle and is not a bridge. H-e is connected and has a spanning tree. Under finite positive weights that tree has positive probability, so Pr(e in tree)<1. Summing at t0 gives E deg(t0)<3. The same strict maximum-degree inequality holds at each root. The argument works for every full-support distribution on all spanning trees, not only a product-weight UST.

Precisely what is excluded: exact finite-parameter mean fitting to d* in an exponential family supported on ALL H trees, including any law assigning every tree positive probability. This also rules out a maximum-entropy optimizer with full support and that mean.

What is not excluded: conditioning on all forced root and outer spokes, using zero weights or limits of diverging weights, a measure supported on a face of the tree polytope, a distribution on a different graph or object set, or a positive-measure argument not requiring this exact mean. Boundary convex feasibility is not contradicted. Nor is a positive probability of the exact target event contradicted by a different mean. The report's sentence "conditioning or diverging weights is compulsory" should be read as a statement about exact mean fitting on H, not all probabilistic proof strategies. An arbitrary boundary-supported law is another possibility.

Exact related probability formula: Pr_w(deg=d*) equals the sum over tree states s of the product of weights on undeleted spokes, divided by tau_H(w). Verdict CORRECT, PROVED-HERE. A tree with those degrees deletes exactly one spoke per bounded centre and one per nonroot and none at roots or t0. These n deletions are precisely a state. Its complement is a tree exactly for a tree matching. Uniform success is M/tau(H), whereas uniform-state success is M/S. These samplers must not be identified.

### P2. Convex means and rounding

Exact claim: finite exponential-family means fill the relative interior of the convex hull of their finite feature support; limits fill its closure. Matching the mean does not imply a support atom at that mean.

Verdict CORRECT, PROVED-HERE. Strict positive convex combinations lie in the relative interior. Conversely on the span of differences, for an interior target b, `log sum c_i exp(theta.(a_i-b))` is coercive: the maximum directional slope has a strictly positive uniform lower bound on the unit sphere. Its minimizer has zero gradient. A singleton support has zero-dimensional span and is immediate. Boundary approximation gives the closure statement. The Hessian is covariance; the KL variational argument establishes maximum relative entropy. None supplies the missing integer point at b. A fractional vertex elsewhere in a slice is not evidence that this particular target is absent.

The six-cycle joint-degree M-exchange obstruction in PROOFS section 4 is CORRECT, PROVED-HERE: deleting one cycle edge gives two adjacent leaves, and the demanded exchange produces a pair of nonadjacent leaves. This refutes the proposed general two-sided M-convex extension. One-sided degree substitution uses a linear nonnegative substitution and does not suffer this objection. No new audit of Lorentzian theory is claimed here.

### P3. Root-location shortcuts

Exact claims: the signed z-polynomial need not be real-rooted or have all nonzero roots on the unit circle; the incidence-linear polynomial need not be real-rooted.

Verdict CORRECT, REFUTED universal shortcuts, COMPUTED with exact symbolic certificates. The independent code solves the unit white-circulation equations by rational linear algebra, sets free variables to zero, enumerates pairs itself, and calculates the disk phase from cyclic face order. It imports no author weights, signs, states or polynomial routine.

For the supplied off-circle edge-list witness, with root face {0,6,1}, it gives `-(z-1)(z^2+3)`, precisely the reported exponential factor up to sign. The roots ±i sqrt(3) certify failure. For the eight-prism, rooted at {8,0,1}, it gives `z^3-1`, certifying nonreal roots.

For the supplied linear witness graph, rooted at {0,4,1}, my independently chosen circulation gauge gives `-x(x+2)(x^2+2x+2)`. Its roots -1±i prove the same failure. The author's exact factor `x(x+1)(2x+1)(2x^2+5x+4)` is not independently reproduced in its original incidence gauge here. Substituting each incidence weight linearly is gauge dependent; it is not obtained by applying a gauge change to the final exponential polynomial. Both displayed quadratics have negative discriminant. The verdict certifies the refutation and my retained gauge, not the author's exact linear table or minimum-size scan. See `code/polynomials.json`, which retains every weight used.

All "first example" assertions must remain relative to the author's root, orientation and weight scan. Independent minimality was not established here.

### P4. Signed measure and moments

Exact claim: for a uniform ordered pair, pushing the signed mass epsilon/P onto second states leaves atoms epsilon(r_s,s)/P at tree states and zero at other states. Pair signs have mass 1/2 each; the surviving signed measure on states has positive and negative masses M/(2P) and variation M/P. Height monomials of total degree less than m=c_min have zero signed expectation, and a degree-m product has nonzero expectation.

Verdict CORRECT, PROVED-HERE, assuming P>0. The fixed-s involution cancels every cyclic fibre. A forest fibre has one element. Reversal of a canonically chosen D-cycle is fixed-point-free and flips epsilon on all pairs, proving zero total signed mass. Thus the M surviving atoms split equally by sign. The height moment assertion follows by multilinear expansion of the independent cycle-orientation differences; fewer than m factors cannot cover all cycles. At degree m a minimal cover and suitable labelled white faces provide a positive permanent, with the common disk sign. State-independent height shifts introduce only lower-degree moments and preserve the first nonzero degree.

After a further pushforward to height vectors, opposite atoms can coincide and cancel. The stated total-variation M/P concerns the measure on STATES; do not assign it automatically to the height pushforward. Its Jordan parts still have matching lower moments. This is a signed finite measure, not a probability distribution. Dividing a tilted signed sum by a positive partition function merely restates nonvanishing and proves no new existence assertion.

### P5. Height-marked constructor

Exact claim: given the true minimum m, suitable labelled white faces w_1,...,w_m, integer height functions, shifts making H_i>=0 on every state, and deterministic orders, the proposed alternating walk terminates at a forest pair.

Verdict CORRECT, PROVED-HERE conditional on these initialization inputs. Here is the full coordinate check, which is the delicate part of this claim. For a fixed undirected D, use its all-clockwise state to define b_i>=0. Then

    H_i(s)=b_i+sum_C x_C a_iC,

where x_C indicates counterclockwise orientation and a_iC is zero or one according as w_i lies outside or inside C. At slot i use b_i permanently labelled base tokens plus a token labelled C for each active C with a_iC=1. Give this pool a deterministic order. Its cardinality is H_i(s), so rank conversion is a bijection to ordinary integer marks.

The D-map reverses the first cycle whose label is absent from every slot, retaining chosen token identities and re-ranking. The reversed cycle's token was never chosen, so all retained tokens remain valid. The chosen labels, the uncovered-cycle set and its order are unchanged. Thus the same cycle is reversed on return. Its disk phase changes sign. If every cycle is covered, c<=m, while minimality gives c>=m. There are exactly m distinct covered cycles, no base token is chosen, and each cycle appears once and must be counterclockwise. Every such fixed point has sign (-1)^((n-m)/2). A minimal cover and a bijective choice of interior w_i give at least one fixed point.

The Q-map retains s and the INTEGER ranks, rather than trying to retain the old D-labels when D changes. Each rank remains in {1,...,H_i(s)}. Its token labels are recomputed from the new D on the next D-step. This is why coordinate changes between the maps are valid. Q-reversal is its own inverse and reverses sign off its forest fixed set.

Keep labelled parallel edges if both involutions swap the same two objects. The finite two-coloured graph has degree at most two. Starting at a D-fixed endpoint traces a finite path or a singleton. If the other endpoint were D-fixed, the path would have odd length and opposite endpoint signs, contradicting the common fixed-point sign. It must be Q-fixed. A singleton already supplies a forest pair. This supplies the minor singleton detail omitted from the short termination paragraph.

The algorithm is implementable by finite exhaustive preprocessing. It has no proved efficient initialization or polynomial running time. I have audited the argument; no executable implementation of this marked variant was supplied or independently tested here.

Relation to sources: `barnette_trees`, section 5.1, uses an ordered list of tokens from the total incidence-weight pool and equal-rank transport within cycle pools. It can start from an arbitrary pair and restart when c decreases. This variant uses one slot per selected height and assumes the global minimum, so its endpoint signs agree without restarts. `proofs/involutions/INVOLUTIONS.md` uses an unordered set of distinct geometric crossings, allowing repeated spokes but not the same crossing twice, with extra crossing-direction signs. Its endpoint principle is the same. These are different marked sets and maps, not a claim of identical algorithms or matching running-time bounds.

### P6. Zero-cycle and sampling claims

Exact claim: weighting a state by exp(-beta cycle_rank(Q)) need not remove root defects, and if A states have acyclic Q then tree success is at most M/A for beta>=0.

Verdict CORRECT, PROVED-HERE. Every acyclic state has weight one, including every successful state, so the denominator is at least A. The hexagonal prism's third state has acyclic Q but no partner; this is independently visible in the state enumeration. Thus cycle rank alone is an inadequate success indicator. Numerical hitting rates, floating sampler probabilities, mixing spectra, and the particular tube count A=68 remain the author's COMPUTED observations, not asymptotic theorems or independently certified experiments in this review.

## Obligation graph and dependency table

P1 <- nonbridge spokes AND full support AND maximal prescribed root degree. P2 <- interior convexity AND coercivity AND first-order optimum. P3 <- admissible weights AND independent signed enumeration AND nonreal factor. P4 <- fibre cancellation AND unique forest partner AND orientation balance AND height increments. P5 <- P4 height increments AND finite nonnegative pools AND two involutions AND common fixed sign AND finite path. P6 <- acyclic states retain unit weight.

| ID | Exact obligation | Needed by | Route / edge | Classification | Support | Status |
|---|---|---|---|---|---|---|
| O1 | Every spoke can be omitted by an H tree | P1 | cycles / AND | algebraic/logical step | hexagonal face boundary | discharged |
| O2 | Every tree has positive probability | P1 | measure / AND | hypothesis | finite positive weights | discharged |
| O3 | Relative-interior target gives coercivity | P2 | optimization / AND | algebraic/logical step | directional bound above | discharged |
| O4 | Own weights satisfy bounded-face circulation | P3 | linear system / AND | side condition | exact check.py equations | discharged |
| O5 | Author's precise linear gauge reproduced | original factor table | replay / AND | side condition | different gauge used here | open |
| O6 | Cyclic fibres cancel and forests have one mate | P4,P5 | signed count / AND | named theorem | OpenAI 5.1 and rooted orientation | discharged |
| O7 | Rank conversion survives each map | P5 | marking / AND | algebraic/logical step | explicit distinction above | discharged |
| O8 | m is a true minimum and selected heights are suitable | P5 | initialization / AND | hypothesis | stated algorithm input, finite search available | discharged |
| O9 | Finite alternating path ends in Q-fixed set | P5 | endpoints / AND | algebraic/logical step | common sign and odd path | discharged |

## Verdict

FOLLOWS for the mean obstruction with its full-support scope, convex-mean statements, signed-measure interpretation and initialized height walk. The root-location shortcuts are REFUTED by independently evaluated witnesses. The precise original linear-gauge factor and scan minimalities remain COMPUTED by the author. The report is not a proof that all positive-measure strategies fail. Its two-tree packing conjecture has a separate proposed proof in the Opus folder, outside this audit.
