# Referee report on the rainbow route (Fable)

Referee: Opus 5.5, 2026-11-14. Refereed: `research/2026-11-14_fable_referee-topology/RAINBOW.md`, the proofs in its `REFEREE.md` that the brief names (claim (c), the retraction lemma; claim (h), lattice height), and its `REPORT.md`. I read Fable's code only to learn the file format of the saved counterexamples. Every number below comes from my own code in `code/` (about 700 lines, written for this report). Its only external input is plantri's rotation system (`plantri -b -a V`). Commands and outputs are in `code/README.md` and `data/`.

Notation is that of `research/BRIEF.md` and `digestions/steps/GLOSSARY.md`: good state, good pair, cover, `m`. Fable's "tree matching" is a good state. I write `W` for the white-face graph (Fable's `H*`), `F_σ` for `H` minus the spokes `(σ(x), x)`, and `d°(x)` for the number of black faces at `x`, which is half the degree of `x`.

## Verdicts

| Claim | Verdict |
| --- | --- |
| (a) Theorem R and identity (R) | CORRECT. One notation slip (the length of `C_x`) |
| (a') Lemma R2, a face-rainbow tree always exists | CORRECT |
| Lemma X1, the unique exchange | CORRECT |
| (b) Theorem S (1)-(3) and Proposition U | CORRECT. One sentence is needed in Proposition U, supplied below |
| (c) Lemma X3 and Corollary X4, `n` fixed-point-free involutions on good states | CORRECT |
| (d) lattice height equals signed white area | CORRECT, with one hypothesis made explicit (which direction of a clock move is "up") |
| (e) face-count proof of the retraction lemma | CORRECT |
| (f1) the surplus walk can be periodic | CORRECT. Four of the saved examples (`V = 38, 40`) replayed with my code, periods 48, 68, 68, 60 as claimed |
| (f2) strict descent fails at `V = 8` | CORRECT. Reproduced exactly (8,782 trees without a decreasing move for `V <= 12`) |
| (f3) the load vectors are not M-convex at `V = 12` | CORRECT. Same instance as Fable's (plantri index 2, outer face `{0, 1, 6}`), explicit witness in `data/S_6_12.json` |
| (g) Step X | Still a CONJECTURE. Restated below. Reproduced for all rootings `V <= 12`. Partial result on the `V = 18` cut-off set, below |

Nothing is WRONG.

## (a) Theorem R

**Statement.** Let `T` be a rooted Eulerian triangulation. A map `σ: X -> A` with `x ∈ σ(x)` is a *rainbow tree* if `F_σ` is a spanning tree of `H`. A rainbow tree exists iff no separating triangle of `T` has black inner boundary.

**Line-by-line.**

1. *Translation to Rado.* By tree and cotree duality in the plane graph `H` (whose dual is `W`, see my check below), `F_σ` is a spanning tree iff the `n` edges `e(σ(x), x)` form a spanning tree of `W`. `W` has `n + 1` vertices, so this is a basis of the cycle matroid `M(W)` that takes one element from each class `C_x = {e(t, x)}`. The classes are disjoint. Rado's theorem applies verbatim: in the exact form of Schrijver, *A Course in Combinatorial Optimization* (CWI, version of March 23, 2017), Exercise 10.26: "(X1, ..., Xm) has an independent transversal if and only if the rank of the union of any t sets among X1, ..., Xm is at least t" (Rado 1942). I opened that text in this session (`code/README.md` says how). Rado also follows in three lines from Edmonds' matroid intersection theorem (Schrijver, *Polyhedral combinatorics*, Handbook of Combinatorics ch. 30, Theorem 5.26, p. 1678, held in the project at `research/2026-11-14_sol_machinery-literature/source-text/`), so the citation is not load-bearing. Discharged.
2. *`H` and `W` are plane duals.* Not stated in RAINBOW.md beyond "is the plane dual". Check (mine): the face of `H` around a white face `w` with corners `v1 v2 v3` has boundary `v1, c(t1), v2, c(t2), v3, c(t3)`, where `ti` is the black face across the side `vi v(i+1)`. So the faces of `H` are the `n + 1` white faces, and the spoke `(t, v)` separates the two faces of `H` that contain the white faces across the two sides of `t` at `v`. Euler agrees: `|E(H)| - |V(H)| + 2 = 3n + 3 - (2n + 4) + 2 = n + 1`. Discharged. My code builds `W` from this rule and checks every rainbow tree it finds both as a forest of `W` and as a complement tree in `H`.
3. *Rank of a union.* `C_x` is a cycle of length `d°(x)` (RAINBOW.md says "length `d_v`" and "two parallel edges if `d_v = 2`", so its `d_v` is my `d°`; with the brief's degree it should read `d_v / 2`). Two classes share a white face iff the points are adjacent, so the rank of `⋃_{x ∈ J} C_x` is `w(J) - comp(T[J])`. The reduction to connected `J` is correct because white faces of different components are distinct. Discharged.
4. *Faces of `T[U]`.* For connected `J` and `U = V \ J`, the faces of `T[U]` are one face `Φ ⊇ J` and the faces of `T` with all corners in `U`. Both inclusions are argued correctly. For the converse inclusion I add one sentence: an open face of `T` whose three sides lie in `T[U]` is open and also closed in `S^2 \ T[U]`, hence a component. Discharged.
5. *The three counts and (R).* I redid the elimination. From `σ_Φ = 3(w_U - b_U)`, Euler `p - m + b_U + w_U + 1 = 1 + c` and `2m = 3(b_U + w_U) + d` one gets `w_U = p - c - d/2 + σ_Φ/6`, and with `w(J) = n + 1 - w_U`, `|J| = n + 3 - p`, identity (R) follows. Discharged.
6. *Sign analysis.* `d >= 3` needs every component of `T[U]` to border `Φ` or at least one with a cycle to do so. RAINBOW.md argues the second via the root component, correctly. The case table (`c >= 2`; `c = 1` and `d = 4, 5, >= 6`; `c = 1, d = 3`) is complete and each line is right. In the case `d = 3`, `σ_Φ = 3`: `U ⊇ R` because `J ⊆ X`, so `t0` is a face of `T[U]` other than `Φ`, and `Φ` is the inner side. Discharged.
7. *Converse.* The disk count for a triangle with black inner boundary: `h = 3`, `l = 3`, so `B = I + (h + l)/3 - 1 = I + 1` and `W - B = (h - 2l)/3 = -1`, `W = I`. I verified both formulas from Euler and the signed side count. Every white face with a corner inside lies inside, so `w(J) <= |J|` and the rank is at most `|J| - 1`. Discharged.

**COMPUTED (mine).** `check_rainbow.py R 6 12`: all 262 rootings with `V <= 12`. Identity (R) holds exactly on all 57,901 connected sets `J`. The 68 sets with negative left side all have `(c, d, σ_Φ) = (1, 3, 3)` and every one is the interior of a black-inner separating triangle. In all 262, "rainbow tree exists" (my matroid intersection), "a 2-factor of `B` exists" (my max flow) and "no black-inner separating triangle" agree: 208 yes, 54 no. These are Fable's numbers exactly, from independent code. I did not run this check above `V = 12`; Fable's run covers `V <= 16`. The packing run (`data/PACK_6_14.log`) confirms "pair exists iff no black-inner triangle" for all rootings `V <= 14`.

**Lemma R2.** Correct as written. The step "equality forces `S_i ∪ N(S_i)` to be closed under adjacency of faces" uses that a black face of `S_i` has all three white neighbours in `N(S_i)` by definition and a white face of `N(S_i)` has all three black neighbours in `S_i` by the equality. COMPUTED: a face-rainbow tree exists in all 262 rootings `V <= 12` and all rootings to `V = 14` (`data/R_6_12.json`, `data/PACK_6_14.log`, field `cor3.2a` for supports).

**Lemma X1.** Correct. COMPUTED by brute force (all `d°(x) - 1` alternatives tried, not the fundamental cycle): 651,072 (tree, point) pairs for `V <= 12`, exactly one alternative each, and it equals the fundamental-cycle answer.

## (b) Theorem S and Proposition U

**Statement.** For a rainbow tree `σ`, with `F_σ` rooted at the centre of `t0` and `par_σ(x)` the parent of `x`: (1) `σ ⊔ par_σ` is a 2-factor of `B`; (2) it is the only 2-factor containing the edges `(x, σ(x))`; (3) for a 2-factor with deleted-corner map `u` and digraph `G_u` (arcs `v -> u(t)` from the two used corners of `t`), a choice `σ` of one edge per point inside the 2-factor is a rainbow tree iff the unused arcs `x -> u(σ'(x))` are acyclic, and it is a good state iff in addition it uses one arc of every face.

**Check.** (1) The neighbours of `x` in `F_σ` are its black faces other than `σ(x)`, one of them its parent; the centre of `t` has `3 - c_σ(t)` neighbours, one its parent (a corner of `t`), so `2 - c_σ(t)` children. Correct. (2)-(3) The orientation `x -> σ'(x)`, `t -> u(t)`, `r -> t0` gives every spoke of `H - σ` exactly one direction: the spokes at a non-root `x` other than `σ(x)` are `σ'(x)` and the spokes `(t, x)` with `u(t) = x`, and nothing else, because a spoke `(t, x)` outside the 2-factor has `x = u(t)`. So `H - σ` is a functional digraph on `2n + 4` vertices with one sink and `2n + 3` arcs, a tree iff acyclic, and then the orientation is the one towards the root, which forces `σ' = par_σ`. This proves (2) for every 2-factor containing `σ` at once. Correct. The good-state clause: the arc from `v` through `t` is used iff `σ'(v) = t`, so "one arc per face" is `c_{σ'} ≡ 1`, equivalently `c_σ ≡ 1`. Correct.

**Proposition U.** The direction "a directed cycle gives a second 2-factor" needs the faces `t_i` on the cycle to be distinct. They are, because `u(t_i) = v_{i+1}` and the `v_i` of a simple directed cycle are distinct. For the converse, RAINBOW.md says "the symmetric difference of two 2-factors is a union of alternating cycles". At a point the symmetric difference can have degree 4 (two edges `(x, t)` with `u(t) = x` in the new factor), so "alternating closed trails" is the right word. Each such trail gives a closed directed walk in `G_u`, which contains a directed cycle. The conclusion stands; I would replace "cycles" by "closed trails" (fix, mine).

**COMPUTED (mine), `check_rainbow.py S 6 12`, all rootings `V <= 12` with a rainbow tree (208 instances, 74,432 rainbow trees by brute force over all `Π d°(x)` maps):** (1) and (2) hold for every tree; the unique 2-factor is found by enumerating all 2-factors; (3) holds for all `2^n` selections of every 2-factor (acyclic iff rainbow), and the rainbow trees are partitioned by their 2-factors; Proposition U's equivalence (directed cycle iff more than one 2-factor) holds in all 208; with one 2-factor there are exactly `2^n` rainbow trees (206 instances); two instances have two 2-factors.

## (c) Evict the resident: `n` fixed-point-free involutions

**Statement.** For `t ∈ A` and a good state `s`, move `s(t)` out of `t` by its exchange, then repeatedly move the resident (the point of the doubly loaded face that did not just arrive) by its exchange, until a move lands in an empty face. The result `ι_t(s)` is a good state, `ι_t(ι_t(s)) = s` and `ι_t(s) ≠ s`. Hence the number of good states is even.

**Check.** I went through Lemma X3 and Corollary X4 step by step.

- A walk state has excess exactly 2 throughout (moves of type `(2, 1)` keep it), so the only empty face is `t`, and a stop is a move into `t`. Correct.
- Injectivity: `mirror ∘ step ∘ mirror` is a left inverse of `step`. Spelled out: from `(σ', t', y)`, mirroring gives arrival `z` (the old point of `t'`) and resident `y`; moving `y` uses the same fundamental cycle, so it returns to `t`, which has load 1, giving `(σ, t, y)`; mirroring gives `(σ, t, x)`. Correct.
- The first walk state `(σ_1, t_1, x_0)` has no predecessor, because the backward move sends `x_0` into the empty face `t`. So its orbit is a path, not a cycle, and the forward walk terminates. This is the point that makes the involution well defined even though periodic orbits exist elsewhere (f1). Correct and important.
- Reversal: the walk from `s'` at `t` begins with `mirror(u_m)` and its states are `mirror(u_{m-1}), ..., mirror(u_1)`, then stops at `s`. Correct.
- No fixed point: the parity argument (odd `m`: the middle state equals its mirror, impossible since the arrival changes; even `m`: two consecutive states share a tree, impossible since a step changes the tree) is complete. I add that `m >= 1` always.

The proof uses no sign, no weight and no planarity beyond Lemma X1. It shows evenness of the number of good states for every rooted instance with `n >= 1`. Together with existence it gives "at least two". It does not give existence.

**COMPUTED (mine).** `ι_t` for every good state and every `t ∈ A`, all rootings `V <= 12`: 5,052 evaluations, each a good state different from `s`, each `ι_t(ι_t(s)) = s`. The number of good states is even in all 208 instances (620 good states in total, which also equals the number of rainbow trees of excess 0).

## (d) Lattice height equals signed white area

**Statement.** Without separating triangles, for any two states `r, s` and any path of clock moves from `r` to `s`, (number of counterclockwise moves) minus (number of clockwise moves) equals `Φ(r, s) = Σ_C ε(C) W_in(C)`, the sum over the cycles of `D(r, s)` of the white faces enclosed on the side away from `t0`, signed by orientation.

**Check.** The 1-chain `s - r` on spokes is the sum of the spoke detours of the cycles of `D(r, s)`. A detour sweeps only the interior of one black triangle, so it encloses the same white faces as the straight cycle. The winding number around a point of a white face (on the sphere punctured inside `t0`) is linear in the chain, so `Φ(r, s) + Φ(s, q) = Φ(r, q)`. A clock move has a single 3-cycle as relative cycle. A 3-cycle of `D` avoids the roots, so if it bounds a face of `T` that face is not `t0` and lies on the side away from `t0`, and by `W = B + 1` it is white. So every clock move changes `Φ` by `±1`. Correct.

What must be added: the statement "height difference equals `Φ`" identifies the lattice order of Hine and Kálmán with "counterclockwise is up". The proof shows that the signed count of moves along a path is path-independent and equals `Φ`; it is the lattice height difference once one fixes that convention. That is a convention, not a gap. Separately, `D` has no 2-cycles (an edge of `T` has one black face), so the shortest relative cycle is a 3-cycle around a white face. I did not recompute (d); Fable's own check is `referee.py height 12`. Verdict CORRECT.

## (e) The retraction lemma by counting faces

**Statement.** Let `P ⊆ E(T)` contain exactly one edge of every face of `T`, and let `c` be the number of cycles of the 2-factor of `G` dual to `E(T) \ P`. Then the plane graph `(V(T), P)` has `b_1 = c - 1` and `b_0 = c + 1`.

**Check.** `S^2` minus the vertices and the edges of `P` is the union of the open faces of `T` and the open edges not in `P`. Its components, the faces of `(V(T), P)`, are therefore the classes of faces of `T` joined across edges not in `P`, which are the cycles of the dual 2-factor. Euler for a plane graph with `b_0` components, `|V| - |P| + c = 1 + b_0`, and `|P| = |V| - 2` give both claims. Correct and complete. It is three lines and should replace the homotopy argument in any write-up. Dual statement, standard: Schrijver's course notes, Theorem 10.3 (rank function of the dual matroid).

## (f) The refutations

- **(f1) Periodic surplus walks.** `code/verify_periodic.py` loads only the rotation system, the outer face and `σ` from Fable's JSON, checks that `σ` is a rainbow tree with my code, and follows every walker. Results (`data/periodic.json`): the three `V = 38` trees of `cycles_hunt_38_400_19` have periodic walkers with exact periods 48, 68, 68, and the `V = 40` tree of `cycles_hunt_40_200_5` has period 60, both walkers in each case. These match RAINBOW.md §4. REFUTED stands. The other saved files use a different key layout and I did not replay them.
- **(f2) Strict descent.** My run finds the first rainbow trees of positive excess without a decreasing move at `V = 8` (120 of them), and 8,782 for `V <= 12`, Fable's number. One saved example: `data/S_6_12.json`, `strict_descent_fails`.
- **(f3) M-convexity.** Murota's exchange axiom fails at `V = 12`, plantri index 2, outer face `{0, 1, 6}`; the two load vectors and the index are in `data/S_6_12.json`. In the 206 instances with one 2-factor the axiom holds (exhaustive, not sampled), in both instances with two 2-factors it fails. This agrees with Fable's explanation (Minkowski sum when there is one 2-factor).

## (g) Step X

**Precise statement (CONJECTURE).** Let `T` be a rooted Eulerian triangulation without a separating triangle with black inner boundary, and let `𝓡` be the set of its rainbow trees, with the move graph of Lemma X1 (an `n`-regular graph, each move an involution). For every `σ ∈ 𝓡` there is a sequence of moves `σ = σ_0, σ_1, ..., σ_k` with `exc(σ_{i+1}) <= exc(σ_i)` and `exc(σ_k) = 0`.

Equivalent form used for computation: let `𝓖` be the set of trees reachable from the good states by moves that never decrease the excess (moves are involutions, so this is the set that can descend). Step X says `𝓖 = 𝓡`.

What it would give, with Theorem R and Theorem S: a good state, hence a good pair, with no signed count. What it would not give is in INTEGRATION.md §5.

**Reproduction.** `check_rainbow.py S 6 12`: `𝓖 = 𝓡` in all 208 rootings with `V <= 12` (74,432 trees). This is Fable's range `V <= 12` reproduced with independent code.

**The `V = 18` cut-off set.** See `code/README.md` and `data/stepx_18_*.json` for what my time-boxed run covered; the summary is in `REPORT.md`. My enumeration uses Theorem S (rainbow trees are the acyclic selections inside 2-factors), which I verified against brute force for `V <= 12`, and Proposition U for rootings with one 2-factor.

## Dependency table (bounded to the refereed claims)

Accepted primitives: Euler's formula for plane graphs (with `b_0` components), the signed side count, the Jordan curve theorem, Rado's theorem (Schrijver course Ex. 10.26), Edmonds' matroid intersection theorem (Schrijver handbook Thm 5.26), and the disk identity `W = B + 1` (OpenAI Lemma 4.1, refereed elsewhere in the project).

| ID | Claim or obligation | Needed by | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- |
| R0 | Theorem R | root | major claim | R1-R6 | discharged |
| R1 | `H` and `W` are plane duals; tree-cotree | R0, S0 | algebraic/logical step | §(a) item 2 (mine) | discharged |
| R2 | rank of `⋃ C_x` is `w(J) - comp(T[J])` | R0 | algebraic/logical step | RAINBOW §2 step 1 | discharged |
| R3 | Rado | R0 | named theorem | Schrijver course Ex. 10.26 | discharged |
| R4 | identity (R) | R0 | algebraic/logical step | three counts | discharged |
| R5 | sign analysis, `d >= 3` | R0 | side condition | RAINBOW §2 step 5 | discharged |
| R6 | converse via `W = I` in a black-inner triangle | R0 | algebraic/logical step | disk count | discharged |
| X1 | unique exchange | S0, C0 | algebraic/logical step | RAINBOW Lemma X1 | discharged |
| S0 | Theorem S (1)-(3) | INTEGRATION | major claim | orientation argument | discharged |
| U0 | Proposition U | S0 consequences, (g) | algebraic/logical step | "cycles" should read "closed trails" | discharged after fix |
| C0 | `ι_t` is a fixed-point-free involution | root | major claim | X1, injectivity, start state is an end | discharged |
| D0 | height = `Φ` | root | major claim | winding numbers, `W = B + 1`, Hine-Kálmán connectivity | discharged, convention stated |
| E0 | `c = 1 + b_1(P)` | root | algebraic/logical step | face count | discharged |
| G0 | Step X | INTEGRATION §5 | CONJECTURE | computed only | open |

## Verdict

FOLLOWS for Theorem R, Lemma R2, Lemma X1, Theorem S, Proposition U (after replacing "cycles" by "closed trails"), the involutions `ι_t`, the height identity and the retraction lemma. The three refutations are reproduced. Step X remains a conjecture. Review state for the PROVED-HERE items: refereed (1 independent AI referee, this report; Fable is the author); human check pending; tier T2.
