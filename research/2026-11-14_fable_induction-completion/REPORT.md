# Report: refereeing and trying to complete the inductive route

Fable 5.2, 2026-11-14, folder `research/2026-11-14_fable_induction-completion/`.

**Summary.**
1. The induction does not close. There is no cancellation-free second proof of Proposition 5.1 here. Two lemmas are missing, and `MISSING-LEMMA.md` states them exactly.
2. Referee: the four proved statements of `research/2026-11-14_opus_route-induction` (state splitting, lift criterion, rotation, evenness) are correct. Every computed count I compared reproduces exactly with my own code, and (L+) and (G) still hold at `V = 18` and `V = 19` (`COMPUTED`).
3. One of the author's conjectures is false: "some tree matching of `T/M` lifts" fails in 50 contractions at `V = 18` (`REFUTED`). The contraction inequality survives. The two were wrongly ranked in `INDUCTION.md`.
4. New, `PROVED-HERE`: the rotation is a bijection between the exception sets of the two contractions at `x`. So `#TM(T) >= #TM(T/M)` holds whenever the other contraction has no tree matching, and `#TM(T) >= #TM(T/M) + #TM(T/N) - 2e` always, sharp at `V = 13`.
5. What is left is a two-sided step (not every tree matching of both contractions is exceptional) and (G). For (G) I proved a reformulation by tight sets and one restriction on a counterexample, no more.

## What I set out to do

Half 1: referee the inductive route line by line, reproduce (G) and (L) independently, confirm the 13 refuted schemes, and audit the logical shape of the induction. Half 2: find the second rule for the 466 residual cases, prove (G), test the weaker existence statement, and write the complete proof if it closed.

## What I established

Referee (`REFEREE.md`).

- OP Prop. 1.1, 2.1, Lemma 3.1, Prop. 3.2, Cor. 3.3 and Prop. 4.1 are correct. I found no gap. Prop. 4.1 imports the sign-reversing involution, so it is outside a cancellation-free route.
- `COMPUTED` with own code (`code/census.py`): 344,872 rooted contractions for `V <= 17` and 857,920 at `V = 18`, no failure of `#TM(T) >= #TM(T/M)`. (G): 7,386 rooted instances for `8 <= V <= 17`, then 16,032 at `V = 18` and 38,998 at `V = 19`, no failure. 466 exceptions among 28,189 failing lifts for `V <= 16`, as claimed. State splitting on 58,530 vertex-root pairs.
- 11 of the 13 refuted schemes confirmed on the stated instances. R13 only at `V = 6` by hand, R8 (`lc`) not re-checked.
- Reverse-Lamport audit: the induction is sound in shape, with open leaves exactly at (G) and at the lifting step. The generation theorem with unread sources is not used by the argument and can be dropped. A degree-4 non-root vertex exists by Euler's formula, and a simple merge exists by a five-line argument.

New results (`RESIDUAL-CASES.md`, all `PROVED-HERE` unless tagged).

- Opposite neighbours of a degree-4 vertex are never adjacent. Both merges are always loop-free.
- A non-simple contraction has no pair, so the inequality is trivial there.
- A table of `TM(T)`, `TM(T/M)`, `TM(T/N)` as sets of outer states of `T - x` with a missing vertex and a two-component forest. Seven patterns. A state of pattern `{a v1 | b v2}` is never a tree matching of `T`.
- Every exception has that pattern, and the rotation maps the exceptions of `M` bijectively onto the exceptions of `N`. An exception of `M` rotates to a tree matching of `T/N`.
- One-sided inequality: if `T/N` has no tree matching, `#TM(T) >= #TM(T/M)`, with OP's injection and no exception.
- `#TM(T) >= #TM(T/M) + #TM(T/N) - 2e`. `COMPUTED` sharp in 783 vertex-root pairs, `V <= 17`. It explains the deficit in the author's R10.
- If `x` has two root neighbours there are no exceptions.
- `COMPUTED`: 7,940 exceptions for `V <= 18`, all of the one shape, classified in `data/residual_summary.json`. At most half of the tree matchings of a contraction are exceptional (`V <= 17`).

For (G) (`MISSING-LEMMA.md` §3): a deficiency formula `f(S) = sum (d + w - 6)/3` for the Hall function, the characterisation of bad merges by 4-cycles and 5-cycles through `v1 x v2`, the effect of contraction on `f`, and Proposition D: in a counterexample, every degree-4 vertex of a minimal tight set has two consecutive neighbours outside it.

## What failed, and why

- A second local rule. The exceptions have no local signature beyond "both contractions are simple and have tree matchings". The obstruction is where `b` sits in a spanning tree. The only black faces on the hole are `g` and `g'`, and the rotation at `g'` does not apply to an exception.
- A sign argument. Pattern-`P_1` tree matchings are sign-balanced among themselves in 103 of 693 contractions (`V <= 15`), so sign balance of `TM(T/M)` does not force a tree matching of another pattern.
- A rank argument. States are counted by a determinant, and state splitting is a cofactor expansion. Tree matchings are the states with exactly one mate, and I found no linear-algebra handle on that.
- Choosing `x` to avoid the two-sided step. A vertex with exactly one good contraction exists in most instances but not in `V = 14`, graph 31 (all 24 roots), nor in 175 rooted instances with `16 <= V <= 19`.
- (G). I ran out of time after Proposition D. The remaining case analysis is finite but I did not do it, and the step "a minimal tight set is the inside of one short cycle" is only sketched.

## What is still open

- ML2, the two-sided step (`MISSING-LEMMA.md` §2), and its stronger form `2|E_M| <= #TM(T/M)`, which would give the full contraction inequality.
- ML1 = (G).
- Not machine-checked: the deficiency formula (Lemma A). Not re-checked from the author's folder: R8, the counts in R11 and R13, S3, S5 beyond states, S6, S7, S8.

## Three best next steps

1. Attack ML2 through the bound 1/2. Extend `code/superadd.py` to `V = 18, 19` and look for an explicit involution on `TM(T/M)` that moves every exceptional tree matching to a non-exceptional one. First test: does the mate `r_s` or a single `D`-cycle reversal of an exceptional `s` give one?
2. Finish (G) from Proposition D. Enumerate minimal tight cycles on the census, check that some interior degree-4 vertex is not a boundary apex, then prove it by cases on cycle length 4, 5, 6.
3. Use the one-sided inequality now. It is a complete, cancellation-free induction step wherever a non-root degree-4 vertex has exactly one contraction with a pair. Such a vertex exists at every rooted instance without separating triangle and `8 <= V <= 13` (`data/onesided_8_16.json`). It is short enough for the exposition as "why lifting almost works".

## Leads for others

- For the author of route-induction: replace conjecture (L) by "some tree matching lifts or rotates", cite the `V = 18` counterexample, and drop the generation theorem from the proof.
- For the counting agents: `#TM(T) >= #TM(T/M) + #TM(T/N) - 2e` is a proved recursive lower bound for the number of tree matchings.
- For the exposition: Lemma 0 and the pattern table make the degree-4 contraction a clean worked example of how a tree matching can fail to survive a local change.
