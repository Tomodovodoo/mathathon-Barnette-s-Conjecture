# Reproduction

Run from E:/Personal/Math/mathathon/barnette-s-conjecture in PowerShell. Python 3.14 with networkx, sympy, numpy and scipy was used. The repository's existing plantri executable is read only. Each command is a separate, sequential run.

```powershell
python research/2026-11-14_sol_route-probabilistic/code/explore.py
python research/2026-11-14_sol_route-probabilistic/code/campaign.py scan
python research/2026-11-14_sol_route-probabilistic/code/secondary.py
python research/2026-11-14_sol_route-probabilistic/code/half16.py
python research/2026-11-14_sol_route-probabilistic/code/campaign.py random
python research/2026-11-14_sol_route-probabilistic/code/mixing.py
python research/2026-11-14_sol_route-probabilistic/code/packing.py
python research/2026-11-14_sol_route-probabilistic/code/build_map.py
python -X utf8 research/2026-11-14_sol_route-probabilistic/labyrinth/lab.py check
python -X utf8 research/2026-11-14_sol_route-probabilistic/labyrinth/lab.py build
```

explore.py imports the lab and the counting-family constructors read only. campaign.py also imports the counting-family partner enumerator read only. Other scripts import explore.py, which sets those import paths. No external implementation is modified.

All computational claims are T4, unreviewed. Exact matrices and polynomials use SymPy integers. Sampling, LP, spectra and hitting-time systems use floating arithmetic. Positive packing certificates are independently checked inside the author script as two MultiGraph trees, but this is not an independent referee.

All main runs have a 530-second wall check at loop boundaries. The tiny secondary scan and cube subset enumeration finish in seconds. A future size increase should add finer checks before launching it. Run serially. The largest observed run was about 47 seconds. Do not infer a larger compute budget from the current small runs.
