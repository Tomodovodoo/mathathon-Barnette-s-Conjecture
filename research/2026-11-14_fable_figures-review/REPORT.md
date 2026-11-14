The figure sequence is rebuilt on a new 13-vertex running example in a disk layout: 15 figures, gallery of 10 pages, all from checked data.
COMPUTED: one pair of states of that example shows cancellation, a disk with B=5, W=6, I=3, h=7, l=2, and the recovery of the Hamiltonian cycle.
COMPUTED: it is the only 4-connected Eulerian triangulation with at most 13 vertices that has both a cyclic Q_s and a D-cycle enclosing a vertex.
All eight listed problems are addressed; four missing figures were added (cube, local triangle, incidence graph with flow, leading coefficient).
Weak points: the white-tree curves wander, the smallest corner is 20 degrees, and I made no greyscale proofs.

# Report

## What I set out to do

Review the 14 figures in `paper/figures/`, fix the eight problems the coordinator listed, find more, and leave a toolkit that rebuilds from the README. `REVIEW.md` has the figure-by-figure account and `before-after/` has the renders.

## What I established

COMPUTED (`search_example.py`; `plantri -bc4` for 8 to 14 vertices; every face as `t0`). Rooted 4-connected Eulerian triangulations with a pair whose `Q_s` has a cycle: none up to 11 vertices, 2 of 100 at 12 vertices, 4 of 66 at 13. Exactly one triangulation with at most 13 vertices also has a `D`-cycle enclosing a vertex. It has maximum degree 6. At 14 vertices the only one is the first-pass example with a degree-8 vertex.

COMPUTED (`paper/figures/check.py`, the 13-vertex example with `t0 = {0,4,5}`, all states and pairs):

- 12 states, 8 ordered pairs, 2 with cyclic `Q_s`. The pairs fall into two groups by undirected `D`, each with two cycles and four pairs.
- The displayed pair `(r,s)` is the unique pair with `Q_s` cyclic, `Q_r` a forest and a `D`-cycle enclosing a vertex. `J(r,s) = 0`, `J(r~,s) = -2`, and the reversal is an involution on the two partners of `s`.
- The disk identity (both equations of 4.1, equation 4.2, and the delta-sum) holds on every directed cycle of `D` and of `Q_s` over all pairs. On the long cycle `B=5, W=6, I=3, h=7, l=2`.
- With spoke weights of unit circulation, `L+(C) - L-(C)` equals the number of white faces inside `C` for both cycles of `D` (6 and 1).
- Inequality (3.1) holds for all 1024 subsets of `X`, with equality at `S = {2}`.
- From `(s,r)`: `H - r` is a tree, the white-face tree is a tree, `P` has one edge per face and two components, both classes induce trees, and the complementary dual is a cycle through all 22 faces.

COMPUTED (`paper/figures/crosscheck_lab.py`): `workings/barnette_lab` returns the same counts, the same two cyclic pairs, the same `P` and the same cycle.

COMPUTED (`check.gluing`): in the 9-vertex nested-octahedron example the construction on each piece, with the prescribed edge passed across the cap, glues to two induced trees.

HUNCH: `L+(C) - L-(C) = W(C)`, the number of white faces inside a `D`-cycle, should hold in general when `H0` is connected. The spoke curve differs from `C` by sectors of black triangles, and the bounded faces of `H0` are the white triangles away from the outer edges. I checked it only on this example and did not write a proof. If true it is a cleaner statement for the paper than "positive".

## What failed and why

- Equal-area layout in the disk. The three faces on the outer arcs contain a circular segment about four times the mean face area, so the optimiser flattened them against the rim. Fix: a larger area target for those three faces.
- Keeping the 14-vertex triangulation with another root face. Two rootings work combinatorially but the degree-8 vertex is then adjacent to two roots and still produces thin faces.
- Rounded polylines for the edges of `G` looked kinked. Bezier curves through the midpoint of the crossed edge look better.
- My first caption for the `Q` figure stated a cycle length I had not computed, and it was wrong (6 instead of 3). Captions now take numbers from checked values or `check.py` asserts them.

## Still open

- No greyscale proofs and no print test.
- No computed check that the curved edges (edges of `G`, white tree) cross only their own dual edges. I checked by eye.
- The paper does not exist yet, so figure placement and cross-references are untested. `captions.json` refers to figures by the numbers of this sequence.
- The first-pass files `search.py`, `candidates.py`, `qa.py`, `example.json` and the `lab-export.json` of the 14-vertex example are removed from `paper/figures/`. They are at commit `af6c63a`.

## Three next steps

1. Place the figures in the draft and adjust captions to the text. Figures 1 to 3 belong in the first two sections, 4 to 8 with the pair and the disk identity, 9 to 11 with the sum, 12 and 13 with recovery.
2. Prove or refute the HUNCH above, and if it holds, state Lemma 5.3 with it.
3. Hand-route the white-face tree in Figures 12 and 13, and add a greyscale page to the gallery.

## Leads for others

- The 13-vertex example is small enough to list all 8 pairs in a table. It would serve the algebra and algorithm agents as a common test case. `paper/figures/running.json` has the faces; `checked.json` has every object.
- COMPUTED: no rooted 4-connected Eulerian triangulation with at most 11 vertices has a cyclic `Q_s`. An exposition that uses the cube or a prism cannot show the cancellation step.
- COMPUTED (`check.gluing`, `n_pairs` in `checked.json`): the 9-vertex gluing example has a separating triangle and still has 4 pairs of states. The hypothesis of Proposition 3.1 is sufficient for a pair, not necessary. The figure still uses the cut-and-glue route, because that is what the proof does.
