# Proofs

All new results below are PROVED-HERE, T2, unreviewed. The supplied OpenAI manuscript is cited as LIT without a claim of peer review. The disk identity used below is Lemma 4.1, also re-proved in the referee's REWRITTEN-PROP-5-1.md. Notation follows research/BRIEF.md.

## 1. Exact primal dictionary

PROVED-HERE. Fix the primal black root vertex b0. Call its three incident faces root faces. Covers are in bijection with edge subsets S of G satisfying these local conditions:

1. Every black vertex other than b0 is incident with exactly one edge of S; b0 with none.
2. Every non-root face has exactly two boundary edges in S; every root face has none.

The black endpoint of an edge identifies its supplying black triangle in T. Selecting the two incident faces of this edge is precisely selecting the two corners of that triangle. Condition 2 says its dual edge set D has degree two at all nonroots and zero at roots. Hence D is a disjoint union of simple cycles. Conversely any such S gives a 2-factor of B by replacing each dual edge with its two incidence spokes. Alternating around each bipartite incidence cycle decomposes it into two states. Each component has two choices, independently. Therefore S determines exactly 2^c ordered pairs.

There is no prescribed degree at white vertices of G. S is a disjoint union of stars and isolated vertices because every black degree is at most one. In particular S is a forest. G-S usually has white degrees other than two and has degree three at b0; it is not a primal 2-factor.

PROVED-HERE. Write kappa for number of connected components, including isolated vertices. Then

    c(D) = kappa(G-S)-1 = nullity(T[S*]).

To prove the first equality, draw D as c disjoint Jordan curves. Their complement has c+1 regions, by adding the curves one at a time. Each region contains triangles of T. Triangles in a region are connected through sides outside D: a generic path in the region connects interior points, avoids vertices, and crosses only such sides. Thus the triangles of each region are exactly a connected component of G-S. The three isolated roots in the spanning dual subgraph do not separate a region. For the nullity equality, T[S*] has n edges, n+3 vertices, and c+3 components, so its nullity is n-(n+3)+(c+3)=c. Consequently c_min is the minimum number of extra primal components caused by an admissible deletion S. It depends on the root as well as the embedded graph.

PROVED-HERE. Each component cycle is dual to a bond of G, with the bounded shore avoiding b0. The same path argument shows each side of one Jordan curve induces a connected primal subgraph, so the crossed edges form a minimal cut. The c bounded shores are laminar. Contract the components of G-S, retaining S as possibly parallel edges. The resulting multigraph has an underlying simple graph which is a tree: one edge for each separating curve, with a parallel bundle of size equal to that curve's length. This follows inductively by inserting a curve into one region, splitting that region in two. The root component contains b0. These observations give a primal region tree for each cover.

## 2. Unbounded c_min without triangular separators

PROVED-HERE. For every integer m>=2 there is a simple Eulerian triangulation T_m with 3m+2 vertices, no separating triangle, a specified black root, and exactly one cover. That cover has m-2 triangles and one pentagon. Thus

    c_min=m-1,  #TM=2^(m-1),  |V(G_m)|=6m.

Construction. Indices are modulo m. Take vertices A,B,x_i,y_i,z_i. The edges for each i are

    Ax_i, Ay_i, x_i y_i, x_i y_(i-1),
    By_i, Bz_i, z_i y_i, z_i y_(i-1), z_i x_i.

Start with a bipyramid whose equator is x_0,y_0,...,x_(m-1),y_(m-1), and poles A,B. Subdivide every edge Bx_i with z_i and join z_i to y_(i-1) and y_i. This explicitly embeds the graph as a sphere triangulation. The degrees of A,B are 2m, those of x_i,z_i are four, and those of y_i are six. All are even. The 6m faces are exactly

    A x_i y_i, A x_i y_(i-1),
    x_i z_i y_i, x_i z_i y_(i-1),
    B z_i y_i, B z_i y_(i-1).

Every triangle is listed here. Indeed there are no edges between two y vertices, between distinct x vertices, between distinct z vertices, from A to B or z, or from B to x. A triangle at A or B must therefore be one of the listed cap triangles; one with neither pole must contain x_i z_i and one of their two common y neighbours. The same argument works for m=2. Hence no triangle separates. A simple sphere triangulation without separating triangles is 4-connected: a three-vertex cut in a maximal plane graph bounds a separating triangle. Alternatively this last standard characterization can be replaced throughout by the proved no-separating-triangle property requested here.

Color black the faces

    P_i=A x_i y_i, Q_i=x_i z_i y_(i-1), R_i=B z_i y_i.

The other listed faces are white. Root at P_0, so A,x_0,y_0 are roots.

For every i!=0, P_i must select the D edge x_i y_i because A is a root. At every nonroot x_i there are just two black incident faces, P_i and Q_i, so Q_i must select x_i. Every z_i has exactly two black incident faces, Q_i and R_i, so both must select z_i. It follows that Q_i selects x_i z_i for i!=0, while Q_0 selects z_0 y_(m-1) because x_0 is a root. Face R_0 selects Bz_0 because y_0 is a root. The vertex y_(m-1) already has its two D edges from P_(m-1) and Q_0, so R_(m-1) selects Bz_(m-1). These two edges exhaust B's required degree. Therefore every R_i with 1<=i<=m-2 selects y_i z_i.

All choices are forced, and they do give degree two at every nonroot. The components are

    x_i y_i z_i x_i,   1<=i<=m-2,
    B z_0 y_(m-1) x_(m-1) z_(m-1) B.

This proves uniqueness and the cycle count. To prove the TM count without using the conjectured bound, suppose an orientation of this unique cover had cyclic Q_s. Reverse a Q_s cycle in its partner r. This changes the deleted corner on every supplying face while preserving s and both state bijections. It gives a different cover, a contradiction. Thus all 2^(m-1) orientations are tree pairs. Every tree state has one partner, since its opposite edges orient uniquely toward their roots. Hence #TM=2^(m-1).

PROVED-HERE. The absolute leading coefficient for unit white-face weights is 2, independently of m. Each triangular component is the white face x_i z_i y_i, so has weight one. The pentagon encloses exactly the two white faces Bz_0y_(m-1) and x_(m-1)z_(m-1)y_(m-1), and the intervening black face R_(m-1). Its weight is two. The interiors are disjoint. Section 4 now gives coefficient 2. More precisely, up to overall sign and monomial, the integer polynomial is

    (z-1)^(m-2) (z^2-1).

Thus arbitrarily high vanishing order needs neither triangular separators nor a large leading coefficient.

## 3. Parity and flips

PROVED-HERE, restatement with proof. Let C be a D cycle of length h. For its bounded disk let I count interior vertices, B and W black and white faces, and l boundary edges with black face inside. The state bijection gives B=I+l. Euler and side counting give B+W=2I+h-2 and 3(B-W)=2l-h. Substitution gives h=2l+3 and W=B+1. Every cycle is odd, hence

    c(D) = n mod 2,   1 <= c(D) <= floor(n/3).

This holds for every cover, not only minimizers. In particular every change of cycle count under any allowed flip is even. The sign epsilon does not force c modulo four.

PROVED-HERE. A single facial hexagon flip in H_0 changes c by -2,0,or 2. The flip changes precisely three edges of D. Delete those three edges, leaving three path pieces on the affected cycles, and reconnect their six endpoint occurrences with the other three edges. At most three components are involved before and after. The number can therefore change by at most two; the parity result excludes odd changes. Endpoint occurrences are used so the argument also covers adjacent removed edges and zero-length path pieces. This assertion concerns a facial hexagon, not arbitrary essential-cycle lattice moves.

## 4. The lowest coefficient and pointed cuts

PROVED-HERE, using the refereed height-increment and fixed-s cancellation lemmas, rederived here at the algebraic step. Put Omega(s)=sum_w h_s(w) for the fixed integer heights, and

    F(x)=sum_pairs epsilon(r,s) exp(x Omega(s)).

For an undirected cover D, take its all-clockwise pair as reference and write b_D for its second-state Omega. If a_C counts white faces inside C, independent cycle reversal gives

    F_D(x)=(-1)^((n+c)/2) exp(x b_D) product_C (1-exp(x a_C)).

Every a_C is positive by the disk identity. Each factor has a simple zero with first coefficient -a_C. Hence the exact vanishing order of F_D is c and its first coefficient is (-1)^((n-c)/2) product_C a_C. Put q=c_min. All covers of c>q have zero coefficient at degree q. All covers of c=q have the same sign. Therefore

    [x^q] F(x)=(-1)^((n-q)/2) sum_(D:c=q) product_C a_C != 0.

Replacing exp(x) by z gives the same first coefficient at z=1, since exp(x)-1=x+O(x^2). The q-th derivative has the extra factor q!. This normalization matters.

On the other hand, for fixed s with a cyclic Q_s, choose one Q_s cycle using s alone and reverse it in r. The disk identity changes J by plus or minus two, reversing epsilon, while Omega(s) is fixed. Terms cancel. A forest s has its unique partner. Thus the identical F is a signed weighted sum over tree matchings. If there were no tree matchings it would be identically zero, contrary to the displayed coefficient. The minimal cover is a certificate for a nonzero coefficient, not a location where the surviving tree matching must live. The two regroupings partition the same pair set differently.

PROVED-HERE. The absolute coefficient counts covers with the minimum number of cycles, together with an independent choice of a white vertex of G in the b0-free shore of each corresponding bond. Choices may repeat when shores nest. This is a literal bijection with pointed laminar bond families satisfying the local conditions in Section 1: dualize the bonds and retain each white mark, with the inverse given by the dual cycles. In the region tree, a mark for an edge may be any white vertex in the descendant subtree cut off by that edge. Thus the coefficient is a sum of products of descendant white masses. This gives a wholly primal counting interpretation without claiming an unknown bijection to spanning forests or unweighted tree matchings.

PROVED-HERE. No bijection to all unweighted tree matchings can hold in general. In Section 2 the coefficient is 2 and #TM=2^(m-1), unequal for m>=3. For a 2r-prism the coefficient is r-1 while #TM=2, also giving arbitrarily large ratios in the other direction. A bijection involving additional weights or signed objects remains open.

## 5. Counting when there are exactly two covers

PROVED-HERE. Suppose B has exactly two distinct covers D1,D2, with c1,c2 cycles, and let j be the number of component cycles identical as edge sets in both. Then

    #TM = 2^c1 + 2^c2 - 2a,   where a is either 0 or 2^j.

In particular #TM >= 2^min(c1,c2). Equality could occur only if c1=c2=j+1 and a=2^j. This is a necessary condition, not a construction or an assertion that this configuration is possible in a plane instance.

Proof. For fixed s, orient Q_s using a partner. Each component contains at most one root: its edge count is its vertex count minus its number of roots, and connectivity forbids two roots. Components with a root are trees and orient uniquely toward it. Root-free components are unicyclic and have two independent cyclic directions. Thus s has exactly 2^k partners, with k its number of unicyclic components. Different partners give different covers, because s and a cover determine r uniquely. With only two covers available k is zero or one. A state has k=1 precisely when it occurs as second state in both covers; all others occurring in a pair are tree states. Counting pairs proves the first formula.

On a face where the two covers differ, the two selected two-element corner sets have exactly one common corner. A common second state must choose that corner, fixing the orientation of that entire component cycle in either cover. Any D1 cycle containing no changed face is identical in D2. Conversely every nonidentical D1 cycle contains a changed face, so its orientation is forced. The j common cycles are disjoint from all other components in both covers and may each be oriented freely. If the forced choices are consistent they give exactly 2^j common states; otherwise none. This proves the formula for a.

Distinctness gives j<=min(c1,c2)-1. Put q=min(c1,c2). Then 2a<=2^q and 2^c1+2^c2>=2^(q+1), proving the bound. Equality in both inequalities requires exactly c1=c2=j+1 and a=2^j.

PROVED-HERE. If c1!=c2, parity gives max(c1,c2)>=q+2, so #TM>=4*2^q. If c1=c2=q and j<=q-2, then #TM>=3*2^(q-1)>2^q. The remaining equality configuration would have just one noncommon cycle in each cover. Excluding it by planarity would prove strictness in the two-element case. No such exclusion is proved here.

CONJECTURE. The exceptional configuration cannot occur for these planar incidence graphs. Test by recording c1,c2,j,a for all two-element lattices, and seek a Jordan-curve obstruction using the shared second-state spokes. This isolates a smaller obligation than the full strict-inequality conjecture. The census supports strictness but does not replace that proof.
