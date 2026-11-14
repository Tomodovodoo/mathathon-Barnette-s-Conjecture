# Conjecture tests and limits

All new numerical evidence is COMPUTED, T4, under review. No referee was launched, as the brief forbids subagents. The independent checks below mean separate implementations by this author, not independent refereeing. PROVED-HERE means T2 unreviewed.

## M >= 2^c_min

PROVED-HERE. Even prisms realize equality M=2, c_min=1. The white-face q-prism chain realizes equality M=2^q, c_min=q for arbitrarily large q. Therefore the conjectured exponential bound, if true, is sharp for every positive value of c_min. It cannot be improved by a uniform factor greater than one. The established 2c_min bound is sharp at q=1,2 and has ratio 2^(q-1)/q thereafter.

COMPUTED with exact transfer certificates. Width-4 tubes realize equality for all lengths in the stationary model. Width-6 tubes have c_min=1 and increasingly many tree matchings. Here the lower bound is asymptotically very loose. Pair-cost Boolean stabilization certifies c_min=1 in both stationary transfers, not just through the largest table. These infinite conclusions depend on the still-unrefereed transfer arithmetic and state conventions in FAMILIES.md.

COMPUTED. The first octahedral four-subdivision has M=12,c_min=1. Four-subdivided stacked cubes with q=2,3 have M=160,2088 and c_min=1. No violation appears, but this supplies no large-c_min evidence without separators.

The next discriminating test should target minimum cycle count in families joined across 4-cycles. Increasing L in the two solved tube widths does not test the conjecture beyond exponent 1.

## 3M <= H

PROVED-HERE in the already-refereed combinatorics report, not an open conjecture. For a fixed black root, its three prescriptions give disjoint images, each of cardinality M. Prisms have ratio 3/(m+1); only the cube gives equality. The q-prism chain has ratio 3*2^q/[20*3^(q-2)] for q>=2, tending to zero. The two tube transfers also give ratios tending to zero. Hence no universal constant fraction of all Hamiltonian cycles comes from a fixed root's tree matchings.

COMPUTED. Direct recovery was checked for every tree matching and all three prescriptions at the listed prism roots m=2,...,11, tube widths 4 through L=5 and 6 through L=4, q-prism chains through q=5, and the octahedral first subdivision. Every image count equals 3M. All direct HC totals were obtained independently by complementing primal perfect matchings. `count.py` asserts image cardinality and the inequality.

## c_min and rarity

PROVED-HERE. The q-prism chain has unbounded c_min=q, with separators. The two tube models have no separating triangle. Their certified pair transfers have c_min=1, so they do not meet the requested fifth-family condition.

REFUTED prediction. Four-subdividing stacked cubes did not preserve their increasing c_min. The three cases q=1,2,3 all have c_min=1 after subdivision. Lesson: removing triangular separators can create new low-cycle pairings, so a c_min certificate cannot be transported through subdivision without controlling those new states.

COMPUTED certificate consequence. Rarity M/S is exponential even in the no-separator width-4 tube: 2/Fib_(2L+3). At width 6 the per-layer ratio tends to the quotient of dominant growth rates, about 2.382975768/5.613134261. The earlier limits report's exponential-rarity phenomenon therefore does not require triangular separators. Independent referee confirmation of this new infinite-family strengthening is pending.

## What was confirmed directly for Proposition 5.1

COMPUTED, finite and reproducible. The largest full state-and-pair enumeration in this folder is the four-subdivision of three stacked cubes: dual order 42, primal order 80, 69,984 states, 13,376 ordered pairs and 2,088 tree matchings. `subdivided-stacks.json` records it. No Hamiltonian enumeration was attempted for that instance.

COMPUTED, transfer rather than full enumeration. Width-6 tube L=40, primal order 492, has positive P by the pair transfer and positive M by the matching transfer. The saved pair transfer reaches L=102, primal order 1236, but M was not separately tabulated there. The stationary recurrence certificates give an all-length argument conditional on their finite arithmetic verification. Do not call those lengths exhaustive state enumeration or a general verification of Proposition 5.1 outside the family.

## Signed-polynomial tests

PROVED-HERE. Prism and nested-chain polynomials factor into positive factors z^d-1 for z>1. Width-4 tube polynomials have the same one-factor form, conditional on the certified two-pair transfer. Their unweighted evaluations at z=1 all vanish. The coefficient controlling existence counts one enclosed white face per minimal D-cycle, not the unsigned number of tree matchings.

COMPUTED. Width-6 tube signed polynomials through L=4 have mixed coefficients; the coefficient lists are retained, including cancellations. No claim that their quotient by (z-1)^c_min has nonnegative coefficients is made. No recurrence for the full width-6 signed polynomial has been found. Its positive leading coefficient is supplied by the original theorem, not by a new family-specific positivity recurrence.
