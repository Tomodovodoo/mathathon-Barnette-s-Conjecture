from pathlib import Path
import json,re
D=Path('research/2026-11-14_astra_lean-check')
with (D/'REPORT.md').open('a',encoding='utf-8') as f:f.write('\nCOMPUTED cleanup: the guarded PowerShell removal of E:/lb2 succeeded in 42.62 seconds. The directory no longer exists; E:/lbb remains present and was only read for the cache copy. cleanup.out records the checked target, upstream HEAD, timestamps and postconditions. No Lean or Lake process from the review remains.\n')
(D/'REVIEW-STATE.md').write_text('Review complete. The fresh rebuild and targeted proof-route replacement pass. TODO T5, the whole-Lemma-4.5 wording and the literal no-polynomial-dependencies wording do not. Canonical statuses were not changed. See REPORT.md for the final verdict and all deliverables. E:/lb2 has been removed; E:/lbb was not modified.\n',encoding='utf-8')
required=['BUILD-LOG.md','AXIOMS.txt','FAITHFULNESS.md','REACHABILITY.md','RECOUNT.md','REPORT.md']
assert all((D/f).stat().st_size>100 for f in required)
assert len(re.findall(r'^## \d+\.',(D/'FAITHFULNESS.md').read_text(encoding='utf-8'),re.M))==29
assert len(json.loads((D/'recount.json').read_text())['rows'])==34
assert 'Types structurally identical' in (D/'replacement-walk.out').read_text(encoding='utf-8')
assert not Path('E:/lb2').exists() and Path('E:/lbb').exists()
assert json.loads((D/'input-changes-at-finish.json').read_text())==[]
print('All six deliverables present; 29 theorem entries; 34 recount entries; type identity and cleanup confirmed.')
