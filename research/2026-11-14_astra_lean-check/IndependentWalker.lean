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
