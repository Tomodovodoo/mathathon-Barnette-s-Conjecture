# Critique of the three Barnette papers

Scope: exposition of the supplied versions, not a verdict on Barnette's conjecture. LIT marks claims attributed to the supplied public preprints O and L. O is OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, September 24, 2026. L is Zhentao Li, *A note on the proof of Barnette's conjecture*, arXiv:2610.30490v1, October 21, 2026. C is the supplied *A constructive proof of Barnette's conjecture*, dated October 18, 2026; no author or independently verified publication identifier was established. Its additional mathematical claims are treated as HUNCH pending a separate audit, not promoted to LIT. Recommendations and rankings are editorial HUNCH judgments.

## OpenAI, eleven pages

The opening already does something the requested rewrite should preserve. After Theorem 1.1 it says, "The difficulty is to obtain one spanning cycle." It then distinguishes a spanning subgraph of degree two from a connected one. Section 1.1 gives a real account of both regroupings of the weighted sum. It would be inaccurate to diagnose this paper as having no motivation or no proof route.

The reader's first likely loss of orientation is the jump from that excellent problem statement to states, pairs, Q_s, D, spokes and phases. The introduction explains each, but in rapid succession before the reader has seen the geometric conversion from a forest state to a Hamiltonian cycle. The first full incidence-tree construction is in §6.1, on page 8. An earlier conditional recovery picture would tell the reader what a forest state buys before asking them to spend §§3–5 obtaining one.

LIT, §2 supplies the state bijection and counts, Proposition 3.1 supplies a pair without separating triangles, Lemma 4.1 supplies the disk identity, Proposition 5.1 supplies the forest state, and §§6–7 recover and glue. That is a sound expository spine to retain. The proposed change is to expose its target sooner, not to replace its proof by a new route.

The full norm of the difficulty appears in §5. A reader must distinguish a Q_s cycle, whose reversal changes r only, from a D cycle, whose reversal exchanges both choices. Figure 1 depicts the local edges well, but it appears on page 8 after the nonvanishing argument. Put the two local edge choices at their first definitions on page 5 or 6. Add a two-row invariance table rather than another paragraph narrating the whole proof.

There is useful compression available in Proposition 3.1. The source gives the capacity network, minimizes the cut and then proves the integral augmenting-path conclusion in detail. For a research exposition, cite integral max-flow after giving capacities and the exact cut condition. Keep the planar density proof, especially its treatment of triangular regions and repeated boundary sides. Those are graph-specific, unlike the elementary flow proof. LIT, O Proposition 3.1.

Do not cut B=I+ℓ from the disk proof or the simple-spoke-detour argument from §5.3. The former encodes the bijection; the latter verifies the orientation to which positivity applies. These are precisely the sort of proof-specific bridges the floating audits preserved. Similarly, the final selected-edge count in §6.2 must explain why an internal chord cancels. "By duality" alone would not prove that the selected graph is acyclic.

Notation is largely disciplined internally. B denotes a black-face count locally; it is not also the named incidence graph in this paper. The main hazards arise when combining sources. H_0 excludes the outer black center, while H in §6 includes it. D is a cycle union, not the final forest. P denotes selected edges of T, not a matching in G. The phase i^J should be explained as a bookkeeping device whose sign changes under the appropriate reversal, not treated as a new analytic problem. In a combined manuscript use B_d,W_d for disk counts so B can name the incidence graph.

Corollary 7.2 introduces Pfaffian orientations and a path-containment consequence after the main proof. It is correctly attributed, but an exposition centered on why the Barnette construction works can omit it or place it in a brief consequences section. This is a scope cut, not a simplification of the proof of Theorem 1.1.

## Li, fourteen pages

Li's strongest feature is the visual proof sketch on pages 1–2. The matching, incidence tree, white tree and primal cycle are shown before the technical argument. Section 4 also explains the logic of two sign-reversing involutions before defining the signed objects. Preserve this order of purpose before machinery.

The paper nevertheless asks the reader to learn too much before the central need is visible. Definition 5 introduces G_FB; Definition 6 packages a rooted graph; §1.1 introduces aux(G); §2 inventories definitions including bit flips and involutions that are not yet used. The sentence "This section can be skipped and referenced when needed" is a symptom. Move the nonstandard conventions beside their consumers and leave elementary graph terminology in a short preliminary paragraph.

The main interruption is explicit in §4.1: "we restrict ourselves to the case where c_min=1 ... and extend this ... in Appendix B." The case is a useful illustration, but it is not the general argument. Section 4.9 invokes Lemmas 34–35 from Appendix A, and Appendix B supplies the general marked objects. The reader must assemble the central proof across three locations. Keep the single-mark case as an example, then state and prove the full construction in the main cancellation section. This follows the floating appendix lesson without claiming that deferred proofs are logically invalid.

The general mark convention needs a careful editorial and mathematical pass. Definition 14 uses braces around the intersections; Appendix B writes indexed marks and refers to a "first" cycle. A reader needs to know whether marks are ordered, distinct, or repeatable, and what fixed order makes the involution select the same move on the return step. This critique does not assert that an intended convention is false. It identifies the exact question a revision must settle before compressing the formulas. LIT source location: L Definition 14 and Appendix B; sufficiency of the convention remains open here.

Section 4.8 proves the parity mechanism using τ and the counts t_C,in and t_C,out. Its purpose is good, but Claim 25's elementary Euler rearrangements occupy many display lines. Keep the three graph counts and the resulting t_C,out identity, then explain the substitution briefly. Keep the turn table in Claim 26: it is a compact comparison that actually helps. LIT, L Claims 25–26.

The final recovery in §6 is much harder to read than the introductory drawing suggests. The black dual trace alternates between graph types, and the symbol with an arrow over T_W denotes an oriented tree in G−b_0, whereas T_W itself is a tree on white vertices in an incidence dual. The symbol table acknowledges this, but the reader encounters the change much earlier. Use T_BW and its arrowed version consistently for the traced tree, retaining T_W for the white-vertex tree. This is a type distinction, not a cosmetic rename.

Other notation hazards are explicit boundary conventions. Int(C) includes C, although prose also says "inside"; strict interior must be named when that is meant. B,W are primal vertex classes, while the shared repository uses B for the incidence graph. P is a primal matching and its complement is the desired cycle. Translating this P directly into OpenAI's selected dual forest would reverse its role. Give a dictionary if both presentations are discussed.

The appendix is not just long in the text dump. I rendered page 12 and confirmed that its long multi-mark tuple formulas extend beyond the visible right margin. Replace full tuples by "replace the i-th mark by ... and reverse C_i when ...", after a precise mark convention. This preserves the action and avoids unreadable repetition. The page image is retained in this folder as `A-Note-On-Barnette.pdf.png`.

Appendix C contains the essential 3-edge-cut reduction. Place it immediately before or after the irreducible case, with the two-edge boundary choice drawn. State which edge is omitted in the second piece and why this forces compatible crossings. LIT, L Theorem 3 proof. Do not merely write that cycles glue.

## The constructive paper, fifteen pages

This is the strongest starting point for a first-principles explanation. The introduction begins with degree two and connectivity, uses the two opposite cube faces as a counterexample to local sufficiency, defines the incidence-tree target, and follows the cube through Example 2.2 and §7.2. Equation 3 and Proposition 2.1 explain what the second matching does: it orients the opposite-edge graph, revealing rooted tree components and rootless unicyclic components. Those are source assertions, not independently audited general results in this report.

The central expository cost is scope. The introduction promises an exact obstruction criterion, reachability within every exchange component, a deterministic marked walk, a faster enumeration, a determinant bound, prescribed-edge recovery and implementation checks. These are several papers' worth of reader goals compressed into one opening. The abstract has nine sentences and explicitly says the exposition is self-contained, a claim the prose should demonstrate rather than advertise.

The most useful structural cut depends on the theorem selected. For an existence exposition, retain the incidence-tree target and weighted cancellation; move algorithms out. For the stated time-bounded construction theorem, keep the enumeration and determinant proof in the main line, but place the slower marked walk after the completed cycle construction as an alternative. Currently §5.1's token pools and restarts intervene between existence and the faster algorithm in §6, even though that faster algorithm does not use them. The source itself distinguishes the two constructions at the end of the introduction and in §8. Make section order respect that independence.

The stronger exact obstruction theorem also needs a purpose statement. OpenAI assumes no separating triangle; C distinguishes black from white inner boundary and cuts only when flow fails. That refinement earns space if the paper promises the exact criterion or the selective decomposition algorithm. It is unnecessary baggage if the paper only promises the easiest exposition of existence. Do not combine the simpler hypothesis with the stronger conclusion without preserving the refined density proof.

The polynomial proof in Theorem 5.2 is concise and clear. It says what each grouping proves before doing it, and it emphasizes that the polynomial can vanish at 1 without being identically zero. The cube example 1−z makes this distinction tangible. Preserve it. The component restriction requires both reversals to remain inside the component, and the text checks this; if the new paper sums globally, the exchange graph itself can disappear.

Notation has fewer internal problems than Li's. H and B are full and reduced incidence graphs; H_0 is introduced for circulations; Q_s, D_r,s and W_s have different jobs. The dangers are accumulation and type changes during reading: P first denotes the set of pairs as a calligraphic letter and later an ordinary selected-edge set; W(s) denotes tokens while W_s denotes a white-face tree. These are not proven collisions, but the marks section makes them harder to distinguish. Moving that section later removes the burden without unnecessary global renaming. The distinction between permutation sign in Lemma 6.1 and pair sign ε is already explicitly stated and should remain.

The recovery section should arrive sooner. After the incidence-tree target is defined, give at least the conditional conversion to a Hamiltonian cycle, and reserve its disk-count verification for the proof. This lets the reader understand the target before learning a theorem about every exchange component. Keep the cube labels stable when moving the material.

The title "A constructive proof" is accurate only with the algorithmic contract and termination proof retained. It does not imply a polynomial-time algorithm. The source compares its exponential bound with Eppstein's faster general cubic-graph algorithm. Keep that honest comparison if computational complexity stays in scope; do not present the bound as the main practical advantage.

## Ten changes, ranked by expected value

| Rank | Concrete edit | Main beneficiary | Acceptance test |
| --- | --- | --- | --- |
| 1 | Choose existence or time-bounded construction as the main contract; separate the optional algorithmic route. | C and new paper | Every main section is a dependency of that contract. |
| 2 | Explain the forest certificate and its degree/connectivity consequences before constructing states. | O and C | Reader can say why a forest state is useful before reading cancellation. |
| 3 | Put the general marked-object argument and its sign checks beside the involutions, not in appendices. | L | Main proof handles arbitrary c_min with explicit mark conventions. |
| 4 | Give the two reversals a local picture and invariance table at first use. | All | Reader identifies which matching and weight stay fixed in each move. |
| 5 | State why a second matching is needed through the outdegree/root-component argument. | O and L | No unsupported inference from arbitrary acyclicity to an incidence tree. |
| 6 | Lead the disk count with B_d=I+ℓ's purpose and show the counted boundary incidences. | All | Reader distinguishes matching information from ordinary Euler counting. |
| 7 | Introduce the prescribed edge as gluing data; keep separator recovery in the main route. | All | The common facial pattern is visibly preserved across induction. |
| 8 | Remove routine flow proofs and expanded Euler rearrangements while retaining graph-specific premises. | O and L | Every removed derivation has an exact named theorem or one-line substitution. |
| 9 | Resolve cross-paper graph types and Li's traced-tree notation; specify marks and strict interiors. | L and synthesis | One symbol means one type in each active scope. |
| 10 | Place figures at their use and rewrite long tuple actions as local replacements. | O and L | Print-size inspection shows readable figures and no clipped general-case formulas. |

These are not rankings of mathematical truth. None licenses deleting the nonvanishing argument, claiming that a 2-factor is connected, or replacing an exponential algorithm by an asserted polynomial one.
