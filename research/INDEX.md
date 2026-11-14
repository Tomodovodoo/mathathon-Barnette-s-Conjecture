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
| `fable_digestions/` | Fable 5.2 | `digestions/steps/`, eleven documents | done, under audit | |
| `sol_referee-structure/` | GPT-6.1 Sol | Referee of graph-theory and limits reports | running | |
| `opus_conjectures/` | Opus 5.5 | Lattice-extreme, 2^cmin and descent conjectures | running | |
| `opus_review-draft-A/` | Opus 5.5 | Cold-reader review of draft A | running | |
| `astra_primal-proof/` | GPT-6 Astra | Proof entirely in G, `proofs/primal/` | running | |
| `fable_referee-topology/` | Fable 5.2 | Referee of topology report, rainbow-exchange attack | running | |
| `sol_counting-families/` | GPT-6.1 Sol | Exact counts on infinite families | running | |
| `astra_older-approaches/` | GPT-6 Astra | Earlier methods re-read through the new proof | running | |
| `fable_review-draft-B/` | Fable 5.2 | Cold-reader review of draft B, merge plan | running | |
| `opus_route-induction/` | Opus 5.5 | Inductive routes | running | |
| `astra_audit-digestions/` | GPT-6 Astra | Audit of digestions, route map and labyrinth | running | |