"""Rerun unchanged legacy family/polynomial checks, redirecting every output here."""
import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
root=Path.cwd();out=root/'research/2026-11-14_sol_involutions-revision'
d=json.loads((out/'verification.json').read_text());rows=[]
for r in d['rows']:
    if r['mode']=='ray':rows.append(dict(r,lowest_coefficient=r.get('moment')))
(out/'census.json').write_text(json.dumps(dict(command='code/legacy_checks.py, derived from verification.json ray rows',rows=rows)))
for name in ('extras.py','more_checks.py'):
    src=(root/'research/2026-11-14_sol_li-completion'/name).read_text()
    src=src.replace('from verify import *',"from base import *\nOUT=Path(r'"+str(out)+"')")
    src=src.replace('python research/2026-11-14_sol_li-completion/'+name,'python research/2026-11-14_sol_involutions-revision/code/legacy_checks.py')
    exec(compile(src,name,'exec'),dict(__name__='__main__',__file__=str(out/'code/legacy_checks.py')))
