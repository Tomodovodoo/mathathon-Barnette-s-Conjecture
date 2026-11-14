# Proofs

All PROVED-HERE statements are T2, unreviewed. The disk identity is reproved below. Claims attributed to the supplied preprints are LIT as source provenance, not a claim that these preprints have been peer reviewed. No new proof of Barnette's conjecture is claimed.

## 1. The disk identity and common determinant sign

PROVED-HERE. Fix a state r. Choose one directed edge out of r(t) in every bounded black triangle t. A directed simple cycle has odd length and signed delta sum -3 counterclockwise, +3 clockwise.

Proof. Roots have no outgoing edges. All roots lie outside the bounded disk of the cycle. Let h be its length, I its number of interior vertices, b and w its interior black and white face counts, and l the number of boundary edges whose black triangle is inside. Euler counting and triangle-side counting give

    b+w = 2I+h-2,       3(b-w) = 2l-h.

The matching gives b=I+l. Each interior vertex is matched to a black triangle inside. Each boundary vertex is matched to its outgoing edge's triangle, which is inside exactly at the l counted positions. Conversely every black triangle inside is matched to one of these vertices. Substitution gives 2l-h=-3. Reversing traversal reverses the signed sum. In particular h is odd. This is the supplied OpenAI Lemma 4.1, with the parity consequence stated in barnette_trees Lemma 4.1.

PROVED-HERE. All states have the same permutation sign. Hence for arbitrary commuting incidence weights w_tv,

    det K(w) = sigma sum_s product_t w_t,s(t),       sigma in {+1,-1}.

Proof. For two states r,s, direct r(t) to s(t) wherever they differ, and complete the outgoing choices arbitrarily elsewhere. Each nontrivial cycle of the relative permutation is a simple directed cycle in these choices. The preceding lemma makes its length odd. Every such cycle is an even permutation; fixed points are also even. Thus the relative permutation is even. The determinant expansion proves the formula. No no-separating-triangle hypothesis was used. The zero-one incidence matrix is therefore already a determinant counting matrix. This does not assert a facial Kasteleyn sign rule for every face of the reduced embedded graph.

## 2. A real mixed determinant for the central sum

For t in A, define an X by X matrix

    M_t(w)[u,v] = delta(u,v) w_tv if u,v are distinct corners of t,
                 0 otherwise.

Let

    F(w) = [product_t y_t] det(sum_t y_t M_t(w)).

PROVED-HERE. For arbitrary incidence weights,

    F(w) = sum_disjoint(r,s) epsilon(r,s) product_t w_t,s(t),
    epsilon(r,s) = product_t delta(r(t),s(t)).

For w_tv=exp(x a_tv), this equals i^n Z(x). It is n! times the mixed discriminant under the convention that the mixed discriminant is the squarefree coefficient divided by n!.

Proof. A term in the determinant chooses one outgoing column for each row u and a face label for every selected matrix entry. Extracting product y_t forces the labels to be used exactly once. The rows assigned to each face give a state r; the columns give a state s. Zero diagonal enforces disjointness. Conversely each ordered disjoint pair gives exactly one such term. Its permutation on X sends r(t) to s(t) and has sign +1 by section 1. This proves the first formula.

Write d=sum delta=3J. There are n signs, so J has parity n. If k of them are negative, their product is (-1)^k with k=(n-3J)/2. This has the same parity exponent as (n+J)/2. Thus epsilon=i^(n+J), proving F=i^n Z. Equivalently Z=(-i)^n F. This removes all sixth roots from the local matrix.

PROVED-HERE. The coefficient has the exact polarization formula

    F(w) = sum_{S subset A} (-1)^(n-|S|) det(sum_{t in S} M_t(w)).

Proof. Inclusion-exclusion kills any monomial omitting a y variable. The determinant is homogeneous of degree n, so every surviving monomial uses all n variables exactly once.

PROVED-HERE. There is also a formal Pfaffian version. For N=sum y_t M_t,

    F(w)=(-1)^(n(n-1)/2) [product y_t] Pf([[0,N],[-N^T,0]]).

This follows by expanding the block Pfaffian, or the usual determinant-Pfaffian identity. It does not remove coefficient extraction or improve complexity.

PROVED-HERE. At w=1 each M_t is skew symmetric and has rank at most two. Indeed its support has at most three vertices, and a 3 by 3 skew matrix has rank at most two. With general weights it is that skew matrix times a diagonal matrix, so the same rank bound holds. These matrices are not positive semidefinite. The usual positivity theorems for mixed discriminants of positive semidefinite matrices do not directly apply.

## 3. What doubling does

Replace the diagonal zero of M_t by lambda w_tu, retaining the off-diagonal signs. Write F_lambda for the same squarefree coefficient.

PROVED-HERE.

    F_lambda(w)=sum_all(r,s) lambda^#{t:r(t)=s(t)}
                 product_{t:r(t)!=s(t)} delta(r(t),s(t)) product_t w_t,s(t).

The proof is the identical determinant expansion. In particular F_0=F.

PROVED-HERE. F_lambda(1)=lambda^n times the number of states.

Proof. The union of any two matchings splits into doubled edges and alternating cycles. Every nontrivial relative-permutation cycle has odd length by section 1. Reversing it changes the product of deltas by -1. With w=1 both orientations have the same magnitude; all configurations with a nontrivial cycle cancel. The remaining pairs are r=s, each contributing lambda^n.

This is a precise doubled-edge extension, not a claimed realization by a standard SL2 connection. It proves why unrestricted nonvanishing is insufficient. The 9-vertex witness random_9_1 has four states, no disjoint pairs, no tree matchings, and F_1(1)=4.

## 4. Forest support, moments, and a positive norm

PROVED-HERE. A state s has a disjoint mate exactly when every component of Q_s is a tree with one root or a unicyclic component with no root. With k unicyclic components it has 2^k mates. It is a tree matching exactly when it has one mate.

Proof. A mate directs every opposite edge from r(t) to the third corner, giving outdegree one at nonroots and zero at roots. A connected component with v vertices and a roots has v-a edges, so connectivity forces a at most one. If a=1 it is a tree and must be directed toward the root; if a=0 it is unicyclic, with its branches directed toward the cycle. Its cycle has two orientations. Conversely these orientations give a bijection from faces to nonroot tails, hence a mate. Finally H-s is obtained by subdividing Q_s and joining its roots to the outer center. It is a tree exactly in the all-rooted-tree case.

PROVED-HERE. For arbitrary weights,

    F(w)=sum_tree states s epsilon(r_s,s) product_t w_t,s(t),

where r_s is the unique mate.

Proof. For a non-tree s with a mate, choose one cycle in Q_s. Reversing that cycle changes r only. The local identity delta(u,s)-delta(r,s)=2 delta(r,u), followed by the disk identity, changes J by +2 or -2. Thus epsilon changes sign. The monomial in s stays fixed and cancels. States without mates never entered the sum. The previous proposition identifies the survivors.

Consequently every coefficient of F in the independent incidence variables is 0,+1, or -1. Its support is exactly the set of tree matchings. This is stronger than a univariate signed enumeration, where distinct tree monomials can coincide.

PROVED-HERE. The number of tree matchings is

    CT_w F(w) F(w^-1)
      = integral_[0,2pi]^E |F(exp(i theta))|^2 dtheta/(2pi)^|E|.

Proof. Different states have different squarefree incidence monomials. Constant-term extraction pairs only equal monomials. Their squared coefficients are one. Fourier orthogonality proves the integral formula. This is a positive representation, but proving the norm is positive still requires proving F is not the zero polynomial.

PROVED-HERE. Suppose the spoke weights have positive counterclockwise circulation and at least one pair exists. Let m be the minimum number of D cycles, and A_C=Lplus(C)-Lminus(C)>0. Then

    sum_tree s epsilon_s binomial(omega(s),m)
      = (-1)^((n-m)/2) sum_{D:c(D)=m} product_{C in D} A_C.

All lower binomial moments vanish. Equivalently, for exponential moments replace binomial(omega,m) by omega^m/m!. Both sides remain equal in the first nonzero degree.

Proof. Independent orientation choices give each D group the polynomial

    (-1)^((n-c(D))/2) product_C (q^Lplus(C)-q^Lminus(C)).

Each factor has a simple zero at q=1 with coefficient A_C. Only m-cycle groups contribute in degree m; their signs agree. The forest-support identity gives the other expansion. Substitution q=exp(x) preserves the first nonzero coefficient. Integer unit-face circulations make A_C the number of enclosed bounded spoke faces, so the positive sum counts an undirected minimum-cycle configuration with one enclosed face marked per cycle. The unweighted signed tree count is zero, not this positive count.

## 5. The constrained matrix-tree formula

Let W=H* with white triangles as vertices and spokes as dual edges. Retain only edges dual to B and give the edge dual to (t,v) weight p_t z_v w_tv. Let L_W be its weighted Laplacian, with any one row and column deleted.

PROVED-HERE.

    sum_tree states s product_t w_t,s(t)
      = [product_t p_t product_{v in X} z_v] det L_W.

Proof. The matrix-tree theorem expands the determinant into weighted spanning trees of W, each with n edges. The specified coefficient forces each face label and each nonroot label to occur exactly once. Thus selected spokes form a state s. Tree/cotree duality says their duals form a tree exactly when H-s is a tree. The correspondence preserves the product of w weights. Conversely every tree matching contributes once. Parallel dual edges remain separate edges throughout.

The equivalent prescribed-degree formula on H takes the coefficient of product z_u^d_u in a reduced Laplacian with spoke weight z_t z_v, where d_t=2 on bounded black centers, d_t0=3, d_v=deg_H(v)-1 at nonroots and d_v=deg_H(v) at roots. Taking complements proves the same bijection. Neither formula makes the desired coefficient transparently positive.

## 6. Scalar weights that cannot work

PROVED-HERE. If a_tv=alpha_t+beta_v then omega(s)=sum alpha_t+sum beta_v is independent of s. Every D group cancels, so Z is identically zero whenever n>0. Vertex-only or black-face-only statistics therefore cannot replace incidence circulation.

PROVED-HERE. The three-corner local off-diagonal phase delta(u,v) cannot be written as a_u b_v with all six entries nonzero. Multiplying the three cyclic entries would equal multiplying the three reverse cyclic entries under such a factorization. For delta those products have opposite signs. The same obstruction holds for exp(i*pi*delta/6): the ratio of the two products is -1. This rules out the direct factorization into separate scalar r- and s-matching weights at a degree-three black center. It does not rule out a more elaborate graph gadget, a connection reproducing only global cycle weights, or a nonabelian construction.

## 7. Linear incidence weights suffice

PROVED-HERE. Define P(x)=F(w) with w_tv=1+x a_tv, using the same positive-circulation incidence weights as before. Then P has degree at most n, and if disjoint pairs exist its order of vanishing is exactly m=cmin. Its leading coefficient equals that of F(exp(xa)).

Proof. For each undirected D group the product over cycles now has factors

    product_{t in C}(1+x a_t,plushead) - product_{t in C}(1+x a_t,minushead),

with overall sign (-1)^((n-c(D))/2). Each factor vanishes at zero and has derivative A_C>0 there. The minimum-cycle argument from section 4 applies without change. Forest cancellation holds because each weight depends only on s. On the forest side the coefficient of x^m is the signed sum of elementary symmetric polynomials e_m of the selected incidence weights. Thus

    sum_tree s epsilon_s e_m((a_t,s(t))_t)
      = (-1)^((n-m)/2) sum_{D:c(D)=m} product_C A_C != 0.

This is a finite polynomial version of the same proof. It reduces the degree from the possible O(n^2) exponent sum to n. It does not establish a polynomial-time method to compute the mixed determinant coefficient.
