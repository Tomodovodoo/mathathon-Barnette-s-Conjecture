# Reachability and complexity audit

## Boundary

Audit the proof-supplied routes to Theorems 5.2, 5.3 and Proposition 6.2 of the supplied October 18 manuscript. Input is a finite rooted Eulerian triangulation with a disjoint pair. Conclusion is a good pair in its exchange component, constructed by the specified marked walk; a separate enumeration has the stated time bound. Accepted primitives are the Jordan curve theorem, Euler counting, integral max flow, Hadamard's inequality and elementary permutation algebra. The disk identity and positive circulation are checked explicitly in ALGORITHM.md. This audit does not certify every historical attribution or search for replacement proofs.

The entire 15-page extraction was read. PDF pages 9-11 were rendered and inspected to check exponents, ordered-token multiplicities, and the determinant formula. The PDF hash is recorded in ALGORITHM.md. The exposition extraction is retained for notation provenance.

## Obligation graph

```
C0 component reachability <- R0 AND(C1 cancellation,C2 nonvanishing,C3 closure)
C1 <- AND(O1 partner classification,O2 Q involution,O3 sign reversal)
C2 <- AND(O4 full orientation orbits,O5 positive gaps,O6 least-order coefficient)
C3 <- AND(O7 exchange reversibility)
C4 marked termination <- R1 AND(C5 phase ends,C6 endpoint classification,C7 restart decreases)
C5 <- AND(O8 finite objects,O9 both involutions,O10 start endpoint)
C6 <- AND(O11 beta fixed iff good,O12 alpha fixed sign/count)
C7 <- AND(O13 odd path parity,O12)
C8 marked bound <- R2 AND(O14 state count,O15 phase count,O16 work/storage)
C9 enumeration bound <- R3 AND(O17 same-sign determinant,O18 Hadamard,O19 prefix charging,O20 safe tests,O21 per-test cost)
C10 global bound <- R4 AND(C9,O22 additive splits,O23 gluing)
```

There are two independent supplied routes to finding a good state, marked extraction and enumeration backed by component existence. They must not be conflated into a polynomial algorithm.

## Critical findings

No failing obligation was found in these routes. In particular, the phase space includes the tokens. An unmarked pair may recur. The sign change at the other alpha endpoint gives a decrease of two or more only at restarts. Equal-rank transport works with repeated tokens because list positions, rather than a set of occupied units, are transported. Parallel alpha and beta edges may be retained as labelled multigraph edges; they cannot occur in the component of a degree-one start in a way that obstructs the path argument.

The determinant signs here are permutation signs of single matchings, not epsilon signs of pairs. Confusing these would incorrectly remove the cancellation. The current manuscript already proves the `3^(n/4)` bound, and the current constructive report quotes it correctly. Earlier descriptions in the task context are therefore less precise than the current files.

## Dependency table

| ID | Exact obligation | Needed by | Route | Classification | Support | Status |
|---|---|---|---|---|---|---|
| C0 | Good pair in each component | root | R0 | major claim | C1-C3 | discharged |
| C1 | Nongood terms cancel | C0 | R0 | major claim | O1-O3 | discharged |
| C2 | Polynomial nonzero | C0 | R0 | major claim | O4-O6 | discharged |
| C3 | All operations stay in component | C0 | R0 | major claim | O7 | discharged |
| O1 | Partnered Q consists of rooted trees and rootless unicycles | C1 | AND | proved earlier | Proposition 2.1 outdegree count | discharged |
| O2 | First Q-cycle reversal fixes s and is involutive | C1 | AND | definition | Cycle order depends only on s | discharged |
| O3 | Both exchanges reverse epsilon | C1 | AND | algebraic/logical step | Disk delta sum and triangle identity | discharged |
| O4 | A cover group contains all orientations | C2 | AND | definition | Independent D reversals | discharged |
| O5 | Integer positive circulation for every D cycle | C2 | AND | proved earlier | Lemma 5.1 dual routing and simple detour | discharged |
| O6 | Minimum-order coefficients have one sign | C2 | AND | algebraic/logical step | Products of strictly positive gaps | discharged |
| O7 | Exchange preserves pairs and reverses itself | C3 | AND | definition | Bijections on cycles | discharged |
| C4 | Marked walk terminates in a good pair | root | R1 | major claim | C5-C7 | discharged |
| C5 | Each phase reaches an endpoint | C4 | R1 | major claim | O8-O10 | discharged |
| C6 | Endpoints are good or suitable alpha-fixed objects | C4 | R1 | major claim | O11-O12 | discharged |
| C7 | Unsuccessful restart decreases c by at least two | C4 | R1 | major claim | O12-O13 | discharged |
| O8 | Finite marked set | C5 | AND | definition | Finite pairs, finite h-tuples of tokens | discharged |
| O9 | Alpha and beta are involutions | C5 | AND | algebraic/logical step | Stable first cycle, reversible rank transport | discharged |
| O10 | Initialization is alpha-fixed | C5 | AND | side condition | One excess-rank token on every CCW cycle | discharged |
| O11 | Beta fixed iff good | C6 | AND | proved earlier | O1 and definition of beta | discharged |
| O12 | Alpha fixed implies c<=h and epsilon=(-1)^((q-c)/2) | C6,C7 | AND | definition | All cycles CCW, each marked | discharged |
| O13 | Path between alpha endpoints has odd length | C7 | AND | algebraic/logical step | Alternating labels, beta at both ends | discharged |
| C8 | Marked time/space bound | root | R2 | major claim | O14-O16 | discharged |
| O14 | At most 6^q(6q^2)^h marked objects | C8 | AND | algebraic/logical step | Six choices per triangle, bounded token pool | discharged |
| O15 | At most ceil(c0/2) phases | C8 | AND | proved earlier | C7 and positive c | discharged |
| O16 | Each move and encoding polynomial | C8 | AND | side condition | Graph scans and bounded integers | discharged |
| C9 | Enumeration O(q^3 M) | root,C10 | R3 | major claim | O17-O21 | discharged |
| O17 | M=abs(det K_B) | C9 | AND | algebraic/logical step | Odd relative permutation cycles by disk identity | discharged |
| O18 | M<=3^(q/2) | C9 | AND | named theorem | Hadamard, row norms at most sqrt(3) | discharged |
| O19 | At most (q+1)M retained prefixes | C9 | AND | algebraic/logical step | Inject prefix into depth and one extension | discharged |
| O20 | Prefix tests preserve every good completion | C9 | AND | side condition | Remaining matching, supergraph of final tree | discharged |
| O21 | O(q^2) test | C9 | AND | algebraic/logical step | At most q augmentations, O(q) edges | discharged |
| C10 | Global polynomial-space poly(n)3^(n/4) | root | R4 | major claim | C9,O22,O23 | discharged |
| O22 | Positive additive split measure q | C10 | AND | algebraic/logical step | Triangle counted in both pieces | discharged |
| O23 | Aligned induced trees glue and preserve prescription | C10 | AND | proved earlier | Section 7.3, connected vertex/edge intersection | discharged |

## Verdict

FOLLOWS for C0, C4, C8, C9 and C10 in the stated boundary. No polynomial running-time claim occurs in these theorem statements. The stronger claim that any unmarked exchange rule terminates is neither stated nor established. The audit is unreviewed and is not a formal verification of the supplied papers.
