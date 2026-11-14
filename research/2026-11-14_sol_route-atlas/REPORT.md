# Illustrated proof-route atlas

COMPUTED: delivered 28 standalone vector pages and a collected amsart A4 atlas.
COMPUTED: all illustrated states, pairs, trees, orientations, lattices and cycles are generated and checked, with a separate laboratory comparison on the running example.
COMPUTED: every page was rendered to PNG and visually inspected; the final audit checks word counts, margins, vector content and TeX overflow.
The atlas follows the available referee corrections and states each route's review status outside its picture.
Unrefereed claims and deliberately schematic or incomplete readings are listed below; no new general existence proof is claimed.

## What I set out to do

Build an illustrated atlas of the main proof routes and reformulations, using the same running objects and fixed visual encodings. The owned paths are this research folder and `digestions/atlas/`. No other digestion or paper figure was edited. I read the repository brief, README, unslop skill, the figure conventions and toolkit, the three paper text dumps, the route map and the relevant submission and referee reports. I applied the PDF render-and-inspect workflow with PyMuPDF and LaTeX rather than the skill's generic reportlab/output-folder defaults, because the user explicitly required amsart and this destination. No subagents were used.

## What I established and delivered

COMPUTED. `digestions/atlas/atlas.pdf` collects 28 one-page routes. Every page has a standalone PDF, TeX source, body source and short Markdown explanation. Each explanation has 100 to 180 words, a separate status paragraph, numbered connections and source pointers. `README.md` gives commands and a page index. `build.py`, `pages.py`, `audit.py`, all JSON certificates and all PNG renders are included. `QA.md` records the visual review. Source SHA256 hashes are in `audit.json`.

COMPUTED. Commands from the repository root:

```powershell
python digestions/atlas/build.py
python digestions/atlas/audit.py
```

COMPUTED. The build enumerates all 12 states and 8 ordered pairs of the 13-vertex running triangulation, checks its two cyclic pairs and six forest pairs, and compares states, pairs and recovery with `workings/barnette_lab`. It solves the face-potential equations exactly to generate both Hasse diagrams and the integer height labels. It computes the signed pair table, the linear-substitution polynomial, and an exact incidence-matrix row dependence.

COMPUTED. A fixed-seed LP search finds a half-integral vertex on this same running example. All partition equations and all graphic subset inequalities are checked with exact rational values, and the active constraints have rank 25. This is a checked finite obstruction to the naive integrality claim, not a new theorem about all relaxations.

COMPUTED. The cube's three one-mark Li objects pass both involution tests and all nonfixed sign reversals. Its second involution has one fixed object. The hexagonal prism has three states, two tree matchings, eight Hamiltonian cycles and two rooted recovery images; all are enumerated. Four nonstate common bases of the two-constraint relaxation are checked. The cube's triangular and quadrilateral partition restrictions are enumerated. Five prism sizes and width-four nanotubes at layers 0 through 3 are directly counted. The second trinity of the cube has 14 vertices, 36 edges and 24 triangular faces, and its separate plane drawing has no crossings between nonincident edges.

COMPUTED. The white-tree exchange in page 16 is point-preserving: every nonroot still supplies one deleted spoke. It changes face loads from all ones to one zero and one two. This illustrates the actual missing face-balance condition, rather than only an arbitrary spanning-tree exchange.

## Which pages rest on unrefereed claims

Every new finite calculation in this atlas remains COMPUTED and has not acquired independent referee status merely by passing assertions. Existing research tagged PROVED-HERE is attributed to its source, not presented as a new proof in this folder.

| Pages | Unrefereed dependency or limit |
| --- | --- |
| 03 | Li Appendix B's multi-mark laboratory implementation remains outside the determinant referee's scope. Only the cube's complete one-mark implementation is newly checked here. |
| 16 | The new Theorem R and exchange results in `fable_referee-topology/RAINBOW.md` were authored by the referee and have not themselves received independent review. The original rainbow dictionary has a referee verdict. |
| 17 | Categorical quadrilateral completeness and the five-cut failure are unrefereed; one completeness subcase rests on finite checking. The drawn cube restrictions are independently computed here, but are only label words, not full piece states. |
| 18 | The Lean dependency and primal-flow reading comes from the unrefereed formalization report. This atlas does not rebuild Lean or supply a new full flow diagram. The drawn recovered cycle is checked independently with the lab. |
| 22 | General prism formulas and nanotube transfer theorems are in an unrefereed family report. The displayed finite counts are directly recomputed here. |
| 24 | The older-method comparison and precise Feder-Subi bridge are unrefereed research. Source limitations are retained. The picture shows only the checked two-tree endpoint. |
| 25 | Berezin, Gaussian and gauge-obstruction claims are from the unrefereed algebra report. The overlapping determinant identities have a separate referee. |
| 26 | Joint true-extremes, efficient exchange, contraction injection and exponential counting remain conjectures or hunches. The active conjecture and induction folders were incomplete at reading time; no absent REPORT was treated as evidence. |
| 28 | The second-trinity triangle-factor equivalence is unrefereed. K itself is computed here. The Floer dictionary has an independent AI referee verdict as a dictionary, not an independent proof. |

The remaining general claims use the supplied papers or the available independent AI referee verdicts. Those verdicts are not human peer review. The corrected full-cycle meaning of alpha-orientation extremes is used; original-face terminal orientations are not silently called true extremes.

## What failed and why

COMPUTED. A first attempt to count nanotube tree matchings tested only whether Q was a forest. It returned 2,5,12,29 rather than 2,2,2,2 because root components were not constrained. The corrected calculation additionally requires exactly one root in each component. The final table and all saved certificates use the corrected criterion.

COMPUTED. The original categorical caption called six quadrilateral restrictions present on the cube. Direct enumeration found five label words. The report's six patterns also include connectivity data in a disk piece, so they are different objects. The final page states the distinction explicitly instead of altering the computed data to fit the prose.

COMPUTED. Overlaying all exterior H and G routes from the figure toolkit can merge distinct edges on the same collar. The second-trinity page therefore uses a separately computed, crossing-checked plane layout of the same cube objects. It does not falsely present those overlapping routes as a triangulation.

Visual inspection caught an unreadable full degree-ten polynomial, overlapping lattice rings, crowded historical witness labels, tinted faces obscuring their context edges, and long source paths running out of the text block. These were corrected. The full polynomial remains available in JSON.

## What is still open or deliberately not drawn

The atlas is a 28-reading selection, not 175 separate route pages. Pages 21, 25 and 26 are obligation diagrams. Page 24 does not draw a Feder-Subi contraction. Page 17 does not draw a new five-cut witness, and page 18 illustrates the primal endpoint rather than all flow weights. The current figures do not certify the multi-mark Li code, prove efficient exchange, resolve the true-extremes disjunction, or establish a new Floer nonvanishing theorem. These limits are stated where they matter and in the README.

## Three best next steps

1. Have a human reader check the atlas against the supplied PDFs and the AI-refereed corrections, especially the normalization of heights, the sign conventions and the distinction between label words and boundary connectivity states.
2. Extend page 03 to a separately refereed, fully drawn multi-mark Li example; extend page 18 with a computed primal flow and cut-side certificate on the same 22-vertex G.
3. Draw a verified five-cut missing-pattern witness and an explicit Feder-Subi contraction only after their complete data and hypotheses are fixed. These are the most useful remaining additions beyond the 28-page selection.

## Leads for others

The same running example supports a full-rank fractional vertex, so a separate LP witness need not disrupt the exposition. Its two-factor alpha lattice has only two nodes, both carrying tree orientations, while its state lattice has twelve nodes. The two lattices should never share a single unlabeled diagram. New results in referee folders need their own review-status label rather than inheriting the review status of the claims they originally checked.
