# Research report

The Corollary 7.2 audit gap is closed at the named-theorem boundary: GSW 4.16 applies exactly.
Heawood and three nonplanar trisums pass exhaustive P4 checks and explicit Pfaffian-sign searches.
The root-free Heawood torus polynomial is identically zero despite odd-cycle cancellation surviving.
The six trisum path signatures give a one-step gluing proof; dual four-cut patterns are a different interface.
A direct nonplanar states proof remains open; new proofs and computations need independent review.

## Task and result

LIT plus PROVED-HERE conditional inference. `GSW-CHAIN.md` records complete restatements, theorem numbers, sources, and a bounded reverse-Lamport table. Verdict FOLLOWS assumes OpenAI Theorem 1.1 and the opened GSW named theorems. GSW 4.4 supplies planar P4-Hamiltonicity from the universal planar theorem; 4.9 and 4.12 supply the Pfaffian brace induction; 1.7 lifts through tight cuts. OpenAI Corollary 7.1 is not needed. No extension of the Lean formalisation was attempted.

COMPUTED/T4. The seven test inputs are cube, hexagonal prism, Heawood, cube trisum, cube/cube/prism trisum, nested cube trisum, and K3,3 control. All are cubic, bipartite, 3-connected and 2-extendable. GF2 matching-sign equations find a Pfaffian orientation for the first six and reject K3,3. Every three-edge path extends in all seven. Separate DFS counts agree with perfect matching complement enumeration. The four nonplanar Pfaffian examples have respectively 24,12,16,24 Hamiltonian cycles and 84,96,120,144 unoriented P4 paths. See `data/results.json` and `data/verification.json` for certificates, edge lists and exact counts. These are named examples, not a census of all small Pfaffian graphs.

PROVED-HERE/T2. `PROOFS.md` gives the signing certificate argument, the failure of constant Pfaffian signs to cancel disconnected complements, the genus-dependent cardinality obstruction, the root-free torus forest obstruction, and a corrected six-signature Hamiltonian assembly lemma. It also proves that literal retained piece faces fail before the states can be defined.

## What failed and why

REFUTED, with COMPUTED/T4 witness. The prediction that Heawood's root-free torus pairs would have even D cycles was wrong. There are 24 states and 48 pairs; every D is a seven-cycle. All Q cycles are odd too, and every state's two partner contributions cancel. The resulting polynomial is identically zero. The delta sums are plus/minus 1 and 7, not plus/minus 3. This isolates nonvanishing as the first failing step after restoring equal state cardinality. The literal rooted construction fails earlier, with domain size six and codomain size four.

REFUTED, PROVED-HERE/T2. Piece faces minus the glued cycle are not a valid incidence system in a cube trisum. Most are no longer cycles, their number is wrong, and shared vertices have six incident labels rather than three. Perfect matchings of G itself do give nonzero Pfaffian determinants, but those signs count disconnected complements positively as well.

COMPUTED/T4. Replaying the categorical code on all seven Eulerian triangulations through eleven vertices checks 524 rotated cut sides: 108 chordless ++-- cases have six patterns, 24 chorded ++-- cases have five, and 392 alternating cases have six. Thus the unqualified six-pattern assertion needs the chord exception. This replay is not an independent implementation.

PROVED-HERE/T2, using named Pfaffian no-cross theorems. P4-Hamiltonicity supplies the six correct primal path signatures at a summand's four-cycle. Twelve ordered triples glue to one spanning cycle. That establishes one-step trisum Hamiltonicity. Recursive closure of all signatures, or preservation of a prescribed P4, still needs a stronger invariant such as GSW 4.12. The categorical proof itself uses Corollary 7.2, so treating it as an independent way to derive that corollary would hide a dependency cycle.

## What is open

HUNCH/T6. A direct states proof may need homology or boundary-connectivity weights and a cyclic spine target. No useful nonvanishing sign was found. Crossing-parity drawings alone do not supply the required incidence structure; no drawing enumeration was performed. Torus embeddings of trisums were not enumerated because the rooted cardinality and root-free forest obstructions already apply analytically. The original RST, McCuaig and Hertel proofs were not independently audited; GSW's exact named statements are the accepted boundary.

## Three best next steps

1. Independently referee the short proofs and replay the stored signing and torus certificates, focusing on rotation conventions and the no-cross application.
2. Try a homology-sensitive polynomial on the explicit Heawood rotation that retains cyclic states with connected primal complements; test coefficient nonvanishing before building a general theory.
3. Formalise the six boundary signatures and GSW's prescribed-P4 trisum closure, correcting the v3 textual slips documented in `GSW-CHAIN.md`.

## Leads for others and provenance

The dependency auditor can replace the unopened-GSW leaf by the discharged application in `GSW-CHAIN.md`. The categorical author should keep the chord exception and distinguish dual cut patterns from primal trisum signatures. The Lean exposition should retain the hypothesis that face circuits are bonds; cut terminology alone does not remove planarity.

Predictions were committed before testing. New results remain unreviewed. No subagents were used. All writes stay in this assigned folder. The local map tracks one closed audit question and three failed literal direct constructions, with the broader direct route left open. The dashboard is local only.
