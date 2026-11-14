# Refereed statements for integration

Independent referee: gpt-6.1-sol, 14 November 2026.

All propositions below are `PROVED-HERE`, tier T2 with one independent AI referee, human checking pending. They are not promoted to published literature. The numerical examples are `COMPUTED`; their commands and exact ranges are in `code/README.md`. The two referee files record corrections to the submitted proofs.

## Setting and inputs

Let T be a finite simple sphere triangulation with its faces properly coloured black and white. Choose a black outer face t0 with root set R, let A be the other black faces, and let X be the nonroots. Write n=|A|=|X|. There are n+1 faces of each colour, n+3 vertices and 3n+3 edges. H is the incidence graph of all black faces and their corners, and B is obtained by deleting the outer centre and the roots. A state is an incidence bijection s:A→X. Its opposite-edge graph Q_s has one edge opposite s(t) in each t∈A. A tree matching is a state for which H−s is a spanning tree.

We use sphere tree/cotree duality, integral max-flow and the Jordan curve theorem. For the existence conclusion after the pair criterion we use OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, 24 September 2026, Proposition 5.1 and Section 6. These are supplied preprint results, not a claim of external publication. The structural arguments below are independent proofs of the requested surrounding statements. A manuscript retaining its own proof of Proposition 5.1 need only cite that earlier proposition.

## 1. An exact Euler identity

`PROVED-HERE`. Let K be a connected induced subgraph of T on p≥3 vertices, with m edges. A face of K is actual if it is a face of T. Let b count its actual black faces. For each remaining face region F, let d(F) be its boundary length, counting edge sides with repetition, and let β(F) be the number of original black faces in that region minus the number of original white faces there. Then

\[
m-b-(2p-4)=\frac12\sum_{F\text{ not actual}}\bigl(\beta(F)-d(F)+4\bigr).
\tag{1}
\]

Proof. Let w count the actual white faces and let q be the number of remaining regions. Euler's formula and the side count give

\[
p-m+b+w+q=2,\qquad
2m=3b+3w+\sum_Fd(F).
\]

Consequently

\[
m-b-2p+4=-m+b+2w+2q
=\frac12\left(w-b-\sum_F(d(F)-4)\right).
\]

The original faces partition into actual faces and the faces in the remaining regions. The total black-minus-white balance on the sphere is zero, hence w−b=Σ_Fβ(F). Substitution proves (1). This reasoning includes bridges, whose two sides are counted separately. ∎

`PROVED-HERE`. If σ_j is +1 or −1 according as the original face on the region side of boundary side j is black or white, cancellation of internal sides gives

\[
3\beta(F)=\sum_{j=1}^{d(F)}\sigma_j.
\tag{2}
\]

Thus |β|≤d/3 and β≡d modulo 2. When d=3, β=±1 and β=1 precisely when all three inner incidences are black. For d=4 parity forces β=0; for d=5 it forces β=±1; for d≥6, d/3≤d−4. Therefore β≤d−4 for every d≥4. A nonactual triangular region contributes +1 to (1) when its region-side incidences are black, and zero when they are white. ∎

## 2. The exact pair criterion

`PROVED-HERE`. The reduced incidence graph B has two edge-disjoint perfect matchings if and only if T has no separating triangle with black inner boundary. Inner means the side not containing t0. Such a triangle is an obstruction of capacity deficit exactly one.

Proof. Give capacity two to source-to-X edges and A-to-sink edges, and capacity one to incidence edges. For S⊆X, minimizing a cut over the placement of A gives capacity

\[
2(n-|S|)+\sum_{t\in A}\min(2,|V(t)\cap S|).
\]

Integral max-flow and alternation on bipartite cycles therefore make a pair equivalent to

\[
\sum_{t\in A}\min(2,|V(t)\cap S|)\ge 2|S|
\quad(S\subseteq X).
\tag{3}
\]

Put U=V(T)\S, and let e(U) count edges of T[U] and b(U) its actual black faces, including t0. Include t0 in the shortfall sum. A black face with j corners in U has shortfall max(0,j−1), equal to the number of its U-edges minus one if j=3. Each edge has one black owner. Hence (3) is equivalent to

\[
e(U)-b(U)\le2|U|-4\quad(U\supseteq R).
\tag{4}
\]

If Δ has black inner boundary, take U to contain every vertex outside its strict interior. The induced graph T[U] is connected and has exactly one nonactual region, the disk bounded by Δ. Its data are d=3 and β=1. Equation (1) gives e(U)−b(U)=2|U|−3. The inequality fails by one, and the corresponding flow cut has capacity 2n−1.

Conversely, suppose there is no such triangle. The component K_R of T[U] containing R contains all three roots, since they are pairwise adjacent. If it has order three, then m−b=3−1=2=2p−4. If its order is at least four, apply (1). Regions of length at least four contribute at most zero. A nonactual triangular region contains an original vertex on its region side, and K_R has a vertex on the other side. Its boundary is therefore separating. Since t0 is an actual face of K_R, the region side is the inner side. Our hypothesis forces β=−1, giving contribution zero. Thus m−b≤2p−4 for K_R.

For any other component of order at least four, the same argument applies except to its one region containing t0. That region contributes at most one if triangular and at most zero otherwise. Thus m−b≤2p−3≤2p. For components of order one, two or three the bound m−b≤2p follows directly from simplicity. Summing over components proves (4). This proves both directions. ∎

`PROVED-HERE`, using the central existence proposition. A tree matching exists exactly under the same criterion. Indeed H−s is obtained by subdividing the edges of Q_s and adding a star at the three roots. Therefore H−s is a tree if and only if Q_s is a forest with exactly one root in each component. Orienting these trees towards their roots produces a unique disjoint mate. Conversely a pair gives outdegree one on X and zero on R in Q_s; Proposition 5.1 supplies a pair with Q_s a forest, and the component outdegree count forces one root per component.

The last paragraph invokes the central existence proposition. The equivalence between a pair and the separator condition does not.

## 3. The sharp primal hypothesis

`PROVED-HERE`. Let G be a finite simple cubic bipartite 3-connected plane graph and let b0 be the black vertex dual to t0. Then Li's reduced face/black-vertex incidence graph has a 2-factor if and only if every nontrivial 3-edge cut has b0 on its black-ended shore. This is a condition on the chosen black root, not an unrooted connectivity condition.

Proof. There is no edge cut of size one or two in G. Each shore of such a cut would have more vertices than its at most two boundary endpoints, by cubicity and simplicity, and deleting those endpoints would violate 3-connectivity.

Every 3-edge cut is a bond: if a shore had two components, their boundaries would each have size at least three, contrary to the total cut size. Sphere duality sends its bond to a 3-cycle of T. It is nontrivial exactly when the dual triangle has vertices strictly on both sides. To see the cyclic condition directly, a nontrivial shore Y has odd order at least three and spans (3|Y|−3)/2≥|Y| edges, so it contains a cycle. Conversely a shore with a cycle cannot be a singleton.

Write δ_B and δ_W for the cut edges with black and white endpoints in Y. Counting internal edges from the two colour classes gives

\[
3(|Y\cap B_G|-|Y\cap W_G|)=|\delta_B|-|\delta_W|.
\]

The right side is one of −3,−1,1,3 and is divisible by three. Thus all three Y-endpoints have the same colour, and the other endpoints have the opposite colour. The black inner-boundary triangles are precisely the cuts whose shore avoiding b0 has black endpoints. The result now follows from Section 2. ∎

This statement supplies the exact hypothesis for Li's Lemma 9. It does not assert that Li's entire exposition has already been rewritten under that hypothesis.

## 4. Gluing only at an obstruction

`PROVED-HERE`, with the direct pair-to-partition construction as input. For every rooted T and every e0∈E(t0), there is a partition into two induced trees with the endpoints of e0 together and the third root apart. One can obtain it by cutting only at black inner-boundary triangles, always relative to the current root and current face colouring.

Proof. Induct on |V(T)|. If Section 2 supplies a pair, the direct construction applies to the whole rooted triangulation. Its weighted cancellation and recovery steps require a pair and the sphere triangulation hypotheses; they do not use the absence of other separating triangles.

Otherwise choose a black inner-boundary triangle Δ. Cut along Δ and cap each side with a triangular face. Both pieces are simple and smaller. On either side, (2) makes three times the face balance a sum of three signs. Divisibility forces those signs to be equal. Give the cap the opposite colour. The alternating fan at each boundary vertex then has odd length, and adjoining the cap makes the degree even. Both capped pieces are Eulerian triangulations.

Solve the outer piece with its original prescription. On its cap both tree labels occur, for otherwise one induced tree would contain the cap triangle. There is exactly one same-label cap edge e1. Solve the inner piece with its cap as root face and e1 as prescription, exchanging face colours if necessary. Rename its two tree labels to agree on Δ.

For each label, its two trees intersect in a single vertex or a single edge with its endpoints. The union is connected, and its edge count is its vertex count minus one, so it is a tree. It is induced because there is no edge between the two strict interiors and the label classes agree on Δ. The original root prescription survives. The induction terminates because both children are smaller. ∎

The complementary dual edges form one Hamiltonian cycle and omit e0*. This follows because every triangle has one same-label edge, so the complementary dual is 2-regular; the selected edges form a spanning forest, so complementary sphere duality makes that dual connected.

## 5. Which Hamiltonian cycles the direct construction produces

`PROVED-HERE`. Fix t0 and e0. Let C be any Hamiltonian cycle of G avoiding e0*, and let P be the primal-dual complement of C in T. Then P consists of two induced trees. Deleting e0 leaves three trees, each containing one root. Orient P−e0 towards the roots, and define s_C(t) to be the tail of its unique edge in t, for t∈A. This defines a state. Moreover:

1. For every tree matching s, the direct construction gives s_{C(s)}=s. In particular it is injective.
2. The cycle C is produced precisely when H−s_C is a tree.
3. Equivalently, C is produced precisely when s_C has a disjoint mate. If C is missed, s_C has no disjoint mate at all.
4. The equivalent white parent-map test is acyclicity on the white faces, with the white face across e0 as its unique sink.

Proof. The Jordan curve C labels the vertices of T by its two sides. An edge is in P exactly when its ends have the same label. There is one selected edge per triangular face, hence |P|=n+1. Removing any edge f from C gives a spanning tree of G. Its complementary dual P∪{f*} is a tree of T, so P is a forest with two components. Each component has a constant label and both labels occur. Thus each label class is exactly one component and induces a tree. The only P-edge of t0 is e0. Removing it gives the asserted three rooted trees. Each nonroot is the tail of exactly one edge, and each bounded black face owns exactly one such edge. Thus s_C is a bijection.

Let W_s be the plane dual graph of the deleted spokes of s on the white faces. For each black t it has an edge joining the white faces across the two sides of t incident with s(t). It has n edges and n+1 vertices, and H−s is a tree exactly when W_s is a tree. When W_s is a tree rooted at y0, there is a unique assignment of its edges to incident endpoints which uses every white face except y0 once. Assign each edge to its endpoint farther from y0. The sides selected by P give exactly such an assignment. Therefore the constructor returns P whenever s=s_C is a tree matching. Conversely the constructor orients P−e0 out of s(t), with outdegree one on X and zero on R. In a rooted forest that is the orientation towards the roots. This proves assertions 1 and 2, including injectivity.

Here is an independent proof of the stronger assertion 3, following the fable report's supplied route. Suppose W_s is not a tree. Since it has n edges on n+1 vertices, it contains a cycle. Choose an embedded simple cycle Γ, permitting a two-edge cycle if the white graph has parallel edges. Draw it through its white-face interiors and through black faces t_1,...,t_q. In t_i it crosses exactly the two sides incident with s(t_i). It crosses no side of t0. Take the disk side avoiding the roots, let S be its original vertices, let σ=|S|, let B_i,W_i count black and white triangular faces strictly inside, and let a count those crossed black faces whose selected corner s(t_i) lies inside.

The selected sides P pair all black faces with white faces. A crossed black face is paired across one of its two crossed sides to a white face on Γ. The q crossed black faces therefore consume exactly the q white faces on Γ. Every strictly interior face must consequently be paired to another strictly interior face. Hence B_i=W_i.

No edge of Q_s crosses Γ: in a crossed black face its selected edge is the opposite side. An edge with both endpoints in S belongs either to a strictly interior black face, contributing three edges per such face, or to a crossed black face whose selected corner is outside, contributing one. Thus

\[
e_T(S)=3B_i+q-a.
\]

Subdivide at the 2q crossing points. The closed disk has σ+2q vertices, e_T(S)+4q edges including its boundary, and B_i+W_i+2q regions. Euler's disk formula gives

\[
\sigma=e_T(S)-B_i-W_i+1=B_i+q-a+1.
\]

Exactly B_i+q−a=σ−1 edges of Q_s lie inside. There are no Q_s edges leaving S and no roots in S. If s had a mate, orienting Q_s by that mate would give one outgoing edge at every vertex of S, forcing exactly σ internal Q_s edges. This contradicts σ−1. Thus s has no mate. The reverse implication in assertion 3 follows from the unique mate of a tree matching.

For assertion 4, the selected edge in a white face z≠y0 belongs to a black face t_z and has tail s(t_z). Let par(z) be the other white face at that spoke. The map z↦t_z is bijective onto A. Its n parent arcs are exactly the edges of W_s, with outdegree one away from y0 and zero at y0. Such a functional graph is acyclic exactly when all paths reach y0, equivalently when W_s is a tree. ∎

`COMPUTED`. The hexagonal prism has three states, two tree matchings, and four Hamiltonian cycles avoiding the saved prescribed edge. Only two are produced. The reverse map from all avoiding cycles to states need not be injective. There is no contradiction with the injectivity of the forward map on tree matchings.

## 6. Exponential rarity under white-face sums

`PROVED-HERE`, with a finite local enumeration supplied below. There are rooted triangulations with n=5q, exactly 3^q states and exactly 2^q tree matchings. Their tree fraction is (2/3)^q, and their primal order is 10q+2.

Use the hexagonal-prism dual with root {0,1,2} and bounded black faces

\[
(0,5,6),\ (0,3,4),\ (2,7,3),\ (1,6,7),\ (4,7,5).
\]

In that order its states are

\[
(5,3,7,6,4),\ (5,4,3,6,7),\ (6,4,3,7,5).
\]

The first and third states are disjoint and are tree matchings. The middle state shares a choice with each of them, so it has no mate. To check the tree property directly, the first state's opposite edges are {06,04,23,17,57}, whose three components have roots 0,1,2 respectively. The third state's opposite edges are {05,03,27,16,47}, again with one root per component. These three states exhaust the bijections, as can be checked by assigning the two choices in the first face and continuing through the five rows.

Insert q−1 additional copies into white faces, removing the black cap of each inserted copy. Each insertion adds five vertices and five bounded black faces. New vertices have no old incident black faces, so a perfect matching must match all five new black faces to the five new vertices. Thus states and disjoint pairs factor into the rooted local states and pairs.

The local tree states have Q consisting of three trees rooted at the boundary. Adding those trees to the old rooted Q forest attaches one tree at each boundary vertex and makes no cycle; each resulting component retains its single outer root. Hence every tuple of local tree states is a global tree state. Conversely a global tree state has a disjoint mate, which restricts to a local disjoint pair in every copy. The local enumeration has just two states participating in pairs, both tree states. Therefore exactly 2^q global states are tree matchings, out of 3^q. ∎

The local enumeration and all q=1,...,6 counts were independently reproduced by `code/limits.py examples`.

## 7. The two natural matroid triples

`PROVED-HERE`. On the full spoke set E(H), let P_c have capacity one at each bounded centre and zero at t0, and let P_v have capacity one at each nonroot and zero at each root. The tree matchings are precisely the common bases of M*(H), P_c and P_v. Equivalently, map every spoke to the side opposite its corner and identify the roots of T. They are the common bases of M(T/R) and the two transported partition matroids.

Proof. All three matroids in the first formulation have rank n. A common basis of the two partitions is exactly a state. It is a cographic basis exactly when its complement is a tree. For the second formulation, the centre partition ensures that every bounded black centre retains exactly two spokes, and the outer centre retains three. Suppressing bounded centres identifies the retained graph with Q_s together with the outer star. Hence it is a tree exactly when the opposite edges form a tree after root identification. This proves equivalence of the common-base families. It does not identify the two individual matroids before imposing the centre partition. ∎

`PROVED-HERE`. Neither complementing the displayed common bases nor relabelling the cographic matroid by plane duality removes either partition constraint. A partition matroid with block size m and capacity c has dual block capacity m−c. Thus these operations give another displayed triple. The independent small examples in the referee report show that each natural constraint matters. They do not rule out all other representations.

## 8. The alpha-orientation quotient

`PROVED-HERE`. Suppose a pair exists. Let d_v be the number of black faces incident with v in the full triangulation. Pairs modulo independent reversal of D-cycles are in bijection with orientations of H−t0 having outdegree two at every centre, d_x−2 at x∈X, and d_r−1 at r∈R.

Proof. The pair union is a 2-factor of B. Conversely each bipartite cycle of a 2-factor has two alternating decompositions, independently of the other cycles. In each bounded black face let u(t) be the unused corner. Direct its unused spoke from corner to centre and its two used spokes from centre to corner. This has the prescribed outdegrees. At a root every incident spoke in H−t0 is unused, while each nonroot is incident with exactly two used spokes.

Conversely the centre outdegree condition leaves exactly one corner-to-centre spoke at every bounded centre. The root outdegree equals the root's whole degree in H−t0, so no centre-to-corner spoke ends there. Each nonroot has exactly two incoming spokes. Therefore the centre-to-corner spokes form a 2-factor of B. These two constructions are inverse after quotienting by the alternating cycle choices. ∎

`LIT`. Felsner, *Lattice Structures from Planar Graphs*, Electronic Journal of Combinatorics 11(1), 2004, R15, Theorem 1, then gives a distributive lattice because the alpha function is feasible. The full paper was opened at https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r15/pdf/ . Its directed essential cycles must be retained in the statement; original facial flips need not generate all relevant moves.

## 9. The corrected degree-four lift statement

`PROVED-HERE`. Let T be obtained from T' by splitting a nonroot v into nonroots v1,v2 and inserting a degree-four nonroot x, without changing t0. Let the other neighbours of x be a,b, and let its two black faces be β_a,β_b. States of T' are in bijection with the states of T whose choices on β_a,β_b avoid {a,b}.

For such a lift s of s', let t* be the old face assigned v by s'. Its corner in T is v*, and the other split copy is v_o. The new black face through v* is assigned x; call its a-or-b corner c2. The other new black face is assigned v_o; call its a-or-b corner c1. Then

\[
Q_s=\operatorname{split}(Q_{s'})\cup\{xc_1,c_2v^*\}.
\]

If s' is a tree matching, s is a tree matching exactly when c2 belongs to the v_o component obtained by splitting v in Q_{s'} augmented by a two-edge path through the roots.

Proof. Every old assignment lifts to its unique original corner, except that the merged corner v lifts to v* in t*. The uncovered nonroots are then x and v_o. Of the two new black faces only the one through v_o can take that vertex; the other must take x. This proves the bijection and the displayed opposite-edge formula.

For the last assertion, the augmented Q_{s'} is a tree. Splitting v leaves two components, containing v* and v_o respectively, including the possibility of an isolated split copy. The new edge xc1 makes x a leaf. The remaining new edge c2v* joins the two components exactly under the stated condition. The resulting augmented graph is a tree precisely in that case, proving the assertion. ∎

The assertion assumes that s' is a tree matching. It makes no claim that every tree lift contracts to a tree matching. That reverse implication is false.

## 10. The abstract hardness result

`PROVED-HERE`, with published source input. Deciding whether a planar bipartite graph of maximum degree three has a perfect matching with spanning-tree complement is NP-hard under polynomial Turing reductions.

Proof. Akiyama, Nishizeki and Saito prove NP-completeness of Hamiltonicity for 2-connected cubic bipartite planar graphs in Journal of Information Processing 3(2), 1980, 73–76. Let G be such an input, and choose two edges e1,e2 at one vertex. For e=uw, form K=G−e. A Hamiltonian cycle through e has a complementary perfect matching of K, and deleting that matching from K leaves a spanning path. Conversely a perfect matching of K with tree complement leaves degrees one at u,w and two elsewhere, so that tree is a spanning path, closed to a Hamiltonian cycle by e. Every Hamiltonian cycle uses e1 or e2. Two oracle queries and their OR therefore decide the source problem. ∎

The original scan was opened at https://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J029.pdf . This result concerns the broader graph class and is not a hardness theorem for finding a tree matching in the total special spoke class.

## What should stay out

`REFUTED`. Do not state the unqualified reverse implication in Opus Lemma 6.2(iii). A tree lift can contract to a non-tree state. Retain the forward conditional side test only, with the split vertices required to be nonroots or with a separate root case.

`REFUTED`. Do not identify the cographic restriction of H with the graphic matroid on opposite edges of T/R on arbitrary subsets. The identification of tree conditions is valid after imposing one deletion per bounded centre. Both three-matroid formulations are valid, but that does not prove a matroid isomorphism.

`GAP`. Do not infer that no possible two-matroid description or min-max theorem exists. The natural triple is irredundant, the natural LP has fractional vertices, and the broader decision problem is NP-hard under polynomial Turing reductions. Those conclusions do not exclude every encoding of the special spoke class.

`COMPUTED`, with limits. The LP has a half-integral vertex at V=13. Do not call 13 the first order on the strength of a random-objective search. Do not describe the saved fractional support as averaging two non-tree states: a feasible completion has one tree state and one non-tree state.

`REFUTED` as descriptions of saved data. The saved 80-vertex alpha maximum is not an actual lattice maximum. It has directed cycles in both senses. The general failure of each extreme is nevertheless real, with independently certified examples at 40 and 120 vertices.

`CONJECTURE`. O6 and monotone D3 remain conjectures. A face-flip terminal orientation must not be substituted silently for a lattice extreme. The tests here support the precisely defined versions but do not prove them.

`REFUTED`. Nonvanishing of the first potentially nonzero coefficient is sufficient, not necessary, for Z to be nonzero with arbitrary weights. The 14-vertex integer-weight example in `code/weights-leading-zero.json` has its degree-one coefficient zero and Z nonzero.

`GAP`. Treat the arbitrary include-one/avoid-another and Hamilton-laceability rows as finite tests, unless an exact general source or proof is supplied. The verified P4 consequence through Gorsky, Steiner and Wiederrecht is a published equivalence applied to the supplied existence proof, not an independent unconditional reproof of that existence input.
