# Report: digestions of the proof, step by step

1. Eleven documents are in `digestions/steps/`: an overview with a dependency diagram, nine step files and a glossary, about 23,000 words in all.
2. `COMPUTED`: every number in them comes from `code/examples.py`, an independent model of the proof objects, and agrees with `workings/barnette_lab` on states, pairs, tree matchings and the signed polynomial for the cube, the prism and the 13-vertex running example.
3. Each non-published claim carries its review status in plain words. The statuses of the structure and limits reports were taken from `research/2026-11-14_sol_referee-structure/INTEGRATION.md`, whose final `REPORT.md` did not exist yet.
4. `PROVED-HERE`: nothing new. Two proofs are restated with small repairs that I checked, and one worked example exhibits both expansions of the signed polynomial with the cancellation between two cycle covers visible term by term.
5. Open: no human has read any of it, step 06 runs longer than the five pages asked for, and Li's multi-mark involutions are described but not run on the worked example.

## What I set out to do

Write one self-contained explanatory document for each major step of the proof, for a reader who knows basic graph theory. Each file opens with what is wanted and why, gives the idea in plain words, the precise statement, a proof with every assumption named, a worked example with computed numbers, what does not work with the smallest counterexamples, other routes with their status, and where the step is used next. Mark the review status of everything that is not in one of the three papers.

## What I established

### Documents

| File | Content |
| --- | --- |
| `digestions/steps/00-overview.md` | the proof in ten sentences, a Mermaid dependency diagram, the examples, the status vocabulary |
| `01-degree-two-and-connectivity.md` | 2-factors as complements of perfect matchings, the nine 2-factors of the cube, the four hypotheses as a knife edge |
| `02-dual-and-two-trees.md` | the dual and why it is simple, the counts, tree/cotree duality, Stein's two induced trees with a full proof |
| `03-states-and-pairs.md` | why a Hamiltonian cycle leaves a state behind, tree matchings, the three jobs of the partner, the pair criterion through the Euler identity |
| `04-disk-identity.md` | both forms, the three counts, where bijectivity enters, what parity buys and what the value 3 buys, three readings |
| `05-cancellation.md` | the real sign, the reversal of a cycle of `Q_s` with parity only, the two families of cubes, the incidence determinant |
| `06-nonvanishing.md` | one polynomial with two expansions, the five arguments side by side, the heights proof in full, the running example computed by four methods, the 16-vertex example, the table of failed canonical choices |
| `07-recovery.md` | the six links, both worked examples, which Hamiltonian cycles are produced |
| `08-gluing-and-hypotheses.md` | the induction, a computed gluing at a root with no pair, why the prescribed edge is needed, a table of every hypothesis with its first use and smallest failure |
| `09-what-is-still-open.md` | algorithms and complexity, the three-matroid remark with the referee's verdict on each claim, counting conjectures, the lattice-extreme conjecture, formal verification |
| `GLOSSARY.md` | every term and symbol with its name in each of the three papers |

### Computations

All `COMPUTED`. Commands, from the repository root:

```
python research/2026-11-14_fable_digestions/code/examples.py      # writes data/examples.json and data/examples.log
python research/2026-11-14_fable_digestions/code/crosscheck.py    # writes data/crosscheck.json
python research/2026-11-14_fable_digestions/code/audit_docs.py    # style and link audit of digestions/steps
```

`code/dig.py` is a model of the proof objects that takes oriented face lists and shares no code with the lab. It fixes the orientation conventions explicitly, which the lab leaves to the planarity routine. Range and results:

- Cube: 9 two-factors, 6 Hamiltonian and 3 with two cycles. 2 states, 2 pairs, 2 tree matchings, one cycle cover.
- Hexagonal prism: 20 two-factors (8, 10, 2 with one, two, three cycles). 3 states, 2 pairs, 2 tree matchings. The third state has a forest `Q_s` with root counts 2, 1, 0. For `e0 = 01` there are 4 Hamiltonian cycles avoiding its dual and 2 tree matchings.
- Running example (`paper/figures/running.json`): 112 two-factors, 28 Hamiltonian. 12 states, 8 pairs, 7 states with a partner, 6 tree matchings, two cycle covers with two cycles each. The signed polynomial is `z^-4 - z^-3 + z^-2 - z^-1 - z + z^3`, and `F(1 + xa) = 9x^2 + 5x^3`. The disk identity, `B = I + l`, the sign formula `eps = (-1)^((n+J)/2)` and the height lemma are asserted on every cycle of every pair.
- Double octahedron, all 14 roots: 8 have four pairs, 6 have none, in agreement with the black inner boundary test at every root.
- The 12-vertex example of `fable_route-combinatorics`: the state of largest rank among the partnered ones is not a tree matching, and on the mirror image the state of smallest rank is not. This confirms the referee's correction about reflections.
- The 16-vertex example: three covers, the one with a single 13-cycle has no forest pair in either orientation, the 12 tree matchings lie in the other two.
- The non-bijective 9-vertex example of `astra_limits`: `B = W = 2`, `I = 1`, `l = 2`, `h = 4`, delta-sum 0.
- Gluing at the root `(0,1,5)` of the double octahedron, which has no pair: classes `{2,3,5,8}` and `{0,1,4,6,7}`, both induce trees, the cycle passes through all 14 faces and avoids the dual of `e0`.
- Agreement with the lab on the first three instances, including the six coefficients of the polynomial up to a shift of the exponent by 5.

### Small mathematical points worth recording

- `PROVED-HERE` (two lines, in `05-cancellation.md`): the product of the local signs `delta(r(t), s(t))` equals `(-1)^((n+J)/2)`, the sign of the trees paper. `SIGNIFICANCE.md` section 2 writes the sign of a cover as `(-1)^((n-c)/2)` for its all-counterclockwise orientation, which is consistent, and my script asserts both on every pair.
- `COMPUTED`: in the running example the state with a cyclic `Q_s` has one partner in each of the two cycle covers. So the cancellation of Lemma 5.2 is at the same time a cancellation between covers, and it is visible as the terms `-z^2` and `+z^2`. This makes the running example a complete illustration of step 06, which the figures use only for step 05.
- `COMPUTED`: in the 16-vertex example `c_min = 1` and the unique cover with one cycle is the cover with no forest pair. So the cover that makes the lowest coefficient non-zero contains no solution. `ROUTES.md` records the example under "every cover contains a forest pair" and does not draw this second lesson.
- In `08-gluing-and-hypotheses.md` the failure of the four-edge path property on the cube is given a label-free proof: two vertices at distance two have a second common neighbour, which is left with one usable edge.

## What failed and why

- The first version of my sign check asserted `eps = (-1)^((n-J)/2)`. It failed on the cube. The product of local signs has `(n - 3J)/2` factors `-1`, which gives `(n+J)/2`. Kept in the report because the two exponents differ by `J`, which has the parity of `n`, and it is easy to get wrong.
- I did not run Li's involutions on the running example. `06-nonvanishing.md` says so. The lab has them and the determinant referee did not review that part.
- Step 06 is about 3,900 words. I kept it whole because the side-by-side table, the full proof and the fully computed example belong together.
- The colouring of vertices by three colours is used only as a remark, and I did not write its proof in the digestions. They point to `SIGNIFICANCE.md` section 3.
- I did not render new figures. The documents link to `paper/figures/renders/`, which another agent is still changing. If a file is renamed there, `code/audit_docs.py` reports the broken link.

## What is still open

- A human reading of everything. The digestions repeat the review status of their sources and add none.
- `research/2026-11-14_sol_referee-structure/REPORT.md` was still a work log when I finished. I used the referee's `INTEGRATION.md`. If the final report changes a verdict, the status sentences in steps 03, 07, 08 and 09 need the same change. They are easy to find, each names that folder.
- Three statements are marked "not yet refereed" because the integration notes do not list them: the 26-vertex computation with no pair at any root, the torus example, and the non-bijective disk example. I recomputed the last one.
- The glossary takes the translation of Li's notation from `fable_dependency-graph/correspondence.md`, which is unrefereed. I checked the entries I used in proofs, not all of them.

## Three best next steps

1. Have one person read `06-nonvanishing.md` against `REWRITTEN-PROP-5-1.md` and `SIGNIFICANCE.md` section 2. It is the step where the project's simplifications replace the published argument, and it has only been read by models.
2. Add two figures that the digestions describe in words only: the two covers of the running example side by side with the shared state `s*`, and the 16-vertex example with its 13-cycle and the two triangles of `Q_s`.
3. Run Li's multi-mark involutions on the running example with the lab and add the fixed points to the worked example of step 06, so that all five versions are computed on the same instance.

## Leads for others

- Manuscript writers: the running example has `c_min = 2`, six tree matchings and a signed polynomial with six terms. It refutes "tree matchings come in cubes of dimension `c_min`" and shows the cancellation between covers. One figure could carry both.
- Figures: `code/dig.py` computes the white faces inside every cycle and the heights for explicit paths. For the pair drawn in the figures it gives 6 and 1, the `W` labels of figure 11. The other cover has 3 and 1.
- Dependency graph: the table "what odd buys and what three buys" in step 04 has five rows, not four. The fifth is the white face inside each cycle, which is the positivity of step 06.
- Lab maintainers: `Instance` takes its orientation from `networkx.check_planarity`. For statements that depend on orientation, such as the extremal counterexamples, a constructor from oriented face lists would remove the ambiguity that the combinatorics referee ran into.
