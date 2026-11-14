# 12. Forget orientations, keep the pair lattice

Each node represents one incidence two-factor, not one ordered pair. The unused corner in every black triangle determines an orientation of the full spoke graph with prescribed outdegrees. Subtracting two such orientations gives integer face potentials, and their componentwise order gives the displayed Hasse diagram. The build enumerates all eight ordered pairs and quotients them into these nodes. A green square means at least one ordered orientation at that node has a forest second state. A ring marks a minimum or maximum. The distinction matters: reversing D-cycles stays inside one node, whereas a lattice move can change the unused corners. The structural referee verified the alpha-orientation correspondence. Large counterexamples refute either specified extreme as a universal choice. A disjunction saying that one of the two extremes always works remains a separate question, not a consequence of distributivity.

Status: PROVED-HERE correspondence independently AI-refereed. COMPUTED complete running-example Hasse diagram. REFUTED individual extreme guarantees; joint-extremes conjecture remains open in the reviewed sources.

Connects to: 13 state lattice; 23 canonical choices; 26 open doors.

Sources: research/2026-11-14_sol_referee-structure/REFEREE-graph-theory.md; INTEGRATION.md; build.py; computed.json.

COMPUTED figure provenance: build.py, computed.json, picture kind `alpha`.
