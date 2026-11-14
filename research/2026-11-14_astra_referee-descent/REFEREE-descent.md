# Descent referee

## Audit boundary

This audit concerns Fable's DESCENT.md, PROOFS.md A-F, and COMPLEXITY.md, including Proposition G. The source manifest records the files read; the shared tree already contained changes in that folder. I use good state, good pair, cover, and m as in the glossary. Write q for the number called k in the descent code, c for the number of cover cycles, and n=V-3. V is the order of the dual triangulation, not the primal cubic graph.

Accepted inputs are the definitions, elementary finite graph theory, the supplied OpenAI paper's Lemmas 4.1 and 5.3 and Proposition 5.1, and the integer normalization and marked involutions in the supplied trees paper, Lemma 5.1 and Theorem 5.3. This is not a new audit of those entire papers. Their presence in this repository is not evidence of peer review.

## Exact conjecture and logical dependencies

CONJECTURE C3. For every rooted simple Eulerian sphere triangulation and every pair p, there is a finite sequence p=p0,...,pt with pt good, each adjacent pair related by reversing one D-cycle or one Q-cycle, and q(p[i+1])<=q(p[i]). Empty pair sets impose no condition. Test by constructing the complete exchange graph and reverse-searching from all good pairs along nondecreasing-q edges.

The supplied route is

    C3 <- AND: every positive-level plateau has an exit to a lower level.
    plateau exit <- missing general argument.
    equivalent sublevel formulation <- finite plateau argument in Proposition C.
    whole-component existence <- signed cancellation, accepted background.

PROVED-HERE audit. Proposition C is CORRECT. A closed plateau is a union of components of the q-sublevel graph. Conversely, the component at exactly q=j reachable from a nongood pair must have a lower exit if no closed plateau exists. Repeating decreases the nonnegative integer j. The whole-component theorem alone supplies no such exit. Grouping an incomplete orientation cube cannot use the product formula for its whole cube. Thus C3 remains a conjecture, even if every finite run succeeds.

COMPUTED. code/check.py is independent of both reports and barnette_lab. It reconstructs faces from directed edge walks, colors their dual graph, enumerates incidence bijections, generates both exchange moves, and reverse-searches the exchange graph. It checks reciprocity and membership of every generated edge. code/census_6_16.json gives all roots of all plantri Eulerian triangulations through V=16, including the empty V=7 census. The totals are 24,744 pairs, 24,090 good pairs and 5,088 roots with a pair. There are exactly two nongood local optima for strict descent, both at V=16. Hence the least-order assertion for strict descent is independently confirmed. The census is of embedded rooted inputs, without quotienting root automorphisms.

COMPUTED. The extended independent replay covers all 3,373,400 pairs through V=20, with 3,168,818 good pairs, 411,031 roots admitting pairs, 3,289 nongood local optima for strict descent, and no escape radius above two. It also checks all 335,704 pairs of the 40-graph V=40 batch at all 3,040 roots, matching the source totals. The full 49,325,864-pair V<=22 range and full 9,970,784-pair random range remain author-reported computations, not ranges independently replayed here. A smaller independent replay validates core mechanics but does not make the larger run a same-size independent check. The V=23 files were outside the requested range and were still changing during this session.

## Saved witnesses and bounded variants

COMPUTED. code/witnesses.py verifies the saved facewise pairs and searches unrestricted exchange balls. Its output is code/witnesses.json. The V=16,21,60 examples have q-escape radii 2,3,4 respectively. This confirms refutations of lookahead 1,2,3. Minimality of V=21 is now independently established: code/c3_6_19.json and code/c3_20_20.json check every pair through V=20 and find no radius above two. The saved V=40 RHO line has radius 3, exactly as its header now says; it is not a certificate for failure of lookahead 3. The random summary reports a different V=40 pair with radius 4, but provides no complete such pair in witnesses.txt. The independent recovery below now supplies the missing certificate. The last two saved lines, for the size/area potentials at V=40 and V=50, are truncated before the complete graph and pair. They are not certificates as saved. The independent recovery below supplies complete V=40 replacements.

REFUTED, CORRECT AFTER FIX. The finite list of tested rules fails in the reported ranges. This does not mean every bounded variant fails: lookahead four is explicitly open in DESCENT.md. No unbounded-radius theorem follows from observed radii 2,3,4. Likewise, neither a bounded local rotation's failure nor a small collection of potentials refutes all bounded local algorithms.

PROVED-HERE audit of Proposition E. Parity c=n mod 2 follows because every D-cycle has odd length, by the disk identity. D-swaps fix c. Q-reversals change it by an even integer. At the V=16 witness, the two orientations of its one-cycle cover are nongood, and any exit from that cover increases c to three. Therefore a path that never increases c cannot repair that pair. This does not refute every potential that depends on c, or every potential nondecreasing in c with other data fixed. A constant potential is nondecreasing in c and allows all exchanges. A tie-break term can distinguish the two c=1 pairs. Replace the universal potential assertion by the path restriction just stated or by explicitly named potentials. Verdict WRONG as universally worded, CORRECT AFTER FIX for the intended restriction.

PROVED-HERE counterexample to the unrestricted phrase 'every c-dependent potential.' Let d(p) be exchange-graph distance to the set of good pairs in p's component. The accepted component existence theorem makes d finite. The lexicographic potential (d(p),c(p)) depends on c, yet every nongood pair has a neighbor decreasing d by one and hence decreasing this potential. This argument makes no claim that d is polynomial-time computable. It isolates the missing computational or structural restriction in the universal assertion.

## Recovered certificates and individual potential verdicts

COMPUTED, CORRECT AFTER FIX to the certificate archive. Regenerating the raw skew V=40, count=40, seed=15 inputs and using the new cover enumerator located the radius-four pair at graph 3, root {10,16,11}. code/recovered40_0_40.json preserves its rotation, face-indexed pair and radius. The saved graph-37 witness has radius three and should not be substituted for it. Graph 21, root {6,30,31}, supplies complete weak-descent traps for vq, wq, (q,vq), (q,wq), all independently checked and saved in the same file. The author generator supplies only raw triangulations; both enumeration and verification are this referee's code.

COMPUTED. code/all_potentials.json checks complete smallest saved witnesses for the nine c-bearing potentials, eight signed three-entry height potentials, both signed (q,psi) rules, and both wq+wd rules. code/potentials.json checks the (q,-om) weak trap and two-move macro trap at V=40; reflection gives the opposite sign. code/signed_radii.json checks the two saved V=60 signed radii, three for (q,+psi,-om) and four for (q,+om,+psi). Reflection flips both height signs, not just one. Together with the four recovered size/area rules this independently confirms weak-descent failure for all 27 named alternatives. SINK-only lines are not counted as weak-descent refutations.

| Rules, exact comparisons | Smallest supplied weak trap | Verdict | Independent evidence |
| --- | --- | --- | --- |
| q+c; (c,q), (c,wq), (c,vq), (c,q,wq) | 16, also two-move macros | CORRECT | all_potentials.json |
| (q,c), (q,c,wq), (q,c,+psi), (q,c,-psi) | 16, single moves | CORRECT | all_potentials.json |
| (q,+psi), (q,-psi) | 18 | CORRECT | all_potentials.json |
| (q,+om), (q,-om) | 40 | CORRECT | potentials.json and reflection |
| (q,sign*psi,sign*om) and reversed order, equal signs | 16 | CORRECT | all_potentials.json |
| same two orders, opposite signs | 18 | CORRECT | all_potentials.json |
| wq+wd; (q,wq+wd) | 18 | CORRECT | all_potentials.json |
| vq,wq,(q,vq),(q,wq) | 40 | CORRECT AFTER FIX | recovered40 certificates replace truncated lines |

COMPUTED. code/height_minimality.json checks all pairs through V=17. Equal-sign plateau-free potentials first fail at V=16; opposite-sign versions have no nongood local optimum for strict descent through 17 and the saved V=18 witnesses establish their least order. Orders in the remaining table rows are least independently replayed witnesses unless a separate exhaustive smaller-order check is stated. In particular V=40 is not a minimum-order theorem. COMPUTED. code/recover50.py subsequently regenerated skew/50/12/6 graph 11 at root {5,15,14}. code/recovered50.json supplies complete replacements and confirms two trapped pairs for each of the four size/area potentials even with radius-two macros.

COMPUTED. code/macro40.json supplies radius-two local-optimum certificates for all eight signed three-entry height potentials at V=40. Seven were found directly in the regenerated batch; reflecting the embedding of the (q,-psi,-om) certificate supplies (q,+psi,+om). code/finalize_macro.py independently verifies every resulting radius-two ball, including the reflected certificate. These are strict-improvement obstructions; they are not automatically weak-descent traps. The V=60 signed radius-four certificate refutes lookahead three for its named potential and, by reflection, the potential with both signs reversed. It does not by itself establish that statement for all eight potentials.

COMPUTED. A separate independent insertion sample rejects every split that creates a separating triangle. code/random_separator_free.json contains 20 new graphs, five each at V=26,30,34,40, with eight randomly selected roots per graph. All 1,160 pairs pass C3, of which 1,008 are good. No strict-descent obstruction occurs in this sample. Its degree-four insertion distribution is biased; this is additional stress testing, not a uniform large-order census.

## Structural proof ledger

PROVED-HERE audit, Lemma A, CORRECT. A(a): orient each opposite edge from its r-corner; every nonroot has one outgoing edge and roots have none. On an undirected cycle all tails must be distinct, so the cycle is directed. A(b): after swapping on C, the supplying face at x is the old face at sigma^{-1}(x), yielding f'(x)=f(sigma^{-1}(x)). Outside C the supplier is unchanged. A(c): every old cycle meeting C loses an edge. That edge cannot be supplied by another black face because black faces own disjoint edge sets. An old cycle avoiding C survives. Any genuinely new cycle must meet C, since outgoing edges outside C have not changed. This proves the count formula. 'Destroys exactly' refers to old edge cycles, not merely their vertex sets or to a guaranteed decrease in q. Corollaries A1 and A2 follow immediately.

PROVED-HERE audit, Lemma B, CORRECT with its stated normalized weights. B(a): the three selected corners partition the three incidences of each face, so their weight sum is constant. B(b): the change of w_s is minus the old directed spoke circulation; w_r changes oppositely and w_u stays fixed. The slide is simple because it uses each black face once, and the subdisk avoids the third corner even if that corner lies elsewhere on the curve. B(c): exchange r and u along the Q-cycle and repeat the same argument. B(d): these cycles avoid roots. A white face adjacent to t0 cannot be enclosed, since its root vertices lie on the unbounded side. Thus the bounded spoke faces enclosed are exactly the white triangles enclosed. The disk identity gives W=B+1>=1. The bound is n times 6n. Corollary B1 uses at most n/3 disjoint Q-cycles and two integer heights in [0,6n^2]; its O(n^5) bound is correct. No direction toward a good pair follows from strictness of a height change.

PROVED-HERE audit, Proposition D, CORRECT AFTER FIX for the nonvacuous statement. Specify that both pieces admit pairs. The inner nonroots occur only in the inner bounded black faces; equal cardinalities force these faces to match exactly those vertices. This proves state and pair products. The functional graph cannot leave the outer piece after entering it, so no directed Q-cycle crosses pieces. D-cycles are disjoint across the pieces. Therefore exchanges form the Cartesian product, and q and c add. C3 passes to the product; conversely freeze the other coordinate in the component of a good pair at level zero. The accepted existence theorem supplies that good pair. For escape radius, the first decrease of the total implies some coordinate has fallen below its initial value. Project the path to that coordinate. The reverse inequality is attained by a worst coordinate paired with a good state in the other factor. An all-good factor has radius zero. Without the nonempty-pair hypothesis the 'iff' can be vacuous on an empty product.

PROVED-HERE audit, Proposition F, CORRECT AFTER FIX in a minor bound. A degree bound d<=2n/3 gives at most 1+d+...+d^L vertices in a ball, not literally d^L including the center. For fixed L the polynomial conclusion is unchanged. Each successful round lowers q by at least one; at most n/3 rounds are needed. The analogous height bound is O(n^5). A procedure may stop when it first reaches a good pair.

## Complexity audit

The proposed exposition paragraph is not safe to quote unchanged. Its claim about every instance tried also needs to exclude the three V=300 searches stopped at a cap in the source report; an unfinished search is neither success nor a counterexample.

PROVED-HERE, CORRECT. Conditional on the supplied existence theorem, the totalized BARNETTE-HC relation is polynomially balanced and verifiable, including rejection of invalid inputs. Hence it is in TFNP. TREE-PAIR should likewise return an invalid-input certificate or use an explicit promise when the supplied triangulation or pair is invalid.

LIT input, CORRECT as an attribution. The trees paper gives deterministic O(poly(N) 3^(N/4)) time and polynomial space by matching enumeration, and 2^O(N log N) time and polynomial space for its marked walk. Calling both 'exhaustive' obscures the difference between enumeration and a walk. These upper bounds give no lower bound or evidence against a polynomial algorithm. 'No hardness result is known' is a broad literature claim that this review has not certified. Use 'these arguments establish no hardness result.' NP-hardness of a total search task must name the search reduction notion. The defensible standard statement concerns FNP-hardness under polynomial search reductions and the consequence NP=coNP, not an unspecified decision reduction to a search oracle.

PROVED-HERE, Proposition G is CORRECT, conditional on the marked involutions. At level h with h=n mod 2, set sigma_h=(-1)^((n-h)/2), direct beta from sigma_h to -sigma_h and alpha back. The two sink types in the original text are correct for nonisolated level vertices. An alpha-fixed sink of sign -sigma_h has c<=h-2, by c<=h and c=h+2 mod 4. All these calculations check.

The restart sentence needs its implicit justification made explicit. An arbitrary normalization can change Q_s, but this restart is applied only to an alpha-fixed K2 endpoint. By the marked involution's fixed-point rule, every D-cycle there is already counterclockwise. Hence start(x) changes only the token list and leaves the underlying pair unchanged. Since x is not beta-fixed, the target is a genuine source, as claimed. An earlier referee checkpoint suspected a gap here; this additional premise resolves it. No new good-sink case is needed for the actual construction.

Complete encoding details, PROVED-HERE. Use levels 1<=h<=floor(n/3) of parity n. A history lists prior levels of that parity in strictly decreasing order, with valid marked K2 vertices; allow arbitrary such lists, not only histories whose reachability has been established. The endpoint of a restart contains the entire previous marked vertex and history. Its predecessor is computed by checking the last entry and equality to its canonical restart. Distinct restart sources cannot collide. There are at most floor(n/6) earlier levels, and each marked vertex has O(n log n) bits. Invalid encodings receive self-loops and create no imbalance. Every non-good K2 vertex can append its level, since at least two cycles disappear and c>=1. Every level edge and restart edge has a polynomial-time predecessor and successor. A nongood normalized input is a known source; a good one is returned immediately. This is a valid sink reduction. The encoding details complete routine domain obligations omitted from the supplied sketch.

PROVED-HERE. PPADS is contained in PPP directly: on a valid degree-one directed graph let F(v) be its successor if present and v otherwise. A collision consists of a predecessor and a sink. A preimage of the known source can only be an isolated source, excluded by the required outgoing edge. Thus the usual collision-or-target PIGEON task yields a sink. The directed path argument does not establish PPAD or PPA membership, because their answer may be a different, useless source or leaf. Failure of that reduction is not a separation from those classes.

For the full graph, polynomially many pair-search calls suffice after decomposition and flow. Buss and Johnson's 2012 paper supplies closure of PPADS under polynomial-time Turing reductions. I checked Corollary 6.2 in the indexed text of the author's July 6, 2011 PDF: it identifies the many-one and Turing closures for the complete problems and explicitly includes PPADS. Direct PDF retrieval failed, so this is a check of the stated corollary rather than a new line-by-line audit of its proof. The input decomposition and reconstruction are in OpenAI sections 3, 6, 7. Primary author PDF: https://www.math.ucsd.edu/~sbuss/ResearchWeb/NPSearch/NPSearch.pdf .

PROVED-HERE, PLS claims CORRECT AFTER FIX. A PLS formulation needs a polynomial-time initial feasible solution, polynomial-time cost computation with polynomial-size integer representation, and a polynomial-time improvement oracle. For fixed L the exchange ball can be enumerated in polynomial time, so these conditions hold for the explicitly computable potentials in the report, starting from the supplied pair. They do not hold for an arbitrary unspecified Phi. Good local optima are equivalent to every nongood pair having a strictly lower point in that ball. C3 alone allows plateaus and does not establish this property. Polynomially many cost values imply polynomially many strict improvements. Exponentially many values are not logically required for any 'meaningful' PLS statement; they are only necessary if this counting argument is not already to yield a polynomial algorithm.

LIT source check: Li, Pires and Robere, Intersection Classes in TFNP and Proof Complexity, ITCS 2024, section 1, confirms the standard PPAD, PPADS, PPA, PPP and PLS framework and PPAD's inclusions. Its printed parenthetical for negative imbalance contains a reversed inequality; the sink convention here is indegree greater than outdegree. Source: https://drops.dagstuhl.de/storage/00lipics/lipics-vol287-itcs2024/LIPIcs.ITCS.2024.74/LIPIcs.ITCS.2024.74.pdf . Closure source: https://www.sciencedirect.com/science/article/pii/S0168007212000346 .

LIT source check, CORRECT. Akiyama, Nishizeki and Saito, NP-Completeness of the Hamiltonian Cycle Problem for Bipartite Graphs, Journal of Information Processing 3(2), 1980, pages 73-76, explicitly treats 2-connected cubic bipartite planar graphs. The primary scan is https://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J029.pdf . The report's mathematical attribution is correct. Saying 3-connectivity is "exactly" what makes the problem total is an informal comparison within this fixed nested pair of graph classes, not a characterization of every individual Hamiltonian graph.

LIT source check. Megiddo and Papadimitriou, On total functions, existence theorems and computational complexity, Theoretical Computer Science 81, 1991, pages 317-324, section 1 defines polynomial balance, polynomial verification and totality; section 1.2 gives the local-search conditions, and Theorem 2.1 states the FNP-completeness obstruction with its reduction definition in section 2. The primary PDF was opened and these statements checked: https://theory.stanford.edu/~megiddo/pdf/papadimX.pdf . The Akiyama primary scan was available in indexed text, but direct opening timed out.

## Dependency table

| ID | Exact obligation | Needed by | Route | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | C3 for every pair | root | plateau induction | root | C1,C2 | open |
| C1 | each positive plateau has a lower exit | C0 | AND | missing | finite tests only | open |
| C2 | repeated lower exits terminate at zero | C0 | AND | algebraic/logical step | integer q | discharged |
| A0 | old Q-cycle survives iff it avoids swapped C | structural claim | function model | major claim | A1,A2 | discharged |
| A1 | swap precomposes f on C with sigma inverse | A0 | AND | definition | face supplier calculation | discharged |
| A2 | removed edge cannot reappear from another face | A0 | AND | side condition | unique black owner | discharged |
| B0 | height changes have magnitude W>=1 | structural claim | circulation | major claim | B1,B2 | discharged |
| B1 | simple spoke slide preserves enclosed white faces | B0 | AND | proved earlier | OpenAI 5.3, checked applicability | discharged |
| B2 | W=B+1 | B0 | AND | named theorem | OpenAI Lemma 4.1 for r-directed cycles | discharged |
| D0 | product equivalence for C3 | structural claim | coordinate projection | major claim | D1,D2 | discharged after fix |
| D1 | states and moves factor | D0 | AND | algebraic/logical step | saturation and functional graph | discharged |
| D2 | both factors admit pairs and hence good pairs | D0 | AND | side condition | added nonvacuity, accepted existence theorem | discharged after fix |
| G0 | TREE-PAIR in PPADS | complexity claim | merged sink graph | major claim | G1,G2,G3 | discharged |
| G1 | unsuccessful level sink decreases c by two | G0 | AND | proved earlier | marked fixed-point sign formula | discharged |
| G2 | K2 restart preserves the pair and is not good | G0 | AND | proved earlier | alpha-fixed endpoints already have all cycles counterclockwise | discharged |
| G3 | restart source has unique predecessor | G0 | AND | algebraic/logical step | history encoding above | discharged |
| L0 | fixed-radius local search solves good-pair search | conditional claim | strict descent | major claim | L1,L2 | open |
| L1 | polynomial cost and improvement oracle | L0 | AND | side condition | finite ball, explicit potentials | discharged |
| L2 | all local optima are good | L0 | AND | hypothesis | refuted for listed candidates | failing for those candidates |

## Verdict

C3 finite survival: CORRECT in the independently verified ranges above; GAP as an unbounded theorem. Lemmas A, B and Proposition C: CORRECT. Product and complexity formulations: CORRECT AFTER FIX. Universal claims about all bounded rules or all c-dependent potentials: WRONG. The V=40 radius-four and single-move size/area claims: CORRECT AFTER FIX to their certificate archive. The selected V=50 two-move size/area line was also replaced by independently verified complete certificates. The PPADS route closes, conditional on the marked-involution theorem, with the alpha-fixed restart observation and explicit encoding above.
