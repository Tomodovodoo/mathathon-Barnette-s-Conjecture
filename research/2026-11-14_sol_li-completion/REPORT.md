# Completion of Li's multi-mark argument

PROVED-HERE: a complete two-involution proof of pair existence implying a forest pair is written in proofs/involutions/.
PROVED-HERE: both general-m involutions, their fixed sets, common sign and nonemptiness are verified in the note.
COMPUTED: all 1206 rooted instances through 14 triangulation vertices, 221050 marked objects, agree with the claims.
COMPUTED: all 880 paired roots agree in lowest coefficient with the existing integer-weight polynomial; family paths reach 20 vertices.
The constructor requires minimum-cover enumeration; the source's older 213-object example is not identified with our current 279-object example.

## Aim and sources read

The task was to complete the combinatorial route of Li's Key Lemma, supply an explicit construction, and audit and verify it. I read research/BRIEF.md, README.md, the requested unslop and reverse-Lamport skills, the dependency audit and dictionary, the refereed height proof, the primal dictionary, the route-combinatorics data, and the relevant implementation and family generators read-only.

I opened the actual Li PDF with PyMuPDF, extracted all 14 pages into the owned research directory, rendered every page, and inspected the four page contact sheets covering all pages. The main definitions and Appendix B were read from the actual PDF in addition to the extracted text. The other two PDFs were opened with PyMuPDF and their cancellation, disk, spoke-slide and marked-construction sections compared from the fresh extraction. I did not rely exclusively on papers/text/. The PDF skill was consulted for authoring and visual QA. No web sources or new literature citations were needed.

## What is established

PROVED-HERE. The standalone note assumes only a simple properly face-bicoloured sphere triangulation, a chosen outer black face, and existence of a pair. It gives the disk count, the incidence/forest dictionary and the sign convention before defining unordered sets of m distinct crossing tokens. Repeated white faces are allowed. Repeated identical crossings are not.

PROVED-HERE. The first involution fixes the second state and reverses a cycle selected from that state alone. The disk count gives its sign change. The second uses Li's exact geometric pairing, with an invariant priority rule on unoriented cycles. The proof covers the unmarked-cycle case, the all-marked one-token-per-cycle deduction, both partner-matching cases, token validity and collision exclusion, selection invariance, sign reversal and the fixed predicate. It proves nonemptiness by orienting minimum cycles independently and counts fixed points by a product of enclosed white-face counts.

PROVED-HERE. Alternation from any second-fixed object ends at a first-fixed object. The proof uses the finite two-labelled path and common fixed sign. It needs no polynomial, limit or complex number. Finding the initial minimum cover can be done by finite exhaustive enumeration; no efficient initialization is claimed. The comparison with heights and the polynomial is confined to a separate section and is not used to prove existence or termination.

PROVED-HERE reconstruction. Li's main text restricts to c_min=1 immediately after Definition 14. Definitions 22-23 give the maps; Lemmas 34-35 establish their one-mark sign changes; Claim 25 gives the disk count and Claim 26 the local turn formula used in Lemma 17. Appendix B gives the general sign and priorities, states the fixed set and common sign, but omits complete return-move and nonemptiness arguments. The note supplies those checks without attributing a false theorem to Li. The balance missing at the Ore invocation is supplied separately by Euler; the involution theorem itself assumes a pair.

COMPUTED concrete witnesses. witnesses.json contains complete face lists, pairs, tokens, signs and images at m=2 on 9-vertex class 0 root 0, and m=3 on 12-vertex class 0 root 0. Both show why an unmarked cycle must be handled even with m marks. polynomial-comparison.json supplies the interior nonfirst branch at m=2 on 11-vertex class 1 root 0. nonseparating-witness.json gives m=3 without any separating triangle at 14-vertex class 27 root 0, with 826 objects and eight second-fixed objects. Class numbering is explicitly tied to the canonical generator.

## Independent computation

Commands, run from the repository root:

```powershell
python research/2026-11-14_sol_li-completion/verify.py 14
python research/2026-11-14_sol_li-completion/extras.py
python research/2026-11-14_sol_li-completion/more_checks.py
python research/2026-11-14_sol_li-completion/build.py
```

COMPUTED. verify.py independently implements states, pairs, cycle decomposition, exact rational Tutte layouts, generic shears, ray crossings, signs, both maps, fixed counts and alternating paths. It imports only the established triangulation input generator. It does not import the existing Li maps. The census took about 20 seconds. extras.py compares the entire canonical class sets against the installed plantri -ba output, and supplies families and the comparison walk. more_checks.py uses the existing lab only as an external polynomial comparator. Every run was well below ten minutes and heavy runs were sequential.

| Quantity | Verified value |
| --- | --- |
| Triangulation vertex range | through 14, including separating triangles |
| Unrooted classes | 56 |
| Rooted instances | 1206 |
| Paired rooted instances | 880 |
| Paired roots with m=1,2,3 | 560,162,158 |
| Marked objects | 221050 |
| Second-fixed objects | 4658 |
| Maximum alternating length from all second-fixed objects | 2 nonfixed moves |
| Polynomial comparator roots | all 880 with pairs |

COMPUTED. The family output covers p=4,6 tubes with L=0,1,2; p=4,6 stacks with q=2,3; and the subdivided octahedron, using one stated root per input. It reaches 20 vertices of T. All second-fixed starts are measured. Ray lengths are zero or two. On the subdivided octahedron all 14 ray starts take two moves. The existing barnette_trees implementation, compared from every pair rather than the same geometric starts, has maximum three moves and eight total restarts. The different starts prevent any speed comparison.

## Example and figures

COMPUTED. paper/figures/example.json is absent in this checkout. The current running.json has 13 triangulation vertices, minimum cycle count two, 12 states and eight pairs. With our recorded rational layout it has 279 objects, nine second-fixed objects and lowest coefficient nine. Every object and both images appear in the PDF and copied JSON. Counts of crossing objects vary with the embedding. I did not retrofit the earlier 213-object table to a different layout.

The three figures import the project's model and Panel toolkit read-only and use its encodings. They show a marked pair, the second map on that pair, and a nontrivial first map on a 12-vertex witness. The exact crossings are specified by the stored layout; figure labels identify the token white faces and spokes. The first map is already fixed at every second-fixed start on the running example, so a separate witness is used to illustrate a nontrivial first move.

## Audit and PDF QA

PROVED-HERE self-audit. AUDIT.md freezes the theorem contract and gives a bounded conclusion-first AND graph with classifications, a dependency table and verdict FOLLOWS. It checks the construction as a separate conclusion and excludes computations as proof premises. The key checks are O5-O10 and O13-O16. This is a self-audit, not independent peer review.

The note is amsart, A4, one-inch margins. It compiles twice with pdflatex. An initial longtable pagination issue was corrected by using explicit table pages. The final log has no undefined reference, TeX error, ignored error or overfull box. The only package-name warning is the read-only relative path to the project's style package. The MiKTeX update notice is external to the document build. All final rendered pages were visually inspected. Build commands and render command are in proofs/involutions/README.md.

## What failed or remains open

The source request's 213-object running example could not be identified with the current input and exact layout; the note explicitly supplies and labels a reproducible 279-object replacement. The manuscript's optimized layout is not used to infer any crossing in the verifier. The figures use an affine view of the verified Tutte layout and are less spread out than the optimized manuscript figures.

No universal short-path bound was obtained. The maximum two is a census measurement only. The geometric constructor needs a minimum-cover search. The arbitrary-start, restart-based construction in barnette_trees avoids that search, but a direct geometric restart formulation has not been proved here. No conjugacy of the two token models is asserted.

## Three best next steps

1. Independently referee the written general-m proof, especially mark selection invariance and the set/list normalization.
2. Give a geometric arbitrary-start constructor with cycle-count-decreasing restarts, or prove a precise translation to the existing ordered weight-token construction.
3. Extend the census and family path measurements past 14 vertices and test whether longer paths occur; retain the complete certificates and exact root/layout choices.

## Leads for others

The set-token model makes the lowest coefficient's area-product formula visible without polynomial operations. A reader-facing exposition could use this as the main route and keep the algebraic proof as a compact alternate. Any global constructive-efficiency claim should distinguish minimum-cover initialization from the path itself.
