# Experiments

All runs use the Eulerian triangulations produced by `plantri -ba` (the lab's `vendor/plantri.exe`), one per isomorphism class: 1, 1, 1, 2, 2, 8, 8, 32 classes for 6, 8, 9, 10, 11, 12, 13, 14 vertices. Commands are run from `code/`. Every `COMPUTED` claim is evidence from one implementation, mine, with no independent replay. Outputs are in `data/`. Predictions were written before each run and are quoted as made.

| # | Command | Output | Time (rough) |
| --- | --- | --- | --- |
| E1 | `python cuts.py glue 10 6` | `data/glue_v10.txt` | 3 s |
| E2 | `python cuts.py three 12` | `data/three_v12.txt` | 2 s |
| E3 | `python cuts.py four 15` | `data/four_v15.txt`, `data/four_cuts_v15.json` | 50 s |
| E4 | `python cuts.py full 13 m` for `m = 3, 4, 5, 6` | `data/full_v13.txt` | 20 s |
| E5 | `python gadgets.py 11` and `python gadgets.py 11 p4` | `data/gadgets_thm22_v11.txt`, `data/gadgets_p4_v11.txt` | 10 s |
| E6 | `python trinity.py tutte 11` | `data/tutte_v11.txt` | 5 s |
| E7 | `python trinity.py factors 11` | `data/factors_v11.txt` | 5 s |
| E8 | `python trinity.py tworoot 12` | `data/tworoot_v12.txt` | 3 min |
| E9 | `python homology.py hall 9` | `data/hall_v9.txt` | 1 s |
| E10 | `python homology.py bicomplex 12` | `data/bicomplex_v12.txt` | 2 s |
| E11 | `python recursion.py mult 9` | `data/mult_v9.txt` | 30 s |
| E12 | `python recursion.py contract 12` | `data/contract_v12.txt` | 20 s |
| E13 | `python monodromy.py 12` | `data/monodromy_v12.txt` | 20 s |

## E1. The gluing formula

Prediction: "the loop polynomial of the sphere equals the pairing of the two disk vectors, for every cycle, with no exception; if it fails my boundary state is missing data".

Result: holds for all 1157 cycles of length 3 to 6 (67, 154, 356, 580) in the five triangulations with at most 10 vertices. The loop polynomials are, for example, `6d + 3d^2` for the octahedron (6 Hamiltonian cycles of the cube up to the normalisation `lab(c_0) = 0`, and 3 two-cycle 2-factors). The Hamiltonian-compatible boundary states seen number 3, 8, 20, 50 for `m` = 3, 4, 5, 6, equal to `sum_j C(m, 2j) Cat(j)`.

Status: Proposition 1 of `PROOF.md`, `PROVED-HERE` and `COMPUTED`.

## E2. Separating triangles

Result: all 278 sides of separating triangles with an interior vertex, in the triangulations with at most 12 vertices, realise exactly the three label words `001, 010, 011`. This is O Theorem 2.2 seen as "the boundary functor is full at length 3". It is a check of my code against a known theorem, not new information.

## E3. Cuts of length 4

Prediction: "unlike triangles, no single pattern is always achievable, and the realised set depends on the piece". This was wrong.

Result: among 14872 rotated cut sides (4-cycles with an interior vertex on both sides, all triangulations with at most 15 vertices), exactly three pattern sets occur:

| signs | chord | realised set | sides |
| --- | --- | --- | --- |
| `++--` | none | `A0 A2 P01 P12 X02 X13` | 3516 |
| `++--` | `c0 c2` | `A0 A2 P01 P12 X02` | 1244 |
| `+-+-` | none | `A0 A1 A2 A3 X02 X13` | 10112 |

So the realised set is a function of the sign word and the chord. The missing patterns are exactly those excluded by the selection rule (Proposition 2) and by the chord. This led to Theorem 3.

The "abstract gluing" lines of the output test sides from different triangulations against each other. With one pattern set per type they carry no information.

## E4. Is the realised set always everything the rule allows?

Prediction (made after E3): "true for `m = 4`, and I expect it to fail for `m = 5` or `6`, perhaps 70%, because a fullness statement at every length would be too strong a strengthening of Barnette's conjecture to have gone unnoticed".

Result, chordless sides with an interior vertex on both sides, up to 13 vertices:

| `m` | allowed by the rule | sides | realise all | miss some |
| --- | --- | --- | --- | --- |
| 3 | 3 | 26 | 26 | 0 |
| 4 | 6 | 705 | 705 | 0 |
| 5 | 14 | 450 | 95 | 353 miss one, 2 miss two |
| 6 | 30 or 32 | 1258 | 2 | 1256 |

Smallest failure: `plantri_9_0`, cycle `(0, 1, 6, 8, 4)`, signs `---+-`, three interior vertices, pattern `00011` missing. The script also asserts that no realised state violates the selection rule.

Caveat: the pieces are small, and I did not look for a finer local rule that would explain the missing patterns at `m = 5`. What is established is that the realised set is not a function of the sign word.

## E5. Which prescriptions force a 4-cut pattern

Result with one prescribed facial edge (O Theorem 2.2): over all caps in triangulations with at most 11 vertices, only `X13` for signs `++--` is forced, by the two-triangle cap. Nothing is forced for `+-+-`.

Result with a prescribed 3-edge path (O Corollary 7.2): every allowed pattern is forced by some cap without chords, except `X13` for `++--`, which is forced only by caps containing the chord `c0 c2` (as it must be, and there Theorem 2.2 suffices). The smallest caps are a single vertex of degree 4 for `+-+-` and the octahedron minus two adjacent faces for `++--`. These are the caps used in the proof of Theorem 3.

## E6. Tutte's tree trinity

Result: for all 153 pairs (rooted triangulation with at most 11 vertices, colour), the map from states to arc sets is injective, every image is an arborescence into the root, and the number of states equals the determinant of the reduced Laplacian. A check of the dictionary against a published theorem.

## E7. Projections of triangle factors

Prediction: "a Hamiltonian cycle with one root on each side gives a two-root state by construction; its `Q` is a forest often but not always".

Result: 2048 factors up to 11 vertices. Black projection acyclic 1839, white 1875, both 1681, neither 15. The octahedron and the 8-vertex and first 10-vertex triangulations have no failure.

## E8. Two-root tree matchings

Predictions: "(a) every root pair has one, even with separating triangles, 50%; (b) each gives a Hamiltonian cycle in at least one orientation, 60%; (c) every Hamiltonian cycle is reached, 50%".

Results up to 12 vertices (15 triangulations):

- (a) true for the 10 triangulations without separating triangle and for 4 of the 5 with one. `REFUTED` in general by `plantri_12_6` (51 of 66 root pairs).
- (b) `REFUTED` at 8 vertices: 12 of the 86 two-root tree matchings of `plantri_8_0` have no Hamiltonian orientation. Overall 1327 of 5154 have none, 1230 have one, 2597 have two. Every two-root tree matching has exactly two orientations, as the unicyclic dual predicts.
- (c) true in all 15 triangulations (258 cycles).

## E9. Topological Hall condition

Prediction: "fails early, 80%: intersections of three matroids are not highly connected".

Result: fails for all 17 rooted triangulations with at most 9 vertices. On the octahedron the subcomplex on two faces is disconnected, and the whole complex (which should have vanishing reduced homology in degrees 0 and 1) has `b_0 = 1`. Homology over GF(2).

## E10. Do the two reversals commute?

Prediction: "no, first failure on a small example".

Result: 624 pairs in total over all rooted triangulations with at most 12 vertices. For 12 of them the set of pairs reached by a `Q`-reversal followed by a `D`-reversal differs from the set reached in the other order. I expected more failures. The small total reflects how few pairs these instances have.

## E11. Insertion into a face

Result: 1016 insertions into white faces, where states, pairs and tree matchings all multiply, and 840 insertions into black faces, where pairs and tree matchings vanish. Pieces up to 9 vertices, glued size up to 14. Proposition 6.

## E12. Contraction of a degree-4 vertex

Prediction: "no exact recursion; the inequality `tau(T) >= tau(T/ac)` fails somewhere, 60%". The second part was wrong in this range.

Result: 948 contractions that keep the triangulation simple and the root face intact, up to 12 vertices. `tau(T) >= tau(T/ac)` in all of them. In 36, `tau(T/ac) = 0 < tau(T)`. Never the reverse. The case where both contractions of one vertex are simple did not occur, so the candidate `tau = tau_ac + tau_bd` could not be tested.

## E13. Permutation triple

Result: for all 15 triangulations up to 12 vertices the triple has `k + 2` cycles, cycle lengths `deg/2`, product one, and the three matchings of `G` are recovered from it. States counted as transversals of cycles agree with states counted directly. Hamiltonian cycles counted from the triple agree with those counted from the map. The passport `((2,2,3,3), (2,2,3,3), (2,2,3,3))` is shared by `plantri_12_2`, `plantri_12_4`, `plantri_12_7` with 24, 20, 24 Hamiltonian cycles.

## What was not run

- Gluing for annuli (pieces with two boundary cycles).
- Cuts of length 4 beyond 15 vertices, and any search for a finer rule at length 5.
- Two-root experiments beyond 12 vertices.
- An independent implementation of anything here. The only cross-checks are against the lab (state and pair counts through `barnette_lab.core.Instance` in E10) and against published theorems (E2, E6).
