# G: the formula is correct; the proposed descent is false

Status of G: CONJECTURE, not proved here. New proofs below are PROVED-HERE, T2, unreviewed. Census results are COMPUTED, T4. Exact counterexamples have also been replayed with the independent `workings/barnette_lab` engine and NetworkX flow. This is code cross-validation, not an independent human or agent referee.

## Contract and notation

G asks whether a simple rooted Eulerian sphere triangulation T, with more than six vertices and no separating triangle, has a non-root degree-4 vertex with a simple contraction admitting a pair. Write its neighbours as a,p,b,q, in cyclic order, with black faces xap and xbq. Merge M identifies p,q. Merge N identifies a,b. The root is a black face t0.

PROVED-HERE, using the independently refereed pair criterion in `research/2026-11-14_sol_referee-structure/INTEGRATION.md`, section 2. A simple contraction is good precisely when it creates no black-inner separating triangle. The criterion uses Hall and Euler, without Proposition 5.1 or a signed count. T itself has a pair by OpenAI Proposition 3.1.

## 1. The exact deficiency formula

PROVED-HERE. For S contained in the nonroots, put

    f(S) = sum over bounded black faces t of min(2, |t intersect S|) - 2|S|.

Assume U=V(T) minus S induces a connected graph K. For each face region F of K which is not an actual face of T, let d_F count boundary edge sides, with repetitions, and w_F count those sides whose original incident face on the region side is white. Then

    f(S) = sum_F (d_F + w_F - 6)/3.                         (G1)

Proof. Write p=|U|, m=|E(K)|, b,w for actual black and white faces of K, and q for its remaining regions. A black triangle with j corners in U has shortfall max(0,j-1) from its maximum Hall contribution 2. This is its number of induced edges, less one when j=3. Every edge has one black face. Since T has |V(T)|-2 black faces, this gives

    f(S)=2p-4-m+b.

Euler and side counting give

    p-m+b+w+q=2,       2m=3b+3w+sum_F d_F.

Let beta_F be black minus white original faces in F. Global colour balance and internal-side cancellation give

    w-b=sum_F beta_F,       3 beta_F=d_F-2w_F.

Eliminating m,b,w yields

    f(S)=1/2 sum_F (d_F-4-beta_F)
        =1/3 sum_F (d_F+w_F-6).

Every count uses edge sides, so bridges cause no problem. The root is an actual black face of K and contributes zero to the Hall sum. This also covers U equal to the root triangle, where its other face is a nonactual region. No assumption about separating triangles was used. QED.

COMPUTED. `code/deficiency.py` performs the elimination in SymPy, obtaining residual zero. It then computes Hall sums independently of the induced-embedding face walks. Every connected U containing a possible root face is tested in both possible black colour classes, for all plantri triangulations with 6 through 14 vertices. This is not merely one subset per graph. Repeated boundary vertices occur in the data and are included. See `data/deficiency_6_14.json` for exact counts.

PROVED-HERE. The formula does not extend as written to disconnected U. Its stated connectedness assumption must be retained. The always-valid identity is f(S)=2|U|-4-e(U)+b(U); component-by-component Euler identities can then be applied separately.

## 2. Contraction and Hall sets

PROVED-HERE. Let v be the image of p,q, and let S be a set of nonroots of T/M. If v is absent from S, identify S with the same vertices of T. Then

    f_(T/M)(S)=f_T(S)-[a in S]-[b in S].                  (G2)

If v belongs to S, then neither p nor q is a root, and

    f_(T/M)(S)=f_T((S minus {v}) union {p,q,x}).           (G3)

Proof. All outer black faces retain exactly the same intersection cardinalities with the indicated sets. In G2 the deleted faces xap and xbq contribute the two displayed indicators. In G3 each deleted face contributes 2 and the expanded set has two additional vertices, so the changes cancel. Opposite neighbours are not adjacent, so no surviving face contains both p and q. This argument remains valid for a loop-free parallel-edge contraction because faces retain their identities. QED.

COMPUTED. `code/contraction_formula.py` checks G2 and G3 directly on every contracted nonroot subset, every root, every degree-4 vertex, and both merges through V=14. Root merges and non-simple results are included. The output is `data/contraction_formula_6_14.json`.

PROVED-HERE. Assuming T has a pair, G2 and G3 imply the earlier tight-set obstruction exactly: a bad merge has a set avoiding x,p,q with f_T=0 containing a or b, or f_T=1 containing both. This statement concerns pair loss, whether or not the contraction is simple.

## 3. The short cycles have lengths four AND five

PROVED-HERE. Suppose T has no separating triangle. A merge M fails to be simple with a pair if and only if one of these witnesses exists:

1. A chordless 4-cycle x p y q x, with y outside the closed neighbourhood of x.
2. A chordless 5-cycle x p y z q x whose side away from t0 has exactly one white boundary incidence and four black boundary incidences.

The first obstructs simplicity. The second obstructs the pair in a simple contraction. They need not be mutually exclusive when simplicity is not assumed.

Proof of the four-cycle clause. A third common neighbour y of p,q, other than x,a,b, leaves two different edges from the merged vertex to y. Conversely every surviving parallel pair comes from such a common neighbour. The four-cycle has no chord: p,q are nonadjacent and y is not adjacent to x. There is no loop. One elementary proof of nonadjacency is to consider the triangle x p q if pq existed. On the side containing a, its two sides at x have opposite face colours, so its signed boundary sum would be +1 or -1. Signed triangle-side counting says it is divisible by three, a contradiction.

Proof of the five-cycle clause when M is simple. A separating triangle in T/M must contain v. Otherwise it is a triangle of T and hence an actual face, which survives. Its two incident edges at v must lift to different split copies p,q. If they lifted to the same copy, the old triangle would again be an actual surviving face. Thus the triangle lifts to a path p y z q, closed by q x p. The five vertices are distinct.

This cycle is chordless. A chord pz or yq would give an old triangle with the same image, making the image a surviving face. A chord xy or xz would make that vertex a or b; the other split copy is already adjacent to a and b, again giving a surviving old triangle with the same image. The remaining possible chord pq is impossible. At x, each side of the cycle has one black and one white boundary incidence. After merging, these two sides disappear and the three remaining boundary edges are exactly those of the image triangle. They are all black on its inner side precisely when the original five-cycle has four black and one white inner incidences.

Conversely, a chordless five-cycle of this form has both a and b off its boundary, on opposite sides. They survive strictly on the two sides of the image triangle, so that triangle separates. Its inner boundary is black under the stated colour condition. The pair criterion finishes the proof. QED.

PROVED-HERE. Each side of a four-cycle has w=2 by divisibility of 4-2w by three. A five-cycle has w=1 or w=4. Thus its black-heavy side is unambiguous. Notice that a four-cycle of this kind has become a **2-cycle**, not a triangle, after merging. The four-cycle-only claim in the task's proposed route is false.

COMPUTED. `code/g_structure.py` enumerates chordless four- and five-cycles and their embedded sides, independently tests each merge by flow and simplicity, and compares the answers. All roots of all separator-free plantri triangulations through V=19 pass. This reproduces 62,416 rooted instances at V=8 through 19. It checks each merge, not only the existence of some good one.

## 4. What Euler counting actually gives

PROVED-HERE. Let a chordless d-cycle bound a nonempty triangulated disk, with all its interior vertices having even degree at least four in T. Let k_v be the degree of boundary vertex v within the disk. Let n4 be the number of degree-4 interior vertices. Then

    2 n4 = 6 + sum_(interior, deg>=6)(deg_T-6)
                 + sum_(boundary)(k_v-4).                (G4)

Proof. Euler gives E=3I+2d-3. The sum of disk degrees is 2E. Rearranging gives the familiar disk curvature equation

    sum_interior(6-deg_T)+sum_boundary(4-k_v)=6.

Separate the degree-4 interior terms. QED.

PROVED-HERE. If c is the number of colour changes between consecutive boundary incidences on this side, then

    2 n4 >= 6-c.                                         (G5)

Indeed, every boundary vertex has at least one interior neighbour, since the boundary is chordless and its disk is triangulated. Thus k_v>=3. The fan of k_v-1 incident triangles alternates colours. If the two end colours agree then k_v is even and k_v>=4; if they differ then k_v is odd and k_v>=3. Sum these lower bounds in G4.

In particular, a four-cycle has at least one interior degree-4 vertex. A five-cycle has exactly two colour changes, hence at least **two** interior degree-4 vertices. A six-cycle with all boundary incidences black has at least three. The last assertion is a consequence of G5, not an exhaustive six-cycle census claim.

COMPUTED. The four- and five-cycle checks in `g_structure.py` verify G4 and G5 for each enumerated disk, as well as the two-vertex minimum for five-cycles. These checks precede acceptance of the displayed proof.

## 5. Why the proposed descent cannot prove G

REFUTED, with explicit certificate. An innermost bad four-cycle need not enclose any good vertex. Take V=11, graph 1 in `plantri -b -a 11`, root {0,1,2}. Its rotation system is saved in `data/g_structure_8_16.json`. The cycle

    0,1,7,5,0

encloses precisely vertex 6. It witnesses the non-simple merge {0,7} at vertex 5. It is innermost by interior-set inclusion because its interior is a singleton. At vertex 6 the two merges are:

| Merge | Obstruction | Hall set in the contraction | Deficiency |
| --- | --- | --- | --- |
| {0,7} | parallel edges | {5} | -1 |
| {5,1} | simple, pair lost | {7,8,10} | -1 |

The independent flow value is 11, below the required 12, in both cases. Vertices 3,8,10 each have a good merge. Consequently G remains true on this graph; the asserted inward descent fails. `code/check_certificates.py` and `data/certificates.json` give every face and the Hall calculations. This is the smallest such example in the complete census through V=19.

REFUTED, same graph. The merge {6,4} at x=5 is simple and loses the pair. Its obstruction is the five-cycle 1,6,5,4,9, with inner set {7,8,10}. A four-cycle witness in that merge direction would make the contraction non-simple, so no four-cycle witness can replace it.

PROVED-HERE. For any non-root degree-4 vertex z, f({z})=deg(z)/2-2=0. Therefore if an inclusion-minimal nonempty tight set contains a degree-4 vertex, it is that singleton. Its boundary is the link four-cycle, and z is an apex at every boundary edge. The proposed step "a minimal tight set contains a degree-4 vertex which is not a boundary apex" cannot be true. Fable's Proposition D merely says that such a singleton vertex has two consecutive neighbours outside the singleton, which is automatic. The proposition is not false; its proposed use supplies no contradiction.

## 6. A proved restricted form of G

PROVED-HERE. If T has more than six vertices, no separating triangle, and no chordless five-cycle, every non-root degree-4 vertex has a simple contraction with a pair.

Proof. Euler gives at least six degree-4 vertices, so some are nonroots. At each degree-4 vertex at least one merge is simple. For completeness, if both were non-simple, choose common neighbours y of p,q and z of a,b outside the link. The four-cycle x p y q separates a,b, so the path a z b crosses it and forces z=y. Thus y is adjacent to all four link vertices. Each of the four resulting triangles at y is an actual face because no triangle separates. Together with the four faces at x they close the sphere, making T the octahedron. This contradicts |V|>6. A simple merge cannot lose its pair without the five-cycle in section 3. QED.

This restriction is useful but does not handle the V=11 obstruction. The remaining general problem is a selection argument across crossing four- and five-cycles. The enumerated short-cycle classification is exact; no missing finite list of local colours remains to check. What is missing is a global reason that at least one degree-4 vertex escapes both directions.
