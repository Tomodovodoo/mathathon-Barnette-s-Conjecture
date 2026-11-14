/-
Lemma 3.7 of paper/main/barnette.tex (outdegree), the component count, for a connected graph
(a component of the paper's `F`). Mathlib only.

Paper: "Let F be a set of edges of T, each directed, such that every vertex has at most one
outgoing edge in F. [...] A component of F with q vertices, of which γ have no outgoing edge, has
q - γ edges; so γ ≤ 1, the component is a tree if γ = 1, and it contains exactly one cycle if
γ = 0."

Model: a simple graph `G` on a finite type (the component), and `out : V → Option V` giving the
head of the outgoing edge of each vertex (`none` for a vertex without one). Every edge of `G` is
directed one way, so `out v = some w` and `out w = some v` never hold together.
"Exactly one cycle" is stated as: `G` is not acyclic, and deleting any edge that is not a bridge
leaves a tree (so every cycle of `G` uses every non-bridge edge, hence there is only one).
Not formalised here: the first claim of Lemma 3.7, that every cycle of `F` is directed.
-/
import Mathlib

namespace OAI.Barnette.Devices

open SimpleGraph

variable {V : Type*} (G : SimpleGraph V)

/-- A direction on every edge of `G` with outdegree at most one at every vertex. -/
structure OutOrientation where
  out : V → Option V
  out_adj : ∀ v w, out v = some w → G.Adj v w
  covers : ∀ v w, G.Adj v w → out v = some w ∨ out w = some v
  one_way : ∀ v w, out v = some w → out w ≠ some v

namespace OutOrientation

variable {G} (o : OutOrientation G)

/-- The edge leaving a vertex that has one. -/
def tailEdge (v : {v : V // o.out v ≠ none}) : G.edgeSet :=
  ⟨s(v.val, (o.out v.val).get (Option.isSome_iff_ne_none.mpr v.property)),
    o.out_adj _ _ (Option.some_get _).symm⟩

theorem tailEdge_bijective : Function.Bijective o.tailEdge := by
  constructor
  · rintro ⟨v, hv⟩ ⟨w, hw⟩ h
    have h' := congrArg Subtype.val h
    simp only [tailEdge, Sym2.eq_iff] at h'
    rcases h' with ⟨h1, _⟩ | ⟨h1, h2⟩
    · exact Subtype.ext h1
    · exfalso
      have hv' : o.out v = some w := by
        rw [← h2]; exact (Option.some_get _).symm
      have hw' : o.out w = some v := by
        conv_rhs => rw [h1]
        exact (Option.some_get _).symm
      exact o.one_way v w hv' hw'
  · rintro ⟨e, he⟩
    induction e using Sym2.ind with
    | h v w =>
      rcases o.covers v w he with h | h
      · refine ⟨⟨v, by rw [h]; exact Option.some_ne_none w⟩, Subtype.ext ?_⟩
        simp only [tailEdge, h, Option.get_some]
      · refine ⟨⟨w, by rw [h]; exact Option.some_ne_none v⟩, Subtype.ext ?_⟩
        simp only [tailEdge, h, Option.get_some, Sym2.eq_swap]

/-- Edges are counted by their tails: `|E| = q - γ`. -/
theorem card_edgeSet_add_sinks [Finite V] :
    Nat.card G.edgeSet + Nat.card {v : V // o.out v = none} = Nat.card V := by
  have := Fintype.ofFinite V
  classical
  rw [← Nat.card_eq_of_bijective _ o.tailEdge_bijective, Nat.card_eq_fintype_card,
    Nat.card_eq_fintype_card, Nat.card_eq_fintype_card, add_comm]
  have h := Fintype.card_subtype_compl (fun v : V => o.out v = none)
  have hle := Fintype.card_subtype_le (fun v : V => o.out v = none)
  have heq : Fintype.card {v // o.out v ≠ none} = Fintype.card {v // ¬o.out v = none} :=
    Fintype.card_congr (Equiv.refl _)
  omega

/-- **Lemma 3.7 (outdegree), the component count.** A connected graph with a direction on every
edge and outdegree at most one, with `q` vertices of which `γ` have no outgoing edge, has `q - γ`
edges; `γ ≤ 1`; it is a tree if `γ = 1`; and if `γ = 0` it has a cycle and deleting any edge that is
not a bridge leaves a tree (exactly one cycle). -/
theorem component_count [Finite V] (hG : G.Connected) :
    Nat.card G.edgeSet + Nat.card {v : V // o.out v = none} = Nat.card V ∧
      Nat.card {v : V // o.out v = none} ≤ 1 ∧
      (Nat.card {v : V // o.out v = none} = 1 → G.IsTree) ∧
      (Nat.card {v : V // o.out v = none} = 0 →
        ¬G.IsAcyclic ∧ ∀ x y, G.Adj x y → ¬G.IsBridge s(x, y) →
          (G.deleteEdges {s(x, y)}).IsTree) := by
  have hcount := o.card_edgeSet_add_sinks
  have hlow := hG.card_vert_le_card_edgeSet_add_one
  refine ⟨hcount, by omega, fun h1 => ?_, fun h0 => ⟨fun hac => ?_, fun x y hxy hb => ?_⟩⟩
  · exact isTree_iff_connected_and_card.mpr ⟨hG, by omega⟩
  · have hT : G.IsTree := ⟨hG, hac⟩
    have := (isTree_iff_connected_and_card.mp hT).2
    omega
  · have hconn : (G.deleteEdges {s(x, y)}).Connected :=
      hG.preconnected.connected_deleteEdges_of_not_isBridge hb
    refine isTree_iff_connected_and_card.mpr ⟨hconn, ?_⟩
    have := Fintype.ofFinite V
    have hmem : s(x, y) ∈ G.edgeSet := hxy
    rw [edgeSet_deleteEdges, Nat.card_coe_set_eq, Set.ncard_sdiff_singleton_of_mem hmem,
      ← Nat.card_coe_set_eq]
    have hpos : 0 < Nat.card G.edgeSet := by
      rw [Nat.card_coe_set_eq]
      exact (Set.ncard_pos (Set.toFinite _)).mpr ⟨_, hmem⟩
    omega

end OutOrientation
end OAI.Barnette.Devices
