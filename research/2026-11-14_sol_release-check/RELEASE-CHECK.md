# Release check, 14 November 2026

This checks reproducibility and mechanical consistency, not the validity of the mathematics. All computational findings below are COMPUTED over the stated files and test ranges.

## Snapshots and environment

Two fresh clones were made directly from origin/main, outside the shared working tree:

```powershell
git clone --single-branch --branch main https://github.com/Tomodovodoo/mathathon-Barnette-s-Conjecture.git E:/rc-sol-1114
git clone --single-branch --branch main https://github.com/Tomodovodoo/mathathon-Barnette-s-Conjecture.git E:/rc-sol-late
```

- First snapshot: `eceaf633aaff996f18f00075ce1b7d4af5cf6b5b`.
- Later snapshot: `b5945098ec916379e4518db303fd792b6659de19`, including the sign-free note, proofread notes, repaired atlas and descent certificates.
- Windows, Python 3.14.5, MiKTeX pdfTeX/BibTeX and Poppler utilities. GCC 15.2 compiles plantri. Graphviz is installed at its standard Program Files location, although `dot` is absent from PATH; the blueprint builder's fallback finds it.
- Exercised Python packages: networkx 3.6.1, numpy 2.4.3, scipy 1.17.1, sympy 1.14.0, PyMuPDF 1.27.2.3, Pillow 12.2.0, matplotlib 3.11.2. Added only the permitted new top-level `requirements.txt`.
- One heavy command at a time. Each command has a nine-minute limit. The longest completed initial command was the shared figure build, 311.18 seconds. No test used untracked inputs from the shared working tree.

The exact commands, working directories, return codes and timings are appended below and recorded in `logs/*-commands.json` and `logs/late/*-commands.json`. `python` in the appendix denotes the Python executable whose full version is recorded in each baseline JSON. Console logs preserve diagnostic output.

## 1. Documents

The committed TeX edition and the historical generators must be distinguished. The first README-driven primal regeneration and involution figure regeneration succeeded as processes but did not reproduce the committed edition. Their differences are retained in `logs/pdf-comparison.json` and `*-text.diff`. I then restored only the exact committed source inputs inside the disposable clone, compiled directly and compared again. The restored input list is `logs/pristine-restored-inputs.json`. No shared manuscript or figure content was changed.

| Product | Committed pages | Direct source build | Text comparison |
| --- | ---: | --- | --- |
| paper/main/barnette.pdf | 20 | pass | exact extracted text |
| proofs/primal/primal.pdf | 15 | pass | exact extracted text |
| proofs/involutions/involutions.pdf | 18 | pass | exact extracted text |
| digestions/atlas/atlas.pdf | 34 | pass using committed figure PDFs | exact extracted text |
| paper/figures/gallery.pdf | 10 | full regeneration passes | exact extracted text |
| paper/draft-A/barnette.pdf | 11 | pass | shared-figure text differs |
| paper/draft-B/barnette.pdf | 16 | pass | shared-figure text and float order differ |
| proofs/sign-free/sign-free.pdf | 11 | later snapshot: direct and regenerated builds pass | exact extracted text |

The five current note/atlas PDFs were also compiled directly in the later clone. See `logs/late/late-docs-commands.json` and `logs/late/pdf-comparison.json`. Gallery and drafts in that latter JSON were not rebuilt in that phase, so their equality entries merely describe the untouched committed files; their actual build evidence is in the first clone's logs.

The committed-edition main, primal, involution and atlas builds have no errors, undefined references/citations, missing characters or overfull boxes above 2pt. The later direct builds also have no such warnings. All listed PDF fonts are embedded. The atlas contains one embedded Type 3 font, present on PDF pages 1 and 30; this is not a missing font. The rebuilt atlas figure `24-earlier` has a separate 3.46451pt overfull hbox in its standalone log, line 626. This is reported rather than changed because it concerns protected figure content.

`latexmk` failed immediately because MiKTeX could not find Perl. It also emitted the update-check warning mentioned in the brief. Direct pdflatex/bibtex builds work. Added main/draft READMEs and direct-tool fallbacks, and corrected primal/involution README build instructions.

The stale primal Markdown generator restores a model author line, loses URL formatting on a path and moves the worked-example paragraph, producing 16 pages. The involution historical figure generator replaces final captions and the marked picture, removing `fig:paths` and yielding an undefined Figure ?? even after three TeX passes. The subsequent `figure2.py` does not repair `panels.tex`. Those generators remain historical records. READMEs now use the committed TeX sources. I did not alter their mathematical or figure output.

Both historical drafts still build, but current shared figure panels differ from the panels in their committed PDFs. The differences are confined to historical reproduction and float/text layout; no bit-for-bit reconstruction of their original editions is claimed. Their new READMEs state the shared-figure dependence.

## 2. Figure toolkits

- Shared figures: `build.py` passes, including `check.py`, `draw.py`, all 18 standalone PDFs, gallery and `audit.py`. `geometry_check.py`, `crosscheck_lab.py` and the additional `check_hunch.py` pass.
- The optional `research/2026-11-14_sol_figures-polish/proofs.py` writes review material but exits 1 at line 67. It counts eight lines in caption 17, above its five-line bound. Its fixed 3-by-3 contact-sheet canvas also predates the 10-page gallery. I did not shorten captions or weaken the assertion.
- Primal figures: `check.py --build` passes; cancellation checks at 15 and 16 and `inspect_figures.py` pass.
- Involutions: census `check.py 14`, independent `referee_rerun.py`, `drawings.py` and the newer second-figure script pass. The earlier figure generator is stale as described above.
- Atlas at the first pin: both build and verify fail at `figs_proofs.py:257`, `KeyError: 'weaker'`; the same block also hardcodes old blueprint counts. The later clone contains the owner's repair. Its full rebuild/verify result is recorded in the completion addendum below.
- Sign-free at the later pin: figure generation and all 61 figure assertions pass; regeneration changes no tracked figure source or Markdown content. Verification through order 12 passes on the README's 262 rooted instances.

## 3. Code and extraction

Plantri was obtained exactly through `workings/barnette_lab/setup_plantri.py`, downloaded from the README's mirror, hash-checked and compiled in each clone. No plantri-dependent test was skipped. Vendor sources/binaries stayed untracked. The first quick tier passes all 14 unit tests and 70 rooted runs; full passes all 14 tests and 1,209 rooted runs. The same tiers were repeated at the later pin; their final states are in the completion addendum.

Route generation, frontier generation, seed, `lab.py check` and `lab.py build` pass. The initial route JSON, DOT, PNG and text outputs are unchanged. PDF and SVG bytes differ only because of rendering metadata and generated element IDs: all three PDFs have equal extracted text and equal rendered pixels, and all SVGs match after date/ID normalization. See `logs/route-reproducibility.json`; the actual diff is preserved in `logs/route-map-patch.txt`. Protected route-map and Labyrinth files were not edited.

Synthesis `count.py`, `evidence.py` and `snapshot.py` pass. `audit.py` fails its 3,500-to-5,000-word assertion: the first pin has 5,611 words. This is an editorial gate failure, not a failed mathematical census. I did not edit the protected synthesis or relax its audit.

All blueprint README extraction stages pass: sparse upstream checkout at `4eaee87548250b2682affda7d05d947c05554bae`, upstream and project Lean header extraction, TeX statement extraction, JSON/DOT/PDF/SVG/PNG generation and status-table generation. This checks the extraction pipeline, not a new Lean build. The upstream clone exists only inside the disposable clone and is ignored.

## 4. Links and source targets

`scan.py` checks tracked Markdown links in the requested scopes and every braced input/includegraphics/bibliography target in tracked TeX; it accounts for the shared input paths, included involution fragments and macro placeholders. `paths.py` also checks 440 root-qualified path mentions, every path cited in papers/INDEX.md, code-span candidates, filename patterns and the two Markdown anchor links. Machine-readable evidence is `scan.json`, `rooted-paths.json`, `path-triage.json`, `papers-paths.json` and `anchors.json`.

At the first pin:

- One real broken Markdown link: `digestions/steps/09-what-is-still-open.md:39`, pointing to the then-untracked `research/2026-11-14_astra_referee-descent/code/recovered40_0_40.json`. Protected, not edited. The later pin includes the certificate.
- One nonexistent bare citation path: `papers/INDEX.md:22`, OLD-MACHINERY.md. Fixed to `research/2026-11-14_astra_older-approaches/BRIDGES.md`, whose Section 1 contains the cited comparison.
- Atlas `proposed/` is explicitly described as removed history, not a live target. The primal STATUS upstream path is an explicitly untracked external checkout.
- The remaining unresolved TeX candidates are historical manuscript/atlas snapshots: bibliography lookup depends on building from the parent main directory, or snapshot figure names have since been renumbered. Full file/line/target lists are in `logs/scan.json`. They are not missing current product inputs. None was silently repaired by borrowing a shared untracked file.

The path scan is syntactic. It does not interpret arbitrary TeX macros or every natural-language filename as a shell command. All current product builds separately exercised actual input resolution. Contextual abbreviated filenames and proposed/generated Lean filenames are retained as candidates rather than falsely called missing files.

## 5. Hygiene

Full inventories and the earlier survey's item-by-item follow-up are in `HYGIENE.md`; exact duplicate groups and all file/line locations are in `logs/scan.json`.

The first pin has 3,161 tracked files, 327,612,966 bytes, eight files above 5,000,000 bytes and 97 SHA256 duplicate groups. No tracked upstream/vendor clone or Python bytecode was found. Of 67 build-pattern files, the three `proofs/involutions/involutions.aux/.log/.out` are disposable TeX artefacts; the other 64 are computation/audit/formal-build records. Two .bbl files are retained as possible distribution inputs. No computation records were removed.

All 76 tracked research folders at the initial pin have REPORT.md; seven are absent from INDEX after respecting its date-prefix abbreviation. Later differences are in the completion addendum. Local path occurrences are listed individually by file/line; executable historical scripts with fixed external checkout paths are identified by that inventory. They require project-specific inputs rather than a trivial relative-path substitution.

Personal data are reported by location only. The UTF-8 text scan checks email addresses, the local account username and user-directory paths. A separate pass inspected all 174 initial tracked PDFs for those patterns in extracted text and metadata, finding 77 candidate locations and no unreadable PDFs. See `logs/pdf-personal-locations.json`. No OCR of raster images or arbitrary person-name recognition is claimed.

Earlier cleanup: gzip of record-22/24, removal of canonical-changes.patch, blueprint upstream ignore and README layout rows are completed. Large algebra/packing records, raster proof sheets, historical renders, literature copies, duplicates, committed TeX artefacts and some missing index rows remain. Exact IDs A1 through C12 are reconciled in HYGIENE.md.

## 6. Reader-facing internal residue

`RESIDUE.md` gives all 89 initial matches with exact file/line/source text, including tags, model/folder references and process talk. It includes the exact primal first-page status line at primal.tex:16 and a proposed replacement. No reader-facing prose was edited by this release check. Later proofreader changes are inventoried separately in the completion addendum.

The proposed replacement for the opening status sentence is: "We reconstruct the proof in the cubic graph. The theorem is OpenAI, Theorem 1.1 and Corollary 7.1." Keep the subsequent explanation of the Lean commit and two departures, and move review status to STATUS.md. This remains a proposal, not an applied edit.

## Fixes and remaining ownership

Only build READMEs, the new requirements file, one broken reference, and this research folder were changed. See CHANGELOG.md and path-scoped commits. One papers/INDEX.md commit captured 42 lines already added by a concurrent citation agent alongside my one-path replacement; that overlap is recorded, and their work was preserved. A concurrent proofreader also committed the primal README while I was correcting its build instructions.

The final result, clone cleanup and remaining blocking/non-blocking list follow in the completion addendum. Changes after the later pin are outside this check.

## Completion addendum

The later pin passes quick and full, including all 14 unit tests, 70 quick rooted runs and 1,209 full rooted runs. Full took 223.71 seconds including the unit-test entry point. All route/Labyrinth commands pass again, and the three map PDFs again match in text and rendered pixels. All normalized SVGs match.

The repaired atlas fully rebuilds from all 30 recompiled figure sources in 61.11 seconds. `verify.py` passes all 30 routes and 34 pages in 11.52 seconds. Its final PDF text and page count exactly match the later committed PDF. The remaining 3.46451pt standalone figure-24 overfull box is the only current TeX warning found by the final scan. All current note builds have no missing input, unresolved citation/reference or missing character.

The sign-free figure and note pipeline passes, including its 61 assertions, 262-root verification and Markdown extraction. Its generated figure TeX/JSON and Markdown are unchanged relative to the committed later pin. The regenerated PDF is 11 pages with exact extracted-text equality. Every font in the later product font logs is embedded.

At the later pin there are zero broken Markdown links and zero research folders missing from INDEX. Three tracked runs lack REPORT.md at that pin: `2026-11-14_astra_final-proofread`, `2026-11-14_opus_notes-proofread`, `2026-11-14_sol_referee-sign-free`. These were concurrent runs, not deleted reports. The later residue inventory has 64 matches, listed exactly in `RESIDUE-LATE.md`; the original primal status/model opening was removed by the proofreader, not by this release check. PDF pattern scanning covers all 175 later PDFs, with 77 candidate locations, no unreadable PDFs and no personal values exposed in the inventory.

The later rooted-path misses are documented generated upstream checkouts and the explicitly removed atlas proposal directory, not missing committed product inputs. The later hygiene inventory has 105 duplicate groups, the same eight large files and no tracked vendor/upstream clone. Its counts include earlier release-check evidence. The sign-free note adds two disposable tracked TeX files, `sign-free.log` and `sign-free.out`; the added verification .log is a computation record. After both tested pins, shared commit `290e972` untracked the three involution TeX artefacts. That cleanup was observed in Git, not retested as a third release snapshot.

Blocking for a completely green release-check claim:

- `research/2026-11-14_astra_synthesis/audit.py:12` still exits 1, now at 5,910 words against the 5,000-word ceiling. The protected synthesis owner must reconcile the document and its gate.
- The optional review command in the shared-figure README, `research/2026-11-14_sol_figures-polish/proofs.py:67`, exits 1 because Figure 17 has eight caption lines. Its 3-by-3 contact-sheet canvas also clips a 10-page gallery. The figure owner must decide the caption/layout correction; no assertion was weakened here.

Non-blocking for compiling and reading the current products:

- The figure-24 standalone overfull box, one embedded Type 3 atlas font, historical-draft drift, duplicate/large records, local paths in historical scripts, pending concurrent-run reports and reader-facing process residue remain inventoried.
- Historical primal/involution generators do not reproduce the final edited edition; the corrected READMEs now identify the committed TeX sources and guard those stale generators.
- The atlas failure and missing descent-certificate link from the first pin are resolved at the later pin.

All requested current document products can be built from tracked source inputs at the tested pins with the documented direct-tool alternatives. The repository is not completely green because the two commands above still fail. No mathematical result or figure content was changed to obtain a pass.


## Clone cleanup

Both clone paths were resolved and verified outside the shared workspace. Automatic approval review rejected recursive Remove-Item deletion as "blocked by policy", including a retry using the exact verified literal path. Neither clone was deleted. They remain at E:/rc-sol-1114 and E:/rc-sol-late. See logs/clone-cleanup.txt. No alternative deletion mechanism was used to bypass that rejection.

<!-- COMMAND LEDGER -->
## Exact command ledger

Commands execute sequentially. All unqualified working directories are relative to the indicated fresh clone. A nonzero code is a recorded failure, not an omitted check.

### E:/rc-sol-1114, blueprint-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 0.82 | `git clone --filter=blob:none --no-checkout https://github.com/openai/math.git research/2026-11-14_opus_blueprint/upstream/openai-math` |
| . | 0 | 0.03 | `git -C research/2026-11-14_opus_blueprint/upstream/openai-math sparse-checkout set lean/OAI/Combinatorics/Hamiltonian lean/ComparatorChallenges` |
| . | 0 | 1.67 | `git -C research/2026-11-14_opus_blueprint/upstream/openai-math checkout 4eaee87548250b2682affda7d05d947c05554bae` |
| . | 0 | 0.3 | `python -I research/2026-11-14_opus_lean-integration/scripts/lean_sigs.py research/2026-11-14_opus_blueprint/upstream/openai-math/lean/OAI/Combinatorics/Hamiltonian research/2026-11-14_opus_lean-integration/data/lean-sigs-upstream.json` |
| . | 0 | 0.05 | `python -I research/2026-11-14_opus_lean-integration/scripts/lean_sigs.py proofs/lean/Devices research/2026-11-14_opus_lean-integration/data/lean-sigs-devices.json` |
| . | 0 | 0.14 | `python -I research/2026-11-14_opus_lean-integration/scripts/extract_tex.py` |
| . | 0 | 1.93 | `python -I research/2026-11-14_opus_lean-integration/scripts/build_blueprint.py` |
| . | 0 | 0.09 | `python -I research/2026-11-14_opus_lean-integration/scripts/status_table.py` |

### E:/rc-sol-1114, code-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 7.91 | `python -X utf8 -B workings/barnette_lab/setup_plantri.py` |
| . | 0 | 20.54 | `python -X utf8 -B workings/barnette_lab/run_tests.py quick` |
| . | 0 | 226.34 | `python -X utf8 -B workings/barnette_lab/run_tests.py full` |
| . | 0 | 11.1 | `python -X utf8 -B digestions/route-map/build_map.py` |
| . | 0 | 0.1 | `git diff --stat -- digestions/route-map` |
| . | 0 | 0.87 | `git diff -- digestions/route-map` |
| . | 0 | 0.29 | `python -X utf8 -B labyrinth/make_frontier.py` |
| . | 0 | 0.12 | `python -X utf8 -B labyrinth/seed.py` |
| . | 0 | 0.09 | `python -X utf8 -B labyrinth/lab.py check` |
| . | 0 | 0.1 | `python -X utf8 -B labyrinth/lab.py build` |
| . | 0 | 0.23 | `python -X utf8 -B research/2026-11-14_astra_synthesis/count.py` |
| . | 0 | 0.06 | `python -X utf8 -B research/2026-11-14_astra_synthesis/evidence.py` |
| . | 1 | 0.08 | `python -X utf8 -B research/2026-11-14_astra_synthesis/audit.py` |
| . | 0 | 0.08 | `python -X utf8 -B research/2026-11-14_astra_synthesis/snapshot.py` |

### E:/rc-sol-1114, compare-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 0.46 | `pdffonts E:\rc-sol-1114\paper\main\barnette.pdf` |
| . | 0 | 0.33 | `pdffonts E:\rc-sol-1114\proofs\primal\primal.pdf` |
| . | 0 | 0.44 | `pdffonts E:\rc-sol-1114\proofs\involutions\involutions.pdf` |
| . | 0 | 0.43 | `pdffonts E:\rc-sol-1114\digestions\atlas\atlas.pdf` |
| . | 0 | 0.29 | `pdffonts E:\rc-sol-1114\paper\figures\gallery.pdf` |
| . | 0 | 0.34 | `pdffonts E:\rc-sol-1114\paper\draft-A\barnette.pdf` |
| . | 0 | 0.33 | `pdffonts E:\rc-sol-1114\paper\draft-B\barnette.pdf` |

### E:/rc-sol-1114, documents-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| paper/main | 1 | 0.28 | `latexmk -pdf -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/main | 0 | 1.51 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/main | 0 | 0.28 | `bibtex barnette` |
| paper/main | 0 | 1.49 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/main | 0 | 1.49 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| proofs/primal | 0 | 3.39 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/primal | 0 | 3.35 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/primal | 0 | 3.38 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/involutions | 0 | 1.67 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| proofs/involutions | 0 | 1.61 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| proofs/involutions | 0 | 1.59 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| paper/draft-A | 0 | 1.31 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/draft-A | 0 | 0.26 | `bibtex barnette` |
| paper/draft-A | 0 | 1.34 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/draft-A | 0 | 1.28 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/draft-B | 0 | 1.87 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/draft-B | 0 | 0.25 | `bibtex barnette` |
| paper/draft-B | 0 | 1.84 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/draft-B | 0 | 1.86 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| . | 0 | 8.27 | `python -X utf8 -B research/2026-11-14_astra_primal-revision/build.py` |

### E:/rc-sol-1114, figures-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 311.18 | `python -X utf8 -B paper/figures/build.py` |
| . | 0 | 0.54 | `python -X utf8 -B paper/figures/geometry_check.py` |
| . | 0 | 1.09 | `python -X utf8 -B paper/figures/crosscheck_lab.py` |
| . | 0 | 8.68 | `python -X utf8 -B proofs/primal/figures/check.py --build` |
| . | 1 | 53.9 | `python -X utf8 -B digestions/atlas/build.py` |
| . | 1 | 8.36 | `python -X utf8 -B digestions/atlas/verify.py` |
| . | 0 | 70.97 | `python -X utf8 -B research/2026-11-14_sol_involutions-revision/code/check.py 14` |
| . | 0 | 170.55 | `python -X utf8 -B research/2026-11-14_sol_involutions-revision/code/referee_rerun.py` |
| . | 0 | 11.82 | `python -X utf8 -B research/2026-11-14_sol_involutions-revision/code/drawings.py` |
| . | 0 | 1.21 | `python -X utf8 -B research/2026-11-14_sol_involutions-revision/code/figures.py` |
| . | 0 | 0.08 | `python -X utf8 -B research/2026-11-14_fable_referee-involutions-v2/code/figure2.py` |

### E:/rc-sol-1114, pristine-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| proofs/primal | 0 | 3.41 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/primal | 0 | 3.45 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/involutions | 0 | 1.65 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| proofs/involutions | 0 | 1.66 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| digestions/atlas | 0 | 1.41 | `pdflatex -interaction=nonstopmode -halt-on-error atlas.tex` |
| digestions/atlas | 0 | 1.08 | `pdflatex -interaction=nonstopmode -halt-on-error atlas.tex` |

### E:/rc-sol-1114, supplement-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 14.94 | `python -X utf8 -B research/2026-11-14_sol_figures-polish/check_hunch.py` |
| . | 1 | 4.59 | `python -X utf8 -B research/2026-11-14_sol_figures-polish/proofs.py` |
| . | 0 | 1.55 | `python -X utf8 -B research/2026-11-14_astra_primal-revision/check_cancellation.py 15` |
| . | 0 | 7.2 | `python -X utf8 -B research/2026-11-14_astra_primal-revision/check_cancellation.py 16` |
| . | 0 | 1.57 | `python -X utf8 -B research/2026-11-14_astra_primal-revision/inspect_figures.py` |

### E:/rc-sol-late, code-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 7.29 | `python -X utf8 -B workings/barnette_lab/setup_plantri.py` |
| . | 0 | 19.71 | `python -X utf8 -B workings/barnette_lab/run_tests.py quick` |
| . | 0 | 223.71 | `python -X utf8 -B workings/barnette_lab/run_tests.py full` |
| . | 0 | 11.08 | `python -X utf8 -B digestions/route-map/build_map.py` |
| . | 0 | 0.11 | `git diff --stat -- digestions/route-map` |
| . | 0 | 0.83 | `git diff -- digestions/route-map` |
| . | 0 | 0.25 | `python -X utf8 -B labyrinth/make_frontier.py` |
| . | 0 | 0.14 | `python -X utf8 -B labyrinth/seed.py` |
| . | 0 | 0.1 | `python -X utf8 -B labyrinth/lab.py check` |
| . | 0 | 0.14 | `python -X utf8 -B labyrinth/lab.py build` |
| . | 0 | 0.72 | `python -X utf8 -B research/2026-11-14_astra_synthesis/count.py` |
| . | 0 | 0.07 | `python -X utf8 -B research/2026-11-14_astra_synthesis/evidence.py` |
| . | 1 | 0.12 | `python -X utf8 -B research/2026-11-14_astra_synthesis/audit.py` |
| . | 0 | 0.09 | `python -X utf8 -B research/2026-11-14_astra_synthesis/snapshot.py` |

### E:/rc-sol-late, compare-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 0.39 | `pdffonts E:\rc-sol-late\paper\main\barnette.pdf` |
| . | 0 | 0.34 | `pdffonts E:\rc-sol-late\proofs\primal\primal.pdf` |
| . | 0 | 0.31 | `pdffonts E:\rc-sol-late\proofs\involutions\involutions.pdf` |
| . | 0 | 0.42 | `pdffonts E:\rc-sol-late\digestions\atlas\atlas.pdf` |
| . | 0 | 0.3 | `pdffonts E:\rc-sol-late\paper\figures\gallery.pdf` |
| . | 0 | 0.32 | `pdffonts E:\rc-sol-late\paper\draft-A\barnette.pdf` |
| . | 0 | 0.35 | `pdffonts E:\rc-sol-late\paper\draft-B\barnette.pdf` |
| . | 0 | 0.32 | `pdffonts E:\rc-sol-late\proofs\sign-free\sign-free.pdf` |

### E:/rc-sol-late, late-atlas-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| . | 0 | 61.11 | `python -X utf8 -B digestions/atlas/build.py` |
| . | 0 | 11.52 | `python -X utf8 -B digestions/atlas/verify.py` |

### E:/rc-sol-late, late-docs-commands

| Working directory | Return | Seconds | Command |
| --- | --- | ---: | --- |
| paper/main | 0 | 1.61 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/main | 0 | 0.37 | `bibtex barnette` |
| paper/main | 0 | 1.54 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| paper/main | 0 | 1.52 | `pdflatex -interaction=nonstopmode -halt-on-error barnette.tex` |
| proofs/primal | 0 | 3.43 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/primal | 0 | 3.41 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/primal | 0 | 3.37 | `pdflatex -interaction=nonstopmode -halt-on-error primal.tex` |
| proofs/involutions | 0 | 1.78 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| proofs/involutions | 0 | 1.58 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| proofs/involutions | 0 | 1.65 | `pdflatex -interaction=nonstopmode -halt-on-error involutions.tex` |
| proofs/sign-free | 0 | 3.61 | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` |
| proofs/sign-free | 0 | 3.56 | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` |
| proofs/sign-free | 0 | 3.52 | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` |
| digestions/atlas | 0 | 1.25 | `pdflatex -interaction=nonstopmode -halt-on-error atlas.tex` |
| digestions/atlas | 0 | 1.08 | `pdflatex -interaction=nonstopmode -halt-on-error atlas.tex` |
| digestions/atlas | 0 | 1.12 | `pdflatex -interaction=nonstopmode -halt-on-error atlas.tex` |
| . | 0 | 7.58 | `python -X utf8 -B workings/barnette_lab/setup_plantri.py` |
| proofs/sign-free/figures | 0 | 1.81 | `python -X utf8 -B make_figs.py` |
| proofs/sign-free/figures | 0 | 0.28 | `python -X utf8 -B check.py` |
| research/2026-11-14_fable_sign-free-note/code | 0 | 66.78 | `python -X utf8 -B verify.py 6 12 ../data/release_verify_6_12.json` |
| research/2026-11-14_fable_sign-free-note/code | 0 | 0.07 | `python -X utf8 -B tex2md.py ../../../proofs/sign-free/sign-free.tex ../../../proofs/sign-free/SIGN-FREE.md` |
| proofs/sign-free | 0 | 3.56 | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` |
| proofs/sign-free | 0 | 3.51 | `pdflatex -interaction=nonstopmode -halt-on-error sign-free.tex` |

### Evidence scripts

From the shared repository root, where `R=research/2026-11-14_sol_release-check`:

```powershell
$R = 'research/2026-11-14_sol_release-check'
python -B $R/run.py E:/rc-sol-1114 $R/logs baseline
python -B $R/scan.py E:/rc-sol-1114 $R/logs
python -B $R/paths.py E:/rc-sol-1114 $R/logs
python -B $R/route_compare.py E:/rc-sol-1114 $R/logs
python -B $R/pdf_privacy.py E:/rc-sol-1114 $R/logs
python -B $R/scan.py E:/rc-sol-late $R/logs/late
python -B $R/paths.py E:/rc-sol-late $R/logs/late
python -B $R/route_compare.py E:/rc-sol-late $R/logs/late
python -B $R/summarize.py
python -B $R/append_commands.py
```

Run baseline before any product rebuild. The runner phases used are baseline, code, figures, documents, compare, blueprint, pristine, supplement, late-docs and late-atlas. Each phase is invoked as `python -B $R/run.py CLONE LOGDIR PHASE`; its expanded child commands are the ledger above. `pristine` restores exact tracked inputs only inside the disposable clone. `figures` and `late-atlas` delete disposable cloned atlas figure PDFs to force real compilation rather than reuse the committed PDFs.
