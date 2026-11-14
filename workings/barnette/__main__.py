"""`python -m barnette`: the proof at work on the cube and on the example of
Figure 3 of the paper."""
from . import *
from . import examples

G = examples.cube()
print('cube, avoiding the edge (0, 1):', hamiltonian_cycle(G, (0, 1)))

T = examples.running_example()
print('\nrunning example: n =', T.n, ' roots', T.roots, ' e0 =', T.e0)
print('states:', len(list(states(T))), ' good states:', len(list(states(T, good=True))))
for r, s in pairs(T):
    print('  pair  eps = %+d  omega(s) = %2d  cycles of D: %d  cycles of Q_s: %d'
          % (sign(T, r, s), weight(T, s), len(D_cycles(T, r, s)), len(Q_cycles(T, r, s))))
print('signed sum of omega^m and m:', signed_sum(T))
r, s = first_pair(T)
(r, s), moves = exchange_walk(T, r, s)
print('exchange walk from the first pair:', moves, 'moves, good state', s)
P = acyclic_selection(T)
print('selection P:', sorted(P))
print('Hamiltonian cycle through the 22 faces:', cycle_of_selection(T, P))
