# Reproducing the calculations

Requirements: Python, networkx, sympy. The installed environment already supplied them. From the repository root run, in order:

    python -B research/2026-11-14_astra_route-dimers/code/explore.py
    python -B research/2026-11-14_astra_route-dimers/code/extra.py
    python -B research/2026-11-14_astra_route-dimers/code/linear.py

explore.py writes data.json with 17 initial rows. extra.py appends the 12-vertex cyclic-mate graph and writes coefficient_check.json. Run explore.py first on every replay, so extra.py does not append duplicates. linear.py writes linear_weights.json for those 18 rows.

The first script imports graph definitions and circulation weights from workings/barnette_lab/barnette_lab/core.py without changing them. It independently implements fraction-free Bareiss determinants, determinant polarization, directed trinity Laplacians and white dual Laplacians. The extra script reads the constructive agent's hard_instance.json. The full edge list and root triangle are also preserved in our data.json. All arithmetic in the checks is exact; no floating-point determinant comparisons are used.

The family generator uses seed 14112026, even bipyramid seeds and random octahedral face insertions, followed by two sampled roots for each requested size. These are structured examples, not uniformly random triangulations and not an exhaustive census. Named cases are the octahedron, hexagonal-prism dual and truncated-octahedron dual. The appended 12-vertex case checks actual nonforest cancellation.

Each process completed in a few seconds locally. Tests include all state pairs of each sampled rooted graph. Determinant polarization runs on cases of n<=8 and on the two named larger tests. It costs 2^n integer determinants. White-tree coefficient checking enumerates edge subsets only at 6 and 8 vertices. Computational evidence is T4 because the shared state model has not received independent verification in this task.

Serialization warning: a face's numeric index depends on embedding construction. Reconstruct the root using its three vertices, not its saved face index. linear.py does this. Re-embedding can change the circulation gauge, and hence the univariate polynomial, while preserving counts and the order of vanishing.
