COMPUTED: 55 small graphs, 1,206 roots and 3,618 prescribed-edge recoveries passed.
PROVED-HERE: recovery is injective, with an exact image criterion; the prism shows non-surjectivity.
PROVED-HERE: a prism-sum family has exponentially rare tree matchings; uniqueness is impossible.
COMPUTED: explicit witnesses isolate coloring, connectivity, disk-bijection and torus failures.
OPEN WORK: independent review, larger surface examples and full strengthening literature status.

# Report

## Scope and method

I set out to identify where each hypothesis enters the three supplied arguments, find small failures of weakened conditions, and determine what their construction actually parametrizes. I read the three supplied paper dumps and checked decisive formulas against rendered PDF pages. I used the reference implementation unchanged, with separate primal perfect-matching enumeration and endpoint-path DFS. Predictions precede experiments in the two prediction files. Every edit is confined to this folder.

No new subagents or referees were used. Mathematical write-ups are T2 unreviewed. Numerical results are T4 under review, including the exhaustive range. They are not certified T3 merely because all generated inputs passed.

## Established within the stated qualifications

PROVED-HERE. Fixed-root recovery is injective. Given an avoiding Hamiltonian cycle, orient its complementary dual forest minus e0 toward the three roots. Its edge tails recover a unique state. The cycle is in the construction's image exactly when this state is a tree matching. The hexagonal prism supplies the smallest computed failure of surjectivity, with two recovered cycles among four avoiding ones.

PROVED-HERE. White-face sums of q hexagonal-prism duals have 3^q states and 2^q tree matchings. The incidence matchings factor across each inserted disk, and all local disjoint pairs are tree pairs. This yields exponential rarity despite an explicit successful construction. The local three-state count and q<=6 checks are recorded. A unique tree matching cannot occur, by signed cancellation and the unique-mate property; the cube attains the minimum positive count of two.

COMPUTED. Plantri returned all 55 Eulerian triangulations through 14 dual vertices. All 1,206 roots satisfy the exact black-inner separator criterion. Recursive construction passed all 3,618 prescriptions. Direct recovery had no collisions across 9,720 produced images. Root counts vary even when the black face class is fixed. All 55 primal graphs, through order 24, pass arbitrary include-one/avoid-another, P4, and opposite-color Hamiltonian endpoint tests.

PROVED-HERE. P5 fails on the cube by a forced-degree obstruction. Original states cannot exist on the torus, since |A|-|X|=2. The explicit nine-vertex torus triangulation has no two-induced-tree partition although its dual has Hamiltonian cycles. A root-free relaxed pair exists but Q cannot be a forest. The appropriate general target is one selected edge per triangular face whose complementary dual is connected.

COMPUTED. The 26-vertex theta-of-cubes example has eight states and zero pairs at every root. At root 0 all eight incidence complements are disconnected, with cycle rank three. A deficient capacity cut is supplied. The disk identity still has a valid incidence-count proof on this multimap; pair existence is the first failed assertion.

COMPUTED. Relaxed non-bijective choices on a nine-vertex Eulerian triangulation produce a directed 4-cycle of delta-sum zero. The disk has B=W=2, I=1, l=2, exposing precisely the missing B=I+l equality. Maximum-cut colorings of K4, BBL38 and Tutte46 still leave edges with zero or two black owners. Zero spoke weights give identically zero Z on the cube.

## What failed and what it taught

REFUTED. The direct map does not enumerate all avoiding Hamiltonian cycles. Exposition should state its image criterion rather than imply a bijection with the full cycle set.

REFUTED. My first rarity construction inserted pieces in the wrong face color and produced no pairs. The old piece's boundary forces the new boundary color. The preserved failed run distinguishes an obstructed root from a feasible but rare target.

REFUTED. A forest Q without a mate is enough. The prism has a third state whose Q is acyclic but has one component with two roots and another with none. The partner is what supplies the needed outdegree count.

REFUTED. Exactly one tree matching could make Proposition 5.1 tight. The signed tree count is zero, so nonempty tree sets have at least two members. This is already implicit in the constructive paper's component theorem.

The first dashboard build also exposed a schema mismatch and Windows text-decoding issue. The local data format was corrected and the documented engine commands now use Python's UTF-8 mode. Both validation and build pass.

## Limits and open work

The report does not claim a complete independent audit of every lemma. The main structural dependencies and requested small tests are covered; minimum failures of arbitrary r-dependent cycle-selection rules and mixed-sign nonzero circulations were not classified. Li's higher-mark involutions were read but not independently reimplemented here.

The full 1982 minimality paper returned HTTP 403; its 26-vertex result is attributed to the publisher abstract. The 38-vertex minimality paper was not opened. The explicit 38- and 46-vertex adjacency data and coloring failures were checked, but their non-Hamiltonicity was not independently recomputed.

The 50-, 54-, and 96-vertex nonplanar counterexamples were not constructed, nor were projective-plane embeddings enumerated. A small torus counterexample to the proposed dual target and its relaxed pair are provided. The global literature status of arbitrary edge-pair control and Hamilton-laceability remains unresolved here; the absence of small failures is not a proof or an assertion that these are globally open.

All proof claims need independent review, especially the general inverse-recovery characterization, the prism-sum factorization and the topological spine description. The frontier map deliberately marks no uncertified impossible ranges. The tested finite frontier grew from 15 graphs and 262 roots through dual order 12 to 55 graphs and 1,206 roots through order 14. Certified resolved fraction remains zero until independent validation.

## Three best next steps

1. Independently check the recovery inverse and prism-sum factorization, with a separate implementation of the local three-state case and a referee proof pass.
2. Extend the strengthening census beyond primal order 24 while reading original sources for arbitrary H+- and Hamilton-laceability. Retain explicit failing paths or edge pairs if found.
3. Build a surface-aware incidence implementation retaining darts and homology. Test root-free torus pairs against connected unicyclic or tree-plus-bicyclic complements, keeping complementary-dual connectedness as the actual acceptance criterion.

## Leads for others

The exposition should distinguish three notions that the prism separates: a state with acyclic Q, a tree matching, and a Hamiltonian cycle avoiding the root edge. It should also state that every root works after recursive gluing, while some roots have no direct pair. The exact image theorem may explain which output cycles an algorithmic variant can ever find.

## Deliverables

HYPOTHESES.md contains proofs, failures, smallest-instance qualifications and lessons. STRENGTHENINGS.md separates direct consequences, cited equivalences, finite evidence and unresolved questions. ROOT_COUNTS.md summarizes the root table. README.md gives exact commands. code/, data/ and examples/ preserve scripts, full counts, solver outputs and explicit adjacency certificates. The validated local dashboard is labyrinth/dashboard/index.html.
