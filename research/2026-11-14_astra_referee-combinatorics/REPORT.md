1. `PROVED-HERE`. The weight-free route to Proposition 5.1 passes the reverse-Lamport audit; the final verdict is FOLLOWS.
2. `PROVED-HERE`. The signed-height identity and Hamiltonian-state dichotomy are correct with the stated domain and normalization clarifications.
3. `COMPUTED`. Independent plantri enumeration through 16 vertices passes 140,358 state checks and 636,682 height-monomial checks across 7,868 roots.
4. `REFUTED`. Reflection gives 12-vertex failures of both the lowest-state and all-clockwise choices; the reported first sizes 14 and 13 need correction.
5. `PROVED-HERE`. A self-contained replacement proof and a simpler exact incidence-determinant formula are ready for the exposition; human review remains pending.

## What I set out to do

Independently referee `research/2026-11-14_fable_route-combinatorics/`, reconstruct its proof dependencies, recompute its main claims without reusing its laboratory, check its counterexamples and write a short rigorous proof of Proposition 5.1.

## What I established

`REFEREE.md` gives the audit boundary, conclusion-first AND graph, 13 claim nodes and 35 exact obligations, claim verdicts, corrections and final verdict. The primary route closes. The citation to OpenAI's local sliding argument is valid, and the replacement proof incorporates that argument explicitly. Section 6's interior Euler count also closes, including the nonempty interior and absence of roots.

`PROVED-HERE`. With the submission's canonical colour orientation of the opposite edges, the real signed partner sum has the exact formula `mu(s) = (-1)^n sigma det(d_s)`. The global factor is independent of s because s is bijective. This sharpens the submission's state-dependent-factor description. The detailed twisted-matrix proposition was already correct.

`PROVED-HERE`. The height interpretation needs fixed paths or a reference-state normalization. The volume equality is up to an additive constant and concerns unit circulation on every bounded spoke face. I supplied the potential-difference proof and the connectedness argument for the spoke graph after deleting the outer centre. Theorem B needs an explicit assumption that a pair exists. The short proof of OpenAI Lemma 6.2 establishes P0 as stated; one extra root-component sentence gives the published conclusion for P.

`COMPUTED`. The independent generator and verifier agree with the author's full multiset of orientation-independent rooted profiles through 16 vertices, not just their totals. All 24,744 pairs and 24,090 tree matchings agree. The tests cover 636,682 height monomials, including repeated faces, and 378,632 Hamiltonian-cycle/root incidences. The 176,726 nonimage Hamiltonian states reported by the author agree after restricting to roots with pairs. Extra through-12 checks cover every available directed state cycle and compare volumes with the third model's reference implementation. Commands, limitations and exact counts are in `code/README.md`.

`COMPUTED`, `REFUTED`. The four explicit counterexample face lists reproduce their intended failures. However, reflecting the 12-vertex example reverses rank and orientation, giving the lowest-state and clockwise-minimum-cover failures at size 12. An enumeration identifying reflections cannot support orientation-sensitive first-failure sizes without testing both orientations.

`REWRITTEN-PROP-5-1.md` gives the recommended self-contained existence proof. It uses the disk count, fixed-second-state cancellation, signed intersections at selected white faces and a multilinear expansion. It requires neither a vertex colouring nor the determinant discussion.

## What failed and why

The author's broad negative conclusions exceed their witnesses. A bad specified cover refutes guaranteed success by reversals of that cover, not every proof selecting one cover. A mixed-sign quotient refutes a uniformly signed rank-compatible cube decomposition, not an abstract partition into cubes. Finite examples with c_min up to four do not prove unboundedness. These errors concern interpretations of counterexamples, not dependencies of Proposition 5.1.

`COMPUTED`, `REFUTED`. I supplied a separate cardinality refutation of the abstract cube-partition claim: a 13-vertex instance has six tree matchings and c_min=2. Six cannot split into four-element sets. The full new witness is in `code/cube_cardinality.json`; it repairs the conclusion using different evidence, rather than validating the submitted inference.

An initial extended computation repeated disk flood fills unnecessarily. I stopped it before ten minutes, cached the disk regions, and used an exact fraction-free determinant. The final complete run finished in 190.7 seconds. No unfinished run is represented as a completed certificate.

## What is still open

- `CONJECTURE`. The bound `#TM >= 2^c_min` remains unproved. The independent exhaustive run supplies further evidence but no theorem. A rooted triangulation with a pair and fewer tree matchings would refute it.
- The generator agreement through 16 does not prove the completeness of the author's two local generating moves at all orders.
- Human checking of the replacement proof and the Section 6 argument remains appropriate before publication.

The bound `3 #TM <= #HC` is proved in the submission and passes this review. It should not be listed as a conjecture. The linear lower bound `#TM >= 2 c_min` also passes.

## Three best next steps

1. Apply the exact domain, normalization, reflection and scope corrections in `REFEREE.md`, then use the replacement Proposition 5.1 proof as the exposition's core.
2. Add a figure for the spoke detour and signed path intersection, including the case where a third corner lies elsewhere on the cycle. Keep the orientation convention visible.
3. Investigate the exponential tree-matching lower bound separately. Any proposed cube decomposition must specify how ranks and signs behave; an abstract cube partition alone does not explain the moment identity.

## Leads for others

The determinant specialist can use the stronger global-factor identity. The computational coordinator can compare `code/comparison.json` against the author's data and must distinguish oriented from reflection-identified enumeration. The writer can retain the new disk-balance form and the Hamiltonian-state dichotomy, with the eight-step Euler explanation in the referee report available when needed.

All files changed by this referee are in the assigned folder. The author's files and shared manuscript were left unchanged. Results remain AI-refereed T2 proofs and independently checked finite computations, with human review pending.
