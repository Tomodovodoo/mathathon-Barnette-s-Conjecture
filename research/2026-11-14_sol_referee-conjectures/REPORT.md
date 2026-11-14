REFUTED: R2 fails at V=33 by gluing two V=18 witness regions; all ten extreme/irreducible candidates fail.
COMPUTED: the V=18 C2 minimum and its four-element lattice pass independent exhaustive verification.
COMPUTED: C1 and its equality pattern pass all 4,656,948 feasible rooted instances through V=22.
PROVED-HERE: the two cancellations are a directed-cycle reversal between decorated ideals and a Boolean finite difference within each ideal.
GAP: testing a specified pair is linear; finding a successful direction choice for an arbitrary factor is not made polynomial by the criterion.

# Referee report

gpt-6.1-sol, 14 November 2026. Work is confined to this assigned folder. No subagents were used. No author verification code or earlier referee engine was run. All source code here is new; the author's random generator supplied only the V=70 input. The OpenAI source was read through its supplied text extraction, including the section 5 formulas, rather than a visual PDF audit. The requested running-example path was absent; the identical graph was recovered from two saved face fixtures and checked at the same root.

## What I set out to do

Audit the conjecture report independently, verify the exact full-lattice counterexamples, test the directed-cycle criterion, hunt R2 in structured families, and determine whether the two cancellations become a general distributive-lattice identity or an efficient construction. REFEREE.md contains the per-claim verdicts and reverse-Lamport dependency table. LATTICE-READING.md contains the exact signed sums and full new arguments.

## What is established

`COMPUTED`. The V=18 witness has 54 states, 20 ordered pairs, four factors and 12 tree pairs. The lattice is a diamond. Both extremes have one 15-cycle and no tree direction; the two middle factors have cycle lengths 3,5,7 and six tree pairs each. Every vertex-deletion set of size at most three leaves it connected. Each extreme spoke orientation has exactly two directed cycles, both facial hexagons, blocking its two directions separately. The full all-root plantri census through V=18 finds exactly the author's 26 failures there and none earlier.

`PROVED-HERE`, submitted results independently checked, T2 with this AI referee and human check pending. The difference-constraint proof, shortest-path extremes, directed-cycle criterion and unique-factor equality argument close. The moment barrier closes after narrowing it to low-degree vanishing plus existence of a nonzero minimal-degree moment. The stronger full-prescribed-moment reading is not established.

`COMPUTED`. Seven of the nine earlier greedy terminals equal neither lattice extreme. The other two are the reported genuine minimum and maximum failures. The V=24 distance-two and V=60 tree-free-chain witnesses pass full independent lattice reconstruction. The V=70 minority witness has exactly 654/1410 successful elements, 483,960 pairs and 71,180 tree pairs, now independently confirmed.

`REFUTED`, new result. R2 fails in an explicit V=33 triangulation with a white-inner separating triangle. Its lattice is B_4, with 16 elements and four successful elements, all at rank two. None of its two extrema, four join-irreducibles or four meet-irreducibles carries a tree pair. A second program independently enumerates all 2,916 states and all state pairs, confirming 400 pairs, 144 tree pairs and zero success on all ten candidates. The graph, potentials and Hasse covers are saved in `data/R2_glued_V33.json`.

`PROVED-HERE`, T2 unreviewed, conditional on the explicit finite V=18 base certificate. Inserting a black-rooted witness into the rigid white face (1,2,9) splits pairs and tree pairs and gives a product lattice. Repetition yields dual order 15q+3, lattice B_(2q), 20^q pairs, 12^q tree pairs and successful fraction 2^-q. Successful elements have rank q and distance q from either extreme. For q>=2 the family refutes R2, R3 and R5; it also rules out every fixed cover-distance replacement. Direct checks at q=1,2,3 agree. This reduces the known R3 and R5 counterexample orders from 60 and 70 to 33, without asserting minimality.

`COMPUTED`. The independent C++ census through V=22 covers 243,547 triangulations, 9,531,638 facial roots, 4,656,948 feasible rooted instances, 6,436,022 factors and 49,325,864 ordered pairs. It finds 45,375,214 tree pairs, no C1 violation and 3,320,987 equality cases. Equality occurs exactly at singleton lattices. The C++ factor method and Python all-state-pair method agree on every row through V=18. This independently reproduces the author's whole C1 range.

`COMPUTED`. C3 holds for all 24,744 ordered pairs at all rooted instances through V=16, plus all pairs of the saved V=50 and V=30 plateau traps. The author log's 940 random starts were inspected but not rerun in full. Independent R2 family tests include 16 specified tube roots, five prism sums and three witness sums.

`PROVED-HERE`. The exact signed sum over J(P) must retain the cycle-direction fibre at every ideal. The first involution reverses a directed spoke cycle, exchanges u and r there, and preserves s. The second sum is a Mobius finite difference on each Boolean direction fibre, not the rank or Mobius sum of the base lattice. The unit-face integer-weight polynomials and their leading coefficients are checked explicitly on the octahedron, hexagonal-prism dual, V=13 running example and V=18 witness. The height-product proof retains the same positivity mechanism as the refereed proof; it does not become a shorter general order-theoretic proof.

## What failed and what remains open

`REFUTED`. Universal R2 and any fixed bound on distance from the extremes fail under rigid-face witness gluing. The targeted family reveals a failure mode that the random campaign missed. It does not refute R2 restricted to triangulations without separating triangles. The independently tested tubes all pass that possible restriction.

`REFUTED` as a proof route. The ordinary rank polynomial or interval Euler characteristic cannot determine the signed pair sum. Two singleton lattices already have different signed polynomials. The Boolean finite-difference operation is real and useful, but it acts on the directions above a lattice element and still needs the cycle disks and disk identity.

`GAP`. A specified pair is tested in linear time by cycle search. The question whether a fixed u carries SOME tree pair still asks for one consistent orientation choice across all D-cycles. The exact dangerous-cycle clauses may have exponentially many members. The criterion gives linear verification of a full choice and no polynomial search algorithm for the restricted clause family. No hardness theorem for that special planar problem is claimed.

`CONJECTURE`. C1, strict inequality for nonsingleton lattices, and C3 remain open globally. Their finite tests are not promoted to proofs. A barrier for the complete prescribed-moment family of Theorem B remains unproved. The full original V=19..24 extreme/irreducible census was not repeated, so its reported counts remain source computations beyond this audit's independent range.

## Three best next steps

1. Obtain an outside check of the V=33 certificate and the rigid-face product lemma, then replace universal R2 by a question confined to separator-free pieces. Keep the failed unrestricted conjecture visible.
2. Study the special direction-choice SAT problem from LATTICE-READING.md, section 7. Either exploit planarity and the state constraints to solve it, or prove hardness on this exact class; generic subcube-covering hardness is insufficient.
3. Retain C1 and its strictness conjecture as the counting target. Use the singleton base proof and distinguish the full prescribed N(w) identities from their much weaker moment-vanishing consequence.

## Leads for others

The exposition can use one orientation picture for Lemma 5.2 and the forest criterion, then show the Boolean finite difference over each fibre. It should not label the base-lattice rank polynomial as the nonvanishing object. The V=18 example explains why one canonical factor fails; its rigid-face double explains why all extrema and irreducibles can fail together. The source's R2 finite evidence is compatible with the new refutation, since the new example has V=33 and no minimum-order claim is made.

All commands, output scopes and hashes are in `code/README.md`, `data/README.md` and `data/provenance.json`. Jobs were under ten minutes. One accidental brief overlap of two C++ counters was cancelled; the retained final census came from a subsequent serial run. No process was left running. Shared canonical maps and other agents' files were left untouched for the coordinator to integrate.
