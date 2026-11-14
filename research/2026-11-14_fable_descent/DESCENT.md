# Descent on the exchange graph

Fable 5.2, 2026-11-14. Notation is the shared one. Proofs are in `PROOFS.md`, the complexity statement in `COMPLEXITY.md`, commands in `code/README.md` and `data/README.md`.

**Summary.**
1. C3 in its original form survives everything I could throw at it. From every one of the 49,325,864 ordered pairs of all 4,656,948 rooted instances with `V <= 22`, and from every one of the 9,970,784 pairs of 230 random triangulations with `V = 26` to `80` at every root, a tree pair is reached by exchange moves that never increase `k`, the number of cycles of `Q_s`.
2. Every sharper variant is false. Strict descent in `k` fails at `V = 16` (least), lookahead two at `V = 21` (least), lookahead three at `V = 40`. Every potential that involves the number of cycles of `D` traps a pair at `V = 16`. The plateau-free potentials built from the heights fail at `V = 16` or `18`. Tie-breaking the plateau moves by a height, or by the size of the Q-cycles, fails at `V = 18` or `40`.
3. Two exact facts organise the moves. A D-swap along `C` destroys exactly the Q-cycles that meet `C`. There are three heights `w_r + w_s + w_u = const`, a D-swap moves height between `r` and `s`, a Q-reversal between `r` and `u`, always by the number of white faces inside the cycle.
4. Small traps are uniform. Every strict local minimum of `k` up to `V = 21` has `k = 1`, and in 98.8% of them the Q-cycle lies on a single D-cycle. When two moves suffice there, one way out is to reverse the Q-cycle first, which changes the 2-factor, and then swap. At `V = 40` all three regularities have exceptions.
5. No polynomial bound follows. C3 is equivalent to the absence of a closed plateau, the known cancellation proves that only for the top level, and the lookahead needed grows with `V` (1, 2, 3, 4 at `V = 15, 16, 21, 40`).

## 1. Setting

A pair `(r, s)` has third corners `u`. `k` is the number of cycles of `Q_s` and `c` the number of cycles of `D(r, s)`. The exchange graph `E` joins a pair to the pairs obtained by one D-swap (exchange `r` and `s` along a cycle of `D`) or one Q-reversal (put `r := u` along a cycle of `Q_s`). A Q-reversal keeps `s`, so it keeps `k`, and it changes the 2-factor. A D-swap keeps the 2-factor and changes `s`. Only D-swaps change `k`.

Other quantities used as potentials:

| name in the data | meaning |
| --- | --- |
| `k`, `c` | number of cycles of `Q_s`, of `D` |
| `vq` | number of vertices on cycles of `Q_s` |
| `wq`, `wd` | white faces enclosed, summed over the cycles of `Q_s`, of `D` (each summand is `B + 1` by the disk identity) |
| `om` | the height `w_s = sum_t a(t, s(t))`, the exponent `omega(s)` of the OpenAI paper, up to a global sign |
| `psi` | the height `w_u = sum_t a(t, u(t))` of the third corners, up to a global sign. It is the position of the 2-factor in its lattice |

Tuples are compared lexicographically. By Lemma B, `om` changes under every D-swap and under no Q-reversal, and `psi` changes under every Q-reversal and under no D-swap. The signs `+` and `-` in potential names refer to the plantri rotation convention of the census. Mirror images exchange `(+,+)` with `(-,-)` and `(+,-)` with `(-,+)`, so only "equal signs" and "opposite signs" have an invariant meaning.

## 2. The variants

For a potential `Phi` and a move set I ask three questions, in increasing strength.

- **Weak descent (the C3 type).** From every pair, is a tree pair reachable by moves that never increase `Phi`? A pair from which it is not reachable is *trapped*.
- **Strict descent.** Does every non-tree pair have a move to a strictly smaller `Phi`? A non-tree pair without one is a *strict local minimum*.
- **Escape radius.** The least number of exchange moves from a pair to a pair with strictly smaller `Phi`, with no condition on the pairs in between. Strict descent with a lookahead of `L` moves works iff the radius is at most `L` everywhere.

Move sets: single exchange moves, and macro moves, where a macro move of length at most two is any pair at distance at most two with `Phi` not larger. The variant "reverse a cycle of `D`, then make a forced repair" is a macro move of length two, so it is covered. Where macro moves of length two fail, it fails. The data say the useful compound move has the other order, a Q-reversal followed by a D-swap (Section 4).

The engine `code/descent.cpp` enumerates all 2-factors of a rooted instance, all their orientations, builds `E`, and answers the three questions for 28 potentials by breadth-first search on the digraph of allowed moves. It reproduces the refereed totals exactly (5,088 rooted instances, 24,744 pairs, 24,090 tree pairs for `V <= 16`, and 4,656,948 rooted instances with a pair for `V <= 22`). An independent check of the main witnesses with the reference lab is in `data/witnesses_verified.json`.

## 3. Verdicts

`COMPUTED` throughout. "Census" means all rooted instances with `V <= 22`, all pairs (`data/census_*.txt`, `data/census_tables.md`). "Random exact" means all pairs of random triangulations at every root (`data/exhaustive_random_*.txt`). "Sampled" means random walks on larger instances (`data/walk_*.txt`). A least order is claimed only where the census decides it.

| Variant | Verdict | Smallest trap or range |
| --- | --- | --- |
| `k`, weak descent, single moves (C3) | `CONJECTURE`, no counterexample | holds on the census (49,325,864 pairs), on all 9,970,784 pairs of the random exact instances (`V = 26..80`), and from 27,660 sampled strict local minima on instances with `V = 40..200` |
| `k`, strict descent | `REFUTED` | `V = 16`, least. One rooted instance, 2 pairs |
| `k`, lookahead 2 | `REFUTED` | `V = 21`, least. 6 pairs. None at `V = 22` |
| `k`, lookahead 3 | `REFUTED` | `V = 40` (random exact, 1 pair among 335,704), not known to be least. 17 and 16 pairs in the two `V = 50` batches, 188 at `V = 60`. Sampled at `V = 80, 100, 150, 200` |
| `k`, lookahead 4 | open | radius 5 not seen |
| `vq`, `wq`, `(k, vq)`, `(k, wq)`, weak descent | `REFUTED` | hold on the census. Trapped pairs at `V = 40` (random exact). At `V = 50` also with macro moves of length two |
| `(k, om)` either sign, weak descent (D-swaps on a plateau may only move `w_s` one way) | `REFUTED` | holds on the census. Trapped pairs at `V = 40` (random exact), also with macro moves of length two |
| `(k, psi)` either sign, weak descent (Q-reversals only one way) | `REFUTED` | `V = 18` |
| `(k, psi, om)`, `(k, om, psi)`, all signs, strict descent (plateau-free) | `REFUTED` | `V = 16` for equal signs, `V = 18` for opposite signs |
| the same, lookahead 2 | `REFUTED` | holds on the census. Fails at `V = 40` (random exact) |
| the same, lookahead 3 | `REFUTED` | radius 4 at `V = 60` (sampled) |
| `k + c`, `(c, k)`, `(c, wq)`, `(c, vq)`, `(c, k, wq)`, weak descent | `REFUTED` | `V = 16`, also with macro moves of length two |
| `(k, c)`, `(k, c, wq)`, `(k, c, psi)`, weak descent | `REFUTED` | `V = 16` with single moves. Macro moves of length two rescue them on the census |
| `wq + wd`, `(k, wq + wd)`, weak descent | `REFUTED` | `V = 18` |
| "reverse a D-cycle, then repair", any rule, strict in `k` | `REFUTED` | `V = 21`, as a macro move of length two |

The candidate named in the brief, `(c, then the white faces inside the Q-cycles)`, is `(c, wq)`. It dies at `V = 16` for a reason that has nothing to do with the heights: `c` has to go up before `k` can go down (Proposition E).

Three things in this table surprised me. First, the height tie-breaks looked right on the whole census and then failed on the first random instances with 40 vertices. Second, lookahead two fails at 21 vertices and at no rooted instance with 22. Third, the plateau-free potentials, which would have given a polynomial algorithm outright (Corollary B1), fail as early as plain strict descent does.

## 4. Traps

### 4.1 The smallest one

`V = 16`, plantri graph 27, root `(0, 1, 2)`, first line of `data/witnesses.txt`. The 2-factor is one Hamiltonian cycle (`c = 1`) and `Q_s`, `Q_r` have one cycle each. The only D-swap exchanges `r` and `s`, so it gives `k = 1` again (Corollary A1). The only other move is the Q-reversal, which leads to a 2-factor with three cycles, and from there one D-swap gives a tree pair. So:

- strict descent in `k` fails, and the escape is "Q-reversal, then D-swap";
- anything that charges for `c` is stuck, because the escape goes through `c = 3`;
- it is an instance of the known fact that one 2-factor can carry no tree pair (the instance has three 2-factors, with 1, 3 and 3 cycles, and 18 pairs).

The graph-theory folder calls a strict local minimum a weak trap. It found the first one at `V = 30` by random search, after an exhaustive check to `V = 15`. The exhaustive answer is 16. Its deep trap (no lowering swap under any mate) is a pair with no exit of the form "Q-reversals, then one D-swap". The least one is at `V = 21` (the six pairs of Section 4.2), against `V = 50` found there by sampling.

### 4.2 What strict local minima look like

`COMPUTED`, `data/sinkstats.txt`, all 15,364 strict local minima of `k` with `16 <= V <= 21`.

| k | c | D-cycles that meet the Q-cycle | exits within two moves | pairs |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Q then D | 2,380 |
| 1 | 2 | 1 | Q then D only | 6,033 |
| 1 | 2 | 1 | Q then D, and D then D | 5,959 |
| 1 | 2 | 2 | Q then D (some also D then D) | 163 |
| 1 | 2 | 2 | none | 6 |
| 1 | 3 or 4 | 1 | Q then D (almost all also D then D) | 806 |
| 1 | 3 or 4 | 2 or 3 | Q then D, and D then D | 17 |

- Every one has `k = 1`. Pairs with `k = 2` or `3` exist in this range (64,964 of them at `V <= 21`) and all of them have a D-swap that lowers `k`.
- In 15,178 of 15,364 the Q-cycle `K` has all its vertices on one D-cycle `C`. Swapping `C` destroys `K` (Lemma A) and creates exactly one new cycle.
- Whenever an exit of length two exists, "reverse `K`, then swap a cycle of the new 2-factor" is one. A second D-swap works in about half of the cases.
- These regularities weaken with size. On 40 random triangulations with 40 vertices (`data/sinkstats_random40.txt`, 11,778 strict local minima) 65 have `k = 2`, 15% have a Q-cycle that meets two or three D-cycles, and 143 have only the exit "D then D".
- The six pairs with no exit of length two (all at `V = 21`, plantri graph 47751, root `(0, 1, 2)`, `c = 2`) have a Q-cycle that meets both D-cycles. The radius-4 pairs found by sampling at `V = 60` to `200` also have `k = 1`.

So the picture asked for in the brief is nearly right, with one correction. A small trap is a single Q-cycle sitting on a single D-cycle. What blocks the swap is not nesting but the twin cycle: `f` and `f'` of Lemma A each have a cycle through `V(C)`.

### 4.3 When does a D-swap destroy a Q-cycle without creating one

`PROVED-HERE` (Lemma A). With `sigma` the permutation whose cycles are the D-cycles and `f(x) = u(r^{-1}(x))`:

- the swap along `C` destroys exactly the Q-cycles through vertices of `C`;
- it creates one Q-cycle for each cycle of the function `f'`, equal to `f o sigma^{-1}` on `V(C)` and to `f` elsewhere, that passes through `V(C)`;
- so it lowers `k` iff `f'` has fewer cycles through `V(C)` than `f`.

In the language of the directed-cycle criterion (Lemma 2 of the conjectures folder): a Q-cycle is a directed cycle of the alpha-orientation `O_u` that leaves every centre towards `r`. The swap along `C` kills the ones that visit a centre on `C`, and it turns into Q-cycles exactly the directed cycles that leave towards `s` at their centres on `C`, towards `r` at the others, and visit at least one centre on `C`. A swap is clean when no directed cycle of `O_u` has that mixed exit pattern.

### 4.4 Gluing does not make traps

`PROVED-HERE` (Proposition D). Gluing a rooted instance into a white face of another gives the product of the exchange graphs, with `k` and `c` additive. So C3 holds for the glued instance iff it holds for both parts, and the escape radius is the maximum of the two. The device that refuted R2 at `V = 33` cannot refute C3. `COMPUTED` (`data/families.txt`): chains of 1, 2, 3 copies of the `V = 18` witness of C2 have 20, 400, 8,000 pairs, and chains of 1 to 4 copies of the `V = 16` trap have 18, 324, 5,832, 104,976. No trapped pair, escape radius 2 throughout. The largest distance to a tree pair is twice the number of copies.

### 4.5 Families

`COMPUTED`, exact, every root (`data/families.txt`).

| Family | Sizes | Pairs | Result for `k` |
| --- | --- | --- | --- |
| Tubes of width 6, length `L = 2..5` | `V = 20..38` | 576 to 39,168 | no trapped pair, escape radius at most 2 |
| Tubes of width 8 (`L = 2, 3`) and 10 (`L = 2`) | `V = 26..34` | 4,960 to 53,888 | the same |
| Bipyramids (duals of prisms), `m = 3..12` | `V = 8..26` | 2 per root | every pair is a tree pair |
| Chains of the `V = 18` witness of C2 | `V = 18, 33, 48` | 20, 400, 8,000 | product, as proved |
| Chains of the `V = 16` trap | `V = 16, 29, 42, 55` | 18 to 104,976 | product, as proved |
| The three saved traps of the graph-theory folder | `V = 30, 50, 50` | 18, 122, 102 | no trapped pair, escape radius 2 |

Three families named in the brief are vacuous for descent, each for a provable reason.

- The separator-free family with `c_min = m - 1` has one 2-factor, so all its pairs are tree pairs (Lemma 3 of the conjectures folder).
- Tubes of width four have exactly two pairs, both tree pairs (`sol_counting-families/FAMILIES.md`). Tree matchings are exponentially rare among the states there. That rarity is invisible to the exchange graph, which lives on pairs.
- Prism sums and all gluings into a white face are products (Proposition D).

## 5. Lengths

`COMPUTED`.

| Quantity | Range | Value |
| --- | --- | --- |
| Largest distance in `E` from a pair to a tree pair | census | 0 for `V <= 11`, 1 for `V = 12..15`, 2 for `V = 16..19`, 3 for `V = 20..22` |
| | random exact | up to 5 (`V = 50`, `60`) |
| Largest length of a shortest non-increasing path to a tree pair | census | 3 |
| | random exact | up to 5 (`V = 50`, `60`) |
| | sampled, `V = 150` | 8 |
| Moves used by nearest-improvement descent (go to the nearest pair with smaller `k`, repeat) | sampled, 536,258 starts | mean 1.0 to 7.7 per batch, largest 17 (`V = 300`, start with `k = 13`). Table below |
| Marked walk of the trees paper, from every non-tree pair (reference lab) | all rooted instances, `V = 12..17`, 2,610 starts | at most 7 involution moves, at most 8 exchange moves with the initial normalisation, 293 restarts. The nearest tree pair is at distance at most 2 in the same range |

Nearest-improvement descent on sampled non-tree pairs (`data/walk_random_A.txt`, `data/walk_random_B.txt`; the walk is biased towards large `k`):

| model | V | sampled non-tree pairs | largest `k` | strict local minima | largest escape radius | mean moves | most moves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| skew | 40 | 33,747 | 3 | 1,444 | 3 | 1.15 | 4 |
| skew | 60 | 52,025 | 5 | 2,985 | 4 | 1.43 | 7 |
| skew | 80 | 65,174 | 6 | 4,864 | 4 | 1.68 | 9 |
| skew | 100 | 72,068 | 8 | 3,795 | 4 | 2.15 | 9 |
| skew | 150 | 78,740 | 10 | 2,340 | 4 | 3.38 | 12 |
| skew | 200 | 7,974 | 13 | 99 | 4 | 4.74 | 12 |
| skew | 300 | 8,000 | 15 | 15 | 2 | 7.73 | 17 |
| ins | 40 | 9,689 | 2 | 103 | 2 | 1.01 | 2 |
| ins | 60 | 21,856 | 3 | 762 | 2 | 1.11 | 4 |
| ins | 80 | 33,301 | 3 | 1,910 | 3 | 1.24 | 5 |
| ins | 100 | 38,229 | 3 | 1,920 | 2 | 1.22 | 4 |
| ins | 150 | 52,912 | 3 | 3,714 | 3 | 1.35 | 6 |
| ins | 200 | 62,543 | 7 | 3,823 | 4 | 1.63 | 9 |

The mean grows roughly linearly with `V` in the skew model, from 1.15 at `V = 40` to 7.7 at `V = 300`, because `k` does. In every batch the longest run used at most `2k + 1` moves for its starting `k`. Nothing in the samples suggests more than linear growth. The C3 search from the sampled strict local minima succeeded every time except three starts at `V = 300`, where it hit the cap of 200,000 visited pairs undecided.

**A linear lower bound.** `PROVED-HERE` from Proposition D: in the chain of `m` copies of the `V = 16` trap (`V = 13m + 3`) the pair that is the trap in every copy is at distance `2m` from the nearest tree pair, since distances add in a product. `COMPUTED` for `m <= 4`: 2, 4, 6, 8. So "ten moves always suffice", as observed in the constructive folder on its instances, fails from `m = 6` (`V = 81`) on. I know of no family where the distance to a tree pair grows faster than linearly.

**Comparison with the marked walk.** Up to `V = 17` the marked walk is as short as everything else: 0 moves in 65% of the starts (orienting all D-cycles counterclockwise already gives a tree pair), at most 7 otherwise. Its `2^{O(n log n)}` bound is not visible at these sizes. I did not run it on large instances, because the reference implementation is slow there, so I cannot say where it starts to lose against descent.

Nothing here is an upper bound. No bound on the length of a non-increasing path is known, because plateau moves are free. The refinement that would have bounded it, D-swaps monotone in `w_s`, gives paths of length `O(n^4)` when it applies and is false in general (`V = 40`).

## 6. The proof attempt and where it stops

**What a proof needs.** By Proposition C, C3 says that no set of pairs with a constant `k = j >= 1` is closed under the moves that do not raise `k`. Equivalently every component of the subgraph `E_j` on the pairs with `k <= j` contains a tree pair.

**What the cancellation gives.** Sum `eps(r, s) z^{w_s}` over a component `S` of `E_j`. Grouping by `s` still works: all `2^{k(s)}` mates of `s` have the same `k`, so they lie in `S` together, and they cancel unless `k(s) = 0`. Grouping by `D` does not: `S` meets the orientation cube of a 2-factor in a union of components of the part of the cube where `k <= j`, and the product formula `prod (z^{L+} - z^{L-})` needs the whole cube. For `j` at least the largest `k` it is the whole cube, and that is Theorem 5.2 of the trees paper. Below the top level I found no substitute. On a cube, `k` is a sum of indicator functions of subcubes (one for each dangerous directed cycle, Corollary 2.1 of the conjectures folder), so the sets `{k <= j}` are not subcubes and their signed sums have no reason to have a sign.

**The heights.** Lemma B gives potentials under which every move is strict, with polynomially many values. A proof along the lines of the brief would pick, at a non-tree pair, a reversal that lowers such a potential. The census says no rule of this kind exists for the twelve sign and order choices: each has non-tree strict local minima. The disk identity `W = B + 1` enters only as `W >= 1`, which makes the moves strict. It does not select a direction.

**Why `c` cannot help.** Proposition E. The marked walk of the trees paper makes progress by lowering `c` at restarts. A descent that never raises `c` is impossible. The two methods measure progress in opposite directions, and I see no way to merge them.

**What I would try next.** The traps have `k = 1` and one D-cycle through the Q-cycle. Prove C3 at level `j = 1` first: every component of `E_1` contains a tree pair. For a pair with `k = 1` there are two mates, `(r, s)` and `(r', s)`, on two 2-factors that differ along `K`. The statement to prove is that the D-swaps of these two 2-factors, iterated, cannot all keep exactly one cycle. Lemma A turns this into a statement about the cycles of the functions `f o sigma^{-1}` on blocks.

## 7. Statements with status

| Statement | Status |
| --- | --- |
| Lemma A (function model, a swap destroys exactly the Q-cycles it meets) | `PROVED-HERE` |
| Lemma B (three heights, every move strict in exactly one of `w_s`, `w_u`) | `PROVED-HERE`, well-definedness `COMPUTED` on all census exchange graphs |
| Proposition C (C3 iff no closed plateau iff every component of every `E_j` has a tree pair) | `PROVED-HERE` |
| Proposition D (white-face gluing gives products) | `PROVED-HERE` |
| Proposition E (potentials monotone in `c` are trapped at `V = 16`) | `COMPUTED`, with the parity of `c` from the trees paper |
| Proposition F (bounded escape radius gives a polynomial algorithm) | `PROVED-HERE` |
| C3 | `CONJECTURE`. Test: find a closed plateau. `COMPUTED` none for `V <= 22` |
| Escape radius of `k` is unbounded | `HUNCH`. Observed maxima 1, 2, 3, 4 at `V = 15, 16, 21, 40` |
| Every strict local minimum of `k` has `k = 1` | `COMPUTED` true for `V <= 21`, `REFUTED` at `V = 40` (65 of 11,778 strict local minima of 40 random triangulations have `k = 2`) |
| C3 restricted to D-swaps monotone in `w_s` | `REFUTED`, `V = 40` |
| Strict descent in any of the twelve plateau-free height potentials | `REFUTED`, `V = 16` or `18` |
