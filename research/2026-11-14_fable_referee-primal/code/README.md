# Referee's checker for the primal proof

COMPUTED. All code here is mine. It shares nothing with `research/2026-11-14_astra_primal-proof/check_primal.py` and uses no proof object from `workings/barnette_lab`. The one outside input is the plantri binary `workings/barnette_lab/vendor/plantri.exe`, called as `plantri -ba N`. It lists the Eulerian triangulations with `N` vertices, one per isomorphism class, with their rotation systems. I did not certify plantri's census.

## Files

- `primal.py`. A cubic graph with a rotation system (`PG`): face tracing, corners, cuts, components, perfect matchings, caps. A rooted graph (`Rooted`): colour classes, `A`, `R`, `X`, the sign `δ`, the path flow, local potentials, states, pairs, `Q_s`, cut sides, state circuits.
- `gen.py`. Parses plantri output and builds the dual cubic graph with its rotation system. Also a cube written by hand.
- `check_lemmas.py`. One counted check per assertion of Lemmas 1 to 13 and Theorem T. A failed check is counted under `… FAIL` and printed. Nothing fails silently.
- `check_examples.py`. Reads Section 11 of `proofs/primal/PRIMAL-PROOF.md`, rebuilds the rotation system from the printed facial cycles, and recomputes every printed item.
- `out/`. Outputs. `totals.json` adds the three runs.

## Commands

From this folder:

```
python check_lemmas.py 6 12  > out/lemmas_6_12.json     # 17 s
python check_lemmas.py 13 13 > out/lemmas_13.json       # 38 s
python check_lemmas.py 14 14 > out/lemmas_14.json       # 430 s
python check_examples.py     > out/examples.txt         # 1 s
```

The two numbers are the least and greatest number of faces of `G`, which is the number of vertices of the dual triangulation.

## Range

56 graph records: the cube by hand, and the duals of all Eulerian triangulations with 6 to 14 vertices (1, 0, 1, 1, 2, 2, 8, 8, 32, so 55 classes). The hand cube repeats the 6-vertex case, and every count below includes it twice. The cubic graphs have 8 to 24 vertices. 32 of them have no nontrivial 3-edge cut, 24 have at least one (39 such cuts in all).

A rooting for the state machinery is a vertex `b0`, and its colour class is then called black, so both colourings occur. There are 1,214 of them. Recovery and the recursion also choose the edge `e0` at `b0`: 3,642 pairs `(b0, e0)`.

15,202,328 checks, 0 failures.

## What is checked, lemma by lemma

| Lemma | Checks (names in the output) | Count |
| --- | --- | --- |
| 1 | facial boundaries are cycles; three distinct faces at each vertex; two faces share at most one edge; the counts; `\|R\| = 3`, `\|X\| = \|A\|` | every graph, every root |
| 2(a) | every face circuit (cycle of the face-link graph) is a bond with connected shores; the number of bonds, by enumeration of all `2^(\|V\|-1)` vertex subsets, equals the number of face circuits; no root face meets the cut side of a state circuit | 1,066,157 face circuits = 1,066,157 bonds |
| 2(b) | `\|S\| + \|U_S\| = \|E_S\| + 1` on both shores of every bond; mixed faces are the circuit faces; each has a cut edge | 2,132,314 shores |
| 3 | one `σ` in (2.2) around every face circuit, both directions, both shores, both colourings; reversal flips `σ` | 4,264,628 |
| 4 | (3.1) for every `Y ⊆ X` holds exactly when a pair exists; every graph with only trivial 3-edge cuts has a pair for every root; for each inclusion-minimal deficient `Y`: `K` connected, induced, `W_1` empty, three cut edges with black ends inside, `k = 1`, `d(Y) = 4 - 2k - c/3 = 1`, both shores have two vertices | 1,214 roots; (3.1) fails at 326 of them |
| 5 | for every state and every choice of outgoing links, every directed circuit: the four counts, `U = r(B∩S) ∪ C`, `h = 2ℓ + 3`, `\|W∩S\| = \|B∩S\| + 1`, `Σδ = -3σ` | 84,984 state circuits, lengths 3 to 11 |
| 6 | divergences of the path flow; consistency of the local potentials; slope `= σ\|W∩S\|` on every state circuit, for the path flow and for a second flow (path flow plus random integer circulations) | 84,984 twice |
| 7 | for every state `s` with a partner and a circuit in `Q_s`: partner signs sum to zero; each circuit of `Q_s` is odd and avoids `R`; reversal maps partners to partners, has no fixed point, is an involution, flips the sign | 20 states, 40 reversals |
| 8 | `Z` computed by brute force over all pairs; circuits of each `D` odd, at least 3 long, cover `X`; each group has `2^c` pairs; group sum equals (6.3); `(h+3)/2` negative signs on the positive orientation; `Z ≠ 0`; lowest coefficient equals (6.4); `Z` equals the sum over circuit-free second states; such a state with a partner exists | 888 roots with a pair; minimum circuit number 1, 2, 3 at 568, 162, 158 roots |
| 9 | for every circuit-free `s` with a partner and each of the three `e0`: `K` connected with `\|V\|-1` edges; removed links form a tree on the faces; degrees | 9,768 recoveries |
| 10 | parent edges of white vertices form a perfect matching in `K` through `e0`; its edge at `b` lies on `s(b)` | 9,768 |
| 11 | for every perfect matching `M` and every union `S` of components of `G - M`: `h = 2ℓ`, either colour called black | 8,067 perfect matchings |
| 12 | `P \ {e0}` and `P` have no face circuit; `G - P` connected. General form: for every perfect matching and every root, if some state is compatible then the complement is connected | 9,768; 186,476 matching and root pairs |
| 13 | every nontrivial 3-edge cut: shores connected, `ℓ ∈ {0,3}`, three distinct ends, exactly one rotation at the cap vertex has genus 0, cap simple cubic bipartite 3-edge-connected and smaller; all pairs of cap Hamiltonian cycles omitting the same cut edge glue to a Hamiltonian cycle | 39 cuts, 78 caps |
| T | brute force: every edge is avoided by some Hamiltonian cycle (1,821 edges). The proof run as a recursion (cap, cap, glue, or the main case) for every `(b0, e0)` | 3,642 runs, depth up to 2 |

## Three observations that are not in the note

- A state with circuit-free `Q_s` and no partner never gives a tree in Lemma 9 (25,272 cases). The partner hypothesis cannot be dropped.
- A circuit-free second state with a partner has exactly one partner (3,256 states).
- For a perfect matching `P` and a root, a state compatible with `P` exists exactly when `G - P` is connected (35,712 yes, 150,764 no, no mixed case).

These are COMPUTED on the range above and nothing more.

## Worked examples

`out/examples.txt`: 33 comparisons, 0 failed. For the cube and for the 20-vertex example the printed facial cycles are coherently oriented and give a genus-0 rotation system with the printed edges. From that and the printed flow I recompute the potentials, the state list, every `Q_s` and `c_s`, the set of ordered pairs, every circuit with its cut side, count tuple, delta-sum and slope (2 and 26 circuits), the polynomials `-z` and `4z + 9z^2 - 2z^3 - 9z^4 - 2z^5`, the cancelling state `s_1` with partners `s_6, s_7` and its `Q`-circuit `(5,9,10)`, the removed set, the tree, `P`, and the Hamiltonian cycle. All agree with the note.

## Limits

Finite range only. The orientation convention (`δ = +1` in the direction of my face tracing) is a global choice. Every statement tested is invariant under the global flip, and I did not determine which of the two the author's "black end on the left" is. An early version of `check_examples.py` had a regular expression that matched no state line, so two comparisons passed vacuously. I found it because a later step crashed, fixed it, and added a guard that the parsed state list is nonempty.
