import Devices.RealSign
open OAI.Barnette OAI.Barnette.TriangleSystem
namespace IndependentWitness
-- Three nonroot vertices and three root vertices, with the octahedron's three inner black faces.
def T : TriangleSystem (Fin 3) (Fin 6) where
  vertex t i := ![(![0,1,3] : Fin 3 → Fin 6), ![1,2,4], ![2,0,5]] t i
  vertex_injective := by decide
  edge_unique := by decide

def X : Set (Fin 6) := {0,1,2}
def r : T.State X := ⟨fun _ => 0, by decide⟩
def s : T.State X := ⟨fun _ => 1, by decide⟩
def P : T.Pair X := ⟨(r,s), by decide⟩
example : Nonempty (T.Pair X) := ⟨P⟩
example : paperSign r s = 1 := by decide
example : paperSign s r = -1 := by decide
example : r ≠ s := by decide
#print axioms IndependentWitness.P
end IndependentWitness
