Release check in progress against a fresh origin/main clone.
Pinned commit: eceaf633aaff996f18f00075ce1b7d4af5cf6b5b.
Quick regression passed, including all 14 unit tests and 70 rooted runs.
Plantri downloaded, hash-checked and compiled; no plantri skips are needed.
Final blocking list and full build evidence will replace this checkpoint.

# Scope

Test newcomer reproducibility, mechanical consistency, links, build hygiene and process residue. This is not a mathematical review.

# Established so far

The clone has no untracked local inputs from the shared workspace. See `logs/baseline.json`, `logs/scan.json` and the command logs.

# Open

Document, figure and full code checks are running sequentially. A protected open-problems link points at an untracked-only certificate.

# Next steps

1. Finish all build and verification commands.
2. Fix mechanical build instructions and record each changed path.
3. Publish the final release decision and remove the disposable clone.
