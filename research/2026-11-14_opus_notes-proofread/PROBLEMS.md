# Problems found

## Mathematical problems

None found. I read both notes in full with the source alongside. I spot-checked the sign arithmetic that is easiest to get wrong:

- primal Section 6: the ratio $i^{n-4t/3}=i^n$;
- primal Lemma 8: $(h+3)/2$ negative signs and the prefactor $(-1)^{(n-c)/2}$;
- involutions Section 8: the factor $(-1)^m$ between its moment formula and the main paper's Proposition 4.8 (main paper $\Sigma=(-1)^{(n-m)/2}m!\sum\prod L$, with $H=-\omega$).

All three agree with paper/main/barnette.tex as it stands. Every main-paper statement number cited by the two notes matches paper/main/barnette.aux: Lemma 3.8 (disk identity), Lemma 4.2, Lemmas 4.5 to 4.7, Proposition 4.8, Proposition 5.2, Section 4 (heights and turns).

## Figure defects (not fixed: they need a redraw, which this task excludes)

1. primal.pdf, Figure 4, right panel: several flow labels touch arrow heads or vertices. A "1" sits on an arrow head left of the central haloed vertex, another "1" overlaps the arrow near the bottom right, and the "2" at the bottom touches the white vertex next to $b_0$. Left panel: the "1" next to the central white vertex touches the edge. The numbers are readable at 250 dpi, but tight.
2. primal.pdf, Figure 8, right panel: the label "cap" touches the cap vertex at the bottom.
3. involutions.pdf, Figure 1, right panel: the label $w_6$ sits on a blue cycle edge.
4. involutions.pdf, Figure 3: the face-path rows are drawn small, so the labels ($v=6,\ \kappa=+1$) are about 6pt on the page. Scaling would fix this, but the figure is generated code (figures/paths.tex) and I did not change its size.

## Build note (not a defect in the PDF)

proofs/primal/README.md says that research/2026-11-14_astra_primal-revision/build.py regenerates primal.tex from Markdown. Running it now would overwrite every edit in this proofread. Either the Markdown source (PRIMAL-PROOF.md) is brought in line with primal.tex, or primal.tex should be treated as the source from now on. PRIMAL-PROOF.md is outside my scope, so I did not change it.
