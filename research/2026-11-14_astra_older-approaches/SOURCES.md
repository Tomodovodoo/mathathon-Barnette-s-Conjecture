# Sources and access record

Read on 2026-11-14. Local original PDFs remain in the history-literature and machinery-literature folders. `text/` contains layout extraction copies, not new editions. Only the sections listed here are represented as inspected; extraction of a complete PDF does not mean its entire proof was audited.

| Key | Source and inspected part | Access |
|---|---|---|
| O | OpenAI, Paired states and Hamiltonian cycles in cubic bipartite planar graphs, supplied September 24, 2026 manuscript, Sections 1–7 | Supplied PDF text read; not independently verified as a publication |
| FS | Feder–Subi, On Barnette's conjecture, ECCC TR06-015, Section 2 definitions and result; readable author revision dated February 20, 2008 | 2006 first page rendered and inspected; Type 3 text unusable. [Author PDF](https://theory.stanford.edu/~tomas/barnew.pdf) fetched to text/feder-readable.pdf, Sections 1–2 read. Do not silently identify revisions |
| BF21 | Bagheri Gh.–Feder–Fleischner–Subi, Hamiltonian cycles in planar cubic graphs with facial 2-factors, and a new partial solution of Barnette's Conjecture, arXiv:1806.05483v3, Definitions 5–7 and Theorem 11 with proof | Downloaded PDF extraction read |
| BF22 | Same authors, On Finding Hamiltonian Cycles in Barnette Graphs, Fundamenta Informaticae 188, 2022, 1–14, arXiv:2212.02668v2 | Introduction and scope read; detailed complexity reductions not audited |
| Stein | B-sets and planar maps, Pacific J. Math. 37, 1971, 217–224, Theorem 2.2 and proof | Downloaded PDF extraction read |
| APSW | Alt–Payne–Schmidt–Wood, Thoughts on Barnette's conjecture, AJC 64, 2016, 354–365; arXiv:1312.3783v1 | Lemma 5 proof, Theorem 4 and Section 5 context read |
| Hertel | A survey and strengthening of Barnette's conjecture, 2005 | Theorems 8–10 and Corollary 3 proof read |
| K | Kardoš, A computer-assisted proof of the Barnette–Goodey conjecture, SIAM J. Discrete Math. 34, 2020, 62–100; arXiv:1409.2440v2 | Sections 2.1–2.5, Lemma 6 and Theorem 4; patch construction passages inspected, computer code not rerun |
| S | Schnieders, Barnette graphs with faces up to size 8 are hamiltonian, arXiv:2508.03531v1 | Introduction, substitution definition and Lemma 3.3 proof mechanism, Section 6 limitations; not treated as a peer-reviewed result |
| GSW | Gorsky–Steiner–Wiederrecht, Matching theory and Barnette's conjecture, Discrete Math. 346, 2023, 113249; arXiv:2202.11641v3 | Section 4, especially 4.8–4.17 and trisum proof read |
| Grinberg | Plane homogeneous graphs of degree three without Hamiltonian circuits, English translation arXiv:0908.2563 | Theorem and face-weight counting inspected |
| BGM | Brinkmann–Goedgebeur–McKay, Generation of cubic graphs and the minimality of the Georges–Kelmans graph, arXiv:2101.00943v2 | Introduction, scope of minimality and 90-vertex result; not a reproduction of the census |
| HK | Hine–Kálmán, Clock theorems for triangulated surfaces, arXiv:1808.06091v1 | Introduction, state moves, Theorem 4.3 and Lemma 4.4 |
| Kalman | A version of Tutte's polynomial for hypergraphs, Adv. Math. 244, 2013, 823–873 | Section 9 and Theorem 9.10, Berman reference |
| TY | Thomas–Yu, 4-connected projective-planar graphs are Hamiltonian, JCTB 62, 1994, 114–132 | [Author PDF](https://thomas.math.gatech.edu/PAP/ham.pdf) fetched; introduction and Section 2 bridge/admissibility definitions read |

Sources not obtained in full: Goodey 1975, Tutte 1975 Duality and trinity, Berman 1980 original, original Kelmans strengthening papers, original Tutte 1956, Thomassen 1983, HMM 1985. Secondary access is stated wherever used. Berman's [publisher abstract](https://epubs.siam.org/doi/10.1137/0601009) was located, but is not a full-proof source.

Novelty searches used the exact combinations `"tree trinity" "Hamiltonian"`, `"Tutte matchings" "Hamiltonicity"`, `"Tutte matching" "Barnette"`, `"trinity" "Hamiltonian" Tutte Kalman`, and Berman/Tutte title searches. No pre-2026 paired-state Hamiltonicity result was located. Several broad searches returned unrelated uses of Trinity or Tutte matchings; these were discarded. No universal negative is inferred. Local grep of HK, Kálmán hypergraphs, Kálmán–Postnikov, Kálmán–Murakami, Kálmán–Tóthmérész and Juhász–Kálmán–Rasmussen found no Barnette/Hamiltonian occurrence in those files. Their full bibliographic closure was not searched.

Extraction command, repository root:

```powershell
Get-ChildItem research/2026-11-14_opus_history-literature/pdf/*.pdf | ForEach-Object { pdftotext -layout $_.FullName ('research/2026-11-14_astra_older-approaches/text/' + $_.BaseName + '.txt') }
```

Fetched files used `Invoke-WebRequest <URL> -OutFile <assigned-folder>/text/<name>.pdf` followed by `pdftotext -layout`. `feder-page1.png` was made with PyMuPDF at scale 1.5 from the original ECCC PDF. Checksums and extraction sizes are in `code/source-manifest.json`.
