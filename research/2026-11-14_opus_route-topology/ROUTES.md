# Topological routes: status, tests, lessons

Predictions were committed before any run, in `PREDICTIONS.md` (commit 13aaac6). All scripts are in `code/topo.py`, and `code/README.md` lists the commands. "V" is the number of vertices of `T`. "Rooted instances" means every plantri Eulerian triangulation of that order with every black outer face, for V ≤ 10 or 12 as stated, and two outer faces (one of each colour class, recoloured) above that.

| # | Route | Status | One-line result |
| --- | --- | --- | --- |
| R1 | Disk identity as Umlaufsatz | PROVED-HERE, COMPUTED | The state is a flat signed-angle structure. Turning equals minus the colour winding, vertex by vertex. Hopf gives ±1. |
| R2 | Disk identity as argument principle / degree | PROVED-HERE, COMPUTED | `sum delta = 3 wind(f∘C) = 3(B-W)` for the folding map or Belyi map. Orientation-free form `W = B + 1`. |
| R3 | Final step as Alexander duality | PROVED-HERE | The complement of the 2-factor retracts onto `P`, so `#cycles = 1 + b1(P)`. |
| R4 | Cancellation as discrete Morse theory | PROVED-HERE, COMPUTED | Q-fibres are Boolean lattices. Forest pairs are the critical cells. `Z(1) = 0` always; the proof uses the graded Euler characteristic. |
| R5 | State lattice and root-polytope ball | LIT, COMPUTED | Connected distributive lattice. Height = signed enclosed white area (no separating triangles). States are facets of a shellable ball. Tree matchings are not order-theoretically special. |
| R6 | Floer support: one spin^c structure decides | PROVED-HERE (conditional on barnette_trees Thm 1.2), COMPUTED | Tree matching exists ⇔ the point-side vector `g` is a hypertree ⇔ `g ∈ supp SFH(S^3 - F_G, L_G)`. The hard direction still needs the cancellation. |
| R7 | Parity / mod 2 | COMPUTED, one sub-guess REFUTED | Tree matchings are even (LIT) and inject into Hamiltonian cycles avoiding `e0*`. The mate involution does not explain the evenness. |
| R8 | Sperner/Tucker on the state complex | HUNCH, not pursued | The state complexes found are contractible (cone, ball), so there is no nontrivial degree to exploit. |
| R9 | Oriented path following (PPAD) | PROVED-HERE per phase, open globally | Each phase of the marked walk is END-OF-LINE. |
| R10 | Nodal lines of eigenvectors | COMPUTED | see below |
| R11 | Cubic differential / spectral cover | HUNCH with an unrun test | `T` is an `A_2` chamber complex. A state picks a sheet of `λ^3 = q` at each black centre. |
| R6′ | Exchange descent from point-rainbow trees | CONJECTURE, COMPUTED 450/450 | Same-colour exchanges with non-increasing black excess reached a tree matching every time (V ≤ 16). |
| R12 | Two-sided degree polytope saturation | CONJECTURE, small evidence | Every lattice point of the hull of two-sided tree degree vectors of `H` was realised in 8 small cases. |

## R1, R2. The disk identity

*Prediction P1–P3 (high confidence): confirmed.*

- `exp_disk`, V ≤ 12, 262 rooted instances, 40 samples each. The colouring is consistent in 262 of 262. In 3264 of 3264 random chosen-edge cycles `W = B + 1`, Euler holds and `±sum delta = 3(B-W)`. The colour winding equals the `delta`-sum in 3264 of 3264. The general formula `B - W = 2m - h + 2` holds in 49,680 of 49,680 (cycle, state) samples.
- `exp_lattice2`: in 17,312 of 17,312 relative cycles of random state pairs, including non-disjoint pairs, `W = B + 1`.

Proofs are in TOPOLOGY.md §1-2. **Lesson.** The disk identity splits into a local identity, "turning = -winding" at every vertex of a chosen-edge path, and a global one, the Umlaufsatz. The state enters only through the local identity, which needs one fact: the outgoing edge at `v` lies in the matched face of `v`. This is the cleanest account I found. It also explains why the identity fails for arbitrary cycles (the local identity fails) and gives the exact correction `2m - h + 2` for them.

## R3. Jordan curve and tree-cotree

TOPOLOGY.md Lemma 3.1. Proof only, no computation needed. It turns the recovery step into "Hamiltonian ⇔ the perfect matching `M = P*` has acyclic dual", with the number of cycles of `G - M` equal to `1 + b1(M*)`. **Lesson.** The two induced trees are the two components of `S^2 \ (Jordan curve)` up to homotopy. Inducedness is automatic.

## R4. Discrete Morse reading of the cancellation

*Prediction (implicit in the brief): the involution is a Morse matching whose critical cells are the forest pairs. Confirmed, but the Euler characteristic it computes is zero.*

`exp_morse`, V ≤ 14: in 445 of 445 states with mates there are `2^k` mates, the `J`-levels are binomial `C(k,i)`, and the signed sum is `[k = 0]`.

**Lesson.** The ungraded count cannot work. Both regroupings are acyclic matchings on the same set, and the `D`-one has no critical cells at all, so `Z(1) = 0` always. Existence comes from the `ω`-grading, which the `Q`-matching preserves and the `D`-matching does not. This is the structural reason the original proof needs the parameter `x`, and Li needs the half-ray marks, which are an `ω`-type refinement. The Forman reading is: tree pairs = gradient vector fields; cyclic pairs = vector fields with closed orbits; cancellation = orbit reversal. A tree matching is a perfect discrete Morse function on the sphere complex `X_H`.

**Open door.** Ask whether `Z(z)` is a Ruelle-Fried type zeta function (Forman, "Combinatorial vector fields and dynamical systems", Math. Z. 1998, defines closed orbits of combinatorial vector fields; I have not opened it) for this family of vector fields twisted by the circulation weights. HUNCH.

## R5. The state space

*Prediction P6: "connected; tree matchings not an interval and not always an antichain; top/bottom are tree matchings in fewer than half of instances." The first two parts were confirmed; the third was wrong.*

- `exp_lattice`, 166 rooted instances, V ≤ 14: connected, acyclic, one source and one sink in all 166 (Hine-Kálmán, confirmed). 135 have tree matchings. In those, the bottom is a tree matching in 107 and the top in 95. The tree matchings form an antichain in 31 instances and an interval in 20. When there are exactly two tree matchings they are typically bottom and top and mates of each other.
- `exp_sepcheck`: height difference = signed enclosed white area in 17,153 of 17,153 sampled pairs without separating triangles, and fails in 629 of 10,352 with separating triangles. **CONJECTURE** (test: larger V): exact for all Eulerian triangulations without separating triangles. One move around an empty white triangle changes both sides by 1 (that much is PROVED-HERE). The general case needs the lattice to be graded by area, which I have not proved.
- `exp_rootpoly`, 498 (instance, colour) cases: the colour-c complement of `Q_s` is a spanning tree of `G_c`, and the map is injective (Tutte/Kálmán, confirmed). Clock moves are always facet adjacencies of the Kálmán-Murakami triangulation, and equal to them in 156 of 498.
- **REFUTED** (my own guess during the run, not in PREDICTIONS.md): "the mate of a tree matching is a tree matching". Holds in 436 of 442 tree matchings and fails in 6, including triangulations without separating triangles (V = 12 plantri index 2 outer 0; V = 14 index 7 outer 0). **Lesson.** The evenness of the tree matchings (barnette_trees Thm 5.2) is a signed-cancellation fact, not a free involution on tree matchings. In the counterexamples one cyclic state `m` with a single 3-cycle in `Q_m` is the common mate of two tree matchings.

**Lesson for routes.** Every natural topology on the state set found here (order complex, root-polytope ball) is contractible, and the tree matchings are not distinguished in it. A fixed-point or degree argument on these spaces has nothing to grip. That closes R8 for now.

## R6. Floer: one spin^c structure decides (PROVED-HERE, conditional)

*Predictions P7 (hypertree position does not characterise tree matchings) and P8 (no pair ⇒ joint target outside the hull) confirmed.*

- `exp_hyper`, 86 rooted instances, V ≤ 12, six hypergraphs each: the state → hypertree map is injective (Kálmán, confirmed). Tree matchings land on extreme points in 1254 of 1260 cases and non-tree states in 906 of 1140: a bias, not a characterisation.
- `exp_degpoly`, 66 rooted instances, V ≤ 10: in the 60 with a pair everything is realised. In the 6 without a pair the black-side vector `f` is a hypertree, the point-side vector `g` is not, and the joint target is outside the hull.
- `exp_rainbow`, rainbow spanning trees in the white-face graph by matroid intersection (equivalent to one-sided hypertree membership by Lemma 2.1 duality), all 826 rooted instances with V ≤ 16: pair ⇔ `g` realisable in 826 of 826. `f` is realisable in all 826. (A first version, `exp_hyperside`, ran matroid intersection directly on `H` and was too slow; it was stopped and is kept only as code.)
- The equivalence then turned out to have a two-line proof of (2)⇒(3) (TOPOLOGY.md Thm 5.4). The conjecture became a theorem conditional on barnette_trees Thm 1.2.

**Meaning.** A tree matching exists iff one specific relative spin^c structure, the vector `g` of "degree minus 2", lies in the support of `SFH` of the complement of the Seifert surface of `L_G`, the special alternating link of the Barnette graph (JKR Thm 1.1). By Kálmán's convexity that is a family of linear inequalities. **What is missing**: an exchange lemma turning a spanning tree with point degrees `g` into one that also has black degrees `f`. The joint problem is a three-matroid intersection, so no general theorem does this. **Lesson.** The Floer dictionary rewrites states and their counts exactly, but the proof's real content, a joint degree condition on one tree, has no single-spin^c meaning beyond Theorem 5.4: the black side was realisable in every computed instance (not proved in general) and the point side decides, but only through the hard direction (3)⇒(1).

**New door.** Find a direct exchange argument: from a rainbow spanning tree for the point colours, reach one that is also rainbow for the black colours, for example by local exchanges that reduce the black-side excess. A proof would give a cancellation-free proof of the key lemma. Test first: is the graph of point-rainbow trees under single exchanges connected, and does it always contain a doubly rainbow tree that is reachable greedily?

First test run (`exp_exchange`, all 450 rooted instances with a pair, V ≤ 16): start from a point-rainbow tree found by matroid intersection. Make random same-colour single exchanges (swap the deleted spoke at one point for another spoke at the same point) that keep a spanning tree, and accept a move if the black excess `Σ_t |#deleted at t - 1|` does not increase. With at most 20 restarts of 400 steps, this reached excess 0, a tree matching, in **450 of 450**. **CONJECTURE R6′**: from every point-rainbow tree, a sequence of same-colour exchanges with non-increasing black excess reaches a tree matching. Next tests: (a) worst-case number of steps and whether strictly decreasing moves always exist (no plateaus); (b) larger V; (c) look for a potential function that makes the descent monotone. A proof would be a cancellation-free, local-search proof of the key lemma, given the two-line Rado-type proof of the point side. Two halves of that are missing: a direct proof that (3) implies (2), and the exchange step.

## R7. Parity and Thomason

*Predictions P4 and P5 confirmed.*

`exp_ham`, 166 rooted instances, V ≤ 14 (the Barnette graphs have up to 24 vertices):

- The recovery map from tree matchings to Hamiltonian cycles avoiding `e0*` is injective in 166 of 166. Its image is exactly the avoiding cycles whose induced state is a tree matching. That is a strict subset in 109 of 166.
- Every avoiding cycle induces a valid state (166 of 166, as proved in TOPOLOGY.md 3.4).
- The number of tree matchings is even in 166 of 166 (LIT: barnette_trees Thm 5.2), and divisible by 4 in 75 of them.
- Thomason's theorem (every edge is on an even number of Hamiltonian cycles) checks in 166 of 166. Total Hamiltonian cycle counts are even in all instances. Since `#avoiding(e) ≡ #total (mod 2)` for any edge of a cubic graph (PROVED-HERE: from Thomason at an endpoint of `e`), the avoiding counts are even too. Whether every Barnette graph has an even number of Hamiltonian cycles: COMPUTED for these instances only. CONJECTURE, not attempted. Note that cubic graphs in general can have an odd number (`K4` has 3).

**Lesson.** Smith/Thomason parity concerns all Hamiltonian cycles, and tree matchings are a structured sub-family with their own sign-balanced parity. The obvious bridge (mate involution) is refuted, so a lollipop-style proof would have to work on Hamiltonian cycles directly, and lollipop arguments need a first cycle to start from.

## R8. Sperner / Tucker on the state complex

HUNCH, not tested beyond R5. The complexes found are contractible, and no labelling made forest pairs "fully labelled" in a way that gives a nonzero count. The sign-balanced count of tree pairs (`Z(1) = 0`) is itself the obstacle: any unweighted degree argument would see zero.

## R9. Oriented path following

PROVED-HERE, conditional on barnette_trees Theorem 5.3. Orienting `α`-edges from `+` to `-` and `β`-edges from `-` to `+` makes the marked-pair graph a disjoint union of directed paths and cycles with poly-time neighbour functions. Each phase is END-OF-LINE. **Open**: merge the restarts (at most `n/3` phases) into one instance to place the search problem in PPAD. A literature check of TFNP placements of "find a Hamiltonian cycle in a Barnette graph" was not done.

## R10. Nodal lines (continuum test)

*Prediction P10: fewer than 5% of eigenvectors give two induced trees.* Confirmed, narrowly. `exp_nodal`, all plantri Eulerian triangulations with V ≤ 14: 17 of 364 eigenvectors without zero entries (4.7%), mostly at high eigenvalues (examples in `data/nodal.json`). The base rate among all 2-colourings with V ≤ 12 is 258 of 19,857 (1.3%). **Lesson.** The induced-tree condition needs the nodal line to visit every face (high frequency) while leaving only two nodal domains (low frequency). Spectral sign patterns do not combine the two. A continuum version would need a different variational principle, such as a function whose zero set is a single curve maximising the number of faces crossed. HUNCH.

## R11. Cubic differential, spectral cover, A_2 buildings

HUNCH. TOPOLOGY.md §6. Test proposed, not run: compare tree-ness across states with equal colour vector `κ_s`. If `κ_s` does not determine tree-ness, the spectral-cover sheet choice alone is not the right invariant.

## R12. Saturation of the two-sided degree polytope

CONJECTURE with small evidence (`exp_degpoly`: 8 instances with `|V(H)| ≤ 12`, every lattice point of the hull of two-sided spanning-tree degree vectors is realised). If saturation held for all `H` from Eulerian triangulations, existence would reduce to an LP feasibility statement. The Section 3 density bound would then be a candidate certificate after all. Test: larger `H` with a smarter enumerator. A bipartite 4-cycle shows no general obstruction (its hull points are all realised), but saturation for general bipartite planar graphs is not known to me.
