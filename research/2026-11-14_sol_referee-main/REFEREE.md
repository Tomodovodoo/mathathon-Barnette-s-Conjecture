# Independent referee report

Reviewer: gpt-6.1-sol, 14 November 2026. The mathematical verdict concerns the merged 18-page manuscript, not the author's earlier drafts. I read all eighteen pages as 130 dpi images before opening the TeX or earlier reports. SUMMARY-FROM-MEMORY.md records that first reading. Fingerprints are in code/fingerprints.json. No manuscript file was edited.

Status convention: the audit arguments and deductions below are PROVED-HERE. Counts are COMPUTED only within the ranges stated in code/README.md. Source descriptions are LIT, meaning the identified source says this, not that its proof has been independently certified. No conjectural claim is used to discharge an obligation.

## Audit boundary

C0 is Theorem 1.1: for every finite simple cubic bipartite planar 3-connected graph G and every edge e of G, there is a Hamiltonian cycle avoiding e. The stronger dual induction contract is Theorem 6.2: for every coloured sphere triangulation T, every facial triangle t0, and every side e0 of t0, an acyclic selection contains e0. A coloured triangulation has at least four vertices, is simple, has triangular facial boundaries, and has opposite face colours across every edge.

The proof under audit is only paper/main/barnette.tex, read first in its PDF form. The source papers and earlier reports were used afterwards for transcription and citation checks. They are not replacement routes for a missing step. In particular I do not use the Lean theorem as a premise. Its DIFFERENCES.md and LESSONS-FOR-EXPOSITION.md identify obligations that deserve attention, not facts that make the exposition automatically correct.

Accepted background consists of the Jordan curve theorem for embedded cycles; Euler's formula for a connected sphere graph; elementary plane dual construction and vertex rotation order; integral max-flow/min-cut for a finite integral network; elementary finite graph theory and polynomial algebra. Elementary graph facts include tree edge counts, uniqueness of paths in a tree, a connected 2-regular graph being a cycle, an even nonempty edge set containing a cycle, and the even intersection of a cycle with a cut. I check connectedness before each Euler application. I do not accept the disk identity, the pair-to-good-state assertion, tree recovery, or the restriction-to-a-disk claim as background.

The proof of C0 has no dependency on the historical citations in Section 1 or the off-route statements in Section 7. SOURCES.md records every checked numbered citation and distinguishes unavailable historical originals.

## Obligation graph

Every displayed route is primary. The manuscript supplies one route per major claim. There is no sufficient alternative route and no diagnostic route is counted as support. Cases A0 and B0 are both required by the induction, rather than alternatives that could excuse a failed case.

```text
C0 <- R0 AND C1, C2, C3, O1
C1  Lemma 2.1, dual is a coloured triangulation
   <- R1 AND O2, O3, O4
C2  Theorem 6.2, prescribed acyclic selection
   <- R2 AND O5, A0, B0
A0  no separating triangle case
   <- R3 AND O6, C17, C16, C7
B0  separating triangle case
   <- R4 AND C18, O7, O8, O9
C3  Proposition 2.6, Hamiltonian complement and two induced trees
   <- R5 AND C4, C5, O10, O11
C4  Lemma 2.2, cyclic face boundaries imply connectedness
   <- R6 AND O12
C5  Lemma 2.5, cycle/forest duality and tree/cotree
   <- R7 AND O13, O14
C7  Proposition 3.9, good state gives a prescribed acyclic selection
   <- R8 AND C8, C6, C10, O15, O16
C8  Lemma 3.6, tree Y_s and one selected side per face
   <- R9 AND C9, C5, C4, O17, O18
C9  Lemma 3.5, good iff S_s spanning tree
   <- R10 AND O19
C6  Lemma 3.8, W=B+1 and h=2 ell+3
   <- R11 AND C4, O20, O21, O22, O23
C10 Lemma 3.7, outdegree principle
   <- R12 AND O24
C11 Lemma 4.2, partner structure and unique partner of a good state
   <- R13 AND C10, O25
C12 Lemma 4.3, two pair reversals
   <- R14 AND C11, O26
C13 Lemma 4.4, sign changes and exact sign formula
   <- R15 AND C6, O27, O28
C14 Lemma 4.5, fixed-s cancellation
   <- R16 AND C12, C13, C11, O29
C15 Lemma 4.6, height increment and positive cycle weight
   <- R17 AND C6, C5, O30, O31, O32
C16 Proposition 4.8, pair implies good state
   <- R18 AND C14, C13, C15, C19, O33, O34
C19 Lemma 4.7, finite difference formula
   <- R19 AND O35
C17 Proposition 5.2, pair without separating triangles
   <- R20 AND O36, O37, O38, O39, O40, O41
C18 Lemma 6.1, smaller valid coloured pieces
   <- R21 AND C4, O42, O43
```

Equation 2.3 is O10 and is shared by several branches. The two uses of bijectivity are not interchangeable. O22 uses both injectivity and surjectivity of a state to count the interior; O25 uses the first state's bijectivity to orient Q_s. No cycle in this graph discharges itself. In particular C6 does not use pairs, C16 does not use recovery, and recovery does not use the existence proof.

## Findings, ranked by severity

### F1. ERROR, off the theorem route: the displayed integer polynomial is Laurent

Location: Section 4, Remark 4.10, source line 751. Status PROVED-HERE, with COMPUTED witness in code/examples.json.

The signed heights can be negative. After fixed-s cancellation, the running example still gives

```text
sum eps z^omega = z^-4 - z^-3 + z^-2 - z^-1 - z + z^3.
```

Thus the expression called an integer polynomial is not one with the manuscript's definition of omega. This is also a transcription mismatch. The unsigned source's Lemma 5.1, PDF page 8, explicitly normalizes its incidence weights into [0,6n], and its Theorem 5.2 uses those nonnegative weights. The finite-difference proof in the merged paper is unaffected. A Laurent polynomial has a perfectly valid formal expansion at z=1, and the generalized binomial coefficient gives exactly the stated coefficient. Alternatively one could shift all exponents by a common sufficiently large integer. The vanishing lower moments make that shift harmless at degree m.

Exact replacement: E1 in EDITS.md, reproduced from a uniqueness-checked old/new pair. It distinguishes the source's nonnegative weights from the present signed heights, calls the latter expression Laurent, and specifies expansion at z=1. This is a terminology and attribution error with an explicit counterexample, not a break in C16.

### F2. GAP, off the theorem route: structural assertions in the necessity examples

Location: Section 7, paragraph headed "Why each hypothesis is needed", lines 906 and 907. Status PROVED-HERE for the repairs; COMPUTED for the two named finite graphs.

The paragraph labels its statements proved or literature, but neither proves nor cites the 3-connectivity of the 11-vertex incidence graph or the 2-connectivity of the 26-vertex construction. The constructions are correct. The missing support concerns their structural properties, not their non-Hamiltonicity once those properties are granted. The 5-versus-6 bipartition and the deletion of two vertices leaving three components supply the two non-Hamiltonicity arguments.

E6 supplies a direct proof for the radial graph of the triangular bipyramid. With equator a,b,c and apices u,v, its six faces are uab,ubc,uca,vab,vbc,vca. With at most one face centre removed, each surviving original edge retains a two-edge incidence path through its other face centre. Removing at most two original vertices leaves the bipyramid connected, and every surviving face centre has a corner. With two centres removed, no original vertex is removed, and at most one original edge loses both incidence paths, since two faces share at most one edge. The bipyramid has no bridge. This proves the required connectivity after any two deletions.

E7 supplies the missing deletion check for the 26-vertex graph. A cube minus an edge is 2-connected. Deleting one new vertex leaves all copies joined through the other. Deleting a vertex in one copy leaves that copy attached to at least one new vertex, and the other copies join the new vertices. The two new vertices themselves form a cut. The proposed replacements contain the full arguments and do not invoke new literature. No C0 dependency uses these examples.

### F3. IMPRECISION: the polynomial remark suppresses its hypothesis

Location: Section 7, "The polynomial behind the count", line 918. Status PROVED-HERE; COMPUTED counterexample to an unconditional reading in code/supplement.json.

"Proposition 4.8 is the statement F != 0" must retain "when a pair exists". F is zero at obstructed roots. The saved 9-vertex witness has states but no pair, with maximum flow 11 instead of 12. The proposition itself is correctly conditional, so this is not a defect in its proof. E2 restores the hypothesis and the common-leading-sign clause needed when reading off nonvanishing from the linear substitution.

### F4. IMPRECISION: the perfect-matching proof must start with the good-state direction

Location: Section 7, "Which Hamiltonian cycles arise", lines 896 and 897. Status PROVED-HERE.

For arbitrary C, Y_{s_C} is not necessarily a tree. The proof's first sentence calls it a tree before explicitly assuming that s_C is good. The implication intended is sound. If s_C is good, both P and P_{s_C} are perfect matchings of the tree Y_{s_C}. Two different perfect matchings have an alternating cycle in their symmetric difference, so a tree has at most one. Hence they coincide. Conversely, recovery orients P_s minus e0 with one outgoing edge at every nonroot and none at the roots. In a rooted tree this must be the orientation towards its root. Lemma 3.1 therefore recovers s itself. This proves both the equivalence and injectivity of the forward map. E3 writes these scopes and the converse explicitly. The six-cycle running example and the prism distinction both pass independent enumeration.

### F5. IMPRECISION: state the range behind "smallest examples"

Location: Section 7, no-separating-triangle remark, line 908. Status COMPUTED, all face rootings of all 15 generated classes with at most 12 vertices.

The computation label gives a graph order but no search range behind minimality. E5 gives the range of the present exhaustive check. Minimality also has a short PROVED-HERE explanation: every coloured simple triangulation has minimum degree at least four and thus at least six vertices; the two pieces at a separating triangle each have at least six, so the whole has at least 6+6-3=9 vertices. The double octahedron attains that order. The count statement is true.

### F6. IMPRECISION: "not constructive" overstates what is being compared

Location: Remark 4.10, line 753. Status LIT for the source's explicit algorithm, PROVED-HERE for the distinction.

The unsigned source does turn its cancellation into a deterministic marked walk in Theorem 5.3. The immediate polynomial nonvanishing calculation does not itself give an efficient construction. E8 says precisely that. Section 7 already distinguishes the existence argument from the source's enumeration algorithm, so this correction makes the two passages consistent. It does not assert that a polynomial-time algorithm is known.

### F7. TYPO: Table 2 does not list all twelve states

Location: Section 1, "The example", line 100. Status COMPUTED.

The table lists eight pairs and describes their second states, not the twelve states. Only seven different states even occur as second states of pairs. E4 changes the sentence to say that all eight pairs are listed. No numerical count is wrong.

All exact replacement text is in EDITS.md, E1 through E8. Its generator checks that every old string occurs exactly once. No edits are proposed to a core theorem or lemma statement.

## Exact replacement texts

These are the exact proposed new strings. EDITS.md supplies their unique old strings. Status PROVED-HERE for mathematical repairs and COMPUTED for the added range.

### E1 for F1, source line 751

```tex
The unsigned manuscript \cite{constructive2026} uses nonnegative integer incidence weights to obtain an integer polynomial of this form.
For our signed heights, $\sum\eps(r,s)z^{\omega(s)}$ is an integer Laurent polynomial.
Its expansion at $z=1$ has coefficient $\sum\eps(r,s)\binom{\omega(s)}{m}=\Sigma/m!$ in degree $m$, where the binomial coefficient has its usual polynomial meaning also for negative integers $\omega(s)$; the lower moments vanish by Lemma~\ref{lem:difference}.
```

### E2 for F3, source line 918

```tex
When a pair exists, Proposition~\ref{prop:good} proves $F\neq0$.
This can also be read off at $w_{t,v}=1+\xi\kappa(t,v)$ with $\kappa=\sum_y\kappa_y$: each factor is then $\xi L(C)+O(\xi^2)$, and the classes with the fewest cycles have a common leading sign.
```

### E3 for F4, source line 896

```tex
If $s_C$ is good, the complement $P$ of $C$ avoids $S_{s_C}$, because its side in each $t\in A$ contains $s_C(t)$ and its side in $t_0$ is $e_0$.
Thus $P$ and $P_{s_C}$ are perfect matchings of the tree $Y_{s_C}$, and a tree has at most one perfect matching, so $P=P_{s_C}$.
Conversely, when $C$ comes from a good state $s$, directing $P_s\setminus\{e_0\}$ out of $s(t)$ gives outdegree one at each nonroot and zero at each root.
On each rooted tree this is its orientation towards the root, so Lemma~\ref{lem:selections-give-states} recovers $s_C=s$.
This also proves that different good states give different cycles.
```

### E4 for F7, source line 100

```tex
It has $12$ states and $8$ pairs; all eight pairs are listed in Table~\ref{tab:pairs}.
```

### E5 for F5, source line 908

```tex
Two octahedra glued along a face ($9$ vertices) give the smallest examples, with a pair for one choice of $t_0$ and none for another of the same colour (computed over every face rooting of every Eulerian sphere triangulation with at most $12$ vertices).
```

### E6 for F2, source line 906

```tex
The incidence graph of the vertices and faces of the triangular bipyramid has classes of sizes $5$ and $6$, so it has $11$ vertices and no Hamiltonian cycle.
It is planar by drawing each face centre joined to its three corners.
Here is also a check of $3$-connectivity.
The bipyramid has equatorial vertices $a,b,c$, apices $u,v$, and faces $uab,ubc,uca,vab,vbc,vca$.
Deleting at most two of its five vertices leaves a connected graph, as is seen directly from the equatorial triangle and the two apices.
If at most one face centre is deleted from the incidence graph, every surviving bipyramid edge is still represented by a two-edge path through one of its incident face centres, and every remaining face centre has a surviving corner.
If two face centres are deleted, no original vertex is deleted, and at most one bipyramid edge loses both its incident face centres, since two faces share at most one side.
The bipyramid stays connected after deleting one edge, and the surviving face centres all attach to it.
Thus the incidence graph stays connected after any two vertex deletions.
```

### E7 for F2, source line 907

```tex
The result is cubic, bipartite and planar with $26$ vertices.
To check $2$-connectivity, each cube with an edge removed is $2$-connected and joins the two new vertices by a path.
Deleting a new vertex leaves the three copies connected through the other new vertex.
Deleting a vertex of a copy leaves that copy connected to at least one new vertex, while the other two copies still connect the new vertices.
Deleting both new vertices leaves three components, so the graph is $2$-connected but has no Hamiltonian cycle.
```

### E8 for F6, source line 753

```tex
These nonvanishing arguments do not by themselves give an efficient construction.
```

## Verification of the core obligations

All deductions in this section are PROVED-HERE. Computational corroboration is COMPUTED, with the exact limits below. These paragraphs explain discharged nodes rather than silently supply alternative routes.

**Dual and target, Sections 2 and 3.** Lemma 2.1's edge-cut argument is valid: on either shore of a cut of size at most two, cubicity and simplicity force at least three vertices. Deleting its at most two boundary endpoints therefore leaves a vertex on that shore and all vertices on the other, contradicting 3-connectivity. A dual loop or parallel pair is a Jordan curve crossing the specified primal edges once, so each crossed edge has endpoints on opposite sides and both shores are nonempty. No separate simplicity assumption on the dual is smuggled in. Cubicity makes a dual facial walk have length three; simplicity turns it into a triangle. The bipartition supplies the face colouring. Euler on the connected G gives the dual vertex count.

Lemma 2.2's proof is correct with the ordinary meaning of a face boundary as its full topological boundary. An isolated component would force a face with a disconnected or noncyclic full boundary, so it is not a counterexample. The finite embedding gives a small neighbourhood of a point of K that meets no other component. Its incident face boundaries belong to K. Thus both sets in the proof are open. Applying this to T justifies the later global Euler count. The edge-side count gives k faces of each colour, 3k edges, and k+2 vertices; hence |A|=|X|=k-1=n.

Lemma 2.5 correctly treats the dual cut induced by a primal cycle. In its converse, membership changes an even number of times in the rotation at every vertex. Connectivity of M makes the boundary edge set nonempty, so the all-even argument supplies a cycle in N. Euler applies to connected M for the tree/cotree count. The contraction sentence after the proof is also valid: contracting a larger tree containing N gives a connected dual subgraph contained in M* minus N*. Proposition 2.6 has k selected edges and k+2 vertices, hence two forest components. Adding an omitted edge whose ends are in one component makes a cycle; its dual cut would meet the Hamiltonian complement exactly once, impossible. This proves inducedness, not just connectivity.

Lemma 3.1 uses that inducedness to put a,b together and c apart. Deleting e0 splits the first tree into two. Tails of its orientation to roots give an injection into X, and every nonroot is a tail, giving surjection. Distinct black faces own distinct sides because every edge has exactly one black face. This is also why Q_s has n distinct edges. S_s has n+2=|V|-1 edges: its extra root sides belong only to t0 and are absent from Q_s. Lemma 3.5 follows because adding ac and bc to a forest makes no cycle exactly when all three roots are in different components. There are exactly three components before adding them.

For Lemma 3.6, duality makes Y_s a tree on 2k faces, with 2k-1 edges. A nonroot black face has degree two and t0 degree one. Rooting gives one child per black face. A white face is its black parent's sole child, so gets exactly that selected side. A further selected side in the same white face would require the same black-white pair to share another side. The preceding two-common-sides argument excludes this using simplicity and at least four vertices. The side in each nonroot black face is at s(t), and the root's selected side is e0.

**Disk and acyclicity.** The topology paragraph at lines 383 to 388 is enough. First define the restricted graph, then identify its faces without assuming connectivity: its complement inside Z equals the complement of T there, since every vertex and edge of T in the closed disk was retained. A face of T cannot cross Z. Thus the inner complementary regions are exactly the original triangular faces. The other region is the whole open outside disk, with boundary Z. Lemma 2.2 now proves the restricted graph connected. This is not the circular argument "Euler holds because this is a triangulated disk". The same reasoning applies to the other closed disk if it is needed. In the dual, faces on each side are connected by generic paths in that open disk, crossing edges away from finitely many vertices. The manuscript does not separately need this stronger dual-side statement for its Euler calculation. This explains why the Lean's bond proof needed more intermediate lemmas than this geometric presentation.

A vertex strictly inside Z has a neighbourhood inside its disk; an incident face cannot cross the cycle. This is exactly the no-pinched-interior-vertex property needed in the state count. A boundary vertex may meet both sides, and the manuscript handles it through its unique outgoing chosen edge. Roots are not on a chosen-side cycle because they have outdegree zero, and they are outside because t0 is the outer face. These observations verify all uses of the disk, including the fact that e0 cannot be an interior selected side in Proposition 3.9.

For Lemma 3.8 the connected restricted graph has V=I+h, F=B+W+1 and E=[3(B+W)+h]/2. Euler yields B+W=2I+h-2. Signed sides give 3(B-W)=2 ell-h. The map from inner black faces to their state corners is injective; it hits every strictly interior vertex by surjectivity and the no-pinch property. At a boundary vertex, its outgoing cycle edge must belong to the unique face assigned that vertex, so exactly ell boundary vertices are hit. Thus B=I+ell. Substitution gives h=2 ell+3 and W-B=1, with W at least one. Both halves of bijectivity are essential here.

Lemma 3.7 uses distinct tails along a cycle and the edge count q-gamma in a component. The bounds q-1 <= q-gamma give gamma <= 1 and the stated tree or unicycle alternatives, including isolated vertices. In Proposition 3.9, a hypothetical cycle of P0 is therefore directed. The selected sides match inner faces either to each other or across Z. Exactly ell black and h-ell white faces are matched across Z. The remaining equal numbers force B-ell=W-(h-ell), or W-B=h-2 ell=3, contradicting W-B=1. The resulting components each contain one root, and e0 joins two different components. Every step is present in the manuscript.

**Pairs, signs and both reversals.** Lemma 4.2 orients Q_s from r(t) to the third corner, giving precisely one outgoing edge at every nonroot and none at roots. A component without a root is unicyclic; one with a root is a tree. A good state has a partner by directing each tree towards its root, not merely at most one partner. The tails use every nonroot once and each edge is owned by a unique face, so the resulting map is a state and differs from s. The tree orientation is unique.

For D, r and s give one incoming and one outgoing edge at every vertex of X. Different faces cannot supply the same undirected edge because it has one black owner. There are no loops and no 2-cycles, so the components are simple cycles of length at least three. D-cycles and Q-cycles are both cycles of chosen sides for the first state r, making the disk identity applicable in both places. Reversing a Q-cycle changes only r on its faces; its old tails and heads are the same vertex set, so it remains a bijection and the operation undoes itself. Reversing a D-cycle exchanges two bijections on that same vertex set. Table 1 correctly records what is preserved in each operation.

The local delta convention is consistent. In a black face r,s,u, the directions r to s, s to u, u to r have the same sign. Hence delta(u,s)=-delta(r,s), and delta(s,r)=-delta(r,s). Each reversal changes one factor for every edge of the affected cycle; its odd length makes the product flip. Counterclockwise traversal has black-on-left count ell, hence delta sum 2 ell-h=-3; clockwise traversal has sum +3. An h-cycle consequently has [h+3]/2 negative signs when counterclockwise and [h-3]/2 otherwise. Summing gives [n-3c]/2+3c+ negative signs. Since all c lengths are odd and sum to n, n=c modulo two. The parity difference from [n+c]/2+c+ is -2c+2c+, even. This proves the displayed epsilon formula exactly, with no orientation sign omitted.

Lemma 4.5 chooses its Q-cycle using s alone, so the second application uses the same cycle. The involution is fixed-point-free. States without partners contribute an empty sum; good states have exactly one partner. These points justify the second displayed equality, not just cancellation of some partners.

**Heights and finite differences.** Heights are well-defined after paths are fixed. They are not defined as path-independent absolute quantities, and no such claim is needed. Connectedness of the dual follows from Lemma 2.5 with N empty. A simple face path has neither a repeated face nor an entry and exit through the same side, because two faces share at most one side. Its endpoints are white y and black t0, and no face in A is an endpoint. There is no state corner at the root face and none needs to be evaluated there. A cycle of D contains no root edge and t0 is outside it.

For the local sign check in Lemma 4.6, direct the new counterclockwise edge from s to r. If t is on its left and the path exits t across that edge, entry through ru turns around r with sign +, whereas entry through su turns around s with sign -. In either case kappa(r)-kappa(s)=+1. If t is on the right, entry is across the cycle edge; exits through ru or su give respectively the same +1 difference. Reversing travel changes the sign. The third-corner turn uses neither endpoint and gives zero. Every crossing is counted at its unique black face exactly once. Exits minus entries of the inside along a path ending outside equal the inside indicator of its starting face. This proves the height jump, independent of the chosen path. Summing over all white faces gives precisely their number inside C, not their signed black-white difference. It is positive by Lemma 3.8. Disjoint cycles use disjoint black faces, so their height changes add, even for nested cycles.

In Lemma 4.7, reduce powers of Boolean variables by x_i^j=x_i for positive j. A monomial involving fewer than all c variables cancels in the signed sum. When m=c, the only surviving term uses every variable once; it occurs c! times with coefficient product L_i and signed sum (-1)^c. This includes c=m=0 with the usual empty-product convention. All sums are finite and require no analytic convergence.

An undirected D contains exactly one side per face of A. Once those sides are fixed, an orientation change of exactly one incident edge at a vertex would repeat that vertex as an r-value or s-value. Thus changes propagate around the entire cycle. Conversely each cycle reversal is legal. The class is exactly 2^c pairs. For m the minimum number of cycles, classes with c>m vanish in the mth moment; classes with c=m contribute

```text
(-1)^((n+m)/2) (-1)^m m! product L_i
 = (-1)^((n-m)/2) m! product L_i.
```

The exponents differ by 2m. At least one such class exists, every L_i is positive, and all have the same sign. This proves nonvanishing and then existence of a good state through fixed-s cancellation. The exact sign and the minimum, rather than an arbitrary cycle count, are both necessary in this calculation.

**Flow and gluing.** Capacities 2,1,2 and equality |A|=|X| force degree two on both sides of the incidence graph when the flow value is 2n. Integral flow prevents fractional incidences. Alternation around even components gives two disjoint perfect matchings. For a source-side S, each face is placed independently to pay min[2,|V(t) intersect S|]. The cut formula is correct.

For U=V minus S, including the roots, the contribution from a face with j corners in U is 2-max[0,j-1]. The latter shortfall is its induced-edge count minus one when j=3. Removing the outer face's three sides and one black-face count gives the exact expression 2n-[e(U)-3]+[b(U)-1]. Comparing with 2|S| gives e(U)-b(U)<=2|U|-4. Faces cannot span two induced components because their corners are pairwise adjacent.

The root component has at least three vertices. At order three it has three edges and one black face, giving equality. Other components of order at most three satisfy the weaker bound by simplicity. For a component of order at least four, boundary walks have length at least three. A triangular boundary is a simple triangle. Its facial side is a whole side of that Jordan curve, and the fourth component vertex is on the other side. No separating triangle therefore makes that facial side an original face. Conversely every original face with all corners in the component stays a face of the component. This is the one use of no separating triangle.

In larger regions, internal original edges cancel in opposite colour pairs, including bridge incidences and other components lying within the region. Thus 3 bal(F) is a sum of d_F signs. For d=4, evenness and divisibility force zero; for d=5, the signed sum is plus or minus three; for d>=6, d/3<=d-4. Therefore bal<=d-4. Global colour balance gives f_white-f_black=sum bal. Substitution in 2q=4f-[f_black+f_white]+sum[d-4] gives 2q>=4f-2f_black. Euler p-q+f=2 now yields q-f_black<=2p-4. All the required component bounds follow.

Lemma 6.1's signed boundary sum has three terms and is divisible by three, so all have the same sign. The cap must have the other colour. Restricting to a closed disk and adding that cap leaves triangular boundaries; the face-identification reasoning used for C6 and Lemma 2.2 gives connectivity. The graph is a simple subgraph, has an interior vertex, and omits an interior vertex on the other side. Both pieces are valid smaller inputs. The nonseparating case supplies the base of strong induction; no nonexistent four-vertex coloured triangulation is required.

The root face lies wholly on one side of a separating triangle, even if it shares a side with it. P1's cap selects one side e'. Applying the induction statement to T2 with its cap and e' is legitimate regardless of the cap's colour. Both selections agree on all three boundary sides. The union has one side per original face. By Proposition 2.6, in either piece x,y are together and z apart when e'=xy, and the only path between two boundary vertices is xy itself. A cycle using both pieces would give a path of length at least two through the strict interior of T2 between two distinct boundary vertices. Distinctness follows from the simplicity of the cycle and its not being contained in T2. This contradicts the boundary-path property. The union is acyclic and retains e0. C0 then follows by the already proved dual complement result, with e in P*.

## Examples, citations and comparison material

COMPUTED. code/check.py imports no project proof implementation. Only plantri is reused for generation. Its generated rotation systems, stderr counts, executable hash and all commands are recorded. All 15 unrooted Eulerian triangulations of orders at most 12 were checked at every face root, including both colour choices, for 262 rootings. There are no orders 4 or 5 because minimum degree is four and the sphere triangulation count excludes those orders. The combined run adds the running example, one repeated cube root, and one repeated prism root, giving the 265-root totals in code/census.json. It checks every state, pair, arbitrary chosen-side system, selection, all root-containing density subsets, and all compatible gluing pairs for each generated separator. Generic corner-weight evaluations also verify the multivariate polynomial identity at all 262 roots. Exact supplementary totals are in code/supplement.json.

These are exhaustive rooted-instance checks, not an enumeration of every unrelated plane graph M or every abstract edge subset N in the general duality lemma. Its unrestricted statement was checked by proof above. The height checks use the specified shortest paths at every rooting; the local proof checks arbitrary simple paths. The finite-difference lemma was checked algebraically and also on 560 exact integer instances with c up to six, including negative and zero increments. No universal assertion is inferred from the computations alone.

COMPUTED. The running example has 13 vertices, 22 faces, 33 edges, 11 faces of each colour, 12 states, 8 ordered pairs, and 6 good states. code/examples.py verifies both named states against every printed face column; Q_alpha's sole cycle; all three Q_beta components; the two P_beta components; both D cycles and their directions; all five Figure 5 counts; the three changed entries in the cancellation figure; the face path and both heights in Figure 9; all eight Table 2 rows, with their signs, weights, goodness and alpha/beta labels; class sizes and weights; the signed moments 0,0,18; and every avoiding cycle by perfect-matching enumeration and a connected-complement test. It also checks the cube's exact listed selected edges and vertex sets, the prism counts 3 states and 2 good states with avoiding counts 4,2,2 for the three prescribed sides, the 11-vertex and 26-vertex necessity examples, and the smallest separator example. There is no numerical discrepancy.

LIT comparison. I read the requested notes after the independent PDF pass. The face-path proof adopts the simplification in fable_review-draft-B, replacing the spoke isotopy in astra's REWRITTEN-PROP-5-1 rather than omitting its job. The product sign and linear polynomial agree with fable_referee-determinants/SIGNIFICANCE.md. The density translation, exact pair criterion, gluing and recovery characterization agree with sol_referee-structure/INTEGRATION.md. The merge DECISIONS.md accurately describes these adoptions. Its assertion that the disk repair closes the earlier problem is supported by the independent argument above. NOTATION.md has harmless local reuse of c as a root and a cycle count, but neither use is ambiguous in a mathematical assertion. The author's AUDIT.md reaches the same theorem verdict. I did not use that agreement to discharge a node.

LIT citation check. OpenAI Theorem 1.1 and Corollaries 7.1 and 7.2, Gorsky-Steiner-Wiederrecht Theorems 4.3 and 4.16, and the unsigned Theorem 1.2 all have the cited numbers and the required statements in the held PDFs. OpenAI Lemma 5.3 and Section 5.3, Li Sections 4 and 6 and Appendix C were opened and checked for the attributed constructions. Hertel Corollary 3 and Alt-Payne-Schmidt-Wood Lemma 5 were absent from papers/ but a final repository-wide search found both PDFs in the history-literature research folder. I opened their original statements and rendered pages: Hertel page 7 has exactly the universal edge-avoidance equivalence; Alt et al. pages 3 and 4 have the two-permeating-induced-trees equivalence. Alt et al. Section 5, pages 8 through 10, supports the cut-reduction attribution. All numbered external citations in the merged manuscript are therefore verified. SOURCES.md gives paths and scopes. The history source also holds Brinkmann-Goedgebeur-McKay, whose Theorem 1.1 and Section 4 confirm the 50-vertex minimum and the 90-vertex computation range, and Schnieders, whose Corollary 1.13 confirms the face-size-eight assertion.

## Dependency table

All discharged entries have PROVED-HERE status as audit conclusions, except named background theorems accepted at the stated boundary. Claim nodes use "major claim"; each obligation has exactly one of the skill's classifications. R numbers refer to the graph above.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Every specified G,e has an avoiding Hamiltonian cycle | root | R0 | root | C1,C2,C3,O1 | discharged |
| C1 | Dual of specified G is a coloured triangulation | C0 | R1 | major claim | Lemma 2.1, O2-O4 | discharged |
| C2 | Every coloured T,t0,e0 has a prescribed acyclic selection | C0 | R2 | major claim | Theorem 6.2, A0,B0,O5 | discharged |
| A0 | Nonseparating induction case | C2 | R3 | major claim | O6,C17,C16,C7 | discharged |
| B0 | Separating induction case | C2 | R4 | major claim | C18,O7-O9 | discharged |
| C3 | Acyclic selection gives Hamiltonian complement and two induced trees | C0,B0 | R5 | major claim | Proposition 2.6 | discharged |
| C4 | Cyclic full face boundaries imply connectivity | C3,C8,C6,C18 | R6 | major claim | Lemma 2.2, O12 | discharged |
| C5 | Cycle/forest duality and tree/cotree | C3,C8,C15 | R7 | major claim | Lemma 2.5, O13,O14 | discharged |
| C6 | Chosen-side cycle has W=B+1 and h=2 ell+3 | C7,C13,C15 | R11 | major claim | Lemma 3.8, C4,O20-O23 | discharged |
| C7 | Good state gives prescribed acyclic P_s | A0 | R8 | major claim | Proposition 3.9 | discharged |
| C8 | Y_s is a tree and child selection takes one side per face | C7 | R9 | major claim | Lemma 3.6 | discharged |
| C9 | Good state iff S_s is a spanning tree | C8 | R10 | major claim | Lemma 3.5, O19 | discharged |
| C10 | Outdegree principle, directed cycles and component counts | C7,C11 | R12 | major claim | Lemma 3.7, O24 | discharged |
| C11 | Pair orients Q_s; good iff acyclic; good has unique partner | C12,C14 | R13 | major claim | Lemma 4.2 | discharged |
| C12 | Q- and D-reversals give pairs, with required involution | C14 | R14 | major claim | Lemma 4.3 | discharged |
| C13 | Both sign flips; n=c mod 2; exact epsilon formula | C14,C16 | R15 | major claim | Lemma 4.4 | discharged |
| C14 | Cancellation for fixed s and reduction to good states | C16 | R16 | major claim | Lemma 4.5 | discharged |
| C15 | Height increment equals inside indicator; L=#white>0 | C16 | R17 | major claim | Lemma 4.6 | discharged |
| C16 | A pair implies a good state | A0 | R18 | major claim | Proposition 4.8 | discharged |
| C17 | No separating triangle implies a pair | A0 | R20 | major claim | Proposition 5.2 | discharged |
| C18 | Capped pieces are smaller valid coloured triangulations | B0 | R21 | major claim | Lemma 6.1 | discharged |
| C19 | Signed finite difference of degree m<=c | C16 | R19 | major claim | Lemma 4.7 | discharged |
| O1 | e0 in P implies e in P* and hence omitted | C0 | R0 AND | definition | Dual-edge crossing definition | discharged |
| O2 | G has no edge cut of size <=2 | C1 | R1 AND | algebraic/logical step | Cubic simple shores and 3-connectivity | discharged |
| O3 | A dual loop or parallel pair gives such a nonempty cut | C1 | R1 AND | algebraic/logical step | Jordan separation and crossing property | discharged |
| O4 | Dual faces triangular, vertex count >=4, opposite face colours | C1 | R1 AND | algebraic/logical step | Cubicity, simplicity, Euler on G, bipartition | discharged |
| O5 | Strong induction cases exhaustive and well-founded | C2 | R2 AND | algebraic/logical step | Separating triangle or none; O43 | discharged |
| O6 | Face colours may be exchanged to make t0 black | A0 | R3 AND | definition | Selection does not depend on colours | discharged |
| O7 | Induction applies to both pieces, second with cap,e' | B0 | R4 AND | side condition | C18 and smaller orders | discharged |
| O8 | P1 and P2 agree on all shared triangle sides | B0 | R4 AND | algebraic/logical step | Cap selects exactly one common prescribed side | discharged |
| O9 | Agreed selections unite without a cycle | B0 | R4 AND | algebraic/logical step | C3 induced trees and boundary path argument | discharged |
| O10 | k faces per colour, 3k edges, k+2 vertices; n=k-1 | C3,C9,C17 | R5 AND | algebraic/logical step | Signed side count and Euler after C4 | discharged |
| O11 | Complement degree two and connected; inducedness via cut parity | C3 | R5 AND | algebraic/logical step | C5 and cycle/cut parity | discharged |
| O12 | Component plus its incident full faces is open and closed | C4 | R6 AND | algebraic/logical step | Finite embedding, cyclic full boundaries, sphere connected | discharged |
| O13 | A Jordan cycle separates dual faces exactly across its edges | C5 | R7 AND | named theorem | Jordan theorem, dual construction; both sides nonempty | discharged |
| O14 | Nonempty boundary is even; tree complement has F-1 edges | C5 | R7 AND | algebraic/logical step | Rotation order, M connected, Euler on M | discharged |
| O15 | Interior selected-face matching forces B-ell=W-(h-ell) | C7 | R8 AND | algebraic/logical step | C8, chosen cycle sides, colour pairing | discharged |
| O16 | e0 not interior; forest P0 has one root per component | C7 | R8 AND | side condition | Roots outside, C10 outdegrees | discharged |
| O17 | Black degrees in Y_s are 2 off root and 1 at root | C8 | R9 AND | algebraic/logical step | Unique black edge ownership; S_s definition | discharged |
| O18 | Exactly one side chosen in each white face | C8 | R9 AND | algebraic/logical step | Parent/child uniqueness; faces share <=1 side | discharged |
| O19 | n+2 distinct edges in S_s; extra root edges join three trees | C9 | R10 AND | algebraic/logical step | Edge ownership, root forest definition, O10 | discharged |
| O20 | Restricted graph's faces are inner triangles and one outside disk | C6 | R11 AND | side condition | Closed-disk restriction and Jordan theorem | discharged |
| O21 | Euler and signed sides give two disk counts | C6 | R11 AND | named theorem | Euler after C4,O20; internal sides cancel | discharged |
| O22 | State bijection counts B=I+ell | C6 | R11 AND | algebraic/logical step | Both halves of bijectivity, no pinch, unique outgoing side | discharged |
| O23 | Roots are outside chosen-side cycle | C6 | R11 AND | side condition | Zero root outdegree, outer face incident to roots | discharged |
| O24 | Cycle tails distinct; component edges=q-gamma | C10 | R12 AND | algebraic/logical step | Outdegree <=1 and connectivity edge bound | discharged |
| O25 | Partner's tails orient every Q_s edge and exhaust X | C11 | R13 AND | definition | State bijection and r(t)!=s(t) | discharged |
| O26 | Cycle reversal permutes assigned vertex set bijectively | C12 | R14 AND | algebraic/logical step | Equal tail/head sets, third corner distinction | discharged |
| O27 | Local delta flips under both exchanges | C13 | R15 AND | algebraic/logical step | Cyclic order in a black triangle | discharged |
| O28 | D covers X by distinct simple directed cycles | C13 | R15 AND | algebraic/logical step | Two bijections, distinct edge owners, simplicity | discharged |
| O29 | Q-cycle chosen using s only | C14 | R16 AND | side condition | Fixed ordering on cycles | discharged |
| O30 | Simple face paths exist and turns are defined away from endpoints | C15 | R17 AND | side condition | Connected dual, distinct shared sides, endpoints y,t0 | discharged |
| O31 | Local kappa difference is signed crossing indicator | C15 | R17 AND | algebraic/logical step | Four entry/exit cases, checked above | discharged |
| O32 | Path's exits minus entries equals start's inside indicator | C15 | R17 AND | algebraic/logical step | O13; path ends outside at t0 | discharged |
| O33 | Fixed undirected D class is exactly its 2^c orientations | C16 | R18 AND | algebraic/logical step | One edge per face; bijectivity propagates orientation | discharged |
| O34 | Minimum m exists, c>=m, and minimal classes have same nonzero sign | C16 | R18 AND | side condition | Nonempty finite pair set, C13,C15,C19 | discharged |
| O35 | Boolean monomial cancellation leaves c! product increments | C19 | R19 AND | algebraic/logical step | Finite polynomial expansion | discharged |
| O36 | Integral flow of 2n gives a pair; cut bound sufficient | C17 | R20 AND | named theorem | Integral max-flow/min-cut, capacities 2,1,2, equal class sizes | discharged |
| O37 | Hall-type inequality is exactly e(U)-b(U)<=2|U|-4 | C17 | R20 AND | algebraic/logical step | t0 included in b, shortfall formula | discharged |
| O38 | Component bounds sum; small root component gives equality | C17 | R20 AND | algebraic/logical step | Face corners adjacent, root triangle, simplicity | discharged |
| O39 | Triangular component faces are original T faces | C17 | R20 AND | hypothesis | No separating triangle, p>=4, Jordan theorem | discharged |
| O40 | Signed region balance <=d-4, including repeated boundary sides | C17 | R20 AND | algebraic/logical step | Colour cancellation, parity, divisibility | discharged |
| O41 | Euler on connected component gives q-b<=2p-4 | C17 | R20 AND | named theorem | Connected H, O39,O40, side count | discharged |
| O42 | Three boundary incidences have the same colour | C18 | R21 AND | algebraic/logical step | Three signed terms with sum divisible by three | discharged |
| O43 | Both restrictions are simple, have >=4 vertices, fewer than T | C18 | R21 AND | side condition | Subgraph simplicity, strict vertices on both sides | discharged |

## Verdict

FOLLOWS for Theorem 1.1 on the route actually supplied. The decisive nodes C6, C13, C15, O20, O22, O39 and O9 are discharged. In particular the disk repair is sufficient, the sign and finite-difference algebra are correct, and the prescribed-side induction is valid. I found no false core lemma in the proof or in exhaustive rooted tests through 12 vertices.

The manuscript is not wholly correct as written: F1 is an explicit off-route error, F2 identifies two omitted checks in the closing remarks, and F3-F7 require the exact corrections above. These do not change the theorem verdict. This is an independent mathematical audit with reproducible finite checks, not a formal certification or a claim that all cited historical originals were available.
