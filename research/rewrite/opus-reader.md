# A first reading of paper/barnette.tex

I read the draft once, as a graph theorist who knows the conjecture but none of the 2026 papers, and then checked every step. The proof holds up. One lemma is misstated, the introduction asserts one fact that nothing proves, and the body never says why a second state or a weight is needed. Line numbers refer to paper/barnette.tex at commit 06ebcfa.

## Must change

**Lemma 2.3 is false as stated (l.141, l.151).** The hypothesis allows a cycle Z that runs through two sides of one black face t meeting at r(t). The proof then opens with "The faces $t_f$ are distinct", which nothing in the hypothesis gives. All three uses (l.178, l.209) satisfy the missing condition, because M\*, Q_s and D(r,s) each contain one side of every black face.
Old: `Let $r$ be a state and let $Z$ be a cycle of $T$ of length $h$ such that, for every edge $f$ of $Z$,`
New: `Let $r$ be a state and let $Z$ be a cycle of $T$ of length $h$ that contains at most one side of each black face, such that, for every edge $f$ of $Z$,`
Old: `The faces $t_f$ are distinct, so` New: `The faces $t_f$ are distinct by hypothesis, so`
At l.209 add after "Lemma~\ref{lem:disk}": `, since $Q_s$ and $D(r,s)$ contain one side of each $t\in A$`. Do the same at l.178.

**The introduction asserts something the body never proves (l.55, used again at l.136).** The claim is "three trees, one through each corner of the black face $t_0$". I would not accept it as obvious. The proof takes one parity count. If a tree contained an end a of e_0 and the third root w, then the path between them together with the side aw of t_0 would form a cycle Z. Matching across Z gives B−W = b_P−w_P, while counting edges gives 3(B−W) = b_P−w_P−1, so 2(B−W) = −1. Add after l.55:
`(If one tree contained an end $a$ of $e_0$ and the third corner $w$, its path from $a$ to $w$ and the side $aw$ would bound a disk in which $M$ forces $B-W=b-w$ and an edge count forces $3(B-W)=b-w-1$, where $b$ and $w$ count the path edges with a black or a white face inside.)`
If that is too heavy for the introduction, l.136 must at least stop saying "we saw".

**Section 3 never says why there is a second state (l.189).** The motivation lives only in the introduction (l.69). Insert before l.189:
`By Proposition~\ref{prop:recover} it remains to find a good state. Whether $s$ is good depends on the cycles of $Q_s$, and a second state that differs from $s$ in every face directs $Q_s$ so that these cycles become directed cycles that can be reversed.`

**The weight is never motivated in the body (l.258).** A reader reaching "Choose a point $p_t$" does not know why. Insert at the start of the subsection:
`By Lemma~\ref{lem:sign}(2), reversing a cycle of $D(r,s)$ also changes the sign, so the pairs with a given $2$-factor cancel among themselves and $\sum\eps(r,s)=0$. We therefore weight each pair by a function of its second state that grows when a clockwise cycle of $D(r,s)$ is reversed.`

**The abstract is inaccurate (l.26).** "Encoded" suggests a bijection, which Remark l.433 denies. "Form a spanning forest" is not the condition.
New: `In the dual Eulerian triangulation, a Hamiltonian cycle can be built from a choice of one corner in each black face but one, using every other vertex once, for which the sides opposite the chosen corners and two sides of the remaining black face form a spanning tree.`

**Intro l.74.** "Reversing one of these cycles … raises" is false for counterclockwise cycles.
Old: `Reversing one of these cycles $C$ exchanges` New: `Reversing such a cycle $C$ from clockwise to counterclockwise exchanges`

**Lemma 4.1, l.356.** The sum over components needs all three roots in one component.
Old: `and the lemma follows by summing over the components.` New: `and, since the roots are pairwise adjacent and so lie in one component, the lemma follows by summing over the components.`

**Figure 1 caption (l.91).** The symbol $M_s$ is used nowhere else. Also, "The dual spanning tree of $G$" should read "The spanning tree $G-S_s^*$ of $G$".

## 1. The introduction

After reading it I could tell a colleague the following:

1. A Hamiltonian cycle avoiding e is the complement of a perfect matching M ∋ e whose dual M\* is acyclic in the Eulerian triangulation.
2. If we choose one corner in every black face but t_0, using each other vertex once, and the opposite sides plus two sides of t_0 form a spanning tree, then such an M is forced.
3. A second state disagreeing everywhere directs those sides so that each vertex has outdegree one. Every obstruction is then a directed cycle, and reversing it flips a sign, so a signed sum over pairs only sees good second states.
4. The same sum can also be grouped by the cycles r(t)→s(t). Reversing one of these flips the sign and raises a height-function weight by the number of white faces inside, so each group is ±z^ω∏(1−z^a).
5. Near z = 1 the groups with the fewest cycles dominate and all have the same sign, so the sum is not zero. A pair exists by a flow argument unless there is a separating triangle, where one glues.

The order is right. Three things were unclear:

- "rules out" (l.62) needs its reason, which is that the side of t in M\* contains s(t). Also write "the two sides of $t_0$ other than $e_0$".
- The disk identity is named twice (l.63, l.74) with no content. Give it once, in a clause: `a cycle along which every edge carries its face's chosen corner encloses one more white than black face`.
- l.80 "they all carry the same sign" needs a reason: the sign depends only on the number of cycles and how many run counterclockwise.

Replace "Here a second structure enters." (l.72) with `With $f=1$ the sum vanishes, for a reason that also shows how to choose $f$.` Then "although $Z(1)=0$" in l.81 is already explained.

The sentence "In the rest of this introduction we describe the argument." (l.47) can go.

## 2. Section by section

**Section 2.** Lemma 2.2 is one line. Fold it into the proof of Proposition 2.4 at l.173. At l.127, "a cycle can run clockwise" should be "a directed cycle runs clockwise". The disk identity arrives with r instead of s and no hint why. Add "(we state it for an arbitrary state $r$, as it will be applied to both states of a pair)". The proof of Proposition 2.4 is good, and the black-to-child matching is the nicest step in the paper.

**Section 3.** I re-read l.190. Q_s gets a direction that depends on r, but the notation does not show r. Say "directed by $r$". l.288 belongs inside the proof of Proposition 3.4, where it is used. l.328 is the key reason for working at z = 1, and it should come before the proof, not after it.

**Section 4.** Lemma 4.1 comes before anything that needs it. The reader meets e(U)−b(U) cold. Put Proposition 4.2 first and the density lemma after it, or open with `A pair is a $2$-factor of $H$; Hall's condition for it becomes, after complementation, the following edge count.` At l.360, "on its far side" made me stop. Use "outside it".

## 3. The core

The mechanism is visible, but only once Proposition 3.4 starts. The cancellation sits inside that proof, after the weight has been built. The intro tells it in the order sign, cancellation, weight, count. The body should follow the same order. Make the first paragraph of the proof of 3.4 a lemma right after Lemma 3.2: `For every function $f$ on states, $\sum\eps(r,s)f(s)$ over all pairs equals the same sum over the pairs in which $s$ is good.` OpenAI says it outright: "The cancellation works for arbitrary weights; we will choose them afterwards to establish nonvanishing."

The weight would read better as a sum of local weights, matching the sign as a product of local signs. Replace l.263–266 by:
`For $t\in A$ and a corner $v\in X$ of $t$ let $a(t,v)=\sum_y\cross{p_t\to v}{\gamma_y}$, the sum being over the white faces, and call $\omega(s)=\sum_{t\in A}a(t,s(t))$ the \emph{weight} of $s$.`
Move the Thurston sentence (l.289) to the head of the subsection. A reader who knows height functions then understands the definition before reading it.

Li's half-rays are easier to picture than arcs to t_0. "the half-ray of w intersects C an odd number of times if w is in the interior of C".

Lemma 3.3 convinced me. At l.278 add why the white faces inside are unchanged: `the region between an edge of $C$ and its detour through $p_t$ lies in the black face $t$`. The manuscript says it more carefully: "Each detour and the edge it replaces bound a triangular subdisk excluding the third corner."

## 4. Figures

Figure 1 is right in scope. In (d), use the same s as in (b) and draw Q_s directed by r, so the reader sees the forest oriented to the roots. Next to it, draw D(r,s). In the octahedron D(r,s) is the boundary of one white face, so a(C) = 1. Say so, and say that both states are good and give the cube's two Hamiltonian cycles avoiding e.

Figure 2: in (a), mark the left side of r(t)→s(t), so that δ_t can be read off. In (c), add one γ_y from a white face inside C, crossing Γ once from left to right. That is the picture I wanted most. No disk-identity figure is needed; it is a count.

Figure 3 is only worth its space if it shows the cancellation. Add a panel (c) with the non-good second state, its cycle K of Q_s, and its two first states.

## 5. Remarks and the example

The example is worth keeping if it says what it shows. Expanded, the polynomial is 1−z+z²−z³−z⁵+z⁷ times z^{ω0}. The z⁶ terms cancel, one from each 2-factor. That shows the involution changing the 2-factor, which the remark at l.436 relies on. Replace l.334 by:
`Expanded, $Z(z)=z^{\omega_0}(1-z+z^2-z^3-z^5+z^7)$. The two terms $z^6$, one from each $2$-factor, come from the two pairs with the same second state, which is not good; the six remaining monomials are the six good states.`

Two things are missing from the remarks. The first is that states are Tutte's states from trinity and Kauffman's clock theorem; OpenAI cites Hine–Kálmán, and it is in papers/. The second is the exact criterion in the manuscript, Theorem 1.2: a pair exists if and only if "no separating triangle has black inner boundary". That tells the reader how necessary the induction is.

At l.429, NP-completeness only shows non-Hamiltonian 2-connected examples exist if P ≠ NP. Cite an explicit example instead. The phase detail at l.421 is fine. At l.442, "We do not know either whether" should be "It is open whether".

## 6. Tone

Most of the prose is plain and good. These parts read like a report:

- l.45–47 and l.138 ("The argument needs a count that will be used again") describe the paper instead of doing the work.
- l.83 "Two points remain." and l.324 "up to a sign" are fine.

The manuscript has an opener I would borrow for l.50: "The difficulty is connectivity. A spanning subgraph of degree two at every vertex is a disjoint union of cycles. The task is to make it connected."

The title "The proof of Barnette's conjecture" reads as a claim to the proof. I suggest "Barnette's conjecture by a signed count of states" or "A short account of the proof of Barnette's conjecture". The abstract is five sentences, which is within the limit. Fix sentence four as above. Sentence five could drop "a generating function with" and read "a weight with one factor $1-z^{a}$ for every cycle".

## 7. From the sources

OpenAI's overview states the mechanism better than l.66–81: "We analyze one finite exponential sum over pairs in two different ways. First fix s. … To prove that the whole sum is nonzero, instead fix the undirected edge set D". The draft should say "the same sum, grouped two ways" in so many words, in the introduction and at l.310.

The manuscript has a cleaner wording of goodness: "We seek a tree matching, meaning that H − s is a spanning tree. The matching fixes the degrees of the retained graph; the tree condition ensures that it is connected." Here H is the full incidence graph, including t_0 and the roots. This is equivalent to the draft's definition and needs no special pair of sides of t_0. It would also shorten l.135 and the abstract.

Li's contribution is the half-ray picture cited in section 3.
