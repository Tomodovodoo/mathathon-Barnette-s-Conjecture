# How the proof of Barnette's conjecture works

A plain account for a graduate student, written from the route map (`ROUTE-MAP.md`, `route-map.pdf`). Labels such as N.H or A.T are routes on that map. About six printed pages.

Status tags. `LIT` means stated and proved in one of the three 2026 papers (unrefereed preprints: O is the OpenAI paper, L is Li's note, T is the trees paper) or in older published work. `PROVED-HERE` means a full proof sits in an agent folder of this project. None of those has been checked by a human, and I say which ones an AI referee has passed. `COMPUTED` gives the range. `CONJECTURE`, `HUNCH` and `REFUTED` mean what they say.

The diagram records routes supplied by these sources. Its words "forced" and "free" describe that inventory, not a theorem that other proofs are impossible. A route ID such as N.H is only a lookup key; the explanation below can be read without following those links.

## 1. What must be shown

A Barnette graph `G` is cubic, bipartite, planar and 3-connected. The claim is that `G` has a Hamiltonian cycle. The proof gives more. For any edge of `G` there is a Hamiltonian cycle that avoids it [`LIT`, O Corollary 7.1].

Work in the dual. `T = G*` is a triangulation of the sphere. It is simple because `G` is 3-connected, and this is the only place where 3-connectivity enters [`PROVED-HERE`, dependency-graph audit, unreviewed]. Its faces are coloured black and white because `G` is bipartite. Vertices of `G` are faces of `T`, and faces of `G` are vertices of `T`.

A Hamiltonian cycle of `G` is a closed curve on the sphere that passes through every triangle of `T` once. It cuts the vertices of `T` into an inside set and an outside set, and each set induces a tree in `T`. The converse holds too, so the goal has been known since 1971 in this form, to split `V(T)` into two induced trees [`LIT`, Stein 1971; Alt, Payne, Schmidt, Wood 2016].

For 57 years people tried to cross that one edge of the map directly. Face-size bounds reached 8, computers reached 90 vertices, and several equivalent forms were found [`LIT`]. None of it produced a way to make the two trees exist. The obstacle is that 3-connectivity is a global property, and the conjecture is false without it from face size 10 on [`LIT`, Schnieders 2025]. This explains an obstacle for those local reductions; it does not exclude every possible local method.

The 2026 proof does not cross that edge. It goes down through a dozen other waypoints and comes back up. The rest of this note explains why each waypoint is there.

## 2. Read the answer backwards

The quickest way to see where the waypoints come from is to start from a Hamiltonian cycle and ask what it looks like in `T`.

Fix a black face `t0` of `T` and one of its edges `e0`. Suppose a Hamiltonian cycle of `G` avoids the edge `e0*`. Every vertex of `G` has three edges, the cycle uses two, so the unused edges form a perfect matching `P` of `G`. In `T` this says that `P` picks exactly one side of every triangle. The cycle is a single curve, so `P`, seen as a set of edges of `T`, has no cycle and falls into two trees, one on each side of the curve.

Remove `e0` from `P`. The tree containing it splits, and now there are three trees, one for each corner of `t0`. Call those corners the roots. Direct every tree towards its root. Each bounded black face `t` contains exactly one selected edge, and that edge has a tail. Call the tail `s(t)`.

The map `s` sends the bounded black faces `A` to the non-root vertices `X`, with `s(t)` a corner of `t`, and it is a bijection because every non-root vertex has exactly one outgoing edge. Such a bijection is called a **state**. So every Hamiltonian cycle that avoids `e0*` determines a state [`PROVED-HERE`, route-combinatorics Proposition 7, AI-refereed; also limits and route-graph-theory, under review; replayed on three bipyramids by `spotcheck.py`].

A state can exist at all because of a count. Euler's formula gives `T` equally many black and white faces, say `k`, and `k + 2` vertices. Remove `t0` and its three corners and both `A` and `X` have `n = k - 1` elements [`LIT`, O (2.1)]. This is the first and most basic use of bipartiteness.

Now run the construction forwards. Draw a new vertex in the middle of every black face and join it to the three corners. These edges are the spokes, and they form the spoke graph `H`. A state deletes one spoke at every bounded black face. Ask for a state `s` such that the remaining spokes `H - s` form a spanning tree. Call that a **good state**, the main paper's word. T calls it a tree matching; O has no name and speaks of a pair with `Q_s` a forest. From a good state the cycle comes back by classical steps:

- the duals of the deleted spokes form a spanning tree on the white faces, because the complement of a spanning tree in the plane is a spanning tree of the dual [`LIT`, O Lemma 2.1];
- root that white tree at the white face across `e0`, and let each tree edge select the side of its black face that borders the end farther from the root. Together with `e0` this is one side of every face, the set `P` [`LIT`, O Section 6.1];
- the complement of `P` in `G` is 2-regular, and one shows it is a single cycle (Section 6 below).

So the whole problem becomes this. **Find a state whose complement in the spoke graph is a tree.** Everything classical is on the right-hand side of the map. Everything new is about finding that state.

One warning before going on. Not every Hamiltonian cycle that avoids `e0*` comes from a good state. On the hexagonal prism four cycles avoid a given edge and only two come from good states [`COMPUTED`, limits; `REFUTED` as route A.x1]. The other two give one and the same state, which has no partner [`COMPUTED`, `spotcheck.py`]. Its `Q_s` has no cycle; a path of opposite edges joins two roots. So "`Q_s` is a forest" is not the same as "good". A state fixes the tail of the selected edge in each black face, and that determines the edge only when `H - s` is a tree. The proof finds a special kind of cycle.

## 3. Why a second state appears

How do you test whether `H - s` is a tree? At each bounded black face `t` the two remaining spokes join the two corners other than `s(t)`. Replace them by the edge of `t` opposite `s(t)`. The set of these `n` edges is called `Q_s`. Then `H - s` is a tree exactly when `Q_s` is a forest in which every component contains exactly one root.

"Exactly one root per component" is awkward to check directly, and here the second state comes in. Suppose `r` is another state with `r(t) ≠ s(t)` for every `t`. Call `(r, s)` a **pair**. Then `r(t)` is one end of the `Q_s`-edge of `t`. Direct that edge out of `r(t)`. Because `r` is a bijection, every non-root vertex has exactly one outgoing edge of `Q_s` and the roots have none. In a graph like that, a component with no cycle has exactly one vertex without an outgoing edge, so it contains exactly one root. So for a pair, "`Q_s` is a forest" already gives the good state [`LIT`, O Lemma 6.1].

The partner `r` is a certificate. It orients `Q_s`, and the orientation does the counting. Without it the statement is false. On the hexagonal prism all three states have `Q_s` a forest and only two are good states [`COMPUTED`, limits, and my own check in `research/2026-11-14_fable_labyrinth-map/spotcheck.py`; `REFUTED` as route R.x1].

The same picture shows what goes wrong when `Q_s` is not a forest. A component with a cycle has no root, its cycle is a directed cycle, and reversing that cycle gives a different partner `r'` of the same `s`. If `Q_s` has `q(s)` such components, `s` has exactly `2^q(s)` partners. So a good state is a state with exactly one partner [`LIT`, T Proposition 2.1 and Theorem 1.2; `COMPUTED` on 140358 states].

A pair `(r, s)` also defines a second object. In each black face take the side from `r(t)` to `s(t)`, directed that way. Since both states are bijections, these `n` directed edges form disjoint directed cycles through the non-root vertices. Call these directed cycles `D(r, s)`; with the directions forgotten they are the **cover** of the pair (O's "group"). Reversing one cycle of `D` exchanges `r` and `s` along it and gives another pair.

So the pairs carry two kinds of moves: reverse a cycle of `Q_s` (this changes `r` and keeps `s`), or reverse a cycle of `D` (this changes both). We want a pair on which the first move is impossible.

## 4. The one new idea

Nobody knows how to point at a pair with `Q_s` a forest. The project tried: the highest state, the lowest state, a cover with fewest cycles oriented one way, the pair with the largest rank difference, the extremes of the lattice of pairs, greedy descent on the number of cycles. Several individual rules are `REFUTED` (routes N.x3 to N.x6, N.x14). An independent referee confirms the first joint failure of the two true lattice extremes at 18 vertices. The replacement extreme-or-irreducible rule also fails, at 33 vertices, by two independent implementations. Monotone descent allowing plateaus is a separate conjecture.

The proof counts instead. Attach a sign to every pair, add up the signs of all pairs with a weight that depends only on `s`, and compute the sum twice. Nothing like this appears in the Barnette literature before 2026 [`COMPUTED` by a text search of 23 papers, history-literature].

**The sign.** Going from `r(t)` to `s(t)` along the boundary of the black face `t` is either counterclockwise or clockwise. Write `δ = +1` or `-1`. The sign of the pair is the product of these `n` numbers [`PROVED-HERE`, route-dimers, AI-refereed; it agrees with the phase `i^J` of O and the signs of L and T up to a constant depending on `n` only, dependency-graph, unreviewed].

**The disk identity.** The sign is only useful if both moves flip it. Reversing a cycle of `D` of length `h` changes `h` of the factors `δ`, so the sign is multiplied by `(-1)^h`. The same happens for a cycle of `Q_s`. So everything rests on one fact. These cycles have odd length. That is a consequence of the disk-counting lemma [`LIT`, O Lemma 4.1]:

> Let a state choose a corner in each black face, and let a directed cycle run through edges that leave their black face from the chosen corner. Then the disk bounded by the cycle, on the side away from `t0`, contains exactly one more white face than black faces.

The proof is a double count. Euler's formula counts the faces of the disk. A count of the sides along the boundary gives black minus white in terms of the boundary. The bijection says the black faces of the disk are matched exactly with its interior vertices and with the boundary vertices whose face lies inside. Three equations, and out comes `W = B + 1`, in the paper's form `2l - h = -3`. The bijection is essential. Let two faces choose the same vertex and there is a 9-vertex example where the identity fails [`COMPUTED`, limits; `REFUTED` as B.x1].

In the real-sign form the proof uses only the parity of `h` here. The exact value is needed once more, in the next step [`PROVED-HERE`, referee-determinants, unreviewed].

**First evaluation, with `s` fixed.** Take any function `F(s)` and form the sum of `sign(r, s) · F(s)` over all pairs. Fix `s`. If `Q_s` has a cycle, choose one by a rule that looks at `s` only, and reverse it. This pairs up the partners of `s`, keeps `F(s)`, and flips the sign. Those terms cancel. What is left is the sum over good states, each with its unique partner. In particular, if the total is not zero, a good state exists [`LIT`, O Lemma 5.2]. In linear algebra this is the remark that the incidence matrix of a graph with a cycle is singular (route K.1).

**Second evaluation, with `D` fixed.** Group the pairs by their cover, the cycles of `D` with orientations forgotten. A cover with `c` cycles carries `2^c` pairs, one for each choice of orientations, and reversing one cycle flips the sign. So with `F` constant every group sums to zero, and the unweighted count is `0 = 0`. It says only that good states come in equal numbers of both signs [`LIT`, T Theorem 5.2]. This rules out this unweighted signed sum, including its reduction modulo any prime; it does not rule out every possible modular invariant (route N.x2) and why the number of good states is always even.

So `F` must tell the two orientations of a cycle apart, while still depending on `s` alone. That is the content of the next section, and it is the step where the published proofs differ most.

## 5. Why the total is not zero

Here is the shortest version I know, with a polynomial in one variable [`PROVED-HERE`, route-dimers and referee-determinants, AI-refereed; the Lean formalisation uses the same polynomial].

Give every spoke `(t, v)` a real number `a(t, v)`, and let `F(s)` be the product over `t` of `1 + x · a(t, s(t))`. Along a cycle `C` of `D`, add up the numbers `a` used by the state that is `s` when `C` runs counterclockwise, and call the result `L+(C)`. Call `L-(C)` the same for clockwise. Because `F` is a product over faces, the sum over a group factors over its cycles, and each cycle contributes a difference of two products whose constant terms cancel:

    (1 + x L+(C) + ...) - (1 + x L-(C) + ...) = x (L+(C) - L-(C)) + ...

So a group with `c` cycles contributes `± x^c · ∏ (L+(C) - L-(C))` plus higher powers of `x`. Two things are needed.

1. `L+(C) > L-(C)` for every cycle. One can choose the numbers `a` so that `L+(C) - L-(C)` is the number of white faces inside `C`. Route a unit of flow from every white face to the outer face and let `a` record the crossings [`LIT`, O Lemma 5.3; `PROVED-HERE` as a height function, route-combinatorics, AI-refereed]. By the disk identity that number is `B + 1`, at least 1.
2. All groups with the same number of cycles have the same sign. This is where the exact value in the disk identity is used. A counterclockwise cycle of length `h` contributes `(-1)^((h+3)/2)`. Multiplying over a cover gives `(-1)^((n-c)/2)`, so the group sign depends on `n` and `c`, although individual cycle signs depend on length.

Now let `m` be the smallest number of cycles of any cover. The coefficient of `x^m` in the total is a sum of positive products, all with one sign. It is not zero. By the first evaluation, a good state exists.

That is Proposition 5.1 of O: **if there is a pair, there is a pair with `Q_s` a forest.**

The other proofs of this step are the same computation in other clothes. O uses `e^{x a}` and a Taylor coefficient. Li counts sets of `m` distinct marked ray crossings and cancels them with a second involution. T uses an integer polynomial on each component of the exchange graph and also turns the two involutions into a walk that finds a good pair. Route N.H tests against a product of `m` heights of white faces and needs no weights at all. All of them take the lowest order at which something survives, and that order is `m`. It is unbounded even without separating triangles, according to the new T2 unreviewed construction in `research/2026-11-14_astra_cycle-covers/PROOFS.md`. On 3m+2 dual vertices it has one cover, m=m-1 and 2^(m-1) good states. The primal meaning is components(G-S)-1 for the admissible deletion S. The finite separator-free census reaches m=6 at V=23. First-order arguments cannot cover this family.

What nobody has is a version that avoids the minimum over covers, or a determinant that evaluates the sum without extracting a coefficient. The sum is a coefficient of one determinant, at the cost of `2^n` evaluations [`PROVED-HERE`, four agents independently, AI-refereed], and each plausible simplification (drop the extraction, allow doubled edges, make the blocks positive semidefinite) is `REFUTED` on an 8- or 9-vertex example.

## 6. The first pair, the last step, and the gluing

**The first pair.** Section 5 needs one pair to start from. Two disjoint perfect matchings in the incidence graph exist exactly when a Hall-type condition holds, and a planar Euler count verifies it when `T` has no separating triangle [`LIT`, O Proposition 3.1 by max-flow; L Lemma 9 by Ore's theorem]. The exact statement is sharper. A separating triangle has exactly one side whose faces along the triangle are black [`PROVED-HERE`, dependency-graph, unreviewed]. Call it the black side. A pair exists if and only if `t0` lies on the black side of every separating triangle [`LIT`, T Theorem 1.2; `COMPUTED` at all 7868 roots up to 16 vertices; a proof from one Euler identity is `PROVED-HERE` in route-graph-theory, independently AI-refereed by the structure referee]. This is the only place where separating triangles matter.

**The last step.** `P` has one edge in each face of `T`, so the rest of `G` is a union of cycles. Why one cycle? O and T show that `P` has no cycle in `T`. Such a cycle would be a state cycle, and counting selected sides gives its disk one black face fewer than the disk identity allows. Li argues differently, with an innermost cycle of `G` and a tree of faces inside it, and uses neither the disk identity nor the partner [`LIT`, O Lemma 6.2, L Lemma 30]. This is one of the three places on the map with real freedom.

**The gluing.** If `t0` is on the wrong side of a separating triangle, cut `T` along the triangle and cap both pieces with a new face. Solve one piece. Its solution tells you which edge of the cap the other piece must treat as its `e0`. Solve the other piece with that prescription and glue [`LIT`, O Section 7]. This is why the theorem is proved in the stronger form with a prescribed avoided edge. The induction needs the prescription to make the two halves agree, and one edge is the right amount. Prescribing arbitrary sets of edges is NP-complete for Barnette graphs [`LIT`, Bagheri Gh., Feder, Fleischner, Subi 2022]. The reduction itself was known to Kelmans in 1986.

## 7. What is forced and what is free

The map as a whole, step by step. `ROUTE-MAP.md` has the details in its section "Where the proofs are forced".

| Step | Published arguments | Alternatives found here | Verdict |
| --- | --- | --- | --- |
| dual, states, count | 1 (the Lean proof builds the dual algebraically) | hypotheses each shown necessary by a witness | forced |
| first pair | 4 | one exact Euler identity | free |
| disk identity | 1 | readings (one more white face; winding of the 3-colouring); a signed-angle Gauss-Bonnet derivation, AI-refereed with boundary corrections | forced |
| sign, cancellation with `s` fixed | 1 | determinant form | forced |
| nonvanishing | 5 | heights; linear weights | free |
| good pair to incidence tree to white tree to `P` | 1 | none sought | forced |
| `P` gives one cycle | 2 | restatements | free |
| gluing | 1 | exact condition for when to cut | forced |

The proof is rigid where it is new and flexible where it is technical. The pair, the disk identity and the two-way count have no known substitute.

## 8. What is still not understood

I would not call the problem understood yet, for four reasons the map makes visible.

- **No structural proof.** The target has nine exact unsigned reformulations (a spanning tree with prescribed degrees, a three-matroid intersection, a white tree with two label constraints, and others; routes U.1 to U.7). Each is `PROVED-HERE`. None has an existence argument, and the abstract version of the problem is NP-hard [`PROVED-HERE` modulo a cited theorem, route-graph-theory, under review]. So any structural proof must use the hexagonal faces of the spoke graph, which is what the disk identity does.
- **No canonical choice.** C2 is independently refuted first at V=18 and R2 at V=33. Rainbow exchange X passes all trees through V=17 and samples to V=120, but remains conjectural. Surplus walks can cycle at V=38; plateau search is essential.
- **No fast algorithm.** The proof gives exponential search. Good states can be exponentially rare among states, `2^j` among `3^j` in an explicit family [`PROVED-HERE`, limits, under review], so sampling states does not help.
- **How many.** C1, #TM >= 2^m, passes the independently reproduced all-root census through V=22 and a T4 separator-free census through V=24 on 23,824,742 facial roots. Only 2m is proved in general, with an AI referee. One-cover equality is independently AI-refereed; its converse remains open. The new two-cover proof is T2 unreviewed.

The smallest case shows the whole mechanism. For the cube, `T` is the octahedron. Three black faces meet `t0` in one corner each, and the three non-root vertices form the opposite white face. There are two states and they are disjoint, so there are two pairs. `D` is the triangle around the opposite white face in its two directions, and the disk holds one white face and no black face. Both `Q_s` are three edges, each joining a root to a non-root, so both states are good states. Their signs are opposite. With no weights the sum is zero. With the weight "one white face inside" the two terms differ at first order, and the sum is not zero [`COMPUTED`, several agents; the counts and signs also by `spotcheck.py`].


## Current written routes and unfinished shortcuts

Three complete written routes exist: `paper/main/` in the dual language, `proofs/primal/` entirely in G, and `proofs/involutions/` with distinct marked crossings and two finite involutions. Nothing here is human-checked.

The merged paper has an independent AI referee, verdict FOLLOWS for the main theorem, including the repair that makes the inside of a cycle connected before Euler's formula is used (`research/2026-11-14_sol_referee-main/REPORT.md`). Eight edits were proposed and a second version applying them is in progress. One of them matters for readers now: with these heights the off-route generating expression in Remark 4.10 is a Laurent polynomial. The paper uses the product of local signs, heights counted by turn signs along paths of faces, and an explicit connectivity lemma for the inside of a cycle. These simplify the explanation without removing the signed nonvanishing argument.

The involution note has an independent AI referee, verdict FOLLOWS, with one sign error off the route (`research/2026-11-14_opus_referee-involutions/REPORT.md`). Its revision applied all fifteen edits; a second referee of the revision has not reported. The note counts 279 marked objects on the running example and the digestion audit counted 213. Both are right. The two runs use the same `running.json` and the same Tutte drawing recipe, with roots 4 and 5 sent to each other's anchor points, a reflection of the drawing. Li's objects are ray crossings, so their number depends on the drawing (69 drawings give 35 values from 103 to 363); the signed sum and the nine second-fixed objects do not (`research/2026-11-14_opus_referee-involutions/DISCREPANCY-279-213.md`).

The primal proof was AI-refereed, revised and accepted in a cross-audit. The dispute over referee item M4 is settled: the primal note's real sign divided by the Lean phase is the constant `i^n` for every pair (`research/2026-11-14_opus_cross-audit/ADJUDICATION.md`). The upstream Lean proof was machine-checked in a local build. Of the 34 statements on the merged route, 4 have an exact Lean counterpart, 25 a counterpart in a different form whose translation is not formalised, and 5 none; the finite-difference lemma has a standalone Lean proof (`research/2026-11-14_opus_blueprint/REPORT.md`).

The unsigned contraction route has two exact gaps, ML1 and ML2, in `research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md`. Local splitting, lift criteria and rotation have an independent AI referee. A one-sided existence step is unreviewed. Direct lifting of even one contracted good state can fail at V=18, although rotation succeeds on that example. The follow-up run (`research/2026-11-14_astra_induction-lemmas/REPORT.md`) proves ML1 for triangulations without chordless five-cycles and shows that a repair for ML2 must sometimes change the cover; both stay open. The two-tree packing conjecture is proved, unreviewed, but it holds for any choice of one deleted corner per black face and so never sees the states (`research/2026-11-14_opus_two-tree-packing/REPORT.md`). C3 and rainbow exchange remain the other live descent questions. See [the open problems](../steps/09-what-is-still-open.md) for ranges, counterexamples and tests.
