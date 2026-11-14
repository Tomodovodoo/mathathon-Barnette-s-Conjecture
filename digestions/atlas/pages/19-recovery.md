# 19. From a white tree to one Jordan curve

The bold edges P are the selected sides of the triangulation. Black disks and white squares mark their two components. The purple curve is the complementary dual cycle in G. Starting with the forest state, delete its spokes from the incidence graph to obtain a tree. The dual edges across those deleted spokes form the green white-face tree seen on page 16. Root it at the white face adjacent to the prescribed outer edge. Each oriented white-tree edge then selects a side of its black triangle; include the prescribed outer edge as well. The build checks that every triangle has exactly one selected side and that both components of P induce trees. Plane duality makes their interface a single Jordan curve. Following the interface visits each triangle once, so the curve is Hamiltonian in G.

Status: LIT: OpenAI Section 6 and constructive paper recovery criterion. COMPUTED P, inducedness, white tree and Hamiltonian cycle; independent laboratory recovery agrees.

Connects to: 16 white tree; 18 primal; 20 produced cycles; 24 Stein equivalence.

Sources: papers/OpenAI-Barnette.pdf, Section 6; papers/barnette_trees.pdf; build.py; computed.json.

COMPUTED figure provenance: build.py, computed.json, picture kind `recover`.
