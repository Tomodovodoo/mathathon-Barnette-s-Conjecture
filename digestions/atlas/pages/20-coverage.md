# 20. Two produced cycles, six missed cycles

Both panels show the same hexagonal prism, drawn as two hexagons with corresponding rungs. Purple edges form a Hamiltonian cycle in each panel. For the fixed root face and prescribed edge, recovery from the two tree matchings produces exactly two of the prism's eight Hamiltonian cycles. The left cycle is produced; the right cycle is absent from that image. Missing an image does not mean missing a Hamiltonian cycle of the graph. It means that this rooted state construction is not surjective. The build enumerates every primal perfect matching, tests which complements are connected, and compares their edge sets with every recovered cycle. This distinction matters when interpreting counts or proposing a uniform Hamiltonian-cycle sampler. A uniform sampler of tree matchings would sample only this rooted image, even if its self-reduction implementation were exact.

Status: COMPUTED all 8 prism cycles and both recovery images here. Injectivity and failure of surjectivity independently AI-refereed in sol_referee-structure/REFEREE-limits.md.

Connects to: 10 prism determinant; 19 recovery; 22 family counts.

Sources: research/2026-11-14_sol_referee-structure/REFEREE-limits.md; build.py; computed.json, hex_prism.

COMPUTED figure provenance: build.py, computed.json, picture kind `coverage`.
