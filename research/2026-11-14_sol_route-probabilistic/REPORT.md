# Report

Finite positive UST weights cannot attain the full-H target mean, even on the cube.
Joint degree support is not M-convex; one-sided Lorentzian theory does not settle the joint event.
Half a disjoint pair passed 425 small rank-check cases and 27 larger two-tree packing tests.
Exact 12-vertex factors refute general unit-circle and linear real-rootedness shortcuts.
The signed measure is a difference of moment-matched positive measures; no unsigned existence proof was found.

## What I set out to do

Explore uniform and weighted spanning trees, convex mean fitting, positive measures behind the signed count, random sampling and flip chains, and analytic zeros. I read research/BRIEF.md, the repository README, the named skills and their loop, compute, Codex and saturation references, the OpenAI paper's text extraction, the route-map summaries, the specified dimers, determinant, combinatorics and topology writeups, the counting-family report and the structure referee integration. The source PDF was read through papers/text/OpenAI-Barnette.txt, not visually rendered. No garbled formula was treated as independent evidence; formulas used agree with the supplied referee derivations and lab conventions.

All writes are inside this assigned folder. The lab and other research folders were read only. No subagents were used. All computations ran serially. New proofs are T2 unreviewed; all experiments are T4 unreviewed. There is no independently refereed result from this task yet.

## What was established

PROVED-HERE, PROOFS 1-3. The full-H degree-event probability is a constrained weighted tree coefficient divided by the UST partition function. At uniform weights it is M/tau(H), compared with M/S for state rejection. Finite positive weights cannot give the prescribed mean because the outer-centre and root degrees are maximal and every spoke can be absent from a tree. Mean fitting is an exponential-family problem whose exact range is the relative interior of the projected tree polytope. This is a convex feasibility statement; rounding to an exact joint degree vector is separate.

PROVED-HERE, with literature input, PROOFS 4. The one-sided degree substitution is linear and inherits Lorentzian support convexity. The joint substitution is bilinear and has no such closure theorem. A six-cycle gives a hand proof that the joint degree support can fail M-exchange. COMPUTED, code/campaign.py scan, the cube spoke graph itself fails the exchange axiom. Its 128 spanning trees were counted both by exhaustive deletion and a Laplacian determinant.

PROVED-HERE, conditional on the supplied cancellation and height identities, PROOFS 5-6. Under uniform ordered pairs, signs are equiprobable. The signed pushforward to second states has atoms of size 1/P exactly on tree states and has total variation M/P. Its Jordan parts have equal low height moments. A degree-c_min product separates them. Shifted nonnegative heights give explicit token pools and a height-marked alternating involution walk ending at a forest pair. This is a reformulation of the signed mechanism, not a new unsigned argument or a runtime improvement.

COMPUTED, code/secondary.py. The first off-unit-circle example in the outer-0 scan through V=14 is at V=12 index 2, with normalized polynomial (z-1)(z^2+3). The first nonreal linear-weight example is V=12 index 0, with x(x+1)(2x+1)(2x^2+5x+4). Exact factors certify both failures. Real-rootedness in z already fails on the eight-prism, V=10, with 1-z^3. Minimality is only in the recorded root and gauge scan.

COMPUTED, code/campaign.py scan and code/half16.py. The white-edge vector equal to 1/2 on any selected pair support satisfies every tree-polytope rank inequality in 55 one-root instances through V=14 and 370 instances at V=16 with roots 0 and 1. Instances without pairs are vacuous. COMPUTED, code/packing.py, 27 larger examples through V=120 have explicit checked partitions of pair supports into two white spanning trees. The saved edge-colour lists certify each positive output. This is the strongest remaining lead.

CONJECTURE. Every pair support decomposes into two white spanning trees. If proved, this gives fractional target feasibility directly from a pair, without first invoking the forest-pair theorem. The separate joint-degree rounding lemma is still missing. NEXT-PREDICTION.md records the larger test before it ran.

## What failed and why

REFUTED. A positive finite UST weight optimum on all of H with target mean cannot exist. The target lies on a forced-spoke boundary face.

REFUTED. The general two-sided Lorentzian shortcut uses a bilinear substitution as though it were linear. The cube exchange witness makes that distinction concrete.

REFUTED. Zero cycles of Q is not the tree event. The hexagonal prism has three acyclic-Q states but only two tree states. A cycle-only Gibbs tilt cannot distinguish them. Root connectivity needs its own penalty.

REFUTED as universal root-location principles. Neither a unit-circle theorem for the z polynomial nor real-rootedness for the linear polynomial survives the exact small examples. Family product formulas are exceptional.

No verified second-moment, entropy, local-lemma or dependent-rounding existence argument was obtained. Negative association does not automatically lower-bound the exact event on overlapping degree stars. Paley-Zygmund for the event indicator is tautological. An exact degree-preserving rounding step would supply the missing structural theorem rather than follow from the standard rounding guarantee.

## Algorithms and random data

COMPUTED, code/campaign.py random. Three random constructions and rare controls were tested, with 160 approximate uniform-state samples and 12 local downhill flip trials per instance. The 50-vertex subdivision case gave 1/160 rejection successes but 12/12 downhill successes within 2000 proposals. The feasible rare 54-vertex width-4 tube gave 0/160 and 0/12. The latter has exactly 196418 states and, by the counting-family certificate, two tree states. Five obstructed plantri roots are separately identified by exact flow and are not counted as feasible-instance algorithm failures.

Sampling evaluates determinant self-reduction with floating inverses, with positivity, normalization and state-validity checks. It is approximate, not certified exact uniform sampling. The large graph models are biased and do not estimate the law of a uniform random Eulerian triangulation. Sampled cycle-cover counts provide upper bounds on c_min only.

COMPUTED, code/mixing.py. Uniform lazy white-face chains were fully enumerated through width-4 L=6. Symmetric transition matrices give finite spectral gaps and first-hit times by floating linear algebra. At L=6 the mean first-hit time from a uniform start is about 23119 proposals. Mixing and rare-set hitting must be discussed separately. No polynomial-time claim follows from successful runs.

## Source and workflow limitations

paper/figures/example.json is absent. The 13-vertex worked example was reconstructed from the figure-review search candidate with t0=4 and is labelled as a candidate throughout. The 16-vertex bad cover is reconstructed from the structure referee's saved file and matches its totals. EXPERIMENTS.md gives the positive and negative height histograms for all four requested worked cases subject to that source limitation.

The local map and dashboard are in labyrinth/. The frontier is intentionally empty because this task did not classify every value of a mathematical invariant at any size. It must not claim a resolved fraction for all rooted triangulations. Some event entries were backfilled from committed predictions and saved run outputs and are marked accordingly. The dashboard template needed Python UTF-8 mode on Windows; reproduction commands record it. This folder's SOTA is a local handoff, not an edit of the coordinator's canonical table.

## Three best next steps

1. Referee the half-pair tree-packing conjecture. Prove or refute its equivalent rank inequalities using the planar disk count, and independently verify the 27 explicit packing certificates. This could supply a direct fractional feasibility lemma.
2. Attack rounding after packing. Find a degree-preserving exchange that reaches a doubly rainbow tree, or a counterexample to a precisely stated monotone rule. The full-H weight fitting obstruction means this should start on a conditioned face rather than the full-support UST.
3. Referee the height-token involutions and add a root-defect potential to the sampler. Test feasible no-separator families separately from obstructed roots, and measure rare-set hitting rather than treating mixing as successful search.

## Leads for others

The exact factors at V=12 are short counterexamples suitable for the route map. The cube's 1/64 UST acceptance against perfect state acceptance is a useful warning that the two sampling spaces are different. The half-pair packing statement is ready to hand to the graph-theory and topology routes, but it is a conjecture rather than an established replacement for cancellation.
