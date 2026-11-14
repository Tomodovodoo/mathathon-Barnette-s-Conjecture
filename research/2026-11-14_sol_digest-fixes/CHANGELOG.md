# Changelog

- Rewrote 00-overview.md around the final manuscript recovery route and compact dependency diagram.
- Rewrote 09-what-is-still-open.md with precise descent/lattice names, readable induction witnesses and late-review qualifications.
- Updated routes.py, figure subtitles and generated route-map outputs. Updated current labyrinth source rows and regenerated data/dashboard; preserved historical events.
- Verified current atlas numbering against atlas.pdf and clarified its contents-page offset in the README index.
- Added finite recomputation, source arithmetic, full reference-lab replay, atlas-index, build and link-check evidence in this research folder.

## Reproduce checks from the repository root

```powershell
python -X utf8 -B research/2026-11-14_sol_digest-fixes/code/recompute.py
python -X utf8 -B research/2026-11-14_sol_digest-fixes/code/recheck.py
python -X utf8 -B workings/barnette_lab/run_tests.py full --output research/2026-11-14_sol_digest-fixes/lab-replay
python -X utf8 -B digestions/route-map/build_map.py
python -X utf8 -B labyrinth/make_frontier.py
python -X utf8 -B research/2026-11-14_sol_digest-fixes/code/verify_build.py
python -X utf8 -B research/2026-11-14_sol_digest-fixes/code/linkcheck.py
```

The edit_*.py, finish_edits.py, late_source.py and final_source.py files record the implementation steps. They are not rebuild entry points. Some depend on intermediate text and should not be replayed over the finished documents. routes.py is the canonical catalogue; the commands above rebuild its derived outputs. recheck.py reuses the second auditor's implementation without running its write-to-own-folder entry point.
