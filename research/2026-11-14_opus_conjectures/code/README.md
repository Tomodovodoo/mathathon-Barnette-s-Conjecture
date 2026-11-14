# Code for the conjecture campaign

Run everything from this folder (`research/2026-11-14_opus_conjectures/code`) in Git Bash. `P` is plantri 4.5 from the reference lab: `P=../../../workings/barnette_lab/vendor/plantri.exe` (see `workings/barnette_lab/README.md` for how it was obtained). `plantri -b V` writes all 3-connected Eulerian triangulations with `V` vertices; `-c4` restricts to 4-connected ones. Compiler: GCC 15.2 (winlibs). Python 3.14 with networkx.

## Files

| File | What it does |
| --- | --- |
| `bar.c` | The engine. For every rooted instance (every face as `t0`, or `-r k` random faces): pair existence by bipartite b-matching, the lattice of 2-factors as integer potentials (PROOFS Lemma 1), exact extremes `E_lo`, `E_hi` by 0-1 BFS, tree-pair search inside a 2-factor (backtracking over D-cycle orientations with a rollback union-find), optional full enumeration of the lattice (`-m full`), lattice structure (`-S`), search outward from the extremes (`-N d`), the R3 chain test (`-C cap`), the direct R2 test over all join- and meet-irreducibles (`-J`), dumps of failures (`-d file`). |
| `gen.py` | Random Eulerian triangulations: `ins` (random degree-4 insertions), `skew` (insertion at a vertex chosen with probability proportional to degree cubed), `mcmc` (insert/delete walk), `glue`, `prism` (face gluings). Output in `bar.c -t` text format. |
| `verify_c2.py` | Independent check built on the reference lab: brute-force states and pairs, 2-factors, all directed simple cycles of each `O_u` and their senses, the two extremes by Felsner's characterisation. Writes JSON. |
| `verify_near.py` | Independent check in pure Python plus networkx, sharing no code with `bar.c`: own faces, max-flow 2-factor, Bellman-Ford extremes, covers by lower-bound relaxation, forest test over all orientations. Modes: distance to the nearest tree-pair element; `chain` (R3). |
| `anatomy.py` | Directed cycles of `O_u`, their exit patterns along the D-cycles, which orientations they kill (PROOFS Cor. 2.1, 2.2), cross-checked against the direct forest test. |
| `c3.py` | C3: BFS over ordered pairs with D-swaps and Q-reversals that do not increase `k`, from random starts with `k > 0`, or from a saved trap (`python c3.py trap file.json cap`). |
| `rot2txt.py`, `cmpu.py`, `checku.py` | Convert the graph-theory folder's JSON files and locate their stored 2-factors in the exact lattice. |
| `run_random.sh`, `run_near.sh` | Batch drivers for the random campaign. |

Build: `gcc -O2 -o bar.exe bar.c` (the runs below used the binaries `bar.exe`, `bar2.exe`, `bar3.exe`, all compiled from successive versions of the same `bar.c`; the final `bar.c` reproduces every output).

## Validation

- `for v in 6 8 9 10 11 12 13 14 15 16; do $P -b $v | ./bar.exe -m full; done`: 5,088 rooted instances with a pair, 24,744 ordered pairs, 24,090 tree matchings, 4,609 cases with `#TM = 2^{c_min}`. These are exactly the totals of the combinatorics folder and its referee.
- Extremes: `E_lo` has only counterclockwise directed facial hexagons, `E_hi` only clockwise (printed as `SENSES`, every run).
- `python verify_c2.py ../data/both_18.txt 0 ../data/c2_counterexample_V18.json` (independent, reference lab).
- `python verify_near.py ../data/r1_counterexample_V24.txt 0 3`, `python verify_near.py ../data/r1_dist2_instances.txt 0 3`, `python verify_near.py ../data/r3_counterexample_V60.txt 0 0 chain` (independent, no shared code).
- The near-search (`-N`) and the full-lattice structure (`-m full -S`) give identical distance histograms at `V = 20` and `V = 22`.

## Commands for the data files

| Output in `../data/` | Command |
| --- | --- |
| `full_le16.txt` | `for v in 6 8 9 10 11 12 13 14 15 16; do $P -b $v \| ./bar.exe -m full \| grep "^R "; done` |
| `ext_fail_V.txt` (V = 17..22; large ones git-ignored) | `$P -b V \| ./bar.exe -d ../data/ext_fail_V.txt` |
| `full_summary_V.txt` (V = 17..22) | `$P -b V \| ./bar.exe -m full -S -d ../data/full_flags_V.txt \| grep -v "^R "` |
| `ext_summary_23_24.txt`, `ext_fail_23/24.txt` (ignored) | `$P -b V \| ./bar2.exe -N 4 -d ../data/ext_fail_V.txt` |
| `both_18.txt` | `grep BOTH ../data/ext_fail_18.txt \| sed 's/^BOTH \([0-9]*\) [0-9]* /\1 /; s/ \| t0//'` |
| `c2_counterexample_V18.json` | `python verify_c2.py ../data/both_18.txt 0 ../data/c2_counterexample_V18.json` |
| `random_A.txt` | `bash run_random.sh ../data/random_A.txt "ins skew mcmc" "30 40 60 80 100" 100 10 1` (stopped during skew V=100: lattices too large) |
| `random_B.txt`, `random_C.txt` | `bash run_near.sh ../data/random_B.txt "ins skew mcmc" "40 60 80 100 150" 60 20 2 5`; `bash run_near.sh ../data/random_C.txt "skew" "150 200 250" 60 20 3 10` |
| `r1_dist2_instances.txt` | the `NEARFAR` lines of the `near_flags_skew_*` dumps, sorted by `V` |
| `r1_counterexample_V24.txt` | the `NEARFAR` line of `ext_fail_24.txt` |
| `r3_exhaustive.txt` | `BOTH` lines of `ext_fail_V.txt` (V = 18..24) piped into `./bar3.exe -T -C 1000000` |
| `r3_random.txt`, `r3_counterexample_V60.txt` | `python gen.py skew 60 100 31 \| ./bar3.exe -t -C 200000 -r 20 -s 31 -d dump`; first `R3FAIL` line |
| `r5_exhaustive.txt` | `$P -b V \| ./bar2.exe -m full \| python ratio.py V=V` (V = 16..22; minimum over `R` lines of `Ltp/L`) |
| `r5_random.txt`, `tp_fraction.txt` | `python gen.py MODEL V COUNT SEED \| ./bar2.exe -t -m full -r 10 -s SEED -cap 300000 \| python ratio.py ...` |
| `r2_random.txt` | `python gen.py MODEL V COUNT SEED \| ./bar3.exe -t -m full -S -r 10 -s SEED -cap 20000` for (skew 60 100 61), (skew 80 60 62), (ins 120 60 63); (skew 100 30 64) timed out at 140 s |
| `r2_tests.txt` | `BOTH` lines of `ext_fail_V.txt` into `./bar4.exe -T -J`; random: `python gen.py skew V 60 SEED \| ./bar4.exe -t -J -r 20 -s SEED` |
| `c3_random.txt` | `python gen.py MODEL V COUNT 21 > _c3.txt; python c3.py _c3.txt 0 COUNT 20 50000 21` for (ins 60 30), (skew 60 30), (ins 100 20), (skew 100 20), (skew 150 10) |

Run times: the exhaustive extremes run takes 20 s at `V = 22`, 77 s at `V = 23`, 317 s at `V = 24` (89 million rooted instances). Full lattice enumeration takes about 60 s at `V = 22`.

## Caveats

- Random models are not uniform. `mcmc` drifts towards triangulations with many separating triangles (few roots have pairs), so it contributed little.
- `gen.py glue` and `prism` produce pairs at few roots and then one-element lattices, so they test nothing for C2.
- R5 failures at `V >= 70` come from `bar.c` alone (full lattice enumeration). The engine is validated, but those particular instances were not re-checked by an independent program.
