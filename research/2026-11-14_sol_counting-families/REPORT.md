# Research report

Even prisms now have complete formulas for all requested counts and their signed polynomial.
Two explicit no-separator nanotube widths have stationary integer transfer certificates for states, pairs, tree matchings and Hamiltonian cycles.
The width-4 tube has two tree matchings but exponentially many states, extending rarity beyond separating-triangle families.
Nested prism sums give M=2^c_min for every positive c_min and an explicit signed-product formula.
The no-separator unbounded-c_min family, the full width-6 signed recurrence and iterated-inflation asymptotics remain unresolved.

## Scope and sources

I worked only in this assigned folder, used `workings/barnette_lab/` read-only, and read the brief, README, the named skills, the OpenAI paper's text, and the specified prior reports and referee corrections. The determinant referee files are named REFEREE-dimers.md and REFEREE-constructive.md, rather than REFEREE.md. I read the former for the relevant common-sign and integer-formula conclusions. The supplied paper's PDF was not visually rendered; its complete text extraction was the reading source. The formulas used were checked against the available exact-code conventions and the finished referee reports.

The source-dependent lower-bound comparisons were checked against opened publisher or author pages. BOUNDS.md records precisely which theorem statements were read and which proof audits remain undone. No current global optimality claim is made.

## Established and computed

PROVED-HERE, T2 unreviewed. FAMILIES.md gives a direct proof for the 2m-prism: S=m, P=M=F=2, c_min=1, H=2m+2, rail avoidance 2, rung avoidance 2m-2, and normalized signed polynomial z^(m-1)-1. Recovery gives two cycles per root prescription and six over its three prescriptions.

PROVED-HERE, T2 unreviewed. The alternating-diagonal ring adjacency rule defines Eulerian triangulations with no separating triangles. Their primal faces have sizes 4,6 and two cap p-gons. The face-frontier matching transfer, opposite-edge forest transfer, pair-cycle transfer and induced-tree HC transfer are justified by bijections. Avoidance of any edge is a monochromatic-edge constraint in the latter transfer.

COMPUTED, T4 under review. Widths 4 and 6 have complete sparse matrices, integer initial and terminal vectors, rational generating functions and finite recurrence certificates. Width 4 has S_L=Fib_(2L+3), P_L=M_L=2, c_min=1, and H_L=2H_(L-1)-H_(L-2)+4H_(L-3). The state success fraction is 2/Fib_(2L+3), exponentially small with no triangular separators. Width 6 has larger recurrences in FAMILIES.md; numerical per-layer bases are approximately 5.6131 for S, 3.1304 for P, 2.3830 for M and 4.2581 for H. The exact algebraic polynomials are saved, so these decimals are not inputs to the counting claims.

PROVED-HERE, T2 unreviewed. The q-prism chain has S=3^q, P=M=F=2^q, c_min=q and normalized signed polynomial product_(j=0..q-1)(z^(5j+2)-1). This proves sharpness of the conjectured exponential TM bound at every exponent. Its leading coefficient at z=1 is product_(j=0..q-1)(5j+2). The local HC tensor is COMPUTED from eight explicit prism cycles; conditional on that finite tensor, the proved gluing identity gives H_q=20*3^(q-2) for q>=2, and prescribed-edge counts by matrix insertion. The chosen-root recovery gives 2^q cycles per edge, 3*2^q over its three edges.

PROVED-HERE conditional on the supplied existence theorem and refereed recovery argument. BOUNDS.md derives H_avoid(e)>=2c_t and H>=6c_t for a feasible fixed root, the correctly normalized sum-over-roots bound, and H_avoid(e)>=2^b and H>=3*2^b when b irreducible pieces are glued. In particular the proof gives at least six cycles universally, tight on the cube. Prisms rule out a universal exponential-in-order lower bound for the full Barnette class.

## Validation and limits

COMPUTED. Direct enumerations cover prisms m=2,...,11, width-4 tubes through L=5, width-6 tubes through L=4, prism chains through q=5, and the first octahedral four-subdivision. State counts equal the incidence determinant. Recovery images have the expected cardinality. Hamiltonian counts agree between primal perfect-matching complements, a general edge-frontier transfer and the stationary induced-tree matrices on their overlapping ranges. All implementations are by this author, so this is not independent referee validation and no T3 promotion is claimed.

COMPUTED. The largest full pair enumeration was dual order 42, primal order 80, from the four-subdivision of three stacked cubes, with 69,984 states, 13,376 pairs and 2,088 tree matchings. The largest separately tabulated simultaneous pair/TM family case was the width-6 tube at L=40, primal order 492. Pair transfer continues to L=102, primal order 1236. The transfer certificates give all-length statements conditional on their finite arithmetic checks, not a general exhaustive verification of the theorem.

The files `code/README.md` and `data/README.md` give all exact commands and provenance. Each observed run was under ten minutes. One short transfer run overlapped the tail of the stack enumeration; that was a scheduling mistake, and subsequent computations were serialized. No process remains running. No subagents were used.

## What failed and what remains open

REFUTED prediction. Four-subdividing stacked cubes did not preserve growing c_min: q=1,2,3 all gave c_min=1. A literal hexagon replacement of a cubic vertex is also underspecified and fails cubicity with only the three original attachments. I used exactly the operation dual to splitting each triangle into four, and did not identify it with leapfrog.

No family with unbounded c_min and no separating triangle was found. Width-6 signed polynomials were computed only through L=4; no full polynomial recurrence or global z>1 positivity proof was found there. The full second iterated octahedral subdivision was not enumerated. General-width nanotube numerical recurrences and inflation growth rates are not solved. These omissions are stated in FAMILIES.md rather than hidden behind the general finite-transfer framework.

The local dashboard and map are confined to `labyrinth/`. Its task frontier records four counted quantities per selected tube length, not a solved classification of all invariant values. All new results require independent referee review before manuscript integration.

## Three best next steps

1. Referee the stationary matrices independently, especially root contraction, forgetting rules, cap color conventions, and the Boolean c_min stabilization. The sparse files are small enough to reconstruct without importing these scripts.
2. Use the width-4 tube as the exposition's first exponential-rarity example, and the nested chain as the worked example with arbitrarily high order of vanishing. Verify their drawings against the given adjacency rules before publication.
3. Search 4-cycle sums or wider tubes for unbounded c_min without triangular separators, and derive a height-weighted transfer for the width-6 signed polynomial. Neither follows from the existing unweighted transfers.

## Leads for others

The universal six-cycle consequence should be checked against known cubic bipartite parity bounds before it is described as new. It is a consequence of this proof, not a novelty claim. The distinction between direct tree matchings at an obstructed root and recursively glued cycles must be retained in the exposition. The two-independent-induced-trees viewpoint made the Hamiltonian transfer substantially smaller than enumerating all primal perfect matchings.
