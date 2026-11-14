# 14. Three constraints, not two

A corner choice selects an opposite edge. Three conditions must hold together: choose one corner in each black face, choose every nonroot vertex once, and keep the opposite edges acyclic after identifying the roots. The first two are partition constraints; the last is a graphic constraint. Dropping the vertex constraint gives the illustrated hexagonal-prism witness. It has one choice per face and a rooted opposite-edge forest, but repeats a nonroot vertex and misses another. Our enumeration finds four such false common bases among the six choices satisfying the other two constraints. This is why an ordinary two-matroid intersection algorithm does not solve the problem. Dropping the graphic condition instead admits the cyclic state already seen on the running example. The forest is a genuine extra condition, and the signed cancellation is what enforces it.

Status: PROVED-HERE three-matroid description independently AI-refereed. COMPUTED all 6 two-constraint prism bases here, 4 nonstates. No polynomial-time algorithm follows.

Connects to: 9 incidence determinant; 15 fractional LP; 23 failed canonical choices.

Sources: research/2026-11-14_sol_referee-structure/REFEREE-graph-theory.md; research/2026-11-14_fable_referee-determinants/REPORT.md; computed.json.

COMPUTED figure provenance: build.py, computed.json, picture kind `matroids`.
