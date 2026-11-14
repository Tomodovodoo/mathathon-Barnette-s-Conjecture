G and X remain open; this is a partial result, not a cancellation-free proof of Barnette's conjecture.
PROVED-HERE: the Hall identities, exact four-/five-cycle obstruction, coloured disk curvature, and G without chordless five-cycles.
REFUTED: innermost bad-disk descent at V=11, five-cycle-only descent at V=13, and its blocked-source refinement at V=14.
REFUTED: mate repair at V=16, single-cycle repair at V=17, and every fixed-cover direction repair at V=18.
COMPUTED: formulas through V=14, G structure through V=19, corner avoidance and the global half-exception bound through V=18.

# Report

gpt-6-astra, 14 November 2026. All writes are confined to this assigned folder. No subagents or external services were used. The new proofs are T2 unreviewed. Aggregate census results are T4; decisive certificates have separate reference-engine checks, not an independent referee's approval.

## What I set out to do

Complete G and X in the degree-4 induction, beginning with the unverified deficiency formula and the proposed innermost-cycle descent. For X, search corner-avoidance and local-pattern hypotheses, and test repairs of exceptional matchings using mates and D-cycle reversals. The prior Opus and Fable proof files, their experiment interfaces, the named referee results, and the supplied OpenAI text guided the tests. The paper was read through `papers/text/OpenAI-Barnette.txt`; this was not a visual PDF audit.

## What is established

PROVED-HERE. `G.md` derives the connected-complement identity

    f(S)=sum_F (d_F+w_F-6)/3

and both Hall formulas under contraction. The derivation retains repeated boundary sides and the connectedness premise. Symbolic elimination gives zero residual. The independent embedded-walk computation checks 699,666 eligible colour/subset instances through V=14, including 443,092 repeated-boundary region occurrences. The contraction formulas pass 6,202,336 subset checks over 15,496 rooted merges through V=14.

PROVED-HERE. With no separating triangle, parallel edges after contraction are witnessed by a chordless four-cycle through x and its opposite neighbours. A new black-inner separating triangle in a simple contraction is witnessed by a chordless **five-cycle** whose inner boundary has four black incidences and one white incidence. This corrects the four-cycle-only picture in the proposed task route. All 1,050,032 rooted merges in the separator-free census through V=19 agree with the criterion, covering 62,416 rooted instances.

PROVED-HERE. Coloured disk curvature gives `2 n4 >= 6-c`, where c counts changes of boundary-incidence colour. In particular a chordless four-cycle has at least one degree-4 interior vertex; a five-cycle has at least two. G follows when there is no chordless five-cycle, since a simple merge then cannot lose its pair.

REFUTED. The desired non-apex conclusion does not follow from this curvature. Each degree-4 singleton is already a minimal tight set, with its vertex an apex at every edge of its link. More strongly, V=11 graph 1 has an innermost bad four-cycle with one interior vertex and two blocked merges at that vertex. Independent flow gives value 11 instead of 12; both negative Hall sets are saved. Restricting to innermost bad five-cycles also fails at V=13 graph 4. Requiring the source vertex to have both merges blocked still fails at V=14 graph 22. Both interior degree-4 vertices there are blocked as well.

REFUTED. For X, the first decisive new obstruction is V=18 graph 80, root {8,0,1}, x=15, merge {14,9}. One cover of the contraction has a single 13-cycle and one tree matching, which is exceptional. Its other orientation is cyclic. Any D-cycle reversal sequence stays in that cover. Thus even arbitrary direction changes cannot repair this exception. Other covers do contain successful lifts. `data/cube_witness.json` gives all 22 states' aggregate counts, the ten ordered pairs' aggregate count, the eight tree matchings' classification, and the exact obstructing pair and Q-cycle. The reference lab independently verifies it.

COMPUTED. All 7,940 exceptions through V=18 were examined. Mate repair fails for 646 exceptions, beginning at V=16. A single D-cycle repair fails for 222, beginning at V=17. At V=17 the two-cycle witness can be repaired in two steps; the per-cover half bound already fails there. At V=18, 220 fixed covers have all their tree matchings exceptional. Nevertheless the half bound for the **whole contraction** passes every contraction with exceptions, with maximum exceptional fraction 1/2. Corner avoidance passes 594,884 bounded-black-face tests over 41,102 rooted instances with tree matchings. Both surviving statements remain conjectures.

PROVED-HERE. `PARTIAL.md` states the cancellation-free certificate theorem: octahedral leaves, pair-compatible separator gluing, and one-sided contractions suffice. `AUDIT.md` supplies the bounded reverse-Lamport graph. It does not assert that every graph has such a certificate.

## What failed and why

G's local counting facts are sound. The jump from an interior degree-4 vertex to an interior **good** vertex is false. A blocked vertex's next obstruction can leave the current disk. The exact obstruction classification is complete, so the missing ingredient is a global selection or uncrossing argument, not a few omitted local colour cases.

X's exception is global connectivity data. Replacing a matching by its mate need not preserve a tree. Reversing one cycle can fail, and even the entire orientation cube of a fixed cover can fail to escape the exception set. A proof must sometimes change the unused corner map. The directed-cycle criterion explains which orientation fails, but does not supply such an exchange or a decreasing potential.

The proposed statement "all four local patterns occur" fails already at V=8. Corner avoidance survives, but it was already Opus's S7, not an untested strengthening. I found no inductive transfer rule for it. Evenness and the signed `2 c_min` bound give sufficient numerical conditions when e is small; they do not bound e and would import cancellation.

There is also a logical correction. The strict inequality `TM(T/M)+TM(T/N)>2e` is sufficient for a tree matching of T. The earlier Theorem 4(c) does not prove the converse. This report uses only the sufficient implication.

## What remains open

G in general; X in the two-sided case; the global half-exception bound; and corner avoidance with an inductive proof. The finite tests do not close any of those unrestricted statements. New proofs and scripts need an external referee before integration as established project results.

## Three best next steps

1. For G, compare crossing short-cycle obstructions at vertices with both merges blocked. Use the V=11, V=13 and V=14 certificates to reject inward-selection rules before attempting an arbitrary-size proof.
2. For X, work on V=18 graph 80 and explicitly move from its exceptional one-cycle cover to the successful three-cycle cover. A rule confined to orientation bits has been ruled out. Require a progress measure for the cover-changing move.
3. Independently referee G.md and replay the three decisive finite certificates. Then test any new global repair against the full 7,940-exception fixture before extending the census. More confirmation of the same inequalities is less useful than a new exchange or selection lemma.

## Leads for others and handoff

The exact short-cycle criterion and coloured curvature can replace the unverified Hall sketch in the induction exposition. The fixed-cover counterexample belongs beside the directed-cycle criterion and lattice discussion, since it identifies precisely what the direction-choice approach cannot repair.

Exact commands and validation limits are in `code/README.md`; data hashes are in `data/sha256.json`. The local dashboard and map are handoff copies only. Shared canonical maps, other research folders and the reference lab were not edited. The work was committed in scoped commits, and the final git outcome is recorded in the chat handoff.
