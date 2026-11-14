# Exact families of paired states

All new proofs are PROVED-HERE, T2, unreviewed. Every numerical table and finite matrix certificate is COMPUTED, T4, under review. No independent referee has checked this folder. The general transfer identities have proofs below; the small numerical recurrences have machine-checkable integer certificates, whose arithmetic still needs independent review. The supplied manuscripts are cited as LIT without asserting peer review.

Write S for states, P for ordered disjoint pairs, M for tree matchings, F for forest pairs, and H for undirected Hamiltonian cycles. PROVED-HERE, by unique orientation toward the roots, F=M for every instance. Throughout, the signed polynomial is

    F_T(z) = sum_(r,s) epsilon(r,s) z^omega(s),
    epsilon = (-1)^((n+J)/2).

This is i^n times the paper's exponential sum after z=exp(x). It is not the incidence determinant. We quotient by an overall sign and monomial factor when displaying a normalized polynomial. The JSON retains both factors. Unit bounded-spoke-face circulation fixes exponent differences; adding a row or column potential changes only the monomial factor. Reflection can reverse exponents as well as signs. Positivity below concerns the explicitly normalized polynomial for real z>1.

## 1. Even prisms, complete formulas

PROVED-HERE. Let p=2m>=4. The primal has vertices a_i,b_i, indices modulo p, and edges a_i a_(i+1), b_i b_(i+1), a_i b_i. Its dual has a p-cycle v_0,...,v_(p-1) and two poles N,S, each adjacent to the entire cycle. Every dual face is equivalent under automorphisms. Choose t0=Nv_0v_1. Then

| Quantity | Exact value |
|---|---:|
| Primal order | 4m |
| S | m |
| P=M=F | 2 |
| c_min | 1 |
| Normalized F_T(z) | z^(m-1)-1 |
| First nonzero coefficient at z=1 | m-1 |
| H | 2m+2 |
| H avoiding a rail edge | 2 |
| H avoiding a rung | 2m-2 |
| Images for fixed t0,e0 | 2 |
| Images for three choices of e0 at t0 | 6 |

PROVED-HERE, state proof. Apart from t0, the northern black faces have available corners {v_(2i),v_(2i+1)}, 1<=i<m. The southern black faces have available corners {S,v_(2i+1),v_(2i+2)}, 0<=i<m, with roots removed. Exactly one southern face takes S. Once its index j is chosen, the other choices are forced along the resulting alternating path, so there are m states. Write them s_0,...,s_(m-1). They have

    northern face i -> v_(2i+1) if i<=j, otherwise v_(2i);
    southern face i -> v_(2i+2) if i<j, S if i=j,
                       v_(2i+1) if i>j.

The two extreme states are disjoint. Any disjoint states must differ at every northern face, forcing their indices to lie on opposite sides of every i, hence to be 0 and m-1. Their Q graphs are rooted forests. For s_0, northern opposite edges form the star N-v_(2i+1), 1<=i<m. The first southern opposite edge is v_1-v_2; the others are S-v_(2i+2), 1<=i<m, with the last endpoint v_0. These are three disjoint trees rooted at N,v_1,v_0. The reflected statement holds for s_(m-1). Thus there are two forest pairs. The sole undirected D is a spanning cycle of X, so c_min=1.

PROVED-HERE, polynomial proof. Every nonroot is on that D-cycle, so there are no strictly interior vertices. The disk identity gives B=(n-3)/2=m-2 and W=B+1=m-1. The two orientations differ in height by W and have opposite signs. Therefore the normalized polynomial is z^(m-1)-1. It is positive for z>1. As a sequence in m it satisfies f_(m+2)=(z+1)f_(m+1)-z f_m, with f_2=z-1 and f_3=z^2-1.

PROVED-HERE, Hamiltonian proof. If a Hamiltonian cycle omits some rungs, its used rungs delimit intervals on the two rails. With exactly two used rungs, both rails must be spanning paths, so the rungs are adjacent and both rails omit their common intervening edge. There are p such cycles. If more than two rungs are used, any gap between consecutive used rungs of length greater than one forces both rail segments across that gap, creating an isolated cycle at those two rungs. Therefore all rungs are used. At each vertex exactly one rail edge is then used, so each rail is an alternating matching. The two opposite phases give two Hamiltonian cycles; equal phases give disjoint squares. Thus H=p+2. A fixed rail edge is omitted by one of the p first cycles and one of the two alternating cycles, giving 2. A fixed rung is omitted by p-2 of the first cycles and neither alternating cycle. The recovery counts follow from injectivity and the disjointness of the three edge-avoidance images.

COMPUTED. `count.py prism --max 10` checks m=2,...,11, including every primal edge's avoidance count and all recovery images. Prisms have no separating triangles in the dual. All three counts S,M,H have growth base 1 per primal vertex; M/S=2/m. The exponential conjecture M>=2^c_min is an equality. The ratio 3M/H=3/(m+1) tends to zero.

## 2. Explicit hexagonal tubes

PROVED-HERE. The dual T_(p,L), for even p>=4 and L>=0, has rings v_(j,i), 0<=j<=L and i modulo p, and poles A,B. Add all ring edges. Between consecutive rings add v_(j,i)v_(j+1,i) for every i. In the quadrilateral indexed i, put the diagonal v_(j,i)v_(j+1,i+1) when i is even, and v_(j,i+1)v_(j+1,i) when i is odd. Join A to ring 0 and B to ring L. This is the adjacency rule in `families.py`.

PROVED-HERE. For L>=1 the first ring vertices have degrees 6,4 alternating, and the last ring has 4,6 alternating. Every middle ring vertex has degree 6, and each pole has degree p. Thus the dual is Eulerian and its primal is cubic bipartite, with p squares, p(L+1)-p hexagons, and two p-gons. When p=4 or 6, coincident face sizes must be combined. The primal order is N=2p(L+1). The listed faces triangulate a sphere; the graph is simple, hence its triangulation is 3-connected. Every 3-cycle is facial: three vertices in a ring cannot form one; a cycle using consecutive rings bounds one of the displayed triangles; a cycle meeting a pole uses two adjacent vertices of its cap ring. Therefore there are no separating triangles.

For L>=1 choose the lateral root {v_(0,0),v_(0,1),v_(1,1)}. For L=0 use {A,v_(0,0),v_(0,1)}. The distinction matters. COMPUTED root sweeps through L=5 find M=2 at every root for p=4, but the following sets for p=6.

| L | M over all facial roots, p=6 |
|---:|---|
|1|4|
|2|12,14|
|3|34,38,40|
|4|82,96,98|
|5|194,230,232,240,242|

No assertion of root independence beyond these finite checks is made. State counts are root independent by the trinity theorem, cited in the dimer report; all numerical recurrences below use the specified root.

### The exact transfers and why they count

PROVED-HERE. Process black triangles in layer order. For S the boundary records which live nonroot vertices have already been matched. Choosing a corner marks that vertex, and a vertex can be forgotten only after it has been marked exactly once. This is a bijection between transfer paths and states. For M identify all three roots to one vertex, retain also the connectivity partition of opposite edges on live vertices, and reject an edge joining already-connected vertices. The opposite-edge graph has n edges and n+1 vertices after root identification. It is a tree precisely when no cycle was created, equivalent to a rooted forest before identification. Thus this transfer counts M=F. A forgotten component need not be explicitly rejected: the fixed final edge count forces a cycle elsewhere if such a disconnected component survives.

PROVED-HERE. For P record separate used bits for r and s and connectivity for edges r(t)s(t). Add q whenever an edge closes a component cycle. A completed pair has degree two on every nonroot. Consequently the product of q marks is q^c(D), with no missing or extra cycles. Triangle choices have distinct r,s corners. Forgetting enforces both bijections. This proves the polynomial-in-q transfer, including c_min from its lowest exponent. This q is a cycle marker, distinct from z in the signed height polynomial.

PROVED-HERE. For H fix the first pole's color to 0, assign binary colors to successive rings, forbid monochromatic facial triangles, and retain connectivity of monochromatic edges in both colors. Reject cycles and a component disappearing from the boundary before the terminal cap. Each ring must contain both colors because its edges form a cycle. An induced-tree partition therefore cannot have a finished color class in the middle of the tube, and no valid partition is discarded. The terminal pole may have either color; accept precisely two final tree components. This counts each unordered induced-tree partition once, hence each Hamiltonian cycle once, by plane duality. This is a second HC implementation, separate from complement-of-perfect-matching enumeration and the general edge-frontier transfer in `transfer.py`.

PROVED-HERE. At a middle layer the boundary consists of a fixed number of ring vertices. Relabel them by subtracting the layer coordinate and canonically number partition blocks. The triangle list and transfer rules are then identical at every layer. Thus each quantity has an exact expression v T^r w with a finite integer matrix, or a matrix over Z[q] for the pair-cycle distribution. For S,M,P the saved prefix ends at L=2 and r=L-2. For H the expression is v T^L w. All entries, v and w are in the certificate JSON files.

COMPUTED, exact certificate arithmetic, under review. `certify.py`, `hamilton_matrix.py`, and `pair_matrix.py` give the following recurrences. A list [a1,...,ad] means f_L=sum_(j=1..d) aj f_(L-j). Initial values start at the indicated L, and the recurrence applies once those d values are available.

| Width | Quantity | Start L | Initial values | Recurrence list | Matrix dimension |
|---:|---|---:|---|---|---:|
|4|S|2|13,34|3,-1|4|
|4|M=F|2|2|1|2|
|4|P|2|2|1|2|
|4|H|0|6,14,30|2,-1,4|12|
|6|S|2|91,513,2881,16171|7,-9,7,-1|15|
|6|M=F|2|12,34,82,194,464,1104,2642,6290|0,4,4,0,1,0,-4,-4|39|
|6|P|2|16,56,176|4,-4,4|36|
|6|H|0|8,44,176,752,3200,13568|2,-1,40,8,64,-16|64|

The small omitted L=0,1 values are in the next table. For both widths c_min=1 for all L. The pair transfer checks eventual repetition of its Boolean boundary vector restricted to costs 0 and 1, at offsets [0,1] for p=4 and [2,3] for p=6. The prefix checks cover the earlier offsets. The repeats imply the existence of a one-cycle cover at every later length; zero cycles cannot cover nonempty X.

PROVED-HERE, recurrence certification principle. Let Q(x)=x^d-a1 x^(d-1)-...-ad. If v Q(T)=0 then every future scalar discrepancy vanishes. More generally the discrepancy sequence v T^r Q(T)w itself obeys the characteristic recurrence of the D-dimensional matrix T. Checking D successive discrepancies equal to zero proves all of them zero by Cayley-Hamilton. The scripts use this finite criterion, with exact integer arithmetic. They do not infer an infinite statement merely from a long scalar fit.

COMPUTED. The relevant counts are:

| p | L | N | S | P | M=F | c_min | H |
|---:|---:|---:|---:|---:|---:|---:|---:|
|4|0|8|2|2|2|1|6|
|4|1|16|5|2|2|1|14|
|4|2|24|13|2|2|1|30|
|4|3|32|34|2|2|1|70|
|4|4|40|89|2|2|1|166|
|4|5|48|233|2|2|1|382|
|4|20|168|433494437|2|2|1|111601126|
|6|0|12|3|2|2|1|8|
|6|1|24|16|4|4|1|44|
|6|2|36|91|16|12|1|176|
|6|3|48|513|56|34|1|752|
|6|4|60|2881|176|82|1|3200|
|6|5|72|16171|not tabulated here|194|1|13568|
|6|40|492|2697215884908658351209612006211|see pair matrix|3086691296945298|1|143483007122235382275409280|

COMPUTED. Direct state and primal perfect-matching enumerations agree with transfers through L=5 at width 4 and L=4 at width 6. State counts also agree with the integer incidence determinant. HC matrices agree with the separate edge-frontier transfer through width-4 L=20 and width-6 L=29. All this remains T4, not an independent referee's T3 certificate.

### Generating functions, rates and avoidance

PROVED-HERE conditional on the displayed certificate arithmetic. The width-4 state sequence is S_L=Fib_(2L+3), with Fib_1=Fib_2=1. Its generating function from L=0 is (2-z)/(1-3z+z^2). Also

    sum H_L z^L = (6+2z+8z^2)/(1-2z+z^2-4z^3).

`recurrences.json` gives reduced generating functions for all rows, with the L=2 shift stated explicitly. Given initial f_0,...,f_(d-1), the numerator is the degree-<d part of their generating polynomial times 1-sum aj z^j. This supplies a rational generating function without any further enumeration.

COMPUTED numerical roots of the certified characteristic polynomials give these growth bases per layer and per primal vertex. They are approximate, not exact real certificates. The exact candidates are the largest positive roots of the characteristic polynomials in `recurrences.json`; dominance can also be read from the finite nonnegative matrices.

| p | Quantity | Per layer | Per vertex |
|---:|---|---:|---:|
|4|S|2.618033989|1.127838486|
|4|M|1|1|
|4|H|2.314596212|1.110604438|
|6|S|5.613134261|1.154605936|
|6|P|3.130395435|1.099765100|
|6|M|2.382975768|1.075044980|
|6|H|4.258116576|1.128326519|

The width-6 M polynomial factors as (x-1)(x^3-4x-4)(x^4+x^3+x^2+x+1). Thus the predicted M/S decay per layer is about 0.4245, and 3M/H about 0.5596. At width 4 M/S=2/Fib_(2L+3), so exponential rarity already occurs without separating triangles. All numerical asymptotic conclusions inherit the certificate review status.

PROVED-HERE. To count H avoiding any prescribed primal edge, require its dual edge to be monochromatic in the two-tree transfer. If the edge is introduced at layer j, replace that layer's T by T_eq which retains exactly transitions giving its endpoints the same color. The exact answer is v T^(j-1) T_eq T^(L-j) w. A ring edge uses the colors of the new ring; a vertical or diagonal edge uses the old and new rings. For an edge at a cap constrain v or w instead. `avoid.py` implements all four cases for arbitrary supplied p,L and dual edge. This is an exact recurrence/matrix-power specification for every edge, including positions moving with L, rather than an assumption of edge transitivity.

COMPUTED. For the three dual edges (0,1), (0,p+1), (1,p+1) of the specified root, avoidance counts are:

| p | L | Counts in that order |
|---:|---:|---|
|4|1|4,2,8|
|4|2|8,6,16|
|4|3|20,14,36|
|4|4|48,30,88|
|4|8|1344,878,2504|
|6|1|18,8,18|
|6|2|66,42,68|
|6|3|282,174,296|
|6|4|1210,710,1280|
|6|8|397338,236822,415824|

PROVED-HERE. For each root prescription recovery produces exactly M cycles, and over its three edges exactly 3M, using the already-refereed injectivity argument. At width 4 this is always 2 and 6. The signed polynomial there has only two terms because P=2 and c_min=1. Its sole D spans all nonroots, so the disk argument in Section 1 yields normalized F_T(z)=z^(2L+1)-1. The leading coefficient at z=1 is 2L+1. As L varies it satisfies f_(L+2)=(z^2+1)f_(L+1)-z^2 f_L. At width 6 the polynomial has many terms and no closed recurrence in L has been established here. Exact polynomials through L=4 are retained in `tube6.json`; for L=1 it is (1+z)(z^5-1). Only the general positive leading-coefficient formula is proved for larger L, not global positivity of F_T(z).

## 3. Iterated four-subdivision

PROVED-HERE. Subdivide each edge of an Eulerian triangulation once and replace each face by its four midpoint triangles. Old vertex degrees stay even and each midpoint has degree 6. The result is a simple Eulerian sphere triangulation. Starting at the octahedron, the r-th subdivision has dual order 4*4^r+2 and primal order 8*4^r. This follows from F'=4F and Euler's formula. The adjacency rule is in `subdivide` in `families.py`.

REFUTED as a literal definition. Replacing a cubic vertex by a six-cycle and attaching its three old edges leaves three new vertices of degree 2. It does not define a cubic graph. The leapfrog and the dual four-subdivision should not be identified without specifying their distinct operations and orders. This report uses exactly the dual four-subdivision above.

COMPUTED. The first octahedral subdivision, rooted at {0,6,7}, has N=32, S=54, P=20, M=F=12, c_min=1, H=84, and 28 cycles avoiding each of the three root edges. Recovery gives 12 per prescription and 36 over the three. Its normalized signed polynomial is

    -1+z+z^2+z^5+z^6-z^8-z^9-z^12-z^13+z^14.

COMPUTED. Four-subdivisions of q=1,2,3 stacked cubes have respectively dual orders 18,30,42, S=54,1944,69984, P=20,432,13376, M=12,160,2088 and c_min=1 throughout. `subdivided-stacks.json` retains all graphs and polynomials. These are finite tests, not recurrences in r or q. The full second iterated octahedral subdivision and infinite growth rates remain uncomputed. This family has not been quantitatively solved beyond these cases.

## 4. Nested white-face prism sums

PROVED-HERE. A family member consists of q hexagonal-prism duals glued successively into a white face, retaining the first black root. The incoming cap is black. Choose the outgoing white triangle of each inserted labeled bipyramid to be {v_4,v_5,S}; it lies inside its local D-cycle. `stack(6,q)` gives the corresponding embedded chain using the laboratory's face ordering. This labeling fixes the gluing permutation; arbitrary permutations can change H. The dual order is 5q+3 and N=10q+2.

PROVED-HERE. States factor over the q pieces. A new interior vertex can only be matched by a new black face, and their counts agree, so no new black face can take a boundary vertex. Removing them leaves precisely an old state. Disjoint pairs factor as well. Each prism piece has three states and two pairs. The local D-cycles have disjoint nonroot vertex sets even when their disks nest, so c_min=q. Local rooted forests attach at one vertex in each root component, preserving acyclicity and root counts. Thus

    S=3^q, P=M=F=2^q, c_min=q,
    M/S=(2/3)^q.

PROVED-HERE. There is one undirected D-cover, with q cycles. Its nested disk areas are 2,7,...,5q-3. The innermost local prism cycle encloses two white triangles. Each inserted piece replaces one inner white triangle by six white triangles, increasing every enclosing disk area by five. Therefore

    normalized F_T(z)=product_(j=0..q-1)(z^(5j+2)-1).

It is positive for real z>1, and its first nonzero coefficient at z=1 is product_(j=0..q-1)(5j+2). The recurrence is F_(q+1)=(z^(5q+2)-1)F_q with F_1=z^2-1. This is a variable-coefficient recurrence, not a claim of a rational generating function in q.

PROVED-HERE. Hamiltonian cycles glue by their missing edge on the separating triangle. Restrict a global two-induced-tree partition to either side. Each color meets the separator in a connected vertex or edge, so its restriction remains connected: any excursion through the other side can be replaced inside that separator vertex or edge. It remains acyclic and induced. Conversely two local partitions of the same triangle pattern glue into induced trees, uniquely. Thus H(A sum B)=sum_(i=1..3) H_A(avoid i) H_B(avoid i), with the gluing permutation applied. More general prescribed-edge counts use the same sum with a simultaneous-avoidance count on the side containing that edge.

COMPUTED local tensor, independently inspectable from the eight explicit prism cycles in `stack-HC-transfer.json`. In the stated edge order the through-piece matrix is

    C = [[0,1,1], [1,0,1], [1,1,2]],
    u = [4,2,2], a = [2,2,4].

PROVED-HERE conditional on that finite eight-cycle table and the stated labeled gluing. The outgoing avoidance vector after q pieces is u C^(q-1), and for q>=2 the total is u C^(q-2) a^T. Since C a^T=3a^T and u a^T=20,

    H_1=8; H_q=20*3^(q-2) for q>=2.

The generating function is 8z+20z^2/(1-3z). Root-avoidance counts at the retained original root are 3^(q-2)*(4,6,10) for q>=2 in the stored order; the initial prism vector is (2,2,4). The first piece's root-to-exit tensor is C'=[[1,1,0],[1,0,1],[2,1,1]], a column permutation of C, and C'a^T=(4,6,10)^T. This proves the root formula. The fully explicit matrix formula covers arbitrary local edge prescriptions by retaining that edge's equality condition in its piece. Direct enumeration confirms q<=5; the tensor recurrence is replayed through q=8.

COMPUTED.

| q | N | S | P=M=F | c_min | H | Recovery over three root edges |
|---:|---:|---:|---:|---:|---:|---:|
|1|12|3|2|1|8|6|
|2|22|9|4|2|20|12|
|3|32|27|8|3|60|24|
|4|42|81|16|4|180|48|
|5|52|243|32|5|540|96|

The rates per vertex are 3^(1/10) for S and H, and 2^(1/10) for M. Recovery for a fixed prescription gives 2^q cycles and for its three prescriptions 3*2^q. Other roots can have no direct pair, as the limits report establishes; those cases require recursive gluing. The formulas above must not be assigned to every root.

## 5. Unbounded c_min without separators remains open here

HUNCH, not a constructed family. Such a family may exist, but neither the two tube widths nor the subdivided stacks above provide it. The prediction that four-subdivision would preserve or amplify stacked c_min failed: q=2 and 3 return c_min=1. Keep this failure when planning a search. It is not evidence that c_min is universally bounded in 4-connected Eulerian triangulations. A useful next test is an exact minimum-cycle pair search in width>=8 tubes or families built across separating 4-cycles.
