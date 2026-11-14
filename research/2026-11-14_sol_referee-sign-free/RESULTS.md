# Independent computations

COMPUTED. All commands below run from the repository root under Python 3.14. They import neither the lab nor the author's implementation. The lab supplies only its documented plantri executable. Plantri is called directly with `-b -a V`; all faces are used as roots, including both colour choices. These are rooted occurrences, not rooted isomorphism classes.

```
python research/2026-11-14_sol_referee-sign-free/check.py
python research/2026-11-14_sol_referee-sign-free/check.py --all-maps
python research/2026-11-14_sol_referee-sign-free/regions.py
python research/2026-11-14_sol_referee-sign-free/necessity.py
python research/2026-11-14_sol_referee-sign-free/witness_detail.py
python research/2026-11-14_sol_referee-sign-free/captions.py
python research/2026-11-14_sol_referee-sign-free/render.py
python research/2026-11-14_sol_referee-sign-free/render.py --original
```

The first two commands write `census.json` and `census-exhaustive.json`, respectively, followed by `witness16.json`. Other commands write the correspondingly named JSON files. Logs record the same command names. The default packing campaign enumerates every deleted-corner map for n<=7, then 20 fixed-seed maps per eligible root; its count excludes separately enumerated covers. `--all-maps` checks every map through order 12. Census results are saved before the larger witness, so counters in a census file cover exactly orders 6-12.

| Requested quantity | Note | Independent result |
| --- | ---: | ---: |
| rooted occurrences through 12 | 262 | 262 |
| with a pair | 208 | 208 |
| states | 1,706 | 1,706 |
| covers | 210 | 210 |
| rainbow trees | 74,432 | 74,432 |
| good states | 620 | 620 |
| connected J for identity (3.3) | 57,901 | 57,901 |
| walk states | 325,536 | 325,536 |
| involution evaluations | 5,052 | 5,052 |
| positive-excess trees with no decreasing exchange | 8,782 | 8,782 |
| first order with such a tree | 8 | 8, with 120 trees |

COMPUTED. The headline counts agree with the note's saved data. The lab README's independently checked-state row also records 262 roots, 1,706 states, 208 paired roots and 620 good states. This was a comparison after constructing our objects, not an implementation dependency.

The note's 82,118 tested maps are a mixed exhaustive/sample count. STATUS.md states this correctly: all maps for n<=7, then 20 maps otherwise, plus the 210 covers. Our default count is 81,908 without counting those covers again, so adding 210 gives exactly 82,118. No claim of exhaustive map enumeration at orders 11-12 should be inferred from the note's number. Our exhaustive campaign checks 2,624,616 deleted-corner maps and explicitly partitions both the W-edges and the root-contracted primal sides into two forests in every case. Two forests with 2n edges on n+1 vertices are two spanning trees.

COMPUTED. `check.py` enumerates states by matching recursion, covers as distinct unions of disjoint state matchings, and rainbow trees by graphic independence of a vertex transversal in W. Goodness is checked separately by Q_s plus a root star. It brute-forces all alternatives for each exchange, tests all cover selections against the directed forest description, checks unique cover membership, walk reversal and fixed-point-free involutions, and takes the reverse monotone closure of all good states for Step X. All nonempty vertex subsets are checked for density. Its final version also recovers each cover directly by the H-tree parent map and checks the directed-cycle/second-cover equivalence.

COMPUTED. `regions.py` checks tree/cotree equivalence on 524,000 fixed-seed sets of removed spokes. It constructs regions independently by merging original T-faces across edges absent from the induced subgraph. This checks Lemma 6.2 on every connected induced subset with at least three vertices at every root through 12: 557,586 sets and 793,254 regions. It checks the identity and each individual region bound, including triangular regions. `necessity.py` constructs one of Remark 6.7's obstructed maps for each black-inner separator, 68 in total, and verifies failure of the exact two-forest partition algorithm.

COMPUTED. At plantri index 27 of order 16, rooted at `{0,1,2}`, the three covers have respectively:

| cover | cycles | states | good states | rainbow trees |
| --- | ---: | ---: | ---: | ---: |
| bad cover | 1 | 2 | 0 | 6,144 |
| other cover | 3 | 8 | 6 | 6,912 |
| other cover | 3 | 8 | 6 | 6,912 |

The triangulation has 19,968 rainbow trees overall and 12 good states. The bad cover has no excess-zero rainbow tree. `witness-detail.json` includes its complete incidence set and both states. `captions.py` independently checks the running example's 1,792 rainbow trees, six good states, loads, exchange endpoint and increased excess, fundamental cycle, and the two-step involution orbit. It also records coincident Figure 5 vertices 4 and 5.

## Failed checks and their resolution

COMPUTED. The initial full-map run completed the entire small census and all 2,624,616 maps in 503.78 seconds, then failed at a wrongly implemented corollary check on the sixteen-vertex witness. My test had imposed both the face and vertex conditions while trying to test the face condition alone. The bad cover exposed that mistake. I corrected the test to select one incidence per face, allowing repeated vertices. The corrected default campaign and witness then passed. `exhaustive-map-attempt.log` retains the initial failure rather than hiding it. The full-map campaign was rerun with the correction, and its clean log is `check-all-maps.log`.

The finite computations do not prove Step X at arbitrary order. Larger ranges quoted in the note were reconciled against saved reports, not rerun here. See PROVENANCE.md.
