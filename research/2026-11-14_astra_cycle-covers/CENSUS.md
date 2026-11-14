# Census of separator-free rooted instances

COMPUTED, T4 under review. plantri 4.5 -b -c4, every facial root, exhaustive lattice enumeration. Range: dual orders 6 through 24. All tested roots have pairs. No overflow or bound violation was reported. Equality counts agree with one-element-lattice counts at every order. The latter comparison tests strictness in addition to the weak bound.

| Dual order | Classes | Facial roots | c_min distribution | Largest lattice | Seconds |
|---:|---:|---:|---|---:|---:|
| 6 | 1 | 8 | 1: 8 | 1 | 0.05 |
| 7 | 0 | 0 | empty | 0 | 0.01 |
| 8 | 1 | 12 | 1: 12 | 1 | 0.02 |
| 9 | 0 | 0 | empty | 0 | 0.01 |
| 10 | 2 | 32 | 1: 32 | 1 | 0.01 |
| 11 | 1 | 18 | 2: 18 | 1 | 0.01 |
| 12 | 5 | 100 | 1: 100 | 2 | 0.01 |
| 13 | 3 | 66 | 2: 66 | 2 | 0.01 |
| 14 | 18 | 432 | 1: 408, 3: 24 | 2 | 0.02 |
| 15 | 19 | 494 | 2: 494 | 3 | 0.02 |
| 16 | 79 | 2212 | 1: 2044, 3: 168 | 3 | 0.03 |
| 17 | 134 | 4020 | 2: 3990, 4: 30 | 4 | 0.04 |
| 18 | 501 | 16032 | 1: 14080, 3: 1952 | 5 | 0.16 |
| 19 | 1147 | 38998 | 2: 38760, 4: 238 | 6 | 0.36 |
| 20 | 3976 | 143136 | 1: 117900, 3: 25200, 5: 36 | 8 | 1.35 |
| 21 | 11055 | 420090 | 2: 415036, 4: 5054 | 10 | 4.26 |
| 22 | 37231 | 1489240 | 1: 1137240, 3: 351600, 5: 400 | 12 | 16.17 |
| 23 | 114560 | 4811520 | 2: 4709964, 4: 101514, 6: 42 | 16 | 56.06 |
| 24 | 384053 | 16898332 | 1: 11968484, 3: 4918496, 5: 11352 | 20 | 210.02 |

Total rooted instances: 23,824,742. Maximum c_min is 6, first attained at order 23. The largest single census run took 210.02 seconds. Larger orders were not enumerated. The explicit family proves unboundedness beyond this finite range.

## Independent implementation checks

COMPUTED. code/levels.py independently enumerates degree-two corner selections and checks the primal complement identity for every resulting cover through order 17, then stops at the first disconnected level at order 18. It does not certify the larger C engine census independently. code/check.py uses reference state/pair enumeration for family m=2,...,6 and the prior square witness. Direct family enumeration reaches m=10. No independent human or separate-agent referee has reviewed these results.

## Parser caveat

The existing Windows plantri executable emits CRLF-expanded planar code. The C consumer reads in text mode and reverses this expansion. The Python parser explicitly replaces CRLF with LF. Its first unnormalized run failed at order 10 and was corrected before any level conclusions were retained. Extending the C pipeline to order 26 requires handling Windows control-Z and switching both producer and consumer to binary mode, or using text input. Do not extrapolate this pipeline past its tested range silently.

## Predictions and counterexamples

Prediction before census: c_min reaches at least 5 by order 24. Observed: 5 at 20 and 6 at 23. The record graphs led to the proved family. Prediction before the independent family test: unique cover with m-2 triangles and one pentagon. Confirmed through m=10. Prediction before flip-level search: levels need not be connected. First found failure is order 18; every root through order 17 was checked. This is smallest only within the separator-free class and the stated move definition.

The raw certificate data, commands, generator provenance, and retained witnesses are in data/ and code/README.md. The full strict-inequality problem remains open despite the negative census.
