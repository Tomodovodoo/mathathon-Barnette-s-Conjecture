# 05. Put the height on white faces

A state is a matching in the black-centre incidence graph. Subtract a fixed reference matching. The resulting flow has zero divergence, so it is the boundary of an integer face potential. The labels show that potential on the bounded white spoke regions, with the exterior fixed at zero and the lattice minimum subtracted. They are heights of regions, not heights of triangulation vertices. A directed cycle reversal changes every enclosed label by one. Summing these labels gives the matching volume, up to the chosen normalization. The exponential weights read this same volume when all bounded face circulations are one. Thus the analytic exponent has a discrete interpretation. The referee corrected the original wording: paths or a reference state must be fixed before comparing heights. The build solves the boundary equations exactly over the integers for all twelve states.

Status: PROVED-HERE in the combinatorics referee with normalization corrections; independently AI-refereed, human review pending. COMPUTED exact heights on all 12 states.

Connects to: 2 exponents; 7 area; 13 clock lattice.

Sources: research/2026-11-14_astra_referee-combinatorics/REFEREE.md; build.py; computed.json.

COMPUTED figure provenance: build.py, computed.json, picture kind `height`.
