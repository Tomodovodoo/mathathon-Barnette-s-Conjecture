# Audit of the atlas repair

GPT-6.1 Sol, 2026-11-14. Scope: pages 24, 26, 29 and 30, the repair report and changelog, and the later page-24 wording. I own only this folder and `digestions/atlas/`. No subagents. The audit checks the atlas against supplied project sources, not the truth of the entire proof or every Lean declaration. No graph census was rerun. `COMPUTED` below means either the independent saved-data reconciliation in `recheck.py`, or a quoted computation with its original script and range explicitly identified.

## Page 29

Verdict: correct, unchanged. COMPUTED by `recheck.py` from `proofs/blueprint/blueprint.json`, selecting the 34 distinct IDs in `analysis.skeleton`, then grouping node statuses. The script does not use the stored aggregate count or import an atlas figure function. It compares each ID's class against the route row in `research/2026-11-14_opus_lean-integration/STATUS-TABLE.md`, then against the atlas certificate. The four groups are:

| Class | Count | IDs |
| --- | --- | --- |
| exact | 5 | `def:pair`, `def:state`, `lem:difference`, `lem:reversals`, `txt:flow` |
| after an unformalised translation | 17 | `def:selection`, `eq:counts`, `eq:hall`, `lem:cap`, `lem:disk`, `lem:dual`, `lem:duality.1`, `lem:sign`, `prop:good`, `prop:pair`, `prop:recover`, `prop:target.1`, `thm:T`, `txt:D`, `txt:delta`, `txt:inside`, `txt:two-faces` |
| weaker or different | 10 | `def:good`, `lem:Y`, `lem:cancel`, `lem:duality.2`, `lem:good`, `lem:height`, `lem:outdegree`, `lem:partner`, `thm:main`, `txt:heights` |
| no counterpart | 2 | `lem:connected`, `prop:target.2` |

COMPUTED. Every named node in panel a has the corresponding fill/outline, with labels supplied by `BP_SHORT`. The five dark nodes are state, pair, reversals, finite difference and max-flow. The two dashed nodes are connectedness and two trees. Heavy outlines identify precisely the ten weaker/different IDs above. The legend, segmented bar and prose all say 5/17/10/2. The existing build also checks the advisory 5/27/2 recount statement by statement after merging translation and weaker. This is a check of the table's representation, not a fresh semantic audit of the Lean source.

The six-lemma qualification of "no polynomial" agrees with `proofs/lean/README.md` and `research/2026-11-14_astra_lean-check/REACHABILITY.md`. General polynomial algebra is explicitly retained in the page text. The provenance sentence still correctly describes the original blueprint author's four-way curation and the earlier checker's three-way recount.

## Page 30, every open bar

All entries here are COMPUTED finite evidence, not theorems beyond their ranges. Numbers are dual order V. FACTS means `research/2026-11-14_opus_reconcile/FACTS.md`.

| Statement | Two programs / one program / samples | Verdict and source |
| --- | --- | --- |
| counting bound on every feasible root | 22 / 22 / 100 | Keep. FACTS; `sol_referee-conjectures/REFEREE.md` h1 and census table, independent `code/count.cpp`; `opus_conjectures/CONJECTURES.md` section 5 and `code/bar.c` supply samples. The source count is 9,531,638 roots, 4,656,948 admitting a pair. The bound uses the minimum number of cycles over existing covers. |
| same bound without separating triangles | 16 / 24 / none | Keep. FACTS; `astra_cycle-covers/REPORT.md`, `sol_referee-covers/REFEREE-covers.md`, 3,374 rooted occurrences through 16. |
| pair descent, never increasing Q-cycle count | 20 / 23 / 200 | Correct sample endpoint, previously 150. FACTS; `astra_referee-descent/REPORT.md` and `code/c3_6_19.json`, `code/c3_20_20.json` give 3,373,400 pairs through 20. `fable_descent/REPORT.md` and `code/descent.cpp` give 193,623,384 through 23. See sampling discussion below. |
| rainbow exchange descent | 12 / 17 / 120 | Keep. FACTS; `opus_referee-rainbow/REPORT.md`, own `code/stepx.py` through 12; `fable_referee-topology/REPORT.md`, `code/exp_rainbow.py` through 17 and samples to 120. Partial order-18 coverage is not an exhaustive endpoint. |
| some contraction keeps a pair, no separating triangles | 19 / 19 / none | Correct solid endpoint, previously 17. `fable_induction-completion/REPORT.md`, `code/census.py` and `astra_induction-lemmas/G.md`, `code/g_structure.py`. Added the separator-free restriction to the chart label. |
| a contraction has at most the original good-state count | 18 / 18 / none | Correct solid endpoint, previously 17. Fable's `code/census.py` checks the inequality directly; Astra's `code/induction.py` checks sufficient inequalities through 18. See bounded dependency audit below. |

COMPUTED. `recheck.py` sums Astra's saved G output `data/g_structure_8_19.json` to 62,416 rooted instances. Inspection of `g_structure.py` resolves the repair's uncertainty: after collecting the flow-and-simplicity result of both merges at every nonroot degree-four vertex, it explicitly executes `if nv>6: assert any(any(v) for v in good.values())`. This is exactly the existential statement, in addition to the short-cycle classification test. Thus 17 is not the right endpoint. The range is 8 through 19 on separator-free inputs, including both face-colour choices.

Implementation boundary: Astra's `common.py` imports Fable's `et` for parsing, setups, contraction, simplicity and flow. The flow assertion alone is therefore not an independent second algorithm. The second computation is Astra's chordless-cycle enumeration and embedded-side classification: its `ws` is computed from the original embedding, then `assert bool(ws)==(not simple or not pair)` checks every merge. Together with the existence assertion, this also checks existence by the structural criterion, not just by rerunning Fable's flow. That geometric computation is the reason to count two programs through 19. They share enumeration/setup infrastructure; this is not a clean-room implementation. The chart's program independence concerns the structural versus flow test, and should not be read as independent input generation.

COMPUTED, quoted samples. The older 150 endpoint was supported, not fabricated: `opus_conjectures/CONJECTURES.md` section 6, `code/c3.py` and `data/c3_random.txt` report 940 successful starts through 150. But it is no longer the largest supported sample. `fable_descent/REPORT.md` and `DESCENT.md` sections 3 and 6 report 27,660 sampled strict local minima through 200. Its `code/walk.cpp` function `monotone` rejects every move increasing k. `data/walk_random_B.txt` has a completed order-200 summary with 99 sinks, zero C3 failures and zero caps; the completed insertion order-200 summary in `walk_random_A.txt` has 3,823 sinks and zero failures/caps. Order 300 has three capped, undecided searches. The new endpoint is 200, not 80, which is the author's all-pairs-on-random-graphs range, and not 300. The chart now rescales its logarithmic axis to 200. The source entry names the sampling scope and the caps.

### Bounded dependency audit of the contraction inequality

I applied the repository reverse-Lamport method to this specific implication. Boundary: finite rooted contractions tested by Astra through 18. Accepted inputs are the saved computation and the rotation/counting argument reviewed in `astra_referee-descent/REFEREE-induction.md`. This does not assume a universal half-exception theorem.

Write U for the number of good states upstairs, M and N for the two contracted counts, and e for the common exception count. The supplied route is:

```text
C0: U >= M and U >= N
  <- R0 AND(C1: U >= M+N-2e, O1: 2e <= M, O2: 2e <= N)
C1 <- R1 AND(O3: rotation bijects exception sets,
             O4: successful direct and rotated images are disjoint)
```

PROVED-HERE, elementary implication conditional on those inputs: O2 gives M+N-2e >= M; O1 gives M+N-2e >= N. Combining with C1 proves C0. This is the chart's inequality for either contraction.

| ID | Obligation | Needed by | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- |
| C0 | both one-sided count inequalities | root | major claim | R0 | discharged in the finite scope |
| C1 | two-sided counting inequality | C0 | proved earlier | referee counting section; code `inequality_fail` | discharged |
| O1 | half bound for M | C0 | hypothesis, finite computational input | `half_fail` checked on each merge | discharged through 18 |
| O2 | half bound for N | C0 | hypothesis, finite computational input | same loop, other merge | discharged through 18 |
| O3 | equal exception counts via rotation | C1 | proved earlier | referee rotation section; `bijection_fail` | discharged |
| O4 | disjoint successful images | C1 | proved earlier | referee counting proof | discharged |

Verdict: FOLLOWS within the finite range. COMPUTED by `recheck.py`: saved `code/induction_6_16.json` and `code/induction_17_18.json` sum to 1,202,792 contractions and 7,940 exceptions, with zero half, bijection and inequality failures. The V=7 output has no graphs and no counters; it is not a missing nonempty case. The repair correctly noticed that C1 alone differs from the chart statement, but missed O1 and O2. These are also explicitly checked by the referee's program, so the stronger conclusion is justified through 18. Beyond that range the half bound remains CONJECTURE, with a test to extend the same census.

## Page 30, every counterexample cross

All rows are COMPUTED quoted witnesses. FACTS and the named reports support the following unchanged values. A circle means smaller cases were exhaustively checked, not that an uncircled witness is known nonminimal.

| Statement | V | Circle? | Authority |
| --- | --- | --- | --- |
| highest partnered state good | 12 | no | FACTS; `astra_referee-combinatorics/REPORT.md`, reflections included |
| an extreme cover good | 18 | yes | FACTS; `sol_referee-conjectures/REFEREE.md`, all-root census through 18, 26 failures at 18 |
| some contracted good state directly lifts | 18 | yes | FACTS; `fable_induction-completion/REPORT.md`, `code/census.py`, 50 contractions at 18, none below |
| a cover one step from an extreme good | 24 | no | `sol_referee-conjectures/REFEREE.md` g1 and witness section; `opus_conjectures/CONJECTURES.md` R1 |
| extreme or irreducible cover good | 33 | no | FACTS; `sol_referee-conjectures/REFEREE.md`, gluing witness |
| every maximal chain meets a good cover | 33 | no | same witness and report, improves the older order-60 example |
| half the covers good | 33 | no | same witness and report, improves the older order-70 example |
| evict walk never repeats | 38 | no | FACTS; `fable_referee-topology/REPORT.md`, repeated by `opus_referee-rainbow` |

COMPUTED. The prose's three crosses at 33 and its two pair-census totals agree with the chart and source reports. Panel b still recomputes its running-example obstruction. No census value was inferred from the drawn example.

## Pages 24 and 26

Page 24 verdict: correct mathematical provenance distinction, wording made explicit. LIT, quoted from `astra_citation-audit/TEXT-FIXES.md` and `astra_older-approaches/SOURCES.md`: Stein's published article is *B-sets and planar maps*, Pacific J. Math. 37, 1971, 217-224, Theorem 2.2. Feder and Subi are read through ECCC TR06-015 and the readable author revision; Kelmans through Hertel and Alt, Payne, Schmidt and Wood. The original Kelmans paper was not opened. The coordinator's wording already avoided "all three published", but left the report unnamed and the unopened-original qualification implicit. The new text names both. The project translation remains explicitly unrefereed. I did not independently open those literature originals in this pass.

Page 26 verdict: correct, unchanged. FACTS and `fable_referee-families/DISAGREEMENTS.md` section 1 support the distinction between the same-model all-length proof check and a different-model finite count check. The latter's scopes differ by statistic: width four S to length 20, M/P to 14, H to 10; width six S/M to 12, P to 9, H to 6. The page prudently says "finite ranges" and makes no all-length claim for the different model. The direct enumeration pictured on the page is separate from those recurrence checks.

## Build and visual verdict

COMPUTED by `build.py` and the strengthened `verify.py`: 30 routes, 34 PDF pages. All page texts are 130 to 150 words and all figure widths are 0.80 to 0.95 of text width. The page-24 standalone table had two columns plus default intercolumn space wider than its 14.4 cm minipage. Reducing the second column from 12.0 to 11.8 cm removes the 3.46451 pt overfull box. The verifier now inspects standalone logs too.

I opened the rendered pages 24, 26, 29 and 30, plus the changed source pages. Labels remain legible and separated, both new solid endpoints and the 200 sample are visible, page 24's table wraps within its boundary, and all status prose and cross-references fit. A higher-resolution title crop confirms page 30's full title, despite poor rasterisation of the initial W at 110 dpi. No remaining overfull box was found. Commands and final measurements are in CHANGELOG.md and the generated JSON files.

