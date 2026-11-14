# Code for the descent report

Run everything from this folder (`research/2026-11-14_fable_descent/code`) in Git Bash. Compiler: GCC 15.2 (winlibs). Python 3.14 with networkx. `P=../../../workings/barnette_lab/vendor/plantri.exe` is plantri 4.5 (see `workings/barnette_lab/README.md`). `G=../../2026-11-14_opus_conjectures/code/gen.py` is the random generator of the conjectures folder, used read-only.

## Files

| File | What it does |
| --- | --- |
| `descent.cpp` | Exact engine. For every rooted instance (every face as root, or the roots given on the line) it enumerates all 2-factors and all ordered pairs, builds the exchange graph, checks that the two heights `psi`, `om` are path independent and that every component has a tree pair, and for each of 28 potentials reports trapped pairs (single moves and macro moves of length at most two), strict local minima, escape radius, longest shortest non-increasing path and longest strictly decreasing path. `-pots MASK` selects potentials by bit, `-cap N` skips rooted instances with more than `N` pairs, `-w N` prints `N` witnesses per kind, `-g I` only graph `I`, `-sinkstats` prints the structure of the strict local minima of `k`. |
| `walk.cpp` | Sampling version for large instances (includes `descent.cpp`). Max-flow 2-factor, biased random walk on pairs, and at sampled non-tree pairs: strict local minimum or not, escape radius of `k`, the C3 search (breadth-first over non-increasing moves), the same with D-swaps monotone in `om` (`-signed`), the radii of the eight plateau-free potentials (`-signed`), and the length of nearest-improvement descent. |
| `families.py` | Tubes, bipyramids, the saved traps of the graph-theory folder, chains of glued copies of an instance. Output in the text format read by both programs. |
| `run_walk.sh` | Batch driver for `walk.exe` on random instances. |
| `summarize.py` | Census outputs to `data/census_summary.json` and `data/census_tables.md`. |
| `verify_witness.py` | Independent check of the `k`-witnesses with the reference lab (no shared code with the engine). |
| `gm_lengths.py` | Lengths of the marked walk of the trees paper from every pair, using the reference lab. |

Build: `g++ -O2 -o descent.exe descent.cpp` and `g++ -O2 -o walk.exe walk.cpp`. The binaries are not committed.

Input formats, one triangulation per line: plantri ascii (`plantri -ba V`), or `V d n1..nd d n1..nd ... [r0 r1 r2]` (rotation lists, optional roots). Rotation lists are clockwise in plantri output and counterclockwise in `gen.py` output. Only the signs in the names of the signed potentials depend on this.

Output lines of `descent.exe`: `T` totals, `K` histogram of `k`, `S` one line per potential, `W` witnesses, `H` sink structure. In an `S` line `trap1` counts pairs with no non-increasing path to a tree pair, `trap2` the same with macro moves of length at most two, `sinks` the non-tree pairs without a strictly smaller neighbour, `maxrho` the largest escape radius (99 means the component has no smaller value), `maxmono` the longest shortest non-increasing path, `maxstrictlen` the longest strictly decreasing path. A `W` line has the form `W KIND pot=.. V=.. graph=.. t0=a,b,c k=.. c=.. extra=.. | graph line | faces .. | pair r>s r>s ...`, where the pair lists `r(t)>s(t)` for the faces of `A` in the order of the `faces` field (in `walk.exe` output the `faces` field is omitted, and the face of an entry is the black face that contains both vertices).

## Validation

- `for v in 6 8 9 10 11 12 13 14 15 16; do $P -ba $v | ./descent.exe | grep "^T"; done` gives 5,088 rooted instances with a pair, 24,744 pairs and 24,090 tree pairs in total, the refereed numbers. The counts of rooted instances with a pair at `V = 17..22` (8,042; 27,972; 82,819; 287,110; 944,804; 3,301,113) agree with `research/2026-11-14_opus_conjectures` and sum with the smaller orders to the referee's 4,656,948.
- The engine exits with an error if a component of an exchange graph has no tree pair, if a move leads outside the enumerated set of pairs, or if a height is path dependent. None of these happened in any run.
- `python verify_witness.py ../data/witnesses.txt > ../data/witnesses_verified.json` recomputes the `k`-witnesses with the reference lab.

## Commands for the data files

| Output in `../data/` | Command |
| --- | --- |
| `census_V.txt`, `V = 6..22` | `$P -ba V \| ./descent.exe > ../data/census_V.txt` (38 s for `V = 17..20` together, 2.5 min at `V = 21`, 9 min at `V = 22`) |
| `census_tables.md`, `census_summary.json` | `python summarize.py > ../data/census_tables.md` |
| `sinkstats.txt` | `for v in 16 17 18 19 20 21; do $P -ba $v \| ./descent.exe -pots 1 -sinkstats -w 0 \| grep "^H" >> ../data/sinkstats.txt; done` |
| `traps_graphtheory.txt` | `python families.py trap D/deeptrap_50_1.json; python families.py trap D/weaktrap_30_seed37.json; python families.py trap D/strongviol_50_seed50.json` with `D=../../2026-11-14_opus_route-graph-theory/code/data` (those three files are not in git; they were present in the working tree) |
| `exhaustive_random_26_30.txt` | for `(ins 26 30 3)`, `(skew 26 30 3)`, `(ins 30 20 4)`, `(skew 30 20 4)`: `python $G MODEL V COUNT SEED \| ./descent.exe -pots 0x300801 -cap 400000 -w 1` |
| `exhaustive_random_40_80.txt` | for `(skew 40 20 5)`, `(ins 40 20 5)`, `(skew 50 12 6)`, `(ins 60 12 6)`, `(ins 80 8 7)`: `python $G MODEL V COUNT SEED \| ./descent.exe -pots 0x300801 -cap 300000 -w 1` |
| `exhaustive_random_refined.txt` | for `(skew 40 40 15)`, `(skew 50 12 6)`, `(skew 50 12 16)`, `(skew 60 6 8)`: `python $G MODEL V COUNT SEED \| timeout 240 ./descent.exe -pots 0x18D -cap 600000 -w 1` |
| `walk_random_A.txt` | `bash run_walk.sh ../data/walk_random_A.txt "skew ins" "40 60 80 100 150 200" 40 11 3000 0.5 -signed`, with the first version of `walk.cpp` (no `C3OM` line). The `skew 200` batch did not finish, see `data/README.md` |
| `walk_random_B.txt` | see `data/README.md` |
| `families.txt` | see `data/README.md` |
| `witnesses.txt` | selected `W` lines of the files above (`grep -m1` commands in `data/README.md`) |
| `witnesses_verified.json` | `python verify_witness.py ../data/witnesses.txt > ../data/witnesses_verified.json` |
| `gm_lengths_V.json` | `python gm_lengths.py V > ../data/gm_lengths_V.json` |
