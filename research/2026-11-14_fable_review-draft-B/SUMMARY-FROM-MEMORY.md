# The proof, from memory after one reading of draft B

Written straight after the cold read, without reopening the PDF or my log. Where I was unsure I say so in brackets; those places are data about the exposition.

**Statement.** G cubic, bipartite, planar, 3-connected, e an edge. Then G has a Hamiltonian cycle avoiding e.

**1. Dual picture.** Embed G in the sphere and take the dual T. Because G is cubic, faces of T are triangles; because G is 3-connected, T is a simple graph; because G is bipartite, the faces of T are coloured black and white with one of each at every edge. There are k black faces, k white faces, 3k edges, k + 2 vertices. A perfect matching of G is a set P of edges of T with exactly one side of every face (a "selection"). By a duality lemma (an edge set is acyclic if and only if the dual of its complement is connected), the complement of the matching is a Hamiltonian cycle exactly when P has no cycle. Then P is a forest with two components, and each component contains every edge between its own vertices. So the theorem asks for an acyclic selection containing the edge e0 that crosses e.

**2. States.** Take the black face t0 at e0 = ab, third corner c; a, b, c are the roots. A = the other black faces, X = the other vertices, both of size n = k − 1. If P is an acyclic selection containing e0, remove e0: three trees, one root each. Orient towards the roots; each black face in A has one side in P, and its tail is a corner of that face. This gives a bijection s: A → X with s(t) a corner of t. Call any such bijection a state.

Conversely, from a state let Q_s be the sides opposite the chosen corners, and S_s = Q_s plus ac and bc. If S_s is a spanning tree of T (equivalently Q_s is a forest whose three components each contain one root: "s is good"), then the dual complement Y_s is a tree on the faces, t0 is a leaf, every other black face has degree two. Root it at t0; each black face selects the side shared with its child. This is a selection P_s containing e0, and its side in each t passes through s(t).

**3. Disk identity.** For a state r, pick in each black face one of the two sides at r(t), directed away from r(t). A directed cycle Z of such sides with h edges encloses B black and W white faces with W = B + 1 and h = 2ℓ + 3, where ℓ counts the edges of Z with their black face inside. Proof: three equations. Euler for the disk: B + W = 2I + h − 2. Signed count of face sides: 3(B − W) = 2ℓ − h. And B = I + ℓ, because r sends the black faces inside bijectively to the interior vertices plus those cycle vertices whose outgoing edge has its black face inside. [I remember that Euler is applied without saying why the disk graph is connected.]

Consequence: P_s is acyclic for good s. A cycle in P_s minus e0 would be a directed cycle of such sides; matching the faces inside across P_s gives W − B = h − 2ℓ = 3, against W − B = 1. Then a count of outdegrees shows each tree of P_s minus e0 has one root, so adding e0 closes no cycle.

So: a good state gives the Hamiltonian cycle. It remains to find a good state.

**4. Pairs.** A pair (r, s) is two states with r(t) ≠ s(t) everywhere. Directing each edge of Q_s from r(t) to the third corner u(t) gives every non-root outdegree one, roots outdegree zero. So each component of Q_s is a tree with one root or has no root and one directed cycle. Hence, when s has a partner, s is good if and only if Q_s is acyclic. The edges r(t) → s(t) form D(r, s), a set of disjoint directed cycles covering X. Cycles of Q_s and cycles of D are both made of "chosen sides" for r, so the disk identity applies to both.

Two moves. (i) Reverse a cycle K of Q_s: on its faces, move r(t) to u(t). Keeps s. (ii) Reverse a cycle C of D: swap r and s on its faces.

Sign. δ(v, w) = +1 if the black face of vw is to the left of v → w. J(r, s) = (1/3) Σ δ(r(t), s(t)) = number of clockwise cycles of D minus counterclockwise, by the disk identity (each cycle sums to ±3). ε = (−1)^{(n+J)/2}. Both moves flip ε: for (ii) clear; for (i) a local identity in each triangle, δ(u,s) − δ(r,s) = 2δ(r,u), sums to twice the δ-sum of K, which is ±3, so J moves by ±2.

Cancellation. For fixed s with Q_s cyclic, reversing the first cycle of Q_s (first in a fixed order, chosen from s alone) is a sign-reversing involution on partners. So Σ over pairs of ε·F(s) equals the same sum over pairs with s good, for any F.

Nonvanishing. F = 1 fails because move (ii) also flips the sign. Choose F to see orientation: for each white face w, a path from a point in w to the outer face; h_s(w) = signed number of crossings of that path with the spokes (centre of t to s(t)); ω(s) = Σ_w h_s(w). Reversing a clockwise cycle C of D to counterclockwise raises h(w) by 1 for w inside C and by 0 otherwise [proof: the spokes of the faces on C form a closed curve homotopic to C inside the black triangles, and signed crossings equal winding number]. So ω rises by L(C) = number of white faces inside C, at least 1 by the disk identity.

Let m = minimum number of cycles of D over all pairs. Take F = ω^m. Group pairs by the undirected edge set of D; a group with c cycles has 2^c members indexed by orientation bits, ε = const·(−1)^{Σ x_i}, ω = b + Σ x_i L_i. The alternating sum of an m-th power of an affine function over c bits is 0 if c > m and (−1)^m m! Π L_i if c = m. So the total is ± m! Σ over minimal groups of Π L(C) ≠ 0. Hence a good state exists whenever one pair exists.

**5. First pair.** A pair is a 2-factor of the bipartite incidence graph on A ∪ X. By max-flow min-cut it exists if Σ_t min(2, |t ∩ S|) ≥ 2|S| for all S ⊆ X. Rewritten with U = complement: e(U) − b(U) ≤ 2|U| − 4. Proved component by component of T[U] with Euler and the signed side count: a face of length d in the component has black-minus-white excess at most d − 4. This uses that a triangle of T bounds a face on one side, i.e. no separating triangle. [I do not remember the exact chain of inequalities at the end.]

**6. Separating triangles.** Cut T along a separating triangle into two pieces, each closed by a cap face. The three faces along the triangle on one side have the same colour, so the cap takes the other colour. Induct: get an acyclic selection P1 of the piece containing t0 with e0; it uses one side e' of the triangle; get P2 of the other piece containing e'. The union is a selection, and it is acyclic because in each piece the two ends of e' are in one tree and the third vertex in the other (the "each component is induced" statement from step 1).

**7. Remarks.** Where each hypothesis is used; a 2-connected counterexample from three cubes minus an edge; not every Hamiltonian cycle comes from a good state (hexagonal prism).

**Example.** 13 vertices, 22 faces, n = 10; 12 states, 8 pairs, 6 good states; two groups with m = 2, total 2!(6·1 + 3·1) = 18.

## What I could not reproduce

- The precise conventions in the definition of heights (which crossing direction counts +1) and why the paths do not matter.
- The end of the density bound in Section 5 beyond "Euler plus |β(F)| ≤ d − 4".
- The orientation bookkeeping in Lemma 4.4 for move (i) beyond the local identity.
- How the route's opening promise, "every construction is there to enforce connectivity", applies to Sections 4 and 5. I can say what those sections prove but not how to tell it as a connectivity story.
- Why two states: I can repeat "the partner turns 'one root per component' into 'no cycle'", and that is a reason for the pair. I cannot give a reason for the signed count other than that it works.

## What stuck without effort

- Degree two is easy, one cycle is hard.
- A selection is one side per triangle; Hamiltonian if and only if acyclic.
- The state is read off the answer (Lemma 3.1) before it is defined.
- "One more white face than black, but a selection along the cycle would force three more."
- F = 1 fails by symmetry, so weigh by something that sees orientation.
