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

`li.LiObjects` implements the literal half-ray involutions for c_min=1 using exact rational coordinates. `LiMultiObjects` implements Appendix B with sets of distinct intersections, following Definition 14. The finite range is recorded separately.

Integer polynomial coefficients use the constructive paper's epsilon sign. The original exponential sum is `i**(-n) * Z(exp(x))`. JSON includes all states but only a representative pair, and records the selected tree state separately. The cycle certificate lives in `certificate`.

All finite ranges and unchecked obligations are listed in the research folder's VERIFICATION.md.


For an arbitrary prescribed input edge:

```python
from barnette_lab import hamiltonian_cycle, named_graphs
g = named_graphs()['cube']
cycle = hamiltonian_cycle(g, next(iter(g.edges())))
```

The checked examples are in `examples/cube.json` and `examples/truncated_octahedron.json`. Their representative pair uses the exported tree matching as its second state.

Optional exhaustive small-graph campaign:

```powershell
python workings/barnette_lab/setup_plantri.py
python -m barnette_lab.verify --output research/2026-11-14_sol_route-constructive/data --max-dual-vertices 10 --plantri workings/barnette_lab/vendor/plantri.exe --plantri-max 14
python -m unittest discover -s workings/barnette_lab/tests -v
```

The setup script downloads a hash-pinned plantri 4.5 mirror and disables CPU timing for Windows compilation with GCC. The official 5.8 server timed out. Downloaded source and executables stay in ignored `vendor/`. The built-in generator needs neither GCC nor plantri. Algorithm experiments are reproducible with the commands in DATA.md.
