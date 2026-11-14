# Report: second audit and final edit of digestions/steps

1. Steps 01 to 08 and the glossary now follow the refereed paper: good state through $S_s$ (Lemma 3.5), recovery through the tree of faces $Y_s$ (Lemma 3.6), heights along paths of faces, finite differences and $F = \omega^m$ (Lemmas 4.6, 4.7, Proposition 4.8), the real sign as a product of local signs.
2. Every number in the worked examples on the cube, the hexagonal prism, the running example, the double octahedron and the 16-vertex example was recomputed by an independent script on the paper's orientation model, cross-checked against `workings/barnette_lab` (COMPUTED). All agree with the paper's Table 2 and examples.
3. Errors found and fixed: the glossary's $\varepsilon = i^n i^{-J}$ (should be $i^{n+J}$); the glossary's "chosen sides" as a synonym of the selection; a wrongly oriented triangle in step 04's example; step 04's claim that the exact value 3 is used once.
4. "What does not work" and "Other routes" now carry the final results with plain-word review status: lattice extremes (18, and 10 for the state lattice), extremes or irreducibles (33), one cover with no good state (16), direct lifting (18), matroid and LP shortcuts, packing, Step R proved and Step X open, C1 and C3 open with bounded descent dead, Lean status.
5. Every step links the paper section, the primal note lemma, the blueprint node and the atlas page; all 199 links and paths in `digestions/steps/` resolve. Problems in 00 and 09 are listed for their owner.

## What I set out to do

The brief: read 01 to 08 and the glossary as the intended reader; check them line by line against `paper/main/barnette.tex`; recompute every example; update the negative results and other routes; add pictures and cross-links; unslop; complete the glossary. Deliverables: the edited files, `AUDIT.md`, a problem list for 00 and 09, the recomputation script and output, a link check, this report.

## What I established

- `COMPUTED` (`code/recompute.py`, output `outputs/recompute.txt`, `outputs/recompute.json`). On the running example: 12 states, 8 pairs, 7 partnered, 6 good; $\alpha$, $\beta$, $\tilde\beta$ as in the paper; $D(\beta,\alpha)$ = counterclockwise 7-cycle with $h = 7$, $\ell = 2$, $I = 3$, $B = 5$, $W = 6$ and clockwise triangle $8,7,12$; the eight pairs with the paper's $\varepsilon$ and $\omega$; $\Sigma = 18$; the Laurent polynomial; $9x^2 + 5x^3$; heights-product sums 1 and 2; the Figure 10 height values; $P_\beta$ and the Hamiltonian face order; 112 two-factors and 28 Hamiltonian cycles, 6 avoiding the edge across $e_0$; tight set $\{2\}$. The disk identity, $\delta$-sum convention, $\varepsilon = (-1)^{(n+c)/2}(-1)^{c^+} = (-1)^{(n+J)/2}$ and $J = $ #cw $-$ #ccw asserted on every pair and cycle of all examples. Cube, prism (all three $e_0$), double octahedron (14 roots) and the 16-vertex class-158 example as listed in `AUDIT.md`.
- The sign conventions of steps 01 to 08 agree with the paper. The involution note's $H(s) = -\omega(s)$ is the one opposite convention, stated where used.
- Link check (`code/linkcheck.py`, `outputs/linkcheck.txt`): every Markdown link and every backticked repository path in `digestions/steps/*.md` resolves.
- Fresh PNG renders of four paper figures whose committed renders were older than their PDFs (`code/render.py`, into `digestions/steps/img/`).

## What failed or was not done

- Length: 03 (about 3,600 words) and 06 (about 3,500 with tables) exceed five pages. I kept the full proof of the sharp pair criterion in 03 and the worked example tables in 06.
- Not recomputed, quoted with source: Li's marked-object counts, the subdivided-octahedron counts, census totals (1,794, 5,088, 7,868 rooted triangulations), the extremal-choice failures, the gluing example (checked earlier by `fable_digestions/crosscheck.py`).
- The Lean column of the glossary comes from the primal dictionary and the blueprint, not from the Lean source.
- The atlas was renumbered by another agent during this run (commit `cf39b69`). My links follow the new numbering; the atlas README index was still on the old numbering when I looked.
- The brief named `paper/figures/example.json`; the file is `paper/figures/running.json`.

## What is still open

Nothing mathematical was opened or closed here. The open problems are those of 09 and the route map; the digestions now point to them by door number.

## Three best next steps

1. The owner of 00 and 09 should apply `PROBLEMS-00-09.md`, in particular the two different "strict descents" and the two different lattices in 09, and the spoke-based sentence 9 of 00.
2. Shorten 03 and 06 to five pages by moving the Euler identity proof (03) and the "other dress" table (06) into an appendix file, if the five-page rule matters more than self-containedness.
3. A human reader should check the glossary's Lean column against the Lean source and step 06 against the paper's Section 4; these are where a reader moving between the formal proof and the exposition will look first.

## Leads for others

- `barnette_lab.core.Instance.polynomial` uses an embedding whose orientation may be the mirror of `paper/figures/` and spoke weights shifted per face, so its exponents can differ from the paper's $\omega$ by reflection and a constant. Anyone quoting the lab's polynomial next to the paper's should say so or convert.
- The atlas README index lags the renumbered pages.
