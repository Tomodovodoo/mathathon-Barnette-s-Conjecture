# Equivalent formulations of Barnette's conjecture

Notation follows `research/BRIEF.md`. `G` is a Barnette graph (cubic, bipartite, planar, 3-connected), `T = G*` its dual. `T` is a simple sphere triangulation with at least four vertices whose faces are properly 2-coloured black and white. A plane triangulation is Eulerian (all degrees even) iff its faces are 2-colourable iff its vertices are 3-colourable, and then the vertex 3-colouring is unique up to names. So "Eulerian triangulation", "face-bicoloured triangulation" and "3-colourable triangulation" name the same objects. The dual of a simple triangulation on at least four vertices is a 3-connected cubic plane graph, and it is bipartite iff the triangulation is Eulerian (APSW 2016, Section 1).

Each entry gives the statement, the source, the idea of the equivalence in two lines, and whether the OpenAI paper (`papers/OpenAI-Barnette.pdf`) uses it. Status of every equivalence is `LIT` unless marked. "Checked" means I read the statement in the source; where I could only read a secondary source I say so.

A general remark first. Several entries are equivalences of the form "Barnette's conjecture holds iff every Barnette graph has the stronger property P". If the OpenAI proof is correct, P now holds for every Barnette graph, but only as securely as the published proof of the equivalence. For Kelmans' equivalences that is a real caveat: Alt, Payne, Schmidt and Wood write that the original publications "contained very few details" and that in their exposition "some details are still left to the reader to verify", and one direction was only "claimed by Kelmans" in a 2003 RUTCOR report.

---

## 1. Polyhedral form

**Statement.** Every simple convex 3-polytope all of whose 2-faces have an even number of edges has a Hamiltonian graph.

**Source.** Steinitz's theorem; stated this way by Schnieders 2025 (intro) and Wikipedia. Checked.

**Idea.** Steinitz: 3-connected planar graphs are exactly graphs of 3-polytopes; cubic means simple; a plane graph is bipartite iff every face is even.

**OpenAI.** Not used.

## 2. Dual triangulation form

**Statement.** For every simple Eulerian (equivalently, properly 3-vertex-colourable, equivalently face-bicoloured) plane triangulation `T` with at least four vertices, the dual cubic graph `T*` has a Hamiltonian cycle.

**Source.** Folklore; APSW 2016 Section 1; Florek 2023 intro ("G* ∈ P iff G is an Eulerian plane triangulation different from the 3-cycle"). Checked.

**Idea.** Duality between 3-connected cubic plane graphs and simple triangulations; bipartite primal iff Eulerian dual. The proof of Theorem 1.1 in the OpenAI paper redoes this, including simplicity of `T` from 3-connectivity.

**OpenAI.** Used. It is the setting of the whole proof.

## 3. Stein's B-sets, two induced forests

**Statement (Stein 1971, Theorem 2.2).** Let `M` be a 3-regular map on the sphere. The 1-skeleton of `M` has a Hamiltonian circuit iff the family of all region-cycles of length at least three has a B-set, that is, the regions split into two classes neither of which contains a region-cycle of length at least three.

Dual reading: `T*` is Hamiltonian iff `V(T)` splits into two sets each inducing a forest.

**Source.** S. K. Stein, B-sets and planar maps, Pacific J. Math. 37 (1971) 217-224. Checked (Theorem 2.2 and its proof opening). Stein remarks that Theorem 2.2 contradicts an assertion in a reference [2: p. 616] of his paper.

**Idea.** A Hamiltonian cycle is a Jordan curve; regions inside and regions outside form the two classes, and a region-cycle inside one class would enclose a vertex the cycle misses. Conversely the boundary between the two classes is a 2-regular graph that must be connected.

**OpenAI.** Used, through the APSW form (entry 4). Cited as [13, Theorem 2.2].

## 4. Two induced trees, permeating subtrees

**Statement (APSW 2016, Lemma 5).** For a plane triangulation `T` the following are equivalent: (1) `T*` is Hamiltonian; (2) `T` contains a permeating subtree, an induced subtree meeting every face; (3) `V(T)` partitions into two sets each inducing a tree.

**Source.** H. Alt, M. S. Payne, J. M. Schmidt, D. R. Wood, Thoughts on Barnette's conjecture, Australas. J. Combin. 64(2) (2016) 354-365, arXiv:1312.3783, Lemma 5 (attributed to [Florek 2010, Florek 2012, Skupień 2002, Stein 1971]). Checked.

**Idea.** In a triangulation each face has exactly one monochromatic edge in a partition with no monochromatic triangle, so there are `f/2 = n-2` monochromatic edges; two induced forests with `n - 2` edges on `n` vertices have exactly two components, hence are two trees. Contracting the two trees leaves a two-vertex multigraph whose dual is a cycle, the Hamiltonian cycle of `T*`.

Note the counting shows that for triangulations, "two induced forests" (Stein) and "two induced trees" (APSW, Florek, Lu's "2-tree colouring") are the same thing.

**OpenAI.** Used. Theorem 2.2 is a strengthening of (3), and the last step of the proof (Section 6.2 and the proof of Theorem 1.1) is exactly the argument of this lemma.

## 5. Vertex arboricity of 3-colourable planar graphs

**Statement.** Barnette's conjecture holds iff every 3-colourable planar graph has vertex arboricity at most 2 (its vertices split into two sets each inducing an acyclic subgraph). Equivalently, Barnette fails iff some planar graph has chromatic number 3 and point arboricity 3.

**Source.** Jensen and Toft, Graph Coloring Problems (1995), p. 45, as quoted by Harant 2013, who says the proof "is a consequence of the results of Król and Stein". Checked via Harant; I did not see Jensen-Toft.

**Idea.** Every 3-colourable planar graph is a subgraph of an Eulerian triangulation (Król, as cited by Harant), and a partition into induced forests passes to subgraphs; for Eulerian triangulations, entry 3 converts forests to a Hamiltonian dual.

**Correction worth recording.** Hertel's 2005 survey states this as a property of the Barnette graph itself ("partition its vertex set into two subsets so that each induces an acyclic subgraph of G") and notes in brackets that it must be wrong as stated. It is wrong as stated; the statement is about the dual triangulation (or 3-colourable planar graphs), as Harant gives it.

**OpenAI.** Touched only through entry 4.

## 6. A-trails in Eulerian triangulations

**Statement.** Barnette's conjecture holds iff every simple 3-connected Eulerian plane triangulation has an A-trail, an Euler trail in which consecutive edges are consecutive in the rotation at their common vertex (so they lie on a common face). Related: a 2-connected plane cubic bipartite graph is Hamiltonian iff its dual has a non-separating A-trail (Fleischner, Theorem VI.71).

**Source.** H. Fleischner, Eulerian Graphs and Related Topics, Part 1 Vol. 1, Ann. Discrete Math. 45 (1990), pp. VI.112-VI.113, as stated in Bagheri Gh., Feder, Fleischner, Subi 2021 (JGT) and 2022 (Fund. Inform.). Checked via those two papers; the book is not open access.

**Idea.** An A-trail splits every vertex of the triangulation in one of two ways ("1-splitting" or "2-splitting"); the induced vertex partition and the set of faces of one colour give a quasi spanning tree of faces, which traces a Hamiltonian cycle of the dual.

**OpenAI.** Not used. A-trails are complexity-hard in general: Andersen and Fleischner (1995) proved A-trail existence NP-complete for 3-connected plane Eulerian graphs with only 3- and 4-faces.

## 7. Spanning trees of faces in a reduced graph

**Statement (Bagheri Gh., Feder, Fleischner, Subi 2021, Proposition 1).** Let `G` be a 3-connected cubic plane graph with a facial 2-factor `Q`, and `H = G/Q` (contract every `Q`-face to a vertex). Then `H` has a quasi spanning tree of faces with the outer face not used iff `G` has a Hamiltonian cycle with prescribed inside/outside behaviour of the `Q`-faces and no two inner non-`Q` faces sharing an edge. A quasi spanning tree of faces is a set of edge-disjoint faces whose restricted radial (vertex-face incidence) graph is a tree, with degree conditions at "quasi" vertices.

Every Barnette graph has facial 2-factors: its faces are properly 3-colourable, and each colour class covers every vertex exactly once.

**Source.** doi:10.1002/jgt.22612, arXiv:1806.05483; first in Feder-Subi 2006. Checked.

**Idea.** Walking around the boundary of a cactus of faces in `H` and expanding each contracted `Q`-face gives a Hamiltonian cycle of `G`, and conversely.

This is a sufficient condition with constraints, not an equivalence with Barnette's conjecture as stated. I include it because it is the closest older relative of the OpenAI incidence-tree step (see WHAT-WAS-HARD.md, section 3).

**OpenAI.** Not used.

## 8. Kelmans' equivalences

**Statement (Kelmans 1986/1994, as given in APSW 2016, Theorem 8).** The following are equivalent:

1. Every Barnette graph is Hamiltonian.
2. Every Barnette graph is (x+y-)-Hamiltonian for every two edges x, y on a common face: some Hamiltonian cycle contains x and avoids y.
3. Every cyclically 4-edge-connected Barnette graph is Hamiltonian.
4. Every cyclically 4-edge-connected Barnette graph is (x+y+)-Hamiltonian for every x, y on a common face.

In the dual, cyclically 4-edge-connected means `T` has no separating triangle; so (3) reads: it suffices to treat Eulerian triangulations without separating triangles.

**Source.** A. K. Kelmans, Constructions of cubic bipartite 3-connected graphs without Hamiltonian cycles, AMS Transl. (2) 158 (1994) 127-140 (doi:10.1090/trans2/158/12), translated from Sb. Tr. VNIISI 10 (1986) 64-72. Exposition with proof sketches: APSW 2016 Section 5. Also Hertel 2005, Harant 2013. Checked via APSW and Hertel; Kelmans' paper not seen.

**Idea.** (1)⇒(2) and (3)⇒(4) go by contradiction: cut x and y to make a "four-pole" from a bad graph, then glue two or four copies so that the bad property propagates into a non-Hamiltonian Barnette graph (a parity "covering path property" of four-poles does the bookkeeping). (4)⇒(1) inducts on cyclic 3-edge-cuts: contract each side, both pieces are Barnette, and the (x+y+) property on the side without cuts lets the two Hamiltonian cycles agree on the three cut edges.

**OpenAI.** Partly. The OpenAI proof contains its own version of (4)⇒(1): Theorem 2.2 prescribes an edge of the root face, and Section 7 glues partitions across a separating triangle using that prescription. This is the dual of Kelmans' cut-and-glue, with "edge e0 in one tree, third vertex in the other" playing the role of (x+y+)/(x+y-) at the cut. The OpenAI paper does not cite Kelmans for this step; it cites Kelmans only for the edge-avoidance equivalence (entry 9).

## 9. Hertel's and Braverman's strengthenings

**Statements.** Each is equivalent to Barnette's conjecture:

- every edge of a Barnette graph lies on a Hamiltonian cycle (Hertel 2004 thesis);
- every two adjacent vertices are joined by a Hamiltonian path (corollary of the previous);
- for any face and any two edges of it, some Hamiltonian cycle contains both (Braverman, personal communication to Hertel, 2004);
- **H-**: every edge is avoided by some Hamiltonian cycle (Hertel, Corollary 3);
- any path of length 3 on a face: some Hamiltonian cycle uses its middle edge and avoids its two end edges (Hertel 2005, Theorem 12, the "x-y-z" form);
- any path of length 3 lies on a Hamiltonian cycle, i.e. P4-Hamiltonicity (Hertel, Corollary 6);
- every Barnette graph with a 4-face has at least 6 Hamiltonian cycles (Corollary 7).

**Source.** A. Hertel, A survey and strengthening of Barnette's conjecture, Univ. Toronto tech. report, 29 April 2005. Checked. Hertel himself records that Kelmans had proved the edge statements earlier.

**Idea.** Gadget insertion. Subdivide a face by adding vertices and edges so the result is still a Barnette graph; apply the face form of Kelmans (delete one edge, mark another) in the bigger graph; forced-edge propagation at degree-2 and saturated degree-3 vertices turns this into the required behaviour in the original graph.

**OpenAI.** Used. Corollary 7.1 (Hamiltonian cycle avoiding any edge) is the H- form, and the paper cites Hertel [7, Corollary 3] and GSW [5, Theorem 4.3] for its equivalence with Barnette. More to the point, the prescribed edge in Theorem 2.2 is the dual form of H-: requiring `e0` inside an induced tree is requiring the dual edge `e0*` off the Hamiltonian cycle, and then cubicity forces the other two edges at the dual vertex onto the cycle. So the OpenAI proof proves H- directly, and needs it for the separating-triangle induction.

## 10. Linear-length paths

**Statement (Harant 2013, Theorem 4).** Barnette's conjecture holds iff there is a constant c > 0 such that every Barnette graph `G` has a path on at least c|V(G)| vertices.

**Source.** J. Harant, A note on Barnette's conjecture, Discuss. Math. Graph Theory 33 (2013) 133-137, doi:10.7151/dmgt.1643. Checked.

**Idea.** Bondy-Locke turn a long path into a long cycle in 3-connected cubic graphs. If some Barnette graph on k vertices is non-Hamiltonian, delete a vertex and substitute the rest for every vertex of the cube, iterate; the longest cycle grows like (k-2)^i while the order grows like (k-1)^i, so the ratio tends to 0.

A consequence worth stating: a single non-Hamiltonian Barnette graph would make the shortness coefficient of the class zero. So the class was always "all or very little".

**OpenAI.** Not used.

## 11. Matching theory: braces and Pfaffian graphs

**Statement (Gorsky, Steiner, Wiederrecht 2023, Theorem 4.16).** Equivalent:

1. all graphs in the Barnette class are Hamiltonian;
2. all braces in the class are Hamiltonian;
3. all braces in the class are P4-Hamiltonian;
4. all cubic Pfaffian braces are P4-Hamiltonian;
5. all cubic 3-connected Pfaffian bipartite graphs are P4-Hamiltonian;
6. all cubic 3-connected Pfaffian bipartite graphs are Hamiltonian.

Also (Corollary 4.15, from Holton-Plummer): a cubic 3-connected bipartite graph is a brace iff it is cyclically 4-connected. And Theorem 1.7: for cubic 3-connected bipartite graphs, H-, P3- and H+- hold iff they hold for all braces; P4 lifts from braces.

**Source.** Discrete Math. 346(2) (2023) 113249, doi:10.1016/j.disc.2022.113249; arXiv:2202.11641v3. Checked. They also note that the Horton graph is not Pfaffian (it has K3,3 as a brace) and ask whether every planar brace is Hamiltonian (Question 6.1) and for the smallest non-planar non-Hamiltonian brace (Question 6.2).

**Idea.** Tight cuts in a cubic 3-connected bipartite graph are 3-edge-cuts, and Hamiltonicity properties pass through tight cut contractions (Lemma 4.5). Non-planar Pfaffian braces are built from planar ones and the Heawood graph by cubic trisums (McCuaig; Robertson-Seymour-Thomas), and P4-Hamiltonicity survives trisums (Lemma 4.12). Kasteleyn (planar graphs are Pfaffian) closes the loop from (6) to (1).

**OpenAI.** Used as a consequence only: Corollary 7.2 applies (i)⇒(v). The planar proof does not use Pfaffians. See WHAT-WAS-HARD.md section 4 for a remark on signs.

## 12. Book embeddings

**Statement.** A planar graph is Hamiltonian iff it has a 2-page book embedding in which every pair of consecutive spine vertices, including last and first, is joined by an edge. So Barnette's conjecture says every Barnette graph has a subhamiltonian cycle with n edges.

**Source.** Bekos, Kaufmann, Pfister, Approximating Barnette's conjecture, GD 2025, LIPIcs 357, paper 6, doi:10.4230/LIPIcs.GD.2025.6. Checked.

**Idea.** The Hamiltonian cycle is the spine; the inside and outside edges are the two pages.

**OpenAI.** Not used.

## 13. Complexity form (conditional)

**Statement.** If Barnette's conjecture is false, Hamiltonicity restricted to Barnette graphs is NP-complete (Feder-Subi 2006; Bagheri Gh. et al. 2022). Since a true conjecture makes the problem trivial, under P ≠ NP the conjecture is equivalent to "Hamiltonicity of Barnette graphs is not NP-complete".

**Source.** ECCC TR06-015 abstract; Fund. Inform. 188 (2022). Checked (abstracts and intro).

**Idea.** A single non-Hamiltonian Barnette graph can be used as a gadget in a reduction from an NP-complete Hamiltonicity problem.

**OpenAI.** Not used.

## 14. The OpenAI intermediate forms

These are statements introduced by the 2026 papers. Before 2026 none of them was known to imply Barnette's conjecture; the papers prove both that they imply it and that they hold. I list them so that other agents can see them next to the classical forms.

**14a. Prescribed-edge induced-tree partition (OpenAI Theorem 2.2).** For every face-bicoloured sphere triangulation `T`, every face `t0` and every edge `e0` of `t0`, `V(T)` splits into two induced trees with the endpoints of `e0` in one tree and the third vertex of `t0` in the other. Equivalent to H- (entry 9) by duality as explained there, hence to Barnette's conjecture (via Hertel/Kelmans).

**14b. Forest state (OpenAI Proposition 5.1 with Lemma 6.1).** If `T` has no separating triangle there is a pair of states `(r, s)` with `Q_s` a forest; then each component of `Q_s` has exactly one root. The paper derives 14a from this.

**14c. Incidence-tree criterion (constructive paper, Theorem 1.2).** With the spoke graph `H` and incidence graph `B` on `A ∪ X`, the following are equivalent: (i) a perfect matching `s` of `B` with `H - s` a spanning tree; (ii) `B` has two edge-disjoint perfect matchings; (iii) no separating triangle has black inner boundary. Also: `H` has a spanning tree with degree 2 at bounded black centres, 3 at the outer centre, d_H(x) - 1 at non-roots, d_H(v) at roots.

**14d. Cycle-breaking matching (Li 2026, proof sketch).** In the face-black-vertex incidence graph `G_FB` of a cyclically 4-edge-connected Barnette graph with root edge `b0w0`, there is a perfect matching `M` of `G_FB - N[b0]` such that `G_FB - M` is a spanning tree. This is 14c in the primal.

**OpenAI.** These are the proof.

## Which equivalences the OpenAI proof touches

| Entry | Role in the OpenAI paper |
|---|---|
| 2 dual triangulation | the setting |
| 3 Stein, 4 APSW | used directly; the final step is Lemma 5 of APSW |
| 8 Kelmans (separating triangles, cut and glue) | re-proved in dual form in Section 7, not cited for this |
| 9 H- (Hertel, Braverman, Kelmans) | proved as Corollary 7.1 and built into Theorem 2.2 |
| 11 GSW Pfaffian/P4 | consequence, Corollary 7.2 |
| 14 | the new content |
| 1, 5, 6, 7, 10, 12, 13 | not touched |

If the OpenAI theorem stands, these become theorems as well, as securely as their equivalence proofs: all forms in entries 5, 6, 9, 10, 11, 12, the face form of H+- from entry 8 (via Kelmans' (1)⇒(2), whose published proof is a sketch), and the six-cycles-with-a-4-face statement. Global H+- for arbitrary pairs of edges does not follow and is still open (Hongmin Li, Zenodo 2026, states the same).
