# Induction toward the tree matching

Opus 5.5, 2026-11-14. Notation of `research/BRIEF.md`. Status tags as in the brief. Proofs are in `PROOFS.md`, every failed scheme with its smallest counterexample is in `data/failed_inductions.json`, and the commands are in `code/README.md`.

My verdict first. Induction by degree-4 contraction does reduce Proposition 5.1 to two clean combinatorial statements, and both hold on every Eulerian triangulation up to 17 vertices (15 for one of them). I proved the step that shows why they should hold: a lifting rule plus a three-face rotation covers 98.7% of the cases. The other 1.3% need a second rule I did not find. So the inductive cell of the route map is now "reduced to two conjectures, one of them 98.7% proved locally", not empty.

## 1. Generation theorems

| Statement | Status | Source I opened |
| --- | --- | --- |
| Every 3-connected Eulerian triangulation (dual of a 3-connected cubic bipartite plane graph) is generated from the octahedron by Batagelj's P- and Q-operations | `LIT` | plantri 4.5 source `workings/barnette_lab/vendor/plantri.c`: `initialize_bip` builds "the inital octahedron", `extend_bip_P` and `extend_bip_Q` are "the implementation of the P-operation [Q-operation] in Batagelj's paper", and `scanbipartite` recurses with exactly these two. Drápal, *On elementary moves that generate all spherical latin trades*, Comment. Math. Univ. Carolin. 50 (2009) 477-511, p. 477: "The graphs dual to the planar Eulerian triangulations can be obtained from the octahedron by the two moves of Batagelj [1]". |
| Batagelj's paper | `LIT`, not opened | V. Batagelj, *An improved inductive definition of two restricted classes of triangulations of the plane*, Combinatorics and Graph Theory (Warsaw 1987), Banach Center Publ. 25, PWN 1989, 11-18 (reference [1] of Drápal 2009, copied from there). |
| One of the two operations suffices if one starts from all even double wheels | `LIT`, abstract only | A. Drápal, P. Lisoněk, *Generating spherical Eulerian triangulations*, Discrete Math. 310 (2010) 1403-1405, doi 10.1016/j.disc.2009.12.023. I read the abstract on Lisoněk's publication page. The full text was paywalled, so I do not know which operation is the one that suffices. Drápal 2009, p. 477-478, says the move "contains in its graph version a central vertex". |
| 4-connected Eulerian triangulations (no separating triangle) | `LIT` for the enumeration method only | plantri's `-bc4` (`scanbipartite4c`) uses the same P/Q recursion and filters by tracking non-facial triangles, so the source does not give a generation theorem inside the 4-connected class. Matsumoto and Nakamoto, *Generating 4-connected even triangulations on the sphere*, Discrete Math. (2014), doi 10.1016/j.disc.2014.08.017, is the relevant paper. I saw only its bibliographic record, not the statement. |
| Brinkmann and McKay, *Fast generation of planar graphs*, MATCH Commun. Math. Comput. Chem. 58 (2007) 323-357 | `LIT`, not opened | The ANU server timed out. Its plantri guide (`vendor/plantri-guide.txt`) gives the counts below. |
| Every Eulerian triangulation without separating triangles and with `V > 6` has a degree-4 vertex whose contraction (in one of the two directions) is simple | `PROVED-HERE` in `research/2026-11-14_opus_route-graph-theory/PROOFS.md` Lemma 6.1, re-read by me: correct | |

The operations, read off the plantri source and checked by my own implementation (`code/tri.py`):

- **Q** (one new vertex, the inverse of the degree-4 contraction): split a vertex `v` along two of its edges `va, vb` into `v1, v2` and insert a degree-4 vertex `x` adjacent to `a, v1, b, v2`. The inverse `Q^-1` deletes a degree-4 vertex `x` and identifies two opposite neighbours. I call the two choices `M` (identify `v1, v2`) and `N` (identify `a, b`).
- **P** (two new vertices): replace an edge `xe` with faces `xae, xed` by the path `x b c e`, where `b, c` have degree 4 and are both adjacent to `a` and `d`. The inverse removes two adjacent degree-4 vertices with two common neighbours and restores the diagonal `xe` of the quadrilateral `x a e d`.
- **S** (in plantri's minimum-degree-4 class, not used for `-b`): glue an octahedron into a face. In our setting this is the white-face insertion of `research/2026-11-14_fable_route-categorical` Prop. 6.

Census used (plantri 4.5 `-b`, counts agree with the plantri guide table): `V = 6..17`: 1, 0, 1, 1, 2, 2, 8, 8, 32, 57, 185, 466 triangulations. Rooted instances: every face as root. My implementation agrees with `workings/barnette_lab` on the number of states, pairs and tree matchings for all 438 rooted instances with `V <= 13` (`code/check_lab.py`, `data/check_lab.txt`).

## 2. What each reduction does to the invariants

For each rooted `(T, t0)` and each reduction avoiding `t0` I computed: #states, #pairs, #D (undirected `D`-sets), `c_min`, the number of tree matchings, their signs, and `lc`, the lowest coefficient of `P(x) = F(1 + x a)` for the canonical spoke weights of OpenAI Lemma 5.3. These weights give every bounded face of `H0` circulation 1. A detour curve of a `D`-cycle `C` then encloses exactly the white triangles inside `C`, so `lc = sum over D with c_min cycles of prod_C (white faces inside C)`, an integer.

### 2.1 Degree-4 contraction (`Q^-1`), `V <= 17`, 344,872 rooted contractions (131,336 with a simple result)

| Law | Status |
| --- | --- |
| `#states(T) = #states(T/M) + #states(T/N)`, by an explicit bijection on four types of states | `PROVED-HERE` (PROOFS Prop. 1.1); `COMPUTED` 172,436 vertex-root pairs |
| Every TM of `T` is a lift for exactly one of `M`, `N` | `PROVED-HERE` (Prop. 1.1) |
| `#TM(T) >= #TM(T')`, the **contraction inequality** | `CONJECTURE`, `COMPUTED` on all 344,872 contractions, multigraph results included. It confirms and extends route-categorical's 948 cases. |
| `#states`, `#pairs`, `#D` never increase under contraction | `CONJECTURE`, `COMPUTED`, same range |
| `c_min(T) <= c_min(T')` when both have pairs | `CONJECTURE`, `COMPUTED`; equality fails 358 times (R9) |
| `lc(T) >= lc(T')` | `REFUTED`, `V = 14` (R8): `c_min` drops from 3 to 1 under expansion and `lc` restarts |
| `#TM(T) >= 2 #TM(T')` | `REFUTED`, `V = 8` (R7). Equality `#TM(T) = #TM(T')` is common |
| Pair existence is preserved | `REFUTED`, simple from `V = 11` (R2) |
| #TM is even and the signs balance | `PROVED-HERE` (Prop. 4.1); `COMPUTED` 21,848 rooted instances |

### 2.2 Inverse P-operation, `V <= 15`, 7,173 rooted reductions

`#TM(T) >= #TM(T'')` held in all of them (`CONJECTURE`, `COMPUTED`, `data/misc_6_15.jsonl`). The P-reduction loses the pair in 1,865 cases, including every reduction of the octahedron (R13), so it is a worse induction step than `Q^-1`.

### 2.3 Octahedron insertion (S, gluing at a separating triangle)

Inserting an octahedron into a face exactly doubles `#TM` if the face is white for the root, and leaves no pair if it is black (`COMPUTED`, every face of every rooted instance with `V <= 13`, `data/skein_oct.txt`). This re-checks a special case of route-categorical Prop. 6 ("states, pairs and tree matchings multiply under insertion into a white face"), which I use below without having re-proved it in general.

## 3. Deletion-contraction (skein) relations

The two contractions at one vertex give the cleanest relation in the data: **`#states(T) = #states(T/M) + #states(T/N)` exactly** (`PROVED-HERE`). A least-squares fit `Y(T) = alpha Y(T/M) + beta Y(T/N) + gamma` over the 58,530 vertex-root pairs with `V <= 16` gives `(1, 1, 0)` with zero residual for `Y = #states`, and no exact fit for `#TM` (residual 14.5), `#pairs` (19.4) or `lc` (279). `#TM(T) = #TM(T/M) + #TM(T/N)` holds in 86% of the cases and fails in both directions (R10, `data/analyse_6_17.txt`).

The reason is structural. A state of `T` has one of four types at `x`, two for each contraction, and the type determines the projection. A pair `(r, s)` can mix an `M`-type `r` with an `N`-type `s`, so pairs and `D`-sets do not split (`#D(T) = #D(T/M) + #D(T/N) + #(mixed D)`, where mixed `D` route the `D`-path through `x` as `a-x-v2` or `v1-x-b`). The tree-matching polynomial `F` inherits the split on its support, since every monomial is a TM of one type. But on each type the coefficient is the coefficient of `T/M` (or `T/N`) multiplied by a global side condition (PROOFS Prop. 2.1), so there is no linear skein relation for `F`. I found no third triangulation that repairs it.

## 4. The inductive scheme, and where it stands

Induction on `V` over rooted instances that have a pair.

1. **Base.** The octahedron: 2 tree matchings for every root.
2. **Separating triangle.** It is white-inner (a black-inner one excludes a pair, OpenAI Prop. 3.1 together with route-graph-theory Lemma 2.2). Split there and use multiplicativity (route-categorical Prop. 6, `PROVED` there, special case re-checked here).
3. **No separating triangle.** Choose a degree-4 non-root `x` whose faces avoid `t0`, and a merge `M` with `T/M` simple and still having a pair. Conjecture **(G)** says one exists. By induction `T/M` has a TM. Conjecture **(L)** says some TM of `T/M` lifts, or more strongly `#TM(T) >= #TM(T/M)`.

| Ingredient | Status | Evidence |
| --- | --- | --- |
| (G) good contraction exists, no separating triangle, `V > 6` | `CONJECTURE` | `COMPUTED`: 1,154 of 1,154 rooted instances, `8 <= V <= 15`, always with a simple `T/M` (`code/exp_misc.py`). With a separating triangle it can fail (`V = 9`, R12), which is why step 2 comes first. |
| (L) some TM of `T/M` lifts | `CONJECTURE` | `COMPUTED`: all 344,872 contractions, `V <= 17` |
| (L+) contraction inequality | `CONJECTURE` | same range |
| (L+) up to an exception set `E` | `PROVED-HERE` | PROOFS Cor. 3.3: lift, else rotate. `E` is 108 of 8,140 failing lifts for `V <= 15` |

### The lift and the rotation

With `beta1 = {x,a,v1}` and `beta2 = {x,b,v2}` black, a TM `s'` of `T/M` has exactly one `M`-type lift `s`. Let `tau' = Q_{s'} + root edges`, a spanning tree of `T/M`. Splitting `v` back into `v1, v2` cuts it into `K1 ∋ v1` and `K2 ∋ v2`. If `s'` takes `v` on the `v1` side, then `s` is a TM iff `a ∈ K2` (Prop. 2.1). If the lift fails, the black face `g = {a, v2, c}` across the edge `a v2` must take `a` (Lemma 3.1). Rotating the three values `x, v2, a` among `beta1, beta2, g` gives a state of the other contraction's type. That state is a TM unless `b` lies in the `v2`-part of `K2 - v2c` (Prop. 3.2). Lifts and rotations land in disjoint types, so the map is injective. The figure in words: a failing lift is a spanning tree with one edge "on the wrong side of `v`", and a rotation of three choices around the white face `{x, v2, a}` moves that edge across.

What is missing is a rule for the remaining case `b ∈ K2'`. The data show it is rare, that it involves a root neighbour of `x` up to `V = 13`, and that an injection still exists (`C >= b` in all 344,872 contractions). The probe `code/probe_injection.py` finds for `V = 14` (root-free) that 483 of 487 instances are covered by moves that change at most 3 faces, and the other 4 need moves of 5 or 11 faces.

## 5. Candidate induction hypotheses tested

The brief asked for the strongest `H` such that `H(T')` implies `H(T)`. Every true statement satisfies that implication trivially on the census, because the theorem is true. So I tested hypotheses in the form an induction would need: `H` true on every rooted instance with a pair, and `H` carried through the step by an explicit local rule. Results:

| Hypothesis | Holds on census? | Transfers by a local rule? |
| --- | --- | --- |
| TM exists (plain) | yes (theorem) | yes iff (G)+(L); local rule = lift or rotate, 98.7% |
| TM with a prescribed corner `s(t) = u` at a prescribed face (HCs) | **no**, fails at `V = 8`; holds in 13 of 1,794 instances (R11) | n/a |
| TM whose mate has `r(t) = u` (HCr) | **no**, `V = 8` (R11) | n/a |
| TM with a prescribed edge in `Q_s` (HQin) | **no**, same instances as HCs | n/a |
| No face is frozen: each `t`, `u` has a TM with `s(t) != u` (HQout) | yes, `V <= 15` (`CONJECTURE`) | not tested; too weak to control the lift |
| TM satisfying the local condition LC at a given split (edge `av ∈ Q`) | **no**, `V = 10` (R5) | LC implies the lift (Lemma 3.1) |
| TM whose lift at a given split is a TM | yes, `V <= 17` | this is (L); carrying it through the next step needs a two-split version, and so on. The global side condition is the obstacle |
| lowest coefficient positive and monotone | positive yes (theorem); monotone **no** (R8) | n/a |
| all boundary patterns on every 4-cycle | route-categorical Theorem 3, conditional on the theorem | not usable as a hypothesis without a decomposition along 4-cycles. Eulerian triangulations without separating triangles need not have separating 4-cycles, so it does not drive an induction by itself |

The lesson matches `research/2026-11-14_opus_history-literature/WHAT-WAS-HARD.md`: every local prescription is false already at 8 to 10 vertices. A hypothesis that survives must be either the bare existence statement or a statement about the specific split being undone. A split-specific hypothesis does not survive the next reduction, because a different vertex is split there. The workable form is therefore the counting form, the contraction inequality, which needs no hypothesis beyond existence.

## 6. Induction on `c_min` or along 4-cycles of `D` (task 5)

I did not get far here, and I say so. Two observations from the data:

- `c_min` does not decrease under contraction (`c_min(T) <= c_min(T')`, `COMPUTED` `V <= 17`). An induction on `c_min` would have to go the other way, toward instances with a Hamiltonian `D` (`c_min = 1`), where Li's Appendix A argument is simplest. Contraction moves away from them. I did not pursue this further.
- `D`-cycles have odd length (disk identity), so `D` has no 4-cycles. A "`D`-cycle of length 4" in the brief can only mean a 4-cycle of `T` crossing `D`. Route-categorical's 4-cut table needs `T` to have a separating 4-cycle. I did not test how often a separating 4-cycle exists, or whether the six patterns combine into a TM of `T`. That stays open.

## 7. Summary of status changes

- New `PROVED-HERE`: state deletion-contraction (Prop. 1.1); correct lift criterion (Prop. 2.1); local condition and rotation (Lemma 3.1, Prop. 3.2, Cor. 3.3); TM count even with balanced signs (Prop. 4.1).
- New `REFUTED`: the "only if" half of route-graph-theory Lemma 6.2(iii) (`V = 6`, simple `V = 11`), and twelve further schemes (R2-R13).
- `CONJECTURE` upgraded in range: contraction inequality, `V <= 12` (948 cases) to `V <= 17` (344,872 cases); P-reduction inequality, new; (G), new.
