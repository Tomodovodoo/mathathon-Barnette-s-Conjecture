import Devices.RealSign
open OAI.Barnette OAI.Barnette.TriangleSystem
namespace IndependentWitness

def T : TriangleSystem (Fin 3) (Fin 6) where
  vertex t i := ![(![0,1,3] : Fin 3 → Fin 6), ![1,2,4], ![2,0,5]] t i
  vertex_injective := by decide
  edge_unique := by decide

def X : Set (Fin 6) := {0,1,2}
def r : T.State X := ⟨fun _ => 0, by
  constructor
  · decide
  · apply Set.ext
    change ∀ v : Fin 6, (∃ t : Fin 3, T.vertex t 0 = v) ↔ (v = 0 ∨ v = 1 ∨ v = 2)
    decide⟩
def s : T.State X := ⟨fun _ => 1, by
  constructor
  · decide
  · apply Set.ext
    change ∀ v : Fin 6, (∃ t : Fin 3, T.vertex t 1 = v) ↔ (v = 0 ∨ v = 1 ∨ v = 2)
    decide⟩
def P : T.Pair X := ⟨(r,s), by
  change ∀ t : Fin 3, T.vertex t 0 ≠ T.vertex t 1
  decide⟩
example : Nonempty (T.Pair X) := ⟨P⟩
example : paperSign r s = 1 := by decide
example : paperSign s r = -1 := by decide
example : r ≠ s := by
  intro h
  have hh := congrArg (fun z : T.State X => z.val 0) h
  norm_num [r,s] at hh
#print axioms IndependentWitness.P
end IndependentWitness
