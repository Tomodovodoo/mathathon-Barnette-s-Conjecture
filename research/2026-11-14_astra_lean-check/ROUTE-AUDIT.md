# Bounded proof-route audit

## Audit boundary

COMPUTED/PROVED-HERE. C0 is the unchanged upstream `OAI.Barnette.MainStatement` at commit `4eaee87548250b2682affda7d05d947c05554bae`. It quantifies finite simple graphs with decidable adjacency, degree three, bipartiteness, a crossing-free topological plane embedding, and three-vertex-connectivity, and concludes a Hamiltonian cycle. It does not include the paper's prescribed avoided edge. Accepted primitives are the Lean kernel, propext, Classical.choice, Quot.sound, and compiled upstream/Mathlib results with their actual types. We audit the supplied replacement route; the original phase proof is a control, not an alternative used to rescue it.

## Obligation graph

```text
C0 unchanged main
 <- R0 (AND: U0 embedding-to-dual, U1 pair-existence and gluing/recovery, C1 forest-pair lemma)
C1 existence of a pair with acyclic Q_right
 <- R1 (AND: H0 Nonempty Pair, H1 opposite disk identities, H2 strict cycle-slope signs,
              C2 realSum nonzero, C3 no-good-pair implies realSum zero)
C2 realSum(w,minCycles) nonzero
 <- R2 (AND: D0 genuine pair/class partition, D1 representative minimum attained,
              C4 class sum zero above m, C5 common-sign nonzero class sum at m)
C4 zero class contribution for m<c
 <- R3 (AND: C6 real-sign reversal, D2 weight additivity, C7 finite differences)
C5 common-sign nonzero class contribution for m=c
 <- R4 (AND: C8 sign closed formula, H2 strict slope signs, D2 weight additivity,
              C7 finite differences, A0 factorial/product positivity)
C3 no-good-pair implies realSum zero
 <- R5 (AND: C9 fixed-second-state reversal involution, H1 opposite disk,
              C6 real-sign reversal, A1 finite fiber summation)

P0 literal complete paper route
 <- diagnostic only (AND: C0 algebraic existence route, B1 geometric dictionary,
                     B3 face paths to flow weights, B4 full good-state/root/partner bridge,
                     B5 prescribed-edge drawing theorem, P1 paper's two-tree gluing)
```

There is no OR route used to conceal an open bridge. The diagnostic P0 comparison is separate from C0. Neither phase nor polynomial nonvanishing is an accepted primitive on R1--R5; the environment walk tests this independently.

## Critical findings

The replacement proof needs only the no-good-pair case of cancellation, which it supplies. The missing full sum over good states is not a missing leaf of C0. Likewise D1 minimises over representatives and suffices for C2; identification with the paper's all-pairs minimum is not required by this route. Literal paper coverage remains blocked by the diagnostic bridge nodes. TODO T5 cannot be a target for closing B4 because it is false.

## Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | MainStatement | root | R0 | root | rebuilt main and independent closure | discharged |
| U0 | Drawing admits exact algebraic dual | C0 | R0 | named theorem | upstream exists_exact_dual, same hypotheses | discharged |
| U1 | Pair construction, recovery, gluing | C0 | R0 | named theorem | unchanged upstream tail, generated.diff | discharged |
| C1 | Forest pair exists | C0 | R1 | major claim | forest_pair_of_disk_circulation_real | discharged |
| H0 | Nonempty Pair | C1,C2 | R1,R2 | hypothesis | explicit argument, upstream pair existence | discharged |
| H1 | Every opposite cycle has delta sum ±3 | C1,C3 | R1,R5 | hypothesis | opposite_disk in concrete use | discharged |
| H2 | Every D-cycle has signed nonzero slope | C1,C5 | R1,R4 | hypothesis | paired_sign plus existence of white-charge flow | discharged |
| C2 | realSum nonzero | C1 | R2 | major claim | realSum_ne_zero | discharged |
| C3 | No forest pair implies zero total | C1 | R5 | major claim | sum_sign_eq_zero_of_no_good | discharged |
| D0 | Pair fibers partition pairs and Boolean choices enumerate each fiber | C2 | R2 | named theorem | groupEquiv and sum_groups' | discharged |
| D1 | Finite nonempty representative minimum is attained | C2 | R2 | algebraic/logical step | Finset.min', image membership, Nonempty Pair | discharged |
| C4 | Contributions vanish for m<c | C2 | R3 | major claim | group_sum_lt | discharged |
| C5 | At m=c all class contributions have common nonzero sign | C2 | R4 | major claim | group_sum_card and strict positivity | discharged |
| C6 | Reversals multiply real sign as required | C3,C4 | R3,R5 | proved earlier | LocalSign, disk premises explicit | discharged |
| C7 | Finite difference at degrees below/equal orbit count | C4,C5 | R3,R4 | proved earlier | Blueprint.finite_difference | discharged |
| C8 | epsilon=(-1)^((n+c)/2+c_plus) | C5 | R4 | proved earlier | sign_formula | discharged |
| C9 | Chosen opposite-cycle reversal is fixed-point-free involution | C3 | R5 | named theorem | upstream reversal_ne and reversal_involutive | discharged |
| D2 | Reversing chosen cycles adds -cycleSlope | C4,C5 | R3,R4 | proved earlier | weight_orient for local sums | discharged |
| A0 | Factorial and product of strictly positive absolute slopes nonzero | C5 | R4 | side condition | positive slopes from H2, factorial_ne_zero | discharged |
| A1 | Finite sums split into second-state fibers | C3 | R5 | algebraic/logical step | finite State/Pair and secondFiberEquiv | discharged |
| B1 | Literal sphere, face and orientation dictionary | P0 | diagnostic | missing | not formalised by this package | failing |
| B3 | Face-path heights coincide with a permitted flow weight | P0 | diagnostic | missing | TODO T2 has no proof | failing |
| B4 | Full good-state/unique-partner/root-component correspondence | P0 | diagnostic | missing | T3 plus additional obligations needed | failing |
| B5 | Drawing-level prescribed-edge variant | P0 | diagnostic | missing | existing blueprint gap, unchanged | failing |
| P1 | Two induced trees and gluing through them | P0 | diagnostic | missing | TODO T6, no replacement proof | failing |

## Verdict

C0 FOLLOWS by the supplied replacement route. The fresh build and independent walk in REACHABILITY.md discharge every obligation on R0 through R5, using only the three standard axioms. The literal-paper route P0 is NOT ESTABLISHED BY THIS PROOF: the package does not discharge B1, B3, B4, B5 or P1. This is not a claim that the paper theorem is false. TODO T5 itself is REFUTED by the explicit prism computation.
