COMPUTED: a fresh clone at 4eaee875 rebuilt all 31 upstream files, all submitted devices, and the 17-file replacement route.
COMPUTED: all 29 advertised theorems and the replacement main use only propext, Classical.choice and Quot.sound; theorem types and targeted dependency claims pass.
PROVED-HERE/COMPUTED: the sign/phase identity is correct; 174,763 sign words and 136 actual pairs pass independent numerical checks.
REFUTED: TODO T5 is too strong; the whole-Lemma-4.5 claim and the literal claim of no polynomial-library dependencies also need correction.
COMPUTED: the advisory route recount is 5 exact / 27 after translation / 2 without counterpart; canonical statuses remain unchanged under the user's all-checks condition.

# Independent Lean review report

## What I set out to do

Independently rebuild the author's Lean devices and replacement Barnette proof, audit the 29 formal statements against the current paper, trace dependencies without the author's walker, check the sign identity independently, and review the remaining formalisation targets. I used the repository's reverse-Lamport method and retained the distinction between a proved formal-model theorem and an unproved dictionary to the paper's objects. No subagents were used.

## What is established

COMPUTED. The fresh clone was `E:\lb2`, checked out at `4eaee87548250b2682affda7d05d947c05554bae`. I copied only `.lake/packages` from `E:\lbb`; none of its project build outputs were reused. All nine dependency repositories match the supplied manifest and have no tracked source differences. The 31 upstream sources and nine submitted Lean sources copied into the fresh project match their inputs. Input hashes did not change during the review.

The toolchain was Lean 4.34.1, commit `5045d0056413266e57c625dcd7c365b10e377c52`, and Lake `5.0.0-src+5045d00`, called through `C:\Users\Tom\.elan\bin\lake.exe`. Mathlib was `d13f23b723b8a846827a245b89c10fc7d3f11612`. The first upstream build was deliberately interrupted at 438 seconds to remain within the process limit, after the cold Mathlib import took 295 seconds. Resuming took 259.397 seconds and completed all 8,955 jobs. Devices and PaperRoute completed in 206.27 seconds, 8,963 jobs. No submitted Lean source failed to compile. Commands, exact timings, interruptions, and full sidecar outputs are in BUILD-LOG.md.

All 29 advertised axiom reports and the rebuilt main have exactly `propext`, `Classical.choice`, and `Quot.sound`. AXIOMS.txt retains them. A separate reviewer witness constructs an actual three-face triangle system with a pair and both signs, so the sign development is not merely a singleton or empty-type assertion. The source/configuration scan covered 29 files, including all generated copies, and found no occurrence of the requested forbidden tokens or any set_option line. The rejected drafts of my optional witness/checker are preserved as diagnostics and were never used; their final versions compile.

The generated Main.lean changes only its import. Its declaration is still `OAI.Barnette.main : OAI.Barnette.MainStatement`, using the identical Model.lean definition. Across all 17 generated files, sixteen first-line import prefixes change, Forest adds one import, and one theorem call changes at upstream Forest line 238. No theorem statement changes. The old/new abstract forest-pair theorem types are structurally identical in Lean's environment. MainStatement itself does not state the paper's prescribed-edge enhancement.

The independent walker follows types and bodies, including theorem bodies, and reports no missing constants. Original main reaches 36,722 constants; replacement main reaches 36,345. All six named old phase/nonvanishing dependencies disappear; the new forest-pair theorem, realSum_ne_zero, paperSign_reverse, sign_orient and finite_difference are reached. The original control reaches all six old dependencies. REACHABILITY.md contains the code, outputs and exact source diff explanation.

PROVED-HERE/COMPUTED. SIGN-CHECK.md proves the sign identity directly: if t=n-2N=3J, then epsilon/phase=i^(n-t-J)=i^n. It also derives the closed sign formula and the reversed-orientation convention. My own enumerator checks every admissible sign word through length 18 and every partner pair in all face rootings of the running triangulation and hexagonal bipyramid. All tests pass.

## What failed, and why

1. **TODO T5 is false.** It proposes surjectivity onto all eligible Hamiltonian cycles, while the paper proves a conditional characterisation of the construction's image. COUNTEREXAMPLE.md gives a complete explicit example in the hexagonal prism. There are four eligible Hamiltonian cycles and only two good states. A displayed cycle recovers a state whose opposite graph has components containing one, two and zero roots. This is an acyclic Q but not a good state. The failure is in the proposed TODO, not in a compiled theorem.
2. **The full-Lemma-4.5 wording is too broad.** Fiber cancellation with the real sign is checked. The total-sum theorem handles the case where no pair has acyclic Q. The paper's full equality to a sum over good states and their unique partners is not stated or proved by these files. The weaker theorem is sufficient for the replacement existence proof.
3. **“No polynomial lemma” is false if read literally.** The replacement still reaches 276 general Mathlib Polynomial declarations. An explicit path to Polynomial.eval₂_add runs through the unchanged exact-dual construction, strong rank condition and Noetherian polynomial-ring machinery. This does not use OpenAI's polynomial nonvanishing argument, and does not invalidate its replacement. The precise verified claim is elimination of that phase/polynomial argument, not elimination of every polynomial-library dependency. The generated build also still imports the old modules for structural definitions.
4. **The TODO inventory is incomplete.** RECOUNT.md lists omitted obligations, including full good-state/partner correspondence, the full cancellation equality, explicit rooted recovery, B1/B5, two-tree gluing, and remaining off-route statements. Some README/source wording also reverses the positive-step direction: step=-slope is positive when reversing an originally clockwise cycle, as the current paper correctly says.

Under the user's instruction to update statuses only if everything checks, I changed neither proofs/blueprint nor proofs/lean/README.md. No paper or submitted Lean proof was edited. RECOUNT.md is an advisory per-node recount, not a canonical status promotion. Its 5/27/2 totals retain the old blueprint's “weaker but covers the part used” convention, so they do not mean 32 whole paper statements are formalised.

## Paragraph for the synthesis and paper remarks

COMPUTED, independently rebuilt and audited: on OpenAI's Lean 4.34.1 development at commit 4eaee875, the real local-sign product, its reversal and closed-form identities, its relation epsilon=i^n phase, sufficient real-sign cancellation, local-weight additivity and finite differences provide a replacement proof of forest-pair existence that rebuilds the unchanged upstream Barnette main theorem with only propext, Classical.choice and Quot.sound. An independent environment walk confirms that the replaced phase/polynomial nonvanishing argument is absent from the main theorem's dependencies, although general polynomial-library dependencies remain elsewhere. The component-count conclusions for a finite connected graph with outdegree at most one and uniqueness of a forest perfect matching also compile. This does not formalise the paper's face-path heights, its complete good-state and unique-partner dictionary, its full good-state cancellation identity, its representative-independent minimum statement, its literal topological lemmas, explicit recovery or two-tree gluing. The proposed converse in TODO T5 must be replaced by the conditional image characterisation in the paper.

## What remains open

The formal-model replacement route is FOLLOWS in ROUTE-AUDIT.md. The literal complete paper route is NOT ESTABLISHED BY THIS PROOF because its translation and route-specific obligations remain. No failure found here challenges the compiled replacement main theorem. The validity of every upstream theorem as an exposition of geometry was not re-audited; imported Mathlib compiled artifacts were the explicitly permitted trust boundary.

## Three best next steps

1. Correct TODO T5 to the image-characterisation statement and narrow the README's whole-cancellation and polynomial-dependency wording. Then integrate this review's qualified verification and recount.
2. Prove the good-state/root-component bridge, partner uniqueness, and full real-sign cancellation equality; add the orbit-count invariance and all-pairs minimum corollary.
3. Define the paper's face-path weights and prove the B3 flow correspondence with the correct reversal direction. Keep explicit rooted recovery and two-tree gluing visible as separate unfinished work.

## Leads for others

The prism counterexample also illustrates why acyclic Q alone must never be substituted for “good state” without a partner/root-component argument. The 276 residual Polynomial dependencies arise in existing general algebra, so deleting whole phase/polynomial modules would require separating reusable definitions, not merely changing an import.

## Files and git

The required deliverables are BUILD-LOG.md, AXIOMS.txt, FAITHFULNESS.md, REACHABILITY.md, RECOUNT.md and this report. Supporting code, raw outputs, source hashes, generated.diff, the bounded audit and explicit counterexample are in this folder. Checkpoint commits were `32d51be` and `58fc728`; the completed evidence is committed separately. Only this research folder was staged by this review. A push of the checkpoints reported the remote already up to date. Final cleanup and push results are recorded below.

COMPUTED cleanup: the guarded PowerShell removal of E:/lb2 succeeded in 42.62 seconds. The directory no longer exists; E:/lbb remains present and was only read for the cache copy. cleanup.out records the checked target, upstream HEAD, timestamps and postconditions. No Lean or Lake process from the review remains.

Automatic approval review rejected removal of the ignored reviewer cache __pycache__/rebuild.cpython-314.pyc, including a nonrecursive exact-file attempt, with the reason 'blocked by policy'. The 5,737-byte cache remains untracked/ignored. This did not block removal of the fresh E:/lb2 clone.
