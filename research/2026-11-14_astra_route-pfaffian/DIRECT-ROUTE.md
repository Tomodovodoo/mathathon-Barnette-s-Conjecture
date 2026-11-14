# Direct route tests

Status convention: PROVED-HERE is T2 unreviewed, COMPUTED is T4 unreviewed, LIT identifies inspected source statements. This is a bounded investigation of three specified formalisms, not a nonexistence theorem for direct proofs.

## A. Perfect matchings of G

Definition. A state is a perfect matching s:A->B of the original bipartite graph. A pair r,s disagrees at every a. D has directed edges r(a)->s(a) on B, a permutation cycle cover. Q_s=G-s is a spanning 2-factor. Give s its Pfaffian determinant sign tau(s), and the pair the product tau(r)tau(s). All these signs are +1 after normalization. This is the literal direct-matching candidate; it is different from the face-incidence matching B in the planar proof.

PROVED-HERE. There is no distinguished side of a D cycle and no disk identity in these data. A Pfaffian orientation only controls conformal cycles of G. It does not turn their images in a permutation cover into boundaries of regions. Q_s is always cyclic, so the literal forest conclusion cannot hold. Replacing that target by connected Q_s gives exactly Hamiltonicity but leaves the difficult connectedness assertion untouched. `PROOFS.md` proves that the Pfaffian sign cannot cancel disconnected matching complements.

COMPUTED. Heawood has 24 matchings and all their complements are Hamiltonian. It is a poor negative test for connectedness. The cube trisum has 36 matchings: 12 connected complements, 18 with two cycles, six with three. All 36 determinant terms have the same sign. The nested trisum has 144 matchings but only 24 connected complements. The stored disconnected witnesses disprove any claim that Pfaffian sign alignment alone distinguishes the desired states. Nonzero determinant holds; cancellation and forest recovery do not. The earliest failure is the missing face/disk structure, and the first testable algebraic failure is cancellation with the proposed sign.

## B. Piece faces minus the glued square

Definition attempted. Use black vertices as the domain, retained piece-face labels as the codomain, bijective incident assignments as states, disjoint assignments as pairs, r(b)->s(b) as D, and the unselected two labels as Q_s, with the cyclic local sign from each piece.

REFUTED, PROVED-HERE. The cube trisum has fifteen retained labels and eight black vertices; a shared black vertex sees six of these labels. Twelve of the fifteen retained facial boundaries have lost an edge. Neither bijectivity nor the unique opposite edge is available. Details are in `PROOFS.md`, section 4. No sign, signed sum, or disk count is well-defined for this literal candidate, so reporting zero sums or failed recovery would be misleading. The same obstruction applies at the first cube trisum in the nested example. Heawood is an exceptional brace with no four-cycle and has no decomposition of this prescribed type.

HUNCH, T6. Keep separate states on capped planar pieces and boundary signatures. This avoids inventing global faces, but the hard theorem becomes closure of boundary data under trisums. It is a decomposition proof, not yet a single global states proof. Test the closure at every remaining four-cycle after one gluing, not just at its construction seam.

## C. Cellular surface faces

Definition. Use a rotation system, its faces, and the same incidence definitions as in the primal proof. On a positive-genus surface rooted states fail by cardinality. For the root-free torus variant retain all black vertices and all faces. D joins r(b) to s(b); Q_s joins the two face labels other than s(b). Local delta is +1 along the cyclic ordering of the three incident face labels and -1 in reverse. Put epsilon(r,s)=product_b delta(r(b),s(b)) and F=sum epsilon(r,s) product_b w[b,s(b)]. This avoids the invalid division by three in the original J formula.

COMPUTED. `data/results.json` stores an orientable Heawood embedding with seven distinct hexagonal faces and the rotation at every vertex. It has 24 root-free states and 48 ordered disjoint pairs. Contrary to the prediction, there is no even D cycle. Every D is one seven-cycle. Its delta-sum is +1 for 21 pairs, -1 for 21, +7 for three and -7 for three. Thus oddness survives in this instance, but the exact disk identity does not.

COMPUTED. All 24 Q_s have odd cycles. Each state has two partners and its coefficient in F is zero. `data/torus_signs.json` lists every state, Q-cycle and coefficient. Consequently F is identically zero, not just zero at the all-one specialization. Here step i in its oddness-only form holds for all occurring cycles; step ii cancels every cyclic state; step iii fails; step iv has no forest witness and cannot use the planar forest criterion. `PROOFS.md` proves the general edge-count reason. The prediction of even D cycles is retained in `PREDICTIONS.md` as a failed prediction.

PROVED-HERE. The rooted surface candidate also fails on every cellular embedding of a nonplanar trisum in an orientable surface: its genus is positive and the cardinality deficit is 2g. A root-free torus candidate cannot produce a forest, independently of the example. We did not enumerate torus embeddings of the trisums. This is an analytic obstruction, not a claimed computational run.

HUNCH, T6. Replace the forest target by a surface spine and track homology. One needs a new nonvanishing sum that preserves the required cyclic terms instead of cancelling all of them. The formalisation's cut language does not already supply this: primal face circuits correspond to bonds on the sphere, but essential surface circuits need not separate. Merely replacing the word inside by a cut shore does not prove every circuit is a bond.

## D. Drawings and crossing parity

Definition attempted. Start with the matching states in A and attach a crossing-parity factor to each matching in a chosen drawing. Even if the drawing has even crossing parity for every perfect matching, this factor is constant and gives the same obstruction as A. It supplies neither three incident face labels at each black vertex nor disk sides for D. No theorem equating this particular drawing condition with Pfaffianity is invoked here; the implication just stated is conditional on having such a drawing. We did not construct or enumerate crossing drawings. A drawing with crossings also introduces vertices outside G if it is planarized, so applying the planar states proof to it requires an unproved gadget correspondence.

## Boundary patterns and a direct trisum argument

LIT, inspected local source with unreviewed portions. The categorical report concerns a four-cycle in the dual triangulation, equivalently a four-edge cut in G. Its Theorem 3 has six allowed states in the chordless cases but only five when a specified diagonal is present. Its proof already uses OpenAI Corollary 7.2 for P4 prescriptions, and one chorded case has only a finite gadget check. It is not an independent assumption from which to derive Corollary 7.2 without checking circularity.

PROVED-HERE. A trisum identifies a four-vertex cycle of primal graphs and deletes the cycle edges. These are different interfaces. In particular each piece interior attaches by four edges, but the three pieces share terminal vertices with degree constraints. The categorical labeling partitions cannot be pasted three at a time as if three planar disks shared the same dual boundary. `PROOFS.md` states the correct six path signatures, proves their availability from P4-Hamiltonicity and the Pfaffian no-cross theorem, and proves a one-step Hamiltonian gluing lemma. This is a direct elementary assembly once the boundary data are known. It is not a states proof of their existence.

COMPUTED. All six path signatures occur on the canonical first square of cube, hexagonal prism, cube trisum, cube/cube/prism trisum and nested trisum. There are twelve compatible ordered triples of signatures. K3,3 is a useful control: it has the four single-path signatures and the crossing pairing, but neither of the two required noncrossing double-path signatures. This exposes the role of Pfaffianity in the boundary argument, despite K3,3 itself being P4-Hamiltonian.

## Saturation record and remaining door

The investigation changed tool family from literature to GF2 signing and exhaustive states, changed parameter from Hamiltonian counts to fixed-state polynomial coefficients, and tested an extreme base case, Heawood. It relaxed roots to restore torus cardinality, inverted nonvanishing into a coefficient-vanishing test, imported the Pfaffian no-cross obstruction, and checked the primal and referee reports for reusable lemmas. The resulting edge-count obstruction makes further root-free forest searches unnecessary. Broad campaigns and independent referees are outside this sub-agent's no-delegation scope. No claim of global research saturation is made.

CONJECTURE, T5. A useful direct theory must retain homology or boundary connectivity in its state weights. Test whether a modified Heawood polynomial has a nonzero coefficient selecting connected complements while preserving a tractable cancellation rule. This remains open; no successful sign construction is claimed.
COMPUTED/T4, additional replay. `code/verify.py` checks 524 rotated four-cut sides through eleven dual vertices with the categorical implementation. Counts are 108 chordless ++-- six-pattern cases, 24 chorded ++-- five-pattern cases, and 392 alternating six-pattern cases. Separate DFS independently of matching enumeration, but by the same author, reproduces every Hamiltonian count and P4 coverage in the seven named inputs. These remain unreviewed evidence.
