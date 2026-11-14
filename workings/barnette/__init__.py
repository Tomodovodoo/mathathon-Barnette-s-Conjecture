"""The 2026 proof of Barnette's conjecture, as code to read next to the paper.

Every cubic, bipartite, 3-connected planar graph G has a Hamiltonian cycle
avoiding any given edge e:  hamiltonian_cycle(G, e)  returns one.
"""
from .triangulation import Triangulation, dual_triangulation, validate, edge
from .states import (states, is_good, opposite_sides, incidence_matrix, selection,
                     is_selection, cycle_of_selection)
from .pairs import (pairs, is_pair, D_cycles, Q_cycles, reverse_D, reverse_Q, delta, sign,
                    corner_weights, weight, signed_sum)
from .solve import (first_pair, exchange_walk, good_state, separating_triangle, pieces,
                    acyclic_selection, hamiltonian_cycle, is_hamiltonian_cycle)
from . import examples
