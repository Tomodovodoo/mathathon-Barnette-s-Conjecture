# Report: graph-theoretic and structural routes to the tree matching

Opus 5.5, 2026-11-14, folder `research/2026-11-14_opus_route-graph-theory/`.

**Summary.**
1. The tree-matching condition is a three-matroid intersection (graphic and two partition matroids). Planar duality keeps it at three, so no Edmonds-type min-max applies.
2. The abstract problem is NP-hard. On planar bipartite graphs of maximum degree 3, deciding whether some perfect matching has a spanning-tree complement is NP-hard. The natural LP relaxation is not integral (first at `V = 13`). Verdict: not matroid intersection.
3. Every structural shortcut I could state and test fails, each with a saved counterexample: lattice extremes, every-2-factor, single-step descent, degree-4 induction, partitions = tree matchings. The smallest failures are at `V = 8` to `V = 80`.
4. Clean proofs: an exact Euler identity makes the pair-existence criterion a one-line computation. I also give the gluing step, the sharp primal hypothesis replacing Li's cyclic 4-edge-connectivity, and an exact description of which Hamiltonian cycles tree matchings produce.
5. Two live conjectures: (a) the face-flip min or the face-flip max of Felsner's lattice of pairs always carries a tree pair (0 joint failures in 180 instances); (b) the cycle count of `Q_s` can always be lowered without ever increasing it.

## What I set out to do

Find routes to the tree matching that use structure instead of a signed count, following the six directions in the brief. Test each by computer before investing in a proof. Write clean proofs of the surrounding steps.

## What I established

All proofs are in `PROOFS.md`, all routes in `ROUTES.md`, all code in `code/` (see `code/README.md`).

**Tools (`COMPUTED`).**
- An exhaustive generator of Eulerian triangulations by degree-4 insertions and face gluings. Completeness is PROOFS Lemma 6.1, and the counts are validated against an independent flip enumeration for `V <= 12`.
- The census for `V <= 16`: 1, 0, 1, 1, 2, 2, 8, 8, 32, 57, 185.
- Every random counterexample is saved as JSON and re-checked from scratch by a verifier script.

**Matroid verdict (direction 1).**
- `PROVED-HERE`: tree matchings are exactly the common bases of `M*(H)`, "one spoke per bounded centre" and "one spoke per nonroot". Equivalently, in `T`: the graphic matroid of `T/R`, one edge per bounded black face, and one edge opposite each nonroot. Tree/cotree duality maps this triple to a triple of the same kind, because the dual of a partition matroid is again a partition matroid. The second set of degree constraints never becomes a graphic condition.
- A restatement worth keeping: a tree matching is a spanning tree of the 6-regular white-face graph `H*` that contains exactly one edge of every face, except four faces it must avoid.
- `PROVED-HERE` modulo the cited NP-completeness of Hamiltonicity in cubic bipartite planar graphs (Akiyama–Nishizeki–Saito, not opened here): the abstract problem is NP-hard. So any min-max must use the hexagonal-face structure of spoke graphs.
- `COMPUTED`:
  - no constraint is redundant (octahedron and `V = 8`);
  - `TM` is not a matroid's base family;
  - the polytope "perfect matchings of `B` ∩ (1 − spanning-tree polytope of `H`)" has fractional vertices at `V = 13`. The one found is the average of two non-tree states.

**Exact obstruction and the first step (directions 5 and 6).**
- `PROVED-HERE`: for a connected induced subgraph `K` of `T`,

      m - b - (2p - 4) = (1/2) * sum over non-face regions of (beta - (d - 4)),

  where `beta` is the black-minus-white face balance of a region. With the signed side count this proves "pair exists ⇔ no separating triangle with black inner boundary" in a few lines, in both directions. It also shows that a single black-inner triangle violates the density bound by exactly one.
- `COMPUTED`: the criterion agrees with max-flow on all 7,868 rooted instances with `V <= 16`.
- `PROVED-HERE`: in the primal the obstruction is a nontrivial 3-edge cut whose black-ended side avoids `b0`. Li's cyclic 4-edge-connectivity is sufficient, not sharp: 1,714 of 4,494 rooted instances with separating triangles still have pairs. I also wrote a clean gluing proof that splits only at black-inner triangles.

**Orientation structure (direction 2).**
- `PROVED-HERE`: pairs up to reversing `D`-cycles are exactly the alpha-orientations of `H - t0` with out-degrees 2, `d_x - 2` and `d_r - 1`, equivalently the "deleted-corner" maps. So they form Felsner's distributive lattice.
- `COMPUTED`: the extremes of that lattice usually carry a tree pair, but each extreme alone fails: the minimum at `V = 40`, the maximum at `V = 80`.

**Induction (direction 3).**
- `PROVED-HERE`: under degree-4 expansion, states lift bijectively, and the lift of a tree matching is a tree matching iff a single side condition at the split vertex holds.
- `COMPUTED`: the step breaks in two ways. Contraction can create the obstruction (from `V = 11`). Not every tree matching of the smaller triangulation lifts (708 of 1,516 cases).

**Two induced trees (direction 4).**
- `PROVED-HERE`: the OpenAI map from tree matchings to induced-tree partitions is injective, with an explicit left inverse. Its image is exactly the partitions whose "white parent map" is acyclic.
- `COMPUTED`: it is not onto, even using both faces at `e0` (from `V = 8`).
- Grinberg's identity is automatic for two induced trees (`PROVED-HERE`), so Grinberg-type counting carries no information here.

## What failed, and why

- **Matching-lattice extremes** (`V = 10`): rotations around white triangles change `s`, but cycles of `Q_s` are reversed by changing `r`. The obstruction is invisible in the `s`-lattice.
- **Every 2-factor contains a tree pair** (`V = 40`) and **lattice minimum / maximum** (`V = 40` / `V = 80`): all three counterexamples are one-cycle 2-factors, where the only two ordered pairs `(r,s)` and `(s,r)` both have cyclic `Q`. A structural proof has to move between 2-factors.
- **Strong descent** is false for a structural reason. A swap along a Hamiltonian `D`-cycle exchanges `r` and `s`, so it cannot lower `k` both ways (`PROVED-HERE`). Exhaustive data up to `V = 15` had made it look true.
- **Weak descent** fails at `V = 50` (`data/deeptrap_50_1.json`, 4-connected). Two swaps suffice there.
- **Degree-4 induction**: the tree condition is global and the expansion is local. The needed side condition is not inherited.

The negative results agree with each other. The counting proof cancels globally inside exchange components. Every local or extremal rule I tried breaks on long `D`-cycles, typically Hamiltonian on `X`, where the `(r,s) <-> (s,r)` symmetry removes any local preference.

## What is still open

- **O6 (CONJECTURE)**: the face-flip min *or* the face-flip max always carries a tree pair. If true, it gives an explicit polynomial construction: flip to both extremes, then test `2^c` orientations, or better, a smarter search inside one 2-factor.
- **D3 (CONJECTURE)**: from every pair with `k > 0` there is a path of exchanges along which `k` never increases and reaches 0. This is a sign-free form of BT Theorem 5.2.
- A Hall-free (shelling) construction of a pair (F2, HUNCH).
- Whether facial flips generate Felsner's lattice for these `H_0` beyond `V = 12`. Rigid edges at the roots might create non-facial essential cycles. This matters for O4–O6.
- The delta-matroid / transition-system reading of pairs grouped by their 2-factor: not started.

## Three best next steps

1. **Attack O6 with a proof attempt and a C census.** The joint-failure count is the only structural regularity that survived. A census of Eulerian triangulations up to `V ≈ 24` (plantri `-b` when the ANU server is back, or a port of `tri.py`) would test it exhaustively where one-cycle 2-factors start to appear. The proof idea to try: in a one-cycle 2-factor `D`, the two orientations are related by the disk identity (δ-sum `-3` vs `+3`). The extremal flips should push `D` to the orientation whose `Q` is acyclic.
2. **Make D3 precise and test it on the exchange graph exactly**, for `V` around 20–30 where exchange components are still enumerable. If non-increasing paths always exist, look for the potential that the signed count is secretly tracking, for example `k` plus the number of `D`-cycles, or the depth `m` of the marked walk in BT Thm 5.3.
3. **Write the Euler identity (PROOFS Lemma 2.2) into the paper** as the single tool for both Prop. 3.1 and the cap-colour lemma. Use the injectivity theorem (PROOFS Thm 7.2) to explain to readers exactly which Hamiltonian cycles the proof produces, and why that set depends on the root.

## Leads for others

- **Complexity (for the constructive / algorithms agents).** Finding a tree matching is a total search problem. BT's marked walk (Thm 5.3) is a path-following argument in a graph of degree at most 2, with sign-alternating edges, so each phase looks like a PPAD instance. HUNCH: tree matching ∈ FP^PPAD. Worth stating carefully. PROOFS Prop. 1.2 shows the non-total general version is NP-hard.
- **Exposition.** "A spanning tree of the white-face graph `H*` with exactly one edge on every face" (PROOFS §1) is a short picture of the whole certificate. `H*` is 6-regular with triangle and `d`-gon faces.
- **Data.** `code/data/eul_*.json` is a reusable census of Eulerian triangulations up to 16 vertices, and `code/tri.py` can extend it, slowly in Python.
- Felsner's and Akiyama–Nishizeki–Saito's papers were cited from memory and not opened in this session. Someone with library access should confirm the exact statements before the paper uses them.
