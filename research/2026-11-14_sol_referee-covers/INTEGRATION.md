# Statements cleared for integration

GPT-6.1-sol, independent referee, 14 November 2026. These are final suggested passages, not edits to the manuscript or open-problem list. PROVED-HERE means T2 with this AI referee, human review pending. COMPUTED claims retain their explicit ranges. The supplied OpenAI and constructive manuscripts are preprints; citing them is not a peer-review claim.

## Safe mathematical remarks

PROVED-HERE. "An admissible cover is equivalently a primal deletion set S with one selected edge at each nonroot black vertex and none at the root, two selected boundary edges at each nonroot face and none at a root face. Its dual is a union D of vertex-disjoint cycles, and c(D)=kappa(G-S)-1. The local conditions impose no selected degree at white vertices. Thus G-S is generally not a 2-factor." Proof: REFEREE-covers C2; submitted PROOFS section 1. Keep S distinct from the recovered primal perfect matching P*.

PROVED-HERE. "The minimum cover-cycle count is unbounded even without separating triangles. For m>=2, start with the bipyramid on the equator x_0,y_0,...,x_(m-1),y_(m-1); subdivide Bx_i by z_i and add z_i y_(i-1), z_i y_i. Root the face A x_0 y_0 and colour A x_i y_i, x_i z_i y_(i-1), B z_i y_i black. The resulting T_m has a unique cover, consisting of m-2 triangles and one pentagon. Consequently c_min=m-1 and M=2^(m-1)." Full construction and forcing proof: REFEREE-covers C1; submitted PROOFS section 2. This resolves the unrestricted separator-free boundedness question, but not the bounded-face-size version.

PROVED-HERE. "For exactly two covers D1,D2, with c1,c2 cycles and j shared component cycles, M=2^c1+2^c2-2a, where a is either zero or 2^j. In particular M>=2^min(c1,c2). Equality requires c1=c2=j+1 and a=2^j." Proof: REFEREE-covers C3. Do not infer the general exponential conjecture or strictness from this special case.

PROVED-HERE. "For unit white-face circulation, if q=c_min then the absolute coefficient of x^q in the signed exponential sum is the sum, over minimal covers, of the product of the white-face counts inside their cycles. It counts a minimal cover together with an independently chosen interior white-face mark for each cycle. Marks may repeat across nested disks. Covers with more cycles vanish to higher order; minimum covers have a common first sign." Proof: REFEREE-covers C6. In primal language these are locally admissible laminar bond families with one white vertex chosen on each root-free shore. A q-th derivative has an additional q! factor. This is not a count of unweighted tree matchings.

PROVED-HERE with independent finite certificates. "The width-four alternating-diagonal tube, rooted at its specified lateral face, has S_L=Fib_(2L+3), M_L=P_L=2 and c_min=1 for all L>=0. Its dual has no separating triangles and its primal has only square and hexagonal faces. Thus a uniformly chosen state is a tree matching with probability 2/Fib_(2L+3), exponentially small in primal order 8(L+1)." Construction, proof and independent all-length transfer: REFEREE-families F2–F3, `code/transfer.py`, `code/rebuilt-transfers.json`. This is a different family from T_m.

PROVED-HERE with independent finite certificates. "At width six, for the specified lateral root and L>=2, the state, tree-matching and ordered-pair sequences have the initial values and recurrences in REFEREE-families F2. The Hamiltonian sequence starts at L=0 with 8,44,176,752,3200,13568 and satisfies H_L=2H_(L-1)-H_(L-2)+40H_(L-3)+8H_(L-4)+64H_(L-5)-16H_(L-6). The minimum cover-cycle count is one for every L." Retain the root and recurrence starting index. The independent reconstructed matrices and Cayley-Hamilton discrepancy tests establish every length, rather than fitting a finite list.

PROVED-HERE. "The 2m-prism has m states, two tree matchings, one cover cycle, 2m+2 Hamiltonian cycles and signed polynomial z^(m-1)-1 up to overall sign and a monomial. A rail edge is avoided by two Hamiltonian cycles and a rung by 2m-2." Proof: REFEREE-families F1.

PROVED-HERE. "For the labelled nested white-face hexagonal-prism chain, S=3^q, M=P=2^q and c_min=q. Its normalized polynomial is product_(j=0,...,q-1)(z^(5j+2)-1). Thus the conjectural bound M>=2^c_min would be sharp for every positive exponent." Proof: REFEREE-families F4. Its Hamiltonian count is 8 at q=1 and 20*3^(q-2) for q>=2 for the submitted gluing permutation, verified through an exhaustive eight-cycle local tensor. Specify the labelled permutation or cite the retained graphs and tensor; other permutations can change H.

PROVED-HERE conditional on the signed forest theorem and recovery. "For a feasible root t, each incident primal edge has at least M_t>=2c_t avoiding Hamiltonian cycles, and H>=3M_t>=6c_t. More generally H>=(2/N) sum_(uv) max(M_u,M_v), with zero assigned to unavailable direct-root counts. Decomposition into b irreducible pieces yields H_avoid(e)>=2^b and H>=3*2^b for every prescribed edge e. In particular H>=6, tight on the cube." Proof and normalization: REFEREE-families F5. No exponential-in-order bound holds for the full class, since prisms have H=N/2+2. Do not claim novelty or global literature optimality.

PROVED-HERE. "Finite positive edge weights on the full spoke graph cannot fit the prescribed tree degrees in expectation: every root or outer-centre spoke can be absent from a spanning tree, so its inclusion probability is strictly less than one under any full-support law. The target requires maximal degree at the roots and outer centre." Scope: REFEREE-probabilistic P1–P2. This excludes full-support mean fitting, not conditioned or boundary-supported positive measures, nor positive-measure proofs in general.

PROVED-HERE conditional on height and cancellation identities. "The signed pushforward of a uniform pair to its second state is supported on tree matchings. Its variation on states is M/P and its two sign masses are M/(2P). Its height moments below total degree c_min vanish, while a degree-c_min product is nonzero. Marking suitably shifted nonnegative heights gives a finite two-involution walk from a minimum-cover marked object to a forest pair." Proof: REFEREE-probabilistic P4–P5. The walk assumes minimum-cover preprocessing, suitable labelled height slots and deterministic rank conversions; it has no polynomial-time guarantee. The distinct-crossing walk in proofs/involutions and the ordered-incidence-token walk of barnette_trees use different marked objects.

## Safe computed refutations

REFUTED, COMPUTED. "Neither fixed-cycle levels nor minimizing levels are always connected by simple-cycle reversals." Cite `code/witnesses.json` and REFEREE-covers C5 for the two independent order-18 certificates. The saved witnesses prove failure without any smallest-order claim.

REFUTED, COMPUTED with exact algebraic certificates. "Neither real-rootedness nor unit-circle root location holds for the signed exponential polynomial, and incidence-linear real-rootedness also fails." Cite REFEREE-probabilistic P3 and `code/polynomials.json`. The off-circle factor is `(z-1)(z^2+3)` up to sign and monomial. The referee's independently chosen linear gauge gives `-x(x+2)(x^2+2x+2)`. Do not quote the author's exact linear factor as independently replayed by this referee, or assign gauge-independent minimality to that scan.

## Wording for the open-problem list

CONJECTURE. "Does M>=2^c_min hold for every rooted instance admitting a pair? Is the inequality strict whenever there is more than one cover? The single-cover and two-cover cases satisfy the weak bound. Explicit single-cover families attain equality for every exponent. The general multi-cover case and strictness remain open." A next test is the necessary two-cover equality configuration in REFEREE-covers C3, not an induction on connected c-levels.

CONJECTURE. "Can c_min be unbounded when all primal faces have bounded size, in particular when all have size four or six?" The separator-free T_m family has growing pole degree and does not answer this. The width-four rare family has c_min=1.

CONJECTURE. "Is there an efficient constructor or a useful positive-measure proof after conditioning the forced spokes?" The finite-positive-weight obstruction does not decide it. The height-marked walk gives a finite constructor but uses global minimum and height preprocessing. Mixing a state sampler does not overcome exponentially small success density.

COMPUTED. "The cycle-cover campaign reports no counting-conjecture violation in 23,824,742 facial-root occurrences through dual order 24. An independent state-and-pair replay in this referee folder confirms all 3,374 occurrences of the 129 graphs through order 16. The class counts through order 24 agree with published plantri Table 6." This wording preserves the difference between source-reported larger invariants and independently reproduced smaller ones. Facial-root occurrences are not isomorphism classes of rooted maps.

The new Opus two-tree-packing report claims a proof of the probabilistic report's former conjecture. That proof has a separate review assignment. Do not leave it categorically labelled open without checking that referee, and do not treat this report as an independent certification of it.

## Literature corrections

LIT. Cite Florek's published 2020 Theorem 1 for the facial-quadrilateral-2-factor bound with the ceiling. The 2018 arXiv statement lacks that ceiling. Cite arXiv:2309.09578v2 Proposition 1.4 for the small-and-big-incidence bound, using the maximum degree of the dual big-vertex induced graph. It does not require the separate four-big-neighbour hypothesis. Maximum primal face length supplies a weaker substitute, not the exact source parameter. Details and opened URLs are in REFEREE-families F6.

## Claims not cleared by this review

COMPUTED only by their authors: census invariant calculations at orders 17–24, original linear-gauge factor and first-example minimalities, numerical sampler and mixing tables, larger root sweeps and subdivision counts, and decimal width-six asymptotic rates. These may be quoted with provenance and range, not as independently replayed here. General exponential counting, strictness, bounded-face-size unboundedness and efficient search remain conjectural. An unrestricted assertion that positive-measure arguments cannot work is not supported.
