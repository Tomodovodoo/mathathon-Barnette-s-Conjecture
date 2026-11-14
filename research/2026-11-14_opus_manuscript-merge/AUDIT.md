# Reverse-Lamport audit of `paper/main/barnette.tex`

Method: `skills/reverse-lamport/SKILL.md`, from Theorem 1.1 backward, over the route the manuscript supplies. I wrote the manuscript, so this is the author's audit, not an independent one. Status of the whole: `PROVED-HERE` (the manuscript), with the example numbers `COMPUTED` by `example.py` (output `example.txt`).

## 1. Audit boundary

**Conclusion C0 (Theorem 1.1).** For every finite simple graph `G` that is cubic, bipartite, planar and 3-connected (at least four vertices; connected after deleting any two) and every edge `e` of `G`, some Hamiltonian cycle of `G` does not contain `e`.

**Hypotheses.** As stated; a sphere embedding of `G` with polygonal edges is fixed.

**Accepted primitives.**
- P1 Jordan curve theorem for polygonal closed curves on the sphere: two open disks, the curve is the boundary of each.
- P2 Euler's formula `V − E + F = 2` for a connected plane graph (connectedness checked at each use).
- P3 Plane duality basics: each dual edge crosses its own edge once and no other; edges and faces alternate around a vertex; the dual face containing a vertex `v` is bounded by a closed walk through the faces at `v`.
- P4 Integral max-flow min-cut (Ford-Fulkerson).
- P5 Finite graph facts: a nonempty edge set with all degrees even contains a cycle; a connected 2-regular graph is a cycle; trees have `q − 1` edges, a connected graph with `q` vertices and `q` edges has one cycle; a cycle meets an edge cut evenly; a tree has at most one perfect matching; Hall's theorem for regular bipartite graphs.

Not accepted without proof: anything about states, the disk identity, connectedness of `T`, of `R_Z` or of the pieces.

## 2. Obligation graph (all groups AND; one supplied route per claim)

```text
C0  Thm 1.1            <- L2.1, T6.2, P2.6(1), O-avoid
L2.1 T coloured triang. <- O-cut, O-simple, O-tri, O-four, O-colour
T6.2 acyclic selection containing e0, all coloured T, t0, e0
                        <- induction on |V|: O-dichotomy, CaseA, CaseB
CaseA (no sep. triangle) <- O-swap, P5.2, P4.8, P3.9
CaseB                   <- L6.1, IH(T1), IH(T2), O-union-sel, O-union-acyc
P2.6 (1) Ham. cycle, (2) two components / edge in P iff ends together
                        <- L2.5, O-conn-T, (2.3)
L2.5 duality            <- P1, P3, P5, P2
L2.2 faces bounded by cycles => connected <- P1 (sphere connected), definitions
O-conn-T                <- L2.2
P3.9 good => P_s acyclic selection ∋ e0 <- L3.6, L3.5, L3.7, L3.8, O-match, O-e0-not-inside
L3.6 Y_s tree; P_s selection <- L3.5, L2.5(2), O-conn-T, O-one-side
L3.8 disk identity      <- O-noroot, O-RZ (L2.2), P2, O-sides, O-state-count
P4.8 a pair => a good state <- L4.5, L4.4, L4.6, L4.7, O-class, O-min
L4.5 cancellation       <- L4.3(1), L4.4, L4.2, O-Ks
L4.4 sign               <- O-local-delta, L3.8 (odd length; δ-sum ±3)
L4.6 heights            <- O-path, O-turn-cases, L2.5(1), L3.8 (L ≥ 1)
L4.2 partner            <- L3.7
P5.2 a pair             <- P4, O-translate, O-components, O-tri-face, O-bal, P2
L6.1 cap colour, pieces <- signed side count, L2.2, simplicity
```

No cycle: L3.8 uses only bijectivity of a state and P1, P2, L2.2. L4.6 uses L3.8 only for `L(C) ≥ 1`. P4.8 does not use P3.9; P3.9 does not use any pair.

## 3. Critical points checked

- **O-RZ (the gap found in draft B).** The paragraph "The inside of a cycle" identifies the faces of `R_Z` (outside of `Z` plus the inner faces of `T`), each bounded by a cycle, then applies L2.2. Edge count `(3(B+W)+h)/2` follows. Discharged.
- **O-conn-T, O-conn-piece.** Stated after L2.2 and inside L6.1. Discharged.
- **O-e0-not-inside (draft A's N12c).** Prop 3.9: "it is not `e0`, whose ends are roots"; the roots are outside `Z` by O-noroot. Discharged.
- **O-one-side.** Two faces share at most one side, proved after L2.1, used in L3.6. Discharged.
- **O-translate (draft A's N5b).** `b(U)` counts `t0`; the left side of (5.1) is `2n − (e(U)−3) + (b(U)−1)`. Re-derived. Discharged.
- **O-local-delta.** `δ(u,s) = −δ(r,s)` and `δ(s,r) = −δ(r,s)`, from "the three directed edges run the same way round". Discharged.
- **O-turn-cases (new proof of L4.6).** Four cases checked with coordinates (DECISIONS section 4). Each crossing of the path with `C` is counted once at a face of `A`, which is neither end of the path. Discharged; `COMPUTED` on 16 reversals.
- **O-class.** The undirected edge set of `D` has one side per face of `A`; consecutive faces on a cycle agree; the class is the `2^c` orientations. Discharged.
- **O-min / sign alignment.** Lemma 4.4 gives `ε = (−1)^{(n+c)/2}(−1)^{c⁺}`; with Lemma 4.7 every class with `c = m` contributes `(−1)^{(n−m)/2} m! ∏ L > 0` times one sign. This is the one use of the exact value `±3` of the δ-sum; the other uses need only odd length. Discharged.
- **O-Ks.** The reversed `Q_s`-cycle depends on `s` only. Discharged.
- **O-tri-face.** The only use of "no separating triangle". Discharged.
- **O-union-acyc.** Uses P2.6(2) in both pieces and simplicity of `T` (an edge of `T_2` with both ends in `Δ` is a side). Discharged.
- **Remarks.** "A cycle arises iff its state is good": uses P5 (a tree has at most one perfect matching) and that the complement avoids `S_{s_C}`. The polynomial identity uses L4.2, L4.4, L4.5. Both off the route to C0.

## 4. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Thm 1.1 | root | R0 | root | L2.1, T6.2, P2.6(1), O-avoid | discharged |
| O-avoid | `e ∈ P*` when `e0 ∈ P` | C0 | R0 | definition | Def. 2.4 | discharged |
| L2.1 | `T` simple, ≥ 4 vertices, triangular faces, 2-coloured | C0 | R0 | major claim | O-cut … O-colour | discharged |
| O-cut | no edge cut of size ≤ 2 | L2.1 | AND | hypothesis | 3-connected, cubic, simple | discharged |
| O-simple | no loop or parallel pair in `T` | L2.1 | AND | side condition | O-cut, P1 | discharged |
| O-tri | faces are triangles | L2.1 | AND | algebraic/logical step | P3, simplicity | discharged |
| O-four | `|V(T)| ≥ 4` | L2.1 | AND | named theorem | P2 on `G` | discharged |
| O-colour | proper face colouring | L2.1 | AND | hypothesis | bipartition | discharged |
| O-one-side | two faces share ≤ 1 side | L3.6 | AND | algebraic/logical step | simplicity, ≥ 4 vertices | discharged |
| L2.2 | faces bounded by cycles ⇒ connected | O-conn-T, O-RZ, L6.1 | AND | major claim | P1, openness argument | discharged |
| (2.3) | `k` black = `k` white, `3k` edges, `k+2` vertices | P2.6, Sec. 3, P5.2 | AND | named theorem | P2, O-conn-T | discharged |
| L2.5 | duality lemma | P2.6, L3.6, L4.6 | AND | major claim | P1, P3, P5, P2 | discharged |
| P2.6 | acyclic selection: Ham. cycle; two components; edge iff ends together | C0, P3.9, L3.1, T6.2 | AND | major claim | L2.5, (2.3), P5 | discharged |
| T6.2 | acyclic selection ∋ `e0` | C0 | induction | major claim | CaseA, CaseB | discharged |
| L3.5 | good ⇔ `S_s` spanning tree | L3.6 | AND | algebraic/logical step | edge count, P5 | discharged |
| L3.6 | `Y_s` tree; `P_s` selection ∋ `e0`, side at `s(t)` | P3.9 | AND | major claim | L3.5, L2.5(2), O-one-side | discharged |
| L3.7 | outdegree ≤ 1 ⇒ cycles directed; component count | P3.9, L4.2 | AND | algebraic/logical step | P5 | discharged |
| O-noroot | `Z` avoids and does not enclose roots | L3.8 | AND | side condition | outdegree, P1 | discharged |
| O-RZ | `R_Z` connected, faces = inner faces + outside | L3.8 | AND | side condition | P1, L2.2 | discharged |
| O-sides | `3(B−W) = 2ℓ − h` | L3.8 | AND | algebraic/logical step | colouring | discharged |
| O-state-count | `B = I + ℓ` | L3.8 | AND | algebraic/logical step | bijectivity, P1 | discharged |
| L3.8 | `W = B + 1`, `h = 2ℓ + 3` | P3.9, L4.4, L4.6 | AND | major claim | above | discharged |
| O-match | `B − ℓ = W − (h − ℓ)` | P3.9 | AND | algebraic/logical step | one selected side per face | discharged |
| O-e0-not-inside | no face inside `Z` selects `e0` | O-match | AND | side condition | roots outside | discharged |
| P3.9 | good ⇒ `P_s` acyclic | CaseA | AND | major claim | above | discharged |
| L4.2 | partner: outdegrees; components; good ⇔ acyclic; one partner | L4.3, L4.5 | AND | major claim | L3.7 | discharged |
| L4.3 | both reversals give pairs; (1) involutive | L4.5, O-class | AND | major claim | L4.2 | discharged |
| O-local-delta | `δ(u,s) = −δ(r,s)` | L4.4 | AND | algebraic/logical step | orientation of a triangle | discharged |
| L4.4 | both reversals flip `ε`; `ε = (−1)^{(n+c)/2}(−1)^{c⁺}` | L4.5, P4.8 | AND | major claim | L3.8, O-local-delta | discharged |
| O-Ks | cycle chosen from `s` alone | L4.5 | AND | side condition | fixed order | discharged |
| L4.5 | cancellation | P4.8 | AND | major claim | L4.3(1), L4.4 | discharged |
| O-path | path of faces exists, no repeats | L4.6 | AND | algebraic/logical step | `G` connected | discharged |
| O-turn-cases | summand = ±1 by crossing direction | L4.6 | AND | algebraic/logical step | four cases | discharged |
| L4.6 | height jump `[y inside C]`; `L(C) ≥ 1` | P4.8 | AND | major claim | L2.5(1), L3.8 | discharged |
| L4.7 | finite difference | P4.8 | AND | algebraic/logical step | expansion | discharged |
| O-class | class = `2^c` orientations | P4.8 | AND | algebraic/logical step | L4.3(2), one side per face | discharged |
| O-min | `m ≥ 1` exists; every class has `c ≥ m` | P4.8 | AND | hypothesis | a pair exists, finiteness | discharged |
| P4.8 | a pair ⇒ a good state | CaseA | AND | major claim | above | discharged |
| O-translate | (5.1) ⇔ (5.3) | P5.2 | AND | algebraic/logical step | `b(U)` counts `t0` | discharged |
| O-components | component bounds sum to (5.3) | P5.2 | AND | algebraic/logical step | faces' corners pairwise adjacent | discharged |
| O-tri-face | length-3 faces of `H` are faces of `T` | P5.2 | AND | hypothesis | no separating triangle, P1 | discharged |
| O-bal | `bal(F) ≤ d_F − 4` | P5.2 | AND | algebraic/logical step | parity, divisibility | discharged |
| P5.2 | no separating triangle ⇒ a pair | CaseA | AND | major claim | P4, above, P2 | discharged |
| L6.1 | cap colour forced; piece is a smaller coloured triangulation | CaseB | AND | algebraic/logical step | signed sides, L2.2 | discharged |
| O-union-sel | `P1 ∪ P2` is a selection ∋ `e0` | CaseB | AND | algebraic/logical step | shared edges = sides of `Δ` | discharged |
| O-union-acyc | `P1 ∪ P2` acyclic | CaseB | AND | algebraic/logical step | P2.6(2) in both pieces, simplicity | discharged |

## 5. Verdict

**FOLLOWS** on the supplied route, within the boundary above. Decisive nodes: L3.8 (the only place where bijectivity of a state enters a count), L4.4 and L4.6 (which consume it), O-RZ and L2.2 (the connectedness the drafts lacked), O-tri-face (the only use of "no separating triangle") and O-union-acyc (which consumes P2.6(2)). This is the author's own audit of a text written in one sitting; a cold read by someone who has not seen the drafts is the right next check.
