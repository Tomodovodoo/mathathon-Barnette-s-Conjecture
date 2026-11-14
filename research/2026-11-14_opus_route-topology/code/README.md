# Code for the topology route

`topo.py` is the only script. It imports the shared reference implementation `workings/barnette_lab` read-only and uses its plantri binary (`workings/barnette_lab/vendor/plantri.exe`, built by `workings/barnette_lab/setup_plantri.py`).

Run from the repository root. Each command writes `data/<name>.json`, and the producing command is stored in the file's `command` field.

| Command | Range | What it tests | Time |
| --- | --- | --- | --- |
| `python research/2026-11-14_opus_route-topology/code/topo.py disk 12` | all rooted, V ≤ 12 (262) | colouring vs delta; `W = B + 1` on chosen-edge cycles; Gauss-Bonnet formula `B - W = 2m - h + 2` | 50 s |
| `... topo.py ham 14` | 166 rooted, V ≤ 14 | Hamiltonian cycles of `G`; recovery injective; tree matchings vs cycles avoiding `e0*`; Thomason parity | 5 s |
| `... topo.py lattice 14` | 166 rooted | clock-move graph: connected, one top and one bottom; position of tree matchings | 2 s |
| `... topo.py lattice2 14` | 166 rooted | mate of a tree matching; height vs signed white area | 3 s |
| `... topo.py sepcheck 14` | 166 rooted | lattice2 split by presence of separating triangles | 5 s |
| `... topo.py rootpoly 14` | 166 rooted × 3 colours | `Q_s` complement is a spanning tree of `G_c`; clock moves vs root-polytope facet adjacencies | 3 s |
| `... topo.py morse 14` | 166 rooted | mates of `s` form a Boolean lattice graded by `J`; signed sum is `[k = 0]` | 2 s |
| `... topo.py hyper 12` | 86 rooted, V ≤ 12 | Kálmán hypertree map of states (six hypergraphs); extreme-point position | 4 s |
| `... topo.py degpoly 10` | 66 rooted, V ≤ 10 | two-sided degree vectors of spanning trees of `H` (brute force); target in hull; one-sided realisability; saturation on 8 small cases | 75 s |
| `... topo.py rainbow 16` | 826 rooted, V ≤ 16 | point-side and black-side rainbow spanning trees (matroid intersection) vs existence of a pair | 8 s |
| `... topo.py nodal 14` | all unrooted, V ≤ 14 | sign patterns of Laplacian eigenvectors as induced-tree partitions | 2 s |

"Rooted" means every plantri Eulerian triangulation of that order (`plantri -ba V`, V = 6..max), with every face as outer face up to V = 10 (V = 12 for `disk`, `degpoly` and `rainbow`) and two outer faces (indices 0 and the first face of the other colour) above. Instances whose `Instance` constructor fails are skipped.

`exp_hyperside` (matroid intersection directly on `H` using networkx) is kept in the file but was stopped as too slow. `exp_rainbow` computes the same predicate through Lemma 2.1 duality, and on V ≤ 10 it agrees with the brute-force `exp_degpoly`.

Limits: the disk experiment samples random states and choices (seeds fixed in the code). Every other experiment is exhaustive over states in its stated range. Nothing here was validated by an independent implementation, so all results are T4 (COMPUTED, unreviewed).
