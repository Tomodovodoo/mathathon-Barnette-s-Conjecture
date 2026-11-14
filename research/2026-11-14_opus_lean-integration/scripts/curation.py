"""Hand-curated part of the blueprint: implicit uses, correspondences, Lean counterparts.

Every entry was written after reading the statement and its proof in the TeX source
and the Lean header in data/lean-sigs.json (commit 4eaee875). Conventions:

uses      final list of uses for the node (explicit citations mapped to parts, plus
          uses that the proof makes without a \\ref; those are listed in `implicit`).
rel       relation of the closest Lean declaration(s) to the statement:
          exact | primal-form | different-form | stronger | weaker | none
          ("primal-form": same content stated on G / algebraic dual;
           "different-form": same content with another device, e.g. phase instead of sign)
covered   True if the part of the statement that the main route uses is stated by a
          Lean declaration up to a translation that is listed in `bridge`.
route     'same' if the Lean proof follows the same argument, 'different' otherwise.
gap       for uncovered statements: nearest formal lemma and the distance.
"""

# Lean declarations are short names resolvable in data/lean-sigs.json.

MAIN = {
 'thm:main': dict(
    uses=['lem:dual', 'thm:T', 'prop:target.1'], implicit=[],
    openai='Thm 1.1 + Cor 7.1', primal='Theorem T', inv='-',
    lean=['main', 'Duality.connected_complement_matching', 'PlaneEmbedding.exists_exact_dual'],
    rel='primal-form', covered=True, route='different',
    bridge='Lean main has no prescribed edge; the edge-avoiding form is proved for graphs with an algebraic dual and is not restated for drawings (a few lines would combine it with exists_exact_dual).',
 ),
 'lem:dual': dict(
    uses=[], implicit=['background: Jordan curve theorem', 'background: Euler formula'],
    openai='proof of Thm 1.1 (Sec 7, paragraphs 1-2)', primal='Lemma 1; last paragraph of proof of Thm T', inv='-',
    lean=['cut_card_three', 'Duality.simple_dual_edge', 'Duality.cubic_face_triangles_edge', 'make_coloredDual', 'black_dual_card'],
    rel='primal-form', covered=True, route='different',
    bridge='"T simple with triangular faces" is "the algebraic dual D is simple and the star of every vertex of G is a triangle of D"; Lean argues by gradients of small support, not Jordan curves.',
 ),
 'lem:connected': dict(
    uses=[], implicit=['background: the sphere is connected'],
    openai='none (tacit)', primal='none (map rules in Sec 2)', inv='-',
    lean=['region_connected', 'Bond.connected_shore'],
    rel='none', covered=False, route='different',
    gap='Lean has no topological plane graphs. Nearest: region_connected (the region network of a connected shore A of G is connected) and Bond.connected_shore. These state connectivity of the inside of a cycle for the algebraic region network built from a vertex set of G, not for a plane graph whose faces are bounded by cycles. Far: different objects; the Lean needs no such lemma because connectivity is a field of Duality and survives minors (Duality.minor).',
 ),
 'eq:counts': dict(
    uses=['lem:connected'], implicit=['lem:connected (T connected, for Euler)'],
    openai='(2.1)', primal='Lemma 1 (counts)', inv='Sec 1',
    lean=['cubic_cards', 'black_dual_card', 'Duality.euler', 'nonroots_card'],
    rel='primal-form', covered=True, route='different',
    bridge='faces of T = vertices of G; Euler is a rank identity (Duality.euler).',
 ),
 'def:selection': dict(
    uses=[], implicit=[],
    openai='"one selected edge at each black and white triangle" (Sec 6.1)', primal='perfect matching P of G', inv='-',
    lean=['Duality.connected_complement_matching'],
    rel='primal-form', covered=True, route='same',
    bridge='a selection is a perfect matching P of G: (N.star v).filter (. in P) has card 1 for every v.',
 ),
 'lem:duality.1': dict(
    uses=[], implicit=['background: Jordan curve theorem'],
    openai='Sec 6.2 (Jordan curve labelling)', primal='circuit-cut fact; Lemma 2(a)', inv='background',
    lean=['Duality.circuit_cut', 'Duality.bond_of_circuit'],
    rel='primal-form', covered=True, route='different',
    bridge='a cycle of T is a flow circuit of D, equal to c times the gradient of the indicator of a root-free vertex set A of G; its support is the cut of A, a bond.',
 ),
 'lem:duality.2': dict(
    uses=[], implicit=['background: Euler formula'],
    openai='Lemma 2.1', primal='circuit-cut fact (converse direction)', inv='-',
    lean=['Duality.complement_connected', 'conserved_supported_acyclic'],
    rel='weaker', covered=True, route='different',
    bridge='Lean proves "N acyclic in T implies G minus N* connected". The spanning-tree sentence is not a lemma; where it is needed (lem:Y) Lean uses remainder_connected plus remainder_independent and an edge count.',
 ),
 'prop:target.1': dict(
    uses=['lem:duality.2', 'def:selection'], implicit=[],
    openai='proof of Thm 1.1, last paragraph', primal='Lemma 12, second paragraph', inv='-',
    lean=['Duality.hamiltonian', 'Duality.complement_connected', 'matching_complement_two', 'cycle_at_of_connected_two'],
    rel='primal-form', covered=True, route='same',
 ),
 'prop:target.2': dict(
    uses=['lem:duality.1', 'eq:counts', 'def:selection'], implicit=['eq:counts (k edges on k+2 vertices)', 'background: a cycle meets an edge cut evenly'],
    openai='Thm 2.2 (two induced trees)', primal='Remark 15 (part)', inv='-',
    lean=[],
    rel='none', covered=False, route='-',
    gap='Theorem 2.2 is not stated anywhere in the Lean (opus_lean-formalisation DIFFERENCES item 22). Nearest: Duality.circuit_cut + cap_matching_boundary (exactly one cut edge of a 3-cut lies in a perfect matching). Far: the Lean glues perfect matchings with connected complement and never needs the two-component structure of P.',
 ),
 'lem:selections-give-states': dict(
    uses=['prop:target.2'], implicit=[],
    openai='none', primal='Remark 15 (stronger: also uniqueness)', inv='-',
    lean=[],
    rel='none', covered=False, route='-',
    gap='No counterpart; the Lean never goes from a Hamiltonian cycle back to a state. Off the main route (motivation and Sec 7 remark only).',
 ),
 'def:state': dict(
    uses=[], implicit=[],
    openai='Sec 2 (state)', primal='Sec 3 (state)', inv='Sec 1 (state)',
    lean=['TriangleSystem.State', 'ColoredDual.State'],
    rel='exact', covered=True, route='same',
 ),
 'def:good': dict(
    uses=['def:state'], implicit=[],
    openai='Prop 5.1 + Lemma 6.1 (no name)', primal='"circuit-free Q_s" with partner; Remark 14', inv='Theorem 1 (forest Q_s)',
    lean=['oppositeGraph', 'ColoredDual.augQ'],
    rel='different-form', covered=True, route='-',
    bridge='Lean never names good states; it works with "second state of a pair with oppositeGraph acyclic" and adds two root sides (augQ).',
 ),
 'lem:good': dict(
    uses=['eq:counts', 'def:good'], implicit=['eq:counts (|S_s| = |V(T)|-1)'],
    openai='Sec 6.1 ("the remainder is a spanning tree of H")', primal='Lemma 9, first paragraph; Remark 14', inv='-',
    lean=['ColoredDual.removed_acyclic', 'ColoredDual.augQ_acyclic'],
    rel='weaker', covered=True, route='different',
    bridge='Lean proves only "pair with Q_s acyclic implies S_s (removed) acyclic", i.e. lem:partner followed by the direction good => spanning tree that lem:Y uses. The converse is not formalised.',
 ),
 'txt:two-faces': dict(
    uses=[], implicit=[],
    openai='tacit', primal='Lemma 1 (two faces share at most one edge)', inv='-',
    lean=['TriangleSystem', 'ColoredDual.system'],
    rel='primal-form', covered=True, route='different',
    bridge='a field of TriangleSystem: two triangles sharing two vertices coincide; supplied for ColoredDual.system from simplicity of D.',
 ),
 'lem:Y': dict(
    uses=['lem:good', 'lem:duality.2', 'txt:two-faces', 'eq:counts', 'def:selection'], implicit=['txt:two-faces', 'eq:counts (2k faces)'],
    openai='Sec 6.1 (tree on white faces, rooted at y0)', primal='Lemmas 9 and 10', inv='-',
    lean=['ColoredDual.remainder_connected', 'ColoredDual.remainder_independent', 'ColoredDual.remainder_black_degree', 'tree_matching', 'ColoredDual.recovery_matching'],
    rel='weaker', covered=True, route='different',
    bridge='Lean proves that Y_s (complement of removed in G) is a spanning tree with black degrees 2 and root degree 1, then gets SOME perfect matching inside it by Hall (tree_matching). The explicit rooting rule that defines P_s is not formalised; only existence is, which is all the theorem needs.',
 ),
 'lem:outdegree': dict(
    uses=[], implicit=[],
    openai='inline in Lemma 5.2, 6.1, 6.2', primal='inline (Sec 3, Lemma 9)', inv='inline (Lemma 4)',
    lean=['CycleCoordinates.tail_orientation', 'addSink_acyclic'],
    rel='weaker', covered=False, route='different',
    gap='tail_orientation states "injective tails on a cycle force a directed cycle" (first sentence). The component count (q - gamma edges, gamma <= 1, tree iff gamma = 1) is not formalised: Lean replaces it by addSink_acyclic (outdegree <= 1 plus a sink gives acyclicity). Close: about 30-60 Lean lines on top of Mathlib SimpleGraph.IsTree.card_edgeFinset.',
 ),
 'txt:inside': dict(
    uses=['lem:connected'], implicit=['background: Jordan curve theorem (only Jordan is needed although the text says "open disk")'],
    openai='Sec 4, one sentence ("its bounded disk contains no root")', primal='Lemma 2 (cut side, no-pinch)', inv='background',
    lean=['Duality.circuit_cut', 'Bond.connected_shore', 'region_connected', 'region_euler', 'mixed_corner_on_boundary'],
    rel='different-form', covered=True, route='different',
    bridge='the inside of Z is the root-free shore A of the bond cut(A) = Z; Euler for R_Z is region_euler |A| + |U| = |E(A)| + 1; "no vertex is pinched" is mixed_corner_on_boundary. The paper\'s object R_Z and its connectivity via lem:connected have no counterpart.',
 ),
 'lem:disk': dict(
    uses=['txt:inside', 'lem:outdegree', 'def:state'], implicit=['txt:inside (Euler for R_Z)', 'lem:outdegree (vertices of Z lie in X)', 'def:state (both halves of bijectivity)'],
    openai='Lemma 4.1', primal='Lemma 5', inv='Lemma 2',
    lean=['state_disk_delta', 'ColoredDual.cycle_disk', 'state_disk_count', 'disk_boundary_imbalance', 'white_positive_of_boundary'],
    rel='primal-form', covered=True, route='same',
    bridge='Lean states h = 2l+3 as |cut A| = 2|blackCut A| + 3 and W >= 1 as white_positive_of_boundary; W = B+1 is not stated (it follows from cubic_black_region_count). disk_count_identity (PairPhases:22) is the paper\'s arithmetic, proved and unused.',
 ),
 'prop:recover': dict(
    uses=['lem:Y', 'lem:outdegree', 'lem:disk', 'prop:target.1'], implicit=['lem:disk ("the disk identity gives")'],
    openai='Lemma 6.2 and end of Sec 6.2', primal='Lemmas 11 and 12', inv='-',
    lean=['ColoredDual.selected_forest', 'ColoredDual.selectNet_forest', 'matching_cut_balance', 'ColoredDual.recover_connected_complement'],
    rel='stronger', covered=True, route='same',
    bridge='Lean (and primal Lemma 12) prove acyclicity for every perfect matching compatible with s, not only P_s. "Matched across Z" count = matching_cut_balance. The component-per-root step uses addSink in Lean, lem:outdegree here.',
 ),
 'def:pair': dict(
    uses=['def:state'], implicit=[],
    openai='Sec 2 (pair)', primal='Sec 3 (pair)', inv='Sec 1 (pair)',
    lean=['TriangleSystem.Partner', 'TriangleSystem.Pair'],
    rel='exact', covered=True, route='same',
 ),
 'lem:partner': dict(
    uses=['lem:outdegree', 'def:pair', 'def:good'], implicit=[],
    openai='Lemma 5.2 proof (outdegree) and Lemma 6.1', primal='Sec 3; Lemma 9; Remark 14 (uniqueness)', inv='Lemma 4 proof',
    lean=['TriangleSystem.OppositeCycle.partner_orientation', 'ColoredDual.augQ_acyclic'],
    rel='weaker', covered=True, route='different',
    bridge='"a cycle of Q_s is directed by r" is partner_orientation; "acyclic Q_s with a partner has one root per component" is replaced by augQ_acyclic. Uniqueness of the partner of a good state is not formalised; the main route needs it only for the regrouped formula of lem:cancel, which prop:good does not need.',
 ),
 'txt:D': dict(
    uses=['def:pair', 'lem:partner'], implicit=[],
    openai='Sec 5 (D is a union of vertex-disjoint cycles)', primal='Lemma 8, first paragraph', inv='Sec 2 (D_p)',
    lean=['TriangleSystem.Pair.next', 'CycleClass', 'ColoredDual.pairedCycle'],
    rel='different-form', covered=True, route='different',
    bridge='cycles of D are the cycles of the permutation next = r^-1 o s of the black triangles; pairedCycle turns one into a state cycle of T.',
 ),
 'lem:reversals': dict(
    uses=['lem:partner', 'txt:D'], implicit=['txt:D (part 2)'],
    openai='Lemma 5.2 proof (1); Sec 5.3 grouping (2)', primal='Lemma 7 proof (1); Lemma 8 (2)', inv='Lemma 4 (1); Lemma 5 case 1 (2)',
    lean=['TriangleSystem.OppositeCycle.reverse', 'TriangleSystem.OppositeCycle.reversal_involutive', 'TriangleSystem.OppositeCycle.reversal_ne', 'TriangleSystem.Pair.orient', 'TriangleSystem.Pair.groupEquiv'],
    rel='exact', covered=True, route='same',
    bridge='(2) appears as the bijection between orientation bits of the cycles of next and the pairs with the same D (groupEquiv).',
 ),
 'txt:delta': dict(
    uses=['lem:disk'], implicit=[],
    openai='Sec 4 (delta)', primal='Sec 2 (delta), Lemma 3', inv='Sec 2 (delta)',
    lean=['TriangleSystem.indexDelta', 'Triangle.index_delta', 'blackDelta', 'ColoredDual.cycle_disk'],
    rel='different-form', covered=True, route='different',
    bridge='delta is indexDelta of the stored corner labelling; "counterclockwise" is the sign c in cycle flow = c * gradient(1_A); cycle_disk gives blackDelta = -3c.',
 ),
 'lem:sign': dict(
    uses=['lem:reversals', 'lem:disk', 'txt:delta', 'txt:D'], implicit=['txt:delta', 'txt:D (lengths add up to n)'],
    openai='(5.1): phase i^J', primal='Lemmas 7-8 (same real sign)', inv='Definition 3 (sign with floor(J/2))',
    lean=['phase', 'TriangleSystem.rawIndexSum', 'TriangleSystem.OppositeCycle.reverse_phase', 'phase_add_six', 'TriangleSystem.Pair.group_sum_product'],
    rel='none', covered=False, route='different',
    gap='The real sign eps = prod delta(r(t),s(t)) does not occur in the Lean, which uses phase(rawIndexSum) = I^(sum delta div 3) and proves only that one Q_s-reversal multiplies it by -1 (reverse_phase) and that it factorises over D-cycles (group_sum_product). Distance: the identity eps = i^n * phase(rawIndexSum), which needs 3 | sum delta from the disk identity on every D-cycle (primal STATUS.md, phase comparison). Estimated 60-120 Lean lines; see FORMALISATION.md.',
 ),
 'lem:cancel': dict(
    uses=['lem:reversals', 'lem:sign', 'lem:partner'], implicit=[],
    openai='Lemma 5.2', primal='Lemma 7', inv='Lemma 4',
    lean=['TriangleSystem.OppositeCycle.fixed_second_state_cancels', 'ColoredDual.opposite_disk'],
    rel='different-form', covered=True, route='same',
    bridge='Lean cancels with the complex phase and any weight in a C-module; the real-sign version follows through the uncovered lem:sign bridge. The regrouped formula (sum over good states with their unique partner) is not stated.',
 ),
 'txt:heights': dict(
    uses=['lem:duality.2'], implicit=['lem:duality.2 with N empty: G connected, so paths of faces exist'],
    openai='Lemma 5.3 (spoke circulations, different weights)', primal='Lemma 6 (integer path flow and local potentials)', inv='rays rho_w and crossings (Sec 1)',
    lean=['whiteCharge', 'boundary_of_sum_zero', 'ColoredDual.weights'],
    rel='different-form', covered=True, route='different',
    bridge='summing the unit path flows from each white face y to t0 gives a flow alpha on G with boundary whiteCharge; the heights kappa are then the potentials ColoredDual.weights alpha up to one additive constant per black triangle (constants cancel on every cycle). This identification is not formalised.',
 ),
 'lem:height': dict(
    uses=['txt:heights', 'txt:D', 'lem:duality.1', 'lem:disk'], implicit=['lem:disk (L(C) >= 1)', 'txt:D (faces of C lie in A)'],
    openai='Lemma 5.3 and (5.3)', primal='Lemma 6', inv='crossing pairing (Lemmas 5-6)',
    lean=['whiteCharge_cut_integral', 'ColoredDual.StateCycle.signed', 'ColoredDual.paired_sign', 'white_positive_of_boundary'],
    rel='weaker', covered=True, route='different',
    bridge='Lean proves the summed statement for EVERY flow with boundary whiteCharge (slope = c * #white faces inside), hence for the path flow of the heights. The per-white-face statement (jump 1 or 0 at each y) is not formalised; the main route uses only the sum.',
 ),
 'lem:difference': dict(
    uses=[], implicit=[],
    openai='Taylor coefficient of the product (5.4)-(5.5)', primal='Lemma 8 (product of linear polynomials)', inv='Sec 7 (moment comparison, off-route)',
    lean=['TriangleSystem.Pair.cycle_factor_witness', 'common_phase_sum_ne_zero'],
    rel='none', covered=False, route='different',
    gap='The Lean never forms omega^m: it factorises each D-class as a product of polynomials X * q_C with q_C(0) > 0 (cycle_factor_witness) and reads off the lowest coefficient (common_phase_sum_ne_zero). Distance: the identity itself is self-contained algebra (Mathlib has only the one-step versions fwdDiff_iter_pow_eq_zero_of_lt and fwdDiff_iter_eq_factorial in Algebra/Group/ForwardDiff.lean, with one common step h). PROVED in Lean here: research/2026-11-14_opus_blueprint/lean/FiniteDifference.lean (see FORMALISATION.md).',
 ),
 'prop:good': dict(
    uses=['lem:cancel', 'lem:reversals', 'lem:sign', 'lem:height', 'lem:difference', 'txt:D', 'lem:partner'], implicit=['txt:D (class of a pair)', 'lem:partner (acyclic Q_s with a partner is good)'],
    openai='Prop 5.1', primal='Lemma 8', inv='Theorem 1',
    lean=['ColoredDual.forest_pair', 'TriangleSystem.Pair.forest_pair_of_disk_circulation', 'TriangleSystem.Pair.total_sum_ne_zero'],
    rel='primal-form', covered=True, route='different',
    bridge='forest_pair: if a pair exists, some pair has oppositeGraph of its second state acyclic; that state is good by lem:partner. Same conclusion, different nonvanishing argument (phase * prod (1 + aX) instead of eps * omega^m).',
 ),
 'rem:other-sums': dict(
    uses=['lem:difference'], implicit=[],
    openai='(5.2)', primal='(6.1)', inv='Sec 7', lean=['TriangleSystem.Pair.term'],
    rel='none', covered=False, route='-',
    gap='Off-route remark. The referee (sol_referee-main) noted that sum eps z^omega is a Laurent polynomial, not an integer polynomial, since omega can be negative (Table 4.2 has omega = -4).',
 ),
 'eq:hall': dict(
    uses=['def:pair'], implicit=[],
    openai='(3.1)', primal='(3.1)', inv='-', lean=['ColoredDual.state_capacity'],
    rel='primal-form', covered=True, route='same',
 ),
 'txt:flow': dict(
    uses=['eq:hall', 'def:pair'], implicit=['background: integral max-flow min-cut (Ford-Fulkerson)'],
    openai='Prop 3.1, first paragraph', primal='Lemma 4, first paragraph', inv='-',
    lean=['BMatching.two_matchings'],
    rel='exact', covered=True, route='different',
    bridge='two_matchings: equal sides and 2|S| <= sum_b min(2, |S cap N(b)|) give two disjoint perfect matchings. Lean uses Hall twice instead of max-flow.',
 ),
 'prop:pair': dict(
    uses=['txt:flow', 'eq:hall', 'eq:counts', 'txt:two-faces', 'lem:dual'], implicit=['txt:two-faces / one black face per edge ("would share the side ab")', 'lem:dual (simplicity, via the definition of coloured triangulation)', 'background: Euler formula for H'],
    openai='Prop 3.1', primal='Lemma 4 (different proof: minimal deficit)', inv='hypothesis',
    lean=['ColoredDual.pair_nonempty', 'ColoredDual.state_capacity', 'capacity_full', 'induced_density', 'region_density', 'region_balance_rim', 'rim_defect', 'rim_three_cut', 'complement_singleton_root', 'induced_euler_bound'],
    rel='primal-form', covered=True, route='same',
    bridge='"no separating triangle" is TrivialThreeCuts (every 3-edge cut of G has a singleton side). The density bound is proved globally (induced_euler_bound), not per component.',
 ),
 'lem:cap': dict(
    uses=['lem:connected'], implicit=[],
    openai='proof of Thm 2.2 (cap colouring)', primal='Lemma 13, first part', inv='-',
    lean=['threeCut_black_card', 'cap_coloring', 'cap_simple', 'cap_cubic', 'cap_threeConnected', 'cap_duality'],
    rel='primal-form', covered=True, route='different',
    bridge='the piece is the contraction G / A^c; its dual comes from Duality.minor instead of lem:connected.',
 ),
 'thm:T': dict(
    uses=['prop:pair', 'prop:good', 'prop:recover', 'lem:cap', 'prop:target.2'], implicit=[],
    openai='Thm 2.2', primal='Theorem T (first sentence)', inv='-',
    lean=['Duality.connected_complement_matching', 'irreducible_matching', 'cap_matching_boundary', 'cap_glue_matching', 'cap_glue_connected'],
    rel='primal-form', covered=True, route='different',
    bridge='statement: perfect matching P containing e with G - P connected (no face parameter). Route: Lean glues matchings (cap_glue_connected); the paper glues acyclic selections using prop:target.2, which is not formalised.',
 ),
 'rem:which': dict(
    uses=['lem:selections-give-states', 'prop:recover', 'lem:Y'], implicit=[],
    openai='none', primal='Remarks 14-15', inv='-', lean=[],
    rel='none', covered=False, route='-',
    gap='Off-route. No Lean counterpart.',
 ),
 'rem:poly': dict(
    uses=['lem:partner', 'lem:cancel', 'prop:good'], implicit=[],
    openai='(5.4)', primal='(6.3)', inv='-', lean=['TriangleSystem.Pair.group_sum_product'],
    rel='weaker', covered=False, route='-',
    gap='Off-route. group_sum_product is this factorisation after the substitution w_(t,v) = 1 + a(t,v) X, with the phase in place of the sign.',
 ),
}

# drop the explicit citation of these labels (cited in running text of the proof, not used)
DROP = {'txt:flow': ['prop:good'], 'prop:pair': ['eq:density']}

# examples are numbered but carry no proof obligations
EXAMPLES_OFF_ROUTE = True

PRIMAL = {
 'PT': dict(uses=['PL4', 'PL5', 'PL6', 'PL7', 'PL8', 'PL9', 'PL10', 'PL11', 'PL12', 'PL13'],
            lean=['Duality.connected_complement_matching', 'matching_strong', 'main'], rel='primal-form', covered=True,
            main='thm:T', note='plane map versus algebraic dual'),
 'Pcircuit': dict(uses=[], lean=['Duality.circuit_cut', 'Duality.bond_of_circuit', 'Bond.connected_shore'], rel='primal-form', covered=True,
            main='lem:duality.1', note='converse (bond => face circuit) proved by kernel duality in Lean'),
 'PL1': dict(uses=['Pcircuit'], lean=['ColoredDual.cubic_cards', 'ColoredDual.nonroots_card', 'make_coloredDual'], rel='primal-form', covered=True, main='lem:dual'),
 'PL2': dict(uses=['Pcircuit'], lean=['Duality.circuit_cut', 'Bond.connected_shore', 'region_euler', 'mixed_corner_on_boundary'], rel='primal-form', covered=True, main='txt:inside'),
 'PL3': dict(uses=['PL2'], lean=['cycle_cut_scalar', 'blackDelta_cut', 'Triangle.index_delta'], rel='different-form', covered=True, main='txt:delta',
            note='no single Lean counterpart; coherence of orientations comes from the algebra (oriented_face)'),
 'PL4': dict(uses=['PL1'], lean=['ColoredDual.pair_nonempty'], rel='exact', covered=True, main='prop:pair',
            note='hypothesis is literally TrivialThreeCuts; proof differs (minimal deficit and max-flow versus density and Hall)'),
 'PL5': dict(uses=['PL2', 'PL3'], lean=['state_disk_count', 'disk_boundary_imbalance', 'state_disk_delta'], rel='exact', covered=True, main='lem:disk'),
 'PL6': dict(uses=['PL5', 'PL3'], lean=['boundary_of_sum_zero', 'whiteCharge_cut_integral', 'ColoredDual.StateCycle.signed'], rel='exact', covered=True, main='lem:height',
            note='Lean allows any real flow; the note specialises to an integer path flow'),
 'PL7': dict(uses=['PL5'], lean=['TriangleSystem.OppositeCycle.fixed_second_state_cancels'], rel='different-form', covered=True, main='lem:cancel',
            note='real sign versus complex phase; ratio i^n (primal STATUS.md)'),
 'PL8': dict(uses=['PL1', 'PL5', 'PL6', 'PL7'], lean=['TriangleSystem.Pair.total_sum_ne_zero', 'TriangleSystem.Pair.forest_pair_of_disk_circulation'], rel='different-form', covered=True, main='prop:good',
            note='same linear products as Lean; real prefactor (-1)^((n-c)/2) not in Lean'),
 'PL9': dict(uses=['PL2'], lean=['ColoredDual.removed_acyclic', 'ColoredDual.remainder_connected', 'ColoredDual.remainder_black_degree', 'ColoredDual.remainder_independent'], rel='exact', covered=True, main='lem:Y'),
 'PL10': dict(uses=['PL9'], lean=['tree_matching', 'ColoredDual.recovery_matching'], rel='weaker', covered=True, main='lem:Y',
            note='Lean gives existence by Hall; the rooting rule is not formalised'),
 'PL11': dict(uses=[], lean=['matching_cut_balance'], rel='exact', covered=True, main='prop:recover'),
 'PL12': dict(uses=['PL5', 'PL11', 'PL9', 'Pcircuit'], lean=['ColoredDual.selectNet_forest', 'ColoredDual.selected_forest', 'ColoredDual.recover_connected_complement'], rel='exact', covered=True, main='prop:recover'),
 'PL13': dict(uses=['PL1'], lean=['cap_simple', 'cap_cubic', 'cap_threeConnected', 'cap_coloring', 'cap_glue_matching', 'cap_glue_connected', 'cap_duality'], rel='primal-form', covered=True, main='lem:cap'),
 'PR14': dict(uses=['PL9', 'Pcircuit'], lean=[], rel='none', covered=False, main='lem:partner', note='added in the revision after the Fable referee'),
 'PR15': dict(uses=['PL12', 'Pcircuit'], lean=[], rel='none', covered=False, main='lem:selections-give-states', note='added in the revision after the Fable referee'),
}

INVOLUTIONS = {
 'I:main': dict(uses=['I:one', 'I:two', 'I:fixed', 'I:objects'], lean=['ColoredDual.forest_pair'], rel='primal-form', covered=True, main='prop:good'),
 'I:disk': dict(uses=[], lean=['state_disk_delta'], rel='primal-form', covered=True, main='lem:disk'),
 'I:objects': dict(uses=['I:disk'], lean=[], rel='none', covered=False, main='txt:heights',
            note='rays, tokens and the sign with floor(J/2) have no Lean counterpart'),
 'I:one': dict(uses=['I:disk', 'I:objects'], lean=['TriangleSystem.OppositeCycle.reversal_involutive', 'TriangleSystem.OppositeCycle.reverse_phase'], rel='weaker', covered=False, main='lem:cancel',
            note='Lean has the reversal and its phase flip, not the action on marked objects'),
 'I:two': dict(uses=['I:objects', 'I:disk'], lean=[], rel='none', covered=False, main='prop:good'),
 'I:fixed': dict(uses=['I:disk', 'I:two'], lean=['common_phase_sum_ne_zero'], rel='none', covered=False, main='prop:good',
            note='F = sum prod a(C) is the lowest coefficient magnitude of Lean\'s polynomial for the white-charge weights; Lean only proves it is positive'),
 'I:walk': dict(uses=['I:one', 'I:two', 'I:fixed'], lean=[], rel='none', covered=False, main=None,
            note='constructive alternating path; the Lean proof is not constructive'),
}

# five-column chart: (waypoint, OpenAI, merged, primal, involutions, Lean)
WAYPOINTS = [
 ('statement', 'Thm 1.1, Cor 7.1', ['thm:main'], ['PT'], [], ['main', 'Duality.connected_complement_matching']),
 ('dual is a coloured triangulation', 'Sec 7, proof of Thm 1.1', ['lem:dual', 'eq:counts'], ['PL1'], [], ['make_coloredDual', 'Duality.simple_dual_edge', 'black_dual_card']),
 ('cycle = cut, forest => connected dual', 'Lemma 2.1; Sec 6.2', ['lem:duality.1', 'lem:duality.2', 'lem:connected'], ['Pcircuit'], [], ['Duality.circuit_cut', 'Duality.complement_connected']),
 ('target: acyclic selection => HC', 'Thm 2.2; proof of Thm 1.1', ['prop:target.1', 'prop:target.2'], ['PL12'], [], ['Duality.hamiltonian']),
 ('states and pairs', 'Sec 2', ['def:state', 'def:pair'], [], [], ['TriangleSystem.State', 'TriangleSystem.Pair']),
 ('a pair exists', 'Prop 3.1', ['txt:flow', 'prop:pair'], ['PL4'], [], ['ColoredDual.pair_nonempty', 'BMatching.two_matchings']),
 ('inside of a cycle', 'Sec 4 (one sentence)', ['txt:inside'], ['PL2'], [], ['region_euler', 'mixed_corner_on_boundary']),
 ('disk identity', 'Lemma 4.1', ['lem:disk'], ['PL5'], ['I:disk'], ['state_disk_delta']),
 ('sign', '(5.1) phase i^J', ['txt:delta', 'lem:sign'], ['PL3', 'PL7'], ['I:objects'], ['phase', 'TriangleSystem.OppositeCycle.reverse_phase']),
 ('cancel cyclic Q_s', 'Lemma 5.2', ['lem:reversals', 'lem:cancel'], ['PL7'], ['I:one'], ['TriangleSystem.OppositeCycle.fixed_second_state_cancels']),
 ('weights with positive slope', 'Lemma 5.3, (5.3)', ['txt:heights', 'lem:height'], ['PL6'], ['I:objects'], ['whiteCharge_cut_integral', 'ColoredDual.StateCycle.signed']),
 ('group by D', 'Sec 5.3', ['txt:D'], ['PL8'], ['I:two'], ['TriangleSystem.Pair.groupEquiv', 'TriangleSystem.Pair.group_sum_product']),
 ('nonvanishing', '(5.4)-(5.5), Prop 5.1', ['lem:difference', 'prop:good'], ['PL8'], ['I:fixed', 'I:main'], ['TriangleSystem.Pair.total_sum_ne_zero', 'ColoredDual.forest_pair']),
 ('forest pair => spanning tree', 'Lemma 6.1, Sec 6.1', ['lem:partner', 'lem:good'], ['PL9'], [], ['ColoredDual.augQ_acyclic', 'ColoredDual.removed_acyclic']),
 ('selection from the tree', 'Sec 6.1 (rooting at y0)', ['lem:Y'], ['PL10'], [], ['tree_matching']),
 ('selection is acyclic', 'Lemma 6.2', ['lem:outdegree', 'prop:recover'], ['PL11', 'PL12'], [], ['ColoredDual.selected_forest', 'matching_cut_balance']),
 ('separating triangles', 'Sec 7, proof of Thm 2.2', ['lem:cap', 'thm:T'], ['PL13', 'PT'], [], ['cap_glue_connected', 'matching_strong']),
 ('construct a forest pair', '-', [], [], ['I:walk'], []),
]


# ======================================================================================
# Version 2 statuses (research/2026-11-14_opus_lean-integration), after the independent
# rebuild and audit research/2026-11-14_astra_lean-check (FAITHFULNESS.md, RECOUNT.md).
# Where the author's Lean report (opus_lean-devices) and the checker disagree, the
# checker's verdict is used.
#
# status   exact        exact Lean counterpart, given the definitions of states and pairs
#          translation  Lean counterpart after an unformalised translation (named in `via`)
#          weaker       Lean counterpart for a weaker or different form (`how`)
#          none         no counterpart
# origin   upstream     only declarations of openai/math@4eaee875
#          project      declarations added in proofs/lean/Devices, independently rebuilt
#          both         the statement's counterpart combines the two
# lean2    project declarations added to the node's Lean list (upstream ones stay in `lean`)
# B1..B5 are the translations named in proofs/blueprint/BLUEPRINT.md:
#   B1 drawing -> algebraic dual (faces, inside, orientation as indexDelta / sign c)
#   B2 real sign <-> OpenAI phase (now CHECKED: sign_eq_I_pow_mul_phase_concrete)
#   B3 heights along face paths <-> weights of a flow with boundary whiteCharge
#   B4 good state (one root per component) <-> second state of a pair with acyclic Q_s
#   B5 prescribed-edge theorem for drawings (combine with exists_exact_dual)
# ======================================================================================

V2 = {
 'thm:main': dict(status='weaker', origin='both', lean2=[],
    how='OAI.Barnette.main states Hamiltonicity without the avoided edge; the avoided-edge form is Duality.connected_complement_matching for graphs with an algebraic dual (B1, B5). main is rebuilt unchanged through the project route.'),
 'lem:dual': dict(status='translation', origin='upstream', lean2=[], via='B1 (simple T with triangular faces = simple algebraic dual whose vertex stars are triangles)'),
 'txt:two-faces': dict(status='translation', origin='upstream', lean2=[], via='B1 (field edge_unique of TriangleSystem)'),
 'lem:connected': dict(status='none', origin='-', lean2=[], how='no plane topology in the Lean; nearest is region_connected for the algebraic region network'),
 'eq:counts': dict(status='translation', origin='upstream', lean2=[], via='B1 (faces of T = vertices of G; Euler as a rank identity)'),
 'def:selection': dict(status='translation', origin='upstream', lean2=[], via='B1 (selection = perfect matching of G)'),
 'lem:duality.1': dict(status='translation', origin='upstream', lean2=[], via='B1 (cycle of T = flow circuit of D, support a bond)'),
 'lem:duality.2': dict(status='weaker', origin='upstream', lean2=[], how='Lean proves N acyclic => G - N* connected; the spanning-tree clause is not a lemma'),
 'prop:target.1': dict(status='translation', origin='upstream', lean2=[], via='B1 (matching complement with two edges at each vertex, connected => Hamiltonian cycle)'),
 'prop:target.2': dict(status='none', origin='-', lean2=[], how='two induced trees are not stated; the Lean glues matchings instead'),
 'def:state': dict(status='exact', origin='upstream', lean2=[]),
 'def:good': dict(status='weaker', origin='upstream', lean2=[], how='the Lean never defines one root per component; it uses the second state of a pair with acyclic Q_s (B4). Acyclic Q_s alone is not equivalent (checker: hexagonal prism)'),
 'lem:good': dict(status='weaker', origin='upstream', lean2=[], how='only the direction pair with acyclic Q_s => S_s acyclic; the converse and the spanning-tree iff are absent'),
 'lem:Y': dict(status='weaker', origin='both', lean2=['IsAcyclic.perfectMatching_unique'], how='Y_s spanning tree and SOME perfect matching by Hall (upstream); uniqueness of a forest perfect matching is now checked (project), but the rooted rule defining P_s and its identification with the Hall matching are not'),
 'lem:outdegree': dict(status='weaker', origin='project', lean2=['OutOrientation.card_edgeSet_add_sinks', 'OutOrientation.component_count'], how='component_count gives |E| + sinks = q, at most one sink, tree with one sink, one cycle with none, for one finite connected graph; the first sentence (every cycle is directed, T4) is missing and the lemma is not applied to Q_s (T3)'),
 'txt:inside': dict(status='translation', origin='upstream', lean2=[], via='B1 (inside of Z = root-free shore A of the bond cut(A) = Z)'),
 'lem:disk': dict(status='translation', origin='upstream', lean2=[], via='B1 (|cut A| = 2|blackCut A| + 3; W >= 1)'),
 'prop:recover': dict(status='translation', origin='upstream', lean2=[], via='B1; Lean proves it for every perfect matching compatible with s, which is stronger'),
 'def:pair': dict(status='exact', origin='upstream', lean2=[]),
 'lem:partner': dict(status='weaker', origin='upstream', lean2=[], how='partner_orientation directs cycles of Q_s; one root per component (B4) and uniqueness of the partner of a good state are not formalised'),
 'txt:D': dict(status='translation', origin='upstream', lean2=[], via='cycles of D(r,s) = orbits of the permutation next = r^-1 o s'),
 'lem:reversals': dict(status='exact', origin='upstream', lean2=[]),
 'txt:delta': dict(status='translation', origin='upstream', lean2=[], via='B1 (delta = indexDelta of the stored cyclic order; counterclockwise = delta-sum -3)'),
 'lem:sign': dict(status='translation', origin='project', lean2=['OppositeCycle.paperSign_reverse', 'Pair.sign_orient', 'Pair.sign_formula', 'ColoredDual.sign_formula_concrete'], via='B1 only for the word counterclockwise: Lean counts cycles of D with delta-sum -3 (ccwCount). Both reversals and the closed formula are proved for the concrete system with no further hypothesis'),
 'lem:cancel': dict(status='weaker', origin='project', lean2=['OppositeCycle.paperSign_partners_sum', 'Pair.sum_sign_eq_zero_of_no_good'], how='first sentence proved with the real sign; second sentence only in the case where no pair has acyclic Q_s (total sum zero), which is what the existence proof by contradiction uses. The equality with a sum over good states and their unique partners is not stated'),
 'txt:heights': dict(status='weaker', origin='upstream', lean2=[], how='face-path heights are not defined in Lean; the Lean uses the potentials of a flow with boundary whiteCharge (B3, T2)'),
 'lem:height': dict(status='weaker', origin='both', lean2=['Pair.weight_orient'], how='additivity of reversals for arbitrary local weights (project) and slope = number of white faces inside for flow weights (upstream whiteCharge_cut_integral); the per-white-face jump of 0 or 1 and the face-path heights are absent (B3)'),
 'lem:difference': dict(status='exact', origin='project', lean2=['finite_difference_fin', 'finite_difference'], how='stronger: any commutative ring, any finite index set'),
 'prop:good': dict(status='translation', origin='both', lean2=['ColoredDual.forest_pair_real', 'Pair.forest_pair_of_disk_circulation_real', 'Pair.realSum_ne_zero'], via='B4 (conclusion is a pair whose Q_s is acyclic, not "a good state"); the proof by eps * omega^m and finite differences is checked with the Lean flow weights in place of heights (B3), and m is the minimum over class representatives (T1)'),
 'txt:flow': dict(status='exact', origin='upstream', lean2=[]),
 'eq:hall': dict(status='translation', origin='upstream', lean2=[], via='B1 (capacity condition in the incidence network)'),
 'prop:pair': dict(status='translation', origin='upstream', lean2=[], via='B1 (no separating triangle = TrivialThreeCuts)'),
 'lem:cap': dict(status='translation', origin='upstream', lean2=[], via='B1 (piece = contraction G/A^c; dual from Duality.minor)'),
 'thm:T': dict(status='translation', origin='upstream', lean2=[], via='B1 (acyclic selection containing e0 = perfect matching containing e with G - P connected); the Lean proof glues matchings, not acyclic selections through Prop. 2.6(2)'),
 # off route
 'lem:selections-give-states': dict(status='none', origin='-', lean2=[], how='no map from Hamiltonian cycles back to states'),
 'rem:other-sums': dict(status='weaker', origin='project', lean2=['ColoredDual.sign_eq_I_pow_mul_phase_concrete', 'Pair.phase_eq_paperSign'], how='the identity i^J = i^-n eps is checked for every pair (B2 closed); the Taylor-coefficient, Laurent-polynomial and Li statements are not'),
 'rem:which': dict(status='weaker', origin='project', lean2=['IsAcyclic.perfectMatching_unique'], how='only "a tree has at most one perfect matching"; the image characterisation and injectivity are not stated (TODO T5 as first written was false)'),
 'rem:poly': dict(status='weaker', origin='upstream', lean2=[], how='group_sum_product is the factorisation with the phase after w = 1 + aX; the multivariate statement is not formalised'),
}

# primal and involution notes: status after the integration (exact | translation | weaker | none)
V2_NOTES = {
 'PT': 'translation', 'Pcircuit': 'translation', 'PL1': 'translation', 'PL2': 'translation', 'PL3': 'translation',
 'PL4': 'exact', 'PL5': 'exact', 'PL6': 'weaker', 'PL7': 'translation', 'PL8': 'translation', 'PL9': 'exact',
 'PL10': 'weaker', 'PL11': 'exact', 'PL12': 'exact', 'PL13': 'translation', 'PR14': 'none', 'PR15': 'weaker',
 'I:main': 'translation', 'I:disk': 'translation', 'I:objects': 'none', 'I:one': 'weaker', 'I:two': 'none',
 'I:fixed': 'none', 'I:path-crossings': 'none', 'I:walk': 'none',
}
V2_NOTES_LEAN2 = {
 'PL7': ['OppositeCycle.paperSign_partners_sum'], 'PL8': ['Pair.realSum_ne_zero', 'ColoredDual.forest_pair_real'],
 'PL3': ['Pair.sign_formula'], 'PR15': ['IsAcyclic.perfectMatching_unique'], 'I:one': ['OppositeCycle.paperSign_reverse'],
 'I:main': ['ColoredDual.forest_pair_real'],
}
INVOLUTIONS['I:path-crossings'] = dict(uses=['I:two', 'I:objects'], lean=[], rel='none', covered=False, main=None,
                                       note='added to the involution note after the blueprint; crossings of paths')

# five-column chart, version 2: the project declarations join the Lean column
WAYPOINTS_V2 = [
 ('statement', 'Thm 1.1, Cor 7.1', ['thm:main'], ['PT'], [], ['main', 'Duality.connected_complement_matching']),
 ('dual is a coloured triangulation', 'Sec 7, proof of Thm 1.1', ['lem:dual', 'eq:counts'], ['PL1'], [], ['make_coloredDual', 'Duality.simple_dual_edge', 'black_dual_card']),
 ('cycle = cut, forest => connected dual', 'Lemma 2.1; Sec 6.2', ['lem:duality.1', 'lem:duality.2', 'lem:connected'], ['Pcircuit'], [], ['Duality.circuit_cut', 'Duality.complement_connected']),
 ('target: acyclic selection => HC', 'Thm 2.2; proof of Thm 1.1', ['prop:target.1', 'prop:target.2'], ['PL12'], [], ['Duality.hamiltonian']),
 ('states and pairs', 'Sec 2', ['def:state', 'def:pair'], [], [], ['TriangleSystem.State', 'TriangleSystem.Pair']),
 ('a pair exists', 'Prop 3.1', ['txt:flow', 'prop:pair'], ['PL4'], [], ['ColoredDual.pair_nonempty', 'BMatching.two_matchings']),
 ('inside of a cycle', 'Sec 4 (one sentence)', ['txt:inside'], ['PL2'], [], ['region_euler', 'mixed_corner_on_boundary']),
 ('disk identity', 'Lemma 4.1', ['lem:disk'], ['PL5'], ['I:disk'], ['state_disk_delta']),
 ('outdegree at most one', 'inline in Lemmas 5.2, 6.1, 6.2', ['lem:outdegree'], [], [], ['CycleCoordinates.tail_orientation', 'OutOrientation.component_count']),
 ('sign', '(5.1) phase i^J', ['txt:delta', 'lem:sign'], ['PL3', 'PL7'], ['I:objects'], ['Pair.sign_formula', 'OppositeCycle.paperSign_reverse', 'Pair.sign_orient', 'ColoredDual.sign_eq_I_pow_mul_phase_concrete']),
 ('cancel cyclic Q_s', 'Lemma 5.2', ['lem:reversals', 'lem:cancel'], ['PL7'], ['I:one'], ['TriangleSystem.OppositeCycle.fixed_second_state_cancels', 'OppositeCycle.paperSign_partners_sum', 'Pair.sum_sign_eq_zero_of_no_good']),
 ('weights with positive steps', 'Lemma 5.3, (5.3)', ['txt:heights', 'lem:height'], ['PL6'], ['I:objects', 'I:path-crossings'], ['whiteCharge_cut_integral', 'ColoredDual.StateCycle.signed', 'Pair.weight_orient']),
 ('group by the cover', 'Sec 5.3', ['txt:D'], ['PL8'], ['I:two'], ['TriangleSystem.Pair.groupEquiv', 'Pair.group_sum']),
 ('nonvanishing', '(5.4)-(5.5), Prop 5.1', ['lem:difference', 'prop:good'], ['PL8'], ['I:fixed', 'I:main'], ['finite_difference_fin', 'Pair.realSum_ne_zero', 'ColoredDual.forest_pair_real', 'ColoredDual.forest_pair']),
 ('forest pair => spanning tree', 'Lemma 6.1, Sec 6.1', ['lem:partner', 'lem:good'], ['PL9'], [], ['ColoredDual.augQ_acyclic', 'ColoredDual.removed_acyclic']),
 ('selection from the tree', 'Sec 6.1 (rooting at y0)', ['lem:Y'], ['PL10'], [], ['tree_matching', 'IsAcyclic.perfectMatching_unique']),
 ('selection is acyclic', 'Lemma 6.2', ['prop:recover'], ['PL11', 'PL12'], [], ['ColoredDual.selected_forest', 'matching_cut_balance']),
 ('separating triangles', 'Sec 7, proof of Thm 2.2', ['lem:cap', 'thm:T'], ['PL13', 'PT'], [], ['cap_glue_connected', 'matching_strong']),
 ('construct a forest pair', '-', [], [], ['I:walk'], []),
]
