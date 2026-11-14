# Proofs for the descent report

Notation is the shared one (`research/BRIEF.md`). A pair is `(r, s)`, and `u(t)` is the third corner of `t`. `k(r, s)` is the number of cycles of `Q_s`, and `c(r, s)` the number of cycles of `D(r, s)`. A tree pair is a pair with `k = 0`. The exchange graph `E` has the pairs as vertices and two kinds of edges: a D-swap along a cycle `C` of `D` exchanges `r` and `s` on the faces of `C`, and a Q-reversal along a cycle `K` of `Q_s` puts `r(t) := u(t)` on the faces of `K`. `n = |A| = |X|`.

Every statement below is `PROVED-HERE` unless tagged otherwise. None has been refereed. Each proof was reread once against the engine's output, and the checks are listed.

## Lemma A. The function model of a 2-factor

Let `(r, s)` be a pair. Write `sigma` for the permutation `x -> s(r^{-1}(x))` of `X`. Its cycles are the cycles of `D`. Write `f(x) = u(r^{-1}(x))`, a map from `X` to `V(T)`. So the face `t` with `r(t) = x` is the triangle `(x, sigma(x), f(x))`.

**(a)** The cycles of `Q_s` are the cycles of the functional graph of `f`. So `k(r, s)` is the number of cycles of `f`.

**(b)** Let `C` be a cycle of `D` with vertex set `V(C)`, and `(r', s')` the pair after the D-swap along `C`. Its function is

    f'(x) = f(sigma^{-1}(x))   for x in V(C),        f'(x) = f(x)   otherwise.

**(c)** The swap destroys every cycle of `Q_s` that meets `V(C)` and no other. The new cycles are the cycles of `f'` that meet `V(C)`. Hence

    k(r', s') - k(r, s) = #{cycles of f' meeting V(C)} - #{cycles of f meeting V(C)}.

*Proof.* (a) The edge of `Q_s` in `t` joins `r(t)` and `u(t)`. Orient it from `r(t)`. Every nonroot is `r(t)` for exactly one `t`, so out-degrees are 1 on `X` and 0 on the roots, and the oriented `Q_s` is the functional graph of `f`. A cycle of the underlying graph with `h` vertices has `h` edges, and each edge leaves one of its two ends, so every vertex of the cycle is a tail of a cycle edge and the cycle is directed. (This is Proposition 2.1 of the trees paper.)

(b) The swap does not change `u`. For `x` in `V(C)`, both `r^{-1}(x)` and `s^{-1}(x)` are faces of `C`, and `r'^{-1}(x) = s^{-1}(x)`. The face `s^{-1}(x)` has `r`-corner `sigma^{-1}(x)`, so `f'(x) = u(s^{-1}(x)) = f(sigma^{-1}(x))`. Off `V(C)` nothing changes.

(c) A cycle of `f` through a vertex `x` of `V(C)` uses the arc `x -> f(x)`. That arc belongs to the face `r^{-1}(x)`, whose `Q`-edge after the swap is `{sigma(x), f(x)}`. Different faces give different edges of `T`, so the old arc is gone and the cycle is destroyed. A cycle of `f` that avoids `V(C)` is also a cycle of `f'`. The count follows. ∎

*Check.* `COMPUTED`: `code/descent.exe` builds `k` after every swap from scratch. The lemma is not used by the code. It is used below to read the traps.

**Corollary A1.** If `D` is one Hamiltonian cycle (`c = 1`), the only D-swap replaces `Q_s` by `Q_r`. So no D-swap lowers `k` iff `Q_r` has at least as many cycles as `Q_s`. This is the smallest trap (Section 4 of `DESCENT.md`, `V = 16`): there `Q_s` and `Q_r` have one cycle each.

**Corollary A2.** A D-swap lowers `k` iff it creates fewer cycles through `V(C)` than it destroys. In particular a swap along a cycle `C` that meets no cycle of `Q_s` never lowers `k`.

## Lemma B. Three heights

Let `a(t, v)` be the integer spoke weights of Lemma 5.3 of the OpenAI paper, in the normalised form of Lemma 5.1 of the trees paper (`0 <= a(t, v) <= 6n`). Every counterclockwise simple spoke cycle of `H_0` has weight equal to the number of bounded faces of `H_0` inside it. For a pair `(r, s)` with third corners `u` put

    w_r = sum_t a(t, r(t)),     w_s = sum_t a(t, s(t)),     w_u = sum_t a(t, u(t)).

For a cycle `Z` of `D` or of `Q_s`, let `W(Z)` be the number of white faces of `T` in the disk bounded by `Z` (the side away from `t0`).

**(a)** `w_r + w_s + w_u` is the same for all pairs.

**(b)** A D-swap along `C` changes `w_s` by `+W(C)` or `-W(C)`, changes `w_r` by the opposite amount, and fixes `w_u`. The sign is `-` exactly when `C`, directed from `r` to `s`, is counterclockwise before the swap.

**(c)** A Q-reversal along `K` changes `w_u` by `+W(K)` or `-W(K)`, changes `w_r` by the opposite amount, and fixes `w_s`. The sign is decided by the sense of `K`.

**(d)** `W(Z) >= 1` in both cases. So every edge of `E` changes exactly one of `w_s`, `w_u`, and changes it strictly. All three heights lie in `[0, 6n^2]`.

*Proof.* (a) Each face contributes the sum of its three spoke weights, whichever corners are chosen.

(b) The swap exchanges `r` and `s` on the faces of `C`, so `u` is fixed and `w_s' - w_s = sum_{t in C} (a(t, r(t)) - a(t, s(t)))`. Replace each edge `r(t) -> s(t)` of `C` by its spoke route `r(t) -> t -> s(t)`, of weight `a(t, s(t)) - a(t, r(t))`. By Section 5.3 of the OpenAI paper the resulting closed spoke curve is simple and has the sense of `C`. If `C` is counterclockwise its weight is the number of bounded faces of `H_0` inside it. The bounded faces of `H_0` are the inner white faces of `T`, and the curve differs from `C` by slides inside black triangles, so that number is `W(C)`. Hence `w_s' - w_s = -W(C)` for a counterclockwise `C` and `+W(C)` for a clockwise one.

(c) Here `s` is fixed, `r' = u` and `u' = r` on the faces of `K`. So `w_u' - w_u = sum_{t in K} (a(t, r(t)) - a(t, u(t)))`, the weight of the closed spoke curve through `u(t) -> t -> r(t)`, `t in K`. This curve is the cycle `K` of `Q_s` pushed onto spokes, by the same sliding argument (one edge per black triangle, the slide avoids the third corner `s(t)`). Its weight is `+W(K)` or `-W(K)` according to its sense.

(d) Both `D` and `Q_s` consist of edges that leave `r(t)` inside `t`. The disk identity (Lemma 4.1 of the OpenAI paper) applies to any directed cycle of such edges and gives `2l - h = -3`, so `3(B - W) = -3` and `W = B + 1 >= 1`. The bound on the heights is `n` faces times `6n`. ∎

*Remarks.* The first half of (b) is the known reading of `omega(s)` as a volume under a height function (`research/2026-11-14_fable_route-combinatorics/PROOF.md`, Section 2.3). Part (c) is the same statement for the third corner. It is also Lemma 1 of `research/2026-11-14_opus_conjectures/PROOFS.md` in disguise: a Q-reversal reverses a directed cycle of the alpha-orientation `O_u`, and `w_u` is, up to sign and an additive constant, the sum of the lattice potential `phi_u` over the faces of `H_0`.

*Check.* `COMPUTED`: the engine does not compute `a`. It assigns `psi` and `om` along a spanning forest of `E` using the increments `-W * sense` and then tests every remaining edge. No inconsistency on any exchange graph of the census `V <= 22` (49,331,840 pairs) or on the saved traps. In the engine's names, `om` is `w_s` and `psi` is `w_u`, each up to a global sign that depends on whether the input rotation is clockwise (plantri) or counterclockwise (`gen.py`).

**Corollary B1.** A potential `Phi = (k, e1 * w_u, e2 * w_s)` or `(k, e2 * w_s, e1 * w_u)`, compared lexicographically, with `e1, e2` in `{+1, -1}`, has no plateau: every exchange move changes it. A strictly decreasing sequence of pairs has at most `(n/3 + 1)(6n^2 + 1)^2` terms. (There are at most `n/3` cycles in `Q_s` because each has at least three vertices.)

## Proposition C. Three forms of C3

For `j >= 0` let `E_j` be the subgraph of `E` induced on the pairs with `k <= j`. The following are equivalent.

1. (C3) From every pair there is a path in `E` to a tree pair along which `k` never increases.
2. For every `j`, every connected component of `E_j` contains a tree pair.
3. There is no closed plateau. A closed plateau is a nonempty set `S` of pairs, all with the same `k = j >= 1`, such that every exchange move from a pair of `S` leads to a pair of `S` or to a pair with larger `k`. (Q-reversals keep `s`, hence `k`, so `S` is closed under them. The condition only bites on D-swaps.)

*Proof.* (1) implies (2): a non-increasing path from a pair of `E_j` stays in `E_j`. (2) implies (3): a closed plateau `S` with value `j` is a union of connected components of `E_j`, because an edge of `E_j` at a pair of `S` ends at a pair with `k <= j`, hence in `S`. It contains no tree pair. (3) implies (1): let `p` have `k(p) = j >= 1`, and `S` the set of pairs reachable from `p` by moves that keep `k = j`. `S` is not a closed plateau, so some move, necessarily a D-swap, leads from a pair of `S` to a pair `p'` outside `S` with `k(p') <= j`, hence `k(p') < j`. The path from `p` to `p'` never increases `k`. Induct on `j`. ∎

The signed count of the trees paper proves (2) only for `j >= max k`, where `E_j` is the whole exchange graph. For smaller `j` the grouping by `D` meets a part of each orientation cube, and the product formula for a full cube is not available. That is the exact point where a proof of C3 by the known cancellation stops.

## Proposition D. Gluing cannot hurt

Let `T` be obtained from rooted triangulations `T_1` (root `t0`) and `T_2` (root `t0'`) by deleting a white face `y` of `T_1` and the root face `t0'` of `T_2` and identifying their boundaries. Root `T` at `t0`. This is the gluing that killed R2 at `V = 33`.

**(a)** States of `T` are the pairs (state of `T_1`, state of `T_2`). Pairs of `T` are the pairs (pair of `T_1`, pair of `T_2`).

**(b)** `D` is the disjoint union of the two `D`'s. Every cycle of `Q_s` lies in one of the two pieces. So `k = k_1 + k_2`, `c = c_1 + c_2`, and the exchange graph of `T` is the Cartesian product of the two exchange graphs.

**(c)** C3 holds for `T` iff it holds for `T_1` and `T_2`. The escape radius (the largest distance from a non-tree pair to a pair with smaller `k`) of `T` is the maximum of the two.

*Proof.* (a) The nonroots of `T_2` are corners only of faces of `T_2`, and there are as many of them as bounded black faces of `T_2`. A state of `T` is a bijection, so it matches the bounded black faces of `T_2` exactly onto the nonroots of `T_2`. The rest is a state of `T_1`. Disjointness is facewise.

(b) `D` has its edges inside black faces between the two matched corners, so the first claim is clear. For `Q_s` use Lemma A(a). For a nonroot `x` of `T_2`, `f(x)` is a vertex of `T_2`. For a nonroot `x` of `T_1`, `f(x)` is a vertex of `T_1`, because the face `r^{-1}(x)` is a face of `T_1`. So a cycle of `f` that contains a nonroot of `T_1` stays among the vertices of `T_1`, and the other cycles consist of nonroots of `T_2`. Moves act on one coordinate and leave the other alone.

(c) Given C3 for both pieces, descend in the first coordinate and then in the second. Conversely a closed plateau `S_1` of `T_1` gives the closed plateau `S_1 x {pairs of T_2 with k_2 = 0 reachable from a fixed tree pair by moves inside k_2 = 0}`. For the radius, a pair `(p_1, p_2)` reaches a smaller `k` exactly when one coordinate does. ∎

So no gluing of this type, in particular no chain of copies of the `V = 18` witness, can refute C3 or raise the escape radius. `COMPUTED` cross-check: `data/families.txt`.

The other kind of separating triangle (black faces inside it, seen from the root) does not give a product, since one inner black face must then be matched to a corner of the triangle.

## Proposition E. The parity of c, and why c cannot be part of the potential

`c(r, s) = n (mod 2)` for every pair (trees paper, after (8): each cycle of `D` contributes `+1` or `-1` to `J`, and `J = n (mod 2)`). So a Q-reversal changes `c` by an even number, and a D-swap does not change `c`.

`COMPUTED`: at `V = 16` there is a rooted instance (`data/witnesses.txt`, first line) with a pair that has `k = 1`, `c = 1`. Its only D-swap gives `k = 1` again (Corollary A1). Its only Q-reversal gives `c = 3`. Hence every potential that is non-decreasing in `c` for fixed `k`, and in particular `k + c`, `(c, k)`, `(c, anything)`, `(k, c)`, traps this pair under single moves. For `k + c` and `(c, .)` it stays trapped under macro moves of length two. This is the descent form of the known fact that a single 2-factor can carry no tree pair.

## Proposition F. What a bounded lookahead would give

For a potential `Phi` on pairs and `L >= 1`, say that `Phi` has escape radius at most `L` if from every non-tree pair some pair with strictly smaller `Phi` is within `L` exchange moves.

**(a)** If `k` has escape radius at most `L` on a class of rooted instances, a tree pair is found from any pair in at most `L n / 3` moves, by at most `n/3` searches of balls of radius `L`. A pair has at most `n/3 + n/3` neighbours, so a ball has at most `(2n/3)^L` pairs and the search is polynomial for fixed `L`.

**(b)** The same holds for the potentials of Corollary B1, with `O(n^5)` rounds.

*Proof.* (a) Each round lowers `k` by at least one and `k <= n/3`. Both `D` and `Q_s` have at most `n/3` cycles. (b) Corollary B1. ∎

The converse direction is where the data speak: the escape radius of `k` is not bounded by 3 (Section 3 of `DESCENT.md`).
