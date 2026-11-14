# Research report

The older radial-tree method maps to a colour-restricted induced-tree partition, not directly to H-s.
The proposed BF21 parity identification is refuted by the truncated octahedron.
Prescribed-edge inclusion follows directly from avoidance and cubicity; all 138 named-graph edge tests passed.
Goodey octahedral chains have unbounded c_min with separators; a direct Pfaffian state transfer remains unsupported.
Novelty is best attached to the paired-state cancellation/nonvanishing mechanism, with explicit source-access limits.

## Task and deliverables

I investigated the seven requested historical routes, read the available source passages and the supplied OpenAI proof, and tested the proposed identifications using the reference lab without editing its source. BRIDGES.md contains the dictionaries, exact stopping points, proofs and the bounded Pfaffian-transfer audit. NOVELTY.md contains proposed introduction text and exclusions. TESTS.md records predictions and results. SOURCES.md records editions, inspected sections and inaccessible originals. older-routes.dot uses the existing 14 core node identifiers. Reproduction scripts and JSON outputs are in code/.

## Established here

PROVED-HERE, T2 unreviewed. The quasi spanning-tree dictionary passes through the original dual's colour-restricted permeating tree. Its radial graph is not the triangular spoke graph. The truncated-octahedron contraction proves that BF21's even-interior hypothesis and the black-inner obstruction differ. A prescribed included edge follows from prescribing avoidance of an adjacent edge. End-rooted chains of k octahedra have only pairs with k D-components, while their primal faces have sizes four and six.

COMPUTED, T4 unreviewed. All 262 facial roots of the 15 Eulerian triangulations of orders 6–12 agree with the lab's pair/black-inner obstruction criterion. Same-T parity gives 78 rooted-separator discrepancies. The four/six census through dual order 16 has 18 graphs. Two refined Goodey examples separate minimum D-component pairs from forest pairs. Chains k=1–8 confirm the stated formula. Edge forcing succeeds on all 138 edges of four named graphs. Matching enumeration gives 24 Heawood Hamiltonian cycles and 12 for the 16-vertex cube trisum, with all three-edge paths extendable. K3,3 is retained as a non-Pfaffian Hamiltonian control.

LIT. GSW already proves the equivalence needed for O's nonplanar Pfaffian corollary. The direct-transfer question is about a proof, not an additional Hamiltonicity theorem. Kardoš's resonant-hexagon flip acts on a primal 2-factor, whereas Q reversal fixes s and cannot change its recovered cycle. Berman's determinant count of single states predates the new proof.

## Failures and limitations

REFUTED. The literal parity identification does not survive the truncated-octahedron example. Minimizing D-component count does not select a tree pair even in Goodey graphs. A face-size bound of six does not bound c_min when separators remain.

The original Goodey, Tutte trinity, Berman, Kelmans, Tutte path, Thomassen and HMM papers were not all accessible. Their source-access limits are listed rather than hidden behind citations. Feder–Subi's original text extraction was unusable; its first page was inspected visually and a readable 2008 author revision supplied the detailed definitions. I did not audit every page of every downloaded PDF, rerun historical computer certificates, exhaust all contractions, or certify the computations independently. No claim that the historical search is exhaustive is made.

The literal Pfaffian state route lacks balanced incidence objects, a disk identity and recovery on a nonplanar embedding. The bounded audit rejects that proposed route, not the already established consequence through GSW. No new canonical forest constructor was found.

## Three best next steps

1. Independently referee the radial-tree dictionary, contraction counterexample and octahedral-chain proof, then integrate the corrected historical statements into the exposition.
2. Study c_min and canonical selection specifically on separator-free Goodey graphs. The chain obstruction says nothing about that narrower class; the refined examples still rule out minimum-cycle selection as a general rule there.
3. Obtain original Goodey, Tutte and Berman texts and search their citing literature before using "first" in the novelty paragraph. For the nonplanar proof route, begin with explicit incidence objects on Heawood rather than assuming a Pfaffian orientation supplies them.

## Leads for others

PROVED-HERE. A useful expository bridge is the exact distinction between three trees: the radial tree after a face-colour contraction, the deleted-spoke tree, and its white-face cotree. Give each a different symbol. They share planar boundary arguments but not their vertices or constraints.

HUNCH. The four-port path patterns in GSW's trisum proof and Schnieders's boundary certificates are natural inputs to the categorical route. They are closer to each other than either is to the signed state exchange.

## Integration and git

Only this assigned folder is staged and committed. All proofs remain unreviewed and all computations T4. Canonical labyrinth files and other agents' work were not edited. The local map and event files are a handoff, not updates to the coordinator's state-of-the-art table.


COMPUTED/T4, final spot check. `code/validate.py` verifies the radial/permeating-tree predicate equivalence on 39,714 nontrivial vertex subsets across all 15 duals of orders 6?12, and verifies all 108 black-band face incidences used by the chain proof through k=8. This is an author check, not independent review. Output: `code/validation.json`.
