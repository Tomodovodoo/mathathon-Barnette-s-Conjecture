# Open problems

The theorem is proved. The questions below are open; each would give a simpler proof, a count, or an algorithm.

Setting. T is the dual triangulation with V vertices, its faces coloured black and white, and a white root face. A *state* picks one corner of each non-root white face, using each non-root vertex once. A *pair* is two states that disagree on every face; its *cover* is the set of cycles formed by the two chosen corners of each face, and m is the least number of cycles in a cover at this root. For a state s, q(s) is the number of cycles in its graph Q_s. A state is *good* when Q_s with the two root edges is a spanning tree, and a pair is good when one of its states is. Sizes below are V. Graphs named in brackets are in [instances/](instances/).

## 1. Monotone pair descent

**Question.** A pair can be changed by two moves: swap the two states along one cycle of the cover, or change the partner around one cycle of Q_s. From every pair, can a good pair be reached by moves that never increase q?

**Evidence.** True for all 193,623,384 pairs up to V = 23, and for every sampled pair up to V = 200.

**Refuted nearby.**
- Some move always lowers q: fails at V = 16 [cover-without-good-state-16].
- A lower q is always within two moves: fails first at V = 21.
- Within three moves: fails at V = 40 [lookahead-three-40]. Four moves, and any fixed bound, are open.
- Every cover contains a good state: fails at V = 16 [cover-without-good-state-16], so the moves must change the cover.

## 2. The rainbow exchange step

**Setting.** A rainbow tree is a spanning tree of the white-face graph that uses, for each non-root vertex, exactly one edge through that vertex. One exists exactly when no separating triangle has black faces along its inner side, and each lies in exactly one cover. Its *excess* is twice the number of black faces meeting two tree edges; excess zero means a good state.

**Question.** Can every rainbow tree be brought to excess zero by single-edge exchanges that never increase the excess?

**Evidence.** True at every root up to V = 17 and at most roots with V = 18.

**Refuted nearby.**
- Some exchange always lowers the excess: fails at V = 8.
- The deterministic walk that always evicts the first offending edge can cycle: V = 38, period 48 [walk-cycling-38].

## 3. The contraction induction

A degree-four vertex can be removed by merging two opposite neighbours. An induction on V along these contractions needs two lemmas.

**Lemma G (open).** Every triangulation without separating triangles and with V > 6 has a non-root vertex of degree four with a merge that leaves a simple triangulation admitting a pair. Proved without chordless 5-cycles; true up to V = 19.

**Lemma X (open).** If both merges at such a vertex leave triangulations with good states, then some good state downstairs lifts, possibly after a repair, to a good state upstairs. True up to V = 18.

**Refuted nearby.**
- Every good state downstairs lifts: fails at V = 8.
- Some good state downstairs lifts: fails at V = 18 [no-lift-18].
- A failed lift can be repaired inside the same cover: fails at V = 18. The repair must change the cover.
- Every simple contraction keeps a pair: fails at V = 11.

## 4. At least 2^m good states

**Question.** Does every root that admits a pair have at least 2^m good states, with equality exactly when there is one cover?

**Evidence.** The general bound is 2m. The bound 2^m is proved for one cover, and in a weak form for two. It holds at all 4,656,948 roots up to V = 22, and up to V = 24 without separating triangles.

**Refuted nearby.** No canonical choice finds a good pair: the extreme states of the lattice of states may have no partner (V = 10); the top and bottom of the lattice of covers may carry no good pair (V = 18, the smallest) [lattice-extremes-18]; nor need any irreducible element (V = 33, with a separating triangle; open without one) [lattice-irreducibles-33].

## 5. A polynomial-time algorithm

**Question.** Can a Hamiltonian cycle, or just a good pair, be found in polynomial time?

**Known.** Enumeration with matching repair runs in time O(q²(M+1)), where q = n/2 − 1 for a cubic graph on n vertices and M ≤ 3^(q/2) is the number of states. The marked walk of the constructive proof stops by a parity argument, with no polynomial bound.

**Evidence against the marked walk.** On trap chains with k = 1, …, 8 factors [trap-chain-1 to trap-chain-4] it takes 0, 5, 14, 113, 562, 2811, 14060, 70309 moves. Conjecture: (9·5^(k−2) − 2k + 9)/2 moves for k ≥ 4. No recurrence is proved.

**Refuted nearby.** A partial state that extends to a state need not extend to a good one, even after discarding every corner that alone closes a cycle: V = 8 [prefix-8, prefix-filtered-8]. So a matching oracle cannot guide the search.

Problems 1 and 2 alone would not give an algorithm: the search among moves that keep q or the excess equal also needs a polynomial bound.
