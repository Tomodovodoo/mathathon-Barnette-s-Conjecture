# Report: dependency graphs of the three Barnette papers

Fable 5.2, 2026-11-14. Folder `research/2026-11-14_fable_dependency-graph/`.

## Five-line summary

1. All three proofs close. OpenAI and the trees paper follow as written. Li's note follows once four unwritten routine steps are supplied (the balance count for Ore's theorem and three verifications in Appendix B).
2. The three papers share one engine and 14 core nodes. They differ in substance at four nodes only: the first pair, the weights, the nonvanishing count, and the last step from `P` to one cycle.
3. "No separating triangle" is used at one node in OpenAI. 3-connectivity is used once, to make the dual simple. The disk identity is used four times in OpenAI and three times in Li, who avoids its last use.
4. New, proved and checked: the OpenAI sum is the multilinear coefficient of one determinant, and the cancellation is the vanishing of a twisted incidence determinant of `Q_s`.
5. New, refuted: there need not be a tree pair among the pairs with the fewest `D`-cycles (counterexample with `n = 15`).

## What I set out to do

Audit each paper backward from its conclusion by the reverse-Lamport method, check every side condition, build a node-by-node dictionary between the three, draw the graphs, and extract the minimal skeleton with leads for other routes.

## What is in the folder

| File | Content |
| --- | --- |
| `audit-openai.md` | boundary, AND/OR graph, 13 findings, 73-row table, verdict |
| `audit-li.md` | the same for Li's note, 12 findings, 60-row table |
| `audit-trees.md` | the same for the trees paper, 10 findings, 58-row table |
| `correspondence.md` | dictionary of objects and lemmas, proofs of the non-obvious translations, list of real differences |
| `skeleton.md` | the 14 core nodes, the variants, essential versus packaging, and for each core edge the papers' argument plus other kinds, tagged |
| `graphs/` | `openai.dot`, `li.dot`, `trees.dot`, `merged.dot`, each rendered to PDF and SVG, and `build_graphs.py`, the single source |
| `scripts/check_nodes.py`, `data/check_nodes.txt` | checks of the nodes on 36 rooted triangulations, `n` from 3 to 23 |

Commands. `python scripts/check_nodes.py > data/check_nodes.txt` (about 4 seconds). `python graphs/build_graphs.py`. Graphviz `dot` was not installed, so the renders come from matplotlib. The DOT files are standard and carry `role`, `classification`, `status` and `layer` on every node.

## What I established

Statuses as in `BRIEF.md`.

**Verdicts.**
- OpenAI, Theorem 1.1 and Corollary 7.1: FOLLOWS. Corollary 7.2 is indeterminate for me because it rests on [5, Theorem 4.16], which I could not open.
- Li, Theorem 3: FOLLOWS, with four steps supplied in the audit. Theorem 10 (Ore) is applied without stating `|B'| = |F'|`. Appendix B (the case `c_min > 1`) does not write out that `ι2` is an involution, that it reverses the sign, or that its fixed set is nonempty. All four are true and routine. Read strictly, the Key Lemma is fully proved in the note only for `c_min = 1`.
- Trees, Theorems 1.1, 1.2, 5.2, 5.3: FOLLOWS. The remarks about the companion's breadth-first and random-walk constructors are outside what I was given.

**Side conditions, checked.** `PROVED-HERE` unless marked.
- "No separating triangle" enters OpenAI only at `P5` (a triangular face of a component of `T[U]` is a face of `T`). Sections 4 to 6 do not use it.
- 3-connectivity enters only through "the dual has no loop or parallel edge". Simplicity then matters in the flow bound (faces of length at least 3, small components) and in the gluing.
- Every use of bijectivity of a state is listed in `audit-openai.md`, F4.
- Orientation conventions are consistent in all three papers. I rechecked the local identity in both cyclic orders, Li's table for `τ`, and Li's Lemma 24. `COMPUTED`: `δ`-sums of all `D`-cycles and `Q_s`-cycles, `J = #cw - #ccw`, and the change of `J` by 2 under both moves, on every pair of every test case.
- The spoke curve: "simple" is immediate (distinct vertices, distinct centres). "Counterclockwise" is where the slide across subdisks is needed, and it holds.
- All Euler counts are correct. `COMPUTED` for (2.1), (4.1), (4.2).

**Dictionary.** `PROVED-HERE`.
- Li's `H` is the shared `B`. Li's `G_FB` is the shared `H`.
- `cw' = -J`, with `τ = (1 + δ)/2`. The three signs agree up to a constant depending on `n`.
- Li's Claim 25 is the disk identity, with `t_in = l`.
- Li's marks are the monomials of the Taylor coefficient of order `c_min`, for the weight "signed number of white-vertex rays crossing the spoke". That weight field is OpenAI's Lemma 5.3 with vertical rays as dual paths. The fixed points of `ι2` count formula (5.5).
- Li's proof of Lemma 9 already yields a separating triangle with black inner boundary. So one direction of the trees criterion is in Li's note unstated.
- Li's Lemma 30 does not use the disk identity or the partner. It reduces to this: the faces inside an innermost cycle form a tree, each has an out-step, so some step is undone, and that puts two faces on one black vertex.
- For a pair, "`Q_s` forest", "cycle-breaking" and "tree matching" coincide. For a single state they do not. `COMPUTED`: 34 of 54 states of one `n = 15` example have `B - s` acyclic and `H - s` not a tree.

**New facts.**
- `PROVED-HERE`, `COMPUTED` (21 cases up to `n = 15`): `Z = [λ_1 ⋯ λ_n] det(Σ_t λ_t W_t)` with `W_t[v, w] = ζ^{δ(v,w)} a(t, w)`, `ζ = e^{iπ/6}`. See `skeleton.md`, L1.
- `PROVED-HERE`, `COMPUTED` (35 cases): for fixed `s`, the sum over mates is `κ det N_s`, a twisted incidence determinant of `Q_s`, which vanishes exactly when `Q_s` has a cycle. See C1.
- `PROVED-HERE`: `J` is an integer by the vertex 3-colouring alone, since `δ(v, w) ≡ c(w) - c(v) mod 3`. The disk identity then says the colouring map has degree `-1` on the disk of a state cycle. See B0.
- `PROVED-HERE`: every separating triangle has exactly one black side, and condition (iii) of the trees paper says `t0` lies on the black side of each. `COMPUTED`: one triangulation has 0 pairs or 4 pairs depending on the side.
- `COMPUTED`, all 36 cases: number of states equals `|det K_B|`, common permutation sign, mates number `2^k`, tree matching if and only if one mate, a tree pair in every exchange component with balanced signs, and the recovery gives two induced trees for every tree matching and every root edge.

## What failed and why

- `REFUTED`: "some tree pair has the minimum number of `D`-cycles". In the octahedron with every face split in four, the 4 one-cycle pairs all have a cycle in `Q_s` and the 12 tree pairs all have three cycles. So an extremal proof that first minimises the cycle count cannot work.
- My first test families (double wheels, barycentric subdivisions, random vertex splits) had almost no pairs and none with a cyclic `Q_s`, so the cancellation checks were vacuous. Degree-4 vertices force both of their incidences into every 2-factor. Splitting each face in four fixed this. Anyone testing these lemmas should avoid triangulations with many degree-4 vertices.
- I found no error in any paper. Looking for one took most of the time, and the result is negative.

## What is still open

- I did not open Ore 1957, Gorsky-Steiner-Wiederrecht, Kasteleyn, Kenyon-Propp-Wilson or the mixed-discriminant literature. Every reference to them in my files is from memory and marked as such.
- I did not look at the figures of any paper. I opened two PDF pages (OpenAI p. 4, trees p. 6) to confirm formulas. Everything else comes from the text dumps with formulas re-derived.
- Li's weights were matched to OpenAI's by proof, not by computation, because the script has no coordinates.
- The checks stop at `n = 23` and use few triangulations with many pairs.
- The leads in `skeleton.md` are untested apart from D2.

## Three best next steps

1. Test A2: does every Hamiltonian cycle avoiding `e0` come from a tree matching when there is no black-inner separating triangle? Enumerate cycles on small Barnette graphs and compare with the image of `recover` in the script.
2. Work L1 and C1 into a determinantal proof. The target is to show directly that `Σ_s det N_s Π_t a(t, s(t))` is not the zero polynomial, by mixed-discriminant or matrix-pencil methods.
3. Test G2: with three roots of three colours that are not the corners of a face, does the black-inner obstruction disappear? If yes, the induction over separating triangles can leave the exposition.

## Leads for others

- For the exposition agents. The proof reads better on spokes than on edges of `T`: the slide lemma disappears, and the disk identity becomes "a closed alternating spoke cycle has three more third edges outside than inside". The partner `r` should be introduced as the orientation of `Q_s`. The hypothesis should be the black-side condition from the start.
- For the figures agent. The `n = 15` example (octahedron, each face split in four) is the smallest I found with cyclic `Q_s`, three `D`-cycles and one exchange component. It shows every phenomenon.
- For the machinery agent. `COMPUTED`: the number of states of a barycentric subdivision equals the number of spanning trees of the base map (16 for `K4`, 384 for the octahedron, `m` for an `m`-cycle), as Tutte's trinity predicts. The hexagonal faces of `H` are Kasteleyn's condition.
