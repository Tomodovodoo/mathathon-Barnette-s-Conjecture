# Referee work log

- Read the protocol, the named audit skills, and all eleven pages of the OpenAI paper through its supplied text. Read the relevant arguments in Li and the constructive paper.
- COMPUTED. Independent plantri generation and an independently written verifier pass all roots through 12 vertices. The run includes 1706 states, 624 pairs, and 4360 height monomials. Output: code/up_to_12.json.
- COMPUTED. The four explicit counterexample maps pass independent reconstruction. Output: code/examples.json.
- Under review. The proof route appears sound; exact normalization and the scope of negative conclusions need corrections. Final dependency audit is pending.

## Completed review

- PROVED-HERE. The primary audit verdict is FOLLOWS. The self-contained rewrite includes the local sliding argument. The Hamiltonian-state dichotomy also closes.
- COMPUTED. The final independent 16-vertex run completes in 190.7 seconds, with 7868 roots, 140358 states and 636682 height monomials. Orientation-independent rooted profiles agree exactly with the submitted data.
- REFUTED. Reflections of the printed 12-vertex witness invalidate the reported orientation-sensitive first failures at 13 and 14. Full reflected witnesses are saved.
- PROVED-HERE. The determinant's phase simplifies to a single global sign for the real signed measure. Height normalization and the unit-face volume identification are justified explicitly.
- REFUTED. A new 13-vertex witness has six tree matchings with c_min=2, ruling out abstract cube partitions by cardinality.
- All deliverables are complete. No continuing computation, subagent, or external service is running for this referee task.
