# Changes checked against the referee

PROVED-HERE marks written arguments; COMPUTED marks finite checks; REFUTED preserves the one rejected referee assertion. The implementation owns only proofs/primal/ and this research folder. No paper/ file was edited.

| Requested item | Verification | Final change |
| --- | --- | --- |
| 1. Lemma 3 boundary signs | PROVED-HERE. For e=bw with g to its left, its coefficient in boundary(g) is +1 and in boundary(f) is -1. Reversing the transition reverses both. Pairing the circuit vector with boundary(f_i) gives delta-in squared minus delta-out squared. | Inserted the coefficient identity and displayed inner-product calculation in Markdown and TeX. |
| 2. Global delta convention | PROVED-HERE. Independent vertex reversals would destroy the coefficient identity. | Required the same sphere-induced cyclic sense at every black vertex. |
| 3. Lemma 2(b) deletion | PROVED-HERE. Each deleted edge has both sides among U_S; distinct-face deletion merges, same-face bridge deletion and isolated-vertex deletion preserve the global face count. | Added the explicit accounting sentence. |
| 4. Hypothesis ledger | PROVED-HERE. A parallel pair leaves at most two outgoing edges from its two ends; the deficient cut is positive and divisible by three; 3-edge-connectivity supplies 2-connectivity in Lemma 1. | Corrected all three entries, including caps and the role of three distinct cut ends. |
| 5. Planar background | PROVED-HERE relative to Euler. Checked dart splicing, coherent signed boundaries, inherited subgraphs, bridge deletion and isolated vertices. Vertex splitting counts facial walks componentwise, not global faces. | Chose oriented genus-zero maps; Euler is the sole imported planar theorem. General circuit-cut argument now precedes Lemma 1. |
| 6a. Missing Lean citations | Source-checked make_coloredDual at ThreeCuts.lean:101 and cap_duality at CappedDuality.lean:148. | Added both and explained the map-rule replacements. |
| 6b. One-way circuit_cut | Source-checked FlowCircuits.lean:71 and Bonds.lean:109. | Added bond_of_circuit and separated the note's converse from Lean's kernel-duality connectivity proof. |
| 6c. Lemma 3 scope | Lean uses oriented incidence matrices; the local map boundary-coefficient argument is this note's proof. | Removed the restatement category; named ColoredDual.oriented and Triangle.index_delta. |
| 6d. Phase dependence | REFUTED. The referee's ratio (-1)^((n+3c)/2) i^c equals i^n. Directly t=sum delta is divisible by three, epsilon=i^(n-t), phase=i^(t/3), hence epsilon/phase=i^n. Read the actual phase and rawIndexSum definitions in PairPhases.lean. | Corrected the referee rather than inserting its erroneous conclusion. With aligned signs and weights the sums are constant multiples. Added proof and 21,576 finite pair checks, including the running example. |
| 6e. General Lemma 12 | Source-checked selected_forest at ForestMatching.lean:338. Reread the informal proof: no partner or forest is used. | Statement now covers any state and compatible perfect matching. The root edge is the matching's edge at b0. |
| 7. Three observations | PROVED-HERE. Rootward orientation gives the partner criterion and uniqueness. The face forest of a matching with connected complement gives a unique compatible state; cut parity separates the root faces. | Remarks 14 and 15 contain full proofs. Recorded referee's original finite ranges and compared the incidence-tree criterion in the structure integration report. |
| 8. Cancellation coverage | COMPUTED. Dedicated checker, all roots and states in plantri -ba census at 15 and 16 dual vertices; all 22 roots of running.json. | 307 additional cancelling states at 15/16 faces, 614 reversals, no failures. Running example gives four states and eight reversals across all roots. |
| Figures | COMPUTED. Rebuilt primal rotations from shared input, identified face labels, checked pairs, disk counts, path flow, forest recovery, matching, Hamiltonian cycle, glued cut and cube pieces. | Eight standalone source/PDF/PNG figures plus checked.json. All drawn graph edges are edges of G; incidence segments terminate at face labels. Natural-size panels occupy 0.48 textwidth. |
| Dictionary | LIT for terminology, PROVED-HERE for identifications. Read the local source texts and Lean headers. | DICTIONARY.md and one PDF page, covering G, T and the four source vocabularies. |
| Build and audit | COMPUTED for build; PROVED-HERE for bounded audit. | A4 amsart, one-inch margins, 15 pages, no errors, undefined references or overfull boxes. Every page rendered and inspected. AUDIT.md gives FOLLOWS. |

## Other referee details

Added that the two neighbours in Lemma 4 belong to A and that the reduced positive-deficit set is nonempty. The subgraph rule justifies k>=1. Replaced the unnecessarily strong four-vertex facial-cycle bound with the two-vertex bound actually needed. Stated independence of the cap rotation from the contracting spanning tree. Kept the extra white=black+1 identity. Moved the long exact data dump to the already-existing EXAMPLES.md supplement; the main note now ends with the new remarks and figure appendix.

## Visual corrections

The first render clipped b0; expanded the bounds. The first cap-piece label incorrectly marked the old root; the cap is now found by its actual three boundary faces and asserted. The dictionary initially used code formatting for whole cells containing underscores; restricted it to declaration names. Reviewed the final layout after those fixes. The graph drawing follows the shared curved layout, so the cube is shown in its dual-derived embedding rather than square-in-square form.

## Workflow limits

The PDF skill's container marker command was attempted and failed because container_tools/mark_artifact_operation_started.mjs is absent in this Windows repository. This affects telemetry only; compilation and rendering used installed MiKTeX and PyMuPDF. No human approval was needed. The proof is not newly machine-checked. No subagents or new referee were invoked. The first referee's verdict and this revision's self-audit are distinct review events.
