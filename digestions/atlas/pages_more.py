"""Page texts, continued (imported at the end of pages.py)."""
from pages import page, OA, LI, BT, RS, HERE, G2, G3, G4, G5, G6

# ---------------------------------------------------------------- linear algebra
page('rowdep', 'row dependence', 'Cancellation is a dependent set of rows', G2, r'''
Fix the second state $s$ and write a matrix with a row for each black face and a column for each non-root vertex.
The row of a face has two entries, at the ends of its opposite edge.
Expanding the determinant picks one end in every row and each column once, which is a partner $r$ for $s$.
If the opposite edges contain a cycle, the rows on the cycle add up to zero and the determinant vanishes. If they form three trees, one at each root, it is plus or minus one.
Having no cycle is not enough. When one tree holds two roots the determinant is zero, as for five states here.
This explains the cancellation, not why a good state exists.''',
     r'''Proved here and checked by a second model, which corrected the overall sign. Not read by a human. All twelve matrices are computed here.''',
     ['sum', 'involutions', 'determinant', 'matroids'],
     [RS + 'astra_referee-combinatorics/REPORT.md', BT + ', Proposition 2.1', HERE])

page('determinant', 'one determinant', 'One determinant is not enough', G2, r'''
It is tempting to put all states into a single determinant and evaluate it once.
The hexagonal prism shows why that fails. Its dual has three states, and its two good states carry opposite signs.
With every weight equal to one they cancel, so the evaluation is zero although good states exist.
The signs balance like this on every example.
The remedy keeps the weights as variables. The polynomial is then the coefficient, in the determinant of the matrix in (d), of the monomial that uses every black face once,
and anticommuting variables package the same extraction.
Either way the nonvanishing still has to come from the positive direction of pages 4 and 5.''',
     r'''The coefficient formula and the sign balance were proved in this project. A second model checked the formula and the prism example. The matrix in (d) is computed here. Not read by a human.''',
     ['polynomial', 'rowdep', 'dimers', 'produced'],
     [RS + 'fable_referee-determinants/REFEREE-dimers.md', RS + 'fable_referee-determinants/SIGNIFICANCE.md, Sections 1 and 3',
      RS + 'sol_route-algebra/REPORT.md (Grassmann form, unrefereed)', RS + 'opus_route-induction/PROOFS.md, Proposition 4.1 (signs balance)', HERE])

page('dimers', 'double dimers', 'Two matchings laid on top of each other', G2, r'''
A state is a perfect matching between black centres and non-root vertices. Lay two states on top of each other.
Where they disagree, their spokes alternate around closed curves, and forgetting the centres turns each curve into a cycle of $D$.
Physicists call this a double-dimer picture, and a pair is the case with no agreement, as in (a).
The method is good at counting such overlays with a determinant.
The trouble is in (b). Two states that agree on some faces leave doubled spokes. A doubled spoke bounds no disk, the disk identity has nothing to say about it,
and the determinant counts these overlays together with the pairs.
So the standard tools count too much, and the surplus terms have no sign control.''',
     r'''Proved in this project and checked by a second model, which confirmed a 9-vertex obstruction to the enlarged count. Not read by a human.''',
     ['pairs', 'determinant', 'pfaffian', 'trinity'],
     [RS + 'astra_route-dimers/PROOF.md', RS + 'fable_referee-determinants/REFEREE-dimers.md', HERE])

page('pfaffian', 'Heawood torus', 'Off the sphere: the Heawood graph on a torus', G2, r'''
The paper extends the theorem to cubic bipartite graphs with a Pfaffian orientation by quoting a structure theorem. A direct proof would rerun the argument on another surface.
The smallest test is the Heawood graph on a torus. Its dual is the complete graph on seven vertices.
No roots are removed, since seven black faces already match seven vertices. There are 24 states and 48 pairs, and every cycle of $D$ runs through all seven vertices.
Such a cycle bounds no disk, the walk around it sees black faces on the left seven times or once instead of three,
and the two partners of each state cancel. The signed sum is zero.
The Heawood graph is Hamiltonian, so only the method fails.''',
     r'''Computed in an unrefereed report of this project and recomputed here independently. The extension itself rests on published theorems. Not read by a human.''',
     ['disk', 'sum', 'hypotheses', 'open'],
     [RS + 'astra_route-pfaffian/REPORT.md', RS + 'astra_route-pfaffian/GSW-CHAIN.md', RS + 'astra_route-pfaffian/PROOFS.md', OA + ', Corollary 7.2', HERE])

# ---------------------------------------------------------------- order and optimisation
page('lattice', 'clock lattice', 'Twelve states under clock moves', G3, r'''
The twelve states of the running example form a lattice. One clock move turns the wedges around a single white face and raises the state by one unit of volume.
Every line in the diagram is one such move, and the shaded faces show the height gained so far.
A natural hope is that a fixed place in this order, the top or the bottom, always holds a good state.
Here both ends do, and six of the twelve states are good states.
In general the hope fails, and page 16 shows a triangulation whose extreme partnered state has a cycle.
The order describes how states are related. It does not find a good state.''',
     r'''Such lattices of matchings are classical. The order is computed here. The failure of the extremes was found in this project and checked by a second model. Not read by a human.''',
     ['heights', 'pairlattice', 'canonical', 'involutions'],
     [RS + 'astra_referee-combinatorics/REFEREE.md', RS + 'fable_route-combinatorics/', HERE + ' (lib.py: state_order)'])

page('pairlattice', 'cover lattice', 'The lattice of covers', G3, r'''
Forget which state of a pair is $r$ and which is $s$. What remains is a cover, the cycles of $D$ without direction, or equivalently the one corner that each black face leaves unused.
Covers form a lattice too.
The running example has two covers, so its lattice is the single step in (c).
Each cover has four orientations, and reversing a cycle moves between them without leaving the node.
The tempting conjecture said that the highest or the lowest cover always has an orientation that is a good pair.
In an 18-vertex example neither extreme has one, and a search over every root found no smaller example.''',
     r'''The correspondence with orientations of the spoke graph was proved in this project and checked by a second model, which also rebuilt the 18-vertex example and repeated the search. Not read by a human.''',
     ['lattice', 'involutions', 'canonical', 'open'],
     [RS + 'sol_referee-structure/REFEREE-graph-theory.md', RS + 'opus_conjectures/CONJECTURES.md, Section 3',
      RS + 'sol_referee-conjectures/REFEREE.md (18-vertex example and census through 18 rebuilt)', HERE])

page('canonical', 'extreme states fail', 'The extreme state can have a cycle', G3, r'''
The cheapest proof would name the state that works. The obvious candidates are the top and the bottom of the clock order, among the states that have a partner.
This 12-vertex triangulation defeats one of them. Its extreme partnered state, in (a), has a cycle among its opposite edges, so it gives no Hamiltonian cycle.
Mirror the picture and the same example defeats the other candidate.
Good states exist here, eight of them, but the rule passes over them all.
The lesson is narrow. It rules out these two choices and does not show that every explicit rule must fail. A rule that reads more of the structure could still work.''',
     r'''Found in this project. A second model checked it and corrected which mirror image defeats which rule. The witness and its nine states are recomputed here. Not read by a human.''',
     ['lattice', 'pairlattice', 'open'],
     [RS + 'fable_route-combinatorics/data/counterexamples.txt', RS + 'astra_referee-combinatorics/REPORT.md', HERE])

page('matroids', 'three conditions', 'Three conditions, and any two are easy', G3, r'''
A good state meets three conditions at once. Every black face has one wedge. Every non-root vertex is used once. The edges opposite the wedges form three trees, one at each root.
Each condition alone is a matroid constraint, the third after the three roots are merged into one vertex. Matroid intersection, a fast and standard method, meets any two of them together.
The panels show what goes wrong when one condition is dropped.
The table counts the choices that pass each pair of tests, against the six that pass all three.
Intersecting three matroids is hard in general, which is why no algorithm falls out of the proof.
This does not show that finding a good state is hard.''',
     r'''The three-condition description was proved in this project and checked by a second model. The witnesses and counts are computed here. Not read by a human.''',
     ['pairs', 'lp', 'rowdep', 'open'],
     [RS + 'sol_referee-structure/REFEREE-graph-theory.md', RS + 'fable_referee-determinants/REPORT.md', HERE])

page('lp', 'fractional point', 'The relaxed problem has a fractional corner', G3, r'''
Turn the three conditions into linear inequalities and allow fractional weights.
If every corner of the feasible region were a state, linear programming would find a good state.
The running example already has a bad corner. It puts weight one half on fourteen spokes that form one closed curve.
It is the average of two states, and it satisfies every forest inequality although one of those states has a cycle among its opposite edges.
So an optimal solution need not be a state, and a rounding rule would need a further argument.
This blocks the most direct route from the proof to a fast algorithm. Whether a different formulation works is open.''',
     r'''The point, its inequalities and the rank test that makes it a corner are computed exactly here. The general obstruction was checked by a second model. Not read by a human.''',
     ['matroids', 'open'],
     [RS + 'sol_referee-structure/REFEREE-graph-theory.md', HERE + ' (figs_order.py: lp_fig, seed 714)'])

# ---------------------------------------------------------------- trees
page('rainbow', 'rainbow tree', 'A tree that uses every black face once', G4, r'''
Give each black face its own colour. Deleting a spoke of a face opens a passage between two white regions, in the colour of that face.
A good state is then a spanning tree on the white faces that uses every colour once, with one passage at every non-root vertex.
First find a spanning tree with one passage per vertex. Rado's theorem does that with no signed sum.
Then repair the colours by exchanges, as in (a) and (b). An exchange keeps the tree, repeats one colour and loses another.
It is open whether exchanges that never increase the colour error always reach a good state.''',
     r'''The first step was proved in this project and is unrefereed. The descent is a conjecture. Its report checked every such tree up to 16 vertices and, with a theorem for part of the cases, up to 17. Not read by a human.''',
     ['recovery', 'matroids', 'trinity', 'open'],
     [RS + 'fable_referee-topology/RAINBOW.md', RS + 'fable_referee-topology/REPORT.md', RS + 'opus_route-topology/TOPOLOGY.md', HERE])

page('random', 'random trees', 'A random spanning tree with the right degrees', G4, r'''
Delete one spoke at each bounded black centre and one at each non-root vertex.
If the rest of the spoke graph is a spanning tree, the deleted spokes are a good state, and conversely.
A uniformly random spanning tree has those degrees with probability six in 6,670,188 here.
The hope was to tune edge weights until the prescribed degrees are the average, then show that the exact degrees have positive probability.
On the whole spoke graph the first half fails. The roots and the outer centre must keep every spoke, and no positive weights make that the average.
Measures on trees forced to keep those spokes are not excluded.''',
     r'''From a report of this project. Two further models checked the obstruction and narrowed it to weights on the whole spoke graph. The count and the sample are computed here. Not read by a human.''',
     ['rainbow', 'recovery', 'lp', 'open'],
     [RS + 'sol_route-probabilistic/REPORT.md', RS + 'sol_route-probabilistic/PROOFS.md', RS + 'sol_referee-covers/INTEGRATION.md (scope of the mean obstruction)',
      RS + 'opus_two-tree-packing/REFEREE.md', HERE + ' (figs_scope.py: random_fig, seed 2026)'])

page('trinity', 'three graphs', 'Three graphs inside one triangulation', G4, r'''
Mark a centre in every face of $T$, black and white, and join each centre to its three corners and to the centres across its three sides.
The result, in (a), contains three graphs.
Keep the black centres and their spokes, and the spoke graph of the proof remains. Keep the white centres and their spokes for its mirror.
Keep the joins between centres and what is left is the cubic graph $G$.
A state lives in the first, the tree on the white faces in the second, and the Hamiltonian cycle in the third,
which is why the proof keeps changing graphs.
Knot theorists know this structure as a trinity, and one report restates the theorem as a statement about hypertrees.''',
     r'''The drawing is computed here. The restatements are dictionaries, checked by a second model as dictionaries only. They prove nothing new. Not read by a human.''',
     ['dimers', 'recovery', 'rainbow', 'primal'],
     [RS + 'fable_route-categorical/CATEGORICAL.md, Section 2', RS + 'fable_referee-topology/REFEREE.md, part e', HERE])

# ---------------------------------------------------------------- cutting and induction
page('cuts', 'small cuts', 'What a small cut has to remember', G5, r'''
The proof splits $T$ along separating triangles and glues the answers.
Across a triangle, two of the three vertices lie in the same tree and are joined by an edge, so there are three patterns.
Prescribing that edge makes both sides agree, which is why the theorem carries a prescribed edge.
Across a cycle of length four the split of the vertices is not enough. A side must also report which cut vertices each tree joins through it.
On one such cycle here five splits occur, in six ways. The alternating split occurs with either tree joined through the inside.''',
     r'''Gluing along triangles is in the OpenAI paper, Section 7. The patterns are computed here from all Hamiltonian cycles of the two examples. An audit by a second model found the sixth. The general list for length four is in an unrefereed report. Not read by a human.''',
     ['pairs', 'recovery', 'induction', 'earlier'],
     [OA + ', Section 7', RS + 'fable_route-categorical/REPORT.md', RS + 'astra_route-pfaffian/REPORT.md (chord exception)',
      RS + 'sol_atlas-audit/AUDIT.md (six connection signatures; recomputed here with open sides)', HERE])

page('induction', 'induction', 'Induction by removing a vertex of degree four', G5, r'''
Euler's formula supplies a non-root vertex $x$ of degree four. Remove it and merge two opposite neighbours.
A good state of the smaller triangulation lifts back in one way, shown in (b) and (c).
If the lift is not a good state, rotate three wedges around one white face, as in (d).
Up to 16 vertices the rotation repairs 27,723 of 28,189 failing lifts. The other 466 need a rule nobody has found.
At 18 vertices some contractions have no good state that lifts directly.
The induction also needs a contraction that keeps a pair, which held in every test and is not proved.''',
     r'''A second model checked the lift and the rotation, reproduced the counts, and found the failures at 18 vertices. In 1.2 million contractions up to 18 vertices the number of good states never dropped. Both open statements are conjectures. Not read by a human.''',
     ['cuts', 'rainbow', 'open'],
     [RS + 'opus_route-induction/REPORT.md', RS + 'opus_route-induction/INDUCTION.md, Section 4', RS + 'opus_route-induction/PROOFS.md',
      RS + 'fable_induction-completion/REFEREE.md', RS + 'fable_induction-completion/REPORT.md', RS + 'astra_induction-lemmas/REPORT.md',
      RS + 'sol_atlas-audit/code/proposed.py (aligned layout proposed there; recomputed here)', HERE])

page('earlier', 'earlier methods', 'Where the older methods meet this proof', G5, r'''
Three older ideas end at the same object. Stein showed that a Hamiltonian cycle of $G$ is a split of the vertices of $T$ into two induced trees.
Kelmans strengthened the conjecture to cycles that avoid or use a prescribed edge, which makes gluing along small cuts possible. Feder and Subi colour the vertices of $T$, contract one class, and look for a spanning tree of faces.
A relaxed reading, tested in (c) and (d), asks for an induced tree whose vertices outside one class are pairwise non-adjacent. Their theorem asks more, a degree condition on omitted vertices.
None of the three supplies the step from a pair to a good state.''',
     r'''The three results are published. The translation of Feder and Subi was written in this project and is unrefereed. An audit of this atlas found the 10-vertex example, recomputed here. Not read by a human.''',
     ['recovery', 'cuts', 'produced'],
     [RS + 'astra_older-approaches/BRIDGES.md', RS + 'astra_older-approaches/SOURCES.md', RS + 'astra_older-approaches/NOVELTY.md', OA + ', Section 2',
      RS + 'sol_atlas-audit/outputs/fs-witness.json (the 10-vertex triangulation; every count on it recomputed here)', HERE])

# ---------------------------------------------------------------- scope
page('produced', 'produced cycles', 'Which Hamiltonian cycles the proof can produce', G6, r'''
The construction turns each good state into one Hamiltonian cycle, and different good states give different cycles.
It does not reach every cycle. The hexagonal prism has eight Hamiltonian cycles. Four of them avoid the prescribed edge, and the construction produces two.
The test for a given cycle runs the construction backwards. Orient the edges of $T$ that the cycle does not cross towards the roots and read off a state.
The cycle is produced exactly when that state is good.
The bottom row shows the four states. Two are good. In the other two a path of opposite edges joins two roots.
So counting good states undercounts Hamiltonian cycles, and sampling good states does not sample cycles uniformly.''',
     r'''Proved in this project and checked by a second model. Not read by a human. All eight cycles and the four recovered states are computed here.''',
     ['recovery', 'families', 'determinant'],
     [RS + 'astra_limits/REPORT.md', RS + 'sol_referee-structure/REFEREE-limits.md', RS + 'astra_limits/examples/prism_recovery.json', HERE])

page('hypotheses', 'hypotheses', 'What breaks when a hypothesis is dropped', G6, r'''
Each hypothesis enters at one place, and a small example shows the break.
Without bipartiteness the faces of the dual cannot be coloured black and white, already for the tetrahedron, so states are not defined.
Without 3-connectivity the theorem itself is false. The graph in (b) has 26 vertices, and removing two of them leaves three pieces, which no Hamiltonian cycle allows.
If a vertex may be used twice, the disk identity fails. In (c) a cycle of four arrows has left and right counts that cancel.
On a torus, cycles need not bound disks. The grid in (d) has pairs, but no state there can have a forest, because nine edges on nine vertices contain a cycle.''',
     r'''Written in this project and checked by a second model. Not read by a human. That 26 is the smallest size in (b) is a published result, not reproved here.''',
     ['disk', 'pairs', 'pfaffian', 'produced'],
     [RS + 'astra_limits/HYPOTHESES.md', RS + 'astra_limits/examples/', RS + 'sol_referee-structure/REFEREE-limits.md', HERE])

page('families', 'families', 'Two families, counted', G6, r'''
Counting on families shows how thin the set of good states can be.
The dual of a prism with $2m$ sides has $m$ states and exactly two good states, while the number of Hamiltonian cycles of the prism grows with $m$.
A nanotube of width four is a stack of rings. Its states multiply with every layer, 2, 5, 13, 34, and it still has exactly two good states.
So the proof finds a cycle in a set of states where almost none qualify, and the cycles it finds are a small part of all Hamiltonian cycles.
Both families have no separating triangles, so the rarity is not caused by gluing.''',
     r'''The counts in the chart are computed here by direct enumeration. The general formulas for these families come from a report of this project, and a second model rebuilt their proofs independently. Not read by a human.''',
     ['produced', 'lattice', 'open'],
     [RS + 'sol_counting-families/FAMILIES.md', RS + 'sol_counting-families/REPORT.md', RS + 'sol_referee-covers/REFEREE-families.md', HERE])

page('open', 'open doors', 'What is still open, and how far it was tested', G6, r'''
Six statements would give a proof that avoids the signed sum, a fast algorithm, or a count. None is proved.
A solid bar reaches the size up to which two independent programs checked every case. An outlined bar marks checks by one program, and a dashed line marks random samples.
The counting bound was checked twice on every root up to 22 vertices. The search without separating triangles reaches 24, but a second program repeated it only up to 16.
The crosses are statements of the same kind that failed, at the size of a known counterexample.
Three crosses sit at 33 vertices, beyond every exhaustive range, so passing all small cases is weak evidence.''',
     r'''The ranges are quoted from this project's reports and from the second models that repeated them. No census was rerun for this atlas. Panel (b) is computed here. Not read by a human.''',
     ['chain', 'rainbow', 'induction', 'pairlattice', 'canonical'],
     [RS + 'opus_conjectures/REPORT.md', RS + 'sol_referee-conjectures/REFEREE.md (bound replayed on 9,531,638 roots through 22; descent on all 24,744 pairs through 16; 33-vertex counterexamples)',
      RS + 'astra_cycle-covers/REPORT.md (23,824,742 roots through 24, no separating triangles)', RS + 'sol_referee-covers/REFEREE-covers.md (replayed through 16 only: 129 graphs, 3,374 roots)',
      RS + 'fable_referee-topology/REPORT.md (rainbow descent through 17, walk periodic at 38)', RS + 'opus_route-induction/REPORT.md',
      RS + 'fable_induction-completion/REFEREE.md (contractions through 18 and 19, direct lift refuted at 18)', RS + 'astra_referee-combinatorics/REPORT.md (12-vertex example)',
      RS + 'sol_atlas-audit/AUDIT.md (range ledger)', HERE + ' (panel b only)'])
