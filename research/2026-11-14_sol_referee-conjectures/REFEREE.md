# Independent referee of the conjecture report

Referee: gpt-6.1-sol, 14 November 2026. Folder ownership and git scope follow `research/BRIEF.md`. No author verification code was imported or executed. The sole use of the author's generator was to recover the input of the saved V=70 statistical witness. All subsequent enumeration and verification used new code in this folder. Plantri supplied exhaustive input graphs.

## Audit boundary

The submitted sources are `research/2026-11-14_opus_conjectures/{REPORT,CONJECTURES,PROOFS,PREDICTIONS}.md`, their data and code documentation. The alpha-orientation definition is from the graph-theory PROOFS.md, section 3, with the corrections in the structure referee's report. The exact claim is about the full difference-potential lattice, not greedy single-hexagon terminals. The domain is finite simple Eulerian sphere triangulations with a chosen black outer triangle and at least one pair.

Accepted inputs are the state and pair definitions, elementary graph and plane-cycle facts, integer circulation as a sum of facial boundaries, and the disk identity from the supplied OpenAI manuscript, Lemma 4.1. I read its text extraction and the relevant section 5 formulas. The height and polynomial reformulations are from the two referee files named in the task. Their nonvanishing argument is written out again in LATTICE-READING.md, rather than accepted as an unexplained theorem. No claim is made to audit the rest of the Hamiltonicity proof here.

`LIT` below records a statement in the supplied manuscript, without asserting its publication or peer-review status. `PROVED-HERE` records a written argument in this folder or the independently checked submitted argument. `COMPUTED` always means a specified finite check. The mathematical tier of an AI-refereed proof remains T2, human check pending. Newly discovered generalizations in this folder have not received an outside referee.

## Claims and verdicts

| Claim | Verdict | Status and exact scope |
|---|---|---|
| (a) C2 is false; the V=18 saved graph has the claimed four-element lattice | CORRECT | `COMPUTED`, complete independent brute force of all states and pairs, all four factors and their order; 4-connectivity checked. Independent exhaustive minimum-order check through V=18. |
| (b) Seven of nine saved greedy witnesses are not true extrema | CORRECT | `COMPUTED`, all nine checked by new shortest-path code; all are local terminals in their claimed direction. |
| (c) Difference constraints and two shortest paths give the exact extremes | CORRECT | `PROVED-HERE`, the submitted proof closes, with the connectedness clarification below. Independent all-root comparison against complete factor enumeration through V=18. |
| (d) The directed-cycle criterion | CORRECT | `PROVED-HERE`, independent proof in LATTICE-READING.md, section 2. `COMPUTED` on every pair at every rooted instance through V=18, stronger than the requested V=14. |
| (e) One 2-factor implies #TM=2^c_min | CORRECT | `PROVED-HERE`, cycle reversal and unique-mate proof below. The converse remains `CONJECTURE`, independently `COMPUTED` through V=22. |
| (f) Theorem B's moment identities alone cannot prove C1 | CORRECT AFTER FIX | `PROVED-HERE` for vanishing below degree m plus nonvanishing at degree m. `GAP` for the stronger reading that includes all prescribed values N(w); the examples do not settle that. |
| (g1) R1, R3 and R5 failures at V=24,60,70 | CORRECT | `COMPUTED`, independently reproduced all three particular examples, including V=70. The quoted sizes for R3 and R5 are not minimal: the new V=33 gluing refutes both. |
| (g2) R2 holds universally | WRONG | `REFUTED`, explicit V=33 graph, L=B_4, all ten distinct extrema/irreducible candidates fail. Two new implementations agree. |
| (g3) The reported finite R2 tests passed | CORRECT as finite evidence, with range qualification | Source logs say no failures through V=24 and random up to V=250. I independently checked all roots through V=14, named witnesses and 24 family instances. I did not repeat the complete V=19..24 lattice census or the full random campaign. A V=33 counterexample does not contradict the finite V<=24 claim. |
| (h1) C1 has no violation through V=22 | CORRECT | `COMPUTED`, independent complete C++ replay on all 243,547 input triangulations, 9,531,638 roots and 4,656,948 feasible rooted instances. |
| (h2) C3 survived the stated random tests | CORRECT as finite evidence, not a theorem | The saved log has 940 starts and no failures. `COMPUTED` independently on all 24,744 ordered pairs through V=16, plus all pairs of the two saved plateau traps. The full 940-start campaign was not rerun. |

## The V=18 certificate

`COMPUTED`. `code/independent.py` reads ONLY the graph rotation and root from the author's JSON. It reconstructs the faces, colouring, incidence data and spoke embedding. It enumerates all 54 states as bijections and tests every ordered pair of states for disjointness. This gives exactly 20 pairs. An independently formulated capacity-assignment enumeration of u gives the same four factors, and their cycle decompositions give exactly the same 20 pairs. A union-find Q-forest test agrees with a topological-sort test of the criterion on every pair.

`COMPUTED`. The reference factor in our certificate is the maximum. Only H0 faces 4 and 8 have nonzero potential ranges. In this coordinate system the full lattice is

| Element ID | phi(4), phi(8) | Rank | D-cycle lengths | Ordered pairs | Tree pairs |
|---:|---|---:|---|---:|---:|
| 3 | -1,-1 | 0 | 15 | 2 | 0 |
| 1 | 0,-1 | 1 | 3,5,7 | 8 | 6 |
| 2 | -1,0 | 1 | 3,5,7 | 8 | 6 |
| 0 | 0,0 | 2 | 15 | 2 | 0 |

The complete u-vectors and all r,s pairs are in `data/v18.json`. There are 12 distinct tree states. Every vertex-deletion set of size at most three leaves the graph connected. `code/anatomy.py` enumerates every simple directed cycle of each extreme O_u, finding exactly two facial hexagons in each. One blocks each of its two D-directions. The data are in `data/v18_directed_cycles.json`.

`COMPUTED`. `code/census.py 18` independently generates all Eulerian triangulations through V=18 using plantri. It tries every face as root, brute-enumerates states and all ordered pairs, compares with every factor decomposition, computes both shortest-path extrema and tests them. It finds no C2 failure below V=18 and 26 rooted failures at V=18. Thus the submitted minimum order is independently verified relative to the plantri class enumeration, not inferred from the single saved instance.

## Proof audits

### Difference constraints

`PROVED-HERE`, independent check of submitted Lemma 1. The graph H0 is connected. A useful direct justification is that each triangulation edge except those of t0 routes through its black centre. Each edge of t0 can instead be replaced by the other two sides of the white triangle across it; its third vertex is not a root, and these two sides are not edges of t0. Hence deleting t0's three edges preserves connectivity, and all remaining triangulation paths route in H0.

For a reference orientation O0, the reversed spokes of another fixed-outdegree orientation, directed in their new direction, have zero divergence. They form an integer circulation c. In a connected plane graph, c is the sum of clockwise facial boundaries with unique coefficients phi after setting the outer coefficient to zero. On a reference-directed edge e this is

    c(e)=phi(R(e))-phi(L(e)) in {-1,0}.

Conversely such coefficients define a reversal set with zero divergence, preserving outdegrees. A bridge has equal left and right face and cannot be reversed. Thus the claimed bijection has no hidden bridge exception.

Rewrite each constraint as the two arcs L->R of weight 0 and R->L of weight 1. They form a strongly connected constraint digraph. All solutions satisfy phi(f)<=dist(O,f) and phi(f)>=-dist(f,O). The upper and lower distance bounds themselves satisfy every constraint and outer normalization, proving the formulas for both extrema. Pointwise min and max preserve every difference upper bound, proving distributivity. Reversing a simple clockwise directed cycle subtracts the disk indicator, so the least orientation has no such cycle; the counterclockwise statement is dual. These assertions use the sign convention stated by Opus, not the earlier mirrored labels.

`COMPUTED`. Every shortest-path extreme agrees with the componentwise extreme of the completely enumerated factors at every feasible root through V=18. `code/witnesses.py greedy` checks the nine older stored orientations. The true maximum is `alpha_max_fail_120_123.json`; the true minimum is `ef_fail_40_40.json`; the other seven equal neither extreme. Their empty single-face move lists in the claimed direction confirm local terminality. Full details are in `data/greedy.json`.

### Criterion and the unique-factor argument

`PROVED-HERE`. LATTICE-READING.md, section 2, supplies the complete indegree proof of the criterion, including why a forest has one root per component. No assumption about dangerous facial cycles alone is used. Directed cycles of arbitrary length are covered.

`PROVED-HERE`, independent closure of submitted Lemma 3. Suppose u is the sole factor and some pair r,s has a Q_s cycle. Reverse that cycle by exchanging r(t) and u(t) on its supplying faces. This preserves the state s and changes the factor, a contradiction. Thus every one of the 2^c decompositions of u is a tree pair. A forest Q_s with one root per component has exactly one orientation toward the roots with outdegree one at each nonroot, determining its partner r. Hence no two tree pairs have the same second state. Therefore #TM=2^c, and c=c_min. The converse does not follow from this proof.

### Moment barrier, exact repair

`PROVED-HERE`. For m=3 use positive atoms at 0,4,5 and negative atoms at 1,2,6. Their moments of degrees 0,1,2 are respectively 3,9,41 on both sides, while degree 3 gives 189 and 225. For m=4 use 0,4,7,11 against 1,2,9,10. The common moments through degree 3 are 4,22,186,1738, while degree 4 gives 17298 and 16578. `code/anatomy.py` also checks this exact integer arithmetic.

Embed the points as x*(1,...,1) in a height space of dimension at least m. Every polynomial of total degree below m restricts to a polynomial in x of degree below m. All such signed moments vanish. A product of m coordinate heights gives the nonzero degree-m moment. Both measures have unit signed masses and fewer than 2^m distinct integer atoms.

The repaired conclusion is that LOW-DEGREE VANISHING PLUS EXISTENCE OF ONE NONZERO DEGREE-m MOMENT cannot force 2^m atoms. If the phrase "Theorem B's identities" includes the full family of prescribed nonnegative minimal-cover counts N(w), these examples have not been shown to satisfy that family. Nor were they realized as actual tree-state height configurations. The stronger impossibility statement remains a gap. This agrees with the qualification at the end of the submitted Proposition 4, and that qualification must also appear in its headline claim.

## Larger witnesses and the replacement conjecture

`COMPUTED`. `code/witnesses.py stored r1` reconstructs the saved V=24 lattice with 20 elements. Its nearest successful element has cover-distance two from either extreme. `stored r3` reconstructs the saved V=60 lattice with 24 elements and a tree-free maximal chain of seven elements. Both witnesses have successful irreducibles, as reported.

`COMPUTED`. For V=70, I recovered graph number 24 from the documented generator seed 52 and chose face 80, whose roots are {18,20,21}. Generation alone used the author's `gen.py`; no author enumeration output was consumed. Complete new enumeration yields

    lattice elements   1410
    successful elements 654, fraction 109/235 < 1/2
    ordered pairs      483960
    tree pairs         71180.

These are exactly the previously singly checked counts. Input and result are saved in `data/r5_input.json` and `data/r5.json`.

`CONJECTURE`, precise submitted R2. For every feasible rooted instance, at least one of bottom, top, a join-irreducible or a meet-irreducible u carries a pair r,s with Q_s a rooted forest. Join-irreducible excludes bottom and means exactly one lower cover; meet-irreducible excludes top and means exactly one upper cover. Extrema are explicitly included, so the statement also covers a singleton lattice.

`REFUTED`. The V=33 rigid-face gluing has lattice B_4. Exactly four elements succeed. Every success has one selected coordinate in each of two designated coordinate pairs. None is bottom, top, an atom or a coatom. In B_4 the atoms are all join-irreducibles and the coatoms all meet-irreducibles. Thus all ten distinct R2 candidates fail. All details, the independent second certificate, a product-order proof, and the recursively glued all-q family are in LATTICE-READING.md, section 6. This is a valid simple Eulerian sphere triangulation, with a white-inner separating triangle; it does not refute a NEW restriction of R2 to triangulations without separating triangles.

`COMPUTED`. Family tests independently reconstructed the nanotube adjacency rule rather than importing the counting-family scripts. Width 4 lengths 0..6, width 6 lengths 0..4 and width 8 lengths 0..3 all pass R2 at the specified lateral root. Five prism sums pass and each has a singleton lattice. Witness sums q=2,3 fail R2, with orders 33,48, lattices 16,64 and tree-pair counts 144,1728. These 24 rooted family cases are not a uniform random sample and are not claimed to exhaust those families.

`PROVED-HERE` conditional on the finite base certificate. Repeated rigid-face witness sums give successful fraction 2^-q and distance q from either extreme. They also have tree-free maximal chains for every q>=2. Thus R3 and R5 already fail at V=33, and the idea of replacing R1 by any fixed cover-distance bound fails in this general class. No minimum-order assertion is made for the new R2 counterexample.

## C1 and C3 finite evidence

`COMPUTED`. The independent C++ program `code/count.cpp` has no lattice-search code and no author source. It enumerates all deleted-corner assignments with degree capacities, decomposes each into all cycle directions, and directly tests Q_s for a cycle. Its totals agree with the independent Python all-state brute force on their entire overlapping range through V=18. The complete C++ run through V=22 has:

| Quantity | Total |
|---|---:|
| Unrooted plantri inputs | 243,547 |
| All facial roots | 9,531,638 |
| Feasible rooted instances | 4,656,948 |
| Factors, with rooted multiplicity | 6,436,022 |
| Ordered pairs | 49,325,864 |
| Tree pairs = tree states | 45,375,214 |
| Equality cases in C1 | 3,320,987 |
| C1 violations | 0 |

At every root, equality is equivalent to there being one factor. The exact per-order outputs are `data/fast_census_*.json`. The V=22 row agrees with the author's 3,301,113 feasible roots and 2,306,337 equality cases. These are exhaustive finite facts conditional on the standard plantri enumeration, not a proof of C1 or its converse for all orders.

`COMPUTED`. The independent C3 checker builds every allowed D-swap and Q-reversal on the finite pair set, keeps only moves not increasing k, and runs reverse reachability from all k=0 pairs. Every pair through V=16 reaches k=0. All 122 pairs of `deeptrap_50_1.json` and all 18 pairs of `weaktrap_30_seed37.json` also succeed. This is stronger than spot-testing the stored starts, but does not establish C3 globally or replay all 940 author starts.

## Reverse-Lamport obligation graph

Only proof-supplied routes are used for the submitted claims. The new gluing is a separately labelled refutation, not a repair of the submitted R2 conjecture.

    A0, C2 false <- AND(A1, A2, A3)
    A1, complete four-factor lattice <- AND(D1, D2, D3)
    A2, extrema carry no tree pair <- AND(D3, T1, E1)
    A3, smallest order 18 <- E2
    C0, exact lattice extremes <- AND(D1, D2, D3)
    T0, directed-cycle criterion <- AND(T1, T2, T3)
    U0, unique factor gives equality <- AND(T0, U1, U2)
    M0, repaired moment barrier <- AND(M1, M2)
    Mstrong, barrier for full prescribed N(w) family <- M3 [missing]
    R0, universal R2 <- R1 [open conjecture; no general proof was supplied]
    R0 refuted <- AND(G1, G2, G3) [new referee route]
    ALG, polynomial construction from R2 <- AND(R0, P1, P2)

## Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
|---|---|---|---|---|---|---|
| A0 | C2 is false, first at V=18 | root | submitted counterexample / AND | major claim | A1,A2,A3 | discharged, `COMPUTED` |
| A1 | The saved graph's full lattice is a four-element diamond | A0 | enumeration / AND | major claim | D1,D2,D3; v18.json | discharged |
| A2 | Neither extreme has a tree pair | A0 | all direction choices / AND | major claim | D3,T1,E1 | discharged |
| A3 | No smaller admissible instance refutes C2 | A0 | minimum-order / AND | side condition | E2 | discharged, finite enumeration |
| C0 | Potentials and two shortest paths give exact extremes | A1 | submitted Lemma 1 / AND | major claim | D1,D2,D3 | discharged |
| D1 | H0 is connected and reversed-spoke chains are integer circulations | C0,A1 | circulation representation / AND | algebraic/logical step | independent connectedness and divergence proof above | discharged |
| D2 | Normalized facial potentials biject with reversals satisfying -1<=phi(R)-phi(L)<=0 | C0,A1 | chain coefficients / AND | definition | facial-boundary circulation basis, bridge case checked | discharged |
| D3 | Min/max preserve constraints, distances are feasible sharp coordinate bounds | C0,A1,A2 | distance bounds / AND | algebraic/logical step | proof above; full finite comparison | discharged |
| T0 | Tree pair iff no directed cycle with all centre exits toward r | root | submitted Lemma 2 / AND | major claim | T1,T2,T3 | discharged |
| T1 | Suppressed F has precisely Q_s edges | T0,A2 | definition / AND | definition | {u(t),r(t)} is opposite s(t) | discharged |
| T2 | In indegree-at-most-one F, undirected cycles are directed | T0 | head count / AND | algebraic/logical step | one head per cycle vertex | discharged |
| T3 | A forest F has exactly one root per component | T0 | edge-indegree count / AND | side condition | r bijective, roots indegree zero | discharged |
| E1 | All 20 pairs of the saved graph have been checked | A2 | finite certificate / AND | side condition | independent.py; all-state and all-factor enumerations agree | discharged, `COMPUTED` |
| E2 | Every rooted plantri instance through V=18 was checked | A3 | exhaustive class / AND | side condition | census_18.json; 26 failures, none smaller | discharged, `COMPUTED` |
| U0 | Unique factor implies #TM=2^c_min | root | submitted Lemma 3 / AND | major claim | T0,U1,U2 | discharged |
| U1 | A Q-cycle reversal preserves s and changes u | U0 | Lemma 5.2 / AND | proved earlier | LATTICE-READING.md section 2 | discharged |
| U2 | Each rooted forest state has exactly one partner | U0 | forest orientation / AND | algebraic/logical step | unique orientation toward each component's root | discharged |
| M0 | Vanishing plus a nonzero minimal moment does not imply 2^m atoms | root | submitted Proposition 4 / AND | major claim | M1,M2 | discharged |
| M1 | The two integer PTE examples have the stated moment matches | M0 | arithmetic / AND | algebraic/logical step | exact sums above; moments.json | discharged |
| M2 | Diagonal embedding kills all multivariate degrees below m | M0 | restriction / AND | algebraic/logical step | substitution h=x(1,...,1) | discharged |
| Mstrong | Full Theorem B identities cannot prove C1 | root, stronger reading | diagnostic / AND | major claim | M3 | open |
| M3 | The PTE examples satisfy every prescribed N(w) identity of actual configurations | Mstrong | extra bridge / AND | missing | neither realized nor proved by the submission | failing |
| R0 | Some extreme or irreducible succeeds in every feasible instance | root | submitted R2 evidence | major claim | R1; new counterexample G1-G3 | failing |
| R1 | A general argument extends beyond the finite R2 tests | R0 | conjecture / AND | missing | no general proof was supplied or claimed; finite evidence was honestly labelled | open |
| G1 | Explicit rigid-face gluing gives a valid V=33 input and product factor set | R0 refutation | new referee / AND | algebraic/logical step | LATTICE-READING.md gluing lemma; graph certificate | discharged |
| G2 | Its order is B_4 | R0 refutation | new referee / AND | side condition | fixed gluing-face potential; all 16 potentials and covers | discharged, `COMPUTED` base |
| G3 | All ten R2 candidates fail | R0 refutation | new referee / AND | side condition | two enumerations; second_R2_glued_V33.json | discharged, `COMPUTED` |
| ALG | R2 yields a polynomial-time tree-pair construction | root | proposed algorithm / AND | major claim | R0,P1,P2 | failing |
| P1 | The irreducible candidate list is polynomial | ALG | threshold solutions / AND | algebraic/logical step | LATTICE-READING.md section 7 | discharged |
| P2 | An arbitrary candidate factor can be given a successful direction choice in polynomial time, or certified to fail | ALG | orientation search / AND | missing | criterion gives linear checking of a chosen pair, not existential search | failing on the proposed algorithmic route; complexity unresolved |

## Final verdict

`CORRECT` for (a)-(e), the three specific replacement failures, C1 through V=22 and the explicitly bounded C3 evidence. The repaired version of (f) `FOLLOWS`; the stronger full-identity impossibility is `NOT ESTABLISHED BY THIS PROOF` at M3. Universal R2 is `WRONG`, refuted by G1-G3 at V=33. The claimed polynomial implication remains unsupported at P2 independently of R2's failure. No proof of global C1, its equality converse or C3 is claimed.
