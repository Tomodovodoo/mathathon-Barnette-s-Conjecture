# 09. What is still open

## What we want at this point and why

The proof shows that a Hamiltonian cycle exists. It does not say how to find one fast, how many there are, or whether a simpler argument could replace the signed count. This file collects the open questions that the project has met, each with what is known and how firmly. It is the place to start for anyone who wants to add something new.

Nothing here is needed for the proof. Unlike the other files, most of the content is unrefereed or conjectural, and every item says so.

## 1. Algorithms and complexity

### What is known

The existence proof is a counting argument and gives no efficient procedure. The OpenAI paper says so itself. The trees paper adds two procedures, both exponential.

| Procedure | What it does | Bound | Status |
| --- | --- | --- | --- |
| enumeration with pruning | tries states face by face, rejects a partial state when the remaining spokes are already disconnected or when it cannot be completed to a state | $O(n^3 M)$ with $M$ the number of states, and $M \le 3^{n/2}$, so $O(\mathrm{poly}(N)\, 3^{N/4})$ for a graph on $N$ vertices | published, trees paper Proposition 6.2 |
| marked walk | follows the two cancelling involutions of step 06 alternately, starting from any pair. Ends at a forest pair or restarts with at least two fewer cycles | $2^{O(n \log n)}$ time, polynomial space | published, trees paper Theorem 5.3. Not refereed in this project |
| generic search in cubic graphs | Eppstein's algorithm | $O(2^{N/3})$ | published, cited in the trees paper. It ignores all structure and has the smaller exponent, since $2^{1/3} < 3^{1/4}$ |

The bound $M \le 3^{n/2}$ comes from a pleasant fact. All states have the same permutation sign, by the parity of the disk identity, so the number of states is the absolute value of the determinant of the $0/1$ incidence matrix of faces against vertices, and Hadamard's inequality bounds that.

A certificate is easy to check. Given a state, testing that the remaining spokes form a tree takes linear time, and step 07 turns it into the cycle in linear time. So the search problem is of the kind where a solution always exists and is easy to verify.

### What is not known

**No polynomial-time construction is known**, deterministic or randomised. The specific gaps are these.

- *Sampling.* The determinant counts states, and it also counts completions of a partial state. So one can sample a uniform random state in polynomial time. That is proved in `research/2026-11-14_sol_route-constructive/ALGORITHMS.md` and was found correct by the referee `research/2026-11-14_fable_referee-determinants/`. It does not help directly, because a random state need not be a tree matching, and tree matchings can be rare, see below.
- *One determinant for the signed sum.* The signed sum of step 06 is one coefficient of a determinant with a variable for each black face. Extracting that coefficient takes $2^n$ determinants. A polynomial-size formula for it, for instance a Pfaffian, would give a polynomial algorithm by fixing the state one face at a time and keeping a non-zero branch. Nobody has one. Status of the idea: a hunch. Status of the obstruction: the plain determinant fails on the hexagonal prism, computed and refereed.
- *The length of the walks.* Every component of the exchange graph contains a forest pair. That gives reachability and no bound on the distance. In the experiments of the constructive report all 320 random or greedy walks from ten bad starting pairs finished within ten moves. That is a small computed sample, not refereed beyond the claims listed in the referee's report, and it says nothing about worst cases.
- *The complexity class.* The marked walk follows a path in a graph of degree at most two with alternating signs, which is the shape of the problems in the class PPAD. The report `research/2026-11-14_opus_route-graph-theory/REPORT.md` suggests that finding a tree matching lies in $\mathrm{FP}^{\mathrm{PPAD}}$. A hunch, not worked out.

### Tree matchings can be exponentially rare

There are rooted triangulations with $n = 5q$ that have exactly $3^q$ states and exactly $2^q$ tree matchings. They are built by inserting $q$ copies of the dual of the hexagonal prism into white faces. States factor over the copies, because the new black faces must be matched to the new vertices, and each copy has three states of which two are tree matchings. So a uniformly random state is a tree matching with probability $(2/3)^q$.

Status. Proved in `research/2026-11-14_astra_limits/HYPOTHESES.md` and checked by a second model, with the local enumeration reproduced, in section 6 of `research/2026-11-14_sol_referee-structure/INTEGRATION.md`. Not yet read by a human. The counts for $q \le 6$ are computed.

This does not make these instances hard. Their tree matchings are products and easy to write down. It only rules out the naive plan of sampling states until one works.

### The three-matroid remark

A tree matching is a set of spokes that is a common basis of three matroids. One says that the remaining spokes form a spanning tree. One says that each black face loses one spoke. One says that each non-root vertex loses one spoke. Two matroids can be intersected in polynomial time by Edmonds' theorem. Three in general cannot.

What has been established and what has not, according to the referee's integration notes.

| Claim | Status |
| --- | --- |
| tree matchings are exactly the common bases of these three matroids | proved in `opus_route-graph-theory/PROOFS.md` Lemma 1.1, accepted by the referee as a valid formulation |
| no one of the three conditions is implied by the other two | computed on the octahedron and the prism, accepted |
| a relaxation to two of the three matroids already fails on the hexagonal prism, where 4 of its 6 solutions are not states | computed in the constructive report, corrected and confirmed by the determinant referee |
| the natural linear programming relaxation has a half-integral vertex at 13 vertices | computed and confirmed. The referee adds that 13 should not be called the smallest size, since the search used random objectives, and that the fractional point is the average of one tree matching and one other state, not of two non-tree states as the report said |
| the general problem, given a planar bipartite graph of maximum degree 3, decide whether some perfect matching has a spanning tree as its complement, is NP-hard under polynomial-time Turing reductions | proved in `PROOFS.md` Proposition 1.2 from the NP-completeness of Hamiltonicity for cubic bipartite planar graphs (Akiyama, Nishizeki, Saito 1980). The referee's notes restate the NP-hardness as a conclusion, and the referee's folder contains the 1980 paper, which the original report had cited from memory |
| therefore no description by two matroids and no min-max theorem exists | **not established.** The referee marks this inference as a gap. The results above concern the natural encodings and the wider problem class. They do not exclude a cleverer encoding that uses the special shape of spoke graphs |
| the spanning-tree condition on spokes is the same matroid as the graphic matroid on opposite edges with the roots contracted | **refuted** as a statement about arbitrary subsets. The two tree conditions agree only after one spoke per black face has been removed |

The NP-hardness result does not make Barnette graphs hard. In our setting the answer is always yes once the single-triangle obstruction is absent. It says that an efficient algorithm has to use the structure, the hexagonal faces of the spoke graph and the colour balance, since the bare combinatorial problem is hard.

## 2. Counting

Let $m = c_{\min}$ be the least number of cycles formed by a pair, and write TM for the number of tree matchings and HC for the number of Hamiltonian cycles of $G$.

| Statement | Status |
| --- | --- |
| tree matchings of sign $+1$ and $-1$ are equally many, so TM is even and never 1 | published, trees paper Theorem 5.2 |
| $\mathrm{TM} \ge 2m$ | proved in `research/2026-11-14_fable_route-combinatorics/PROOF.md`, Corollary 3, and checked by a second model. Not yet read by a human |
| $3\,\mathrm{TM} \le \mathrm{HC}$ | proved in the same file, Proposition 7, and checked by a second model |
| $\mathrm{TM} \ge 2^{m}$ | **conjecture.** True for all 5,088 rooted triangulations with a pair and at most 16 vertices, with equality in 4,609 of them. Two independent enumerations agree. A rooted triangulation with a pair and fewer tree matchings would refute it |
| tree matchings split into cubes of dimension $m$ | refuted. The running example has 6 tree matchings and $m = 2$ |
| $m$ can be large | $m$ reaches 4 in the range computed. The referee points out that this does not prove that $m$ is unbounded |

The conjecture $\mathrm{TM} \ge 2^m$ says that instances whose cycle covers need many cycles have more tree matchings, not fewer. A proof would have to explain the moment identities of step 06 by some structure finer than a partition into cubes.

One more counting question has a precise form. Li counts objects with $m$ distinct marked crossings. The linear-weight version of step 06 counts the same pairs through an elementary symmetric function of the weights. The determinant referee conjectures that these are the same count for unit marks and proposes a test on an instance with $m = 2$. Not done.

## 3. Canonical choices and the lattice of pairs

Step 06 lists the canonical choices that fail. Two questions survive.

**The lattice-extreme conjecture.** A 2-factor of the incidence graph, that is a pair up to reversing cycles, is the same as an orientation of the spoke graph with prescribed out-degrees. By a theorem of Felsner such orientations form a distributive lattice with a least and a greatest element. The conjecture says that the least or the greatest element always contains a forest pair.

- Source: `opus_route-graph-theory/ROUTES.md`, route O6. In 180 random instances with 80, 100 and 120 vertices the least element failed 14 times, the greatest 11 times, and never both.
- The referee confirms that each extreme alone can fail, with certified examples at 40 and 120 vertices. The referee also found that the saved 80-vertex "maximum" is not a lattice maximum, since it still has directed cycles in both senses. So the experiment tested orientations where no further face flip was possible, and those need not be the extremes of the lattice. The conjecture stays a conjecture, for the precisely defined extremes, and the evidence for it is weaker than the report suggests.
- Felsner's theorem was cited from memory in the report. Whether face flips generate the whole lattice for these graphs is itself open there.
- If true, the conjecture would give an explicit candidate. It would not by itself give a polynomial algorithm, since one would still search among the orientations of the cycles of the extreme 2-factor.

**Monotone descent.** For a pair $(r,s)$ let $k$ be the number of cycles of $Q_s$. The conjecture says that from every pair some sequence of cycle reversals reaches $k = 0$ without ever increasing $k$. It would prove that every exchange component contains a forest pair without any signs. The single-step versions are false. A reversal along a cycle through all of $X$ swaps $r$ and $s$, so it cannot lower $k$ in both directions, and a 50-vertex example has a pair from which no single reversal lowers $k$. Two steps suffice in every example found. Source: `opus_route-graph-theory/PROOFS.md` section 8 and `ROUTES.md` D3. The referee lists it as a conjecture.

**Induction on the triangulation.** Every triangulation without separating triangles other than the octahedron has a vertex of degree 4 that can be removed by merging two of its neighbours. States lift bijectively. A tree matching of the larger triangulation may contract to a state that is not a tree matching, and the other direction needs a side condition that the induction does not supply. The referee refuted the "if and only if" form of the lifting lemma in the report. So this route is open at best.

## 4. Simpler or different proofs of the hard step

- **A proof inside one cycle cover.** Impossible, by the 16-vertex example of step 06.
- **A proof by a positivity theorem for determinants.** The matrices involved are not positive semidefinite. Open, with no lead.
- **A probabilistic proof.** The two reversals look like cycle popping in Wilson's algorithm. A hunch in `research/2026-11-14_fable_dependency-graph/skeleton.md`, edge D4.
- **A topological proof of the disk identity** as a statement about the degree of the colouring map. A hunch, same file, edge B2.

## 5. Stronger statements

| Statement | Status |
| --- | --- |
| a Hamiltonian cycle avoiding any one edge | published, Corollary 7.1 |
| a Hamiltonian cycle through any path with two edges | follows at once, see step 08 |
| a Hamiltonian cycle through any path with three edges | published as Corollary 7.2, through an equivalence of Gorsky, Steiner and Wiederrecht. It rests on their paper as well as on the proof |
| a Hamiltonian cycle through any path with four edges | false on the cube |
| a Hamiltonian cycle through one given edge and avoiding another | true for all 55 Barnette graphs with at most 24 vertices. A finite test. The referee asks that it be reported as nothing more, since the project did not settle what the literature says |
| a Hamiltonian path between any black vertex and any white vertex | same status |
| analogues on the torus or the projective plane | the states of this proof do not exist there. A different definition would be needed. Open |

## 6. Review and formal verification

- **The OpenAI proof.** A Lean 4 formalisation by OpenAI exists. An agent of this project rebuilt it and found that the main theorem depends only on the three standard axioms and that the formal statement matches the conjecture (`research/2026-11-14_opus_lean-formalisation/REPORT.md`, a computation by one agent). The formal proof covers Theorem 1.1 and the edge-avoiding form. It does not cover Corollary 7.2. It takes a different route from the paper in several places. In particular it never states the two-trees theorem and uses a polynomial where the paper uses an exponential.
- **The three papers.** All are preprints. No journal review is known to the project's literature review as of 14 November 2026.
- **Li's note and the trees paper.** Not formalised. Within the project, Li's involutions for more than one cycle, the marked walk and the enumeration bounds have been implemented in `workings/barnette_lab` and run on finite ranges. The determinant referee did not review that part. It stays computed and unreviewed.
- **The project's own proofs.** The weight-free proof of Proposition 5.1, the linear-weight proof, the Euler identity and the pair criterion, the sharp hypothesis in $G$, the description of the cycles produced by recovery and the rarity family have each been checked by a second model. None has been read by a human, and none is formalised. The heights proof is short and uses only the disk identity and signed intersection numbers, which makes it a reasonable first target for a formal check.

## Where to start

Three suggestions, in order of how well posed they are.

1. Prove or refute $\mathrm{TM} \ge 2^{c_{\min}}$. The data and two programs are in `fable_route-combinatorics/` and `astra_referee-combinatorics/`.
2. Test the lattice-extreme conjecture with true lattice extremes, on an exhaustive list of triangulations, where failures of the single extremes start to appear.
3. Look for a polynomial-size formula for the signed sum, or show that the coefficient extraction is hard in some precise sense.
