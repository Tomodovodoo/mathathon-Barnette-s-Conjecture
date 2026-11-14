# Instances

The examples cited in [OPEN-PROBLEMS.md](../OPEN-PROBLEMS.md), in [routes.md](../../digestions/routes.md) and in [the algorithm note](../../proofs/algorithm/algorithm.md), one JSON object per file, in the notation of [the paper](../../paper/barnette.pdf). $H^+$ is the graph on the black faces and the vertices of $T$ in which a face is adjacent to its corners.

| Key | Meaning |
| --- | --- |
| `V`, `edges` | the number of vertices of $T$, numbered from 0, and its $3V-6$ edges |
| `t0` | the three roots, the corners of the black face $t_0$ |
| `about` | what the example shows |
| `black_faces` | the faces in $A$; every state, and `unused`, lists one corner for each of them in this order |
| `unused` | a 2-factor of $H$, given by the corner of each face that it leaves out |
| `rotation` | the neighbours of each vertex in cyclic order |
| `faces` | all faces of $T$, each with its corners in counterclockwise order; the faces in $A$ are taken in this order |
| `pair` | a pair $(r,s)$ |

A triangulation is loaded with `Triangulation.from_graph(networkx.Graph(edges), t0, t0[:2])` from [workings](../../workings/README.md). The edges determine the drawing of $T$ only up to reflection, and `from_graph` returns one of the two mirror images. States, pairs and the cycles of $Q_s$ are the same in both.

## The trap chains

The number of moves of the exchange walk is not the same in both mirror images, and it depends on the order of the faces. The files `trap-chain-1` to `trap-chain-10` therefore list `faces`. From `workings/`:

```python
import json
from barnette import Triangulation, exchange_walk

d = json.load(open('../research/instances/trap-chain-4.json'))
T = Triangulation(dict(enumerate(d['faces'])), d['faces'].index(d['t0']), d['t0'][:2])
r, s = (dict(zip(T.A, state)) for state in d['pair'])
print(exchange_walk(T, r, s)[1])                    # 113

M = Triangulation({t: f[::-1] for t, f in T.faces.items()}, T.t0, T.e0)
print(exchange_walk(M, r, s)[1])                    # 3
```

`T` is the triangulation as stored and `M` its mirror image, with the same faces in the same order. For $k=1,\dots,10$ the first number is

```
0, 3, 24, 113, 562, 2811, 14060, 70309, 351558, 1757807
```

and the second is 3. The walk for $k=8$ takes about ten seconds, for $k=9$ under a minute and for $k=10$ about three minutes. Loaded with `from_graph` from `edges`, under networkx 3.6.1, the same triangulations come out as the mirror image with the faces in another order, and the walk from `first_pair` takes 5 moves for $k=1$ and 15 for $k=2,\dots,10$.
