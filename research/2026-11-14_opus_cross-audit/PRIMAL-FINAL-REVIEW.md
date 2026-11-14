# Final review of the primal note

Object: proofs/primal/primal.pdf as revised at commit 048615a (15 pages, eight figures), with PRIMAL-PROOF.md as its source and STATUS.md, DICTIONARY.md, COMPARISON.md beside it. I read the TeX source line by line, rendered all 15 pages at 110 dpi and looked at each, and checked every displayed count against the figures. I read the referee's REFEREE.md and LEAN-MATCH.md only after my own pass, to check that each item had been applied.

Verdict: **ACCEPT.** The route from Lemma 1 to Theorem T closes. I found no false statement. I made nine small edits (listed at the end); none changes a proof. The real-sign normalization dispute is settled in ADJUDICATION.md in favour of the revision.

## 1. Line-by-line read

What I checked, by section. Every item below I re-derived myself.

- **Section 1.** Theorem T and its corollary. The complement of a perfect matching in a cubic graph is 2-regular, so connected means Hamiltonian. Fine.
- **Section 2.** The map conventions: Euler in the form v - e + f = 1 + c, the bridge rule, the subgraph rule, the cut-vertex criterion by splitting a repeated vertex. The general circuit-cut fact: facial boundaries span the F2 cycle space (dimension count from face connectivity, which comes from contracting a spanning tree and deleting loops); face circuits are bonds; bonds have connected shores. All correct. One sentence is loose: "Every other dependence assigns equal coefficients..." means "every dependence"; harmless.
- **Lemma 1.** Counts |B| = |W| = n + 1, |E| = 3(n + 1), |F| = n + 3 follow from Euler. Distinct faces at a vertex and at most one shared edge follow from 2-connectivity and the two-edge-bond exclusion. Correct.
- **Lemma 2.** (2.1) checked by subtracting the two Euler equations; the no-pinch argument is right; the root faces avoid S. Correct.
- **delta and Lemma 3.** I verified the local identity delta(f, g) = [d g](e) = -[d f](e) with a picture (walk from f to g, b on the left, edge b to w has g on its left). The pairing with the boundary of f_i is delta_{i-1}^2 - delta_i^2 = 0. Gradient, constant on shores, values plus or minus one. Correct.
- **Lemma 4.** The capacity network and (3.1); the 2-factor gives the pair. In the deficit argument I rechecked: additivity over components (components share no black vertex), W_1 empty (removing f does not lower the deficit), K = G[V(K)] with all cut ends black, (3.2), and the Euler/degree identity 2|Y| + 2k = 4 + |B_2| + |B_3| + |W_2| + |W_3|, which gives d(Y) = 4 - 2k - c/3. Then k = 1, c = 3 and both shores have at least two vertices. Correct. COMPUTED support: in my phase run (scripts/phase_ratio.py) every one of the 2,780 rooted instances without a pair has a separating triangle, i.e. a nontrivial three-edge cut.
- **Lemma 5.** All four counts in (4.2) re-derived; elimination gives h = 2l + 3; colour count gives |W cap S| = |B cap S| + 1; sum of (2.2) gives -3 sigma. Correct.
- **Lemma 6.** Path flow divergences; consistency of the local potentials (the three equations sum to minus the outgoing divergence, which is zero on A); summing around C gives -sigma times outward flux = sigma |W cap S|. Correct.
- **Section 6.** Lemma 7: the circuit of Q_s is directed by every partner (out-degree at most one), reversal keeps a bijection, is a fixed-point-free involution, and flips an odd number of signs by Lemma 5. Lemma 8: D is a union of odd circuits covering X; 2^c pairs per D; group sum (6.3) with prefactor (-1)^((n - c)/2), which I recomputed; linear coefficient |W cap S_C| > 0 by (5.1); lowest coefficient (6.4) is a sum of same-sign positive terms. Correct. The remark that only oddness is needed for Lemma 7 but the exact value three is needed for (6.3) is accurate and worth keeping.
- **Lemmas 9 to 12.** Out-degree counting gives one root per component; the two root edges join three components; edge count 2n + 1 gives a tree; parent edges of white vertices form a perfect matching containing e0; Lemma 11 by two degree counts; Lemma 12 by Lemma 5 against Lemma 11. Correct.
- **Lemma 13 and Theorem T.** Shores connected (two components would need six boundary edges); l = 0 or 3; three distinct ends; caps simple, cubic, bipartite, 3-edge-connected, smaller. The induction keeps the quantifier over e0 and handles e0 internal or crossing. Correct. The 3-vertex to 3-edge paragraph is correct.
- **Section 9.** The hypothesis ledger now matches the proofs.
- **Remarks 14 and 15.** See Section 3 below.
- **Dictionary page.** Typesets cleanly. Its column entries are checked against the sources in CONSISTENCY.md; two cells need attention there (Li's "H" and the constructive paper's "B" are the incidence graph, which the note itself never names).

## 2. Were the referee's items applied?

| Referee item | Applied? | Where |
| --- | --- | --- |
| F1, planar facts and setting | Yes. The note chose genus-zero combinatorial maps with Euler as the one imported theorem and states the deletion, bridge, isolated-vertex, contraction and subgraph rules. One residue: the corollary for planar graphs needs that a drawing gives a rotation system. I added that sentence to Section 8. | Section 2; Section 8 last paragraph |
| F2, coherent delta | Yes. "The sense cannot be chosen independently at different vertices." | Section 2, before Lemma 3 |
| F3, Lemma 3 cancellation | Yes, with the coefficient identity and displayed pairing. | Lemma 3 proof |
| F4, Lemma 2(b) deletion | Yes, the accounting sentence is there. | Lemma 2 proof |
| F5, general Lemma 12 | Yes, any state and compatible matching. I added the definition of "compatible" here, since Remark 15 used the word without one. | Lemma 12 |
| F6, partner needed | Yes, now proved as Remark 14. | Section 11 |
| F7, hypothesis ledger | Yes, all three corrections. | Section 9 |
| F8, smaller points | Yes: circuit-cut fact precedes Lemma 1; neighbours in A; nonempty remainder; k >= 1 via the subgraph rule; spanning-tree independence in Lemma 13; two-vertex bound. | various |
| F9, Lemma 7 coverage | Yes: 307 further cancelling states at 15 and 16 faces in the revision; my phase run covers the same range for normalization. | STATUS.md |
| M1, missing Lean citations | Yes, `make_coloredDual` and `cap_duality`. | STATUS.md |
| M2, one-way `circuit_cut` | Yes, `bond_of_circuit` cited and the converse marked as the note's own. | STATUS.md |
| M3, Lemma 3 not a restatement | Yes. | STATUS.md |
| M4, phase ratio | Correctly rejected; the ratio is i^n. See ADJUDICATION.md. | Section 6, STATUS.md |
| M5, Lemma 12 scope | Yes. | Lemma 12 |

## 3. The three new observations

1. **A circuit-free state without a partner never gives a tree (Remark 14).** If Q_s is a forest it has n edges on n + 3 faces, hence three components. A partner exists exactly when each component holds one root face (orient toward the root; the out-degree pattern forces this orientation, giving uniqueness). Lemma 9 adds two edges, both with root endpoints, so a component without a root stays separate and the face graph L is not a tree. By the bond argument and the edge count, L is a face tree exactly when G - L is a tree. Proof correct and complete.
2. **A circuit-free second state with a partner has exactly one (Remark 14).** Same argument: in a tree component with one root, out-degree one at every non-root face and zero at the root determines the orientation. Correct.
3. **A perfect matching has a compatible state exactly when its complement is connected (Remark 15).** Forward is Lemma 12. Converse: a face circuit in P is a bond missed by the connected spanning cycle, impossible; so P is a forest with two components. The other two root edges lie on the cycle; if either closed a face path in P, the resulting face circuit would be a cut met once by a cycle. So the third root face is in the other component, and deleting e0 leaves three trees with one root each. Orienting toward the roots gives the state, and the same forcing gives uniqueness. Correct. Note that "complement connected" and "complement Hamiltonian" are the same here; REPORT.md of the revision says "Hamiltonian", the brief says "connected".

The finite counts quoted before the remarks (25,272; 3,256; 186,476 = 150,764 + 35,712) match the referee's code/out/totals.json.

## 4. Figures against text

| Figure | What I checked | Result |
| --- | --- | --- |
| 1 | Cube has six faces f0 to f5, running graph 13 faces f0 to f12 and 22 vertices; root faces are the three at b0; e0 bold. | Matches. |
| 2 | Each non-root face and each non-root black vertex meets one blue and one vermilion segment (cube: f3, f4, f5; running: ten faces). | Matches. |
| 3 | Left: S = one white vertex, counts 1 + 3 = 3 + 1, h = 3, l = 0. Right: |S| = 11, |B cap S| = 5, |E_S| = 20, |U_S| = 10, so (2.1) holds, 3*11 + 7 = 40 = 2*20, 3*5 + 7 = 22 = 20 + l gives l = 2, 5 + 7 = 10 + 2. I counted seven dashed boundary edges. Six white vertices inside = five black + 1. | Matches caption and (4.2). |
| 4 | Outflow from b0: cube 2 + 1 + 1 = 4 = |W|; running 6 + 3 + 2 = 11 = |W|. Weights 1 and 6 equal |W cap S|. | Matches. |
| 5 | Two partners with signs -1 and +1, summing to zero. Caption "The same second state" referred to nothing; rewritten. | Fixed caption. |
| 6 | P has one edge per vertex, e0 in P, purple cycle through all vertices. | Matches. |
| 7 | 14 vertices, two seven-vertex shores, three dashed cut edges, outer ends black and inner ends white (l = 0 or 3). | Matches. |
| 8 | Two cubes; left cap white (replaces a shore whose ends are black), right cap black. The left "cap" label sat on the vertex and the right one touched it; moved both. The caption described Hamiltonian cycles that are not drawn; now says so. | Fixed label and caption. |

## 5. Unslop pass

The note's prose is plain and specific; it has no puffery and few tells. I changed: "Here are all details of the state count, the fourth equation." to "The fourth equation is the state count."; removed the referee chatter from the body of Section 6 (it belongs in STATUS.md); replaced the vague "local determinant referee report" and "structure referee's INTEGRATION.md, Sections 6 and 7" by paths, and corrected the section numbers to 5 and 7 (Section 6 of INTEGRATION.md is about exponential rarity, not the tree criterion). "contained in any perfect matching" became "contained in a perfect matching". I left the dense status paragraph on page 1; it is accurate and the project's protocol asks for it.

## 6. Edits made (all in proofs/primal/)

1. Section 6 phase paragraph: cites Lemma 5 for 3 | t, states i^(-n) for the opposite corner order, moves the adjudication note to STATUS.md.
2. Lemma 5 proof: first sentence of the state-count paragraph.
3. Lemma 11: "any" to "a".
4. Lemma 12: defines "compatible".
5. Section 8: one sentence on drawings giving rotation systems (referee F1 residue).
6. Section 9: path to SIGNIFICANCE.md.
7. Section 11: path to INTEGRATION.md, Sections 5 and 7.
8. Figure 5 and Figure 8 captions (captions.json and figures/check.py).
9. Figure 8 cap labels (08-pieces-body.tex, 08-pieces.tex, check.py; standalone PDF/PNG rebuilt).

STATUS.md: phase section rewritten as the adjudication. The PDF was rebuilt with scripts/build_primal.py (a copy of the revision's build.py that writes its logs and renders into this folder); 15 pages, no overfull boxes, no undefined references.

## 7. What remains

- A human referee should still read Section 2 and Remarks 14 and 15. My read is a second machine read, not that.
- Which corner orientation Lean's `ColoredDual.oriented` fixes relative to the note's sphere orientation is not settled; the constant is i^n or i^(-n).
- STATUS.md's "Exact finite range" section describes the first version's checker and its 20-vertex example, now in EXAMPLES.md. It is accurate as history, but a reader may confuse that 20-vertex example with the 22-vertex running example. CONSISTENCY.md lists it.
