# Independent environment dependency walk

COMPUTED. IndependentWalker.lean was written for this review without reusing the submitted #reaches implementation. It performs a breadth-first transitive walk from OAI.Barnette.main over every constant in each visited declaration's type and body, including theorem bodies and available opaque bodies. A hash set prevents revisits. It records axioms and missing constants, and emits every reached OAI/Blueprint name with its defining module. It also enumerates all reached Polynomial namespace constants. The two runs use separate Lean processes, so importing the original main cannot shadow the replacement main.

Commands and timings are in BUILD-LOG.md; full command output is original-walk.out and replacement-walk.out; full project-constant walks are original-closure.txt and replacement-closure.txt. The source is reproduced below.

## Results

| Constant | Original main | Replacement main |
| --- | --- | --- |
| `OAI.Barnette.phase` | True | False |
| `OAI.Barnette.TriangleSystem.Pair.term` | True | False |
| `OAI.Barnette.TriangleSystem.Pair.forest_pair_of_disk_circulation` | True | False |
| `OAI.Barnette.TriangleSystem.Pair.total_sum_ne_zero` | True | False |
| `OAI.Barnette.common_phase_sum_ne_zero` | True | False |
| `OAI.Barnette.TriangleSystem.OppositeCycle.fixed_second_state_cancels` | True | False |
| `OAI.Barnette.TriangleSystem.Pair.forest_pair_of_disk_circulation_real` | False | True |
| `OAI.Barnette.TriangleSystem.Pair.realSum_ne_zero` | False | True |
| `OAI.Barnette.TriangleSystem.OppositeCycle.paperSign_reverse` | False | True |
| `OAI.Barnette.TriangleSystem.Pair.sign_orient` | False | True |
| `Blueprint.finite_difference` | False | True |

Original summary:

```
root=OAI.Barnette.main
visited=36722
axioms=#[Classical.choice, Quot.sound, propext]
missing=#[]
Polynomial declarations=297
```

Replacement summary:

```
root=OAI.Barnette.main
visited=36345
axioms=#[Classical.choice, Quot.sound, propext]
missing=#[]
Polynomial declarations=276
```

## Statement and generated-copy identity

Both processes typecheck `(OAI.Barnette.main : OAI.Barnette.MainStatement)`. The MainStatement definition is imported from the exact same unchanged upstream Model module and both runs print it. The source of Main.lean differs only in its import prefix. inspect_sources.py independently diffs every one of the 17 generated files against the checked-out upstream source. generated.diff records every changed line. Sixteen files change only their first-line import from OAI.Combinatorics.Hamiltonian to PaperRoute. Forest.lean adds `import Devices.RealSign` at line 2 and changes the call to forest_pair_of_disk_circulation_real at old line 238, new line 239. Its theorem statement and remaining proof text are unchanged. There are 17 removed lines and 18 added lines in total.

The abstract old/new forest-pair theorem types are also compared directly by #same_type, using structural expression equality in the environment. The result is in replacement-walk.out. Their common explicit inputs are Nonempty Pair, the opposite-cycle delta hypothesis, local real weights and the strict cycle-slope sign hypothesis.

The submitted build still imports PairPhases and PairPolynomials and uses structural definitions declared in those modules. The verified claim is about proof dependencies, not that these entire source files can be deleted without refactoring. In particular group/class definitions and cycleSlope remain in use. The broad assertion “no polynomial lemma anywhere” must be read against the complete Polynomial count above, not just the six targeted constants.

## Walker source

```lean
import Lean
open Lean Elab Command

/-- Independent breadth-first environment walk. Types and all available bodies are followed,
including theorem and opaque bodies. This intentionally does not call the author's walker. -/
elab "#audit_closure " root:ident " to " dest:str : command => do
  let env ← getEnv
  let mut todo := #[root.getId]
  let mut cursor := 0
  let mut seen : Std.HashSet Name := {}
  let mut project : Array String := #[]
  let mut polynomial : Array String := #[]
  let mut axioms : Array String := #[]
  let mut missing : Array String := #[]
  while cursor < todo.size do
    let n := todo[cursor]!
    cursor := cursor + 1
    if seen.contains n then continue
    seen := seen.insert n
    match env.find? n with
    | none => missing := missing.push n.toString
    | some ci =>
      if n.toString.startsWith "OAI." || n.toString.startsWith "Blueprint." then
        let modName := match env.getModuleIdxFor? n with
          | some idx => (env.header.moduleNames[idx.toNat]!).toString
          | none => "<current>"
        project := project.push s!"{n}\t{modName}"
      if n.toString.startsWith "Polynomial." then polynomial := polynomial.push n.toString
      match ci with
      | .axiomInfo _ => axioms := axioms.push n.toString
      | _ => pure ()
      todo := todo ++ ci.type.getUsedConstants
      if let some body := ci.value? (allowOpaque := true) then
        todo := todo ++ body.getUsedConstants
  let lines := #[s!"root={root.getId}", s!"visited={seen.size}",
      s!"axioms={axioms.qsort (· < ·)}", s!"missing={missing}",
      s!"Polynomial declarations={polynomial.size}"] ++ polynomial.qsort (· < ·) ++
      #["Project declarations (name TAB defining module):"] ++ project.qsort (· < ·)
  liftIO <| IO.FS.writeFile dest.getString (String.intercalate "\n" lines.toList ++ "\n")
  logInfo m!"Walk complete: {seen.size} constants, {project.size} project constants, {polynomial.size} Polynomial constants, axioms {axioms}, missing {missing.size}"

elab "#same_type " a:ident " and " b:ident : command => do
  let ca ← getConstInfo a.getId
  let cb ← getConstInfo b.getId
  unless ca.type == cb.type do throwError "Types are not structurally identical"
  logInfo "Types structurally identical (not merely propositionally equivalent)"

elab "#audit_path " root:ident " target " target:ident " to " dest:str : command => do
  let env ← getEnv
  let mut todo := #[root.getId]
  let mut cursor := 0
  let mut parents : Std.HashMap Name (Name × String) := {}
  parents := parents.insert root.getId (root.getId, "root")
  while cursor < todo.size && !(parents.contains target.getId) do
    let n := todo[cursor]!
    cursor := cursor + 1
    if let some ci := env.find? n then
      let mut exprs := #[(ci.type, "type")]
      if let some b := ci.value? (allowOpaque := true) then exprs := exprs.push (b, "body")
      for (e, label) in exprs do
        for child in e.getUsedConstants do
          if !(parents.contains child) then
            parents := parents.insert child (n, label)
            todo := todo.push child
  unless parents.contains target.getId do throwError "Target not reached"
  let mut n := target.getId
  let mut lines := #[n.toString]
  while n != root.getId do
    let (parent, label) := parents[n]!
    lines := lines.push s!"{parent} --{label}--> {n}"
    n := parent
  let result := String.intercalate "\n" lines.reverse.toList ++ "\n"
  liftIO <| IO.FS.writeFile dest.getString result
  logInfo m!"{result}"

```

## Qualification: general polynomial library dependencies remain

REFUTED if read literally: “not reaching any polynomial lemma.” The replacement reaches 276 Polynomial namespace declarations, against 297 in the original. This does not undermine removal of the six named phase/polynomial nonvanishing dependencies, all of which are absent. The following independently traced path runs entirely through the unchanged exact-dual and rank-condition machinery, not through the replaced nonvanishing argument. The command source is PathCheck.lean, its implementation is the #audit_path command above, and the full output is polynomial-path.out.

```
OAI.Barnette.main --body--> OAI.Barnette.PlaneEmbedding.exists_exact_dual
OAI.Barnette.PlaneEmbedding.exists_exact_dual --body--> OAI.Barnette.Network.Duality.graphMinor
OAI.Barnette.Network.Duality.graphMinor --body--> OAI.Barnette.Network.Duality.minor
OAI.Barnette.Network.Duality.minor --body--> OAI.Barnette.Network.range_internal_boundary
OAI.Barnette.Network.range_internal_boundary --body--> commRing_strongRankCondition
commRing_strongRankCondition --body--> CommRing.orzechProperty
CommRing.orzechProperty --body--> is_noetherian_subring_closure
is_noetherian_subring_closure --body--> isNoetherianRing_of_fg
isNoetherianRing_of_fg --body--> MvPolynomial.isNoetherianRing
MvPolynomial.isNoetherianRing --body--> MvPolynomial.isNoetherianRing_fin
MvPolynomial.isNoetherianRing_fin --body--> MvPolynomial.isNoetherianRing_fin._f
MvPolynomial.isNoetherianRing_fin._f --body--> MvPolynomial.finSuccEquiv
MvPolynomial.finSuccEquiv --body--> MvPolynomial.optionEquivLeft
MvPolynomial.optionEquivLeft --body--> Polynomial.aevalTower
Polynomial.aevalTower --body--> Polynomial.eval₂AlgHom
Polynomial.eval₂AlgHom --body--> Polynomial.eval₂RingHom'
Polynomial.eval₂RingHom' --body--> Polynomial.eval₂_add
Polynomial.eval₂_add

```

The reached declarations from the upstream PairPolynomials module are structural: group indices and their equivalences, cycle faces/deltas/slopes, orientation values, and second-state fibers. None is the old polynomial nonvanishing proof.
