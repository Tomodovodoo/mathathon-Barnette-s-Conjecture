# Status of the primal reconstruction

All thirteen lemmas and Theorem T have full informal proofs in PRIMAL-PROOF.md. PROVED-HERE means that the proof is written there, not that a new formalisation has been checked. LIT identifies the supplied papers. COMPUTED applies only to the finite ranges below. The independent Fable referee returned FOLLOWS with corrections. Those corrections are incorporated; human review is pending.

The Lean source was read directly in research/2026-11-14_opus_lean-formalisation/upstream/openai-math/lean/OAI/Combinatorics/Hamiltonian/, commit `4eaee87548250b2682affda7d05d947c05554bae`. Actual declaration headers are saved in the research folder's LEAN-EXTRACTS.md. The previous agent's successful build is reported in its REPORT.md; I did not rerun that build and do not claim this prose is machine-checked.

The categories requested in the brief are not exclusive. (i) means a primal restatement or a stated specialization of the cited Lean lemma. (ii) means a numbered statement in a supplied paper. (iii) means the proof or formulation is supplied here. Full namespaces start with `OAI.Barnette`. Network lemmas below are under `Network`, and `ColoredDual` lemmas under `Network.ColoredDual`, unless stated otherwise.

| Claim | Category and mathematical status | Exact source and difference | Numerical checks by this checker |
| --- | --- | --- | --- |
| Lemma 1, setup | (iii) PROVED-HERE; counts also (i) | `ColoredDual.cubic_cards`, Matching.lean:477; `ColoredDual.nonroots_card`, BMatching.lean:341. `make_coloredDual`, ThreeCuts.lean:101, supplies simple dual, triangles and their orientation. This note uses the map rules instead. | All 270 rootings: colour balance, three distinct faces at each vertex, incidence-part balance. |
| Lemma 2, circuits, shores, Euler, no pinch | (i), (iii) PROVED-HERE | `Duality.circuit_cut`, FlowCircuits.lean:71; `Bond.connected_shore`, Bonds.lean:163; `region_euler`, DiskRegions.lean:252; `mixed_corner_on_boundary`, StateDisk.lean:129. `Duality.circuit_cut` is one direction only; `Duality.bond_of_circuit`, Bonds.lean:109, supplies minimality. The converse used in recovery is proved here; Lean instead uses kernel duality. Lean does not start from a drawing. | 442 arbitrary bonds on graphs of at most 12 vertices; also every state circuit tested below. |
| Lemma 3, coherent orientation | (iii) PROVED-HERE | `Duality.circuit_cut`; `cycle_cut_scalar`, StateDisk.lean:416; `blackDelta_cut`, StateDisk.lean:390. There is no single Lean counterpart. `ColoredDual.oriented` and `Triangle.index_delta`, TriangleSystem.lean:291, supply algebraic coherence; the cited scalar and black-delta results presuppose the cycle flow. Here the rotation-system coherence is proved. | Signed delta-sum and slope tested on 1,140 pair-related circuit occurrences and 248 further arbitrary-choice state-circuit occurrences. |
| Lemma 4, pair existence | (ii), (iii) PROVED-HERE and LIT | Li, Lemma 9, Claim 12 and Theorem 10; OpenAI, Proposition 3.1. Conclusion agrees with (i) `ColoredDual.pair_nonempty`, BMatching.lean:403. Proof differs: primal minimal deficit and integral max-flow rather than the Lean density/Hall route. Balance and the outside white endpoint are written out. | Exact capacity deficits on 96,640 face subsets across 270 rootings; pair existence agrees with the capacity test, and every graph without nontrivial 3-cuts has a pair for every root. |
| Lemma 5, four-count identity | (i), (ii), (iii) PROVED-HERE and LIT | `state_disk_count`, StateDisk.lean:260; `disk_boundary_imbalance`, :428; `state_disk_delta`, :442. OpenAI, Lemma 4.1. The extra identity W=B+1 follows from the colour count. | All four equations, root exclusion, mixed faces, signed delta and positivity checked on 1,140 pair-related and 248 arbitrary-choice circuit occurrences. The latter exhaust all outgoing choices for all states on graphs of at most 12 vertices in this input family. |
| Lemma 6, flow potentials | (i), (iii) PROVED-HERE | `boundary_of_sum_zero`, Circulation.lean:154; `whiteCharge_cut_integral`, :208; `white_positive_of_boundary`, :227; `ColoredDual.StateCycle.signed`, ColoredDual.lean:183. Lean uses real weights; integer paths here are a specialization. Outgoing divergence here is the negative of Lean's boundary convention. | Local potential consistency at every nonroot black vertex of all rootings; slope equals signed white count on all 1,388 tested state-circuit occurrences. |
| Lemma 7, real-sign cancellation | (iii) PROVED-HERE; same cancellation as (ii) | OpenAI, Lemma 5.2; local determinant referee SIGNIFICANCE.md, Section 2. Lean's `TriangleSystem.OppositeCycle.fixed_second_state_cancels`, PairPhases.lean:91, uses a different phase, so this exact real-sign statement is not labelled machine-checked. | Every partner coefficient computed; two cyclic second-state occurrences, each with its explicit partner reversal and sign change. |
| Lemma 8, nonvanishing | (iii) PROVED-HERE; conclusion (i), (ii) | `TriangleSystem.Pair.forest_pair_of_disk_circulation`, PairPolynomials.lean:423; OpenAI, Proposition 5.1. The linear products follow Lean; the real prefactor is the local determinant referee's refinement. | 216 nonempty rooted pair spaces: complete exact polynomial and predicted lowest coefficient agree. No assertion about empty pair spaces. |
| Lemma 9, recovery tree | (i), (iii) PROVED-HERE | `ColoredDual.removed_acyclic`, Matching.lean:330; `remainder_connected`, :342; `remainder_black_degree`, :444; `remainder_independent`, :487. Uses the partner to prove one root per component. | All 1,908 forest-state/root-edge recoveries: connectedness, tree edge count and degrees. |
| Lemma 10, matching | (i), (iii) PROVED-HERE | Constructive specialization of `tree_matching`, ForestMatching.lean:51, and `ColoredDual.recovery_matching`, :226. Lean uses Hall; this note roots the existing tree. Li, Claim 31 gives the related explicit selection. | All 1,908 recoveries: each vertex covered once; prescribed edge selected. |
| Lemma 11, matching cut balance | (i), (iii) PROVED-HERE | `matching_cut_balance`, ForestMatching.lean:176, with exactly the same cubic, bipartite and matching hypotheses. | 4,196 cut-side tests over all 988 primal perfect matchings of the 16 input records. Includes the empty-boundary full-vertex-set case. |
| Lemma 12, connected complement | (i), (iii) PROVED-HERE | `ColoredDual.selectNet_forest`, ForestMatching.lean:307; `selected_forest`, :338; `recover_connected_complement`, :375. General statement: any state and any compatible perfect matching, with no partner or forest hypothesis. | All 1,908 recoveries: selected links acyclic, complement connected and degree two. |
| Lemma 13, caps and gluing | (i), (ii), (iii) PROVED-HERE and LIT | Li, Appendix C and Claim 36. `cap_threeConnected`, ThreeCuts.lean:230; `cap_simple`, :352; `cap_cubic`, :360; `cap_coloring`, :381; `cap_glue_matching`, Gluing.lean:94; `cap_glue_connected`, :167. `cap_duality`, CappedDuality.lean:148, supplies the cap duality replaced here by map contraction. Proof keeps 3-edge-connectivity throughout. | 278 three-edge cuts checked, including 8 nontrivial ones; 16 caps and 172 compatible pairs of cap Hamiltonian cycles checked. |
| Theorem T | (i), (ii), (iii) PROVED-HERE and LIT | `Duality.connected_complement_matching`, Gluing.lean:294, interpreted on the face incidence relation; `main`, Main.lean:47 for the final conjecture. OpenAI, Theorem 1.1 and Corollary 7.1; Li, Theorem 3. | Independent enumeration of all perfect matchings confirms edge avoidance for every input graph and every edge, including graphs where some rooted incidence pair spaces are empty. |

## Exact finite range

COMPUTED. Command, from the repository root:

```powershell
python research/2026-11-14_astra_primal-proof/check_primal.py --max-order 20 > research/2026-11-14_astra_primal-proof/check.log
```

The input is the named cube plus the lab's plantri generator for 6 through 12 face labels. After converting generated inputs to cubic graphs, every proof object is rebuilt from the primal graph. There are 16 graph records, 15 generated classes with one repeated cube, orders 8 through 20, and 270 rootings. Both choices of colour class occur because each vertex is used as root and its class is then named black. The class census is what the existing plantri binary reports; this agent does not independently certify the generator's completeness. `outputs/summary.json` lists every input graph by its edges, removing dependence on a census claim.

There are 1,722 states and 640 ordered pairs. Exactly two rooted state occurrences exhibit cancellation. The 20-vertex worked example has nine states and ten ordered pairs. Its polynomial is $4z+9z^2-2z^3-9z^4-2z^5$. The cube's is $-z$. Potential shifts and embedding orientation can change the displayed polynomial, so use the exported rotation/faces and weights when reproducing these numbers.

The checker does not test an arbitrary theorem quantifier by finite enumeration. It does not formally verify its own graph library, prove the numerical census complete, or rebuild Lean. The audit does not use a numerical check to discharge a mathematical obligation.


## Phase comparison, adjudicated

PROVED-HERE, and adjudicated independently in research/2026-11-14_opus_cross-audit/ADJUDICATION.md. The referee's M4 (research/2026-11-14_fable_referee-primal/LEAN-MATCH.md) said the note's real sign and Lean's phase differ by a factor depending on the number $c$ of circuits. The revision said the factor is the constant $i^n$. The revision is right.

For a pair, let $t=\sum_b\delta(r(b),s(b))$. The selected edges split into $c$ state circuits with delta-sums $\pm3$ (Lemma 5), so $3\mid t$. The real sign is a product of $n$ signs with sum $t$, hence $\varepsilon=i^{n-t}$. Lean's phase is `phase (rawIndexSum r s)` $=i^{t/3}$ (PairPhases.lean:9 and :31; Lean's integer division is exact here). With Lean's corner order equal to ours the ratio is $i^{n-4t/3}=i^n$. With the opposite corner order Lean's sum is $-t$ and the ratio is $i^{3n}=i^{-n}$. Either way it is one constant for the rooted graph, so with the same weights $Z_{\rm real}=i^{\pm n}Z_{\rm Lean}$.

The referee's closed forms are correct: with $c_+$ circuits of delta-sum $-3$ and $c_-$ of delta-sum $+3$, $\varepsilon=(-1)^{(n+3c)/2}(-1)^{c_-}$ and Lean's phase is $i^{c_--c_+}$, so the ratio is $(-1)^{(n+3c)/2}i^c$. The exponent is an integer because every circuit is odd, so $n\equiv c\pmod 2$. The error was the last step: $(-1)^{(n+3c)/2}=i^{n+3c}$, so the ratio is $i^{n+4c}=i^n$. Changing $c$ by two flips both factors.

COMPUTED, research/2026-11-14_opus_cross-audit/scripts/phase_ratio.py: all 297 Eulerian triangulations with 6 to 16 vertices from the lab's plantri (`-b -a`), plus the running example as a separate record, both colour classes as black, every black root, every ordered pair. 7,890 rooted instances, 24,856 pairs, no failure. 295 rooted instances contain pairs with two different circuit counts ($\{1,3\}$ or $\{2,4\}$); the ratio is the same for both. With equal random integer weights the two polynomials agree coefficientwise up to $i^n$. All 2,780 rooted instances without a pair come from triangulations with a separating triangle, as Lemma 4 requires.

Remarks 14 and 15 are new informal proofs in PRIMAL-PROOF.md, not claims about new Lean declarations. The revision's finite checks and build results are recorded in research/2026-11-14_astra_primal-revision/REPORT.md.


## Revision checks

COMPUTED. The dedicated revision checker exhausts all roots and states on the plantri -ba inputs at each indicated number of dual vertices, equivalently faces of G. It checks every cyclic second state with a partner, every circuit reversal, and the constant phase normalization for every ordered pair. This extends Lemma 7 coverage, not the full all-bonds census.

| Faces of G | Graphs | Roots | States | Cancelling states | Reversals | Phase checks |
| --- | --- | --- | --- | --- | --- | --- |
| 15 | 57 | 1,482 | 23,946 | 72 | 144 | 4,816 |
| 16 | 185 | 5,180 | 103,488 | 235 | 470 | 16,648 |
| Current 13-face running example | 1 | 22 | 264 | 4 | 8 | 112 |

No assertion failed. Commands and JSON outputs are in research/2026-11-14_astra_primal-revision/. The figure check script independently rebuilds the two illustrated primal rotation systems, checks states and pairs, all four disk counts, path-flow divergences and slopes, the recovery tree, matching and cycle, and the separate three-cut example. Fifteen PDF pages and all eight standalone figure renders were inspected. No new Lean build was run.
