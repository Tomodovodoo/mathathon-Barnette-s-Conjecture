# Quoted larger ranges

COMPUTED, source reconciliation only. I compared the note's larger-order assertions with `research/2026-11-14_opus_reconcile/FACTS.md`. A match here means that the cited sources report the same finite result. It does not mean I recomputed their larger campaigns.

| Note's assertion | Reconciliation and source check | Result |
| --- | --- | --- |
| A cover without a good state at 16 vertices | FACTS witness row; Opus rainbow INTEGRATION section 5 | matches; independently recomputed here |
| Step X through 17; 1492 of 1543 triangulations at 18, 51 unfinished | FACTS gives original 1485 plus seven; Opus REPORT gives completed indices and remaining 51 | matches, arithmetic checked |
| Sampled Step X through 120 | Not a separate FACTS row; topology RAINBOW.md reports it | matches source, finite samples only |
| Strict rainbow descent first fails at 8 | FACTS strict-descent row | matches; recomputed here |
| Periodic walks at 38 with periods 48,68 and at 40 with 60 | FACTS evict/surplus row gives 38; Opus REPORT and periodic replay list 48,68,68,60 | matches, witness sizes not minima |
| No periodic walk through 15 | Not a separate FACTS row; topology RAINBOW.md supplies finite range | source-supported; not rerun |
| Load M-convexity fails at 12 | FACTS load row and topology RAINBOW.md | matches |
| Involutions need not be transitive at 13 and 14 | Not a FACTS row; topology RAINBOW.md reports 24 failures among 672 rootings at 13-14 | matches source, not independently replayed at these sizes |
| Pair descent all pairs through 16 by two programs, through 22 by original | FACTS verified-range row gives completed independent range 20 and original 23; final reports agree | stale ranges corrected in TeX and STATUS.md |
| Strict pair descent first fails at 16 | FACTS strict-descent row | matches |
| Three and four moves needed at 21 and 40 | FACTS lookahead row; Astra INTEGRATION | matches; 21 has a minimality proof by census, 40 is a witness |
| Non-increasing cover-cycle constraint fails at 16 | Astra INTEGRATION; not a separate FACTS row | matches source |
| Contraction half-exception count through 18 | FACTS contraction row, Astra INTEGRATION | matches |
| Fixed-cover lifting repair fails at 18 | FACTS repair row, Astra INTEGRATION | matches |
| Some usable contraction exists, no counterexample known | FACTS Lemma G row gives 62,416 instances, orders 8-19; Astra INTEGRATION | consistent; the note makes the weaker statement |
| Plateau depth at most 7 in exhaustive range, 27 in samples through 120 | topology RAINBOW.md section 6; no separate FACTS row | matches original report; not a uniform theoretical bound |

LIT. External sources opened independently in this review:

- https://homepages.cwi.nl/~lex/files/dict.pdf, title page and printed pp. 188-189, Exercises 10.26-10.29.
- https://ir.cwi.nl/pub/2216, bibliographic record.
- https://ir.cwi.nl/pub/2216/2216D.pdf, title page, pp. 1674, 1685-1686 and bibliography p. 1699.

The original Rado, Nash-Williams and Edmonds papers were not opened. The theorem statements were checked in Schrijver's sources, as described in REFEREE.md.
