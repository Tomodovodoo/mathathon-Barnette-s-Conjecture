# Report: the labyrinth and the route map

Fable 5.2, 2026-11-14. Folder `research/2026-11-14_fable_labyrinth-map/`. Also owned by this run: `labyrinth/` and `digestions/route-map/`.

## Five-line summary

1. The map exists: 16 waypoints, 17 steps and 175 routes (46 published, 40 proved here, 9 computed, 17 conjectures, 24 hunches, 39 refuted), in one data file that feeds the figures, `ROUTE-MAP.md` and the labyrinth.
2. Every complete proof (OpenAI, Li, the trees paper, the Lean formalisation) walks the same chain. It is forced at the pair, the disk identity, the sign and the cancellation. It is free at three steps: the first pair, the nonvanishing, and the last step to one cycle.
3. The direct edge to two induced trees and the unsigned bypass to a tree matching have no complete route. The bypass has nine exact reformulations and nine refuted relaxations.
4. `COMPUTED` here: two independent enumerations agree on states, pairs and tree matchings for all 7868 rooted Eulerian triangulations up to 16 vertices. That is the one T3 node of the labyrinth.
5. `COMPUTED` here, not predicted: a Hamiltonian cycle determines a state, but two cycles can give the same state. On the hexagonal prism 4 avoiding cycles give 3 states.

## What I set out to do

Build one place that shows every node of the proof, every route between nodes that anyone found or refuted, and its status. Deliverables: `labyrinth/` per the skill, `digestions/route-map/ROUTE-MAP.md` with a rendered graph, `digestions/route-map/HOW-IT-WORKS.md`, and this report with ten open doors.

## What is delivered

| Path | Content |
| --- | --- |
| `digestions/route-map/routes.py` | the single source: waypoints, steps, routes with status, source, lesson, counterexample, test |
| `digestions/route-map/build_map.py` | renders everything below from `routes.py` |
| `digestions/route-map/route-map.pdf`, `.svg`, `.png` | the full map, about 25 by 26 inches, every route listed next to its step |
| `digestions/route-map/route-map-overview.pdf`, `.svg`, `.png` | the same map without the lists, readable on one screen |
| `digestions/route-map/route-kinds.pdf`, `.svg`, `.png` | a matrix of the 17 steps against 11 kinds of argument, each cell giving established, open and refuted routes |
| `digestions/route-map/route-map.dot`, `routes.json` | Graphviz source (one edge per route) and machine-readable export |
| `digestions/route-map/ROUTE-MAP.md` | summary, reading guide, counts, one section per step with every route, lessons, counterexamples and tests |
| `digestions/route-map/HOW-IT-WORKS.md` | the plain account, about 3500 words |
| `labyrinth/` | `knowledge.json` (267 nodes), `events.jsonl` (53 backfilled, 1 live), `sota.json` (15 rows), `frontier.json`, `scatter.json`, `dashboard/index.html`, `STATUS.md`, `README.md` |
| `research/2026-11-14_fable_labyrinth-map/spotcheck.py`, `spotcheck.json` | my own check, written from the definitions |

Commands, from the repository root:

```
python -X utf8 -B digestions/route-map/build_map.py
python -X utf8 -B labyrinth/make_frontier.py
python -X utf8 -B labyrinth/seed.py
python -X utf8 -B labyrinth/lab.py check      # prints ok
python -X utf8 -B labyrinth/lab.py build
python -B research/2026-11-14_fable_labyrinth-map/spotcheck.py
```

The dashboard is `labyrinth/dashboard/index.html`. It is local and was not published.

## Choices I made

- **Shape of the picture.** The map is a U. The proof goes down the left arm (find a tree matching), across the bottom, and up the right arm (recover the cycle). The top edge, from the triangulation to two induced trees, is the goal as an equivalence. It is drawn grey with only partial and refuted strands. I think this shape says the main thing about the problem: the direct edge is closed and the proof is a detour.
- **Forced against free.** One black strand per distinct published argument. A single black strand means all sources agree up to translation. Five black strands at the nonvanishing step show where the exposition has choices.
- **Strands, facts, reformulations.** Only arguments that cross a step are drawn. Facts about a step and exact reformulations of the target are listed with a marker and not drawn. Without this rule the nine reformulations would look like nine proofs.
- **Frontier.** Size is `|V(T)|`. The invariant is the number of tree matchings of a rooted triangulation. Sizes 6 to 16 are fully resolved. Sizes 17, 18, 23, 28, 33 are there to show how little is known beyond.
- **Tiers.** `LIT` is T1, as the brief says. The three 2026 papers are unrefereed preprints, and every T1 node that rests on them says so in its status. I promoted nothing. Referee reports changed review states only.
- **Graphviz** was not installed. I drew the map with matplotlib on a hand-made layout, looked at the render, and revised it four times. The DOT file is written for anyone who prefers `dot`.

## What I established

- `COMPUTED` (`labyrinth/make_frontier.py`, output `labyrinth/frontier_crosscheck.json`). The multiset of (states, pairs, tree matchings) over all rooted triangulations is the same in `research/2026-11-14_fable_route-combinatorics/data/rows_v16.json` and in `research/2026-11-14_sol_route-algebra/counts.json`, at every size from 6 to 16 vertices: 8, 12, 14, 32, 36, 160, 176, 768, 1482, 5180 rooted triangulations. The two use different generators (own moves from the octahedron, plantri) and different state code. The combinatorics referee reports a third agreeing recount. Range: complete to 16 vertices.
- `COMPUTED` (`spotcheck.py`, bipyramids of rim 4, 6, 8, 10). Octahedron: 2 states, 2 pairs, 2 tree matchings. Hexagonal prism dual: 3 states, 2 pairs, 2 tree matchings, and all three `Q_s` are forests. On every instance: tree matching if and only if exactly one partner, all `D`-cycles odd with `δ`-sum `±3`, the real sign flips under reversal of a `D`-cycle, the signed sum over pairs is 0, and the two tree matchings have opposite signs.
- `COMPUTED` (`spotcheck.py`, rim 4, 6, 8, each edge of `t0`). The backward construction of `HOW-IT-WORKS.md` Section 2 works on every Hamiltonian cycle avoiding `e0*`: the complement gives three trees, one per root, and a state. Each such state is a tree matching or has no partner, as route-combinatorics Proposition 7 says. New: the map from cycles to states is not injective. On the prism, for the middle edge of `t0`, 4 avoiding cycles give 3 states. On the rim-8 bipyramid 6 cycles give 4 states. The reason is simple. A state fixes the tail of the selected edge in each black face and not the edge, unless `H - s` is a tree.
- Synthesis, with the status of its sources. The proofs are forced at six places and free at three (`ROUTE-MAP.md`, last sections). The dead ends fall into four groups: drop a constraint, pick an extreme, count without weights, weaken a hypothesis.
- The matrix of steps against kinds of argument (`route-kinds.png`) shows which corridors nobody has entered. At the nonvanishing step only polynomial arguments are established (5 routes), determinant arguments stand at 0 established, 4 open, 4 refuted, and no matroid, topological or inductive argument has been tried. Induction carries the gluing and nothing else.
- One link between reports that their authors had not made. The dependency-graph conjecture A2 (every avoiding cycle comes from a tree matching) was already refuted by the route-combinatorics survey and by the limits prism example. It is a dead end on the map (A.x1) with an `answered` event.

Everything else on the map carries the status its author or referee gave it. I did not re-prove anything.

## What failed and why

- My expectation that distinct cycles give distinct states was wrong, as above. I had written "recorded by a state" in the exposition and changed it to "determines a state".
- `HOW-IT-WORKS.md` is about six printed pages, not five. I kept the table of alternatives and the cube example and did not cut further.
- I did not open the dashboard in a browser. `lab.py check` prints ok, the build ran, and `node` parses both scripts of `index.html`. A rendering fault in a tab would not have been caught.
- The first build of `frontier.json` claimed some values both realized and impossible. `lab.py check` caught it, and the script now writes the impossible values as the complement of the realized ones.
- The route-graph-theory agent had tested the LP hunch of the machinery agent before I listed it. I had it as a live hunch for twenty minutes. It is now the dead end U.x5.
- Conjecture A.2 (roots of three colours not on a common face) is not well posed as stated. With three roots off a face there are `k` black faces and `k - 1` non-root vertices, so one black face has to be dropped and the conjecture does not say which. The categorical agent has since tested a two-root version: the obstruction moves and the recovery lemma fails without a root face (A.x2). I left A.2 as a conjecture and no longer count it among the ten best doors.

## What is still open

- Nothing written in this project has been read by a human. Two folders are AI-refereed, two are under review, the rest unreviewed. The state-of-the-art row `review` lists them.
- The map was frozen at 11:20 UTC. Folded in last: `fable_route-categorical`, at 11:15. Not folded in: the final verdict of `sol_referee-structure` (provisional when I read it), `astra_primal-proof` (in progress), `opus_conjectures`, `fable_digestions`, both manuscript drafts and the figure folders. To add a report, edit `routes.py` (routes and `REVIEW`) and `labyrinth/seed.py` (events, state-of-the-art rows), then run the commands above.
- The Lean routes on the map rest on the lean-formalisation agent's reading in `DIFFERENCES.md`, which is unreviewed.
- "Smallest known counterexample" is the smallest found, not a proved minimum, except where the entry says so.

## Three best next steps

1. A human reads the two candidate proofs of Proposition 5.1, `research/2026-11-14_astra_referee-combinatorics/REWRITTEN-PROP-5-1.md` and `research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` Section 2. They are the core of any new exposition and both are one page.
2. Attack the two structural conjectures that survived all the data, U.7h and D.7 (doors 1 and 2 below). Either would give the first existence proof with no signed count.
3. Keep the map alive. When a referee reports, change one line of `REVIEW` in `routes.py`. When a route is tested, change its status and add the counterexample. The rebuild takes under a minute.

## The ten most valuable open doors

Ranked by what a positive answer would change. Ids are those of `ROUTE-MAP.md` and the labyrinth.

| # | Door | Status and source | Concrete first test |
| --- | --- | --- | --- |
| 1 | **U.7h** Local search on white spanning trees: same-colour exchanges from a point-rainbow tree, never increasing the black excess, reach a tree matching | `CONJECTURE`, route-topology, 450 of 450 instances up to 16 vertices | At 18 vertices (1543 triangulations by plantri) record the longest plateau and the number of steps. One instance where every exchange raises the excess refutes it |
| 2 | **D.7** The face-flip minimum or maximum of Felsner's lattice of pairs always carries a tree pair | `CONJECTURE`, route-graph-theory, no joint failure in 180 random instances at 80 to 120 vertices | Exhaustive census up to 20 vertices first, then 24. Before that, on the saved 40-vertex and 80-vertex single failures (`gt/code/data/ef_fail_40_40.json`, `alpha_max_fail_80_83.json`) confirm that the other extreme works and count the orientations searched |
| 3 | **D.3** Every rooted triangulation with a pair has at least `2^cmin` tree matchings | `CONJECTURE`, route-combinatorics, 5088 of 5088 up to 16 vertices | Enumerate rooted triangulations with 17 and 18 vertices, keep those with `cmin = 3`, and look for a count below 8. In parallel study the 479 cases with more than `2^cmin` in `rows_v16.json` |
| 4 | **N.4** A Pfaffian or determinant for the signed sum with no coefficient extraction | `HUNCH`, machinery-literature and route-dimers | Write the turn tensor of one black face as a six-value boundary signature with zeros on equal corners and test the matchgate Grassmann-Pluecker identities. Any candidate must reproduce `5 y0 y1 y4 (-4 y0 y3 - 5 y1 y2 + 9 y2 y3)/64` on the hexagonal prism |
| 5 | **N.11** From every pair there is an exchange path along which the number of `Q`-cycles never increases and reaches 0 | `CONJECTURE`, route-graph-theory | Breadth-first search of the exchange graph of the 50-vertex trap `gt/code/data/deeptrap_50_1.json`, restricted to non-increasing moves. Then exhaustive exchange graphs at 20 to 30 vertices |
| 6 | **U.2h, D.8** Complexity of finding a tree matching: matroid parity, or PPAD | `HUNCH`, history-literature and route-graph-theory. The abstract problem is NP-hard, so the hexagonal faces must be used | Build the parity gadget for one black centre and for two adjacent centres and compare its feasible sets with the partial spoke choices. Separately, write one phase of the marked walk as an END-OF-LINE instance |
| 7 | **B.6** The disk identity as the theorem of turning tangents | `PROVED-HERE`, route-topology, unreviewed | Referee it. A sharp test: on `lim/examples/nonbijective_disk.json` (9 vertices, defect `d = -1`) the angle structure must fail to be flat by exactly the amount that gives `δ`-sum 0 |
| 8 | **N.12** Li's objects with `cmin` distinct marks are the elementary symmetric coefficient of the linear-weight polynomial | `CONJECTURE`, referee-determinants | On the 9-vertex double octahedron with the unobstructed root (`cmin = 2`, 4 tree matchings) enumerate Li's objects with `li.py` and compare the signed count with the coefficient of `x^2` in `F(1 + xa)` |
| 9 | **U.6h** Describe, in `G` alone, the Hamiltonian cycles whose state has a partner | `CONJECTURE`, route-combinatorics | On the hexagonal prism, middle edge of `t0`: `spotcheck.py` gives 2 partnered cycles and 2 unpartnered ones that share a state. Print the four cycles as face sequences and find what the shared state costs. Then test any rule on the 176726 unpartnered cycles of the survey |
| 10 | **D.9** Contracting a degree-4 vertex never increases the number of tree matchings. An injection behind it would be the first inductive tool on the left arm of the map, where induction has no established route | `CONJECTURE`, route-categorical, 948 contractions | Look for a local rule that extends a tree matching across a vertex split, on the 948 cases (`research/2026-11-14_fable_route-categorical/code/recursion.py contract`). The graph-theory agent's failed lift (U.x6: 708 of 1516 cases) says which side condition the rule must supply |

## Leads for others

- **Writers of the manuscript.** The backward reading in `HOW-IT-WORKS.md` Section 2 (start from a Hamiltonian cycle and derive the state) motivates states, tree matchings and the white tree before any counting. The hexagonal prism dual, with 3 states and 2 tree matchings, separates almost every pair of notions a reader might confuse. Say that a cycle determines a state and not conversely.
- **Dependency-graph and exposition agents.** Two counts of the uses of the disk identity are in circulation. The audit says four uses in OpenAI and three in Li. The determinant referee says parity is enough three times and the value 3 is used once. Both are right, and the paper should say which it means.
- **Route-combinatorics.** Your referee's reflection correction (first failures at 12, not 14 and 13) is in the map. Your `ROUTES.md` still has the old sizes.
- **Limits.** Your report says the certified resolved fraction stays zero until an independent validation exists. For the counts of states, pairs and tree matchings that validation now exists up to 16 vertices (`labyrinth/frontier_crosscheck.json`).
- **Coordinator.** `research/INDEX.md` can point to `digestions/route-map/route-map-overview.png` as the picture of the programme and to `labyrinth/STATUS.md` for the lists of conjectures, doors and dead ends.

## Git

Commits touch only `labyrinth/`, `digestions/route-map/` and this folder. The push result is in the final chat message.
