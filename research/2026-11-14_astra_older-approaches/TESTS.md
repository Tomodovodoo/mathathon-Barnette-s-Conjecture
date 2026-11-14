# Predictions recorded before computation

CONJECTURE/T5. The literal identification of the two parity obstructions is false. The contracted graph and the dual triangulation are different graphs; an even-order contracted triangulation can fail Theorem 11 at its outer triangle while the original dual has no separators. Test all plantri Eulerian triangulations of orders 6 through 12, all facial roots, and separately the contraction of the square faces of the truncated octahedron.

CONJECTURE/T5. A Goodey graph need not have c_min=1. Enumerate pairs for the cube, hexagonal prism and truncated octahedron. No uniform bound is predicted.

PROVED-HERE/T2, unreviewed. Edge avoidance implies inclusion of either other incident edge in any cubic graph: a spanning cycle has degree two at that vertex. Test all target edges of the named graphs.

HUNCH/T6. Pfaffian orientation alone does not supply the rooted triangular incidence structure or positive disk circulation. Test Heawood and a trisum of three cubes for Hamiltonicity and 2-extendability, but do not attempt to run the planar lab on a fabricated embedding.

## Outcomes

COMPUTED/T4. `results.json` contains 15 unrooted triangulations and 262 rooted cases through dual order 12; pair existence agrees with the black-inner criterion in every case. There are 78 disagreements between separator interior parity and black-inner colour on the same T. The correctly typed contraction counterexample is the truncated octahedron, whose square contraction is an octahedron with three vertices inside its outer triangle. BRIDGES.md gives a direct proof.

COMPUTED/T4. `goodey.json` has 18 four/six instances through dual order 16, c_min in {1,2} when a pair exists, and two no-pair roots. `refined.json` records the 32- and 48-vertex examples whose minimum-cycle pairs are never tree pairs. `chains.json` records k=1 through 8 with c_min=k. The chain construction has an unreviewed general proof in BRIDGES.md.

COMPUTED/T4. All 138 requested edge inclusions across the four named graphs succeeded. Fixed-root frequencies are retained per edge in results.json. These depend on the sampling rule and prescribed omitted edge.

COMPUTED/T4. Heawood: 24 Hamiltonian cycles; cube trisum: 12; K3,3 control: 6. All tested three-edge paths extend. Each is two-extendable; only the first two have Pfaffian status supplied by the cited structural theorem.

Scope limits: no exhaustive census of all facial 2-factor contractions; no implementation of arbitrary BF21 separating-digon conditions; no certified T3 computation; no universal separator-free Goodey bound or canonical forest rule. Actual fullerene graphs fail bipartiteness and were not fed to the planar lab. Predictions that failed remain above. Predictions for the additional Goodey/refinement and chain runs are recorded in their source before the run, with the chain prediction tested rather than assumed.


COMPUTED/T4, final spot check. `code/validate.py` verifies the radial/permeating-tree predicate equivalence on 39,714 nontrivial vertex subsets across all 15 duals of orders 6?12, and verifies all 108 black-band face incidences used by the chain proof through k=8. This is an author check, not independent review. Output: `code/validation.json`.
