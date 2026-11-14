# Referee code

Written from the text of `proofs/involutions/involutions.pdf`. It does not import the author's `verify.py`, `extras.py` or `more_checks.py`, nor the lab's `li.py`. Inputs come from `workings/barnette_lab/vendor/plantri.exe -b -a v` (rotation systems; faces are traced here). `running.py` imports the lab's `Instance` only to read the face order the lab uses, to reproduce the 213 count.

Run from the repository root with Python 3 (standard library; `running.py` also needs networkx for that one import; `extras.py` and `check.py` need nothing else). Exact rational arithmetic throughout.

| Command | Time | Output |
| --- | --- | --- |
| `python research/2026-11-14_opus_referee-involutions/code/check.py census 14` | 4.5 min | `out/census-14.json`, `out/census-14.log` |
| `python research/2026-11-14_opus_referee-involutions/code/check.py census 10` | 2 s | `out/census-10.json` |
| `python research/2026-11-14_opus_referee-involutions/code/running.py` | 12 s | `out/running.json` |
| `python research/2026-11-14_opus_referee-involutions/code/compare_running.py` | 3 s | `out/compare-running.json` |
| `python research/2026-11-14_opus_referee-involutions/code/extras.py 12` | 9 s | `out/extras-12.json` |

`out/figure1-proposed.png` was made by compiling a modified copy of `proofs/involutions/figures/marked.tex` (EDITS.md, E14) in the scratchpad and rendering it with PyMuPDF.

## Files

- `ref.py`: instance (faces, colouring, A, X), exact Tutte layout with roots sent to (0,0), (100,0), (0,100) in a chosen order, first generic shear at or above a chosen minimum, ray direction as a parameter; states, pairs, D_p cycles, Q_s cycles, δ, J (two ways), tokens, signs, and the two maps exactly as written in Sections 3 and 4 of the note, with the cycle order as a parameter.
- `check.py`: for one rooted instance, asserts: J by δ equals J by signed area; every D_p cycle odd with δ-sum ±3; spoke polygon and side polygon enclose the same white points, and ray parity equals inside; δ-sum ±3 on every directed Q_s cycle; Ω closed under both maps; both are involutions; both applications of ι2 take the same case; sign reversal off the fixed sets; Fix(ι1) = forest pairs; the fixed-set description and sign of Lemma 6; |Fix(ι2)| = F with 2^m pairs per minimum unoriented cover; the alternating walk from every ι2-fixed object ends at a forest pair without repetition; signed moments of H vanish below m and the m-th equals m!(−1)^⌈n/2⌉ Σσ = m!(−1)^{(n+m)/2} F; and records whether the printed sign (−1)^{(n−m)/2} F holds. Every instance is run twice, with the lexicographic cycle order and with a random one. Also records the signed counts with m − 1 and m + 1 marks.
- `running.py`: the running example in 69 drawings (note layout, lab layout, six root assignments, sixty random directions).
- `compare_running.py`: object-by-object comparison with `proofs/involutions/running-objects.json`, and the lab-layout object set.
- `extras.py`: increment of H under cycle reversal; list convention with repetitions; k = m + 1 marks.

## Results (COMPUTED)

Census through 14 vertices: 55 classes, 1206 rooted instances, 880 with a pair, m = 1, 2, 3 on 560, 162, 158 roots, 244240 objects in this drawing, 4658 second-fixed objects, all assertions pass in both cycle orders. Walk lengths 0 (4627), 2 (30), 4 (1). The printed Section 7 sign fails on exactly the 718 roots with m odd. Signed count with m − 1 marks is zero on all 880 roots; with m + 1 marks it is nonzero on 823.

Running example: the published 279-object table agrees with this code object by object (set, sign, ι1, ι2). The lab's root order gives 213 objects, 141 first-fixed, 9 second-fixed. Over 69 drawings: 35 distinct object counts from 103 to 363, first-fixed 89 to 303, walk lengths up to 6, signed sum always −9, second-fixed always 9.
