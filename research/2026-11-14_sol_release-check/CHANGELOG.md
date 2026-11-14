# Release-check changes

All checks use the fresh clone at `E:/rc-sol-1114`, origin/main commit `eceaf633aaff996f18f00075ce1b7d4af5cf6b5b`. Rebuild output in that clone is disposable and is not copied back as a product change.

## Check infrastructure

- Added `run.py`, a sequential command runner with individual time limits and saved commands, return codes and console logs.
- Added `scan.py`, a read-only tracked-tree inventory for links, paths, hygiene and reader-facing process residue.
- Added baseline PDF text and page-count evidence under `logs/` before any rebuild.

No mathematical content or figure content has been edited.

## Mechanical fixes

- `requirements.txt`: new file pinning only the seven packages exercised by the release commands.
- `paper/main/README.md`: new build instructions, direct pdflatex/bibtex fallback, committed inputs and historical source context.
- `paper/draft-A/README.md` and `paper/draft-B/README.md`: new build instructions and shared-figure history warning.
- `papers/INDEX.md`: replace nonexistent OLD-MACHINERY.md with BRIDGES.md, whose Section 1 contains the cited Feder-Subi comparison. No citation claim changed.

## Shared-path overlap

Commit e095165 was scoped to papers/INDEX.md but also captured 42 pre-existing lines from the concurrent citation audit. The release-check edit itself was one target replacement. The other lines were preserved. No shared-tree reset or history rewrite was attempted.
