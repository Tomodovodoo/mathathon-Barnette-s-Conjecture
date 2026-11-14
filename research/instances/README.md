# Instances

The examples cited in [OPEN-PROBLEMS.md](../OPEN-PROBLEMS.md) and in [routes.md](../../digestions/routes.md), one JSON object per file, in the notation of [the paper](../../paper/barnette.pdf).

| Key | Meaning |
| --- | --- |
| `V`, `edges` | the number of vertices of $T$, numbered from 0, and its $3V-6$ edges |
| `t0` | the three roots, the corners of the black face $t_0$ |
| `about` | what the example shows |
| `black_faces` | the faces in $A$; every state, and `unused`, lists one corner for each of them in this order |
| `unused` | a 2-factor of $H$, given by the corner of each face that it leaves out |
| `rotation` | the neighbours of each vertex in cyclic order |

A triangulation is loaded with `Triangulation.from_graph(networkx.Graph(edges), t0, t0[:2])` from [workings](../../workings/README.md).
