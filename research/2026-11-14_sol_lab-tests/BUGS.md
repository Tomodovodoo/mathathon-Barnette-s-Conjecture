# Bugs and statement discrepancies

COMPUTED. No production-code bug was exposed by the completed campaigns. The changes add tests and documentation. `core.py`, `algorithms.py`, `li.py`, `verify.py`, public function names, face and vertex numbering, and schema-1 JSON export are unchanged.

## Statement and documentation discrepancies

1. COMPUTED. The brief's `paper/figures/example.json` no longer exists. The retained 13-vertex instance is `paper/figures/running.json`. The campaign reconstructs its graph and identifies its root by its vertex set, without changing the lab's face numbering.
2. REFUTED as an absolute-height assertion. Heights along two face paths need not be identical. The correct checked statement is that their difference is independent of the state, so relative heights are path independent. The clarified source is `research/2026-11-14_astra_referee-combinatorics/REWRITTEN-PROP-5-1.md`, last paragraph. The campaign also checks signed moments at and below the minimum cycle count for both path families.
3. COMPUTED. In the running example the lab's drawing gives 213 distinct-mark objects, 141 first-fixed objects and 9 second-fixed objects. The note's layout gives 279, 273 and 9, as recorded by both involution referees. This is a drawing choice, not an involution failure. The independent second referee, supplied with the lab's exact rational coordinates and vertical rays, agrees object by object on both maps. Signs agree up to one global orientation convention. No claim of equality between different drawings' raw object sets is made.
4. COMPUTED. The ordered incidence-token marked walk and the note's distinct ray-intersection walk have different domains. Their trajectories and move counts are not interchangeable. The tests compare the lab's Li maps exactly to the second referee on a common domain, compare the drawing-independent second-fixed counts to both saved referees, and check every ordered-walk endpoint with the referee's independent Q-cycle detector. This does not identify the two walks.
5. COMPUTED. The prism relaxation has six common bases, only two states. A successful return from the current augmenting order does not certify that the relaxation is exact. The new regression enumerates all six bases.
6. COMPUTED. The old cube-forest test said duality was embedding independent. That comment was too broad. It now states the property used here, uniqueness of the subdivided K4 embedding. No assertion changed.
7. COMPUTED. The old nine tests and 77-run ledger used plain `assert` in mathematical verifiers. New campaign obligations use an explicit exception guard and remain active with `-O`; external referees and the legacy verifier retain their original assertions. Normal Python is the documented execution mode.

## Limits

COMPUTED. Bounds 3.3 and 3.4 and the exact Euler identity are checked on explicitly described finite subset families, not all subsets at every order. Recovery's reverse image is exhaustive through order eight, then checked on deterministic two-tree cuts. Those limits are printed in the README and coverage ledger. No general proof or human referee certification is claimed.
