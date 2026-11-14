# Finding the cycle

The paper shows that a good state exists whenever a pair exists, without pointing to one. The anonymous manuscript *A constructive proof of Barnette's conjecture* (`papers/barnette_trees.pdf`, cited as [A]) finds one by two searches, stated here with their proved bounds and implemented in `workings/barnette/`.

In the paper's notation, `n = |A| = |X| = N/2 - 1` when `G` has `N` vertices. A state `s` is good when `Q_s` is a forest with one root in each component; as `Q_s` has `n` edges on `n + 3` vertices, this means that `Q_s` stays acyclic when the three roots are identified.

The other steps of the proof take polynomial time, and a cut along a separating triangle splits `n` as `n1 + n2`. So it suffices to find a good state in a triangulation that has a pair.

## 1. Enumeration

**Lemma 1** ([A]). The number `M` of states is at most `3^(n/2)`.

*Proof.* Let `K(t,x)` be `1` when `x` is a corner of `t` and `0` otherwise. The states are the nonzero terms of `det K`. For two states `r, s`, each nontrivial cycle of the permutation `r(t) -> s(t)` is a directed cycle of sides leaving corners chosen by `r`, so by the disk identity its length is odd and it is an even permutation. Hence all terms have the same sign and `M = |det K|`. Each row of `K` has at most three ones, so `|det K| <= 3^(n/2)` by Hadamard's inequality. ∎

**Algorithm E.** Go through the faces of `A` in a fixed order and choose a corner in each, depth first. Keep a partial choice only if

1. it extends to a state (the remaining faces have a perfect matching to the remaining vertices), and
2. the opposite sides chosen so far are acyclic after the roots are identified.

Stop at the first complete choice.

**Theorem 2** ([A], Proposition 6.2, Theorem 1.1). If `T` has a pair, Algorithm E returns a good state in `O(n^3 M)` steps and polynomial space. Hence a Hamiltonian cycle of `G` avoiding a given edge is found in time `poly(N) * 3^(N/4)` and polynomial space.

*Proof.* A complete choice satisfying (2) is a good state, every part of a good state satisfies (1) and (2), and a good state exists by the paper. Each partial choice kept lies in a state, and a state contains `n + 1` of them, so at most `(n + 1) M` are kept. Each has at most three children, and a matching test costs `O(n^2)`. Finally there are at most `n` pieces, each with at most `3^(n/2) < 3^(N/4)` states. ∎

Conditions (1) and (2) do not imply that a good state extends the choice. Take the dual of the hexagonal prism, with vertices `0,...,7`, root face `{0,3,4}` and

```
a = {0,1,2},  b = {1,4,5},  c = {1,6,7},  d = {2,7,3},  e = {3,6,5}.
```

Its states, as corners chosen in `a, b, c, d, e`, are `(1,5,7,2,6)`, `(2,1,6,7,5)` and `(2,5,1,7,6)`. The first two are good. For the third, `Q_s = {01, 14, 67, 23, 35}` joins the roots `0` and `4` and leaves `{6,7}` without a root. Choosing the corner `1` in `c` satisfies (1) and (2), and its only completion is the third state.

## 2. The exchange walk

Let `kappa(t,v)` be the sum of `kappa_y(t,v)` over the white faces `y`, and `a(t,v) = kappa(t,v) - min_w kappa(t,w)`. For a cycle `C` of `D` let `L+` and `L-` be the sums of `a(t, head of C in t)` when `C` runs counterclockwise and clockwise. By the height lemma `L+ - L-` is the number of white faces inside `C`, so `L+ > L-`.

A *token* is a pair `(t,j)` with `1 <= j <= a(t,s(t))`; it lies on the cycle of `D` through `t`. The tokens on `C`, ordered by face and then by `j`, form its *pool*, of size `L+` or `L-`. A *marked pair* is a pair with a list of `h` tokens. Cycles are ordered by their earliest faces.

- `beta`: reverse the first cycle of `Q_s`, keeping the tokens. Fixed when there is none, that is, when `s` is good.
- `alpha`: if some cycle of `D` carries no token, reverse the first such cycle. Otherwise take the first cycle whose tokens all have rank at most the size of the opposite pool, reverse it, and move each token to the same rank in the opposite pool. Fixed when no cycle qualifies.

Both are involutions: `beta` because `s` is unchanged, `alpha` because the selected cycle qualifies again after the move and the earlier cycles are untouched. A clockwise cycle always qualifies, so at a fixed point of `alpha` every cycle is counterclockwise and carries a token, and the number `c` of cycles is at most `h`.

**Algorithm W.** Given a pair, repeat: reverse the clockwise cycles of `D`; let `h` be the number of cycles and put on each cycle the token of rank `L- + 1`; apply `beta, alpha, beta, ...` until `beta` fixes the marked pair (stop: `s` is good) or `alpha` does (repeat from this pair).

**Theorem 3** ([A], Theorem 5.3). Algorithm W stops at a pair with good second state after `2^(O(n log n))` moves.

*Proof.* The marked pairs with `h` tokens, joined by the moves of `alpha` and `beta`, form a graph of maximum degree two. The start of a round is fixed by `alpha`, so it is an end of a path, which the walk follows to its other end. If that end is fixed by `beta`, we are done. Otherwise it is fixed by `alpha`, the path has an odd number of edges, each a reversal, and its ends have opposite signs `eps`. At both ends all cycles are counterclockwise, and there the sign lemma gives `eps = (-1)^((n+c)/2) (-1)^c` with `c ≡ n (mod 2)`. So the two numbers of cycles differ by `2 (mod 4)`; the start has `h` cycles and the end at most `h`, hence at most `h - 2`. As `h <= n/3`, there are at most `n/6 + 1` rounds.

A round visits each marked pair at most once. There are at most `6^n` pairs, and as `|kappa(t,v)| <= n + 1`, each of the `h` tokens takes at most `2n(n+1)` values. ∎

## 3. Bounded width

Let `H` join every black face to its three corners. A good state is a set `S` of edges of `H`, one at each face of `A` and each vertex of `X`, with `H - S` a spanning tree, since contracting each face of `A` onto its opposite side turns `H - S` into `Q_s` with the roots identified. If `T` has treewidth `w`, then `H` has treewidth at most `max(w,3)`, and the standard dynamic programme for spanning trees with prescribed degrees finds `S` in time `f(w) * n`. Independently of the proof, a Hamiltonian cycle of the planar graph `G - e` is found in time `2^(O(sqrt N))` (Dorn et al., *Algorithmica* 58 (2010), 790-810).

## 4. Polynomial time?

It is open whether the cycle can be found in polynomial time. The conjecture below is the only unproved statement of this note.

A triangulation with 16 vertices (`examples.trap()`) has pairs from which no single reversal lowers the number of cycles of `Q_s`. Glue `k` copies in a chain, each inside a white face of the previous one. For one choice of first pair, weights and face order, Algorithm W was observed to take

```
0, 5, 14, 113, 562, 2811, 14060, 70309
```

moves for `k = 1,...,8`.

**Conjecture.** For that choice the number of moves is `(9 * 5^(k-2) - 2k + 9)/2` for all `k >= 4`, as it is for `4 <= k <= 8`.

With the weights `a` above and the first pair of `workings/barnette`, the walk on such chains ends without a move.
