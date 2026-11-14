# Report: topological readings and topological routes

1. PROVED-HERE: the disk identity is Hopf's Umlaufsatz for a flat signed-angle structure defined by the state, together with a vertex-local identity "turning = minus colour winding". Orientation-free form: every chosen-edge disk has `W = B + 1`.
2. PROVED-HERE: the final step is Alexander duality. The complement of the 2-factor retracts onto `P`, so `#cycles = 1 + b1(P)`. The cancellation is an acyclic (cone-collapse) Morse matching whose critical cells are the forest pairs. Its Euler characteristic `Z(1)` is always 0, so the proof needs the graded version.
3. PROVED-HERE (conditional on barnette_trees Thm 1.2), COMPUTED 826/826 with V ≤ 16: a tree matching exists iff one spin^c structure `g` is supported in `SFH` of the Barnette graph's own special alternating link (JKR). Equivalently, iff a "point-rainbow" spanning tree of the white faces exists.
4. CONJECTURE R6′, COMPUTED 450/450 with V ≤ 16: same-colour exchanges from a point-rainbow tree, never increasing the black excess, reach a tree matching. A proof would give a cancellation-free local-search proof of the key lemma.
5. REFUTED: "the mate of a tree matching is a tree matching" (6 failures out of 442). Also refuted, as a prediction: "top and bottom of the clock lattice are rarely tree matchings". The state spaces (lattice, root-polytope ball) are contractible, and tree matchings are not distinguished in them.

## What I set out to do

The brief (Wild routes B, topology) asked for topological readings of each step of the proof and topological proof routes. The five areas were: the disk identity as winding/Gauss-Bonnet/degree, the trinity and Floer dictionary, the Jordan-curve step and parity/fixed-point routes, the topology of the state complex with a Morse reading of the cancellation, and continuum analogues. I read the three papers, the Hine-Kálmán, Juhász-Kálmán-Rasmussen, Kálmán (2013) and Kálmán-Murakami texts already fetched by the machinery-literature run, and the lab code. I committed ten predictions (PREDICTIONS.md) before running 14 experiments (`code/topo.py`, `data/`).

## What was established

- **Disk identity (TOPOLOGY.md §1-2).** `delta` is three times the pullback of the angular cochain under the folding map `f: T -> Δ` given by the vertex 3-colouring. `J` is the colour winding number. `3(B - W) = 2l - h` is the argument principle (degree formula) for the branched cover / Belyi map. A state defines corner angles (white `π/3`; black `-π/3`, plus `2π` at the matched corner) that make every non-root vertex flat. Along a chosen-edge path the turning equals `-2π J`, vertex by vertex, and the Umlaufsatz gives the rotation `±1`. For an arbitrary cycle the same argument gives `B - W = 2m - h + 2`. COMPUTED checks: 3264/3264 and 49,680/49,680 samples, plus 17,312/17,312 relative cycles.
- **Final step (§3).** Lemma 3.1, plus the reformulation "Hamiltonian cycles = perfect matchings of `G` with acyclic dual". The selected-edge acyclicity (OpenAI Lemma 6.2) becomes winding 0 against winding -1. Tree matchings inject into Hamiltonian cycles avoiding `e0*`, as exactly those whose induced state is a tree matching. That is a strict subset in 109 of 166 instances.
- **State space (§4).** Hine-Kálmán's lattice was confirmed (166/166). Height = signed enclosed white area without separating triangles: CONJECTURE, 17,153/17,153. States are facets of Kálmán-Murakami's shellable root-polytope triangulations, one for each colour. `Q_s` is the union of three cotrees. Forman reading: pairs are combinatorial vector fields, tree pairs are gradient fields, and cancellation reverses a closed orbit. A tree matching is a perfect discrete Morse function on the sphere complex `X_H` with prescribed upward edges.
- **Floer dictionary (§5).** `T` and the Barnette graph's trinity `T' = (H, H_w, G)`. States correspond to `SFH` generators of the three links `L_{G_c}` (Kálmán Thm 10.5 with JKR Thm 1.1). Theorem 5.4 is in the summary above. Its new direction, (2)⇒(3), is a two-line Rado-type count.
- **Continuum (§6).** `G` is the dessin of `γ = β^3`. States are systems of distinct representatives of monodromy cycles. The equilateral metric is `|q|^{2/3}` with `q = β*(dz^3/(z^3-1)^2)`. These are HUNCH-level links to spectral covers and `A_2` buildings. Laplacian sign patterns give induced-tree partitions in 4.7% of eigenvectors: enriched over the 1.3% base rate, but no mechanism.
- **Path following (§4.6).** Each phase of the constructive marked walk is END-OF-LINE. It is the oriented analogue of Thomason's lollipop.

## What failed, and why

- The mate involution as the reason tree matchings are even: REFUTED. The evenness is a signed cancellation (`Z(1) = 0`), not a free involution.
- Order-theoretic location of tree matchings: no pattern. They are neither an interval nor an antichain, and the top and bottom are often tree matchings (prediction P6 wrong).
- Sperner/Tucker/degree arguments: every natural state complex found is contractible, and the unweighted signed count is 0. An ungraded topological count cannot see existence. This is the main negative lesson of the run.
- Hypertree-polytope position: a strong bias (tree matchings are extreme points in 1254/1260) but no characterisation.
- The first matroid-intersection script was too slow and was replaced by the rainbow formulation.

## Still open

- A direct proof of Theorem 5.4's (3)⇒(2), a Rado condition for point-rainbow trees, and of Conjecture R6′. Together they would replace the cancellation.
- Whether the height = area formula holds for all triangulations without separating triangles. Whether every Barnette graph has an even number of Hamiltonian cycles (true in all 166 instances; false for cubic graphs in general).
- Whether `Z(z)` is a Ruelle-Fried / Forman zeta function or a Floer-type graded Euler characteristic in a precise sense. Whether "find a Hamiltonian cycle in a Barnette graph" is in PPAD.
- No independent implementation has checked these computations. All COMPUTED claims are T4, unreviewed.

## Three best next steps

1. **Attack Conjecture R6′.** Measure plateaus and step counts at V = 18-20 (plantri gives 1543 triangulations at V = 18). Look for a monotone potential, for example the black excess plus a white-tree distance. Then try to prove that a strictly improving exchange always exists. This is the most promising cancellation-free route found.
2. **Prove (3)⇒(2) of Theorem 5.4 directly** from Kálmán's hypertree inequalities `Σ_{x∈S} g(x) ≤ |N(S)| - c(S)`, by a density argument like OpenAI §3. Combined with step 1, that would be a complete proof.
3. **Referee this folder with another model.** In particular, check Lemma 2.3's local turning identity and Lemma 3.1's retraction by independent code: rotation numbers computed from actual angle sums on non-simple chosen-edge paths, and component counts of `P` against the number of cycles of the 2-factor on random one-edge-per-face selections.

## Leads for others

- For the manuscript (exposition): §2's "turning = -winding, plus Umlaufsatz" is a one-paragraph explanation of where the 3 in the disk identity comes from, and Lemma 3.1 is a one-paragraph account of the recovery step. Both fit the style guide's request to explain why.
- For the graph-theory and constructive routes: the rainbow-spanning-tree formulation (one spoke per point, white duals a tree) and the exchange descent (`exp_exchange`) are concrete algorithms that need no pair and no weights.
- For the dimer/algebra route: the cancellation pattern "two acyclic matchings, one preserving a grading" is the abstract shape that any replacement of the exponential sum must have.

## Files

`TOPOLOGY.md` (accounts and proofs), `ROUTES.md` (routes, status, tests, lessons), `PREDICTIONS.md` (committed before the runs), `code/topo.py` with `code/README.md` (commands and ranges), `data/*.json` (outputs, each carrying its command).
