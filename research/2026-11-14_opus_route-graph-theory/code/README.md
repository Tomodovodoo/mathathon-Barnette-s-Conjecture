# Code for the graph-theory routes

Python 3.14 with networkx 3.6, numpy, scipy. Run everything from this folder. Outputs go to `data/`. For reproducible random runs, set `PYTHONHASHSEED=0`; the data files below were produced that way, except where noted.

## Core modules

| File | Content |
| --- | --- |
| `tri.py` | Rotation systems, faces, face 2-colouring, planar canonical code, exhaustive generator of Eulerian triangulations (degree-4 insertions plus face gluings, PROOFS Lemma 6.1), `load(V)` for the census. |
| `flipcheck.py` | Independent check of the generator: enumerates all triangulations by edge flips and filters Eulerian ones. |
| `states.py` | `Rooted(T, t0)`: black/white faces, `A`, `X`, states, `Q_s`, tree-matching test, mates, flow test for pairs, black-inner separating triangles. |
| `pairs.py` | Pairs without enumeration: flow pair, Q-map `f`, `D`-cycles, D-swaps, Q-reversals, random Eulerian triangulations. |
| `lattice.py` | Difference cycles of two states and their orientation via the delta-sum (disk identity). |
| `alpha.py` | Deleted-corner maps `u`, face flips in the alpha-orientation lattice, the ordered pairs inside a 2-factor. |
| `induced.py` | OpenAI's construction `s -> P -> partition`, all induced-tree partitions, the inverse map `derive`. |

## Experiments (command, output)

| Script | Question | Command | Output |
| --- | --- | --- | --- |
| `gen_census.py` | census `V <= 16` | `python gen_census.py 16` | `data/eul_*.json`, `data/gen_census.log` |
| `exp_census.py` | BT Thm 1.2, unique mate | `python exp_census.py 14` | `data/census_14.txt` |
| `exp_obstruction.py` | flow vs black-inner criterion | `python exp_obstruction.py 16` | `data/obstruction_16.txt` |
| `exp_matroid.py` | M1, M2 | `python exp_matroid.py 12` | `data/matroid_12.txt` |
| `exp_hole.py` | M5 | `python exp_hole.py 13` | `data/hole_13.txt` |
| `exp_lp.py` | M3 (LP integrality) | `python exp_lp.py 13 10` | `data/lp_13.txt` |
| `exp_lattice.py` | O1 | `python exp_lattice.py 13` | `data/lattice_13.txt` |
| `exp_mate.py` | O2, mate cycle orientations | `python exp_mate.py 12` | `data/mate_12.txt` |
| `exp_alpha.py` | alpha-lattice extremes, exhaustive | `python exp_alpha.py 12` | console (all instances pass) |
| `exp_alpha2.py` | validate face-flip min; random O4–O6 | `python exp_alpha2.py validate 12`; `python exp_alpha2.py random V 60 seed` | `data/alpha_max_test.txt` (run without the both-fail counter), `data/alpha_max_V80.txt`, `data/alpha_V120_both.txt`, `data/alpha_*_fail_*.json` |
| `exp_every_factor.py` | O3 exhaustive | `python exp_every_factor.py 13` | console: 0 failures `V <= 13` |
| `exp_ef_lattice.py` | O3 random | `python exp_ef_lattice.py 40 20 40` | `data/ef_fail_40_40.json` |
| `exp_descent.py` | D2 exhaustive | `python exp_descent.py 15` | `data/descent_15.txt` |
| `exp_moves.py` | D1 exhaustive | `python exp_moves.py 15 13` | `data/moves_13_15.txt` |
| `exp_random_descent.py` | D1 random | `python exp_random_descent.py 50 30 200 50` | `data/strong_V50.txt`, `data/strongviol_50_seed50.json`, `data/strong_V30.txt` |
| `exp_traps.py` | D2 random | `python exp_traps.py 50 30 150 104` (deep trap), `python exp_traps.py 30 30 150 37` (weak trap) | `data/deeptrap_50_1.json`, `data/weaktrap_30_seed37.json`, `data/deep_search2.txt` |
| `exp_traps2.py` | D2 smaller V | `python exp_traps2.py 20,24,28,32,36,40 60 150 11` | `data/traps2.txt` (run without fixed hash seed) |
| `exp_induction.py` | I1 | `python exp_induction.py 13` | `data/induction_13.txt` |
| `exp_lift.py` | PROOFS Lemma 6.2 check | `python exp_lift.py 13` | `data/lift_13.txt` |
| `exp_induced.py` | P1 | `python exp_induced.py 12` | `data/induced_12.txt` |
| `exp_induced2.py` | P1, both roots at `e0` | `python exp_induced2.py 12` | `data/induced2_12.txt` |

## Verifiers for saved counterexamples

They rebuild the triangulation from the stored rotation system, re-check that it is Eulerian, simple and free of black-inner separating triangles, and recompute everything from scratch.

- `python verify_trap.py data/deeptrap_50_1.json` reports `V = 50`, no separating triangles, `k = 1`, every swap under both mates keeps `k = 1`, and two swaps reach `k = 0`.
- `python verify_trap.py data/strongviol_50_seed50.json` and `python verify_trap.py data/weaktrap_30_seed37.json` work the same way.
- `python verify_ef.py data/ef_fail_40_40.json` reports a one-cycle 2-factor with no tree pair, equal to the face-flip minimum. The maximum has 4 tree pairs out of 8.
- `python verify_ef.py data/alpha_max_fail_80_83.json` reports a one-cycle 2-factor with no tree pair, equal to the face-flip maximum. The minimum has 2 out of 8.

## Caveats

- Random triangulations come from random degree-4 insertions on the octahedron. This distribution is not uniform.
- The "face-flip minimum" equals Felsner's lattice minimum when facial flips generate the lattice. That is checked for `V <= 12`, not beyond.
- `exp_lp.py` finds fractional vertices with random objectives. "None found" for `V <= 12` is not a proof of integrality there.
- The python files `exp_*.py` import each other in a few places. Each has a `__main__` guard.
