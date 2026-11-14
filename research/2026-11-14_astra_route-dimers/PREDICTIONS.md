# Predictions before testing

All claims below start as CONJECTURE, T5, unreviewed.

1. The real polynomial F(q)=sum_pairs prod_t delta(r(t),s(t)) q^omega(s) equals i^n Z(log q). It equals [product y_t] det(sum y_t M_t), where M_t[u,v]=delta(u,v) q^a(t,v) for distinct corners in X and is zero otherwise. Test exact inclusion-exclusion of determinants against pair enumeration.
2. Removing coefficient extraction fails already for the octahedron or hexagonal prism. Record the smallest tested failure.
3. Adding diagonal entries lambda q^a(t,u) allows common matching edges. At q=1 its squarefree coefficient equals lambda^n times the number of states, even on an obstructed glued octahedron with no tree matching.
4. The first nonzero coefficient at q=1 is a signed sum of products of positive cycle circulations. It equals sum over tree states of their sign times binomial(omega,m), but is not the unweighted signed tree count, which is zero.
5. A reduced white-face Laplacian with edge weights p_t z_v has coefficient [product p_t product z_v] equal to the number of tree matchings. The unrestricted determinant overcounts already on the octahedron.
6. The three trinity directed matrix-tree cofactors equal abs(det K), whereas the tree-matching count can be strictly smaller.
7. Weights depending only on the selected vertex or only on the black face give constant omega and identically zero Z.

Compute scope: named duals and seeded random octahedral face gluings and even bipyramids, 8 to 14 vertices. Not an exhaustive census. Reuse reference graph construction read-only, disable bytecode writes outside this folder. Proofs remain T2 unreviewed; computations T4.
