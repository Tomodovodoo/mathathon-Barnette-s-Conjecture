# Dimer-route report

PROVED-HERE, T2 unreviewed: the central sum is a squarefree face coefficient of a real mixed determinant.
PROVED-HERE, T2 unreviewed: linear incidence weights give the same nonvanishing proof with degree at most n.
PROVED-HERE, T2 unreviewed: a constrained Laplacian coefficient and a positive coefficient norm each count tree matchings.
REFUTED: raw determinants, unconstrained white trees, and doubled-edge nonvanishing do not isolate tree matchings.
COMPUTED, T4: 18 rooted examples through 14 vertices support the formulas; no independent referee has checked this work.

## Objective

Explore the statistical-mechanics and linear-algebra reading of the paired-state sum. I read the three supplied papers, checked key PDF formulas, and used exact computations before writing the proposed new identities as proofs. All writes stayed inside this folder. No agents were delegated.

## What was established

PROVED-HERE. Let M_t[u,v]=delta(u,v) w_tv for distinct nonroot corners of t, zero otherwise. Then

    i^n Z(x) = [product_t y_t] det(sum_t y_t M_t(exp(xa))).

The permutation sign is positive for each relative permutation, and the product of local delta signs is precisely the integer pair sign. PROOF.md supplies the disk count, common-sign argument and determinant expansion. The matrix is real after the global phase is removed. A formal block Pfaffian formula follows, but retains coefficient extraction.

PROVED-HERE. Exponentials can be replaced by w_tv=1+x a_tv. The polynomial then has degree at most n. In its first occurring degree m=cmin, the coefficient is a common sign times the sum over minimum-cycle undirected pairs of products of positive cycle circulations. On the forest side it is a signed elementary symmetric moment. This is the most useful simplification found.

PROVED-HERE. With independent incidence variables, the signed polynomial has coefficient +1 or -1 on each tree state and zero on every other state. Consequently the constant term of F(w)F(w^-1) counts tree matchings. The matrix-tree theorem gives a separate positive formula: extract both sets of label variables from the Laplacian of the restricted white-face graph. The two formulas expose the remaining constraints instead of hiding them.

LIT and COMPUTED. Tutte trinity counts all states. Hine-Kalman Theorem 4.3 and Lemma 4.4 provide the exact bijection, and all three directed cofactors agree with the incidence determinant in the tests. The white-face graph is a different graph. Its spanning trees correspond to tree matchings only after two sets of label constraints are imposed.

## What failed

REFUTED. The ordinary determinant without face coefficient extraction fails on the 8-vertex hexagonal-prism dual. At q=2 it is 0 while F is 6. Extra determinant terms reuse face labels.

REFUTED. Allowing doubled edges makes nonvanishing too easy. In the explicit extension with diagonal parameter lambda, F_lambda(1)=lambda^n times the state count. A rooted 9-vertex gluing has four states but no disjoint pairs and no tree matching. Its doubled value is 4. Kenyon's SL2 connection does not itself suppress doubled edges, since backtracking transport is identity.

REFUTED. The unweighted signed forest count is not the positive leading coefficient. It is zero. The positive coefficient is a marked count or moment. On the octahedron the signed count is 0 and the leading coefficient is -1 under our real-sign convention.

REFUTED. Uniform spanning trees alone do not solve the constrained problem. The octahedron gives 128 full white trees, 8 after restricting edges to B duals, and only 2 tree matchings. Vertex-only or black-face-only weights also fail because their sum over any state is constant.

## Checks and limits

COMPUTED, T4. The suite contains the three named examples, fourteen seeded rooted examples of sizes 8 through 14, and a 12-vertex cyclic-mate example read from the constructive agent and re-enumerated here. All state pairs were enumerated. On the cyclic-mate example there are 9 states, 10 disjoint ordered pairs, and 8 tree matchings; the two non-tree pairs cancel.

COMPUTED, T4. Exact determinant polarization was checked on 12 examples, at q=2, against direct pair enumeration. All 18 examples were checked for the common permutation sign, trinity cofactors, forest cancellation, lowest coefficient, linear weights and coefficient norm. White-tree coefficient extraction was checked by separate edge-subset enumeration at 6 and 8 vertices. No floating-point equality tests were used.

The computation reuses the repository's state and embedding implementation, so it is not independently validated T3 evidence. The sampled graphs are structured gluings and bipyramids, not uniformly random or an exhaustive census. The smallest witnesses are smallest tested, not classified minima. An initial replay error exposed unstable numeric face IDs; root triangles are now stored explicitly and used when reconstructing examples.

All new proofs remain unreviewed T2. I did not find a coefficient-free determinant, a working SL2 gadget, a structural positivity argument for the constrained Laplacian coefficient, or a new positive sampling proof of existence.

## Three best next steps

1. Independently referee the real-sign mixed determinant and the degree-n linear-weight proof. These can shorten the exposition immediately if they check out.
2. Test antisymmetric local gadgets by their complete signatures. A useful Pfaffian construction must exclude doubled edges and repeated face labels without a global coefficient operator.
3. Characterize the tree-matching subset inside one trinity arborescence family. Compare this condition with the two label constraints in the white Laplacian, then test whether its probability has a meaningful lower bound.

## Leads for others

For the exposition agent: the one-line identity in PROOF section 7 equates a signed elementary symmetric moment of tree matchings with a positive marked-cycle count. It uses a degree-n polynomial and avoids exponentials.

For the constructive agent: the local matrices have rank at most two. This is an exact mixed-discriminant problem, but the matrices are not positive semidefinite. The determinant coefficient reproduces the sixth-root experiment in your folder with integer arithmetic and no algebraic number field.

For the machinery agent: trinity arborescences and white-face trees must be distinguished. The former count all states; the latter require two transversal constraints. Direct scalar phase factorization fails on the local three-corner cyclic-product test.

## Files and research map

PROOF.md contains full arguments. IDENTITIES.md lists statuses and test ranges. ROUTES.md records each route, source and obstacle. code/README.md gives replay commands. data.json stores graphs, roots, incidence matrices, exact polynomials and counts. coefficient_check.json and linear_weights.json store additional tests.

The local map has four theorem nodes awaiting review, three recorded dead ends and one open gadget question. The frontier records only sampled cmin values, using 0 for no disjoint pair; it makes no completeness claim. labyrinth/dashboard/index.html is local. Build with `python -X utf8 -B labyrinth/lab.py build` from this folder, and check with the corresponding `check` command. The UTF-8 option avoids the Windows default decoding failure in the supplied template engine.
