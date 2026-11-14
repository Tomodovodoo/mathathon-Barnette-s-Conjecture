# Independent referee computations

Run from the repository root in PowerShell. Python, NetworkX and SymPy must be available. No project algorithm package or author verification module is imported. The existing plantri executable is used only as a graph generator. All writes stay in this folder. Run commands sequentially; each completed in under one minute in this session, with one heavy process at a time.

```powershell
python -B research/2026-11-14_sol_referee-covers/code/check.py families
python -B research/2026-11-14_sol_referee-covers/code/check.py certificates
python -B research/2026-11-14_sol_referee-covers/code/check.py witnesses
python -B research/2026-11-14_sol_referee-covers/code/check.py polynomials
python -B research/2026-11-14_sol_referee-covers/code/check.py family-polynomials
python -B research/2026-11-14_sol_referee-covers/code/check.py stacks
python -B research/2026-11-14_sol_referee-covers/code/check.py stack-source
python -B research/2026-11-14_sol_referee-covers/code/check.py census
python -B research/2026-11-14_sol_referee-covers/code/transfer.py
python -B research/2026-11-14_sol_referee-covers/code/provenance.py
```

Each `check.py MODE` writes `MODE.json` beside the script. `transfer.py` writes `rebuilt-transfers.json`, retaining all independently reconstructed matrices, initial and terminal vectors and boundary states. Initial runs omitted `-B`, before any local imports were present; subsequent commands use it to avoid bytecode writes. No author module was imported.

`families` independently builds the submitted T_m and tube adjacency rules. It checks T_m for m=2,...,8; prisms for m=2,...,7; width-four tubes at L=0,...,5 and width-six at L=0,...,3. Faces come from NetworkX's embedding, coloured by a separately constructed face dual. Incidence bijections are recursively enumerated. All ordered state pairs are tested for disjointness. Opposite-edge forests are checked directly for acyclicity and exactly one root per component. Hamiltonian cycles are enumerated as connected complements of every perfect matching of the cubic primal. The primal deletion identity is asserted on every enumerated cover.

`census` uses `plantri.exe -b -c4 V`, independently decodes its Windows planar-code stream, and tests every facial root through V=16. This gives 129 unrooted classes and 3,374 facial-root occurrences. Every weak-bound or multi-cover-strictness violation is counted; there were none. The final replay also asserts the exact two-cover overlap formula on every encountered two-cover root. Larger invariant counts were not replayed. The CRLF normalization is safe in this range, whose encoded labels are all below control-Z.

`witnesses` reads edge lists and root sets as input data only. It reconstructs the entire state and cover sets and the maximal simple-cycle reversal graph. Cover adjacency is checked through connected degree-two changed-corner graphs. Output cover ordering differs from the sources.

`polynomials` reads the two retained witness graph edge lists, chooses root face zero in the independent embedding, solves bounded white-face unit-circulation equations over the rationals and sets all free parameters to zero. Cyclic black-face order gives the sign, and explicit pair enumeration gives both exponential and incidence-linear polynomials. This independent gauge reproduces the reported off-circle exponential factor, but changes the linear factor. JSON retains weights and root sets. In each case the exponent shift is removed, but overall sign is not normalized.

`family-polynomials` performs the same computation for T_m through m=6. `stacks` generates a control prism chain with an explicit permutation distinct from the submission; its Hamiltonian counts deliberately differ. `stack-source` reads the submission's retained chain edge lists and roots, independently checks all quantities through q=5, independently enumerates all eight base-prism induced-tree partitions, and rebuilds their local simultaneous-avoidance tensor. No source count is used as an enumeration input.

`certificates` independently multiplies all eight submitted sparse matrices by their vectors and checks at least D scalar recurrence discrepancies for matrix dimension D. For pair polynomials this evaluates the cycle marker at one. It checks the submitted arithmetic, without using any `certified` Boolean or stored scalar sequence as evidence.

`transfer.py` goes further: it constructs its own black-face order and boundary keys from independently embedded tubes, builds stationary S,M,P matrices from local matching/forest invariants, and constructs H matrices by explicit monochromatic connectivity graph operations. It checks the submitted recurrences on these NEW matrices for at least D consecutive discrepancies. Translation equality of middle strip face lists is asserted. Cayley-Hamilton then certifies all lengths. Pair costs zero and one are propagated independently and their Boolean boundary vector is followed to exact repetition, proving c_min=1 for every L>=2. Prefix cases L=0,1 are directly enumerated. These independent matrices happen to have the same dimensions as the originals, but their state numbering and ordering are not imported.

The first certificate replay needed a parser correction because pair entries are polynomial dictionaries rather than scalar integers; only the corrected successful output is retained. This was a referee input-format error, not a failure of a submitted recurrence.

Limitations: the census shares plantri generation with the authors, not their invariant code. It does not constitute an independent proof of plantri completeness. No floating sampler, numerical spectrum, decimal asymptotic calculation, original author incidence gauge, or executable height-marked walk was replayed. The height-marked constructor was checked mathematically in the referee report.

`provenance.py` records hashes of reviewed source reports and JSON inputs and checks each census row's graph count, face multiplier, all-pair count, absence of reported overflows or violations, and equality-count agreement with the one-element-lattice count. Published e_4 values are transcribed explicitly from the opened primary table. It verifies the 23,824,742 total without claiming to rerun those larger invariant calculations.
