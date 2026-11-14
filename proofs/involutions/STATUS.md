# Status and provenance

Theorem numbers refer to involutions.tex. PROVED-HERE means a complete written argument is present, with a self-audit; it does not mean independent human review.

| Claim | Status | Origin and exact source | What is supplied here |
| --- | --- | --- | --- |
| Theorem 1, good pair (earlier name: forest pair) from pair existence | LIT; PROVED-HERE | OpenAI Proposition 5.1; Li Lemma 7 after pair existence | Pure finite signed-set proof |
| Lemma 2, disk identity | LIT; PROVED-HERE | OpenAI Lemma 4.1; Li Claim 25 in incidence language | Three disk counts, root exclusion, parity, white-face existence |
| Definition 3, signed marked set | LIT definition; PROVED-HERE convention | Li Definitions 13, 14, 18, 21 and Appendix B | Unordered, distinct crossings; repeated white points allowed; exact orientation dictionary |
| Lemma 4, first involution | LIT; PROVED-HERE | OpenAI Lemma 5.2; Li Definitions 22 and Lemmas 17, 34 | Invariant cycle choice, bijectivity, sign change, fixed set |
| Lemma 5, second involution | LIT construction; PROVED-HERE | Li Definitions 20, 23, Lemma 35 and Appendix B | All general-m well-definedness, invariant selection and return-move checks |
| Lemma 6, fixed points | LIT sketch; PROVED-HERE | Li Lemma 24 and Appendix B | Nonemptiness, independent cycle orientations, exact area-product count, common sign |
| Lemma 8, alternating path | LIT method; PROVED-HERE | Garsia-Milne method as explained in barnette_trees Section 5.1 and Theorem 5.3 | Direct finite graph proof for these geometric set tokens, without restarts |
| Lowest coefficient comparison | PROVED-HERE; COMPUTED | OpenAI Section 5.3; refereed project REWRITTEN-PROP-5-1.md | Signed-moment comparison and normalization; no role in existence proof |
| All-root verification | COMPUTED | Independent verify.py; plantri input cross-check in extras.py | 55 classes, 1206 roots, at most 14 vertices of T; 880 paired roots; 221050 marked objects; 4658 fixed starts |
| Integer polynomial comparison | COMPUTED | more_checks.py against existing lab core.py | All 880 paired roots; vanishing lower coefficients and equal absolute lowest coefficient |
| Family paths | COMPUTED | extras.py, families.json | Tubes p=4,6, L=0,1,2; stacks p=4,6, q=2,3; subdivided octahedron; specified root only; up to 20 vertices of T |
| Current running example | COMPUTED | running.json copied from current project input | 279 objects and every image listed; minimum count 2; nine second-fixed objects |

Accepted background: Euler's formula for a disk and sphere; Jordan curve crossing parity and entry/exit alternation; existence of a straight-line drawing of a simple plane graph. None assumes the good-pair conclusion. The note proves the cycle/sign identities it uses. The existence of an initial pair is an explicit hypothesis, not an audited consequence of Ore's criterion.

The original census drawings have maximum path length two. The referee census reaches four, the 69 running-example drawings reach six, and the two drawing-free tree censuses each reach four. These are finite measurements, not universal bounds. The constructor searches for a minimum cover; the constructive paper avoids that search with a different token model and restarts. The note does not prove or claim that the two walks are conjugate.

The original example.json is absent. The current running.json is copied here. The 213-object Li replay interchanges the anchor points of roots 4 and 5. Both counts are correct; the signed sum is -9 in both drawings.

## Revision, 14 November 2026

PROVED-HERE. Section 5, Lemma 7 gives drawing-free tokens as white-face/path-step incidences, their direction bit, all second-map checks, and the same area-product fixed count. This is the face-path height of paper/main Section 4 with opposite normalization, unpacked term by term. The main route remains Li's intended proof written out in full.

COMPUTED. research/2026-11-14_sol_involutions-revision/code/check.py checks all 1206 roots in ray mode and with two face-path trees. Object totals are 221050, 17832 and 18362; all three modes give 4658 second-fixed objects. Every displayed sign has explicit computational checks, including the corrected (n+m)/2 coefficient and Li's orientation convention. The referee's independent code is rerun separately, including its 57 higher-mark zeros. The author's ray geometry has 78 such zeros. See verification.json, referee-rerun.json, drawing-census.json and AUDIT.md in that research folder.

The coefficient error is REFUTED by the octahedron and corrected. The count is 55 classes. Rays, object lists, first-fixed sets and path lengths depend on the drawing; path-mode analogues depend on the dual tree. F and the signed sum do not. Actual second-fixed marked objects can change even though their cardinality is invariant.

## Second referee, 14 November 2026

Independent review of Section 5 and final check of the note, in research/2026-11-14_fable_referee-involutions-v2/ (REFEREE.md, CHANGELOG.md, code/).

PROVED-HERE, checked by a second reader. Lemma 7 is correct after a fix to its wording. Its statement was "the lists have the same rules as the ray lists" and is now three exact claims (parity, alternation, first exit) and one consequence. Its proof called the three sectors of a black triangle corner sectors and said the route r(t), t, s(t) separates two of them from each other; each sector lies on a side, and the route separates the sector on the side r(t)s(t) from the other two. The proof now also says why the incidence cycle and the side cycle enclose the same white faces. No mathematical step failed.

COMPUTED by code written from the text alone (census.py, canonical.py, running.py). In the note's encoding it reproduces 55 classes, 1206 roots, 880 paired roots, 221050 ray objects, 17832 and 18362 path objects, 4658 second-fixed objects in every mode, ray walks of zero or two moves, tree walks up to four, 78 zeros with m+1 marks, the three witnesses of Section 7, and all 279 rows of the printed table. With plantri input it checks five families of face paths on all 1206 roots: two breadth-first trees, a depth-first tree, a random spanning tree, and independent random simple paths that form no tree. Rays in two directions are checked through 12 vertices. m is 1, 2, 3 on 560, 162, 158 roots.

The face-path proof does not need a tree. Any fixed simple path from each white face to the outer face works, and the note now says so.

Corrected in this pass. Figure 2 showed the reversal of an unmarked cycle under a caption that described a token move; it now shows a token move (object 2 to object 6). Figures 1 and 4 have their labels moved off the spokes and the marked crossings dotted. The note's layout of the running example is the mirror image of the main paper's drawing, so each kappa in Figure 3 is the negative of the sign in the main paper's height figure; Section 9 and the caption now say so. H = -omega holds for the same paths and the same orientation. The PDF has 18 pages.
