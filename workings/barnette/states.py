"""States, good states, and the Hamiltonian cycle of a good state
(Section 3 of the paper, Proposition 3.5).

A state s chooses a corner s(t) in X of every black face t in A, using every
vertex of X once.  It is stored as a dict {t: s(t)}.
"""
from .triangulation import edge


def opposite_sides(T, s):
    """The edge set Q_s: for every t in A the side of t opposite s(t)."""
    return [T.opposite(t, s[t]) for t in T.A]


class _RootedForest:
    """Union-find on the vertices of T with the three roots identified.

    Edges added without closing a cycle here form a forest in T in which no
    component contains two roots.
    """

    def __init__(self, T):
        self.parent = {v: v for v in T.vertices}
        for v in T.roots:
            self.parent[v] = T.roots[0]

    def copy(self):
        other = object.__new__(_RootedForest)
        other.parent = dict(self.parent)
        return other

    def find(self, v):
        while self.parent[v] != v:
            v = self.parent[v]
        return v

    def add(self, v, w):
        """Add the edge vw; return False if it closes a cycle."""
        v, w = self.find(v), self.find(w)
        if v != w:
            self.parent[v] = w
        return v != w


def is_good(T, s):
    """Whether s is good: Q_s is a forest whose three components each contain
    one root.

    Q_s has n edges on n + 3 vertices, so this holds exactly when Q_s stays
    acyclic after the three roots are identified.
    """
    forest = _RootedForest(T)
    return all(forest.add(*q) for q in opposite_sides(T, s))


def _completable(faces, options):
    """Whether the faces can be matched to distinct corners from `options`."""
    owner = {}

    def augment(t, seen):
        for v in options(t):
            if v not in seen:
                seen.add(v)
                if v not in owner or augment(owner[v], seen):
                    owner[v] = t
                    return True
        return False

    return all(augment(t, set()) for t in faces)


def states(T, avoid=None, good=False):
    """Generate the states of T by choosing corners face by face.

    A partial choice is extended only if it can be completed to a state, so
    the number of partial choices visited is at most n + 1 times the number
    of states, and the memory used is polynomial.

    avoid   a state r: generate only the states s with s(t) != r(t) for all t,
            that is, the second states of the pairs (r, s).
    good    generate only the good states; a partial choice is then dropped
            as soon as its opposite sides close a cycle or join two roots.
    """
    roots, s, used = set(T.roots), {}, set()

    def options(t):
        return [v for v in T.faces[t]
                if v not in roots and v not in used and (avoid is None or avoid[t] != v)]

    def extend(i, forest):
        if i == T.n:
            yield dict(s)
            return
        t = T.A[i]
        for v in options(t):
            grown = forest
            if good:
                grown = forest.copy()
                if not grown.add(*T.opposite(t, v)):
                    continue
            s[t] = v
            used.add(v)
            if _completable(T.A[i + 1:], options):
                yield from extend(i + 1, grown)
            del s[t]
            used.remove(v)

    if _completable(T.A, options):
        yield from extend(0, _RootedForest(T))


def incidence_matrix(T):
    """The n x n matrix with entry 1 where the face t in A has the corner x in X.

    States are the nonzero terms of its determinant; they all have the same
    sign, by the disk identity (Lemma 5.1), so the number of states is the
    absolute value of the determinant.
    """
    return [[int(x in T.faces[t]) for x in T.X] for t in T.A]


def selection(T, s):
    """The edge set P = M^* of a good state s (Lemma 3.4): one side of
    every face of T, without cycles (Proposition 3.5).

    Colour the vertices of T with two colours so that the ends of every edge
    of the spanning tree S_s (Q_s and the two sides of t0 other than e0) have
    different colours.  P consists of the edges of T whose ends have the same
    colour; it contains e0 and, in every t in A, a side with end s(t).
    """
    if not is_good(T, s):
        raise ValueError('the state is not good')
    tree = set(opposite_sides(T, s)) | {edge(v, w) for v, w in T.sides(T.t0)}
    tree.discard(T.e0)
    nbrs = {v: [] for v in T.vertices}
    for v, w in tree:
        nbrs[v].append(w)
        nbrs[w].append(v)
    colour, queue = {T.roots[0]: 0}, [T.roots[0]]
    for v in queue:
        for w in nbrs[v]:
            if w not in colour:
                colour[w] = 1 - colour[v]
                queue.append(w)
    return {(v, w) for v, w in T.edges() if colour[v] == colour[w]}


def is_selection(T, P):
    """Whether P contains exactly one side of every face of T, that is,
    whether P = M^* for a perfect matching M of G."""
    return all(sum(edge(v, w) in P for v, w in T.sides(t)) == 1 for t in T.faces)


def cycle_of_selection(T, P):
    """The Hamiltonian cycle G - M for P = M^*: it crosses exactly the edges
    of T not in P.

    P must be acyclic and contain one side of every face.  Every face of T
    then has two sides not in P, and following them from face to face visits
    every face once.  The cycle is returned as a list of faces of T, that is,
    of vertices of G.
    """
    start = T.t0
    cycle, previous = [start], None
    while True:
        t = cycle[-1]
        step = [T.left[w, v] for v, w in T.sides(t) if edge(v, w) not in P]
        if len(step) != 2:
            raise ValueError('P is not a selection')
        following = step[1] if step[0] == previous else step[0]
        if following == start:
            break
        if len(cycle) > len(T.faces):
            raise ValueError('P is not acyclic')
        cycle.append(following)
        previous = t
    if len(cycle) != len(T.faces):
        raise ValueError('P is not acyclic')
    return cycle
