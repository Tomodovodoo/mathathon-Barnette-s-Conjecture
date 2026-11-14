# The three conjectures: precise statements, status, evidence

Notation as in `research/BRIEF.md`. Proofs referred to as "Lemma n" are in `PROOFS.md`. Commands are in `code/README.md`. "Rooted instance" means a 3-connected Eulerian triangulation `T` together with a face `t0` coloured black, every face counted (this is the convention of the combinatorics folder: 7,868 rooted instances up to 16 vertices, 5,088 of them with a pair).

## 1. Definitions, and how the two source folders' conventions fit together

**2-factors and pairs.** A 2-factor of `B` is recorded by its deleted-corner map `u` (`u(t)` = the corner of `t` the 2-factor does not use; at a face with a root corner, `u(t)` is the root). Its D-edges are the sides `{a, b}` of each `t` opposite `u(t)`. They form `c(u)` disjoint cycles through all nonroots. The ordered pairs `(r, s)` with deleted corners `u` are the `2^{c(u)}` orientations of these cycles, with `r(t) -> s(t)` along each. `c_min` is the least `c(u)`.

**The lattice.** `H_0` is the spoke graph without the centre of `t0`. `O_u` orients `H_0` by `u(t) -> t` and `t -> v` for the other two corners. These are exactly the alpha-orientations for out-degrees 2 (centres), `d_x - 2` (nonroots), `d_r - 1` (roots), where `d` counts black faces at a vertex (graph-theory folder, PROOFS Lemma 3.1). Lemma 1 identifies them with integer potentials on the faces of `H_0`. The faces are the hexagons around inner white faces plus one outer face. The potentials satisfy one difference constraint per spoke, and the componentwise order makes them a distributive lattice. This is Felsner's lattice, and it is what the graph-theory report means.

**Flips.** A cover move raises (or lowers) by 1 the potential on an inclusion-minimal set of faces that is forced to move together. Geometrically, it reverses a directed cycle that bounds that set. When the set is a single hexagon this is the "face flip" (rotate `u` around a white triangle avoiding the roots). When rigid spokes glue several hexagons, the cover move reverses the boundary of their union, and single hexagon flips cannot perform it.

**Extremes.** `E_lo` is the least element and `E_hi` the greatest. `E_lo` has no clockwise directed cycle and `E_hi` no counterclockwise one (Lemma 1; faces of `T` traced with the interior on the left count as counterclockwise). `code/bar.c` computes both exactly with two shortest-path computations.

**Reconciliation.**
- The graph-theory folder's "face-flip minimum/maximum" is a greedy single-hexagon descent/ascent. In 7 of its 9 saved files it stops at a local extreme that is not the extreme of the lattice (`code/checku.py`, PROOFS Remark 1.1). Its labels are mirror images of mine: on `ef_fail_40_40.json` its "minimum" is my `E_lo`. C2 is symmetric under reflection, so the labels do not matter for C2.
- The combinatorics folder orients state cycles and uses `delta`. Its "all-clockwise orientation of a cube" is a statement inside one 2-factor (one cube), not about the lattice of 2-factors.

**"Carries a tree pair."** The 2-factor `u` carries a tree pair if some orientation `(r, s)` of its D-cycles has `Q_s` a forest, equivalently `s` a tree matching (Lemma 2). Lemma 2 also gives a criterion inside `O_u`: `(r, s)` is a tree pair iff no directed cycle of `O_u` leaves every centre `t` it passes towards `r(t)`.

**Exchange moves** (for C3), on ordered pairs `(r, s)`:
- a *D-swap* along a cycle `C` of `D(r, s)` exchanges `r` and `s` on the faces of `C`. It stays in the same 2-factor and changes `s`.
- a *Q-reversal* along a cycle `K` of `Q_s` sets `r(t) := u(t)` on the faces supplying `K`. It keeps `s`, so it keeps `k`, and it moves to another 2-factor.

Here `k(r, s) = k(s)` is the number of cycles of `Q_s`.

## 2. Status table

| Id | Statement | Status | Evidence / witness |
| --- | --- | --- | --- |
| C2 (O6) | `E_lo` or `E_hi` carries a tree pair | `REFUTED` | Smallest witness `V = 18`: `data/c2_counterexample_V18.json`, checked independently (`code/verify_c2.py`, reference lab) |
| O4, O5 | `E_lo` carries a tree pair; `E_hi` carries a tree pair | `REFUTED` (each, for the true extremes) | `V = 18` again: both fail together. Single failures at `V = 18` (28 and 30 rooted instances) |
| R1 | some element at cover-distance `<= 1` from `E_lo` or `E_hi` carries a tree pair | `REFUTED` | Exhaustive: true for `V <= 23`, one failure at `V = 24` (`data/r1_counterexample_V24.txt`, independent check `code/verify_near.py`). Random: distance 2 at `V = 150, 200, 250` |
| R2 | some extreme, join-irreducible or meet-irreducible element carries a tree pair | `COMPUTED` true for `V <= 22` exhaustively. Not tested beyond | Weak test: lattices there have at most 12 elements |
| R3 | every maximal chain from `E_lo` to `E_hi` meets an element carrying a tree pair | `REFUTED` | Exhaustive: true for `V <= 24` (all 11,637 both-fail instances). Random: fails at `V = 60` (`data/r3_counterexample_V60.txt`, independent check) |
| R5 | at least half of the 2-factors carry a tree pair | `REFUTED` | Exhaustive: true for `V <= 22`, attained with equality (4-element lattices). Random: 109/235 at `V = 70`, 2427/6032 at `V = 90` (`bar.c` only) |
| C1 | `#TM >= 2^{c_min}` | `CONJECTURE`, `COMPUTED` | Exhaustive `V <= 22`: 4,656,948 rooted instances with a pair, no violation. Random up to `V = 100` |
| C1= | `#TM = 2^{c_min}` iff `B` has exactly one 2-factor | "if": `PROVED-HERE` (Lemma 3). "only if": `CONJECTURE`, `COMPUTED` | Exhaustive `V <= 22` (equality count = one-element-lattice count at every `V`) and all random runs |
| C3 (D3) | from every pair, `k` reaches 0 by exchange moves that never increase `k` | `CONJECTURE`, `COMPUTED` (random only) | 940 random starts with `k > 0`, `V = 60..150`; the three saved traps of the graph-theory folder |

## 3. C2 in detail

**Prediction before the test:** survives to `V = 20` (60%). Wrong.

**Exhaustive counts** (`code/bar.c`, plantri `-b`, every face as root; `data/ext_fail_*.txt`, `data/ext_summary_23_24.txt`):

| V | rooted with a pair | `E_lo` fails | `E_hi` fails | both fail | lattice has one element |
| --- | --- | --- | --- | --- | --- |
| <= 17 | 13,130 | 0 | 0 | 0 | |
| 18 | 27,972 | 28 | 30 | 26 | 23,302 |
| 19 | 82,819 | 0 | 0 | 0 | 66,350 |
| 20 | 287,110 | 144 | 174 | 66 | 220,742 |
| 21 | 944,804 | 103 | 115 | 46 | 692,724 |
| 22 | 3,301,113 | 2,670 | 3,227 | 833 | 2,306,337 |
| 23 | 11,395,661 | 3,977 | 3,981 | 935 | 7,554,133 |
| 24 | 40,301,964 | 47,517 | 55,846 | 9,731 | 25,317,466 |

The 26 failures at `V = 18` come from two triangulations, one with degree sequence `4^6 6^12` (24 of its 32 roots fail) and one with `4^7 6^10 8`. Every failure at `V = 18, 20, 22` is 4-connected: `plantri -b -c4` gives the same counts. At `V = 21`, 44 of the 46 have a (white-inner) separating triangle.

**Random** (`data/random_B.txt`, `random_C.txt`): the joint failure rate grows with `V` and with degree skew. `ins`: 0 to 7 per 1,200 rooted instances at `V = 40..150`. `skew`: 24/1200 at `V = 100`, 116 and 124/1200 at `V = 150`, 182/1200 at `V = 200`, 276/1200 at `V = 250`.

**The smallest witness** (`data/c2_counterexample_V18.json`, `code/anatomy.py`). The lattice has four elements, a square. Both extremes are one Hamiltonian D-cycle of length 15, and both orientations fail. The two middle elements have three D-cycles (lengths 7, 3, 5) and 6 tree pairs out of 8 each. In total there are 12 tree matchings and `c_min = 1`, attained only at the two failing extremes.

**What goes wrong.** By Lemma 2 a 2-factor fails iff the subcubes excluded by its "dangerous" directed cycles cover all orientations (Corollary 2.1). At each extreme of the `V = 18` example, `O_u` has exactly two directed cycles, both facial hexagons around white triangles `y1`, `y2`. Corollary 2.2 says a directed hexagon around `y` kills exactly the orientations with `y` inside `Q_s`. On the single D-cycle the two hexagons exit in opposite directions, so orientation `+` puts `y1` into `Q_s` and orientation `-` puts `y2`. The other extreme is the mirror situation. The middle elements are reached by flipping exactly these hexagons, which splits the D-cycle into three. So the hexagons that block the extreme are the ones whose flip produces the tree pairs.

**Why the old evidence looked good.** Below `V = 18` the lattice almost always has one element, and there Lemma 3 makes every pair a tree pair. The 180 random instances of the graph-theory folder used the greedy local extremes, so they did not test C2 as stated.

**Why the hoped-for proof fails.** The brief asked whether at `E_lo` some orientation of all D-cycles must give a forest. Lemma 1 says every directed cycle of `O_u` at `E_lo` is counterclockwise. But whether a counterclockwise directed cycle is dangerous depends on its exits relative to the D-cycles, and the sense of a directed cycle in `H_0` does not control these exits. The `V = 18` example shows two counterclockwise hexagons with opposite exits on one D-cycle.

## 4. Replacements for C2

All four natural weakenings I could state fail, at increasing sizes:

- **R1** (within cover-distance 1 of an extreme). Prediction: fails by `V = 24` (55%). Correct: one failure at `V = 24`, out of 40.3 million rooted instances. There the extremes have 3 D-cycles each and a single cover each, both covers are Hamiltonian and fail, and all six elements at distance 2 carry tree pairs. At `V = 150` the extremes plus all 19 elements at distance 1 fail (`data/r1_dist2_instances.txt`, independently checked). The distance from the extremes to the nearest tree-pair element grows slowly: 2 is the largest seen up to `V = 250`.
- **R3** (every maximal chain meets a tree pair). This would have given a polynomial algorithm without a canonical element. It holds for all 11,637 both-fail instances with `V <= 24`, and fails at `V = 60` with a failing chain through 7 elements.
- **R5** (at least half the lattice carries tree pairs). Exhaustive to `V = 22`, tight at 1/2, and false at `V = 70`.
- **R2** (an irreducible element) is untested where it matters.

**Lesson.** The set of 2-factors carrying tree pairs has no visible order-theoretic shape inside Felsner's lattice: not near the extremes, not on every chain, not a majority. A canonical construction will need a different structure, for example one that couples the choice of 2-factor with the orientation of its cycles, which the lattice order ignores.

## 5. C1 in detail

**Statement.** `#TM >= 2^{c_min}` for every rooted instance with a pair.

**Evidence** (`data/full_summary_*.txt`, `data/full_le16.txt`). The histogram of `floor(#TM / 2^{c_min})` per `c_min` is in the summary files. Examples at `V = 22`: `c_min = 1` in 1,137,240 instances, `c_min = 3` in 2,016,472, `c_min = 5` in 147,401, and the ratio `#TM / 2^{c_min}` is always at least 1. Prediction: survives to `V = 20` (80%). Correct, and to `V = 22`.

**Equality.** In every exhaustive and random run, the equality count equals the number of instances whose lattice has exactly one element. Lemma 3 proves one direction: a unique 2-factor forces every pair to be a tree pair. Strengthened conjecture C1+: if `B` has at least two 2-factors, then `#TM > 2^{c_min}`.

**Structure in the non-equality cases** (`C1STRUCT` lines, `V <= 20`).
- Often a minimal 2-factor is a full cube of tree pairs: 250,177 of 287,110 at `V = 20`.
- But in 936 instances at `V = 20` the minimal 2-factors carry no tree pair at all. The `V = 18` C2 witness is one: `c_min = 1`, and all 12 tree matchings sit in the 3-cycle cubes.
- So an injection `{0,1}^{c_min} -> TM` cannot stay inside a minimal cube. The referee's 13-vertex example already rules out partitions into cubes.

**A barrier** (Proposition 4, `PROVED-HERE`). The moment identities of Theorem B, vanishing below degree `m` and nonvanishing at degree `m`, are satisfied by signed point sets of size 6 for `m = 3` and 8 for `m = 4` (Prouhet-Tarry-Escott). So `2^m` cannot follow from them alone. A proof must use the cubes, the exchange moves, or the integrality of `N(w)` for all face choices.

## 6. C3 in detail

**Precise statement.** From every ordered pair, a sequence of D-swaps and Q-reversals, each not increasing `k`, reaches `k = 0`. Since whether a move is allowed depends only on the current pair, this is reachability in a directed graph, tested by BFS (`code/c3.py`).

**Evidence.** 940 random starts with `k >= 1` on random rooted instances: `ins` `V = 60, 100`, `skew` `V = 60, 100, 150`. All succeed. The largest search visited 11,912 pairs (`data/c3_random.txt`). The graph-theory folder's deep trap (`V = 50`, no single decreasing swap under any mate) escapes after visiting 6 pairs, because Q-reversals move along the plateau `k = 1`. Its weak trap escapes after 5. Not tested exhaustively: the graph-theory folder's exhaustive weak-descent check to `V = 15` already implies C3 there.

Status `CONJECTURE`. I have no proof idea that survives the C2 lesson: plateau moves are essential, and the region with `k <= k0` can be large.
