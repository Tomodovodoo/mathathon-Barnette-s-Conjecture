# Machine-checking the paper's route: what remains

Summary (version 2, 14 November 2026).
1. Done and independently rebuilt: the sign of Lemma 4.4, the finite difference of Lemma 4.7, the real-sign cancellation in the case the existence proof uses, and Proposition 4.8 by `ε · ω^m` with the Lean's flow weights. With them OpenAI's unchanged `main` rebuilds without the six phase and polynomial lemmas (`proofs/lean/`, `research/2026-11-14_astra_lean-check`).
2. Section 4 is not yet machine-checked as written. Four things are missing: the heights along face paths (B3), Lemma 4.5 in full with partner uniqueness and the good-state bridge (B4), the class-size invariance behind `m` (T1), and Lemma 4.2 obtained through Lemma 3.7 (T3, T4). Estimate: 530 to 1,010 new Lean lines, the upper end including the per-face jump of Lemma 4.6.
3. Outside Section 4, two route statements have no counterpart at all: the topological Lemma 2.2 and the two induced trees of Prop. 2.6(2). I recommend not formalising either literally. Lemma 2.2 needs a Jordan curve theorem that Mathlib `d13f23b7` lacks. Prop. 2.6(2) leaves the route if the paper glues perfect matchings as the Lean does.
4. The first estimates were low. Steps 2 and 4 of the version 1 plan came to 714 lines against 360 to 500. The estimates below are already scaled up by about 1.5 for that. They are HUNCH, by analogy with the existing files.

Line references are to `proofs/lean/TODO-statements.lean.txt` (T1 to T12) and to the bridges B1 to B5 of `BLUEPRINT.md`.

## The model stays algebraic

The target remains a Lean proof of `OAI.Barnette.MainStatement` whose intermediate declarations state the paper's lemmas in the Lean's objects (`Network`, `Duality`, `ColoredDual`, `TriangleSystem`). A face of `T` is a vertex of `G`, and the inside of a cycle is the root-free shore of a bond. `exists_exact_dual` already turns a drawing into an algebraic dual. Bridge B1 (drawing to dual) therefore stays informal, and so does the word "counterclockwise" (`δ`-sum `-3`). Closing B1 literally would mean formalising plane topology, which is a separate project of thousands of lines.

## Section 4 as written

**A. Heights along face paths (B3, T2; Lemma 4.6 and the heights paragraph).** 250 to 400 lines.
- Paths of faces: for each white vertex `y` of `G`, a path in `G` to the root vertex (`G.Connected` from `Duality`). Choosing one is a `Classical.choose` on `SimpleGraph.Reachable`, with `Walk.IsPath`. About 30 lines.
- Turn signs `κ_y(t, v)`: at a black vertex `t` the path enters and leaves across two of its three edges, and they meet at one corner `v`. Its side (left or right) needs the cyclic order of the three edges at `t`. The Lean has it in `ColoredDual.oriented` and `Triangle.index_delta`. This is the delicate part, 80 to 120 lines.
- The bridge proper: there are `α` with boundary `whiteCharge` and `k : A → ℝ` with `weights α = Σ_y κ_y + k`. Take `α` = sum of the signed path indicators. Each path contributes `±1` across the edges it uses, and the potentials match the turn signs up to the entry side of each face. 100 to 150 lines. Then `realSum_ne_zero_concrete` applies to the paper's `ω`, because a per-face constant does not change any slope. The step is positive when a **clockwise** cycle is reversed.
- The per-white-face jump of Lemma 4.6 (0 or 1 for each `y`): a path crosses a bond an odd number of times exactly when it ends on the other side (`circuit_cut`), with the crossing sign from the turn signs. 60 to 120 lines. The route does not need it, but the lemma states it.

**B. Lemma 4.5 in full, with the good-state bridge (T3, T7, T8, T10).** 200 to 350 lines.
- T3: restrict `oppositeGraph s` to one connected component as a `SimpleGraph` on a subtype, carry the partner's orientation over, apply `component_count`. 60 to 100 lines.
- T7: given a partner, acyclic `Q_s` implies one root per component. 40 to 70 lines on top of T3.
- T8: a good state has exactly one partner. Each tree with one root has a unique orientation towards it, and the partner is read off that orientation. 50 to 100 lines.
- T10: regroup the signed sum over second states. Pairs with cyclic `Q_s` cancel (`paperSign_partners_sum`), and each good state contributes one term. 40 to 60 lines with T7 and T8.
- `IsGood` must be "one root per component", not "acyclic `Q_s`". The checker's hexagonal prism has an acyclic `Q_s` that is not good.

**C. `m` as the minimum over all pairs (T1).** 40 to 70 lines: equal orbit counts across a class (`bits_invariant`), then the minimum transfers through `GroupIndex.representative`. It changes no conclusion.

**D. Lemma 3.7's first sentence (T4).** 40 to 70 lines: on a cycle with every edge covered and outdegree at most one, counting edges forces one outgoing cycle edge per vertex, and propagation gives one of the two directions.

Total for Section 4: about 530 to 890 lines, plus 60 to 120 for the per-face jump. Steps A and B are independent and can go in parallel. A needs nothing new from upstream. B needs only `component_count` and upstream's `partner_orientation`.

## Outside Section 4

**E. The topological lemma (Lemma 2.2), and the inside of a cycle as a plane graph.** Not recommended. Mathlib `d13f23b7` has no Jordan curve theorem (version 1 grep; the checker did not repeat it). The algebraic stand-ins are already proved: `Duality` connectivity, `region_connected`, `Bond.connected_shore`, `region_euler`. A Jordan curve theorem for polygonal curves alone would be a multi-thousand-line project. The honest record is "Lemma 2.2 has no formal counterpart; the formal proof does not need it".

**F. The two induced trees (Prop. 2.6(2)) and the paper's gluing (T12).** Two options.
- Formalise it: in `D` restricted to an acyclic selection there are two components, and an edge is selected exactly when its ends lie in one of them. Cycles of `D` are bonds (`circuit_cut`), and a cycle meets a cut evenly. Then rewrite the gluing in `matching_strong` to glue acyclic selections. 200 to 350 lines.
- **Recommended**: change the paper's Theorem 6.2 to glue perfect matchings with connected complement, as upstream's `cap_glue_connected` does (48 lines, already checked). Prop. 2.6(2) and Lemma 3.1 then leave the route, and the route count becomes 5 / 17 / 10 / 1 on 33 statements. This is a paper decision, not Lean work.

**G. The explicit selection `P_s` (Lemma 3.6, T9).** 100 to 180 lines: root `Y_s`, let each white vertex select its parent edge, and identify the result with the Hall matching by `perfectMatching_unique` (done). Also needed for T5.

**H. Which cycles arise (T5, corrected).** 150 to 250 lines after B and G. Define the state recovered from an eligible matching. Prove that it is a left inverse on good states, and that a matching lies in the image exactly when its recovered state is good. Do not try to prove surjectivity: it is false (hexagonal prism, `research/2026-11-14_astra_lean-check/COUNTEREXAMPLE.md`).

**I. The prescribed edge for drawings (B5, T11).** 10 to 40 lines: combine `Duality.connected_complement_matching` with `PlaneEmbedding.exists_exact_dual`. Small, and it would make the formal statement match Theorem 1.1.

## Totals

| item | paper | lines (HUNCH) | needed for the paper's route as written? |
| --- | --- | --- | --- |
| A | heights, Lemma 4.6 | 250 to 400 (+60 to 120 for the per-face jump) | yes |
| B | Lemma 4.5 in full, Lemma 4.2 | 200 to 350 | yes |
| C | `m` over all pairs | 40 to 70 | yes, for the definition of `m` |
| D | Lemma 3.7, first sentence | 40 to 70 | yes |
| E | Lemma 2.2 | thousands | no, if the algebraic model is accepted |
| F | Prop. 2.6(2) and its gluing | 200 to 350, or 0 if the paper glues matchings | only if the paper keeps its gluing |
| G | explicit `P_s` | 100 to 180 | yes for Lemma 3.6 as stated |
| H | which cycles arise | 150 to 250 | no (Section 7) |
| I | prescribed edge | 10 to 40 | yes for Theorem 1.1 as stated |

Section 4 as written (A to D): 530 to 1,010 lines. The whole route in the algebraic model with the paper gluing matchings (A to D, G, I): 640 to 1,230 lines. Adding F instead of changing the paper: 840 to 1,580.

## How to continue

1. Reproduce the build from `proofs/lean/README.md` ("How to build"). `E:\lbb` exists on the machine where it was made; elsewhere make a short path and run `lake exe cache get`.
2. Put new files after `Devices/Concrete.lean` (`Devices/Heights.lean` for A, `Devices/Good.lean` for B). Prove each item for the abstract `TriangleSystem` first, then for `ColoredDual`, as the existing files do.
3. After A: change `forest_pair_real` to use the paper's heights, rebuild `PaperRoute`, and rerun `Devices/Axioms.lean` and the dependency check. Ask for an independent rebuild again, as was done in `astra_lean-check`.
4. Keep the paper's numbering in docstrings, so that `blueprint.json` can point at exact declarations.
