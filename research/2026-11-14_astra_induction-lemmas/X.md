# X: repairs must sometimes change the cover

Status of X: CONJECTURE for a cancellation-free proof. It is not proved here. New arguments are PROVED-HERE, T2, unreviewed. Census evidence is COMPUTED, T4, with independent reference-engine replay of the decisive witnesses.

## 1. What an exception means

Use the notation of G.md, replacing p,q by v1,v2 when comparing the earlier files. Let s' be a tree matching of T/M. Its unique lift has one of the types

    (s(beta1),s(beta2))=(x,q) or (p,x).

Take the first type; the other is its mirror. Split the augmented tree Q_(s') plus the two root edges back at p,q. It becomes a two-component forest F, with K1 containing p and K2 containing q. The lift is a tree matching exactly when a lies in K2.

If it fails, the black face g=aqc across aq must take a. The rotation changes the assignments on beta1,beta2,g from x,q,a to a,x,q. After removing qc from K2, write K2' for the component containing q. The rotation is a tree matching of T exactly when b does not belong to K2'.

These are the refereed statements of Opus PROOFS.md 2.1, 3.1 and 3.2. An exception is a tree matching s' for which both tests fail. It is **not** just a state with partition {a p | b q}. That partition is necessary; one must also test b after removing qc. Its rotation is a tree matching of T/N, though not of T.

PROVED-HERE, restating the checked argument in Fable RESIDUAL-CASES.md, Theorems 3 and 4. The rotation bijects E_M with E_N. Indeed its outer forest is F-qc+ac, with components K2' and K1 joined to the c-component. For an exception, a,p stay together and b,q stay together. Its missing corner changes from q to a, which is an N-type tree matching. The N rotation undoes precisely this exchange. Thus, with e=|E_M|=|E_N|,

    TM(T) >= TM(T/M)+TM(T/N)-2e.                         (X1)

Here TM denotes cardinality. The four disjoint images are successful lifts from M and N, and successful rotations of failing lifts from M and N. A rotated image projects to a non-tree state in its new contraction; that separates it from the direct-lift image of that contraction.

PROVED-HERE. The strict inequality TM(T/M)+TM(T/N)>2e is equivalent to the existence of a nonexceptional tree matching in at least one contraction, because each exception count is bounded above by its corresponding total. It is sufficient for TM(T)>0. The earlier Theorem 4(c) supplies only this sufficiency through its contrapositive; it does not by itself prove that TM(T)>0 implies the strict inequality. Tree matchings of T can project to non-tree states. I do not use the claimed equivalence with existence in T.

## 2. What the extended search tested

COMPUTED. `code/x_hypotheses.py` enumerates all tree matchings at every facial root of every plantri Eulerian triangulation through V=18. It tests all non-root degree-4 vertices of instances with a tree matching. Exceptions agree with the previous census, 7,940 in total. It also recomputes mates and individual D-cycle reversals.

| Proposed strengthening or repair | Result |
| --- | --- |
| Every bounded black face can avoid any specified corner | No counterexample through V=18; still CONJECTURE |
| Every feasible local type at a usable x occurs | REFUTED at V=8 |
| The mate of every tree matching is a tree matching | REFUTED at V=12 |
| The mate of an exception is a nonexceptional tree matching | REFUTED at V=16 |
| Some single D-cycle reversal repairs every exception | REFUTED at V=17 |
| Some direction choice in the exception's entire fixed cover repairs it | REFUTED at V=18 |
| At most half of a fixed cover's tree matchings are exceptional | REFUTED at V=17 |
| At most half of all tree matchings of a contraction are exceptional | No counterexample through V=18; still CONJECTURE |

Corner avoidance was already Opus's S7, also called HQout. The new test extends its range rather than introducing a new hypothesis. It says each face has at least two values across all tree matchings. No transfer rule proving it inductively was found. It supplies a local alternative but does not control which side of F-qc contains b.

REFUTED. At V=8, graph 0, root {0,1,2}, use x=5 with a=4,p=1,b=6,q=3. The feasible types are (4,5), (5,3), (5,6), listed as ordered assignments at beta1,beta2. Only the first and third occur among the two tree matchings. The missing (5,3) type is a legitimate state type, not a root-forbidden prescription. `data/x_hypotheses_6_18.json` saves the rotation system.

## 3. A single cycle can fail, but two can repair

REFUTED. At V=17, graph 451, root {7,1,8}, x=2, a=3,p=0,b=1,q=9, there is an exception for merge {0,9} with two D-cycles of lengths 9 and 3. Its four direction choices have these classes:

| Reverse 9-cycle | Reverse 3-cycle | Class |
| --- | --- | --- |
| no | no | E |
| no | yes | E |
| yes | no | not a tree matching |
| yes | yes | L |

Thus every single reversal fails as a one-step repair, while two successive tree-preserving reversals can escape. There are two exceptions of this kind at V=17. The fixed cover has two exceptions among three tree matchings, disproving a per-cover half bound. The entire contraction has six tree matchings, three exceptional and three lifting, so the global half bound survives.

COMPUTED, independent replay. `code/repair_witness.py` uses `barnette_lab.Instance`, enumerates all 18 states and eight ordered pairs, and tests the spoke-tree complement directly. It confirms the table, the six tree matchings, and a shortest tree-preserving repair path of length two. Full face-indexed states, cycles and path are in `data/repair_witness.json`. The original T has no separating triangle.

## 4. No sequence of direction changes repairs the next witness

REFUTED. At V=18, graph 80, root {8,0,1}, choose

    x=15, a=16, p=14, b=8, q=9,     M merges {14,9}.

An exceptional tree matching in T/M has a mate whose D is one 13-cycle. The only two direction choices are the exception itself and a non-tree state. Its cover has just one tree matching, which is exceptional. The entire contraction has eight tree matchings: two exceptional and six directly lifting. The others belong to a different cover.

COMPUTED, independent replay. `code/repair_witness.py --cube` enumerates all 22 states and ten ordered pairs of this contraction with `barnette_lab`. Seven tree matchings belong to the three-cycle cover and one to the 13-cycle cover. Reversing the 13-cycle leaves a Q cycle. The full faces, state, mate and Q-cycle certificate are in `data/cube_witness.json`. The original T has no separating triangle. These are the smallest all-exception fixed covers found in the complete exception census through V=18; 220 occur at V=18 and none earlier.

PROVED-HERE. Reversing cycles of D preserves the deleted corner u(t), which is the third corner distinct from r(t),s(t). Consequently any sequence of such reversals stays in the same fixed cover. If each intermediate second state is a tree matching, recomputing its mate changes nothing: a tree matching has exactly one mate, obtained by orienting its opposite forest towards the roots. Hence the V=18 witness admits no tree-preserving sequence of D-cycle reversals to a nonexceptional matching. It also admits no repair by reversing an arbitrary subset of its D-cycles in one move. This obstruction is stronger than failure of one preferred local reversal.

The exact finite check turns the proposed universal fixed-cover repair into a REFUTED claim. It does not refute X. A successful general repair must sometimes change u, for example through a Q-cycle move at an intermediate non-tree state or through a different exchange of incidence assignments.

## 5. Heights, directed cycles, and the signed lower bounds

PROVED-HERE, interpretation of the refereed directed-cycle criterion. For fixed u, select one orientation bit for each D-cycle. A directed spoke cycle prevents exactly the choices which use all of its outgoing centre spokes as r-spokes. Testing Q is equivalent to checking these forbidden choices. The V=18 witness has one bit. Its only alternative orientation is forbidden by an explicit Q-cycle. A height assigned to a white face inside that cycle identifies an obstruction, but does not produce a second orientation outside this two-element set. Any height-based repair must include a cover-changing move and a termination proof.

The relevant source is `research/2026-11-14_opus_conjectures/PROOFS.md`, Lemma 2, now independently checked in `research/2026-11-14_sol_referee-conjectures/REPORT.md`. The lattice of covers describes possible new u values. It does not supply a monotone move that preserves tree matchings or escapes E. No such bridge is proved here.

PROVED-HERE, conditional use of signed inputs. If the existing evenness theorem or the signed bound TM(T/M)>=2 c_min(T/M) is imported, then e<2 c_min(T/M) is sufficient to force a nonexceptional matching of T/M. Evenness alone rules out e=1 with all matchings exceptional, since a positive even total is at least two. Neither bound controls e in general. Algebraically TM(T/M)=TM(T/N)=e=2 is consistent with evenness and X1 but leaves its right-hand side zero. Importing the full signed existence theorem for T settles existence directly and defeats the purpose of a second cancellation-free proof. These are recorded consequences, not ingredients of PARTIAL.md.

## 6. What remains

CONJECTURE X. At a two-sided usable vertex, at least one contraction has a nonexceptional tree matching. The bound 2e<=TM(T/M), and its counterpart for N, would imply it and the stronger contraction inequality. Our extension checks that bound through V=18 on every contraction with exceptions. Zero-exception contractions satisfy it automatically. `code/cube_repairs.py` and `data/cube_repairs.json` record the counts.

HUNCH. A cover-changing exchange may exploit the particular Q-cycle produced by reversing the exceptional Hamiltonian D-cycle. The smallest witness gives a finite target: move from the one-cycle cover to the three-cycle cover, then choose one of its six lifting states. A test must specify the exchange and its progress measure. Saying that the cycle encloses a white face is insufficient, since every obstructing state cycle already has that property.
