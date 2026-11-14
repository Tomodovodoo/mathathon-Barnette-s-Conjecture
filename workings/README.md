# workings

`barnette/` is a small Python package that carries out the proof of Barnette's
conjecture on a given graph: for a cubic, bipartite, 3-connected planar graph
`G` and an edge `e`, `hamiltonian_cycle(G, e)` returns a Hamiltonian cycle of
`G` that avoids `e`. It is meant to be read next to
[the paper](../paper/barnette.pdf) and uses its names and notation.

| Module | Section of the paper | Contents |
|---|---|---|
| `triangulation.py` | 2. States | the graph `G` or its rotation system, validation, the dual Eulerian triangulation `T` (Lemma 2.4), its face colouring, the face `t0`, the side `e0`, the roots, the sets `A` and `X` |
| `states.py` | 2. States | states, `Q_s`, good states, the set `M^*` and the Hamiltonian cycle `G - M` of a good state (Lemma 2.11, Proposition 2.12) |
| `pairs.py` | 3. Pairs of states, 4. The weighted count | pairs, the cycles of `D(r,s)` and of `Q_s` (Lemmas 4.2(1) and 3.4(1)), the two reversals, the sign `eps` (Lemmas 3.4(2) and 4.2(3)), the weight `omega` (Lemma 4.6), the signed sum (Lemma 3.5, Proposition 4.9) |
| `solve.py` | 5. Proof of the theorem | a pair by a flow (Proposition 5.5), the exchange walk and the search through the states of [the algorithm note](../proofs/algorithm/algorithm.md), cutting along a separating triangle and gluing (Theorem 5.6), `hamiltonian_cycle`, `is_hamiltonian_cycle` |
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
