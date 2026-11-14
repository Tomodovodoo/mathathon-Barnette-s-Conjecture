# Predictions before tests

All predictions start as HUNCH, T6. Tests use exact integer arithmetic.

1. Tree matchings are even, with equally many signs. This is already LIT, constructive Theorem 5.2, and is a validation target rather than a discovery. The stronger positivity certificates `tree count odd`, `signed count = 1`, and `tree count nonzero mod 3` should fail early.
2. Hamiltonian cycles avoiding an edge need not be even. Smith's edge-through parity only implies all three avoidance counts at a vertex have the same parity. Test all edges of all generated graphs.
3. No universal mod 3 action is supplied by the vertex coloring. Predict tree counts divisible by 3 on some unobstructed input. Test plantri through order 12, all facial roots.
4. The signed forest polynomial has both coefficient signs whenever it is nonzero. Predict no positive real incidence gauge can make it coefficientwise nonnegative. Test explicit forest coefficients.
5. A two-species Grassmann formula exists with a local quartic term enforcing disjointness. Predict a Gaussian local decoupling with scalar independent matching weights fails the three-corner cyclic product test. An exact non-Gaussian formula should survive.
6. Tree counts will differ from unrestricted spanning-tree counts, state counts, Tait colorings, and nowhere-zero Z3 flows. Test cube first, then hexagonal prism. Standard invariant comparisons are for these precise graphs, not unspecified normalizations.

Scope: use installed plantri read-only. Counts remain COMPUTED, T4, pending independent validation. No subagents, per the brief.
