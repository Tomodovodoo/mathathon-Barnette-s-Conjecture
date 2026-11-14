# Independent verification code

All programs in this folder were written by the referee. None imports or executes code from either audited report, from fable, or from `workings/barnette_lab/`. The saved graphs, rotations and assignments are inputs only. Author code was read to understand field meanings and the scope of claims. It was not used to produce verification outputs.

Run from `E:\Personal\Math\mathathon\barnette-s-conjecture`. Python 3.14, NetworkX 3.6.1, SciPy 1.17.1 and SymPy are installed. The exact versions and SHA-256 hashes are recorded by `provenance.py`. Only the maximum-cut experiment uses a floating MILP solver. LP feasibility and extremality use rational arithmetic, not the author's numerical separation code.

Each command is independent except that the certificate checker reads prior JSON outputs. Run one computation at a time. The longest observed job was the census, approximately six minutes; no single job needs a run longer than ten minutes on this machine. Console `.log` files are scratch and excluded from Git; the JSON files are the recorded outputs.

| Command after `python research/2026-11-14_sol_referee-structure/code/` | Output | What it establishes |
| --- | --- | --- |
| `audit.py census` | `census.json` | All states, pairs, flow and obstruction equivalence, all induced-tree partitions and inverse images, monotone D3 through V=14 |
| `structure.py matroids` | `matroids.json` | Full-ground-set relaxations at V=6,8; explicit failure of the unrestricted matroid-isomorphism claim |
| `structure.py lp` | `lp-certificate.json` | Complete rational half-integral vertex at V=13, all 2,047 subset inequalities, active rank 25 |
| `structure.py contractions` | `contractions.json` | Restricted state lifts, conditional side test, explicit false-converse certificate through V=13 |
| `counterexamples.py lattice` | `matching-extremes.json` | Exact all-cycle matching extrema at V=10,12, including ten joint failures at 12 |
| `counterexamples.py large` | `large-counterexamples.json` | Saved V=40,50,80 factor, extremality and descent certificates |
| `counterexamples.py fable` | `fable16.json` | Independent replay of the V=16 no-tree factor and exact D3 on its full pair graph |
| `euler_alpha.py euler` | `euler.json` | Exact Euler identity on all 28,718 connected induced subgraphs of all saved V≤12 graphs |
| `euler_alpha.py alpha_small` | `alpha-small.json` | Independently enumerate alpha-orientations, compare with pair quotients, test true extremes and O6 through V=14 |
| `euler_alpha.py alpha_large` | `alpha-large.json` | Compute actual all-cycle lattice extremes on eight saved V=40..120 inputs and test O6 |
| `limits.py examples` | `limits-examples.json` | Rarity q=1..6, prism inverse failure, P5 cube, defective disk, torus, noncubic and theta examples, root dependence |
| `limits.py maxcuts` | `maxcuts.json` | Fresh binary MILP for K4, BBL38 and Tutte46, optimum cut sizes and defective edges |
| `limits.py strengthenings` | `strengthenings.json` | All 55 graph rows, complete Hamiltonian-cycle counts, all edge pairs and P4 paths, exact endpoint DFS |
| `limits.py reduction` | `NP-reduction-small.json` | All edge-deletion reduction equivalences on cube, prism and the non-Hamiltonian theta graph |
| `extras.py gluing` | `gluing.json` | All 3,618 prescribed-edge partitions through V=14, splitting only at black-inner obstructions |
| `extras.py weights` | `weights-leading-zero.json` | Integer-weight example with c_min=1, zero linear coefficient and nonzero Z; direct all-pair and tree-state polynomial agreement |
| `verify_certificates.py` | `certificate-checks.json` | Separate direct checks of LP and lift certificates and the five-row rarity enumeration |
| `provenance.py` | `provenance.json` | Input, program and output hashes, interpreter/library versions |

For example:

```powershell
python research/2026-11-14_sol_referee-structure/code/structure.py lp
python research/2026-11-14_sol_referee-structure/code/verify_certificates.py
```

## Scope and independence

The small corpus is the 55 saved triangulations through V=14, with graph counts 1,0,1,1,2,2,8,8,32 at V=6,...,14. I independently checked their rooted properties. I did not independently generate every isomorphism class. Thus the unconditional finite assertion is about every saved input. Completeness of that census is a separate generator claim, supported by the structural generation argument and the other report's plantri provenance, not certified anew here.

`census.json` records 1,206 facial rootings, 12,924 states, 3,280 ordered pairs, 3,240 tree states, 9,720 direct images and 35,664 prescribed partitions. Exactly 880 roots admit pairs. The D3 test is reverse reachability in the directed graph that retains only exchanges which do not increase k. It checks every ordered pair, rather than a chosen start or mate.

`gluing.json` uses fresh exhaustive partition search as its base solver. It verifies boundary agreement and tree unions independently of the source matching constructor. Its 4,640 distinct recursive calls include 1,151 actual joins. It does not reprove the central weighted existence proposition.

`alpha-large.json` does not use facial flips. Exact rational barycentric coordinates and signed-area edge weights allow detection of a directed cycle in either sense. Arbitrary directed cycles are reversed to compute the genuine extrema. This distinction is necessary: several author's facial terminals have directed cycles in both senses.

`lp-certificate.json` uses graphic base inequalities in H*, equivalent to cographic base inequalities in H. All 2,047 nonempty white subsets are checked, including the full set. Full-rank tight constraints certify a vertex. The author's saved dump omitted its coordinates equal to one; both possible integral completions of that partial support are recorded. One completion is the certified fractional vertex. The other has two tree states in its support and is not claimed to be a vertex.

State coordinates are always interpreted using an explicit bounded-black-face list where a certificate stores a tuple. This avoids depending on dictionary order or an unstated planar-face numbering.

## Recorded corrections

The independent code establishes a false reverse implication in the degree-four lift theorem, a false unrestricted matroid isomorphism, false labels on several alleged lattice extrema, a missing integral completion in the LP dump, the incorrect two-non-tree-state description of that support, and a stale deficient-set label list for the theta example. The coefficient example refutes a necessity claim about arbitrary weights. Read the referee reports for exact corrected statements.
