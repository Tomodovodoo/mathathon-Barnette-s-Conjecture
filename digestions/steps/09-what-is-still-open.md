# 09. What is still open

The supplied 2026 preprints prove the existence theorem. The questions here concern a shorter proof, an efficient construction, and the structure of its certificates. No claim in this project is human-checked. `PROVED-HERE` means T2, even after an AI referee; `COMPUTED` states only a finite result. Independent exhaustive implementations can justify T3 for their stated range. Unchecked numerical campaigns remain T4.

Throughout, V is the dual order |V(T)|. A feasible root has at least one pair. A cover is the unoriented D of a pair, equivalently a degree-two factor of the incidence graph. Its two directions per component give 2^c ordered pairs. The minimum c over covers is c_min. It is not the number of cycles in Q_s. A tree matching is a state whose spoke complement is a tree, equivalently a state with exactly one partner.

## What c_min measures now

`PROVED-HERE`, T2 unreviewed, [cycle-cover proofs](../../research/2026-11-14_astra_cycle-covers/PROOFS.md). Under the primal dictionary, an admissible edge set S has c(D)=components(G-S)-1. Thus c_min asks how few components such a deletion can leave, less one. This is a connectivity invariant, not merely the order at which an analytic trick begins to work.

The same run gives a separator-free family T_m on 3m+2 dual vertices, with one cover, m-2 triangles and one pentagon. It has c_min=m-1 and #TM=2^(m-1). The construction is unreviewed. Its [family data](../../research/2026-11-14_astra_cycle-covers/data/family.json) include independent corner enumeration through m=10 and reference pair checks through m=6, all by the author. Separator-free unboundedness should therefore be marked as an author-proved result awaiting review, rather than an untouched conjecture. Unboundedness with bounded primal face sizes and no separating triangles remains open. The two large faces in this family prevent that conclusion.

## Ten open doors

### 1. C1, the exponential number of tree matchings

`CONJECTURE`, T5. Every feasible rooted triangulation has #TM >= 2^c_min. The proposed equality characterization says equality holds exactly when there is one cover. The forward implication from one cover is `PROVED-HERE` and independently AI-refereed in [the conjecture referee](../../research/2026-11-14_sol_referee-conjectures/REFEREE.md). The converse remains open.

`COMPUTED`, T3 for the independently reproduced finite statement. All 9,531,638 facial roots through V=22 were enumerated, including 4,656,948 feasible ones. There were no violations of either assertion. The [per-order outputs](../../research/2026-11-14_sol_referee-conjectures/data/fast_census_summary.json) and `code/count.cpp` record the replay. `COMPUTED`, T4 under review, the [cycle-cover census](../../research/2026-11-14_astra_cycle-covers/CENSUS.md) extends evidence to V=24 on 23,824,742 facial roots of 4-connected triangulations. This does not extend the all-triangulation census to 24.

The moment route has a precise limitation. Low-degree vanishing plus one nonzero degree-c_min moment does not force 2^c_min atoms. The referee's small integer examples prove that barrier. They do not settle what follows from the full prescribed family of minimal-cover counts N(w). The next useful step is to exclude the one exceptional planar overlap in the unreviewed two-cover proof, then extend its shared-state calculation to more covers.

### 2. ML1, a pair-preserving contraction

`CONJECTURE`, T5. If T has no separating triangle and V>6, some non-root degree-four vertex has an opposite-neighbour merge producing a simple rooted triangulation with a pair. Simplicity alone is insufficient. A merge can create a black-inner separating triangle.

`COMPUTED`, T4, all 62,416 separator-free facial roots with 8<=V<=19 pass, in [MISSING-LEMMA.md](../../research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md). The new reductions to short 4- and 5-cycles, deficiency and tight sets are T2 unreviewed. The earlier local contraction propositions were independently AI-refereed. The next step is to check the minimal-tight-set reduction and prove that one interior degree-four vertex escapes the bad boundary-apex pattern. A graph generation theorem does not supply this rooted statement.

### 3. ML2, the two-sided lifting step

`CONJECTURE`, T5. At a non-root degree-four vertex, if both opposite merges have tree matchings, not every tree matching of either contraction is exceptional in the precise sense of [the residual-case analysis](../../research/2026-11-14_fable_induction-completion/RESIDUAL-CASES.md). Equivalently, some matching lifts or rotates successfully. The one-sided case is T2 unreviewed and proved there.

`COMPUTED`, T4. The stronger counting inequality #TM(T)>=#TM(T/M) passes 1,202,792 rooted contractions through V=18. Direct lifting is false. At V=18, graph 309, root (5,0,6), x=11, merge {10,2}, both contracted tree matchings fail to lift and both rotate. There are 50 such rooted contractions in [nolift_18.jsonl](../../research/2026-11-14_fable_induction-completion/data/nolift_18.jsonl). No smaller direct-lift existence failure was found in that census. An injection from exceptional into non-exceptional matchings would prove more than existence; start by testing the proposed one-half bound. The later induction-lemmas run must be checked before claiming that these two doors remain unchanged.

### 4. C3, monotone descent among pairs

`CONJECTURE`, T5. Every ordered pair reaches a forest pair by D-swaps and Q-reversals along a path on which the number of cyclic Q-components never increases. Plateaus are allowed. This is an existence statement about paths, with no polynomial bound on finding them.

`COMPUTED`. The author reports 940 successful starts. Independent reverse reachability checks every one of the 24,744 ordered pairs through V=16 and all pairs on both saved plateau traps. See [REFEREE.md](../../research/2026-11-14_sol_referee-conjectures/REFEREE.md) and [cancellations_16.json](../../research/2026-11-14_sol_referee-conjectures/data/cancellations_16.json). Strict descent already fails. The next step is to search for a closed plateau component with positive Q-cycle count, rather than run another greedy trajectory that might miss an exit.

### 5. Rainbow exchange X

`CONJECTURE`, T5. Every point-rainbow white spanning tree reaches a tree matching by exchanges that never increase black excess. The new Rado-Euler existence criterion and the unique-factor completion theorem are T2 unreviewed in [RAINBOW.md](../../research/2026-11-14_fable_referee-topology/RAINBOW.md). The older topology dictionary and Gauss-Bonnet proof were independently AI-refereed, with corrections.

`COMPUTED`, T4. X passes every rainbow tree through V=17. The report enumerates about 69 million trees, with singleton-factor cases handled by its proposition, and samples to V=120. The surplus walk alone is false: periods 48 and 68 occur at V=38. The minimum failure is only bounded between 17 and 38. Certificates are in `data/cycles_hunt_*.json` and [cycles_analyse.json](../../research/2026-11-14_fable_referee-topology/data/cycles_analyse.json). Strict descent fails at V=8, and load M-convexity at V=12. The next proof must use both types of plateau move. Establishing X would still leave a runtime bound open.

### 6. Two-tree packing and exact rounding

`CONJECTURE`, T5 at this snapshot. Every selected pair support partitions into two white spanning trees. The [probabilistic report](../../research/2026-11-14_sol_route-probabilistic/REPORT.md) has 278 nonvacuous small rank tests and 27 larger checked packings through V=120, all T4 unreviewed. The dedicated two-tree-packing run has not yet delivered a REPORT at the initial integration.

Packing would give fractional feasibility. Exact joint-degree rounding is another problem. The full-H target mean cannot be attained by finite positive weights, already on the cube; the target forces root spokes. The joint degree support is not M-convex. Work on the conditioned face and prove the relevant rank inequalities first. Do not treat a fractional point as a tree matching.

### 7. Direction choice and lattice structure

`CONJECTURE`, an algorithmic problem. Given a factor u, decide whether some direction of each D-cycle gives a forest pair, and find one if it exists. Testing a specified pair takes linear time by the independently AI-refereed directed-cycle criterion, checked on every pair through V=18. The forbidden-cycle SAT formulation can have exponentially many clauses. It gives no efficient direction-selection algorithm and no hardness theorem for this planar class.

Canonical boundary choices have failed. C2 first fails at V=18, with a four-element lattice, 54 states, 20 pairs and 12 tree states. Both extremes fail. Independent exhaustive minimality and the full certificate are in [v18.json](../../research/2026-11-14_sol_referee-conjectures/data/v18.json). R2, extreme or join/meet irreducible, fails at V=33, in [R2_glued_V33.json](../../research/2026-11-14_sol_referee-conjectures/data/R2_glued_V33.json) and its independent second certificate. All ten candidates fail. The lattice is B_4 and successes occur only at rank two. This witness has separating triangles; the restriction of R2 to separator-free inputs remains a new question. Test that restriction while searching for a direction-selection theorem on a fixed factor.

### 8. A determinant without extraction

`HUNCH`, T6. A structured determinant or Pfaffian might evaluate the signed sum without an exponential squarefree extraction. Existing formulas express the sum as a coefficient, not a polynomial-time evaluation procedure. Raw block determinants, doubled edges, positive-semidefinite blocks and scalar factorization have explicit failures in [the determinant referee](../../research/2026-11-14_fable_referee-determinants/REFEREE-dimers.md). A new candidate must reproduce the small signed polynomials and the orientation cube over each lattice element. The signed sum is not the ordinary rank polynomial of the base lattice, even when that lattice is a singleton. Test a local turn signature against matchgate identities before pursuing another global determinant.

### 9. Which cycles are recovered?

`CONJECTURE`, T5. Find a criterion in G alone for a Hamiltonian cycle avoiding the prescribed edge to lie in forest-pair recovery. Recovery is injective on tree matchings and is not surjective on all avoiding cycles. On the hexagonal prism four cycles avoid a given edge, two are recovered, and the other two can give the same unpartnered state. The small replay is [spotcheck.py](../../research/2026-11-14_fable_labyrinth-map/spotcheck.py). The revised primal compatible-state theorem concerns a broader correspondence and does not prove forest-pair surjectivity. Compare the two excluded cycles locally, then test the proposed criterion on the saved census.

### 10. Formal and human verification

`COMPUTED`. The upstream Lean theorem builds locally with only `propext`, `Classical.choice` and `Quot.sound`, as recorded in [the Lean report](../../research/2026-11-14_opus_lean-formalisation/REPORT.md). This machine check does not certify every new exposition or research lemma. The exact merged, primal and involution texts still need human review. Corollary 7.2 has an unreviewed named-theorem deduction through GSW 4.16, not a new Lean formalisation.

The primal revision disputes referee M4. It simplifies the referee's phase ratio to i^n, a constant; the referee had claimed circuit-count dependence. Record both sources, [the original referee](../../research/2026-11-14_fable_referee-primal/REFEREE.md) and [the revision](../../research/2026-11-14_astra_primal-revision/REPORT.md). The revision's self-audit is not an independent resolution of the dispute. A focused re-referee of that calculation and the inside-cycle connectivity lemma is the next useful review.

## Unsigned proofs: the graveyard

Each entry closes the stated shortcut. It does not prove that every method in its area fails. The generated [route inventory](../route-map/ROUTE-MAP.md) supplies the full provenance and lesson for every dead end.

| Shortcut | Where it died |
|---|---|
| Natural two-matroid intersection | The third state constraint is indispensable. Hexagonal prism common bases include four nonstates among six. `sol_referee-structure/INTEGRATION.md` and determinant referee corrections. |
| Natural LP integrality or automatic rounding | Half-integral vertex at V=13, not proved minimal. No standard rounding theorem preserves both endpoint degree constraints. |
| Lattice extremes C2 | V=18, `sol_referee-conjectures/data/v18.json`, independently minimal. |
| Extreme or irreducible R2 | V=33, `sol_referee-conjectures/data/R2_glued_V33.json`, two implementations. |
| Distance one, every maximal chain, at least half the lattice | Saved R1/R3/R5 witnesses at V=24/60/70 in `data/r1.json`, `r3.json`, `r5.json` of that referee. Gluing gives R3/R5 failure at V=33 and no fixed distance bound in general. Those larger original sizes are not minimum claims. |
| Sign gauge and universal congruences | `sol_route-algebra/REPORT.md`. Pair signs cannot be removed by a state gauge; the unweighted signed total is zero. This excludes those proposed invariants, not every modular argument. |
| Canonical extremal states and rank differences | `fable_route-combinatorics/ROUTES.md`, corrected first failures at V=12 by its referee; graph-theory greedy terminals need not be genuine lattice extremes. |
| A single minimal cover supplies a forest pair | A cover can have no successful direction. V=16 saved bad cover; V=18 lattice extremes provide independently replayed examples. Counting all covers remains essential to the known proof. |
| Fixed-c flip connectivity | V=18 squares, `astra_cycle-covers/data/levels.json`; even minimum levels can disconnect. |
| Direct local lifting | V=18, `fable_induction-completion/data/nolift_18.jsonl`; rotation rescues these examples. Earlier “every matching lifts” fails already at V=8. |
| Strict rainbow descent or surplus walk termination | Strict descent fails at V=8; periodic surplus walks at V=38. Both need plateaus or additional moves. |
| Positive full-spoke mean fitting | Cube forced-degree boundary obstruction, `sol_route-probabilistic/PROOFS.md`. |
| Joint Lorentzian or M-convex support | Cube joint-degree witness; rainbow load vectors fail at V=12. One-sided closure is insufficient. |
| Unit-circle or real-rooted polynomials | V=12 factors `(z-1)(z^2+3)` and `x(x+1)(2x+1)(2x^2+5x+4)`; real z roots fail at V=10. Probabilistic run `code/secondary.py`. |
| Uniform state rejection as an efficient algorithm | Width-four tubes have two successes among Fib_(2L+3) states without separating triangles. `sol_counting-families/FAMILIES.md`. |
| Forest Q without the partner | Hexagonal prism, V=8: three acyclic-Q states, only two tree matchings. Root connectivity cannot be omitted. |
| Mate of a tree matching is a tree matching | Refuted in the topology referee's `data/ref_mate.json`; signed balance is not that involution. New surplus-walk involutions are a different construction, unreviewed. |
| Ordinary lattice rank polynomial | Singleton base lattice already loses the two opposite signs and the graph-dependent weights. `sol_referee-conjectures/LATTICE-READING.md`. |
| Automatic nonplanar state proof | Heawood root-free torus: 24 states, 48 pairs, odd-cycle cancellation survives, polynomial zero. `astra_route-pfaffian/data/results.json`. |
| Universal boundary condition at longer cuts | Length-five cut with nine vertices, categorical `PROOF.md`. Even quadrilateral six-pattern completeness needs the chord qualification. |
| Commuting reversal bicomplex or topological Hall | Reversals fail to commute in 12 of 624 tested pairs; octahedral partial-tree complex disconnected. Categorical `REPORT.md`. |

## What survives

The contraction induction would close with ML1 and ML2. Its local splitting, lifting and rotation statements have an independent AI referee; the new one-sided extension still needs one. C3 and rainbow exchange X survive finite tests with plateaus. Two-tree packing remains a promising fractional statement pending its dedicated report, and exact rounding is still separate. C1 survives all tested sizes, with an unreviewed two-cover proof and sharp infinite families. None of these is a replacement proof of the key existence lemma yet.
