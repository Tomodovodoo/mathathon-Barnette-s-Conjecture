# Revision report

The primal proof note is corrected, illustrated and rebuilt as a 15-page PDF.
All three referee observations now have informal proofs in Remarks 14 and 15.
The phase warning in referee M4 is false: the proposed ratio simplifies to i^n.
Cancellation checks add 307 states at 15/16 faces; all 614 reversals pass.
The final self-audit returns FOLLOWS; human review and a new Lean build remain pending.

## Task and ownership

The task was to revise the primal reconstruction against the independent Fable referee, increase cancellation coverage, add checked figures and a dictionary, rebuild the PDF, and repeat the reverse-Lamport audit. Only proofs/primal/ and research/2026-11-14_astra_primal-revision/ were written. The shared figure toolkit and referee checker were imported read-only. No subagents were used.

## Established

PROVED-HERE. Lemma 3 now contains the missing local boundary-sign calculation. The global orientation convention, face deletion, planar-map rules and hypothesis ledger are explicit. Lemma 12 covers every state-compatible perfect matching. The general circuit-cut argument precedes its use in Lemma 1. The supplementary proofs show that a forest state has a partner exactly when its three components contain one root each, that this partner is unique, and that a perfect matching has a compatible state exactly when its complement is Hamiltonian. That state is unique too.

REFUTED. Referee M4's circuit-count-dependent normalization. Its own expression equals i^n; the same result follows directly from Lean's phase definition. The aligned polynomials are constant multiples. CHANGES.md records this deliberate exception to the requested edits, with the full calculation also in STATUS.md and the proof note.

COMPUTED. At 15 faces: 57 graphs, 1,482 roots, 23,946 states, 72 cancelling states, 144 reversals and 4,816 phase checks. At 16 faces: 185 graphs, 5,180 roots, 103,488 states, 235 cancelling states, 470 reversals and 16,648 phase checks. On the current 13-face running example: 22 roots, 264 states, four cancelling states, eight reversals and 112 phase checks. Zero failed assertions. These are the plantri binary's generated inputs; no independent census certification is claimed. The dedicated run targets cancellation, not the full all-bonds checker.

COMPUTED. Eight figures show G and its face labels, a pair, a cut side with the four count values, flow and circuit weight, cancellation, matching and Hamiltonian cycle, a nontrivial three-cut and its two capped pieces. The cube and current running graph share the project's layout and encodings. Sources, standalone PDFs, PNGs, captions, assertions and checked objects are in proofs/primal/figures/. The running example has 22 primal vertices and 13 faces; the cube has eight vertices and six faces. The cut example has two seven-vertex shores and two cube caps.

COMPUTED. The final amsart PDF is A4 with one-inch margins, 15 pages, no LaTeX errors, no undefined references, and zero overfull boxes. All 15 pages and eight figure renders were inspected. A one-page dictionary links primal objects, dual objects, OpenAI, Li, the constructive paper and Lean. The exact old example data remain in EXAMPLES.md. README.md gives the build commands. The unslop pass removed stale status and audit prose and kept the mathematical qualifications explicit.

PROVED-HERE. AUDIT.md is the final bounded AND/OR dependency audit. It returns FOLLOWS for the supplied route, relative to finite graph algebra, integral max-flow and the stated sphere-map convention with Euler. It separately audits the two supplementary remarks and phase normalization. The independent Fable report applies to the earlier version; this revision has the author's verification, not a newly commissioned independent referee.

## What failed and why

The referee's M4 inference failed by elementary exponent simplification and was corrected rather than copied. The first figure pass clipped a root label and mislabeled the first cap; both were found by render inspection and fixed. An initial dictionary layout overflow was removed by ending its table paragraph explicitly. The PDF skill's telemetry marker is unavailable in this Windows workspace; the attempted command returned MODULE_NOT_FOUND. The installed compiler and renderer completed normally.

## Still open

No mathematical obligation in the audited existence route remains open. Human verification and formal checking of this exact exposition have not been done. The numerical census, the checker implementation and the sampled figure geometry are not formally certified. The stronger question of which Hamiltonian cycles arise specifically from forest-pair recovery is not settled by the compatible-state characterization; no such claim is made.

## Three best next steps

1. Ask a human referee to check the map-surgery paragraph, the generalized Lemma 12, Remarks 14 and 15, and the corrected phase normalization.
2. Let the merge agent reuse the primal proof, dictionary and primal figures in paper/main/, preserving the distinction between the new self-audit and the original independent referee.
3. If a machine-checked correspondence is desired, formalize the real-sign normalization and the compatible-state converse next to the existing Lean declarations.

## Leads for others

The phase-ratio correction should be propagated to any integration document that copied referee M4. The simplification uses the disk identity and aligned corner conventions; it is not a statement about arbitrary triangle systems. The current figure inputs are named running.json and layout-running.json, not example.json and layout.json.

## Reproduction

Commands are in proofs/primal/README.md. build.py regenerates TeX and renders. check_cancellation.py takes a dual-vertex count and writes JSON; inspect_figures.py checks the running example and writes figure contact sheets. CHANGES.md maps each request to its verification. revise.py is a historical initial patch, not a build entry point.
