# GSW chain and dependency audit

## Boundary and sources

LIT. Gorsky, Steiner and Wiederrecht, *Matching theory and Barnette's conjecture*, Discrete Mathematics 346, 2023, article 113249, DOI 10.1016/j.disc.2022.113249. Numbering here follows [arXiv:2202.11641v3](https://arxiv.org/abs/2202.11641v3), 15 August 2022, exactly as OpenAI reference 5 specifies. Read the local full text in `research/2026-11-14_astra_older-approaches/text/2022_Gorsky-Steiner-Wiederrecht_Matching-theory-Barnette_arXiv2202.11641v3.txt`; PDF is in `research/2026-11-14_opus_history-literature/pdf/` with the same stem. Online abstract metadata was also opened. RST, McCuaig and Hertel are accepted as named results in GSW; their original proofs were not independently audited here.

LIT, supplied manuscript. OpenAI Theorem 1.1 asserts Hamiltonicity of every finite simple cubic bipartite planar 3-vertex-connected graph. Corollary 7.1 asserts that each such graph has, for each specified edge, a Hamiltonian cycle avoiding it. Corollary 7.2 asserts that every simple three-edge path in every finite simple cubic 3-vertex-connected Pfaffian bipartite graph extends to a Hamiltonian cycle. This audit accepts Theorem 1.1 as a primitive. It does not re-audit that proof or upgrade the supplied manuscript to peer-reviewed T1.

## Exact statements needed, restated in full

LIT. GSW works with simple graphs. Write B for cubic 3-connected planar bipartite graphs. A brace is C4 or a bipartite 2-extendable graph. A graph is k-extendable when it is connected, has at least 2k+2 vertices, and every matching of size at most k extends to a perfect matching. P4-Hamiltonian means every path of three edges extends to a Hamiltonian cycle. H-minus means every edge can be avoided by some Hamiltonian cycle. H-plus-minus means that for any distinct edges e,f some Hamiltonian cycle contains e and avoids f.

LIT. Theorem 4.3, p.7, attributed to Hertel as a corollary of Kelmans: Barnette's conjecture holds if and only if every graph in B has H-minus. Theorem 4.4, p.7, attributed to Hertel: Barnette's conjecture holds if and only if every graph in B is P4-Hamiltonian. These are universal equivalences, not claims that an individual Hamiltonian graph automatically has those stronger properties.

LIT. Theorem 4.6, p.9, Kasteleyn: every planar graph is Pfaffian. Theorem 4.7, p.10, Vazirani and Yannakakis: a matching covered graph is Pfaffian if and only if all its bricks and braces are Pfaffian.

LIT. A trisum takes three bipartite graphs with pairwise intersection exactly the same four-cycle C, each with vertices outside C, and deletes any chosen subset S of E(C) from their union. A cubic trisum deletes all four edges. Theorem 4.8, p.10, attributed to McCuaig and Robertson, Seymour and Thomas: a brace is Pfaffian if and only if it is Heawood or can be constructed from planar braces by repeated trisums. Corollary 4.9: a cubic brace is Pfaffian if and only if it is Heawood or can be constructed from cubic planar braces by repeated cubic trisums.

PROVED-HERE, T2 unreviewed. The cubic specialization has no degree loophole. Every non-C4 brace has minimum degree at least three. Each summand has vertices outside the shared C, so is not C4. Each boundary vertex contributes at least one edge outside C from each summand. Degree three of the result forces exactly one from each and no retained edge of C. Interior degrees are unchanged. Heawood cannot be a nontrivial summand because it has no four-cycle. This justifies recursion to planar cubic pieces.

LIT. Lemma 4.12, pp.11-12: if G1,G2,G3 are cubic Pfaffian braces, G is their cubic trisum at C, and every Gi is P4-Hamiltonian, then G is P4-Hamiltonian. The hypothesis is P4-Hamiltonicity, not merely H-minus. The proof uses control of the intersections of Hamiltonian cycles with C.

LIT. Lemma 4.2, p.7, McCuaig: the two tight-cut contractions of a nontrivial tight cut of a cubic 3-connected bipartite graph are again cubic, 3-connected and bipartite. Theorem 1.7, p.3, has four clauses for a cubic 3-connected bipartite graph G: if its braces are P4-Hamiltonian then G is P4-Hamiltonian; G has H-minus iff its braces do; G is P3-Hamiltonian iff its braces are; G has H-plus-minus iff its braces do. Lemma 4.5 proves the corresponding statements for one tight cut. Cubic connected bipartite graphs are matching covered by Corollary 1.5, from Konig's perfect matching decomposition.

LIT. Theorem 4.16, pp.12-13: the following six universal assertions are equivalent.

1. Every graph in B is Hamiltonian.
2. Every brace in B is Hamiltonian.
3. Every brace in B is P4-Hamiltonian.
4. Every cubic Pfaffian brace is P4-Hamiltonian.
5. Every cubic 3-connected Pfaffian bipartite graph is P4-Hamiltonian.
6. Every cubic 3-connected Pfaffian bipartite graph is Hamiltonian.

LIT. The proof uses 4.4 for 1 implies 3; 4.9 and 4.12, plus Heawood's P4-Hamiltonicity, for 3 implies 4; and 1.7 for 4 implies 5. Pfaffianity of the braces comes from 4.7. A brace's 3-connectivity comes from Theorem 2.5, that k-extendability for k>1 implies both k-minus-one extendability and k-plus-one connectivity. The C4 exception is not cubic.

## Critical findings

PROVED-HERE, conditional on the accepted literature. OpenAI Theorem 1.1 supplies exactly assertion 1. No extra planar hypothesis is missing. Corollary 7.1 supplies H-minus but is unnecessary for this route. One must not replace the universal Hertel equivalence by the unsupported pointwise assertion that edge avoidance implies P4-Hamiltonicity in every graph.

LIT, textual caution. The v3 proof contains typographical errors. Observation 4.11 says a path in C has length four where it must mean three edges. Lemma 4.12 calls paths between adjacent bipartition colors even in length; they are odd. Its first case defines H2 using edges 01 and 23 but then removes 03 and 12. The intended deletion is E(C). These do not change the exact theorem being cited. Our audit accepts the named theorem, rather than claiming a line-by-line certification of that proof. `PROOFS.md` supplies a corrected basic Hamiltonicity gluing argument, not a replacement proof of all of Lemma 4.12.

## Obligation graph

C0 <- R0 AND O1,O2,O3.
O2 <- named GSW Theorem 4.16, implication 1 to 5.
Expanded explanation of O2: CplanarP4 <- 4.4 AND O1; CbraceP4 <- 4.9 AND 4.12 AND CplanarP4 AND Heawood base; CgeneralP4 <- 1.7 AND 4.2 AND 4.7 AND CbraceP4.

| ID | Exact obligation | Needed by | Route | Classification | Support | Status |
|---|---|---|---|---|---|---|
| C0 | OpenAI Corollary 7.2 | root | R0 | root | O1-O3 | discharged |
| O1 | All graphs in B are Hamiltonian | C0 | R0 | proved earlier | accepted OpenAI 1.1 | discharged |
| O2 | That universal assertion implies every cubic 3-connected Pfaffian bipartite graph is P4-Hamiltonian | C0 | R0 | named theorem | opened GSW 4.16 | discharged |
| O3 | Finite simple graph and path conventions match | C0 | R0 | definition | both texts, three-edge P4 | discharged |
| CplanarP4 | All planar cubic braces are P4-Hamiltonian | O2 expansion | 4.4 | named theorem | GSW 4.4 and 2.5 | discharged |
| CbraceP4 | All cubic Pfaffian braces are P4-Hamiltonian | O2 expansion | trisum induction | named theorem | GSW 4.9, 4.12, Heawood base | discharged |
| CgeneralP4 | Lift from Pfaffian braces to G | O2 expansion | tight-cut induction | named theorem | GSW 1.7, 4.2, 4.7, 1.5 | discharged |

## Verdict

FOLLOWS, relative to the explicit audit boundary. O1-O3 close the route actually cited by OpenAI. The previously unavailable named-theorem leaf is now discharged. This is a literature-dependent mathematical corollary, not a Lean-checked corollary. No direct nonplanar states proof has been supplied by this implication.
