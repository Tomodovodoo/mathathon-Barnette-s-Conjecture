"""The plane graph G, its validation, and the dual Eulerian triangulation T
(Section 2 of the paper, Lemma 2.4).

G is a cubic, bipartite, 3-connected planar graph.  Its dual T is a simple
triangulation of the sphere with all degrees even, so the faces of T can be
coloured black and white with different colours across every edge.  The faces
of T are the vertices of G, and that is how they are labelled here.
"""
import networkx as nx


def edge(u, v):
    """The undirected edge uv of T, as a sorted pair."""
    return (u, v) if u <= v else (v, u)


class Triangulation:
    """An Eulerian triangulation T with a black face t0 and a side e0 of t0.

    `faces` maps a label to a triple of vertices.  All triples are listed with
    the same orientation, called counterclockwise: every directed edge lies in
    exactly one triple, and `left[v, w]` is the face on the left of v -> w.
    The colouring is the one in which t0 is black.

    Attributes, in the notation of the paper:
      roots   the three corners of t0
      A       the black faces other than t0
      X       the vertices other than the roots;  |A| = |X| = n
      black, white   the two colour classes of faces
    """

    def __init__(self, faces, t0, e0):
        self.faces = {t: tuple(f) for t, f in faces.items()}
        self.t0, self.e0 = t0, edge(*e0)
        self.left = {}
        for t, (a, b, c) in self.faces.items():
            for d in ((a, b), (b, c), (c, a)):
                if d in self.left:
                    raise ValueError('the faces are not consistently oriented')
                self.left[d] = t
        if any((w, v) not in self.left for v, w in self.left):
            raise ValueError('some edge has only one face')
        self.vertices = sorted({v for f in self.faces.values() for v in f})
        degree = dict.fromkeys(self.vertices, 0)
        for v, _ in self.left:
            degree[v] += 1
        if len(self.vertices) - len(self.left) // 2 + len(self.faces) != 2:
            raise ValueError('the faces do not form a sphere')
        if len(self.vertices) < 4 or any(d % 2 for d in degree.values()):
            raise ValueError('expected a triangulation with all degrees even')
        if not set(self.e0) <= set(self.faces[t0]):
            raise ValueError('e0 is not a side of t0')

        # Two-colour the faces, starting from t0 (black).
        colour, queue = {t0: True}, [t0]
        for t in queue:
            for y in self.neighbours(t):
                if y not in colour:
                    colour[y] = not colour[t]
                    queue.append(y)
                elif colour[y] == colour[t]:
                    raise ValueError('the faces are not two-colourable')
        if len(colour) != len(self.faces):
            raise ValueError('the triangulation is not connected')
        self.black = {t for t in self.faces if colour[t]}
        self.white = set(self.faces) - self.black
        self.roots = self.faces[t0]
        self.A = [t for t in self.faces if t in self.black and t != t0]
        self.X = [v for v in self.vertices if v not in self.roots]
        self.n = len(self.A)
        self.index = {t: i for i, t in enumerate(self.A)}

    def sides(self, t):
        """The three sides of the face t, directed counterclockwise."""
        a, b, c = self.faces[t]
        return [(a, b), (b, c), (c, a)]

    def neighbours(self, t):
        """The three faces that share a side with t."""
        return [self.left[w, v] for v, w in self.sides(t)]

    def opposite(self, t, v):
        """The side of t opposite its corner v."""
        return edge(*(w for w in self.faces[t] if w != v))

    def third(self, t, v, w):
        """The corner of t other than v and w."""
        return next(u for u in self.faces[t] if u != v and u != w)

    def edges(self):
        """All edges of T."""
        return {edge(v, w) for v, w in self.left}

    def primal(self):
        """The cubic graph G: faces of T, adjacent when they share a side."""
        return nx.Graph((self.left[v, w], self.left[w, v]) for v, w in self.left)

    @classmethod
    def from_graph(cls, T, t0, e0):
        """Build from a 3-connected planar triangulation given as a graph.

        t0 lists the three roots, the corners of the face t0; faces are
        numbered 0, 1, ...
        """
        triples = _faces(embedding(T))
        if any(len(f) != 3 for f in triples):
            raise ValueError('expected a triangulation')
        root = next(i for i, f in enumerate(triples) if set(f) == set(t0))
        return cls(dict(enumerate(triples)), root, e0)


def embedding(G, rotation=None):
    """A planar embedding of G.

    `rotation` may give the embedding as a rotation system: for every vertex
    the list of its neighbours in clockwise order.  Without it the embedding
    is computed; for a 3-connected graph it is unique up to reflection.
    """
    if rotation is None:
        planar, emb = nx.check_planarity(G)
        if not planar:
            raise ValueError('the graph is not planar')
        return emb
    emb = nx.PlanarEmbedding()
    emb.set_data(rotation)
    try:
        emb.check_structure()
    except nx.NetworkXException as error:
        raise ValueError('the rotation system is not a planar embedding') from error
    if {frozenset(e) for e in emb.edges()} != {frozenset(e) for e in G.edges()}:
        raise ValueError('the rotation system does not describe the graph')
    return emb


def _faces(emb):
    """The faces of an embedding, each as the cyclic list of its vertices."""
    seen, faces = set(), []
    for v, w in emb.edges():
        if (v, w) not in seen:
            faces.append(tuple(emb.traverse_face(v, w, seen)))
    return faces


def validate(G, rotation=None):
    """Check that G is cubic, bipartite, planar and 3-connected.

    Returns a planar embedding of G, and raises ValueError otherwise.
    """
    if G.is_directed() or G.is_multigraph() or nx.number_of_selfloops(G):
        raise ValueError('expected a simple undirected graph')
    if len(G) < 4 or any(d != 3 for _, d in G.degree()):
        raise ValueError('the graph is not cubic')
    if not nx.is_bipartite(G):
        raise ValueError('the graph is not bipartite')
    emb = embedding(G, rotation)
    if nx.node_connectivity(G) < 3:
        raise ValueError('the graph is not 3-connected')
    return emb


def dual_triangulation(G, e, rotation=None):
    """The dual triangulation of G, with t0 and e0 chosen for the edge e = vw.

    The vertices of T are the faces of G, numbered 0, 1, ...; the face of T
    dual to a vertex x of G is labelled x and has the three faces of G at x as
    corners.  The face t0 is v, and e0 is the edge of T dual to e.
    """
    v, w = e
    if not G.has_edge(v, w):
        raise ValueError('e is not an edge of the graph')
    emb = validate(G, rotation)
    face_left = {}
    for i, f in enumerate(_faces(emb)):
        for d in zip(f, f[1:] + f[:1]):
            face_left[d] = i
    faces = {x: tuple(face_left[x, y] for y in emb.neighbors_cw_order(x)) for x in G}
    return Triangulation(faces, v, (face_left[v, w], face_left[w, v]))
