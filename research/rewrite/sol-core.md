# The paired-state core

Use the Laurent generating function and a reference-state winding weight. Together they remove the path-by-path height calculation and the finite-difference lemma. The generating function needs only integer weights, the binomial factorization, and the first nonzero coefficient at 1. Negative weights cause no difficulty: multiply the entire sum by one sufficiently large power of z if an ordinary polynomial is preferred.

The sign convention matters. With c cycles, c⁺ counterclockwise, the paper's local sign is

\[
\varepsilon=(-1)^{(n+c)/2+c^+}.
\]

Consequently the all-clockwise term has sign (-1)^((n+c)/2), and a cover contributes

\[
(-1)^{(n+c)/2}z^{\omega_0}\prod_{i=1}^c(1-z^{L_i}).
\]

Its coefficient of (z−1)^c is (-1)^((n−c)/2)∏L_i. This coefficient has a common sign only after restricting to covers with the same c. Taking the smallest c is therefore essential. Merely saying that every individual cover polynomial is nonzero would not prove that their sum is nonzero. With m the smallest cycle count, the coefficient of (z−1)^m in the total is exactly

\[
(-1)^{(n-m)/2}\sum_{\text{covers with }m\text{ cycles}}\prod_C L(C)\ne0.
\]

The following is the proposed replacement section. It includes the disk calculation so that its precise role remains visible. At the main paper's 10-point setting it is intended as a two-page section; it uses no displayed example, figure, or separate finite-difference lemma.

```latex
\section{Pairs of states}

Let $t_0$ be the outer black face, $A$ the other black faces,
$X$ the nonroot vertices, and $n=|A|=|X|$.
A state is a bijection $s:A\to X$ choosing a corner of each face;
$Q_s$ consists of the sides opposite these corners.
A state is good if $Q_s$ is a forest with one root in each component.
A pair is an ordered pair $(r,s)$ of states differing everywhere.
Write $u(t)$ for the remaining corner of $t$.
For a pair, direct $Q_s$ by $r(t)\to u(t)$ and put
$D(r,s)=\{r(t)\to s(t):t\in A\}$.
The former has outdegree one on $X$ and zero at the roots;
the latter has indegree and outdegree one on $X$.
Thus every component of $Q_s$ is either a tree with one root
or a rootless component with one directed cycle, and $D$ is a
disjoint union of directed cycles covering $X$.
Indeed a connected component with $v$ vertices and $q$ roots
has $v-q$ edges, hence $q\le1$; every undirected cycle is directed
because its edges have distinct tails.
Edges supplied by different black faces are distinct.

\begin{lemma}[disk identity]
Suppose one side at $r(t)$ is directed out of $r(t)$ in every
$t\in A$, and $C$ is a directed cycle of these sides.
If $h=|C|$, $I$ counts its interior vertices, $B,W$ its interior
black and white faces, and $\ell$ its sides with black face inside,
then $W=B+1$ and $h=2\ell+3$.
\end{lemma}
\begin{proof}
The roots are outside $C$.
Euler's formula for the triangulated closed disk and signed
counting of its face sides give
$B+W=2I+h-2$ and $3(B-W)=2\ell-h$.
The bijection $r$ sends the interior black faces precisely onto
the interior vertices and the tails of those $\ell$ boundary sides,
so $B=I+\ell$.
Substitution gives both identities.
\end{proof}

For an oriented edge $vw$ let $\delta(v,w)=1$ if its black face
is on its left, and $-1$ otherwise. Define
\[
 \varepsilon(r,s)=\prod_{t\in A}\delta(r(t),s(t)).
\]
Reversing a cycle of $D$ exchanges $r,s$ on its faces and gives
a pair: its heads and tails are the same vertex set.
Reversing a cycle $K$ of $Q_s$ replaces $r(t)$ by $u(t)$ on its
faces and also gives a pair, for the same reason.
Each operation flips every local sign on its cycle, since
$\delta(s,r)=-\delta(r,s)$ and, in a black triangle,
$\delta(u,s)=-\delta(r,s)$.
The disk identity makes both cycles odd, so both operations
reverse $\varepsilon$.
Moreover, a counterclockwise cycle of length $h$ has
$\delta$-sum $2\ell-h=-3$, and a clockwise one has sum $3$.
If $D$ has $c$ cycles, $c^+$ counterclockwise, their lengths give
$n\equiv c\pmod2$, and counting negative factors gives
\begin{equation}\label{eq:pair-sign}
 \varepsilon(r,s)=(-1)^{(n+c)/2+c^+}.
\end{equation}

Fix a total order on edge subsets.
If $Q_s$ is cyclic, reverse its first cycle for every partner $r$.
The chosen cycle depends only on $s$, which is unchanged;
reversal twice restores $r$.
This is a sign-reversing involution on its partners.
If $Q_s$ is acyclic, the component count above makes $s$ good.
Every good state has exactly one partner: direct each tree towards
its root and take the tails of its edges.
Consequently, for any function $F$ on states,
\begin{equation}\label{eq:pair-cancel}
 \sum_{(r,s)\text{ pair}}\varepsilon(r,s)F(s)
 =\sum_{s\text{ good}}\varepsilon(r_s,s)F(s).
\end{equation}

Assume a pair exists and fix any reference state $s_*$.
Place a point $b_t$ inside each $t\in A$, and draw disjoint
interior spokes from $b_t$ to its three corners.
Let $M_s$ be the integral chain of spokes $b_t\to s(t)$.
Its boundary $\sum_{x\in X}x-\sum_{t\in A}b_t$ is independent of $s$,
so $M_s-M_{s_*}$ is a closed integral chain.
For a point $p_y$ inside each white face, set
\[
 \omega(s)=\sum_{y\text{ white}}
       \operatorname{wind}(M_s-M_{s_*},p_y)\in\mathbb Z,
\]
where counterclockwise winding is positive.
Winding number is additive on closed chains and invariant under
homotopies avoiding the point.
If a clockwise cycle $C$ of $D(r,s)$ is reversed to obtain
$(r',s')$, the chain $M_{s'}-M_s$ is the sum of the paths
$s(t)\to b_t\to r(t)$ on $C$.
Each can be moved to the side $s(t)\to r(t)$ within its closed
black triangle, avoiding every $p_y$.
Thus this chain has the winding numbers of the counterclockwise
cycle $C$. By the Jordan curve theorem,
\begin{equation}\label{eq:pair-weight}
 \omega(s')-\omega(s)=L(C),\qquad
 L(C)=\#\{\text{white faces inside }C\}\ge1.
\end{equation}
The inequality is the other use of the disk identity.

\begin{proposition}
If a pair exists, a good state exists.
\end{proposition}
\begin{proof}
Form the finite Laurent polynomial
$Z(z)=\sum_{(r,s)\text{ pair}}\varepsilon(r,s)z^{\omega(s)}$.
By \eqref{eq:pair-cancel} it is supported on good states.
Group pairs by the undirected edge set of $D$.
Such a cover with cycles $C_1,\ldots,C_c$ has exactly $2^c$ pairs:
orient its cycles independently, taking tails for $r$ and heads
for $s$. Conversely, any pair with this cover must orient each
whole cycle coherently, since both maps are bijections.
Put $L_i=L(C_i)$ and let $\omega_0$ be the second-state weight
when all cycles are clockwise.
Equations \eqref{eq:pair-sign}--\eqref{eq:pair-weight} give its contribution
\[
 (-1)^{(n+c)/2}z^{\omega_0}
 \sum_{J\subseteq[c]}(-1)^{|J|}z^{\sum_{i\in J}L_i}
 =(-1)^{(n+c)/2}z^{\omega_0}\prod_{i=1}^c(1-z^{L_i}).
\]
Its order at $z=1$ is exactly $c$, with coefficient
$(-1)^{(n-c)/2}\prod_iL_i$ at $(z-1)^c$.
Let $m$ be the minimum cycle count among covers.
The coefficient of $(z-1)^m$ in $Z$ is
\[
 (-1)^{(n-m)/2}
 \sum_{\substack{\text{covers}\ D\\c(D)=m}}\prod_{C\in D}L(C),
\]
which is nonzero. Hence $Z\ne0$, and a good state occurs.
\end{proof}
```

## What the preceding sections must supply

Only the following setup is needed. The triangulation is finite, simple, embedded in the oriented sphere, and its triangular faces are properly coloured black and white. Choose a black face t₀ as the outer face of a plane embedding. Its three distinct corners are the roots. A is the set of other black faces, X the set of other vertices, and |A|=|X|=n>0. A state means a bijection A→X incident with its face. Distinct black faces cannot supply the same edge because each edge has just one black incident face. Q_s is the union of the sides opposite s(t), with every vertex retained. Good means a forest with one root per component.

No existence theorem for states, matching theorem, height lemma, or planar duality lemma is needed by the section. A pair is assumed only in the proposition and supplies the reference state. Euler's formula for a triangulated disk, the Jordan curve theorem, and the standard additivity and homotopy invariance of winding number are explicitly invoked. The earlier recovery theorem is needed afterwards to turn a good state into the desired selection and Hamiltonian cycle. The first-pair argument and separating-triangle induction remain separate.

## The weight and its alternatives

The reference-state definition is an exact direct winding definition. A sum of winding numbers of M_s alone would be meaningless: M_s has boundary. Subtracting M_s* closes it, because both states use every nonroot vertex exactly once. There is no need to choose a cycle decomposition of this closed chain. Winding of an integral circulation is defined by linearity, or equivalently by its unique integer face potential normalized to zero in the unbounded face. For a purely combinatorial exposition, that last sentence can replace the geometric definition: extend the spoke graph by the triangulation edges and take the face potential of M_s−M_s*. This is the planar circulation/face-potential correspondence.

This definition shortens the proof because the difference under reversal already is a closed cycle, with each edge detoured through its black face. Detours may overlap the reference spokes; additivity handles overlap. Nested D-cycles cause no problem: their winding functions add, and every reversed clockwise cycle contributes +1 to every white point inside it, including points inside another cycle. No assertion that their interiors are disjoint is used.

The present fixed-path heights give the same normalized weight. Intersect a closed spoke chain with a path from p_y to the outer face. Positive winding is the signed number of exits, and at a black-face turn the intersection is exactly the local corner indicator κ_y. Hence the present height difference η_s(y)−η_s*(y) equals this winding number. The reference-state weight differs from the paper's weight by the constant −ω(s*), multiplying Z by a Laurent monomial. Li's fixed rays are the same intersection calculation with a particular choice of paths. Rays require generic-position conventions; arbitrary paths require local turn conventions. The primal/Lean flow construction is attractive for algebraic formalisation but takes an extra construction of a unit white-face charge flow and local potentials. In a plane drawing the closed-chain definition has the shortest change proof.

The disk identity is used twice, and these uses should stay explicit. Oddness makes both reversals change the local-product sign and determines the cover's common leading sign. W=B+1 makes L(C) strictly positive. The weight-change equality itself uses only winding and Jordan separation, not the disk count. The disk proof in the section uses the three identities B+W=2I+h−2, 3(B−W)=2ℓ−h, B=I+ℓ; removing the last, state-dependent count would invalidate the conclusion.

## The sign and the competing counts

Keep the local product. The permutation r⁻¹s on A, or sr⁻¹ on X, has the same cycle lengths as D; all those lengths are odd. Its permutation sign is therefore always +1. The inverse permutation s⁻¹r has the same defect. It cannot detect either required sign reversal. Multiplying a permutation sign by a counterclockwise-cycle factor recovers the displayed formula only after adding the factor (-1)^((n+c)/2). That reformulation makes Q_s-reversal harder to check, since it can change both the number and arrangement of D-cycles. The local product changes visibly at every affected triangle under both operations, and one disk lemma supplies the oddness. It is the cleaner definition.

The Laurent form is shorter than the power-and-finite-difference proof: it replaces a separate lemma and its multinomial proof by ∏(1−z^L). Its m-th derivative at 1 gives the same nonzero count as the paper's ω^m moment. More precisely the derivative uses falling factorials of ω, but all lower moments vanish, so the two degree-m sums agree. The complex exponential form gives the same leading coefficient after z=e^ξ and a constant phase normalization, with extra complex notation. The anonymous signed integer polynomial is a useful ordinary-polynomial implementation and supports its constructive interpretation; for existence alone, its cycle differences are exactly what this factorization records. Li's two involutions replace the coefficient extraction with marked objects and two cancellations. That gives a bijective explanation but requires more definitions than this section. The sign-free note does not complete a shorter substitute for this core: its simultaneous-condition theorem still requires the signed argument, although its separate feasibility results explain the structure.

## Small-case checks

An independent inline Python enumeration, using only paper/figures/running.json and an explicitly generated octahedron, found 12 states, 8 ordered pairs and 2 covers for the running example; the octahedron has 2 states, 2 ordered pairs and 1 cover. It computed integer corner heights along breadth-first dual paths, the local signs, and interior white-face counts by deleting the cycle's dual crossings and flooding from t₀. For every cover it checked W=B+1 and the entire Laurent-polynomial factorization, not just the leading term. In that path normalization the running polynomial is

\[
z^{-4}-z^{-3}+z^{-2}-z^{-1}-z+z^3
 =z^{-4}(1-z)(1-z^3)+z^{-2}(1-z)(1-z^4).
\]

Its order at 1 is 2 and its leading coefficient is 3+4=7, agreeing with (-1)^((10−2)/2). The octahedron gives z⁻¹−1, with order 1 and coefficient −1, agreeing with (-1)^((3−1)/2). Subtracting a reference-state weight merely translates all exponents. These checks verify the sign normalization, shift direction, positivity, cover size, and absence of cancellation between minimal covers on these two examples; they do not replace the general proof.

Two states turn the chosen corners into directed cycles and turn failure of goodness into a reversible obstruction. The sign makes those obstructions cancel while the weight records the white faces swept out by reversing a cycle. Each cycle then contributes one factor vanishing at 1. Covers with the fewest cycles appear first in the expansion, and their positive enclosed-face counts all come with the same sign. Some good state must therefore survive the cancellation.
