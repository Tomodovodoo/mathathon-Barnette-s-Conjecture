# What cycle lower bounds follow from this proof?

## Fixed roots and prescribed edges

PROVED-HERE, T2 unreviewed here, using the independently refereed Theorem B and recovery injection. If the root t admits a pair, let c_t be its minimum D-cycle count and M_t its tree-matching count. For each of the three incident primal edges e at the corresponding primal vertex,

    H_avoid(e) >= M_t >= 2c_t,
    H >= 3M_t >= 6c_t.

The first inequality is an injection; the factor three uses disjoint avoidance classes at one cubic vertex. A Hamiltonian cycle omits exactly one of that vertex's incident edges. The conjectural bound M_t>=2^c_t would replace the last bounds by H_avoid(e)>=2^c_t and H>=3*2^c_t. It is not used as a theorem.

PROVED-HERE. Varying the root gives H>=3 max_t M_t, over feasible roots. For an edge e with primal endpoints u,v, use the larger of M_u,M_v, allowing a color swap to make either root black. If neither admits a direct pair, these direct bounds are unavailable; zero is a safe lower bound, not a declaration that no avoiding cycle exists. Since every Hamiltonian cycle omits exactly N/2 of the 3N/2 edges,

    H >= (2/N) sum_e max(M_u,M_v).

Proof: sum the individual avoidance inequalities and use sum_e H_avoid(e)=(N/2)H. Repeated root images must not be counted as distinct cycles. No linear or exponential lower bound in N follows merely by multiplying the number of roots by the fixed-root bound.

## Separators and a universal six

PROVED-HERE conditional on the supplied forest-pair theorem. Decompose the dual into b irreducible pieces along separating triangles. Every piece, at every facial root, has a pair and hence at least two tree matchings by the degree-zero signed identity. For a fixed prescribed outer edge, choose any one of these two local recovery cycles independently at every recursive piece, prescribing the interface pattern inherited from the previous piece. Distinct local choices give distinct global induced-tree partitions because restriction recovers the local partition, as proved in FAMILIES.md's gluing argument. Therefore

    H_avoid(e) >= 2^b,   H >= 3*2^b >= 6.

This counts a recursively assembled construction. It does not claim that an obstructed global root has 2^b direct tree matchings. When stronger local M bounds depend on the induced cap root, a safe multiplicative bound uses each piece's minimum M over facial roots. Using its maximum instead is unjustified.

PROVED-HERE. The cube has exactly six Hamiltonian cycles, so the constant six is tight as a graph-independent lower bound. This proof does not show six is attained at unbounded order. Even prisms have H=N/2+2 and admit no triangular separators, so no universal exponential-in-N lower bound is possible for the full Barnette class. This does not exclude stronger bounds for subclasses with bounded face sizes or for graphs with linearly many irreducible pieces.

## Comparison with opened literature

LIT. Jan Florek, "Remarks on Barnette's conjecture", Journal of Combinatorial Optimization 39, 149-155, 2020, Theorem 1, DOI 10.1007/s10878-019-00460-8. For a cubic 3-connected bipartite plane graph P having a 2-factor consisting of facial quadrilaterals, he proves at least 3^ceil(2|P*|/Delta(P*)^2) Hamiltonian cycles. The publisher's full HTML, including the precise hypothesis and theorem, was opened. This is a conditional subclass bound, not a bound for every Barnette graph. [Publisher source](https://link.springer.com/article/10.1007/s10878-019-00460-8).

LIT, preprint statement checked in the author's abstract. Jan Florek, "A sufficient condition for cubic 3-connected plane bipartite graphs to be hamiltonian", arXiv:2309.09578v2, 1 May 2024. Under its stated no-more-than-four-big-neighbors setting, the abstract also gives a 2^k cycle bound when every vertex meets both a small and a big face, with k=ceil((|B|-2)/(4Delta(B)-7)). Here big means size at least six. I opened the abstract but did not audit the theorem's proof or all interactions of its hypotheses. Treat this as a source-checked literature lead, not an independently checked theorem application to these tubes. [Author's abstract](https://arxiv.org/abs/2309.09578v2).

LIT. Irene Pivotto and Gordon Royle, "Highly-connected planar cubic graphs with few or many Hamilton cycles", arXiv:1901.10683v2, 14 February 2019, Sections 2,5,6. Their full HTML constructs cyclically 4-edge-connected cubic planar graphs with exactly four Hamilton cycles and develops fixed-width nanotube transfer matrices. Those graphs are not asserted to be bipartite. Their introduction recalls the Smith parity consequence that a Hamiltonian cubic graph has at least three Hamiltonian cycles. Thus our six is stronger in the supplied Barnette setting, while their four-cycle families forbid naive linear lower bounds in the broader cubic planar class. [Author source](https://arxiv.org/html/1901.10683v2).

LIT in the supplied OpenAI manuscript. Corollary 7.1 gives avoidance of every prescribed edge but no numerical multiplicity. The six-cycle statement adds the signed balance and injectivity already developed in the finished research reports. The source paper explicitly declines a polynomial-time construction. None of the exact counting recurrences here establishes a general efficient algorithm.

No assertion of a current optimal universal lower bound for bipartite cubic planar graphs is made. That question would need a dedicated literature audit. The opened sources settle the comparisons just stated; other search results were not promoted to verified citations.
