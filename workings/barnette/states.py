"""States, good states, and the Hamiltonian cycle of a good state.

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
    """Whether Q_s is a forest in which each component contains one root.

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
    sign, so the number of states is the absolute value of the determinant.
    """
    return [[int(x in T.faces[t]) for x in T.X] for t in T.A]


def selection(T, s):
    """The selection P_s of a good state s: one side of every face of T.

    P_s contains e0 and, in every t in A, a side at the corner s(t).  The
    faces of T, joined across the edges that are neither in Q_s nor sides of
    t0 other than e0, form a tree Y_s; P_s is its unique perfect matching,
    found by matching a leaf to its neighbour and removing both.
    """
    if not is_good(T, s):
        raise ValueError('the state is not good')
    excluded = set(opposite_sides(T, s)) | {edge(v, w) for v, w in T.sides(T.t0)}
    excluded.discard(T.e0)
    across = {t: {} for t in T.faces}            # neighbour in Y_s -> shared side
    for v, w in T.left:
        if edge(v, w) not in excluded:
            across[T.left[v, w]][T.left[w, v]] = edge(v, w)
    leaves = [t for t in across if len(across[t]) == 1]
    P = set()
    while leaves:
        t = leaves.pop()
        if len(across[t]) != 1:
            continue                              # already matched
        (y, side), = across[t].items()
        P.add(side)
        for f in (t, y):
            for g in list(across[f]):
                del across[g][f]
                if len(across[g]) == 1:
                    leaves.append(g)
            across[f] = {}
    return P


def is_selection(T, P):
    """Whether P contains exactly one side of every face of T."""
    return all(sum(edge(v, w) in P for v, w in T.sides(t)) == 1 for t in T.faces)


def cycle_of_selection(T, P):
    """The Hamiltonian cycle of G that crosses exactly the edges of T not in P.

    P must be an acyclic selection.  Every face of T then has two sides not in
    P, and following them from face to face visits every face once.  The cycle
    is returned as a list of faces of T, that is, of vertices of G.
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
