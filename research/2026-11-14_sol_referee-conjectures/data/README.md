# Certificates and provenance

`COMPUTED`. All exact commands are in `../code/README.md`. JSON files contain finite results, not universal proofs. `provenance.json` hashes the scripts, saved outputs and principal graph inputs. Timing fields vary between replays.

Start with `v18.json` for the audited C2 witness and `R2_glued_V33.json` for the new R2 refutation. Their element IDs index the `entries` lists. `lower` and `upper` are exact Hasse neighbors, `ideal` lists join-irreducible element IDs below that orientation, and `phi` uses the indexed `hfaces` with the unique 12-side outer face normalized to zero. A factor's `tree_pairs` counts successful directions of all its D-cycles. The second V=33 implementation checks all state pairs without consuming those verdicts as input.

`r5_input.json` preserves the regenerated V=70 rotation and root. `r5.json` is the independently reproduced 654/1410 minority example. `examples.json` stores the exact signed Laurent polynomial under independently chosen unit-face spoke weights; it also stores the ordinary lattice rank polynomial so the two can be compared without conflating their variables.

The `census` and `fast_census` files count every facial rooting separately. The slow census and fast census agree through V=18, despite using all-state-pair enumeration and factor enumeration respectively. The compiled counter has zero inputs at V=7; its wrapper records that empty row at the requested order.
