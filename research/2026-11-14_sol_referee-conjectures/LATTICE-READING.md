# The two cancellations in lattice language

Referee: gpt-6.1-sol, 14 November 2026. New arguments are `PROVED-HERE`, T2 unreviewed. Finite calculations are `COMPUTED`. Human review is pending. The source labels `LIT` refer to the supplied manuscripts, without making a publication or peer-review claim.

## 1. What a lattice element remembers

`PROVED-HERE`. Write L for the lattice of deleted-corner maps u, and P for its poset of join-irreducibles. An element of L is a 2-factor, not an ordered pair. Above u there are 2^c(u) ordered pairs, the independent directions of its D-cycles. The actual summation domain is

    E = disjoint union over I in J(P) of {I} x {0,1}^c(I).

The second coordinate is necessary. Reversing one D-cycle fixes I and reverses the pair sign. Thus the pair sign cannot be a character of lattice rank, even before any weights are introduced.

`PROVED-HERE`, a self-contained justification of the notation J(P). Every element of a finite lattice is a join of join-irreducibles below it, by induction, splitting any element that is neither bottom nor join-irreducible. In a distributive lattice a join-irreducible j is join-prime. Indeed, j <= a join b implies

    j = (j meet a) join (j meet b),

so j <= a or j <= b. Consequently I(x) = {j in P: j <= x} preserves meets as intersection and joins as union. It is injective by the first observation. Every ideal I of P is I(join I), because join-primality prevents a new join-irreducible appearing. This proves L = J(P). Covers add one element of P, and rank(x) = |I(x)|.

`CORRECT AFTER FIX`, `PROVED-HERE`. A lattice cover need not raise one geometric face. It raises a minimal forced set of face potentials. The sum of all geometric face heights is therefore a weighted rank statistic, not necessarily rank. The threshold events {phi(f) >= k} can coincide for several faces because rigid spokes force them together. Rank counts the distinct join-irreducible events.

## 2. The forest criterion and the first cancellation

`PROVED-HERE`, independent proof of Opus Lemma 2. Fix a pair r,s, with third corners u. Form the directed graph F with spokes

    u(t) -> t -> r(t).

Every centre has indegree one. Each nonroot has indegree one, since r is a bijection. Roots have indegree zero. Suppressing centres gives exactly the undirected edges of Q_s, directed u(t) -> r(t). In any undirected cycle of F, its edges have distinct heads because indegrees are at most one. All vertices of that cycle must therefore have one incoming and one outgoing cycle edge. The cycle is directed. Hence Q_s is a forest exactly when F has no directed cycle. A directed cycle of O_u belongs to F exactly when every exit from a centre t goes to r(t). This proves the criterion.

If Q_s is a forest, it has n edges on n+3 vertices. In each tree component the indegree sum equals the number of vertices minus the number of roots. It also equals the number of edges, one less than the number of vertices. Each component contains exactly one root. This is the tree-matching condition, including isolated roots.

`PROVED-HERE`. Choose an undirected cycle K in Q_s by a deterministic rule depending on s alone. In F it has the direction u -> t -> r. Reverse this entire spoke cycle in O_u. On its faces,

    u'(t) = r(t),    r'(t) = u(t),    s'(t) = s(t).

The old r-corners and u-corners on K are the same vertex set, cyclically permuted, so r' is a state. This is precisely Lemma 5.2, now expressed as a directed-cycle reversal of a lattice orientation. The reverse rule is the same because Q_s is fixed. It is a fixed-point-free involution on decorated elements of E.

In face potentials this operation adds or subtracts the indicator of the disk bounded by the spoke cycle. It therefore moves to a comparable lattice element. It need not be a cover. In J(P), the ideals before and after differ by all threshold events crossed by this disk move. There is no reason for only one join-irreducible to change.

`LIT`, supplied OpenAI manuscript, Lemma 4.1 and Lemma 5.2. The disk identity gives odd length for the Q-cycle and J(r',s)-J(r,s) = +/-2. For the real sign

    epsilon(r,s) = product over t of delta(r(t),s(t)),

each changed triangle flips its local sign, and the odd number of changes flips epsilon. Any weight depending only on s is preserved. Thus the same involution cancels every term with cyclic Q_s. This description exposes the role of the criterion without changing the cancellation argument.

`COMPUTED`. `code/cancellations.py 16` checks every pair at every rooted plantri instance through V=16. It checks the sign reversal, the disk-indicator potential change, fixed-s coefficient cancellation, positive spoke-cycle weights, and C3 reachability. `code/census.py 18` independently compares the criterion with a union-find forest test on every ordered pair through V=18.

## 3. The exact signed sum over J(P)

`PROVED-HERE`. Give incidence t,v weight a(t,v), and let omega(s) be its sum on a state. For integer weights use the Laurent polynomial

    F(z) = sum over (r,s) of epsilon(r,s) z^omega(s).

An overall monomial converts it into a polynomial. For I in J(P), orient all its D-cycles clockwise as reference. Put b_I = omega(s_cw), let c_I be the number of cycles, and let

    A_(I,C) = omega(heads_ccw on C) - omega(heads_cw on C).

The disk identity gives the sign of a counterclockwise h-cycle as (-1)^((h+3)/2), and h is odd. Therefore the exact formula in terms of the ideal I is

    F(z) = sum over I in J(P) of
           (-1)^((n-c_I)/2) z^b_I product over C of (z^A_(I,C) - 1).       (1)

Every item decorating I matters: c_I, the incidence weights, and the disks of its cycles. With unit bounded-face circulation on H0, A_(I,C) is the positive number of bounded H0 faces inside the spoke detour of C. This is the paper's detour argument, not a consequence of the order on P. The independent construction of these integer weights is `Instance.spoke_weights` in `code/independent.py`.

For fully independent incidence indeterminates w_tv, the same statement is

    F(w) = sum over I in J(P) (-1)^((n-c_I)/2)
           product over C of (w^(C+) - w^(C-)).                           (2)

Here each monomial on a cycle is the product of the selected head-incidence variables. Substitution w_tv = 1 + x a(t,v) gives the integer-polynomial version of the proof from the determinant referee's SIGNIFICANCE.md, section 2. Its first coefficient in degree m = min c_I is

    (-1)^((n-m)/2) sum over I with c_I=m of product over C of A_(I,C),    (3)

which is nonzero because all A_(I,C)>0. Formula (1) at z=1+x has the same first nonzero coefficient. Negative exponents do not affect it since z^b has constant term one there.

## 4. Where the Mobius operation actually occurs

`PROVED-HERE`. Fix white faces w_1,...,w_m and the intersection heights h_s from the combinatorics referee's REWRITTEN-PROP-5-1.md. In the fibre over I, write x_C=1 for the counterclockwise direction, zero for clockwise. Then

    h_s(w_i) = b_(I,i) + sum over C of x_C [w_i is inside C].

The contribution of that fibre to the signed height-product sum is exactly

    (-1)^((n+c_I)/2) sum over x in {0,1}^c_I (-1)^|x|
       product over i=1,...,m of
           (b_(I,i) + sum over C of x_C [w_i is inside C]).              (4)

This IS a Mobius finite difference on the Boolean lattice of directions over one I, since mu(empty,x)=(-1)^|x| there. It is not the Mobius function of L. It also gives an exact formula using P: first sum (4) over all its ideals, retaining the listed cycle-disk decorations.

Proof of nonvanishing. Expanding the product in (4), any monomial missing a variable x_C cancels in that coordinate. Its degree is at most m. Thus a fibre with c_I>m contributes zero. For c_I=m the only surviving terms use each cycle variable once, giving

    (-1)^((n-m)/2) times
    #{bijections beta from {1,...,m} to cycles(I): w_i lies inside beta(i)}.

The count is nonnegative. Choose I with m cycles and w_i inside its ith cycle. Every cycle contains a white face by the disk identity. That I contributes at least one. All nonzero contributions have the same sign, proving nonvanishing. Repeated choices of white faces cause no difficulty. This is a full proof of the regrouping step in orientation-fibre language.

`REFUTED`, as the proposed shortcut. The sum is not the ordinary rank-generating function of J(P) at a root of unity, nor its ordinary Mobius or Euler sum. Even when P is empty, there are two opposite-sign pairs above its one ideal, and F(1)=0. The rank polynomial of that lattice is 1. Moreover the octahedron and hexagonal-prism dual have the identical one-element lattice, but different polynomials, 1-z and z^2-1 with our weights. Their difference cannot be read from P. Generic distributive-lattice root-of-unity evaluations have no universal nonvanishing property: the two-element chain has rank polynomial 1+q, zero at q=-1.

An arbitrary decorated weighted sum can of course be written over any indexing set. Formula (4) identifies a useful general operation, a Boolean finite difference, but its positivity uses the cycle disks and the disk identity. It does not remove those inputs. No claim is made that all conceivable identities involving a decorated P are impossible.

## 5. Four exact examples

`COMPUTED`. `code/examples.py` produces `data/examples.json`, including the ideals, Hasse covers, cycle counts, signs and integer-weight polynomials. Put G(z)=z^(-minimum exponent)F(z). We preserve the computed overall sign.

| Example | P and rank polynomial of L | Pairs / tree pairs | G(z) | First nonzero coefficient of F(1+x) |
|---|---|---:|---|---:|
| Octahedron | Empty; 1 | 2 / 2 | 1-z | -1, degree 1 |
| Hexagonal-prism dual | Empty; 1 | 2 / 2 | z^2-1 | 2, degree 1 |
| Running V=13 | One point; 1+q | 8 / 6 | (z-1)^2 (z^2+z+1)(z^3+z^2+1) | 9, degree 2 |
| V=18 witness | Two incomparable points; 1+2q+q^2 | 20 / 12 | (z-1)(z+1)(z^2-z+1)(z^4-z^3-z^2-z+1)(z^6+z^5+z^4+z^3+z^2+z+1) | -14, degree 1 |

The requested `paper/figures/example.json` was absent. I reconstructed the V=13 graph from the identical face fixture in `research/2026-11-14_fable_figures-review/search_example_13.json`, and checked that its black faces at root {0,4,5} equal those in `research/2026-11-14_opus_manuscript-merge/example.json`. No author verification code was used. The chosen weights are independently constructed unit-circulation weights, so their polynomial need not equal an author's polynomial for other weights.

## 6. R2 fails under an explicit rigid-face gluing

`COMPUTED`, counterexample. `data/R2_glued_V33.json` gives the full rotation, black faces, all 16 orientations, face potentials, Hasse covers and tree-pair counts. `code/gluing.py` constructs it from two V=18 witnesses, and `code/second_certificate.py` independently enumerates all 2,916 states and all ordered state pairs. It confirms 400 pairs, 144 tree pairs and zero tree pairs on each of the ten distinct candidates formed by the extrema and irreducibles. The lattice is B_4. There are four successful elements, all at rank two.

The gluing removes the white face (1,2,9) from the first witness and its black root face from the second. For the second copy map its root vertices 0,6,5 to 1,9,2 respectively, and map its other vertices increasingly to 18,...,32. Preserve the first copy's root {0,5,6}. The white gluing face is H0 face 3 and has potential zero in all four first-copy orientations. This rigidity is essential to the product-order argument. Gluing into an arbitrary moving face does not automatically produce a product order.

`PROVED-HERE`, gluing lemma. Insert a black-rooted triangulation T2 into a white face f of a rooted triangulation T1. All pairs split as independent pairs on the pieces. To see this, let Y be the strictly inserted vertices. The inserted black faces other than the cap number |Y|, and every vertex of Y can only be matched to one of those faces. A state bijection therefore uses every inserted black face on a vertex in Y and uses no boundary vertex there. Restriction gives the two local states; conversely their union is a state. Disjointness is preserved.

The Q graph is the union of the two local Q graphs. Cycles in either piece persist. If both local Q graphs are rooted forests, each inner tree attaches at exactly one of the three boundary vertices, so their union is a rooted forest. Thus tree pairs also split, and both pair counts and tree-pair counts multiply.

For the lattice order, normalize the local potential in T2 to zero at its outer face. The global potential restricts to phi1 outside, and equals phi1(f)+phi2 inside. This follows by comparing differences across each spoke, including the rigid boundary spokes. If phi1(f) is constant over L1, the global componentwise order is exactly the product of the two local orders. This proves the product assertion under the stated rigidity hypothesis.

`PROVED-HERE`, conditional on the explicitly enumerated V=18 base certificate. The V=33 lattice is B_2 x B_2. A successful element must be a middle element in EACH factor. A join-irreducible of a product has a nonbottom entry in just one factor; a meet-irreducible has a nontop entry in just one factor. Some other factor is therefore a failing extreme. Both global extremes fail as well. This proves the failure of R2 from the base certificate without relying on a large search.

More generally, recursively insert a witness into the image of the same rigid face. At q copies the dual order is 15q+3, L=B_(2q), the number of pairs is 20^q, the number of tree pairs is 12^q, and exactly 2^q of the 4^q elements succeed. Success means choosing exactly one of each designated pair of Boolean coordinates. Every successful element has rank q and distance q from either extreme. A maximal chain can first fill both coordinates in one block, then proceed through the other blocks, avoiding success at every stage when q>=2. Thus the successful fraction is 2^(-q), and no fixed cover-distance bound from the extremes can suffice. The same rigid-face argument applies inductively, so these are all-q statements conditional only on the base finite certificate. `code/families.py` checks q=1,2,3 directly.

## 7. What the criterion does algorithmically

`PROVED-HERE`. A SPECIFIED PAIR can be tested in linear time. Construct the n arcs u(t)->r(t), or the 2n-spoke graph F. Run a topological-sort or DFS cycle test. If a cycle remains, return it as a certificate of failure. Otherwise Q_s is the required rooted forest. All exit choices are fixed, so there is no difficult side condition left to test.

The question for a SPECIFIED LATTICE ELEMENT u is existential. One must choose the directions of all c(u) D-cycles. A linear cycle test at one choice answers only that choice. The criterion gives the exact following SAT formulation. A directed cycle Z of O_u can be present in F only if, on each D-cycle it meets, all of its centre exits agree with one of that D-cycle's two directions. Otherwise Z can never be harmful. For each consistent Z, let S_Z be the set of D-cycles it meets, and let b_(Z,j) be the required direction. The condition for success is

    AND over consistent Z of OR over j in S_Z of (x_j != b_(Z,j)).       (5)

There may be exponentially many directed cycles and clauses, and clauses can involve many variables. Testing a full assignment is linear by the preceding algorithm, but that is a separation test for a chosen assignment, not a polynomial algorithm to find a satisfying assignment. The criterion alone supplies neither a bounded-width SAT reduction nor a tractable optimization theorem for this special clause family. It also supplies no NP-hardness proof for this special planar class. Calling the unrestricted subcube-covering problem hard would not settle this restricted problem.

`GAP`, algorithmic claim. Polynomial-time decidability of the existential question is not established by this criterion. The precise unresolved obligation is finding one globally consistent direction choice, rather than detecting its bad cycle after it has been chosen. A direct algorithm takes O(2^c(u) |T|). This is polynomial for bounded c(u), not in general. R2 would only have supplied polynomially many factors, still with this orientation-search obligation; the unrestricted R2 is now false anyway.

For completeness, the candidate list itself really is polynomial. In the difference system, J(f,k) is the least feasible potential with phi(f)>=k. It is join-irreducible: a join of two smaller solutions cannot reach its required threshold. Every join-irreducible equals some J(f,k), since an element is the join of the least solutions for its attained coordinate thresholds. Duplicates are identified. The dual statement gives meet-irreducibles. Shortest paths of length at most the number of faces minus one bound each coordinate range by O(|T|), so there are O(|T|^2) thresholds. This validates the list-size assertion and isolates the unsolved search over directions.

## Outcome

`PROVED-HERE`. The useful lattice reading is a directed-cycle involution BETWEEN decorated ideals and a Boolean Mobius finite difference WITHIN each ideal's direction fibre. The former explains the first cancellation. The latter reproduces the height proof's nonvanishing step. It gives neither a shorter general lattice proof nor a proof of R2. `REFUTED`: R2 itself fails on the explicit V=33 gluing.
