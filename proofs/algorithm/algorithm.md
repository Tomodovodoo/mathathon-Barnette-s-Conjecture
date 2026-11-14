# Finding the cycle

Notation and terms are those of [the paper](../../paper/barnette.pdf). Proposition 4.9 shows that $T$ has a good state whenever it has a pair, without pointing to one. The anonymous manuscript *A constructive proof of Barnette's conjecture* (`papers/barnette_trees.pdf`, cited as [C]) finds one by two searches. They are stated here with their bounds, and both are implemented in [workings/barnette](../../workings/README.md).

If $G$ has $N$ vertices, then $n=|A|=|X|=N/2-1$. A state $s$ is good when $Q_s$ is a forest with one root in each component; as $Q_s$ has $n$ edges and $n+3$ vertices, this holds exactly when $Q_s$ stays acyclic after the three roots are identified.

Every other step of the proof takes polynomial time: the dual triangulation (Lemma 2.4), the matching $M$ and the cycle $G-M$ of a good state (Lemma 2.11 and Proposition 2.12), a pair by a flow (Proposition 5.5), and the cut along a separating triangle (Theorem 5.6), which replaces $n$ by two numbers with sum $n$. So it suffices to find a good state of a triangulation that has a pair.

## 1. Enumeration

**Lemma 1** ([C]). The number $M_T$ of states is at most $3^{n/2}$.

*Proof.* Let $K$ be the $n\times n$ matrix with $K_{t,x}=1$ when $x$ is a corner of $t$ and $0$ otherwise, for $t\in A$ and $x\in X$. The states are the nonzero terms of $\det K$. For two states $r,s$, each nontrivial cycle of the permutation $r(t)\mapsto s(t)$ of $X$ is a cycle of $T$ to which the disk identity (Lemma 2.9) applies, so its length is odd and the permutation is even. Hence all terms have the same sign and $M_T=|\det K|$. Each row of $K$ has at most three ones, so $|\det K|\le 3^{n/2}$ by Hadamard's inequality. ∎

**Algorithm E.** Go through the faces of $A$ in a fixed order and choose a corner in each, depth first. Keep a partial choice only if

1. it extends to a state, that is, the remaining faces have a perfect matching in $H$ to the remaining vertices, and
2. the sides opposite the corners chosen so far are acyclic after the roots are identified.

Stop at the first complete choice.

**Theorem 2** ([C], Proposition 6.2 and Theorem 1.1). If $T$ has a pair, Algorithm E returns a good state after $O(n^3M_T)$ steps, in polynomial space. Hence a Hamiltonian cycle of $G$ that avoids a given edge is found in time $3^{N/4}$ up to a polynomial factor, in polynomial space.

*Proof.* A complete choice that satisfies (2) is a good state, every part of a good state satisfies (1) and (2), and a good state exists by Proposition 4.9. Each partial choice that is kept lies in a state, and a state contains $n+1$ of them, so at most $(n+1)M_T$ are kept. Each has at most three children, and a test for a perfect matching takes $O(n^2)$ steps. The cuts along separating triangles give at most $n$ triangulations, each with at most $3^{n/2}<3^{N/4}$ states. ∎

Conditions (1) and (2) do not imply that a good state extends the choice. Take the dual of the hexagonal prism, with vertices $0,\dots,7$, roots $0,3,4$ and

```
a = {0,1,2},  b = {1,4,5},  c = {1,6,7},  d = {2,7,3},  e = {3,6,5}
```

as the faces in $A$ (`examples.eight_vertex_example()`). Its states, as corners chosen in $a,b,c,d,e$, are $(1,5,7,2,6)$, $(2,1,6,7,5)$ and $(2,5,1,7,6)$. The first two are good. For the third, $Q_s$ has the edges $01$, $14$, $67$, $23$, $35$; it joins the roots $0$ and $4$ and leaves $\{6,7\}$ without a root. Choosing the corner $1$ in $c$ satisfies (1) and (2), and the only state with this corner is the third.

## 2. The exchange walk

For $t\in A$ and a corner $v\in X$ of $t$ let $\omega(t,v)$ be the local weight of the paper, and put $\alpha(t,v)=\omega(t,v)-\mu_t$ for integers $\mu_t\le\min_w\omega(t,w)$, so that $\alpha\ge0$. For a cycle $C$ of $D(r,s)$ let $L(C)$ be the sum of $\alpha(t,s(t))$ over the faces $t$ with a side on $C$. Reversing a clockwise cycle $C$ raises $L(C)$ by $a(C)\ge1$ (Lemma 4.6); we write $L^+$ and $L^-$ for the values of $L(C)$ when $C$ runs counterclockwise and clockwise, so $L^+>L^-$.

A *token* is a pair $(t,j)$ with $1\le j\le\alpha(t,s(t))$; it lies on the cycle of $D(r,s)$ with a side on $t$. The tokens on $C$, ordered by face and then by $j$, form the *pool* of $C$, of size $L^+$ or $L^-$. A *marked pair* is a pair together with a list of $h$ tokens. Cycles are ordered by their first faces.

- $\beta$: replace $r$ by $r^K$ for the first cycle $K$ of $Q_s$, keeping the tokens. A marked pair is fixed when $Q_s$ has no cycle, that is, when $s$ is good (Lemma 3.4(1)).
- $\alpha$: if some cycle of $D(r,s)$ carries no token, reverse the first such cycle. Otherwise take the first cycle all of whose tokens have rank at most the size of the pool of the reversed cycle, reverse it, and move each token to the same rank in that pool. A marked pair is fixed when no cycle qualifies.

Both are involutions: $\beta$ because $s$ and the order of the cycles of $Q_s$ do not change, $\alpha$ because the cycle chosen qualifies again after the move and the earlier cycles are untouched. A clockwise cycle always qualifies, so at a fixed point of $\alpha$ every cycle runs counterclockwise and carries a token, and the number $c$ of cycles is at most $h$.

**Algorithm W.** Given a pair, repeat: reverse the clockwise cycles of $D(r,s)$; let $h$ be the number of cycles, and put on each cycle the token of rank $L^-+1$; apply $\beta,\alpha,\beta,\dots$ until $\beta$ fixes the marked pair, in which case $s$ is good and the algorithm stops, or $\alpha$ does, in which case it starts again from this pair.

**Theorem 3** ([C], Theorem 5.3). Algorithm W stops, at a pair with good second state, after $2^{O(n\log n)}$ moves.

*Proof.* The marked pairs with $h$ tokens, joined by the moves of $\alpha$ and $\beta$, form a graph of maximum degree two. The start of a round is fixed by $\alpha$, so it is an end of a path, which the walk follows to its other end. If that end is fixed by $\beta$, we are done. Otherwise it is fixed by $\alpha$, the path has an odd number of edges, each of which changes the sign (Lemmas 3.4(2) and 4.2(3)), and so its ends have opposite signs. At both ends all cycles run counterclockwise, so the sign is $(-1)^{(n+c)/2+c}$ with $c\equiv n\pmod 2$ (Lemma 4.2(3)). Hence the two numbers of cycles differ by $2$ modulo $4$; the start has $h$ cycles and the end at most $h$, hence at most $h-2$. As $h\le n/3$, there are at most $n/6+1$ rounds.

A round visits each marked pair at most once. There are at most $6^n$ pairs. If every arc $\gamma_y$ follows a path of a spanning tree of $G$ from $y$ to $t_0$, it passes through each face at most once, so $|\omega(t,v)|\le n+1$, and with $\mu_t=\min_w\omega(t,w)$ each of the $h$ tokens takes at most $2n(n+1)$ values. ∎

No polynomial bound on the number of moves is known. The number depends on the first pair, on the arcs $\gamma_y$ and on the order of the faces. With the choices of `workings/barnette`, the walk takes at most $3$ moves from each of the 18 pairs of the triangulation with 16 vertices `examples.trap()`, and $15$ moves from the first pair on chains of two, three and four copies of it (`research/instances/trap-chain-2` to `trap-chain-4`).

## 3. Bounded width

A good state is a set $S$ of edges of $H$, one at each face of $A$ and one at each vertex of $X$, such that removing $S$ from $H$ together with the roots and a point in $t_0$ joined to them leaves a spanning tree: contracting each face of $A$ onto its side opposite the chosen corner turns this graph into $Q_s$ with the roots identified. If $T$ has treewidth $w$, then this graph has treewidth at most $\max(w,3)$, and the standard dynamic programme for spanning trees with prescribed degrees finds $S$ in time $f(w)\,n$. Independently of the proof, a Hamiltonian cycle of the planar graph $G-e$ is found in time $2^{O(\sqrt N)}$ (Dorn, Penninkx, Bodlaender and Fomin, *Algorithmica* 58 (2010), 790–810).

## 4. Polynomial time

It is open whether a good state, or a Hamiltonian cycle of a cubic, bipartite, 3-connected planar graph, can be found in polynomial time. The triangulation `examples.trap()` has pairs from which no reversal of a cycle of $D(r,s)$ or of $Q_s$ lowers the number of cycles of $Q_s$, and a 2-factor of $H$ none of whose pairs has a good second state; see [the open problems](../../research/OPEN-PROBLEMS.md).
