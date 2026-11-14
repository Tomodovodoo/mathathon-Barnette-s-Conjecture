# Verification and reproduction

Run from the repository root with Python, networkx, sympy, matplotlib, numpy and scipy available:

```powershell
python -X utf8 -B research/2026-11-14_astra_audit-digestions/code/verify.py
python -X utf8 -B research/2026-11-14_astra_audit-digestions/code/extended.py
python -X utf8 -B research/2026-11-14_astra_audit-digestions/code/details.py
python -X utf8 -B research/2026-11-14_astra_audit-digestions/code/recovery.py
python -X utf8 -B digestions/route-map/build_map.py
python -X utf8 -B labyrinth/seed.py
python -X utf8 -B labyrinth/lab.py check
python -X utf8 -B labyrinth/lab.py build
```

COMPUTED outputs:

- verification.json: cube, prism and running-example counts; complete Li fixed-point lists and face-number translation.
- extended.json: 12- and 16-vertex examples and all double-octahedron roots. The script also writes the two PNG figures into digestions/steps/img/.
- detail-checks.json: replayed disks, signs and polynomial coefficients using the lab and supplied face/weight inputs.
- recovery.json: exact selected edges, recovered classes, nonbijective disk and glued certificate.
- links.json: unresolved Markdown links in steps. Empty means no broken links were found.
- final-checks.log: final commands, exit codes and output.
- edits.json and reader-edits.json: replacement-level ledgers for the first two prose passes.
- canonical-changes.patch: exact textual changes to the three authorized canonical directories, relative to the parent of the first audit commit. Generated binaries are listed in CHANGELOG.md with SHA-256 hashes.
- snapshot.json: hashes and sizes of final files; a snapshot is not a claim that every line was independently verified.

The remaining code files are one-time migration scripts preserved as the editing record. Do not rerun them on the corrected documents: they assert the old text and some append route entries. The verification and build commands above are rerunnable.

The scripts read the digestion author's saved faces and weights as inputs, but obtain states, partners and recovery from workings/barnette_lab. They do not run the author's separate state model. The figure script imports the repository figure model and layout read-only. No bytecode is written because commands use -B.

For the source-page inspection:

```powershell
pdftoppm -f 7 -singlefile -scale-to 1600 -png papers/OpenAI-Barnette.pdf research/2026-11-14_astra_audit-digestions/outputs/openai-page7
```

The saved map-review.png is a downsampled visual-QA copy of the full map, made with Pillow. Use the vector PDF or SVG for reading the dense route lists, and the overview PNG for navigation.

Limits are in AUDIT.md. Finite checks here do not prove the unbounded claims they illustrate.
