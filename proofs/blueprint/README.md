# proofs/blueprint

A statement-level blueprint of the project's Barnette proofs, in the style of a Lean blueprint. For every statement of the merged paper (`paper/main/barnette.tex`) it gives what that statement uses, the corresponding statement in the OpenAI paper, the primal note and the involution note, and the Lean declarations at `openai/math@4eaee875` with their relation and status.

| file | content |
| --- | --- |
| `BLUEPRINT.md` | the correspondence tables, the statements with no machine-checked counterpart, the skeleton, unused statements, order problems |
| `FORMALISATION.md` | what it would take to machine-check the merged paper's route by adapting the Lean development |
| `blueprint.json` | nodes (merged paper, primal note, involution note, Lean declarations) and edges (`uses`, `corresponds-to`), with statuses, bridges and gaps |
| `blueprint.dot`, `blueprint.pdf/.svg/.png` | layered uses-graph of the merged paper (transitive reduction), fill = verification status, border = section |
| `columns.dot`, `columns.pdf/.svg/.png` | five-column chart: one row per waypoint, columns OpenAI, merged paper, primal, involutions, Lean |

## Rebuild

From the repository root, with Python 3.14 and Graphviz (`dot`, installed with `winget install Graphviz.Graphviz`):

```sh
# 1. Lean sources at the pinned commit (not committed; .gitignore'd)
git clone --filter=blob:none --no-checkout https://github.com/openai/math.git research/2026-11-14_opus_blueprint/upstream/openai-math
git -C research/2026-11-14_opus_blueprint/upstream/openai-math sparse-checkout set lean/OAI/Combinatorics/Hamiltonian lean/ComparatorChallenges
git -C research/2026-11-14_opus_blueprint/upstream/openai-math checkout 4eaee87548250b2682affda7d05d947c05554bae

# 2. Lean headers of every declaration
python -I research/2026-11-14_opus_blueprint/scripts/lean_sigs.py research/2026-11-14_opus_blueprint/upstream/openai-math/lean/OAI/Combinatorics/Hamiltonian research/2026-11-14_opus_blueprint/data/lean-sigs.json

# 3. Statements, proofs and cited labels of the three notes, read with `git show` at the pinned commit b0fc398
python -I research/2026-11-14_opus_blueprint/scripts/extract_tex.py
#    (add --worktree to read the working tree instead; output gets the suffix -worktree)

# 4. Merge with the curation, analyse, write json/dot, render pdf/svg/png
python -I research/2026-11-14_opus_blueprint/scripts/build_blueprint.py

# 5. Tables spliced into BLUEPRINT.md
python -I research/2026-11-14_opus_blueprint/scripts/tables.py > research/2026-11-14_opus_blueprint/data/tables.md
```

The hand-made part is `research/2026-11-14_opus_blueprint/scripts/curation.py`: the uses each proof makes without a `\ref`, the counterpart in each source, the Lean declarations, and the relation, bridge and gap for each statement. `build_blueprint.py` checks that every label cited in a proof appears among the curated uses and stops listing problems when there are none ("consistency problems: none").

`BLUEPRINT.md` is written by hand around the two tables from step 5. If the curation changes, rerun step 5 and paste the tables back in.

The Lean proof of Lemma 4.7 is `research/2026-11-14_opus_blueprint/lean/FiniteDifference.lean`. Check it in any Lake project whose only dependency is Mathlib `d13f23b7` (Lean v4.34.1): `lake env lean FiniteDifference.lean`. The output is in `FiniteDifference.out`.
