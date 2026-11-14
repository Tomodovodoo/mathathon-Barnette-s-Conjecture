# The residual cases of the contraction inequality

Fable 5.2, 2026-11-14. Notation of `research/BRIEF.md` and of `research/2026-11-14_opus_route-induction/PROOFS.md` (cited as OP). Tags as in the brief. All computations use this folder's own code (`code/`, commands in `code/README.md`).

What this file establishes. The 466 residual cases are not a local accident that a second small rule will remove. They have one shape, they come in pairs exchanged by the rotation between the two contractions at `x`, and they exist only when both contractions have tree matchings. This gives a proved one-sided inequality, a proved superadditive bound, and a precise statement of what is missing.

## 1. Set-up: outer states and patterns

`x` is a non-root vertex of degree 4 with neighbours `a, v1, b, v2` in rotation order, black faces `beta1 = {x,a,v1}`, `beta2 = {x,b,v2}`, white faces `omega1 = {x,v1,b}`, `omega2 = {x,v2,a}`. `M` merges `v1, v2` and `N` merges `a, b`. Let `g` be the black face on the edge `a v2` and `g'` the black face on the edge `b v1`. Write `g = {a, v2, c}`, `g' = {b, v1, c'}`.

**Lemma 0 (no loops).** `PROVED-HERE`. In an Eulerian triangulation the opposite neighbours of a degree-4 vertex are not adjacent. So both merges are always loop-free and the hypothesis "loop-free" in OP Prop. 1.1 is automatic.

*Proof.* Suppose `v1 ~ v2`. The 3-cycle `x v1 v2` has `a` on one side. On that side the faces along `x v1` and `x v2` are `beta1` (black) and `omega2` (white), because `a` is the only neighbour of `x` there. Signed side counting on that side gives `3(B - W) = 1 - 1 + sigma` with `sigma = +-1` for the edge `v1 v2`. The right side is not divisible by 3. The same argument with the colours exchanged gives `a !~ b`. ∎

`COMPUTED`: no loop in 1,202,792 rooted contractions, `V <= 18` (`data/census_*.json`, field `loops`).

**Lemma 1 (a non-simple contraction has no pair).** `PROVED-HERE`. If `v1, v2` have a common neighbour `w` outside `{x, a, b}`, then `T/M` has no pair and no tree matching.

*Proof.* In `T/M` the two edges `v w` bound two discs. Let `Delta` be the one without `t0`. It contains `a` or `b` strictly inside, so its number `I` of interior vertices is at least 1, and they are non-roots. Side counting gives `3(B - W) = sigma1 + sigma2`, so `B = W` and exactly one boundary edge has its black face inside. Euler's formula for a disc with boundary length 2 gives `B + W = 2I`, so `B = I`. Let `S` be the interior vertices. The black faces meeting `S` are the `I` black faces inside, and the one on the boundary edge has only one corner in `S`. So `sum_t min(2, |t ∩ S|) <= 2I - 1 < 2|S|`, and the condition (3.1) of the OpenAI paper fails. ∎

So the contraction inequality is trivial for non-simple contractions. `COMPUTED`, consistent: every failing lift in the census occurs in a simple contraction (`lift_fail = lift_fail_simple`, `V <= 17`).

**Outer states.** Let `N0 = T - x`, with the quadrilateral hole `a v1 b v2`. An *outer state* is an injective choice `sigma` of corners for the black faces of `A` not at `x`, using every non-root of `N0` except one vertex `m` of `{a, v1, b, v2}`, such that `F_sigma = Q_sigma + {two root edges}` is acyclic. `F_sigma` has `n` edges on `n + 2` vertices, so it is a spanning forest of `N0` with two components. Its *pattern* is the partition it induces on `(a, v1, b, v2)`:

    P_a = {a | v1 b v2},  P_v1, P_b, P_v2 (one vertex alone),
    P_1 = {a v1 | b v2},  P_2 = {a v2 | v1 b},  P_0 = all four together.

`{a b | v1 v2}` cannot occur: with `x` put back, a path `a..b` in one component closes to a cycle through `x` that separates `v1` from `v2`.

**Proposition 2 (table).** `PROVED-HERE`; `COMPUTED` against a direct count of `TM(T/M)` on all 1,202,792 contractions with `V <= 18` (`pattern_vs_direct_fail = 0`). States of `T` correspond to pairs `(sigma, m)`: `beta1, beta2` take `x` and `m`. With this identification

| set | outer states |
| --- | --- |
| `TM(T)` | `m` in `{v2, b}` and `a, v1` separated, or `m` in `{v1, a}` and `b, v2` separated |
| `TM(T/M)` | `m` in `{v1, v2}` and `v1, v2` separated |
| `TM(T/N)` | `m` in `{a, b}` and `a, b` separated |

In patterns: `TM(T)` is `(m in {v2,b}; P_a, P_v1, P_2)` and `(m in {v1,a}; P_b, P_v2, P_2)`. `TM(T/M)` is `(m in {v1,v2}; P_v1, P_v2, P_1, P_2)`. The failing lifts of `T/M` are `(v2; P_v2 or P_1)` and `(v1; P_v1 or P_1)`. A state of pattern `P_1` is never a tree matching of `T`, whatever `m` is.

*Proof.* The four choices of `m` are the four types of OP §0. For `m = v2` the faces at `x` contribute the edges `a v1` and `x b` (OP Prop. 2.1), `x` is a leaf, and `F_sigma + a v1` is a tree iff `a, v1` lie in different components. The other three types are the same computation: `m = b` adds `a v1, x v2`; `m = v1` adds `x a, b v2`; `m = a` adds `x v1, b v2`. The rows for `T/M` and `T/N` are OP Prop. 2.1(b). ∎

## 2. The rotation exchanges the exceptions of the two contractions

Let `rho` be the rotation of OP Prop. 3.2 and its mirror. On outer states it is the involution that swaps `m = v2` with `m = a` at the face `g` (`sigma(g)`: `a <-> v2`, forest edge `v2 c <-> a c`), and `m = v1` with `m = b` at `g'`.

Let `E_M` be the set of tree matchings of `T/M` whose lift fails and whose rotation is not a tree matching of `T` (the exception set of OP Cor. 3.3), and `E_N` the same for `N`.

**Theorem 3.** `PROVED-HERE`.

1. Every element of `E_M` has pattern `P_1`. A failing lift of pattern `P_v2` or `P_v1` always rotates to a tree matching of `T`.
2. `rho` maps `E_M` bijectively onto `E_N`. In particular `|E_M| = |E_N|`.
3. If `sigma` is in `E_M` then `rho(sigma)` is a tree matching of `T/N`.

*Proof.* Take `sigma` in `TM(T/M)` with `m = v2` and failing lift, the other case being the mirror. By OP Lemma 3.1, `sigma(g) = a`. With `K1`, `K2`, `K2'`, `K2''` as in OP Prop. 3.2, the forest of `rho(sigma)` has components `K2'` and `K1 + K2'' + ac`, and `rho(sigma)` is a tree matching of `T` iff `b` is not in `K2'`. In pattern `P_v2` the vertex `b` lies in `K1`, which proves 1. Now let `sigma` be in `E_M`, so `b` is in `K2'`. Then `rho(sigma)` has `m = a` and pattern `P_1` again: `{a, v1}` in one component, `{b, v2}` in the other. By the table it is a tree matching of `T/N` (this is 3) and not of `T`. So it is a failing lift for `N`. The rotation of the `N`-setup at a state with `m = a` uses the black face on the edge `a v2`, which is `g`, and moves `sigma(g)` from `v2` back to `a`. It returns `sigma`, which is not a tree matching of `T`. So `rho(sigma)` is in `E_N`. The same argument started from `E_N` gives the inverse map. ∎

`COMPUTED` (`code/residual.py`, `code/superadd.py`): all 7,940 exceptions with `V <= 18` have pattern `P_1`, `sigma(g) = a`, and `sigma(g')` in `{b, v1}`. The two contractions have equal exception counts at each of the 3,106 vertex-root pairs with exceptions (`V <= 18`), and at all 172,436 vertex-root pairs with `V <= 17`.

**Theorem 4 (consequences).** `PROVED-HERE`.

(a) One-sided inequality. If `T/N` has no tree matching, then `#TM(T) >= #TM(T/M)`, by the injection "lift, else rotate" of OP Cor. 3.3 with no exception. This covers every case in which `T/N` is non-simple or has no pair.

(b) Superadditivity up to exceptions. With `e = |E_M| = |E_N|`,

    #TM(T) >= #TM(T/M) + #TM(T/N) - 2e.

(c) If `T` has no tree matching, then `TM(T/M) = E_M` and `TM(T/N) = E_N`: every tree matching of either contraction has pattern `P_1` before and after rotation.

(d) If `x` has two root neighbours, they are `a, v2` or `b, v1`, one of `g, g'` is `t0`, no outer state has pattern `P_1`, and `e = 0`.

*Proof.* (a) By Theorem 3.3 an exception produces a tree matching of `T/N`. (b) Four sets of tree matchings of `T` are pairwise disjoint: lifts from `T/M` (M-type, projection a tree matching), rotations of failing lifts from `T/M` (N-type, pattern `P_v2` or `P_v1`, so `a, b` are together and the projection to `T/N` is not a tree matching), lifts from `T/N`, and rotations from `T/N` (M-type, projection not a tree matching). Their sizes add up to the right side. (c) is (b) read backwards together with injectivity. (d) Roots are pairwise adjacent, and `a !~ b`, `v1 !~ v2` by Lemma 0, so two root neighbours are consecutive. The edges `a v1`, `b v2` lie in `beta1`, `beta2`, not in `t0`, so the pair is `a, v2` or `b, v1`. Then the root path joins `a` to `v2` (or `b` to `v1`) inside `F_sigma`, which excludes `P_1`. ∎

`COMPUTED` (`code/superadd.py`, `data/superadd_6_17.json`, all 172,436 vertex-root pairs, `V <= 17`): (b) never fails and is an equality in 783 pairs with `e > 0`, so it is sharp. The smallest equality is OP's own example R10 (`V = 13`, graph 7, `x = 10`): `6 = 4 + 4 - 2`. No exception occurs when one contraction is free of tree matchings (0 of 172,436). The largest fraction `|E_M| / #TM(T/M)` is exactly 1/2.

Second reading of the proofs of Theorems 3 and 4. I checked these points again after writing. (i) Root cases: if `a` is a root then `sigma(g) = a` is impossible and no lift with `m = v2` fails; if `v2` is a root then `m = v2` does not occur. (ii) `rho(sigma)` is an outer state: it is injective, misses `a`, and its forest is `F - v2c + ac`, acyclic with two components. (iii) The four sets in 4(b): the first two have sizes adding to `#TM(T/M) - |E_M|` because lifting and `rho` are injective, and the test that separates rotations from lifts of the other contraction is whether `a, b` (or `v1, v2`) lie in one component. (iv) The `N`-setup is the `M`-setup with the names `(a, v1, b, v2)` replaced by `(v1, a, v2, b)`, and its faces "`g`" and "`g'`" are `g'` and `g`. The proofs were not read by a second agent.

## 3. Classification of the exceptions

`data/residual_summary.json`, from `data/exceptions_*.jsonl(.gz)`. One row per exception, normalised so that the missing vertex is `v2`.

| `V` | failing lifts | exceptions | `x` has no root neighbour | one root neighbour | class A (`g'` takes `b`) | class B (`g'` takes `v1`) |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | 600 | 8 | 0 | 8 | 4 | 4 |
| 14 | 2,162 | 20 | 4 | 16 | 10 | 10 |
| 15 | 4,942 | 80 | 18 | 62 | 40 | 40 |
| 16 | 20,049 | 358 | 104 | 254 | 179 | 179 |
| 17 | 60,832 | 1,320 | 458 | 862 | 660 | 660 |
| 18 | 246,159 | 6,154 | 2,410 | 3,744 | 3,077 | 3,077 |

Up to `V = 16` this is OP's count: 466 exceptions among 28,189 failing lifts. The share of exceptions grows slowly: 1.3%, 0.9%, 1.6%, 1.8%, 2.2%, 2.5% for `V = 13..18`.

Structure, all `COMPUTED` on the 7,940 rows and explained by Theorems 3 and 4:

- Pattern `P_1` in every row. The dual cycle of the two-component forest passes the hole between `a` and `v2` through the spoke `(g, a)` and between `b` and `v1` through a spoke of `g'`. Classes A and B are the two spokes of `g'`, and `rho` exchanges A-rows of `M` with B-rows of `N`, which is why the two columns agree.
- Never two root neighbours (Theorem 4(d)). With one root neighbour the root is `v1` or `b`, never `a` (431 + 431 at `V = 17`).
- All four neighbours of `x` have degree at least 6. This is forced: a neighbour of degree 4 makes one contraction non-simple, and then Theorem 4(a) applies.
- The roots lie on the `K1` side in half of the rows and on the `K2` side in the other half.
- At most 3 exceptions at one contraction (`V <= 17`), usually 1.

So there is no local feature of the triangulation around `x` that separates exceptions from non-exceptions beyond "both contractions are simple with tree matchings". The feature is global: where `b` sits in the tree `K2` relative to the edge `v2 c`.

## 4. What I tried for a second rule, and why I stopped

- A second three-face rotation does not exist. The only black faces on the hole are `g` and `g'`, and an exception has `m = v2`, so the rotation at `g'` (which needs `m` in `{v1, b}`) does not apply. OP's probe found that the shortest repairing moves change up to 11 faces. I agree with the reading that no bounded local rule works.
- Signs. `REFUTED` as a route: I hoped that all pattern-`P_1` tree matchings of `T/M` carry the same sign `eps`, so that sign balance (OP Prop. 4.1) would force a tree matching of another pattern. `code/signs.py`: for `V <= 15`, 693 contractions have pattern-`P_1` tree matchings. In 590 of them these all carry one sign, but in 103 they are sign-balanced among themselves, so no contradiction follows. The sign balance of `TM(T/M)` itself was confirmed on all 9,880 contractions with tree matchings, `V <= 15`.
- Determinants. All states have the same permutation sign (every cycle of two states is odd by the disk identity, and 2-cycles cannot occur), so `#states = |det B|` and OP Prop. 1.1 is a cofactor expansion. Tree matchings are states with exactly one mate, and I found no rank statement that sees "exactly one". This agrees with `research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` §1. `HUNCH` only.

The positive result of this section is Theorem 4(c): for existence one needs much less than a second rule. It suffices to exclude that every tree matching of both contractions is exceptional. See `MISSING-LEMMA.md`.

## 5. Machine-readable data

| File | Content |
| --- | --- |
| `data/exceptions_6_13.jsonl`, `data/exceptions_14_17.jsonl.gz`, `data/exceptions_18.jsonl.gz` | one JSON row per exception: `V`, `gid` (index in `plantri -b -a V`), `t0`, `x`, `a, v1, b, v2, c` (normalised), `rootnbrs`, the outer faces with their assigned corners, all black and white faces |
| `data/residual_summary.json` | the classification above, per `V` |
| `data/superadd_6_17.json` | Theorem 4(b) check and exception fractions |
| `data/nolift_18.jsonl` | the 50 contractions at `V = 18` in which no tree matching of `T/M` lifts directly |
