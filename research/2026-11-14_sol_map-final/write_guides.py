from pathlib import Path
import sys,re
sys.path.insert(0,'digestions/route-map')
import routes as rt
base=Path('digestions/steps')
text=r'''# 09. What is still open

The existence theorem is proved in the supplied 2026 preprints. The questions below ask for a different proof, an efficient constructor, or more information about good states. Nothing here is human-checked. `PROVED-HERE` means T2, including after an AI referee. `COMPUTED` means the stated finite range only. T3 requires independently validated exhaustive code; the new author-only searches remain T4.

Write V=|V(T)| for dual order. The primal order is N=2V-4. A feasible root admits a pair. A cover is the unoriented D of a pair, equivalently a 2-factor of the incidence graph. A cover with c cycles has 2^c orientations. Let m be the minimum c over covers and q(s) the number of cycles of Q_s. These are different invariants. A good state has Q_s a forest with exactly one root per component, equivalently its spoke complement is a tree, equivalently it has exactly one partner. Ordinary acyclicity without a partner is insufficient. Census files call the number of good states `TM`.

## Ten open doors, ranked

### 1. Rainbow Step X

`CONJECTURE`, T5. Every point-rainbow white spanning tree reaches a good state by exchanges that never increase black-face excess, allowing plateaus. [RAINBOW.md](../../research/2026-11-14_fable_referee-topology/RAINBOW.md) defines the moves and excess exactly. Step R is now `PROVED-HERE`, T2 unreviewed: a point-rainbow tree exists if and only if there is no separating triangle with black inner boundary. Rado's theorem and an Euler identity prove this without signed nonvanishing. Theorem S completes each such tree to exactly one incidence 2-factor, so R also gives a pair. For each bounded black face, resident eviction gives a fixed-point-free involution on good states, a sign-free evenness proof, also unreviewed.

`COMPUTED`, T4. X holds at all rooted instances through V=17, and at all rootings of 1,485 of the 1,543 triangulations at V=18. The remaining 58 are not checked. Singleton-factor instances use Proposition U; the other cases enumerate rainbow trees. Samples reach V=120. The [report](../../research/2026-11-14_fable_referee-topology/REPORT.md) lists exact counts and missing indices. Strict descent fails at V=8, periodic eviction walks at V=38, load M-convexity at V=12. Next test: finish the 58 cases and compare plateau components with the unique-factor dictionary. R plus X would give a counting-free proof. X alone supplies no polynomial bound on plateau search.

### 2. Induction G, also ML1

`CONJECTURE`, T5. Every rooted separator-free T with V>6 has a non-root degree-four vertex and a simple opposite-neighbour merge that still admits a pair. `COMPUTED`, T4, all 62,416 separator-free facial-root occurrences with 8<=V<=19 pass.

`PROVED-HERE`, T2 unreviewed, [G.md](../../research/2026-11-14_astra_induction-lemmas/G.md). A chordless four-cycle witnesses parallel edges after contraction. A chordless five-cycle with four black and one white inner boundary incidences witnesses a new black-inner separator in a simple contraction. Coloured disk curvature gives an interior degree-four vertex and proves G when chordless five-cycles are absent. It does not give an interior vertex with a good merge. Inward selection fails at V=11, five-cycle-only selection at V=13, and the blocked-source refinement at V=14. Next test: a global uncrossing rule must survive those three saved certificates before any larger census.

### 3. Induction X, also ML2

`CONJECTURE`, T5. If both opposite contractions at a non-root degree-four vertex have good states, some contracted good state is non-exceptional and lifts or rotates successfully, with exception as defined in [RESIDUAL-CASES.md](../../research/2026-11-14_fable_induction-completion/RESIDUAL-CASES.md). This is a different X from rainbow Step X. State splitting, the exact lift criterion and the original rotation have an independent AI referee. The one-sided step and the exception-set bijection are T2 unreviewed extensions.

`COMPUTED`, T4. The contraction inequality #good(T)>=#good(T/M) passes 1,202,792 rooted contractions through V=18. The later [X.md](../../research/2026-11-14_astra_induction-lemmas/X.md) checks all 7,940 exceptions through V=18; the exceptional fraction of the whole contraction is at most one half. Mate repair fails at V=16 and single-cycle repair at V=17. At V=18 graph 80, root {8,0,1}, x=15, merge {14,9}, every good state of one cover is exceptional. No orientation change within it repairs the exception, although another cover succeeds. Next test: construct a cover-changing injection into non-exceptional good states. The numerical inequality TM(T/M)+TM(T/N)>2e is sufficient for success, not a proved equivalence.

### 4. C1, at least 2^m good states

`CONJECTURE`, T5. Every feasible root has at least 2^m good states; equality is conjectured to mean exactly one cover. The known general bound is 2m. One cover gives equality, independently AI-refereed. For exactly two covers with c1,c2 cycles and j shared component cycles, `PROVED-HERE`, T2 AI-refereed, the count is 2^c1+2^c2-2a with a either 0 or 2^j. Hence the weak exponential bound holds. Equality requires c1=c2=j+1 and a=2^j. Excluding that planar overlap is still necessary for strictness. See [the qualified integration statements](../../research/2026-11-14_sol_referee-covers/INTEGRATION.md).

`COMPUTED`, T3. The independent all-root replay reaches V=22, with 9,531,638 facial-root occurrences, 4,656,948 feasible. The separate separator-free census reaches V=24 and 23,824,742 occurrences, T4 for its larger invariant calculations. The covers referee independently replayed its 3,374 occurrences on 129 separator-free graphs only through V=16. Neither scope silently extends the other. [C1 replay](../../research/2026-11-14_sol_referee-conjectures/data/fast_census_summary.json), [separator-free census](../../research/2026-11-14_astra_cycle-covers/CENSUS.md). Next test: resolve two-cover equality, then extend the shared-state calculation to several covers. A single nonzero degree-m moment alone does not force 2^m states.

### 5. C3, monotone pair descent

`CONJECTURE`, T5. From every ordered pair, some sequence of D-swaps and Q-reversals reaches a good pair without increasing q(s). Plateaus are allowed. Equivalently no positive-q plateau is closed, or every component of each sublevel graph contains a good pair. This equivalence is T2 unreviewed in [PROOFS.md](../../research/2026-11-14_fable_descent/PROOFS.md). The full exchange-component theorem does not establish its sublevel version.

`COMPUTED`, T4, [descent report](../../research/2026-11-14_fable_descent/REPORT.md). All 49,325,864 pairs through V=22 pass, as do all 9,970,784 pairs on 230 random triangulations with V=26..80. Earlier independent reachability replay reaches V=16. Sampled starts through V=200 succeeded; three capped V=300 starts are undecided. Strict descent first fails at V=16; lookahead two first fails at V=21; lookahead three fails at V=40, not known least. No tested height tie-break survives. Next target: prove no closed component at q=1, using the function model of a D-swap rather than another fixed lookahead. White-face gluing gives product exchange graphs, so the gluing trick that killed lattice R2 does not kill C3.

### 6. P2, face-rainbow packing

`CONJECTURE`, T5. Every pair support splits into two face-rainbow white spanning trees, equivalently Q_r union Q_s splits into two transversal spanning trees of T/R. `COMPUTED`, T4, all 14,881 supports through V=17 pass. [Packing proofs](../../research/2026-11-14_opus_two-tree-packing/PROOFS.md), Conjecture 3.4. Next test: use matroid intersection on larger supports and look for the obstruction to the face-side analogue of Edmonds branchings.

The ordinary two-tree packing is `PROVED-HERE`, T2 unreviewed, by Nash-Williams and the density inequality extended to all vertex sets. It holds even for deleted-corner maps that are not pairs. Every pair support contains a face-rainbow tree and splits into two point-rainbow trees, also T2 unreviewed. Meeting both constraints at once can fail within one support, already at V=16. P2 would not close that integrality gap.

### 7. Efficient construction and search complexity

Open problem. Find a good pair in polynomial time. The supplied constructive preprint gives matching search bounded by O(poly(N) 3^(N/4)) time and a marked walk bounded by 2^O(N log N), both using polynomial space. The new [complexity analysis](../../research/2026-11-14_fable_descent/COMPLEXITY.md) gives a T2 unreviewed reduction of TREE-PAIR to PPADS conditional on the preprint's Theorem 5.3. It merges marked-walk levels into a find-a-sink instance. Extra sources obstruct the obvious PPAD reduction. The full Hamiltonian problem additionally needs the recalled closure citation or explicit chaining, which the author did not write out. Do not promote that qualification to an unconditional complexity classification.

C3 does not put the search in PLS: plateaus need a tie-break, and all tested polynomial-range choices fail. No polynomial runtime follows from rainbow X either. Next test: bound plateau diameter or construct a valid sink-preserving reduction that pairs extra sources. Finite positive-weight fitting on the full spoke graph fails because forced spokes have target inclusion one; conditioned or boundary-supported positive measures remain possible. Exponentially rare good states in width-four tubes defeat uniform state rejection, not every sampler.

### 8. Unbounded m with bounded primal face sizes

`CONJECTURE`, T5. Can m grow without bound among separator-free triangulations whose dual graphs have only square and hexagonal faces? `PROVED-HERE`, T2 independently AI-refereed, the separator-free family T_j on 3j+2 vertices has one cover, m=j-1 and exactly 2^(j-1) good states. Its pole degrees grow, so it does not answer the bounded-face-size question. Width-four tubes have bounded face sizes and exponentially rare good states, but m=1 at their specified root. [Family referee](../../research/2026-11-14_sol_referee-covers/REFEREE-families.md). Next test: construct fixed-width transfers with growing minimum cycle count while preserving separator-freeness.

### 9. Directions, determinants and the recovery image

Open problems. Given a cover, select directions yielding a good pair when one exists; characterize the image of good-state recovery using G alone; or evaluate a positive coefficient without exponential coefficient extraction. Testing a specified pair is already linear time. Some covers have no successful direction. Lattice extremes fail first at V=18; extremes plus irreducibles fail at V=33, with separators, leaving the separator-free restriction a separate test. [Lattice reading](../../research/2026-11-14_sol_referee-conjectures/LATTICE-READING.md).

Recovery from good states is injective and not onto all avoiding cycles. The hexagonal prism has four avoiding cycles but only two in this image. The primal compatible-state theorem concerns a broader correspondence. Next test: distinguish its unpartnered states from the good-state image on the same fixed fixture. The Feder-Subi face-tree dictionary must retain the proper-quasi-vertex condition; the relaxed predicate already differs at primal order 10, as checked in [the atlas audit](../../research/2026-11-14_sol_atlas-audit/AUDIT.md).

### 10. Finish statement bridges and human review

The [main paper v2 referee](../../research/2026-11-14_sol_referee-main-v2/REPORT.md) says FOLLOWS; its [fresh cold read](../../research/2026-11-14_opus_coldread-main-v2/REPORT.md) found no mathematical problem. The primal route is ACCEPT in the [cross-audit](../../research/2026-11-14_opus_cross-audit/ADJUDICATION.md): real sign divided by the formal phase is the constant i^n. The [involution v2 referee](../../research/2026-11-14_fable_referee-involutions-v2/REPORT.md) says FOLLOWS on both ray and drawing-free routes. These are AI verdicts, not human checks.

`COMPUTED`, compiled by its author; independent check pending. [The Lean devices](../../proofs/lean/README.md) compile the real-sign lemma, finite-difference route to Proposition 4.8 and a replacement main theorem over OpenAI's development. The main theorem's dependency closure excludes the complex phase and polynomial. The old [blueprint](../../proofs/blueprint/BLUEPRINT.md) count of 4 exact, 25 different-form and 5 absent counterparts is a dated baseline, superseded for several devices. Paper heights versus formal flow weights, topological translation bridges and the paper's gluing proof are not all formalised by this replacement. Next steps: complete the independent rebuild and statement check, then formalise those bridges and ask a human to read the three texts.

## What the unsigned approaches have taught us

Interpretation, not an impossibility theorem. Density now supplies pairs, rainbow trees, ordinary tree packings and each one-sided degree condition. The obstruction survives when those conditions must hold together. A fixed support can contain no good state, every direction of a cover can fail, and the closest exchange can create a new Q-cycle as it removes the old one. The signed sum succeeds because cancellation compares different covers while its first surviving order has a common sign. The failed shortcuts explain why that comparison matters in the known proof. They do not prove a signed count is necessary for every proof.

## Graveyard of counting-free shortcuts

Each row retains the exact rejected claim, its smallest saved or reported witness, its data or proof location, and the lesson. Unless the row explicitly certifies minimum order, the listed size is a witness size only. Some algebraic failures have proofs instead of numerical data; some older rows have no certified smallest size. Those absences are recorded, not filled with guesses. Sizes in the table are dual V unless a row explicitly says primal. The [generated route catalogue](../route-map/ROUTE-MAP.md) gives the claim-specific review state.

'''
# Preserve every negative, not just the newest ones. Source metadata is the authority.
text+='| Route and rejected shortcut | Counterexample and size | Data or proof | Lesson |\n|---|---|---|---|\n'
def cell(s): return str(s).replace('|',' / ').replace('\n',' ')
for r in rt.ROUTES:
 if r['status']=='REFUTED':
  where=r['where']
  for tag,folder in rt.FOLDERS.items():
   where=re.sub(r'(?<![\w/])'+re.escape(tag)+'/',folder+'/',where)
  text+='| '+ ' | '.join(cell(v) for v in (r['id']+' '+r['label'],r.get('cex','No numerical minimum recorded; see the proof source.'),where,r.get('lesson','See source.')))+' |\n'
text+='''
## What survives

Rainbow Step X, induction G and induction X, the exponential bound #good states>=2^m, C3 and P2 remain open. G without chordless five-cycles, Step R, unique-factor completion, resident-eviction evenness and ordinary two-tree packing are written proofs with their stated review limits. One- and two-cover counting and the separator-free forcing and rarity families now have independent AI referees. No unsigned existence proof has closed the simultaneous constraints.
'''
(base/'09-what-is-still-open.md').write_text(text,encoding='utf8')
# Update overview's final account in one place; preserve its introductory proof.
p=base/'00-overview.md'; s=p.read_text(encoding='utf8'); s=s[:s.index('## Where the project stands now')]+'''## Where the project stands now

Snapshot of 2026-11-14. Nothing is human-checked. The [main paper version 2](../../paper/main/barnette.tex) has a fresh independent AI referee, verdict FOLLOWS, and a completed fresh cold read. The [primal proof](../../proofs/primal/PRIMAL-PROOF.md) is accepted in the cross-audit. The [involution proof](../../proofs/involutions/INVOLUTIONS.md) has a second AI referee, verdict FOLLOWS for both ray and drawing-free face-path routes. Review changes the review state, never the proof tier.

The phase dispute is settled: real sign divided by the formal phase is the constant $i^n$. The [Lean devices](../../proofs/lean/README.md) compile the real sign, finite differences and a replacement main theorem on OpenAI's development whose dependency closure excludes the complex phase and polynomial. This is compiled by its author; independent check pending. It does not formalise every statement or every topological translation of the paper. The earlier blueprint counts are a dated baseline, not the final coverage of the new devices.

For sentence 8, $m$ is the minimum cycle count of a cover, and $q(s)$ counts cycles of $Q_s$. An independently AI-refereed separator-free family on $3j+2$ dual vertices has one cover, $m=j-1$ and $2^{j-1}$ good states. Its primal deletion interpretation is $c(D)=components(G-S)-1$. The forcing family has growing face sizes. A different width-four tube family has only square and hexagonal primal faces and exactly two good states among $Fib_{2L+3}$ states, at its specified root. The all-root counting census reaches dual order 22; the separate separator-free evidence reaches 24. Larger invariant calculations in the latter were not independently replayed by the covers referee beyond 16.

The unsigned routes have gained several proofs but no replacement existence proof. Rainbow Step R follows from Rado and Euler and supplies a pair by unique-factor completion; these new proofs are unreviewed. Step X remains conjectural, with all rooted instances through 17, 1,485 of 1,543 triangulations at 18, and samples to 120. The contraction induction still needs G and X, also called ML1 and ML2. G is proved without chordless five-cycles; the remaining repair must sometimes change the cover. Ordinary two-tree packing and each rainbow constraint separately are proved, unreviewed; the face-side packing P2 and simultaneous integrality remain open. Monotone pair descent C3 passes all pairs through 22, but strict descent, lookahead two and lookahead three fail at 16, 21 and 40. No polynomial-time constructor follows. Exact statements, review provenance, data and the ranked ten open doors are in [09](09-what-is-still-open.md).
'''
s=s.replace('\x0barepsilon',r'\varepsilon');p.write_text(s,encoding='utf8')
# HOW-IT-WORKS is the directory's reader guide, despite its non-README name.
p=Path('digestions/route-map/HOW-IT-WORKS.md');s=p.read_text(encoding='utf8')
s=s.replace('according to the new T2 unreviewed construction','by the independently AI-refereed construction')
s=s.replace('On 3m+2 dual vertices it has one cover, m=m-1 and 2^(m-1) good states.','On 3j+2 dual vertices it has one cover, m=j-1 and 2^(j-1) good states.')
s=s.replace('The new two-cover proof is T2 unreviewed.','The two-cover weak bound is T2 independently AI-refereed; strictness remains open.')
s=s[:s.index('## Current written routes and unfinished shortcuts')]+'''## Current written routes and unfinished shortcuts

Three complete written routes exist. The main dual paper version 2 has a fresh AI referee, FOLLOWS, and a completed fresh cold read. The primal route is accepted in the cross-audit. The marked-involution note has a second AI referee, FOLLOWS on both rays and drawing-free face paths. Nothing is human-checked. Sources and exact scopes are in [the final open-problem list](../steps/09-what-is-still-open.md).

The phase ratio is the constant i^n. The author has compiled the real-sign lemma, finite-difference nonvanishing and a replacement main theorem on the OpenAI Lean development. Its dependency closure excludes the complex phase and polynomial. Independent rebuild and statement check are pending. The paper's path heights versus formal flow weights and several topological translations remain separate obligations. See [the devices](../../proofs/lean/README.md). Do not read the earlier blueprint's 4/25/5 coverage count as a current tally of these additions.

The ray-mark counts 279 and 213 both use the running graph with two root anchors interchanged. Their total depends on the drawing; their signed count and nine second-fixed objects agree. Drawing-free face-path marks now have their own independent AI check. Their normalization H=-omega must be retained when comparing with the main paper.

Rainbow Step R is proved, unreviewed, by Rado and Euler. Every rainbow tree has a unique incidence-factor completion, so R also constructs a pair. Resident eviction gives n fixed-point-free involutions on good states, a sign-free explanation of evenness. Step X remains open: all rootings through V=17, all rootings of 1,485 of 1,543 triangulations at V=18, and samples to V=120 pass. Its plateau search has no polynomial bound. The eviction walk alone cycles at V=38.

Contraction induction still needs G and X, also ML1 and ML2. The exact obstruction uses four- and five-cycles. G is proved without chordless five-cycles, unreviewed; inward selection fails at 11, 13 and 14. At 18 an exceptional good state cannot be repaired by any orientation change of its cover. Ordinary two-tree packing and each rainbow constraint separately are proved, unreviewed. A fixed support can contain no good state from 16 on. P2, the two face-rainbow-tree split, remains open.

C3 is still a conjecture. The new author census checks every pair through V=22 and every pair of 230 random triangulations at V=26..80. Earlier independent reachability checks stop at 16. Strict q descent fails first at 16, lookahead two first at 21, and lookahead three at 40, not known least. Height tie-breaks also fail. The new conditional PPADS reduction asks for a sink; extra sources prevent the obvious PPAD argument. C3 alone does not give a PLS formulation or a polynomial algorithm. See [the qualified complexity discussion](../../research/2026-11-14_fable_descent/COMPLEXITY.md).

The independent covers referee confirms the separator-free forcing family, one- and two-cover weak counting bounds and the all-length width-four rarity formula at its prescribed root. The full-spoke mean obstruction excludes full-support measures, not conditioned positive measures. The two-cycle-level counterexamples are order-18 certificates, without a certified minimum-order claim. The larger separator-free counting census is source-reported through 24; that referee's independent invariant replay reaches only 16.
'''
p.write_text(s,encoding='utf8')
