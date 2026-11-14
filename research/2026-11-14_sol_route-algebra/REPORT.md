# Algebra route report

PROVED-HERE, T2 unreviewed: an exact quartic Berezin integral and real Gaussian determinant-product decoupling.
PROVED-HERE, T2 unreviewed: a positive squared-minor coefficient formula, with its missing support theorem identified.
COMPUTED, T4 unreviewed: 297 plantri triangulations through 16 vertices, all 7,868 roots, plus 102 named-example and fixture roots.
REFUTED: universal nonzero residues mod 2,3,4,5,7,11, unrooted invariant equality, and a signed-incidence-gauge positivity shortcut.
OPEN: no new independent algebraic nonvanishing proof; both proof and full-count independent reviews remain pending.

## Task and reading

I sought a single polynomial or number whose nonzero value transparently forces a forest pair. I read the brief, the two requested skills and their relevant method references, all three supplied paper text dumps, the specified sibling reports, and the key PDF formula pages. I used the reference lab without edits and wrote only in this folder. PREDICTIONS.md was committed before the first count campaign.

LIT provenance is distinguished from peer-review status. The supplied papers are preprints. Thomason's 1978 primary paper was downloaded after web timeouts, and its scanned Corollary 1.5 on p. 262 was read visually. Kálmán's primary hypergraph paper was read online. The full linked Penrose paper PDF was unavailable, so the table explicitly labels the standard specialization used instead of pretending to compute its state sum.

## Established here

PROVED-HERE. PROOF.md gives complete proofs and an adversarial reread checklist. The new representation uses two species of Grassmann variables and a quartic face interaction. Saturation enforces the two matching bijections; a zero diagonal enforces disjointness. It admits an exact real Gaussian auxiliary-field decoupling into E[det K(xi) det K(eta)]. The full covariance is positive definite, but its cross block carries the antisymmetric turn signs. The integrand is not an expected square and has no assured sign. The decoupling needs no planarity, so it does not explain the central planar nonvanishing theorem.

PROVED-HERE. A root-contracted opposite-edge Laplacian gives a double squarefree coefficient equal to the tree count. Cauchy-Binet makes every summand a nonnegative square. This is closely related to the sibling's white-dual Laplacian formula, and its missing step is the same support issue. A minor must satisfy both incidence partitions. Positivity of the determinant elsewhere does not supply that minor.

PROVED-HERE. The unsigned cube tree polynomial abc+def is not real stable. The signed local rank-two matrices are indefinite after their natural Hermitian normalization. Positive incidence rescaling cannot make the tree-support polynomial coefficientwise one-signed. Multiplicative face-only or vertex-only variables annihilate the signed sum. These are precise obstructions to proposed shortcuts, not impossibility theorems for every larger representation.

COMPUTED. A second prediction and test sought a global incidence sign gauge, which the sibling's local factorization obstruction does not exclude. The 13-vertex six-tree example refutes it. A six-state GF2 inconsistency certificate has every incidence appearing evenly but three negative coefficients. PROVED-HERE gives the conditional obstruction from this explicit certificate in PROOF 2. Thus even signed incidence flips cannot always remove cancellation among the tree monomials. The certificate itself remains T4, pending independent review.

PROVED-HERE, using Thomason's published Corollary 1.5. Hamiltonian cycles avoiding any edge of a cubic bipartite graph occur in even number. The bipartite case has no cycle of odd length |V|-1, so the corollary directly gives even parity for the two other incident edges. Planarity is unnecessary. This corrects my initial prediction that odd avoidance counts might occur.

## Computation and counterexamples

COMPUTED. TABLES.md and counts.json contain every facial root, exact counts and residues modulo 2,3,4,5,7,11. They distinguish tree matchings, forest pairs, states, all ordered disjoint pairs, and Hamiltonian edge-avoidance counts. Forest pairs and tree matchings coincide. The signed unweighted count vanishes in every case, as the published cancellation proves.

COMPUTED. The final corpus also includes all 30 roots of the saved 17-vertex restart fixture, for 7,970 rooted records total. The 12-vertex cyclic fixture is already covered up to isomorphism by the exhaustive corpus. No exhaustive claim is made at order 17 or at the named larger orders.

COMPUTED. Smallest tested positive zero-residue witnesses are T=2 on the octahedron for mod 2; T=6 on plantri_13_7, root 2, for mod 3; T=4 on plantri_9_0, root 0, for mod 4; T=10 on plantri_14_7, root 4, for mod 5; T=14 on plantri_16_27, root 19, for mod 7; and T=22 on the named truncated cuboctahedron, root 0, for mod 11. This last example has 26 dual vertices and 48 primal vertices. The full positive tree-count set observed is 2,4,6,8,10,12,14,16,22.

COMPUTED. The five smallest plantri maps have full ordinary Tutte and all six hypergraph interior/exterior polynomials in invariants.json. Hypergraph evaluations at one count all states, rather than trees. Tait counts, the standard Penrose value at three, and Z3 flow counts fail the proposed equality. One 12-vertex triangulation has two or eight trees depending on the root, although every root admits a pair. This directly obstructs equality with a fixed unrooted invariant evaluation. Rooted invariants or coefficient extraction remain possible.

COMPUTED. A second author-written implementation checked every state and tree count on all 66 roots through order ten using permutations and a disjoint-set cycle test. Hamiltonian path DFS independently checked all cycles and edge-avoidance counts of the same five graphs. A reconstruction initially failed because sorted edge lists can change the embedding's face numbering. The checker now remaps saved root vertex sets and dual labels explicitly, then passes. These checks are not an independent referee's certification. The entire count corpus remains T4.

COMPUTED. The checker also reconstructs the six-state sign-gauge certificate separately: it builds each Q_s, verifies a forest with one root per component, orients toward roots to recover its unique mate, and recomputes all six signs. The even incidence multiplicities and odd negative-sign count then pass exact assertions. The local map validates and builds successfully with Python UTF-8 mode.

## What failed and why

REFUTED. Same determinant sign for states does not give same pair sign for tree states. The tree signs balance, even within exchange components by C Theorem 5.2. A literal same-sign Alon-Tarsi interpretation of the unweighted forest survivors therefore fails. The marked minimum-cycle coefficient already has a same-sign expansion in the known proof. No different orientation polynomial was constructed.

PROVED-HERE. The norm identity CT F(w)F(w^-1)=T, already in the sibling report, is exact and positive. It proves existence only after F is shown nonzero. Calling a norm positive without that step is circular. The same issue remains in the positive squared-minor determinant coefficient. Nullstellensatz applied after selecting a nonzero tree monomial also presupposes the target existence.

REFUTED. None of the tested unweighted congruences forces positivity by having a universal nonzero residue. The color-three symmetry does not create a free order-three state action: the cube's two-element tree set already prevents that. An action with meaningful fixed points is still an open direction.

## Open questions and three next steps

1. HUNCH. Seek a support theorem for the root-contracted Laplacian under the two incidence partitions. State it as a special planar three-matroid theorem and test any exchange axiom on the saved root-dependent examples. This is the clearest positive algebraic target.
2. HUNCH. Construct an actual directed graph whose Alon-Tarsi coefficient is the marked minimum-cycle imbalance. Test a full coefficient identity on a one-cycle and a two-cycle input before asserting a new interpretation.
3. HUNCH. Use the explicit Gaussian cross-covariance formula to search for a global transformation or auxiliary tensor with a nonnegative integrand. First verify the one-triangle six-transition tensor and overlapping-loop consistency. Local expected-square replacement fails.

The local dashboard and frontier are in labyrinth/. The frontier records T4 observed counts in the window 0..16 and the proved parity exclusion of odd values. It does not certify every missing even value. No coordinator-owned file was changed.

## Leads for others

COMPUTED. plantri_12_2 supplies a compact, unobstructed root-dependence example for any proposed root-free counting interpretation. PROVED-HERE. The cube supplies a minimal-size stability obstruction. LIT. Thomason Corollary 1.5 gives the requested Hamiltonian avoidance parity without planarity and is useful in an exposition separating Smith's theorem from Kotzig's total parity.
