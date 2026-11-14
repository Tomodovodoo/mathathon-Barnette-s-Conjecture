# Route and architecture for the expository paper

## 1. From where to where

The proof is six ideas. Each one answers the question the previous one leaves open.

**1. Degree is free, connectivity is the problem.** A Hamiltonian cycle of cubic $G$ is $G-M$ for a perfect matching $M$, and $G-M$ is connected exactly when $M^*$ contains no cycle of the dual $T$ (cycles of $T$ are bonds of $G$). A nontrivial 3-edge cut (a separating triangle of $T$) splits the problem, and the halves splice only if they avoid the same cut edge. That is why the avoided edge is in the theorem. *Reader believes* two classical facts.

**2. Orient the answer and a bijection appears.** Orient $M^*\setminus e_0$ towards the corners of a black face $t_0\ni e_0$. Each other vertex is the tail of one edge, and each other black face holds one edge, so the tails give a perfect matching $s$ of the incidence graph $H^\circ$ of black faces and non-root vertices: a *state*. Backwards, $s$ forbids the side opposite $s(t)$ in each black face. If these sides and two sides of $t_0$ form a spanning tree (a *good* state), the dual tree in $G$ has a unique perfect matching, whose complement is the cycle. *Reader believes:* the definition is what the answer looks like once oriented.

**3. The disk identity.** Why one cycle? A directed cycle of sides leaving chosen corners encloses one more white face than black and has length $2\ell+3$. Three counts prove it: Euler for the disk, colour balance, and the state (black faces inside ↔ interior vertices plus $\ell$ cycle vertices). A perfect matching along such a cycle would force three more. It serves acyclicity, odd length and the sign.

**4. A second state makes a global condition local.** A state $r$ disjoint from $s$ orients $Q_s$ with outdegree one off the roots, so a component without a cycle has exactly one root. Hence $s$ is good iff it has a partner and $Q_s$ is acyclic, the partner is then unique, and partners differ by reversing cycles of $Q_s$.

**5. One sum, two products (the 2026 idea).** Put $Z(z)=\sum_{(r,s)}\varepsilon(r,s)\,z^{\omega(s)}$ over ordered pairs of disjoint states, with $\varepsilon$ a product of local signs and $\omega$ a height function. Grouped by $s$, the sum over partners is a product over the cycles of $Q_s$. Each cycle is odd, so reversing it flips $\varepsilon$ and fixes $s$, and each factor is $1-1$. Hence $Z=\sum_{s\text{ good}}\pm z^{\omega(s)}$. Grouped by the 2-factor $r\cup s$, it is a product over its cycles. Reversing $C$ flips $\varepsilon$ and shifts $\omega$ by $L(C)\ge1$, the white faces inside, so a 2-factor with $c$ cycles gives $\pm z^{\omega_0}\prod_{i\le c}(1-z^{L_i})$, vanishing at $1$ to order exactly $c$. All 2-factors with the least number $m$ of cycles have leading sign $(-1)^{(n+m)/2}$, so $Z$ has a zero of order exactly $m$ and $Z\neq0$. *Reader believes:* one sum factors over the cycles of two graphs, with exponent $0$ over $Q_s$ and positive over $r\cup s$.

**6. A first pair.** A pair is a 2-factor of $H^\circ$ with a marked matching. Hall's theorem gives one when an edge count holds, and Euler proves it without separating triangles, the one hypothesis left.

The new idea is 5, powered by 3. Ideas 1–2 are classical in substance (Stein; Tutte's trinity states).

## 2. Language

Write the paper in $T$, with two auxiliary graphs used only where they make lemmas disappear.

- **$T$ carries the geometry.** Corners, the inside of a cycle, Euler for a disk and colour balance are visible in $T$. In $G$ they become statements about bonds and shores.
- **$G$ carries the statement and the reduction.** Lemma 2.1 and the 3-cut splice take three sentences each in $G$, against a page of induced-tree gluing in $T$.
- **$H^\circ$ carries states and pairs.** $H$ is the plane bipartite incidence graph of black faces and vertices of $T$, equivalently of black vertices and faces of $G$. Every face of $H$ is a hexagon around a white face. $H^\circ$ deletes $t_0$ and its corners. There a state is a perfect matching, a pair a 2-factor with a marked matching, a cycle of chosen sides an alternating cycle, a reversal a rotation. The reversal, outdegree and cover-class lemmas disappear into standard matching language. Above all, the height becomes Thurston's. For a fixed state $s_0$, $s-s_0$ is a circulation on $H$, hence the coboundary of a unique integer function on faces vanishing on the outer face; $\omega(s)$ is its sum. Rotating $C$ changes $\omega$ by $\pm$ the number of faces inside $C$. The old height lemma and its case analysis become five lines.

Rejected frames. α-orientations name the partner lemma but do not shorten it. Temperley/KPW fails because a spanning tree with one side per black face need not come from a state. LGV and Thomason do not fit, since the proof needs a product of $(1-1)$ factors and nonvanishing, not path crossings or parity.

Definitions needed: the face 2-colouring; $t_0,e_0$, roots, $A$, $X$; $H$, $H^\circ$; state; $Q_s$; good; chosen sides (= $r$-alternating cycles); pair; $\varepsilon$; $\omega$; $L(C)$; $m$. The words "selection", "cover", "spokes", "tree of faces" and "piece" go. Say "perfect matching $M$ with $M^*$ acyclic" and "the 2-factor $r\cup s$".

## 3. The core: generating function, not finite difference

Present $Z(z)$. Reasons:

1. Both groupings are products $\prod(1-z^{a})$, with $a=0$ on cycles of $Q_s$ and $a=L(C)\ge1$ on cycles of $r\cup s$. Cancellation and nonvanishing become one argument.
2. $m$ enters as the order of a zero, not as an exponent chosen in advance. The need for the minimum explains itself: the leading sign $(-1)^{(n+c)/2}$ alternates as $c$ grows by two.
3. The expansion lemma for $(\omega_0+\sum x_iL_i)^m$ is replaced by $1-z^L=L(1-z)+O((1-z)^2)$.

The sign lemma stays. Along a counterclockwise cycle of chosen sides the local signs sum to $2\ell-h=-3$. So $\varepsilon(r,s)=(-1)^{(n+c)/2+c^+}$, and every reversal flips $\varepsilon$. One sentence after the theorem links the sources: the coefficient $\frac1{m!}Z^{(m)}(1)=\sum\varepsilon\binom{\omega(s)}{m}$ is the finite difference, $Z(e^x)$ is OpenAI's exponential sum up to $i^{-n}$, Li's marked crossings expand the same coefficient bijectively, and the anonymous manuscript specialises the multivariate polynomial at nonnegative integer weights.

## 4. What to cut and what to cite

- Dual is a simple 2-coloured triangulation: one sentence (Whitney; Mohar–Thomassen).
- Connectivity lemma: gone into "Euler for a triangulated disk" (Mohar–Thomassen).
- Duality lemma: cited (Diestel, Ch. 4: cycles of $T$ are bonds of $G$; tree duality).
- Two induced trees: one historical clause (Stein; Alt–Payne–Schmidt–Wood).
- Selections give states: a motivating paragraph. Good ⇔ spanning tree: the definition. $Y_s$: four sentences in Prop. 3.2.
- Outdegree and reversal lemmas: one clause each (Lovász–Plummer). Cancellation: $\prod(1-1)$. Finite difference: gone.
- Heights: five lines via face potentials (Thurston; Diestel for face boundaries spanning the cycle space).
- Cap lemma and gluing in $T$: Lemma 2.2 in $G$ (Kelmans via Hertel and Alt et al.; Li, App. C; 3-connectivity of contractions cited).
- Flow network: Hall's theorem with multiplicities.
- Removed outright: the remark on other sums, the reversal table, Example environments, "how this account differs", the Lean and companion-note paragraphs, the hypotheses section.

## 5. Discoveries: in or out

- **One more white than black.** In, as Lemma 3.1. The recovery needs only the state count $B=I+\ell$, the matching count $W-(h-\ell)=B-\ell$ and Euler's $B+W=2I+h-2$. Together they give $0=-2$. Colour balance serves only the odd length and the sign.
- **Role of $m$.** In, as the order of the zero.
- **Sign-free limits.** In, two sentences in the remarks. Inside a 2-factor each half of goodness can be met alone. But a 16-vertex triangulation has a 2-factor, a single cycle, neither of whose orientations has a good second state. So a proof must compare 2-factors, and the order-$m$ coefficient does that.
- **Not a matroid intersection.** In, one sentence. Good states are the common bases of three matroids on $E(T)$: graphic, one side per black face, distinct opposite corners. Dropping one of them admits non-states on the hexagonal prism.
- **Which cycles arise.** In, three sentences. The map from good states to cycles is injective. A cycle avoiding $e$ arises iff the state it induces is good. The hexagonal prism, with the edge on the equator, has four such cycles and two good states.
- **Hypothesis counterexamples.** Out; name Tutte's and Georges' graphs in the history.
- **Algorithm.** In, two sentences: the manuscript's enumeration in polynomial time $\times\,3^{|V(G)|/4}$; no polynomial algorithm known.
- **Open problems.** In: a polynomial construction; a sign-free proof (which must leave its starting 2-factor); at least $2^m$ good states? Plus the Pfaffian corollary and Kelmans' open two-edge version as consequences.
- **Exact first-pair criterion, families, descent, lattice.** Out.

## 6. Architecture

**Title.** *The proof of Barnette's conjecture*; short title *Barnette's conjecture*.

**Abstract.**
> We give a short self-contained account of OpenAI's 2026 proof of Barnette's conjecture, in the form that every cubic, bipartite, 3-connected planar graph has a Hamiltonian cycle avoiding any prescribed edge. In the dual Eulerian triangulation such a cycle comes from a choice of one corner in each black face, using every vertex once, whose opposite sides form a spanning tree. Such a choice is found by a signed count over pairs of disjoint choices, recorded as a Laurent polynomial in one variable. Grouped by its second choice, the count keeps only the choices with the tree property. Grouped by the cycles along which the two choices differ, it vanishes at 1 to order exactly the least number of these cycles, and so it is not zero. Both groupings rest on one count: a cycle of sides leaving chosen corners encloses one more white face than black.

**Sections and budget** (11.5 pages):

1. Introduction, 1.75 pp. Theorem 1.1, five sentences of history (Tait, Tutte, Barnette, computer searches, the three 2026 accounts), the idea of the proof, Figure 1.
2. The dual triangulation, 1.5 pp.
3. States and the disk identity, 2.5 pp.
4. The signed count, 2.75 pp.
5. The first pair, 1.25 pp.
6. Remarks, 1 p, unnumbered paragraphs.

References, 0.75 pp.

**Numbered statements.**

- **Theorem 1.1** (OpenAI). $G$ cubic, bipartite, planar, 3-connected, $e\in E(G)$ ⇒ a Hamiltonian cycle avoiding $e$.
- **Lemma 2.1.** $G-M$ is a Hamiltonian cycle if $M$ is a perfect matching with $M^*$ acyclic in $T$. Uses: cycles of $T$ are bonds of $G$ (cited).
- **Lemma 2.2** (three-edge cuts). If Theorem 1.1 holds for both contractions of a nontrivial 3-edge cut, it holds for $G$. Uses: colour count on the cut, the splice, 3-connectivity (cited).
- **Theorem 2.3.** If $T$ has no separating triangle, then $G$ has a perfect matching $M\ni e$ with $M^*$ acyclic. Proved at the end of §5. With 2.1–2.2 and induction it gives 1.1.
- **Lemma 3.1** (disk identity). For a directed cycle of chosen sides of a state, $W=B+1$ and $h=2\ell+3$. Uses: Euler for a triangulated disk, colour balance, bijectivity of the state.
- **Proposition 3.2.** A good state yields a perfect matching $M\ni e$ with $M^*$ acyclic. Uses: tree duality (cited), the unique perfect matching of the dual tree, the three counts.
- **Lemma 4.1** (partners). Partners of $s$ are the orientations of $Q_s$ with outdegree one off the roots. They exist only if every component is a one-root tree or a rootless unicyclic graph, and they differ by reversing cycles. So $s$ is good iff it has a partner and $Q_s$ is acyclic, and then the partner is unique.
- **Lemma 4.2** (sign). Reversing a cycle of chosen sides flips $\varepsilon$, and $\varepsilon(r,s)=(-1)^{(n+c)/2+c^+}$. Uses: 3.1.
- **Lemma 4.3** (height). Rotating a cycle $C$ of $r\cup s$ changes $\omega(s)$ by $\pm L(C)$, $L(C)\ge1$. Uses: face potentials of circulations in $H$.
- **Theorem 4.4.** If $T$ has a pair, it has a good state. Uses: 4.1–4.3, the two groupings of $Z$.
- **Lemma 5.1** (density). Without separating triangles, $e(U)-b(U)\le 2|U|-4$ for every $U\supseteq\{a,b,o\}$. Uses: Euler for $T[U]$, the balance of faces of length at least 4.
- **Proposition 5.2.** Without separating triangles, $H^\circ$ has a 2-factor, so $T$ has a pair. Uses: Hall with multiplicities, 5.1.

No numbered definitions or examples.

**Figures** (four).

1. *Cube and octahedron*: a disconnected 2-factor, the dual with $t_0,e_0$, a good state with $Q_s$, the Hamiltonian cycle. The whole translation, checkable by hand. With two states and $Z=\pm z^{\omega_0}(1-z)$ it is too small for the core.
2. *One black face*: $r(t),s(t),u(t)$, the side in $Q_s$, the arc $r(t)\to s(t)$, the edges of $H$ at $t$. The legend.
3. *Disk identity* on the 7-cycle of the 13-vertex example, with $B,W,I,\ell$ marked.
4. *The two groupings* on the 13-vertex example. The pair $(\beta,\alpha)$ with the cycles of $r\cup s$ and the cyclic $Q_\alpha$. Beside it, the two 2-factors as squares of four pairs, each summing to $z^{\omega_0}(1-z^{L_1})(1-z^{L_2})$, with the two pairs sharing $\alpha$ shaded. This is the key figure.
The core needs a cancelling pair and $m=2$, which is why the 13-vertex triangulation is used there. It should appear only in Figures 3–4 and their captions.

**Closing remarks** (§6, one page). They hold the items marked "in" in §5, the sources' variants of the count, and the multivariate form $\sum_{s\text{ good}}\pm w^s=\sum_F\pm\prod_{C}(w^{C+}-w^{C-})$.

## 7. The idea of the proof (for the introduction)

> A Hamiltonian cycle of a cubic graph $G$ is the complement of a perfect matching $M$, and $G-M$ is connected exactly when the edges $M^*$ of the dual triangulation $T$ that cross $M$ contain no cycle. Since $G$ is bipartite, the faces of $T$ are coloured black and white. Fix a black face $t_0$ with a side $e_0$, and orient the forest $M^*$ minus $e_0$ towards the corners of $t_0$. Every other vertex is then the tail of exactly one edge, so $M$ determines a bijection $s$ from the black faces other than $t_0$ to the remaining vertices, with $s(t)$ a corner of $t$. We call such a bijection a state. Conversely, a state forbids in each black face other than $t_0$ the side opposite its chosen corner. If the forbidden sides, together with two sides of $t_0$, form a spanning tree of $T$, the state is good. Then the dual tree in $G$ has a unique perfect matching, and its complement is a Hamiltonian cycle. That the complement is a single cycle rests on a count due to OpenAI: a directed cycle of sides leaving chosen corners encloses exactly one more white face than black, whereas a perfect matching running along such a cycle would force three more.
>
> Nobody knows how to point to a good state, so we count. A second state $r$ that differs from $s$ in every face orients the forbidden sides with outdegree one at every vertex off $t_0$, and then $s$ is good exactly when these sides contain no cycle. We sum over all such pairs the expression $\varepsilon(r,s)\,z^{\omega(s)}$, where $\varepsilon$ is a product of local signs and $\omega$ is a height function. For fixed $s$, the partners $r$ differ by reversing cycles of forbidden sides. Each such cycle has odd length, so its reversal changes the sign and not $s$, and every state that is not good contributes zero. For fixed $2$-factor $r\cup s$, the pairs differ by reversing its cycles. Reversing a clockwise cycle $C$ changes the sign and multiplies $z^{\omega(s)}$ by $z^{L(C)}$, where $L(C)\ge1$ is the number of white faces inside $C$. A $2$-factor with $c$ cycles therefore contributes $\pm z^{\omega_0}\prod_C(1-z^{L(C)})$, which vanishes at $z=1$ to order exactly $c$. The $2$-factors with the fewest cycles have leading terms of one sign, so the sum has a zero of exactly that order at $z=1$. It is therefore not zero, and a good state exists. It remains to find one pair, which Hall's theorem does when $T$ has no separating triangle, and to cut along separating triangles. The avoided edge is needed there, because two halves can be joined only if their cycles avoid the same edge of the cut.
