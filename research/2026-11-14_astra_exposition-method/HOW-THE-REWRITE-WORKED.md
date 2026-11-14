# How the rewrite worked

The improvement came from changing what the proof asked the reader to carry. First the revision removed stronger intermediate problems that the conclusion did not need. Then it put each surviving calculation immediately after the question that required it. Sentence polishing helped, but these two changes did most of the work.

## Evidence and limits

I retrieved the complete activity sequence, positions 0 through 2764, from [Rewrite the Floating Proof](t3-thread://v2/1027ef7f-c3ad-4c48-b57e-8f5d57123b4b/1646eeb3-f07c-41e0-9471-33eacc18d19d), including all 55 runs. `USER-TURN-INDEX.md` preserves every user turn, including housekeeping and corrections. `thread-messages.json` preserves the user and assistant messages with their positions. Tool-output continuations were retrieved separately. This is a history reconstructed from conversation, saved sources, comparisons, and audits, not an independent certification of the floating theorem.

Historical observations below are documentary evidence, not mathematical claims. Mathematical changes are attributed to their drafts and audits. They should not acquire PROVED-HERE status merely because an assistant said a review passed. Editorial recommendations are HUNCH judgments to test on a reader. The source manifest records the files available at inspection time. Dates and page counts below belong to the thread's particular builds, not to a single immutable file named floating.pdf.

Main source locations, relative to `E:/Personal/Math/Leeham/floating/`, are `floating.pdf`; `Astra/v1/floating_revised.tex`; `Astra/v2/floating.tex`; `Astra/v3/floating.tex`; `Astra/v4/floating.tex`; `Astra/v5/floating.tex`; `Astra/v6/floating.tex`; `Astra/V6_Figures/floating.tex`; the six files in `Audits/`; `rewrite/v2/floating_v2.tex`; `rewrite/v3/floating_v3.tex`; and `Astra/v6/reviews/history.md`. The final title proposal is in `Astra/V6_Figures/work/title-abstract-review/main.tex`, not in the canonical manuscript. The downloaded alternatives live in `online proofs/v1`, `online proofs/v2`, and `expansion/manuscripts`. `output/` contains supporting artifacts, not another automatically authoritative revision.

## Starting state, 22 October

At position 0 the user asked for a publishable paper, not an audit report. The request already distinguished a shorter route from denser prose. It specified amsart, A4, one-inch margins, a brief title, at most six abstract sentences, few unnecessary headings, and fewer displays for routine rearrangements. The user explicitly called these examples approximate pointers toward a cleaner argument.

The original begins with the theorem and analytic conventions, including matrix norms and a global parameter-jet norm. Its abstract says the proof "combines an all-degree arithmetic estimate ... with an exact differential reduction and an analytic iteration". This names ingredients without explaining why one forces the next. The opening also calls the parameter an "admissible chord half-angle", language later corrected because the displacement belongs to a chosen parametrization.

### The first two deletions were mathematical

Positions 28 and 56 identify the first large cuts. The revision used a fixed, sufficiently high shape approximation instead of making its order grow as the amplitude decreased. It estimated Lipschitz differences on successive closed admissible sets, using the physical residual there. The corresponding global extension and artificial-residual problems disappeared. The scalar phase could still be extended for the measure argument. Thus "no extension" would be an inaccurate summary.

The deletion propagated. Once the conclusion needed only a fixed-order shape approximation, the paper no longer needed all-order shape-coefficient growth, Gevrey closure for that approximation, or amplitude-dependent optimal truncation. This did not initially remove the distinct all-order Fourier reduction for the operator. Confusing these two truncations would turn a useful lesson into an invalid shortcut.

The first revision and checks are reported at 81, 104, 152 and 166. Positions 168, 175, 186, 189 and 193 concern folder placement, collected downloads, an initially requested empty audit file, and deduplication. They changed the evidence organization, not the argument.

## The audits narrow what may be cut

At 205 the user asked for synthesis across `Audits`, `online proofs`, `rewrite`, and `Astra`. The central instruction was to stop explaining routine facts at excessive length and use appropriate citations consistently. The response at 216 retained operator-increment estimates while cutting repeated bookkeeping. At 257 terminology became an explicit audit target. At 279 the theorem was stated once and only expansion coefficients used later survived. At 324 the resulting Astra v2 was reported as nine pages.

The audits are a dispute, not six votes of confidence. Audit 3 opens by withdrawing its earlier unconditional FOLLOWS verdict. It distinguishes proving that an estimate would suffice from proving the estimate itself. It accepts the fixed-order seed conditionally on uniform losses, but rejects the inference from admissibility at the limit to recovery of the original equation. Audit 5 rejects the proposed symmetric-module inequality and the claim that a single estimate on accumulated corrections replaces stagewise control. Its useful addition is the direct critical-coefficient calculation. Audit 6 is a thirteen-page manuscript's editorial cover note, not an independent sixth verification.

This is the central compression test. Delete an obligation only after showing that the consumer needs less. If the consumer still needs it, either prove it or cite a result whose hypotheses actually match. The recorded negative audits remain evidence even after the manuscript improves.

## Comparing v2s and reaching six pages

Positions 363, 386 and 391 organize v1/v2 folders. At 399 the user asks which v2 is best written, explicitly suggesting six pages. The assistant's assessment at 465 prefers the ten-page online `symmetric_floating_bodies` over nine-page Astra because its finite-dimensional elimination is easier to follow. The assessment pasted by the user at 478 instead prefers Astra. These are different judgments. The history should not turn them into a unanimous ranking.

The user at 478 gives the decisive editorial constraint: shorten "by cutting away fluff and proofs which are already obvious", not by putting everything into "blobs of text". The next revision makes the right inverse a proposition, removes unused expansion coefficients and four reconstruction constants, shortens arithmetic and pole calculations, and puts the Neumann series on the side that permits the raw column norm. The response at 495 reports that this last mathematical change removes the two-index remainder norm. The six-page v3 is reported at 540 and 568, at unchanged 11pt/A4/one-inch formatting. Positions 467 and 472 had meanwhile identified purported v3 downloads as exact v2 duplicates, confirmed at 476.

The important pattern is mixed. The right-inverse proposition adds a useful interface while several small lemmas disappear. Fewer lemmas is not itself the objective. A statement earns separation when later reasoning needs its complete contract.

## V4 grows, then the user makes it readable again

At 570 the user asks to compare the two v3s. At 613 and 701 the user requests part-by-part reviews. The integrated v4 adds explicit derivative assumptions, controls the remainder after finite elimination, moves the seed after the cap equations, and simplifies the displayed linearization. It grows to seven pages.

The user objects at 754. The response at 762 admits that review work had become manuscript exposition: reconstruction details, auxiliary-column cancellation, repeated norm bookkeeping, and proof labels. At 801 the paper is back to six pages, retaining the correction for the post-elimination remainder. This is the clearest failed experiment in the record. More verified text did not produce a better paper.

The user requests rendered comparisons at 803, then gives passage-specific corrections at 917. These identify the desired voice more precisely than the initial general brief:

| Before or objection | Accepted direction | What it changes |
| --- | --- | --- |
| "For K = -K" | "For an origin-symmetric body" | Readable prose introduces a hypothesis; symbolic identity remains available where used. |
| A calculation begins with new periodicity notation | "To ... , write" | State the goal before the device. |
| Long quadratic-energy explanation | Return to v3 after the necessary opening | Keep the improved orientation sentence; cut the re-proof. |
| Unexplained pole calculation | "The apparent poles are removable" | Say what the calculation establishes before doing it. |
| "normalizer bounds", "new margin", "the phase bound" | Name the operators and give the actual bound | Replace labels without definitions by identifiable mathematical objects. |

At 941 and 975 those edits are applied, with equations unchanged. These are pure writing improvements, unlike the earlier norm simplification.

## The appendix challenge changes the reading order

At 977 the user asks whether the Fourier-reduction appendix is needed. At 1004 the answer correctly distinguishes the indispensable estimates from their placement. At 1006 the user challenges both placement and the complexity of the decay derivation. At 1041 the reduction moves immediately before the inverse proposition, and a direct remainder bound followed by substitution of the truncation order replaces the longer presentation.

At 1111 the user asks whether the fourth-power decay is used before it is proved and why the last section feels like an afterthought. The answer at 1128 separates definition, proof, and application: the weighted norm is defined, the reduction lemma proves finiteness, and the inverse uses it. The section sequence becomes "Expansion at the ball", "The linearized equations", "Proof of Theorem 1". The last heading makes convergence part of completing the theorem. This is a dependency-order edit, not a new proof.

## The expansion is a second theorem, not a longer copy

At 1156 the user raises a three-dimensional density and asks for generalization; 1188 clarifies the source history. The new floating-2 source arrives at 1231. The response at 1256 identifies a second mathematical simplification: polynomial divisor bounds permit finite-order operator reduction, and a limiting argument replaces the wide-inverse lemma. The reported 26-to-10-page reduction at 1380 concerns this expanded source, not the original four-dimensional paper.

At 1382 the user asks to apply the earlier optimization method. The history review explicitly warns that v5 has already made the old major cuts. At 1426 downloads are organized in `expansion`; at 1433 the user supplies detailed notation and compression proposals. At 1439 divergence-theorem boundary integrals replace expanded nonlinear cap formulas. At 1465 the assembled v6 is nine pages. At 1493 the user requests a separate terminology/citation pass.

The notation changes at 1433 distinguish polynomial from angular profile, parameter from cap coordinate, energy constant from cosine coordinate, coefficient transform from frequency set, and scalar determinant from strip loss. These are type repairs. The evidence does not support renaming every local variable globally. The terminology review expressly allows harmless local reuse in disjoint contexts.

## An unwanted addition and a second appendix dispute

Positions 1513 through 1595 investigate a degree-six example and a possible family. At 1597 the user rejects a corollary or companion proof. The assistant misreads this as a request to integrate the family, creates v7, and is corrected at 1670. The user asks to remove v7 at 1676; 1684 confirms deletion. This addition did not belong to the accepted exposition. It is a scope failure, even though the assistant reported successful arithmetic checks.

At 1686, 1693 and 1699 the user asks what the arithmetic appendix does and why it is there. The answer vacillates between calling the choice wrong and reasonable. The useful distinction is objective: stating a lemma before use with an independent later proof is logically legitimate, but it can make reading harder. At 1703 and 1705 the user chooses reader order: put the isolation proof in the spherical-calculation section and explain the route in the introduction. At 1776 the user further rejects an abstract that merely lists techniques. The proof moves beside Lemma 3; parameter sets move before their estimates; the draft remains nine pages.

## The twenty edits show the writing method at sentence scale

Positions 1848 and 1894 request explicit rendered before/after comparisons. Four changes are accepted at 1971, followed by a request for twenty more, clarified at 1976 as changes to structure, ordering and language. All twenty are accepted at 2169 and reported applied at 2194. The saved comparison records six formal statements and 48 displays unchanged.

`APPROVED-EDIT-EXAMPLES.md` preserves all twenty exact pairs. The most instructive short pairs are:

* Before: "The first three terms vanish at T_* ... We show that the quotient ..." After: "To prove isolation, we show that S_M(T)/(T-T_*) is a local unit ..." The purpose precedes the factorization.
* Before: "The cap inequality is now s>h" after the transformation. After: "To transform the moving cap into s>h, put ..." The destination precedes the definitions, and the repeated destination disappears.
* Before: estimates appear before the definition of F. After: "For z=..., set F(z,a)=..." begins the paragraph. The reader knows what is being bounded.
* Before: "The series is bounded at the source width; the left diagonal costs a strip power." After: "The Neumann series costs no strip width; [the diagonal inverse] has polynomial cost across a gap." Each cost has a named owner.
* Before: "A finite-mode and tail split proves the limit". After: "Dominated convergence proves the limit for the diagonal inverse", preceded by the summable majorant. A standard theorem replaces procedural narration while its applicability remains visible.
* Before: the final paragraph derives "analytic and strictly convex" after the pole argument. After: C2 closeness supplies convexity and the graph at the poles supplies analyticity in separate sentences. The reasons are attached to the conclusions they support.

## Figures and the final abstract, 27 October

At 2196 the user asks for generated mathematical figures without image generation. At 2214 aesthetic skills are explicitly limited to minor visual guidance. At 2338 the user chooses deformation, waterline and noncritical modes. At 2355 readable sizing takes precedence over reaching ten pages. The illustrated paper reaches eleven pages.

At 2394 the user offers a friend's alternatives; at 2421 the formula-heavy noncritical panel is criticized. At 2430 the user corrects premature implementation: an opinion was requested first. At 2442 the user asks to see figures in paper context. At 2509 the user authorizes a resonance panel inspired by the alternative and the additional dimension plot if it fits. The integrated version retains four full-width figures at eleven pages. The final figure audit distinguishes illustrative first-order bodies from exact solutions and finite spectral samples from infinite-mode proofs.

Positions 2610, 2613 and 2617 concern updating a shared Overleaf project; the initial new-project advice was corrected by an extracted update bundle. No mathematical edit follows from these turns.

At 2624, 2631 and 2636 the user challenges Figure 2's location. It moves from beside the introduction's corollary to immediately after the argument verifying the quartic hypotheses in all dimensions. The text now concludes that application, introduces the heights/densities plot, and explicitly returns to general resonances afterward. The figure placement follows the question answered by the text, not merely the first occurrence of a related formula.

At 2679 the user requests title and abstract comparisons. "Analytic symmetric floating bodies" is proposed. At 2734 the user chooses "a degree-four spherical resonance"; at 2737 the user requests a full stop after "deformations" and a new sentence beginning "To obtain actual bodies". The updated proposal is saved at 2763. The canonical source still says "Symmetric floating bodies". Do not report the proposed title as already installed.

## Which changes mattered most

HUNCH, in descending value for the Barnette rewrite: first remove unnecessarily strong intermediate targets; next choose one proof route and preserve its exact obligations; then put objectives before constructions and prerequisite proofs before their consumers. Consolidate repeated calculations and retain only used coefficients. Give the inverse or cancellation lemma a complete reusable contract. Audit notation by mathematical type. Finally refine abstract, figures, and page layout in context.

The success criterion is not six pages. The four-dimensional version reached six, the broader theorem needed nine, and readable figures justified eleven. The checkable method is to show, for each deletion, that its mathematical obligation vanished or has an explicit surviving source; for each addition, name the reader's unanswered question it resolves.
