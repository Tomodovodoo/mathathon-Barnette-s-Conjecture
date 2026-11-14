# Referee report on `research/2026-11-14_opus_route-induction`

Fable 5.2, 2026-11-14. I read `INDUCTION.md`, `PROOFS.md` (cited as OP), `REPORT.md`, `data/failed_inductions.json` and `code/README.md`. I did not run or import the author's code. Every number below comes from `code/` in this folder (commands in `code/README.md`). Generation uses plantri 4.5 from `workings/barnette_lab/vendor`.

Verdict in one paragraph. The four proved statements are correct as written and I found no gap in their proofs. Every computed count I could reach reproduces exactly. The induction does not prove the theorem, and the author says so. Two things in the write-up are wrong: the conjecture "some tree matching of `T/M` lifts" fails at `V = 18`, and it is not weaker than the contraction inequality as `INDUCTION.md` §4 says. The generation theorem with unread sources is not needed at all.

## 1. Proved claims, line by line

| Claim | Verdict | Notes |
| --- | --- | --- |
| OP Prop. 1.1, states split: `#states(T) = #states(T/M) + #states(T/N)` | CORRECT | The hypothesis "both merges loop-free" is always true (RESIDUAL-CASES.md Lemma 0, new). Reproduced on 58,530 vertex-root pairs, `V <= 16`, no failure. The same number of pairs as the author's range `V <= 16`. |
| OP Prop. 2.1, lift criterion | CORRECT | The edge count `n` edges on `n + 2` vertices is right because `T/M` has `n - 2` faces in `A`. Checked by comparing two independent counts of `TM(T/M)` and of `TM(T)` on 1,202,792 contractions, `V <= 18` (`pattern_vs_direct_fail = 0`). |
| OP correction of route-graph-theory Lemma 6.2(iii) | CORRECT | Reproduced: 13,210 simple contractions with `V <= 17` have M-type tree matchings of `T` whose projection is not a tree matching. Smallest simple example confirmed (`V = 11`, graph 1, `x = 5`, merge `{6, 4}`, six roots). |
| OP Lemma 3.1, local condition | CORRECT | `g != t0` under the hypothesis, as stated. `local_condition_fail = 0` on 335,180 failing lifts, `V <= 18`. |
| OP Prop. 3.2, rotation | CORRECT | The case `c = b` cannot occur at all, since `a !~ b` (Lemma 0). I tested the criterion "`rho(s)` is a tree matching iff `b` not in `K2'`" against a direct spanning-tree test of the rotated state: `rot_criterion_fail = 0` on the same failing lifts. |
| OP Cor. 3.3, partial injection | CORRECT | 466 exceptions among 28,189 failing lifts for `V <= 16`, reproduced per `V` (8, 20, 80, 358). First exception `V = 13`, first one without root neighbour `V = 14`, both confirmed on the stated instances. |
| OP Prop. 4.1, evenness and sign balance | CORRECT | The proof imports Step 1 of the refereed polynomial form, so it uses the sign-reversing involution and the disk identity. It is not part of a cancellation-free route. `TM_odd = 0` on 71,224 rooted instances, `V <= 18`. Sign balance re-checked for the tree matchings of 9,880 contractions, `V <= 15` (`code/signs.py`). |

I looked for hidden hypotheses in each proof. I found three small ones, none of which breaks anything. OP §0 needs `x` to be a non-root. Its four faces then avoid `t0` automatically, so the extra condition in the text is redundant. OP Prop. 1.1 uses that no face outside `x` contains both `v1` and `v2`, which is the loop condition and is always true. OP Prop. 3.2 uses `c != v1`, which the author derives from `v1 !~ v2`.

## 2. Computed claims

| Claim | Author's range | Reproduced | Extended |
| --- | --- | --- | --- |
| (L+) `#TM(T) >= #TM(T/M)` | 344,872 contractions, `V <= 17` | exactly 344,872, 131,336 simple, 0 failures | `V = 18`: 857,920 contractions, 0 failures |
| (G) good contraction exists without separating triangle | 7,386 rooted instances, `8 <= V <= 17` | exactly 7,386, 0 failures | `V = 18`: 16,032; `V = 19`: 38,998; 0 failures |
| pair iff tree matching; pair iff no black-inner separating triangle | `V <= 14` smoke test | 71,224 rooted instances, `V <= 18`, 0 failures | |
| rooted instances | 21,848 for `V <= 17` | 21,848 | 49,376 at `V = 18` |
| (L) "some tree matching of `T/M` lifts" | 344,872, `V <= 17` | holds for `V <= 17` | WRONG as a conjecture: fails in 50 contractions at `V = 18` |
| pair existence lost by a simple contraction | 7,510 of 131,336 | 7,510 (36, 96, 183, 570, 1495, 5130 for `V = 11, 13..17`) | |

The counterexample to (L): `plantri -b -a 18`, graph 309, root `(5, 0, 6)`, `x = 11`, merge `{10, 2}`. `T` has no separating triangle and 14 tree matchings, `T/M` has 2, neither lifts, both rotate (`data/nolift_18.jsonl`, 50 rows). So for existence the right weak statement is "some tree matching lifts or rotates". That one holds on every contraction with tree matchings up to `V = 18`.

`INDUCTION.md` §4 says conjecture (L) asserts that some tree matching lifts, "or more strongly" the inequality. The two are incomparable. At `V = 18` the inequality holds while nothing lifts. The induction needs positivity of `#TM(T)`, which follows from the inequality and not from (L).

Not re-checked: S3 (`C >= b`), S5 for pairs, `D` and `c_min` beyond the one example R9, S6 and the count in R13 (P-reductions), S7, S8, the least-squares fits, and the integer formula for `lc`. Monotonicity of `#states` needs no check, it follows from OP Prop. 1.1.

## 3. The thirteen refuted schemes

`code/check_refuted.py`, output `data/check_refuted.txt`. The author's root index refers to his own face order. I searched all roots of the stated graph and report the roots where the failure occurs.

| Id | Verdict | What I saw |
| --- | --- | --- |
| R1 | CONFIRMED | `V = 6`: one M-type tree matching of `T`, `T/M` has none and is not simple. `V = 11`, graph 1: six roots with `TM(T) = 4`, two of M-type, `T/M` simple without pair. |
| R2 | CONFIRMED | same instance |
| R3 | CONFIRMED | `V = 8`: four roots with `TM(T/M) = 2`, one lift fails, root neighbours 2. `V = 10`, graph 1, `x = 8`, merge `{9, 7}`: two roots without root neighbour. |
| R4 | CONFIRMED | `V = 8`: `B = 0 < b = 1`, and `C = 1` |
| R5 | CONFIRMED | `V = 10`, graph 1, `x = 9`, merge `{2, 8}`: four roots with 2 tree matchings of `T/M`, none satisfies the local condition, both lift |
| R6 | CONFIRMED | `V = 13`, graph 7, `x = 10`, merge `{8, 4}`, root `(4, 0, 5)`; `V = 14`, graph 12, `x = 2`, merge `{9, 0}`, roots `(11, 8, 13)` and `(11, 5, 6)` without root neighbour |
| R7 | CONFIRMED | `V = 8`: `TM(T) = TM(T/M) = 2` |
| R8 | NOT RE-CHECKED | I did not implement `lc`. The drop of `c_min` that the lesson cites is confirmed under R9. |
| R9 | CONFIRMED | `V = 14`, graph 7, `x = 12`, merge `{10, 6}`: `c_min` is 1 for `T` and 3 for `T/M` |
| R10 | CONFIRMED | `V = 6`: `2 != 0 + 0`. `V = 13`, graph 7, `x = 10`: `6 < 4 + 4` at two roots. RESIDUAL-CASES.md Theorem 4(b) explains the deficit: it is twice the number of exceptions. |
| R11 | CONFIRMED | `V = 8`, face `(3, 6, 5)`, corner 3, root `(1, 0, 2)`: 0 of 2 tree matchings. The count 20 of 13,130 was not re-checked. |
| R12 | CONFIRMED | `V = 9`: at all 8 roots with a pair, no contraction is simple |
| R13 | CONFIRMED at `V = 6` by hand | Removing two adjacent vertices of the octahedron leaves 4 vertices and a doubled edge. The count 15,226 of 58,593 was not re-checked. |

## 4. Reverse-Lamport audit of the induction

Audit boundary. Conclusion `C0`: every rooted simple Eulerian triangulation `(T, t0)` with a pair has a tree matching. Route: `INDUCTION.md` §4, strong induction on `|V|`. Accepted primitives: the definitions of `research/BRIEF.md`, Euler's formula, and the two refereed imports named in the table.

    C0 <- R0 (AND: O1, C1, C2)
    C1 (separating triangle) <- R1 (AND: O2, O3, O4, IH)
    C2 (no separating triangle, V > 6) <- R2 (AND: O5, O6, O7, O8, IH, O9)

| ID | Exact claim or obligation | Needed by | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- |
| C0 | pair implies tree matching, all rooted `T` | root | root | R0 | open |
| O1 | base: the octahedron has a tree matching at each root, and no smaller Eulerian triangulation exists | C0 | algebraic/logical step | computed, 8 roots; `sum(6 - deg) = 12` forces 6 vertices | discharged |
| O2 | a separating triangle of a `T` with a pair has white inner boundary | C1 | named theorem | pair criterion, route-graph-theory Thm 2.1, refereed by sol; recomputed here, `criterion_fail = 0` | discharged |
| O3 | cutting gives two simple Eulerian triangulations with fewer vertices, the inner one rooted at its black cap, the outer one with a white cap and the old root | C1 | side condition | OpenAI §7; sol INTEGRATION §4 | discharged |
| O4 | pairs and tree matchings multiply | C1 | named theorem | route-categorical Prop. 6, proof re-read here and correct | discharged |
| O5 | a non-root vertex of degree 4 exists | C2 | algebraic/logical step | at least 6 vertices of degree 4, at most 3 roots | discharged |
| O6 | at each degree-4 vertex one merge is simple | C2 | proved earlier | route-graph-theory Lemma 6.1; short proof below | discharged |
| O7 | (G): some `x`, `M` with `T/M` simple and with a pair | C2 | missing | computed for `8 <= V <= 19` only | failing |
| O8 | `T/M` is in the class: simple, Eulerian, rooted at the image of `t0`, `V - 2 >= 6` vertices | C2 | side condition | `x` is a non-root, `v1, v2` are not both roots because they are not adjacent; separating triangles in `T/M` are allowed because the induction is over the whole class | discharged |
| O9 | `TM(T/M)` nonempty implies `TM(T)` nonempty | C2 | missing | OP Cor. 3.3 proves it up to the exception set; RESIDUAL-CASES.md Theorem 4(a) proves it when `T/N` has no tree matching | failing in the two-sided case |

Proof of O6, written out because the brief asks whether the generation theorem supplies it. Suppose both merges at `x` fail to be simple. Loops do not occur, so `v1, v2` have a common neighbour `w` and `a, b` a common neighbour `w'`, both outside the closed neighbourhood of `x`. The cycle `x v1 w v2` separates `a` from `b`, so the path `a w' b` meets it, and `w' = w`. Then `w` is adjacent to all four neighbours of `x`. The four triangles `w a v1`, `w v1 b`, `w b v2`, `w v2 a` are faces because `T` has no separating triangle, and with the four faces at `x` they close up the sphere. So `T` is the octahedron. ∎

Critical findings.

1. O7 and O9 are open. The route does not establish `C0`.
2. The generation theorem is not on the route. Batagelj's theorem says that some sequence of inverse P- and Q-operations reaches the octahedron. It does not say that a Q-reduction exists away from the root, that it keeps a pair, or that P-operations can be avoided. The induction needs none of that from the literature: O5 and O6 are elementary. So the four `LIT` rows of `INDUCTION.md` §1 with unopened sources carry no weight in the argument. The third row there has status "`LIT`, abstract only" for a statement the author could not read in full. It should be tagged as not verified. Since nothing depends on it, the cleanest fix is to drop the generation theorem from the proof and keep it as motivation.
3. Parallel edges. (G) asks for a simple `T/M`, so the induction never contracts into a multigraph. That is necessary: a non-simple contraction has no pair (RESIDUAL-CASES.md Lemma 1, new). OP states the inequality for multigraph results too, where it is trivially true.
4. Separating triangles created by the contraction are harmless for the logic, because the hypothesis is applied to the whole class. They are the content of (G): a new separating triangle through `v` comes from a 5-cycle through `v1 x v2`, and it is black-inner exactly when `t0` is off the black side of that 5-cycle (MISSING-LEMMA.md Lemma B).
5. The root face survives every contraction used, and the three roots stay distinct.
6. Step 2 of `INDUCTION.md` §4 cites "OpenAI Prop. 3.1 together with route-graph-theory Lemma 2.2" for the white inner boundary. The statement needed is route-graph-theory Theorem 2.1 (the criterion), of which Lemma 2.2 is the tool. Wording only.
7. `REPORT.md` says the lift-or-rotate rule covers 98.3% of failing lifts. That is the figure for `V <= 16`. The share falls with `V`: 97.8% at `V = 17`, 97.5% at `V = 18`.

Verdict. NOT ESTABLISHED BY THIS PROOF. The decisive nodes are O7 and O9. This does not show `C0` false, it is the known theorem, and it does not rule out closing the two nodes. The proved part of the route is correct: O1 to O6, O8, and O9 in the one-sided case.

## 5. Verdict per claim

| Claim | Verdict |
| --- | --- |
| State splitting (OP 1.1) | CORRECT |
| Lift criterion (OP 2.1) and the correction of the older lemma | CORRECT |
| Local condition, rotation, partial injection (OP 3.1, 3.2, 3.3) | CORRECT |
| Evenness and sign balance (OP 4.1) | CORRECT, with imported cancellation |
| (L+) contraction inequality, computed | REPRODUCED, extended to `V = 18`, still a conjecture |
| (L) some tree matching lifts | WRONG beyond `V = 17` |
| "(L+) is stronger than (L)" | WRONG |
| (G), computed | REPRODUCED, extended to `V = 19`, still a conjecture |
| Thirteen refuted schemes | 11 CONFIRMED on the stated instances, R13 at `V = 6` only, R8 not re-checked |
| Generation theorem as an ingredient | GAP if relied on; CORRECT AFTER FIX once it is removed, since it is not needed |
| The induction proves "pair implies tree matching" | GAP at (G) and at the two-sided lifting step |
