# Choices for manuscript B

Opus 5.5, 2026-11-14. Folder `research/2026-11-14_opus_manuscript-B/`, manuscript `paper/draft-B/`.

## The one language: the dual triangulation T

I tell the whole proof in `T = G*`, with its faces coloured black and white. Every object of the proof is a set of edges of `T` or a set of corners of its black triangles:

| Object | What it is in T |
| --- | --- |
| Hamiltonian cycle of G avoiding `e` | a set `P` of edges of `T` with one side in every triangle and no cycle, containing `e*` |
| state `s` | one corner in each bounded black triangle, every nonroot used once |
| `Q_s` | the sides opposite the chosen corners |
| `D(r, s)` | the sides from `r(t)` to `s(t)`, directed |
| the white tree | the faces of `T`, joined across the sides not in `Q_s` plus two root sides (a tree whose nodes are triangles) |
| weights | heights: how often the chosen corners' spokes cross a path from a white face to the outer face |
| obstruction | a separating triangle of `T` |

`G` appears in two places only. It is the home of the problem (Section 1), and it is the graph of faces of `T` that the single duality lemma talks about. The spoke graph `H` is never used as a plane graph with faces. Spokes appear only as the drawing of a corner, inside the height function.

### Why T and not the other two

1. **One duality lemma, used twice.** In `T`, the forest-to-tree step and the final step are both the same statement: for a plane graph, a set of edges is acyclic exactly when the dual edges of its complement are connected. The recovery is then: `Q_s` plus two sides of `t0` is a spanning tree of `T`, so the faces of `T` joined across the remaining sides form a tree `Y`; in `Y` each bounded black triangle has degree two and `t0` is a leaf, so rooting `Y` at `t0` forces a unique selection `P`. This replaces the spoke graph `H`, its faces, the white-face tree and the "black dual trace" by one sentence about `T` and its faces. (In H-language the same step needs `H`, `H*`, a second duality and an explanation of why faces of `H` are white triangles.)
2. **All counts are the same count.** The disk identity, the selected-side count that makes `P` acyclic, the density inequality for the first pair, and the cap colour at a separating triangle are all "Euler on a region of `T`, plus count sides by the colour of their face". In `H` the disk identity becomes a hexagon count with "third spokes inside and outside" (Li's Claim 25), which is correct but harder to picture. In `G` the density step is Li's minimal deficient set and 3-edge-cut argument, fine on its own but in a third vocabulary.
3. **Both kinds of cycle live in one graph.** `D` and `Q_s` are both edge sets of `T`, drawn in the same triangle (Figure local). The reader compares the two reversals in one picture.
4. **The target is visible.** "An acyclic set with one side per triangle" can be drawn and checked by eye on the running example, and its two components are the two induced trees of Stein's reformulation.

What I give up. Li's primal language makes the gluing across a 3-edge cut very intuitive ("glue two Hamiltonian cycles"). In `T` the gluing is a short argument about two acyclic selections that share one edge. I keep it in `T` and add one sentence saying what it means in `G`. The spoke graph makes the weights look natural without any detour; in `T` I need one homotopy remark (an edge of `T` and its two-spoke route bound a region inside one black triangle). That remark is two lines once phrased with winding numbers; the "slide preserves simplicity" argument of OpenAI 5.3 is not needed.

## Mathematical route

| Step | Source | Status in the draft |
| --- | --- | --- |
| `T` simple, coloured; counts (2.1) | OpenAI §2, §7 | proved in full |
| duality lemma | OpenAI Lemma 2.1 | proved directly ("boundary of a set of faces has even degrees") |
| acyclic selection ⟹ Hamiltonian cycle | OpenAI §6.2, §7 | proved |
| every acyclic selection comes from a state | route-combinatorics `PROOF.md` §6, astra limits | proved, used as motivation |
| recovery via the face tree `Y` | OpenAI §6.1 rephrased; new phrasing (tree of faces of `T` instead of white tree in `H*`) | proved |
| disk identity as `W = B + 1` | OpenAI Lemma 4.1; form from route-combinatorics `PROOF.md` §1 | proved |
| `P` acyclic: `W - B = 1` against `W - B = 3` | OpenAI Lemma 6.2; short form from `PROOF.md` §5 | proved, checked by me |
| partners orient `Q_s` | OpenAI Lemma 5.2/6.1; trees paper Prop. 2.1 | proved |
| sign `ε = (-1)^{(n+J)/2}` | trees paper (8); OpenAI uses `i^J` | proved |
| cancellation for fixed `s` | OpenAI Lemma 5.2 | proved |
| heights and `ω`; `L(C)` = white faces inside | `PROOF.md` §2.3, referee `REWRITTEN-PROP-5-1.md`; I replace the slide by a homotopy and winding numbers | proved, checked by me |
| nonvanishing via `Σ ε ω^m` and an `m`-fold difference | trees paper Thm 5.2 (polynomial), OpenAI (5.5); finite-difference form new here | proved |
| first pair by flow and density | OpenAI Prop. 3.1 | proved |
| gluing | OpenAI §7 rephrased for selections; Li App. C for the primal reading | proved |

I did not use: the complex phase, the exponential sum, Li's half-rays and involutions, the marked walk, the determinant identities (`PROOF.md` §4, skeleton L1/C1), the exact obstruction criterion (trees paper Thm 1.2). Each is mentioned once with a pointer.

### Why `ω^m` and not a product of heights at chosen faces

`PROOF.md` Theorem B and the referee's rewrite test against `h_s(w_1) ⋯ h_s(w_m)` with `w_i` inside the `i`-th cycle of one minimal cover. I use `ω(s)^m` with `ω` the sum of all heights. The argument is the same `m`-fold difference, the count is `m! Σ_D Π_C L(C)`, and it is the quantity the three published proofs compute (OpenAI (5.5) up to phase, trees Thm 5.2, Li's marks). The reader sees one weight per state, which matches the published papers, and needs no choice of faces.

## Worked example

The shared running example (`paper/figures/running.json`): 13 vertices, 22 triangles, `n = 10`, no separating triangle. COMPUTED by `example.py` (independent of the figure code and the lab), output `example.txt`:

- 12 states, 8 ordered pairs, falling into two cycle covers of 4 pairs each;
- every cover has `m = 2` cycles: a 7-cycle enclosing 6 white triangles with a triangle enclosing 1, and a 7-cycle enclosing 3 with a triangle enclosing 1;
- exactly one second state has cyclic `Q_s` (a triangle on 1, 8, 9); its two partners cancel;
- 6 forest pairs, signs three `+1` and three `-1`;
- `Σ ε ω(s)^2 = 18 = 2! (6·1 + 3·1)`;
- the recovery from every forest pair gives an acyclic selection with two induced trees and a Hamiltonian cycle through the 22 faces.

## Figures

Shared figures used read-only from `paper/figures/` where they are already in `T`-language and carry no notation I do not use: 02 (two 2-factors), 03 (the dual with labels), 07 (pair and `D`), 08 (disk identity), 09 (`Q_s` cycle and forest), 13 (selection and the curve), 14 (gluing). I drew my own where the shared ones carry the exponential-sum notation (`i^J`, `a(t, v)`, `Z(x)`): the local triangle, the cancellation, the heights, the recovery tree `Y`.

## Departures from the outline proposal

- The recovery comes before the cancellation (the outline does this too), but the disk identity is introduced at the recovery, its first use, and reused for the signs.
- The first pair comes after the cancellation. Each section discharges the assumption of the one before: recovery assumes a good state, the cancellation produces one from a pair, the flow produces a pair unless a separating triangle blocks it, the gluing handles separating triangles.
- No exponential sum and no complex numbers.
