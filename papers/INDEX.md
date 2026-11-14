# Papers

Every PDF in this folder, with its citation and what it contains. Keys in brackets are the citation keys of [the paper](../paper/barnette.pdf) for the sources it cites.

## The three accounts of the proof

| Paper | File | Contents |
| --- | --- | --- |
| OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, preprint, 24 September 2026. [OpenAI] | `OpenAI-Barnette.pdf` | The proof: states and pairs, the disk identity, the cancellation, the weighted count with a complex phase and an exponential sum, the flow argument, the induction over separating triangles. |
| Z. Li, *A note on the proof of Barnette's conjecture*, arXiv:2610.30490v1, 21 October 2026. [Li] | `A-Note-On-Barnette.pdf` | An exposition of the same proof in the cubic graph $G$, with the evaluation of the count replaced by a second sign-reversing involution. |
| *A constructive proof of Barnette's conjecture*, anonymous manuscript, 18 October 2026. [Constructive] | `barnette_trees.pdf` | The real sign and the integer polynomial; the criterion for a pair to exist (Theorem 1.2); the exchange walk on pairs (Theorem 5.3); the bound $3^{n/2}$ on the number of states and the search through them (Proposition 6.2, Theorem 1.1). |

Plain-text copies of these three are in `text/`.

## Cited in the paper

| Paper | File | Contents |
| --- | --- | --- |
| S. K. Stein, *B-sets and planar maps*, Pacific J. Math. 37 (1971), 217–224. [Stein] | `stein-1971-b-sets-and-planar-maps.pdf` | Theorem 2.2: a cubic map on the sphere has a Hamiltonian circuit if and only if its regions can be divided into two sets neither of which contains a cycle of at least three regions. In the dual triangulation this is a partition of the vertices into two induced trees. |
| H. Alt, M. S. Payne, J. M. Schmidt, D. R. Wood, *Thoughts on Barnette's conjecture*, Australas. J. Combin. 64 (2016), 354–365. [Alt] | `alt-payne-schmidt-wood-2016-thoughts-on-barnettes-conjecture.pdf` | A sufficient condition for the dual of a triangulation to be Hamiltonian; the dual is Hamiltonian exactly when the vertices split into two induced trees (Lemma 5); Kelmans' equivalent forms of the conjecture, with proofs (Section 5). |
| G. Brinkmann, J. Goedgebeur, B. D. McKay, *The minimality of the Georges–Kelmans graph*, Math. Comp. 91 (2022), 1483–1500. arXiv:2101.00943. [BGM] | `brinkmann-goedgebeur-mckay-2022-minimality-of-georges-kelmans-graph.pdf` | No cubic, bipartite, 3-connected graph with fewer than 50 vertices is non-Hamiltonian; Barnette's conjecture holds up to 90 vertices. |
| C. Hine, T. Kálmán, *Clock theorems for triangulated surfaces*, arXiv:1808.06091, 2018. [HineKalman] | `hine-kalman-2018-clock-theorems-for-triangulated-surfaces.pdf` | Tutte matchings, or states, of a triangulation with faces coloured black and white and a fixed outer triangle (Definition 2.1; the states are on the white triangles there); on the sphere they form a distributive lattice under a local move. |

## Background

| Paper | File | Contents |
| --- | --- | --- |
| E. Grinbergs, *On planar regular graphs degree three without Hamiltonian cycles*, 1968; English translation by D. Zeps, arXiv:0908.2563. | `grinberg-1968-plane-homogeneous-graphs-of-degree-three.pdf` | Grinberg's necessary condition for a planar graph to have a Hamiltonian cycle, and cubic planar graphs without one that have no nontrivial edge cut of size less than four or five. |
| D. Holton, R. E. L. Aldred, *Planar graphs, regular graphs, bipartite graphs and Hamiltonicity*, Australas. J. Combin. 20 (1999), 111–131. | `holton-aldred-1999-planar-regular-bipartite-graphs-and-hamiltonicity.pdf` | A survey of Hamiltonicity: the classical theorems, the smallest non-Hamiltonian 3-connected cubic planar graphs, the number of Hamiltonian cycles of regular graphs, and Barnette's conjectures. |
| A. Hertel, *A survey & strengthening of Barnette's conjecture*, University of Toronto, 2005. | `hertel-2005-survey-and-strengthening-of-barnettes-conjecture.pdf` | A survey of the conjecture, and its equivalence with the existence of a Hamiltonian cycle through the middle edge of any path of length three on a face that avoids the other two edges; the form with one avoided edge is Corollary 3. |
| T. Feder, C. Subi, *On Barnette's conjecture*, ECCC TR06-015, 2006. | `feder-subi-2006-on-barnettes-conjecture.pdf` | The conjecture holds when the faces are 3-coloured and two of the colour classes contain only faces with four or six sides; this extends Goodey's theorem. |
| F. Kardoš, *A computer-assisted proof of the Barnette–Goodey conjecture: not only fullerene graphs are Hamiltonian*, SIAM J. Discrete Math. 34 (2020), 62–100. arXiv:1409.2440v2. | `kardos-2020-computer-assisted-proof-of-barnette-goodey.pdf` | Every 3-connected cubic planar graph with faces of size at most six is Hamiltonian. |
| B. Bagheri Gh., T. Feder, H. Fleischner, C. Subi, *Hamiltonian cycles in planar cubic graphs with facial 2-factors, and a new partial solution of Barnette's Conjecture*, J. Graph Theory 96 (2021), 269–288. arXiv:1806.05483v3. | `bagheri-feder-fleischner-subi-2021-facial-2-factors-partial-solution.pdf` | Hamiltonian cycles of plane cubic graphs with a 2-factor of faces, through spanning trees of faces; the leapfrog extensions of planar cubic bipartite cyclically 4-edge-connected graphs are Hamiltonian. |
| B. Bagheri Gh., T. Feder, H. Fleischner, C. Subi, *On finding Hamiltonian cycles in Barnette graphs*, Fund. Inform. 188 (2022), 1–14. arXiv:2212.02668. | `bagheri-feder-fleischner-subi-2022-finding-hamiltonian-cycles-in-barnette-graphs.pdf` | The complexity of finding the spanning trees of faces of the previous paper; if Barnette's conjecture were false, Hamiltonicity of 3-connected cubic bipartite planar graphs would be NP-complete. |
| M. Gorsky, R. Steiner, S. Wiederrecht, *Matching theory and Barnette's conjecture*, Discrete Math. 346 (2023), 113249. arXiv:2202.11641v3. | `gorsky-steiner-wiederrecht-2023-matching-theory-and-barnettes-conjecture.pdf` | The conjecture in terms of matching theory: it reduces to cubic planar braces, and it is equivalent to the same statement for Pfaffian in place of planar graphs (Theorem 4.16). |
| T. Schnieders, *Barnette graphs with faces up to size 8 are Hamiltonian*, arXiv:2508.03531, 2025. | `schnieders-2025-barnette-graphs-with-faces-up-to-size-8.pdf` | Cubic, bipartite, planar, connected graphs with faces of size at most eight are Hamiltonian; part of the proof is a computation. |
| M. A. Bekos, M. Kaufmann, M. Pfister, *Approximating Barnette's conjecture*, GD 2025, LIPIcs 357, 6:1–6:7. | `bekos-2025-approximating-barnettes-conjecture.pdf` | Every cubic, bipartite, 3-connected planar graph with $n$ vertices has a subhamiltonian cycle with $5n/6$ of its edges. |

Bibliographic data for all of these, and for the references of the paper that are not held here, are in `barnette.bib`.
