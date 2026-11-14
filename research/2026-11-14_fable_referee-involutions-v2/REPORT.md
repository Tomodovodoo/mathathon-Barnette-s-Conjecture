# Report: second referee of the involution note

1. Lemma 7 (marks along face paths, no drawing) is CORRECT AFTER FIX: the mathematics holds, the statement was inexact and two sentences of the proof misdescribed the sectors. Fixed in the note.
2. COMPUTED: my own code reproduces every census count printed in the note and all 279 rows of its table, and passes every check with five families of face paths on all 1206 rooted instances through 14 vertices.
3. All 15 edits of the first referee are applied correctly; no sign or number regressed.
4. Figure 2 had a caption that described a move its picture did not show. It now shows a token move. Three other figures got label and caption fixes.
5. Final verdict FOLLOWS for Theorem 1 on both routes. The note is 18 pages, builds clean, and is committed.

## What I set out to do

Review the new Section 5 of `proofs/involutions/involutions.pdf` line by line and with independent code, confirm the first referee's 15 edits, recheck signs and numbers, judge the figures, apply corrections, and give a final verdict by the reverse-Lamport method.

## What is established

PROVED-HERE (in the note; reread and rederived here, details in REFEREE.md Section 1). With marks defined as turns of a fixed simple face path around the selected corner, the list of a cycle at a white face has odd length exactly for inside faces, consecutive entries cross in opposite directions, and the first entry of an inside face crosses right to left for a counterclockwise cycle. Both involutions, the fixed-set count `F` and the constructor then hold as in the ray version. The paths need not form a tree.

COMPUTED (`code/census.py 14 12`, `code/canonical.py 14 14`, `code/running.py`, `code/extra.py`; ranges and tables in `code/README.md`). All 1206 rooted instances through 14 vertices, 880 with a pair, `m = 1, 2, 3` on 560, 162, 158. Five path families and two ray directions (rays through 12 vertices with plantri input, through 14 in the note's own drawings). In every mode the number of second-fixed objects is `F` (total 4658), the signed size is `(-1)^floor(m/2) F`, and the moment identity has the sign `(-1)^((n+m)/2)`. For path tokens `H = -omega`, Lemma 4.6 of the main paper holds term by term, and the value of Proposition 4.8 is reproduced, as are the eight rows of the main paper's Table 2.

COMPUTED. The note's layout of the running example is the mirror image of the main paper's drawing. Turn signs in the note's Figure 3 are the negatives of those in the main paper's height figure. The note now says so.

## What failed, and what I did not do

Nothing failed mathematically. My first ray routine divided by zero on a spoke parallel to the ray; fixed before any reported run. I did not rerun the first referee's 69 drawings (the 213 count, the range 103 to 363, walks up to six in rays), the hard-family paragraph, the lab polynomial comparison, or Li's orientation dictionary; these stand on the first referee's and the reviser's checks. The 57 zeros at `m + 1` belong to the first referee's drawings; I reproduced the 78 of the author's drawings and the 123 and 125 of the two trees. Figure 3 is still a schematic of two paths and not a picture on the triangulation. I ran over the ninety minutes.

## Still open

- No bound on the walk length is known. Measured maxima: 2 (note's rays), 4 (breadth-first trees), 6 (non-tree paths, and rays in other drawings).
- Which choice of paths gives the fewest objects. Breadth-first trees give about 17000 objects over the census, a depth-first tree 718000.
- No human has read the note.

## Three next steps

1. Use the face-path form in the main paper's remark on Li (Remark after Proposition 4.8): it is the same height, expanded term by term, and needs no drawing. Keep the opposite normalization `H = -omega` and the orientation in view.
2. Draw Figure 3 on the triangulation, with the two paths and the turned corners, in the main paper's orientation, so that it can sit next to the main paper's height figure without a sign clash.
3. If a Lean formalisation of the forest-pair lemma is attempted, formalise the face-path form. Its only topological input is the Jordan property of a simple cycle in a sphere map.

## Leads for others

- The main paper's `omega` with shortest paths and this note's path tokens are literally the same data. A single figure could serve both.
- The count with `m + 1` marks depends on the paths (36 to 150 zero roots across families), so nothing canonical lives there.

## Files

`REFEREE.md` (verdicts, the 15 edits, figures, audit, synthesis paragraph), `CHANGELOG.md` (every change to the note), `code/` (README, scripts, `out/`), `pages/` (renders of the final 18 pages).
