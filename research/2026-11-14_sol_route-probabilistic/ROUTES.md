# Routes

New proofs are T2 unreviewed. COMPUTED means T4 evidence from the named scripts, not independent certification. Literature inputs retain their source status. No positive-measure existence proof was found.

| Route | Status | Result and stopping point |
| --- | --- | --- |
| Full-H positive weights with target mean | REFUTED, PROVED-HERE | Impossible on every instance, already the cube. The target forces outer and root spokes; a finite positive UST has full support. PROOFS 2. |
| One-sided Lorentzian or hypertree support | LIT; PROVED-HERE application | Linear substitution gives a stable, hence Lorentzian degree polynomial on one class. Its M-convex support has no lattice holes. This addresses one degree family only. |
| Two-sided Lorentzian support | REFUTED | Bilinear substitution is outside the closure theorem. The six-cycle has a hand-proved M-exchange obstruction; code/campaign.py finds a cube H obstruction. PROOFS 4. |
| Target fractional membership from a pair | CONJECTURE | Half the two state indicators on the white graph appears to lie in the tree polytope. Equivalent conjecture: their 2n selected dual edges split into two white spanning trees. Subset tests in 278 nonvacuous rooted samples out of 425 tested, plus explicit packing in 27 larger samples, have no failure. |
| Fractional feasibility alone rounds | HUNCH, unresolved | It would require a joint-degree integrality statement special to spoke graphs. A half-integral vertex elsewhere in the slice neither proves nor disproves that target statement. |
| Entropy or matrix scaling | PROVED-HERE reduction; open | Mean fitting characterises relative interior of the convex hull, not integer support. Full-H fitting diverges. After conditioning, boundary faces still need diagnosis. No numerical weight optimum is claimed. |
| Pipage, swap, or negative-correlation rounding | HUNCH, unresolved | Matroid base rounding preserves expected edge marginals, not both degree families exactly. Even a partition into two white trees gives correct means while individual trees can violate both labels. A disk-specific degree-preserving rounding lemma would be new mathematics. |
| Determinantal or strongly Rayleigh UST | LIT; route open | The edge indicator process is determinantal. Vertex degrees are sums of those indicators, not themselves a determinantal point process. Negative association bounds tails but does not give a lower bound for a simultaneous exact event on overlapping stars. |
| Second moment for the exact degree event | PROVED-HERE diagnosis | Its indicator I has E I^2=E I. Paley-Zygmund reduces to Pr[I>0]>=E I, so evaluating the first moment is already the problem. A useful second moment needs a different witness count. |
| Local lemma for degree failures | HUNCH, no verified criterion | UST degrees are dependent across the whole graph. A dependency graph based only on overlapping stars is invalid. No valid lopsided dependency criterion and numerical threshold were supplied by this work. |
| Signed measure as two probabilities | PROVED-HERE conditional | Uniform pair signs are fair. Pushing forward the signed measure kills nonforest states. The two forest-sign measures have matching low height moments and differ at degree c_min. PROOFS 5. |
| Raw sign coupling leaves all forests unmatched | REFUTED as a strict-imbalance proof | At weight one both total sign masses are equal, including the forest contribution. An injection cannot prove a surplus of that unweighted sign. |
| Height-marked coupling | PROVED-HERE conditional | Integer-shifted heights give a finite marking and two explicit involutions. Their alternating walk ends at a marked forest pair. It is the same signed mechanism in height coordinates, with no efficiency bound. PROOFS 6. |
| Cycle-count Gibbs measure | REFUTED as a sufficient potential | Acyclic Q need not mean one root per component. The hexagonal prism already has a zero-cycle non-tree state. On rare tubes many bad states retain zero penalty. |
| White-face triangle-flip descent | COMPUTED, unresolved | Uniform proposals, accept nonincreasing cycle rank. It succeeds in 12/12 trials on the 50-vertex subdivision sample and 0/12 on the rare 54-vertex tube within 2000 proposals. This is a heuristic hitting result, not a mixing theorem. |
| Fast mixing implies fast tree search | REFUTED as an inference | Even a perfectly mixed sampler has success density M/S. The no-separator width-4 family has exponentially small M/S. Finite spectra and first hitting equations are in data/mixing.json. |
| Real-rooted signed polynomial in z | REFUTED | First in this scan at V=10, prism8, normalized 1-z^3. Nonreal cube roots of unity. |
| All roots on the unit circle | REFUTED | At V=12 index 2 outer 0, normalized polynomial is (z-1)(z^2+3), with roots plus/minus i sqrt(3). |
| Real-rooted linear-weight polynomial | REFUTED | V=12 index 0 outer 0 gives x(x+1)(2x+1)(2x^2+5x+4). Last factor has discriminant -7. |
| Family root formulas | LIT within project; checked finite cases | Prism and nested-prism product formulas give roots of unity. Those special families are misleading as a universal Lee-Yang prediction. |

## Scope of the fractional conjecture

CONJECTURE. For every rooted instance with a disjoint pair r,s, let E_pair be the 2n white dual spokes selected by r or s. Then E_pair decomposes into two spanning trees of W. Each edge retains its identity when parallel edges occur. The convex mixture of those two trees puts marginal 1/2 on E_pair and zero elsewhere, hence has the prescribed mean count one at each face label and nonroot label.

Test. Enumerate every pair support at the next graph order, or use code/packing.py on a new family. A negative result must include a subset S of white vertices with more than 2|S|-2 selected edges internal to S, or an independently checked matroid-union obstruction. Our augmentation routine only certifies its positive outputs by checking the two resulting trees; failure of its search alone would not be a theorem.

PROVED-HERE, conditional on this conjecture. The target belongs to the degree projection of the H spanning-tree polytope. Complement each white tree to an H tree and average. The deleted edge marginals are 1/2 on r union s, zero elsewhere. Since each state uses each bounded centre and nonroot once, the expected H degrees are exactly d*. This constructs a boundary-supported tree distribution, not a finite positive UST on all H.

## What the saturation ladder changed

The search changed from polynomial support to convex expectations, then to explicit two-tree packing. It changed parameter from graph order to cycle rank and root defects. Rare tubes supplied the extreme cases. Dropping the spoke hypothesis exposed a six-cycle obstruction to the claimed closure theorem. Inverting the question led to the concrete half-pair cut inequalities. The imported communities were Lorentzian polynomials, determinantal probability and exponential families. The height-marked lemma replaces circulation token pools by shifted-height token pools but removes no signed comparison. Existing referee reports were read, including the new average-load warning in the topology referee folder. A wider agent campaign was not authorised by this sub-agent brief. These are the rungs used, not a claim that every remaining route is saturated.

## Literature read

LIT. Branden-Huh, Lorentzian polynomials, Annals of Mathematics 192, 2020, 821-891. Full HTML opened, https://arxiv.org/html/1902.03719v6 and publisher page https://annals.math.princeton.edu/2020/192-3/p04 . Linear nonnegative substitutions preserve Lorentzian polynomials; bilinear edge-to-endpoint substitution is not that theorem.

LIT. Borcea-Branden-Liggett, Negative dependence and the geometry of polynomials, JAMS 22, 2009, 521-567, https://arxiv.org/abs/0707.2340 . Abstract opened and read, confirming UST membership in the strongly Rayleigh class. No attempt here to reprove its negative-association theorem.

LIT. Kalman, A version of Tutte's polynomial for hypergraphs, Advances in Mathematics 244, 2013, 823-873, https://arxiv.org/abs/1103.1057 . Abstract opened. It states the integer polymatroid description of hypertrees. Do not attribute the two-sided extension to this source.
