# Routes and their limits

All new proofs are PROVED-HERE, T2, unreviewed. Counts are COMPUTED, T4, unreviewed. No independent algebraic proof of the central existence statement was obtained. This report separates new deductions from the exact identities already in the sibling reports.

## Nullstellensatz and Alon-Tarsi

PROVED-HERE. The incidence-variable polynomial F has coefficients zero or plus/minus one and tree-state support. A coefficient is nonzero precisely when the corresponding tree exists. A Boolean-grid Nullstellensatz application then works over every field, including characteristic two, but presupposes the coefficient we sought. PROOF 1 gives the exact argument. It is useful for encoding, not an existence proof.

PROVED-HERE. The direct compression to one multiplicative variable per black face or per nonroot annihilates F. Every state uses each variable once, so all monomials coalesce to a common monomial multiplied by the zero signed count. Binary incidence-dependent exponents avoid collisions using vertex variables, but their degree is exponential and nonvanishing remains unproved independently.

LIT. The strongest known same-sign statements concern three different objects. C Lemma 6.1 gives a common determinant sign for all states. C Theorem 5.2 gives a common sign for minimum-cycle D groups in the first nonzero weighted coefficient. Its marked fixed points have this same sign. The actual unweighted surviving tree pairs have equal positive and negative populations, even within each exchange component.

REFUTED. All surviving tree monomials already have the same sign, or a positive real incidence rescaling makes them have that property. The cube has two tree states with opposite signs. PROOF 1 proves the global obstruction. A signed or complex gauge is not excluded by this claim.

REFUTED, COMPUTED. The stronger signed-incidence-gauge route fails too. Exact GF2 elimination in code/gauge.py finds inconsistent sign equations on 68 of the initial 7,940 rooted examples. The first is plantri_13_7, root 2, with six tree states. Every incidence occurs an even number of times across those six states, but their coefficient signs have product minus one. PROOF 2 proves that such a certificate obstructs every incidence sign flip, even with a global sign. The exact lists and face order are in gauges.json. Arbitrary complex gauges remain untested.

HUNCH. A new Alon-Tarsi interpretation could encode the marked minimum-cycle coefficient as an Eulerian-subgraph imbalance. Test by constructing a specific directed graph whose Eulerian-subgraph polynomial equals that marked coefficient, first on the cube and on a two-D-cycle example. No such graph or independent coefficient theorem was found. Calling the existing signed imbalance an Alon-Tarsi count without that construction would only rename it.

## Modular counts

COMPUTED. TABLES.md and counts.json give all facial roots of the installed plantri corpus through the stated maximum. All forest-pair counts equal tree-matching counts. Tree counts, pair counts, and Hamiltonian edge-avoidance counts are even. The signed unweighted count is zero, rather than one.

PROVED-HERE. PROOF 2 establishes the elementary mate-histogram congruences and explains their failure to force positivity. Its Hamiltonian avoidance parity follows from Thomason's published Corollary 1.5. The prediction that avoidance might be odd was refuted and is retained in PREDICTIONS.md.

REFUTED. Tree matchings are always odd, always nonzero modulo three, or always nonzero modulo four. The smallest tested counterexamples are the octahedron, a rooted 13-vertex map with six trees, and an unobstructed root of the 9-vertex connected sum with four trees, respectively. TABLES records witnesses for other small primes. Every general congruence claimed as a theorem here has a proof, not just data.

PROVED-HERE. A free order-three action cannot exist on every tree-state set, since the cube's set has two elements. Relabeling the three vertex-color names fixes the underlying incidence matching and does not itself permute states nontrivially. This does not rule out a useful action with fixed points. A group-action existence proof would need to identify those fixed points without assuming a tree already exists.

## Graph and hypergraph polynomials

LIT. Kálmán's "A version of Tutte's polynomial for hypergraphs", arXiv:1103.1057v1, Section 5 and Section 10, defines interior and exterior polynomials by hypertree inactivity and relates hypertrees in a trinity to arborescences. Its introduction explicitly says that evaluation at one counts hypertrees. I read the accessible primary text at https://arxiv.org/html/1103.1057 . Do not infer the fixed pair of degree constraints from this one-sided hypertree count.

COMPUTED. For each of the five plantri graphs of orders 6,8,9,10, code/invariants.py constructs the proper vertex three-coloring and the three graphs induced by two colors. It computes their full Tutte polynomials, five special evaluations, and both hypergraph polynomials for each bipartition. All six hypergraph evaluations at one equal the state count. The hexagonal-prism dual has three states but only two tree matchings. The three ordinary graph spanning-tree counts there are 12,12,6. The cube's three counts are 4,4,4, while its tree-matching count is two.

REFUTED. The unweighted tree count is a fixed evaluation of any invariant depending only on the unrooted trinity. In plantri_12_2 it changes from two to eight with the facial root, although every root admits a pair. This is a computational obstruction with the root data saved, rather than a theorem classifying every rooted invariant. The same objection applies to the leading weighted signed coefficient if the weights and outer face are omitted from its proposed description. The unweighted signed count is identically zero and has only trivial such evaluations.

COMPUTED. The labeled Tait counts are 24 for the cube and 72 for the hexagonal prism. Neither equals their tree count two. The precise sum enumerated is sum_M 2^(number of components of G-M), since M is the color-one matching and the remaining even cycles have two alternating colorings. PROVED-HERE follows directly from that bijection. PROOF 2 gives exactly two nowhere-zero Z3 flows on every connected cubic bipartite primal graph; the truncated octahedron's four trees refute equality with that flow count.

LIT, access limitation. The primary paper "A Penrose polynomial for embedded graphs", arXiv:1106.5279, states the plane cubic specialization P_G(3) equals the number of edge-three-colorings. The primary search text supported this statement, but the linked full Royal Holloway PDF timed out. The table's Penrose column is therefore the Tait enumeration under this cited specialization, not an independently computed Penrose state sum. No formula for other Penrose values or for a rooted modification is claimed.

HUNCH. A coefficient of a rooted hypergraph polynomial may retain both degree constraints. Test against the exact target-degree Laplacian coefficient, rather than trying more unrooted evaluations. Root dependence does not exclude this route. No all-data nontrivial invariant match was found.

## Linear algebra

PROVED-HERE. PROOF 3 gives a positive Cauchy-Binet expansion on the graph of opposite edges with the roots identified. It represents the answer as a double squarefree coefficient of a reduced Laplacian determinant. Every contributing minor is a square, and every nonzero square is one. It retains the two matching partitions as coefficient extractions. Thus it makes positivity visible but leaves the required support theorem unproved. This is closely related to the sibling's white-dual Laplacian coefficient, rather than an independent existence proof.

REFUTED, PROVED-HERE. Real stability of the unsigned tree-state polynomial fails already for the cube. Its polynomial abc+def has a zero with all six variables in the upper half-plane. Stable spanning-tree measures therefore do not retain stability under this matching projection in general. PROOF 3 supplies the exact zero.

REFUTED, PROVED-HERE for the stated transformations. The rank-two local matrices of the signed mixed determinant cannot become positive semidefinite by similarity or Hermitian congruence of iM_t. Their eigenvalues have both signs. A diagonal similarity cannot turn both opposite entries nonnegative, nor can it give the local off-diagonal sign condition of a real M-matrix. PROOF 4 gives the invariant negative product. This does not exclude a larger auxiliary matrix with a different coefficient representation.

PROVED-HERE. The coefficient norm CT F(w)F(w^-1) equals the tree count and is a sum of squares. PROOF 6 repeats the sibling identity and spells out the circularity. A norm is strictly positive if and only if its polynomial is nonzero. The identity alone does not prove that.

## Exterior algebra

PROVED-HERE. PROOF 5 writes F as a two-species Berezin integral with one quartic term per black face. Barred-face saturation supplies one choice per face, and unbarred-vertex saturation supplies the two bijections. Zero diagonal excludes overlap. This removes the external face coefficient extraction syntactically, while retaining its full algebraic constraint in the integral.

PROVED-HERE. A real Gaussian auxiliary-field decoupling is exact. Use per-face cross covariance C_t[u,v]=delta(u,v)w_tv and sufficiently large diagonal same-species covariance. Same-species contractions vanish because of the repeated barred face generator. The result is an expectation of two determinants. This works before planarity is used and therefore does not explain nonvanishing. The product of determinants has no assured sign. Replacing it by an expected square conflicts with the nonsymmetric opposite-sign local covariance. This is the strongest complete new algebraic representation obtained here.

HUNCH. A different interaction or global change of variables might isolate the forest configurations with positive weights. Test first whether the resulting local tensor can reproduce the six transitions of one triangle and the zero diagonal, then check overlapping cycles. Planarity alone does not justify dropping contractions or signs. No exact positive decoupling was found.

## Source reading and ownership

The three supplied text dumps were read, with key formulas checked visually in the PDFs. The saved PNGs show O p. 7, Li p. 8, and C p. 9. The specified sibling reports were read before experimentation. The reference lab was imported read-only with bytecode disabled. The only written paths are in this folder. Thomason's scanned p. 262 was read visually after web fetches timed out and curl succeeded. The source PDF is an external reading copy, not a new project result.
