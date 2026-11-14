# 09. What is still open

`LIT`. The supplied preprints prove existence of a Hamiltonian cycle. The questions here concern a simpler proof, an efficient construction, or the number of good states. None has a recorded human check. `PROVED-HERE` means a written project proof; `COMPUTED` means a finite check with the range stated; `CONJECTURE` means a claim still to test; `REFUTED` retains a failed claim and its lesson. An independent AI referee changes review status, not a conjecture into a theorem. The route map calls written proofs T2, independently validated exhaustive computations T3, author-only computations T4, conjectures T5 and hunches T6.

Use the [glossary](GLOSSARY.md) for states, pairs, covers and the rainbow constructions. Sizes below are dual order $V=|V(T)|$, unless explicitly called primal order $N=2V-4$. A feasible root admits a pair. A cover is the unoriented $D(r,s)$; $m$ is its minimum possible number of cycles. By contrast, $q(s)$ counts cycles of $Q_s$. A good state has one root in each component of its forest $Q_s$, equivalently $S_s=Q_s\cup\{ao,bo\}$ is a spanning tree. Census files call its count `TM`. Without a partner, an acyclic $Q_s$ alone does not suffice.

## Ten doors

### 1. Rainbow exchange

`CONJECTURE`, rainbow Step X. A point-rainbow tree is a spanning tree of the white-face graph selecting one dual spoke edge for each non-root vertex. The load of a bounded black face counts selected spokes incident to its centre. Black-face excess is twice the number of faces with load two. Step X asks for a path to a good state that never increases this excess, allowing equal-excess moves. [The exact moves](../../research/2026-11-14_fable_referee-topology/RAINBOW.md) include both kinds of plateau exchange.

`PROVED-HERE`. Step R gives such a starting tree exactly when no separating triangle has black inner boundary. Unique-factor completion, Theorem S, completes each rainbow tree to one incidence 2-factor. Proposition U handles the case of a unique cover. Resident eviction pairs good states without fixed points and proves evenness without signs. The [new rainbow referee](../../research/2026-11-14_opus_referee-rainbow/REFEREE-rainbow.md) accepts these proofs with stated notation and hypothesis corrections. Its [summary report](../../research/2026-11-14_opus_referee-rainbow/REPORT.md) confirms those verdicts. The packing part uses independent code from a fresh instance of the author's model.

`REFUTED`, strict black-excess descent means that every positive-excess rainbow tree has an immediately decreasing exchange. It fails at $V=8$, independently replayed by that referee. It is different from strict $q$-descent in door 5. The author's Step X tests reach all roots through $V=17$ and only part of $V=18$; the referee independently reaches $V=12$ and completes seven more $V=18$ graphs, leaving 51 incomplete. Their 224 roots include 7,999,488 enumerated rainbow trees in the multiple-cover cases, re-summed in [our arithmetic check](../../research/2026-11-14_sol_digest-fixes/numbers.json). These are `COMPUTED` ranges, not a proof. Next test: finish the missing roots and search entire equal-excess components.

### 2. Degree-four induction G, also ML1

`CONJECTURE`. Every rooted triangulation without separating triangles and with $V>6$ has a non-root degree-four vertex whose opposite-neighbour merge is simple and still admits a pair. The [induction report](../../research/2026-11-14_astra_induction-lemmas/REPORT.md) defines these two possible contractions. Its census supports G through $V=19$, author-only `COMPUTED`.

`PROVED-HERE`, independently AI-refereed. [G.md](../../research/2026-11-14_astra_induction-lemmas/G.md), now checked in the [induction review](../../research/2026-11-14_astra_referee-descent/REFEREE-induction.md), proves G when there are no chordless five-cycles. Coloured disk curvature supplies a degree-four vertex, but may supply no good merge. The saved inward-selection failures prevent simply choosing the innermost obstruction. Next step: an uncrossing rule that survives those certificates.

### 3. Induction X, also ML2

`CONJECTURE`. If both opposite contractions have good states, some contracted good state lifts or rotates to a good state upstairs. This X is unrelated to rainbow Step X. An exceptional state is one for which both prescribed repairs fail, as defined in [the residual cases](../../research/2026-11-14_fable_induction-completion/RESIDUAL-CASES.md).

`PROVED-HERE`. State splitting, the exact lift criterion and the original rotation have an independent AI referee; the completed descent review also supports the qualified one-sided and exception-bijection arguments. The [descent referee](../../research/2026-11-14_astra_referee-descent/REPORT.md) independently reproduces all 7,940 exceptions, the rotation bijection and counting inequality through $V=18$, `COMPUTED`. [The contraction witnesses](../../research/2026-11-14_fable_induction-completion/data/nolift_18.jsonl) refute direct lifting without rotation. [X.md](../../research/2026-11-14_astra_induction-lemmas/X.md) shows that even changing directions within one cover can fail. Next step: a repair that changes the cover.

### 4. Exponential counting, C1

`CONJECTURE`. Every feasible root has at least $2^m$ good states, with equality exactly when there is one cover. The known general bound is $2m$. One-cover equality and the weak exponential bound for two covers are `PROVED-HERE`, independently AI-refereed. The two-cover equality case is still unresolved; see [the qualified statements](../../research/2026-11-14_sol_referee-covers/INTEGRATION.md).

`COMPUTED`. An [independent all-root replay](../../research/2026-11-14_sol_referee-conjectures/data/fast_census_summary.json) reaches $V=22$. A [separate separator-free census](../../research/2026-11-14_astra_cycle-covers/CENSUS.md) reaches $V=24$; its larger-range invariant calculations remain author-only. Neither establishes a general inequality. Next step: exclude the remaining two-cover equality pattern before tackling several covers.

### 5. Monotone pair descent, C3

`CONJECTURE`. From every ordered pair, D-swaps and Q-reversals can reach a good pair without increasing $q(s)$. A D-swap exchanges the two states on a component of $D$; a Q-reversal changes the partner around a cycle of $Q_s$. A plateau is a connected set of equal-$q$ pairs. A sublevel graph retains pairs with $q$ at most a fixed threshold. C3 is equivalent to every component of every sublevel graph containing a good pair. The [equivalence proof](../../research/2026-11-14_fable_descent/PROOFS.md) is `PROVED-HERE`, accepted by the completed independent AI referee.

`COMPUTED`, author campaign. The [descent report](../../research/2026-11-14_fable_descent/REPORT.md) checks all 193,623,384 pairs through $V=23$, all pairs of its random samples through $V=80$, and sampled starts through $V=200$. Three capped starts at $V=300$ remain undecided. The [completed independent review](../../research/2026-11-14_astra_referee-descent/REPORT.md) confirms C3 through $V=19$ and on all 335,704 pairs of a 40-graph $V=40$ batch. It supplies a complete radius-four witness at graph 3, root {10,16,11}, in [recovered40_0_40.json](../../research/2026-11-14_astra_referee-descent/code/recovered40_0_40.json); the originally selected $V=40$ line had radius three. Our [arithmetic check](../../research/2026-11-14_sol_digest-fixes/numbers.json) sums the census outputs; it does not repeat the large search.

`REFUTED`, strict $q$-descent means every non-good pair has an immediately $q$-decreasing move. It first fails at $V=16$. Bounded-lookahead $q$-descent asks for a lower-$q$ pair within a fixed number of exchanges. Radius two first fails at $V=21$; radius three fails at $V=40$, without a minimum-order claim. The saved $V=60$ pair also has escape radius four, which refutes lookahead three, not four. Lookahead four and unbounded escape radius remain open. All 27 named alternatives to $q$ now have independently checked counterexamples. This is not a theorem ruling out every bounded variant or every height potential.

`PROVED-HERE`, independently AI-refereed. The three-height identity assigns heights to $r,s$ and their unused-corner map with constant total; a move transfers enclosed white area between two heights. It proves strict change, not progress toward a good state. Next step: prove that no positive-$q$ component is closed, beginning with $q=1$.

### 6. Face-rainbow packing, P2

`CONJECTURE`. Every pair support, the union of its two sets of dual spokes, splits into two white spanning trees using one edge from each bounded black face. This is face-rainbow packing; point-rainbow packing instead prescribes one edge per non-root vertex. [The packing proofs](../../research/2026-11-14_opus_two-tree-packing/PROOFS.md) separate the two constraints. The [new packing referee](../../research/2026-11-14_opus_referee-rainbow/REFEREE-packing.md) checks the ordinary packing and one-sided statements; its [summary report](../../research/2026-11-14_opus_referee-rainbow/REPORT.md) accepts the named theorems while leaving P2 open.

`REFUTED`. Requiring both constraints in the same fixed support fails at $V=16$. Ordinary two-tree packing is `PROVED-HERE` and does not detect whether the deleted corners form states. P2 alone therefore leaves the joint requirement open. Next test: larger supports with several covers, not just singleton-cover cases.

### 7. Efficient construction

Open problem. Find a good pair in polynomial time. `LIT`, the [constructive preprint](../../papers/barnette_trees.pdf), gives exponential time with polynomial space. The [new complexity argument](../../research/2026-11-14_fable_descent/COMPLEXITY.md) conditionally places TREE-PAIR, the search for a good pair, in PPADS, a class of directed sink-search problems. It assumes the preprint's marked-walk theorem and is `PROVED-HERE`, supported by the completed independent review. Extra sources obstruct the proposed PPAD route. Extension to full Hamiltonian search needs polynomial-time decomposition, flow and reconstruction plus the PPADS closure citation. The referee checked that citation in an author/publisher abstract but could not access its full theorem statement. C3 and rainbow Step X give no polynomial bound on plateau exploration. Next step: prove such a bound or pair the extra sources.

### 8. Growing minimum cover count with bounded faces

`CONJECTURE`. Can $m$ grow without bound without separating triangles when every primal face is a square or hexagon? The [refereed forcing family](../../research/2026-11-14_sol_referee-covers/REFEREE-families.md) has unbounded $m$, but unbounded pole degree. Width-four tubes have bounded primal face sizes and exponentially rare good states, but $m=1$ at their specified root. These are `PROVED-HERE` with independent AI checks in the stated scopes. The [additional families review](../../research/2026-11-14_fable_referee-families/INTEGRATION.md) distinguishes all-length author transfer proofs from its finite checks and corrects gluing-dependent Hamiltonian counts. Its [summary report](../../research/2026-11-14_fable_referee-families/REPORT.md) checks finite sequences and matrix arithmetic but does not check the author's all-length transfer code. It also narrows the sign-gauge obstruction to signs on one state's incidences; allowing signs on both states remains open. Next step: a fixed-width transfer family with growing $m$.

### 9. Canonical choices and the recovery image

Two different lattices must be kept separate. Propp's state clock lattice orders individual states by clock moves. `REFUTED`: its extreme need not even have a partner, with a witness at $V=10$ in [O1](../../research/2026-11-14_opus_route-graph-theory/ROUTES.md). Felsner's pair lattice orders pair configurations after forgetting component directions. `REFUTED`: neither its minimum nor maximum need carry a good pair, with an independently replayed witness at $V=18$ in [the lattice reading](../../research/2026-11-14_sol_referee-conjectures/LATTICE-READING.md). No minimum-order assertion is needed here. Adding join- and meet-irreducibles, elements with a unique lower or upper neighbour, fails on a gluing with separators. The separator-free restriction remains a separate question.

`LIT`/`REFUTED`. Good-state recovery is injective but does not produce every Hamiltonian cycle avoiding the prescribed edge. The hexagonal prism has four eligible cycles and only two produced cycles, freshly [recomputed](../../research/2026-11-14_sol_digest-fixes/worked-examples.txt). The paper's Section 7 gives an exact criterion using the recovered state's partner. Next step: express that image through $G$ alone, without pretending every eligible cycle occurs.

### 10. Formal statement bridges and human review

`COMPUTED`. The [independent Lean review](../../research/2026-11-14_astra_lean-check/REPORT.md) rebuilds the upstream theorem, the submitted devices and the replacement real-sign route. The checked declarations use only `propext`, `Classical.choice` and `Quot.sound`. Four qualifications matter. The proposed TODO T5 is false because it asks for surjectivity. The full general statement of paper Lemma 4.5 is not formalised. Generic Mathlib polynomial dependencies remain, although the old phase and nonvanishing route is removed. Heights are represented by an abstract flow, so the paper's face-path-to-flow translation remains to prove.

The [main-v2 referee](../../research/2026-11-14_sol_referee-main-v2/REPORT.md), [cold reader](../../research/2026-11-14_opus_coldread-main-v2/REPORT.md), [primal cross-audit](../../research/2026-11-14_opus_cross-audit/ADJUDICATION.md) and [involution referee](../../research/2026-11-14_fable_referee-involutions-v2/REPORT.md) accept their named written routes. These are AI verdicts. Next steps: correct the TODO, formalise the remaining dictionaries and obtain human review.

## Failed induction rules, in readable form

Each row is `REFUTED`. All witness identifiers below come from the linked [induction data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). Graph indices and facial roots follow that file's plantri ordering. $T/M$ means one opposite-neighbour contraction at the named degree-four vertex; a lift splits it back. $g(T)$ counts good states. The [completion referee](../../research/2026-11-14_fable_induction-completion/REFEREE.md) replays the specified witnesses except R8, and checks R13 only on the octahedron. The table records witness sizes, not new minimum-order proofs.

| Rule | Rejected statement and named witness |
| --- | --- |
| R1 | A good lifted state must come from a good contracted state. Witness: V=11, graph 1, root 0, vertex 5, merge 6 into 4. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R2 | Every simple degree-four contraction preserves a pair. Witness: V=11, graph 1, root 0, vertex 5, merge 6 into 4. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R3 | Every contracted good state lifts to a good state. Witness: V=8, graph 0, root 0, vertex 4, merge 5 into 0. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R4 | Failed lifts can be compensated by good states of the same contraction type. Witness: V=8, graph 0, root 0, vertex 4, merge 5 into 0. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R5 | Some contracted good state uses the prescribed local opposite edge. Witness: V=10, graph 1, root 3, vertex 9, merge 2 into 8. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R6 | The original rotation repairs every failed lift. Witness: V=13, graph 7, root {0,4,5}, vertex 10, merge 8 into 4. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R7 | $g(T)\geq2g(T/M)$. Witness: V=8, graph 0, root 0, vertex 4, merge 5 into 0. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R8 | The lowest nonzero cover-area coefficient is monotone under contraction. Witness: V=14, graph 12, root 3, vertex 2, merge 3 into 1; coefficients 5 and 7, author-only. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R9 | $m(T)=m(T/M)$ whenever both admit pairs. Witness: V=14, graph 7, root 1, vertex 12, merge 10 into 6; minima 1 and 3. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R10 | $g(T)=g(T/M)+g(T/N)$ for the two contractions. Witness: V=6, graph 0, root 0, vertex 3. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R11 | Every allowed non-root corner can be prescribed in a good state. Witness: V=8, graph 0, root 0, face {3,6,5}, corner 3. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R12 | Some pair-preserving contraction always exists, even with separators. Witness: V=9, graph 0, root 1. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |
| R13 | Every inverse Batagelj P-operation preserves a pair. Witness: V=6, octahedron; all such reductions are non-simple and lose the pair. [Data](../../research/2026-11-14_opus_route-induction/data/failed_inductions.json). |

## Where the other failures live

The [generated route catalogue](../route-map/ROUTE-MAP.md) retains the full graveyard, sources, witnesses and review states. Matroid and linear-programming relaxations lose joint constraints; a fixed cover may have no good direction; a deterministic eviction walk may loop. Those counterexamples refute their exact shortcuts. They do not prove that every unsigned proof is impossible.

`COMPUTED`. Our fresh full-tier replay also passes; its [output](../../research/2026-11-14_sol_digest-fixes/lab-replay/full.json) retains the counted evidence. The [new lab campaign](../../research/2026-11-14_sol_lab-tests/REPORT.md) passes both counted tiers. Its full census covers all facial roots through $V=14$ plus larger saved witnesses, with independent state/pair/sign comparisons through $V=12$. It finds no production-code bug. Absolute heights can shift by state-independent constants when paths change; raw marked-object counts depend on the drawing. Relative heights, relevant moments and common-geometry map comparisons pass. These finite checks support the implementation, not arbitrary-size claims.
