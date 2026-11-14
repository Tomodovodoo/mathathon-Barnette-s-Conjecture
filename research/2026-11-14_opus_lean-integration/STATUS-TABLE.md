# Status table, statement by statement

COMPUTED from `proofs/blueprint/blueprint.json` by `scripts/status_table.py`. Paper: `paper/main/barnette.tex` at commit `e97b0614eb` (version 2). Statement numbers are unchanged from version 1 (`extract_tex.py --worktree` reports no mismatch against `barnette.aux`).

Old status: the blueprint of `research/2026-11-14_opus_blueprint` (v1), which had three values, exact, "counterpart in different form" (covered) and none.
New status: four values, after the independent rebuild `research/2026-11-14_astra_lean-check`. Where the author's report (`opus_lean-devices`) and the checker disagree, the checker's verdict is used.

- **exact**: the Lean states the same proposition, given the upstream definitions of state and pair.
- **after translation**: the Lean states the proposition in its algebraic-dual model, and the dictionary to the paper's drawing is informal. The translation is named (B1 to B5, see `proofs/blueprint/BLUEPRINT.md`).
- **weaker / different**: the Lean states less, or a different statement that the route can use. The reason says what is missing.
- **none**: no Lean counterpart.

Lean origin: `upstream` = OpenAI's 31 files at `4eaee875`; `added here` = `proofs/lean/Devices`, built by opus_lean-devices and rebuilt from a fresh clone by astra_lean-check; `both` = the counterpart uses both.

## Counts on the route to Theorem 1.1 (34 statements)

| | exact | after translation | weaker / different | none |
| --- | --- | --- | --- | --- |
| v1 (opus_blueprint) | 4 | 25 (one class: "different form") | | 5 |
| checker's advisory recount (astra RECOUNT.md) | 5 | 27 (one class) | | 2 |
| **now** | **5** | **17** | **10** | **2** |

The new count agrees with the checker's: its 27 is our 17 + 10. Splitting the class is new here. It separates statements whose whole content is in the Lean from statements of which the Lean has only part.

Moved out of "none" by the project's Lean, now independently rebuilt: `lem:outdegree` (weaker / different), `lem:sign` (after translation), `lem:difference` (exact).
The v1 class "different form" (25 statements) splits into 16 after translation and 9 weaker or different: `thm:main`, `lem:duality.2`, `def:good`, `lem:good`, `lem:Y`, `lem:partner`, `lem:cancel`, `txt:heights`, `lem:height`.

## Route statements

| statement | content | v1 status | new status | Lean origin | project declarations | reason |
| --- | --- | --- | --- | --- | --- | --- |
| Thm 1.1 `thm:main` | Hamiltonian cycle avoiding e | other form | **weaker / different** | both | - | OAI.Barnette.main states Hamiltonicity without the avoided edge; the avoided-edge form is Duality.connected_complement_matching for graphs with an algebraic dual (B1, B5). main is rebuilt unchanged through the project route. |
| Lemma 2.1 `lem:dual` | the dual is a coloured triangulation | other form | **after translation** | upstream | - | translation: B1 (simple T with triangular faces = simple algebraic dual whose vertex stars are triangles) |
| Text `txt:two-faces` | two faces share <= 1 side | other form | **after translation** | upstream | - | translation: B1 (field edge_unique of TriangleSystem) |
| Lemma 2.2 `lem:connected` | faces bounded by cycles => connected | none | **none** | - | - | no plane topology in the Lean; nearest is region_connected for the algebraic region network |
| Eq. (2.3) `eq:counts` | k black, k white, 3k edges, k+2 vertices | other form | **after translation** | upstream | - | translation: B1 (faces of T = vertices of G; Euler as a rank identity) |
| Def. 2.4 `def:selection` | selection | other form | **after translation** | upstream | - | translation: B1 (selection = perfect matching of G) |
| Lemma 2.5(1) `lem:duality.1` | cycle in N => dual disconnected | other form | **after translation** | upstream | - | translation: B1 (cycle of T = flow circuit of D, support a bond) |
| Lemma 2.5(2) `lem:duality.2` | N acyclic => dual connected | other form | **weaker / different** | upstream | - | Lean proves N acyclic => G - N* connected; the spanning-tree clause is not a lemma |
| Prop. 2.6(1) `prop:target.1` | acyclic selection => HC | other form | **after translation** | upstream | - | translation: B1 (matching complement with two edges at each vertex, connected => Hamiltonian cycle) |
| Prop. 2.6(2) `prop:target.2` | two induced trees | none | **none** | - | - | two induced trees are not stated; the Lean glues matchings instead |
| Def. 3.2 `def:state` | state | exact | **exact** | upstream | - | same proposition under the definitions of states and pairs |
| Def. 3.4 `def:good` | good state | other form | **weaker / different** | upstream | - | the Lean never defines one root per component; it uses the second state of a pair with acyclic Q_s (B4). Acyclic Q_s alone is not equivalent (checker: hexagonal prism) |
| Lemma 3.5 `lem:good` | good <=> S_s spanning tree | other form | **weaker / different** | upstream | - | only the direction pair with acyclic Q_s => S_s acyclic; the converse and the spanning-tree iff are absent |
| Lemma 3.6 `lem:Y` | tree Y_s and selection P_s | other form | **weaker / different** | both | `perfectMatching_unique` (TreeMatching:20) | Y_s spanning tree and SOME perfect matching by Hall (upstream); uniqueness of a forest perfect matching is now checked (project), but the rooted rule defining P_s and its identification with the Hall matching are not |
| Lemma 3.7 `lem:outdegree` | outdegree <= 1 | none | **weaker / different** | added here | `card_edgeSet_add_sinks` (Outdegree:65), `component_count` (Outdegree:81) | component_count gives |E| + sinks = q, at most one sink, tree with one sink, one cycle with none, for one finite connected graph; the first sentence (every cycle is directed, T4) is missing and the lemma is not applied to Q_s (T3) |
| Text `txt:inside` | inside of a cycle (R_Z) | other form | **after translation** | upstream | - | translation: B1 (inside of Z = root-free shore A of the bond cut(A) = Z) |
| Lemma 3.8 `lem:disk` | disk identity | other form | **after translation** | upstream | - | translation: B1 (|cut A| = 2|blackCut A| + 3; W >= 1) |
| Prop. 3.9 `prop:recover` | P_s acyclic | other form | **after translation** | upstream | - | translation: B1; Lean proves it for every perfect matching compatible with s, which is stronger |
| Def. 4.1 `def:pair` | pair | exact | **exact** | upstream | - | same proposition under the definitions of states and pairs |
| Lemma 4.2 `lem:partner` | partner orients Q_s | other form | **weaker / different** | upstream | - | partner_orientation directs cycles of Q_s; one root per component (B4) and uniqueness of the partner of a good state are not formalised |
| Text `txt:D` | D(r,s) = disjoint cycles | other form | **after translation** | upstream | - | translation: cycles of D(r,s) = orbits of the permutation next = r^-1 o s |
| Lemma 4.3 `lem:reversals` | two reversals | exact | **exact** | upstream | - | same proposition under the definitions of states and pairs |
| Text `txt:delta` | delta, delta-sum = -/+3 | other form | **after translation** | upstream | - | translation: B1 (delta = indexDelta of the stored cyclic order; counterclockwise = delta-sum -3) |
| Lemma 4.4 `lem:sign` | sign = product of local signs | none | **after translation** | added here | `paperSign_reverse` (LocalSign:127), `sign_orient` (LocalSign:200), `sign_formula` (LocalSign:270), `sign_formula_concrete` (Concrete:48) | translation: B1 only for the word counterclockwise: Lean counts cycles of D with delta-sum -3 (ccwCount). Both reversals and the closed formula are proved for the concrete system with no further hypothesis |
| Lemma 4.5 `lem:cancel` | cancellation | other form | **weaker / different** | added here | `paperSign_partners_sum` (LocalSign:155), `sum_sign_eq_zero_of_no_good` (RealSign:47) | first sentence proved with the real sign; second sentence only in the case where no pair has acyclic Q_s (total sum zero), which is what the existence proof by contradiction uses. The equality with a sum over good states and their unique partners is not stated |
| Text `txt:heights` | heights along face paths | other form | **weaker / different** | upstream | - | face-path heights are not defined in Lean; the Lean uses the potentials of a flow with boundary whiteCharge (B3, T2) |
| Lemma 4.6 `lem:height` | height jump = white faces inside | other form | **weaker / different** | both | `weight_orient` (RealSign:77) | additivity of reversals for arbitrary local weights (project) and slope = number of white faces inside for flow weights (upstream whiteCharge_cut_integral); the per-white-face jump of 0 or 1 and the face-path heights are absent (B3) |
| Lemma 4.7 `lem:difference` | finite difference | none | **exact** | added here | `finite_difference_fin` (FiniteDifference:82), `finite_difference` (FiniteDifference:50) | stronger: any commutative ring, any finite index set |
| Prop. 4.8 `prop:good` | a pair gives a good state | other form | **after translation** | both | `forest_pair_real` (Concrete:65), `forest_pair_of_disk_circulation_real` (RealSign:262), `realSum_ne_zero` (RealSign:219) | translation: B4 (conclusion is a pair whose Q_s is acyclic, not "a good state"); the proof by eps * omega^m and finite differences is checked with the Lean flow weights in place of heights (B3), and m is the minimum over class representatives (T1) |
| Text `txt:flow` | capacity => pair (max-flow) | exact | **exact** | upstream | - | same proposition under the definitions of states and pairs |
| Eq. (5.1) `eq:hall` | capacity condition | other form | **after translation** | upstream | - | translation: B1 (capacity condition in the incidence network) |
| Prop. 5.2 `prop:pair` | no separating triangle => pair | other form | **after translation** | upstream | - | translation: B1 (no separating triangle = TrivialThreeCuts) |
| Lemma 6.1 `lem:cap` | caps | other form | **after translation** | upstream | - | translation: B1 (piece = contraction G/A^c; dual from Duality.minor) |
| Thm 6.2 `thm:T` | acyclic selection containing e0 | other form | **after translation** | upstream | - | translation: B1 (acyclic selection containing e0 = perfect matching containing e with G - P connected); the Lean proof glues matchings, not acyclic selections through Prop. 2.6(2) |

## Off the route

| statement | content | v1 status | new status | Lean origin | project declarations | reason |
| --- | --- | --- | --- | --- | --- | --- |
| Lemma 3.1 `lem:selections-give-states` | HC => state | none | **none** | - | - | no map from Hamiltonian cycles back to states |
| Remark 4.10 `rem:other-sums` | other sums | none | **weaker / different** | added here | `sign_eq_I_pow_mul_phase_concrete` (Concrete:57), `phase_eq_paperSign` (LocalSign:303) | the identity i^J = i^-n eps is checked for every pair (B2 closed); the Taylor-coefficient, Laurent-polynomial and Li statements are not |
| Remark Sec 7 `rem:which` | which HCs arise | none | **weaker / different** | added here | `perfectMatching_unique` (TreeMatching:20) | only "a tree has at most one perfect matching"; the image characterisation and injectivity are not stated (TODO T5 as first written was false) |
| Remark Sec 7 `rem:poly` | polynomial F(w) | none | **weaker / different** | upstream | - | group_sum_product is the factorisation with the phase after w = 1 + aX; the multivariate statement is not formalised |
