# Code of the rainbow and packing referee

Written for this referee by Opus 5.5, 2026-11-14. No code from other folders is imported. The only external input is plantri 4.5's ASCII output (`workings/barnette_lab/vendor/plantri.exe -b -a V`, Eulerian triangulations; counts 1, 0, 1, 1, 2, 1, 8, 6, 32 for `V = 6..14`, 185 for 16, 1543 for 18). Run from this directory with Python 3.14 and numpy.

| File | What |
| --- | --- |
| `core.py` | rotation system to faces, 2-colouring, rooting, white-face graph `W`, spoke graph test, separating triangles with inner side, 2-factor test (max flow), all 2-factors (backtracking with closure pruning), states |
| `rb.py` | matroid intersection (shortest augmenting paths), rainbow trees by brute force, exchanges via the fundamental cycle, loads, excess, the surplus walk, `ι_t` |
| `check_rainbow.py` | `R`: Theorem R, identity (R) on every connected `J`, Lemma R2. `S`: Lemma X1 by brute force, Theorem S (1)-(3), Proposition U, `ι_t`, evenness, strict descent, Step X (backward closure from good states), M-convexity (exhaustive) |
| `check_packing.py` | `L12`: Lemma 1.2 on every vertex set. `PACK`: Theorems 2.1 and 2.7 by Nash-Williams on `W` and `T/R` plus explicit splits, Prop 2.3, Cor 2.6, Cor 3.2, Thm 3.3 (brute force). `BAD`: covers without a good state |
| `verify_periodic.py` | replays Fable's saved periodic surplus walks |
| `stepx.py` | Step X on chosen `V = 18` triangulations, rainbow trees enumerated per 2-factor (Theorem S), time-capped |

## Commands and outputs (all in `../data/`)

| Command | Output | Time |
| --- | --- | --- |
| `python check_rainbow.py R 6 12` | `R_6_12.json` | 3 s |
| `python check_rainbow.py S 6 12` | `S_6_12.json` | 122 s |
| `python check_packing.py PACK 6 14` | `PACK_6_14.json`, `PACK_6_14.log` | 83 s |
| `python check_packing.py L12 6 14` | `L12_6_14.json` | under 1 min |
| `python check_packing.py BAD 16 16 27` | `BAD_16_16_27.json` | 1 s |
| `python verify_periodic.py <Fable>/data/cycles_hunt_38_400_19_0.0.json <Fable>/data/cycles_hunt_40_200_5_0.0.json <Fable>/data/walk_saved.json` | `periodic.json` (the third file has another layout and gave no examples) | 1 min |
| `python stepx.py 18 1542,1541,103,...,315 420` | `stepx_18_*.json`, `stepx_18.log` | 7 min cap |

Counters in the `PACK` and `S` outputs are cumulative over `V`. "rand" maps are 10 uniformly random deleted-corner maps per rooting (seed 1).

## Validation

- Plantri counts agree with the numbers quoted by the project. Face counts `2V - 4`, edge counts `3V - 6` and proper 2-colouring are asserted on every triangulation.
- Every rainbow tree found by matroid intersection is re-verified as a spanning tree of `H` and as a forest of `W` (two independent tests, which also checks tree-cotree duality).
- The fundamental-cycle exchange is checked against brute force on 651,072 (tree, point) pairs.
- The pruned 2-factor enumeration was re-validated by rerunning `check_rainbow.py S 6 10`, whose assertions compare the rainbow trees found per 2-factor with brute force.
- All counts that Fable also reports for `V <= 12` agree exactly: 262 rootings, 208 with a rainbow tree, 57,901 connected sets, 68 violations, 74,432 rainbow trees, 8,782 trees without a decreasing move, the M-convexity failure at plantri index 2, outer face `{0, 1, 6}`.
