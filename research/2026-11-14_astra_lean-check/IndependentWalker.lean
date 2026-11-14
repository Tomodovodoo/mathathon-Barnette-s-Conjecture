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
