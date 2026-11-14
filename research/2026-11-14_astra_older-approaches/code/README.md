# Reproducing the computations

From the repository root, with Python, networkx, sympy and the existing read-only lab installation:

```powershell
python research/2026-11-14_astra_older-approaches/code/test_routes.py
python research/2026-11-14_astra_older-approaches/code/goodey.py
python research/2026-11-14_astra_older-approaches/code/refined.py
python research/2026-11-14_astra_older-approaches/code/chains.py
```

Each command writes the correspondingly named JSON, except `test_routes.py` writes `results.json`. Outputs include explicit edge lists for counterexamples and generated families. Census input is existing `workings/barnette_lab/vendor/plantri.exe -ba n`. The reference implementation is imported, never edited. Python bytecode under the lab is incidental cache output, not source changes.

Ranges: all plantri simple Eulerian triangulations of orders 6–12 at every face root; all four/six degree duals of orders 6–16 at the first embedding face; two uniform triangular refinements; octahedral chains k=1–8; four named planar graphs; Heawood, one cube trisum, K3,3 control. The named planar edge-forcing test handles every edge. Nonplanar Hamiltonian cycles are counted by enumerating perfect matchings and testing connectivity of their degree-two complements. Bracehood is checked by extending every disjoint edge pair to an enumerated perfect matching. Three-edge paths are tested explicitly. No Pfaffian-orientation recognition is implemented.

T4 only. These tests were not independently refereed. Completeness of graph generation relies on plantri; the returned abstract graphs are re-embedded by NetworkX. Separator tests use the lab's existing implementation. The contracted-octahedron negative is additionally proved without computation in BRIDGES.md. This is not an exhaustive test of every facial 2-factor or every multigraph contraction. Ordinary fullerene graphs are outside the bipartite lab's input domain.

An initial `goodey.py` summary print tried to sort `None` with integers when a root had no pair. JSON had already been written. The print was corrected and the command rerun. No-pair cases remain in the data, rather than being dropped from the census.

Run `python research/2026-11-14_astra_older-approaches/code/validate.py` for the dictionary and chain spot checks, producing validation.json. Run `python research/2026-11-14_astra_older-approaches/code/build.py` to regenerate the DOT, manifest and handoff JSON. A Windows code-page error in the first build attempt was fixed by saving prose and build.py as UTF-8, then rerunning.
