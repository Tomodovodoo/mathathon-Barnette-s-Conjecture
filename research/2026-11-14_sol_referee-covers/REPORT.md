# Independent referee report

The separator-free unique-cover family and the two-cover exponential bound pass the proof audit.
Both disconnected-level witnesses and the signed-polynomial root counterexamples pass independent computation.
All eight tube recurrences now have independently reconstructed all-length transfer certificates.
The prism formulas, labelled prism-chain tensor and Hamiltonian lower-bound derivations pass, with one literature-parameter correction.
The larger census remains author-computed beyond order 16; full-support mean fitting is obstructed, not all positive-measure arguments.

## Scope and method

I acted as the requested review sub-agent and used no further agents. I wrote only in `research/2026-11-14_sol_referee-covers/`. I read the brief, README, the three named skills and referee instructions, the supplied OpenAI paper through its text extraction, the requested reports and relevant code/data, the primal dictionary, the route-topology retraction lemma, the constructive manuscript's marked-walk section and the involution exposition. I read the Opus two-tree-packing report and did not duplicate that proof audit. Mathematical dependencies and accepted source inputs are explicit in the three referee documents.

The source PDFs were not visually rendered in this review. The disk, sign, circulation, recovery and gluing formulas were checked in their extracted source sections, against independent implementations and explicit arguments. The OpenAI and constructive manuscripts are supplied preprints, not treated as peer-reviewed publications. Published counting comparisons were checked against the primary sources linked in REFEREE-families F6; INDEX.md reports those sources as not locally held.

The independent scripts use NetworkX for embeddings and elementary graph tests, SymPy for exact linear equations and factors, and the existing plantri executable only for generation. They import no author verifier or laboratory algorithm. All command-produced outputs and exact commands are in `code/README.md`. Reviewed-source hashes and environment versions are in `code/provenance.json`.

## Established

PROVED-HERE, T2, independently AI-refereed here, human check pending:

- The exact admissible primal deletion dictionary, c(D)=kappa(G-S)-1, and its compatibility with the distinct recovered-matching retraction identity.
- Simplicity, Eulerian degrees, absence of separating triangles, forced unique cover and M=2^(m-1) for the rooted T_m family, m>=2.
- The exact two-cover overlap count, hence M>=2^c_min when there are exactly two covers.
- The minimum-cover leading coefficient and its independent white-face marks, equivalently pointed laminar bonds, including the factorial convention and the failure of a bijection to all unweighted tree matchings.
- The full-support positive-weight mean obstruction with its exact scope; finite exponential-family mean characterization; signed-measure moment interpretation; and correctness of the initialized height-marked walk, including coordinate changes and singleton endpoints.
- Even-prism counts and avoidance formulas, separator-free tube construction and rarity, all-length S,P,M,H recurrences at widths four and six, and c_min=1 at both widths.
- Multiplicative state/pair/tree counts and the signed-product formula for the specified nested prism chain, with its Hamiltonian recurrence from an independently verified eight-cycle tensor.
- The fixed-root, varying-root and separator-product Hamiltonian lower bounds, conditional on the supplied signed existence and recovery lemmas. An independent Newton-identity argument supplies the linear M>=2c_min consequence.

COMPUTED independent checks, with reproducible scripts:

- T_m for m=2,...,8, with signed polynomials through m=6.
- Prisms for m=2,...,7, including all Hamiltonian cycles and every edge's avoidance count.
- Width-four tubes L=0,...,5 and width-six L=0,...,3 by full state, pair and primal matching enumeration.
- Eight independently reconstructed stationary transfers, with dimensions 4,2,2,12 and 15,39,36,64. Exact recurrence discrepancies certify all lengths by Cayley-Hamilton. Boolean pair-cost repeats [0,1] and [2,3] certify c_min=1 beyond the directly checked prefix.
- Every separator-free facial root through dual order 16, 129 unrooted classes and 3,374 face occurrences; the stated histograms and counting inequalities agree. The final replay additionally tests the exact two-cover overlap formula.
- Both order-18 flip graphs, both polynomial witness graphs, chain graphs through q=5, and all eight local Hamiltonian tensor entries.
- Author census summary consistency through order 24 and population counts against published e_4 values. The arithmetic total is 23,824,742 facial-root occurrences, not distinct rooted-map isomorphism classes.

## Corrections and limits

CORRECT AFTER FIX: the second Florek comparison should cite Proposition 1.4 with the induced dual big-vertex maximum degree, and should not attach the separate four-big-neighbour hypothesis to that proposition. A maximum primal face length gives a weaker valid parameter. The published first Florek theorem includes a ceiling which its older arXiv version omits.

CORRECT AFTER FIX: the positive-weight obstruction excludes exact mean fitting by full-support laws on all H spanning trees. It does not exclude conditioning, boundary-supported laws, limiting weights, or positive-measure arguments with another objective. The variation M/P is for the signed measure on states, not automatically for a height pushforward where atoms may merge.

COMPUTED with explicit scope: my independent incidence gauge changes the linear-polynomial witness's exact factor, but still gives nonreal roots. The off-unit-circle exponential factor reproduces up to sign. Original linear-gauge factors, first-example minimalities, census invariant calculations at orders 17–24, numerical sampling and spectra, larger subdivision/root tables and decimal growth-rate estimates are not independently replayed here.

The report's prism-chain gluing permutation is essential. My control chain using a different explicit permutation has H=24 at q=2, while the submitted graph has H=20. Its state and polynomial formulas agree. This was a useful control, not a submitted-theorem counterexample.

No required claim was found outright false after specifying its stated root, gauge, permutation and evidence range. The strongest remaining qualification is provenance, especially the larger census. All new AI-reviewed results remain T2 or independently supported computational certificates, not T1 by virtue of this review.

## What failed and what remains open

REFUTED: connectivity of fixed-cycle levels and of minimizers, universal real-rootedness/unit-circle shortcuts, interpreting the leading coefficient as all unweighted tree matchings, and using cycle rank alone to detect a tree state. The witnesses and precise lessons are retained in the referee documents.

CONJECTURE: the general exponential tree-matching bound and multi-cover strictness. The two-cover equality configuration is isolated but not excluded. CONJECTURE: unbounded c_min within bounded primal face sizes, especially squares and hexagons. The unrestricted separator-free question is resolved by T_m and should be removed from the global open list. Efficient search and positive-measure routes after conditioning remain open. The two-tree-packing route has a separate Opus proposed proof requiring its assigned referee.

## Three best next steps

1. Integrate the exact passages in INTEGRATION.md, replacing the obsolete separator-free boundedness question and qualifying the large census, mean obstruction and literature parameters.
2. Seek a planar obstruction to the two-cover equality configuration, or a multi-cover overlap argument proving M>=2^c_min. The disconnected-level witnesses rule out an induction that assumes level connectivity.
3. Test bounded-degree triangulations for growing c_min, and study a conditioned positive-measure construction that enforces both degree families. Use the width-four family to test hitting a rare success set, not merely mixing over states.

## Leads for others

The minimal-cover coefficient is a clean primal pointed-bond count but supplies no unweighted tree-matching bijection. The topology retraction formula concerns another edge set and should be presented separately. The prism-chain control suggests always retaining the gluing permutation with any claimed Hamiltonian recurrence. No manuscript, canonical map, dashboard or another agent's file was modified.

## Git and process

Only this folder was staged and committed. No heavy process ran concurrently with another heavy process in this review, no run exceeded ten minutes, and no computation remains running. A first stable code commit was made during the review; the final commit includes the reports, independent transfer reconstruction and provenance. The brief's requested push is attempted after that commit; its outcome is recorded in the final chat response.
