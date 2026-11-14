# Citation and transcription ledger

Status LIT applies to the statements attributed to sources in this file. "Checked" means I opened the held source and compared its number and statement. It does not certify every proof in that source. Missing originals are identified rather than silently replaced by the project's earlier citation audit.

## Every numbered external theorem or lemma citation

| Manuscript location | Reference | Held source and result of opening it | Status |
| --- | --- | --- | --- |
| Theorem 1.1, line 52 | OpenAI [16], Theorem 1.1 and Corollary 7.1 | papers/OpenAI-Barnette.pdf, pages 1 and 10. The theorem gives Hamiltonicity under the same graph assumptions; the corollary gives avoidance of any specified edge. Together they match the merged statement. | Checked |
| Introduction, line 60 | Hertel [11], Corollary 3 | papers/INDEX.md says the PDF is not held. I did not obtain the original. Gorsky et al. Theorem 4.3 explicitly attributes the H-minus equivalence to Hertel as a corollary of Kelmans. That is secondary verification only. | Original unverifiable locally |
| Introduction, line 60 | Gorsky-Steiner-Wiederrecht [10], Theorem 4.3 | papers/equivalents/2023-Gorsky-Matching-theory-and-Barnettes-conjecture.pdf, page 7. All graphs in class B Hamiltonian iff all have the H-minus property. B is defined on page 1 as cubic, 3-connected, planar and bipartite. H-minus is defined on page 3 as avoidance of each edge. These are universal class statements, exactly as used. | Checked |
| Introduction, line 86 | Alt-Payne-Schmidt-Wood [2], Lemma 5 | PDF not held in papers/, as INDEX.md records. The held OpenAI paper, page 2, cites precisely Lemma 5 for the two-induced-trees formulation. That does not replace inspection of the original. The merged paper independently proves the relevant implication. | Original unverifiable locally |
| After Lemma 4.6, line 663 | OpenAI [16], Lemma 5.3 | OpenAI PDF page 7. Real spoke weights with positive counterclockwise circulation, constructed by unit paths in the plane dual. The merged face-path formula is a different explicit representation of the needed weights, and its increment is proved locally. No numbered statement is mistranscribed. | Checked |
| Section 7, line 908 | Unsigned manuscript [5], Theorem 1.2 | papers/barnette_trees.pdf, page 2. Equivalence of an incidence-tree matching, two disjoint perfect matchings, and no separating triangle with black inner boundary. The definition just above the theorem specifies boundary incidences on the bounded side. This matches the merged remark's side away from t0. | Checked |
| Section 7, line 927 | Gorsky-Steiner-Wiederrecht [10], Theorem 4.16 | Held PDF page 12. Item i is universal Hamiltonicity in B, item v is universal P4-Hamiltonicity of cubic, 3-connected Pfaffian bipartite graphs. The definition on page 3 says P4 has four vertices and three edges. The equivalence yields the stated consequence. | Checked |
| Section 7, line 927 | OpenAI [16], Corollary 7.2 | OpenAI PDF page 10, same consequence with finite simple undirected graphs explicitly specified. | Checked |

The held Gorsky PDF has the quoted theorem numbering. The merged bibliography omits a version note, but the local numbered statements are not mismatched. I inspected rendered source pages for OpenAI Corollaries 7.1 and 7.2, unsigned Theorem 1.2, and Gorsky Theorems 4.3 and 4.16; those PNGs are in pages/. An initially rendered Gorsky page 6 contains useful context but not Theorem 4.3; the actual theorem is on page 7 and was subsequently rendered and read.

## Numbered sections and construction attributions

| Citation | Opened source | Result |
| --- | --- | --- |
| OpenAI Section 5.3, introduction line 94 | pages 7 and 8 | The two-spoke detour, positivity and lowest Taylor coefficient are there. The merged local height proof really replaces this detour argument. |
| Li Section 4, line 663 | papers/A-Note-On-Barnette.pdf, pages 5 to 7 | Half-rays and marked crossings, with the single-cycle exposition extended in Appendix B. The merged text correctly says a symmetric function replaces the power, rather than claiming the marking is literally omega to the mth power. |
| Li Section 6, line 95 | pages 10 and 11, Definitions 28 and 29 and Lemma 30 | The black dual trace gives the rooted tree in G minus the black root; restoring that root as its e0 leaf gives the merged Y_s. The correspondence of the two selections is consistent. |
| Li Appendix C, line 871 | pages 12 and 13 | Both cut contractions are Barnette graphs and their cycles avoid the same cut edge. The merged cap-and-selection proof expresses the same prescribed-boundary step. |
| Alt et al. Section 5, line 872 | Original not held | The held Gorsky source, page 12, attributes the cyclically 4-connected reduction to Kelmans and points to Alt et al. for an overview. Exact original section number not independently verified. |

## Additional source comparisons

LIT. I compared the OpenAI paper's density proof, disk identity, phase convention, the two regroupings, tree recovery, acyclicity, separator colouring and final dual passage to the merged proof. The merged sign has the same phase after multiplication by i to the power minus n: i^J=i^(-n) epsilon. Its finite moment is the mth Taylor coefficient multiplied by m! and i^n. The new W=B+1 formulation is algebraically equivalent to the source's delta sum. The merged recovery uses a tree directly in G, while the original uses spoke duality. Neither substitution loses a hypothesis.

LIT. There is one source-weight mismatch, F1 in REFEREE.md. The unsigned PDF's Lemma 5.1 on page 8 normalizes weights to nonnegative integers at every black centre before calling the resulting expression an integer polynomial. The merged signed heights have not undergone that normalization. Calling their expression an integer polynomial is false. Generalized binomial expansion repairs the remark without changing any core argument.

LIT. The unsigned source's Theorem 5.3 supplies an explicit marked walk; its abstract and Theorem 1.1 claim O(poly(N) 3^(N/4)) time and polynomial space. The merged Section 7 explicitly says it has not checked that algorithm. This audit confirms that the source makes that claim, not its complexity proof. E8 removes the broader phrase "None of these arguments is constructive".

## What remains unavailable

The original numbered claims not verified locally are Hertel Corollary 3 and Alt-Payne-Schmidt-Wood Lemma 5, plus the latter paper's Section 5 cross-reference. The local INDEX identifies them as located online but not held; I did not treat a prior agent's "opened" label as my own inspection.

The historical originals for the numerical literature claims about orders 38, 46, 50 and 90, the 1980 hardness result, and the older face-size bounds are also not held. They are not newly certified here. They are distinguished from the actual finite example counts, which I recomputed. The bibliography and INDEX provide explicit references, so these are unavailable-source qualifications, not counterexamples to the manuscript. The main proof does not rely on any of these historical facts.
