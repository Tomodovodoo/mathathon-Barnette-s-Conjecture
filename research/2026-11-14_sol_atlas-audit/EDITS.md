# Exact proposed edits

All mathematical corrections below have the status and evidence given in AUDIT.md. These are proposals against the snapshotted sources, not direct edits. The atlas text owner may already have replaced terminology. Preserve the mathematical distinction after renaming.

## E1. digestions/atlas/pages_more.py

Old:
```text
If they form a forest, the determinant is plus or minus one.
```
New:
```text
If they form three trees, each containing exactly one root, the determinant is plus or minus one. Acyclicity alone does not suffice: states without a partner can have a tree joining roots.
```

Exact substring present in retained source snapshot: True.

## E2. digestions/atlas/pages_more.py

Old:
```text
The edges opposite the wedges form a forest.
```
New:
```text
After identifying the three roots, the edges opposite the wedges form a spanning tree. Before identification they form three trees, one at each root.
```

Exact substring present in retained source snapshot: True.

## E3. digestions/atlas/figs_order.py

Old:
```text
Among the 12 states, the number that fail this way is {nb}.
```
New:
```text
Among the 12 states, {nb} has an ordinary cycle. Five more fail root separation, so only six meet the forest constraint after root identification.
```

Exact substring present in retained source snapshot: source was not retained; check against current file.

## E4. digestions/atlas/figs_order.py

Old:
```text
For every set of vertices, the opposite edges inside it weigh at most its size minus one
```
New:
```text
Identify the three roots first. For every set of the resulting vertices, the opposite edges inside it weigh at most its size minus one
```

Exact substring present in retained source snapshot: source was not retained; check against current file.

## E5. digestions/atlas/pages_more.py

Old:
```text
So the relaxed problem has fractional corners and rounding it fails.
```
New:
```text
So this relaxation has fractional corners. An arbitrary optimum need not be a state; a rounding algorithm would need an additional argument.
```

Exact substring present in retained source snapshot: True.

## E6. digestions/atlas/pages_more.py

Old:
```text
The first half fails.
```
New:
```text
Mean fitting on the full spoke graph with finite positive weights fails.
```

Exact substring present in retained source snapshot: True.

## E7. digestions/atlas/pages_more.py

Old:
```text
Writing the signed sum as a difference of two positive measures restates the proof and does not replace it.
```
New:
```text
This obstruction does not rule out measures conditioned on the forced spokes. The signed-measure identity alone supplies no new existence proof.
```

Exact substring present in retained source snapshot: True.

## E8. digestions/atlas/pages_more.py

Old:
```text
Lift or rotate settles 98.3 per cent of the failing cases up to 16 vertices. The rest need a rule nobody has found.
```
New:
```text
Rotation repairs 27,723 of 28,189 failing lifts through 16 vertices, leaving 466 exceptions. All have the two-sided outer-forest pattern described by the induction referee. Some contraction has no successful direct lift at 18 vertices; the weaker lift-or-rotate existence question remains open.
```

Exact substring present in retained source snapshot: True.

## E9. digestions/atlas/pages_more.py

Old:
```text
The lift and the rotation were proved in an unrefereed report. The two remaining statements are conjectures, tested on all 344,872 contractions up to 17 vertices.
```
New:
```text
The lift criterion and rotation were checked by an independent referee. The contraction inequality was independently tested on 344,872 contractions through 17 vertices and 857,920 at 18. The pair-preserving contraction question and the remaining lifting step are still open.
```

Exact substring present in retained source snapshot: True.

## E10. digestions/atlas/pages_more.py

Old:
```text
In the present language their tree is an induced tree whose vertices outside one colour class are pairwise non-adjacent, as in (c).
```
New:
```text
The relaxed radial-tree dictionary asks for one induced tree whose vertices outside a chosen colour class are pairwise non-adjacent. Feder and Subi additionally require every omitted quasi vertex to have degree four and no incident digon. Panel (c) separates these conditions and shows a 10-vertex example where the relaxed condition excludes one of fourteen cycles.
```

Exact substring present in retained source snapshot: True.

## E11. digestions/atlas/pages_more.py

Old:
```text
This project tested it. It fails first at 18 vertices, where both extremes lack one.
```
New:
```text
This project tested it. An independently checked 18-vertex example has no good direction at either extreme. An all-root census through 18 vertices found no smaller example.
```

Exact substring present in retained source snapshot: True.

## E12. digestions/atlas/pages.py

Old:
```text
The marks are not drawn, and their code was checked on the cube only.
```
New:
```text
The proposed ray panel draws an actual crossing-pairing move. The full marked construction has since been independently checked on all 1,206 rooted instances through 14 vertices; see the involutions referee. The single displayed token is not the whole marked set.
```

Exact substring present in retained source snapshot: True.

## E13. digestions/atlas/figs_scope.py

Old:
```text
('exchange descent on rainbow trees reaches a tree matching', 16, 120)
```
New:
```text
('exchange descent on rainbow trees reaches a tree matching', 17, 120)
```

Exact substring present in retained source snapshot: True.

## E14. digestions/atlas/figs_scope.py

Old:
```text
('every maximal chain of covers has one', 60), ('half of all covers have one', 70)
```
New:
```text
('every maximal chain of covers has one', 33), ('half of all covers have one', 33)
```

Exact substring present in retained source snapshot: True.

## E15. digestions/atlas/figs_scope.py

Old:
```text
refuted, first failure at
```
New:
```text
refuted, counterexample known at
```

Exact substring present in retained source snapshot: True.

## E16. digestions/atlas/pages_more.py

Old:
```text
Every number on the chart is quoted from an unrefereed report of this project and was not recomputed here.
```
New:
```text
The chart combines source-reported tests with independent referee replays. The counting conjecture is independently checked through 22 vertices in the all-root census. The separate separator-free campaign reports 23,824,742 facial-root occurrences through 24 vertices, independently replayed only through 16. This atlas audit did not rerun those large censuses.
```

Exact substring present in retained source snapshot: True.

## E17. digestions/atlas/pages_more.py

Old:
```text
The descent survived all 34.8 million such trees up to 16 vertices and remains a conjecture.
```
New:
```text
The descent remains a conjecture. The topology referee enumerated every rainbow tree through 16 vertices, then at 17 vertices enumerated 34,659,072 trees in the 1,119 multi-cover instances and used its single-cover theorem for the other 6,923 instances.
```

Exact substring present in retained source snapshot: True.

## Figure replacements

Use the mapping in `digestions/atlas/proposed/README.md`. Page 22 must say six connection signatures, with alternating word 0101 split 8 + 4; five label words remain correct. Replace the page 24 caption rather than applying its original all-28 caption to the new example.

For page 28 add R2 as a refuted row at 33 and name its scope, an extreme or join- or meet-irreducible cover. Keep monotone descent as a separate open row. Split the contraction row into the pair-preserving choice G and the tree-count inequality L+, since their evidence ranges and statements differ.

For greyscale legibility, locally thicken white-tree dash-dot strokes to 1.5 pt in panels 8(b), 8(c), 19(a), 19(b), 21(a), 21(c). Keep the current dash patterns. Make Q strokes black dashed with a white halo where they sit exactly on base edges. Do not change the mathematical selection.

For page 23 replace the generation-theorem opening by "Euler's formula supplies a non-root vertex of degree four. Removing it and merging one pair of opposite neighbours suggests induction." Cite fable_induction-completion/REFEREE.md and astra_induction-lemmas/G.md.