# Coordinator notes

Session started 2026-11-14 about 10:00 UTC (machine clock 11:00, user clock 02:00). The user expects work until about 16:00 UTC (machine 17:00). From 14:05 UTC shift to cross-audits and cleanup.

## Standing orders

- Keep about eight delegated agents running. Models: `codex` (gpt-6-astra, gpt-6.1-sol), `claude-ai1`, `claude-ai`, `claude-dev` (claude-fable-5-2, claude-opus-5-5). Rotate providers.
- Mostly broad exploration. Some cross-audits, always by a different model than the author.
- Every brief starts by pointing at `research/BRIEF.md`.
- On every wake: read finished reports, update `INDEX.md`, `git fetch`, merge or fast-forward, `git push origin main`.
- Agents commit only their own paths. The coordinator owns `research/INDEX.md`, `research/COORDINATOR.md`, `README.md`.

## Wave 1 (launched 10:15 UTC)

See `INDEX.md`.

## Queue (launch as slots free up; adapt to what wave 1 found)

Exploration
1. Wild routes A, statistical mechanics and dimers: Z(x) as a twisted double-dimer partition function, Kasteleyn determinant with a U(1) or SL2 connection, Lee-Yang zeros, transfer matrices.
2. Wild routes B, topology: trinity and sutured Floer homology (Juhasz-Kalman-Rasmussen), hypertrees and the interior polynomial, discrete Morse theory, Heegaard-style or knot-theoretic reading of states, winding number reading of the disk identity.
3. Wild routes C, algebra: Alon-Tarsi and the combinatorial Nullstellensatz, graph polynomials, permanents and determinants, Penrose polynomial, mod-p counting, Pfaffian braces (Gorsky-Steiner-Wiederrecht) and the non-planar corollary.
4. Category theory and reformulation: what a categorical statement of the tree/matching/duality correspondences looks like, and whether it buys anything.
5. Generalisations and limits: which hypotheses are needed (non-simple, 2-connected, other surfaces, non-bipartite with Tutte's graph as test, higher genus, Eulerian triangulations with separating triangles of each type). Counterexample hunting by computer.
6. Counting consequences: how many Hamiltonian cycles, lower bounds, the number of tree matchings, asymptotics on families (prisms, nanotubes).
7. Primal-language proof: the whole argument written in G with no dual, compared with Li.
8. A second, independent implementation for cross-validation of `workings/barnette_lab/`.

Synthesis and writing
9. Labyrinth map: `labyrinth/` with knowledge graph, events, state of the art and dashboard built from the reports.
10. Route map: one graph of every proof route found, nodes and edges, with status (reverse-Lamport style), plus a rendered figure.
11. Digestions: one per major step (dual reduction, states and pairs, disk identity, cancellation, positivity, recovery, gluing), written for a graduate student.
12. Manuscript drafts in `paper/` following the style guide from the exposition-method run: two competing drafts by different models, then a merge.
13. Unslop pass and notation audit on the manuscript.

Cross-audits
14. Referee each wave-1 report with a different model (own code, own reasoning).
15. Reverse-Lamport audit of the manuscript draft.
16. Figure review in context (scale against text width, legibility).
