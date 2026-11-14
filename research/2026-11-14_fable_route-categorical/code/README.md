# Code for the categorical route

Python 3.14 with `networkx` and `sympy`. Triangulations come from `workings/barnette_lab/vendor/plantri.exe -ba N` (build it with `python workings/barnette_lab/setup_plantri.py` if it is missing). The lab is imported read-only. Run everything from this directory.

| File | What it does |
| --- | --- |
| `common.py` | `Tri` (faces, face colours, vertex 3-colouring), face-proper labellings by backtracking, Hamiltonian partitions |
| `cuts.py` | disks cut out by a cycle, boundary states, the gluing formula, pattern sets for cuts of length 3 to 6 |
| `gadgets.py` | caps on which a prescribed facial edge or a prescribed 3-edge path forces a 4-cut pattern |
| `trinity.py` | Tutte's arborescences, triangle factors and their projections, two-root states |
| `homology.py` | GF(2) homology of the complex of partial tree matchings, commutation of the two reversals |
| `recursion.py` | insertion into faces, contraction of degree-4 vertices |
| `monodromy.py` | the permutation triple and what can be rebuilt from it |

Exact commands, with the output file each one wrote:

```
python cuts.py glue 10 6            > ../data/glue_v10.txt
python cuts.py three 12             > ../data/three_v12.txt
python cuts.py four 15              > ../data/four_v15.txt      (also writes ../data/four_cuts_v15.json)
python cuts.py full 13 3            >> ../data/full_v13.txt     (then 4, 5, 6)
python gadgets.py 11                > ../data/gadgets_thm22_v11.txt
python gadgets.py 11 p4             > ../data/gadgets_p4_v11.txt
python trinity.py tutte 11          > ../data/tutte_v11.txt
python trinity.py factors 11        > ../data/factors_v11.txt
python trinity.py tworoot 12        > ../data/tworoot_v12.txt
python homology.py hall 9           > ../data/hall_v9.txt
python homology.py bicomplex 12     > ../data/bicomplex_v12.txt
python recursion.py mult 9          > ../data/mult_v9.txt
python recursion.py contract 12     > ../data/contract_v12.txt
python monodromy.py 12              > ../data/monodromy_v12.txt
```

The longest run is `trinity.py tworoot 12`, about three minutes. `four_v15.txt` is the output with the per-triangulation progress lines removed (`grep -v "done$"`). `four_cuts_v13.json` is from an earlier run with `four 13`.

Conventions. Face 0 is black. A cycle is a tuple of vertices, a disk is one of the two face sets it cuts out. Boundary positions are indices into the cycle, and the label of position 0 is 0. State names for 4-cycles (`A0`, `P01`, `X02`, ...) are defined in `PROOF.md`, Section 2. Sign words are read on the edges `(c0c1, c1c2, c2c3, c3c0)`, `+` when the face of the disk on that edge is black.
