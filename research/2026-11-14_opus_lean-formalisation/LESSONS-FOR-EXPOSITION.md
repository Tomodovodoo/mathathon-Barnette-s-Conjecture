# What the formal proof teaches the exposition

Summary.
1. The proof uses planarity in exactly one form: the cycle space of `G` is the cut space of `T`, and vice versa. A human exposition can say so on page one and then argue on the cubic graph `G` alone. The disk identity becomes a counting identity for a bond of `G`.
2. Five devices of the paper can be swapped for simpler ones that the Lean already checked. Use a polynomial instead of `exp`. Use one flow on `G` (one unit from the root face to every white face) instead of spoke circulations. Use the H- form as the induction statement instead of two induced trees. Do the whole recovery step in `G` instead of on the spoke graph. Drop the integrality of `J`.
3. The paper is shortest where the Lean is longest: the disk identity (6% of the paper, 13% of the Lean). It never says why the inside of a cycle is a disk, why no vertex is pinched, or why a capped piece is again a simple Eulerian triangulation. An exposition should spend its extra words there.
4. The paper is longest where the Lean found simplifications: Section 5 (26% of the paper, 19% of the Lean) and Section 6 (14% against 9%). An exposition can be shorter there than the paper.
5. `COMPUTED`: on all 7,868 rooted Eulerian triangulations with at most 16 vertices, the flow weights give slope `±#(white faces inside)` on every `D`-cycle, coincide (up to one global sign) with the paper's spoke weights, and make the polynomial `Z(X)` nonzero with the predicted lowest coefficient (`scripts/check_lean_devices.py`, `data/check_lean_devices_v16.txt`).

## 1. The one place planarity enters

In the Lean, `G` and `T` are two oriented graphs on the same edge set `E` with `ker ∂_G = im ∇_T` and `ker ∂_T = im ∇_G` (`DIFFERENCES.md`, items 1 to 4). Every planar fact used later is derived from this:

| Planar fact used by the paper | Algebraic form in the Lean |
| --- | --- |
| faces of `T` are triangles, `T` is simple | the star of a vertex of `G` is a 3-edge flow of `T`. No flow of `T` has support at most 2 (3-edge-connectivity) |
| a simple cycle of `T` has an inside | a circuit of `T` is `±∇_G 1_A`. `A` is the shore without the root, and both shores are connected (bond) |
| Euler for the whole sphere | `|V| + |F| = |E| + 2` from ranks |
| Euler for a disk | the cycle space of the region of `A` has dimension `|A|` |
| a vertex of `T` touching both sides lies on the cycle | the link of a vertex of `T` is a circuit of `G` |
| Lemma 2.1 | a flow of `T` on a forest is zero |
| cutting along a separating triangle | contracting one side of a 3-edge cut of `G`; duality survives minors |

**Suggested opening for the exposition.** "Let `G` be a Barnette graph and `T` its dual. We use one fact about planarity: an edge set of `G` is a cycle space element exactly when it is a cut of `T`, and the other way round." Readers who know Whitney's theorem will accept it at once. Readers who do not can take the sphere picture on trust. Everything after that is counting on `G`.

## 2. A topology-free statement of the disk identity

This is the form the Lean proves (`state_disk_count`, `disk_boundary_imbalance`, `StateDisk.lean`), restated on `G`. `PROVED-HERE` (the algebra below). The Lean checks it formally (`COMPUTED`, build).

**Setting.** `G` is cubic and bipartite, black and white, with dual `T`. The vertices of `G` are the faces of `T`. A *root* is a black vertex `ρ` of `G`. A *state* `r` assigns to each black vertex `b ≠ ρ` of `G` one corner of the triangle `b` of `T` (one of the three faces of `G` around `b`). It is a bijection onto the vertices of `T` that are not corners of `ρ`.

**Lemma (disk identity on `G`).** Let `A` be a set of vertices of `G` with `ρ ∉ A` such that `G[A]` and `G[V - A]` are connected. Suppose the edges of the cut `∂A` form a cycle `v_1 v_2 ... v_h` of `T` in which every edge `v_i v_{i+1}` lies in the black triangle `b` with `r(b) = v_i`. Let `l` be the number of cut edges whose black end lies in `A`. Then `h = 2l + 3`.

**Proof by four counts.** Let `E_A` be the set of edges of `G` with at least one end in `A`, `A_b` the black vertices of `A`, and `U` the set of vertices of `T` lying on some triangle in `A`.
1. Cubic count: `3|A| + h = 2|E_A|`.
2. Colour count (each edge has one black end): `3|A_b| + h = |E_A| + l`.
3. Euler for the disk: `|A| + |U| = |E_A| + 1`.
4. State count: `|A_b| + h = |U| + l`. The vertices in `U` matched to black triangles of `A` number `|A_b|`, the cycle has `h` vertices, and the overlap is the `l` cycle vertices whose outgoing edge has its black triangle inside. Every vertex of `U` is matched to a black triangle in `A` or lies on the cycle (*no pinch vertex*).

From (3) and (4), `|A_b| = |E_A| + 1 - |A| + l - h`. Put this into (2) and use (1): `h = 2l + 3`. ∎

Planarity is used only in (3) and in the no-pinch-vertex clause of (4). Both are statements about a bond of a plane cubic graph. The paper's `B, W, I` never appear. `A` is `B + W`, and `U` is `I + h`.

**Figure suggestion.** One picture with `G` drawn over `T`, the set `A` shaded, the cut `∂A` (= the cycle of `T`) thick, the `l` edges with black end inside marked.

## 3. Ready-made simplifications (all formally checked)

| Paper device | Replacement in the Lean | What the exposition gains |
| --- | --- | --- |
| `Z(x) = Σ i^J exp(x ω(s))`, Taylor coefficient at 0 | `Z(X) = Σ i^J ∏_t (1 + a(t,s(t)) X)` in `ℂ[X]`, lowest coefficient | no analysis. The factor of a cycle is `∏(1 + a_+ X) - ∏(1 + a_- X) = (L+ - L-) X + O(X^2)` by expanding two products |
| Lemma 5.3: spoke graph `H0`, boundary circulations along dual paths, "the spoke curve is simple and counterclockwise" with an isotopy | one flow `α` on `G`: one unit from the root face to every white face. `a(t,v)` = potential of `α` around the black triangle `t` | the slope of a `D`-cycle is `±#(white faces inside)` by summing the flow across the cut. Positivity: the disk identity forbids an all-black disk. No isotopy, no `H0` |
| `J` is an integer by Lemma 4.1 | not needed. `i^J` only has to change sign under a reversal, and `J` changes by 2 | one fewer appeal to Lemma 4.1. Integrality per `D`-cycle is automatic in the product formula |
| Theorem 2.2 (two induced trees, prescribed face and edge) as the induction statement | for every edge `e` of `G`, a perfect matching `P ∋ e` with `G - P` connected | the statement the reader cares about (H-, a Hamiltonian cycle avoiding `e`) is the induction statement. No colour exchange, no face parameter, no Jordan-curve labelling at the end of Section 6 |
| Section 6.1 on the spoke graph `H` and its dual tree on white faces | the complement in `G` of `Q_s` plus two root sides is a spanning tree of `G` in which every black vertex has degree 2, except the root (degree 1) | the white-face tree is visible directly in `G`. Suppress each degree-2 black vertex into an edge between its two white neighbours. The result is a tree on the white vertices, rooted where the root's single edge ends. The paper's "assign each tree edge to its far endpoint" is then an assignment of black vertices to white ones, i.e. a perfect matching of `G` inside the tree. The Lean uses Hall's theorem here; for a human, the paper's explicit rooting is shorter |
| Lemma 6.1 by counting outdegrees per component | add two root sides of `t0` into the third root; outdegree stays at most 1, so every cycle would be directed, and there is none | one principle ("outdegree at most 1, so every cycle is a directed cycle") serves Lemmas 5.2, 6.1 and 6.2. Say it once |
| Lemma 6.2 with a signed face count (6.1) | "a cut of `G` made of matching edges has as many black-inside as white-inside ends", against `h = 2l + 3` | one sentence of counting, after the disk identity in the form of section 2 |
| max-flow min-cut for Proposition 3.1 | Hall's theorem, twice | a matter of taste. Hall is more familiar to graph theorists. The capacity inequality (3.1) is the same |
| Euler per component in (3.4) | one global inequality `|E(T[U])| + 2 <= |U| + #faces of T[U]` | no case split by component size |

The `COMPUTED` check of the flow device (`scripts/check_lean_devices.py`). For every rooted Eulerian triangulation with `6 <= V <= 16` (297 classes, 7,868 choices of `t0`, 60,152 `D`-cycles of 24,744 pairs) I took a spanning-tree solution of the flow plus random integer circulations around the vertices of `T`. On every `D`-cycle, the slope `Σ a(t,head) - a(t,tail)` equals `#(white faces inside)` up to sign. The sign is tied to `δ` (`sign(slope) · δ-sum/3` is the same on every cycle). The slope equals minus the slope of the paper's spoke weights from `rooted.py`. So the paper's spoke weights are one particular solution of the same flow problem, with the opposite orientation convention. The polynomial `Z(X)` with these weights cancels exactly on every `s` with cyclic `Q_s` (327 such `s`). It is nonzero on all 5,088 rootings that have a pair, and its lowest coefficient is `(-i)^{c_min} Σ ∏ (L+ - L-)` as predicted. `data/check_lean_devices_v18_seed2.txt` repeats the run up to 18 vertices with another random seed (see REPORT.md for its status).

## 4. A modular structure the Lean suggests

The Lean proves the cancellation part for an abstract *triangle system*: a set of triangles with labelled corners, two of which share at most one edge (`forest_pair_of_disk_circulation`, `PairPolynomials.lean:423`). The input is two hypotheses:
- (H1) every cycle of `Q_s` that can be reversed has index sum `±3`;
- (H2) there are weights such that every cycle of every `D` has index sum `-3` with positive slope, or `+3` with negative slope.

The conclusion is that some pair has `Q_s` acyclic. This splits the proof into an algebraic part about states, which knows nothing about the plane, and a planar part, which consists of the disk identity plus the flow. A chapter plan in this order:

1. States and pairs of a triangle system. The two reversals. Cancellation and nonvanishing under (H1) and (H2). Pure combinatorics.
2. The disk identity on `G` (section 2 above). This is the only planar input.
3. (H1) and (H2) follow from it, with the flow weights.
4. Proposition 3.1: a pair exists.
5. Recovery in `G`, then the induction over 3-edge cuts.

## 5. Where the exposition should spend more words than the paper

Comparison of the share of the paper's text with the share of the Lean (`graph/effort.md`, `graph/effort.png`):

| Paper section | paper % | Lean % | Lean%/paper% | Advice |
| --- | --- | --- | --- | --- |
| Sec 4, disk identity | 6 | 13 | 2.1 | more words. State and justify "the inside of a cycle is a disk": both sides connected, no pinch vertex, Euler for the disk. These are 500 lines of Lean and zero sentences in the paper |
| Sec 7 and proof of Thm 1.1 | 12 | 14 (plus 29% with no counterpart) | 1.1 | more words on "the dual is a simple triangulation", "3-vertex-connected cubic is 3-edge-connected", "the capped pieces are again Barnette duals" and the cap colouring |
| Sec 3, Prop 3.1 | 15 | 13 | 0.8 | about the same. The global Euler inequality shortens it |
| Sec 5, cancellation | 26 | 19 | 0.7 | fewer words. Use the polynomial and the flow. Drop the isotopy and the integrality of `J` |
| Sec 6, recovery | 14 | 9 | 0.7 | fewer words. Work in `G`, use the H- statement, drop the Jordan labelling |
| Sec 2, plane trees and states | 8 | 3 | 0.3 | Lemma 2.1 is three lines once cycle space = cut space is on the table |

A caveat about the measure. Lean lines count formal friction as well as mathematical content. The Hall gadget in `BMatching.lean` (92 lines) is routine for a human. The 1,078 lines from a drawing to a dual are a standard theorem (planar graphs have duals) that an exposition should cite, not prove. The ratio for Section 4 survives this caveat. The Lean lines there are about the shape of the disk, and the paper is silent about it.

## 6. What the formalisation shows is not needed

- The Jordan curve theorem, and any notion of face or rotation system. Whitney duality is enough, and the Lean gets it from compactness and grid minors.
- Integrality of `J` (DIFFERENCES item 14).
- The exponential function and Taylor expansion (item 16).
- The spoke graphs `H0` and `H`, and the isotopy argument (items 17, 19).
- Theorem 2.2 in induced-tree form, the colour exchange, and the face `t0` as a parameter (items 22, 23).
- The Stein and Alt-Payne-Schmidt-Wood equivalence, in either direction.
- Max-flow min-cut (Hall is used instead).

What it does need, and the paper should say:
- 3-edge-connectivity of `G` (the Lean's working hypothesis from start to end);
- the bond property of a cycle of `T` and the absence of pinch vertices;
- duality of the capped pieces after a 3-edge cut (`Duality.minor`);
- a connected 2-regular graph is one cycle (the last line, 24 Lean lines).
