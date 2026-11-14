Checked two fresh origin/main clones, pinned at eceaf633 and b594509.
All current document products build, including the repaired atlas and 11-page sign-free note.
Quick and full regressions pass, including all 14 unit tests and 1,209 full rooted runs; no plantri skips.
Two checks remain red: synthesis word count and the optional figure review's caption-length gate.
Mechanical fixes and evidence are committed; automatic approval review blocked deletion of both temporary clones.

# Task

Check newcomer reproducibility and mechanical consistency after the campaign. This is a release test, not a mathematical audit. Full commands, results, changes and limitations are in RELEASE-CHECK.md; hygiene and exact process-residue locations are in HYGIENE.md, RESIDUE.md and RESIDUE-LATE.md.

# Established

COMPUTED over the two pinned tracked trees. Main paper 20 pages, primal 15, involutions 18, atlas 34, gallery 10 and sign-free 11 reproduce their committed extracted text and page counts from their current source editions. Historical drafts build at 11 and 16 pages but their shared figures have drifted. The later atlas fully regenerates all 30 figures and passes verify.py. Sign-free figure generation, all 61 assertions, its 262-root verification and Markdown extraction pass.

Shared figure build, geometry and independent lab checks, primal figure/cancellation checks, both involution verification runs, route-map regeneration, Labyrinth check/build and all blueprint extraction stages pass. Both lab tiers pass on both pins. Plantri was downloaded, hash-checked and compiled in each clean clone. All product fonts are embedded. No current note has an undefined reference/citation, missing input or missing character. One atlas standalone figure has a 3.46451pt overfull hbox.

The later pin has no broken requested Markdown links and no research folder missing from INDEX. Three concurrent runs lack REPORT.md at that pin; paths are listed in RELEASE-CHECK.md. No tracked upstream/vendor clone or bytecode was found. Large files, SHA256 duplicates, local paths, personal-data locations and remaining historical-source targets are inventoried. Personal values are omitted from the inventories.

# What failed and why

- Blocking for an all-green check: synthesis audit exits 1 at 5,910 words against its 5,000-word ceiling. The synthesis is protected, so neither text nor assertion was changed.
- Blocking for an all-green check: optional figure proofs.py exits 1 because Figure 17 has eight caption lines against its five-line bound. Its fixed contact-sheet canvas also fits only nine gallery pages. Figure content and assertions were left intact.
- Resolved at the later pin by other owners: the atlas's obsolete blueprint status/count mapping and the missing descent-certificate link.
- Resolved mechanically in READMEs: missing main/draft build instructions, latexmk's missing-Perl/update failure, and stale primal/involution editorial generators that overwrite final source/caption edits. The committed TeX editions build correctly. No mathematical content was altered.

# Changes and Git

Added requirements.txt with the seven exercised Python packages; added main/draft build READMEs and top-level build links; corrected primal/involution build instructions; repaired one nonexistent citation path in papers/INDEX.md. CHANGELOG.md records each path and the concurrent commit overlaps. All commits were path-scoped. The INDEX reference-fix commit also captured 42 lines already added by the citation agent; those lines were preserved. A concurrent proofreader committed the primal README correction in ba8d7d4.

# Open and non-blocking

Historical-draft drift, stale editorial generators, an embedded Type 3 atlas font, the single standalone overfull box, duplicate/large records, hardcoded external paths in historical audit scripts and process residue remain documented. The later source inventory has 64 residue matches; the original primal opening and its proposed replacement are preserved in the initial inventory. Later shared commit 290e972 untracked the three involution TeX artefacts; two sign-free TeX build files were still tracked at the tested later pin.

The repository continued changing during the check. Results apply to the two explicit pins, not to untested edits after b594509.

# Three best next steps

1. Have the synthesis and figure owners reconcile the two red editorial gates, including the review contact-sheet height. Preserve the gates until the intended layout/length decision is made.
2. Finish concurrent reports and remove remaining disposable sign-free TeX artefacts. Keep computation transcripts and source provenance intact; use HYGIENE.md for the earlier cleanup proposal's remaining items.
3. Freeze a release commit after the remaining agents finish, then repeat the direct document builds, atlas verify and quick regression at that exact commit. Use the recorded commands and requirements file.

# Cleanup

Automatic approval review rejected recursive deletion of the verified temporary clone paths as "blocked by policy", including a literal-path retry. Both clones remain at E:/rc-sol-1114 and E:/rc-sol-late. See logs/clone-cleanup.txt. No bypass was attempted.
