# Induction referee

## Audit boundary and exact statements

The audited sources are Astra's G.md, X.md and PARTIAL.md, plus Fable's RESIDUAL-CASES.md Theorems 3 and 4 and MISSING-LEMMA.md. I also read the supplying lift and rotation proofs in Opus PROOFS.md sections 0-3. This is a fresh instance of Astra, not a different model family from that report's author. It supplies independent reasoning and a new implementation.

Let x be a nonroot degree-four vertex with cyclic neighbors a,p,b,q and black faces xap,xbq. M identifies p,q and N identifies a,b. A good state means that Q_s is a forest with three distinct rooted components, equivalently that adding two root edges produces a tree. Forestness alone is not the definition for unpaired states. Contractions keep face identities and may have parallel edges in intermediate tests.

Accepted inputs are elementary planar graph topology, Euler's formula, Hall's capacitated matching criterion, and the previously refereed criterion that a rooted simple Eulerian triangulation admits a pair precisely when no separating triangle has black inner boundary. The source OpenAI Proposition 3.1 proves the separator-free case. The stronger pair criterion is an explicitly imported project result, not claimed to be Proposition 3.1 itself.

## Deficiency formula, line-by-line

PROVED-HERE, CORRECT. For S contained in the nonroots and connected K=T[U], U=V(T)\S, the formula is

    f(S)=sum_F (d_F+w_F-6)/3,

where F runs over nonactual face regions of K, boundary edge sides are counted with multiplicity, and w_F counts white incidences on the region side.

G1 first equality: each black triangle with j vertices in U contributes shortfall max(0,j-1) from two. For j=0,1,2,3 these are 0,0,1,2, precisely its induced-edge count minus its indicator of being wholly in U. Summing, and using V-2 black faces, gives f=2|U|-4-e(U)+b(U). The root contributes zero to the original Hall sum and one to b(U), so it is correctly included in that identity.

Euler line: connectedness gives p-m+b+w+h=2, where h is the number of nonactual regions. Side counting gives 2m=3b+3w+sum d_F. Color balance gives w-b=sum beta_F, and internal cancellation gives 3 beta_F=d_F-2w_F. Substitute the first two equations into 2p-4-m+b to obtain one half of sum(d_F-4-beta_F), then substitute beta_F. Each sign is correct. Bridges are handled by the edge-side convention; no simple-boundary assumption is used. The root-only triangle has one actual black face and one nonactual region, which the same derivation covers. For disconnected U the Euler constant changes; do not remove the connectedness hypothesis.

' Machine-checked' should mean computationally verified algebra and finite examples here. A SymPy residual and a census are not a formal proof certificate for all triangulations. The written counting proof is the general proof.

PROVED-HERE, G2 and G3 CORRECT. If the merged vertex is absent from S, the two deleted black faces contribute exactly [a in S]+[b in S]. If it is present, replace it by p,q,x. The surviving faces have the same intersection counts because no surviving face contains both p and q. The two deleted contributions total four, canceling the four added units of demand. A merged root cannot belong to S. With f_T>=0, negativity is therefore possible only in the first case, with f_T=0 and one or both a,b present, or f_T=1 and both present. The stated tight-set obstruction follows.

## Four- and five-cycle classification

PROVED-HERE, CORRECT with the separator-free hypothesis retained. For merge M, failure of simplicity is equivalent to a common neighbor y of p,q outside {x,a,b}. It produces the chordless four-cycle x,p,y,q. The opposite-neighbor edge pq is impossible by signed triangular side counting, so no loop case was omitted. Conversely the common neighbor gives a surviving parallel pair.

For a simple contraction, a new separating triangle must contain the merged vertex. Its two incident edges lift to different split copies, otherwise the triangle was facial before contraction and survives as a face. Thus it lifts to x,p,y,z,q. The five vertices are distinct. A chord pz or yq would again make the triangle facial before contraction; a chord xy or xz forces a link vertex a or b and the same contradiction. The absent pq is the remaining chord. Conversely a chordless such pentagon puts a,b strictly on opposite sides; its image separates. At x the two disappearing boundary incidences have opposite colors. The image's inner three incidences are all black exactly when the original pentagon's root-free side has four black and one white incidence. The imported pair criterion finishes the equivalence. Four-cycle obstructions make parallel edges, not separating triangles. A four-cycle-only formulation is WRONG.

PROVED-HERE, curvature claims CORRECT. Euler gives E=3I+2d-3, hence sum_interior(6-deg)+sum_boundary(4-k_v)=6. Isolating degree-four vertices yields G4. Chordlessness forces each boundary vertex to have an interior neighbor for a nonempty disk with d>=4. The alternating fan has k_v-1 triangles. Equal end colors force even k_v>=4; different colors force odd k_v>=3. This yields 2n4>=6-c. Four sides have two white incidences by divisibility, hence at most four changes and at least one interior degree-four vertex. Five sides have one or four white incidences and exactly two changes, hence at least two such vertices. A black six-sided boundary has no changes and at least three. These statements do not select an unblocked vertex.

PROVED-HERE, restricted G CORRECT. If both merges at x were nonsimple, a common-neighbor path between a,b would cross the four-cycle through p,q. It must meet its extra vertex, producing a second apex adjacent to all four link vertices. With no separating triangle all four triangles there are facial. Together with the four at x they exhaust a sphere, so the graph is the octahedron. For V>6 at least one merge is therefore simple. In the absence of chordless pentagons the exact classification says that this merge retains a pair. Euler supplies at least six degree-four vertices, so at least one is nonroot. This proves the claimed stronger statement for every nonroot degree-four vertex in that restricted class.

## Lift, rotation, exceptions and counts

PROVED-HERE, CORRECT. A contracted state lifts uniquely by following the supplying face of the merged vertex back to p or q and assigning the unused split copy and x to the two local black faces. Opposite neighbors are nonadjacent, so a surviving face cannot contain both split copies. Root merges have exactly one root copy and obey the same rule.

For the type with local assignments x,q, splitting the augmented contracted tree gives a two-component forest F with p in K1 and q in K2. The original augmented Q consists of F plus ap and the leaf edge xb. It is a tree exactly when a is in K2. If the lift fails, the black face g=aqc cannot choose q, already used locally; if it chose c, its opposite edge aq would put a in K2. Thus it chooses a. Rotating the three assignments x,q,a to a,x,q is a valid state and changes the augmented graph to F-qc+ac+bq+xp. Removing qc divides K2 into K2' containing q and K2'' containing c. Since a is in K1, ac joins K1 to K2''. The rotation is good exactly when b is outside K2'. No assumption c!=b is needed.

PROVED-HERE, rotation bijection CORRECT. An exception means both failures, so a,p lie in K1 and b,q in K2'. After the rotation these pairs remain separated. The missing outer corner changes q to a, so this outer state contracts to a good state under N. Its lift to T is the nongood rotated state. The N rotation uses the same g and reverses the three assignments, returning the original nongood lift. Therefore it is an N exception and the maps are mutual inverses. The mirrored case handles missing p. This is an actual bijection, not merely equality of counted exceptions.

PROVED-HERE, counting inequality CORRECT. The successful M lifts and successful N lifts have different local types. Rotated failing M lifts have N type, but their N projection is nongood: the relevant two split vertices remain in the same component. Thus they cannot collide with direct N lifts. The mirrored argument separates rotated N images from M lifts. Rotation is injective on each type because the three assignments are recoverable. The four image sets are disjoint and have total size

    #good(T/M)+#good(T/N)-|E_M|-|E_N|.

With e=|E_M|=|E_N| this proves #good(T)>=#good(T/M)+#good(T/N)-2e. In particular, if the other contraction has no good state, there are no exceptions and the one-sided inequality follows. A nonsimple contraction has no pair by the two-sided parallel-edge disk Hall obstruction in RESIDUAL-CASES Lemma 1; its disk has B=I and one boundary black triangle contributing at most one instead of two.

WRONG as an inference, corrected in Astra X.md. Theorem 4(c) says that absence of good states upstairs forces all contracted good states to be exceptional. It does not prove the converse. Thus the claim in MISSING-LEMMA.md that ML2 is equivalent to existence upstairs does not follow. Nor does equality |E_M|=|E_N| make the separate assertions 'some nonexception in M' and 'some nonexception in N' equivalent, since the two total counts may differ. Use the symmetric sufficient condition that at least one side has a nonexception. Astra's formulation uses that condition correctly.

CORRECT AFTER FIX, scope of RESIDUAL-CASES Proposition 2. Its sentence that all states of T correspond to outer states is stronger than its definition permits: an outer state is required to have acyclic augmented outer Q. Only states satisfying that outer-forest condition have this correspondence. Good states of T and lifts of contracted good states do satisfy it, which is exactly the domain needed by the table and Theorems 3 and 4. Restrict that sentence; do not silently drop the acyclicity requirement.

COMPUTED counterexample, with a directly checkable cycle. At V=8, root (0,1,4), x=6, take bounded black faces (0,3,2), (1,6,5), (1,2,7), (3,6,7), (3,4,5) and state (2,6,7,3,5). Its augmented outer graph contains the cycle 0-3-4-1-0. The full rotation is in code/outer_scope_counterexample.json. Thus the unrestricted state correspondence is false, while the forest-restricted correspondence used in the counting proof survives.

## Numerical verification and counterexample scope

COMPUTED. code/induction.py enumerates states from incidence constraints, tests good states with a disjoint-set forest and separate roots, constructs contractions by face substitution, and finds the three-face rotation by testing the two cyclic permutations at each possible third face. It imports no author implementation. It compares actual exception image sets, not merely their cardinalities. Through V=18, the exception counts by V=13,14,15,16,17,18 are 8,20,80,358,1320,6154. All tests of the rotation bijection, counting inequality, global half-exception bound and corner avoidance pass. This is a full independent replay of all 7,940 exceptions and 1,202,792 rooted contractions through V=18.

Corner avoidance means: if good states exist, then for every bounded black face and each specified corner, some good state avoids that corner. Equivalently each face assumes at least two values over the good states. It does not mean that every feasible local contraction type occurs. The half bound means 2|E_M|<=#good(T/M) separately for each contraction; it is not a bound within each cover. Both remain CONJECTURE beyond their computational ranges.

The requested negative claims are logically distinct. At V=11 a singleton interior already proves inclusion-minimality of the bad four-cycle disk, but its only interior degree-four vertex has neither usable merge. At V=13 the bad pentagon interior has no usable degree-four vertex, but the source need not be blocked. At V=14 the stronger blocked-source rule fails. A local obstruction inside one such disk does not refute G because good vertices can lie outside. COMPUTED. code/minimal_regions.json independently scans all roots and all obstruction regions through V=16, in the V>6 domain of G. It confirms first failures at V=11,13,14, respectively. Its minimality order is strict inclusion of interior vertex sets, matching the source.

PROVED-HERE, fixed-cover obstruction mechanism CORRECT. D reversals preserve u and therefore the cover. A good state has a unique partner, by orienting its three rooted Q-trees. Recomputing the partner at a good state cannot change the cover. Consequently an exceptional good state in a cover with no nonexceptional good orientation admits no repair by any sequence of D reversals that stays good, or by any simultaneous subset reversal. The V=18 example asserts one 13-cycle, so only two orientations need be checked. This is stronger than the V=17 failure of one reversal; the latter has a two-reversal good repair. Neither statement rules out changing covers through nongood intermediate states.

COMPUTED, decisive witness replay. code/induction_witnesses.json gives 22 states, 10 pairs and eight good states for the V=18 contraction, with classes six directly lifting and two exceptional. Its 13-cycle cover has exactly the bad/E orientations. The V=17 contraction has 18 states, eight pairs and six good states, three lifting and three exceptional. Its two covers separately have L,E,bad,L and E,E,L,bad classes. The saved V=13 and V=14 pentagon disks have interiors {5,6,12} and {6,7,13}, respectively, one white boundary incidence, and no usable interior degree-four vertex. Both are inclusion-minimal among all bad-pentagon interiors in their rooted graphs. The V=11 disk has singleton interior {6} and neither merge there is usable.

COMPUTED, exhaustive exceptional-cover replay. code/cover_obstructions.py uses the saved exception rows as an input index, then independently reconstructs each contraction and enumerates all cover orientations. Its output agrees with the independent complete exception census. No cover has only exceptional good orientations below V=18; there are 220 such rooted contraction-cover records at V=18. The per-cover half bound fails in two records at V=17 and 220 at V=18, while the global half bound never fails through V=18. These are counts of rooted records, not counts up to graph isomorphism. The least-order fixed-cover obstruction is therefore independently confirmed as V=18.

COMPUTED. The region deficiency identity was independently checked for every connected induced complement containing a facial root, with both eligible color choices, through V=14; see code/deficiency_6_14.json. Root choices with the same complement and color give the same identity and are not repeatedly counted. G2/G3 were checked on every contracted nonroot subset, both merges, every degree-four nonroot and root through V=14; see code/contraction_formula.json. The exact short-cycle criterion was checked at every merge of every separator-free rooted input through V=16 by direct pair enumeration; see code/structure_6_16.json.

## Dependency graph and remaining obligations

    I0: cancellation-free induction for all pair-admitting T
      <- AND: base, white-face factorization, G, smaller-instance induction, X.
    G: usable contraction somewhere
      <- missing global selection among crossing four/pentagon obstructions.
    restricted G
      <- AND: some simple merge, no chordless pentagon, exact obstruction classification.
    X: at least one nonexception on the two sides
      <- missing global escape or count bound.
    sufficient escape bound
      <- AND: rotation bijection, disjoint successful images, positive remainder.

No alternative proof through signed existence is silently inserted into I0. The accepted signed theorem would give existence directly, but would not supply the requested cancellation-free proof.

| ID | Exact obligation | Needed by | Route | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| I0 | general contraction induction closes | root | induction | root | I1-I5 | open |
| I1 | octahedron base | I0 | AND | algebraic/logical step | two explicit disjoint assignments | discharged |
| I2 | white-face gluing preserves good states | I0 | AND | proved earlier | saturation and forest product | discharged |
| I3 | some simple pair-preserving contraction | I0 | AND | missing | G, only restricted proof supplied | open |
| I4 | a nonexception exists on at least one usable side | I0 | AND | missing | X, finite tests and partial bounds | open |
| I5 | smaller pair-admitting instances have good states | I0 | AND | hypothesis | strong induction with V reduced by two | discharged conditionally |
| F0 | deficiency region formula | major claim | Euler elimination | major claim | F1,F2 | discharged |
| F1 | induced complement connected | F0 | AND | hypothesis | explicit in G1 | discharged |
| F2 | Euler, side counts, root accounting | F0 | AND | algebraic/logical step | expanded above | discharged |
| G0 | bad merge iff specified chordless 4/5 witness | major claim | contraction | major claim | G1,G2 | discharged |
| G1 | new nonsimplicity is a third common neighbor | G0 | AND | definition | no opposite edge | discharged |
| G2 | simple pair loss iff black-inner separator | G0 | AND | proved earlier | imported pair criterion with simple domain | discharged |
| X0 | rotation bijects E_M,E_N | major claim | forest edge replacement | major claim | X1,X2 | discharged |
| X1 | failure forces g to take a | X0 | AND | algebraic/logical step | aq would join split components otherwise | discharged |
| X2 | rotated forest has the required two components and inverse | X0 | AND | algebraic/logical step | F-qc+ac, reverse at same g | discharged |
| X3 | four successful image sets disjoint | count bound | AND | side condition | local type and nongood projection | discharged |
| X4 | existence upstairs implies nonexception downstairs | claimed equivalence | AND | too strong | no reverse implication supplied | failing |

## Verdict

| Claim and scope | Verdict | Status and independent evidence |
| --- | --- | --- |
| Connected-complement deficiency identity | CORRECT | PROVED-HERE derivation above; COMPUTED 699,666 checks through V=14 |
| Contraction deficiency identities G2/G3 | CORRECT | PROVED-HERE local contribution calculation; COMPUTED 6,202,336 checks through V=14 |
| Exact four-/five-cycle obstruction criterion | CORRECT | PROVED-HERE with imported pair criterion; COMPUTED 48,388 merge checks through V=16 |
| G without chordless pentagons, V>6 | CORRECT | PROVED-HERE crossing-path proof above |
| Inward-selection failures first at V=11,13,14 | CORRECT | REFUTED strategies; COMPUTED exhaustive region test through V=16 |
| Fixed-cover repair first fails at V=18 | CORRECT | REFUTED strategy; COMPUTED all exception records and cover orientations through V=18 |
| Corner avoidance and global half bound through V=18 | CORRECT | COMPUTED complete contraction census; CONJECTURE in general |
| Rotation bijection and two-sided counting inequality | CORRECT | PROVED-HERE forest proof; COMPUTED all 7,940 exceptions through V=18 |
| All states have the asserted outer-state correspondence | CORRECT AFTER FIX | REFUTED unrestricted wording at V=8; retain the outer-forest domain |
| Claimed equivalence between upstairs existence and a downstairs nonexception | GAP | The necessary reverse implication is absent; retain only sufficiency |
| General cancellation-free contraction induction | GAP | CONJECTURE G and X remain the two missing obligations |

Deficiency, exact obstruction classification, restricted G, rotation bijection and counting bound: CORRECT. The asserted equivalence in MISSING-LEMMA.md: GAP, with Astra's sufficient-condition correction CORRECT AFTER FIX. General G and X: GAP as a cancellation-free proof, not refuted. Finite corner avoidance and the half bound must remain COMPUTED, not general lemmas. The fixed-cover repair strategy is REFUTED once its two orientations are checked; it does not refute X.
