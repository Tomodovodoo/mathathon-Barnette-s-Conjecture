# 15. The natural relaxation has a fractional vertex

Use one variable for each available nonroot corner. The two partition equations require total weight one at each face and each nonroot vertex. For every vertex subset after root identification, a graphic inequality bounds the total weight of opposite edges contained in that subset by its size minus one. Integral feasible points are the desired tree matchings. The picture shows the fractional vertex found on the running example by a fixed-seed search over linear objectives. Solid wedges have weight one, outlined wedges weight one half, and missing wedges weight zero. These are fractional corner weights, not a state or a disjoint pair. The build checks every graphic subset inequality and verifies that the active constraints have full rank. Thus the point is a vertex rather than a convex combination accidentally returned by a solver. This blocks a direct integrality claim for the relaxation.

Status: COMPUTED here with all subset inequalities and full active-rank certificate; exact half values. General relaxation obstruction independently AI-refereed in the structure report.

Connects to: 14 three matroids; 26 algorithmic open doors.

Sources: research/2026-11-14_sol_referee-structure/REFEREE-graph-theory.md; build.py; computed.json, lp.

COMPUTED figure provenance: build.py, computed.json, picture kind `lp`.
