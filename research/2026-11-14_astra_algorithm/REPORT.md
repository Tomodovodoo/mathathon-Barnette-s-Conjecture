PROVED-HERE: the manuscript's exponential bounds and marked endpoint argument withstand the bounded audit.
PROVED-HERE: incremental matching repair gives O(q^2(M+1)) enumeration; a direct good-state DP is FPT in supplied width.
COMPUTED: the complete hybrid passed all 30 larger benchmark inputs, and all 1,411 archived successful cycles passed independent replay.
REFUTED: both basic prefix sufficiency and individually filtered prefix sufficiency fail on an explicit 8-vertex triangulation.
CONJECTURE: an exponential marked-chain formula fits five sizes; polynomial construction and a proved Barnette pivot lower bound remain open.

# Research report

## Scope and source account

I read the project brief, source manuscript, exposition notation, named prior results and the authoritative FACTS table. The entire constructive text was read; PDF pages 9-11 were rendered and checked for the decisive formulas. The exposition's PDF was extracted locally. Source hashes are recorded in ALGORITHM.md. I used the reverse-Lamport audit method and the unslop writing instructions. No subagents were used.

The current source and current prior constructive ALGORITHMS.md agree. The manuscript proves `O(poly(n)3^(n/4))`, not just an unspecified exponential bound. The determinant coefficient bottleneck in the earlier report is a separate formula, not a gap in the manuscript's prefix-enumeration bound. The exposition already mentions enumeration in its closing section; it does not yet explain the algorithms. These are corrections to the task context, not errors attributed to the current files.

## What is proved

PROVED-HERE, unreviewed. The bounded audit closes the component polynomial route, the marked endpoint/parity route, the determinant matching count, prefix charging and additive gluing route. The exact dependency table is in AUDIT.md. This is a proof audit conditional on the supplied setting, not a machine-checked proof or certification of the entire Barnette theorem.

PROVED-HERE, unreviewed. Maintain a full extending matching at each search node. Forcing one incidence displaces one row and needs at most one O(q) augmenting-path repair. Rollback union-find tests the deleted spokes' dual white forest. Deterministic adaptive row selection still admits the qM prefix charging argument. This gives O(q^2(M+1)) search and O(q^2) words, with `M<=3^(q/2)` and `q=n/2-1`.

PROVED-HERE, unreviewed. A direct forest-and-deletion DP uses at most `2^b Bell(b)` syntactic states per bag and `q poly(b)4^b Bell(b)^2` time with joins. It finds a good state, not merely a Hamiltonian cycle outside the fixed-root recovery image. The path version is implemented, with explicit resource-limit exceptions and complete fallback. Arbitrarily large vertex degrees do not enlarge its degree states, since it counts deleted incidences.

PROVED-HERE, unreviewed. The account gives sharper marked-space bounds, an unmarked BFS bound, linear triangle listing, the separate cost of elementary separator processing and gluing, a direct linear prism construction, and the conditions under which bounded piece size or tube width helps. It rechecks the linear trap-chain lower bound and the corrected PPADS history construction. It does not claim that bounded m implies FPT, or that C3 plus existential polynomial path length implies a polynomial algorithm.

REFUTED with a full small proof. Even after removing each individually forest-incompatible residual incidence, a perfect matching can exist with no good completion. The 8-vertex witness has three states, two good, and a prefix forcing the third. ALGORITHM.md lists the complete matching argument and retained-centre neighbour lists. `filtered-prefix-counterexample.json` saves the input; `verify_saved.py` independently enumerates it. No novelty claim is made for this elementary obstruction.

## What is computed

Every row below is COMPUTED. Counts are finite experimental ranges, not proofs of asymptotic behavior.

| Campaign | Exact scope | Evidence |
|---|---|---|
| Census | 15 unrooted plantri graphs, every facial root through V=12, 262 rootings, four solvers, 1,048 successes | census-instances.json, census.jsonl |
| Larger families | 30 inputs, nine original methods, 270 rows, 246 successes; all failures explicitly capped | families-instances.json, families.jsonl |
| Final hybrid and DP | Same 30 inputs, both methods; hybrid 30 successes, standalone DP 19 successes and 11 width caps | hybrid.jsonl |
| Direct rollback stress | 500 biased split instances, V in 20,30,40,50; worst 32,161 candidates and 24,699 prefixes | stress.json |
| Public hybrid hunt | 60 relabelled/random-root split instances, V in 30,50,80,120, all successful; max two exchanges | hunt-instances.json, hunt.jsonl |
| Independent replay | 1,411 successful archived cycles, plus exact enumeration of both prefix witnesses | independent-checks.json, verify_saved.py |
| Existing regression | 14 tests and quick campaign of 70 rooted runs, pass, campaign 13.69 seconds | command below |
| New tests | Three methods; all generated roots through V=10, all edges of four named graphs, bad-certificate checks, resource-limit check | optimized/test_optimized.py |

The largest family graph has 300 primal vertices. The hybrid's slowest solver-only time in that campaign is 0.032959 seconds. The public hunt includes input validation and dual construction; its maximum is 0.454309 seconds. These are different timing boundaries. Single-run fits and censored counts are in BENCHMARKS.md. The machine/package versions and content hashes are in manifest.json.

The 193,623,384-pair C3 census and 3,373,400-pair independent referee census are prior evidence, checked against FACTS.md, not rerun here. The V=16/21/40 obstruction scopes are unchanged. The 38/40 evict graphs were reused for solver benchmarks; their original periodic rainbow walk was not reverified by this run. No disagreement with the authoritative numeric table was found.

## What failed

Rollback enumeration without a flow hint is not a good universal dispatch. It hit seven eight-second caps in the 30-case family campaign, including narrow tubes. The reference hit three, primal backtracking twelve, CP-SAT one internal cap and the marked walk one move cap. The final hybrid avoided those caps in this sample. It is still an exponential fallback algorithm.

The two prefix-sufficiency ideas failed at V=8. A residual matching oracle sees only incidence constraints, while the white forest condition is global. Adding individual compatibility does not repair this mismatch.

The 500-case stress search made rollback enumeration work harder but produced no asymptotic lower-bound family. The 60-case search for a difficult final hybrid instance produced no example needing more than two exchanges. The inserted degree-four structure biases the samples; easy observations should not be promoted into a general length claim.

The primary planar-flow theorem and cubic TSP sources were opened. The publisher's planar subexponential theorem statement was opened, but its full subscription proof was not retrieved. The PPADS closure source was not accessible in this run. These boundaries are stated in ALGORITHM.md. No latest-global-optimality claim is made for literature time bounds.

## Marked-walk lower-bound lead

COMPUTED. The fixed-flow trap chains with one through eight factors take 0, 5, 14, 113, 562, 2811, 14060 and 70309 marked moves. The eight-factor case finished in 79.794269 seconds and passed independent certificate replay. Nine and ten factors remain censored at twenty seconds. These extra eight successful records bring independent replay to 1,411 cycles.

CONJECTURE. For k>=4, the exact formula is (9*5^(k-2)-2*k+9)/2 under the saved labelled construction, reference flow cover, weights and token ordering. Five checked values support it, but no recurrence proof was found. This is the strongest lower-bound lead from the run, not a proved exponential family.

PROVED-HERE. Two first-eligible involutions on a product of five-point paths have an alternating path of length 5^k-1, despite O(k)-bit objects and O(k)-time moves. The proof is in marked-chain-analysis.md and ALGORITHM.md. It shows that the abstract endpoint argument alone cannot imply polynomial time. An embedding into the actual Barnette marks is still missing.

## What remains open or unfinished

Polynomial-time construction; C3; an efficient bounded-length pivot rule; Step X with a computable progress mechanism; constructive induction repair; a restricted determinant/Pfaffian completion oracle; and superlinear or exponential lower bounds for named pivots.

The implementation does not precompute a linear-time separator decomposition. It uses the existing polynomial separator search and label gluing, preserving the proved global exponential bound. General tree-decomposition joins, sphere-cut search and dynamic link-cut maintenance are not implemented. Height-guided, bidirectional and restart rules were not benchmarked; no exhaustive claim about the fastest rule is made. The special-family theorem is for prisms and fixed-width tubes, not all graphs with faces of size four and six. The requested optimization is therefore a concrete tested improvement, not a claim of complete optimization across every listed approach.

## Three best next steps

1. Independently audit the matching-repair charging proof and the join transition of the width DP. Implement general join bags only after that review.
2. Build a separator decomposition once, then benchmark flow-first leaves and deferred label gluing end to end. Preserve arbitrary prescribed-edge mapping in this change.
3. Prove or refute the marked-chain recurrence, starting from the product-involution theorem and checking unmarked-cycle priority and token transport. For a polynomial approach, any stronger prefix oracle must first survive the saved V=8 filtered witness.

## Exact sentences for the coordinator

No coordinator document was edited. Suggested additions or replacements follow.

**paper/main closing section**, replace the sentence beginning "The unsigned manuscript [4] states an algorithm" with:

> The unsigned manuscript [4] proves an enumeration bound of a polynomial factor times 3^{|V(G)|/4}, using polynomial space. Its determinant counts all incidence states and bounds the search; the algorithm does not extract a determinant coefficient. A separate marked walk terminates by an endpoint-parity argument, with only a 2^{O(|V(G)| log |V(G)|)} time bound.

Add after it, subject to review of the new proof:

> Maintaining an extending matching reduces the prefix-enumeration bound from O(q^3 M) to O(q^2(M+1)), where q=|V(G)|/2-1 and M is the number of incidence states. This improves a polynomial factor and does not give a polynomial-time algorithm.

**digestions/steps/09-what-is-still-open.md**, add:

> C3 plus the existence of a polynomial-length path would still require a polynomial-time method for finding that path. A bounded computable pivot rule, or a polynomial-time oracle for good completions of arbitrary prefixes, would close that algorithmic gap.

**digestions/SYNTHESIS.md**, add:

> The constructive algorithm account and audit are in proofs/algorithm/. The new hybrid combines flow, a bounded exchange search, a bounded-frontier dynamic programme and complete enumeration. Its successful finite benchmarks do not establish polynomial running time; new proofs remain unreviewed.

**digestions/route-map/HOW-IT-WORKS.md**, add:

> The incidence determinant counts states, not good states. Prefix matching and connectivity tests are necessary but not sufficient, even if every individually incompatible incidence is removed: an 8-vertex dual witness is saved in the algorithm report.

**digestions/route-map/ROUTE-MAP.md**, add a route record with this wording:

> Algorithmic route: complete marked walk and determinant-bounded enumeration are established in the supplied manuscript. Incremental enumeration and bounded-width good-state DP have new unreviewed proofs. A general polynomial completion oracle remains open; local prefix sufficiency is refuted.

## Reproduction and git

See README.md for every command and data-producing script. Heavy campaigns were serialized, with 480-second campaign caps and eight-second solver-worker caps. No subagents or outside service messages were used. Existing lab files and other owners' folders were untouched. The source account, bounds, and implementation milestones were committed and pushed to origin main as dbd6ede, 86ed02f and c3be25d. The final report milestone is committed separately; the chat handoff records its hash.
