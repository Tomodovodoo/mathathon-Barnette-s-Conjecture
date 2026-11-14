# Exact reformulations and their missing theorems

Notation is that of the brief. All statements concern a fixed rooted face-colored simple sphere triangulation. The existence assertion E is that some pair r,s of disjoint states has Q_s a forest. Use C Proposition 2.1 to distinguish a forest with the correct roots from an arbitrary forest. The supplied papers are preprints, not a certification supplied by this review.

## 1. Incidence tree and prescribed degrees

[LIT, C Theorem 1.2 and Proposition 2.1; O Sections 5-6] E is equivalent to a state s with H-s a spanning tree. Its retained degrees are two at bounded black centers A, three at t0, d_H(x)-1 at nonroots, and d_H(v) at roots. This is a degree-constrained spanning-tree problem with special planar incidence structure.

[PROVED-HERE] Deleting s leaves Q_s with each edge subdivided by its black center, and adds the three outer spokes. A mate orients Q_s with one outgoing edge per nonroot and none at roots. If Q_s is a forest, each component contains exactly one root by the outdegree count. Joining the roots to t0 therefore makes a tree. Conversely a retained tree makes Q_s a forest with one root per component. Orienting it towards the roots reads off a unique mate. Finally, the stated degree constraints leave exactly one unused spoke at each vertex of B and none at the deleted outer vertices; the complement is a state. This proves the equivalence without appealing to a general degree-constrained-tree algorithm.

[HUNCH] A special prescribed-degree-tree theorem for this H would finish the proof. A generic spanning-tree existence theorem does not address the prescribed degrees.

## 2. Unique disjoint mate

[LIT, C Proposition 2.1] E is equivalent to the existence of a state with exactly one disjoint partner. More generally the partner count is zero or 2^k, where k is the number of rootless unicyclic Q_s-components, provided every other component is a singly rooted tree. See the full orientation proof in `MACHINERY.md`.

[PROVED-HERE] Let K_B be ordered so all matching terms have common sign sigma. Then det of the matrix obtained by setting the s-entries to zero is sigma times the partner count. Consequently E is equivalent to some s for which the absolute value of this determinant is one. This determinant counts partners because deleting allowed edges only removes terms from the common-sign expansion. The assertion is not that det K_B itself is one.

[HUNCH] An arithmetic theorem forcing a partner count one, given any positive partner count in this special family, would finish. Divisibility by powers of two alone does not force it.

## 3. A determinant coefficient for Z

[PROVED-HERE, conditional on O Lemma 4.1] Here is an explicit determinant representation with coefficient extraction. It allows arbitrary commuting incidence weights b(t,v), with exp(x a(t,v)) as a specialization. Set q=exp(pi i/6). On rows and columns indexed by X define

    M_t(u,v) = q^{delta(u,v)} b(t,v)  if u != v and u,v are corners of t,
               0                    otherwise.

Then the exact formula is

    Z_b = [product over t of z_t] det(sum over t of z_t M_t).

With b(t,v)=exp(x a(t,v)), this is exactly O's Z(x), since q^{sum delta}=i^J.

Proof. Expand the determinant into permutations pi of X, and then expand each chosen matrix entry into its face summands. Extracting the squarefree monomial product z_t forces each face to occur exactly once. If its selected entry is u->v, set r(t)=u, s(t)=v. The row condition makes r a bijection; the permutation's column condition makes s a bijection; the diagonal zero forces disjointness. Conversely every ordered disjoint pair gives precisely this term. Each cycle of pi is a simple directed D-cycle and the disk identity gives delta sum +/-3. Its length is odd since each summand is odd. Every cycle of pi is thus an even permutation, so sgn(pi)=+1. The remaining product is exactly the pair weight. No factorial is missing. This is a mixed-determinant coefficient, n! times the convention that divides this coefficient by n!.

[PROVED-HERE] Homogeneity gives a second exact formula,

    Z_b = sum over S subset A of (-1)^{n-|S|} det(sum over t in S of M_t).

Indeed inclusion-exclusion retains only determinant monomials using every z_t. They have total degree n and hence use each exactly once. This is 2^n determinant evaluations, not a polynomial-time determinant evaluation. It can be useful for verification but does not improve C's 3^{n/2} enumeration bound. For n>=1 the empty summand is det of the zero n by n matrix, hence zero.

[PROVED-HERE] Local matrices have rank at most two. If a face has three nonroot corners, strip the nonzero column weights b and inspect the zero-diagonal three by three matrix. Its determinant is q^3+q^{-3}=i-i=0, while a two by two off-diagonal minor is nonzero. Boundary faces restrict this matrix and do not increase rank. Rank two does not remove coefficient extraction. It permits repeated use of a face twice in an unrestricted determinant expansion, so setting all z_t=1 has not been justified.

[PROVED-HERE] This is not the naive product of two scalar dimer determinants. Scalar factorization of q^{delta(u,v)} as alpha(u) beta(v) on distinct corners would force equality of its two cyclic triple products. Their ratio is q^6=-1. This refutes that factorization in faces with three permitted corners. A larger planar gadget, block determinant, or a connection model remains possible.

[COMPUTED] `check_determinant.py` constructs the even-rim bipyramids with rim lengths 4 and 6. The rooted instances have n=3 and n=5, respectively. It enumerates all states and ordered disjoint pairs, assigns distinct positive integer incidence weights, computes the symbolic coefficient determinant, and compares it with the direct sum in Q[q]/(q^4-q^2+1). Results are `determinant-check.json`. Counts are 2 and 3 states, with 2 ordered disjoint pairs in both cases. Coefficients are -51 q^3 and -20775 q^3. Command:

    python research/2026-11-14_sol_machinery-literature/check_determinant.py

[HUNCH] A nonvanishing theorem for this mixed determinant under positive spoke curvature would repackage O's central argument. To replace that argument, prove nonvanishing from independent matrix hypotheses. The rank-two matrices are complex and not supplied as positive semidefinite matrices, so standard mixed-discriminant positivity cannot be invoked without a transformation preserving the coefficient.

## 4. A positive spanning-tree coefficient

[PROVED-HERE, using weighted matrix-tree] Give every vertex u of H a variable y_u, and every spoke uv weight y_u y_v. Form its weighted Laplacian L_H and delete any one row and column. Write

    Tau_H(y) = det L_H^{root}(y) = sum over spanning trees F of product over u y_u^{deg_F(u)}.

Define the target vector d* by the retained degrees in Section 1. Then

    [y^{d*}] Tau_H(y) = number of tree matchings of B.

Proof. A tree contributes exactly the monomial of its degree sequence, with coefficient one. At the target degrees its complement has degree one at every vertex of B and zero at all other H vertices, hence is exactly a state. Conversely every tree matching gives that degree vector and a distinct tree. Thus this is a positive integer coefficient and E is equivalent to its positivity.

[HUNCH] This is the cleanest unsigned algebraic target. A theorem proving that this degree vector lies in the actual support of the tree-degree polynomial would finish. Membership in a convex hull alone would not suffice without an integer-support theorem. General coefficient positivity of Tau_H does not assert positivity at this particular monomial.

## 5. Two-sided hypertrees

[PROVED-HERE] Let centers be E=A union {t0} and triangulation vertices be V=X union R. Seek one H-tree simultaneously realizing

    f(t)=deg_F(t)-1 = 1 on A, 2 at t0,
    g(v)=deg_F(v)-1 = d_H(v)-2 on X, d_H(v)-1 on R.

This common realization is equivalent to E by Section 1. Both have the correct total degree sums. Their separate hypertree membership is necessary, and is not asserted sufficient here. The equality of transposed interior polynomials counts degree data rather than checking this coupled pair.

[HUNCH] A simultaneous hypertree-realization theorem or a Bernardi representative realizing this g for the specified f would finish. It would be stronger than the one-sided hypertree inequalities of Kálmán's Theorem 3.4.

## 6. Three matroids, with roots contracted

[PROVED-HERE] Use ground set E(B). Its element (t,x) corresponds to the edge opposite x in t. Define P_A and P_X as the two partition matroids on its endpoints. Define M_R as the graphic matroid on those opposite edges after identifying all three roots to a single vertex. Keep loops and parallel edges. Then E is equivalent to a common independent set of size n in P_A, P_X and M_R.

Proof. Size n and the two partition constraints give a state. Graphic independence after root identification is equivalent to Q_s being a forest with at most one root per component: an original cycle remains cyclic, and a path between distinct roots closes after identification; conversely every cycle after contraction lifts to an original cycle or a root-to-root path. The n edges on n+3 original vertices leave three forest components. All roots are distinct among them, so every component contains one root. Section 1 supplies the mate and incidence tree. Conversely a tree matching has all these properties.

[REFUTED] Combining P_A and P_X into “the matching matroid” violates augmentation on K_2,2, as shown in `MACHINERY.md`. A transversal matroid on a vertex class forgets the corners. Edmonds's two-matroid theorem therefore does not directly apply. [HUNCH] A special exchange or integrality theorem for this three-way intersection would finish. General three-matroid intersection results are not being claimed.

[PROVED-HERE, derivation of the Rado criterion from the checked Edmonds theorem] Given subsets A_i of a matroid ground set, replace each candidate e in A_i by a copy (i,e). On these copies take the partition matroid with at most one per i and the parallel extension of the original matroid. A common independent set of size m is an independent system of representatives. Necessity of rank(union_{i in I} A_i)>=|I| is immediate. For sufficiency, let U be any set of copies and let I be the indices with no copy in U. The partition rank of U is m-|I|, while the original-matroid rank of the remaining copies is at least rank(union_{i in I} A_i)>=|I|. Every Edmonds rank cut therefore has value at least m, proving existence. This checks the Rado statement without pretending the inaccessible 1942 proof was read. Applying it to this problem still requires absorbing the second endpoint partition constraint into one genuine matroid.

## 7. Rooted functional orientations

[PROVED-HERE] E is equivalent to choosing one opposite edge per black face with a distinct unchosen corner s(t), covering X once, such that the chosen edges admit an orientation with outdegree one at X, zero at R, and no directed cycles. Such an orientation is a forest oriented toward roots. To prove the reverse statement, an undirected cycle would have distinct tails at its vertices and hence be directed, since outdegree is at most one. Reading tails gives r; reading the opposite corner gives s. Every directed path then terminates at a root. The distinct-corner condition must remain; a generic root-reaching orientation does not include it.

[HUNCH] An orientation theorem with these local triangular constraints would finish. Schnyder or alpha-orientation existence by itself omits the corner bijection.

## 8. Disjoint dimers with signed loop valuation

[LIT, O Section 5.3] Superposing r and s in B gives disjoint alternating loops with no doubled edges. Contract their passages through black centers to obtain D. O's loop expansion is

    Z(x) = sum over D of product over C in D
           {-i exp(xL+(C)) + i exp(xL-(C))}.

[PROVED-HERE] Each factor equals -2i exp(xm_C) sinh(x Delta_C/2). Positive curvature makes Delta_C>0. Hence val_0 Z=min_D c(D), and its leading coefficient has phase (-i)^{min c(D)} and positive magnitude. This conclusion is conditional on the cycle regrouping and disk identity already established in O. Combined with cancellation for cyclic Q_s it proves E. It is a reformulation of O's route, not an independent new proof.

[HUNCH] A direct Pfaffian or SL2-dimer interpretation would be useful if it reproduces both the no-doubled-edge restriction and the turn weights. Standard double dimers include doubled edges. A flat sphere connection has trivial contractible monodromy. Neither issue can be omitted.

## 9. State lattice with a distinguished subset

[LIT, HineKalman2018] States are elements of a finite distributive lattice. [PROVED-HERE] E asks that its subset of states with partner count exactly one be nonempty. Equivalently it asks for some element in this lattice whose opposite-edge forest is singly rooted. This is an exact set-theoretic translation, without a proved lattice characterization of that subset.

[HUNCH] A theorem identifying the target subset as a nonempty interval, ideal, extremal family or optimization set would finish or give a search algorithm. The clock theorem only makes the ambient set connected. No monotonicity of the target subset was established here.

## 10. Homology and induced trees

[LIT, O Section 6, Stein1971] A tree matching recovers a partition V(T)=U union W with both induced subgraphs trees and a prescribed outer edge monochromatic. [PROVED-HERE] For nonempty U,W this says reduced H_0(T[U])=H_1(T[U])=0 and the same for W, over any field. Those vanishing conditions are exactly connectedness and acyclicity for finite graphs. The complementary dual edges form a connected degree-two graph and hence a Hamiltonian cycle. Conversely a Hamiltonian dual Jordan curve partitions triangulation vertices into the two induced trees, by its two sides and Euler counting. This is the classical global reformulation.

[HUNCH] The converse from an arbitrary such partition to a tree matching for a fixed rooted incidence problem is NOT established here. In particular separator obstructions can prevent a tree matching although gluing still gives a global partition. Treat the induced-tree condition as the downstream Hamiltonian formulation, not an unconditional equivalent of E on all rooted triangulations.

## 11. Feedback sets and Yutsis comparison

[PROVED-HERE] A two-induced-tree partition is equivalently a vertex set U for which U and its complement each induce a connected forest. Each is then a feedback vertex set. A single feedback vertex set whose complement is a tree is insufficient unless U itself induces a tree. General induced-forest size results therefore do not finish this statement.

[REFUTED] A Yutsis partition of the original cubic graph is not the same object as an induced-tree partition of the dual triangulation. The ground vertices differ, and equal class sizes in the cubic setting come from cubic degree counting, absent in T. No conversion theorem was verified.

## What these reformulations buy

[PROVED-HERE] Sections 3 and 4 give explicit exact determinant coefficients. Section 6 states the precise matroid ground set and shows why the tempting two-matroid shortcut fails. Sections 2 and 5 identify unique-partner and common-degree targets. [HUNCH] The shortest genuinely different route would prove one of those targets using a theorem whose hypotheses are easier to check than O's cancellation argument. None of the neighboring theorems surveyed already does so without an additional step.
