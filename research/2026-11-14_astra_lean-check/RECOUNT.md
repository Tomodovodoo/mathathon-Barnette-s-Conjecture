# Recount and TODO review

COMPUTED/PROVED-HERE. This is an advisory recount, conditional on the successful fresh build recorded in BUILD-LOG.md. Canonical blueprint statuses and charts are deliberately unchanged: TODO T5 is false, the full-Lemma-4.5 claim overstates the checked theorem, and the TODO inventory omits several blueprint obligations.

## Rule for counting

Use the blueprint's existing convention, which includes a weaker counterpart when it covers the part of the argument used by the formal route. This is not a count of 34 fully formalised paper statements. Preserve its four exact nodes. Add finite differences as exact. Count the real-sign lemma and the component-count part of outdegree as counterparts after translation, with their qualifications explicit. This gives **5 exact, 27 after translation, 2 without counterpart**, versus the old 4/25/5. The remaining no-counterpart nodes are Lemma 2.2 and Proposition 2.6(2).

If whole-statement coverage is required, do not silently reuse these numbers: outdegree lacks its directed-cycle sentence, and the old inventory already allowed five partial counterparts. A more generous convention might call the sign exact once oriented triangles and the disk identity are accepted; it would give 6/26/2. I retain the geometric orientation bridge and use 5/27/2. Neither count certifies the paper's full route.

## All 34 route nodes

| Node | Proposed category | Reason |
| --- | --- | --- |
| `thm:main` | after translation | Unchanged MainStatement rebuilt by replacement; the paper additionally prescribes an avoided edge. B5 remains. |
| `lem:dual` | after translation | Existing algebraic dual construction; no literal sphere/face translation added. |
| `txt:two-faces` | after translation | TriangleSystem edge_unique supplies the algebraic condition; drawing correspondence remains. |
| `lem:connected` | no counterpart | No literal topological connectivity lemma added. |
| `eq:counts` | after translation | Existing network/dual cardinality theorems; no new dictionary proof. |
| `def:selection` | after translation | Perfect matching in the primal versus one side per face in the dual. |
| `lem:duality.2` | after translation | Existing acyclicity-to-connectivity result; full spanning-tree clause still not added. |
| `lem:duality.1` | after translation | Existing circuit/cut correspondence in the network model. |
| `prop:target.1` | after translation | Existing matching-complement cycle construction, not a new sphere lemma. |
| `prop:target.2` | no counterpart | Two induced trees and the paper gluing through them still absent. |
| `def:state` | exact | Same incidence-constrained bijection; unchanged exact classification. |
| `def:good` | after translation | Paper requires one root per component. Formal route uses a partner plus acyclic Q; B4 remains. |
| `lem:good` | after translation | Full iff with S_s a spanning tree still absent; existing one-direction counterpart retained. |
| `lem:Y` | after translation | Hall constructs a matching; uniqueness of forest matching is now checked, but explicit rooted P_s and identification are not. |
| `lem:outdegree` | after translation | New component_count covers the component arithmetic and tree/unicycle conclusions. Directed-cycle sentence and restriction to actual Q components still missing. Promote only under existing weaker-but-covered convention. |
| `txt:inside` | after translation | Existing root-free shore/bond surrogate; no literal disk boundary bridge. |
| `lem:disk` | after translation | Existing disk delta/count theorems, now used by the real-sign route as well. |
| `prop:recover` | after translation | Existing selected-forest recovery theorem unchanged. |
| `def:pair` | exact | Subtype of state pairs differing at each face; exact under existing definition dictionary. |
| `lem:partner` | after translation | Orientation exists upstream; full component-root characterisation and partner uniqueness not supplied. |
| `txt:D` | after translation | Permutation orbit decomposition still the algebraic representation of directed chosen-side cycles. |
| `lem:reversals` | exact | Existing reverse and orient operations; unchanged exact classification. |
| `txt:delta` | after translation | indexDelta remains cyclic index order; geometric orientation correspondence is informal. |
| `lem:sign` | after translation | New paperSign reverse/orient/formula, including concrete versions. Product arithmetic checked; geometric ccw interpretation still uses B1. Count as different form conservatively. |
| `lem:cancel` | after translation | Real-sign fiber cancellation now checked. Full equality over unique good-state partners still missing. Keep different form, explicitly partial. |
| `txt:heights` | after translation | Face-path local turn signs are not defined in Lean; flow weights remain surrogate. |
| `lem:height` | after translation | New arbitrary-local-weight additivity; neither pointwise face-height jumps nor B3 implemented. |
| `lem:difference` | exact | New finite_difference_fin specialises exactly to real numbers and bit-subset indexing; stronger ring theorem supports exact classification. |
| `prop:good` | after translation | New real-sign finite-difference proof reaches the same forest-pair conclusion. B3/B4 and representative-minimum interpretation remain. |
| `txt:flow` | exact | Existing two_matchings theorem, unchanged. |
| `eq:hall` | after translation | Existing capacity theorem in the incidence/network model. |
| `prop:pair` | after translation | Existing no-three-cut argument and pair existence unchanged. |
| `lem:cap` | after translation | Existing capped network operations; sphere cap dictionary remains. |
| `thm:T` | after translation | The route still glues matchings with connected complements, not the paper two-induced-tree construction. |

## TODO statements

- **T1, correct target.** Equality of orbit counts for Q in P.Group is the right structural invariant. It is expressible under the ambient variables A,V,T,X and Fintype A. It does not alone state equality of the two minima; a short second lemma must transfer through GroupIndex.representative. The present nonvanishing proof only needs the representative minimum, so this is an interpretation gap, not an existence-proof gap.
- **T2, plausible but underspecified target.** The prose has no defined path family, kappa or function w and is not a Lean statement. State the choice of paths and coherent cyclic order, a per-face additive constant k(t), and the exact equality weights(alpha)(t)(v)=w(t)(v)+k(t). The slope sign must be positive for original delta=-3 and the reversal step negative there. Constant shifts leave slopes unchanged, so the generic realSum theorem can be reapplied to w once the bridge is proved. The statement “holds verbatim” should mean this reapplication, not equality of the original moments without a lower-moment/translation argument. The paper's stronger per-white-face 0/1 jump also remains.
- **T3, correct under omitted ambient partner premise.** Given r partner to s, each nonroot is r(t) exactly once, permitting out(v)=third corner; roots have no outgoing edge. A component restriction must transport all edges and its vertex finiteness. The statement as a standalone recipe must include that partner. It does not prove uniqueness of the partner for a good state.
- **T4, correct target.** For a genuine cycle, every cycle edge is covered, every vertex has at most one outgoing edge, and one_way prohibits double orientation. Counting the cycle edges forces one outgoing cycle edge at each cycle vertex. Propagation around the cycle gives precisely the forward/backward disjunction. getVert(c.length) is the start, so the last edge is included. This is not present in the checked component_count theorem.
- **T5, REFUTED.** It says every eligible perfect matching with connected complement comes from a good state. The paper says only that a cycle is produced if and only if its associated state is good. In the hexagonal prism, choose the outer dual triangle (6,0,1) and prescribed side (0,1). Our independent enumeration finds three states, two good, four eligible Hamiltonian cycles. Two recover the same non-good state. numerical.json lists all matching edges and recovered states; numerical.py is the reproducer. Correct target: first define the state recovered from an eligible cycle, then prove recovery from a good state is injective and that a cycle lies in the construction's image iff its recovered state is good. Do not assert surjectivity onto all Hamiltonian cycles.
- **T6, correct gap names, not precise formal targets.** Neither the plane-topological Lemma 2.2 nor the two-induced-tree Proposition 2.6(2) is stated in the TODO file as a Lean proposition. Not attempting them is honest. The claimed absence of a Jordan-curve library was not independently exhaustively checked in this review; it is not needed for the rebuilt theorem.

## Missing from the TODO inventory

Relative to BLUEPRINT.md and FORMALISATION.md, the list is incomplete. It must also retain B1, the literal drawing/face/inside/orientation to algebraic-dual dictionary; B4, the good-state/root-component bridge and full partner uniqueness; B5, the prescribed-edge drawing-level theorem; the full good-state cancellation equality of Lemma 4.5; the full iff of Lemma 3.5; the spanning-tree clause of Lemma 2.5(2); the explicit rooted selection P_s of Lemma 3.6 and identification with the existential matching; and the paper's two-tree gluing proof rather than the existing matching gluing. For off-route claims, neither the full multivariate polynomial remark nor the full exponential/Laurent lower-moment statements are formalised by proving the sign/phase relation.

The compiled matching-uniqueness lemma is useful but cannot by itself close the missing recovery and injectivity bridges. The real-sign equality closes B2 internally in the Lean model. It does not close B1 or B3.
