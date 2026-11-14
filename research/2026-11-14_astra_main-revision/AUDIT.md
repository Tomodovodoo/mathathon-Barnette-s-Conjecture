# Reverse-Lamport audit of version 2

## Audit boundary

The exact conclusion C0 is Theorem 1.1: for every finite simple cubic bipartite planar 3-connected graph `G` and every edge `e` of `G`, a Hamiltonian cycle of `G` avoids `e`. The stronger induction conclusion C2 is Theorem 6.2: every coloured sphere triangulation `T`, with any facial triangle `t0` and any side `e0` of that face, has an acyclic selection containing `e0`. A coloured triangulation is simple, has at least four vertices, has triangular facial boundaries and has opposite face colours across every edge. A selection has exactly one side in every face.

Scope is the final `paper/main/barnette.tex`, Sections 2 through 6, with the exact source and PDF fingerprints in `verification.json`. Version 1 and the independent referee's `REFEREE.md` were comparison material. Neither the referee's verdict nor the Lean formalisation is a premise in this audit. I am the reviser, not a new independent referee.

Status convention: the dependency deductions below are PROVED-HERE, with their arguments stated in the support column and the cited manuscript proofs. Finite checks are COMPUTED only for the ranges in `verification.json`, `example.json` and `independent/examples.json`. Historical/source assertions are LIT in `CHANGES.md`; none is used as an unsupported replacement proof.

Accepted background is the Jordan curve theorem on the sphere, Euler's formula for a connected embedded graph, the elementary plane-dual construction and cyclic order at a vertex, integral max-flow/min-cut for finite networks with integral capacities, and elementary finite graph and polynomial algebra. In particular, connected 2-regular graphs are cycles, trees have unique paths, a nonempty even-degree graph contains a cycle, cycles cross cuts evenly, and a forest in a connected graph extends to a spanning tree. For the explicitly supplied contraction alternative to Lemma 2.5(2), also accept the elementary duality of contracting a nonloop primal edge and deleting its dual, and connectivity of the dual of a connected sphere graph. Its conditions are checked below. Do not accept the disk identity, partner existence, positive height increment or recovery theorem as background.

## Obligation graph

Every listed route is an AND route. The separating and nonseparating cases are both required by C2. There is one supplied alternative, for the connectivity clause of Lemma 2.5(2); it is not needed to rescue the primary route.

```text
C0 <- R0 AND H0, C1, C2, C3, O1
C1 <- R1 AND H0, O2
C2 <- R2 AND O3, A0, B0
A0 <- R3 AND O4, C17, C16, C7
B0 <- R4 AND C18, O5, O6, C3
C3 <- R5 AND C4, C5, O7, O8
C4 <- R6 AND O9
C5 <- R7 AND O10, O11, O12
  forest-connectivity clause <- R7a supplied alternative AND O13
C7 <- R8 AND C8, C6, C10, O14
C8 <- R9 AND C9, C5, O15
C9 <- R10 AND O16
C6 <- R11 AND C4, O17, O18, O19
C10 <- R12 AND O20
C11 <- R13 AND C10, O21
C12 <- R14 AND C11, O22
C13 <- R15 AND C6, O23
C14 <- R16 AND C11, C12, C13, O24
C15 <- R17 AND C6, C5, O25, O26
C16 <- R18 AND C14, C13, C15, C19, O27, O28
C19 <- R19 AND O29
C17 <- R20 AND O30, O31, O32, O33
C18 <- R21 AND C4, O34, O35
```

C6 is shared by recovery, signs and positivity. It requires a state, not a pair. C16 assumes only that at least one pair exists, not that a good state exists. C17 provides that assumption in the nonseparating case without using C16. C7 assumes goodness and proves recovery without invoking the existence argument. These separations rule out the tempting circular reading of the exposition.

## Critical findings

All conclusion-reachable obligations close. The source comparison found two accidental replacements of `Phi` by `Psi` in the duality proof; they were corrected before this audit. The change of the third root from `c` to `o` was checked in the selection-to-state lemma, the excluded sides, the good-state lemma, the face-tree proof and the root-component case of the density proof. The disk identity's new standalone statement has exactly the old proof's assumptions.

The main inference to check after the opening rewrite is C16. Heights supply the positive increments in O26. They do not replace the exponential sum. The finite-difference identity C19 is what turns the regrouped count into a nonzero expression at the minimum number of cycles. The revised source attribution states this distinction.

The weight in C14 depends only on the second state. The chosen cancellation cycle also depends only on that state. Thus the same cycle is chosen after the first reversal, the weight is preserved, and the involution has no fixed point. C12's other reversal exchanges both states on a `D` cycle and is used for a different grouping. No route silently exchanges these two operations.

The disk argument counts the connected region `R_Z`, not a potentially disconnected induced subgraph. It explicitly checks its facial boundaries, then invokes C4 before Euler. O18 uses injectivity and surjectivity separately. The density argument permits repeated edges in a face boundary walk; its signed boundary count counts each occurrence, including both sides of a bridge. The root component contains all three roots, which are joined by `t0`.

The induction preserves the prescribed side. Both pieces are strictly smaller; colour exchange is harmless because the definition of selection does not depend on face colours. Gluing arbitrary selections would fail O6, but the proof prescribes the first selection's unique cap side in the second piece. The use of two induced trees here is C3, proved without using the induction.

The eight referee corrections concern either statements outside the main route or clarity of finite examples. They were checked separately: signed heights give a Laurent polynomial; nonzero requires a pair; recovery injectivity requires goodness; the table contains eight pairs; the exhaustive range is specified; both connectivity counterexamples now have proofs; and the construction claim is limited to efficiency. The finite reruns confirm the printed numbers, including the signed moments and negative Laurent exponents. These computations do not discharge a universal node of this graph.

## Dependency table

All statuses are explicit. An item labelled “proved earlier” points to its expanded claim node rather than to an unnamed fact.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Hamiltonian cycle avoiding the given edge under the full theorem contract | root | R0 | root | C1, C2 and C3, with O1 | discharged |
| H0 | G is finite, simple, cubic, bipartite, planar, 3-connected; e is its edge | C0,C1 | R0,R1 | hypothesis | Theorem 1.1 | discharged |
| C1 | The embedded dual is a coloured triangulation | C0 | R1 | major claim | Lemma 2.1 and O2 | discharged |
| C2 | Any facial side has a containing acyclic selection | C0 | R2 | major claim | Theorem 6.2, both cases | discharged |
| A0 | C2 holds without a separating triangle | C2 | R3 | major claim | Pair, good state, recovery | discharged |
| B0 | C2 holds when a separating triangle exists | C2 | R4 | major claim | Smaller pieces and prescribed gluing | discharged |
| C3 | An acyclic selection has a Hamiltonian complementary dual and two induced tree components | C0,B0 | R5 | major claim | Proposition 2.6 | discharged |
| C4 | A finite sphere graph whose facial boundaries are cycles is connected | C3,C6,C18 | R6 | major claim | Lemma 2.2 | discharged |
| C5 | Cycle separation, forest-dual connectivity and tree/cotree | C3,C8,C15 | R7 | major claim | Lemma 2.5; optional R7a for connectivity | discharged |
| C6 | A state-directed cycle satisfies W=B+1 and h=2 ell+3 | C7,C13,C15 | R11 | major claim | Lemma 3.8, three counts | discharged |
| C7 | A good state gives an acyclic selection containing e0 | A0 | R8 | major claim | Proposition 3.9 | discharged |
| C8 | The face tree gives one selected side at every face, at s(t) in each bounded black face | C7 | R9 | major claim | Lemma 3.6 | discharged |
| C9 | Goodness is equivalent to S_s being a spanning tree | C8 | R10 | major claim | Lemma 3.5 | discharged |
| C10 | Outdegree at most one forces directed cycles and tree/unicyclic component counts | C7,C11 | R12 | major claim | Lemma 3.7 | discharged |
| C11 | A partner orients Q_s; acyclic Q_s is good; each good state has exactly one partner | C12,C14 | R13 | major claim | Lemma 4.2 | discharged |
| C12 | Both prescribed reversals preserve the pair conditions | C14 | R14 | major claim | Lemma 4.3 | discharged |
| C13 | Both reversals flip sign; eps=(-1)^((n+c)/2+c+) | C14,C16 | R15 | major claim | Lemma 4.4 | discharged |
| C14 | Fixed-s cancellation leaves only good states for any function F(s) | C16 | R16 | major claim | Lemma 4.5 | discharged |
| C15 | Clockwise-to-counterclockwise reversal raises omega by L(C), with L(C)>=1 | C16 | R17 | major claim | Lemma 4.6 | discharged |
| C16 | If a pair exists, a good state exists | A0 | R18 | major claim | Proposition 4.8 | discharged |
| C17 | No separating triangle implies existence of a pair | A0 | R20 | major claim | Proposition 5.2 | discharged |
| C18 | Each capped side is a smaller coloured triangulation | B0 | R21 | major claim | Lemma 6.1 | discharged |
| C19 | The alternating c-fold difference of degree m<=c is zero for m<c and (-1)^c c! product L_i for m=c | C16 | R19 | major claim | Lemma 4.7 | discharged |
| O1 | e0 crosses e, so deleting P* deletes e when e0 is selected | C0 | R0 | definition | Definition of crossing dual edges, final proof | discharged |
| O2 | No edge cut of size <=2; no dual loop/parallel pair; triangular faces, >=4 vertices and opposite colours | C1 | R1 | algebraic/logical step | A small edge cut gives a vertex cut of size <=2 after excluding sides of size 1 or 2 by cubic simplicity. A dual loop/2-cycle gives such an edge cut by Jordan. Cubicity gives length-three boundary walks, dual simplicity makes them triangles. Euler gives the size bound; bipartition gives colours. | discharged |
| O3 | Induction on the positive finite vertex count; separating/nonseparating cases exhaust all cases | C2 | R2 | side condition | Theorem 6.2 and C18 strict decrease; no separate invalid minimal graph is assumed | discharged |
| O4 | t0 may be made black without changing selections | A0 | R3 | definition | Global colour exchange preserves every hypothesis and edge prescription | discharged |
| O5 | t0 stays in the first smaller piece; both induction calls have valid facial sides | B0 | R4 | side condition | t0 is a face on one side of the separating cycle; second prescription is a side of the cap; C18 supplies both smaller domains | discharged |
| O6 | Selections share only their prescribed cap side; union is a selection and has no cross-piece cycle | B0 | R4 | algebraic/logical step | Each original face keeps exactly its old selected side. C3 separates the third cap vertex from the endpoints. A cross-piece cycle would create a length>=2 path between cap vertices, contradicting the unique cap-edge path in the corresponding tree. | discharged |
| O7 | Counts are k black faces, k white faces, 3k edges and k+2 vertices; a selection has k edges | C3 | R5 | algebraic/logical step | One black/white face per edge, triangular faces, C4 then Euler; each selected edge pairs one face of each colour | discharged |
| O8 | Complement is connected 2-regular; P has two components and all intra-component edges selected | C3 | R5 | algebraic/logical step | Degree two follows from one selected side. C5 gives connectivity. Forest count gives two components. An unselected intra-component edge would close a cycle meeting the Hamiltonian complementary dual in exactly one cut edge, violating cut parity. | discharged |
| O9 | A component together with its incident open faces is both open and closed in the sphere | C4 | R6 | algebraic/logical step | Cyclic face boundaries lie in one component; local rotation neighbourhoods give openness of that union and its complement. Sphere connectedness rules out another component. | discharged |
| O10 | A primal cycle separates two nonempty face sets and dual steps change sides exactly across it | C5 | R7 | named theorem | Jordan curve theorem; an embedded simple cycle has both adjacent faces across each edge. Dual edges cross only their own primal edge. | discharged |
| O11 | Disconnected complementary dual produces a nonempty even boundary-edge set contained in N | C5 | R7 | algebraic/logical step | Faces in one dual component give membership changes around each vertex in even number. Connected M makes this boundary nonempty. Each boundary edge must have been deleted. An even nonempty set has a cycle, contradicting N acyclic. | discharged |
| O12 | When N is a spanning tree the connected complementary dual has exactly F(M)-1 edges | C5 | R7 | named theorem | Euler on connected finite M, and the tree's V(M)-1 edges | discharged |
| O13 | The supplied contraction alternative proves forest-dual connectivity | C5 connectivity clause | R7a, supplied alternative | named theorem | Extend N to a spanning tree K of connected M; contract the edges of K, each a nonloop at contraction. Contraction/deletion duality leaves M* minus K* connected as the dual of the resulting one-vertex sphere graph. Adding K* minus N* preserves connectivity. | discharged |
| O14 | P_s minus e0 is state-directed; a cycle forces both W-B=1 and W-B=3; adding e0 closes no cycle | C7 | R8 | algebraic/logical step | C8 gives one outgoing chosen side per nonroot; C10 directs any cycle. Boundary selected edges match ell black and h-ell white faces out of the disk, so B-ell=W-(h-ell); C6 contradicts this. The remaining forest has one root per component by C10; e0 joins two different root components. | discharged |
| O15 | Y_s is a tree; black nodes have degree two except root t0 of degree one; selecting each black node's child matches every white node once | C8 | R9 | algebraic/logical step | C9 and C5 give tree/cotree. Only one side of each bounded black face is in S_s, while exactly two sides of t0 are. Alternating colours in a rooted tree give exactly the asserted matching; two faces share at most one side. | discharged |
| O16 | S_s adds the two unprescribed root sides to Q_s; acyclicity is equivalent to three distinct rooted components | C9 | R10 | algebraic/logical step | Q_s has n distinct edges on n+3 vertices; a forest has three components. Adding ao and bo creates no cycle exactly when all three roots are in different components. | discharged |
| O17 | The inside graph R_Z has precisely the bounded T faces inside Z plus one exterior face and is connected | C6 | R11 | side condition | Jordan plus triangular face boundaries; apply C4 to those cyclic boundaries before Euler. Roots are outside Z because every cycle vertex has positive outdegree and is nonroot. | discharged |
| O18 | The state bijection counts interior black faces as B=I+ell | C6 | R11 | algebraic/logical step | Injection avoids repetitions; surjection reaches each interior vertex through a face inside. At a boundary vertex the unique chosen outgoing side belongs to exactly its state's face, which lies inside precisely for the ell counted sides. | discharged |
| O19 | B+W=2I+h-2 and 3(B-W)=2ell-h imply the disk identities with O18 | C6 | R11 | algebraic/logical step | Euler on O17, triangular side counts, cancellation on inner edges, then substitution | discharged |
| O20 | h cycle edges have h distinct tails; a connected nu-vertex component has nu-gamma edges | C10 | R12 | algebraic/logical step | At most one outgoing edge per vertex; sum outdegrees and compare with nu-1 | discharged |
| O21 | r is a bijection onto nonroots; good Q_s has a unique root orientation and its tails define a partner | C11 | R13 | algebraic/logical step | Opposite side avoids s(t); r(t) is its tail. C10 supplies root-component conditions. Conversely every nonroot is the tail of one rooted-tree edge and every face supplies one edge. | discharged |
| O22 | Cycle tails/heads are the same distinct vertex set; all changed corners remain distinct from the other state's choices | C12 | R14 | algebraic/logical step | Q reversal swaps r(t),u(t), keeps s. D reversal swaps r(t),s(t) on the full cycle. Both permutations preserve the two bijections. | discharged |
| O23 | Each reversal negates one local sign per odd cycle edge; exact parity is (n+c)/2+c+ | C13 | R15 | algebraic/logical step | In each black face the three cyclic directed sides share delta. C6 makes lengths odd and their delta sums +/-3. Counting negative factors gives the displayed parity; n and c have the same parity. | discharged |
| O24 | Cancellation chooses a cycle using only s; reversal is fixed-point-free and keeps F(s); good s has one partner | C14 | R16 | algebraic/logical step | Fixed order on cycles, C12 involution, C13 sign flip, C11 uniqueness. Finite sums permit regrouping. | discharged |
| O25 | Each fixed simple face path exists and each crossing contributes +1 for leaving the reversed cycle and -1 for entering | C15 | R17 | side condition | Dual connectedness supplies paths; simple paths visit each black face once. The proof checks entry/exit through both possible sides and both black-face sides of the cycle. Paths start at y and end outside at t0. | discharged |
| O26 | Net crossings are the indicator that y is inside; summing y gives positive L(C), and distinct cycle increments add | C15 | R17 | algebraic/logical step | C5 side-change rule telescopes along the path. C6 gives at least one white face inside. Cycles use disjoint black faces, so contributions add. | discharged |
| O27 | Fixed undirected D classes have exactly 2^c independent orientations, with affine weight and the stated sign | C16 | R18 | algebraic/logical step | Reversing exactly one incident edge at a vertex would duplicate an r or s value. Hence orientations are constant choices around each cycle; C12 realizes all choices, C13 supplies sign, C15 supplies increments. | discharged |
| O28 | m is defined, classes with c>m vanish, and all classes with c=m have the same nonzero sign and positive product | C16 | R18 | side condition | Nonempty finite pair set defines m>=1. C19 kills higher-cycle classes. n congruent to m makes (-1)^((n-m)/2) common, and each L(C)>=1 by C15. At least one minimal class exists. C14 then forces a good state. | discharged |
| O29 | Boolean monomials missing an index cancel; degree c surviving terms use every index once in c! ways | C19 | R19 | algebraic/logical step | Expand the power, reduce positive powers of bits to the bit, and factor the finite alternating sum; valid also for m=0 and c=0 | discharged |
| O30 | An integral 2n flow in the stated finite capacity network yields disjoint states, and the cut minimum is the stated Hall-type expression | C17 | R20 | named theorem | Integral max-flow/min-cut with capacities 2,1,2. Saturation gives degree two on both incidence classes of size n; alternating even cycles split into two matchings. Place each black node on its cheaper cut side to obtain min(2,number of corners in S). | discharged |
| O31 | With U=V(T) minus S containing the roots, the cut inequality is e(U)-b(U)<=2|U|-4 | C17 | R20 | algebraic/logical step | For j corners in U, min(2,3-j)=2-max(0,j-1). Count each edge through its unique black face, accounting separately for t0; n+3 vertices yields the displayed constants. | discharged |
| O32 | Every induced component with p>=4 has length-three faces exactly the T faces with corners in that component | C17 | R20 | side condition | Connected component, simplicity, inducedness, and no separating triangle. The other side of any triangular face contains another component vertex; the face side cannot contain a T vertex. A residual edge would be parallel to a boundary edge. Boundary walks of a simple connected graph with p>=4 have length at least three. | discharged |
| O33 | Each component gives q-b_H<=2p-4 for the root component and <=2p for others | C17 | R20 | algebraic/logical step | Small components use q<=p(p-1)/2; the three-root component has q=3,b_H=1. For larger components O32 identifies triangular faces. Every other face of length d has 3 bal equal to a sum of d signs, hence bal<=d-4 by parity for d=4,5 and magnitude for d>=6. Sum balances, count boundary occurrences and use Euler to get q-b_H<=2p-4. | discharged |
| O34 | The three inner boundary faces of a separating triangle have a common colour | C18 | R21 | algebraic/logical step | Signed face-side count is divisible by three and equals three signs on the boundary, so all signs agree | discharged |
| O35 | Cap of the opposite colour gives a simple coloured triangulation with >=4 and fewer vertices | C18 | R21 | side condition | Subgraph simplicity, triangular boundaries and C4 connectivity. Each side of a separating triangle has an interior vertex; the piece retains one and omits those on the other side. O34 supplies boundary colour compatibility. | discharged |

## Verdict

**FOLLOWS.** PROVED-HERE: R0 closes through C1, C2 and C3; both required branches of C2 close. The decisive shared nodes are C6, C14, C15, C19, C17 and C7. Every conclusion-reachable obligation in the primary route is discharged, with no circular dependency, hidden additional hypothesis or unbridged change of route. This is a bounded revision audit of the exposition, not a fresh independent certification of the project or of every source cited in its closing remarks.
