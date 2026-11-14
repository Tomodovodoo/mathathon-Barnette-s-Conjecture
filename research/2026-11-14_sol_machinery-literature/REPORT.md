Reviewed the proof machinery and neighboring theories with explicit source-access limits.
Established exact determinant-coefficient and prescribed-tree-degree reformulations, conditional where stated.
Separated Tutte's magic-number count from the additional disjoint-pair and forest conditions.
Delivered eighteen ranked routes, forty-seven bibliography records, and twenty-six public PDFs.
No independent replacement proof, scalar dimer product, or two-matroid shortcut was established.

## Scope and delivered files

The assignment was a tools-focused literature review, leaving the conjecture's historical development to another agent. I read the repository protocol, README, unslop skill and three supplied papers, then searched and fetched real sources. All changes made by this agent are inside `research/2026-11-14_sol_machinery-literature/`.

- `MACHINERY.md` identifies the exact ingredients of all three papers, classical neighboring theorems, their use sites, and what those theorems do not prove. Its final table gives the main input statements and general-versus-specific classification.
- `REFORMULATIONS.md` gives eleven formulations and comparisons, including explicit determinant formulas with proofs. The downstream induced-tree formulation is carefully distinguished from a global equivalence for every rooted matching problem.
- `ROUTE-IDEAS.md` ranks eighteen candidate approaches, each with a finite afternoon test and a stated obstruction or missing theorem.
- `bibliography.bib` has forty-seven records. Unread originals and preprints are marked. No original Bonichon title was guessed; its exact conference record was located.
- `pdf/INDEX.md`, `downloads.json`, `source-text/` and `SOURCES.md` record public sources, hashes, reading depths and failures. Twenty-six PDFs were actually downloaded. Bonichon's original host failed certificate validation and is recorded as a failure rather than a downloaded file.
- `fetch_sources.py` reproduces downloads and text extraction. `check_determinant.py` and `determinant-check.json` reproduce the exact small-instance determinant comparison.

## Established

[LIT] O's states are planar Tutte states, after swapping the two face colors. Their number is the trinity magic number, equivalently the absolute determinant of the face/nonroot incidence matrix. The checked modern sources are Hine-Kálmán and Kálmán's hypergraph paper. The original Tutte and Berman proofs were not obtained, and this limitation is explicit.

[PROVED-HERE, conditional on O's disk identity] The weighted pair sum admits the exact formula

    Z_b = [product_t z_t] det(sum_t z_t M_t),
    M_t(u,v) = q^{delta(u,v)} b(t,v),  u != v corners of t,
    q = exp(pi i/6).

All other entries are zero. Coefficient extraction forces each face exactly once. The determinant permutation has only odd cycles by the disk identity, so every surviving sign is positive before the phase weight. This is a mixed determinant, not a claim that a single ordinary determinant evaluation computes Z. Inclusion-exclusion gives a valid sum of 2^n determinant evaluations.

[PROVED-HERE] The target tree matchings are counted by a positive coefficient in the spanning-tree degree polynomial. Weight spoke uv by y_u y_v and take a Laplacian cofactor. The coefficient of the prescribed retained degree sequence counts exactly those trees whose complements are states. This is also the precise simultaneous two-sided hypertree-realization problem.

[PROVED-HERE] The local turn phase cannot factor as a scalar weight on r times a scalar weight on s when three nonroot corners are allowed. Its two cyclic triple products have ratio -1, whereas any separated factorization has ratio one. This blocks the simplest product of dimer determinants. It leaves planar gadget, block-matrix and connection approaches open.

[PROVED-HERE] The natural matroid formulation has two endpoint partition matroids and the graphic matroid of opposite edges after root identification. The tempting union of the endpoint constraints is not a matroid, as the K_2,2 augmentation counterexample shows. Rado's criterion is derived from the checked Edmonds theorem in the reformulations file, so its statement does not rest on pretending to have read the inaccessible original.

[COMPUTED] On the rooted even bipyramids of rim lengths 4 and 6, the direct pair sum and symbolic determinant coefficient agree exactly. They have n=3 and n=5, two and three states, respectively, and two ordered disjoint pairs each. Distinct positive integer incidence weights give coefficients -51 q^3 and -20775 q^3 in the cyclotomic field. Script and command are recorded. These two checks verify the implementation and illustrate the formula; the general formula has a written proof, and the computation does not establish any candidate route on arbitrary maps.

## What failed or stopped

[REFUTED] The naive scalar dimer factorization and the proposed “matching matroid intersect graphic matroid” reduction fail for the explicit algebraic and augmentation reasons above. These are narrow negative conclusions. No general impossibility theorem for Pfaffian gadgets or alternative matroid reductions is claimed.

[HUNCH] No theorem in the checked trinity, clock, hypertree, root-polytope or Floer sources automatically supplies the disjoint state pair with the desired forest. One-state cardinality, a connected clock lattice, separately feasible degree vectors and a Floer support polytope all omit a constraint. The exact missing condition is stated for each proposed route.

[HUNCH] I did not identify Z with a standard unmodified SL2 or U(1) double-dimer partition function. The exclusion of doubled edges, local turn dependence, and nonflat positive circulations must all be represented. A flat connection on the unpunctured sphere cannot supply the needed contractible-loop holonomy. The least-zero-order argument is exact; a Lee-Yang circle theorem is not established.

Several older originals could not be fetched. Their metadata and modern formulations were checked where possible, and theorem-level access limits are in `SOURCES.md`. Full proofs of the Floer, map-bijection and generic invariant results were not independently audited. The exact Eulerian-triangulation specialization of the constellation decoder is located as a map class, but its behavior on the extra state constraints is still open.

## Leads for others

[LIT, preprint claims only] The general Albertson-Berman conjecture should not be described using an outdated still-open label without checking current sources. August 2026 preprints by Makarov and Jung report counterexamples. Their public abstracts and PDFs were checked; their verifiers and proofs were not independently audited. This does not refute the Eulerian-triangulation statement relevant here.

[PROVED-HERE] The ordinary Yutsis two-induced-tree partition is a partition of the original cubic graph's vertices. The Barnette induced-tree formulation concerns its dual triangulation's vertices. These are different ground sets and should not be conflated in the exposition.

[HUNCH] The mixed-determinant identity may be useful to the dimer and constructive-route agents. It provides an exact formula to compare against any proposed ordinary determinant, Pfaffian gadget or symbolic polynomial. It does not establish novelty relative to all existing literature; no such claim was searched exhaustively.

## Three best next steps

1. Extend the exact determinant comparison to the shared triangulation corpus, including three-nonroot black faces and both separator colors. Test legal gauges of the rank-two matrices before invoking any positivity theorem.
2. Enumerate the common degree-vector support of H-trees and compare it with the corresponding hypertree relaxations. Find the smallest obstruction to any proposed one-sided or convex-hull argument.
3. Test pair-level height potentials and local matchgate signatures. Either can produce a precise small counterexample quickly, or a concrete map worth proving.

## Git and reproducibility

The first stable source collection was committed as `7ef9eb8`; the machinery, routes and determinant formula were committed as `8c96d08`. Every commit stages only this folder and ends its message with `Co-Authored-By: GPT-6.1-sol`. A final source-ledger/report commit and a push attempt follow this report. Other agents' shared-tree changes were left untouched.

Reproduction commands are the downloader, the determinant check, `python research/2026-11-14_sol_machinery-literature/validate_sources.py`, and the page-render command in `SOURCES.md`. The final validation passed for required files, local PDF links, download hashes, bibliography uniqueness and exact determinant outputs. An initial metadata check used Windows' default text encoding and failed on a UTF-8 quote; the saved validator explicitly reads UTF-8 and passes. No large computation or long-running search was used.
