# Report: review of draft B

Claude Fable 5.2, 2026-11-14. Folder `research/2026-11-14_fable_review-draft-B/`. Object: `paper/draft-B/barnette.pdf` (16 pages) and `barnette.tex`. I did not edit the draft.

1. Mathematics: every statement on the route to Theorem 1.1 is correct. One hypothesis is not checked: Euler's formula is applied to "`Z` and everything inside it" with no proof that this plane graph is connected. I judge it a real, small gap and supply the missing lemma (Lemma D, five lines, `PROVED-HERE`), which also gives the unstated connectedness of a coloured triangulation and of the glued pieces. Strict verdict as written: not established at that one node. With Lemma D: follows.
2. The author's own parts (face tree by duality, winding numbers for the slide, the `m`-fold finite difference, Lemma 4.6, Proposition 4.8) are sound. The worked example recomputes with `workings/barnette_lab`: 12 states, 8 pairs, 6 good states, `Σ = 18`, 6 Hamiltonian cycles avoiding the edge (`COMPUTED`). One side remark is underspecified: the hexagonal-prism count holds for one of the three sides of `t0` only.
3. Exposition: clearer than the best of the three papers at eleven of seventeen steps, and not clearer at two (weights, nonvanishing). Against the style guide: 13 pass, 1 mixed, 7 fail. The fails are the introduction's insider paragraphs, overloaded letters, process talk, and figures: two misplaced, most without the vertex labels the text uses, none for heights.
4. Two simplifications worth adopting, both proved in `REFEREE.md`: heights by a path of faces (no spokes, no winding numbers; `COMPUTED` on 736 cycle reversals), and the sign as a product `ε = ∏ δ(r(t), s(t))`, which the reviewer of draft A also found.
5. Against draft A: B has the better architecture, A the better first page, a cube overview figure and printed example data. `COMPARISON.md` gives a merge outline on B's skeleton. `EDITS.md` has 25 edits; every quoted old string occurs exactly once in the source (checked by script).

## What I set out to do

Review draft B in three separate phases. Phase 1: read only the PDF, page by page as rendered images, log every hesitation, then write the proof from memory. Phase 2: an informed review (referee report by reverse-Lamport audit, the 22 style rules, comparison with the three papers, unslop audit, figures, attribution, and at most 25 exact edits). Phase 3: read draft A and its review and write a comparison with a merge plan.

Phase separation was kept. Before finishing `COLD-READ.md` and `SUMMARY-FROM-MEMORY.md` I opened only `research/BRIEF.md` and the PDF. I opened `paper/draft-A/` only after `EDITS.md` was committed.

## What I established

| Claim | Status | Where |
| --- | --- | --- |
| Cold-read log: 78 entries, with every term used before definition, symbol clash, unverified step and figure problem | editorial | `COLD-READ.md` |
| After one reading I could reproduce the whole proof except the crossing conventions for heights and the last inequalities of the density bound | editorial | `SUMMARY-FROM-MEMORY.md` |
| Draft B proves Theorem 1.1 except for one unchecked side condition (connectedness of the disk graph, of `T`, of the pieces) | `PROVED-HERE` (audit), human review pending | `REFEREE.md` sections 2, 3, 7, 8 |
| Lemma D: a finite graph embedded in the sphere, each of whose faces is bounded by a cycle, is connected. Consequences for `R_Z`, `T` and the pieces | `PROVED-HERE` | `REFEREE.md` G1; proposed text in `EDITS.md` 1 |
| The "no pinched vertex" issue of the Lean proof does not arise in draft B's topological formulation | `PROVED-HERE` (by inspection of the third count) | `REFEREE.md` G1 |
| Spokes as "segments" need a wording change; the remark on changing paths is true, unproved and unused | `PROVED-HERE` | `REFEREE.md` G2, G3 |
| Example data of draft B: 12, 8, 6, two classes with `m = 2` and `L = (6,1), (3,1)`, `Σ ε ω^2 = 18`, one cancelling state on the triangle 1, 8, 9, signs three and three, 6 Hamiltonian cycles avoiding the edge and all recovered, `P_s` components as stated, orientations of the `D`-cycles as in the captions | `COMPUTED`: `python research/2026-11-14_fable_review-draft-B/recompute.py`, output `recompute.txt`; one instance (the running example) plus the hexagonal bipyramid with each of the three sides of `t0` | `REFEREE.md` section 6 |
| Hexagonal prism: 3 states, 2 good; 4 Hamiltonian cycles avoiding the edge when `e0` is the equatorial side, 2 for each apex side | `COMPUTED`, same script | `REFEREE.md` section 4, `EDITS.md` 15 |
| Heights can be defined by a path of faces in `G`, and then Lemma 4.6 follows from Lemma 2.4(1) with a four-case sign check | `PROVED-HERE`; `COMPUTED` by `check_face_paths.py` on the running example, the hexagonal bipyramid and 148 rootings of `barnette_lab.core.generated(12)` (94 with a pair, 344 pairs, 736 reversals of `D`-cycles), output `check_face_paths.txt` | `REFEREE.md` S1, `EDITS.md` 5 |
| `ε = ∏_t δ(r(t), s(t))` equals `(−1)^{(n+J)/2}` and shortens Lemma 4.4 | `PROVED-HERE` in `research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` section 2; rechecked here | `REFEREE.md` S2 |
| Remark 4.10's description of Li's marks and "the weight `ω^m` that all three papers use" are inaccurate | from astra's `REFEREE.md`; I did not reread Li's Definition 14 | `REFEREE.md` section 4 |
| 22 style rules: 13 pass, 1 mixed, 7 fail, 1 not applicable; comparison with the three papers; 18 unslop items; figure table; attribution findings | editorial (`HUNCH`) | `EXPOSITION-REVIEW.md` |
| 25 edits, 33 quoted old strings each occurring exactly once in `barnette.tex` | `COMPUTED`: `python research/2026-11-14_fable_review-draft-B/verify_edits.py`, output `verify_edits.txt` | `EDITS.md` |
| Comparison with draft A and a merge outline | editorial | `COMPARISON.md` |

## What failed, and what I did not do

- **I did not build the edited draft.** The edits are checked as string matches, not by compiling a scratch copy. Edit 16 adds a table and a label, edit 3 a package; a build could still show an overfull box or a float in a bad place.
- **My first geometric check of the disk counts was wrong.** Centroids computed from `paper/figures/layout-running.json` put three faces with a root corner inside cycles, because the figures draw the sides of `t0` as arcs and the saved coordinates are not a straight-line embedding. I excluded faces with a root corner, which cannot be inside a cycle of `D`, and the counts then agree. The reviewer of draft A reports the same property of the layout file.
- **The loop over the lab's generated family first ran on nothing.** `generated()` yields triangulations and I passed them to `Instance.from_primal`. The printed "rootings 0" exposed it; the committed script and output are the corrected run.
- **Li's note and the constructive paper were not reread in full.** For the step-by-step comparison I read OpenAI's paper completely, Li's introduction, and used `skeleton.md` and astra's referee report for the rest. Rows that depend on this are marked "per skeleton".
- **The Lean source was not opened.** The statement that the formal proof builds the same face tree as draft B rests on `research/2026-11-14_opus_lean-formalisation/DIFFERENCES.md` item 19.
- **Draft A was read once**, at lower resolution, and its review only in part (`REPORT.md` and the attribution paragraphs). The comparison is therefore lopsided, and says so.
- **The exact separating-triangle criterion** quoted from the constructive paper at the end of Section 5 was not checked. It is cited, not used.
- **Time.** I had no clock in the session. The work covers all three phases and all seven deliverables.

## What is still open

- A human reading of Lemma D, of the face-path proof of Lemma 4.6 (four sign cases) and of the product sign before any of them enters the paper.
- Whether to keep spokes at all. With face paths the paper never leaves `T` and its faces; without them, edits 6 and 7 are needed.
- The form of the Barnette 1969 citation (nobody in the project has seen page 343) and a pinpoint for Kelmans's reduction to graphs without nontrivial 3-edge cuts.
- Where reference [1], the unsigned constructive manuscript, can be found by a reader.
- Whether the merged paper should carry two examples (cube and the 13-vertex triangulation) against the style guide's rule 17. I recommend yes, with the cube confined to one overview figure and one table.

## Three best next steps

1. Apply edits 1, 8 and 10 to 25 to draft B, build, and rerun the author's `example.py` and my `recompute.py`. These edits do not depend on any merge decision.
2. Decide the two mathematical options together (face-path heights, product sign), have a human read the two proofs in `REFEREE.md` section 5, and then rewrite Section 4 once.
3. Merge along `COMPARISON.md`: A's opening paragraph, cube overview figure and printed states into B's skeleton; then a figure pass (labels in every example figure, one new figure for heights), then a cold read by a reader who has seen neither draft.

## Leads for others

- **Figure owner.** `layout-running.json` is not a straight-line embedding with respect to the sides of `t0` (vertex 3 lies below the chord 0 to 4). Anything that computes inside/outside from those coordinates must treat faces with a root corner separately. Shared `08-disk` ends its side table with OpenAI's form `2ℓ − h = −3`; both drafts state `W = B + 1`.
- **Both manuscripts.** OpenAI's Lemma 5.3 weights, Li's ray counts and the drafts' heights are the same object. The shortest rigorous version I know is the face-path one: a path of faces from each white face to `t0`, `±1` when it turns around the chosen corner, and the jump under a reversal is a count of crossings of `C` (REFEREE S1). It is the Lean's flow on `G` in the language of `T`.
- **Draft A.** Its Lemma 6 has the same Euler gap. Lemma D fits there unchanged.
- **History.** Draft B's remark that the prism map is not onto depends on the choice of `e0`. For a rung of the hexagonal prism there are four Hamiltonian cycles avoiding it and two good states; for an edge of a hexagon, two and two.

## Files

| File | Content |
| --- | --- |
| `COLD-READ.md` | phase 1 log |
| `SUMMARY-FROM-MEMORY.md` | phase 1 summary |
| `REFEREE.md` | reverse-Lamport audit, Lemma D, simplifications, recomputation, dependency table, verdict |
| `EXPOSITION-REVIEW.md` | style rules, comparison with the three papers, unslop audit, figures, attribution |
| `EDITS.md` | 25 edits with exact old and new text |
| `COMPARISON.md` | draft A against draft B, merge plan |
| `recompute.py`, `recompute.txt` | independent recomputation of the example |
| `check_face_paths.py`, `check_face_paths.txt` | check of the face-path heights |
| `verify_edits.py`, `verify_edits.txt` | check that the old strings of the edits match the source |

The page renders used for the cold read (`pages/`, `pagesA/`) are not committed. To regenerate: `python -c "import fitz; d=fitz.open('paper/draft-B/barnette.pdf'); [p.get_pixmap(dpi=130).save(f'p{i+1:02d}.png') for i,p in enumerate(d)]"`.
