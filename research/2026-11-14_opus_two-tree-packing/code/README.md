# Code: exact commands

Run from `research/2026-11-14_opus_two-tree-packing/code` in Git Bash or PowerShell, one at a time. Python 3.14 with networkx. Plantri is the lab's `workings/barnette_lab/vendor/plantri.exe` (`-ba`, read only). `tp.py` is the library: rotation systems, faces, colouring, `W`, 2-factor enumeration, matroid partition into `k` forests (Edmonds, shortest augmenting paths; every positive answer is re-checked by union-find), and a max-closure density witness for failures.

| Command | Output | Time |
| --- | --- | --- |
| `python census.py 6 12 20` | `data/census_V6-12.json` (first timing run, 20 random maps) | 5 s |
| `python census.py 13 15 5 2` | `data/census_V13-15.json` (timing run) | 31 s |
| `python census.py 6 15 5 2` | `data/census_V6-15.json`, log `data/census_6-15.log` | 45 s |
| `python census.py 16 17 3 3` | `data/census_V16-17.json`, log `data/census_16-17.log` | 4 min |
| `python rainbow.py 6 13` | `data/rainbow_V6-13.json` (predictions 2-4) | 1 s |
| `python rainbow.py 14 17` | `data/rainbow_V14-17.json` | 2.2 min |
| `python referee_sol.py` | `data/referee_sol.json`, log `data/referee_sol.log` | 3 s |
| `python big.py 5` | `data/big.json`, log `data/big.log` | 21 s |
| `python tside.py 6 16 5 7` | `data/tside_V6-16.json` | 7 s |

`census.py VMIN VMAX RANDOM SEED`: all rootings of all plantri Eulerian triangulations; every pair support (2-factor of `B`) is tested for a split into two spanning trees of `W`, the tree matchings of its group are counted, and `RANDOM` random deleted-corner maps are tested. Flagged rows (any failure, or a group without a tree matching) are saved with their rotation system.

`rainbow.py`: inside every pair support, brute force over the `2^n` one-per-block choices for face blocks and point blocks; records existence of a rainbow tree, of a split into two rainbow trees (P1, P2), of a split that is a pair of tree matchings, and whether `W` minus the triangle of `t0` is three spanning trees.

`referee_sol.py`: replays the probabilistic folder's 278 cases and 27 certificates (see `REFEREE.md`). The lab is imported only to reproduce that folder's root choice and face numbering.

`big.py`: large and adversarial instances, and the exact failure rule of PROOFS Proposition 2.3. Uses the counting-families constructors `tube`, `stack`, `subdivide` read only.

`tside.py`: PROOFS Theorem 2.7, packing of `E(T) - E(t0) - D_u` into two spanning trees of `T/R`.

All results are `COMPUTED` (T4). The packing algorithm and the brute force in `rainbow.py` agree on every support where both run (both report a split for all 14,881 supports), which is an internal cross-check, not an independent implementation.
