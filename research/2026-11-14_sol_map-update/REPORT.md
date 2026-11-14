# Report

The map now contains 226 routes, up from 186, with 67 retained refutations.
The labyrinth has 334 nodes and 22 state-of-the-art rows; validation and dashboard build pass.
C1 coverage is separated into all-root dual order 22 and separator-free order 24; the complete value frontier remains at 16.
The merged main theorem now has an independent AI referee; the primal normalization disagreement and pending reviews remain explicit.
No new theorem or human check is claimed by this integration; large censuses were attributed and spot-checked, not repeated.

## What I set out to do

Bring the route figures, catalogue, labyrinth and reader guides up to date from research/INDEX.md and the named late runs. Ownership was limited to this folder, digestions/route-map/, labyrinth/, and steps 00 and 09. I read BRIEF.md, the project README, the named skills and schema, the prior map-maintainer and digestion-auditor reports, the generator and the incoming author/referee reports. No agents were spawned. No paper, proof, atlas or other digestion files were edited.

## What changed

The catalogue retains lattice C2 and R2 as refutations, the independently certified C2 minimum at 18, the two-implementation R2 witness at 33, and the larger R1/R3/R5 witnesses at 24/60/70 without pretending the latter sizes are minimal. The lattice sum is explicitly not a base-lattice rank polynomial. Linear testing of a pair is separated from selecting directions on a factor.

Cycle-cover entries include the unreviewed primal component formula, separator-free unbounded-c_min construction, one- and two-cover counting results, failed fixed-level connectivity, and the order-24 census. The finite ranges distinguish all roots from 4-connected inputs. New proofs from a referee's own work stay T2 unreviewed; AI review never promotes a tier.

Induction entries include every one of the thirteen failed schemes, the independently AI-refereed local propositions, the direct-lift refutation at 18, and the remaining ML1 and ML2. The one-sided extension is new referee work, not independently refereed. Rainbow entries include the reviewed original topology claims and the unreviewed Rado-Euler criterion, unique-factor completion, reversible-walk involutions, exchange-X evidence and periodic-walk failure. Probability entries record mean fitting, joint support convexity, zero-location failures and the packing question with exact rounding still separate. Pfaffian entries record the conditional GSW chain, one-step trisum interface and Heawood's cancellation-with-zero-total failure. The older parity identification stays refuted; through-edge follows from avoidance.

The three written routes are individually tracked. The merged theorem route's late referee says FOLLOWS and proposes eight ancillary edits. I did not certify their application. The involution text remains under review. The earlier primal proof is AI-refereed; its revision disputes M4 by simplifying the claimed phase ratio to i^n. That revision and dispute do not acquire a fresh referee merely because the earlier version had one. The upstream Lean local build is recorded as machine checking of its formal theorem.

The figures were regenerated from routes.py. Probability and lattice have their own matrix columns. The detailed map needed a wider identifier column, shortened display titles, protected list backgrounds and more top margin. Full titles remain in the generated Markdown and JSON. The overview, detailed raster and matrix were inspected; labels that had been crossed by dense bypass strands were repaired. The matrix cells show supplied proof, open and refuted counts, not a count of human-established results.

Step 09 was rewritten around precise open statements, finite evidence, failed substitutes and concrete tests, with an unsigned graveyard. The overview and HOW-IT-WORKS explain c_min, current written routes and the merged paper's local signs, face-path heights and inside-cycle connectivity lemma. The 213-object older audit and 279-object new involution fixture remain distinct pending a direct convention comparison.

## Current counts

| Route status | Count |
|---|---:|
| LIT, source provenance, including unrefereed preprints | 46 |
| PROVED-HERE, T2 with claim-specific review | 57 |
| COMPUTED, T3 or T4 as specified | 12 |
| CONJECTURE | 19 |
| HUNCH | 25 |
| REFUTED | 67 |
| Total | 226 |

The graph has 334 nodes. There are 19 open conjectures, 25 live hunches, 67 dead ends and 11 open question nodes. The full invariant-value frontier is fully resolved at every represented size through 16. Larger displayed resolved fractions are 9.23% at 17, 5.36% at 18, 3.08% at 19, 1.78% at 20, 1.03% at 21, 0.59% at 22, 0.34% at 23 and 0.20% at 24. These fractions classify possible tree-count values, not the fraction of roots tested. No larger spectrum was silently certified by a C1 inequality census.

The all-root C1 replay reaches V=22 on 9,531,638 roots, 4,656,948 feasible. The separate 4-connected census reaches V=24 on 23,824,742 roots. Its C1, equality-pattern and c_min-distribution evidence remains T4 under review. `frontier.json/statistic_coverage` records exactly these scopes and the sources. The original scatter still displays the feasible-root sample through 16.

## Verification and reproducibility

From the repository root, the successful commands were:

```
python -X utf8 -B digestions/route-map/build_map.py
python -X utf8 -B labyrinth/make_frontier.py
python -X utf8 -B labyrinth/seed.py
python -X utf8 -B labyrinth/lab.py check
python -X utf8 -B labyrinth/lab.py build
python -X utf8 -B research/2026-11-14_sol_map-update/validate.py
```

The dashboard is `E:\Personal\Math\mathathon\barnette-s-conjecture\labyrinth\dashboard\index.html`, recorded in labyrinth/README.md. It builds locally. No interactive browser audit or publication is claimed.

`spotcheck.json` records an independent reconstruction of the V=33 order from stored face potentials. It finds sixteen elements, ten R2 candidates, zero successful candidates and total 144 tree pairs. Aggregate census root arithmetic was independently checked. These checks inspect retained certificates; they do not independently enumerate the 33-vertex states or rerun the large censuses. Local Markdown links in the maintained guides all resolve. The original events were preserved append-only and SOTA history is preserved across regeneration.

The Python update scripts in this folder are historical one-shot edits and must not be rerun over the final generator. `validate.py` is a repeatable check. The authoritative regeneration commands are the ones above. `add_failures.py` also produced spotcheck.json during this run; it mutates routes.py and is historical too.

## What failed and why

The first detailed render had long route identifiers running into labels, and dense bypass strands crossed the inside-cycle list and overview labels. The repair separates columns, shortens only display titles, reserves source width and puts opaque backing behind lists. An initial backing hid route markers because its drawing order was too high; the final drawing order leaves markers visible above it. The mathematical route inventory was not shortened.

Several requested incoming results are still absent at the final report scan, saved in validation.json. There is no REPORT.md in astra_induction-lemmas or opus_two-tree-packing. The latter has a draft PROOFS.md announcing a theorem, but the task explicitly gated integration on its report, so I did not treat that live draft as a finished result. The involution referee and second merged cold read also have no REPORT.md. The first merged referee did arrive and was integrated. These limits are material; the map is a dated snapshot rather than a claim that active research has stopped.

## Ten best open doors

1. C1 and its equality converse. Exclude the exceptional two-cover overlap, then extend the shared-state calculation.
2. ML1, a simple pair-preserving degree-four merge. Referee the tight-set reduction and close its short-cycle obstruction argument.
3. ML2, two-sided lifting. Find an injection from exceptional to non-exceptional matchings, allowing rotation.
4. C3. Search for closed positive-Q-cycle plateaus in the allowed exchange graph, or prove they have exits.
5. Rainbow exchange X. Relate its plateau components to pair exchange components and account for periodic surplus walks.
6. Two-tree packing, then exact rounding. Await the finished packing report and independently referee its density argument; do not conflate packing with a doubly constrained tree.
7. Direction selection for a fixed factor. Exploit the special forbidden-cycle clauses; a linear test of an assignment is already available.
8. A determinant or Pfaffian without coefficient extraction. Test local signatures before asserting global positivity.
9. The forest-pair recovery image in G alone. Separate the compatible-state theorem from the stricter forest-pair image.
10. Verification. Re-referee the primal M4 disagreement and new rainbow/cycle-cover lemmas; obtain a human check of the current expositions.

A further structural question, now sharper, is whether c_min is unbounded among separator-free Goodey graphs with bounded primal face sizes. The known new family has growing pole degrees.

## Three best next steps

1. Re-scan the four pending reports and integrate only their finished verdicts, with new claim-specific review states.
2. Independently referee the separator-free forcing family, two-cover overlap and rainbow R/S/X4 proofs. They were newly discovered by authors or referees and remain unreviewed.
3. Give a human the merged referee's eight edits and the primal phase dispute, then compare the 213/279-object conventions on the same fixed fixture.

## Git

The first stable commit is b62d081. All commits are path-scoped to the assigned files. The final report-and-render commit and push outcome are recorded in the final response. No unrelated working-tree files were staged.
