# Illustrated route atlas

[Read the 28-page atlas](atlas.pdf). Each route also has a standalone vector PDF and a short Markdown explanation in `pages/`.

The atlas compares readings of the same proof. It does not claim 28 independent proofs. Each page contains 100 to 180 words, its review status, source pointers, and numbered connections. Status paragraphs govern mathematical claims on that page; finite illustrated objects have the separate status COMPUTED. LIT identifies supplied literature, including preprints, and does not assert peer review. Independently AI-refereed research still needs human checking.

## Build

From the repository root, with Python and MiKTeX `pdflatex` on PATH:

```powershell
python -m pip install networkx numpy scipy sympy pymupdf pillow
python digestions/atlas/build.py
python digestions/atlas/audit.py
```

The build runs in under two minutes on this machine. It writes only inside this directory and disables Python bytecode writes before importing external modules. It reads the current `paper/figures/` toolkit and loads its style via TEXINPUTS. The current example files are `running.json` and `layout-running.json`; the historical `example.json` and `layout.json` are not the authoritative 13-vertex example. No paper figure sources are copied or edited.

`build.py` computes graph objects, writes exact or independently checked finite data, emits TikZ and amsart A4 sources with one-inch margins, builds 28 standalone pages and the collected PDF, and renders every page to PNG. `audit.py` checks page counts, word counts, vector-only content, text margins and TeX overflow, then records input SHA256 hashes. `pages.py` is the editable prose. `QA.md` records visual inspection. Transient TeX logs and auxiliary files are ignored.

## Examples and encodings

The principal example is the toolkit's 13-vertex triangulation, dual to a 22-vertex cubic graph. The cube illustrates doubled matchings and Li's one-mark involution. The hexagonal prism is explicitly substituted for determinant, relaxation and coverage failures. Page 23 explicitly changes to the smallest reviewed 12-vertex canonical-choice witness. `examples.json` exports the face lists and running coordinates used.

The toolkit supplies grey triangulation edges and black faces, hollow roots, blue solid second-state wedges, outlined vermilion first-state wedges, blue D arrows, dashed vermilion Q edges, black retained spokes, green dash-dot white trees, bold black selected edges and purple Hamiltonian curves. LP wedges represent fractional weights only, as its legend states. Lattice nodes use green squares for tree objects and rings for extremes. No status tags appear inside pictures. Single running graphs occupy about 0.74 textwidth; multi-panel figures occupy a common 0.86 textwidth container. Matrices and small abstract lattices retain readable natural sizes.

## Computation and limits

- COMPUTED: all 12 running states, 8 ordered pairs, 2 cyclic pairs and 6 forest pairs; independently compared with `workings/barnette_lab`.
- COMPUTED: exact white-face potentials, both complete Hasse diagrams, signed pair terms, polynomial coefficients and an incidence-matrix row dependence.
- COMPUTED: a half-integral vertex on the running example, with all graphic subset inequalities checked exactly and active rank 25.
- COMPUTED: all 3 marked cube objects for Li's one-mark involution, with both involutions and every nonfixed sign reversal checked. This does not certify Appendix B's multi-mark implementation.
- COMPUTED: all 8 hexagonal-prism Hamiltonian cycles, its 2 rooted recovery images, and 4 nonstate bases of the two-constraint relaxation.
- COMPUTED: all cube partition restrictions on one triangle and one quadrilateral. These are label words, not the richer piece states in the categorical report. Five quadrilateral label words occur here; the report's six piece patterns must not be substituted for them.
- COMPUTED: five even prisms and width-four nanotubes through three layers, by direct enumeration. General transfer theorems remain the family author's unrefereed work.

Pages 21, 25 and 26 use obligation diagrams rather than invented graph constructions. Page 24 reuses the checked endpoint and explicitly declines to draw an uncomputed Feder-Subi contraction. The second trinity K is checked and drawn on page 28 in a separate plane layout of the cube objects. A five-cut witness and a full primal flow diagram are not newly computed figures in this atlas. Page 18 shows the checked primal endpoint and explains the cut-side reading. The atlas covers 28 major readings, not all 175 entries of the route map.

## Index

| Page | Route | PDF | Review status |
| --- | --- | --- | --- |
| 01 | One proof, several readings | [PDF](pages/01-waypoints.pdf) | LIT for the supplied OpenAI proof, Sections 3 to 7. The alternative research routes have mixed review status, recorded on their pages. |
| 02 | Eight terms, two regroupings | [PDF](pages/02-exponential.pdf) | LIT: OpenAI Proposition 5.1 and Lemmas 5.2 to 5.3. COMPUTED here for all 8 ordered pairs; the general proof is supplied literature. |
| 03 | Li turns the sum into paired objects | [PDF](pages/03-involutions.pdf) | LIT: Li, Definitions 13 to 23 and Appendix B. COMPUTED: first involution here. COMPUTED cube one-mark involution and signs; multi-mark implementation has not been independently refereed. |
| 04 | The same argument with linear weights | [PDF](pages/04-linear.pdf) | PROVED-HERE in the determinant referee, SIGNIFICANCE Section 2; independently AI-refereed reformulation, human review pending. COMPUTED polynomial here. |
| 05 | Put the height on white faces | [PDF](pages/05-heights.pdf) | PROVED-HERE in the combinatorics referee with normalization corrections; independently AI-refereed, human review pending. COMPUTED exact heights on all 12 states. |
| 06 | The disk identity as a census | [PDF](pages/06-euler.pdf) | LIT: OpenAI Lemma 4.1. COMPUTED: B=5, W=6, I=3, h=7, l=2; all D and directed Q cycles of all pairs also checked. |
| 07 | The disk has one extra white face | [PDF](pages/07-white-surplus.pdf) | PROVED-HERE in both combinatorics and topology referees; independently AI-refereed, human review pending. COMPUTED white areas 6 and 1 on this pair. |
| 08 | The disk identity as turning number | [PDF](pages/08-turning.pdf) | PROVED-HERE in the topology submission, CORRECT after explanatory additions by its independent AI referee. COMPUTED turn labels here; human review pending. |
| 09 | Cancellation is a row dependence | [PDF](pages/09-incidence.pdf) | PROVED-HERE in the combinatorics referee, exact global-factor correction included. Independently AI-refereed; COMPUTED matrix and null vector here. |
| 10 | A determinant needs coefficient extraction | [PDF](pages/10-determinant.pdf) | PROVED-HERE formulas independently AI-refereed in fable_referee-determinants. REFUTED shortcut: one raw evaluation counts tree matchings. The prism formula is independently reproduced there. |
| 11 | A doubled spoke is not a D-cycle | [PDF](pages/11-double-dimers.pdf) | PROVED-HERE double-dimer dictionary, independently AI-refereed. REFUTED shortcut with doubled edges. COMPUTED cube doubled matching here; no general cancellation-free proof. |
| 12 | Forget orientations, keep the pair lattice | [PDF](pages/12-pair-lattice.pdf) | PROVED-HERE correspondence independently AI-refereed. COMPUTED complete running-example Hasse diagram. REFUTED individual extreme guarantees; joint-extremes conjecture remains open in the reviewed sources. |
| 13 | The twelve states under clock moves | [PDF](pages/13-clock-lattice.pdf) | COMPUTED complete order on all 12 states and tree markers here. General height reading independently AI-refereed; canonical-extreme shortcuts REFUTED in the combinatorics referee. |
| 14 | Three constraints, not two | [PDF](pages/14-three-matroids.pdf) | PROVED-HERE three-matroid description independently AI-refereed. COMPUTED all 6 two-constraint prism bases here, 4 nonstates. No polynomial-time algorithm follows. |
| 15 | The natural relaxation has a fractional vertex | [PDF](pages/15-fractional.pdf) | COMPUTED here with all subset inequalities and full active-rank certificate; exact half values. General relaxation obstruction independently AI-refereed in the structure report. |
| 16 | A white tree with one token per face | [PDF](pages/16-rainbow.pdf) | Original rainbow dictionary independently AI-refereed. New Theorem R and exchange results in RAINBOW.md are PROVED-HERE but unrefereed. COMPUTED tree and point-preserving exchange here. |
| 17 | What a small cut must remember | [PDF](pages/17-boundary.pdf) | COMPUTED cube boundary restrictions here. LIT triangular gluing. Categorical 4-cut completeness proof is unrefereed and has a finite-check subcase; 5-cut failure is unrefereed computation. |
| 18 | Keep the construction inside G | [PDF](pages/18-primal.pdf) | LIT supplied proof; formal dependency description from opus_lean-formalisation is unrefereed research. COMPUTED recovered cycle checked by toolkit and barnette_lab here. |
| 19 | From a white tree to one Jordan curve | [PDF](pages/19-recovery.pdf) | LIT: OpenAI Section 6 and constructive paper recovery criterion. COMPUTED P, inducedness, white tree and Hamiltonian cycle; independent laboratory recovery agrees. |
| 20 | Two produced cycles, six missed cycles | [PDF](pages/20-coverage.pdf) | COMPUTED all 8 prism cycles and both recovery images here. Injectivity and failure of surjectivity independently AI-refereed in sol_referee-structure/REFEREE-limits.md. |
| 21 | Four places a hypothesis enters | [PDF](pages/21-hypotheses.pdf) | PROVED-HERE failure analyses independently AI-refereed in the limits report. Schematic obligations only; no claim of four newly computed graph counterexamples. |
| 22 | Counts separate existence from abundance | [PDF](pages/22-families.pdf) | COMPUTED prisms p=4,6,8,10,12 and width-four nanotubes L=0,1,2,3 here. General prism formulas and nanotube transfers are PROVED-HERE in an unrefereed family report; no independent review claimed. |
| 23 | The tempting highest state can be cyclic | [PDF](pages/23-canonical.pdf) | REFUTED canonical highest/lowest guarantees, independently AI-refereed with reflection correction. COMPUTED validity and cyclic Q of this 12-vertex witness here. |
| 24 | Earlier methods meet the new forest step | [PDF](pages/24-earlier.pdf) | LIT endpoint equivalence as cited in supplied papers. Older-method comparison is unrefereed research, with explicit original-source limitations; no new equivalence asserted. |
| 25 | Grassmann variables package the same coefficient | [PDF](pages/25-berezin.pdf) | PROVED-HERE identities and REFUTED gauge shortcuts in sol_route-algebra, unrefereed. The overlapping determinant identity is independently AI-refereed elsewhere. |
| 26 | The doors that are actually still open | [PDF](pages/26-open.pdf) | CONJECTURE and HUNCH only for the new implications. Unrefereed conjecture and induction reports; finite checks are not general guarantees. Established backbone is supplied literature. |
| 27 | Morse cancellation pairs the bad orientations | [PDF](pages/27-morse.pdf) | PROVED-HERE dictionary independently AI-refereed after sign and root corrections. COMPUTED complete two-mate cube here. This is not an independent existence proof. |
| 28 | Three incidence graphs in one triangulation | [PDF](pages/28-trinity.pdf) | COMPUTED K on the cube, with 14 vertices, 36 edges and 24 triangular faces. Triangle-factor reformulation is unrefereed. Floer dictionary independently AI-refereed as a dictionary only. |

## Data files

Every JSON data file records its command, or is emitted by `build.py` as named in this README. `computed.json` carries the complete running enumeration, heights, covers, polynomial and LP values. `incidence.json`, `li-cube.json`, `rainbow-exchange.json`, `prism-counts.json` and `nanotube-counts.json` and `trinity.json` carry the smaller certificates. `manifest.json` records page metadata and prose word counts. `audit.json` records PDF checks and read-only input hashes.
