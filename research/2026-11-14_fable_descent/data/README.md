# Data for the descent report

All files are `COMPUTED`. Commands are run from `../code` in Git Bash (see `../code/README.md` for the programs, the line formats and the validation). `P` is plantri 4.5, `G` the random generator of the conjectures folder.

| File | Content | Command |
| --- | --- | --- |
| `census_V.txt` (`V = 6, 8..22`) | Exact analysis of every pair of every rooted instance with `V` vertices: totals, histogram of `k`, one summary line per potential, a few witnesses | `$P -ba V \| ./descent.exe > ../data/census_V.txt` |
| `census_tables.md`, `census_summary.json` | The same as tables | `python summarize.py > ../data/census_tables.md` |
| `sinkstats.txt` | Structure of all strict local minima of `k`, `V = 16..21` | loop in `../code/README.md` |
| `sinkstats_random40.txt` | The same for 40 random `skew` triangulations with 40 vertices | `python $G skew 40 40 15 \| ./descent.exe -pots 1 -sinkstats -w 0 \| grep "^H\|^T"` |
| `exhaustive_random_26_30.txt`, `exhaustive_random_40_80.txt`, `exhaustive_random_refined.txt` | Exact analysis of all pairs of random triangulations at every root | see `../code/README.md` |
| `families.txt` | Tubes, bipyramids, chains of glued copies | the block of commands below |
| `traps_graphtheory.txt` | The three saved traps of the graph-theory folder as input lines | `python families.py trap FILE` |
| `walk_random_A.txt` | Sampling on random instances, `V = 40..200` | `bash run_walk.sh ../data/walk_random_A.txt "skew ins" "40 60 80 100 150 200" 40 11 3000 0.5 -signed` |
| `walk_random_B.txt` | Sampling on larger instances with the final `walk.cpp` | `bash run_walk.sh ../data/walk_random_B.txt "skew" "200 300" 8 21 1500 0.5` |
| `witnesses.txt` | One witness line for each refutation quoted in `DESCENT.md` | `grep -m1` on the files above, listed below |
| `witnesses_verified.json` | Independent recomputation of the `k`-witnesses with the reference lab | `python verify_witness.py ../data/witnesses.txt > ../data/witnesses_verified.json` |
| `heights_check.txt` | Lemma B checked with the lab's weights, `V = 12..16` | `for v in 12 13 14 15 16; do python verify_heights.py $v; done` |
| `census_23_partIof8.txt` (`I = 0..7`) | The census at `V = 23` in eight plantri parts, potential `k` only | `$P -ba 23 I/8 \| ./descent.exe -pots 1 -w 1` |
| `gm_lengths_V.json` (`V = 12..17`) | Marked-walk lengths from every non-tree pair, and the distance to the nearest tree pair | `python gm_lengths.py V > ../data/gm_lengths_V.json` |

## Incidents

- `walk_random_A.txt`: the driver was started as a background job with a 15 minute limit. The limit fell during the batch `skew V=200`. That batch has no summary line and its partial witness lines must not be used. The shell loop survived the limit and went on with the `ins` batches while the orphaned `skew V=200` process was still running, so two heavy processes overlapped for about a minute before I killed the orphan. The `ins` batches completed normally. I also overwrote the header of the `ins V=150` batch by mistake and restored it by hand. No number in the report comes from the unfinished batch.
- `verify_heights.py` (Python, about a minute) ran while part 0 of the `V = 23` census was still running in the background.
- The `ins`, `skew` models are not uniform, and `skew` (insertion at a vertex chosen with probability proportional to the cube of its degree) is the harder one for every variant.

## families.txt

    W18 = the "line" field of ../../2026-11-14_opus_conjectures/data/c2_counterexample_V18.json
    S16 = the V = 16 trap in text format with roots "0 1 2" (rotation lists read off the plantri line of the first witness)
    python families.py tube P L | ./descent.exe -pots 0x30098D -cap 2000000 -w 0      for (P, L) = (6,2) (6,3) (6,4) (6,5) (8,2) (8,3) (10,2)
    python families.py bipyramid M | ./descent.exe -pots 1 -w 0                       for M = 3 4 6 8 10 12
    python families.py line "$W18" N | ./descent.exe -pots 0x30098D -w 0               for N = 1 2 3
    python families.py line "$S16" N | ./descent.exe -pots 0x30098D -w 0               for N = 1 2 3 4

## witnesses.txt

Line by line:

1. `W SINK pot=k`, `V = 16`: the least strict local minimum of `k` (`census_16.txt`).
2. `W TRAP2 pot=k+c`, 3. `W TRAP2 pot=(c,wq)`, `V = 16`: trapped even with macro moves of length two (`census_16.txt`).
4. `W SINK pot=(k,+psi,+om)`, `V = 16` (`census_16.txt`). 5. `W SINK pot=(k,+psi,-om)`, `V = 18` (`census_18.txt`).
6. `W TRAP1 pot=(k,+psi)`, `V = 18`. 7. `W TRAP2 pot=wq+wd`, `V = 18` (`census_18.txt`).
8. `W RHO pot=k`, `V = 21`, `extra=3`: the least pair with escape radius 3 (`census_21.txt`).
9. `W RHO`, `V = 60`, `rho=4`. 10. `W RHO`, `V = 40`, `rho=3` (`walk_random_A.txt`).
11, 12. `W SIGNEDRHO`, `V = 60`: plateau-free potentials with radius 3 and 4. `pot=1` is `(k,+psi,-om)`, `pot=4` is `(k,+om,+psi)`, signs in the `gen.py` rotation convention (`walk_random_A.txt`).
13, 14. `W TRAP1`, `W TRAP2`, `pot=(k,-om)`, `V = 40`: the height tie-break is trapped (`python $G skew 40 20 5 | ./descent.exe -pots 0x300000 -cap 300000 -w 1 | grep "^W TRAP"`).
15, 16. `W TRAP1 pot=(k,wq)`, `V = 40`, and `W TRAP2 pot=(k,wq)`, `V = 50` (`exhaustive_random_refined.txt`).

Lines 1, 8, 9, 10 are checked by `verify_witness.py`. The other lines were produced by the engine alone.
