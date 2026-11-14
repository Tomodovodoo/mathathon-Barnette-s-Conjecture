# Ranked routes and afternoon tests

These are proposed research tasks, not asserted proofs. Ranks weigh closeness to an exact formulation and how quickly a failed premise can be found. Each mathematical proposal is tagged `HUNCH`; established starting identities are in `REFORMULATIONS.md`. Use one fixed rooting throughout a test, and include separating triangles with each inner-boundary color. An unsuccessful hypothesis should be retained with its smallest counterexample.

## 1. Mixed determinant with positive curvature

[HUNCH] Prove nonvanishing of the coefficient [product z_t] det(sum z_t M_t) from structural hypotheses on the rank-two local matrices. This would give an algebraic version of the central lemma. Start with the exact proved formula in reformulation 3, not an assumed Pfaffian identification. The missing theorem is a complex mixed-determinant positivity statement after a legal phase normalization.

Afternoon test: extend `check_determinant.py` to even bipyramids of rim 8 and to the team's small triangulation corpus. Compute the least nonzero coefficient after b(t,v)=w^{a(t,v)} for integer circulation weights. Compare its degree and phase with minimum union cycle count. Record whether a diagonal gauge makes all matrices Hermitian positive semidefinite. One explicit failure would rule out that simplest normalization.

## 2. Support of the tree-degree polynomial

[HUNCH] Prove that the target degree vector lies in the support of det L_H^{root}(y), using special plane incidence inequalities. This is an unsigned formulation, so there is no cancellation to explain. The desired theorem is stronger than having a real point in a degree polytope.

Afternoon test: enumerate H-trees on the cube and hexagonal bipyramid, collect their degree vectors, and extract the target coefficient. Compare the actual support with all integer points in its convex hull for the relevant degree slice. A hole in that slice would identify exactly why a convexity-only argument fails. Keep the tree matching count as a second check.

## 3. Unique-mate arithmetic

[HUNCH] Use det K_{B-s} to prove a state has a unique mate. Partner counts are zero or powers of two. One might find a congruence for a weighted sum of these counts that cannot be supported entirely on even counts.

Afternoon test: enumerate states and tabulate mate counts, their 2-adic valuations, and the phase of their fixed-s contribution to Z. Check simple candidates such as the number of positive-mate states modulo two. Do not infer a unique mate from an odd total unless the total actually has that parity. Sources are Berman's common-sign determinant and C Proposition 2.1.

## 4. Two-sided hypertree representatives

[HUNCH] Start with the forced center hypertree f and apply the hypergraph Bernardi process. Seek a ribbon/root choice whose representative realizes the required vertex vector g. This asks a concrete question beyond interior-polynomial duality.

Afternoon test: implement one version of Kálmán-Tóthmérész's process on the small corpus. Try all base incidences and both ribbon orientations, logging the resulting vertex degrees. If these choices miss g on a small map, retain that map before enlarging the search. A successful universal family would suggest a structural proof, not yet establish one.

## 5. Three-matroid intersection with a planar certificate

[HUNCH] Exploit the special opposite-edge correspondence to prove integrality or an augmenting-path theorem for P_A intersect P_X intersect M_R. Edmonds's two-way theorem does not apply unchanged. The missing theorem should explain why planarity removes otherwise possible fractional obstructions.

Afternoon test: solve the natural LP with the two partition constraints and graphic rank inequalities for root-contracted opposite edges. Enumerate fractional vertices on n<=7 instances, or separate graphic inequalities dynamically. Compare the optimum for generic random costs with integral states. A fractional vertex refutes full integrality but may leave feasibility at cardinality n intact.

## 6. Local Pfaffian gadget for the turn tensor

[HUNCH] Replace each triangular face by a small planar matching gadget whose boundary signature is q^{delta(u,v)} on distinct ordered corners and zero on equal corners. The local rank-two identity is encouraging; scalar separation is already refuted. A successful gadget could turn Z into a Pfaffian with appropriate boundary extraction.

Afternoon test: write the six turn values and the equal-corner zeros as a boundary signature. Test the relevant matchgate Grassmann-Plücker identities with the boundary order fixed. If they hold, solve for a minimal gadget's edge weights; if they fail, stop claiming a free-fermion reduction of that signature. Sources are Kasteleyn-Percus and Kenyon's block connection model.

## 7. Height potential on pairs

[HUNCH] A combination of the two single-state heights might direct exchanges toward tree matchings. It must handle both first-state-only reversals and simultaneous union reversals. An ordinary single-state clock rank is not enough.

Afternoon test: construct the two state lattices and the pair-exchange graph for small maps. Evaluate linear combinations of their ranks, their height difference's L1 norm, and oriented area. Search for a non-tree local minimum for every candidate. Preserve a counterexample as an exchange component with all potential values. A useful potential must permit a move decreasing it at every non-tree pair.

## 8. Cut cycles into an LGV network

[HUNCH] Choose seams joining the roots and cut the pair diagram into nonintersecting directed paths. If the endpoint order forces one permutation and the path family encodes all choices, an LGV determinant could replace the signed sum.

Afternoon test: perform the cut on the cube and on the first instance with two D-cycles. List endpoints and their cyclic order for every pair. Check whether the resulting path graph is acyclic and whether reconstructing the seams gives a bijection. A seam that depends on the state is a warning, since a single fixed path matrix is required.

## 9. All-minors forest projection

[HUNCH] Insert a three-root Laplacian minor that kills cycles of Q_s while retaining the matching transversal. This may turn the fixed-s involution into an algebraic projection.

Afternoon test: form the root-deleted Laplacian with edge variables indexed by opposite-corner choices. Expand on a small instance and intersect its monomials with the state generating polynomial. Track multiplicities and signs. A Hadamard product or coefficient contraction is exact but not a single determinant unless that extra operation is eliminated. Source is Chaiken's all-minors theorem.

## 10. Matroid parity with a correct gadget

[HUNCH] Encode retaining two spokes per center by disjoint element pairs in a representable matroid, while using additional gadgets to enforce vertex degrees. The overlapping alternatives at a center are the main obstacle.

Afternoon test: design the gadget for ONE black center and its three corners, then combine two adjacent centers. Enumerate feasible parity solutions and compare them with actual partial spoke choices. Reject the gadget immediately if it admits two alternatives at one center, omits a needed degree, or creates spurious cycles. Only after exact agreement should Lovász's algorithm be invoked.

## 11. Bernardi orientations and parking functions

[HUNCH] Carry tree matchings through Bernardi's tree/orientation bijection and express the prescribed spoke degrees as inequalities on a root-connected orientation or a parking function. Such inequalities might be easier to satisfy by burning or chip-firing.

Afternoon test: enumerate all H-trees for n=3 and n=5, compute their Bernardi data under one fixed root half-edge, and classify which satisfy d*. Look for a local criterion in the image, then falsify it against the full list. Root-connected outdegree SEQUENCES are not individual prescribed orientations; retain the distinction.

## 12. Blossom-tree decoder

[HUNCH] A canonical map encoding for Eulerian triangulations may expose a recursive tree matching directly. The challenge is that gluing blossom buds can create long opposite-edge cycles.

Afternoon test: use a checked Bousquet-Mélou-Schaeffer or orientation encoding for the applicable map class. On small decoded maps, choose corners by the parent/bud rule suggested by the encoding. Check bijectivity on X, root placement, disjoint-mate existence and H-s connectivity separately. A failure at a closure edge would suggest what the encoding must remember.

## 13. Schnyder-to-state conversion

[HUNCH] A Schnyder wood might supply one of the two corner assignments and an acyclic orientation for the other. The conversion is not supplied by the fact that both theories use three colors.

Afternoon test: enumerate Schnyder woods on the octahedron and hexagonal bipyramid. For each simple local corner rule based on edge colors and cyclic order, test the state bijection and opposite-edge forest. Try all root-color conventions. A correct rule must be defined facewise without using the desired forest as an oracle. Source is FPS's Schnyder specialization and Bonichon's encoding.

## 14. Boundary transfer algebra

[HUNCH] Give separating triangles a finite boundary state space and express gluing as tensor contraction. This might simplify an exposition or enable dynamic programming on a decomposition with bounded separators. It is not yet a TQFT.

Afternoon test: enumerate boundary labelings and rooted forest-connectivity types on the two sides of one triangle. Write the exact composition table, including which labelings create a cycle. Verify that the same-label-edge prescription is sufficient. Then test whether the state space stays finite under larger boundary cycles or must retain arbitrary connectivity partitions.

## 15. Curved double-dimer connection

[HUNCH] Realize the difference-of-exponentials loop factor using a nonflat diagonal or SL2 connection plus a turning contribution. It must respect trace symmetry under inverse monodromy and exclude doubled edges.

Afternoon test: solve the connection equations on the two bipyramid examples. Compare the trace for each admissible alternating loop with -i exp(xL+)+i exp(xL-), including contractible nested loops. Check trace identities on overlapping loops. Failure of a trace identity rules out that connection assignment; it does not refute the determinant coefficient already proved.

## 16. Random tree conditioning

[HUNCH] Use transfer-current determinants to sample H-trees, then condition or reweight toward d*. A useful existence proof needs a positive joint probability; a useful constructor needs a lower bound large enough for sampling.

Afternoon test: enumerate the exact probability of d* under the uniform tree measure for the smallest maps, then compare product-of-marginal estimates. Search for rapid decay with n and identify the worst degree patterns. A tiny probability does not defeat existence, but it defeats a naive fast rejection sampler.

## 17. Valuation theorem beyond Barnette

[HUNCH] Abstract O's argument into a finite signed cycle system with two involutions and a positive circulation valuation. This could clarify exactly which planar hypotheses are doing work without adding category language.

Afternoon test: list the minimal axioms required by the coefficient proof and try the same construction on a torus and on a triangulated disk with four roots. Find the first failing axiom, likely disk index, holonomy or root count. A precise failed axiom is useful even if no extension survives.

## 18. Induced-forest completion

[HUNCH] Begin with a large induced forest in the Eulerian triangulation and try exchanges that make it and its complement connected while preserving acyclicity. This is farthest from the pair machinery and must use the Eulerian restriction.

Afternoon test: enumerate maximum induced forests on small Eulerian triangulations and test whether some admit a tree complement. Then test single-vertex transfers from arbitrary maximal induced forests. Keep a smallest trapped configuration. Do not use the general Albertson-Berman conjecture as an input: current 2026 preprints report counterexamples for general planar graphs.

## Suggested allocation

The determinant, tree-degree and unique-mate tests reuse the same state enumerator. Run them first. The height and gadget tests can give clean negative results quickly. The Floer, TQFT and generic categorical directions have no identified finishing theorem and are deliberately ranked behind explicit finite tests.
