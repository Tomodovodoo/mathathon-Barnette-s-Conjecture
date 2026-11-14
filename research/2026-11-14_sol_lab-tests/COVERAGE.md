# Coverage ledger

COMPUTED. Baseline from `research/2026-11-14_sol_route-constructive/data/verification.json`, as independently recounted in the determinant referee's REFEREE-constructive.md: 77 rooted runs, 59 with pairs, 18 without; 1,040 states and 254 ordered pairs. Cancellation had partnered cyclic second states in only three runs, covering six pairs. The nine unittest tests had no sampler uniformity check and no per-check vacuity table.

## After

COMPUTED. Commands, versions and input hashes are in environment.json. Run from the repository root:

```powershell
python -B workings/barnette_lab/run_tests.py quick --output research/2026-11-14_sol_lab-tests
python -B workings/barnette_lab/run_tests.py full --output research/2026-11-14_sol_lab-tests
```

COMPUTED. PowerShell output redirection captured the two `*-output.txt` files. Their encoding was normalized from UTF-16 to UTF-8 without changing their text. Each run executes 14 unit tests first. Every registered check must have a positive object total. Zero-object eligible runs are reported as vacuous rather than silently counted as passes.

COMPUTED. Quick: 70 rooted runs in 14.02 campaign seconds. Full: 1209 rooted runs in 232.19 campaign seconds. The full census has 55 graphs and 1,206 facial roots through order 14, of which 880 have a pair and 326 do not. The three special witnesses all have pairs. Independent complete-set comparisons cover all 262 facial roots through order 12, 208 with pairs and 54 without. All 14 unit tests pass in both tiers.

COMPUTED. Cancellation now has 23 nonvacuous rooted runs, 28 partnered cyclic second states and 56 actual Q-cycle reversal objects. Those totals include the three requested witnesses and count repeated occurrences explicitly. The table records every other check in the same way. Region and reverse-image subset ranges are exactly those in the lab README; neither is presented as exhaustive at larger orders.

| check | instances | objects | vacuous count |
| --- | ---: | ---: | ---: |
| Euler induced regions | 1209 | 160963 | 0 |
| Lean phase ratio | 883 | 3326 | 326 |
| Li independent objects and maps | 211 | 27355 | 54 |
| Li independent signed convention | 211 | 27355 | 54 |
| Q cancellation partnered states | 23 | 28 | 1186 |
| Q reversal objects | 23 | 56 | 1186 |
| bound 3.3 regions | 1209 | 136279 | 0 |
| bound 3.4 connected subsets | 671 | 18815 | 538 |
| cover components | 883 | 3326 | 326 |
| cycle white-face weight | 883 | 6950 | 326 |
| directed good-pair criterion | 883 | 3326 | 326 |
| even good states | 1209 | 13016 | 0 |
| exchange adjacency | 883 | 7006 | 326 |
| exchange walks | 883 | 3468 | 326 |
| good unique partner | 883 | 3270 | 326 |
| height cycle increments | 883 | 79660 | 326 |
| heights path independence | 1209 | 150368 | 0 |
| independent good states | 208 | 620 | 54 |
| independent pairs | 208 | 624 | 54 |
| independent signs | 208 | 624 | 54 |
| independent states | 262 | 1706 | 0 |
| lowest finite difference | 883 | 941 | 326 |
| marked constructors | 883 | 3326 | 326 |
| marked nonfixed moves | 7 | 136 | 1202 |
| ordered mult mark involutions | 883 | 34846 | 326 |
| ordered token involutions | 883 | 38768 | 326 |
| pair criterion | 1209 | 1209 | 0 |
| pair local sign and closed formula | 883 | 3326 | 326 |
| property black inner separator | 326 | 326 | 0 |
| property has pair | 883 | 883 | 0 |
| property m=1 | 562 | 562 | 0 |
| property m=2 | 163 | 163 | 0 |
| property m=3 | 158 | 158 | 0 |
| property minimal cover without good pair | 2 | 3 | 0 |
| property white inner separator | 374 | 374 | 0 |
| recovery image | 331 | 788 | 878 |
| recovery injectivity | 883 | 9810 | 326 |
| sampler exact probability | 2 | 5 | 0 |
| sampler seeded chi square | 2 | 3600 | 0 |
| saved running referees | 1 | 2 | 0 |
| saved small census referees | 2 | 132 | 0 |
| signed height moments across paths | 883 | 4490 | 326 |
| state disk W=B+1 | 1209 | 27090 | 0 |
| two matroid common bases | 1 | 6 | 0 |

## Quick table

| check | instances | objects | vacuous count |
| --- | ---: | ---: | ---: |
| Euler induced regions | 70 | 8634 | 0 |
| Lean phase ratio | 64 | 190 | 6 |
| Li independent objects and maps | 64 | 2836 | 6 |
| Li independent signed convention | 64 | 2836 | 6 |
| Q cancellation partnered states | 3 | 8 | 67 |
| Q reversal objects | 3 | 16 | 67 |
| bound 3.3 regions | 70 | 8554 | 0 |
| bound 3.4 connected subsets | 55 | 4055 | 15 |
| cover components | 64 | 190 | 6 |
| cycle white-face weight | 64 | 310 | 6 |
| directed good-pair criterion | 64 | 190 | 6 |
| even good states | 70 | 352 | 0 |
| exchange adjacency | 64 | 326 | 6 |
| exchange walks | 64 | 236 | 6 |
| good unique partner | 64 | 174 | 6 |
| height cycle increments | 64 | 3116 | 6 |
| heights path independence | 70 | 3264 | 0 |
| independent good states | 61 | 144 | 6 |
| independent pairs | 61 | 144 | 6 |
| independent signs | 61 | 144 | 6 |
| independent states | 67 | 260 | 0 |
| lowest finite difference | 64 | 70 | 6 |
| marked constructors | 64 | 190 | 6 |
| marked nonfixed moves | 2 | 60 | 68 |
| ordered mult mark involutions | 64 | 1186 | 6 |
| ordered token involutions | 64 | 1380 | 6 |
| pair criterion | 70 | 70 | 0 |
| pair local sign and closed formula | 64 | 190 | 6 |
| property black inner separator | 6 | 6 | 0 |
| property has pair | 64 | 64 | 0 |
| property m=1 | 54 | 54 | 0 |
| property m=2 | 9 | 9 | 0 |
| property m=3 | 1 | 1 | 0 |
| property minimal cover without good pair | 2 | 3 | 0 |
| property white inner separator | 9 | 9 | 0 |
| recovery image | 67 | 329 | 3 |
| recovery injectivity | 64 | 522 | 6 |
| sampler exact probability | 2 | 5 | 0 |
| sampler seeded chi square | 2 | 3600 | 0 |
| saved running referees | 1 | 2 | 0 |
| saved small census referees | 2 | 132 | 0 |
| signed height moments across paths | 64 | 278 | 6 |
| state disk W=B+1 | 70 | 726 | 0 |
| two matroid common bases | 1 | 6 | 0 |
