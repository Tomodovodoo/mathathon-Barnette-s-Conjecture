# Reverse-Lamport audit of the remaining induction

## Boundary

Conclusion C0 is: every rooted simple Eulerian sphere triangulation with a pair has a tree matching, proved by the proposed cancellation-free induction on its vertex count. This audit covers the route in Fable MISSING-LEMMA.md and the attempted additions in this folder. It does not audit or dispute the supplied OpenAI proof by cancellation.

Accepted primitives are Euler and signed side counting, integral Hall flow, the independently refereed pair criterion and gluing lemma, the state-splitting and lift/rotation lemmas, and elementary tree and Jordan-curve facts. OpenAI Proposition 5.1 is deliberately excluded, since it is C0 itself. Computations are evidence and finite counterexample certificates, not arbitrary-size induction premises.

## Obligation graph

```text
C0 <- R0 strong induction
      AND: B, S, I
S  <- R1 cutting a separating triangle
      AND: PC, GL, SMALL, IH
I  <- R2 contracting with no separating triangle
      AND: D4, SIMPLE, G, IH, LIFT
G  <- R3 proposed minimal bad-region descent
      AND: SHORT, CURV, INSIDE-GOOD
LIFT <- R4 case split on the other contraction
        AND: CASES, ONE, X
ONE <- R5 exception bijection
       AND: ROT, NO-PAIR
X  <- R6 proposed repair within the original D-cover
      AND: COVER-ESCAPE

Diagnostic restricted G route:
G_restricted <- AND: SIMPLE, SHORT, NO-FIVE-CYCLE

Separate certificate theorem in PARTIAL.md:
Ccert <- AND: B, GL, ONE, FINITE-CERT
```

The restricted G route is not an alternative proof of G for arbitrary T, since NO-FIVE-CYCLE is not among the original hypotheses. The two branches of LIFT are an AND case split, not alternatives from which the favourable case may be chosen.

## Critical findings

REFUTED. INSIDE-GOOD fails at V=11. Both degree-4 contractions of the unique interior vertex of an innermost bad four-cycle lose the pair. CURV is true and does not imply INSIDE-GOOD.

REFUTED. COVER-ESCAPE fails at V=18. The relevant cover has one exceptional tree matching and one non-tree orientation. Existence of successful tree matchings in another cover supplies no bridge to the proposed fixed-cover repair.

PROVED-HERE. The conditional certificate theorem closes without either unsupported general assertion. Its extra premise is a finite certificate with one-sided contractions at every contraction node. That premise is not claimed universally.

## Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Every rooted simple T with a pair has a TM by this induction | root | R0 | root | Proposed route | failing |
| B | Octahedron base has a TM at each root | C0,Ccert | R0 / AND | algebraic/logical step | Two explicit state choices; small certificate replay | discharged |
| S | Separating-triangle step preserves existence | C0 | R0 / AND | major claim | R1 | discharged |
| PC | Pair excludes black-inner separating triangle | S,G | R1 / AND | proved earlier | Sol INTEGRATION section 2 | discharged |
| GL | Pair-compatible cap gluing multiplies TM sets | S,Ccert | R1 / AND | proved earlier | Fable categorical Proposition 6, prior independent referee | discharged |
| SMALL | Capped pieces are simple, smaller and rooted correctly | S | R1 / AND | side condition | Pair criterion and cap construction | discharged |
| IH | Existence on smaller simple rooted instances with a pair | S,I | induction / AND | hypothesis | Strong induction assumption | discharged |
| I | Separator-free contraction step | C0 | R0 / AND | major claim | R2 | failing |
| D4 | Non-root degree-4 vertex exists | I | R2 / AND | algebraic/logical step | Euler gives at least six; only three roots | discharged |
| SIMPLE | At each such vertex at least one merge is simple when V>6 | I,G_restricted | R2 / AND | proved earlier | G.md section 7 | discharged |
| G | Some such merge preserves the pair | I | R2 / AND | major claim | R3 attempted | failing |
| SHORT | Bad merges have exact four-/five-cycle witnesses | G,G_restricted | R3 / AND | proved earlier | G.md section 3 | discharged |
| CURV | Chordless short disks contain degree-4 interior vertices | G | R3 / AND | proved earlier | G.md section 4 | discharged |
| INSIDE-GOOD | An innermost bad disk contains a good degree-4 vertex | G | R3 / AND | too strong | V=11 certificate disproves it | failing |
| LIFT | A contraction TM yields a TM of T | I | R2 / AND | major claim | R4 | failing |
| CASES | Other contraction has a TM or does not | LIFT | R4 / AND | algebraic/logical step | Excluded middle for finite sets | discharged |
| ONE | One-sided case succeeds | LIFT,Ccert | R4 / AND | proved earlier | X.md section 1 and PARTIAL.md | discharged |
| ROT | Exceptions biject and produce a TM of the other contraction | ONE | R5 / AND | proved earlier | Fable Theorem 3, forest calculation restated here | discharged |
| NO-PAIR | Other contraction has no pair in the certificate rule | ONE | R5 / AND | hypothesis | Explicit certificate condition | discharged |
| X | In the two-sided case a contraction has a nonexceptional TM | LIFT | R4 / AND | major claim | R6 attempted | failing |
| COVER-ESCAPE | Every exceptional cover has a nonexceptional TM orientation | X | R6 / AND | too strong | V=18 certificate disproves it | failing |
| NO-FIVE-CYCLE | T has no chordless five-cycle | G_restricted | restricted / AND | side condition | Additional restricted-theorem hypothesis | diagnostic only |
| Ccert | Every certified instance has a TM | separate root | certificate induction | root | PARTIAL.md | discharged |
| FINITE-CERT | Reduction certificate exists and has the listed rules | Ccert | certificate / AND | hypothesis | Explicit premise, not a universal claim | discharged |

## Verdict

NOT ESTABLISHED BY THIS PROOF for C0. The attempted G route fails at INSIDE-GOOD, and the attempted fixed-cover repair fails at COVER-ESCAPE. Neither counterexample disproves G or X themselves. Their unrestricted statements remain missing premises for a cancellation-free induction. FOLLOWS for the separate conditional certificate theorem Ccert.
