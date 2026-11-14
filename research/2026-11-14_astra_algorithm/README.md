# Algorithm research artifacts

All writes are in the assigned research folder, `proofs/algorithm/`, and the new `workings/barnette_lab/barnette_lab/optimized/` subpackage. Existing files elsewhere are read-only inputs. Claims and omissions are in REPORT.md and proofs/algorithm/STATUS.md.

Run the following commands from the repository root, in this order. Each campaign is a separate process. Do not run heavy campaigns concurrently.

```powershell
$env:PYTHONPATH='workings/barnette_lab'
python -B -m unittest barnette_lab.optimized.test_optimized -v
python -B workings/barnette_lab/run_tests.py quick
python -B research/2026-11-14_astra_algorithm/examples.py
python -B research/2026-11-14_astra_algorithm/experiments.py census
python -B research/2026-11-14_astra_algorithm/experiments.py families
python -B research/2026-11-14_astra_algorithm/experiments.py hybrid
python -B research/2026-11-14_astra_algorithm/attack.py
python -B research/2026-11-14_astra_algorithm/attack.py filtered
python -B research/2026-11-14_astra_algorithm/hunt.py
python -B research/2026-11-14_astra_algorithm/verify_saved.py
python -B research/2026-11-14_astra_algorithm/experiments.py figures
python -B research/2026-11-14_astra_algorithm/metrics.py
python -B -m barnette_lab.optimized research/2026-11-14_astra_algorithm/cli-cube.json
```

`experiments.py` makes `*-instances.json` and corresponding JSONL rows. Each original family solver is capped at eight seconds including process startup; individual algorithm caps are documented in BENCHMARKS.md. The parent ends after 480 seconds. The completed archived family campaign has 270 rows. Hybrid/DP has 60 rows. Census has 1,048 rows. Counts below these totals on a slower machine mean the run was incomplete. The programs do not hide a cap as success.

`examples.py` generates worked-examples.md and example-certificates.json and inserts the worked section into ALGORITHM.md. It uses the source running.json as input without editing it. `attack.py` writes prefix-counterexample.json and stress.json; the filtered mode writes filtered-prefix-counterexample.json. The stress search uses a 100-second overall limit and at most 500 samples. The recorded run completed 500. `hunt.py` generates 60 random relabelled/rooted inputs, then runs the public solver in serialized eight-second workers with a 480-second overall cap. Its rows retain certificates and full end-to-end times.

`verify_saved.py` uses its own primal adjacency and cycle checker and a Cartesian-product state enumerator. It does not import the lab. It writes independent-checks.json. The only common mechanism in its cycle replay is NetworkX's planar embedding, needed to reconstruct the saved primal face IDs. This is independent checking code, not a different author or a formal verifier.

`experiments.py figures` writes proofs/algorithm/time.png, moves.png and summary.json. `metrics.py` writes BENCHMARKS.md, fits.json and manifest.json. The latter captures file hashes and package versions; hashes describe the archived filesystem bytes, so Git newline conversion can change a reproduced hash. No data file exceeds 1 MB in this run.

`cli-cube.json` is the hand-written cube edge list in the subpackage README. The CLI returned `[0,3,2,1,7,6,5,4]`, avoiding `[0,1]`. The unit tests also check string input labels.

Source-reading evidence was produced by:

```powershell
pdftotext -layout paper/main/barnette.pdf research/2026-11-14_astra_algorithm/exposition.txt
python -B -c "import fitz; d=fitz.open('papers/barnette_trees.pdf'); [d[i].get_pixmap(matrix=fitz.Matrix(1,1)).save('research/2026-11-14_astra_algorithm/source-page-'+str(i+1)+'.png') for i in [8,9,10]]"
```

These are source audit images, not generated scientific figures. The entire manuscript was read through its supplied extraction. No source PDF was edited.

The later marked-chain investigation is reproduced by:

```powershell
python -B research/2026-11-14_astra_algorithm/marked_chains.py
python -B research/2026-11-14_astra_algorithm/marked_chains.py 7 long
python -B research/2026-11-14_astra_algorithm/verify_saved.py
python -B research/2026-11-14_astra_algorithm/metrics.py
```

The first command uses ten serial twenty-second workers. The second raises the move cap to 100,000 for the eight-factor input and writes marked-chain-eight.json directly as UTF-8. It took about 80 seconds here. The original command redirected stdout in PowerShell and the file was then normalized from UTF-16 to UTF-8; the current script removes that unnecessary encoding step. Metrics generates the third figure marked-chains.png and its separate table. The all-length recurrence in marked-chain-analysis.md is a conjecture.
