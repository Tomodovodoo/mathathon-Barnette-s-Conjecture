# Reproduce the algebra tests

Run from the repository root with Python 3.14, networkx and sympy installed. Use `python -B` so the read-only lab import writes no bytecode. No package installation or reference implementation edits are needed.

```powershell
python -B research/2026-11-14_sol_route-algebra/code/count.py --max 16
python -B research/2026-11-14_sol_route-algebra/code/invariants.py
python -B research/2026-11-14_sol_route-algebra/code/gauge.py
python -B research/2026-11-14_sol_route-algebra/code/check.py
python -B research/2026-11-14_sol_route-algebra/code/tables.py
python -B research/2026-11-14_sol_route-algebra/code/map.py
python -X utf8 -B research/2026-11-14_sol_route-algebra/labyrinth/lab.py check
python -X utf8 -B research/2026-11-14_sol_route-algebra/labyrinth/lab.py build
```

`count.py` calls the installed plantri executable with `-ba`, enumerates every state and ordered pair with the lab, and independently enumerates primal perfect matchings to count Hamiltonian complements and labeled Tait colorings. It visits every facial root, including both choices of black/white convention and obstructed roots. Face IDs are implementation labels. To reconstruct a rooted case from its saved edge list, identify the saved root vertex set among the new embedding's faces. Sorted-edge reconstruction can renumber faces and dual vertices. `check.py` performs this remapping explicitly.

`invariants.py` computes the five smallest graphs' Tutte polynomials and all six trinity hypergraph activity polynomials by spanning-tree subset enumeration. It also checks the determinant-product Wick expansion using exact integer incidence weights. This checks the algebraic expansion, not numerical Gaussian sampling.

`check.py` independently enumerates all permutations for states and uses a disjoint-set test after root contraction for forests on all 66 roots through order ten. Hamiltonian path DFS checks all cycles and edge-avoidance counts on the same five graphs. These are author-written second implementations, not an independent referee's code.

`tables.py` regenerates every displayed count and residue from JSON. `map.py` writes a local frontier and proof-status dashboard using the supplied labyrinth engine. No server or public preview is used. Counts stay T4 until independently checked. New proofs stay T2 unreviewed.

The largest single run is the all-root count campaign. Keep one process at a time; smaller maxima are valid quick reproductions. The script checkpoints after each completed order. The named 48-vertex example is deliberately non-exhaustive at its order.

The count campaign also includes every root of the saved 17-vertex restart fixture. The 12-vertex cyclic fixture is isomorphic to a map already in the exhaustive corpus. `fixture.py` appends the restart case without rerunning an existing corpus. `gauge.py` tests a global forest-sign incidence gauge by exact GF2 elimination and saves any inconsistent subsystem. Windows dashboard generation needs `-X utf8` for the supplied template.
