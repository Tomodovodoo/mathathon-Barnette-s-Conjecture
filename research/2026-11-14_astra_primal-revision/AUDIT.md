# Reverse-Lamport audit of the corrected primal note

## Audit boundary

PROVED-HERE. This is the implementation author's second audit, not a second independent referee. The audited source is proofs/primal/PRIMAL-PROOF.md after the revision, including Remarks 14 and 15 and the phase comparison. Numerical checks and Lean declarations are corroboration, not premises.

C0 is the exact quantified claim: for every finite simple cubic bipartite 3-edge-connected genus-zero plane map G and every edge e0, there is a perfect matching P containing e0 whose complement is connected. The final corollary applies this to every cubic bipartite 3-vertex-connected planar graph.

Accepted primitives are finite graph definitions, elementary linear algebra and polynomial arithmetic, strong induction, Euler's formula for sphere maps including disconnected submaps, and integral max-flow/min-cut with integer capacities. Map surgery is checked on the cyclic dart lists as explained in Section 2. Euler is the only imported planar theorem. The sphere-map convention includes the grouping of boundary walks into faces after a disconnection; an arbitrary list of unrelated rotations would not provide that grouping.

## Obligation graph

All routes below are primary AND routes; the two induction cases are exhaustive cases, not OR alternatives. Nodes R14 and R15 are separate supplementary roots, not premises of C0.

```text
C0 <- induction (H, CASE, IRR, CAP, SMALL, SYNC)
BARNETTE <- specialization (C0, V3)
IRR <- recovery (PAIR, NONZERO, TREE, MATCH, CONNECT)
PAIR <- integral flow (BAL, FLOW, DEFICIT, NONTRIVIAL)
NONZERO <- two expansions (PAIR, CANCEL, GROUP, SLOPE, MIN)
CANCEL <- fixed-second reversal (TAIL, DISK, INV)
GROUP <- independent circuit directions (SIMPLE, TAIL, DISK, SIGN)
SLOPE <- cut flux (ORIENT, CHARGE, POT, WHITE)
DISK <- four counts (CUT, REGION, STATECOUNT, DEG)
ORIENT <- facial boundary pairing (BOUNDARY, SPAN, CUT)
REGION <- deletion and Euler (SHORES, SURGERY, EULER)
TREE <- augmented Q (TAIL, ROOTS, CUT, BAL)
MATCH <- white parent edges (TREE, DEGREES)
CONNECT <- contradiction (COMPAT, DISK, MATCHCUT, ROOTS, CUT)
CAP <- contraction (SHORES3, ENDS3, COLOURS3, SURGERY, LIFT)
R14 <- orientation toward roots (FOREST, ROOTS, CUT)
R15 <- compatible matching iff connected complement (CONNECT, PFOREST, ROOTSEP, TAIL)
PHASE <- local-sign count (DISK, EXPONENT)
```

## Critical findings

The missing Lemma 3 implication is now written as delta(f,g) = coefficient of e in the receiving facial boundary = minus its coefficient in the departing boundary. The inner product at a circuit face is 1-1, not an unsupported appeal to cancellation. The common rotation sense is global. These changes discharge ORIENT without importing an unstated geometric argument.

The general circuit-cut argument precedes Lemma 1. Its proof allows parallel face links before 3-edge-connectivity excludes them. This removes the forward citation that previously required a scope explanation. REGION explicitly tracks edge deletions and isolated-vertex removal. Both shores remain essential: connectedness of one merges its incident faces, and connectedness of the other permits the stated Euler subtraction.

The general Lemma 12 uses only a state and a compatible perfect matching. Its root edge is defined to be the matching edge at b0. This avoids accidentally retaining the prescribed edge as an extra hypothesis in the generalized statement. The main construction supplies the prescribed edge separately in MATCH.

REFUTED: referee M4's assertion that the phase ratio varies with circuit count. The referee's own ratio simplifies to i^n. The direct argument uses t=sum delta, divisible by three by DISK, and compares i^(n-t) with i^(t/3). It does not extend the claim to arbitrary triangle systems without the disk property. Sign conventions and weights must be aligned before comparing whole polynomials. This is a correction to provenance, not a change to the existence proof.

R14's converse does not assume a partner: orient each Q tree toward its unique root, then assign each edge's tail to its black endpoint. R15's converse does not assume a forest state: P is a face forest because its complement is connected. The two nonmatching root edges join its two components, since otherwise a face circuit would be a cut crossed once by a cycle. Removing the matching root edge then gives three root trees. Thus neither supplementary proof is circular.

The computed claims are finite claims only. The plantri census and imported checker code are not formally verified. No claim about every Hamiltonian cycle arising specifically from a forest pair is made.

## Dependency table

Every discharged obligation stops at the stated primitive or the earlier claim named in its support. The finite algebra inside a node is not a new theorem assumption.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Prescribed-edge matching with connected complement | root | induction | root | IRR, CAP, SMALL, SYNC | discharged |
| V3 | Cubic simple 3-vertex-connected planar graph admits a sphere embedding and has no cut of size below three | BARNETTE | specialization | algebraic/logical step | definition of planar; at most two cut ends would separate vertices, small shores excluded by simplicity and degree | discharged |
| BARNETTE | Hamiltonian cycle avoiding any specified edge in the original conjecture class | root | specialization | root | C0 and V3; connected degree-two complement | discharged |
| H | Finite simple cubic bipartite 3-edge-connected sphere map | C0 | induction | hypothesis | Theorem T | discharged |
| CASE | Either all three-cuts trivial or one nontrivial cut exists | C0 | cases | algebraic/logical step | finite excluded-middle split | discharged |
| IRR | Conclusion when all three-cuts trivial | C0 | construction | major claim | PAIR, NONZERO, TREE, MATCH, CONNECT | discharged |
| BAL | A and X both have n elements | PAIR, TREE | counts | proved earlier | Lemma 1, degree sums and Euler | discharged |
| SIMPLE | Three distinct incident faces; no parallel face links | GROUP | setup | proved earlier | Lemma 1, general cut fact, H | discharged |
| FLOW | Capacity criterion gives a spanning incidence 2-factor | PAIR | max-flow | named theorem | finite integer capacities 2,1,2; balanced parts | discharged |
| DEFICIT | Minimal deficient Y has d=4-2k-c/3, k>=1, c positive divisible by 3 | PAIR | counting | algebraic/logical step | Lemma 4; subgraph rule and two colour counts | discharged |
| NONTRIVIAL | Deficit forces a three-cut with at least two vertices per shore | PAIR | contradiction | side condition | facial cycle inside; root and white endpoint outside | discharged |
| PAIR | At least one incidence pair | IRR, NONZERO | flow | major claim | BAL, FLOW, DEFICIT, NONTRIVIAL | discharged |
| BOUNDARY | Coherent boundary coefficient equals local delta | ORIENT | local rotation | definition | global orientation and displayed coefficient identity | discharged |
| SPAN | Facial boundaries span the real and mod-two cycle spaces | ORIENT, CUT | rank | algebraic/logical step | face-incidence connectivity, Euler, unique boundary dependence | discharged |
| CUT | Face circuits exactly bonds | DISK, TREE, CONNECT | orthogonality | proved earlier | general circuit-cut fact, path-sum cut-space proof | discharged |
| SHORES | Bond shores connected; mixed face meets a cut edge | REGION | minimality/walk | algebraic/logical step | proper subcut contradiction; closed boundary traversal | discharged |
| SURGERY | Deletion and contraction have the stated face effects | REGION, CAP | dart lists | definition | splicing/removing successors; Euler bridge test | discharged |
| EULER | v-e+f=1+c for sphere maps | REGION | subtraction | named theorem | genus-zero inherited maps, connected remainder | discharged |
| REGION | |S|+|U_S|=|E_S|+1 | DISK | deletion | proved earlier | Lemma 2(b), SHORES, SURGERY, EULER | discharged |
| STATECOUNT | U is assigned inner faces union circuit faces with overlap ell | DISK | bijection | algebraic/logical step | root exclusion and no-pinch in Lemma 2; state bijection | discharged |
| DEG | Cubic and colour counts in (4.2) | DISK | incidence count | algebraic/logical step | count internal and boundary ends separately | discharged |
| DISK | h=2ell+3 and delta sum=-3sigma | NONZERO, CANCEL, CONNECT | elimination | major claim | DEG, REGION, STATECOUNT, ORIENT | discharged |
| ORIENT | One sigma on every circuit cut | DISK, SLOPE | gradient | proved earlier | Lemma 3, BOUNDARY, SPAN, connected shores | discharged |
| WHITE | White count on state cut side is black count plus one | SLOPE | degrees | algebraic/logical step | DEG and DISK | discharged |
| CHARGE | Path flow has stated divergences | SLOPE | path sum | algebraic/logical step | connected G; one path to each white vertex | discharged |
| POT | Three local differences are consistent integers | SLOPE | sum zero | side condition | zero divergence at every nonroot black vertex | discharged |
| SLOPE | Positive orientation slope equals positive white count | NONZERO | flux | proved earlier | Lemma 6, ORIENT, CHARGE, POT, WHITE | discharged |
| TAIL | One outgoing link per nonroot face, none per root | CANCEL, GROUP, TREE | incidence | definition | state is a bijection onto X | discharged |
| INV | Circuit choice depends only on s; tail reversal is a sign-reversing involution | CANCEL | reversal | algebraic/logical step | tails become old heads, odd length, third-corner sign flip | discharged |
| CANCEL | Every cyclic second-state coefficient vanishes | NONZERO | involution | proved earlier | Lemma 7, TAIL, DISK, INV | discharged |
| SIGN | Positive h-cycle sign is (-1)^((h+3)/2) | GROUP | sign count | algebraic/logical step | delta sum=-3 and h odd | discharged |
| GROUP | Group contribution is (6.3) | NONZERO | directions | proved earlier | exactly 2^c independent orientations; SIGN | discharged |
| MIN | Lowest possible circuit count coefficient is nonzero | NONZERO | coefficient | algebraic/logical step | finite nonempty pairs; positive products of slopes; common sign | discharged |
| NONZERO | A pair with circuit-free Q exists | IRR | contradiction | major claim | GROUP, MIN, CANCEL | discharged |
| ROOTS | Forest with one outgoing link per nonroot has one root per component | TREE, CONNECT, R14 | v-1 count | algebraic/logical step | outgoing degree sum on each tree | discharged |
| TREE | Augmented Q complement is a primal spanning tree | IRR, MATCH | cut exclusion | proved earlier | Lemma 9, ROOTS, CUT, edge count | discharged |
| DEGREES | Recovery tree root black degree one, other blacks degree two | MATCH | removed edges | algebraic/logical step | distinct black endpoints of Q edges and root-star deletion | discharged |
| MATCH | White parent edges form a matching through prescribed e0 | IRR | rooted tree | proved earlier | Lemma 10, TREE, DEGREES | discharged |
| COMPAT | Matching edge at b lies on s(b) | CONNECT | avoidance | side condition | matching avoids q_s(b), Lemma 10; hypothesis in general form | discharged |
| MATCHCUT | Cut supported on perfect matching has h=2ell | CONNECT | two counts | proved earlier | Lemma 11, matching and cubic degree equations | discharged |
| CONNECT | Any compatible matching has Hamiltonian complement | IRR, R15 | contradiction | major claim | Lemma 12, DISK versus MATCHCUT, ROOTS, CUT | discharged |
| SHORES3 | Both shores of a three-cut connected | CAP | cut size | algebraic/logical step | two components would each have boundary at least three | discharged |
| ENDS3 | Three distinct ends on each nontrivial shore | CAP | smaller cut | side condition | deleting a repeated end creates a cut of size at most two | discharged |
| COLOURS3 | Ends on a shore have one colour | CAP | congruence | algebraic/logical step | 3 divides 2ell-3 with 0<=ell<=3 | discharged |
| LIFT | Cap cuts lift to original cuts | CAP | contraction | algebraic/logical step | expand cap to contracted shore | discharged |
| CAP | Both caps satisfy Theorem T hypotheses | C0 | contraction | major claim | SHORES3, ENDS3, COLOURS3, SURGERY, LIFT | discharged |
| SMALL | Each cap is strictly smaller | C0 | induction | side condition | each contracted shore has at least two vertices | discharged |
| SYNC | Cap cycles omit same cut edge and glue, preserving avoidance | C0 | splice | algebraic/logical step | first cap retains e0; request its omitted edge in second; two spanning paths | discharged |
| FOREST | Q_s forest in R14 | R14 | assumption | hypothesis | Remark 14 | discharged |
| R14 | Partner iff one root per Q component; unique; no partner gives no recovery tree | supplementary root | orientation | major claim | FOREST, ROOTS, CUT and two added root links | discharged |
| PFOREST | Connected matching complement makes P a two-component face forest | R15 | cut test | proved earlier | CUT and |P|=n+1 | discharged |
| ROOTSEP | Other root edges cross these two components | R15 | parity | algebraic/logical step | internal root edge would close a cut met by Hamiltonian cycle once | discharged |
| R15 | Compatible state iff Hamiltonian complement; unique | supplementary root | orient forest | major claim | CONNECT, PFOREST, ROOTSEP, unique orientation toward roots | discharged |
| EXPONENT | i^(n-t)/i^(t/3)=i^n when 3 divides t | PHASE | powers | algebraic/logical step | exponent difference n-4t/3 | discharged |
| PHASE | Aligned real polynomial equals i^n times Lean polynomial | supplementary root | termwise | major claim | DISK, EXPONENT, identical weight products | discharged |

## Verdict

FOLLOWS. C0 closes through IRR and CAP with strictly smaller caps and synchronized omitted edges. ORIENT and REGION now contain the missing local arguments. R14, R15 and PHASE close separately; none is used to rescue the main proof. The only rejected referee assertion is M4's circuit-count dependence, refuted at EXPONENT. Human review and a formalization of this exact exposition remain outside this audit.
