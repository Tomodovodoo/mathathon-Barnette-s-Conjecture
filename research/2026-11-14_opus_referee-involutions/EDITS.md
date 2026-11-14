# Proposed edits to proofs/involutions/ (15)

Each edit gives the exact current text of `proofs/involutions/involutions.tex` (unless another file is named) and its replacement. I have not applied any of them; the folder belongs to its author. E1 to E8 correct statements. E9 to E13 tighten the proof's wording. E14 fixes the figures. E15 propagates E2 and E7 to the Markdown files. Finding numbers refer to REFEREE.md.

## E1. Section 7 sign (F1, wrong for odd m)

Old:
```tex
 =(-1)^{\lceil n/2\rceil}\sum_{o\in\Omega}\sigma(o)
 =(-1)^{(n-m)/2}F.
\]
The last signs agree since $n\equiv m\pmod2$. This is the lowest
```
New:
```tex
 =(-1)^{\lceil n/2\rceil}\sum_{o\in\Omega}\sigma(o)
 =(-1)^{(n+m)/2}F.
\]
The last signs agree since $\lceil n/2\rceil+\lfloor m/2\rfloor=(n+m)/2$
when $n\equiv m\pmod2$. The height $H$ falls by $a(C)$ when a cycle $C$
turns from clockwise to counterclockwise, while the height $\omega$ of
the project's main paper rises by the same amount. This accounts for the
factor $(-1)^m$ between this formula and its Proposition~4.8. This is the lowest
```
Test: octahedron, n = 3, m = 1, F = 1; the middle term is +1. COMPUTED on all 880 paired roots through 14 vertices (`code/check.py`).

## E2. Class count (F2)

Old: `COMPUTED. The independent verifier checks all roots of all 56 unrooted`
New: `COMPUTED. The independent verifier checks all roots of all 55 unrooted`

## E3. Relation to the height proof (F6)

Old:
```tex
The height-product proof in the project fixes an indexed list of white
faces; here we allow all white faces and mark the actual crossings.
```
New:
```tex
The height proof in the project's main paper (Section 4) measures heights
along fixed paths of faces and expands $\omega(s)^m$ algebraically. Here
the paths are rays, and the expansion is replaced by marking $m$ actual
crossings. The second involution is a bijective form of its
finite-difference lemma: case 1 kills the monomials that miss a cycle,
and case 2 reduces each remaining factor to one first exit per enclosed
white face.
```

## E4. What Li writes and what Li leaves out (F5)

Old:
```tex
Appendix B states the extension, the fixed set and its sign, but leaves
the following checks implicit. The marks need a set or list convention.
A cycle choice needs invariant data. Once all cycles carry marks,
minimality forces exactly one mark on each cycle. Moving that mark cannot
invalidate another one. If the partner belongs to the other matching, the
cycle must be reversed even in the interior nonfirst-crossing case.
The selected cycle must remain selected on the return move. The fixed set
needs an independent orientation choice on each minimum cycle.
Lemmas~\ref{two} and \ref{fixed} supply these checks for every $m$.
```
New:
```tex
Appendix B states the set convention, the rule for an unmarked cycle,
the case of exactly $c_{\min}$ cycles with one mark each, the priority
rule (using the total order on cycles fixed in Li's Section 4.3), the
reversal along a single cycle in the exterior case, the fixed set and
its sign. It does not prove that all-marked objects have one mark per
cycle, that the map is an involution, or that it reverses sign; it says
only ``switch to the other edge'' in the interior nonfirst case, where
the cycle must also be reversed when the partner belongs to the other
matching; and it does not show that the fixed set is nonempty, which
needs an independent orientation choice on each minimum cycle.
The project's dependency audit of Li's note
(\texttt{research/2026-11-14\_fable\_dependency-graph/audit-li.md},
items L-F5 and L-F6) first identified these steps and sketched them.
Lemmas~\ref{two} and \ref{fixed} write them out for every $m$.
```

## E5. The m = 2 witness sentence (F5)

Old:
```tex
The issue is already present at $m=2$: a set of two tokens can lie entirely
on one cycle, so the unmarked-cycle rule is necessary. At $m=3$ a reversal
on a singly marked cycle must leave the other two token directions intact;
a global interchange of the matchings would not do this.
```
New:
```tex
These cases occur early. At $m=2$ a set of two tokens can lie entirely
on one cycle, so Li's unmarked-cycle rule is used. At $m=3$ a reversal on
a singly marked cycle must leave the other two token directions intact,
as Li's $M_1\triangle C_i$ does; the global interchange $(M_2,M_1)$ of
Li's one-cycle case would not.
```

## E6. Path lengths depend on the drawing (F4)

Old:
```tex
moment identity above. There are 4658 second fixed points. Alternating
paths from all of them have length zero or two, with maximum two.
```
New:
```tex
moment identity above. There are 4658 second fixed points. In our
drawings, alternating paths from all of them have length zero or two.
Path lengths depend on the drawing: an independent census with a
different generic direction finds a path of four moves, and the running
example with unsheared vertical rays has paths of six moves.
```

## E7. The 279/213 explanation (F3)

Old:
```tex
The listing uses that geometry, not the manuscript's optimized disk layout.
Marked-object counts depend on these choices. In particular the present
279 objects should not be identified with an earlier layout's 213 objects.
```
New:
```tex
The listing uses that geometry, not the manuscript's optimized disk layout.
The project's Li replay (\texttt{workings/barnette\_lab}) uses the same
recipe with roots $4$ and $5$ interchanged. That drawing is the mirror
image of ours, its rays cross other spokes, and it has $213$ objects,
none of them among our $279$. Both lists are correct. The number of
objects, the first fixed set and the path lengths depend on the drawing.
The signed sum $-9$ and the nine second-fixed objects do not, by
Lemma~\ref{fixed}: over 69 generic drawings the object count ranges
from $103$ to $363$.
```

## E8. Say at the definition that Ω depends on the drawing

Old:
```tex
The identical crossing may not occur twice. Let $\Omega$ be this finite set.
```
New:
```tex
The identical crossing may not occur twice. Let $\Omega$ be this finite set.
It depends on the drawing, since a ray swept past a vertex or a centre
gains or loses crossings. Only its signed size is used, and
Lemma~\ref{fixed} shows that the signed size does not depend on the drawing.
```

## E9. Spoke cycles: replace the sliding argument

Old:
```tex
same white-face points. To justify this assertion, the side and its detour
bound a subdisk in its black triangle excluding the third corner. Distinct
detours use distinct black triangles and have disjoint interiors. Sliding
successively across these subdisks preserves simplicity and orientation;
it never crosses a white-face point. This also handles a third corner that
lies elsewhere on the cycle. We call these the spoke cycles of $p$.
```
New:
```tex
same white-face points. Indeed, each detour lies in the interior of its
own black triangle apart from its two ends, and distinct triangles have
disjoint interiors, so the route is a simple closed polygon. It differs
from the side cycle by the boundaries of the small triangles
$r(t),t,s(t)$, which contain no white-face point. Winding numbers at
white-face points are therefore equal. Lemma~\ref{disk} puts a
white-face point inside, where both winding numbers are $\pm1$, so the
orientations agree. We call these the spoke cycles of $p$.
```

## E10. Lemma 2: the bijection count

Old:
```tex
inside the disk. State bijectivity gives $B=I+\ell$.
Indeed a black triangle inside must select an interior vertex, unless its
selected vertex is on the boundary. Every boundary vertex already has its
unique selected triangle supplying the outgoing boundary side. The latter
triangles are inside exactly for the $\ell$ specified sides. Conversely an
interior vertex can only select an inside triangle.
```
New:
```tex
inside the disk. State bijectivity gives $B=I+\ell$.
Indeed the state is injective, and an inside triangle selects a vertex of
the closed disk. An interior vertex is selected by some triangle, which
contains it and so lies inside. A boundary vertex is selected by the
triangle supplying its outgoing boundary side, which lies inside exactly
for the $\ell$ specified sides. So the inside triangles correspond to the
$I$ interior vertices and those $\ell$ boundary vertices.
```

## E11. Lemma 5, case 1: tokens stay valid

Old:
```tex
In case 1 the same cycles remain unmarked. The same first cycle is chosen
twice, and no token changes membership or direction.
```
New:
```tex
In case 1 the reversed cycle carries no token, so every token keeps its
spoke as an $s$-spoke and $M$ is a token set of the new pair. The same
cycles remain unmarked. The same first cycle is chosen twice, and no
token changes membership or direction.
```

## E12. Traversal of r-spokes

Old:
```tex
Call this partial pairing $P_{C,w}$. It depends only on the drawing, $C$,
and $w$. Two paired crossings have opposite directions when $C$ is directed,
because consecutive crossings alternate entry and exit.
```
New:
```tex
Call this partial pairing $P_{C,w}$. It depends only on the drawing, $C$,
and $w$. When $C$ is directed it is traversed $r(t)\to t\to s(t)$, so an
$s$-spoke is traversed away from its centre and an $r$-spoke towards it;
after reversal of $C$ the old $r$-spoke is an $s$-spoke traversed away
from the centre. Two paired crossings have opposite directions of
traversal, because consecutive crossings alternate entry and exit.
```

## E13. The order on cycles

Old:
```tex
Fix total orders on unoriented simple cycles, for example the lexicographic
order on their sorted supplying-face sets. Cycle choices below never use
their current direction.
```
New:
```tex
Fix total orders on unoriented simple cycles. Both maps compare only
cycles of one $Q_s$ or of one $D_p$, which use disjoint sets of faces,
so the lexicographic order on sorted supplying-face sets suffices.
Cycle choices below never use their current direction.
```

## E14. Figures 1 and 2: draw the rays and zoom

In `proofs/involutions/figures/marked.tex` (and the same two coordinates in each panel of `second.tex`), insert before the line
```tex
\node[draw=bfW,circle,fill=white,inner sep=1pt,font=\tiny] at (-0.112,-1.905) {$w_{5}$};
```
the two lines
```tex
\draw[bfW,densely dashed,thin] (-0.112,-1.905) -- (-3.353,3.709);
\draw[bfW,densely dashed,thin] (-0.849,-0.317) -- (-3.234,3.813);
```
These are the rays from w5 and w6, mapped into the figure's affine view: the exact vertical direction becomes (−0.500, 0.866) there (fit error 0.004 over all vertices). Then add a second, zoomed copy of the picture beside the first, made from the same file with `x=0.42cm,y=0.42cm` replaced by `x=1.45cm,y=1.45cm` and the bounding-box line replaced by
```tex
\path[use as bounding box] (-2.6,-2.2) rectangle (1.0,2.3);\clip (-2.6,-2.2) rectangle (1.0,2.3);
```
Tested: `code/out/figure1-proposed.png` shows both rays crossing the thick marked spokes t0 and t7. Add to the caption of Figure 1: "Dashed lines are the rays from $w_5$ and $w_6$, in the direction that is vertical in the exact layout."

## E15. Markdown companions (F2, F3)

`proofs/involutions/STATUS.md`, old: `56 classes, 1206 roots,` new: `55 classes, 1206 roots,`.
Old: `The original example.json is absent. The current running.json and a different exact layout are used and copied here. Earlier 213-object tables have not been identified with this 279-object set.`
New: `The original example.json is absent; running.json is used. The 213-object Li replay uses the same file and the same layout recipe with roots 4 and 5 interchanged. Both counts are correct; object counts depend on the drawing, the signed sum -9 does not.`

`proofs/involutions/INVOLUTIONS.md`, old: `All 56 classes through 14 triangulation vertices` new: `All 55 classes through 14 triangulation vertices`.
Old: `Earlier counts of 213 refer to a different geometry or input and are not silently reused.`
New: `The count 213 of the earlier Li replay comes from the same input in the mirror-image drawing (roots 4 and 5 interchanged). Object counts depend on the drawing; the signed sum and the nine second-fixed objects do not.`
