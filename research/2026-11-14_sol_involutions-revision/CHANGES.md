# Revision change log

All mathematical assertions below use the status tags of research/BRIEF.md. The implementation is confined to proofs/involutions/ and this research folder.

| Referee edit | Checked how | Applied change |
| --- | --- | --- |
| E1 | COMPUTED, code/check.py on 880 paired roots in three modes; octahedron n=3,m=1,F=1 gives +1. Also reran the independent referee checker. | Corrected exponent to (n+m)/2; supplied the floor/ceiling identity and opposite height normalization. |
| E2 | COMPUTED, canonical census plus independent plantri input. Class counts 1,0,1,1,2,2,8,8,32 sum to 55. | Corrected all three companions. |
| E3 | Read paper/main/barnette.tex Section 4, including the turn definition and height and finite-difference proofs; read draft-B referee report. | Replaced the indexed-list description; explained the term-by-term dictionary and the roles of both involutions. |
| E4 | Read Li's text and the rendered source PDF, especially page 12 Appendix B. Checked Section 4.3 and Definitions 14, 20, 23. | Distinguished Li's stated convention, rule and priorities from unwritten verifications; credited the earlier dependency audit. |
| E5 | Same source check and all-object branch verification. | Said that the unmarked-cycle case uses Li's existing rule and the local reversal he specifies. |
| E6 | COMPUTED, code/drawings.py repeats the referee's 69 drawings and all checks; full referee census separately rerun. | Qualified two moves by the original drawings; recorded four and six in other drawings. |
| E7 | COMPUTED, drawing-census.json reproduces root-order swap, 279 and 213, 35 values from 103 to 363, invariant signed sum -9 and F=9. | Replaced the earlier-layout explanation with the mirror-image root-anchor explanation; specified root order 0,5,4. |
| E8 | PROVED-HERE, fixed-set bijection and new path lemma. COMPUTED in both censuses. | Declared drawing dependence at the definition; distinguished fixed objects from their invariant cardinality. |
| E9 | Checked that detours have disjoint triangle interiors; winding-number differences avoid all white faces. Referee rerun checks spoke and side interiors separately. | Replaced sliding prose by the winding-number proof. |
| E10 | Checked inside triangle/vertex correspondence and the state boundary assignment. | Replaced the tautological sentence with the full bijection count; made disk connectedness explicit. |
| E11 | Every token belongs to a different cycle from the reversed unmarked cycle. All objects checked. | Stated token eligibility after case 1. |
| E12 | PROVED-HERE, local incidence directions and path lemma; COMPUTED by direction alternation and first-exit checks. | Specified r-to-centre and centre-to-s traversal and what reversal does. |
| E13 | Each compared cycle family has disjoint supplying-face sets; no global face-set uniqueness is needed. | Restricted the lexicographic example to the families actually compared; Markdown agrees. |
| E14 | COMPUTED objects and images in figure-data.json, checked against published full listing. Rendered figures and inspected pages 8 and 9. | Added rays and overview/zoom to Figure 1, zoomed before/after with rays to Figure 2, and a face-path mark diagram as Figure 3. All explicit labels are at least footnote size. |
| E15 | Searched both Markdown companions for stale counts, attribution and layout claims. | Corrected counts, mirror-image explanation, drawing dependence, attribution and lemma numbering. |

## Additional requested work

PROVED-HERE. Section 5 gives marks as (white face, black-face path step) incidences. Eligibility is equality of the selected and turned corners. The bit is (1+kappa)/2. The local traversal sign is -kappa on s and +kappa on r. The proof cuts the abstract oriented sphere map along a formal incidence cycle, derives alternating inside/outside transitions, and explicitly checks both maps, independent orientation choices, common sign and the area-product count. No metric drawing enters the construction. A dual spanning tree supplies the paths; changing it changes the marked set.

COMPUTED. code/check.py enumerates every object in three modes on every rooted instance through 14 vertices. It checks membership, involution identities, signs, forest fixed points, F, every second-fixed alternating start, Li's orientation dictionary, phase normalization, lower moments and the corrected leading sign. The path version independently checks parity against rational polygon winding and checks successive directions and first-exit signs. The base enumeration and maps are copied, with attribution, from the original author's verifier; the new path-token data, BFS paths, signs and additional checks are revision code. This is an implementation verification, not a claim of a new independent referee.

COMPUTED. Two dual BFS trees give 17832 and 18362 objects, F-total 4658 each, maximum walk four each. Original rays give 221050 objects and maximum two. The referee's geometry is separately rerun. Its 57 zeros for m+1 are geometry-specific; original author rays have 78. The note now says this explicitly. All m-1 counts vanish, also proved by unmarked-cycle reversal.

The proof remains Li's intended proof written out in full. It unpacks one height term by term. The first map is the cancellation lemma on marked objects, the second proves the height and finite-difference lemmas together. This attribution is stated in the TeX, Markdown and status file.
