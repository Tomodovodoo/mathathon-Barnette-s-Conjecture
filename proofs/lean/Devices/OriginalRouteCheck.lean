import OAI.Combinatorics.Hamiltonian.Main

/-! Control: the same reachability check on the ORIGINAL `OAI.Barnette.main`.
call `Pair.forest_pair_of_disk_circulation` replaced by `Pair.forest_pair_of_disk_circulation_real`). -/

open Lean Elab Command in
/-- `#reaches c [d₁, d₂, ...]`: for each `dᵢ`, whether the constant `dᵢ` occurs in the transitive
closure of the types and values of the constants used by `c`. -/
elab "#reaches " c:ident " [" ds:ident,* "]" : command => do
  let env ← getEnv
  let start := c.getId
  let mut seen : NameSet := {}
  let mut todo : Array Name := #[start]
  while h : todo.size > 0 do
    let n := todo.back
    todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    if let some ci := env.find? n then
      for m in ci.type.getUsedConstants do
        unless seen.contains m do todo := todo.push m
      if let some v := ci.value? (allowOpaque := true) then
        for m in v.getUsedConstants do
          unless seen.contains m do todo := todo.push m
  logInfo m!"{start}: {seen.size} constants in its closure"
  for d in ds.getElems do
    let resolved ← liftCoreM <| realizeGlobalConstNoOverload d
    logInfo m!"  {resolved}: {if seen.contains resolved then "REACHED" else "not reached"}"

#check (OAI.Barnette.main : OAI.Barnette.MainStatement)
#print axioms OAI.Barnette.main

#reaches OAI.Barnette.main [
  OAI.Barnette.TriangleSystem.Pair.forest_pair_of_disk_circulation,
  OAI.Barnette.TriangleSystem.Pair.total_sum_ne_zero,
  OAI.Barnette.common_phase_sum_ne_zero,
  OAI.Barnette.TriangleSystem.OppositeCycle.fixed_second_state_cancels,
  OAI.Barnette.phase,
  OAI.Barnette.TriangleSystem.Pair.term]
