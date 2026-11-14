# Which language for the final paper

Reviewer: Claude Fable 5.2, 2026-11-14. This is an editorial judgement. What it rests on: a full read of `proofs/primal/PRIMAL-PROOF.md`, the section outlines of `paper/draft-A/barnette.tex` and `paper/draft-B/barnette.tex`, and the summaries and findings of their referee reports (`research/2026-11-14_opus_review-draft-A/REFEREE.md`, `research/2026-11-14_fable_review-draft-B/REFEREE.md`). I did not read the two drafts line by line.

Summary.
1. Recommendation: a hybrid with the primal proof as the logical backbone and the dual triangulation as the picture language. Every lemma is stated and proved in `G`. The dual appears in figures, in one dictionary table and in remarks.
2. The reason is that both dual drafts tripped on the same thing, the inside of a cycle, and the primal proof has no such step to trip on.
3. The primal note is not paper-ready. It has no figures, its planar section is dry, and it must absorb the fixes of REFEREE.md.
4. Two steps should keep a dual picture next to the primal proof: the definition of a state and the disk identity.
5. Three steps should be primal only: the flow weights, the recovery, the induction.

## The evidence from the two drafts

Draft B's referee found one real gap: Euler's formula applied to "`Z` and everything inside it" with no proof that this plane graph is connected. Draft A's referee found that Lemma 8 never says why the outer vertex is outside the disk, and that a sentence of Lemma 4 is false without the partner. Two of these three are about the inside of a cycle of the triangulation. The Lean development spends its longest proofs on the same point (`state_disk_count`, `region_euler`, `mixed_corner_on_boundary`).

In the primal proof the inside is the shore of a bond that misses `b0`. It is connected because a bond has connected shores, which takes four lines and no planarity. The root is outside by definition. A face cannot be pinched because its boundary is one closed walk. My referee report found the primal note's planar section incomplete as a list, but found no gap of this kind in the argument. That is the strongest reason a reader would recognise: the dual drafts needed a referee to close the disk, and the primal text does not.

## Step by step

| Step | Language of statement and proof | Dual material to keep | Why |
| --- | --- | --- | --- |
| Target and induction statement | Primal: a perfect matching through `e0` with connected complement | none | The theorem is about `G`. Two induced trees are a detour unless tree partitions are the subject. |
| Planar toolkit | Primal: face circuits are bonds, the Euler count for a shore, one sign around a circuit | one sentence: "a face circuit is a cycle of the dual graph" | Pay for planarity once, by name. Put the proofs in an appendix and the statements up front, so the paper does not open with a page of linear algebra. |
| States | Primal definition: each black vertex other than `b0` picks one of its three faces | a figure with the dual triangle and its chosen corner next to the three sectors at a cubic vertex | Corners of a triangle are easier to draw and to count than sectors at a vertex. Draft B's "corner choices" figure does this well. |
| First pair | Primal, Li's deficient set as in Lemma 4 | none | The union of facial cycles and its 3-edge cut live in `G`. The dual density argument is longer. |
| Disk identity | Primal: the four counts of Lemma 5 | a figure of the disk in the triangulation with its `h` boundary vertices and `ℓ` inward black triangles, labelled as a picture of the cut side | The dual picture explains what is being counted faster. The primal proof is the one with no hidden step. |
| Weights | Primal only: one unit of flow from `b0` to every white vertex, local potentials | none | Spoke circulations and the detoured cycle are the heaviest part of the dual route, and the Lean replaced them with exactly this flow. |
| Sign and polynomial | Neutral. Use the real sign `∏δ` and the factors `1 + a z` | a remark giving the relation to the original phase and exponential | No index `J`, no limit. Draft A's referee recommended the same sign. |
| Cancellation, nonvanishing | Neutral, as in Lemmas 7 and 8 | a remark on Li's two involutions as the bijective reading | Same mathematics in either language. |
| Recovery | Primal only: the tree in `G`, parent edges, cut balance. State Lemma 12 in the general form (REFEREE.md, F5) | a remark for Draft B's face tree `Y_s`, which is the dual of the removed links | The proof ends in the graph where the cycle is wanted. |
| Three-edge cuts | Primal only: contract a shore, glue two paths | the phrase "separating triangle" once | Contraction is shorter than capping a triangulation, and keeps "for every edge" visible. |

## What the dual route still does better

- It gives the reader something to look at. A triangulation with coloured triangles is a familiar picture. Three face sectors at a cubic vertex are not.
- "Cycle" is a shorter word than "face circuit", and "inside the cycle" is a faster idea than "the shore that misses `b0`". The paper should say both once and then use the primal term.
- It matches the original paper. A reader who comes from OpenAI's text needs a dictionary. One table is enough: `T` and `G`, triangle and vertex, vertex and face, cycle and bond, disk and cut side, spoke weights and flow.
- Draft B's winding-number proof and finite-difference lemma are its author's own and the referee found them sound. They are a second proof of the nonvanishing and belong in a remark or an appendix, not in the main line.

## What has to change in the primal note before it can be the backbone

1. Apply the replacement texts of REFEREE.md: the planar list (F1), the definition of `δ` (F2), the missing step of Lemma 3 (F3), the sentence in Lemma 2(b) (F4), Section 9 (F7).
2. Reorder: general circuit and cut lemma, then Lemma 1, then cut sides and the Euler count.
3. Add figures. At least four: the cube with one state and its `Q_s`; three sectors at a black vertex with the sign of each transition, beside the dual triangle; a cut side with its four counts on the 20-vertex example; the recovery tree and the matching on the cube.
4. Replace the data dump of Section 11 by the figures and one table per example. Keep the dump as supplementary data.
5. State Lemma 12 as Lemma 12'. Say in one sentence that the pair and the forest exist only to produce a matching compatible with a state.
6. Say plainly, where face circuits are introduced, that they are the cycles of the dual graph. The note does this. The paper should too, early, so nobody feels the dual was hidden.

## What I would not do

I would not write the main text in the dual with primal remarks. The remarks would then carry the three places where the argument is safest in the primal (inside of a cycle, weights, recovery), and the main text would carry the versions that two referees had to repair. I would also not write a purely primal paper with no dual picture. The disk identity without a picture of a disk is a page of bookkeeping.
