# workings

`barnette/` is a small Python package that carries out the proof of Barnette's
conjecture on a given graph: for a cubic, bipartite, 3-connected planar graph
`G` and an edge `e`, `hamiltonian_cycle(G, e)` returns a Hamiltonian cycle of
`G` that avoids `e`. It is meant to be read next to
[the paper](../paper/barnette.pdf) and uses its names and notation.

| Module | Section of the paper | Contents |
|---|---|---|
| `triangulation.py` | 2. The dual triangulation, 3. Good states | the graph `G` or its rotation system, validation, the dual Eulerian triangulation `T` (Lemma 2.4), its face colouring, the face `t0`, the side `e0`, the roots, the sets `A` and `X` (Setup 3.1) |
| `states.py` | 3. Good states | states, `Q_s`, good states, the set `M^*` and the Hamiltonian cycle `G - M` of a good state (Lemma 3.4, Proposition 3.5) |
| `pairs.py` | 4. Pairs of states, 5. The cancellation, 6. The weighted count | pairs, the cycles of `D(r,s)` and of `Q_s` (Lemmas 6.2(1) and 5.5(1)), the two reversals, the sign `eps` (Lemmas 5.5(2) and 6.2(3)), the weight `omega` (Lemma 6.6), the signed sum (Lemma 5.6, Proposition 6.9) |
| `solve.py` | 2. The dual triangulation, 4. Pairs of states | a pair by a flow (Proposition 4.6), the exchange walk and the search through the states of [the algorithm note](../proofs/algorithm/algorithm.md), cutting along a separating triangle and gluing (Proposition 2.7), `hamiltonian_cycle`, `is_hamiltonian_cycle` |
| `examples.py` | | cube, prisms, truncated octahedron, a family of tubes, two glued cubes, the example of Figure 2, the example with 8 vertices and the example with 16 vertices of the algorithm note |

A state is a dict `{t: s(t)}` from the black faces in `A` to their chosen
corners, a pair is two such dicts, and a cycle of `D(r,s)` or `Q_s` is the
list of faces that supply its edges. The faces of `T` are labelled by the
vertices of `G`, so a Hamiltonian cycle is a list of faces. The functions
`selection`, `is_selection`, `cycle_of_selection` and `acyclic_selection`
deal with the set `M^*` of the paper, which contains one side of every face.

The package needs Python 3 with `networkx`, and `pytest` for the tests
(`pip install -r ../requirements.txt`). From this directory:

```
python -m barnette          # the cube and the example of Figure 2, step by step
python -m pytest barnette   # the tests, a few seconds
```

```python
import networkx as nx
from barnette import hamiltonian_cycle
G = nx.circular_ladder_graph(6)          # the hexagonal prism
print(hamiltonian_cycle(G, (0, 1)))
```
