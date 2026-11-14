# Citation checks

No numbered theorem citation mismatch was found in drafts A and B in the inspected versions. This checks references and statements, not their proofs. The OpenAI original's external numbered citations were also checked.

## Statement checks

The following are `LIT` statement comparisons, except the unpublished Fable note. Text was extracted directly from the identified PDFs. Stein, Alt, the disk identity and Ford were also rendered and inspected.

| Manuscript citation | Exact source | Result |
|---|---|---|
| Draft A, Stein Theorem 2.2 | Stein 1971, printed p. 218, scan p. 3 | Matches the region-cycle B-set criterion for a 3-regular sphere map. |
| Both drafts, Alt Lemma 5 | arXiv:1312.3783v1, p. 3 | Matches the two permeating induced-tree formulation. |
| Draft A, OpenAI Proposition 3.1 | Supplied PDF, p. 3 | Matches pair existence without separating triangles. |
| Draft A, OpenAI Lemma 4.1 | Supplied PDF, p. 5 | Matches delta-sum minus three counterclockwise, plus three clockwise. The matching count B = I + ell is explicit. |
| Draft A, OpenAI Section 6 | Supplied PDF, Sections 6.1–6.3 | Matches the white-face tree and selected-edge recovery. |
| Draft B, OpenAI Lemma 5.3 and Section 5.3 | Supplied PDF, Sections 5.2–5.3 | Correct. Lemma 5.3 is in Section 5.2; the sliding argument is in Section 5.3. |
| Draft B, Li Section 6 | Supplied PDF, Definition 28 and Lemma 30 | Matches black dual trace and recovery. |
| Draft B, Li Appendix C | Supplied PDF, pp. 12–13 | Matches three-edge-cut gluing. |
| Draft A, Fable Sections 1–3 | research/2026-11-14_fable_route-combinatorics/PROOF.md | Matches disk identity, heights and signed height identity. Project note, not published LIT. |
| OpenAI, Schnieders Corollary 1.13 | arXiv:2508.03531v1, introduction | Matches faces at most eight. Preprint statement checked; computation not rerun. |
| OpenAI, Hertel Corollary 3 | Author report, Corollary 3 | Matches universal edge-avoidance equivalence. |
| OpenAI, GSW Theorems 4.3 and 4.16 | arXiv:2202.11641v3, pp. 8, 12–13 | Matches universal H-minus and Pfaffian P4 equivalences. |
| OpenAI, GSW Theorem 4.6 | Same v3, p. 9 | Matches planar Pfaffian assertion. Original Kasteleyn source remains secondary. |
| OpenAI, Kenyon Lemma 1, Section 3.2.1 | arXiv:1105.4158v2, p. 5 | Matches two choices per double-dimer cycle. |
| OpenAI, KPW Theorem 1 | arXiv:math/9903025, p. 5 | Matches. Bijection requires incident root vertex and face. Otherwise the theorem gives only an injection. |
| Constructive account, OpenAI Lemma 5.3 | Supplied OpenAI PDF | Correct number for positive spoke circulation. |

## Bibliographic conflicts and cautions

1. Draft A attributes the 1969 proceedings entry to Grünbaum as Unsolved problem 5; draft B attributes Conjecture 5 to Barnette. Original p. 343 was not obtained from an authorized free source. `Barnette1969` retains the history inventory's attribution provisionally and records both alternatives. Unresolved.
2. `bgm2021` becomes `Brinkmann2022`. The journal article is Mathematics of Computation 91, 2022, 1483–1500; 2021 is the preprint year.
3. KPW's publisher page displays publication date 1999-07-03 but assigns the paper to volume 7, 2000. The PDF running head also says 2000. Keep `Kenyon2000`.
4. Berman's publisher record spells the title "Tuite's". Modern references identify Tutte's trinity theorem. Retain "Tutte's" with the spelling warning in the note.
5. `LIT`. HMM supplies the earlier 64-vertex bound; BGM Theorem 4.1 supplies 90. Draft B cites both after the 90-vertex sentence. Split that attribution during revision.
6. GSW v3 typographical concerns in Observation 4.11 and Lemma 4.12 are recorded in research/2026-11-14_astra_route-pfaffian/GSW-CHAIN.md. That audit flags path-length, parity and deletion slips. No replacement proof is certified here.
7. Feder–Subi's 2006 ECCC scan and readable 2008 author revision are different versions. The cited 2006 record remains canonical; the older-approaches SOURCES.md identifies the 2008 copy.

## Rejected metadata search hits

Crossref returned a 2001 book chapter for Alon's article, a different Schrijver paper, a 2025 chapter for Bouchet, an unrelated graph-theory record for Kasteleyn, and a later Hamiltonian-connected paper for Thomas–Yu. These were not imported. `extra-metadata.json` retains the results. A stale same-title lookup confusing Feder–Subi with Florek was rejected too.

See KEY-MAP.md for all canonical key changes. An unsigned manuscript is `Anonymous2026`, without an invented author.
