# Independent sign calculation

PROVED-HERE. Fix an ordered pair in a triangle system, with the same cyclic corner order for the paper delta and Lean indexDelta. Let n be the number of faces, N the number of negative local signs, and t the sum of local signs. Each local sign is ±1, so t=n-2N and epsilon=(-1)^N=i^(n-t). If 3 divides t, write t=3J. Lean's phase is i^(t/3)=i^J, with exact integer division. Therefore

    epsilon / phase = i^(n-3J-J) = i^(n-4J) = i^n.

No cycle-count parity assumption is needed beyond the divisibility at this point. The disk identity supplies divisibility because t is the sum of the delta sums ±3 of the permutation cycles. This proves epsilon=i^n phase and agrees with ADJUDICATION.md.

For the closed formula let c be the number of cycles and c_plus count the ones with delta sum -3. Then t=3c-6c_plus, so

    2N = n-3c+6c_plus.

This implies n and c have the same parity. The difference between N and (n+c)/2+c_plus is -2c+2c_plus, an even integer. Hence epsilon=(-1)^((n+c)/2+c_plus). Reversing one such cycle negates every local delta on it; its odd length follows because its sign sum is ±3. Reversing k disjoint cycles multiplies the product by (-1)^k. The opposite-graph reversal likewise negates the changed local signs, and the disk identity makes their number odd. These are ordinary integer computations, independent of the submitted Lean proofs.

If geometric delta is the negative of Lean indexDelta at every face, paper epsilon=(-1)^n times the Lean product and the ratio is i^(-n). Thus a coherent reversed orientation still gives a constant. Independently reversing orders at only some faces is not the same comparison. The concrete orientation convention has to be translated coherently.

The finite-difference sign also agrees. With cycle count m, the formal exponent is (n+m)/2+m; the paper exponent is (n-m)/2. Their difference is 2m. The absolute cycle slope is the magnitude of the reversal step. In the formal hypotheses delta=-3 has positive slope, so step=-slope is negative: this reverses a counterclockwise cycle to clockwise. Reversing a clockwise cycle to counterclockwise has positive step, as in the current paper.

COMPUTED. `python -I research/2026-11-14_astra_lean-check/numerical.py` independently tests every ±1 word of lengths 0 through 18 with sum divisible by 3: 174,763 words. It also enumerates all incidence-bijection states and ordered partner pairs for every face rooting, allowing both colour classes as black, of the paper's running triangulation and the hexagonal bipyramid. It checks 112 and 24 pairs respectively. For each pair it constructs the permutation cycles itself, checks their delta sums are ±3, the closed sign formula, and the phase ratios in both global orientations. Output is numerical.json. This is not a census claim for all triangulations.

The same script enumerates all perfect matchings of the dual hexagonal prism containing the prescribed edge, checks connectedness of their 2-regular complements, recovers their states by orienting the selected dual forest towards the roots, and checks the full good-state condition. It finds four eligible Hamiltonian cycles but only two good recovered states. Two cycles have the same non-good recovered state. This independently refutes TODO T5. The first draft of this checker mistakenly tested only acyclicity for goodness, and failed the expected-count assertion. It was corrected to test one root per component as the paper requires. That diagnostic reinforces why B4 must not be silently discarded.
