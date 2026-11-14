# Data and reproduction

COMPUTED. All commands below run from `E:\Personal\Math\mathathon\barnette-s-conjecture`. Timing uses `time.perf_counter` and one process at a time. `data/environment.json` records Python and dependency versions. No benchmark is a worst-case complexity measurement.

```powershell
$env:PYTHONPATH='workings/barnette_lab'
python workings/barnette_lab/setup_plantri.py
python -m barnette_lab.verify --output research/2026-11-14_sol_route-constructive/data --max-dual-vertices 10 --plantri workings/barnette_lab/vendor/plantri.exe --plantri-max 14
python -m unittest discover -s workings/barnette_lab/tests -v
python research/2026-11-14_sol_route-constructive/scan.py
python research/2026-11-14_sol_route-constructive/supplemental.py
python research/2026-11-14_sol_route-constructive/benchmark.py --plantri workings/barnette_lab/vendor/plantri.exe --output research/2026-11-14_sol_route-constructive/data
python research/2026-11-14_sol_route-constructive/check_signed_determinant.py
python research/2026-11-14_sol_route-constructive/exact_determinant.py
python research/2026-11-14_sol_route-constructive/other_candidates.py
python research/2026-11-14_sol_route-constructive/growing_family.py
python research/2026-11-14_sol_route-constructive/finalize_data.py
```

COMPUTED. `setup_plantri.py` reproduces the pinned mirror source and timing patch; it needs GCC. `data/plantri_provenance.json` records the hash, version and failed official-download attempt. The official project page is [Brinkmann and McKay's plantri page](https://users.cecs.anu.edu.au/~bdm/plantri/). The mirror used here is older than the current official release. Its complete-generation guarantee is taken from plantri's documentation, not independently proved here. `scan.py` stops at the first bad pair and does not exhaust its final order.

## File inventory

| File in data/ | Command or script | Meaning |
| --- | --- | --- |
| verification.json | barnette_lab.verify | COMPUTED. 77 rooted finite verification runs, including repetitions. |
| supplemental.json | supplemental.py | COMPUTED. All 55 plantri outputs at orders 6 through 14, grouped-polynomial checks; 7,819 region checks at orders <=10. |
| plantri_scan.json | scan.py | COMPUTED. Counts and first cyclic-pair discovery; early stop at order 12, index 2. |
| hard_instance.json | scan.py | COMPUTED. The 20-vertex primal witness, stored by T edges, root and bad ordered pair. |
| benchmarks.json | benchmark.py | COMPUTED. 86 solvable rooted samples selected at evenly spaced enumeration indices through T order 20. Obstructed roots are skipped. |
| bad_starts.json | benchmark.py | COMPUTED. Ten bad pair starts, their full T edges, marked statistics and sixteen seeds per walk method. |
| naive_determinant.json | check_signed_determinant.py | COMPUTED. Floating-point diagnostics on four named graphs; do not use as the exact counterexample. |
| exact_determinant.json | exact_determinant.py | COMPUTED. Exact symbolic hexagonal-prism counterexample and squarefree coefficient. |
| other_candidates.json | other_candidates.py | COMPUTED. Matroid relaxation witnesses and white-tree rejection trials. |
| growing_family.json | growing_family.py | COMPUTED. Seven structured graphs, 24 through 288 primal vertices. |
| cube.json, truncated_octahedron.json | finalize_data.py, using verify.export | COMPUTED. Complete worked objects; copies also live in workings/barnette_lab/examples/. |
| environment.json | finalize_data.py | COMPUTED. Runtime and library versions. |
| plantri_provenance.json | recorded during setup | COMPUTED. Source provenance and exact compilation patch. |

COMPUTED. The three source PNGs were generated with PyMuPDF from page index 6 of each local paper at scale 1.3 to inspect the spoke formula and Li involutions. The PDF originals remain untouched. They are source-reading aids, not produced data about the graphs.

## Sample and measurement limits

COMPUTED. Plantri outputs by dual order 6 through 14 were respectively 1, 0, 1, 1, 2, 2, 8, 8 and 32. Verification uses one root per output. The benchmark obtains all outputs through order 20, then chooses at most twelve evenly spaced indices per order. It measures only those chosen roots passing the initial pair test. This is an enumeration-biased convenience sample, not a random graph model.

COMPUTED. On the seven truncated-even-bipyramid examples, enumeration times in seconds were approximately 0.0046, 0.0096, 0.0204, 0.0350, 0.1065, 0.1410 and 0.3349. The primal orders were 24, 48, 72, 96, 144, 192 and 288. These graphs usually need no enumeration backtracking. The marked times exclude max flow and mostly measure weight construction and normalization. General exponential behavior cannot be inferred or refuted by this easy family.

COMPUTED. On the 86 small benchmark roots, the enumerator visited at most 36 retained prefixes. Ten saved non-tree pair starts were used in 320 capped random or greedy runs, all successful and at most ten exchange steps. Determinant sampling accepted 319 tree states in 784 trials. The marked starts include two restarts from four D cycles to two. The recorded counts distinguish alternating involution moves from initial orientation reversals.

COMPUTED. White-tree rejection accepted 24/100 cube trials, 3/100 hexagonal-prism trials and 0/100 on each of the truncated octahedron, truncated cuboctahedron and saved cyclic witness. A zero observed count is not a proof of zero probability.

COMPUTED. Editable installation was checked with `python -m pip install -e workings/barnette_lab --no-deps --no-build-isolation`. The nine standard-library unittest cases passed. The per-lemma campaign uses plain assertions, so do not run it with Python's `-O` option.
