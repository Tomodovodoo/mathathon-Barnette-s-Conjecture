# Reverse-Lamport audit of the revision

## Audit boundary

PROVED-HERE denotes the written proofs in involutions.tex. The root contract C0 is: for every finite simple face-bicoloured sphere triangulation with outer black face t0, if disjoint states exist, there is a pair whose Q_s is a forest. The separate contract W is termination of the alternating constructor from any second-fixed start. The changed proof route under audit is Section 5, the face-path replacement, together with the unchanged maps in Sections 3 and 4 and the corrected coefficient comparison in Section 8.

Accepted primitives are finite signed-set cancellation, elementary bijection algebra, oriented sphere-map subdivision, Jordan separation for a simple incidence cycle, and Euler's formula for a triangulated disk. The disk is connected because its underlying space is a disk with the inherited triangulation. Earlier proved results accepted at their checked contracts are Lemma 2, the disk count and enclosed-white-face existence, and the directed-cycle reversal bijections verified in Lemmas 4 and 5. Pair existence is a hypothesis, not an inferred consequence of a Hamiltonian-cycle theorem. The audit checks the supplied route; computations support but do not replace it.

## Obligation graph

Every listed group is AND. There is one supplied path-mode route, no rescue alternative.

```text
C0 <- R0: H, M, A, B, F, N
M  <- R1: H, finite pairs, odd cycle disk count
A  <- R2: K, S, D
B  <- R3: L, U, E, V
L  <- R4: T, X, Z
F  <- R5: L, M, I, Q
N  <- R6: A, B, F, finite signed counting
W  <- R7: A, B, F, G
P  <- R8: Eps, Expansion, B, F, Parity
```

C0 is the forest-pair conclusion. M is existence and positivity of the minimum cycle count. A and B are the first and second sign-reversing involutions with their exact fixed sets. L is the path-list crossing lemma. F is positivity and common sign of the second-fixed set. N is the nonzero imbalance. W is termination. P is the corrected signed-moment identity. Obligations are specified below.

## Critical findings

The bridge L is the main new obligation. A face-path step alone is not an unconditional token: the selected corner must be the corner cut off by its two boundary sides. With that eligibility condition, a step crosses one formal incidence, so there is neither an omitted crossing nor an extra token. Increasing path order is the order needed by the original maps. The third-corner turn crosses neither incidence of the chosen cycle. Thus there is no switch from side cycles to incidence cycles without a bridge.

Both steps of the return move use data they preserve. First-map cycle choice uses s only. Second-map choice uses the unoriented cycle, its assigned white face and its first/nonfirst status. Token collision is excluded by distinct cycles, not by distinct white faces. Independent orientation choices are available because cycle reversal swaps two matchings locally. These checks also cover repeated white faces and repeated black-face IDs across different white paths.

The earlier coefficient exponent was REFUTED off the main route. The corrected exponent is the sum of the two phase exponents, giving (n+m)/2. No assumption about arbitrary weights or arbitrary mark counts enters the proof. The higher-mark zero count depends on the rays and is now qualified.

## Dependency table

All classifications are primary classifications. Every leaf has an exact accepted justification.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | A forest pair exists under H | root | R0 | root | M,A,B,F,N | discharged |
| H | T is as stated and the finite pair set is nonempty | C0,M | R0,R1 | hypothesis | theorem contract | discharged |
| M | m is a positive attained minimum, c(p)>=m | C0,B,F | R1 | major claim | H, finiteness, nonempty cycle covers | discharged |
| A | First map is an involution, reverses signs off forests | C0,N,W | R2 | major claim | K,S,D | discharged |
| K | First Q_s cycle is selected from invariant s | A | R2 | definition | Section 3 order, disjoint supplying sets | discharged |
| S | First reversal is a disjoint-state bijection and retains all tokens | A | R2 | proved earlier | Lemma 4, eligibility uses s only | discharged |
| D | First reversal changes J by +/-2 and retains all bits | A | R2 | proved earlier | Lemmas 2 and 4; local delta identity | discharged |
| B | Second map is involutive with exact fixed set and opposite nonfixed signs | C0,N,W,P | R3 | major claim | L,U,E,V | discharged |
| L | Path lists alternate, have inside parity and first-exit sign | B,F | R4 | major claim | T,X,Z, Section 5 Lemma 7 | discharged |
| T | A path visits each face at most once; each token has a unique step and corner | L | R4 | definition | dual tree paths and the common corner of distinct sides | discharged |
| X | A turn cuts off its common corner and crosses only that formal incidence, with sign -kappa away from centre | L | R4 | algebraic/logical step | two local cyclic orders checked in Lemma 7 | discharged |
| Z | Listed steps change components of the cycle cut; endpoint is outside | L | R4 | named theorem | Jordan separation applies to simple incidence cycles, which preserve side-cycle orientation and white faces | discharged |
| U | All marked implies exactly m cycles and one token each | B | R3 | algebraic/logical step | c>=m and exactly m tokens; otherwise unmarked case | discharged |
| E | Partners exist, remain eligible, do not collide; priority and reversal decisions return | B,P | R3 | side condition | Lemma 7 and Lemma 5, distinct cycle incidences, paired indices both nonfirst | discharged |
| V | Sign flips by a direction change or by J parity with two direction changes | B | R3 | algebraic/logical step | L, cycle reversal changes J by +/-2, other tokens on other cycles | discharged |
| F | Second fixed count is F>0 with common sign (-1)^floor(m/2) | C0,N,W,P | R5 | major claim | L,M,I,Q | discharged |
| I | Each cycle encloses a white face and has a first exit; unique independent orientation makes it eligible | F | R5 | proved earlier | Lemmas 2,6,7 and independent matching swaps | discharged |
| Q | q counterclockwise fixed cycles give J=m-2q and direction sum q | F | R5 | algebraic/logical step | L, then floor((m-2q)/2)+q=floor(m/2) | discharged |
| N | Signed sum is nonzero, forcing a first fixed object | C0 | R6 | algebraic/logical step | A,B,F and finite orbit cancellation | discharged |
| W | Every alternating start terminates at a forest without repetition | separate root | R7 | major claim | A,B,F,G | discharged |
| G | Two-labelled finite component from a second-fixed point is a path; a second-fixed terminal would have opposite sign | W | R7 | algebraic/logical step | degree at most one per label; odd path parity; Lemma 8 | discharged |
| P | Normalized m-th moment equals (-1)^((n+m)/2) F | separate root | R8 | major claim | Eps,Expansion,B,F,Parity | discharged |
| Eps | epsilon=(-1)^ceil(n/2) (-1)^floor(J/2) | P | R8 | algebraic/logical step | J=n mod 2, elementary integer floors | discharged |
| Expansion | Lower ordered moments cancel; repetitions at order m leave an unmarked cycle; distinct sets have m! orderings | P | R8 | algebraic/logical step | unmarked-cycle reversal, token eligibility, m minimal | discharged |
| Parity | ceil(n/2)+floor(m/2)=(n+m)/2 | P | R8 | algebraic/logical step | n=m mod 2, checked for both parities | discharged |

## Verdict

FOLLOWS. The path-mode route to C0 closes at L through T, X and Z; its remaining obligations close through the written checks E and V and the nonempty fixed-set argument I and Q. W and the corrected off-route comparison P also follow. There is no circular dependency, unbridged representation switch or failing leaf on these supplied routes. This is a self-audit of the revision, not an independent referee verdict on the new lemma.
