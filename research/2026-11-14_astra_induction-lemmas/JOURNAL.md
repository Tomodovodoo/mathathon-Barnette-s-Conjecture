# Research journal

2026-11-14, gpt-6-astra. Assigned scope is G and X. All new proofs are T2, unreviewed; all new census evidence is T4 unless independently certified. No child agents. Imports are read-only, with Python bytecode writing disabled.

## Predictions before experiments

1. The connected-complement deficiency formula is correct, including boundary walks with repeated edges. Test by direct Hall sums and independent embedded-face traversal through V=14, and symbolic elimination of Euler and side-count identities.
2. A simple bad contraction is witnessed by a 5-cycle, not a 4-cycle. Test each new black-inner triangle by lifting its three edges and checking the five boundary incidences. A 4-cycle witnesses parallel edges instead.
3. Disk curvature gives at least one interior degree-4 vertex for a chordless 4- or 5-cycle with nonempty interior and no separating triangles. It does not guarantee that vertex is not a boundary-face apex. Singleton tight sets are an immediate suspected obstruction to the earlier proposed argument.
4. Corner avoidance may survive, but all four feasible corner patterns at every usable vertex likely fail. Test all rooted instances through V=16. Test whether the mate of an exceptional matching is a nonexceptional tree matching, then the weaker existence of a repairing reversal of one D-cycle.

The requested four-cycle-only picture conflicts with the supplied source, MISSING-LEMMA.md Lemma B. The source uses 4- and 5-cycles. This discrepancy must be resolved before attempting a minimal-region proof.

## First results and revised tests

- Deficiency formula: symbolic residual zero, and all connected eligible complement sets through V=14 pass, including repeated boundary walks.
- G descent: the prediction that an innermost bad region contains a good degree-4 vertex is false at V=11, graph 1, root 1,0,2. The 4-cycle 0,1,7,5 encloses only vertex 6, and both merges there are bad. Thus the proposed Euler-counting descent cannot close G as stated.
- X: all feasible patterns is false at V=8. Mate repair of exceptions fails from V=16. Every single D-cycle repair can fail from V=17, graph 451, root 7,1,8, x=2, merge 0,9. The two reversals give a non-tree state and another exception. Through V=18 there are 222 such exceptions in total.
- Saturation change of parameter: replace a single reversal by the entire direction cube of the fixed cover, then by the graph of tree matchings joined by D-cycle reversals with the mate recomputed after each move. Prediction: some fixed cubes contain only exceptional tree states, but a larger tree-state component may still escape. This tests the actual distinction between keeping a cover and changing it.
- The inherited no-frozen-face conjecture was already tested by Opus as S7. It was not a new untried hypothesis. Our new test extends it through V=18.

## Second G descent test

Before testing: the failure above involves a four-cycle, while a bad five-cycle contains at least two interior degree-4 vertices by coloured curvature. Test the sharper prediction that every black-heavy bad five-cycle, or at least every innermost such five-cycle, encloses a good degree-4 vertex. This would repair the choice of region in the proposed proof, although an arbitrary-size argument would still be needed.

Result: even the innermost-five-cycle version fails at V=13, graph 4. Before the next test, restrict the source vertex of the five-cycle to one whose two merges are both bad. This removes the V=13 example, whose boundary source already has a good alternative. Prediction: this restriction may rescue the descent claim. Test all such regions and their inclusion-minimal members through V=19.

Result: the blocked-source refinement fails too, at V=14 graph 22. Boundary sources 8 and 9 and interior degree-4 vertices 6 and 13 all have both merges blocked. The cycle is 0,5,10,9,8; its interior is 6,7,13. Added an independent flow replay. No inward-selection rule tested here survives.

## Saturation and scope at handoff

The escalation ladder was used within this sub-agent's scope: algebraic elimination, embedded census, extremal witnesses, weaker local hypotheses, whole-cover direction cubes, the directed-cycle formulation, and read-only consultation of the referee and primal files. New delegation was prohibited, so no broad agent campaign was launched. The four-cycle descent, two refinements of it, mate repair, one-cycle repair, and whole-cover repair are now closed routes. The surviving global selection and cover-changing exchange questions need different arguments. No claim of exhaustive proof search is made.
