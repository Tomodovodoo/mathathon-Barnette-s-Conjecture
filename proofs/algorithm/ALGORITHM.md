# Finding the cycle

## What the constructive proof gives you

The proof gives two deterministic searches. One walks between pairs of states, carrying integer marks that prevent it from looping forever. The other tries states one corner at a time and rejects a choice as soon as it disconnects the incidence graph or makes completion to a state impossible. Both terminate. The second has the smaller proved worst-case bound, a polynomial factor times `3^(n/4)` for a primal graph on `n` vertices. Neither is a polynomial-time algorithm.

The determinant counts all states. It does not count good states. Its role in this algorithm is to bound how much enumeration can occur. No coefficient extraction or evaluation of the signed polynomial is needed.

## Notation and source boundary

Here `n=|V(G)|`, `V=|V(T)|=n/2+2`, and `q=|A|=|X|=V-3=n/2-1`. This avoids using `n` for both input order and number of nonroots. The manuscript uses `N,n` where this account uses `n,q`. The exposition uses `k=q+1` black faces. Roots are the corners of the black outer face `t0`. A state `s:A -> X` is an incident bijection. A pair `p=(r,s)` consists of disjoint states. `H` is the full black-face spoke graph; `B` deletes its roots and outer centre. A good state has `H-s` a tree. The manuscript calls it a tree matching and a good pair a tree pair.

`Q_s` contains the side opposite `s(t)` in each bounded black triangle. A partner `r` directs that side from `r(t)` to the third corner `u(t)`. Nonroots have outdegree one and roots zero. Each component is therefore a tree with one root or a rootless unicyclic component. The orientations toward a root are forced; each rootless cycle has two orientations. Thus a partnered state has `2^b` partners, where `b` is the number of cycles of `Q_s`, and it is good precisely when `b=0`. For an arbitrary unpartnered state, acyclicity alone is not the full good-state test.

`D(r,s)` consists of `r(t)->s(t)` and is a directed cycle cover of `X`. Its undirected edge set is a cover. Write `c(p)` for its number of cycles. The exposition's `m` is the minimum cover cycle count in the stated domain. The component proof uses the minimum *in one exchange component*. The marked walk instead uses a phase parameter `h=c(p)` at its start. These are different parameters.

The source is the unsigned *A constructive proof of Barnette's conjecture*, dated 18 October 2026, supplied as `papers/barnette_trees.pdf`, SHA256 `0329e10ae1a6eadf150a0c2b999224106bf9c0bb5f790bba0c0ce594ce155bb2`. References below are to its numbered results. The exposition PDF read for notation has SHA256 `f6597c02143f1f4c25439565cb5c9ee37fa8722166beeb5d4536846405e6d1cc`. Mathematical status tags are collected at the end.

## The exchanges and the polynomial

A D exchange reverses one cycle of `D`, swapping `r(t),s(t)` on its supplying faces. A Q exchange reverses one directed cycle of `Q_s`, replacing `r(t)` by `u(t)` on its faces and leaving `s` fixed. Each preserves bijectivity and disjointness. Applying it again on the same cycle restores the pair. These moves define the exchange graph `E`.

For an oriented triangulation edge let `delta(v,w)` be +1 when its black face is on the left and -1 otherwise. The disk identity gives total delta -3 on a counterclockwise state-directed cycle, +3 clockwise. Indeed, if its disk has `I` interior vertices, `l` boundary edges with black face inside, length `a`, and `B_d,W_d` faces, then

```
B_d+W_d = 2I+a-2,    3(B_d-W_d)=2l-a,    B_d=I+l.
```

The last identity uses the matching of every interior vertex and the matched outgoing side at each boundary vertex. Eliminating the face counts gives `2l-a=-3`. In particular every such cycle is odd. Roots lie outside because they meet the outer face.

Set `J(p)=sum_t delta(r(t),s(t))/3` and `epsilon(p)=(-1)^((q+J(p))/2)`. Oddness gives `J=c mod 2=q mod 2`, so the exponent is integral. A D reversal changes J by two in magnitude. For a Q reversal, the triangle identity

```
delta(u,s)-delta(r,s) = 2 delta(r,u)
```

and the disk identity give the same conclusion. Every exchange reverses epsilon.

Choose nonnegative integer spoke weights `a(t,v)<=6q` with positive counterclockwise circulation. To construct them, remove the outer centre, route one unit from every bounded face to the unbounded face through a dual spanning tree, and put the signed crossing totals on spokes. Internal contributions cancel, leaving circulation one around each bounded face. There are at most `3q` bounded faces, so signed weights have magnitude at most `3q`. Subtract the minimum at each black centre to obtain the stated interval without changing any circulation. A simple D cycle slides through its distinct black centres without crossing itself: each detour lies inside its triangle and excludes the third corner. Its positive circulation is

```
L_plus(C)-L_minus(C)>0,
L_plus(C)=sum a(t, counterclockwise head),
L_minus(C)=sum a(t, clockwise head).
```

The state weight `omega(s)=sum_t a(t,s(t))` is a height functional, with the same circulation increments as the exposition's heights. It is not a descent potential for finding a good state.

For one exchange component `K` the signed integer polynomial is

```
Z_K(z) = sum_(r,s in K) epsilon(r,s) z^omega(s).
```

Its degree is at most `6q^2`. Fixing `s`, reverse its first Q cycle in an order depending only on `s`. This pairs all cyclic-Q terms within K with opposite signs and equal exponents. The survivors are exactly good pairs.

Alternatively group by covers. Every orientation of a cover is present in K, since D reversals connect its orientations. The cover contribution is

```
(-1)^((q-c)/2) product_C (z^L_plus(C)-z^L_minus(C)).
```

Each factor has a simple zero at one and positive first coefficient there. If `m_K` is the least cycle count in K, the coefficient of `(z-1)^m_K` is

```
(-1)^((q-m_K)/2) sum_(covers D in K, c(D)=m_K)
                         product_(C in D) (L_plus(C)-L_minus(C)).
```

The sum is nonempty and strictly positive. Hence Z is not zero, so its good-pair expansion has a term. At `z=1` every cover contribution vanishes, so the good pairs of the two signs occur equally often and both occur. This proves component reachability, without claiming that an arbitrary walk reaches them.

## Why the marked walk stops

For a phase parameter h, a marked object is a pair p and an ordered list of h tokens `(t,j)`, with `1<=j<=a(t,s(t))`. Repetitions are allowed. Tokens mark the D cycle containing their face. A cycle has two ordered pools, indexed by face and then j, of sizes `L_plus,L_minus`.

The involution beta fixes a good pair, otherwise reverses the first Q cycle and keeps all tokens. It is well-defined because s does not change; the same cycle is selected on the return move.

Alpha first reverses the first unmarked D cycle, if there is one. Otherwise it chooses the first cycle which is clockwise, or counterclockwise with every occupied token rank at most `L_minus`. It reverses this cycle and transports its tokens to the same ranks in the opposite pool. If there is no eligible cycle, it fixes the object. For a clockwise pool all ranks are at most `L_minus<L_plus`; for the eligible counterclockwise pool all ranks fit in the smaller pool. Transport therefore exists in both directions. The set of list positions on each cycle is preserved. The same first cycle qualifies in both directions. Thus alpha is an involution. Each nonfixed alpha or beta move reverses epsilon.

An alpha-fixed object has every cycle counterclockwise and at least one rank exceeding `L_minus` on every cycle. Thus `c<=h` and its sign is `(-1)^((q-c)/2)`.

```
marked(p):
    repeat:
        h = number of D cycles of p
        reverse clockwise D cycles, making all counterclockwise
        on each cycle place one token of rank L_minus+1
        x = this alpha-fixed marked object
        repeat:
            if beta(x)==x: return pair(x)
            x = beta(x)
            if alpha(x)==x: break
            x = alpha(x)
        p = pair(x)       # discard marks, begin the next phase
```

Here is the termination proof in full. On the finite set of marked objects, retain the nonfixed involution edges with their labels. Each vertex has at most one alpha edge and one beta edge. Keep parallel differently labelled edges if both maps happen to have the same image. The starting vertex has no alpha edge. If beta fixes it, it is already good. Otherwise its component is a path: a finite component of maximum degree two containing a degree-one vertex cannot be a cycle. The alternating walk traverses that path without repeating a vertex and reaches its other end. A missing beta edge certifies goodness. Otherwise the last edge is beta, as was the first, so the number of edges is odd. The endpoint signs are opposite. At the start c=h, and at the end `c'<=h`; the fixed-point sign formula gives `c'=h+2 mod 4`. Therefore `c'<=h-2`. Each unsuccessful phase reduces a positive integer by at least two. All unmarked normalization reversals and all involution moves are legal exchanges, so the result remains in the initial component.

The proof forbids repetition of *marked objects within one phase*. It does not forbid revisiting an unmarked pair or increasing either cycle count during a phase.

## From the input to the cycle

The first pair is an integral flow. Give source-to-X arcs capacity two, X-to-incident-A arcs capacity one, and A-to-sink arcs capacity two. A value-2q flow gives a degree-two bipartite spanning subgraph, whose even cycles alternate into r and s. It exists exactly when

```
sum_(t in A) min(2, |t intersect S|) >= 2|S|  for every S subset X.
```

Section 3 of the source proves that failure is equivalent to a separating triangle with black inner boundary. The relevant hypotheses include the fixed black outer face. A white inner boundary is not an obstruction. The density proof rewrites the cut condition as `e(U)-b(U)<=2|U|-4` for U containing the roots. On each induced component, signed face balance is a multiple of three; a face of boundary length d>=4 has balance of magnitude at most d-4. Triangular positive-balance regions are actual black faces except possibly the outer region of a nonroot component. Euler counting gives `e-b<=2|U|-4` on the root component and `e-b<=2|U|` on the others. Summing proves sufficiency. Conversely a black-inner triangle enclosing I vertices has I+1 inner black faces, and its strict interior violates the capacity inequality by one.

```
solve(G, forbidden edge e):
    embed G, form its coloured dual T
    choose a face t0 incident with e*=e0, colour it black
    labels = solve_piece(T,t0,e0)
    return the primal edges dual to edges whose endpoint labels differ

solve_piece(T,t0,e0):
    p = integral flow pair
    if p exists:
        if second(p) is good: s = second(p)
        else: s = enumerate_good_state(T,t0)
              # marked(p) is a slower, independently valid alternative
        return recover(s,e0)
    find a black-inner separating triangle C
    cap both pieces, colouring caps opposite their neighbouring faces
    solve the piece containing t0 with prescription e0
    let f be the unique same-label edge of C
    solve the other piece rooted at C with prescription f
    align the two labels on C; unite the classes

enumerate_good_state(T,t0):
    search the bounded black faces in a fixed order
    try each as-yet-unused nonroot corner
    reject if the remaining incidence graph has no perfect matching
    reject if deleting the chosen spokes disconnects H
    at depth q return the state; otherwise backtrack
```

The prefix tests cannot remove a prefix of a good state. At depth q, `H-s` has `2q+4` vertices and `2q+3` edges, so connectedness makes it a tree. Existence and finite enumeration prove termination.

For recovery, dualize the deleted spokes to a spanning tree W on the q+1 white faces. Root it at the white face across e0. For each spoke, select the side of its black triangle incident with the spoke and adjacent to the child white face in W. Add e0. Each black and white face has exactly one selected side. Orient the bounded-face selections away from s(t). Nonroots have outdegree one, roots zero. A cycle would be directed. The disk identity gives `2l-a != 0`, whereas counting selected sides gives `B_d-W_d=2l-a` and counting all sides gives `3(B_d-W_d)=2l-a`. Contradiction. Thus the selections other than e0 form three rooted trees; e0 joins two of them. The complementary primal edges are connected by forest-dual connectivity and degree two by the one-side-per-face property. They form one Hamiltonian cycle avoiding e.

For gluing, a cap cannot have all corners in one induced-tree class. Its unique same-label edge determines the next prescription. The two trees of each colour meet in exactly one vertex or one edge with its endpoints. Their union is connected and has no cycle: a cycle crossing the pieces would require two disjoint routes through this connected intersection, contradicting acyclicity of a piece. There are no edges between opposite strict interiors, so the unions remain induced. The measure `|V(T)|-3` is positive and additive across each split. Recursion terminates and preserves e0.

## Bounds stated and proved in the manuscript

All incidence states have the same permutation sign. For any two, allowing common incidences, every nontrivial relative-permutation cycle gives a state-directed cycle in T. Choose arbitrary outgoing edges at their common faces; they cannot change these cycles. The disk identity makes every nontrivial cycle odd. An odd cycle is an even permutation, so relative permutation sign is positive. Therefore `M=|det K_B|`. Hadamard gives `M<=product_t sqrt(d_B(t))<=3^(q/2)`.

There are at most `(q+1)M` extendable prefixes in a fixed row order: charge each prefix to one full matching extending it and its depth. Each retained prefix tests at most three children. A residual matching test by at most q augmentations costs O(q^2); connectivity costs O(q). Thus enumeration costs O(q^3 M) time and polynomial space. This argument is complete and does not mistake a coefficient of a determinant polynomial for a determinant evaluation.

With `W=sum_t max_v a(t,v)<=6q^2`, the marked phase set has at most `6^q W^h` objects: six ordered distinct corner choices per face and W choices per token. A phase uses fewer moves than this bound. There are at most `ceil(c0/2)` phases and `c0<=floor(q/3)`. The initialization reverses at most c0 cycles. This proves `2^O(q log q)` time with polynomial work per move. The pair, token list, weights and workspace need polynomial space; no visited set is needed.

If terminal piece parameters are q_i, then `sum q_i=q`. Summing their enumeration bounds and polynomial decomposition costs gives `poly(q)3^(q/2)=poly(n)3^(n/4)`. Depth-first gluing uses polynomial space.

| Claim | Claimed in manuscript | Proved there | Proved here | Open |
|---|---|---|---|---|
| Every exchange component contains a good pair | Theorem 5.2 | Yes, signed polynomial | Detailed reconstruction above | No, conditional on source setting |
| Marked walk terminates | Theorem 5.3 | Yes | Endpoint argument checked above | Polynomial phase length |
| Every arbitrary exchange walk terminates | No | No | No | False for backtracking rules |
| `O(q^3 M)` enumeration | Proposition 6.2 | Yes | Prefix charging checked above | Polynomial bound on visited prefixes |
| `poly(n)3^(n/4)` and polynomial space | Theorem 1.1 | Yes | Additive-piece argument checked above | Polynomial time |
| Determinant coefficient extraction is polynomial | No | No | No | A useful restricted-count formula |

The current prior constructive report already states these precise exponential bounds. Describing it as proving only an unspecified exponential search loses information; it is not a contradiction between the two documents.

## Claim status

| Claims | Tag | Evidence and scope |
|---|---|---|
| Definitions, disk identity, integer weights, exchanges, polynomial, component theorem, marked walk, matching count, enumeration, recovery and gluing | LIT | Supplied unsigned manuscript, Sections 2-7, reconstructed here; preprint attribution, not peer-review certification |
| Audit of the two explicit running-time arguments | PROVED-HERE | Proofs above and research AUDIT.md; unreviewed |
| Polynomial deterministic search via these methods | CONJECTURE | No such algorithm established; conditions discussed in the extensions |

## Quantitative extensions

### A smaller marked-space bound

Let P be the number of ordered disjoint pairs. A fixed s has `2^b(s)` partners, and each rootless Q cycle has at least three vertices. Hence `b(s)<=floor(q/3)`, and

```
P = sum_s 2^b(s) <= M 2^floor(q/3) <= 3^(q/2) 2^floor(q/3).
```

The sum ranges only over partnered states. The exact size of the phase-h space is `sum_p omega(second(p))^h`. It is at most `P W^h`. Therefore the total number of involution moves is at most

```
P sum_(j=0..floor((c0-1)/2)) W^(c0-2j),   W<=6q^2.
```

Add at most `c0` normalization exchanges at the initial phase; subsequent unsuccessful endpoints already have every D cycle counterclockwise. This improves the base in the manuscript's coarse count, but remains `2^O(q log q)`. Even constant c0 leaves the exponential factor P. Bounded minimum m does not bound c0 and neither parameter alone yields an FPT algorithm by this argument.

On unmarked pairs a shortest path to a good pair has at most P-1 edges, because a shortest path repeats no vertex. BFS therefore has exponential time and space. There are at most `2q/3` legal exchanges at a pair. One can scan D and the functional orientation of Q in O(q) time. Swapping a cycle of length l changes l entries, requiring O(l) writes in the explicit representation. Recomputing both cycle decompositions costs O(q); generating and scoring all neighbours costs O(q^2). Thus BFS takes O(q^2 P) time and O(qP) words if it stores explicit pairs and predecessor records. These are upper bounds, not expected practical costs.

A balanced dynamic forest can speed up edge edits, but the whole move still changes l incidences. Q is a pseudoforest on a partnered state. One may keep a forest and one extra edge per cyclic component, with appropriate replacement-edge operations when cutting. Merely naming a link-cut tree does not implement replacement discovery or update marks, first-cycle ordering and circulation ranks. No logarithmic-cost complete marked move is asserted here. Linear scans are the proved implementation-independent bound used above. Token pools need not be materialized: prefix sums of weights locate a rank, using polynomial time and O(q+h) words.

### Incremental enumeration theorem

**Theorem.** Given the embedded incidence instance, complete good-state enumeration can find a state or establish its absence in `O(q^2(M+1))` time and O(q^2) words, with the state count M as above.

**Proof.** Maintain a full matching extending the current partial assignment. Initially compute one by at most q augmentations, each scanning O(q) edges. To force face i to corner x, do nothing if its current mate is x. Otherwise x is occupied by another unassigned face j. Remove j's match, give x to i, and leave i's old corner free. There is now exactly one unmatched residual face and corner. A single augmenting-path search decides extendability in O(q) time. If a full extension exists, its symmetric difference with the almost-perfect matching contains an augmenting path from j; if the search finds one, flipping it constructs an extension. Fixed faces cannot be traversed. Copies of the matching arrays cost O(q) per child.

Replace the test that H minus the deleted spokes stays connected by the equivalent condition that their dual white edges form a forest. For any plane connected graph, a set of dual edges contains a cycle exactly when its complementary primal edges contain a cut. This is the cycle-cut duality proved by the Jordan curve argument in the exposition. Maintain that white forest with union by size and rollback, without path compression. A find uses O(log q) parent links because a vertex's containing component at least doubles whenever its root becomes a child. Union and undo use constant additional work. A candidate joining two already connected vertices is rejected.

The next row can be selected by minimum remaining available corners, breaking ties deterministically. At any retained depth, choose an extending complete matching. Two different prefixes at that depth cannot have the same extension: following that matching's corners through the deterministic row selection would force both to be the same path. Hence there are still at most `(q+1)M` retained prefixes, even with this adaptive row order. There are at most three children each. Computing the row choice, copying arrays and repairing a matching cost O(q); the forest test is smaller. This proves the bound, including the O(q^2) initialization if M is zero. A depth-q stack with O(q)-sized matching arrays gives O(q^2) space. At a complete matching, q white edges on q+1 vertices forming a forest make a tree, so recovery is valid. Every good completion survives both necessary prefix tests. This proves completeness. QED.

The implementation is `barnette_lab.optimized.enumerate_tree`. It does not evaluate a determinant. The rollback-only benchmark uses the same search and the source's separator recursion. It enumerates an obstructed piece before splitting it; the public hybrid described below instead tests flow first. For worst-case accounting, all recursion-node parameters are at most q and there are O(q) nodes, so even this policy retains a `poly(q)3^(q/2)` bound. It can waste time on obstructed instances; a flow-first dispatch would avoid that waste. The implementation does not claim linear-time decomposition or linear-time input validation.

### Planar flow and separators

The elementary first-pair flow takes O(q^2): its value is at most 2q, integral augmentations increase value by at least one, and each augmenting search scans O(q) arcs. The single super-source network need not be planar. For a planar formulation, orient B from X to A with unit arc capacities, attach a new source leaf to each x with capacity two, and a sink leaf to each t with capacity two. Use multiple-source multiple-sink planar flow. These pendant additions preserve planarity and enforce the original vertex supplies. The theorem of Borradaile, Klein, Mozes, Nussbaum and Wulff-Nilsen gives O(q log^3 q). Their [primary paper](https://arxiv.org/pdf/1105.2228), abstract and Theorem 1.1, were opened. This is a verified available bound, not a claim that no later bound improves it. Integral capacities admit an integral optimum; implementations must retain integral flows or extract an integral optimum rather than simply round a fractional output. Alternating the resulting degree-two incidence cycles costs O(q).

**Triangle-listing lemma.** All triangles of a planar graph can be listed in linear time on adjacency-list input with dictionary adjacency tests, or with sorted bounded outgoing lists. Repeatedly remove a vertex of degree at most five, orienting its remaining edges outward. Such a vertex exists in every planar subgraph by the planar edge bound. Degree buckets implement the removals in O(V+E). Each vertex has at most five outgoing neighbours. Test their at most ten pairs for adjacency; using their outgoing lists of length at most five makes this a deterministic constant-time test. Every triangle is reported once, at its earliest removed vertex. Thus there are O(V) candidates and O(V) work. QED.

Listing triangles does not by itself construct the nested separator decomposition in linear time. A safe elementary implementation tests each nonfacial triangle by a graph scan, and repeats this on recursive pieces. With at most O(q) pieces and O(q) triangles per piece it costs O(q^3) overall. This is enough for the exponential bound. Once the decomposition is supplied with total piece size O(q), boundary prescriptions and label alignment take O(q), and one scan of original dual edges outputs the primal cycle. Explicitly recopying whole descendant solutions at each ancestor can instead cost O(q^2). The current wrapper does those copies. No unimplemented linear preprocessing is included in benchmark claims.

If every terminal piece has parameter at most b and there are L pieces, the enumeration sum is at most `O(L b^2 3^(b/2))` for the improved search, in addition to decomposition costs. Bounded *largest piece* is useful. Few separating triangles alone is not: zero separating triangles still allows arbitrarily large pieces.

### Direct good-state dynamic programming

**Theorem.** Given a width-w tree decomposition of T with O(q) bags, a good state for a specified root can be found, or its absence certified, in `q poly(b) 4^b Bell(b)^2` time and `q 2^b Bell(b)` states, where `b=max(w+2,4)+1`. This is FPT in w. For a supplied path decomposition, join nodes disappear, giving `q poly(b) 2^b Bell(b)` time. Reconstruction adds a polynomial factor if records are copied instead of predecessor pointers.

**Construction and proof.** Every triangle of T is a clique, so some bag contains all its corners. This follows from the Helly property for connected subtrees of a tree applied to the three vertex bag-subtrees. Attach a new leaf bag containing those corners and the black centre, for every black triangle. Erase original T edges from the graph, but retain the bags. This is a decomposition of H with bag size at most max(w+1,4). Add the outer centre a to every bag, so every processed component that can survive must remain connected to some boundary vertex and the final component can close at a. The stated b is a conservative upper bound on the resulting bag size. Convert to introduce-vertex, introduce-edge, forget and join nodes, with edges introduced exactly once.

For each bag store a deletion bit d(v) at every vertex and a partition pi of the bag. A deleted spoke is part of the proposed state. Bits count deleted incidences already processed, and may never exceed one. Roots and a have target bit zero; every other H vertex has target one. The retained edges must form a forest, with connected components intersecting the bag exactly in the blocks of pi; no component may have lost all boundary vertices. Isolated vertices count as components. Thus there are at most `2^b Bell(b)` syntactic states, often fewer because root bits are fixed. Bell(b) is exactly the number of partitions of a b-element set; this is an exact count of the unrestricted encoding set, not a claim that every encoding is realizable.

At introduction, add a singleton block and bit zero. For a spoke uv there are two alternatives. Delete it if both endpoints allow deletion and currently have bit zero; set their bits to one. Or retain it if u and v are in distinct blocks; merge those blocks. Retaining an edge within a block would create a cycle and is rejected. On forgetting v, require its target bit, and reject if its block is the singleton {v}. Otherwise restrict the partition. The anchor a is not forgotten until final acceptance.

At a join, add corresponding deletion bits and reject exceeding targets. Let child partitions be pi1,pi2 and let pi be their join. Reject if `b+|pi|-|pi1|-|pi2|` is nonzero. This expression is the cycle rank of the union: child forests have disjoint edge sets and intersect only on the bag; all their components meet it, so their component counts are |pi1|,|pi2|, and the union count is |pi|. Substitute these counts into E-V+components. It is nonnegative, and zero is equivalent to acyclicity. Store pi. Each pair of states can be tested in poly(b) time.

Induction on the decomposition proves that these transitions represent exactly the partial deletion matchings whose complementary retained graph is a forest with no closed component. The forward direction follows from each check. For the reverse direction restrict a valid partial forest to each child; its deletion bits and connectivity determine the predecessor states. At a forget node, a closed component cannot later connect to any unprocessed edge by the decomposition property, so rejecting it loses no connected final solution. At the top, retain only bag {a}, bit zero and its singleton partition. Every other vertex has met its required deletion degree and the retained graph is one tree. The deleted spokes form an incident bijection A to X. This is exactly a good state. Storing one predecessor per accepted state reconstructs it. Squaring the state bound at joins proves the time bound. QED.

This general tree-decomposition DP is specified and proved here. The path version is implemented below; general join nodes are not implemented. It handles high-degree vertices of T without a degree-dependent state count because deleted, not retained, incidences are counted.

### Subexponential and cubic-graph alternatives

Delete the forbidden edge and solve Hamiltonian cycle in the remaining planar graph. The supplied existence theorem guarantees success. The [Dorn, Penninkx, Bodlaender and Fomin paper](https://link.springer.com/article/10.1007/s00453-009-9296-1), Algorithmica 58, 790-810, states an `O(2^(6.903 sqrt(n)))` weighted planar Hamiltonian-cycle algorithm. The publisher's theorem summary was opened; the full subscription proof was not accessible in this run. Thus `2^O(sqrt(n))` is an attributed literature bound, not a new proved-here theorem or an implemented benchmark result. Plain Bell-number DP combined only with width O(sqrt(n)) would give `2^O(sqrt(n) log n)`; eliminating that logarithm requires the sphere-cut noncrossing structure or another single-exponential connectivity method.

[Eppstein's published cubic-graph algorithm](https://www.jgaa.info/index.php/jgaa/article/view/paper137) gives O(2^(n/3)) time and linear space. [Xiao and Nagamochi](https://arxiv.org/pdf/1212.6831) state O*(1.2312^n) and polynomial space for maximum degree three. Deleting e keeps the graph within that degree bound. These are useful alternatives to the manuscript's enumeration and do not rely on it for their running time. They are not implementations supplied here and no global fastest-known claim is made.

### Families and lower bounds

An even prism can be solved directly in O(n) time. Name its rim vertices a_i,b_i for i modulo an even k. If a rim edge a_i a_(i+1) is forbidden, use the cycle obtained from both full rim paths with the corresponding pair of rim edges removed and the two connecting rungs at their endpoints. It avoids both removed edges. If rung a_i b_i is forbidden, choose any adjacent rung positions j,j+1 distinct from i and use the same construction. For k>=4 such j exists. The two rim paths and two rungs visit every vertex once. This is a proof for every edge of an even prism, independent of matching rarity.

Fixed-width nanotubes have a vertex order exposing O(width) vertices at each layer. The DP above yields linear-in-length time with a width-dependent constant. Faces of size four or six alone do not bound treewidth or the layer width, so this reasoning does not give a uniform polynomial theorem for all such graphs. No fresh audit of Goodey's constructive algorithm is claimed here.

For the known 16-vertex trap, each shortest path to goodness takes at least two exchanges. Glue r copies into white faces as in the descent report. Inner nonroots can be matched only by the inner bounded black faces, and their cardinalities agree, so state choices factor. Every D or Q cycle stays in one factor. For Q, follow its functional orientation: once in an outer nonroot the supplier face remains outer; a cycle cannot enter an inner strict interior and then return. Thus the exchange graph is the Cartesian product, and good pairs require every factor good. Projecting a path onto each factor shows at least two moves per factor, hence at least `2r=2(V-3)/13` in total. This is a lower bound from the supplied trap certificate and the checked product argument. It is linear, not evidence of a superlinear or exponential pivot lower bound. No such stronger family is proved here.

## Complexity classes and what would give polynomial time

The total search formulation returns a cycle avoiding e for a valid Barnette input, or a polynomially checkable rejection of the input conditions. Existence plus certificate verification places it in TFNP, conditional on the supplied Barnette theorem. The marked construction supplies the more specific PPADS route for TREE-PAIR. At a level h of parity q, put `sigma_h=(-1)^((q-h)/2)`. Direct beta edges from sign sigma_h to its opposite, and alpha edges back. There are at most one incoming and one outgoing edge. A sink is either beta-fixed and good, or alpha-fixed of opposite sign with c<=h-2.

Join every latter sink to the canonical start at level c, carrying the whole old endpoint in a history. At an alpha-fixed endpoint the pair is already all-counterclockwise, so this restart changes only marks and is still nongood. Histories have strictly decreasing levels, polynomial length, and O(q^2 log q) bits. They make the restart map injective. Allow all syntactically valid histories, not just reachable ones; predecessors test the last recorded endpoint and its canonical restart. Invalid encodings receive self-loops. Nongood sinks disappear; the specified normalized input is a source unless already good. Thus a sink oracle returns a good pair. This is the corrected reduction in the descent referee, restated with its encoding obligations. The [Li, Pires and Robere primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol287-itcs2024/LIPIcs.ITCS.2024.74/LIPIcs.ITCS.2024.74.pdf) confirms the sink-based class definitions.

For the full graph, polynomially many adaptive TREE-PAIR calls give a polynomial-time Turing reduction to PPADS. Turning this into the usual many-one membership uses closure under Turing reductions, attributed by the earlier referee to Buss and Johnson, Corollary 6.2. That source was not retrievable here. The unqualified many-one membership of the full problem is therefore not a new proved-here result in this account. TREE-PAIR membership above does not need that closure citation. PPAD and PPA accept extra sources or leaves, which need not be good, so these constructions do not prove either membership. This is not a separation from those classes. C3 permits plateaus and does not itself furnish a PLS improvement oracle.

The following sufficient hypotheses would give polynomial algorithms, with different obligations.

* A polynomial-time pivot rule with at most L(q) moves gives O(q L(q)) search with linear rebuilding, plus polynomial preparation and recovery. C3 plus an existential polynomial path-length bound alone does **not** suffice: a polynomial-degree graph can still have exponentially many candidate paths of polynomial length. An efficient way of finding the path is also required. With a fixed escape radius d and O(q) neighbours, BFS to a lower Q count costs O(q^(d+1)) per descent and O(q^(d+2)) altogether. Radii one, two and three are refuted at V=16,21,40 respectively. The V=40 witness does not prove minimality or refute every fixed radius.
* A polynomial-time computable integer potential with polynomially many values and a polynomial-time strict-improvement oracle, whose local optima are all good, gives polynomial time by strict descent. The 27 specified potentials in FACTS.md have counterexamples. This does not quantify over every possible potential.
* Step X would yield a polynomial construction if it supplies a polynomial-time way to replace a rainbow tree by one with smaller integer surplus, after Step R, or a polynomially bounded sequence with computable pivots. Mere existence of a lower-surplus tree after an unbounded exchange search is insufficient. The 38- and 40-vertex periodic evict instances already exclude the naive walk.
* The two induction lemmas would yield a polynomial algorithm if a valid contraction and a lift or repair can be found in polynomial time with only one recursive subproblem per order. Trying both contractions at each step can give exponential recursion even if one eventually lifts. Numerical counting inequalities alone do not specify a polynomial constructor. Repair within one fixed cover already fails at V=18.
* An exact nonnegative count of good completions, computable in time C(q) for arbitrary fixed incidences, gives a deterministic constructor with at most 3q oracle calls, hence O(q C(q)). Test each candidate corner and keep one with positive count. Ordinary incidence determinants count all completions and do not meet this condition. A signed restricted sum may vanish despite good completions and is not automatically a decision oracle.

The promising implementation question is therefore a stronger prefix oracle. The present two tests enforce a matching extension and a white forest separately. Their conjunction need not give a good extension; the attack below tests this exact obstruction rather than assuming that matroid intersection enforces both corner and face partitions.

## Extended claim status

| Claims | Tag | Evidence and scope |
|---|---|---|
| Improved P bound, marked sum bound, BFS bound | PROVED-HERE | Counting proofs above, unreviewed |
| O(q^2(M+1)) enumeration | PROVED-HERE | Augmenting repair and prefix charging above, unreviewed |
| FPT good-state DP and exact encoding bound | PROVED-HERE | Full transitions and invariant above; not implemented |
| Linear triangle listing | PROVED-HERE | Degeneracy orientation proof; decomposition not included |
| Planar multi-terminal flow O(q log^3 q) | LIT | Opened primary theorem; no latest-optimality claim |
| Planar 2^O(sqrt(n)) algorithm | LIT | Opened publisher theorem statement; full proof not audited |
| Cubic exponential alternatives | LIT | Eppstein published statement, Xiao-Nagamochi preprint |
| Prism construction and bounded-width tube DP consequence | PROVED-HERE | Direct proofs above |
| Linear trap-chain lower bound | PROVED-HERE | Product proof plus prior finite trap certificate |
| TREE-PAIR in PPADS | PROVED-HERE | Corrected history reduction above, building on descent referee |
| C3, Step X, polynomial prefix oracle | CONJECTURE | Open statements with explicit computational tests |
| Named bounded radii/potentials and naive evict rules | REFUTED | Exact scopes in FACTS.md; no new census claim |


## Worked examples

These are exact, reproducible arithmetic traces, with every exchange and recovery choice listed. `examples.py` generates them from the input graphs; they are computed examples, not additional existence proofs. Neither example requires separator gluing.

### Cube

Dual face IDs are the following ordered triples. The outer face is 0; roots are [0, 1, 2]; the prescribed dual side is (0, 2).

| Face | Corners | Colour |
|---|---|---|
| 0 | (0, 2, 1) | black |
| 1 | (0, 4, 2) | white |
| 2 | (0, 3, 4) | black |
| 3 | (0, 1, 3) | white |
| 4 | (1, 2, 5) | white |
| 5 | (1, 5, 3) | black |
| 6 | (2, 4, 5) | black |
| 7 | (3, 5, 4) | white |

The state coordinates below are in face order A=[2, 5, 6]. Nonroots are [3, 4, 5].

An integral value-6 flow chooses r=(3, 5, 4) and s=(4, 3, 5). Each X vertex and A face has degree two in their union. All other incidence arcs carry zero. Alternating each union cycle gives these two states.

There are 2 states and 2 pairs by exhaustive enumeration. For a nontrivial walk when available, start instead at r=(3, 5, 4), s=(4, 3, 5).

Its D cycles, specified by supplying faces, are [(2, 5, 6)]. Its Q cycles are [].

Nonzero spoke weights `(face,corner,weight)` are [(6, 4, 1)].

The signed polynomial in these weights is {0: 1, 1: -1}, written as exponent-to-coefficient entries.

Phase 1, h=1.
Normalize D cycle (2, 5, 6): r=(4, 3, 5), s=(3, 5, 4).
Initial excess-rank tokens are ((6, 1),); alpha fixes this object.
Beta fixes the object: the second state is good.

The opposite edges Q_s are [(0, 4), (1, 3), (2, 5)].

The white tree is [[1, 7], [3, 7], [4, 7]], rooted at 1.

| Black face | Deleted corner | White edge | Child | Selected side |
|---|---|---|---|---|
| 2 | 3 | (3, 7) | 3 | (0, 3) |
| 5 | 5 | (4, 7) | 4 | (1, 5) |
| 6 | 4 | (1, 7) | 7 | (4, 5) |

Add e0=(0, 2). The selected sides are [(0, 2), (4, 5), (0, 3), (1, 5)]. The two induced-tree classes are [[0, 2, 3], [1, 4, 5]].

The primal cycle, using dual face IDs, is [0, 3, 5, 7, 2, 1, 6, 4], closed back to its first vertex. The omitted edge is (0, 1). Each consecutive pair shares a side in the face table, and the list contains all 8 face IDs exactly once. The independent primal checker accepts it.

### 13-vertex running triangulation

Dual face IDs are the following ordered triples. The outer face is 2; roots are [0, 4, 5]; the prescribed dual side is (0, 4).

| Face | Corners | Colour |
|---|---|---|
| 0 | (0, 6, 1) | black |
| 1 | (0, 5, 6) | white |
| 2 | (0, 4, 5) | black |
| 3 | (0, 3, 4) | white |
| 4 | (0, 2, 3) | black |
| 5 | (0, 1, 2) | white |
| 6 | (1, 6, 7) | white |
| 7 | (1, 9, 2) | black |
| 8 | (1, 8, 9) | white |
| 9 | (1, 7, 8) | black |
| 10 | (6, 5, 11) | black |
| 11 | (6, 12, 7) | black |
| 12 | (6, 11, 12) | white |
| 13 | (2, 9, 3) | white |
| 14 | (3, 9, 4) | black |
| 15 | (4, 11, 5) | white |
| 16 | (4, 10, 11) | black |
| 17 | (4, 9, 10) | white |
| 18 | (7, 12, 8) | white |
| 19 | (8, 10, 9) | black |
| 20 | (8, 11, 10) | white |
| 21 | (8, 12, 11) | black |

The state coordinates below are in face order A=[0, 4, 7, 9, 10, 11, 14, 16, 19, 21]. Nonroots are [1, 2, 3, 6, 7, 8, 9, 10, 11, 12].

An integral value-20 flow chooses r=(6, 2, 1, 7, 11, 12, 3, 10, 9, 8) and s=(1, 3, 2, 8, 6, 7, 9, 11, 10, 12). Each X vertex and A face has degree two in their union. All other incidence arcs carry zero. Alternating each union cycle gives these two states.

There are 12 states and 8 pairs by exhaustive enumeration. For a nontrivial walk when available, start instead at r=(6, 2, 1, 8, 11, 7, 3, 10, 9, 12), s=(1, 3, 2, 7, 6, 12, 9, 11, 10, 8).

Its D cycles, specified by supplying faces, are [(0, 4, 7, 10, 14, 16, 19), (9, 11, 21)]. Its Q cycles are [(7, 9, 19)].

Nonzero spoke weights `(face,corner,weight)` are [(0, 6, 2), (4, 0, 2), (7, 1, 1), (10, 11, 1), (11, 6, 1), (11, 12, 1), (14, 3, 1), (16, 4, 2), (16, 10, 1)].

The signed polynomial in these weights is {0: 1, 2: -1, 4: -1, 5: 1, 6: -1, 7: 1}, written as exponent-to-coefficient entries.

Phase 1, h=2.
Normalize D cycle (0, 4, 7, 10, 14, 16, 19): r=(1, 3, 2, 8, 6, 7, 9, 11, 10, 12), s=(6, 2, 1, 7, 11, 12, 3, 10, 9, 8).
Initial excess-rank tokens are ((0, 1), (11, 1)); alpha fixes this object.
Beta fixes the object: the second state is good.

The opposite edges Q_s are [(0, 1), (0, 3), (1, 8), (2, 9), (4, 9), (4, 11), (5, 6), (6, 7), (8, 10), (11, 12)].

The white tree is [[1, 6], [3, 13], [5, 8], [5, 13], [6, 18], [8, 17], [12, 15], [12, 18], [17, 20], [18, 20]], rooted at 3.

| Black face | Deleted corner | White edge | Child | Selected side |
|---|---|---|---|---|
| 0 | 6 | (1, 6) | 1 | (0, 6) |
| 4 | 2 | (5, 13) | 5 | (0, 2) |
| 7 | 1 | (5, 8) | 8 | (1, 9) |
| 9 | 7 | (6, 18) | 6 | (1, 7) |
| 10 | 11 | (12, 15) | 15 | (5, 11) |
| 11 | 12 | (12, 18) | 12 | (6, 12) |
| 14 | 3 | (3, 13) | 13 | (3, 9) |
| 16 | 10 | (17, 20) | 20 | (10, 11) |
| 19 | 9 | (8, 17) | 17 | (9, 10) |
| 21 | 8 | (18, 20) | 18 | (8, 12) |

Add e0=(0, 4). The selected sides are [(0, 4), (3, 9), (0, 2), (1, 9), (9, 10), (10, 11), (8, 12), (1, 7), (6, 12), (0, 6), (5, 11)]. The two induced-tree classes are [[0, 2, 4, 6, 8, 12], [1, 3, 5, 7, 9, 10, 11]].

The primal cycle, using dual face IDs, is [0, 5, 7, 13, 4, 3, 14, 17, 16, 15, 2, 1, 10, 12, 21, 20, 19, 8, 9, 18, 11, 6], closed back to its first vertex. The omitted edge is (2, 3). Each consecutive pair shares a side in the face table, and the list contains all 22 face IDs exactly once. The independent primal checker accepts it.

## Implementation of the bounded-width route

`barnette_lab.optimized.path.path_tree` implements the path version of the forest-and-deletion DP. It orders black centres by their sorted corner triples and processes their three spokes consecutively. The outer centre is a permanent anchor. A vertex enters at its first processed spoke and leaves at its last. The recorded frontier width is the actual largest temporary bag, including the anchor. For this ordering, the states and transitions are exactly the introduce-edge and forget operations proved above. Closing any block not containing a remaining frontier vertex is rejected, even if several vertices of that block are forgotten together.

The implementation retains a full chosen-state tuple per table entry, so its reconstruction storage and tuple-copying cost have an extra O(q) factor relative to a predecessor-pointer implementation. It supports explicit width and state limits that raise `BudgetExceeded`; exceeding a limit is never reported as nonexistence. With no limits, it is a complete decision and construction algorithm. For the path-decomposition theorem, insert a bag containing an existing bag and its new black centre rather than attaching a leaf; this preserves a path and adds at most one vertex to bag size. The stated conservative b covers that construction too.

The public hybrid first obtains a flow pair. It returns immediately when that pair is good. Otherwise it makes at most 32 deterministic exchanges, choosing the unvisited neighbour with fewest Q cycles and breaking ties lexicographically. This rule is allowed to increase the cycle count; it is not an implementation of the conjectured C3 theorem. If the bounded walk does not succeed, the hybrid tries the path DP with frontier limit 12 and table limit 20,000, then uses complete rollback enumeration. A failed flow triggers separator gluing immediately. These bounded preliminary searches add only polynomial work to the complete enumeration bound. The cap is a design choice, not a mathematical claim about exchange distance.

| Additional claim | Tag | Scope |
|---|---|---|
| Edge-frontier DP implements the stated invariant | PROVED-HERE | Same induction as path DP; code tests recorded separately |
| Hybrid terminates and returns a checked certificate | PROVED-HERE | Finite preliminary searches, complete enumeration, flow obstruction and gluing; input existence theorem assumed |
| Fast times on tubes and biased split samples | COMPUTED | BENCHMARKS.md and saved per-instance cycles |

## The prefix-oracle attack

The next possible improvement is to replace backtracking by a polynomial prefix oracle. The two source tests do not suffice, even after one natural strengthening. Here is a complete small obstruction.

Use the 8-vertex triangulation in `filtered-prefix-counterexample.json`, with outer face `(0,3,4)`. The bounded black faces, in order, are

```
a=(0,1,2), b=(1,4,5), c=(1,6,7), d=(2,7,3), e=(3,6,5).
```

The nonroots are `{1,2,5,6,7}`. Its only states are

```
s1=(1,5,7,2,6), s2=(2,1,6,7,5), s3=(2,5,1,7,6).
```

To check exhaustiveness, a chooses 1 or 2. If a chooses 1 then b must choose 5, e must choose 6, c must choose 7 and d chooses 2. If a chooses 2, d must choose 7. The remaining three faces b,c,e either choose 1,6,5 or 5,1,6. There is no other matching. Directly contracting the retained two spokes in each bounded face shows that s1 and s2 give three one-root trees. For s3, the Q edges are `(0,1),(1,4),(6,7),(2,3),(3,5)`. The component `{0,1,4}` contains two roots and `{6,7}` has none. Hence s3 is not good.

Now prescribe the prefix `a->2,b->5`. Its sole matching extension is s3. The prefix leaves H connected. In fact the three remaining required deletions are each individually compatible with connectivity. This can be checked without enumerating any spanning trees. After the prefix the neighbour lists of the six black centres are

```
t0: 0,3,4;  a:0,1;  b:1,4;  c:1,6,7;  d:2,7,3;  e:3,6,5.
```

All centres and vertices lie in one component. Delete just `c-1`: c still reaches the outer component through `c-7-d-3-t0`, and a,b retain 1. Delete just `d-7`: d still reaches it through 3, and c connects 7 through 1. Delete just `e-6`: e still reaches it through 3, and c connects 6 through 1. Thus all three edges of the unique residual perfect matching survive a filter that removes individually forest-incompatible choices. Deleting all three at once disconnects the retained graph, as the Q components already show.

This refutes both a polynomial constructor that greedily trusts those tests and its individually filtered matching variant. It does not refute a stronger global oracle, C3, Step X or a restricted determinant formula. The witness already lives in the hexagonal-prism dual; no large construction is needed.

The search `attack.py filtered` found this witness after ten eligible rootings in its stated order. `verify_saved.py` independently rebuilt H from the saved face list, enumerated the three states by Cartesian products, and checked each deletion test. The companion unfiltered witness at another root was found after nine eligible rootings. These are the exact search ranges, not a new general census claim.

The same campaign stressed minimum-remaining-corners enumeration on 500 split-generated graphs of dual orders 20,30,40,50 with seed 101441. The worst recorded input used 32,161 candidate tests and 24,699 retained prefixes. Its complete adjacency, root and state are saved in `stress.json`. This is evidence against treating cheap prefix tests as a complete optimization. It is not a superlinear lower bound, since the finite count has no asymptotic force.

A separate 60-instance hunt varied labels and roots at dual orders 30,50,80,120, seed 719883. Every public hybrid call succeeded, with at most two exchanges. The largest measured end-to-end time was 0.454309 seconds on a 236-vertex primal input, including validation and dual construction. This hunt did not produce a difficult family for the final pivot rule. No superlinear or exponential lower bound for that rule was obtained.

## A candidate exponential marked-walk family

The fixed-flow marked constructor was run on the recursively labelled trap chains with k=1,...,10. Its completed move counts for k=1,...,8 are

```
0, 5, 14, 113, 562, 2811, 14060, 70309.
```

The eight-factor case has 210 primal vertices and completed in 79.794269 seconds with eight phases, decreasing the D count at unsuccessful endpoints from 24 to 10 in steps of two. The first run censored k=8,9,10 at twenty seconds; only k=8 was rerun with a larger cap. The initialization uses the flow pair at every k, not a specially substituted bad pair. Exact graph labels, roots, starting pairs, returned cycles and software versions are saved in marked-chain-instances.json, marked-chains.jsonl, marked-chain-eight.json and manifest.json. The first factor's normalization count can depend on the orientation in which the flow union is traversed; the marked count follows the all-counterclockwise normalized start.

**Conjecture, fixed rule.** For this labelled chain construction, the reference flow cover, the reference positive weights and the manuscript's ordered-cycle/ordered-token rule, the number of marked moves for every k>=4 is

```
L(k) = (9*5^(k-2)-2*k+9)/2.
```

It agrees exactly at k=4,...,8. Equivalently, the observed recurrence from k=5 is `L(k)=5L(k-1)+4k-23`. Testing k=9, then identifying a local marked-state transition invariant, is a concrete next step. The five verified values do not prove an exponential lower bound. The shortest-path lower bound remains the earlier linear one. Different starting covers, weights or tie rules need not obey this conjecture.

The following elementary theorem explains a possible mechanism, without identifying it with the Barnette walk.

**Theorem, abstract involution product.** There are two polynomial-time computable sign-reversing involutions on objects encoded with O(k) bits whose alternating path from a specified alpha-fixed object has exactly `5^k-1` moves before it reaches a beta-fixed object.

**Proof.** On `{0,1,2,3,4}` let alpha fix 0 and interchange 1 with 2 and 3 with 4. Let beta interchange 0 with 1 and 2 with 3 and fix 4. On k-tuples, apply alpha to the first coordinate not fixed by its local alpha, fixing the tuple if none exists. Define beta the same way using its local rule. These are involutions because the first eligible coordinate remains the first eligible coordinate after its swap. Each nonfixed move reverses `(-1)^(sum of coordinates)`. The unique alpha-fixed tuple is all zero; the unique beta-fixed tuple is all four.

For k=1 the alternating walk is 0,1,2,3,4, of length four. Suppose the remaining k-1 coordinates have an alternating path of length D. The first coordinate traverses 0 to 4 in four moves. There beta fixes that coordinate, so the next beta move acts on the remaining tuple. Alpha then traverses the first coordinate back from 4 to 0, again in four alternating moves. At zero alpha fixes that coordinate, so the next alpha move acts on the remaining tuple. Continue. Thus the remaining tuple takes its own alternating path, while coordinate one makes a complete four-edge sweep before the first remaining-tuple move, between consecutive such moves, and after the last. There are D+1 sweeps and D remaining-tuple moves. Induction gives D=`5^(k-1)-1`, which is even, so the last sweep ends at 4. The total is `4(D+1)+D=5^k-1`, and the endpoint is all four. Testing the first eligible coordinate takes O(k) time and the encoding has k digits. QED.

This is a lower bound for the abstract first-eligible involution rule. It proves that finite path structure, sign reversal, efficient move evaluation and a known start endpoint do not by themselves imply a polynomial path. To turn it into a Barnette lower bound one must embed the product transition system in the actual token dynamics, including the priority given to unmarked cycles, pool ranks, restart normalization and the face ordering. That embedding is not established here. The matching factorization across white-face gluings does not automatically factor the marked walk.


## Final status table

| Claim group | Status | Evidence or remaining obligation |
|---|---|---|
| Source reachability, marked termination and exponential enumeration | LIT | Supplied manuscript Theorems 5.2, 5.3, Proposition 6.2; source audit in AUDIT.md |
| Audit of source arguments | PROVED-HERE | Explicit obligation graph and proofs; unreviewed |
| Improved enumeration O(q^2(M+1)), polynomial space | PROVED-HERE | Matching repair, rollback forest and deterministic-prefix charging |
| Bounded-width good-state DP | PROVED-HERE | Full tree-decomposition transitions; path version implemented |
| Marked state-space refinement and unmarked BFS bounds | PROVED-HERE | Counting arguments above |
| Prism linear constructor, fixed-width tube DP and piece-size bounds | PROVED-HERE | Stated structural hypotheses essential |
| Planar flow and subexponential Hamiltonian search | LIT | Verified source statements; sphere-cut proof and implementation not supplied |
| Linear trap-chain lower bound | PROVED-HERE | Prior finite trap plus product argument; no stronger lower bound |
| TREE-PAIR in PPADS | PROVED-HERE | History construction checked; full-problem many-one closure remains attributed to prior referee |
| Two prefix-oracle conjectures | REFUTED | Explicit 8-vertex proof above and independently replayed certificates |
| Census, family and adversarial-search performance | COMPUTED | BENCHMARKS.md, scripts, saved cycles, independent-checks.json |
| C3 and general polynomial construction | CONJECTURE | No proof; bounded variants already refuted in FACTS.md |
| Better global completion oracle or bounded efficient pivot rule | HUNCH | Must survive the prefix witnesses and prior plateau witnesses |
| Abstract first-eligible involution product takes 5^k-1 moves | PROVED-HERE | Induction above; not a Barnette lower bound |
| Formula L(k) for the actual marked trap chains | CONJECTURE | Exact agreement for k=4,...,8; embedding/recurrence proof missing |
