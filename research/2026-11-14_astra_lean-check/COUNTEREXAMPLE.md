# Explicit counterexample to TODO T5

REFUTED, with COMPUTED enumeration in numerical.py/numerical.json and the following direct verification, PROVED-HERE.

Take the hexagonal bipyramid T. Its equator is 0,1,2,3,4,5 and its apices are 6,7. Its oriented upper faces are U_i=(6,i,i+1), its lower faces L_i=(7,i+1,i), with equatorial indices modulo 6. Colour U_0,U_2,U_4,L_1,L_3,L_5 black. Root at U_0, with roots 6,0,1, and prescribe side e0={0,1}. Its dual G is the hexagonal prism. Label U_i by i and L_i by 6+i.

Choose the selection P with dual sides {0,1}, {1,2}, {2,3}, {4,6}, {0,5}, {4,7}. Each face contains exactly one selected side, so its primal dual edges form a perfect matching. The complement is the explicit Hamiltonian cycle

    0 -> 5 -> 4 -> 10 -> 11 -> 6 -> 7 -> 8 -> 9 -> 3 -> 2 -> 1 -> 0.

It avoids the edge across e0 because e0 belongs to the matching. Thus P satisfies the premise of T5. Direct inspection of the two hexagons joined by their six spokes, or the deletion check in numerical.py, verifies cubicity, bipartiteness and three-vertex-connectivity. The usual prism embedding gives planarity.

Remove e0 from the selected dual forest and orient its edges towards roots 6,0,1. On the five nonroot black faces U_2,U_4,L_1,L_3,L_5, the tails give the recovered state

    s=(3,4,2,7,5).

These are precisely the five nonroot vertices, each once. Its opposite edges are {6,2}, {6,5}, {7,1}, {4,3}, {7,0}. The three components are {6,2,5}, {7,1,0}, and {4,3}. They contain respectively one, two, and zero roots. Q_s is acyclic but s is not good.

No other good state can recover P. If a good state recovered P, orienting its selected forest minus e0 towards the roots would recover that state, uniquely, since each rooted tree has a unique orientation towards its root. This same operation gives the non-good s above. Hence the universal claim in T5 is false. The conditional image characterisation in the current paper is consistent with this example.
