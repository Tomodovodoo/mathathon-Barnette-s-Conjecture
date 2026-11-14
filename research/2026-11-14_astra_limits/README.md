# Reproduction and files

Run commands from `E:\Personal\Math\mathathon\barnette-s-conjecture`. All scripts write only inside this folder and import the reference library without editing it. Python needs networkx, sympy, scipy and numpy. The reference plantri executable must already exist at `workings/barnette_lab/vendor/plantri.exe`. This run used the existing executable; it did not run setup or change the reference library.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python research/2026-11-14_astra_limits/code/campaign.py 14
python research/2026-11-14_astra_limits/code/special.py
python research/2026-11-14_astra_limits/code/rarity.py
python research/2026-11-14_astra_limits/code/more.py
python research/2026-11-14_astra_limits/code/certificates.py
python research/2026-11-14_astra_limits/code/multimap.py
```

`more.py` reads the saved public House of Graphs response `data/hog954.json`. Fetch it again with Python urllib from `https://houseofgraphs.org/api/graphs/954` if needed. The graph payload is retained to avoid a network dependency during replay.

`campaign.py` writes `data/roots.json`, `data/strengthenings.json`, and `examples/tN_I.json`. All face IDs index the face list; edge endpoints are integers. A primal edge list and a dual edge list are distinguished by key. The reference library recomputes the same rotation system from insertion-ordered edges. `special.py` writes named obstruction examples, non3connected counts and a nonbijective disk witness. `rarity.py` writes white-face prism sums through six pieces and their state counts. `more.py` writes maximum-cut solver results, the P5 witness, zero weights and torus states. `certificates.py` writes the noncubic witness, exact prism recovery images and disk counts, and validates the small primal graph hypotheses.

`data/rarity_black_obstructed.json` records the failed initial prediction. To reproduce that historical run, copy `code/rarity.py` to a temporary script in this folder and replace `b.white[-1]` by `b.A[-1]`; choose different output names before running so it does not overwrite the corrected white-face examples. The recorded wrong-color result is a dead end with its lesson, not part of the rarity proof.

Predictions were written before each experiment in PREDICTIONS.md and PREDICTIONS_2.md. The append-only events log contains both the preliminary range through 12 and the final range through 14; repeated entries are replay history, not additional graphs. Every heavy run finished well under ten minutes. The scripts run sequentially, one computation at a time.

The three `data/*-formula.png` files were rendered from PDF pages 5 of OpenAI-Barnette, 9 of barnette_trees, and 8 of A-Note-On-Barnette using PyMuPDF at scale 1.3. They were visually inspected to check the disk identity, leading coefficient and Li's third-edge counts. The text dumps supplied with all three PDFs were read for their surrounding arguments. Other source PDFs were not altered.

Status discipline: all computational results remain T4 under review. Comparing output cycles with independently enumerated primal cycles catches recovery errors but does not certify plantri completeness or independently validate every state and separator count. Exact small minimality claims refer only to the declared class and range, unless a separate argument is given.

The local research map is `labyrinth/dashboard/index.html`. Rebuild with:

```powershell
python research/2026-11-14_astra_limits/code/map.py
python -X utf8 research/2026-11-14_astra_limits/labyrinth/lab.py check
python -X utf8 research/2026-11-14_astra_limits/labyrinth/lab.py build
```
