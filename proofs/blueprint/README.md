# proofs/blueprint

A statement-level blueprint of the project's Barnette proofs, in the style of a Lean blueprint. For every statement of the paper (`paper/main/barnette.tex`, version 2) it gives what that statement uses, the corresponding statement in the OpenAI paper, the primal note and the involution note, and the Lean declarations with their status. The Lean column has two sources: OpenAI's development at `openai/math@4eaee875` (upstream) and the declarations added in `proofs/lean/Devices`, which a second model rebuilt and audited from a fresh clone (`research/2026-11-14_astra_lean-check`).

| file | content |
| --- | --- |
| `BLUEPRINT.md` | counts, the translations B1 to B5, the two Lean reports compared, the correspondence tables, the statements with no counterpart, the skeleton |
| `FORMALISATION.md` | what remains to machine-check Section 4 of the paper as written, with estimates |
| `blueprint.json` | nodes (paper, primal note, involution note, Lean declarations) and edges (`uses`, `corresponds-to`); each paper node has `status`, `status_v1`, `origin`, and `translation` or `weaker_how` |
| `blueprint.dot`, `blueprint.pdf/.svg/.png` | layered uses-graph of the paper (transitive reduction); fill = status, third line = origin of the Lean counterpart, border = section |
| `columns.dot`, `columns.pdf/.svg/.png` | five-column chart: one row per waypoint, columns OpenAI, paper, primal, involutions, Lean (grey = upstream, blue `+` = added here) |

Status vocabulary: exact; after an unformalised translation; weaker or different form; none. Counts on the route (34 nodes): 5 / 17 / 10 / 2.

## Rebuild

From the repository root, with Python 3.14 and Graphviz (`dot`; `winget install Graphviz.Graphviz`). `S=research/2026-11-14_opus_lean-integration/scripts`.

```sh
# 1. Upstream Lean sources at the pinned commit (not committed)
git clone --filter=blob:none --no-checkout https://github.com/openai/math.git research/2026-11-14_opus_blueprint/upstream/openai-math
git -C research/2026-11-14_opus_blueprint/upstream/openai-math sparse-checkout set lean/OAI/Combinatorics/Hamiltonian lean/ComparatorChallenges
git -C research/2026-11-14_opus_blueprint/upstream/openai-math checkout 4eaee87548250b2682affda7d05d947c05554bae

# 2. Lean headers: upstream and the project's Devices
python -I $S/lean_sigs.py research/2026-11-14_opus_blueprint/upstream/openai-math/lean/OAI/Combinatorics/Hamiltonian research/2026-11-14_opus_lean-integration/data/lean-sigs-upstream.json
python -I $S/lean_sigs.py proofs/lean/Devices research/2026-11-14_opus_lean-integration/data/lean-sigs-devices.json

# 3. Statements of the three notes at the committed HEAD (--worktree reads the working tree and checks numbers against barnette.aux)
python -I $S/extract_tex.py

# 4. Merge with the curation, write json/dot, render pdf/svg/png
python -I $S/build_blueprint.py

# 5. STATUS-TABLE.md and the tables spliced into BLUEPRINT.md
python -I $S/status_table.py
```

The hand-made part is `$S/curation.py`. `MAIN`, `PRIMAL` and `INVOLUTIONS` are version 1's reading (uses, counterparts, bridges). `V2`, `V2_NOTES` and `WAYPOINTS_V2` hold the version 2 statuses, the origins and the project declarations, with the reason for each. `build_blueprint.py` checks that every label cited in a proof is among the curated uses ("consistency problems: none").

Version 1 (paper version 1, three-valued status) is in `research/2026-11-14_opus_blueprint/`.
