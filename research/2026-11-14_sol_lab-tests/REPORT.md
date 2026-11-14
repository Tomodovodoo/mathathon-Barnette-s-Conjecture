# Test campaign report

COMPUTED. Added a deterministic counted campaign and five focused unit tests without changing the lab's production objects or export schema.
COMPUTED. The full tier covers every facial-root occurrence of all 55 plantri Eulerian triangulations through 14 vertices, plus the three requested larger witnesses.
COMPUTED. Independent standard-library comparisons through 12 vertices check complete state, pair and good-state sets and every pair sign.
COMPUTED. Li objects and both involutions agree with the second referee on identical exact geometry; both saved referees agree on drawing-independent fixed counts.
COMPUTED. No production-code bug was found. Absolute path-height invariance and raw object equality across different drawings require the qualifications in BUGS.md.

## Task and implementation

Extend the reference implementation's tests, expose vacuity, cover the named witnesses and preserve all public behavior. The new `workings/barnette_lab/barnette_lab/campaign.py` contains the mathematical checks and coverage counters. `run_tests.py` runs both unit tests and the selected campaign in one command. `tests/test_campaign.py` adds focused regressions for explicit failure guards, coverage accounting, prism relaxation bases, the recovery left inverse and sampler uniformity. The existing forest-test comment was corrected.

COMPUTED. The campaign checks all directed state-cycle disks, all pairs, cancellation only when a cyclic second state actually has partners, each Q-cycle reversal, local and closed signs, Lean phase ratios, the directed-cycle good-pair criterion, the cover-component identity, cycle white-area weights, minimum finite-difference coefficients, relative heights, signed height moments, unique mates and parity, every good-state recovery, exchange adjacencies and walks, ordered token involutions and constructors, and the region Euler and density identities. A zero total for any registered check fails the run. Per-check eligible vacuity remains visible.

COMPUTED. Rooting uses every face of every generated triangulation, including both face colour classes. This preserves the existing Instance face numbering. The running example uses its saved root triangle by vertex set; the missing filename in the brief is documented. The order-16 fixture comes from the E3 section of the original combinatorics counterexamples, rather than a newly generated proxy. The order-18 fixture comes from the exact retained JSON witness.

## Independent comparisons

COMPUTED. `etri.py` is imported read-only from the determinant referee folder. Its own standard-library reconstruction determines the faces, states, pairs, rooted Q forests and local signs. The adapter aligns faces by their vertex sets, and aligns the global orientation once on an edge. Complete sets, not just counts, must agree.

COMPUTED. `fp.py` is imported read-only from the second involution referee folder. With the lab's rational coordinates and vertical rays it supplies an independent complete object enumeration and both maps, compared object by object. The running example retains 213 lab objects and nine second-fixed objects; both saved referees record nine second-fixed objects for the note's 279-object drawing. The small-census second-fixed total is also compared to both saved referee outputs. No external script is executed in a mode that writes its own output folder. Bytecode writes are disabled during external imports.

COMPUTED. Ordered marked and exchange walks are checked from every pair and their endpoints independently checked by `fp.py`. They are different from the note's distinct-mark walk, so the report does not claim equality of their trajectories. The existing restart fixture remains part of both tiers.

## Evidence and limits

Commands from the repository root:

```powershell
python -B workings/barnette_lab/run_tests.py quick --output research/2026-11-14_sol_lab-tests
python -B workings/barnette_lab/run_tests.py full --output research/2026-11-14_sol_lab-tests
```

COMPUTED. `quick.json` and `full.json` contain every rooted instance, invariant counts, Li object counts, sampler statistics, coverage totals and elapsed seconds. The corresponding output text files retain the unit-test output and complete printed coverage tables. COVERAGE.md records before and after. README.md contains the final full table and the exact sampling ranges.

COMPUTED. Region bounds are exhaustive for the small subsets stated in the README and sampled at larger orders. Reverse recovery images are exhaustive only through order eight and sampled by explicit induced-tree cuts above it. Multiple ordered marks are bounded to 24 one-per-cycle combinations per pair, while the independent Li comparison enumerates its complete distinct-mark domain in the stated range. A finite cap on a walk raises failure rather than certifying a general running-time bound. Plantri class completeness is inherited from the existing hash-pinned setup, not independently certified here.

## What failed and why

REFUTED as initially phrased. Absolute heights are not path independent. After a path change each height may shift by a state-independent constant; relative heights and the relevant lowest signed moments are the invariant statements. The corrected interpretation is already in the combinatorics referee's rewritten proposition.

COMPUTED. Raw Li object counts depend on drawing and ray choices. Comparing 213 to 279 as if they described the same domain would create a false bug report. Common-geometry map comparisons and invariant fixed-count comparisons pass.

COMPUTED. No production bug required a fix. No claim about a paper beyond the checked finite instances was established by this work.

## Still open and three best next steps

1. Extend exhaustive region-subset checks and reverse-image enumeration to larger orders in separately bounded batches.
2. Add a second independent implementation of the constructive ordered-token maps and compare complete marked trajectories, including every restart branch.
3. Obtain a human review of the formulas and of the distinction between absolute and relative heights; finite agreement is not a substitute for that review.

## Leads for others

COMPUTED. The prism remains a small useful counterexample to exactness of the two-matroid relaxation. The order-16 minimal cover without any good orientation and the order-18 lattice witness remain explicit regression inputs. Their presence prevents a future test campaign from selecting only easy successful starts.
