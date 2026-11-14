"""Page texts, continued (imported at the end of pages.py)."""
from pages import page, OA, LI, BT, RS, HERE, G2, G3, G4, G5, G6

# ---------------------------------------------------------------- linear algebra
page('rowdep', 'row dependence', 'Cancellation is a dependent set of rows', G2, r'''
Fix the second state $s$ and write a matrix with one row for each black face and one column for each non-root vertex.
The row of a face has two entries, at the two ends of its opposite edge.
Expanding the determinant picks one end in every row and each column once, which is exactly a partner $r$ for $s$.
So the determinant adds up the partners of $s$ with signs.
If the opposite edges contain a cycle, the rows on the cycle add up to zero and the determinant vanishes. If they form a forest, the determinant is plus or minus one.
This explains the cancellation. It does not show that any state has a forest.''',
     r'''Proved in this project and checked by a second model, which corrected the overall sign. Not read by a human. Both matrices are computed here.''',
     ['sum', 'involutions', 'determinant', 'matroids'],
     [RS + 'astra_referee-combinatorics/REPORT.md', BT + ', Proposition 2.1', HERE])

page('determinant', 'one determinant', 'One determinant is not enough', G2, r'''
It is tempting to put all states into a single determinant and evaluate it once.
The hexagonal prism shows why that fails. Its dual has three states and two good states, and the two good states carry opposite signs.
With every weight equal to one they cancel, so the evaluation is zero although good states exist.
The signs always balance in this way, on every example.
The remedy keeps the weights as variables. The polynomial is then the coefficient, in a larger determinant, of the monomial that uses every black face once,
and anticommuting variables package the same extraction.
Either way the nonvanishing still has to come from the positive direction of pages 4 and 5.''',
     r'''The coefficient formula and the sign balance were proved in this project. A second model checked the formula and the prism example. Not read by a human.''',
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
The smallest test is the Heawood graph, drawn on a torus. Its dual is the complete graph on seven vertices with fourteen triangles.
Without roots there are 24 states and 48 pairs, and every cycle of $D$ runs through all seven vertices.
Such a cycle does not bound a disk, the walk around it sees black faces on the left seven times or once instead of three,
and the two partners of each state cancel. The signed sum is identically zero.
The Heawood graph is Hamiltonian, so the conclusion survives and only this method fails.''',
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

page('pairlattice', 'pair lattice', 'The lattice of cycle covers', G3, r'''
Forget which state of a pair is $r$ and which is $s$. What remains is a cycle cover, or equivalently the one corner that each black face leaves unused.
Covers form a lattice too, and a step up raises the cover over some white faces.
The running example has two covers, so its lattice is the single step in (c).
Each cover has four orientations, and reversing a cycle moves between them without leaving the node.
The tempting conjecture said that the highest or the lowest cover always has an orientation that is a good pair.
This project tested it. It fails first at 18 vertices, where both extremes lack one.''',
     r'''The correspondence with orientations of the spoke graph was proved in this project and checked by a second model. The 18-vertex failure comes from an unrefereed report. Not read by a human.''',
     ['lattice', 'involutions', 'canonical', 'open'],
     [RS + 'sol_referee-structure/REFEREE-graph-theory.md', RS + 'opus_conjectures/CONJECTURES.md, Section 3', HERE])

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
A good state meets three conditions at once. Every black face has one wedge. Every non-root vertex is used once. The edges opposite the wedges form a forest.
Each condition alone is a matroid constraint, and matroid intersection, a fast and standard method, meets any two of them together.
The three panels show what goes wrong when one condition is dropped, each on the running example.
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
So the relaxed problem has fractional corners and rounding it fails.
This blocks the most direct route from the proof to a fast algorithm. Whether a different formulation works is open.''',
     r'''The point, its inequalities and the rank test that makes it a corner are computed exactly here. The general obstruction was checked by a second model. Not read by a human.''',
     ['matroids', 'open'],
     [RS + 'sol_referee-structure/REFEREE-graph-theory.md', HERE + ' (figs_order.py: lp_fig, seed 714)'])

# ---------------------------------------------------------------- trees
page('rainbow', 'rainbow tree', 'A tree that uses every black face once', G4, r'''
Give each black face its own colour. Deleting a spoke of a face opens a passage between two white regions, in the colour of that face.
A good state is then a spanning tree on the white faces that uses every colour once, with one passage at every non-root vertex.
So the proof splits in two. First find a spanning tree with one passage per vertex. Rado's theorem does that with no signed sum.
Then repair the colours by exchanges. One exchange is shown in (a) and (b). It keeps the tree and the vertices, repeats one colour and loses another.
It is open whether exchanges that never increase the colour error always reach a good state.''',
     r'''The first step was proved in this project and is unrefereed. The descent survived all 34.8 million such trees up to 16 vertices and remains a conjecture. Not read by a human.''',
     ['recovery', 'matroids', 'trinity', 'open'],
     [RS + 'fable_referee-topology/RAINBOW.md', RS + 'fable_referee-topology/REPORT.md', RS + 'opus_route-topology/TOPOLOGY.md', HERE])

page('random', 'random trees', 'A random spanning tree with the right degrees', G4, r'''
Delete one spoke at each bounded black centre and one at each non-root vertex.
If the rest of the spoke graph is a spanning tree, the deleted spokes are a good state, and conversely.
So a good state is a spanning tree with a prescribed degree at every point.
A spanning tree chosen uniformly at random has those degrees with probability six in 6,670,188 here.
The hope was to tune edge weights until the prescribed degrees are the average, then show that the exact degrees have positive probability.
The first half fails. The roots and the outer centre must keep every spoke, and no positive weights make that the average.
Writing the signed sum as a difference of two positive measures restates the proof and does not replace it.''',
     r'''From an unrefereed report. The tree count and the random sample are computed here. Not read by a human.''',
     ['rainbow', 'recovery', 'lp', 'open'],
     [RS + 'sol_route-probabilistic/REPORT.md', RS + 'sol_route-probabilistic/PROOFS.md', HERE + ' (figs_scope.py: random_fig, seed 2026)'])

page('trinity', 'three graphs', 'Three graphs inside one triangulation', G4, r'''
Mark a centre in every face of $T$, black and white, and join each centre to its three corners and to the centres across its three sides.
The result, in (a), contains three graphs on equal terms.
Delete the white centres and the spoke graph of the proof remains. Delete the black centres and its mirror on the white faces remains.
Delete the original vertices and what is left is the cubic graph $G$.
A state lives in the first, the tree on the white faces in the second, and the Hamiltonian cycle in the third,
which is why the proof keeps changing graphs.
Knot theorists know this structure as a trinity, and one report restates the theorem as a statement about hypertrees.''',
     r'''The drawing is computed here. The restatements are dictionaries, checked by a second model as dictionaries only. They prove nothing new. Not read by a human.''',
     ['dimers', 'recovery', 'rainbow', 'primal'],
     [RS + 'fable_route-categorical/CATEGORICAL.md, Section 2', RS + 'fable_referee-topology/REFEREE.md, part e', HERE])

# ---------------------------------------------------------------- cutting and induction
page('cuts', 'small cuts', 'What a small cut has to remember', G5, r'''
The proof splits $T$ along separating triangles and glues the answers.
Each side must only report how its two trees meet the cut.
Across a triangle, two of the three vertices lie in the same tree and are joined by an edge, so there are three patterns, shown in the top row.
Both sides can be made to agree by prescribing that edge, which is why the theorem carries a prescribed edge.
Across a cycle of length four there are more patterns, and they also differ in how each tree connects the cut vertices.
The bottom row shows every pattern that occurs on one such cycle of the running example.''',
     r'''Gluing along triangles is in the OpenAI paper, Section 7. The patterns are computed here from all Hamiltonian cycles of the two examples. The general list for length four is in an unrefereed report. Not read by a human.''',
     ['pairs', 'recovery', 'induction', 'earlier'],
     [OA + ', Section 7', RS + 'fable_route-categorical/REPORT.md', RS + 'astra_route-pfaffian/REPORT.md (chord exception)', HERE])

page('induction', 'induction', 'Induction by removing a vertex of degree four', G5, r'''
Every triangulation of this kind grows from the octahedron by two local moves, so one can try induction.
The useful step removes a vertex $x$ of degree four and merges two opposite neighbours.
A good state of the smaller triangulation lifts back in exactly one way, shown in (b) and (c).
If the lift is not a good state, rotate three wedges around one white face, as in (d). The result usually is one.
Lift or rotate settles 98.3 per cent of the failing cases up to 16 vertices. The rest need a rule nobody has found.
The induction also needs a contraction that keeps a pair, which holds in every tested case and is not proved.''',
     r'''The lift and the rotation were proved in an unrefereed report. The two remaining statements are conjectures, tested on all 344,872 contractions up to 17 vertices. Not read by a human.''',
     ['cuts', 'rainbow', 'open'],
     [RS + 'opus_route-induction/REPORT.md', RS + 'opus_route-induction/INDUCTION.md, Section 4', RS + 'opus_route-induction/PROOFS.md', HERE])

page('earlier', 'earlier methods', 'Where the older methods meet this proof', G5, r'''
Three older ideas end at the same object. Stein showed that a Hamiltonian cycle of $G$ is the same thing as a split of the vertices of $T$ into two induced trees, as in (a).
Kelmans strengthened the conjecture to cycles that avoid or use a prescribed edge, which makes gluing along small cuts possible. Panel (b) counts the cycles avoiding each edge.
Feder and Subi colour the vertices of $T$ with three colours, contract one colour class, and look for a spanning tree of faces.
In the present language their tree is an induced tree whose vertices outside one colour class are pairwise non-adjacent, as in (c).
None of the three supplies the step from a pair to a good state.''',
     r'''The three results are published. The translation of Feder and Subi into induced trees was written in this project and is unrefereed. Not read by a human.''',
     ['recovery', 'cuts', 'produced'],
     [RS + 'astra_older-approaches/BRIDGES.md', RS + 'astra_older-approaches/SOURCES.md', RS + 'astra_older-approaches/NOVELTY.md', OA + ', Section 2', HERE])

# ---------------------------------------------------------------- scope
page('produced', 'produced cycles', 'Which Hamiltonian cycles the proof can produce', G6, r'''
The construction turns each good state into one Hamiltonian cycle, and different good states give different cycles.
It does not reach every cycle. The hexagonal prism has eight Hamiltonian cycles. Four of them avoid the prescribed edge, and the construction produces two.
The test for a given cycle runs the construction backwards. Orient the edges of $T$ that the cycle does not cross towards the roots and read off a state.
The cycle is produced exactly when that state is a good state.
The bottom row shows the four states. Two are good states and two are not.
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
     r'''The counts in the chart are computed here by direct enumeration. The general formulas for these families are in an unrefereed report. Not read by a human.''',
     ['produced', 'lattice', 'open'],
     [RS + 'sol_counting-families/FAMILIES.md', RS + 'sol_counting-families/REPORT.md', HERE])

page('open', 'open doors', 'What is still open, and how far it was tested', G6, r'''
Four statements would each give a proof that avoids the signed sum, or a fast algorithm. None is proved.
The bars show how far each was tested, by exhaustive search on the left and by sampling beyond it.
The crosses are statements of the same kind that looked plausible and failed, at the size where the first counterexample appeared.
Several crosses sit beyond the range where the surviving conjectures were tested exhaustively. Passing every example up to 22 vertices is weak evidence in this subject.
Panel (b) shows the mechanism behind the failures at the extremes. A white face whose three black neighbours all put their wedge at the far corner closes a triangle of opposite edges.''',
     r'''Every number on the chart is quoted from an unrefereed report of this project and was not recomputed here. Panel (b) is computed here. Not read by a human.''',
     ['chain', 'rainbow', 'induction', 'pairlattice', 'canonical'],
     [RS + 'opus_conjectures/REPORT.md', RS + 'opus_conjectures/CONJECTURES.md', RS + 'fable_referee-topology/REPORT.md', RS + 'opus_route-induction/REPORT.md',
      RS + 'sol_counting-families/CONJECTURE-TESTS.md', HERE])
