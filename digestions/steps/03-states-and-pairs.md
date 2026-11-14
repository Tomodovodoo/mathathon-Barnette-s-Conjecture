# 03. States, pairs, and when a pair exists

Where this step lives elsewhere. Paper: Lemma 3.1, Definitions 3.2 and 3.4, Lemma 3.5, Definition 4.1, Lemma 4.2 and Section 5 (condition (5.1), Proposition 5.2, Figure 12) of [`barnette.pdf`](../../paper/main/barnette.pdf). Primal note: Lemma 4 and the rows "Incidences A to X", "Two disjoint states" and "Edge not on s(b)" of [`DICTIONARY.md`](../../proofs/primal/DICTIONARY.md). Blueprint nodes `lem:selections-give-states`, `def:state`, `def:good`, `lem:good`, `def:pair`, `lem:partner`, `eq:hall`, `prop:pair` in [`BLUEPRINT.md`](../../proofs/blueprint/BLUEPRINT.md); the definitions of state and pair and the flow step have exact Lean counterparts. Atlas: page 2, [two states from one count](../atlas/pages/02-pairs.pdf); page 15, [the lattice of covers](../atlas/pages/15-pairlattice.pdf); page 17, [three conditions](../atlas/pages/17-matroids.pdf); page 19, [rainbow trees](../atlas/pages/19-rainbow.pdf).

Review status, 14 November 2026. The paper's version of this step was refereed by a second AI model (verdict: the proof follows). The sharper criterion of Theorem 2 below was proved in this project and confirmed by a second model in `research/2026-11-14_sol_referee-structure/INTEGRATION.md`. No human has read either.

## What we want at this point and why

Step 02 turned the problem into finding two induced trees in the triangulation $T$, with a prescribed edge $e_0$ of the outer black face $t_0$ inside one of them. We now want a finite object to search for that encodes such a pair of trees. That object is a state. This step explains why states are the right object, why the proof needs two of them at once, and exactly when two exist.

Notation from step 02. $R$ is the set of three roots, $A$ the black faces other than $t_0$, $X$ the non-root vertices, and $|A| = |X| = n$.

## Why match black triangles to vertices

Start from the answer and look at its shadow. Suppose we had the two induced trees. Their edges form a set $P$ with one edge in every face, and $e_0 \in P$. Remove $e_0$. The tree that contained it falls into two pieces, so $P_0 = P \setminus \{e_0\}$ is a forest with three components, and each component contains exactly one root. Direct every edge of $P_0$ towards the root of its component. Then every non-root vertex is the tail of exactly one edge.

Each edge of $P_0$ lies in exactly one black face, and that face is in $A$, because the only edge of $P$ in $t_0$ is $e_0$. Each face of $A$ contains exactly one edge of $P_0$. So

$$t \ \longmapsto\ \text{the tail of the edge of } P_0 \text{ in } t$$

is a bijection from $A$ to $X$ that sends each black face to one of its own corners. The two trees leave behind a perfect matching between black faces and vertices. So a search for the trees can be organised as a search over such matchings.

This derivation is now Lemma 3.1 of the paper, which uses it to motivate states before defining them. It was found in this project three times (`fable_route-combinatorics/PROOF.md` Proposition 7, `opus_route-graph-theory/PROOFS.md` Theorem 7.2, `astra_limits`), and checked by two second models. The three source papers go in the other direction only, from the matching to the trees. The state read off a Hamiltonian cycle need not be good; step 07 says which cycles the proof can return.

## Definitions

**State.** A bijection $s : A \to X$ with $s(t)$ a corner of $t$ for every $t$. Equivalently, a perfect matching of the bipartite incidence graph $\mathcal B$ whose two sides are $A$ and $X$ and whose edges are the pairs $(t, v)$ with $v$ a corner of $t$. These are the Tutte states of trinity theory. Li calls them perfect matchings of $H$, the trees paper perfect matchings of $B$. In these digestions $H$ is the spoke graph below and $B$ is the number of black faces in a disk (step 04), so the incidence graph gets the main paper's letter $\mathcal B$.

**Opposite edges.** For a state $s$, $Q_s$ is the graph on all of $V(T)$ whose edges are the side of $t$ opposite $s(t)$, one for each $t \in A$. These $n$ edges are distinct, since an edge has only one black face.

**Good state** (paper Definition 3.4). A state $s$ such that $Q_s$ is a forest in which each component contains exactly one root. The trees paper and earlier versions of these digestions say *tree matching*; the OpenAI paper has no name and speaks of a pair with $Q_s$ a forest.

Write $e_0 = ab$ and let $o$ be the third root. The paper packages the condition in one spanning tree (Lemma 3.5). Put $S_s = Q_s \cup \{ao, bo\}$, the $n+2$ edges that any selection built from $s$ must avoid: in each $t \in A$ the side opposite $s(t)$, and in $t_0$ the two sides other than $e_0$. Then

$$s \text{ is good} \iff S_s \text{ is a spanning tree of } T.$$

Indeed $S_s$ has $|V(T)| - 1$ edges, so it is a spanning tree exactly when it is acyclic, and adding $ao$ and $bo$ to the forest $Q_s$ closes no cycle exactly when $a$, $b$, $o$ lie in three different components. A forest with $n$ edges on $n+3$ vertices has three components, so that means one root in each. Step 07 dualises this tree into a tree on the faces.

The older formulation uses the spoke graph $H$: a centre in every black face, $t_0$ included, joined to its three corners. A state is a set of $n$ spokes, and $s$ is good exactly when $H$ minus those spokes is a tree (the trees paper's (3)). The two are the same picture. Deleting the spoke $(t,s(t))$ leaves the centre of $t$ as a subdivision point on the edge of $Q_s$, and the centre of $t_0$ plays the role of the two edges $ao$, $bo$. The paper no longer needs spokes, and these digestions use $S_s$.

**Pair.** Two states $r, s$ with $r(t) \neq s(t)$ for every $t \in A$. We also say that $r$ is a partner of $s$. The trees paper says mate. For a pair, $u(t)$ denotes the third corner of $t$.

![A state as a matching, and a second disjoint state](img/paper-05-state.png)

The edge of Q_s is opposite s(t); the edge of D is incident with s(t). They are different edges of the same triangle. Reversing Q_s changes r only, while reversing D changes both states.

## Why a second state

A single state does not tell you much about $Q_s$. A partner does three jobs.

**It orients $Q_s$.** The edge of $Q_s$ in $t$ joins the two corners other than $s(t)$, which are $r(t)$ and $u(t)$. Direct it from $r(t)$ to $u(t)$. Since $r$ is a bijection onto $X$, every non-root is the tail of exactly one edge and no root is a tail.

**Lemma 1** (paper Lemma 4.2; trees paper, Proposition 2.1; the first half is OpenAI Lemma 6.1). Let $s$ be a state with a partner. Every component of $Q_s$ is a tree containing exactly one root, or contains no root and exactly one cycle. If there are $q(s)$ components of the second kind, $s$ has exactly $2^{q(s)}$ partners. (The trees paper writes $k$; here $k$ is reserved for the number of black faces.)

*Proof.* Take a component with $v$ vertices of which $a$ are roots. Its edges number $v - a$, one per tail. A connected graph has at least $v - 1$ edges, so $a \le 1$. If $a = 1$ it has $v - 1$ edges and is a tree, and all edges point to the root. If $a = 0$ it has $v$ edges, hence one cycle. The cycle runs one of two ways and everything else points to it. Conversely any such orientation gives a partner by reading off the tails, and the two directions of each cycle are free choices. $\square$

So with a partner, "$Q_s$ is a forest" already implies "one root per component", and only then may "forest" stand for the whole condition. Without a partner it may not: the third state of the prism below has a forest $Q_s$ and is not good. A good state is exactly a state with one partner.

**It gives something to move.** If $Q_s$ has a cycle, the cycle can be run the other way, and that changes $r$ without touching $s$. Step 05 uses this to cancel.

**It gives something to count.** The directed edges $r(t) \to s(t)$ form disjoint cycles through all of $X$. Step 06 groups pairs by these cycles.

## When does a pair exist

**Theorem 2** (trees paper, Theorem 1.2, (ii) $\Leftrightarrow$ (iii). OpenAI Proposition 3.1, paper Proposition 5.2 and Li Lemma 9 prove the "if" direction when there is no separating triangle at all). A pair exists if and only if no separating triangle of $T$ has black inner boundary.

A separating triangle is a 3-cycle of $T$ with vertices on both sides. Its inner side is the side away from $t_0$. It has black inner boundary if the three faces on the inner side that touch its edges are black.

The proof has two parts.

### Part 1, from pairs to a counting condition

Two disjoint perfect matchings of $\mathcal B$ together form a subgraph with degree two everywhere. Conversely such a subgraph is a union of even cycles, and taking alternate edges splits it into two disjoint perfect matchings. So we want a 2-factor of the incidence graph $\mathcal B$. (A 2-factor of $\mathcal B$ is not a 2-factor of $G$; step 01 uses the word for $G$.)

Set up a flow. A source sends capacity 2 to each vertex of $X$, each incidence $(t,v)$ carries capacity 1, and each face of $A$ sends capacity 2 to a sink. A flow of value $2n$ with whole numbers is a 2-factor. By the max-flow min-cut theorem with integral capacities (Ford and Fulkerson 1956) such a flow exists if and only if every cut has capacity at least $2n$, which works out to

$$\sum_{t \in A} \min\bigl(2,\ |V(t) \cap S|\bigr) \ \ge\ 2|S| \qquad \text{for every } S \subseteq X. \tag{1}$$

In words, any set $S$ of vertices needs $2|S|$ incidences, and each black face can give at most two, and no more than it has corners in $S$.

Rewrite (1) in terms of $U = V(T) \setminus S$, which contains the roots. A black face with $j$ corners in $U$ contributes $\min(2, 3-j) = 2 - \max(0, j-1)$. The number $\max(0, j-1)$ is the number of edges of that face inside $T[U]$, minus one if all three corners are in $U$. Every edge has one black face. With $e(U)$ the number of edges of $T[U]$ and $b(U)$ the number of black faces with all corners in $U$, condition (1) becomes

$$e(U) - b(U) \ \le\ 2|U| - 4 \qquad \text{for every } U \supseteq R. \tag{2}$$

### Part 2, the Euler identity

**Lemma 3** (Euler identity, `research/2026-11-14_opus_route-graph-theory/PROOFS.md`, Lemma 2.2. Proved in this project and checked by a second model, whose restatement is section 1 of `research/2026-11-14_sol_referee-structure/INTEGRATION.md`. Not yet read by a human.) Let $K$ be a connected induced subgraph of $T$ with $p \ge 3$ vertices and $m$ edges. Some faces of the plane graph $K$ are faces of $T$. Call the others regions. Let $b$ be the number of black faces of $T$ that are faces of $K$. For a region $F_i$ let $d_i$ be the length of its boundary and $\beta_i$ the number of black faces of $T$ inside it minus the number of white ones. Then

$$m - b - (2p - 4) \ =\ \tfrac12 \sum_i \bigl(\beta_i - (d_i - 4)\bigr).$$

*Proof.* Let $w$ count the white faces of $T$ that are faces of $K$ and let $q$ be the number of regions. Euler gives $p - m + b + w + q = 2$. Counting edge sides gives $2m = 3b + 3w + \sum d_i$. Eliminate to get $m - b - (2p-4) = \tfrac12\bigl(w - b - \sum(d_i - 4)\bigr)$. Since $T$ has equally many black and white faces, $w - b = \sum \beta_i$. $\square$

The size of $\beta$ is controlled by a second count. Give each black face inside a region $+3$ and each white face $-3$ and spread these over their sides. Inner sides cancel in pairs. So $3\beta$ is a sum of $d$ signs, one per boundary side. Hence $\beta \equiv d \pmod 2$ and $|\beta| \le d/3$. For $d = 3$ this gives $\beta = \pm 1$, with $+1$ exactly when the three faces along the boundary are black. For $d \ge 4$ it gives $\beta \le d - 4$.

*Proof of Theorem 2.* If a separating triangle has black inner boundary, let $U$ be everything not strictly inside it. Then $T[U]$ has a single region, with $d = 3$ and $\beta = 1$, and Lemma 3 gives $e(U) - b(U) = 2|U| - 4 + 1$. So (2) fails by exactly one.

If no separating triangle has black inner boundary, take any $U \supseteq R$ and apply Lemma 3 to each component of $T[U]$. In the component of the roots, a region of length at least 4 contributes at most 0. A region of length 3 is the inner side of a separating triangle, which has $\beta = -1$ by assumption, and contributes 0. So that component satisfies $m - b \le 2p - 4$. If it has only three vertices it is $t_0$ itself, with $m - b = 3 - 1 = 2$, and the bound holds with equality. Any other component with at least four vertices has one region that contains $t_0$ and may contribute $1$, and so satisfies $m - b \le 2p - 3 \le 2p$. Smaller components have at most three edges, so $m - b \le 2p$ there too. Summing over the components gives (2). $\square$

How this compares with the paper. The paper proves only the case with no separating triangle, and its proof is the same count organised per component. It shows $\mathrm{bal}(\Psi) \le d_\Psi - 4$ for every face $\Psi$ of length at least 4 of $T[U]$ (length 4 forces balance 0, length 5 forces $\pm 3$, and $|\mathrm{bal}| \le d/3$ in general), and uses the hypothesis once, to say that a face of length 3 is a face of $T$. Lemma 3 above isolates exactly what the faces of length 3 contribute, which is why it gives the sharp criterion. In the running example (5.1) is tight already for $S = \{2\}$, a vertex in only two black faces (paper Figure 12; recomputed).

Computed check. The criterion agrees with a direct flow computation on all 7,868 rooted triangulations with at most 16 vertices (`opus_route-graph-theory`, and independently on 1,206 rooted cases up to 14 vertices in `astra_limits`).

## Worked examples

**Octahedron.** $A$ is faces $4 = (1,3,5)$, $5 = (2,4,3)$, $6 = (0,5,4)$ and $X = \{3,4,5\}$. The incidence matrix with rows $4,5,6$ and columns $3,4,5$ is

$$\begin{pmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & 1 & 1 \end{pmatrix}.$$

It has two perfect matchings, the states $s_1 = (3,4,5)$ and $s_2 = (5,3,4)$, written as the images of faces $4,5,6$. They differ everywhere, so they form a pair in either order. $Q_{s_1}$ has the edges $15, 23, 04$ and $Q_{s_2}$ has $13, 24, 05$. Each is three single edges with one root each. Both states are good.

**Prism.** $T$ is the double wheel with apexes $6, 7$ and rim $0,\dots,5$, and $t_0 = (6,0,1)$. There are three states. Two of them form a pair and are good states. The third sends the faces $(7,2,1), (6,2,3), (7,4,3), (6,4,5), (7,0,5)$ to $2, 3, 7, 4, 5$. Its opposite edges are $71, 62, 43, 65, 70$. That is a forest. Its components are $\{0,1,7\}$ with two roots, $\{2,5,6\}$ with one, and $\{3,4\}$ with none. It is not a good state and it has no partner. This is the smallest example showing that "forest" without a partner is not enough.

**Double octahedron.** Glue an octahedron with new vertices $6,7,8$ into the face $(3,4,5)$ of the octahedron. The triangle $3,4,5$ is now separating. Of the 14 possible outer faces, 8 give four states, four pairs and four good states. The other 6 give four states and no pair. For $t_0 = (0,1,5)$ the inner faces along the triangle are black, namely $(3,4,8), (4,5,6), (5,3,7)$, together with the central face $(6,7,8)$. Take $S = \{6,7,8\}$. These three vertices need $6$ incidences. The four black faces that touch them supply $1 + 1 + 1 + 2 = 5$. Condition (1) fails by one.

**Running example.** 13 vertices, $n = 10$, no separating triangle. There are 12 states and 8 pairs. Seven states have a partner. Six of them have one partner each and are good states. The seventh has two partners and a cycle in its $Q$. The figure shows the flow for one pair.

![The flow that supplies a pair](../../paper/figures/renders/06-flow.png)

## What does not work

- **One state.** The prism example above. Also, in the octahedron with every face split in four, 34 of the 54 states have an acyclic $Q_s$ and are not good states (`research/2026-11-14_fable_dependency-graph/correspondence.md`, note 3.5, computed).
- **Dropping the second bijection.** Keep $r$ a state and keep the choices distinct in each face, but drop the requirement that $s$ is a bijection. For any choice of one corner per face, the signed sum over states $r$ avoiding that choice is a determinant, and the sum over all choices is non-zero for an easy reason. It produces a choice function whose opposite edges form a rooted forest, but that function may use a vertex twice, and step 07 needs each vertex used once. So the whole difficulty is the second bijection. This is the side remark in section 4 of `fable_route-combinatorics/PROOF.md`, proved in this project and checked by a second model, not yet read by a human.
- **Graphs that are only 2-connected.** Then $T$ has parallel edges. On the 26-vertex non-Hamiltonian example every root has eight states and no pair, so the proof stops here and nowhere later (`astra_limits/HYPOTHESES.md`, computed in this project, not yet refereed).
- **Rooting anywhere.** Pairs depend on $t_0$. The double octahedron has them for 8 roots out of 14. This is why step 08 is needed.
- **Picking the pair from the lattice.** The pairs of a rooted triangulation form a distributive lattice (Felsner, see below), so there are canonical pairs: the top, the bottom, the join-irreducibles. None of them has to be good. The two extremes both fail on an 18-vertex triangulation with 20 pairs and 12 good states, and on a 33-vertex triangulation glued from two copies of it all ten extreme or irreducible candidates fail, while 144 of the 400 pairs are good. The 33-vertex example has separating triangles, so the separator-free case is untested. Distance from an extreme is also unbounded. Computed and replayed by two implementations in `research/2026-11-14_sol_referee-conjectures/` (a referee folder), no minimality claim.
- **Two matroids, or a linear program.** A state with $S_s$ a spanning tree is a common base of three structures: a matching of black faces to vertices, a matching of the same faces to white faces, and the graphic matroid. Any two are easy. Dropping the vertex matching gives the matroid intersection of the face partition and the white graphic matroid; on the hexagonal prism 4 of its 6 common bases are not states. The natural linear program has a half-integral vertex at 13 vertices. Both refuted by computation and checked by a second model (atlas pages [17](../atlas/pages/17-matroids.pdf) and [18](../atlas/pages/18-lp.pdf)).
- **Packing.** The edges $Q_r \cup Q_s$ of a pair always split into two spanning trees of $T$ with the roots identified (Nash-Williams plus the density inequality (2), proved in this project, not refereed). That is true and does not see which pair is good: inside one fixed pair support a good split can be missing, first at 16 vertices, and at 17 vertices 239 of 9,290 supports have none (`research/2026-11-14_opus_two-tree-packing/`, computed, unreviewed). The face-side packing P2 is open (step 09, door 6).

## Other routes to a pair

- **Li's route.** Take a smallest set $S$ violating (1) and show that it is cut off by three edges of $G$. Published. The audit in `fable_dependency-graph/correspondence.md`, note 3.7, observes that Li's argument already yields the black inner boundary.
- **Pairs as orientations.** A 2-factor of $\mathcal B$ is the same as an orientation of $H$ minus the centre of $t_0$ with prescribed out-degrees, so by a theorem of Felsner the 2-factors form a distributive lattice. Proved in `opus_route-graph-theory/PROOFS.md` section 3, not refereed; Felsner's theorem was cited there from memory. The lattice does not single out a good pair (see "What does not work").
- **Rainbow trees, Step R.** A spanning tree on the white faces that uses every black face exactly once as a link (a point-rainbow tree) exists if and only if no separating triangle has black inner boundary. The proof uses Rado's theorem and an Euler identity, with no signed count, and each such tree completes to exactly one 2-factor of $\mathcal B$, hence a pair. Proved in this project (`research/2026-11-14_fable_referee-topology/RAINBOW.md`), not yet refereed. Its companion, Step X, would turn a rainbow tree into a good state by exchanges; it is open (step 09, door 1). Atlas page [19](../atlas/pages/19-rainbow.pdf).
- **A construction without flows.** Unknown. The obstruction is always a single triangle, which suggests that an explicit ordering argument should exist, as it does for Schnyder woods. Nobody in the project found one.

## Where this is used next

Step 04 proves the counting lemma for cycles made of edges that leave the corners chosen by a state. Steps 05 and 06 assume that a pair exists and produce a pair whose second state is a good state.
