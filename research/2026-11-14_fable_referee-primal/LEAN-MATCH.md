# STATUS.md against the Lean sources

Reviewer: Claude Fable 5.2, 2026-11-14. Sources opened: the clone at `research/2026-11-14_opus_lean-formalisation/upstream/openai-math`, `git log -1` gives `4eaee87548250b2682affda7d05d947c05554bae`. Files are under `lean/OAI/Combinatorics/Hamiltonian/`. I read each cited declaration in the source file, with the definitions it depends on (`Network`, `Duality`, `cut`, `blackCut`, `regionEdges`, `regionVertices`, `Bond`, `FlowCircuit`, `Simple`, `ThreeEdgeConnected`, `TrivialThreeCuts`, `ColoredDual`, `StateCycle`, `whiteCharge`). I did not rebuild the Lean. The copy at `E:\lbb` was not needed.

Summary.
1. Every line number in STATUS.md is right. Every cited declaration exists with the header printed in the author's LEAN-EXTRACTS.md.
2. No informal lemma claims more than its Lean counterpart on a hypothesis the Lean needs. I found no false "machine-checked" label. Lemma 7 and the sign in Lemma 8 are correctly marked as not machine-checked in this form.
3. Five mismatches, all of scope or of citation, none of substance. They are M1 to M5 below.
4. The largest representational difference is orientation. Lean has no rotation system. The note's Lemma 3 has no single Lean counterpart.
5. Lemma 12 is stated more narrowly than the Lean lemma it cites. The Lean form is the better statement.

## Dictionary

| Note | Lean |
| --- | --- |
| `G`, its vertices, edges | `N : Network V E` (oriented multigraph, `N.graph` its simple graph) |
| faces of `G`, face links | vertices and edges of `D : Network F E`, same edge type `E` |
| planarity | `N.Duality D`: both connected, `ker ∂_N = im ∇_D`, `ker ∂_D = im ∇_N` over the reals |
| cut `∂S`, `E_S`, `U_S` | `N.cut A`, `N.regionEdges A`, `N.regionVertices D A` |
| `ℓ` | `(N.blackCut black A).card` |
| three distinct faces at a vertex, with a cyclic order | `face : ∀ v, D.Triangle (N.star v)`, plus the field `oriented` of `ColoredDual` |
| two faces share at most one edge | `D.Simple` (`dual_simple`) |
| state | `M.State root`, a choice of corner per nonroot black vertex, injective, with range the nonroot faces |
| `δ(f,g)` at `b` | `indexDelta` of the two corner indices in the triangle of `b` |
| `Q_s` | `oppositeGraph s` |
| cut side | the `A` with `root ∉ A` returned by `Duality.circuit_cut` |

`regionVertices D A` is defined through edges (faces incident with an edge that has an end in `A`). The note's `U_S` is defined through vertices. In a cubic graph with three faces at each vertex the two agree.

## Lemma by lemma

| Lemma | Cited declaration | Lean hypotheses | Note hypotheses | Match |
| --- | --- | --- | --- | --- |
| 1 | `ColoredDual.cubic_cards`, Matching.lean:477 | a `ColoredDual` (duality, simple, dual simple, cubic, colouring, triangles) | simple cubic bipartite 3-edge-connected plane | Yes for the counts `\|E\| = 3\|B\|`, `\|V\| = 2\|B\|`. |
| 1 | `ColoredDual.nonroots_card`, BMatching.lean:341 | `ColoredDual`, root black | same | Yes, `\|X\| = \|A\|`. |
| 1 | not cited | `make_coloredDual`, ThreeCuts.lean:101 | Lemma 1, "three distinct faces", "two faces share at most one edge" | See M1. |
| 2(a) | `Duality.circuit_cut`, FlowCircuits.lean:71 | duality, `x` a minimal nonzero flow of `D`, any `root` | face circuit (cyclic list) | One direction only. See M2. |
| 2(a) | `Bond.connected_shore`, Bonds.lean:163 | `N` connected, `A` a bond, `A` and its complement nonempty | bond of `G` | Yes. |
| 2(b) | `region_euler`, DiskRegions.lean:252 | duality, `G[A]` and `G[A^c]` connected, `D` simple, triangles | "connected complementary shores" | Yes. The note states it in the same generality inside its standing hypotheses. |
| 2(b) | `mixed_corner_on_boundary`, StateDisk.lean:129 | duality, `D` simple, triangles, `z` in the region of `A` and of `A^c` | face meeting both shores | Yes. |
| 3 | `cycle_cut_scalar`, StateDisk.lean:416; `blackDelta_cut`, :390 | cycle flow equals `c·∇1_A`; colouring; `cut A` equals the cycle edges | oriented face circuit with cut side | Yes for `c = ±1` and for the summed form of (2.2). See M3 for orientation. |
| 4 | `ColoredDual.pair_nonempty`, BMatching.lean:403 | `ThreeEdgeConnected`, `TrivialThreeCuts`, root black | 3-edge-connected, every 3-edge cut has a singleton shore | Yes, hypothesis by hypothesis. Proofs differ, as STATUS says. |
| 5 | `state_disk_count`, StateDisk.lean:260 | duality, `D` simple, triangles, colouring, `m` injective on nonroot blacks with `m v` a corner of `v` and range the nonroot faces, cycle `C` with `m(blackEndpoint e_i) = C.vertex i` and that endpoint not the root, `root ∉ A`, `cut A = cycleEdges C` | state `r`, chosen links from `r(b)` across an edge at `b`, forming a directed face circuit, `S` its cut side | Yes. This is the fourth count of (4.2). |
| 5 | `disk_boundary_imbalance`, :428 | adds `N` simple, cubic, both shores connected, the state count as a hypothesis | same | Yes, `h = 2ℓ + 3`. |
| 5 | `state_disk_delta`, :442 | as `state_disk_count`, without `A` | same | Yes, `blackDelta = -3c` is `Σδ = -3σ`. |
| 5 | none | | `\|W∩S\| = \|B∩S\| + 1` | Not a Lean declaration. Lean has only `white_positive_of_boundary` (positivity). STATUS says so. |
| 6 | `boundary_of_sum_zero`, Circulation.lean:154 | `N` connected, real `b` with sum zero | integer path flow | Yes, a specialisation. |
| 6 | `whiteCharge_cut_integral`, :208; `white_positive_of_boundary`, :227 | `root ∉ A`, `∂α = whiteCharge`, `x = c·∇1_A`; resp. colouring and `h = 2ℓ+3` | flux through the cut side | Yes. The sign remark in STATUS is right: Lean's `boundary` is inflow, `whiteCharge` is `+1` at white vertices and `-\|W\|` at the root. |
| 6 | `ColoredDual.StateCycle.signed`, ColoredDual.lean:183 | `∂α = whiteCharge` | (4.1) with (5.1) | Yes. `(delta = -3 ∧ slope > 0) ∨ (delta = 3 ∧ slope < 0)` is `Σδ = -3σ`, slope `= σ\|W∩S\|`. |
| 7 | `OppositeCycle.fixed_second_state_cancels`, PairPhases.lean:91 | every partner has `cyclicDelta = ±3` on the cycle; phase `I^(n/3)` | circuit length odd; real sign `∏δ` | Different statement, correctly labelled. See M4. |
| 8 | `TriangleSystem.Pair.forest_pair_of_disk_circulation`, PairPolynomials.lean:423 | a pair exists; `cyclicDelta = ±3` for all opposite cycles and partners; weights with the signed property on all pairs and cycles | a pair exists (Lemmas 5, 6 in context) | Conclusion matches (a pair with `oppositeGraph` acyclic). Proof of nonvanishing differs in the sign, as STATUS says. |
| 9 | `removed_acyclic`, Matching.lean:330; `remainder_connected`, :342; `remainder_black_degree`, :444; `remainder_independent`, :487 | pair `P`, `oppositeGraph P.right` acyclic, a root edge index `i`; root black for the degrees | pair with circuit-free `Q_s` | Yes. Both need the partner. |
| 10 | `tree_matching`, ForestMatching.lean:51; `recovery_matching`, :226 | Lean proves existence by Hall (`hhall`, line 62) | parent edges of white vertices | Yes, the note is constructive and proves the same existence. |
| 11 | `matching_cut_balance`, ForestMatching.lean:176 | simple, cubic, colouring, `P` meets every star once, `cut A ⊆ P` | same | Exact. |
| 12 | `selectNet_forest`, :307; `selected_forest`, :338; `recover_connected_complement`, :375 | any state `s`, any perfect matching `P` whose edge at each nonroot black vertex is incident with `s(t)`; root's matching edge is a root edge | the matching of Lemma 10 | Lean is more general. See M5. |
| 13 | `cap_threeConnected`, ThreeCuts.lean:230; `cap_simple`, :352; `cap_cubic`, :360; `cap_coloring`, :381 | `\|cut A\| = 3`, `2 ≤ \|A\|`, complement nonempty | both shores have at least two vertices | Yes, the note assumes slightly more than each single lemma needs. |
| 13 | `cap_glue_matching`, Gluing.lean:94; `cap_glue_connected`, :167 | two cap matchings that agree on the cut, complements connected | two cap cycles omitting the same cut edge | Yes. |
| 13 | not cited | `cap_duality`, CappedDuality.lean:148 | "contracting a spanning tree … preserves planarity" | See M1. |
| T | `Duality.connected_complement_matching`, Gluing.lean:294 (from `matching_strong`, :244) | duality, simple, cubic, 3-edge-connected, 2-colouring, any edge `e` | Theorem T | Exact, including the quantifier over `e` inside the induction. |
| T | `main`, Main.lean:47 | `MainStatement` (Model.lean:42); 3-vertex-connected to 3-edge-connected by `cut_card_three`, CutSpaces.lean:51 | last paragraph of Section 8 | Yes. |

## Mismatches

**M1. Two Lean declarations that carry planar content are missing from STATUS.** `make_coloredDual` (ThreeCuts.lean:101) builds, from duality, simplicity, 3-edge-connectivity and cubicity, the simple dual, the triangle at each vertex and its orientation. It is the Lean counterpart of the note's Lemma 1 beyond the counts, and of the phrase "oriented rotation system". `cap_duality` (CappedDuality.lean:148) proves that a cap has a dual again. It is the counterpart of one sentence in Lemma 13. STATUS lists neither. The Lemma 1 row says face simplicity "is interpreted through the plane embedding, rather than the Lean network", which is true of the note and silent about where Lean does that work. Fix for STATUS: add both declarations, with the remark that the note replaces them by the accepted facts on facial walks and on contraction.

**M2. `Duality.circuit_cut` is one direction of Lemma 2(a).** It says a minimal flow of `D` is `c·∇1_A` with `cut A` its support and `root ∉ A`. That the cut is a bond is the separate `Duality.bond_of_circuit` (Bonds.lean:109), not cited. The converse, that every bond is a face circuit, is what Lemmas 9 and 12 use ("if `G - L` were disconnected, `L` would contain a bond, hence a face circuit"). Lean does not go through bonds there. `remainder_connected` and `selected_forest` get connectivity from acyclicity in `D` by the duality of kernels (`Forest.lean`, for example `connected_of_kernel_constants`, line 249). So the word "exactly" in Lemma 2(a) is PROVED-HERE in the note and has no single cited Lean counterpart. Fix for STATUS: cite `bond_of_circuit` for the forward direction and say the converse is the note's own.

**M3. Orientation.** Lean has no sphere orientation and no rotation system. The field `ColoredDual.oriented` says that the cyclic order of the corners of the triangle at `v` agrees with `∇_N 1_v` read through `D.arcSign`. It is produced by `oriented_face` from the two signed incidence matrices. The note instead starts from an oriented sphere and proves coherence in Lemma 3. The cited `cycle_cut_scalar` and `blackDelta_cut` are algebra on a cycle flow already known to be `c·∇1_A`. They do not contain the statement that "black end on the left" is coherent around a circuit. The Lean declarations that play that role are `ColoredDual.oriented` and `Triangle.index_delta` (TriangleSystem.lean:291), not cited. This is a difference of representation. Lemma 3 as written is the note's own lemma, tagged PROVED-HERE, and it should not be described as a restatement.

**M4. Lemma 7 and the phase.** With `c₊, c₋` the numbers of positively and negatively oriented circuits of a pair and `c = c₊ + c₋`, the note's sign is `ε = (-1)^{(n+3c)/2}·(-1)^{c₋}` and Lean's phase is `I^{c₋ - c₊}`. Their ratio is `(-1)^{(n+3c)/2}·I^c`. PROVED-HERE, three lines from `Σδ = ∓3` per circuit. It depends on `c`. So the note's `Z` and Lean's polynomial are different sums, not multiples of each other, although both vanish and survive for the same reasons. STATUS handles this honestly. I add the formula so nobody later writes "the same polynomial".

**M5. Lemma 12 is narrower than `selected_forest`.** The Lean hypotheses are a state `s` and any perfect matching `P` whose edge at each nonroot black vertex lies on the face `s` assigns to it. The hypothesis on the root edge is vacuous, since every edge at the root is one of its three. Neither a partner nor acyclicity of `Q_s` appears. The note's proof of Lemma 12 uses exactly these hypotheses and no more, but the statement says "the matching from Lemma 10". COMPUTED (`code/check_lemmas.py`, 6 to 14 faces): for every perfect matching and every root, a compatible state exists exactly when the complement is connected. The forward direction is the general lemma. The converse is an observation in this range, tagged COMPUTED only.

## What I did not check

I did not rebuild the Lean and did not re-derive that the cited proofs compile. I rely on the build log reported in `research/2026-11-14_opus_lean-formalisation/REPORT.md` for that. I compared statements, not proof scripts, except where a hypothesis could only be understood from the proof (`cap_duality`, `make_coloredDual`, `tree_matching`).
