# The complexity of finding the cycle

Status tags as in `research/BRIEF.md`. Nothing here is refereed. The citations to the complexity literature are from memory. I did not open those papers in this session, and each such citation says so.

## The paragraph for the exposition

> The proof is constructive only in a weak sense. For a Barnette graph on `N` vertices the known algorithms are exhaustive: a search over the incidence matchings, of which there are at most `3^{N/4}`, and a walk driven by two involutions whose length is only bounded by `2^{O(N log N)}`. Both use polynomial space. No polynomial-time algorithm is known, and no hardness result is known either. Hardness in the usual sense is not to be expected: the cycle always exists and is easy to check, so the search problem is total, and a total search problem cannot be NP-hard unless NP = coNP. The involutions do place the problem in a recognised class of total problems. Following the walk is an instance of "given a source of a directed graph of paths and cycles, find a sink", so the problem lies in PPADS, a subclass of PPP. We do not know whether it lies in PPAD, in PPA or in PLS. In practice local search is fast. On every instance we tried, a few exchange moves that never increase the number of cycles of `Q_s` reach a tree matching. We could not prove that such moves always exist, and we show that the simplest rules for choosing them fail: a single move can be stuck from 16 vertices on, two moves from 21, three moves from 60.

Each sentence is justified below.

## 1. The search problems

**BARNETTE-HC.** Input: a simple graph `G`. Output: a Hamiltonian cycle of `G`, or the statement that `G` is not cubic, bipartite, planar and 3-connected. The four properties are decidable in polynomial time, so by Theorem 1.1 of the OpenAI paper every input has an output that can be checked in polynomial time. The problem is in TFNP (`LIT`, conditional on that theorem: Megiddo and Papadimitriou, On total functions, existence theorems and computational complexity, Theoret. Comput. Sci. 81 (1991), define the class. Cited from memory).

**TREE-PAIR.** Input: a rooted Eulerian triangulation `T` and a pair `(r, s)`. Output: a pair `(r', s')` with `Q_{s'}` a forest. Total by Theorem 5.2 of the trees paper. A pair is found by one maximum flow when it exists (OpenAI, Proposition 3.1), and a tree pair gives the cycle in linear time (OpenAI, Section 6). BARNETTE-HC reduces to polynomially many instances of TREE-PAIR, one per piece of the decomposition along separating triangles (trees paper, Section 7. `LIT`).

**Hardness.** A problem in TFNP is not FNP-hard under the usual reductions unless NP = coNP (`LIT`, Megiddo and Papadimitriou 1991, cited from memory). The decision problem is trivial. Without 3-connectivity the picture changes: the Hamiltonian cycle problem is NP-complete for 2-connected cubic planar bipartite graphs (`LIT`, Akiyama, Nishizeki and Saito, NP-completeness of the Hamiltonian cycle problem for bipartite graphs, J. Inform. Process. 3 (1980). Cited from memory, not opened). So 3-connectivity is exactly what turns an NP-complete problem into a total one.

## 2. What is proved about running time

| Algorithm | Bound | Source |
| --- | --- | --- |
| Depth-first search over extendable matching prefixes | `O(n^3 M)` time with `M = \|det K_B\| <= 3^{n/2}`, polynomial space; `n = N/2 - 1` | `LIT`, trees paper, Lemma 6.1 and Proposition 6.2 |
| Marked walk (two involutions, restarts) | `2^{O(n log n)}` moves, polynomial space | `LIT`, trees paper, Theorem 5.3 |
| Breadth-first search in the exchange graph | exponential time and space | `LIT`, trees paper, Theorem 5.2 |

All three are preprints. `COMPUTED` here: the exchange graph always contained a tree pair in every component (49,331,840 pairs, all rooted instances with `V <= 22`, `code/descent.exe` aborts otherwise).

## 3. The class given by the involutions: PPADS

The classes (`LIT`, from memory): PPAD is defined by END-OF-LINE, "given a directed graph of in- and out-degree at most one by circuits for successor and predecessor, and a source, find another source or a sink" (Papadimitriou, J. Comput. System Sci. 48 (1994)). PPADS is defined by the same data with the task "find a sink" (named in Beame, Cook, Edmonds, Impagliazzo and Pitassi, The relative complexity of NP search problems, J. Comput. System Sci. 57 (1998)). PPA is the undirected version, "given a leaf, find another leaf". PPAD is contained in PPA and in PPADS, and PPADS in PPP.

**Proposition G.** `PROVED-HERE`, conditional on Theorem 5.3 of the trees paper and the facts in its proof (`alpha` and `beta` are involutions of `Omega_m`, every non-fixed move reverses the sign, and (12)). TREE-PAIR is in PPADS.

*Proof.* Fix the weights and orders of the trees paper, all computable in polynomial time. For `m >= 1`, `Omega_m` is the set of pairs with an ordered list of `m` tokens. An element has a polynomial-size description. Let `sigma_m = (-1)^{(n - m)/2}`. Make `Omega_m` a digraph: a `beta`-edge `{x, beta(x)}` is directed from its end of sign `sigma_m` to its end of sign `-sigma_m`, an `alpha`-edge from sign `-sigma_m` to sign `sigma_m`. The two ends of an edge have opposite signs, so this is well defined. A vertex of sign `sigma_m` has at most one out-edge (`beta`) and one in-edge (`alpha`). A vertex of sign `-sigma_m` has at most one in-edge (`beta`) and one out-edge (`alpha`). The sinks are of two kinds.

- (K1) `beta`-fixed, not `alpha`-fixed, of sign `sigma_m`. These are tree pairs with marks.
- (K2) `alpha`-fixed, not `beta`-fixed, of sign `-sigma_m`. By (12) such a vertex has `c <= m` cycles and sign `(-1)^{(n - c)/2}`, so `c = m + 2 (mod 4)` and `c <= m - 2`.

The constructor's start for a pair with `m` cycles (all cycles counterclockwise, the token of rank `L^- + 1` on each) is `alpha`-fixed of sign `sigma_m`. If it is `beta`-fixed the pair is a tree pair. Otherwise it is a source.

Now join the levels. A vertex of the big graph is a triple `(m, x, h)`: a level, an element `x` of `Omega_m`, and a history `h`, a list of at most `n/6` earlier vertices `(m_1, x_1), ..., (m_j, x_j)` with `m_1 > ... > m_j > m`. Inside a fixed `(m, h)` keep the edges of level `m`. For every sink `x` of kind (K2) at level `m` and every history `h` add the edge

    (m, x, h)  ->  (c(x), start(x), h + (m, x)),

where `c(x)` is the number of `D`-cycles of `x` and `start(x)` is the constructor's start for the pair of `x`. The target is a source of its level: it is `alpha`-fixed of sign `sigma_{c(x)}`, and it is not `beta`-fixed because `x` is not and being `beta`-fixed depends only on the pair. The added edge is its only in-edge, and the map is injective because the target records `(m, x)`. So in- and out-degrees are still at most one, and successor and predecessor are computable in polynomial time (to find the predecessor of a level start, look at the last entry of the history and test that it is a (K2) sink).

Every (K2) sink now has an out-edge. The sinks of the big graph are exactly the (K1) vertices of all levels, and each of them carries a tree pair. Given the input pair with `m_0` cycles, either its normalised form is a tree pair, or `(m_0, start, empty)` is a source of the big graph. So TREE-PAIR reduces to "given a source, find a sink". ∎

**What this does not give.**

- **PPAD.** `PROVED-HERE` (the obstruction, not an impossibility). END-OF-LINE accepts any other source as an answer. Each level has many sources that are useless and easy to write down: any `alpha`-fixed marked pair with `c = m (mod 4)` cycles, for instance the start itself with its tokens permuted. So an END-OF-LINE oracle applied to the marked walk answers nothing. The statement in `research/2026-11-14_opus_route-topology/TOPOLOGY.md` 4.6 that each phase "is an instance of END-OF-LINE" is right about the shape of the graph. As a way to place the search problem it needs the sink version, and then the merging of phases asked for in its route R9 goes through as above. Membership in PPAD would need a rule that pairs up the extra sources. I did not find one. `CONJECTURE`-level question: is TREE-PAIR in PPAD? Test: an involution on the `alpha`-fixed points of sign `sigma_m` with exactly one fixed point.
- **PPA.** The undirected version has the same problem with leaves.
- **PPP.** Follows from PPADS (`LIT`, the inclusion, from memory).
- **The full problem.** BARNETTE-HC needs one tree pair per piece. Either chain the instances by the same linking device, or use that PPADS is closed under Turing reductions (`LIT`, Buss and Johnson, Propositional proofs and reductions between NP search problems, Ann. Pure Appl. Logic 163 (2012); cited from memory, I recall the statement for PPA, PPAD, PPADS and PLS). I did not write the chaining out, so "BARNETTE-HC is in PPADS" is `PROVED-HERE` only modulo that citation.

## 4. Local search: PLS and the descent problem

A PLS problem (`LIT`, Johnson, Papadimitriou and Yannakakis, How easy is local search?, J. Comput. System Sci. 37 (1988), from memory) has polynomial-time computable feasible solutions, cost, and neighbourhood, and asks for a solution with no strictly better neighbour.

**DESCENT(Phi, L).** Solutions are the pairs of the instance, the cost is a potential `Phi`, and the neighbourhood is the ball of radius `L` in the exchange graph. For fixed `L` this is a PLS problem. It solves TREE-PAIR iff every local optimum is a tree pair, that is, iff `Phi` has escape radius at most `L` (`PROOFS.md`, Proposition F).

Three points that are easy to get wrong.

1. **C3 does not put TREE-PAIR in PLS.** C3 allows moves that keep `k`. A pair on a plateau with no strictly better neighbour is a local optimum in the sense of PLS. Turning C3 into a PLS formulation needs a rule that breaks the ties, which is the same as a second potential that strictly decreases along the plateau.
2. **With these potentials, "in PLS with good local optima" already means "in P".** `k` takes at most `n/3 + 1` values, and the plateau-free potentials of Corollary B1 take `O(n^5)` values. A PLS problem whose cost has polynomially many values is solved by plain local search in polynomial time. So for the potentials studied here there is no intermediate outcome: either the local optima are tree pairs and the problem is in P, or the formulation does not solve the problem. A PLS statement with content would need a potential with exponentially many values, such as the position along the marked walk, which nobody knows how to compute.
3. **What the data say** (`DESCENT.md`, Section 3). `COMPUTED`: `k` has non-tree local optima for `L = 1` from `V = 16`, for `L = 2` from `V = 21` (exhaustive, so 21 is the least order), and for `L = 3` on random instances with `V = 60` (not known to be least). The plateau-free potentials have non-tree local optima for `L = 1` from `V = 16` or `18`, and for `L = 2` and `L = 3` at `V = 60`. Potentials that involve the number of `D`-cycles are stuck for good at `V = 16`.

`CONJECTURE` (C3, unchanged): there is no closed plateau. Evidence: exhaustive for `V <= 22`, sampled to `V = 200`. `HUNCH`: the escape radius of `k` is unbounded, growing slowly with `V` (observed maxima 1, 2, 3, 4 at `V = 15, 16, 21, 60`). If so, no local search with a fixed lookahead on `k` solves TREE-PAIR, and a polynomial algorithm along these lines needs a plateau rule.

## 5. Summary table

| Statement | Status |
| --- | --- |
| BARNETTE-HC is total, in TFNP | `LIT` (OpenAI Theorem 1.1) |
| Deterministic `O(poly(N) 3^{N/4})` time, polynomial space | `LIT` (trees paper, Proposition 6.2) |
| TREE-PAIR in PPADS, hence in PPP | `PROVED-HERE`, conditional on trees paper Theorem 5.3, unreviewed |
| TREE-PAIR in PPAD, PPA or PLS | open; the obvious reductions fail for the stated reasons |
| TREE-PAIR in P | open |
| Not FNP-hard unless NP = coNP | `LIT` (general fact about TFNP, from memory) |
| C3 (non-increasing path to a tree pair) | `CONJECTURE`; `COMPUTED` for all pairs with `V <= 22` |
| Bounded lookahead on `k` with radius 1, 2, 3 | `REFUTED` at `V = 16`, `21`, `60` |
| Descent on any potential that never lets `c` grow | `REFUTED` at `V = 16` |
