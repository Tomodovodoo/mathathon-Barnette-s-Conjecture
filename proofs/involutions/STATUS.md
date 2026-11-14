# Status and provenance

Theorem numbers refer to involutions.tex. PROVED-HERE means a complete written argument is present, with a self-audit; it does not mean independent human review.

| Claim | Status | Origin and exact source | What is supplied here |
| --- | --- | --- | --- |
| Theorem 1, forest pair from pair existence | LIT; PROVED-HERE | OpenAI Proposition 5.1; Li Lemma 7 after pair existence | Pure finite signed-set proof |
| Lemma 2, disk identity | LIT; PROVED-HERE | OpenAI Lemma 4.1; Li Claim 25 in incidence language | Three disk counts, root exclusion, parity, white-face existence |
| Definition 3, signed marked set | LIT definition; PROVED-HERE convention | Li Definitions 13, 14, 18, 21 and Appendix B | Unordered, distinct crossings; repeated white points allowed; exact orientation dictionary |
| Lemma 4, first involution | LIT; PROVED-HERE | OpenAI Lemma 5.2; Li Definitions 22 and Lemmas 17, 34 | Invariant cycle choice, bijectivity, sign change, fixed set |
| Lemma 5, second involution | LIT construction; PROVED-HERE | Li Definitions 20, 23, Lemma 35 and Appendix B | All general-m well-definedness, invariant selection and return-move checks |
| Lemma 6, fixed points | LIT sketch; PROVED-HERE | Li Lemma 24 and Appendix B | Nonemptiness, independent cycle orientations, exact area-product count, common sign |
| Lemma 7, alternating path | LIT method; PROVED-HERE | Garsia-Milne method as explained in barnette_trees Section 5.1 and Theorem 5.3 | Direct finite graph proof for these geometric set tokens, without restarts |
| Lowest coefficient comparison | PROVED-HERE; COMPUTED | OpenAI Section 5.3; refereed project REWRITTEN-PROP-5-1.md | Signed-moment comparison and normalization; no role in existence proof |
| All-root verification | COMPUTED | Independent verify.py; plantri input cross-check in extras.py | 55 classes, 1206 roots, at most 14 vertices of T; 880 paired roots; 221050 marked objects; 4658 fixed starts |
| Integer polynomial comparison | COMPUTED | more_checks.py against existing lab core.py | All 880 paired roots; vanishing lower coefficients and equal absolute lowest coefficient |
| Family paths | COMPUTED | extras.py, families.json | Tubes p=4,6, L=0,1,2; stacks p=4,6, q=2,3; subdivided octahedron; specified root only; up to 20 vertices of T |
| Current running example | COMPUTED | running.json copied from current project input | 279 objects and every image listed; minimum count 2; nine second-fixed objects |

Accepted background: Euler's formula for a disk and sphere; Jordan curve crossing parity and entry/exit alternation; existence of a straight-line drawing of a simple plane graph. None assumes the forest-pair conclusion. The note proves the cycle/sign identities it uses. The existence of an initial pair is an explicit hypothesis, not an audited consequence of Ore's criterion.

The maximum verified alternating path is two nonfixed moves. This is a finite census result, not a universal complexity bound. The constructor searches for a minimum cover; the constructive paper avoids that search with a different token model and restarts. The note does not prove or claim that the two walks are conjugate.

The original example.json is absent. The current running.json is copied here. The 213-object Li replay interchanges the anchor points of roots 4 and 5. Both counts are correct; the signed sum is -9 in both drawings.
