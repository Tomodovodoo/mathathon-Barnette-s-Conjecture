import Devices.Concrete

open OAI.Barnette OAI.Barnette.TriangleSystem OAI.Barnette.Network.ColoredDual

-- Devices.FiniteDifference (Lemma 4.7)
#print axioms Blueprint.finite_difference
#print axioms Blueprint.finite_difference_fin
-- Devices.LocalSign (Lemma 4.4, phase relation)
#print axioms OAI.Barnette.prod_sum_of_signs
#print axioms OppositeCycle.paperSign_reverse
#print axioms OppositeCycle.paperSign_partners_sum
#print axioms Pair.sign_orient
#print axioms Pair.sign_reverse_one
#print axioms Pair.sign_formula
#print axioms Pair.I_zpow_rawIndexSum
#print axioms Pair.phase_eq_paperSign
#print axioms Pair.paperSign_eq_I_pow_mul_phase
#print axioms Pair.three_dvd_rawIndexSum
#print axioms Pair.sign_eq_I_pow_mul_phase
-- Devices.RealSign (Lemmas 4.5, 4.6, Proposition 4.8)
#print axioms Pair.sum_sign_eq_zero_of_no_good
#print axioms Pair.weight_orient
#print axioms Pair.group_sum
#print axioms Pair.group_sum_card
#print axioms Pair.group_sum_lt
#print axioms Pair.realSum_ne_zero
#print axioms Pair.forest_pair_of_disk_circulation_real
-- Devices.Concrete (the Lean's concrete system)
#print axioms OAI.Barnette.Network.ColoredDual.sign_reverse_opposite
#print axioms OAI.Barnette.Network.ColoredDual.sign_orient_concrete
#print axioms OAI.Barnette.Network.ColoredDual.sign_formula_concrete
#print axioms OAI.Barnette.Network.ColoredDual.sign_eq_I_pow_mul_phase_concrete
#print axioms OAI.Barnette.Network.ColoredDual.forest_pair_real
#print axioms OAI.Barnette.Network.ColoredDual.realSum_ne_zero_concrete
