# Referee code

Independent of `workings/barnette_lab`. Python 3.14, standard library only. No networkx, no sympy. Run everything from the repository root.

| File | What it does | Command | Output | Time |
| --- | --- | --- | --- | --- |
| `etri.py` | The implementation. Triangulation as oriented triangles, faces found as non-separating triangles, states, pairs, `delta`, `J`, `eps`, D cycles with a flood-fill test for inside, `Q_s`, tree matchings, my own spoke weights, `F` by pairs and by `2^n` determinants, Bareiss and Fraction determinants, recovery of the Hamiltonian cycle. | imported | | |
| `referee.py` | Runs every claimed identity on named examples (both mirrors) and on all plantri Eulerian triangulations of order 6 to 14 at every root. | `python -B research/2026-11-14_fable_referee-determinants/code/referee.py` | `results.json` | about 3.5 minutes |
| `export_lab.py` | The only file that imports the lab. Dumps its states, pairs, `J`, weights, polynomial, recovery certificate, two-matroid candidate, 3,000 sampler draws and Hamiltonian cycles for 19 instances. | `python -B research/2026-11-14_fable_referee-determinants/code/export_lab.py` | `lab_export.json` | about 3.5 minutes |
| `compare_lab.py` | Compares that dump with `etri.py`. Rebuilds sol's hexagonal-prism determinant in `Q[x]/(x^4 - x^2 + 1)` and astra's real determinant from the lab's labels and weights. | `python -B research/2026-11-14_fable_referee-determinants/code/compare_lab.py` | `compare_lab.json` | under a second |
| `extra_checks.py` | Replays astra's 18 stored rows from their edge lists, checks the gauge identity between the two determinants, compares raw determinant and `F` at random weights, checks the sign flip under both reversals. | `python -B research/2026-11-14_fable_referee-determinants/code/extra_checks.py` | `extra_checks.json` | about a second |

## Data sources

- Octahedron, bipyramids, dual of the truncated octahedron (cube with face centres), dual of the truncated cuboctahedron (barycentric subdivision of the cube surface), double octahedron: built in `etri.py`.
- The 12-vertex cyclic example: edge list read from `research/2026-11-14_sol_route-constructive/data/hard_instance.json`.
- Census: `workings/barnette_lab/vendor/plantri.exe -ba N` for N = 6..14, used as a source of edge lists only. Counts 1, 0, 1, 1, 2, 2, 8, 8, 32. Completeness is plantri's guarantee, not mine.
- Astra's rows: edges and root triangle from `research/2026-11-14_astra_route-dimers/data.json`.

## Conventions

Each directed edge `u -> v` lies on one oriented triangle, `left[(u, v)]`. `delta(u, v) = +1` when that triangle is black. `mirror=True` reverses every triangle and negates `delta`. A cycle is counterclockwise when the disk not containing `t0` is on its left, decided by flood fill over faces.

Spoke weights. The dual of the spoke graph `H0` has the white triangles as vertices, with the three white triangles around `t0` merged into one outer vertex. I take a spanning tree of that dual from the outer vertex and push one unit from every other white triangle to the root. The result has circulation 1 around every white triangle away from `t0`. The routine asserts this. It differs from the lab's weights by a gauge.

## What a run covers

`results.json` totals: 1,246 rooted instances, 13,872 states, 3,428 pairs, 3,384 tree matchings, 908 instances with a pair, 22 with a cyclic `Q_s` that has mates, `c_min` 1, 2, 3 on 572, 178, 158 instances. Polarization by `2^n` determinants runs on 300 instances (`n` up to 11). Symbolic Laplacian coefficient extraction runs on 24 instances (`n <= 5`). Every check passed. The random weights use seed 20261114.
