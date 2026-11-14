# Revision report

1. Applied all 15 referee edits within proofs/involutions/, including the corrected leading sign and attribution to Li.
2. PROVED-HERE: a drawing-free mark model on dual-tree face paths, with a complete proof that both involutions and the constructor still work.
3. COMPUTED: all 1206 roots through 14 vertices in ray mode and two tree modes; every object and all 4658 fixed starts per mode passed.
4. Rebuilt the 17-page PDF, inspected all pages, and found no errors, undefined references or overfull boxes.
5. The new lemma has a FOLLOWS self-audit; an independent referee of that addition is the main next step.

## Scope and results

The assignment was to finish the standalone bijective note by applying the independent Opus referee's report and adding a drawing-free formulation. Only proofs/involutions/ and research/2026-11-14_sol_involutions-revision/ were edited. The shared main paper and other research folders were read only. The required brief, unslop skill, reverse-Lamport skill and its worked example were read. Li's source text and the rendered Appendix B were checked against the revised attribution. The main paper's Section 4 and the draft-B referee were read for the face-path convention.

PROVED-HERE. Section 5, Lemma 7 replaces a crossing by a white-face/path-step incidence eligible precisely when the path turns around the selected corner. Its bit is (1+kappa)/2. A cut of the oriented incidence map supplies parity, alternating directions and the first-exit rule. The proof checks the second map's partner eligibility, no collisions, invariant priority and return reversal explicitly. The old fixed-count and finite-path arguments then apply with the same F. This is Li's intended proof written out, and a term-by-term bijective unpacking of one height in the main paper. It is not a separate proof route or an efficiency improvement.

REFUTED and corrected. The old coefficient exponent (n-m)/2 fails for odd m, first on the octahedron. It is now (n+m)/2, both algebraically and computationally checked. The census has 55 classes. Li already states the set convention and unmarked-cycle rule; the revised text says so and credits the earlier dependency audit.

COMPUTED. The mirrored root anchoring explains 279 versus 213 on the same running input. Across 69 drawings, 35 counts occur from 103 to 363, paths have zero through six moves, the signed sum is always -9 and F is always 9. The actual second-fixed objects vary; only their count is invariant. This distinction is explicit in the note and both Markdown companions.

## Verification

| Mode | Rooted instances | Paired instances | Objects | Second-fixed starts | Maximum moves |
| --- | --- | --- | --- | --- | --- |
| Original author's rays | 1206 | 880 | 221050 | 4658 | 2 |
| Increasing-ID BFS face tree | 1206 | 880 | 17832 | 4658 | 4 |
| Decreasing-ID BFS face tree | 1206 | 880 | 18362 | 4658 | 4 |
| Independent referee rays, rerun | 1206 | 880 | 244240 | 4658 | 4 |

All entries are COMPUTED, with commands and outputs in COMMANDS.md. Every object was checked for involution membership, both return identities, both nonfixed sign changes, the first fixed-set forest criterion and the second fixed-set count and common sign. Every second-fixed alternating start was traversed without repetitions to a forest. Lower moments vanish and the corrected normalized leading coefficient agrees with F. The tree code checks crossing parity by an independent rational polygon winding test, successive directed signs and first-exit signs. Additional checks cover Li's opposite orientation convention, the epsilon phase, the local delta identity in every triangle order, and integer floor identities. The old verifier's maps and enumeration were copied with attribution; the path data and added checks are revision code. The referee code is imported read-only and all its outputs are redirected here.

The complete canonical class sets agree with plantri, not merely in cardinality. The hard-family suite and its walk comparisons were rerun, as were all 880 comparisons with the integer-weight polynomial. The full 279-row published listing agrees with the independent referee implementation, with no sign or image mismatch. Every drawn object and image is computed in figure-data.json.

COMPUTED. With m-1 marks all counts vanish. With m+1 the referee's drawings give 57 zero counts; the author's drawings give 78, and the two face trees give 123 and 125. The note records the requested 57 with its geometry qualifier. PROVED-HERE: fewer marks cannot give the nonzero imbalance, and more marks break the second map's one-token-per-cycle deduction.

## PDF and prose

The PDF is amsart on A4 with one-inch margins, 17 pages. Two final pdflatex runs completed without errors, undefined references or overfull boxes of any size. The remaining package-name warning comes from the read-only relative style import, not a reference or layout problem. MiKTeX also prints its update reminder. All 17 pages were rendered with pdftoppm and inspected in contact sheets; figure pages were also inspected at full size. Figures are on dedicated pages after all statements and proofs. Figures 1 and 2 show the actual rays in the affine direction and zoomed crossings. Figure 3 shows computed face-path incidences; Figure 4 retains the first-map state change. Explicit figure labels are footnote size or larger. Prose was checked for inflated claims, unfair attribution and stale layout assertions.

## What failed and what remains open

The first path checker used sorted cycle-face order for its independent polygon test, which need not be traversal order; it was corrected to follow the r-to-s permutation before the full successful run. A SymPy Boolean also needed explicit integer conversion in an added sign check. Neither was a proof defect. The original coefficient sign and layout explanation were real errors and are corrected. Bare face-path steps without selected-corner eligibility would be the wrong mark model, so the definition includes that condition.

No requested implementation item remains open. The changed proof has a bounded conclusion-first FOLLOWS self-audit in AUDIT.md. That is not an independent referee verdict on the new path lemma. No universal walk bound, efficient minimum-cover initialization or invariance of higher-mark counts is claimed.

## Leads for others and three next steps

1. Independently referee Section 5, especially the local turn sign and the component-change argument in Lemma 7.
2. If the main paper uses this note, cite its term-by-term dictionary and preserve the opposite H/omega normalization.
3. Study how the dual-tree choice affects object counts and alternating walks. The two measured trees differ, but no optimization theorem is proved here.
