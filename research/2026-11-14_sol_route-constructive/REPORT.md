COMPUTED. Built an executable incidence-matching package, recovery algorithm, separator gluing and worked JSON examples.
COMPUTED. All checked statements passed on 77 rooted runs, including all 55 plantri outputs through dual order 14.
PROVED-HERE. Derived a determinant coefficient formula for the signed sum, with an exponential coefficient-extraction step.
REFUTED. The naive single determinant fails on the hexagonal prism; two-matroid relaxation and white-tree rejection also have concrete failures.
LIT. The supplied constructive proof gives exponential-time polynomial-space search; this investigation does not produce a polynomial-time algorithm.

# Report

## Objective and delivery

COMPUTED. I implemented the proof objects and constructions in `workings/barnette_lab/`, with nine unit tests, a larger lemma-verification command, and JSON examples for the cube and truncated octahedron. The public `hamiltonian_cycle` function accepts an input graph and a prescribed edge and returns a cycle in the input labels. The named examples include both requested truncated polyhedra. Optional plantri supplies all small Eulerian triangulations; the dependency-free generator supplies a smaller non-exhaustive family.

COMPUTED. VERIFICATION.md maps the requested paper numbers to actual lemmas or equation numbers and states the exact finite coverage. DATA.md lists every data file, its producing command and the sample restrictions. ALGORITHMS.md gives the algorithmic conclusions and full arguments for the new determinant expression, the coefficient-extraction bottleneck, the state-sampling self-reduction and the local factorization obstruction.

## What was established

COMPUTED. The campaign covers 77 rooted instances with repetitions, all 55 unrooted plantri outputs through dual order 14 and named primal graphs through 48 vertices. It enumerates 1,040 states and 254 pairs. The exact disk identities, exchange signs, polynomial grouping, mate counts, incidence-tree criterion, determinant count, induced trees and final cycles pass in their recorded ranges. The Li implementation tests both its literal single-mark involutions and the set-of-marks extension in Appendix B. No checked paper statement was contradicted.

COMPUTED. A 20-vertex primal example contains a non-tree second state and exercises cancellation. The broader benchmark contains ten bad starting pairs and two marked phases that restart from four D cycles to two. The random and greedy tests all succeed within ten exchange moves, but the sample is far too small and biased to suggest a worst-case bound. A structured scaling family reaches 288 primal vertices and stays easy for enumeration.

PROVED-HERE. Subject to the supplied disk lemma, the signed polynomial equals a squarefree coefficient of an n by n determinant over a fixed algebraic number field. Coefficient extraction still needs an exponential procedure in the formula obtained here. Exact determinant extension counts do support uniform sampling of all incidence states. They do not by themselves sample tree matchings.

## What failed and why

REFUTED. Replacing coefficient extraction by setting all face variables to one fails on the hexagonal prism. The exact determinant is `5*y0*y1*y4*(-4*y0*y3-5*y1*y2+9*y2*y3)/64` at z=5/4. Its squarefree coefficient is 45/64, while its all-one evaluation is zero. Repeated use of a black face creates unwanted cycle-cover terms.

COMPUTED. Intersecting the face partition with the white graphic matroid can produce a spanning tree whose spokes repeat nonroots. The missing second partition is essential. Sampling white trees and rejecting those failures gave no accepted example in 100 trials on either larger named graph. These failed candidates are retained with explicit witnesses.

COMPUTED. The first official plantri download timed out. I compiled a hash-pinned 4.5 mirror after disabling Unix CPU timing. Downloaded source and binaries remain ignored; the reproducible setup script and provenance are committed. No other agent's files were edited or staged.

## What remains open

HUNCH. A different polynomial-size determinant or Pfaffian for the restricted tree sum could change the search complexity. The present coefficient formula does not supply one. The local phase cannot be separated into independent tail and head scalar factors, which blocks a simple product-of-incidence-determinants attempt but proves no general impossibility.

LIT. The complexity justified by the supplied constructive paper is deterministic polynomial-space exponential-time search. No polynomial bound follows for marked-walk path lengths, greedy descent, random-walk hitting time or determinant-state rejection. This report makes no hardness claim under the Barnette promise.

COMPUTED. Remaining verification limits include arbitrary simple spoke cycles, exhaustive outgoing choices beyond n=6, all roots of all generated graphs, and large marked state spaces. Region bound 3.3 was exhaustively checked only through dual order 10; density subsets have a larger finite range. Runtime tests do not verify asymptotic claims.

## Leads for others

PROVED-HERE. The coefficient determinant isolates the missing condition in one place: use each black face exactly once. It may help a determinant or tensor-network specialist decide whether planarity can remove that condition efficiently. The exact hexagonal-prism polynomial is a small regression test for any proposed formula.

COMPUTED. Figure and writing agents can use `workings/barnette_lab/examples/cube.json` and `truncated_octahedron.json`. They include rotations, colored faces, roots, states, a consistent pair, delta, J, spoke weights, Z coefficients, Q, white tree, P, both vertex classes and the cycle in dual-face and original-input labels.

## Three best next steps

1. CONJECTURE. Search for a family with exponentially few tree states among all incidence states. Test by exact determinants and complete tree-state counts on increasing separator-free plantri samples.
2. CONJECTURE. Bound the exchange distance or marked path length in terms of a structural parameter beyond cycle count. Test adversarial roots, altered positive-circulation trees and instances with many failed restart phases.
3. HUNCH. Investigate whether planar gadgets can extract the squarefree coefficient without exponential size. Require any proposed determinant or Pfaffian to reproduce the hexagonal-prism witness and partial-assignment self-reductions before claiming an efficient search.
