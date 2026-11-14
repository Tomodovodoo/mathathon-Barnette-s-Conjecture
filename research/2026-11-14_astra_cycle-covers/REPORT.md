# Research report

PROVED-HERE, unreviewed: c_min is minimum primal component count after admissible edge deletion, minus one.
PROVED-HERE, unreviewed: a separator-free family has unique covers with arbitrarily many cycles and attains TM=2^c_min.
COMPUTED: the complete 4-connected census through dual order 24 covers 23,824,742 facial roots, with no bound or strictness violation.
REFUTED by explicit order-18 witnesses: fixed-cycle-count levels, including the minimum level, need not be flip-connected.
PROVED-HERE, unreviewed: the two-cover case satisfies the exponential bound; the general bound and strictness remain open.

## Scope and deliverables

I investigated the primal meaning of D, the size of c_min without triangular separators, flip structure, the exponential counting conjecture, and the first signed coefficient. All changes are confined to research/2026-11-14_astra_cycle-covers/. I read the brief, named skills, supplied OpenAI paper text, primal dictionary, and the specified prior result and referee files. The PDF's extracted text was the reading source; no visual PDF audit is claimed. No reference implementation was edited and no subagents were used.

COVERS.md is the reader-facing account and figure. PROOFS.md contains the primal dictionary, explicit family, parity and local flip lemma, coefficient argument, and two-cover counting proof. CENSUS.md gives exact tables and limits. code/README.md and data/README.md give commands and provenance. The owner-local knowledge, frontier, state-of-the-art, board, event log, and data/visual.html are the handoff map and dashboard; they do not modify the coordinator's canonical files.

## What changed

PROVED-HERE, T2 unreviewed. An admissible S chooses one edge at each non-root black vertex and exactly two boundary edges of each non-root face, avoiding root faces. The dual cover satisfies c(D)=kappa(G-S)-1. Its cycles are laminar primal bonds, and the quotient by primal components is a tree of parallel bundles. Thus c_min has a direct connectivity meaning.

PROVED-HERE, T2 unreviewed. For every m>=2, the explicit T_m has 3m+2 vertices, no separating triangle, and exactly one cover, consisting of m-2 triangles and one pentagon. Therefore c_min=m-1 and TM=2^(m-1). This closes the separator-free unboundedness question. It also proves equality is attained for every exponent within that class. The normalized polynomial is (z-1)^(m-2)(z^2-1), whose leading coefficient is always two. The growing pole degrees mean this does not settle unboundedness among Goodey graphs without separators.

PROVED-HERE, T2 unreviewed. With exactly two covers, write c1,c2 for their component counts and j for their identical component cycles. Their common second states number either zero or 2^j. Hence TM=2^c1+2^c2-2a, and the exponential lower bound follows. Strictness is proved except for the possible configuration c1=c2=j+1 and a=2^j. No planar exclusion of that configuration is established here.

PROVED-HERE, T2 unreviewed. The first coefficient counts minimal laminar bond families with a white vertex chosen on every root-free shore. Its magnitude is the sum of products of descendant white masses in the region trees. This is a direct primal bijection for pointed covers. It is not a bijection to unweighted tree matchings. The two different regroupings of pairs explain why a minimal cover can certify existence while containing no forest pair.

LIT. The object already has a name: Eppstein-Mumford rooted cycle cover. Their arXiv:0912.0537v1, Section 3 and Lemma 29, identifies its corner-polyhedron meaning and supplies earlier existence for the 4-connected case. Relevant passages were opened at https://arxiv.org/pdf/0912.0537 . The attempted journal PDF and guessed author PDF failed to open; the arXiv copy succeeded. I do not claim an audit of their full geometric proof or novelty of this object.

## Computation and failures

COMPUTED, T4 under review. The exact census uses the prior C lattice enumerator copied into this folder with a record-witness hook, and the existing plantri 4.5 generator with -b -c4. Orders 6 through 24 and every facial root give 23,824,742 instances. No lattice overflow occurred. Maximum c_min reaches 6 at order 23. The longest run was 210.02 seconds; one heavy process ran at a time. This is not a new independent certification of the C algorithm.

COMPUTED. Independent corner-degree enumeration checks the family through m=10. Reference states and pairs check m=2,...,6, including tree counts and coefficients. The primal component identity is asserted on every cover in the separate level search, exhaustive through order 17. The two-cover formula agrees with all 52 two-cover rooted instances through order 14. These are separate implementations by the same author, not an independent referee.

REFUTED, COMPUTED. The first disconnected fixed-c level in the separator-free search occurs at order 18. Its flip square has c labels 3,1,5,3. A second independently reproduced square, already supplied by Opus, has labels 1,3,3,1, so its minimum level is disconnected. The move test even allows every simple directed-cycle reversal, stronger than just Hasse moves. Minima therefore need not be lattice-convex or connected; monotone rank arguments cannot simply track c.

The raw Python planar-code parser initially failed at order 10 because the Windows binary emits CRLF-expanded bytes. Normalization fixed it, and the entire retained level search was rerun. The C pipeline's text-mode reader reverses the same expansion. Its control-Z limit matters at order 26, so larger sizes require a binary-mode or text-format repair before use. Orders above 24 were not censused.

The family discovery made large random searches and ILP unnecessary for the unboundedness question. Those requested approaches were not implemented. I did not prove the full strict inequality or exponential bound, construct a general injection from minimal-cover orientations, or find a new spanning-forest bijection. This is a bounded research handoff with those questions open, not a claim of saturation across all methods.

## Three best next steps

1. Independently referee the T_m forcing proof, especially the facial list, m=2 boundary case, and pentagon's two white faces. If accepted, replace the open separator-free-unboundedness question with this construction and figure.
2. Exclude the exceptional two-cover overlap by planarity, then determine whether the shared-state calculation extends beyond two covers. A direct induction on fixed-c levels is already refuted.
3. Study the pointed-bond region tree for a nonnegative weighted-tree interpretation, and separately ask whether bounded primal face sizes still permit unbounded c_min without separators.

## Leads for others

The Eppstein-Mumford rooted-cover definition is an exact dictionary, not an analogy. It should be cited where covers first appear. The new family simultaneously separates vanishing order from leading coefficient size and shows that separator gluing is not the source of large c_min. Its two growing primal faces identify the next natural restriction.

## Review and git

All new proofs remain T2 unreviewed and all numerical campaigns T4 under review. Human review is pending. Only the assigned path was staged and committed. The final push outcome is reported in chat.
