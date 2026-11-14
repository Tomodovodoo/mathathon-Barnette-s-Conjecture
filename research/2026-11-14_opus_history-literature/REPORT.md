# Report: history and literature of Barnette's conjecture

**Summary.**

1. I built a checked literature base: 74 BibTeX entries (DOIs resolved through Crossref, arXiv ids through the arXiv API), 24 open PDFs, a results table, a narrative history and a list of 14 equivalent formulations.
2. The OpenAI proof reuses three old pieces: the dual two-induced-trees form (Stein 1971, APSW 2016), the edge-avoidance strengthening H- (Kelmans 1986, Hertel 2005) and Kelmans' reduction to triangulations without separating triangles. The new part is the disk identity and the signed cancellation over pairs of Tutte states. None of the 23 Barnette papers I collected uses anything like it.
3. As of 14 November 2026 the proof is unrefereed. There is an exposition on arXiv (Zhentao Li, arXiv:2610.30490), an unsigned "constructive proof" with no public source, and a Lean formalisation in OpenAI's repository. A third-party audit reports that two Lean kernels accept it (cert-machine, 10 October 2026). I did not rebuild it.
4. Two corrections to the brief or to the literature. "Takanori" is not a separate source: it is Akiyama-Nishizeki-Saito 1980 cited by the authors' given names. Hertel's survey misstates the Jensen-Toft colouring equivalence; it is about the dual, not the Barnette graph.
5. Why it was hard (`HUNCH`, argued in WHAT-WAS-HARD.md): local reductions cannot see 3-connectivity, and Schnieders' connected counterexample shows that 3-connectivity becomes necessary at face size 10. Arbitrary prescribed edges are NP-hard. The translations to other theories gave no existence mechanism.

## What I set out to do

The brief (my folder `research/2026-11-14_opus_history-literature/`) asked for an extensive literature review covering origins, partial results, equivalent forms, failed proofs, neighbouring conjectures and the 2026 events. The deliverables are HISTORY.md, RESULTS-TABLE.md, EQUIVALENTS.md, bibliography.bib, pdf/ with INDEX.md, WHAT-WAS-HARD.md and this report. All seven are in the folder.

## What I established

All `LIT` unless tagged. The details and citations are in the deliverables.

- **Computer verification.** Holton-Manvel-McKay 1985 reached 64 vertices. Aldred-Brinkmann-McKay announced 84 in 2000. Brinkmann-Goedgebeur-McKay (Math. Comp. 2022) reached 90, with every edge on a Hamiltonian cycle up to 78 vertices and H+- for all edge pairs up to 66. Wikipedia says "fewer than 86 vertices", which is the 84-vertex bound and is out of date.
- **Face-size results.** Goodey 1975 did faces 4 and 6. Feder-Subi 2006 did two colour classes with 4 and 6. Bagheri Gh.-Feder-Fleischner-Subi 2021 did leapfrogs of cyclically 4-edge-connected graphs. Florek 2025 did at most four big neighbours per face. Schnieders 2025 did faces at most 8, without needing 3-connectivity, using 339 million computer cases; this is sharp for connected graphs, with a non-Hamiltonian example at face size 10.
- **Kardoš 2020** proved the other Barnette conjecture (Barnette-Goodey, faces at most 6, not bipartite), with computer assistance.
- **Equivalent forms.** EQUIVALENTS.md has 14 of them, each with source and proof idea. The OpenAI paper touches the dual (2), Stein/APSW (3, 4), Kelmans' separating-triangle reduction (8, re-proved without citation), H- (9, proved as Corollary 7.1 and built into Theorem 2.2) and GSW (11, used for Corollary 7.2).
- **Unconditional hardness of prescribed edges.** Hamiltonicity through an arbitrary prescribed edge set is NP-complete for Barnette graphs (Bagheri Gh. et al. 2022, proof of Thm 4.6). This explains why the induction hypothesis must prescribe only something bounded.
- **Claimed proofs that failed or were never accepted.** Cahit 2009 (arXiv draft), Clarke 2013 (withdrawn on arXiv, April 2014), Shah 2014 (Int. J. Math. Combin.). I did not audit them.
- **2026 events I could document.** The OpenAI repository went public on 6 October. Gil Kalai's blog (7 October) and the Hacker News thread followed. The cert-machine kernel replay ran on 10 October, and formal-conjectures issue #7144 and PR #7149 opened on 11 October (the PR is still open, with maintainers asking what evidence counts). The unsigned constructive manuscript is dated 18 October, Li's arXiv note 21 October, and Hongmin Li's Zenodo preprint (25 October to 6 November) uses the result. I found no refereed publication, no correction specific to family 180, no press coverage, and no Wikipedia or Open Problem Garden update.
- **Our copy of the paper.** `COMPUTED`: `papers/OpenAI-Barnette.pdf` is byte-identical to the repository copy downloaded 14 November 2026. I checked with `cmp` against a curl download of `preprints/Paired-states-.../paper.pdf`.
- **The Lean files.** `COMPUTED`: the 31 Lean files of `lean/OAI/Combinatorics/Hamiltonian/` total 8,936 lines and import only Mathlib. `grep -n "sorry\|^axiom\|admit"` finds nothing. I ran this on a scratchpad download; the files are not in the repository. The comparator config permits only `propext`, `Quot.sound`, `Classical.choice`. I did not build the files.
- **Grinberg.** `PROVED-HERE` (WHAT-WAS-HARD.md section 2): in a Barnette graph f_4 = 6 + sum_{k≥8} (k/2 - 3) f_k. So there are at least six faces of Grinberg weight 2, and the classical "all weights but one divisible by m" argument is impossible.

## What failed and why

- **Paywalled or offline originals.** I did not read Tutte 1946, Goodey 1975/1977, Holton-Manvel-McKay 1985, Kelmans 1986/1994, Florek 2010, Lu 2011, Fleischner's book, Grünbaum-Walther 1973, Akiyama-Nishizeki-Saito 1980 or the Waterloo proceedings page. Their content is cited through secondary sources that I did read, and the verified column says which one. Grünbaum-Walther is metadata only. I still do not know which "Grünbaum-Walther" statement the brief had in mind, beyond their 1973 shortness-exponent paper.
- **Feder-Subi.** The ECCC PDF uses Type 3 fonts and `pdftotext` produces garbage. I used the ECCC abstract and its later published versions (Bagheri Gh. et al.).
- **lance.fortnow.com** did not resolve (DNS failure, twice). I could not read "OpenAI Math: TCS Selection".
- **The constructive paper.** No search found a public source or author for "A constructive proof of Barnette's conjecture". Its PDF metadata has no author field.
- **The Kelmans 2003 RUTCOR report**, which APSW cite for the (4)⇒(1) direction, was not found.
- **Holton-Manvel-McKay's lifting theorem.** I did not verify the mechanism (their Theorem 5) that turns a stronger computed property into Hamiltonicity at larger orders. It is described only in the paywalled paper.

## What is still open

- Whether the OpenAI proof is correct as written. That is for the dependency and route agents. On the literature side, the third-party Lean replay is the strongest evidence I found, and I did not reproduce it.
- Global H+- (any ordered pair of edges) for Barnette graphs. It is not implied, and Hongmin Li's preprint says the same.
- GSW Question 6.1 (is every planar brace Hamiltonian?), and the Bekos et al. question whether graphs built by C4-expansions alone are Hamiltonian. Both are answered yes by the OpenAI theorem (planar cubic braces are Barnette graphs, and C4-expansions of the cube stay Barnette), but Question 6.1 asks about all planar braces, not only cubic ones, and that stays open.
- The `CONJECTURE` in WHAT-WAS-HARD.md section 4: Bagheri Gh. et al.'s parity "invariant property" on separating triangles of `G/Q` and the constructive paper's "black inner boundary" obstruction may be the same condition. The test is stated there.

## Three best next steps

1. **Rebuild the Lean proof locally**, or at least re-run the Comparator challenge, and read `ExactDual.lean`, `Gluing.lean` and `StateDisk.lean` against Sections 2, 4 and 7 of the paper. The file names suggest that much of the formal effort goes into planarity-to-duality (lattice corridors, minors). That part is invisible in the paper and may be the most reusable piece for our exposition. This belongs to the route-constructive agent.
2. **Write a two-page "pre-history" for the paper (`paper/`)** from HISTORY.md sections 3 to 6. It should show the reader that the dual trees, H- and the separating-triangle reduction were all known, so the disk identity and the cancellation arrive as the one new idea. EQUIVALENTS.md entry 9 and WHAT-WAS-HARD.md section 9 give the exact citations.
3. **Run the test in WHAT-WAS-HARD.md section 4** on plantri-generated Eulerian triangulations with separating triangles, comparing the Feder-Subi/Bagheri tree-of-faces framework with the incidence-tree criterion. If the two obstructions coincide, the OpenAI incidence tree is a direct descendant of the 2006 Feder-Subi idea, and the history gets a cleaner line.

## Leads for others

- **Route-graph-theory agent.** Feder-Subi and Bagheri Gh. et al. decide spanning trees of faces with 2- and 3-sided faces through the spanning tree parity problem, which is polynomial. The OpenAI incidence tree asks for a spanning tree of the spoke graph `H` with each black centre keeping exactly two of its three spokes. That looks like a parity or matroid-parity instance and might give a polynomial algorithm, against the 3^(N/4) of the constructive paper. `HUNCH`, untested.
- **Sol machinery agent.** Gorsky-Steiner-Wiederrecht use Pfaffians only as a graph class. The OpenAI sign i^J on pairs of matchings may be a Kasteleyn-type sign, and the constructive paper's determinant bound hints at a determinant formula. Worth checking whether Z(x) is a Pfaffian or determinant. `HUNCH`.
- **Dependency-graph agent.** The OpenAI paper re-proves Kelmans' separating-triangle gluing without citing it (Section 7 against APSW Theorem 8, (4)⇒(1)). This is a candidate node for "known lemma, cite instead of prove".
- **Everyone.** Theorem numbers in GSW differ between arXiv versions. The OpenAI paper uses v3 (15 August 2022), and so does my PDF.

## Files

- `HISTORY.md`: narrative, 1884 to November 2026, with timeline.
- `RESULTS-TABLE.md`: one row per result, with verification status.
- `EQUIVALENTS.md`: 14 equivalent forms with sources, proof ideas and OpenAI usage.
- `WHAT-WAS-HARD.md`: why the conjecture resisted, and which idea was new.
- `bibliography.bib`: 74 entries, each with a note on how far it was checked.
- `pdf/INDEX.md` and 24 PDFs.

Commands behind the `COMPUTED` claims: `cmp` of the paper PDF; `grep -n "sorry\|^axiom\|admit" *.lean` and `wc -l *.lean` on the downloaded Lean directory; `pdftotext -layout` followed by `grep -l -i <term>` over the PDF corpus (WHAT-WAS-HARD.md section 9). All were run from the scratchpad on downloaded copies.
