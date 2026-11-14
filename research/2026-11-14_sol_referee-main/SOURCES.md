# Citation and transcription ledger

Status LIT applies to the statements attributed to sources in this file. "Checked" means I opened the held source and compared its number and statement. It does not certify every proof in that source. Missing originals are identified rather than silently replaced by the project's earlier citation audit.

## Every numbered external theorem or lemma citation

| Manuscript location | Reference | Held source and result of opening it | Status |
| --- | --- | --- | --- |
| Theorem 1.1, line 52 | OpenAI [16], Theorem 1.1 and Corollary 7.1 | papers/OpenAI-Barnette.pdf, pages 1 and 10. The theorem gives Hamiltonicity under the same graph assumptions; the corollary gives avoidance of any specified edge. Together they match the merged statement. | Checked |
| Introduction, line 60 | Hertel [11], Corollary 3 | Found outside papers/: research/2026-11-14_opus_history-literature/pdf/2005_Hertel_Survey-and-strengthening-Barnette.pdf, page 7. The original says Barnette's conjecture holds iff every arbitrary edge in a Barnette graph can be avoided by a Hamiltonian cycle. The theorem number and universal quantifiers match. The following paragraph credits Kelmans. | Checked |
| Introduction, line 60 | Gorsky-Steiner-Wiederrecht [10], Theorem 4.3 | papers/equivalents/2023-Gorsky-Matching-theory-and-Barnettes-conjecture.pdf, page 7. All graphs in class B Hamiltonian iff all have the H-minus property. B is defined on page 1 as cubic, 3-connected, planar and bipartite. H-minus is defined on page 3 as avoidance of each edge. These are universal class statements, exactly as used. | Checked |
| Introduction, line 86 | Alt-Payne-Schmidt-Wood [2], Lemma 5 | Found outside papers/: research/2026-11-14_opus_history-literature/pdf/2013_Alt-Payne-Schmidt-Wood_Thoughts-on-Barnette_arXiv1312.3783.pdf, pages 3 and 4. The equivalent statements are Hamiltonicity of the dual, a permeating subtree, and two disjoint permeating subtrees partitioning the vertices. Permeating means induced and meeting every face. The note on page 4 explicitly says permeating can be omitted in the third condition. This matches the merged formulation. | Checked |
| After Lemma 4.6, line 663 | OpenAI [16], Lemma 5.3 | OpenAI PDF page 7. Real spoke weights with positive counterclockwise circulation, constructed by unit paths in the plane dual. The merged face-path formula is a different explicit representation of the needed weights, and its increment is proved locally. No numbered statement is mistranscribed. | Checked |
| Section 7, line 908 | Unsigned manuscript [5], Theorem 1.2 | papers/barnette_trees.pdf, page 2. Equivalence of an incidence-tree matching, two disjoint perfect matchings, and no separating triangle with black inner boundary. The definition just above the theorem specifies boundary incidences on the bounded side. This matches the merged remark's side away from t0. | Checked |
| Section 7, line 927 | Gorsky-Steiner-Wiederrecht [10], Theorem 4.16 | Held PDF page 12. Item i is universal Hamiltonicity in B, item v is universal P4-Hamiltonicity of cubic, 3-connected Pfaffian bipartite graphs. The definition on page 3 says P4 has four vertices and three edges. The equivalence yields the stated consequence. | Checked |
| Section 7, line 927 | OpenAI [16], Corollary 7.2 | OpenAI PDF page 10, same consequence with finite simple undirected graphs explicitly specified. | Checked |

The held Gorsky PDF has the quoted theorem numbering. The merged bibliography omits a version note, but the local numbered statements are not mismatched. I inspected rendered source pages for OpenAI Corollaries 7.1 and 7.2, unsigned Theorem 1.2, Gorsky Theorems 4.3 and 4.16, Hertel Corollary 3 and Alt et al. Lemma 5; those PNGs are in pages/. An initially rendered Gorsky page 6 contains useful context but not Theorem 4.3; the actual theorem is on page 7 and was subsequently rendered and read.

## Numbered sections and construction attributions

| Citation | Opened source | Result |
| --- | --- | --- |
| OpenAI Section 5.3, introduction line 94 | pages 7 and 8 | The two-spoke detour, positivity and lowest Taylor coefficient are there. The merged local height proof really replaces this detour argument. |
| Li Section 4, line 663 | papers/A-Note-On-Barnette.pdf, pages 5 to 7 | Half-rays and marked crossings, with the single-cycle exposition extended in Appendix B. The merged text correctly says a symmetric function replaces the power, rather than claiming the marking is literally omega to the mth power. |
| Li Section 6, line 95 | pages 10 and 11, Definitions 28 and 29 and Lemma 30 | The black dual trace gives the rooted tree in G minus the black root; restoring that root as its e0 leaf gives the merged Y_s. The correspondence of the two selections is consistent. |
| Li Appendix C, line 871 | pages 12 and 13 | Both cut contractions are Barnette graphs and their cycles avoid the same cut edge. The merged cap-and-selection proof expresses the same prescribed-boundary step. |
| Alt et al. Section 5, line 872 | History-folder PDF, pages 8 through 10 | Section 5 explains Kelmans' reductions; Theorem 8, page 9, includes the equivalence with the cyclically 4-edge-connected class, and its proof joins compatible cycles across a 3-edge cut. Exact section and attribution checked. |

## Additional source comparisons

LIT. I compared the OpenAI paper's density proof, disk identity, phase convention, the two regroupings, tree recovery, acyclicity, separator colouring and final dual passage to the merged proof. The merged sign has the same phase after multiplication by i to the power minus n: i^J=i^(-n) epsilon. Its finite moment is the mth Taylor coefficient multiplied by m! and i^n. The new W=B+1 formulation is algebraically equivalent to the source's delta sum. The merged recovery uses a tree directly in G, while the original uses spoke duality. Neither substitution loses a hypothesis.

LIT. There is one source-weight mismatch, F1 in REFEREE.md. The unsigned PDF's Lemma 5.1 on page 8 normalizes weights to nonnegative integers at every black centre before calling the resulting expression an integer polynomial. The merged signed heights have not undergone that normalization. Calling their expression an integer polynomial is false. Generalized binomial expansion repairs the remark without changing any core argument.

LIT. The unsigned source's Theorem 5.3 supplies an explicit marked walk; its abstract and Theorem 1.1 claim O(poly(N) 3^(N/4)) time and polynomial space. The merged Section 7 explicitly says it has not checked that algorithm. This audit confirms that the source makes that claim, not its complexity proof. E8 removes the broader phrase "None of these arguments is constructive".

## Additional historical checks and availability

All numbered external theorem and lemma citations are now verified in original held sources. The initial papers/ inventory missed the history-literature folder. A repository-wide PDF search located the two missing originals before the final report. This corrected the preliminary ledger's unavailable labels; I opened the files rather than adopting a prior agent's inspection claim.

The history folder's 2021_Brinkmann-Goedgebeur-McKay_Minimality-Georges-Kelmans_arXiv2101.00943.pdf has Theorem 1.1 on page 3 asserting no smaller non-Hamiltonian 3-connected bipartite cubic graph than the 50-vertex Georges-Kelmans graph. Its Section 4 gives verification through at least 90 vertices in the Barnette class. Its introduction also attributes the 46-vertex Tutte example and 38-vertex minimum to the originals cited by the merged manuscript. The latter two originals were not found, so I checked their statements only in this secondary source. The history folder's 2025_Schnieders_Barnette-faces-up-to-8_arXiv2508.03531.pdf has Corollary 1.13 giving exactly the face-size-eight claim. Hertel Theorem 10, page 7, also explicitly confirms the common-face include-one/avoid-another consequence in the final remark.

The original 1980 hardness paper, Tutte's 1946 paper, Holton-McKay's 1988 paper and several older historical originals were not found. They are not newly certified here. These availability limits do not concern any numbered theorem citation in the manuscript or any C0 proof premise. The finite examples were independently recomputed rather than accepted from these sources.
