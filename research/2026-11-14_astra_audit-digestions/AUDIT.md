# Audit of the reader-facing digestions

## Audit boundary

Referee: gpt-6-astra, a different model from the Fable authors. The main conclusion is the supplied OpenAI theorem: every finite simple cubic bipartite 3-connected planar graph has a Hamiltonian cycle avoiding any prescribed edge. The source boundary is the eleven step documents, HOW-IT-WORKS.md, the route-map generator and the supplied referee reports. I read the OpenAI text and visually checked PDF page 7, including the spoke slide and leading coefficient.

Accepted primitives are elementary finite graph theory, Euler's formula for sphere graphs and disks, integral max-flow, tree/cotree duality and the Jordan curve theorem with signed intersection numbers. The audit checks the explanatory route; it does not establish historical priority or certify every cited paper. LIT below identifies supplied literature, not journal review.

This is not a blanket certification of every ancillary claim in the 186-route inventory. The exact computations replayed are recorded below. Large census totals, historical citations with inaccessible originals, runtime claims and the new conjecture campaign remain attributed evidence, not newly certified facts.

## Findings and applied corrections

| ID | Severity | Location | Finding and disposition |
|---|---|---|---|
| A01 | major | step 01, counting 2-factors | The determinant claim covered arbitrary planar graphs. Restricted it to bipartite planar graphs and identified the general Pfaffian formulation. |
| A02 | moderate | step 01, example table | Three examples do not prove that the connected fraction decreases with graph size. Restricted the sentence to the displayed examples. |
| A03 | moderate | step 01, historical discussion | Removed the universal claim that all earlier face-size results use the stated local method. Removed an unverified König date while retaining the Hall proof. |
| A04 | major | step 02, equal cardinalities | Equality of the two part sizes does not prove existence of an incidence matching. Said explicitly that the matching argument is still needed. |
| A05 | moderate | step 02, octahedron face list | Coherently oriented sphere faces are not all counterclockwise in the plane: the outer face has the opposite planar orientation. Corrected the caption. |
| A06 | major | step 03, failed relaxation | The paragraph began by dropping disjointness, then actually dropped bijectivity. Replaced it by the relaxation the proof discusses, retaining distinct choices in each face. |
| A07 | moderate | step 05, weights | Functions of s are sufficient, not necessary. Any weight invariant under the selected involution also cancels. Corrected the exclusive wording. |
| A08 | major | step 06, lab polynomial | COMPUTED. The current lab output is z^3 Z(1/z), not just an exponent shift. Corrected the comparison and recorded the embedding dependence. |
| A09 | major | step 06 and HOW-IT-WORKS, Li marks | Lists, repeated marks and distinct unordered marks have different multiplicities. Corrected the description and stopped presenting their coefficient identification as already proved. |
| A10 | moderate | step 06, missing computation | COMPUTED. Added the 213-object Li replay, the 141 and 9 fixed-point counts, signs and the exhaustive orbit checks. Full fixed points are saved, with a face-ID dictionary. |
| A11 | major | step 08, nonfacial roots | The proposed root variant omitted which black face is removed. Explained the cardinality obstruction and required a corrected formulation before testing it. |
| A12 | major | step 09, route D.7, SOTA | The conjecture campaign reports joint failures at 18 vertices. Replaced the surviving-conjecture claim by an attributed provisional refutation. Added the distance-one and irreducible replacement doors. Independent replay remains pending. |
| A13 | major | routes U.3 and U.x5 | Natural triple irredundancy does not rule out every two-matroid encoding. Corrected that inference and the fractional-support description from the structure referee. |
| A14 | major | seed.py, knowledge, README | LIT had automatically implied T1, including unrefereed preprints. Separated provenance from tier. Source preprint claims and waypoints are conservatively T2, with explicit review state. |
| A15 | major | seed.py | Unreviewed project proofs were labelled established. Changed this to proof supplied with the actual review state. |
| A16 | moderate | seed.py, events | Rebuilding used to rewrite the historical backfill. It now preserves existing event lines and only appends new entries. |
| A17 | moderate | seed.py, SOTA | Added result-history preservation and a row for the new manuscript routes. |
| A18 | moderate | HOW-IT-WORKS, group sign | Individual counterclockwise cycles do not all have the same sign. Wrote the length-dependent sign and its product over the cover. |
| A19 | moderate | HOW-IT-WORKS, modular counts | Vanishing of this signed sum does not exclude all modular invariants. Restricted the negative claim. |
| A20 | moderate | map figures and HOW-IT-WORKS | Forced suggested a theorem excluding alternative proofs. Replaced rendered labels by shared and choice, and explained their inventory-only meaning. The matrix now says proof supplied, not established. |
| A21 | moderate | steps 03, 07, 08, 09 | The structure REPORT remains a work log. Added that exact snapshot; retained the specific INTEGRATION verdicts without inventing a final report. |
| A22 | moderate | topology routes | Late REFEREE confirms named claims with corrections: negative sign in the Q-cycle grading, root spokes in the Forman matching, boundary flatness and outer-face exclusion. Applied those qualifications in the route entries. |
| A23 | moderate | step 09, counting | The late older-approaches report supplies an unbounded c_min family with separators. Replaced the stale finite-range-only sentence, retaining unreviewed status. |
| A24 | moderate | manuscript routes | Added primal, draft A and draft B separately. Draft B uses scalar height moments and recovery through Y_s, not the linear-weight polynomial. Corrected the initial integration label before delivery. |
| A25 | minor | steps and HOW-IT-WORKS | Removed em dashes and curly quotation marks; shortened broad claims and unnecessary metaphors where they obscured the mathematical scope. |
| A26 | minor | step 06 images | Added the two covers with common s* and the 16-vertex bad cover in both orientations, using the figure toolkit's model and layout read-only. Visually inspected both. |
| A27 | minor | glossary | Li's inner-white-face translation now excludes white vertices adjacent to the black root. |

## Numerical coverage

COMPUTED. The checks use workings/barnette_lab, not the digestion author's implementation. Saved face lists and weights are inputs; their asserted answers are not used to generate the lab states or pairs.

- Cube, prism and running example: exhaustive states, ordered pairs, tree matchings, 2-factor component distributions, sign reversal and lab polynomials.
- The six stored state examples, including both 12-vertex orientations and the 16-vertex example: all states and partner lists, component root counts, every displayed cover disk, B/W/I/h/ell, interior vertex and white-face lists, pair signs, J, weights and complete linear-weight polynomials.
- Double octahedron: all 14 roots, eight with four pairs and six with no pair.
- Recovery: exact selected edges for the cube and running example; induced tree classes and Hamiltonian cycle. Gluing classes checked in the full double octahedron. Nonbijective disk counts independently recovered from a cut in the lab dual.
- Li running example: 213 objects; involution closure, squaring to the identity and sign reversal on every nonfixed orbit. First fixed set has 66 positive and 75 negative objects; second has nine negative objects. Both signed counts are -9.
- All Markdown image links in the step documents resolve.

Limitations: the census tables through 16 vertices, 26-vertex non-3-connected example, torus example, sampled LP/lattice experiments, determinant test-point arithmetic and runtime bounds were not all rerun here. Individual absolute height values depend on the paths; the saved sum weights and resulting polynomials were replayed, but this run does not independently reconstruct every path used by the author. Those claims keep their original source-specific review status. No exhaustive historical citation verification is claimed.

## Reader test: ten points repaired

1. Overview: distinguish existence by a nonzero count from an efficient constructor.
2. Step 01: say exactly what connectivity adds to a 2-factor.
3. Step 02: distinguish a cycle through dual vertices from the desired cycle through dual faces.
4. Step 03: distinguish opposite Q edges from incident D edges and name what each reversal changes.
5. Step 04: fix the disk side and explain which data change under reversal.
6. Step 05: explain that a cube is a set of binary orientation choices.
7. Step 06: allow repeated chosen white faces while keeping their indices distinct.
8. Step 07: distinguish the three vertex roots from the one white-face root.
9. Step 08: explain the order of solving the two capped pieces.
10. Step 09: distinguish finite tests, supplied proofs, AI review and formal verification.

The overview and HOW-IT-WORKS answer why the proof uses these objects: a state is extracted from a putative answer, a partner supplies an orientation, cycles can be reversed, and the two evaluations force a forest state. The new bridges address definitions that previously arrived without that distinction.

## Incoming reports and remaining review boundaries

The topology REFEREE arrived during this run and was integrated. Its referenced RAINBOW.md was absent at the integration snapshot, so its new Rado proof is recorded as announced, not inspected. The older-approaches final report also arrived and was integrated with unreviewed status. The induction folder was absent. The conjecture folder had predictions and data, but no final report. The structure final report was still provisional. Draft A has a referee verdict with repairs; this audit does not certify that its author applied every repair. Draft B had no final independent referee report at the snapshot.

The new topology referee proofs, the primal proof and the family proofs need their own bounded audits. This audit does not convert their inclusion on a map into approval of their proofs.

## Obligation graph for the main explanatory route

LIT conclusion C0 and its supplied route, after the local explanatory repairs above:

    C0 <- R0 AND(C1, C2, C7)
    C2 <- R2 AND(C3, C4, C5, C6, O13, O14, O15, O16)
    C3 <- R3 AND(O1, O2)
    C4 <- R4 AND(O3, O4, O5)
    C5 <- R5 AND(O6, O7)
    C6 <- R6 AND(O8, O9, O10)
    C7 <- R7 AND(O11, C2, O12)

C2 is the rooted no-obstruction case; C7 handles the complementary separator case. These are exhaustive cases, not alternative OR proofs. The height route is the actual sufficient route of step 06; determinant and topology remarks do not repair or replace an obligation on that route.

## Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
|---|---|---|---|---|---|---|
| C0 | Prescribed-edge-avoiding Hamiltonian cycle | root | R0 | root | steps 01–08 | discharged |
| C1 | Dual is simple, face-bicoloured sphere triangulation | C0 | R0 | major claim | step 02; OpenAI Thm 1.1 proof | discharged |
| C2 | Rooted partition when a pair exists | C0,C7 | R2 | major claim | steps 03–07 | discharged |
| C3 | Pair criterion | C2 | R3 | major claim | step 03; structure INTEGRATION §§1–2 | discharged |
| O1 | Incidence flow is integral and its cuts have the stated capacity | C3 | R3 | named theorem | integral max-flow, capacities 2/1/2 | discharged |
| O2 | Euler-region bound excludes exactly black-inner triangles | C3 | R3 | algebraic/logical step | component and repeated-edge-side counts in step 03 | discharged |
| C4 | State-cycle disk identity | C2 | R4 | major claim | step 04; OpenAI Lemma 4.1 | discharged |
| O3 | Directed cycle is simple and its disk excludes roots | C4 | R4 | side condition | outdegree and outer-face placement | discharged |
| O4 | B=I+ell uses a bijection | C4 | R4 | algebraic/logical step | step 04 Count 1 | discharged |
| O5 | Side count and Euler give W=B+1 and h-2ell=3 | C4 | R4 | algebraic/logical step | step 04 Counts 2–3 | discharged |
| C5 | Cyclic Q contributions cancel | C2 | R5 | major claim | step 05 | discharged |
| O6 | Choose cycle using s alone; reversal preserves state and has no fixed point | C5 | R5 | algebraic/logical step | explicit involution | discharged |
| O7 | Odd cycle reverses sign while F(s) is fixed | C5 | R5 | proved earlier | C4 plus local sign identity | discharged |
| C6 | Some weighted sum is nonzero | C2 | R6 | major claim | step 06 height proof | discharged |
| O8 | Spoke detours preserve simple orientation and white-face containment | C6 | R6 | algebraic/logical step | Lemma H; OpenAI PDF p7; rewritten Prop 5.1 | discharged |
| O9 | Every cycle contains a white face; a minimum cover exists | C6 | R6 | proved earlier | C4, finite nonempty pair set | discharged |
| O10 | Finite differences kill higher-cover terms; minimal terms have common sign and one is nonzero | C6 | R6 | algebraic/logical step | explicit indexed-bijection expansion | discharged |
| C7 | Separator induction glues prescribed partitions | C0 | R7 | major claim | step 08 | discharged |
| O11 | Caps are smaller simple bicoloured triangulations | C7 | R7 | side condition | signed three-side count | discharged |
| O12 | Agreeing tree classes intersect in vertex or edge and remain induced | C7 | R7 | algebraic/logical step | step 08 gluing | discharged |
| O13 | Forest Q has one root per component using partner | C2 | R2 | proved earlier | step 03 component outdegree count | discharged |
| O14 | White cotree selects one edge per face | C2 | R2 | named theorem | tree/cotree duality on H | discharged |
| O15 | P0 is acyclic by disk contradiction; e0 joins distinct components | C2 | R2 | algebraic/logical step | step 07 Link 4 | discharged |
| O16 | Complementary dual is connected and 2-regular | C2 | R2 | named theorem | tree/cotree duality and face degree count | discharged |

In R2, C2 requires O13–O16 as well as C3–C6; these are the recovery obligations expanded in the table.

## Verdict

FOLLOWS for the main explanatory height/cancellation/recovery/gluing route after the stated corrections. No failing conclusion-reachable obligation remains in that route. This verdict does not certify every ancillary conjecture, historical attribution, computational census or newly supplied route. The unverified items above remain explicit review tasks.
