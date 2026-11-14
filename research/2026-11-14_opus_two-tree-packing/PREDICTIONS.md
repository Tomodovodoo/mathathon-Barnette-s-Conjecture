# Predictions, written before the tests they name

Opus 5.5, 2026-11-14. Each line was committed before the corresponding run.

1. (made after reading the probabilistic folder, before any computation) The half-pair packing conjecture is true and needs no signed count: it reduces to the planar density bound (3.2) of the OpenAI paper, and the bijectivity of the states plays no role. Test: random deleted-corner maps that are not 2-factors also pack, in every rooted instance that has a pair. Second test: in rooted instances without a pair, some deleted-corner maps fail to pack, with a witness at a separating triangle with black inner boundary.
2. Inside each pair support F (a 2-factor of B), there is a black-rainbow W-tree (one edge per cherry) and a point-rainbow W-tree (one edge per nonroot). Both follow from prediction 1 and Edmonds' matroid intersection theorem, so I expect no failure.
3. (low confidence, about 50 percent each) P1: every 2-factor F splits into two point-rainbow W-trees. P2: every 2-factor F splits into two black-rainbow W-trees. P1 and P2 together on one split would make both states of a pair tree matchings, which is known to fail for some groups, so at least the joint statement fails; I expect each one-sided split to survive at V <= 14.
4. The edge set of W minus the triangle of t0 is a union of three spanning trees of W in every rooted instance with a pair (the 1/3 point is in the tree polytope). I expect it to hold also without a pair, since the 1/3 point has slack at a black inner triangle; medium confidence.
