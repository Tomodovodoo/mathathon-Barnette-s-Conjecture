# Proposed exposition outline

HUNCH editorial proposal. The main paper should explain existence with a prescribed edge avoided, using the supplied OpenAI route. The incidence-tree interpretation helps explain that route without requiring the stronger exact-obstruction or exchange-component theorems. An algorithmic sequel can retain those results after a separate audit. LIT references below are to OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, September 24, 2026, by section/result. C denotes the supplied constructive draft, used as an expository model rather than a certified extension.

Working title: *Hamiltonian cycles from incidence trees*. This title identifies the construction rather than announcing a new proof. Use the five-sentence exposition abstract in STYLE-GUIDE.md.

## 1. Degree two and connectivity

Reader's question: Why is a Hamiltonian cycle hard to find when every vertex has only three edges?

Begin with the two requirements. In a cubic graph a perfect matching's complement satisfies degree two, but may have multiple components. Use the cube's opposite square faces and a Hamiltonian cycle side by side, following C Figure 1. Define Hamiltonian cycle and Barnette graph in prose. State the prescribed-edge version once, with all graph hypotheses. Explain in one sentence that the extra prescription will let smaller solutions agree when glued.

LIT, O §1 and Corollary 7.1. The elementary equivalence between connected spanning degree-two subgraphs and Hamiltonian cycles is proved in DEPENDENCY-AUDIT.md. End with the question, "How can a construction enforce connectivity as well as degree two?"

## 2. A forest certificate in the dual

Reader's question: What object would certify both requirements at once?

Pass to T=G*. Explain why cubicity makes faces triangular and bipartiteness colors those faces black and white. State the target: select one side of every triangle, with the selected edges forming a spanning forest. The complementary dual has degree two because two sides remain at each face, and is connected by plane forest duality. Prove the short duality lemma here, where it is needed.

Explain the two induced trees and the prescribed edge as the form of certificate retained for gluing. Avoid presenting inducedness as a synonym for connectedness. LIT, O Lemma 2.1, Theorem 2.2 and §6.2. Show one small complete example of selected and unselected sides. At this point the forest is a target, not an object already constructed.

Finish by stating a conditional recovery proposition: the incidence tree constructed next yields such a selection. Give the conversion picture now; prove its acyclicity in Section 6 below. Label the deferred proof explicitly. This one forward reference is deliberate: it motivates the target without pretending to have established it.

## 3. Incidence matchings and why they come in pairs

Reader's question: How can we encode local choices without losing track of connectivity?

Choose the outer black face t0 and roots R. Define A and X; use one short Euler count to obtain |A|=|X|. Draw H by placing black centers and spokes, including the outer center. Define B by deleting roots and outer center. Introduce s only after explaining the desired deletion: one spoke at each bounded center and one at each nonroot. Such deletions are a perfect matching of B, equivalently a state s:A→X.

Define Q_s by suppressing the degree-two black centers after deletion. Explain the role of a disjoint mate r: its tails orient the opposite edges with outdegree one at nonroots and zero at roots. For a pair with Q_s acyclic, count edges against outdegrees to give one root per component, hence H−s a tree. LIT, O §5, Lemma 6.1 and §6.1. C Proposition 2.1 offers a useful fuller account, but the main proof need only establish the version it uses.

Keep one cube assignment, with the same labels used later. Do not suggest that the cube demonstrates difficult cyclic Q_s states if the chosen example is already a tree. End with two tasks: obtain any pair, then obtain one whose Q_s is acyclic.

## 4. An initial pair and a disk count

Reader's question: Why do the local incidence requirements have a solution, and what controls cycles?

First handle the no-separating-triangle case. Give the capacity-two/capacity-one network, cite integral flow, and prove its graph-specific cut inequality via planar density. Retain the root component, actual versus component faces, repeated boundary sides, and the small components. LIT, O Proposition 3.1. Announce that separating triangles will be handled by gluing in Section 7. Do not import C's weaker obstruction hypothesis unless its stronger proof is retained.

Then introduce the two directed edges in a black triangle, r(t)→s(t) in D and r(t)→u(t) in Q_s. The reader now needs a rule for how reversal affects signs. Define δ and prove the disk identity. Display the three counts together and explain the state-dependent count B_d=I+ℓ. LIT, O Lemma 4.1. Put the disk picture here, with roots outside the disk and only the relevant incidences marked.

These can remain two subsections because they answer different questions. If the section becomes long, split it into "An initial pair" and "The disk identity" rather than adding numbered micro-lemmas for every rearrangement.

## 5. Two groupings force a forest state

Reader's question: How can an existence argument rule out every cyclic second state?

State the forest-state proposition before defining the sum. Explain the intended contradiction: cyclic second states cancel, but the total is nonzero. Define weights depending only on s, then J and Z. Give the two-reversal table. Prove fixed-s cancellation first, retaining the choice of cycle from s alone and bijectivity after reversal.

Now ask why the total cannot vanish. Choose spoke circulations to order the two orientations of every D-cycle. Prove the positive circulation lemma and the orientation-preserving spoke detour. Group by undirected D, factor over cycles, and inspect the first potentially nonzero coefficient. Explain that minimum-cycle groups have the same phase and positive magnitudes; groups with more cycles do not contribute in that degree. LIT, O Proposition 5.1 and Lemmas 5.2–5.3.

Use the original finite exponential sum as the baseline because it supplies this route completely. A global signed-polynomial version may be substituted after checking the integer weights and sign convention against C Theorem 5.2. Do not present both derivations in the main line. A short remark can identify the alternative. No exchange graph or marked tokens are required for the baseline existence claim.

Exit with exactly the result needed: a pair with Q_s a forest. Do not announce a local improvement algorithm; cancellation has not supplied a monotone local move.

## 6. Recover the cycle

Reader's question: We have the promised incidence tree. How does it produce the selected forest in Section 2?

Take the complementary dual tree W_s on white faces, root it at the white face across the prescribed edge e0, and assign each edge to its child face. Convert each assigned deleted spoke to a selected triangle side; add e0. Explain separately why each black and each white face receives one side. LIT, O §6.1.

Prove acyclicity using the disk identity a second time. The selected-side count gives B_d−W_d=2ℓ−h, whereas triangle-side counting gives three times that face imbalance. The contradiction is with the nonzero disk sum, not with Euler's formula alone. Explain internal chords' cancellation. Add the prescribed edge only after showing the three roots are in different components. LIT, O Lemma 6.2.

Complete the degree/connectivity argument and obtain inducedness from the complementary Jordan curve. Finish the cube example using the same labels as Section 3. The reader now sees both ends of the construction, with no new naming scheme.

## 7. Gluing and completion

Reader's question: What happens when a separating triangle obstructs the initial pair argument?

Split along the triangle and prove that each cap inherits a compatible face color. Solve the piece containing t0 first. Its induced-tree partition gives one same-label edge on the shared triangle. Prescribe that edge on the second piece, align the labels, and glue each tree along a vertex or an edge. Explain why no edge joins strict interiors of opposite pieces, so inducedness survives. State the smaller-size induction measure. LIT, O §7.

Return to G and identify the omitted primal edge. This is the proof's conclusion, not an appendix. End after the theorem has been proved; optional consequences must not obscure completion.

## Optional separate part: an explicit construction

Reader's question: How would we find the certificate algorithmically, and what bound is proved?

If the coordinator wants the constructive theorem, add this part and revise the title/abstract accordingly. Give enumeration with connectivity and residual-matching prefix tests, prove no target prefix is pruned, then give the determinant count and its conversion from n to N. Treat the marked walk as an alternative after that algorithm, explaining its endpoint argument and strict decrease at restarts. C §§5.1 and 6 are the source assertions requiring a separate mathematical audit. Do not imply that the smaller enumeration bound applies to the marked walk.

## How to test this outline

Ask a reader to pause before each section and state the outstanding question. At the end of Section 3 they should know why two matchings are present. At the end of Section 5 they should know which reversal fixes s and why positivity survives the other grouping. At the end of Section 6 they should be able to name the separate reasons for degree two, connectivity, and inducedness. At the end of Section 7 they should know why the stronger facial prescription was necessary.

The outline earns its length only if those answers become easier. A page target should be set after the route, examples and readable figures are in place.
