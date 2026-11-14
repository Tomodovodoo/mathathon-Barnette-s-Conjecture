# Algebraic statements and proofs

All PROVED-HERE statements below are T2, unreviewed. I reread each proof adversarially, as recorded at the end. This is not independent review. O denotes the supplied OpenAI paper, C the supplied constructive paper. LIT is source provenance, not a claim that those preprints are peer reviewed.

## 1. The sign barrier and what Nullstellensatz can say

LIT. O Lemma 4.1 and C Lemmas 4.1, 4.2 give the disk identity and sign reversal. C Proposition 2.1 gives the mate count. We use these inputs explicitly. Write

\[
 F(w)=\sum_{r\perp s}\epsilon(r,s)\prod_{t\in A}w_{t,s(t)},\qquad
 \epsilon(r,s)=\prod_t\delta(r(t),s(t)).
\]

PROVED-HERE. In independent incidence variables, every coefficient of F is zero or plus/minus one. Its nonzero monomials correspond exactly to tree matchings. If there are trees, F has equally many positive and negative coefficients. Multiplication of variables by positive real constants cannot make all nonzero coefficients have one sign.

Proof. Fix s. Its mates orient Q_s toward the roots in tree components and around rootless unicyclic components. If there is a unicyclic component, choose one using s alone and reverse it. The disk identity changes epsilon by a minus sign, while preserving the monomial. These terms cancel. If all components are rooted trees, the mate is unique and its coefficient is epsilon, hence plus/minus one. States without mates contribute zero. Distinct states give distinct incidence monomials.

To evaluate at w=1, group pairs by their undirected union D. Reversing any one D-cycle pairs the orientations with opposite signs. Every D has a cycle, so F(1)=0. Therefore its surviving plus and minus coefficients occur equally often. Positive variable rescaling multiplies each coefficient by a positive number and preserves its sign. This proves the claim. This repeats the forest-support identity in the dimer report to make the subsequent deductions checkable. It is not claimed as a new identity.

PROVED-HERE. Setting w_tv=a_t b_v, with commuting variables a_t and b_v, annihilates F. Thus the direct face-only or vertex-only substitution gives the zero polynomial, not an Alon-Tarsi certificate.

Proof. Every state monomial becomes the same product, namely product a_t times product b_v. Its coefficient is F(1)=0 by the preceding proof.

PROVED-HERE. Over any field, F is nonzero exactly when a tree matching exists. Given a known nonzero monomial w^S, its coefficient remains plus/minus one, even in characteristic two. The coefficient form of Combinatorial Nullstellensatz applied to this degree-n multilinear polynomial gives a nonzero evaluation on a grid with two values on the variables in S and one value on all others. This use of Nullstellensatz does not independently prove existence.

Proof. The support identity establishes the first assertion in every characteristic because each surviving coefficient is a unit. For the second, the coefficient formula can be proved here without citing the general theorem. Set variables outside S to zero. Every degree-n monomial then vanishes except w^S, since there are n surviving variables and F is multilinear. The evaluation with all variables of S equal to one is its nonzero coefficient. The two-value grid includes this point. Selecting S already selected a tree matching, so this argument supplies no new existence theorem.

PROVED-HERE. Incidence variables can be compressed to one variable x_v per nonroot without identifying different state monomials, but exponential exponents suffice rather than a low-degree Alon-Tarsi construction. Order faces t_0,...,t_{n-1} and substitute w_{t_i,v}=x_v^{2^i}. Distinct states yield distinct monomials and coefficients remain plus/minus one.

Proof. For each v the exponent records in binary the face choosing v. A state chooses v exactly once, so it is in fact one power of two. Equality of all exponents recovers the full state. The earlier support identity now proves the conclusion. It does not establish nonvanishing before existence is known.

## 2. Exact parity statements and their limits

PROVED-HERE. Let N_j be the number of states s admitting 2^j mates, and let P be the ordered-pair count and T the tree-matching count. States with no mates are omitted from N_j. Then

\[
 T=N_0,\quad P=\sum_{j\ge0}2^jN_j,\quad
 T\equiv P-2N_1\pmod4.
\]

T is even, and the number of forest pairs is exactly T. If every D has at least m cycles, then 2^m divides P. These conclusions alone do not force T positive.

Proof. The mate characterization gives all identities except the two parity conclusions. A forest state has a unique mate, proving forest pairs equal T. Section 1 balances its two signs, proving T even. An undirected D with c cycles gives 2^c ordered pairs by independent orientations. Partitioning pairs by D proves the divisibility assertion. Expanding the displayed sum modulo four proves the congruence. All formulas are compatible with T=0, so they cannot by themselves force positivity.

LIT. A.G. Thomason, "Hamiltonian cycles and uniquely edge colourable graphs", Annals of Discrete Mathematics 3, 1978, pp. 259-268, Corollary 1.5 on p. 262, proves that in a cubic graph the total Hamiltonian-cycle count H, the number h(e,f) through any two incident edges, and the number g(v) of cycles of length |V|-1 avoiding v are congruent modulo two. The scanned p. 262 was downloaded and visually read. Source: https://www.dpmms.cam.ac.uk/~agt2/HC.pdf .

PROVED-HERE, using that published corollary. Every cubic bipartite graph has an even number of Hamiltonian cycles avoiding each edge. No planarity or connectivity assumption beyond those needed to define the counts is required.

Proof. A cubic bipartite graph has equally many vertices in its two parts, by counting edges, hence even order. Its cycles have even length, so g(v)=0. Thomason's congruence makes H and every h(e,f) even. At an endpoint of a specified edge e, a Hamiltonian cycle avoiding e uses exactly the other two incident edges f,g. Its count is h(f,g), hence even. This is a deduction from the cited corollary, not an independent proof of that corollary. The same result follows from Kotzig's total parity and Smith's edge-through parity.

PROVED-HERE. A connected cubic bipartite graph has exactly two nowhere-zero Z3 flows.

Proof. Orient every edge from one bipartition class to the other. A nonzero value is plus or minus one in Z3. At each vertex the sum of its three incident values is zero, since they all enter or all leave. Three signs sum to zero in Z3 exactly when all three signs agree. Connectivity propagates agreement to all edges. Assigning every edge plus one or every edge minus one gives the two flows. Reorienting edges gives a bijection for any reference orientation.

## 3. A positive Cauchy-Binet formula on the opposite-edge graph

PROVED-HERE. Identify the three roots of T to a single vertex rho, retaining loops and parallel labeled edges. For every allowed incidence i=(t,v) of B, let e_i be the edge opposite v in t after this identification. Let b_i be an oriented incidence column of e_i with the rho row deleted. A loop gives the zero column. Set

\[
 L(p,z)=\sum_{(t,v)\in E(B)}p_t z_v b_{tv}b_{tv}^{\mathsf T}.
\]

Then

\[
 T=[\prod_t p_t\prod_{v\in X}z_v]\det L(p,z),
\qquad
 \det L=\sum_{|S|=n}\det(B_S)^2\prod_{(t,v)\in S}p_tz_v.
\]

All summands in the latter expression have nonnegative integer coefficients. This formula proves a positive representation, but does not establish that the specified coefficient is present.

Proof. The contracted graph has n+1 vertices. Cauchy-Binet applied to B diag(p_t z_v) B^T gives the second equation. For n chosen columns, det B_S is zero unless the chosen edges form a spanning tree. Indeed a cycle makes the columns dependent; a disconnected selected graph has a nonconstant component indicator in the left kernel of its reduced incidence matrix. If it is a tree, deleting a leaf and expanding its row inductively gives determinant plus/minus one. This argument includes loops and parallel edges.

Extracting the displayed monomial forces one incidence at every t and every v, hence a state s. The selected opposite edges form a tree after root identification exactly when Q_s is a forest with one root per component. For the forward direction, an original cycle stays a cycle after contraction, and a path joining different roots would become a cycle. Thus Q_s has no cycle or root-to-root path. Its n edges on n+3 vertices leave three components, so all components contain exactly one root. Conversely contracting one root in each of these three tree components joins them at rho without creating a cycle. The unique-mate orientation then makes s a tree matching. Thus precisely T states survive with squared determinant one.

The logical obstruction is explicit. Existence of a nonzero minor satisfying both incidence partitions is exactly the three-matroid existence problem. Positivity of all other minors does not prove that this particular double coefficient is positive. This is a variant of, rather than an improvement over, the dimer report's white-dual Laplacian formula.

PROVED-HERE. The unsigned multivariate tree-state polynomial need not be real stable. It already fails for the cube.

Proof. The cube's reduced incidence graph is a six-cycle and has exactly two states, both tree states, as seen directly from C Example 2.2. In six independent incidence variables its unsigned polynomial is abc+def. Choose a=b=c=exp(i pi/6) and d=e=f=i. All variables have strictly positive imaginary parts. The two products are i and -i, so the value is zero. This violates the defining zero-free property of real stability. Thus the matching-and-forest projection does not preserve the usual spanning-tree stability property in general.

## 4. Why the local matrices cannot be positive

PROVED-HERE. For positive incidence weights, a nonzero local matrix M_t with entries delta(u,v)w_tv off the diagonal is similar, after multiplication by i, to an indefinite Hermitian matrix. Positive definiteness cannot follow by a similarity or Hermitian congruence applied to that local matrix. No simultaneous diagonal similarity can turn its nonzero opposite off-diagonal entries both nonnegative, or both nonpositive.

Proof. On its permitted corners M_t=S_t D_t with S_t real skew-symmetric and D_t positive diagonal. Thus D_t^(1/2) M_t D_t^(-1/2)=D_t^(1/2)S_tD_t^(1/2). Multiplication by i gives a nonzero Hermitian matrix of trace zero. Its rank is two for two or three permitted corners, so it has one positive and one negative eigenvalue. Similarity preserves eigenvalues and invertible Hermitian congruence preserves inertia. Finally M_uv M_vu=-w_tu w_tv<0, and this product is invariant under diagonal similarity. Two real nonnegative entries or two nonpositive entries would have nonnegative product. These claims concern the proposed local normalization, not every possible larger determinant representation.

## 5. A coefficient-free quartic Berezin representation

PROVED-HERE. Take Grassmann generators bar(psi)_t, psi_v, bar(chi)_t, chi_v. Normalize the top-degree functional so that

\[
 \int_\psi \exp(\sum_{t,v}\bar\psi_t K_{tv}\psi_v)=\det K,
\]

and use the product normalization for the two species. With

\[
 V_t=\sum_{u\ne v\in t\cap X}\delta(u,v)w_{tv}
       (\bar\psi_t\psi_u)(\bar\chi_t\chi_v),
\]

one has the exact identity

\[
 F(w)=\int_\psi\int_\chi \exp(\sum_t V_t).
\]

Proof. V_t squared is zero because every term contains bar(psi)_t and bar(chi)_t. The even V_t commute, so the exponential is product_t(1+V_t). To saturate every barred generator the integral must select V_t once for each t. To saturate both sets of unbarred generators, the selected u values and v values must each be a bijection to X. The restriction u!=v imposes disjointness. The integral sign for this term is sgn(r)sgn(s). The disk lemma makes all states have the same permutation sign, as C Lemma 6.1 proves, so their product is one. The remaining factor is exactly epsilon(r,s) times the s monomial. This gives F. The forest condition is enforced by the fixed-s sign cancellation in section 1, not by a separate local quartic constraint.

PROVED-HERE. This quartic interaction admits an exact real Gaussian auxiliary-field decoupling. It does not require planarity, apart from the identification of the resulting integral with F via common matching signs. The decoupled integrand has no assured sign.

Proof. At each t write C_t[u,v]=delta(u,v)w_tv for u!=v and zero on the diagonal. Choose a real c_t larger than the operator norm of C_t. The real symmetric covariance matrix

\[
 \Sigma_t=\begin{pmatrix}c_t I&C_t\\ C_t^{\mathsf T}&c_t I\end{pmatrix}
\]

is positive definite. For real vectors x,y its quadratic form is at least (c_t-||C_t||)(||x||^2+||y||^2), by Cauchy-Schwarz. Let centered Gaussian vectors xi_t,eta_t have this covariance, independently across t. Put A_u=bar(psi)_t psi_u and B_v=bar(chi)_t chi_v. These are even, commute, and satisfy A_u A_v=B_u B_v=0. The finite Grassmann expansion and Gaussian moment formula therefore give

\[
 \mathbb E\exp(\sum_u A_u\xi_{tu}+\sum_v B_v\eta_{tv})
       =\exp(\sum_{u,v} A_u C_t[u,v] B_v)=1+V_t.
\]

The same-species covariance terms vanish because AA=BB=0. Independence across faces, followed by the two Gaussian determinant integrals, yields

\[
 F(w)=\mathbb E[\det K(\xi)\det K(\eta)],
\]

where each matrix has the allowed incidences as entries and zeros elsewhere. All interchanges are finite polynomial operations with Gaussian moments. Realizing this as an expected square by setting eta=xi is impossible with this local covariance when both transitions u->v and v->u are allowed: C_t is not symmetric and has opposite-sign cross entries. In particular F(1)=0 even when trees exist, so strict positivity for all positive weights would itself be false. Planarity has not removed the sign issue.

## 6. The positive norm does not finish existence

PROVED-HERE. For independent incidence variables and the F above,

\[
 \operatorname{CT} F(w)F(w^{-1})=T.
\]

Proof. Write F=sum_s c_s w^s. Distinct state exponent vectors are distinct. A constant term in F(w)F(w^-1) must pair equal vectors, so its value is sum_s c_s^2. Section 1 gives c_s^2=1 exactly for tree states. Thus it equals T. The norm vanishes exactly when F is identically zero. Proving that it is strictly positive is therefore equivalent to proving existence. This restates the dimer report's norm identity and makes its logical limit explicit.

## Adversarial reread

PROVED-HERE proofs checked internally for the following points. The forest support needs independent incidence variables. The face/vertex annihilation uses bijectivity on both parts. Binary compression does not give low degree. Pair swapping alone does not pair tree states with tree states; the evenness proof uses signed cancellation instead. The parity deduction uses a published corollary rather than assuming Smith implies total parity. Root contraction retains loops and labels. Cauchy-Binet is a polynomial identity without square roots of variables. The stability witness keeps every variable strictly in the upper half-plane. The Gaussian cross covariance is nonsymmetric but the full covariance is symmetric positive definite. Berezin species reordering moves even bilinears and introduces no extra sign. None of these arguments proves a new independent nonvanishing theorem.
