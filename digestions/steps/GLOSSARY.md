# Glossary

Every term and symbol used in the digestions, with the name each of the three papers gives it. "O" is the OpenAI paper, "L" is Li's note, "T" is the trees paper. The digestions follow the shared notation of `research/BRIEF.md`, which is close to O and T. The translation between the papers is taken from `research/2026-11-14_fable_dependency-graph/correspondence.md`, an audit made in this project and not refereed. Where I use a translation in a proof I rechecked it.

A warning first. The letter $H$ means the full spoke graph in O and T and the reduced incidence graph in L. Li's $H$ is our $B$.

## Graphs and the setting

| Term or symbol | Meaning | O | L | T |
| --- | --- | --- | --- | --- |
| Barnette graph, $G$ | a finite simple graph that is cubic, bipartite, planar and 3-connected | "a graph satisfying Theorem 1.1" | Barnette graph | cubic bipartite polyhedral graph |
| $N$ | number of vertices of $G$ | not named | not named | $N$ |
| 2-factor | a spanning subgraph with all degrees two | "spanning subgraph of degree two" | 2-factor, also used for two disjoint matchings of $H$ | same as O |
| $T = G^*$ | the dual of $G$, a simple triangulation of the sphere | sphere triangulation | not used. L works in $\mathrm{aux}(G)$, which is $T$ with a centre in every face | triangulation |
| black face, white face | the two colours of the triangles of $T$, coming from the two colours of the vertices of $G$ | black and white triangles | black vertex $b$, white vertex $w$ of $G$ | black and white faces |
| vertex of $T$ | a face of $G$ | vertex | face-vertex $f$ | vertex |
| Eulerian triangulation | a triangulation with all degrees even, equivalently one whose faces can be coloured in this way | not named | not used | "colouring exists iff all degrees are even" |
| $k$ | number of black faces, also the number of white faces | $k$ | not named | not named |
| $t_0$ | the chosen outer black face | $t_0$ | the black vertex $b_0$ | $t_0$ |
| $e_0$ | the prescribed edge of $t_0$. The Hamiltonian cycle avoids the edge of $G$ dual to it | $e_0$ | the edge $b_0 w_0$ of $G$ | $e_0$ |
| $y_0$ | the white face across $e_0$ from $t_0$ | $y_0$ | $w_0$ | $y_0$ |
| roots, $R$ | the three vertices of $t_0$ | roots | root face-vertices, $F(G) \cap N(b_0)$ | $R$ |
| $A$ | the black faces other than $t_0$ | $A$ | $B' $, the black vertices of Li's $H$ | $A$ |
| $X$ | the vertices of $T$ that are not roots | $X$ | $F'$ | $X$ |
| $n$ | $\lvert A\rvert = \lvert X\rvert = k - 1 = N/2 - 1$ | $k - 1$ | not named | $n$ |
| separating triangle | a 3-cycle of $T$ with vertices on both sides | separating triangle | non-trivial 3-edge cut of $G$ | separating triangle |
| black inner boundary | the three faces along a separating triangle on the side away from $t_0$ are black | not used | appears inside the proof of Lemma 9 without a name | black inner boundary |
| cap | the triangular face added to close one side after cutting along a separating triangle | "capping each side by a triangle" | the vertex $x$ of $G/X$ | cap |
| induced subgraph $T[U]$ | all edges of $T$ with both ends in $U$ | $T[U]$ | not used | induced tree |

## Incidence graphs

| Term or symbol | Meaning | O | L | T |
| --- | --- | --- | --- | --- |
| centre | a point inside a black face | center | the black vertex itself | center |
| spoke | the edge from the centre of a black face to one of its corners, written $(t,v)$ | incidence spoke | an edge of $G_{FB}$ | spoke |
| $H$ | the spoke graph, all centres including that of $t_0$ joined to their corners | $H$ in section 6.1 | $G_{FB}$ | $H$ |
| $H_0$ | $H$ without the centre of $t_0$ | $H_0$ in section 5.2 | not named | $H_0$ |
| $B$ | the incidence graph between $A$ and $X$ | "the bipartite incidence graph on $A$ and $X$" | $H = G_{FB} - N[b_0]$ | $B$ |
| $K_B$ | the $0/1$ matrix of $B$, rows $A$, columns $X$ | not used | not used | $K_B$ |
| $M$ | the number of states, equal to $\lvert\det K_B\rvert$ | not used | not used | $M$ |

## States and pairs

| Term or symbol | Meaning | O | L | T |
| --- | --- | --- | --- | --- |
| state | a bijection $s : A \to X$ with $s(t)$ a corner of $t$, that is a perfect matching of $B$ | state | perfect matching of $H$ | perfect matching of $B$ |
| pair $(r,s)$ | two states that differ in every face. $r$ is the first state, $s$ the second | pair | ordered 2-factor $(M_1, M_2)$ with $M_1 = r$, $M_2 = s$ | disjoint matching pair, element of $\mathcal P$ |
| partner | a state $r$ that forms a pair with $s$ | partner | not named | disjoint mate |
| $u(t)$ | the third corner of $t$, other than $r(t)$ and $s(t)$ | $u(t)$ | not named | $u(t)$ |
| $Q_s$ | the edges of $T$ opposite $s(t)$, one for each $t \in A$ | $Q_s$ | $H - M_2$, which is $Q_s$ with every edge subdivided and the roots removed | $Q_s$ |
| $k(s)$ | the number of cycles of $Q_s$. A state with a partner has $2^{k(s)}$ partners | not used | not used | $k$ in Proposition 2.1 |
| tree matching | a state $s$ such that $H - s$ is a spanning tree, equivalently $Q_s$ is a forest with one root in each component | not named. "$Q_s$ a forest" for a pair | cycle-breaking, for a pair | tree matching |
| forest pair | a pair $(r,s)$ with $Q_s$ a forest. Its second state is a tree matching | "a pair with $Q_s$ a forest" | cycle-breaking 2-factor | tree pair |
| $D(r,s)$ | the directed edges $r(t) \to s(t)$. They form disjoint cycles through all of $X$ | $D$ | the cycles of $H[M_1 \cup M_2]$ with the orientation $\mathrm{orient}(M_1, M_2)$, which runs the other way | $D_{r,s}$ |
| cycle cover | the set of undirected cycles of $D(r,s)$. The pairs with a given cover are its orientations | "group" | a 2-factor of $H$ | "group" |
| $c(D)$, $c_{\min}$, $m$ | the number of cycles of a cover, and the least such number over all pairs | $c(D)$, $c_{\min}$ | $c_{\min}$ | $c$, $m$ |
| exchange graph | pairs as nodes, joined when they differ by reversing one cycle of $D$ or one cycle of $Q_s$ | not used | not used | $\mathcal E$ |

## The disk identity

| Term or symbol | Meaning | O | L | T |
| --- | --- | --- | --- | --- |
| $\delta(v,w)$ | $+1$ if the black face on the edge $vw$ is on the left going from $v$ to $w$, else $-1$ | $\delta$ | the local turn $\tau(b) \in \{0,1\}$, with $\tau = (1 + \delta)/2$ | $\delta$ |
| state cycle | a simple directed cycle of edges, each leaving the corner chosen by a state in the black face that owns the edge | "simple directed cycle in the chosen edges" | a cycle of $H$ alternating between $M_1$ and other edges | same as O |
| $h$, $\ell$, $I$, $B$, $W$ | for the disk of a state cycle, its length, the number of its edges with the black face inside, the number of vertices strictly inside, and the numbers of black and white faces inside | $h, l, I, B, W$ | $\lvert C\rvert = 2h$, $t_{C,\mathrm{in}} = \ell$ | $h, l, I, B, W$ |
| disk identity | $W = B + 1$ and $h - 2\ell = 3$. The $\delta$-sum is $-3$ counterclockwise and $+3$ clockwise | Lemma 4.1 | Claim 25 | Lemma 4.1 |
| vertex colouring $c$ | the colouring of $V(T)$ by $\mathbb Z/3$ with $\delta(v,w) \equiv c(w) - c(v)$ | mentioned as not needed | not used | not used |

## Signs, weights and sums

| Term or symbol | Meaning | O | L | T |
| --- | --- | --- | --- | --- |
| $J(r,s)$ | $\tfrac13\sum_t \delta(r(t), s(t))$, equal to the number of clockwise cycles of $D$ minus the number of counterclockwise ones | $J$ | $-cw'$ | $J$ in (8) |
| sign of a pair, $\varepsilon(r,s)$ | $\prod_t \delta(r(t),s(t)) = (-1)^{(n+J)/2}$ | the phase $i^J = i^{-n}\varepsilon$ | $(-1)^{cw}$ with $cw = \lfloor cw'/2\rfloor \bmod 2$ | $\varepsilon$ |
| $\mu(s)$ | the sum of $\varepsilon(r,s)$ over the partners of $s$. It is $\pm 1$ for a tree matching and $0$ otherwise | not named | not named | not named |
| $a(t,v)$ | a weight on the spoke $(t,v)$ | real numbers from Lemma 5.3 | the signed number of white-vertex rays crossing the spoke | integers with $0 \le a \le 6n$ |
| $\omega(s)$ | $\sum_t a(t, s(t))$ | $\omega(s)$ | the number of available marks, with signs | $\omega(s)$ |
| $L^+(C)$, $L^-(C)$ | the sum of $a(t,\text{head})$ along a cycle of $D$ in its counterclockwise and clockwise orientation. The difference is positive | $L^+$, $L^-$ | not named | $L^+$, $L^-$ |
| spoke detour | the route from tail through the centre to head that replaces an edge of $D$ | "two-spoke route", the slide | not needed, cycles live on spokes from the start | spoke detour |
| inner white face | a white face that shares no edge with $t_0$ | a bounded face of $H_0$ | a white vertex not adjacent to $b_0$ | same as O |
| height $h_s(w)$ | the signed number of crossings of a fixed path from the inner white face $w$ to $t_0$ with the spokes of $s$ | not used | the crossings of the ray of $w$ with $M_2$ | not used |
| $\mathcal F(w)$ | the polynomial $\sum \varepsilon(r,s)\, w^s$ in one variable per spoke | not used | not used | not used. From this project |
| the signed sum | the sum over pairs that is evaluated in two ways | $Z(x) = \sum i^J e^{x\omega(s)}$ | $\lvert O^+\rvert - \lvert O^-\rvert$ | $Z_{\mathcal C}(z) = \sum \varepsilon z^{\omega(s)}$ on one exchange component |
| the two cancellations | reversing a cycle of $Q_s$, and reversing a cycle of $D$ | Lemma 5.2, and the factors of (5.4) | the involutions $\iota_1$ and $\iota_2$ | the moves (b) and (a), the involutions $\beta$ and $\alpha$ |
| marks, tokens | the objects Li and the trees paper attach to a pair to turn the weighted sum into a count | not used | marks $(w, e_2)$ | tokens $(t, j)$ |

## Recovery

| Term or symbol | Meaning | O | L | T |
| --- | --- | --- | --- | --- |
| incidence tree | the spanning tree $H - s$ of a tree matching | "the remainder" | $T_{FB} = G_{FB} - M_2$ | $H - s$ |
| white-face tree, $W_s$ | the tree on the white faces dual to the spokes of $s$ | "spanning tree on the white triangles" | $T_W = M_2^*$ | $W_s$ |
| selected edges, $P$ | one edge in every face of $T$, read in $G$ a perfect matching | $P \subset E(T)$ | the perfect matching $P$ of $G$ | $P$ |
| $P_0$ | $P$ without $e_0$ | $P_0$ | $\mathrm{trace}_B(P)$, moved onto spokes | not named |
| plain and mixed edges | for a partition of $V(T)$ into two classes, edges with both ends in one class, and the others. Words of these digestions | "same-label" edges | not used | not used |
| the two induced trees | the two components of $P$, also the two sides of the Hamiltonian cycle | Theorem 2.2 | not used | Lemma 7.1 |
| $s_C$ | the state read off a Hamiltonian cycle $C$ that avoids the dual of $e_0$ | not used | not used | not used. From this project |

## Names of results

| Result | O | L | T |
| --- | --- | --- | --- |
| Barnette's conjecture | Theorem 1.1 | Theorem 3 | Theorem 1.1 |
| two induced trees with a prescribed edge | Theorem 2.2 | not stated | Lemma 7.1 with section 7.3 |
| tree/cotree duality | Lemma 2.1 | used inside Corollary 27 | section 7.1 |
| a pair exists | Proposition 3.1 | Lemma 9 | Theorem 1.2, (ii) and (iii) |
| disk identity | Lemma 4.1 | Claim 25 | Lemma 4.1 |
| cancellation for a fixed second state | Lemma 5.2 | Lemma 17, $\iota_1$ | Lemma 4.2, move (b) |
| positive weights | Lemma 5.3 with (5.3) | Remark 19, Definition 20 | Lemma 5.1 |
| a forest pair exists | Proposition 5.1 | Lemma 7, the Key Lemma | Theorem 5.2 |
| one root per component | Lemma 6.1 | Lemma 8 | Proposition 2.1 with (3) |
| the selected edges form a forest | Lemma 6.2 | Lemma 30, by a different argument | Lemma 7.1 |
| gluing | section 7 | Appendix C | section 7.3 |
| avoiding an edge | Corollary 7.1 | Theorem 3 | Theorem 1.1 |
| only in one paper | Corollary 7.2 | the ray drawing | Theorems 1.2, 5.2, 5.3, Lemma 6.1, Proposition 6.2 |
