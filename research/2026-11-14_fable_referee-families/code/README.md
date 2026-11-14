# Referee code

Written by Claude Fable 5.2 from the OpenAI paper and the glossary. `core.py` does not import `workings/barnette_lab`. It uses networkx for the planar embedding and the laboratory's `vendor/plantri.exe` (`-b -a`) to list Eulerian triangulations. One script, `t_chain_lab.py`, imports the author's `families.py` to generate their chain graphs and nothing else.

Python 3.14, networkx 3.6.1, numpy 2.4.3. Run from this directory. Every run finished in under two minutes except `t_tubes_long.py` (about four minutes, of which 105 s for the last Hamiltonian count).

| Command | Output | What it checks |
|---|---|---|
| `python t_sanity.py` | printed | conventions: unit circulation, disk identity, sign formula, the orientation with J=-1 has the larger omega |
| `python t_families.py` | `out_families.json` | prisms m=2..12 with every edge; tubes width 4 (L<=6) and 6 (L<=4): S, determinant, P, M, good pairs, least cover, polynomial, H, avoidance at the root edges |
| `python t_tubes_long.py 45 > out_tubes_long.txt` | `out_tubes_long.txt`, `out_tubes_long.json` | tube sequences past the initial values of each recurrence. The argument is the time in seconds after which a sequence stops |
| `python t_certs.py` | `out_certs.txt` | replay of the author's eight matrix certificates and comparison with the brute-force sequences |
| `python t_chain.py > out_chain.txt` | `out_chain.txt`, `out_chain.json` | prism chain for three identifications, root sweeps of M on tubes, four-subdivided octahedron over all roots |
| `python t_chain_perms.py` | `out_chain_perms.txt` | Hamiltonian counts of the chain for all six identifications |
| `python t_chain_lab.py` | `out_chain_lab.txt` | the author's chain graphs counted with `core.py`, and the search for the mixed gluing rule |
| `python t_census.py 16 > out_census_16.txt` | `out_census_16.txt`, `out_census_16.json` (also the run with 14) | all roots of all triangulations up to 16 vertices: common sign of states, zero signed sum, balance, M even, M>=2m, M>=2^m, 2^m divides P, vanishing moments, gauge systems over GF(2), residues, zeros of the polynomials |
| `python t_walk.py 12 > out_walk.txt` | `out_walk.txt`, `out_walk.json` | the height-marked walk on every marked object of 215 rooted instances |
| `python t_misc.py` | `out_misc.txt` | spanning trees of H, bridges of H, separating triangles of tubes, H_avoid >= M and 3M <= H on 1206 roots |

Conventions in `core.py`. Faces are stored with one orientation of the sphere. delta(v,w)=+1 when (v,w) is a dart of its black face in that orientation. The weights a(t,v) are the path cochains of Lemma 5.3, one path per inner white face from a breadth-first tree of the dual of H_0, and kappa_y is the cochain of the single face y, so the height of y at s is the sum of kappa_y over the spokes of s. A state is good when the opposite edges form a tree after the three roots are identified. Polynomials are printed as coefficient tuples from the lowest exponent, divided by a monomial and with positive top coefficient.

Known limits. `hamilton` is a plain depth-first search with one degree prune and is slow beyond about 90 primal vertices. `summary` lists all states and all covers and is meant for small instances. The assertion in `summary` on the sign formula is vacuous, the real check is in `t_sanity.py`.
