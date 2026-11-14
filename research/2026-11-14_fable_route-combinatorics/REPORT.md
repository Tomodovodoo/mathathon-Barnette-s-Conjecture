# Report: combinatorial routes to the forest pair

Five-line summary.

1. Proposition 5.1 has a weight-free proof: test the signed sum against a product of `cmin` heights at white faces. `PROOF.md` writes it in full, with the disk identity restated as "a state cycle encloses one more white face than black faces".
2. The sign `i^J` is the Leibniz sign of an incidence determinant. For fixed `s` the partner sum is `det` of the incidence matrix of `Q_s`, after a gauge by the vertex 3-colouring. `J` is clockwise minus counterclockwise cycles, which is the colour winding of `D`.
3. Every canonical choice I tried fails: highest or lowest partnered state, minimal cycle cover with all cycles one way, largest rank difference, "every cycle cover contains a forest pair". Counterexamples at 12, 13, 14 and 16 vertices.
4. New and proved: a Hamiltonian cycle avoiding `e0*` defines a state, and that state is a tree matching or has no partner at all. Tree matchings number at least `2 cmin`. Conjecture, true up to 16 vertices: at least `2^cmin`.
5. A lab in `lab/` checks all of this on the 7868 rooted Eulerian triangulations with at most 16 vertices. No determinant or parity argument replaced the planar positivity step.

## What I set out to do

Find combinatorial proof routes for Proposition 5.1 of the OpenAI paper (a pair of disjoint states implies a pair `(r, s)` with `Q_s` a forest), test sharp conjectures by computer, look for a canonical forest pair, say what `J` and the disk identity mean, and write the best route in full.

## What I established

Statuses as in `research/BRIEF.md`. Details and proofs are in `PROOF.md`, the list of routes in `ROUTES.md`, the numbers in `DATA.md`.

| Claim | Status | Where |
| --- | --- | --- |
| Disk identity in the form `W = B + 1` and `(h - l) - l = 3` | `PROVED-HERE` (`LIT`: OpenAI Lemma 4.1) | PROOF 1 |
| `J(r, s)` = clockwise minus counterclockwise cycles of `D` = total colour winding = minus the turning number | `PROVED-HERE`, given the vertex 3-colouring (`LIT`, source not opened) | PROOF 1 |
| The spoke weights are a height function: `omega(s)` is the volume under the height of `s`, and `L+(C) - L-(C)` is the number of white faces inside `C` | `PROVED-HERE`, `COMPUTED` (`lab/analyze.py`, up to 12 vertices by independent flood fill) | PROOF 2.3 |
| Theorem B: the signed sum over tree matchings of a product of `j` heights is `0` for `j < cmin` and a signed count of minimal cycle covers for `j = cmin` | `PROVED-HERE`, `COMPUTED` (`lab/dets.py 12`, D4) | PROOF 3 |
| Proposition 5.1 follows with no weights | `PROVED-HERE` | PROOF 3 |
| Partner sum for fixed `s` equals `sigma det N_s`, and `N_s` is the incidence matrix of `Q_s` up to unit scalings | `PROVED-HERE`, `COMPUTED` (`lab/dets.py 12`, D1) | PROOF 4 |
| The whole sum is the multilinear coefficient of a Hermitian adjacency determinant, and has a Fourier expansion over subsets of `A` | `PROVED-HERE`, `COMPUTED` (D2, D3) | PROOF 4 |
| Lemma 6.2 from `W - B = 1` against `W - B = 3` | `PROVED-HERE` (`LIT`: OpenAI Lemma 6.2) | PROOF 5 |
| A Hamiltonian cycle avoiding `e0*` gives a state; it is a tree matching or has no partner; tree matchings inject into such cycles; `3 #TM <= #HC(G)` | `PROVED-HERE`, `COMPUTED` (`lab/survey.py 16`, E8) | PROOF 6 |
| `#TM >= 2 cmin`; the two signs are equally frequent | `PROVED-HERE` | PROOF 3 |
| `#TM >= 2^cmin` | `CONJECTURE`, `COMPUTED` up to 16 vertices | ROUTES 11 |
| "s is a tree matching iff it has exactly one partner" (trees paper, Theorem 1.2) | `LIT`, `COMPUTED` on 140358 states by brute force over all states (`lab/extra2.py 16`) | DATA |

Nothing here has been refereed.

## What failed and why

| Attempt | Outcome | Lesson |
| --- | --- | --- |
| Highest (lowest) partnered state is a tree matching | `REFUTED` at 12 (14) vertices | Reversing a cycle of `Q_s` changes the number of cycles of `D` by two, and extremality of `s` does not forbid it |
| Minimal `D` with all cycles counterclockwise (clockwise) | `REFUTED` at 12 (13) vertices | The leading coefficient is a sum over all minimal `D` and prefers no orientation |
| Pair with largest `omega(s) - omega(r)` | `REFUTED` at 12 vertices | It forces the cycles of `Q_s` to be counterclockwise, no more |
| Every cycle cover `D` has an orientation that is a forest pair | `REFUTED` at 16 vertices, one case in 5088 | No proof can work inside one `D`. The cancellation across cycle covers is needed |
| Tree matchings split into cubes of dimension `cmin` | `REFUTED` at 14 vertices | `Z(q)/(q-1)^cmin` can have mixed signs |
| Sign of a tree matching is the parity of its rank | `REFUTED` at 8 vertices | |
| A parity or mod `p` count with no weights | no existence proof | The unweighted signed count is `0 = 0`. Weights must depend on `s` only, and the first degree at which anything survives is `cmin` |
| Nonvanishing from the determinant formulas | not obtained | The blocks are indefinite, so the mixed discriminant is an alternating sum of squares |
| One cycle always suffices | `REFUTED` at 9 vertices | `cmin` reaches 3 without separating triangles and 4 with them |

## What is still open

1. `#TM >= 2^cmin`. A proof would probably show a structure on tree matchings that the signed sum does not see.
2. A proof of nonvanishing that does not minimise over the number of cycles. The minimum is forced by the alternation of the leading sign with `c` modulo 4. Is there a test function for which all cycle covers contribute with one sign?
3. A direct description of the Hamiltonian cycles whose state has a partner (Proposition 7), without states. That would turn Proposition 5.1 into a statement about `G` alone.
4. Whether the generation in `lab/tri.py` is complete. The class counts match the published ones as I remember them. I did not open a source.
5. The proofs in `PROOF.md` Sections 3 and 6 need an independent reader.

## Three best next steps

1. Referee `PROOF.md` Sections 1 to 3 and, if they hold, use them as the core of the exposition: disk identity as `W = B + 1`, two families of cubes, heights. It removes the exponential sum, the circulation lemma and the token bookkeeping, and the figure is a cycle with white faces inside.
2. Attack `#TM >= 2^cmin` and the structure behind it. Start from the 479 cases where the count exceeds `2^cmin` (`data/rows_v16.json`) and from the counterexample to the cube decomposition at 14 vertices.
3. Work out the trinity side. The number of states is a number of arborescences, and Proposition 5 says that a tree matching is a state whose `Q_s` is a rooted spanning forest. A bijection that carries states to arborescences should carry pairs and tree matchings to something recognisable, and might give the canonical choice that the extremal principles failed to give.

## Leads for others

- For the dependency graph: Lemma 6.1 of the trees paper (all states have one sign) is the only place where the determinant view needs the disk identity. Lemma 5.2 of the OpenAI paper then follows from linear algebra and the 3-colouring.
- For the figures: the picture for the disk identity is a directed cycle with `B` black and `B + 1` white triangles inside. The picture for nonvanishing is a white face inside a cycle and a path from it to the outer face.
- For the constructive route: Proposition 7 gives a test. A returned Hamiltonian cycle `C` should satisfy "`s_C` has a partner". The reference implementation can cross-check the totals in `DATA.md` (140358 states, 24744 pairs, 24090 tree matchings up to 16 vertices).
- For the literature agents: please confirm the class counts `1, 0, 1, 1, 2, 2, 8, 8, 32, 57, 185, 466` for 3-connected cubic bipartite planar graphs on 8 to 30 vertices, the two generating operations for Eulerian triangulations, and the attribution of the 3-colour theorem.

## Files

- `PROOF.md`: the full argument and the status table.
- `ROUTES.md`: thirteen routes with status, evidence and lesson.
- `DATA.md`: tables and tallies.
- `lab/`: code and `lab/README.md` with the commands.
- `data/`: raw outputs, including `counterexamples.txt`.
