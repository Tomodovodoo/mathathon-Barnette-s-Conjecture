# Reproducing the work

Run from `E:\Personal\Math\mathathon\barnette-s-conjecture` using Python 3.14. Dependencies are SymPy and NetworkX. Generation uses the existing plantri 4.5 executable. All scripts set `sys.dont_write_bytecode=True` before importing another folder. They read the Fable enumerator and the reference lab; they do not edit them.

The working folder below is `research/2026-11-14_astra_induction-lemmas`. One computation was run at a time. The longest final census run is about two minutes, below the ten-minute limit.

```powershell
$taskDir='research/2026-11-14_astra_induction-lemmas'
python -B "$taskDir/code/deficiency.py" 6 14 "$taskDir/data/deficiency_6_14.json"
python -B "$taskDir/code/contraction_formula.py" 6 14 "$taskDir/data/contraction_formula_6_14.json"
python -B "$taskDir/code/g_structure.py" 8 19 "$taskDir/data/g_structure_8_19.json"
python -B "$taskDir/code/x_hypotheses.py" 6 18 "$taskDir/data/x_hypotheses_6_18.json"
python -B "$taskDir/code/cube_repairs.py" "$taskDir/data/cube_repairs.json"
python -B "$taskDir/code/check_certificates.py" "$taskDir/data/certificates.json"
python -B "$taskDir/code/g_five_certificates.py" "$taskDir/data/g_five_certificates.json"
python -B "$taskDir/code/repair_witness.py" "$taskDir/data/repair_witness.json"
python -B "$taskDir/code/repair_witness.py" "$taskDir/data/cube_witness.json" --cube
python -B "$taskDir/code/build_summary.py"
```

`check_certificates.py` needs the earlier G pilot file, and `repair_witness.py` needs the earlier X pilot file. They are retained as immutable inputs. To recreate those pilot files:

```powershell
python -B "$taskDir/code/g_structure.py" 8 16 "$taskDir/data/g_structure_8_16.json"
python -B "$taskDir/code/g_structure.py" 17 19 "$taskDir/data/g_structure_17_19.json"
python -B "$taskDir/code/x_hypotheses.py" 6 16 "$taskDir/data/x_hypotheses_6_16.json"
python -B "$taskDir/code/x_hypotheses.py" 17 18 "$taskDir/data/x_hypotheses_17_18.json"
```

The initial X pilots preceded an added diagnostic counter for the merged-vertex D-cycle and a correction to the serialization order of the generic non-TM mate witness. Their totals and exception witnesses are unchanged. Use the final combined file for that generic witness. The independent exception replays reconstruct mates from scratch and never consume the misordered array. Timings and the new diagnostic fields will differ on regeneration.

The initial G pilots preceded the refined five-cycle descent counters. The final combined G file includes both refinements and the coloured-curvature checks. Regenerating the pilots with current code adds those fields without changing their original counters.

## Methods and independence

`common.py` imports `et.py` read-only. Its TM enumerator was independently checked by the preceding referee. We additionally compare entire TM sets, not just counts, against `barnette_lab` on all 438 rooted instances through V=13. Our formula, disk and repair logic is new and remains unreviewed.

`deficiency.py` traverses induced embedded face walks and compares them with direct Hall sums. It tests one representative for all root faces of the same colour contained in U, since neither side of the identity depends on which such root is chosen. It does not test disconnected U under a connected-U formula.

`g_structure.py` tests only graphs with no separating triangle, all roots, both colours, all degree-4 nonroots and both merges. It enumerates chordless four- and five-cycles, cuts the dual face adjacency to identify the two sides, and tests the criterion against a separate max-flow computation. No test uses tree-matching existence as a substitute for pair existence.

`x_hypotheses.py` enumerates all tree matchings directly and tests avoidance, local assignment patterns, mates and single D-cycle reversals. It tests local patterns only for instances with at least one tree matching. Its exceptions reproduce all 7,940 saved by the earlier full census.

`cube_repairs.py` reads every saved exception row through V=18, groups by rooted contraction, then re-enumerates all its tree matchings and their covers. It tests the half bound on the complete contraction and separately on each fixed cover. It also constructs the tree-preserving D-cycle reversal graph. Contractions with zero exceptions need no additional half-bound test.

`repair_witness.py` is a separate replay using the reference lab's state enumeration, pair enumeration, spoke-tree test and cycle routines. It checks the decisive V=17 and V=18 examples without importing the new X classification code. `check_certificates.py` independently verifies G's negative Hall cuts using NetworkX max flow.

## Labels

Graph identifiers are zero-based indices in `plantri -b -a V`, even when a run subsequently filters out graphs with separating triangles. Vertex labels are zero-based. A root triple is a face, with cyclic order immaterial unless explicitly used for orientation. The local setup is always `[x,a,p,b,q]`. In the reference-lab JSON, `cycles` and `qcycles` contain the lab's face indices, while the `contracted_faces` list is in its A order. Full source faces are retained in the witness for reconstruction.
