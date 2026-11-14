from pathlib import Path
import json,re,subprocess,fitz
O=Path(__file__).resolve().parent;L=O/'logs';R=Path('E:/rc-sol-late')
w=[]
for p in (R/'digestions/atlas').rglob('*.log'):
 for n,line in enumerate(p.read_text(errors='replace').splitlines(),1):
  if any(float(x)>2 for x in re.findall(r'Overfull \\[hv]box \(([0-9.]+)pt',line)):w.append(dict(file=p.relative_to(R).as_posix(),line=n,text=line))
(L/'atlas-warnings.json').write_text(json.dumps(w,indent=2))
with fitz.open(stream=subprocess.check_output(['git','show','HEAD:digestions/atlas/atlas.pdf'],cwd=R),filetype='pdf') as a,fitz.open(R/'digestions/atlas/atlas.pdf') as b:
 (L/'atlas-comparison.json').write_text(json.dumps(dict(committed_pages=len(a),rebuilt_pages=len(b),text_equal=''.join(p.get_text() for p in a)==''.join(p.get_text() for p in b)),indent=2))
commit=(L/'commit.txt').read_text().strip()
text=f'''# Final recheck

COMPUTED. Snapshot `{commit}`, fetched from origin/main and checked out detached in `E:/rc-sol-late`. This is a build and finite-test check, not a mathematical proof audit.

The clone retained plantri/vendor inputs from the earlier release check. Tracked inputs were restored to origin/main before checkout; the first checkout attempt failed because the worktree restoration had not updated the index. Restoring both index and worktree resolved it. The old untracked release_verify_6_12.json was not used. Setup_plantri ran again successfully. Dependencies are those pinned in requirements.txt.

## Results

- GREEN: main, primal, involution and sign-free direct builds passed, at 20, 15, 18 and 11 pages. Each matches the committed PDF's extracted text exactly before the mechanical fixes. Main used pdflatex, bibtex, then two pdflatex passes; the inline-bibliography notes used three pdflatex passes.
- GREEN: no errors, undefined citations/references or overfull boxes above 2pt in the four final document logs, including the corrected involution build.
- GREEN: extracted main bibliography contains none of `content checked`, `not opened`, `research/`, `Wikipedia`.
- GREEN: atlas full rebuild with all figure PDFs removed first, and verify.py; primal figure check with --build; sign-free figure check; paper figure check; plantri setup; quick lab tests; Labyrinth check; route-map regeneration.
- GREEN: route-map PDF text and pixels match; SVGs match after date/ID normalization. Raw diff is logs/22.txt. No route-map edits were copied back.
- GREEN: requested Markdown link scopes have zero broken links. At the snapshot, no research folders lack REPORT.md and none are missing from INDEX. This new report folder postdates that snapshot and is deliberately not added to the protected index.
- GREEN: citation validator passes after ignoring note/annote fields. The comparison preserves all remaining entry bytes. Ran in the disposable clone so its generated validation and metadata reports did not alter the other agent's folder in the shared tree.
- GREEN: inline OAI and trees references confidently match canonical OpenAI2026 and Anonymous2026. Full publication identification replaces local-source wording; the unsigned manuscript has no public URL in the canonical entry. Corrected PDF is still 18 pages.
- RED/nonblocking: atlas standalone figure diagnostics are listed in logs/atlas-warnings.json. No protected figure was changed.
- An initial sign-free check invocation from the root failed on figdata.json. The documented figure-directory invocation passed; both logs are retained.

## Reproduction and command ledger

Run `python -B research/2026-11-14_astra_final-recheck/run.py` from the shared repository root after preparing the pinned disposable clone. Then run `check_fixes.py` after applying the two source fixes, followed by `diagnostics.py` and `report.py`. The scripts use one child process at a time, each with a 540-second timeout. `fixes.py` records the source transformations and should not be rerun blindly because its README append is not idempotent.

Preparation commands, in E:/rc-sol-late: `git fetch origin`; `git restore --source=origin/main --worktree -- .`; failed `git checkout --detach origin/main`; `git restore --source=origin/main --staged --worktree -- .`; successful `git checkout --detach origin/main`; `git rev-parse HEAD`.

| Directory | Command | Exit | Seconds | Log |
|---|---|---:|---:|---|
'''
for row in json.loads((L/'commands.json').read_text())+json.loads((L/'fix-commands.json').read_text()):text+='| '+row['cwd']+' | `'+subprocess.list2cmdline(row['command'])+'` | '+str(row['code'])+' | '+str(row['seconds'])+' | '+row['log']+' |\n'
(O/'RECHECK.md').write_text(text,encoding='utf8')
(O/'REPORT.md').write_text('''# Final recheck report
COMPUTED: all four current documents reproduce their committed text and expected page counts.
COMPUTED: all requested figure, atlas, quick lab, Labyrinth and route checks pass.
COMPUTED: both authorized mechanical fixes pass validation; involutions stays at 18 pages.
COMPUTED: no broken Markdown links, absent reports or missing index rows at the pinned snapshot.
Open: standalone atlas figure overflow remains; later commits are outside this check.

I checked the changed release products at the commit recorded in RECHECK.md, then tested the two authorized fixes. Commands, results, diffs and diagnostics are in RECHECK.md and logs/; run.py and check_fixes.py record the checked scope.

- GREEN: direct builds, bibliography-note suppression, figure assertions, atlas verification, quick finite tests, Labyrinth consistency, normalized route reproduction, links and research inventory.
- GREEN: validator ignores only note/annote fields; papers/README.md explains why. Two certain inline bibliography matches now give canonical publication identification. Rebuilt PDF remains 18 pages.
- RED/nonblocking: standalone atlas overfull box diagnostics remain in logs/atlas-warnings.json. The initial sign-free run failed only because I used the wrong working directory; the corrected command passed.

No mathematical validity claim follows from these mechanical checks. No uncertain bibliography match was substituted. No synthesis or protected figure edits were made. There are no missing-report or missing-index folders to list at the tested commit; this new run itself needs coordinator indexing after publication.

The three best next steps are to index this report, let the atlas owner address the standalone overflow, and rerun affected checks for any later source edits.
''',encoding='utf8')
print(w)
