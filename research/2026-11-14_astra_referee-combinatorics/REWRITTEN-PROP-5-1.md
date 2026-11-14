# A forest pair by intersection numbers

Status: `PROVED-HERE`, referee's self-contained presentation of the submitted height-product route. The proposition and disk identity are `LIT`, OpenAI, Proposition 5.1 and Lemma 4.1. The proof below includes the topological step that the submission cites from OpenAI, Section 5.3. It uses no vertex colouring, determinant, assigned spoke circulation, exponential sum, or ordered marks. Human review is pending.

Let $T$ be a finite simple triangulation of the sphere with its faces properly coloured black and white. Choose a black face $t_0$ as the outer face. Its three vertices are the roots. Let $A$ be the other black faces and $X$ the nonroot vertices. Side counting and Euler's formula give $|A|=|X|=n$.

A state is a bijection $s:A\to X$ selecting a corner of each face. A pair is an ordered pair of states $r,s$ such that $r(t)\ne s(t)$ for every $t\in A$. Let $Q_s$ contain the edge opposite $s(t)$ in each $t\in A$, together with all vertices of $T$.

For an oriented edge $v\to w$, put $\delta(v,w)=1$ if its black incident face is on its left, and $-1$ otherwise. We use the disk identity in the following equivalent form. If one chooses, in every $t\in A$, an edge directed from the corner selected by a state, then any simple directed cycle $C$ avoids and encloses no root. In its bounded disk, the numbers $B,W$ of black and white faces satisfy

$$
W=B+1,\qquad |C|-2\ell=3,
$$

where $\ell$ counts boundary edges with their black face inside. Consequently the $\delta$-sum is $-3$ counterclockwise and $3$ clockwise, the length is odd, and the disk contains a white face. These statements follow from the three counts $B=I+\ell$, $E=3B+|C|-\ell=3W+\ell$, and $I+|C|-E+B+W=1$, where $I$ counts strictly interior vertices. The first count uses the state bijection.

**Proposition.** If a pair exists, some pair $r,s$ has $Q_s$ a forest.

**Proof.** For a pair $r,s$, direct the edge of $t$ from $r(t)$ to $s(t)$. These edges form a directed cycle cover $D$ of $X$. They are distinct because an edge has only one black incident face. Its cycles are therefore simple and have odd length. Define

$$
J(r,s)=\frac13\sum_{t\in A}\delta(r(t),s(t)),\qquad
\varepsilon(r,s)=(-1)^{(n+J(r,s))/2}.
$$

The disk identity gives $J=\#\mathrm{clockwise}-\#\mathrm{counterclockwise}$. Thus $J\equiv n\pmod2$, and the sign is defined.

First fix $s$. A partner $r$ directs each opposite edge from $r(t)$ to the third corner of $t$, giving outdegree one at nonroots and zero at roots. If $Q_s$ contains a cycle, choose one using $s$ alone. All its edges must be directed cyclically: their distinct tails exhaust its vertices. Reverse it, changing $r$ and fixing $s$. The new tails are the old heads, so this is a fixed-point-free involution on partners. On each changed face, writing $u$ for the third corner,

$$
\delta(u,s)-\delta(r,s)=2\delta(r,u).
$$

The disk identity on the reversed cycle changes $J$ by $2$ or $-2$. Hence it reverses $\varepsilon$. For any function $F$ of states, all terms with cyclic $Q_s$ cancel in

$$
S_F=\sum_{(r,s)\text{ pair}}\varepsilon(r,s)F(s).                 \tag{1}
$$

We construct $F$ for which this finite sum is nonzero. Put a centre in every face of $A$, joined to its corners by spokes. For each white face $w$, choose a path $\gamma_w$ from its interior to the outer face, avoiding vertices and centres and meeting spokes transversally. Let $h_s(w)$ be the signed intersection count of $\gamma_w$ with the spokes selected by $s$, oriented centre to corner; crossing the oriented path from right to left contributes $1$. Fix these paths once and for all.

Reversing a clockwise cycle $C$ of $D$ to counterclockwise changes these heights by

$$
h_{s_{\rm new}}(w)-h_{s_{\rm old}}(w)
   =\mathbf1_{\{w\text{ inside }C\}}.                             \tag{2}
$$

Indeed, the difference of selected spokes is the counterclockwise curve obtained by replacing each edge of $C$ with its tail-centre-head path. This curve is simple and retains the original orientation. Each replacement takes place across the subdisk between that edge and its spokes, which excludes the third corner. Its interior misses every other edge and detour, since the cycle uses at most one edge of each black face. Sliding across these subdisks preserves simplicity and orientation, even if a third corner occurs elsewhere on the cycle. No white-face point crosses a slide. Finally, the signed intersection of a counterclockwise Jordan curve with a path is the indicator that its initial point is inside minus the corresponding indicator for its endpoint. The endpoint in $t_0$ is outside. This proves (2).

Let $m\ge1$ be the least number of cycles among pairs, which exists by finiteness and the hypothesis. Choose a cover with $m$ cycles, and choose a white face $w_i$ inside its $i$-th cycle. Such a face exists by the disk identity. Repeated choices are allowed. Set

$$
F(s)=\prod_{i=1}^m h_s(w_i).
$$

Group (1) by the underlying undirected cover $D$. A cover with $c$ cycles has exactly $2^c$ pairs, obtained by independently orienting its cycles. Write $x_C=1$ for counterclockwise and $0$ for clockwise. Equation (2) gives its contribution as

$$
(-1)^{(n+c)/2}\sum_{x\in\{0,1\}^c}(-1)^{\sum_Cx_C}
 \prod_{i=1}^m\left(b_i+\sum_Cx_C\mathbf1_{\{w_i\text{ inside }C\}}\right),       \tag{3}
$$

where $b_i$ is the height in the all-clockwise orientation. In the product expansion, every term missing a variable $x_C$ cancels on summing that variable. Since $c\ge m$, a surviving term must have $c=m$ and choose each variable once. Thus (3) is zero for $c>m$; for $c=m$ it equals

$$
(-1)^{(n-m)/2}
\#\{\beta:\{1,\ldots,m\}\xrightarrow{\sim}\mathrm{cycles}(D):
                   w_i\text{ is inside }\beta(i)\text{ for every }i\}.
$$

All nonzero contributions have the same sign. The cover used to choose the $w_i$ contributes at least one. Therefore $S_F\ne0$. The first cancellation shows that some pair has acyclic $Q_s$, as required. $\square$

The same expansion with $j\le m$ factors proves Theorem B of the submission. The word "height" here means an integer defined after paths have been fixed; it makes no assertion of nonnegativity. Changing the paths adds constants independent of the state, and has no effect on the argument.
