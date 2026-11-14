# Glossary

Every term and symbol of the digestions, one line each, with the names used elsewhere. Columns: "paper" is the project's exposition [`paper/main/barnette.tex`](../../paper/main/barnette.tex), whose names the digestions follow; "OpenAI" is `papers/OpenAI-Barnette.pdf`; "Li" is `papers/A-Note-On-Barnette.pdf`; "constructive" is the unsigned manuscript `papers/barnette_trees.pdf` (called "the trees paper" in older digestions); "Lean" is the declaration in OpenAI's Lean development (namespace `OAI.Barnette`, commit `4eaee875`) as listed in [`proofs/primal/DICTIONARY.md`](../../proofs/primal/DICTIONARY.md) and [`proofs/blueprint/BLUEPRINT.md`](../../proofs/blueprint/BLUEPRINT.md). A dash means no counterpart with that name. The Li and OpenAI columns come from `research/2026-11-14_fable_dependency-graph/correspondence.md`, an unrefereed audit; the Lean column was not checked against the Lean source here.

Two warnings. The letter $H$ is the spoke graph in OpenAI and the constructive paper but the incidence graph $\mathcal B$ in Li. Plain $B$ in the digestions is only the number of black faces inside a disk.

## The setting

| Term | Meaning | Paper | OpenAI | Li | Constructive | Lean |
| --- | --- | --- | --- | --- | --- | --- |
| Barnette graph $G$ | finite simple cubic bipartite planar 3-connected graph | "$G$ as in Theorem 1.1" | same | Barnette graph | cubic bipartite polyhedral graph | `main` |
| $N$ | number of vertices of $G$, $N = 2V - 4$ | $\lvert V(G)\rvert$ | - | - | $N$ | - |
| $T = G^*$, $V$ | the dual triangulation, and its number of vertices | $\T$, coloured triangulation | sphere triangulation | $\mathrm{aux}(G)$ adds face centres | triangulation | `ColoredDual` (algebraic dual) |
| black, white face | faces of $T$ coloured by the bipartition of $G$ | same | black, white triangles | black, white vertex of $G$ | same | `ColoredDual` colours |
| $k$ | number of black faces, also of white faces | $k$ | $k$ | - | - | `black_dual_card` |
| $t_0$ | the outer black face | $t_0$ | $t_0$ | $b_0$ | $t_0$ | state root |
| $e_0 = ab$ | prescribed side of $t_0$; the cycle avoids the edge of $G$ crossing it | $e_0$ | $e_0$ | edge $b_0 w_0$ | $e_0$ | - |
| $o$ | third corner of $t_0$ | $o$ | - | - | - | - |
| $y_0$ | white face across $e_0$ | $y_0$ | $y_0$ | $w_0$ | $y_0$ | - |
| roots $R$ | the corners $a, b, o$ of $t_0$ | roots | roots | root face-vertices | $R$ | root |
| $A$, $X$, $n$ | black faces other than $t_0$; non-root vertices; $n = \lvert A\rvert = \lvert X\rvert = k-1$ | same | same, $k-1$ | $B'$, $F'$ | same | `nonroots_card` |
| separating triangle | 3-cycle of $T$ with vertices on both sides | same | same | non-trivial 3-edge cut of $G$ | same | - |
| black inner boundary | the three faces inside a separating triangle along its sides are black | used in Section 7 | - | inside proof of Lemma 9 | black inner boundary | - |
| piece, cap | one closed side of a separating triangle, closed by a new face, the cap | piece, cap | capping | contracted shore $x$ | cap | `cap_duality`, `cap_glue_connected` |
| feasible root | a choice of $t_0$ that admits a pair | - | - | - | - | - |
| Eulerian triangulation | all degrees even, equivalently faces 2-colourable this way | coloured triangulation | - | - | same | - |

## Selections and the target

| Term | Meaning | Paper | OpenAI | Li | Constructive | Lean |
| --- | --- | --- | --- | --- | --- | --- |
| selection $P$ | set of edges of $T$ with exactly one side in every face; in $G$, a perfect matching | selection | "one selected edge per triangle" | perfect matching $P$ | $P$ | `selected_forest`, `connected_complement_matching` |
| acyclic selection | selection with no cycle; its complement in $G$ is a Hamiltonian cycle | same | - | connected complement | - | `connected_complement_matching` |
| $P_0$ | $P \setminus \{e_0\}$ | $P_0$ | $P_0$ | $\mathrm{trace}_B(P)$ | - | - |
| plain, mixed edges | for a split of $V(T)$, edges inside a class and between classes (digestion words) | - | "same-label" | - | - | - |
| two induced trees | the two components of an acyclic selection | Proposition 2.6(2) | Theorem 2.2 | - | Lemma 7.1 | not stated |
| tree/cotree duality | complement of a spanning tree dualises to a spanning tree; a cycle disconnects the dual | Lemma 2.5 | Lemma 2.1 | inside Corollary 27 | Section 7.1 | `circuit_cut`, `complement_connected` |
| connectivity lemma | a sphere graph whose faces are bounded by cycles is connected | Lemma 2.2 | tacit | - | - | `region_connected` |

## States and pairs

| Term | Meaning | Paper | OpenAI | Li | Constructive | Lean |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathcal B$ | bipartite incidence graph on $A$ and $X$ | $\mathcal B$ | incidence graph | $H$ | $B$ | - |
| state $s$ | bijection $A \to X$ with $s(t)$ a corner of $t$; a perfect matching of $\mathcal B$ | state | state | perfect matching of $H$ | perfect matching of $B$ | `TriangleSystem.State` |
| $Q_s$ | the $n$ sides opposite $s(t)$ | $Q_s$ | $Q_s$ | $H - M_2$ | $Q_s$ | `oppositeGraph` |
| $S_s$ | $Q_s \cup \{ao, bo\}$, the edges every selection built from $s$ avoids | $S_s$ | - | - | - | - |
| good state | $Q_s$ is a forest with exactly one root per component; equivalently $S_s$ is a spanning tree | good | "pair with $Q_s$ a forest" | cycle-breaking (for a pair) | tree matching | via `forest_pair_of_disk_circulation` |
| pair $(r,s)$ | two states differing in every face; $r$ the first state, $s$ the second | pair | pair | ordered 2-factor $(M_1, M_2)$ | disjoint matching pair | `TriangleSystem.Pair` |
| partner | $r$ in a pair $(r,s)$; a good state has exactly one, $r_s$ | partner | partner | - | disjoint mate | - |
| good pair | a pair whose second state is good; for a pair, "$Q_s$ a forest" suffices | - | "$Q_s$ a forest" | cycle-breaking 2-factor | tree pair | - |
| $u(t)$ | third corner of $t$ in a pair | $u(t)$ | $u(t)$ | - | $u(t)$ | - |
| $q(s)$ | number of cycles of $Q_s$; a state with a partner has $2^{q(s)}$ | - | - | - | $k$ (Prop. 2.1) | - |
| $\alpha$, $\beta$, $\tilde\beta$ | the running example's states: $\alpha$ with a $Q$-cycle, its partners $\beta$ (good) and $\tilde\beta$ | Example 3.3 | - | - | - | - |
| outdegree lemma | edges with outdegree at most one: cycles are directed, components have at most one sink | Lemma 3.7 | inside Lemma 6.1 | - | Prop. 2.1 | - |
| chosen sides | for a state $r$, one side at $r(t)$ in each $t \in A$, directed out of $r(t)$ | chosen sides | "chosen edges" | - | - | - |
| $D(r,s)$ | the directed edges $r(t) \to s(t)$; disjoint cycles covering $X$ | $D(r,s)$ | $D$ | cycles of $M_1 \cup M_2$, opposite orientation | $D_{r,s}$ | `StateCycle` |
| cover | undirected edge set of $D(r,s)$; its $2^c$ orientations are pairs | cover | group | 2-factor of $H$ | group | `Pair.group_sum_product` |
| $c$, $c^+$, $m$ | cycles of a cover; counterclockwise ones; least $c$ over all covers | $c$, $c^+$, $m$ | $c(D)$, $c_{\min}$ | $c_{\min}$ | $c$, $m$ | - |
| exchange graph | pairs joined by reversing one $D$-cycle or one $Q$-cycle | - | - | - | $\mathcal E$ | - |

## The disk identity and the sign

| Term | Meaning | Paper | OpenAI | Li | Constructive | Lean |
| --- | --- | --- | --- | --- | --- | --- |
| $\delta(v,w)$ | $+1$ if the black face of $vw$ is left of $v \to w$, else $-1$ | $\delta$ | $\delta$ | $\tau = (1+\delta)/2$ | $\delta$ | corner sign |
| state cycle | directed cycle of chosen sides of a state | cycle of chosen sides | "simple directed cycle in the chosen edges" | alternating cycle of $H$ | same | `StateCycle` |
| $h, \ell, I, B, W$ | length, edges with black face inside, interior vertices, black and white faces inside | same | $h, l, I, B, W$ | $\lvert C\rvert = 2h$, $t_{C,\mathrm{in}}$ | same | `state_disk_count` |
| disk identity | $W = B + 1$ and $h = 2\ell + 3$; $\delta$-sum $-3$ counterclockwise, $+3$ clockwise | Lemma 3.8 | Lemma 4.1 | Claim 25 | Lemma 4.1 | `state_disk_count`, `disk_boundary_imbalance` |
| vertex colouring $c$ | $\mathbb Z/3$ colouring with $\delta(v,w) \equiv c(w) - c(v)$ | - | mentioned | - | - | - |
| $J(r,s)$ | $\tfrac13 \sum_t \delta(r(t),s(t))$, equal to #clockwise $-$ #counterclockwise cycles of $D$ | $J$ (Remark 4.10) | $J$ | $-cw'$ | $J$ | `rawIndexSum` |
| sign $\varepsilon(r,s)$ | $\prod_t \delta(r(t),s(t)) = (-1)^{(n+c)/2}(-1)^{c^+} = (-1)^{(n+J)/2} = i^{\,n+J}$ | $\varepsilon$ (Lemma 4.4) | phase $i^J = i^{-n}\varepsilon$ | $(-1)^{cw}$ | $\varepsilon$ | `phase`; real sign $= i^n \cdot$ phase |
| two reversals | reverse a $Q_s$-cycle (changes $r$) or a $D$-cycle (swaps $r, s$ on it); both flip $\varepsilon$ | Lemma 4.3, Table 1 | Lemma 5.2, (5.4) | $\iota_1$, $\iota_2$ | moves (b), (a) | exact counterpart of Lemma 4.3 |
| cancellation | partners of a state with a $Q$-cycle cancel in signed sums | Lemma 4.5 | Lemma 5.2 | Lemma 17 | Lemma 4.2 | - |

## Heights and nonvanishing

| Term | Meaning | Paper | OpenAI | Li | Constructive | Lean |
| --- | --- | --- | --- | --- | --- | --- |
| path of faces | fixed path in $G$ from a white face $y$ to $t_0$ | path of faces | - | vertical ray | - | unit path flow |
| turn, $\kappa_y(t,v)$ | $\pm 1$ if the path of $y$ turns around $v$ in $t$ with $v$ on its left/right, else 0 | $\kappa_y$ | - | ray-spoke crossing | - | - |
| height $\eta_s(y)$ | $\sum_t \kappa_y(t, s(t))$; rises by 1 when a $D$-cycle around $y$ turns counterclockwise | $\eta_s(y)$ | - | crossings of the ray of $y$ with $M_2$ | - | potentials `ColoredDual.weights` |
| weight $\omega(s)$ | $\sum_y \eta_s(y)$; the involution note's $H(s)$ is $-\omega(s)$ | $\omega$ | $\omega(s)$ from spoke weights | number of available marks | $\omega(s)$, integers in $[0, 6n]$ | `whiteCharge_cut_integral` |
| spoke weights $a(t,v)$ | older form of the weights, on spokes from black centres to corners | $\mathfrak a$ (Section 7) | Lemma 5.3 | ray crossings | integers | `ColoredDual.weights` |
| $L(C)$ | white faces inside a $D$-cycle; the rise of $\omega$ when $C$ turns counterclockwise | $L(C)$ | $L^+(C) - L^-(C)$ | - | $L^+ - L^-$ | - |
| finite difference | alternating sum over $\{0,1\}^c$ kills degree $< c$ and leaves $\pm c!\prod L_i$ | Lemma 4.7 | - | - | - | project file `FiniteDifference.lean` |
| $\Sigma$ | $\sum_{(r,s)} \varepsilon(r,s)\, \omega(s)^m = (-1)^{(n-m)/2} m! \sum \prod L(C_i)$ | $\Sigma$ | Taylor coefficient of $Z(x)$ | $\lvert O^+\rvert - \lvert O^-\rvert$ | coefficient of $Z_{\mathcal C}(z)$ | - |
| $\Pi(w)$ | $\sum \varepsilon\, \prod_t w_{t,s(t)}$; its monomials are the good states | $\Pi$ (Section 7) | - | - | - | - |
| marks, tokens | objects attached to a pair to make the weighted count a count | - | - | marks $(w, e_2)$ | tokens $(t, j)$ | - |

## Recovery

| Term | Meaning | Paper | OpenAI | Li | Constructive | Lean |
| --- | --- | --- | --- | --- | --- | --- |
| tree of faces $Y_s$ | faces of $T$ joined across sides not in $S_s$; a spanning tree of $G$ when $s$ is good | $Y_s$ | - | black dual trace plus a leaf | - | `remainder_connected` |
| white-face tree $W_s$ | $Y_s$ with black nodes suppressed, rooted at $y_0$ | Figure 5(a) | "spanning tree on the white triangles" | $T_W = M_2^*$ | $W_s$ | - |
| $P_s$ | the side each black face shares with its child in $Y_s$ rooted at $t_0$ | $P_s$ | - | - | $P$ | `tree_matching`, `recovery_matching` |
| spoke graph $H$, $H_0$ | centres of all black faces joined to their corners; without $t_0$'s centre. Older form of $S_s$ and $Y_s$ | not used | $H$, $H_0$ | $G_{FB}$ | $H$, $H_0$ | - |
| $s_C$ | the state read off a Hamiltonian cycle $C$ avoiding the edge across $e_0$ | $s_C$ (Section 7) | - | - | - | - |

## Open problems and project labels

| Term | Meaning | Where |
| --- | --- | --- |
| point-rainbow tree | spanning tree on white faces using each black face once as a link | [step 03](03-states-and-pairs.md), 09 door 1 |
| Step R | a point-rainbow tree exists iff no black-inner separating triangle; gives a pair (proved here, unreviewed) | 09 door 1 |
| Step X (rainbow) | every point-rainbow tree reaches a good state by non-increasing exchanges (open) | 09 door 1 |
| induction G, X (ML1, ML2) | degree-four contraction keeps a pair; a good state lifts or rotates (open) | [step 08](08-gluing-and-hypotheses.md), 09 doors 2, 3 |
| C1 | at least $2^m$ good states (open; $2m$ proved) | [step 06](06-nonvanishing.md), 09 door 4 |
| C3 | monotone pair descent in $q(s)$, plateaus allowed (open) | step 06, 09 door 5 |
| P2 | face-rainbow packing of a pair support (open) | step 03, 09 door 6 |
| T2 to T5 | the route map's proof tiers: T2 written proof, T3 independently validated exhaustive computation, T4 author-only computation, T5 conjecture | [route map](../route-map/ROUTE-MAP.md) |
| `TM` | number of good states in census files ("tree matchings") | census data |

## Synonyms

One name per object in the digestions. This table lists the other names in use, so that a reader coming from another document can find the object. "inv" is `proofs/involutions/`, "pri" is `proofs/primal/`.

| Name here | Other names |
| --- | --- |
| good state | tree matching (constructive paper, older digestions, route map and labyrinth before 2026-11-14), forest state (atlas first pass), "circuit-free $Q_s$ with a partner" (pri), cycle-breaking (Li, for a pair) |
| good pair | forest pair (inv, older digestions), tree pair (constructive), cycle-breaking 2-factor (Li), "a pair with $Q_s$ a forest" (OpenAI) |
| cover | group (OpenAI, constructive), cycle cover (older digestions), unoriented-cover class (inv), 2-factor of $H$ (Li), "the undirected collection $D$" (pri) |
| $m$ | $c_{\min}$ (OpenAI, Li, older digestions and route map), `cmin` (data files) |
| $q(s)$ | $k$ (constructive, Proposition 2.1); renamed because $k$ is the number of black faces |
| $\mathcal B$ | $B$ (constructive), $H$ (Li); in pri $B$ is the set of black vertices of $G$ |
| selection $P$, selected edges | "the selected matching" (pri); pri also says "selected" for the edges of $D$, which these digestions never do. Not the paper's "chosen sides", which are the edges leaving a state's corners |
| height $\eta_s(y)$ | $h_s(w)$ (older digestions, spoke-crossing version), $-H$ summed (inv), integer potentials $a(b,f)$ (pri) |
| $\omega(s)$ | weight (paper), $-H(s)$ (inv) |
| $Y_s$, $W_s$ | incidence tree $H - s$ and its dual (older digestions), recovery tree $K$ (pri) |
| constructive paper | trees paper (older digestions), unsigned manuscript (paper) |
