# Referee code, version 2

Written from the text of `proofs/involutions/involutions.tex` and of `paper/main/barnette.tex` Section 4. It imports nothing from the author's, the reviser's or the first referee's code. Inputs: `workings/barnette_lab/vendor/plantri.exe -ba v` (rotation systems) for `census.py` and `extra.py`; the canonical census of `research/2026-11-14_fable_route-combinatorics/lab/tri.py` as an input generator only, for `canonical.py`, so that class numbers and face IDs match the note. Standard library only, exact rational arithmetic. Run from the repository root.

| Command | Time | Output |
| --- | --- | --- |
| `python research/2026-11-14_fable_referee-involutions-v2/code/census.py 14 12` | 62 s | `out/census-14.json`, `out/census-14.log` |
| `python research/2026-11-14_fable_referee-involutions-v2/code/census.py 10 10` | 1 s | `out/census-10.json`, `out/census-10.log` |
| `python research/2026-11-14_fable_referee-involutions-v2/code/canonical.py 14 14` | 32 s | `out/canonical-14.json`, `out/canonical-14.stdout` |
| `python research/2026-11-14_fable_referee-involutions-v2/code/running.py` | 2 s | `out/running.json` |
| `python research/2026-11-14_fable_referee-involutions-v2/code/extra.py` | 20 s | `out/extra.json` |
| `python research/2026-11-14_fable_referee-involutions-v2/code/figure2.py` | 1 s | `proofs/involutions/figures/second.tex` |

`edit_note.py` and `figfix.py` record the one-time edits to the note and to two figure files. They are not idempotent.

## Files

- `fp.py`. An instance is a list of oriented triangles and an outer face. States, pairs, cycles of `D_p`, inside sets by flood fill of the dual, `J`, cycles of `Q_s` (two ways). A mode gives each white face an ordered list of crossings `(face, corner, signed crossing)`: `path_crossings` reads it off face paths with the main paper's rule for `kappa`, `ray_crossings` off an exact Tutte drawing and a ray direction. `Model` holds objects, the sign and the two maps of Sections 3 and 4, with the order on cycles as a parameter.
- `census.py`. For each rooted instance and mode, asserts: the three claims of Lemma 7 for every pair, cycle and white face; both maps stay in `Omega`, are involutions, take the same branch on the return move, and reverse sign off their fixed sets; the first map fixes exactly forest pairs and its cycle is determined by `s` alone; the second-fixed set has the form and sign of Lemma 6 and `F` members, with `F` computed without marks; the signed size of `Omega`; the walk from every second-fixed object; vanishing moments below `m` and the Section 8 identity; zero signed count with `m - 1` marks. In path modes also `H = -omega`, Lemma 4.6 of the main paper and the value of its Proposition 4.8. Path modes: `bfs+`, `bfs-` (breadth-first, ties by increasing or decreasing face ID), `dfs`, `rand` (random spanning tree), `walk` (independent loop-erased random walks, no tree). The modes `bfs-`, `rand`, `walk` use a random order on cycles, the others the lexicographic one. Through `RAY_VMAX` vertices it also runs two ray directions and tests `kappa` against coordinates.
- `canonical.py`. The same checks in the note's encoding and the note's layout recipe, to reproduce its printed counts and the witnesses of Section 7.
- `running.py`. The running example: the note's exact layout from `running-geometry.json`, the 279-row table parsed from `example-table.tex`, the data of Figures 1 to 3, five path families, and the orientation of the main paper's drawing with its Table 2.
- `extra.py`. Disk-identity signs, `J`, the local delta identity on all pairs; the interior nonfirst witness.

## Results (COMPUTED)

All assertions pass. Range: all 1206 rooted instances with at most 14 vertices, 880 with a pair, `m = 1, 2, 3` on 560, 162, 158 of them.

| Mode (plantri face IDs) | Roots | Objects | First-fixed | Second-fixed | Longest walk | Roots with zero count at `m + 1` |
| --- | --- | --- | --- | --- | --- | --- |
| `bfs+` | 880 | 16586 | 16448 | 4658 | 4 | 150 |
| `bfs-` | 880 | 17882 | 17714 | 4658 | 4 | 130 |
| `dfs` | 880 | 717994 | 716786 | 4658 | 2 | 36 |
| `rand` | 880 | 49436 | 49216 | 4658 | 2 | 87 |
| `walk` | 880 | 139262 | 138654 | 4658 | 6 | 68 |
| ray, direction (1/97, 1) | 208 (through 12 vertices) | 16662 | 16638 | 742 | 2 | |
| ray, direction (-13/7, -1) | 208 | 25060 | 25048 | 742 | 2 | |

In the note's encoding (`canonical.py`): rays 221050 objects, 4658 second-fixed, walks 0 (4617) and 2 (41), 78 zeros at `m + 1`; `bfs+` 17832 objects, `bfs-` 18362, longest walk 4 in both, 123 and 125 zeros at `m + 1`. Witnesses: 9-vertex class 0 root 0 has `m = 2`, 40 objects, 4 second-fixed; 12-vertex class 0 root 0 has `m = 3`, 1200, 28; 14-vertex class 27 root 0 has `m = 3`, 826, 8, and no separating triangle; 11-vertex class 1 root 0 has `m = 2` and two objects on the interior nonfirst branch.

The object totals of the two breadth-first trees differ between the two encodings (16586 against 17832) because face IDs differ, which changes the tie-breaking and so the trees. `F` does not.

Running example: 12 states, 8 pairs, `m = 2`, `F = 9`, 279 objects, signed sum -9, all 279 table rows agree. Path families give 31, 49, 161, 33, 85 objects.
