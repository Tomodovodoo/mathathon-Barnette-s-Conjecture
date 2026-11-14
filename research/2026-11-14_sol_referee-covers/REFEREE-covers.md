# Referee of the cycle-cover report

Reviewer: GPT-6.1-sol, 14 November 2026. New arguments below are PROVED-HERE, T2, independently AI-refereed here, human check pending. Numerical results are COMPUTED. No author verification code was imported or executed.

## Audit boundary

The submission is `../2026-11-14_astra_cycle-covers/`, especially PROOFS sections 1–5. I use the brief's simple face-bicoloured sphere triangulation, facial black root and ordered disjoint states. A cover is an undirected degree-two spanning subgraph of the incidence graph on A and X, or equivalently the selected sides in T. The accepted source inputs are OpenAI Lemma 4.1, fixed-second-state cancellation, and unique partner for a rooted forest state. I read the supplied paper's text, especially sections 4–7. These are supplied-preprint inputs, not assertions of external peer review.

## Claims and findings

### C1. Separator-free family

Exact claim: for every integer m>=2, the submitted T_m, rooted at P_0=A x_0 y_0, is a simple Eulerian sphere triangulation on 3m+2 vertices with no separating triangle. It has precisely one cover, consisting of m-2 triangles and a pentagon; c_min=m-1 and M=2^(m-1).

Verdict CORRECT, PROVED-HERE. Subdividing the m distinct Bx_i edges of the 2m-equator bipyramid gives exactly the six displayed faces per i and 9m distinct edges. Euler gives 6m faces. The vertices A,B have degree 2m; x_i,z_i have degree four; y_i has degree six, also at m=2. The construction is simple. To list all graph triangles, a triangle through a pole must use adjacent neighbours; away from the poles it must use x_i z_i and a common y-neighbour. These are exactly the listed faces, including at m=2. Thus none separates. The black list P_i,Q_i,R_i gives one black face at each edge.

The forcing proof closes. P_i for i!=0 must use x_i y_i. The two black incidences at each x_i force Q_i to use x_i, and the two at every z_i force both Q_i and R_i to use z_i. The root excludes x_0,y_0. Hence Q_0=z_0 y_(m-1), R_0=Bz_0, and the saturated y_(m-1) forces R_(m-1)=Bz_(m-1). B is now saturated. The remaining R_i use z_i y_i. These choices form the stated components and satisfy every degree constraint.

If any orientation had cyclic Q_s, the fixed-s cycle reversal would change r and hence change the cover, since s and a cover determine r. This contradicts uniqueness. All 2^(m-1) orientations therefore have forest Q_s. Conversely every tree matching has its unique partner. This establishes the count without the exponential conjecture.

COMPUTED independent range: m=2,...,8, all states, ordered pairs, opposite-edge graphs and covers, in `code/families.json`. M is 2,4,8,16,32,64,128. Independent unit-circulation polynomial calculations for m=2,...,6 give, up to sign and a monomial, `(z-1)^(m-2)(z^2-1)`. See `code/family-polynomials.json`. This confirms the absolute leading coefficient 2. The pentagon's root-free disk contains two white faces; each triangular component bounds one white face.

### C2. Primal deletion identity

Exact claim: S is a primal edge subset with one incident selected edge at each black vertex other than b0, none at b0; every nonroot face has exactly two selected boundary edges and every root face has none. Then its dual D is a cover and

    c(D) = kappa(G-S)-1 = cycle_rank(T[S*]).

Verdict CORRECT, PROVED-HERE. The first local constraint supplies one side per bounded black triangle; the second gives degree two at every nonroot dual vertex and zero at roots. Replacing sides by their two incidence spokes proves the inverse correspondence and the 2^c ordered orientations.

For the component identity, c disjoint Jordan curves divide the sphere into c+1 regions, also when nested. A region contains triangle interiors, and any two such interiors in that region are joined by a generic path crossing only sides outside D. This identifies its triangles with one component of G-S. The spanning dual subgraph has n edges, n+3 vertices and c+3 components, giving rank c by E-V+kappa. Individual cycles dualize to bonds. Root-free shores are laminar; their region adjacency graph is a tree with one parallel bundle per cycle. White primal vertices in a shore are exactly the white dual faces in its disk.

COMPUTED: the implementation checks the deletion identity on every cover of every tested family, both saved flip witnesses, and every separator-free facial rooting through order 16.

This agrees with `proofs/primal/DICTIONARY.md`. It does not substitute S for the recovery matching. In the topology report's Lemma 3.1, P is a dual set with one edge at EVERY face, P* is a primal perfect matching, and F=G-P* is a primal 2-factor. Its formula is c(F)=1+cycle_rank(P). Here S has no white degree condition, G-S need not be regular, and D itself is a union of dual cycles. Both formulas are valid for their separate objects. They have no conflicting plus/minus-one convention.

### C3. Exactly two covers

Exact claim: if the two covers have cycle counts c1,c2 and share j identical component cycles, then M=2^c1+2^c2-2a, with a either 0 or 2^j. Consequently M>=2^min(c1,c2); equality requires c1=c2=j+1 and a=2^j.

Verdict CORRECT, PROVED-HERE. Orient Q_s from its first-state corner to the unused corner. Every nonroot has outdegree one and each root zero. A connected component has at most one root; a rooted component is a tree and a root-free component unicyclic. Thus s has 2^k partners where k counts root-free components. Distinct partners give distinct covers. With only two covers k is zero or one, so a shared second state contributes two pairs and no tree matching. All other partnered states contribute one pair and one tree matching. This gives the formula for M.

On a face whose two cover choices differ, the common second corner is forced. Hence a nonidentical component has forced orientation. Components unchanged as cycles can be oriented freely; they are vertex-disjoint from every other component in both covers, so there are no additional matching conflicts involving them. Either the forced choices are inconsistent, or exactly 2^j common second states result. Distinctness implies j<=min(c1,c2)-1. Substitution gives the bound and the equality condition. The strict inequality for two covers is not proved by this argument.

COMPUTED: `analyse` independently asserts the exact overlap formula on every two-cover instance encountered by `census`; replay command in the README. The saved census used the initial enumerator; a final replay after adding this assertion is recorded separately there.

### C4. Census

Exact claim: no failure of M>=2^c_min, or of strictness when there is more than one cover, occurred among 23,824,742 facial-root occurrences of separator-free unlabelled graphs through |T|=24.

Verdict CORRECT AFTER FIX to the evidence wording, COMPUTED. The retained summaries report this, and their total and graph counts are consistent. This referee independently reproduces the whole census only through |T|=16: 129 graphs and 3,374 face occurrences, including both facial colours by recolouring the root black. All histograms agree and no violation occurs. Orders 17–24 remain an author computation, not independently replayed numerical certification by this referee.

The word "rooted" counts every face of one representative of each unrooted class, including automorphism-equivalent faces. It is not a count of nonisomorphic rooted maps. Indeed each graph contributes 2V-4 roots. The published e_4 column of Brinkmann–McKay, *Fast generation of planar graphs*, Table 6, agrees at every V=6,...,24. In particular its last three entries are 37,231; 114,560; 384,053, not the orientation-preserving e'_4 counts. Source opened: https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf . The web cached table was accessible after direct fetches timed out. This checks population size, not the author's mathematical invariants at larger sizes.

### C5. Disconnected levels and minimizers

Exact claims: under reversals of a single simple directed cycle in the complementary incidence orientation, a fixed-c level need not be connected, and the minimizing level need not be connected.

Verdict CORRECT, REFUTED universal connectivity, COMPUTED certificates in `code/witnesses.json`. I rebuilt all states and covers from the saved edge lists and root, without importing either verifier. The first witness has S=42, P=50, M=30, four covers, and square flip graph with opposite vertices of c=3 and the other vertices c=1,5. The other witness has S=54, P=20, M=12 and a square with opposite c=1 minima and the other vertices c=3. Cover ordering in my JSON differs from the authors'.

To test adjacency, I formed the symmetric difference in the incidence graph by recording the deleted corner u(t). A single alternating cycle has exactly the changed face nodes and the graph of changed corners must be connected and degree two. These conditions are necessary and sufficient, since at each changed face the old and new deleted incidences determine its alternating passage. Enumerating all pairs of covers checks the larger simple-cycle reversal move set. Disconnectedness therefore also holds for any restricted facial move set. The author's smallest-order assertion is only independently checked here by the census range through 16, not through 17.

### C6. Lowest coefficient

Exact claim: with unit white-face circulation and q=c_min, the real signed exponential sum has first coefficient

    [x^q] F(x) = (-1)^((n-q)/2) sum_(D:c(D)=q) product_(C in D) a_C,

where a_C counts white faces in the root-free disk. Its absolute value counts minimal covers with an independent white-face mark in each disk.

Verdict CORRECT, PROVED-HERE conditional on the stated height-increment identity. A cover contributes

    (-1)^((n+c)/2) exp(b_D x) product_C (1-exp(a_C x)).

Every a_C>0 by the disk identity. The exact order is c, and the degree-c sign is (-1)^((n-c)/2). Thus larger covers do not contribute at degree q and minimum-cover contributions have one sign. There is no cancellation at that first degree. The same coefficient occurs for powers of z-1 after z=exp(x); the q-th derivative is q! times it.

The marks are indexed by component cycles. They may repeat for nested disks. Dualizing the cycles and retaining their marks is a literal bijection with admissible minimal laminar bond families pointed by a white primal vertex on each root-free shore. An unpointed arbitrary laminar bond family is not sufficient: retain the local constraints on S. The interpretation counts neither all tree matchings nor their orientations. T_m has coefficient 2 and M=2^(m-1); prisms have coefficient m-1 and M=2. Both possible ratios are unbounded. This explicitly disproves an unweighted bijection to tree matchings.

## Obligation graph and dependency table

The supplied routes are AND routes, with no replacement proof silently used: C1 <- embedding, exhaustive triangles, forcing, unique-cover cancellation; C2 <- local dictionary, Jordan regions; C3 <- partner multiplicity, shared-state orientations; C4 <- population, enumerator correctness, all roots completed; C5 <- witness enumeration, exact move definition; C6 <- positive slopes, cover factorization, common first sign, marking dictionary.

| ID | Exact obligation | Needed by | Route / edge | Classification | Support | Status |
|---|---|---|---|---|---|---|
| O1 | Listed faces embed T_m and exhaust triangles | C1 | construction / AND | algebraic/logical step | C1 argument above | discharged |
| O2 | Every cover choice is forced | C1 | forcing / AND | algebraic/logical step | saturated degrees above | discharged |
| O3 | Cyclic partnered Q gives another cover | C1,C3 | reversal / AND | named theorem | OpenAI fixed-s reversal; cover determines r | discharged |
| O4 | Regions equal components of G-S | C2 | duality / AND | algebraic/logical step | generic path proof | discharged |
| O5 | Shared states occur in 0 or 2^j orientations | C3 | overlap / AND | algebraic/logical step | changed-face constraints | discharged |
| O6 | Population through 24 equals the stated classes | C4 | generation / AND | named theorem | plantri Table 6 and face multiplier | discharged |
| O7 | All larger-root invariants computed correctly | C4 | census / AND | side condition | author summaries; independent replay only through 16 | open |
| O8 | Saved graph has exactly the asserted moves | C5 | finite enumeration / AND | algebraic/logical step | check.py witnesses | discharged |
| O9 | Every a_C is positive | C6 | disk / AND | named theorem | OpenAI Lemma 4.1 | discharged |
| O10 | Cycle reversal adds a_C to height sum | C6 | weights / AND | proved earlier | circulation plus detour, OpenAI 5.2–5.3 | discharged |
| O11 | Minimal terms share the same sign | C6 | Taylor / AND | algebraic/logical step | displayed factorization | discharged |

## Verdict

FOLLOWS for C1,C2,C3,C5,C6 with the stated source inputs and move convention. C4 is INDETERMINATE FROM THE PROVIDED MATERIAL as an independently certified full computation beyond order 16; quote the larger range as the author's COMPUTED result. The general exponential bound and multi-cover strictness remain CONJECTURE.
