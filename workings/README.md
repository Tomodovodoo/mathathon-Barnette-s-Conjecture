# workings

`barnette/` is a small Python package that carries out the 2026 proof of
Barnette's conjecture on a given graph: for a cubic, bipartite, 3-connected
planar graph `G` and an edge `e`, `hamiltonian_cycle(G, e)` returns a
Hamiltonian cycle of `G` that avoids `e`. It is meant to be read next to the
paper (`paper/main/barnette.pdf`) and uses its names and notation.

| Module | Section of the paper | Contents |
|---|---|---|
| `triangulation.py` | The dual triangulation and the target | input graph or rotation system, validation, the dual triangulation `T`, its face colouring, the root face `t0`, the side `e0`, the sets `A` and `X` |
| `states.py` | Corner choices and the tree of faces | states, `Q_s`, good states, the selection `P_s` of a good state, the Hamiltonian cycle of a selection |
| `pairs.py` | Pairs of states | pairs, the cycles of `D(r,s)` and of `Q_s`, the two reversals, the sign `eps`, the weight `omega`, the signed sum |
| `solve.py` | The first pair; Separating triangles | the first pair by a flow, the exchange walk and the enumeration of `proofs/algorithm/algorithm.md`, cutting along a separating triangle and gluing, `hamiltonian_cycle`, `is_hamiltonian_cycle` |
| `examples.py` | | cube, prisms, truncated octahedron, a nanotube family, two glued cubes, the running example of the paper, the 8-vertex example and the 16-vertex trap of the algorithm note |

A state is a dict `{t: s(t)}` from the black faces in `A` to their chosen
corners, a pair is two such dicts, and a cycle of `D` or `Q_s` is the list of
faces that supply its edges. The faces of `T` are labelled by the vertices of
`G`, so a Hamiltonian cycle is a list of faces.

It needs Python 3 with `networkx`, and `pytest` for the tests. From this directory:

```
python -m barnette          # the cube and the running example, step by step
python -m pytest barnette   # the tests, a few seconds
```

```python
import networkx as nx
from barnette import hamiltonian_cycle
G = nx.circular_ladder_graph(6)          # the hexagonal prism
print(hamiltonian_cycle(G, (0, 1)))
```
