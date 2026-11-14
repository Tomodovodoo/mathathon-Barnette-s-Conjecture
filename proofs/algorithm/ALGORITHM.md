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
