# Report: manuscript B

Opus 5.5, 2026-11-14. Folder `research/2026-11-14_opus_manuscript-B/`; manuscript `paper/draft-B/barnette.pdf` (16 pages, source `barnette.tex`, `refs.bib`, `figures/`).

## Five-line summary

1. Draft B is a complete, self-contained proof of Barnette's conjecture (with a prescribed avoided edge), told entirely in the dual triangulation `T`: every object is a set of edges or corners of `T`, `G` appears only as the graph of faces in one duality lemma, and the spoke graph `H` is never used as a plane graph.
2. Route: acyclic selection (one side per triangle, no cycle) ⟸ good state, via a tree of faces `Y_s` obtained from `Q_s` plus two root sides by duality; good state ⟸ a pair, via cancellation and the weight `Σ ε ω(s)^m` with heights at white faces; a pair ⟸ no separating triangle (flow + density); separating triangles by gluing.
3. No complex numbers, no exponential sum, no slide lemma: the sign is `ε = (-1)^{(n+J)/2}`, the weights are heights, the slide is replaced by a winding-number homotopy inside black triangles, and nonvanishing is an `m`-fold finite difference.
4. A reverse-Lamport audit of the draft (`AUDIT.md`) from Theorem 1.1 backward gives FOLLOWS; it found and fixed one wording slip in a proof, two terse steps and a numbering collision. All example numbers are `COMPUTED` by an independent script.
5. Compiles with `latexmk -pdf` with no errors, warnings, undefined references or overfull boxes; every page was rendered and inspected.

## What I set out to do

Write manuscript B per the brief: a rigorous exposition of OpenAI's proof in one picture and one language, with a worked example through every step, complete proofs of the obligations the dependency audits flagged, precise credit, figures, a clean build, an audit and an unslop pass. I did not read draft A.

## What I established

| Claim | Status | Where |
| --- | --- | --- |
| The whole proof reads in `T`; choice justified | editorial | `CHOICES.md` |
| Draft B proves Theorem 1.1 (OpenAI's theorem) completely, modulo the primitives P1–P7 listed in `AUDIT.md` | `PROVED-HERE` (exposition of `LIT` OpenAI 2026) | `barnette.tex`, `AUDIT.md` |
| Recovery via the tree of faces: if `Q_s ∪ {ac, bc}` is a spanning tree of `T`, the faces joined across the other edges form a tree `Y_s` with black degrees 2 and leaf `t0`; rooting forces the selection | `PROVED-HERE` (rephrasing of OpenAI §6.1; equals Li's black dual trace plus a leaf) | Lemmas 3.3, 3.4 |
| Heights: reversing a clockwise `D`-cycle raises `h_s(w)` by `[w inside C]`, proved by winding numbers without the slide lemma | `PROVED-HERE`; `COMPUTED` on every clockwise `D`-cycle of all 8 pairs of the example (`example.py`) | Lemma 4.6 |
| Nonvanishing: `Σ ε ω^m = (-1)^{(n-m)/2} m! Σ_D Π_C L(C)` with `L(C)` = white faces inside | `PROVED-HERE`; `COMPUTED` value 18 on the example | Prop. 4.8, Ex. 4.9 |
| Example data: 12 states, 8 pairs, 2 covers with `m = 2` (`L` = 6,1 and 3,1), one cancelling state, 6 good states with signs balanced, 6 recovered Hamiltonian cycles = all cycles avoiding the edge | `COMPUTED` (`python research/2026-11-14_opus_manuscript-B/example.py > example.txt`) | `example.txt` |
| Hexagonal prism: 3 states, 2 good, 4 Hamiltonian cycles avoiding `e0*`; the other two cycles both give one state with no partner | `COMPUTED` (`python .../prism.py > prism.txt`) | `prism.txt` |

Credit in the paper: objects and route from OpenAI; finite signed count idea from Li; the real sign, outdegree description of partners and the rooted-forest target from the constructive paper; the disk identity as `W = B + 1`, the short acyclicity proof, "selections come from states", heights and the finite-difference form from the project's unpublished notes (`research/2026-11-14_fable_route-combinatorics/PROOF.md`, refereed in part by `research/2026-11-14_astra_referee-combinatorics/REWRITTEN-PROP-5-1.md`), each re-checked by me; the direct duality derivation of `Y_s` and the winding-number replacement for the slide are mine.

## What failed or was left out, and why

- The referee folder has no `REFEREE.md` yet, only a rewritten Prop. 5.1 "appears sound". I therefore checked every step of the height argument myself and kept only what I could verify; I used `ω^m` (as in all three papers) rather than the product of heights at chosen faces.
- I removed the claim that the running example is the smallest with both phenomena: it came from another agent's search that I did not repeat.
- Not included: the exact obstruction criterion of the constructive paper (mentioned in one sentence), algorithms, the determinant identities, Li's involutions, Corollary 7.2 of OpenAI.
- Euler's formula on a triangulated disk is used without proving that the disk's graph is connected; `AUDIT.md` F9 classifies this as an accepted primitive.
- Shared figures are included from `paper/figures/` at their natural size; if that folder changes, the draft's figures change with it. Seven of eleven figures are shared; four (local triangle, recovery, cancellation, white faces) are drawn by `figs.py` from the shared layout coordinates. Figure 2 (shared 03) has vertex labels that sit close to edges in places.
- No independent reader has checked the draft. My audit is not independent of the author.

## What is still open

- An outside referee of draft B, in particular of Lemma 4.6 (winding numbers) and Lemma 3.3 (the tree of faces).
- Whether the shared figure set should gain versions of the cancellation and heights figures in the `ε` notation, so both drafts can share them.
- A short proof that the graph of a triangulated disk is connected, if a referee wants F9 discharged in the text.

## Three best next steps

1. Give draft B to a reader who has not seen the three papers and ask, before each section, what question they expect it to answer (the test in `STYLE-GUIDE.md`); fix the places where they cannot.
2. Have the combinatorics referee check Lemma 4.6 and Proposition 4.8 as written in the draft, and the tree-of-faces recovery (Lemmas 3.3–3.4 and Proposition 3.7).
3. Compare drafts A and B section by section on the same example and merge the clearer version of each step; the single-language choice is the main thing to test.

## Leads for others

- The recovery needs no spoke graph: `Q_s ∪ {two root sides}` is a spanning tree of `T` exactly when `s` is good, and then the dual complement is a spanning tree of `G` with all black degrees 2 except a leaf at `t0`. This is the same duality lemma that turns an acyclic selection into a Hamiltonian cycle.
- The slide lemma of OpenAI §5.3 is not needed for the weights: only winding numbers around points of white faces matter, and an edge and its two-spoke route are homotopic inside their closed black triangle, which contains no such point.
- For figure makers: shared figures 10 and 11 carry the `i^J`, `a(t, v)` and `Z(x)` notation; a draft using `ε` and heights needs its own versions (draft B has them in `paper/draft-B/figures/`).
