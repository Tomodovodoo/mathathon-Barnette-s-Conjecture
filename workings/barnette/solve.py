"""From the graph to the Hamiltonian cycle, following Section 4 of the paper.

A first pair comes from a flow (Proposition 4.2).  From a pair, the exchange
walk reaches a pair whose second state is good, and a search through the
states finds a good state in any case; both are described in
proofs/algorithm/algorithm.md.  If there is no pair, T has a separating
triangle and is cut along it (Theorem 4.3).
"""
import networkx as nx

from .triangulation import Triangulation, dual_triangulation, edge
from .states import states, selection, cycle_of_selection
from .pairs import D_cycles, Q_cycles, reverse_D, reverse_Q, corner_weights


def first_pair(T):
    """A pair of T, or None if T has no pair.

    Send flow from a source to every x in X (capacity 2), from x to every face
    t in A with corner x (capacity 1), and from t to a sink (capacity 2).  A
    flow of value 2n uses two corners of every face and two faces at every
    vertex; these edges form a 2-factor of H, and alternate edges along each
    of its cycles give the two states.  A pair exists whenever T has no
    separating triangle (Proposition 4.2).
    """
    net = nx.DiGraph()
    for x in T.X:
        net.add_edge('source', ('x', x), capacity=2)
    for t in T.A:
        net.add_edge(('t', t), 'sink', capacity=2)
        for x in T.faces[t]:
            if x not in T.roots:
                net.add_edge(('x', x), ('t', t), capacity=1)
    value, flow = nx.maximum_flow(net, 'source', 'sink')
    if value != 2 * T.n:
        return None
    corners = {t: [x for x in T.faces[t] if x not in T.roots and flow['x', x]['t', t]] for t in T.A}
    faces = {x: [t for t in T.A if x in corners[t]] for x in T.X}
    r, s = {}, {}
    for t in T.A:
        x = corners[t][0]
        while t not in s:                     # walk once around an even cycle
            s[t] = x
            r[t] = x = next(y for y in corners[t] if y != x)
            t = next(f for f in faces[x] if f != t)
    return r, s


def exchange_walk(T, r, s, max_moves=None):
    """Walk from the pair (r, s) by reversals to a pair with good second state.

    This is Algorithm W of proofs/algorithm/algorithm.md.  Put
    alpha(t, v) = omega(t, v) - min_w omega(t, w) >= 0, the minimum over the
    three corners w of t.  The pool of a cycle C of D(r, s) is the list of
    tokens (t, j) with t on C and 1 <= j <= alpha(t, s(t)); it is longer when
    C runs counterclockwise.  The walk carries one token for every cycle.  A
    round starts with all cycles counterclockwise and, on each cycle, the
    first token that has no counterpart in the clockwise pool.  It then
    alternates
      beta:   reverse the first cycle of Q_s (stop if there is none: s is good);
      alpha:  reverse the first cycle of D(r, s) without a token; if there is
              none, reverse the first cycle whose tokens have counterparts in
              the opposite pool, and move them there.
    If alpha has nothing to reverse, the round ends at a pair with fewer
    cycles of D(r, s) and a new round starts.

    Returns ((r, s), number of moves), or None after max_moves moves.
    """
    kappa = corner_weights(T)
    low = {t: min(kappa[t, v] for v in T.faces[t]) for t in T.A}

    def pool(C, state):
        return [(t, j) for t in sorted(C, key=T.index.get)
                for j in range(1, kappa[t, state[t]] - low[t] + 1)]

    def alpha(r, s, tokens):
        cycles = D_cycles(T, r, s)
        held = [[i for i, (t, _) in enumerate(tokens) if t in C] for C in cycles]
        for C, mine in zip(cycles, held):
            if not mine:
                return reverse_D(T, r, s, C) + (tokens,)
        for C, mine in zip(cycles, held):
            here, there = pool(C, s), pool(C, r)
            ranks = [here.index(tokens[i]) for i in mine]
            if all(k < len(there) for k in ranks):
                tokens = list(tokens)
                for i, k in zip(mine, ranks):
                    tokens[i] = there[k]
                return reverse_D(T, r, s, C) + (tokens,)
        return None

    moves = 0
    while True:                                           # one phase
        for C in D_cycles(T, r, s):
            if len(pool(C, s)) < len(pool(C, r)):
                r, s = reverse_D(T, r, s, C)
        tokens = [pool(C, s)[len(pool(C, r))] for C in D_cycles(T, r, s)]
        while True:
            K = Q_cycles(T, r, s)
            if not K:
                return (r, s), moves
            if max_moves is not None and moves >= max_moves:
                return None
            r, s = reverse_Q(T, r, s, K[0])
            moves += 1
            step = alpha(r, s, tokens)
            if step is None:
                break
            r, s, tokens = step
            moves += 1


def good_state(T, pair=None, max_moves=1000):
    """A good state of T, or None if T has no pair.

    Runs the exchange walk from a first pair for at most max_moves moves, and
    otherwise enumerates the states until a good one appears.
    """
    pair = pair or first_pair(T)
    if pair is None:
        return None
    found = exchange_walk(T, *pair, max_moves=max_moves)
    if found is not None:
        return found[0][1]
    return next(states(T, good=True))


def separating_triangle(T):
    """A 3-cycle of T that bounds no face, or None."""
    facial = {frozenset(f) for f in T.faces.values()}
    nbrs = {v: set() for v in T.vertices}
    for v, w in T.left:
        nbrs[v].add(w)
    for v, w in sorted(T.edges()):
        for x in sorted(nbrs[v] & nbrs[w]):
            if frozenset((v, w, x)) not in facial:
                return v, w, x
    return None


def pieces(T, triangle):
    """Cut T along a separating triangle.

    Returns the face dicts of the two triangulations T_1 and T_2 of the
    proof of Theorem 4.3, the one containing t0 first.  Each consists of the
    faces of T on one side and a new face bounded by the triangle; both new
    faces are labelled ('cap', triangle).
    """
    x, y, z = triangle
    cut = {edge(x, y), edge(y, z), edge(x, z)}
    side, queue = {T.t0}, [T.t0]
    for t in queue:
        for v, w in T.sides(t):
            f = T.left[w, v]
            if edge(v, w) not in cut and f not in side:
                side.add(f)
                queue.append(f)
    cap = ('cap', triangle)
    first = {t: f for t, f in T.faces.items() if t in side}
    second = {t: f for t, f in T.faces.items() if t not in side}
    first[cap] = (x, y, z) if T.left[x, y] not in side else (x, z, y)
    second[cap] = first[cap][::-1]
    return first, second


def acyclic_selection(T, max_moves=1000):
    """The set M^* of a perfect matching M of G that contains the dual of e0
    and has G - M connected: a set P of edges of T that contains e0 and one
    side of every face, without cycles.

    If T has a pair, P comes from a good state (Proposition 2.3).  Otherwise
    T has a separating triangle, and P is put together as in the proof of
    Theorem 4.3.  The triangulation T_1 containing t0 has such a set P1
    containing e0; P1 contains one side e' of the triangle; the other
    triangulation T_2, with its new face as t0, has such a set P2 containing
    e'; and P = P1 | P2.
    """
    s = good_state(T, max_moves=max_moves)
    if s is not None:
        return selection(T, s)
    triangle = separating_triangle(T)
    first, second = pieces(T, triangle)
    cap = ('cap', triangle)
    P1 = acyclic_selection(Triangulation(first, T.t0, T.e0), max_moves)
    x, y, z = triangle
    e, = P1 & {edge(x, y), edge(y, z), edge(x, z)}
    return P1 | acyclic_selection(Triangulation(second, cap, e), max_moves)


def hamiltonian_cycle(G, e, rotation=None, max_moves=1000):
    """A Hamiltonian cycle of G that avoids the edge e, as a list of vertices
    (Theorem 1.1).

    G is a cubic, bipartite, 3-connected planar networkx graph; `rotation`
    optionally gives its embedding (see triangulation.embedding).
    """
    T = dual_triangulation(G, e, rotation)
    cycle = cycle_of_selection(T, acyclic_selection(T, max_moves))
    assert is_hamiltonian_cycle(G, cycle, avoid=e)
    return cycle


def is_hamiltonian_cycle(G, cycle, avoid=None):
    """Whether `cycle` lists every vertex of G once, consecutive vertices (and
    the last and first) being adjacent, without using the edge `avoid`."""
    steps = list(zip(cycle, cycle[1:] + cycle[:1]))
    return (len(cycle) == len(G) and set(cycle) == set(G)
            and all(G.has_edge(v, w) for v, w in steps)
            and (avoid is None or all({v, w} != set(avoid) for v, w in steps)))
