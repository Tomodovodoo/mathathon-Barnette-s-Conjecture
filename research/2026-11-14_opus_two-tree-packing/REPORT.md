# Report: the two-tree packing route

The probabilistic folder's half-pair packing conjecture is true. I prove it (PROOFS Thm 2.1) by Nash-Williams plus an extension of OpenAI (3.2) to all vertex sets, with no signed count.
It is much weaker than it looked: it holds for every choice of a deleted corner per black face, pairs or not, so it never sees the state structure.
The same count proves: `Q_r ∪ Q_s` re-splits into two root-separating forests (Thm 2.7), and every pair support splits into two point-rainbow trees (Thm 3.3, via Edmonds' branchings).
The face-side twin (P2) is a new conjecture, true on all 14,881 supports with `V <= 17`. Doing both sides at once is the key lemma and fails inside a fixed support.
The positive-weight mean obstruction is correct but only excludes full-support measures on all of `H`; it is not why positive-measure arguments fail. The integrality gap is.

Opus 5.5, 2026-11-14. Folder `research/2026-11-14_opus_two-tree-packing/`. Files: `PACKING.md` (statements, relationships, status table), `PROOFS.md` (complete proofs, re-read adversarially in §5), `REFEREE.md` (verdicts on the probabilistic folder), `PREDICTIONS.md` (written before the runs), `code/`, `data/` with READMEs.

## What I set out to do

Take the two-tree packing conjecture seriously as a counting-free route to the key lemma: state it precisely, say what it implies, relate it to the density inequality (3.2), Nash-Williams, matroid union, Schnyder woods and the 3-colouring; referee the 278 cases and 27 certificates with my own code and hunt for counterexamples; prove it or refute it; referee the positive-weight mean obstruction; say what a proof would give.

## What I established

`PROVED-HERE` (T2, unreviewed):

- **Lemma 1.2.** With no black-inner separating triangle, `e(U) - b(U) + max(0, |U ∩ R| - 1) <= 2|U| - 2` for every nonempty `U`. For `U ⊇ R` this is (3.2).
- **Theorem 2.1.** Under the pair criterion, for every deleted-corner map `u`, the `2n` white-face edges of its support split into two spanning trees of `W`. This includes the conjecture. The Nash-Williams term of each black face is at most its Hall shortfall, so (3.2) extended is the two-forest condition.
- **Proposition 2.3.** Without the criterion the statement fails for arbitrary maps: any `u` that deletes a triangle corner in all three inner faces along a black-inner triangle fails. Remark 2.4 recalls why no pair exists there.
- **Theorem 2.5 / Corollary 2.6.** The box `{face sums 1, 0 <= y <= 1/2}` lies in the tree polytope of `W`; `W` minus the triangle of `t0` is three spanning trees (a Schnyder-type statement for `W`).
- **Theorem 2.7.** `E(T) - E(t0) - D_u` is two spanning trees of `T/R`. For a pair, `Q_r ∪ Q_s` always re-splits into two forests with one root per component, but not transversally.
- **Corollary 3.1.** The three-matroid LP is feasible whenever a pair exists, with witness `(r + s)/2`, without signs.
- **Corollary 3.2, Theorem 3.3.** Inside every pair support there is a face-rainbow tree and a point-rainbow tree (Rado). Every pair support splits into **two** point-rainbow trees (Edmonds' disjoint branchings, the same count). So every 2-factor of `B` carries at least two of fable's rainbow trees.
- **Propositions 4.1, 4.2.** `E(T) - E(t0) = Q_r ⊔ Q_s ⊔ D`, one edge of each kind per bounded black face. A pair is a 3-orientation (out-degree 3 at nonroots, 0 at roots) in which every bounded black triangle is transitive with sink `u(t)`, hence (`LIT`, cited from memory) a Schnyder wood; its Schnyder colour classes are not `Q_r, Q_s, D`.

`COMPUTED` (T4, `code/`, `data/`):

- Exhaustive census, every rooting, `V <= 17`: 21,848 rooted instances, 13,130 with a pair, 14,881 pair supports, all pack. 42,978 random non-pair maps in instances with a pair, all pack. 9,706 of 27,942 random maps fail in instances without a pair, all at black-inner triangles.
- Referee replay: the folder's 278 nonvacuous cases (43 + 235 of 55 + 370) reproduced exactly; all 27 saved certificates verified with my own `W`.
- Adversarial: the `V = 18` lattice-extreme counterexample, tubes to `V = 70`, `tube6_6`/`tube8_4`/`tube10_3` with 233–300 supports per rooting, a subdivided tube, prism chains, random octahedral sums in faces of both colours: 2,442 supports, no failure; the failure rule of Prop 2.3 matched all 5,440 random maps, so "only if" holds on this sample.
- P2 (two face-rainbow trees) and Theorem 3.3 agree with brute force on all 14,881 supports. A split rainbow for both faces and points (a pair of tree matchings) fails on 239 of 9,290 supports at `V = 17`. One support (V = 16, plantri index 27, my face 0) contains no tree matching at all.

## What failed and why

- The packing route as a route to the key lemma. `REFUTED` as a route, not as a statement: the statement is true for all `3^n` deleted-corner maps, so it cannot select a good pair. Lesson: a statement that survives dropping the bijection is a density statement, and density statements are all equivalent to "no black-inner triangle".
- "Every pair support contains a tree matching": `REFUTED` at `V = 16`. So rounding confined to one support cannot work, and `(r + s)/2` is in the LP but not in the convex hull of tree matchings.
- My prediction 3 put P1 and P2 at 50 percent each. P1 turned out provable; P2 survived but I found no proof. The Edmonds argument does not transfer, because the face constraint pairs two arcs entering a vertex rather than two arcs leaving one.
- I did not test the Schnyder-wood hunch (a pair whose `Q_s` is a Schnyder colour class), and I did not decide whether the target lies in the relative interior of the conditioned degree polytope.

## What is still open

1. The key lemma restated: some 2-factor of `B` has an alternating half that is a spanning tree of `W`. Every one-sided version is now solved inside every 2-factor; the alternation is the whole difficulty.
2. P2 (PROOFS Conj 3.4): every pair support splits into two face-rainbow trees; equivalently `Q_r ∪ Q_s` splits into two transversal spanning trees of `T/R`.
3. Corollary 2.6 without the pair hypothesis (computed true, `V <= 17`).
4. "Only if" in Proposition 2.3 (computed on 5,440 maps).
5. Relative interior of the conditioned degree polytope (REFEREE §3), which decides whether a finite exponential family can match the target mean exactly.

## Three best next steps

1. **Prove P2 or find where it breaks.** It is the face-side twin of a theorem with a two-line count, and it is the `T`-side statement the brief asked about (two transversal forests plus `D`). Search for counterexamples on large supports with a matroid-intersection algorithm instead of brute force; try an Edmonds-type argument on the digraph whose arcs enter `u(t)`.
2. **Start fable's Conjecture X from Theorem 3.3.** Each 2-factor gives a pair of complementary point-rainbow trees in polynomial time. Test whether the exchange walk from one of them ends at a tree matching more often, or faster, than from a random rainbow tree, and whether the complement structure gives a potential.
3. **Record the packing route on the route map as closed**, with the density lesson, and record the mean obstruction with its scope "full-support measures on all of `H`; condition on forced spokes first".

## Leads for others

- The single count (Hall shortfall per black face, at most one per face with two corners in `U`) proves three different matroid statements here. The manuscript could present (3.2) once, extended to all `U`, and derive the pair, the two-tree packing and the rainbow trees from it.
- Theorem 3.3 strengthens fable's Theorem S: the map from rainbow trees to 2-factors is onto, with at least two preimages.
- `W` minus the triangle of `t0` is three spanning trees: a Schnyder-type decomposition of the white-face graph, which might make a figure.

## Protocol

All writes are in this folder. No subagents. One heavy process at a time; the longest run was 4 minutes (`census.py 16 17`). The lab and other folders were read only; the lab was imported only to decode the probabilistic folder's face numbering and to call plantri. Literature results (Nash-Williams 1964, Rado 1942, Edmonds 1973, Schnyder 1989, de Fraysseix–Ossona de Mendez 2001) are cited from memory; I did not open them in this session.
