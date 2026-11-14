# What was hard: why Barnette's conjecture lasted 57 years

This file separates three kinds of statement: what the literature says (`LIT`, cited), small facts I check here (`PROVED-HERE`, proof inline), and my reading of it (`HUNCH`). Citations are BibTeX keys in `bibliography.bib`.

## 0. Short version

`HUNCH`. Before 2026 every serious approach was one of four kinds.

1. Local reductions: induction on faces, reducible configurations, computer-checked substitutions.
2. Colouring constraints in the dual.
3. Strengthenings built to find a counterexample.
4. Translations into other theories, such as matching theory, A-trails or book embeddings.

The local methods stalled because a Barnette graph can have faces of any size and 3-connectivity is a global condition that a bounded neighbourhood cannot see. The translations stalled because they produced equivalent problems with no new existence mechanism. The OpenAI proof supplies one. It replaces "find the good object" with "count all candidate objects with signs and show the bad ones cancel while the total does not". As far as I can find, nobody had done that in the Barnette literature. The other two necessary pieces, the reduction to triangulations without separating triangles and the edge-avoidance strengthening that makes the reduction glue, were already in Kelmans (1986) and Hertel (2005).

## 1. The class sits on a knife edge

`LIT`. Dropping any single hypothesis gives non-Hamiltonian graphs: Tutte's graph (not bipartite), Horton's graph (not planar), Kirkman's graph (not cubic) [hertel2005], and NP-completeness for 2-connected cubic bipartite planar graphs [ans1980]. Hertel's own summary: Barnette graphs "seem to exist on a knife-edge between Hamiltonicity and non-Hamiltonicity" [hertel2005]. Two results make this precise:

- if the conjecture were false, Hamiltonicity in the class would be NP-complete [feder-subi2006], [bagheri2022];
- one non-Hamiltonian Barnette graph would make longest cycles sublinear in the whole class [harant2013].

`HUNCH`. Together these say there was no room for an "approximately true" theorem that could be pushed to the full one by a sequence of improvements. Bekos-Kaufmann-Pfister's 5n/6 subhamiltonian cycle [bekos2025] is real progress in its own terms, but Harant's theorem shows that no linear bound short of n can be the last step before the full result. Either every Barnette graph is Hamiltonian or the class is as bad as general NP-hard instances.

`HUNCH`. Any proof has to use bipartiteness somewhere essential, because Tutte's graph satisfies the other three hypotheses. Tutte-path and Tutte-bridge methods [tutte1956], [thomassen1983] are about 4-connected graphs and do not see a 2-colouring. Whitney's theorem [whitney1931] gives Hamiltonian cycles in triangulations without separating triangles, which are cycles in `T`, not in `T* = G`. In the OpenAI paper the black/white face colouring of `T` (the dual of bipartiteness) is used throughout. Its first and most basic use is the count (2.1): `#white = #black = k` and `|V(T)| = k + 2`, hence `|A| = |X| = k - 1`. That equality is what makes a state, a bijection from bounded black faces to non-root vertices, possible at all.

## 2. Grinberg's theorem gives no obstruction here

`LIT`. Grinberg's formula [grinberg1968] is the classical tool for proving cubic planar graphs non-Hamiltonian. Hertel remarks that using it against Barnette "seems to be difficult; since all faces in Barnette graphs have an even number of sides ... may require some clever trick, if it is at all possible" [hertel2005]. Krooss wrote a paper on exactly this question in 2004 (cited in [apsw2016]); I could not obtain it.

`PROVED-HERE`. The standard Grinberg argument needs a modulus m such that m divides (i-2) for every face size present except one face, which then makes sum (i-2)(f_i' - f_i'') nonzero mod m. In a Barnette graph that pattern cannot occur with the classical choice. For any cubic plane graph, sum over faces of (6 - |f|) = 12. (Use 2E = 3V and Euler; then 6F - 2E = 6(2 - V + E) - 2E = 12 - 6V + 4E = 12.) With all faces even this reads f_4 = 6 + sum over k ≥ 8 of (k/2 - 3) f_k, so there are at least six 4-faces, each with weight i - 2 = 2. A modulus m dividing every weight but one must divide 2, so m = 2, and every weight is even, so mod 2 says nothing. Grinberg contradictions therefore need information about which 4-faces lie inside the cycle, and a face count alone does not supply it. This is a remark about the classical technique only, not a proof that no Grinberg-type obstruction exists.

`HUNCH`. The OpenAI disk identity (Lemma 4.1) is a Grinberg-type count in the dual. Signed side counting in a disk of `T` gives 3(B - W) = 2l - h, a Grinberg balance between black and white triangles. The new ingredient is the extra relation B = I + l, which holds only because a state is a bijection. Combined, these force the δ-sum of every directed state cycle to be exactly ±3. So the proof does not use Grinberg as an obstruction; it rigidifies a Grinberg count with a matching, and the rigid count becomes the phase i^J that cancels. That is my reading, not a claim made in the paper.

## 3. Face-size induction and reducible configurations

`LIT`. Most partial results bound the face sizes:

- Goodey: faces 4 and 6 [goodey1975];
- Feder-Subi: two colour classes with 4 and 6 only [feder-subi2006];
- Bagheri Gh. et al. 2021, leapfrog and colour-class conditions [bagheri2021];
- Florek 2025, local conditions on big faces [florek2025];
- Schnieders: all faces at most 8, with 339 million computer cases [schnieders2025];
- in the non-bipartite setting, Kardoš: faces at most 6 [kardos2020].

The Euler count above forces many 4-faces. A minimal counterexample therefore has a 4-face, and the proofs reduce configurations around 4-faces.

`LIT`. Schnieders lists why this does not extend [schnieders2025, Section 6]:

1. The number of cases may grow fast as the face bound goes from 8 to 10 to 12, and might not stay finite for all Barnette graphs.
2. With unbounded faces, "there would exist faces that cannot be covered by any neighbourhood", so more global arguments, like his use of Euler's formula, would be needed.
3. Without 3-connectivity the statement is already false at face size 10. Schnieders' connected non-Hamiltonian example has all faces at most 10, so a local substitution scheme must be restricted to 3-connected substitutions, and the code would have to be rewritten.

`LIT`. In the Holton-Manvel-McKay generation scheme (cube and C4 expansions), cube-expansions preserve Hamiltonicity, so "the main challenge in Barnette's conjecture lies in handling" the C4-expansion [bekos2025]. Bekos et al. ask whether graphs generated by C4-expansions alone are all Hamiltonian.

`HUNCH`. Point 3 is the deep one. Reducible-configuration methods prove theorems about classes that are closed under the reductions. Below face size 10 the connected class is already Hamiltonian, so 3-connectivity is not needed. From face size 10 on, the theorem is true only because of 3-connectivity, which is a statement about every 2-vertex cut of the whole graph. No bounded neighbourhood certifies it. The OpenAI proof uses 3-connectivity once, globally: in the proof of Theorem 1.1 it rules out edge cuts of size one or two, so the dual `T` is a simple triangulation. Everything after that is about simple face-bicoloured triangulations, and the proof never looks at a local configuration.

## 4. Spanning trees of faces (Feder-Subi and successors)

`LIT`. Feder and Subi contract one face colour class of `G` and look for a proper quasi spanning tree of faces in the reduced graph [feder-subi2006]. That is a set of faces whose vertex-face (radial) incidence graph is a tree, with degree conditions at the contracted vertices. When all remaining faces have 2 or 3 sides, the existence question is a spanning tree parity problem and is polynomial. With 4-sided faces, or arbitrary ones, the general question is NP-complete for reduced graphs of even degree [feder-subi2006], [bagheri2022]. This is why their theorem needs two colour classes of 4- and 6-faces: those become 2- and 3-sided faces after contraction. Bagheri Gh. et al. prove that every simple 4-connected Eulerian triangulation has a quasi spanning tree of faces. Whether those triangulations have an A-trail (equivalently, for Barnette's conjecture, a Hamiltonian dual) they leave open [bagheri2021].

`HUNCH`. This is the closest older relative of the OpenAI method, and the comparison shows what changed.

- **Feder-Subi.** The object is a spanning tree inside a vertex-face incidence graph with prescribed degrees, as in the OpenAI incidence tree. The constructive paper's Theorem 1.2 is literally "H has a spanning tree with degrees 2 at bounded black centres ...".
- **OpenAI.** The faces carrying the constraints are the black triangles of `T`, all of size 3, whatever the face sizes of `G`. The large faces of `G` become high-degree vertices of `T`, and the constraint there is that a state uses each vertex exactly once, not a face-size condition. So the dual switch puts every constraint in the "3-sided" regime where Feder and Subi already had a tractable case, and moves the difficulty into the global bijection.
- **Complexity.** The NP-completeness of general spanning trees of faces explains why the extra structure must be used. The Eulerian colouring and the bijection give the disk identity, and the disk identity is what the cancellation runs on.

`CONJECTURE` (lead, not checked). Bagheri Gh. et al.'s Theorem 11 asks that every triangle of the reduced graph have an even number of vertices inside, plus a condition on separating digons. The constructive paper's obstruction is a separating triangle of `T` "with black inner boundary". These may be the same parity obstruction seen from opposite sides. Test: on small Eulerian triangulations with separating triangles (plantri), compute both conditions after the standard identification of `G/Q` with a quotient of `T`, and check whether they fail on the same triangles.

## 5. Colouring approaches in the dual

`LIT`. APSW's main theorem and Florek's series give two induced trees when the 3-colour classes of `T` satisfy acyclicity or degree conditions [apsw2016], [florek2016], [florek2025]. APSW also prove a limitation theorem. There are properly 3-coloured Eulerian triangulations in which every permeating subtree contains at least k vertices of every colour class and misses at least k of each. So "any approach that ... constructs a permeating subtree with all or no vertices from a colour class ... is insufficient" [apsw2016].

`HUNCH`. The OpenAI trees respect this limitation automatically. They are not built from colour classes. They come from a state, a matching that assigns each black triangle one of its three corners, one corner of each colour. A tree on the white faces then selects one edge per face. The colour classes play no role after (2.1).

## 6. The strengthening programme gave the induction hypothesis

`LIT`. Kelmans proved the reduction to cyclically 4-edge-connected graphs, which in the dual means no separating triangles. His argument glues Hamiltonian cycles across a cyclic 3-edge-cut using the (x+y+) property on the cut-free side [apsw2016, Theorem 8, (4)⇒(1)]. Hertel and Braverman proved that H-, avoiding any prescribed edge, is equivalent to Barnette's conjecture [hertel2005].

`LIT` (OpenAI paper). Theorem 2.2 prescribes a facial edge `e0` inside one induced tree. In primal terms the Hamiltonian cycle avoids `e0*`, the H- property. Section 7 uses the prescription to make the partitions of the two sides of a separating triangle agree on the cap, and glues.

`LIT`. There is a hard limit on how strong the induction hypothesis may be. Deciding whether a Barnette graph has a Hamiltonian cycle through an arbitrary prescribed set of edges is NP-complete, unconditionally. Bagheri Gh. et al. reduce Akiyama-Nishizeki-Saito instances along 2-edge-cuts, and each cut becomes a prescribed edge in a 3-connected piece [bagheri2022, proof of Theorem 4.6]. So "prescribe what you need at every cut" fails in general. A workable hypothesis must prescribe something bounded: one avoided edge (H-), two edges on a face (Kelmans), or a path of length 3 (Hertel, GSW).

`HUNCH`. So the shape of the induction was in the literature by 1986/2005: prove the H- form, reduce to the case without separating triangles, glue. That case was where everything was stuck, and it is where all the new mathematics of the OpenAI paper goes (Sections 3 to 6). The paper does not cite Kelmans for the gluing; it re-proves it.

## 7. Translations without an existence engine

`LIT`. Gorsky-Steiner-Wiederrecht's matching-theory translation shows the planar case is equivalent to a non-planar Pfaffian one [gsw2023]. Fleischner's A-trails [bagheri2021] and Bekos et al.'s book embeddings [bekos2025] are other dictionaries. Each turns the conjecture into a statement of the same difficulty in another language.

`HUNCH`. Gorsky, Steiner and Wiederrecht came closest in spirit. Pfaffian orientations are exactly the device that turns a signed sum over perfect matchings into a determinant (Kasteleyn, Theorem 4.6 in [gsw2023]). Their paper, though, uses Pfaffians only as a class of graphs, through tight cuts and trisums, never as a counting tool. The OpenAI proof signs pairs of perfect matchings of the incidence graph `B` by i^J, with J computed by the disk identity, and shows that cancellation kills every pair whose `Q_s` contains a cycle. That is a Kasteleyn-like sign trick on a different object. I have not checked whether the OpenAI sum is a Pfaffian or a determinant in disguise. The constructive paper's "determinant bound 3^(N/4)" suggests a determinant enters at least for counting (see the Sol and Fable route agents' folders).

## 8. Computation hit its limits

`LIT`. The record is 90 vertices [bgm2021], achieved by checking a stronger property up to 66 vertices (about 37 CPU years, plus 5 more for 68 and 70 vertices with a restriction) and lifting by the Holton-Manvel-McKay theorem. Hertel predicted in 2005 that the computer era was ending [hertel2005]. Harant's theorem [harant2013] means a counterexample, if one existed, need not be pathological. But Holton and Aldred observed for the Barnette-Goodey case that a counterexample "may be hard to find by a blind search" [holton-aldred1999].

## 9. What the OpenAI proof has that the literature did not

I list each idea and say whether I found it in the pre-2026 Barnette literature. My corpus is the 24 PDFs in `pdf/`. As a `COMPUTED` check I ran `pdftotext -layout` on each and then `grep -l -i` for trinity, Kenyon, Temperley, Kasteleyn, Pfaff, sign-reversing, involution, clock theorem, Kauffman, leaving out Hine-Kálmán, which is itself the state paper. That leaves 23 Barnette-related papers, 1968 to 2025. Only Gorsky-Steiner-Wiederrecht mention Pfaffian or Kasteleyn. None mentions Tutte's trinity, Temperley, Kenyon, Kauffman or involutions. The Feder-Subi PDF has no extractable text, so the grep does not cover it, and its abstract mentions none of these.

| Idea | In the OpenAI paper | Earlier in the Barnette literature? |
|---|---|---|
| Dual Eulerian triangulation, two induced trees | Thm 2.2, Sec. 6 | Yes: Stein 1971, Florek 2010, APSW 2016, Lu 2011 |
| Prescribed edge (H-) as the induction hypothesis | Thm 2.2, Cor. 7.1 | Yes as an equivalence: Kelmans 1986, Hertel 2005 |
| Reduction to no separating triangles by gluing | Sec. 7 | Yes: Kelmans 1986 (APSW Thm 8) |
| Tutte states (face-vertex matchings) as configurations | Sec. 2 | No. Tutte 1975 and Hine-Kálmán 2018 are outside this literature |
| Two disjoint states via a planar density inequality and max-flow | Prop. 3.1 | No. Sharpened by the constructive paper to an exact criterion |
| Disk identity: δ-sum of a directed state cycle is ±3 | Lemma 4.1 | No. The Grinberg-type part 3(B-W) = 2l-h is classical, the bijection part B = I + l is new (`HUNCH` on novelty) |
| Signed sum over pairs; involution cancels cyclic `Q_s` | Lemma 5.2 | No |
| Non-vanishing by positive spoke circulations, lowest-order coefficient | Sec. 5.2-5.3 | No. Li replaces it by a second involution, the constructive paper by an integer polynomial |
| Forest state to a tree on white faces (Temperley-type duality) | Sec. 6.1 | No in the Barnette literature. The incidence-tree idea is close to Feder-Subi's trees of faces (section 4 above) |

`HUNCH`. Measured by what the later expositions kept, the essential new idea is the cancellation. Li's note keeps it as two sign-reversing involutions, and the constructive paper keeps it as a signed polynomial plus a marked walk. All three need the disk identity to make the signs work. So my answer to "which idea was absent" is that the disk identity and the signed cancellation it powers were absent. Everything around them (the dual, the induced trees, H-, the separating-triangle gluing) was in place by 2005 or 2016.

`HUNCH`. Why might nobody have tried it? Through 2025 the Barnette community worked in structural and computational graph theory: reductions, colourings, generation, complexity. The tools the proof uses come from elsewhere: Tutte's trinity and Kauffman-style state models, double-dimer regrouping, Temperley's bijection, sign-reversing involutions. The Hacker News reactions, "complex roots and annihilating terms" (jboggan) and the cancellation as "quite novel" but with "precedents ... in loop-model physics" (thomasahle) [hn-2026], fit that reading. It is a guess about sociology, and I would not put it in a paper without better evidence.
