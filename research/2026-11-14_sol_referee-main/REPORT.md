# Review of the merged Barnette manuscript

1. PROVED-HERE: the supplied route establishes Theorem 1.1; the reverse-Lamport verdict is FOLLOWS.
2. PROVED-HERE: the new disk paragraph is sufficient, and the signs, height jumps, nonvanishing and prescribed-side gluing are correct.
3. REFUTED: Remark 4.10's expression is an ordinary integer polynomial with the stated heights; it is Laurent. This is off the theorem route.
4. COMPUTED: every printed finite example agrees; all 15 Eulerian triangulations through 12 vertices were checked at all 262 face roots.
5. Eight unique old/new replacements are supplied; no paper/ file was edited. Every numbered external theorem citation was checked in a held original.

## What I set out to do

Act as an independent referee of paper/main/barnette.pdf and its source, using the manuscript alone as the proof under audit. I read every rendered page before opening the source or comparison material, wrote SUMMARY-FROM-MEMORY.md, and committed that record first. I then checked the supplied route backward, compared it with the named source papers and research notes, and wrote independent enumeration code. I did not delegate.

## What I established

PROVED-HERE. REFEREE.md gives the boundary, a conclusion-first AND obligation graph, ranked findings, the detailed mathematical verification, a complete dependency table and the verdict last. In particular the disk-face identification is made before connectivity is used, so the new repair is not circular. Both halves of the state bijection, the two different reversals, the exact product-sign formula, path endpoints, positive white-face weights, class size, minimum-cycle sign alignment, all flow cut terms and the smaller-input induction were checked.

COMPUTED. code/check.py checks all generated face rootings through 12 vertices and the named examples. The combined run covers 707,952 arbitrary chosen-side systems and 239,180 directed chosen cycles. No core identity fails. code/examples.py verifies every Table 2 entry, every printed named state and cycle, the cube and prism, the height figure and the exact gluing selections, as well as the two auxiliary hypothesis examples. code/supplement.py directly checks max-flow, the S_s equivalence and generic evaluations of the multivariate polynomial identity at all 262 roots, and checks the finite-difference formula on 560 exact integer instances. Commands, ranges, outputs and generator provenance are in code/README.md.

PROVED-HERE. Eight exact replacements are in EDITS.md. Its generator asserts that each old string occurs once in the audited TeX. They correct the Laurent terminology and source-weight mismatch, explicitly scope two conditional remarks, add the two missing structural checks, give a computation range, qualify a construction claim, and correct the claim that Table 2 lists all states.

LIT. SOURCES.md records the numbered citations. The held OpenAI, Gorsky-Steiner-Wiederrecht, Hertel, Alt-Payne-Schmidt-Wood and unsigned-source theorem numbers and statements agree. Li's cited sections and appendix support the attributions. The comparison notes' adopted simplifications are correctly represented, except for the unsigned source's normalization of weights noted above.

## What failed and why

REFUTED. The ordinary-polynomial assertion fails on the running example itself: after cancellation it has nonzero terms z^-4, -z^-3, z^-2 and -z^-1. The manuscript's power-moment proof never uses that assertion. Its expansion at z=1 is valid with generalized binomial coefficients.

PROVED-HERE. The first perfect-matching sentence in Section 7 needs the hypothesis that the recovered state is good before calling its face graph a tree. Its intended implication and the converse are valid. The unconditional shorthand F!=0 also needs the pair-existence hypothesis. A saved 9-vertex root with flow value 11 instead of 12 exhibits why that scope matters.

The first citation inventory was too narrow: papers/INDEX.md says Hertel and Alt et al. are not held in papers/, but a final repository-wide search found their PDFs in the history-literature research folder. I corrected the ledger after opening and rendering their original statements. All numbered external theorem citations are checked. The same folder supplied the original Brinkmann-Goedgebeur-McKay 50-vertex minimum and 90-vertex range and Schnieders' face-size-eight result. Some older unnumbered historical citations remain checked only through secondary sources, as SOURCES.md records.

## What is still open

The manuscript's main mathematical route has no unresolved obligation within the stated audit boundary. Some older historical originals and the source's enumeration complexity proof remain outside what I independently verified. The finite census is corroboration, not a proof for larger orders. No polynomial-time construction was established by this review.

## Three best next steps

1. Apply the eight proposed replacements, then rebuild the PDF and check the longer Section 7 examples for pagination.
2. Reconcile the history-folder PDF holdings with papers/INDEX.md, pin the Gorsky PDF version in the bibliography, and obtain the older historical originals still checked only through secondary sources.
3. Have a human referee check the discharged disk, height and gluing obligations in REFEREE.md against the paper. The reports and independent scripts identify the precise statements to inspect.

## Leads for others

PROVED-HERE. The elementary face-restriction argument succeeds because this manuscript defines the inside geometrically. An exposition using an algebraic bond must still prove both connected shores and the vertex-link condition. The Lean comparison is a useful checklist, but its longer proof should not be imported as an extra unproved premise here.

All authored files, generated pages and check outputs are confined to research/2026-11-14_sol_referee-main/. Commits contain only that path. Git delivery status is recorded in the final chat response.
