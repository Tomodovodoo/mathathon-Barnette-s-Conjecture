# The Lean proof of Barnette's conjecture: structure and skeleton

Summary.
1. The formal proof never builds faces, rotation systems or the Jordan curve theorem. Planarity becomes an *algebraic dual*: a second oriented graph on the same edge set whose cut space is the cycle space of the first (Whitney's criterion over ℝ). It gets one by showing that a drawn graph is a minor of a square grid, that a rectangle grid has an explicit dual, and that duality survives deletion and contraction.
2. Everything after that is linear algebra and counting on the cubic graph `G` itself. The triangulation `T = G*` exists only as the dual network. Its faces are the vertices of `G`, and the inside of a cycle of `T` is the shore of a bond of `G` that misses the root vertex.
3. The induction statement is the primal edge-avoidance form: for every edge `e` of `G` there is a perfect matching containing `e` whose complement is connected. Theorem 2.2 (two induced trees) is never stated. The Jordan-curve labelling of Section 6.2 disappears.
4. The exponential sum is replaced by a polynomial, `exp(x a)` by `1 + a X`. The positive spoke circulations of Lemma 5.3 are replaced by one flow on `G` with a unit source at every white vertex and the sink at the root. The isotopy argument ("the spoke curve is simple and counterclockwise") is not needed at all.
5. Size: 31 files, 8,936 lines, 697 declarations. About 29% of the counted lines have no counterpart in the paper (embedding to dual 15%, algebraic duality layer 14%). The disk identity gets 13% of the Lean against 6% of the paper.

## Provenance

| item | value |
| --- | --- |
| repository | `https://github.com/openai/math` (blobless clone with sparse checkout in `upstream/openai-math/`, not committed) |
| commit read | `4eaee87548250b2682affda7d05d947c05554bae` (HEAD, 29 Oct 2026) |
| history of the proof files | `git log` on `lean/OAI/Combinatorics/Hamiltonian` and the challenge: one commit, `adc7f124` (initial commit, 6 Oct 2026) |
| commit replayed by cert-machine | `fd4aeeb2` (10 Oct 2026). `git diff fd4aeeb HEAD` on the 31 files, the challenge `.lean`/`.json`, `lake-manifest.json` and `lean-toolchain` is empty, so cert-machine checked exactly these sources |
| toolchain | `leanprover/lean4:v4.34.1` |
| Mathlib | `d13f23b723b8a846827a245b89c10fc7d3f11612` (from `lean/lake-manifest.json`) |
| files | `lean/OAI/Combinatorics/Hamiltonian/*.lean` (31 files), challenge `lean/ComparatorChallenges/BarnetteHamiltonian.lean`, config `BarnetteHamiltonian.json`, scope note `lean/docs/180.md` |
| imports | Mathlib only. The 31 files form a single linear import chain (each imports the previous one) |

The build is reported in `REPORT.md` and in the axiom section of `DIFFERENCES.md`.

## The import chain, in reading order

`Model → Network → CutSpaces → FlowCircuits → Bonds → Quotients → DiskRegions → StateDisk → Circulation → TriangleSystem → ColoredDual → CycleReversal → PairPhases → PairPolynomials → Forest → Contraction → MinorDuality → BMatching → Matching → ForestMatching → ThreeCuts → CappedDuality → Gluing → Traces → SquareGrid → Corridors → MinorModel → BranchPartition → Rectangle → ExactDual → Main`

The chain is linear, so file order says nothing about logical order. The declaration graph does. Picture: `graph/files.png` (files grouped by paper section, arrows from the declaration graph) and `graph/skeleton.png` (60 key theorems).

| group | files | lines | what it does |
| --- | --- | --- | --- |
| statement | Model | 50 | `PlaneEmbedding`, `Planar`, `ThreeVertexConnected`, `HasHamiltonianCycle`, `MainStatement` |
| algebraic duality | Network, CutSpaces, FlowCircuits, Bonds, Quotients | 1,441 | oriented networks, `gradient` and `boundary` maps, `Duality` = exactness, Euler from ranks, cycle = bond, minors of networks |
| disk identity (Sec 4) | DiskRegions, StateDisk, Circulation | 1,054 | the region network of a disk and its Euler count, the state count `B = I + l`, orientations of the black triangles, the white-charge flow |
| states and cancellation (Sec 5) | TriangleSystem, ColoredDual, CycleReversal, PairPhases, PairPolynomials, Forest | 1,892 | abstract triangle systems and states, the `Q_s` reversal, regrouping by `D`, polynomial nonvanishing, Proposition 5.1 |
| a pair exists (Sec 3) | Contraction, MinorDuality, BMatching | 1,101 | the density inequality on regions of `T[U]`, Hall's theorem for two disjoint matchings |
| recovery (Sec 6) | Matching, ForestMatching | 904 | Lemma 2.1, the root-sink trick (Lemma 6.1), tree to matching by Hall, Lemma 6.2 |
| separating triangles (Sec 7) | ThreeCuts, CappedDuality, Gluing | 1,020 | nontrivial 3-edge-cuts of `G`, the cap `G/A^c`, duality of the cap, gluing, induction on `|V(G)|` |
| embedding to dual | Traces, SquareGrid, Corridors, MinorModel, BranchPartition, Rectangle, ExactDual | 1,388 | drawing → compact branch sets → grid cells → minor of a grid → dual of a rectangle grid → dual of `G` |
| top | Main | 86 | 3-vertex-connected ⇒ 3-edge-connected, colouring, the 2-factor is one cycle |

## The objects

**Network.** `structure Network (V E) where tail : E → V; head : E → V` (`Network.lean:9`). A directed multigraph with edge type `E`. `gradient : (V → ℝ) → (E → ℝ)` and `boundary : (E → ℝ) → (V → ℝ)` are the coboundary and boundary maps.

**Duality.** `structure Duality (N : Network V E) (D : Network F E)` (`Network.lean:145`): both graphs connected, `ker ∂_N = im ∇_D` and `ker ∂_D = im ∇_N`. This is Whitney's algebraic duality with orientations, over ℝ. `Duality.euler` gives `|V| + |F| = |E| + 2` from ranks. In the main proof `N` is the Barnette graph `G` (vertices `V`) and `D` is `T` (vertices `F`, the faces of `G`). Primal and dual share the edge type `E`, so "the dual edge" is the same term.

**Faces of `T` are vertices of `G`.** `D.Triangle (N.star v)` (`CutSpaces.lean:222`) says the three edges at `v` form a triangle in `D`. `ColoredDual.face v` stores one for every `v`. A triangle comes with a cyclic labelling of its corners by `Fin 3`, and the field `oriented` fixes the labelling so that `∇_N 1_v` equals the cycle flow of the triangle (`Circulation.lean:100`, `oriented_face`). This is the only orientation data in the proof. It plays the role of "counterclockwise around each face".

**ColoredDual** (`ColoredDual.lean:13`) bundles: duality, `G` simple, `T` simple, `G` cubic, a 2-colouring `black : V → Prop` of `G`, the triangles `face v`, and their orientations. `make_coloredDual` (`ThreeCuts.lean:101`) builds one from a cubic 3-edge-connected simple graph with a dual and a 2-colouring.

**TriangleSystem** (`TriangleSystem.lean:9`). An abstract family of triangles `A`, each with three labelled vertices, such that two triangles sharing two vertices are equal. A `State X` is a corner index per triangle whose values form a bijection onto `X` (`TriangleSystem.lean:19`). `Partner r s` means the states differ at every triangle. `indexDelta i j ∈ {0, ±1}` is `+1` when `j` follows `i` in the cyclic labelling. This replaces `δ`: for a black triangle the corner labelling is the orientation, so `δ(v,w)` is `indexDelta` of the two labels (`Triangle.index_delta`, `TriangleSystem.lean:291`).

Sections 5.1 and 5.3 of the paper are proved for an arbitrary `TriangleSystem` with two hypotheses supplied from outside (`forest_pair_of_disk_circulation`, `PairPolynomials.lean:423`). One is that every reversible `Q_s`-cycle has index sum `±3`. The other is that every `D`-cycle has index sum `∓3` with weight slope of the opposite sign. Topology enters only through these two hypotheses.

**The inside of a cycle.** A simple cycle `C` of `T` is a minimal flow (circuit) of `D`. By duality its flow is `c · ∇_N 1_A` for a vertex set `A` of `G` that misses the root and a sign `c = ±1` (`Duality.circuit_cut`, `FlowCircuits.lean:71`). Minimality makes `cut(A)` a bond, so `A` and its complement are connected in `G` (`Bond.connected_shore`, `Bonds.lean:163`). `A` is the set of triangles inside, and `c` says whether `C` runs counterclockwise. No Jordan curve theorem is used. The "bounded side" is by definition the side without the root triangle.

## The skeleton

Edges are "uses", read top down. Each node gives the Lean name, the file and line, and its paper counterpart.

```
main  (Main:50)                                                        [Thm 1.1]
├─ ThreeVertexConnected → cut_card_three (CutSpaces:51)                 [Thm 1.1 proof, no 1-,2-cuts]
├─ cubic_bipartite_order (Network)                                      [|V(T)| >= 4]
├─ PlaneEmbedding.exists_exact_dual (ExactDual:116)                     [none: "fix a sphere embedding", "sphere dual"]
│   ├─ exists_lattice_corridor_model (Corridors:61)   thicken branch sets and arc cores, cover by grid cells
│   ├─ exists_lattice_minor_model (MinorModel)        clean connections inside corridors
│   ├─ lattice_minor_in_rectangle (Rectangle:303)     a finite box of the grid
│   ├─ grid_duality (Rectangle:180)                   explicit dual of the (2r)x(2r) grid
│   └─ Duality.graphMinor (ExactDual:96) ← Duality.minor (CappedDuality:62)   [Whitney: delete in G = contract in T]
└─ Duality.hamiltonian (Main:12)                                        [Thm 1.1, last paragraph]
    ├─ cycle_at_of_connected_two (CappedDuality:187)  connected 2-regular graph = one cycle
    └─ Duality.connected_complement_matching (Gluing:294)               [Thm 2.2 in primal form = Cor 7.1]
        └─ matching_strong (Gluing:244): strong induction on |V(G)|      [Sec 7]
            ├─ nontrivial 3-edge-cut A: cap_duality, cap_simple, cap_cubic, cap_coloring,
            │   cap_glue_matching, cap_glue_connected                     [split, cap, glue]
            └─ irreducible_matching (ThreeCuts:109)                     [Thm 2.2 without separating triangles]
                ├─ pair_nonempty (BMatching:403)                        [Prop 3.1]
                │   ├─ two_matchings (BMatching:286): Hall on a gadget graph, then a 2-regular bipartite graph splits
                │   └─ state_capacity ← capacity_full ← induced_density ← region_density, induced_euler_bound   [(3.1)-(3.4)]
                ├─ forest_pair (Forest:234)                             [Prop 5.1]
                │   ├─ boundary_of_sum_zero + whiteCharge (Circulation)  [replaces Lemma 5.3]
                │   ├─ opposite_disk (Forest:200) ← StateCycle.signed ← cycle_disk ← state_disk_delta   [Lemma 4.1 in Lemma 5.2]
                │   ├─ paired_sign (Forest:156) ← StateCycle.signed                                  [(5.3)]
                │   └─ forest_pair_of_disk_circulation (PairPolynomials:423)   abstract, for any TriangleSystem
                │       ├─ fixed_second_state_cancels (PairPhases:91) ← reverse_phase, reversal_involutive   [Lemma 5.2]
                │       └─ total_sum_ne_zero (PairPolynomials:348) ← groupEquiv, group_sum_product,
                │           cycle_factor_witness, common_phase_sum_ne_zero                            [(5.4), (5.5)]
                └─ recover_connected_complement (ForestMatching:375)    [Sec 6]
                    ├─ recovery_matching ← tree_matching (ForestMatching:51)   [Sec 6.1, rooting by Hall]
                    │   └─ remainder_independent ← removed_acyclic ← augQ_acyclic ← addSink_acyclic   [Lemma 6.1]
                    ├─ selected_forest (ForestMatching:338) ← selectNet_forest ← cycle_disk, matching_cut_balance   [Lemma 6.2]
                    └─ Duality.complement_connected (Matching:79)       [Lemma 2.1]

state_disk_delta (StateDisk:442)                                        [Lemma 4.1]
├─ Duality.circuit_cut, Bond.connected_shore                            [none: inside of a cycle]
├─ state_disk_count (StateDisk:260)  |black ∩ A| + |cut A| = |U| + |blackCut A|   [(4.2) B = I + l]
│   └─ mixed_corner_on_boundary (StateDisk:129)   a vertex of T touching both sides lies on C   [none: no pinch point]
└─ disk_boundary_imbalance (StateDisk:428)  |cut A| = 2 |blackCut A| + 3
    └─ region_euler (DiskRegions:252)                                   [(4.1) Euler for the disk]
```

The disk identity feeds three consumers: the `Q_s`-reversal (Lemma 5.2), the sign coupling on `D`-cycles ((5.3) with (5.4)), and Lemma 6.2. In the paper it also proves that `J` is an integer. The Lean does not need that (see `DIFFERENCES.md`, item 14).

## How the declaration graph was extracted

`scripts/extract_lean_graph.py` parses the sources with regular expressions. A declaration starts at a column-0 line with `theorem`, `lemma`, `def`, `structure`, `abbrev`, `instance`, `inductive` or `class`, after optional attributes and modifiers. It ends at the next declaration or at a column-0 `namespace`, `section`, `end`, `variable` or `open` line. Its name is qualified by the `namespace` stack. An edge `X → Y` is recorded when an identifier in `X`'s text resolves to project declaration `Y` that occurs earlier. A dotted token `a.b.c` is matched against declarations whose full name ends with `a.b.c`, then `b.c`, then `c`. Dot notation such as `hd.hamiltonian` resolves through its last component.

How approximate this is:
- 697 declarations, 4,097 edges. 1,647 edges are marked ambiguous. They resolve through a single name component, and either several declarations share it or it is a common Mathlib name (`symm`, `card`, `graph`, ...).
- Reachable from `OAI.Barnette.main`: 675 of 697 declarations with all edges, 601 with unambiguous edges only. The truth is in between. Of the 22 unreachable ones, 9 are instances or `@[simp]` lemmas that Lean uses without naming them. The rest look like genuine leftovers: the 3-vertex-connected versions `gradient_small_support`, `Duality.simple_dual` and `Duality.cubic_face_triangles` (superseded by the 3-edge-connected `..._edge` versions in `ThreeCuts`), `Bond.compl`, `disk_euler_count`, `state_nonempty_iff`, `cycle_group_polynomials_ne_zero` (superseded by `common_phase_sum_ne_zero`), and `disk_count_identity`. The last one is the paper's own algebra for Lemma 4.1, `B+W = 2I+h-2, 3(B-W) = 2l-h, B = I+l ⊢ 2l-h = -3`, stated and proved by `omega` in `PairPhases.lean:22` and then never used: the main route derives the identity in the form `|cut A| = 2|blackCut A| + 3` instead.
- Tactic proofs call lemmas through `simp` sets and `omega` without naming them, and the parser cannot see those uses. Local hypotheses that share a name with a declaration create false edges. The script suppresses names of the form `h`, `hX...`.
- Line counts are non-blank, non-comment lines from the declaration header to its end, proof included. They total 7,015 against 8,936 raw lines. The difference is blank lines, comments, `namespace` and `variable` lines.

Outputs: `graph/lean-decls.json` (every declaration with file, line, size, uses, used-by, the tokens behind each edge, reachability), `graph/lean-decls.dot` (reachable declarations clustered by file), `graph/lean-files.dot`, `graph/files.png`, `graph/skeleton.{dot,json,png}`. Graphviz is not installed, so the PNGs come from networkx and matplotlib (`scripts/render_graphs.py`). The skeleton keeps all edges except those created only by Mathlib-like names, then applies a transitive reduction.
