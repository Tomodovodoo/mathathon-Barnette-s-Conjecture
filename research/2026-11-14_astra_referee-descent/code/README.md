# Independent referee computations

Run commands from the repository root with Python 3.14. All outputs are written beside these scripts, inside the assigned referee directory. No author verification code is imported. Plantri 4.5 is the only census generator. NetworkX is used for ordinary planarity/connectedness in selected geometry and family scripts.

Commands and outputs:

- `python research/2026-11-14_astra_referee-descent/code/check.py 6 16` produces `census_6_16.json`.
- `python research/2026-11-14_astra_referee-descent/code/induction.py 6 16` and then `.../induction.py 17 18` produce the two induction JSON files. The latter run took about 512 seconds, with V=18 taking 426 seconds. Peak sampled working set was about 17 MB.
- `python research/2026-11-14_astra_referee-descent/code/witnesses.py` produces `witnesses.json`.
- `python research/2026-11-14_astra_referee-descent/code/potentials.py` produces `potentials.json`.
- `python research/2026-11-14_astra_referee-descent/code/all_potentials.py` produces `all_potentials.json` from the complete saved census witnesses. SINK means no strict improvement, not failure of weak descent. TRAP1 and TRAP2 mean no weak path with the indicated macro radius. The output preserves this distinction.
- `python research/2026-11-14_astra_referee-descent/code/induction_witnesses.py` produces `induction_witnesses.json`.
- `python research/2026-11-14_astra_referee-descent/code/structure.py deficiency 6 14` produces `deficiency_6_14.json`.
- `python research/2026-11-14_astra_referee-descent/code/structure.py structure 6 16` produces `structure_6_16.json`.
- `python research/2026-11-14_astra_referee-descent/code/contraction_formula.py` produces `contraction_formula.json` through V=14.
- `python research/2026-11-14_astra_referee-descent/code/families.py` produces `families.json`.
- `python research/2026-11-14_astra_referee-descent/code/adversarial_extra.py` produces `adversarial_extra.json`, including the actual saved V=33 instance.
- `python research/2026-11-14_astra_referee-descent/code/random_sample.py` produces `random.json`. Seed 714992, independent degree-four vertex splitting, five samples each at V=26,30,34 and one random facial root per sample. This is a biased insertion distribution, not uniform sampling of triangulations.
- `python research/2026-11-14_astra_referee-descent/code/recover40.py 21 22` regenerates the report's raw random input using Opus gen.py, model skew, V=40, count=40, seed=15, then independently checks graph 21. Only this raw generator is shared; none of its states, moves or conclusions are used. Output is `regenerated40.txt` and `recovered40_21_22.json`.
- `python research/2026-11-14_astra_referee-descent/code/minimal_regions.py` produces `minimal_regions.json` through V=16.
- `python research/2026-11-14_astra_referee-descent/code/manifest.py` records the source hashes at the checkpoint.

Implementation details relevant to independence:

`check.py` enumerates states as incidence bijections using minimum-remaining-domain recursion. An initial version tested disjointness between every pair of states; the final version enumerates partner bijections with the second-state incidences forbidden. The final rerun records agreement. The functional model generates cycles and exchanges; every complete exchange-graph run verifies move reciprocity. C3 is tested by reverse breadth-first reachability from all q=0 pairs.

`induction.py` does not use the functional model to decide goodness. It builds opposite edges and uses disjoint-set cycle detection and three distinct root components. Contraction preserves face identity. To find the rotation it tests the two cyclic permutations of assignments on the two local black faces and each possible third face, independently of the author's forest classification. It then checks the resulting state directly.

`structure.py` checks deficiency with induced rotation face walks, including repeated sides and the distinction between the two sides of a triangle. It checks the obstruction criterion against direct existence of two disjoint incidence bijections on the contraction, rather than assuming the pair criterion in code.

`potentials.py` computes enclosed white-face counts by flood fill across nonboundary edges. It integrates the signed increments over each exchange component and checks consistency at every edge. Its face-walk orientation is opposite the labels used by the report; both om and psi are negated once when evaluating those labels. This convention is fixed for all inputs. Reversing the embedding exchanges both height signs. The method checks increment integrability and the named potential traps, not a separate solution of the spoke-weight linear system.

All heavy runs were sequential. No run was intentionally allowed beyond ten minutes. JSON outputs report counts or exact certificates, not a proof of an unbounded claim. See the referee reports for unreplayed ranges and source limitations.

Additional completed checks and commands:

- `python research/2026-11-14_astra_referee-descent/code/covers.py` validates a second, cover-first enumerator against all incidence-bijection pairs through V=16; output `covers_validation.json`.
- `python research/2026-11-14_astra_referee-descent/code/recover40.py 0 40` performs a complete independent C3 replay on all roots of the 40-graph batch, writes `summary40_0_40.json`, and preserves complete replacement certificates in `recovered40_0_40.json`. It takes about 63 seconds with the cover-first enumerator. The earlier graph-21 run used matching-first enumeration and took about 162 seconds.
- `python research/2026-11-14_astra_referee-descent/code/signed_radii.py` produces `signed_radii.json` by bounded BFS with geometry-derived increments.
- `python research/2026-11-14_astra_referee-descent/code/height_minimality.py` produces `height_minimality.json`, complete through V=17.
- `python research/2026-11-14_astra_referee-descent/code/c3_census.py 6 19` and `.../c3_census.py 20 20` produce the extended C3 census and two-step escape checks.

The first minimal-region test included the octahedron, which is outside G's V>6 domain. The final script and output start at V=8. An attempted author-executable locator was abandoned because the shared executable had disappeared; it supplied no evidence. The radius-four witness was found by the new cover-first enumerator instead. The regenerated raw input is fully saved, so subsequent verification does not require that external generator.

Final certificate extensions:

- `python research/2026-11-14_astra_referee-descent/code/recover50.py` regenerates skew/50/12/6 graph 11 and checks the selected root's complete exchange components. `recovered50.json` replaces the truncated V=50 two-move size/area certificates.
- `python research/2026-11-14_astra_referee-descent/code/macro40.py` searches the saved 40-vertex raw batch for radius-two local optima of the eight signed three-entry potentials. Seven are found directly. It then calls `finalize_macro.py`, which reflects the eighth from its both-signs-reversed partner and verifies all eight radius-two balls; `macro40.json` contains full certificates. Running `finalize_macro.py` alone rechecks the saved certificates.
- `python research/2026-11-14_astra_referee-descent/code/cover_obstructions.py` uses the saved exception census only as an input index, reconstructs every listed contraction, independently enumerates all cover orientations, and records `cover_obstructions.json`. The complete independent induction census already validates the exception totals through V=18.
- `python research/2026-11-14_astra_referee-descent/code/outer_scope.py` searches for a state whose augmented outer graph is cyclic, recording `outer_scope_counterexample.json` for the qualification to RESIDUAL-CASES Proposition 2.
- `python research/2026-11-14_astra_referee-descent/code/random_separator_free.py` generates 20 new graphs at V=26,30,34,40 with eight random roots each, seed 714993, rejecting degree-four splits that create separating triangles. Output `random_separator_free.json` records all rotations and 1,160 checked pairs. This distribution is biased and has no strict-descent sinks.
- `python research/2026-11-14_astra_referee-descent/code/recover40.py 0 10` was the earlier partial search that produced `recovered40_0_10.json`; the complete 0-to-40 output supersedes it.
- `python research/2026-11-14_astra_referee-descent/code/final_checks.py` checks script syntax, parses every JSON, checks saved verification flags, aggregates the independent counts in `verification_summary.json`, and compares current source hashes with the checkpoint in `source-changes.json`. The final comparison reports no changed source files. This script does not rerun the expensive enumerations.
