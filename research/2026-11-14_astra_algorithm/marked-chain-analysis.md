## A candidate exponential marked-walk family

The fixed-flow marked constructor was run on the recursively labelled trap chains with k=1,...,10. Its completed move counts for k=1,...,8 are

```
0, 5, 14, 113, 562, 2811, 14060, 70309.
```

The eight-factor case has 210 primal vertices and completed in 79.794269 seconds with eight phases, decreasing the D count at unsuccessful endpoints from 24 to 10 in steps of two. The first run censored k=8,9,10 at twenty seconds; only k=8 was rerun with a larger cap. The initialization uses the flow pair at every k, not a specially substituted bad pair. Exact graph labels, roots, starting pairs, returned cycles and software versions are saved in marked-chain-instances.json, marked-chains.jsonl, marked-chain-eight.json and manifest.json. The first factor's normalization count can depend on the orientation in which the flow union is traversed; the marked count follows the all-counterclockwise normalized start.

**Conjecture, fixed rule.** For this labelled chain construction, the reference flow cover, the reference positive weights and the manuscript's ordered-cycle/ordered-token rule, the number of marked moves for every k>=4 is

```
L(k) = (9*5^(k-2)-2*k+9)/2.
```

It agrees exactly at k=4,...,8. Equivalently, the observed recurrence from k=5 is `L(k)=5L(k-1)+4k-23`. Testing k=9, then identifying a local marked-state transition invariant, is a concrete next step. The five verified values do not prove an exponential lower bound. The shortest-path lower bound remains the earlier linear one. Different starting covers, weights or tie rules need not obey this conjecture.

The following elementary theorem explains a possible mechanism, without identifying it with the Barnette walk.

**Theorem, abstract involution product.** There are two polynomial-time computable sign-reversing involutions on objects encoded with O(k) bits whose alternating path from a specified alpha-fixed object has exactly `5^k-1` moves before it reaches a beta-fixed object.

**Proof.** On `{0,1,2,3,4}` let alpha fix 0 and interchange 1 with 2 and 3 with 4. Let beta interchange 0 with 1 and 2 with 3 and fix 4. On k-tuples, apply alpha to the first coordinate not fixed by its local alpha, fixing the tuple if none exists. Define beta the same way using its local rule. These are involutions because the first eligible coordinate remains the first eligible coordinate after its swap. Each nonfixed move reverses `(-1)^(sum of coordinates)`. The unique alpha-fixed tuple is all zero; the unique beta-fixed tuple is all four.

For k=1 the alternating walk is 0,1,2,3,4, of length four. Suppose the remaining k-1 coordinates have an alternating path of length D. The first coordinate traverses 0 to 4 in four moves. There beta fixes that coordinate, so the next beta move acts on the remaining tuple. Alpha then traverses the first coordinate back from 4 to 0, again in four alternating moves. At zero alpha fixes that coordinate, so the next alpha move acts on the remaining tuple. Continue. Thus the remaining tuple takes its own alternating path, while coordinate one makes a complete four-edge sweep before the first remaining-tuple move, between consecutive such moves, and after the last. There are D+1 sweeps and D remaining-tuple moves. Induction gives D=`5^(k-1)-1`, which is even, so the last sweep ends at 4. The total is `4(D+1)+D=5^k-1`, and the endpoint is all four. Testing the first eligible coordinate takes O(k) time and the encoding has k digits. QED.

This is a lower bound for the abstract first-eligible involution rule. It proves that finite path structure, sign reversal, efficient move evaluation and a known start endpoint do not by themselves imply a polynomial path. To turn it into a Barnette lower bound one must embed the product transition system in the actual token dynamics, including the priority given to unmarked cycles, pool ranks, restart normalization and the face ordering. That embedding is not established here. The matching factorization across white-face gluings does not automatically factor the marked walk.

