# Predictions, written before running the experiments

Recorded 2026-11-14 before any code in `code/` was run. Outcomes are filled in ROUTES.md; this file is not edited afterwards except for the "outcome" pointers at the bottom.

P1 (disk identity, orientation-free form). For every state r, every choice of one out-edge per black face from r(t), and every directed cycle of the chosen edges, the disk it bounds has W = B + 1, whether the cycle is clockwise or counterclockwise. Confidence: high (follows from Lemma 4.1 and signed side counting).

P2 (Gauss-Bonnet form). For every state s and every simple cycle C of T avoiding the roots, B - W = 2m - h + 2, where m counts boundary vertices whose s-matched black face lies inside C. Confidence: high (derived by hand).

P3 (colour winding). delta(u,v) is the lift to {+1,-1} of c(v) - c(u) mod 3 for a proper 3-colouring c of V(T) (consistent over every instance), so J(r,s) is the total winding number of the colour map along the cycles of D(r,s). Confidence: high.

P4 (Hamiltonian cycles versus tree matchings). The recovery map s -> Hamiltonian cycle is injective; its image is a proper subset of the Hamiltonian cycles of G avoiding e0* in at least one instance with at least 12 dual vertices. The number of tree matchings is always even. Confidence: injective high, proper subset medium, even high (follows from the component theorem of barnette_trees.pdf).

P5 (Thomason parity). Every edge of G lies on an even number of Hamiltonian cycles (Thomason). Expected true; serves as a check of the enumerator.

P6 (state lattice). Clock moves (D-cycles of length 3) connect all states (Hine-Kalman). The tree matchings are not an interval of the lattice and are not always an antichain. The top and bottom states are tree matchings in fewer than half of the rooted instances. Confidence: medium-low; this is a guess.

P7 (hypertree position). The hypertree vectors (Kalman) of tree matchings are not characterised by their position in the hypertree polytope: in some instance a tree matching gives an interior lattice point and a non-tree matching gives a vertex, or vice versa. Confidence: medium.

P8 (two-sided degree polytope). In rooted instances with no pair (a separating triangle with black inner boundary), the target degree vector of the incidence tree lies outside the convex hull of two-sided degree vectors of spanning trees of H. Where a tree matching exists the target is of course inside. Confidence: medium.

P9 (saturation). For every H in the sample, every lattice point in the convex hull of the two-sided degree vectors of spanning trees of H is itself realised by a spanning tree. Confidence: low (this would be a genuinely new route if it held).

P10 (nodal lines, the continuum test). Sign patterns of Laplacian eigenvectors of T almost never give a partition into two induced trees (fewer than 5% of eigenvectors over the sample). Confidence: high.

## Outcome pointers (added after the runs)

P1, P2, P3 confirmed; P4 confirmed (the inclusion is strict in 109 of 166 instances); P5 confirmed; P6 partly wrong (top and bottom are often tree matchings); P7 confirmed; P8 confirmed; P9 no counterexample in 8 small cases; P10 confirmed narrowly (4.7%). Details in ROUTES.md.
