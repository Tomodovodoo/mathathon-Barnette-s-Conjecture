# Report: category theory and the paired-state proof

1. One categorical idea does real work: cut the triangulation along a cycle, record a finite boundary state, glue. The number of Hamiltonian cycles is the linear term of a Temperley-Lieb pairing of two disk vectors (`PROVED-HERE`, `COMPUTED` on 1157 cycles).
2. In that picture O Theorem 2.2 says "every piece with triangular boundary realises all 3 boundary patterns", and the 3-edge-path corollary says the same for quadrilaterals: all 6 patterns allowed by a parity rule occur (Theorem 3, `PROVED-HERE` conditional on O, checked on every 4-cut up to 15 vertices).
3. It stops there. For 5-cycles the realised patterns depend on the piece (`COMPUTED`, witness with 9 vertices). No induction along longer cuts with a uniform boundary condition exists.
4. Trinity gives a symmetric restatement (Hamiltonian cycle = acyclic triangle factor of a second trinity `K`) and shows what the face root is for. Homology, deletion-contraction and Belyi maps give vocabulary only. Two homological shortcuts are `REFUTED` on small examples.
5. No new proof of Barnette's conjecture. Verdict for the paper: one paragraph on boundary states where the separating triangles are treated, one figure of `K`, nothing else.

## What I set out to do

Find out whether a categorical or functorial viewpoint explains the proof or makes its steps compose, along five directions: gluing along cuts, trinity and triality, homology of the signed sum, recursions and operads, Belyi maps. Every functor was to have a source, a target and a consequence tested on small examples.

## What is established

Proofs are in `PROOF.md`, statements with verdicts in `CATEGORICAL.md`, runs in `EXPERIMENTS.md`. Nothing here has been refereed.

| Statement | Status |
| --- | --- |
| Face-proper labellings are 2-factors, with `c0 + c1 - 1` cycles (Lemma 0) | `PROVED-HERE`, `LIT` in substance |
| Gluing formula for the loop polynomial across any cycle (Prop. 1) | `PROVED-HERE`, `COMPUTED` lengths 3 to 6, up to 10 vertices |
| Number of Hamiltonian boundary states is `sum_j C(m,2j) Cat(j)` | `COMPUTED` for `m <= 6` |
| Selection rule: mono boundary edges carry a third of the sign sum (Prop. 2) | `PROVED-HERE`, `COMPUTED` |
| Completeness for 4-cuts (Theorem 3) | `PROVED-HERE` conditional on O Thm 2.2 and Cor. 7.2; one sub-case uses a finite `COMPUTED` check; `COMPUTED` independently up to 15 vertices |
| Completeness fails for 5-cuts and 6-cuts (Prop. 4) | `COMPUTED` up to 13 vertices |
| Hamiltonian cycles with a root on each side are acyclic triangle factors of `K` (Prop. 5) | `PROVED-HERE`, `COMPUTED` |
| States, pairs, tree matchings multiply under insertion into a white face (Prop. 6) | `PROVED-HERE`, `COMPUTED` |
| Every Hamiltonian cycle is selected by a two-root tree matching | `CONJECTURE`, `COMPUTED` up to 12 vertices |
| Every root pair has a two-root tree matching when there is no separating triangle | `CONJECTURE`, `COMPUTED` up to 12 vertices |
| `tau(T) >= tau(T/ac)` for a simple contraction of a degree-4 vertex | `CONJECTURE`, `COMPUTED` on 948 contractions |

## What failed, and why

- **Every root pair has a two-root tree matching.** `REFUTED` with separating triangles (`plantri_12_6`, 51 of 66 pairs). Two roots move the obstruction, they do not remove it.
- **A two-root tree matching gives a Hamiltonian cycle.** `REFUTED` at 8 vertices. O Lemma 6.2 needs all roots on one side of every selected cycle, and a root face guarantees that.
- **The two cube structures form a bicomplex.** `REFUTED`: the two reversals do not commute for 12 of 624 pairs up to 12 vertices.
- **Topological Hall for the complex of partial tree matchings.** `REFUTED` on the octahedron: a two-face subcomplex is disconnected.
- **Theorem 2.2 alone gives the 4-cut patterns.** `REFUTED` in the tested range: one prescribed facial edge forces one pattern of six. The 3-edge-path form is needed.
- **A fullness statement at every cut length.** `REFUTED` at length 5.
- **My own first prediction for 4-cuts** ("no pattern is always achievable") was wrong, and so was my prediction that the contraction inequality would fail.

## What is open

- A hand proof of the last sub-case of Theorem 3 (pieces with the chord `c0 c2`), now a finite enumeration.
- Whether the missing patterns at length 5 obey a finer local rule.
- The three conjectures in the table. The contraction inequality is the one with a possible use: an injection would lift tree matchings along vertex splits.
- The gluing formula for annuli. Same proof, not written and not tested.
- A theorem about triangle factors of 3-coloured Eulerian triangulations.

## Honest overall verdict

Category theory does not explain why the proof works. The heart of the proof, Proposition 5.1, is a planar positivity statement, and none of the five viewpoints touches it: the homological packaging is a restatement, the algebraic structures (operad, monodromy) are blind to it, and the gluing functor starts only after a Hamiltonian cycle exists.

What it does explain is the shape of the theorem. The prescribed edge of Theorem 2.2 is the complete boundary datum of a triangular cut, the two corollaries of O are the fullness statements at cut lengths 3 and 4, and there is no such statement at length 5. That is worth a paragraph and no more. I would not put the words "functor" or "planar algebra" in the paper. I would put the table of boundary patterns.

## Three best next steps

1. Look for the injection behind `tau(T) >= tau(T/ac)`. A local rule that extends a tree matching across a vertex split, checked on the 948 cases, would be a new inductive tool. Start from `code/recursion.py contract`.
2. Decide the two-root conjecture "every Hamiltonian cycle is selected by a two-root tree matching" beyond 12 vertices, and if it holds, find the modified disk identity for cycles that separate the roots. That would say exactly which Hamiltonian cycles the state method can see.
3. Use the 4-cut table in the paper: add to the section on separating triangles a short remark with the three and six patterns, and state Theorem 3 as the reason Corollary 7.2 is natural. Have a referee check the proof of Theorem 3 first.

## Leads for others

- For the exposition agents: the trinity `K` on `V`, `B`, `W` contains `G`, the spoke graph `H` and the selected set `P` in one picture (`CATEGORICAL.md`, Section 2). It may make a better figure for O Section 6 than three separate drawings.
- For the limits agent: Lemma 6.2 with two vertex roots fails at 8 vertices (`data/tworoot_v12.txt`). That is a clean "what breaks" example for the role of the root face.
- For the combinatorics agent: for every single state, reflecting each vertex across the opposite edge of its matched face is acyclic (Tutte's arborescences, checked in `code/trinity.py tutte`). So acyclicity of one natural map is free, and Proposition 5.1 is about a different map.
- For the constructive agent: counts multiply under insertion into white faces, so benchmarks built by repeated insertion are not independent tests.

## Sources not opened

Gorsky, Steiner, Wiederrecht (the equivalence behind O Corollary 7.2), Di Francesco, Golinelli, Guitter (meanders and Temperley-Lieb), Aharoni and Haxell, Meshulam (topological Hall). They are cited from memory as pointers. Theorem 3 depends on the first only through O's Corollary 7.2 as stated in O.
