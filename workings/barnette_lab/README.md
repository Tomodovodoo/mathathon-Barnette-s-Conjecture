# Barnette lab

COMPUTED. Reference implementation of the three local papers. This is experimental verification, not a proof checker for arbitrary graphs.

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH='workings/barnette_lab'
python -m barnette_lab.verify --output research/2026-11-14_sol_route-constructive/data --max-dual-vertices 10
```

Dependencies are networkx and sympy. Optional installation is `python -m pip install -e workings/barnette_lab`.

`Instance.from_primal(g)` accepts a Barnette graph; `Instance(t)` accepts its Eulerian triangulation. `named_graphs()` supplies the cube, hexagonal prism, truncated octahedron and truncated cuboctahedron. `generated()` makes a non-exhaustive family of even prisms and octahedral connected sums, testing isomorphism and connectivity. Each instance retains a rotation system. Face and dual vertex IDs index `faces`; the certificate also includes original primal labels when constructed by `from_primal`.

`states`, `pairs`, `Q`, `dcycles`, `J`, `delta`, `H`, `B`, `weights`, `polynomial`, `recover` expose the proof objects. `enumerate_tree` implements prefix pruning. `algorithms.marked_walk` implements the ordered-token involutions. `algorithms.solve` handles black-boundary separators recursively. `check_cycle` independently validates the resulting cycle against the constructed primal graph.

`li.LiObjects` implements the literal half-ray involutions for m=1 using exact rational coordinates. `LiMultiObjects` implements Appendix B with sets of distinct intersections, following Definition 14. The finite range is recorded separately.

Integer polynomial coefficients use the constructive paper's epsilon sign. The original exponential sum is `i**(-n) * Z(exp(x))`. JSON includes all states but only a representative pair, and records the selected tree state separately. The cycle certificate lives in `certificate`.

All finite ranges and unchecked obligations are listed in the research folder's VERIFICATION.md.


For an arbitrary prescribed input edge:

```python
from barnette_lab import hamiltonian_cycle, named_graphs
g = named_graphs()['cube']
cycle = hamiltonian_cycle(g, next(iter(g.edges())))
```

The checked examples are in `examples/cube.json` and `examples/truncated_octahedron.json`. Their representative pair uses the exported good state as its second state.

Optional exhaustive small-graph campaign:

```powershell
python workings/barnette_lab/setup_plantri.py
python -m barnette_lab.verify --output research/2026-11-14_sol_route-constructive/data --max-dual-vertices 10 --plantri workings/barnette_lab/vendor/plantri.exe --plantri-max 14
python -m unittest discover -s workings/barnette_lab/tests -v
```

The setup script downloads a hash-pinned plantri 4.5 mirror and disables CPU timing for Windows compilation with GCC. The official 5.8 server timed out. Downloaded source and executables stay in ignored `vendor/`. The built-in generator needs neither GCC nor plantri. Algorithm experiments are reproducible with the commands in DATA.md.


## Counted regression tiers

COMPUTED. Run either command from the repository root. The entry point runs all 14 unit tests and then the counted campaign. It needs networkx, sympy, the repository research inputs and the plantri binary built by the setup command above.

```powershell
python -B workings/barnette_lab/run_tests.py quick
python -B workings/barnette_lab/run_tests.py full
```

To retain per-instance evidence, append `--output research/2026-11-14_sol_lab-tests`. The recorded commands use this option. Both tiers use fixed sampler seeds and exchange-walk seeds. Counters and mathematical outputs are deterministic; wall-clock seconds are not. Failures raise exceptions and return a nonzero process exit code. New obligations remain active with `-O`, though normal Python is required to retain assertions inside the legacy verifier and imported referees.

COMPUTED. Quick includes every facial root of every plantri Eulerian triangulation through order 10, the running example, the order-16 minimal-cover obstruction, the order-18 lattice witness, and a property-selected order-12 instance with minimum cover count three. Full includes every facial root through order 14 and those three larger fixtures. Every face is tried, so both choices of black colour occur. These are rooted occurrences, not distinct rooted isomorphism classes. Property counters explicitly record paired roots, partnered cyclic Q states, both separator boundary colours, minimum counts 1, 2, 3 and a minimal cover without a good pair. A missing required property fails the campaign.

COMPUTED. Every simple directed state cycle is enumerated in the graph of all permitted outgoing edges for each state; the disk table deduplicates cycles by their undirected edge sets within each instance. Pair-level checks cover every pair. Independent `etri.py` comparisons cover every census root through order 12, with an explicit face-set relabelling and one global orientation alignment. The referee is imported from its own research folder, never copied or modified.

COMPUTED. Li comparisons use the second involution referee's `fp.py` with the lab's exact rational coordinates and rays on all paired roots through order 12 and all larger fixtures. Both object sets and both maps agree exactly; signs may have one global orientation factor. Saved outputs from both involution referees supply independent checks of the small-census second-fixed counts and the running example. Different drawings legitimately have different object totals. Ordered incidence-token walks and distinct-intersection walks are separate constructions. Their move counts are not compared. The ordered walk and exchange walk are run from every pair with explicit caps, and their endpoints are checked with the independent Q-cycle detector. Single ordered marks are exhaustive; multiple ordered marks use the first 24 one-per-cycle rank combinations per pair. The legacy restart fixture checks the four-to-two-cycle restart.

COMPUTED. The region tests exhaust all connected induced subsets with at least three vertices at orders through eight, and at the first root of every order-nine and order-ten graph. At the remaining roots/orders they test all connected triples, all connected vertex prefixes of size at least four, and all connected complements of a vertex. They check the exact Euler identity, signed boundary balance, bound 3.3 on every tested region with boundary length at least four, and bound 3.4 on separator-free instances. These subset ranges are deliberately explicit. The tests do not establish the inequalities for all larger subsets.

COMPUTED. Recovery has a left inverse at every good state and each of the three root prescriptions, proving injectivity within the tested sets. Reverse-image tests enumerate every avoiding Hamiltonian cycle through order eight. Above order eight they use two-induced-tree cuts from the first 32 bit masks, prefixes and an alternating mask. The exact image criterion is checked on every resulting cycle, including missed cycles. The finite-difference first coefficient is compared to the full minimum-cover white-area product sum. Relative heights and lowest signed moments agree for BFS and DFS face paths. Absolute heights may differ by state-independent constants.

COMPUTED. Sampling tests check exact conditional determinant probabilities on every state of the cube and hexagonal prism, then use 1,800 fixed-seed samples of each. The chi-square cutoffs are stated in the JSON evidence. The two-matroid regression enumerates all six prism common bases and verifies that four are not states.

In the coverage table, instances counts runs with at least one exercised object. Vacuous counts eligible runs with zero exercised objects. Checks restricted to a range, such as independent comparison through order 12, do not count ineligible larger inputs as vacuous. Property rows count occurrences only. A vacuous count is reported rather than hidden, and each main check must have a nonzero total. This remains finite computation, not a proof certificate for arbitrary inputs.

<!-- LAB-COVERAGE -->
