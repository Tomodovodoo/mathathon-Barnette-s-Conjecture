# Independent checks

`COMPUTED`. Run from the repository root with Python 3.14.5. Dependencies used are networkx, numpy and sympy. No script imports or executes the reviewed author's laboratory. The explicit counterexamples are read as face-list input from its text output. `additional.py` also imports the separately authored reference implementation in `workings/barnette_lab/`, as requested.

```powershell
py -3.14 -B research/2026-11-14_astra_referee-combinatorics/code/check.py --max 12
py -3.14 -B research/2026-11-14_astra_referee-combinatorics/code/check.py --examples
py -3.14 -B research/2026-11-14_astra_referee-combinatorics/code/check.py --max 16
py -3.14 -B research/2026-11-14_astra_referee-combinatorics/code/additional.py
py -3.14 -B research/2026-11-14_astra_referee-combinatorics/code/compare.py
py -3.14 -B research/2026-11-14_astra_referee-combinatorics/code/cube_witness.py
```

These produce `up_to_12.json`, `examples.json`, `up_to_16.json`, `additional.json`, `comparison.json`, and `cube_cardinality.json`, respectively. Each output records its actual command. Run serially. The completed main 16-vertex run took 190.7 seconds, the additional run 8.0 seconds. An earlier, slower extension run was stopped after completing size 15, before ten minutes, then restarted with cached disk regions and fraction-free integer determinants. The completed JSON is the authority for results. There are no continuing jobs.

Generation uses `workings/barnette_lab/vendor/plantri.exe -ba V` for each size. The executable is the existing pinned 4.5 build described in that lab's setup script. Its SHA-256 is stored in the main outputs. `-b` selects Eulerian triangulations; the default connectivity is three and separating triangles are included. `-a` emits adjacency lists. We recover an embedding with networkx, use every face as outer, and make its colour black. The unrooted class counts from 6 to 16 vertices are 1, 0, 1, 1, 2, 2, 8, 8, 32, 57, 185.

| Test population | Through 12 | Through 16 |
| --- | ---: | ---: |
| Rooted triangulations | 262 | 7,868 |
| States and determinants | 1,706 | 140,358 |
| Ordered disjoint pairs | 624 | 24,744 |
| Tree matchings | 620 | 24,090 |
| Directed D-cycle occurrences | 1,120 | 60,152 |
| Directed Q-cycle occurrences under partners | 4 | 654 |
| Height monomials, all degrees through c_min | 4,360 | 636,682 |
| Hamiltonian-cycle/root incidences | 4,784 | 378,632 |
| Hamiltonian states outside the tree-matching image | 2,924 | 306,362 |

All main assertions pass. The height monomials use every multiset of white-face indices, so repeated factors and all distinct monomials occur. Ordered permutations of the same factors give identical products and right-hand counts. Cases without a pair skip c_min statements and still check determinants and Hamiltonian states.

The larger nonimage count than the author's 176,726 includes roots without a pair. Restricting to the 5,088 roots with pairs gives exactly 176,726. `compare.py` checks equality of the complete multisets of rooted profiles with fields size, state count, pair count, tree-matching count, c_min, and Hamiltonian-cycle count. The two generators agree on all those profiles through 16. This is stronger than agreement of grand totals, but does not prove completeness of the author's generator for arbitrary size.

`additional.py` passes 7,636 arbitrary directed state-cycle tests, 1,706 exact signed-determinant tests, 4,784 compatible-face-pairing tests of the acyclicity lemma, and 1,706 reference volume comparisons. The reference volume is compared up to a common additive constant and, where necessary, reversal of the embedding orientation. It also checks the reflected versions of every printed counterexample.

## What is independent

- States are enumerated by recursive incidence assignment. Partners are found by checking every pair of states, not by the pseudoforest classification being tested.
- Cycle interiors are found by cutting the primal cycle's dual edges and flood filling from the outer face. Heights use separate paths in the spoke dual. Thus area and height difference are computed through different graphs.
- The reduced incidence determinant is an exact fraction-free integer calculation. The original through-12 run and additional tests use SymPy's exact determinant as a second implementation. The complex twisted matrix and its local gauge are tested separately with numpy, tolerances 1e-8 and 1e-10.
- Hamiltonian cycles are enumerated as complements of all perfect matchings of the cubic dual, then checked for connectivity. This does not assume the tree-matching constructor or the dichotomy under review.
- The four explicit counterexample face lists are used exactly, preserving their original orientation and root. Absolute height ranks may shift. Separate independent witnesses include full face lists and state data.

## Limits and interpretation

Plantri and networkx are not formally verified here. The finite exact results cross-check the author's implementation and, for volume, the third implementation; they are computational evidence for the general mathematical statements, not substitutes for the proofs.

The main generator identifies reflections. The theorem identities transform equivariantly under reflection. Extremal-rank and clockwise-versus-counterclockwise tallies do not. Do not compare such tallies without aligning the orientation. In particular the reflected printed 12-vertex witness refutes both the lowest-state and all-clockwise-minimum-cover conjectures, invalidating the author's embedding-independent first-failure sizes 14 and 13. `additional.json` contains these reflected witnesses.

Only the four full face-list witnesses are exact replays of the author's named instances. Other refutations use newly generated witnesses with independent class indices. The main task did not require replaying the auxiliary magnetic coefficient and Fourier formulas; those received algebraic review only.

The new `cube_cardinality.json` witness has 13 vertices, six tree matchings and c_min=2. It refutes partition into abstract c_min-dimensional cubes by cardinality. It includes all states and pairs, not only the failure flag. This is the referee's replacement for the overbroad inference from the author's mixed-sign polynomial witness.

JSON rows count a Hamiltonian cycle once per root, with the unique avoided outer edge determining which of the three choices it belongs to. They do not multiply each cycle by three. The unrooted class enumeration and all-root counts match the review's stated range.
