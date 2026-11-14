# Report: referee of the rainbow route and of the two-tree packing

1. Fable's Step R (a rainbow tree exists iff no separating triangle has black inner boundary) is CORRECT. I checked every line and reproduced its counts with my own code.
2. Theorem S (every rainbow tree lies in exactly one 2-factor, as an in-forest of `G_u`) and the "evict the resident" involutions are CORRECT. So the number of good states is even, by a proof with no sign in it.
3. The height identity and the face-count retraction lemma are CORRECT. The three refutations reproduce: periodic walks at `V = 38, 40`, strict descent at `V = 8`, M-convexity at `V = 12`.
4. Opus's Lemma 1.2, Theorems 2.1, 2.7, 3.3 and their corollaries are CORRECT. The three theorems cited from memory are now located in sources opened here, and each use meets their hypotheses. The `V = 16` cover with no good state is confirmed.
5. Step X remains a conjecture. I reproduced it for `V <= 12` and finished 7 of the 58 `V = 18` triangulations that Fable's run had cut off: 224 rootings, 8.0 million rainbow trees, no trap.

Opus 5.5, 2026-11-14. Folder `research/2026-11-14_opus_referee-rainbow/`. Files: `REFEREE-rainbow.md`, `REFEREE-packing.md`, `INTEGRATION.md`, `code/` (with README), `data/`.

## What I set out to do

Referee, with my own reasoning and code, the proofs in `research/2026-11-14_fable_referee-topology/RAINBOW.md` (and the two proofs in its `REFEREE.md` that the brief names) and in `research/2026-11-14_opus_two-tree-packing/PROOFS.md`/`PACKING.md`. Locate the literature the packing proofs cite from memory. Write the safe statements with proofs in publication style.

## What I established

Referee verdicts (details in the two referee files):

| Claim | Verdict |
| --- | --- |
| Theorem R, identity (R), Lemma R2, Lemma X1 | CORRECT |
| Theorem S, Proposition U | CORRECT; "alternating cycles" in Prop U should read "alternating closed trails" |
| `ι_t` fixed-point-free involutions | CORRECT |
| height = signed white area | CORRECT, convention "counterclockwise is up" to be stated |
| retraction lemma by face count | CORRECT |
| refutations (f1)-(f3) | CORRECT, reproduced |
| Step X | CONJECTURE |
| Lemma 1.2, Thm 2.1, Prop 2.2, 2.3, Rem 2.4, Thm 2.5, Cor 2.6, Thm 2.7, Cor 3.1, 3.2, Thm 3.3, Prop 4.1, 4.2 | CORRECT; fix the publisher of Edmonds 1973 (Academic Press) |
| `V = 16` cover with no good state | CORRECT: plantri index 27, outer face `{0, 1, 2}`, one-cycle cover, the only bad one of 42 covers over all rootings of that triangulation |

Literature located (opened in this session): Rado and Nash-Williams as Exercises 10.26 and 10.29 (with Edmonds' covering theorem 10.28) of Schrijver, *A Course in Combinatorial Optimization*, CWI, March 23, 2017; Edmonds' disjoint branchings and matroid intersection in Schrijver, *Polyhedral combinatorics*, Handbook of Combinatorics ch. 30 (Application 5.6, Theorem 5.26, pp. 1685-1686), already held in the project. Not located: Schnyder / de Fraysseix-Ossona de Mendez (only used in a remark).

COMPUTED (mine, `code/README.md` has commands):

- All rootings `V <= 12`: identity (R) on 57,901 connected sets; 74,432 rainbow trees; Lemma X1 by brute force on 651,072 (tree, point) pairs; Theorem S(1)-(3) and Proposition U on every tree and every 2-factor; 5,052 evaluations of `ι_t`; Step X (no trap) in all 208 instances; M-convexity fails exactly in the two instances with two 2-factors.
- All rootings `V <= 14`: Lemma 1.2 on every vertex set (880 rootings hold, 308 with a black-inner triangle fail); Theorems 2.1 and 2.7 on all 932 covers and 8,800 random maps; Theorem 3.3 and Corollary 3.2 by brute force on all 932 covers; Prop 2.3 on 1,212 forced maps; its "only if" on 3,260 random maps; Corollary 2.6 also without a pair (326 rootings).
- Fable's periodic walks: four trees replayed, periods 48, 68, 68, 60.
- Step X at `V = 18` on the cut-off set: see the section below.

PROVED-HERE (mine): the missing sentences listed in the referee files (duality of `H` and `W`; faces of `T[U]` are open and closed; closed trails in Prop U; `I >= 2` in Remark 2.4; identity (3) of INTEGRATION). INTEGRATION.md has the publication-style proofs of Step R, Theorem S and the evenness of the number of good states.

## Step X at `V = 18`

COMPUTED (`code/stepx.py 18 1542,1541,103,...,315 420`, output `data/stepx_18_*.json` and `data/stepx_18.log`). Seven of the 58 triangulations that Fable's run left out are now complete: plantri indices 1541, 1542 and 103 to 107. That is all 224 of their rootings. None has a black-inner separating triangle. 104 have a single 2-factor and are covered by Proposition U (I assert there that the number of rainbow trees is `2^n`). In the other 120, all 7,999,488 rainbow trees were enumerated (as acyclic selections inside 2-factors, Theorem S) and every one can descend: no trap. Index 108 was cut off by the time cap after 17 of its 32 rootings, all fine. The remaining 51 triangulations (108 to 130, 310 to 337) are still open in both runs. Cost: about 40 microseconds per tree and exchange in Python; the two indices above 1540 are the largest, with 2.1 and 2.5 million trees.

## What failed and why

- My first 2-factor enumeration had no pruning and stalled at `V = 16`; a closure-pruned version fixed it. My first cover-state enumerator mixed face and vertex indices (both integers); I caught it because it hung, fixed it with tagged keys, and reran.
- I replayed only four of Fable's periodic examples; `walk_saved.json` uses another layout.
- I did not recompute the height identity numerically, and I did not rerun Theorem R above `V = 12` (Fable's run covers `V <= 16`, mine of the pair criterion covers `V <= 14`).

## What is still open

1. Step X.
2. Corollary 2.6 without the pair hypothesis (holds for all rootings `V <= 14`).
3. The "only if" of Proposition 2.3.
4. The face-side split P2 (not refereed here; the author marks it as conjecture).

## Three best next steps

1. Put INTEGRATION.md §1 to §3 into the manuscript as the sign-free part: Theorem 1 plus Corollary 4 is a second proof that a pair exists, and Theorem 7 is a combinatorial reason for evenness.
2. Attack Step X through Theorem 3: inside one cover the problem is acyclic re-pointing in `G_u`; the exchanges that leave a cover are exactly the directed cycles of `G_u`. A potential that decreases on one of the two kinds of move is the missing piece.
3. Finish the remaining cut-off `V = 18` triangulations with a compiled implementation (the per-2-factor enumeration in `code/stepx.py` is the right algorithm; Python costs about 40 microseconds per tree and move).

## Leads for others

- Rado and Nash-Williams can both be cited from one open source (Schrijver's course notes, Exercises 10.26, 10.28, 10.29). The manuscript should cite it instead of the 1942 and 1964 papers alone, which nobody in the project has opened.
- The `T/R` and `W` versions of the packing failed on exactly the same random maps in rootings without a pair; that is expected from the shared inequality but worth one sentence in the paper.

## Protocol

All writes are in this folder. No subagents. One heavy process at a time, longest 7 minutes. Fable's folder was read for the definitions and to load the saved counterexamples; the packing author's code was not read.
