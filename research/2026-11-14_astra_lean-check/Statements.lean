import Devices.Concrete
import Devices.Outdegree
import Devices.TreeMatching

open OAI.Barnette OAI.Barnette.TriangleSystem OAI.Barnette.Network.ColoredDual

-- Devices.FiniteDifference (Lemma 4.7)
#check @Blueprint.finite_difference
#check @Blueprint.finite_difference_fin
-- Devices.LocalSign (Lemma 4.4, phase relation)
#check @OAI.Barnette.prod_sum_of_signs
#check @OppositeCycle.paperSign_reverse
#check @OppositeCycle.paperSign_partners_sum
#check @Pair.sign_orient
#check @Pair.sign_reverse_one
#check @Pair.sign_formula
#check @Pair.I_zpow_rawIndexSum
#check @Pair.phase_eq_paperSign
#check @Pair.paperSign_eq_I_pow_mul_phase
#check @Pair.three_dvd_rawIndexSum
#check @Pair.sign_eq_I_pow_mul_phase
-- Devices.RealSign (Lemmas 4.5, 4.6, Proposition 4.8)
#check @Pair.sum_sign_eq_zero_of_no_good
#check @Pair.weight_orient
#check @Pair.group_sum
#check @Pair.group_sum_card
#check @Pair.group_sum_lt
#check @Pair.realSum_ne_zero
#check @Pair.forest_pair_of_disk_circulation_real
-- Devices.Concrete (the Lean's concrete system)
#check @OAI.Barnette.Network.ColoredDual.sign_reverse_opposite
#check @OAI.Barnette.Network.ColoredDual.sign_orient_concrete
#check @OAI.Barnette.Network.ColoredDual.sign_formula_concrete
#check @OAI.Barnette.Network.ColoredDual.sign_eq_I_pow_mul_phase_concrete
#check @OAI.Barnette.Network.ColoredDual.forest_pair_real
#check @OAI.Barnette.Network.ColoredDual.realSum_ne_zero_concrete
-- Devices.Outdegree (Lemma 3.7) and Devices.TreeMatching
#check @OAI.Barnette.Devices.OutOrientation.card_edgeSet_add_sinks
#check @OAI.Barnette.Devices.OutOrientation.component_count
#check @OAI.Barnette.Devices.IsAcyclic.perfectMatching_unique
