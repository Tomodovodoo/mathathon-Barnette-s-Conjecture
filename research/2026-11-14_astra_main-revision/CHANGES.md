# Version 2 change record

The starting manuscript was the 18-page main paper. Its unmodified TeX and PDF were copied to `paper/main/history/barnette-v1.tex` and `barnette-v1.pdf` before any edit, in commit `0881bf7`. The cold reader's trial applied cleanly: its base fingerprint matches the original after newline normalization. I used that trial, including its 59 replacements and seven block moves, then applied the mathematical referee's corrections and the further changes below.

Review item numbers below are those of the two supplied `EDITS.md` files. “Applied” includes small punctuation and citation-key changes. “Modified” means that the purpose was retained with a different implementation. All mathematical preservation conclusions in this record are PROVED-HERE in `AUDIT.md`; numerical confirmations are COMPUTED by `verify_final.py`, `example.py` and `independent/examples.py`. These are revision checks, not a new independent referee report.

## Mathematical referee

| Item | Decision | Result and reason |
| --- | --- | --- |
| E1 | Applied | Remark 4.10 calls the signed-height expression an integer Laurent polynomial, distinguishes the unsigned source's nonnegative weights, and expands at 1 using polynomial binomial coefficients for negative exponents. The negative exponents in the example confirm the need for the correction. |
| E2 | Applied | The multivariate polynomial is nonzero **when a pair exists**. Its leading-term explanation now says that the classes with the fewest cycles share a sign. Renamed it `Pi` to reserve `F` for a function on states. |
| E3 | Applied | The recovery remark assumes goodness before forming the tree, proves the converse by the root orientation, and proves injectivity. It no longer treats the state read from an arbitrary Hamiltonian cycle as automatically good. |
| E4 | Applied | Table 2 lists all eight pairs, not all twelve states. |
| E5 | Applied | The minimality statement explicitly concerns every face rooting of every Eulerian sphere triangulation with at most 12 vertices. This is the existing referee's exhaustive computation, not a new census performed by this revision. |
| E6 | Applied | Added the deletion-of-two-vertices proof of 3-connectivity for the 11-vertex radial graph of the triangular bipyramid. Renamed its equatorial vertices to avoid the roots' letters. |
| E7 | Applied | Added the deletion-of-one-vertex proof of 2-connectivity for the 26-vertex construction from three cubes. |
| E8 | Applied | The nonvanishing argument does not itself give an **efficient** construction. It no longer says that no constructive interpretation exists. |

## Cold reader

| Item | Decision | Result and reason |
| --- | --- | --- |
| 1 | Applied | Replaced the abstract with the proposed six-sentence abstract. The first sentence states the theorem; the rest identifies the connectivity problem, the dual selection, cancellation and induction. |
| 2 | Modified | Kept the five causal steps but shortened the trial's much longer plan so it fits on page 1. The disk identity and the reasons for the partner, weight and prescribed edge remain. Panels are referenced in the new order. |
| 3 | Applied | Shortened the history and deferred distinctions among proof methods. Historical originals not inspected by the project are credited through the sources that explain them. |
| 4 | Applied, checked | Moved the comparison of accounts to the closing section. The heights replace the circulation/spoke presentation; the finite difference of Lemma 4.7 replaces the exponential sum. Lemma 4.6 supplies additive positive increments but does not itself establish the nonzero moment. |
| 5 | Applied | The disk identity states the state, directed-cycle and counting hypotheses in its own statement. |
| 6 | Applied | Disk figure is after the five counts are introduced and before the disk identity and its proof. Its page also contains the full proof. |
| 7 | Modified | The recovery figure follows the complete proof of the tree-of-faces lemma. Its introductory reference is just before that lemma. This prevents an interruption and keeps the construction beside its proof. |
| 8 | Applied | Section 4 opens with its four steps. “Second state” consistently means `s`; the extra state is `r`. |
| 9 | Modified | Split the two local triangles. The state picture stays at the opposite-side definition; the pair picture follows the pair definition, with its caption beside it. Both use 9-point labels. |
| 10 | Applied | The reversal table follows the sign lemma, after all columns have a meaning. Removed the premature `F(s)` from that table. |
| 11 | Applied | Introduced fixed-second-state cancellation before its lemma. A weight depending only on `s` is constant under the involution; the heights subsection explains why a nonconstant weight is needed. |
| 12 | Applied | The height caption describes (a) as a clockwise starting pair and (b) as its reversal. |
| 13 | Modified | Added the exit-minus-entry explanation before Lemma 4.6; moved the source comparison to the closing section. The height figure now follows the complete proof, with its first reference there, because putting it before the proof left an excessive gap. |
| 14 | Applied | Added the eight-pairs figure. Its rows group by undirected `D`; a line joins the two shaded entries with the same second state. Shortened the caption and vertical spacing without shrinking the labels. The toolkit also exports it as `18-groupings`. |
| 15 | Applied | Explained why a tree is useful: leaf matching forces at most one perfect matching. Stated that goodness is sufficient, not necessary for an arbitrary Hamiltonian cycle's associated state. |
| 16 | Applied | Separated all corners in the state table and the cancellation example by centred dots. |
| 17 | Modified | Heading is “The selection has no cycle,” followed by the two incompatible disk counts that drive the proof. Dropped “recovered.” |
| 18 | Applied | Removed the apology for the letter `r` and the uninformative “used four times” sentence. |
| 19 | Applied | The small-cut argument explicitly uses sets of size one or two. |
| 20 | Applied | Replaced “pinched” by the fact actually needed: every face at a strictly interior vertex lies inside the cycle. |
| 21 | Applied | Moved the example figure to the end of its introduction and widened it to 0.62 text width. |
| 22 | Modified | Opposite-side figure stays after the complete example, fixed in place. |
| 23 | Modified | Pair figure is fixed immediately after the definition and cycle properties of `D`. One panel at 0.54 text width keeps labels at footnote size and fits with the following reversal lemma. |
| 24 | Applied | Cancellation figure follows the explanatory paragraph and precedes the heights subsection. |
| 25 | Applied | Eight-pair table precedes the complete numerical example. |
| 26 | Modified | Flow figure follows the network definition and cut inequality, at its first reference. It precedes the pair-existence proposition. This lets the reader identify its capacities and avoids splitting that proof. |
| 27 | Modified | Gluing figure follows the cap lemma and its complete proof, before the induction theorem. Its first reference moved with it. Putting it directly after the definition left roughly a third of a page empty; this position fills that gap while keeping the picture before the gluing argument. |
| 28 | Applied | Removed project tags and process statements. The closing section states proofs, finite enumeration ranges, literature assertions and open questions in ordinary mathematical prose. |
| 29 | Applied | Introduced `D(r,s)` as the object that supplies the second grouping of the count. |
| 30 | Modified | Rewrote the overview caption in words, with the new panel order and explanations of the ring and the suppressed black nodes. |
| 31 | Applied | Defined separating triangle again at its first substantive use in Section 5. |
| 32 | Applied | Explained the density inequality as a planar edge count, attained by coloured triangulations. |
| 33 | Applied / optional part declined | Added the reason for a lemma about arbitrary edge sets. Kept `M,N`: the general forest/cotree statement is clean and its two applications are explicit. Replacing every `M` with `T` would not improve the argument. |
| 34 | Applied, extended | Third root `c` became `o`; directed edges became `vec E`; `F` is only the weight function; a region is `Psi`; the polynomial is `Pi`. Also separated the outdegree vertex count `nu` from the density edge count `q`, finite-difference index set from disk count `I`, and source spoke weights from root `a`. Two accidental `Phi`/`Psi` substitutions were found and corrected during source comparison. |
| 35 | Applied as directed | Exact requested title, short running head, empty author command and exactly one author-decision comment. No production statement. |
| 36 | Applied | Rebuilt `01-cube` at full text width in two rows. Panels follow the plan; the dual panel overlays the cube in grey; captions use words; the root ring is explained. Explicit inter-row glue separates the first-row captions from the second-row labels. |
| 37 | Applied | Rebuilt `03-dual`: smaller, lighter grey primal edges and vertices; labels moved away from primal vertices. The final running-example label positions sit in white sectors rather than on state wedges. |
| 38 | Applied | Rebuilt `06-flow`: labels left of the squares, on top of incidence lines with white backing; one capacity label per kind; shaded source-side cut for `S={2}`; separated vertex 12. Final width is 0.74 text width. |
| 39 | Applied | Enlarged and labelled the inner gluing triangulation; replaced cancellation's two full disks by the affected three-face patch; reduced the pair diagram to one panel with 6-point arrowheads and a two-item legend. Moved running-example labels away from wedges. |
| 40 | Applied | Split connector-heavy proof sentences and separated the hypothesis examples into paragraphs. Recast the combinatorial parenthesis as a sentence. Reviewed every paragraph for the unslop rules; no em dash remains. Some semicolons that separate genuinely parallel counts or cases remain. |

Every displayed figure and table now uses fixed placement outside statements, proofs, examples and remarks. This is a further change from the trial's permissive float specifiers. It removes the three interruptions left in the trial. A new page can still divide a long proof or example normally; no figure or table intrudes into it.

## Further figure and notation work

The height path is now a polygonal route through its crossed-edge midpoints. It follows the same faces and makes the same two turns; the computation of the two displayed heights is unchanged. Existing figure filenames are stable. The new `18-groupings` export records the new diagram in the toolkit; the main paper keeps the corresponding inline TikZ so its text-width dimensions remain exact.

The outlined first-state wedge, solid second-state wedge, dashed opposite side, solid directed pair edge, dash-dotted face tree, and heavy selected side retain their meanings. Grey fills and shape/dash distinctions make the diagrams readable without colour. Integer labels remain approximately 8 points or larger at final scale; exact rendered sizes are in `verification.json`. Subscripts and superscripts use normal TeX math sizing.

## Bibliography and closing remarks

Copied `papers/barnette.bib` to `paper/main/refs.bib`, remapped the cited keys using the consolidation key map, and supplemented it with `georges1989` and `holton-mckay1988` from the previous standalone bibliography. The canonical file lacks those two entries; the main paper still cites them. The main paper continues to build with `refs.bib` beside it.

The standalone copy omits acquisition notes and project-process notes, changes the two arXiv-only records Hine2018 and Schnieders2025 to `misc` so their identifiers print, and shortens the OpenAI preprint's publication field to avoid a long repository URL in that entry. The separate formalisation reference retains the repository URL. The main bibliography has 17 cited entries. The canonical file itself was not edited.

The historical paragraph now distinguishes the 64-vertex and 90-vertex computer bounds. It attributes the older bound through Hertel, whose survey the project has read. Tait, Barnette's historical formulation, the four/six-face result and Tutte's trinity theory likewise use an explicit secondary account rather than implying inspection of unavailable originals. The questionable Barnette1969 entry is not cited. Source notes remain in the canonical bibliography and consolidation report, outside the paper.

The Pfaffian sentence follows the supplied GSW chain and identifies the universal equivalence and its two decomposition stages. The closing section mentions the accompanying Lean formalisation and the primal and involution companion notes without internal paths.

I omitted the optional lattice-extreme and irreducible counterexamples: stating them would require introducing the state lattice and a new notion of irreducibility in the closing paragraph. The referee report remains their proper record. I also omitted the unreviewed cycle-cover minimum result; it would need a separate definition and qualification and is not needed to explain the proof. These are scope decisions, not negative assessments of those results.

## Preservation and verification

Re-read every statement and proof against version 1 and the mathematical referee, including the unchanged duality, disk, sign, height, density and induction arguments. The substantive repairs are the eight referee corrections. No theorem hypothesis, induction prescription, reversal invariant, sign convention or printed example value was weakened. `AUDIT.md` records a fresh bounded reverse-Lamport pass by the reviser.

COMPUTED: `verify_final.py` reruns the manuscript example checks, the independent referee's example implementation copied into this folder, and the figure toolkit checks. It also checks environment nesting, fixed placement, labels, references, logs, author comment, em dashes and rendered font scale. `build.py` records the successful pdflatex/bibtex/pdflatex/pdflatex build. `latexmk` could not run because this MiKTeX installation lacks Perl; the direct sequence succeeds.

`before/` contains all 18 original page PNGs. `after-v2/` contains all 19 final page PNGs and contact sheets. Pagination changed throughout, so retaining every page is clearer than guessing a page-to-page alignment. All pages were visually inspected, including the first three, the disk proof, both count tables, the cancellation close-up, the network, and the gluing page. The final layout has no figure interruption or page with more than about a quarter of its text area left blank.
