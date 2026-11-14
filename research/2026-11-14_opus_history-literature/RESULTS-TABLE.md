# Results table

One row per result. "Barnette graph" means cubic, bipartite, planar, 3-connected. `T` is the dual Eulerian triangulation (shared notation in `research/BRIEF.md`).

The verified column says how far I checked:

- **yes** means I opened the source (or the published abstract) and the statement in the row matches it;
- **via X** means I could not open the source, but X states the result and I opened X;
- **meta** means I confirmed the bibliographic record (Crossref, arXiv API, publisher page) but not the content;
- **no** means neither.

Every row is `LIT` in the sense of the brief, unless the status column says otherwise. Links point to the open copy when there is one; the local copy is in `pdf/` (see `pdf/INDEX.md`).

## A. Origins and counterexamples to neighbouring conjectures

| # | Year | Authors | Statement | Method | Hypotheses | Link | Verified |
|---|---|---|---|---|---|---|---|
| A1 | 1884 | Tait | Conjecture: every cubic 3-connected planar graph is Hamiltonian (would give the four colour theorem). | Conjecture | cubic, planar, 3-connected | doi:10.1080/14786448408627475 | via Hertel 2005, Holton-Aldred 1999; meta |
| A2 | 1946 | Tutte | A 46-vertex cubic 3-connected planar non-Hamiltonian graph; Tait's conjecture is false. | Construction with "Tutte fragments" that force an edge | drops bipartite | doi:10.1112/jlms/s1-21.2.98 | via Hertel, Kardoš; meta |
| A3 | 1968 | Grinberg | Grinberg's formula: a plane Hamiltonian cycle satisfies sum_i (i-2)(f_i' - f_i'') = 0; gives non-Hamiltonian cubic polyhedra (Grinberg graphs). | Face counting inside/outside a Jordan curve | planar | English transl. arXiv:0908.2563 | yes (abstract, Holton-Aldred Thm 5) |
| A4 | 1971 | Tutte | "It is tempting to conjecture that every 3-connected bipartite cubic graph is hamiltonian." | Remark | cubic, bipartite, 3-connected | doi:10.1016/0012-365X(71)90027-6 | via Brinkmann-Goedgebeur-McKay 2021 abstract |
| A5 | 1976/1982 | Horton | Counterexample to Tutte's conjecture on 96 vertices (in Bondy-Murty 1976); a 92-vertex one in Discrete Math 1982. | Construction | drops planarity | doi:10.1016/0012-365X(82)90079-6 | via Hertel, GSW; meta |
| A6 | 1981-1983 | Ellingham; Ellingham-Horton | Non-Hamiltonian 3-connected cubic bipartite graphs on 78 and 54 vertices. | Construction | non-planar | doi:10.1016/0095-8956(83)90046-1 | via Hertel; meta |
| A7 | 1986/1988 | Kelmans | Non-Hamiltonian cubic bipartite 3-connected (also cyclically 4-connected) graphs on 50 vertices, earlier than Georges; same 1986 paper contains the H+- equivalence (row C2). | Construction, four-pole gluing | non-planar | doi:10.1090/trans2/158/12 (English transl. 1994); doi:10.1070/RM1988v043n03ABEH001738 | via Hertel, APSW 2016; meta |
| A8 | 1989 | Georges | 50-vertex non-Hamiltonian bicubic 3-connected graph. | Construction | non-planar | doi:10.1016/0095-8956(89)90012-9 | via Hertel; meta |
| A9 | 1988 | Holton, McKay | Smallest non-Hamiltonian 3-connected cubic planar graphs have 38 vertices; exactly six of them (one is Barnette-Bosák-Lederberg). Hence every Barnette graph on at most 36 vertices is Hamiltonian. | Okamura reductions plus computer | cubic planar 3-connected | doi:10.1016/0095-8956(88)90075-5 | via Holton-Aldred 1999, BGM 2021 |
| A10 | 1999-2000 | Aldred, Bau, Holton, McKay | Cyclically 4-connected cubic planar: Hamiltonian up to 40 vertices, three non-Hamiltonian ones on 42. Smallest non-Hamiltonian cyclically 5-connected cubic planar graph has 44 vertices (Faulkner-Younger graph), unique. Faces at most 6: Hamiltonian up to 176 vertices. | Computer search | cubic planar, cyclic connectivity | doi:10.1137/S0895480198348665; doi:10.1007/s003730050046 | via Holton-Aldred 1999 |
| A11 | 2022 | Brinkmann, Goedgebeur, McKay | The 50-vertex Georges-Kelmans graph is the smallest non-Hamiltonian 3-connected cubic bipartite graph. Infinite family of non-Hamiltonian cyclically 5-connected bipartite cubic graphs (smallest 300 vertices). No non-Hamiltonian 3-connected bicubic graph of genus < 4 found (non-exhaustive). | Incremental theory plus computation | non-planar | doi:10.1090/mcom/3701, arXiv:2101.00943 | yes |
| A12 | 1969 | Barnette (recorded by Grünbaum) | Barnette's conjecture: every cubic bipartite 3-connected planar graph is Hamiltonian. Problem 5 in Tutte (ed.), Recent Progress in Combinatorics, p. 343. | Problem | all four | book, not online | via every source; original page not seen |
| A13 | 1970 | Grünbaum | Repeats the conjecture in "Polytopes, graphs, and complexes". | Survey | | doi:10.1090/S0002-9904-1970-12601-5 | via Hertel, Harant; meta |
| A14 | 1973 | Grünbaum, Walther | Introduce shortness exponents of families of graphs. | Constructions | | doi:10.1016/0097-3165(73)90012-5 | meta only (paywalled; content not verified) |

## B. Partial results on Barnette's conjecture

| # | Year | Authors | Statement | Method | Hypotheses beyond Barnette | Link | Verified |
|---|---|---|---|---|---|---|---|
| B1 | 1975 | Goodey | Barnette graphs with all faces of size 4 or 6 are Hamiltonian; every edge common to a 4-face and a 6-face is on a Hamiltonian cycle. Also (per Hertel) 7 quadrilaterals, 1 octagon, any number of hexagons. | Induction on faces with reductions | face sizes in {4,6} | doi:10.1007/BF02757273 | via Hertel, Schnieders, Feder-Subi abstract |
| B2 | 1977 | Goodey | Cubic 3-connected planar graphs with only triangles and hexagons are Hamiltonian. | Induction | not bipartite; faces {3,6} | doi:10.1002/jgt.3190010213 | via Hertel; meta |
| B3 | 1985 | Holton, Manvel, McKay | All Barnette graphs with at most 64 vertices are Hamiltonian; H+- (same face) and H-- checked up to 40 vertices; generation of all Barnette graphs from the cube by two expansions. | Generation + computer, lifting a stronger property | n <= 64 | doi:10.1016/0095-8956(85)90072-3 | via Holton-Aldred, Hertel, Florek 2012, Mohar page |
| B4 | 2000 (announced) | Aldred, Brinkmann, McKay | Up to 84 vertices inclusive; for n <= 60 (and n <= 64 without a 4-face adjacent to two others) every pair x, y has a Hamiltonian cycle through x avoiding y. About 3 CPU years. | Same method, plantri | n <= 84 | Mohar problem page | yes (Mohar page) |
| B5 | 2001 | Fowler | List of subgraphs that cannot occur in a minimal counterexample. | Reducible configurations | | unpublished | via Hertel only |
| B6 | 2005 | Hertel | Survey; Barnette iff every path of length 3 on a face has a Hamiltonian cycle through its middle edge avoiding its two end edges; corollaries (any P4 in a Ham. cycle; >= 6 Ham. cycles when a 4-face exists). | Gadget insertion in a face + Kelmans | | Toronto tech. report (pdf/) | yes |
| B7 | 2006 | Feder, Subi | If the faces are 3-coloured and two colour classes contain only 4- and 6-faces, the graph is Hamiltonian; a non-bipartite variant; NP-completeness of spanning trees of faces with 4-sided or arbitrary faces; if Barnette is false then Hamiltonicity of Barnette graphs is NP-complete. | Contract one face class, find a proper quasi spanning tree of faces; spanning tree parity | two colour classes {4,6} | ECCC TR06-015 | yes (abstract; PDF text not extractable) |
| B8 | 2010 | Florek | A Barnette graph with a 2-factor of facial 4-cycles is Hamiltonian (as cited in Florek 2023). | Dual induced trees | facial 4-cycle 2-factor | doi:10.1016/j.disc.2010.01.018 | via Florek 2023 intro; meta |
| B9 | 2011 | Lu | 2-tree colourings of even triangulations; "B-graphs"; certain configurations are reducible. | Reducible configurations in the dual | | doi:10.1016/j.disc.2011.08.011 | via search abstract snippet only (paywalled) |
| B10 | 2013 | Harant | Barnette iff there is c > 0 such that every Barnette graph has a path on at least c|V| vertices. | Substitution of a non-Hamiltonian graph for every vertex, iterated; Bondy-Locke | | doi:10.7151/dmgt.1643 | yes |
| B11 | 2016 | Alt, Payne, Schmidt, Wood | If T's vertices are coloured blue/red, blue hits every face, no blue cycle, every red cycle has a vertex of degree <= 4, the dual is Hamiltonian. Corollary: properly 3-coloured Eulerian T where every red-green cycle has a degree-4 vertex. Limitation theorem: permeating subtrees must contain and exclude >= k vertices of each colour class. Exposition of Kelmans' equivalences. | Dual, permeating subtrees | colouring condition | Australas. J. Combin. 64(2) 354-365; arXiv:1312.3783 | yes |
| B12 | 2016 | Florek | If G[B1 ∪ B2], G[B1 ∪ B3] acyclic (Bi = degree >= 6 vertices of colour i in T), then strong two-induced-tree partitions exist (H+- type). | Dual induced trees | colour/degree condition | doi:10.1007/s10878-014-9797-y, arXiv:1208.4332 | yes (arXiv abstract) |
| B13 | 2020 | Florek | A Barnette graph with a facial 4-cycle 2-factor has at least 3^(2|P*|/Δ(P*)) Hamilton cycles (exponent as printed). | Counting induced-tree partitions | facial 4-cycle 2-factor | doi:10.1007/s10878-019-00460-8, arXiv:1807.08933 | yes (exponent garbled in text dump; check PDF) |
| B14 | 2021 | Bagheri Gh., Feder, Fleischner, Subi | Leapfrog extension of every cyclically 4-edge-connected planar cubic bipartite graph is Hamiltonian; every simple 4-connected Eulerian triangulation has a quasi spanning tree of faces; Goodey-type theorem with parity conditions on separating triangles of the reduced graph. | Facial 2-factor Q, quasi spanning trees of faces in G/Q, contracting triangles under an "invariant property" | leapfrog / colour-class conditions | doi:10.1002/jgt.22612, arXiv:1806.05483 | yes |
| B15 | 2022 | Bagheri Gh., Feder, Fleischner, Subi | Polynomial-time decision of special spanning trees of faces (via spanning tree parity); NP-completeness of related tree-of-faces problems; if Barnette is false, Hamiltonicity of Barnette graphs is NP-complete. | Complexity | | doi:10.3233/FI-222139, arXiv:2212.02668 | yes |
| B16 | 2022 | Brinkmann, Goedgebeur, McKay | Every Barnette graph on at most 90 vertices is Hamiltonian; at most 78: every edge on a Hamiltonian cycle; at most 66: H+- for every pair of edges. About 37 + 5 CPU years. | plantri + cubhamg, lifting via HMM Thm 5 | n <= 90 | doi:10.1090/mcom/3701 | yes |
| B17 | 2024/2025 | Florek | Barnette graphs in which no face has more than four big (>= 6) neighbours are Hamiltonian; >= 2^k Hamilton cycles when each vertex meets a 4-face and a big face. | Dual induced forests | local face condition | doi:10.1002/jgt.23270, arXiv:2309.09578 | yes |
| B18 | 2025 | Bekos, Kaufmann, Pfister | Every n-vertex Barnette graph has a subhamiltonian cycle with at least 5n/6 edges (2-page book embedding with 5n/6 spine edges); improves 2n/3 of Alam et al. 2021. | Edge/face 3-colouring, spanning tree of blue-green faces | | doi:10.4230/LIPIcs.GD.2025.6 | yes |
| B19 | 2025 | Schnieders | Cubic bipartite planar connected graphs with all faces of size <= 8 are Hamiltonian, hence Barnette graphs with faces <= 8. Sharp for connected graphs: a connected non-Hamiltonian example with faces <= 10. | Minimal counterexample, Euler count f4 = 6 + f8, 339,068,624 computer-checked substitution cases (Sage) | faces <= 8 | arXiv:2508.03531 | yes |
| B20 | 2026 | OpenAI | Barnette's conjecture; plus a Hamiltonian cycle avoiding any prescribed edge; plus (via GSW) P4-Hamiltonicity of cubic 3-connected Pfaffian bipartite graphs. | Dual induced trees, Tutte states, signed sum over pairs of states | none | github.com/openai/math, family 180 (`papers/OpenAI-Barnette.pdf`) | yes (read in full) |

## C. Equivalent forms and strengthenings (details in EQUIVALENTS.md)

| # | Year | Authors | Statement | Method | Link | Verified |
|---|---|---|---|---|---|---|
| C1 | 1971 | Stein | A cubic sphere map is Hamiltonian iff the family of region-cycles of length >= 3 has a B-set (dually, the triangulation's vertices split into two induced forests). | B-sets | doi:10.2140/pjm.1971.37.217 | yes |
| C2 | 1986/1994 | Kelmans | Barnette iff H+- on each face (through e1, avoiding e2, both on one face); iff Barnette for cyclically 4-edge-connected graphs; iff (x+y+) for cyclically 4-edge-connected graphs (the last direction "claimed" in a 2003 RUTCOR report). | Four-pole gluing | doi:10.1090/trans2/158/12 | via APSW 2016 Thm 8, Hertel, Harant |
| C3 | 2004/2005 | Hertel; Braverman (pers. comm.) | Barnette iff every edge on a Ham. cycle; iff any two edges of a face on a Ham. cycle; iff H- (avoid any edge). | Gadgets | Hertel 2005 | yes |
| C4 | 1985/1995 | Jensen, Toft (via Král and Stein) | Barnette iff every 3-colourable planar graph splits into two induced forests (vertex arboricity <= 2). | Duality, Král's characterisation of 3-colourable planar graphs | Jensen-Toft p. 45 | via Harant 2013 |
| C5 | 1990 | Fleischner | Barnette iff every simple 3-connected Eulerian plane triangulation has an A-trail. | A-trails | Fleischner, Eulerian Graphs and Related Topics I.1, pp. VI.112-113 | via Bagheri et al. 2021, 2022 |
| C6 | 2013 | Harant | Barnette iff Barnette graphs have linear-length paths. | Substitution | doi:10.7151/dmgt.1643 | yes |
| C7 | 2016 | Alt, Payne, Schmidt, Wood (Lemma 5) | T's dual Hamiltonian iff T has a permeating subtree iff V(T) splits into two induced trees. | Euler count | arXiv:1312.3783 | yes |
| C8 | 2023 | Gorsky, Steiner, Wiederrecht | Barnette iff all cubic planar braces Hamiltonian iff all cubic 3-connected Pfaffian bipartite graphs Hamiltonian iff all are P4-Hamiltonian (Thm 4.16). Tight-cut reductions for H-, H+-, P3, P4. | Matching theory (tight cuts, McCuaig / Robertson-Seymour-Thomas trisums, Little) | doi:10.1016/j.disc.2022.113249, arXiv:2202.11641 | yes |

## D. Complexity results

| # | Year | Authors | Statement | Link | Verified |
|---|---|---|---|---|---|
| D1 | 1976 | Garey, Johnson, Tarjan | Hamiltonian cycle is NP-complete for cubic 3-connected planar graphs (also with all faces >= 5, per Hertel). | doi:10.1137/0205049 | meta; face condition via Hertel |
| D2 | 1980 | Akiyama, Nishizeki, Saito | Hamiltonian cycle is NP-complete for cubic bipartite planar 2-connected graphs. So 3-connectivity cannot be dropped from Barnette. The brief's "Takanori" is this paper: Bagheri et al. and Florek cite it as "Takanori, Takao, Nobuji" (the authors' given names). | J. Inf. Process. 3(2):73-76 (IPSJ) | via Schnieders Thm 1.1, Hertel, Wikipedia ref list |
| D3 | 2006/2022 | Feder, Subi; Bagheri Gh. et al. | If Barnette is false, Hamiltonicity for Barnette graphs is NP-complete. | rows B7, B15 | yes |
| D4 | 1995 | Andersen, Fleischner | A-trail existence NP-complete for 3-connected plane Eulerian graphs with 3- and 4-faces (4-faces one colour). | doi:10.1016/0166-218X(95)80001-K | via Bagheri 2022 |
| D5 | 2023 | Bonnet, Chakraborty, Duron | Perfect Matching Cut is NP-complete on Barnette graphs; "Hamiltonian Cycle would only join this private club if Barnette's conjecture were refuted." | arXiv:2302.11667 | yes (abstract) |

## E. Neighbouring theorems and conjectures

| # | Year | Authors | Statement | Link | Verified |
|---|---|---|---|---|---|
| E1 | 1931 | Whitney | A plane triangulation with no separating triangle (4-connected triangulation) is Hamiltonian. | doi:10.2307/1968197 | via secondary sources (search results); meta |
| E2 | 1956 | Tutte | Every 4-connected planar graph is Hamiltonian (Tutte paths/bridges). | doi:10.1090/S0002-9947-1956-0081471-8 | via Hertel, Holton-Aldred |
| E3 | 1983 | Thomassen | 4-connected planar graphs are Hamiltonian-connected; Tutte paths. Gap completed by Chiba-Nishizeki (per Holton-Aldred). | doi:10.1002/jgt.3190070205 | via Hertel, Holton-Aldred |
| E4 | 1977/2020 | Goodey; Kardoš | Barnette-Goodey conjecture: cubic 3-connected planar graphs with faces <= 6 are Hamiltonian. Proved by Kardoš (computer-assisted), so fullerenes are Hamiltonian. Verified earlier up to 316 vertices (Brinkmann et al.). | doi:10.1137/140984737, arXiv:1409.2440 | yes |
| E5 | 2025 | Shao, Wu | 2-connected cubic planar with faces <= 6 is Hamiltonian; 6 is tight. | arXiv:2504.20706 | yes (abstract) |
| E6 | 1975/2009 | Payan-Sakarovitch; Fleischner-Hobbs-Muzheve | Cyclically 4-edge-connected cubic graph of order n ≡ 2 (mod 4) has an independent set S with G - S a tree; leapfrog of such planar G is Hamiltonian. | doi:10.1016/j.disc.2008.06.011 | via Bagheri et al. 2021 |
| E7 | 2016-2018 | Ozeki, Ye; Hoffmann-Ostenhof, Kaiser, Ozeki | 3-decomposition conjecture (spanning tree + 2-regular + matching) holds for 3-connected plane cubic graphs, then for all connected plane cubic graphs. Claimed full proof: Ma 2026 (arXiv:2608.25385, unrefereed, with Lean). | doi:10.1016/j.ejc.2015.08.005, arXiv:1609.05059 | yes (abstracts) |
| E8 | 2018 | Hine, Kálmán | Tutte's face-vertex matchings ("states") of black/white triangulations form a distributive lattice (clock theorem). | arXiv:1808.06091 | yes (abstract) |
| E9 | 2017 | Knauer, Valicov | Tait, Barnette, Tutte conjectures fit a "cuts in matchings" framework; links to Neumann-Lara. | arXiv:1712.06143 | yes (abstract) |
| E10 | 2024/2025 | Cambie, Dross, Knauer, La, Valicov | CAI-partitions (connected acyclic + independent set) of Eulerian oriented triangulations, at the Barnette / Neumann-Lara intersection. | arXiv:2412.11774 | yes (abstract) |

## F. Claimed proofs that did not stand, and the 2026 events

| # | Year | Who | What | Status | Link | Verified |
|---|---|---|---|---|---|---|
| F1 | 2009 | I. Cahit | "Algorithmic proof of Barnette's Conjecture" via "spiral-chain" opening of chambers. | arXiv draft, never published, never accepted; not audited here | arXiv:0904.3431 | yes (abstract) |
| F2 | 2013 | P. Clarke | "Cyclic subsets and Barnette's conjecture", inductive proof. | Withdrawn by the author on arXiv, v2 (6 Apr 2014): "withdrawn for further review" | arXiv:1309.2560 | yes |
| F3 | 2014 | M. A. Shah | "Necessary condition ... with proof of Barnette's conjecture", Int. J. Math. Combin. 3 (2014) 70-88. | Low-visibility journal; no citations as a proof in any later paper I read (all later papers call the conjecture open) | fs.unm.edu/IJMC | yes (first pages) |
| F4 | 2026-09-24 (dated), public 2026-10-06 | OpenAI | "Paired states and Hamiltonian cycles in cubic bipartite planar graphs", family 180 of the OpenAI math release; Lean formalisation in `lean/OAI/Combinatorics/Hamiltonian/` (31 files, ~8,900 lines, imports only Mathlib, no `sorry` found by grep) checked against `ComparatorChallenges/BarnetteHamiltonian.lean`. | Unrefereed preprint; Lean not built by me | github.com/openai/math | yes (paper read; Lean grepped) |
| F5 | 2026-10-18 | anonymous (PDF metadata has no author) | "A constructive proof of Barnette's conjecture": incidence-tree criterion, exchange graph, signed polynomial, marked walk, O(poly(N) 3^(N/4)). | Not found online by any search I ran | `papers/barnette_trees.pdf` | read (intro) |
| F6 | 2026-10-21 | Zhentao Li | "A note on the proof of Barnette's conjecture", arXiv:2610.30490 v1, two sign-reversing involutions instead of the exponential sum. | arXiv | arXiv:2610.30490 | yes |
| F7 | 2026-10-11 | anxkhn (GitHub) | Issue #7144 and PR #7149 to google-deepmind/formal-conjectures adding the Barnette statement in a "research solved" category, without a `formal_proof` attribute; maintainers asked what evidence suffices. Open as of 2026-11-14. | Open PR | github.com/google-deepmind/formal-conjectures/pull/7149 | yes |
| F8 | 2026-10-25 / 11-06 | Hongmin Li | "Exponentially many Barnette graphs with the global H+- property", Zenodo, treats Barnette as proved, says global H+- for all Barnette graphs remains open; author states AI assistance and no expert review. | Preprint | doi:10.5281/zenodo.24054767 | yes (record page) |
