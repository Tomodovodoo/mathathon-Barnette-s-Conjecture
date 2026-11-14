# Two involutions for the forest-pair lemma

PROVED-HERE. If a pair of disjoint states exists in a simple face-bicoloured sphere triangulation, a pair exists whose opposite-edge graph is a forest. The complete standalone proof is in involutions.tex and involutions.pdf. It assumes pair existence, so it does not need a separating-triangle hypothesis.

## Objects and the two maps

Let m be the minimum cycle count of a pair. A marked object consists of a pair and an unordered set of m distinct crossings of selected second-state spokes with fixed white-face rays. Repeated white faces and repeated spokes are permitted; repeated identical crossings are not. Direct each cycle through the first-state corner, centre, and second-state corner. With J equal to clockwise minus counterclockwise cycles, its sign is (-1) raised to floor(J/2) plus the number of marked right-to-left crossings.

The first map fixes objects with a forest opposite-edge graph. Otherwise it reverses the first opposite-edge cycle, choosing that cycle from the second state alone. This preserves all marks. The disk identity changes J by two, so it reverses sign.

The second map first reverses the first unmarked cycle of the underlying unoriented cover. If all cycles are marked, minimality forces exactly one mark per cycle. First select an exterior white-face mark, or else a nonfirst interior crossing, using a fixed orientation-independent cycle order. Pair successive ray crossings, leaving only the first crossing of an interior ray unpaired. Move the mark to its partner and reverse its cycle exactly when the partner is currently a first-state spoke. All other marks lie on other cycles. The same cycle qualifies on the return move; this proves involutivity. Geometric pairing reverses crossing direction, and cycle reversal reverses it again while flipping floor(J/2). Thus the sign reverses in either case.

Second-fixed objects are minimum covers with one interior white-face point per cycle, marked at the first crossing, with the unique orientation making that crossing a second-state spoke. Their number is the sum over minimum covers of the product of enclosed white-face counts. It is positive, and all fixed objects have sign (-1)^floor(m/2). The two signed counts force a first-fixed object.

## Explicit construction

Choose any second-fixed object by enumerating minimum covers. Alternate first and second moves, stopping before a fixed move. The finite two-coloured degree-two graph of the two involutions is a path from this endpoint. A second-fixed terminal endpoint would have the opposite sign after an odd number of moves, impossible. Hence it ends at a forest pair. This is the Garsia-Milne finite path argument. It is an exhaustive constructor, with no claim that finding a minimum cover is efficient.

## Verification

COMPUTED by research/2026-11-14_sol_li-completion/verify.py and extras.py. All 55 classes through 14 triangulation vertices agree as canonical maps with plantri. All 1206 roots are checked, including 880 with pairs. The verifier enumerates 221050 marked objects and checks both maps, signs, fixed sets, lowest coefficients and all 4658 paths from second-fixed objects. Maximum path length is two moves in those drawings; the 69-drawing recheck of the running example reaches six. Family checks reach 20 triangulation vertices. See the research census, witnesses and family outputs.

## Example and source relation

The current running.json has minimum cycle count two. The exact rational layout here gives 279 marked objects, nine second-fixed objects, and lowest coefficient nine. running-objects.json lists every object and both images; example-table.tex includes the full listing in the PDF. The earlier Li replay has 213 objects on the same input with roots 4 and 5 interchanged. The marked set depends on the drawing; the signed sum and the second-fixed count of nine do not. The actual fixed marked objects can change.

Li's incidence orientation is opposite to the directed two-spoke convention used here, so his cw-prime is -J. The two sign definitions nevertheless agree because n and m have the same parity. Li Definitions 13 through 23 and Appendix B supply the maps. Li states the set convention, unmarked-cycle rule, priority rule and fixed-set description. This note writes out his intended proof, including all-marked minimality, return-move and sign checks, the interior partner reversal, and independent orientation choices for nonemptiness. The project audit research/2026-11-14_fable_dependency-graph/audit-li.md, L-F5 and L-F6, had already identified and sketched these checks. OpenAI supplies the disk identity and first cancellation; barnette_trees uses a different ordered weight-token walk with restarts. Heights at white faces are signed counts of the same ray crossings.

## Full proof details

All claims in this section are PROVED-HERE. Their source attributions are in STATUS.md.

### Disk identity

Direct one side in each bounded black triangle out of the corner chosen by a state. Every nonroot has exactly one outgoing side; roots have none. A directed simple cycle therefore avoids the roots, and its bounded disk contains no root because all roots lie on the outside triangle.

Let h be its length, I its number of strictly interior vertices, B and W its numbers of interior black and white faces, and ell the number of boundary sides whose black face is inside. State bijectivity implies B=I+ell. Indeed an interior vertex is matched to an interior black triangle. A boundary vertex is already matched to the triangle supplying its outgoing boundary side, and that triangle lies inside precisely for the ell indicated sides. No other inside black triangle can select a boundary vertex.

If E counts disk edges, side counting and Euler give

$$E=3B+h-\ell=3W+\ell,\qquad I+h-E+B+W=1.$$

Substituting gives W=B+1 and h-2ell=3. Thus the cycle has odd length and contains a white face. With delta(u,v)=1 when the black face is to the left of u to v, its delta sum is -3 counterclockwise and 3 clockwise.

For a pair, the sides r(t) to s(t) have indegree and outdegree one at every nonroot. Their cycles are simple: each edge has only one black incident triangle and so cannot be supplied twice. The disk identity applies with state r. Thus J, one third of their total delta sum, is clockwise minus counterclockwise cycles, and J, n and the cycle count have the same parity.

Replacing each side by its tail-centre-head detour gives a simple cycle because detours lie in distinct black-triangle interiors apart from their endpoints. The old and new cycles differ by small triangular boundaries containing no white-face point. Their winding numbers at every white face agree. A white face inside exists by the disk count, so their orientations agree as well.

### First map

Write u(t) for the third corner. Orient every opposite edge from r(t) to u(t). A simple cycle of this graph has h edges with distinct tails among h vertices, so every vertex is a tail once and the cycle is directed. In particular it avoids roots. Reversing the first such cycle cyclically permutes the first state's assigned vertices, hence preserves bijectivity; u(t) differs from s(t), so disjointness remains true. The second state stays fixed, which preserves all tokens, their directions, and the selected cycle. Reversing again returns the original object. A nonempty reversal changes the first state.

For every changed triangle,

$$\delta(u(t),s(t))-\delta(r(t),s(t))=2\delta(r(t),u(t)).$$

Summing the disk identity changes J by plus or minus two. Thus floor(J/2) changes parity and no token direction changes. This proves the first map's involution, sign reversal and exact forest fixed set.

### Second map

Fix a total order on unoriented cycles. Within each family compared by the maps, supplying-face sets are disjoint, so their lexicographic order suffices. The same order is used in both directions. For each cycle C and white point w, order ray crossings from w. An exterior point has an even number of crossings, paired 1 with 2, 3 with 4, and so on. An interior point has an odd number, with crossing 1 unpaired and pairs 2 with 3, 4 with 5, and so on. Paired crossings have opposite traversal directions by Jordan entry/exit alternation.

First reverse the first unmarked cycle if one exists, leaving all tokens fixed. The unoriented cover and its unmarked cycles stay unchanged. The same reversal therefore applies twice, and no token can become invalid. Its sign changes because J changes by two and no marked direction changes.

Otherwise all cycles carry a token. Since there are m tokens and every cover has at least m cycles, there are exactly m cycles and exactly one token on each. Choose the first cycle whose token's white point is exterior. If none exists, choose the first cycle whose crossing is not first. If neither exists, fix the object.

For a chosen cycle, move its token to the paired crossing. If the partner is a second-state spoke, leave the states alone. If it is a first-state spoke, exchange the two states on that cycle so that the moved token becomes a second-state token. This exchange preserves both bijections. Other tokens are on other cycles, so remain valid and retain their directions. The new token cannot collide with another token, since different cycles have different spokes.

The same first cycle is selected on the return move. The underlying cycles, the white point assigned to each, and all exterior predicates are unchanged. If selection reached the nonfirst test, its paired crossing is also nonfirst. Every earlier cycle retains its status. The geometric pairing reverses itself. When the initial move did not reverse a cycle, the old spoke is still a second-state spoke and the return move also makes no reversal. When the initial move reversed a cycle, the old spoke is now a first-state spoke and the return move reverses that same cycle again. Thus the original object returns in both cases.

Without cycle reversal, J stays fixed and the moved token changes direction. With reversal, pairing and reversal each change its direction, so its final direction is unchanged; meanwhile floor(J/2) changes parity. Other marked directions are unchanged. Hence every nonfixed second move reverses the sign.

### Fixed points and counting

The preceding priority rules fix exactly the objects with m cycles, one token on each, an interior white point for each token, and the first crossing on each ray. For every minimum unoriented cover choose one enclosed white face on each cycle. Such a face exists by the disk identity. Orient each cycle independently so that its selected first crossing is a second-state spoke. Exactly one of the two orientations does this. Tokens on different cycles remain distinct even if their white faces are equal. Conversely each fixed object uniquely recovers those choices. Therefore the number F of second-fixed objects is the sum over minimum covers of the product of enclosed-white-face counts, and F is positive.

If q cycles are counterclockwise, their first exits go right to left, while clockwise first exits go left to right. The marked direction sum is q and J=m-2q. The sign exponent is floor((m-2q)/2)+q=floor(m/2), independent of the fixed object.

Every nonfixed two-element orbit cancels one positive and one negative object. The second map leaves imbalance (-1)^floor(m/2) times F, which is nonzero. The first map therefore cannot be fixed-point free. Its fixed object supplies a forest pair.

In Li's incidence graph the second-matching complement contains subdivided opposite sides with root endpoints removed. Its cycles are exactly the cycles of the opposite-edge graph, because a partnered opposite-edge cycle cannot contain a root by the distinct-tail argument. The forest conclusion is therefore exactly Li's cycle-breaking conclusion.

### Termination of the construction

Join objects exchanged by each nonfixed map with an edge carrying that map's label; keep parallel edges of different labels. Every object has at most one edge of each label. Begin at a second-fixed object constructed above, which lacks a label-two edge. Its finite component is a path or a singleton, since an endpoint cannot belong to any degree-two cycle, including a parallel two-edge cycle. Alternating first and second edges traverses this path without repetition.

If the other endpoint were also second-fixed, the path would begin and end with a first edge and have odd length. Sign reversal on every edge would give opposite endpoint signs, contradicting the common sign of second-fixed objects. Thus it ends at a first-fixed object, or the initial singleton is already first-fixed. This proves termination and construction. Minimum-cover enumeration is a prerequisite; there is no claim of a polynomial-time initialization or of a universal two-move bound.


## Drawing-free version

PROVED-HERE, Section 5 and Lemma 7 of the note. Fix a dual spanning tree rooted at the outer black face. For each white face w, follow its path to the root. At a black-face step i, let v be the common corner of the entering and leaving sides, and let kappa be +1 for a left turn around v and -1 for a right turn. A token is the incidence (w,i) eligible when s(f_i)=v. Its direction bit is (1+kappa)/2. Keep m distinct tokens.

For a cycle, list those steps turning around either its r-corner or its s-corner. Cutting the oriented sphere map along the formal incidence cycle shows that these steps alternate entry and exit, end outside, and have odd length exactly for an inside white face. The signed traversal at an s-incidence is -kappa, with the opposite sign at an r-incidence. Thus consecutive entries pair exactly as in the ray version. The full proof in Lemma 7 checks eligibility after reversal, distinctness, the return move, first-exit signs and independent cycle orientations. No metric drawing is part of the construction.

COMPUTED by research/2026-11-14_sol_involutions-revision/code/check.py 14. All 1206 roots, 880 paired roots, and all objects for two BFS trees were checked. Increasing and decreasing face-ID tie breaks give 17832 and 18362 objects, respectively, each with 4658 second-fixed objects and maximum path length four. The count of objects, first-fixed count and walks depend on the tree; m, F and the signed sum do not.

PROVED-HERE. This is a term-by-term bijective unpacking of the main paper's height argument for one height. The first involution lifts its cancellation lemma to marked objects; the second proves the height and finite-difference lemmas together. For face-path tokens H=-omega exactly. For ray tokens H has the opposite cycle-reversal increment, with a possible constant on each unoriented-cover class. The corrected comparison is

$$\frac{1}{m!}\sum_p\varepsilon(p)H(s)^m=(-1)^{(n+m)/2}F.$$

COMPUTED. The octahedron has n=3, m=1, F=1 and coefficient +1. The former exponent (n-m)/2 gave -1 and is REFUTED. With fewer than m marks the signed count is zero by unmarked-cycle reversal, PROVED-HERE. With m+1 marks it vanishes on 57 of 880 paired roots in the referee's drawings, and 78 in the original author's drawings. This higher count also depends on the rays. The second involution is not defined for arbitrary larger mark counts.
