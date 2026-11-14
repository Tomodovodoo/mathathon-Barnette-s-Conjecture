"""Examples: a few cubic, bipartite, 3-connected planar graphs, and three
triangulations with a face t0 and a side e0."""
import json
from itertools import permutations
from pathlib import Path

import networkx as nx

from .triangulation import Triangulation


def cube():
    return nx.cubical_graph()


def prism(k):
    """The prism over a k-gon, k >= 4 even; the cube is prism(4)."""
    return nx.circular_ladder_graph(k)


def truncated_octahedron():
    """The permutations of 1234, adjacent when they differ by exchanging two
    neighbouring entries: 24 vertices, six squares and eight hexagons."""
    G = nx.Graph()
    for p in permutations(range(1, 5)):
        for i in range(3):
            q = list(p)
            q[i], q[i + 1] = q[i + 1], q[i]
            G.add_edge(p, tuple(q))
    return G


def nanotube(m):
    """A tube of m hexagonal rings closed by a vertex at each end: 6m + 2
    vertices, six squares, and hexagons otherwise.  nanotube(1) is the cube."""
    G = nx.Graph()
    for i in range(m):
        for j in range(6):
            G.add_edge((i, j), (i, (j + 1) % 6))
            if i + 1 < m and (i + j) % 2 == 0:
                G.add_edge((i, j), (i + 1, j))
    G.add_edges_from(('bottom', (0, j)) for j in (1, 3, 5))
    G.add_edges_from(('top', (m - 1, j)) for j in range(6) if (m - 1 + j) % 2 == 0)
    return G


def two_cubes():
    """Two cubes, each with one vertex removed, joined by three edges.  The
    three edges form a cut, and the dual triangulation (two octahedra glued
    along a face) has a separating triangle."""
    G = nx.Graph()
    for side in (0, 1):
        cube_ = nx.relabel_nodes(nx.cubical_graph(), lambda v: (side, v))
        G.update(cube_)
    G.remove_nodes_from([(0, 0), (1, 0)])
    G.add_edges_from(((0, v), (1, v)) for v in nx.cubical_graph()[0])
    return G


def running_example():
    """The example of Figure 3 of the paper: a triangulation with 13 vertices
    and 22 faces, with roots 0, 4, 5 and e0 = {0, 4}.  It has 12 states, two
    2-factors of H with two cycles each, hence 8 pairs, and 6 good states."""
    data = json.loads((Path(__file__).parent / 'running.json').read_text())
    return Triangulation(dict(enumerate(data['faces'])), data['t0'], data['e0'])


def eight_vertex_example():
    """The dual of the hexagonal prism with roots 0, 3, 4 and e0 = {0, 3};
    the example of proofs/algorithm/algorithm.md.

    Its black faces are 0 = {0,1,2}, 1 = {1,4,5}, 2 = {1,6,7}, 3 = {2,7,3},
    4 = {3,6,5} and t0.  It has three states; the one choosing the corners
    2, 5, 1, 7, 6 is not good, and it is the only state with the corner 1 in
    the face 2.
    """
    faces = [(0, 1, 2), (1, 4, 5), (1, 6, 7), (2, 7, 3), (3, 6, 5), (0, 3, 4),
             (0, 4, 1), (0, 2, 3), (1, 7, 2), (1, 5, 6), (3, 5, 4), (3, 7, 6)]
    return Triangulation(dict(enumerate(faces)), 5, (0, 3))


def trap():
    """A triangulation with 16 vertices, with roots 0, 1, 2 and e0 = {0, 1}.
    It has pairs whose second state is not good and from which no single
    reversal lowers the number of cycles of Q_s, and a 2-factor of H with one
    cycle neither of whose pairs has a good second state."""
    rows = {0: (1, 2, 3, 4, 5, 6, 7, 8), 1: (8, 9, 10, 11, 2), 2: (11, 12, 13, 3),
            3: (13, 4), 4: (13, 5), 5: (13, 14, 15, 6), 6: (15, 7), 7: (15, 14, 9, 8),
            8: (9,), 9: (14, 12, 10), 10: (12, 11), 11: (12,), 12: (14, 13), 13: (14,),
            14: (15,)}
    T = nx.Graph((v, w) for v, ws in rows.items() for w in ws)
    return Triangulation.from_graph(T, (0, 1, 2), (0, 1))
