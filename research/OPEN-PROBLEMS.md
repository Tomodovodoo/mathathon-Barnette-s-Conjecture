# Open problems

Notation and terms are those of [the paper](../paper/barnette.pdf). We write $q(s)$ for the number of cycles of $Q_s$, so that $s$ is good exactly when $q(s)=0$ (Lemma 3.1), and $g$ for the number of good states. Sizes are numbers of vertices of $T$. Names in brackets are files in [instances/](instances/README.md).

Proposition 3.5 gives a good state whenever a pair exists, without constructing one.

## 1. Monotone descent

A pair can be changed by two moves: reversing a cycle of $D(r,s)$, which keeps the 2-factor, and replacing $r$ by $r^K$ for a cycle $K$ of $Q_s$, which keeps $s$.

**Question.** From every pair, can a pair with good second state be reached by moves that never increase $q(s)$?

**Evidence.** Yes for all 193,623,384 pairs with at most 23 vertices, and for random pairs up to 200.

**False.**
- Some move always lowers $q(s)$: fails at 16 vertices [2-factor-without-good-state-16].
- A pair with lower $q$ is always within two moves: fails first at 21 vertices.
- Within three moves: fails at 40 vertices [lookahead-three-40]. Larger fixed numbers are open.
- Every 2-factor of $H$ has a pair with good second state: fails at 16 vertices [2-factor-without-good-state-16]. So the moves must change the 2-factor.

## 2. The exchange step for rainbow trees

Let $H^+$ be $H$ together with the roots and a point in $t_0$ joined to them. A *rainbow tree* is a map $\sigma\colon X\to A$, with $x$ a corner of $\sigma(x)$, such that removing the $n$ edges $x\sigma(x)$ from $H^+$ leaves a spanning tree. Its *excess* is $\sum_{t\in A}\bigl||\sigma^{-1}(t)|-1\bigr|$. The rainbow trees of excess zero are the inverses of the good states. A rainbow tree exists exactly when $T$ has a pair. An *exchange* moves one $x$ to another face at $x$; for each $x$ exactly one exchange gives a rainbow tree. See [sign-free](../proofs/sign-free/sign-free.pdf).

**Question.** Can every rainbow tree be brought to excess zero by exchanges that never increase the excess?

**Evidence.** Yes for every $t_0$ up to 17 vertices, and for most with 18.

**False.**
- Some exchange always lowers the excess: fails at 8 vertices.
- A fixed rule for choosing the next exchange suffices: the rule tried returns to its start after 48 exchanges at 38 vertices [walk-cycling-38].

## 3. Induction by contraction

A vertex $v\in X$ of degree four can be removed by identifying two opposite neighbours; $n$ drops by two. An induction along these contractions needs two statements, both open.

**Statement G.** If $T$ has no separating triangle and more than six vertices, then some $v\in X$ of degree four has a contraction that leaves a simple triangulation with a pair. Proved when $T$ has no chordless cycle of length five; true up to 19 vertices.

**Statement X.** If both contractions at such a vertex leave triangulations with good states, then a good state of one of them extends to a good state of $T$, possibly after a change on the remaining faces. True up to 18 vertices.

**False.**
- Every good state of the contracted triangulation extends: fails at 8 vertices.
- Some good state of a given contraction extends: fails at 18 vertices [no-lift-18].
- A state that does not extend can be changed within its 2-factor into one that does: fails at 18 vertices.
- Every contraction that leaves a simple triangulation leaves one with a pair: fails at 11 vertices.

## 4. At least $2^m$ good states

**Question.** If $T$ has a pair, is $g\ge 2^m$, with equality exactly when $H$ has only one 2-factor?

**Known.** $g$ is even and $g\ge 2m$. The bound $g\ge2^m$ is proved when $H$ has one 2-factor. It holds for all 4,656,948 choices of $T$ and $t_0$ up to 22 vertices, and up to 24 without separating triangles.

**False.** No rule tried selects a pair with good second state. The perfect matchings of $H$ form a distributive lattice, whose extreme elements may belong to no pair (10 vertices). So do the 2-factors of $H$, and neither the minimum nor the maximum need have a pair with good second state (18 vertices, the smallest example) [lattice-extremes-18]; nor need any join- or meet-irreducible element (33 vertices, with a separating triangle; open without one) [lattice-irreducibles-33].

## 5. Polynomial time

**Question.** Can a good state of a triangulation with a pair be found in polynomial time?

**Known.** $H$ has at most $3^{n/2}$ perfect matchings, and a search through them finds a good state in time $O(n^3\,3^{n/2})$. The exchange walk on pairs ends at a good state after at most $2^{O(n\log n)}$ moves; no polynomial bound is known. Both are in [algorithm](../proofs/algorithm/algorithm.md).

On chains of $k=1,\dots,8$ copies of the triangulation with 16 vertices [trap-chain-1 to trap-chain-4], one run took 0, 5, 14, 113, 562, 2811, 14060, 70309 moves. These counts depend on the first pair, on the arcs $\gamma_y$ and on the order of the faces. The package in [workings](../workings/README.md) does not reproduce them: its walk takes at most 15 moves for $k\le4$.

**False.** A choice of corners in some faces that extends to a state, and whose opposite sides are acyclic after the roots are identified, need not extend to a good state: 8 vertices [prefix-8, prefix-filtered-8]. So these two tests do not spare the search backtracking.

A positive answer to Question 1 or 2 would not give an algorithm: the search among moves that leave $q(s)$ or the excess unchanged also needs a bound.
