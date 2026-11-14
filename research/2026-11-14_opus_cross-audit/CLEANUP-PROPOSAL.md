# Cleanup proposal (nothing here has been deleted)

For the coordinator. Sizes are bytes on disk at survey time (data/hygiene.json). "Recommend" is my suggestion; each item needs the owning folder's agreement or the coordinator's decision. Total tracked size 305 MB; the items below account for roughly 150 MB.

## A. Large data files

| ID | Path | Size | Why it looks removable | Recommendation |
| --- | --- | --- | --- | --- |
| A1 | research/2026-11-14_astra_cycle-covers/data/record-24.txt | 37.6 MB | Raw plantri-style record dump for 24 vertices, regenerable from the census command; the folder's reports cite summaries. | Replace by a gzip copy (text compresses about 10:1) or by the generating command plus a checksum. |
| A2 | research/2026-11-14_astra_cycle-covers/data/record-22.txt | 1.9 MB | Same kind. | Gzip with A1. |
| A3 | research/2026-11-14_sol_route-algebra/counts.json, gauges.json | 15.5 MB, 2.1 MB | Full per-instance outputs; REPORT.md and ROUTES.md cite only aggregates. | Keep a summary JSON and the command; gzip or drop the full dump. |
| A4 | research/2026-11-14_opus_two-tree-packing/data/census_V16-17.json, census_V6-15.json, census_V13-15.json | 9.5, 1.2, 1.1 MB | Census outputs; V13-15 overlaps V6-15. | Check whether V13-15 is a strict subset of V6-15; if so drop it. Gzip the rest. |
| A5 | research/2026-11-14_fable_referee-determinants/code/results.json; research/2026-11-14_astra_referee-combinatorics/code/up_to_16.json; research/2026-11-14_fable_route-combinatorics/data/rows_v16.json; research/2026-11-14_fable_route-categorical/data/four_cuts_v15.json; research/2026-11-14_astra_limits/data/roots.json; research/2026-11-14_opus_referee-involutions/code/out/census-14.json; research/2026-11-14_opus_lean-formalisation/graph/lean-decls.json | 1.0 to 2.5 MB each, about 12 MB together | Machine output, regenerable. | Low priority. Gzip if the repository size matters. |
| A6 | research/2026-11-14_astra_audit-digestions/outputs/canonical-changes.patch | 2.8 MB | A patch already applied to digestions/; git history holds the same diff. | Drop, or keep a pointer to the commit that applied it. |

## B. Large binaries and duplicated renders

| ID | Path | Size | Why | Recommendation |
| --- | --- | --- | --- | --- |
| B1 | research/2026-11-14_sol_figures-polish/after-proof.pdf, deuteranopia-proof.pdf, greyscale-proof.pdf | 17.8, 17.8, 5.9 MB | Rasterised proof sheets of an earlier figure pass. The figures have since been redrawn (fable_figures-review, atlas). REVIEW.md links the greyscale and deuteranopia sheets. | Replace by low-resolution PNG contact sheets (under 1 MB each) or drop; the review text keeps its conclusions. |
| B2 | research/2026-11-14_fable_coldread-main/pages/p01-p17.png and research/2026-11-14_sol_referee-main/pages/page-01..17.png | 5.2 MB duplicated | Byte-identical page renders of the same paper/main build, made by two referees. | Keep one set (or neither: they are regenerable from the PDF at a known commit). |
| B3 | digestions/atlas/renders/*.png and research/2026-11-14_fable_atlas-review/after/*.png | 6.0 MB duplicated | Byte-identical. The atlas is being redrawn, so both sets will go stale. | After the redraw, keep renders only in digestions/atlas/renders/; the review folder can cite the commit. |
| B4 | research/2026-11-14_astra_primal-revision/renders/ | 6.2 MB | Page renders of primal.pdf at the revision commit; superseded by the rebuilt PDF. | Drop or keep only the contact sheets. |
| B5 | research/2026-11-14_fable_figures-review vs research/2026-11-14_sol_figures-polish vs paper/figures | 1.9 MB duplicated across 2 or 3 copies | Same figure PNGs copied between passes. | Keep paper/figures/ as the single source. |
| B6 | digestions/route-map/route-map.png, route-map.svg | 1.8, 1.3 MB | Large but current; the SVG is the source of the PNG. | Keep; optionally drop the PNG if the SVG renders on GitHub. |

## C. Literature copies

| ID | Path | Size | Why | Recommendation |
| --- | --- | --- | --- | --- |
| C3 | Four PDFs present both in papers/ and in research/2026-11-14_opus_history-literature/pdf/ (Shao-Wu 2025, Bekos et al. 2025, Gorsky-Steiner-Wiederrecht 2022, Bagheri Gh. et al. 2022), and one in both history-literature and sol_machinery-literature (Hine-Kalman 2018) | 2.5 MB duplicated | Byte-identical (same sha256). papers/ is the curated library per the README. | Delete the research copies and point the research reports to papers/. |
| C4 | research/2026-11-14_sol_machinery-literature/pdf/ (28 PDFs) | 41.6 MB | Third-party papers stored in a research folder. Some are large book chapters or surveys (bms-constellations 9.0 MB, schrijver-matroid-intersection 7.1 MB, propp-orientations 5.1 MB). The README asks that literature live in papers/ and that it be trimmed to what is relevant. Redistribution rights for published versions are a separate question I did not check. | Move the few that the proof uses into papers/ with bibliographic notes; replace the rest by a reference list with arXiv/DOI links. |
| C5 | research/2026-11-14_opus_history-literature/pdf/ | 11.4 MB in folder | Same issue on a smaller scale. | Same. |

## D. Build artefacts I was not allowed to untrack

| ID | Path | Size | Recommendation |
| --- | --- | --- | --- |
| C1 | proofs/involutions/involutions.aux, involutions.log, involutions.out | 38 KB | Untrack (`git rm --cached`) after the involutions referee finishes; add a proofs/involutions/.gitignore like proofs/primal's. |
| C2 | paper/main/barnette.bbl, paper/draft-B/barnette.bbl | 7 KB | Keep only if the .bbl is wanted for arXiv; otherwise untrack after the paper revision lands. |

## E. Empty, orphaned or stale files

| ID | Path | Size | Why | Recommendation |
| --- | --- | --- | --- | --- |
| E1 | research/2026-11-14_astra_cycle-covers/data/record-7.txt, record-9.txt | 0 | Empty. Probably correct (no records at that order: there is no 7-vertex Eulerian triangulation, and order 9 may have none of the recorded kind), but an empty file does not say so. | Replace by a one-line note "no records at V = 7" or drop. |
| E2 | research/2026-11-14_fable_referee-primal/code/out/lemmas_14.err | 0 | Empty stderr capture. | Drop. |
| E3 | paper/draft-A/, paper/draft-B/ | small | Superseded by paper/main/ (the merge). | Keep as history or move under paper/history/ once the revision of paper/main/ lands. |
| E4 | proofs/primal/EXAMPLES.md and STATUS.md "Exact finite range" | small | Describe the first version's 20-vertex worked example, not the current 22-vertex running example. Accurate as history. | Label both sections "first version" (I did not change them beyond the phase section). |
| E5 | research/2026-11-14_astra_primal-revision/revise.py | small | Its README says not to run it; historical patch. | Keep, already labelled. |

## F. Structure

| ID | Item | Recommendation |
| --- | --- | --- |
| C9 | research/2026-11-14_opus_blueprint/upstream/ is an untracked clone with no .gitignore | Add `upstream/` to that folder's .gitignore so nobody commits it with `git add <folder>`. |
| C10 | research/ and labyrinth/ are not in the README layout table | Add two rows to README.md. |
| C11 | research/INDEX.md lacks 12 folders (HYGIENE.md, Section 4) | Add rows when those runs report. |
| C12 | `*.log` and `*.out` cannot be ignored globally without hiding computation transcripts | Ask agents to name LaTeX logs inside a LaTeX folder with a local .gitignore, and computation logs under data/ or out/. |
