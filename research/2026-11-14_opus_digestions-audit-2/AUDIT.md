# Second audit of digestions/steps, document by document

Scope: `digestions/steps/01` to `08` and `GLOSSARY.md`, read against `paper/main/barnette.tex` (version 2, refereed FOLLOWS), `proofs/primal/`, `proofs/blueprint/BLUEPRINT.md`, the atlas, `digestions/steps/09` and `research/INDEX.md`. Numbers were recomputed with `code/recompute.py` (output in `outputs/recompute.txt` and `outputs/recompute.json`); links with `code/linkcheck.py` (`outputs/linkcheck.txt`, all resolve). The brief named `paper/figures/example.json`; that file does not exist, the running example is `paper/figures/running.json`.

How the recomputation works. Orientation-dependent quantities ($\delta$, clockwise, $J$, $\varepsilon$, heights) use `paper/figures/model.py`, which stores faces in the paper's counterclockwise order, so they follow the paper's sign conventions. States, pairs and good states are recomputed a second time with `workings/barnette_lab` (its own embedding) and compared; they agree on all six examples. Heights are implemented in the script from the paper's definition (shortest face paths, ties to the smallest face index), independently of the code that produced the paper's Table 2. COMPUTED on the cube, the hexagonal prism (three choices of $e_0$), the running example, the double octahedron (all 14 roots) and the 16-vertex class-158 example. Everything below marked "recomputed" passed an assertion or matches the printed output.

Convention check. The paper: $\delta(v,w) = +1$ when the black face of $vw$ is on the left of $v \to w$; counterclockwise state cycles have $\delta$-sum $-3$; $\varepsilon = \prod \delta(r(t),s(t)) = (-1)^{(n+c)/2}(-1)^{c^+}$; $J = \tfrac13\sum\delta = $ #cw $-$ #ccw; reversing a cycle from clockwise to counterclockwise raises $\omega$ by $L(C)$; OpenAI's phase is $i^J = i^{-n}\varepsilon$. The digestions now agree everywhere. The one source with the opposite sign is the involution note, whose $H(s)$ is $-\omega(s)$; 06 and the glossary say so. The lab's own polynomial (`barnette_lab.core.polynomial`) uses an embedding that may be the mirror image and spoke weights shifted per face, so its exponents can differ by reflection and a constant; 06 no longer quotes it.

## 01. Degree two and connectivity

Findings. Correct, and not worse than the paper's introduction. The hypothesis list lacked the smallest sizes the paper now gives (38 vertices for non-bipartite, Georges-Kelmans 50 for non-planar) and described the 26-vertex example only through an abstract. The Kasteleyn sentence said 2-factors of planar graphs are counted by a Pfaffian, which is true only through perfect matchings in a cubic graph. No status line about the theorem itself.

Recomputed. Cube: 9 perfect matchings, 6 Hamiltonian, the three omitted matchings and their 4-cycles as listed. Prism 20 two-factors (8, 10, 2 by cycle count). Running example 112 (28, 52, 27, 4, 1).

Fixes. Cross-link header (paper, primal Theorem T and Lemma 12, blueprint `thm:main`, `prop:target.1`, atlas pages 1, 27, 29). Hypothesis bullets updated with the paper's sizes and the paper's construction of the 26-vertex graph. Kasteleyn sentence corrected. Added a status bullet for the theorem.

## 02. Dual and two trees

Findings. Euler's formula was used without saying why the graph is connected; the paper's Lemma 2.2 is missing. The tree/cotree proof used contraction only; the paper's boundary-edge proof is shorter and covers any acyclic set. The "converse" paragraph was correct but did not name paper Lemma 2.5(1). Nothing said that Proposition 2.6(2), the two-trees statement, is the one statement here with no Lean counterpart. The octahedron example is right; it shows the partition $\{0,1,3\}$/$\{2,4,5\}$ while the paper's Figure 1 shows the other good state's $\{0,1,4\}$/$\{2,3,5\}$, which a reader comparing the two would trip on.

Recomputed. Octahedron counts, $P = \{01,13,24,45\}$, the cycle $0,3,6,1,4,7,5,2$; the other good state gives $\{0,1,4\}$/$\{2,3,5\}$.

Fixes. Header; Lemma 2.2 paragraph; the paper's proof of Lemma 2.5(2) and the Jordan-curve proof of 2.5(1); Proposition 2.6 paragraph with the Lean gap; paper numbers on every statement; primal note in "Other routes"; the second partition named.

## 03. States and pairs

Findings. Good states were defined through the spoke graph $H$, which the paper no longer uses; the paper's $S_s$ and Lemma 3.5 were missing. The review-status line pointed at a "provisional work log". The derivation of states from selections was attributed only to research folders although it is now the paper's Lemma 3.1. The flow argument is fine; the paper's per-component density argument was not compared. "What does not work" and "Other routes" predated the lattice, matroid, LP, packing and rainbow results.

Recomputed. Octahedron states and $Q$; prism: 3 states, 2 pairs, 2 good, the third state with forest $Q$ components $\{0,1,7\}$, $\{2,5,6\}$, $\{3,4\}$ and no partner; double octahedron: 8 roots with (4 states, 4 pairs, 4 good), 6 with (4, 0, 0), and $S = \{6,7,8\}$ supplied 5 of 6 incidences; running example 12 states, 8 pairs, 7 partnered, 6 good; tight set $S = \{2\}$ in (5.1). Not recomputed: the 34 of 54 states of the subdivided octahedron, the 7,868 rooted-triangulation flow check (both attributed).

Fixes. Header and current status; definition of good state switched to the paper's, with $S_s$, and the spoke form kept as a remark; Lemma 1 and Theorem 2 with paper numbers; a paragraph comparing the paper's Proposition 5.2 with the sharp Euler identity; image re-rendered from the current PDF (`img/paper-05-state.png`; the committed render predated the PDF); "What does not work" gained lattice extremes (18) and extremes-or-irreducibles (33, with separators), two matroids (prism) and the LP (13), and packing true but blind to pairs (16, 17); "Other routes" gained Step R (proved, unreviewed) with Step X open.

Length. 3,600 words, over the five-page target. The worked examples and the Euler identity proof are the bulk; I left them because they are the only full proof of the sharp criterion in the digestions.

## 04. Disk identity

Findings. One error: for the paper's pair $(\beta,\alpha)$ the triangle is $8 \to 7 \to 12$, clockwise; the digestion wrote $8 \to 12 \to 7$. The pair was not named, so the reader could not match it to the paper's Figure 6. The connectivity of the disk was waved through as "the Jordan curve theorem"; the paper needs Lemma 2.2 for Euler's formula and says so. The "odd buys / three buys" table said the exact value is used once; in the paper it is used twice (the sign formula of Lemma 4.4 and the recovery count of Proposition 3.9). The outdegree lemma (paper 3.7) was absent.

Recomputed. All five numbers of the 7-cycle ($h = 7$, $\ell = 2$, $I = 3$ at $7, 8, 12$, $B = 5$, $W = 6$, $\delta$-sum $-3$, 20 edges); the triangle ($\delta$-sum $+3$); the other cover's 7-cycle $1,7,12,8,10,11,6$ ($\ell = 2$, $I = 0$, $B = 2$, $W = 3$); octahedron cycle $3,4,5$ counterclockwise with $\delta$-sum $-3$. The identity and the sign convention were asserted on all 18 directed cycles of $D$ and $Q$ in the running example.

Fixes. Header; paper numbers; outdegree paragraph; the connectivity of $R_C$ through Lemma 2.2; example renamed to $(\beta,\alpha)$ with the direction corrected and the correction stated; usage table rewritten to match the paper; primal Lemma 5 in "Other routes".

## 05. Cancellation

Findings. Correct mathematics. It used private names $s^*, r, r'$ and face indices where the paper has $\alpha, \beta, \tilde\beta$ and corner names. The product sign was presented as a project write-up "with no second reader"; it is now the paper's Lemma 4.4 and refereed. The phase relation and the settled phase dispute were missing. A dated remark about the lab's test suite.

Recomputed. $\alpha$, $\beta$, $\tilde\beta$; the three changed faces; $\varepsilon(\beta,\alpha) = -1$, $J = 0$; $\varepsilon(\tilde\beta,\alpha) = +1$, $J = -2$; both covers. The sign formula $\varepsilon = (-1)^{(n+c)/2}(-1)^{c^+} = (-1)^{(n+J)/2}$ and $J = $ #cw $-$ #ccw asserted on every pair of all examples.

Fixes. Header (with the Lean status of Lemmas 4.3 and 4.4); the sign paragraph rewritten around the paper's Lemma 4.4 with $i^J = i^{-n}\varepsilon$; names switched to the paper's; the flip for $D$-reversal added; the Heawood torus example (cancellation without nonvanishing) added to "What does not work". I removed a claim I had first written that the running example is "the smallest" of its kind; nothing establishes it.

## 06. Nonvanishing

Findings. The document was built on spoke-crossing heights, five parallel proofs and a 4,300-word length. The paper's argument (face-path heights, Lemma 4.6, finite differences Lemma 4.7, $F = \omega^m$) was absent, and the reader had no account of why the minimum $m$ is needed beyond one sentence. The extremal-choice table predated the lattice and descent results. The per-state heights table used spoke-path heights, which differ from the paper's by constants.

Recomputed. The paper's Table 2 exactly ($\omega = -4, -3, 2, 3$ and $-2, -1, 1, 2$; $\varepsilon$; which states are good); $\Sigma = 18$, $\sum\varepsilon = \sum\varepsilon\omega = 0$; the Laurent polynomial; $9x^2 + 5x^3$ for the linear substitution $w = 1 + x\kappa$; the heights-product sums 1 and 2; white faces inside each cycle; the height example of Figure 10 ($-1$ then $0$); the cube ($\Sigma = -1$); the 16-vertex example (26 states, 18 pairs, 12 good, three covers, the one-cycle cover with $W = 6$ and no good pair).

Fixes. Rewritten (about 3,500 words including tables): heights along face paths with the paper's example and Lemma 4.6; the finite difference and Proposition 4.8 with full proof; why $m$; the worked example as the paper's Table 2; one table of the other versions with their running-example values; the 16-vertex lesson; the canonical-choice table extended with Felsner extremes (18), extremes or irreducibles (33), bounded distance (24), and C3 bounded descent (16, 21, 40); "Other routes" with the involution note's referee verdict, C3 and C1 status. The spoke and ray versions survive as a paragraph naming them as older forms.

## 07. Recovery

Findings. Links 1 to 3 went through the spoke graph and its dual, where the paper uses $S_s$ and the tree of faces $Y_s$ (Lemma 3.6) and roots at $t_0$. The running example called $\beta$ "the state drawn as $r$" and $\alpha$ "$s^*$". The "Which cycles are produced" section matches the paper's Section 7 and the prism numbers are right. A stale render of the tree-cotree figure.

Recomputed. Cube: both good states, white tree a star at face 7, $P$, the cycles of faces; prism: 4 avoiding cycles for $e_0 = 01$, 2 and 2 for the other sides, 2 produced; running example: $P_\beta$, its two classes, $y_0 = 3$, the Hamiltonian face order, 28 Hamiltonian cycles of which 6 avoid the edge across $e_0$.

Fixes. Header and status; Links 1 to 3 rewritten on $S_s$ and $Y_s$ following the paper's proof of Lemma 3.6, with the white-face tree $W_s$ kept as $Y_s$ with black nodes suppressed and the spoke picture as a figure; Link 4 named as the paper's Proposition 3.9; names $\alpha$, $\beta$; primal Lemma 12 (compatibility suffices) in "Other routes".

## 08. Gluing and hypotheses

Findings. Correct. The paper's own gluing (cut at any separating triangle; acyclicity by the path argument) was not described. The hypothesis table missed the paper's smallest-size facts for the conclusion. "Other routes" lacked the degree-four induction (G and X open, direct lifting dead at 18) and the length-5 cut lesson. Kelmans's two-edge consequence was missing.

Recomputed. Double octahedron counts at all 14 roots and the deficient set; the gluing example's classes are as in `fable_digestions/crosscheck.py` (not re-run here).

Fixes. Header and status; paper's version of the gluing; table rows for bipartite and planar; Kelmans; induction G/X and longer cuts in "Other routes".

## Glossary

Findings. Two errors. The sign row said $\varepsilon = i^n i^{-J}$; it is $i^{n+J}$ (for the cube, $n = 3$, $J = 1$: $\varepsilon = +1$ while $i^{n-J} = -1$). The synonyms table listed the paper's "chosen sides" as a synonym of the selection; in the paper chosen sides are the edges leaving a state's corners. Heights were defined by spoke crossings. Missing: $S_s$, $Y_s$, $P_s$, $o$, outdegree lemma, chosen sides, turns and $\kappa$, $L(C)$, $\Sigma$, $\Pi$, finite difference, connectivity lemma, $\alpha/\beta$, Step R and X, induction G and X, C1, C3, P2, tiers, Lean names.

Fixes. Rebuilt as one line per term with columns paper, OpenAI, Li, constructive, Lean. The Lean names come from the primal dictionary and the blueprint; I did not open the Lean source.

## Not done

- Five-page limit: 03 (3,600 words) and 06 (3,500 with tables) are over. The rest are 1,600 to 2,900.
- I did not re-run Li's object counts (213/279), the subdivided-octahedron counts in 03, the 1,794/5,088 census figures, or the extremal-choice table; they are quoted with their sources and review state.
- Unslop: applied to every paragraph I wrote or rewrote. Paragraphs I did not touch keep their earlier style.
