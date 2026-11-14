# Report: referee of the topology route, and the rainbow attack

Fable 5.2, 2026-11-14. Folder `research/2026-11-14_fable_referee-topology/`.

1. Referee: all eight claims of `research/2026-11-14_opus_route-topology/` stand. Seven are CORRECT, one (the Morse reading) is CORRECT AFTER FIX: a sign in the `J` formula, and the roots must be paired in the vector field. Its exact counts (826 with 580 and 246; 442 and 6) are reproduced by independent code.
2. PROVED-HERE: Step R. A point-rainbow spanning tree exists iff no separating triangle has black inner boundary, by Rado's theorem and one exact Euler identity. The Floer-reading theorem of the refereed report no longer depends on the cancellation. The lattice-height conjecture is also proved (signed white area is a winding number).
3. Step X (exchange descent) survives everything I could throw at it: all 34.8 million rainbow trees of all rootings with `V <= 16`, and sampled runs to `V = 120`. It is still a CONJECTURE.
4. PROVED-HERE: each point of a rainbow tree has exactly one exchange, and "evict the resident" is a reversible walk. It gives `n` fixed-point-free involutions on tree matchings, a sign-free reason for their even number. REFUTED: the hope that this walk never cycles. Periodic walks exist at `V = 40`.
5. R plus X would be a counting-free proof of the key lemma. It would not be a polynomial-time algorithm as it stands, because X needs a plateau search and the one deterministic rule I found fails.

## What I set out to do

Part 1 was to referee eight claims of the opus topology run with independent code. Part 2 was to attack its main lead: Step R (a rainbow spanning tree on the white faces exists) and Step X (local exchanges that never increase the black-face excess reach a tree matching).

I wrote a new implementation from the plantri rotation systems (`code/etri.py`, `code/rainbow.py`), about 2,700 lines with the experiment scripts. All numbers below come from it. Commands and run times are in `code/README.md`.

## What I established

### Referee (details and dependency table in `REFEREE.md`)

| Claim | Verdict |
| --- | --- |
| (a) flat angle structure, turning identity, Gauss-Bonnet, disk identity | CORRECT. Two unstated steps supplied: boundary flatness for clockwise cycles, and why the disk meets the hypotheses of Gauss-Bonnet. 6,417 cycles checked from actual corner sums. |
| (b) `W = B + 1` | CORRECT. Agrees with node C4 of the astra combinatorics referee. |
| (c) retraction lemma, `#cycles = 1 + b1(P)` | CORRECT. I give a three-line face-count proof and the standard source, the dual rank formula. 3,300 random perfect matchings checked. |
| (d) cancellation as an acyclic matching, `Z(1) = 0` | CORRECT AFTER FIX. `J = J_ccw - 2·#clockwise`, not `+`. The roots must be paired with their `t0`-spokes. The report's computed evidence only reaches `k <= 1`. |
| (e) Floer reading | CORRECT as a dictionary, checked against JKR Theorem 1.1 (arXiv:1112.2632, fetched). Nothing Floer-theoretic is used or produced. The dependence on barnette_trees Thm 1.2 is removed by Theorem R. |
| (f) rainbow criterion, 826 instances | CORRECT. Reproduced exactly, extended to all 7,868 rootings with `V <= 16`, and proved. |
| (g) mate of a tree matching | CORRECT. 6 of 442 reproduced; 40 of 3,240 over all rootings with `V <= 14`. |
| (h) lattice height equals signed white area | CORRECT. The CONJECTURE part is now PROVED-HERE. |

### New mathematics (statements and proofs in `RAINBOW.md`)

- **Theorem R, PROVED-HERE.** With the exact identity `w(J) - |J| - 1 = (c - 1) + (3d - σ - 12)/6` for every connected set `J` of non-roots. COMPUTED on 57,901 sets and 7,868 rooted instances.
- **Lemma R2, PROVED-HERE.** The black-side (face-rainbow) tree always exists.
- **Lemma X1, PROVED-HERE.** In a rainbow tree every point has exactly one exchange. The move graph is `n`-regular. COMPUTED: connected in all 5,088 instances with `V <= 16`.
- **Lemma X2, PROVED-HERE.** The net surplus of loads inside the fundamental cycle of an exchange equals `W - B - 1 + [old face inside]`. This is the disk identity for rainbow trees. COMPUTED on 102,976 moves.
- **Lemma X3 and Corollary X4, PROVED-HERE.** The surplus walk is reversible. For each bounded black face `t` it defines a fixed-point-free involution `ι_t` on tree matchings. COMPUTED: 107,226 of 107,226 pairs.
- **Height formula, PROVED-HERE** (`REFEREE.md`, claim (h)).

### Evidence for Conjecture X, COMPUTED

Exhaustive over every rainbow tree: `V <= 12` (74,432 trees), `V = 13, 14` (1,327,360), `V = 15` (4,030,720), `V = 16` (29,366,528), all rootings. No trap. The largest plateau distance to a decreasing move is 5. Sampled: `V = 18, 20, 22` (3,786 starts), random `V = 40` to `120` (396 starts), the eleven saved adversarial instances of the graph-theory run (99 starts), and a hunt over 1,753 random instances with `V = 24` to `50`. Every start reached a tree matching without ever increasing the excess.

## What failed, and why

- **X′, "the surplus walk never cycles": REFUTED.** True for all rootings with `V <= 15` (31.7 million walk states) and in samples to `V = 36`. False at `V = 40`: exact periods 60 and 104 at `V = 40`, and 56 to 236 at `V = 50` to `120`. Nine such trees were examined. In each, moves that relocate the empty face lead to a decreasing move within plateau depth 27. Lesson: a proof of X must use both kinds of plateau move. The examples sit on the same instances that broke single-step descent in the graph-theory run.
- **Strict descent: REFUTED at `V = 8`.** 1,684,312 rainbow trees with `V <= 16` have positive excess and no decreasing move.
- **Four candidate potentials** (distance between a loaded and an empty face, in the tree or in `H`, least or summed): each fails on 5 to 7 percent of the rainbow trees with `V <= 12`.
- **"Mean load 1 at every face": REFUTED at `V = 12`.** It holds in 828 of 880 instances with `V <= 14`, exactly those with `2^n` rainbow trees, exactly those where the slot identity `c(t) + a(t) = 2` holds. With M-convexity it would have given a second proof route.
- **I did not find a proof of X.** Lemma X2 is the only place where I see the disk count entering an exchange, and I could not turn it into a monotone quantity.

## What is still open

- Conjecture X.
- Conjecture M: the set of load vectors of rainbow trees is M-convex. COMPUTED for 108 instances with `V <= 12`. If true, the key lemma becomes the Hall-type condition (H) of `RAINBOW.md` §5, a two-matroid statement.
- The smallest periodic surplus walk, somewhere in `17 <= V <= 40`.
- Which rooted instances have exactly `2^n` rainbow trees, and why the three properties of the dichotomy coincide.
- Whether the involutions `ι_t` act transitively on tree matchings. Not tested.
- A citation for `c = 1 + b1(M*)` in exactly that form. I give the dual rank formula as its source, from memory.
- All new COMPUTED claims here are T4, unreviewed. The proofs are T2, unreviewed.

## Three best next steps

1. **Referee Theorem R and Corollary X4, then put them in the paper.** R is short and replaces the conditional statement in the topology report. X4 is a one-paragraph, sign-free proof that tree matchings come in pairs, which the exposition wanted and the mate involution could not give.
2. **Find the smallest periodic surplus walk and read it.** Enumerate walk states for `V = 17` to `24` in C or with a compiled inner loop (Python handles `V = 16` in eight minutes). The first cycle will show what a potential for X must measure. In parallel, test Conjecture X exhaustively at `V = 17, 18` for triangulations without separating triangles (`plantri -bc4`).
3. **Test Conjecture M to destruction, then try to prove (H).** Run full M-convexity on every instance with `V <= 14`. If it survives, compute `ρ(S)` by weighted matroid intersection and look for the Euler count behind `ρ(S) >= |S|`.

## Leads for others

- **Manuscript.** Three short pieces are ready to lift: the face-count proof of `#cycles = 1 + b1(P)` (`REFEREE.md` (c)); the two missing sentences in the Gauss-Bonnet account of the disk identity ((a)); and the corrected sign `J = J_ccw - 2·#clockwise` ((d)).
- **Constructive route.** `rainbow.py` finds a rainbow tree by matroid intersection and then walks it to a tree matching. On the random instances this took 134 exchanges per start on average at `V = 80`, with no pair, weights or marks. It has no proof of termination, and the surplus walk alone can cycle from `V = 40` on, so the plateau search of `exp_cycles.py` is needed as a fallback.
- **Graph-theory route.** The periodic walks occur on your saved instances `ef_fail_40_40`, `deeptrap_50_1`, `alpha_min_fail_60_61`, `alpha_min_fail_100_7` and `alpha_max_fail_120_123`. A common cause with the Hamiltonian `D`-cycles there is a HUNCH worth an hour.
- **Lean route.** Theorem R needs only Rado's theorem and Euler's formula for possibly disconnected plane graphs. The count in Lemma R2 needs neither.

## Files

`REFEREE.md` (verdicts, corrections, dependency table), `RAINBOW.md` (definitions, proofs, evidence, counterexamples), `code/` with `code/README.md` (exact commands), `data/*.json` (each stores its command).
