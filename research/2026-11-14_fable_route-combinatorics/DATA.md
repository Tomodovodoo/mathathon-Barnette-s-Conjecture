# Data

All numbers here are `COMPUTED` by the scripts in `lab/`. The commands are in `lab/README.md`. Raw output is in `data/`.

Range: every isomorphism class of Eulerian triangulation of the sphere with at most 16 vertices (Barnette graphs with at most 28 vertices), and every face of it as `t0`. Triangulations with separating triangles are included, because Proposition 5.1 only assumes that a pair exists.

## How the triangulations were generated

`lab/tri.py` closes the octahedron under two operations, the 4-split of a vertex and the gluing of an octahedron into a face, and keeps one canonical code per isomorphism class (reflections identified). The class counts for 6 to 17 vertices are

```
1, 0, 1, 1, 2, 2, 8, 8, 32, 57, 185, 466
```

These agree with the counts of 3-connected cubic bipartite planar graphs on 8, 10, ..., 30 vertices as I remember them from the literature on `plantri`. I did not open a source during this run, so the completeness of the generation is `COMPUTED` up to that unchecked comparison. Nothing in the proofs depends on completeness.

## What is asserted on every instance

`lab/analyze.py` raises an error if any of these fails. None failed on the 7868 rooted triangulations.

1. All states have the same permutation sign.
2. The disk identity on every cycle of every `D(r, s)` and of every `Q_s`: the `delta`-sum is `-3` exactly when the cycle is counterclockwise, where orientation is decided by a flood fill of the faces on the left.
3. A partnered state with `k` cycles in `Q_s` has `2^k` partners.
4. `mu(s) = sum_r eps(r, s)` is `0` when `Q_s` has a cycle and `+1` or `-1` otherwise.
5. `L+(C) - L-(C)` for the spoke circulation equals the number of white faces inside `C`, found by an independent flood fill (up to 12 vertices), and is positive (up to 16).
6. `sum over tree matchings of eps(s) omega(s)^j` is `0` for `j < cmin`, and for `j = cmin` equals `(-1)^((n - cmin)/2) cmin! sum over minimal D of prod_C area(C)`.

`lab/survey.py` also asserts, for every tree matching and every edge `e0` of `t0`, that the construction of OpenAI Section 6 returns a Hamiltonian cycle of the dual avoiding `e0*`, that different tree matchings give different cycles, and that the cycle gives the state back.

## Totals

| Quantity | Value |
| --- | --- |
| rooted triangulations `(T, t0)` | 7868 |
| with a pair | 5088 |
| without a pair | 2780, all with a separating triangle |
| states, summed | 140358 |
| pairs, summed | 24744 |
| cycle covers `D`, summed | 5591 |
| tree matchings, summed | 24090 |
| Hamiltonian cycles avoiding `e0*` that are not of the form `C(s)` | 176726, every one gives a state with no partner |

Small instances are rigid. Up to 11 vertices there is one cycle cover per rooted triangulation and every partnered state is a tree matching. The first state with a cyclic `Q_s` and a partner appears at 12 vertices.

## Tally of the tested statements

From `data/survey_v16.txt`, `data/zpoly_v15.txt`, `data/extra_v16.txt`. "Holds in" counts rooted triangulations with a pair, out of 5088 unless stated.

| Statement | Holds in | First failure (vertices, class, face) |
| --- | --- | --- |
| every highest partnered state is a tree matching | 4993 | 12, 6, 8 |
| every lowest partnered state is a tree matching | 5032 | 14, 21, 13 |
| minimal `D`, all counterclockwise, gives a forest pair | 4925 | 12, 6, 8 |
| minimal `D`, all clockwise, gives a forest pair | 4969 | 13, 6, 6 |
| pairs maximising `omega(s) - omega(r)` are forest pairs | 4987 | 12, 6, 8 |
| ... and all cycles of their `Q_s` are counterclockwise | all | none (proved) |
| every `D` contains a forest pair | 5087 | 16, 158, 8 |
| the top state of the whole lattice is unique | all | none |
| the top state has a partner | 2717 | 10, 0, 1 |
| sign of a tree matching is `(-1)^rank` up to a constant | 1251 | 8, 0, 0 |
| `#tree matchings >= 2^cmin` | all | none |
| `#tree matchings = 2^cmin` | 4609 | 12, 6, 8 |
| `cmin = 1` | 2604 | 9, 0, 0 |
| `Z(q)/(q-1)^cmin` has coefficients of one sign (up to 15 vertices, of 1794) | 1786 | 14, 24, 6 |
| every Hamiltonian cycle avoiding `e0*` is `C(s)` for a tree matching (per `e0`, of 15264) | 1559 | 8, 0, 0 |
| a Hamiltonian cycle not of that form gives a state with no partner | all 176726 | none (proved) |
| the map cycle to state is injective (per `e0`, up to 15 vertices, of 8064) | 917 | 8, 0, 0 |

`cmin` by separating triangles, rooted triangulations with a pair: without separating triangles `cmin` is 1 in 2604 cases, 2 in 578, 3 in 192. With separating triangles it is 2 in 442, 3 in 1216, 4 in 56.

### Summary by number of vertices of T

| V(T) | N=|V(G)| | n | classes | rooted (T,t0) | with a pair | states (min..max) | pairs (max) | tree matchings (min..max over rooted with a pair) | cmin values | max trees/2^cmin |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 8 | 3 | 1 | 8 | 8 | 2..2 | 2 | 2..2 | 1: 8 | 1 |
| 8 | 12 | 5 | 1 | 12 | 12 | 3..3 | 2 | 2..2 | 1: 12 | 1 |
| 9 | 14 | 6 | 1 | 14 | 8 | 4..4 | 4 | 4..4 | 2: 8 | 1 |
| 10 | 16 | 7 | 2 | 32 | 32 | 4..5 | 2 | 2..2 | 1: 32 | 1 |
| 11 | 18 | 8 | 2 | 36 | 28 | 6..7 | 4 | 4..4 | 2: 28 | 1 |
| 12 | 20 | 9 | 8 | 160 | 120 | 5..9 | 10 | 2..8 | 1: 100, 3: 20 | 4 |
| 13 | 22 | 10 | 8 | 176 | 126 | 8..12 | 8 | 4..8 | 2: 126 | 2 |
| 14 | 24 | 11 | 32 | 768 | 546 | 6..16 | 10 | 2..10 | 1: 408, 3: 138 | 5 |
| 15 | 26 | 12 | 57 | 1482 | 914 | 10..21 | 24 | 4..16 | 2: 858, 4: 56 | 4 |
| 16 | 28 | 13 | 185 | 5180 | 3294 | 7..28 | 18 | 2..16 | 1: 2044, 3: 1250 | 8 |

### Distinct rooted profiles, V(T) <= 12

| V | class | #t0 with this profile | sep. triangles | states | partnered states | pairs | D by cycle count | cmin | lead | tree matchings (+/-) | partner-count histogram k: #s | HC of G | HC avoiding each edge of t0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 0 | 8 | 0 | 2 | 2 | 2 | {"1": 1} | 1 | 1 | 2 (1/1) | {"0": 2} | 6 | [2, 2, 2] |
| 8 | 0 | 12 | 0 | 3 | 2 | 2 | {"1": 1} | 1 | 2 | 2 (1/1) | {"0": 2} | 8 | [2, 2, 4] |
| 9 | 0 | 2 | 1 | 4 | 4 | 4 | {"2": 1} | 2 | 4 | 4 (2/2) | {"0": 4} | 12 | [4, 4, 4] |
| 9 | 0 | 6 | 1 | 4 | 0 | 0 | {} | None | None | 0 (0/0) | {} | 12 | [4, 4, 4] |
| 9 | 0 | 6 | 1 | 4 | 4 | 4 | {"2": 1} | 2 | 1 | 4 (2/2) | {"0": 4} | 12 | [4, 4, 4] |
| 10 | 0 | 8 | 0 | 5 | 2 | 2 | {"1": 1} | 1 | 3 | 2 (1/1) | {"0": 2} | 14 | [4, 4, 6] |
| 10 | 0 | 8 | 0 | 5 | 2 | 2 | {"1": 1} | 1 | 3 | 2 (1/1) | {"0": 2} | 14 | [2, 4, 8] |
| 10 | 1 | 16 | 0 | 4 | 2 | 2 | {"1": 1} | 1 | 3 | 2 (1/1) | {"0": 2} | 10 | [2, 2, 6] |
| 11 | 0 | 1 | 1 | 6 | 4 | 4 | {"2": 1} | 2 | 12 | 4 (2/2) | {"0": 4} | 16 | [4, 6, 6] |
| 11 | 0 | 3 | 1 | 6 | 0 | 0 | {} | None | None | 0 (0/0) | {} | 16 | [4, 6, 6] |
| 11 | 0 | 5 | 1 | 6 | 4 | 4 | {"2": 1} | 2 | 2 | 4 (2/2) | {"0": 4} | 16 | [4, 4, 8] |
| 11 | 0 | 2 | 1 | 6 | 4 | 4 | {"2": 1} | 2 | 2 | 4 (2/2) | {"0": 4} | 16 | [4, 6, 6] |
| 11 | 0 | 5 | 1 | 6 | 0 | 0 | {} | None | None | 0 (0/0) | {} | 16 | [4, 4, 8] |
| 11 | 0 | 2 | 1 | 6 | 4 | 4 | {"2": 1} | 2 | 5 | 4 (2/2) | {"0": 4} | 16 | [4, 4, 8] |
| 11 | 1 | 6 | 0 | 7 | 4 | 4 | {"2": 1} | 2 | 5 | 4 (2/2) | {"0": 4} | 20 | [6, 6, 8] |
| 11 | 1 | 12 | 0 | 7 | 4 | 4 | {"2": 1} | 2 | 2 | 4 (2/2) | {"0": 4} | 20 | [4, 6, 10] |
| 12 | 0 | 2 | 2 | 8 | 8 | 8 | {"3": 1} | 3 | 28 | 8 (4/4) | {"0": 8} | 24 | [8, 8, 8] |
| 12 | 0 | 12 | 2 | 8 | 0 | 0 | {} | None | None | 0 (0/0) | {} | 24 | [8, 8, 8] |
| 12 | 0 | 6 | 2 | 8 | 8 | 8 | {"3": 1} | 3 | 4 | 8 (4/4) | {"0": 8} | 24 | [8, 8, 8] |
| 12 | 1 | 16 | 2 | 8 | 0 | 0 | {} | None | None | 0 (0/0) | {} | 24 | [8, 8, 8] |
| 12 | 1 | 2 | 2 | 8 | 8 | 8 | {"3": 1} | 3 | 1 | 8 (4/4) | {"0": 8} | 24 | [8, 8, 8] |
| 12 | 1 | 2 | 2 | 8 | 8 | 8 | {"3": 1} | 3 | 4 | 8 (4/4) | {"0": 8} | 24 | [8, 8, 8] |
| 12 | 2 | 2 | 2 | 8 | 8 | 8 | {"3": 1} | 3 | 7 | 8 (4/4) | {"0": 8} | 24 | [8, 8, 8] |
| 12 | 2 | 12 | 2 | 8 | 0 | 0 | {} | None | None | 0 (0/0) | {} | 24 | [8, 8, 8] |
| 12 | 2 | 6 | 2 | 8 | 8 | 8 | {"3": 1} | 3 | 1 | 8 (4/4) | {"0": 8} | 24 | [8, 8, 8] |
| 12 | 3 | 8 | 0 | 8 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 20 | [6, 6, 8] |
| 12 | 3 | 8 | 0 | 8 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 20 | [4, 6, 10] |
| 12 | 3 | 4 | 0 | 8 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 20 | [4, 4, 12] |
| 12 | 4 | 4 | 0 | 7 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 20 | [6, 6, 8] |
| 12 | 4 | 4 | 0 | 7 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 20 | [2, 6, 12] |
| 12 | 4 | 4 | 0 | 7 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 20 | [2, 4, 14] |
| 12 | 4 | 8 | 0 | 7 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 20 | [4, 4, 12] |
| 12 | 5 | 8 | 0 | 8 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 24 | [6, 8, 10] |
| 12 | 5 | 4 | 0 | 8 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 24 | [2, 8, 14] |
| 12 | 5 | 4 | 0 | 8 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 24 | [4, 6, 14] |
| 12 | 5 | 4 | 0 | 8 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 24 | [4, 10, 10] |
| 12 | 6 | 12 | 0 | 9 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 24 | [6, 8, 10] |
| 12 | 6 | 6 | 0 | 9 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 24 | [4, 10, 10] |
| 12 | 6 | 2 | 0 | 9 | 9 | 10 | {"1": 1, "3": 1} | 1 | 4 | 8 (4/4) | {"0": 8, "1": 1} | 24 | [8, 8, 8] |
| 12 | 7 | 20 | 0 | 5 | 2 | 2 | {"1": 1} | 1 | 4 | 2 (1/1) | {"0": 2} | 12 | [2, 2, 8] |

### Tree matchings against 2^cmin (rooted triangulations with a pair)

| cmin | tree matchings | how many rooted triangulations |
|---|---|---|
| 1 | 2 | 2248 |
| 1 | 4 | 72 |
| 1 | 8 | 179 |
| 1 | 10 | 96 |
| 1 | 12 | 5 |
| 1 | 14 | 1 |
| 1 | 16 | 3 |
| 2 | 4 | 932 |
| 2 | 6 | 40 |
| 2 | 8 | 37 |
| 2 | 16 | 11 |
| 3 | 8 | 1373 |
| 3 | 12 | 22 |
| 3 | 16 | 13 |
| 4 | 16 | 56 |
