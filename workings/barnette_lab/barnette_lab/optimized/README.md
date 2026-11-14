# Optimized construction

This subpackage leaves the existing lab objects and exports unchanged. Its public function uses a flow pair, a bounded deterministic exchange search, bounded path DP, and complete rollback enumeration. Failed flow invokes separator gluing. Every output is checked against the input graph by a primal-only checker.

From the repository root:

```powershell
$env:PYTHONPATH='workings/barnette_lab'
python -B -m barnette_lab.optimized graph.json
python -B -m unittest barnette_lab.optimized.test_optimized -v
python -B workings/barnette_lab/run_tests.py quick
```

Input JSON:

```json
{"vertices":[0,1,2,3,4,5,6,7],"edges":[[0,1],[0,3],[0,4],[1,2],[1,7],[2,3],[2,6],[3,5],[4,5],[4,7],[5,6],[6,7]],"forbidden":[0,1]}
```

The result is a cyclic ordering, without repeating the initial vertex, and counters. Python use:

```python
from barnette_lab.optimized import hamiltonian_cycle
cycle = hamiltonian_cycle(graph, forbidden_edge)
```

`enumerate_tree(instance)` is the complete rollback search. `path.path_tree(instance)` is the complete edge-frontier DP. Optional DP resource limits raise `BudgetExceeded`, never return a false nonexistence answer. Public input validation and dual construction use the existing Instance implementation. The public solver is deterministic; the separate benchmark random walks are not part of it. NetworkX and SymPy are existing lab dependencies; OR-Tools and matplotlib are only benchmark dependencies.

Correctness and bounds are in `proofs/algorithm/ALGORITHM.md`. The public solver is not polynomial-time in the worst case. No linear-time separator implementation or dynamic link-cut structure is claimed.
