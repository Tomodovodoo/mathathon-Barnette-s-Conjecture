# Proofs

All new proofs below are PROVED-HERE, T2, unreviewed. No unsigned existence proof is claimed. The disk identity, fixed-state cancellation, and height increment formula are inputs from the supplied paper and the named referee reports. Those inputs are not new results here.

## 1. What the UST probability counts

PROVED-HERE. Let tau_H(w) be the weighted spanning-tree sum on H, with every edge weight positive. Let d* be the degree vector in the brief, including full degrees at roots. Then

    Pr_w[deg(T)=d*] = sum_tree_states_s product_(e not in s) w_e / tau_H(w).

Proof. H has 2n+4 vertices and 3n+3 edges. A spanning tree deletes n edges. Its prescribed centre degrees delete exactly one spoke at each bounded centre and none at the outer centre. The vertex degrees delete exactly one spoke at each nonroot and none at roots. The deleted edges therefore form a state. Conversely the complement of a tree state has exactly these degrees. The two correspondences are inverse and preserve weights. Divide the weighted count by the partition sum.

PROVED-HERE. Under the uniform UST, this probability is M/tau(H). Sampling a uniform state instead has success M/S. These are different rejection samplers.

Proof. Set every weight to one in the displayed formula. The state sampler is uniform on a set of size S with M successful elements.

## 2. The full-H target cannot be a finite positive-weight mean

PROVED-HERE. For every instance in the brief, and every finite strictly positive assignment of spoke weights, E deg_T(t0)<3. In particular E deg(T) cannot equal d*.

Proof. Every spoke lies on the boundary of a face of H corresponding to a white triangle. Its boundary is a six-cycle, alternating the three distinct original corners with the three distinct incident black centres. Distinctness uses simplicity of the triangulation and the fact that two distinct black triangles cannot share an edge. Thus no spoke is a bridge. For any spoke e at t0, H-e is connected and has a spanning tree. Every spanning tree has positive probability under finite positive weights, so Pr[e in T]<1. Add this inequality over the three spokes at t0.

PROVED-HERE. The same argument gives E deg_T(v)<deg_H(v) at every root v. The target is on a proper face of the degree projection, rather than in its relative interior. Root-spoke conditioning or diverging weights is compulsory before mean fitting can be relevant.

Proof. Each root spoke has inclusion probability less than one. The maximum-degree inequality is valid for all trees and strict for some. Its equality hyperplane is consequently a proper supporting face, whenever the target is feasible.

## 3. Exactly what mean fitting proves

PROVED-HERE. For a finite nonempty set of feature vectors a_i, with positive base masses c_i, the exponential family p_i(theta) proportional to c_i exp(theta dot a_i) has mean range exactly relint conv{a_i}. Its closure has mean range the whole convex hull.

Proof. Every finite parameter gives strictly positive mass to every i, so its mean is in the relative interior. For the converse work on the linear span L of feature differences and let b be in the relative interior. Minimise

    f(theta)=log sum_i c_i exp(theta dot (a_i-b)), theta in L.

For every unit u in L, max_i u dot (a_i-b)>0. Otherwise b lies on a proper supporting hyperplane. Compactness of the unit sphere gives a common positive lower bound eta on this maximum. Therefore f(theta)>=eta ||theta||+min_i log c_i. A minimum exists. Its gradient is the mean minus b and lies in L, so it vanishes. Boundary means are limits of interior means by approaching a boundary point along a segment from an interior point and using continuity of expectation on the finite probability simplex.

PROVED-HERE. The covariance matrix is the Hessian of log sum_i c_i exp(theta dot a_i). The maximum-entropy distribution with a prescribed interior mean is this exponential family, with entropy relative to the base masses.

Proof. Differentiate twice to get E[aa^T]-E[a]E[a]^T. If p has the specified mean and q is the exponential-family distribution with that mean, then KL(p||q)=sum p log(p/c)+log Z-theta dot b. Nonnegativity of KL, proved by log x<=x-1, shows that q maximises -sum p log(p/c).

PROVED-HERE. Applying this to tree degrees says only that d* is a convex combination of tree degree vectors. It does not select a tree at d*. Preserving all degree constraints in a rounding scheme would be an additional integrality theorem. A fractional vertex of a relaxation alone does not prove that the specific target is a hole in the degree support.

Proof. The first assertion is the definition of convex hull membership. A convex combination can mix feature vectors that differ from its mean. The last assertion distinguishes a fractional point of a feasible slice from absence of every integral point of that slice.

## 4. Why one-sided Lorentzian theory does not transfer

LIT. Branden and Huh, Lorentzian polynomials, Annals of Mathematics 192, 2020, 821-891, establish nonnegative linear substitution closure and M-convex support. Their paper was opened at https://arxiv.org/html/1902.03719v6 . Kalman, A version of Tutte's polynomial for hypergraphs, Advances in Mathematics 244, 2013, 823-873, proves the hypertree polymatroid theorem. Its abstract was opened at https://arxiv.org/abs/1103.1057 . Only the abstract of Kalman was read here; this is not a fresh audit of its proof.

PROVED-HERE, given the standard Lorentzian theorem. On one bipartition class C of H, substitute z_e=x_v for the endpoint v in C in the spanning-tree polynomial. This is a nonnegative linear substitution and gives exactly the one-sided degree generating polynomial. Its support is M-convex and contains every lattice point of its polymatroid base polytope. Degrees minus one give the usual hypertree convention. The black target includes the outer degree 3, not just the bounded degrees 2.

Proof. Every edge has exactly one endpoint in C. Thus each tree monomial becomes product_(v in C) x_v^deg_T(v). Apply the stated substitution and support theorems. Translating by the all-one vector changes no exchange axiom.

PROVED-HERE. The two-sided polynomial substitutes z_tv=x_t y_v, which is bilinear, and need not be Lorentzian. The six-cycle example below proves this. COMPUTED, the cube H also has degree support that is not M-convex.

Proof of the counterexample. Use the lab cube with centres 0,2,4,6. In node order

    t0,v0,v1,v2,t2,v3,v4,t4,v5,t6

two spanning trees have degree vectors

    a = 1,1,1,2,2,1,2,3,2,3
    b = 1,1,1,2,3,2,1,2,2,3.

They are obtained by deleting edge indices 0,1,6 and 0,1,9 from list(b.H.edges()), respectively. The script saves that ordering through the deterministic lab constructor; the numerical vectors can also be checked directly. At coordinate t4, a exceeds b. Deficit coordinates are t2 and v3. Transfer to v3 changes the fixed total degree on each bipartition class and is impossible. Transfer to t2 leaves all original-vertex degrees unchanged. In a these degrees force v0 and v1 to be leaves, v2,v4,v5 to have degree two, and v3 to be a leaf. Together with the proposed centre degrees, no tree exists. To make this last finite check transparent, the omitted-edge characterization is exhaustive: deleting three of the 12 cube spokes gives 220 subsets, 128 of which are trees, and none has a-e_t4+e_t2. This is a finite exhaustive proof by explicit algorithm in code/campaign.py, not independent T3 validation. For a purely abstract proof that bilinear substitution can fail, take the six-cycle bipartite graph. Its tree degrees are all twos except for the endpoints of the one deleted edge. Fixing one endpoint while exchanging the other to its non-neighbour violates the M-exchange axiom. This six-cycle proof does not depend on computation.

The cube witness itself is COMPUTED, T4. The abstract six-cycle refutation is PROVED-HERE. Do not promote the cube's last enumeration sentence to a hand-checked proof.

## 5. The signed measure in probability language

PROVED-HERE, conditional on the refereed cancellation identities. Let P be the number of ordered pairs and M the number of tree states. Draw a uniform ordered pair and let epsilon be its real sign. The signed pushforward to s is

    lambda(s)=epsilon(r_s,s)/P for tree states, and 0 otherwise.

The positive and negative pair measures both have mass 1/2. The positive and negative parts of lambda each have mass M/(2P). The total variation norm sum_s |lambda(s)| is M/P.

Proof. The Q-involution cancels all non-tree fibres. A tree state has exactly one partner. On the full pair set the D-involution, reverse a chosen cycle, has no fixed points and flips the sign, so sum epsilon=0 and the two pair signs are equiprobable. Therefore sum lambda=0. Each surviving atom has magnitude 1/P, which proves all three mass formulas.

PROVED-HERE. For a state statistic h and positive tilt exp(beta h),

    E_tilt[epsilon] = F(exp(beta a)) / sum_pairs exp(beta h(s))

when h(s)=sum_t a_t,s(t). The denominator is positive. The statement that this expectation is nonzero is the original signed nonvanishing problem. A positive denominator supplies no new existence argument.

Proof. Expand the expectation by its definition. The numerator is exactly the real signed partition function.

PROVED-HERE. For the heights of the referee's Theorem B, the two Jordan parts of lambda have identical moments of every total degree less than m=c_min. They differ on an explicit degree-m product. Additive shifts of the heights preserve these statements.

Proof. Apply Theorem B to each monomial and use linearity. Expanding a shifted monomial introduces only lower-degree monomials, whose signed sums vanish. The degree-m product selected by the minimum-cover proof has nonzero signed sum. Thus the signed measure is a finite moment-annihilating measure on state heights, not a probability distribution with negative event probabilities.

## 6. A height-marked version of the involution walk

PROVED-HERE, using the height increment formula and m minimal. Choose m white faces w_i as in the refereed height proof. Shift each height by a state-independent integer so that H_i(s)>=0 on every state. Expand product_i H_i(s) as ordered integer marks, one token in {1,...,H_i(s)} for each i. This defines two finite positive counting measures by epsilon. The Q-involution preserves s and all marks and cancels every nonforest pair.

On a fixed undirected D, write each H_i=b_i+sum_C x_C a_iC, where a_iC is the indicator that w_i lies inside C and x_C is 1 for CCW. The all-clockwise orientation is a state, so b_i>=0. Give slot i a canonical ordered token pool consisting of b_i base tokens and one labelled token for each active cycle C with a_iC=1. Order cycles by face IDs and identify this pool with integer marks by rank. If a cycle has no chosen labelled token, reverse the first such cycle and preserve the labelled token choices, then convert them back to ranks. This operation is an involution: the uncovered cycle rule depends only on the labels already chosen, which do not change. It flips the sign. If no cycle is uncovered, c<=m. Minimality says c>=m, so c=m, every cycle is covered once, and every cycle is CCW. All such fixed points have the common sign (-1)^((n-m)/2), and the chosen minimum cover provides at least one.

Proof of termination of the resulting walk. Draw the graph whose edges are the two involutions on marked pairs, omitting loops. Each vertex has degree at most two. Start at a fixed point of the D-involution and alternate Q and D. A finite path starting at a degree-one vertex cannot enter a cycle. Its other endpoint cannot be another D-fixed point. Two endpoints of that type are connected by an odd number of sign-reversing edges and would have opposite signs, whereas all D-fixed points have the same sign. Hence the other endpoint is Q-fixed, a marked forest pair. Empty-token objects are absent, so an endpoint exists only when its mark weight is positive.

This is a height-marked Garsia-Milne construction. It needs m, the selected w_i, finite height shifts, and changes of token coordinates. No runtime bound follows. It is not an unsigned proof, and it is not shown simpler than barnette_trees in an implementation. At weight one, a global injection whose unmatched set consists of all forest pairs is impossible if it is meant to certify a strict imbalance: the total signed mass is zero and forest signs are balanced. Marking is the source of the imbalance.

## 7. Zero-cycle tilts miss root defects

PROVED-HERE, using the counting-family certificates as an explicit conditional input. Suppose a family has S states, M tree states, and A acyclic-Q states. Under weights exp(-beta cycle_rank(Q)), for beta>=0, the tree probability is at most M/A.

Proof. Every tree state has cycle rank zero and weight one. Every acyclic-Q state has weight one as well. The partition sum is at least A, while the successful numerator is M.

COMPUTED, code/explore.py. On tube4 L=4, M=2, S=89 and A=68, so even infinite beta cannot beat 1/34. On the hexagonal prism, A=S=3, so this tilt changes nothing. These counts diagnose a missing root-connectivity penalty. They do not themselves prove an all-length formula for A.
