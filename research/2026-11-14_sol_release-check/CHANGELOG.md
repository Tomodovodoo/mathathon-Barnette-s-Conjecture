# Release-check changes

All checks use the fresh clone at `E:/rc-sol-1114`, origin/main commit `eceaf633aaff996f18f00075ce1b7d4af5cf6b5b`. Rebuild output in that clone is disposable and is not copied back as a product change.

## Check infrastructure

- Added `run.py`, a sequential command runner with individual time limits and saved commands, return codes and console logs.
- Added `scan.py`, a read-only tracked-tree inventory for links, paths, hygiene and reader-facing process residue.
- Added baseline PDF text and page-count evidence under `logs/` before any rebuild.

No mathematical content or figure content has been edited.
