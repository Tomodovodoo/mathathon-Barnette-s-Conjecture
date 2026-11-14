# Predictions before computation

I use the repository's unslop and labyrinth skills. All new proofs are T2 unreviewed; computed evidence is T4 until an independent referee checks it.

1. CONJECTURE. The 2m-prism has m states, two pairs, two tree matchings and c_min=1. Its sole D-cycle encloses m-1 inner white faces, so its signed polynomial, after an exponent shift and overall sign, is z^(m-1)-1. Test m=2 through 12.
2. CONJECTURE. White-face sums of q rooted prisms have multiplicative state and pair counts, c_min=q and exactly 2^q tree matchings. Test q=1 through 6 and roots of other types.
3. HUNCH. Fixed-width hexagonal tubes have a bounded c_min. Test the alternating-diagonal cylinder defined in code/families.py at widths 4 and 6. This prediction is deliberately stronger than parity alone.
4. HUNCH. Uniform four-subdivision of every dual triangle produces growing c_min under iteration. Test the octahedron and the first subdivision before attempting a larger run.

The ground truth is finite enumeration of incidence matchings and complements of primal perfect matchings. Enumeration will fail before determinants do. Transfer across a separating triangle should provide the first complete infinite-family result. No subagents are permitted. Each local run has a 540-second deadline and only one heavy process runs at a time.
