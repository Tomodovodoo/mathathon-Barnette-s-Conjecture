# Report: synthesis final pass

1. `digestions/SYNTHESIS.md` is at 4,972 words by its gate (`audit.py`, unchanged copy of Astra's), down from 5,910; the gate and `check.py` exit 0.
2. The closing runs are in a new section 12, each with its review status; the sign-free note's Figure 5 is marked as not re-reviewed, the atlas repair as unaudited.
3. The owner section lists nine decisions: author lines of four documents, 50 third-party PDFs, `E:\lbb`, the two temporary clones, drafts A and B, 41 MB of proof sheets, gluing with perfect matchings, the 20-page length, and where a human should start.
4. `products` figure redrawn for the new run count (88); `route-outcomes` unchanged.
5. Not done: no second reader of this cut.

## What I set out to do

Bring the synthesis to its final state under its own 5,000-word gate, add the runs of the last two hours, and complete the owner section, without dropping a qualification, review status, counterexample size or housekeeping item.

## What I established

The cut is mostly repetition: census sizes stated in both section 7 and section 11, the Lean counts in three places, a correspondence table that exists in its own file, and second links to the same evidence. CHANGELOG.md lists every kind of cut. Inventory at 2026-11-14 15:22 UTC: 88 run folders, all with a final report; 246 route records, 77 refuted; page counts unchanged (20, 18, 15, 18, 34). Every relative link resolves (101 checked by `check.py`, 101 by `audit.py`). Outputs: `check-output.txt`, `audit-output.txt`, `synthesis-audit/count-output.txt`, `synthesis-audit/counts.json`.

## What failed

`check.py` from the reconcile run rejected a snapshot with no open run; I fixed my copy. One number was wrong in the old text: 53 third-party PDFs; there are 50.

## Open

No other model has read this version. The products figure has no box for the sign-free note. The optional figure review's caption-length gate is still red (release check).

## Next steps

1. A cold read of SYNTHESIS.md against FACTS.md by a different model.
2. Add the sign-free note to the products figure.
3. The owner's nine decisions.
