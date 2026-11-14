# Barnette lab

COMPUTED. Reference implementation of the three local papers. This is experimental verification, not a proof checker for arbitrary graphs.

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH='workings/barnette_lab'
python -m barnette_lab.verify --output research/2026-11-14_sol_route-constructive/data --max-dual-vertices 10
```

Dependencies are networkx and sympy. Optional installation is `python -m pip install -e workings/barnette_lab`.

`Instance.from_primal(g)` accepts a Barnette graph; `Instance(t)` accepts its Eulerian triangulation. `named_graphs()` supplies the cube, hexagonal prism, truncated octahedron and truncated cuboctahedron. `generated()` makes a non-exhaustive family of even prisms and octahedral connected sums, testing isomorphism and connectivity. Each instance retains a rotation system. Face and dual vertex IDs index `faces`; primal input vertex names are replaced by face IDs in the constructed dual-of-dual.

`states`, `pairs`, `Q`, `dcycles`, `J`, `delta`, `H`, `B`, `weights`, `polynomial`, `recover` expose the proof objects. `enumerate_tree` implements prefix pruning. `algorithms.marked_walk` implements the ordered-token involutions. `algorithms.solve` handles black-boundary separators recursively. `check_cycle` independently validates the resulting cycle against the constructed primal graph.

`li.LiObjects` implements the literal half-ray involutions for c_min=1 using exact rational coordinates. It does not implement Li's Appendix B for multiple marks. The verification output records this restricted coverage.

Integer polynomial coefficients use the constructive paper's epsilon sign. The original exponential sum is `i**(-n) * Z(exp(x))`. JSON includes all states but only a representative pair, and records the selected tree state separately. The cycle certificate lives in `certificate`.

All finite ranges and unchecked obligations are listed in the research folder's VERIFICATION.md.
