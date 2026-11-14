# Expository choices for draft A

Editorial judgments in this document are HUNCH prescriptions tested against the rendered draft. Mathematical statements carry protocol tags. The paper deliberately contains no status tags.

## Main route and attribution

1. HUNCH. Start with degree two and connectivity, then ask for a forest of omitted dual edges. This gives the reader a reason to leave the primal graph before introducing states.
2. LIT. The theorem includes avoiding any prescribed edge, OpenAI Corollary 7.1. Keep the arbitrary facial-edge version of its Theorem 2.2 as the induction contract. A Hamiltonian existence statement alone would not supply compatible gluing data.
3. HUNCH. Retain two induced trees even though the irreducible construction can go straight to a cycle. They make agreement across a separating triangle explicit and keep the gluing proof short.
4. LIT. Retain OpenAI Proposition 3.1's density proof. It proves exactly the no-separator case needed here. Reject the stronger exact black-inner-boundary criterion as unnecessary scope, not as a false statement.
5. PROVED-HERE. Use the height-product nonvanishing argument from the Fable note, Sections 1--3. It is written in full in Section 4 of the manuscript and checked at C9--C12 in AUDIT.md. Adopt the note's W=B+1 disk formulation and boundary-pairing proof of the selected forest.
6. PROVED-HERE. Keep the minimum cycle count m. The height product has m labelled factors; the alternating expansion kills groups with more cycles and gives one common sign on the minimum groups. No extremal choice of a preferred state is asserted.
7. HUNCH. Omit the complex phase, exponential, positive circulation construction, Taylor expansion and token bookkeeping. This is a change of test function inside OpenAI's mechanism, not an independent discovery. Bibliography entries distinguish the original, Li, the unsigned constructive manuscript and the unpublished Fable note.
8. HUNCH. Omit determinants and all algorithmic material. The incidence determinant is an alternative explanation of cancellation, but supplies no simpler nonvanishing proof here. Adding its vertex coloring and gauge would interrupt the existence route.
9. PROVED-HERE. Do not omit the spoke deformation. The height difference still needs its curve to have the original orientation and enclose the same white faces. The proof checks the sector excluding the third corner, including when that corner is elsewhere on the cycle.
10. PROVED-HERE. Define heights for all white faces, rather than first defining the smaller inner-face set. The increment calculation applies to each face. Witness faces exist because W=B+1. Fixed paths give finite signed integers; no nonnegativity or path independence is used.
11. HUNCH. Use n, A, X, R, B, H, Q_s, D and W_s consistently with the shared brief. Local disk face counts B,W are explicitly distinguished from incidence graph B. The larger example uses a_j for the figure's numerical face IDs, avoiding a collision with the distinguished face t_0.

## Referee integration

PROVED-HERE. Read research/2026-11-14_astra_referee-combinatorics/REFEREE.md and REWRITTEN-PROP-5-1.md before finalization. The main height proof was found correct there. The relevant repairs are included: pair existence precedes m, witness positions can repeat, paths are fixed and signed, the deformation is proved, and P_0 acyclicity is followed by the root-component argument before adding e_0. No volume identity, determinant normalization, reflection-sensitive minimal counterexample, or sweeping impossibility claim from the auxiliary research is used.

HUNCH. No fallback to the exponential argument was needed. The height proof survived the independent checking recorded in AUDIT.md and the available referee's corrections.

## Examples and figures

COMPUTED. examples.py recomputes the supplied cube and truncated-octahedron JSON examples through the reference implementation, translating face IDs by corner sets. It also independently reconstructs the current figure octahedron and 13-vertex triangulation, checks recovered cycles, verifies the Q involution and signs, counts the displayed disk and verifies the nested four-term identity. Exact outputs and the finite range are in examples.json. Command from repository root:

```
python research/2026-11-14_astra_manuscript-A/examples.py
```

HUNCH. Use the cube for the whole sequence from local choices to the final cycle, but do not pretend it has a cyclic partnered Q. The larger revised figure example has nested D cycles and minimum count two, so it illustrates the general product-of-heights argument. The truncated octahedron was checked but is not printed, since the shared 13-vertex example serves this purpose with fewer labels.

HUNCH. Reference shared PDFs by filename so revisions propagate. Do not edit or rebuild paper/figures. Write only the signed-intersection schematic locally. Caption the shared disk figure in terms of W=B+1, and the cyclic-Q figure with its actual triangle 1,8,9. The initial shared captions still included an obsolete cycle-length-six sentence and exponential language; the manuscript supplies its own captions rather than reproducing them.

HUNCH. Use 10pt amsart on A4 with one-inch margins. This keeps the shared figures at readable natural scale, with text labels at least the document's 8pt footnote size, apart from mathematical subscripts. Widths are fractions of textwidth. A one-point horizontal trim removes only part of the standalone border. The first 11pt build made some shared labels smaller than the footnote font and was replaced.

HUNCH. Use flafter to prevent figures preceding their definitions, and needspace before lemma/proposition statements to keep them with the start of the proof. The final paper has six sections, thirteen numbered equations and eight figures. No algorithmic appendix is needed.

## Prose pass and preservation

HUNCH. Applied the unslop pass after the backward audit. Cut an unnecessary contrast about independent discovery, replaced a vague claim that the height product localizes the mechanism with its actual action on one face per factor, and replaced an unused-theorems disclaimer by the positive promise to prove the state properties. Added source citations at the density, disk and recovery arguments. These edits change no quantifier, hypothesis or mathematical inference.

COMPUTED. build.py runs pdflatex, BibTeX and three settling passes, rejects undefined references and overfull boxes, then renders every page with PyMuPDF at scale 1.5. build-check.json records all source and shared-figure hashes. The first layout had floats above their explanation and a lemma separated from its proof; the final layout was inspected page by page after repairing those issues.

```
python research/2026-11-14_astra_manuscript-A/build.py
```

The paper also builds directly by running pdflatex, bibtex, pdflatex, pdflatex from paper/draft-A. No network lookup or dependency install is needed for the delivered build.
