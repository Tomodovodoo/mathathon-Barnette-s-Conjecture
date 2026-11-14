# Reverse-Lamport audit: OpenAI, "Paired states and Hamiltonian cycles in cubic bipartite planar graphs" (24 Sep 2026)

Summary.
1. The route to Theorem 1.1 closes. I found no failing node. Verdict: FOLLOWS.
2. "No separating triangle" is used at exactly one node (`P5`, triangular faces of a component are actual faces). Sections 4 to 6 never use it.
3. 3-connectivity enters once, to make the dual simple (`O1a`). Simplicity of `T` then carries the weight in Proposition 3.1.
4. The disk identity (`C4`) is used four times: `J` is an integer, the `Q_s` reversal flips the phase, the leading phases agree, and `P` is a forest.
5. Corollary 7.2 rests on a cited theorem I could not open, so that corollary alone is INDETERMINATE.

Source: `papers/OpenAI-Barnette.pdf`, text dump `papers/text/OpenAI-Barnette.txt`. I worked from the dump and opened the PDF for page 4 (formulas (3.1) to (3.4)). Every other formula below was re-derived by hand, so a garbled character in the dump cannot have slipped through. Status tags follow `research/BRIEF.md`. A statement proved in the paper is tagged `LIT` with its location. A check I wrote out here is `PROVED-HERE`. A check by script is `COMPUTED` (`scripts/check_nodes.py`, output `data/check_nodes.txt`, 36 rooted triangulations with `n` between 3 and 23).

## 1. Audit boundary

**Conclusion `C0`** (Theorem 1.1). Every finite simple undirected graph that is cubic, bipartite, planar and 3-vertex-connected has a Hamiltonian cycle.

**Secondary conclusion `C0e`** (Corollary 7.1). For every such `G` and every edge `e`, some Hamiltonian cycle avoids `e`.

**Out of the main route.** Corollary 7.2 (Pfaffian graphs). It needs [5, Theorem 4.16] and [5, Theorem 4.6] of Gorsky, Steiner and Wiederrecht. I did not open that paper.

**Hypotheses.** `G` finite, simple, cubic, bipartite, planar, 3-vertex-connected (at least four vertices, no separating set of at most two vertices).

**Definitions in scope.** Sphere triangulation (connected, simple, at least four vertices, every face bounded by a 3-cycle). Separating triangle (3-cycle with vertices strictly on both sides). State, pair, `Q_s`, `D`, `δ`, `J`, `ω`, `Z(x)`, `H0`, `H`, `P`, `P0`.

**Accepted primitives.**
- Euler's formula for connected plane graphs, with edge-side counting of face lengths.
- The Jordan curve theorem for polygonal curves, and the fact that an isotopy through simple closed curves keeps the orientation (counterclockwise stays counterclockwise).
- A 2-regular bipartite graph splits into two perfect matchings.
- Max-flow min-cut with integral flows (Ford and Fulkerson). The paper also proves the integral statement inline by augmenting paths.
- A finite sum of exponentials is real-analytic, so it vanishes identically if and only if all its Taylor coefficients at 0 vanish.
- Elementary counting and algebra.

Not accepted without proof: the Stein and Alt-Payne-Schmidt-Wood equivalence, Temperley, double-dimer regrouping. The paper says these are context only, and the audit confirms that no node needs them.

## 2. Obligation graph

```text
C0  Theorem 1.1
    <- R0, dualise and apply Theorem 2.2
       AND: O1, O2, C1, O3

O1  T = G* is a sphere triangulation (connected, simple, >= 4 vertices, faces are 3-cycles)
    <- AND: O1a, O1b, O1c, O1d
O1a G has no edge cut of size 1 or 2          <- 3-connected + cubic + simple
O1b dual loop or parallel pair => edge cut of size 1 or 2 with both sides nonempty
O1c every dual face has a boundary walk of length 3, a triangle since T is simple
O1d |V(T)| = 2 + |V(G)|/2 >= 4                 <- Euler
O2  the bipartition of G colours the faces of T black and white, opposite across every edge
O3  two induced trees partitioning V(T) => Hamiltonian cycle of G
    <- AND: O3a (exactly one within-class edge per triangle), L21 (forest case), O3b (connected + 2-regular = one cycle)

C0e Corollary 7.1  <- AND: C1 with e0 = e*, O3, O3c (the cycle uses only duals of edges outside the forest)

L21 Lemma 2.1, complementary plane-tree duality (tree case and forest case)
    <- contraction + Euler

C1  Theorem 2.2: for any facial t0 and edge e0 of t0, V(T) splits into two induced trees
    with the ends of e0 together and the third vertex of t0 apart
    <- R1, induction on |V(T)|
       AND: C1b (no separating triangle), C1g (a separating triangle exists)

C1b base case
    <- R2  AND: E1, C3, C5, C61, W, C62, S

E1  (2.1): #white = k, |E| = 3k, |V| = k + 2, |A| = |X| = k - 1

C3  Proposition 3.1: no separating triangle => a pair exists
    <- R3  AND: P1, P2, P3, P4
P1  a degree-2 spanning subgraph of the incidence graph splits into two disjoint states
P2  (3.1) + integral max-flow => such a subgraph
P3  (3.1) <=> (3.2): e(U) - b(U) <= 2|U| - 4
P4  (3.2) for every U containing the roots
    <- AND: P5, P6, P7, P8, P9
P5  for a component K with p >= 4, triangular faces of K = actual faces of T on V(K)   [uses: no separating triangle]
P6  (3.3): |b' - w'| <= d - 4 for a region of length d >= 4
P7  (3.4): m - b <= 2p - 4 for a component with p >= 4          <- P5, P6, Euler
P8  small components: root component of order 3 is t0; others have m <= 2p by simplicity
P9  summation over components, with t0 counted once

C4  Lemma 4.1, disk identity
    <- R4  AND: D1, D2, D3, D4, D5
D1  a directed cycle in the chosen edges avoids the roots, and its disk contains no root
D2  Euler for the triangulated disk: B + W = 2I + h - 2
D3  signed side count: 3(B - W) = 2l - h
D4  the state gives B = I + l                                   [uses: r is a bijection, one chosen edge per face]
D5  algebra: 2l - h = -3, and this is the delta-sum of the counterclockwise traversal

C5  Proposition 5.1: a pair exists => some pair has Q_s a forest
    <- R5, two evaluations of Z(x)
       AND: N1, N2, C52, C53, N3, N4, N5, N6, N7
N1  for a pair, D is a union of vertex-disjoint simple directed cycles covering X
N2  J(r,s) is an integer, and equals #clockwise - #counterclockwise    <- N1, C4
C52 Lemma 5.2: for fixed s with cyclic Q_s the terms cancel
    <- AND: K1 (the chosen cycle is directed and avoids the roots), K2 (r~ is a state and a partner of s),
            K3 (fixed-point-free involution), K4 (local identity delta(u,s) - delta(r,s) = 2 delta(r,u)),
            C4 on the Q_s-cycle, K5 (omega(s) unchanged)
C53 Lemma 5.3: spoke weights with positive circulation on every counterclockwise simple spoke cycle
N3  regrouping: the pairs with a given undirected D are exactly the orientations of its cycles
N4  (5.3): L+(C) - L-(C) > 0
    <- AND: N4a (spoke weight of the detoured curve = L+ - L-), N4b (the spoke curve is a simple cycle of H0),
            N4c (it is counterclockwise), C53
N5  (5.4): the group sum factors over cycles                    <- N2, additivity of omega
N6  first nonzero Taylor coefficient of a group: degree c(D), value (-i)^c(D) prod (L+ - L-)
N7  at degree c_min the groups cannot cancel; so Z is not identically 0; with C52 some pair has Q_s a forest

C61 Lemma 6.1: for a pair with Q_s a forest, each component of Q_s has exactly one root   [uses r]

W   section 6.1, white tree and selection
    <- AND: W1 (H connected, faces of H = white triangles), W2 (H minus the spokes of s is a spanning tree, uses C61),
            L21 (tree case), W3 (rooting at y0 gives one selected side per white face),
            W4 (one selected side per black face, |P| = k, P0 oriented out of s(t))

C62 Lemma 6.2: P is a forest
    <- AND: F1 (a cycle in P0 is directed), F2 ((6.1): B - W = 2l - h by the one-selected-side count),
            D3, C4 for the state s, F3 (one root per component of P0), F4 (e0 joins two root components)

S   two induced trees from P
    <- AND: L21 (forest case), S1 (dual of the complement is 2-regular, hence one cycle),
            S2 (Jordan curve labels: same label iff edge in P), S3 (P has 2 components, both labels occur),
            S4 (the same-label edge at t0 is e0)

C1g gluing over a separating triangle
    <- AND: G1 (both capped pieces are smaller sphere triangulations), G2 (the colouring extends to the caps),
            G3 (both labels occur on the cap), G4 (induction hypothesis applies to the second piece with the cap as t0),
            G5 (union of two trees meeting in a vertex or an edge is a tree, and it is induced)
```

There are no supplied alternative routes. No diagnostic route was needed.

## 3. Critical findings

No node is `missing`, `circular`, `too strong` or an unbridged `route switch`. The findings below are side conditions I checked for real, and notes on what each hypothesis does.

**F1. Where "no separating triangle" is used.** Only at `P5`. The text says a triangular face of `K` is bounded by a 3-cycle, the cycle is not separating, so one side is a face of `T`, and `K` has a vertex on the other side. Nothing in Sections 4, 5 or 6 uses the hypothesis. Section 6 opens with "Assume that T has no separating triangle", and the only purpose is to call Proposition 3.1. `PROVED-HERE` by inspection of every node. This is why the trees paper can weaken the hypothesis to "no separating triangle with black inner boundary" (see `audit-trees.md`, `T-P5`).

**F2. Where 3-connectivity enters.** Only at `O1a`, to exclude edge cuts of size one and two, which gives a loopless dual without parallel edges. After that the proof never mentions `G` until the last paragraph. The real consumer is `P6` to `P8`. With a parallel pair in `T`, a component `K` could have a face of length 2, where the bound (3.3) reads `|b' - w'| <= -2` and fails. So simplicity of `T` is what the flow bound needs. `PROVED-HERE`.

**F3. Where simplicity of `T` is used.** (a) `O1c`, a closed walk of length three is a triangle. (b) `P7`, every face of `K` has length at least 3. (c) `P8`, a component with at most three vertices has `m <= 2p`. (d) States pick one of three distinct corners. (e) `G1`, the capped pieces stay simple. The fact that distinct black faces supply distinct edges (used in `N1`, `N3`, `N4b`, `D4`, `W4`) does not come from simplicity. It comes from the colouring, since each edge has exactly one black face.

**F4. Where bijectivity of a state is used.** I list every use, because this is the hypothesis that turns a colour count into an exact identity.
- `D4`. Surjectivity onto `X` matches every interior vertex. Injectivity prevents double counting. Totality on `A` matches every black face in the disk. The boundary case needs that the outgoing cycle edge at `v` is the chosen edge of `r^{-1}(v)`.
- `N1`. In-degree one needs `s` bijective. Out-degree one needs `r` bijective.
- `K1`. Distinct tails need `r` injective, which forces the `Q_s`-cycle to be directed.
- `K2`. The reversal permutes the assigned vertices cyclically, so `r~` is again a bijection.
- `C61`. Out-degree exactly one at every nonroot needs `r` onto `X`.
- `F1` and `F3`. The same two facts for `s`.
- `W2`, `W4`. Exactly `k - 1` spokes are deleted, one at each face of `A` and one at each nonroot.

**F5. Orientation conventions.** `δ(v,w) = 1` when the black face is on the left of `v -> w`. A counterclockwise cycle has its disk on the left, so its `δ`-sum is `l - (h - l) = 2l - h = -3`, and it contributes `-1` to `J`. The same convention is used in Lemma 5.2 (the local identity, which I checked in both cyclic orders of `(r, s, u)`), in (5.4) and in Lemma 6.2. Consistent throughout. `PROVED-HERE` for the local identity. `COMPUTED` for the rest: on every pair of every test triangulation, each `D`-cycle and each directed `Q_s`-cycle has `δ`-sum `-3` when counterclockwise and `+3` when clockwise, `J = #cw - #ccw`, and both reversals change `J` by exactly 2.

**F6. The claim that the spoke curve is simple and counterclockwise (`N4b`, `N4c`).** These are two different claims and the text proves them in one breath.
- Simple (`N4b`) is immediate and needs no topology. The closed walk `v1, t1, v2, t2, ..., vh, th` in `H0` has distinct `v_i` (the `D`-cycle is simple) and distinct centres `t_i` (one edge of `D` per black face). So it is a cycle of the plane graph `H0`.
- Counterclockwise (`N4c`) is where the sliding argument is needed. The closed subdisk between the edge `vw` and the route `v, t, w` is the triangle `v t w` inside the closed face `t`. It meets the boundary of `t` only in the edge `vw`, so it misses the third corner even when that corner lies elsewhere on `C`. The open face `t` contains no other part of the curve, because the rest of the curve lies in `T`-edges and in other black faces. So each slide is an isotopy through simple closed curves, and orientation is preserved by the accepted primitive.

Both hold. `PROVED-HERE`. Note that the slide exists only because `D` and `J` are defined on edges of `T` while the weights live on spokes. Li's note defines cycles on spokes from the start and never needs it.

**F7. Lemma 5.3 on a disconnected `H0`.** The proof works per component, and a simple cycle lies in one component. The circulation of a counterclockwise simple cycle is the number of faces of its own component inside it, which is at least one. A dual path never crosses a bridge, since a bridge is a dual loop. Fine.

**F8. The Euler counts.** (2.1): `3k = |E| = 3 #white`, then `|V| = 2 + 3k - 2k`. (4.1): `V = I + h`, `E = (3(B + W) + h)/2`, `F = B + W + 1`. Lemma 2.1: `|E| - |V| + 1 = |F| - 1`. (3.4): `2m = 3(b + w) + 4(f - b - w) + sum (d - 4)` and `p - m + f = 2`. The last line of Lemma 6.2: `(k + 2) - k = 2` components. All correct. `PROVED-HERE`, and `COMPUTED` for (2.1), (4.1), (4.2).

**F9. What Lemma 6.2 contradicts.** The text says the cycle "would have δ-sum zero in either orientation, contrary to Lemma 4.1". For this, Lemma 4.1 must apply to the state `s` with chosen edges `P0`. It does: `P0` has exactly one edge in each `t ∈ A`, directed out of `s(t)`. The contradiction is sharper than stated. Euler and (6.1) give `B = I + l - 1`, the state gives `B = I + l`. The cycle would enclose one black face too few. The partner `r` is not used in Lemma 6.2 except through Lemma 6.1 (the three roots lie in different components of `Q_s`), which `W2` needs.

**F10. The exponential sum needs a pair to exist.** "There is at least one group" is the hypothesis of Proposition 5.1. Without a pair `Z` is the empty sum. The proposition is stated with that hypothesis, so there is no gap.

**F11. The gluing step needs the full strength of Theorem 2.2.** The induction hypothesis is applied to the second piece with the cap as `t0`, which may be white, and with a prescribed edge chosen by the first piece. So the theorem must be stated for an arbitrary facial triangle and edge, as it is. The cap colour is forced because `3(B - W)` is a sum of three signs.

**F12. Claims that are context and not obligations.** The Stein and Alt-Payne-Schmidt-Wood equivalence is cited in 1.1, but the direction needed (two induced trees give a Hamiltonian cycle) is proved in the last paragraph of Section 7 (`O3`). Temperley and double-dimer are named as context. No node depends on them.

**F13. Corollary 7.2.** It applies [5, Theorem 4.16] (equivalence of Barnette's conjecture with `P4`-Hamiltonicity of cubic 3-connected Pfaffian bipartite graphs). I could not open [5]. The node is `named theorem`, status `open`.

## 4. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Theorem 1.1 | root | R0 / claim | root | O1, O2, C1, O3 | discharged |
| C0e | Corollary 7.1, a Hamiltonian cycle avoiding a given edge | root | R0 / claim | major claim | C1 with `e0 = e*`, O3, O3c | discharged |
| O1 | `T = G*` is a sphere triangulation | C0 | R0 / AND | proved earlier | O1a to O1d, Section 7 | discharged |
| O1a | no edge cut of size 1 or 2 | O1 | AND | algebraic/logical step | each side has at least 3 vertices, delete at most 2 endpoints | discharged |
| O1b | dual loop or parallel pair gives such a cut | O1 | AND | algebraic/logical step | Jordan curve through one or two edges | discharged |
| O1c | dual faces are triangles | O1 | AND | side condition | cubic, plus simplicity from O1a, O1b | discharged |
| O1d | `|V(T)| >= 4` | O1 | AND | algebraic/logical step | Euler | discharged |
| O2 | proper black and white face colouring of `T` | C0, E1, everything | R0 / AND | hypothesis | bipartition of `G` | discharged |
| O3 | two induced trees give a Hamiltonian cycle | C0, C0e | R0 / AND | proved earlier | O3a, L21, O3b, Section 7 | discharged |
| O3a | each triangle has exactly one within-class edge | O3 | AND | algebraic/logical step | a tree class cannot hold a triangle | discharged |
| O3b | connected and 2-regular is one spanning cycle | O3 | AND | algebraic/logical step | elementary | discharged |
| O3c | the cycle omits the dual of every forest edge | C0e | AND | definition | construction in O3 | discharged |
| L21 | Lemma 2.1, complement of a spanning tree (forest) dualises to a spanning tree (connected spanning subgraph) | W, S, O3 | AND | proved earlier | contraction and Euler, Section 2 | discharged |
| C1 | Theorem 2.2 | C0, C0e | R1 / claim | major claim | induction: C1b, C1g | discharged |
| C1b | Theorem 2.2 without separating triangles | C1 | R1 / AND | major claim | E1, C3, C5, C61, W, C62, S | discharged |
| E1 | counts (2.1), `|A| = |X| = k - 1` | C1b, P3, S3 | AND | algebraic/logical step | side counting and Euler | discharged |
| C3 | Proposition 3.1, a pair exists | C1b | R2 / AND | major claim | P1 to P4 | discharged |
| P1 | degree-2 subgraph splits into two disjoint states | C3 | AND | algebraic/logical step | even cycles alternate | discharged |
| P2 | (3.1) and integral max-flow give the subgraph | C3 | AND | named theorem | Ford-Fulkerson, cut computed in the text, capacities integral | discharged |
| P3 | (3.1) is equivalent to (3.2) | C3 | AND | algebraic/logical step | shortfall `max(0, j - 1)`, one black face per edge, E1 | discharged |
| P4 | (3.2) holds for all `U ⊇ R` | C3 | AND | proved earlier | P5 to P9 | discharged |
| P5 | triangular faces of `K` are actual faces of `T` | P7 | AND | side condition | hypothesis "no separating triangle", `p >= 4` | discharged |
| P6 | (3.3) `|b' - w'| <= d - 4` | P7 | AND | algebraic/logical step | parity and divisibility by 3, cases `d = 4, 5, >= 6` | discharged |
| P7 | (3.4) `m - b <= 2p - 4` | P4 | AND | algebraic/logical step | P5, P6, Euler | discharged |
| P8 | components of order at most 3 | P4 | AND | side condition | simplicity of `T`, roots are pairwise adjacent | discharged |
| P9 | summation over components | P4 | AND | algebraic/logical step | each black face on `U` lies in one component | discharged |
| C4 | Lemma 4.1, disk identity | N2, C52, N5, C62 | R4 / claim | major claim | D1 to D5 | discharged |
| D1 | the cycle and its disk avoid the roots | C4 | AND | side condition | only nonroots have out-edges, roots lie on the outer face | discharged |
| D2 | `B + W = 2I + h - 2` | C4, C62 | AND | algebraic/logical step | Euler on the disk | discharged |
| D3 | `3(B - W) = 2l - h` | C4, C62 | AND | algebraic/logical step | internal sides cancel | discharged |
| D4 | `B = I + l` | C4 | AND | side condition | state bijective, one chosen edge per face, D1 | discharged |
| D5 | `2l - h = -3` is the counterclockwise δ-sum | C4 | AND | algebraic/logical step | algebra, definition of δ | discharged |
| C5 | Proposition 5.1, a forest pair exists | C1b | R2 / AND | major claim | N1 to N7, C52, C53 | discharged |
| N1 | `D` is a disjoint union of simple directed cycles on `X` | C5, N2, N3 | AND | algebraic/logical step | bijectivity, one black face per edge | discharged |
| N2 | `J` is an integer, `#cw - #ccw` | C5, N5 | AND | proved earlier | N1, C4 | discharged |
| C52 | Lemma 5.2, cancellation for fixed `s` | C5 | AND | major claim | K1 to K5, C4 | discharged |
| K1 | the chosen `Q_s`-cycle is directed and avoids roots | C52 | AND | side condition | distinct tails, out-degree 0 at roots | discharged |
| K2 | `r~` is a state and a partner of `s` | C52 | AND | side condition | cyclic permutation of assigned vertices, `u(t) ≠ s(t)` | discharged |
| K3 | the map is a fixed-point-free involution | C52 | AND | algebraic/logical step | the cycle is chosen from `s` alone | discharged |
| K4 | `δ(u,s) - δ(r,s) = 2δ(r,u)` | C52 | AND | algebraic/logical step | two cyclic orders checked | discharged |
| K5 | `ω(s)` unchanged | C52 | AND | definition | `ω` depends on `s` only | discharged |
| C53 | Lemma 5.3, positive spoke circulations | N4 | AND | proved earlier | unit dual paths, per component | discharged |
| N3 | a `D`-group is the set of orientations of its cycles | C5 | AND | algebraic/logical step | one black face per edge, bijectivity | discharged |
| N4 | (5.3) `L+ - L- > 0` | N6, N7 | AND | proved earlier | N4a, N4b, N4c, C53 | discharged |
| N4a | spoke weight of the detour is `a(t,head) - a(t,tail)` | N4 | AND | algebraic/logical step | antisymmetry of the weights | discharged |
| N4b | the spoke curve is a simple cycle of `H0` | N4 | AND | side condition | distinct vertices and distinct centres | discharged |
| N4c | the spoke curve is counterclockwise | N4 | AND | side condition | slide across subdisks, isotopy primitive | discharged |
| N5 | (5.4) product over cycles | N6 | AND | algebraic/logical step | N2, `ω` additive over cycles | discharged |
| N6 | leading Taylor coefficient `(-i)^c prod (L+ - L-)` at degree `c(D)` | N7 | AND | algebraic/logical step | each factor has a simple zero | discharged |
| N7 | `Z` is not identically zero, so a forest pair exists | C5 | AND | algebraic/logical step | N6 at `c_min`, N4, C52, at least one pair | discharged |
| C61 | Lemma 6.1, one root per component of `Q_s` | W2 | AND | proved earlier | out-degree count with the partner `r` | discharged |
| W | white tree and selected set `P` | C1b | R2 / AND | proved earlier | W1 to W4, L21 | discharged |
| W1 | `H` connected, faces of `H` are the white triangles | W | AND | side condition | routing through centres, sectors | discharged |
| W2 | `H` minus the spokes of `s` is a spanning tree | W | AND | algebraic/logical step | subdivided `Q_s` plus three root spokes, C61 | discharged |
| W3 | one selected side at each white triangle | W, F2 | AND | algebraic/logical step | rooted tree, child assignment, `e0` at `y0` | discharged |
| W4 | one selected side at each black triangle, `|P| = k` | W, F2 | AND | algebraic/logical step | one deleted spoke per `t ∈ A`, `e0` at `t0` | discharged |
| C62 | Lemma 6.2, `P` is a forest | C1b | R2 / AND | major claim | F1 to F4, D3, C4 | discharged |
| F1 | a cycle in `P0` is directed | C62 | AND | side condition | `s` injective | discharged |
| F2 | (6.1) `B - W = 2l - h` | C62 | AND | algebraic/logical step | W3, W4, interior selected edges cancel, chords included | discharged |
| F3 | one root per component of `P0` | C62 | AND | algebraic/logical step | out-degree count for `s` | discharged |
| F4 | `e0` joins two different components | C62 | AND | algebraic/logical step | F3, ends of `e0` are roots | discharged |
| S | two induced trees with the prescribed pattern | C1b | R2 / AND | proved earlier | S1 to S4, L21 | discharged |
| S1 | the complementary dual is one simple cycle | S | AND | algebraic/logical step | two unselected sides per face, L21, `2k > 2` | discharged |
| S2 | same label if and only if the edge is in `P` | S | AND | named theorem | Jordan curve, one transverse crossing | discharged |
| S3 | the two classes are the two components of `P` | S | AND | algebraic/logical step | E1, both labels occur | discharged |
| S4 | the same-label edge at `t0` is `e0` | S | AND | definition | `e0 ∈ P`, one selected side at `t0` | discharged |
| C1g | gluing across a separating triangle | C1 | R1 / AND | major claim | G1 to G5 | discharged |
| G1 | capped pieces are smaller sphere triangulations | C1g | AND | side condition | simple, at least 4 vertices, triangular faces | discharged |
| G2 | the colouring extends to each cap | C1g | AND | algebraic/logical step | three signs with sum divisible by 3 | discharged |
| G3 | both labels occur on the cap | C1g | AND | algebraic/logical step | a monochromatic triangle is a cycle in a tree | discharged |
| G4 | the induction hypothesis applies with the cap as `t0` | C1g | AND | side condition | Theorem 2.2 is stated for any facial triangle and edge | discharged |
| G5 | the glued classes induce trees | C1g | AND | algebraic/logical step | trees meeting in a vertex or an edge, no edge between the open sides | discharged |
| X72 | Corollary 7.2 | none on the main route | separate | named theorem | [5, Theorems 4.6, 4.16], not opened | open |

## 5. Verdict

**FOLLOWS** for Theorem 1.1 (`C0`) and Corollary 7.1 (`C0e`). Every obligation on the single supplied route is discharged. The decisive nodes are `C3` (with its one use of the hypothesis at `P5`), `C4`, `C52`, `N4`, `N7`, `C62` and `C1g`.

**INDETERMINATE FROM THE PROVIDED MATERIAL** for Corollary 7.2 alone (`X72`), because the cited equivalence was not available to me. This does not touch the main theorem.
