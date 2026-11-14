# Identity register

Proofs are T2 unreviewed. Computations are T4 unreviewed. A COMPUTED entry records evidence, not a general theorem. Every test below uses exact integers.

| Identity or proposed shortcut | Status | Evidence and range |
|---|---|---|
| State count = absolute incidence determinant | PROVED-HERE; LIT barnette_trees Lemma 6.1 | PROOF 1; explore.py, all 18 examples |
| i^n Z = sum product delta times matching weight | PROVED-HERE | PROOF 2; every disjoint pair in all 18 |
| F = squarefree face coefficient of det(sum y_t M_t) | PROVED-HERE, COMPUTED | PROOF 2; exact determinant polarization at q=2 on 10 examples with n<=8, plus truncated octahedron and cyclic-mate example |
| Raw determinant equals F | REFUTED | Hexagonal prism dual, 8 vertices: 0 versus 6 at q=2; octahedron happened to pass |
| det(K1+z K2) counts two matchings | REFUTED | Expansion selects a single matching; PROOF-style expansion in ROUTES |
| Doubled extension F_lambda(1)=lambda^n times states | PROVED-HERE, COMPUTED | PROOF 3; lambda=1 on the same 12 polarization examples |
| Nonzero doubled extension implies tree matching | REFUTED | random_9_1: doubled value 4, zero trees and zero disjoint pairs |
| Leading coefficient = signed sum of products of enclosed face counts | PROVED-HERE, COMPUTED | PROOF 4; all 18; cmin=1 and 2, plus obstructed cases |
| Leading coefficient = unweighted signed tree count | REFUTED | Octahedron: -1 versus 0 |
| Multivariate coefficient at state s is 0 or its unique-mate sign | PROVED-HERE, COMPUTED | PROOF 4; linear.py, all 18 |
| CT F(w)F(w^-1) = number of tree matchings | PROVED-HERE, COMPUTED | PROOF 4; coefficient norm in linear.py, all 18 |
| Tree count = unconstrained white Laplacian determinant | REFUTED | Octahedron 2 versus 128, or 8 after restricting to B duals |
| Tree count = doubly label-squarefree Laplacian coefficient | PROVED-HERE, COMPUTED | PROOF 5; extra.py independent edge-subset enumeration at 6 and 8 vertices |
| All three trinity cofactors = states | LIT; COMPUTED | Hine-Kalman Theorem 4.3, Lemma 4.4; explore.py all 18 |
| Trinity arborescence count = tree-matching count | REFUTED | Hexagonal prism dual 3 versus 2 |
| Vertex-only or black-face-only weights suffice | REFUTED, PROVED-HERE | PROOF 6; omega is constant, so Z=0 |
| Local phase is a product of separate scalar matching weights | REFUTED, PROVED-HERE | PROOF 6; three-corner cyclic product obstruction |
| Linear incidence weights preserve nonvanishing | PROVED-HERE, COMPUTED | PROOF 7; linear.py all 18, including cmin=2 |
| A coefficient-free SL2/Pfaffian realization exists | HUNCH | No construction established; local-signature test proposed in ROUTES |

See data.json for complete graphs, root triangles, K matrices, exact polynomials, counts and determinant values. The word 'smallest' in the route discussion means smallest tested witness unless a separate proof of minimality is supplied.

