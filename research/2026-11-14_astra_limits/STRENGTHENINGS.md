# Strengthenings

Status follows HYPOTHESES.md. COMPUTED is T4 evidence pending independent review. PROVED-HERE is T2, unreviewed. The results below distinguish consequences of the supplied proof from conclusions checked only on a finite corpus.

## What the proof gives

PROVED-HERE. A Hamiltonian cycle through any specified edge e follows immediately from single-edge avoidance. Choose another edge f incident with one endpoint of e and construct a cycle avoiding f. Cubicity forces the cycle to use the other two edges there, including e. In fact this forces any prescribed two-edge path, the P3 property. No second run of the forest machinery is needed.

LIT. Gorsky, Steiner and Wiederrecht, "Matching Theory and Barnette's Conjecture", Discrete Mathematics 346, 2023, 113249, arXiv:2202.11641v3, Theorems 4.4 and 4.16, establishes equivalence with P4-Hamiltonicity and extends it to cubic 3-connected Pfaffian bipartite graphs. The full HTML statement was opened at https://arxiv.org/html/2202.11641v3 . Conditional on the supplied Barnette proof, this is a theorem, not an open strengthening. The original manuscript explicitly invokes it in Corollary 7.2. The local state recovery alone is not presented as a direct P4 constructor.

LIT. Kelmans' same-face include-one/avoid-another equivalence is recorded on Bojan Mohar's problem page, https://www.sfu.ca/~mohar/Problems/P4BarnetteConjecture.html . This page is a literature lead rather than the original proof; no new global theorem for arbitrary two edges is asserted here. Cofacial and arbitrary edge pairs must not be conflated.

## Finite tests

COMPUTED. The command `python research/2026-11-14_astra_limits/code/campaign.py 14` tested 55 isomorphism classes of Barnette graphs, all those dual to plantri Eulerian triangulations on at most 14 vertices, hence primal order at most 24. Counts by dual order 6 through 14 are 1,0,1,1,2,2,8,8,32. Every graph passed:

- Every distinct ordered pair e,f has a Hamiltonian cycle using e and avoiding f.
- Every simple three-edge path lies on a Hamiltonian cycle.
- Every opposite-color endpoint pair has a Hamiltonian path.

`data/strengthenings.json` stores the graph-level results and complete failure lists, all empty. The Hamiltonian cycles come from an independent definition-level routine: enumerate every primal perfect matching, delete it, and test whether the remaining cubic complement is connected. Endpoint paths use a separate exhaustive DFS. This is independent of the reference recovery algorithm, but is not an independent referee implementation of the entire campaign.

CONJECTURE T5. Arbitrary include-one/avoid-another holds for the full Barnette class. CONJECTURE T5. The class is Hamilton-laceable, meaning every black-white pair is joined by a Hamiltonian path. These are hypotheses for further testing, not declarations that the problems are globally open. The sources opened here do not settle their full current literature status. The next test is to extend the enumeration and search graphs with several nested separators. A proof of either statement needs more than the tested range.

PROVED-HERE. Removing an edge from a Hamiltonian cycle through it gives the Hamiltonian path between adjacent endpoints. Single-edge avoidance therefore settles adjacent opposite-color endpoint pairs. Nonadjacent endpoint pairs are the unresolved part of the Hamilton-laceability test relative to this proof.

## A natural stronger statement already fails

REFUTED, PROVED-HERE. P5-Hamiltonicity fails on the cube. In `examples/P5_cube.json`, the path is 0-3-2-7-6. The remaining vertex 5 has neighbors 3,4,7. Vertices 3 and 7 already have their two cycle edges fixed by the prescribed path. Consequently vertex 5 could use only edge 5-4, impossible in a cycle. The file includes all cube edges and its six Hamiltonian cycles. This is the smallest Barnette graph, so no smaller Barnette witness exists.

PROVED-HERE. Hamiltonian-connectedness for same-color endpoints is impossible in a balanced bipartite graph: a spanning path on an even number of vertices has opposite-color endpoints. This is why the requested bipartite qualification matters.

## How far the method goes

PROVED-HERE. The direct sphere argument extends from no separating triangles to precisely those rooted triangulations without black-inner separators. It does not extend to every root without recursive gluing. Recovery is injective but not surjective onto all avoiding cycles; its exact image is characterized in HYPOTHESES.md.

PROVED-HERE. Pfaffian generalization comes through the cited structural equivalence, not by drawing the spoke-circulation construction on an arbitrary surface. The torus experiment exposes a cardinality obstruction to doing that literally. Its 18-vertex primal is Hamiltonian, but its dual admits no two-induced-tree partition.

Unresolved work is explicit. We did not build or embed the 50-, 54-, or 96-vertex nonplanar counterexamples, certify their surface genera, or implement a projective-plane state theory. The first torus obstruction and a working root-free pair are supplied instead. We also did not classify arbitrary mixed-sign weights or audit every possible weakening of Li's marking conventions.
