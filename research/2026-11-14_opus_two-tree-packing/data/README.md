# Data

Every file is produced by the command recorded in its `command` field (see `../code/README.md`).

- `census_V6-15.json`, `census_V16-17.json`: exhaustive census, all rootings, `V <= 17`. `summary` per order; `flagged` lists every rooted instance with a failure or a group without a tree matching (only failures of random maps in instances without a pair, plus the `V = 16` bad-cover instance, index 27, outer face 0).
- `census_V6-12.json`, `census_V13-15.json`: earlier timing runs with other random counts; superseded by `census_V6-15.json`, kept for the record.
- `rainbow_V6-13.json`, `rainbow_V14-17.json`: one-sided rainbow trees inside supports, P1, P2, tree pairs with both states trees, three-tree packing of `W - Δ_{t0}`.
- `referee_sol.json`: replay of the probabilistic folder's 278 cases and 27 certificates.
- `big.json`: large and adversarial instances, failure-rule agreement.
- `tside_V6-16.json`: the `T/R` packing.
- `counterexample_nonpair_V9.json`: smallest failing deleted-corner map (not a pair; the rooting has no pair), with its rotation system, faces, the map `u`, the support edges in `W` and a dense white-face set `S` with `|F[S]| = 2(|S| - 1) + 1`.

There is no counterexample to the packing conjecture as stated: it is a theorem (PROOFS Thm 2.1).
