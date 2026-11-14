# Local build of the Lean proof (14 November 2026)

`COMPUTED`. The 31 files of `lean/OAI/Combinatorics/Hamiltonian/` from `openai/math` at commit `4eaee875` (identical to `fd4aeeb2`, the commit cert-machine replayed) build against Mathlib `d13f23b7` with Lean `v4.34.1`, and the main theorem depends only on the three standard axioms.

What I did:

1. Made a minimal Lake project with only Mathlib as a dependency (`lakefile.toml` here), the 31 proof files and the challenge file. OpenAI's own `lakefile.lean` requires about twenty unrelated projects (Carleson, sphere eversion, ...). The Barnette files import only Mathlib, so they are not needed.
2. The project has to sit at a short path (`E:\lbb`). Inside the repository folder, Windows' 260-character path limit broke the Mathlib cache unpacking and the build of one Mathlib file.
3. Commands, run in `E:\lbb`:
   - `lake exe cache get` (Mathlib oleans from the official cache, 68 s)
   - `lake build` (31 project files, about 10 s each, finished 11:46:55; `build.log` is the tail of the output)
   - `lake env lean Axioms.lean > axioms.out`
   - `lake env lean Defs.lean > defs.out` (prints the Mathlib definitions used in the statement)
4. `diff` of the definitions block (`PlaneEmbedding` to `MainStatement`) between `Model.lean` and `ComparatorChallenges/BarnetteHamiltonian.lean`: identical.

Result (`axioms.out`):

```
'OAI.Barnette.main' depends on axioms: [propext, Classical.choice, Quot.sound]
OAI.Barnette.main : OAI.Barnette.MainStatement
```

The same holds for `Duality.connected_complement_matching` (the H- form), `PlaneEmbedding.exists_exact_dual` and `ColoredDual.forest_pair`. No `sorryAx`, no `Lean.ofReduceBool` (which `native_decide` would introduce). A grep of the sources for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `opaque`, `implemented_by`, `extern`, `set_option`, `macro` and `elab` finds nothing. Plain `decide` occurs 29 times, on finite statements about `Fin 3` and `Fin 2`, and the kernel checks those.

I did not run OpenAI's Comparator tool, which also checks that the solution's `MainStatement` is the challenge's `MainStatement`. Here the textual diff stands in for it. The challenge and the solution cannot be imported together, because both declare `OAI.Barnette.main`.
