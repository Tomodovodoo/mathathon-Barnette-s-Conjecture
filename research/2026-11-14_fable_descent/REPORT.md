# Report: is there a descent that finds the tree pair?

Fable 5.2, 2026-11-14, folder `research/2026-11-14_fable_descent/`.

**Summary.**
1. C3 stands, and only C3. From all 49,325,864 pairs of the census `V <= 22`, and all 9,970,784 pairs of 230 random triangulations with `V = 26..80`, a tree pair is reached by exchange moves that never increase the number `k` of cycles of `Q_s`. I could not prove it.
2. Every variant that would bound the search is false: strict descent in `k` (`V = 16`, least), lookahead two (`V = 21`, least), lookahead three (`V = 40`), any potential that charges for the number of `D`-cycles (`V = 16`), the plateau-free height potentials (`V = 16` or `18`), and plateau moves ordered by a height or by the size of the Q-cycles (`V = 18` or `40`). Twenty-seven of the 28 potentials I tested die. `k` alone survives.
3. Two structural facts, both proved here: a D-swap destroys exactly the Q-cycles that meet its cycle, and there are three heights with constant sum such that every exchange move transfers the number of enclosed white faces from one to another. Gluing into a white face gives products, so the trick that killed R2 cannot touch C3.
4. Complexity: the tree-pair search is in PPADS (find a sink), by merging the phases of the marked walk into one instance. It is not shown to be in PPAD, because the walk has many useless sources, and C3 would not put it in PLS. `COMPLEXITY.md` has the paragraph for the exposition.
5. Lengths: in practice a handful of moves (batch means 1 to 8, most 17, up to `V = 300`). The only proved statement is a lower bound, `2(V - 3)/13` moves on chains of the `V = 16` trap.

## What I set out to do

Settle C3 as far as possible: make every reasonable variant precise, hunt for the smallest counterexample of each, describe the traps, try to prove a surviving variant with a height potential, measure lengths, and state the complexity picture without overclaiming.

## What I established

| Claim | Status | Where |
| --- | --- | --- |
| C3 holds for every pair of every rooted instance with `V <= 22` | `COMPUTED` (`code/descent.cpp`, totals equal to the refereed census) | `DESCENT.md` 3, `data/census_*.txt` |
| C3 holds for every pair of 230 random triangulations, `V = 26..80`, all roots | `COMPUTED` | `data/exhaustive_random_*.txt` |
| C3 from 27,660 sampled strict local minima, `V = 40..200`; three undecided at `V = 300` (cap) | `COMPUTED` | `data/walk_random_*.txt` |
| Strict descent in `k` first fails at `V = 16`; lookahead two first fails at `V = 21` | `COMPUTED` exhaustively, witnesses rechecked with the reference lab | `data/witnesses.txt`, `data/witnesses_verified.json` |
| Lookahead three fails at `V = 40` | `COMPUTED` (random exact; the `V = 60` radius-4 witness rechecked with the lab) | `DESCENT.md` 3 |
| Twenty-seven other potentials: smallest trap for each | `COMPUTED`, `REFUTED` | `DESCENT.md` 3, `data/census_tables.md` |
| Lemma A: function model; a D-swap destroys exactly the Q-cycles it meets | `PROVED-HERE` | `PROOFS.md` |
| Lemma B: three heights `w_r + w_s + w_u = const`, every move strict in exactly one of `w_s`, `w_u` | `PROVED-HERE`; well-definedness `COMPUTED` on every census exchange graph | `PROOFS.md` |
| Proposition C: C3 iff no closed plateau iff every component of every sublevel graph has a tree pair | `PROVED-HERE` | `PROOFS.md` |
| Proposition D: white-face gluing gives products; C3 and the escape radius pass to chains | `PROVED-HERE`, `COMPUTED` on chains | `PROOFS.md`, `data/families.txt` |
| Proposition F: a bounded escape radius would give a polynomial algorithm | `PROVED-HERE` | `PROOFS.md` |
| Proposition G: TREE-PAIR is in PPADS | `PROVED-HERE`, conditional on Theorem 5.3 of the trees paper; unreviewed | `COMPLEXITY.md` 3 |
| Structure of strict local minima for `V <= 21`: all have `k = 1`, 98.8% sit on one D-cycle | `COMPUTED` | `DESCENT.md` 4.2 |
| Distance to a tree pair at least `2m` in the chain of `m` traps (`V = 13m + 3`) | `PROVED-HERE` from Proposition D, `COMPUTED` for `m <= 4` | `DESCENT.md` 5 |
| Marked walk from every non-tree pair, `V = 12..17`: at most 7 moves | `COMPUTED` with the reference lab | `data/gm_lengths_*.json` |

## Predictions and how they fared

I did not keep a separate predictions file. These are the guesses I made before the runs, as I remember them from the session.

- "Two moves always lower `k`" would fail at larger sizes. Right, and sooner than I thought: `V = 21`.
- The plateau-free potentials would work with lookahead two, since they held on the whole census. Wrong: `V = 40`.
- Ordering the plateau by the height `w_s` would survive, for the same reason. Wrong: `V = 40`.
- Gluings of the `V = 18` witness would be the place to look for a counterexample. Wrong for a provable reason (Proposition D).
- C3 would not be proved in the time. Right.

The lesson for the next person: the census to 22 vertices is not a safe guide here. Three variants passed 49 million pairs and failed on the first batch of random instances with 40 vertices.

## What failed and why

- **A proof of C3.** The cancellation proves the sublevel statement only at the top level. Below it the pairs of one 2-factor that are in play form a part of the orientation cube, and the product formula needs the whole cube (`DESCENT.md` 6).
- **A potential from the heights.** Every move is strict in one of two heights with polynomially many values, which is exactly what a polynomial descent needs. But non-tree strict local minima exist for all twelve sign and order choices. The disk identity only says the moves are strict. It does not point anywhere.
- **Charging for `c`.** The smallest trap needs `c` to go from 1 to 3 before `k` can drop. The marked walk measures progress by lowering `c`. The two do not combine.
- **Campaign A.** The background driver outlived its time limit and overlapped with an orphaned process for about a minute. One batch (`skew V = 200`, 40 graphs) is lost. `data/README.md` has the details. I reran `V = 200` and `300` with 8 graphs each.
- **Time.** I did not write out the chaining of several TREE-PAIR instances for the full Hamiltonian cycle problem. That step leans on a citation from memory.

## What is still open

1. C3 itself. The cleanest target is level one: every component of the graph on pairs with `k <= 1` contains a tree pair.
2. Whether the escape radius of `k` is unbounded. Observed maxima 1, 2, 3, 4 at `V = 15, 16, 21, 40`. No radius 5 in 6.3 million pairs at `V = 60`.
3. The least order with escape radius 4 (between 23 and 40), and the least orders of the traps found only on random instances.
4. TREE-PAIR in PPAD, PPA, PLS or P.
5. Any upper bound on the length of a non-increasing path, or on the distance to a tree pair. The examples are linear.

## Three best next steps

1. **Attack level one with Lemma A.** A pair with `k = 1` has two mates on two 2-factors that differ along the Q-cycle. Prove that the D-swaps available on these two 2-factors cannot all keep exactly one cycle of the block functions `f o sigma^{-1}`. The data say the hard cases have the Q-cycle on a single D-cycle. In parallel, push the exact census to `V = 23` and `24` with `descent.exe -pots 1` and plantri's `res/mod` splitting (the engine did `V = 22` with all 28 potentials in nine minutes), looking for a closed plateau.
2. **Referee Proposition G and decide PPAD.** Check the merged instance against the exact definitions in the trees paper, and the two citations I give from memory (Buss and Johnson 2012 on Turing closure, Beame et al. 1998 for PPADS). Then look for an involution on the surplus sources of a level.
3. **Find the family behind the growing radius.** Dump the radius-4 pairs of the `V = 60` exact batch (188 pairs), look at their Q-cycle and the D-cycles through it, and try to build radius 5 by hand. If the radius is bounded on a natural subclass, say bounded vertex degree in `T`, descent is polynomial there by Proposition F.

## Leads for others

- **Topology route, R9.** "Each phase is END-OF-LINE" should read "each phase is a find-a-sink instance". With that change the phases merge and the problem is in PPADS. END-OF-LINE proper is useless here because other sources are free (`COMPLEXITY.md` 3).
- **Constructive folder.** "A tree matching within ten moves on every tested instance" is an observation about those instances. The chain of six `V = 16` traps (`V = 81`) needs twelve.
- **Graph-theory folder.** Its weak traps start at `V = 16` (not 30) and its deep traps at `V = 21` (not 50), both least by exhaustion. The witnesses are lines 1 and 8 of `data/witnesses.txt`. Its conjecture D3 with two steps fails at `V = 21`.
- **Digestion 09, door 4.** The requested search for a closed plateau has now been done exactly to `V = 22` and on random instances to `V = 80`. The entry can say so, and can add that no tie-break rule survives.
- **Exposition.** Two statements are short and I think worth a figure. The three heights: a D-swap moves `W` units of height between `r` and `s`, a Q-reversal between `r` and `u`, where `W = B + 1` is the number of white faces inside the cycle. And the `V = 16` picture: one Hamiltonian D-cycle, `Q_s` and `Q_r` each with a cycle, so the proof has to change the 2-factor.
- **Anyone with a census need.** `code/descent.exe` builds every exchange graph for `V <= 22` in about twelve minutes and checks the component theorem on the way.

## Files

- `DESCENT.md`: variants, verdicts, traps, lengths, the proof attempt, status table.
- `PROOFS.md`: Lemmas A and B, Propositions C to F.
- `COMPLEXITY.md`: the paragraph for the exposition, the problems, Proposition G, PLS.
- `code/README.md`, `data/README.md`: programs, exact commands, incidents, witness list.
