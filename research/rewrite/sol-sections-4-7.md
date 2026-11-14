# Cuts to the second half

Line numbers refer to `paper/main/barnette.tex`. Retain the disk identity and recovery proposition from the first half; the arguments below use both. Aim for five pages from pairs through the theorem, plus at most one page of remarks and references.

| Item and lines | Recommendation; target printed proof length |
|---|---|
| Opening explanations, 493–504 | Cut. Define pairs immediately. |
| Pair definition, 506–509 | Keep inline. Say “two incidence-disjoint states”; retain ordered pairs. Define the third corner only where needed. |
| Partner lemma, 532–543 | Keep its content within the cancellation argument; 4 lines. Outdegree classification is already available. Unique partners matter for the weighted identity, not for existence alone. |
| Directed cycle decomposition, 545–551 | Keep in 3 lines immediately before defining signs. Invoke bijectivity, distinct black faces and simplicity, without separately proving each degree count. |
| Reversals lemma, 566–581 | Absorb into the nonvanishing proposition. Two numbered operations, each one sentence; one shared justification that tails and heads are the same vertex set. No separate lemma. |
| Local sign and sign lemma, 583–608 | Keep definition and both conclusions; 5–6 proof lines. Delete motivational 584–585, explanatory 610–612 and the repeated triangle calculation at 602. |
| Cancellation lemma, 629–652 | Absorb into the nonvanishing proof; 3 lines. Keep the requirement that the selected cycle depends only on the second state. Delete 630–632 and 652 once this is stated correctly. |
| Heights, 662–688 | Keep the corner weights and reversal formula. Cut 663–668, connectivity explanation 670, alternative orientation description 674, and reminder 679. Define fixed simple dual paths in one sentence. |
| Height proof, 690–709 | Keep the intersection-number argument; 6–8 lines. Delete the four-case narration 697–702, replacing it with the local crossing rule below. |
| Nonvanishing preamble, 719–736 | Delete, except define the minimum number of cycles at its first use. The proof itself explains the grouping. |
| Finite-difference lemma, 738–752 | Absorb its identity into the nonvanishing proof. Standard polynomial finite differences, not a new named lemma; 1 line of justification. |
| Pair gives good state, 754–779 | Keep as the principal proposition; 15–18 proof lines including cancellation and finite differences. Delete 763–766 in favour of “a fixed undirected cycle decomposition admits exactly its independent cycle orientations.” Retain the common-sign calculation. |
| Warning about minimum, 781–782 | Cut; choosing the minimum and the vanishing formula already explain this. |
| Worked example, 806–812 | Cut. It repeats the proof and table. |
| Other sums remark, 843–851 | Cut from the proof. Retain at most one source-comparison sentence in closing remarks. No Laurent-polynomial digression. |
| Incidence graph/network, 855–867 | Keep in the first-pair proof, compressed to 4 lines including the cut inequality. Invoke Ford–Fulkerson integral max-flow min-cut, *Maximal flow through a network* (1956), already cited as Ford1956. |
| Separating triangle definition, 870 | Move before the first-pair proposition, inline. |
| First-pair proposition, 872–913 | Keep; 20–24 proof lines. This density estimate is substantive, not a standard planar edge bound. Replace 879–886 by the single equivalence between the cut inequality and density. Compress component reduction and small cases to 2 lines. Replace 894–899 by “Every triangular face of H is a face of T, since no triangle separates.” Keep the parity argument for boundary lengths 4 and 5. |
| Pieces/cap definition and cap lemma, 925–939 | Absorb into induction; 3 lines. Keep signed boundary count 934–935. Delete the separate checks of connectivity, simplicity, size and inherited face colours, 936–938. |
| Dual theorem and induction, 950–979 | Keep theorem; 9–12 proof lines. Replace the cycle-following argument by the two-tree gluing proof below. |
| Gluing commentary, 981–983 | Keep at most the Kelmans attribution and one sentence translating to a three-edge cut. Avoid repeating why the edge is prescribed. |
| Main theorem proof, 985–990 | Keep as 2 lines or conclude the dual theorem proof with this translation. |
| Source comparison, 994–1001 | Reduce to 3 sentences, as specified below. |
| Cycles obtained, 1003–1013 | Optional closing paragraph; 4–5 lines. State the exact good-state criterion and injectivity, justified by uniqueness of a perfect matching in a tree. Delete the enumeration at 1011 and retain at most the prism counterexample. |
| Hypotheses, 1015–1047 | Keep a compact four-row table of counterexamples, with citations. Delete the genus calculation, proof-mechanism commentary, both connectivity proofs and NP-completeness aside. |
| Pair criterion, 1049 | Optional one sentence citing Anonymous2026, Theorem 1.2. Delete minimality and exhaustive enumeration. No-separating-triangle is an intermediate sufficient assumption, not a hypothesis of the theorem. |
| Polynomial, 1051–1061 | Cut entirely. It repeats the nonvanishing argument and introduces unused variables. |
| Algorithms, 1063–1066 | Keep two sentences, citing the constructive manuscript, Theorem 1.1 and Section 6. Its bound is a polynomial times 3^{N/4}, with N the primal vertex count. Do not turn the exponent into a dual-vertex bound. |
| Consequences/questions, 1068–1073 | Keep Pfaffian consequence with Gorsky–Steiner–Wiederrecht, Theorem 4.16, and OpenAI, Corollary 7.2; keep the arbitrary-two-edge question. Delete the decomposition explanation at 1073; it belongs to the cited theorem. Common-face strengthening needs only a sentence and citation. |
| Formal verification, 1075–1079; companion notes, 1081–1084 | Cut all. These paragraphs are repository inventory and checking history. |
| Bibliography, 1086–1087 | Keep references actually cited after compression. Remove revision hashes, checking annotations and publication-timeline detail from rendered entries; retain identifying publication data. |

## Replacement arguments

For the partner/cancellation step:

“Orient the edge opposite s(t) from r(t) to the third corner. Every nonroot has outdegree one and every root outdegree zero; hence an acyclic component is a tree with one root. If s is good, these orientations toward the roots determine its unique partner. Otherwise, fix a cycle of Q_s and reverse its orientation by replacing r(t) by the third corner on that cycle. This preserves s and reverses an odd number of local signs, so all terms with second state s cancel.”

For the sign calculation:

“Either reversal negates each local factor on its cycle, whose length is odd by the disk identity. A directed D-cycle of length h has (h+3)/2 negative factors counterclockwise and (h−3)/2 clockwise. Multiplying over the cycles gives ε=(-1)^{(n+c)/2+c⁺}.”

For heights:

“After reversing C to counterclockwise, the change at a face t on C is κ_y(t,r(t))−κ_y(t,s(t)). By the definition of κ this is +1 for a crossing of C from inside to outside, −1 for the reverse crossing, and zero otherwise. Summing along the dual path telescopes to the indicator that y lies inside C, since its endpoint t₀ lies outside. Summing over white faces gives Δω=L(C)>0 by the disk identity.”

For the end of nonvanishing, following cancellation:

“Group pairs by their undirected D-edges and let m be the minimum number of cycles. A class with c cycles consists of their 2^c independent orientations. Writing x_i=1 for counterclockwise orientation, its contribution to Σ=∑εω^m is

    (-1)^{(n+c)/2} ∑_{x∈{0,1}^c} (-1)^{∑x_i}(ω₀+∑x_i L_i)^m.

The c-fold finite difference is zero for c>m and equals (-1)^m m!∏L_i for c=m: expansion leaves only the term containing every x_i. Consequently Σ=(-1)^{(n−m)/2}m!∑_{classes with m cycles}∏L_i≠0, since all L_i>0. Cancellation therefore leaves a good state.”

For gluing:

“On either side of a separating triangle, the signed boundary count is three times the black-minus-white face count. Its three summands are ±1 and thus agree; cap each piece with the opposite colour. Apply induction first to the piece containing t₀, obtaining P₁, then to the other piece with the selected cap edge xy prescribed, obtaining P₂. Their union is a selection containing e₀. In each P_i, the component containing x,y is a tree containing xy, and the other is a tree containing z, by the two-induced-trees characterization. The two xy-trees meet exactly in xy and the two z-trees exactly in z. Their unions are disjoint trees, so P₁∪P₂ is acyclic.”

Hall's theorem on the original incidence graph proves only one state. Cloning both vertex classes permits both matchings to use the same original incidence and does not prove a pair exists. A Hall gadget can enforce incidence capacity one, but merely encodes the present flow network. Keep the integral-flow proof: neither König's theorem nor Hoffman's circulation theorem shortens it. The density inequality is the essential additional input, not ordinary Hall's neighbourhood inequality.

## Notation, displays and illustrations

Delete “partner”, “second state” as separately announced terminology; r and s suffice. Delete r_s, K_s and “cover” by saying unique partner, fixed cycle and undirected cycle decomposition locally. Delete J, Π, w, ξ and all polynomial monomial notation with their remarks. Define u(t), L(C), ω₀ and c⁺ immediately where used. Keep δ, ε, κ and ω; η can disappear if the crossing calculation is stated directly for the sum over white faces. Keep b(U) distinct from face counts within a component.

Put 590, 677 and 883 inline. Keep the cancellation/nonvanishing identity displayed, but combine 771 and 776 into its single final formula. Replace the standalone finite-difference display by the class calculation above. The two reversal operations deserve a two-item list, not a floating comparison table.

Cut Figures 07-pair-D, 10-cancellation and 06-flow, and Tables reversals and pairs. The eight-pair table earns no space beside the argument. Keep the local-pair diagram only if the earlier corner diagram is removed; caption: “The two orientations r→s and r→u define D and Q_s.” Keep at most one of heights and groupings, preferably groupings with numerical detail removed; caption: “Independent cycle reversals form a cube of orientations; fixed-second-state cancellation joins different cubes.” Gluing is optional; caption: “The two selected forests glue along one edge and one vertex.”

## Closing budget and mathematical cautions

Use at most one page: three sentences locating OpenAI's proof, Li's primal presentation and the constructive manuscript; one short paragraph on cycles produced; four counterexamples in a compact table; algorithmic bound and two open questions. Cite Tutte, Georges–Kelmans, the bipyramid radial graph and the three-branch cube construction without elementary connectivity proofs. Omit smallest-order claims.

No mathematical error was found in the retained argument. Preserve the nonseparating assumption precisely at 894–898, parity at 905, dependence only on s at 645, and minimality of m. These are essential qualifications. The outer-face convention is necessary throughout the height proof. The empty-pair case must be excluded before defining m.

Order and budget: first pair plus planar density, 1.25 pages; pairs, reversals and signs, 0.75; height construction, 0.75; cancellation and nonvanishing proposition, 1; separating triangles and theorem, 0.5; one optional diagram, 0.5; closing remarks, at most 1; references, approximately 0.5. Total about six pages, with only three substantive headings.
