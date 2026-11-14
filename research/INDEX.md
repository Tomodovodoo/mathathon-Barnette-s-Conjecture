# Research runs

Status is `running`, `done` (report delivered, not refereed), `refereed` or `stale`. All folders are prefixed `2026-11-14_`.

| Folder | Model | Topic | Status | Result |
| --- | --- | --- | --- | --- |
| `astra_exposition-method/` | GPT-6 Astra | What made the floating-proof rewrite work | done | 22-rule style guide, critique of the three papers, outline. Removing proof obligations mattered more than shortening prose. |
| `fable_dependency-graph/` | Fable 5.2 | Reverse-Lamport graphs of the three papers | done | No error found in any paper. 14-node shared core, four nodes of real difference. Li needs four routine steps written out. |
| `opus_history-literature/` | Opus 5.5 | History, partial results, equivalents | done | Three old ideas (two induced trees, edge avoidance, gluing) and one new one (disk identity with signed cancellation). Lean formalisation exists upstream. |
| `sol_machinery-literature/` | GPT-6.1 Sol | Tools and reformulations | done | 11 reformulations, 18 ranked route ideas, 47 references. |
| `fable_route-combinatorics/` | Fable 5.2 | Combinatorial routes | done, under review | Weight-free proof of Prop. 5.1 via heights; J is cw minus ccw cycles; cancellation is an incidence determinant; no canonical forest pair (counterexamples at 12 to 16 vertices). |
| `opus_route-graph-theory/` | Opus 5.5 | Matroid, orientation and structural routes | done, under review | Not a matroid intersection (three matroids; half-integral LP vertex at V=13). Exact Euler identity for the pair criterion. Pairs form a Felsner lattice. Extremes refuted singly. |
| `sol_route-constructive/` | GPT-6.1 Sol | Reference implementation and algorithms | done, under review | `workings/barnette_lab/`; all lemmas pass on 77 rooted runs; determinant coefficient formula; no polynomial-time algorithm. |
| `astra_figures/` | GPT-6 Astra | Figure toolkit, first pass | done | 14 figures in `paper/figures/`. Layout and marks need work. |
| `astra_route-dimers/` | GPT-6 Astra | Dimer and determinant routes | done, under review | Linear weights replace exponentials; mixed-determinant coefficient formula; counterexamples to raw determinants. |
| `fable_figures-review/` | Fable 5.2 | Figure second pass | done | New 13-vertex running example, circular layout, wedge marks, 15 figures. |
| `opus_route-topology/` | Opus 5.5 | Topological and trinity routes | done, under review | Disk identity from the turning-number theorem; cancellation as Morse matching; rainbow-tree plus exchange conjecture (450/450 up to V=16). |
| `fable_referee-determinants/` | Fable 5.2 | Referee of constructive and dimer claims | done | All claims correct (two wording fixes). The two determinant formulas coincide. Linear weights give a one-polynomial proof of Prop. 5.1. No cancellation-free proof. |
| `astra_limits/` | GPT-6 Astra | What breaks when a hypothesis is dropped | done, under review | Recovery injective, not surjective. Exponentially rare tree matchings on prism-sums. P5 containment fails on the cube. |
| `sol_route-algebra/` | GPT-6.1 Sol | Alon-Tarsi, mod-p counts, graph polynomials | done | Berezin and determinant-product formulas. No sign gauge, no universal congruence, no independent nonvanishing proof. |
| `opus_lean-formalisation/` | Opus 5.5 | The upstream Lean proof as a dependency map | done | Built locally; standard axioms only. Polynomial 1+aX, one flow on G, recovery in G, induction on edge avoidance. |
| `astra_referee-combinatorics/` | GPT-6 Astra | Referee of the weight-free proof | done | FOLLOWS, with corrections. `REWRITTEN-PROP-5-1.md`. |
| `fable_labyrinth-map/` | Fable 5.2 | Labyrinth map, route graph, `digestions/route-map/` | done | 16 waypoints, 17 steps, 175 routes. One chain; freedom at three steps. |
| `astra_manuscript-A/` | GPT-6 Astra | First full manuscript draft in `paper/draft-A/` | done, under review | 11 pages, height proof. |
| `sol_figures-polish/` | GPT-6.1 Sol | Figure third pass | done | Crossing checks, greyscale proofs, cube layout, six-panel introduction strip. |
| `fable_route-categorical/` | Fable 5.2 | Categorical and structural reformulations | done | Cutting along cycles is substantive (3 patterns on triangles, 6 on quadrilaterals, fails at 5). The rest is vocabulary. |
| `opus_manuscript-B/` | Opus 5.5 | Second manuscript draft in `paper/draft-B/` | done, under review | 16 pages, all in the dual triangulation. |
| `fable_digestions/` | Fable 5.2 | `digestions/steps/`, eleven documents | done, audited | 23,000 words; audited and corrected by `astra_audit-digestions/`. |
| `sol_referee-structure/` | GPT-6.1 Sol | Referee of graph-theory and limits reports | done | Euler criterion, sharp gluing, recovery image and rarity confirmed. Degree-4 converse and matroid isomorphism refuted. `INTEGRATION.md`. |
| `opus_conjectures/` | Opus 5.5 | Lattice-extreme, 2^cmin and descent conjectures | done, under review | Lattice-extreme conjecture FALSE (V=18). Irreducible-element variant survives to V=24. 2^cmin holds to V=22. Directed-cycle criterion for tree pairs. |
| `opus_review-draft-A/` | Opus 5.5 | Cold-reader review of draft A | done | Proof follows; four sentences missing; 9 of 22 style rules pass; 25 edits. |
| `astra_primal-proof/` | GPT-6 Astra | Proof entirely in G, `proofs/primal/` | done, refereed | 13 lemmas, no dual. Revised in `astra_primal-revision/`. |
| `fable_referee-topology/` | Fable 5.2 | Referee of topology report, rainbow-exchange attack | done | All eight claims stand. Step R proved. Step X open (true to V=17). Evict walk cycles at V=38. |
| `sol_counting-families/` | GPT-6.1 Sol | Exact counts on infinite families | done | Prism formulas, nanotube recurrences, exponentially rare tree matchings without separators, 2^cmin tight on prism-sums. |
| `astra_older-approaches/` | GPT-6 Astra | Earlier methods re-read through the new proof | done | Feder-Subi parity link refuted. Through-an-edge follows from avoidance. `NOVELTY.md`. |
| `fable_review-draft-B/` | Fable 5.2 | Cold-reader review of draft B, merge plan | done | One unchecked hypothesis (connectivity for Euler), fixed by a five-line lemma. 13 of 22 rules pass. `COMPARISON.md`. |
| `opus_route-induction/` | Opus 5.5 | Inductive routes | done, under review | Contraction induction reduced to statements G and L, both true to V=17; L proved in 98.3% of hard cases. 13 schemes refuted. |
| `astra_audit-digestions/` | GPT-6 Astra | Audit of digestions, route map and labyrinth | done | 27 findings fixed; map rebuilt with 186 routes. |
| `fable_referee-primal/` | Fable 5.2 | Referee of the primal proof | done | FOLLOWS; one gap closed, three fixes; recommends primal backbone with dual pictures. |
| `astra_route-pfaffian/` | GPT-6 Astra | Non-planar Pfaffian corollary and a direct route | done | Corollary 7.2 follows via GSW 4.16. On Heawood cancellation survives, nonvanishing fails. |
| `sol_route-probabilistic/` | GPT-6.1 Sol | Probabilistic and positive-measure routes | done, under review | No unsigned proof. Mean obstruction. Two-tree packing conjecture. |
| `astra_literature-consolidation/` | GPT-6 Astra | `papers/INDEX.md`, `papers/barnette.bib` | done | 87 sources indexed; no theorem-number mismatch. |
| `astra_primal-revision/` | GPT-6 Astra | Primal note with referee fixes and figures | done | 15 pages, 8 figures, dictionary; three observations proved. |
| `sol_route-atlas/` | GPT-6.1 Sol | `digestions/atlas/`, first pass | done | 28 pages, too schematic. |
| `opus_manuscript-merge/` | Opus 5.5 | Merged manuscript in `paper/main/` | done | Version 1, 18 pages, dual language. |
| `fable_referee-topology/` | Fable 5.2 | Referee of topology report, rainbow-exchange attack | done | All eight claims stand. Step R proved. Step X open (true to V=17). Evict walk cycles at V=38. |
| `fable_induction-completion/` | Fable 5.2 | Referee and completion of the contraction induction | done | Shape sound; two lemmas missing. "Some good state lifts" refuted at V=18. |
| `fable_atlas-review/` | Fable 5.2 | Atlas second pass | done | Computed figure on every page. |
| `sol_referee-conjectures/` | GPT-6.1 Sol | Referee of the conjecture report | done | Extremes-or-irreducibles false at V=33. Signed sum is not a lattice rank polynomial. |
| `astra_cycle-covers/` | GPT-6 Astra | What cycle covers and the minimum m are | done, refereed | m unbounded without separating triangles; cycle count as components of G minus S, less one. |
| `opus_two-tree-packing/` | Opus 5.5 | Two-tree packing conjecture | done | True by Nash-Williams, but blind to pairs. Both degree conditions together can fail in one support (V=16). |
| `sol_li-completion/` | GPT-6.1 Sol | Bijective proof in `proofs/involutions/` | done, refereed | Two involutions for general m. |
| `sol_referee-main/` | GPT-6.1 Sol | Mathematical referee of paper version 1 | done | FOLLOWS; eight corrections. |
| `fable_coldread-main/` | Fable 5.2 | Cold reader of paper version 1 | done | Body good, opening weak; 40 edits. |
| `astra_main-revision/` | GPT-6 Astra | Paper version 2 | done | 19 pages; both reviews applied. |
| `sol_referee-main-v2/` | GPT-6.1 Sol | Regression referee of version 2 | done | FOLLOWS; eight small corrections applied. |
| `opus_coldread-main-v2/` | Opus 5.5 | Fresh reader and finishing editor of version 2 | done | 17 edits; main idea given room. |
| `fable_final-polish/` | Fable 5.2 | Last figure fixes; naming in companion notes | running | |
| `astra_induction-lemmas/` | GPT-6 Astra | The two missing lemmas of the induction | done | Both still open. G proved without chordless 5-cycles. |
| `opus_referee-involutions/` | Opus 5.5 | Referee of the bijective note | done | FOLLOWS; object count depends on the drawing, signed sum does not. |
| `sol_involutions-revision/` | GPT-6.1 Sol | Bijective note revised, drawing-free version added | done | |
| `fable_referee-involutions-v2/` | Fable 5.2 | Check of the drawing-free section | done | FOLLOWS on both routes. |
| `opus_cross-audit/` | Opus 5.5 | Primal adjudication, consistency table, hygiene | done | Sign over Lean phase is the constant i^n. Primal note accepted. |
| `opus_consistency-edits/` | Opus 5.5 | Naming convention applied to digestions, map, atlas text | done | good state, good pair, cover, m. |
| `sol_referee-covers/` | GPT-6.1 Sol | Referee of cycle-cover, probabilistic and family reports | done | Main proofs pass, with qualified ranges. |
| `opus_blueprint/` | Opus 5.5 | `proofs/blueprint/` against Lean | done | Of 34 route statements: 4 exact, 25 after translation, 5 without counterpart. |
| `opus_lean-devices/` | Opus 5.5 | `proofs/lean/`: sign and finite-difference route in Lean | done, check pending | 866 lines; main theorem rebuilt without phase or polynomial, by its author's account. |
| `astra_lean-check/` | GPT-6 Astra | Independent rebuild and statement check of `proofs/lean/` | running | |
| `fable_descent/` | Fable 5.2 | Monotone descent and complexity | see its report | |
| `sol_map-update/`, `sol_map-final/` | GPT-6.1 Sol | Route map and labyrinth updates | done | 244 routes, 77 refutations. |
| `astra_synthesis/` | GPT-6 Astra | `digestions/SYNTHESIS.md` | done | |
| `fable_synthesis-audit/` | Fable 5.2 | Fact-check of the synthesis | see its report | |
| `sol_atlas-audit/` | GPT-6.1 Sol | Second-model review of the atlas | done | 78 checks pass; seven figures proposed. |
| `fable_atlas-final/`, `fable_atlas-finish/` | Fable 5.2 | Atlas integration and finishing | finishing | |