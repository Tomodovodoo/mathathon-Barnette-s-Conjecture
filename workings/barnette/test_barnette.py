"""Tests; run `python -m pytest barnette` in workings/."""
from fractions import Fraction
from itertools import product

import networkx as nx
import pytest

from barnette import *
from barnette import examples as ex

GRAPHS = [ex.cube(), ex.prism(6), ex.truncated_octahedron(), ex.two_cubes()] \
    + [ex.nanotube(m) for m in (2, 3, 4)] + [ex.prism(k) for k in range(8, 17, 2)]
TRIANGULATIONS = [ex.running_example(), ex.eight_vertex_example(), ex.trap(),
                  dual_triangulation(ex.cube(), (0, 1)),
                  dual_triangulation(ex.prism(6), (0, 1)),
                  dual_triangulation(ex.nanotube(3), ('top', (2, 0)))]


def key(T, *states_):
    return tuple(tuple(s[t] for t in T.A) for s in states_)


def determinant(M):
    M, det = [[Fraction(x) for x in row] for row in M], Fraction(1)
    for i in range(len(M)):
        pivot = next((j for j in range(i, len(M)) if M[j][i]), None)
        if pivot is None:
            return 0
        if pivot != i:
            M[i], M[pivot], det = M[pivot], M[i], -det
        det *= M[i][i]
        for j in range(i + 1, len(M)):
            c = M[j][i] / M[i][i]
            M[j] = [a - c * b for a, b in zip(M[j], M[i])]
    return det


@pytest.mark.parametrize('G', GRAPHS, ids=len)
def test_cycle_avoiding_every_edge(G):
    for v, w in G.edges():
        for e in ((v, w), (w, v)):                # t0 is the first end of e
            assert is_hamiltonian_cycle(G, hamiltonian_cycle(G, e), avoid=e)


def test_input_is_validated():
    with pytest.raises(ValueError, match='bipartite'):
        validate(nx.complete_graph(4))
    with pytest.raises(ValueError, match='planar'):
        validate(nx.complete_bipartite_graph(3, 3))
    two = nx.disjoint_union(nx.cubical_graph(), nx.cubical_graph())   # joined by two edges
    two.remove_edges_from([(0, 1), (8, 9)])
    two.add_edges_from([(0, 8), (1, 9)])
    with pytest.raises(ValueError, match='3-connected'):
        validate(two)
    G = ex.cube()
    _, emb = nx.check_planarity(G)
    rotation = {v: list(emb.neighbors_cw_order(v)) for v in G}
    assert is_hamiltonian_cycle(G, hamiltonian_cycle(G, (0, 1), rotation), avoid=(0, 1))


@pytest.mark.parametrize('T', TRIANGULATIONS, ids=lambda T: len(T.vertices))
def test_states_agree_with_brute_force(T):
    roots = set(T.roots)
    choices = product(*([v for v in T.faces[t] if v not in roots] for t in T.A))
    brute = {c for c in choices if len(set(c)) == T.n}
    found = [s for s in states(T)]
    assert {key(T, s)[0] for s in found} == brute and len(found) == len(brute)
    assert abs(determinant(incidence_matrix(T))) == len(brute)
    good = [s for s in found if is_good(T, s)]
    assert key(T, *states(T, good=True)) == key(T, *good)
    G = T.primal()
    for s in good:
        P = selection(T, s)
        assert T.e0 in P and is_selection(T, P)
        assert is_hamiltonian_cycle(G, cycle_of_selection(T, P),
                                    avoid=(T.left[T.e0], T.left[T.e0[::-1]]))


def test_running_example_counts():
    T = ex.running_example()
    assert (T.n, len(list(states(T))), len(list(pairs(T)))) == (10, 12, 8)
    assert len(list(states(T, good=True))) == 6


@pytest.mark.parametrize('T', TRIANGULATIONS, ids=lambda T: len(T.vertices))
def test_reversals_sign_and_weight(T):
    all_pairs = {key(T, r, s) for r, s in pairs(T)}
    for r, s in pairs(T):
        assert is_pair(T, r, s)
        assert (len(Q_cycles(T, r, s)) == 0) == is_good(T, s)
        for K in Q_cycles(T, r, s):
            r2, s2 = reverse_Q(T, r, s, K)
            assert key(T, r2, s2) in all_pairs and s2 == s
            assert sign(T, r2, s2) == -sign(T, r, s)
            assert reverse_Q(T, r2, s2, K) == (r, s)
        for C in D_cycles(T, r, s):
            r2, s2 = reverse_D(T, r, s, C)
            assert key(T, r2, s2) in all_pairs
            assert sign(T, r2, s2) == -sign(T, r, s)
            assert weight(T, s2) != weight(T, s)
            assert sum(delta(T, r[t], s[t]) for t in C) in (3, -3)


@pytest.mark.parametrize('T', TRIANGULATIONS, ids=lambda T: len(T.vertices))
def test_signed_sum_counts_good_states(T):
    total, m = signed_sum(T)
    good = [(r, s) for r, s in pairs(T) if is_good(T, s)]
    assert len(good) == len(list(states(T, good=True)))      # one partner each
    assert total == sum(sign(T, r, s) * weight(T, s) ** m for r, s in good)
    assert total != 0
    assert signed_sum(T, 0)[0] == 0


@pytest.mark.parametrize('T', TRIANGULATIONS, ids=lambda T: len(T.vertices))
def test_exchange_walk_from_every_pair(T):
    for r, s in pairs(T):
        (r2, s2), moves = exchange_walk(T, r, s)
        assert is_pair(T, r2, s2) and is_good(T, s2)
        assert is_good(T, good_state(T, (r, s), max_moves=0))   # by enumeration


def test_eight_vertex_example():
    T = ex.eight_vertex_example()
    assert key(T, *states(T)) == ((1, 5, 7, 2, 6), (2, 1, 6, 7, 5), (2, 5, 1, 7, 6))
    assert [is_good(T, s) for s in states(T)] == [True, True, False]


def test_trap_and_separating_triangle():
    T = ex.trap()
    stuck = 0
    for r, s in pairs(T):
        q = len(Q_cycles(T, r, s))
        moves = [reverse_D(T, r, s, C) for C in D_cycles(T, r, s)] \
            + [reverse_Q(T, r, s, K) for K in Q_cycles(T, r, s)]
        stuck += q > 0 and all(len(Q_cycles(T, *p)) >= q for p in moves)
    assert stuck == 2
    G = ex.two_cubes()
    rooted = [dual_triangulation(G, e) for v, w in G.edges() for e in ((v, w), (w, v))]
    assert all(separating_triangle(T) for T in rooted)
    assert any(first_pair(T) is None for T in rooted)
    assert separating_triangle(ex.running_example()) is None
