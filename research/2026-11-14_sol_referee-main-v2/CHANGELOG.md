# Applied corrections

All items are PROVED-HERE scope or dependency corrections, except C7, which records the supplied formalisation's checked scope. No structure, figure source or style was changed. Locations use labels so they survive line shifts.

| ID | Location | Before and correction | Reason |
| --- | --- | --- | --- |
| C1 | Abstract, sentence 3 | Says a matching corresponds to exactly one side per triangle and explicitly places its connected complement in the original graph; states the iff. | Prevents identifying connectivity of the primal complement with connectivity in the triangulation. Both directions are Lemma 2.5. |
| C2 | Plan, fourth step | The reversal pairs off pairs whose second state is unsuitable, rather than pairing off second states. | It fixes s and changes its partner r. The two cancelled terms can have the very same s. |
| C3 | Lemma 2.5(1) proof and paragraph before Lemma 3.8 | Replaced two claims of open disks with connected open regions bounded by Z. | This is exactly Jordan separation; no Schoenflies homeomorphism is needed. |
| C4 | Paragraph before Proposition 3.9 | Restricted the purported cycle of chosen sides to P_s minus e0. | e0 is not a chosen side for the state, and the proof first excludes cycles avoiding e0, then proves that adding e0 closes no cycle. |
| C5 | Proposition 3.9 proof | Added explicit reference to Lemma 3.8 at the disk-identity invocation. | Blueprint's first implicit use. |
| C6 | Heights definition paragraph | Added Lemma 2.5(2), with M=T and N empty, to justify G connected. | G now denotes the dual of an arbitrary coloured triangulation, not just the original graph in Theorem 1.1. T is connected by Lemma 2.2. |
| C7 | Final paragraph | Added that the Lean route uses algebraic duality and does not check every statement or proof here; names Proposition 2.6(2). | COMPUTED in the supplied Lean build and PROVED-HERE source comparison in proofs/blueprint/BLUEPRINT.md. The original sentence about the formal proof of Barnette itself remains correct. |

Build and commit recorded in REPORT.md and code/README.md.
