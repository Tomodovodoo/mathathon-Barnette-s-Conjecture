# Referee report on `2026-11-14_sol_route-probabilistic`: packing and the mean obstruction

Referee: Opus 5.5, 2026-11-14. I read REPORT.md, ROUTES.md, PROOFS.md, EXPERIMENTS.md, PREDICTIONS.md, NEXT-PREDICTION.md, `code/` and `data/` in that folder. All my code is new (`code/tp.py` and the scripts that import it). The lab is used only to decode the folder's face numbering when replaying its saved data. Commands are in `code/README.md`.

Verdict summary.

| Claim (folder location) | Verdict |
| --- | --- |
| Half-pair packing conjecture (ROUTES "Scope", REPORT, NEXT-PREDICTION) | **True; now `PROVED-HERE`** (PROOFS Thm 2.1). Holds for all deleted-corner maps, not only pairs. |
| "Equivalent conjecture: half the two state indicators lie in the tree polytope" | Correct equivalence (Nash-Williams, or integer decomposition of the base polytope). |
| 278 nonvacuous rooted cases, 147 vacuous (EXPERIMENTS "Fractional tests") | **Reproduced exactly** with independent code: 55 cases / 43 nonvacuous (V=6..14, lab face 0), 370 / 235 (V=16, lab faces 0, 1). No failure. |
| 27 explicit two-tree certificates through V=120 (`data/packing.json`) | **All 27 verified** independently: pair valid, coloured edges = pair support, both colour classes spanning trees of my own `W`. |
| "This is the strongest remaining lead" (REPORT) | **Overstated.** The statement does not use that `r, s` are states. It is a planar density fact and cannot distinguish good pairs from bad ones. |
| Conditional consequence: target in the degree projection of the `H`-tree polytope (ROUTES "Scope") | Correct, and now unconditional. It was already known as a corollary of the signed theorem (a tree matching is such a tree); the new content is a sign-free proof for every pair. |
| "Finite positive weights cannot attain the full-H target mean" (PROOFS 2) | **Correct as stated, proof correct.** Its reach is much narrower than the REPORT's framing; see §3. |
| "The separate joint-degree rounding lemma is still missing" | Correct, and sharper than stated: no rounding confined to one pair support can work (§2). |

## 1. The packing conjecture

**Statement** (folder ROUTES): for every rooted instance with a disjoint pair `r, s`, the `2n` white dual spokes selected by `r` or `s` decompose into two spanning trees of `W`.

**Verdict.** True. PROOFS Theorem 2.1 proves it, and more: under the pair criterion (no separating triangle with black inner boundary), the support of **any** map `u: A -> V(T)` with `u(t) ∈ V(t)` packs into two spanning trees of `W`. The proof is Nash-Williams' covering theorem applied to a doubled multigraph on `H`, plus an extension of OpenAI (3.2) to all vertex sets (PROOFS Lemma 1.2). The bijection property of states is never used.

**Independent evidence** (`COMPUTED`, `code/census.py`, every rooting of every plantri Eulerian triangulation, `V <= 17`):

- 21,848 rooted instances, 13,130 with a pair, 14,881 pair supports. All pack.
- 42,978 random deleted-corner maps in instances with a pair. All pack.
- 27,942 random maps in instances without a pair: 9,706 fail (0.35). PROOFS Proposition 2.3 predicts failure with probability `(2/3)^3 = 8/27 ≈ 0.30` per black-inner triangle (each inner face along it deletes one of its two triangle corners with probability 2/3), more when there are several.
- Cross-checks with other folders: 7,868 rootings for `V <= 16`, 5,088 with a pair (graph-theory folder and fable topology referee report the same numbers); `V = 9` has 8 of 14 rootings with a pair (graph-theory Corollary 4.2).
- `code/big.py` (seed 5): the `V = 18` lattice-extreme counterexample (all 4 supports), tubes up to `V = 70`, `tube6_6`, `tube8_4`, `tube10_3` (233 to 300 supports per rooting), a subdivided tube (`V = 50`), prism chains, and random octahedral sums glued into faces of both colours. 136 rooted instances, 2,442 pair supports, 0 failures. On 5,440 random maps the exact failure rule (some black-inner triangle has all three inner faces deleting a triangle corner) agreed with the packing test every time.

**The 278 cases.** `code/referee_sol.py` reproduces the folder's selection of roots through the lab's face numbering and gets 55 cases with 43 nonvacuous (`V = 6..14`, face 0) and 370 with 235 nonvacuous (`V = 16`, faces 0 and 1), the folder's numbers. My census covers all rootings and is a superset.

**The 27 certificates.** Their face numbering comes from embeddings that I cannot reconstruct from the saved edge list, so `referee_sol.py` decodes each black face of the pair as the face of the right colour on the edge `{r(t), s(t)}`, takes the leftover face of that colour as `t0`, and checks: `r, s` is a pair; the 2n coloured spokes are exactly `r ∪ s`; the cherry structure of the saved white ids matches mine; each colour class is a spanning tree of `W` built by my code. All 27 pass (`data/referee_sol.json`).

**Was it the strongest lead?** No. Three facts locate it.

1. It holds for all `3^n` deleted-corner maps, almost none of which are pairs. So it is a statement about the planar density of black faces, not about states.
2. Each one-sided relaxation (face-rainbow tree, point-rainbow tree) follows from it inside every support (PROOFS Cor 3.2, Thm 3.3). The doubly rainbow one, a tree matching, does not: the `V = 16` rooted instance at plantri index 27, my outer face 0 (it has 12 tree matchings, like the folder's "bad cover 16", and is presumably the same instance), has three pair supports, one of which contains no tree matching although it packs.
3. Its proof uses neither the disk identity nor the 3-colouring, which are the two ingredients every proof of the key lemma uses.

## 2. What the conjecture would imply, as the folder states it

ROUTES says: "If proved, this gives fractional target feasibility directly from a pair, without first invoking the forest-pair theorem. The separate joint-degree rounding lemma is still missing." Both sentences are correct. Two sharpenings.

- The rounding cannot be done inside the support of the given pair. The point `(1/2)(1_r + 1_s)` has support `r ∪ s`; any convex combination of tree matchings equal to it would use only tree matchings inside that support, and the bad-cover support has none. So the half-pair point is in the tree polytope and in the LP, but **not** in the convex hull of tree matchings.
- "Pipage, swap or negative-correlation rounding" (ROUTES) preserves marginals; the folder correctly notes it cannot preserve both degree families. Theorem 3.3 shows that preserving one family is free: the support itself splits into two point-rainbow trees, a two-point distribution with the right point degrees and the right mean face degrees.

## 3. The finite-positive-weight mean obstruction (folder PROOFS 2)

**Statement.** For every instance and every assignment of finite strictly positive weights to the spokes of `H`, the weighted uniform spanning tree has `E deg(t0) < 3`. Hence its mean degree vector cannot equal the target `d*` (degree 3 at `t0`, 2 at bounded centres, `deg_H - 1` at nonroots, `deg_H` at roots).

**Proof check.** Correct. Each spoke lies on two distinct faces of `H` (the two white hexagons on either side), so no spoke is a bridge, so every spoke is missed by some spanning tree, which has positive weight. The same argument at the roots is correct.

**What it rules out.** Exactly one thing: a strictly positive measure on **all** spanning trees of `H` (in particular a weighted UST or any exponential family with full support) whose mean degrees equal `d*`. The reason is that `d*` requires every tree to contain the three spokes of `t0` and every root spoke, so `d*` lies on a proper face of the degree polytope.

**What it leaves open.**

- It is a boundary artefact. Every tree with degrees `d*` contains the forced spokes, so one conditions on them (contracts them in `H`, equivalently deletes their duals from `W`). After that the obstruction disappears from the argument; the folder's PROOFS 3 already says "root-spoke conditioning or diverging weights is compulsory".
- In the conditioned problem, mean matching is a convex question, and PROOFS Theorem 2.5 here answers it: the whole box `{face sums 1, 0 <= y <= 1/2}` lies in the tree polytope of `W`, and `(1/2)(1_r + 1_s)` has the target degrees. Whether the target lies in the **relative interior** of the conditioned projection (so that a finite exponential family attains it exactly) is not decided by either folder. `CONJECTURE` (test: for small instances maximise `min_e y_e` over the tree polytope intersected with the degree constraints, restricted to spokes that lie in some tree with degrees `d*`).
- None of this bears on existence. Even an exact mean match is a first-moment statement; the key lemma is that the event `deg = d*` has positive probability. The half-pair point shows that fractional feasibility holds everywhere and gives no information. So the obstruction is not "the reason positive-measure arguments cannot work". The reason first-moment arguments cannot work is the integrality gap of the three-matroid LP: fractional vertices exist (graph-theory ROUTES M1–M4), and a support can carry the target mean exactly while containing no tree matching (§2).

**Recommendation for the route map.** Record the obstruction as `PROVED-HERE`, scope "full-support measures on all of `H`", lesson "condition on forced spokes first". Do not record it as evidence against positive-measure methods in general.

## 4. Minor points

- ROUTES "Scope" says a counterexample must exhibit "a subset S of white vertices with more than 2|S|-2 selected edges internal to S, or an independently checked matroid-union obstruction". By Nash-Williams these are the same thing; `code/tp.py density_witness` produces such a set, and `data/counterexample_nonpair_V9.json` is one for a map that is not a pair (`V = 9`, excess 1 on three white faces).
- NEXT-PREDICTION calls the half-pair point statement "equivalent [to the partition] by the integer matroid-union theorem". Correct; Nash-Williams' theorem is the cleanest citation for graphs.
- EXPERIMENTS, joint M-convexity: not refereed here (outside this brief).
