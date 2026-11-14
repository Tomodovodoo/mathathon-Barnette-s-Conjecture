1. PROVED-HERE: a complete informal primal proof is in proofs/primal/PRIMAL-PROOF.md, with matching amsart TeX and PDF.
2. The proof uses root-free cut shores, four counts, one vertex-charge flow, a real-sign linear polynomial, direct matching recovery and prescribed-edge induction.
3. COMPUTED: 270 rootings, 1,722 states, 640 pairs, 1,388 state-circuit occurrences, 1,908 recoveries and 172 compatible cap gluings passed exact checks.
4. The cube and a 20-vertex cancellation example list every face, edge, state, pair, weight and recovered matching; actual Lean headers and a claim-by-claim status table accompany them.
5. The reverse-Lamport self-audit closes under stated elementary planar facts; this is not independent review or a new machine-checked proof, and face incidences still encode cycle-cut duality.

# Report

## What I set out to do

Write the complete argument in the cubic bipartite graph G and its faces, using the simpler devices of the checked Lean proof, then compare that route with the dual and Li presentations. Work was confined to this research folder and proofs/primal/. No subagents were used.

I read the repository protocol, the local unslop and reverse-Lamport skills, the requested Lean reports and declaration skeleton, actual Lean statements in the existing upstream clone, the supplied paper texts, the local combinatorics and determinant referee proofs, and the structural route report. The structural referee's REPORT.md was still marked under review on the final check. I therefore use none of its unissued verdicts. The source commit was verified by git as 4eaee87548250b2682affda7d05d947c05554bae.

## What I established

PROVED-HERE. The note proves the stronger working theorem: every finite simple cubic bipartite 3-edge-connected plane graph has a perfect matching containing any prescribed edge and having connected complement. It then gives the short conversion from 3-vertex-connectivity and obtains the original Hamiltonian conclusion. All thirteen lemmas have full written proofs.

The first-pair argument is Li's minimal-deficit proof, with its balance condition, induced-subgraph step, connectedness and nontrivial-cut witnesses made explicit. It avoids relying on the extra claim that a connected union of facial cycles is 2-connected. The note uses the ordinary nontrivial-three-cut induction rather than the sharper colour-sensitive structural result.

The disk lemma has exactly the four-count form in StateDisk.lean. Its planar support is isolated: a face circuit is a bond, deleting a connected shore merges precisely its incident faces, and a facial boundary meeting both shores contains a cut edge. The proof states Euler and the elementary plane-embedding operations it accepts. There is no detoured spoke curve or Jordan labelling.

The flow runs from the root black vertex to white vertices. This corrects the potentially misleading phrase "root face to white faces" when translated from the dual commentary. Its local potentials have positive slope on each positively oriented state circuit. The signed polynomial has linear factors. The exact signed value three aligns minimal groups; oddness alone handles the cancelling involution and the final matching-cut contradiction.

The recovery tree lies in G. Taking the parent edge at each white vertex constructs the perfect matching explicitly. The proof that its complement is connected is the Lean matching-cut balance argument. It ends the Hamiltonian proof directly, without proving the two-induced-tree theorem first.

COMPUTED. The numerical run imports the lab only for graph generation and facial-walk enumeration. All proof objects are recomputed in the primal checker. The input manifest contains 16 records, 15 generated classes plus a repeated named cube, orders 8 through 20. Every vertex is a root, giving 270 rootings. The run checked:

- 96,640 capacity subsets, 1,722 states and 640 ordered pairs;
- 1,140 pair-related state circuits and 248 arbitrary-choice state circuits on graphs of order at most 12;
- 216 nonempty pair spaces with exact polynomial lowest coefficients;
- 442 arbitrary bonds on the small graphs, and 4,196 matching-cut balances across 988 primal perfect matchings;
- all 1,908 forest-state/root-edge recoveries;
- 278 three-edge cuts, 16 caps at the eight nontrivial cuts, and all 172 compatible cap-cycle pairs.

The worked cube polynomial is -z. The 20-vertex example has nine states, ten ordered pairs and polynomial 4z+9z^2-2z^3-9z^4-2z^5. Its cancelling second state has two partners of opposite sign. Its Q circuit bounds the singleton white shore {12}. The two full second-state weight polynomials cancel exactly.

The Markdown and TeX contain the same proof and exact examples. The note uses amsart, A4 paper and a one-inch margin, and compiles to 12 pages. I rendered all pages and inspected the contact sheet and dense example pages. Long inline lists have discretionary breaks; there are no overfull boxes. The remaining underfull-page warning is harmless white space, not lost or clipped text.

## What failed and why

No mathematical gap was found in the final self-audit. This does not give independent referee status.

The first example builder reinserted graph edges in sorted order and thereby obtained different face labels from NetworkX. It now reads the exported facial boundaries directly. The first TeX attempt used nonscalable default fonts with microtype; adding Latin Modern fixed the build. The first aligned equation placed its tag inside the aligned environment; the tag now belongs to the outer display. These were implementation and typesetting faults, not changes to the mathematical proof.

The proposed simplification does not remove planar duality in substance. A face circuit is exactly the incidence object usually regarded as a cycle in the dual graph. This limitation is stated on the first page and developed in COMPARISON.md. The result is a distinct exposition and recovery route, not a claim to an independent proof principle.

## What is still open

Independent review of the primal rewrite remains. In particular, a referee should read the elementary plane-embedding calculus in Lemmas 1 through 3 and the explicit Li deficit proof without relying on the Lean provenance as a substitute.

This agent did not rebuild Lean or formalise the real-sign variant. The earlier Lean agent's build and its statement verification remain the source for the machine-check report. The current work records actual declaration headers and marks the two main departures honestly.

The numeric census depends on the existing plantri binary; the graph manifest is explicit, but this agent does not certify generator completeness. No complexity improvement or practical algorithmic advantage is claimed.

## Three best next steps

1. Independently referee Lemmas 2 through 4 and the orientation convention in Lemma 6, the portions where the prose changes the representation or proof of a Lean statement.
2. Adopt the one-flow lemma and the direct matching recovery in the final paper. They remove the longest unnecessary geometric construction and the induced-tree detour.
3. Draw the cube's primal recovery tree and the 20-vertex example's singleton cancellation shore, keeping face-sector signs and vertex-flow arrows in separate panels.

## Leads for others

The sharp black-inner-cut obstruction is unnecessary for this complete route. The deficient-set proof does recover its sufficient direction, so the structural team can reuse that argument after its independent review is complete.

The real polynomial is a convenient common language for Lean, the determinant referee and Li. It supplies the full multi-cycle nonvanishing argument without an appendix of marked involutions. The exact sign formula is included in equation (6.3), not inferred from a computation.

## Deliverables and reproducibility

In proofs/primal/: PRIMAL-PROOF.md, primal.tex, primal.pdf, EXAMPLES.md, STATUS.md and COMPARISON.md.

In this folder: AUDIT.md, check_primal.py, build_note.py, extract_lean.py, LEAN-EXTRACTS.md, README.md, logs and outputs/. README.md gives the commands that produce the data and note. STATUS.md gives each lemma's source category and exact finite check range.

Commits made during the work include 88e5423, the scoped work log, and f2a6fdd, the proof and first complete checker. A final scoped commit records the audit, status, comparison and final verification. The protocol's push to origin/main is attempted after that commit; its result is reported in the final handoff.
