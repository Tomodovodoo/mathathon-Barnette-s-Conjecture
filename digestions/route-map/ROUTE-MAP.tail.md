## Where the proofs are forced

All four published proofs do the same thing at these places, and the project found no way around any of them.

- **A second matching.** A state alone is not enough. The partner `r` orients `Q_s`, and without it "forest" does not imply "tree matching" (R.x1, hexagonal prism).
- **The disk identity (B).** One double count in every source. It needs the state to be a bijection (B.x1). Its parity part is used three times and its value 3 once (C.5).
- **The sign and the cancellation with `s` fixed (C, K).** Three notations for one sign. The cancellation is the vanishing of an incidence determinant on a cycle (K.1), and the reversed cycle must be chosen from `s` alone (K.x1).
- **Weights that depend on `s` only, with positive circulation on cycles (N).** Gauge weights give `0 = 0` (N.x1). Every working variant still takes the lowest order at which something survives, the minimum number of cycles `cmin`.
- **Tree-cotree duality and the rooted selection (E, E2).** The three papers select the same edge set `P`. The Lean proof reaches `P` without building the white tree.
- **One prescribed edge in the induction (G).** An unbounded prescription is NP-hard (G.x1).

## Where there is freedom

- **A, the first pair.** Four published arguments: flow with a component-wise density bound (O), Ore with a minimal deficient set (L), the exact criterion (T), Hall on a gadget with a global bound (Lean). One identity proved here gives both directions of the criterion (A.GT).
- **N, the nonvanishing.** Five published arguments (Taylor coefficient, second involution, polynomial per component, marked walk, polynomial with a flow on `G`) and two shorter ones proved and AI-refereed here (heights, linear weights). This is where a better exposition gains most.
- **F, one cycle.** Two arguments. O, T and the Lean proof use the disk identity again. Li uses an innermost cycle and needs neither the identity nor the partner.
- **The ending.** O and T pass through two induced trees. Li and the Lean proof glue Hamiltonian cycles or matchings directly.

## What the dead ends have in common

Most of the refuted routes fall into four groups.

1. **Drop a constraint** (U.x1, U.x2, U.x3, U.x5, N.x9, N.x10, R.x1, B.x1). The target has three independent constraints: one spoke per black face, one per non-root vertex, and acyclicity. Any two are easy. The hexagonal prism dual, with 8 vertices, 3 states and 2 tree matchings, refutes most two-constraint shortcuts.
2. **Pick an extreme** (N.x3 to N.x6, N.x14, and each half of D.7 taken alone). Highest state, lowest state, one-way cover, largest rank difference, lattice minimum, lattice maximum, single-swap descent. Each fails, at 12 to 80 vertices, typically on one long `D`-cycle where swapping `r` and `s` removes any preference.
3. **Count without weights** (N.x1, N.x2, N.x12, N.x13, N.x15, U.x7). The unweighted signed count is zero and the number of tree matchings is even. Positivity statements on the `s` side are equivalent to existence and prove nothing.
4. **Weaken a hypothesis** (S0.x1 to S0.x3, G.x1, TG.x1). Each hypothesis has a witness, and each fails at a different waypoint.

Two structural statements survive the data. D.7 says the minimum or the maximum of Felsner's lattice of pairs always carries a tree pair. U.7h says a local search from a point-rainbow tree always reaches a tree matching.

## Limits of this map

- It was compiled from the agents' reports. I recomputed one thing myself: the agreement of the two enumerations up to 16 vertices (`labyrinth/make_frontier.py`). Everything else carries the status its author or referee gave it.
- The map was frozen at 11:15 UTC on 2026-11-14. The reports of referee-structure, primal-proof, route-categorical, conjectures and the manuscript drafts had not arrived or were provisional. Two topology predictions (TG.h2, B.5) are listed as conjectures with the outcome to be read in the topology folder.
- A route listed as `LIT` for the Lean proof rests on the lean-formalisation agent's reading in `DIFFERENCES.md`, which nobody has refereed.
- "Smallest known counterexample" means smallest found, not proved minimal, unless the entry says so.
