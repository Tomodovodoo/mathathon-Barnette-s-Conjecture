# Referee of counting families and lower bounds

Reviewer GPT-6.1-sol. Submission boundary is FAMILIES, BOUNDS and CONJECTURE-TESTS in `../2026-11-14_sol_counting-families/`, including their retained certificate data. Mathematical arguments below are PROVED-HERE, T2; exact replay results are COMPUTED. The recovery and height lemmas are accepted supplied-preprint inputs, with the inverse argument for injectivity checked below. No author verification routine was executed.

## Claims and findings

### F1. Even prisms

Exact claim: for p=2m>=4 the p-prism has S=m, P=M=2, c_min=1, normalized signed polynomial z^(m-1)-1, H=2m+2, avoidance count 2 for a rail and 2m-2 for a rung. Fixed-root recovery yields two cycles per prescribed edge and six over the three prescriptions.

Verdict CORRECT, PROVED-HERE. The submission's explicit state list is exhaustive: one southern face must take the southern pole, and thereafter a path forces every other corner. Two indices give disjoint states only when they straddle every northern index, so they must be the two extremes. Their opposite edges are the displayed three rooted trees. The one cover spans all nonroots and has one cycle; its disk has m-1 white faces by the disk identity. This gives its two-term polynomial and leading coefficient m-1.

For H, at least two rungs must occur. If exactly two occur, the two rail paths must be spanning, so their omitted rail edges join the same adjacent pair of rungs, giving p choices. If more than two occur, a gap longer than one between consecutive used rungs forces both rail paths across that gap and closes an isolated cycle. Hence all rungs occur, and the two rails must be opposite alternating matchings, giving two further cycles. Equal matchings give disconnected squares, including at p=4. Each rail is omitted once in the p-cycle class and once in the alternating class. Each rung is omitted in p-2 of the first class. These prove the avoidance formulas, not merely their sum.

COMPUTED independent range: m=2,...,7, with all states and all primal perfect-matching complements and every edge's avoidance count. H=6,8,10,12,14,16. See `code/families.json`.

### F2. Tube definition, finite counts and recurrences

Exact construction: p even, p>=4, rings 0,...,L of length p, vertical edges, alternating diagonals indexed by parity, two cap poles. Root is {v_00,v_01,v_11} for L>=1 and a cap face for L=0. The graph is a simple Eulerian triangulation with no separating triangle, primal order 2p(L+1). For L>=1 its primal has p square faces, pL hexagonal faces and two p-gons, combining equal sizes.

Verdict CORRECT, PROVED-HERE. The listed edges triangulate a cylinder and two cap disks. Endpoint ring degrees are 4,6 alternating in opposite phases; internal ring degrees are six and poles have degree p. A graph triangle either meets a pole and uses adjacent cap vertices or uses two consecutive rings. Alternating diagonals make each such triple one of the actual strip faces. No ring has a triangle for p>=4. These exhaust the graph triangles, so no triangle separates. The special root at L=0 must not be substituted into the L>=1 formula.

COMPUTED: independent complete counts for p=4,L=0,...,5 and p=6,L=0,...,3 agree in S,P,M,c_min,H. For width four these are S=2,5,13,34,89,233 and H=6,14,30,70,166,382 with P=M=2 throughout. For width six they are S=3,16,91,513; P=2,4,16,56; M=2,4,12,34; H=8,44,176,752. Every case has c_min=1. All primal matchings, not merely recovery images, were used for H.

Exact recurrence-certificate claim: each submitted finite matrix, with its submitted initial and terminal vectors, has the scalar recurrence below. Lists [a1,...,ad] mean f_L=sum aj f_(L-j).

| p | Quantity | Sequence starts | Recurrence list | Matrix dimension |
|---|---|---|---|---|
| 4 | S | L=2, 13,34 | [3,-1] | 4 |
| 4 | M | L=2, 2 | [1] | 2 |
| 4 | P | L=2, 2 | [1] | 2 |
| 4 | H | L=0, 6,14,30 | [2,-1,4] | 12 |
| 6 | S | L=2, 91,513,2881,16171 | [7,-9,7,-1] | 15 |
| 6 | M | L=2, 12,34,82,194,464,1104,2642,6290 | [0,4,4,0,1,0,-4,-4] | 39 |
| 6 | P | L=2, 16,56,176 | [4,-4,4] | 36 |
| 6 | H | L=0, 8,44,176,752,3200,13568 | [2,-1,40,8,64,-16] | 64 |

Verdict CORRECT for these matrix identities, COMPUTED with exact integer arithmetic. `code/certificates.json` records an independent multiplication replay for all eight certificates. For each dimension D and recurrence degree d I checked at least D consecutive scalar discrepancies after d initial values, which proves the infinite matrix scalar recurrence by Cayley-Hamilton. Polynomial pair matrices are evaluated at the cycle marker q=1 here; this check certifies pair totals, not their whole cycle distribution. No floating root fit enters this result.

For completeness, the exact graph-to-transfer arguments in FAMILIES section 2 are CORRECT as abstract algorithms. Matching-used flags enforce each corner once. Opposite-edge union partitions reject cycles after identifying roots, which is equivalent to three separately rooted trees before identification. The fixed final edge count prevents a discarded component from producing a false tree acceptance. In the pair transfer a connectivity closure counts one component cycle because completed D has degree two. In the HC transfer colours encode the induced subgraphs, union partitions reject monochromatic cycles, and a component disappearing early cannot reconnect. A whole ring must contain both colours, because a monochromatic ring is a cycle. Fixing the first pole's colour removes the colour-swap double count.

I then independently rebuilt all eight stationary transfers in `code/transfer.py`, without importing author code, boundary numbering or transition entries. This closes the graph-to-matrix obligation as well. S,M,P use independently embedded and face-coloured length-six tubes. Black faces are sorted by maximum ring and then sorted vertex tuple. The prefix includes the first two strips; each middle strip is checked equal after translation in the next two strips; the far cap supplies the terminal vector. The algorithm tracks live matching-used bits and the partition of live vertices connected by previously inserted edges. For M it collapses roots, rejects any edge joining an already connected pair, and counts opposite edges. For P it tracks separate bits for both states, joins the two selected corners, and additionally propagates attainable costs zero and one. A vertex is forgotten only at its last incident face, after its matching constraints are met. These rules are precisely the invariant arguments above and define the independent finite matrices retained in `code/rebuilt-transfers.json`.

For H the independent implementation uses actual NetworkX connectivity and path tests on a small graph, replacing each old boundary component by a tree on its boundary vertices. It adds all monochromatic new edges and rejects an edge when its endpoints already have a path. It rejects vanished components, fixes the first pole colour and accepts exactly two components after the far cap. This reconstructs a stationary matrix independent of the author's union-label implementation.

The independent dimensions are again 4,2,2,12 at width four and 15,39,36,64 at width six. Every independent sequence obeys the displayed recurrence for at least D consecutive discrepancies and has the same initial terms. Cayley-Hamilton therefore proves the asserted graph-count recurrence for every length. For P, the independent Boolean cost-zero/one boundary vector repeats at offsets [0,1] and [2,3], respectively, and every tested terminal value on that finite preperiod and period has cost one possible and zero impossible. Thus c_min=1 forever; L=0,1 are directly enumerated. Verdict CORRECT for the all-length formulas, PROVED-HERE with independent finite arithmetic certificates. They remain T2/T3 AI-reviewed results, not externally published theorems.

### F3. Exponential rarity without separators

Exact claim: width four has M_L=2 and S_L=Fib_(2L+3), hence M_L/S_L=2/Fib_(2L+3), exponentially small while c_min=1 and there are no separating triangles.

Verdict CORRECT, PROVED-HERE using the independently reconstructed F2 transfer. The algebra is exact: S_0=2,S_1=5 and S_(L+2)=3S_(L+1)-S_L identify the odd Fibonacci subsequence. Its exponential base per layer is (3+sqrt(5))/2, and N=8(L+1), so the success density decays exponentially in order. This is now supported by an independently reconstructed all-length certificate, not only finite spot checks.

This family differs from the cycle-cover report's T_m. For example width four at dual order 14 has c_min=1; T_4 at that order has c_min=3. The former has bounded degrees 4,6 and exactly two tree matchings; T_m has poles of degree 2m and 2^(m-1) tree matchings. Our finite enumeration finds S(T_m)=2^m-1 for m<=8, giving no observed exponential rarity there. No all-m state-count formula for T_m is claimed by this referee.

### F4. White-face prism chains

Exact claim: the specifically labelled nested q-chain has |T|=5q+3, N=10q+2, S=3^q, P=M=2^q, c_min=q and normalized polynomial

    product_(j=0,...,q-1) (z^(5j+2)-1).

Verdict CORRECT, PROVED-HERE. At a white-face insertion, new black faces and new interior vertices have equal size, and only new faces can cover new vertices. Every new face must therefore take an interior vertex. This proves factorization of states and pairs. Each local prism has a unique cover and two forest orientations. Covers have disjoint vertex supports across pieces, so c=q; local rooted trees attach along their roots without creating a cycle. Alternatively uniqueness of the global cover and fixed-s reversal directly prove every orientation forest. The count gives equality M=2^c_min for every q>=1.

The chosen outgoing triangle is inside the local five-cycle. Each insertion replaces one interior white face by six and increases each enclosing disk's white mass by five. The cycle masses are 2,7,...,5q-3, proving the product, the leading coefficient product(5j+2), and positivity of this normalized polynomial for z>1. These formulas are for the retained original root.

Exact additional claim: for the submitted gluing permutation, H_1=8 and H_q=20*3^(q-2) for q>=2. Verdict CORRECT, PROVED-HERE plus independently verified finite tensor. Restrict an induced-tree partition to either capped side of a separating triangle. An excursion on the other side can be replaced through the separator's monochromatic vertex or edge, proving connected restriction; inducedness and acyclicity are inherited. Conversely compatible restrictions glue along that vertex or edge to trees. Thus the same-label separator edge is a complete three-valued interface, and the local simultaneous-avoidance tensor gives exact multiplication.

I independently enumerated the eight induced-tree partitions of the base prism. Their avoided-dual-edge sets exactly equal all eight submitted sets. Computing the simultaneous-avoidance tensor from these eight sets reproduces every retained step's matrix

    C=[[0,1,1],[1,0,1],[1,1,2]], u=[4,2,2], a=[2,2,4].

Direct multiplication gives Ca^T=3a^T and ua^T=20, establishing the recurrence. The root tensor gives the submitted (4,6,10)*3^(q-2) vector. This is a complete small local certificate, unlike the much larger tube matrices. COMPUTED direct independent replay on the actual retained chain graphs through q=5 gives H=8,20,60,180,540 and all asserted S,P,M,c_min and polynomials. See `code/stack-source.json`.

A control chain with a different explicit gluing permutation, independently generated in `check.py stack`, instead has H=8,24,72,216 through q=4. It has the same state counts and signed-product formula. This is not a refutation of the submitted labelled chain; it confirms that "prism chain" without the permutation is insufficient to specify H. Control data are `code/stacks.json`.

### F5. Bounds on Hamiltonian cycles

Exact fixed-root bounds: for a feasible facial root t and each incident primal edge e,

    H_avoid(e)>=M_t>=2c_t, and H>=3M_t>=6c_t.

Verdict CORRECT, PROVED-HERE conditional on the signed height identity. Recovery is injective for each root prescription: from its Hamiltonian cycle recover the unselected dual set P, delete prescribed e0, orient its three rooted trees towards their roots, and recover s(t) as the tail in each bounded black triangle. Thus the cycle determines s. Each Hamiltonian cycle avoids exactly one edge at that cubic vertex; the three prescription images are disjoint. This justifies factor three without assuming they exhaust all cycles.

Here is an independent argument for M>=2c_t from the moment statement. The signed tree states have M/2 atoms of each sign. Choose a generic linear functional on the finite height vectors, separating all distinct vectors. If p=M/2<c_t, the vanishing moments through degree p give equal first p power sums of the two p-element scalar multisets, including multiplicity. Newton identities give identical multisets. Their signed measure is then zero on distinct height vectors, contradicting the nonzero degree-c_t moment. Thus p>=c_t. This uses the full low-degree moment statement but not the exponential conjecture.

Exact varying-root bounds: H>=3 max_t M_t and H>=(2/N) sum_(uv in E(G)) max(M_u,M_v), assigning zero to unavailable direct-root counts. Verdict CORRECT, PROVED-HERE. The first follows by choosing a root. For the second, either endpoint's recovery supplies the edge-avoidance lower bound, with a global colour exchange if necessary. Every Hamiltonian cycle omits N/2 edges; summing H_avoid over all edges and dividing by N/2 proves the stated normalization. Taking a sum of root recovery counts without this overlap accounting is invalid.

Exact separator bound: with b irreducible pieces, H_avoid(e)>=2^b and H>=3*2^b>=6. Verdict CORRECT, PROVED-HERE conditional on the supplied existence theorem and recovery. Each irreducible piece has a feasible pair at every facial root; signed degree-zero balance plus nonvanishing gives at least two tree matchings. For the prescribed inherited separator pattern choose either of two local recovery cycles. Restriction uniquely recovers these choices, so distinct tuples yield distinct global cycles. This works recursively for any original facial edge. If using larger root-dependent bounds, take each piece's minimum over possible incoming roots, not its maximum.

The cube has six cycles by independent direct enumeration. Even prisms have H=N/2+2, ruling out any universal exponential-in-N lower bound over the whole Barnette class. Neither assertion claims current literature optimality or infinitely many graphs attaining six.

### F6. Literature comparisons

I checked `papers/INDEX.md`. It does not hold local copies of these three counting papers; its entries give primary-source URLs. I opened those sources. These are statement checks, not proof audits of the literature.

LIT, CORRECT: Florek, *Remarks on Barnette's conjecture*, Journal of Combinatorial Optimization 39, 149–155, Theorem 1, assumes a 2-factor made of facial 4-cycles and gives `3^ceil(2|P*|/Delta(P*)^2)` cycles. The published theorem includes the ceiling; the older arXiv v2 statement omits it. Use the published version when quoting the ceiling. Source https://link.springer.com/article/10.1007/s10878-019-00460-8 . This is a subclass result.

LIT, CORRECT AFTER FIX for the precise second Florek attribution: arXiv:2309.09578v2, Proposition 1.4, independently of the later maximum-four-big-neighbours theorem, assumes every dual facial triangle contains both a small and a big vertex. It gives `2^ceil((|B|-2)/(4 Delta(G[B])-7))`, where B is the set of degree-at-least-six vertices of the dual G. In primal terms every vertex meets both a square and a big face. Delta(G[B]) counts a big face's big neighbours, not its whole boundary length. Replacing it by the maximum primal face length gives a valid weaker bound but is not the exact proposition. The report's abstract-based comparison is directionally correct but should quote this full proposition. Source https://arxiv.org/html/2309.09578v2 , Proposition 1.4 and its proof.

LIT, CORRECT: Pivotto–Royle, arXiv:1901.10683v2, introduction and section 2, gives cubic planar cyclically 4-edge-connected four-cycle families and recalls the Smith lower bound three for Hamiltonian cubic graphs. Sections 5–6 develop fixed-width transfer methods. The four-cycle families are not a bipartite counterexample, and do not contradict the six bound here. Source https://arxiv.org/html/1901.10683v2 . No claim of novelty or current globally best bipartite bound follows from these comparisons.

LIT in supplied preprint, CORRECT: OpenAI Corollary 7.1 supplies single-edge avoidance, without a numerical multiplicity or polynomial-time guarantee. The multiplicity above additionally uses signed balance, moments and injectivity.

### F7. Other assertions in the requested files

PROVED-HERE, CORRECT: simultaneous midpoint subdivision has face count multiplied by four, old even degrees unchanged and midpoint degree six; after r octahedral subdivisions |T|=4*4^r+2 and N=8*4^r. It differs from replacing a cubic vertex by a six-cycle with only three attachments, which leaves three degree-two vertices. The latter proposed literal operation is REFUTED as a cubic construction.

COMPUTED only: numerical subdivision counts, larger tube root sweeps and decimal growth rates were not independently replayed here. A dominant-root decimal is not an exact asymptotic certificate; one must establish that the dominant mode is present in vT^Lw. The retained nonnegative matrices permit that analysis, but it was not redone in this review. The conjecture tests correctly label the general exponential bound and strictness as open. Their "unbounded c_min without separators remains open here" records that earlier report's scope; the later cycle-cover family resolves it and must update any global open-problem list.

## Obligation graph and dependency table

F1 <- forced state list AND direct prism cycle classification. F2 graph counts <- transfer bijections AND correct saved transitions AND correct initial/cap vectors; F2 matrix recurrence <- integer products AND Cayley-Hamilton. F3 <- F2 AND Fibonacci algebra. F4 <- insertion factorization AND disk increments; its H formula <- gluing bijection AND eight-cycle tensor. F5 <- moments AND recovery injectivity AND disjoint prescriptions; separator version <- local existence AND recoverable gluing. F6 <- exact source hypotheses AND matching notation.

| ID | Exact obligation | Needed by | Route / edge | Classification | Support | Status |
|---|---|---|---|---|---|---|
| O1 | Prism state list and HC cases exhaustive | F1 | direct classification / AND | algebraic/logical step | proof above, finite replay | discharged |
| O2 | Tube local rules count intended objects | F2 | frontier / AND | algebraic/logical step | explicit invariant arguments | discharged |
| O3 | A finite stationary transfer implements all local rules | F2,F3 | encoding / AND | side condition | independent transfer.py reconstruction | discharged |
| O4 | D recurrence discrepancies vanish for each D-dimensional matrix | F2 | certificate / AND | algebraic/logical step | independent exact multiplication | discharged |
| O5 | D discrepancies imply all future ones | F2 | recurrence / AND | named theorem | Cayley-Hamilton, square finite matrix | discharged |
| O6 | Boolean low-cost repetition proves all-L c_min | F2 | cost transfer / AND | side condition | independently rebuilt cost transfer and exact repeats | discharged |
| O7 | Insertion forces local states and disjoint cycles | F4 | decomposition / AND | algebraic/logical step | balanced new faces and vertices | discharged |
| O8 | Eight local HC sets and simultaneous counts are exhaustive | F4 | tensor / AND | algebraic/logical step | independent induced-tree enumeration | discharged |
| O9 | Recovery has inverse on its image | F1,F5 | injection / AND | algebraic/logical step | recover s from rooted P-e0 | discharged |
| O10 | Low moments force M>=2c_min | F5 | moments / AND | algebraic/logical step | Newton identities above | discharged |
| O11 | Every piece supplies two choices for every incoming root | F5 | recursion / AND | named theorem | supplied existence and sign balance | discharged |
| O12 | Literature hypotheses and exponents copied exactly | F6 | source check / AND | named theorem | opened primary sources, correction above | discharged after fix |

## Verdict

FOLLOWS for prisms, the all-length width-four and width-six graph-count recurrences, separator-free exponential rarity, the labelled prism-chain state and polynomial formulas, its Hamiltonian tensor, and the derived lower bounds with the stated source inputs. O3 and O6 are discharged by the independently rebuilt transfers. The second Florek comparison needs the precise hypothesis and degree-parameter fix above. Larger direct census ranges, decimal asymptotics and subdivision tables remain outside the independently replayed range.
