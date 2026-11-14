# Lab

Python 3.14, standard library only, except `dets.py` which needs `numpy`. Run every command from this folder's parent (`research/2026-11-14_fable_route-combinatorics/`). Each run is a single process. The longest takes about one minute.

| File | What it does |
| --- | --- |
| `tri.py` | Eulerian triangulations as lists of counterclockwise faces. Generation from the octahedron by the 4-split and the octahedron insertion, canonical codes, face 2-colouring, vertex 3-colouring, separating triangles. |
| `rooted.py` | A rooted triangulation `(T, t0)`: states, `Q_s` and its cycles, partners, `D(r, s)`, `J`, orientation of a cycle by flood fill, the spoke circulation `a(t, v)` of OpenAI Lemma 5.3, heights `h_s(w)`, rank `omega(s)`, Hamiltonian cycles of the dual. |
| `analyze.py` | All statistics of one rooted triangulation, with assertions for every proved identity. Also the maps tree matching to Hamiltonian cycle (OpenAI Section 6) and back. |
| `survey.py` | Runs `analyze` on every rooted triangulation and tests the extremal candidates and counting statements E1 to E8. |
| `zpoly.py` | The signed rank polynomial `Z(q)` and the tests Z1 to Z4. |
| `dets.py` | Numerical checks D1 to D4 of the determinant, Fourier and height identities in `PROOF.md`. |
| `extra.py` | Checks X1 to X3. |
| `extra2.py` | Check X4: partners found from the cycles of `Q_s` agree with a brute-force search over all states. |
| `cex.py` | Prints the counterexamples in full. |
| `tables.py` | Markdown tables from the survey output. |

## Commands that produced the data

```
python lab/survey.py 16 data/rows_v16.json > data/survey_v16.txt     # 40 s
python lab/zpoly.py 15                      > data/zpoly_v15.txt     # 10 s
python lab/dets.py 12                       > data/dets_v12.txt      # 60 s
python lab/extra.py 16                      > data/extra_v16.txt     # 30 s
python lab/extra2.py 16                     > data/extra2_v16.txt    # 60 s
python lab/cex.py                           > data/counterexamples.txt
python lab/tables.py data/rows_v16.json     > data/tables.md
```

`DATA.md` is a hand-written header followed by `data/tables.md`.

## Conventions

- Faces are stored counterclockwise for one orientation of the sphere. With `t0` as the outer face, every other face is counterclockwise in the plane. A directed cycle is counterclockwise when the faces on its left do not include `t0`.
- A state is a tuple indexed like `Rooted.A`, with entry the vertex `s(t)`.
- `delta(v, w) = +1` when the face containing the directed edge `v -> w` has the colour of `t0`.
- Rooted triangulations are named `(V, class, face)`: number of vertices, index of the class in `enumerate_classes(vmax)[V]`, index of `t0` in `Tri.faces`. `cex.py` prints the face lists, so the examples do not depend on this indexing.

## A quick start

```python
from tri import octahedron
from rooted import Rooted
from analyze import analyze
R = Rooted(octahedron(), 0)
stats, extra = analyze(R)
print(stats)            # n=3, 2 states, 2 pairs, 2 tree matchings, cmin=1
```

## Known limits

- The code has not been compared with an independent implementation. The `route-constructive` agent has one, and a cross-check of the counts in `DATA.md` against it would be worth doing.
- Completeness of the generation rests on a comparison of class counts with numbers quoted from memory.
- `dets.py` uses floating point with tolerance `1e-6`.
