# Route and architecture for the expository paper

## 1. From where to where

The proof is six ideas. Each one answers the question the previous one leaves open.

**1. Degree is free, connectivity is the problem.** A Hamiltonian cycle of a cubic graph $G$ is $G-M$ for a perfect matching $M$. $G-M$ is connected exactly when the dual edge set $M^*$ contains no cycle of the dual triangulation $T$, because cycles of $T$ are the bonds of $G$. So we want a perfect matching with acyclic dual through the prescribed edge $e_0$. A nontrivial 3-edge cut of $G$ (a separating triangle of $T$) splits the problem in two. The halves can be spliced only if they avoid the same cut edge, and that is why the avoided edge is part of the theorem. *The reader must believe:* the problem lives in $T$, and $T$ may be assumed to have no separating triangle. It is natural because both steps are classical (plane duality; Kelmans' reduction).

**2. Orient the answer and a bijection appears.** Orient the forest $M^*\setminus e_0$ towards the corners of a black face $t_0\ni e_0$. Every other vertex is then the tail of exactly one edge, and every other black face contains exactly one edge. The tails give a bijection $s$ from the black faces other than $t_0$ to the non-root vertices, with $s(t)$ a corner of $t$. This is a perfect matching of the incidence graph $H^\circ$ between black faces and vertices, a *state*. Read backwards, a state forbids in each black face the side opposite $s(t)$. When the forbidden sides, together with the two sides of $t_0$ other than $e_0$, form a spanning tree of $T$ (a *good* state), the dual tree in $G$ has a unique perfect matching. Its complement is the Hamiltonian cycle. *The reader must believe:* a good state is exactly the right certificate. The definition is not invented. It is what the answer looks like once it is oriented.

**3. The disk identity.** Why is that complement one cycle? A directed cycle of sides leaving chosen corners encloses one more white face than black, and it has length $2\ell+3$, where $\ell$ counts its edges whose black face is inside. The proof is three counts: Euler for the disk, the colour balance of the sides, and the state, which matches the black faces inside with the interior vertices and $\ell$ vertices of the cycle. A perfect matching running along such a cycle would force three more white faces than black. *The reader must believe* one count. This is the geometric engine of the whole paper, and it is used three times (acyclicity, odd length, sign).

**4. A second state turns a global condition into a local one.** "One root in each tree" is a condition on whole components. A state $r$ disjoint from $s$ orients the forbidden sides $Q_s$ with outdegree one at every non-root and zero at the roots. Then a component without a cycle contains exactly one root. So $s$ is good if and only if it has a partner and $Q_s$ is acyclic, and then the partner is unique. The partners of $s$ differ by reversing cycles of $Q_s$. *Natural because* outdegree-one orientations are the most elementary way to count roots.

**5. One sum, two products (the 2026 idea).** Put
$$Z(z)=\sum_{(r,s)}\varepsilon(r,s)\,z^{\omega(s)},$$
the sum running over ordered pairs of disjoint states. Here $\varepsilon$ is a product of local signs, one in each black face, and $\omega$ is a height function. Grouped by $s$, the partners of $s$ form a product over the cycles of $Q_s$. Each cycle is odd by idea 3, so reversing it flips $\varepsilon$ and leaves $s$ alone, and each factor is $1-1=0$. Hence $Z(z)=\sum_{s\text{ good}}\pm z^{\omega(s)}$. Grouped by the 2-factor $r\cup s$ of $H^\circ$, the pairs form a product over its cycles. Reversing a cycle $C$ flips $\varepsilon$ and multiplies $z^{\omega(s)}$ by $z^{\pm L(C)}$, where $L(C)\ge1$ counts the white faces inside. So a 2-factor with $c$ cycles contributes $\pm z^{\omega_0}\prod_{i=1}^{c}(1-z^{L_i})$. This vanishes at $z=1$ to order exactly $c$. The 2-factors with the least number $m$ of cycles all have the leading sign $(-1)^{(n+m)/2}$. So $Z$ has a zero of order exactly $m$ at $1$, and $Z\ne0$. *The reader must believe:* the same sum factors over the cycles of two different graphs. Over $Q_s$ the exponent is $0$; over $r\cup s$ it is positive. That contrast is the entire proof of existence.

**6. A first pair.** A pair is a 2-factor of $H^\circ$ with one of its two perfect matchings marked. Hall's theorem gives one if an edge-count inequality holds for every vertex set, and Euler's formula proves that inequality when $T$ has no separating triangle. *Natural because* this is the only hypothesis left to use.

The new idea is 5, together with the count 3 that powers it. Ideas 1 and 2 are classical in substance (Stein; Tutte's trinity states). Idea 4 is elementary. The paper should feel like a descent to 5.

## 2. Language

Write the paper in $T$, with two auxiliary graphs used only where they make lemmas disappear.

- **$T$ carries the geometry.** Corners, sides, the inside of a cycle, Euler for a triangulated disk and the colour balance are all visible in $T$. In $G$ the same counts become statements about bonds and shores, and the reader translates back anyway.
- **$G$ carries the statement and the reduction.** Lemma 2.2 (perfect matching with acyclic dual) and the 3-edge-cut splice are three sentences in $G$, against a page of "two induced trees" gluing in $T$.
- **$H^\circ$ carries states and pairs.** $H$ is the plane bipartite incidence graph of black faces and vertices of $T$, equivalently of black vertices and faces of $G$. Every face of $H$ is a hexagon around a white face. $H^\circ$ deletes $t_0$ and its corners. In $H^\circ$, a state is a perfect matching, a pair is a 2-factor with a marked matching, a directed cycle of chosen sides is an alternating cycle, a reversal is the rotation of an alternating cycle, and the class of a pair is its 2-factor. All of this is standard matching language, so the lemmas on reversals, the outdegree lemma and the cover-class argument disappear. Most important, the height becomes Thurston's height function. The 2-factor difference $s-s_0$ is a circulation on $H$, so it is the coboundary of a unique integer function on the faces that vanishes on the outer face (the face boundaries span the cycle space). $\omega(s)$ is its sum. Rotating an alternating cycle $C$ changes $\omega$ by $\pm$ the number of faces inside $C$. The old Lemma 4.5, with its paths of faces and its left/right case analysis, becomes five lines.

Frames considered and rejected. Felsner's α-orientations name the partner lemma but do not shorten it; one clause can mention them. Kenyon–Propp–Wilson/Temperley does not apply: a spanning tree of $T$ with one side in each black face need not come from a state, and the state condition is genuinely extra. Lindström–Gessel–Viennot is the wrong shape, since the cancellation here is a product of $(1-1)$ factors and not a path-crossing involution. Thomason's lollipop gives parity, and the proof needs nonvanishing, not parity.

Objects that need definitions: Eulerian triangulation with its face 2-colouring (one sentence, standard); $t_0$, $e_0$, the roots, $A$, $X$; $H$ and $H^\circ$; state; $Q_s$; good state; chosen sides (arcs $v\to w$ with $vw$ a side of $t$ and $v=r(t)$), identified with $r$-alternating cycles; pair; the sign $\varepsilon$; the height $\omega$; $L(C)$; $m$. The old words "selection", "cover", "spokes", "tree of faces" and "piece" disappear. Use "perfect matching $M$ of $G$ with $M^*$ acyclic" and "the 2-factor $r\cup s$".

## 3. The core: generating function, not finite difference

Present $Z(z)$. Reasons:

1. Both groupings become products of the same shape, $\prod(1-z^{a})$, with $a=0$ for cycles of $Q_s$ and $a=L(C)\ge1$ for cycles of $r\cup s$. That symmetry explains why the cancellation and the nonvanishing are one argument and not two tricks.
2. The vanishing order at $z=1$ is the number of cycles. So $m$ enters as the order of a zero and not as an exponent chosen in advance. The reason for the minimum explains itself: different orders cannot be compared, and the leading sign $(-1)^{(n+c)/2}$ alternates as $c$ grows by two.
3. Lemma 4.8 (expansion of $(\omega_0+\sum x_iL_i)^m$) disappears; $1-z^L=L(1-z)+O((1-z)^2)$ replaces it.

The sign lemma remains. Along a counterclockwise cycle of chosen sides the local signs sum to $2\ell-h=-3$ by the disk identity. So $\varepsilon(r,s)=(-1)^{(n+c)/2}(-1)^{c^+}$, and reversing any cycle of chosen sides, of $Q_s$ or of $r\cup s$, flips $\varepsilon$. One sentence after the theorem gives the dictionary to the sources: the Taylor coefficient $\frac1{m!}Z^{(m)}(1)=\sum\varepsilon\binom{\omega(s)}{m}$ is the finite difference, $Z(e^x)$ is OpenAI's exponential sum up to $i^{-n}$, Li's marked crossings expand the same coefficient bijectively, and the anonymous manuscript specialises the multivariate polynomial at nonnegative integer weights.

## 4. What to cut and what to cite

| Present statement | Fate | Reference |
|---|---|---|
| Lemma 2.1 (dual is a simple 2-coloured triangulation) | one sentence | Whitney; Mohar–Thomassen |
| Lemma 2.2 (faces bounded by cycles ⇒ connected) | disappears into "Euler for a triangulated disk" | Mohar–Thomassen, Ch. 2 |
| Lemma 2.3 (plane duality of acyclic sets, spanning trees) | cited | Diestel, Ch. 4 (bonds are dual cycles; dual of a spanning tree's complement) |
| Prop. 2.4 (two induced trees) | removed; one historical clause | Stein; Alt–Payne–Schmidt–Wood, Lemma 5 |
| Lemma 3.1 (selections give states) | motivating paragraph, no statement | |
| Lemma 3.3, Lemma 3.4 (good ⇔ spanning tree; $Y_s$) | "good" defined as the spanning tree; recovery is 4 sentences inside Prop. 3.2 | |
| Lemma 3.5 (outdegree) | one clause (functional graphs) | |
| Lemma 4.2 (reversals) | rotation of an alternating cycle, standard | Lovász–Plummer |
| Lemma 4.4 (cancellation by involution) | the product $\prod(1-1)$ | |
| Lemma 4.5 (heights) | five-line lemma via face potentials | Thurston (height functions); Diestel (face boundaries span the cycle space) |
| Lemma 4.6 (finite difference) | removed | |
| Remark 4.7, tables of reversals, all Example environments | removed; example lives in two figures and one table | |
| Lemma 6.1 (cap colours), Theorem 6.2 (gluing in $T$) | Lemma 2.3 in $G$: colour count on a 3-cut, contract each side, splice | Kelmans via Hertel and Alt et al.; Li, App. C; 3-connectivity of the contractions cited |
| Prop. 5.1 network | Hall's theorem with multiplicities | Hall; or Ford–Fulkerson |
| "How this account differs", Lean paragraph, companion notes | removed | |
| Hypotheses section (bipyramid incidence graph, 26-vertex construction) | removed; Tutte's and Georges–Kelmans' graphs named in the introduction | Tutte 1946; Georges 1989 |

Kept with proof: the disk identity, the recovery, the partner lemma, the sign lemma, the height lemma, the main count, the density inequality, the 3-cut splice.

## 5. Discoveries: in or out

- **One more white than black.** In. It is the statement of Lemma 3.1, and its two counts give the recovery proof a one-line contradiction. Note for the writer: the recovery needs only the state count and Euler. With $B=I+\ell$ (state), $W-(h-\ell)=B-\ell$ (matching), and $B+W=2I+h-2$ (Euler), adding gives $0=-2$. The colour balance is needed only for the odd length and the sign.
- **Role of $m$.** In, as the order of the zero, with one sentence on why the minimum is needed.
- **Sign-free limits.** In, closing remarks, two sentences. Inside each 2-factor each half of goodness can be met on its own, but a 16-vertex triangulation has a 2-factor that is a single cycle, neither of whose two orientations has a good second state. So any proof must compare 2-factors, and the order-$m$ coefficient does exactly that.
- **Not a matroid intersection.** In, one sentence in the algorithmic remark. Good states are the common bases of three matroids on $E(T)$ (graphic, one side per black face, distinct opposite corners). The two-matroid relaxations admit non-states already on the hexagonal prism.
- **Which Hamiltonian cycles arise.** In, three sentences. Different good states give different cycles. A cycle avoiding $e$ arises exactly when the state it induces is good. The hexagonal prism with $e_0$ on the equator has four such cycles and two good states.
- **Counterexamples for each hypothesis.** Out, except naming Tutte's graph and Georges' graph in the introduction, and the fact that planarity enters only through $|A|=|X|$ (Euler).
- **Algorithm.** In, two sentences. The anonymous manuscript enumerates good states in time polynomial times $3^{|V(G)|/4}$. No polynomial-time algorithm is known.
- **Open problems.** In, three items. Find a polynomial-time construction. Find a proof without signs, which by the 16-vertex example must leave the 2-factor it starts in. Decide whether there are always at least $2^m$ good states. Also the Pfaffian corollary (Gorsky–Steiner–Wiederrecht) as one sentence of consequence, and Kelmans' open two-edge version.
- **Exact criterion for the first pair, families, counts, descent, lattice.** Out.

## 6. Architecture

**Title.** *The proof of Barnette's conjecture*; short title *Barnette's conjecture*.

**Abstract.**
> We give a short self-contained account of OpenAI's 2026 proof of Barnette's conjecture, in the form that every cubic, bipartite, 3-connected planar graph has a Hamiltonian cycle avoiding any prescribed edge. In the dual Eulerian triangulation such a cycle comes from a choice of one corner in each black face, using every vertex once, whose opposite sides form a spanning tree. Such a choice is found by a signed count over pairs of disjoint choices, recorded as a Laurent polynomial in one variable. Grouped by its second choice, the count keeps only the choices with the tree property. Grouped by the cycles along which the two choices differ, it vanishes at 1 to order exactly the least number of these cycles, and so it is not zero. Both groupings rest on one count: a cycle of sides leaving chosen corners encloses one more white face than black.

**Sections and budget** (11.5 pages):

1. Introduction, 1.75 pp. Theorem 1.1. A five-sentence history (Tait, Tutte, Barnette; Holton–Manvel–McKay and Brinkmann–Goedgebeur–McKay; OpenAI, Li, the anonymous manuscript). The idea of the proof. Figure 1.
2. The dual triangulation, 1.5 pp.
3. States and the disk identity, 2.5 pp.
4. The signed count, 2.75 pp.
5. The first pair, 1.25 pp.
6. Remarks, 1 p, unnumbered paragraphs.

References, 0.75 pp.

**Numbered statements.**

- **Theorem 1.1** (OpenAI). $G$ cubic, bipartite, planar, 3-connected, $e\in E(G)$ ⇒ a Hamiltonian cycle avoiding $e$.
- **Lemma 2.1.** $G-M$ is a Hamiltonian cycle if $M$ is a perfect matching with $M^*$ acyclic in $T$. Uses: cycles of $T$ are bonds of $G$ (cited).
- **Lemma 2.2** (three-edge cuts). If Theorem 1.1 holds for both contractions of a nontrivial 3-edge cut, it holds for $G$. Uses: colour count forcing the cut edges' ends on each side into one class, the splice, 3-connectivity of the contractions (cited).
- **Theorem 2.3.** Let $T$ be an Eulerian triangulation without separating triangle, $t_0$ a black face, $e_0$ a side. Then $G$ has a perfect matching $M\ni e$ with $M^*$ acyclic. Theorem 1.1 follows by induction from 2.1–2.3. Proved at the end of §5.
- **Lemma 3.1** (disk identity). For a directed cycle of chosen sides of a state, $W=B+1$ and $h=2\ell+3$. Uses: Euler for a triangulated disk, colour balance, bijectivity of the state.
- **Proposition 3.2.** A good state yields a perfect matching $M\ni e$ with $M^*$ acyclic. Uses: tree duality (cited), the unique perfect matching of the dual tree, the three counts.
- **Lemma 4.1** (partners). Partners of $s$ are the orientations of $Q_s$ with outdegree one off the roots. They exist only if each component is a one-root tree or a rootless unicyclic graph, and they are then obtained from one another by reversing cycles. So $s$ is good iff it has exactly one partner and $Q_s$ is acyclic.
- **Lemma 4.2** (sign). Reversing a cycle of chosen sides flips $\varepsilon$, and $\varepsilon(r,s)=(-1)^{(n+c)/2+c^+}$. Uses: 3.1.
- **Lemma 4.3** (height). Rotating a cycle $C$ of $r\cup s$ changes $\omega(s)$ by $\pm L(C)$, $L(C)\ge1$. Uses: face potentials of circulations in $H$.
- **Theorem 4.4.** If $T$ has a pair, it has a good state. Uses: 4.1–4.3, the two groupings of $Z$.
- **Lemma 5.1** (density). Without separating triangles, $e(U)-b(U)\le 2|U|-4$ for every $U\supseteq\{a,b,o\}$. Uses: Euler for $T[U]$, the balance of faces of length at least 4.
- **Proposition 5.2.** Without separating triangles, $H^\circ$ has a 2-factor, so $T$ has a pair. Uses: Hall with multiplicities, 5.1.

Twelve statements. No numbered definitions or examples.

**Figures** (four, with a fifth optional).

1. *The cube and its octahedron.* (a) A 2-factor of the cube with two components; (b) the dual with black faces, $t_0$, $e_0$; (c) a good state and $Q_s$; (d) the Hamiltonian cycle. This shows the whole translation on a graph checkable by hand. The cube has two states, both good, and one 2-factor (a triangle), so $Z=\pm z^{\omega_0}(1-z)$. It is too small for the core, which is why it appears only here.
2. *One black face.* The corners $r(t)$, $s(t)$, $u(t)$, the side in $Q_s$, the arc $r(t)\to s(t)$, and the three edges of $H$ at $t$. This is the legend for everything after it.
3. *The disk identity* on the 7-cycle of the 13-vertex example, with $B,W,I,\ell$ marked. The reader needs to see the three counts once.
4. *The two groupings* on the 13-vertex example. Left: the pair $(\beta,\alpha)$ with the two cycles of $r\cup s$ and the cyclic $Q_\alpha$. Right: the two 2-factors as squares of four pairs with $\varepsilon$ and $\omega$, each summing to $z^{\omega_0}(1-z^{L_1})(1-z^{L_2})$, with the two pairs sharing $\alpha$ shaded. One small table of the eight pairs may sit beside it. This is the key figure.
5. (Optional) *The splice across a 3-edge cut* in $G$.

Running example: the octahedron for the overview, the 13-vertex triangulation for the core. The 13-vertex example is the smallest at hand that shows a cancelling pair and two cycles in every 2-factor ($m=2$), which the product needs. It should appear only in Figures 3–4 and their captions, never in example environments in the text.

**Closing remarks** (§6, about one page): which Hamiltonian cycles arise; the sources' variants of the count (finite difference, exponential sum, involutions, integer weights) and the multivariate form $\sum_{s\text{ good}}\pm w^s=\sum_F\pm\prod_{C}(w^{C+}-w^{C-})$; why signs, via the 16-vertex 2-factor; the three-matroid description and the $3^{|V(G)|/4}$ enumeration; consequences (Kelmans' edge pairs on a face, the Pfaffian corollary); the open problems of §5.

## 7. The idea of the proof (for the introduction)

> A Hamiltonian cycle of a cubic graph $G$ is the complement of a perfect matching $M$, and $G-M$ is connected exactly when the edges $M^*$ of the dual triangulation $T$ that cross $M$ contain no cycle. Since $G$ is bipartite, the faces of $T$ are coloured black and white. Fix a black face $t_0$ with a side $e_0$, and orient the forest $M^*$ minus $e_0$ towards the corners of $t_0$. Every other vertex then becomes the tail of exactly one edge of $M^*$, which lies in a black face, and so $M$ determines a bijection $s$ from the black faces other than $t_0$ to the remaining vertices, with $s(t)$ a corner of $t$. We call such a bijection a state. Conversely, a state forbids in each black face the side opposite its chosen corner. If the forbidden sides, together with two sides of $t_0$, form a spanning tree of $T$, the state is good. Then the dual tree in $G$ has a unique perfect matching, and its complement is a Hamiltonian cycle. That the complement is a single cycle rests on a count due to OpenAI: a directed cycle of sides leaving chosen corners encloses exactly one more white face than black, whereas a perfect matching running along such a cycle would force three more.
>
> Nobody knows how to point to a good state, so we count. A second state $r$ that differs from $s$ in every face orients the forbidden sides with outdegree one at every vertex off $t_0$, and then $s$ is good exactly when these sides contain no cycle. We sum over all such pairs the expression $\varepsilon(r,s)\,z^{\omega(s)}$, where $\varepsilon$ is a product of local signs and $\omega$ is a height function. For fixed $s$, the partners $r$ differ by reversing cycles of forbidden sides. Each such cycle has odd length, so its reversal changes the sign and not $s$, and every state that is not good contributes zero. For fixed $2$-factor $r\cup s$, the pairs differ by reversing its cycles. Reversing a cycle $C$ changes the sign and multiplies $z^{\omega(s)}$ by $z^{L(C)}$, where $L(C)\ge1$ is the number of white faces inside $C$. A $2$-factor with $c$ cycles therefore contributes $\pm z^{\omega_0}\prod_C(1-z^{L(C)})$, which vanishes at $z=1$ to order exactly $c$. The $2$-factors with the fewest cycles contribute leading terms of one sign, so the sum has a zero of exactly that order at $z=1$. In particular it is not zero, and a good state exists. It remains to find one pair, which Hall's theorem does when $T$ has no separating triangle, and to cut $T$ along separating triangles. That cut is where the avoided edge is needed: the two halves can be joined only if their cycles avoid the same edge of the cut.
