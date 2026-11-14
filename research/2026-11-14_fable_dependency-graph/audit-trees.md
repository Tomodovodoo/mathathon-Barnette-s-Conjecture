# Reverse-Lamport audit: "A constructive proof of Barnette's conjecture" (`barnette_trees.pdf`, 18 Oct 2026)

Summary.
1. The routes to Theorems 1.1, 1.2, 5.2 and 5.3 all close. Verdict: FOLLOWS. I found no failing node.
2. The paper proves three things the other two do not: the exact criterion (ii) ⟺ (iii), the unique-mate characterisation of tree matchings, and the common permutation sign of all states.
3. The hypothesis "no separating triangle with black inner boundary" is used at exactly one node (`S6`). The region that contains `t0` is handled by a separate one-line bound, and that line is what makes the weaker hypothesis enough.
4. Theorem 1.2 (ii) ⟹ (i) is proved in Section 5, after the statement that cites it. There is no circularity.
5. Statements about the companion implementation (breadth-first search, random walk) point to material I do not have. They are not on any route to a theorem.

Source: `papers/barnette_trees.pdf`, text dump `papers/text/barnette_trees.txt`. I opened the PDF for page 6 (Section 3) and re-derived the rest. `COMPUTED` refers to `scripts/check_nodes.py` and `data/check_nodes.txt`.

## 1. Audit boundary

**Conclusion `C0`** (Theorem 1.1). Given a finite simple cubic bipartite 3-connected planar graph `G` on `N` vertices and an edge `e`, a deterministic algorithm constructs a Hamiltonian cycle avoiding `e`, in polynomial space and `O(poly(N) 3^{N/4})` time.

**Conclusion `C12`** (Theorem 1.2). For a simple sphere triangulation `T` with at least four vertices, properly coloured, with a black outer face, the following are equivalent. (i) Some perfect matching `s` of `B` has `H - s` a spanning tree. (ii) `B` has two edge-disjoint perfect matchings. (iii) No separating triangle has black inner boundary. Also, `s` is a tree matching if and only if it has exactly one disjoint mate.

**Conclusions `C52`, `C53`** (Theorems 5.2, 5.3). Every component of the exchange graph contains a tree pair, with both signs equally often. The marked walk reaches a tree pair in the same component.

**Accepted primitives.** Euler's formula. Jordan curve theorem and isotopy invariance of orientation. Integral max-flow min-cut. Hadamard's inequality. Complementary plane-tree duality (the paper also proves it in 7.1). Elementary facts on functional digraphs and on paths in graphs of maximum degree 2.

**Out of scope.** The companion code and its proofs for the breadth-first and random-walk constructors. Eppstein's bound, cited for comparison only.

## 2. Obligation graph

```text
C0  Theorem 1.1
    <- R0  AND: O1, C12, P62, L71, G73, O3, TB

O1  T = G* is a simple sphere triangulation, properly coloured (same argument as OpenAI section 7)
O3  the two classes give a Hamiltonian cycle of G that omits e
TB  time bound: n = N/2 - 1, |V(T)| - 3 is additive over splits, sum of 3^{n_i/2} <= 3^{n/2}

C12 Theorem 1.2
    <- R1  AND: E3, C21, F23, C52, DG
E3  (3): H - s is a tree  <=>  Q_s is a forest with one root in each component
C21 Proposition 2.1: s has a mate <=> every component of Q_s is a tree with one root or unicyclic with no root;
    then there are exactly 2^k mates
    gives: (i) => (ii), and "tree matching <=> exactly one mate"
DG  prescribed-degree form: spanning trees of H with the listed degrees <=> complements of perfect matchings of B
F23 (ii) <=> (iii)
    <- AND: S1, S2, S3, S4
S1  two disjoint perfect matchings <=> (4), by integral max-flow
S2  (4) <=> (5): e(U) - b(U) <= 2|U| - 4
S3  a separating triangle with black inner boundary violates (5) by exactly one
S4  no such triangle => (5)
    <- AND: S5 ((6), (7): |beta(F)| <= d - 4), S6 (a bounded triangular region of balance 1 is an actual black face),
            S7 (the region containing t0: b^ = b_K for the root component, b^ <= b_K + 1 otherwise),
            S8 (m - b^ <= 2p - 4 by Euler), S9 (small components, summation)
    (ii) => (i) is C52.

C41 Lemma 4.1, disk identity, and every such cycle has odd length
C42 Lemma 4.2: every edge of the exchange graph reverses epsilon
    <- AND: X1 (epsilon is defined: J = c = n mod 2), X2 (a D-reversal changes J by +-2),
            X3 (a Q_s-reversal changes J by +-2: local identity and C41), X4 (moves are well defined, C21)
C51 Lemma 5.1: integer weights 0 <= a(t,v) <= 6n with L+(C) > L-(C) for every D-cycle
    <- AND: W1 (unit circulations by dual-tree paths), W2 (bounds), W3 (subtracting the minimum at a centre keeps L+ - L-),
            W4 (spoke detour is a simple counterclockwise cycle)
C52 Theorem 5.2 (component theorem)
    <- R2  AND: C42, C51, Y1, Y2, Y3, Y4
Y1  fix s: the Q_s-reversal is a sign-reversing involution inside the component; survivors are the tree pairs (C21, E3)
Y2  a D-group lies inside one component and is the full set of cycle orientations
Y3  (11) and its expansion at z = 1: the coefficient of (z - 1)^m is a nonzero integer
Y4  Z_C(1) = 0, so the surviving signs balance
C53 Theorem 5.3 (marked construction)
    <- R3  AND: C42, C51, M1, M2, M3, M4, M5, M6
M1  beta is an involution, fixed points are tree pairs
M2  alpha is an involution
M3  (12): at an alpha-fixed point c <= m and epsilon = (-1)^{(n-c)/2}
M4  the start is alpha-fixed with c = m
M5  path argument: the walk ends, and an alpha-endpoint has c' <= m - 2
M6  bounds: 2^{O(n log n)} moves, polynomial space

C61 Lemma 6.1: all perfect matchings of B have one permutation sign, M = |det K_B| <= 3^{n/2}
    <- AND: C41 (odd cycles), Hadamard
P62 Proposition 6.2: the prefix search returns a tree matching in O(n^3 M) time
    <- AND: C12 (existence), Z1 (both prefix tests are necessary conditions), Z2 (at most (n+1)M retained prefixes),
            Z3 (a connected H - s with 2n + 3 edges is a tree), C61
L71 Lemma 7.1: a tree matching gives two induced trees with the pattern at t0
    <- AND: R1a (faces of H are the white triangles, plane-tree duality), R1b (one selected side per face),
            R1c (P0 is a forest: C41 for the state s and the selected-side count), R1d (root components, e0),
            R1e (dual cycle, Jordan curve labels)
G73 section 7.3: cut only at a black-inner separating triangle, cap, recurse, glue
    <- AND: C12 (failure of the flow gives such a triangle), H1 (cap colours forced), H2 (both labels on the cap),
            H3 (glued classes induce trees), H4 (termination by additivity of |V(T)| - 3)
```

## 3. Critical findings

No node fails. The notes below record what was checked and what each hypothesis does.

**T-F1. The one use of (iii) (`S6`, `S7`).** A triangular face region of `K` with balance 1 has black faces along all three sides on its own side. If it is not a face of `T` it contains a vertex, and `K` has a vertex on the other side, so its boundary is a separating triangle. "Black inner boundary" is defined with respect to the bounded side, so the triangle is forbidden only when the region is the bounded side. The paper handles the other case in one sentence: only the region containing `t0` can be an unbounded-side region, the root component has that region equal to `t0`, and any other component loses at most one, which the slack `2p` versus `2p - 4` absorbs. Checked line by line. `PROVED-HERE` for the reading, `LIT` for the proof (Section 3).

A reformulation that I find easier to use. Across each edge of a separating triangle the two faces have opposite colours, and by signed side counting each side is monochromatic along the triangle. So every separating triangle has exactly one black side. Condition (iii) says that `t0` lies on the black side of every separating triangle. `PROVED-HERE`. `COMPUTED`: the same triangulation with one separating triangle has 0 pairs with `t0` on the white side and 4 pairs with `t0` on the black side.

**T-F2. Order of proof in Theorem 1.2.** (i) ⟹ (ii) is Proposition 2.1. (ii) ⟺ (iii) is Section 3. (ii) ⟹ (i) is Theorem 5.2, which uses only Lemmas 4.1, 4.2, 5.1, Proposition 2.1 and (3). None of these uses Theorem 1.2. No cycle.

**T-F3. The component refinement (`Y1`, `Y2`).** The OpenAI sum runs over all pairs. Here it runs over one component of the exchange graph, and this needs both regroupings to stay inside the component. They do, because each regrouping moves by allowed exchanges: `Y1` by move (b), `Y2` by move (a). `COMPUTED`: in every component of every test case there is a tree pair and the signs of the tree pairs sum to zero (up to 11 components in one case).

**T-F4. The sign `ε` is defined (`X1`).** `ε = (-1)^{(n+J)/2}` needs `J ≡ n mod 2`. Each cycle contributes `±1` to `J`, so `J ≡ c`. Each cycle has odd length by Lemma 4.1 and the cycles cover `n` vertices, so `c ≡ n`. `COMPUTED` on all pairs.

**T-F5. Lemma 5.1, bounds (`W2`, `W3`).** The spoke graph `H0` has `3n` spokes, so its components have at most `3n` bounded faces in total. A unit dual-tree path crosses a spoke at most once, so the signed weights lie in `[-3n, 3n]`. Subtracting the minimum at each centre gives `0 ≤ a ≤ 6n` and keeps `L+ - L-`, since a cycle enters and leaves each centre once. After this step the numbers are labels on (centre, vertex) incidences and no longer antisymmetric edge weights. Correct.

**T-F6. Theorem 5.3, the marked walk.** I checked each claim.
- `M2`. In rule (1) the reversed cycle carries no token, so all tokens stay valid, and it is still the first unmarked cycle. In rule (2) a clockwise cycle has its tokens in the clockwise pool, with ranks at most `L-`. After reversal it is counterclockwise with all ranks at most `L-`, so it still qualifies, and the transport is its own inverse. Other cycles keep their status. So `α² = 1`.
- `M3`. At an `α`-fixed point every cycle is marked, so `c ≤ m`, and every cycle is counterclockwise, so `J = -c`.
- `M4`. The strict gap `L+ ≥ L- + 1` supplies a token of rank `L- + 1` on each cycle.
- `M5`. The walk starts at a vertex with no `α`-edge, so it runs along a path. It applies `β` first. If it stops at an `α`-fixed point it has made an odd number of moves, each reversing `ε`. With (12) at both ends this gives `c' ≡ m + 2 mod 4` and `c' ≤ m`, so `c' ≤ m - 2`.
- The cycle membership of a token is recomputed after each move. This matters because `β` changes `r`, which changes the cycles of `D`.

All correct. The involution principle of Garsia and Milne is cited, but the path argument is written out, so the citation is not an input.

**T-F7. Lemma 6.1.** The relative permutation `s r^{-1}` has only odd cycles, by Lemma 4.1 applied with arbitrary out-edges on the faces where `r` and `s` agree. A 2-cycle cannot occur, because it would need two black faces on one edge. The paper does not say this, but Lemma 4.1 covers it, since a directed 2-cycle is not available among the chosen edges. `COMPUTED`: `|det K_B|` equals the number of states and the sign is constant in all 36 cases.

**T-F8. Where each hypothesis enters.**
- No black-inner separating triangle: `S6` only.
- 3-connectivity of `G`: `O1` only (dual simple).
- Simplicity of `T`: `S9` (small components), face lengths at least 3 in `S8`, and `n ≥ 3` in Section 2.
- A partner `r`: needed for `C42`, `C52`, `C53`. Not needed for `L71`. The paper says so in 7 ("It requires only a tree matching"), and Proposition 2.1 shows a tree matching always has its mate anyway.
- Bijectivity of a state: the disk identity (`C41`), the cycle cover `D`, Proposition 2.1 (out-degree one at every nonroot), `R1c`, `R1d`.

**T-F9. Time bound (`TB`).** Terminal pieces have parameters `n_i ≥ 3` with sum `n`, so the matching counts multiply out to at most `3^{n/2}` in total. Non-terminal pieces cost a flow and a triangle search. Correct.

**T-F10. Statements outside the audit.** "The companion gives the implementation details and the proofs for the breadth-first and random-walk alternatives." I do not have the companion. The remark that a properly coloured triangulation exists if and only if all degrees are even is standard and unused.

## 4. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Theorem 1.1 | root | R0 / claim | root | O1, C12, P62, L71, G73, O3, TB | discharged |
| O1 | `T = G*` simple triangulation, coloured | C0 | AND | proved earlier | proof of Theorem 1.1, no 1- or 2-edge cut | discharged |
| O3 | two classes give a Hamiltonian cycle omitting `e` | C0 | AND | algebraic/logical step | one within-class side per triangle, duality | discharged |
| TB | `O(poly(N) 3^{N/4})` time, polynomial space | C0 | AND | algebraic/logical step | P62, H4, T-F9 | discharged |
| C12 | Theorem 1.2 | C0, P62, G73 | R1 / claim | major claim | E3, C21, F23, C52, DG | discharged |
| E3 | (3), `H - s` tree iff `Q_s` rooted forest | C12, Y1 | AND | algebraic/logical step | subdivision plus three root spokes | discharged |
| C21 | Proposition 2.1, mates and the count `2^k` | C12, X4, Y1, M1 | AND | proved earlier | out-degree count, both directions | discharged |
| DG | prescribed-degree formulation | C12 | AND | definition | edge complements in `H` | discharged |
| F23 | (ii) iff (iii) | C12 | AND | major claim | S1 to S4 | discharged |
| S1 | two disjoint matchings iff (4) | F23 | AND | named theorem | integral max-flow, cut value computed | discharged |
| S2 | (4) iff (5) | F23 | AND | algebraic/logical step | shortfall count, `t0` adds two | discharged |
| S3 | black-inner triangle violates (5) by one | F23 | AND | algebraic/logical step | `B_d = I + 1`, `e(U) = 3n + 3 - 3I`, `b(U) = n - I` | discharged |
| S4 | no black-inner triangle gives (5) | F23 | AND | proved earlier | S5 to S9 | discharged |
| S5 | (6), (7) | S4 | AND | algebraic/logical step | parity and divisibility by 3 | discharged |
| S6 | bounded triangular region of balance 1 is an actual black face | S4 | AND | hypothesis | condition (iii), `p ≥ 4` | discharged |
| S7 | the region containing `t0` costs at most one | S4 | AND | side condition | root component has outer region `t0`, T-F1 | discharged |
| S8 | `m - b^ ≤ 2p - 4` | S4 | AND | algebraic/logical step | Euler, zero total balance | discharged |
| S9 | small components and summation | S4 | AND | side condition | simplicity | discharged |
| C41 | Lemma 4.1, disk identity, odd length | C42, C61, L71 | claim | major claim | Euler, side count, matching count | discharged |
| C42 | Lemma 4.2, each exchange reverses `ε` | C52, C53 | AND | major claim | X1 to X4 | discharged |
| X1 | `J ≡ c ≡ n mod 2` | C42 | AND | side condition | C41 | discharged |
| X2 | `D`-reversal changes `J` by `±2` | C42 | AND | algebraic/logical step | C41 on `D`-cycles | discharged |
| X3 | `Q_s`-reversal changes `J` by `±2` | C42 | AND | algebraic/logical step | local identity, C41 on the `Q_s`-cycle | discharged |
| X4 | both moves are well defined and self-inverse | C42 | AND | side condition | C21, cycles of `Q_s` are directed and avoid roots | discharged |
| C51 | Lemma 5.1, integer weights with `L+ > L-` | C52, C53 | AND | proved earlier | W1 to W4 | discharged |
| W1 | unit circulation on every bounded face | C51 | AND | algebraic/logical step | dual-tree paths | discharged |
| W2 | `0 ≤ a ≤ 6n` | C51, M6 | AND | algebraic/logical step | at most `3n` bounded faces | discharged |
| W3 | normalisation keeps `L+ - L-` | C51 | AND | algebraic/logical step | entry and exit at a centre cancel | discharged |
| W4 | the spoke detour is a simple counterclockwise cycle | C51 | AND | side condition | distinct centres, slide across subdisks | discharged |
| C52 | Theorem 5.2 | C12, P62 | R2 / claim | major claim | C42, C51, Y1 to Y4 | discharged |
| Y1 | cancellation inside a component | C52 | AND | algebraic/logical step | move (b), C42, C21, E3 | discharged |
| Y2 | a `D`-group lies in one component | C52 | AND | algebraic/logical step | move (a) | discharged |
| Y3 | coefficient of `(z - 1)^m` is nonzero | C52 | AND | algebraic/logical step | (11), simple zeros, positivity from C51 | discharged |
| Y4 | signs of tree pairs balance | C52 | AND | algebraic/logical step | `Z_C(1) = 0` | discharged |
| C53 | Theorem 5.3 | none on the route to C0 | R3 / claim | major claim | M1 to M6 | discharged |
| M1 | `β` involution with tree pairs as fixed points | C53 | AND | algebraic/logical step | cycle chosen from `s` alone, C21 | discharged |
| M2 | `α` involution | C53 | AND | algebraic/logical step | T-F6 | discharged |
| M3 | (12) | C53 | AND | algebraic/logical step | definition of `α`-fixed | discharged |
| M4 | the start is `α`-fixed | C53 | AND | side condition | strict gap from C51 | discharged |
| M5 | termination and `c' ≤ m - 2` | C53 | AND | algebraic/logical step | path argument, C42, M3 | discharged |
| M6 | `2^{O(n log n)}` moves | C53 | AND | algebraic/logical step | `W ≤ 6n²`, at most `6^n` pairs, `m0 ≤ n/3` | discharged |
| C61 | Lemma 6.1, `M = |det K_B| ≤ 3^{n/2}` | P62, TB | AND | proved earlier | C41, Hadamard | discharged |
| P62 | Proposition 6.2, prefix search | C0 | AND | proved earlier | C12, Z1 to Z3, C61 | discharged |
| Z1 | prefix tests are necessary for a tree completion | P62 | AND | algebraic/logical step | deleting spokes cannot reconnect | discharged |
| Z2 | at most `(n + 1)M` retained prefixes | P62 | AND | algebraic/logical step | each extends to a matching | discharged |
| Z3 | connected with `2n + 3` edges on `2n + 4` vertices is a tree | P62 | AND | algebraic/logical step | count | discharged |
| L71 | Lemma 7.1, recovery of the two trees | C0 | AND | major claim | R1a to R1e | discharged |
| R1a | white tree `W_s` | L71 | AND | named theorem | plane-tree duality, proved in 7.1 | discharged |
| R1b | one selected side per face, `|P| = n + 1` | L71 | AND | algebraic/logical step | rooted tree at `y0` | discharged |
| R1c | `P0` is a forest | L71 | AND | algebraic/logical step | C41 for `s`, selected-side count | discharged |
| R1d | `P` has two components, `e0` joins two roots | L71 | AND | algebraic/logical step | out-degree count | discharged |
| R1e | the components are induced trees | L71 | AND | named theorem | Jordan curve, duality | discharged |
| G73 | recursive cutting and gluing | C0 | AND | proved earlier | C12, H1 to H4 | discharged |
| H1 | cap colours are forced | G73 | AND | algebraic/logical step | three signs, divisibility | discharged |
| H2 | both labels occur on the cap | G73 | AND | algebraic/logical step | no monochromatic triangle in a tree | discharged |
| H3 | glued classes induce trees | G73 | AND | algebraic/logical step | no edge between open sides | discharged |
| H4 | termination, additivity of `|V(T)| - 3` | G73, TB | AND | algebraic/logical step | count | discharged |
| XC | proofs for the breadth-first and random-walk constructors | none | separate | missing | companion not supplied | open |

## 5. Verdict

**FOLLOWS** for Theorems 1.1, 1.2, 5.2, 5.3, Lemma 6.1 and Proposition 6.2. The decisive nodes are `S6` and `S7` (the exact obstruction), `C41`, `C42`, `Y3`, `M5` and `R1c`.

The remarks about the companion's alternative constructors (`XC`) are **INDETERMINATE FROM THE PROVIDED MATERIAL**. No theorem depends on them.
