"""Pairs of states: their cycles, the two reversals, sign and weight
(Sections 3 and 4 of the paper).

A pair (r, s) consists of two states with r(t) != s(t) for every t in A; s is
the second state, and u(t) is the third corner of t.  A pair gives
  D(r, s):  the edges r(t) -> s(t), a set of disjoint directed cycles through
            all of X;
  Q_s:      directed by r, with the edges r(t) -> u(t), one leaving every
            vertex of X.
A cycle is returned as the list of the faces t in A that supply its edges.
"""
from .states import states


def is_pair(T, r, s):
    return all(r[t] != s[t] for t in T.A)


def pairs(T):
    """Generate all pairs (r, s) of T."""
    for r in states(T):
        for s in states(T, avoid=r):
            yield r, s


def _cycles(T, arrow):
    """The cycles of a set of directed edges {tail: (head, face)} on X.

    Every vertex has at most one outgoing edge.  The cycles are listed in the
    order of their first faces in T.A, each starting at that face.
    """
    seen, cycles = set(), []
    for v in arrow:
        path = []
        while v in arrow and v not in seen:
            seen.add(v)
            path.append(v)
            v = arrow[v][0]
        if v in path:
            faces = [arrow[x][1] for x in path[path.index(v):]]
            i = faces.index(min(faces, key=T.index.get))
            cycles.append(faces[i:] + faces[:i])
    return sorted(cycles, key=lambda c: T.index[c[0]])


def D_cycles(T, r, s):
    """The cycles of D(r, s)."""
    return _cycles(T, {r[t]: (s[t], t) for t in T.A})


def Q_cycles(T, r, s):
    """The cycles of Q_s, directed by r.  There are none exactly when s is
    good (Lemma 3.4(1))."""
    return _cycles(T, {r[t]: (T.third(t, r[t], s[t]), t) for t in T.A})


def reverse_D(T, r, s, C):
    """Reverse the cycle C of D(r, s): exchange r(t) and s(t) on its faces."""
    r, s = dict(r), dict(s)
    for t in C:
        r[t], s[t] = s[t], r[t]
    return r, s


def reverse_Q(T, r, s, K):
    """Reverse the cycle K of Q_s: replace r by r^K, that is, r(t) by u(t) on
    the faces of K."""
    r = dict(r)
    for t in K:
        r[t] = T.third(t, r[t], s[t])
    return r, s


def delta(T, v, w):
    """delta_t(v, w) for the black face t at the edge vw: 1 if t is on the
    left of v -> w, else -1."""
    return 1 if T.left[v, w] in T.black else -1


def sign(T, r, s):
    """The sign eps(r, s): the product of delta_t(r(t), s(t)) over t in A.

    Both reversals change it (Lemmas 3.4(2) and 4.2(3)).
    """
    result = 1
    for t in T.A:
        result *= delta(T, r[t], s[t])
    return result


def corner_weights(T):
    """The local weights omega(t, v), as a dict {(t, v): omega(t, v)}.

    The arc gamma_y of a white face y follows the path of faces from y to t0
    in a breadth-first tree of G.  When it passes through a face t in A it
    turns around one corner v of t and crosses only the arc from p_t to v:
    from left to right if v is on the left of gamma_y, which counts 1, and
    from right to left otherwise, which counts -1.
    """
    if hasattr(T, '_kappa'):
        return T._kappa
    parent, queue = {T.t0: None}, [T.t0]           # face -> (parent, shared side)
    for t in queue:
        for v, w in T.sides(t):
            y = T.left[w, v]
            if y not in parent:
                parent[y] = (t, {v, w})
                queue.append(y)
    kappa = {(t, v): 0 for t in T.A for v in T.faces[t]}
    for y in T.white:
        entry, (t, exit) = None, parent[y]
        while t != T.t0:
            entry, (following, exit) = exit, parent[t]
            if t in T.black:
                v, = entry & exit
                a, = entry - {v}
                b, = exit - {v}
                i = T.faces[t].index(v)
                counterclockwise = T.faces[t][i - 2] == a and T.faces[t][i - 1] == b
                kappa[t, v] += 1 if counterclockwise else -1
            t = following
    T._kappa = kappa
    return kappa


def weight(T, s):
    """The weight omega(s): the sum of omega(t, s(t)) over t in A.

    Reversing a clockwise cycle C of D(r, s) raises the weight of the second
    state by a(C) >= 1, the number of white faces inside C (Lemma 4.6).
    """
    kappa = corner_weights(T)
    return sum(kappa[t, s[t]] for t in T.A)


def signed_sum(T, m=None):
    """The sum of eps(r, s) * omega(s)^m over all pairs (r, s), which is the
    value of (z d/dz)^m Z(z) at z = 1.

    By default m is the least number of cycles of a 2-factor of H.  The pairs
    whose second state is not good cancel (Lemma 3.5), and for this m the sum
    is m! times the value of Z(z)/(z - 1)^m at z = 1, which is not zero
    (Proposition 4.9).  Returns (sum, m); the sum is 0 if there is no pair.
    """
    terms = [(sign(T, r, s), weight(T, s), len(D_cycles(T, r, s))) for r, s in pairs(T)]
    if m is None:
        m = min((c for _, _, c in terms), default=0)
    return sum(e * w ** m for e, w, _ in terms), m
