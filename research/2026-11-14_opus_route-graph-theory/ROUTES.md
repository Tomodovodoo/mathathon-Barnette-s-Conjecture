# Routes tried

Opus 5.5, 2026-11-14. Each route has a status, the evidence, the smallest counterexample when there is one, and the lesson. Scripts are in `code/` and outputs in `code/data/`; `code/README.md` gives the commands. "Rooted instance" means an Eulerian triangulation with a chosen root face `t0` (coloured black) and no separating triangle with black inner boundary, so that pairs exist.

The census behind every exhaustive claim is all Eulerian triangulations with `V <= 16` up to isomorphism: 1, 0, 1, 1, 2, 2, 8, 8, 32, 57, 185 for `V = 6..16` (`COMPUTED`, generator validated against an independent flip enumeration for `V <= 12`). Random instances come from random degree-4 insertions starting at the octahedron. They are not uniform; treat them as stress tests, not samples.

| Route | Question | Status |
| --- | --- | --- |
| M1 | Is one of the three constraints redundant? | REFUTED (octahedron, `V = 8`) |
| M2 | Is `TM` the base family of a matroid? | REFUTED (octahedron) |
| M3 | Is the natural LP relaxation integral? | REFUTED (`V = 13`) |
| M4 | Is the problem a two-matroid intersection in general? | REFUTED in the abstract class (NP-hard, PROVED-HERE modulo [ANS]) |
| M5 | Hole test for a hidden two-matroid structure | inconclusive (no hole for `V <= 13`) |
| O1 | Is the minimum (maximum) of the matching lattice a tree matching? | REFUTED (`V = 10`; "min or max" `V = 12`) |
| O2 | Do min and max of the matching lattice form a tree pair? | REFUTED (`V = 10`, not even disjoint) |
| O3 | Does every 2-factor of `B` (every `D`) contain a tree pair? | REFUTED (`V = 40`) |
| O4 | Does the minimal alpha-orientation contain a tree pair? | REFUTED (`V = 40`) |
| O5 | Does the maximal alpha-orientation contain a tree pair? | REFUTED (`V = 80`) |
| O6 | Does the min or the max always contain a tree pair? | CONJECTURE (0 joint failures in 180 instances) |
| D1 | Strong descent: every D-swap through a Q-cycle lowers `k` | REFUTED (PROVED-HERE in principle; instance `V = 50`) |
| D2 | Weak descent: some single swap lowers `k` | REFUTED (`V = 50`) |
| D3 | Bounded-lookahead descent | open; two steps suffice on all traps found |
| I1 | Degree-4 induction: lift tree matchings through expansion | REFUTED as stated; precise breaking point PROVED-HERE |
| P1 | Induced-tree partitions = tree matchings? | REFUTED (`V = 8`); exact image PROVED-HERE |
| F1 | Exact obstruction to pairs, clean proof | PROVED-HERE (Euler identity) |
| F2 | Hall-free construction of a pair | open |
| G1 | Gluing and the primal hypothesis | PROVED-HERE; Li's hypothesis is sufficient, not sharp |

---

## M. Matroid routes

**Formulation (PROVED-HERE, PROOFS Lemma 1.1).** A tree matching is a common basis of three matroids on the spokes: the cographic matroid of `H` and two partition matroids (one spoke per bounded centre, one spoke per nonroot). In `T` it is a common basis of the graphic matroid of `T/R`, "one edge per bounded black face" and "one edge opposite each nonroot". Tree/cotree duality turns the triple into another triple of the same shape: graphic, plus two partition matroids whose blocks are the two ends of each spoke. Planarity does not merge two of the three. The second degree condition dualises to "the white tree `s*` has exactly one edge on each vertex-face of `H*`", which is again a partition condition, not a graphic one.

**M1. Redundancy** (`COMPUTED`, `code/exp_matroid.py`, `data/matroid_12.txt`, all rooted instances `V <= 12`).

- BT := graphic ∩ black-face partition. The octahedron has `|BT| = 14` against `|TM| = 2`.
- OT := graphic ∩ opposite-vertex partition. At the octahedron `OT = TM`, but at `V = 8` (dual of the hexagonal prism) `|OT| = 6` against `|TM| = 2`.
- States (the two partition matroids): at `V = 8`, 3 states and 2 tree matchings.
- In every instance `TM = BT ∩ OT`, and neither of `BT`, `OT` contains the other.

Lesson: all three constraints carry information already at 6 and 8 vertices.

**M2. Matroid structure.** `BT`, `OT` and `TM` all fail the basis-exchange axiom in every instance, including the octahedron (`COMPUTED`, same script). For `TM` this is forced: a tree matching and its unique mate are disjoint, and nothing lies between them.

**M3. Integrality of the natural relaxation** (`COMPUTED`, `code/exp_lp.py`, `data/lp_13.txt`). Let `P` be the set of fractional perfect matchings `x` of `B` such that `1 - x` lies in the spanning-tree polytope of `H`. Separation is exact: subtour constraints are found by `|V(H)|` min-cuts. Its integer points are exactly the tree matchings. Over 10 random objectives per rooted instance:

- no fractional optimum was found for `V <= 12`;
- at `V = 13`, 4 of 126 instances have an LP optimum strictly above every tree matching.

The fractional vertex found is half-integral, the average of two states on seven faces. Neither state is a tree matching, but their average satisfies all subtour constraints. Lesson: the obstacle to a polyhedral proof is "two non-trees average to a fractional tree". That is the same phenomenon the signed count controls, because pairs differing on a cycle carry opposite signs.

**M4. Complexity of the abstract problem** (PROOFS Prop. 1.2, PROVED-HERE, using the NP-completeness of Hamiltonian cycle in cubic bipartite planar graphs, `LIT` [ANS], not opened here). Deciding whether a planar bipartite graph of maximum degree 3 has a perfect matching whose complement is a spanning tree is NP-hard. So the tree-matching problem is not a matroid intersection in any form that ignores the special shape of spoke graphs: all faces hexagons, all centres of degree 3, the root structure. Any min-max proof must use that shape. The density inequality (3.2) uses exactly hexagonal faces and the colour balance, so it could in principle enter. But for a three-matroid problem there is no min-max template to verify it against.

**M5. Hole test** (`COMPUTED`, `code/exp_hole.py`, `data/hole_13.txt`). If `TM` were the common bases of two matroids on the spoke set, no non-tree state could lie in `conv(TM)`. None does for `V <= 13`. So this cheap test cannot exclude a hidden two-matroid description on the spoke set. M3 excludes the natural one.

**Verdict on the matroid-intersection question.** The tree-matching condition is a three-matroid intersection: one graphic or cographic matroid and two partition matroids. Planar duality maps it to another three-matroid intersection, not to a two-matroid one. It is not matroid union or matroid parity in any natural way I found. The general problem class is NP-hard, and the natural LP relaxation is not integral (`V = 13`). So no Edmonds-type min-max condition can be written down and checked against (3.2), and there is no polynomial algorithm from this route. One could still try a delta-matroid or Eulerian-system view: the pairs, grouped by their 2-factor, look like Bouchet's transition systems. I did not get far enough to tag it. This is a door, not a corridor.

---

## O. Orientation and lattice routes

**Basic structure (PROVED-HERE, PROOFS Lemma 3.1).** States are perfect matchings of the plane bipartite graph `B`. They form Propp's distributive lattice under rotation around white triangles avoiding the roots. 2-factors of `B` (pairs up to reversing `D`-cycles) are exactly the alpha-orientations of `H_0` with out-degree 2 at bounded centres, `d_x - 2` at nonroots and `d_r - 1` at roots. Equivalently, they are the "deleted corner" maps `u`. These form Felsner's lattice.

**O1, O2. Matching lattice** (`COMPUTED`, `code/exp_lattice.py`, `exp_mate.py`; `data/lattice_13.txt`, `data/mate_12.txt`).

- The lattice minimum and maximum are unique in every instance.
- The minimum is a tree matching in 28 of 32 rooted instances at `V = 10`, so not always. Smallest failure: the first `V = 10` example in `data/lattice_13.txt`.
- "Min or max" holds up to `V = 11` and fails at `V = 12` (10 of 120 instances).
- The pair (min, max) is often not even disjoint: 8 of 32 instances at `V = 10`.
- The mate of a tree matching shows no orientation pattern: the cycles of `D(r,s)` come in every cw/ccw mixture.

Lesson: rotation around white triangles changes `s`. The obstruction to a tree lives in cycles of `Q_s`, and reversing those changes only `r`, so it is invisible in the `s`-lattice.

**O3–O6. Alpha-orientation lattice** (`code/exp_alpha.py`, `exp_alpha2.py`, `exp_every_factor.py`, `exp_ef_lattice.py`, `verify_ef.py`).

- For `V <= 13`, `B` has almost always exactly one 2-factor (122 for 120 instances at `V = 12`, 132 for 126 at `V = 13`), and every 2-factor contains a tree pair (`COMPUTED`, exhaustive). Up to `V = 12` the minimal and maximal alpha-orientations always contain one, but that test is close to vacuous at these sizes.
- **O3 REFUTED.** At `V = 40` there is a 2-factor without any tree pair (`data/ef_fail_40_40.json`, verified by `verify_ef.py`). It is a single cycle `D` through all 37 nonroots, and both orientations `(r,s)` and `(s,r)` have cyclic `Q`. The triangulation has no separating triangle at all.
- **O4 REFUTED.** That same 2-factor is the face-flip minimum (no ccw-directed flippable face).
- **O5 REFUTED.** At `V = 80` the face-flip maximum is a single-cycle 2-factor without tree pair (`data/alpha_max_fail_80_83.json`). Failure rates over random instances:
  - min fails 1/60 (`V = 40`), 2/60 (`V = 60`), 3/60 (`V = 80`), 6/60 (`V = 120`);
  - max fails 0, 0, 3/60, 4/60.
- **O6 CONJECTURE.** "The face-flip min or the face-flip max contains a tree pair." Over 180 random instances at `V = 80, 100, 120`, the min failed 14 times and the max 11 times, but never both together (`data/alpha_max_V80.txt`, `data/alpha_V120_both.txt`). If the failures were independent we would expect about one joint failure. Test: random instances at `V = 150-300`, and an exhaustive check once a census reaches `V >= 40`, which is out of reach for my Python generator.

Caveat: "face-flip minimum" is the greedy result of flipping ccw-directed bounded faces. On `V <= 12` it is unique from every start and equals the enumerated lattice minimum. On larger instances I did not verify that facial flips generate Felsner's lattice: rigid edges at the roots can create essential cycles that are not faces.

Lesson: one-cycle 2-factors are the enemy. If `D` is a single cycle, the only two pairs are `(r,s)` and `(s,r)`, and both can fail. The sign argument copes with this because such a group contributes at the lowest order only together with other groups. A structural proof has to move between 2-factors, by `Q`-reversals, not just choose inside one.

---

## D. Descent routes (local search in the exchange graph)

Potential: `k(s)` = number of cycles of `Q_s` (unicyclic components). `s` has `2^k` mates, and `k = 0` means tree matching.

**D1 Strong descent: REFUTED.**
- Exhaustively for `V <= 15`, every D-swap along a `D`-cycle that meets a `Q`-cycle lowered `k` by exactly 1, and swaps along `D`-cycles missing all `Q`-cycles left `k` unchanged (`data/moves_13_15.txt`). Random `V = 30`: 837 such moves, all with `dk = -1`.
- The statement is false in principle (PROOFS Prop. 8.1): if `D` is one cycle, the swap exchanges `r` and `s`, so it cannot lower `k` in both directions.
- Instance: `V = 50`, `data/strongviol_50_seed50.json`. The swap along a 47-cycle leaves `k = 1`. At `V = 50`, 180 of 2,599 tested moves had `dk = 0` (`data/strong_V50.txt`). At `V = 80`, 14 moves had `dk = +1`.

**D2 Weak descent: REFUTED.** At every pair with `k > 0`, ask whether some D-swap, under some mate, lowers `k`.
- Exhaustive `V <= 15`: always yes (`data/descent_15.txt`).
- Random: a weak trap (no decreasing swap under the current mate) first appears at `V = 30` (`data/weaktrap_30_seed37.json`).
- A deep trap (no decreasing swap under any of the `2^k` mates) at `V = 50`: `data/deeptrap_50_1.json`. It has no separating triangle, `k = 1`, and every swap under both mates keeps `k = 1`.
- Deep traps are rare: about 1 hit per 4,000 sampled pairs with `k > 0` at `V = 50`.

**D3 Bounded lookahead: open.** In every trap found, two consecutive D-swaps reach `k = 0` (`verify_trap.py`). CONJECTURE (weak, test: search for pairs with no `k`-decrease within 2 swaps at `V >= 80`): from every pair with `k > 0`, some sequence of D-swaps and Q-reversals along which `k` never increases reaches `k = 0`. If true, this gives a structural proof that every exchange component contains a tree pair (BT Thm 5.2) without signs. It would not give a polynomial bound, since plateaus can be long.

Lesson: the cancellation in the counting proof is global, and single exchanges cannot track it. The failures all involve long `D`-cycles (Hamiltonian or nearly so on `X`), which are exactly where the swap symmetry `(r,s) <-> (s,r)` bites.

---

## I. Direct induction (degree-4 expansion)

**Generation (PROVED-HERE, PROOFS Lemma 6.1).** Every Eulerian triangulation is obtained from the octahedron by degree-4 insertions (vertex splits along two neighbours with odd arcs) and face gluings. Every 4-connected one with `V > 6` has a reducible degree-4 vertex.

**Lift lemma (PROVED-HERE, PROOFS Lemma 6.2; `COMPUTED` check `data/lift_13.txt`, 1,920 cases).** States of `T'` correspond bijectively to the states of `T` whose two new black faces avoid `a, b`. The lift of `s'` is a tree matching iff a boundary condition holds: `c2` must lie on the `v_o`-side after splitting `v` in the tree `Q_{s'} + R`.

**Where it breaks** (`COMPUTED`, `data/induction_13.txt`).
1. Contraction can create a black-inner separating triangle, so `T'` may have no tree matching while `T` does: 132 of 1,648 cases, first at `V = 11`.
2. When `T'` has tree matchings, some of them lift (all 1,516 cases), but in 708 cases not all do.

An induction would need the hypothesis "for every vertex `v` and every split of its rotation into two odd arcs, some tree matching satisfies the side condition". That hypothesis is not preserved by the step in any way I could see, because the side condition at one vertex says nothing about the next. Lesson: degree-4 induction controls states perfectly and trees not at all. The tree condition is global (connectivity through `v`), while the expansion is local.

---

## P. Two induced trees directly

**Exact relation (PROVED-HERE, PROOFS Thm 7.2).** The OpenAI construction `s -> partition` is injective with explicit left inverse `derive` (orient the monochromatic forest minus `e0` towards the roots and read off tails). Its image is exactly the set of partitions whose white parent map is acyclic.

**Not onto** (`COMPUTED`, `data/induced_12.txt`, `data/induced2_12.txt`).
- At `V = 8`, 4 of 12 rooted instances have 2 tree matchings but 4 partitions.
- Using both faces through `e0` (black root, or white root with colours swapped) still misses partitions: at `V = 12`, for 118 of 209 edges.

So Hamiltonian cycles avoiding `e` are strictly more numerous than tree matchings at either root. Tree matchings are a rigid, root-dependent certificate.

**Other partition-level tools.**
- Grinberg's identity is automatic for any two-induced-tree partition (PROOFS 9.1), so Grinberg-type counts carry no information here. The Eulerian form `sum_{v in U}(d_v - 1) = n` is just the edge count of two trees.
- Black and white faces both split as `|U| - 1` and `|U'| - 1` (PROOFS 9.2). This is the only place I found where the colouring talks to the partition directly. It is the combinatorial content of the disk identity.
- Decycling sets: `U'` is a decycling set of `T` whose complement is a tree and which itself induces a tree. I found no useful interaction with the colouring beyond 9.2. HUNCH only: Stein's B-set framework (`LIT`, Stein 1971, cited by OpenAI; not opened here) phrases the same partitions, but its known results are for special face sizes.
- Tutte-path or bridge arguments: not attempted. They give long cycles in 4-connected planar graphs, but `G` is cubic and only 3-connected. The dual statement (paths in `T`) does not obviously produce induced trees.

---

## F. The first step (pairs)

**F1 (PROVED-HERE, PROOFS Thm 2.1).** A pair exists iff no separating triangle has black inner boundary. The proof uses one exact Euler identity, `m - b - (2p - 4) = (1/2) sum_regions (beta - (d - 4))`, plus the signed side count. Every region contributes `<= 0` except black-inner separating triangles, which contribute `+1` each. This replaces the inequality chain of OpenAI §3 and BT §3 by one identity and one table. Verified exhaustively against max-flow for all 7,868 rooted instances `V <= 16` (`data/obstruction_16.txt`).

**F2 Hall-free construction: open.** PROOFS Lemma 3.1 recasts a pair as an alpha-orientation (each black face deletes one corner, each nonroot deleted `d_x - 2` times). HUNCH: a canonical-ordering (shelling) construction from `t0` inward, as for Schnyder woods, should produce one directly. The certificate of non-existence is always a single triangle, which is how density conditions behave when a shelling exists. Not tested.

---

## G. Gluing and the primal hypothesis

**G1 (PROVED-HERE, PROOFS §4–5).** The gluing of OpenAI §7 holds verbatim when splitting only at black-inner separating triangles (as in BT §7.3). In the primal:

- separating triangles are nontrivial 3-edge cuts;
- each such cut has all black ends on one side and all white ends on the other (Li App. C);
- the obstruction is exactly a cut whose black-ended side avoids `b0`.

So Li's Lemma 9 holds under the sharp hypothesis "every nontrivial 3-edge cut has `b0` on its black-ended side". Cyclic 4-edge-connectivity is sufficient but not necessary: 1,714 of the 4,494 rooted instances with a separating triangle still have pairs for `V <= 16`.

Li's Lemma 9 proof: I checked the steps I used (minimal deficit set, `W_1` empty, the face count). One point is stated loosely: "GS is 2-connected" needs the fact that two faces of a cubic plane graph meeting at a vertex share an edge. It holds, and the conclusion is not affected.
