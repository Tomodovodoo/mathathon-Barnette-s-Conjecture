# Report: the Lean formalisation of the OpenAI proof

**Summary.**

1. I built OpenAI's Lean proof locally (Lean 4.34.1, Mathlib `d13f23b7`, 31 files, 8,936 lines). `#print axioms OAI.Barnette.main` gives only `propext`, `Classical.choice`, `Quot.sound`, and the formal statement matches Barnette's conjecture definition by definition (`COMPUTED`).
2. The formal proof never uses faces, rotation systems or the Jordan curve theorem. Planarity becomes Whitney's algebraic duality, obtained from a drawing through grid minors. After that everything is linear algebra and counting on the cubic graph `G`, and the inside of a `T`-cycle is the root-free shore of a bond of `G`.
3. The Lean takes a simpler route than the paper in five places: a polynomial instead of `exp`, one flow on `G` instead of spoke circulations, the H- form (Hamiltonian cycle avoiding any edge) as the induction statement instead of two induced trees, recovery done in `G` with no spoke graph, and no integrality of `J`. Theorem 2.2 is never stated.
4. The paper is shortest where the formalisation is longest. The disk identity is 6% of the paper and 13% of the Lean. The paper never says why the inside of a cycle is a disk with connected sides and no pinch vertex. 29% of the Lean has no counterpart in the paper at all.
5. `COMPUTED` up to 16 vertices (7,868 rooted triangulations): the flow weights give slope `±#white faces inside` on every `D`-cycle and equal the paper's spoke weights up to one global sign. The polynomial `Z` is nonzero with the predicted lowest coefficient, and the four-count disk identity on `G` holds.

## What I set out to do

The brief: use the formal proof as the most explicit dependency graph of the argument. Clone and if possible build the Lean, extract the declaration graph, map every declaration to the paper, find what the paper skips and where the formal and informal proofs differ, check the top-level statement and axioms, and compare the distribution of effort. Deliverables: `LEAN-STRUCTURE.md`, `LEAN-TO-PAPER.md`, the graph files and scripts, `DIFFERENCES.md`, `LESSONS-FOR-EXPOSITION.md` and this report.

## What I established

**Provenance** (`COMPUTED`, git). Repository `https://github.com/openai/math`, read at `4eaee87548250b2682affda7d05d947c05554bae` (29 Oct 2026). The 31 proof files and the challenge have a single commit, `adc7f124` (6 Oct 2026). `git diff fd4aeeb2 HEAD` on them is empty, so cert-machine's replay (10 Oct, commit `fd4aeeb2`) checked exactly these sources. The clone is in `upstream/` and is not committed (`.gitignore`).

**Build and axioms** (`COMPUTED`, `build/`). A minimal Lake project with only Mathlib, at a short path because of the Windows 260-character limit. `lake exe cache get` took 68 s, and `lake build` compiled the 31 files at about 10 s each. Output: `'OAI.Barnette.main' depends on axioms: [propext, Classical.choice, Quot.sound]`. The same holds for the H- theorem, the existence of the dual and Proposition 5.1. A grep finds no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `opaque`, `extern`, `implemented_by`. The definitions block of `Model.lean` is identical to the comparator challenge. This is the first rebuild in the project. The history agent only grepped.

**The statement** (`DIFFERENCES.md` section A). Finite simple graph, `IsRegularOfDegree 3`, `IsBipartite = Colorable 2`, planar as a crossing-free drawing in ℝ² by injective continuous paths, 3-vertex-connected as at least 4 vertices and connected after deleting at most 2, Hamiltonian as a Mathlib `IsHamiltonianCycle` (one cycle, each vertex once). All match the usual statement. I printed the Mathlib definitions after the build (`build/defs.out`).

**The structure** (`LEAN-STRUCTURE.md`, `graph/skeleton.png`, `graph/files.png`). Declaration graph: 697 declarations and 4,097 edges (1,647 ambiguous), extracted by regex. Between 601 and 675 declarations are reachable from `main`, and the uncertainty is stated in the file. There are 22 unreachable declarations. One of them is the paper's own arithmetic for Lemma 4.1 (`disk_count_identity`), formalised and then never used. The skeleton graph has 60 key theorems with their paper counterparts.

**Lean to paper** (`LEAN-TO-PAPER.md`, plus the generated 697-row `graph/lean-to-paper-full.md`). Every numbered statement on the route to Theorem 1.1 has a counterpart, except Theorem 2.2 (replaced by its primal form) and Corollary 7.2 (not formalised).

**Differences** (`DIFFERENCES.md`, 29 numbered items). Highlights:
- (a) one-sentence steps that cost hundreds of lines: "fix a sphere embedding / the sphere dual" (1,078 lines, through thickening, grid cells, minor models, the rectangle dual and minor-closure of duality); the inside of a cycle is a disk (bond, connected shores, no pinch vertex, region Euler, about 500 lines); "`T` is a simple triangulation" (about 540 lines in the proof of Theorem 1.1); the caps after a separating triangle are again Barnette duals (about 430 lines).
- (b) different statements: 3-edge-connected throughout (from 3-vertex-connected at the start); "no separating triangle" is "every 3-edge cut is trivial"; the disk is a vertex set `A` of `G` and the orientation is a sign `c = ±1`; `δ` comes from per-triangle orientations derived from the algebra; the induction statement is the H- form, with no face parameter and no colour exchange; Lemma 5.3 is weaker (positivity only on `D`-cycles), which is exactly what is needed.
- (c) not formalised: Corollary 7.2. Corollary 7.1 exists only for algebraic duals, not restated for drawings.
- (d) `Z(x)` is the polynomial `Σ i^J ∏_t (1 + a(t,s(t)) X)` and the argument takes its lowest coefficient. `J` is never shown to be an integer (`phase n = i^(n div 3)` and only `phase(n±6) = -phase(n)` is needed). `PROVED-HERE` that the replacement is legitimate, and checked formally by the build.
- (e) planarity is Whitney's algebraic duality over ℝ with orientations. No rotation system. This gives a topology-free statement of the disk identity on `G` by four counts, of which only Euler for the disk and the no-pinch clause use planarity (`LESSONS-FOR-EXPOSITION.md` section 2, `PROVED-HERE` algebra, `COMPUTED` check).

**Numerical check of the Lean devices** (`COMPUTED`, `scripts/check_lean_devices.py`, using the route-combinatorics agent's `tri.py` and `rooted.py` read-only). Range: all Eulerian triangulation classes with `6 <= V <= 16`, every choice of `t0`: 297 classes, 7,868 rootings, 24,744 pairs, 60,152 `D`-cycles (`data/check_lean_devices_v16.txt`).
- W1. With the white-charge flow (spanning-tree solution plus random integer circulations around vertices of `T`), every `D`-cycle has slope `±#(white faces inside)`.
- W2. The sign is tied to `δ` on every cycle.
- W3. The paper's spoke weights give exactly the negative of the same slopes. The paper's Lemma 5.3 construction is therefore one solution of the same flow problem, with the opposite orientation convention.
- P1. Exact cancellation on every `s` with cyclic `Q_s` (327 states).
- P2. `Z(X) != 0` on all 5,088 rootings with a pair, with lowest degree `c_min` and lowest coefficient `(-i)^{c_min} Σ ∏ (L+ - L-)`.
- D0-D5. On every `D`-cycle: the cut of the inside is the cycle (a bond), the four counts hold, and no vertex is pinched.

A second run up to `V = 18` with another seed (`data/check_lean_devices_v18_seed2.txt`, W and P checks only, the D checks were added later) is described in its own section below.

**Effort** (`graph/effort.md`, `graph/effort.png`). Paper text lines against Lean lines per section: Sec 3 15% vs 13%, Sec 4 6% vs 13%, Sec 5 26% vs 19%, Sec 6 14% vs 9%, Sec 7 with Thm 1.1 12% vs 14%. No counterpart: algebraic duality 14%, embedding to dual 15%. Conclusion (`LESSONS-FOR-EXPOSITION.md` section 5): spend more words than the paper on the shape of the disk and on why the dual and the caps are simple Eulerian triangulations. Spend fewer on Sections 5 and 6, using the simpler devices.

## What failed and why

- **Building in the repository folder.** The Mathlib cache unpacking and one Mathlib file failed on Windows' 260-character path limit. I moved the build to `E:\lbb` (outside the repository, build artifacts only). The commands and logs are in `build/`.
- **OpenAI's own `lakefile.lean`** requires about twenty unrelated projects. I did not use it. The Barnette files import only Mathlib, so the minimal project builds the same declarations.
- **The Comparator tool** was not run. A textual diff of the definitions stands in for its statement check.
- **graphviz** is not installed. The `.dot` files are written, and the PNGs are drawn with networkx and matplotlib.
- **Dependency extraction** is approximate. Tactic proofs use lemmas through `simp` and `omega` without naming them, and dot notation on local variables can only be resolved by name. My first version missed edges such as `C.delta_eq.trans`. The final version tries every sub-path of a dotted name and reports both an upper (675) and a lower (601) reachability count.

## What is still open

- Whether a human exposition can prove the no-pinch and connected-shore facts for cycles of `T` in a few lines from the sphere picture, or should cite them. The Lean's algebraic proofs (`vertex_flow_circuit`, `Bond.connected_shore`) are short in mathematics but long in Lean.
- The paper's explicit rooting of the white-face tree versus the Lean's Hall argument. I describe in `LESSONS-FOR-EXPOSITION.md` how the paper's construction reads in `G`, but I did not write it out as a full proof.
- I did not test whether the H- induction statement, which is stronger than Theorem 1.1, could be weakened back for an exposition that wants only Hamiltonicity. Audit F11 says the prescribed edge is needed for gluing, so probably not.

## Three best next steps

1. **Write the exposition's Section 4 from `LESSONS-FOR-EXPOSITION.md` section 2.** State the disk identity on `G` with the four counts, and state the two planar inputs (Euler for the disk, no pinch vertex) as a separate lemma with a figure. This is where the paper is thinnest and the Lean is thickest.
2. **Adopt the flow weights and the polynomial `Z` in the exposition's Section 5.** One sentence ("send one unit of flow from the root face to every white face") replaces Lemma 5.3, the spoke graph and the isotopy, and `1 + aX` replaces `exp(xa)`. Both are formally checked and `COMPUTED` here against the paper's weights.
3. **Use the H- statement as the induction hypothesis and do Section 6 in `G`.** The figure: the spanning tree of `G` in which black vertices have degree 2 (root degree 1), seen as a subdivided tree on the white vertices, with the matching read off by rooting.

## Leads for others

- **Route-combinatorics and dimers agents.** The paper's spoke weights are exactly a solution of the flow problem "one unit from the root face to every white face" (W3, up to sign). So `ω(s)` is a height function of that flow. This may connect directly with the "heights `h_s(w)`" in `rooted.py`, `HUNCH`.
- **Constructive-route agent.** The Lean is less constructive than the paper (Hall's theorem in Proposition 3.1 and in the recovery step). For a constructive exposition, keep the paper's explicit rooting and the alternating-cycle split.
- **Dependency-graph agent.** The formalisation confirms audit F1 (no separating triangle is used only for the triangular-face step of Proposition 3.1) and F11 (the gluing needs the prescribed edge). It adds three obligations that the audit accepts silently: connected shores, no pinch vertex, and the duality of the caps (`DIFFERENCES.md` items 4, 13, 24).
- **History agent.** cert-machine's commit `fd4aeeb2` and the current HEAD have identical proof files, and the local rebuild agrees with cert-machine's verdict.

## Files

- `LEAN-STRUCTURE.md`: provenance, file groups, objects, skeleton, extraction method and its approximations.
- `LEAN-TO-PAPER.md`: curated table by paper section; `graph/lean-to-paper-full.md`: all 697 declarations.
- `DIFFERENCES.md`: statement check, axioms, 29 differences.
- `LESSONS-FOR-EXPOSITION.md`: the algebraic view, the disk identity on `G`, simplifications, chapter plan, where to spend words.
- `graph/`: `lean-decls.json`, `lean-decls.dot`, `lean-files.dot`, `files.png`, `skeleton.{dot,json,png}`, `lean-to-paper.json`, `effort.{md,json,png}`.
- `scripts/`: `extract_lean_graph.py`, `map_to_paper.py`, `render_graphs.py`, `statements.py` (prints declaration headers), `check_lean_devices.py`.
- `build/`: `lakefile.toml`, `lake-manifest.json`, `lean-toolchain`, `Axioms.lean`, `axioms.out`, `Defs.lean`, `defs.out`, `build.log`, `README.md`.
- `data/`: outputs of `check_lean_devices.py`.

Commands (from the repository root; `R=research/2026-11-14_opus_lean-formalisation`):
```
python -I $R/scripts/extract_lean_graph.py $R/upstream/openai-math/lean/OAI/Combinatorics/Hamiltonian $R/graph
python $R/scripts/map_to_paper.py $R/graph/lean-decls.json papers/text/OpenAI-Barnette.txt $R/graph
python $R/scripts/render_graphs.py $R/graph
python $R/scripts/check_lean_devices.py 16 1 > $R/data/check_lean_devices_v16.txt
python $R/scripts/check_lean_devices.py 18 2 > $R/data/check_lean_devices_v18_seed2.txt
```
(`-I` is dropped for the last three because matplotlib's dependencies live in the user site-packages.)
