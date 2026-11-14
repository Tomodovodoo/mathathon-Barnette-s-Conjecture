# Barnette's conjecture in the cubic graph

Status: PROVED-HERE, a complete informal reconstruction, subject to independent review. The theorem is LIT, OpenAI, Theorem 1.1 and Corollary 7.1. The proof follows the checked Lean development at commit `4eaee87548250b2682affda7d05d947c05554bae`, with two explicit departures: Li's primal deficit proof supplies the first pair, and real local signs replace Lean's complex phases. STATUS.md distinguishes restatements from these departures. Numerical checks are evidence about the implementation, not a proof of the theorem.

## 1. The target and the objects

**Theorem T.** Every finite simple cubic bipartite 3-edge-connected plane graph $G$ has, for every edge $e_0$, a perfect matching $P$ containing $e_0$ such that $G-P$ is connected. Consequently every cubic bipartite 3-vertex-connected planar graph has a Hamiltonian cycle avoiding any prescribed edge.

The connected complement of a perfect matching in a cubic graph has degree two at every vertex, so it is one cycle. This is what we will construct. Working with 3-edge-connectivity keeps the induction within precisely the hypotheses it needs.

Fix an orientation of the sphere, a bipartition $B,W$ of $V(G)$, and an edge $e_0=b_0w_0$ with $b_0\in B$. Write $\mathcal F$ for the faces of $G$. The three faces at $b_0$ form $R$. Put

$$
A=B\setminus\{b_0\},\qquad X=\mathcal F\setminus R,\qquad n=|A|.
$$

We use faces as incidence labels. We never construct a triangulation, a spoke graph, or a labelling by the two sides of the final Hamiltonian cycle. A *face link* is simply an edge $e$ of $G$, regarded as joining its two incident faces. A face circuit is a cyclic list of distinct faces $f_0,\ldots,f_{h-1}$ and distinct edges $e_i$ with $e_i$ incident with $f_i,f_{i+1}$, with indices modulo $h$. This is an incidence description on $G$; no drawn arcs through faces are required. Forest and connected-component language for face links means the corresponding ordinary finite incidence relation on the face labels. This relation retains the cycle-cut content of planar duality. Avoiding the triangulation does not remove that content.

**Lemma 1, elementary setup.** PROVED-HERE. Facial boundaries are cycles; each vertex is incident with three distinct faces; two faces share at most one edge; and

$$
|B|=|W|=n+1,\qquad |E|=3(n+1),\qquad |\mathcal F|=n+3,\qquad |X|=n.
$$

Proof. A cut vertex of a connected cubic graph has a component attached by at most one of its three edges, producing a bridge. Thus our graph is 2-connected. In a 2-connected plane graph the facial boundary walks have no repeated vertex: a repetition separates the incident sectors into two nonempty blocks, and paths between the corresponding parts must pass through that vertex. This is the usual boundary-walk criterion for a cut vertex. Consequently each facial boundary is a cycle. If a face used two sectors at a cubic vertex it would repeat that vertex. The three faces there are distinct. Two faces sharing two edges would give a two-edge face circuit. Lemma 2 below makes that a two-edge bond, impossible here. Count edges from the two colour classes to get $3|B|=|E|=3|W|$, and use Euler's formula $|V|-|E|+|\mathcal F|=2$. This proves the displayed counts. The appeal to Lemma 2 uses only its general face-circuit assertion, not the present simplicity conclusions.

## 2. The planar facts, with their scope stated

We accept the elementary calculus of finite plane embeddings: facial boundary walks with their cyclic orders, Euler's formula for a connected plane graph, deletion of an edge merging its two distinct incident faces, and contraction of a nonloop edge preserving a plane embedding. We also use the boundary-walk criterion for a cut vertex explained in Lemma 1. These are the planar background facts. We do not invoke a Jordan curve labelling theorem, an isotopy of a detoured cycle, or a theorem about two induced trees.

The following lemma isolates the two planar facts used by the four-count identity. Its first part also supplies the cycle-cut test used later.

**Lemma 2, face circuits and cut-side faces.** PROVED-HERE; Lean counterparts are `Duality.circuit_cut`, `Bond.connected_shore`, `region_euler`, and `mixed_corner_on_boundary`.

(a) A face circuit is exactly the edge set of a bond of $G$, a nonempty inclusion-minimal edge cut. Its two shores induce connected graphs. If a face circuit avoids the three faces in $R$, let $S$ be the unique shore not containing $b_0$. Call this its *cut side*. No root face meets $S$.

(b) For connected complementary shores $S,\overline S$, let $E_S$ be all edges with an end in $S$, and $U_S$ all faces incident with a vertex of $S$. Then

$$
|S|+|U_S|=|E_S|+1.                                      \tag{2.1}
$$

A face meeting both shores contains a cut edge on its boundary. If the cut is a face circuit, the mixed faces are precisely its listed faces. This is the no-pinch assertion needed here.

Proof. We give the cycle-cut argument without drawing a separating curve. Over $\mathbb F_2$, the boundary vectors of the faces span the cycle space of $G$. Here is the standard Euler proof of this fact. Their sum is zero. Every other dependence assigns equal coefficients to the two faces at each edge. All faces are linked by successive edge incidences, so those coefficients are all equal. Face-incidence connectivity follows, for example, by contracting a spanning tree and deleting the remaining loops one by one. The resulting one-vertex graph remains connected at each deletion, so Euler forces its face count to fall by one; that deletion merges its two incident faces. Eventually only one face remains. Thus the boundary span has dimension $|\mathcal F|-1=|E|-|V|+1$, the cycle-space dimension. Facial boundaries are even-degree edge sets, so their span is the whole cycle space.

An edge set is therefore a cut exactly when it meets every facial boundary evenly. For completeness, the orthogonal complement of the cycle space is the cut space: if an edge indicator has even sum on every cycle, its path sum from a fixed vertex is independent of the path; its value on an edge is the difference of the two vertex path sums. In characteristic two this is the cut of the vertices assigned value one.

A face circuit meets each of its faces twice, and all other faces zero times, so is a cut. A proper nonempty subset cannot meet all those faces evenly: following the cyclic list propagates the choice of one edge to all of them. Hence this cut is a bond. Conversely, the edge set of a cut gives an even-degree face-link relation. A nonempty such relation contains a circuit, which is itself a cut by the argument just given. Minimality of a bond makes it that single circuit. The assertions include loops or parallel face links if present; 3-edge-connectivity rules out circuits of length one or two.

A cut is minimal precisely when both shores are connected. If a shore had two components, the boundary of one would be a proper nonempty subcut. Conversely, if both shores are connected, deleting a proper subset leaves an edge joining the shores and leaves each shore connected.

For the no-pinch statement, traverse the boundary walk of a face with vertices in both shores. Membership must change somewhere, along a cut edge. A face on the circuit has two such edges and meets both shores; a face off it has none. Since $b_0\notin S$, a root face meeting $S$ would be mixed and hence on the circuit, contrary to its avoidance of $R$.

Finally delete the vertices of $S$ and all incident edges. All faces in $U_S$ merge into one face: removing the star of one vertex joins its incident sectors, and stars at adjacent vertices of the connected graph $G[S]$ make these mergers connected. No face outside $U_S$ changes. The remaining graph $G[\overline S]$ is connected, so its face count is $|\mathcal F|-|U_S|+1$. Subtract its Euler equation from the Euler equation for $G$ to obtain (2.1). This argument also handles a singleton shore. It requires both shores connected; it makes no assumption that a boundary has been drawn as a round disk.

We need the oriented version of (a). For a directed transition $f\to g$ across an edge with black end $b$, put $\delta(f,g)=+1$ when $b$ is on the left of the transition, and $-1$ otherwise. Equivalently, fix the cyclic order of the three faces around $b$ and give its three cyclic transitions sign $+1$. This definition uses only the oriented rotation system. Orient every edge of $G$ from black to white.

**Lemma 3, orientation of a bond.** PROVED-HERE. On an oriented face circuit with cut side $S$, there is a common $\sigma\in\{1,-1\}$ such that

$$
\delta(f_i,f_{i+1})=\sigma\bigl(\mathbf1_S(b_i)-\mathbf1_S(w_i)\bigr).       \tag{2.2}
$$

Call $\sigma=+1$ the positive orientation.

Proof. The real signed facial boundary vectors span the real cycle space by exactly the dimension proof in Lemma 2, orienting every facial boundary consistently. Give each crossed edge the value $\delta(f_i,f_{i+1})$ and the other edges value zero. Its pairing with a facial boundary is zero: arrival and departure at each listed face cancel. It is therefore a vertex gradient. Since its support is a bond, its vertex potential is constant on each connected shore. Its nonzero values have magnitude one, giving (2.2). This also proves that reversing a circuit reverses $\sigma$.

## 3. The incidence matchings and existence of a pair

A *state* is a bijection $s:A\to X$ assigning to each black vertex an incident face. It is a perfect matching of the bipartite incidence relation between $A$ and $X$. A *pair* is two states $r,s$ such that $r(b)\ne s(b)$ for every $b\in A$.

For a state $s$, let $q_s(b)$ be the unique edge at $b$ not on face $s(b)$. Let $Q_s$ be the set of these $n$ edges, regarded as face links. For a pair, orient $q_s(b)$ from $r(b)$ to the third face at $b$. Each nonroot face has one outgoing link and root faces have none. If $Q_s$ has a circuit, it is directed: the distinct tails of its edges exhaust its vertices. In particular that circuit avoids $R$.

**Lemma 4, a pair exists in the irreducible case.** PROVED-HERE, expanding Li, Lemma 9 and Claim 12; its conclusion matches Lean's `ColoredDual.pair_nonempty`. Suppose every three-edge cut has a singleton shore. Then a pair exists.

Proof. The two incidence parts have equal size $n$, by Lemma 1. We first explain the exact capacity criterion. Direct a network from a source to each face of $X$ with capacity two, from a face to each incident $b\in A$ with capacity one, and from each $b$ to the sink with capacity two. For a source-side set of faces $Y$, minimizing the contribution of each black vertex to a cut gives $\min(2,|N(b)\cap Y|)$. Thus every source-sink cut has capacity at least $2n$ exactly when

$$
\sum_{b\in A}\min(2,|N(b)\cap Y|)\ge 2|Y|\quad\hbox{for every }Y\subseteq X.    \tag{3.1}
$$

Integral max-flow then gives a degree-two spanning subgraph of the incidence relation. It consists of even cycles, whose alternate edges give the required pair. Integral max-flow is the only matching existence theorem used here.

Suppose (3.1) fails. Choose a nonempty inclusion-minimal set $Y$ of positive deficit

$$
d(Y)=2|Y|-\sum_{b\in A}\min(2,|N(b)\cap Y|)>0.
$$

Let $K$ be the union in $G$ of the boundaries of faces of $Y$. Write $B_j,W_j$ for vertices incident with exactly $j$ faces of $Y$, for $j=1,2,3$. The root is not in $K$. Distinct components of $K$ partition $Y$, and the deficit adds over this partition. Minimality therefore makes $K$ connected.

There is no vertex in $W_1$. If $w\in W_1$ lies on $f\in Y$, its two neighbours along $f$ are distinct black vertices. Each is incident with a face outside $Y$, namely the other face at its edge to $w$, and hence belongs to $B_1$ or $B_2$. Removing $f$ lowers the sum in the deficit by at least two and lowers $2|Y|$ by two. The remaining set still has positive deficit, a contradiction.

A vertex in $B_2\cup B_3\cup W_2\cup W_3$ has all three of its edges in $K$, whereas a vertex in $B_1$ has just two. Its third edge must leave $V(K)$: if its white endpoint were in $K$, that endpoint would be in $W_2\cup W_3$ and the edge would already belong to $K$. Thus $K=G[V(K)]$, and its cut has size $c=|B_1|$, with all ends in $V(K)$ black. Counting its internal edges from the two colours gives

$$
c=3\bigl(|B\cap V(K)|-|W\cap V(K)|\bigr).                         \tag{3.2}
$$

Let $k$ be the number of faces of the embedded connected graph $K$ not among the original faces $Y$. It is at least one: the omitted root lies in one of these faces. Euler and the degree count give

$$
2|Y|+2k=4+|B_2|+|B_3|+|W_2|+|W_3|.
$$

Subtracting $|B_1|+2|B_2|+2|B_3|$ yields

$$
d(Y)=4-2k-c/3.
$$

The cut is nonempty, since $K$ omits $b_0$ and $G$ is connected. Hence $c\ge3$. Since $d(Y)\ge1$ and $k\ge1$, necessarily $k=1$ and $c=3$. This cut is nontrivial. Its $K$ shore contains a facial cycle, of length at least four by simplicity and bipartiteness. Its other shore contains $b_0$ and a white endpoint of the cut. This contradicts the hypothesis, proving (3.1).

The stronger colour-sensitive obstruction is visible here: a deficient set produces a root-free three-edge cut whose inner ends are black. We will not need the converse or the sharper decomposition theorem from the constructive paper.

## 4. The four-count identity

**Lemma 5, the cut-side identity.** PROVED-HERE, restating the conjunction of Lean's `state_disk_count` and `disk_boundary_imbalance`; LIT in equivalent form, OpenAI, Lemma 4.1. Let $r$ be a state. At each $b\in A$ choose one of the two edges of face $r(b)$ incident with $b$, directing its face link from $r(b)$ to its other face. Suppose some chosen links form a directed face circuit $C$. Let $S$ be its cut side, $h=|C|$, and let $\ell$ count its cut edges whose black endpoint belongs to $S$. Then

$$
h=2\ell+3,\qquad |W\cap S|=|B\cap S|+1,\qquad
\sum_{C}\delta=-3\sigma.                                         \tag{4.1}
$$

In particular $h$ is odd and $S$ contains a white vertex.

Proof. Every tail belongs to $X$, so the circuit avoids $R$. Both shores are connected by Lemma 2. Put $U=U_S$ and $E_S$ as in that lemma. The four counts are

$$
\begin{aligned}
3|S|+h&=2|E_S|,\\
3|B\cap S|+h&=|E_S|+\ell,\\
|S|+|U|&=|E_S|+1,\\
|B\cap S|+h&=|U|+\ell.
\end{aligned}\tag{4.2}
$$

The first counts ends at $S$. In the second, $3|B\cap S|$ counts internal edges and the $\ell$ black-ended boundary edges; adding $h$ gives the displayed form. The third is (2.1).

Here are all details of the state count, the fourth equation. The set $U$ is the union of $r(B\cap S)$ and the $h$ faces of $C$. Indeed, $U$ contains no root face by Lemma 2. A face in $U$ off $C$ has every boundary vertex in $S$ by the no-pinch statement, so its unique state partner is in $B\cap S$. Conversely both sets are contained in $U$. Their intersection has size $\ell$: a face on $C$ is the assigned face of the black endpoint of its outgoing circuit edge, and that endpoint is in $S$ exactly for those $\ell$ edges. Bijection of $r$ makes this count exact, with no duplicates. Inclusion-exclusion proves the fourth equation.

Eliminating $|S|,|U|,|E_S|$ from (4.2) gives $h-2\ell=3$. The colour degree count on the cut is

$$
3\bigl(|B\cap S|-|W\cap S|\bigr)=2\ell-h=-3,
$$

which gives the second assertion. Sum (2.2) to get the final assertion. Only the third count and the no-pinch part of the fourth need the planar facts of Lemma 2.

## 5. One flow and its local potentials

**Lemma 6, the weights.** PROVED-HERE, a primal restatement of Lean's `boundary_of_sum_zero`, `whiteCharge_cut_integral`, and `StateCycle.signed`. There are integer weights $a(b,f)$ for incident pairs $b\in A$, $f\ni b$, such that for every directed state circuit with cut side $S$,

$$
\sum_{b\text{ on }C}\bigl(a(b,f_{\rm head})-a(b,f_{\rm tail})\bigr)
=\sigma|W\cap S|.                                                \tag{5.1}
$$

Proof. Send one unit along a path in $G$ from $b_0$ to each $w\in W$, adding signed flows on the edges oriented black to white. Call the resulting integer flow $\alpha$. Its outgoing divergence is $|W|$ at $b_0$, $-1$ at each white vertex, and zero at every other black vertex.

At $b\in A$ define local face potentials, up to an additive constant, by

$$
a(b,g)-a(b,f)=-\delta(f,g)\alpha(e)                               \tag{5.2}
$$

when $f,g$ are the two faces at $e\ni b$. These three equations are consistent. Following the three faces in their positive cyclic order gives the negative sum of $\alpha$ on the three edges oriented away from $b$, which is zero. Fix one potential to zero to obtain integer values.

Now sum (5.2) around $C$ and use (2.2). The result is $-\sigma$ times the outward flux of $\alpha$ through $\partial S$. The root is outside $S$, so summing divergences over $S$ gives outward flux $-|W\cap S|$. This proves (5.1). Lemma 5 makes this strictly positive for $\sigma=+1$. Neither integrality of the flow nor of the weights is needed for existence; integer paths make exact examples easy.

## 6. One polynomial, two expansions

For a pair define its real sign and its weight polynomial by

$$
\varepsilon(r,s)=\prod_{b\in A}\delta(r(b),s(b)),\qquad
L_s(z)=\prod_{b\in A}(1+a(b,s(b))z).
$$

Set

$$
Z(z)=\sum_{(r,s)\text{ pair}}\varepsilon(r,s)L_s(z)\in\mathbb Z[z].           \tag{6.1}
$$

There is no index $J$, exponential, or analytic limit.

**Lemma 7, cancellation.** PROVED-HERE. For any fixed $s$ for which $Q_s$ contains a face circuit,

$$
\sum_{r:(r,s)\text{ pair}}\varepsilon(r,s)=0.                      \tag{6.2}
$$

Proof. If there are no partners the sum is empty. Otherwise fix a circuit of $Q_s$ by a rule depending only on $s$, for instance a fixed total order on finite edge subsets. Every partner $r$ directs it cyclically, as observed in Section 3. On its black vertices replace $r(b)$ by the third face $u(b)$, leaving $s$ fixed. The new tails are precisely the old heads, so the result $r'$ is still a bijection onto $X$; it differs from $s$ everywhere. The operation is a fixed-point-free involution because the chosen undirected circuit is unchanged. At each changed black vertex, $\delta(u(b),s(b))=-\delta(r(b),s(b))$. Lemma 5 says the number of changes is odd, so the sign reverses. Since $L_s$ depends only on $s$, the same cancellation holds in (6.1).

**Lemma 8, nonvanishing.** PROVED-HERE. If there is at least one pair, $Z\ne0$. Hence there is a pair whose $Q_s$ has no face circuit.

Proof. A pair selects at each black vertex the edge whose incident faces are $r(b)$ and $s(b)$, directed from the former to the latter. Call this collection $D$. Each face in $X$ has one incoming and one outgoing link. There are no loops, and no two-edge circuits, by Lemma 1 and the fact that each primal edge has exactly one black endpoint and is selected at most once. Thus $D$ is a disjoint union of simple face circuits covering $X$. Each is a state circuit for $r$.

Fix the undirected collection $D$. Its pairs are exactly the independent choices of direction on its circuits. Indeed, a choice of direction supplies each face once as tail and once as head, and each black vertex labels exactly one selected edge. There are exactly $2^{c(D)}$ such pairs. For a circuit of length $h$, its positive orientation has delta-sum $-3$, and hence $(h+3)/2$ negative local signs. The reverse orientation has the opposite product sign because $h$ is odd. Let $L_C^+$ and $L_C^-$ be the products of $1+a(b,f_{\rm head})z$ along the two orientations. The group's sum is therefore

$$
(-1)^{(n-c(D))/2}\prod_{C\subset D}(L_C^+-L_C^-).                 \tag{6.3}
$$

To check the prefactor, multiply $(-1)^{(h+3)/2}$ over the circuits. The exponent is $(n+3c(D))/2$, which differs from $(n-c(D))/2$ by $2c(D)$. Both are integers because all circuit lengths are odd.

Each difference has constant term zero and, by Lemma 6, linear coefficient

$$
\lambda_C=\sum_{b\text{ on }C}\bigl(a(b,f_{\rm head+})-a(b,f_{\rm head-})\bigr)
=|W\cap S_C|>0.
$$

Let $m$ be the least number of circuits in any $D$, which exists because pairs exist. All terms of degree below $m$ vanish. The coefficient of degree $m$ is

$$
[z^m]Z=(-1)^{(n-m)/2}\sum_{D:c(D)=m}\prod_{C\subset D}|W\cap S_C|\ne0.       \tag{6.4}
$$

Every factor in this nonempty sum is positive. This proves nonvanishing. If every second state had cyclic $Q_s$, Lemma 7 would instead make $Z=0$. Some $Q_s$ is therefore circuit-free.

Oddness is enough for Lemma 7. The exact signed value three is needed in (6.3) to give all groups with the same number of circuits the same sign. This distinction is easy to lose when compressing the proof.

## 7. Recovering the perfect matching in G

**Lemma 9, the recovery tree.** PROVED-HERE, restating Lean's `removed_acyclic`, `remainder_connected`, and `remainder_black_degree`. For a pair with circuit-free $Q_s$, put

$$
K=G-\bigl(Q_s\cup(\partial\{b_0\}\setminus\{e_0\})\bigr).
$$

Then $K$ is a spanning tree, with degree two at every black vertex other than $b_0$, and degree one at $b_0$.

Proof. Orient $Q_s$ using its partner $r$. Each nonroot face has outdegree one and each root face outdegree zero. Since it is a forest of face links, a component with $v$ faces and $k$ roots has both $v-k$ edges by outdegree counting and $v-1$ edges by being a tree. Hence $k=1$. This includes isolated root faces.

The two removed edges at $b_0$ join the three root faces as a two-edge path. Adding them to $Q_s$ therefore joins its three components into a face-link tree. Call the added collection $L$. If $G-L$ were disconnected, $L$ would contain a bond of $G$, and hence a face circuit by Lemma 2, a contradiction. Thus $K$ is connected. It has $3(n+1)-(n+2)=2n+1=|V(G)|-1$ edges, and is a tree. Each nonroot black vertex lost exactly $q_s(b)$, and the root lost its other two edges. This proves the degree statements.

**Lemma 10, the selected matching.** PROVED-HERE, a constructive version of Lean's `tree_matching` and `recovery_matching`. Root $K$ at $b_0$. For every white vertex select its edge toward the root. These edges form a perfect matching $P\subseteq E(K)$ containing $e_0$.

Proof. Every white vertex has exactly one parent edge. Every nonroot black vertex has degree two in $K$, one parent and one child, both white. It is selected by its white child, and by no other white vertex. The root has the single white child $w_0$ and is selected by it through $e_0$. Each black and white vertex is therefore covered exactly once. Since $P$ avoids $q_s(b)$, its edge at $b\ne b_0$ lies on the assigned face $s(b)$.

**Lemma 11, matching cut balance.** PROVED-HERE; Lean's `matching_cut_balance`. If the cut $\partial S$ is contained in any perfect matching of a cubic bipartite graph and $\ell$ of its $h$ edges have black ends in $S$, then $h=2\ell$.

Proof. Let $p$ count matching edges internal to $S$, and $b=|B\cap S|$, $w=|W\cap S|$. Matching degrees give $b=p+\ell$ and $w=p+h-\ell$, so $b-w=2\ell-h$. Cubic degrees give $3(b-w)=2\ell-h$. Subtract to obtain $b=w$ and $h=2\ell$.

**Lemma 12, the complement is one cycle.** PROVED-HERE, restating Lean's `selectNet_forest`, `selected_forest`, and `recover_connected_complement`. The matching from Lemma 10 has connected complement.

Proof. First consider $P\setminus\{e_0\}$ as face links. Direct its edge at $b\in A$ from $s(b)$ to the other incident face. Every nonroot face has one outgoing link and root faces have none. Any face circuit would therefore be directed and would be a state circuit for $s$. Its cut side would satisfy $h=2\ell+3$ by Lemma 5. All its edges belong to $P$, so Lemma 11 gives $h=2\ell$, a contradiction. Thus these links are a forest. The same component count as in Lemma 9 gives exactly one root face per component. Adding $e_0$, which joins two distinct root faces, still creates no face circuit.

If $G-P$ were disconnected, $P$ would contain a bond and hence a face circuit, again a contradiction. Thus $G-P$ is connected. It has degree two everywhere because $P$ is a perfect matching. Following successive edges in a finite degree-two graph closes a cycle without a branch; connectedness says it contains every vertex. It is the required Hamiltonian cycle and avoids $e_0$.

The phrase "one selected edge per face" from the original paper has become "one selected edge per vertex of $G$" here. We do not claim that the perfect matching uses one edge on each primal face.

## 8. The induction over three-edge cuts

**Lemma 13, caps and gluing.** PROVED-HERE, expanding Li, Appendix C, and matching the statements of Lean's `cap_simple`, `cap_cubic`, `cap_threeConnected`, `cap_coloring`, `cap_glue_matching`, and `cap_glue_connected`. Suppose $\partial S$ has size three and both shores have at least two vertices. Contract either shore to a new vertex, deleting internal loops. The resulting two capped graphs are smaller simple cubic bipartite 3-edge-connected plane graphs. Hamiltonian cycles in the caps that omit the same one of the three boundary edges glue to a Hamiltonian cycle of $G$.

Proof. Each shore is connected. Otherwise its distinct components would each have boundary size at least three, exceeding the total three. Let $\ell$ be the number of cut edges with black ends in $S$. The colour count gives

$$
3(|B\cap S|-|W\cap S|)=2\ell-3.
$$

The right side is one of $-3,-1,1,3$, and is divisible by three. Hence $\ell=0$ or $3$. All cut ends on each shore have the same colour, so the new cap vertex receives the opposite colour.

The three ends on each shore are distinct. If a vertex $v$ had two boundary edges, removing it from that shore would leave a nonempty set with at most two boundary edges: one remaining old cut edge plus at most one edge to $v$. If it had all three, connectedness of that nontrivial shore would already fail. This contradicts 3-edge-connectivity. Caps are therefore simple and cubic. Contracting a spanning tree of the removed connected shore and deleting the resulting loops preserves planarity. Every edge cut in a cap lifts to an edge cut of equal size in $G$, by placing the entire contracted shore on the side containing its cap vertex. Thus every cap is 3-edge-connected. Each has fewer vertices because the contracted shore had at least two.

Delete the cap vertex from a Hamiltonian cycle in each cap. What remains is a spanning path in that shore whose two ends correspond to the two used boundary edges. If the cycles omit the same third edge, their two paths and those two boundary edges form a single cycle through both shores. Their complementary matchings likewise agree on the cut, using exactly the omitted edge.

Proof of Theorem T. Apply strong induction on $|V(G)|$, with the quantifier "for every edge $e_0$" retained. If there is no nontrivial three-edge cut, Lemmas 4 through 12 prove the assertion. Otherwise use Lemma 13. Choose as the first cap a side on which $e_0$ remains an edge; if $e_0$ crosses the cut either side works. By induction choose its Hamiltonian cycle avoiding $e_0$. It omits exactly one cap edge, say $a$. In the other cap use induction with prescribed avoided edge $a$. The cycles glue by Lemma 13. If $e_0$ is internal to the first side, its avoidance persists. If it is a boundary edge, it is precisely $a$ and is again avoided. The complement is the desired matching containing $e_0$.

Finally a cubic 3-vertex-connected graph is 3-edge-connected in the present setting. To see this directly, suppose a cut had at most two edges. Each shore has at least three vertices: a singleton has three outgoing edges, and a two-vertex set has at least four in a simple cubic graph. Delete the at most two cut endpoints on one shore. A vertex remains on that shore and all vertices remain on the other, with no path between them. This contradicts 3-vertex-connectivity. The theorem therefore applies to every graph in Barnette's conjecture.

## 9. What each hypothesis does

Finiteness supplies the enumerations, minima, flow network, and strong induction. Simplicity rules out two-vertex facial cycles and ensures the small-shore cut argument. Cubicity supplies three incident faces, the unique opposite edge, the four counts, the recovery-tree degrees, and the cap degrees. Bipartiteness supplies balanced incidence parts, the local black-edge labels, the colour counts, and the matching recovery. Planarity supplies Lemmas 1 through 3 and Euler in Lemma 4, and survives capping. Three-edge-connectivity makes face links simple, excludes a deficient cut of size less than three, and makes caps simple and connected. The additional absence of nontrivial three-edge cuts is used only in Lemma 4.

The real-sign polynomial proof in Section 6 is the linear-weight refinement from the local determinant referee report, Section 2. The flow and cut-side form of the disk identity come from the Lean development. The complete argument written here is an informal proof, not a new Lean file or a claim that this exact prose has been machine-checked.

## 10. Sources

LIT. OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, September 24, 2026, especially Proposition 3.1, Lemma 4.1, Proposition 5.1, Lemmas 6.1 and 6.2, and Corollary 7.1. Repository copy: papers/OpenAI-Barnette.pdf.

LIT. Zhentao Li, *A note on the proof of Barnette's conjecture*, arXiv:2610.30490v1, October 21, 2026, especially Lemma 9, Claim 12, Lemma 30, and Appendix C. Repository copy: papers/A-Note-On-Barnette.pdf. We use the written deficit proof, supply its balance and connectivity details, and do not rely on the sketched general case of Appendix B.

LIT. *A constructive proof of Barnette's conjecture*, October 18, 2026, repository copy papers/barnette_trees.pdf, Proposition 2.1 and Theorem 1.2. Its incidence-tree viewpoint helps explain the unique partner in the recovery case; its sharper obstruction theorem is not an input here.

Source-checked Lean statements and exact file locations are recorded in STATUS.md and research/2026-11-14_astra_primal-proof/LEAN-EXTRACTS.md. The local reverse-Lamport audit is AUDIT.md in that research folder. Worked examples generated by the primal checker follow below.

## 11. Two exact worked examples

COMPUTED. All data below are regenerated by check_primal.py and build_note.py. Vertices are integers. Face labels are the listed boundary cycles in the rotation system returned by NetworkX. Edge labels are local to each example. The checker imports only graph generators and the facial-walk routine from workings/barnette_lab; it constructs all states, cuts, flows, signs, polynomials and recovered matchings itself. Both colourings put the specified root in the black class.

### The cube

The graph has 8 vertices. Its root is $b_0=0$ and its prescribed edge is $e_0^{\rm prescribed}=(0, 1)$. In the edge numbering below this is $e_{0}$. The superscript keeps the prescribed edge distinct from the enumerated label $e_0$.

$B=\{0,2,5,7\}$, $W=\{1,3,4,6\}$, $A=\{2,5,7\}$, $R=\{0,1,2\}$, and $X=\{3,4,5\}$.

The full edge list and flow follow. Every flow value is signed in the black-to-white direction, regardless of the numerical order of its endpoints.

$e_{0}=(0, 1)$, $\alpha(e_{0})=2$.

$e_{1}=(0, 3)$, $\alpha(e_{1})=1$.

$e_{2}=(0, 4)$, $\alpha(e_{2})=1$.

$e_{3}=(1, 2)$, $\alpha(e_{3})=-1$.

$e_{4}=(1, 7)$, $\alpha(e_{4})=0$.

$e_{5}=(2, 3)$, $\alpha(e_{5})=0$.

$e_{6}=(2, 6)$, $\alpha(e_{6})=1$.

$e_{7}=(3, 5)$, $\alpha(e_{7})=0$.

$e_{8}=(4, 5)$, $\alpha(e_{8})=0$.

$e_{9}=(4, 7)$, $\alpha(e_{9})=0$.

$e_{10}=(5, 6)$, $\alpha(e_{10})=0$.

$e_{11}=(6, 7)$, $\alpha(e_{11})=0$.

The facial boundary cycles are:

$f_{0}=(0,3,2,1)$.

$f_{1}=(0,4,5,3)$.

$f_{2}=(0,1,7,4)$.

$f_{3}=(1,2,6,7)$.

$f_{4}=(2,3,5,6)$.

$f_{5}=(4,7,6,5)$.

The black-vertex incidence lists and local potentials are:

$b=0$ has incident faces $(0,1,2)$; no state potential at the root is needed.

$b=2$ has incident faces $(0,3,4)$ and potentials $(0,1,0)$ in that order.

$b=5$ has incident faces $(1,4,5)$ and potentials $(0,0,0)$ in that order.

$b=7$ has incident faces $(2,3,5)$ and potentials $(0,0,0)$ in that order.

Every state is listed below as the tuple of assigned face indices in the displayed order of $A$. Its $Q$ list uses the enumerated edges, and $c_s$ is the sum of signs over its partners.

$s_{0}=(3,4,5)$, $Q_{s_0}=\{e_{4},e_{5},e_{8}\}$, $c_{s_0}=-1$.

$s_{1}=(4,5,3)$, $Q_{s_1}=\{e_{3},e_{7},e_{9}\}$, $c_{s_1}=1$.

Every ordered pair follows, including all of its directed face circuits, cut sides, four-count data and slopes. A tuple of faces gives the cyclic order. Its crossed edges are listed in the same order. In the count tuple the entries are $|S|,|B\cap S|,|E_S|,|U_S|,h,\ell$.

Pair $(s_{0},s_{1})$ has sign $1$.

Faces $(3,4,5)$; edges $(e_{6},e_{10},e_{11})$; cut side $S=\{6\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Pair $(s_{1},s_{0})$ has sign $-1$.

Faces $(3,5,4)$; edges $(e_{11},e_{10},e_{6})$; cut side $S=\{6\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

The exact polynomial is

$$
Z(z)=-1z.
$$

For recovery choose $s_{0}$. The removed edge set is $\{e_{1},e_{2},e_{4},e_{5},e_{8}\}$.

The recovery tree has edges $\{e_{0},e_{3},e_{6},e_{7},e_{9},e_{10},e_{11}\}$.

The selected perfect matching is $P=\{e_{0},e_{6},e_{7},e_{9}\}$.

Its complementary Hamiltonian cycle, in cyclic vertex order, is $(1,2,3,0,4,5,6,7)$. It avoids the prescribed edge.

### A 20-vertex cancellation example

The graph has 20 vertices. Its root is $b_0=0$ and its prescribed edge is $e_0^{\rm prescribed}=(0, 1)$. In the edge numbering below this is $e_{0}$. The superscript keeps the prescribed edge distinct from the enumerated label $e_0$.

$B=\{0,2,4,7,9,11,13,15,16,19\}$, $W=\{1,3,5,6,8,10,12,14,17,18\}$, $A=\{2,4,7,9,11,13,15,16,19\}$, $R=\{0,1,2\}$, and $X=\{3,4,5,6,7,8,9,10,11\}$.

The full edge list and flow follow. Every flow value is signed in the black-to-white direction, regardless of the numerical order of its endpoints.

$e_{0}=(0, 1)$, $\alpha(e_{0})=3$.

$e_{1}=(0, 5)$, $\alpha(e_{1})=5$.

$e_{2}=(0, 6)$, $\alpha(e_{2})=2$.

$e_{3}=(1, 2)$, $\alpha(e_{3})=-1$.

$e_{4}=(1, 15)$, $\alpha(e_{4})=-1$.

$e_{5}=(2, 3)$, $\alpha(e_{5})=0$.

$e_{6}=(2, 14)$, $\alpha(e_{6})=1$.

$e_{7}=(3, 4)$, $\alpha(e_{7})=2$.

$e_{8}=(3, 11)$, $\alpha(e_{8})=-1$.

$e_{9}=(4, 5)$, $\alpha(e_{9})=-3$.

$e_{10}=(4, 10)$, $\alpha(e_{10})=1$.

$e_{11}=(5, 7)$, $\alpha(e_{11})=-1$.

$e_{12}=(6, 9)$, $\alpha(e_{12})=-1$.

$e_{13}=(6, 16)$, $\alpha(e_{13})=0$.

$e_{14}=(7, 8)$, $\alpha(e_{14})=1$.

$e_{15}=(7, 10)$, $\alpha(e_{15})=0$.

$e_{16}=(8, 9)$, $\alpha(e_{16})=0$.

$e_{17}=(8, 13)$, $\alpha(e_{17})=0$.

$e_{18}=(9, 18)$, $\alpha(e_{18})=1$.

$e_{19}=(10, 13)$, $\alpha(e_{19})=0$.

$e_{20}=(11, 12)$, $\alpha(e_{20})=1$.

$e_{21}=(11, 14)$, $\alpha(e_{21})=0$.

$e_{22}=(12, 13)$, $\alpha(e_{22})=0$.

$e_{23}=(12, 19)$, $\alpha(e_{23})=0$.

$e_{24}=(14, 15)$, $\alpha(e_{24})=0$.

$e_{25}=(15, 17)$, $\alpha(e_{25})=1$.

$e_{26}=(16, 17)$, $\alpha(e_{26})=0$.

$e_{27}=(16, 18)$, $\alpha(e_{27})=0$.

$e_{28}=(17, 19)$, $\alpha(e_{28})=0$.

$e_{29}=(18, 19)$, $\alpha(e_{29})=0$.

The facial boundary cycles are:

$f_{0}=(0,1,2,3,4,5)$.

$f_{1}=(0,6,16,17,15,1)$.

$f_{2}=(0,5,7,8,9,6)$.

$f_{3}=(1,15,14,2)$.

$f_{4}=(2,14,11,3)$.

$f_{5}=(3,11,12,13,10,4)$.

$f_{6}=(4,10,7,5)$.

$f_{7}=(6,9,18,16)$.

$f_{8}=(7,10,13,8)$.

$f_{9}=(8,13,12,19,18,9)$.

$f_{10}=(11,14,15,17,19,12)$.

$f_{11}=(16,18,19,17)$.

The black-vertex incidence lists and local potentials are:

$b=0$ has incident faces $(0,1,2)$; no state potential at the root is needed.

$b=2$ has incident faces $(0,3,4)$ and potentials $(0,-1,0)$ in that order.

$b=4$ has incident faces $(0,5,6)$ and potentials $(0,2,3)$ in that order.

$b=7$ has incident faces $(2,6,8)$ and potentials $(0,-1,-1)$ in that order.

$b=9$ has incident faces $(2,7,9)$ and potentials $(0,1,0)$ in that order.

$b=11$ has incident faces $(4,5,10)$ and potentials $(0,1,0)$ in that order.

$b=13$ has incident faces $(5,8,9)$ and potentials $(0,0,0)$ in that order.

$b=15$ has incident faces $(1,3,10)$ and potentials $(0,1,1)$ in that order.

$b=16$ has incident faces $(1,7,11)$ and potentials $(0,0,0)$ in that order.

$b=19$ has incident faces $(9,10,11)$ and potentials $(0,0,0)$ in that order.

Every state is listed below as the tuple of assigned face indices in the displayed order of $A$. Its $Q$ list uses the enumerated edges, and $c_s$ is the sum of signs over its partners.

$s_{0}=(3,5,6,7,4,8,10,11,9)$, $Q_{s_0}=\{e_{4},e_{5},e_{9},e_{13},e_{14},e_{16},e_{20},e_{22},e_{28}\}$, $c_{s_0}=-1$.

$s_{1}=(3,5,6,9,4,8,10,7,11)$, $Q_{s_1}=\{e_{4},e_{5},e_{9},e_{12},e_{14},e_{20},e_{22},e_{23},e_{26}\}$, $c_{s_1}=0$.

$s_{2}=(3,6,8,7,4,5,10,11,9)$, $Q_{s_2}=\{e_{4},e_{5},e_{7},e_{11},e_{13},e_{16},e_{17},e_{20},e_{28}\}$, $c_{s_2}=1$.

$s_{3}=(3,6,8,9,4,5,10,7,11)$, $Q_{s_3}=\{e_{4},e_{5},e_{7},e_{11},e_{12},e_{17},e_{20},e_{23},e_{26}\}$, $c_{s_3}=-1$.

$s_{4}=(4,5,6,7,10,8,3,11,9)$, $Q_{s_4}=\{e_{3},e_{8},e_{9},e_{13},e_{14},e_{16},e_{22},e_{25},e_{28}\}$, $c_{s_4}=1$.

$s_{5}=(4,5,6,9,10,8,3,7,11)$, $Q_{s_5}=\{e_{3},e_{8},e_{9},e_{12},e_{14},e_{22},e_{23},e_{25},e_{26}\}$, $c_{s_5}=-1$.

$s_{6}=(4,6,8,7,5,9,3,11,10)$, $Q_{s_6}=\{e_{3},e_{7},e_{11},e_{13},e_{16},e_{19},e_{21},e_{25},e_{29}\}$, $c_{s_6}=1$.

$s_{7}=(4,6,8,7,10,5,3,11,9)$, $Q_{s_7}=\{e_{3},e_{7},e_{8},e_{11},e_{13},e_{16},e_{17},e_{25},e_{28}\}$, $c_{s_7}=-1$.

$s_{8}=(4,6,8,9,10,5,3,7,11)$, $Q_{s_8}=\{e_{3},e_{7},e_{8},e_{11},e_{12},e_{17},e_{23},e_{25},e_{26}\}$, $c_{s_8}=1$.

Every ordered pair follows, including all of its directed face circuits, cut sides, four-count data and slopes. A tuple of faces gives the cyclic order. Its crossed edges are listed in the same order. In the count tuple the entries are $|S|,|B\cap S|,|E_S|,|U_S|,h,\ell$.

Pair $(s_{0},s_{8})$ has sign $1$.

Faces $(9,11,7)$; edges $(e_{29},e_{27},e_{18})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(8,5,6)$; edges $(e_{19},e_{10},e_{15})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(10,3,4)$; edges $(e_{24},e_{6},e_{21})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Pair $(s_{1},s_{6})$ has sign $1$.

Faces $(3,4,5,6,8,9,7,11,10)$; edges $(e_{6},e_{8},e_{10},e_{15},e_{17},e_{18},e_{27},e_{28},e_{24})$; cut side $S=\{10,11,12,13,14,18,19\}$. Counts $(7,3,15,9,9,3)$; delta-sum $-3$; slope $4$.

Pair $(s_{1},s_{7})$ has sign $-1$.

Faces $(9,7,11)$; edges $(e_{18},e_{27},e_{29})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(8,5,6)$; edges $(e_{19},e_{10},e_{15})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(10,3,4)$; edges $(e_{24},e_{6},e_{21})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Pair $(s_{2},s_{5})$ has sign $-1$.

Faces $(9,11,7)$; edges $(e_{29},e_{27},e_{18})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(8,6,5)$; edges $(e_{15},e_{10},e_{19})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(10,3,4)$; edges $(e_{24},e_{6},e_{21})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Pair $(s_{3},s_{4})$ has sign $1$.

Faces $(9,7,11)$; edges $(e_{18},e_{27},e_{29})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(8,6,5)$; edges $(e_{15},e_{10},e_{19})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(10,3,4)$; edges $(e_{24},e_{6},e_{21})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Pair $(s_{4},s_{3})$ has sign $-1$.

Faces $(9,11,7)$; edges $(e_{29},e_{27},e_{18})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(8,5,6)$; edges $(e_{19},e_{10},e_{15})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(10,4,3)$; edges $(e_{21},e_{6},e_{24})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Pair $(s_{5},s_{2})$ has sign $1$.

Faces $(9,7,11)$; edges $(e_{18},e_{27},e_{29})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(8,5,6)$; edges $(e_{19},e_{10},e_{15})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(10,4,3)$; edges $(e_{21},e_{6},e_{24})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Pair $(s_{6},s_{1})$ has sign $-1$.

Faces $(3,10,11,7,9,8,6,5,4)$; edges $(e_{24},e_{28},e_{27},e_{18},e_{17},e_{15},e_{10},e_{8},e_{6})$; cut side $S=\{10,11,12,13,14,18,19\}$. Counts $(7,3,15,9,9,3)$; delta-sum $3$; slope $-4$.

Pair $(s_{7},s_{1})$ has sign $1$.

Faces $(9,11,7)$; edges $(e_{29},e_{27},e_{18})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(8,6,5)$; edges $(e_{15},e_{10},e_{19})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(10,4,3)$; edges $(e_{21},e_{6},e_{24})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Pair $(s_{8},s_{0})$ has sign $-1$.

Faces $(9,7,11)$; edges $(e_{18},e_{27},e_{29})$; cut side $S=\{18\}$. Counts $(1,0,3,3,3,0)$; delta-sum $-3$; slope $1$.

Faces $(8,6,5)$; edges $(e_{15},e_{10},e_{19})$; cut side $S=\{10\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

Faces $(10,4,3)$; edges $(e_{21},e_{6},e_{24})$; cut side $S=\{14\}$. Counts $(1,0,3,3,3,0)$; delta-sum $3$; slope $-1$.

The exact polynomial is

$$
Z(z)=4z+9z^2-2z^3-9z^4-2z^5.
$$

The cancelling second state is $s_{1}$. Its two partners are $s_{6}$ with sign $-1$ and $s_{7}$ with sign $1$. The fixed circuit of $Q_s$ is the face sequence $(5,9,10)$. Reversing its tails interchanges exactly these partners. Their entire state-weight polynomials cancel, not merely their constant terms.

This cancellation circuit crosses $(e_{22},e_{23},e_{20})$ and has cut side $S=\{12\}$. Its four-count tuple is $(1,0,3,3,3,0)$, so its odd length is visible directly in G.

For recovery choose $s_{0}$. The removed edge set is $\{e_{1},e_{2},e_{4},e_{5},e_{9},e_{13},e_{14},e_{16},e_{20},e_{22},e_{28}\}$.

The recovery tree has edges $\{e_{0},e_{3},e_{6},e_{7},e_{8},e_{10},e_{11},e_{12},e_{15},e_{17},e_{18},e_{19},e_{21},e_{23},e_{24},e_{25},e_{26},e_{27},e_{29}\}$.

The selected perfect matching is $P=\{e_{0},e_{6},e_{8},e_{10},e_{11},e_{12},e_{17},e_{23},e_{25},e_{27}\}$.

Its complementary Hamiltonian cycle, in cyclic vertex order, is $(17,16,6,0,5,4,3,2,1,15,14,11,12,13,10,7,8,9,18,19)$. It avoids the prescribed edge.

