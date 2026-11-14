# Reverse-Lamport audit of the completed involution note

## Audit boundary

PROVED-HERE self-audit, not an independent review. Source boundary is proofs/involutions/involutions.tex, Theorem 1 through Lemma 7, frozen after the explicit incidence/forest dictionary was added. The theorem contract is: for every finite simple sphere triangulation with a proper black/white face colouring and a chosen outer black face, existence of a disjoint state pair implies existence of a pair with acyclic opposite-edge graph. The constructor additionally assumes its finite minimum-cover enumeration has completed.

Accepted primitives are finite-set arithmetic, Euler's sphere and disk formulas, the Jordan curve theorem with transverse entry/exit alternation, and the existence of a straight-line drawing of the plane spoke graph. A finite enumeration terminates because its universe is finite. We do not accept a polynomial nonvanishing theorem, the forest-pair conclusion, or a Hamiltonicity theorem as a primitive. Initial pair existence is a hypothesis. The preliminary Ore application is outside the theorem contract.

## Obligation graph

Only one sufficient proof route is supplied. Cases in the second map form AND obligations, not alternative proof routes.

```text
C0 forest pair exists
 <- R0 signed finite-set comparison
    AND H0, C1, C2, C3, C4, O0
C1 first map is an involution reversing signs off forest fixed set
 <- R1 cycle reversal with second state fixed
    AND O1, O2, O3, C5
C2 second map is an involution reversing signs off its stated fixed set
 <- R2 complete priority-rule case split
    AND O4, O5, O6, O7, O8
C3 second fixed set is nonempty
 <- R3 choose one interior white point per minimum cycle
    AND C5, O9, O10
C4 second fixed set has constant sign
 <- R4 first-exit computation
    AND O11, O12
C5 disk identity and spoke-cycle transfer
 <- R5 state count, side count, Euler, disjoint local slides
    AND O13, O14, O15, O16
C6 constructor returns a forest without repetition
 <- R6 finite alternating path from a second-fixed point
    AND C1, C2, C3, C4, O17, O18
```

## Critical findings

PROVED-HERE. O5 is the key general-m obligation: if all cycles carry marks, c ≥ m and exactly m tokens imply c=m and exactly one token on each cycle. It is this condition that makes a cycle reversal leave every other mark valid and every other direction unchanged. Repeated white faces cause no collision because tokens on different cycles have different spokes.

PROVED-HERE. O6 is the cycle-selection obligation. The chosen unoriented cover, white point on each cycle, exterior status, and nonfirst status all survive the move. Selection cannot use current orientation. The proof explicitly treats both priorities and both partner-matching cases.

PROVED-HERE. O9 requires orienting each cycle separately, not swapping both entire matchings. A minimum cover plus an interior white face on each cycle gives exactly one permitted orientation per first crossing, even when the same white face is chosen on nested cycles.

PROVED-HERE. The constructor's finite path needs no monotone numeric potential. An initial endpoint cannot enter a cycle in a graph with degree at most two, including a parallel two-edge cycle. A terminal second-fixed endpoint would have opposite sign, which is impossible. Minimum-cover search is a real prerequisite and the note does not silently replace it by the more efficient arbitrary-start walk in barnette_trees.

PROVED-HERE. The orientation dictionary was checked rather than assumed. Li's directed incidence cycle is opposite to the note's two-spoke direction; both its cycle statistic and crossing direction must change. The resulting sign agrees because n and m have the same parity.

The coefficient comparison and the 221050-object computation are supplementary evidence, not leaves supporting C0. Numerical agreement does not discharge any mathematical obligation in the graph.

## Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Pair existence implies a forest pair | root | R0 | root | C1-C5, H0, O0 | discharged |
| H0 | At least one pair exists in the finite specified triangulation | C0 | R0 AND | hypothesis | Theorem 1 contract | discharged |
| O0 | Opposite signs pair under an involution; a nonempty constant-sign fixed set has nonzero imbalance | C0 | R0 AND | algebraic/logical step | Finite two-element orbits | discharged |
| C1 | First-map claims | C0,C6 | R1 | major claim | Lemma 4 | discharged |
| O1 | Every opposite-edge cycle is directed and avoids roots | C1 | R1 AND | proved earlier | Distinct tails exhaust cycle vertices, outdegree zero at roots | discharged |
| O2 | Reversal preserves the first bijection and disjointness | C1 | R1 AND | side condition | Cyclic permutation of selected vertices; third corner differs from second | discharged |
| O3 | Second state, all tokens and the chosen cycle remain fixed | C1 | R1 AND | definition | First cycle chosen using s alone | discharged |
| C2 | Second-map claims | C0,C6 | R2 | major claim | Lemma 5 | discharged |
| O4 | Unmarked-cycle reversal preserves token validity, selects the same cycle and changes J by ±2 | C2 | R2 AND | proved earlier | Lemma 5 case 1 and definition of J | discharged |
| O5 | Every marked cycle has exactly one token in the all-marked case | C2 | R2 AND | algebraic/logical step | c≥m, m tokens, surjection to cycles | discharged |
| O6 | Same first qualifying cycle is selected twice | C2 | R2 AND | side condition | Underlying cover, exterior predicate and nonfirst predicate invariant | discharged |
| O7 | Geometric partner exists and returns; reversal makes the new token an s-token without collision | C2 | R2 AND | side condition | Consecutive-crossing pairing, O5, proof of Lemma 5 | discharged |
| O8 | A pairing flips direction; optional reversal flips it back while changing floor(J/2) parity | C2 | R2 AND | named theorem | Jordan entry/exit alternation, plus cycle statistic; other marks unchanged by O5 | discharged |
| C3 | Second fixed set nonempty | C0,C6 | R3 | major claim | Lemma 6 | discharged |
| O9 | Independent orientations make all chosen first crossings s-spokes | C3 | R3 AND | side condition | Matchings exchange on one cycle; choices independent | discharged |
| O10 | Result has m distinct tokens and satisfies exactly the fixed predicate | C3 | R3 AND | definition | Different cycles have different spokes; Lemma 5 fixed description | discharged |
| C4 | Every second-fixed object has sign (-1)^floor(m/2) | C0,C6 | R4 | major claim | Lemma 6 | discharged |
| O11 | First exit is right-to-left precisely on a counterclockwise cycle | C4 | R4 AND | named theorem | Oriented Jordan curve, point inside, endpoint outside | discharged |
| O12 | floor((m-2q)/2)+q=floor(m/2) | C4 | R4 AND | algebraic/logical step | q integer | discharged |
| C5 | Disk identity, white-point existence, cycle orientation dictionary | C1,C3 | R5 | major claim | Lemma 2 and following spoke-slide paragraph | discharged |
| O13 | B=I+ell in the bounded root-free disk | C5 | R5 AND | side condition | State bijection, outgoing boundary cycle, explicit boundary matching argument | discharged |
| O14 | E=3B+h-ell=3W+ell, Euler gives W=B+1 and h-2ell=3 | C5 | R5 AND | algebraic/logical step | Disk side counts and Euler; all disk faces triangular | discharged |
| O15 | Local detours have disjoint interiors and exclude every third corner | C5 | R5 AND | side condition | At most one used side in each black triangle | discharged |
| O16 | Slides preserve simplicity, direction and every white-face point's side | C5 | R5 AND | named theorem | Local planar isotopy through the subdisks in O15 | discharged |
| C6 | Alternating constructor terminates at a forest pair | root, secondary claim | R6 | major claim | Lemma 7 | discharged |
| O17 | Labelled graph is finite of degree at most two; starting endpoint lies on a path | C6 | R6 AND | algebraic/logical step | C1,C2 and finiteness of objects | discharged |
| O18 | A second-fixed terminal endpoint would have opposite sign | C6 | R6 AND | algebraic/logical step | Odd number of sign-reversing edges, contradicting C4 | discharged |

## Verdict

FOLLOWS. Every leaf on R0 and R6 is discharged within the stated boundary. The delicate obligations are O5-O10 and O13-O16; the written proof addresses each. This verdict does not include initial pair existence, a polynomial-time initialization claim, or independent certification of the background topology.
