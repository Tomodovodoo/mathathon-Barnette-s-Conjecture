# 279 versus 213 marked objects on the running example

Both numbers are correct. They count the same kind of object (Li's Definition 14 with the note's set convention: a pair plus an unordered set of m = 2 distinct crossings of upward white rays with s-spokes) on the same input, `paper/figures/running.json` with outer face 4. They use two different drawings. Nothing else differs.

## What each count is

| Count | Produced by | Layout | Status |
| --- | --- | --- | --- |
| 279 | `research/2026-11-14_sol_li-completion/verify.py`, listed in `proofs/involutions/running-objects.json` | Tutte barycentric layout, roots in stored face order 0, 5, 4 sent to (0,0), (100,0), (0,100), then shear x ↦ x + y (first generic shear ≥ 1), vertical rays from barycentres of white faces | COMPUTED, reproduced object by object |
| 213 | `research/2026-11-14_astra_audit-digestions/code/verify.py` calling `workings/barnette_lab/barnette_lab/li.py` (`LiMultiObjects`) | the same recipe, but the roots taken in the lab's networkx face order 0, 4, 5, so 4 goes to (100,0) and 5 to (0,100), then the same shear 1 | COMPUTED, reproduced |

So the two drawings differ by swapping the images of roots 4 and 5. That is a reflection of the whole Tutte drawing (the barycentric solution is affine-equivariant) followed by the same shear. Relative to the triangulation, the rays point in a different direction, and they cross different spokes.

The note's own explanation is not right. Section 8 says the 213 belongs to "an earlier layout", and contrasts the note's geometry with "the manuscript's optimized disk layout". The 213 comes from neither. It comes from the lab's Tutte layout of the same file, with a different root order. The STATUS.md phrase "a different geometry or input" is vaguer and also misleading on "input": the input is the same.

## Evidence (COMPUTED, `code/running.py`, `code/compare_running.py`, outputs in `code/out/`)

1. My implementation (`code/ref.py`, written from the PDF only) with the note's recipe reproduces the coordinates of `proofs/involutions/running-geometry.json` exactly (`note_positions_reproduced: true`).
2. In that layout my object set equals the published 279-object set, and for every one of the 279 objects my sign, my ι1 image and my ι2 image agree with the table (`published_set_equals_mine: true`, `mismatches: []`).
3. With the lab's root order (0, 4, 5) and shear 1, the same code gives 213 objects, 141 first-fixed and 9 second-fixed objects, signed sum −9. Astra's audit reports 213, 141 and 9 for the lab replay (AUDIT.md line 51). The three numbers match.
4. The two object sets are disjoint. Every token differs. Per pair the token counts are (note layout / lab layout): 9/7, 15/7, 10/6, 6/8, 12/8, 3/9, 3/9, 4/8, with no token in common in any pair.
5. Varying the drawing further: the six assignments of the roots to the three anchor points (shear 0) give 221, 209, 279, 213, 317, 145 objects. Sixty random generic ray directions on the unsheared Tutte layout with the note's root order bring the total to 69 drawings and 35 distinct counts between 103 and 363. In every case the signed sum is −9, the second fixed set has 9 objects, every check of `check.py` passes (both involutions, sign reversal, fixed-set description, F formula, alternating paths, moment identity).
6. First-fixed counts also move: 273 in the note layout, 141 in the lab layout, between 89 and 303 in the other drawings.

## Why the count depends on the drawing, and why that is harmless

`|Ω| = Σ_p C(N_p, m)`, where `N_p` is the number of pairs (white face w, black face t) whose ray ρ_w crosses the spoke from t to s(t). A ray can be rotated past a vertex or a centre, and then a crossing appears or disappears. So `N_p`, `|Ω|` and the first fixed set all depend on the drawing. The proof never uses `|Ω|`.

What the proof uses is layout-free:

- the signed sum `Σ σ(o) = (−1)^{⌊m/2⌋} F`, with `F = Σ_D Π_{C∈D} a(C)` over unoriented covers with m cycles, `a(C)` the number of white faces inside C. Both `F` and `a(C)` are combinatorial: "inside" is the side of the cycle away from t0.
- the second fixed set as a set of choices: one minimum cover plus one enclosed white face per cycle. The object attached to a choice records the first spoke crossed by the ray, which depends on the drawing. The number of such objects, F, does not.

The mechanism: the ray pairing cancels crossings two at a time along each ray. What survives on a cycle C is one first exit for each white face inside C. A different drawing changes which crossings exist, but along each ray consecutive crossings of C still alternate entry and exit, so the survivors are again one per enclosed white face.

## What should change in the note

The dependence is real and should be stated as a property of the construction, not as a disclaimer about an earlier table. Proposed text is EDITS.md items E7 and E8: say which two root orders give 279 and 213, say that |Ω| and the first fixed set depend on the drawing while F and the signed sum do not, and give one line of reason.

A layout-free object count is not available in this model. Any token model built from crossings of a fixed curve system with spokes has this dependence. The project's height route (paper/main Section 4) replaces rays by fixed paths of faces. There a token would be a black face where the path turns around the selected corner. That count depends on the chosen paths in the same way (HUNCH, not computed). The invariant content is F.
