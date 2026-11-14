# Reproduction

Run from `E:\Personal\Math\mathathon\barnette-s-conjecture` in PowerShell. Environment used: Python 3.14.5, NetworkX 3.6.1. No installation was needed. Each run took under three seconds locally; one process was run at a time.

```powershell
python -B research/2026-11-14_astra_route-pfaffian/code/experiment.py
python -B research/2026-11-14_astra_route-pfaffian/code/followup.py
python -B research/2026-11-14_astra_route-pfaffian/code/verify.py
python -B research/2026-11-14_astra_route-pfaffian/code/map.py
```

`experiment.py` writes `data/results.json`. It constructs named graphs using NetworkX and explicitly identifies squares for trisums. Every edge list is saved. Perfect matchings are enumerated by bijective neighbor choices; complements give every 2-factor exactly once. A complement is Hamiltonian exactly when connected. Every unoriented simple three-edge path is tested for containment in those cycles. GF2 equations search for a signed adjacency matrix with all determinant terms positive and validate the solution on every perfect matching. Saved negative edges specify the orientation: positive edges go from the NetworkX color-1 class to color-0, negative edges in reverse. The same deterministic coloring convention is in the script.

`followup.py` writes `data/torus_signs.json` and `data/patterns.json`. It uses the saved rotation to assign cyclic signs to all incidence pairs, computes every coefficient of the root-free state polynomial, and enumerates all 6^3 abstract signature triples. It also calls the read-only planar reference constructor on the cube. That stdout certificate is recorded in the event log. Heawood's embedding is found by checking binary rotations at cubic vertices until seven simple hexagons occur.

`verify.py` writes `data/verification.json`, `data/categorical_four11.json`, and `data/categorical_replay.txt`. A separately written simple-path DFS enumerates Hamiltonian cycles without using perfect matching complements and checks P4 coverage. It also tests 2-extendability by deleting endpoints of every disjoint edge pair and finding a perfect matching. It imports the categorical author's code read-only, with bytecode disabled, and directs its four-cut census output to this folder. That census uses the existing `workings/barnette_lab/vendor/plantri.exe` to enumerate Eulerian triangulations through eleven vertices. It is a replay, not independent verification of the categorical algorithm.

`map.py` writes the local knowledge graph, frontier, status table, and HTML dashboard from the saved evidence. `events.jsonl` is a human-maintained append-only event log. No global coordinator files are changed.

All counts remain COMPUTED/T4, unreviewed. The DFS is an author cross-check, not an independent research referee. The input family has seven specified graphs; it is not an exhaustive census by vertex count. The four nonplanar Pfaffian inputs have orders 14,16,20,24. K3,3 is deliberately non-Pfaffian despite passing Hamiltonicity and P4 tests.
