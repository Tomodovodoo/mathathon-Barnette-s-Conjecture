COMPUTED: C3 independently passes the full census through V=20, totaling 3,373,400 pairs, and all 335,704 pairs of a 40-graph V=40 batch.
REFUTED: all 27 named alternative potentials have independently checked counterexamples; universal claims about all bounded rules need correction.
PROVED-HERE audit: the structural descent identities and the conditional PPADS reduction are supported, with explicit scope and encoding details.
COMPUTED: all 7,940 induction exceptions through V=18, the rotation bijection, counting inequality, corner avoidance and global half bound were independently reproduced.
GAP: C3, general G and the two-sided cancellation-free induction step remain unproved; the earlier claimed equivalence is unsupported.

# Referee report

## What I set out to do

Audit the descent report and the induction-lemma/completion reports with independent reasoning and code. All writes stayed in research/2026-11-14_astra_referee-descent/. No subagents were used. I am a fresh GPT-6 Astra instance, a different model from Fable but the same model family as the induction report's author. This review supplies implementation independence, not a different-model check of the Astra report.

I read BRIEF.md, the glossary, the requested skills and referee rules, the complete supplied text of OpenAI-Barnette.pdf, the relevant trees-paper sections, and the proof-supplying induction lemmas. The raw PDF was not visually rendered; no disputed formula required reconstruction beyond its supplied text and the displayed project equations. The shared tree was dirty on arrival. Other owners' files were neither edited nor staged.

## What I established

COMPUTED. Two new enumerators agree on every pair through V=16: direct incidence-bijection search and independent degree-two cover search followed by cycle orientations. Neither imports barnette_lab or either report's verification code. The only shared inputs are plantri triangulations, saved certificates, and the raw random generator for reconstructing the report's lost certificates. Separate independent random samples use a new degree-four split generator.

| Check | Independently completed range | Evidence |
| --- | --- | --- |
| C3 and radius-two escape | all roots and pairs, V<=20; no radius above two below 21 | code/c3_6_19.json, code/c3_20_20.json |
| C3 random batch replay | 40 graphs at V=40, all 3,040 roots, 335,704 pairs, 209,542 good pairs | code/summary40_0_40.json |
| New random sample | 15 graphs, five each at V=26,30,34, one random root each, all 70 pairs | code/random.json |
| New separator-free sample | 20 graphs at V=26,30,34,40, eight roots each, all 1,160 pairs | code/random_separator_free.json |
| Adversarial families | saved V=18 lattice example, its white gluing and the actual saved V=33 example; prism sums, nanotubes, separator-free one-cover family | code/families.json, code/adversarial_extra.json |
| Named potential traps | 27 alternatives, including all sign/order cases, with recovered V=40 area/size certificates | code/all_potentials.json, code/potentials.json, code/recovered40_0_40.json |
| q radii | 2,3,4 at V=16,21,40, with 16 and 21 independently minimal; saved V=60 radius four also checked | code/witnesses.json, code/recovered40_0_40.json |
| Height minimality | all pairs through V=17; equal signs first fail at 16, opposite signs first fail at 18 using saved witnesses | code/height_minimality.json |
| Region deficiency | 699,666 eligible connected-complement/color checks, V<=14 | code/deficiency_6_14.json |
| Contraction deficiency | 6,202,336 subset/merge/root checks, V<=14 | code/contraction_formula.json |
| Short-cycle obstruction criterion | 48,388 merges, 3,374 separator-free rooted inputs, V<=16 | code/structure_6_16.json |
| Induction bijection and bound | all 1,202,792 rooted contractions, V<=18, all 7,940 exceptions | code/induction_6_16.json, code/induction_17_18.json |
| Corner avoidance and global half bound | every tested eligible face and contraction, V<=18 | same induction files |
| Inward-descent minima | exhaustive region selection through V=16, first failures at 11,13,14 in the V>6 domain | code/minimal_regions.json |
| Fixed-cover repair obstruction | all exception records through V=18; first all-exception covers at 18, 220 rooted records | code/cover_obstructions.json, code/induction_witnesses.json |
| Height lookahead two | all eight signed three-entry potentials, full V=40 certificates | code/macro40.json |

Every table row is COMPUTED, with the scope given in its middle column. The general structural proofs are audited separately in REFEREE-descent.md and REFEREE-induction.md. They remain project proofs with AI review, not human-checked literature.

## Corrections required before integration

REFUTED overclaims. 'Every bounded variant is false' goes beyond failures of lookahead one, two and three. Radius four is open. 'Every potential involving c fails' also exceeds what was shown. The robust negative statement is that some pairs cannot reach a good pair without increasing c; the other refutations name specific potentials.

COMPUTED certificate repairs. The original selected V=40 radius witness has radius three. I recovered a radius-four witness at graph 3, root {10,16,11}, of the recorded skew/40/40/15 batch. Truncated V=40 size/area witnesses were replaced by complete independently checked pairs at graph 21, root {6,30,31}; V=50 two-move traps were recovered from skew/50/12/6 graph 11, root {5,15,14}. The outputs preserve full rotations and face-indexed states.

PROVED-HERE audit. The PPADS restart preserves the pair because the preceding endpoint is alpha-fixed, so its cycles are already counterclockwise. An initial suspicion about normalization was resolved by that premise. The sink reduction is supported conditional on the supplied marked-involution theorem. The exposition still needs precise totalization, efficient-cost assumptions for PLS, and the correct search-reduction qualification for the hardness claim. Capped V=300 runs cannot be summarized as completed successes.

GAP. The rotation/counting theorem gives a sufficient condition for a good state upstairs. It does not prove the converse claimed in MISSING-LEMMA.md. Use the symmetric missing lemma that at least one side has a nonexceptional good state. The blanket state-to-outer-state correspondence also needs the outer-forest restriction already used by its proof; code/outer_scope_counterexample.json gives a V=8 counterexample to the unrestricted sentence.

## What failed, what remains open, and why

I found no C3 counterexample. The new insertion sample is small and biased; the adversarial white-face products are constrained by the proved product structure. The full V<=22 census and full 230-graph random campaign were not independently replayed. Their reported sizes must remain distinct from this review's ranges.

No general proof of C3, G or X emerged. The finite half-exception and corner-avoidance checks do not supply the missing induction step. The V=18 fixed-cover example rules out a whole class of repairs, but a cover-changing repair remains possible.

The supplied source papers are accepted inputs for the bounded audit, not newly certified proofs of Barnette's conjecture. Megiddo-Papadimitriou's primary definition and hardness theorem were opened. Buss-Johnson's Turing closure statement was checked in Corollary 6.2 of the indexed author PDF; direct full-PDF retrieval failed. The reports record that source limitation.

## Three best next steps

1. Integrate the corrected wording and complete recovered certificates. Keep the finite ranges and same-model-review qualification visible.
2. Attack C3 through the positive-level plateau obligation, or seek an explicit radius-five family. The product construction cannot increase the factor radius.
3. For induction, seek a global selection proof across four- and five-cycle obstructions and a repair that changes covers. A proof of the global half-exception bound would settle the two-sided counting step.

## Reproduction and git

code/README.md lists every output command and implementation boundary. Heavy runs were sequential; the longest completed run in this review was the 512-second induction job. Source hashes were recorded during the session, and the final comparison found no changes to the recorded source files. Final artifact checks parsed every Python script and JSON output and verified the saved certificate flags and aggregate counts. Commits stage only this folder. Final commit and push status are recorded in the chat handoff.
