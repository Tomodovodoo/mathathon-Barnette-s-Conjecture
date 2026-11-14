# Report: an inductive route to the tree matching

Opus 5.5, 2026-11-14, folder `research/2026-11-14_opus_route-induction/`.

**Summary.**
1. Induction by degree-4 contraction (Batagelj's Q-operation reversed) reduces Prop. 5.1 to two statements: (G) a contraction keeping a pair exists, and (L) the contraction inequality `#TM(T) >= #TM(T/M)`. (G) holds on all 7,386 rooted instances with `8 <= V <= 17` and no separating triangle. (L) holds on all 344,872 rooted contractions with `V <= 17` (`COMPUTED`).
2. `PROVED-HERE`: states split exactly over the two contractions at a degree-4 vertex. I also proved the correct lift criterion, and a three-face rotation that turns a failing lift into a tree matching of the other type. Together they inject all but 466 of 28,189 failing cases (`V <= 16`) into the tree matchings of `T`.
3. `REFUTED`: the "only if" half of route-graph-theory Lemma 6.2(iii) (simple counterexample at `V = 11`). Every local induction hypothesis I tested is also refuted: prescribed corner, prescribed `Q`-edge, local split condition, monotone lowest coefficient, `TM` skein relation. All thirteen refuted schemes, with smallest examples, are in `data/failed_inductions.json`.
4. `PROVED-HERE`: the number of tree matchings is even and their signs balance (`F(1) = 0`). So a counting induction is the natural form, not "at least one".
5. Open: a second local rule for the 1.7% exceptional case `b ∈ K2'`, and a proof of (G).

## What I set out to do

Fill the empty "inductive" cell of the route map. Collect the generation theorems for Eulerian triangulations, measure how each reduction acts on states, pairs, tree matchings, `c_min` and the signed polynomial, search for a hypothesis that survives the inductive step, try to prove the contraction inequality by an injection, and fit skein relations.

## What I established

- **Generation (`LIT`).** The plantri 4.5 source generates all 3-connected Eulerian triangulations from the octahedron by Batagelj's P- and Q-operations. Drápal (CMUC 2009, p. 477) states the same. Drápal and Lisoněk (Discrete Math. 310, 2010) reduce this to one operation starting from even double wheels (abstract only). Batagelj 1989, Brinkmann-McKay 2007 and Matsumoto-Nakamoto 2014 were not opened. INDUCTION.md §1 gives the exact citations and what each opened source says.
- **Own code, validated.** `code/tri.py` agrees with `workings/barnette_lab` on 438 rooted instances. It handles multigraph contractions.
- **Proofs (`PROVED-HERE`, PROOFS.md).** Prop. 1.1: `#states(T) = #states(T/M) + #states(T/N)`, by four types of states at `x`. Prop. 2.1: the lift `s` of `s'` is a TM iff `split(tau') + a v1` is a spanning tree of `T - x`, and if `s'` is a TM this reduces to `a ∈ K2`. Lemma 3.1 and Prop. 3.2: a failing lift has `s(g) = a`, and rotating `x, v2, a` around the white face `{x, v2, a}` gives an `N`-type TM unless `b ∈ K2'`. Cor. 3.3: `#TM(T) >= #TM(T/M) - E`. Prop. 4.1: tree matchings come in sign-balanced pairs.
- **Computations (`COMPUTED`).** The contraction inequality and monotonicity of states, pairs and `D` hold on 344,872 contractions (`V <= 17`). `C >= b` also holds there: there are always enough tree matchings of the other type to absorb the failing lifts. The P-reduction inequality holds on 58,593 reductions (`V <= 17`). Octahedron insertion doubles `#TM` in a white face and kills the pair in a black one.

## What failed, and why

Everything that prescribes something local failed, and it failed early.

- A TM with a prescribed corner at a prescribed face exists in only 20 of 13,130 rooted instances (`V <= 17`) (`V = 8` first). Same for the mate and for a prescribed `Q`-edge.
- A TM satisfying the one-edge local lift condition fails at `V = 10`.
- The lowest coefficient `lc` of the refereed polynomial is not monotone (`V = 14`), because expansion can lower `c_min` and the lowest degree jumps.
- `#TM(T) = #TM(T/M) + #TM(T/N)` fails both ways, because pairs mix the two contraction types. Only the state count obeys deletion-contraction.
- Contraction can destroy the pair (simple from `V = 11`), so the contraction has to be chosen. Without separating triangles a good choice always existed in the census. With separating triangles it may not (`V = 9`), and gluing has to take over.
- The rotation fails when `b` sits in the `v2`-part of the split tree. First root-free case: `V = 14`.

The common lesson: the tree condition is global. The only local handle I found works on a counted family (tree matchings of the other type), not on a single prescribed witness.

## What is still open

- (L) in full: an injection `TM(T/M) -> TM(T)` covering the case `b ∈ K2'`. Data say an injection exists in every case up to `V = 17`, and short moves (at most 3 faces) cover 483 of 487 root-free instances with failures at `V = 14`.
- (G): a proof that some degree-4 contraction keeps a pair when there is no separating triangle. A new black-inner separating triangle through the merged vertex `v` comes from a 5-cycle `x v1 y z v2` of `T`. A counting argument over the degree-4 vertices may work.
- The induction on `c_min` and along 4-cuts (task 5): not done beyond two observations (INDUCTION.md §6).
- The `S`-step (gluing) uses route-categorical Prop. 6, which I re-checked only for octahedron insertions.

## Three best next steps

1. **Find the second rule.** Take the exceptional cases from `code/rho.py` (466 for `V <= 16`; first root-free one at `V = 14`, graph #12). Following the path from `b` to `v2` in `K2`, look for a longer rotation along that path (a chain of the same three-face move) that lands in type `(x, b)` or `(a, x)`. If it always works, (L) is proved, and with (G) and Prop. 6 the induction gives a second, sign-free proof of Prop. 5.1.
2. **Prove (G)** using route-graph-theory's Euler identity (its Lemma 2.2). A black-inner triangle created by merging `v1, v2` is a short cycle through `x`. Show that two degree-4 vertices cannot both be blocked. E2 takes about a minute at `V = 17`, so extend it to `V = 18, 19` first.
3. **Use Prop. 1.1 and Prop. 4.1 in the exposition.** "States obey deletion-contraction, tree matchings come in sign-balanced pairs" is a short explanation of why the count `#TM` is the right inductive quantity, and why `#TM >= 2` whenever a pair exists.

## Leads for others

- **For route-graph-theory and the referees.** Lemma 6.2(iii) of `research/2026-11-14_opus_route-graph-theory/PROOFS.md` needs the correction in PROOFS.md §2 here. Its `COMPUTED` claim "when `T'` has a TM, some TM of `T` projects to one" is consistent with my data. The "iff" in (iii) is not.
- **For the constructive agents.** Lift-or-rotate is a polynomial step from a TM of `T/M` to a TM of `T` in 98.3% of the failing cases. Combined with the Batagelj reductions it gives a fast heuristic construction, worth benchmarking against the marked walk.
- **For the exposition.** `lc = sum over D with c_min cycles of prod_C (white faces inside C)` is an integer formula for the leading coefficient with the canonical spoke weights. It may be a concrete way to show the lowest-degree term in the paper.
