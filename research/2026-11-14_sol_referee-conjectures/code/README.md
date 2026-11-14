# Independent verification commands

Run from `E:\Personal\Math\mathathon\barnette-s-conjecture` in PowerShell. Python 3.14, networkx, sympy and g++ were available. The hash manifest records exact versions and input hashes. The compiled binary and Python cache are ignored. All code in this directory was written for this audit; it imports no author or earlier referee implementation.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$referee='research/2026-11-14_sol_referee-conjectures'
python "$referee/code/independent.py"
python "$referee/code/census.py" 14
python "$referee/code/census.py" 18
python "$referee/code/examples.py"
python "$referee/code/anatomy.py"
python "$referee/code/witnesses.py" greedy
python "$referee/code/witnesses.py" stored r1
python "$referee/code/witnesses.py" stored r3
python "$referee/code/witnesses.py" r5
python "$referee/code/gluing.py"
python "$referee/code/second_certificate.py"
python "$referee/code/families.py"
python "$referee/code/cancellations.py" 16
g++ -O3 -std=c++17 "$referee/code/count.cpp" -o "$referee/code/count.exe"
python "$referee/code/fast_census.py" 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
python "$referee/code/validate.py"
```

Run these sequentially. A complete Python V<=18 census took about 161 seconds, including 124 seconds at order 18. The C++ V<=22 run took about 80 seconds, with the V=22 counter taking about 58 seconds. The V=70 check took 50 seconds. Other jobs took seconds. The C++ wrapper imposes a 540-second timeout per order. The input producer plantri is a generator feeding one counter, not a second search campaign. No background compute is required.

## Programs

`independent.py` reconstructs facial walks and colours from rotations, builds H0, enumerates states and deleted-corner assignments using capacity constraints, integrates face potentials and independently computes their shortest-path bounds. It enumerates all directions of every D-cycle. Its two tests of the forest criterion use different algorithms, union-find on Q_s and topological sorting on F. Its main program BRUTE-FORCES EVERY ORDERED STATE PAIR of the V=18 witness and compares the resulting pair set with all factor decompositions. It also tries every vertex-deletion set of size at most three.

`second_certificate.py` imports no other audit implementation. It re-enumerates all states and all ordered state pairs of the new V=33 witness, checks Q_s by DFS with root counts, checks the graph rotation and black-face incidence, reintegrates potentials and builds all Hasse covers by pairwise comparison. The only input is the explicit graph-and-face certificate, not a verdict. It checks the stored result rather than trusting its list of orientations.

`count.cpp` separately implements capacity enumeration and direct Q-forest counting in C++. It does not implement potential order and does not import or include Python code. The Python all-state brute force and C++ all-factor census agree on every aggregate row through V=18. `validate.py` enforces that agreement and checks the named totals.

`cancellations.py` checks the first involution and builds the complete non-increasing move graph for C3. Reverse reachability from k=0 tests every pair, not just random starts.

`gluing.py` constructs the V=33 R2 refutation. `families.py` implements the tube adjacency rule directly and glues explicit face lists. Networkx is used only for an embedding of generated tube graphs. The chosen root is the lateral face specified in the counting-family report.

`witnesses.py r5` uses `opus_conjectures/code/gen.py` ONLY to reconstruct an input from the documented seed. It keeps graph 24 at V=70 and chooses face 80, then passes the rotation to this directory's independent enumerator. This is generation, not reuse of the author's verifier. All other saved author instances are read strictly as graph data. No `bar.exe`, author `verify_*.py`, reference-lab verifier or earlier referee engine was run.

## Output map

| Data file | Producing command above |
|---|---|
| `v18.json` | `independent.py` |
| `census_14.json`, `census_18.json` | `census.py 14`, `census.py 18` |
| `examples.json` | `examples.py` |
| `v18_directed_cycles.json`, `moments.json` | `anatomy.py` |
| `greedy.json` | `witnesses.py greedy` |
| `r1.json`, `r3.json` | `witnesses.py stored r1`, `stored r3` |
| `r5_input.json`, `r5.json` | `witnesses.py r5` |
| `R2_glued_V33.json` | `gluing.py` |
| `second_R2_glued_V33.json` | `second_certificate.py` |
| `families.json` | `families.py` |
| `cancellations_16.json` | `cancellations.py 16` |
| `fast_census_6.json` through `fast_census_22.json`, including empty order 7; `fast_census_summary.json` | `fast_census.py 6 ... 22` |
| `provenance.json` | `validate.py` |

`COMPUTED`. `examples.py` independently reconstructs the clockwise reference in every fibre, checks its sparse product formula against the direct signed enumeration, and saves the normalized factorization and the first nonzero coefficient. The normalization multiplies the signed Laurent polynomial by z to the negative of its minimum exponent. The first nonzero coefficient at z=1+x is sum_e coefficient(e)*binomial(e,c_min), valid also for negative e.

## Enumeration scope and limitations

Plantri is the existing executable `workings/barnette_lab/vendor/plantri.exe`, invoked as `-ab V`. Its standard class enumeration is an input, not independently reimplemented. Every face is tried as root, without quotienting by root automorphisms. The Python census tries all ordered state pairs and checks all factor decompositions through V=18. The C++ census does not enumerate all states separately, but enumerates every factor and direction through V=22. The two independent methods agree on the whole overlapping range.

The original V=19..24 extreme/irreducible census and 940-start random C3 run were not fully repeated. The independent checks specified in REFEREE.md are the range claims of this audit. No test establishes a conjecture beyond its checked range.

Process note. A first C++ wrapper run produced harmless Python reader-thread errors after closing the plantri stdout pipe and then asking `communicate` to read it again. The C++ runs completed normally. The wrapper was fixed and the full final run completed cleanly. I accidentally started a repeat before noticing that the first V=22 count was still active; I cancelled the repeat, checked that it left no process, then ran the final serial campaign. There was a brief overlap of two counters. This departed from the one-heavy-process instruction and is recorded rather than concealed. All retained final census outputs come from the later serial run.
