# Independent referee report

Referee: gpt-6-astra. Date: 2026-11-14. Status vocabulary follows `research/BRIEF.md`. A `CORRECT` verdict below validates the stated argument; it does not confer publication or human review. Results proved in this report remain `PROVED-HERE`, T2, AI-refereed with human review pending. Computations are `COMPUTED`; their range and limitations are explicit below.

## Audit boundary

The primary conclusion C0 is exactly OpenAI Proposition 5.1, called Theorem A in the submission: for every finite simple sphere triangulation with properly black-and-white-coloured faces and a specified outer black face, **if a pair of disjoint states exists, a pair with acyclic $Q_s$ exists**. No assumption excluding separating triangles is permitted. A state must be a bijection from nonouter black faces to nonroot vertices, incident at every choice.

The supplied route is PROOF.md Sections 0 to 3. Theorem B is its stronger intermediate conclusion. Sections 4 to 6 supply separate conclusions, so they have auxiliary roots in the graph below, not invented dependencies of C0. REPORT.md, ROUTES.md, DATA.md, the laboratory and its outputs are also audited for accurate descriptions of evidence and implications. Audited document hashes are in `code/additional.json`.

I read the entire eleven-page OpenAI paper in `papers/text/OpenAI-Barnette.txt`, opened the PDF, and checked the formulas and sliding argument on PDF page 7 visually. I read the relevant arguments in Li, Section 4 and Appendix B, and the constructive paper, Sections 2, 4, 5 and Lemma 6.1. `LIT` here identifies these supplied papers, not an independent assertion about peer review. The unverified historical attribution of vertex three-colourability to Heawood is not an accepted citation.

Accepted background is elementary finite graph theory, Euler's formula for a disk, the Jordan curve theorem and oriented intersection numbers, elementary permutation/determinant algebra, finite Boolean-cube expansion, Newton's identities, and complementary plane-tree duality as proved in OpenAI Lemma 2.1. Applications, including roots and incidence multiplicities, are checked below. I rechecked the submission's disk proof rather than accepting Proposition 5.1 or any equivalent forest-pair theorem as background.

The audit freezes the orientation convention: bounded facial boundaries are counterclockwise; $\delta(v,w)=+1$ means black on the left; a counterclockwise state cycle has $\delta$-sum $-3$. A height counts a centre-to-corner spoke crossing the directed path from right to left positively. Reflection reverses this convention's numerical heights and $J$, a point relevant to the counterexample tables.

## Obligation graph

All displayed groups are AND groups. The submission supplies one primary route to each claim here. No diagnostic or replacement proof is silently used to rescue that route.

```text
C0 forest pair exists
 <- R0 nonzero signed height test: O0, C1, C2, C3
C1 fixed-second-state cancellation
 <- R1 Q-cycle involution: O1, O2, O3, O4, C4
C2 height identity at degree m
 <- R2 regroup by D: O0, O5, O6, O7, C4, C5, O8
C3 some degree-m height test is nonzero
 <- R3 choose points in a minimum cover: O0, O9, C4, C2
C4 reformulated disk identity
 <- R4 matching/edge/Euler counts: O10, O11, O12, O13
C5 heights on an orientation cube
 <- R5 oriented intersections: O14, O15, O16, O17

C6 determinant interpretation, auxiliary root
 <- R6 determinant expansion and gauge: O18, C4, O19, O20, O21
C7 Hamiltonian-state dichotomy and injection, auxiliary root
 <- R7 split on whether W_s is a tree: O22, O23, O24, C8, C9
C8 unique Hamiltonian preimage of a tree matching
 <- R8 orient the white tree: O23, O25, C10
C9 non-tree W_s implies no partner for s_C
 <- R9 interior Euler deficit: O26, O27, O28, O29, O2
C10 selected face pairing is acyclic
 <- R10 contradictory disk balances: C4, O30, O31
C11 #TM >= 2m, auxiliary root
 <- R11 equal low moments and Newton: C2, C3, O32, O33
C12 3 #TM <= #HC, auxiliary root
 <- R12 count three disjoint images: C7, C8, O34
```

There is no circularity. In particular C4 uses the state bijection, not existence of a forest state; C5 uses elementary topology, not the weighted nonvanishing lemma; C9 uses the partner component count, not C0.

## Critical findings and exact repairs

### The main proof closes

`PROVED-HERE`. Sections 1 to 3 establish C0. The cited OpenAI sliding argument is available, applies with all its hypotheses, and discharges O16. It is not a gap. A self-contained presentation should include it; `REWRITTEN-PROP-5-1.md` does so. The finite-difference calculation is correct, including its final sign.

There are two editorial side conditions to spell out. Add "Assume a pair exists" to Theorem B. If no pair exists, $m$ is undefined, not zero. Theorem A is then vacuous and no minimum or witness face is chosen. Also say explicitly that the $w_i$ need not be distinct. They index factors and a bijection from labelled positions; nesting and repeated faces cause no problem.

`PROVED-HERE`. A pair has a cycle cover because both maps are bijections. Each vertex has indegree and outdegree one. A 2-cycle would require the same undirected edge twice, hence the same black face twice, which cannot occur. Each cycle has length at least three. The disk identity makes every length odd, hence $c\equiv J\equiv n\pmod2$. Thus $\varepsilon=(-1)^{(n+J)/2}=i^n i^J$ is a real sign.

`PROVED-HERE`. A partner's opposite-edge orientation gives a component with $v$ vertices and $a$ roots exactly $v-a$ edges. Connectivity implies $a\le1$. For $a=1$ it is a tree; for $a=0$ it is unicyclic. In the forest case the roots determine all orientations and the partner is unique. Isolated roots are allowed. A forest without a partner contributes nothing; the definition of tree matching deliberately includes existence of a partner.

`PROVED-HERE`. On a $Q_s$-cycle reversal, the identity $\delta(u,s)-\delta(r,s)=2\delta(r,u)$ has the correct sign. The directed cycle consists of edges chosen from the state $r$, so the disk identity applies, even though it is not a cycle of $D$. The change in $J$ is $\pm2$. Choosing the cycle using $s$ alone makes the operation involutive for every partner.

`PROVED-HERE`. For a cover with $c$ cycles, $\varepsilon=(-1)^{(n+c)/2}(-1)^{p}$, with $p$ the number of counterclockwise cycles. In a product of $j$ height factors, a surviving term must use every cycle variable. For $j<c$ there is none. For $j=c$, the assignments are bijections and the Boolean sum is $(-1)^c$. The total sign is $(-1)^{(n-c)/2}$, since the two exponents differ by $2c$. Repetitions among faces do not remove the labelled bijection multiplicity. The selected minimum cover supplies at least one such bijection.

### Heights, roots, and volume

`PROVED-HERE`. The submission's height is single valued after the paths are fixed. It is not an absolute, nonnegative, path-independent surface. It is a signed integer attached to a state and a white face. A generic piecewise-smooth path with finitely many transverse crossings exists in the plane avoiding the finitely many vertices and centres. Paths may intersect one another; nothing requires disjoint paths.

Here is the missing explanation behind the volume identification, supplied by this referee. For any two states $s,s_0$, the formal difference of their selected oriented spokes is a closed integral 1-chain: its boundary at every centre cancels, and its boundary at every nonroot cancels by bijectivity. It has zero boundary at roots because neither matching uses them. Its intersection with a path from $w$ to the outer face therefore depends only on the endpoints. Equivalently, it is the winding function of that closed chain, zero in the exterior. Changing $\gamma_w$ changes all $h_s(w)$ by the same constant. The normalized differences $h_s(w)-h_{s_0}(w)$ are intrinsic to the oriented embedding.

`PROVED-HERE`. The full spoke graph $H$ has one face for each white triangle. Deleting the outer black centre merges the three distinct adjacent white faces into the exterior. It leaves a connected graph $H_0$. To check connectedness directly, each outer edge $ab$ has a white face $abz$ on its other side. The sides $az,zb$ route through black centres other than $t_0$, joining $a$ to $b$ in $H_0$. All roots are therefore joined. Every component after deleting the outer centre contains a former neighbour of that centre, since $H$ was connected. Hence all components coincide. Its bounded faces correspond exactly to white faces not sharing an edge with $t_0$, of which there are $n-2$.

The sum of the path intersection cochains has circulation $1$ on each bounded face of $H_0$. Any other weights with those same face circulations, in particular OpenAI Lemma 5.3's unit-face prescription, differ by a vertex potential on this connected plane graph. Summing the potential difference over a state gives

$$
\sum_{x\in X}\phi(x)-\sum_{t\in A}\phi(t),
$$

which is independent of the state. Thus $\omega(s)=\sum_w h_s(w)+K$ for a constant $K$, and $L_+(C)-L_-(C)=\#\{\text{white faces inside }C\}$. Arbitrary positive face circulations would give a weighted area, not this unweighted count. Correct the prose to say "signed volume, up to an additive constant, for unit bounded-face circulation."

`PROVED-HERE`. Every relevant directed cycle avoids the roots because roots have outdegree zero. It cannot enclose a root because that root is incident with the outer face, or because the un-crossed outer triangle joins all roots to the exterior. The disk count uses all faces with interiors in the bounded disk, including faces incident with its boundary, not merely faces with all vertices strictly inside. It gives $W=B+1\ge1$, including $B=0$. A white face sharing an outer edge cannot be enclosed, since it contains roots. Hence every witness face is one of the permitted inner white faces. Inner white faces may themselves touch a root; they simply never serve as enclosed witnesses.

### Determinants: correct formula and a stronger simplification

The detailed Proposition 5 is `CORRECT`. The informal assertion that the complex partner sum literally equals an ordinary incidence determinant is `CORRECT AFTER FIX`. With the notation of PROOF.md Section 4, the exact equalities are

$$
\sum_r i^{J(r,s)}=\sigma\det N_s,\qquad
N_s\Omega=\operatorname{diag}(\rho_t)d_s.
$$

The common permutation sign $\sigma$ is justified by constructive-paper Lemma 6.1. For completeness, nontrivial cycles of the relative permutation of two states are state cycles after completing unused faces arbitrarily. The disk identity makes their lengths odd, so their permutation signs are positive. This also covers states with common choices.

`PROVED-HERE`, referee's simplification. Orient each row of $d_s$ positively at the opposite corner of colour $\operatorname{col}(s(t))+1$ and negatively at the other corner. Then

$$
\rho_t=\frac{1-\omega_3}{\sqrt3}\omega_3^{\operatorname{col}(s(t))+1}.
$$

Since $s$ is bijective, $\sum_t\operatorname{col}(s(t))=\sum_{x\in X}\operatorname{col}(x)$. Therefore

$$
\det N_s=i^n\det d_s,\qquad
\mu(s)=\sum_r\varepsilon(r,s)=(-1)^n\sigma\det d_s.       \tag{A}
$$

The factor in the real signed identity is independent of $s$, stronger than the submission states. The check of the local complex row identity and the integer determinant check are separate in the verifier. The determinant is taken after deleting all three root columns. Identifying those roots turns it into a square reduced incidence matrix on $n+1$ vertices. Its determinant is $0$ unless the contracted graph is a tree, when it is $\pm1$. A root-root edge becomes a zero row; a component with no root also forces singularity. One must not replace this criterion by "acyclic" for an arbitrary choice function lacking a partner.

`PROVED-HERE`. The vertex colouring needs no historical attribution. Modulo 3, the antisymmetric cochain $\delta$ sums to zero around every facial boundary, because those sums are $3$ or $-3$. Facial boundaries span the cycle space of a sphere embedding. Define $\operatorname{col}(v)$ by integrating $\delta$ modulo 3 from a fixed vertex. It is path independent and increases by 1 across every black-left oriented edge. This proves the required colouring and its winding interpretation directly.

The Section 4 magnetic-coefficient and Fourier identities are also algebraically correct. The multilinear coefficient forces one edge per black face, and odd cycle lengths make each permutation sign positive. In the Fourier identity the factor $1-\omega_3^{\operatorname{col}(r)-\operatorname{col}(s)}$ kills shared choices. These auxiliary identities are not needed by C0, and I do not claim a new exhaustive check of them.

### Lemma 6.2 and the Hamiltonian-state dichotomy

`PROVED-HERE`. The short disk proof of acyclicity is correct. In a proposed directed cycle, the matching $P$ pairs the $B-\ell$ black faces whose selected edge is not on the boundary with the $W-(h-\ell)$ white faces of that kind. Each face is counted once because $P$ has exactly one edge in each face. Thus $W-B=h-2\ell=3$, contradicting $W-B=1$. Boundary chords count internally on both sides and cause no exception. To obtain the full statement of OpenAI Lemma 6.2, append the omitted final sentence: $P_0$ has one root in each component by the outdegree count, so adding $e_0$, which joins two roots, preserves acyclicity. The submission explicitly states only the $P_0$ conclusion. Its proof actually needs no tree-matching hypothesis beyond the stated existence of a compatible face pairing and a state.

`PROVED-HERE`. Section 6's Proposition 7 is correct. Its most delicate Euler count survives independent reconstruction. Here are the details that should be retained when shortening it.

1. A Hamiltonian cycle avoiding $e_0^*$ gives two primal trees by complementary plane duality. The third root lies on the other side from the endpoints of $e_0$, because the other two sides of $t_0$ are crossed. Removing $e_0$ splits its tree and leaves three trees, each with one root. Orienting toward the roots uses every nonroot as a tail exactly once. Each edge belongs to one black face and $e_0$ is the only one from $t_0$, so these tails define a state.
2. Regard $W_s$ as an embedded multigraph, retaining edge identities. It has $n+1$ white vertices and $n$ edges. Complementary tree duality gives that $W_s$ is a tree exactly when $Q_s$ is a rooted forest. A rooted forest itself supplies its unique partner, so this is the submission's definition of tree matching. OpenAI Section 6.1 is stated in the surrounding no-separator case, but this equivalence uses no such assumption.
3. If $W_s$ is a tree, assigning every edge to its endpoint away from the white root is the unique assignment using every other white vertex once and omitting the root. Both the original Hamiltonian complement and the constructed complement have that assignment. They coincide. This proves uniqueness as well as the left inverse needed for injectivity.
4. If $W_s$ is not a tree, its edge count implies that it contains a cycle. Realize a simple cycle as a Jordan curve $\Gamma$, passing through distinct white faces and distinct black faces $t_1,\ldots,t_k$. It crosses the two sides of $t_i$ incident with $s(t_i)$. It meets no side of $t_0$, so all roots lie in its exterior. No edge of $Q_s$ crosses it. Parallel-edge cycles, if present, are handled with their distinct embedded arcs.
5. The $k$ cut black faces use selected $P$-edges to match $k$ distinct cut white faces, exhausting those white faces. Therefore all wholly interior faces are matched to wholly interior faces and $B_{\rm in}=W_{\rm in}$.
6. Let $S$ be the interior vertex set, $\sigma=|S|$, and let $a$ count cut black faces whose selected corner is inside. Counting edges by their unique black face gives $e(S)=3B_{\rm in}+k-a$. Faces with the selected corner outside have their other two corners inside and contribute the one internal side. Those with the selected corner inside contribute no internal side.
7. Clip the triangulation along $\Gamma$. Its cell decomposition has $\sigma+2k$ vertices, $e(S)+4k$ edges, and $B_{\rm in}+W_{\rm in}+2k$ faces. The $4k$ comprises $2k$ clipped crossing edges and $2k$ boundary arcs. Euler on this disk gives $\sigma=B_{\rm in}+k-a+1\ge1$. This justifies both the count and nonemptiness of $S$.
8. Exactly $B_{\rm in}+k-a=\sigma-1$ edges of $Q_s$ lie on $S$. None leave $S$, which contains no root. If a partner existed, every component there would be unicyclic by Lemma 2, hence would have as many edges as vertices, totaling $\sigma$. Contradiction.

These steps establish the submitted route, without appealing to a different theorem to bypass it. The factor-three bound is then correct: every Hamiltonian cycle omits exactly one of the three edges at $t_0^*$, so the three sets receiving the injections are disjoint and exhaust all Hamiltonian cycles.

### Counterexamples and claims exceeding their evidence

`COMPUTED`, `REFUTED`. All four explicit face-list witnesses in `data/counterexamples.txt` were reconstructed independently. The exact top state, bottom state, and two states of the bad 16-vertex cover match. Absolute ranks can differ by a common additive constant because our paths differ. The 14-vertex polynomial witness gives exactly

$$
Z(q)=-1+2q+q^5-2q^6,\qquad
Z(q)/(q-1)=1-q-q^2-q^3-q^4-2q^5.
$$

The following corrections are necessary.

- **Reflection error.** The statements "lowest first fails at 14" and "all-clockwise minimum cover first fails at 13" are false as embedding-independent minimum-size claims. Reverse every face tuple of the printed 12-vertex example. Its same bad state is now lowest, and the same minimum cycle runs clockwise. In formulas, $h'_s(w)=-h_s(w)+K_w$ and $J'=-J$. Both failures therefore already occur at 12 vertices. `code/additional.json` records the reflected face list and results; `code/up_to_12.json` independently found both failures through plantri. The author's counts are counts for chosen oriented representatives, not all orientations. An enumeration identifying reflections is insufficient for orientation-sensitive universal claims unless both representatives are checked. The corresponding highest and counterclockwise first failures remain at 12; the exhaustive smaller cases have only forest partnered states.
- **Single-cover overclaim.** The 16-vertex example proves that an arbitrary specified cover, even a minimum-cycle cover, need not have a forest orientation. It does not prove "no proof can work inside one D" or that inter-cover cancellation is logically necessary for every proof. Replace the lesson by "A method starting from an arbitrary cover cannot guarantee success using only reversals of that cover's cycles." Its two other covers have forest pairs. Choosing a successful cover by another argument is not excluded.
- **Cube overclaim.** Mixed signs in $Z/(q-1)^m$ refute a decomposition into uniformly signed, rank-compatible unit-step cubes. They do not by themselves refute a partition into abstract cubes, or cubes with differing base signs. In particular the printed example has $m=1$ and ten tree matchings, a set that certainly can be partitioned into five two-element sets. State the rank and sign requirements of the proposed decomposition before calling it refuted.
- **Unbounded-degree overclaim.** Observing $c_{\min}=2,3,4$ does not prove that $c_{\min}$ is unbounded. Replace "So the degree of the test function cannot be bounded in advance" by "These examples rule out restricting this test to degree one, and exhibit required degrees up to four." An infinite-family argument would justify unboundedness, but none is supplied.
- **Weight overclaim.** Functions of $s$ alone are sufficient for fixed-$s$ cancellation. They are not the only possible weights: invariance under the chosen $Q_s$ involution suffices. Replace "and nothing else can" in ROUTES Section 8 by this exact sufficient condition.

`COMPUTED`, `REFUTED`, referee's replacement witness. The abstract cube-partition claim is nevertheless false, for a different and simpler reason. `code/cube_cardinality.json` gives a 13-vertex rooted triangulation with six tree matchings and $m=2$. Six elements cannot be partitioned into four-element cubes. The output lists every state, pair and tree matching, and the command `code/cube_witness.py` reconstructs it independently from plantri. This supplies a valid cardinality refutation; it is not the submitted 14-vertex polynomial argument.

`COMPUTED`, `REFUTED`. The remaining concrete claims have independent small witnesses in `code/up_to_12.json` and `code/up_to_16.json`: rank-parity sign at 8 vertices, noninjectivity of the Hamiltonian-cycle-to-state map at 8, $c_{\min}=1$ at 9, and the assertion that the top state has a partner at 10. The specified 12-vertex map refutes the top partnered state, counterclockwise minimum-cover choice, and maximal rank-difference choice. The specified 14-vertex bottom-state witness remains valid, as does the clockwise failure at the claimed size, but they are not smallest once reflection is included. New witnesses use independent plantri indices, not the author's class numbering. I do not certify an unpublished face list merely from its class number.

## Claim-by-claim verdicts

| User claim | Verdict | Exact scope and status |
| --- | --- | --- |
| 1. Weight-free proof of Proposition 5.1 | CORRECT | `PROVED-HERE`. Sections 1 to 3 close. "Weight-free" means no assigned positive spoke circulation; signed intersection counts still serve as incidence coefficients. |
| 2. $J$, cycle orientation, colour winding | CORRECT | `PROVED-HERE`. CW minus CCW with the given convention. The direct colouring proof above removes the unsupported historical attribution. |
| 3. Partner sum is an incidence determinant | CORRECT AFTER FIX | `PROVED-HERE`. Detailed Proposition 5 is correct. Use equation (A) for the real signed sum, and $\sigma i^n\det d_s$ for the complex sum. |
| 4. Disk identity and Lemma 6.2 | CORRECT AFTER FIX | `PROVED-HERE`. Both counts and the $P_0$ proof are correct. Append the root-component argument to recover the published conclusion that $P$ itself is a forest. |
| 5. Height and volume | CORRECT AFTER FIX | `PROVED-HERE`. Fixed paths define signed heights; normalized differences are path independent. Volume agrees up to a state-independent constant for unit face circulation. Explicit justification is supplied above. |
| 6. Theorem B | CORRECT AFTER FIX | `PROVED-HERE`. Add the nonempty-pair hypothesis. All signs and labelled multiplicities are correct. The comparison with Li is structural, not an equality of its distinct-mark set with ordered power moments. |
| 7. Hamiltonian-state dichotomy | CORRECT | `PROVED-HERE`. The Euler deficit proof closes, including its nonempty interior and absence of roots. |
| 8a. #TM ≥ $2c_{\min}$ | CORRECT | `PROVED-HERE`. Degree-zero moment balances signs; Newton's identities applied to equally sized multisets yield the bound. |
| 8b. #TM ≥ $2^{c_{\min}}$ | GAP as a theorem | `CONJECTURE`, with independent `COMPUTED` evidence in the recorded range. The submission correctly labels it a conjecture. This audit supplies no general proof. |
| 8c. $3\,\#TM\le\#HC(G)$ | CORRECT | `PROVED-HERE`. This is already proved in the submission, not merely conjectured as the question's list might suggest. |
| 9. Concrete refutations | CORRECT AFTER FIX | `COMPUTED`, `REFUTED`. Exact examples work; reflection changes two minimum-size claims, and the broad proof-impossibility/cube/unboundedness lessons exceed the evidence. |

For the $2m$ bound, the only nontrivial arithmetic side condition is that the positive and negative multisets have the same finite size $N$, supplied by the degree-zero identity. If $N<m$, equality of moments through $m-1$ includes the first $N$ moments. Newton then determines both monic degree-$N$ polynomials, so the multisets coincide. Their nonzero signed $m$-th moment is a contradiction. The case $N=0$ is already excluded by nonvanishing. This proof does not require integral or nonnegative heights.

## Independent computation

The verifier was written from the definitions in this referee folder. It never imports or executes the author's `lab/`. The four printed face lists are input data, not imported results. Generation uses the third model's pinned plantri executable with `-ba`, which generates simple Eulerian triangulations including separating triangles. Every face is used as outer face, recolouring accordingly. The executable hash and actual commands are in the JSON outputs.

The first completed exhaustive run through 12 vertices covers 15 unrooted classes and 262 roots, with 1,706 states, 624 ordered pairs, 620 tree matchings, 1,120 directed $D$-cycle occurrences, four directed $Q_s$-cycle occurrences, and 4,360 commutative height monomials of degrees $0$ through $m$. Repeated face factors are included. It checks every monomial, not random samples. It independently enumerates Hamiltonian cycles as complements of all perfect matchings of the cubic dual, testing connectivity, and obtains 4,784 root/cycle incidences. This includes roots with no pair, where Theorem B is skipped and the Hamiltonian dichotomy is still checked.

`code/additional.py` checks the disk identity on all directed cycles available from every state through 12 vertices, not just pair cycles; compatible face pairings for Lemma 6.2; the exact signed determinant formula; and rank equality up to a constant against `workings/barnette_lab/`'s separate embedded-spoke implementation. `code/additional.json` records these counts and the reflected explicit examples. `code/up_to_16.json` extends the main checks to 16 vertices and records all per-root totals. `code/README.md` gives final totals and reproduction commands.

All combinatorial tests, heights, cycle-area differences, moments, Hamiltonian checks and reduced incidence determinants are exact integer operations. The twisted complex determinant and local gauge identity use floating point with tolerances $10^{-8}$ and $10^{-10}$; they are backed by the separate exact formula (A). No numerical tolerance enters the nonvanishing or state classification tests. Plantri's completeness is accepted as a generator contract, not formally verified here. Matching class counts and rooted profile multisets with the independently generated author data supports, but does not constitute a theorem about, the author's two generating moves for all sizes. Reflection-sensitive tallies should not be compared without aligning orientation.

## Comparison of the three supplied arguments

`LIT`. OpenAI Sections 5.1 to 5.3 use fixed-$s$ cancellation, unit face circulation, and the least-degree term of a finite exponential sum. The constructive paper Theorem 5.2 uses the same two regroupings for an integer polynomial near $z=1$, and Section 5.1 turns power moments into ordered token lists for an algorithm. Li Section 4 and Appendix B use ray intersections and two involutions. Li's marks are sets of distinct intersections in Definition 14; for $m>1$ their signed test is an elementary-symmetric expression in crossing signs, not literally $\omega(s)^m$. With ordered marks and repetition, one obtains power moments instead. The common content is fixed-second-state cancellation followed by orientation cancellation and same-sign minimal-cycle survivors.

The height-product version is shorter and clearer for a reader comfortable with oriented intersections. It removes the construction of a globally positive circulation, complex phases, Taylor language, and the token transport order. It does **not** remove the disk identity, the two regroupings, the local spoke deformation, or the choice of a minimum cycle count. Those are the work of the proof. Claiming an independent new combinatorial mechanism would overstate the result. Calling it a useful compression and localization of the existing mechanism is accurate.

The replacement proof uses the disk identity, signed paths to chosen white faces, and one multilinear expansion. It leaves out all partner-count classification and determinant material because neither is needed to prove existence. The remaining topology is stated explicitly rather than concealed in the word "height". This is the version I recommend for the exposition. The constructive paper remains preferable when an actual finite search walk, rather than an existence proof, is the objective.

## Dependency table

Each unique obligation has one primary classification. "Discharged" concerns the specified proof route and accepted boundary, not computer verification alone.

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | A forest pair exists whenever a pair exists | root | R0 | root | C1, C2, C3, O0 | discharged |
| C1 | Fixed-$s$ signed sum vanishes except at tree matchings | C0 | R1 | major claim | O1 to O4, C4 | discharged |
| C2 | Height products below $m$ vanish; degree $m$ gives signed N | C0, C3, C11 | R2 | major claim | O5 to O8, C4, C5 | discharged with explicit nonempty domain |
| C3 | Some degree-$m$ product has a nonzero sum | C0, C11 | R3 | major claim | O0, O9, C4, C2 | discharged |
| C4 | $W=B+1$, $h-2\ell=3$, odd lengths and orientation sums | C1, C2, C3, C6, C10 | R4 | major claim | O10 to O13 | discharged |
| C5 | CCW reversal adds the enclosed-face indicator to heights | C2 | R5 | major claim | O14 to O17 | discharged |
| C6 | Twisted determinant and reduced-incidence interpretation | auxiliary root | R6 | root | O18 to O21, C4 | discharged |
| C7 | HC states with a partner are exactly tree matchings | auxiliary root, C12 | R7 | root | O22 to O24, C8, C9 | discharged |
| C8 | Each tree matching has a unique HC preimage per outer edge | C7, C12 | R8 | major claim | O23, O25, C10 | discharged |
| C9 | Non-tree $W_s$ for an HC state forbids a partner | C7 | R9 | major claim | O26 to O29, O2 | discharged |
| C10 | Compatible selected edges $P_0$ are acyclic | C8 | R10 | major claim | C4, O30, O31 | discharged |
| C11 | #TM is at least $2m$ | auxiliary root | R11 | root | C2, C3, O32, O33 | discharged |
| C12 | $3\,\#TM\le\#HC$ | auxiliary root | R12 | root | C7, C8, O34 | discharged |
| O0 | Nonempty finite pair set has a positive minimum cycle count | C0, C2, C3 | R0/R2/R3 AND | hypothesis | Theorem A hypothesis, finite simple graph | discharged |
| O1 | Opposite edges are distinct and partner tails exhaust X | C1 | R1 AND | definition | Unique black face per edge and bijection | discharged |
| O2 | Partnered components are rooted trees or rootless unicycles | C1, C9 | R1/R9 AND | algebraic/logical step | $e=v-a\ge v-1$, connectedness | discharged |
| O3 | Selected $Q_s$ cycle is directed and reversal preserves a partner | C1 | R1 AND | side condition | Outdegree constraints; same head and tail set | discharged |
| O4 | $s$-only cycle selection gives fixed-point-free sign reversal | C1 | R1 AND | algebraic/logical step | Local delta identity plus C4; selection unchanged | discharged |
| O5 | D is a simple cycle cover and its orientations are precisely its pairs | C2 | R2 AND | side condition | Two bijections; unique black supplying face | discharged |
| O6 | $c\equiv J\equiv n\pmod2$, epsilon defined, cube sign correct | C2 | R2 AND | algebraic/logical step | Odd lengths from C4 and $J=c-2p$ | discharged |
| O7 | Both regroupings are of the same finite sum | C2 | R2 AND | algebraic/logical step | Finite pair partition by s or undirected D | discharged |
| O8 | Boolean product sum kills missing variables and counts bijections | C2 | R2 AND | algebraic/logical step | PROOF Section 3 expansion, labelled factor indices | discharged |
| O9 | Each minimum cycle has an admissible enclosed white face | C3 | R3 AND | proved earlier | C4 plus root exclusion in O10 | discharged |
| O10 | State cycles avoid/enclose no root, so all disk black faces are in A | C4 | R4 AND | side condition | Roots have no outgoing edge and touch outer face | discharged |
| O11 | $B=I+\ell$, counting every matched boundary vertex exactly once | C4 | R4 AND | algebraic/logical step | State injectivity and surjectivity; unique outgoing face | discharged |
| O12 | $E=3B+h-\ell=3W+\ell$ with all boundary incidences | C4 | R4 AND | algebraic/logical step | Opposite face colours and simple disk boundary | discharged |
| O13 | Disk Euler formula and orientation convention apply | C4 | R4 AND | named theorem | Jordan disk; Euler; left side CCW | discharged |
| O14 | Fixed generic paths give finite integer height sums | C5 | R5 AND | definition | Finitely many spokes, endpoint choices and transversality | discharged |
| O15 | Difference of height sums is intersection with the spoke detour | C5 | R5 AND | algebraic/logical step | Head minus tail spokes; unchanged terms cancel | discharged |
| O16 | Detour is simple, orientation preserving, and encloses the same white faces | C5 | R5 AND | named theorem | OpenAI Section 5.3 sliding argument, one edge per black face checked | discharged |
| O17 | CCW Jordan intersection is initial-inside minus final-inside | C5 | R5 AND | named theorem | Oriented intersection theorem, exterior endpoint | discharged |
| O18 | All states have one permutation sign, including shared choices | C6 | R6 AND | named theorem | Constructive paper Lemma 6.1, C4 supplies odd relative cycles | discharged |
| O19 | The colour cochain is integrable modulo 3 on the sphere | C6 | R6 AND | algebraic/logical step | Facial delta sums vanish modulo 3; proof above | discharged |
| O20 | Local complex gauge equality, determinant factors and orders | C6 | R6 AND | algebraic/logical step | PROOF Proposition 5 row calculation; formula (A) above | discharged |
| O21 | Reduced incidence determinant detects one-root-per-component forests | C6 | R6 AND | named theorem | Reduced incidence tree lemma after root identification | discharged |
| O22 | HC complement yields two trees and removing e0 separates the roots | C7 | R7 AND | named theorem | Plane cycle/tree duality, prescribed outer crossings | discharged |
| O23 | $W_s$ is a tree iff $Q_s$ is a rooted forest | C7, C8 | R7/R8 AND | named theorem | OpenAI Section 6.1 complementary spoke-tree duality | discharged |
| O24 | Tree versus non-tree case split is exhaustive | C7 | R7 AND | algebraic/logical step | Finite graph dichotomy | discharged |
| O25 | Edge-to-child assignment is unique on a white tree | C8 | R8 AND | algebraic/logical step | Leaf elimination or root orientation | discharged |
| O26 | Non-tree $W_s$ has a simple embedded cycle avoiding t0 and roots | C9 | R9 AND | side condition | $e=v-1$, Jordan realization, unchanged outer triangle | discharged |
| O27 | Cut-face matching forces $B_{in}=W_{in}$ | C9 | R9 AND | algebraic/logical step | k distinct selected boundary pairings exhaust cut white faces | discharged |
| O28 | Interior Euler count yields $\sigma=B_{in}+k-a+1\ge1$ | C9 | R9 AND | algebraic/logical step | Clipped disk cell counts spelled out above | discharged |
| O29 | Q has $\sigma-1$ internal edges and no edges leaving S | C9 | R9 AND | algebraic/logical step | Only crossed sides meet selected corner; opposite side uncut | discharged |
| O30 | A $P_0$ cycle is directed from the state s | C10 | R10 AND | side condition | Outdegree one on X, zero on roots | discharged |
| O31 | Selected face pairing would require $W-B=h-2\ell$ | C10 | R10 AND | algebraic/logical step | Distinct boundary selections; internal pair cancellation | discharged |
| O32 | Summing height monomials gives equal scalar moments below m and nonzero at m | C11 | R11 AND | algebraic/logical step | Finite expansion of $(\sum_w h_s(w))^j$, positive enclosed areas | discharged |
| O33 | Equal first N power sums determine a size-N multiset | C11 | R11 AND | named theorem | Newton's identities over characteristic zero; j=0 gives equal size | discharged |
| O34 | HC avoidance sets at the three incident outer edges partition all HC | C12 | R12 AND | algebraic/logical step | A Hamiltonian cycle has degree two at that cubic vertex | discharged |

## Verdict

**FOLLOWS.** The supplied primary route to Proposition 5.1 closes at C1, C2 and C3. In particular the potentially delicate detour obligation O16 is discharged by the cited, available sliding argument with its exact hypotheses checked. The independent Section 6 route closes at O27 to O29; it has no missing Euler or root assumption. Theorem B needs its nonempty-pair domain stated explicitly, and the summaries need the normalization and scope corrections listed above. The conjectured exponential lower bound remains open. The false minimum-size and broad impossibility claims are not dependencies of the main theorem and do not invalidate it.
