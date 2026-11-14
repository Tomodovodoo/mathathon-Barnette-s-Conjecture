## Worked examples

These are exact, reproducible arithmetic traces, with every exchange and recovery choice listed. `examples.py` generates them from the input graphs; they are computed examples, not additional existence proofs. Neither example requires separator gluing.

### Cube

Dual face IDs are the following ordered triples. The outer face is 0; roots are [0, 1, 2]; the prescribed dual side is (0, 2).

| Face | Corners | Colour |
|---|---|---|
| 0 | (0, 2, 1) | black |
| 1 | (0, 4, 2) | white |
| 2 | (0, 3, 4) | black |
| 3 | (0, 1, 3) | white |
| 4 | (1, 2, 5) | white |
| 5 | (1, 5, 3) | black |
| 6 | (2, 4, 5) | black |
| 7 | (3, 5, 4) | white |

The state coordinates below are in face order A=[2, 5, 6]. Nonroots are [3, 4, 5].

An integral value-6 flow chooses r=(3, 5, 4) and s=(4, 3, 5). Each X vertex and A face has degree two in their union. All other incidence arcs carry zero. Alternating each union cycle gives these two states.

There are 2 states and 2 pairs by exhaustive enumeration. For a nontrivial walk when available, start instead at r=(3, 5, 4), s=(4, 3, 5).

Its D cycles, specified by supplying faces, are [(2, 5, 6)]. Its Q cycles are [].

Nonzero spoke weights `(face,corner,weight)` are [(6, 4, 1)].

The signed polynomial in these weights is {0: 1, 1: -1}, written as exponent-to-coefficient entries.

Phase 1, h=1.
Normalize D cycle (2, 5, 6): r=(4, 3, 5), s=(3, 5, 4).
Initial excess-rank tokens are ((6, 1),); alpha fixes this object.
Beta fixes the object: the second state is good.

The opposite edges Q_s are [(0, 4), (1, 3), (2, 5)].

The white tree is [[1, 7], [3, 7], [4, 7]], rooted at 1.

| Black face | Deleted corner | White edge | Child | Selected side |
|---|---|---|---|---|
| 2 | 3 | (3, 7) | 3 | (0, 3) |
| 5 | 5 | (4, 7) | 4 | (1, 5) |
| 6 | 4 | (1, 7) | 7 | (4, 5) |

Add e0=(0, 2). The selected sides are [(0, 2), (4, 5), (0, 3), (1, 5)]. The two induced-tree classes are [[0, 2, 3], [1, 4, 5]].

The primal cycle, using dual face IDs, is [0, 3, 5, 7, 2, 1, 6, 4], closed back to its first vertex. The omitted edge is (0, 1). Each consecutive pair shares a side in the face table, and the list contains all 8 face IDs exactly once. The independent primal checker accepts it.

### 13-vertex running triangulation

Dual face IDs are the following ordered triples. The outer face is 2; roots are [0, 4, 5]; the prescribed dual side is (0, 4).

| Face | Corners | Colour |
|---|---|---|
| 0 | (0, 6, 1) | black |
| 1 | (0, 5, 6) | white |
| 2 | (0, 4, 5) | black |
| 3 | (0, 3, 4) | white |
| 4 | (0, 2, 3) | black |
| 5 | (0, 1, 2) | white |
| 6 | (1, 6, 7) | white |
| 7 | (1, 9, 2) | black |
| 8 | (1, 8, 9) | white |
| 9 | (1, 7, 8) | black |
| 10 | (6, 5, 11) | black |
| 11 | (6, 12, 7) | black |
| 12 | (6, 11, 12) | white |
| 13 | (2, 9, 3) | white |
| 14 | (3, 9, 4) | black |
| 15 | (4, 11, 5) | white |
| 16 | (4, 10, 11) | black |
| 17 | (4, 9, 10) | white |
| 18 | (7, 12, 8) | white |
| 19 | (8, 10, 9) | black |
| 20 | (8, 11, 10) | white |
| 21 | (8, 12, 11) | black |

The state coordinates below are in face order A=[0, 4, 7, 9, 10, 11, 14, 16, 19, 21]. Nonroots are [1, 2, 3, 6, 7, 8, 9, 10, 11, 12].

An integral value-20 flow chooses r=(6, 2, 1, 7, 11, 12, 3, 10, 9, 8) and s=(1, 3, 2, 8, 6, 7, 9, 11, 10, 12). Each X vertex and A face has degree two in their union. All other incidence arcs carry zero. Alternating each union cycle gives these two states.

There are 12 states and 8 pairs by exhaustive enumeration. For a nontrivial walk when available, start instead at r=(6, 2, 1, 8, 11, 7, 3, 10, 9, 12), s=(1, 3, 2, 7, 6, 12, 9, 11, 10, 8).

Its D cycles, specified by supplying faces, are [(0, 4, 7, 10, 14, 16, 19), (9, 11, 21)]. Its Q cycles are [(7, 9, 19)].

Nonzero spoke weights `(face,corner,weight)` are [(0, 6, 2), (4, 0, 2), (7, 1, 1), (10, 11, 1), (11, 6, 1), (11, 12, 1), (14, 3, 1), (16, 4, 2), (16, 10, 1)].

The signed polynomial in these weights is {0: 1, 2: -1, 4: -1, 5: 1, 6: -1, 7: 1}, written as exponent-to-coefficient entries.

Phase 1, h=2.
Normalize D cycle (0, 4, 7, 10, 14, 16, 19): r=(1, 3, 2, 8, 6, 7, 9, 11, 10, 12), s=(6, 2, 1, 7, 11, 12, 3, 10, 9, 8).
Initial excess-rank tokens are ((0, 1), (11, 1)); alpha fixes this object.
Beta fixes the object: the second state is good.

The opposite edges Q_s are [(0, 1), (0, 3), (1, 8), (2, 9), (4, 9), (4, 11), (5, 6), (6, 7), (8, 10), (11, 12)].

The white tree is [[1, 6], [3, 13], [5, 8], [5, 13], [6, 18], [8, 17], [12, 15], [12, 18], [17, 20], [18, 20]], rooted at 3.

| Black face | Deleted corner | White edge | Child | Selected side |
|---|---|---|---|---|
| 0 | 6 | (1, 6) | 1 | (0, 6) |
| 4 | 2 | (5, 13) | 5 | (0, 2) |
| 7 | 1 | (5, 8) | 8 | (1, 9) |
| 9 | 7 | (6, 18) | 6 | (1, 7) |
| 10 | 11 | (12, 15) | 15 | (5, 11) |
| 11 | 12 | (12, 18) | 12 | (6, 12) |
| 14 | 3 | (3, 13) | 13 | (3, 9) |
| 16 | 10 | (17, 20) | 20 | (10, 11) |
| 19 | 9 | (8, 17) | 17 | (9, 10) |
| 21 | 8 | (18, 20) | 18 | (8, 12) |

Add e0=(0, 4). The selected sides are [(0, 4), (3, 9), (0, 2), (1, 9), (9, 10), (10, 11), (8, 12), (1, 7), (6, 12), (0, 6), (5, 11)]. The two induced-tree classes are [[0, 2, 4, 6, 8, 12], [1, 3, 5, 7, 9, 10, 11]].

The primal cycle, using dual face IDs, is [0, 5, 7, 13, 4, 3, 14, 17, 16, 15, 2, 1, 10, 12, 21, 20, 19, 8, 9, 18, 11, 6], closed back to its first vertex. The omitted edge is (2, 3). Each consecutive pair shares a side in the face table, and the list contains all 22 face IDs exactly once. The independent primal checker accepts it.
