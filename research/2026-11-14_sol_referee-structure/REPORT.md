PROVED-HERE: the Euler pair criterion, sharp rooted cut condition, gluing and recovery image survive independent review.
REFUTED: the degree-four reverse implication and unrestricted matroid-isomorphism claim fail on small certificates.
COMPUTED: the V=13 LP vertex has an exact rank-25 certificate; several alleged lattice extrema are not true extrema.
COMPUTED: 55 graphs, 1,206 roots, 9,720 recovery images and all finite strengthening rows were independently checked.
CONJECTURE: corrected O6 and monotone D3 survive the stated finite tests; neither has been proved.

# Referee report

Independent referee: gpt-6.1-sol, 14 November 2026. All new work is confined to this folder. No author code, fable code or reference implementation was imported or executed. The verification code is my own. Other agents' changes were left untouched.

## What I set out to do

Audit the graph-theory and limits reports as unestablished research, check their proof obligations and saved examples, resolve overlap with fable's Hamiltonian-cycle claim, and supply final integration statements. The two referee files give exact claim boundaries, proof ledgers, individual verdicts and reverse-Lamport dependency tables.

## What is now established

`PROVED-HERE`, original results independently reviewed, T2 with one AI referee and human check pending:

* The exact Euler region identity and both directions of the black-inner separating-triangle pair criterion, including deficit one and disconnected induced sets.
* The sharp primal hypothesis for Li's reduced-incidence 2-factor: every nontrivial 3-edge cut has the chosen black root on its black-ended shore. Gluing can cut only at current black-inner obstructions.
* The alpha-orientation quotient and the applicable lattice theorem with essential-cycle flips.
* Forward recovery injectivity, the white-parent acyclicity image criterion, and fable's stronger dichotomy: every missed avoiding cycle gives a state with no partner.
* The white-face prism-sum count, exactly 3^q states and 2^q tree matchings, with the local enumeration now explicit. Positive tree counts cannot equal one, using the stated central cancellation input.
* Both natural three-matroid descriptions, after imposing the centre condition before identifying the tree conditions.

`LIT`. The actual Akiyama–Nishizeki–Saito source proves the required hardness for 2-connected cubic bipartite planar graphs. The two-query reduction is correct as a polynomial Turing reduction. Felsner's Theorem 1 applies to the feasible plane alpha-orientation set. Gorsky–Steiner–Wiederrecht's Theorems 4.4 and 4.16 give the stated P4 and Pfaffian consequences when the supplied existence theorem is used. Exact sources and scope are in `sources/README.md`.

`COMPUTED`, with saved-corpus and arithmetic qualifications in `code/README.md`:

| Independent check | Range or result |
| --- | --- |
| States, pairs, flow and obstruction | 55 saved graphs through V=14; 1,206 roots; 880 roots admit pairs |
| State totals | 12,924 states; 3,280 ordered pairs; 3,240 tree states |
| Recovery and inverse | 9,720 images, no collisions; 35,664 prescribed partitions satisfy the stronger dichotomy |
| Euler identity | 28,718 connected induced subgraphs, all saved V≤12 graphs |
| Sharp gluing | 3,618 prescriptions; 1,151 joins |
| LP vertex | V=13; 2,047 subset inequalities; active rank 25; determinant −2 |
| Degree-four lifts | 6,638 restricted lifts through V=13; 2,896 tree-input side tests pass |
| Alpha quotient and O6 | 932 factor occurrences through V=14; no joint extreme failure |
| Large O6 | True extrema on eight saved inputs, V=40..120; no joint failure |
| Monotone D3 | All 3,280 small pairs, all 18 pairs of fable's V=16 example, and the V=50 trap |
| Rarity | q=1,...,6, matching the exact powers |
| Limits and strengthenings | All named examples and all 55 strengthening rows checked, with the cut-label correction below |

A separate direct checker, without importing the main audit implementation, rechecks the LP, lift and local rarity certificates. Versions and SHA-256 input/output hashes are in `code/provenance.json`. I did not independently generate every graph isomorphism class.

## What failed and why

`REFUTED`. Opus Lemma 6.2(iii) has a false reverse implication. A tree lift can contract to a non-tree state, already at V=11. The correct side test assumes the contracted state is a tree matching. The formula also needs both split copies to be nonroots or a separate root case.

`REFUTED`. The spoke-to-opposite-edge map is not a cographic/graphic matroid isomorphism on arbitrary subsets. An octahedral witness distinguishes them when a centre loses more than one spoke. The common-base equivalence after the centre partition remains correct.

`REFUTED` as saved labels. The alleged V=80 alpha maximum and `alpha_min_fail_40_41` have directed cycles in both senses. Their factors have no tree orientations, but they are not lattice extrema. The separate V=40 `ef_fail_40_40` is a genuine minimum failure; V=120 `alpha_max_fail_120_123` is a genuine maximum failure. Facial terminals must not replace full lattice extremes.

`REFUTED` as a description. The saved LP dump omits the coordinates equal to one. Completing it yields a genuine fractional vertex supported on one tree state and one non-tree state, rather than two non-tree states. Random objectives do not establish minimality of order 13.

`REFUTED`. Astra's first-potential-coefficient test is sufficient, not necessary, for nonvanishing. A new V=14 integer-weight example has c_min=1 and zero linear Taylor coefficient but nonzero Z, checked by all-pair and tree-state aggregation separately.

`COMPUTED`, certificate correction. The theta example's named set has deficit two in its saved triangle labels. The set `{4,5,6,8,9,10,12,13,14}` has the asserted maximal deficit three. There are still eight states and no pairs at every root.

`COMPUTED`, overlap. Fable's V=16 no-tree factor is valid and smaller than Opus's stress example. All three recovery claims agree; fable's stronger dichotomy closes. The V=50 stored mate has three D-cycles; its other mate supplies the advertised single long cycle. The descent counterexample remains valid.

## What is still open

`CONJECTURE`. O6 is about the true extremes in Felsner's full order. It has no polynomial-time consequence without controlling the search among a factor's 2^c decompositions.

`CONJECTURE`. Monotone D3 permits D-swaps and Q-reversals without increasing k. It is distinct from a uniform two-swap lookahead claim. Neither has been proved globally.

`HUNCH`, not established. The evidence does not exclude every hidden two-matroid encoding or min-max theorem for the special spoke class. Hardness of a broader decision problem is not a hardness theorem for the total special search problem.

Historical minimum-order assertions for the larger named non-Hamiltonian graphs, a primary proof of the cofacial Kelmans attribution, and global status of arbitrary include-one/avoid-another and Hamilton-laceability were not certified. None is an input to the integrated structural proofs. The central pair-to-tree existence proposition remains an explicit supplied earlier theorem; this audit does not claim to rereferee every assertion of the source manuscript.

## Three best next steps

1. Apply the final integration statements and exclusions to the paper, especially the lift correction, true-lattice distinction and exact recovery image.
2. Test O6 on new larger inputs with full essential-cycle extrema, and D3 by exact non-increasing reachability. Preserve states with explicit face orders.
3. Obtain a second reader's check of the final Euler/component proof and the white-cycle disk proof of the tree-or-no-partner dichotomy. Both have independent finite checks and are compact additions to the exposition.

## Deliverables

* `REFEREE-graph-theory.md`: requested graph-theory verdicts, proofs and dependency audit.
* `REFEREE-limits.md`: limits, hypothesis examples, rarity and strengthening audit.
* `INTEGRATION.md`: final-form structural statements and complete proofs, with explicit inputs and exclusions.
* `code/`: independent programs, README, seventeen experiment/certificate outputs and a provenance manifest.
* `sources/README.md`: opened primary sources and unverified attributions.

Reviewed claims retain their mathematical tier. New findings made by this referee still need an external reader before they themselves are labelled independently refereed.
