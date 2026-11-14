# 07. Recovery: from a forest pair to the Hamiltonian cycle

## What we want at this point and why

Step 06 produced a pair $(r,s)$ whose opposite-edge graph $Q_s$ is a forest. That is a statement about $n$ edges opposite chosen corners. The theorem asks for a Hamiltonian cycle of $G$ that avoids the edge dual to $e_0$, or equally for two induced trees of $T$ with $e_0$ inside one of them. This step is the translation. It is a chain of six links, and each link is either a planar duality or a count.

$$\text{forest pair} \to \text{incidence tree} \to \text{white-face tree} \to \text{selected edges } P \to P \text{ is a forest} \to \text{one cycle in } G \to \text{two induced trees}.$$

## The idea in plain words

A state removes one spoke from every black face. If what remains of the spoke graph is a tree, then by planar duality the removed spokes, seen from the faces of the spoke graph, also form a tree. The faces of the spoke graph are the white triangles. So we get a tree on the white faces.

A rooted tree is the same as a way to give every non-root node its own edge, the edge to its parent. Here that gives every white face one black face, across one edge of $T$. Select those edges. Every face of $T$, black or white, now has exactly one selected edge. In $G$ this is a perfect matching, and by step 01 its complement is a 2-factor. The disk identity shows that the selected edges contain no cycle, and by duality that means the 2-factor is connected.

## The six links

Fix a pair $(r,s)$ with $Q_s$ a forest, the outer face $t_0$, an edge $e_0$ of $t_0$, and let $y_0$ be the white face on the other side of $e_0$.

### Link 1. The incidence tree

By Lemma 1 of step 03, the partner $r$ forces every component of the forest $Q_s$ to contain exactly one root. Hence $H - s$ is a spanning tree of the spoke graph $H$. This is the last time the partner is needed. From here on only $s$ is used.

*Why.* $H - s$ consists of the edges of $Q_s$, each subdivided by the centre of its black face, plus the three spokes of $t_0$. A forest with three components, one root in each, becomes a tree when the three roots are joined to one new vertex.

### Link 2. The white-face tree

The faces of $H$ are in bijection with the white faces of $T$. The spokes cut each black triangle into three sectors, one along each side, and each sector merges with the white triangle across that side when the edges of $T$ are erased.

By tree/cotree duality (Lemma 3 of step 02, applied to the plane graph $H$) the duals of the removed spokes form a spanning tree $W_s$ on the white faces. The removed spoke $(t, s(t))$ separates the two sectors of $t$ at the corner $s(t)$. So its dual edge joins the two white faces that lie across the two sides of $t$ at $s(t)$. $W_s$ has $n+1$ nodes and $n$ edges, one for each face of $A$.

### Link 3. The selected edges

Root $W_s$ at $y_0$. Every white face $y \neq y_0$ has a parent, and the edge to the parent is the dual of a spoke $(t, s(t))$ for a unique $t$. This gives a bijection between the white faces other than $y_0$ and the faces of $A$. For each such $y$ select the side of $t$ that borders $y$. It is one of the two sides of $t$ at $s(t)$. Finally select $e_0$, which lies between $t_0$ and $y_0$.

Call the selected set $P$ and put $P_0 = P \setminus \{e_0\}$. By construction every black face and every white face contains exactly one selected edge. So $|P| = n + 1$. The edge of $P_0$ in $t$ is incident with $s(t)$.

### Link 4. $P$ is a forest

**Lemma** (OpenAI Lemma 6.2; trees paper Lemma 7.1). $P$ has no cycle and has exactly two components.

*Proof.* Direct each edge of $P_0$ away from $s(t)$, where $t$ is the black face that contains it. Every non-root is $s(t)$ for one $t$, so it has out-degree one, and roots have out-degree zero.

Suppose $P_0$ has a cycle $C$. With out-degree at most one everywhere it is a directed cycle. Its edges leave corners chosen by the state $s$, so the disk identity of step 04 applies. The disk has $W = B + 1$ and $h - 2\ell = 3$, with $h$ the length and $\ell$ the number of edges of $C$ whose black face is inside.

Now count the faces of the disk through $P$. Each face has one selected edge and each edge lies in one black and one white face, so $P$ pairs black faces with white faces. A face of the disk is paired with a face of the disk unless its selected edge is on $C$. All $h$ edges of $C$ are selected. They use up $\ell$ black faces and $h - \ell$ white faces of the disk. The remaining faces pair off inside, so $B - \ell = W - (h - \ell)$, that is $W - B = h - 2\ell = 3$. But $W - B = 1$. So $P_0$ is a forest.

In a forest with out-degree one at non-roots and zero at roots, every component contains exactly one root, by the count of Lemma 1 in step 03. So $P_0$ has three components. The edge $e_0$ joins two different roots, hence two components. Adding it keeps the graph acyclic and leaves two components. $\square$

The assumptions used are that $s$ is a bijection, for the disk identity, and that each face has exactly one selected edge. The two-line form of the argument is Lemma 6 of `research/2026-11-14_fable_route-combinatorics/PROOF.md`. Its referee asked for the last paragraph to be added, since the short form proved the statement for $P_0$ only. Proved in this project and checked by a second model, not yet read by a human. The published proofs reach $2\ell - h = 0$ and contradict the oddness of $h$.

### Link 5. One cycle in $G$

Take the edges of $G$ dual to the edges of $T$ that are not in $P$. Every face of $T$ has two unselected sides, so this subgraph has degree two at every vertex of $G$. $P$ is a spanning forest of $T$, so by tree/cotree duality the duals of the remaining edges are connected. A connected graph with all degrees two is a single cycle through all vertices. It does not use the dual of $e_0$, because $e_0 \in P$.

### Link 6. Two induced trees

Apply Theorem 4 of step 02 to this Hamiltonian cycle. The two sides of the cycle split $V(T)$ into two sets, each inducing a tree, and the edges with both ends on one side are exactly those of $P$. So the two trees are the two components of $P$. Inside $t_0$ the only edge of $P$ is $e_0$. Its ends are in one set and the third root is in the other. This is Theorem 2.2 of the OpenAI paper for rooted triangulations that have a pair.

## Worked example: the cube

Octahedron, $t_0 = (0,2,1)$, $e_0 = 01$, state $s = (3,4,5)$ on the faces $4 = (1,3,5)$, $5 = (2,4,3)$, $6 = (0,5,4)$. The white faces are $1 = (0,1,5)$, $2 = (1,2,3)$, $3 = (2,0,4)$, $7 = (3,4,5)$, and $y_0 = 1$.

| Black face | $s(t)$ | Sides at $s(t)$ | White faces across them | Edge of $W_s$ |
| --- | --- | --- | --- | --- |
| 4 | 3 | $13$, $35$ | 2, 7 | $2 - 7$ |
| 5 | 4 | $24$, $43$ | 3, 7 | $3 - 7$ |
| 6 | 5 | $05$, $54$ | 1, 7 | $1 - 7$ |

$W_s$ is a star with centre 7. Rooted at $y_0 = 1$, face 7 has parent 1 through black face 6, and faces 2 and 3 have parent 7 through black faces 4 and 5.

| White face | Its black face | Selected side |
| --- | --- | --- |
| 7 | 6 | the side of $(0,5,4)$ bordering $(3,4,5)$, which is $45$ |
| 2 | 4 | the side of $(1,3,5)$ bordering $(1,2,3)$, which is $13$ |
| 3 | 5 | the side of $(2,4,3)$ bordering $(2,0,4)$, which is $24$ |
| 1 | $t_0$ | $e_0 = 01$ |

So $P = \{01, 13, 24, 45\}$, the two paths $0 - 1 - 3$ and $2 - 4 - 5$ of step 02. The eight unselected edges give the cycle of faces $0, 3, 6, 1, 4, 7, 5, 2$ in the cube.

![The whole construction on the cube](../../paper/figures/renders/01-cube.png)

## Worked example: the running graph

Use the tree matching $s = (6, 2, 8, 1, 3, 10, 11, 7, 12, 9)$. It is the state drawn as $r$ in the figures, the partner of the state $s^*$ whose $Q$ has a cycle. With $e_0 = 04$ the white root is $y_0 = 3$. The script returns

$$P = \{02,\ 04,\ 06,\ 19,\ 39,\ 5\,11,\ 67,\ 78,\ 9\,10,\ 10\,11,\ 11\,12\},$$

eleven edges, one in each of the 22 faces. Its two components are $\{0, 2, 4, 6, 7, 8\}$ and $\{1, 3, 5, 9, 10, 11, 12\}$. The Hamiltonian cycle visits the 22 faces in the order

$$0, 1, 9, 10, 2, 3, 11, 12, 13, 14, 4, 5, 15, 16, 17, 18, 19, 20, 21, 8, 7, 6.$$

![The white-face tree](../../paper/figures/renders/12-tree-cotree.png)

![The selected edges and the cycle](../../paper/figures/renders/13-selected.png)

## Which Hamiltonian cycles are produced

The construction is a map from tree matchings to Hamiltonian cycles avoiding the dual of $e_0$. Three facts describe it.

1. **It is injective.** Given the cycle, recover $P$, remove $e_0$, direct the three trees towards their roots, and read off the tails. This returns $s$. That is the derivation at the start of step 03 run backwards.
2. **Its image is known.** Every Hamiltonian cycle $C$ avoiding the dual of $e_0$ defines a state $s_C$ in that way. $C$ is produced by the construction exactly when $s_C$ is a tree matching. If it is not, $s_C$ has no partner at all.
3. **It is not onto.** In the prism with $t_0 = (6,0,1)$ and $e_0 = 01$, four Hamiltonian cycles avoid the dual of $e_0$ and there are two tree matchings. For the other two choices of $e_0$ the numbers are two and two.

A consequence of the first fact is $3 \cdot \#\{\text{tree matchings}\} \le \#\{\text{Hamiltonian cycles of } G\}$, since each cycle avoids exactly one of the three edges at the vertex of $G$ in $t_0$.

In the running example $G$ has 28 Hamiltonian cycles. Six avoid the dual of $e_0 = 04$, and there are six tree matchings. So here every avoiding cycle is produced. Over all rooted triangulations with a pair and at most 16 vertices the number of avoiding cycles is between 1 and 26 times the number of tree matchings.

Status. Facts 1 and 2 are Proposition 7 of `fable_route-combinatorics/PROOF.md`, Theorem 7.2 of `research/2026-11-14_opus_route-graph-theory/PROOFS.md` and a section of `research/2026-11-14_astra_limits/HYPOTHESES.md`, found independently three times. Two different second models checked them, in `research/2026-11-14_astra_referee-combinatorics/` and in section 5 of `research/2026-11-14_sol_referee-structure/INTEGRATION.md`. Not yet read by a human. Fact 3 is computed, by three programs, mine included.

The reading that matters for intuition is this. Proposition 5.1 does not find an arbitrary Hamiltonian cycle. It finds one of a special kind, one whose state has a partner, and that kind depends on the root $t_0$. A proof that tried to show that every Hamiltonian cycle comes from a forest pair would be aiming at a false statement.

## What does not work

- **A state whose $Q_s$ is a forest but which has no partner.** The third state of the prism in step 03 has two roots in one component of $Q_s$ and none in another. Then $H - s$ is not connected, $W_s$ has a cycle, and Link 3 has nothing to root.
- **A choice of corners that is not a bijection.** Links 1 to 3 go through for any choice of one corner per face whose opposite edges form a rooted forest, and such choices are easy to find, see step 03. Link 4 breaks, because the disk identity needs the bijection. This is the reason the proof insists on states.
- **Other surfaces.** On a torus the complement of a spanning tree has two edges too many to be a tree, so Link 2 fails, and the two-tree target of Link 6 is impossible by the count in step 02.

## Other routes

- **Li's Link 4.** Li does not show that $P$ is a forest. He assumes that the complement of $P$ in $G$ has more than one cycle, takes one with no root face inside, and finds two faces matched to the same black vertex. That uses neither the disk identity nor the partner, and it does not produce the induced trees, which he does not need. Published.
- **Entirely in $G$.** The Lean formalisation does the recovery in the cubic graph with no spoke graph. Formalised.
- **Through Temperley's correspondence.** The papers point to the bijection between spanning trees and matchings of Kenyon, Propp and Wilson as a relative of Links 1 to 3. Nobody in the project wrote out an exact dictionary. A hunch.
- **By removing leaves.** Remove a leaf of $W_s$ together with its black face and show that a smaller rooted triangulation with a tree matching remains. A conjecture in `research/2026-11-14_fable_dependency-graph/skeleton.md`, edge F1, untested.

## Where this is used next

The theorem is now proved for every rooted triangulation that has a pair. Step 08 removes that assumption by cutting along separating triangles.
