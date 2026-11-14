# Code for induction-completion

Own implementation. It imports nothing from `research/2026-11-14_opus_route-induction` and nothing from `workings/barnette_lab` except the plantri 4.5 executable `workings/barnette_lab/vendor/plantri.exe` (generation only). Python 3, standard library only. Run everything from this directory.

| File | What it does |
| --- | --- |
| `et.py` | plantri reader, faces and 2-colouring, rooted instances, backtracking enumeration of states and tree matchings (union-find with undo), pair test by max-flow, simplicity, separating triangles with inner colour, degree-4 set-ups, contraction |
| `census.py` | every rooted degree-4 contraction: direct count of `TM(T/M)`, outer-state patterns, lift criterion, rotation, exceptions, state splitting, pair criterion, (G) |
| `check_refuted.py` | the stated counterexamples of `failed_inductions.json` |
| `nolift.py` | contractions in which no tree matching of `T/M` lifts directly |
| `residual.py` | classification of the exception rows |
| `signs.py` | signs `eps(r_s, s)` of the tree matchings of `T/M` by class |
| `onesided.py` | which contractions keep a pair, per non-root degree-4 vertex; (G) and one-sided vertices |
| `superadd.py` | `#TM(T) >= #TM(T/M) + #TM(T/N) - |E_M| - |E_N|`, `|E_M| = |E_N|`, exception fractions |

## Commands that produced `data/`

```
python census.py 6 13 ../data/census_6_13.json --states 13 --exc ../data/exceptions_6_13.jsonl          # 1 s
python census.py 14 17 ../data/census_14_17.json --states 16 --exc ../data/exceptions_14_17.jsonl > ../data/census_14_17.log   # 90 s
python census.py 18 18 ../data/census_18.json --exc ../data/exceptions_18.jsonl > ../data/census_18.log   # 240 s
gzip ../data/exceptions_14_17.jsonl ../data/exceptions_18.jsonl
python check_refuted.py > ../data/check_refuted.txt
python nolift.py 18 ../data/nolift_18.jsonl > ../data/nolift_18.log                                       # 4 min
python residual.py ../data/residual_summary.json ../data/exceptions_6_13.jsonl ../data/exceptions_14_17.jsonl.gz ../data/exceptions_18.jsonl.gz
python onesided.py 8 16 ../data/onesided_8_16.json                                                        # 5 s
python onesided.py 17 19 ../data/onesided_17_19.json --c4 > ../data/onesided_17_19.log                    # 3 min
python superadd.py 6 17 ../data/superadd_6_17.json                                                        # 1 min
python signs.py 8 15                                                                                      # output quoted in RESIDUAL-CASES.md section 4, not saved
```

`census.py` prints one JSON line per `V`. Fields: `contractions`, `simple`, `loops`, `L_fail` (contraction inequality), `pattern_vs_direct_fail` (two counts of `TM(T)` and `TM(T/M)` disagree), `split_checked`, `split_fail` (state splitting, only up to `--states`), `criterion_fail` (pair iff no black-inner separating triangle), `pair_iff_TM_fail`, `TM_odd`, `some_lift_fail` (`T/M` has tree matchings and none lifts), `lift_fail`, `local_condition_fail`, `rot_ok`, `rot_exc`, `rot_exc_rootfree`, `rot_criterion_fail`, `nosep_rooted`, `G_fail`, `pair_lost_simple`, `old_lemma_fail_simple`.

Instance ids: `V`, `gid` = index in the output of `plantri -b -a V`, vertices 0-based (plantri letter `a` = 0), root `t0` as a vertex triple. With `--c4`, `gid` is the index in `plantri -bc4 -a V`.

Validation of the code. Two independent counts inside `census.py` agree on every contraction. The totals agree with the author's published numbers in every case I compared (344,872 contractions, 131,336 simple, 7,386 instances for (G), 21,848 rooted instances, 13,210, 7,510, 28,189, 466).
