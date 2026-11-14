# Code for the topology referee and the rainbow attack

Python 3.14, standard library only. Run every command from the repository root. Each script writes one JSON file into `../data/` and stores its own command line in the field `command`.

The code is independent of `research/2026-11-14_opus_route-topology/code/topo.py` and of `workings/barnette_lab`. It uses the plantri binary `workings/barnette_lab/vendor/plantri.exe` (build it with `python workings/barnette_lab/setup_plantri.py`) and reads the rotation system from plantri's ASCII output. One command, `exp_structure.py replicate`, imports `barnette_lab` for a single purpose: to learn which face that library numbers as `outer`, so that the refereed report's instance sets can be rebuilt exactly.

## Modules

| File | Content |
| --- | --- |
| `etri.py` | Rotation systems, faces, 2-colouring, rooted instances, `delta`, disks of cycles, states, `Q_s`, mates by orientation, tree-matching test, flow test for a pair, black-inner separating triangles, random Eulerian triangulations (degree-4 insertions, octahedron gluing), loader for the graph-theory run's saved instances. |
| `rainbow.py` | White-face graph, matroid intersection (cycle matroid with a partition matroid), enumeration of all rainbow trees, the unique exchange, load and excess, plateau search, random and adversarial starts. |

## Referee checks (Part 1)

`P = research/2026-11-14_fable_referee-topology/code`

| Command | Range | Checks | Time | Output |
| --- | --- | --- | --- | --- |
| `python P/referee.py angles 12` | 262 rootings, 80 states each, seed fixed | corner sums, local turning identity, Gauss-Bonnet, `W = B + 1`, general formula 2.5 | 1 s | `ref_angles.json` |
| `python P/referee.py retract 14` | 55 triangulations, 60 random perfect matchings each | `b0(P) = c + 1`, `b1(P) = c - 1`, inducedness | 1 s | `ref_retract.json` |
| `python P/referee.py morse 14` | 1,206 rootings, all states | `2^k` mates, `J` formula with both signs, binomial levels, `Z(1) = 0` | 1 s | `ref_morse.json` |
| `python P/referee.py mate 14` | 1,206 rootings, all tree matchings | mate of a tree matching | 1 s | `ref_mate.json` |
| `python P/referee.py height 12` | 262 rootings, all states, 40 sampled pairs each | clock-move digraph, height against signed white area, additivity | 1 s | `ref_height.json` |
| `python P/exp_structure.py replicate` | the report's 826 and 166 instances | its exact counts | 3 s | `replicate.json` |

## Step R

| Command | Range | Output |
| --- | --- | --- |
| `python P/exp_rainbow.py rado 12` | all connected `J` in 262 rootings: Rado condition, exact formula (R) | `rado_12.json` |
| `python P/exp_rainbow.py exist 16` | 7,868 rootings: rainbow tree, pair, triangle criterion, face-rainbow tree (5 s) | `exist_16.json` |

## Step X and the surplus walk

| Command | Range | Time | Output |
| --- | --- | --- | --- |
| `python P/exp_rainbow.py traps 6 12 all` | every rainbow tree, all rootings | 1 s | `traps_6_12_all.json` |
| `python P/exp_rainbow.py traps 13 14 all` | same | 17 s | `traps_13_14_all.json` |
| `python P/exp_rainbow.py traps 15 15 all` | same | 59 s | `traps_15_15_all.json` |
| `python P/exp_rainbow.py traps 16 16 all` | same, 29.4 million trees | 467 s | `traps_16_16_all.json` |
| `python P/exp_walk.py exhaust 6 12 all`, `exhaust 13 14 all`, `exhaust 15 15 all`, `exhaust 16 16 two` | every walk state: paths, cycles, involutions | 1, 18, 63, 40 s | `walk_exhaust_*.json` |
| `python P/exp_walk.py sample 18 4 1`, `sample 20 40 1`, `sample 22 400 1` | every 4th, 40th, 400th plantri triangulation, 2 random roots, 3 starts | 3 to 7 s | `walk_sample_*.json` |
| `python P/exp_walk.py random 40 60 1`, `random 60 30 2`, `random 80 20 3`, `random 120 8 4`, `random 45 30 5 0.15` | random triangulations, last one with glued octahedra | 1 to 3 s | `walk_random_*.json` |
| `python P/exp_walk.py saved` | 11 saved instances of the graph-theory run, `V = 40` to `120` | 5 s | `walk_saved.json` |
| `python P/exp_cycles.py analyse` | re-examines every failure recorded by `exp_walk.py`: exact periods, plateau search | 1 s | `cycles_analyse.json` |
| `python P/exp_cycles.py hunt 24 400 1`, `hunt 28 400 2`, `hunt 32 300 3`, `hunt 36 300 4`, `hunt 40 200 5`, `hunt 50 100 6`, `hunt 44 100 7 0.1` | random instances, every walker classified exactly | 6 to 22 s | `cycles_hunt_*.json` |
| `python P/exp_structure.py identity 12` | Lemma X2 on a sample of at most 60 trees per instance, every move | 3 s | `identity_12.json` |
| `python P/exp_structure.py loads 12` | load vectors: exchange towards all-ones (all instances), M-convexity when `|L| <= 400` | 15 s | `loads_12.json` |
| `python P/exp_structure.py potential 12` | four candidate secondary potentials | 6 s | `potential_12.json` |
| `python P/exp_average.py 6 14` | number of rainbow trees, slot identity, mean load | 30 s | `average_6_14.json` |

Earlier runs of `exp_rainbow.py exist`, `exp_structure.py identity 10`, `loads 10` and `potential 10` left `identity_10.json`, `loads_10.json` and `potential_10.json`. They are superseded by the `_12` files.

`exp_rainbow.py sample`, `random` and `saved` are the plateau-search versions of the walk experiments. They were written first and were not used for the reported numbers.

## Exploratory scripts

`scratch_chir.py`, `scratch_revisit.py`, `scratch_levels.py`, `scratch_alt.py` are one-off probes. They print to the console and write no data. What they showed: the orientation of (arrival, resident, pivot) is not constant along a surplus walk; a surplus walk can visit a face twice (13 of 86,060 walks with `V <= 13`); the level counts of rainbow trees; and the slot identity, later rerun properly as `exp_average.py`.

## Limits

- Random triangulations come from degree-4 insertions on the octahedron. They are not uniform and have no separating triangles unless octahedra are glued in.
- Adversarial starts are random walks followed by moves that never lower the excess. This is a heuristic, not a search for the worst start.
- `exp_walk.py` detects a periodic walk only when the start state recurs after a multiple of 64 steps or after 200,000 steps. `exp_cycles.py` compares the full state at every step and is exact. Every failure of the first was re-examined by the second.
- Nothing here has been checked by a second implementation, except where this folder is itself the second implementation of the refereed report. The new computed claims in `RAINBOW.md` are T4, unreviewed.
