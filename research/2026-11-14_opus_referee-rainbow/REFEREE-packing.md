# Referee report on the two-tree packing (Opus)

Referee: Opus 5.5, 2026-11-14, a fresh instance of the author's model, so I tried to be harder on it than on the other file. Refereed: `research/2026-11-14_opus_two-tree-packing/PROOFS.md` and `PACKING.md`. I did not run or read the author's code. All numbers come from `code/check_packing.py` (mine). Notation: `research/BRIEF.md`; `W` is the white-face graph, `u` a deleted-corner map (one corner `u(t)` of each `t ∈ A`), `F_u` its support (the `2n` spokes `(t, v)`, `v ≠ u(t)`), `j_t(U) = |V(t) ∩ U|`, `ρ(U) = |U ∩ R|`.

## The cited theorems, located

The author cited four results from memory. Here is what each says in a source I opened in this session.

| Cited as | Exact statement found | Source opened | Hypotheses of each use |
| --- | --- | --- | --- |
| (L2) Nash-Williams 1964 | "Let G = (V, E) be a graph and let k ≥ 0. Show that E can be partitioned into k forests if and only if each nonempty subset W of V contains at most k(\|W\| - 1) edges of G." (Nash-Williams [1964]) | Schrijver, *A Course in Combinatorial Optimization*, CWI, March 23, 2017, Exercise 10.29, derived there from Exercise 10.28 (Edmonds' covering theorem: a matroid is covered by k independent sets iff `\|U\| <= k r(U)` for all `U`, Edmonds [1965b]) | Used on multigraphs (`M_u` has parallel spokes, `W` and `T/R` have parallel edges). The covering theorem 10.28 is stated for any matroid, and the cycle matroid of a multigraph is a matroid, so the multigraph form holds; the passage from `|U| <= k r(U)` for edge sets to the vertex-set form is the same for multigraphs (it suffices to test edge sets that are the full edge sets of the vertex sets of their components). Loops: none occur (checked in each use below). Satisfied |
| (L3) Rado 1942 | "(X1, ..., Xm) has an independent transversal if and only if the rank of the union of any t sets among X1, ..., Xm is at least t, for any t ≥ 0." | same, Exercise 10.26 | Satisfied in Cor 3.2 |
| Edmonds 1973, disjoint branchings | "the minimum size of an r-cut is equal to the maximum number of pairwise disjoint r-arborescences", where an r-arborescence is a set of `\|V\| - 1` arcs forming a spanning tree with every `v ≠ r` entered by exactly one arc, and an r-cut is `δ^in(U)` for nonempty `U ⊆ V \ {r}` | Schrijver, *Polyhedral combinatorics*, Handbook of Combinatorics ch. 30, Application 5.6 (p. 1674) and the paragraph after Application 6.19 (pp. 1685-1686), attributing it to Edmonds (1973), "Edge-disjoint branchings", in *Combinatorial Algorithms*, ed. Rustin, Academic Press, pp. 91-96. Text at `research/2026-11-14_sol_machinery-literature/source-text/schrijver-matroid-intersection.txt` | The author cites "Algorithmics Press"; the bibliography of the handbook says Academic Press, New York. Fix the publisher. Theorem 3.3 needs the in-arborescence form, obtained by reversing all arcs: r-cuts become `δ^out(Y)`. Parallel arcs are allowed in the handbook's digraphs. Satisfied |
| Schnyder 1989; de Fraysseix and Ossona de Mendez 2001 | not located verbatim in this session | `research/2026-11-14_sol_machinery-literature/source-text/fps-bipolar.txt` exists in the project; I did not have time to locate the statement there | PROOFS Prop 4.2 uses them only in a remark tagged LIT and a HUNCH. Nothing downstream depends on it. Leave as "cited from memory" |

## Lemma 1.2 (extended density)

**Statement.** If no separating triangle has black inner boundary, then for every nonempty `U ⊆ V(T)`, `e(U) - b(U) + max(0, ρ(U) - 1) <= 2|U| - 2`.

**Line-by-line.**

- Lemma 1.1, the Euler identity. I re-derived `m - b - (2p - 4) = (1/2) Σ_F (β(F) - d(F) + 4)` from Euler and the side count, using `Σ_F β(F) = w - b` (equal numbers of black and white faces). The bounds `β <= d - 4` for `d >= 4` and `β = ±1` for `d = 3` follow from parity, `3 | 3β` and `|3β| <= d`. Correct.
- The identification of `b` in Lemma 1.1 (actual black faces of `K`) with `b` in Lemma 1.2 (black faces of `T` with all corners in `K`): a black face with corners in `K` has its three sides in `K` (induced) and its open disk contains nothing of `T`, so it is a face of `K`. The text uses this silently. Fine.
- Reduction to components: edges and black faces with corners in `U` live in one component; the roots in `U` are pairwise adjacent, so in one component; `Σ_K (2p_K - 2) <= 2|U| - 2`. Correct.
- `p <= 3`: the case list is complete. The point to check is a triangle with three roots, which must be `t0`, a black face, so a non-face triangle has `ρ <= 2`. Correct.
- `p >= 4`: a region with `d = 3` is bounded by a 3-cycle (a closed walk of length 3 in a simple graph is a triangle, and for a connected plane graph a face whose boundary walk is a simple cycle is one side of it). It contains a vertex of `T`, else it would be a face of `T`. `K` has a vertex on the other side. So it is a separating triangle, and if the region misses `t0` the hypothesis gives `β = -1`, contribution 0. At most one region contains `t0`. Correct.
- The final case split on `ρ_K`: if `ρ_K = 3`, `t0` is an actual face, so `ε = 0`. Correct.

**Verdict: CORRECT.**

**COMPUTED (mine).** `check_packing.py L12` over every nonempty `U ⊆ V(T)` (all `2^V - 1` sets, numpy), every rooting, `V <= 14`: results in `data/L12_6_14.json`. The inequality holds in all 880 rootings without a black-inner separating triangle, with minimum slack 0, and fails in all 308 rootings with one (minimum slack -1, or -2 in 18 rootings with two such triangles). The special case (3.2), `U ⊇ R`, has minimum slack 0 in all 880.

## Theorem 2.1 (two spanning trees of `W` from any deleted-corner map)

**Statement.** Under the hypothesis, for every `u` the `2n` edges `F_u*` of `W` split into two spanning trees of `W`.

**Check.** `M_u` has `6 + 2n + 2n = 2(|V(H)| - 1)` edges. The reduction of the Nash-Williams condition on `Z = U ∪ C` to `Σ_t max(0, μ_t(U) - 2) <= 2|U| - 2` is right: for fixed `U` the worst `C` takes exactly the centres with `μ_t > 2`; the case `U = ∅` is trivial. The table of terms against shortfalls is right (I recomputed each row). The identity `e(U) - b(U) = Σ_{black t} max(0, j_t - 1)`, which the proof uses without proof, holds because every edge of `T` lies in exactly one black face and a black face with `j` corners in `U` has 3, 1, 0, 0 sides inside for `j = 3, 2, 1, 0`. Step 2 (two forests with `2(|V| - 1)` edges are spanning trees, and parallel copies split) and Step 3 (tree-cotree in `H`, whose dual is `W`) are correct. `M_u` has no loops. **CORRECT.**

**Proposition 2.2** (converse inside the proof): correct.

**COMPUTED (mine), a different route.** I check the conclusion directly on `W`, not on `M_u`: Nash-Williams' condition with `k = 2` for the multigraph `F_u*` on the white faces, over all subsets, plus an explicit split by my own matroid intersection, re-verified as two spanning trees. All rootings `V <= 14`: every one of the 932 pair supports and all 8,800 random maps in rootings with a pair split (`data/PACK_6_14.log`).

## Proposition 2.3 (the hypothesis is needed) and Remark 2.4

**Statement.** If `Δ` is a separating triangle with black inner boundary and `u(t_i) ∈ V(Δ)` for the three inner faces `t_i` along its sides, then `F_u*` does not split.

**Check.** `U` = the closed outer side. `T[U]` is the outer disk (no chord inside `Δ`, by simplicity), one region with `d = 3`, `β = 1`, so `e(U) - b(U) = 2|U| - 3`. The faces with `j = 2` are exactly `t_1, t_2, t_3`, and they are distinct (a face along two sides of `Δ` would be `Δ`). The left side of (2.2) is `(e - b - 2) + 4 = 2|U| - 1`. **CORRECT.** Remark 2.4 (Hall count `2I - 1 < 2I`) is correct; it implicitly needs `I >= 2`, which holds because `I = 1` would give a vertex of degree 3.

**COMPUTED (mine).** 1,212 maps of this form over all rootings with a black-inner triangle, `V <= 14`: none splits, on the `W` side and on the `T/R` side. The author's "only if" (a random map in such a rooting fails only if it has this pattern on some black-inner triangle) holds on all 3,260 random maps I drew there (1,093 fail, all with the pattern; 2,167 split, none with it). It stays COMPUTED.

## Theorems 2.5, 2.7 and Corollary 2.6

- **2.5** (box in the tree polytope): correct. The product of the triangles `{y ∈ [0, 1/2]^3, Σ y = 1}` has the points `(1/2) 1_{F_u}` as vertices.
- **2.6** (`W` minus the triangle of `t0` is three spanning trees): correct as derived. COMPUTED (mine): Nash-Williams with `k = 3` holds in all rootings `V <= 14`, with a pair (880) and without one (326). So the hypothesis is not needed in this range. The author says the same and has no proof; neither do I. Note on the comparison with Schnyder in PACKING.md: Schnyder's three trees each span the interior vertices and one outer vertex, they are not spanning trees of `T`. The analogy is loose; say "three trees, each with `n` edges" for `T` and "three spanning trees" for `W`.
- **2.7** (`T/R` side): I rechecked both cases (`ρ ∉ S`, `ρ ∈ S` with `U = (S - ρ) ∪ R`, `|U| = |S| + 2`). The count `Σ_{t ∈ A} max(0, j_t - 1) = e(U) - b(U) - 2` when `R ⊆ U` is right. No loops, since root-root edges are the sides of `t0`. **CORRECT.** COMPUTED (mine): Nash-Williams on `T/R` holds for every pair support and every random map in rootings with a pair, `V <= 14`. In rootings with a black-inner triangle, the `T/R` test and the `W` test failed on exactly the same maps (1,093 + 1,212). That coincidence has a reason: both conditions reduce to the same inequality (2.2) table, as the author says.

## Corollary 3.2 and Theorem 3.3

**Corollary 3.2** (a face-rainbow and a point-rainbow tree inside every pair support, by Rado): correct. The blocks are `n` disjoint 2-sets, a union of `j` blocks has `2j` elements and rank at least `j` because the support is two forests. COMPUTED: both exist in all 932 supports `V <= 14`.

**Theorem 3.3** (every pair support splits into two point-rainbow trees).

- Step 1 is Fable's Theorem S(3), reproved. I checked the orientation argument (each spoke of `H - σ` oriented exactly once; out-degree one except at the centre of `t0`; edge count `2n + 3`). Correct.
- Step 2. A split `F = σ ⊔ σ'` with both halves rainbow is a partition of the arcs of `G_u` into two sets, each with one out-arc per non-root and acyclic. After merging the roots into `ρ`, each set is a spanning in-arborescence to `ρ`. Conversely two arc-disjoint in-arborescences have `2n` arcs, hence use all arcs, and each takes one out-arc at each non-root. Since the two out-arcs of `x` come from its two spokes, this is a split. Correct. Edmonds, in-form: `k` disjoint in-arborescences to `ρ` iff `|δ^out(Y)| >= k` for every nonempty `Y ⊆ V \ {ρ}`. Correct use.
- Step 3. Arcs inside `Y` from face `t`: `[u(t) ∈ Y]·|(V(t) - u(t)) ∩ Y| <= max(0, j_t - 1)`. Then Lemma 1.2 with `ρ(Y) = 0`. Correct.

**Verdict: CORRECT.** COMPUTED (mine): brute force over all `2^n` splits of every pair support, `V <= 14`: a split into two rainbow trees exists in all 932.

## The `V = 16` support with no good state

**Claim.** Some pair support contains no good state: `V = 16`, plantri index 27, outer face 0 in the author's numbering.

**CORRECT (COMPUTED, mine).** `check_packing.py BAD 16 16 27` enumerates all 2-factors of `B` in every rooting of plantri index 27 at `V = 16` and all `2^c` states inside each. Of 42 pair supports, exactly one contains no good state: outer face `{0, 1, 2}` (face 0 in my numbering as well), a cover with `c = 1`. Output `data/BAD_16_16_27.json`, with the deleted-corner map.

## Smaller remarks

- PROOFS (L4) cites "the pair criterion PROVED-HERE in the graph-theory folder and refereed". Theorem 2.1 is stated under "no black-inner triangle, equivalently a pair exists". Only the hypothesis "no black-inner triangle" is used in the proofs, so the equivalence is never needed. With Fable's Theorem R plus Theorem S, the equivalence now also has a second proof.
- PACKING.md says the packing route "is closed as a route to the key lemma". The argument for this (the statement holds for all `3^n` maps `u`, so it cannot distinguish good pairs) is sound as a heuristic. It is not a theorem that no extension works, and should be labelled as a judgement.
- PROOFS §3 "What is left": "a common transversal is one of the `2^c` alternating halves": correct, since choosing one point per face and one face per point inside a 2-factor is a perfect matching of the 2-factor, i.e. one of the two perfect matchings of each cycle.

## Dependency table

| ID | Claim | Needed by | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- |
| P1 | Lemma 1.1 | P2, P5 | algebraic/logical step | Euler, side count | discharged |
| P2 | Lemma 1.2 | P3, P6, P7 | major claim | P1, component bookkeeping | discharged |
| P3 | Theorem 2.1 | P4, P8 | major claim | P2, Nash-Williams (Schrijver Ex. 10.29 via 10.28, multigraph form), tree-cotree | discharged |
| P4 | Thm 2.5, Cor 2.6 | | algebraic/logical step | P3, Nash-Williams `k = 3` | discharged |
| P5 | Prop 2.3, Remark 2.4 | | algebraic/logical step | P1 | discharged |
| P6 | Theorem 2.7 | | major claim | P2, Nash-Williams on `T/R` | discharged |
| P7 | Theorem 3.3 | | major claim | P2, Theorem S(3), Edmonds (Schrijver handbook pp. 1674, 1685-1686) | discharged |
| P8 | Cor 3.1, 3.2 | | algebraic/logical step | P3, Rado (Schrijver Ex. 10.26) | discharged |
| P9 | Prop 4.1, 4.2 | | algebraic/logical step | counting | discharged |
| P10 | Schnyder link | | named theorem | not located | open, not used |

## Verdict

FOLLOWS for Lemma 1.2, Theorem 2.1, Proposition 2.2, Proposition 2.3, Remark 2.4, Theorem 2.5, Corollary 2.6, Theorem 2.7, Corollaries 3.1 and 3.2, Theorem 3.3 and Propositions 4.1 and 4.2. Fixes: the publisher of Edmonds 1973, the Schnyder analogy wording, and "closed as a route" labelled as a judgement. The three theorems the author cited from memory are stated as used, and each application meets its hypotheses. Review state: refereed (1 independent AI referee, this report); human check pending; tier T2.
