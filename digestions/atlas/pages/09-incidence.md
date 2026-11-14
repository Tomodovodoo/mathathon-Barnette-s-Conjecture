# 09. Cancellation is a row dependence

Fix the cyclic second state from the running example. Each row of this matrix belongs to a bounded black face; its two possible nonzero entries belong to the endpoints of the opposite edge, after root columns are removed. The entries carry the local orientation sign. The vector below the matrix gives an exact nonzero dependence among its rows. It runs around the opposite-edge cycle. Consequently the determinant vanishes. Expanding that determinant chooses one endpoint per row and one occurrence of each nonroot column, precisely the possible mates of the fixed state, with the appropriate signs up to a global factor. The geometric cancellation involution is therefore visible in linear algebra. This reformulation explains why cyclic states vanish, but it does not by itself produce a nonzero determinant for some other state. That is still the positivity step.

Status: PROVED-HERE in the combinatorics referee, exact global-factor correction included. Independently AI-refereed; COMPUTED matrix and null vector here.

Connects to: 3 first involution; 10 global determinant; 14 matroids.

Sources: research/2026-11-14_astra_referee-combinatorics/REPORT.md; build.py; incidence.json.

COMPUTED figure provenance: build.py, computed.json, picture kind `matrix`.
