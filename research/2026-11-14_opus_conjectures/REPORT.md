# Report: the three open conjectures on pairs and tree matchings

Opus 5.5, 2026-11-14, folder `research/2026-11-14_opus_conjectures/`.

**Summary.**
1. C2 (O6, "an extreme of Felsner's lattice of pairs carries a tree pair") is false. The smallest counterexample has 18 vertices and is 4-connected. It was found by an exhaustive search over every rooted instance up to `V = 24` (89 million at `V = 24` alone) and checked with the reference lab (`data/c2_counterexample_V18.json`).
2. Three weaker replacements fail: within cover-distance 1 of an extreme (first failure at `V = 24`), every maximal chain (at `V = 60`), at least half of the lattice (at `V = 70`). One survives every test to `V = 250`: some extreme or irreducible element carries a tree pair (R2), a polynomial-size candidate list. The earlier evidence for C2 came from greedy local extremes, which are usually not the lattice extremes.
3. C1 (`#TM >= 2^{c_min}`) holds for all 4,656,948 rooted instances with a pair up to `V = 22`. Equality holds exactly when `B` has one 2-factor. I prove that direction. I also prove that Theorem B's moment identities alone cannot give `2^{c_min}`.
4. New tools, all proved: the lattice as a system of difference constraints with exact extremes by shortest paths, and a tree-pair criterion: `(r, s)` is a tree pair iff no directed cycle of the alpha-orientation exits every centre towards `r`. A directed facial hexagon means a white triangle in `Q_s`. That is exactly how the extremes fail.
5. C3 (monotone descent) survived 940 random starts up to `V = 150`. It is unproved.

## What I set out to do

Make C1, C2, C3 precise, test them far beyond 16 vertices, hunt counterexamples, find the weakest true replacement for whatever falls, and prove what survives, in the order C2, C1, C3.

## What I established

| Claim | Status | Where |
| --- | --- | --- |
| Alpha-orientations = integer potentials with one difference constraint per spoke; extremes by two shortest-path computations; `E_lo` has no clockwise and `E_hi` no counterclockwise directed cycle | `PROVED-HERE` | PROOFS Lemma 1 |
| The graph-theory folder's "face-flip extremes" are greedy local extremes; 7 of its 9 saved witnesses are not lattice extremes | `COMPUTED` | PROOFS Remark 1.1, `code/checku.py` |
| `(r, s)` tree pair iff no directed cycle of `O_u` leaves every centre towards `r`; inside a 2-factor, tree-pair existence is a covering problem by subcubes; a directed facial hexagon around `y` kills exactly the orientations with `y` in `Q_s` | `PROVED-HERE`, cross-checked by computer | PROOFS Lemma 2, Cor. 2.1, 2.2 |
| C2, O4, O5 for the true lattice extremes | `REFUTED`, smallest `V = 18` | CONJECTURES §3 |
| Exhaustive C2 census `V <= 24` (both-fail counts 26, 66, 46, 833, 935, 9,731 at `V = 18, 20, 21, 22, 23, 24`; none at odd `V <= 19`) | `COMPUTED` | `data/ext_summary_23_24.txt`, CONJECTURES §3 |
| R1 (distance `<= 1`), R3 (every chain), R5 (half the lattice) | `REFUTED` at `V = 24`, `60`, `70` | CONJECTURES §4 |
| R2: an extreme, join- or meet-irreducible element carries a tree pair | `CONJECTURE`; `COMPUTED` exhaustively for `V <= 24`, random to `V = 250` | CONJECTURES �4, `data/r2_tests.txt` |
| C1 for `V <= 22` exhaustively, random to `V = 100` | `COMPUTED` | `data/full_summary_*.txt` |
| A unique 2-factor makes every pair a tree pair, so `#TM = 2^{c_min}` | `PROVED-HERE` | PROOFS Lemma 3 |
| Equality in C1 only for a unique 2-factor | `CONJECTURE`, `COMPUTED` to `V = 22` | CONJECTURES §5 |
| Moment identities alone allow `2m < 2^m` points (`m = 3, 4`) | `PROVED-HERE` | PROOFS Prop. 4 |
| C3 on random starts | `COMPUTED` (940 starts, `V <= 150`) | CONJECTURES §6 |

Engine validation: `code/bar.c` reproduces the refereed totals up to 16 vertices exactly (5,088 rooted with pair, 24,744 pairs, 24,090 tree matchings, 4,609 equality cases). Two independent programs check every counterexample I report as `REFUTED`, except R5. `verify_c2.py` uses the reference lab and brute-force cycle enumeration. `verify_near.py` is pure Python and shares no code with the engine. The R5 failure is from the engine alone (flagged in CONJECTURES).

## What failed and why

- **C2 and its proof route.** The brief hoped that at the lattice minimum every directed cycle has one sense and that this forces a forest for some orientation. The first half is true (Lemma 1). The second half is false. A directed cycle is harmful only if its exits are uniform along the D-cycles it meets, and the sense of the cycle does not control the exits. At `V = 18`, each extreme is one Hamiltonian D-cycle with two directed counterclockwise hexagons exiting in opposite directions. One orientation of the D-cycle puts the first white triangle into `Q_s`, the other puts in the second. Flipping exactly those hexagons gives the middle elements, which carry the tree pairs.
- **Every order-theoretic replacement I could state.** Tree-pair elements are not near the extremes, not on every chain, and not a majority. The distance grows slowly with `V` (2 at `V = 24` and at `V = 150..250`), so "bounded distance" might survive in some weaker form. I would not bet on it.
- **An injection for C1 through minimal cubes.** In 936 rooted instances at `V = 20` the minimal 2-factors carry no tree pair at all.
- **Proving C1 from Theorem B.** Impossible in principle (Prop. 4).

Process note: once, for a few minutes, I ran two heavy processes at the same time (the V = 23/24 census and an R3 test). The brief allows one. No result depends on the overlap.

## What is still open

1. **C1 and C1+** (`#TM > 2^{c_min}` whenever there are at least two 2-factors). The equality characterisation is new and suggests induction on the lattice. A move from a one-element lattice to a larger one adds tree matchings faster than it lowers `c_min`.
2. **C3.** Untested exhaustively beyond the graph-theory folder's `V <= 15`, unproved.
3. **R2** (extremes or irreducibles). Every test passes, and the candidate list is polynomial. Open: a proof, and whether testing one 2-factor for a tree pair (subcube covering, Cor. 2.1) is polynomial.
4. **A canonical tree pair.** No canonical element of Felsner's lattice works. The structure that decides success couples the 2-factor with the orientation of its cycles (Lemma 2), and the lattice order ignores the orientation.

## Three best next steps

1. **Use Lemma 2 as the local picture of the whole proof.** A tree pair is an orientation of the D-cycles that cuts every directed cycle of the alpha-orientation. Facial cycles cut means no white triangle in `Q_s`. Rewrite the cancellation (Lemma 5.2 of OpenAI, Theorem B) in this language: the signed sum over orientations is an inclusion-exclusion over the subcubes of dangerous cycles. That could give the exposition one picture for both cancellations, and it might suggest a weight that counts uncovered orientations directly.
2. **Attack C1+ by induction over the lattice.** Start with two-element lattices, where the two 2-factors differ by reversing one essential cycle. Use the exhaustive data (`code/bar.c -m full`, `V <= 22`) to find what the extra tree matchings are. Lemma 3 handles the base case.
3. **Attack R2.** The join-irreducible `J(a, k)` is the least 2-factor in which face `a` has been "flipped `k` times". Ask which faces `a` give a tree pair at `J(a, k)` in the data (`bar.c -J` stops at the first success; log all of them instead). Look for a rule that picks `a` from the dangerous hexagons of `E_lo` (Cor. 2.2). In the `V = 18` witness the right faces are exactly the two blocking white triangles.

## Leads for others

- **Exposition and figures.** The `V = 18` witness (`data/c2_counterexample_V18.json`) is a clean picture of why choosing a single 2-factor fails: a four-element lattice, both extremes Hamiltonian, two white triangles that block the two orientations. It would make a good figure for "the cancellation has to move between 2-factors".
- **Graph-theory folder.** Its O4/O5/O6 numbers and the claim "the minimum fails at V = 40" concern greedy face-flip results, not lattice extremes (PROOFS Remark 1.1). With the true extremes, the `alpha_min_fail_40_41.json` instance has tree pairs at both extremes. O4 still fails at `V = 40` via `ef_fail_40_40.json`, whose stored 2-factor is the true `E_lo`.
- **Algorithms.** Lemma 1 gives both extremes with two shortest-path runs, and the near-search in `bar.c` explores the lattice by exact cover moves. Anyone implementing "flip to the extreme" should use potentials, not single-face flips.
- **Census.** `bar.c` processes all 89 million rooted Eulerian triangulations with 24 vertices in about five minutes and checks pair existence, extremes and tree pairs. It can serve as a fast cross-check for other agents' claims at `V <= 24`.

## Files

- `CONJECTURES.md`: definitions, the reconciliation of conventions, status, evidence ranges, counterexamples.
- `PROOFS.md`: Lemma 1, Lemma 2 with two corollaries, Lemma 3, Proposition 4, each with its adversarial reading.
- `PREDICTIONS.md`: predictions made before the tests, and their outcomes.
- `code/README.md`: exact commands for every data file. `data/`: summaries and counterexamples. Bulky regenerable dumps are git-ignored.
