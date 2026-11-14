/-
"A forest has at most one perfect matching" (used for the uniqueness of the selection recovered
from a good state: the paper's tree `Y_s` determines `P_s`). Mathlib only.

Proof: the symmetric difference of two perfect matchings has every degree `0` or `2`
(Mathlib's `IsPerfectMatching.symmDiff_isCycles`), so none of its edges is a bridge
(`IsCycles.reachable_deleteEdges`); in an acyclic graph every edge is a bridge; so the symmetric
difference has no edge.
-/
import Mathlib

namespace OAI.Barnette.Devices

open SimpleGraph

variable {V : Type*} [Finite V] {G : SimpleGraph V}

open scoped symmDiff in
/-- An acyclic graph has at most one perfect matching. -/
theorem IsAcyclic.perfectMatching_unique (hG : G.IsAcyclic) {M M' : G.Subgraph}
    (hM : M.IsPerfectMatching) (hM' : M'.IsPerfectMatching) : M = M' := by
  set H := M.spanningCoe ∆ M'.spanningCoe
  have hcyc : H.IsCycles := hM.symmDiff_isCycles hM'
  have hle : H ≤ G := by
    intro v w h
    rcases h with ⟨h, _⟩ | ⟨h, _⟩
    · exact M.adj_sub h
    · exact M'.adj_sub h
  have hHac : H.IsAcyclic := hG.anti hle
  have hbot : H = ⊥ := by
    ext v w
    simp only [bot_adj, iff_false]
    intro hvw
    have hbr := isAcyclic_iff_forall_adj_isBridge.mp hHac hvw
    exact (isBridge_iff.mp hbr) (hcyc.reachable_deleteEdges hvw)
  have hspan : M.spanningCoe = M'.spanningCoe := symmDiff_eq_bot.mp hbot
  ext v
  · rw [hM.2.verts_eq_univ, hM'.2.verts_eq_univ]
  · rename_i w
    have := congrArg (fun K : SimpleGraph V => K.Adj v w) hspan
    simp only [Subgraph.spanningCoe_adj] at this
    rw [this]

end OAI.Barnette.Devices
