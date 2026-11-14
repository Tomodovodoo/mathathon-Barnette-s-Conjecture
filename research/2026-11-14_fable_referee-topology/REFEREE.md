# Referee report on `research/2026-11-14_opus_route-topology/`

Referee: Fable 5.2, 2026-11-14. Refereed files: `REPORT.md`, `TOPOLOGY.md`, `ROUTES.md`, `code/topo.py` (read, not run).

All numerical checks below use my own code in `code/etri.py`, `code/referee.py`, `code/rainbow.py`, `code/exp_rainbow.py` and `code/exp_structure.py`. It shares nothing with `topo.py` or with `workings/barnette_lab`. The rotation systems come straight from plantri's ASCII output. The single exception is `exp_structure.py replicate`, which imports `barnette_lab` only to learn which face that library numbers as `outer`, so that I could rebuild the refereed report's exact instance sets. Commands are in `code/README.md`.

Notation as in `research/BRIEF.md`. "Rooted instance" means a triangulation with a chosen outer face, recoloured so that the outer face is black. "All rootings" means every face in turn.

## Verdicts at a glance

| Claim | Verdict | One line |
| --- | --- | --- |
| (a) angle structure, local turning identity, Gauss-Bonnet, disk identity | CORRECT | Two unstated steps, both supplied below. 6,417 cycles checked from actual corner sums. |
| (b) every chosen-edge disk has `W = B + 1` | CORRECT | Same statement as node C4 of the astra combinatorics referee, which is discharged there. |
| (c) retraction lemma, `#cycles = 1 + b1(P)` | CORRECT | A shorter face-count proof and the standard source (dual rank formula) are below. |
| (d) cancellation as an acyclic matching, `Z(1) = 0` | CORRECT AFTER FIX | Sign slip in the `J` formula, the roots are left unpaired in the Forman reading, and the computed evidence only reaches `k <= 1`. |
| (e) Floer reading | CORRECT as a dictionary | The condition on barnette_trees Thm 1.2 can be dropped for (2) ⇔ (3), see `RAINBOW.md` Theorem R. No Floer theory is used or produced. |
| (f) rainbow criterion on 826 instances | CORRECT | Reproduced on the same 826 and on all 7,868 rootings with `V <= 16`. Now a theorem. |
| (g) the mate of a tree matching need not be a tree matching | CORRECT | Reproduced, and 40 of 3,240 over all rootings with `V <= 14`. |
| (h) lattice height equals signed white area | CORRECT, and the CONJECTURE part is now PROVED-HERE (mine) | The signed area is a winding number, hence additive. |

No claim is WRONG. Nothing in the folder depends on the two fixes in (d).

## (a) The flat structure and the disk identity

**What is claimed** (TOPOLOGY §2). Corner angles in units of `π/3`: `+1` at white corners, `+5` at the matched corner of a face of `A`, `-1` at the other black corners. Then (2.1) every face except `t0` has angle sum `π` and every non-root vertex has total angle `2π`; (2.2) a triangulated disk whose faces all have angle sum `π` satisfies `Σ_int (2π - θ_v) + Σ_bdry (π - θ_v) = 2π`; (2.3) at a vertex `v` of a chosen-edge path the left exterior angle is `(π/3)((δ_in + δ_out)/2 - 3 δ_out)`; (2.4) hence `J = -1` for a counterclockwise chosen-edge cycle and `+1` for a clockwise one.

**Check of each step.**

- 2.1. A non-root of degree `2d` has `d` white corners, one matched corner and `d - 1` other black corners: `d + 5 - (d - 1) = 6`. Faces: `3`, `5 - 1 - 1 = 3`, and `-3` for `t0`. Correct.
- 2.2. With `I` interior and `h` boundary vertices, `V - E + F = 1` and `2E = 3F + h` give `2I + h - F = 2`. The left side of the identity is `π(2I + h - F)`. Correct, and it needs no sign condition on the angles. The hypotheses actually used are: the disk is bounded by a simple cycle, so it has `h` boundary vertices and `h` boundary edges, and every face in it has angle sum `π`.
- 2.3. The faces on the left at `v` alternate in colour between the outgoing and the incoming edge. Their white-minus-black count is `-(δ_in + δ_out)/2`. The matched face of `v` is the black face of the outgoing edge, so it is on the left exactly when `δ_out = +1`, adding 6 units. Hence `θ_left = -(δ_in + δ_out)/2 + 3(1 + δ_out)` and `ε_v = 3 - θ_left`, as claimed. Summing over a closed path, `Σ ε_v = Σδ - 3Σδ = -2Σδ` units, which is `-2πJ`. Correct.
- 2.4. Correct, with two steps that the text does not state.

**Gap 1 (mine, small).** For a clockwise cycle the disk is on the right, while 2.3 measures left angles. The step from "left exterior angles" to "interior angles of the disk" uses `θ_left + θ_right = 2π` at every boundary vertex. That holds because boundary vertices are non-roots and non-roots are flat by 2.1. So flatness is needed on the boundary as well as in the interior. The text only mentions interior vertices.

**Gap 2 (mine, small).** Where the hypotheses of 2.2 come from. The disk is the side of the cycle away from `t0`. So `t0`, the only face with angle sum different from `π`, is outside. The roots lie on `t0`, so no root is strictly inside. No root is on the cycle, because roots have no outgoing chosen edge. Every black face inside is in `A` and has exactly one matched corner. With these four remarks 2.2 applies to the disk and 2.1 gives zero curvature at every interior vertex.

**Two remarks on wording.**

- 2.3 is stated for closed paths that need not be simple. With one chosen edge per face (the setting of Lemma 4.1) every vertex has at most one outgoing edge, so every directed closed path is a simple cycle and the generality is empty. If both edges of the matched face are allowed, the path can backtrack `u -> v -> u`, and then "the faces on the left between the outgoing and incoming edge" is not defined. State 2.3 for simple cycles, or for paths with `w ≠ u` at every vertex.
- "Hopf's Umlaufsatz" is a fair name for the smooth analogue. What the proof uses is the combinatorial Gauss-Bonnet identity 2.2, which is two lines of Euler counting. The manuscript should say so, otherwise a reader looks for a theorem about smooth curves.

**Claim 2.5** (`B - W = 2m - h + 2` for any simple cycle avoiding the roots). Correct. Proof check: the white-minus-black corner count over boundary vertices is `3(W - B)`, since interior vertices contribute zero, so 2.2 reads `3h - 3(W - B) - 6m = 6`.

**COMPUTED (mine).** `referee.py angles 12`, all 262 rootings with `V <= 12`, 80 random states each. For 6,417 chosen-edge cycles I summed the actual corner angles of the faces on the left of the path at every vertex, and separately the corner angles inside the disk. Results: the local formula of 2.3 holds at every vertex of all 6,417 cycles; `Σ ε = -2Σδ` in 6,417; the Gauss-Bonnet sum over the disk equals 6 units in 6,417; `Σδ = -3` on the 3,208 counterclockwise and `+3` on the 3,209 clockwise ones; `W = B + 1` in 6,417. Claim 2.5 holds on 6,372 cycles taken from one state and measured against another, and on 410 vertex links. Output: `data/ref_angles.json`.

Claims 1.2 to 1.4 (colouring, winding, argument principle) I checked by reading only. They follow from the signed side count and I found no error.

## (b) The unoriented form `W = B + 1`

Correct. From `3(B - W) = 2l - h` and the disk identity `2l - h = -3`, valid for both orientations: for a clockwise cycle the `δ`-sum is `h - 2l = 3`.

Comparison with `research/2026-11-14_astra_referee-combinatorics/REFEREE.md`. That referee states the same fact (line 85 and node C4, obligations O10 to O13, status discharged): the count includes all faces of the closed disk, gives `W = B + 1 >= 1`, and includes the case `B = 0`. The two reports agree, and the two derivations are independent of each other: astra's goes through `B = I + l` as in the OpenAI paper, opus's through Gauss-Bonnet. My count above is a third, numerical confirmation.

## (c) The retraction lemma

**Claim** (TOPOLOGY Lemma 3.1). If `P` contains exactly one edge of every face of `T` and `F` is the set of dual edges of `E(T) \ P`, then `S^2 \ F` deformation retracts onto the graph `(V(T), P)`. So `b0(P) = c + 1` and `b1(P) = c - 1`, where `c` is the number of cycles of the 2-factor `F`. Hamiltonian cycles of `G` are exactly the perfect matchings `M` of `G` whose dual edge set is a forest.

**Verdict: CORRECT.** The retraction is well defined. In each face the arc of `F` separates a corner piece from a piece containing the selected edge. A half-edge of an unselected edge is moved along itself to its vertex by both faces that contain it, because an edge is selected in one of its faces iff it is selected in the other. Alexander duality for `c` disjoint circles in `S^2` gives the two Betti numbers. Inducedness follows as stated: an unselected edge crosses one cycle of `F` exactly once, so its ends lie in different components of the complement.

**A shorter proof, without homotopy (mine).** Regard `(V(T), P)` as a plane graph, possibly disconnected. Two faces of `T` lie in the same face of this plane graph iff one can pass from one to the other across edges not in `P`, that is, iff they are in the same component of the dual subgraph `F`. So `c` equals the number of faces of `(V(T), P)`. Euler's formula for a plane graph with `b0` components reads `|V| - |P| + c = 1 + b0`, so `c = 1 + b0 - |V| + |P| = 1 + b1(P)`. The edge count `|P| = k = |V| - 2` then gives `b0 = c + 1`. This is the form to put in the paper. It is the same argument as OpenAI Lemma 2.1, applied to an arbitrary edge set instead of a forest.

**Citation.** The statement is the rank formula of the dual matroid, `r*(Y) = |Y| - r(E) + r(E \ Y)`, together with Whitney's theorem that the cycle matroid of the plane dual is the dual of the cycle matroid. Both are in Oxley, *Matroid Theory*, 2nd ed., chapter 2. I cite this from memory and did not open the book in this session, so the exact proposition numbers must be confirmed before use. The special case `c = 1`, in the form of a partition into two induced trees, is Stein (1971, Theorem 2.2) and Alt, Payne, Schmidt and Wood (2016, Lemma 5), as cited in the OpenAI paper. I did not find the sentence "`c = 1 + b1(M*)`" in a paper, and I did not have time for a proper search. "Folklore, a direct consequence of the dual rank formula" is the honest attribution.

**COMPUTED (mine).** `referee.py retract 14`: 3,300 random perfect matchings of `G` over the 55 triangulations with `V <= 14`, with `c` between 1 and 6. `b0(P) = c + 1` and `b1(P) = c - 1` in all 3,300. In the 822 samples with `c = 1`, an edge is selected iff its ends are in the same component of `P`. Output: `data/ref_retract.json`.

## (d) The cancellation as a discrete Morse matching

**Verdict: CORRECT AFTER FIX.** The structure is right. Three corrections.

**Fix 1 (sign).** TOPOLOGY 4.5 writes `J(r,s) = J_ccw(s) + 2·#{clockwise Q-cycles}`. With the paper's `δ` (black on the left is `+1`) and the orientation `r(t) -> u(t)` of `Q_s`, the correct formula is

    J(r,s) = J_ccw(s) - 2·#{clockwise Q-cycles}.

Reason: a `Q_s`-cycle that is counterclockwise under `r` has `δ`-sum `-3` by Lemma 4.1, and reversing it changes `J` by `(2/3)(-3) = -2` (OpenAI Lemma 5.2). After the reversal the cycle is clockwise. COMPUTED: `referee.py morse 14`, all 1,206 rootings with `V <= 14`. The minus formula holds for all 3,260 states with a mate. The plus formula fails for every one of the 20 states with `k = 1`. The Boolean-lattice statement is unaffected, because the grading is only reversed.

**Fix 2 (the roots in the Forman reading).** "Pair each point `r(t)` with the spoke `(r(t), t)` and each centre `t` with `(t, u(t))`" leaves the three roots unpaired, so they would be three more critical vertices and the claim "the only critical vertex is the centre of `t0`" would be false. Pair each root with its spoke to `t0`. Then `n + n + 3 = 2n + 3` spokes are used, the remaining `n` are the `s`-spokes, and the centre of `t0` is the only critical vertex. The closed V-paths are then the directed `Q_s`-cycles as claimed.

**Fix 3 (wording).** "Barnette's theorem is equivalent to: `X_H` has a perfect discrete Morse function whose upward-paired edges form a perfect matching of `B`" compares two true statements. What is meant, and what is correct, is that the existence of such a Morse function is a restatement of the existence of a tree matching for the given rooted instance.

**What is proved.** For fixed `s` with `k` cycles in `Q_s`, the mates are the `2^k` orientations (barnette_trees Prop. 2.1), `J` drops by 2 for each clockwise cycle, and "reverse the first cycle" is the standard acyclic matching on a Boolean lattice. Its only unmatched cell occurs for `k = 0`, and a state with a mate and `k = 0` is a tree matching. `Z(1) = 0` follows from the `D`-regrouping, in which every group is a product of factors `(1 - 1)`. This last point is already in barnette_trees Theorem 5.2 ("every group vanishes at `z = 1`"), so it is LIT, not new.

**Weak evidence, flagged.** The report's computed support ("445 states with mates, levels binomial") cannot test much. On its 166 instances 442 of those 445 states are tree matchings, so only three states have `k >= 1`. My run over all rootings with `V <= 14` finds 3,260 states with a mate, of which 3,240 have `k = 0` and 20 have `k = 1`. No state with `k >= 2` exists in this range. So the binomial distribution of levels is checked only for `k <= 1`. The claim rests on the proof, which is fine, and not on the computation. Other counts from the same run: `2^k` mates in 3,260 of 3,260; the signed sum over mates is `[k = 0]` in all; `Z(1) = 0` in 1,206 of 1,206 instances; the number of tree pairs is even in all. Output: `data/ref_morse.json`.

## (e) The Floer reading

**The source.** I fetched `arxiv.org/abs/1112.2632` in this session: Juhász, Kálmán, Rasmussen, *Sutured Floer homology and hypergraphs*, one version (12 Dec 2011), journal reference Math. Res. Lett. 19 (2012), no. 6, 1309-1328. For the theorem text I read the dump of that arXiv version stored by the machinery-literature run (`research/2026-11-14_sol_machinery-literature/source-text/juhasz-kalman-rasmussen.txt`). I did not download the PDF again.

Theorem 1.1 there reads: for a plane bipartite graph `G` with colour classes `E, V` and regions `R`, `S(F_G) ≅ Q_(E,R) ≅ -Q_(V,R)`. `S(F_G)` is the support of `SFH(S^3 - F_G, L_G)`, `F_G` is the surface of the median construction, and `Q_(E,R)` is the set of hypertrees of the hypergraph with vertex set `E` whose hyperedges are the regions. A hypertree (their Definition 2.1) is a vector `f` on the hyperedges such that the bipartite graph has a spanning tree with valence `f + 1` at each hyperedge. The first isomorphism is an affine identification of the lattice of relative spin^c structures with a hyperplane in `Z^R`.

**The dictionary, checked.** Take `G` the Barnette graph, `E` its black vertices. The regions of `G` are the vertices of `T`, and `Bip(E, R)` is the spoke graph `H`. A spanning tree `H - S` with one deleted spoke at each non-root and none at the roots has valence `d_x - 1` at non-roots and `d_r` at roots, so its hypertree is `g(x) = d_x - 2`, `g(r) = d_r - 1`. This is the vector `g` of TOPOLOGY 5.4, and it is a function on `R` as JKR require. The dictionary is correct.

**What is proved.**

1. `g ∈ Q_(E,R)` iff a point-rainbow spanning tree of the white faces exists. This is OpenAI Lemma 2.1 (tree and cotree). Correct.
2. (2) ⇒ (3) of Theorem 5.4: a black-inner separating triangle with `I` interior vertices leaves only `I` white faces for `I` colour classes. Correct. One sentence should be added: every white face in the disk has a corner strictly inside, because a face with all three corners on the triangle would be the whole disk.
3. (3) ⇒ (2) is obtained in the report only through barnette_trees Theorem 1.2, that is, through the cancellation. **This detour is unnecessary.** `RAINBOW.md` Theorem R proves (2) ⇔ (3) directly by Rado's theorem and an Euler count. So "PROVED-HERE, conditional on barnette_trees Thm 1.2" can be replaced by "PROVED-HERE" for the equivalence of (2) and (3). The equivalence of (1) and (3) is barnette_trees Theorem 1.2 itself.
4. "`f` realisable in all 826" (the black side) is also a theorem with a three-line proof, `RAINBOW.md` Lemma R2.

**What is analogy.**

- No property of sutured Floer homology enters any argument, and nothing is deduced about Floer homology beyond JKR's own theorem. The sentence "the obstruction to a tree matching is exactly the failure of one spin^c structure to be supported" is true because both sides are equivalent to the triangle criterion. Neither side explains the other.
- "One specific spin^c structure" is specific only after JKR's affine identification, which is fixed up to a translation that the report does not pin down. It also depends on the root face `t0`, since `g` does. The link `L_G` and its Floer homology do not depend on `t0`. So a rooted combinatorial condition is being read off an unrooted invariant: each of the `k` black faces gives its own lattice point `g_{t0}`, and the statement is about that family of points.
- The key lemma needs the black side as well. The Floer group of `L_G` sees only the point side, and the group of the link of `H_w` sees only the black side. The joint condition has no single-link meaning in this dictionary. The report says this itself in "What this does and does not give", and I agree.
- The Lipshitz index remark in 5.3 and the Hosokawa-Torres remark in 4.5 are tagged HUNCH in the report. I leave them as that.

**Verdict.** CORRECT as a dictionary, with claim tags that can be strengthened as in item 3. As a route it adds no leverage. Its real product is the rainbow formulation, which is refereed under (f) and developed in `RAINBOW.md`.

## (f) The rainbow criterion on 826 rooted instances

**Claim.** A point-rainbow spanning tree of the white faces exists iff a pair exists (580 instances with both, 246 with neither), and the face-rainbow tree exists in all 826.

**Verdict: CORRECT, and now a theorem.** `RAINBOW.md` Theorem R and Lemma R2.

**COMPUTED (mine).**

- Same instance set, rebuilt through the lab's face numbering (`exp_structure.py replicate`): 826 instances, 580 with a pair and with a point-rainbow tree, 246 with neither, face-rainbow tree in all 826. See "Reproduction of the exact counts" below.
- All rootings with `V <= 16` (`exp_rainbow.py exist 16`): 7,868 rooted instances, 5,088 with a pair. A point-rainbow tree exists in exactly those 5,088. A pair exists iff no separating triangle has black inner boundary, 7,868 of 7,868. A face-rainbow tree exists in all 7,868. Output: `data/exist_16.json`.
- The Rado condition by brute force (`exp_rainbow.py rado 12`): 57,901 connected vertex sets over 262 rootings; see `RAINBOW.md` §2.

My matroid intersection is a from-scratch augmenting-path implementation in `rainbow.py`. Each returned tree is re-verified by an independent union-find test.

## (g) "The unique mate of a tree matching is a tree matching" is refuted

**Verdict: CORRECT.** The refutation stands.

**COMPUTED (mine).** `referee.py mate 14`, all 1,206 rootings with `V <= 14`: 3,240 tree matchings in 880 instances. For 40 of them, in 20 instances, the unique mate is not a tree matching. All 40 occur in triangulations without separating triangles, and in all 40 the mate has exactly one cycle in its `Q` (`k = 1`). The first example in my enumeration is `V = 12`, plantri index 2, the same triangulation as the report's. Twelve examples with rotation systems are in `data/ref_mate.json`. On the report's own 166 instances I get its numbers exactly: 442 tree matchings, 6 with a mate that is not a tree matching.

The report's explanation is right: evenness of the number of tree matchings is a signed cancellation, not a fixed-point-free involution. The 40 failures come in pairs inside an instance (20 instances, two each), which agrees with "two tree matchings share one mate". I did not check that the cycle of the common mate has length 3.

## (h) State lattice and height

**Claims.** (4.1) Clock moves make the states a connected distributive lattice (LIT, Hine-Kálmán). (4.2) Without separating triangles, the height difference of two states is the signed number of white faces enclosed by their relative cycles. Tagged PROVED for one move, COMPUTED in general, CONJECTURE for all such triangulations.

**Verdict: CORRECT. The conjecture can be closed.**

**Proof of 4.2 (mine, PROVED-HERE).** View states as perfect matchings of the plane bipartite graph `B`, drawn by its spokes. For states `r, s` the 1-chain `s - r` (spokes of `s` directed from centre to point, spokes of `r` reversed) is a cycle. Each relative cycle `C` of `D(r,s)` corresponds to one of its closed curves, obtained by replacing every edge `r(t) -> s(t)` with the route through the centre of `t`. This is the spoke detour of OpenAI §5.3. Sliding an edge across the subdisk of its black triangle crosses no white face, so the spoke curve encloses the same white faces as `C`, with the same orientation. Hence

    Φ(r,s) := Σ_C (-J(C)) · W_in(C) = Σ_{w white} wind(s - r; w),

the sum over white faces of the winding number of the 1-cycle `s - r` around a point of `w`. Winding numbers are additive in the chain, and `(s - r) + (q - s) = q - r`. So `Φ(r,s) + Φ(s,q) = Φ(r,q)` for all states, with or without separating triangles. A clock move is a pair of states whose relative cycle is a single 3-cycle `Δ`, so it changes `Φ` by `±W_in(Δ)`, with the sign given by the direction of rotation. If `T` has no separating triangle then `Δ` is a face. It avoids the roots, so it is not `t0`, and its disk is that face, which is white because `W = B + 1`. So every clock move changes `Φ` by exactly `±1`, and along any path of clock moves from `r` to `s` the number of counterclockwise moves minus the number of clockwise moves equals `Φ(r,s)`. With the connectivity of the move graph (LIT, Hine-Kálmán) this is the claim. ∎

The same argument gives the corrected formula when separating triangles are present: `Φ(r,s)` is the sum over the moves of a path of the signed number of white faces inside each move's triangle. The plain move count then differs from `Φ` exactly when some move turns around a separating triangle, where `W_in > 1`.

**COMPUTED (mine).** `referee.py height 12`, all 262 rootings with `V <= 12`. The move digraph has one source and one sink, is connected and is graded in 262 of 262. In the 170 instances without separating triangles every move has area 1 and height difference equals `Φ` on 5,531 of 5,531 sampled pairs. `Φ` is additive on all 8,685 sampled triples, in both classes. With separating triangles, height difference equals `Φ` on only 2,644 of 3,154 pairs. In 67 of those 92 instances all moves still have area 1. Output: `data/ref_height.json`.

Claims 4.3 and 4.4 (root polytope, position of tree matchings in the lattice) I did not recompute.

## Reproduction of the exact counts

`exp_structure.py replicate` rebuilds the report's instance sets: every face as root up to `V = 12` (respectively `V = 10`), and above that the lab's faces "0 and the first face of the other colour". Output `data/replicate.json`.

| Quantity | Report | My run |
| --- | --- | --- |
| rooted instances, rainbow experiment | 826 | 826 |
| with a pair, and with a point-rainbow tree | 580 and 580 | 580 and 580, agreeing instance by instance |
| without either | 246 | 246 |
| face-rainbow tree exists | 826 | 826 |
| rooted instances, mate experiment | 166 | 166 |
| instances with a tree matching | 135 | 135 |
| states with a mate | 445 | 445 |
| tree matchings | 442 | 442 |
| tree matchings whose mate is not a tree matching | 6 | 6 |

Every number agrees.

## Dependency table (reverse-Lamport format, bounded to the claims refereed)

Accepted primitives: Euler's formula for plane graphs, the signed side count `3(B - W) = 2l - h`, the Jordan curve theorem and Alexander duality for circles in `S^2`, Rado's theorem, barnette_trees Prop. 2.1 and OpenAI Lemma 5.2 (both refereed elsewhere in this project), and the statement of JKR Theorem 1.1.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| A0 | Chosen-edge cycle has `δ`-sum `∓3` | root of (a) | R0: A1, A2, A3, A4, A5 | root | TOPOLOGY Thm 2.4 | discharged |
| A1 | Faces other than `t0` have angle sum `π`; non-roots are flat | A0, A5 | count | algebraic/logical step | TOPOLOGY 2.1 | discharged |
| A2 | Combinatorial Gauss-Bonnet for a disk bounded by a simple cycle | A0 | Euler | algebraic/logical step | TOPOLOGY 2.2 | discharged |
| A3 | Local turning identity at a vertex of a simple chosen-edge cycle | A0 | colour alternation | algebraic/logical step | TOPOLOGY 2.3 | discharged |
| A4 | Disk away from `t0` contains no `t0`, no interior root, no root on the cycle | A2 applied | hypothesis check | side condition | not stated in the text; supplied here (Gap 2) | discharged after fix |
| A5 | Boundary vertices are flat, so left exterior angles convert for clockwise cycles | A0, clockwise case | A1 | side condition | not stated; supplied here (Gap 1) | discharged after fix |
| B0 | `W = B + 1` for every chosen-edge disk | root of (b) | A0, signed side count | algebraic/logical step | TOPOLOGY 2.4; astra referee C4 | discharged |
| C0 | `c = 1 + b1(P)`, `b0(P) = c + 1` | root of (c) | R0: C1, C2. Supplied alternative R1: C3 | root | TOPOLOGY 3.1 | discharged |
| C1 | `S^2 \ F` retracts onto `(V, P)` | C0 via R0 | piecewise retraction | algebraic/logical step | TOPOLOGY 3.1(2), compatibility checked | discharged |
| C2 | Alexander duality for `c` circles | C0 via R0 | | named theorem | standard | discharged |
| C3 | Faces of the plane graph `(V, P)` are the components of `F`; Euler | C0 via R1 | mine | algebraic/logical step | this report | discharged |
| D0 | Fibre over `s` is a Boolean lattice graded by `J`; first-cycle reversal is an acyclic matching; critical cells are tree pairs | root of (d) | D1, D2, D3 | root | TOPOLOGY 4.5 | discharged after fix |
| D1 | `2^k` mates, one per orientation | D0 | | proved earlier | barnette_trees Prop. 2.1 | discharged |
| D2 | `J = J_ccw - 2·#cw` | D0 | OpenAI Lemma 5.2 | algebraic/logical step | sign wrong in the text; corrected here | discharged after fix |
| D3 | `Z(1) = 0` | (d) | `D`-regrouping | proved earlier | barnette_trees Thm 5.2 | discharged |
| D4 | Roots paired with their `t0`-spokes in the vector field | Forman reading | | missing | supplied here (Fix 2) | discharged after fix |
| E0 | Tree matching exists ⇔ `g ∈ supp SFH(S^3 - F_G, L_G)` ⇔ no black-inner separating triangle | root of (e) | E1, E2, E3, E4 | root | TOPOLOGY Thm 5.4 | discharged |
| E1 | `supp SFH ≅ Q_(E,R)` | E0 | | named theorem | JKR Thm 1.1; premises (plane, bipartite, connected) hold for `G` | discharged |
| E2 | `g ∈ Q_(E,R)` ⇔ point-rainbow tree exists | E0 | tree and cotree | proved earlier | OpenAI Lemma 2.1 | discharged |
| E3 | Rainbow tree ⇒ no black-inner triangle | E0 | count | algebraic/logical step | TOPOLOGY 5.4 | discharged |
| E4 | No black-inner triangle ⇒ rainbow tree | E0 | report: via E5. Supplied alternative: Rado and Euler | proved earlier | `RAINBOW.md` Theorem R | discharged, E5 no longer needed for this edge |
| E5 | No black-inner triangle ⇒ tree matching | E0, statement (1) | | proved earlier | barnette_trees Thm 1.2 (the cancellation) | discharged, outside this audit |
| H0 | Height difference = signed white area, no separating triangles | root of (h) | H1, H2, H3 | root | conjecture in the text; proved here | discharged |
| H1 | Signed white area is a sum of winding numbers, hence additive | H0 | spoke detour | algebraic/logical step | this report | discharged |
| H2 | A clock move around a face encloses exactly one white face | H0 | B0 | algebraic/logical step | this report | discharged |
| H3 | Clock moves connect all states | H0 | | named theorem | Hine-Kálmán, arXiv:1808.06091; confirmed on 262 instances | discharged |

## Verdict

FOLLOWS, for every refereed claim, on the routes listed above. Nodes A4, A5, D2 and D4 needed a correction or a missing sentence, each supplied in this report. Node E4 has a new direct route that removes the dependence of claim (e) on the cancellation. Node H0 moves from conjecture to proved. The review state of the folder's PROVED-HERE claims (a) to (e) and (h) can be raised to "refereed (1 independent AI referee; human check pending)". The tier stays T2. The COMPUTED claims (f) and (g) are now confirmed by an independent implementation on a larger range.
