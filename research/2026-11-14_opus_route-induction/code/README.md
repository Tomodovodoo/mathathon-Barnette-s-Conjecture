# Code for route-induction

Own implementation (does not import `workings/barnette_lab` except in `check_lab.py`). Needs Python 3, numpy (for `exp_skein.py`), networkx and sympy only for `check_lab.py`, and the plantri executable at `workings/barnette_lab/vendor/plantri.exe` (plantri 4.5, see `workings/barnette_lab/README.md`).

Run everything from this directory (`research/2026-11-14_opus_route-induction/code`).

| File | What it does |
| --- | --- |
| `tri.py` | Triangulations as faces plus side gluing (multigraphs allowed), rooting, states, `Q_s`, tree-matching test, unique mate and sign, `D`-sets, cycles, white faces inside a cycle, invariants, degree-4 contractions (`contractions`), inverse P-operation (`p_reductions`), plantri reader |
| `check_lab.py` | Cross-check of #states, #pairs, #TM against `workings/barnette_lab` |
| `exp_contract.py` | E1: every rooted degree-4 contraction, with lift statistics |
| `analyse_contract.py` | Laws, identities and first counterexamples from E1 rows |
| `rho.py` | The rotation of PROOFS Prop. 3.2 on all failing lifts |
| `probe_injection.py` | Distances from failing lifts to N-type TMs; existence of injections by short moves |
| `exp_misc.py` | E2 good contractions, E3 P-reductions, E4 local hypotheses |
| `exp_skein.py` | Least-squares skein fits; octahedron insertion |
| `quick.py` | Smoke test: pair exists iff TM exists, `V <= 14` |

## Commands that produced `data/`

```
python check_lab.py                                     > ../data/check_lab.txt         # 438 instances, 0 differences
python exp_contract.py 6 16 ../data/contract_6_16.jsonl # ~70 s
python exp_contract.py 17 17 ../data/contract_17.jsonl  # ~190 s, log in ../data/contract_17.log
python analyse_contract.py ../data/contract_6_16.jsonl ../data/contract_17.jsonl > ../data/analyse_6_17.txt
python rho.py 8 15                                      > ../data/rho_8_15.txt
python probe_injection.py 14 0                          > ../data/probe_injection_14.txt
python exp_misc.py 6 15                                 > ../data/misc_6_15.jsonl
python exp_skein.py ../data/contract_6_16.jsonl 13      > ../data/skein_oct.txt
```

The two large row files are committed gzipped (`*.jsonl.gz`). Run `gunzip -k` on them before `analyse_contract.py` or `exp_skein.py`.

Row format of `contract_*.jsonl`: `V`, `gid` (index in `plantri -b -a V` output), `t0` (face index in `tri.from_rotation` order), `x`, merge `q -> p`, `o1, o3` (the other two neighbours), `rootnbrs`, `simple`, `T` and `Tp` (invariants: states, TM, TMpos, TMneg, D, pairs, cmin, Nmin, lc), and the lift counts `A, B, C, b, LC, LCbad, liftOK` explained in the docstring of `exp_contract.py`.

`data/failed_inductions.json` is written by hand from these outputs. Each entry gives the instance id and the range.
