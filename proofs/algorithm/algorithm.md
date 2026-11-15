# Finding the cycle

Notation and terms are those of [the paper](../../paper/barnette.pdf). Proposition 6.9 shows that $T$ has a good state whenever it has a pair, without pointing to one. Two searches find one. They are stated here with their bounds. [workings/barnette](../../workings/README.md) implements Algorithm E with the test (2) below, and Algorithm W.

If $G$ has $N$ vertices, then $n=|A|=|X|=N/2-1$. A state $s$ is good when $Q_s$ is a forest with one root in each component; as $Q_s$ has $n$ edges and $n+3$ vertices, this holds exactly when $Q_s$ stays acyclic after the three roots are identified.

Let $H^+$ be the graph on the black faces and the vertices of $T$ in which a face is adjacent to its three corners; it contains $H$. For a state $s$, removing the $n$ edges $ts(t)$ from $H^+$ leaves $Q_s$ with every edge subdivided by its face, together with $t_0$ joined to the roots. This graph has $2n+4$ vertices and $2n+3$ edges, so $s$ is good exactly when it is connected.

Every other step of the proof takes polynomial time: the dual triangulation (Lemma 2.4), the matching $M$ and the cycle $G-M$ of a good state (Lemma 3.4 and Proposition 3.5), a pair by a flow (Proposition 4.6), and the cut along a separating triangle (Proposition 2.7), which replaces $n$ by two numbers with sum $n$. So it suffices to find a good state of a triangulation that has a pair.

## 1. Enumeration

**Lemma 1.** The number $M_T$ of states is at most $3^{n/2}$.

*Proof.* Let $K$ be the $n\times n$ matrix with $K_{t,x}=1$ when $x$ is a corner of $t$ and $0$ otherwise, for $t\in A$ and $x\in X$. The states are the nonzero terms of $\det K$. For two states $r,s$, each nontrivial cycle of the permutation $r(t)\mapsto s(t)$ of $X$ is a cycle of $T$ to which the disk identity (Lemma 5.1) applies, so its length is odd and the permutation is even. Hence all terms have the same sign and $M_T=|\det K|$. Each row of $K$ has at most three ones, so $|\det K|\le 3^{n/2}$ by Hadamard's inequality. ∎

**Algorithm E.** Go through the faces of $A$ in a fixed order and choose a corner in each, depth first. Keep a partial choice only if

1. it extends to a state, that is, the remaining faces have a perfect matching in $H$ to the remaining vertices, and
2. the sides opposite the corners chosen so far are acyclic after the roots are identified.

Stop at the first complete choice.

The second test can be replaced by another: a partial choice, as a set $S$ of edges of $H$, is kept if (1) holds and

2′. $H^+-S$ is connected.

**Theorem 2.** If $T$ has a pair, Algorithm E returns a good state after $O(n^3M_T)$ steps, in polynomial space, and so does the search with (2′) in place of (2). Hence a Hamiltonian cycle of $G$ that avoids a given edge is found in time $3^{N/4}$ up to a polynomial factor, in polynomial space.

*Proof.* A complete choice that satisfies (1) is a state, and it satisfies (2), or (2′), exactly when it is good. Every part of a good state satisfies (1), (2) and (2′), since a subgraph of a forest is a forest and removing fewer edges leaves a connected graph connected. A good state exists by Proposition 6.9. Each partial choice that is kept lies in a state, and a state contains $n+1$ of them, so at most $(n+1)M_T$ are kept. Each has at most three children; a test for a perfect matching takes $O(n^2)$ steps, and (2) and (2′) take $O(n)$. The cuts along separating triangles give at most $n$ triangulations, each with at most $3^{n/2}<3^{N/4}$ states. ∎

Neither of (2) and (2′) implies the other, and (1), (2) and (2′) together do not imply that a good state extends the choice. Take the dual of the hexagonal prism, with vertices $0,\dots,7$, roots $0,3,4$ and

```
a = {0,1,2},  b = {1,4,5},  c = {1,6,7},  d = {2,7,3},  e = {3,6,5}
```

as the faces in $A$ (`examples.eight_vertex_example()`). Its states, as corners chosen in $a,b,c,d,e$, are $(1,5,7,2,6)$, $(2,1,6,7,5)$ and $(2,5,1,7,6)$. The first two are good. For the third, $Q_s$ has the edges $01$, $14$, $67$, $23$, $35$; it joins the roots $0$ and $4$ and leaves $\{6,7\}$ without a root. All three choices below lie in the third state only, so (1) holds and no good state extends them.

- The corner $1$ in $c$ satisfies (2) and (2′).
- The corners $2$ in $a$ and $5$ in $b$ satisfy (2′) but not (2): the sides $01$ and $14$ join the roots $0$ and $4$.
- The corners $1$ in $c$, $7$ in $d$ and $6$ in $e$ satisfy (2), with the sides $67$, $23$, $35$, but not (2′): the vertices $6$ and $7$ lie on no black face other than $c$, $d$, $e$, so removing the three edges separates $c$, $6$ and $7$ from the rest of $H^+$.

In the triangulation of Figure 2 of the paper (`examples.running_example()`, 13 vertices), with the faces in the order of the package, 89 choices of corners in the first $j$ faces, $0\le j\le n$, satisfy (1); of these, 9 satisfy (2′) but not (2), and 2 satisfy (2) but not (2′) (computed).

## 2. The exchange walk

For $t\in A$ and a corner $v\in X$ of $t$ let $\omega(t,v)$ be the local weight of the paper, and put $\alpha(t,v)=\omega(t,v)-\mu_t$ for integers $\mu_t\le\min_w\omega(t,w)$, so that $\alpha\ge0$. For a cycle $C$ of $D(r,s)$ let $L(C)$ be the sum of $\alpha(t,s(t))$ over the faces $t$ with a side on $C$. Reversing a clockwise cycle $C$ raises $L(C)$ by $a(C)\ge1$ (Lemma 6.6); we write $L^+$ and $L^-$ for the values of $L(C)$ when $C$ runs counterclockwise and clockwise, so $L^+>L^-$.

A *token* is a pair $(t,j)$ with $1\le j\le\alpha(t,s(t))$; it lies on the cycle of $D(r,s)$ with a side on $t$. The tokens on $C$, ordered by face and then by $j$, form the *pool* of $C$, of size $L^+$ or $L^-$. A *marked pair* is a pair together with a list of $h$ tokens. Cycles are ordered by their first faces.

- $\beta$: replace $r$ by $r^K$ for the first cycle $K$ of $Q_s$, keeping the tokens. A marked pair is fixed when $Q_s$ has no cycle, that is, when $s$ is good (Lemma 5.5(1)).
- $\alpha$: if some cycle of $D(r,s)$ carries no token, reverse the first such cycle. Otherwise take the first cycle all of whose tokens have rank at most the size of the pool of the reversed cycle, reverse it, and move each token to the same rank in that pool. A marked pair is fixed when no cycle qualifies.

Both are involutions: $\beta$ because $s$ and the order of the cycles of $Q_s$ do not change, $\alpha$ because the cycle chosen qualifies again after the move and the earlier cycles are untouched. A clockwise cycle always qualifies, so at a fixed point of $\alpha$ every cycle runs counterclockwise and carries a token, and the number $c$ of cycles is at most $h$.

**Algorithm W.** Given a pair, repeat: reverse the clockwise cycles of $D(r,s)$; let $h$ be the number of cycles, and put on each cycle the token of rank $L^-+1$; apply $\beta,\alpha,\beta,\dots$ until $\beta$ fixes the marked pair, in which case $s$ is good and the algorithm stops, or $\alpha$ does, in which case it starts again from this pair.

**Theorem 3.** Algorithm W stops, at a pair with good second state, after $2^{O(n\log n)}$ moves.

*Proof.* The marked pairs with $h$ tokens, joined by the moves of $\alpha$ and $\beta$, form a graph of maximum degree two. The start of a round is fixed by $\alpha$, so it is an end of a path, which the walk follows to its other end. If that end is fixed by $\beta$, we are done. Otherwise it is fixed by $\alpha$, the path has an odd number of edges, each of which changes the sign (Lemmas 5.5(2) and 6.2(3)), and so its ends have opposite signs. At both ends all cycles run counterclockwise, so the sign is $(-1)^{(n+c)/2+c}$ with $c\equiv n\pmod 2$ (Lemma 6.2(3)). Hence the two numbers of cycles differ by $2$ modulo $4$; the start has $h$ cycles and the end at most $h$, hence at most $h-2$. As $h\le n/3$, there are at most $n/6+1$ rounds.

A round visits each marked pair at most once. There are at most $6^n$ pairs. If every arc $\gamma_y$ follows a path of a spanning tree of $G$ from $y$ to $t_0$, it passes through each face at most once, so $|\omega(t,v)|\le n+1$, and with $\mu_t=\min_w\omega(t,w)$ each of the $h$ tokens takes at most $2n(n+1)$ values. ∎

No polynomial bound on the number of moves is known. The first step of Algorithm W leaves a pair that is determined by its 2-factor, so the number of moves depends on the 2-factor of the first pair, on the arcs $\gamma_y$, on the order of the faces, and on which of the two drawings of $T$, mirror images of each other, is used.

The counts that follow are computed with `exchange_walk` of `workings/barnette`. There $\gamma_y$ follows the path from $y$ to $t_0$ in a breadth-first tree of $G$, $\mu_t=\min_w\omega(t,w)$, and a move is one application of $\beta$ or $\alpha$. The triangulations are stored in [research/instances](../../research/instances/README.md), which says how to repeat the runs.

- On the triangulation with 16 vertices `examples.trap()` the walk takes at most $3$ moves from each of the 18 pairs.
- `trap-chain-k`, for $k=1,\dots,10$, consists of $k$ copies of this triangulation, the roots of each further copy being the corners of a white face of the copy before; it has $13k+3$ vertices. From the pair stored with it the walk takes

  $$0,\ 3,\ 24,\ 113,\ 562,\ 2811,\ 14060,\ 70309,\ 351558,\ 1757807$$

  moves. For $4\le k\le10$ this is $(9\cdot5^{k-2}-2k+9)/2$, of order $5^{n/13}$. With two other breadth-first trees the counts for $3\le k\le8$ were the same.
- In the mirror image of `trap-chain-k`, with the same pair and the same order of faces, the walk takes $3$ moves for every $k\le10$, and $5$ moves for $k\le8$ if the arcs are the mirror images of those used before.
- The second state of the stored pair is good, for every $k$. Algorithm W does not look at $Q_s$ before it reverses the clockwise cycles, and after that step the second state is no longer good for $k\ge2$.

So Algorithm W as stated needs exponentially many moves on this family if the formula persists. This is not proved, and it says nothing about a walk that makes other choices: here a pair with good second state has the same 2-factor as the first pair.

## 3. Bounded width

A good state is a set $S$ of edges of $H$, one at each face of $A$ and one at each vertex of $X$, such that $H^+-S$ is connected. If $T$ has a tree decomposition of width $w$, then $H^+$ has one of width at most $\max(w,3)$: the corners of a black face are pairwise adjacent in $T$, so they lie in a common bag, and a new bag that consists of the face and its corners is attached to that bag.

The condition on $S$ can be written in monadic second-order logic with quantification over sets of edges. By Courcelle's theorem (*Inform. and Comput.* 85 (1990), 12–75) it is then decided in time $f(w)\,n$, given the decomposition, whether a good state contains a given set of edges, and choosing the corners face by face finds a good state in time $f(w)\,n^2$. We quote this theorem and have not checked that it applies in this form. No explicit dynamic programme is proved in this note, and `workings/barnette` contains none.

## 4. Polynomial time

Algorithms that use nothing from the proof have better bounds than Theorems 2 and 3. Eppstein finds a Hamiltonian cycle through given edges in a graph with $N$ vertices and maximum degree three in time $O(2^{N/3})$ and linear space (*J. Graph Algorithms Appl.* 11 (2007), 61–81); applied to $G-e$ this is faster than $3^{N/4}$, since $2^{1/3}<3^{1/4}$. For planar graphs with $N$ vertices, Dorn, Penninkx, Bodlaender and Fomin state the bound $O(2^{6.903\sqrt N})$ for a Hamiltonian cycle of least weight (*Algorithmica* 58 (2010), 790–810). Both bounds are taken from the abstracts, the second from that of the technical report UU-CS-2006-006 of the same title; the papers are not in `papers/` and their proofs were not read.

It is open whether a good state, or a Hamiltonian cycle of a cubic, bipartite, 3-connected planar graph, can be found in polynomial time. The triangulation `examples.trap()` has pairs from which no reversal of a cycle of $D(r,s)$ or of $Q_s$ lowers the number of cycles of $Q_s$, and a 2-factor of $H$ none of whose pairs has a good second state; see [the open problems](../../research/OPEN-PROBLEMS.md).
