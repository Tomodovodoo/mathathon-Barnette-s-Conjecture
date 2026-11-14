# Proofs: degree-4 contraction and tree matchings

Opus 5.5, 2026-11-14. Notation of `research/BRIEF.md`. All statements here are `PROVED-HERE` unless tagged otherwise. Each proof was re-read once adversarially; the objections raised and how they were met are at the end of each proof.

Throughout, `T` is an Eulerian triangulation of the sphere, rooted at a black face `t0` with roots `R`. I allow parallel edges but no loops, because one of the two contractions at a vertex often produces a parallel pair. Edges are identified by their black face and a side, so `Q_s`, `D` and spanning trees make sense for multigraphs (a parallel pair is a 2-cycle). A **tree matching** (TM) is a state `s` such that `Q_s` together with the two abstract root edges `r0r1, r1r2` is a spanning tree. This is equivalent to "some pair `(r,s)` has `Q_s` a forest": a forest `Q_s` with `n` edges on `n+3` vertices has three components; a mate exists iff each contains one root, and then the mate is unique (orient `Q_s` towards the roots and let `r(t)` be the tail of the `Q_s`-edge of `t`; OpenAI Lemma 6.1 gives one direction, the orientation gives the other).

## 0. Set-up at a degree-4 vertex

Let `x` be a non-root vertex of degree 4 whose four faces differ from `t0`. Name its neighbours in rotation order so that the two black faces at `x` are

    beta1 = {x, a, v1},   beta2 = {x, b, v2},

and the white faces are `omega1 = {x, v1, b}`, `omega2 = {x, v2, a}`. (If the black faces are `{x,v1,b}, {x,v2,a}`, swap the names `v1` and `v2`.)

Two contractions delete `x` and its four faces:

- `M`: identify `v1` and `v2` into `v`; the edges `a v1, a v2` become one edge `a v`, likewise `b v1, b v2`.
- `N`: identify `a` and `b` into `w`.

`T/M` and `T/N` are again Eulerian triangulations (possibly with parallel edges). I assume the merge considered creates no loop, that is `v1 !~ v2` for `M` (and `a !~ b` for `N`). Each remaining face keeps its colour, `t0` survives, and the roots of `T/M` are the images of `R`. The face-sets of `T/M` and `T` minus the four faces at `x` are identified.

The black faces at `x` are the only black faces containing `x`, so in every state exactly one of `beta1, beta2` takes `x`. That leaves four **types** of states, written `(s(beta1), s(beta2))`:

    M-types: (x, v2), (v1, x)        N-types: (x, b), (a, x).

## 1. States split over the two contractions

**Proposition 1.1.** Assume `M` is loop-free. Projection `pi_M` (forget `beta1, beta2`, rename `v1, v2 -> v`) is a bijection from the M-type states of `T` onto the states of `T/M`. Likewise for `N`. Hence, when both merges are loop-free,

    #states(T) = #states(T/M) + #states(T/N),

and every tree matching of `T` is of exactly one of the four types.

*Proof.* Non-root sets: if `v1, v2` are non-roots, `X(T/M) = X(T) - {x, v1, v2} + {v}`. If one of them, say `v1`, is a root, then `v` is a root, `X(T/M) = X(T) - {x, v2}`, and the type `(v1, x)` is empty. They are not both roots, since two roots are adjacent and `M` is loop-free.

Let `s` be of type `(x, v2)`. The outer faces (those other than the four at `x`) take every non-root of `T` except `x` and `v2`, each once. In particular they take `v1` once if `v1` is a non-root. After renaming, they take every element of `X(T/M)` once. So `pi_M(s)` is a state. Type `(v1, x)` is symmetric.

Inverse. Let `s'` be a state of `T/M`. If `v` is a non-root, let `t*` be the face with `s'(t*) = v`. As a face of `T` it contains exactly one of `v1, v2`: at least one because its corner `v` comes from one of them, at most one because `v1 !~ v2`. Call it `v*`, the other `v_o`. Lift `s'` by `s(t*) = v*`, leave the other outer faces unchanged, and give `v_o` to the black face at `x` containing it and `x` to the other black face. This is the only M-type state projecting to `s'`, because `v_o` must be taken and only one black face at `x` contains it. If `v` is a root, exactly one of `v1, v2` is a root and the same argument applies with `t*` absent.

The count follows because the four types partition the states. ∎

*Adversarial check.* "Can an outer face contain both `v1` and `v2`?" Only via an edge `v1 v2`, excluded. "Can a face of `T/M` be counted twice?" No, the face sets are identified. The identity was checked on 172,436 vertex-root pairs with both merges defined, `V <= 17`, no failure (`data/analyse_6_17.txt`). Loops never occurred in that range.

## 2. The correct lift criterion

For a state `s'` of `T/M` put `tau' = Q_{s'} + {r0 r1, r1 r2}`: `n` edges on the `n+1` vertices of `T/M` (with `n = |A(T)|`). It is a spanning tree iff `s'` is a TM. Let `split(tau')` be the same edge set read in `T - x`: an edge of `T/M` at `v` is an edge of `T` at `v1` or at `v2`, and a root edge at `v` goes to the root copy.

**Proposition 2.1.** Let `s` be the M-type lift of `s'`, of type `(x, v2)`. Then

    Q_s + root edges = split(tau') + {a v1, x b}.

(a) `s` is a TM iff `split(tau') + {a v1}` is a spanning tree of `T - x`.

(b) `s'` is a TM iff `split(tau')` is a forest in which `v1` and `v2` lie in different components.

(c) Hence if `s'` is a TM, write `K1 ∋ v1`, `K2 ∋ v2` for the two components of `split(tau')`. Then `s` is a TM iff `a ∈ K2`.

For type `(v1, x)` exchange `(a, v1) <-> (b, v2)` throughout: `Q_s + root edges = split(tau') + {x a, b v2}`, and the condition in (c) is `b ∈ K1`.

*Proof.* In type `(x, v2)` the face `beta1` takes `x`, so its `Q`-edge is `a v1`. The face `beta2` takes `v2`, so its `Q`-edge is `x b`. Every outer face has the same opposite side in `T` and in `T/M`. That gives the displayed identity.

(a) `x` is a leaf, attached by `x b`. So the edge set is a spanning tree of `T` iff the rest, `split(tau') + a v1`, is a spanning tree of `T - x`.

(b) `split(tau')` has `n` edges on `n+2` vertices. Identifying `v1` with `v2` gives `tau'`. If `split(tau')` is a forest with `v1, v2` in different components, identifying them gives a forest with one component fewer, `n` edges on `n+1` vertices, so a tree. If `split(tau')` contains a cycle, so does `tau'`. If `split(tau')` is a forest with `v1, v2` in one component, the identification closes a cycle. A tree has neither.

(c) Under (b), `split(tau')` has exactly two components, `K1` and `K2`. Adding `a v1` gives a spanning tree iff it joins them, iff `a ∈ K2`. ∎

**Correction to an earlier claim.** `research/2026-11-14_opus_route-graph-theory/PROOFS.md`, Lemma 6.2(iii), states that `s` is a TM iff `s'` is a TM and a side condition holds. The "only if" half is false (`REFUTED`). By (a) and (b), `s` can be a TM while `tau'` has a cycle through `v` that the split opens. Smallest example: the octahedron (`V = 6`, merge into a parallel pair). Smallest simple example: `V = 11`, plantri `-b` graph #1, root face 0, `x = 5`, merge `6 -> 4`. Here `T/M` has no pair at all, while 2 of the 4 tree matchings of `T` are of M-type. Counts: 13,210 of 131,336 simple contractions with `V <= 17` have M-type TMs of `T` whose projection is not a TM (`data/analyse_6_17.txt`, row "[old Lemma 6.2(iii)]"). The "if" half and the side condition are correct, as (c) shows.

*Adversarial check.* "Are `a v1` and the outer edge `a v` the same edge?" No. `a v1` is a side of `beta1`. The edge `a v` of `T/M` is `a v2` of `T`, whose black face is the outer face `g` across from `omega2` (Section 3). Both appear in the proofs below with their own roles. "Roots at `v`": a root edge at `v` goes to the root copy, consistent with Prop. 1.1.

## 3. A local sufficient condition and the rotation

Let `g` be the black face across the side `a v2` of the white face `omega2 = {x, v2, a}`, and `g = {a, v2, c}`. (`g != t0`: if `g = t0` then `v2` is a root, and a type `(x, v2)` state would take a root.)

**Lemma 3.1 (local condition).** Let `s'` be a TM of `T/M` whose lift `s` has type `(x, v2)`. Then `s(g) ∈ {a, c}`. If `s(g) = c`, the lift is a TM. So a failing lift has `s(g) = a`.

*Proof.* `v2` is taken by `beta2`, so `s(g) != v2`. If `s(g) = c`, the `Q`-edge of `g` is `a v2`. It lies in `split(tau')`, so `a ∈ K2` and Prop. 2.1(c) applies. ∎

**Proposition 3.2 (rotation).** Let `s'` be a TM of `T/M` whose lift `s`, of type `(x, v2)`, is not a TM. Define `rho(s)` from `s` by

    beta1: x -> a,     beta2: v2 -> x,     g: a -> v2.

Then `rho(s)` is a state of type `(a, x)` (an N-type). Let `K2'` be the component of `v2` in `K2 - {v2 c}`. Then `rho(s)` is a TM iff `b ∉ K2'`.

*Proof.* By Lemma 3.1, `s(g) = a`. The three faces exchange the three values `x, v2, a` and each new value is a corner: `a ∈ beta1`, `x ∈ beta2`, `v2 ∈ g`. So `rho(s)` is a state of type `(a, x)`.

`Q`-edges. `beta1` taking `a` contributes `x v1`. `beta2` taking `x` contributes `b v2`. `g` taking `v2` contributes `a c`. They replace `a v1`, `x b` and `v2 c`, so

    Q_{rho(s)} + root edges = split(tau') - {v2 c} + {a c, b v2, x v1}.

Since `s(g) = a`, the `Q`-edge of `g` in `T/M` is `v c`, which is `v2 c` in `T - x` (it is a side of `g`, which contains `v2`). It lies in `K2`. `x` is a leaf via `x v1`. Removing `v2 c` splits `K2` into `K2' ∋ v2` and `K2'' ∋ c`. The lift failed, so `a ∈ K1` by Prop. 2.1(c), and `a c` joins `K1` and `K2''`. The resulting two-component forest becomes a tree by adding `b v2` iff `b` is not in the component `K2'` of `v2`. ∎

**Corollary 3.3 (partial injection).** Let `Phi` send a TM `s'` of `T/M` to its lift if the lift is a TM, and otherwise to `rho(lift)` (or the mirror rotation `rho'` for type `(v1, x)`, with `g'` across `b v1` from `omega1`). `Phi` is injective wherever its value is a TM. Hence

    #TM(T) >= #TM(T/M) - E,

where `E` counts the TMs of `T/M` with a failing lift and `b ∈ K2'` (or the mirror condition).

*Proof.* Lifts are M-type, images of `rho` are of type `(a, x)` and images of `rho'` of type `(x, b)`. These three classes are disjoint. On each class the map is injective: lifting is injective by Prop. 1.1, and `rho` is undone by the reverse rotation `beta1: a -> x, beta2: x -> v2, g: v2 -> a`. ∎

`COMPUTED` (`code/rho.py`, `data/rho_8_15.txt`, `data/rho_16.txt`, all rooted contractions `V <= 16`). Every failing lift has `s(g) = a`, as Lemma 3.1 says. `rho` produces a TM in 27,723 of 28,189 failing lifts. The 466 exceptions start at `V = 13`, where every exception has a root among the neighbours of `x`. The first root-free exception is at `V = 14` (graph #12, root face `(5, 11, 6)`, `x = 2`, merge `9 -> 0`). So the rotation alone does not prove the contraction inequality. A second rule is needed for `b ∈ K2'`. In every exception some injection still exists (Section 5, `C >= b`).

*Adversarial check.* "Is `rho(s)` perhaps the lift of another TM, so that `Phi` collides?" No, it is N-type and lifts are M-type. "Is `c` distinct from `x, v1, b`?" `c != x` because `g` is not a face at `x`. `c != v1` because `v1 !~ v2`. `c = b` can happen. The proof does not use `c != b`: then `a c = a b`, and the component argument is unchanged.

## 4. Tree matchings come in sign-balanced pairs

**Proposition 4.1.** For a rooted `T` with `n >= 1`, the number of tree matchings is even. Exactly half have `eps(r_s, s) = +1`, where `r_s` is the unique mate.

*Proof.* Use the refereed form of Prop. 5.1 (`research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` §2, refereed in `research/2026-11-14_astra_referee-combinatorics/REWRITTEN-PROP-5-1.md`). `F(w) = sum over pairs of eps(r,s) w^s`. Its coefficient of `w^s` is `eps(r_s, s)` when `s` is a TM and `0` otherwise (Step 1 there, plus uniqueness of the mate). By (*) there, `F` is a sum over `D` of `±prod_C (w^{C+} - w^{C-})`. Every `D` has at least one cycle when `n >= 1`, so each term vanishes at `w = 1`. Hence `0 = F(1) = sum over TMs of eps(r_s, s)`. ∎

A direct proof avoids (*), though it still needs Step 1 for the coefficients. Reversing the cycle of `D(r,s)` through the least non-root (a choice that depends on `D` only, so the map is an involution) maps pairs to pairs and multiplies `eps` by `(-1)^{|C|} = -1` (odd length by the disk identity), so `sum over pairs of eps = 0`. Grouping that sum by `s` gives the same conclusion.

`COMPUTED`: `#TM+ = #TM-` on all 21,848 rooted instances in `data/contract_*.jsonl.gz` (`V <= 17`).

Consequence for induction. Any inductive count of tree matchings must produce even numbers. Indeed the minimum is 2 (octahedron, `V = 8`, `V = 12` examples). This makes "TM(T) >= TM(T')" the natural form of the contraction step, not "TM(T) >= 1".

## 5. What the proofs do not give

The inductive scheme of INDUCTION.md §4 needs two statements that I could not prove:

- (G) for a rooted `T` with a pair, no separating triangle and `V > 6`, some degree-4 non-root `x`, with faces avoiding `t0`, has a simple contraction `T/M` that still has a pair (`CONJECTURE`, `COMPUTED` `8 <= V <= 17`, `code/exp_misc.py`);
- (L) the contraction inequality `#TM(T) >= #TM(T/M)` (`CONJECTURE`, `COMPUTED` on 344,872 contractions, `V <= 17`), or the weaker "some TM of `T/M` lifts" (`COMPUTED`, same range).

Corollary 3.3 proves (L) up to the exception set `E`.
